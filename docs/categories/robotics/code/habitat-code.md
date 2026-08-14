# Habitat Sim

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Habitat Sim |
| **语言** | Python / C++ |
| **用途** | 3D 模拟器（具身 AI） |
| **GitHub** | [facebookresearch/habitat-sim](https://github.com/facebookresearch/habitat-sim) |
| **许可证** | MIT |

## 简介

Meta AI 开发的 Habitat Sim 是一个高效的 3D 模拟器，专为具身 AI 研究设计。支持 Matterport3D / Gibson / HM3D 等大规模 3D 场景数据，为导航 / 操控 / 问答等任务提供物理模拟环境。

## 核心功能

- 大规模 3D 场景渲染（10M+ 场景）
- 物理引擎支持刚体运动学
- RGB / 深度 / 语义 / 光流多种传感器
- 20+ 具身基准任务
- 支持 VR 和人机交互

## 快速开始

```bash
git clone https://github.com/facebookresearch/habitat-sim.git
cd habitat-sim && pip install -e .

python examples/example.py --scene data/scene_datasets/habitat-test-scenes/van-gogh-room.glb
```

## 使用场景

- 具身 AI 导航研究
- 多模态环境感知
- 机器人训练数据生成

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
