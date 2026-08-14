# ResNet 系列

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | ResNet 系列 |
| **作者/团队** | Microsoft Research / Kaiming He |
| **参数规模** | 18 / 34 / 50 / 101 / 152 layers |
| **开源协议** | MIT |
| **模型权重** | [torchvision](https://pytorch.org/vision/stable/models/resnet.html) |
| **ModelScope** | [torch/resnet50](https://modelscope.cn/models/torch/resnet50) |
| **论文原文** | [1512.03385](https://arxiv.org/abs/1512.03385) |

## 简介

ResNet（残差网络）是何恺明等人提出的深度学习架构。通过残差连接 (Skip Connection) 解决了深层网络的退化问题，使训练数百层网络成为可能。ResNet 是 CV 领域最具影响力的工作之一，奠定了现代深度网络的基础设计范式。

## 核心亮点

- 残差学习 (Residual Learning) — 解决网络退化问题
- Bottleneck 设计减少参数量和计算量
- 几乎所有深度学习框架都内置的核心 backbone
- 作为基础骨架用于分类 / 检测 / 分割 / 人脸识别
- ILSVRC 2015 分类、检测、定位三项冠军

## 使用方式

- **[torchvision]**: `from torchvision.models import resnet50; model = resnet50(pretrained=True)`
- **[TensorFlow]**: `from tensorflow.keras.applications import ResNet50; model = ResNet50(weights="imagenet")`
- **[迁移学习]**: 替换最后一层全连接即可适配新任务
- **[特征提取]**: 取 `avgpool` 层输出作为 2048 维特征向量

## 评估结果

- ImageNet Top-1: 77.6% (ResNet-50) → 80.4% (ResNet-152)
- COCO mAP: 39.1% (Faster R-CNN + ResNet-50-FPN)
- 参数量: 25.6M (ResNet-50) / 60.2M (ResNet-152)

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
