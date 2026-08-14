# Gymnasium

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Gymnasium |
| **语言** | Python |
| **用途** | 强化学习环境库 |
| **GitHub** | [Farama-Foundation/Gymnasium](https://github.com/Farama-Foundation/Gymnasium) |
| **许可证** | MIT |

## 简介

Gymnasium 是 OpenAI Gym 的继承者，标准的强化学习环境接口。提供 2000+ 环境和统一 API，涵盖经典控制 / Atari / 机器人 / 棋盘游戏 / 物理模拟等。是 RL 研究中最基础的环境定义标准。

## 核心功能

- 标准 RL 环境接口 (reset / step / render)
- 2000+ 内置环境（Classic Control / Atari / Box2D / MuJoCo）
- 环境封装（奖励缩放 / 动作包装 / 时间限制）
- 观测空间和动作空间定义规范
- Gymnasium 兼容老版 Gym API

## 快速开始

```python
import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")
obs, info = env.reset()
for _ in range(100):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
env.close()
```

## 使用场景

- RL 算法开发和测试
- 自定义环境定义
- 算法基准评估

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
