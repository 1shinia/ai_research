# 大语言模型 (LLM)

## 领域概览

大语言模型是当前 AI 研究最活跃的领域之一，涵盖了从基础架构到训练方法、推理优化、对齐技术等方方面面。

## 关键研究方向

- **架构演进**：Transformer → MoE → 长上下文优化
- **训练方法**：预训练、SFT、RLHF、DPO
- **推理优化**：量化、蒸馏、推测性解码
- **Scaling Law**：参数规模、数据规模、计算量的关系
- **对齐技术**：让模型行为符合人类意图


## 知识库

系统化的算法知识点整理：

- [Transformer 架构](knowledge/transformer-architecture.md)
- [自注意力机制](knowledge/self-attention.md)
- [位置编码](knowledge/positional-encoding.md)
- [MoE 混合专家](knowledge/moe.md)
- [Scaling Law](knowledge/scaling-law.md)
- [涌现能力](knowledge/emergent-abilities.md)
- [上下文学习](knowledge/in-context-learning.md)
- [思维链](knowledge/chain-of-thought.md)
- [RLHF 流水线](knowledge/rlhf-pipeline.md)
- [DPO 详解](knowledge/dpo.md)
- [RAG 详解](knowledge/rag.md)
- [预训练](knowledge/pretraining.md)
- [监督微调 (SFT)](knowledge/sft.md)
- [解码策略](knowledge/decoding-strategies.md)
- [上下文长度扩展](knowledge/context-extension.md)

共 **15** 个知识点


## 论文库

经典及前沿论文汇编：

- [Attention Is All You Need (2017)](papers/2017-06-12-attention-is-all-you-need.md) — Transformer 架构的奠基之作
- [Scaling Laws for Neural Language Models (2020)](papers/2020-01-23-scaling-laws.md) — 规模定律的系统研究
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (2020)](papers/2020-05-22-rag.md) — RAG 范式
- [Language Models are Few-Shot Learners (GPT-3, 2020)](papers/2020-05-28-gpt3.md) — 大规模语言模型与上下文学习
- [Switch Transformers (2022)](papers/2022-01-12-switch-transformer.md) — MoE 高效扩展
- [Chain-of-Thought Prompting Elicits Reasoning (2022)](papers/2022-01-28-chain-of-thought.md) — 思维链推理
- [Training Language Models to Follow Instructions (InstructGPT, 2022)](papers/2022-03-04-instructgpt.md) — 基于人类反馈的指令微调
- [Direct Preference Optimization (2023)](papers/2023-05-29-dpo.md) — 无需强化学习的偏好优化

共 **8** 篇论文

## 模型库

主流开源大模型：

- [Llama 3](models/llama3.md) — Meta 开源系列
- [Qwen 2.5](models/qwen2.5.md) — 阿里通义系列
- [DeepSeek](models/deepseek.md) — 深度求索系列
- [Mistral](models/mistral.md) — Mistral AI 系列

共 **4** 个模型

## 代码库

实用工具与框架：

- [Transformers](code/transformers.md) — HuggingFace 核心库
- [vLLM](code/vllm.md) — 高效推理引擎
- [Ollama](code/ollama.md) — 本地模型部署工具
- [LLaMA-Factory](code/llama-factory.md) — 微调框架

共 **4** 个工具

## 数据集库

大规模预训练数据集：

- [The Pile](datasets/the-pile.md) — 825GB 多样化文本语料
- [C4](datasets/c4.md) — Common Crawl 清洗版
- [RedPajama](datasets/redpajama.md) — 开源 LLaMA 训练数据复现
- [FineWeb](datasets/fineweb.md) — HuggingFace 高质量网络语料
- [Dolma](datasets/dolma.md) — 微软 3T token 开放语料
- [SlimPajama](datasets/slimpajama.md) — RedPajama 精炼版

共 **6** 个数据集

## 前沿趋势

详见 [趋势追踪](trends.md)
