# CrewAI

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | CrewAI |
| **语言** | Python |
| **用途** | 多 Agent 协作框架 |
| **GitHub** | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) |
| **许可证** | MIT |

## 简介

CrewAI 是一个多 Agent 协作框架，提供 "Role → Goal → Task" 的角色扮演式 Agent 编排。每个 Agent 扮演特定角色（研究员 / 写手 / 分析师等），通过任务委托和工作流实现复杂任务的协作完成。

## 核心功能

- **Role-based Agent**: 定义角色 / 目标 / 背景故事
- **Task Delegation**: Agent 之间任务分配和执行
- **Sequential / Hierarchical Process**: 流程编排
- **Tool 共享**: Agent 之间共享工具（搜索 / 计算 / 代码执行）
- **结果追踪**: 思考和执行的完整日志

## 快速开始

```python
pip install crewai

from crewai import Agent, Task, Crew

researcher = Agent(role="研究员", goal="搜集信息", backstory="...")
writer = Agent(role="写手", goal="撰写报告", backstory="...")

task = Task(description="研究 AI Agent 发展趋势", agent=researcher)
crew = Crew(agents=[researcher, writer], tasks=[task])
crew.kickoff()
```

## 使用场景

- 研究报告自动生成
- 多 Agent 协作完成复杂工作流
- 模拟团队协作场景

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
