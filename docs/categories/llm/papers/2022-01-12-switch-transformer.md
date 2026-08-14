---
title: "Mixture of Experts (Switch Transformer)"
date: 2022-01-12
field: llm
tags: [MoE, efficiency, scaling, architecture]
url: https://arxiv.org/abs/2202.08906
source: arxiv
authors: "Fedus et al. (Google Brain)"
---


## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Mixture of Experts (Switch Transformer) |
| **作者** | Fedus et al. (Google Brain) |
| **日期** | 2022-01-12 |
| **领域** | llm |
| **标签** | MoE,  efficiency,  scaling,  architecture |
| **链接** | [arXiv](https://arxiv.org/abs/2202.08906) |

## 一句话总结

通过稀疏激活的混合专家架构，在相同计算成本下实现了更大参数规模和更好性能。

## 核心思想

- **稀疏激活**：每次推理只激活一部分专家（如 1/8），降低计算成本
- **路由机制**：通过门控网络决定每个 token 分配给哪个专家
- **负载均衡**：通过辅助损失确保所有专家被均匀使用
- **规模扩展**：可以在不增加推理成本的情况下大幅增加参数量

## 为什么重要

- 突破了"参数越多、计算越贵"的限制
- 被 GPT-4、Mixtral、Qwen-MoE 等主流模型采用
- 让开源社区也能训练超大模型
- 是当前大模型效率优化的核心方向

## 关键实验结果

- Switch Transformer (1.6T 参数) 训练速度比稠密模型快 4x
- 在相同计算预算下达到更好的性能
- Mixtral 8x7B 性能接近 LLaMA 70B，但推理成本只有 1/6
