# 本周重要模型发布

## 本周记录

各公司/团队新发布的模型、权重和 API。

| 日期 | 项目 | 发布方 | 类型 | 备注 |
|:----|:-----|:------|:----|:----|
| 06/25 | **Qwen-Image-Agent** | Alibaba (Qwen Team) | T2I模型 | Agent式图像生成，主动补全上下文 |
| 06/26 | **Qwen2-57B-A14B (FlexMoE优化)** | NUS / Qwen | MoE模型 | FlexMoE剪枝50%保留99.8%性能 |
| — | Llama-3.1/3.2系列 | Meta | 通用LLM | InfoKV和Block-GTQ的验证基座 |
| — | DeepSeek-R1-Distill-Qwen-7B | DeepSeek | 推理模型 | Block-GTQ在该模型上验证极低比特KV量化 |
| — | LLaVA-v1.6-Mistral-7B / Llama3-LLaVA-8B / Qwen3-VL-30B | 多家 | VLM | JSAE跨架构可解释干预验证的三个VLM |
| — | SD3.5 Large | Stability AI | T2I模型 | DiT-Reward用Flow-GRPO优化提升图像真实感 |
| — | LTX-2 (19B DiT) | — | 视频生成 | HyperQuant在该模型上验证无肉眼可见伪影 |

## 详情

### 🤖 Qwen-Image-Agent（阿里 Qwen Team）

- **arXiv**：[2606.26907](https://arxiv.org/abs/2606.26907)
- **类型**：Agent式文本到图像生成模型
- **核心创新**：将T2I从"用户提供完整提示词"转变为"Agent主动补全上下文"
- **组件**：上下文感知规划 + 上下文接地（推理/搜索/记忆/反馈）
- **配套基准**：IA-Bench（智能体图像生成评估）
- **意义**：代表了T2I从提示词工程到Agent式生成的范式转变

### 🧠 FlexMoE 优化版 Qwen2-57B-A14B

- **arXiv**：[2606.27866](https://arxiv.org/abs/2606.27866)
- **类型**：MoE压缩技术（可应用于任何MoE模型）
- **成果**：Qwen2-57B-A14B剪枝50%路由专家参数后保留~99.8%基础性能
- **亮点**：单次训练输出所有预算嵌套子网络，支持实时在线预算切换

### 📐 SD3.5 Large + DiT-Reward

- **arXiv**：[2606.23626](https://arxiv.org/abs/2606.23626)
- **创新**：用预训练DiT直接作为奖励模型，Flow-GRPO优化SD3.5 Large
- **成果**：HPDv2上85.6%，超越HPSv3

---

*每周更新 — 2026-06-29*
