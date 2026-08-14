# 📚 本周 AI 论文速递 — 2026-07-20

> 本期覆盖 9 大领域，从 180 篇 arXiv 候选论文中精选 **37 篇高影响力论文**，每篇附中文完整摘要。

| 领域 | 精选篇数 | 亮点论文 |
|:----|:-------:|:--------|
| 🧠 [大语言模型](./llm) | 5 | ToolAlignBench、Agentic-DPO |
| 👁️ [计算机视觉](./vision) | 4 | ImprovedVBGS (1680×加速)、VideoChat3 |
| 🔗 [多模态](./multimodal) | 4 | AV-Flamingo、WSI 数据泄露审计 |
| 🤖 [智能体](./agents) | 4 | AI Agents Do Not Fail Alone、MCP 进化基准 |
| 🎨 [生成模型](./generative-models) | 3 | SpectraReward、MusicMark |
| 🎯 [强化学习](./reinforcement-learning) | 4 | BPO、CycleGRPO |
| ⚡ [高效训练](./efficient-training) | 4 | D-Cut、JoLT |
| 🦾 [机器人](./robotics) | 4 | Xiaomi-Robotics-1、VistaVLA |
| 🛡️ [AI 安全](./ai-safety) | 5 | Agent Hacks Agent、MJ、Protective Capacity Hallucination |

---

## 本期重点推荐 🔥

| # | 领域 | 论文 | 为什么值得关注 |
|:-:|:---:|:----|:-------------|
| 1 | 🛡️ AI 安全 | **Agent Hacks Agent** | 首个自动化红队框架，用 agent 攻 agent，发现跨模型可复用的漏洞知识 |
| 2 | 🛡️ AI 安全 | **MJ (Multi-turn Jailbreaking)** | DC-GRPO 多轮越狱攻击率达 **98.26%**，大幅超越 SOTA |
| 3 | 🦾 机器人 | **Xiaomi-Robotics-1** | 100K 小时真实轨迹训练的 VLA 基础模型，展示强 scaling 行为 |
| 4 | ⚡ 高效训练 | **D-Cut** | 批量推测解码中自适应剪枝，高并发下从 1.26× 提升至 **1.65×** 加速 |
| 5 | 🧠 大语言模型 | **ToolAlignBench** | 安全对齐导致工具调用 agent **43.4% 概率覆盖部署指令**，引发法律风险 |
| 6 | 👁️ 计算机视觉 | **ImprovedVBGS** | 实时变分贝叶斯高斯泼溅，**1680 倍**加速（84s → 0.05s/帧） |
| 7 | 🎨 生成模型 | **SpectraReward** | 无需训练的 MLLM 奖励模型，用 MLLM 给图像生成打分指导 RL |
| 8 | 🤖 智能体 | **AI Agents Do Not Fail Alone** | 首次量化"上下文质量"作为 agent 可靠性的领先指标 |
| 9 | 🎯 强化学习 | **BPO** | 分支策略优化：利用沙箱回滚实现高效的 agent 策略学习 |

---

> 📅 本周数据抓取自 arXiv，日期范围 2026-07-13 ~ 2026-07-20。各领域详情页包含每篇精选论文的完整中文摘要（一句话总结、核心思想、重要性分析、关键实验结果）。
