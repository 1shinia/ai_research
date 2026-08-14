---
title: "Score-Based Generative Modeling through Stochastic Differential Equations"
date: 2020-11-26
field: generative-models
tags: [diffusion, score-based, SDE, continuous-time, foundational]
url: https://arxiv.org/abs/2011.13456
source: arxiv
authors: "Song et al. (Stanford)"
---

## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Score-Based Generative Modeling through Stochastic Differential Equations |
| **作者** | Song et al. (Stanford) |
| **日期** | 2020-11-26 |
| **领域** | generative-models |
| **标签** | diffusion, score-based, SDE, continuous-time, foundational |
| **链接** | [arXiv](https://arxiv.org/abs/2011.13456) |

## 一句话总结

用随机微分方程 (SDE) 统一了 Score-based 模型和 DDPM，为扩散模型提供了连续时间的理论框架。

## 核心思想

- **SDE 框架**：前向加噪过程用 SDE 描述，反向去噪用逆 SDE
- **统一视角**：证明了 DDPM 和 Score Matching 是同一框架的离散/连续版本
- **概率流 ODE**：通过 ODE 形式实现确定性采样
- **灵活调度**：噪声调度不再受限于固定步数

## 为什么重要

- 为扩散模型提供了统一的数学框架
- 连接了 Score-based 和 Denoising 两大流派
- ODE 采样为后续加速方法奠定基础
- 被后续大量理论工作引用

## 关键实验结果

| 数据集 | FID |
|--------|-----|
| CIFAR-10 | 2.20 |
| CelebA-HQ 256 | 7.63 |

## 引用量

> 5,000+
