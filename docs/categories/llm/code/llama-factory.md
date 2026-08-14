# LLaMA-Factory

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | LLaMA-Factory |
| **语言** | Python |
| **用途** | 大模型微调框架 |
| **GitHub** | [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) |
| **许可证** | Apache 2.0 |

## 简介

LLaMA-Factory 是一个统一的 LLM 微调框架，支持 LLaMA / Qwen / Mistral 等上百种模型架构。覆盖 SFT / DPO / PPO / KTO 等训练方式，支持 LoRA / QLoRA / Full Fine-tune 等参数效率微调。提供 Web UI 界面，零代码即可完成模型微调。

## 核心功能

- 上百种模型架构支持
- LoRA / QLoRA / GaLore / LISA 等参数高效微调
- SFT / DPO / PPO / KTO / SimPO 等训练算法
- Web UI 操作界面
- 支持 DeepSpeed / FSDP 分布式训练

## 快速开始

```bash
# 安装
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e .

# Web UI 启动
python src/train_web.py

# 命令行微调
llamafactory-cli train examples/train_lora/llama3_lora_sft.yaml
```

## 使用场景

- 对 LLM 进行指令微调以适配特定任务
- DPO 对齐训练提升模型帮助性
- 多模型多数据集批量实验管理

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
