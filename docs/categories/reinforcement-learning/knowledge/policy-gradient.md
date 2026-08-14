# 策略梯度 (Policy Gradient)

## 1. 核心思想

直接优化策略参数，最大化期望回报。

    theta* = argmax_theta J(theta) = E_pi[R]

## 2. REINFORCE 算法

### 2.1 策略梯度定理

    grad J(theta) = E[sum_t grad log pi(a_t|s_t) * G_t]

### 2.2 算法流程

1. 用当前策略采样一个回合
2. 计算每步的回报 G_t
3. 更新策略参数

## 3. 方差问题

### 3.1 问题

策略梯度估计方差大，训练不稳定。

### 3.2 解决方案

| 方法 | 说明 |
|------|------|
| 基线 | 减去 V(s)，减少方差 |
| 优势函数 | 用 A(s,a) 替代 G_t |
| 广义优势估计 (GAE) | 平衡偏差和方差 |

## 4. Actor-Critic

### 4.1 架构

- Actor: 策略网络 pi(a|s)
- Critic: 价值网络 V(s)

### 4.2 优势

- 单步更新（不需要完整回合）
- 方差更低
- 适用于连续动作空间

## 5. 延伸阅读

- [PPO 详解](ppo-detailed.md)
- [价值函数](value-function.md)

---

*最后更新：2026-06-22*
