# 📚 ai-agent-book — 《深入理解 AI Agent：设计原理与工程实践》

> **来源**：https://github.com/bojieli/ai-agent-book
> **状态**：🟢 已收录 · **更新**：2026-08-07

## 项目档案

| 项目 | 信息 |
|:-----|:-----|
| ⭐ Stars | 32.9k |
| 🍴 Forks | 3.5k |
| 语言 / 许可证 | Python / Apache-2.0 |
| 作者 | 李博杰（前华为 AI 专家） |
| 阅读 | 在线版 bojieli.github.io / PDF / EPUB（13 种语言） |

---

## 一句话

围绕 **Agent = LLM + 上下文 + 工具** 这个核心公式，10 章从原理讲到工程实战，95 个配套实验全部开源。

---

## 10 章导读

| 章 | 主题 | 一句话核心 | 实验数 |
|:--|:-----|:----------|:------:|
| 1 | 🚀 Agent 基础知识 | Agent = LLM + 上下文 + 工具；Harness 工程才是竞争力 | 4 |
| 2 | 🎯 上下文工程 | 上下文决定能力上限：KV Cache、提示工程、Skills、压缩 | 9 |
| 3 | 📚 用户记忆和知识库 | 跨会话记忆、RAG、结构化索引、知识图谱 | 13 |
| 4 | 🛠️ 工具 | 工具是 Agent 的双手：MCP 协议、感知/执行/协作工具 | 7 |
| 5 | 💻 Coding Agent | 代码是「能创造新工具的工具」 | 12 |
| 6 | 🎯 Agent 评估 | 评估环境、指标、统计显著性、评估驱动选型 | 12 |
| 7 | 🧠 模型后训练 | 预训练/SFT/RL 三阶段、工具调用内化 | 16 |
| 8 | 🔄 持续进化 | 从运行轨迹获取学习信号、更新知识/指令/程序/参数 | 9 |
| 9 | 🎙️ 多模态与实时交互 | 语音三范式、Computer Use、机器人 | 10 |
| 10 | 🤝 多 Agent 协作 | 协作框架、上下文共享/隔离、「Agent 社会」 | 8 |

---

## 关键设计

### 核心公式

```
Agent = LLM + 上下文 + 工具
```

- **LLM**：推理引擎（预训练/SFT/RL）
- **上下文**：能力上限的决定因素（KV Cache、RAG、压缩、记忆）
- **工具**：行动的双手（MCP 协议为行业标准）

### 配套实验体系

- 95 个实验覆盖全部章节，支持 `uv sync` 一键安装（Python 3.10+）
- 附赠 22 个外部仓库固定 SHA 克隆脚本（SWE-bench、verl、MiniMind、OSWorld、GAIA 等），保证可复现
- 每个实验标注类型：✅ 可运行 / 📖 复现 / 🚧 设计

---

## 外部复现仓库（精选）

| 章节 | 仓库 | 用途 |
|:-----|:-----|:-----|
| 6 | SWE-bench / OSWorld / GAIA / terminal-bench | Agent 评测基准 |
| 7 | MiniMind / verl / AdaptThink / SFTvsRL | 后训练框架与配方 |
| 9 | claude-quickstarts / browser-use / XLeRobot | GUI 与机器人 |
| 10 | TalkAct / generative_agents | 双 Agent 架构、AI 小镇 |

---

## 📌 对「多智能体平台」项目的启示

- 第 2 章上下文工程：多 Agent 上下文共享/隔离的取舍
- 第 4 章 MCP：工具接入的行业标准协议
- 第 7 章后训练：何时 SFT、何时 RL（工具调用内化）
- 第 10 章多 Agent 协作：协作框架与「Agent 社会」涌现
