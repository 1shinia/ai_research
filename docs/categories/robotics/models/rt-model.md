# RT-1 / RT-2 权重

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | RT-1 / RT-2 |
| **作者/团队** | Google Robotics (DeepMind) |
| **参数规模** | RT-1: 35M / RT-2: 12B |
| **开源协议** | 研究使用，未公开权重 |
| **模型论文** | [RT-1](https://robotics-transformer1.github.io) / [RT-2](https://robotics-transformer2.github.io) |
| **论文原文** | [2212.06817 (RT-1)](https://arxiv.org/abs/2212.06817) / [2307.15818 (RT-2)](https://arxiv.org/abs/2307.15818) |

## 简介

Google DeepMind 的 Robotics Transformer 系列。RT-1 是基于 Transformer 的机器人操控模型，使用 130K 示范数据训练。RT-2 是视觉-语言-动作 (VLA) 模型，将互联网级图文知识迁移到机器人操控，实现语义理解和泛化能力。

## 核心亮点

- RT-1: Tokenize 机器人动作序列为离散 token，用 Transformer 预测
- RT-2: 将机器人动作视为文本 token 的 VLA 模型
- RT-2 从网络图文数据中获取零样本泛化能力
- 使用 Fleet of Robots 大规模数据收集
- 支持多种操控技能（抓取/放置/打开/抽屉等）

## 使用方式

- **[RT-1 代码]**: 官方未开源全部权重，参考社区复现
- **[RT-2]**: 基于 PaLI-X / PaLM-E 架构，需大规模计算
- **[Octo 模型]**: 开源替代 RT-2 的 VLA 模型 (https://octo-models.netlify.app)
- **[复现工具]**: robomimic / DROID 等机器人学习框架

## 评估结果

- RT-1: 97% 成功率 (seen tasks) / 10+ 种技能
- RT-2: 62% 成功率 vs 32% (基线) 在 emergent skills
- RT-2: 在未见过场景中 60-70% 泛化成功率

---

*此页面的模型信息由 AI Research Tracker 自动维护。*
