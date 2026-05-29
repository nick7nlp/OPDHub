# Round 01 seed — §1 Introduction deep-read (manual, by main)

**Pre-seeded by main before first cron tick.** This saves the first tick from READ-mode redundancy.
The next tick should jump to VERIFY mode on these findings, OR if the assigned mode is already different, it still has this as reference.

## Source
`latex-v2/main.tex` L82–L108 (§1 Introduction, 27 lines = 9 paragraphs)

## Paragraph-by-paragraph analysis

### ¶1 (L84) — Opening hook: DeepSeek-R1 as load-bearing example
- **Claims**: "near-human competence in reasoning, code generation, and multilingual instruction following" cites Qwen3~\citep{2505.09388}, DeepSeek-R1~\citep{2501.12948}, Gemma~\citep{2408.00118}
  - ⚠️ "near-human competence" is strong — papers actually show narrower benchmark wins (AIME, HumanEval, MMLU). Soften to "near-human on specific benchmarks" or "state-of-the-art across benchmarks"?
- **Claims**: "DeepSeek-R1, whose 671B mixture-of-experts teacher was successfully distilled into dense students spanning 1.5B to 70B parameters"
  - ✅ verified in DeepSeek-R1 paper Table 5 / Section 2.4
- **Issue**: sentence 2 is 60+ words with embedded clauses — could split
- **Insight to add**: Hinton KD was designed for compression (small → smaller), whereas DeepSeek-R1 uses it for **capability transfer** (huge → small but capable) — this re-purposing is worth calling out explicitly

### ¶2 (L86) — Off-policy fragility + exposure bias
- **Claim**: "autoregressive generation amplifies it quadratically in sequence length, producing an expected discrepancy of $O(\epsilon T^2)$ over a horizon $T$"
  - Attributed via \citet{ross2011reduction} (DAgger)
  - ✅ DAgger theorem: O(εT²) under behavior cloning → O(εT) under DAgger correction
- **Claim**: "\citet{2305.15717} already warned the community that off-policy imitation of proprietary LLMs often yields students that reproduce surface style without acquiring the underlying reasoning competence"
  - ✅ "The False Promise of Imitating Proprietary LLMs" (Gudibande et al. 2023)
- **Insight strength**: the "textbook exposure bias + quadratic amplification" framing is solid; already shows WHY not just WHAT ✓

### ¶3 (L88) — OPD definition via sampling-distribution shift
- **Claim**: "the theoretical payoff mirrors the classical DAgger result, where querying an expert on the learner's own visited states reduces the $O(\epsilon T^2)$ compounding of off-policy imitation to $O(\epsilon T)$"
  - ✅ this is the canonical DAgger reduction
- **Citation structure**: white-box/black-box/teacher-free trichotomy with 3 cites each — good pedagogy
- **Minor**: "drifts into the very states it would visit at deployment" — "drifts" is weak. Could strengthen to "exposes itself to" or "populates"

### ¶4 (L90) — Design-choice narrative
- Well-structured: GKD → KL-constrained RL → SPIN/OPSD → industrial adoption (Qwen3, DeepSeek-V4, Gemma 2, MiMo-V2)
- **Claim**: "DeepSeek-V4 in particular replacing its mixed RL stage with pure multi-teacher OPD for model consolidation"
  - ⚠️ NEEDS factcheck against DeepSeek-V4 paper — is "pure" correct? "mixed RL stage" replaced wholesale vs modified? **flagged for Round 1 VERIFY**

### ¶5 (L92) — Field momentum paragraph (added in prior round)
- **Claim**: "GKD introduced the first unified on-policy framework for LLM distillation in mid-2023"
  - ⚠️ GKD (Agarwal et al. 2023) is INDEED the first major LLM OPD paper, but "first unified" is a strong claim — there was also prior on-policy KD in seq2seq MT (knowledge distillation from monolingual data, 2021-2022). Soften to "the first on-policy framework for decoder-only LLM distillation to gain wide adoption"?
- **Claim**: "fewer than three years later the literature has expanded to over one hundred papers"
  - ✅ Awesome list has 104 papers; ok
- **Insight**: closing sentence "making on-policy correction not merely beneficial but architecturally necessary for the next generation of reasoning-capable systems" — strong but unsupported. Add a cite? Perhaps \citep{2603.25562} (Revisiting OPD) or \citet{luo2026demystifying}

### ¶6 (L94) — The motivation for this survey
- "Existing surveys of LLM distillation~\citep{2402.13116} generally retain the classical compression framing"
  - ⚠️ 2402.13116 is Xu et al. 2024 "A Survey on Knowledge Distillation of Large Language Models". Check that it genuinely retains compression framing (likely yes, but worth verifying)
- Well-argued gap identification

### ¶7 (L97–L105) — Four contributions
- **Contribution 1** "unified theoretical framework": promise of f-divergence minimization over student-sampled trajectories ✓
- **Contribution 2** "decision-centric taxonomy": one-method-one-category ✓
- **Contribution 3** "theoretical account of failure": mentions flawed prefix trap, self-play saturation, diversity collapse, calibration-capability gap
  - ⚠️ "calibration-capability gap" — is this a term defined in the survey's §7 or is it novel nomenclature? Should be either cited to source or marked as "we term"
- **Contribution 4**: summary tables + decision tree

### ¶8 (L107) — Paper structure roadmap
- Clean; ties to decision-chain logic ✓

### ¶9 (L108) — Scope statement
- "generic off-policy KD, compression techniques that are orthogonal to the training paradigm such as pruning and quantization, and inference-time methods that leave model weights unchanged"
- ✓ good scope boundary

## Top-5 priority issues to fix (by DEEPEN round)

| # | Issue | Section | Action |
|---|-------|---------|--------|
| 1 | ⚠️ "near-human competence in reasoning, code generation, and multilingual instruction following" — overclaim | ¶1 | Soften: "state-of-the-art performance on reasoning, code generation, and multilingual benchmarks" |
| 2 | ⚠️ "DeepSeek-V4 … replacing its mixed RL stage with pure multi-teacher OPD" — verify "pure" | ¶4 | Check DeepSeek-V4 paper; if not pure, remove word |
| 3 | ⚠️ "GKD introduced the first unified on-policy framework" | ¶5 | Qualify: "first on-policy framework for decoder-only LLM distillation to gain wide adoption" |
| 4 | ⚠️ Closing of ¶5 "architecturally necessary" — unsupported | ¶5 | Add cite to \citep{2603.25562} or \citet{luo2026demystifying} |
| 5 | ⚠️ "calibration-capability gap" — term provenance | ¶7 | Check §7; if novel, mark "we term"; if prior, cite |

## Next action
VERIFY mode should:
1. Read DeepSeek-V4 paper §training pipeline to verify "mixed RL stage replaced with pure multi-teacher OPD"
2. Read Xu et al. 2024 \citep{2402.13116} to confirm compression framing claim
3. Locate "calibration-capability gap" in §7.x
4. Read DeepSeek-R1 Table 5 to confirm 1.5B-70B range
5. Read Gudibande 2023 \citep{2305.15717} abstract for surface-style vs reasoning claim

After VERIFY produces verdicts, DEEPEN can then make the 5 targeted edits.
