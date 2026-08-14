# 位置编码 (Positional Encoding)

## 1. 为什么需要位置编码？

自注意力机制是**置换等变**的 (permutation equivariant)：

$$
\text{Attention}(\pi(X)) = \pi(\text{Attention}(X))
$$

其中 $\pi$ 是任意置换。这意味着模型无法区分不同顺序的输入。

**示例：** "猫追狗" 和 "狗追猫" 会产生相同的注意力分布。

---

## 2. 绝对位置编码

### 2.1 正弦余弦编码 (Sinusoidal)

**原始 Transformer 使用：**

$$
PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right)
$$

$$
PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)
$$

其中 $pos$ 是位置，$i$ 是维度索引。

**设计动机：**

1. **唯一性：** 每个位置有唯一的编码
2. **相对位置：** $PE_{pos+k}$ 可以表示为 $PE_{pos}$ 的线性函数
3. **泛化：** 可以外推到未见过的序列长度

**数学性质：**

对于固定偏移 $k$：

$$
PE_{pos+k} = W_k PE_{pos}
$$

其中 $W_k$ 是与 $k$ 相关的线性变换矩阵。

### 2.2 可学习位置编码 (Learned)

**BERT、GPT 使用：**

$$
PE = E_{pos} \in \mathbb{R}^{L_{max} \times d}
$$

直接作为可训练参数，与 token 嵌入相加：

$$
x_i = \text{TokenEmbed}(x_i) + PE_i
$$

**优点：** 简单，模型可以学习最适合的位置表示

**缺点：** 无法外推到训练时未见过的长度

---

## 3. 相对位置编码

### 3.1 动机

绝对位置编码假设位置是固定的，但很多任务中**相对位置**更重要。

**示例：** 在翻译中，"A 在 B 前面 2 个词"比"A 在位置 3，B 在位置 5"更有意义。

### 3.2 Shaw 等人 (2018)

将相对位置信息加入注意力计算：

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q(K + R^K)^T}{\sqrt{d_k}}\right)(V + R^V)
$$

其中 $R^K, R^V$ 是相对位置嵌入。

### 3.3 T5 / ALiBi

**T5 偏差：**

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + B\right)V
$$

其中 $B_{ij} = f(i-j)$ 是只依赖相对位置的标量偏差。

**ALiBi (Attention with Linear Biases)：**

$$
B_{ij} = -m \cdot |i - j|
$$

其中 $m$ 是每头不同的斜率（固定，不可学习）。

**优点：** 可以外推到任意长度，无需位置嵌入

---

## 4. 旋转位置编码 (RoPE)

### 4.1 核心思想

**LLaMA、Qwen、ChatGLM 使用：**

通过旋转矩阵将相对位置信息编码到 $Q, K$ 中：

$$
\tilde{q}_m = R_{\Theta, m} q, \quad \tilde{k}_n = R_{\Theta, n} k
$$

其中 $R_{\Theta, m}$ 是旋转矩阵：

$$
R_{\Theta, m} = \begin{pmatrix} \cos m\theta_0 & -\sin m\theta_0 & & \\ \sin m\theta_0 & \cos m\theta_0 & & \\ & & \ddots & \\ & & & \cos m\theta_{d/2-1} \\ & & & \sin m\theta_{d/2-1} \end{pmatrix}
$$

### 4.2 频率设置

$$
\Theta = \left\{\theta_i = 10000^{-2i/d}, i = 0, 1, ..., d/2-1\right\}
$$

**特点：**
- 低频维度（$i$ 小）：捕获长距离依赖
- 高频维度（$i$ 大）：捕获短距离依赖

### 4.3 相对位置性质

$$
\langle \tilde{q}_m, \tilde{k}_n \rangle = \langle R_{\Theta, m} q, R_{\Theta, n} k \rangle = \langle q, R_{\Theta, n-m} k \rangle
$$

内积只依赖相对位置 $m-n$。

### 4.4 外推方法

| 方法 | 思想 | 代表模型 |
|------|------|----------|
| NTK-aware | 缩放频率 | LLaMA 2 |
| YaRN | 插值 + 外推 | LongChat |
| PI (Position Interpolation) | 直接插值 | LongFormer |
| RoPE-2D | 扩展到 2D | Code LLaMA |

---

## 5. 位置编码对比

| 方法 | 类型 | 可学习 | 外推性 | 代表模型 |
|------|------|--------|--------|----------|
| Sinusoidal | 绝对 | 否 | 好 | 原始 Transformer |
| Learned | 绝对 | 是 | 差 | BERT, GPT-2 |
| RoPE | 相对 | 否 | 中 | LLaMA, Qwen |
| ALiBi | 相对 | 否 | 好 | BLOOM |
| NoPE | 无 | - | - | Mamba, RWKV |

---

## 6. 实践建议

### 6.1 选择指南

| 场景 | 推荐 | 原因 |
|------|------|------|
| 通用 LLM | RoPE | 平衡性能与外推 |
| 超长上下文 | ALiBi | 外推性最好 |
| 固定长度任务 | Learned | 简单有效 |
| 状态空间模型 | 无 | 不需要位置编码 |

### 6.2 长度外推技巧

**问题：** 训练时最大长度 2048，推理时想用到 8192。

**方法 1：位置插值 (PI)**

$$
PE'_{pos} = PE_{pos \cdot L_{train}/L_{target}}
$$

**方法 2：NTK-aware 缩放**

$$
\theta'_i = \theta_i \cdot (L_{target}/L_{train})^{d/(d-2)}
$$

**方法 3：YaRN**

结合插值和外推，动态调整不同频率的缩放。

---

## 7. 数学推导

### 7.1 RoPE 旋转矩阵推导

设 $q = (q_0, q_1, ..., q_{d-1})$，将其分成 $d/2$ 对：

$$
q^{(i)} = (q_{2i}, q_{2i+1}), \quad i = 0, 1, ..., d/2-1
$$

对每对应用 2D 旋转：

$$
R_{\theta_i, m} q^{(i)} = \begin{pmatrix} \cos m\theta_i & -\sin m\theta_i \\ \sin m\theta_i & \cos m\theta_i \end{pmatrix} \begin{pmatrix} q_{2i} \\ q_{2i+1} \end{pmatrix}
$$

### 7.2 相对位置性质证明

$$
\langle R_{\Theta, m} q, R_{\Theta, n} k \rangle = \sum_{i=0}^{d/2-1} \langle R_{\theta_i, m} q^{(i)}, R_{\theta_i, n} k^{(i)} \rangle
$$

由于旋转保持内积：

$$
= \sum_{i=0}^{d/2-1} \langle q^{(i)}, R_{\theta_i, n-m} k^{(i)} \rangle = \langle q, R_{\Theta, n-m} k \rangle
$$

---

## 8. 常见问题

### Q1: 为什么 RoPE 比 Learned PE 好？

- 天然支持相对位置
- 可以外推到更长序列（配合插值）
- 不需要额外的参数

### Q2: 位置编码应该加还是乘？

**加法（主流）：**

$$
x = \text{TokenEmbed} + PE
$$

**乘法（少数）：**

$$
x = \text{TokenEmbed} \odot (1 + PE)
$$

加法更简单，实验效果更好。

### Q3: 为什么不用 1, 2, 3, ... 作为位置编码？

数值会随位置增大而增大，导致梯度不稳定，且无法泛化到未见过的长度。

---

## 9. 延伸阅读

- [Transformer 架构详解](transformer-architecture.md)
- [自注意力机制](self-attention.md)
- [RoPE 论文](https://arxiv.org/abs/2104.09864)

---

*最后更新：2026-06-22*
