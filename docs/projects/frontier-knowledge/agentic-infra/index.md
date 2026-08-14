# 🏭 Agentic Infra Platform — 总览

> **领域**：Agentic Infra / 推理优化 / Agent 安全 / 硬件平台
> **状态**：🟢 规划中 · **更新**：2026-08-07
> **定位**：企业级 Agent 基础设施平台（内部推动方向）

---

## 一句话

面向 ToB 客户的 **Agentic Infra Platform**：以 **Dynamo PD 分离推理优化 + 安全沙箱 Sandbox** 为核心能力，配合 **Vera Rubin 平台** 的年度落地策略，构建企业级 Agent 运行底座。

> 🗺️ **想看四组件如何协作成完整平台？** → [平台技术全貌](platform-overview.md)（架构图 / 请求旅程 / 软硬件对应 / 部署形态）

---

## 三大支柱

```
┌─────────────────────────────────────────────────────────────┐
│              Agentic Infra Platform                       │
├─────────────────┬───────────────────┬────────────────────────┤
│  ① 推理优化      │  ② Agent 安全      │  ③ 硬件平台             │
│  Dynamo         │  Sandbox           │  Vera CPU + Rubin GPU  │
│  PD 分离推理     │  Secure Workspace  │  HBM4 / NVLink6        │
│  多级 KV 缓存    │  运行时强制层       │  NVL72 机架形态         │
│  智能路由/扩缩   │  凭据代理/审计      │  2026 全面投产          │
└─────────────────┴───────────────────┴────────────────────────┘
```

| 支柱 | 核心文档 | 状态 |
|:-----|:---------|:-----|
| ① Dynamo 推理优化 | [→ Dynamo PD 分离](dynamo-pd-separation.md) | 🟢 已收录 |
| ①b Triton 推理服务 | [→ 多后端服务层](triton-inference-server.md)（Dynamo 前身） | 🟢 已收录 |
| ①c 网络层 CMX/BlueField | [→ KV 存储 + 安全卸载](network-layer.md)（800Gb/s + CMX） | 🟢 已收录 |
| ② Agent 安全沙箱 | [→ 安全沙箱](sandbox.md)（关联 [NVIDIA SAW](nvidia-secure-agent-workspace.md)） | 🟢 已收录 |
| ②b SAW 完整中文翻译 | [→ 12 章全译](nvidia-saw-translation.md)（实施细节） | 🟢 已收录 |
| 🤖 AI 算法工程师手册 | [→ 工作范围 + 技术栈详解](ai-engineer-playbook.md) | 🟢 已收录 |
| ③ Vera 硬件平台 | [→ Vera Rubin](vera-platform.md) | 🟢 已收录 |

---

## 为什么是这三个的组合

### Token 侧（推理）：Dynamo
- 大模型推理的 Token 成本与延迟是 ToB 客户的核心痛点
- PD 分离让 Prefill（算力型）和 Decode（带宽型）各跑各的硬件，利用率拉满
- 多级 KV 缓存省掉重复 Prefill，智能路由 + 自动扩缩控成本

### Agent 侧（安全）：Sandbox
- Agent 自主执行带来新风险面：提示注入、数据外泄、越权操作
- 安全沙箱把「凭提示词约束」升级为「凭环境约束」——策略由控制面签发、运行时强制、不可被 Agent 绕过
- ToB 客户（尤其金融/政务/医疗）没有这一点不会采购

### 底座（硬件）：Vera Rubin
- 2026 年 Vera Rubin 平台全面投产，官方定位就是 **"Opens Agentic AI Frontier"**
- NVL72 机架级形态 = 大规模 AI Factory 的物理载体
- 推理优化和安全能力必须落在具体硬件平台上，才构成可交付的 ToB 方案

---

## 🎯 产品化思路

```
Dynamo（推理） + Sandbox（安全） + Vera（硬件）
        ↓                    ↓                  ↓
   Token 成本/延迟        Agent 可信执行         AI Factory 底座
        └──────────────────┬───────────────────┘
                    企业级 Agent 运行平台
                （可交付、可运维、可审计、可扩展）
```

### 目标客户价值
- **降本**：PD 分离 + KV 缓存 → Token 成本下降
- **安全**：沙箱 + 审计 + 人工审查 → 敢让 Agent 干活
- **规模**：Vera NVL72 → 从试点到 AI Factory 规模化

---

## 📌 待办

- [ ] 深入调研 Dynamo 与现有推理栈（vLLM/SGLang/TensorRT-LLM）的集成路径
- [ ] 安全沙箱选型：NVIDIA OpenShell vs 自研 vs 第三方
- [ ] Vera Rubin 硬件预算与落地节奏评估
- [ ] 联合开发/合作机会评估（对外）
