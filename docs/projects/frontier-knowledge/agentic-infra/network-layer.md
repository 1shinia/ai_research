# 🌐 网络层：ConnectX-9 / BlueField-4 / CMX

> **领域**：Agentic Infra / 网络与存储
> **状态**：🟢 已收录 · **更新**：2026-08-10
> **相关**：[Dynamo PD 分离](dynamo-pd-separation.md) · [Vera Rubin](vera-platform.md) · [平台技术全貌](platform-overview.md) · [总览](index.md)

---

## 一句话

网络层是 AI 工厂的**血管系统**：ConnectX-9（智能网卡）负责高速进出，BlueField-4（DPU）在网卡上叠加计算与安全，**CMX** 更进一步——把网络存储变成 GPU 的「外部 KV Cache 仓库」，解决长上下文 Agent 推理最大的显存瓶颈。

---

## 一、ConnectX-9（SmartNIC 智能网卡）

### 定位

NVIDIA 网络产品线的**高速网卡基础款**，GTC 2026 随 Vera Rubin 平台发布，属 **800Gb/s 世代**。

### 核心能力

| 能力 | 说明 |
|:-----|:-----|
| **800Gb/s 接入** | 以太网 / InfiniBand 双形态 |
| **RDMA** | 远程直接内存访问——**PD 分离 KV Cache 高速传输的关键技术** |
| **GPUDirect** | GPU 直接收发数据，绕过 CPU（省一次拷贝） |
| **RoCE** | 以太网上跑 RDMA（RDMA over Converged Ethernet） |

### 对比定位

```
ConnectX（纯网卡）      = 门卫：只管数据进出，便宜够用
BlueField（DPU）       = 门卫 + 保安 + 仓库管理员：还能卸载计算/安全/存储
```

---

## 二、BlueField-4（DPU 数据处理单元）

### 定位

**官方定义**：*"800Gb/s 基础设施计算平台，面向 gigascale AI 工厂；计算能力是前代（BlueField-3）的 6 倍，内置网络、存储、网络安全加速。"*

### 关键规格

| 维度 | 信息 |
|:-----|:-----|
| 速度 | **800Gb/s**（前代 400Gb/s） |
| 算力 | 前代 **6 倍** |
| 三大加速 | 网络（SDN/分布式路由）、存储（NVMe-oF、GPUDirect Storage）、安全（零信任/实时威胁检测） |
| 特殊版本 | **BlueField-4 STX 存储处理器**——基于 **Vera CPU**，专为 AI 存储设计 |
| 软件栈 | **DOCA**（DPU 编程框架） |

### 在 Agentic Infra 中的角色

- **释放 CPU**：基础设施任务（网络/存储/安全）从主机 CPU 卸载到 DPU
- **零信任安全**：威胁检测比纯软件快 **1000x**，800Gb/s 网络强制（对应 SAW 出站白名单的硬件实现）
- **存储加速**：管理 NVMe SSD、跑存储服务、**卸载 KV Cache 的数据完整性与加密**

---

## 三、CMX（Context Memory Storage Platform）★ 核心概念详解

### 3.1 官方定义

> **NVIDIA CMX™** 是 **AI 原生的上下文层（context tier）**，专为**长上下文、多轮对话、agentic AI 推理**设计。由 **BlueField-4 存储处理器**驱动，用共享的 **pod 级上下文层**扩展 GPU 内存，针对**临时 KV Cache（ephemeral KV cache）**做了深度优化。

### 3.2 它解决什么问题？（白话版）

**问题**：长上下文 Agent 的 KV Cache 太大，GPU 显存装不下。

```
普通推理：KV Cache 存在 GPU 显存里（HBM4 也有限）
   ↓ 上下文变长（百万 Token）或多 Agent 并发
GPU 显存爆了 → 要么缩小上下文，要么加 GPU（贵！）

CMX 的答案：把 KV Cache 存到网络存储层，按需调取
   ↓
GPU 显存只放"正在算的部分"，KV Cache 放 CMX 池
   → 显存瓶颈解除，长上下文/多 Agent 都能跑
```

### 3.3 为什么 KV Cache 值得放到存储层？

| 维度 | 传统做法 | CMX 做法 |
|:-----|:---------|:---------|
| KV Cache 位置 | 只在 GPU 显存 | GPU 显存 + **pod 级网络存储层** |
| 重复计算 | 相同前缀每次重新 Prefill | **复用预计算的 KV Cache**（省算力） |
| 上下文上限 | 被单卡显存卡死 | 接近无限（存储池扩容即可） |
| 多 Agent 共享 | 各算各的、互相重复 | pod 内**共享 KV Cache**（多轮 Agent 协调状态） |

### 3.4 「pod 级网络存储层」是什么意思？（概念澄清）

#### 这里的 pod 怎么理解？

**在 NVIDIA CMX 语境里，pod ≠ Kubernetes Pod。** 它是 **NVIDIA AI 数据中心里的「计算单元」**——一组 GPU 服务器（比如几十台，通过高速网络连成一个可以整体调度的集群单位）：

| 概念 | 类比 |
|:-----|:-----|
| 1 台 GPU 服务器 | 1 个工人 |
| **1 个 pod**（一组服务器 + 交换机） | **1 个班组**（几十个工人 + 班长） |
| AI Factory（整个数据中心） | 整个工厂（多个班组） |

#### 与 Kubernetes Pod 的区别

| | Kubernetes Pod | CMX 的 pod |
|:--|:---------------|:-----------|
| 本质 | 容器调度的最小单元（几个容器一组） | AI 数据中心的计算单元（一批 GPU 节点） |
| 范围 | 软件层面的隔离边界 | 硬件层面的部署/共享边界 |
| 用途 | 跑一组相关容器 | 一组需要共享 KV Cache 的推理节点 |

> 名字相同纯属巧合，都是"一组相关的东西"的意思，但一个管软件容器、一个管 GPU 集群。

#### 存储金字塔：CMX 处在哪一层？

```
层级                    速度       容量       谁用
─────────────────────────────────────────────────────
① GPU 显存（HBM4）      最快 ⚡⚡⚡   最小        单卡私有（随身口袋）
② 本地 NVMe            快   ⚡⚡     中          单机私有（工位抽屉）
③ pod 级网络存储（CMX）  中速 ⚡       大  ★★★    一个 pod 内所有 GPU 共享（班组公共仓库）
④ 数据中心级存储        慢           巨大        整个数据中心（公司中央仓库）
```

**CMX 就是第 ③ 层**——「班组公共仓库」：
- 一个 pod 里的任何 GPU 都能通过网络读写它
- KV Cache 存这里，比显存慢但容量大得多
- 比数据中心级存储快（距离近、RDMA 直达）

#### 为什么偏偏是「pod 级」？（设计意图）

关键在**「多 Agent 协作」**：

```
场景：同一个 pod 里跑 100 个 Agent，都在处理同一个长文档/同一个客户会话

如果 KV Cache 只存显存/本地盘：
   → 每个 Agent 各算各的，重复 Prefill 100 次 ❌

如果存 pod 级共享层（CMX）：
   → 第一个 Agent 算完前缀，其他 99 个直接复用 ✅
   → 多轮 Agent 还能共享中间状态（A 写、B 读）
```

- **太小（单机）**：装不下、共享不了，Agent 协作不起来
- **太大（整个数据中心）**：太远、太慢，取 KV Cache 的延迟反而拖累推理
- **pod 级（一组节点）**：容量够大 + 距离够近 + 高速网络可达 = **刚好** 🎯

### 3.5 性能数据（官方）

| 指标 | 数据 |
|:-----|:-----|
| 吞吐 | **最高 5x 提升**（对比通用存储方案） |
| 能效 | **最高 5x 提升**（KV Cache 优化存储层，省下电力给 GPU） |
| TTFT / TLOT | 显著降低（首 Token 更快、末 Token 更快） |
| 压缩吞吐 | **3.29x**（Vera CPU in BlueField-4 STX） |
| 完整性检查（CRC32C） | **3.67x**（Vera CPU in BlueField-4 STX） |

### 3.6 技术组成（四件套）

**先说结论**：这四件**不是并列关系**，而是一个「产品总称 → 硬件载体 → 运行其上的软件 → 外部连接/外部使用方」的**分层结构**：

```
┌────────────────────────────────────────────────────────────────┐
│  NVIDIA CMX（产品总称：一个完整的存储平台）                        │
│                                                                │
│  ┌──────────────────────── 硬件层 ───────────────────────────┐ │
│  │  BlueField-4 STX（存储处理器/DPU）                        │ │
│  │    ├─ 管理 NVMe SSD 池（KV Cache 物理存放地）              │ │
│  │    └─ 承载存储服务软件（Memos 就跑在它上面）                │ │
│  │  Spectrum-X 以太网（连接硬件：交换机 + ConnectX/BlueField） │ │
│  │    └─ 连接 GPU 节点 ⇄ CMX 存储池的物理通路                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────── 软件层 ───────────────────────────┐ │
│  │  DOCA（BlueField 的通用软件框架）                          │ │
│  │    └─ DOCA Memos（CMX 专属 KV 读写 API/SDK）              │ │
│  │        └─ 跑在 BlueField-4 上，管理 KV Cache 存取          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌────────────── 外部使用方（不属于 CMX，是它的客户） ─────────┐ │
│  │  Dynamo 推理框架（跑在 GPU 节点上）                        │ │
│  │    └─ 通过 Memos 的 API 读写 CMX 里的 KV Cache             │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

#### 包含关系一句话版

| 组件 | 是什么 | 和谁有包含关系 |
|:-----|:-------|:---------------|
| **CMX** | 产品总称（整个平台） | **包含**下面所有东西 |
| **BlueField-4 STX** | 核心硬件（DPU 变体） | CMX 的硬件底座；**承载** DOCA 软件 |
| **DOCA Memos** | 软件 SDK | **跑在 BlueField-4 里**；是 DOCA 框架的 CMX 专属组件 |
| **Spectrum-X** | 网络硬件 | CMX 的**外部连接**设施（不属于 CMX 内部，但 CMX 离不开它） |
| **Dynamo** | 推理框架软件 | CMX 的**外部使用方**（不包含在 CMX 里） |

#### 三个最容易混的关系（白话版）

1. **DOCA Memos 和 BlueField-4 的关系** = 软件和硬件的关系
   ```
   BlueField-4 = 一台「能算的网卡」（电脑）
   DOCA       = 这台电脑的操作系统/框架
   DOCA Memos = 装在这台电脑上的「KV 存取 App」
   ```

2. **Dynamo 不属于 CMX** = 它是顾客
   ```
   CMX   = 一个仓库（BlueField 管仓库、Memos 是仓库的存取系统）
   Dynamo = 来仓库取货的工厂（GPU 节点上的推理框架）
   工厂用仓库，但工厂不是仓库的一部分
   ```

3. **Spectrum-X 是"路"不是"仓库"** = 连接设施
   ```
   CMX 存储池（仓库） ⇄ Spectrum-X（路） ⇄ GPU 节点（工厂）
   ```

#### 四件套各司其职（职责表）

| 组件 | 职责 |
|:-----|:-----|
| **BlueField-4 STX** | 管理 NVMe SSD、跑存储服务、卸载 KV Cache 的完整性与加密 |
| **DOCA Memos** | CMX 优化 SDK：跨计算/存储节点**共享 KV Cache**，暴露简单 KV API，把以太网挂载的 Flash 变成 pod 级缓存层 |
| **Spectrum-X 以太网** | 高性能 RDMA 通路（拥塞控制 + 自适应路由 + 无损 RoCE），低延迟高带宽访问 KV Cache |
| **Dynamo** | 分布式推理框架：让 CMX 层对上层**无缝**，把请求路由到 KV Cache 已存在的地方（KV-aware placement） |

### 3.7 DOCA Memos 详解（KV 读写 API / 控制面）

**官方定义**：DOCA Memos 是 **BlueField-4 和 CMX 优化的 SDK**，跨 AI 计算和 CMX 数据节点**管理和共享 KV Cache**，为 AI 应用暴露一个简单的 key-value API，把 **Ethernet 连接的 Flash 变成 pod 级缓存层**。

#### 核心能力

| 能力 | 说明 |
|:-----|:-----|
| **简单 KV API** | 应用侧只需 `put / get` KV Cache，不关心底层存储细节 |
| **跨节点共享** | 一个 pod 内所有 GPU 节点共享 KV Cache，不重复存储 |
| **硬件加速完整性与加密** | 数据完整性校验 + 加密在 BlueField-4 芯片上完成（不是软件算） |
| **应用无状态化** | 应用保持无状态，KV Cache 的路由和复用交给 CMX 处理（stateful 逻辑下沉） |

#### 为什么重要（白话版）

```
传统：每个 GPU 自己管 KV Cache → 重复存储、显存吃紧、跨节点取不到
DOCA Memos：把 KV Cache 变成"pod 内公共仓库"
   ├─ 应用只需要说：给我 key=abc 的 KV Cache
   └─ 至于它在哪个 SSD、怎么加密、怎么校验 → Memos 全包了
```

#### 关键特性拆解

1. **Key-Value 抽象**：KV Cache 被建模成 (key, value)，key 通常对应「请求/会话/前缀哈希」，value 是 KV 张量
2. **无状态应用设计**：推理引擎（Dynamo/vLLM 等）不用自己管 KV 存储位置，只调用 API → 上层无缝
3. **硬件卸载**：完整性（CRC32C，3.67x）和加密都在 BlueField-4 芯片内做，不占用主机 CPU/GPU
4. **与 Dynamo 配合**：Dynamo 知道"KV 在哪"并做 KV-aware 调度，Memos 负责"怎么存取"——分工清晰

### 3.8 Spectrum-X 以太网详解（RDMA 高速通路 / 数据面）

**官方定义**：Spectrum-X 是 NVIDIA 的高性能以太网平台，为 AI 数据中心优化，提供**无损 RoCE**（RDMA over Converged Ethernet），是 CMX 里 KV Cache 数据搬运的**高速通道**。

#### 核心能力

| 能力 | 说明 |
|:-----|:-----|
| **RDMA（RoCE）** | GPU 之间/GPU-存储之间远程直接内存访问，绕过 CPU 拷贝 |
| **拥塞控制** | 网络拥塞时自动调整，避免 KV Cache 传输抖动 |
| **自适应路由** | 流量动态选择最优路径，避免热点链路 |
| **无损网络** | 不丢包（PFC/ECN 等机制），保证 KV Cache 传输完整性 |
| **低尾延迟** | 减少长尾延迟（tail latency），多 Agent 并发时稳定 |

#### 为什么重要（白话版）

```
PD 分离的瓶颈：KV Cache 在 Prefill 池和 Decode 池之间传输
   → 传输慢 = 整个推理慢（没有高速网络，KV 传输 40x 退化！）
Spectrum-X 的答案：
   ├─ RDMA 直接内存访问（不走 CPU，省拷贝）
   ├─ 拥塞控制（不让传输挤爆网络）
   └─ 无损（不丢包，KV 数据不重传）
```

#### 与 ConnectX 的关系

```
Spectrum-X = 交换机（网络中枢：路由/拥塞控制/无损）
ConnectX-9 = 网卡（端点：接入/收发）
BlueField-4 = 网卡 + 计算（端点 + 存储/安全处理）
```

三者构成完整数据通路：**GPU ⇄ ConnectX/BlueField ⇄ Spectrum-X 交换 ⇄ CMX 存储池**

### 3.9 三大收益

1. **最大化 GPU 利用率**：复用预计算 KV Cache，不重算 → tokens/s↑、TTFT↓
2. **pod 级 KV 共享**：多轮/多 Agent 协调共享状态，减少重复与搁浅容量
3. **扩展 GPU 容量**：支撑长上下文推理、多 Agent 工作流、万亿参数模型、更多并发用户

### 3.10 KV 数据通路全景（Dynamo + Memos + Spectrum-X 如何协同）

```
┌─────────────────────────────────────────────────────────────────┐
│                      KV Cache 生命周期                              │
│                                                                   │
│  ① 请求到达 Dynamo → KV-aware 路由                                  │
│     ├─ 命中 GPU 显存 KV Cache → 直接用                              │
│     └─ 未命中 → 查 Memos（KV 在哪？）                                │
│                                                                   │
│  ② 从 CMX 存储池取回（Spectrum-X RDMA 通路）                        │
│     ├─ ConnectX/BlueField 收数据（800Gb/s）                        │
│     ├─ BlueField 芯片内解密 + 完整性校验（3.67x）                    │
│     └─ GPUDirect 直达 GPU 显存（不走 CPU）                          │
│                                                                   │
│  ③ Decode 完成后 → 新 KV 写回 CMX（Memos put API）                  │
│     ├─ BlueField 芯片加密（Memos 硬件加速）                         │
│     └─ 存到 pod 级 NVMe 池（跨节点共享）                            │
│                                                                   │
│  ④ 下一个 Agent 会话/请求 → 复用 KV（不重算 Prefill）               │
└─────────────────────────────────────────────────────────────────┘
```

**分工总结**：
| 环节 | 谁负责 |
|:-----|:-------|
| 知道 KV 在哪、往哪路由 | **Dynamo**（KV-aware placement） |
| 怎么存取、抽象成 API | **DOCA Memos**（控制面） |
| 数据怎么快速/无损搬运 | **Spectrum-X**（数据面） |
| 数据存在哪、加密校验 | **BlueField-4 STX + NVMe**（存储面） |

### 3.11 与平台全貌的衔接（为什么对 Agentic Infra 关键）

```
Agent 请求 → Dynamo 路由（KV-aware：知道 KV Cache 在哪）
   ├─ KV Cache 在 GPU 显存 → 直接用
   └─ KV Cache 在 CMX 池 → Spectrum-X RDMA 快速取回
   ↓
长上下文 Agent（百万 Token 级）+ 多 Agent 并发 → 显存不再是瓶颈
```

- **补上了「KV Cache 存储」最后一环**：PD 分离解决 Prefill/Decode 分工，CMX 解决 KV Cache 容量
- **生态伙伴**：DDN、Dell、HPE、IBM、NetApp、Supermicro、VAST、Weka 等已跟进（STX 模块化存储基础）

---

## 四、安全能力（In-Silicon Security）

| DOCA 组件 | 能力 |
|:----------|:-----|
| **DOCA Argus** | 零信任文件访问（agentless，硬件强制） |
| **DOCA Vault** | 密钥保护 / 数据加密 |
| **DOCA Flow** | 800Gb/s 网络强制（对应 SAW deny-by-default 出站白名单的硬件执行） |
| 综合 | 威胁检测比纯软件快 **1000x** |

→ 与 SAW 的「网络边界 + 运行时沙箱双重 deny-by-default」形成**硬件级落地**：策略不仅由软件强制，还由 DPU 芯片强制。

---

## 五、在平台五层架构中的位置

```
① 应用层（ToB 场景）
② Agent 层（OpenShell + NemoClaw）
③ 安全层（SAW：凭据代理/审计/人工审查）
④ 推理层（Triton 小模型 + Dynamo 大模型）
   └── KV Cache 不够装？→ CMX（BlueField-4 STX + Spectrum-X）★
⑤ 硬件层（Vera Rubin：CPU/GPU/NVL72）
   └── 节点间高速互联 → ConnectX-9 / BlueField-4（800Gb/s + RDMA）
```

---

## 📌 对平台的意义

1. **卖点升级**：长上下文 Agent + 多 Agent 并发 = KV Cache 容量刚需，CMX 是 NVIDIA 官方答案
2. **组合拳补全**：Dynamo（PD 分离）+ CMX（KV 存储）+ Vera（算力）= 完整推理底座
3. **安全硬件化**：BlueField-4 把 SAW 的策略强制下沉到芯片级（1000x 威胁检测）
4. **ToB 交付**：存储伙伴（DDN/NetApp/VAST/Weka 等）已就绪，可组整体方案

---

## 📚 参考

- NVIDIA CMX 官方页：nvidia.com/en-us/data-center/ai-storage/cmx/
- NVIDIA BlueField-4 官方页：nvidia.com/en-us/networking/products/data-processing-unit/
- NVIDIA 博客：Introducing the NVIDIA BlueField-4-Powered Context Memory Storage Platform
- NVIDIA 博客：Advancing AI Infrastructure for Agentic AI with NVIDIA DOCA In-Silicon Security
