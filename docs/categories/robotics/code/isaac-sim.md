# Isaac Sim

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Isaac Sim |
| **语言** | Python / C++ |
| **用途** | 机器人仿真平台 |
| **GitHub** | [NVIDIA Omniverse 套件](https://developer.nvidia.com/isaac-sim) |
| **许可证** | NVIDIA 研究许可 |

## 简介

NVIDIA Isaac Sim 是建立在 Omniverse 平台上的高级机器人仿真工具。提供逼真的物理引擎、渲染和传感器仿真（Lidar / 深度相机 / IMU）。支持 ROS/ROS2 集成和 Sim-to-Real 迁移。

## 核心功能

- 逼真物理引擎（刚体 / 关节 / 布料 / 流体）
- ROS / ROS2 原生集成
- 传感器仿真（RGB-D / Lidar / IMU）
- 基于域的随机化适合 Sim-to-Real
- 关节式机器人操控和移动仿真

## 快速开始

```bash
# 通过 NVIDIA Omniverse Launcher 安装
# Python API 控制
import omni.isaac.core as core
from omni.isaac.core.robots import Franka

my_world = core.World()
franka = my_world.scene.add(Franka(prim_path="/World/Franka"))
```

## 使用场景

- 机器人算法开发测试
- Sim-to-Real 迁移学习
- 自动化机器人训练数据生成

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
