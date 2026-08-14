---
title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
date: 2022-05-23
field: efficient-training
tags: [FlashAttention, attention, memory-efficiency, IO-aware]
url: https://arxiv.org/abs/2205.14135
source: arxiv
authors: "Dao et al. (Stanford)"
---

## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness |
| **作者** | Dao et al. (Stanford) |
| **日期** | 2022-05-23 |
| **领域** | efficient-training |
| **标签** | FlashAttention, attention, memory-efficiency, IO-aware |
| **链接** | [arXiv](https://arxiv.org/abs/2205.14135) |

## 一句话总结

通过 IO 感知的分块计算，将 Attention 的内存复杂度从 O(N²) 降到 O(N)，速度提升 2-4 倍。

## 核心思想

- **Tiling (分块)**：将 Q、K、V 分成小块加载到 SRAM 中计算
- **Recomputation (重计算)**：前向时不保存中间注意力矩阵，反向时重新计算
- **IO 感知**：最小化 HBM（高带宽内存）和 SRAM 之间的数据搬运
- **精确计算**：不是近似，结果与标准 Attention 完全一致

## 为什么重要

- 解决了 Transformer 长上下文的内存瓶颈
- 成为所有现代 LLM 框架的标配
- 直接推动了 100K+ 上下文模型的实用化
- FlashAttention-2/3 持续优化，成为 GPU 计算的标杆

## 关键实验结果

| 序列长度 | 标准 Attention | FlashAttention | 加速比 |
|----------|---------------|----------------|--------|
| 4096 | 基线 | 2-4x | ✓ |
| 8192 | OOM | 可计算 | ✓ |
| 训练 (GPT-2) | 基线 | 3x | ✓ |
