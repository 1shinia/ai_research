# 本周高影响力论文

## 本周记录

被广泛关注、引用或媒体报道的重磅论文。

| 领域 | 论文 | 亮点 |
|:----|:-----|:-----|
| Agent | **MACU**（CMU） | 多Agent协作操控电脑，OSWorld提升25.5%，长任务提速1.5倍 |
| LLM | **FlexMoE**（NUS） | MoE剪枝50%保留99.8%性能，支持实时预算切换 |
| 高效训练 | **Block-GTQ**（港中文） | RoPE感知KV量化，K3V2下DeepSeek-R1从崩溃恢复到接近fp16 |
| 高效训练 | **HyperQuant** | 率失真最优量化管线，4bit下~3.9x近无损压缩 |
| 多模态 | **ProMSA** | 渐进式多模态搜索Agent，TN-GSPO序列RL优化工具调用 |
| 生成式 | **DiT-Reward** | 用DiT生成表征做奖励模型，HPDv2达85.6% |
| 生成式 | **Qwen-Image-Agent**（阿里） | Agent式图像生成，主动补全用户缺失上下文 |
| 机器人 | **HumanoidUMI** | 用VR采集人形机器人训练数据，无需真机 |
| 机器人 | **WOLF-VLA** | 人形全身最优控制+语言指令行走的VLA |
| 安全 | **REALM** | 首个物理世界VLM红队统一基准 |
| 安全 | **WAICO**（AI治理） | 全球AI治理"第二极"形成的系统分析 |

## 详情

---

### 🔥 最受关注：MACU（Multi-Agent Computer Use）

- **机构**：CMU（Jing Yu Koh, Ruslan Salakhutdinov, Daniel Fried）
- **arXiv**：[2606.01533](https://arxiv.org/abs/2606.01533)
- **意义**：首次将多Agent协作引入计算机使用任务，DAG分解+并行子代理架构显著超越单代理方法
- **影响**：OSWorld+3.4~25.5%、长时Web导航任务完成时间缩短约1.5倍，代码已开源

### 🔥 FlexMoE：MoE模型一次性多预算剪枝

- **机构**：NUS（Fan Mo, Yang You等）
- **arXiv**：[2606.27866](https://arxiv.org/abs/2606.27866)
- **意义**：一次训练产出所有预算的子网络，Qwen2-57B-A14B剪枝50%保留99.8%性能
- **影响**：对大规模MoE部署极具实用价值，支持实时在线预算切换

### 🔥 Block-GTQ：RoPE感知KV量化

- **机构**：港中文（Fengfeng Liang, Jiaya Jia等）
- **arXiv**：[2606.24033](https://arxiv.org/abs/2606.24033)
- **意义**：首次感知RoPE块结构的量化分配，K3V2下DeepSeek-R1从0.0恢复至51.7（fp16为54.2）
- **影响**：Qwen2.5-3B 128K上下文峰值内存从56GB降至20GB

### 🔥 Qwen-Image-Agent（阿里）

- **arXiv**：[2606.26907](https://arxiv.org/abs/2606.26907)
- **意义**：首次将图像生成建模为Agent过程，主动补全用户上下文缺失
- **影响**：同时发布IA-Bench评估基准，代表T2I从"提示词工程"向"Agent式生成"的范式转变

### 🔥 HumanoidUMI

- **arXiv**：[2606.27239](https://arxiv.org/abs/2606.27239)
- **意义**：借鉴UMI思路降低人形机器人训练数据采集门槛，VR设备代替真机遥操作
- **影响**：对解决人形机器人数据稀缺瓶颈具有里程碑意义

---

*每周更新 — 2026-06-29*
