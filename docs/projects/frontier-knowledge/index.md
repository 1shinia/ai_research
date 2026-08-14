# 🌐 前沿知识库 · AI Agent

> **状态**：🟢 建设中 · **更新**：2026-08-07
>
> 本库聚焦 **AI Agent / Harness 工程** 方向，收录高质量开源资源，沉淀为可检索、可复用的结构化知识。

---

## 🎯 定位

将前沿开源项目、论文、实践心得，沉淀为结构化知识，支撑各研究项目（多智能体平台、智能路由系统等）决策。

```
开源项目/论文 → 提炼要点 → 沉淀为知识条目 → 支撑研究项目
```

---

## 📦 已收录资源

### 🤖 Harness 工程（从 0 到 1 手写 Agent 框架）

**learn-claude-code** — 「Bash is all you need」
> ⭐ 73.3k · Python/MIT · 20 课渐进式教程

核心观点：**Agency（自主性）来自模型训练，不来自代码编排。** 模型是司机，Harness 是车。
→ [项目详解 →](learn-claude-code/index.md)

### 📚 Agent 系统理论（设计原理与工程实践）

**ai-agent-book** — 《深入理解 AI Agent：设计原理与工程实践》
> ⭐ 32.9k · Python/Apache-2.0 · 10 章 + 95 实验

核心公式：**Agent = LLM + 上下文 + 工具**，Harness 工程才是竞争力。
→ [项目详解 →](ai-agent-book/index.md)

### ⚡ 大模型部署方案（推理架构）

**PD 分离（Prefill-Decode Disaggregation）**
> 按推理阶段拆：Prefill 计算密集、Decode 带宽密集，分开部署各拉满资源利用率。
→ [详解 →](pd-separation.md)

**AF 分离（Attention-FFN Disaggregation）**
> 按算子类型拆：Attention 受 KV Cache 支配、FFN 权重密集，物理分离做细粒度资源调配。
→ [详解 →](af-separation.md)

### 🛡️ 企业级 Agent 安全（部署架构）

**NVIDIA Secure Agent Workspace 参考架构**
> 给自主运行的 Agent 一个受治理的执行场所：端点只展示不执行，身份/网络/凭据/策略/审计/人工审查共同约束 Agent。
→ [详解 →](agentic-infra/nvidia-secure-agent-workspace.md)

### 🏭 Agentic Infra Platform（内部推动方向）

**平台总览** — Dynamo 推理优化 + 安全沙箱 + Vera 硬件平台三大支柱
→ [总览 →](agentic-infra/index.md)

| 子条目 | 一句话 |
|:-------|:-------|
| [Dynamo PD 分离推理优化 →](agentic-infra/dynamo-pd-separation.md) | 开源推理框架，PD 分离 + KV 缓存 + 智能路由（腾讯云/阿里云已落地） |
| [安全沙箱 Sandbox →](agentic-infra/sandbox.md) | 运行时强制层，让 Agent 行为受环境约束而非提示词约束 |
| [Vera Rubin 平台 →](agentic-infra/vera-platform.md) | 2026 全面投产，官方定位 Agentic AI 的下一代底座 |

---

## 🆚 两者关系

| 维度 | learn-claude-code | ai-agent-book |
|:-----|:------------------|:--------------|
| 形式 | 20 课渐进式教程（每课可运行代码） | 10 章系统性著作 + 95 实验 |
| 侧重 | 手把手实现一个 Harness（造车） | 原理 + 工程全景（理论体系） |
| 互补 | 代码实现细节 | 上下文工程、后训练、评估、多 Agent |

---

## 📌 待办

- [ ] 精读 20 课，提炼每课核心机制
- [ ] 精读 10 章，整理章节导读与关键结论
- [ ] 与「多智能体平台」项目关联，输出可落地的架构建议
