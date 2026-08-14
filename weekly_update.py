# -*- coding: utf-8 -*-
"""
AI Research Tracker - 每周论文更新脚本（v2）
两阶段：
  阶段一：arXiv 抓取 + Semantic Scholar 引用数据 → 精选 top 20 候选
  阶段二：由 Agent 用模型评估影响力 → 筛选 0-5 篇 → 写中文摘要
  注意：阶段二写入 weekly-update/ 暂存区，不自动同步到各分支
"""
import json, os, re, sys, ssl, urllib.request, urllib.parse, urllib.error, xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

# Windows 控制台编码兼容
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(r"D:\ai_research")
DOCS_DIR = BASE_DIR / "docs" / "categories"
CACHE_DIR = BASE_DIR / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

# ── 9 大领域 ──
DOMAINS = {
    "llm": {
        "name": "大语言模型",
        "keywords": [
            "large language model", "transformer", "LLM", "GPT", "instruction tuning",
            "alignment", "RLHF", "DPO", "MoE", "scaling law", "chain of thought",
            "reasoning", "in-context learning", "RL for LLM", "agent", "function calling"
        ],
        "exclude": ["vision", "image", "diffusion", "audio", "speech"]
    },
    "vision": {
        "name": "计算机视觉",
        "keywords": [
            "computer vision", "image recognition", "object detection",
            "segmentation", "visual transformer", "ViT", "3D reconstruction",
            "neural rendering", "gaussian splatting", "video understanding",
            "visual foundation model", "SAM", "DINO"
        ],
        "exclude": ["language model", "text generation", "NLP"]
    },
    "multimodal": {
        "name": "多模态",
        "keywords": [
            "multimodal", "vision-language", "VLM", "CLIP", "image caption",
            "visual question answering", "VQA", "document understanding",
            "multimodal learning", "speech-text", "audio-visual"
        ],
        "exclude": []
    },
    "agents": {
        "name": "AI Agent",
        "keywords": [
            "AI agent", "planning", "tool use", "function calling", "ReAct",
            "autonomous agent", "multi-agent", "collaboration", "computer use",
            "web agent", "code agent", "agentic", "MCP"
        ],
        "exclude": ["reinforcement learning"]
    },
    "generative-models": {
        "name": "生成式模型",
        "keywords": [
            "generative model", "diffusion", "flow matching", "score-based",
            "text-to-image", "image generation", "video generation",
            "consistency model", "3D generation", "DiT", "transformer diffusion",
            "music generation", "audio generation"
        ],
        "exclude": ["language model", "text generation language"]
    },
    "reinforcement-learning": {
        "name": "强化学习",
        "keywords": [
            "reinforcement learning", "policy gradient", "PPO", "actor-critic",
            "RLHF", "reward modeling", "preference learning",
            "offline RL", "inverse RL", "GRPO", "process reward model",
            "reinforcement learning LLM", "RL for reasoning"
        ],
        "exclude": []
    },
    "efficient-training": {
        "name": "高效训练与推理",
        "keywords": [
            "efficient training", "quantization", "LoRA", "parameter-efficient",
            "knowledge distillation", "model compression", "pruning",
            "flash attention", "KV cache", "speculative decoding",
            "PagedAttention", "vLLM", "SGLang", "continuous batching",
            "FP8 training", "MoE efficient"
        ],
        "exclude": []
    },
    "robotics": {
        "name": "机器人与具身智能",
        "keywords": [
            "robot", "robotics", "embodied", "manipulation", "grasping",
            "imitation learning robot", "robot foundation model",
            "VLA", "visual-language-action", "Sim2Real", "motion planning",
            "world model robot", "dexterous", "humanoid", "diffusion policy"
        ],
        "exclude": []
    },
    "ai-safety": {
        "name": "AI安全与对齐",
        "keywords": [
            "AI safety", "alignment", "RLHF safety", "red teaming",
            "hallucination", "jailbreak", "adversarial", "interpretability",
            "mechanistic interpretability", "sparse autoencoder",
            "model privacy", "watermark", "AI governance",
            "constitutional AI", "superalignment"
        ],
        "exclude": []
    }
}


def fetch_arxiv(domain_config, max_results=50, max_retries=2):
    """从 arXiv API 抓取论文，按相关度排序"""
    import time, ssl
    keywords = domain_config["keywords"]
    exclude = domain_config.get("exclude", [])

    # 构建查询词（不包含外层括号）
    parts = []
    for kw in keywords:
        if ' ' in kw:
            parts.append(f'all:"{kw}"')
        else:
            parts.append(f'all:{kw}')
    include_q = " OR ".join(parts)
    query = f"({include_q})"

    # 日期范围（近一周新提交，YYYYMMDD 格式）
    date_from = (datetime.now() - timedelta(days=8)).strftime('%Y%m%d')
    date_to = datetime.now().strftime('%Y%m%d')

    # 重要：submittedDate 必须在 AND NOT 排除条件之前，
    # 否则 arXiv API 会静默丢弃日期筛选，返回所有历史结果。
    raw_search = f"{query} AND submittedDate:[{date_from} TO {date_to}]"
    if exclude:
        for e in exclude:
            if ' ' in e:
                raw_search += f" AND NOT all:\"{e}\""
            else:
                raw_search += f" AND NOT all:{e}"

    url = (f"https://export.arxiv.org/api/query?"
           f"search_query={urllib.parse.quote(raw_search)}&"
           f"start=0&max_results={max_results}&"
           f"sortBy=relevance&sortOrder=descending")

    print(f"    arXiv URL ({len(url)} chars)...")

    # SSL context for HTTPS
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # 重试逻辑
    for attempt in range(1 + max_retries):
        if attempt > 0:
            wait_time = 5 * (2 ** (attempt - 1))  # 5, 10s backoff
            print(f"    第 {attempt+1} 次尝试 (等待 {wait_time}s)...")
            time.sleep(wait_time)
        else:
            time.sleep(3.5)  # 基本延迟，避免 429

        try:
            with urllib.request.urlopen(url, timeout=60, context=ctx) as resp:
                xml_data = resp.read().decode('utf-8')
            break  # 成功，跳出重试循环
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                print(f"    HTTP 429 (限流)，准备重试...")
                continue
            print(f"    arXiv API HTTP 错误: {e.code} {e.reason}")
            if attempt >= max_retries:
                return []
        except Exception as e:
            if attempt < max_retries:
                print(f"    请求失败: {e}，准备重试...")
                continue
            print(f"    arXiv API 请求失败: {e}")
            return []

    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(xml_data)
    papers = []
    for entry in root.findall('atom:entry', ns):
        published = entry.find('atom:published', ns).text[:10]
        paper = {
            'title': entry.find('atom:title', ns).text.strip().replace('\n', ' '),
            'abstract': entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
            'arxiv_id': entry.find('atom:id', ns).text.split('/abs/')[-1],
            'published': published,
            'authors': [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)],
            'categories': [c.get('term') for c in entry.findall('atom:category', ns)],
            'link': entry.find('atom:id', ns).text,
        }
        papers.append(paper)
    return papers


def fetch_citations_semantic_scholar(arxiv_ids):
    """批量查询 Semantic Scholar 获取引用数"""
    if not arxiv_ids:
        return {}

    # 清理 arXiv ID（去掉版本号和空白）
    clean_ids = []
    for aid in arxiv_ids:
        aid = aid.strip().split('v')[0]  # 2404.07731v1 → 2404.07731
        clean_ids.append(f"arXiv:{aid}")

    body = json.dumps({"ids": clean_ids}).encode('utf-8')
    url = ("https://api.semanticscholar.org/graph/v1/paper/batch"
           "?fields=citationCount,influentialCitationCount")
    req = urllib.request.Request(url, data=body,
                                 headers={'Content-Type': 'application/json'})
    try:
        import time
        time.sleep(1)  # 避免 429 限流
        with urllib.request.urlopen(req, timeout=20) as resp:
            results = json.loads(resp.read().decode('utf-8'))
        citations = {}
        for r in results:
            if r and 'paperId' in r:
                ext_id = r.get('externalIds', {}).get('ArXiv', '')
                if ext_id:
                    citations[ext_id] = {
                        'citation_count': r.get('citationCount', 0),
                        'influential_count': r.get('influentialCitationCount', 0),
                    }
        return citations
    except Exception:
        # Semantic Scholar 不可用时降级，不影响主流程
        return {}


def score_paper(paper, citation_data):
    """综合评分"""
    arxiv_id = paper['arxiv_id'].strip().split('v')[0]  # 去版本号
    cit = citation_data.get(arxiv_id, {})
    citation_count = cit.get('citation_count', 0)
    influential_count = cit.get('influential_count', 0)
    # 引用分数（近一周论文引用通常很少，仅作辅助信号）
    cit_score = 1.0 + 0.1 * (citation_count + 2 * influential_count)
    return round(cit_score, 2), citation_count, influential_count


def main_fetch():
    """阶段一：抓取 arXiv + 引用数据 → 输出候选 JSON"""
    today = datetime.now()

    print(f"=== AI Research Tracker 周更任务 v2 ===")
    print(f"执行时间：{today.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    all_candidates = {}

    for slug, config in DOMAINS.items():
        print(f"[{config['name']}]")

        # 1. 抓取 arXiv（近一周新提交 × 按相关度取 40 篇）
        papers = fetch_arxiv(config, max_results=40)
        print(f"     找到 {len(papers)} 篇近一周论文")

        if not papers:
            all_candidates[slug] = []
            continue

        # 2. 查引用数
        arxiv_ids = [p['arxiv_id'].strip().split('v')[0] for p in papers]
        citations = fetch_citations_semantic_scholar(arxiv_ids)
        print(f"     查到引用数据 {len(citations)} 篇")

        # 3. 评分 + 排序
        scored = []
        for p in papers:
            s, cc, ic = score_paper(p, citations)
            scored.append((s, cc, ic, p))
        scored.sort(key=lambda x: -x[0])

        # 4. 取 top 20
        top20 = []
        for s, cc, ic, p in scored[:20]:
            entry = {
                'title': p['title'],
                'abstract': p['abstract'],
                'arxiv_id': p['arxiv_id'].strip(),
                'published': p['published'],
                'authors': p['authors'][:5],
                'categories': p['categories'],
                'link': p['link'],
                'score': s,
                'citation_count': cc,
                'influential_count': ic,
            }
            top20.append(entry)
            print(f"     [{s:.1f}] {p['title'][:70]}... (引用:{cc}, 影响力引用:{ic})")

        all_candidates[slug] = top20
        print()

    # 6. 写候选 JSON
    output = {
        'fetch_time': today.strftime('%Y-%m-%d %H:%M:%S'),
        'week': today.strftime('%Y-%m-%d'),
        'candidates': all_candidates,
    }

    # 也写入 weekly-update 目录方便 agent 读取
    candidates_path = BASE_DIR / '.cache' / 'weekly_candidates.json'
    candidates_path.parent.mkdir(exist_ok=True)
    with open(candidates_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"候选数据已保存: {candidates_path}")
    print(f"\n=== 阶段一完成 ===")
    print(f"下一步：Agent 用模型评估并筛选 0-5 篇/领域，写入中文摘要")

    return candidates_path


def main():
    """入口"""
    main_fetch()


if __name__ == '__main__':
    main()
