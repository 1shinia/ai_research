# AWQ 量化模型

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | AWQ 量化模型 |
| **作者/团队** | MIT / 社区 |
| **参数规模** | INT4 量化版（各种尺寸） |
| **开源协议** | 视基座许可而定 |
| **模型权重** | [HuggingFace AWQ 合集](https://huggingface.co/models?search=awq) |
| **ModelScope** | [ModelScope AWQ 模型](https://modelscope.cn/models?search=AWQ) |
| **论文原文** | [2306.00978](https://arxiv.org/abs/2306.00978) |

## 简介

AWQ (Activation-aware Weight Quantization) 是对激活值敏感的权重量化方法。通过识别权重中少数对激活值影响最大的通道（约 1%）并放大保护，在 INT4 量化下实现接近 FP16 的精度。社区已发布大量基于 AWQ 的量化模型。

## 核心亮点

- 激活感知 — 识别并保护对激活影响大的权重通道
- INT4 量化精度接近 FP16，损失 <0.5%
- 无需回归校准 — 比 GPTQ 更快
- 与 vLLM / TensorRT-LLM 深度集成
- 支持 LLaMA / Qwen / Mistral 等主流模型

## 使用方式

- **[AutoAWQ]**: `pip install autoawq`
- **[量化]**: `from awq import AutoAWQForCausalLM; model = AutoAWQForCausalLM.from_pretrained(model_path)`
- **[vLLM]**: 原生支持 AWQ 量化模型推理
- **[HF Hub]**: 搜索 "AWQ" 下载社区量化版

## 评估结果

- 精度损失: <0.5% (INT4)
- 推理加速: 2-3x vs FP16
- 显存减少: ~4x vs FP16 (以 7B 模型为例，从 14GB 降到 4GB)

---

*此页面的模型信息由 AI Research Tracker 自动维护。*
