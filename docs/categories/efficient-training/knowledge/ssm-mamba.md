# 状态空间模型 (SSM / Mamba)

## 1. 核心思想

用状态空间模型替代注意力机制，实现线性复杂度的序列建模。

## 2. S4 (Structured State Space)

### 2.1 连续时间 SSM

    h'(t) = A*h(t) + B*x(t)
    y(t) = C*h(t)

### 2.2 离散化

    h_t = A_bar * h_{t-1} + B_bar * x_t
    y_t = C * h_t

### 2.3 结构化

A 矩阵使用特殊结构（如 HiPPO），使系统稳定且可并行训练。

## 3. Mamba

### 3.1 选择性机制

SSM 的参数随输入变化：

    B, C, Delta = f(x)

使模型能够选择性地关注或忽略信息。

### 3.2 硬件感知

优化 CUDA 内核，充分利用 GPU 内存层次。

## 4. 与 Transformer 对比

| 方面 | Transformer | Mamba |
|------|-------------|-------|
| 复杂度 | O(n^2) | O(n) |
| 并行训练 | 好 | 好 |
| 长序列 | 差 | 好 |
| 质量 | 最好 | 接近 |

## 5. 延伸阅读

- [Mamba 论文](https://arxiv.org/abs/2312.00752)
- [S4 论文](https://arxiv.org/abs/2111.00396)

---

*最后更新：2026-06-22*
