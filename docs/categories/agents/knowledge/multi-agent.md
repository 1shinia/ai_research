# 多 Agent 协作

## 1. 概述

多个 Agent 协作完成复杂任务，每个 Agent 有特定的角色和能力。

## 2. 协作模式

### 2.1 流水线模式

Agent 按顺序处理任务：

    Agent A (分析) -> Agent B (执行) -> Agent C (验证)

### 2.2 并行模式

多个 Agent 同时处理不同子任务：

    Agent A (搜索) ---|
    Agent B (计算) ---|-> Agent D (整合)
    Agent C (绘图) ---|

### 2.3 辩论模式

多个 Agent 提出不同观点，通过辩论达成共识：

    Agent A: 观点 1
    Agent B: 观点 2
    Agent A: 反驳
    Agent B: 修正
    -> 达成共识

## 3. 通信协议

### 3.1 共享黑板

所有 Agent 共享一个中央存储，读写信息。

### 3.2 消息传递

Agent 之间直接发送消息。

    Agent A -> Agent B: "我找到了相关信息"

### 3.3 层级结构

有管理者 Agent 协调其他 Agent。

    Manager Agent
    ├── Worker A
    ├── Worker B
    └── Worker C

## 4. 典型框架

| 框架 | 特点 |
|------|------|
| AutoGen | 微软，灵活的 Agent 对话 |
| CrewAI | 角色分工，任务编排 |
| LangGraph | 状态图，复杂流程 |
| MetaGPT | 软件开发多 Agent |

## 5. 延伸阅读

- [ReAct 论文](../papers/2022-10-06-react.md)

---

*最后更新：2026-06-22*
