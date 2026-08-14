## LLM & VLM 模型效果评估

> 大语言模型（LLM）与视觉语言模型（VLM）的效果评估体系。LLM 侧重于语言理解、推理、代码、指令遵循等能力；VLM 则在此基础上叠加了视觉感知、多模态推理、视觉定位等维度。

---

## 一、大语言模型（LLM）评估

### 1.1 评估维度全景

LLM 评估已从单一的语言建模困惑度演变为多维能力矩阵：

| 能力维度 | 代表 Benchmark | 指标 | 说明 |
|---------|---------------|------|------|
| **综合知识** | MMLU / MMLU-Pro | Accuracy | 57 学科，大学级知识广度 |
| **中文知识** | C-Eval / CMMLU | Accuracy | 中国教育体系知识 |
| **通用推理** | AGIEval | Accuracy | 公务员考试/竞赛级推理 |
| **数学推理** | GSM8K / MATH / AIME | Pass@1 | 小学到竞赛级数学 |
| **逻辑推理** | BBH (BIG-Bench Hard) | Accuracy | 23 个挑战性推理任务 |
| **代码生成** | HumanEval / MBPP / SWE-bench | Pass@1 | 函数级到仓库级编码 |
| **指令遵循** | MT-Bench / AlpacaEval / IFEval | 评分/Length-Ctrl WinRate | 多轮对话质量 |
| **中文对齐** | SuperCLUE | 综合评分 | 中文多维度评估 |
| **长上下文** | RULER / Needle-in-Haystack | 检索/召回 | 32K-1M+ 上下文长度 |
| **安全与对齐** | HarmBench / TruthfulQA | 拒绝率/准确率 | 有害内容拒绝与真实性 |

### 1.2 2025-2026 旗舰模型 Benchmark 排行榜

| 模型 | MMLU-Pro | AIME 2025 | GPQA Diamond | SWE-bench Verified | HumanEval | MATH-500 |
|------|:--------:|:---------:|:------------:|:------------------:|:---------:|:--------:|
| **Claude Opus 4** | **92.4%** | 54.0% | **86.8%** | **72.3%** | 96.8% | 97.2% |
| **GPT-5.4 Pro** | 91.8% | 55.0% | 86.2% | 71.8% | **97.5%** | **98.1%** |
| **Gemini 3.1 Pro** | 91.2% | **56.5%** | 85.3% | 69.5% | 96.2% | 97.0% |
| **DeepSeek-V4-Pro** | 90.1% | 53.8% | 83.5% | 70.1% | 93.8% | 96.3% |
| **Qwen3-235B-A22B** | 88.5% | 48.2% | 80.1% | 61.3% | 91.5% | 94.6% |
| **Llama 4 Scout** | 86.7% | 42.0% | 76.8% | 55.1% | 88.2% | 91.8% |
| **Mistral Large 3** | 85.9% | 44.5% | 78.2% | 57.8% | 89.5% | 92.3% |

> **数据说明**：以上数据综合自各模型官方技术报告及 Open LLM Leaderboard（截至 2026 年 7 月）。DeepSeek-V4-Pro 数据来自其官方技术报告（arxiv 2607.07658）及 ai-insight.org 评测档案。

### 1.3 常见 Leaderboard 平台

| 平台 | 地址 | 特点 |
|------|------|------|
| **Open LLM Leaderboard** | huggingface.co/spaces/open-llm-leaderboard | 开源模型标准化评测 |
| **LMSYS Chatbot Arena** | lmarena.ai | 人类偏好 Elo 评分 |
| **Artificial Analysis** | artificialanalysis.ai | 推理速度 + 质量综合 |
| **DataLearner** | datalearner.com/benchmarks | 中文 LLM 排行榜 |
| **SuperCLUE** | superclue.ai | 中文综合能力评测 |
| **LiveCodeBench** | livecodebench.github.io | 代码能力持续评测 |

### 1.4 关键 Benchmark 详解

#### MMLU → MMLU-Pro → MMLU-Redux

```
MMLU (57科, 选择题)       → 模型接近饱和（~90%）
MMLU-Pro (增加难度, 10选项) → 去饱和，区分度更好
MMLU-Redux (精选+纠错)    → 修正标注错误
```

2026 年头部模型 MMLU-Pro 得分约 88-92%，差距缩小，**需关注 GPQA（研究生级科学推理）和 SWE-bench（真实编程）这些更难的任务**。

#### 数学推理：GSM8K → MATH → AIME

```
GSM8K（小学应用题）SOTA ~98% → 已饱和
MATH（竞赛级）SOTA ~97% → 接近饱和
AIME（AMC 12 以上选拔赛）SOTA ~56% → 仍有提升空间
```

AIME 已成为区分旗舰模型的关键战场：Gemini 3.1 Pro 以 56.5% 领先。

#### SWE-bench：代码能力的「高考」

SWE-bench 要求模型根据 GitHub Issue 自动修复真实代码仓库的 Bug。2025-2026 年旗舰模型得分从 30% 跃升至 70%+，但仍远低于人类工程师水平（~85%）。

| 模型 | SWE-bench Verified |
|------|:------------------:|
| Claude Opus 4 | 72.3% |
| GPT-5.4 Pro | 71.8% |
| DeepSeek-V4-Pro | 70.1% |
| Agent 模式（GPT-5 + 工具） | 81.2% |

#### 长上下文：RULER 与 Needle-in-Haystack

| 模型 | 支持长度 | Needle @ 全文检索 |
|------|---------|:----------------:|
| GPT-5.4 Pro | 128K → 1M | 98.7% |
| Gemini 3.1 Pro | 1M | 99.1% |
| DeepSeek-V4-Pro | 128K | 97.3% |
| Qwen3-235B | 128K → 1M | 97.8% |

### 1.5 中文场景评估

| Benchmark | 说明 | SOTA 模型 | 得分 |
|-----------|------|----------|:----:|
| **C-Eval** | 中国多学科知识 | Qwen3-235B | 92.3% |
| **CMMLU** | 中文 MMLU | DeepSeek-V4-Pro | 91.8% |
| **SuperCLUE** | 中文综合能力 | DeepSeek-V4-Pro | 91.5 |
| **CLUE** | 自然语言理解 | - | - |

> 中文场景下，DeepSeek-V4-Pro 和 Qwen3 系列表现突出，与英文旗舰差距显著缩小。

---

## 二、视觉语言模型（VLM）评估

### 2.1 评估维度全景

VLM 评估在 LLM 基础上增加了视觉相关能力：

| 能力维度 | 代表 Benchmark | 指标 | 说明 |
|---------|---------------|------|------|
| **多学科理解** | MMMU / MMMU-Pro | Accuracy | 大学级多模态理解 |
| **视觉感知** | MMBench / SEED-Bench | Accuracy | 细粒度视觉理解 |
| **视觉推理** | MathVista / ChartQA | Accuracy | 图表/数学视觉推理 |
| **文档理解** | DocVQA / InfoVQA | ANLS | 文档/信息图问答 |
| **图文匹配** | COCO Caption / Flickr30K | CIDEr / BLEU | 图片描述生成 |
| **场景文本** | OCRBench | Accuracy | 自然场景文字识别 |
| **视觉定位** | RefCOCO / Visual7W | Accuracy | 指代表达理解 |
| **视频理解** | Video-MME / EgoSchema | Accuracy | 视频时序理解 |

### 2.2 2025-2026 主流 VLM 模型排行榜

| 模型 | 视觉编码器 | MMMU-Pro | MMBench | MathVista | DocVQA | 特点 |
|------|-----------|:--------:|:-------:|:---------:|:-----:|------|
| **GPT-5.4 Pro Vision** | - | **94.0%** | **91.2%** | **76.8%** | **96.5%** | 通用 SOTA |
| **Gemini 3.1 Pro** | - | 83.9% | 88.5% | 73.4% | 94.2% | 多模态均衡 |
| **Claude Opus 4** | - | 82.1% | 89.3% | 71.5% | 95.0% | 文档理解强 |
| **Qwen2.5-VL-72B** | 自研 ViT | 78.5% | 86.2% | 69.1% | 93.5% | 开源 SOTA |
| **InternVL3-78B** | InternViT-6B | 76.8% | 84.7% | 67.8% | 92.1% | 开源，多模态 |
| **LLaVA-OneVision-72B** | SigLIP | 72.4% | 82.0% | 64.3% | 90.2% | 开源社区标杆 |
| **DeepSeek-VL3** | - | 75.2% | 83.5% | 66.8% | 91.7% | 中文场景强 |
| **MiniCPM-o 2.6** | SigLIP | 65.8% | 79.4% | 58.5% | 87.6% | 端侧部署 |

> 注：MMMU-Pro 是 MMMU 的升级版，过滤了纯文本可解的题目、扩展选项至 10 个、引入纯视觉输入。GPT-5.4 Pro 以 94.0% 大幅领先。

### 2.3 关键 Benchmark 详解

#### MMMU → MMMU-Pro

```
MMMU（57科, 大学级, 选择题）
  └─ 2026 年旗舰 SOTA ~80%（GPT-5.4 Pro）
MMMU-Pro（难度升级）
  └─ 过滤纯文本可解题（强制视觉理解）
  └─ 选项从 4→10 个（降低猜测率）
  └─ 所有模型下降 16.8%-26.9%
  └─ GPT-5.4 Pro 以 94.0% 大幅领先
```

#### MMBench：中文 VLM 基准

- 约 3,000 道中文多模态选择题
- 涵盖关系推理、属性识别、空间关系、计数等
- 开源模型在此基准上与闭源差距最小

#### MathVista：视觉数学推理

- 结合图表、几何图形、文本的数学推理
- 2026 年最佳开源模型得分 ~69%，闭源 ~77%
- 仍是最具挑战性的 VLM 评测之一

### 2.4 视频理解评估

| 基准 | 任务 | SOTA | 得分 |
|------|------|------|:----:|
| **Video-MME** | 多模态视频理解 | Gemini 3.1 Pro | 84.5% |
| **EgoSchema** | 第一人称视频理解 | GPT-5.4 Pro | 82.1% |
| **ActivityNet-QA** | 开放域视频问答 | GPT-5.4 Pro | 78.3% |

---

## 三、评估方法论

### 3.1 不同规模模型的评估选择

```
模型规模        推荐 Benchmark
────────────────────────────────
旗舰级         MMLU-Pro + AIME + SWE-bench + GPQA
(>100B)        MMMU-Pro + MathVista（VLM）
中型           MMLU + GSM8K + HumanEval + BBH
(7B-70B)       MMBench + DocVQA（VLM）
小型           ARC-C + HellaSwag + PIQA
(<7B)          SEED-Bench 简化版（VLM）
```

### 3.2 评估注意事项

1. **数据泄露**：部分模型在预训练中可能见过 benchmark 数据，建议使用 MMLU-Pro、MMMU-Pro 等更难泄露的版本
2. **多次采样**：代码/数学任务建议 Pass@K（K≥5）而非单次 Pass@1
3. **标准化提示**：不同提示格式可能导致 5-15% 的分数波动，必须固定
4. **公平对比**：开源模型使用官方推荐的推理配置（温度、top-p、max_tokens）

### 3.3 评估工具

| 工具 | 用途 | 地址 |
|------|------|------|
| **LM Evaluation Harness** | LLM 标准化评测框架 | github.com/EleutherAI/lm-evaluation-harness |
| **VLMEvalKit** | VLM 评测工具包 | github.com/open-compass/VLMEvalKit |
| **OpenCompass** | 全模型评测平台 | github.com/open-compass/opencompass |
| **Gaia** | 通用 Agent 评测 | github.com/gaia-benchmark/gaia |

---

## 📈 评估结果

> TODO：待补充实际评测数据。

## 📚 参考资料

- MMLU: Measuring Massive Multitask Language Understanding (Hendrycks et al., 2020)
- MMLU-Pro: A More Robust and Challenging Benchmark (Wang et al., 2024)
- GSM8K: Training Verifiers to Solve Math Word Problems (Cobbe et al., 2021)
- MATH: Measuring Mathematical Problem Solving (Hendrycks et al., 2021)
- HumanEval: Evaluating Large Language Models Trained on Code (Chen et al., 2021)
- SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (Jimenez et al., 2023)
- AIME & GPQA: IMO & Graduate-Level Reasoning - 各模型技术报告
- MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark (Yue et al., 2023)
- MMMU-Pro: A More Robust Multi-discipline Multimodal Understanding Benchmark (Yue et al., 2024)
- MMBench: Is Your Multi-modal Model an All-around Player? (Liu et al., 2023)
- MathVista: Evaluating Mathematical Reasoning in Visual Contexts (Lu et al., 2023)
- DeepSeek-V4-Pro 技术报告: arxiv.org/abs/2607.07658 (2026)
- ai-insight.org: DeepSeek V4 评测榜单深度档案 (2026)
- benchlm.ai: MMMU-Pro Leaderboard & Scores (July 2026)
- codesota.com: The State of Multimodal AI: What VLMs Can Actually Do (2026)
