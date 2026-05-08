# Bundle B Fact-Check: §5 White/Black-box Teacher + §6 Training Dynamics + §7 Failure Modes

**Date**: 2026-05-08  
**Scope**: Claims 1–12 from Bundle B assignment  
**Method**: `pdftotext` + `grep` against source PDFs; web fallback for missing papers  

---

## 1. Veto (2601.07155) — L798

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "Adaptive Gradient Veto (suppressing pathological gradients on low-confidence tokens)" | ✅ | Paper abstract: "Adaptive Gradient Veto that stabilizes optimization by suppressing harmful gradients on low-confidence tokens" |
| "Decisiveness Knob (balancing performance with diversity)" | ✅ | Paper abstract: "Decisiveness Knob to balance reward-driven performance with output diversity" |
| Parameter β serves dual role (gradient veto + decisiveness knob) | ✅ | Paper: "a single scalar parameter β plays a dual role: it acts as an Adaptive Gradient Veto... and as a Decisiveness Knob" |

**Overall**: ✅ All claims accurate.

---

## 2. PromptKD (2402.12842) — L798

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "prepending learnable prompt tokens (adding only 0.0007% of the teacher's parameters)" | ✅ | Paper describes prompt tokens appended to teacher; 0.0007% confirmed in paper |

**Overall**: ✅ Accurate.

---

## 3. TIP (xu2026tip / 2604.14084) — L923

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "Token Importance Profiling" | ✅ | Paper title: "Token Importance Profiling for Efficient On-Policy Knowledge Distillation" |
| "organizing importance along two axes, student entropy $h_t$ and teacher-student divergence $\delta_t$" | ✅ | Paper §3.1: two-axis taxonomy using student entropy and teacher-student divergence |
| "Soft-OR score $s_t = \hat{h}_t + \hat{\delta}_t - \hat{h}_t \cdot \hat{\delta}_t$" | ✅ | Paper Eq. 3: exact formula matches |
| "consistent improvements at 50% token retention across three model families with capacity gaps from 2× to 9×" | ✅ | Paper experiments: Qwen3-8B→4B (2×), Llama-70B→8B (~9×), Qwen2.5-14B→1.5B (~9×) |
| "Q3 tokens are structurally invisible to any entropy-only weighting scheme" | ✅ | Paper Proposition 2: proves any non-decreasing function of entropy with f(0)=0 cannot distinguish Q3 from Q4 |

**Overall**: ✅ All claims accurate.

---

## 4. SCOPE (zheng2026scope / 2604.10688) — L925

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "dual-path architecture routes rollouts by correctness" | ✅ | Paper: dual-path framework separating correct and incorrect trajectories |
| "Incorrect trajectories receive teacher-perplexity-weighted KL distillation" | ✅ | Paper: incorrect rollouts → KL distillation weighted by teacher perplexity |
| "correct trajectories receive student-perplexity-weighted MLE" | ✅ | Paper: correct rollouts → MLE weighted by student perplexity |
| "yielding +5.5% over standard OPD" | ✅ | Paper reports +5.54%; survey rounds to +5.5% |
| "Pass@1 improves at the expense of Pass@$k$" (diversity collapse) | ✅ | Paper: Pass@32 degrades from 93.7% to 84.9% while Pass@1 improves |

**Overall**: ✅ All claims accurate.

---

## 5. TCOD (chen2026tcod / 2604.24005) — L954, L1099

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "Trajectory-Level KL Instability" | ✅ | Paper identifies this phenomenon: inter-turn error compounding causes KL instability |
| "F2B/B2F" two scheduling variants | ✅ | Paper: F2B = Forward-to-Backward (early turns first); B2F = Backward-to-Forward (end turns first) |
| "On ALFWorld, WebShop, and ScienceWorld, TCOD achieves gains of up to +18 points over vanilla multi-turn OPD" | ✅ | Paper: +18.67 on ScienceWorld; three benchmarks confirmed |
| "the F2B variant showing particular strength on tasks where early-turn errors are most consequential" | ✅ | Paper discusses F2B advantage on tasks where early errors cascade |

**Overall**: ✅ All claims accurate.

---

## 6. Semantic Soft Bootstrapping (mitra2025semantic / 2512.05105) — L960

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "provides the model with both correct and incorrect rollouts as in-context exemplars" | ✅ | Paper: uses correct solution and most common incorrect rollout as in-context exemplars for self-distillation |
| "+10.6% on MATH-500 over GRPO" | ✅ | Paper reports +10.6% on MATH-500 (Qwen2.5-3B-Instruct) |

**Overall**: ✅ All claims accurate.

---

## 7. Lightning OPD (wu2026lightning / 2604.13010) — L979, L415, L550

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "decouples student optimization from teacher inference entirely by precomputing teacher distributions into an offline memory bank" | ✅ | Paper: "precomputing teacher log-probabilities once over SFT rollouts... eliminating the need for a live teacher server entirely" (survey's "offline memory bank" is a reasonable paraphrase) |
| "offline distillation under teacher consistency can match online OPD at 4× lower cost" | ✅ | Paper: "achieves a 4.0× speedup" at 8B scale (3.6× at 4B); "achieves performance on par with standard OPD" |
| Table row: "$4\times$ cost reduction" | ✅ | Paper Table 2: 4.0× speedup at 8B scale confirmed |

**Overall**: ✅ All claims accurate.

---

## 8. luo2026demystifying / Stable-OPD (2604.08527) — L1045

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "identify the root cause as an asymmetry in the KL gradient, where positive KL gradients (pushing toward teacher-preferred tokens) are stronger than negative ones" | ⚠️ **Imprecise paraphrase** | Paper's actual explanation: "repetitive tokens receive systematically larger reverse-KL advantages than regular tokens." The paper does NOT frame this as "positive vs negative KL gradient asymmetry" or "teacher-preferred vs dispreferred tokens." It's about repetitive vs regular tokens receiving different advantage magnitudes. The survey's framing introduces a conceptual distortion. |
| "achieve +7.2% over vanilla OPD by breaking the self-amplification cycle" | ✅ | Paper: "improves performance by 7.2% on average compared to standard OPD baselines" |
| "reference divergence term anchoring the student's length distribution" | ⚠️ **Partially inaccurate** | Paper: uses KL(π_θ ∥ π_ref) as a general policy regularizer that "limits uncontrolled policy drift." It anchors the overall policy, not specifically the "length distribution." The length stabilization is a consequence, not the stated target. |
| "rollout mixing that blends on-policy student generations with off-policy teacher generations in a decaying ratio" | ⚠️ **Two errors** | (1) Paper blends with "off-policy golden data" (ground-truth demonstrations from DeepSeek-R1), NOT "teacher generations." Paper explicitly distinguishes: "golden responses are typically used to refine the teacher signal itself... By contrast, mixture distillation leaves the original teacher-derived OPD signal unchanged." (2) No "decaying ratio" — λ_gold is a fixed hyperparameter throughout training. |

**Overall**: ⚠️ The +7.2% number is correct, but the mechanistic description contains multiple inaccuracies. The survey reframes the paper's findings in a way that doesn't match the source material.

### Detailed Discrepancy Analysis:
- **Root cause**: Paper says repetitive tokens get larger advantages → self-reinforcing loop. Survey says positive/negative gradient asymmetry → not what the paper claims.
- **Reference term**: Paper = general KL regularizer on policy. Survey = "anchoring length distribution" (narrower/misleading).
- **Rollout mixing**: Paper = fixed-ratio blend with golden/reference data. Survey = "decaying ratio" with "teacher generations" (both wrong).

---

## 9. TT-OPD (ttopd2026 / 2605.02943) — L1034, L1126

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "diagnoses three such pathologies on Healthcare AI Gym" | ✅ | Paper identifies three pathologies: Response Explosion, Multi-turn Collapse, Distillation Instability |
| "KL collapse (divergence drops from 2.637 to 0.343 at every copy event)" | ✅ | Paper: "at step 10 in the T=30 variant, KL drops from 2.637 to 0.343" |
| "turns drop from 7.82 to 5.52 per episode" | ⚠️ **Conflation of two variants** | Paper: periodic reset causes turns to drop from **7.65** to 5.52. The number 7.82 is the starting value for a DIFFERENT variant (EMA, no conditioning), which drops to 6.23. Survey incorrectly mixes the start value from one ablation (7.82) with the end value from another (5.52). |
| "accuracy collapses from 54.5% to 49.0%" | ✅ | Paper: "initial accuracy plateau at 54.5%... eventually collapses accuracy to 49.0%" (EMA + outcome hints, no length control variant) |
| "TT-OPD reaches the best score on 10 of 18 benchmarks" | ✅ | Paper abstract & conclusion: "best performance on 10 of 18 benchmarks" (Note: key findings section says "12 of 18" but abstract/conclusion say "10 of 18"; survey follows abstract) |
| "average +3.9 percentage-point improvement" | ✅ | Paper: "+3.9 pp improvement over the non-RL baseline" |
| Healthcare AI Gym: "10 clinical domains, 3.6K+ tasks, 135 domain-specific tools, and 828K medical passages" | ✅ | Paper abstract: "10 clinical domains with 3.6K+ tasks, 135 domain-specific tools, and a knowledge base of 828K medical passages" — exact match |

**Overall**: ⚠️ One numerical conflation (7.82→5.52 should be 7.65→5.52 for periodic reset, or 7.82→6.23 for EMA). All other claims are accurate.

---

## 10. PBSD (pbsd2026 / 2605.05040) — §5.3.1, §4.3

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "reward-regularized optimum $\pi^* \propto \pi_{\text{teach}} \exp(r/\beta)$" | ✅ | Paper: "analytic optimum is a reward-reweighted version of the teacher distribution" |
| "provably dominates the teacher itself whenever the reward is informative" | ✅ | Paper: "yielding a target policy provably superior to the original teacher under this objective" |
| "DPO-style pairwise loss where preferred y+ from context-augmented teacher and dispreferred y- from current student" | ✅ | Paper Algorithm: teacher → y+, student → y-, optimizes pairwise logistic loss |
| "On Qwen3-1.7B/4B/8B" model scales | ✅ | Paper §4: experiments on Qwen3-1.7B, Qwen3-4B, Qwen3-8B |
| "matches OPSD's token efficiency and surpasses its peak accuracy" | ✅ | Paper Figure 2B: token-efficient; Table 2: strongest average at all scales |
| "without the post-peak decline documented in Figure 2" | ✅ | Paper Figure 2A: "OPSD peaks early and then degrades" while "PBSD remains stable throughout training" |

**Overall**: ✅ All claims accurate.

---

## 11. Epistemic Suppression (2603.24472) — L1034, L907, L1026

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "trace self-distillation degradation in mathematical reasoning to the suppression of epistemic verbalization" | ✅ | Paper abstract: "We trace this degradation to the suppression of epistemic verbalization—the model's expression of uncertainty during reasoning" |
| "the model's expression of uncertainty during reasoning" (definition) | ✅ | Exact match with paper |
| "When self-distillation shortens reasoning traces, it disproportionately removes hedging phrases and uncertainty markers" | ✅ | Paper: conditioning on rich information "suppresses uncertainty expression"; "removes hedging phrases" consistent with content |
| "performance drops of up to 40%" | ✅ | Paper: "we observe performance drops of up to 40%" (specifically ~40% on AIME24 for DeepSeek-R1-Distill-Qwen-7B with SDPO c=s) |
| L1034: epistemic suppression as "multi-turn extension" of the same phenomenon | ✅ | Reasonable survey interpretation linking single-turn epistemic suppression to multi-turn reward-hint runaway |

**Overall**: ✅ All claims accurate.

---

## 12. §6.3 Concrete Cost Example — L991

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "70B teacher, 7B student on 8×H100 GPUs" | ✅ (reasonable setup) | Standard configuration for large-scale distillation |
| "70B teacher weights ~140GB in BF16" | ✅ | 70×10⁹ × 2 bytes = 140×10⁹ bytes = 140 GB |
| "7B weights and optimizer states ~84GB" | ✅ | Adam FP32: master weights + momentum + variance = 3 × 4 bytes × 7×10⁹ = 84 GB (standard "12 bytes/param" calculation) |
| "Off-policy over 1B tokens: teacher generates (~200 GPU-hours), student trains (~100 GPU-hours), totaling ~300" | ✅ (reasonable) | 70B model at ~200 tokens/sec/GPU on H100 → 1B tokens / (200×8) ≈ 625K sec ≈ 174 GPU-hours for generation. ~200 is a reasonable estimate. Student training at ~10K tokens/sec/GPU → ~100 GPU-hours. |
| "On-policy over 1B tokens... ~1,200–1,500 GPU-hours, a 4–5× overhead" | ✅ (consistent) | 4–5× overhead over 300 = 1,200–1,500. Reasonable given that each step needs student generation + teacher scoring + backward pass. |

**Overall**: ✅ All numbers are reasonable estimates. The 84GB calculation follows standard Adam mixed-precision conventions (12 bytes/parameter for FP32 optimizer states). The GPU-hour estimates are order-of-magnitude correct.

---

## Summary

| # | Paper | Verdict | Issues |
|---|-------|---------|--------|
| 1 | Veto (2601.07155) | ✅ | None |
| 2 | PromptKD (2402.12842) | ✅ | None |
| 3 | TIP (2604.14084) | ✅ | None |
| 4 | SCOPE (2604.10688) | ✅ | None |
| 5 | TCOD (2604.24005) | ✅ | None |
| 6 | SSB (2512.05105) | ✅ | None |
| 7 | Lightning OPD (2604.13010) | ✅ | None |
| 8 | Stable-OPD (2604.08527) | ⚠️ | Root cause misdescribed; "decaying ratio" unsupported; "teacher generations" should be "golden/reference data"; "length distribution" is too narrow |
| 9 | TT-OPD (2605.02943) | ⚠️ | "7.82 to 5.52" conflates numbers from two different ablation variants (should be 7.65→5.52 for periodic reset) |
| 10 | PBSD (2605.05040) | ✅ | None |
| 11 | Epistemic Suppression (2603.24472) | ✅ | None |
| 12 | §6.3 Cost Example | ✅ | Reasonable estimates |

### Severity Assessment

**Critical errors requiring correction**: None (no ❌ verdicts)

**Notable inaccuracies (⚠️) requiring attention**:
1. **Stable-OPD (L1045)**: Three distinct mischaracterizations in one paragraph. The mechanistic explanation diverges from the paper. Recommend rewriting to: "identify the root cause as a self-reinforcing feedback loop in which repetitive tokens receive systematically larger reverse-KL advantages, and once frequent enough, their disproportionate gradient contribution dominates updates, driving length inflation. Stable-OPD combines a reference-based KL regularizer with rollout mixture distillation (blending on-policy student generations with off-policy golden trajectories at a fixed ratio)."
2. **TT-OPD (L1034)**: Change "7.82 to 5.52" to "7.65 to 5.52" (periodic reset variant) or clarify that these are from different ablation conditions.
