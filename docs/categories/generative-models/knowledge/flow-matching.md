# Flow Matching

## 1. 核心思想

通过连续正则化流 (Continuous Normalizing Flow) 学习从噪声到数据的映射。

## 2. 与扩散模型的关系

扩散模型是 Flow Matching 的特例。

| 方面 | 扩散模型 | Flow Matching |
|------|----------|---------------|
| 前向过程 | 固定 SDE | 可选 ODE |
| 训练目标 | 预测噪声 | 预测向量场 |
| 采样 | SDE/ODE | ODE |
| 路径 | 曲线 | 直线（OT） |

## 3. 核心公式

### 3.1 向量场

    v_t(x) = d/dt psi_t(x)

其中 psi_t 是从噪声到数据的流。

### 3.2 训练目标

    L = E[||v_theta(x_t, t) - u_t(x_t)||^2]

其中 u_t 是目标向量场。

## 4. 优势

- 训练更简单
- 采样路径更直（OT 条件流）
- 可以用更少步数生成

## 5. 应用

- Stable Diffusion 3
- FLUX
- 视频生成

## 6. 延伸阅读

- [Flow Matching 论文](../papers/2022-10-03-flow-matching.md)
- [扩散模型](diffusion-models.md)

---

*最后更新：2026-06-22*
