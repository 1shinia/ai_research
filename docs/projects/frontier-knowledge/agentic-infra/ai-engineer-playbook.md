## 工作范围全景（六大块）

### 优先级与技术栈速览

| 优先级 | 工作块 | 核心技术栈 | 为什么重要 |
|:--:|:--|:--|:--|
| 🔥 P0 | ① 模型推理服务化 | 推理引擎：Triton、Dynamo、vLLM、SGLang、TensorRT-LLM<br>推理优化：PD 分离、AF 分离、多级 KV Cache、智能路由、自动扩缩、量化（FP8/INT4/INT8）<br>关键指标：TTFT、TPOT、吞吐、KV 命中率 | 平台最硬核的差异化能力，Token 降本核心 |
| 🔥 P0 | ③ Agent 算法设计 | Prompt 工程、Function Calling、ReAct、RAG、记忆系统、Plan-and-Execute、子代理、MCP、LLM-as-Judge 评估 | 产品化核心，蓝图定制全靠它 |
| ⚡ P1 | ② Agent 运行时 | OpenShell（沙箱）、NemoClaw（harness）、LangGraph、AutoGen、NeMo Agent Toolkit | Agent 主循环：感知→思考→行动→观察 |
| ⚡ P1 | ④ 工具接入 | MCP 协议、工具 Schema、9 类受管服务封装（Git/工单/文档/邮件/数据存储） | 生态层，Agent 的能力来源 |
| 🛡️ P1 | ⑤ 安全约束设计 | 凭据代理、提示注入防御、指令层级、七条不变量、OCSF 审计埋点 | 平台差异化卖点——没有安全 ToB 客户不会采购 |
| 🛠️ P2 | ⑥ 部署与调优 | Docker/K8s、GitOps/Argo CD、Ray Serve、Prometheus/Grafana、GPU 集群 | 工程化落地 |

---

## 一、模型推理服务化（Inference）——算力侧核心

### 出处
SAW 第 5 章：「推理（Inference）：**硬依赖**（hard dependency），两种模式（**本地 / 路由**），GPU 加速独立于推理。」

### 1.1 本地推理（Local Inference）

| 项目 | 内容 |
|:-----|:-----|
| 场景 | Agent 工作区 VM 内直接跑模型（单用户、单租户） |
| 典型硬件 | 第 10 章层级 2-3：GPU VM / 桌面侧加速工作站 |
| 工作内容 | ① 模型选型（开源权重 / 商用 API）② 量化压缩（FP8/INT4/INT8）③ 本地推理栈搭建 ④ 上下文窗口与 KV Cache 管理 ⑤ 长会话稳定性（Agent 常驻数小时） |
| 技术栈 | TensorRT-LLM、vLLM（单机）、SGLang、llama.cpp、ONNX Runtime、CTranslate2 |
| 关键指标 | 上下文长度、TTFT（首 Token 延迟）、TPOT（逐 Token 延迟）、吞吐 |

### 1.2 路由推理（Routed Inference）——企业级模型端点

| 项目 | 内容 |
|:-----|:-----|
| 场景 | Agent 通过集中式企业推理服务调用模型（多用户共享、统一治理） |
| 工作内容 | ① 推理服务化部署 ② 请求路由策略 ③ 模型版本管理 ④ 多租户隔离 ⑤ 弹性扩缩容 ⑥ 服务 SLA 保障 |
| 技术栈 | **Dynamo**（PD 分离 / 智能路由 / 多级 KV 缓存 / 自动扩缩）、**Triton**、vLLM Serving、SGLang Serving、Kubernetes、Ray Serve |
| 关键指标 | TTFT / TPOT / 吞吐 / KV 缓存命中率 / 扩缩容响应时间 |

### 1.3 Triton Inference Server——推理服务的地基

> 🔗 详细专页：[Triton Inference Server](triton-inference-server.md)

**为什么必须懂 Triton**：它是 NVIDIA 的**多框架推理服务框架**（Dynamo 的前身），负责「模型 → 服务」的统一承载——AI 工厂里几乎所有模型（embedding / reranker / 分类 / 生成）都可能跑在它上面。

| 项目 | 内容 |
|:-----|:-----|
| 定位 | 多后端统一推理服务：TensorRT / PyTorch / ONNX / vLLM / Python 自定义 |
| 核心能力 | 动态批处理、并发模型执行、模型版本管理、HTTP/gRPC/流式协议 |
| 与 Dynamo 关系 | **Dynamo 是 Triton 在 LLM 时代的演进**；两者可共存分层（Triton 管传统模型，Dynamo 管大模型主线） |
| 算法工程师工作 | ① 部署与后端配置 ② 动态批处理参数调优 ③ TensorRT 引擎化（FP8 图优化）④ Perf Analyzer 压测 ⑤ 与模型端点/凭据代理集成（配额、限流、审计） |
| 本地推理场景 | Agent 工作区 VM 内的轻量模型承载（embedding、意图分类、小模型工具调用） |

**典型混合推理栈（Agentic Infra 视角）**：

```
Agent 工具调用
   ├─ 小模型（embedding/分类/rerank） → Triton（批处理 + 多后端）
   └─ 大模型主线（生成/推理）          → Dynamo（PD 分离 + KV 缓存）
                                          ↓
                                GPU 资源池（Vera Rubin / NVL72）
```

### 1.4 PD 分离推理优化（关联 Dynamo 页）

**原理**：Prefill（计算密集）与 Decode（带宽密集）拆到不同资源池。

```
Prefill 池（算力型） → KV Cache 传输 → Decode 池（带宽型） → 输出
```

| 维度 | 收益 | 代价 |
|:-----|:-----|:-----|
| 资源利用率 | 各自拉满，吞吐↑ | 跨池调度复杂度 |
| 延迟 | TTFT / TPOT 分别做 SLA | KV 传输延迟 |
| 成本 | 按需配比，硬件不浪费 | 网络带宽要求高（RDMA） |

**算法工程师的工作**：
- 确定 PD 分离配比（Prefill 实例数 vs Decode 实例数）
- 多级 KV 缓存策略设计（热门前缀复用）
- 与 vLLM / SGLang / TensorRT-LLM 的集成选型
- 长上下文场景的 KV 传输优化

### 1.4 模型端点接入（SAW 第 7 章）

> **原文**：模型端点（Model endpoints）→ 路由推理（routed inference）

- 模型端点是企业 9 类受管服务之一
- **与凭据代理集成**：Agent 无密钥调用模型（能力而非凭据）
- 工作内容：模型端点 API 设计（OpenAI 兼容协议 / 自定义协议）、鉴权接入、调用审计、配额管理

---

## 二、Agent 算法设计（Algorithm & Blueprint）——算法侧核心

### 出处
SAW 第 6 章：「蓝图（Blueprints）是可重复的工作流模板。」

### 2.1 七类蓝图目录

| 蓝图 | 典型工作流 | 算法工程师的工作 |
|:-----|:-----------|:-----------------|
| 编码（Coding） | 代码生成/修改/重构 | 代码模型选型、代码上下文切片、变更合入策略 |
| 文档编写（Documentation） | 自动文档/注释/Release Notes | 长文档生成、结构一致性控制 |
| 问题分类（Issue triage） | 工单分诊/路由/标签 | 分类模型或 LLM 分类、标签体系设计 |
| 开发者入职（Onboarding） | 环境搭建/权限申请/文档引导 | 多步工具链编排、知识检索（RAG） |
| 研究笔记本（Research notebook） | 实验/分析/可视化 | 代码+文本混合工作流、结果结构化 |
| 运维（Operations） | 监控/告警/故障排查 | 日志分析、根因定位（RCA）提示链 |
| 知识工作者（Knowledge worker） | 通用办公/汇总/起草 | 企业知识库 RAG、引用溯源、事实核查 |

### 2.2 每个蓝图落实的 6 条安全态势规则

| 规则 | 算法层面的落地 |
|:-----|:---------------|
| ① 最小权限起步 | 蓝图定义最小工具集；prompt 中显式限定可调用工具 |
| ② 写操作需人工审查 | 产出进暂存区（staging）+ MR/PR 审批流 |
| ③ 静态策略 | 蓝图固定模板，不在运行时被 Agent 改写 |
| ④ 纵深防御 | 模型层 + 工具层 + 网络层多层约束 |
| ⑤ 生命周期所有权 | 蓝图版本由平台团队管理，Agent 无权变更 |
| ⑥ 默认始终在线 | 长驻 Agent 设计（心跳/恢复/会话持久化） |

### 2.3 写操作门控（Write Gating）

```
Agent 产出 → 私有暂存区（private staging）→ 人工审批建议 → MR/PR 合入
```

- 算法工程师设计「生成→建议→合入」的流程编排
- 涉及：Git 分支策略、PR 模板、审批 Webhook、变更回滚

### 2.4 算法技术栈明细

| 方向 | 技术/方法 |
|:-----|:----------|
| Prompt 工程 | 系统提示词设计、few-shot、思维链（CoT）、结构化输出（JSON Schema） |
| 工具调用 | Function Calling、OpenAI Tool API、MCP、ReAct 循环 |
| 检索增强 | RAG、向量数据库（Milvus/FAISS）、重排序（Reranker）、混合检索 |
| 记忆系统 | 短期对话记忆、长期向量记忆、会话压缩、摘要记忆 |
| 规划 | Plan-and-Execute、任务分解（Task Decomposition）、子代理委派 |
| 评估 | 工具调用成功率、任务完成率、幻觉率、人工评测（LLM-as-Judge） |
| 模型后训练（可选） | SFT（指令微调）、RLHF / GRPO（强化学习对齐）——对应论文工作流 RL 领域 |

---

## 三、Agent 运行时与框架（Runtime）——执行层

### 出处
SAW 第 2 章组件构成 + 第 5 章运行时强制层。

### 3.1 组件清单与分工

| 组件 | 角色 | 算法工程师的活 |
|:-----|:-----|:---------------|
| **OpenShell** | 运行时沙箱（执行边界） | Agent 工具调用边界设计；确保沙箱内可用工具集 |
| **NemoClaw** | Agent harness（主循环） | Agent Loop 设计：感知→思考→行动→观察 |
| **AI-Q Blueprints** | 预置 Agent 蓝图 | 在预置蓝图基础上定制行业工作流 |
| **NeMo Agent Toolkit** | 技能（Skills）与观测 | 技能封装、遥测埋点、可观测性接入 |

### 3.2 Agent 主循环设计（算法核心）

```
┌─────────────────────────────────────────┐
│  Agent Loop                              │
│  ① 任务理解（解析用户意图/拆解子任务）       │
│  ② 规划（Plan：多步计划 / 任务树）          │
│  ③ 工具调用（Function Calling / MCP）      │
│  ④ 上下文管理（对话历史 / 记忆 / 压缩）      │
│  ⑤ 错误恢复（重试 / 回退 / 人工升级）        │
│  ⑥ 产出（写入暂存区 → 人工审查 → 合入）      │
└─────────────────────────────────────────┘
```

**技术栈**：Function Calling（tool use）、ReAct / Plan-and-Execute 范式、上下文压缩（Context Compression）、记忆系统（短期/长期）、子代理（Sub-agent）、任务系统（Task Manager）、后台任务（Background Task）、Cron 定时任务、MCP（Model Context Protocol）插件。

---

## 四、工具接入（Tool Integration）——生态层

### 出处
SAW 第 7 章 服务类别访问模型。

### 4.1 九类受管服务与动作策略

| 服务类别 | 自动运行（autorun） | 人工审查（human-review） | 算法工程师的工作 |
|:---------|:-------------------|:------------------------|:-----------------|
| 源代码管理 | 读 | 写 | Git 工具封装、diff/patch 生成 |
| 工作跟踪 | 读 | 写 | 工单解析、状态机编排 |
| 文档 | 读 | 写 | 文档解析（PDF/Word/Markdown） |
| 聊天 | — | 需审查 | 消息收发、上下文注入 |
| 邮箱 | — | 需审查 | 邮件解析、草稿生成、发送审批 |
| 包仓库 | 读 | — | 依赖解析、版本查询 |
| 数据存储 | 读 | 写 | SQL/API 封装、数据血缘 |
| 模型端点 | 路由推理 | — | 推理调用封装（见①） |
| 外部互联网 | 受限/无 | — | 受限抓取、白名单管理 |

### 4.2 工具封装技术栈

- **MCP**（Model Context Protocol）：统一工具接入协议
- 工具 Schema 定义（输入/输出 JSON Schema）
- 工具错误处理与重试
- 工具调用的审计埋点（OCSF 格式）

---

## 五、安全约束下的算法设计（Security-aware）——红线层

### 出处
SAW 第 3/5/8 章。

### 5.1 算法工程师必须遵守的七条不变量

| # | 不变量 | 算法层面的影响 |
|:-:|:-------|:---------------|
| 1 | 原始凭据不进 Agent | 模型/工具调用全部走凭据代理；prompt 里禁止出现密钥 |
| 2 | 无自我授权 | Agent 不能自己扩大权限；算法上做权限边界检查 |
| 3 | 不连未列明地址 | 工具目标全部来自白名单；限制任意 URL 访问 |
| 4 | 不篡改系统二进制 | 禁止 Agent 改系统配置（.bashrc 等） |
| 5 | 不创建持久化 | 会话状态临时；记忆需走受管记忆系统 |
| 6 | 不控制生命周期 | Agent 不能启停工作区/其他 Agent |
| 7 | 不压制审计 | 所有调用可追溯；算法设计时预留可解释性 |

### 5.2 提示注入防御（算法层）

- 输入净化：区分「指令」与「数据」（文档/邮件/工单内容）
- 指令层级（hierarchical instructions）：系统 > 用户 > 外部内容
- 工具调用白名单 + 参数校验
- 敏感操作二次确认

### 5.3 可解释性与审计

- 每次工具调用的决策链记录（为什么调用这个工具）
- OCSF 遥测格式埋点
- 人工审查界面（审批流 UI）

---

## 六、部署与调优（Deployment & Optimization）——工程化

### 出处
SAW 第 10/11/12 章 + Dynamo 页 + Vera 页。

### 6.1 五级部署层级（算法视角）

| 层级 | 硬件 | 算法工程师关注点 |
|:-----|:-----|:-----------------|
| CPU VM | 纯 CPU | 小模型（7B 以下）量化部署 |
| GPU VM/工作站 | 单卡 GPU | 主流 7B-70B 模型 |
| 桌面侧加速工作站 | 本地 GPU | 离线/低延迟场景 |
| 团队共享系统 | 多卡共享 | 资源调度、多用户隔离 |
| 平台集群 | 大规模集群 | **Dynamo PD 分离 + 自动扩缩** |

### 6.2 Vera Rubin 平台（2026 落地）

| 能力 | 算法工程师的对接 |
|:-----|:----------------|
| Rubin HBM4 大显存 | 长上下文 KV Cache 承载、更大模型 |
| NVLink 6 高速互联 | PD 分离 KV 传输、多卡并行 |
| Vera CPU | 数据预处理/路由/调度在 CPU 侧卸载 |
| NVL72 机架形态 | 大规模 AI Factory 部署 |

### 6.3 部署技术栈

- 容器化：Docker + Kubernetes（云）/ OpenShift（本地）
- 推理服务：Dynamo / Triton / vLLM Serving
- 编排：GitOps / Argo CD、Ray Serve
- 存储：NFS（OpenShift 参考）、对象存储
- 可观测：Prometheus / Grafana / 链路追踪

---

## 七、技术栈总表（分层全景）

| 层次 | 技术 / 工具 | 文章出处 |
|:-----|:-----------|:---------|
| **模型层** | 开源权重模型、商用 API、量化（FP8/INT4） | 第 5 章 |
| **推理框架** | **Triton**（多后端服务层/地基）、**Dynamo**（LLM 编排）、vLLM、SGLang、TensorRT-LLM | 第 5 章 + Triton 页 + Dynamo 页 |
| **推理优化** | PD 分离、AF 分离、多级 KV 缓存、智能路由、自动扩缩、RDMA | Dynamo 页 + 原理页 |
| **Agent 运行时** | OpenShell（沙箱）、NemoClaw（harness）、AI-Q Blueprints、NeMo Agent Toolkit | 第 2 章 |
| **Agent 算法** | Function Calling、ReAct、RAG、记忆、规划、子代理、MCP、Cron | 第 6 章 + learn-claude-code |
| **工具生态** | Git/工单/文档/聊天/邮箱/包仓库/数据存储/模型端点（9 类） | 第 7 章 |
| **安全集成** | 凭据代理、四身份链、签名策略、人工审查门、OCSF 审计、TEE | 第 5/8 章 |
| **基础设施** | Kubernetes、OpenShift、Azure、GitOps/Argo CD、NFS、Docker | 第 11/12 章 |
| **硬件** | Vera CPU + Rubin GPU、HBM4、NVLink 6、NVL72 | Vera 页 |

---

## 八、能力要求（技能点清单）

**硬技能**：
- LLM 推理原理（Transformer、KV Cache、Prefill/Decode）
- **Triton 部署与调优**（多后端配置、动态批处理、Perf Analyzer 压测、TensorRT 引擎化）
- 推理引擎（Dynamo / vLLM / SGLang / TensorRT-LLM）部署与调优
- PD/AF 分离理解与配比调优
- Prompt 工程 / Function Calling / RAG / 记忆系统
- Agent 框架（OpenShell / NemoClaw / LangGraph / AutoGen）
- 模型量化（FP8/INT4）、长上下文优化
- Python、PyTorch、Docker/K8s 基础、Git 工作流

**软技能**：
- 安全思维（最小权限、不变量、审计意识）
- 企业工具生态理解（Git/工单/CI 流程）
- 与平台/安全团队协作接口设计

---

## 九、对平台项目的启示

1. **岗位画像**：AI 算法工程师 = 模型层（推理服务化）+ Agent 层（算法与蓝图），安全边界由平台提供
2. **能力分层**：推理优化（Dynamo/PD 分离）是最硬核的差异化，Agent 算法是产品化核心
3. **协作接口**：算法工程师通过「蓝图 + 工具封装 + 模型端点」三接口接入平台，不触碰基础设施
4. **培训路线**：从 learn-claude-code（20 课 Harness 机制）→ ai-agent-book（10 章体系）→ SAW 安全约束 → Dynamo 推理优化

## 十、B 站学习资源清单（配套培训路线）

> **定位**：对应第九节培训路线的 B 站视频资源，按学习顺序分五站
> **更新**：2026-08-16 · 来源：B 站公开搜索（播放量为检索时数据）

### 🥇 第 1 站：LLM 推理原理（地基，最优先）

| 视频 | 播放量 | 亮点 |
|:--|:--:|:--|
| [KV Cache 原理讲解](https://search.bilibili.com/all?keyword=KV%20Cache%20%E5%8E%9F%E7%90%86%E8%AE%B2%E8%A7%A3) | 8.9 万 | 最经典的 KV Cache 讲解 |
| [保姆级 KV Cache 教程：底层原理到显存计算](https://search.bilibili.com/all?keyword=KV%20Cache%20%E5%BA%95%E5%B1%82%E5%8E%9F%E7%90%86) | 1.9 万 | 新手友好，配合显存计算实战 |
| [详解 PD 分离，vLLM 和 SGLang 怎么优化它](https://search.bilibili.com/all?keyword=PD%E5%88%86%E7%A6%BB%20vLLM%20SGLang) | 9.5 千 | 直接对口 Dynamo PD 分离原理 |
| [大模型部署为什么要用 PD 分离](https://search.bilibili.com/all?keyword=%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2%20PD%E5%88%86%E7%A6%BB) | 1 千 | 通俗版 PD 分离 |
| [吴恩达：快速高效的 LLM 推理与 vLLM（中英字幕）](https://search.bilibili.com/all?keyword=%E5%90%B4%E6%81%A9%E8%BE%BE%20vLLM) | 3.6 千 | 国际大师课，附代码 |

### ⚙️ 第 2 站：推理引擎实操（vLLM → SGLang → Triton）

| 视频 | 播放量 | 亮点 |
|:--|:--:|:--|
| [vLLM 原理详解（2026 最新版）](https://search.bilibili.com/all?keyword=vLLM%20%E5%8E%9F%E7%90%86%E8%AF%A6%E8%A7%A3) | 3.9 万 | 讲清 Prefill/Decode 两大阶段 |
| [vLLM 推理优化：KV Cache + PageAttention 全解析](https://search.bilibili.com/all?keyword=vLLM%20%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96%20KV%20Cache%20PageAttention) | 3.4 万 | 优化向，对应平台推理优化工作 |
| [Triton Inference Server：工具使用、实践总结与性能优化](https://search.bilibili.com/all?keyword=Triton%20Inference%20Server%20%E5%AE%9E%E8%B7%B5) | 2.2 千 | 直接对口 Triton 专页（B 站高质量内容少，这条最实用） |
| [SGLang 官方 180 秒快速了解](https://search.bilibili.com/all?keyword=SGLang) | 2.3 千 | 官方快览，配合文档学 |
| [TensorRT-LLM 实用指南：Llama3 推理加速](https://search.bilibili.com/all?keyword=TensorRT-LLM%20Llama3) | 1.3 千 | 引擎化实操 |

### 🤖 第 3 站：Agent 算法（FC / RAG / MCP）

| 视频 | 播放量 | 亮点 |
|:--|:--:|:--|
| [RAG 工作机制详解——知识库技术全流程](https://search.bilibili.com/all?keyword=RAG%20%E5%B7%A5%E4%BD%9C%E6%9C%BA%E5%88%B6%E8%AF%A6%E8%A7%A3) | 37.4 万 | RAG 领域经典神作，必看 |
| [MCP 与 Function Calling 到底什么关系](https://search.bilibili.com/all?keyword=MCP%20Function%20Calling%20%E5%85%B3%E7%B3%BB) | 9.4 万 | 一句话讲透两个概念关系，对口 4.1 节 |
| [Function Calling 技术详解（13 集保姆级）](https://search.bilibili.com/all?keyword=Function%20Calling%20%E6%8A%80%E6%9C%AF%E8%AF%A6%E8%A7%A3) | 6.6 千 | 系统课，理论到实战 |
| [AI 工程化实战：MCP 与 Agent 系统构建](https://search.bilibili.com/all?keyword=MCP%20Agent%20%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA) | 5 千 | 工程向 MCP 落地 |
| [尚硅谷 LangGraph 教程](https://search.bilibili.com/all?keyword=%E5%B0%9A%E7%A1%85%E8%B0%B7%20LangGraph) | 34.9 万 | 系统入门课（对标 NemoClaw harness 概念） |

### 🛡️ 第 4 站：Agent 安全（平台差异化卖点）

| 视频 | 播放量 | 亮点 |
|:--|:--:|:--|
| [AI Agent 的沙箱是什么？和 Docker/VM 区别](https://search.bilibili.com/all?keyword=AI%20Agent%20%E6%B2%99%E7%AE%B1) | 22.6 万 | 直接对口 OpenShell 沙箱 |
| [AI Agent 沙箱：演进过程到实现方式](https://search.bilibili.com/all?keyword=AI%20Agent%20%E6%B2%99%E7%AE%B1%20%E6%BC%94%E8%BF%9B) | 5.7 千 | 实现细节向 |
| [AI 攻防：Agent 漏洞/提示注入/安全评测](https://search.bilibili.com/all?keyword=%E5%A4%A7%E6%A8%A1%E5%9E%8B%20%E6%8F%90%E7%A4%BA%E6%B3%A8%E5%85%A5%20%E5%AE%89%E5%85%A8) | 5.8 千 | 对口 5.2 节提示注入防御 |

### 🧮 第 5 站：数据检索与后训练（加分项）

| 视频 | 播放量 | 亮点 |
|:--|:--:|:--|
| [Milvus 向量数据库 + RAG 企业实战（2026）](https://search.bilibili.com/all?keyword=Milvus%20%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%20RAG) | 2.2 万 | 对口 2.4 节向量库（Milvus/FAISS） |
| [GRPO 零基础也能看懂](https://search.bilibili.com/all?keyword=GRPO%20%E7%AE%97%E6%B3%95) | 2.6 万 | 对口可选后训练 RLHF/GRPO |

### 🗺️ 与培训路线的对应

| 培训路线环节 | 对应资源 |
|:--|:--|
| learn-claude-code（20 课 Harness 机制） | 第 3 站 Agent 算法（LangGraph/FC/MCP） |
| ai-agent-book（10 章体系） | 第 3 + 5 站（RAG/记忆/评估） |
| SAW 安全约束 | 第 4 站（沙箱/提示注入）+ wiki SAW 翻译 |
| Dynamo 推理优化 | 第 1 + 2 站（KV Cache/PD 分离/vLLM） |

> ⚠️ **B 站盲区**：Dynamo、NVIDIA SAW、Vera Rubin 硬件层在 B 站几乎无对口视频（太新太前沿），以官方文档 + wiki 内翻译资料为准。
> 🔗 搜索入口：https://search.bilibili.com/all?keyword=关键词（播放量数据截至 2026-08-16）
---

> 📌 本页摘编自 SAW 完整翻译及关联页面，供 AI 算法工程师岗位职责梳理 / 技术栈规划 / 团队协作接口设计使用。
