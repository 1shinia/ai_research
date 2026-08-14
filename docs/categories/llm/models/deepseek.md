# DeepSeek-V2/3

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | DeepSeek-V2/3 |
| **作者/团队** | 深度求索 (DeepSeek) |
| **参数规模** | V2: 236B (21B 激活) / V3: 671B (37B 激活) |
| **开源协议** | DeepSeek License / MIT |
| **模型权重** | [HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-V3) |
| **ModelScope** | [deepseek-ai/DeepSeek-V3](https://modelscope.cn/models/deepseek-ai/DeepSeek-V3) |
| **论文原文** | [2412.19437](https://arxiv.org/abs/2412.19437) |

## 简介

深度求索 (DeepSeek) 的 DeepSeek V2/V3 系列大语言模型。V2 首次大规模商用 MLA (Multi-head Latent Attention) 注意力架构，V3 以 671B 总参数 + 37B 激活参数实现与 GPT-4o 不相上下的性能，训练成本仅约 560 万美元，被誉为 "AI 界的 DeepSeek moment"。

## 核心亮点

- MLA (Multi-head Latent Attention) — 大幅降低 KV Cache 开销
- MoE 架构 — V3 仅激活 37B 参数 / token
- 训练成本极低（V3 约 278 万 GPU 小时）
- DeepSeek-R1: 开源推理模型，使用强化学习训练 CoT
- 多项基准超越 LLaMA 3 405B / GPT-4o

## 使用方式

- **[HuggingFace]**: `model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-V3")`
- **[vLLM]**: 支持 DeepSeek MoE + MLA 推理加速
- **[SGLang]**: 针对 DeepSeek V3 的特殊推理引擎优化
- **[API]**: platform.deepseek.com 提供商业 API 服务

## 评估结果

- MMLU: 88.5% (V3)
- HumanEval: 82.6% (V3)
- GSM8K: 96.5% (V3)
- Arena Elo: 超越 LLaMA-3-405B

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
