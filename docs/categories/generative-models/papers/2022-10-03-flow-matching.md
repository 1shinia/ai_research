---
title: "Flow Matching for Generative Modeling"
date: 2022-10-03
field: generative-models
tags: [flow-matching, continuous-normalizing-flow, generative, diffusion-alternative]
url: https://arxiv.org/abs/2210.02747
source: arxiv
authors: "Lipman et al. (Meta AI)"
---

## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Flow Matching for Generative Modeling |
| **作者** | Lipman et al. (Meta AI) |
| **日期** | 2022-10-03 |
| **领域** | generative-models |
| **标签** | flow-matching, continuous-normalizing-flow, generative, diffusion-alternative |
| **链接** | [arXiv](https://arxiv.org/abs/2210.02747) |

## 一句话总结

提出了一种基于连续正则化流的生成模型训练方法，比扩散模型更简洁、更灵活。

## 核心思想

- **目标匹配**：直接回归预定义的向量场，而非模拟扩散过程
- **最优传输路径**：用 OT 条件流构建从噪声到数据的直线路径
- **无需扩散**：不依赖前向扩散过程，训练目标更直接
- **兼容扩散**：可以恢复扩散模型作为特例

## 为什么重要

- 提供了扩散模型之外的新范式
- 被 Stable Diffusion 3 和 FLUX 采用
- 训练更简单，理论基础更清晰
- 采样路径更直，可以用更少步数生成

## 关键实验结果

| 数据集 | FID | 采样步数 |
|--------|-----|----------|
| CIFAR-10 | 3.07 | 100 |
| ImageNet 64x64 | 4.35 | 100 |
