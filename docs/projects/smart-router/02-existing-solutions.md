# 现有方案分析

> 首次调研日期：2026-07-01 | 状态：🟢 已完成 | 最后更新：2026-08-12

---

## 1️⃣ RouteLLM — UC Berkeley (lm-sys)

**类型**：学术研究 → 开源框架  
**论文**：[RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665) (ICLR 2025)  
**GitHub**：https://github.com/lm-sys/RouteLLM  
**作者**：Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M Waleed Kadous, Ion Stoica

### 核心理念

在 **两个** LLM（一个强/贵、一个弱/便宜）之间动态路由。目标是用强模型 **95% 的性能** 只花 **~50% 的成本**。

训练路由器模型用的是 **Chatbot Arena 的人类偏好数据** + 数据增强技术。路由器本质上是一个二分类器：判定当前问题是否值得调用强模型。

### 四种路由策略

| 策略 | 工作原理 | 训练需求 | 特点 |
|:----|:---------|:--------:|:-----|
| **Similarity Weighting** | 将用户 query Embedding 与历史数据做余弦相似度加权 | ❌ 无需训练 | 最轻量，适合快速验证 |
| **Kernel-based** | 用偏好数据的核函数估计调用强模型的概率 | ✅ 需偏好数据 | 效果好、可扩展，是推荐方案 |
| **Classification** | 训练一个二分类器（基于 BERT 等）直接做路由决策 | ✅ 需训练 | 准确率最高，但维护成本也高 |
| **Matrix Factorization** | 协同过滤思路——用户×模型隐因子分解 | ✅ 需训练 | 适合有个性化场景，但冷启动有挑战 |

### 论文核心发现

- 偏好数据比 GPT-4 打分数据更适合训练路由器
- 数据增强（golden dataset + random弱模型数据）显著提升路由精度
- 在 MT-Bench 和 MMLU 等基准上，可实现 **95% 强模型性能 + 50% 成本节约**

### 评价

| ✅ 优点 | ❌ 局限 |
|:--------|:--------|
| 开源且 ICLR 论文支撑 | 仅支持两模型（强 vs 弱），不是多模型路由 |
| 策略多样（4种） | 仅支持 LLM，不支持 T2I/T2V/Embedding/Reranker |
| 偏好数据方法论扎实 | 需收集偏好数据才能达到最佳效果 |
| 训练框架完整 | 路由决策是"二选一"，缺乏弹性 |

---

## 2️⃣ LLMRouter — UIUC ULab ⭐（千星项目）

**类型**：学术研究 → 开源框架  
**GitHub**：https://github.com/ulab-uiuc/LLMRouter  
**官网**：https://ulab-uiuc.github.io/LLMRouter/  
**发布时间**：2026年2月  
**安装**：`pip install llmrouter-lib`

### 核心理念

一个 **统一的路由框架**——不是一种方案，而是 16+ 种路由策略的工具箱。它把路由抽象为"给一个 query 分配最佳模型"的问题，并提供 CLI、API、插件扩展。

### 路由策略体系（4 大类 × 16+ 子策略）

#### 🔹 单轮路由（Single-Round Routers）—— 一次请求选一个模型

| 策略 | 原理 | 特点 |
|:----|:------|:------|
| **KNN Router** | 基于历史 query-模型匹配做 K 近邻 | 简单直观，完全无训练 |
| **SVM Router** | 用 SVM 分类器做模型选择 | 传统 ML 方法，训练快 |
| **MLP Router** | 多层感知机预测最佳模型 | 能学到非线性决策边界 |
| **Elo Score Router** | 用 Elo 评分体系给模型排序 | 类似竞技游戏的排位机制 |
| **Matrix Factorization Router** | 类似协同过滤，query×模型隐因子 | 能发现隐式关联 |
| **Contrastive Router** | 对比学习 query-模型表示 | 表示学习能力强 |
| **Graph Router** | 用图结构建模 query-模型关系 | 适合复杂关系推理 |
| **HybridLLM Router** | 混合模型级联路由 | 借鉴 HybridLLM 思路 |
| **CausalLM Router** | 用因果语言模型做路由 | 新兴方法，探索中 |

#### 🔹 多轮路由（Multi-Round Routers）—— 对话中动态切换

| 策略 | 原理 | 特点 |
|:----|:------|:------|
| **Router-R1** | 强化学习多轮推理路由 | 在对话过程中感知上下文变化切换模型 |

#### 🔹 个性化路由（Personalized Routers）—— 因用户而异

| 策略 | 原理 | 特点 |
|:----|:------|:------|
| **GMT Router** | 图 Meta-learning 学习用户偏好 | 能根据用户行为自动调整 |

#### 🔹 智能体式路由（Agentic Routers）—— 路由作为 Agent

| 策略 | 原理 | 特点 |
|:----|:------|:------|
| **KNN Multi-Round** | KNN 在多轮中的扩展 | 记忆上下文 |
| **LLM Multi-Round** | 让 LLM 自己决定谁来答 | 灵活性最高 |

### 插件系统

LLMRouter 支持自定义路由器——写一个 Python 类，实现 `router()` 接口，注册到框架即可通过 CLI 调用。

### 内置数据管道

内置 11 个 benchmark 的数据集，可以直接生成训练数据、自动评估路由策略效果。

### 评价

| ✅ 优点 | ❌ 局限 |
|:--------|:--------|
| 16+ 策略，覆盖最全 | 仅支持 LLM 类型模型 |
| 插件系统，可扩展性极强 | 框架较新，社区生态还在发展 |
| 内置数据管道和评估 | 上手需一定学习成本 |
| 支持 CLI 和 Python API | 不支持多模态模型类型 |
| 统一的训练→推理→评估流程 | 无 Retry 机制 |

---

## 3️⃣ OpenRouter — 商业产品

**类型**：商业 SaaS  
**官网**：https://openrouter.ai  
**核心定位**：统一 LLM API 网关

### 功能特点
- 100+ 模型的统一 API 接口
- Provider 自动路由（故障转移 → 负载均衡 → 成本优化）
- 模型输出归一化
- 边缘基础设施降低延迟
- 用量监控和日志

### 评价

| ✅ 优点 | ❌ 局限 |
|:--------|:--------|
| 生产级，稳定可靠 | 闭源，路由策略黑盒 |
| 故障转移保障高可用 | 仅支持 LLM API |
| 开箱即用 | 有被 Provider 封禁的风险 |
| 多 Provider 负载均衡 | 无法自定义路由逻辑 |

---

## 4️⃣ AI Gateway / LLM Gateway 生态

### Portkey AI Gateway
- **定位**：开源 AI Gateway
- **GitHub**：https://github.com/Portkey-AI/gateway
- **功能**：200+ 模型、负载均衡、fallback、缓存、可观测性
- **语言**：Node.js
- **评价**：适合生产环境，但路由策略偏基础（多 Provider 分发），无智能路由

### MLflow AI Gateway (Databricks)
- **定位**：统一模型服务接口
- **支持**：LLM + Embedding + 多模态
- **集成**：MLflow 生态（实验管理 + 模型注册 + 部署）
- **评价**：生态完善，但偏 MLOps 平台，不是独立的路由系统

### K8s Inference Gateway
- **定位**：Kubernetes 原生推理网关
- **功能**：模型名路由、KV Cache 亲和性调度、自动扩缩容
- **评价**：纯云原生方案，需要 K8s 基础设施，路由策略基础

### Azure API Management + AI Gateway
- **定位**：企业级 AI 网关
- **功能**：策略驱动路由、安全、监控、限流
- **评价**：Azure 绑定，封闭生态

---

## 5️⃣ 中文生态方案

### 百度智能云 · 多模型 Router
- 基于任务类型（文本/图片/语音等）的模型选择
- 内置成本-性能平衡策略
- 国内生态友好，支持文心系列、第三方模型

### 腾讯云 · 多模型 Router
- 多模型路由策略（基于模型名称、版本）
- 灰度发布 + A/B 测试
- 监控 + 日志 + 告警

### 知乎 · LLMOps 系列
- LLMOps 与模型路由策略深度分析
- 实践指南、技术选型对比

---

## 6️⃣ OpenSquilla / SquillaRouter ⭐（2026-08-12 新增分析）

**类型**：开源 AI Agent（内含生产级本地模型路由器）
**GitHub**：https://github.com/opensquilla/opensquilla（6.5k+ stars, Apache-2.0, Python 3.12+, 稳定版 0.5.2）
**技术报告**：[Agentic Routing: The Harness-Native Data Flywheel](https://arxiv.org/abs/2607.11399)（arXiv 2026-07-13）
**网站**：https://opensquilla.ai/

### 一句话定位

> 一个「Token 高效」的 microkernel AI Agent——**本地模型路由器 SquillaRouter 给每一轮对话选最便宜的够用模型**，同时用持久记忆、分层沙箱、内置搜索、设备端 Embedding 构成统一 Turn 循环。口号：**Same budget, more capability, better results.**

### SquillaRouter 架构拆解（v4.2 Phase 3，全本地推理）

```
                ┌────────────────────────────────────────────────┐
 每一轮 Turn ──►│  特征工程（设备端，prompt 不出机器）              │
                │  · BGE small zh v1.5 语义嵌入（ONNX INT8）      │
                │  · 浅层特征：长度/语言/代码/关键词/标志词        │
                │  · 历史轨迹：前 N 轮路由决策 + 上下文 token 估算 │
                │  · 390 维特征向量（features_390）               │
                └───────────────┬────────────────────────────────┘
                                ▼
                ┌────────────────────────────────────────────────┐
                │  集成推理（LightGBM 主头 + 辅助头 + MLP 集成）   │
                │  输出：R0-R3 概率分布 + confidence + margin      │
                └───────────────┬────────────────────────────────┘
                                ▼
                ┌────────────────────────────────────────────────┐
                │  决策后处理（生产级规则）                         │
                │  · 档位映射 R0-R3 → S/M/L/XL 四档 + image 档    │
                │  · thinking_mode T0-T3（是否开深度思考）         │
                │  · prompt_policy P0/P1/P2（提示词复杂度缩放）    │
                │  · flag_rules 关键词触发（high_risk/debug/架构）│
                │  · 置信度门控（升级/救援/防降级/防低估）          │
                │  · 轨迹稳定性 + sticky 防抖                      │
                └───────────────┬────────────────────────────────┘
                                ▼
                ┌────────────────────────────────────────────────┐
                │  self_learning 数据飞轮 ★★★                     │
                │  capture→dataset→train→promotion               │
                │  每次路由决策自动留痕（query+状态+选择+轨迹+成本） │
                │  标签来自执行结果（环境给标签，不是路由器自评）    │
                └────────────────────────────────────────────────┘
```

### 四档路由（runtime.yaml 实录）

| 档位 | Route Class | 默认模型 | 用途 |
|:----:|:-----------:|:---------|:-----|
| **S** | R0 | deepseek/deepseek-v4-flash | 琐碎回合、简短确认，直接回答 |
| **M** | R1（默认）| deepseek/deepseek-v4-pro | 常规问答、编辑、有界编码 |
| **L** | R2 | z-ai/glm-5.2 | 调试、多信号诊断、多步实现计划 |
| **XL** | R3 | anthropic/claude-opus-4.8 | 架构设计、跨系统权衡、高风险生产决策 |

> 有趣：OpenSquilla 也是「便宜通用模型 + 贵强模型」的混合，跟我们的三档分级（lightweight/medium/strong）思路一致，但它是 **4 档**且每个档位还附带思维级别（T0-T3）和提示策略（P0-P2）。

### 关键阈值与规则（可直接抄作业的配置）

```yaml
thresholds:
  margin_upgrade: 0.10           # 概率边际差 ≥0.1 才升级档位
  high_confidence: 0.7           # 高置信度阈值
  r1_rescue: {from_r0_max_gap: 0.10}  # R0 疑似低估时的救援逻辑
  cascade_stage1_threshold: 0.4
  under_routing_safety: 0.45     # 防低估安全线
  kv_cache_aware: true           # 感知 KV 缓存连续性

flag_rules:
  high_risk:  [生产/部署/回滚/迁移/删除/客户/法务/财务, deploy/rollback/migration/production...]
  debug:      [error/bug/exception/traceback/failed/根因/修复, Traceback (most recent...]
  repo_arch:  [repo/codebase/monorepo/架构/重构/module/dependency...]
  strict_format: [JSON/YAML/CSV/schema/只返回/不要解释/按格式...]
  long_context: {char_threshold: 6000, code_block: 1500, log_block: 1500, file_ref: 2}

thinking_mode_rules:             # 自适应思考（Adaptive reasoning）
  T0: {max_class: R0, min_margin: 0.5}     # 简单回合不开思考
  T1: {max_class: R1, min_margin: 0.4}
  T2: {default: true}                      # 默认
  T3: {min_class: R2, flags: [debug, long_context, high_risk]}  # 复杂触发深度思考
```

### 论文核心观点（Agentic Routing: The Harness-Native Data Flywheel）

1. **Agent 路由 ≠ 聊天路由**：现有路由（RouteLLM 等）优化单轮成本-质量，但 agent 执行是 harness（观察/上下文/控制/动作/状态/验证）驱动的多步骤过程，存在中间失败和反馈循环
2. **模型结构性专业化**：前端模型在代码编辑、长上下文恢复、工具使用、数学推理、低延迟上各有所长，没有全能王 → 模型选择是核心系统问题
3. **Harness-Native 路由范式**：基于完整 harness 状态做**步骤级**路由——选单模型（成本优先）或多模型集成（质量优先）
4. **数据飞轮**：每次路由决策自动产生结构化记录（query + harness 状态 + 模型选择 + 执行轨迹 + 结果 + 成本），**标签由执行环境提供**而非路由器自评 → 执行痕迹训练更好的路由器，同预算产生更多痕迹，形成正反馈

### 性能证据（PinchBench 1.2.1，25 任务）

| Agent | 模型 | 平均分 | 输入 token | 输出 token | 总成本 |
|:------|:-----|:------:|----------:|----------:|-------:|
| OpenSquilla | 路由器（Opus4.7+GLM5.1+DS4 Flash）| 0.9251 | 1,721,328 | 61,475 | **$0.688** |
| OpenClaw | Claude Opus 4.7 单模型 | 0.9255 | 3,066,243 | 50,890 | $6.233 |

**结论：分数几乎打平（0.9251 vs 0.9255），成本降到 1/9。** 论文还声称多模型集成路由可超过单一最强模型（Fable 5）。

### 与我们的 smart-router-stack 对比

| 维度 | OpenSquilla SquillaRouter | smart-router-stack（当前骨架）|
|:-----|:--------------------------|:------------------------------|
| 难度评估 | **ML 分类器**：LightGBM+MLP 集成 + BGE 语义嵌入 + 390 维特征 | 规则启发式：4 维加权（长度/指令/推理/领域）|
| 模型档位 | 4 档 S/M/L/XL + image 档，每档带 thinking_level | 3 档 lightweight/medium/strong |
| 输出决策 | 档位 + **置信度** + **margin** + thinking_mode + prompt_policy | 档位 + 成本（无概率输出）|
| 历史感知 | ✅ 前 N 轮路由决策入特征 + 轨迹稳定性 + sticky 防抖 | ❌ 单轮决策 |
| 关键词规则 | ✅ flag_rules 结构化（high_risk/debug/架构/格式/长上下文）| ⚠️ 仅 domain 正则 |
| 自适应思考 | ✅ T0-T3 思维级别 + P0-P2 提示词缩放 | ❌ 无 |
| 自学习 | ✅ **数据飞轮**（capture→train→promotion）| ❌ 无 |
| 供应商适配 | 20+（含 OpenRouter/vLLM/国产）| LiteLLM 20+ |
| 模型资产 | 30-100MB（LFS，ONNX+LightGBM）| 无（纯代码）|
| 部署 | Windows/macOS/Linux/桌面/CLI/频道 | 网关 API（待部署 Ubuntu）|

### 💡 对我们的启示（可借鉴清单）

1. **决策后处理是最大差距**：我们的路由只有「难度分→档位」一步，OpenSquilla 有完整的置信度门控体系（margin_upgrade/high_confidence/r1_rescue/under_routing_safety）——**升级代码骨架时先补这个**，纯规则也能用
2. **flag_rules 比 domain 正则更工程化**：把「高风险/调试/架构/严格格式/长上下文」5 类关键词独立成配置（含中英文），比我们散落的 domain 正则好维护
3. **thinking_mode + prompt_policy 是低成本高收益**：同一模型内按难度切换思考级别和提示词复杂度，不换模型就能省钱（我们完全没做）
4. **历史轨迹是 agent 场景刚需**：多轮对话中短续接轮不该降级（sticky），前几轮决策影响本轮——我们的骨架是单轮决策，agent 化后必须补
5. **数据飞轮是长期方向**：论文的核心洞察「标签来自环境而非路由器」——我们的 tracer.py 已记录 JSONL，正好是飞轮的数据基础，可以先做到「捕获」，训练/promotion 后面再说
6. **本地分类器 vs 规则**：OpenSquilla 用 30-100MB 模型资产做本地推理，换来更准的难度判断；我们目前纯规则 0 资产。**中间态**：先用规则 + flag_rules 把决策后处理做扎实，等有数据了再上 ML
7. **注意 OpenSquilla 的坑**：模型资产在 Git LFS（clone 必须 `git lfs pull`）；Windows 需 VC++ 运行时、macOS 需 libomp，缺了自动降级为单模型直连——我们的纯规则方案没这些依赖问题

---

## 📊 方案对比总结

| 方案 | 开源 | 多LLM | 多模态 | 训练路由器 | 路由策略数 | 生产就绪 | 差异化亮点 |
|:----|:----:|:-----:|:------:|:---------:|:---------:|:-------:|:----------|
| **RouteLLM** | ✅ | 仅2个 | ❌ | ✅ | 4 | ⚠️ 实验性 | 偏好数据训练方法论 |
| **LLMRouter** | ✅ | ✅ | ❌ | ✅ | **16+** | ⚠️ 框架 | 最全策略工具箱，插件系统 |
| **OpenSquilla** | ✅ | ✅ | ✅ | ✅ | 4档+规则 | ✅ | **本地ML路由器+数据飞轮，同预算更强** |
| **OpenRouter** | ❌ | ✅ | ❌ | ❌ | 未知 | ✅ | 100+模型，故障转移 |
| **Portkey Gateway** | ✅ | ✅ | ⚠️ | ❌ | 基础 | ✅ | 可观测性强 |
| **K8s Gateway** | ✅ | ✅ | ❌ | ❌ | 基础 | ✅ | 云原生部署 |
| **百度/腾讯 Router** | ❌ | ✅ | ✅ | ❌ | 基础 | ✅ | 国内生态，多模型类型 |

## 💡 对我们的启示

### 核心差异化机会

| 维度 | 现有方案 | 我们可以做 |
|:-----|:---------|:-----------|
| **模型类型** | 仅 LLM | ✅ **LLM + T2I + T2V + Embedding + Reranker + …** |
| **路由范围** | 仅模型选择 | ✅ 模型类型筛选 → 难度评估 → 模型路由 → Retry |
| **Benchmark 感知** | ❌ 无 | ✅ Benchmark 结果影响路由决策 |
| **Retry 机制** | ❌ 无 | ✅ 失败重试 + 降级 + 回退策略 |
| **Few-shot 路由** | ❌ 无 | ✅ 少量示例自动学习路由模式 |
| **难度评估** | 简单二分类 | ✅ 多维任务难度评分 |

### 可借鉴的设计

1. **RouteLLM** → 偏好数据训练方法论、Kernel-based 路由的核心算法
2. **LLMRouter** → 插件架构、策略编配框架、内置评估管道
3. **OpenSquilla** → 本地 ML 分类器（LightGBM+BGE）、决策后处理置信度门控、thinking_mode/prompt_policy 自适应、flag_rules 关键词工程、self_learning 数据飞轮
4. **Portkey** → 生产级可观测性设计、fallback 机制
5. **OpenRouter** → Provider 归一化思路、成本计算模型

---

## 📋 搜索调研过程（阶段一记录）

### 搜索轮次

| 轮次 | 关键词 | 主要发现 |
|:----|:-------|:---------|
| ① | RouteLLM LLM routing cost optimization | RouteLLM 论文 + GitHub，偏好数据路由 |
| ② | LLM Gateway open source | OpenRouter, Portkey, MLflow Gateway |
| ③ | Chinese LLM router solution | 百度、腾讯多模型 Router，知乎 LLMOps |
| ④ | multi-modal model routing T2I T2V | 未找到专门方案，确认市场空白 |
| ⑤ | LLMRouter framework | UIUC 千星项目，16+策略，插件系统 |

### 搜索数据源
- **学术**：arXiv, ICLR, EMNLP 论文
- **开源**：GitHub（Stars + 活跃度评估）
- **商业**：OpenRouter、Portkey、Azure、AWS、百度、腾讯
- **社区**：知乎、Hugging Face

### 结论
- 多模型类型路由（LLM + T2I + T2V + Embedding + Reranker）**目前没有成熟的解决方案**
- 难度评估 + Benchmark 感知 + Retry Loop 的组合是 **独特卖点**
- LLMRouter 的插件架构是 **最佳参考架构**
