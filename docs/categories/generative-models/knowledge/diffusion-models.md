# 扩散模型详解

## 1. 核心思想

通过逐步去噪从噪声中生成数据。

## 2. 前向过程 (加噪)

    q(x_t | x_0) = N(x_t; sqrt(alpha_t) * x_0, (1-alpha_t) * I)

其中 alpha_t 是累积的噪声调度。

## 3. 反向过程 (去噪)

    p_theta(x_{t-1} | x_t) = N(x_{t-1}; mu_theta(x_t, t), sigma_t^2 * I)

训练神经网络预测噪声或均值。

## 4. 训练目标

简化后的噪声预测损失：

    L = E[||epsilon - epsilon_theta(x_t, t)||^2]

## 5. 噪声调度

| 调度 | 公式 | 特点 |
|------|------|------|
| 线性 | beta_t = a + b*t | 简单 |
| 余弦 | alpha_t = cos(...) | 更平滑 |
| 缩放线性 | beta_t = c * t | 稳定 |

## 6. 条件生成

### 6.1 分类器引导

    epsilon_guided = epsilon + w * grad_log_p(y|x_t)

### 6.2 分类器自由引导 (CFG)

    epsilon_guided = epsilon_uncond + w * (epsilon_cond - epsilon_uncond)

## 7. 延伸阅读

- [DDPM 论文](../papers/2020-06-19-ddpm.md)
- [DDIM](../papers/2020-10-04-ddim.md)
- [Latent Diffusion](../papers/2021-12-20-latent-diffusion.md)

---

*最后更新：2026-06-22*
