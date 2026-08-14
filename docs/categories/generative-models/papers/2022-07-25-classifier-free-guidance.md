---
title: "Classifier-Free Diffusion Guidance"
date: 2022-07-25
field: generative-models
tags: [diffusion, classifier-free-guidance, conditional-generation, text-to-image]
url: https://arxiv.org/abs/2207.12598
source: arxiv
authors: "Ho & Salimans (Google Research)"
---

## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Classifier-Free Diffusion Guidance |
| **作者** | Ho & Salimans (Google Research) |
| **日期** | 2022-07-25 |
| **领域** | generative-models |
| **标签** | diffusion, classifier-free-guidance, conditional-generation, text-to-image |
| **链接** | [arXiv](https://arxiv.org/abs/2207.12598) |

## 一句话总结

无需额外分类器，仅用一个同时训练了条件/无条件生成的扩散模型，就实现了强大的条件引导。

## 核心思想

- **联合训练**：同一个模型同时学习 p(x|c) 和 p(x)，训练时随机丢弃条件
- **引导公式**：用条件和无条件预测的外推实现引导：ε_guided = ε_uncond + w(ε_cond - ε_uncond)
- **无需分类器**：比 Classifier Guidance 更简单、效果更好
- **引导强度 w**：w>1 时增强条件影响，w=0 时退化为无条件

## 为什么重要

- 成为文本到图像生成的标配方法
- 被 DALL-E 2、Imagen、Stable Diffusion 全部采用
- 扩展到视频生成（Sora）、音频生成等领域
- CFG scale 成为调参的核心超参数

## 关键实验结果

| 引导方式 | FID (ImageNet 256) | 所需模型 |
|----------|--------------------|----------|
| 无引导 | 22.9 | 1 个 |
| Classifier Guidance | 4.0 | 2 个（扩散 + 分类器） |
| **CFG (本论文)** | **3.6** | **1 个** |

## 引用量

> 4,000+
