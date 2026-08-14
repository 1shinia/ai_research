# 条件生成

## 1. 概述

在生成过程中引入条件信息（如文本、类别、图像），控制生成内容。

## 2. 条件注入方式

### 2.1 拼接

将条件直接拼接到输入：

    x_input = concat(x, condition)

### 2.2 交叉注意力

用交叉注意力融合条件信息：

    output = Attention(Q=x, K=condition, V=condition)

### 2.3 Adaptive Layer Norm (AdaLN)

用条件调制归一化参数：

    output = AdaLN(x, condition) = gamma * LayerNorm(x) + beta

## 3. 引导方法

### 3.1 分类器引导

用预训练分类器的梯度引导采样。

### 3.2 分类器自由引导 (CFG)

    epsilon_guided = epsilon_uncond + w * (epsilon_cond - epsilon_uncond)

w 控制引导强度。

## 4. 应用场景

| 场景 | 条件 | 输出 |
|------|------|------|
| 文本到图像 | 文本描述 | 图像 |
| 图像到图像 | 源图像 | 目标图像 |
| 图像修复 | 掩码 + 图像 | 修复图像 |
| 超分辨率 | 低分辨率 | 高分辨率 |

## 5. 延伸阅读

- [Classifier-Free Guidance 论文](../papers/2022-07-25-classifier-free-guidance.md)

---

*最后更新：2026-06-22*
