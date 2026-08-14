# 扩散模型原理

## 1. 核心思想

通过逐步去噪从噪声中生成数据。

前向过程：数据 -> 逐步加噪 -> 纯噪声
反向过程：纯噪声 -> 逐步去噪 -> 数据

## 2. DDPM 详解

### 2.1 前向过程

    q(x_t | x_{t-1}) = N(x_t; sqrt(1-beta_t) * x_{t-1}, beta_t * I)

逐步添加高斯噪声，直到变成纯噪声。

### 2.2 反向过程

    p_theta(x_{t-1} | x_t) = N(x_{t-1}; mu_theta(x_t, t), sigma_t^2 * I)

训练神经网络预测噪声（或均值）。

### 2.3 训练目标

简化后的损失函数：

    L = E[||epsilon - epsilon_theta(x_t, t)||^2]

只需预测噪声，无需预测均值。

## 3. 采样方法

| 方法 | 步数 | 质量 | 特点 |
|------|------|------|------|
| DDPM | 1000 | 最好 | 马尔可夫采样 |
| DDIM | 50-100 | 好 | 确定性采样 |
| DPM-Solver | 10-20 | 好 | ODE 求解器 |
| 一致性模型 | 1-4 | 中 | 蒸馏加速 |

## 4. 条件生成

### 4.1 分类器引导

用预训练分类器的梯度引导采样。

### 4.2 分类器自由引导 (CFG)

    epsilon_guided = epsilon_uncond + w * (epsilon_cond - epsilon_uncond)

w > 1 时增强条件影响。

## 5. 延伸阅读

- [DDPM 论文](../../generative-models/papers/2020-06-19-ddpm.md)
- [DDIM](../../generative-models/papers/2020-10-04-ddim.md)
- [Latent Diffusion](../../generative-models/papers/2021-12-20-latent-diffusion.md)

---

*最后更新：2026-06-22*
