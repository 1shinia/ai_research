# LangChain

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | LangChain |
| **语言** | Python / TypeScript |
| **用途** | LLM 应用开发框架 |
| **GitHub** | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| **许可证** | MIT |

## 简介

LangChain 是最流行的 LLM 应用开发框架。提供构建 LLM 驱动的应用所需的全部基础设施：链式调用、Agent 循环、工具集成、RAG、记忆管理等。支持 OpenAI / Anthropic / 开源模型等多种后端。

## 核心功能

- **Agent 框架**: Agent Executor + Tool 调用循环
- **RAG**: 文档分割 / 向量库 / 检索器 / 生成器
- **Chain**: 可组合的 LLM 调用管道
- **Memory**: 对话历史管理
- **LangGraph**: 图驱动的 Agent 工作流

## 快速开始

```python
pip install langchain langchain-community

# Agent 示例
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search the web"""
    return f"Results for {query}"

agent = create_tool_calling_agent(llm, [search])
executor = AgentExecutor(agent=agent, tools=[search])
```

## 使用场景

- 构建 LLM Agent 应用
- 文档问答和知识库系统
- 多工具编排工作流

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
