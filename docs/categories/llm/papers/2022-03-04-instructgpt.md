---
title: "Training language models to follow instructions with human feedback (InstructGPT)"
date: 2022-03-04
field: llm
tags: [RLHF, alignment, instruction-tuning, PPO]
url: https://arxiv.org/abs/2203.02155
source: arxiv
authors: "Ouyang et al. (OpenAI)"
---


## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Training language models to follow instructions with human feedback (InstructGPT) |
| **作者** | Ouyang et al. (OpenAI) |
| **日期** | 2022-03-04 |
| **领域** | llm |
| **标签** | RLHF,  alignment,  instruction-tuning,  PPO |
| **链接** | [arXiv](https://arxiv.org/abs/2203.02155) |

## 一句话总结

通过 RLHF（基于人类反馈的强化学习）训练语言模型遵循指令，开创了大模型对齐的技术路线，是 ChatGPT 的技术基础。

## 核心思想

- **三步训练流程**：
  1. SFT（监督微调）：用人工标注的指令-回答对微调模型
  2. 奖励模型训练：训练一个模型预测人类偏好
  3. PPO 强化学习：用奖励模型指导策略优化
- **人类反馈**：标注员对模型输出进行排序，提供偏好信号
- **对齐目标**：让模型"有用、诚实、无害" (Helpful, Honest, Harmless)

## 为什么重要

- 开创了 RLHF 对齐范式，成为行业标准
- 直接催生了 ChatGPT，引爆了大模型产业
- 证明了人类反馈可以有效改善模型行为
- 后续 DPO、KTO 等方法都是对其的改进

## 关键实验结果

- InstructGPT 在人类评估中显著优于 GPT-3
- 在 TruthfulQA 上减少了幻觉
- 在有毒内容生成上显著降低有害输出
