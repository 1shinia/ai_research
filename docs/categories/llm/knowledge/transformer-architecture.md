# Transformer 架构详解

## 1. 整体架构

Transformer 采用 **Encoder-Decoder** 结构，完全基于注意力机制，摒弃了 RNN 和 CNN。

```
输入 → [Encoder × N] → 隐表示 → [Decoder × N] → 输出
         ↑                        ↑
    自注意力 + FFN           自注意力 + 交叉注意力 + FFN
```

### 1.1 编码器 (Encoder)

每个编码器层包含两个子层：
1. **多头自注意力 (Multi-Head Self-Attention)**
2. **前馈神经网络 (Feed-Forward Network, FFN)**

每个子层都有 **残差连接 (Residual Connection)** 和 **层归一化 (Layer Normalization)**。

### 1.2 解码器 (Decoder)

每个解码器层包含三个子层：
1. **掩码多头自注意力 (Masked Multi-Head Self-Attention)**
2. **编码器-解码器注意力 (Encoder-Decoder Attention)**
3. **前馈神经网络 (FFN)**

掩码机制确保位置 i 只能关注位置 < i 的 token，防止信息泄露。

---

## 2. 核心组件详解

### 2.1 缩放点积注意力 (Scaled Dot-Product Attention)

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

**为什么除以 $\sqrt{d_k}$？**

当 $d_k$ 较大时，点积结果的方差会变大，导致 softmax 进入梯度极小的饱和区。缩放因子 $\frac{1}{\sqrt{d_k}}$ 将方差归一化到 1。

**推导：**

假设 $q_i$ 和 $k_i$ 独立同分布，均值为 0，方差为 1：
$$
\text{Var}(q \cdot k) = \sum_{i=1}^{d_k} \text{Var}(q_i k_i) = d_k
$$

因此标准差为 $\sqrt{d_k}$，除以该值后方差为 1。

### 2.2 多头注意力 (Multi-Head Attention)

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O
$$

其中：
$$
\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

**为什么用多头？**

- 不同头可以关注不同子空间的信息
- 类比 CNN 的多通道，每个头学习不同的特征
- 实验表明 8 头效果最佳

### 2.3 前馈网络 (FFN)

$$
\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
$$

通常使用 **GELU** 或 **ReLU** 激活函数。

**参数比例：** FFN 占 Transformer 总参数的约 2/3。

---

## 3. 关键设计选择

| 设计 | 选择 | 原因 |
|------|------|------|
| 注意力类型 | 缩放点积 | 计算高效，梯度稳定 |
| 头数 | 8 | 实验最优 |
| FFN 维度 | $4d_{model}$ | 容量与效率平衡 |
| 归一化 | Post-LN (原论文) / Pre-LN (现代) | Pre-LN 训练更稳定 |
| 激活函数 | ReLU (原) / GELU / SwiGLU (现代) | GELU 更平滑 |

---

## 4. 现代变体

### 4.1 Pre-LN vs Post-LN

**Post-LN (原始):**
$$
x_{t+1} = \text{LayerNorm}(x_t + \text{Sublayer}(x_t))
$$

**Pre-LN (现代):**
$$
x_{t+1} = x_t + \text{Sublayer}(\text{LayerNorm}(x_t))
$$

Pre-LN 训练更稳定，不需要学习率预热 (warmup)。

### 4.2 注意力变体

| 变体 | 特点 | 代表模型 |
|------|------|----------|
| 标准注意力 | $O(n^2)$ 复杂度 | BERT, GPT-2 |
| 稀疏注意力 | 只关注局部 + 全局 | Longformer |
| 线性注意力 | $O(n)$ 复杂度 | Linear Transformer |
| 分组查询注意力 (GQA) | 减少 KV 头数 | LLaMA 2, Mistral |
| 多头潜在注意力 (MLA) | 压缩 KV | DeepSeek-V2 |

---

## 5. 计算复杂度分析

### 5.1 时间复杂度

| 组件 | 复杂度 | 说明 |
|------|--------|------|
| 自注意力 | $O(n^2 d)$ | $n$ 为序列长度，$d$ 为维度 |
| FFN | $O(n d^2)$ | 与序列长度线性相关 |
| 总复杂度 | $O(n^2 d + n d^2)$ | 长序列时注意力主导 |

### 5.2 空间复杂度

| 组件 | 复杂度 | 说明 |
|------|--------|------|
| 注意力矩阵 | $O(n^2)$ | 需要存储 $QK^T$ |
| 激活值 | $O(n d)$ | 每层的输出 |
| 总空间 | $O(n^2 + n d)$ | 长序列时注意力矩阵主导 |

---

## 6. 实践要点

### 6.1 训练技巧

- **学习率预热 (Warmup)**：前几千步线性增加学习率
- **梯度裁剪 (Gradient Clipping)**：防止梯度爆炸
- **Dropout**：通常 0.1，注意力层和 FFN 层分别设置
- **权重衰减 (Weight Decay)**：通常 0.01

### 6.2 推理优化

- **KV Cache**：缓存历史 KV，避免重复计算
- **FlashAttention**：IO 感知的分块计算
- **推测性解码 (Speculative Decoding)**：小模型草稿 + 大模型验证

---

## 7. 数学推导：注意力梯度

设 $A = \text{softmax}(S)$，其中 $S = \frac{QK^T}{\sqrt{d_k}}$。

**Softmax 梯度：**

$$
\frac{\partial A_{ij}}{\partial S_{ik}} = A_{ij}(\delta_{jk} - A_{ik})
$$

**注意力对 Q 的梯度：**

$$
\frac{\partial \text{Attention}}{\partial Q} = \left(\frac{\partial A}{\partial S} \cdot V\right) \frac{1}{\sqrt{d_k}} K^T
$$

---

## 8. 常见问题

### Q1: 为什么 Transformer 比 RNN 快？

**并行性：** RNN 必须按时间步顺序计算，Transformer 的自注意力可以完全并行。

### Q2: 位置编码为什么重要？

自注意力是置换等变的 (permutation equivariant)，没有位置信息就无法区分不同顺序的输入。

### Q3: 为什么用 LayerNorm 而不是 BatchNorm？

- LayerNorm 对每个样本独立归一化，适合变长序列
- BatchNorm 依赖 batch 统计，小 batch 时不稳定

---

## 9. 延伸阅读

- [Attention Is All You Need](../papers/2017-06-12-attention-is-all-you-need.md)
- [FlashAttention](../../efficient-training/papers/2022-05-23-flash-attention.md)
- [MoE 架构](moe.md)

---

*最后更新：2026-06-22*
