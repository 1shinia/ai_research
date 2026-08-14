# 自注意力机制 (Self-Attention)

## 1. 核心思想

自注意力让序列中的每个位置都能直接关注其他所有位置，捕获长距离依赖关系。

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

### 1.1 直觉理解

- **Query (Q)**：我在找什么？
- **Key (K)**：我有什么？
- **Value (V)**：我实际输出的内容

类比信息检索：用 Query 去匹配 Key，匹配度高的 Value 被更多关注。

---

## 2. 计算流程

### 2.1 输入投影

$$
Q = XW^Q, \quad K = XW^K, \quad V = XW^V
$$

其中 $X \in \mathbb{R}^{n \times d}$，$W^Q, W^K, W^V \in \mathbb{R}^{d \times d_k}$

### 2.2 注意力分数

$$
S = \frac{QK^T}{\sqrt{d_k}} \in \mathbb{R}^{n \times n}
$$

$S_{ij}$ 表示位置 $i$ 对位置 $j$ 的注意力权重（归一化前）。

### 2.3 归一化

$$
A = \text{softmax}(S) \quad \text{(按行归一化)}
$$

$$
A_{ij} = \frac{\exp(S_{ij})}{\sum_k \exp(S_{ik})}
$$

### 2.4 加权求和

$$
O = AV \in \mathbb{R}^{n \times d_v}
$$

---

## 3. 多头注意力

### 3.1 动机

单头注意力只能捕获一种关系模式。多头允许模型同时关注不同子空间的信息。

### 3.2 计算

$$
\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O
$$

其中 $W_i^Q, W_i^K, W_i^V \in \mathbb{R}^{d \times d_k}$，$W^O \in \mathbb{R}^{hd_v \times d}$

### 3.3 参数分配

通常 $d_k = d_v = d/h$，这样多头的总参数量与单头相同。

**示例：** $d=512, h=8 \Rightarrow d_k=d_v=64$

---

## 4. 复杂度分析

### 4.1 时间复杂度

| 操作 | 复杂度 | 说明 |
|------|--------|------|
| $QK^T$ | $O(n^2 d_k)$ | 矩阵乘法 |
| Softmax | $O(n^2)$ | 逐行归一化 |
| $AV$ | $O(n^2 d_v)$ | 矩阵乘法 |
| **总计** | $O(n^2 d)$ | $d_k \approx d_v \approx d/h$ |

### 4.2 空间复杂度

| 组件 | 空间 | 说明 |
|------|------|------|
| 注意力矩阵 $A$ | $O(n^2)$ | 需要存储用于反向传播 |
| 中间激活 | $O(nd)$ | 每层输出 |
| **总计** | $O(n^2 + nd)$ | 长序列时 $n^2$ 主导 |

---

## 5. 变体与优化

### 5.1 稀疏注意力

**思想：** 不是所有位置都需要关注，只计算重要的注意力。

| 方法 | 模式 | 复杂度 |
|------|------|--------|
| 局部注意力 | 只关注窗口内 | $O(nw)$ |
| 全局注意力 | 特殊 token 全局关注 | $O(n + g^2)$ |
| 稀疏 Transformer | 固定稀疏模式 | $O(n\sqrt{n})$ |

### 5.2 线性注意力

**思想：** 用核函数近似 softmax，避免 $O(n^2)$ 计算。

$$
\text{Attention}(Q, K, V) \approx \phi(Q)(\phi(K)^T V)
$$

其中 $\phi$ 是核函数（如 elu+1、softmax 等）。

**代表：** Linear Transformer、Performer、Mamba

### 5.3 FlashAttention

**思想：** IO 感知的分块计算，减少 HBM 访问。

- **Tiling：** 将 $Q, K, V$ 分块加载到 SRAM
- **Recomputation：** 反向时重新计算注意力，不存储中间矩阵
- **复杂度：** 时间 $O(n^2 d)$，空间 $O(n)$

详见：[FlashAttention 论文](../../efficient-training/papers/2022-05-23-flash-attention.md)

---

## 6. 可视化理解

### 6.1 注意力模式

不同头学到的典型模式：

| 头类型 | 模式 | 作用 |
|--------|------|------|
| 局部头 | 关注相邻位置 | 语法、局部结构 |
| 全局头 | 均匀关注所有位置 | 全局语义 |
| 位置头 | 关注固定偏移 | 位置关系 |
| 语法头 | 关注特定词性 | 句法分析 |

### 6.2 注意力熵

$$
H(A_i) = -\sum_j A_{ij} \log A_{ij}
$$

- **低熵：** 注意力集中，模型很确定
- **高熵：** 注意力分散，模型在整合多源信息

---

## 7. 实践技巧

### 7.1 注意力 Dropout

在 softmax 之前对注意力分数应用 dropout：

$$
A = \text{softmax}(\text{dropout}(S))
$$

防止模型过度依赖某些位置。

### 7.2 注意力掩码

**因果掩码 (Causal Mask)：**

$$
M_{ij} = \begin{cases} 0 & i \geq j \\ -\infty & i < j \end{cases}
$$

确保位置 $i$ 只能关注位置 $\leq i$。

**Padding 掩码：**

$$
M_{ij} = \begin{cases} 0 & \text{位置 } j \text{ 有效} \\ -\infty & \text{位置 } j \text{ 是 padding} \end{cases}
$$

### 7.3 注意力温度

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\tau}\right)V
$$

- $\tau < \sqrt{d_k}$：注意力更尖锐
- $\tau > \sqrt{d_k}$：注意力更平滑

---

## 8. 数学推导

### 8.1 梯度推导

设 $L$ 为损失函数，$O = AV$ 为注意力输出。

**对 $V$ 的梯度：**

$$
\frac{\partial L}{\partial V} = A^T \frac{\partial L}{\partial O}
$$

**对 $S$ 的梯度：**

$$
\frac{\partial L}{\partial S} = \left(\frac{\partial L}{\partial A} - A \circ \sum_j \frac{\partial L}{\partial A_{ij}}\right) \circ A
$$

其中 $\circ$ 是逐元素乘法。

**对 $Q$ 的梯度：**

$$
\frac{\partial L}{\partial Q} = \frac{1}{\sqrt{d_k}} \frac{\partial L}{\partial S} K
$$

---

## 9. 常见问题

### Q1: 为什么除以 $\sqrt{d_k}$ 而不是 $d_k$？

除以 $\sqrt{d_k}$ 将方差归一化到 1。如果除以 $d_k$，方差会变成 $1/d_k$，导致注意力过于平滑。

### Q2: 多头注意力和单头注意力有什么区别？

多头可以并行捕获不同子空间的关系。实验表明 8 头效果最佳，但 4 头或 16 头也接近。

### Q3: 自注意力和交叉注意力有什么区别？

- **自注意力：** $Q, K, V$ 来自同一序列
- **交叉注意力：** $Q$ 来自一个序列，$K, V$ 来自另一个序列（如解码器关注编码器）

---

## 10. 延伸阅读

- [Transformer 架构详解](transformer-architecture.md)
- [位置编码](positional-encoding.md)
- [FlashAttention](../../efficient-training/papers/2022-05-23-flash-attention.md)

---

*最后更新：2026-06-22*
