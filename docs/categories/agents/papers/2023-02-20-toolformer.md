---
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
date: 2023-02-20
field: agents
tags: [tool-use, self-supervised, API-calling, agent]
url: https://arxiv.org/abs/2302.04761
source: arxiv
authors: "Schick et al. (Meta AI)"
---


## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Toolformer: Language Models Can Teach Themselves to Use Tools |
| **作者** | Schick et al. (Meta AI) |
| **日期** | 2023-02-20 |
| **领域** | agents |
| **标签** | tool-use,  self-supervised,  API-calling,  agent |
| **链接** | [arXiv](https://arxiv.org/abs/2302.04761) |

## 一句话总结

让语言模型自主学习何时以及如何调用外部工具（计算器、搜索引擎、翻译器等），无需人工标注。

## 核心思想

- **自监督学习工具使用**：模型自己决定何时调用工具，并用工具返回的结果继续生成
- **API 调用标记**：在文本中插入特殊的 API 调用标记，如 `[CALL search("query")]`
- **采样 + 过滤**：先生成大量候选 API 调用，再用自洽性过滤出有用的
- **端到端训练**：用 API 返回结果作为额外上下文继续训练

## 为什么重要

- 证明了模型可以自主学习工具使用
- 无需人工标注工具调用数据
- 大幅提升了数学推理、事实核查等任务的性能
- 为 Function Calling 提供了新思路

## 关键实验结果

| 任务 | Toolformer | GPT-3 |
|------|------------|-------|
| 数学 (GSM8K) | 37.7% | 13.5% |
| 事实核查 | 65.2% | 49.0% |
| 翻译 | 显著提升 | 基线 |
