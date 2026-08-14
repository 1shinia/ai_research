---
title: "Scaling Laws for Neural Language Models"
date: 2020-01-23
field: llm
tags: [scaling-law, training, efficiency, foundational]
url: https://arxiv.org/abs/2001.08361
source: arxiv
authors: "Kaplan et al. (OpenAI)"
---


## 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Scaling Laws for Neural Language Models |
| **作者** | Kaplan et al. (OpenAI) |
| **日期** | 2020-01-23 |
| **领域** | llm |
| **标签** | scaling-law,  training,  efficiency,  foundational |
| **链接** | [arXiv](https://arxiv.org/abs/2001.08361) |

## 一句话总结

发现了语言模型性能与模型规模、数据量、计算量之间的幂律关系，为大规模训练提供了理论指导。

## 核心思想

- **幂律关系**：模型性能 (loss) 与参数量 N、数据量 D、计算量 C 之间存在可预测的幂律关系
- **可预测的 Scaling**：在足够大的范围内，性能可以通过幂律公式精确预测
- **数据效率**：模型越大，达到相同性能所需的数据越少
- **与模型宽度/深度无关**：只要参数量相同，宽而浅或窄而深的模型性能相近

## 为什么重要

- 为 GPT-3、Chinchilla 等超大模型提供了理论依据
- 让研究者可以"预算"训练成本
- 引发了"Scaling 是否一切"的激烈讨论
- 直接推动了千亿、万亿参数模型的涌现

## 关键实验结果

- 在 10^7 到 10^10 参数量范围内，loss 与参数量呈幂律关系
- 预测了 GPT-3 的性能，与实际结果高度吻合
