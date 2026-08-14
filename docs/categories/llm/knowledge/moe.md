# MoE 混合专家架构 (Mixture of Experts)

## 1. 核心思想

MoE 的核心是**稀疏激活**：每次推理只激活模型的一部分参数，从而在相同计算成本下实现更大参数量。

$$
\text{MoE}(x) = \sum_{i=1}^{N} G(x)_i \cdot E_i(x)
$$

其中：
- $N$：专家总数
- $E_i$：第 $i$ 个专家（通常是 FFN）
- $G(x)$：门控网络，决定激活哪些专家

---

## 2. 架构设计

### 2.1 专家网络

每个专家通常是一个 FFN：

$$
E_i(x) = \text{FFN}_i(x) = W_{out}^{(i)} \cdot \text{Act}(W_{in}^{(i)} x)
$$

**参数量：** 每个专家 $d \times d_{ff} + d_{ff} \times d$

### 2.2 门控网络

#### Top-K 路由

$$
G(x) = \text{TopK}(\text{softmax}(W_g x), k)
$$

只保留概率最高的 $k$ 个专家，其余置 0。

**常见选择：** $k=1$ 或 $k=2$

#### 负载均衡损失

防止所有 token 都路由到少数专家：

$$
\mathcal{L}_{balance} = N \sum_{i=1}^{N} f_i \cdot P_i
$$

其中：
- $f_i$：batch 中路由到专家 $i$ 的 token 比例
- $P_i$：门控预测路由到专家 $i$ 的平均概率

**目标：** 最小化时，所有专家被均匀使用。

---

## 3. 关键变体

### 3.1 Switch Transformer

**特点：** $k=1$，每个 token 只路由到一个专家

$$
\text{Switch}(x) = E_{\text{argmax}(G(x))}(x)
$$

**优点：** 计算效率最高

**缺点：** 路由决策是硬分配，梯度可能不稳定

### 3.2 GLaM (Generalist Language Model)

**特点：** 双 MoE，每层有两个 MoE 层（一个在注意力前，一个在注意力后）

**规模：** 1.2T 参数，但每次推理只激活 96B

### 3.3 Mixtral 8x7B

**特点：** 8 个专家，$k=2$，基于 LLaMA 架构

**性能：** 接近 LLaMA 70B，但推理成本只有 1/6

---

## 4. 训练技巧

### 4.1 专家容量 (Expert Capacity)

限制每个专家处理的 token 数量，防止某些专家过载：

$$
C = \frac{T \cdot \text{capacity\_factor}}{N}
$$

其中 $T$ 是总 token 数，$N$ 是专家数。

**溢出处理：** 超过容量的 token 被丢弃或路由到下一个专家。

### 4.2 辅助损失

除了负载均衡，还有：

**重要性损失：**

$$
\mathcal{L}_{importance} = \text{CV}(f)^2
$$

其中 $\text{CV}$ 是变异系数，衡量专家使用的不均匀性。

### 4.3 初始化

**专家初始化：** 从预训练的稠密 FFN 复制，或随机初始化

**门控初始化：** 小随机值，避免初始路由过于集中

---

## 5. 推理优化

### 5.1 专家并行

将不同专家放在不同 GPU 上：

```
GPU 0: Expert 1, Expert 2
GPU 1: Expert 3, Expert 4
...
```

**通信：** 需要 All-to-All 通信发送 token 到对应专家。

### 5.2 专家缓存

**思想：** 热门专家常驻 GPU，冷门专家按需加载。

**适用场景：** 专家数量远大于 GPU 数量时。

### 5.3 量化

对专家进行量化（如 INT8、INT4），减少显存占用。

---

## 6. 复杂度分析

### 6.1 参数量

| 配置 | 总参数 | 激活参数 | 比例 |
|------|--------|----------|------|
| 稠密 7B | 7B | 7B | 100% |
| 8x7B MoE | 46B | 12B | 26% |
| 8x22B MoE | 141B | 39B | 28% |

### 6.2 计算量

**FLOPs：** 只与激活参数相关，与总参数无关。

**内存带宽：** 需要加载所有专家参数（即使不激活），这是主要瓶颈。

### 6.3 通信开销

| 并行策略 | 通信量 | 说明 |
|----------|--------|------|
| 专家并行 | $O(T \cdot d)$ | All-to-All 发送 token |
| 数据并行 | $O(P)$ | 梯度同步，$P$ 为参数量 |

---

## 7. 与稠密模型对比

| 维度 | 稠密模型 | MoE 模型 |
|------|----------|----------|
| 参数量 | 全部激活 | 部分激活 |
| 训练效率 | 低 | 高（相同计算下更大模型） |
| 推理效率 | 高（参数少） | 低（需要加载所有专家） |
| 显存需求 | 低 | 高（存储所有专家） |
| 训练稳定性 | 好 | 需要负载均衡 |
| 适用场景 | 部署优先 | 训练优先 |

---

## 8. 实践指南

### 8.1 何时使用 MoE？

**适合：**
- 训练资源有限，但想训练大模型
- 可以接受较高的推理成本
- 有足够 GPU 做专家并行

**不适合：**
- 部署到资源受限环境
- 需要低延迟推理
- GPU 数量少于专家数

### 8.2 超参数选择

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 专家数 $N$ | 8 | 平衡效率与容量 |
| Top-K $k$ | 1-2 | 1 最高效，2 更稳定 |
| 容量因子 | 1.0-1.25 | 太小会丢弃 token |
| 负载均衡权重 | 0.01-0.1 | 太大影响主任务 |

### 8.3 调试技巧

**监控专家负载：**

```python
expert_usage = torch.bincount(expert_indices, minlength=N)
print(f"Expert usage: {expert_usage}")
```

**理想情况：** 所有专家使用量接近 $T/N$

---

## 9. 数学推导

### 9.1 梯度流动

对于 Top-1 路由，只有被选中的专家接收梯度：

$$
\frac{\partial \mathcal{L}}{\partial E_i} = \begin{cases} \frac{\partial \mathcal{L}}{\partial \text{MoE}} \cdot G(x)_i & \text{if } i = \text{argmax}(G(x)) \\ 0 & \text{otherwise} \end{cases}
$$

### 9.2 负载均衡梯度

$$
\frac{\partial \mathcal{L}_{balance}}{\partial W_g} = N \sum_{i=1}^{N} \left(f_i \frac{\partial P_i}{\partial W_g} + P_i \frac{\partial f_i}{\partial W_g}\right)
$$

---

## 10. 常见问题

### Q1: MoE 模型推理一定比稠密模型慢吗？

不一定。如果激活参数量相同，MoE 可能更快（因为 FFN 层更小）。但需要加载所有专家参数到内存。

### Q2: 为什么不用更多专家？

- 通信开销随专家数增加
- 负载均衡更难
- 显存需求线性增长

### Q3: MoE 和模型并行有什么区别？

- **MoE：** 稀疏激活，不同 token 用不同专家
- **模型并行：** 稠密计算，所有 token 用所有参数

---

## 11. 延伸阅读

- [Switch Transformer 论文](../papers/2022-01-12-switch-transformer.md)
- [FlashAttention](../../efficient-training/papers/2022-05-23-flash-attention.md)
- [vLLM](../../efficient-training/papers/2023-09-01-vllm-paged-attention.md)

---

*最后更新：2026-06-22*
