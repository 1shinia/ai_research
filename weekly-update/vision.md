# 👁️ 计算机视觉 (Computer Vision)

> 本周候选：20 篇 | 筛选高影响力：4 篇

---

## 1. Rendering-Aware Bayesian 3D Gaussian Splatting with Native Uncertainty and Adaptive Complexity Control

**📄 arXiv：** [2607.05522](https://arxiv.org/abs/2607.05522v1) | **📅 发布日期：** 2026-07-06  
**👥 作者：** Gaoxiang Jia, Vikram Appia, Junzhou Huang, Xinlei Wang

### 一句话总结
为 3DGS 引入贝叶斯框架，用 Normal-Inverse-Wishart 后验为每个 Gaussian 提供本征不确定性估计，实现主动视角选择和自适应复杂度控制。

### 核心思想
标准 3DGS 训练依赖点估计和手工调参，在稀疏视图下无法识别弱支撑区域。本文用**渲染感知的贝叶斯更新**替代点估计：每个 Gaussian 的均值和协方差由 NIW（Normal-Inverse-Wishart）后验跟踪，渲染器导出的代理统计量作为似然更新。可选 Dirichlet 过程扩展提供组件使用概率信号。重用渲染器的梯度流确保贝叶斯更新与标准 3DGS 训练几乎零开销耦合。

### 为什么重要
稀疏视图 3D 重建是头显/机器人场景刚需，但标准 3DGS 在此设定下会生成漂浮伪影。贝叶斯不确定性为**主动视角选择、重建置信度校准、模型复杂度控制**提供了原生解决方案——这些都是实际部署的核心需求。

### 关键实验
- 固定预算 16→32 主动视角任务：NIW 策略 PSNR +0.453 dB、LPIPS -0.0146，在 29/39 场景-种子对中胜出
- 95% 覆盖误差从 0.796（共享代理）降到 0.046，约改善 17x
- 训练开销仅增加 1.6%，推理时无额外成本

---

## 2. Light-Omni: Reflex over Reasoning in Agentic Video Understanding with Long-Term Memory

**📄 arXiv：** [2607.05511](https://arxiv.org/abs/2607.05511v1) | **📅 发布日期：** 2026-07-06  
**👥 作者：** Chang Nie, Jiaju Wei, Junlan Feng, Chaoyou Fu, Caifeng Shan

### 一句话总结
提出「反射式」而非「侦探式」的视频 Agent——用双状态上下文（全局状态 + 参数化潜状态）替代迭代推理，实现 12.1x 加速、2.6x 显存效率提升。

### 核心思想
现有视频 Agent 依赖反复 search 和证据聚合的迭代推理，本质是在补偿**全局上下文的缺失**。Light-Omni 维护一个有限容量的多模态脚本作为全局状态（通过层次化合并保留最近细节、总结历史事件），并基于全局状态生成参数化潜状态直接驱动动作。推理从「搜索+聚合」变为「单次前向」。

### 为什么重要
视频理解 Agent 的实际瓶颈不是准确率而是速度——消费级场景下用户不能等十几秒。Light-Omni 在多个视频基准上超越 M3-Agent（+2.4% 准确率），同时快了 12 倍，这才是可落地的方案。

### 关键实验
- 多个视频基准：平均准确率 +2.4%（vs M3-Agent）
- 12.1x 推理加速，2.6x GPU 显存效率提升
- 可作为通用记忆系统增强现有 MLLM

---

## 3. SAM-MT: Real-Time Interactive Multi-Target Video Segmentation

**📄 arXiv：** [2607.08688](https://arxiv.org/abs/2607.08688v1) | **📅 发布日期：** 2026-07-09  
**👥 作者：** Ruiqi Shen, Chang Liu, Henghui Ding

### 一句话总结
将 SAM2 扩展为实时多目标视频分割框架，通过解耦掩码注意力将延迟与目标数量解耦，10 个目标仍保持 >36 FPS。

### 核心思想
现有 VOS 方法扩展多目标时需要为每个目标复制单目标处理流程，延迟随目标数线性增长。SAM-MT 用**显式查询**表示不同目标，配合**共享表征**提供全局上下文。通过解耦掩码注意力保持各自身份，稀疏记忆实现稳定时序演化，专用策略处理遮挡和重叠。

### 为什么重要
多目标视频分割是自动驾驶、视频编辑等场景的刚需，但一直受限于「每多一个目标速度就降一格」的架构瓶颈。SAM-MT 从架构层面将延迟与目标数量解耦，是实用化的重要一步。

### 关键实验
- 10 目标 >36 FPS，与单目标基线速度相当
- 保持 SAM2 的分割精度
- 遮挡处理和重叠预防策略有效

---

## 4. GeoGS-SLAM: Geometry-Only Gaussian Splatting for Dense Monocular SLAM

**📄 arXiv：** [2607.07452](https://arxiv.org/abs/2607.07452v1) | **📅 发布日期：** 2026-07-08  
**👥 作者：** Lipu Zhou, Yaoyun Kang, Junxiang Pang, Shengkai Sun, Tingting Bao

### 一句话总结
大胆去掉 3DGS 的外观建模，只用几何参数做稠密单目 SLAM——每个基元的参数量减少 80% 以上，几何收敛更快、对光照变化更鲁棒。

### 核心思想
现有 3DGS 框架同时建模外观和几何。但 SLAM 的核心需求是几何而非照片级渲染。GeoGS 只保留空间参数，通过局部平面初始化对齐 Gaussian 与场景结构，用单视图和多视图几何/光度监督联合优化。提出闭环地图更新策略——全局变换 Gaussian 地图对齐修正位姿，避免多视角修正不一致导致的地图撕裂。

### 为什么重要
这是对 3DGS 方向的一个「必要提问」：到底需不需要外观？对 SLAM 来说答案是不需要——去掉外观不仅省了 80% 参数量，还带来了更好的几何鲁棒性。可能引领一波「Geometry-only 3DGS」子方向。

### 关键实验
- 参数量减少 80%+
- 在合成和真实数据集上优于 SOTA 在线建图效率和几何重建质量
- 闭环地图更新策略有效防止地图撕裂

---

> ⏳ 暂存于 weekly-update/，等待主人手动选择后归档到 papers/ 对应分支。
