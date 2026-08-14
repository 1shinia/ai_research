# MuJoCo

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | MuJoCo |
| **语言** | C / Python |
| **用途** | 物理仿真引擎 |
| **GitHub** | [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) |
| **许可证** | Apache 2.0 |

## 简介

MuJoCo (Multi-Joint dynamics with Contact) 是开源的高效物理仿真引擎。由 Google DeepMind 维护，提供快速精确的接触动力学计算。在强化学习的机器人控制研究中被广泛使用。

## 核心功能

- 快速精确的接触动力学
- 软接触模型（椭圆摩擦锥）
- 关节式机器人支持
- Python / C API
- 实时可视化

## 快速开始

```bash
pip install mujoco

python -c "
import mujoco
import mujoco.viewer as viewer

model = mujoco.MjModel.from_xml_path('humanoid.xml')
data = mujoco.MjData(model)
with viewer.launch_passive(model, data) as v:
    for _ in range(1000):
        mujoco.mj_step(model, data)
        v.sync()
"
```

## 使用场景

- 机器人控制仿真
- RL 训练环境（Gymnasium MuJoCo 环境）
- 运动学 / 动力学分析和验证

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
