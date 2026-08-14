# 开源 RLHF / DPO 模型

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | 开源 RLHF / DPO 模型 |
| **作者/团队** | 社区 / HuggingFace |
| **参数规模** | 视基座模型而定 (LLaMA / Qwen / Mistral) |
| **开源协议** | 视基座模型许可而定 |
| **模型权重** | [HuggingFace Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) |
| **ModelScope** | [ModelScope DPO 模型](https://modelscope.cn/models?search=DPO) |
| **论文原文** | [2406.15037](https://arxiv.org/abs/2406.15037) (Open R1) |

## 简介

使用 RLHF 或 DPO 进行对齐训练的开源模型合集。从数学推理 (DeepSeek-R1) 到指令遵循 (Zephyr / Qwen-Instruct)，社区建立了完善的对齐训练技术栈。GRPO 等高效 RL 方法的引入使模型训练越来越经济。

## 核心亮点

- **DPO (Direct Preference Optimization)** — 无需 Reward Model 的简化对齐方法
- **GRPO (Group Relative Policy Optimization)** — DeepSeek 的无批评者 RL 方法
- **Open R1** — DeepSeek R1 的开源复现项目
- 多项工作证明 1-2 轮 DPO 即可显著提升对齐效果
- TRL / LLaMA-Factory 等工具提供开箱即用的训练支持

## 使用方式

- **[DPO 训练]**: `trl dpo --model_name output/sft --dataset your_pref_dataset`
- **[GRPO]**: 参考 DeepSeek-R1 和 Open R1 项目代码
- **[HF Hub]**: 搜索 "DPO" / "RLHF" 查找社区对齐模型
- **[LLaMA-Factory]**: 一键启动 DPO / PPO / KTO 训练

## 评估结果

- DeepSeek-R1: 超越 OpenAI o1 的推理能力
- Zephyr-7B MT-Bench: 7.34 (7B 级别最佳)
- DPO 训练后胜率提升 ~20% vs SFT

---

*此页面的模型信息由 AI Research Tracker 自动维护。*
