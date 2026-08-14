# CLIP

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | CLIP |
| **作者/团队** | OpenAI |
| **参数规模** | ViT-B/32 / ViT-B/16 / ViT-L/14 |
| **开源协议** | MIT |
| **模型权重** | [HuggingFace](https://huggingface.co/openai/clip-vit-large-patch14) |
| **ModelScope** | [openai/clip-vit-large-patch14](https://modelscope.cn/models/openai/clip-vit-large-patch14) |
| **论文原文** | [2103.00020](https://arxiv.org/abs/2103.00020) |

## 简介

CLIP (Contrastive Language-Image Pre-training) 是 OpenAI 提出的多模态对比学习模型。通过 4 亿图文对的对比学习，将图像和文本映射到同一语义空间。零样本 ImageNet 分类达 76.2%，是跨模态学习的里程碑工作。

## 核心亮点

- 对比学习目标：拉近匹配图文对，推远不匹配对
- 零样本分类 — 无需任何训练数据即可分类
- 多模态语义空间，支持图文互检
- 4 亿图文对训练数据 (WIT)
- 启发了大量多模态学习和对比学习方法

## 使用方式

- **[HuggingFace]**: `from transformers import CLIPModel; model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")`
- **[GitHub]**: https://github.com/openai/CLIP
- **[零样本分类]**: 计算图像与所有类别文本的余弦相似度
- **[图文检索]**: 提取图像和文本嵌入后计算相似度排序

## 评估结果

- ImageNet zero-shot: 76.2% (ViT-L/14)
- CIFAR-100 zero-shot: 80.0% (ViT-L/14)
- Flickr30K text->image R@1: 64.9%
- COCO text->image R@1: 50.2%

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
