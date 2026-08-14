# 🗺️ Agentic Infra Platform — 技术全貌

> **定位**：Dynamo + Triton + Vera Rubin + SAW 四组件如何协作，构成完整的企业级 Agent 运行平台
> **状态**：🟢 已收录 · **更新**：2026-08-10
> **相关**：[Dynamo](dynamo-pd-separation.md) · [Triton](triton-inference-server.md) · [Vera Rubin](vera-platform.md) · [SAW](nvidia-secure-agent-workspace.md) · [SAW 完整翻译](nvidia-saw-translation.md) · [AI 算法工程师手册](ai-engineer-playbook.md)

---

## 一、全景架构图（五层）

```
┌──────────────────────────────────────────────────────────────────────┐
│ ① 应用层  ToB 客户场景                                                  │
│    金融合规 · 政务办公 · 医疗文书 · 制造运维 · 知识办公                     │
├──────────────────────────────────────────────────────────────────────┤
│ ② Agent 层  智能体运行                                                    │
│    Agent 循环（NemoClaw）→ 蓝图工作流 → 工具调用 → 产出暂存 → 人工审查        │
│    ┌─────────────────────────────────────────────────────────┐        │
│    │  OpenShell 运行时沙箱（Agent 执行边界，runtime-bounded）   │        │
│    └─────────────────────────────────────────────────────────┘        │
├──────────────────────────────────────────────────────────────────────┤
│ ③ 安全层  SAW（Secure Agent Workspace）                                 │
│    可信访问代理 · 凭据代理 · 四身份链 · 签名策略 · OCSF 审计 · 人工审查门      │
├──────────────────────────────────────────────────────────────────────┤
│ ④ 推理层  模型服务                                                     │
│    ┌──────────────┐         ┌──────────────────────────────┐         │
│    │ Triton        │         │ Dynamo                        │         │
│    │ 小模型服务     │  路由   │ PD 分离 · KV 缓存 · 智能路由   │         │
│    │ embedding/分类│ ──────► │ 自动扩缩 · 长上下文 Agent 推理 │         │
│    │ rerank/多后端 │ 推理    │                               │         │
│    └──────────────┘         └──────────────────────────────┘         │
├──────────────────────────────────────────────────────────────────────┤
│ ⑤ 硬件层  Vera Rubin 平台                                               │
│    Vera CPU（调度/路由/沙箱控制面） + Rubin GPU（推理/HBM4/KV Cache）      │
│    NVLink 6 高速互联 · ConnectX-9/BlueField-4 网络 · NVL72 机架形态       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 二、四大组件定位（一句话）

| 组件 | 角色 | 一句话 |
|:-----|:-----|:-------|
| **Triton** | 推理地基 | 多后端统一推理服务，小模型/传统模型承载 |
| **Dynamo** | 推理中枢 | LLM 推理编排：PD 分离、KV 缓存、智能路由、自动扩缩 |
| **Vera Rubin** | 硬件底座 | 2026 AI Factory 平台：Vera CPU + Rubin GPU + NVL72 |
| **SAW** | 安全骨架 | Agent 受治理执行场所：凭据代理、沙箱、审计、人工审查 |
| **网络层**（ConnectX-9 / BlueField-4 / CMX） | 血管系统 | 800Gb/s 互联 + KV Cache 网络存储（CMX）+ 安全硬件化 |

> 一句话记忆：**Triton 端盘子，Dynamo 炒菜，Vera Rubin 是厨房，SAW 是门禁+监控，BlueField 是储物柜（CMX 存 KV Cache）。**

---

## 三、组件协作关系（谁依赖谁）

```
                    ┌──────────────────────────┐
                    │    SAW 安全控制面（运维持有）  │
                    │  签名策略/审计/人工审查/凭据代理│
                    └──────┬─────────┬─────────┘
                           │ 约束     │ 约束
                 ┌─────────▼──┐   ┌──▼───────────┐
                 │ ② Agent 层  │   │ ① 推理调用     │
                 │ (OpenShell  │   │ (能力而非密钥)  │
                 │  沙箱内)    │   └──┬───────────┘
                 └─────────┬──┘      │
                           │ 工具调用 │ 模型请求
                 ┌─────────▼──┐   ┌──▼───────────┐
                 │ 企业系统     │   │ ④ 推理层       │
                 │ Git/工单/文档│   │ Triton → Dynamo│
                 └────────────┘   └──┬───────────┘
                                     │ 跑在
                              ┌──────▼──────┐
                              │ ⑤ Vera Rubin │
                              │ CPU+GPU+NVL72│
                              └─────────────┘
```

### 关键协作点

| 协作 | 说明 |
|:-----|:-----|
| **SAW → Agent** | 沙箱边界 + 签名策略约束 Agent 行为；凭据代理让 Agent 拿「能力」不拿「密钥」 |
| **Agent → 推理层** | 模型请求走**路由推理**（模型端点是 SAW 九类受管服务之一），经凭据代理鉴权 |
| **Triton → Dynamo** | 分层：Triton 管小模型（embedding/分类/rerank），Dynamo 管大模型主线（Agent 生成） |
| **Dynamo → Vera Rubin** | PD 分离的 Prefill/Decode 池跑在 Rubin GPU，路由/调度逻辑跑在 Vera CPU |
| **SAW → Vera Rubin** | 沙箱/控制面（策略执行、审计）跑 Vera CPU 侧，不占 GPU 算力 |

---

## 四、一次 Agent 请求的完整旅程

```
① 用户在端点（IDE/终端）发起任务
   ↓
② 可信访问代理（SAW）验证身份 → 签发短时会话
   ↓
③ 进入单用户工作区 VM（Vera CPU 侧沙箱控制面已就绪）
   ↓
④ Agent 循环（NemoClaw）解析任务 → 拆解计划
   ↓
⑤ 需要模型推理：
   ├─ 小模型（embedding/意图分类）→ Triton（批处理服务）
   └─ 大模型（生成/推理）→ Dynamo 路由
        ├─ Prefill 池（Rubin GPU 算力型：算输入/前缀）
        ├─ KV Cache 高速传输（NVLink 6）
        └─ Decode 池（Rubin GPU 带宽型：逐 Token 生成）
   ↓
⑥ 需要工具调用（Git/工单/文档）→ 凭据代理 → 企业系统
   （Agent 只拿到「能力」，密钥留在凭据代理里）
   ↓
⑦ 产出写入私有暂存区 → 人工审查（MR/PR 模式）→ 合入
   ↓
⑧ 全程 OCSF 审计（Agent 进程外遥测，不可被 Agent 压制）
```

---

## 五、软硬件对应关系

| 计算任务 | 承载 | 说明 |
|:---------|:-----|:-----|
| 大模型推理（PD 分离） | **Rubin GPU** | HBM4 大显存承载长上下文 KV Cache |
| 路由/调度/数据预处理 | **Vera CPU** | Dynamo 智能路由、Agent 输入清洗 |
| 沙箱/策略执行/凭据代理 | **Vera CPU** | SAW 控制面逻辑，不占 GPU |
| 小模型推理 | **Rubin GPU 或 CPU** | Triton 多后端（GPU/CPU 异构） |
| KV Cache 传输 | **NVLink 6** | PD 分离的关键通道 |
| 网络边界/出站管控 | **ConnectX-9 / BlueField-4** | SAW 网络形态（brokered network） |

---

## 六、部署形态（从小到大）

| 形态 | 组成 | 适用 |
|:-----|:-----|:-----|
| **单机试点** | Vera CPU + 单 Rubin GPU + Triton + OpenShell 沙箱 | POC、单部门试点 |
| **工作区集群** | 多台 Vera Rubin + Dynamo（单机/小规模 PD）+ SAW 控制面 | 团队级部署 |
| **AI Factory** | NVL72 机架 + Dynamo（完整 PD 分离 + 自动扩缩）+ SAW 全量治理 | 企业级规模化 |

---

## 七、价值闭环

```
硬件层（Vera Rubin 底座）
   ↓ 提供算力
推理层（Triton 小模型 + Dynamo 大模型）
   ↓ 提供智能
安全层（SAW 沙箱 + 凭据代理 + 审计）
   ↓ 提供信任
Agent 层（OpenShell + NemoClaw + 蓝图）
   ↓ 提供能力
应用层（ToB 客户场景）
   ↓ 产生
价值：降本（PD 分离/KV 缓存）· 安全（沙箱/审计）· 规模（NVL72 AI Factory）
```

---

## 八、四组件详细页导航

| 组件 | 页面 | 深度 |
|:-----|:-----|:-----|
| Triton | [→ Triton Inference Server](triton-inference-server.md) | 专页 |
| Dynamo | [→ Dynamo PD 分离](dynamo-pd-separation.md) | 专页 |
| 网络层 | [→ ConnectX-9 / BlueField-4 / CMX](network-layer.md) | 专页 |
| Vera Rubin | [→ Vera Rubin 平台](vera-platform.md) | 专页 |
| SAW | [→ SAW 参考架构](nvidia-secure-agent-workspace.md) · [→ 完整翻译](nvidia-saw-translation.md) | 双页 |
| 算法工程师 | [→ AI 算法工程师手册](ai-engineer-playbook.md) | 专页 |
| 原理 | [→ PD 分离](../pd-separation.md) · [→ AF 分离](../af-separation.md) | 原理页 |

---

> 🏠 [返回 Agentic Infra Platform 总览](index.md)
