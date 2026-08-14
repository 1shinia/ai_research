# YOLOv8

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | YOLOv8 |
| **作者/团队** | Ultralytics |
| **参数规模** | n/s/m/l/x (3.2M - 57.3M) |
| **开源协议** | AGPL-3.0 |
| **模型权重** | [GitHub](https://github.com/ultralytics/ultralytics) |
| **ModelScope** | [YOLOv8 on ModelScope](https://modelscope.cn/search?search=ultralytics+yolov8) |
| **论文原文** | [2305.00622](https://arxiv.org/abs/2305.00622) |

## 简介

Ultralytics 发布的 YOLOv8 目标检测模型，YOLO 系列的集大成者。支持检测、分割、分类、姿态估计和跟踪等多种任务，以极致的推理速度和开箱即用的 API 著称。COCO 精度最高 53.9% mAP，推理仅需 1.9ms。

## 核心亮点

- C2f 模块 + DFL 损失 — 精度显著提升
- 统一任务 API：检测 / 分割 / 分类 / 姿态 / OBB
- 支持 ONNX / TensorRT / CoreML / TFLite 导出
- Mosaic / MixUp / Copy-Paste 数据增强
- 完善的日志和可视化（W&B / Comet / TensorBoard）

## 使用方式

- **[安装]**: `pip install ultralytics`
- **[训练]**: `yolo train model=yolov8n.pt data=coco8.yaml epochs=100`
- **[预测]**: `yolo predict model=yolov8x.pt source="image.jpg"`
- **[导出]**: `yolo export model=yolov8n.pt format=onnx`

## 评估结果

- COCO mAP: 37.3% (n) → 53.9% (x)
- 推理速度: 0.6ms (n) → 1.9ms (x) on T4
- 模型大小: 3.2M (n) → 57.3M (x) 参数

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
