# 规划与推理

## 1. 概述

Agent 的核心能力是将复杂任务分解为可执行的子任务，并推理如何完成。

## 2. 推理方法

### 2.1 Chain-of-Thought (CoT)

逐步推理，每一步显式写出思考过程。

    Q: 23 + 47 = ?
    A: 首先计算个位：3 + 7 = 10，进位 1。然后计算十位：2 + 4 + 1 = 7。答案是 70。

### 2.2 Tree-of-Thought (ToT)

探索多条推理路径，用搜索算法找到最优解。

### 2.3 Self-Consistency

多条推理路径投票，选择最一致的答案。

## 3. 规划方法

### 3.1 任务分解

将复杂任务分解为子任务：

    "写一篇关于 AI 的论文"
    -> "查找 AI 相关文献"
    -> "确定论文结构"
    -> "撰写引言"
    -> "撰写方法"
    -> ...

### 3.2 ReAct 框架

交替推理和行动：

    Thought: 我需要查找最新的 AI 论文
    Action: search("AI papers 2026")
    Observation: 找到了 3 篇相关论文...
    Thought: 第一篇看起来最相关
    Action: read_paper("paper_1.pdf")
    Observation: 这篇论文提出了...
    Thought: 我可以引用这篇论文的结论
    Action: add_reference("paper_1")

### 3.3 Plan-and-Execute

先制定完整计划，再逐步执行：

    Plan:
    1. 搜索相关论文
    2. 阅读摘要
    3. 提取关键信息
    4. 生成报告

## 4. 评估

| 指标 | 说明 |
|------|------|
| 任务成功率 | 完成目标的比例 |
| 步骤效率 | 完成任务所需步数 |
| 推理正确率 | 中间推理的正确性 |

## 5. 延伸阅读

- [ReAct 论文](../papers/2022-10-06-react.md)
- [思维链](../../llm/knowledge/chain-of-thought.md)

---

*最后更新：2026-06-22*
