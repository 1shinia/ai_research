# Ollama

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Ollama |
| **语言** | Go |
| **用途** | 本地 LLM 运行工具 |
| **GitHub** | [ollama/ollama](https://github.com/ollama/ollama) |
| **许可证** | MIT |

## 简介

Ollama 是一个简洁易用的本地 LLM 运行工具。通过一条命令即可下载并运行各种开源模型（LLaMA / Qwen / Mistral 等），自动处理模型下载、量化、上下文管理和 API 暴露。Mac/Windows/Linux 全平台支持。

## 核心功能

- 一键运行模型：`ollama run llama3.2`
- 模型自动下载和管理
- GGUF 量化格式支持
- OpenAI 兼容 API 接口
- Modelfile 自定义模型配置

## 快速开始

```bash
# 安装（macOS/Linux）
curl -fsSL https://ollama.com/install.sh | sh

# 运行模型
ollama run qwen2.5

# API 调用
curl http://localhost:11434/api/generate -d '{"model": "qwen2.5", "prompt": "Hello"}'
```

## 使用场景

- 个人电脑上的本地 AI 助手
- 开发和测试环境中的 LLM 服务
- 离线环境下的模型推理

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
