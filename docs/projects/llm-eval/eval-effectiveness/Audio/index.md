## ASR & TTS 效果评估

> 涵盖自动语音识别（ASR）、语音合成（TTS）与文生音频（Text-to-Audio）三大语音/音频核心技术的评估体系。ASR 负责"语音→文本"的理解任务，TTS 负责"文本→语音"的生成任务，文生音频则关注"文本→音效"的生成。三者各有侧重，但评估方法有共通之处（WER/MOS/FAD）。

---

## 一、自动语音识别（ASR）

### 1.1 评估维度与指标

| 维度 | 指标 | 说明 |
|------|------|------|
| **识别准确率** | **WER（Word Error Rate）** | 词错误率 = (S + D + I) / N。S=替换，D=删除，I=插入，N=总词数。**越低越好**，生产级 <5% |
| | **CER（Character Error Rate）** | 字符错误率，中文场景比 WER 更常用。**越低越好** |
| | **Accuracy** | 句子级准确率（整句全对才算对） |
| **鲁棒性** | **噪声鲁棒性** | 不同 SNR 信噪比下的 WER |
| | **远场/混响** | 麦克风距离、混响时间对识别的影响 |
| | **口音/方言** | 不同口音下的 WER 差异 |
| **实时性** | **RTF（Real-Time Factor）** | 处理时间 / 音频时长。RTF < 1 即实时 |
| | **延迟（Latency）** | 首字延迟 + 尾字延迟，影响用户体验 |
| **语言支持** | **多语言 WER** | 不同语言下的识别表现 |
| | **Code-Switching** | 中英混合场景识别 |
| **说话人自适应** | **Speaker Adaptation** | 适应特定说话人后的 WER 提升 |

### 1.2 2025-2026 主流 ASR 模型排行榜

**Open ASR Leaderboard（Hugging Face）** 和 **SpeechColab Leaderboard** 是两大权威榜单：

| 排名 | 模型 | 参数量 | 平均 WER ↓ | 多语言 | 中文 WER ↓ | 特点 |
|------|------|:-----:|:---------:|:-----:|:---------:|------|
| 🥇 | **Qwen3-ASR** | 7B | 4.1% | ✅ 30+ | **3.2%** | 阿里通义，中文 SOTA |
| 🥇 | **Whisper-large-v3-turbo** | 809M | 4.5% | ✅ 99+ | 4.0% | OpenAI，多语言最广 |
| 🥈 | **Paraformer-large** | 680M | 5.2% | ✅ 中/英/日 | 3.8% | 阿里达摩院，工业级 |
| 🥈 | **SenseVoice-Small** | 184M | 5.8% | ✅ 50+ | 4.5% | 商汤，轻量多语言 |
| 🥈 | **Cohere ASR 2** | - | 4.8% | ✅ 20+ | 4.7% | 闭源，企业级 |
| 🥉 | **Granite-ASR** | 0.5B | 6.5% | ❌ 仅英文 | - | IBM，企业私有部署 |
| 🥉 | **wav2vec2-XLSR-1B** | 1B | 7.8% | ✅ 50+ | 6.8% | Meta 开源，自监督 |
| 🥉 | **USM（Google）** | 2B | 5.6% | ✅ 100+ | 5.0% | 谷歌，多语言覆盖广 |

> 数据来源：Open ASR Leaderboard（huggingface.co/spaces/hf-audio/open_asr_leaderboard）及 SpeechColab Leaderboard。平均 WER 取 Common Voice 15.0 + LibriSpeech clean + Fleurs 多语言数据集。

### 1.3 关键 Benchmark 详解

#### Open ASR Leaderboard（HF）
- 涵盖 11 个公开数据集，包括 LibriSpeech、Common Voice、Fleurs、VoxPopuli、GigaSpeech
- 评估 60+ 开源和商业 ASR 系统
- 统一推理 pipeline，保证可复现

#### SpeechColab Leaderboard
- 专注于中文 ASR 评测
- 涵盖 AISHELL、WenetSpeech、HKUST、MagicData 等中文数据集
- 提供基于 WER 的标准化比较

#### 中文 ASR 评测数据集

| 数据集 | 时长 | 领域 | 采样率 | 典型 WER（Whisper-large-v3） |
|--------|:---:|------|:-----:|:---------------------------:|
| **AISHELL-1** | 170h | 朗读语音 | 16kHz | 2.5% |
| **AISHELL-2** | 1000h | 朗读+自由谈 | 16kHz | 3.8% |
| **WenetSpeech** | 10000h | 互联网多场景 | 16kHz | 5.2% |
| **MagicData-RAMC** | 180h | 会议记录 | 16kHz | 4.1% |
| **HKUST** | 200h | 电话普通话 | 8kHz | 7.5% |

### 1.4 选型建议

```
场景                    推荐模型
──────────────────────────────────────────────────
中文高精度               Qwen3-ASR / Paraformer-large
多语言通用               Whisper-large-v3-turbo
端侧/实时                Whisper-turbo / SenseVoice-Small
会议/远场                 Paraformer-large + 麦克风阵列
电话语音（8kHz）          Whisper / SenseVoice
企业私有部署              Granite-ASR / Paraformer
高噪声环境                Whisper / Mega-ASR（2026新）
成本敏感                  SenseVoice-Small / Whisper-small
```

---

## 二、语音合成（TTS）

### 2.1 评估维度与指标

| 维度 | 指标 | 说明 |
|------|------|------|
| **自然度** | **MOS（Mean Opinion Score）** | 人工评分 1-5，SOTA ~4.3-4.5 |
| | **CMOS（Comparative MOS）** | A/B 对比测试 |
| **相似度** | **SMOS（Similarity MOS）** | 声音克隆与原声相似度 |
| **清晰度** | **WER（Word Error Rate）** | ASR 模型回测的错词率，越低越好 |
| **韵律** | **Prosody Score** | 重音、停顿、语调的自然度 |
| **推理速度** | **RTF（Real-Time Factor）** | 生成 1s 语音所需时间。RTF < 1 即实时 |
| **多语言** | **Code-Switching Acc** | 中英混合能力 |
| **情感控制** | **Emotion Acc** | 情感表达准确性 |
| **鲁棒性** | **Robustness** | 对生僻字/标点/数字的发音正确率 |

### 2.2 2025-2026 主流 TTS 模型排行榜

| 排名 | 模型 | MOS ↑ | WER ↓ | RTF ↓ | 特点 |
|------|------|:----:|:-----:|:-----:|------|
| 🥇 | **ViiTorVoice（云上曲率）** 🆕 | ~4.5+ | **0.99%** | 0.06 | 登顶 Seed-TTS 榜首，局部编辑/跨语种克隆，1B 开源 |
| 🥇 | **Seed-TTS（字节）** | **4.52** | **1.8%** | 0.06 | 闭源，自然度最高 |
| 🥇 | **CosyVoice 2（阿里）** | 4.48 | 2.1% | 0.08 | 中文 SOTA，情感/声线控制 |
| 🥈 | **NaturalSpeech 3（微软）** | 4.35 | 2.8% | 0.15 | 因子分解编解码 |
| 🥈 | **FishSpeech 2** | 4.38 | 2.5% | 0.12 | 开源，多语言 |
| 🥉 | **ChatTTS** | 4.15 | 3.8% | 0.35 | 开源，对话场景优化 |
| 🥉 | **MeloTTS** | 3.92 | 4.5% | 0.18 | 轻量开源多语言 |
| 🥉 | **VoiceCraft** | 4.08 | 3.2% | 0.25 | 零样本语音克隆 |

### 2.3 选型建议

```
场景                    推荐模型
──────────────────────────────────────────────────
局部编辑/精修语音        ViiTorVoice（唯一支持）
中文声音克隆             CosyVoice 2 / ViiTorVoice
英文+TTS API            Seed-TTS / NaturalSpeech 3
开源部署                 FishSpeech 2 / ChatTTS
端侧/轻量                MeloTTS
多语言                   FishSpeech 2
对话/交互                ChatTTS / CosyVoice 2
零样本克隆               VoiceCraft / CosyVoice 2
```

---

## 三、文生音频 / 音效生成（Text-to-Audio / SFX）

文生音频（Text-to-Audio）指从文本描述生成非语音类音频内容，包括环境音效（SFX）、音乐片段、场景音等。与 TTS（语音合成）不同，文生音频关注的是**通用音频内容的生成**，而非人的语音。

### 3.1 评估维度

| 维度 | 指标 | 说明 |
|------|------|------|
| **音频质量** | **FAD（Fréchet Audio Distance）** | 生成音频分布与真实音频分布的距离，越低越好 |
| | **MOS（Mean Opinion Score）** | 人工评分 1-5，评估自然度和清晰度 |
| **文本对齐** | **CLAP Score** | 音频-文本在 CLAP（Contrastive Language-Audio Pretraining）空间的相似度 |
| | **Accuracy** | 分类准确率（如生成音效是否匹配提示词描述） |
| **音效匹配** | **Foley Score** | 特定音效类型（脚步声、雨声、机器声等）的生成准确率 |
| | **Event Detection Rate** | 生成音频中是否包含指定的事件声音 |
| **多样性** | **FD（Fréchet Distance）变体** | 评估生成音频的多样性是否接近真实分布 |
| **时序一致性** | **Temporal Alignment** | 长音频中，声音事件的时序排列是否符合文本描述 |

### 3.2 主流模型与数据集

| 模型/系统 | 定位 | 特点 |
|-----------|------|------|
| **AudioLDM 2** | 开源文生音频 | 基于 Latent Diffusion，支持文生音频和文生音乐 |
| **Stable Audio** | 商业+开源 | Stability AI，高质量文生音频 |
| **AudioGen（Meta）** | 开源 | 基于 Transformer 的音效生成 |
| **Make-An-Audio** | 开源 | 扩散模型文生音频 |
| **Tango** | 开源 | 基于 FLAN-T5 + 扩散模型 |
| **FoleyGen** | 研究 | 专注于影视音效（Foley）生成 |
| **Magnificent** | 商业 | 专业级文生音效工具 |

| 评估数据集 | 说明 |
|-----------|------|
| **AudioCaps** | 30K+ 音频-文本对，用于文生音频评估 |
| **Clotho** | 5K+ 音频描述，用于评估文本-音频对齐 |
| **ESC-50** | 50 类环境音效分类，用于 Foley Score 评估 |
| **AudioSet** | Google 大规模音效数据集（527 类） |

---

## 四、ASR + TTS 联合评估（全链路）

实际语音交互系统中，ASR 和 TTS 经常串联使用：

```
用户语音 → [ASR] → 文本 → [NLP/LLM] → 文本 → [TTS] → 语音回复
```

联合评估关键指标：

| 指标 | 说明 |
|------|------|
| **全链路延迟** | ASR 尾字到 TTS 首字的总延迟，目标 < 500ms |
| **级联错误** | ASR 错误 → LLM 理解错误 → TTS 生成错误 |
| **MOS 全链路** | 最终用户听到的语音自然度 |
| **对话完成率** | 端到端语音交互任务成功率 |

---

## 📈 评估结果

> TODO：待补充实际评测数据。

## 📚 参考资料

- Open ASR Leaderboard: huggingface.co/spaces/hf-audio/open_asr_leaderboard
- SpeechColab Leaderboard: github.com/SpeechColab/Leaderboard
- Whisper: OpenAI 大规模弱监督语音识别 (2022)
- Paraformer: 阿里达摩院快速并行语音识别 (2022-2024)
- SenseVoice: 商汤多语言语音识别 (2024)
- Qwen3-ASR: 阿里通义千问语音识别模型 (2026)
- CosyVoice 2: 阿里通义语音合成 (2025)
- Seed-TTS: 字节跳动语音合成 (2024-2025)
- FishSpeech 2: 开源语音合成 (2024-2025)
- NaturalSpeech 3: Zero-Shot Speech Synthesis with Factorized Codec (微软, 2024)
- ChatTTS: 对话式文本到语音模型 (2024-2025)
- Mega-ASR: Towards In-the-wild Speech Recognition (2026, arxiv 2605.19833)
- ViiTorVoice: 云上曲率语音合成模型 (2026)，Seed-TTS 评测榜首
- TTS Arena: ttsarena.ai — 语音合成盲测 Elo 排名
- Common Voice: Mozilla 众包多语言语音数据集
- AISHELL: 北京希尔贝壳中文语音数据集
- WenetSpeech: 出门问问中文多场景语音数据集
