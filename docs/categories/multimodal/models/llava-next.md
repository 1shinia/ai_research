# LLaVA-NeXT

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | LLaVA-NeXT |
| **作者/团队** | 威斯康星大学 / Microsoft |
| **参数规模** | 7B / 13B / 34B |
| **开源协议** | Apache 2.0 |
| **模型权重** | [HuggingFace](https://huggingface.co/liuhaotian/llava-v1.6-mistral-7b) |
| **ModelScope** | [liuhaotian/llava-v1.6-mistral-7b](https://modelscope.cn/models/liuhaotian/llava-v1.6-mistral-7b) |
| **论文原文** | [2310.03744](https://arxiv.org/abs/2310.03744) |

## 简介

LLaVA-NeXT 是开源视觉语言模型的代表作品。通过简单的 MLP 桥接将视觉编码器与 LLM 连接，仅需约 600K 视觉指令数据即可训练出性能优异的 VLM。34B 版本达到接近 GPT-4V 的多模态水平。

## 核心亮点

- MLP 桥接 — 简洁高效的图文连接方案
- 支持高分辨率输入（4 倍于 LLaVA-1.5）
- 视觉编码器 + LLM 解耦设计，易于替换升级
- 数据高效 — 仅需 600K 视觉指令数据
- 社区生态极其活跃，大量衍生模型

## 使用方式

- **[GitHub]**: https://github.com/haotian-liu/LLaVA
- **[安装]**: `pip install git+https://github.com/haotian-liu/LLaVA.git`
- **[推理]**: `python -m llava.serve.cli --model-path liuhaotian/llava-v1.6-mistral-7b --image-file example.jpg`
- **[HuggingFace]**: 模型权重在 hf.co/liuhaotian 发布

## 评估结果

- MMBench: 76.7% (Mistral-7B)
- MM-Vet: 46.6% (Mistral-7B)
- ScienceQA: 90.6% (Mistral-7B)
- TextVQA: 69.6% (Mistral-7B)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
