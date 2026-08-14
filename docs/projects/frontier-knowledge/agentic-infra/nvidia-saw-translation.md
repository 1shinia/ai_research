# 📄 NVIDIA SAW 参考设计 — 完整中文翻译

> **来源**：NVIDIA Secure Agent Workspace Reference Design（官方文档中文全译）
> **状态**：🟢 已收录 · **更新**：2026-08-10
> **定位**：实施细节完整版（12 章逐章翻译）——决策者看[快速解读](nvidia-secure-agent-workspace.md)，实施团队查本页
> **附件**：[📎 PDF 原件下载](nvidia-saw-translation-zh.pdf)

---

## 第 1 章：始终在线、自主运行的代理（Agent），现在可为 AI 工厂安全部署

企业正从聊天式助手转向「始终在线个人代理」，这些代理能够阅读代码、检查文档、运行测试、查询系统、起草更新，并代表单个员工持续运行数小时。这一转变催生了一项新的平台需求：一个用于自主代理执行的「安全的、受管控的代理工作空间（secure, managed agent workspace）」。

**Secure Agent Workspace** 为企业提供了一个受管控的自主代理运行场所：

- 用户端点（endpoint）作为接入层连接，但实际执行发生在受管控的工作空间内
- 身份（identity）、网络访问（network access）、凭据（credentials）、运行时策略（runtime policy）、审计（audit）和人工审查（human review）共同约束代理的行为能力
- **用户端点是展示层（presentation layer），而非执行层（execution layer）**

代理运行时（agent runtime）在被管控的远程环境（单用户虚拟机，可选 GPU 加速）内执行：
- 经批准的完整生命周期（lifecycle）配置
- 经可信代理（trusted broker）访问
- 受运行时执行层（runtime enforcement layer）约束
- 经受管控的连接器（governed connectors）接入企业系统
- 敏感写操作需经过人工审查

**防护目标**：未经授权或意外的写操作、数据外泄（data exfiltration）、提示注入（prompt injection）、代理作为攻击者（agent-as-attacker，出站滥用）、虚拟机内 root 权限失陷（in-VM root compromise）。

**成果**：
- 员工获得持久化工作空间，代理可无限期运行
- 安全团队获得身份网关（identity gates）、出站策略（egress policy）、凭据隔离（credential isolation）、审计日志（audit logs）以及人工审查控制
- 平台团队获得可支撑 AI 工厂规模（AI Factory scale）的参考模式

**成熟度模型（Maturity Model）**：
- **第一阶段（Phase I）**：代理在托管虚拟机中运行（工作空间边界控制，workspace-perimeter controls）
- **第二阶段（Phase II）**：签名策略强制执行的运行时沙箱（runtime sandbox）（NVIDIA OpenShell 或等效方案），具备运行时内默认拒绝出站（deny-by-default in-runtime egress）、凭据代理（credential proxying）、路由推理（routed inference）、文件系统和进程范围限定（filesystem and process scoping）

---

## 第 2 章：什么是安全代理工作空间？

一个受管控的场所，自主工作在此运行——对用户主机设备、外部互联网和企业网络的访问均在基础设施层面进行监控，处于大语言模型（LLM）信任边界之外。

**组件构成**：

| 组件 | 说明 |
|:-----|:-----|
| **工作空间环境** | 受管控的 Linux/Windows 虚拟机 |
| **门户/API（Portal/API）** | 用于生命周期管理 |
| **终端/IDE/GUI 接入** | Terminal/IDE/GUI attachment |
| **可选的 GPU 加速** | GPU acceleration |
| **运行时受限的代理执行** | runtime-bounded agent execution——OpenShell |
| **代理框架组件** | agent-framework components——NemoClaw、AI-Q Blueprints、NeMo Agent Toolkit |
| **可信访问代理** | trusted access broker——企业 SSO（单点登录）、短时会话（short-lived sessions） |
| **分层身份表面** | layered identity surface——用户/主办者（user/sponsor）、工作空间（workspace）、代理（agent）、每次调用的凭据（per-call credential） |
| **每次委托的记录** | per-engagement delegation record |
| **代理治理层** | agent governance layer——签名策略（signed-policy）、遥测（telemetry）、审计（audit）、人工审查（human-review） |
| **对企业系统的受管控访问** | governed access to enterprise systems |

---

## 第 3 章：安全代理工作空间不是什么

安全代理工作空间**不是**：
- ❌ 用于提供生产应用程序的平台
- ❌ 绕过网络控制的手段
- ❌ 安全审查的替代品
- ❌ 多用户共享工作空间（每个工作空间是**单用户、单租户**的虚拟机）
- ❌ 身份提供者（identity provider）

> ⚠️ **关键前提**：容器级隔离（container-level isolation）不足以满足安全要求——代理执行任意代码，沙箱逃逸（sandbox escape）会波及相邻工作负载。**虚拟机隔离（VM isolation）是前提条件**。

---

## 第 4 章：适用场景

### 四种使用场景（Four use cases）

1. **本地端点（Local endpoint）** — 日常开发工作
2. **公共配置文件（Public profile）** — 开源/公开数据工作
3. **企业配置文件（Corporate profile）** — 使用内部依赖的自主开发
4. **服务托管平台（Service-hosting platform）**

### 能力风险模型（Capability Risk Model）— 三要素法则（Rule of Three）

风险随着以下三个要素的叠加而加剧：
- (a) 内部数据访问（internal data access）
- (b) 自主性（autonomy）
- (c) 外部数据访问（external data access）

> 企业配置文件（Corporate profile）约束了要素 (c)；公共配置文件（Public profile）消除了要素 (a)。

### 三个时间尺度（Three timescales）

| 时间尺度 | 对应载体 |
|:---------|:---------|
| **长期运行**（Long-running） | 虚拟机本身 |
| **每次会话**（Per-session） | OpenShell 沙箱 |
| **每次命令**（Per-command） | 临时 Pod（ephemeral pod） |

---

## 第 5 章：参考架构

### 七个逻辑平面（Seven Logical Planes）

平面 1-4（外围）：端点、身份、访问代理、生命周期治理
平面 5-7（执行）：网络边界、运行时沙箱、工作区 VM / 观测

### 架构不变量（Architectural Invariants）

| # | 不变量 | 说明 |
|:-:|:-------|:-----|
| 1 | 原始凭据（raw credentials）不进入代理 | 凭据代理持有密钥，代理拿能力不拿密钥 |
| 2 | 无自我授权（no self-granted authority） | 只能收窄不能扩大 |
| 3 | 不连接未列入清单的目的地 | 出站严格受允许清单控制 |
| 4 | 不篡改系统二进制文件 | 代理无法修改系统级组件 |
| 5 | 代理不创建持久化 | 工作空间状态临时、可重建 |
| 6 | 代理不控制生命周期 | 不能启动/停止/创建其他工作空间 |
| 7 | 不压制审计 | 所有操作必须可追溯 |

### 网络架构（Network Architecture）

代理网络形态（brokered network shape）——**可信访问代理是唯一的信任边界（trust boundary）**。

### 可信访问代理（Trusted Access Broker）

- 仅限 SSO、短时会话、OCSF 审计（OCSF audit）、撤销传播（revocation propagation）
- **代理的是会话（sessions）而非令牌（tokens）**

### 凭据代理（Credential Proxy）

- 位于出站路径中，持有密钥（secrets）
- 代理获取的是**能力（capabilities）而非凭据**

### 推理（Inference）

- 硬依赖（hard dependency）
- 两种模式：本地 / 路由（routed inference）
- GPU 加速独立于推理

---

## 第 6 章：代理蓝图模式

蓝图（Blueprints）是可重复的工作流模板。

### 安全态势规则（Posture Rules）

1. 从最小范围开始（Start narrow）——最小权限（least-privilege）
2. 写操作需要人工审查（writes require human review）
3. 静态策略（static policy）
4. 纵深防御（defense in depth）
5. 生命周期所有权（lifecycle ownership）
6. 默认始终在线（always-on by default）

### 蓝图目录（Blueprint catalog）

- 编码（Coding）
- 文档编写（Documentation）
- 问题分类（Issue triage）
- 开发者入职（Developer onboarding）
- 研究笔记本（Research notebook）
- 运维（Operations）
- 知识工作者（Knowledge worker）

### 写操作门控（Write gating）

代理将内容写入**私有暂存区（private staging surface）**，提出人工审批建议（分支 + MR/PR 模式）。

---

## 第 7 章：企业工具访问模型

### 三个层次（Three layers）

1. **网络可达性**（Network reach）——允许清单（allowlist）
2. **按服务的认证**（Per-service authentication）
3. **动作类别**（Action class）——按蓝图（per blueprint）

### 授权（Authorization）

- **四身份链（four-identity chain）**：用户/主办者 → 工作空间 → 代理 → 每次调用凭据
- 每次委托的记录（per-engagement delegation record）是用户权限的**策略定义子集（policy-defined subset）**
- 委托**严格衰减（strictly attenuating）**

### 服务类别访问模型（Service Category Access Model）

| 服务类别 | 自动运行（autorun）vs 人工审查（human-review）动作 |
|:---------|:---------------------------------------------------|
| **源代码管理**（Source control） | 读自动运行，写需审查 |
| **工作跟踪**（Work tracking） | 读自动运行，写需审查 |
| **文档**（Documentation） | 读自动运行，写需审查 |
| **聊天**（Chat） | 需审查 |
| **邮箱**（Mailbox） | 需审查 |
| **包仓库**（Package repos） | 读自动运行 |
| **数据存储**（Data stores） | 读自动运行，写需审查 |
| **模型端点**（Model endpoints） | 路由推理（routed inference） |
| **外部互联网**（External internet） | 受限/无 |

---

## 第 8 章：安全与治理模型

### 三层防护包络（Three-layer envelope）

1. **基线托管工作空间控制**（Baseline managed-workspace controls）
2. **运行时沙箱控制**（Runtime sandbox controls）
3. **签名策略治理**（Signed-policy governance）

### 控制面（Control Surface）— 六个领域

1. 工作空间（Workspace）
2. OpenShell / 运行时（Runtime）
3. 签名策略（Signed-policy）
4. 身份 / 委托（Identity / delegation）
5. 凭据中介（Credential mediation）
6. 审计 / 撤销（Audit / revocation）

### 威胁模型（Threat Model）

四级递进，每一级均有残余控制（residual controls）：
- 代理级别（Agent-level）→ 非特权用户空间（Unprivileged user-space）→ 操作系统 root 权限（Root-on-OS）→ 虚拟机监控器失陷（Hypervisor compromise）

### 机密计算（Confidential compute）

可选的 TEE（可信执行环境，Trusted Execution Environment）。

### DPU/SmartNIC

可选的 BlueField/ConnectX 卸载（offload）。

---

## 第 9 章：运行属性

八项属性（8 properties）：

1. **所有者/主办者背书**（owner/sponsor-backed）
2. **权限源自注册所有者**（authority from registered owner）
3. **一次引导**（bootstrap once）
4. **短时会话**（short-lived sessions）
5. **允许清单制出站**（allowlisted outbound）
6. **固定配置文件**（fixed profile）
7. **单租户**（single-tenant）
8. **临时状态**（ephemeral state）
9. **写操作经人工审查**（human-reviewed writes）

---

## 第 10 章：部署层级

五个层级（Five tiers）：

| 层级 | 描述 |
|:-----|:-----|
| **CPU VM** | 基于 CPU 的虚拟机 |
| **GPU VM/工作站**（GPU VM/workstation） | 基于 GPU 的虚拟机或工作站 |
| **桌面侧加速工作站**（Deskside accelerated workstation） | 本地 GPU 加速工作站 |
| **团队共享系统**（Team shared system） | 团队级共享资源 |
| **平台集群**（Platform fleet） | 大规模平台部署 |

---

## 第 11 章：Red Hat OpenShift 虚拟化参考实现（本地部署 On-premise）

**第一阶段（Phase I）**：可部署的托管虚拟机控制（Deployable Managed VM Controls）
**第二阶段（Phase II）**：使用 OpenShell 的运行时强制代理策略（Runtime-Enforced Agent Policy with OpenShell）

关键组件：
- 每个用户一个持久虚拟机（persistent VM）
- GitOps / Argo CD
- NFS 存储（NFS storage）
- 可信访问代理（trusted access broker）

---

## 第 12 章：Microsoft Azure 参考实现（云端部署 Cloud）

**第一阶段（Phase I）**："虚拟机即为沙箱（VM is the sandbox）。"
**第二阶段（Phase II）**：虚拟机内运行时执行（in-VM runtime enforcement）。

关键组件：
- 临时单用户 Azure Linux 虚拟机（ephemeral single-user Azure Linux VM）
- 专用不可信虚拟网络（dedicated untrust VNet）
- Azure 防火墙高级版（Azure Firewall Premium）
- NAT 网关 V2（NAT Gateway V2）
- 工作负载身份联合（Workload Identity Federation）——**无密钥（secretless）**
- Microsoft Entra ID
- 可信访问代理（trusted access broker）

---

> 📌 本页基于 NVIDIA Secure Agent Workspace Reference Design 完整翻译，用于企业内部架构参考。技术术语首次出现时保留英文原文，后续使用中文翻译。
> 🔗 快速理解版（5 分钟）：[NVIDIA Secure Agent Workspace 参考架构 →](nvidia-secure-agent-workspace.md)
> 🏠 [返回 Agentic Infra Platform 总览 →](index.md)
