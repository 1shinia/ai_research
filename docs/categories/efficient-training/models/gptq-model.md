# GPTQ 量化模型

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | GPTQ 量化模型 |
| **作者/团队** | IST / 社区 |
| **参数规模** | INT4 / INT3 量化版（各种尺寸） |
| **开源协议** | 视基座许可而定 |
| **模型权重** | [HuggingFace GPTQ 合集](https://huggingface.co/models?search=gptq) |
| **ModelScope** | [ModelScope GPTQ 模型](https://modelscope.cn/models?search=GPTQ) |
| **论文原文** | [2210.17323](https://arxiv.org/abs/2210.17323) |

## 简介

GPTQ (GPT Post-Training Quantization) 是流行的后训练权重量化方法。通过基于 Hessian 矩阵的二次近似进行逐层量化，在 INT4 精度下保持模型质量。社区（如 TheBloke）已发布数千个 GPTQ 量化模型。

## 核心亮点

- 基于 Hessian 矩阵的二次近似量化
- 支持 INT4 / INT3 / INT2 多种量化级别
- 社区生态丰富 — TheBloke 等发布大量 GPTQ 模型
- 支持批量推理加速
- 与 AutoGPTQ / ExLlama 推理引擎集成

## 使用方式

- **[AutoGPTQ]**: `pip install auto-gptq`
- **[量化]**: `from auto_gptq import AutoGPTQForCausalLM; model = AutoGPTQForCausalLM.from_pretrained(model_path, quantize_config=...)`
- **[ExLlama]**: 专为 GPTQ 优化的高性能推理引擎
- **[HF Hub]**: 搜索 "GPTQ" 下载社区量化版

## 评估结果

- 精度损失: <1% (INT4 128g)
- 推理加速: 2-3x vs FP16
- 显存减少: ~4x vs FP16

---

*此页面的模型信息由 AI Research Tracker 自动维护。*
