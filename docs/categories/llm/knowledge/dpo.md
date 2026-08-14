# DPO 直接偏好优化 (Direct Preference Optimization)

## 1. 核心思想

DPO 跳过奖励模型训练，直接从人类偏好数据优化语言模型策略。

### 1.1 动机

RLHF 的问题：
- 需要训练奖励模型（额外成本）
- PPO 训练不稳定
- 超参数敏感

DPO 的解决：
- 无需奖励模型
- 标准分类损失
- 训练稳定

---

## 2. 数学推导

### 2.1 从 RLHF 到 DPO

**RLHF 目标：**

$$
\max_\pi \mathbb{E}_{x,y} [r(x,y)] - \beta D_{KL}(\pi || \pi_{ref})
$$

**最优策略：**

$$
\pi^*(y|x) = \frac{1}{Z(x)} \pi_{ref}(y|x) \exp(r(x,y)/\beta)
$$

其中 $Z(x)$ 是归一化常数。

**反解奖励：**

$$
r(x,y) = \beta \log \frac{\pi^*(y|x)}{\pi_{ref}(y|x)} + \beta \log Z(x)
$$

### 2.2 Bradley-Terry 模型

人类偏好概率：

$$
P(y_c \succ y_r | x) = \sigma(r(x,y_c) - r(x,y_r))
$$

代入奖励表达式：

$$
r(x,y_c) - r(x,y_r) = \beta \log \frac{\pi(y_c|x)}{\pi_{ref}(y_c|x)} - \beta \log \frac{\pi(y_r|x)}{\pi_{ref}(y_r|x)}
$$

注意：$Z(x)$ 项抵消了！

### 2.3 DPO 损失函数

$$
\mathcal{L}_{DPO} = -\log \sigma\left(\beta \log \frac{\pi_\theta(y_c|x)}{\pi_{ref}(y_c|x)} - \beta \log \frac{\pi_\theta(y_r|x)}{\pi_{ref}(y_r|x)}\right)
$$

**直觉：**
- 让 chosen 的对数几率比高于 rejected
- $\beta$ 控制偏离参考策略的程度

---

## 3. 实现细节

### 3.1 对数几率比

$$
\text{logit}_c = \log \pi_\theta(y_c|x) - \log \pi_{ref}(y_c|x)
$$

$$
\text{logit}_r = \log \pi_\theta(y_r|x) - \log \pi_{ref}(y_r|x)
$$

**计算：**

```python
# 前向计算
log_probs = model(input_ids, labels=labels).logits
ref_log_probs = ref_model(input_ids, labels=labels).logits

# 计算对数几率比
log_ratio = log_probs - ref_log_probs
```

### 3.2 梯度计算

$$
\nabla_\theta \mathcal{L}_{DPO} = -\beta \sigma\left(-\Delta\right) \left(\nabla_\theta \log \pi_\theta(y_c|x) - \nabla_\theta \log \pi_\theta(y_r|x)\right)
$$

其中 $\Delta = \beta(\text{logit}_c - \text{logit}_r)$

**特点：** 梯度只依赖策略模型，不需要奖励模型的反向传播。

---

## 4. 与 RLHF 对比

| 维度 | RLHF | DPO |
|------|------|-----|
| 奖励模型 | 需要 | 不需要 |
| 训练阶段 | 3 阶段 | 1 阶段 |
| 训练稳定性 | 低（PPO） | 高（交叉熵） |
| 超参数 | 多 | 少（主要 $\beta$） |
| 计算成本 | 高 | 低 |
| 性能 | 相当 | 相当或更好 |

---

## 5. 超参数选择

### 5.1 $\beta$ 参数

| 值 | 效果 |
|-----|------|
| 0.01 | 几乎不偏离参考策略 |
| 0.1 | 适度偏离（推荐） |
| 0.5 | 较大偏离 |
| 1.0 | 很大偏离，可能不稳定 |

**推荐：** $\beta = 0.1$

### 5.2 学习率

| 模型规模 | 学习率 |
|----------|--------|
| 7B | 5e-7 |
| 13B | 3e-7 |
| 70B | 1e-7 |

### 5.3 Batch Size

- 推荐：256-512
- 太小：训练不稳定
- 太大：泛化能力下降

---

## 6. 变体

### 6.1 KTO (Kahneman-Tversky Optimization)

**特点：** 不需要配对数据，单个样本即可。

$$
\mathcal{L}_{KTO} = -\lambda_c \log \sigma(\beta(\log \pi_\theta(y|x) - \log \pi_{ref}(y|x)))
$$

其中 $\lambda_c$ 是前景权重（prospect theory）。

### 6.2 IPO (Identity Preference Optimization)

**改进：** 使用 hinge loss 替代 sigmoid。

$$
\mathcal{L}_{IPO} = \max(0, 1 - (\text{logit}_c - \text{logit}_r))
$$

### 6.3 ORPO (Odds Ratio Preference Optimization)

**特点：** 不需要参考模型。

---

## 7. 实践技巧

### 7.1 数据质量

| 要点 | 说明 |
|------|------|
| 多样性 | 覆盖不同场景 |
| 难度 | 混合简单/困难样本 |
| 标注一致性 | 多标注者交叉验证 |
| 去重 | 避免数据泄露 |

### 7.2 训练监控

**关键指标：**

- **准确率：** chosen 被正确预测的比例
- **对数几率差：** $\text{logit}_c - \text{logit}_r$
- **KL 散度：** 与参考策略的偏离

**理想曲线：**
- 准确率：60-80%（太高可能过拟合）
- 对数几率差：稳定增长
- KL 散度：缓慢增长

### 7.3 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 训练崩溃 | 学习率太大 | 减小学习率 |
| 过拟合 | 数据太少 | 增加数据/早停 |
| 性能下降 | $\beta$ 太大 | 减小 $\beta$ |
| 生成重复 | 探索不足 | 增加 temperature |

---

## 8. 代码示例

```python
import torch
import torch.nn.functional as F

def dpo_loss(model, ref_model, batch, beta=0.1):
    """
    batch: {
        'input_ids': ...,
        'chosen_ids': ...,
        'rejected_ids': ...
    }
    """
    # 计算策略模型的对数概率
    chosen_log_probs = model(batch['input_ids'], labels=batch['chosen_ids']).logits
    rejected_log_probs = model(batch['input_ids'], labels=batch['rejected_ids']).logits
    
    # 计算参考模型的对数概率
    with torch.no_grad():
        ref_chosen_log_probs = ref_model(batch['input_ids'], labels=batch['chosen_ids']).logits
        ref_rejected_log_probs = ref_model(batch['input_ids'], labels=batch['rejected_ids']).logits
    
    # 计算对数几率比
    chosen_log_ratio = chosen_log_probs - ref_chosen_log_probs
    rejected_log_ratio = rejected_log_probs - ref_rejected_log_probs
    
    # DPO 损失
    logits = beta * (chosen_log_ratio - rejected_log_ratio)
    loss = -F.logsigmoid(logits).mean()
    
    return loss
```

---

## 9. 数学证明

### 9.1 最优策略

**定理：** 在 Bradley-Terry 模型下，DPO 的最优解等价于 RLHF 的最优解。

**证明：**

RLHF 最优策略：
$$
\pi^*(y|x) \propto \pi_{ref}(y|x) \exp(r(x,y)/\beta)
$$

代入 Bradley-Terry：
$$
P(y_c \succ y_r | x) = \sigma(r(x,y_c) - r(x,y_r))
$$

$$
= \sigma\left(\beta \log \frac{\pi^*(y_c|x)}{\pi_{ref}(y_c|x)} - \beta \log \frac{\pi^*(y_r|x)}{\pi_{ref}(y_r|x)}\right)
$$

这正是 DPO 优化的目标。$\blacksquare$

---

## 10. 延伸阅读

- [DPO 论文](../papers/2023-05-29-dpo.md)
- [RLHF 完整流程](rlhf-pipeline.md)
- [PPO 算法](../../reinforcement-learning/papers/2017-07-20-ppo.md)

---

*最后更新：2026-06-22*
