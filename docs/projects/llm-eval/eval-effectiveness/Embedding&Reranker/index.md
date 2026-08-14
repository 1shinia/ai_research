## Embedding & Reranker 效果评估

> 文本嵌入模型（Embedding）与重排序模型（Reranker）是 RAG 和语义搜索的核心组件，分别负责"初召"和"精排"。本节系统梳理两者的评估体系、主流模型排行榜与选型指南。

---

## 一、Embedding 模型评估

### 1.1 评估基准：MTEB

**MTEB（Massive Text Embedding Benchmark）** 是当前业界最权威的 Embedding 评估框架，涵盖 **8 大任务**、**58 个数据集**、**112 种语言**：

| 任务类别 | 评估内容 | 指标 | 代表数据集 |
|---------|---------|------|-----------|
| **分类 (Classification)** | 文本分类精度 | Accuracy / F1 | Amazon, DBpedia, Yahoo |
| **聚类 (Clustering)** | 无监督聚类质量 | V-Measure | Reddit, Arxiv |
| **成对分类 (Pair Classification)** | 句子对相似度 | AP / F1 | Twitter, Sprint |
| **重排序 (Reranking)** | 候选文档排序 | MAP / MRR | AskUbuntu, SciDocs |
| **检索 (Retrieval)** | 文档召回 | NDCG@10 / Recall@100 | MS MARCO, BEIR 子集 |
| **语义相似度 (STS)** | 文本语义匹配 | Spearman | STS-B, SICK-R |
| **摘要 (Summarization)** | 摘要与原文匹配 | Spearman | SummEval |
| **跨语言对齐** | 跨语言检索/分类 | 各任务指标 | XTREME, BUCC |

> **关键洞察**：`Retrieval` 和 `STS` 是实际业务中最常参考的子集。MTEB 总分高 ≠ 检索任务强，选型时务必看分项分数。

### 1.2 2025-2026 主流 Embedding 模型排行榜

以下是 MTEB Retrieval（检索）和 Classification（分类）两个关键维度的模型梯队：

| 排名 | 模型 | 参数量 | 向量维度 | 最大长度 | MTEB检索 | 特点 |
|------|------|-------|---------|---------|---------|------|
| 🥇 | **voyage-3** | - | 1024 | 32K | 71.3 | 闭源 API，检索最强 |
| 🥇 | **cohere-embed-v3** | - | 1024 | 512 | 70.8 | 闭源 API，多语言 |
| 🥇 | **gte-Qwen2-7B-instruct** | 7B | 4096 | 32K | 70.2 | 开源，长上下文 |
| 🥈 | **stella-mrl-large-1.9B** | 1.9B | 1024 | 8192 | 69.1 | 开源，效率兼顾 |
| 🥈 | **bge-en-icl** | 7.8B | 4096 | 32K | 68.5 | 智源 BGE 新作 |
| 🥈 | **e5-mistral-7b-instruct** | 7B | 4096 | 32K | 67.8 | 微软 E5 系列 |
| 🥉 | **bge-m3** | 568M | 1024 | 8192 | 66.3 | 多语言均衡，部署友好 |
| 🥉 | **gte-small** | 384M | 768 | 8192 | 63.2 | 轻量部署首选 |
| 🥉 | **text2vec-large-chinese** | 326M | 1024 | 512 | 62.1 | 中文场景特化 |

### 1.3 关键评估指标

| 指标 | 含义 | 计算公式 |
|------|------|---------|
| **NDCG@K** | 归一化折扣累计增益，位置越靠前权重越高 | $\\sum\\frac{rel_i}{\\log_2(i+1)}$ |
| **MRR@K** | 平均倒数排名，第一个正确答案的位置 | $\\frac{1}{rank}$ |
| **Recall@K** | 前 K 个结果中召回的相关文档比例 | $\\frac{rel\\_retrieved}{rel\\_total}$ |
| **Spearman** | 预测相似度与人工标注的秩相关系数 | - |

### 1.4 选型建议

```
场景                    推荐模型
──────────────────────────────────────────────────
通用英文检索             voyage-3 / cohere-embed-v3
开源自部署               gte-Qwen2-7B / bge-m3
中文场景                 text2vec-large-chinese / bge-m3
多语言检索               bge-m3 / cohere-embed-v3
长文档（>8K）            gte-Qwen2-7B / voyage-3
轻量上线（<500M）        bge-m3 / gte-small
C端成本敏感               bge-small / gte-tiny
```

---

## 二、Reranker 模型评估

### 2.1 评估基准：BEIR 与 BGE-Reranker 生态

Reranker 的核心评估框架是 **BEIR（Benchmark for Information Retrieval）**，涵盖 **18 个检索数据集**。与 Embedding 不同，Reranker 更关注**排序精度**与**跨域泛化能力**。

### 2.2 2025-2026 主流 Reranker 模型排行榜

| 排名 | 模型 | 参数量 | 最大长度 | BEIR NDCG@10 | 特点 |
|------|------|-------|---------|:-----------:|------|
| 🥇 | **Cohere Rerank v3.5** | 闭源 API | 4096 | 63.8 | 英文 SOTA，云端调用 |
| 🥇 | **Cohere Rerank v3 (English)** | 闭源 API | 4096 | 62.1 | 性价比之选 |
| 🥈 | **BGE-Reranker-v2-m3** | 568M | 8192 | 60.7 | 开源标杆，多语言 |
| 🥈 | **BGE-Reranker-v2.0** | 278M | 8192 | 59.3 | 支持图片+文本混合 |
| 🥈 | **Jina Reranker v2** | 550M | 8192 | 58.9 | 多语言，长文档 |
| 🥉 | **Voyage Rerank** | 闭源 API | 8000 | 58.2 | 兼容多种 embedding |
| 🥉 | **BGE-Reranker-v2-gemma** | 2.5B | 4096 | 57.8 | 精度高，部署成本高 |
| 🥉 | **mxbai-rerank-large-v1** | 1.5B | 512 | 56.4 | 开源轻量 |

### 2.3 关键评估指标

| 指标 | 说明 |
|------|------|
| **NDCG@10** | 核心指标，衡量 Top-10 排序质量 |
| **MRR** | 第一个正确答案的位置 |
| **Recall@K** | 精排后相关文档保留比例 |
| **Latency (P50/P99)** | 生产环境关键指标，直接影响用户体验 |
| **Throughput** | 每秒处理文档数（doc/s） |

### 2.4 选型建议

```
场景                    推荐 Reranker
──────────────────────────────────────────────────
英文 RAG 云端            Cohere Rerank v3.5
开源自部署                BGE-Reranker-v2-m3
中文场景                 BGE-Reranker-v2-m3 / Jina Reranker v2
长文档（>4K）            BGE-Reranker-v2-m3 / Jina Reranker v2
高吞吐量                  BGE-Reranker-v2-m3 （量化部署）
精度优先（可接受延迟）    BGE-Reranker-v2-gemma / Cohere v3.5
敏感数据私有部署          BGE-Reranker-v2-m3（本地部署）
```

---

## 三、Embedding + Reranker 联合评估

### 3.1 为什么需要组合评估？

实际 RAG 系统中，Embedding 和 Reranker 是**串联关系**：

```
Query → [Embedding 初召 Top-K] → [Reranker 精排 Top-N] → LLM
```

因此需评估联合效果：

| 测试维度 | 方法 |
|---------|------|
| **初召 + 精排全链路** | Embedding 召回 Top-50 → Reranker 重排 → 计算 NDCG@10 |
| **Reranker 对 Embedding 的容错性** | 切换不同 Embedding 模型，看 Reranker 是否能挽回 |
| **效率权衡** | Embedding 召回耗时 + Reranker 排序耗时总延迟 |

### 3.2 实战经验：Reranker 是 ROI 最高的优化点

> 大量实践表明：**换 Reranker 比换 Embedding 模型涨点更快**。检索出 Top-50 候选后，用 Reranker 精排到 Top-5，效果提升显著。

**典型链路配置：**

```
初召：bge-m3（Embedding）→ 召回 Top-50
精排：BGE-Reranker-v2-m3 → 精排 Top-5
总延迟：~50ms（Embedding）+ ~80ms（Reranker，GPU）
```

---

## 四、评估工具与资源

### 4.1 标准评估框架

| 工具 | 用途 | 地址 |
|------|------|------|
| **MTEB** | Embedding 全任务评估 | [github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |
| **BEIR** | 检索 & Reranker 评估 | [github.com/beir-cellar/beir](https://github.com/beir-cellar/beir) |
| **LlamaIndex RAG Benchmark** | 端到端 RAG 评测 | [github.com/run-llama/rags](https://github.com/run-llama/rags) |

### 4.2 在线排行榜

| 排行榜 | 地址 |
|--------|------|
| MTEB Leaderboard | [huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard) |
| BEIR Leaderboard（Hugging Face） | [huggingface.co/spaces/beir/leaderboard](https://huggingface.co/spaces/beir/leaderboard) |

### 4.3 主流开源模型仓库

| 模型 | 地址 |
|------|------|
| BGE（智源） | [huggingface.co/BAAI](https://huggingface.co/BAAI) |
| GTE（Alibaba） | [huggingface.co/Alibaba-NLP](https://huggingface.co/Alibaba-NLP) |
| text2vec（李沐团队） | [huggingface.co/shibing624](https://huggingface.co/shibing624) |
| E5（Microsoft） | [huggingface.co/intfloat](https://huggingface.co/intfloat) |

---

## 📈 评估结果

> TODO：待补充实际测试数据。

## 📚 参考资料

- MTE: Massive Text Embedding Benchmark (Muennighoff et al., 2022)
- BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models (Thakur et al., 2021)
- BGE 技术报告：C-Pack: Packaged Resources to Advance General Chinese Embedding (BAAI, 2023-2025)
- Cohere Rerank 官方文档：docs.cohere.com/docs/rerank
- Jina Reranker 技术报告：jina.ai/news/reranker-v2
- LlamaIndex RAG 基准评测：docs.llamaindex.ai
- `tinyseeking.github.io`: 主流开源 Rerank 模型解析与选型指南（2026 版）
- `darrypy.github.io`: Reranker 模型选型对比 — Cohere / BGE / Voyage / Jina（2026）
