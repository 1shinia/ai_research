# Qwen2.5

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Qwen2.5 |
| **作者/团队** | 阿里云 Qwen 团队 |
| **参数规模** | 0.5B / 1.5B / 3B / 7B / 14B / 32B / 72B |
| **开源协议** | Apache 2.0 |
| **模型权重** | [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) |
| **ModelScope** | [qwen/Qwen2.5-7B-Instruct](https://modelscope.cn/models/qwen/Qwen2.5-7B-Instruct) |
| **论文原文** | [2501.00683](https://arxiv.org/abs/2501.00683) |

## 简介

阿里云 Qwen 团队发布的 Qwen2.5 系列大语言模型。覆盖从 0.5B 到 72B 全尺寸，72B 版本性能接近闭源前沿模型。支持 128K 上下文窗口，18T tokens 大规模预训练数据，中英文能力均表现出色。衍生版 Qwen2.5-Coder/Math 专精代码和数学领域。

## 核心亮点

- 覆盖 0.5B-72B 全尺寸，满足从端侧到云端需求
- 128K 上下文窗口（32K 训练，128K 外推）
- 18T tokens 多语言预训练数据
- 支持多种对齐方式（RLHF / DPO / SimPO）
- Qwen2.5-Coder / Math 衍生版专精编码和数学

## 使用方式

- **[HuggingFace]**: `from transformers import AutoModelForCausalLM; model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct")`
- **[vLLM]**: `python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-7B-Instruct`
- **[Ollama]**: `ollama run qwen2.5`
- **[DashScope API]**: 通过阿里云灵积 API 调用 Qwen-Max

## 评估结果

- MMLU: 85.3% (72B)
- HumanEval: 85.4% (72B)
- GSM8K: 92.1% (72B)
- MATH: 76.9% (72B)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
