# ⚡ Dynamo PD 分离推理优化

> **领域**：Agentic Infra / 推理优化
> **状态**：🟢 已收录 · **更新**：2026-08-12
> **相关**：[PD 分离（原理）](../pd-separation.md) · [AF 分离](../af-separation.md) · [总览](index.md)

---

## 一句话

**NVIDIA Dynamo** 是一个开源、低延迟、模块化的 LLM 推理服务框架——**Triton Inference Server 在 LLM 时代的演进**，核心能力之一就是 **PD 分离（Prefill-Decode Disaggregation）**——把计算密集的 Prefill 和带宽密集的 Decode 拆到不同资源池，各跑各的、互不拖累。

> 🔗 Triton 是什么、与 Dynamo 的详细演进关系 → [Triton Inference Server](triton-inference-server.md)

---

## 核心特性

| 特性 | 说明 |
|:-----|:-----|
| **PD 分离（Disaggregated Serving）** | Prefill 实例与 Decode 实例分离部署，中间经高速网络传 KV Cache |
| **智能路由（Intelligent Routing）** | 按负载/延迟动态调度请求到合适的实例池 |
| **多级 KV 缓存（Multi-tier KV Cache）** | 热门前缀 KV 复用，减少重复 Prefill |
| **自动扩缩（Automatic Scaling）** | 按流量自动伸缩实例数量 |
| **框架兼容** | 与 vLLM / SGLang / TensorRT-LLM 等主流推理引擎集成 |

---

## 🌐 Dynamo 与 vLLM / SGLang / TensorRT-LLM 的关系（关键认知）

### 一句话（Dynamo 官方定义）

> **"Dynamo is the orchestration layer above inference engines — it doesn't replace SGLang, TensorRT-LLM, or vLLM, it turns them into a coordinated multi-node inference system."**
>
> Dynamo 是**推理引擎之上的编排层**——它不替换 vLLM/SGLang/TensorRT-LLM，而是**把它们变成协调的多节点推理系统**。

> "Most inference engines optimize a single GPU or a single node. Dynamo is the orchestration layer above them."
>
> 大多数推理引擎优化**单个 GPU / 单个节点**；Dynamo 在它们**之上**，把 GPU 集群变成协调系统。

### 层次图：不是竞品，是上下层

```
┌──────────────────────────────────────────────┐
│  Dynamo（编排层：跨节点协同）                    │
│  PD 分离 · KV-Aware 路由 · 自动扩缩 · 容错迁移  │
│  ┌────────────────────────────────────────┐  │
│  │ vLLM / SGLang / TensorRT-LLM（引擎层）  │  │
│  │ 实际执行 attention、单机 KV 管理、批处理 │  │
│  │（Dynamo 把它们当 worker 后端调用）       │  │
│  └────────────────────────────────────────┘  │
│               ▼                              │
│          GPU 集群（算力）                      │
└──────────────────────────────────────────────┘
```

> 类比：vLLM/SGLang 是**发动机**，Dynamo 是**车队调度中心**。Dynamo 本身不执行 kernel 计算；Kubernetes 之于 Docker 的编排关系与此同理。

### 相同点

| 维度 | 共同点 |
|:-----|:-------|
| 目标 | 最大化吞吐（tokens/s）、最小化延迟（TTFT/TPOT）、降成本 |
| KV Cache 优化 | 全都做：vLLM 页式 / SGLang 前缀树 / TensorRT-LLM 多级 KV / Dynamo 多级缓存 |
| 能力交集 | 都支持连续批处理、PD 分离、OpenAI 兼容 API |
| 开源 | 都是开源项目（TensorRT-LLM 为 NVIDIA 开源） |

### 不同点

| 维度 | **vLLM**（伯克利/社区） | **SGLang**（斯坦福 LMSYS） | **TensorRT-LLM**（NVIDIA） | **Dynamo**（NVIDIA） |
|:-----|:----------------------|:--------------------------|:--------------------------|:---------------------|
| **定位** | 推理引擎（单实例） | 推理引擎（单实例）+ 结构化生成 DSL | 推理引擎（单实例，C++ 底层、最贴硬件） | **编排框架**（集群级） |
| **优化范围** | 单 GPU / 单节点 | 单 GPU / 单节点 | 单 GPU / 单节点（深度引擎化） | **多节点 / GPU 集群** |
| **标志技术** | PagedAttention（分页 KV） | RadixAttention（前缀树复用） | TensorRT 引擎化（图优化 FP8/INT4 量化、In-Flight Batching） | KV-Aware 路由 + PD 分离编排 |
| **调度粒度** | 请求级（连续批处理） | 请求级 + 前缀感知 | 请求级（Inflight Batching） | **实例级**（请求路由到 KV 所在 worker） |
| **KV 复用范围** | 单机显存内 | 单机显存内（共享前缀极强） | 显存内 + 分页 KV 缓存 | **跨节点**（显存→内存→CMX 存储多级） |
| **特长场景** | 生态最大、模型覆盖广、易用 | 多轮对话/共享前缀、约束解码 | NVIDIA GPU 性能极致、量化部署（FP8/INT4）、生产级硬化 | 长上下文 Agent、多实例协同、容错迁移 |
| **可被 Dynamo 管？** | ✅ 是（官方 backend） | ✅ 是（官方 backend） | ✅ 是（官方 backend） | —（它是管理者） |
| **血缘** | 学界→社区（云厂商标配） | 学界（LMSYS） | NVIDIA 自家（Triton 同门） | NVIDIA（Triton 演进） |

### 官方支持的组合（recipes）

> ⚠️ **注意**：模式（Agg/Disagg）是**配置选择，不绑定引擎**——三种引擎都同时支持两种模式，且多个模型提供 Agg + Disagg 两套配方。下表为 README 顶部代表性示例，完整 catalog 见 Dynamo 仓库 `recipes/` 目录。

| 引擎 | 官方配方（示例） | 模式 |
|:-----|:---------|:-----|
| vLLM | Llama-3-70B（`vllm/agg/`） | Aggregated（聚合） |
| vLLM | Llama-3-70B（`vllm/disagg-multi-node/`） | Disaggregated（PD 分离） |
| vLLM | DeepSeek-R1（`vllm/disagg/`，DEP16 多节点） | Disaggregated（PD 分离） |
| SGLang | DeepSeek-R1（`sglang/disagg-8gpu/`、`disagg-16gpu/`） | Disaggregated（PD 分离 + WideEP） |
| TensorRT-LLM | Qwen3-32B-FP8（`trtllm/agg/`） | Aggregated（聚合） |
| TensorRT-LLM | Qwen3-32B-FP8（`trtllm/disagg/`） | Disaggregated（PD 分离） |
| TensorRT-LLM | DeepSeek-R1（`trtllm/disagg/wide_ep/gb200/`，8 decode+1 prefill 节点） | Disaggregated（PD 分离 + WideEP） |

> 实际用法：`docker run nvcr.io/nvidia/ai-dynamo/sglang-runtime:1.3.0` → 启动 Dynamo frontend + SGLang worker。

### Aggregated vs Disaggregated 模式（选型分析）

| 决策维度 | Aggregated（聚合） | Disaggregated（PD 分离） |
|:---------|:-------------------|:-------------------------|
| 部署形态 | 每个 worker 是完整实例（prefill+decode 一起），Dynamo 做负载均衡路由 | prefill worker 池 + decode worker 池分离，KV Cache 经 NIXL/UCX/RDMA 传输 |
| 硬件需求 | 单节点即可 | 多节点 + 高速网络（IBGDA / UCX / NIXL） |
| 适用模型 | 中型模型、短生成（chat）、单实例装得下 | 超大模型、reasoning（长思维链）、长上下文、MoE |
| 收益 | 部署简单、无 KV 传输开销 | Prefill 堆算力 / Decode 堆带宽各拉满，吞吐↑ TTFT↓ |
| 代价 | Prefill/Decode 互相挤占资源 | 调度复杂、KV 传输跨网络 |

**为什么 reasoning 模型（如 DeepSeek-R1）几乎必选 Disagg**：
```
R1 负载画像：
  Prefill：一次性算完 prompt（算力型，做完就闲）
  Decode：几万 token 思维链慢慢吐（显存带宽型，长时间占 GPU）
两阶段资源需求悬殊 → 拆开各配资源收益巨大
且 R1 是 MLA 架构 → KV Cache 压缩约 57 倍 → 传输成本极低 → Disagg 最大代价被化解
```

**经验法则**：
- 模型大 / 生成长（reasoning）/ 长上下文 / MoE → **Disagg**
- 常规 chat、模型小 → **Agg** 足够，别加复杂度
- 资源允许 → 同一模型提供 Agg + Disagg 两套配方灰度对比（官方玩法）

### 选型建议

| 场景 | 选谁 |
|:-----|:-----|
| 单机单卡部署一个模型 | vLLM 或 SGLang 就够，别上 Dynamo |
| 多轮对话/共享前缀多（Agent 场景） | SGLang（RadixAttention 前缀复用强） |
| 需要结构化生成约束 | SGLang（DSL 是它的独门） |
| 模型多、要易用、生态全 | vLLM |
| **多节点集群、PD 分离、KV 路由、扩缩容、容错** | **Dynamo + vLLM/SGLang 组合** |
| 纯调 API（通义/DeepSeek） | 都不用（供应商已内置） |

---

## 🌙 Dynamo vs Mooncake（殊途同归的两个解法）

**同一道题**：PD 分离后，KV Cache 怎么跨节点高效存取。
**两个切入视角**：Mooncake 从「KV Cache 数据面」切入（KV 是主角），Dynamo 从「推理编排面」切入（引擎是主角）。

### 官方定位对比

| | **Mooncake**（月之暗面） | **Dynamo**（NVIDIA） |
|:--|:------------------------|:---------------------|
| 官方一句话 | "A **KVCache-centric** Disaggregated Architecture for LLM Serving" | "The **orchestration layer above inference engines**" |
| 本质 | LLM 推理/训练的**基础设施**（KV 为中心） | 数据中心级**推理编排栈**（引擎为中心） |
| 论文 | FAST'25 · arXiv:2407.00079（最新 v4 2025-09） | 无独立论文（GTC 发布） |
| 生产验证 | **Kimi 生产平台**：真实负载多处理 **75%** 请求；模拟长上下文场景吞吐 +**525%** | NVIDIA + 云厂商部署 |

### 相同点

| 维度 | 共同做法 |
|:-----|:---------|
| **PD 分离** | 都拆 prefill / decode 集群，中间传 KV Cache |
| **KV 缓存分层** | 都利用显存之外的 CPU 内存/SSD 建分布式 KV 池（Mooncake 叫 Store，Dynamo 叫 multi-tier KV caching） |
| **RDMA 传输** | 都用 RDMA 做高速 KV 搬运 |
| **不替代引擎** | 都集成 vLLM / SGLang（Mooncake：vLLM 官方博客推荐 Mooncake Store；Dynamo：官方 backend） |
| **开源** | 都是开源项目 |
| **调度智能** | 都做「请求去哪儿」的全局决策（全局调度器 / KV-aware 路由） |

### 不同点

| 维度 | **Mooncake** | **Dynamo** |
|:-----|:------------|:-----------|
| **核心抽象** | **KV Cache 是一等公民**——调度/驱逐/迁移的对象是 KV 对象（Tensor） | **请求/worker 是一等公民**——调度对象是请求，KV 只是路由依据 |
| **组件构成** | Transfer Engine（传输）+ Mooncake Store（KV/权重存储）+ EP/PG（MoE 执行） | 前端路由 + PD 分离 + 多级 KV 缓存 + 自动扩缩 + 容错迁移 |
| **范围** | 推理 **+ 训练**（RL 权重同步、TorchSpec、DSpark 在线训练） | 聚焦**推理服务**（LLM/reasoning/多模态/视频生成） |
| **抢占策略** | **KVCache 驱逐/迁移**替代请求抢占（cache-centric preemption） | 金丝雀健康检查 + **进行中请求迁移** |
| **硬件绑定** | 多硬件：CUDA / NPU / MUSA / EFA / 国产芯片（Hygon、Biren） | NVIDIA 全家桶（GPU + Spectrum-X + CMX 深度绑定） |
| **过载策略** | **预测式早期拒绝**（prediction-based early rejection，超载时主动拒掉低价值请求保 SLO） | 自动扩缩 + 排队调度（以扩容消化过载） |
| **生态深度** | 与 SGLang 深度集成（HiCache 多级 KV、P2P 权重 7x 加速、多模态 embedding 缓存） | 官方三引擎 backend + GAIE 网关集成 |

### 关键关系：控制面 vs 数据面（甚至可以组合）

```
Dynamo（编排：谁去哪台 worker）        ← 控制面
   ↓ 管理
vLLM / SGLang（引擎：实际算 attention）
   ↓ 存储/传输
Mooncake Store + TE（KV 池：RDMA 存取） ← 数据面
   或
CMX（NVIDIA 自家 KV 存储方案）
```

- Dynamo 管「调度」、Mooncake 管「KV 存取」——一个是控制面，一个是数据面
- 现实中各自闭环：NVIDIA 用自家 CMX，Moonshot 生态用 Mooncake Store
- 开源层面**没有冲突**：Mooncake 已被 vLLM/SGLang 官方收录为后端，Dynamo 也认这两个引擎

### 白话总结

| 问法 | 答案 |
|:-----|:-----|
| 它俩抢生意吗？ | **不直接抢**——一个卖「仓库+物流」（Mooncake），一个卖「车队调度系统」（Dynamo） |
| 为啥长这么像？ | 都要解决 PD 分离后的 KV 传输/存储问题，殊途同归 |
| 谁更底层？ | Mooncake 更底层（含传输、存储引擎、MoE 执行）；Dynamo 更高层（编排引擎） |
| 谁更封闭？ | Dynamo 绑 NVIDIA 硬件；Mooncake 跨硬件（NPU/国产芯片都支持） |
| 对国内用户？ | Mooncake 生态更友好（月之暗面 + 国产硬件 + vLLM/SGLang 官方集成） |

---

## PD 分离的核心权衡

```
Prefill 池（算力型） → KV Cache 传输 → Decode 池（带宽型） → 输出
```

⚠️ **关键约束**：KV Cache 传输量很大，没有高速网络（RDMA 等）时传输会成为新瓶颈。

> 🔗 原理细节（Prefill/Decode 负载差异、TTFT/TPOT、DistServe/Mooncake）→ [PD 分离（原理）](../pd-separation.md) · [AF 分离](../af-separation.md)

---

## 部署形态（国内已有实践）

- **腾讯云**：Dynamo PD Separation Guide（部署指南）
- **阿里云 ACK**：云原生 AI 套件支持部署 Dynamo PD 分离推理服务
- **CSDN NVIDIA 社区**：Dynamo 技术解读

说明 ToB 场景下 PD 分离推理已从论文走向生产落地，是**可交付的成熟方案**。

---

## 📌 对平台的意义

- **卖点**：Token 成本 / 延迟优化是 ToB 客户最直接的 ROI
- **组合**：Dynamo（推理）+ Sandbox（安全）是「跑得快 + 跑得稳」的组合拳
- **路径**：可在 Vera 平台上预集成 Dynamo，形成「开箱即用」的 Agentic Infra 方案

---

## 📚 参考

- NVIDIA Dynamo 官方文档（github.com/ai-dynamo/dynamo）
- 腾讯云：Dynamo PD Separation Guide
- 阿里云 ACK：部署 Dynamo PD 分离推理服务
- MagicNetWorld：大模型推理部署解剖（PD/AF 分离原理）
