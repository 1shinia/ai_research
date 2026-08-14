# 🤖 AI Agent

> 本周候选：20 篇 | 筛选高影响力：4 篇

---

## 1. GATS: Graph-Augmented Tree Search with Layered World Models for Efficient Agent Planning

**📄 arXiv：** [2607.08894](https://arxiv.org/abs/2607.08894v1) | **📅 发布日期：** 2026-07-09  
**👥 作者：** Maureese Williams, Dymitr Nowicki

### 一句话总结
提出图增强树搜索 + 分层世界模型，实现规划阶段**零 LLM 调用**——在 12 个挑战性场景中达到 100% 成功率，相比 LATS 的 88.9% 和 ReAct 的 23.9%。

### 核心思想
现有 Agent 规划方法（LATS、ReAct）每步推理都调用 LLM，计算开销高且结果随机。GATS 构建三层世界模型：L1 精确符号动作匹配、L2 执行日志统计学习、L3 LLM 预测未知动作——但只作为回退。规划过程使用 UCB1 树搜索在图结构的搜索空间中进行，**完全不依赖 LLM 推理**。结果不仅成功率更高，而且是确定性的（零方差）。

### 为什么重要
Agent 规划的高成本和不稳定性是落地的主要障碍。GATS 证明：**系统化的搜索 + 学到的世界模型可完全替代 LLM 引导的探索**，同时获得更好的一致性和 100% 成功率。这对降低 Agent 系统的推理成本和提升可靠性有直接意义。

### 关键实验
- 合成规划任务：GATS 100% vs LATS 92% vs ReAct 64%
- 12 个复杂场景压力测试：GATS 100% vs LATS 88.9% vs ReAct 23.9%
- 每任务零 LLM 调用（vs LATS 每任务 37 次调用）
- 零方差确定性输出

---

## 2. ToolFailBench: A Comprehensive Benchmark for Investigating Tool-Use Failures in LLM Agents

**📄 arXiv：** [2607.08220](https://arxiv.org/abs/2607.08220v1) | **📅 发布日期：** 2026-07-09  
**👥 作者：** Weiran Lin, Sicheng Song, Yuan Cui, Yunqi Zhang, Jiangang Zhu

### 一句话总结
首个系统化工具使用失败基准，标注 56 种真实失败类型，揭示调用级错误比参数级错误更隐蔽且更难修复。

### 核心思想
LLM Agent 的工具使用能力涨点迅速，但失败模式是什么、发生在哪里、为什么发生——这些问题缺乏系统数据。ToolFailBench 构建了覆盖 8 个真实工具的 750 个任务-工具对，标注了 56 种细粒度失败类型。发现关键模式：调用级错误（如错误排序、遗漏必要工具）比参数级错误（如错误参数值）更隐蔽、跨任务泛化性更差，且现有方法对调用级错误的修复效果有限。

### 为什么重要
Agent 工具使用的可靠性是 Agent 落地的核心瓶颈。该工作首次提供了**带有细粒度标注的系统化失败数据**，让社区不仅知道「准确率多少」，还知道「哪里错了、为什么错」。类间混淆矩阵揭示了以往被准确率掩盖的隐蔽失败模式。

### 关键实验
- 750 个任务-工具对，56 种失败类型
- 调用级 vs 参数级失败的跨任务泛化分析
- 类间混淆矩阵揭示隐蔽失败模式

---

## 3. Agent Data Injection Attacks: New Vulnerabilities in LLM Agent Memory

**📄 arXiv：** [2607.05328](https://arxiv.org/abs/2607.05328v1) | **📅 发布日期：** 2026-07-06  
**👥 作者：** Ruixuan Huang, H.J.T. Mookerjee, Khang Nhat Hoang Vo, Timothy Baldwin

### 一句话总结
发现并系统研究 Agent 数据注入攻击——攻击者通过操纵 Agent 记忆中的已有记忆项来间接控制 Agent 的未来行为，无需直接修改 Agent 的提示或工具。

### 核心思想
Agent 的记忆系统允许跨任务持久化上下文。现有攻击聚焦于提示注入或工具操纵，但忽略了记忆本身是攻击面——如果攻击者能在对话中植入一个包含恶意内容的记忆项，此后该 Agent 在处理无关任务时也可能受该记忆影响。论文形式化了这一威胁模型，实现两种注入策略，并发现现有安全措施（如输出过滤、权限限制）无法有效防御。

### 为什么重要
随着记忆功能成为 Agent 的标配（MCP、Mem0、LangGraph Memory），记忆安全性将成为新的关键问题。该工作首次系统性地将记忆注入识别为一类**独立的新攻击面**，对 Agent 安全架构设计有重要启发。

### 关键实验
- 形式化 Agent 数据注入威胁模型
- 两种注入策略的实现与评估
- 现有防御措施对该攻击的失效分析

---

## 4. WebSwarm: Recursive Multi-Agent Orchestration for Deep-and-Wide Web Search

**📄 arXiv：** [2607.08662](https://arxiv.org/abs/2607.08662v1) | **📅 发布日期：** 2026-07-09  
**👥 作者：** Xiaoshuai Song, Liancheng Zhang, Kangzhi Zhao, Yutao Zhu, Zhongyuan Wang

### 一句话总结
提出渐进递归多 Agent 搜索框架，通过动态子节点委托、搜索模式自选择和过程级经验复用，在深度+广度搜索任务上全面超越单 Agent 和多 Agent 基线。

### 核心思想
单 ReAct Agent 受限于单条轨迹和有限上下文，无法同时处理深（递归探索）和广（覆盖全面）。WebSwarm 构建递归委托树：每个搜索节点携带本地目标和搜索模式（explore/expand/aggregate），可自决是否委托子节点。解决后向上回传证据，父节点再基于已有结果进一步扩展。引入先导探测（probe）了解目标信息在网页上的组织形式，以及同级节点的过程经验复用。

### 为什么重要
复杂信息搜索（如研究报告、竞品分析、科技追踪）是 Agent 最有价值的应用场景之一。WebSwarm 在 BrowseComp-Plus、DeepWideSearch 等深度+广度任务上全面领先，证明**递归多 Agent 架构**在复杂信息检索上相比单 Agent 有质的优势。

### 关键实验
- BrowseComp-Plus、WideSearch、DeepWideSearch、GISA 四个基准
- 全面超越单 Agent 和多 Agent 基线
- 先导探测和同级经验复用的消融实验有效

---

> ⏳ 暂存于 weekly-update/，等待主人手动选择后归档到 papers/ 对应分支。
