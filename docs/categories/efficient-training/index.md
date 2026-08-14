# 高效训练与推理 (Efficient Training & Inference)

## 领域概览

随着模型规模不断增大，如何高效地训练和部署大模型成为核心挑战。本领域涵盖从算法优化到系统工程的全面方案。

## 关键研究方向

- **注意力优化**：FlashAttention、Sparse Attention、Linear Attention
- **架构效率**：MoE、SSM (Mamba)、RWKV
- **推理加速**：量化 (GPTQ/AWQ/GGUF)、推测性解码、PagedAttention
- **训练优化**：混合精度、ZeRO、DeepSpeed、梯度检查点
- **上下文扩展**：RoPE 扩展、ALiBi、长上下文微调
- **部署框架**：vLLM、TensorRT-LLM、llama.cpp

## 里程碑论文

详见 [论文库](papers/) 目录


## 知识库

系统化的算法知识点整理：

- [LoRA 低秩适配](knowledge/lora.md)
- [量化技术](knowledge/quantization.md)
- [FlashAttention 详解](knowledge/flash-attention-detailed.md)
- [KV Cache](knowledge/kv-cache.md)
- [推测性解码](knowledge/speculative-decoding.md)
- [PagedAttention](knowledge/paged-attention.md)
- [状态空间模型 (Mamba)](knowledge/ssm-mamba.md)

共 **7** 个知识点

## 前沿趋势

详见 [趋势追踪](trends.md)
