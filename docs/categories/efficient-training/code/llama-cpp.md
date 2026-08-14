# llama.cpp

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | llama.cpp |
| **语言** | C++ |
| **用途** | LLM 量化推理引擎 |
| **GitHub** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) |
| **许可证** | MIT |

## 简介

llama.cpp 是 GGUF 格式 LLM 的高效 C++ 推理引擎。通过 4-bit / 5-bit / 6-bit / 8-bit 量化在 CPU / GPU 上高效运行 LLM。使用 GGML 张量库，支持 Apple Silicon (Metal) / CUDA / Vulkan / OpenBLAS 后端。

## 核心功能

- 纯 C++ 实现，无外部依赖
- 支持 2-8 bit 多种量化级别
- CPU + GPU 混合推理
- Apple Silicon Metal 原生加速
- 内置 HTTPS API 服务器

## 快速开始

```bash
# 编译
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp && make

# 下载模型并运行
wget https://huggingface.co/.../qwen2.5-7b-instruct-q4_k_m.gguf
./llama-cli -m qwen2.5-7b-instruct-q4_k_m.gguf -p "Hello" -n 256

# API 服务器
./llama-server -m model.gguf --port 8080
```

## 使用场景

- 本地 LLM 部署（尤其 CPU / Apple Silicon）
- 模型量化测试
- 边缘设备 AI 推理

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
