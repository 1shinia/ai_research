# SAM 2

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | SAM 2 |
| **作者/团队** | Meta AI |
| **参数规模** | Hiera-B/L/tiny |
| **开源协议** | Apache 2.0 |
| **模型权重** | [HuggingFace](https://huggingface.co/facebook/sam2-hiera-large) |
| **ModelScope** | [facebook/sam2-hiera-large](https://modelscope.cn/models/facebook/sam2-hiera-large) |
| **论文原文** | [2408.00714](https://arxiv.org/abs/2408.00714) |

## 简介

Meta 发布的"分割一切"模型第二版 (Segment Anything 2)。统一了图像和视频分割能力，通过 Hiera 骨干网络 + 流式记忆模块实现视频实时分割。SA-V 数据集包含 51K 视频和 600K mask 标注。

## 核心亮点

- 统一图像和视频分割架构
- 实时交互式分割（点 / 框 / 掩码提示）
- 流式记忆模块处理视频时序和遮挡
- SA-V 数据集：最大视频分割数据集
- 推理速度 >30 FPS（Hiera-B 版本）

## 使用方式

- **[GitHub]**: https://github.com/facebookresearch/sam2
- **[HuggingFace]**: `from transformers import SamModel; model = SamModel.from_pretrained("facebook/sam2-hiera-large")`
- **[安装]**: `pip install git+https://github.com/facebookresearch/sam2.git`
- **[推理]**: `python scripts/amg.py --checkpoint sam2_hiera_large.pt --input images/`

## 评估结果

- SA-V mIoU: 81.3%（视频分割）
- HQ-YTVIS mAP: 54.2%（视频实例分割）
- DAVIS mIoU: 86.8%（视频目标分割）
- 推理速度 >30 FPS（Hiera-B）

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 HuggingFace 官方页面获取最新信息。*
