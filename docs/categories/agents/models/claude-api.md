# Claude 3.5 (API)

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Claude 3.5 (API) |
| **作者/团队** | Anthropic |
| **参数规模** | 闭源 API 服务，参数未公开 |
| **开源协议** | 闭源商业 API |
| **API 入口** | [Anthropic Console](https://console.anthropic.com) |
| **论文原文** | [2305.17965](https://arxiv.org/abs/2305.17965) (Constitutional AI) |

## 简介

Anthropic 提供的 Claude 3.5 系列 API。Sonnet 以顶级的编码能力著称（SWE-bench 49%），Haiku 性价比极高。支持 Tool Use / Computer Use / Extended Thinking，是 AI Agent 和安全对齐领域的标杆模型。

## 核心亮点

- Sonnet: 编码能力领先的商用模型
- Tool Use：函数调用支持复杂 Agent 工作流
- Computer Use：模型可直接操控计算机界面
- Extended Thinking：长链推理的可视化过程
- 200K 上下文窗口（Haiku）

## 使用方式

- **[SDK]**: `pip install anthropic`
- **[API]**: `client.messages.create(model="claude-sonnet-4-20250514", messages=[...])`
- **[Tool Use]**: 定义 tools 实现文件搜索 / 代码执行等
- **[Streaming]**: `stream=True` 实时流式输出

## 评估结果

- HumanEval: 93.7% (Sonnet)
- SWE-bench Verified: 49% (Sonnet)
- MMLU: 88.7% (Sonnet)
- GPQA: 68.3% (Sonnet)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 Anthropic 官方文档获取最新信息。*
