# FlashAttention 详解

## 1. 问题

标准注意力需要 O(n^2) 内存存储注意力矩阵，成为长序列的瓶颈。

## 2. 核心思想

通过 IO 感知的分块计算，减少 HBM 访问。

### 2.1 内存层次

| 层级 | 速度 | 容量 |
|------|------|------|
| SRAM | 快 | 小 (几 MB) |
| HBM | 慢 | 大 (几十 GB) |

### 2.2 Tiling

将 Q, K, V 分成小块，加载到 SRAM 计算。

### 2.3 Recomputation

前向时不保存注意力矩阵，反向时重新计算。

## 3. 效果

| 指标 | 标准注意力 | FlashAttention |
|------|-----------|----------------|
| 内存 | O(n^2) | O(n) |
| 速度 | 基线 | 2-4x |
| 精度 | 精确 | 精确 |

## 4. 版本演进

| 版本 | 创新 |
|------|------|
| FlashAttention-1 | 基础版本 |
| FlashAttention-2 | 减少非 matmul FLOPs |
| FlashAttention-3 | 利用 Hopper 架构特性 |

## 5. 延伸阅读

- [FlashAttention 论文](../papers/2022-05-23-flash-attention.md)
- [KV Cache](kv-cache.md)

---

*最后更新：2026-06-22*
