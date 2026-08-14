# 🛡️ 安全沙箱 Sandbox

> **领域**：Agentic Infra / Agent 安全
> **状态**：🟢 已收录 · **更新**：2026-08-07
> **相关**：[NVIDIA Secure Agent Workspace（完整参考架构）](nvidia-secure-agent-workspace.md) · [总览](index.md)

---

## 一句话

安全沙箱是 Agent 执行时的**运行时强制层**：让自主行为受环境约束（runtime-bounded），而不是仅靠提示词约束（prompt-dependent）。

---

## 为什么 ToB 必须有沙箱

企业不敢部署不可信的 Agent。核心顾虑：

| 顾虑 | 沙箱的答案 |
|:-----|:-----------|
| 提示注入劫持 Agent | 策略由控制面签发，与提示词无关 |
| 数据外泄 | 出口 deny-by-default + 凭据代理（Agent 拿能力不拿密钥） |
| 越权/意外写入 | 敏感写操作人工审查 |
| 被劫持 Agent 攻击内网 | 网络边界白名单 + 出站限制 |
| VM 内被攻破 | 运行时沙箱 + VM 边界双层遏制 |

---

## 沙箱的关键设计（来自 NVIDIA SAW）

```
控制面（运维持有）: 签名策略编写/分发/审计/人工审查
        ↓ 签发
运行时沙箱（VM 内）: 在工具调用边界强制策略
   ├─ deny-by-default 出口
   ├─ 凭据代理（改写 Authorization 头）
   ├─ 受保护路径 deny-write（.bashrc / MCP 配置）
   └─ 系统二进制只读（LSM 强制）
```

> 🔗 架构细节（7 条不变量、逻辑平面、成熟度模型）→ [NVIDIA Secure Agent Workspace 完整解读](nvidia-secure-agent-workspace.md)

---

## 落地选型

| 方案 | 说明 | 适用 |
|:-----|:-----|:-----|
| **NVIDIA OpenShell** | SAW 官方参考实现，运行时沙箱 | 与 NVIDIA 栈深度绑定 |
| **自研沙箱** | 基于 gVisor / Firecracker / LSM 等 | 需要定制策略、兼容已有栈 |
| **第三方云沙箱** | 云厂商托管方案 | 快速上线、免运维 |

---

## 📌 对平台的意义

- **信任前提**：ToB 客户（金融/政务/医疗）没有沙箱不会采购
- **差异化**：Dynamo 解决「快不快」，Sandbox 解决「敢不敢用」——后者是 Agentic Infra 的护城河
- **合规**：审计日志 + 人工审查门满足监管要求

---

## 📚 参考

- NVIDIA Secure Agent Workspace Reference Design（官方文档）
- NVIDIA OpenShell（github.com/NVIDIA/OpenShell）
- 本库完整解读：[NVIDIA Secure Agent Workspace →](nvidia-secure-agent-workspace.md)
