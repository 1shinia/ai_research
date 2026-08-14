# Vision Transformer (ViT)

## 1. 核心思想

将 Transformer 直接应用于图像分类，证明注意力机制在视觉领域同样有效。

## 2. 架构

### 2.1 图像分 Patch

将 H x W 图像切成 P x P 的 patch：

    num_patches = (H/P) * (W/P)

每个 patch 展平后通过线性投影得到 patch embedding。

### 2.2 整体流程

1. 图像 -> 分 patch -> 线性投影 -> patch embeddings
2. 添加 [CLS] token 和位置编码
3. 通过 Transformer 编码器
4. [CLS] token 输出 -> 分类头

### 2.3 与 NLP Transformer 的对比

| 方面 | NLP | Vision |
|------|-----|--------|
| 输入 | 词 token | patch embedding |
| 序列长度 | 可变 | 固定 (num_patches) |
| 位置编码 | 可学习 | 可学习 |
| 输出 | 每个位置 | [CLS] token |

## 3. 关键发现

- **数据规模是关键：** 在大数据集上 ViT 超越 CNN，小数据集上不如
- **Patch 大小：** 16x16 是最佳平衡
- **缩放性：** ViT 的缩放性优于 CNN

## 4. 变体

| 变体 | 创新 |
|------|------|
| DeiT | 知识蒸馏，小数据也能训练 |
| Swin Transformer | 移位窗口注意力，多尺度 |
| BEiT | 掩码图像建模预训练 |
| MAE | 掩码自编码器，高效预训练 |

## 5. 延伸阅读

- [ViT 论文](../papers/2020-10-22-vit.md)
- [CNN](cnn.md)

---

*最后更新：2026-06-22*
