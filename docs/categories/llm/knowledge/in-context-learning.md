# In-Context Learning (上下文学习)

## 1. 核心思想

模型无需参数更新，仅通过提示中的几个示例就能学会新任务。

```
Q: 苹果 → 水果
Q: 白菜 → 蔬菜
Q: 牛排 → 肉类
Q: 牛奶 → ?
A: 乳制品
```

---

## 2. 机制分析

### 2.1 隐式梯度下降

研究表明 Transformer 的注意力层可以隐式执行梯度下降：

$$
x_{l+1} = x_l + \alpha \nabla_\theta \mathcal{L}_{\text{task}}(\theta)
$$

每一层相当于在任务上做一步参数更新。

### 2.2 任务检索

模型通过预训练学到的知识，用示例"检索"对应的任务模式。

### 2.3 注意力机制

注意力权重可以看作是在示例和查询之间做插值：

$$
\text{Attention}(Q, K, V) = \sum_i \alpha_i v_i
$$

其中 $\alpha_i \propto \exp(q \cdot k_i / \sqrt{d})$

---

## 3. 影响 ICL 效果的因素

### 3.1 示例选择

| 因素 | 影响 |
|------|------|
| 多样性 | 高：覆盖不同情况 |
| 难度 | 中：适中难度最好 |
| 相关性 | 高：与测试样本相似 |
| 顺序 | 高：最后一个示例影响最大 |

### 3.2 示例数量

| 数量 | 效果 |
|------|------|
| 0-shot | 基线 |
| 1-shot | 显著提升 |
| 4-shot | 接近饱和 |
| 8-shot+ | 收益递减 |

### 3.3 模型规模

- 小模型 (< 1B)：ICL 效果差
- 中模型 (1B-10B)：部分任务有效
- 大模型 (> 10B)：ICL 效果显著

---

## 4. 变体

### 4.1 提示方法

| 方法 | 示例 | 适用场景 |
|------|------|----------|
| Few-shot | 提供多个示例 | 通用 |
| Zero-shot | 无示例，靠描述 | 简单任务 |
| One-shot | 一个示例 | 示例成本高 |
| Chain-of-thought | 展示推理过程 | 复杂推理 |

### 4.2 动态示例选择

**方法：** 为每个测试样本动态检索最相关的示例

```python
def dynamic_icl(query, database, k=4):
    similar_examples = retrieve(query, database, top_k=k)
    prompt = format_examples(similar_examples) + format_query(query)
    return generate(prompt)
```

**效果：** 比固定示例提升 5-15%

---

## 5. 局限性

| 局限 | 说明 | 解决 |
|------|------|------|
| 上下文长度 | 示例越多，token 越多 | 压缩提示 |
| 示例偏差 | 示例分布影响输出 | 多样化 |
| 顺序敏感 | 不同顺序结果不同 | 多顺序取均值 |
| 无法微调 | 模型参数不更新 | 结合微调 |

---

## 6. 延伸阅读

- [GPT-3 论文](../papers/2020-05-28-gpt3.md)
- [思维链](chain-of-thought.md)
- [涌现能力](emergent-abilities.md)

---

*最后更新：2026-06-22*
