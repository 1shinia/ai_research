# ⚙️ AF 分离（Attention-FFN Disaggregation）

> **领域**：大模型部署 / 推理架构
> **状态**：🟢 已收录 · **更新**：2026-08-07
> **相关**：[PD 分离 →](pd-separation.md)

---

## 一句话

**AF 分离 = Attention-FFN Disaggregation**：在 PD 分离（按推理阶段拆）的基础上，进一步按**算子类型**把 Attention 层和 FFN/Expert 层物理分离部署，做更细粒度的资源调配。

---

## 为什么还要拆算子

PD 分离解决了 Prefill 和 Decode 的负载差异，但每个阶段内部仍混着两类算子，它们的访存/计算特征也不同：

| 算子 | Prefill 阶段特征 | Decode 阶段特征 |
|:-----|:-----|:---------|
| **Attention（注意力）** | 计算+显存双高：N² 的 attention score + QKV 激活，算力和带宽都是瓶颈 | 带宽瓶颈：KV Cache 占用大显存，每次只算 1 个 token，访存 dominated |
| **FFN / Expert（前馈/专家）** | 算力瓶颈：O(N·d²) 的 GEMM，纯计算密集 | 算力瓶颈：每次 O(d²) 矩阵乘，计算密度高 |

计算复杂度：N 指序列长度（context length），d 指隐藏维度（hidden dimension）

- **Attention**：
  - Prefill：计算复杂度 O(N² · d)，KV Cache 显存占用 O(N · d)
  - Decode：每步 O(1)（自回归），但每步仍要读写 KV Cache
  - 瓶颈不在"纯计算量"，而在**KV Cache 的高带宽读写**（带宽 bound）
- **FFN**：
  - 计算复杂度 O(N · d_ff) ≈ O(N · d²)
  - 随 N 线性增长，但每层都是密集矩阵乘（计算 bound）
  - 天然适合堆算力、跑大 batch

### 为什么对 MoE 模型特别有吸引力

MoE（混合专家）模型的 FFN 部分是大量稀疏专家，天然适合做**专家并行（EP）**；而 Attention 部分做数据并行/张量并行即可。AF 分离让两类算子各跑在最优的硬件配置上。

---

## AF 分离 vs PD 分离

| 维度 | PD 分离 | AF 分离 |
|:-----|:--------|:--------|
| **拆分维度** | 按**推理阶段**（Prefill / Decode） | 按**算子类型**（Attention / FFN） |
| **解决什么** | 计算密集型 vs 带宽密集型的阶段错配 | PD 分离内部的算子资源错配 |
| **成熟度** | 主流部署形态，生产验证充分 | 业界前沿探索，工程复杂度更高 |
| **硬件匹配** | Prefill 池堆算力、Decode 池堆带宽 | Attention 节点偏显存带宽、FFN 节点偏算力/大 batch |
| **通信开销** | KV Cache 跨集群传输（数十 GB） | 算子间激活值传输，需高频同步 |

---

## 演进全景（部署形态的拆分解）

```
单卡部署
  └─→ 分布式（张量/流水线并行）
        └─→ PD 分离（按阶段拆）★ 当前主流
              └─→ 大 EP（专家并行，MoE 规模化）
                    └─→ AF 分离（按算子拆）★ 前沿探索
                          └─→ micro-batch 流水线（按时间拆，如 DualPipe）
```

推理部署形态从「单卡 → 分布式 → PD 分离 → 大 EP → Attention 与 FFN 分离」逐层细化，本质是**把拆分粒度逼近硬件特征的本质差异**。

---

## 配套技术：micro-batch 流水线 / DualPipe

- 用 **micro-batch（微批量）** 把请求切成小片，让不同阶段的算子同时跑在不同设备上
- **DualPipe 双向流水线**（DeepSeek）把通信藏进计算里——前向与反向的通信和计算重叠，降低流水线气泡
- 属于「按时间拆」，与 PD/AF 的「按空间拆」互补

---

## 📚 参考

- MagicNetWorld 解读：大模型推理部署解剖——PD 分离、AF 分离，和 micro-batch 流水线（2026-07-24）
- DeepSeek DualPipe 双向流水线
- 知乎：LLM 推理提速——Attention 与 FFN 分离（AFD）方案解析
