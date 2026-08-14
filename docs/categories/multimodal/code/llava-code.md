# LLaVA 代码库

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | LLaVA 代码库 |
| **语言** | Python |
| **用途** | 视觉语言模型训练推理 |
| **GitHub** | [haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA) |
| **许可证** | Apache 2.0 |

## 简介

LLaVA 官方代码库，实现了从零训练到部署的全流程视觉语言模型 (VLM) 解决方案。提供训练 VLM 的标准流程（视觉编码器 + 桥接 MLP + LLM），支持 LLaMA / Mistral / Qwen 等多种 LLM 作为语言骨干。

## 核心功能

- 端到端 VLM 训练流程
- 多模态指令数据构建工具
- LoRA 微调支持
- 模型服务化（Gradio WebUI / CLI）
- 支持 GPT-4V 数据生成

## 快速开始

```bash
git clone https://github.com/haotian-liu/LLaVA.git
cd LLaVA
pip install -e .

# CLI 推理
python -m llava.serve.cli --model-path liuhaotian/llava-v1.6-mistral-7b --image-file example.jpg
```

## 使用场景

- 训练自定义视觉语言模型
- 多模态对话和图像理解
- 文档分析和 OCR 应用

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
