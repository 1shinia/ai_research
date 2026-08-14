---
title: "High-Resolution Image Synthesis with Latent Diffusion Models (Stable Diffusion)"
date: 2021-12-20
field: generative-models
tags: [diffusion, latent-diffusion, text-to-image, Stable-Diffusion, VAE]
url: https://arxiv.org/abs/2112.10752
source: arxiv
authors: "Rombach et al. (LMU Munich / Runway)"
---

## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | High-Resolution Image Synthesis with Latent Diffusion Models (Stable Diffusion) |
| **作者** | Rombach et al. (LMU Munich / Runway) |
| **日期** | 2021-12-20 |
| **领域** | generative-models |
| **标签** | diffusion, latent-diffusion, text-to-image, Stable-Diffusion, VAE |
| **链接** | [arXiv](https://arxiv.org/abs/2112.10752) |

## 一句话总结

在预训练 VAE 的隐空间中运行扩散模型，大幅降低计算成本，使高分辨率图像生成在消费级 GPU 上成为可能。

## 核心思想

- **两阶段架构**：Stage 1 用 VAE 将图像压缩到隐空间，Stage 2 在隐空间运行扩散
- **计算效率**：隐空间分辨率远低于像素空间，训练和推理成本大幅降低
- **交叉注意力**：通过 cross-attention 引入文本、布局等条件信息
- **灵活条件**：支持文本、语义图、类标签等多种条件

## 为什么重要

- Stable Diffusion 的技术基础，引爆了 AI 绘画革命
- 开源后形成了全球最大的 AI 创作社区
- 证明了"隐空间扩散"是最优性价比方案
- 影响了 FLUX、SDXL、SD3 等后续所有版本

## 关键实验结果

| 模型 | FID (MS-COCO) | 参数量 | 推理 GPU |
|------|---------------|--------|----------|
| DALL-E 2 | 10.4 | 3.5B | 专用集群 |
| LDM (本论文) | 12.6 | 860M | **单张 RTX 2080** |
| GLIDE | 12.2 | 5B | 专用集群 |

## 引用量

> 12,000+
