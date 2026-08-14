---
title: "3D Gaussian Splatting for Real-Time Radiance Field Rendering"
date: 2023-02-20
field: vision
tags: [3D-reconstruction, gaussian-splatting, real-time, novel-view]
url: https://arxiv.org/abs/2308.04079
source: arxiv
authors: "Kerbl et al. (INRIA)"
---


## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | 3D Gaussian Splatting for Real-Time Radiance Field Rendering |
| **作者** | Kerbl et al. (INRIA) |
| **日期** | 2023-02-20 |
| **领域** | vision |
| **标签** | 3D-reconstruction,  gaussian-splatting,  real-time,  novel-view |
| **链接** | [arXiv](https://arxiv.org/abs/2308.04079) |

## 一句话总结

用 3D 高斯椭球表示场景，实现了实时、高质量的新视角合成，速度比 NeRF 快 100 倍以上。

## 核心思想

- **3D 高斯表示**：用一组 3D 高斯椭球表示场景，每个高斯有位置、协方差、颜色、透明度
- **可微分光栅化**：将 3D 高斯投影到 2D 并渲染，整个过程可微分
- **自适应密度控制**：通过克隆和分裂高斯来优化场景细节
- **实时渲染**：利用 GPU 光栅化管线，达到 30-300 FPS

## 为什么重要

- 解决了 NeRF 训练慢、渲染慢的核心痛点
- 成为 3D 重建和渲染的新范式
- 催生了大量后续工作（动态场景、反射、物理仿真）
- 在 VR/AR、游戏、影视等领域有巨大应用潜力

## 关键实验结果

| 方法 | 训练时间 | 渲染速度 | PSNR |
|------|----------|----------|------|
| 3DGS | 40 min | 100+ FPS | 31.5 |
| NeRF | 20+ hours | < 1 FPS | 30.8 |
| Instant-NGP | 5 min | 60 FPS | 29.5 |
