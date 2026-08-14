# TRL

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | TRL |
| **语言** | Python |
| **用途** | RLHF 训练库 |
| **GitHub** | [huggingface/trl](https://github.com/huggingface/trl) |
| **许可证** | Apache 2.0 |

## 简介

TRL (Transformer Reinforcement Learning) 是 HuggingFace 的 RLHF 训练库。提供 PPOv2 / DPO / KTO / GRPO 等多种对齐训练算法的实现。与 Transformers/Datasets 库深度集成，支持一键启动对齐训练。

## 核心功能

- **PPOv2**: 标准 PPO 的 RLHF 实现
- **DPO**: 直接偏好优化
- **KTO**: 仅需二元反馈的对齐
- **GRPO**: Group Relative Policy Optimization
- **Reward Model**: 奖励模型训练

## 快速开始

```python
# DPO 训练
from transformers import AutoModelForCausalLM
from trl import DPOTrainer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B")
trainer = DPOTrainer(
    model=model,
    train_dataset=dataset,
    tokenizer=tokenizer,
    beta=0.1,
)
trainer.train()
```

## 使用场景

- LLM 对齐训练（RLHF / DPO / KTO）
- 偏好模型训练
- 安全对齐实验

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
