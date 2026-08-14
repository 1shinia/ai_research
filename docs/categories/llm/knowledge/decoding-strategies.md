# 解码策略 (Decoding Strategies)

## 1. 概述

解码策略决定如何从模型的概率分布中生成 token。不同策略在质量和多样性之间权衡。

---

## 2. 贪婪解码 (Greedy Decoding)

### 2.1 算法

每步选择概率最高的 token：

$$
y_t = \arg\max_{y} P(y | y_{<t}, x)
$$

### 2.2 特点

| 优点 | 缺点 |
|------|------|
| 确定性，可复现 | 容易重复 |
| 速度快 | 缺乏多样性 |
| 实现简单 | 可能陷入循环 |

### 2.3 适用场景

- 事实性问答
- 代码生成
- 需要确定性输出的任务

---

## 3. 束搜索 (Beam Search)

### 3.1 算法

维护 $k$ 个候选序列（束），每步扩展所有候选，保留概率最高的 $k$ 个。

```
初始化：beam = [empty]
for t in 1...T:
    candidates = []
    for beam_seq in beam:
        for token in vocab:
            score = P(token | beam_seq) * beam_seq.score
            candidates.append((beam_seq + token, score))
    beam = top_k(candidates, k)
```

### 3.2 束大小选择

| 束大小 | 效果 |
|--------|------|
| 1 | 等价于贪婪 |
| 4-8 | 推荐（平衡质量与速度） |
| 16+ | 收益递减 |

### 3.3 特点

| 优点 | 缺点 |
|------|------|
| 比贪婪更好 | 计算量大 |
| 全局优化 | 缺乏多样性 |
| 适合翻译 | 可能过于保守 |

---

## 4. 采样方法

### 4.1 温度采样 (Temperature Sampling)

$$
P'(y) = \frac{\exp(\log P(y) / T)}{\sum_{y'} \exp(\log P(y') / T)}
$$

| 温度 | 效果 |
|------|------|
| T < 1 | 更确定，接近贪婪 |
| T = 1 | 原始分布 |
| T > 1 | 更随机，更多样 |

**推荐：** T = 0.7-0.9

### 4.2 Top-K 采样

只从概率最高的 $k$ 个 token 中采样：

$$
P'(y) = \begin{cases} \frac{P(y)}{\sum_{y' \in \text{TopK}} P(y')} & y \in \text{TopK} \\ 0 & \text{otherwise} \end{cases}
$$

| K 值 | 效果 |
|------|------|
| K = 1 | 等价于贪婪 |
| K = 10-50 | 推荐 |
| K = 100+ | 可能采样到低质量 token |

### 4.3 Top-P 采样 (Nucleus Sampling)

从累积概率达到 $p$ 的最小 token 集合中采样：

$$
V' = \{y_1, y_2, ..., y_k\} \quad \text{s.t.} \quad \sum_{i=1}^{k} P(y_i) \geq p
$$

$$
P'(y) = \begin{cases} \frac{P(y)}{\sum_{y' \in V'} P(y')} & y \in V' \\ 0 & \text{otherwise} \end{cases}
$$

| P 值 | 效果 |
|------|------|
| P = 0.5 | 较确定 |
| P = 0.9 | 推荐 |
| P = 1.0 | 等价于无截断 |

---

## 5. 组合策略

### 5.1 Top-K + Top-P

先用 Top-K 过滤，再用 Top-P 采样：

```python
def sample(logits, top_k=50, top_p=0.9, temperature=0.8):
    logits = logits / temperature
    # Top-K
    if top_k > 0:
        indices_to_remove = logits < torch.topk(logits, top_k).values[..., -1, None]
        logits[indices_to_remove] = -float('inf')
    # Top-P
    if top_p < 1.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        sorted_indices_to_remove = cumulative_probs > top_p
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0
        indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
        logits[indices_to_remove] = -float('inf')
    # 采样
    probs = F.softmax(logits, dim=-1)
    return torch.multinomial(probs, 1)
```

### 5.2 推荐配置

| 任务 | Temperature | Top-K | Top-P |
|------|-------------|-------|-------|
| 创意写作 | 0.9 | 40 | 0.95 |
| 问答 | 0.7 | 20 | 0.9 |
| 代码生成 | 0.2 | 10 | 0.95 |
| 翻译 | 0.7 | 50 | 0.95 |

---

## 6. 高级解码

### 6.1 重复惩罚 (Repetition Penalty)

降低已生成 token 的概率：

$$
P'(y) = \begin{cases} P(y) / \text{penalty} & y \in \text{generated} \\ P(y) & \text{otherwise} \end{cases}
$$

**推荐：** penalty = 1.1-1.2

### 6.2 频率惩罚 (Frequency Penalty)

根据出现次数线性降低概率：

$$
P'(y) = P(y) - \alpha \cdot \text{count}(y)
$$

### 6.3 存在惩罚 (Presence Penalty)

只要出现过就降低概率：

$$
P'(y) = P(y) - \beta \cdot \mathbb{1}[y \in \text{generated}]
$$

---

## 7. 对比总结

| 策略 | 质量 | 多样性 | 速度 | 确定性 |
|------|------|--------|------|--------|
| 贪婪 | 中 | 低 | 快 | 是 |
| 束搜索 | 高 | 低 | 中 | 是 |
| 温度采样 | 中 | 高 | 快 | 否 |
| Top-K | 中 | 中 | 快 | 否 |
| Top-P | 高 | 高 | 快 | 否 |
| 组合策略 | 高 | 高 | 快 | 否 |

---

## 8. 实践技巧

### 8.1 调试方法

**观察概率分布：**

```python
probs = F.softmax(logits, dim=-1)
top5 = torch.topk(probs, 5)
print(f"Top-5 tokens: {top5.indices}, probs: {top5.values}")
```

**监控生成质量：**

- 重复率：连续 n-gram 重复的比例
- 多样性：不同 token 的比例
- 长度：生成序列长度

### 8.2 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 重复 | 温度太低 | 增加温度/重复惩罚 |
| 不连贯 | 温度太高 | 降低温度/用 Top-P |
| 太短 | EOS 概率高 | 调整长度惩罚 |
| 太长 | EOS 概率低 | 设置最大长度 |

---

## 9. 数学推导

### 9.1 束搜索概率

束搜索最大化序列概率：

$$
y^* = \arg\max_{y} \prod_{t=1}^{T} P(y_t | y_{<t}, x)
$$

等价于最大化对数概率：

$$
y^* = \arg\max_{y} \sum_{t=1}^{T} \log P(y_t | y_{<t}, x)
$$

### 9.2 温度缩放

温度 $T$ 改变分布的熵：

$$
H(P') = -\sum_y P'(y) \log P'(y)
$$

- $T < 1$：熵降低，分布更尖锐
- $T > 1$：熵增加，分布更平滑

---

## 10. 延伸阅读

- [解码策略对比](https://huggingface.co/blog/how-to-generate)
- [思维链](chain-of-thought.md)
- [In-Context Learning](in-context-learning.md)

---

*最后更新：2026-06-22*
