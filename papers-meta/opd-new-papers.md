# OPD New Papers Tracking

**Last Updated**: 2026-05-29 15:30 CST
**Purpose**: 追踪未进综述的新 OPD 论文,scout 每天自动追加

## 收录范围规则 (2026-05-15 确认)

**收录**: 输出是**文本/语言**的模型的 on-policy distillation
- ✅ 自回归 LLM (GPT/Llama/Qwen 等)
- ✅ VLM / AudioLLM / 多模态 LLM (backbone 是 LLM)
- ✅ VLA / Robot+LLM (底层有 LLM backbone)
- ✅ Diffusion Language Model (输出是文本, 如 MDLM/TABOM)
- ✅ Protein Language Model (domain-specific LLM)
- ✅ GUI Agent (LLM-based)

**不收录**: 输出是**图片/视频**的模型
- ❌ T2I Diffusion (Stable Diffusion, FLUX 等)
- ❌ T2I Flow Matching (SD 3.5 等)
- ❌ Video Diffusion / Video Generation
- ❌ 任何纯图像/视频生成管线（即使用 T5/LLM 做 text encoder）

**判定原则**: 看模型最终输出的模态, 不看内部组件。

## 当前待集成 (待精读 queue — 接 scout 新论文)

**纪律**: 此表只接 daily scout 当周提交、尚未做 V3 精读的论文。Deep-read 一旦完成就移到下方 V3 待集成 backlog。

| # | arXiv ID | Published | Title | 发现日期 | Scout 备注 |
|---|----------|-----------|-------|----------|-----------|
| _空_ | — | — | — | — | — |

> 2026-05-23 23:10 CST 老大复核：SPD (2605.22675) 移到 reject 区 — self-play 性质 (rollout once-before-training)，非真正 OPD。详见下方"2026-05-23 清理"段。

## V4 待集成 backlog (已 V3 精读 + 3-condition 复核, 24 篇)

**说明**: 这些论文已通过 V3 精读 + academic-rigor skill 3-condition (teacher / distill_loss / rollouts→KL→update) 复核, 待下次 latex 综述 (v4) 更新时按 §Section 集成。**§Section 列是 v4 章节结构 best guess**，集成时按论文实际方法确认。

**纪律 (2026-05-23 加)**: V3 精读 is_opd=yes **不等于**最终判定。必须再过 3-condition 复核, 尤其检查 `rollout_frequency` 字段——`once-before-training` / `batch-precomputed` 这类 = off-policy SFT 或 self-play, 不属 OPD 主线。

**5/29 同步说明**: 5/22-5/28 之间 daily-pipeline 共 deep-read 26 篇 is_opd=yes 论文，其中 2 篇被 5/29 老大决策 reject（边界模态，详见下方 reject 段），剩 24 篇全部纳入此表。

| # | arXiv ID | Published | Title | Type | §v4-Section | 发现日期 | V3 精读 |
|---|----------|-----------|-------|------|-------------|----------|---------|
| 1 | 2605.11019 | 2026-05-10 | Efficient LLM Reasoning via Variational Posterior Guidance with Efficiency Awareness | 🚧 Self-Distill | §5.3.2 | 5/16 | ✅ is_opd=yes, per-step rollout |
| 2 | 2605.15239 | 2026-05-15 | Reducing the Safety Tax in LLM Safety Alignment with On-Policy Self-Distillation | 🚧 Self-Distill (Safety) | §8.1 | 5/19 | ✅ is_opd=yes, per-step rollout |
| 3 | 2605.15532 | 2026-05-15 | DeltaPrompts: Escaping the Zero-Delta Trap in Multimodal Distillation | 🚧 VLM Pipeline | §6.2 | 5/19 | ✅ is_opd=yes, per-step rollout, external teacher |
| 4 | 2605.17497 | 2026-05-19 | Self-Supervised On-Policy Distillation for Reasoning Language Models (SSOPD) | 🚧 Self-Distill | §5.3.2 | 5/20 | ✅ is_opd=yes, per-step rollout |
| 5 | 2605.18299 | 2026-05-19 | SD-Search: On-Policy Hindsight Self-Distillation for Search-Augmented Reasoning | 🚧 Self-Distill (Agent) | §5.3.3 | 5/20 | ✅ is_opd=yes, per-step rollout |
| 6 | 2605.17873 | 2026-05-19 | HINT-SD: Targeted Hindsight Self-Distillation for Long-Horizon Agents | 🚧 Self-Distill (Agent) | §5.3.3 | 5/20 | ✅ is_opd=yes, per-outer-iter rollout |
| 7 | 2605.18740 | 2026-05-19 | Vision-OPD: Learning to See Fine Details for Multimodal LLMs via On-Policy Self-Distillation | 🚧 VLM Self-Distill | §5.3.2 | 5/20 | ✅ is_opd=yes, per-step rollout |
| 8 | 2605.17862 | 2026-05-19 | f-OPD: Stabilizing Long-Horizon On-Policy Distillation with Freshness-Aware Control | 🚧 OPD Infra | §6.3 | 5/20 | ✅ is_opd=yes, per-outer-iter rollout, external teacher |
| 9 | 2605.19433 | 2026-05-19 | Backtracking When It Strays: Mitigating Dual Exposure Biases in LLM Reasoning Distillation | 🚧 Curriculum | §6.2 | 5/20 | ✅ is_opd=yes, per-step rollout, external teacher |
| 10 | 2605.20258 | 2026-05-20 | It Takes Two: Complementary Self-Distillation for Contextual Integrity | 🚧 Self-Distill (Privacy) | §5.3.2 / §8 | 5/28 | ✅ is_opd=yes |
| 11 | 2605.20643 | 2026-05-20 | AVSD: Adaptive-View Self-Distillation by Balancing Consensus and Teacher | 🚧 Self-Distill (Multi-view) | §5.3.2 | 5/28 | ✅ is_opd=yes |
| 12 | 2605.21606 | 2026-05-21 | When Are Teacher Tokens Reliable? Position-Weighted On-Policy Self-Distillation | 🚧 Token Weighting | §6.1 | 5/28 | ✅ is_opd=yes |
| 13 | 2605.21834 | 2026-05-21 | On-Policy Consistency Training Improves LLM Safety (OPCT) | 🚧 Self-Distill (Safety) | §8.1 / §5.3.3 | 5/28 | ✅ is_opd=yes, per-step rollout, frozen-copy teacher |
| 14 | 2605.21851 | 2026-05-21 | OPPO: Bayesian Value Recursion for Token-Level Credit Assignment in LLM | 🚧 Token Credit | §6.1 | 5/28 | ✅ is_opd=yes |
| 15 | 2605.21924 | 2026-05-21 | Visual-Advantage On-Policy Distillation for Vision-Language Models | 🚧 VLM Token Reweight | §6.1 | 5/28 | ✅ is_opd=yes |
| 16 | 2605.22240 | 2026-05-22 | Unlocking Proactivity in Task-Oriented Dialogue | 🚧 Self-Distill (PI, TOD) | §5.3.1 | 5/28 | ✅ is_opd=yes, asymmetric self-distill from privileged user concerns |
| 17 | 2605.22263 | 2026-05-22 | Tailoring Teaching to Aptitude: Direction-Adaptive Self-Distillation | 🚧 Adaptive Token Weight | §6.1 / §4.3 | 5/28 | ✅ is_opd=yes, entropy-routed direction-adaptive |
| 18 | 2605.22511 | 2026-05-22 | Search-E1: Self-Distillation Drives Self Evolution in Search | 🚧 Self-Distill + RL | §5.3.2 / §8 | 5/28 | ✅ is_opd=yes, GRPO + offline self-distill alternation |
| 19 | 2605.26844 | 2026-05-26 | Not All Disagreement Is Learnable: Token Teachability in On-Policy Distillation | 🚧 Token Selection | §6.1 | 5/28 | ✅ is_opd=yes, token teachability metric |
| 20 | 2605.27028 | 2026-05-27 | Less is More: Early Stopping Rollout for On-Policy Distillation | 🚧 OPD Efficiency | §6.3 | 5/28 | ✅ is_opd=yes, off-policy teacher decay |
| 21 | 2605.27115 | 2026-05-27 | Counteraction-Aware Multi-Teacher On-Policy Distillation | 🚧 Multi-Teacher | §5.1 | 5/28 | ✅ is_opd=yes, MOPD counteraction-aware |
| 22 | 2605.27186 | 2026-05-27 | MAIGO: Mitigating Lost-in-Conversation with History-Cleaned On-Policy Self-Distillation | 🚧 Self-Distill (Multi-turn) | §5.3.2 / §8 | 5/28 | ✅ is_opd=yes, multi-turn lost-in-conversation |
| 23 | 2605.27255 | 2026-05-27 | Pair-In, Pair-Out: Latent Multi-Token Prediction for Efficient LLMs | 🚧 OPD + MTP Efficiency | §6.3 | 5/28 | ✅ is_opd=yes, OPD teacher as confidence head supervisor |
| 24 | 2605.28014 | 2026-05-28 | ROSD: Reflective On-Policy Self-Distillation for Language Models | 🚧 Self-Distill (Reflective) | §5.3.2 | 5/28 | ✅ is_opd=yes, error-focused self-reflection + quote-localized distill |

**Notes (5/22 之前 9 篇):**
- 2605.11019 (VPG-EA): 双流 self-distill — posterior 是同模型加 reference answer condition, advantage-gated forward KL 是核心 distillation 目标。本质是 OPD 不是 RL。
- 2605.15239 (OPSA): 标题就是 "On-Policy Self-Distillation", per-token KL 教学是核心, 安全对齐应用。典型 OPD。
- 2605.15532 (DeltaPrompts, NVIDIA): 论文核心是为 OPD 选好 prompt, "Run OPD with reverse KL" 写在论文里。NeurIPS 2025。
- 2605.18740 (Vision-OPD): VLM regional-to-global self-distillation, crop-conditioned teacher → full-image student, on-policy rollouts + JSD loss。
- 2605.17862 (f-OPD): 解决 async OPD 的 staleness 问题, sample-level freshness scoring + adaptive buffer refresh。
- 2605.18141 (A Brief Overview): Survey/overview paper, 作为 background reference 保留, 不入 Awesome List。
- 2605.19433 (MOTAB): 监控 student on-policy trajectories via adaptive entropy boundary; 发现偏离后 backtrack 到 safe state 让 teacher 纠正。Qwen3-32B→4B。
- 2605.17743 (MoASE++): ❌ 排除 — 视觉分类/分割模型 (ViT/Segformer), 输出不是文本, 不符合收录边界。

**Notes (5/22-5/28 新增 15 篇):**
- 2605.20258 / 2605.27186: 多轮对话 OPD 应用（context integrity / lost-in-conversation）
- 2605.21606 / 2605.26844 / 2605.21851 / 2605.22263: §6.1 Token Weighting 谱系扩展（teacher reliability / token teachability / Bayesian credit / direction-adaptive）
- 2605.21834 (OPCT): 5/27 commit 提到的 "+OPD"，paper_notes 已确认 is_opd=yes，per-step + frozen-copy teacher
- 2605.21924: VLM token-level visual advantage reweighting
- 2605.22240: TOD 任务的 asymmetric self-distill from privileged user concerns
- 2605.22511 (Search-E1): GRPO + offline self-distill alternation
- 2605.27028: 发现 "Off-policy Teacher Decay" 现象，提出 early stopping
- 2605.27115: Counteraction-aware multi-teacher OPD (MOPD)
- 2605.27255: Latent MTP + OPD 蒸馏的混合架构
- 2605.28014 (ROSD): Reflective self-distillation, error-focused

**已 cite 我们综述 (arXiv 2604.00626) 的 backlog 论文 (确认 2/24 = 8.3%)**:
- 2605.17862 f-OPD: ref [15]
- 2605.19433 MOTAB: ref [35]

## 2026-05-29 输出模态边界 REJECT (老大决策)

5/27-5/28 daily-pipeline deep-read 内层 `is_opd=yes` 但外层字段 None 的 3 篇中，2 篇按 5/15 收录范围 reject：

- **2605.13724 AnyFlow** (Wan2.1-14B 视频扩散 + VBench): 输出是视频帧，非文本。**5/15 规则明确不收录 Video Diffusion**。详见 `excluded-papers.md`。
- **2605.27095 Adversarial Dual OPD from Expressive Flow-based Teacher**: Embodied control，教师是 flow-matching policy（不是 LLM backbone），输出连续机器人动作。不满足 VLA/Robot+LLM 的 "底层有 LLM backbone" 条件。详见 `excluded-papers.md`。

第 3 篇 `2605.28014 ROSD` 经核验是文本 LLM self-distill，已纳入 backlog。

**SERL (2605.19447) 状态澄清**: 5/27 commit `ad8775d` message 写 "+2 OPD: OPCT, SERL"，但 `paper_notes.json` 实际只保存了 OPCT（SERL 笔记从未落盘）。5/28 三条件过滤复核认定 SERL 是 RL-only（GRPO + env feedback reweighting，无 teacher distill），已加入 `excluded-papers.md`。5/29 在 `paper_notes.json` 补 SERL 的 is_opd=no stub，引用 reject reason，让 paper_notes 成为 single source of truth。

## 2026-05-23 清理 (academic-rigor 3-condition 复核)

老大 5/23 22:55 CST 反问 "你确定这 14 篇都是 OPD 方法吗?" 触发复核。按 academic-rigor skill (§OPD 专用判定标准) 的三条件检查 + `paper_notes.json` V3 精读 `on_policy_mechanism.rollout_frequency` 字段, 以下 5 篇从 V3 backlog / 待精读 queue 移除:

### Self-play / off-policy SFT 非 OPD 主线 (3 篇)

- **2605.22675 SPD** (Self-Policy Distillation via Capability-Selective Subspace Projection)
  - V3 精读 `rollout_frequency: once-before-training`, `signal_source: pure self`, `teacher_signal: none`
  - 模型一次性预生成训练数据 + KV-subspace projection hook, **不在 training loop 内重新 rollout** → self-play 谱系, 不是 OPD
  - 老大原话 "self play 的方法"

- **2605.16865 MixSD** (Mixed Contextual Self-Distillation for Knowledge Injection)
  - V3 精读 `is_opd: no`, evidence quote: "generating mixed rollouts incurs a **one-time preprocessing cost** over standard SFT"
  - 论文自己把 OPSD 当对照 baseline → off-policy self-distillation, 不是 OPD

- **2605.16941 WINO+** (Roll Out and Roll Back: Diffusion LLMs are Their Own Efficiency Teachers)
  - V3 精读 `rollout_frequency: once-before-training`, evidence quote: "first run WINO **offline** and record"
  - 预生成 trajectory 的 SFT, 不是训练循环内 OPD

### Analysis-only 非方法论文 (1 篇)

- **2605.16826 Decoupling KL and Trajectories** (A Unified Perspective for SFT, DAgger, Offline RL, and OPD)
  - V3 精读 `is_opd: analysis`, 论文核心是理论框架统一 4 个 distillation 目标
  - 按 academic-rigor "Analysis-only 论文不进 awesome list" 铁律: 不进 backlog, 综述 §4.1 Theory 章可作 background cite

### 边界 / RL 而非 distill (1 篇)

- **2605.19776 PSDISTILL** (VLM self-distillation for aesthetic scoring)
  - 5/20 入库时已标 ⚠️ 边界, evidence: Elo reference pool + confidence-weighted GRPO
  - 本质 GRPO + self-reward (verifier-style), 缺 distill loss → 不属 OPD

### 根因 (2026-05-23)

- daily-pipeline cron 的 LLM 分类**只看 abstract 关键词不看 `rollout_frequency`**, 把 self-play / offline-SFT 都贴 `is_opd=yes`
- 我 5/22 手动加 SPD 时也犯同样错 (看 "self-distill" 关键词就放行)
- **修复**: opd-pipeline.md cron prompt 加 3-condition 强制验证步骤 + SOUL 加 "OPD 判定前必载 academic-rigor skill" 硬纪律

## 授权：2026-05-19 清理

5/19 老大亲身审查后, 以下 9 篇被清理 (PDF 进 trash, paper_notes 删除, Awesome List 撤下, known_arxiv_ids 加黑名单):

### 老论文 (4 篇) — 超出 daily window
- 2502.02671 On Teacher Hacking (DeepMind, ICML 2026)
- 2505.18952 Online KD with Reward Guidance
- 2510.02227 AMPO
- 2602.12262 T3D (NeurIPS 2025) — V3 verdict: not-applicable, trajectory 预生成

### Not-OPD (1 篇)
- 2605.15417 f-Trajectory Balance — V3 verdict: is_opd=no, RL loss family 没有 teacher-student

### 灰色 (2 篇) — 不是 OPD 主线方法
- 2604.20244 HPD — 只有 single-token sampling
- 2604.18963 Distillation Traps and Guards — teacher-side calibration, 不是 OPD 贡献

### 本质是 RL (2 篇) — 标榜 distillation 但本质是 RL
- 2605.15726 NudgeRL — 标题就是 "for RLVR", verifier reward 主信号, distill 只是辅助
- 2604.02621 RL-KD-Judge — 标题就是 "RL-based KD", PPO/GRPO 训练, judge 当 reward (RLAIF 本质)

详见: `papers-meta/excluded-papers.md`

## 待确认 (1 篇)

| arXiv ID | Title | 问题 | 日期 |
|----------|-------|------|------|
| 2604.23336 | Efficient Rationale-based Retrieval: On-policy Distillation from Generative Rerankers based on JEPA | LLM backbone 做 on-policy distillation 但最终输出是 embedding/retrieval score, 不是文本生成。边界模糊。 | 5/16 |

## 已集成到 V3 (归档 - 5/12 至 5/16 batch, 共 10 篇)

| # | arXiv ID | Published | Title | §Section | 集成日期 |
|---|----------|-----------|-------|----------|----------|
| 1 | 2605.15113 | 5/14 | Learning from Language Feedback via Variational Policy Distillation | §5.3.3 | 5/16 |
| 2 | 2605.15155 | 5/14 | Self-Distilled Agentic Reinforcement Learning (SDAR) | §4.3+§8.2 | 5/15 |
| 3 | 2605.13643 | 5/13 | Prefix Teach, Suffix Fade: Local Teachability Collapse | §7.2 | 5/15 |
| 4 | 2605.13501 | 5/13 | RWOPD | §8.2+§4.3 | 5/15 |
| 5 | 2605.13255 | 5/13 | EGRSD | §6 | 5/15 |
| 6 | 2605.13230 | 5/13 | TGPO | §4.3 | 5/15 |
| 7 | 2605.12913 | 5/13 | Revisiting DAgger in the Era of LLM-Agents | §8.2 | 5/15 |
| 8 | 2605.12652 | 5/12 | MOPD | §6 | 5/15 |
| 9 | 2605.11853 | 5/12 | GEAR | §6 | 5/15 |
| 10 | 2605.12741 | 5/12 | RESD | §5.3.1+§6 | 5/15 |

## 已排除 (不在收录范围)

| arXiv ID | Title | 排除原因 | 日期 |
|----------|-------|---------|------|
| 2605.15055 | DiffusionOPD: A Unified Perspective of On-Policy Distillation in Diffusion Models | T2I Diffusion, 输出是图片 | 2026-05-15 |
| 2605.14897 | Critic-Driven Voronoi-Quantization for Distilling Deep RL Policies to Explainable Models | Deep RL 控制策略蒸馏, 非语言模型 | 2026-05-15 |
| 2605.14443 | Prompting Policies for Multi-step Reasoning and Tool-Use in Black-box LLMs with Iterative Distillation of Experience | 不是蒸馏 LLM, 而是优化 prompt selector; LLM 本身 frozen | 2026-05-15 |
| 2605.14071 | Distribution Corrected Offline Data Distillation for Large Language Models | 明确 offline, 无 on-policy sampling ("without online rollouts") | 2026-05-15 |
| 2605.13724 | AnyFlow: Any-Step Video Diffusion Model | 视频扩散模型, 输出是视频 | 2026-05-15 |
| 2605.08063 | Flow-OPD: On-Policy Distillation for Flow Matching Models | T2I Flow Matching (SD 3.5), 输出是图片 | 2026-05-15 |
| 2605.05204 | D-OPSD: On-Policy Self-Distillation for Step-Distilled Diffusion Models | T2I Diffusion, 输出是图片 | 2026-05-15 |
| 2605.15190 | RAVEN: Real-time Autoregressive Video Extrapolation with Consistency-model GRPO | Video diffusion, 输出是视频 | 2026-05-16 |
| 2605.15108 | Logging Policy Design for Off-Policy Evaluation | OPE for recommender, 非语言模型蒸馏 | 2026-05-16 |
| 2605.15012 | Boosting Reinforcement Learning with Verifiable Rewards via Randomly Selected Few-Shot Guidance | 纯 RL (RLVR+SFT), 无 distillation | 2026-05-16 |
| 2605.14450 | Stop Overthinking: Unlocking Efficient Listwise Reranking with Minimal Reasoning | IR reranking, 无蒸馏 | 2026-05-16 |
| 2605.12034 | Boosting Omni-Modal Language Models: Staged Post-Training with Visually Debiased Evaluation | Evaluation methodology, 无 OPD | 2026-05-16 |
| 2605.11706 | GRAFT: Graph-Tokenized LLMs for Tool Planning | Tool planning, 无蒸馏 | 2026-05-16 |
| 2605.19436 | CEPO: RLVR Self-Distillation using Contrastive Evidence Policy Optimization | 纯 RLVR credit assignment, 无 teacher-student distillation | 2026-05-20 |

## 已集成到 V3 (归档 - 5/9 至 5/12 batch, 共 17 篇)

> 以下论文已在 V3 references.bib 中,不再需要操作。

| arXiv ID | Title | §Section |
|----------|-------|----------|
| 2605.08737 | The Extrapolation Cliff in OPD of Near-Deterministic Structured Outputs | §7.2+§8.2 |
| 2605.08741 | Training with Harnesses: On-Policy Harness Self-Distillation ⭐引用我们 | §5.3.1+§8.2 |
| 2605.08776 | Reasoning Compression with Mixed-Policy Distillation | §5.1 |
| 2605.08873 | CoDistill-GRPO | §4.3 |
| 2605.09253 | Rock Tokens in On-Policy Distillation | §7.2 |
| 2605.09548 | Crosslingual On-Policy Self-Distillation | §5.3.1+§8.2 |
| 2605.09725 | OPD with Best-of-N Teacher Rollout Selection | §5.1 |
| 2605.10889 | Unmasking OPD: Where It Helps, Where It Hurts (Apple) | §7.1+§7.2 |
| 2605.11182 | The Many Faces of OPD: Pitfalls, Mechanisms, Fixes (UIUC) | §7.2 |
| 2605.11458 | Adaptive Teacher Exposure for Self-Distillation (ByteDance) | §5.3.1 |
| 2605.11609 | Anti-Self-Distillation via PMI | §4.1+§5.3.1 |
| 2605.11613 | From Generic Correlation to Input-Specific Credit in OPSD | §4.2+§5.3.1 |
| 2605.11739 | Learning to Foresee: Unlocking Efficiency of OPD ⭐引用我们 | §6+§7.1 |
| 2605.11854 | Self-Distilled Trajectory-Aware Boltzmann Modeling (TABOM) | §5.3.2+§8.2 |
| 2605.12227 | Combining On-Policy Optimization and Distillation for Long-Context | §4.3 |
| 2605.12400 | OGLS-SD: Outcome-Guided Logit Steering | §4.2+§5.3.1 |
| 2605.12483 | Beyond GRPO and OPD: Sparse-to-Dense Reward ⭐引用我们 | §4.3 |

## 资料位置
- **PDF**: `/apdcephfs_cq8/share_1324356/nickmysong/openclaw_fsp/papers/opd/{id}.pdf`
- **BibTeX**: `/apdcephfs_cq8/share_1324356/nickmysong/openclaw_fsp/papers/opd/new_opd_2605_bibtex.bib`
- **GitHub**: 已在 taxonomy sections 标 🟡

## 引用我们综述 (2604.00626) 的论文 - 17 篇确认（截至 2026-05-15）

| # | arXiv ID | Title | Date | Status |
|---|----------|-------|------|--------|
| 1 | 2604.25110 | Knowledge Distillation Must Account for What It Loses | 4月 | 已在 V2 |
| 2 | 2605.00642 | Learn where to Click from Yourself: On-Policy Self-Distillation for GUI Grounding | 5/1 | 已在 V2 |
| 3 | 2605.01347 | MAD-OPD: Breaking the Ceiling in On-Policy Distillation via Multi-Agent Debate | 5/2 | 已在 V2 |
| 4 | 2605.02943 | Healthcare AI GYM for Medical Agents | 5/5 | 已在 V2 |
| 5 | 2605.03677 | Uni-OPD: Unifying On-Policy Distillation with a Dual-Perspective Recipe | 5/5 | 已在 V2 |
| 6 | 2605.05040 | Preference-Based Self-Distillation: Beyond KL Matching via Reward Regularization | 5/7 | 已在 V2 |
| 7 | 2605.06230 | Safactory: A Scalable Agentic Infrastructure for Training Trustworthy Autonomous Intelligence | 5/7 | ✅ 已集成 |
| 8 | 2605.06597 | UniSD: Towards a Unified Self-Distillation Framework | 5/7 | 已在 V2 |
| 9 | 2605.07396 | Rubric-based On-policy Distillation | 5/8 | 已在 V2 |
| 10 | 2605.07711 | SimCT: Recovering Lost Supervision for Cross-Tokenizer On-Policy Distillation | 5/8 | 已在 V2 |
| 11 | 2605.07725 | SOD: Step-wise On-policy Distillation for Small Language Models | 5/8 | 已在 V2 |
| 12 | 2605.08737 | The Extrapolation Cliff in On-Policy Distillation of Near-Deterministic Structured Outputs | 5/9 | ✅ 已集成 |
| 13 | 2605.08741 | Training with Harnesses: On-Policy Harness Self-Distillation for Complex Reasoning | 5/9 | ✅ 已集成 |
| 14 | 2605.11739 | Learning to Foresee: Unveiling the Unlocking Efficiency of On-Policy Distillation | 5/12 | ✅ 已集成 |
| 15 | 2605.12483 | Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle | 5/12 | ✅ 已集成 |
| 16 | 2605.12652 | Multi-Rollout On-Policy Distillation via Peer Successes and Failures | 5/12 | ✅ 已集成 |
| 17 | 2605.13255 | Respecting Self-Uncertainty in On-Policy Self-Distillation for Efficient LLM Reasoning | 5/13 | ✅ 已集成 |
| 18 | 2605.13643 | Prefix Teach, Suffix Fade: Local Teachability Collapse in Strong-to-Weak On-Policy Distillation | 5/13 | ✅ 已集成 |

**引用增速**: 45 天 18 篇 ≈ 每 2.5 天一篇，5/9 后加速（OPD 方向爆发）

## OPD 论文增长趋势
| 月份 | 论文数 (bib) | 说明 |
|------|-------------|------|
| 2601 (Jan 2025) | 8 | |
| 2602 (Feb) | 14 | |
| 2603 (Mar) | 13 | |
| 2604 (Apr) | 22 | 我们综述发布 (4/1) |
| 2605 (May) | 20 in V2 + **19 new** = 39 | 🔥 爆发!|

**5 月 OPD 论文日均 ~5 篇**--这个方向在加速增长。我们综述发布后(4/1),引用效应带动了更多人做 OPD。

## Scout 维护规则
- 每天 02:40 CST 自动扫描,06:40 CST 补跑
- 新发现的论文追加到本文件("当前待集成" 表)
- V3 集成后:从本文件移除,移到 "已集成" 归档区
- 收录范围:**不限于 autoregressive text LLM**(Diffusion/VLM/Flow Matching/Multimodal 全收)

---

## 【2026-05-13 13:26 老大决策】Self-Generated Data SFT 谱系

### 核心洞察
SPIN / OPSFT / SSD / TABOM 本质是**同一谱系**:self-generated data + SFT,差别在 **rollout-update staleness**。

| 方法 | Rollout 时机 | Staleness |
|------|------------|----------|
| OPSFT (2602.13407) | 每 training step | 严格 on-policy |
| SPIN (2401.01335) | 每 outer iteration | 中度 stale(batch on-policy) |
| SSD (2604.01193) | 训练前一次 | 最 stale(off-policy SFT) |
| TABOM (2605.11854) | 训练前一次(DLM 版本) | 最 stale(off-policy SFT) |

### V3 整改(下次改)
1. §5.3.2 "Minimalist self-distillation" 部分重写为**统一谱系叙事**,明确 rollout-update staleness 光谱
2. **TABOM 加回** GitHub awesome list §5.3.2(之前按纯二元 on-policy 判断删除是不一致的,既然 SSD 留了 TABOM 也该留)
3. Diffusion LM 的 self-distillation 和 autoregressive LM 的 self-distillation **同等对待**

### 判定规则(未来遇到类似论文)
**属于 §5.3.2 的条件**:
- 信号源:model 自己(no teacher / no verifier / no PI)
- 训练方式:在 self-generated data 上做 SFT(cross-entropy / SFT / KL)
- Rollout 频率**不限**(从 pre-training 一次到 per-step 都行)
- 明确区分其 staleness 位置

**不属于 §5.3.2 的**:
- Teacher 拿 PI(reference solution / GT / tools)→ §5.3.1
- Verifier / RLVR / external reward → §5.3.3
- 真正的 external teacher model(不是 self)→ §5.1/§5.2

---

## 【2026-05-13 13:32 老大发现】§5.3.2 / §5.3.3 边界错位

### 问题
§5.3.2 当前有 3 篇用了外部反馈,违反"无外部反馈"的子节定义:

| 论文 | 现在位置 | 实际依赖 | 应该去哪 |
|------|---------|---------|---------|
| RLSD (yang2026selfdistilled) | §5.3.2 + §5.3.3 重复 | 明确用 RLVR environmental feedback | 主归属 §5.3.3 |
| RLRT (kim2026rlrt) | §5.3.2 | GRPO + reward 才能定义 successful rollouts | §5.3.3 |
| OPSFT (zhao2026onpolicy) | §5.3.2 | "outcome verification" 用 GT answer filter | §5.3.1 (PI) 或 §5.3.3,看怎么 frame |

### V3 整改 todo
1. RLSD 主归属 §5.3.3,§5.3.2 末尾只用一句话提及"也有 RLVR-augmented variant"
2. RLRT 移到 §5.3.3(GRPO reward 是显式外部信号)
3. OPSFT 决策:
   - 选项 A:留 §5.3.2,弱化 verification 描述
   - 选项 B:移 §5.3.1(GT answer 当 PI)✅ 推荐
   - 选项 C:移 §5.3.3
4. **§5.3.2 子节标题 'Beyond adversarial games' 重新组织**:
   - 移除上述 3 篇后,剩 SDFT/MTP-SD,归"轻量级 self-as-teacher"
   - 加上"Self-Generated Data SFT 谱系"的统一叙事(含 SPIN/OPSFT/SSD/TABOM)

### 教训
论文 framing(作者怎么 frame 自己)和实际机制(用了什么信号源)是两件事。**分类要看实际机制**,不要被 framing 带跑:
- 论文叫 "self-distilled RLVR" → 不能因为有 "self-distilled" 就放 §5.3.2
- "Outcome verification" 用了 GT → 就是 PI/external,不是纯 self-play

---

## 【2026-05-13 13:45 核实更新】§5.3.2 更严重的错位(5 篇,不是 3 篇)

老大追问后严格对 PDF 核实,§5.3.2 当前 10 篇里实际错位 5 篇:

### 应移出 §5.3.2 的论文

| 论文 | 错位原因(从 PDF 引用) | 应归属 |
|------|----------------------|---------|
| RLSD (2604.03128) | "RLVR environmental feedback" | §5.3.3 |
| RLRT (2605.10781) | 名字就叫 "Rebellious Student: Reversing Teacher Signals for Reasoning Exploration with Self-Distilled RLVR",augments GRPO | §5.3.3 |
| π-Play (2604.14054) | "search tools and interacts with the search engine" + "GRPO using outcome rewards derived from answer correctness" | §5.3.3 |
| OPSFT (2602.13407) | CORRECT(o, a) 用 training set 自带 GT answer a | §5.3.1 (GT answer = PI) |
| SDFT (2601.19897) | "demonstration-conditioned model as its own teacher" - expert demonstrations 是训练时才有的 | §5.3.1 (demos = PI) |

### 真正属于 §5.3.2 的只有 5 篇
- SPIN (2401.01335) - 纯 iterative self-play
- IRIS (2604.20933) - SPIN 的 Rényi 统一框架
- SSD (2604.01193) - 明确 "No verifier, no teacher, no RL, no code execution"
- UniSD (2605.06597) - multi-checkpoint agreement,无外部
- MTP-SD (2602.06019) - frozen self-as-teacher

### V3 整改加强版
1. 把 RLSD / RLRT / π-Play 移到 §5.3.3
2. 把 OPSFT / SDFT 移到 §5.3.1
3. §5.3.2 只保留 5 篇 + TABOM(下次加回)
4. §5.3.2 统一叙事:"Self-Generated Data SFT 谱系":
   - 严格 on-policy: (暂时空,OPSFT 移走了)
   - Batch on-policy: SPIN, IRIS
   - 最 stale: SSD, TABOM
   - Architectural self-distillation: MTP-SD
   - Integrative framework: UniSD

### 这次学到什么
作者论文里说 "no reward" 或 "minimalist" 不等于真的没用外部信号:
- OPSFT 说 "reward-free",但 CORRECT(o, a) 就是用 GT 做 binary reward
- SDFT 说 "no explicit reward function",但用了 demonstrations 当 in-context teacher
- π-Play 说 "without external data",但用了 search engine + outcome reward

**分类要看实际用了什么 oracle 信号,不看作者 framing**。

---

## 【2026-05-13 13:50 老大】§5.3.2 边缘案例多 - 写作时要注意

### 老大原话
"感觉 self play 有很多处于边缘啊,感觉写的时候可以注意下"
"我们现在精读的时候,真的好好分类了么?"

### 写作 note (V3 整改时)
§5.3.2 章节本身就处于多个范式的交界处,多篇论文是**边缘案例**:
- SDFT: demonstration-conditioned 是不是 PI?(我判它是)
- OPSFT: GT-answer-filter 是不是 PI?(我判它是)
- π-Play: 内部 PI + outcome reward 杂交 (横跨 §5.3.1 + §5.3.3)
- RLSD/RLRT: 名字带 RLVR 但作者把它放在 self-distillation 框架下

写 §5.3.2 时**必须明确该章节的硬边界**:
- 不能因为论文用了 "self-distillation" 这个词就放进来
- 如果方法依赖 GT/verifier/reward → 不属于 §5.3.2
- §5.3.2 = "纯 self(无 PI 无 verifier 无外部 reward)" 是**严格的负面定义**
- 在章节开头明确说"以下论文以 self-as-teacher / temperature diversity / iterative checkpoint 为唯一 asymmetry 来源"

### 精读系统现状(老大问的)
**6 篇精读 ≠ 19 篇新论文都精读了**!
- paper_notes.json 只有 6 篇,全是历史经典论文(KD survey, scaling laws...)
- 5/9-5/12 的 19 篇新论文一篇都没经过精读流程
- 之前的分类是用 grep 关键词 + sub-agent 判断做的,没走精读

### 已修复(系统层)
1. **`paper_deep_read_dispatcher.py` 改 reverse sort**:每天优先读最新 PDF(之前是从 1503.* 开始读,新论文要等 90 天)
2. **prompt 大改**:加入 on_policy_mechanism + opd_classification 结构化字段,要求 evidence_quote
3. **cron count 5 → 10**:加快覆盖速度
4. **prompt 内置判定铁律**:明确 "self-distilled ≠ on-policy","no reward ≠ no PI" 等关键陷阱

### V3 整改的硬性 todo
1. 精读 19 篇新 OPD 论文(让 cron 跑几天先覆盖 5/9-5/12 batch)
2. 用精读输出的 primary_section 重新分类
3. §5.3.2 章节移走 5 篇错位论文(RLSD/RLRT/π-Play/OPSFT/SDFT)
4. §5.3.2 重写"硬边界" + 加 staleness 谱系叙事
5. TABOM 加回 §5.3.2(按 staleness 谱系)


---

## 【2026-05-13 13:58 老大尖锐问题】Self-Play 算不算 on-policy?

### 问题
"如果严格按照 on policy 的定义,self play 根本不算 on policy 吧?"

### 严格定义下的回答:**对,大部分不算**

**Strict on-policy**: 计算 gradient 时,sample 必须来自当前正在更新的 π_θ。两次 sample 之间 policy 不能动。

按这个定义:
- PPO/GRPO 都不是 strict on-policy(K-epoch rollout 重用 + importance ratio 修正)
- SPIN/IRIS(batch self-play):每 outer iter sample 一次,inner K epochs SFT → 越来越 off
- SSD/TABOM:sample 一次后做 N epochs SFT → 严重 off-policy
- 真正 strict 的只有 OPSFT 这种"每 step rollout 用完即丢"

### 社区宽松定义
"rollouts come from a recent snapshot of the policy" - staleness 容忍度问题。

### 综述定位的根本张力
§5.3 整个 self-distillation 章节,**严格说大部分论文不是 on-policy**。
- SPIN-family: outer-iter on-policy(K_inner=1 接近,K_inner>1 越来越 off)
- SSD/TABOM: 严重 off-policy SFT on self-generated data
- 真正 strict on-policy 的 self-distillation 只剩有 RL 信号的(π-Play, RLSD, RLRT)

### V3 整改方案
**Option A(保守)**: §5.3 保留,但章节开头明确写 staleness 谱系,承认这些方法处于 OPD 边界。
**Option B(激进,更诚实)**: §5.3 改名 **"Self-Generated Supervision"** 或 **"Teacher-Free Distillation"**,作为 OPD 邻接范式讨论,按 signal source 重新组织(PI / mutual / feedback),不强行套 on-policy 标签。

**倾向 Option B**:更经得起审稿,避免 "你 SPIN 哪算 on-policy" 的尴尬。综述定位调整为 "OPD 及其邻接范式"。

### Action items
1. 等老大决定 Option A vs B
2. V3 §5.3 章节开头**必须**有"on-policy spectrum" 段落,把 staleness 讲清楚
3. Abstract / Intro 不要 overclaim "all of self-distillation is on-policy"


---

## 【2026-05-13 Scout】+2 new, 8 rejected

### ✅ 新确认 (1 篇)

| # | arXiv ID | Published | Title | §Section | Key Contribution |
|---|----------|-----------|-------|----------|------------------|
| 20 | 2605.07177 | 5/8 | HyperEyes: Dual-Grained Efficiency-Aware Reinforcement Learning for Parallel Multimodal Search Agents | §8.2 | OPD micro-level: dense token-level teacher signals on failed student rollouts for multimodal agents (Xiaohongshu+Cambridge) |

### ❌ 排除 (8 篇)

| arXiv ID | Title | 排除原因 |
|----------|-------|---------|
| 2605.10875 | Compute Where it Counts: Self Optimizing Language Models | 推理效率动态分配,不是 KD (ICML'26) |
| 2605.09920 | Verifier-Free RL for LLMs via Intrinsic Gradient-Norm Reward | 纯 RL intrinsic reward,无 teacher/distillation (ACL'26 Findings) |
| 2605.08887 | Ace-Skill: Bootstrapping Multimodal Agents with Prioritized and Clustered Evolution | Self-evolving agents 经验蒸馏,非 OPD |
| 2605.07579 | Your Language Model is Its Own Critic: Reinforcement Learning with Value Estimation from Actor's Internal States | 纯 RL baseline estimation,无 distillation |
| 2605.04559 | Beyond Static Best-of-N: Bayesian List-wise Alignment for LLM-based Recommendation | IR/推荐领域 BoN alignment,非 LLM capability distillation (SIGIR'26) |
| 2605.10518 | Infinite Mask Diffusion for Few-Step Distillation | 标准 MDM 蒸馏加速,无 on-policy student sampling |
| 2605.07820 | Scaling Categorical Flow Maps | Flow matching self-distill 加速,标准 progressive distillation |
| 2605.07274 | Structured Role-Aware Policy Optimization for Multimodal Reasoning | 纯 GRPO + credit assignment,"self-distilled contrasts" 只是命名 |
| 2605.06850 | How to Compress KV Cache in RL Post-Training? Shadow Mask Distillation for Memory-Efficient Alignment | 纯 RL 效率优化（KV cache 压缩后的 off-policy bias 修复），不是 OPD。5/14 删除 |
| 2605.09536 | TAD: Temporal-Aware Trajectory Self-Distillation for Fast and Accurate Diffusion LLM | Off-policy: teacher conditioned on GT response 生成静态 trajectory，student 学预录轨迹，不是 on-policy sampling。5/14 删除 |
| 2605.11651 | Hide to See: Reasoning-prefix Masking for Visual-anchored Thinking in VLM Distillation | 标准 offline KD: teacher (Qwen3-VL-Thinking) 分布直接做监督，student 没有 on-policy rollouts。5/14 删除 |

### Self-Check

```
论文: HyperEyes (2605.07177)
类型: 第一类(OPD方法) - OPD 应用于 multimodal agents
判定级别: Level 2
判定: 收录
证据: Abstract 明确 "we adapt On-Policy Distillation (OPD) to inject dense token-level corrective signals from an external teacher on failed rollouts"
综述状态: 待加入下次综述 (§8.2)

论文: Shadow Mask Distillation (2605.06850)
类型: 不收录
判定级别: Level 2
判定: 不收录
证据: 纯 RL 训练效率优化。解决 KV cache 压缩引入的 off-policy bias,不是 teacher→student 的 OPD 方法。dense/sparse 是同一个模型的不同 attention mask。
综述状态: 不收录(5/14 纠正)
```

## 【2026-05-14 Scout】+4 new, 6 rejected

### ✅ 新确认 (4 篇)
| # | arXiv ID | Date | Title | §Section | Notes |
|---|----------|------|-------|----------|-------|
| 1 | 2605.10189 | 2026-05-11 | ProteinOPD: Towards Effective and Efficient Preference Alignment for Protein Design | §8.2 Emerging Domains | Multi-teacher OPD for protein PLMs; geometric consensus of weighted teachers; student generates protein sequences on-policy |
| 2 | 2605.10194 | 2026-05-11 | TRACE: Distilling Where It Matters via Token-Routed Self On-Policy Alignment | §6.1 + §5.3.1 | Token-routed self-OPD; FKL on key spans, RKL on error spans, GRPO on rest; solves all-token KL collapse in self-OPD |
| 3 | 2605.09329 | 2026-05-10 | Test-Time Speculation | §8.2 Emerging Domains | Online OPD at test-time for speculative decoding; draft(student) generates, target(teacher) provides distribution, draft updates during inference |
| 4 | 2605.06230 | 2026-05-07 | Safactory: A Scalable Agentic Infrastructure for Training Trustworthy Autonomous Intelligence | §8.1 Industrial Deployment | Shanghai AI Lab; unified evolutionary pipeline integrating RL + OPD for agent safety; dedicated §5.3 on on-policy distillation |

### ❌ 排除 (6 篇)
| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.11556 | Hindsight Hint Distillation: Scaffolded Reasoning for SWE Agents from CoT-free Answers | SFT on pre-collected scaffolded trajectories; no real-time teacher feedback in training loop |
| 2605.07327 | Teacher-Feature Drifting: One-Step Diffusion Distillation with Pretrained Diffusion Representations | Image diffusion distillation, not LM |
| 2605.08354 | Auto-Rubric as Reward: From Implicit Preferences to Explicit Multimodal Generative Criteria | RL alignment via rubric-based reward, not OPD |
| 2605.07503 | Diffusion-APO: Trajectory-Aware Direct Preference Alignment for Video Diffusion Transformers | Video diffusion DPO/GRPO, not on-policy distillation |
| 2605.09422 | Perception Without Engagement: Dissecting the Causal Discovery Deficit in LMMs | ⚠️ arXiv ID 错误，2605.09422 实际是无关论文 |
| 2605.07276 | Signal Reshaping for GRPO in Weak-Feedback Agentic Code Repair | Pure GRPO paper; OPD mentioned only as boundary comparison |

### Self-Check

```
论文: ProteinOPD (2605.10189)
类型: 第一类(OPD方法) - 新应用域(蛋白质设计)
判定级别: Level 2
判定: 收录
证据: "distills their knowledge into a shared student via token-level OPD on the student's own trajectories"; "adapts a pretrained PLM into preference-specific teachers"; multi-objective geometric consensus
综述状态: 待加入下次综述 (§8.2)

论文: TRACE (2605.10194)
类型: 第一类(OPD方法) - Token-routed self-OPD
判定级别: Level 2
判定: 收录
证据: "On-policy self-distillation (self-OPD) densifies RLVR by letting a policy teach itself under privileged context"; token-routed FKL/RKL on critical spans; student generates on-policy rollouts
综述状态: 待加入下次综述 (§6.1 + §5.3.1)

论文: Test-Time Speculation (2605.09329)
类型: 第一类(OPD方法) - Test-time online distillation
判定级别: Level 2
判定: 收录
证据: "treating the target as the teacher, the draft as the student, and the target's distribution over the draft tokens as the distillation sample on which the draft performs an optimization step"; satisfies all 3 OPD criteria (student on-policy generation, teacher feedback, distribution update in loop)
综述状态: 待加入下次综述 (§8.2)

论文: Safactory (2605.06230)
类型: 第二类(OPD系统/基础设施)
判定级别: Level 2
判定: 收录
证据: Paper has dedicated §5.3 "On-policy Distillation" section; "Autonomous Evolution Platform for asynchronous reinforcement learning and on-policy distillation"
综述状态: 待加入下次综述 (§8.1)

论文: Hindsight Hint Distillation (2605.11556)
类型: 不收录
判定级别: Level 2
判定: 不收录
证据: Training is SFT on successful hint-scaffolded trajectories collected beforehand. "The model then self-distills these scaffolded trajectories" = offline SFT, no teacher providing real-time feedback during training loop. More akin to iterative RFT with hint synthesis.

论文: Teacher-Feature Drifting (2605.07327)
类型: 不收录
判定级别: Level 1
判定: 不收录
证据: Pure image generation (ImageNet/SDXL), not language model. "One-Step Diffusion Distillation" for image synthesis.
```

## 【2026-05-14 Scout (Evening)】+8 new, 2 rejected

> **2026-05-29 修正**: 本段第 1 行 `2605.13724 AnyFlow` 在 5/14 当时按 "video diffusion 也收 §8.2 Emerging Domains" 收录，5/29 老大复核后推翻 — 按 5/15 收录范围明确不收 video diffusion，已 reject 加入 `excluded-papers.md`。剩余 7 篇均已集成进 latex-v4 bib。

### ✅ 新确认 (8 篇)
| # | arXiv ID | Date | Title | §Section | Notes |
|---|----------|------|-------|----------|-------|
| 1 | 2605.13724 | 2026-05-13 | AnyFlow: Any-Step Video Diffusion Model with On-Policy Flow Map Distillation | §8.2 Emerging Domains | NVIDIA; flow-map backward simulation; on-policy distillation for video diffusion; 1.3B–14B |
| 2 | 2605.13643 | 2026-05-13 | Prefix Teach, Suffix Fade: Local Teachability Collapse in Strong-to-Weak On-Policy Distillation | §7.2 Failure Modes | Qwen3 family; BIC change-point release rule; dense OPD degrades when teacher margin vanishes in suffix |
| 3 | 2605.13501 | 2026-05-13 | Reward-Weighted On-Policy Distillation with an Open Property-Equivalence Verifier for NL-to-SVA Generation | §8.2 + §4.3 | Verifier-reward-weighted FKL; property-equivalence checker; new SOTA on NL2SVA |
| 4 | 2605.13255 | 2026-05-13 | Respecting Self-Uncertainty in On-Policy Self-Distillation for Efficient LLM Reasoning | §6 Training Efficiency | Entropy-guided confidence gate; causal-lookahead variant; Qwen3-4B/8B |
| 5 | 2605.13230 | 2026-05-13 | Teacher-Guided Policy Optimization for LLM Distillation | §4.3 RL-Augmented | Dense directional teacher guidance on RKL; fixes uninformative negative feedback; NLP2CT/NEU |
| 6 | 2605.12913 | 2026-05-13 | Revisiting DAgger in the Era of LLM-Agents | §8.2 Emerging Domains | Turn-level student-teacher interpolation for SWE agents; +3.9pp SWE-bench Verified at 4B |
| 7 | 2605.12652 | 2026-05-12 | Multi-Rollout On-Policy Distillation via Peer Successes and Failures | §6 Training Efficiency | Peer-conditioned teacher signals; success/failure rollout groups; CMU |
| 8 | 2605.11853 | 2026-05-12 | GEAR: Granularity-Adaptive Advantage Reweighting for LLM Agents via Self-Distillation | §6 Training Efficiency | On-policy student vs GT-conditioned teacher divergence; adaptive segment boundaries; +20% over GRPO |

### ❌ 排除 (2 篇)
| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.13665 | Robot Squid Game: Quadrupedal Locomotion for Traversing Narrow Tunnels | Robotics policy distillation (not LLM), quadruped RL |
| 2605.12798 | Emergent and Subliminal Misalignment Through the Lens of Data-Mediated Transfer | Safety/alignment study; uses OPD as experimental condition but not contributing to OPD methodology |

### Self-Check

```
论文: AnyFlow (2605.13724)
类型: 第一类(OPD方法) - Video diffusion on-policy distillation
判定级别: Level 2
判定: 收录
证据: "enabling efficient on-policy distillation that reduces test-time errors (i.e., discretization error in few-step sampling and exposure bias in causal generation)"; flow-map backward simulation decomposes rollout into transitions for on-policy training
综述状态: 待加入下次综述 (§8.2)

论文: Prefix Teach, Suffix Fade (2605.13643)
类型: 第二类(OPD分析) - Failure mode analysis
判定级别: Level 2
判定: 收录
证据: "We demonstrate that this assumption sometimes fails to hold in strong-to-weak OPD settings"; "local teachability collapse" — identifies when dense OPD supervision stops being effective; directly relevant to OPD practitioners
综述状态: 待加入下次综述 (§7.2)

论文: RWOPD (2605.13501)
类型: 第一类(OPD方法) - Verifier-reward-weighted OPD
判定级别: Level 2
判定: 收录
证据: "on-policy distillation method that samples student rollouts, scores them with an open SymbiYosys+Z3 Property-Equivalence Checker (PEC), and applies a verifier-reward-weighted forward-KL gradient from a frozen 14B teacher on verifier-passable rollouts"
综述状态: 待加入下次综述 (§8.2 + §4.3)

论文: EGRSD (2605.13255)
类型: 第一类(OPD方法) - Self-distillation with entropy gating
判定级别: Level 2
判定: 收录
证据: "On-policy self-distillation trains a reasoning model on its own rollouts while a teacher... provides dense token-level supervision"; proposes entropy-guided confidence gate that down-weights high-entropy positions
综述状态: 待加入下次综述 (§6)

论文: TGPO (2605.13230)
类型: 第一类(OPD方法) - RL-augmented OPD
判定级别: Level 2
判定: 收录
证据: "Teacher-Guided Policy Optimization (TGPO), an on-policy algorithm that incorporates dense directional guidance by leveraging teacher predictions conditioned on the student's rollout"; "remains on-policy, the algorithm integrates seamlessly with existing RLVR frameworks"
综述状态: 待加入下次综述 (§4.3)

论文: Revisiting DAgger (2605.12913)
类型: 第一类(OPD方法) - DAgger for LLM agents
判定级别: Level 2
判定: 收录
证据: "collects trajectories through a turn-level interpolation of student and teacher policies, and the student is then trained on these trajectories using supervised labels provided by the teacher"; "By directly interacting with environments, we expose the model to realistic states" — satisfies on-policy generation + teacher feedback
综述状态: 待加入下次综述 (§8.2)

论文: MOPD (2605.12652)
类型: 第一类(OPD方法) - Multi-rollout OPD
判定级别: Level 2
判定: 收录
证据: "Multi-Rollout On-Policy Distillation (MOPD), a peer-conditioned distillation framework that uses the student's local rollout group to construct more informative teacher signals"; "training on student-generated trajectories" with "peer successes and failures"
综述状态: 待加入下次综述 (§6)

论文: GEAR (2605.11853)
类型: 第一类(OPD方法) - Self-distillation credit assignment
判定级别: Level 2
判定: 收录
证据: "GEAR compares an on-policy student with a ground-truth-conditioned teacher to obtain a reference-guided divergence signal for identifying adaptive segment boundaries and modulating local advantage weights"; on-policy generation + privileged teacher supervision
综述状态: 待加入下次综述 (§6)
```

## 【2026-05-15 Scout】+1 new, 1 rejected

### ✅ 新确认 (1 篇)
| # | arXiv ID | Date | Title | §Section | Notes |
|---|----------|------|-------|----------|-------|
| 1 | 2605.12741 | 2026-05-12 | Learning with Rare Success but Rich Feedback via Reflection-Enhanced Self-Distillation | §5.3.1 + §6 | On-policy self-distillation with reflection from failures; teacher conditioned on retrospective reflections + persistent playbook; single-rollout outperforms GRPO 8× samples; Amazon/UCSD |

### ❌ 排除 (1 篇)
| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.13165 | STOP: Structured On-Policy Pruning of Long-Form Reasoning in Low-Data Regimes | On-policy generation + SFT on pruned self-data only; explicitly "cannot rely on large-scale teacher distillation"; no teacher providing token-level supervision in training loop; efficiency technique not OPD |

### Self-Check

```
论文: RESD (2605.12741)
类型: 第一类(OPD方法) - Self-OPD with reflection-enriched teacher
判定级别: Level 2
判定: 收录
证据: "on-policy self-distillation"; "self-teacher provides actionable token-level supervision"; "Reflection-Enhanced Self-Distillation (RESD) transforms raw failure feedback into active corrective supervision"; student generates rollouts, teacher conditioned on retrospective reflections provides dense token-level supervision
综述状态: 待加入下次综述 (§5.3.1 + §6)

论文: STOP (2605.13165)
类型: 不收录
判定级别: Level 2
判定: 不收录
证据: "cannot rely on large-scale teacher distillation or heavy test-time control"; "STOP constructs self-distilled traces from the model" then prunes and does SFT; no teacher supervision in the training loop. Explicitly contrasts with teacher-guided pruning. This is on-policy generation + SFT on curated data (§5.3.2 borderline but no teacher = not OPD).
```

<!-- 2026-05-15 标题全量校验修正，共 45 处 -->

## 【2026-05-16 Scout】+1 new, 3 rejected

### ✅ 新确认 (1 篇)
| # | arXiv ID | Date | Title | §Section | Notes |
|---|----------|------|-------|----------|-------|
| 1 | 2605.15155 | 2026-05-14 | Self-Distilled Agentic Reinforcement Learning | §4.3 + §8.2 | SDAR: OPSD as gated auxiliary to RL for multi-turn agents; sigmoid gate on teacher-endorsed tokens; handles negative teacher rejections; Qwen2.5/Qwen3 on ALFWorld/WebShop/Search-QA; Meituan/ZJU |

### ❌ 排除 (3 篇)
| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.15141 | Causal Forcing++: Scalable Few-Step Autoregressive Diffusion Distillation for Real-Time Interactive Video Generation | Video diffusion distillation (output modality = video, not text); outside scope |
| 2605.14417 | Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control | Humanoid robot control; not LLM distillation |
| 2605.09317 | Mem-W: Latent Memory-Native GUI Agents | GUI agent architecture with latent memory; not distillation |

### Self-Check

```
论文: SDAR (2605.15155)
类型: 第一类(OPD方法) - RL-Augmented OPSD for multi-turn agents
判定级别: Level 2
判定: 收录
证据: "On-Policy Self-Distillation (OPSD) complements RL by introducing dense token-level guidance from a teacher branch augmented with privileged context"; SDAR "treats OPSD as a gated auxiliary objective while keeping RL as the primary optimization backbone"; "maps detached token-level signals into a sigmoid gate, strengthening distillation on teacher-endorsed positive-gap tokens"; student generates on-policy rollouts in multi-turn environments, teacher with privileged context provides dense supervision
综述状态: 待加入下次综述 (§4.3 + §8.2)
```

## Scout Scan — 2026-05-16 18:40 UTC

**Scan scope**: arXiv API (9 keyword patterns) + arXiv search web
**Papers scanned**: 51 unique May 2026 papers
**New candidates evaluated**: 12 (8 from API + 4 from web search)
**Result**: 0 new OPD papers found

### Evaluated & Rejected (12 papers)

| arXiv ID | Title | Rejection Reason |
|----------|-------|-----------------|
| 2605.10805 | Reasoning Is Not Free: Robust Adaptive Cost-Efficient Routing for LLM-as-a-Judge | LLM-as-Judge routing, no distillation |
| 2605.10207 | LASAR: Latent Adaptive Semantic Aligned Reasoning for Generative Recommendation | Recommender system, no OPD |
| 2605.06650 | Beyond Negative Rollouts: Positive-Only Policy Optimization with Implicit Negative Gradients | Pure RLVR (GRPO alternative), no distillation |
| 2605.05478 | LANTERN: LLM-Augmented Neurosymbolic Transfer with Experience-Gated Reasoning Networks | RL transfer learning, not language model OPD |
| 2605.04507 | Distilling Bayesian Belief States into Language Models for Auditable Negotiation | Off-policy distillation (static dataset), no on-policy sampling |
| 2605.02405 | Closed-Loop CO2 Storage Control With History-Based RL | Reservoir RL control, not language model |
| 2605.02320 | ANO: A Principled Approach to Robust Policy Optimization | Pure RL optimizer (PPO replacement), no distillation |
| 2605.01457 | CoFlow: Coordinated Few-Step Flow for Offline Multi-Agent Decision Making | Offline MARL, not language model OPD |
| 2605.14442 | GGBound: A Genome-Grounded Agent for Microbial Life-Boundary Prediction | Biology agent, unrelated |
| 2605.14382 | Delta Forcing: Trust Region Steering for Interactive Autoregressive Video Generation | Video generation, output is video |
| 2605.14278 | KVPO: ODE-Native GRPO for Autoregressive Video Alignment | Video alignment RL, output is video |
| 2605.11665 | Nautilus: From One Prompt to Plug-and-Play Robot Learning | Robot learning framework, no OPD |


## 【2026-05-17 Scout (retry 06:40 CST)】+0 new, 0 rejected

**Retry reason**: Main scout (02:40 CST) failed
**Scan scope**: arXiv API (9+ keyword patterns, broad distillation queries)
**Papers scanned**: 168 unique from API (filtered to May 14-16 window = 7 candidates)
**Result**: 0 new OPD papers found — all recent papers already captured by 2026-05-16 18:40 UTC scout

**Note**: Saturday arXiv — no new submissions since last scout window. All May 2026 OPD papers through 2605.15155 already tracked.


## 【2026-05-19 Scout (03:01 CST)】+5 new papers confirmed

**Scan scope**: arXiv RSS (cs.CL, cs.LG, cs.AI) keyword filter + DuckDuckGo search
**Note**: arXiv API was rate-limited (429); used RSS feeds instead
**Papers scanned**: ~300+ RSS items filtered to 53 candidates, 9 evaluated at Level 2
**Result**: 5 confirmed new OPD papers

### ✅ Confirmed (5 papers)

| ID | Title | Type | Section | Evidence |
|----|-------|------|---------|----------|
| 2605.15239 | Reducing the Safety Tax in LLM Safety Alignment with On-Policy Self-Distillation | OPD Method | §5.3.1 | Student generates rollouts, frozen teacher (same model + safety privileged context) provides per-token KL supervision. Named "OPSA". |
| 2605.15532 | DeltaPrompts: Escaping the Zero-Delta Trap in Multimodal Distillation | OPD Efficiency | §6.2 | On-policy distillation for VLMs; proposes prompt selection via answer divergence to maximize OPD signal. NVIDIA Research. |
| 2605.15726 | Nudging Beyond the Comfort Zone: Efficient Strategy-Guided Exploration for RLVR | Hybrid OPD+RL | §5.3.1 + §4.3 | GRPO + strategy-conditioned rollouts + distillation objective to transfer behaviors to base policy. Strategy context = privileged info. |
| 2602.12262 | Few-Step Diffusion Language Models via Trajectory Self-Distillation | OPD Diffusion LM | §5.3.2 + §8.2 | Diffusion LM (output=text). Student generates few-step denoising trajectories. DDO (reverse KL) = on-policy. Self-distillation. |
| 2605.15417 | $f$-Trajectory Balance: A Loss Family for Tuning GFlowNets, Generative Models, and LLMs with Off- and On-Policy Data | OPD Theory | §4.1 + §7.3 | ICML 2026. f-divergence loss family with on-policy gradient = f-divergence. Generalizes KL-based OPD losses. |

### ❌ Rejected at Level 1 (4 papers)

| ID | Title | Reason |
|----|-------|--------|
| 2605.16241 | Offline Semantic Guidance for Efficient Vision-Language-Action Policy Distillation | Output modality = robotic actions, not text/language |
| 2605.13143 | On the Generalization of Knowledge Distillation: An Information-Theoretic View | General KD theory, no on-policy focus |
| 2605.15913 | Towards Generalization of Block Attention via Automatic Segmentation and Block Distillation | Standard offline KD for attention architecture |
| 2511.19399 | DR Tulu: Reinforcement Learning with Evolving Rubrics for Deep Research | Pure RLVR, no distillation component |


## 【2026-05-19 Scout (03:01 CST) — Batch 2: API Backfill】+4 new papers confirmed

**Scan scope**: arXiv HTTPS API (9 keyword queries, 80 results each) — caught older papers missed in prior scouts
**Note**: 5/9 queries hit 429 rate limit; still retrieved 150 unique papers from 4 queries
**Papers scanned**: 106 new (unknown) IDs from API
**Result**: 4 confirmed new OPD papers (older, missed in previous scouts)

### ✅ Confirmed (4 papers)

| ID | Title | Type | Section | Evidence |
|----|-------|------|---------|----------|
| 2505.18952 | Online Knowledge Distillation with Reward Guidance | OPD Method | §4.3 | Online PbKD: iteratively collects new preference data from current student policy. Min-max reward optimization between student and teacher. White-box Q-value extension. |
| 2502.02671 | On Teacher Hacking in Language Model Distillation | OPD Analysis | §7.2 | ICML 2026 (DeepMind). Identifies "teacher hacking" (analogous to reward hacking). Shows online data generation mitigates it. Directly compares off vs on-policy distillation. |
| 2510.02227 | More Than One Teacher: Adaptive Multi-Guidance Policy Optimization for Diverse Exploration | OPD Method | §4.3 + §5.1 | AMPO: student on-policy rollouts (GRPO), multi-teacher guidance replaces failures on-demand. Comprehension-based selection mechanism. Code: github.com/SII-Enigma/AMPO |
| 2604.02621 | Reinforcement Learning-based Knowledge Distillation with LLM-as-a-Judge | OPD Method | §4.3 + §5.2 | Student generates on-policy reasoning trajectories, judge LLM provides scalar reward (single-token). RL training (GRPO-style) optimizes student to maximize judge feedback. Label-free KD. |

### ❌ Rejected at Level 2 (2 papers)

| ID | Title | Reason |
|----|-------|--------|
| 2604.03873 | SODA: Semi On-Policy Black-Box Distillation for Large Language Models | "Semi on-policy" is marketing — actual mechanism is ONE-TIME static student snapshot + DPO. No iterative on-policy sampling during training. Student distribution captured once before training begins. |
| 2509.16965 | Preference Distillation via Value based Reinforcement Learning | Off-policy DPO with teacher value function shaping. Explicitly states "does not require additional rollouts." No on-policy student generation. |

### ❌ Rejected at Level 1 (many, key ones listed)

| ID | Title | Reason |
|----|-------|--------|
| 2605.03849 | Stream-R1 | Video generation, output is video |
| 2506.03541 | Debate, Reflect, and Distill | Static debate-generated data for DPO/preference optimization |
| 2504.13471 | From Large to Super-Tiny | Deployment pipeline, not OPD method |
| 2505.11100 | Bidirectional Distillation | Multi-agent RL behaviors, not language model OPD |
| 2506.01523 | Alignment as Distribution Learning | Theoretical alignment/preference, no distillation focus |
| 4 | 2605.18740 | 2026-05-19 | Vision-OPD: Learning to See Fine Details for Multimodal LLMs via On-Policy Self-Distillation | 🚧 第一类(Self-Distill, VLM) | §5.3.2 | 5/20 | ✅ is_opd=yes |
| 5 | 2605.17862 | 2026-05-19 | f-OPD: Stabilizing Long-Horizon On-Policy Distillation with Freshness-Aware Control | 🚧 第一类(Async OPD) | §6.1 | 5/20 | ✅ is_opd=yes |

## 【2026-05-20 Scout (06:40 CST, retry)】+6 new papers confirmed

**Scan scope**: arXiv /list/cs.CL/new + /list/cs.LG/new (title keyword filter → abstract verification)
**Note**: Main 02:40 scout failed (arXiv API 429 rate-limit on 7/9 queries). Retry used HTML listings instead.
**Papers scanned**: 936 unique IDs from listing pages, 932 new (unknown)
**Result**: 6 confirmed new OPD papers

### ✅ Confirmed (6 papers)

| ID | Title | Type | Section | Evidence |
|----|-------|------|---------|----------|
| 2605.16826 | Decoupling KL and Trajectories: A Unified Perspective for SFT, DAgger, Offline RL, and OPD in LLM Distillation | OPD Theory | §4.1 + §7.1 | Decomposes sequence-level KL for autoregressive distillation. Shows OPD/off-policy couple prefix source with KL direction. Unifies SFT, DAgger, offline RL, OPD under one framework. |
| 2605.17497 | Self-Supervised On-Policy Distillation for Reasoning Language Models | OPD Method | §5.3.1 + §4.3 | SSOPD: GRPO-style on-policy rollouts. Correct completions = self-generated teacher witnesses. Wrong completions provide on-policy prefixes for correction. Hybrid RL+distillation. |
| 2605.18299 | SD-Search: On-Policy Hindsight Self-Distillation for Search-Augmented Reasoning | OPD Method | §5.3.1 + §8.1 | On-policy rollouts with interleaved search calls. Hindsight self-distillation provides step-level credit for individual queries. No external teacher/reward model needed. |
| 2605.17873 | HINT-SD: Targeted Hindsight Self-Distillation for Long-Horizon Agents | OPD Method | §5.3.1 + §8.1 | On-policy agent trajectories with selective hindsight feedback. Sparse outcome rewards + feedback-conditioned self-distillation. Only targets unsuccessful turns (efficiency). |
| 2605.16865 | MixSD: Mixed Contextual Self-Distillation for Knowledge Injection | OPD Method | §5.3.2 + §6.2 | External-teacher-free. Constructs supervision from model's own distribution (expert + naive conditionals). Distribution-aligned self-supervision. Compares against "on-policy self distillation baselines". |
| 2605.16941 | Roll Out and Roll Back: Diffusion LLMs are Their Own Efficiency Teachers | OPD Diffusion LM | §5.3.2 + §8.2 | WINO+ distills verified denoising trajectories (from student's own WINO inference) into model parameters. DLLMs self-teach. Output=text (LLaDA/MMaDA). On-policy trajectories. |

### ❌ Rejected (1 paper)

| ID | Title | Reason |
|----|-------|--------|
| 2605.18643 | Post-Trained MoE Can Skip Half Experts via Self-Distillation | Architecture optimization (dynamic expert routing), not OPD training paradigm. No student rollouts during training. |

---

## 2026-05-21 (CST) Scout

**Scout time**: 16:15 CST
**Note**: arXiv API fully rate-limited (429 on all 9 queries, 2 retries). Fallback: arXiv RSS feeds for cs.CL (171 items) + cs.LG (459 items), keyword-filtered for distillation/on-policy/RL terms.
**Papers scanned**: 630 unique from RSS, 93 matched broad keywords, 5 investigated for OPD relevance
**Result**: 1 confirmed new OPD-relevant paper (2605.21266 G2D was retracted on 2026-05-22 after manual deep-read — pure RLVR + offline DPO, no teacher, not OPD)

### ✅ Confirmed (1 paper)

| ID | Title | Type | Section | Evidence |
|----|-------|------|---------|----------|
| 2605.20643 | AVSD: Adaptive-View Self-Distillation by Balancing Consensus and Teacher-Specific Privileged Signals | OPD Method | §5.3.2 + §6.2 | Self-distillation learns on-policy from own trajectories; same model as student and teacher; teacher conditioned on privileged info (solutions, demonstrations, feedback). Balances consensus across multiple teacher views. Dense token-level feedback without external model. |

### ❌ Rejected (3 papers)

| ID | Title | Reason |
|----|-------|--------|
| 2605.20555 | Complementing RL with SFT through logit averaging in post-training of LLMs | Averages logits of frozen SFT + trainable RL policy in GRPO. Not distillation per se — no teacher-student training signal. Architecture trick for combining policies. |
| 2605.20285 | Introspective X Training: Feedback Conditioning Improves Scaling | Offline reward-conditioned training using critique annotations. No on-policy distillation — uses reward model feedback as prefix conditioning, not teacher rollouts. |
| 2605.20865 | Multi-Step Likelihood-Ratio Correction for RLVR | PPO surrogate improvement via N-step likelihood ratio traces. Purely RL optimization technique, no distillation component. |

---

## 2026-05-22 (CST) Scout

**Scout time**: 17:24 CST (manual trigger from session, ahead of cron 18:40)
**Window**: 2026-05-21 → 2026-05-22 CST
**Result**: 8 new in-window candidates; deep-read 8/8 ok; 5 confirmed inserted, 1 边界 staging, 1 analysis staging, 1 reject

### ✅ Confirmed Inserted (5 papers — committed ea0126c)

| ID | Title | Section | Pair |
|----|-------|---------|------|
| 2605.21851 | OPPO: Bayesian Value Recursion for Token-Level Credit Assignment in LLM Reasoning | §4.3 | Qwen3-32B → Qwen3-4B |
| 2605.21924 | Visual-Advantage On-Policy Distillation for Vision-Language Models | §6.1 | Qwen3-VL-8B → Qwen3-VL-2B |
| 2605.22240 | Unlocking Proactivity in Task-Oriented Dialogue (AOPD+STPR) | §5.3.2 | Qwen3-4B → Self (privileged view) |
| 2605.22263 | Tailoring Teaching to Aptitude: Direction-Adaptive Self-Distillation | §4.2 | Qwen3-4B → Self (privileged) |
| 2605.22511 | Search-E1: Self-Distillation Drives Self-Evolution in Search-Augmented Reasoning | §5.3.2 | Qwen2.5-7B → Self (privileged context) |

### 🟡 Edge Cases — 老大已判 (2 papers, 2026-05-22)

| ID | Title | Verdict |
|----|-------|---------|
| 2605.22675 | Self-Policy Distillation via Capability-Selective Subspace Projection (SPD) | ✅ **收** — 已加入「当前待集成」待精读 queue。OPD 谱系 self-distill, low-rank capability subspace + KV projection + NTP loss; staleness 是连续光谱不二元判定 (类似 SSD/TABOM) |
| 2605.22731 | Post-Training is About States, Not Tokens: A State Distribution View | ❌ **不收 awesome** — analysis-only, 不提新方法; 已记入 excluded-papers.md 标 "awesome 历来不收 analysis"; 综述 Theory/Perspective 章节可作为参考引用 |

### ❌ Rejected (1 paper)

| ID | Title | Reason |
|----|-------|--------|
| 2605.22478 | Matching with Deliberation: Test-Time Evolutionary Hierarchical Multi-Agents for ZS-CIR | Test-time multi-agent system, no training. "Reasoning policy distillation" is a hand-crafted prompting protocol, not gradient distillation. |

---

## 2026-05-23 (CST) Scout

**Scout time**: 18:40 CST (cron)
**DATE WINDOW**: 2026-05-22 to 2026-05-23 (CST)
**Result**: arXiv API returned 0 candidates across 9 queries (normal Saturday — arXiv announces Mon-Fri only; Fri batch consumed yesterday).
**Carryover from `_staging/`**: 7 PDFs (6 already in paper_notes from 5/22, 1 new: 2605.21984).

### Deep-read (carryover, 1 paper)

| ID | Title | Submitted | is_opd | Verdict |
|----|-------|-----------|--------|---------|
| 2605.21984 | (deep-read excluded; out of OPD scope) | 2026-05-21 | no | exclude (also outside today's window) |

### Triage re-runs on staged-and-already-noted papers (6)

Re-triage caught up on entries lingering in `_staging/` after yesterday:

| ID | Verdict | Section |
|----|---------|---------|
| 2605.20258 | KEEP | §5.3.2 — Complementary Self-Distillation for Contextual Integrity (Qwen2.5-7B / Llama-3.1-8B → Self; PoE via two feedback-conditioned self-teachers, reverse KL) |
| 2605.22675 | KEEP | §5.3.2 — Self-Policy Distillation via Capability-Selective Subspace Projection (Qwen2.5-{0.5B,7B} → Self; KV-subspace projection hooks steer self-generation, LoRA-finetune) |
| 2605.20201 | exclude | (re-triage downgrade) |
| 2605.20256 | exclude | (re-triage downgrade) |
| 2605.20654 | exclude | (re-triage downgrade) |
| 2605.21699 | exclude | (re-triage downgrade) |

### Awesome List

- 2605.20258 -> §5.3.2 (commit cc7a99c)
- 2605.22675 -> §5.3.2 (commit 247c039)
- pushed to Awesome-LLM-On-Policy-Distillation master @ 247c039

### Summary

- New OPD-confirmed papers today: **0** (Saturday, arXiv quiet)
- Carryover keeps inserted into Awesome List: **2** (both §5.3.2 self-distill)
- known_arxiv_ids.txt: 258 -> 254 (net -4 after triage downgrades and dedup)

## 2026-05-24 (CST) Scout

**Scout time**: 22:43 CST (cron self-repair — original 18:40 cron run missed/skipped, this run triggered by `opd-scout-retry` watchdog detecting absent entry)
**DATE WINDOW**: 2026-05-23 → 2026-05-24 (CST)
**Pre-check**: Sunday (CST) — arXiv quiet, recommended skip full scan; retry-queue path also empty
**Result**: arXiv API returned 0 candidates across 9 queries within window. `_staging/` empty (no carryover).

### Summary

- New OPD-confirmed papers today: **0** (Sunday — arXiv announces Mon–Fri only; weekend window quiet)
- Carryover from `_staging/`: **0**
- Awesome List commits: **0**
- known_arxiv_ids.txt: 259 (unchanged)
- Deep-read / 3-condition / triage: **skipped** (no candidates)

**Next scout**: Monday 2026-05-25 02:40 CST (regular cron) — first weekday batch since Friday 5/22, expect 5–15 candidates window covering Sat+Sun+Mon submissions.

## 2026-05-26 (CST) Scout

**Scout time**: 18:40 CST
**DATE WINDOW**: 2026-05-25 → 2026-05-26 (CST)
**Pre-check**: Tuesday — passes (workday; window covers Mon+Tue CST submissions).

### Summary

- arXiv API: **fully throttled** (9/9 queries returned 429 / timeout) — fell back to RSS feeds (`rss.arxiv.org/rss/cs.CL`, `cs.LG`, `cs.AI`) per `paper-kb` skill's `arxiv-scout-fallback.md` runbook.
- RSS yielded **166** candidates by loose keyword filter (`distill`, `on-policy`, `student`, etc.) across the 3 categories.
- After image/video/audio/RL-only/inference-only narrowing → **4 strong + 4 edge** candidates.
- After abstract + §Method check → **1** in-window OPD-relevant candidate: `2605.25582` ERPD.
- After V3 deep-read + 3-condition filter → **0 confirmed OPD**; ERPD rejected (R1: rollout once-before-training, V3 verdict `is_opd=no`).

### ✅ Confirmed Inserted (0 papers)

(none)

### 🗑️ Rejected (1 paper)

| arXiv ID | Title | Rule | Reason |
|----------|-------|------|--------|
| 2605.25582 | Extreme Region Policy Distillation (ERPD) | R1 | V3 deep-read: `rollout_frequency=once-before-training`, `signal_source=self`, `is_opd=no`. "we first sample responses for 1,000 prompts to construct a static dataset" → Stage 1 is multi-step off-policy updates on a fixed batch (not in-loop rollouts); Stage 2 distills the resulting teacher's token-level log-ratio signal into base policy under trust-region constraint. Core contribution is RL optimization decoupling sample / KL efficiency, distillation framing is the stabilization mechanism. Same family as static-dataset SFT-distill (SPD/MixSD/WINO+) — `papers-meta/excluded-papers.md` logged. |

### 🟡 Edge Cases (0 papers)

(none — all 4 edge candidates rejected at abstract+method check before deep-read)

### Out of DATE WINDOW (1 paper, noted but not processed)

| arXiv ID | Title | Submission |
|----------|-------|------------|
| 2605.24432 | Found in Conversation (FiC): LLMs Teach Themselves to Close the Multi-Turn Gap — View-Asymmetric Self-Distillation | 2026-05-23 06:58Z (= 5/23 14:58 CST) — out of 5/25–5/26 CST window. **Worth revisiting**: abstract describes student samples on multi-turn view + frozen single-turn teacher = candidate on-policy self-distillation. Will re-trigger if it surfaces in a future precheck refresh. |

### Pre-deep-read filtered out (other RSS hits, summary only)

- **2605.25525** SAE-FD — Sparse autoencoder feature distillation for continual learning; feature-space regularizer, no student rollouts in training loop.
- **2605.25676** Llamion / KEPT (XKD) — Frozen equal-size teacher distill on text corpus to convert Orion-14B → Llama-arch; classic off-policy SFT-distill, **not** OPD.
- **2605.25745** SLT (Selective Latent Thinking) — Three-stage: span-compression + future prediction + trajectory-level RL on correctness reward; no teacher distill term, RL-only Stage 3.
- **2605.25378** CollectionLoRA — Multi-Teacher On-Policy Distillation but for **image editing diffusion LoRAs** (output = images, not text) → scope-out.
- **2605.23954** EchoDistill — Audio-LLM noisy-to-clean self-distillation; output modality is audio responses, treated as out-of-scope for text OPD survey.
- **2605.24793** Speculative Decoding "Beyond the Target" — SPD framework (draft + target verifier), inference acceleration, not training distillation.
- **2605.25977** Creative Quality Alignment — SFT on ~100 CoT annotations, no student rollouts.
- **2605.25549** BC Protocol — Data production method (dual-expert dialogue for high-quality CoT), not a training method.

### Phase outcomes

- Phase 0 PRE-CHECK: ✅ workday
- Phase 1 SCOUT: ⚠️ arXiv API fully throttled → RSS fallback succeeded (166 raw, 1 strong candidate after narrowing)
- Phase 2 DEEP-READ: ✅ 1 paper processed in 62s
- Phase 3 TRIAGE: ✅ 1 excluded (PDF → `.trash-2026-05-26-triage-exclude/`)
- Phase 3.5 3-CONDITION: ✅ confirms R1 reject (no false negatives possible since `is_opd=no` already)
- Phase 4 AWESOME LIST: skipped (0 keeps)
- Phase 5 REFRESH IDS: pending below

## 2026-05-25 (CST) Scout

**Scout time**: 18:41 CST
**DATE WINDOW**: 2026-05-24 → 2026-05-25 (CST)
**Pre-check**: Monday (CST) — `scout_precheck.py --both` exit 1 (recommend skip; window covers Sun+Mon CST, arXiv announces Mon–Fri only, but Mon morning batch announces Sat-late submissions which fall outside today's CST window). `_staging/` empty (no carryover).

### Summary

- New OPD-confirmed papers today: **0** (Monday CST precheck skip — see `references/opd-daily-pipeline-runbook.md`)
- Carryover from `_staging/`: **0**
- Awesome List commits: **0**
- known_arxiv_ids.txt: 259 (unchanged after refresh)
- Deep-read / 3-condition / triage: **skipped** (no candidates, no carryover)

**Next scout**: Tuesday 2026-05-26 18:40 CST (regular cron) — window will cover Mon+Tue CST submissions, expect 5–15 candidates.


## 2026-05-27 (CST) Scout

**Scout time**: 18:41 CST
**DATE WINDOW**: 2026-05-26 → 2026-05-27 (CST)
**Pre-check**: ✅ weekday (exit 0)
**arXiv API**: 重度限流 (HTTP 429 反复), 3 次重试后 9 query 中跑通 7 unique results
**S2 fallback**: 全程 429, 无 cross-check 增量 (DATE WINDOW 已覆盖)

### Summary

- 9 query 跑通 (3 次重试) → 7 unique results in window
- 6 already known → 1 new candidate
- Phase 2 deep-read: 1 paper, is_opd=yes
- Phase 3 triage: 1 keep
- Phase 3.5 3-condition: ✅ KEEP (rollout=per-outer-iter, signal=external-teacher, +teacher-distill)
- Phase 4 awesome list: ✅ 1 commit pushed (§5.1)
- Phase 5 refresh ids: 278 → 279

### Candidates → Verdict

| arXiv ID | Title | scout matched | is_opd (V3) | 3-cond | Verdict |
|---|---|---|---|---|---|
| 2605.27255 | Pair-In, Pair-Out: Latent Multi-Token Prediction for Efficient LLMs | "on-policy distillation" | yes (§5.1) | KEEP (R-OK) | ✅ awesome §5.1 |

### Detail: 2605.27255 (Pair-In, Pair-Out / PIPO)

- **Model pair**: Qwen3.5-9B (teacher, uncompressed) → compressed Qwen3.5 (latent MTP w/ pair-in compressor + pair-out MTP head)
- **OPD mechanism**:
  - Training stage = SFT 2 epochs (next-pair prediction + random PAD injection) **+ 1 epoch OPD** (student rollouts → teacher on clean text → reverse-KL + confidence BCE)
  - `L_OPD = KL(p_s ‖ p_t) + λ_conf * BCE(c, min(p_t/p_s, 1))` — 显式 teacher distill (reverse KL)
  - `rollout_frequency = per-outer-iter`, `signal = teacher logits`, source = external Qwen3.5-9B teacher
- **Data**: DAPO-Math (17.4k math) + Codeforces (16.1k code)
- **Why §5.1 (not §6.3/§4.3)**: V3 reasoning notes "core contribution is a white-box on-policy distillation method that reuses teacher logits as free supervision for a confidence head, with distillation being the central training mechanism". Secondary touch §6.3 (efficient inference) + §4.3 (auxiliary losses), but primary methodological contribution is the OPD recovery stage post-MTP compression.
- **Abstract trap check**: abstract 主线写 MTP/latent compression/speculative decoding, OPD 不在 abstract 但 §method 显式 reverse-KL + student rollout + external teacher → 3-condition KEEP 合规

### Awesome list commit

```
[master 65f3e9e] Add 2605.27255 to §5.1
1 file changed, 3 insertions(+), 1 deletion(-)
README.md: 170 → 171 entries
git push: 247c039..65f3e9e (success)
```

### Next scout

Thursday 2026-05-28 18:41 CST — window 2026-05-27 → 2026-05-28

---

## 2026-05-28 (Thu) — daily pipeline cron

### Summary

- arXiv API fully rate-limited (9 queries × 3 retries, all 429/timeout)
- Cross-check via Semantic Scholar: 5 results, 1 OPD candidate
- Phase 2 deep-read: 1 paper (ROSD), is_opd=yes, strict OPD
- Phase 3 triage: 1 keep
- Phase 3.5 3-condition: ✅ KEEP (rollout=per-step, signal=self-teacher, standalone JSD loss)
- Phase 4 awesome list: ✅ 1 commit pushed (§5.3.2), badge 175→176
- Phase 5 refresh ids: 280 → 281

### Candidates → Verdict

| arXiv ID | Title | Source | is_opd (V3) | 3-cond | Verdict |
|---|---|---|---|---|---|
| 2605.28014 | ROSD: Reflective On-Policy Self-Distillation for Language Model Reasoning across Domains | S2 cross-check | yes (§5.3.2) | KEEP (R-OK) | ✅ awesome §5.3.2 |
| 2605.27967 | Multi-Teacher Knowledge Distillation via Teacher-Informed Mixture Priors | S2 cross-check | — | — | ❌ standard multi-teacher KD, no on-policy |
| 2605.27885 | Reflective Dialogue between Teacher and Solver Agents for VQA | S2 cross-check | — | — | ❌ inference-time agent dialogue, no training |

### Detail: 2605.28014 (ROSD)

- **Model pair**: Qwen3-4B/8B (self-teacher conditioned on reflection) → Qwen3-4B/8B
- **OPD mechanism**:
  - Self-reflector extracts corrective idea (e) + error quote (q) from wrong rollouts
  - Self-teacher conditioned on corrective idea e, not full correct solution
  - JSD distillation applied only from error quote position onward (quote-localized)
  - `L_ROSD = Σ_t m_t · KL(π_θ(·|x,y<t) ∥ π_θ(·|x,e,y<t))` where m_t masks valid prefix
  - `rollout_frequency = per-step`, `signal = self-teacher (same model)`
- **Results**: Qwen3-4B avg 72.83% (vs GRPO 69.86%, SDPO 67.02%); strong OOD preservation
- **Code**: https://github.com/ZiqiZhao1/ROSD
- **Why §5.3.2**: Self-distillation variant (same model as teacher), extends OPSD/SDPO with error-focused reflection

### arXiv API note

arXiv API was completely unresponsive across 3 retry attempts (30s + 60s intervals). All 9 queries returned 429/timeout. Semantic Scholar cross-check recovered the one new OPD candidate. Next scout should check if arXiv API has recovered.

### Awesome list commit

```
[master 3f64b57] Add 2605.28014 to §5.3.2
1 file changed, 3 insertions(+), 1 deletion(-)
git push: f7ca6a3..3f64b57 (success)
```

### Next scout

Friday 2026-05-29

---

## 2026-05-30 (Sat) — daily pipeline cron

### Summary

- Phase 0 PRE-CHECK: ✅ refreshed 284 IDs, no weekend skip
- Phase 1 SCOUT: 30 new in-window candidates (RSS-primary, S2 rate-limited 429), all downloaded to `pdfs/_staging/`
- Phase 2 DEEP-READ: 30/30 ok, 438.6s total (workers=3); **1 is_opd=yes**, 29 not-OPD
- Phase 3 TRIAGE: 3 keep (1 new + 2 carryover from prior days), 29 excluded → trash + excluded-papers.md + known_arxiv_ids.txt
- Phase 3.5 3-CONDITION: ✅ all 3 KEEP (28791 R-OK self, 27255 R-OK external teacher, 28014 R-OK self-teacher)
- Phase 4 awesome list: ✅ 1 new commit pushed (`9047e7c`, §5.3.1), badge 175→176
- Phase 5 refresh ids: 284 → 285

### Candidates → Verdict (only OPD-relevant rows shown; 29 excluded omitted)

| arXiv ID | Title | Source | is_opd (V3) | 3-cond | Verdict |
|---|---|---|---|---|---|
| 2605.28791 | Skill-Conditioned Gated Self-Distillation for LLM Reasoning | rss/ok | yes (§5.3.1) | KEEP (R-OK) | ✅ awesome §5.3.1 (NEW) |
| 2605.27255 | Pair-In, Pair-Out: Latent Multi-Token Prediction for Efficient LLMs | carryover (5/27) | yes | KEEP (R-OK) | ✅ already in awesome §6.3 (5/29 backlog) |
| 2605.28014 | ROSD: Reflective On-Policy Self-Distillation for Language Model Reasoning | carryover (5/28) | yes (§5.3.2) | KEEP (R-OK) | ✅ already in awesome §5.3.2 (5/28 commit) |

### Detail: 2605.28791 (Skill-Conditioned Gated Self-Distillation)

- **Model pair**: Qwen3-1.7B/4B/8B (skill-conditioned self-teacher) → Qwen3-1.7B/4B/8B (plain student)
- **OPD mechanism**:
  - Plain-prompt student rollout `y ∼ π_θ(· | x)`; verifier returns scalar outcome `r ∈ {−1, 1}`
  - Skill-conditioned multi-teacher pool retrieved per token via skill bank (online updated)
  - `L_SGSD(x) = Σ_k α_k(x) · ρ_k · ℓ̄^(k)`, with bounded gate `ℓ_gate(Δ) = log2 − log(1 + exp(−Δ²/(2τ_g)))`
  - `rollout_frequency = per-step`, `signal_source = self` (skill-conditioned), `teacher_signal = logits`
- **Data**: English subset of DAPO-Math-17K
- **Why §5.3.1 (Privileged Information)**: Self-distillation variant where the *skill bank* (retrieved skill-mistake pairs + outcome polarity) acts as privileged information conditioning the teacher-side context — fits the OPSD/GATES axis rather than pure self-distillation (§5.3.2) or external-feedback (§5.3.3)

### arXiv API / RSS note

- arXiv API still rate-limited via S2 (429 on all 4 cross-check queries). RSS feed worked: 558 cs.AI items, 62 OPD-keyword matches, 133 unique candidates, 30 selected for deep-read after dedup.
- 2 PDFs in `_staging/` were carried over from prior days (27255, 28014) and skipped by `--from-staging` since already in paper_notes.

### Awesome list commits today

```
[master 9047e7c] Add 2605.28791 to §5.3.1 (Skill-Conditioned Gated Self-Distillation for LLM Reasoning)
1 file changed, 3 insertions(+), 1 deletion(-)
git push: 9ab34ac..9047e7c (success)
```

### Next scout

Sunday 2026-05-31 (cron may skip per `scout_precheck` weekend rule, manual trigger acceptable for spot check)

## 2026-06-02 (Tue) — daily pipeline cron

### Summary

- Phase 0 PRE-CHECK: ✅ exit 0 (non-weekend), known_arxiv_ids.txt = 285 IDs
- Phase 1 SCOUT: **0 new in-window candidates** (RSS 78 + S2 13 = 91 unique; 91/91 rejected by `2606` date window — all are `2605.xxxxx` residuals)
- Phase 2 DEEP-READ: skip (no candidates)
- Phase 3 TRIAGE / 3.5 3-CONDITION: skip
- Phase 4 awesome list / 6 loss-taxonomy / 7 site refresh: skip (no downstream change)
- Phase 5 refresh ids: ✅ kept at 285 (no new entries today)

### 铁律 #4 investigation (0-candidate sanity)

Per pipeline 铁律 #4, investigated the 0-result. Direct arxiv API query (`cat:cs.CL AND abs:"on-policy distillation"`, sorted by submittedDate desc) returns:

```
2605.31490  2026-05-29  Are Full Rollouts Necessary for On-Policy Distillation?
2605.30833  2026-05-29  Your Teacher Can't Help You Here: Combating Supervision Fidelity Decay in OPD
2605.30251  2026-05-28  Same Evidence, Different Answers: Canonical-Context On-Policy Distillation
2605.29584  2026-05-28  GAPD: Gold-Action Policy Distillation for Agentic RL
...
```

Latest OPD paper is `2605.31490` (May 29). No `2606.xxxxx` papers exist on arxiv yet for OPD-keyword search. Conclusion: legitimately empty day; scout pipeline correct.

### Awesome list commits today

(none)

### Next scout

Wednesday 2026-06-03 (regular weekday cron).


## 2026-06-03 (Wed) — daily pipeline cron

### Summary

- Phase 0 PRE-CHECK: ✅ exit 0 (non-weekend), known_arxiv_ids.txt = 400 IDs
- Phase 1 SCOUT: 30 in-window candidates (RSS 184 + S2 12 = 196 unique; 13 rejected by `2606` date window; 111 skipped already-known; 30 final)
- Phase 2 DEEP-READ: ✅ 39 PDFs deep-read (39 today + 7 leftover 2605.* already in notes); **all 39 today's papers is_opd=no** (pure keyword bycatch: Plankton, Bayesian Opt, Diffusion Policy, Wireless, Bandit Sim, etc.)
- Phase 3 TRIAGE: 17 keep / 140 exclude (140 PDFs moved to trash + logged to excluded-papers.md)
- Phase 3.5 3-CONDITION on 17 keeps:
  - 15 KEEP (all already in awesome from prior catch-up runs)
  - 1 REJECT (R3) — `2605.29584` GAPD: RL-only公式, signal=self, no teacher-distill term (consistent with prior R3 verdict)
  - 1 UNKNOWN — `2606.01080` ThinkSwitch: `student_rollout_in_training=no`, `rollout_frequency=n/a`; v3 reasoning admits "thinking checkpoint generates traces ... decode deterministically with temperature 0" = pre-computed offline traces. Same-class as 6/03 cleanup batch (14 内部矛盾论文 is_opd=yes 但 rollout=no). **Per scope 铁律 #6+#8 reject; not added to awesome.**
- Phase 4 awesome list: **0 new insertions** (all today's qualifying OPD papers were already in awesome via prior daily runs; only failures fell through both filters)
- Phase 5 refresh ids: 400 IDs (after triage cleanup)

### Reject details

| aid | rule | reason |
|---|---|---|
| 2605.29584 | R3 | GAPD: GRPO-style RL公式 + 无 teacher-distill 项, signal=self → 伪 OPD |
| 2606.01080 | scope (rollout=no) | ThinkSwitch: 离线 trace 预生成 + LoRA + SLERP 权重插值, 训练循环内无 student rollout, 是 context distillation (offline KD between thinking↔instruct checkpoints) 不是 OPD |

### Awesome list commits today

(none — 0 net additions)

### Next scout

Thursday 2026-06-04 (regular weekday cron).

### 6/03 增补 (PR-driven 发现)

社区 PR `nick7nlp/Awesome-LLM-On-Policy-Distillation#2` (作者 @Myashka, 2026-06-03) 提出加 Trust-Region Behavior Blending — 这是 5-28~6-02 catch-up 时 RSS 漏掉的真 OPD 论文 (`2605.31159`, 2026-05-29 提交)。同时在 web 验证过程中发现另一篇相关工作也漏了 (`2512.17636` TRAPO)。

两篇 deep-read + 3-cond 都通过, 已 inserter 加入:

| arxiv | 标题 | § | pair (student → teacher) | loss class |
|---|---|---|---|---|
| `2605.31159` | Trust-Region Behavior Blending for OPD | §6.2 | Qwen3-1.7B-Base / Qwen3-0.6B-Base → Qwen3-8B / Qwen3-4B | RKL (high) |
| `2512.17636` | Trust-Region Adaptive Policy Optimization | §4.1 | Qwen2.5-Math-7B / Qwen2.5-7B-Instruct → DeepSeek-R1 | KL+RL (medium) |

PR 提交 metadata 与论文原文 2 处差异 (PDF 原文 `Qwen3-1.7B-Base ← Qwen3-8B` / `Qwen3-0.6B-Base ← Qwen3-4B`):
- pair 方向反 (PR teacher→student vs README 惯例 student→teacher)
- 漏 -Base 后缀 (PR 用 Qwen3-1.7B, 原文是 Qwen3-1.7B-Base)

为避免错误信息进 README, 走标准 inserter 流程而非直接 merge PR。PR 待 close + 评论 (作者不上 contributor 榜)。

CHANGELOG.md 增 [2026-06-03] entry, Pending Papers section 增两行, 主表 §6.2 / §4.1 各增一行。Phase 6 loss-taxonomy 重跑: 174 papers classified (KL+RL=39, RKL=44, FKL=34, Symmetric=21, Other=29, f-Div=2, Preference=5)。两个 PNG 已重生成。

### 6/03 进一步清理 (self-play 体系)

由 `2602.13407` (On-Policy SFT for Efficient Reasoning) 触发的范围二审, 扫描 awesome 中所有 `is_opd=yes` 论文寻找同性质 (signal=self/PI(GT)/verifier + loss 无 teacher-distribution KL term):

| arxiv | 标题 | 之前归 | loss class | 删除理由 |
|---|---|---|---|---|
| `2602.13407` | On-Policy SFT for Efficient Reasoning | §5.3.2 | Other (NLL) | 论文自称 "reward-free SFT", 标准 STaR/RFT, 无 distillation |
| `2510.18874` | Retaining by Doing | §8.2 | Other (RL+SFT) | GRPO + KL-to-ref-policy, 非 teacher; 同 GAPD R3 性质 |
| `2509.25100` | ORPO-Distill | §5.2 | Preference (ORPO) | DPO-style preference (chosen vs rejected), 同 SPIN/IRIS 体系 |

3 篇均移出 awesome+site, paper_notes 保留 (供未来 audit / 综述 background 引用)。

8 篇扫到的误报保留 (它们用 self-snapshot / EMA / privileged-self 提供 teacher distribution, 是合法 self-distillation): 2605.12741 / 2605.11613 / 2605.17497 / 2605.18299 / 2605.22511 / 2605.22263 / 2605.27186 / 2512.17636.

副作用: paper count 168 → **165**; loss-taxonomy 重新生成器 (`generate_loss_taxonomy.py`) 加 `restrict-to-awesome` filter, 现在只统计 README 内的 OPD-method 论文 (152 篇, 排除 13 篇 analysis-of-OPD 和 6 篇 reference-only)。

---

## 2026-06-04 daily pipeline

Phase 1 scout: 30 in-window candidates from RSS. Phase 2 deep-read on 80 staged PDFs (combined with 06-02/06-03 backlog), 3 is_opd=yes. Phase 3 triage: 22 keep (most already in README), **5 truly new candidates** to evaluate via 3-condition + manual review.

### REJECT (3 篇, 不进 awesome / site)

| arxiv | 标题 | rule | 理由 |
|---|---|---|---|
| `2605.29584` | GAPD: Gold-Action Policy Distillation for Agentic RL in KBQA | R3 (auto) | GRPO advantage shaping with `lambda_gapd * A_gapd_ik`; signal=self, no `D_KL(π‖π_T)` teacher distill term. 同 PSDISTILL 体系。 |
| `2606.01080` | ThinkSwitch: Context Distillation with LoRA + Weight Interpolation | R1 (manual) | Iterative weight-merging via SLERP + offline QLoRA SFT on answer-only pairs. No student rollout in loss-loop. v3 LLM 偏宽松判 yes, 实为 model-merging recipe。 |
| `2606.01215` | Distilling Neuro-Symbolic Programs into 3D Multi-modal LLMs | R3 (manual) | Three-stage curriculum: perception SFT → CoT-SFT on offline symbolic traces → GRPO with format/grounding rewards. "Distillation" 指离线 program-to-CoT 翻译, 非 on-policy teacher distribution distill. |

### KEEP (2 篇, 进 awesome list)

| arxiv | 标题 | § | pair (student → teacher) | loss class |
|---|---|---|---|---|
| `2606.02684` | Filter, Then Reweight: Rethinking Optimization Granularity in OPD | §6.1 | (TBD via inserter) | KL+RL |
| `2606.03603` | World Models Meet Language Models: On the Complementarity of Concrete and Abstract Reasoning | §5.3.1 | (TBD via inserter) | RKL |

---

## 2026-06-05 daily pipeline

Phase 1 scout: 30 in-window candidates from RSS (date window: 2026-06-04 → 2026-06-05 CST).

### Candidates (pending Phase 2 deep-read + Phase 3.5 3-cond)

| arxiv | title |
|---|---|
| `2606.04036` | Self-Distilled Policy Gradient |
| `2606.04694` | DuDi: Dual-Signal Distillation with Cross-Lingual Verbalizer |
| `2606.04703` | Rethinking Continual Experience Internalization for Self-Evolving LLM Agents |
| `2606.05122` | Self-Evaluation Is Already There: Eliciting Latent Judge Calibration in Base LLMs with Minimal Data |
| `2606.05152` | Reinforcement Learning from Rich Feedback with Distributional DAgger |

### Phase 2 deep-read result (80 PDFs, 2606.04xxx + 2606.05xxx + carryover)

77 ok / 3 fail (2606.03077, 2606.03096, 2606.03180 worker exit 1) / 8 is_opd=yes / 69 is_opd=no.

### Phase 3.5 + manual review

11 candidates not yet in README → 8 KEEP + 3 REJECT.

#### REJECT (3 篇, 不进 awesome / site)

| arxiv | 标题 | rule | 理由 |
|---|---|---|---|
| `2605.29584` | GAPD: Gold-Action Policy Distillation for Agentic RL in KBQA | R3 (auto) | GRPO advantage shaping with `lambda_gapd * A_gapd_ik`; signal=self, no `D_KL(π‖π_T)` teacher distill term. PSDISTILL pattern. (carryover from 06-04, reconfirmed) |
| `2606.01080` | ThinkSwitch: Context Distillation with LoRA + SLERP weight interpolation | R1 (manual) | `student_rollout_in_training=no`, `rollout_frequency=n/a`. SLERP weight-merging recipe + offline QLoRA SFT, no on-policy rollout in loss-loop. (carryover from 06-04, reconfirmed) |
| `2606.01215` | Distilling Neuro-Symbolic Programs into 3D Multi-modal LLMs | R3 (manual) | Three-stage: perception SFT → CoT-SFT on offline symbolic traces → GRPO with format/grounding rewards. "Distillation" = offline program-to-CoT translation. No teacher-distribution distill term. (carryover from 06-04, reconfirmed) |

#### KEEP (8 篇, 进 awesome list)

| arxiv | 标题 | § | pair | loss class (preview) |
|---|---|---|---|---|
| `2606.03089` | Constitutional On-Policy Safe Distillation | §5.3.1 | Qwen3-VL-4B → Self (PI safety-constitution) | RKL |
| `2606.03532` | When Should the Teacher Move? Temporal Coupling and Stability in Self OPD | §6.2 | Qwen3-8B → Self (EMA-history teacher) | KL+RL |
| `2606.03620` | Physics-Guided Policy Optimization with Self-Distillation | §6.1 | Qwen3-8B → Self (privileged feedback) | RKL |
| `2606.04036` | Self-Distilled Policy Gradient | §5.3.1 | Qwen3-4B → Self (PI ground-truth) | RKL+RL |
| `2606.04694` | DuDi: Dual-Signal Distillation with Cross-Lingual Verbalizer | §5.1 | Qwen2.5-3B-Instruct → Qwen2.5-0.5B | KL+RL |
| `2606.04703` | Rethinking Continual Experience Internalization | §6.2 | Qwen3-4B-Instruct → Self | RKL |
| `2606.05122` | Self-Evaluation Is Already There: Eliciting Latent Judge Calibration | §4.3 | GPT-5.4 → Qwen3-4B-Base | KL+RL |
| `2606.05152` | RL from Rich Feedback with Distributional DAgger | §4.1 | Qwen3-8B → Self | FKL |

paper count: 170 → **178**.

### 2026-06-05 manual deep-read audit (post-pipeline)

User challenged the auto-pipeline's keep verdicts, prompting hand-read of all 22 papers from 06-02 ~ 06-05. Result: 1 paper mis-classified, removed.

#### REJECT (1 paper, demoted from KEEP after PDF read)

| arxiv | 标题 | rule | 理由 |
|---|---|---|---|
| `2512.17636` | Trust-Region Adaptive Policy Optimization (TRAPO) | R1 (manual) | Authors explicitly frame as "hybrid SFT+RL" not OPD. TrSFT loss applies to **offline expert prefix tokens** (DeepSeek-R1 demos), not student-rollout positions. The student does rollout (suffix completion) but only gets RL/GRPO supervision there. Same hybrid-imitation+RL pattern as `2602.13407` On-Policy SFT removed on 06-03. paper count 178 → 177. |

#### Section reassignment (no removal)

| arxiv | 当前 | 建议 | 理由 |
|---|---|---|---|
| `2606.05122` | §4.3 RL-Augmented | §5.2 Black-Box | Distill term is masked NLL on judge's discrete score tokens; teacher (judge LLM) only emits scalar labels not logits. Closer to API-constrained black-box than RL+KL. |

### 2026-06-05 cron-scout 09:32 follow-up

cron `30 9 * * 1-5` 早晨 09:32 跑 `--max 50` 抓了 50 个 candidates(比手动 04:14 那次 `--max 30` 多 20 个)。Phase 2 deep-read 50 篇:
- 47 OK / 3 fail (worker exit)
- **is_opd=yes 数: 0**

50 篇全部为 RSS 关键词触发的非 OPD 论文(generic distillation / GRPO RL / quantization / VLM grounding 等)。无需 Phase 4-7 操作。Marked TRAPO + ThinkSwitch + Neuro-Symbolic + GAPD 在 paper_notes 里为 `is_opd=edge`,防止下次 triage 又当 keep 重列。

---

## 2026-06-06 (Sat) — daily pipeline

Phase 1 scout: 30 in-window candidates from RSS (DATE WINDOW: 2026-06-05 → 2026-06-06 CST).

### Candidates (pending Phase 2 deep-read + Phase 3.5 3-cond)

| arxiv | title |
|---|---|
| `2606.05315` | LoRi: Low-Rank Distillation for Implicit Reasoning |

### Phase 2-3.5 result (33 PDFs incl. 3 retry from yesterday)

33 ok / 0 fail / 1 is_opd=yes (auto) / 32 is_opd=no.

#### Manual deep-read audit on 1 keep candidate

| arxiv | 标题 | 判决 | 理由 |
|---|---|---|---|
| `2606.05315` | LoRi: Low-Rank Distillation for Implicit Reasoning | **REJECT (R1)** | Paper explicitly states "without token-level sampling". Student's "trajectory" z_t is deterministic hidden-state vector, not sampled tokens. Teacher hidden states are precomputed offline and fixed during training (low-rank Tucker factors). This is hidden-state KD (à la MiniLM / layer-wise KD), not on-policy distillation. v3 LLM mis-fired `rollout_frequency=per-step` — same R1-violation mis-classification pattern as TRAPO (2512.17636) hand-rejected on 06-05. |

**Net: 0 papers added today.** README count stays at 177.
