# Stable Diffusion 3

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Stable Diffusion 3 |
| **作者/团队** | Stability AI |
| **参数规模** | 800M / 2B / 8B (MMDiT) |
| **开源协议** | SD3 OpenRAIL-M |
| **模型权重** | [HuggingFace](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium) |
| **ModelScope** | [stabilityai/stable-diffusion-3.5-medium](https://modelscope.cn/models/stabilityai/stable-diffusion-3.5-medium) |
| **论文原文** | [2403.03206](https://arxiv.org/abs/2403.03206) |

## 简介

Stability AI 的 SD3 系列采用 MMDiT (Multi-Modal Diffusion Transformer) 架构。使用 Transformer 替代传统 UNet，结合 Rectified Flow 统一噪声调度。文本理解、图像质量和排版能力较 SDXL 大幅提升。3.5 Medium 在消费级显卡可运行（FP8 仅需 ~4GB VRAM）。

## 核心亮点

- MMDiT — 使用 Transformer 替代传统 UNet
- Rectified Flow (RF) 统一噪声调度
- 16 通道 VAE 提升细节还原能力
- 3.5 Medium FP8 量化后消费级显卡可运行
- 排版和文字生成能力大幅提升

## 使用方式

- **[Diffusers]**: `pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-medium")`
- **[ComfyUI]**: 加载 SD3 模型工作流
- **[SD3 Medium]**: 需要 ~8GB VRAM (FP16) / ~4GB (FP8)
- **[提示风格]**: 支持自然语言长文本描述，无需特定关键词

## 评估结果

- T2I-CompBench: 0.66 (8B)
- GenEval: 0.74 (8B)
- CLIP Score: 31.4 (8B)
- Aesthetic: 6.08 (8B)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
