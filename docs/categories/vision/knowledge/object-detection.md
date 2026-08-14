# 目标检测

## 1. 任务定义

给定一张图像，检测其中所有物体的类别和位置（边界框）。

输出：每个物体 = (类别, x1, y1, x2, y2, 置信度)

## 2. 方法演进

### 2.1 两阶段检测器

R-CNN -> Fast R-CNN -> Faster R-CNN -> Cascade R-CNN

核心：先提出候选区域 (Region Proposal)，再分类和回归

### 2.2 单阶段检测器

YOLO 系列、SSD、RetinaNet

核心：直接预测边界框和类别，无需候选区域

### 2.3 YOLO 系列

| 版本 | 年份 | 创新点 |
|------|------|--------|
| YOLOv1 | 2016 | 第一个单阶段检测器 |
| YOLOv3 | 2018 | 多尺度预测 |
| YOLOv5 | 2020 | 工程优化 |
| YOLOv8 | 2023 | 解耦头 + Anchor-free |
| YOLOv10 | 2024 | 无 NMS |

### 2.4 Transformer 检测器

DETR：用 Transformer 的编码器-解码器架构做检测

- 无需锚框、无需 NMS
- 通过二部图匹配训练
- 后续改进：Deformable DETR、DINO、Co-DETR

## 3. 评估指标

| 指标 | 说明 |
|------|------|
| mAP | 平均精度均值 |
| AP50 | IoU=0.5 时的精度 |
| FPS | 推理速度 |

## 4. 延伸阅读

- [SAM 论文](../papers/2023-04-05-sam.md)

---

*最后更新：2026-06-22*
