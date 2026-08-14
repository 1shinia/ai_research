---
title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
date: 2022-01-28
field: llm
tags: [reasoning, prompting, CoT, in-context-learning]
url: https://arxiv.org/abs/2201.11903
source: arxiv
authors: "Wei et al. (Google Brain)"
---


## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models |
| **作者** | Wei et al. (Google Brain) |
| **日期** | 2022-01-28 |
| **领域** | llm |
| **标签** | reasoning,  prompting,  CoT,  in-context-learning |
| **链接** | [arXiv](https://arxiv.org/abs/2201.11903) |

## 一句话总结

通过在提示中加入中间推理步骤（"思维链"），大幅提升了大模型在数学、常识推理等任务上的表现。

## 核心思想

- **思维链 (Chain-of-Thought)**：让模型"一步一步思考"，而不是直接给出答案
- **Few-shot + CoT**：在示例中展示完整的推理过程，模型学会模仿
- **涌现推理能力**：只有足够大的模型（约 100B+）才能从 CoT 中受益
- **无需额外训练**：纯提示技巧，不需要微调

## 为什么重要

- 解锁了大模型的推理能力
- 催生了大量后续工作：Self-Consistency、Tree-of-Thought、Auto-CoT 等
- 成为复杂任务的标准提示方法
- 为后续的推理模型（如 o1、DeepSeek-R1）奠定了基础

## 关键实验结果

| 任务 | 标准提示 | CoT 提示 |
|------|----------|----------|
| GSM8K (数学) | 17.7% | 58.1% |
| MultiArith | 17.7% | 96.7% |
| SVAMP | 32.3% | 78.7% |
