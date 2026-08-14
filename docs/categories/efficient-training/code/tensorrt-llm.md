# TensorRT-LLM

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | TensorRT-LLM |
| **语言** | Python / C++ |
| **用途** | NVIDIA GPU 推理优化 |
| **GitHub** | [NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) |
| **许可证** | Apache 2.0 |

## 简介

NVIDIA TensorRT-LLM 是 NVIDIA GPU 上最快的 LLM 推理引擎。通过图优化、层融合、内核自动调优和内存优化实现极致性能。支持 FP8 / INT4 AWQ / INT4 GPTQ / INT8 等多精度推理。

## 核心功能

- 计算图优化和层融合
- FP8 / INT4 / INT8 量化推理
- In-flight Batching (连续批处理)
- Paged KV Cache (类似 PagedAttention)
- 多节点多 GPU 张量+流水线并行

## 快速开始

```bash
pip install tensorrt_llm

# 构建引擎
trtllm-build --checkpoint_dir ./ckpt --output_dir ./engine   --gemm_plugin auto --max_batch_size 16

# 运行服务器
python run.py --engine_dir ./engine
```

## 使用场景

- 生产级 LLM 服务优化
- 高吞吐量推理需求
- NVIDIA GPU 集群部署

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
