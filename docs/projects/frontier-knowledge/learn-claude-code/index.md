# 🤖 learn-claude-code — Harness 工程从 0 到 1

> **来源**：https://github.com/shareAI-lab/learn-claude-code
> **状态**：🟢 已收录 · **更新**：2026-08-07

## 项目档案

| 项目 | 信息 |
|:-----|:-----|
| ⭐ Stars | 73.3k |
| 🍴 Forks | 11.9k |
| 语言 / 许可证 | Python / MIT |
| 主页 | learn.shareai.run |

---

## 一句话

**Bash is all you need** —— 一个从 0 到 1 手写类 Claude Code 的「Agent Harness（智能体外壳）」教学项目。

---

## 核心理念

1. **Agency 来自模型训练，不来自代码编排。** 模型是司机，Harness 是车。
2. **Agent 产品 = 模型 + Harness。** 模型负责感知、推理、行动；Harness 提供环境。
3. 批判「拖拽式 Agent 平台」——if-else 分支拼 LLM 调用只是「华丽的 shell script」，不是 agent。

### Harness 的组成

```
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions

    Tools:          file I/O, shell, network, database, browser
    Knowledge:      product docs, domain references, API specs
    Observation:    git diff, error logs, browser state
    Action:         CLI commands, API calls, UI interactions
    Permissions:    sandbox isolation, approval workflows
```

### 核心循环（永不改变）

```python
def agent_loop(messages):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS,
        )
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return
        # ...执行工具、追加结果、循环
```

**循环属于 agent，机制属于 harness。** 每课在循环上叠一层机制。

---

## 20 课要点速览

| 课 | 主题 | 核心机制 | 口号 |
|:--|:-----|:--------|:-----|
| s01 | Agent Loop | `while True` + `stop_reason` | One loop & Bash is all you need |
| s02 | Tool Use | `TOOL_HANDLERS` 分发表 | Adding a tool = adding one handler |
| s03 | Permission | `PermissionRule` 审批管线 | Set boundaries first, then grant freedom |
| s04 | Hooks | `PreToolUse` / `PostToolUse` | Hook around the loop, never rewrite the loop |
| s05 | TodoWrite | 先计划后执行 | An agent without a plan drifts |
| s06 | Subagent | 干净上下文隔离 | Big tasks split small |
| s07 | Skill Loading | 按需注入知识 | Load knowledge on demand |
| s08 | Context Compact | 多层压缩策略 | Context always fills up |
| s09 | Memory | 选择/提取/整合三子系统 | Remember what matters |
| s10 | System Prompt | 运行时拼装 | Prompts are assembled at runtime |
| s11 | Error Recovery | 重试/换路/升级 | Errors aren't the end |
| s12 | Task System | 文件持久化任务图 | Big goals break into small tasks |
| s13 | Background Tasks | 线程 + 通知队列 | Slow ops go background |
| s14 | Cron Scheduler | 定时触发 | Fire on schedule |
| s15 | Agent Teams | 消息总线 + 收件箱 | Too big for one agent |
| s16 | Team Protocols | 固定请求-回复格式 | Teammates need shared rules |
| s17 | Autonomous Agents | 空闲循环 + 自动认领 | Teammates check the board |
| s18 | Worktree Isolation | 任务-目录绑定 | Each works in its own directory |
| s19 | MCP Plugin | 外部工具接入 | Plug in more via MCP |
| s20 | Comprehensive | 所有机制汇于一循环 | Many mechanisms, one loop |

---

## 学习路径（6 阶段）

1. **核心能力**（s01-s03）：让 Agent 行动（Loop → 工具 → 权限）
2. **复杂工作**（s05/s06/s08）：计划、子代理、上下文压缩
3. **记忆与恢复**（s09-s11）：记忆、系统提示词、错误恢复
4. **长任务**（s12-s14）：任务系统、后台任务、Cron
5. **多 Agent 协作**（s15-s18）：团队、协议、自主、隔离
6. **扩展与组装**（s07/s19/s20）：Skills、MCP、综合

---

## 生态延伸

- **Kode Agent CLI**：开源编码代理 CLI（GLM / MiniMax / DeepSeek 等开源模型）
- **kode-agent-sdk**：将 Agent 能力嵌入应用的独立库
- **claw0**：姊妹教程——常驻助手（heartbeat + cron + IM + memory + soul）

---

## 📌 对「多智能体平台」项目的启示

- s12-s18 提供了完整的多 Agent 编排思路：任务图、消息总线、自主认领、worktree 隔离
- s03/s04 的权限与 Hooks 是生产级安全管控的蓝本
- s19 MCP 是可扩展工具接入的标准路径
