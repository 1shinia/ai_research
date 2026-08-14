# MMDetection

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | MMDetection |
| **语言** | Python |
| **用途** | 目标检测工具箱 |
| **GitHub** | [open-mmlab/mmdetection](https://github.com/open-mmlab/mmdetection) |
| **许可证** | Apache 2.0 |

## 简介

OpenMMLab 系列中的目标检测框架。集成了 300+ 目标检测模型和 60+ 算法，涵盖单阶段 / 两阶段 / Anchor-Free / Transformer 检测器。提供统一的训练和评估流水线。

## 核心功能

- 300+ 模型和 60+ 算法
- 统一的 Config 配置系统
- 丰富的数据增强（Mosaic / MixUp / Albu）
- 多任务扩展（MMSegmentation / MMPose / MMTracking）
- 完善的基准和模型 zoo

## 快速开始

```bash
pip install -U openmim
mim install mmdetection

mmdetection/demo.py image demo.jpg configs/yolo/yolov8_l_syncbn_fast_8xb16-500e_coco.py yolov8_l_500e_coco.pth
```

## 使用场景

- 检测算法的快速实现和对比
- 竞赛和业务中的检测方案
- 教学和研究中的标准评测平台

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
