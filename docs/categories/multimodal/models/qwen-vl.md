# Qwen2-VL

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Qwen2-VL |
| **作者/团队** | 阿里云 Qwen 团队 |
| **参数规模** | 2B / 7B / 72B |
| **开源协议** | Apache 2.0 |
| **模型权重** | [HuggingFace](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct) |
| **ModelScope** | [qwen/Qwen2-VL-7B-Instruct](https://modelscope.cn/models/qwen/Qwen2-VL-7B-Instruct) |
| **论文原文** | [2409.12191](https://arxiv.org/abs/2409.12191) |

## 简介

阿里云 Qwen 团队的第二代视觉语言模型。原生动态分辨率支持任意尺寸图像，在图像理解、文档 OCR 和视频理解上达到领先水平。支持 8K 视频帧输入，中英文多模态能力均表现优异。

## 核心亮点

- 原生动态分辨率 — 处理任意尺寸图像
- 多图理解和视频理解能力
- 支持 8K 视频帧输入
- 72B 版本多项基准超过 GPT-4V / Gemini Pro
- 文档 OCR 能力尤其突出

## 使用方式

- **[HuggingFace]**: `model = Qwen2VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")`
- **[vLLM]**: 支持 Qwen2-VL 部署
- **[DashScope API]**: 通过阿里云灵积调用 Qwen-VL-Max
- **[官方 Demo]**: https://huggingface.co/spaces/Qwen/Qwen2-VL-7B-Demo

## 评估结果

- MMBench: 88.1% (72B)
- MathVista: 71.4% (72B)
- DocVQA: 97.1% (72B)
- Video-MME: 78.0% (72B)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
