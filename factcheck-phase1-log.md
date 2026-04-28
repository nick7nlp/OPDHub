# Fact-Check Phase 1 Log (2026-04-19)

## BIB Updates
1. **CSD (2509.25837)**: arXiv → ICLR 2026 ✅
2. **ThinkTuning (rrv2025thinktuning)**: arXiv → EMNLP 2025 Main Conference ✅

## Citation Additions
3. L1161: Added `\citep{2501.12948}` to "The DeepSeek-R1 paper" mention ✅
4. L1169: Added `\citep{2501.12948}` to "DeepSeek-R1 off-policy distillation results" ✅
5. L1088: Added `\citep{2601.18734}` to "as demonstrated in OPSD" ✅
6. L1083: Added `\citep{2401.01335}` and `\citep{2601.18734}` to "SPIN or OPSD" mention ✅

## Factual Corrections
7. L1178 (DDT): Changed "proving that... necessary and sufficient" → "showing that... together bridge the SFT-RL generalization gap" (DDT paper does not use "necessary and sufficient") ✅
8. L1031, L1247 (PI Distillation): Changed "proving that the benefit of PI scales" → "showing that the benefit of PI grows" (softer claim) ✅
9. L1214 (Gemma 2): Changed "embeds online KD directly into continuous pre-training" → "embeds knowledge distillation directly into pre-training" (Gemma 2 doesn't specifically say "online") ✅
10. L1214 (Qwen3): Removed specific teacher model names ("Qwen3-32B or Qwen3-235B-A22B") not confirmed in abstract → "strong-to-weak distillation where larger models provide logit-level supervision" ✅

## Verified Claims (Sample)
- SRPO: +3.4% over GRPO, +6.3% over SDPO on Qwen3-8B ✅
- SSB: +10.6% on MATH-500 over GRPO ✅
- SCOPE: +5.5% (actually 5.54%) over standard OPD ✅
- OVD: +12.9% EM on web QA, +25.7% on math ✅
- Entropy-Aware OPD: +5.05 Pass@8 on Qwen3-4B-Base ✅
- ThinkTuning: +3.85% over zero-shot, +2.08% MATH-500, +2.23% AIME, +3.99% GPQA ✅
- KAT-Coder-V2: 79.6% SWE-bench ✅
- Nemotron-Cascade-2: Gold Medal IMO/IOI/ICPC, 20x fewer params ✅
- VOLD: SFT cold-start essential ✅
- Skill-SD: +14.0% AppWorld, +10.9% Sokoban ✅
- CORD: 80K synthetic samples ✅
- DAIL: <1000 solutions, 10-25% pass@k gains ✅
- DP-OPD: ε=2.0, better perplexity on Yelp/BigPatent ✅
- SPIN: MT-Bench 5.94→6.78 ✅
- Lion: 70k training examples ✅
- DeepSeek-R1 numbers (all AIME/MATH-500): Verified in 4/17 ✅
- DDT: on-policy data → RL advantage ✅
- \citet{2510.18874}: RL less forgetting than SFT ✅
- SDFT: on-policy learning from demonstrations ✅
- \citet{2512.23097}: unified KD+RL framework ✅
- AKL: convergence, head/tail analysis ✅
- \citet{2603.25562}: three failure modes ✅
- \citet{li2026rethinking}: 97-99% probability mass ✅
- MiMo-V2: Multi-Teacher On-Policy Distillation ✅
- G-OPD: OPD as KL-constrained RL ✅
- Qwen3: strong-to-weak distillation ✅
- Gemma 2: KD in pre-training ✅

## Formatting Checks
- Semicolons in prose: 0 ✅
- Em-dashes (---): 0 ✅
- Undefined citations: 0 ✅
- Undefined references: 0 ✅
- Uncited bib entries: 0 ✅
- Missing bib entries: 0 ✅
- All table citations appear in text: ✅
- PDF: 49 pages, 0 errors ✅

## Phase 3: Method Descriptions (Continued)

### Corrections Made
11. RLAD TRRD description: Changed "clips per-token probability ratio pθ/pteacher within PPO-style trust region" → "PPO-style likelihood-ratio objective anchored to teacher-old-policy mixture, yielding advantage-aware, trust-region-bounded distillation" (more accurate per paper) ✅
12. Speculative KD (3 locations): Changed "student's generations as speculative drafts that teacher verifies in parallel" → "student generates candidate tokens that are filtered against teacher's distribution, with rejected tokens re-sampled" (SKD is token-level accept/reject, not parallel verification) ✅
13. REOPOLD speedup: Precision fix 3.3× → 3.32× (matching abstract exactly) ✅
14. Qwen3 description: Removed specific teacher model names not confirmed in abstract → "strong-to-weak distillation where larger models provide logit-level supervision" ✅
15. Gemma 2: Changed "online KD directly into continuous pre-training" → "knowledge distillation directly into pre-training" (Gemma 2 doesn't specifically say "online") ✅
16. SDPO Table 1: Changed RL column from "--" to "✓" (paper title says "Reinforcement Learning via Self-Distillation") ✅
17. Added OPSD citation to L1088 (OPSD mention without cite) ✅
18. Added SPIN+OPSD citations to L1083 (method names without nearby cites) ✅

### Verified Claims (Phase 3 Additions)
- RLAD: TRRD mechanism (PPO-style likelihood-ratio, teacher-old-policy mixture) ✅
- SpecKD: token-level accept/reject mechanism (verified from HTML) ✅
- SDPO: "Self-Distillation Policy Optimization", converts binary reward to dense signal ✅
- SuperCorrect: hierarchical thought templates + cross-model DPO ✅
- SCoRe: teacher corrects only earliest error ✅
- KEPO: quality-gated on-policy distillation, exploration collapse ✅
- Veto: geometric bridge, Adaptive Gradient Veto, Decisiveness Knob ✅
- X-OPD: Cross-Modal OPD, speech-mode LLM distillation ✅
- CORD: 80K synthetic samples, online cross-modal self-distillation ✅
- VOLD: SFT cold-start essential ✅
- GATES: consensus-gated learning, document-grounded QA ✅
- OPCD: On-Policy Context Distillation, reverse KL ✅
- OEL: Online Experiential Learning, context distillation ✅
- MTP Self-Distill: multi-token prediction, 3× faster decoding ✅
- KDRL: joint KD+RL objective, prevents catastrophic forgetting ✅
- HDPO: cliff prompts, privileged self-distillation ✅
- TMS: Trajectory-Mixed Supervision, reward-free ✅
- X-KD: AVRIL-based KL, teacher environment reconstruction ✅
- AdaKD: adaptive token-level distillation focus ✅
- SelecTKD: propose-and-verify, token acceptance rate ✅
- SSD: simple self-distillation, Qwen3-30B 42.4%→55.3% LiveCodeBench ✅
- On-Policy SFT: SFT on self-generated correct+concise data ✅
- Skill-SD: +14.0% AppWorld, +10.9% Sokoban ✅
- GAD: minimax adversarial, discriminator as on-policy reward ✅
- KETCHUP: K-step return, Bellman Optimality Equation ✅
- CMDP (2509.22921): constrained RL problem, KL threshold ✅
- PromptKD: 0.0007% of teacher parameters, prompt tuning ✅
- PACED: Beta-kernel, minimax-robust, gradient SNR ✅
- Fast OPD: prefix truncation ✅
- SD-ZERO: 68.3% AIME 2024 (confirmed in paper HTML), GRPO 62.5% ✅
- RLSD: 200 steps surpasses GRPO at 400 steps ✅
- SPIN: MT-Bench 5.94→6.78 (confirmed in paper HTML), global optimum iff pθ=pdata ✅
- SRPO: +3.4% over GRPO, +6.3% over SDPO on Qwen3-8B ✅
- MiMo-V2: Multi-Teacher On-Policy Distillation (MOPD) ✅
- Qwen3: strong-to-weak distillation, off-policy and on-policy ✅
- \citet{2512.23097}: unified KD+RL framework ✅
- \citet{2510.18874}: RL less forgetting than SFT ✅
- SDFT: self-distillation as principled RL alternative ✅
- \citet{2603.25562}: three failure modes ✅
- \citet{li2026rethinking}: 97-99% probability mass, two conditions ✅
- DDT: Distribution Discriminant Theory, IDFT + Hinted Decoding ✅
- DASD: three critical limitations, 448K training samples ✅
- Lightning OPD: gradient discrepancy bounded by χ² divergence (confirmed) ✅
- Stable-OPD: length inflation, truncation collapse, repetition saturation ✅
- \citet{2603.24472}: epistemic verbalization, up to 40% drops ✅
- MiniPLM: Difference Sampling ✅
- DP-OPD: ε=2.0, synthesis-free, DP-SGD only on student ✅
- DSKD: Dual-Space KD, vocabulary-agnostic ✅
- Cross-tokenizer KD: ULD loss via optimal transport ✅
- Precision-Recall: precision-recall tradeoff in student ✅
- f-divergence perspective: adaptive teaching ATKD ✅
- "False Promise" (2305.15717): off-policy distillation limitations ✅
- DAgger (Ross 2011): O(T²)→O(T) error bound ✅
- Existing survey (2402.13116): LLM KD survey ✅
- Autonomous vehicle OPD (2604.07944): confirmed ✅

## Structural Checks
- Semicolons in prose: 0 ✅
- Em-dashes (---): 0 ✅
- Undefined citations: 0 ✅
- Undefined references: 0 ✅
- Uncited bib entries: 0 ✅
- Missing bib entries: 0 ✅
- All cross-references have labels ✅
- Table 2 years match bib entries ✅
- 97 bib entries, 97 cited keys: exact match ✅
- PDF: 50 pages, 0 errors, 0 warnings ✅

## Backup
- main.tex.bak-phase3-factcheck created

## Phase 4: Additional Quality Checks

### BIB Corrections (Phase 4)
19. PACED title: Added missing "On-Policy" → "PACED: Distillation and On-Policy Self-Distillation at the Frontier of Student Competence" ✅
20. OPSDC→CRISP: Paper renamed from "On-Policy Self-Distillation for Reasoning Compression" to "CRISP: Compressed Reasoning via Iterative Self-Policy Distillation". Updated bib title and all 5 text references. ✅
21. DistiLLM-2: @article → @inproceedings, journal → booktitle (ICML 2025 Spotlight) ✅
22. AlignDistil: @article → @inproceedings, journal → booktitle (ACL 2025) ✅
23. ToDi: @article → @inproceedings, journal → booktitle (EMNLP 2025 Oral) ✅

### Title Verification
- 40+ bib titles verified against arXiv citation_title metadata
- 1 mismatch found and fixed (PACED missing "On-Policy")
- 1 rename found and fixed (OPSDC → CRISP)

### Author Verification
- 16 first authors verified against arXiv metadata
- 0 mismatches found ✅

### Venue Verification
- 12 accepted venues verified against arXiv comments
- All matching bib entries ✅
- 3 venues newly updated to @inproceedings format

### Final Status
- PDF: 50 pages, 0 errors, 0 warnings ✅
- 97 bib entries = 97 cited keys (exact match) ✅
- All corrections compiled cleanly ✅
- Backup: main.tex.bak-phase3-factcheck ✅

## Phase 5: Deep Edge Cases & Final Verification

### Additional Verified Items
- HY-Embodied-0.5: "on-policy distillation to transfer large model to smaller" ✅
- VLA-OPD: robotic manipulation, Reverse-KL, sample efficiency over RL ✅
- Video-OPD: temporal video grounding, outperforms GRPO ✅
- Chinchilla (2203.15556): correct citation (Hoffmann et al., NeurIPS 2022) ✅
- Hinton 2015: standard reference ✅
- Ross 2011 DAgger: O(T²ε)→O(Tε) bound correct ✅
- f-DISTILL (2307.15190): unified f-divergence framework ✅
- 8 additional first authors verified ✅

### Section Assignment Check
- All 7 sampled methods confirmed in their correct sections ✅

### Math Verification
- 34 equation environments: 0 brace mismatches ✅
- DAgger bound derivation: mathematically correct ✅
- KD gradient derivation (Section 2.1): mathematically correct ✅

### Total Corrections Made: 23
| # | Type | Description |
|---|------|-------------|
| 1-2 | BIB venue | CSD→ICLR 2026, ThinkTuning→EMNLP 2025 |
| 3-4 | Missing cite | DeepSeek-R1 L1161, L1169 |
| 5-6 | Missing cite | OPSD L1088, SPIN+OPSD L1083 |
| 7 | Over-claim | DDT "proving"→"showing" |
| 8 | Over-claim | PI Distill "proving"→"showing" |
| 9 | Accuracy | Gemma 2 "online KD"→"KD" |
| 10 | Accuracy | Qwen3 removed unconfirmed teacher names |
| 11 | Accuracy | RLAD TRRD description corrected |
| 12 | Accuracy | SpecKD "parallel verification"→"accept/reject" (3 locations) |
| 13 | Precision | REOPOLD 3.3×→3.32× |
| 14 | Table fix | SDPO RL=✓ |
| 15-19 | Rename | OPSDC→CRISP (5 locations) |
| 20 | BIB title | PACED missing "On-Policy" |
| 21 | BIB title | CRISP new title |
| 22-24 | BIB format | DistiLLM-2/AlignDistil/ToDi @article→@inproceedings |

### Final Compilation
50 pages | 97 citations | 0 errors | 0 warnings | 0 undefined

## Phase 8: Round 3 Narrative Verification (2026-04-20)

### Medium-Confidence Claims Verified
- Gemma 2 (2408.00118): Confirmed KD is standard offline, NOT "online" → Fixed Table 3
- DistillSpec (2310.08461): "on-policy KD to improve draft model" ✅
- Distilling Step-by-Step (2305.02301): CoT distillation reference ✅
- PRM (2305.20050): "per-step verification of intermediate reasoning" ✅
- ORPO-Distill (2509.25100): "cross-architecture, Odds-Ratio, mixed-policy" ✅
- li2026rethinking (2604.13016): thinking-pattern consistency, genuine new knowledge, 97% token mass, trajectory depth degradation ✅
- DistiLLM-2 (2503.07067): "contrastive, increases teacher likelihood / decreases student" ✅
- DSKD (2504.11426): "dual-space, different output spaces" ✅
- LUFFY (2504.14945): "augments RLVR with off-policy traces, mixed-policy" ✅
- KETCHUP (2504.19024): "k-step return, Bellman, variance reduction" ✅
- SelecTKD (2510.24021): "selective token-weighted, 'where to apply learning'" ✅
- VOLD (2510.23497): "text-only teacher to VLM student, cold-start essential" ✅
- Veto (2601.07155): "geometric bridge in logit space, gradient veto" ✅
- DASD (2601.09088): "critically reexamines SFT on teacher traces" ✅
- RL vs SFT forgetting (2510.18874): "RL leads to less forgetting than SFT" ✅
- KEPO (2602.00400): "exploration collapse, learning cliff, KD+preference" ✅
- Precision-Recall (2505.13111): "distillation induces precision-recall tradeoff" ✅
- Fast OPD (2602.15260): "training signals concentrated in prefix" ✅
- DistiLLM (2402.03898): "skew KL, adaptive off-policy" ✅
- Scaling laws for KD (2502.08606): "compute-optimal allocation for teacher and student" ✅
- HDPO (2603.23871): "cliff prompts, RL gradient vanishes, privileged self-distillation" ✅
- Sampled-token OPD fragility (2603.25562): "biased relative to sequence-level RKL, tighter variance bound" ✅

### Gray Area Resolution
- False Promise (2305.15717): Corrected L102 from "degrade sharply on multi-step generation" to accurate "mimic style without factual capabilities, gains confined to imitation data". Added Ross 2011 to L1319 as primary compounding-error reference.

### Factual Corrections Made (Round 3 Verification)
| # | Type | Description |
|---|------|-------------|
| 24 | Table accuracy | Gemma 2 Table 3: "Online KD in pre-training" → "KD in pre-training" (paper doesn't say "online") |
| 25 | Citation accuracy | False Promise (2305.15717): corrected description to match actual paper findings (imitation gap, not exposure bias) |
| 26 | Citation accuracy | L1319: Added Ross 2011 as primary theoretical reference for compounding errors |
| 27 | Factual precision | OPSD: "order of magnitude fewer tokens" → "single rollout vs GRPO's eight"; "underperforms" → "gains minimal" at 1.7B |

### Round 3 Narrative Over-Inference Check
Checked all 12 Round 3 modification points from round3-changelog.md:

1. §1 Intro roadmap: "each addresses a failure mode that emerges after the preceding challenge is resolved" — ✅ Accurate structural description
2. §5 intro: "fundamental tension" (saturation-resistant ↔ external-signal dependent) — ✅ Reasonable analytical synthesis
3. §5.1 OPSD cliff-prompt ↔ PACED SNR: — ✅ Verified both papers, parallel is accurate
4. §5.1 GATES ↔ SCOPE functional role: — ✅ Both attenuate unreliable supervision
5. §5.1 CRISP ↔ self-play saturation: — ✅ PI provides structurally different reference policy
6. §5.2 SSD closing (bounded by pre-training distribution): — ✅ Logical inference, properly hedged
7. §5.3 External Feedback closing (coupling arc): — ✅ Accurate progression description
8. §6 intro "cumulative argument": — ✅ Meta-organizational claim, reasonable
9. §6.1 closing "exploitable gap": — ✅ Supported by li2026rethinking's two conditions
10. §6.3 information geometry paragraph: — ✅ Uses "admits a natural interpretation" / "Under this view" — properly hedged as survey interpretation
11. §6.3 closing (OPD/RL/PO spectrum): — ✅ Supported by G-OPD equivalence and unified KD+RL framework
12. §8 Open Problems connective tissue: — ✅ All transitions are logical implications, not factual claims

**Verdict: No over-inferences found in Round 3 narrative. All analytical claims are either directly supported by cited papers or properly hedged as survey-level interpretation.**

### DeepSeek-R1 "Why Off-Policy Works" Analysis
Three reasons provided (data quality, self-correcting traces, memorization vs exploration) — all are survey-original analysis, properly framed as explanatory hypotheses rather than cited findings. ✅ Acceptable for a survey.

### Final Status
- 50 pages | 97 citations | 0 errors | 0 warnings (content) | 0 undefined
- Total corrections: 27 (23 from Phase 1-5 + 4 from Phase 8)
- Backup: main.tex.bak-round3-narrative-check
