# 参考资料

> 汇总智能路由系统相关的论文、开源项目、博客和产品。  
> 更新日期：2026-07-01

---

## 📄 论文

| 论文 | 出处 | 年份 | 关键词 |
|:----|:----|:----:|:-------|
| [RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665) | ICLR 2025 | 2024 | 偏好数据、两模型路由、4种策略 |
| [LLMRouter: An Open-Source Framework for LLM Routing](https://arxiv.org/abs/...) | arXiv | 2025 | 16+路由策略、统一框架、插件系统 |
| [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](https://arxiv.org/abs/2305.05176) | arXiv | 2023 | 级联路由、成本优化、query 分类 |
| [Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing](https://arxiv.org/abs/2404.14618) | arXiv | 2024 | 混合查询路由、质量感知 |
| [CascadeBERT: Accelerating Inference of Pre-trained Language Models via Calibrated Cascades](https://arxiv.org/abs/2012.14682) | EMNLP | 2020 | 级联推理、早退机制 |

## 💻 开源项目

| 项目 | 链接 | 简介 | 推荐理由 |
|:----|:-----|:-----|:---------|
| **RouteLLM** ⭐ | [GitHub](https://github.com/lm-sys/RouteLLM) | UC Berkeley，偏好数据训练路由器 | 方法论扎实，ICLR 2025 |
| **LLMRouter** ⭐⭐⭐ | [GitHub](https://github.com/ulab-uiuc/LLMRouter) | UIUC，16+路由策略，千星项目 | **最佳参考架构** |
| | [官网](https://ulab-uiuc.github.io/LLMRouter/) | 完整文档和教程 | |
| **Portkey AI Gateway** ⭐⭐ | [GitHub](https://github.com/Portkey-AI/gateway) | 开源 AI Gateway，200+模型 | 可观测性设计参考 |
| **routeLLM** (HadiAbtin) | [GitHub](https://github.com/HadiAbtin/routeLLM) | 多Provider LLM Gateway | 轻量网关参考 |
| **K8s Inference Gateway** | [GitHub](https://github.com/kserve/modelmesh) | K8s原生推理网关 | 云原生部署参考 |

## 📝 博客与文章

| 标题 | 链接 | 来源 | 要点 |
|:----|:-----|:------|:-----|
| **The Model Router Pattern (2026)** ⭐ | [AppScale Blog](https://appscale.blog/en/blog/ai-service-pattern-model-router-cost-quality-latency-aware-routing-2026) | AppScale | 4种路由原语、5级成熟度阶梯、8个反模式、成本算例 |
| LLMOps与智能系统重构：模型路由策略 | [知乎](https://zhuanlan.zhihu.com/p/1979461057031448489) | 知乎 | 国内模型路由实践 |
| OpenRouter: Unified LLM API Gateway Guide | [expertbeacon](https://expertbeacon.com/openrouter-unified-llm-api-gateway-guide/) | ExpertBeacon | OpenRouter 技术架构 |
| All You Need to Know About LLM Routing | [LLMRouter 官方博客](https://ulab-uiuc.github.io/LLMRouter/) | UIUC ULab | LLMRouter 教程 |

## 🏢 商业产品

| 产品 | 公司 | 特点 | 适用场景 |
|:----|:-----|:------|:---------|
| **OpenRouter** | OpenRouter | 100+模型，Provider路由，成本优化 | 多 Provider 统一 API |
| **Portkey** | Portkey | AI Gateway，可观测性，Guardrails | 生产环境监控 |
| **Helicone** | Helicone | LLM 可观测性 + 路由 | 日志和追踪 |
| **Azure AI Gateway** | Microsoft | 企业级 AI 网关，策略路由 | 微软生态 |
| **Amazon Bedrock** | AWS | 多模型服务，基础路由 | AWS 生态 |
| **百度智能云·Router** | 百度 | 国内生态，任务路由 | 中文场景 |
| **腾讯云·多模型Router** | 腾讯 | 灰度发布，A/B测试 | 中文场景 |

---

---

## 🚀 独立参考项目：OpenSquilla（基元律动）

> 前华为盘古大模型负责人王云鹤创立的基元律动团队研发，Apache 2.0 开源。  
> 本文来源：「物联网星球」公众号，2026-06-04  
> 加入时间：2026-07-03

| 项目 | 说明 |
|:-----|:------|
| **项目名称** | OpenSquilla — 微内核 AI Agent 框架 |
| **GitHub** | [开源地址](https://github.com/opensquilla/opensquilla)（Apache 2.0，6.5k+ stars） |
| **技术栈** | Python 3.12+，全平台 |
| **核心理念** | Token 成本直降 **60-80%**，通过智能路由实现，非模型压缩 |

### 路由系统架构（SquillaRouter）

OpenSquilla 的路由方案与我们的设计**并列**，可相互参考：

| 对比维度 | OpenSquilla（SquillaRouter） | 我们的方案 |
|:---------|:-----------------------------|:-----------|
| **分类器选型** | **LightGBM + ONNX**，本地 CPU 运行 | ModernBERT 语义分类 |
| **分析维度** | 3 维：手工特征 + 语义特征 + 思维深度 | 4 维：长度 + 指令 + 推理 + 领域 |
| **难度分级** | T0~T3 四档（问候→一般→复杂→深度推理） | 🟢🟡🟠🔴 四档 |
| **路由范围** | 仅 LLM | LLM + T2I + T2V + Emb + Reranker |
| **决策延迟** | 零延迟（本地） | 低延迟（本地 ONNX） |
| **路由时机** | 每次对话请求 | 每次 API 请求 |

### 值得借鉴的设计点

- **LightGBM + ONNX**：验证了树模型做路由在生产环境的可行性，比 Transformer 更轻量、部署更简单
- **思维深度维度**：判断是否需要深度推理 vs 简单问答，是一个独特的分类维度
- **T0 本地模型**：最简单的问候类请求直接走本地模型，零费用
- **微内核架构**：核心只做编排+状态管理，全插件化，架构清晰

### 其他亮点

- **四层记忆系统**：工作记忆 / 情节记忆 / 语义记忆 / 原始记忆，混合检索 + 时间衰减 + 每 24h "梦境"自动整理
- **MetaSkills 协议**：Agent 可自我进化，空闲时重放记忆自动起草新技能
- **三档安全沙箱**：标准 / 严格 / 锁定，支持 Bubblewrap/Seatbelt 系统级沙箱
- **全渠道接入**：Web UI、CLI、Slack/Discord/Telegram/Teams、飞书/钉钉/企微/QQ
- **20+ LLM 供应商**：OpenRouter、OpenAI、Anthropic、Ollama、DeepSeek 等

### ⚡ 2026-08-12 源码级复核（修正与补全）

> 上面的旧笔记来自公众号转述，本次直接分析 GitHub 源码 + arXiv 论文后修正：

| 旧笔记说法 | 源码级事实（v0.5.2 / v4.2 路由器） |
|:-----------|:----------------------------------|
| T0 是本地模型档 | ❌ T0-T3 是 **thinking_mode（思维级别）**，不是档位；档位是 **C0-C3**（legacy T0-T3 别名→C0-C3），另有 image_model 档 |
| 分类器 3 维 | ❌ 实际：LightGBM 主头 + 辅助头 + MLP 集成，输入 BGE 语义嵌入（ONNX INT8）+ **390 维特征** |
| 决策延迟「零延迟」 | ✅ 全本地 CPU 推理，prompt 不出机器（分类决策在设备端） |
| 路由时机「每次对话请求」 | ✅ 每轮 Turn 路由，且**历史感知**（前 N 轮路由决策入特征 + 轨迹稳定性 + sticky 防抖）|
| GitHub 链接缺失 | ✅ https://github.com/opensquilla/opensquilla（Apache-2.0, 6.5k+ stars）|
| 无论文 | ✅ 技术报告 [Agentic Routing: The Harness-Native Data Flywheel](https://arxiv.org/abs/2607.11399)（2026-07-13）|
| 未提数据飞轮 | ✅ **self_learning 模块**（capture→dataset→train→promotion），标签来自执行环境 |
| 未提自适应提示 | ✅ 每档附带 thinking_mode（T0-T3）+ prompt_policy（P0-P2），系统提示随复杂度缩放 |
| 未提基准 | ✅ PinchBench 1.2.1：路由 0.9251 分/$0.688 vs Opus 4.7 单模型 0.9255 分/$6.233（同分 1/9 成本）|

**结论**：公众号旧笔记的「思维深度维度、LightGBM+ONNX 可行性、微内核架构」判断方向正确，但具体档位/特征描述需以源码为准（详见 `02-existing-solutions.md` 第 6️⃣ 节完整分析）。

---

*持续更新中...*
