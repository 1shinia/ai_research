# Stable-Baselines3

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Stable-Baselines3 |
| **语言** | Python |
| **用途** | 强化学习算法库 |
| **GitHub** | [DLR-RM/stable-baselines3](https://github.com/DLR-RM/stable-baselines3) |
| **许可证** | MIT |

## 简介

Stable-Baselines3 (SB3) 是深度强化学习的标准算法库。提供 PPO / SAC / DQN / A2C / TD3 等主流 RL 算法的干净实现。代码质量高、文档完善，是 RL 研究者最常用的训练和基准工具。

## 核心功能

- PPO / SAC / DQN / A2C / TD3 / DDPG 等算法
- 标准 Gymnasium 环境接口
- 回调系统（模型保存 / 学习率调度 / 评估）
- 向量化环境支持多人并行
- 完整文档和教程

## 快速开始

```python
from stable_baselines3 import PPO
from gymnasium import make

env = make("CartPole-v1")
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

obs, _ = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
```

## 使用场景

- 强化学习研究和教学
- RL 算法快速原型
- RLHF 中的 PPO 训练实现

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
