# Round 25 — READ §6 Training Dynamics and Efficiency

**Mode**: READ  
**Section**: §6 Training Dynamics and Efficiency (lines 919–1000)  
**Agent**: cron tick 25  

## Overall Assessment

§6 是当前 survey 写得最好的 section 之一。叙事结构清晰（token weighting → sample weighting → curriculum → compute），方法间有对比和 spectrum 分析（TIP/SCOPE/SelecTKD/AdaSwitch 的 fine-to-coarse 对比），跨 section 连接做得好（back-ref §2, forward-ref §7）。但还有几处需要改进。

## Issues Found

### 1. ⚠️ Fast OPD framing 不准确 (line ~982)

**Current**: "Fast OPD observes that exposure bias is concentrated in the early tokens of a sequence, where errors compound most severely."

**Problem**: 原文 (2602.15260) 的 argument 不是 "exposure bias concentrated in early tokens"。原文说的是 "training signals are often concentrated in the prefix"——意思是 prefix 部分已经包含了大部分有用的 distillation signal，所以可以 truncate 后半部分。这是一个 efficiency observation，不是 error-compounding observation。

**Fix**: Reframe as "Fast OPD observes that the useful distillation signal is concentrated in the prefix of student-generated sequences" + explain that truncating avoids the diminishing-return tail.

### 2. ⚠️ PACED 的 "gradient magnitude scales as p(1-p)" 过度简化 (line ~956-960)

**Current**: "the expected gradient magnitude scales as p(1-p), which is maximized at p=0.5 and vanishes at both extremes"

**Problem**: PACED paper 证明的是 SNR vanishes at p→0 and p→1 boundaries (Proposition 2)，leading-order weight family 是 `w(p) = p^α(1-p)^β` (general Beta kernel)。survey 简化为 p(1-p) (α=β=1) 容易误导读者以为 optimal weight 是对称的。实际上 paper 强调 α≠β 的 asymmetric cases（如 α=1,β=2 emphasis on avoiding hard prompts）。

**Fix**: Keep the intuition that SNR vanishes at both extremes, but qualify that the optimal kernel is `p^α(1-p)^β` with task-dependent (α,β), not simply p(1-p). The simplest instantiation α=β=1 gives p(1-p) but the paper shows asymmetric settings work better.

### 3. ⚠️ AdaSwitch description 略有失真 (line ~944)

**Current**: "maintains a running estimate of the student's cumulative prefix quality"

**Problem**: 实际机制是 sliding window of recent token-level divergences (KL/JSD between student and teacher logits)，threshold = K × d̄_window。不是 "cumulative prefix quality" 而是 "recent divergence history"。

**Fix**: Replace with "maintains a sliding window of recent token-level divergences and switches when divergence exceeds a context-adaptive threshold (K × average recent divergence)"

### 4. ⚠️ "Retaining by Doing" attribution scope (line ~974)

**Current**: framing suggests the paper is specifically about OPD's rehearsal benefit.

**Problem**: Paper 2510.18874 is about RL vs SFT forgetting broadly — it shows that the on-policy nature of RL (not OPD specifically) provides implicit rehearsal. The finding applies to any on-policy method (RLHF, GRPO, OPD) not just distillation.

**Fix**: Clarify that the insight is about on-policy training generally (RL/OPD/etc.), and the survey is extending this finding to the OPD context.

### 5. 🟡 Concrete cost example lacks citation (line ~993-999)

**Current**: "Off-policy over 1B tokens... ~300 GPU-hours. On-policy... ~1,200-1,500 GPU-hours, a 4-5× overhead."

**Problem**: 这些数字没有 citation。Lightning OPD paper 给了 4× 的 ratio（30 vs 120 GPU-hours for their setup），但绝对数字 (300/1200-1500) 像是 back-of-envelope estimates。Survey readers 可能 mistake these for measured values.

**Fix**: Either (a) cite Lightning OPD's 4× figure with their specific setup, or (b) explicitly mark as "back-of-envelope estimates" or "representative estimates."

### 6. 🟡 Uni-OPD "5 domains, 16 benchmarks" unverified

**Current**: "This dual-perspective framework generalizes across LLMs and MLLMs (5 domains, 16 benchmarks)"

**Problem**: 没有 PDF 可验证。arXiv abstract 只说 "generalizes across LLMs and MLLMs" 但没明确 mention "5 domains, 16 benchmarks"。可能来自 paper body 但无法确认。

**Status**: ❓ Need PDF to verify. Flag for next VERIFY round.

### 7. 🟡 Missing synthesis opportunity — curriculum methods' relationship to RL exploration

The section discusses PACED, TCOD, Uni-OPD as curriculum methods but doesn't explicitly connect them to the RL literature on curiosity-driven exploration or intrinsic motivation. The SNR analysis essentially reinvents "learning progress" curriculum (Oudeyer et al. 2007). This connection would strengthen the survey's depth.

### 8. 🟡 Semantic Bootstrapping placement awkward

Mitra 2025 (Semantic Soft Bootstrapping) is listed under §6.2 Curriculum but its mechanism (in-context exemplars → self-refinement) is quite different from the other curriculum methods (which select/weight training prompts). It's more of a data augmentation or in-context learning technique. Consider whether it belongs here or in §5 (Signal Source).

### 9. ✅ Verified claims (no issues)

| Claim | Verdict |
|-------|---------|
| TIP Soft-OR, 50% retention, 3 families 2×-9× | ✅ Accurate |
| SCOPE +5.5% over standard OPD | ✅ Accurate (paper: +5.54%) |
| SelecTKD Top-k/Spec-k, TAR | ✅ Accurate |
| TCOD +18 points over vanilla multi-turn OPD | ✅ Accurate (paper: +18.74 in one setting) |
| Semantic Bootstrapping +10.6% MATH-500 over GRPO | ✅ Accurate |
| Lightning OPD 4× lower cost | ✅ Accurate (paper: 4.0× speedup) |
| Qwen3 two-phase off→on-policy distillation | ✅ Accurate |
| li2026rethinking "thinking-pattern mismatch" + off-policy cold start | ✅ Accurate |
| 2603.25562 three failure modes | ✅ Accurate |
| GPU memory math (70B→140GB BF16, 7B→84GB with optimizer) | ✅ Correct arithmetic |
| Speculative KD mechanism | ✅ Accurate |

### 10. 🟡 Prose style notes

- Line 921: "non-stationary data distributions (the student's policy shifts during training, making older rollouts stale)" — parenthetical is too long, breaks reading flow
- Line 956-961 (PACED SNR paragraph): The paragraph explaining WHY on-policy beats off-policy is excellent synthesis — rare instance of survey explaining "why" rather than "what" 👍
- Line 982-986 (Fast OPD + Lightning OPD synthesis paragraph): The "fidelity-efficiency frontier" framing is good survey writing
- The DistillSpec equation (E[S] formula) — verify the formula matches the paper in next VERIFY round

## Priority for next rounds (VERIFY/DEEPEN)

1. **HIGH**: Fix Fast OPD framing (factual inaccuracy in characterization)
2. **HIGH**: Fix PACED p(1-p) oversimplification  
3. **MEDIUM**: Fix AdaSwitch "cumulative prefix quality" → "sliding window divergence"
4. **MEDIUM**: Add citation or caveat to concrete cost example
5. **LOW**: Consider Semantic Bootstrapping placement
6. **LOW**: Add RL exploration connection for depth
