---
title: "Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM)"
date: 2023-09-01
field: efficient-training
tags: [vLLM, PagedAttention, inference, KV-cache, serving]
url: https://arxiv.org/abs/2309.06180
source: arxiv
authors: "Kwon et al. (UC Berkeley)"
---

## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM) |
| **作者** | Kwon et al. (UC Berkeley) |
| **日期** | 2023-09-01 |
| **领域** | efficient-training |
| **标签** | vLLM, PagedAttention, inference, KV-cache, serving |
| **链接** | [arXiv](https://arxiv.org/abs/2309.06180) |

## 一句话总结

借鉴操作系统的分页内存管理，解决了 LLM 推理中 KV Cache 的内存碎片问题，吞吐量提升 2-4 倍。

## 核心思想

- **PagedAttention**：将 KV Cache 分成固定大小的块，按需分配
- **虚拟内存管理**：用块表 (block table) 映射逻辑块到物理块
- **零碎片**：消除了预分配导致的内存浪费
- **共享**：支持 beam search 等场景的 KV Cache 共享

## 为什么重要

- 成为 LLM 推理部署的行业标准
- 解决了多用户并发推理的瓶颈
- 直接催生了 vLLM 开源项目
- 被几乎所有云服务商的 LLM 服务采用

## 关键实验结果

| 指标 | HuggingFace | Orca | vLLM |
|------|-------------|------|------|
| 吞吐量 (req/s) | 基线 | 1.5x | 2-4x |
| 内存利用率 | 20-40% | 40-60% | >90% |
| P99 延迟 | 高 | 中 | 低 |
