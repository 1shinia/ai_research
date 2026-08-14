---
title: "Attention Is All You Need"
date: 2017-06-12
field: llm
tags: [Transformer, attention, architecture, foundational]
url: https://arxiv.org/abs/1706.03762
source: arxiv
authors: "Vaswani et al. (Google Brain)"
---


## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Attention Is All You Need |
| **作者** | Vaswani et al. (Google Brain) |
| **日期** | 2017-06-12 |
| **领域** | llm |
| **标签** | Transformer,  attention,  architecture,  foundational |
| **链接** | [arXiv](https://arxiv.org/abs/1706.03762) |

## 一句话总结

提出了 Transformer 架构，完全基于注意力机制，摒弃了 RNN 和 CNN，成为后续所有大语言模型的基石。

## 核心思想

- **自注意力机制 (Self-Attention)**：每个 token 可以直接关注序列中任意位置的 token，解决了 RNN 的长距离依赖问题
- **多头注意力 (Multi-Head Attention)**：并行运行多个注意力头，捕获不同子空间的信息
- **位置编码 (Positional Encoding)**：用正弦/余弦函数注入位置信息，弥补无序列归纳偏置的问题
- **编码器-解码器结构**：Encoder-Decoder 架构，适用于翻译等序列到序列任务

## 为什么重要

- 奠定了现代 NLP 的基础架构
- 训练效率大幅提升（可并行化）
- 后续 GPT、BERT、T5 等模型全部基于此
- 影响力远超 NLP，扩展到视觉 (ViT)、音频、多模态等领域

## 关键实验结果

| 任务 | BLEU 分数 | 训练成本 |
|------|-----------|----------|
| 英德翻译 | 28.4 | 3.5 天, 8 P100 GPU |
| 英法翻译 | 41.0 | 低于之前所有模型 |

## 引用量

> 120,000+ (截至 2026 年，是 AI 领域被引用最多的论文之一)
