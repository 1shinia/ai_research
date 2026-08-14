# 安全对齐模型 (Constitutional AI)

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Constitutional AI 安全对齐模型 |
| **作者/团队** | Anthropic |
| **参数规模** | 基于 Claude 系列（闭源）/ 社区复现 |
| **开源协议** | 研究使用 / Apache 2.0 (社区复现) |
| **模型论文** | [Anthropic CAI](https://www.anthropic.com/constitutional) |
| **ModelScope** | [ModelScope CAI 模型](https://modelscope.cn/models?search=constitutional+ai) |
| **论文原文** | [2212.08073](https://arxiv.org/abs/2212.08073) |

## 简介

Constitutional AI (CAI) 是 Anthropic 提出的一种无需人类标注反馈即可训练安全对齐模型的方法。通过定义一份"宪法"（行为准则集合），让模型通过 AI Feedback 的自我修订（Revision）和监督学习实现安全对齐。

## 核心亮点

- **宪法引导**：用一套行为准则替代大量人工标注
- **RLAIF (RL from AI Feedback)**: 使用模型自身生成偏好数据
- **两阶段**: 监督学习（SL）→ 从 AI 反馈的强化学习（RL）
- **无需人类标注安全偏好数据**
- 社区开源的 Constitutional AI 复现项目可用

## 使用方式

- **[RLAIF]**: 使用 AI Feedback 替代人类偏好标注
- **[宪法定义]**: 一份明确的规则列表（如"不要有害内容"）
- **[Self-Revision]**: 模型自我修订违反宪法的输出
- **[社区工具]**: TRL 支持 RLAIF 训练方式

## 评估结果

- Harmlessness: 接近 RLHF 水平（无需人类标注）
- Helpfulness: 不显著低于标准 RLHF
- 可扩展性: 宪法可随时更新扩展，无需重新标注数据

---

*此页面的模型信息由 AI Research Tracker 自动维护。*
