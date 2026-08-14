# KV Cache

## 1. 问题

自回归生成时，每生成一个 token 都需要重新计算之前所有 token 的 K 和 V。

## 2. 解决方案

缓存已计算的 K 和 V，新 token 只需计算自己的 Q、K、V。

### 2.1 无 KV Cache

    生成第 t 个 token：计算 t 次 attention
    总计算量：O(T^2)

### 2.2 有 KV Cache

    生成第 t 个 token：只计算 1 次 attention
    总计算量：O(T)

## 3. 内存占用

    KV Cache 大小 = 2 * num_layers * num_heads * head_dim * seq_len * batch_size

### 3.1 示例

LLaMA 70B, seq_len=2048, batch_size=1:

    2 * 80 * 64 * 128 * 2048 * 1 = 21.5 GB

## 4. 优化技术

| 技术 | 说明 | 节省 |
|------|------|------|
| PagedAttention | 分页管理 | 减少碎片 |
| MQA | 共享 KV 头 | 8x |
| GQA | 分组共享 KV | 4-8x |
| KV Cache 量化 | INT8 存储 | 50% |

## 5. 延伸阅读

- [PagedAttention](paged-attention.md)
- [FlashAttention 详解](flash-attention-detailed.md)

---

*最后更新：2026-06-22*
