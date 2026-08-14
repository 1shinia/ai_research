# -*- coding: utf-8 -*-
"""
阶段一替代脚本 v2：使用 requests 爬取 arXiv 新论文列表页面
兼容 output 格式：.cache/weekly_candidates.json
"""
import json, sys, re, time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(r"D:\ai_research")
CACHE_DIR = BASE_DIR / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

# ── 9 大领域 → arXiv 分类映射 ──
DOMAIN_CATS = {
    "llm": {
        "name": "大语言模型",
        "categories": ["cs.CL"],
        "filter_keywords": ["large language model", "transformer", "llm", "gpt", "instruction tuning",
                           "alignment", "rlhf", "dpo", "moe", "scaling law", "chain of thought",
                           "reasoning", "in-context learning", "agent", "function calling"],
    },
    "vision": {
        "name": "计算机视觉",
        "categories": ["cs.CV"],
        "filter_keywords": ["computer vision", "image recognition", "object detection", "segmentation",
                           "visual transformer", "vit", "3d reconstruction", "neural rendering",
                           "gaussian splatting", "video understanding", "visual foundation model", "sam", "dino"],
    },
    "multimodal": {
        "name": "多模态",
        "categories": ["cs.CV", "cs.CL", "cs.MM", "cs.SD"],
        "filter_keywords": ["multimodal", "vision-language", "vlm", "clip", "image caption",
                           "visual question answering", "vqa", "document understanding", "multimodal learning"],
    },
    "agents": {
        "name": "AI Agent",
        "categories": ["cs.AI", "cs.MA", "cs.CL"],
        "filter_keywords": ["ai agent", "planning", "tool use", "function calling", "react",
                           "autonomous agent", "multi-agent", "collaboration", "computer use",
                           "web agent", "code agent", "agentic", "mcp"],
    },
    "generative-models": {
        "name": "生成式模型",
        "categories": ["cs.CV", "cs.LG", "cs.SD", "cs.MM"],
        "filter_keywords": ["generative model", "diffusion", "flow matching", "score-based",
                           "text-to-image", "image generation", "video generation",
                           "consistency model", "3d generation", "dit", "transformer diffusion",
                           "music generation", "audio generation"],
    },
    "reinforcement-learning": {
        "name": "强化学习",
        "categories": ["cs.LG", "cs.AI", "cs.RO"],
        "filter_keywords": ["reinforcement learning", "policy gradient", "ppo", "actor-critic",
                           "rlhf", "reward modeling", "grpo", "process reward model",
                           "offline rl", "deep rl", "multi-agent rl", "marl"],
    },
    "efficient-training": {
        "name": "高效训练与推理",
        "categories": ["cs.LG", "cs.CL", "cs.AI", "cs.AR"],
        "filter_keywords": ["efficient training", "quantization", "lora", "parameter-efficient",
                           "knowledge distillation", "model compression", "flash attention",
                           "kv cache", "speculative decoding", "vllm", "sglang",
                           "pruning", "sparsity", "low-rank"],
    },
    "robotics": {
        "name": "机器人与具身智能",
        "categories": ["cs.RO", "cs.CV", "cs.AI"],
        "filter_keywords": ["robot", "robotics", "embodied", "manipulation", "grasping",
                           "imitation learning", "robot foundation model", "vla",
                           "diffusion policy", "humanoid", "mobility"],
    },
    "ai-safety": {
        "name": "AI安全与对齐",
        "categories": ["cs.AI", "cs.CL", "cs.CR", "cs.LG"],
        "filter_keywords": ["ai safety", "alignment", "red teaming", "hallucination", "jailbreak",
                           "interpretability", "mechanistic interpretability", "watermark",
                           "ai governance", "safety", "robustness", "fairness"],
    },
}

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
})


def parse_arxiv_list_page(html, cat_prefix=""):
    """解析 arXiv 列表页 (list/{cat}/new) HTML，提取论文信息"""
    papers = []
    soup = BeautifulSoup(html, 'html.parser')
    
    # arXiv 列表页结构：<dl> 中包含 dt/dd 对
    dl = soup.find('dl')
    if not dl:
        return papers
    
    dt_tags = dl.find_all('dt', recursive=False)
    dd_tags = dl.find_all('dd', recursive=False)
    
    for dt, dd in zip(dt_tags, dd_tags):
        try:
            # arXiv ID
            a_tag = dt.find('a', title="Abstract")
            if not a_tag:
                continue
            arxiv_id = a_tag.get('href', '').replace('/abs/', '').strip()
            if not arxiv_id:
                continue
            
            # Title
            title_span = dd.find('div', class_='list-title')
            title = ''
            if title_span:
                title = title_span.get_text().replace('Title:', '').strip()
            
            # Authors
            authors_div = dd.find('div', class_='list-authors')
            authors = []
            if authors_div:
                for a in authors_div.find_all('a'):
                    authors.append(a.get_text().strip())
            
            # Abstract
            abstract_p = dd.find('p', class_='mathjax')
            abstract = ''
            if abstract_p:
                abstract = abstract_p.get_text().strip()
            
            # Categories
            cats_div = dd.find('div', class_='list-subjects')
            categories = []
            if cats_div:
                cats_text = cats_div.get_text().replace('Subjects:', '').strip()
                # Parse: "cs.CL (primary); cs.AI; cs.LG"
                for part in cats_text.split(';'):
                    c = part.strip().split(' ')[0].strip()
                    if c:
                        categories.append(c)
            
            # Published date - try from metadata
            published = ''
            meta_row = dd.find('span', class_='is-size-7')
            if not meta_row:
                # Try the arXiv ID's date prefix
                pass
            
            papers.append({
                'arxiv_id': arxiv_id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'categories': categories,
                'published': published,
                'link': f'https://arxiv.org/abs/{arxiv_id}',
            })
        except Exception as e:
            continue
    
    return papers


def fetch_domain_papers(config, max_pages=2):
    """抓取某个领域的 arXiv 新论文"""
    name = config['name']
    categories = config.get('categories', [])
    filter_kw = config.get('filter_keywords', [])
    
    all_papers = []
    seen_ids = set()
    
    for cat in categories[:3]:  # 最多 3 个子分类
        url = f"https://arxiv.org/list/{cat}/new"
        print(f"    正在抓取: {url}")
        
        try:
            resp = session.get(url, timeout=30)
            if resp.status_code != 200:
                print(f"      HTTP {resp.status_code}")
                continue
            
            papers = parse_arxiv_list_page(resp.text, cat)
            print(f"      解析到 {len(papers)} 篇论文")
            
            for p in papers:
                if p['arxiv_id'] not in seen_ids:
                    # 匹配关键词
                    text = (p['title'] + ' ' + p['abstract']).lower()
                    kw_match = sum(1 for kw in filter_kw if kw.lower() in text)
                    if kw_match > 0:
                        p['_keyword_matches'] = kw_match
                        seen_ids.add(p['arxiv_id'])
                        all_papers.append(p)
                        
        except Exception as e:
            print(f"      Error: {type(e).__name__}: {e}")
            continue
    
    print(f"    {name}: 关键词筛选后共 {len(all_papers)} 篇")
    
    # 按关键词匹配数排序取 top 40
    all_papers.sort(key=lambda x: -x.get('_keyword_matches', 0))
    
    # 去掉辅助字段
    for p in all_papers:
        p.pop('_keyword_matches', None)
    
    return all_papers[:40]


def fetch_citations_semantic_scholar(arxiv_ids):
    """批量查询 Semantic Scholar 获取引用数"""
    if not arxiv_ids:
        return {}
    clean_ids = []
    for aid in arxiv_ids:
        aid = aid.strip().split('v')[0]
        clean_ids.append(f"arXiv:{aid}")
    
    citations = {}
    # 分批查询，每批最多 50
    batch_size = 50
    for i in range(0, len(clean_ids), batch_size):
        batch = clean_ids[i:i+batch_size]
        body = json.dumps({"ids": batch})
        url = ("https://api.semanticscholar.org/graph/v1/paper/batch"
               "?fields=citationCount,influentialCitationCount,title")
        try:
            resp = session.post(url, data=body, timeout=30,
                                headers={'Content-Type': 'application/json'})
            if resp.status_code == 200:
                results = resp.json()
                for r in results:
                    if r and 'paperId' in r:
                        ext_id = r.get('externalIds', {}).get('ArXiv', '')
                        if ext_id:
                            citations[ext_id] = {
                                'citation_count': r.get('citationCount', 0),
                                'influential_count': r.get('influentialCitationCount', 0),
                            }
        except Exception as e:
            print(f"     Semantic Scholar 查询失败: {e}")
        
        time.sleep(1.0)  # 避免速率限制
    
    return citations


def main():
    today = datetime.now()
    print(f"=== AI Research Tracker 阶段一（requests 爬虫版）===")
    print(f"执行时间：{today.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_candidates = {}
    total_papers = 0
    
    for slug, config in DOMAIN_CATS.items():
        name = config['name']
        print(f"[{name}]")
        
        # 1. 抓取
        papers = fetch_domain_papers(config)
        
        if not papers:
            all_candidates[slug] = []
            print(f"      → 0 篇候选\n")
            continue
        
        # 2. 查引用数
        arxiv_ids = [p['arxiv_id'] for p in papers]
        print(f"     查询 Semantic Scholar 引用数据 ({len(arxiv_ids)} 篇)...")
        citations = fetch_citations_semantic_scholar(arxiv_ids)
        print(f"     查到 {len(citations)} 篇引用数据")
        
        # 3. 评分：关键词匹配 + 引用数 + 影响力
        scored = []
        for p in papers:
            cit = citations.get(p['arxiv_id'], {})
            cc = cit.get('citation_count', 0)
            ic = cit.get('influential_count', 0)
            # 综合评分
            score = 1.0 + 0.1 * min(cc + 2 * ic, 50)
            scored.append((score, cc, ic, p))
        scored.sort(key=lambda x: -x[0])
        
        # 4. Top 20 候选
        top20 = []
        for s, cc, ic, p in scored[:20]:
            entry = {
                'title': p['title'],
                'abstract': p['abstract'],
                'arxiv_id': p['arxiv_id'],
                'published': p.get('published', ''),
                'authors': p.get('authors', [])[:5],
                'categories': p.get('categories', []),
                'link': p.get('link', ''),
                'score': round(s, 2),
                'citation_count': cc,
                'influential_count': ic,
            }
            top20.append(entry)
            print(f"     [{s:.1f}] {p['title'][:70]}... (引用:{cc}, 影响力引用:{ic})")
        
        all_candidates[slug] = top20
        total_papers += len(top20)
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
    print(f"共抓取 {total_papers} 篇候选论文（top20/领域）")
    
    return candidates_path


if __name__ == '__main__':
    main()
