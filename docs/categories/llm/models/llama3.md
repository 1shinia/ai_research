# LLaMA 3

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | LLaMA 3 |
| **作者/团队** | Meta |
| **参数规模** | 8B / 70B / 405B |
| **开源协议** | LLaMA 3 Community License |
| **模型权重** | [HuggingFace](https://huggingface.co/meta-llama/Meta-Llama-3-8B) |
| **ModelScope** | [LLM-Research/Meta-Llama-3-8B](https://modelscope.cn/models/LLM-Research/Meta-Llama-3-8B) |
| **论文原文** | [2407.21783](https://arxiv.org/abs/2407.21783) |

## 简介

Meta 发布的第三代开源大语言模型。405B 版本在多项基准测试中达到 GPT-4 级别性能，8B 和 70B 版本以极佳的性价比成为开源社区最流行的基座模型之一。采用分组查询注意力 (GQA)、MoE 等先进架构，训练数据达 15T tokens。

## 核心亮点

- 分组查询注意力 (GQA) 提升推理效率
- 405B 支持 128K 长上下文（8K 默认）
- 使用 RLHF + DPO 多阶段对齐训练
- 社区生态极完善，几乎所有框架都优先支持
- Llama 3.1 版本引入 128K 上下文拓展

## 使用方式

- **[HuggingFace Transformers]**: `from transformers import AutoModelForCausalLM; model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")`
- **[Ollama]**: `ollama run llama3.1`
- **[vLLM]**: `python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3-8B-Instruct`
- **[llama.cpp]**: `./llama-cli -m llama-3.1-8b-instruct.Q4_K_M.gguf -p "Hello"`

## 评估结果

- MMLU: 86.1% (405B)
- HumanEval: 89.0% (405B)
- GSM8K: 95.1% (405B)
- MATH: 73.8% (405B)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
