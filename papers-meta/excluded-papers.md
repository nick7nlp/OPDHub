# OPD Excluded Papers Log

记录被精读后排除的论文及原因。Pipeline 不再考虑这些论文。

## 2026-05-19 Cleanup (V3 deep-read pipeline 第一次系统性清理)

### 老论文 (4 篇 — 超出 daily window)
日期窗口纪律：daily scout 只接当天 + 前一天提交的论文，历史漏论文不进 daily pipeline。

| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2502.02671 | On Teacher Hacking in Language Model Distillation (DeepMind, ICML 2026) | Outside date window (2025-02). V3 verdict: is_opd=analysis (§7.2 失败模式分析), 但属于历史 backfill, 不进 daily |
| 2505.18952 | Online Knowledge Distillation with Reward Guidance | Outside date window (2025-05). V3 verdict: is_opd=yes (§4.3) |
| 2510.02227 | More Than One Teacher: Adaptive Multi-Guidance Policy Optimization | Outside date window (2025-10). V3 verdict: is_opd=yes (§5.3.1) |
| 2602.12262 | T3D: Few-Step Diffusion Language Models via Trajectory Self-Distillation (NeurIPS 2025) | Outside date window (2026-02), 且 V3 verdict: is_opd=no, not-applicable — trajectory 预先一次性生成, 不是 in-loop rollout |

### Not-OPD (1 篇)
| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2605.15417 | f-Trajectory Balance: A Loss Family for Tuning GFlowNets, Generative Models, and LLMs (ICML 2026) | V3 verdict: is_opd=no — 提出 f-divergence loss family for RL fine-tuning, 没有 teacher-student 架构, 不是蒸馏方法 |

### 灰色 (2 篇 — 非 OPD 主线方法)
| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2604.20244 | Hybrid Policy Distillation for LLMs | V3 verdict 判 yes (§4.1), 但只有 single-token sampling 不是 full rollout, 主线非 OPD |
| 2604.18963 | Distillation Traps and Guards: A Calibration Knob for LLM Distillability | V3 verdict 判 yes (§5.1), 但论文核心是 teacher-side calibration, 用 GKD trainer 跑实验, 是 OPD 工具不是 OPD 方法贡献 |

### 本质是 RL (2 篇 — 标榜 distillation 但本质是 RL)
| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2605.15726 | Nudging Beyond the Comfort Zone: Efficient Strategy-Guided Exploration for **RLVR** | 标题就是 "for RLVR"; verifier reward 是主信号, distillation term 只是辅助 loss; 删掉 distillation term 主要贡献还在, 删掉 RL 部分论文垮掉 → RL 是体, distill 是辅 |
| 2604.02621 | **Reinforcement Learning-based** Knowledge Distillation with LLM-as-a-Judge | 标题就是 "RL-based KD", 用 PPO/GRPO 训练, judge 当 reward signal — 本质是 RLAIF (RL with AI Feedback), 把 teacher 当 reward, 不是 teacher logit distillation |

### Analysis-only (1 篇 — 不收 awesome, 综述理论章可 cite)
| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2605.22731 | Post-Training is About States, Not Tokens: A State Distribution View of SFT, RL, and On-Policy Distillation (Dong Nie, 2026-05-21) | Analysis-only — 不提新方法, 提供 state-distribution 视角统一 SFT/RL/OPD, Qwen3-0.6B 小规模 GSM8K 实验. 按"awesome 只收方法论文"铁律不进 awesome list. 综述 Theory/Perspective 章节可作为参考引用 |

## Pipeline 改进
- daily scout DATE WINDOW: 只接当天 + 前一天的 arXiv 提交 (今天 yymm 或上月最末尾)
- V3 deep-read 是收录的强制 gate, abstract-only 判断不可信
- RL vs OPD 边界: 看核心目标是不是 distillation, RL 是不是体

| 2605.17743 | MoASE++: Mixture of Activation Sparsity Experts with Domain-Adaptive On-policy Distillation for Continual Test Time Adaptation | scope-out | 2026-05-20 | Vision classification/segmentation (ViT/Segformer); output is image labels not text. OPD收录只收输出文本的模型 |
| 2026-05-20 | 2605.19436 | CEPO: RLVR Self-Distillation using Contrastive Evidence Policy Optimization | RL paper with distillation as auxiliary loss: the core contribution is a better credit assignment mechanism for RLVR (mo |
| 2026-05-23 | 2605.21699 | X-Token: Projection-Guided Cross-Tokenizer Knowledge Distillation | This is off-policy KD on fixed training data without student rollouts; the contribution is a cross-tokenizer alignment m |
| 2026-05-23 | 2605.20201 | Long-Context Reasoning Through Proxy-Based Chain-of-Thought Tuning | The core contribution is a training framework for long-context reasoning using proxy contexts. The distillation (SFT on  |
| 2026-05-23 | 2605.21984 | Echo: Learning from Experience Data via User-Driven Refinement | This is an SFT-based framework that trains on offline user-refined data mined from production logs; there is no on-polic |
| 2026-05-23 | 2605.20654 | REFLECTOR: Internalizing Step-wise Reflection against Indirect Jailbreaks | The core contribution is an RL-based safety alignment framework with dual rewards; the teacher-guided SFT is an offline  |
| 2026-05-23 | 2605.20256 | FBOS-RL: Feedback-Driven Bi-Objective Synergistic Reinforcement Learning | RL paper with GRPO as core contribution; no distillation term exists—the method improves RL exploration via feedback-aug |
| 2026-05-26 | 2605.25582 | Extreme Region Policy Distillation | The core contribution is an RL optimization framework that decouples sample efficiency from KL efficiency; distillation  |

## 2026-05-28 三条件过滤 REJECT

| arxiv | title | reason |
|---|---|---|
| 2605.16941 | Roll Out and Roll Back: Diffusion LLMs are Their Own Efficiency Teachers | R1: rollout once-before-training → off-policy SFT，不在 training loop 内 rollout |
| 2605.19776 | Preferences Order, Ratings Anchor: From Fused Expert Aesthetic Ground Truth to Self-Distillation | R3: RL-only (confidence-weighted GRPO) + 无 teacher-distill term，D_KL(π_θ ∥ π_ref) 是 ref-policy 正则化不是 teacher distill |
| 2605.19447 | SERL: Selective Hindsight Distillation for Multi-Turn Agents | R3+R1: RL agent framework (GRPO + env feedback reweighting)，无 teacher model，action-token KL 是 π vs π_ref 正则化不是 teacher distill |
| 2605.22675 | Self-Policy Distillation via Capability-Selective Subspace Projection (SPD) | NO: NTP loss on KV-projected self-outputs, no teacher, no KL/divergence loss, paper itself marks "On-Policy Self-Distillation = ×" in comparison table. Three conditions all fail. |

## 2026-05-28 Full Corpus Audit — 明确误判 (post-V3 deep-read 修正)

V3 deep-read 判 `is_opd: yes` 但全库审计反向核对论文标题/方法实质后发现不属 OPD 主线。第一篇 (IRIS) 在 README 5/28 审计表已记录处置，此处补 ThinkTuning。

| arxiv | title | original V3 verdict | reject reason | 处置 |
|---|---|---|---|---|
| 2508.07616 | ThinkTuning: Instilling Cognitive Reflections without Distillation (RRV et al., EMNLP 2025) | is_opd=yes, primary §5.2, secondary §5.3.1; teacher_signal=logits | 论文标题自带 "without Distillation"。Teacher 同尺寸模型仅在 γ 比例 rollout 末尾追加文本结构化反馈（opinions/reasons/phrases），不提供 logit distribution。Loss 是 GRPO+Advantage-Aware Shaping on augmented data，不是 KL-to-teacher。属 teacher-augmented RL，不是 OPD distillation。V3 精读 `teacher_signal=logits` 字段为误标——原文 "implicit supervision through feedback" 明确说是文本反馈。| 2026-05-28 全库审计移除：latex-v4/main.tex (5 处 cite + bib entry)、paper_notes.json (DB 183→182)、INDEX.md (row 26)、Awesome List (-1, 176→175 badge)、PDF→`pdfs/.trash-2026-05-28-thinktuning/` |

## 2026-05-29 输出模态边界 REJECT (老大决策)

V3 deep-read 内层 `is_opd=yes` 但外层字段未填，5/29 backlog 核对发现 2 篇输出模态超出 5/15 收录范围（"输出是文本/语言的模型"）。

| arxiv | title | output | reject reason | 处置 |
|---|---|---|---|---|
| 2605.13724 | AnyFlow: Any-Step Video Diffusion Model with On-Policy Flow Map Distillation | 视频帧 | Wan2.1-14B 视频扩散蒸馏（VBench 84.41），FMBS+DMD 是图像/视频生成 pipeline，不是 LLM。Per 5/15 收录范围明确不收：T2I/Video Diffusion 即使内部用 LLM 做 text encoder 也不收。 | paper_notes.json `is_opd=no` + `rejected_reason`；不进 backlog；不进 awesome list |
| 2605.27095 | Adversarial Dual On-Policy Distillation from Expressive Flow-based Teacher | 连续动作 (embodied control) | 教师是 flow-matching policy（不是 LLM backbone），学生是 control policy，输出是连续机器人动作。VLA/Robot+LLM 的收录条件是"底层有 LLM backbone"，本文不满足。论文 reasoning 字段自标 "may be non-text (robot control)" + `_note` 自标 "⚠️ 可能是 embodied control，需确认收录边界"。 | paper_notes.json `is_opd=no` + `rejected_reason`；不进 backlog；不进 awesome list |
