# 🧩 推理链路全景与开源选型（Inference Stack Landscape）

> **领域**：Agentic Infra / 推理架构
> **状态**：🟢 已收录 · **更新**：2026-08-12
> **相关**：[Dynamo PD 分离](dynamo-pd-separation.md) · [Triton Inference Server](triton-inference-server.md) · [网络层 CMX/BlueField](network-layer.md) · [智能路由系统](../../../smart-router/index.md)

---

## 一句话

一套完整的 LLM 推理服务 = **五层链路**（路由 → 编排 → 引擎 → KV 存储 → 硬件）。每一层都有成熟的开源或自研方案，可以像乐高一样拼出**全开源**的完整链路。

---

## 一、五层链路全景

```
用户请求
   ↓
① 网关/路由层  ── 决策：选哪个模型？（难度评估 / 类型分类 / 成本优化）
   ↓
② 编排层      ── 调度：请求去哪台 worker？（PD 分离 / KV 路由 / 扩缩容）
   ↓
③ 推理引擎层  ── 执行：实际算 token（attention / KV 管理 / 批处理）
   ↓
④ KV 存储层   ── 存取：跨节点 KV Cache（复用 / 传输 / 加密）
   ↓
⑤ 硬件层      ── 算力：GPU 集群（NVIDIA / 国产卡）
```

---

## 二、每层对应的开源 / 自研方案

### ① 网关/路由层（决策：选哪个模型）

| 方案 | 类型 | 定位 |
|:-----|:-----|:-----|
| **smart-router（自研）** ⭐ | 自研 | **差异化核心**：难度评估、类型分类、Benchmark 感知、成本优化 |
| LiteLLM | 开源 | 统一代理：100+ 供应商适配、密钥管理、限流、预算控制 |
| Higress AI Gateway | 开源（阿里） | K8s 原生 AI 网关，与 Istio 生态集成 |

> 与 LiteLLM 的关系见下方「拼装规则 · 坑 3」（决策器 vs 执行器，可二选一或分层）。

### ② 编排层（调度：请求去哪台 worker）

| 方案 | 类型 | 定位 |
|:-----|:-----|:-----|
| **NVIDIA Dynamo** ⭐ | 开源（NVIDIA） | 编排 vLLM/SGLang/TRT-LLM；PD 分离、KV-Aware 路由、自动扩缩、容错 |
| KServe | 开源 | K8s 生产级模型服务平台（A/B、推理图、多引擎托管） |
| Ray Serve | 开源 | 分布式部署平台，Python 生态友好 |

### ③ 推理引擎层（执行：实际算 token）

| 方案 | 类型 | 特色 |
|:-----|:-----|:-----|
| **vLLM** | 开源 | 生态最大、模型覆盖广、易用 |
| **SGLang** | 开源（斯坦福 LMSYS） | RadixAttention 前缀复用、结构化生成 DSL、国产卡支持 |
| **TensorRT-LLM** | 开源（NVIDIA） | NVIDIA GPU 性能极致、FP8/INT4 量化 |

### ④ KV 存储/传输层（跨节点 KV Cache）

| 方案 | 类型 | 定位 |
|:-----|:-----|:-----|
| **Mooncake Store + TE** | 开源（月之暗面） | KV 池 + RDMA 传输引擎，支持 CUDA/NPU/国产卡 |
| **Dynamo 内置多级缓存** | 开源（NVIDIA） | L1 显存 / L2 CPU 内存 / 跨节点，无需额外组件 |
| CMX | 商业（NVIDIA） | pod 级 KV 存储平台（BlueField-4 + DOCA Memos + Spectrum-X） |

### ⑤ 硬件层（算力）

| 方案 | 类型 | 说明 |
|:-----|:-----|:-----|
| NVIDIA GPU | 商业 | H100 / H200 / GB200（Dynamo 路线必备） |
| 国产卡 | 商业 | Ascend / Hygon / Biren（Mooncake 路线支持） |

---

## 三、两套标准拼法（别混搭）

### 🟦 拼法一：NVIDIA 全家路线（NVIDIA GPU）

```
smart-router（自研决策）
   → Dynamo frontend（OpenAI 兼容入口 + KV-aware 路由）   ✅ 官方支持
   → vLLM / SGLang / TensorRT-LLM worker（Dynamo backend） ✅ 官方支持
   → NVIDIA GPU 集群
   （KV 层：Dynamo 内置多级缓存；如需 pod 级存储 → CMX 商业可选）
```

### 🟩 拼法二：开源中立路线（国产硬件友好）

```
smart-router（自研决策）
   → SGLang / vLLM（OpenAI 兼容入口）                     ✅ 官方支持
   → Mooncake Store + TE（KV 池 + RDMA）                   ✅ SGLang/vLLM 官方集成
   → GPU / NPU / 国产卡集群
```

### 兼容性评级

| 拼法 | 兼容性 | 说明 |
|:-----|:-------|:-----|
| 拼法一 | ✅✅✅ | Dynamo 官方 recipes 即此形态，kubectl apply 可跑 |
| 拼法二 | ✅✅✅ | SGLang 集成 Mooncake TE/HiCache，vLLM 官方博客推荐 Mooncake Store |

---

## 四、拼装规则（三个坑）

### 坑 1：Dynamo 和 Mooncake 不要混着拼 ❌

```
Dynamo（KV 走 NIXL/UCX + 路由到 CMX 池）
   + Mooncake（另一套 KV 池协议）  → 两套 KV 体系打架，路由冲突
```

- Dynamo 路线的 KV 层：CMX（商业）或 Dynamo 自带多级缓存
- Mooncake 路线的 KV 层：Mooncake Store
- **二选一，别叠。**

### 坑 2：Dynamo 目前只支持 NVIDIA GPU

Dynamo 官方 recipes 全是 H100/H200/GB200。用国产卡只能走**拼法二**。

### 坑 3：smart-router 与 LiteLLM——「决策器 vs 执行器」（修正认知）

两者**不是两个路由器抢一个位置**，而是可以二选一或分层：

| | smart-router（决策器） | LiteLLM（执行器） |
|:--|:----------------------|:------------------|
| 独有能力 | 难度评估、类型分类、Benchmark 感知 | 供应商适配、密钥管理、预算控制 |
| 重叠能力 | 重试、成本追踪 | 重试、成本追踪 |

**形态 A（全自研）**：smart-router 自带统一客户端 → 不需要 LiteLLM
```
smart-router（决策 + 自写 AliyunClient/DeepSeekClient） → 通义/DeepSeek API
```
适合：只接国内 3 家模型，不想多一个组件。

**形态 B（分层）**：smart-router 只做决策，LiteLLM 做执行
```
smart-router（难度评估 → 输出选定模型名） → LiteLLM（转发/适配/key 管理） → 各 API
```
适合：以后要接几十家海外模型，不想每次加供应商都写代码。

**选择标准**：维护成本 vs 组件数量权衡——模型供应商少选 A，多选 B。

---

## 五、smart-router 在链路中的两种定位

| 路线 | 链路 | 硬件需求 |
|:-----|:-----|:---------|
| **API 网关路线** | smart-router → 云 API（通义/DeepSeek/智谱） | 无 GPU，纯软件 |
| **自建集群路线** | smart-router → Dynamo（或 SGLang+vLLM）→ Mooncake → GPU | 需要 GPU 集群 |

两条路线的 smart-router 逻辑完全一致（难度评估/成本/重试），只是后端从「云 API」换成「自建端点」——**OpenAI 兼容协议让切换成本几乎为零**。

---

## 六、最小验证路径（先跑通再上规模）

| Step | 链路 | 验证点 | 硬件 |
|:----:|:-----|:-------|:-----|
| 1 | smart-router → 云 API | 路由决策逻辑（难度/成本/重试） | 无 GPU |
| 2 | smart-router → Dynamo（agg）→ vLLM | Dynamo frontend OpenAI 兼容接入 | 1× GPU |
| 3 | smart-router → Dynamo（disagg）→ vLLM/SGLang | PD 分离 + KV 路由 | 多节点 GPU |
| 4 | 加 KV 存储层 | Mooncake（拼法二）或 CMX（拼法一） | 多节点 + RDMA |

每步有清晰验证点，不依赖商业组件。

---

## 七、组件矩阵（一键查看）

| 链路层 | 开源首选 | 自研/商业 | 接口标准 |
|:------|:---------|:----------|:---------|
| ① 路由 | LiteLLM / smart-router | **smart-router（自研差异化）** | OpenAI 兼容 |
| ② 编排 | Dynamo / KServe | — | OpenAI 兼容 frontend |
| ③ 引擎 | vLLM / SGLang / TRT-LLM | — | OpenAI 兼容 |
| ④ KV 存储 | Mooncake / Dynamo 内置 | CMX（商业可选） | 各方案私有协议 |
| ⑤ 硬件 | — | NVIDIA / 国产卡（商业硬件） | — |

---

## 📌 关键结论

1. **全链路可 100% 开源**（除 CMX 为可选商业项，也可用开源替代）
2. **接口统一为 OpenAI 兼容协议**（①↔②↔③ 之间天然互通）
3. **自研点只有一个**：smart-router（难度感知路由是差异化，其他全是现成积木）
4. **最难的不是拼装，是 K8s 运维**（GPU 调度、网络、监控）

---

## 📚 参考

- NVIDIA Dynamo 官方仓库（github.com/ai-dynamo/dynamo，recipes 目录）
- LiteLLM（github.com/BerriAI/litellm）
- KServe（github.com/kserve/kserve）
- Mooncake（github.com/kvcache-ai/Mooncake）
- 智能路由系统：[../smart-router/index.md](../../../smart-router/index.md)
