# Harmless Assistant (安全对齐模型)

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Harmless Assistant 安全对齐模型 |
| **作者/团队** | Anthropic / 社区 |
| **参数规模** | 基于 LLaMA / Qwen 等微调 |
| **开源协议** | 视基座许可而定 |
| **模型权重** | [HuggingFace 安全对齐模型合集](https://huggingface.co/models?search=safety) |
| **ModelScope** | [ModelScope 安全模型](https://modelscope.cn/models?search=safety-aligned) |
| **论文原文** | [2204.05862](https://arxiv.org/abs/2204.05862) (HHH) |

## 简介

安全对齐模型是指在训练过程中加入安全考量，通过 RLHF / DPO 等对齐技术训练出的能够拒绝有害请求、遵守伦理规范的模型。Anthropic 的 Harmless Assistant 项目（HH-RLHF 数据集）是该方向的奠基工作。

## 核心亮点

- HH-RLHF 数据集：标准的安全对齐训练数据
- 通过偏好训练学习拒绝有害请求
- 在 Helpfulness 和 Harmlessness 之间取得平衡
- 社区版安全模型基于 LLaMA / Qwen 等开源基座
- 支持多轮安全对话过滤

## 使用方式

- **[安全对齐训练]**: 使用 HH-RLHF 数据集 + DPO 训练
- **[评估工具]**: Safety Eval / HarmBench 基准
- **[搜索]**: HuggingFace 搜索 "safety-aligned" 或 "harmless"
- **[自建]**: 使用 LLaMA-Factory 加载安全数据微调

## 评估结果

- HarmBench 拒绝率: >90%（安全对齐后）
- Helpfulness 保持率: ~95% 不降低
- 毒性输出减少: ~80% (vs 未对齐模型)

---

*此页面的模型信息由 AI Research Tracker 自动维护。*
