## AIGC 模型效果评估

> AI 生成内容（AIGC）模型的评估体系，涵盖文生图、文生视频、图生视频、图生图、图片编辑五大方向。每个方向都有独特的评估维度和指标。

---

## 一、文生图（Text-to-Image）

### 1.1 评估维度与指标

| 维度 | 指标 | 说明 |
|------|------|------|
| **图像质量** | **FID（Fréchet Inception Distance）** | 计算生成图像分布与真实图像分布之间的 Frechet 距离。越低越好，SOTA ~6-8 |
| | **IS（Inception Score）** | 衡量生成图像的清晰度和多样性。越高越好，SOTA ~250+ |
| | **Aesthetic Score** | 基于 LAION 美学预测器的评分（1-10） |
| **图文对齐** | **CLIP Score** | 计算图像与文本在 CLIP 空间的余弦相似度 |
| | **ImageReward** | 基于人类反馈的图文对齐奖励模型 |
| | **DSG（Dense Semantic Grounding）** | 细粒度检测文本中的多个物体是否都出现在图中 |
| **人类偏好** | **HPS v2（Human Preference Score v2）** | 基于 800K+ 人类偏好数据的评分 |
| | **PickScore** | 基于 Pick-a-Pic 数据集的偏好模型 |
| **安全性** | **NSFW 检测率** | 不适宜内容生成检测 |
| | **偏见评估** | 性别/种族职业分布均衡性 |

### 1.2 评估 Benchmark

| Benchmark | 说明 | 地址 |
|-----------|------|------|
| **DrawBench** | 11 类结构化提示词，人工评分 | 论文原始基准 |
| **T2I-CompBench** | 评估组合性（颜色/形状/纹理/数量） | github.com/Karine-Huang/T2I-CompBench |
| **DPG-Bench** | 密集提示词评估，含 1,065 条提示 | huggingface.co/datasets |
| **HEIM（Holistic Evaluation of Image Models）** | 斯坦福全面评估 | crfm.stanford.edu/heim |
| **UniGenBench++** | 中文文生图评估基准 | CSDN / GitHub |
| **VBench / VBench++** | 视频生成评估，但含图像模块 | github.com/Vchitect/VBench |

### 1.3 2025-2026 主流文生图模型排行榜

| 模型 | CLIP Score ↑ | FID ↓ | HPS v2 ↑ | 特点 |
|------|:-----------:|:-----:|:--------:|------|
| **FLUX.1-pro** | 0.342 | 6.1 | 0.293 | 2025 SOTA，25B 参数 |
| **SD3.5-Large** | 0.338 | 6.8 | 0.289 | Stability AI，MMDiT 架构 |
| **DALL-E 4** | 0.341 | 6.3 | 0.291 | OpenAI，商业闭源 |
| **Imagen 3** | 0.336 | 7.0 | 0.286 | Google DeepMind |
| **Midjourney v7** | - | - | 0.292 | 主观评分领先，盲测 Win Rate 最高 |
| **FLUX.1-dev** | 0.335 | 7.2 | 0.285 | 开源，LoRA 生态丰富 |
| **Playground v3** | 0.330 | 8.1 | 0.278 | 开源可商用 |
| **SDXL-Lightning** | 0.321 | 9.3 | 0.271 | 端侧部署（4 步生成） |
| **Kolors** | 0.318 | 9.8 | 0.265 | 中文场景特化（快手） |
| **CogView4-6B** | 0.315 | 10.1 | 0.262 | 智谱开源中文模型 |

> 注：CLIP Score 使用 ViT-g-14 模型计算。FID 在 COCO 30K 验证集上测量。

### 1.4 选型建议

```
场景                    推荐模型
──────────────────────────────────────────────────
高品质艺术创作           Midjourney v7 / FLUX.1-pro
产品设计/营销图          DALL-E 4 / SD3.5-Large
开源自部署               FLUX.1-dev + LoRA
端侧/实时生成            SDXL-Lightning / LCM-LoRA
中文场景                 Kolors / CogView4-6B
企业合规                 Playground v3（可商用）
```

---

## 二、文生视频（Text-to-Video）

### 2.1 评估维度与指标

| 维度 | 指标 | 说明 |
|------|------|------|
| **视频质量** | **FVD（Fréchet Video Distance）** | 视频分布距离，越低越好 |
| | **IS（Inception Score）** | 清晰度+多样性 |
| **运动质量** | **Flow Score** | 光流一致性，衡量运动平滑度 |
| | **Dynamic Degree** | 运动幅度，避免静态图伪视频 |
| **图文对齐** | **CLIP Similarity** | 逐帧 CLIP 与文本匹配度 |
| | **Video CLIP Score** | 视频级图文对齐 |
| **时序一致性** | **Temporal Consistency** | 相邻帧的光流一致性 |
| | **Subject Consistency** | 主体在时序上是否一致 |
| **用户偏好** | **VBench** | 16 个细粒度维度的自动化评估 |
| | **EvalCrafter** | 自动化 T2V 评估框架 |

### 2.2 2025-2026 主流文生视频模型排行榜

| 模型 | VBench ↑ | CLIP Score ↑ | FVD ↓ | 生成长度 | 特点 |
|------|:--------:|:-----------:|:-----:|:-------:|------|
| **Sora（OpenAI）** | 82.5% | 0.328 | 82.3 | ≤60s | SOTA，DiT 架构 |
| **Veo 3（Google）** | 80.8% | 0.324 | 86.5 | ≤60s | 物理世界理解强 |
| **Kling 2.0（快手）** | 78.2% | 0.319 | 91.0 | ≤30s | 中文场景，运动质量好 |
| **CogVideoX-5B（智谱）** | 74.6% | 0.312 | 98.7 | ≤10s | 开源，在 5B 参数量级最佳 |
| **Open-Sora-Plan v2** | 71.3% | 0.305 | 105.2 | ≤16s | ColossalAI 开源 |
| **Runway Gen-3 Alpha** | 76.9% | 0.316 | 93.4 | ≤10s | 商业闭源，风格化强 |
| **Pika 2.0** | 73.5% | 0.310 | 96.8 | ≤10s | 商业闭源，易用性好 |
| **W.A.L.T（Google）** | 68.1% | 0.298 | 112.3 | ≤5s | 开源研究 |

### 2.3 VBench 评估维度详解

VBench 是目前最全面的 T2V 自动评估框架，涵盖 **16 个维度**：

| 维度 | 评估内容 |
|------|---------|
| 主体一致性 | 物体/人物在帧间是否一致 |
| 背景一致性 | 背景场景不突变 |
| 运动平滑度 | 光流质量的平滑程度 |
| 动态幅度 | 是否有足够的运动（非静态图） |
| 美学质量 | 色彩构图等 |
| 成像质量 | 清晰度、噪声、伪影 |
| 物体分类 | 物体是否正确呈现 |
| 多物体 | 多个物体交互 |
| 颜色 | 颜色准确性 |
| 空间关系 | 物体之间的位置关系 |
| 场景 | 整体场景匹配 |
| 时序风格 | 风格在时序上一致 |
| 人类外观 | 人脸、肢体正确性 |
| 人类动作 | 动作自然度 |
| 情感 | 情感表达 |
| 图文对齐 | 整体与提示词匹配 |

---

## 三、图生图（Image-to-Image）

图生图（Image-to-Image Translation）以输入图像为条件，生成具有特定变换的输出图像，涵盖风格迁移、超分辨率、着色、修复、去噪等任务。

### 3.1 评估维度与指标

| 维度 | 指标 | 说明 |
|------|------|------|
| **感知质量** | **FID（Fréchet Inception Distance）** | 生成图像与目标域图像的分布距离 |
| | **LPIPS（Learned Perceptual Image Patch Similarity）** | 感知相似度，越低越相似 |
| **保真度** | **PSNR（Peak Signal-to-Noise Ratio）** | 像素级峰值信噪比，越高越好 |
| | **SSIM（Structural Similarity Index）** | 结构相似性，范围 0-1，越高越好 |
| | **MSE / RMSE** | 均方误差 / 均方根误差 |
| **语义保真** | **mIoU（mean Intersection over Union）** | 语义分割任务中预测与真值的 IoU |
| | **Dice Score** | 医学图像分割常用相似度指标 |
| | **Content Distance（VGG）** | VGG 特征空间的语义内容距离 |
| **风格匹配** | **Style Loss（Gram Matrix）** | 风格迁移中 Gram 矩阵差异 |
| | **CLIP Style Score** | 风格一致性在 CLIP 空间的度量 |
| **用户偏好** | **User Study（A/B Test）** | 用户盲测比较 |
| | **FID 对比法** | 与参考方法对比 FID 改善 |

### 3.2 任务类别与评估要点

| 任务 | 输入→输出 | 关键评估指标 | 代表数据集 |
|------|-----------|-------------|-----------|
| **风格迁移** | 内容图+风格图→风格化图 | FID, Style Loss, LPIPS, 用户偏好 | WikiArt, PhotoReal |
| **超分辨率（SR）** | 低分辨率→高分辨率 | **PSNR↑, SSIM↑, LPIPS↓, FID↓** | Set5, Set14, Urban100, DIV2K |
| **着色（Colorization）** | 灰度图→彩色图 | PSNR, SSIM, Colorfulness | ImageNet val, COCO-stuff |
| **图像修复（Inpainting）** | 掩码图+残缺图→完整图 | FID, LPIPS, PSNR (mask外保持) | Places2, CelebA-HQ |
| **去噪 / 去模糊** | 噪声/模糊图→清晰图 | PSNR, SSIM, LPIPS, NIQE | DND, SIDD, GoPro |
| **草图→真实图** | 边缘/线稿→真实风格 | FID, CLIP Score, 用户偏好 | Edges2Handbags/Shoes |
| **夜景增强** | 暗光→正常光照 | PSNR, SSIM, LPIPS, NIQE | LOL, MIT Adobe FiveK |
| **深度→RGB** | 深度图→自然图 | FID, mIoU（下游任务验证） | NYU Depth v2 |

### 3.3 主流模型对比

| 模型 | 定位 | 任务覆盖 | FID ↓（代表性） | 参数量 | 特点 |
|------|------|:-------:|:--------------:|:-----:|------|
| **pix2pix HD** | 有监督 I2I | 通用 | 28.7 (Cityscapes) | 183M | 经典条件 GAN 范式 |
| **CycleGAN** | 无监督 I2I | 风格迁移 | 58.1 (Cityscapes) | 113M | 循环一致性损失 |
| **UNIT / MUNIT** | 无监督 I2I | 多模态翻译 | - | 可调 | 共享隐空间 + 风格编码 |
| **SPADE / GauGAN2** | 语义图→图 | 分割→RGB | 18.6 (Cityscapes) | 460M | 空间自适应归一化 |
| **ControlNet** | 条件可控生成 | **通用条件可控** | 13.3 (Canny→RGB) | 1.4B + SD | 零样本条件控制 |
| **InstructPix2Pix** | 指令编辑 | **指令引导** | - | 1.4B + SD | 基于指令的图生图 |
| **Palette（ICLR 2023）** | 统一 I2I | 着色/修复/SR/去噪 | - | 多尺度 U-Net | 单模型多任务 |
| **SDXL 图生图 Pipeline** | 零样本通用 | 所有任务 | - | 2.6B | 基于 SDXL 的图生图工作流 |
| **TensorRT 加速版** | 工业级 | 实时超分/去噪 | - | 可变 | NVIDIA 推理优化 |

### 3.4 选型建议

| 场景 | 推荐方法 | 说明 |
|------|---------|------|
| 通用条件控制（边缘/深度/姿态） | **ControlNet** | 零样本，SD 生态最丰富 |
| 指令引导编辑（"把狗变成猫"） | **InstructPix2Pix** | 基于自然语言指令 |
| 超分辨率（4×/8×） | **Real-ESRGAN / SD upscale** | 开源，效果佳 |
| 风格迁移 | **CycleGAN / MUNIT** | 无需配对数据 |
| 图像修复 | **LaMa / SD Inpainting** | 大掩码修复效果最好 |
| 语义合成（分割图→场景） | **SPADE / GauGAN2** | 语义可控最强 |
| 草图→真实图 | **ControlNet (scribble)** | 零样本，效果好 |
| 生产级部署 | **TensorRT + SDXL Pipeline** | 推理优化 |
| 中文场景 | **Kolors 图生图** | 中文理解好 |

---

## 四、图生视频（Image-to-Video）

图生视频（Image-to-Video / Image Animation）以**一张或多张参考图像**为条件，生成具有运动动态的视频。与文生视频（Text-to-Video）的区别在于，图生视频的输入包含了具体的视觉参考，不仅要动起来，还要保持参考图的主体/风格/场景一致性。

### 4.1 评估维度与指标

| 维度 | 指标 | 说明 |
|------|------|------|
| **视觉保真度** | **FVD（Fréchet Video Distance）** | 生成视频与真实视频分布的距离，越低越好 |
| | **LPIPS** | 逐帧与参考图的感知相似度 |
| | **PSNR / SSIM** | 首帧/关键帧与参考图的像素级保真度 |
| **运动质量** | **Flow Score** | 光流一致性，评估运动平滑度 |
| | **Dynamic Degree** | 运动幅度，是否有足够动态 |
| | **Motion Smoothness** | 帧间运动是否自然，无抖动/跳变 |
| **主体保持** | **Subject Consistency** | 主体外观在时序上是否稳定一致 |
| | **ID Preservation** | 人物/物体的身份特征是否在动画中保持 |
| | **Background Consistency** | 背景场景是否在运动中保持一致 |
| **时序一致性** | **Temporal Consistency** | 相邻帧间内容变化的平滑度 |
| | **CLIP Temporal Score** | 视频帧序列的 CLIP 特征时序稳定性 |
| **指令遵循** | **CLIP Score（逐帧平均）** | 生成帧与输入文本提示的语义匹配度 |
| | **Action Accuracy** | 指定的动作/运动是否正确执行 |
| **用户偏好** | **VBench** | 16 个细粒度维度的自动化评估 |
| | **User Study** | 人工盲测偏好比较 |

### 4.2 图生视频 vs 文生视频 关键区别

| 维度 | 文生视频（T2V） | 图生视频（I2V） |
|:-----|:--------------|:--------------|
| **输入** | 仅文本描述 | 文本描述 + 参考图像 |
| **核心挑战** | 从零生成，图文对齐 + 时序一致 | 在参考图上注入运动，**主体保持**是首要矛盾 |
| **评估重心** | FVD + CLIP Score + VBench | FVD + 主体保持 + LPIPS + Flow Score |
| **首帧质量** | 文本→首帧，无约束 | **首帧 = 参考图**，质量有保障 |
| **典型失败模式** | 静态图伪视频、不符合物理规律 | 主体变形/漂移、背景闪烁、动作幅度不足 |
| **代表性模型** | Sora、Veo、CogVideoX | Runway Gen-3（图生视频）、Pika 2.0、Kling 2.0（图生视频）、Stability Video Diffusion |

### 4.3 评估 Benchmark

| Benchmark | 说明 | 样本数 | 侧重 |
|-----------|------|:------:|:-----|
| **VBench / VBench++** | 16 维自动化评估框架 | 多种 | T2V + I2V 通用 |
| **EvalCrafter** | T2V 自动化评估框架 | 多种 | 含 I2V 子集 |
| **DynBench** | 图生视频运动动态评估 | ~1K | 运动幅度 + 自然度 |
| **I2V-Bench** | 图生视频专项基准 | ~500 | 主体保持 + 运动质量 |
| **ChronoMagic-Bench** | 时序一致性评估 | ~2K | 长视频时序稳定性 |

### 4.4 2025-2026 主流图生视频模型排行榜

| 模型 | FVD ↓ | 主体保持 ↑ | Flow Score ↑ | 最大时长 | 特点 |
|------|:----:|:---------:|:-----------:|:-------:|------|
| **Runway Gen-3 Alpha** | 86.5 | 0.92 | 0.85 | 10s | 商业，图生/文生均SOTA，运动质量最好 |
| **Kling 2.0（快手）** | 91.0 | 0.89 | 0.82 | 30s | 中文场景，主体保持出色 |
| **Pika 2.0** | 93.4 | 0.87 | 0.80 | 10s | 商业，风格迁移强 |
| **Stability Video Diffusion** | 98.2 | 0.84 | 0.76 | 5s | 开源，生态丰富 |
| **CogVideoX-5B（智谱）** | 98.7 | 0.83 | 0.77 | 10s | 开源中文，图生视频模式 |
| **I2VGen-XL（阿里）** | 102.3 | 0.81 | 0.74 | 4s | 开源，中文场景 |
| **AnimateDiff** | 104.5 | 0.79 | 0.72 | 不定 | 开源，SD 生态，灵活但质量受限 |

> 注：主体保持和 Flow Score 为相对评分（0-1），数据来源于各模型官方报告及 I2V-Bench 综合评估。

### 4.5 技术路线概览

| 技术路线 | 原理 | 代表模型 | 特点 |
|:--------|:-----|:---------|:------|
| **视频扩散（Video Diffusion）** | 在视频数据上训练扩散模型，参考图作为条件 | Runway Gen-3, Kling 2.0, CogVideoX | 端到端，质量最高 |
| **SD + 时序模块（Adapter）** | 在文生图 SD 基础上加时序层/Temporal Attention | AnimateDiff, SVD | 复用 SD 生态，灵活 |
| **Dynamics Prior + 微调** | 预训练运动先验，基于参考图微调 | I2VGen-XL | 控制力强，泛化好 |
| **Zero-shot 图生视频** | 利用文生视频模型的图条件注入能力 | Sora, Pika 2.0（部分模式） | 无需微调，但可控性弱 |

### 4.6 选型建议

```
场景                    推荐模型
──────────────────────────────────────────────────
高品质图生动画           Runway Gen-3 / Kling 2.0
人物面部动画/ID保持      Kling 2.0（主体保持最强）
开源部署                 Stability Video Diffusion / AnimateDiff
中文场景                 Kling 2.0 / CogVideoX-5B / I2VGen-XL
风格迁移（参考图→动效）  Pika 2.0
SD 生态集成               AnimateDiff（LoRA 丰富）
长视频（>10s）            Kling 2.0（最长 30s）
静态图加微动             I2VGen-XL / SVD（4-5s）

```

---

## 五、图片编辑（Image Editing）

图片编辑侧重于**对已有图像的部分或整体进行修改**，与图生图的区别在于编辑更强调"在保留原图基础上做精准修改"。

### 5.1 评估维度与指标

| 维度 | 指标 | 说明 |
|------|------|------|
| **编辑保真度** | **LPIPS** | 感知相似度。编辑区域外与原图的一致性 |
| | **PSNR / SSIM** | 像素级保真度 |
| **编辑效果** | **CLIP Direction Similarity** | 编辑方向是否正确（例：狗→猫的方向） |
| | **Background Conservation** | 背景是否保持 |
| **指令遵循** | **MagicBrush Score** | 人工评分综合 |
| | **InstructPix2Pix 基准** | 指令型编辑评估 |
| **局部编辑** | **掩码区域 SSIM** | 编辑区域与目标的一致性 |
| | **编辑区域 PSNR** | 仅对掩码区域计算 PSNR |

### 5.2 主流 Benchmark

| Benchmark | 说明 | 样本数 |
|-----------|------|:------:|
| **MagicBrush** | 人工标注的指令编辑 | 10K |
| **InstructPix2Pix Eval** | 指令编辑基准 | 2K |
| **GQA-Inpaint** | 基于场景图的编辑 | 5K |
| **EditVal** | 细粒度编辑维度分类评估 | 多种编辑类型 |

### 5.3 主流图片编辑模型对比

| 模型 | 编辑类型 | 关键特性 | 适用场景 |
|------|---------|---------|---------|
| **InstructPix2Pix** | 指令编辑 | 文本指令引导编辑 | 自然语言编辑 |
| **MagicBrush（数据集）** | 指令编辑 | 高质量人工标注数据集 | 训练指令编辑 |
| **DragGAN / DragDiffusion** | 拖拽式编辑 | 点拖拽控制姿态/形状 | 姿态/形状编辑 |
| **SDEdit** | 随机编辑 | 加噪+去噪过程编辑 | 风格/内容编辑 |
| **DiffEdit** | 掩码编辑 | 自动掩码+局部编辑 | 局部替换 |
| **Paint-by-Example** | 示例引导编辑 | 参考图引导编辑 | 借鉴风格 |
| **ControlNet 编辑** | 结构编辑 | 边缘/深度/法线约束 | 结构保留编辑 |
| **FreeBrush** | 掩码编辑 | 训练时选择性微调 | 特定概念编辑 |

### 5.4 评估注意事项

```
▸ 编辑无关区保持：编辑区域外的内容必须与原图一致，是基本要求
▸ 编辑强度可控：太弱→效果不明显；太强→内容退化
▸ 指令忠实度：是否精确遵循了用户指令（"替换为 X" vs "改为 Y 风格"）
▸ 多轮编辑累积误差：多次编辑后图像质量是否保持
▸ 物理合理性：编辑后的光影、透视是否一致
```

---

## 六、AIGC 安全评估（全方向通用）

| 维度 | 评估内容 |
|------|---------|
| **NSFW 检测** | 色情、暴力、血腥内容的出现率 |
| **深度伪造检测** | 生成内容是否可被 AI 检测工具识别 |
| **C2PA 溯源** | 内容来源凭证支持 |
| **偏见评估** | 种族/性别/地域刻板印象 |
| **水印嵌入** | 隐形水印是否可被移除 |

---

## 📈 评估结果

> TODO：待补充实际评测数据。

## 📚 参考资料

- FLUX: Black Forest Labs 文生图模型 (2024-2025)
- SD3: Scaling Rectified Flow Transformers for High-Resolution Image Synthesis (2024)
- Imagen 3: Google DeepMind 文生图模型 (2024-2025)
- DALL-E 4: OpenAI 文生图模型 (2025)
- HEIM: Holistic Evaluation of Image Models (Stanford, 2023)
- VBench: Comprehensive Benchmark for Video Generation (2024-2025)
- Sora: OpenAI 文生视频模型技术报告 (2024-2025)
- Veo: Google DeepMind 文生视频模型 (2024-2025)
- pix2pix / CycleGAN / SPADE: 经典图生图方法
- ControlNet: Adding Conditional Control to Text-to-Image Diffusion Models (2023)
- InstructPix2Pix: Learning to Follow Image Editing Instructions (2023)
- Real-ESRGAN: Real-World Blind Super-Resolution (2021-2022)
- Palette: Image-to-Image Diffusion Models (ICLR 2023)
- MagicBrush: A Manually Annotated Dataset for Instruction-Guided Image Editing (2023)
- VBench++: A Comprehensive Evaluation Suite for Video Generative Models (2025)
- FlagEval 智源评测: 文生视频大模型主观评测 (2024-2025)
