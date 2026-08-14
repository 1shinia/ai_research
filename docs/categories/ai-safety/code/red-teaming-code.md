# 红队测试框架

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | 红队测试框架 |
| **语言** | Python |
| **用途** | LLM 安全红队测试 |
| **GitHub** | [LLM Red-Teaming 工具](https://github.com/llm-attacks/llm-attacks) |
| **许可证** | MIT |

## 简介

红队测试框架是用于自动化发现 LLM 安全漏洞的工具集。通过对抗性提示注入 / 越狱攻击 / 偏见检测等方法系统性地评估模型安全性。主流工具包括 Garak / PyRIT / HarmBench 等。

## 核心功能

- **对抗性提示注入**：绕过安全限制的提示技术
- **越狱攻击**: 多轮诱导 / 角色扮演攻击
- **偏见检测**: 评估模型在不同人口群体上的表现差异
- **毒性测试**: 检测模型输出的仇恨/毒性言论
- **自动红队**: 使用 LLM 生成对抗性测试用例

## 快速开始

```bash
# Garak 红队测试框架
pip install garak
garak --model_type huggingface --model_name Qwen/Qwen2.5-7B --probes all

# HarmBench 基准测试
git clone https://github.com/centerforaisafety/HarmBench
```

## 使用场景

- LLM 产品上线前安全评估
- 模型安全能力基准测试
- 安全对齐效果验证

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
