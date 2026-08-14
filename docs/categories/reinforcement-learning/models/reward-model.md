# 开源 Reward Model

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | 开源 Reward Model |
| **作者/团队** | 社区 / OpenAssistant 等 |
| **参数规模** | 常见 7B / 13B / 20B |
| **开源协议** | Apache 2.0 / MIT |
| **模型权重** | [HuggingFace](https://huggingface.co/models?pipeline_tag=text-classification&search=reward) |
| **ModelScope** | [ModelScope Reward Model](https://modelscope.cn/models?search=reward-model) |
| **论文原文** | [2312.03971](https://arxiv.org/abs/2312.03971) |

## 简介

Reward Model（奖励模型）是 RLHF 流程中用于评估模型输出质量的关键组件。通过对人类偏好的学习，RM 为强化学习提供训练信号。主流 RM 基于 LLaMA / Qwen 等基座模型在偏好数据集上微调。高质量 RM 直接决定 RLHF 训练效果的上限。

## 核心亮点

- **Bradley-Terry 模型**: 最常用的偏好建模方法
- 基于 LLaMA / Qwen 微调，输出标量奖励分数
- 高质量 RM 是 RLHF 训练效果的关键
- 社区积累了 HH-RLHF / UltraFeedback 等偏好数据集
- DPO 等方法尝试不依赖独立 RM 进行对齐训练

## 使用方式

- **[HF Hub]**: 搜索 "reward-model" 查找开源 RM
- **[OpenAssistant]**: open-assistant.io 提供 Reward Model 数据
- **[使用]**: RM 为 PPO 训练提供奖励信号
- **[评估]**: 用 RM 的准确率 (Accuracy) 衡量偏好预测能力

## 评估结果

- Helpful/Harmless Accuracy: ~70% (7B RM)
- 指令偏好预测准确率: ~65-75%
- 通常需要 >70% 准确率才能有效支持 PPO 训练

---

*此页面的模型信息由 AI Research Tracker 自动维护。*
