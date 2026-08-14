# Qwen-Max (API)

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | Qwen-Max (API) |
| **作者/团队** | 阿里云 Qwen 团队 |
| **参数规模** | 闭源 API 服务 (MoE 架构) |
| **开源协议** | 闭源商业 API (DashScope) |
| **API 入口** | [DashScope](https://dashscope.aliyun.com) |
| **ModelScope** | [qwen/Qwen-Max](https://modelscope.cn/models/qwen/Qwen-Max) |
| **论文原文** | [2407.10770](https://arxiv.org/abs/2407.10770) |

## 简介

阿里云 DashScope 的 Qwen-Max API 服务。千亿参数 MoE 模型，中文场景表现尤为出色。128K 上下文，支持函数调用 / RAG / Agent 架构。提供阿里云级 SLA 保障。

## 核心亮点

- 千亿参数 MoE 架构
- 128K 上下文窗口
- 中文能力突出，适合中国业务场景
- 支持函数调用 (Function Calling)
- DashScope 提供阿里云级 SLA 和运维

## 使用方式

- **[SDK]**: `pip install dashscope`
- **[调用]**: `from dashscope import Generation; Generation.call(model="qwen-max", messages=[...])`
- **[插件]**: 计算器 / 搜索 / 绘图等插件能力
- **[控制台]**: https://dashscope.aliyun.com

## 评估结果

- MMLU: 87.4% (Qwen-Max)
- GSM8K: 95.8% (Qwen-Max)
- 中文综合能力: 领先于同等规模模型
- 推理速度: 低延迟，适合在线服务

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 DashScope 官方文档获取最新信息。*
