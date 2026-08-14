# DeepSpeed

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | DeepSpeed |
| **语言** | Python / C++ |
| **用途** | 分布式训练优化 |
| **GitHub** | [microsoft/DeepSpeed](https://github.com/microsoft/DeepSpeed) |
| **许可证** | Apache 2.0 |

## 简介

微软 DeepSpeed 是大规模分布式训练优化库。提供 ZeRO (Zero Redundancy Optimizer) 系列优化技术，ZeRO-3 可将训练显存占用降低 8 倍。DeepSpeed-Chat 为 RLHF 训练提供端到端支持。

## 核心功能

- **ZeRO-1/2/3**: 分阶段优化器状态 / 梯度 / 参数分片
- **ZeRO-Offload**: 将优化器状态卸载到 CPU
- **MoE 训练**: 高效的专家混合模型训练
- **DeepSpeed-Chat**: RLHF 训练流水线
- **Autotuning**: 自动配置最优训练参数

## 快速开始

```bash
pip install deepspeed

# 使用 deepspeed 启动训练
deepspeed --num_gpus=8 train.py --deepspeed_config ds_config.json

# ZeRO-3 配置示例
{
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {"device": "cpu"}
  }
}
```

## 使用场景

- 大型 LLM 分布式训练
- 显存受限环境下的训练
- RLHF 训练流水线

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
