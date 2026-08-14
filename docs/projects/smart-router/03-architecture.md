# 📐 架构设计

> **状态**：🟢 进行中 · **更新**：2026-07-01

---

## 一、系统总览

### 核心流程

```
用户请求
    │
    ▼
┌─────────────────────────────────────────────────┐
│                 智能路由器                        │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ 类型分类  │ → │ 难度评估  │ → │ 路由决策引擎  │   │
│  │ (Type)   │   │ (Difficulty)│ │ (Router)    │   │
│  └──────────┘  └──────────┘  └──────┬───────┘   │
│                                      │          │
│  ┌──────────┐  ┌──────────┐         │          │
│  │ Benchmark│  │ 成本优化  │ ←────────┘          │
│  │ 感知     │  │ (Cost)   │                    │
│  └──────────┘  └──────────┘                    │
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │         Retry Loop（重试/降级/回退）        │  │
│  └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
    │
    ▼
模型层: {LLM, T2I, T2V, Embedding, Reranker, ...}
```

### 路由决策流程（详细）

```
请求 → [Parser] → 结构化特征 (task_type, prompt_len, keywords, domain...)
                     │
                     ▼
              [Type Classifier] ← 规则 / 语义分类
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
         LLM       T2I/T2V    Emb/Reranker
          │          │          │
          ▼          ▼          ▼
    [难度评估]   [难度评估]    [难度评估]
     Token分析   分辨率分析   维度/批次分析
     推理深度     描述精度    相似度阈值
          │          │          │
          ▼          ▼          ▼
    [Router]     [Router]     [Router]
    cls/级联     级联/KNN    规则匹配
          │          │          │
          ├──────────┼──────────┤
          ▼          ▼          ▼
        [模型执行层]
               │
               ▼
         [结果校验]
         ✅ 通过 → 返回
         ❌ 失败 → Retry Loop
                     │
                     ▼
               降级/换模型 → 重试 → 超时返回
```

---

## 二、路由策略选型（核心理念）

### 行业验证的四条路线

| 策略 | 原理 | 延迟 | 维护成本 | 推荐场景 |
|:----|:------|:----:|:--------:|:---------|
| **级联 (Cascade)** | 小模型先答，置信度不够才升大模型 | 较高（可能付两次） | 低 | **起点方案** |
| **分类器 (Classifier)** ⭐ | DistilBERT/ModernBERT 10-40ms 决策 | **最低** | 中 | **生产主力** |
| **Embedding 相似度** | KNN 查历史路由记录 | 低 | 低 | 冷启动/过渡 |
| **学习型 (Learned)** | Contextual Bandit 在线探索 | 中 | **高** | 成熟期优化 |

### 推荐技术路线：两阶段演进

```
Stage 1（MVP）             Stage 2（生产级）
┌──────────────────┐      ┌──────────────────────┐
│  级联 + 规则引擎   │ ──→ │  分类器 + 级联兜底    │
│                  │      │                      │
│  ├ Embedding 相似度│      │  ├ ModernBERT 分类   │
│  ├ 规则匹配       │      │  ├ 难度回归模型      │
│  ├ 手工置信门控    │      │  ├ 自动置信门控     │
│  └ 简单重试       │      │  └ 带反馈的 Retry   │
│                  │      │                      │
│ 降本 40-70%      │      │ 再降 20-40%          │
│ 开发: 几天       │      │ 开发: 几周           │
└──────────────────┘      └──────────────────────┘
```

**核心原则**：先跑起来，用数据说话，再上模型。

---

## 三、模型类型分类器（Type Classifier）

> ✅ **已决策**：采用语义分类方案

### 问题定义
用户请求来了，第一步：判断该走哪类模型？

### 方案：两阶段演进

#### 阶段一（MVP）：规则 + 关键词匹配

| 请求特征 | 模型类型 | 示例 |
|:---------|:---------|:-----|
| 包含 `生成图片/画/图/绘制/插图`、`create image/generate photo` | T2I | "帮我画一只猫" |
| 包含 `生成视频/动画`、`create video/generate animation` | T2V | "生成一段城市夜景动画" |
| 包含 `向量化/embedding/嵌入`、`similarity/相似度` | Embedding | "将这段文本转成向量" |
| 包含 `重排/rerank/排序`（搜索结果语境） | Reranker | "对搜索结果按相关性重排序" |
| 以上都不匹配 | LLM（默认） | "写一篇关于AI的文章" |

规则优先级：**更具体的匹配优先** → 都不匹配则默认走 LLM。

#### 阶段二（生产）：语义分类器 ⭐——重点方案

用 **ModernBERT**（或 DistilBERT）微调成一个 5 分类模型：

```
输入: "帮我画一只赛博朋克风格的猫"
    │
    ▼
[ModernBERT Classifier]
    │
    ├── T2I:     92%  ← 选中
    ├── T2V:      3%
    ├── LLM:      4%
    ├── Embed:    1%
    └── Rerank:   0%
```

**为什么选 ModernBERT：**

| 维度 | ModernBERT | DistilBERT | 规则引擎 |
|:-----|:-----------|:-----------|:---------|
| 推理延迟 | **10-30ms** | 15-40ms | < 1ms |
| 准确率 | **最高** | 较高 | 较低（难覆盖边界情况） |
| 冷启动 | ❌ 需标注数据 | ❌ 需标注数据 | ✅ 零成本 |
| 长文本理解 | ✅ 支持 8k tokens | ⚠️ 512 tokens | ❌ |
| 泛化能力 | ✅ 可理解语义变体 | ✅ 较好 | ❌ 死板匹配 |

**训练数据收集：**

| 来源 | 用途 | 数量要求 |
|:-----|:-----|:--------:|
| 历史请求日志 | 主训练集 | ~5000 条/类 |
| 人工标注 | 验证集 + 边界案例 | ~200 条/类 |
| 数据增强（同义改写） | 增强鲁棒性 | ~1000 条/类 |

**冷启动策略**：项目早期先用规则引擎跑 → 积累请求日志 → 人工标注 → 训练语义分类器 → 灰度替换规则。

**混合决策逻辑**（生产环境）：

```python
def classify_model_type(request):
    # 1. 语义分类器先做预测
    type_scores = modernbert_classifier(request.text)
    predicted_type = type_scores.argmax()
    confidence = type_scores.max()
    
    # 2. 置信度高 → 直接用
    if confidence >= 0.85:
        return predicted_type
    
    # 3. 置信度中等 → 规则兜底
    if confidence >= 0.6:
        rule_type = rule_classifier(request.text)
        if rule_type == predicted_type:
            return predicted_type
        else:
            return "NEEDS_REVIEW"  # 打标待人工确认
    
    # 4. 置信度低 → 走规则
    return rule_classifier(request.text)
```

### 边界情况处理

| 边界场景 | 处理策略 |
|:---------|:---------|
| **混合请求**（既写文章又配图） | 拆分为两个子请求，分别路由和响应 |
| **显式指定模型**（"用 DALL-E 画"） | 直接路由到指定模型，不经过分类器 |
| **模糊请求**（"帮我设计个东西"） | 默认走 LLM，让 LLM 拆解任务 |
| **多步请求**（先分析情感再画图） | 拆为 pipeline，逐步路由 |
| **新类型请求**（不在5类中） | 落入 "unknown" 兜底 → 走 LLM → 记录打标

---

## 四、难度评估体系（Difficulty Assessment）

> ✅ **已决策**：采用三层信号框架（规则级 → 分类器级 → 学习型）

### 核心思路

难度评估是整个路由中**最难的部分**——模型还没开始回答，就得判断它能不能答好。业界有四个可靠的信号源：

```
请求文本
    │
    ├── ① 分类标签（来自 Type Classifier）
    │      └── 数学题 vs 摘要 vs 代码 → 不同类默认难度不同
    │
    ├── ② 长度+复杂度启发式
    │      └── Token数、代码块、多段指令步骤数 → 计算复杂度分
    │
    ├── ③ Embedding 相似度（KNN）
    │      └── 找历史最相似请求 → 查它们的模型选择与质量评分
    │
    └── ④ 显式难度标记
           └── "think step by step"、"compare" → 标记需推理模型
```

### 工作负载分布（经验基准）

参考生产环境数据，请求天然呈三段分布：

```
◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼ 60-75%  简单（Trivial）
    任何 30B+ 模型都能答好 → 最便宜的模型
◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼ 15-30% 质量敏感（Quality-Sensitive）
    需要一定推理深度 → 中等/前沿模型
◼◼◼◼ 1-10%  复杂推理（Reasoning-Required）
    需逐步推理/长上下文分析 → 最强模型
```

### 方案：三阶段演进

#### 阶段一（MVP）：规则级难度评估

**核心**：用 4 个无需训练的启发式指标算出一个综合难度分。

**维度计算**：

| 维度 | 指标 | 权重 | 计分方式 |
|:-----|:-----|:----:|:---------|
| **① Prompt 长度分** | `min(tokens/2048, 1.0)` | 25% | 越长越难，2048 tokens 封顶 |
| **② 指令复杂度** | 步骤数 / 5 | 25% | 每多一个要求加 0.2 分 |
| **③ 推理标记分** | 含 `think step by step / explain / compare / reason / analyze / evaluate / whether` 等 | 25% | 出现 1 个得 0.3，2 个得 0.6，3+ 得 1.0 |
| **④ 领域技术分** | 含代码块 / 公式 / 数学符号 / 专业术语 | 25% | 有代码块 0.5 + 有公式 0.3 + 专业术语 0.2 |

**综合公式**：
```
Score = w1×len_score + w2×step_score + w3×reasoning_score + w4×domain_score
Score ∈ [0, 1]
```

**难度区间**：

| 得分 | 级别 | 占比（预估） | 推荐模型 |
|:----:|:-----|:------------:|:---------|
| 0.0 - 0.3 | 🟢 简单 | ~60% | 轻量模型（Qwen2.5-7B, LLaMA-3-8B） |
| 0.3 - 0.6 | 🟡 一般 | ~25% | 中型模型（Qwen2.5-32B, LLaMA-3-70B） |
| 0.6 - 0.8 | 🟠 复杂 | ~10% | 强模型（GPT-4o, Claude Sonnet） |
| 0.8 - 1.0 | 🔴 极高 | ~5% | 最强模型（Claude Opus, GPT-4 Turbo） |

**边界特殊处理**：

| 情况 | 处理 |
|:-----|:-----|
| Prompt 超过 8k tokens | 自动标记为「复杂」（长上下文需要强模型） |
| 明确要求"用最简单的语言" | 难度-0.2 降级 |
| 请求包含代码执行/数据分析 | 难度+0.2 升级 |
| 用户历史显示偏好某个模型 | 覆盖难度评分，直接走用户偏好模型 |

**Python 实现**：

```python
def assess_difficulty_stage1(request):
    score = 0.0
    
    # ① Prompt 长度分
    token_count = estimate_tokens(request.text)
    len_score = min(token_count / 2048, 1.0)
    score += 0.25 * len_score
    
    # ② 指令复杂度
    steps = count_instructions(request.text)
    step_score = min(steps / 5, 1.0)
    score += 0.25 * step_score
    
    # ③ 推理标记分
    reasoning_markers = ["think step by step", "explain", "compare",
                         "reason", "analyze", "evaluate", "whether",
                         "what if", "why", "how does"]
    marker_count = sum(1 for m in reasoning_markers if m in request.text.lower())
    reasoning_score = min(marker_count / 3, 1.0)
    score += 0.25 * reasoning_score
    
    # ④ 领域技术分
    has_code = bool(re.search(r'```|def |class |import |function', request.text))
    has_formula = bool(re.search(r'[∑∫√∂±×÷∈πθλ]|\\[\(\)]', request.text))
    has_terms = bool(re.search(r'time complexity|O\(|asymptotic|gradient|loss function', 
                                request.text.lower()))
    domain_score = (0.5 if has_code else 0) + (0.3 if has_formula else 0) + (0.2 if has_terms else 0)
    score += 0.25 * domain_score
    
    # 边界修正
    if token_count > 8000:
        score = max(score, 0.6)
    if "简单的" in request.text or "通俗" in request.text:
        score -= 0.2
    if "执行代码" in request.text or "数据分析" in request.text:
        score += 0.2
    
    return round(min(max(score, 0), 1), 2)
```

#### 阶段二（生产）：Embedding-KNN 增强

在规则基础上增加 Embedding 相似度信号：

```python
def assess_difficulty_stage2(request):
    # 1. 先算规则分
    rule_score = assess_difficulty_stage1(request)
    
    # 2. 查历史相似请求
    request_emb = embed(request.text)
    similar_requests = knn_search(request_emb, k=50)
    
    if similar_requests:
        # 这些历史请求用了什么模型？效果如何？
        avg_model_tier = similar_requests["model_tier"].mean()
        avg_quality = similar_requests["quality_score"].mean()
        
        # 3. 融合：规则分 70% + 历史证据 30%
        historical_score = 1 - (avg_model_tier / 4)  # tier 1-4 映射到 0-1
        confidence = avg_quality  # 历史质量越高，越可信
        
        final_score = 0.7 * rule_score + 0.3 * historical_score * confidence
    else:
        final_score = rule_score
    
    return round(min(max(final_score, 0), 1), 2)
```

#### 阶段三（成熟期）：学习型难度校准

- 用 Contextual Bandit 持续学习——模型实际表现反馈到权重
- 自动发现新维度（如某些特定数据集名 → 固定要强模型）
- 效果稳定后蒸馏回轻量分类器

### T2I / T2V 难度评估

| 维度 | 指标 | 权重 | 计分方式 |
|:-----|:-----|:----:|:---------|
| **描述精度** | Prompt 长度、细节数量、风格/构图要求 | 35% | `min(len/200, 1.0)` + 风格词数量 × 0.1 |
| **语义抽象度** | 抽象概念 vs 具体场景 | 25% | 含 `概念/氛围/情绪/风格` 等抽象词 +0.3 |
| **分辨率要求** | 标准 vs 高清 vs 超清 | 20% | 出现 `4k/HD/超清/高清` +0.5 |
| **合规要求** | 是否需要过滤敏感内容 | 20% | 默认低，含敏感词 +1.0 |

### Embedding / Reranker 难度评估

| 维度 | 指标 | 权重 |
|:-----|:-----|:----:|
| **输入规模** | 输入文本长度 / 批次大小 | 40% |
| **精度要求** | 精确匹配 vs 模糊匹配 | 30% |
| **延迟要求** | 实时响应 (< 100ms) vs 离线批量 | 30% |

---

## 五、路由决策引擎（核心）

### MVP 范围：仅 LLM 路由

> ✅ **已决策**：MVP 阶段只做 LLM 路由，后续迭代扩展 T2I/T2V/Embedding/Reranker

**理由**：
1. LLM 路由是核心价值验证点——难度的算得准、成本降得下，这个系统才有意义
2. 业界（RouteLLM、LLMRouter、Martian）全从 LLM 起步，路径已验证
3. 多模型类型路由在市场空白，但不应在 MVP 阶段分散精力

### 整体决策逻辑（MVP：仅 LLM）

```python
def route(request):
    # MVP 阶段：所有请求走 LLM 路由
    return route_llm(request)
```

### 整体决策逻辑（扩展后：多模型类型）

```python
def route(request):
    # 扩展后：先分类类型，再路由
    # ── 这段代码在 MVP 2.0 才会加上 ──
    # model_type = type_classifier(request)
    # 
    # if model_type == "LLM":
    #     return route_llm(request)
    # elif model_type in ("T2I", "T2V"):
    #     return route_multimodal(request, model_type)
    # elif model_type in ("Embedding", "Reranker"):
    #     return route_embedding(request, model_type)
    
    # MVP 先只走 LLM
    return route_llm(request)
```

#### LLM 路由子流程

```python
def route_llm(request):
    # 1. 规则优先：显式指定模型
    if request.specified_model:
        return request.specified_model
    
    # 2. Benchmark 感知：如果是在跑 benchmark
    if request.is_benchmark:
        return get_benchmark_model(request.benchmark_name)
    
    # 3. 难度评估
    difficulty = assess_difficulty_llm(request)
    
    # 4. 路由决策
    if difficulty < 0.3:
        return select_cheapest_model("lightweight")
    elif difficulty < 0.6:
        return select_model("medium")
    elif difficulty < 0.8:
        return select_best_model("strong")
    else:
        return select_best_model("top")
    
    # 5. Few-shot 路由（数据充足时）
    # 用历史数据中的 (request_embedding, optimal_model) 做 KNN
```

### 级联路由实现（Stage 1 核心）

```
请求 → [小模型] → [置信度 >= 0.9] → ✅ 返回
                      │ < 0.9
                      ▼
               [中模型] → [置信度 >= 0.95] → ✅ 返回
                            │ < 0.95
                            ▼
                        [大模型] → ✅ 返回
```

---

## 六、Retry Loop（重试循环）

### 错误类型分类（来自生产环境经验）

不同类型的失败，处理方式完全不同：

| 错误类型 | 特征 | 根因 | 处理策略 | 重试上限 |
|:---------|:-----|:-----|:---------|:--------:|
| **🔴 网络超时** | timeout, connection reset | 网络波动 | 换同级别模型的另一个 Provider | 2 次 |
| **🟡 429 限流** | Rate limit, Too Many Requests | QPS 超限 | 指数退避等待后重试 | 3 次 |
| **🔴 5xx 服务端** | Internal Server Error, Service Unavailable | 模型方故障 | 换同供应商另一个 endpoint 或跨供应商切换 | 2 次 |
| **🟠 401 鉴权** | Unauthorized, Invalid API Key | API Key 失效/额度耗尽 | 换备用 API Key 或切换供应商 | 1 次 |
| **🟡 参数错误** | Bad Request, Invalid Parameter | 模型参数格式不兼容 | 做参数适配后重试 | 1 次 |
| **⚪ 内容安全** | Content filtered, Violation | 触发安全策略 | 降级到更保守的模型 | 1 次 |
| **🔵 质量不达标** | 模型输出质量不符合预期 | 模型能力不够 | 升级到更强模型 | 1 次 |

### trace_id（请求追踪）

**每个请求必须带唯一的 trace_id**，贯穿整个路由生命周期：

```python
{
    "trace_id": "rtr_20260701_a1b2c3d4",
    "request": {
        "text": "...",
        "model_type": "LLM",
        "difficulty": 0.35
    },
    "route_decision": {
        "selected_model": "qwen-plus",
        "reason": "difficulty_0.35_medium_tier",
        "confidence": 0.88
    },
    "execution": [
        {"attempt": 1, "model": "qwen-plus", "status": "success", "latency_ms": 1200}
    ],
    "cost": {"input_tokens": 450, "output_tokens": 120, "total_cost_yuan": 0.0012}
}
```

trace_id 的作用：
- 问题排查：某个请求为什么走了大模型？查 trace 一目了然
- 成本归因：每笔请求花了多少钱，落实到 trace
- 质量回溯：用户反馈差，找到对应的 trace 分析路由决策

### 重试流程（增强版）

```python
def execute_with_retry(request, selected_model, trace_id):
    max_attempts = 3
    current_model = selected_model
    last_error = None
    
    for attempt in range(max_attempts):
        try:
            result = call_model(current_model, request, trace_id)
            
            if is_quality_acceptable(result, request):
                log_trace(trace_id, attempt, current_model, "success")
                return result
            else:
                # 质量不达标 → 升级重试
                current_model = escalate_model(current_model)
                log_trace(trace_id, attempt, current_model, "quality_escalate")
                
        except APIError as e:
            last_error = e
            action = classify_error(e)  # 根据错误类型判断
            
            if action == "retry_same":
                # 429 限流 → 指数退避
                sleep_time = 2 ** attempt
                time.sleep(sleep_time)
                log_trace(trace_id, attempt, current_model, f"rate_limit_retry:{sleep_time}s")
                
            elif action == "switch_provider":
                # 超时/5xx → 换同级别 Provider
                current_model = switch_provider(current_model)
                log_trace(trace_id, attempt, current_model, "provider_switch")
                
            elif action == "switch_key":
                # 401 → 换备用 API Key
                switch_api_key(current_model.provider)
                log_trace(trace_id, attempt, current_model, "key_switch")
                
            elif action == "adapt_params":
                # 参数错误 → 做参数适配
                request = adapt_parameters(request, current_model)
                log_trace(trace_id, attempt, current_model, "param_adapt")
                
    # 所有重试失败 → 兜底
    log_trace(trace_id, "fallback", "all_retries_exhausted", last_error)
    return fallback_response(request, trace_id)
```

---

## 七、Benchmark 感知

### 设计思路

当检测到请求属于某个 Benchmark（如 MMLU, HumanEval, GSM8K）时，不走常规路由，而是：

1. 根据 Benchmark 名称自动匹配**最优模型**
2. 查询历史评测结果，选择在该 Benchmark 上**得分最高**的模型
3. 记录本次评测结果，**更新路由决策依据**

```python
BENCHMARK_MODEL_MAP = {
    "mmlu": "qwen-max",           # 知识类评测
    "human_eval": "deepseek-coder-v3", # 代码生成
    "gsm8k": "qwen-plus",         # 数学推理
    "ceval": "qwen-max",          # 中文知识评测
    "alignbench": "glm-4-plus",   # 中文对齐评测
    # 持续补充...
}
```

### 数据回流

Benchmark 评测结果 → 更新模型能力画像 → 影响日常路由决策

---

## 八、跨模型参数适配

> 生产环境中的隐形陷阱：同一个请求参数，不同模型/供应商的 API 格式完全不同。

### 常见参数差异

| 参数 | 通义千问 | DeepSeek | 智谱 |
|:-----|:---------|:---------|:-----|
| **模型名** | `model: "qwen-plus"` | `model: "deepseek-chat"` | `model: "glm-4-plus"` |
| **消息格式** | OpenAI 兼容 | OpenAI 兼容 | OpenAI 兼容 |
| **系统提示** | messages 中 role:system | messages 中 role:system | messages 中 role:system |
| **温度** | `temperature: 0-2` | `temperature: 0-2` | `temperature: 0-1` |
| **最大 Token** | `max_tokens` | `max_tokens` | `max_tokens` |
| **流式** | `stream: true/false` | `stream: true/false` | `stream: true/false` |

### 关键适配点

- **供应商统一客户端**：用统一的内部请求格式 → 客户端翻译成各供应商的 API 格式
- **参数范围差异**：如智谱的 temperature 范围是 0-1，其他是 0-2，需要 clamp
- **模型名映射**：路由决策返回逻辑模型名 → 客户端映射为实际 API 模型名
- **错误消息解析**：不同供应商的错误 JSON 结构不同，统一提取错误码和消息

```python
class BaseLLMClient:
    """统一客户端接口"""
    def chat(self, request: RouterRequest) -> LLMResponse:
        raise NotImplementedError

class AliyunClient(BaseLLMClient):
    def chat(self, request):
        api_request = self._translate(request)  # 统一格式 → 阿里格式
        raw = self._call_api(api_request)
        return self._parse_response(raw)        # 阿里格式 → 统一格式
    
    def _translate(self, request):
        return {
            "model": self.model_config.api_model_name,  # 映射实际模型名
            "input": {"messages": request.messages},
            "parameters": {
                "temperature": min(request.temperature, 2.0),  # clamp
                "max_tokens": request.max_tokens,
            }
        }
```

---

## 九、模型注册表（Model Registry）

### MVP 模型池（国内 API，3 档分级）

#### 🟢 轻量级（低成本，处理 60% 简单请求）

| 模型 | 提供商 | 输入价格 | 输出价格 | 特点 |
|:-----|:-------|:--------:|:--------:|:-----|
| **deepseek-chat** (V3) | DeepSeek | ¥1/1M tokens | ¥2/1M tokens | 性价比极高，中文强 |
| **qwen-turbo** | 通义千问 | ¥0.3/1M tokens | ¥0.6/1M tokens | 最便宜，适合简单问答 |
| **glm-flash** | 智谱 | ¥0.1/1M tokens | ¥0.1/1M tokens | 极致低价 |

#### 🟡 中档（性价比均衡，处理 25% 敏感请求）

| 模型 | 提供商 | 输入价格 | 输出价格 | 特点 |
|:-----|:-------|:--------:|:--------:|:-----|
| **qwen-plus** | 通义千问 | ¥0.8/1M tokens | ¥2/1M tokens | 均衡之选 |
| **glm-4-air** | 智谱 | ¥0.5/1M tokens | ¥0.5/1M tokens | 稳定可靠 |

#### 🔴 强模型（高质量，处理 15% 复杂请求）

| 模型 | 提供商 | 输入价格 | 输出价格 | 特点 |
|:-----|:-------|:--------:|:--------:|:-----|
| **qwen-max** | 通义千问 | ¥2/1M tokens | ¥6/1M tokens | 阿里最强 |
| **glm-4-plus** | 智谱 | ¥5/1M tokens | ¥5/1M tokens | 智谱旗舰 |
| **deepseek-reasoner** (R1) | DeepSeek | ¥4/1M tokens | ¥16/1M tokens | 深度推理 |

### 模型注册 YAML 格式

```yaml
# 示例：models/qwen-plus.yaml
model_id: qwen-plus
type: LLM
provider: aliyun
description: 通义千问 Plus，性价比均衡
api:
  endpoint: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  auth_env: "DASHSCOPE_API_KEY"
capabilities:
  max_tokens: 131072
  languages: [zh, en]
  tasks: [chat, code, reasoning, translation]
cost:
  per_1m_input: 0.8       # ¥/1M tokens
  per_1m_output: 2.0
latency:
  p50_ttft: 0.8           # seconds
  p50_tps: 50             # tokens per second
benchmark_scores:
  mmlu: 85.0
  ceval: 90.5
  gsm8k: 90.8
routing:
  tier: medium            # lightweight / medium / strong / top
  difficulty_range: [0.3, 0.6]
  preferred_tasks: [chat, general_qa, translation]
```

---

## 十、评估体系（如何衡量路由效果）

### 核心指标

| 指标 | 定义 | 目标 |
|:-----|:-----|:----:|
| **路由准确率** | 路由选择的模型是否最优 | > 95% |
| **成本降幅** | 相比全量调用最强模型的成本比 | 40-70%（Stage 1） |
| **质量保持率** | 路由后质量分 / 最强模型质量分 | > 95% |
| **平均延迟** | 路由 + 推理总耗时 | < 5s |
| **失败率** | 路由后重试/降级的比例 | < 2% |

### 总成本公式（含隐形成本）

路由节省的成本不能只看模型单价，要算**总拥有成本**：

```
总成本 = 
    输入Token费用 × 输入量
    + 输出Token费用 × 输出量
    + 重试费用 × 重试次数   ← 被忽略的大头
    + 失败损失 × 失败率     ← 业务损失
    + 延迟惩罚 × 超时率     ← 客户体验
    + 人工对账成本          ← 路由策略可解释性差时的隐性成本
```

**例子**：一个月 1200 万请求，全量走 qwen-max 和走路由的对比

| 方案 | 模型调用成本 | 重试成本 | 总成本 |
|:-----|:-----------:|:--------:|:------:|
| 全量 qwen-max（最强模型） | ¥28,800 | ¥1,440 | **¥30,240** |
| 路由后（60%走便宜模型） | ¥11,520 | ¥860 | **¥12,380** |
| **节省** | **60%** | **40%** | **59%** |

### A/B 测试框架

```
对照组: 全部走最强模型（如 GPT-4o）
实验组: 走智能路由器
对比: 成本 / 质量 / 延迟
```

---

## 十一、技术选型建议

| 组件 | 方案 | 选型理由 |
|:-----|:------|:---------|
| **类型分类器**（Stage 1） | 规则 + 关键词 | 零成本，快速上线 |
| **类型分类器**（Stage 2） | ModernBERT 微调 | 10-40ms，no LLM 调用 |
| **难度评分**（Stage 1） | 线性加权公式 | 可解释，易调参 |
| **难度评分**（Stage 2） | 轻量回归模型 | 更精准 |
| **路由决策**（Stage 1） | 级联 + 置信门控 | 最容易正确实现 |
| **路由决策**（Stage 2） | 分类器 + 级联兜底 | 生产级标准 |
| **模型注册** | YAML / JSON 配置 | 简单，Git 可追踪 |
| **模型 API** | 通义千问 / DeepSeek / 智谱 | 国内，延迟低，成本透明 |
| **API 调用** | Python `httpx` + 统一客户端 | 轻量，异步支持 |
| **监控** | 结构化日志 → 后续 Prometheus | 业界标准 |

---

## 十二、实施路线图

### Phase 1：LLM 路由 MVP（Week 1-2）

```
████████░░░░░░  LLM 路由 + 难度评估 + 级联
```

| 模块 | 内容 | 产出 |
|:-----|:-----|:-----|
| **模型注册表** | 3-5 个 LLM 的 YAML 配置 | `models/` 目录 |
| **难度评估** | Stage 1 规则级（4 维加权） | `assess_difficulty()` |
| **路由决策** | 级联路由（3 层，置信门控） | `route_llm()` |
| **Retry** | 错误分类 + trace_id + 重试 | `execute_with_retry()` |
| **参数适配** | 统一客户端 + 参数翻译 | `clients/` 目录 |
| **评估** | 基准测试：对照全走最强模型 | 成本 + 质量对比报告 |

### Phase 2：生产级增强（Week 3-4）

```
████████████░░  LLM 路由优化 + 可观测
```

| 模块 | 内容 |
|:-----|:------|
| 难度回归模型替代规则公式 |
| Embedding-KNN 增强 |
| Benchmark 感知模块 |
| 结构化日志 + 成本归因 |
| A/B 测试框架 |

### Phase 3：扩展多模型类型（Week 5-6+）

```
██████████████  多模型类型路由扩展
```

| 模块 | 内容 |
|:-----|:------|
| ModernBERT 类型分类器（5 类） |
| T2I / T2V 路由策略 | 
| Embedding / Reranker 路由策略 |
| 各类型独立难度评估 |
| 全面落地多模型类型路由 |

---

## 十三、已决策 & 待决策

### ✅ 已决策

- [x] **类型分类方案**：语义分类（ModernBERT），Stage 1 先用规则兜底
- [x] **难度评估方案**：三层框架（规则级 → Embedding-KNN → 学习型）
- [x] **LLM 难度维度**：4 维（Prompt 长度 + 指令复杂度 + 推理标记 + 领域技术分）
- [x] **MVP 范围**：先只做 LLM 路由，Phase 3 再扩展多模型类型
- [x] **模型提供商**：国内 API（通义千问 / DeepSeek / 智谱）
- [ ] T2I/T2V 路由的难度评估维度是否够？
- [ ] Benchmark 列表初期维护几个？
- [ ] 初期对接哪些模型/Provider？

### ⭐ 生产就绪检查清单（借鉴生产环境经验）

| # | 检查项 | 说明 | MVP | Phase 2 |
|:-:|:-------|:-----|:---:|:-------:|
| 1 | **trace_id** | 每个请求有唯一追踪 ID | ✅ 必须 | ✅ |
| 2 | **错误分类处理** | 429/5xx/401/超时分别处理 | ✅ 必须 | ✅ |
| 3 | **指数退避** | 限流时指数级等待 | ✅ 必须 | ✅ |
| 4 | **参数适配** | 跨模型自动适配 API 参数差异 | ✅ 必须 | ✅ |
| 5 | **结构化日志** | 路由决策、耗时、成本全部结构化记录 | ✅ | ✅ |
| 6 | **成本归因** | 每笔请求成本可追踪到 trace | ⏳ 简化版 | ✅ |
| 7 | **租户隔离** | 多租户时互不干扰额度 | ⏳ 后续 | ⏳ |
| 8 | **A/B 测试** | 路由策略可灰度放量 | ⏳ | ✅ |
| 9 | **可解释性** | 路由决策理由可查询（为什么选这个模型？） | ⏳ | ✅ |
| 10 | **路由策略热更新** | 不停机更新模型池和路由规则 | ⏳ | ⏳ |

---

*架构设计持续更新中...*
