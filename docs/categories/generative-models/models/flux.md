# Flux.1

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Flux.1 |
| **作者/团队** | Black Forest Labs |
| **参数规模** | Pro / Dev / Schnell (12B DiT) |
| **开源协议** | Apache 2.0 (Schnell) |
| **模型权重** | [HuggingFace](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| **ModelScope** | [black-forest-labs/FLUX.1-dev](https://modelscope.cn/models/black-forest-labs/FLUX.1-dev) |
| **论文原文** | [2407.16769](https://arxiv.org/abs/2407.16769) |

## 简介

Black Forest Labs（原 Stability AI 核心团队创立）的 Flux 系列。采用改进的 Flow Matching + DiT 架构 + 双编码器 (CLIP + T5-XXL)，在图像质量、排版和提示遵循度上超越 SD3。Schnell 版本支持 4 步极速推理，是目前开源最强的文生图模型。

## 核心亮点

- 改进的 Flow Matching + DiT 架构
- 双编码器 (CLIP + T5-XXL) 增强文本理解
- Schnell 版本 4 步推理（蒸馏）
- Pro 版本效果接近 Midjourney 水平
- 原生支持多种宽高比 (1:1 / 3:2 / 16:9)

## 使用方式

- **[Diffusers]**: `pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell")`
- **[ComfyUI]**: 官方支持 Flux 工作流
- **[Schnell]**: 4 步推理速度极快，适合实时生成
- **[Dev]**: 开源非商用，社区微调版本丰富

## 评估结果

- GenEval: 0.81 (Pro/Dev)
- T2I-CompBench: 0.67 (Pro)
- 排版准确性: 开源最强
- 推理速度: 4 步 (Schnell)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
