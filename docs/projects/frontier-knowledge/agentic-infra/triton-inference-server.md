# 🚀 NVIDIA Triton Inference Server

> **领域**：Agentic Infra / 推理服务
> **状态**：🟢 已收录 · **更新**：2026-08-10
> **相关**：[Dynamo PD 分离](dynamo-pd-separation.md)（演进关系） · [AI 算法工程师手册](ai-engineer-playbook.md) · [总览](index.md)

---

## 一句话

**Triton Inference Server** 是 NVIDIA 开源的**多框架推理服务框架**（原名 TensorRT Inference Server），用统一的 HTTP/gRPC 接口对外服务各种后端模型（TensorRT / PyTorch / ONNX / vLLM…），是 AI 工厂里「模型 → 服务」的标准承载层，也是 Dynamo 的前身。

---

## 为什么它重要

- **一个端点服务所有模型**：异构模型（不同框架、不同精度）统一入口，客户不用关心底层引擎
- **动态批处理（Dynamic Batching）**：高并发下自动合并请求，吞吐↑ 成本↓
- **多模型并发执行（Concurrent Execution）**：同 GPU 上并行跑多个模型，利用率拉满
- **生产级**：模型版本管理、健康检查、GPU/CPU 异构调度、流式输出（LLM 时代必需）
- **生态标准**：云厂商、DGX、OEM 服务器普遍预装/集成

---

## 核心特性

| 特性 | 说明 |
|:-----|:-----|
| **多后端支持** | TensorRT、PyTorch、ONNX Runtime、TensorFlow、Python、OpenVINO 等 |
| **动态批处理** | 请求合并（max_batch_size / preferred_batch_size 策略） |
| **并发模型执行** | 多模型共享 GPU，各自独立调度 |
| **模型集成/流水线** | Ensemble / 业务流编排（多模型串联） |
| **模型版本管理** | 多版本共存、平滑切换、回滚 |
| **异构部署** | GPU（多卡）/ CPU 统一服务 |
| **协议** | HTTP / gRPC / 流式（Streaming）输出 |
| **性能度量** | Perf Analyzer 压测、指标导出（Prometheus） |

---

## 架构速览

```
客户端 (HTTP/gRPC)
   ↓
Triton Server ── 请求调度 / 动态批处理 / 并发管理
   ├─ Backend: TensorRT（GPU 最优路径）
   ├─ Backend: PyTorch / ONNX / TF
   ├─ Backend: vLLM / SGLang（LLM 场景）
   └─ Backend: Python（自定义逻辑）
   ↓
GPU / CPU 资源池
```

---

## Triton vs Dynamo（演进关系）

**关键认知**：Dynamo 不是和 Triton 并列的另一个选择，而是 **Triton 在 LLM 时代的演进**（NVIDIA 官方：Dynamo 定位为 Triton 的下一代，聚焦 LLM/生成式推理）。

| 维度 | Triton（传统推理服务器） | Dynamo（LLM 推理框架） |
|:-----|:------------------------|:------------------------|
| 定位 | 多框架通用推理服务 | 大模型分布式推理编排 |
| 场景 | CV / 推荐 / 传统 ML / LLM | 长上下文 LLM / Agent 推理 |
| 核心能力 | 动态批处理、多后端、并发 | **PD 分离、KV 缓存管理、智能路由、自动扩缩** |
| 模型 | 短请求为主 | 长生成（Decode 阶段）为主 |
| 部署 | 单机/多机 GPU | AI Factory 规模集群 |
| 关系 | **Dynamo 的前身/基础** | 兼容并继承 Triton 生态 |

> 实践中两者可共存：Triton 继续服务传统模型（embedding / reranker / 多模态小模型），Dynamo 承载大模型推理主线。

---

## 在 SAW / Agentic Infra 中的角色

| 场景 | Triton 的作用 |
|:-----|:--------------|
| **本地推理**（Agent 工作区 VM 内） | 承载轻量模型：embedding、意图分类、小模型工具调用 |
| **路由推理**（企业模型端点） | 作为模型端点服务层：统一协议、批处理、版本管理 |
| **混合推理栈** | Triton（传统模型）+ Dynamo（LLM 主线）分层 |
| **模型端点接入**（SAW 第 7 章） | 9 类受管服务中的「模型端点」走 Triton/Dynamo 路由推理 |

---

## 📌 对 AI 算法工程师的意义

1. **必备技能**：会部署 Triton、配置后端、调动态批处理参数、用 Perf Analyzer 压测
2. **架构选型**：小模型/多模型 → Triton；大模型主线 → Dynamo；混合 → 两者分层
3. **性能优化入口**：批处理策略、并发实例数、TensorRT 引擎化（图优化/FP8）
4. **与安全集成**：模型端点走凭据代理 + 审计，Triton 侧做配额/限流

---

## 📚 参考

- NVIDIA Triton Inference Server 官方文档（github.com/triton-inference-server）
- NVIDIA Dynamo 官方仓库（github.com/ai-dynamo/dynamo）
- 腾讯云 / 阿里云：Triton 部署实践
