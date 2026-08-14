# VAE 原理 (Variational Autoencoder)

## 1. 核心思想

通过编码器学习数据的隐变量分布，再用解码器从隐变量生成新数据。

## 2. 架构

### 2.1 编码器

    q_phi(z|x) = N(mu, sigma^2)

将输入 x 映射到隐空间分布。

### 2.2 解码器

    p_theta(x|z)

从隐变量 z 重建数据。

## 3. 训练目标

    L = E_q[log p(x|z)] - D_KL(q(z|x) || p(z))

第一项：重建损失
第二项：KL 散度正则化

## 4. 重参数化技巧

直接从分布采样不可导，使用：

    z = mu + sigma * epsilon,  epsilon ~ N(0, I)

## 5. 变体

| 变体 | 创新 |
|------|------|
| VQ-VAE | 离散隐变量 |
| dVAE | 离散化，DALL-E 使用 |
| Beta-VAE | 调整 KL 权重 |

## 6. 延伸阅读

- [VQ-VAE-2 论文](../papers/2019-06-01-vq-vae-2.md)
- [GAN](gan.md)

---

*最后更新：2026-06-22*
