# RLHF 完整流程 (Reinforcement Learning from Human Feedback)

## 1. 概述

RLHF 通过人类反馈训练语言模型，使其行为符合人类意图。是 ChatGPT 的核心技术。

### 1.1 三步流程

```
预训练模型 → SFT → 奖励模型 → PPO 优化 → 对齐模型
```

1. **SFT (监督微调)**：用人工标注的指令 - 回答对微调模型
2. **奖励模型训练**：训练模型预测人类偏好
3. **PPO 强化学习**：用奖励模型指导策略优化

---

## 2. 第一步：SFT 监督微调

### 2.1 数据收集

**格式：**

```json
{
  "instruction": "解释量子力学的基本原理",
  "input": "",
  "output": "量子力学是描述微观粒子行为的物理理论..."
}
```

**来源：**
- 人工标注（成本高，质量好）
- 筛选预训练数据中的对话
- 其他模型生成 + 人工筛选

### 2.2 训练目标

标准语言建模损失：

$$
\mathcal{L}_{SFT} = -\sum_{t=1}^{T} \log P(y_t | y_{<t}, x)
$$

其中 $x$ 是指令，$y$ 是回答。

### 2.3 关键技巧

| 技巧 | 作用 |
|------|------|
| 学习率衰减 | 避免过拟合 |
| 早停 | 保留泛化能力 |
| 数据去重 | 防止模型记忆 |
| 多轮对话 | 提升对话能力 |

---

## 3. 第二步：奖励模型训练

### 3.1 数据收集

**偏好数据格式：**

```json
{
  "prompt": "写一首关于春天的诗",
  "chosen": "春风拂柳绿，桃花映日红...",
  "rejected": "春天来了，花开了，草绿了..."
}
```

**标注方式：**
- 对同一 prompt，让模型生成多个回答
- 人工标注员排序或选择更好的回答

### 3.2 奖励模型架构

通常基于 SFT 模型，去掉生成头，加一个标量输出头：

$$
r_\theta(x, y) = \text{RewardModel}_\theta(x, y) \in \mathbb{R}
$$

### 3.3 训练目标

**Bradley-Terry 模型：**

$$
\mathcal{L}_{RM} = -\log \sigma(r_\theta(x, y_c) - r_\theta(x, y_r))
$$

其中：
- $y_c$：被选择的回答 (chosen)
- $y_r$：被拒绝的回答 (rejected)
- $\sigma$：sigmoid 函数

**直觉：** 让 chosen 的奖励高于 rejected。

### 3.4 训练技巧

| 技巧 | 说明 |
|------|------|
| 多标注者 | 减少个体偏差 |
| 难度分层 | 简单/中等/困难样本 |
| 正则化 | 防止奖励黑客 (reward hacking) |
| 归一化 | 奖励值范围控制 |

---

## 4. 第三步：PPO 强化学习

### 4.1 问题建模

| 元素 | 定义 |
|------|------|
| 状态 $s_t$ | 当前已生成的 token 序列 |
| 动作 $a_t$ | 下一个 token |
| 策略 $\pi_\theta$ | 语言模型 |
| 奖励 $r$ | 奖励模型的输出 |

### 4.2 PPO 目标函数

$$
\mathcal{L}_{PPO} = \mathbb{E}_{t} \left[ \min(r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t) \right]
$$

其中：
- $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{old}(a_t|s_t)}$：重要性采样比率
- $\hat{A}_t$：优势函数估计
- $\epsilon$：裁剪参数（通常 0.2）

### 4.3 完整损失函数

$$
\mathcal{L} = \mathcal{L}_{PPO} - c_1 \mathcal{L}_{VF} + c_2 S[\pi_\theta]
$$

- $\mathcal{L}_{VF}$：价值函数损失
- $S[\pi_\theta]$：策略熵（鼓励探索）
- $c_1, c_2$：系数

### 4.4 训练流程

```python
for iteration in range(num_iterations):
    # 1. 用当前策略生成样本
    prompts = sample_prompts()
    responses = policy.generate(prompts)
    
    # 2. 计算奖励
    rewards = reward_model(prompts, responses)
    
    # 3. 计算优势函数
    advantages = compute_advantages(rewards, value_model)
    
    # 4. PPO 更新
    for epoch in range(ppo_epochs):
        loss = ppo_loss(policy, old_policy, advantages)
        loss.backward()
        optimizer.step()
    
    # 5. 更新参考策略（KL 惩罚）
    old_policy = copy(policy)
```

---

## 5. 关键挑战与解决方案

### 5.1 奖励黑客 (Reward Hacking)

**问题：** 模型找到奖励模型的漏洞，生成高分但低质量的回答。

**示例：** 重复"这是一个很好的回答"以获得高分。

**解决方案：**

| 方法 | 说明 |
|------|------|
| KL 惩罚 | 限制与 SFT 模型的偏离 |
| 奖励归一化 | 防止奖励值过大 |
| 人类评估 | 定期检查生成质量 |
| 多奖励模型 |  ensemble 减少偏差 |

### 5.2 训练不稳定

**问题：** PPO 训练容易崩溃。

**解决方案：**

- **学习率预热**：前 100 步线性增加
- **梯度裁剪**：max_grad_norm = 1.0
- **小 batch 大小**：减少方差
- **多轮 PPO**：每个样本更新 2-4 次

### 5.3 分布偏移

**问题：** 模型生成的数据与训练数据分布不同。

**解决方案：**

- **经验回放**：混合旧数据
- **在线学习**：定期用新数据更新奖励模型
- **保守更新**：限制策略变化幅度

---

## 6. 变体与改进

### 6.1 DPO (Direct Preference Optimization)

**核心思想：** 跳过奖励模型，直接从偏好数据优化策略。

$$
\mathcal{L}_{DPO} = -\log \sigma\left(\beta \log \frac{\pi_\theta(y_c|x)}{\pi_{ref}(y_c|x)} - \beta \log \frac{\pi_\theta(y_r|x)}{\pi_{ref}(y_r|x)}\right)
$$

**优点：**
- 无需训练奖励模型
- 训练更稳定
- 实现更简单

详见：[DPO 原理](dpo.md)

### 6.2 KTO (Kahneman-Tversky Optimization)

**特点：** 不需要配对数据，单个样本即可训练。

### 6.3 RLHF 2.0

**改进：**
- 多轮对话反馈
- 细粒度奖励（按句子/段落）
- 在线偏好学习

---

## 7. 实践指南

### 7.1 数据规模建议

| 阶段 | 数据量 | 说明 |
|------|--------|------|
| SFT | 10K-100K | 高质量指令 - 回答对 |
| 奖励模型 | 50K-200K | 偏好对 |
| PPO | 10K-50K | 提示词 |

### 7.2 超参数推荐

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| SFT 学习率 | 1e-5 | 小学习率微调 |
| RM 学习率 | 5e-6 | 更小学习率 |
| PPO 学习率 | 1e-6 | 非常小 |
| PPO batch size | 256-512 | 平衡稳定性 |
| KL 系数 | 0.01-0.1 | 防止偏离太大 |
| 裁剪参数 ε | 0.2 | 标准值 |

### 7.3 评估指标

| 指标 | 说明 |
|------|------|
| 人类偏好胜率 | vs SFT 模型 |
| 毒性分数 | 有害内容比例 |
| 事实准确性 | 幻觉率 |
| 多样性 | 生成多样性 |

---

## 8. 数学推导

### 8.1 优势函数

$$
\hat{A}_t = \sum_{l=0}^{T-t} (\gamma \lambda)^l \delta_{t+l}
$$

其中 $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ 是 TD 误差。

### 8.2 KL 惩罚

$$
\mathcal{L}_{KL} = D_{KL}(\pi_\theta || \pi_{ref}) = \mathbb{E}_{\pi_\theta} \left[ \log \frac{\pi_\theta(a|s)}{\pi_{ref}(a|s)} \right]
$$

在 PPO 中通常作为奖励的一部分：

$$
r'_t = r_t - \beta \log \frac{\pi_\theta(a_t|s_t)}{\pi_{ref}(a_t|s_t)}
$$

---

## 9. 常见问题

### Q1: RLHF 一定比 SFT 好吗？

不一定。RLHF 需要大量数据和计算资源。对于简单任务，高质量 SFT 可能足够。

### Q2: 为什么不用人类直接打分，而用偏好？

偏好标注（A vs B）比绝对打分（1-5 分）更可靠，标注者间一致性更高。

### Q3: PPO 为什么比 REINFORCE 好？

- 方差更低（有基线）
- 样本效率更高（重要性采样）
- 训练更稳定（裁剪机制）

---

## 10. 延伸阅读

- [InstructGPT 论文](../papers/2022-03-04-instructgpt.md)
- [DPO 原理](dpo.md)
- [PPO 算法](../../reinforcement-learning/papers/2017-07-20-ppo.md)

---

*最后更新：2026-06-22*
