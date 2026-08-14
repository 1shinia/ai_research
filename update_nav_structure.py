import re

yml_path = r"D:\ai_research\mkdocs.yml"

with open(yml_path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- LLM ---
llm_new = '''    - 知识库:
      - categories/llm/knowledge/index.md
      - 基础架构:
        - Transformer 架构详解: categories/llm/knowledge/transformer-architecture.md
        - 自注意力机制 (Self-Attention): categories/llm/knowledge/self-attention.md
        - 位置编码 (Positional Encoding): categories/llm/knowledge/positional-encoding.md
        - MoE 混合专家架构: categories/llm/knowledge/moe.md
      - 训练方法:
        - 预训练 (Pre-training): categories/llm/knowledge/pretraining.md
        - 监督微调 (SFT): categories/llm/knowledge/sft.md
        - RLHF 完整流程: categories/llm/knowledge/rlhf-pipeline.md
        - DPO 直接偏好优化: categories/llm/knowledge/dpo.md
      - 推理与优化:
        - 解码策略: categories/llm/knowledge/decoding-strategies.md
        - 上下文扩展技术: categories/llm/knowledge/context-extension.md
        - RAG 检索增强生成: categories/llm/knowledge/rag.md
      - 关键概念:
        - Scaling Law: categories/llm/knowledge/scaling-law.md
        - 涌现能力 (Emergent Abilities): categories/llm/knowledge/emergent-abilities.md
        - In-Context Learning: categories/llm/knowledge/in-context-learning.md
        - 思维链 (Chain-of-Thought): categories/llm/knowledge/chain-of-thought.md
    - 趋势追踪: categories/llm/trends.md
  - 计算机视觉:'''

# Find and replace
old_llm_start = content.find('''    - 知识库:\n      - categories/llm/knowledge/index.md\n      - Transformer 架构: categories/llm/knowledge/transformer-architecture.md''')
if old_llm_start == -1:
    print("ERROR: LLM pattern not found!")
else:
    # Find end of LLM knowledge section (next top-level item)
    llm_end = content.find('    - 趋势追踪: categories/llm/trends.md\n  - 计算机视觉:', old_llm_start)
    old_llm = content[old_llm_start:llm_end + len('    - 趋势追踪: categories/llm/trends.md\n  - 计算机视觉:')]
    content = content.replace(old_llm, llm_new)
    print("LLM replaced OK")

# --- Vision ---
vision_old_start = content.find('''    - 知识库:\n      - categories/vision/knowledge/index.md\n      - CNN 卷积神经网络:')
if vision_old_start == -1:
    # Try a broader match
    vision_old_start = content.find('知识库:\n      - categories/vision/knowledge/index.md')
    
vision_new = '''    - 知识库:
      - categories/vision/knowledge/index.md
      - 基础架构:
        - 卷积神经网络 (CNN): categories/vision/knowledge/cnn.md
        - Vision Transformer (ViT): categories/vision/knowledge/vit.md
      - 核心任务:
        - 目标检测: categories/vision/knowledge/object-detection.md
        - 图像分割: categories/vision/knowledge/image-segmentation.md
      - 生成与 3D:
        - 扩散模型原理: categories/vision/knowledge/diffusion-models.md
        - 3D 重建与渲染: categories/vision/knowledge/3d-reconstruction.md
    - 趋势追踪: categories/vision/trends.md
  - 多模态:'''

old_vision_pattern = '''    - 知识库:
      - categories/vision/knowledge/index.md
      - CNN 卷积神经网络: categories/vision/knowledge/cnn.md
      - Vision Transformer (ViT): categories/vision/knowledge/vit.md
      - 目标检测: categories/vision/knowledge/object-detection.md
      - 图像分割: categories/vision/knowledge/image-segmentation.md
      - 扩散模型: categories/vision/knowledge/diffusion-models.md
      - 3D 重建: categories/vision/knowledge/3d-reconstruction.md
    - 趋势追踪: categories/vision/trends.md
  - 多模态:'''

if old_vision_pattern in content:
    content = content.replace(old_vision_pattern, vision_new)
    print("Vision replaced OK")
else:
    print("WARNING: Vision pattern not found, checking...")
    # Find manually
    idx = content.find('- 计算机视觉:')
    if idx >= 0:
        print(f"  Found at {idx}")
        print(content[idx:idx+500])

# --- Multimodal ---
multimodal_new = '''    - 知识库:
      - categories/multimodal/knowledge/index.md
      - 基础方法:
        - 对比学习 (Contrastive Learning): categories/multimodal/knowledge/contrastive-learning.md
        - 跨模态对齐: categories/multimodal/knowledge/cross-modal-alignment.md
      - 核心架构:
        - 视觉-语言模型: categories/multimodal/knowledge/vision-language-models.md
        - 语音识别基础: categories/multimodal/knowledge/speech-recognition.md
    - 趋势追踪: categories/multimodal/trends.md
  - AI Agent:'''

old_multimodal_pattern = '''    - 知识库:
      - categories/multimodal/knowledge/index.md
      - 对比学习: categories/multimodal/knowledge/contrastive-learning.md
      - 跨模态对齐: categories/multimodal/knowledge/cross-modal-alignment.md
      - 视觉语言模型: categories/multimodal/knowledge/vision-language-models.md
      - 语音识别: categories/multimodal/knowledge/speech-recognition.md
    - 趋势追踪: categories/multimodal/trends.md
  - AI Agent:'''

if old_multimodal_pattern in content:
    content = content.replace(old_multimodal_pattern, multimodal_new)
    print("Multimodal replaced OK")

# --- Agents ---
agents_new = '''    - 知识库:
      - categories/agents/knowledge/index.md
      - 基础能力:
        - 规划与推理: categories/agents/knowledge/planning-reasoning.md
        - 工具使用: categories/agents/knowledge/tool-use.md
      - 核心架构:
        - 记忆机制: categories/agents/knowledge/memory-systems.md
        - 多 Agent 协作: categories/agents/knowledge/multi-agent.md
    - 趋势追踪: categories/agents/trends.md
  - 生成式模型:'''

old_agents_pattern = '''    - 知识库:
      - categories/agents/knowledge/index.md
      - 规划与推理: categories/agents/knowledge/planning-reasoning.md
      - 工具使用: categories/agents/knowledge/tool-use.md
      - 记忆机制: categories/agents/knowledge/memory-systems.md
      - 多 Agent 协作: categories/agents/knowledge/multi-agent.md
    - 趋势追踪: categories/agents/trends.md
  - 生成式模型:'''

if old_agents_pattern in content:
    content = content.replace(old_agents_pattern, agents_new)
    print("Agents replaced OK")

# --- Generative Models ---
gen_new = '''    - 知识库:
      - categories/generative-models/knowledge/index.md
      - 核心方法:
        - GAN 原理: categories/generative-models/knowledge/gan.md
        - VAE 原理: categories/generative-models/knowledge/vae.md
        - 扩散模型详解: categories/generative-models/knowledge/diffusion-models.md
        - Flow Matching: categories/generative-models/knowledge/flow-matching.md
      - 关键技术:
        - 条件生成: categories/generative-models/knowledge/conditional-generation.md
        - 采样加速: categories/generative-models/knowledge/sampling-acceleration.md
    - 趋势追踪: categories/generative-models/trends.md
  - 强化学习:'''

old_gen_pattern = '''    - 知识库:
      - categories/generative-models/knowledge/index.md
      - GAN 原理: categories/generative-models/knowledge/gan.md
      - VAE 原理: categories/generative-models/knowledge/vae.md
      - 扩散模型详解: categories/generative-models/knowledge/diffusion-models.md
      - Flow Matching: categories/generative-models/knowledge/flow-matching.md
      - 条件生成: categories/generative-models/knowledge/conditional-generation.md
      - 采样加速: categories/generative-models/knowledge/sampling-acceleration.md
    - 趋势追踪: categories/generative-models/trends.md
  - 强化学习:'''

if old_gen_pattern in content:
    content = content.replace(old_gen_pattern, gen_new)
    print("Generative replaced OK")

# --- RL ---
rl_new = '''    - 知识库:
      - categories/reinforcement-learning/knowledge/index.md
      - 基础概念:
        - 马尔可夫决策过程 (MDP): categories/reinforcement-learning/knowledge/mdp.md
        - 价值函数: categories/reinforcement-learning/knowledge/value-function.md
      - 核心算法:
        - 策略梯度 (Policy Gradient): categories/reinforcement-learning/knowledge/policy-gradient.md
        - PPO 详解: categories/reinforcement-learning/knowledge/ppo-detailed.md
        - RLHF 原理: categories/reinforcement-learning/knowledge/rlhf-explained.md
    - 趋势追踪: categories/reinforcement-learning/trends.md
  - 高效训练与推理:'''

old_rl_pattern = '''    - 知识库:
      - categories/reinforcement-learning/knowledge/index.md
      - 马尔可夫决策过程: categories/reinforcement-learning/knowledge/mdp.md
      - 价值函数: categories/reinforcement-learning/knowledge/value-function.md
      - 策略梯度: categories/reinforcement-learning/knowledge/policy-gradient.md
      - PPO 详解: categories/reinforcement-learning/knowledge/ppo-detailed.md
      - RLHF 原理: categories/reinforcement-learning/knowledge/rlhf-explained.md
    - 趋势追踪: categories/reinforcement-learning/trends.md
  - 高效训练与推理:'''

if old_rl_pattern in content:
    content = content.replace(old_rl_pattern, rl_new)
    print("RL replaced OK")

# --- Efficient Training ---
eff_new = '''    - 知识库:
      - categories/efficient-training/knowledge/index.md
      - 训练优化:
        - LoRA 低秩适配: categories/efficient-training/knowledge/lora.md
        - 量化技术: categories/efficient-training/knowledge/quantization.md
        - FlashAttention 详解: categories/efficient-training/knowledge/flash-attention-detailed.md
      - 推理优化:
        - KV Cache: categories/efficient-training/knowledge/kv-cache.md
        - 推测性解码: categories/efficient-training/knowledge/speculative-decoding.md
        - PagedAttention: categories/efficient-training/knowledge/paged-attention.md
      - 架构优化:
        - 状态空间模型 (Mamba): categories/efficient-training/knowledge/ssm-mamba.md
    - 趋势追踪: categories/efficient-training/trends.md

extra:'''

old_eff_pattern = '''    - 知识库:
      - categories/efficient-training/knowledge/index.md
      - LoRA 低秩适配: categories/efficient-training/knowledge/lora.md
      - 量化技术: categories/efficient-training/knowledge/quantization.md
      - FlashAttention 详解: categories/efficient-training/knowledge/flash-attention-detailed.md
      - KV Cache: categories/efficient-training/knowledge/kv-cache.md
      - 推测性解码: categories/efficient-training/knowledge/speculative-decoding.md
      - PagedAttention: categories/efficient-training/knowledge/paged-attention.md
      - 状态空间模型 (Mamba): categories/efficient-training/knowledge/ssm-mamba.md
    - 趋势追踪: categories/efficient-training/trends.md

extra:'''

if old_eff_pattern in content:
    content = content.replace(old_eff_pattern, eff_new)
    print("Efficient Training replaced OK")

with open(yml_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll knowledge sections updated!")
