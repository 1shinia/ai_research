# 工具使用 (Tool Use)

## 1. 概述

让 Agent 能够调用外部工具（API、函数、数据库）来完成任务。

## 2. 工具使用方式

### 2.1 Function Calling

模型输出结构化的函数调用：

```json
{
  "name": "search",
  "arguments": {
    "query": "latest AI papers",
    "limit": 10
  }
}
```

### 2.2 Code Interpreter

模型生成代码并执行：

```python
import math
result = math.sqrt(144)
print(result)  # 12.0
```

### 2.3 API 调用

模型调用外部 API：

```
Action: call weather_api(city="Beijing")
Observation: {"temp": 25, "condition": "sunny"}
```

## 3. 工具选择策略

| 策略 | 说明 | 适用 |
|------|------|------|
| 精确匹配 | 工具名完全匹配 | 简单场景 |
| 语义匹配 | 用嵌入匹配工具描述 | 大量工具 |
| 学习选择 | 训练模型选择工具 | 复杂场景 |

## 4. 常见工具

| 工具类型 | 例子 | 用途 |
|----------|------|------|
| 搜索 | Google, Bing | 信息检索 |
| 计算 | Python, Calculator | 数学计算 |
| 数据库 | SQL, Vector DB | 数据查询 |
| 文件 | File System, Git | 文件操作 |
| 网络 | HTTP, WebSocket | 网络请求 |

## 5. 延伸阅读

- [Toolformer 论文](../papers/2023-02-20-toolformer.md)
- [ReAct 论文](../papers/2022-10-06-react.md)

---

*最后更新：2026-06-22*
