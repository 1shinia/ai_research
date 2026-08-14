# Mistral / Mixtral

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Mistral / Mixtral |
| **作者/团队** | Mistral AI |
| **参数规模** | 7B / 8x7B / 8x22B / 123B |
| **开源协议** | Apache 2.0 (Mistral 7B) |
| **模型权重** | [HuggingFace](https://huggingface.co/mistralai/Mistral-7B-v0.3) |
| **ModelScope** | [mistralai/Mistral-7B-v0.3](https://modelscope.cn/models/mistralai/Mistral-7B-v0.3) |
| **论文原文** | [2310.06825](https://arxiv.org/abs/2310.06825) |

## 简介

Mistral AI 发布的高效开源大语言模型系列。Mistral 7B 以 7B 参数超越 LLaMA 2 13B；Mixtral 8x7B 采用 Sparse MoE 架构，每 token 仅激活 2 个专家，以约 12B 激活参数量达到接近 70B 密集模型的性能。

## 核心亮点

- 分组查询注意力 (GQA) + 滑动窗口注意力 (SWA)
- Mixtral Sparse MoE — 12B 激活参数量达到 70B 级性能
- 支持 32K 上下文窗口
- Mistral Large 123B 提供极强推理能力
- 法英双语原生能力出色

## 使用方式

- **[HuggingFace]**: `from transformers import AutoModelForCausalLM; model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.3")`
- **[vLLM]**: 原生支持 Mixtral MoE 推理加速
- **[Ollama]**: `ollama run mistral`
- **[Mistral API]**: console.mistral.ai 提供商业 API 服务

## 评估结果

- MMLU: 70.7% (8x7B)
- HumanEval: 66.8% (8x7B)
- GSM8K: 75.5% (8x7B)
- MT-Bench: 8.30 (8x7B)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
