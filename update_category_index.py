import os

base = r'D:\ai_research\docs\categories'

updates = {
    'llm': {
        'name': '大语言模型',
        'knowledge_items': [
            ('Transformer 架构', 'knowledge/transformer-architecture.md'),
            ('自注意力机制', 'knowledge/self-attention.md'),
            ('位置编码', 'knowledge/positional-encoding.md'),
            ('MoE 混合专家', 'knowledge/moe.md'),
            ('Scaling Law', 'knowledge/scaling-law.md'),
            ('涌现能力', 'knowledge/emergent-abilities.md'),
            ('上下文学习', 'knowledge/in-context-learning.md'),
            ('思维链', 'knowledge/chain-of-thought.md'),
            ('RLHF 流水线', 'knowledge/rlhf-pipeline.md'),
            ('DPO 详解', 'knowledge/dpo.md'),
            ('RAG 详解', 'knowledge/rag.md'),
            ('预训练', 'knowledge/pretraining.md'),
            ('监督微调 (SFT)', 'knowledge/sft.md'),
            ('解码策略', 'knowledge/decoding-strategies.md'),
            ('上下文长度扩展', 'knowledge/context-extension.md'),
        ]
    },
    'vision': {
        'name': '计算机视觉',
        'knowledge_items': [
            ('CNN 卷积神经网络', 'knowledge/cnn.md'),
            ('Vision Transformer (ViT)', 'knowledge/vit.md'),
            ('目标检测', 'knowledge/object-detection.md'),
            ('图像分割', 'knowledge/image-segmentation.md'),
            ('扩散模型', 'knowledge/diffusion-models.md'),
            ('3D 重建', 'knowledge/3d-reconstruction.md'),
        ]
    },
    'multimodal': {
        'name': '多模态',
        'knowledge_items': [
            ('对比学习', 'knowledge/contrastive-learning.md'),
            ('跨模态对齐', 'knowledge/cross-modal-alignment.md'),
            ('视觉语言模型', 'knowledge/vision-language-models.md'),
            ('语音识别', 'knowledge/speech-recognition.md'),
        ]
    },
    'agents': {
        'name': 'AI Agent',
        'knowledge_items': [
            ('规划与推理', 'knowledge/planning-reasoning.md'),
            ('工具使用', 'knowledge/tool-use.md'),
            ('记忆机制', 'knowledge/memory-systems.md'),
            ('多 Agent 协作', 'knowledge/multi-agent.md'),
        ]
    },
    'generative-models': {
        'name': '生成式模型',
        'knowledge_items': [
            ('GAN 原理', 'knowledge/gan.md'),
            ('VAE 原理', 'knowledge/vae.md'),
            ('扩散模型详解', 'knowledge/diffusion-models.md'),
            ('Flow Matching', 'knowledge/flow-matching.md'),
            ('条件生成', 'knowledge/conditional-generation.md'),
            ('采样加速', 'knowledge/sampling-acceleration.md'),
        ]
    },
    'reinforcement-learning': {
        'name': '强化学习',
        'knowledge_items': [
            ('马尔可夫决策过程', 'knowledge/mdp.md'),
            ('价值函数', 'knowledge/value-function.md'),
            ('策略梯度', 'knowledge/policy-gradient.md'),
            ('PPO 详解', 'knowledge/ppo-detailed.md'),
            ('RLHF 原理', 'knowledge/rlhf-explained.md'),
        ]
    },
    'efficient-training': {
        'name': '高效训练与推理',
        'knowledge_items': [
            ('LoRA 低秩适配', 'knowledge/lora.md'),
            ('量化技术', 'knowledge/quantization.md'),
            ('FlashAttention 详解', 'knowledge/flash-attention-detailed.md'),
            ('KV Cache', 'knowledge/kv-cache.md'),
            ('推测性解码', 'knowledge/speculative-decoding.md'),
            ('PagedAttention', 'knowledge/paged-attention.md'),
            ('状态空间模型 (Mamba)', 'knowledge/ssm-mamba.md'),
        ]
    },
}

for cat, info in updates.items():
    path = os.path.join(base, cat, 'index.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove old placeholder if exists
    content = content.replace('## 里程碑论文\n\n（待录入）\n\n', '')

    # Add knowledge section before trends
    items = info['knowledge_items']
    knowledge_text = '\n## 知识库\n\n系统化的算法知识点整理：\n\n'
    for name, link in items:
        knowledge_text += f'- [{name}]({link})\n'
    knowledge_text += f'\n共 **{len(items)}** 个知识点\n\n'

    if '## 知识库' not in content:
        if '## 前沿趋势' in content:
            content = content.replace('## 前沿趋势', knowledge_text + '## 前沿趋势')
        else:
            content += '\n' + knowledge_text

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Updated: {cat}/index.md')

print('\nAll category index files updated!')
