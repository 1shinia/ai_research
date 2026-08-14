# 本周新增方法路线

## 本周记录

本周出现的新算法、新架构、新训练范式。

| 领域 | 方法 | 类型 | 一句话简介 |
|:----|:-----|:----|:----------|
| LLM | **Step-DPO** | 训练方法 | 步骤级偏好优化，DPO从结果扩展到推理过程 |
| LLM | **Token-Efficient RL (S-GRPO/T-SPMO)** | 训练方法 | 选择性Token级RL优化，LoRA下也能做推理RL |
| LLM | **FlexMoE（嵌套剪枝）** | 架构优化 | 一次性多预算MoE子网络导出 |
| RL | **PEBS** | RLHF校准 | 经验贝叶斯收缩校准标注者偏差，闭式后处理 |
| RL | **RAC** | RL算法 | 延迟感知RLHF修正，队列+非负核+裁剪残差注入 |
| RL | **GEOALIGN** | 数据筛选 | 几何空间检测并剔除方向冲突的rollout |
| Agent | **ProMSA** | Agent范式 | 渐进式多模态搜索Agent，序列RL优化工具调用 |
| Agent | **MACU（DAG并行）** | Agent架构 | 管理Agent+DAG子代理并行执行计算机使用任务 |
| 多模态 | **MJEPA** | 预训练方法 | 联合嵌入预测架构扩展到音视频跨模态 |
| 多模态 | **Steering VLM with JSAE** | 可解释方法 | 联合稀疏自编码器实现VLM跨模态特征干预 |
| 生成式 | **DiT-Reward** | 奖励建模 | 生成模型的表征也能评估生成结果质量 |
| 生成式 | **Qwen-Image-Agent** | 生成范式 | Agent式T2I，主动补全上下文代替提示词工程 |
| 高效训练 | **InfoKV** | KV压缩 | 信息论信号（预测不确定性）融合到KV压缩 |
| 高效训练 | **Block-GTQ** | KV量化 | RoPE频率块级贪心比特分配 |
| 高效训练 | **HyperQuant** | 量化管线 | 哈达玛变换+最优格量化+Rice编码统一管线 |
| 机器人 | **HumanoidUMI** | 数据采集 | VR采集人类全身轨迹→人形机器人技能 |
| 机器人 | **WOLF-VLA** | VLA控制 | 全身最优控制+VLA实现人形语言指令行走 |
| 机器人 | **运行时编排系统** | 行为编排 | Affordance Templates+行为树+运行时感知编辑 |
| 安全 | **SAE可解释性框架** | 评估方法 | 首个基于人类标注验证SAE可解释性的系统框架 |

## 详情

### 训练方法类

- **Step-DPO**：将DPO从最终答案比较扩展到每步推理的偏好优化。在MATH上比DPO提升近3%（70.8%），仅需10K数据对和<500步训练。
- **Token-Efficient RL (S-GRPO/T-SPMO)**：在LoRA低参数训练下，通过对输出Token智能子集操作实现LLM推理RL。Qwen2-1.5B在SVAMP上从46%提升至70%+。
- **GEOALIGN**：在表征空间检测方向不一致的rollout，剔除噪声训练数据。不修改RL算法本身，即插即用。

### Agent架构类

- **MACU**：管理Agent将任务分解为DAG，子代理并行执行节点，管理Agent动态修订DAG。计算机使用任务的单→多Agent演进。
- **ProMSA**：将多模态RAG建模为渐进式搜索代理行为，引入TN-GSPO序列级RL优化工具调用策略。

### KV Cache压缩（本周最热方向之一）

本周有三篇重磅KV Cache工作：

1. **InfoKV**：首次系统地将预测不确定性作为信号引入KV压缩。在Llama-3.1/3.2、DeepSeek-R1上一致超越注意力基线。
2. **Block-GTQ**：首个RoPE块感知的KV量化。K3V2下DeepSeek-R1从0.0恢复至51.7。
3. **HyperQuant**：哈达玛变换+最优格量化+Rice编码的统一管线。4bit下线性层~3.9x无损压缩。

### 人形机器人（本周第二热方向）

三篇重磅工作聚焦人形机器人：

1. **HumanoidUMI**：VR采集→映射到人形全身控制，数据采集门槛大幅降低。
2. **WOLF-VLA**：全身最优控制合成训练数据→VLA学习语言指令行走。
3. **运行时编排系统**：已在6款真实人形机器人（Atlas、Valkyrie、H1-2等）上部署验证。

---

*每周更新 — 2026-06-29*
