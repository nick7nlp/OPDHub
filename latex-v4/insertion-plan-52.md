# Insertion Plan: 52 OPD Method Papers → main.tex (v4)

Status: drafted 2026-06-06 from `paper_notes.json` + Awesome README §-tags.
Total 52 papers + 4 background surveys (separate decision).

## Section assignment

### §4.1 Fixed Divergence Objectives (5)
- `2603.01683` Surgical Post-Training (proximal OPD; reasoning + retention)
- `2606.00305` Bridging Reasoning Trajectories (OT-based near-future guidance)
- `2606.00564` Decomposed VLM-OPD (gradient steering, language vs visual subspace)
- `2606.01039` OPD+ (advantage redesign via f-divergence gradient analysis)
- `2606.05152` Distributional DAgger (forward CE + future-aware credit)

### §4.2 Adaptive Divergence Objectives (6)
- `2605.21606` Position-Weighted OPSD (token position reliability)
- `2605.22263` Direction-Adaptive Self-Distillation (entropy-routed teacher polarity)
- `2605.26844` Token Teachability (selective weighting by learnability metric)
- `2605.30833` Lookahead Group Reward (Supervision Fidelity Decay)
- `2606.00147` RAFT (data refinement + adaptive distillation, alleviated forgetting)
- `2606.01249` Trust-Region OPD (outlier estimation + off-policy guidance)

### §4.3 RL-Augmented Objectives (4)
- `2605.18529` AMR-SD (asymmetric meta-reflective; token credit assignment in RLVR)
- `2605.21851` OPPO (Bayesian value recursion; oracle-conditioned likelihood ratio)
- `2605.27140` StepOPSD (step-aware online preference for multi-turn agent RL)
- `2606.05122` Self-Evaluation (cyclic RL + masked judge distillation)

### §5.1 White-Box Logit Supervision (2)
- `2605.27255` Pair-In Pair-Out (latent MTP + OPD as confidence head)
- `2606.04694` DuDi (dual-signal multilingual SLM)

### §5.2 Black-Box / API-Constrained (2)
- `2509.25100` ORPO-Distill (cross-architecture preference, mixed-policy negatives)
- `2606.01476` OmniOPD (logit-free chunk-level Monte Carlo verification)

### §5.3.1 Privileged Information (6)
- `2605.20643` AVSD (multi-view consensus + view-specific residual)
- `2605.28791` Skill-Conditioned Gated SD (outcome-validated teacher polarity)
- `2606.00424` Weak Critics → Strong Learners (critique distillation, scalable oversight)
- `2606.03089` Constitutional Cross-SFT (safety vs expressiveness, two-stage)
- `2606.03603` World-Model PI (privileged future videos for MLLM verification)
- `2606.04036` Self-Distilled Policy Gradient (full-vocab on-policy SD + RLVR)

### §5.3.2 Pure Self-Distillation (12)
- `2605.11019` Variational Posterior Guidance (efficiency-aware reasoning)
- `2605.17497` Self-Supervised OPD (intra-group correct-vs-wrong contrast)
- `2605.17873` HINT-SD (targeted hindsight; long-horizon agents)
- `2605.18299` SD-Search (hindsight self-distill for search query supervision)
- `2605.18740` Vision-OPD (regional-to-global; fine-grained MLLM)
- `2605.20258` It Takes Two (complementary SD; contextual integrity)
- `2605.22240` TOD-Proactivity (asymmetric SD from privileged user concerns)
- `2605.22511` Search-E1 (GRPO + offline SD self-evolution loop)
- `2605.27186` MAIGO (multi-turn lost-in-conversation; history-cleaned)
- `2605.28014` ROSD (reflective + quote-localized SD)
- `2605.30251` Canonical-Context OPD (raw-sharded vs full-context teacher)
- `2606.02372` COMAP (co-evolving textual world model + agent)

### §5.3.3 External Feedback (1)
- `2605.21834` On-Policy Consistency Training (safety; frozen-copy teacher)

### §6.1 Token and Sample Weighting (3)
- `2605.21924` Visual-Advantage OPD (token-level visual advantage reweighting)
- `2606.02684` Filter-Then-Reweight (trajectory filter + soft token reweight)
- `2605.27028` Less-is-More Early Stop (off-policy teacher decay → token horizon cut)

### §6.2 Curriculum and Difficulty Adaptation (5)
- `2605.15532` DeltaPrompts (zero-delta trap; high-divergence prompt synthesis)
- `2605.17862` f-OPD (freshness-aware control; async stability)
- `2605.31159` Trust-Region Behavior Blending (warmup curriculum)
- `2606.03532` When Should the Teacher Move (adaptive teacher-refresh gating)
- `2606.04703` Continual Experience Internalization (multi-iter agent stability)

### §6.3 Compute Optimization (2)
- `2605.31490` POPD/TOPD (rollout truncation efficiency)
- `2606.02530` SafeSteer (localized OPD via activation steering)

### §7.2 Failure Modes (3)
- `2605.19433` MOTAB (dual exposure biases; backtracking)
- `2605.27115` Counteraction-Aware MOPD (general-capability loss in domain spec.)
- `2606.03620` Physics-Guided SD (MI-signal step-size; gradient stability)

### §8.1 Industrial Deployment (1)
- `2605.15239` Safety-Tax-OPD (per-token KL from privileged-context teacher)

## Total
5+6+4+2+2+6+12+1+3+5+2+3+1 = **52** ✓

## 4 background surveys (deferred, possibly §2.1 / §1 / §5.3 / §1)
- `2006.05525` KD Survey (Gou) — §2.1 classical KD background
- `2312.11562` Reasoning with FMs — §1 intro context
- `2404.14387` Self-Evolution Survey — §5.3 self-distillation context
- `2405.07863` RLHF Workflow — §1 / §4.3 context

## Writing strategy
1. Every paper: ≤ 3 sentences. Insert via topic cluster (avoid linear append).
2. Lead a paragraph with a thesis (the OPD design problem this cluster addresses), then introduce 2-4 papers as contrast/escalation/complement, end with takeaway or bridge.
3. Forbidden: AI-taste vocab, prose colon, em-dash, sentence-start However/Moreover, novel/significantly/leverages, parallel "Method A does X. Method B does Y."
4. Numeric claims (% improvements, sizes) only when verified from PDF / paper_notes.
