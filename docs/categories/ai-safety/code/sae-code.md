# SAE 解释性工具

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | SAE 解释性工具 |
| **语言** | Python |
| **用途** | 稀疏自编码器与可解释性 |
| **GitHub** | [TransformerLens / SAE](https://github.com/TransformerLensOrg/TransformerLens) |
| **许可证** | MIT |

## 简介

稀疏自编码器 (SAE) 是当前 LLM 可解释性的核心技术。通过将神经网络激活分解为稀疏、可解释的特征单元，研究者可以识别模型内部对应特定概念（如"法律"、"欺骗"、"危险"）的神经元电路。

## 核心功能

- **SAE 训练**: 学习模型的稀疏特征分解
- **特征可视化**: 识别特征对应的文本模式
- **Circuit 分析**: 追踪特征如何组合形成推理
- **激活探测器**: 探测模型内部对特定概念的表征
- **TransformerLens**: 标准化 LLM 内部机制分析框架

## 快速开始

```python
from transformer_lens import HookedTransformer
from sae_lens import SAE

model = HookedTransformer.from_pretrained("gemma-2-2b")
sae = SAE.from_pretrained("gemma-2-2b-res-jb", 1)

# 查看特定特征激活
tokens = model.to_tokens("The legal system should")
_, cache = model.run_with_cache(tokens)
feature_acts = sae.encode(cache["post", 6])
```

## 使用场景

- LLM 安全性分析和审计
- 模型内部机制研究
- 对齐研究和可解释性评估

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
