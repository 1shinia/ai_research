# RLHF 原理

## 1. 概述

基于人类反馈的强化学习，让模型行为符合人类意图。

## 2. 三步流程

### 2.1 监督微调 (SFT)

用人工标注的指令-回答对微调预训练模型。

### 2.2 奖励模型训练

收集人类偏好数据，训练奖励模型预测人类偏好。

### 2.3 PPO 优化

用奖励模型作为奖励信号，用 PPO 优化策略。

## 3. 数学细节

### 3.1 奖励模型

    r(x, y) = RewardModel(x, y)

训练目标：让 chosen 的奖励高于 rejected。

    L = -log(sigma(r(x, y_chosen) - r(x, y_rejected)))

### 3.2 PPO 奖励

    reward = r(x, y) - beta * KL(pi || pi_ref)

KL 惩罚防止模型偏离参考策略太远。

## 4. 与 DPO 对比

| 方面 | RLHF | DPO |
|------|------|-----|
| 奖励模型 | 需要 | 不需要 |
| 训练复杂度 | 高 | 低 |
| 稳定性 | 低 | 高 |

## 5. 延伸阅读

- [RLHF 论文](../papers/2017-06-13-rlhf.md)
- [PPO 详解](ppo-detailed.md)
- [LLM RLHF 流程](../../llm/knowledge/rlhf-pipeline.md)

---

*最后更新：2026-06-22*
