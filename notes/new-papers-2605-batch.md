# New OPD Papers Batch — 2605 (May 7-8 2026)

## Paper 1: Asymmetric On-Policy Distillation (AOPD) (arXiv:2605.06387)

### 核心创新 (1-2 句)
Standard OPD's advantage-weighted policy gradient fails in non-positive advantage regions (high variance, vanishing gradients, exploration black holes). AOPD replaces negative reinforcement with localized forward-KL divergence minimization on teacher's top-K support, creating an asymmetric exploitation-imitation framework.

### 方法概要 (150 字)
AOPD decomposes the standard OPD loss into positive and non-positive advantage regions. For tokens where A_t > 0, standard policy gradient (exploitation) is preserved. For tokens where A_t ≤ 0, the framework switches to truncated forward-KL guidance on the teacher's top-K token support. This resolves three OPD pathologies: (1) heavy-tailed variance from unbounded negative advantages, (2) vanishing gradients at zero-advantage positions where teacher still has rich distributional info, and (3) "exploration black holes" where suppressing a wrong token redistributes mass proportional to the student's prior—unable to boost low-probability correct alternatives. The threshold τ=0 (probability difference) determines the switching point; τ=-1 recovers standard OPD, τ=1 recovers GKD.

### 关键实验结果
| Setting | Model | AOPD gain over OPD |
|---------|-------|-------------------|
| Strong init (long warmup) | Qwen2.5-Math-1.5B/7B | +4.09 avg |
| Weak init (short warmup) | Qwen2.5-Math-1.5B/7B | +8.34 avg |
| Tool-use continual learning | Sequential adaptation | Better capability retention |

Key benchmarks: AIME 2024/2025, MATH-500, competition-level math

### BibTeX
```bibtex
@article{jia2026aopd,
  author    = {Nan Jia and Haojin Yang and Xing Ma and Jiesong Lian and Shuailiang Zhang and Weipeng Zhang and Ke Zeng and Xunliang Cai and Zequn Sun},
  title     = {{Asymmetric On-Policy Distillation: Bridging Exploitation and Imitation at the Token Level}},
  journal   = {arXiv preprint arXiv:2605.06387},
  year      = {2026},
  url       = {https://arxiv.org/abs/2605.06387},
}
```

### 综述分类
- 主章节: §4.2 Adaptive Divergence
- 相关章节: §4.1 Fixed Divergence (Forward KL as intervention), §7.1 Success Conditions (exploration black hole = failure mode)
- 与现有方法关系:
  - **递进** from standard OPD (GKD/ExOPD): identifies and fixes specific gradient pathologies
  - **互补** with TAID (adaptive interpolation): TAID adapts λ between F-KL/R-KL, AOPD switches entirely based on advantage sign
  - **对比** with CaOPD: both address OPD failures but CaOPD focuses on calibration, AOPD on gradient structure

### 综述集成建议
- 建议插入位置: §4.2 after TAID discussion (token-level adaptive mechanisms)
- 建议叙事角度: AOPD represents a principled diagnosis of WHY standard OPD gradients fail at the token level, providing theoretical justification for asymmetric treatment. The "exploration black hole" analysis (Eq.5: probability mass redistributes proportional to student prior, unable to boost novel tokens) offers a formal explanation for the weak-initialization failures observed empirically across many OPD methods.

---

## Paper 2: Near-Policy Distillation (NPD) (arXiv:2605.05940)

### 核心创新 (1-2 句)
Decouples student generation from training in OPD, converting the on-policy loop into an asynchronous SFT-compatible pipeline with sequence packing. Uses Δ-IFD filtering to prevent policy drift from degrading into off-policy learning.

### 方法概要 (150 字)
NPD reformulates on-policy distillation as a three-stage async pipeline: (1) Batch-generate student rollouts via vLLM, (2) Pack sequences and compute teacher top-k logits via parallel prefill, (3) Train student with composite CE+KD loss using sequence packing. The key challenge is policy lag: the generation policy drifts from training policy over async iterations. NPD addresses this with sparse student updates (periodic model syncs) and Δ-IFD filtering, which estimates teacher-student discrepancy via Instruction-Following Difficulty metric and rejects extreme out-of-distribution samples. This keeps optimization in a "safe proximal learning zone" despite asynchronous updates. The framework achieves 8.1× throughput speedup over synchronous on-policy baselines while outperforming SFT by 8.09%.

### 关键实验结果
| Metric | Value | Context |
|--------|-------|---------|
| Speedup over on-policy | 8.1× | Throughput (tokens/sec) |
| vs SFT baseline | +8.09% | Average across math benchmarks |
| openPangu-Embedded-1B | 68.73% | SOTA for 1B class, > Qwen3-1.7B (63.69%) |
| NPD → RL synergy | Best RL init | Narrows exploration space for subsequent GRPO |

### BibTeX
```bibtex
@article{rang2026npd,
  author    = {Miao Rang and Zhenni Bi and Hang Zhou and Kai Han and Xuechun Wang and An Xiao and Xinghao Chen and Yunhe Wang and Hanting Chen},
  title     = {{Near-Policy Distillation: Accelerating On-Policy Distillation via Asynchronous Generation and Selective Packing}},
  journal   = {arXiv preprint arXiv:2605.05940},
  year      = {2026},
  url       = {https://arxiv.org/abs/2605.05940},
}
```

### 综述分类
- 主章节: §6.3 Compute Optimization
- 相关章节: §6.1 Token/Sample Weighting (Δ-IFD as sample selection), §7.1 Success Conditions (near-policy zone)
- 与现有方法关系:
  - **递进** from synchronous OPD: same quality, 8.1× faster
  - **互补** with DistiLLM-2's adaptive sample reuse: both reduce on-policy sampling cost, different mechanisms
  - **对比** with PRISM (proximal regularization): NPD uses filtering to stay proximal, PRISM uses explicit constraints

### 综述集成建议
- 建议插入位置: §6.3 Compute Optimization, after existing throughput discussions
- 建议叙事角度: NPD addresses the fundamental compute bottleneck of OPD (synchronous generation-training coupling) by proving that near-policy training with careful filtering can match on-policy quality. The Δ-IFD threshold defines a "near-policy zone" between on-policy and off-policy, offering a practical middle ground. The NPD→RL pipeline result is relevant for §8.1 (industrial pipelines showing OPD as initialization for RL).

---

## Paper 3: OPSD Compresses What RLVR Teaches (arXiv:2605.06188)

### 核心创新 (1-2 句)
In thinking-enabled mathematical reasoning, OPSD primarily acts as a COMPRESSION mechanism (shortening correct reasoning traces) rather than a CORRECTION mechanism (fixing incorrect ones). Proposes the SFT→RLVR→OPSD pipeline where OPSD is a post-RL compaction stage.

### 方法概要 (150 字)
The paper applies OPSD separately to correct-only vs incorrect-only rollout groups to isolate compression from correction effects. Key findings: (1) Correct-only OPSD preserves accuracy while substantially shortening responses (compression), (2) Incorrect-only OPSD damages accuracy (correction fails), (3) The hindsight-conditioned self-teacher can identify redundancy in long thinking traces but cannot reliably supply better alternative reasoning steps. Three alternative explanations tested and rejected: richer teacher context, mid-trace feedback reinjection, and longer training—none turn OPSD into a correction mechanism. Proposes revised pipeline: SFT establishes format, RLVR expands reachable trajectories, OPSD compacts them for cheaper inference. Models: Qwen3-8B, DeepSeek-R1-Distill-7B, AceReason-7B.

### 关键实验结果
| Condition | Accuracy Δ | Length Δ | Interpretation |
|-----------|-----------|---------|---------------|
| OPSD on correct rollouts | ~0 (preserved) | Significant shortening | Compression ✓ |
| OPSD on incorrect rollouts | Negative (damaged) | — | Correction ✗ |
| OPSD on all rollouts | Small/mixed | Moderate shortening | Compression dominates |
| Post-RLVR + Correct-only OPSD | Best position in accuracy-length plane | | Validated pipeline |

Benchmarks: MATH500, AIME24, AIME25 (average@8, temperature 0.6)

### BibTeX
```bibtex
@article{kim2026opsdcompresses,
  author    = {Jaehoon Kim and Dongha Lee},
  title     = {{OPSD Compresses What RLVR Teaches: A Post-RL Compaction Stage for Reasoning Models}},
  journal   = {arXiv preprint arXiv:2605.06188},
  year      = {2026},
  url       = {https://arxiv.org/abs/2605.06188},
}
```

### 综述分类
- 主章节: §7.1 Success Conditions + §7.2 Failure Modes (analysis paper)
- 相关章节: §5.3.1 Privileged Information (OPSD mechanism), §6.2 Curriculum (pipeline ordering), §8.4 When to Use On- vs Off-Policy
- 与现有方法关系:
  - **分析** OPSD/SDRL family: shows their gains in thinking-enabled math are NOT from correction
  - **递进** from OPSD (Zhao et al.): clarifies WHEN OPSD helps (compression) vs fails (correction)
  - **互补** with Stable-OPD length analysis: both address length, but different mechanism (Stable-OPD prevents inflation, this shows OPSD actively compresses)

### 综述集成建议
- 建议插入位置: §7.1 Success Conditions (as an analysis that refines understanding of WHEN OPSD works)
- 建议叙事角度: This paper provides the most precise characterization of OPSD's role in post-training: it is a compression tool, not a correction tool, for thinking-enabled reasoning. The SFT→RLVR→OPSD pipeline ordering follows logically: RLVR must first expand the model's correct trajectory space before OPSD can compress it. This connects to the broader §8.4 discussion of "when to use what" and strengthens the argument that on-policy methods serve different roles depending on pipeline position.

---

## Paper 4: VISD — Enhancing Video Reasoning via Structured Self-Distillation (arXiv:2605.06094)

### 核心创新 (1-2 句)
First structured self-distillation framework for VideoLLMs, using a video-aware judge to decompose reasoning quality into answer correctness, logical consistency, and spatio-temporal grounding. Introduces direction-magnitude decoupling: RL rewards set update direction, structured privileged info modulates token-level magnitudes.

### 方法概要 (150 字)
VISD augments on-policy training with two components: (1) A video-aware judge model J that evaluates rollouts along multiple structured dimensions (answer correctness, reasoning consistency, spatio-temporal grounding quality), producing feedback f = J(x, y, a*, e). (2) A direction-magnitude decoupling mechanism: rollout-level advantages from rewards determine the UPDATE DIRECTION (which trajectories to reinforce/penalize), while the structured teacher-student discrepancy (conditioned on judge feedback) modulates TOKEN-LEVEL UPDATE MAGNITUDES. This ensures RL stability while enabling fine-grained credit assignment aligned with specific reasoning error types. Additional components: curriculum scheduling (distillation→RL transition), EMA teacher stabilization for long video sequences.

### 关键实验结果
| Metric | Result | Context |
|--------|--------|---------|
| Convergence | ~2× faster | vs RLVR baselines (optimization steps) |
| Accuracy | Consistent improvement | Open-o3-Video benchmarks |
| Grounding quality | Improved | Spatio-temporal grounding metrics |

Base model: VideoLLM (specific model TBD from full paper)
Benchmarks: Open-o3-Video benchmarks, diverse video reasoning tasks

### BibTeX
```bibtex
@article{lin2026visd,
  author    = {Hao Lin and Kunyang Lv and Xu Jiang and Jingqi Tian and Zhongjing Du and Jiayu Ding and Qiaoman Zhang and Hongbo Jin},
  title     = {{VISD: Enhancing Video Reasoning via Structured Self-Distillation}},
  journal   = {arXiv preprint arXiv:2605.06094},
  year      = {2026},
  url       = {https://arxiv.org/abs/2605.06094},
}
```

### 综述分类
- 主章节: §5.3.1 Privileged Information (structured privileged info from judge)
- 相关章节: §8.2 Emerging Domains (VideoLLM application)
- 与现有方法关系:
  - **递进** from OPSD (generic privileged info): VISD structures the privileged context into diagnostically meaningful dimensions
  - **互补** with VOLD (VLM self-distillation): VOLD handles image VLMs with text-only teacher, VISD handles video with structured judge
  - **互补** with TT-OPD (turn-level OPD): both use EMA teacher + structured feedback, but different domains (medical agents vs video)
  - Direction-magnitude decoupling parallels Self-Distilled RLVR (Yang et al.) which also decouples direction from magnitude

### 综述集成建议
- 建议插入位置: §5.3.1 after OPSD discussion (structured privileged info), cross-ref in §8.2 Emerging Domains
- 建议叙事角度: VISD represents the natural evolution of privileged-information OPD from generic (OPSD: binary correctness) to structured (VISD: multi-dimensional judge feedback). The direction-magnitude decoupling is particularly interesting as a principled way to combine RL stability with OPD granularity, offering a template that could generalize beyond video to any domain where reasoning errors have identifiable subtypes.
