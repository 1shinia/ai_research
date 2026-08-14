---
title: "Diffusion Models Beat GANs on Image Synthesis"
date: 2021-05-11
field: generative-models
tags: [diffusion, GAN-comparison, classifier-guidance, image-synthesis]
url: https://arxiv.org/abs/2105.05233
source: arxiv
authors: "Dhariwal & Nichol (OpenAI)"
---

## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Diffusion Models Beat GANs on Image Synthesis |
| **作者** | Dhariwal & Nichol (OpenAI) |
| **日期** | 2021-05-11 |
| **领域** | generative-models |
| **标签** | diffusion, GAN-comparison, classifier-guidance, image-synthesis |
| **链接** | [arXiv](https://arxiv.org/abs/2105.05233) |

## 一句话总结

通过架构改进和分类器引导 (Classifier Guidance)，首次证明扩散模型在 FID 指标上全面超越 GAN。

## 核心思想

- **分类器引导**：用预训练分类器的梯度引导采样过程，提升样本质量
- **架构改进**：引入自适应组归一化、残差连接等 CNN 技巧
- **引导强度**：分类器引导强度 s 可以在质量和多样性之间权衡
- **消融实验**：系统性分析了各种设计选择的影响

## 为什么重要

- 标志性转折点：扩散模型正式超越 GAN
- 分类器引导成为后续条件生成的基础
- 直接影响了 DALL-E 2 的设计
- 引发了扩散模型研究的热潮

## 关键实验结果

| 模型 | FID (ImageNet 256) |
|------|--------------------|
| StyleGAN2 + ADA | 4.83 |
| DDPM (原论文) | 10.71 |
| ADM (本论文) | 4.59 |
| ADM + Classifier Guidance | **2.97** |

## 引用量

> 6,000+
