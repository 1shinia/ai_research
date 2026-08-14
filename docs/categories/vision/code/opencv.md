# OpenCV

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | OpenCV |
| **语言** | C++ (Python/Java bindings) |
| **用途** | 计算机视觉库 |
| **GitHub** | [opencv/opencv](https://github.com/opencv/opencv) |
| **许可证** | Apache 2.0 |

## 简介

OpenCV (Open Source Computer Vision Library) 是最流行的开源计算机视觉库。提供 2500+ 优化算法，涵盖图像处理、特征检测、相机标定、目标跟踪等。是 CV 工程师最基础和最常用的工具库。

## 核心功能

- 图像 I/O 和基本处理（缩放/旋转/滤波/颜色空间）
- 特征检测（SIFT / ORB / SURF）和特征匹配
- 相机标定和 3D 重建
- 目标跟踪和背景分离
- 传统机器学习（SVM / KNN / 决策树）

## 快速开始

```python
import cv2

img = cv2.imread("image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)
cv2.imwrite("edges.jpg", edges)
```

## 使用场景

- 图像预处理管道
- 实时视频处理
- 嵌入式视觉系统（OpenCV 有优化版）
- 传统 CV 算法快速实现

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
