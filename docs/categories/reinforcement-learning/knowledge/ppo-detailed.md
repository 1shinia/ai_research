# PPO 详解 (Proximal Policy Optimization)

## 1. 动机

TRPO 用二阶优化保证策略更新幅度小，但实现复杂。PPO 用一阶优化达到类似效果。

## 2. 核心公式

### 2.1 重要性采样比率

    r_t(theta) = pi_theta(a_t|s_t) / pi_old(a_t|s_t)

### 2.2 截断目标函数

    L = min(r_t * A_t, clip(r_t, 1-epsilon, 1+epsilon) * A_t)

其中 epsilon 通常取 0.2。

## 3. 截断机制

### 3.1 正优势 (A > 0)

- r_t < 1-epsilon: 不截断（鼓励增加概率）
- 1-epsilon <= r_t <= 1+epsilon: 正常更新
- r_t > 1+epsilon: 截断（防止过度增加）

### 3.2 负优势 (A < 0)

- r_t < 1-epsilon: 截断（防止过度减少）
- 1-epsilon <= r_t <= 1+epsilon: 正常更新
- r_t > 1+epsilon: 不截断（鼓励减少概率）

## 4. 完整目标函数

    L = L_policy - c1 * L_value + c2 * entropy

| 项 | 说明 |
|-----|------|
| L_policy | 策略损失 |
| L_value | 价值函数损失 |
| entropy | 熵正则（鼓励探索） |

## 5. 超参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| epsilon | 0.2 | 截断范围 |
| learning rate | 3e-4 | 学习率 |
| GAE lambda | 0.95 | 优势估计参数 |
| gamma | 0.99 | 折扣因子 |
| epochs | 4-10 | 每批数据的更新次数 |
| batch size | 256-4096 | 批次大小 |

## 6. 延伸阅读

- [PPO 论文](../papers/2017-07-20-ppo.md)
- [策略梯度](policy-gradient.md)
- [RLHF 原理](rlhf-explained.md)

---

*最后更新：2026-06-22*
