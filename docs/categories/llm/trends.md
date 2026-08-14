# LLM 趋势追踪

记录大语言模型领域的前沿方向和演进脉络。

## 2026 年趋势

### 🚀 推理增强模型
- **o1/o3 范式普及**: 长链思维 (Long CoT) + 强化学习成为主流，各大厂商纷纷推出推理增强模型
- **DeepSeek-R1 开源冲击**: 开源推理模型首次达到闭源前沿水平，推动社区复现和优化
- **推理成本快速下降**: 推理从"昂贵特供"变为"日用标配"，API 价格持续走低

### 🏗️ MoE 架构全面开花
- DeepSeek V3 / Qwen-MoE / Mixtral 验证了 MoE 在大规模训练中的经济和效率优势
- 训练时 MoE + 推理时 KV Cache 优化的硬件感知设计成为新方向
- MoE 的推理引擎优化（SGLang / vLLM）飞速发展

### 📏 超长上下文竞赛
- 上下文窗口从 128K → 1M → 10M 级别快速扩展
- Ring Attention / YaRN / NTK-aware 等技术成熟
- 长上下文评估标准正在建立（RULER / Needle in a Haystack v2）

### 🔧 Agentic LLM
- LLM 从纯对话式向工具使用 + 代码执行 + 自主规划转变
- MCP (Model Context Protocol) 标准化工具接口
- 模型原生支持 Function Calling 成为标配而非特性

## 2025 年回顾

- **DeepSeek-V3 发布**: 671B MoE 模型以极低训练成本达到 GPT-4o 级别性能
- **推理模型元年**: OpenAI o1 / o3、DeepSeek-R1、Qwen-QwQ 等推理增强模型诞生
- **开源接近闭源**: Qwen2.5-72B / LLaMA 3.1-405B 等在多项基准逼近 GPT-4
- **Agent 框架成熟**: LangGraph / CrewAI / AutoGPT 生态逐步标准化

## 关键节点

| 时间 | 事件 |
|------|------|
| 2024.12 | DeepSeek-V3 发布，MoE 低成本训练范式确立 |
| 2025.01 | DeepSeek-R1 开源推理模型，超越 OpenAI o1 |
| 2025.05 | Qwen3 系列发布，原生 Agentic LLM 能力 |
| 2025.07 | LLaMA 4 发布，开源模型新里程碑 |
| 2025.12 | Claude 4 / GPT-5 相继发布，推理能力再升级 |

## 前沿方向

- **推理时扩展 (Inference-Time Scaling)**: 用更多推理计算换取更好质量
- **测试时训练 (Test-Time Training)**: 推理时进行参数自适应调整
- **超长上下文应用**: 代码仓库级理解 / 整书级写作 / 多文档分析
- **LLM 与数据库融合**: 数据库内置向量 + 全文检索 + LLM 推理

---

*此页面由 AI Research Tracker 自动维护，每月更新。*
