# -*- coding: utf-8 -*-
"""
阶段一替代脚本：使用 arxiv 包（v4 API）代替 urllib 直连旧版 API
输出与 weekly_update.py 完全兼容的 .cache/weekly_candidates.json
"""
import json, sys, time, os
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(r"D:\ai_research")
CACHE_DIR = BASE_DIR / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

DOMAINS = {
    "llm": {
        "name": "大语言模型",
        "arxiv_cats": ["cs.CL"],
        "extra_search": '"large language model" OR "chain of thought" OR "instruction tuning" OR RLHF OR DPO OR MoE OR "scaling law" OR "in-context learning"',
    },
    "vision": {
        "name": "计算机视觉",
        "arxiv_cats": ["cs.CV"],
        "extra_search": '"object detection" OR segmentation OR "3D reconstruction" OR "visual transformer" OR ViT OR "gaussian splatting" OR SAM',
    },
    "multimodal": {
        "name": "多模态",
        "arxiv_cats": ["cs.CV", "cs.CL", "cs.MM", "cs.SD"],
        "extra_search": 'multimodal OR "vision-language" OR VLM OR CLIP OR "visual question answering" OR VQA',
    },
    "agents": {
        "name": "AI Agent",
        "arxiv_cats": ["cs.AI", "cs.CL", "cs.MA"],
        "extra_search": '"AI agent" OR planning OR "tool use" OR "function calling" OR ReAct OR "autonomous agent" OR "multi-agent" OR MCP OR agentic',
    },
    "generative-models": {
        "name": "生成式模型",
        "arxiv_cats": ["cs.CV", "cs.LG", "cs.SD", "cs.MM"],
        "extra_search": 'diffusion OR "flow matching" OR "text-to-image" OR "image generation" OR "video generation" OR DiT OR "consistency model"',
    },
    "reinforcement-learning": {
        "name": "强化学习",
        "arxiv_cats": ["cs.LG", "cs.AI", "cs.RO", "stat.ML"],
        "extra_search": '"reinforcement learning" OR PPO OR "actor-critic" OR RLHF OR "reward modeling" OR GRPO OR "process reward model" OR "offline RL"',
    },
    "efficient-training": {
        "name": "高效训练与推理",
        "arxiv_cats": ["cs.LG", "cs.CL", "cs.AI", "cs.AR"],
        "extra_search": 'quantization OR LoRA OR "parameter-efficient" OR "knowledge distillation" OR "model compression" OR "flash attention" OR "KV cache" OR "speculative decoding" OR vLLM OR SGLang',
    },
    "robotics": {
        "name": "机器人与具身智能",
        "arxiv_cats": ["cs.RO", "cs.CV", "cs.AI"],
        "extra_search": 'robot OR robotics OR embodied OR manipulation OR grasping OR "imitation learning" OR "robot foundation model" OR VLA OR "diffusion policy" OR humanoid',
    },
    "ai-safety": {
        "name": "AI安全与对齐",
        "arxiv_cats": ["cs.AI", "cs.CL", "cs.CR", "cs.LG"],
        "extra_search": '"AI safety" OR alignment OR "red teaming" OR hallucination OR jailbreak OR interpretability OR "mechanistic interpretability" OR watermark OR "AI governance"',
    },
}

# 捕获 arxiv.Result 对象的简单容器类
class Paper:
    def __init__(self, result):
        self.title = result.title.replace('\n', ' ').strip()
        self.summary = result.summary.replace('\n', ' ').strip()
        self.entry_id = result.entry_id
        self.updated = result.updated.isoformat()[:10] if hasattr(result, 'updated') and result.updated else ''
        self.published = result.published.isoformat()[:10] if hasattr(result, 'published') and result.published else ''
        self.authors = [a.name for a in result.authors]
        # 提取 arxiv ID
        self.arxiv_id = self.entry_id.split('/abs/')[-1].split('/')[-1].split('v')[0] if '/abs/' in self.entry_id else self.entry_id.split('/')[-1].split('v')[0]
        # 类别
        self.categories = []
        if hasattr(result, 'categories'):
            self.categories = list(result.categories)
    
    def to_dict(self):
        return {
            'title': self.title,
            'abstract': self.summary,
            'arxiv_id': self.arxiv_id,
            'published': self.published,
            'authors': self.authors[:5],
            'categories': self.categories,
            'link': self.entry_id,
        }


def fetch_with_arxiv(slug, config):
    """使用 arxiv 包抓取"""
    import arxiv
    
    name = config['name']
    cats = config.get('arxiv_cats', [])
    extra = config.get('extra_search', '')
    
    print(f"[{name}]")
    
    # 构建查询：按分类 + 关键词
    cat_query = " OR ".join(f"cat:{c}" for c in cats) if cats else ""
    if extra:
        query = f"({extra})"
        if cat_query:
            query = f"({cat_query}) AND ({extra})"
    else:
        query = cat_query
    
    # 日期范围（近 8 天）
    date_from = datetime.now() - timedelta(days=8)
    
    papers = []
    try:
        client = arxiv.Client(
            page_size=100,
            delay_seconds=2.0,
            num_retries=3,
        )
        
        search = arxiv.Search(
            query=query,
            max_results=40,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
        
        results = list(client.results(search))
        
        # 过滤近一周的论文
        for r in results:
            pub_date = r.published.replace(tzinfo=None) if hasattr(r.published, 'replace') else r.published
            if pub_date < date_from:
                continue
            papers.append(Paper(r))
        
        print(f"     找到 {len(papers)} 篇近一周论文")
        
    except Exception as e:
        print(f"     arxiv 包请求失败: {type(e).__name__}: {e}")
    
    return papers


def fetch_citations_semantic_scholar(arxiv_ids):
    """批量查询 Semantic Scholar 获取引用数"""
    if not arxiv_ids:
        return {}
    clean_ids = []
    for aid in arxiv_ids:
        aid = aid.strip().split('v')[0]
        clean_ids.append(f"arXiv:{aid}")
    
    body = json.dumps({"ids": clean_ids}).encode('utf-8')
    url = ("https://api.semanticscholar.org/graph/v1/paper/batch"
           "?fields=citationCount,influentialCitationCount")
    req = urllib.request.Request(url, data=body,
                                 headers={'Content-Type': 'application/json'})
    try:
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
    except Exception as e:
        print(f"     Semantic Scholar 查询失败: {e}")
        return {}


def main():
    import urllib.request
    
    today = datetime.now()
    print(f"=== AI Research Tracker 阶段一（arxiv 包版）===")
    print(f"执行时间：{today.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_candidates = {}
    
    for slug, config in DOMAINS.items():
        # 1. 抓取
        papers = fetch_with_arxiv(slug, config)
        
        if not papers:
            all_candidates[slug] = []
            print()
            continue
        
        # 2. 查引用数
        arxiv_ids = [p.arxiv_id for p in papers]
        print(f"     正在查询 Semantic Scholar 引用数据...")
        citations = fetch_citations_semantic_scholar(arxiv_ids)
        print(f"     查到引用数据 {len(citations)} 篇")
        
        # 3. 评分
        scored = []
        for p in papers:
            cit = citations.get(p.arxiv_id, {})
            cc = cit.get('citation_count', 0)
            ic = cit.get('influential_count', 0)
            score = 1.0 + 0.1 * (cc + 2 * ic)
            scored.append((score, cc, ic, p))
        scored.sort(key=lambda x: -x[0])
        
        # 4. top 20
        top20 = []
        for s, cc, ic, p in scored[:20]:
            entry = p.to_dict()
            entry['score'] = round(s, 2)
            entry['citation_count'] = cc
            entry['influential_count'] = ic
            top20.append(entry)
            print(f"     [{s:.1f}] {p.title[:70]}... (引用:{cc}, 影响力引用:{ic})")
        
        all_candidates[slug] = top20
        print()
    
    # 保存
    output = {
        'fetch_time': today.strftime('%Y-%m-%d %H:%M:%S'),
        'week': today.strftime('%Y-%m-%d'),
        'candidates': all_candidates,
    }
    candidates_path = CACHE_DIR / 'weekly_candidates.json'
    with open(candidates_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"候选数据已保存: {candidates_path}")
    print(f"\n=== 阶段一完成 ===")
    print(f"共抓取 {sum(len(v) for v in all_candidates.values())} 篇候选论文（top20/领域）")
    
    return candidates_path


if __name__ == '__main__':
    main()
