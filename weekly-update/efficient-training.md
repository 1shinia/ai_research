# ⚡ 高效训练与推理 (Efficient Training & Inference)

> 本周候选：20 篇 | 筛选高影响力：4 篇

---

## 1. DSpark: Confidence-Scheduled Speculative Decoding for Production LLM Serving

**📄 arXiv：** [2607.07658](https://arxiv.org/abs/2607.07658v1) | **📅 发布日期：** 2026-07-08  
**👥 作者：** Yu Zhang, Yan Liang, Tengxuan Chen, Xiaogang Ma, Wenjie Yang（DeepSeek）

### 一句话总结
DeepSeek 团队提出生产级投机解码框架，通过置信度自适应的草稿-验证调度结合两步流水线部署，在 DeepSeek-V4 服务上实现 60-85% 端到端加速。

### 核心思想
现有投机解码研究假设「草稿模型可随意部署」，但生产环境受限多：草稿和目标共享前缀，草稿解码受限于目标的前向速度。DSpark 的三大创新：(1) **置信度调度**——目标模型高速验证的同时计算草稿 token 的置信度，置信度高时跳过后验修正；置信度不足时修正。(2) **两步调度流水线**——CPU/GPU 分别执行不同阶段，消除 pipeline bubble。(3) **KV 预加载**——利用前缀缓存减少草稿加载延迟。

### 为什么重要
这不是又一个投机解码论文，而是**DeepSeek 生产环境的实战记录**——60-85% 的端到端加速已经在 DeepSeek-V4-Pro 和 DeepSeek-V3-Light 部署上线。对你有直接参考价值——如果你要部署 DeepSeek-V4-Pro 在 AMD 集群上，DSpark 的方案可以复现。

### 关键实验
- DeepSeek-V4-Pro 线上加载：端到端加速 60-85%
- AIME 2025 准确率无损（93.2% vs 94.0% 恢复修正后相同）
- 两步调度流水线消除显存碎片和 bubble

---

## 2. TriRoute: Unified Learned Routing for Joint Adaptive Attention, Experts, and KV-Cache Allocation

**📄 arXiv：** [2607.06601](https://arxiv.org/abs/2607.06601v1) | **📅 发布日期：** 2026-07-07  
**👥 作者：** Andrii Balashov, Olena Ponomarova

### 一句话总结
用单一轻量控制器联合决定每 token 的注意力模式（跳过/局部/全局）、FFN 专家选择和 KV Cache 位宽——在计算/显存约束下 Pareto 统治独立优化的 MoD+MoE+KV 量化组合。

### 核心思想
MoE（稀疏 FFN）、MoD（跳过 Transformer 层）、KV 量化各自独立优化一个维度，但三者本质上耦合——需要全注意力的 token 通常也需要高精度缓存。TriRoute 用一个轻量控制器在每层每 token 输出联合策略。端到端通过异质松弛技术训练（Gumbel-Softmax + straight-through + load-balanced top-k），并设计跨轴耦合控制避免路由坍塌在轴间传播。

### 为什么重要
这是第一批系统研究**多轴联合稀疏化**的工作。独立优化 MoE/MoD/KV 各自只能吃到一半的红利，联合优化才能吃到全部。对设计下一代高效 Transformer 架构有直接架构指导意义。

### 关键实验
- 160M-1.3B 参数模型，compute-optimal token 计数
- Pareto 统治最佳独立 MoD+MoE+KV 量化组合
- 控制器在句子起始位置、稀有子词、命名实体上分配全注意力和高精度缓存

---

## 3. Fractal KV-Cache Archives: Efficient KV Cache Compression via Symbolic Storage

**📄 arXiv：** [2607.05722](https://arxiv.org/abs/2607.05722v1) | **📅 发布日期：** 2026-07-06  
**👥 作者：** Abdelmumin Abulgasim

### 一句话总结
将 KV Cache 的压缩重新定义为符号存储问题——用上下文相关的符号嵌入替代浮点值，通过可逆存档结构和步进式调度实现 36-54x 有效压缩比。

### 核心思想
传统 KV Cache 压缩方法把压缩当作数值问题（量化、剪枝）。本文将其重新定义为**符号存储问题**：将 KV 状态映射到任务相关的符号空间，利用符号嵌入的高信息密度大幅压缩存储。设计可逆的存档结构保证压缩前后信息损失可控，配合步进式在线调度算法在推理过程中动态替换冷/热符号。

### 为什么重要
KV Cache 已成为长上下文推理的主要瓶颈。36-54x 的压如果与高效三倍于现有方法，且符号化存储使缓存更具语义可解释性——知道缓存了什么「概念」而非一堆浮点数。

### 关键实验
- 36-54x 有效压缩比（vs 典型方法的 4-8x）
- Pile-test 和长上下文基准上保持逼近无损
- 可逆存档确保关键信息不丢失

---

## 4. BlockServe: Efficient Block-Grained Batching for Diffusion Large Language Models

**📄 arXiv：** [2607.08374](https://arxiv.org/abs/2607.08374v2) | **📅 发布日期：** 2026-07-09  
**👥 作者：** Yiheng Wang, Saifei Liao, Weiyu Feng

### 一句话总结
提出面向扩散 LLM（非自回归）的块粒度批处理机制，通过块级注意力预计算和动态序列池化，实现 1.9-10.6x 的服务吞吐提升。

### 核心思想
扩散 LLM（如 MDLM/Diffusion-LLM）用非自回归生成替代逐 token 解码，但由于序列并行化和不确定性步数，传统的连续批处理技术无法直接适用。BlockServe 将相似状态的序列聚合成块，一次性处理整个块的注意力预计算，并通过动态序列池化管理进度差异。块粒度规划器决定不同序列的最佳批处理配置。

### 为什么重要
扩散 LLM 是自回归的潜在替代方案，但一直缺乏配套的服务基础设施。该工作为扩散 LLM 的实用化部署填补了工具空白，1.9-10.6x 的吞吐提升意味着扩散 LLM 在服务端变得可行。

### 关键实验
- 1.9-10.6x 服务吞吐提升
- 与扩散步数和序列数的扩展性分析
- 块粒度 vs 传统 sample-level batching 对比

---

> ⏳ 暂存于 weekly-update/，等待主人手动选择后归档到 papers/ 对应分支。
