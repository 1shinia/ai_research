# vLLM

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | vLLM |
| **语言** | Python / C++ |
| **用途** | LLM 推理加速引擎 |
| **GitHub** | [vllm-project/vllm](https://github.com/vllm-project/vllm) |
| **许可证** | Apache 2.0 |

## 简介

vLLM 是基于 PagedAttention 的高吞吐、低延迟 LLM 推理引擎。利用 PagedAttention 的显存管理将连续请求的批处理效率提升到极致。支持几乎所有主流开源 LLM 模型，是社区部署 LLM 的首选推理框架。

## 核心功能

- PagedAttention — 类操作系统的虚拟内存分页管理 KV Cache
- Continuous Batching — 动态批处理减少等待
- 支持 AWQ / GPTQ / FP8 量化推理
- OpenAI 兼容 API 接口
- 多 GPU / 张量并行推理

## 快速开始

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-7B-Instruct
```

## 使用场景

- 大规模 LLM API 服务部署
- 高并发推理场景（聊天 / 代码生成 / 文档分析）
- 多模型统一服务化

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
