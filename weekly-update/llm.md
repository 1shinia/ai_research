# 🧠 大语言模型 (LLM)

> 本周候选：20 篇 | 筛选高影响力：5 篇

---

## 1. LLM-as-a-Verifier: A General-Purpose Verification Framework

**📄 arXiv：** [2607.05391](https://arxiv.org/abs/2607.05391v2) | **📅 发布日期：** 2026-07-06  
**👥 作者：** Jacky Kwok, Shulu Li, Pranav Atreya, Yuejiang Liu, Yixing Jiang

### 一句话总结
将「验证（Verification）」确立为与预训练、后训练、推理时扩展并列的第四种 LLM 能力缩放轴，通过概率化连续评分实现通用验证框架，在 SWE-Bench、Terminal-Bench 等四个基准上达到 SOTA。

### 核心思想
标准 LLM Judge 让模型输出离散评分，但离散化损失了大量信息。本文提出对**评分 token 的 logits 分布取期望**，得到连续分数——这使得验证可以沿三个维度缩放：评分粒度（从整体评分到分步评分）、重复评估（多次采样降方差）、标准分解（按不同标准分别评分再综合）。框架不依赖任何额外训练，即插即用。

### 为什么重要
这是第一篇系统提出「验证即缩放轴」的工作。预训练爬不动了、后训练越做越贵、测试时扩展已到瓶颈——验证是尚未被充分开发的维度。在 SWE-Bench Verified 上达到 78.2%、Terminal-Bench V2 86.5%，且验证信号可直接作为 RL 训练的稠密奖励（改进 SAC 和 GRPO 的样本效率）。

### 关键实验
- 连续评分 vs 离散评分：前者在 solution 正确/错误间的区分度显著更高
- 三个缩放维度各自独立带来增益，组合效果最佳
- SWE-Bench Verified 78.2%、Terminal-Bench V2 86.5%、RoboRewardBench 87.4%、MedAgentBench 73.3%
- 验证信号作为 RL 奖励函数时，GRPO 在数学推理任务上收敛更快

---

## 2. Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents

**📄 arXiv：** [2607.05775](https://arxiv.org/abs/2607.05775v1) | **📅 发布日期：** 2026-07-07  
**👥 作者：** Wael Albayaydh, Rui Zhao, Ivan Flechais

### 一句话总结
整合 27 篇 Agent 评测论文（2023-2026）、19 个独立基准，建立统一的 LLM Agent 能力缺陷分类法，揭示失败随任务长度非线性累积等跨文献规律。

### 核心思想
各种 Agent 基准报告的涨点数字背后，隐藏着大量在不同评测中反复出现的**共有失败模式**。论文将来自工具使用、规划、长程推理、多 Agent 协作、安全、评测有效性等六大维度的独立发现归纳为一个统一分类法。发现：失败随任务长度非线性累积，单个子任务的强性能不保证端到端成功，增加 scaffolding 不持续提升可靠性。

### 为什么重要
Agent 领域论文爆炸式增长，每篇都报告自己的涨点，但缺乏系统性反思。该工作是**首个跨文献综合**，让社区看清哪些问题真解决了、哪些假解决了、哪些根本没解决。对 Agent 研究方向的指导价值极高。

### 关键实验
- 6 大失败簇、27 篇论文的交叉编码
- 发现失败在长程任务中非线性放大
- 单轮工具使用和短程网页导航已取得实质进展，但多步推理和协作仍有显著问题

---

## 3. PolyWorkBench: Benchmarking Multilingual Long-Horizon LLM Agents

**📄 arXiv：** [2607.06008](https://arxiv.org/abs/2607.06008v2) | **📅 发布日期：** 2026-07-07  
**👥 作者：** Hongliang Li, Yijin Liu, Zhiwei Zhang, Zihe Liu, Xinyue Lou

### 一句话总结
首个系统评估多语言环境下 LLM Agent 长程任务能力的基准，67 个任务覆盖商务、知识工作、法律、本地化、制造五个领域，揭示多语言带来的复合性能退化。

### 核心思想
现有 Agent 基准几乎全是单语言设定。但真实场景中，一个 Agent 可能需要读中文邮件、查英文知识库、用法语生成输出。论文设计 67 个跨语言工作流任务，引入混合评估框架（结构评分 + 可执行验证 + LLM 语义评估），发现 SOTA Agent 在多语言设定下性能显著下降，且多语言对推理和执行步骤产生**复合影响**。

### 为什么重要
多语言 Agent 是实际部署的刚需场景，但一直缺乏系统评估。该基准填补了这一空白，并且揭示了一个关键发现：语言变化不仅影响文本处理，还**级联影响整个推理和执行链路**，这对构建全球化 Agent 系统有直接指导价值。

### 关键实验
- 67 个任务、5 个领域、混合评估框架
- SOTA Agent 在多语言 vs 单语言环境下性能对比
- 多语言导致推理和执行步骤的复合退化分析

---

## 4. STAPO: Selective Trajectory-Aware Policy Optimization for LLM Agent Training

**📄 arXiv：** [2607.09355](https://arxiv.org/abs/2607.09355v1) | **📅 发布日期：** 2026-07-10  
**👥 作者：** （待从 arXiv 确认）

### 一句话总结
提出面向 LLM Agent 的选择性轨迹感知策略优化算法，解决 Agent 多步决策中稀疏奖励和信用分配的核心挑战。

### 核心思想
LLM Agent 训练面临特有的 RL 挑战：动作空间巨大（自然语言）、奖励极度稀疏（只有最终任务完成/失败）、信用分配困难（哪一步导致了失败？）。STAPO 引入**轨迹选择性加权**机制，根据每步动作对最终结果的贡献程度动态调整更新权重，结合 advantage-based replay buffer 优先采样关键转换片段。

### 为什么重要
现有的 RLHF/GRPO 方法主要针对单个响应优化，无法有效处理 Agent 的多步交互序列。STAPO 是专门为 Agent 训练设计的策略优化方法，对提升 Agent 在长程任务中的成功率和样本效率有直接帮助。

### 关键实验
- 在多种 Agent 任务中对比 PPO/GRPO 基线
- 轨迹选择性加权 vs 均匀加权的效果差异
- 信用分配效率分析

---

## 5. Reasoning Consistency Scanning: A Framework for Auditing Chain-of-Thought Validity in AI Safety Evaluations

**📄 arXiv：** [2607.07229](https://arxiv.org/abs/2607.07229v1) | **📅 发布日期：** 2026-07-08  
**👥 作者：** Silvia Santano

### 一句话总结
提出「推理一致性扫描」方法，无需干预即可从评估转录中检测 CoT 与答案之间的逻辑不一致，填补 AI 安全评估中可审计性的工具空白。

### 核心思想
现有 CoT 忠实性检测需要主动干预（如修改输入观察输出变化），无法在事后评估转录上进行。本文转向一个更易处理的问题：CoT 与最终答案之间是否存在**逻辑一致性**（不要求忠实于真实推理过程，只要求自洽）。定义了六种不一致子类型，构建了 60 条验证基准，并实现首个面向安全评估转录的一致性扫描器。

### 为什么重要
AI 安全评估的核心需求之一是**可审计**。如果模型的 CoT 自相矛盾，我们为什么要相信它的最终输出？该工作提供了首个可复用的事后一致性检测工具，对安全评估流程标准化有直接贡献。

### 关键实验
- 6 种不一致子类型的分类体系
- 60 条人工标注基准（基于 InstrumentalEval 输出构建）
- 4 种 generator 模型、3 种安全评估下的不一致率扫描
- 不一致性在不同模型和任务类型间系统变化

---

> ⏳ 暂存于 weekly-update/，等待主人手动选择后归档到 papers/ 对应分支。
