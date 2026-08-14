# ⚡ PD 分离（Prefill-Decode Disaggregation）

> **领域**：大模型部署 / 推理架构
> **状态**：🟢 已收录 · **更新**：2026-08-07
> **相关**：[AF 分离 →](af-separation.md)

---

## 一句话

**PD 分离 = Prefill-Decode Disaggregation**：把推理的两个阶段（预填充与解码）分开部署到不同的 GPU 集群，各按负载特征配比资源。

---

## 背景：推理不是一种负载，而是两种

一次推理请求分两个阶段，资源特征完全不同：

| 阶段 | 计算形态 | 资源瓶颈 |
|:-----|:---------|:---------|
| **Prefill（预填充）** | 矩阵-矩阵乘（并行处理 prompt 全部 token，算 KV、生成第一个 token） | **计算密集型**——GPU 算力（FLOPS）是瓶颈，显存带宽大量闲置 |
| **Decode（解码）** | 矩阵-向量乘（逐 token 生成，每步读一遍全部权重） | **显存带宽密集型**——算力大量闲置 |

对应的用户体验指标：
```
TTFT（首 token 延迟） ≈ Prefill 耗时  → 用户"等多久才开始出字"
TPOT（每 token 耗时） ≈ Decode 单步耗时 → 用户"出字流不流畅"
```

### 混部的问题

把两种负载塞在同一批 GPU 上：
- 按 Prefill 配资源 → Decode 阶段算力浪费
- 按 Decode 配 → Prefill 排队
- 长 prompt 的 Prefill 会突然插队，拉高所有人正在进行的 Decode 延迟
- **吞吐和延迟两头都做不好**

---

## PD 分离怎么做

```
用户请求 → Prefill 集群（堆算力） → KV Cache 经高速网络 → Decode 集群（堆显存带宽） → 输出
```

Prefill 节点算完 KV Cache 后，通过高速网络把 KV 传给 Decode 节点接力生成。

### 独立优化空间

| 优化点 | 说明 |
|:-------|:-----|
| **独立配比** | Prefill 池堆算力、Decode 池堆显存和带宽，资源利用率各自拉满 |
| **独立调度** | TTFT 和 TPOT 分别做 SLA 保证（DistServe 论文核心贡献：证明分离部署能在同等资源下服务更多请求且不违约延迟目标） |
| **KV 缓存分层** | Moonshot 的 Mooncake 架构把 KV Cache 池化共享，热门前缀（系统提示词、多轮对话历史）的 KV 直接复用、连 Prefill 都省掉，缓存命中率达 90% 量级 |

### 代价

- **KV 传输开销**：长上下文的 KV 动辄几十 GB
- **调度复杂度**：跨集群调度、路由、容错
- 💡 **MLA 架构有结构性优势**：要传的 KV 小约 57 倍（DeepSeek 系）

---

## 演进路线（为什么还要 AF 分离）

```
单卡部署 → 分布式 → PD 分离 → 大 EP（专家并行）→ Attention 与 FFN 分离（AF 分离）
```

PD 分离按「阶段」拆，是当前主流部署形态；AF 分离按「算子」拆，是进一步细化方向。

---

## 📚 参考

- DistServe（PD 分离的 SLA 分析）：arXiv:2401.09670
- Mooncake（KV 缓存分层）：Moonshot 架构
- MagicNetWorld 解读：大模型推理部署解剖（2026-07-24）
