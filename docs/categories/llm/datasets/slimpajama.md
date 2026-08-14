# SlimPajama

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | SlimPajama |
| **发布年份** | 2023 |
| **规模** | 627B tokens |
| **标注类型** | 无标注 |
| **License** | Apache 2.0 |
| **下载地址** | HuggingFace｜[cerebras/SlimPajama-627B](https://huggingface.co/datasets/cerebras/SlimPajama-627B) |

## 简介

RedPajama 的去重精简版。Cerebras 使用 MinHash + LSH 对 RedPajama 进行全局去重，在保留数据质量的同时将体积从 1.2T 缩减到 627B tokens。

## 核心特点

- 全局 MinHash + LSH 去重
- 数据量减半但质量不降
- 训练效率显著提升

## 典型用途

- 高效 LLM 预训练
- 去重算法研究
- 数据高效训练

---

*此页面的数据集信息由 AI Research Tracker 自动维护。*
