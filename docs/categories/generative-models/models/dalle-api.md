# DALL-E 3 (API)

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | DALL-E 3 (API) |
| **作者/团队** | OpenAI |
| **参数规模** | 闭源 API 服务 |
| **开源协议** | 闭源商业 API |
| **API 入口** | [OpenAI Docs](https://platform.openai.com/docs/guides/images) |
| **论文原文** | [2303.15464](https://arxiv.org/abs/2303.15464) |

## 简介

OpenAI 的 DALL-E 3 文生图 API。基于 Rectified Flow + T5-XXL 编码器，在提示遵循和排版能力上有质的飞跃。通过 ChatGPT 自动优化提示词，叠加 HD 质量选项可生成高分辨率细节丰富的图像。是目前最流行的商用文生图服务之一。

## 核心亮点

- 深度文本理解 — 支持长句复杂提示
- 排版生成能力大幅提升
- ChatGPT 自动优化提示词（提示重写功能）
- 内置 Safety Checker
- vivid / natural 两种风格选项

## 使用方式

- **[API]**: `client.images.generate(model="dall-e-3", prompt="...")`
- **[尺寸]**: 1024x1024 / 1792x1024 / 1024x1792
- **[质量]**: `quality="standard"` 或 `"hd"`
- **[格式]**: `response_format="b64_json"` 或 `"url"`

## 评估结果

- T2I-CompBench: 0.70
- 排版正确率: ~60%
- 视觉吸引力: 优于 DALL-E 2 / SDXL

---

*此页面的模型信息由 AI Research Tracker 自动维护，建议访问 OpenAI 官方文档获取最新信息。*
