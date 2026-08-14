# Octo

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Octo |
| **作者/团队** | UC Berkeley / Stanford / CMU 等 |
| **参数规模** | Octo-Small (27M) / Octo-Base (93M) |
| **开源协议** | MIT / Apache 2.0 |
| **模型权重** | [HuggingFace](https://huggingface.co/rail-berkeley) |
| **ModelScope** | [rail-berkeley/octo-base](https://modelscope.cn/models/rail-berkeley/octo-base) |
| **论文原文** | [2405.12213](https://arxiv.org/abs/2405.12213) |

## 简介

Octo 是开源的视觉-语言-动作 (VLA) 通用机器人基座模型。在 Open X-Embodiment 数据集（60+ 机器人数据集，150 万条示范）上训练，支持多种机器人形态和任务。作为 RT-2 的开源替代，Octo 可通过微调适配新机器人。

## 核心亮点

- 开源 VLA 模型，社区完全可用
- 在 60+ 机器人数据集（1.5M 条）上大规模训练
- 支持多种机器人形态（单臂/双臂/移动操控等）
- 可通过少量微调适配到新机器人
- 支持语言指令和目标图像两种任务规范

## 使用方式

- **[HuggingFace]**: https://huggingface.co/rail-berkeley/octo-base
- **[GitHub]**: https://github.com/rail-berkeley/octo
- **[安装]**: `pip install git+https://github.com/rail-berkeley/octo.git`
- **[推理]**: `python octo/examples/gym_eval.py --model rail-berkeley/octo-base`

## 评估结果

- 8 个未见过任务平均成功率: ~60%
- 微调后在新机器人上平均成功率: >80%
- 涵盖抓取/放置/抽屉/转门等泛化操作

---

*此页面的模型信息由 AI Research Tracker 自动维护。*
