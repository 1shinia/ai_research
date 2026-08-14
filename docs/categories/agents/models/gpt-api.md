# GPT-4o / o1 (API)

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | GPT-4o / o1 (API) |
| **作者/团队** | OpenAI |
| **参数规模** | 闭源 API 服务，参数未公开 |
| **开源协议** | 闭源商业 API |
| **API 入口** | [OpenAI Platform](https://platform.openai.com) |
| **论文原文** | [2303.08774](https://arxiv.org/abs/2303.08774) (GPT-4) |

## 简介

OpenAI 提供的 GPT-4o（多模态全能）和 o1/o3（推理增强）API 服务。GPT-4o 支持文本/图像/音频多模态输入输出，o1 采用长链思维推论。作为 AI Agent 系统的后端大脑，是目前最广泛使用的闭源 LLM API。

## 核心亮点

- GPT-4o: 统一多模态 — 文本 / 图像 / 音频
- o1/o3: 推理增强，使用 CoT 链式思考
- Function Calling：为 LLM 挂载外部工具的基石
- Structured Outputs：确保输出符合 JSON Schema
- Assistants API：持久化线程 + 知识库 + 文件处理

## 使用方式

- **[API 调用]**: `client.chat.completions.create(model="gpt-4o", messages=[...])`
- **[Function Calling]**: 定义 `tools` 数组，模型自动选择调用
- **[Structured Outputs]**: `response_format={"type": "json_schema", ...}`
- **[Streaming]**: `stream=True` 实时打字机输出

## 评估结果

- MMLU: 88.7% (GPT-4o)
- HumanEval: 90.2% (GPT-4o)
- MATH: 91.4% (GPT-4o)
- Arena Elo: 领先其他模型

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 OpenAI 官方文档获取最新信息。*
