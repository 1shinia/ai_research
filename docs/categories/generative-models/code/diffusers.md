# Diffusers

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Diffusers |
| **语言** | Python |
| **用途** | 扩散模型库 |
| **GitHub** | [huggingface/diffusers](https://github.com/huggingface/diffusers) |
| **许可证** | Apache 2.0 |

## 简介

HuggingFace Diffusers 是最权威的扩散模型库，提供完整的训练和推理管道。支持 Stable Diffusion / DALL-E / Flux / Imagen / Sora 等 200+ 扩散模型架构。从文生图到视频生成，是生成式 AI 领域的核心工具。

## 核心功能

- 统一 Pipeline API（文生图 / 图生图 / 视频生成）
- 支持 SD3 / Flux / DALL-E 等最新架构
- LoRA / DreamBooth / ControlNet 插件支持
- 完整的训练脚本和示例
- 调度器可插拔（DDIM / PNDM / DPM++ / Euler 等）

## 快速开始

```python
from diffusers import StableDiffusion3Pipeline
import torch

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-medium",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

image = pipe("A cat wearing a hat, photorealistic").images[0]
image.save("cat.png")
```

## 使用场景

- 文生图和图生图应用
- 扩散模型微调（LoRA / DreamBooth）
- 视频生成和编辑

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
