# DINOv2

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | DINOv2 |
| **作者/团队** | Meta AI |
| **参数规模** | ViT-S/B/L/g |
| **开源协议** | Apache 2.0 |
| **模型权重** | [HuggingFace](https://huggingface.co/facebook/dinov2-large) |
| **ModelScope** | [facebook/dinov2-large](https://modelscope.cn/models/facebook/dinov2-large) |
| **论文原文** | [2304.07193](https://arxiv.org/abs/2304.07193) |

## 简介

Meta AI 的视觉自监督学习模型 DINOv2。通过自蒸馏训练从 1.42 亿张未标注图像中学习通用视觉特征，无需任何标注数据即可在 ImageNet 达到 86.3% 的线性探测准确率。特征可直接用于分类 / 分割 / 检索等下游任务。

## 核心亮点

- 纯自监督 — 不需要任何标注数据
- LVD-142M 大规模未标注图像训练
- DINO + iBOT 掩码图像建模联合训练
- 特征空间蕴含丰富语义信息
- 开箱即用：提取特征后线性分类即可

## 使用方式

- **[GitHub]**: https://github.com/facebookresearch/dinov2
- **[HuggingFace]**: `from transformers import AutoModel; model = AutoModel.from_pretrained("facebook/dinov2-large")`
- **[安装]**: `pip install git+https://github.com/facebookresearch/dinov2.git`
- **[特征提取]**: `python dinov2/extract_features.py --input_dir images/ --output_dir features/`

## 评估结果

- ImageNet linear probing: 86.3% (ViT-g)
- ImageNet k-NN: 84.5% (ViT-g)
- ADE20k semantic segmentation mIoU: 59.6%
- NYUv2 depth estimation abs rel: 0.20

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
