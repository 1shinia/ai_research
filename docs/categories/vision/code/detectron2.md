# Detectron2

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Detectron2 |
| **语言** | Python / C++ |
| **用途** | 目标检测与分割框架 |
| **GitHub** | [facebookresearch/detectron2](https://github.com/facebookresearch/detectron2) |
| **许可证** | Apache 2.0 |

## 简介

Detectron2 是 Meta AI 开发的下一代目标检测与分割框架。继承并发展了 Mask R-CNN 系列，提供 Faster R-CNN / Mask R-CNN / Cascade R-CNN / RetinaNet 等丰富模型。采用模块化设计，易于研究和产品化。

## 核心功能

- 丰富的检测/分割/姿态估计模型库
- 支持 COCO / LVIS / Cityscapes 等数据集
- DensePose / Panoptic FPN 等先进方法
- 模块化可插拔设计
- 分布式训练支持

## 快速开始

```bash
pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu118/torch2.0/index.html

python demo/demo.py --config-file configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml \
  --input input.jpg --output output.jpg --opts MODEL.WEIGHTS detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl
```

## 使用场景

- 目标检测/分割研究和应用
- 自定义数据集训练
- 作为检测 backbone 集成到更大系统

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
