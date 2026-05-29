# Round 20 — READ §5 Signal Source and Teacher Architecture

**Mode**: READ  
**Section**: §5 (lines 768–918, ~151 lines)  
**Date**: 2026-05-08 19:31 UTC

## Summary

§5 is the longest section besides §3.2 (method comparison table). It's well-structured with three major subsections (White-Box, Black-Box, Self-Distillation) and the self-distillation further splits into PI/Self-Play/External Feedback. Overall quality is high — strong narrative flow, good synthesis paragraphs, and most claims are cited. However I found several issues.

## Issues Found

### ❌ Factual Error: "1,000× less data" (Distilling Step-by-Step)

**Line ~817**: "enabling it to outperform the teacher on downstream tasks with as little as 1,000× less data"

The actual paper (2305.02301) says:
- "500× fewer model parameters" (770M vs 540B PaLM)
- Outperforms with "only 80% of available data" (not 1000× less data)
- The paper emphasizes parameter reduction + data efficiency, but 1000× less data is not stated

**Fix**: Change to "500× fewer parameters and substantially less training data" or find the exact data reduction figure.

### ⚠️ Misleading Citation: \citep{2305.02301} for "de facto standard for on-policy CoT distillation"

**Line ~789**: "...is why on-policy CoT distillation has become the de facto standard for instilling multi-step reasoning into smaller models~\citep{2305.02301}"

Distilling Step-by-Step (2305.02301) is actually an **off-policy** method — it extracts teacher rationales and does SFT on them. It's NOT on-policy distillation. Using it as the cite for on-policy CoT distillation being the "de facto standard" is misleading. The paper demonstrates the VALUE of rationale distillation, which motivated later on-policy work, but it's not itself on-policy.

**Fix**: Either (a) cite a more appropriate on-policy paper (GKD 2306.13649, or DeepSeek-R1 2501.12948 for the "de facto standard" claim), or (b) rephrase to say "This principle, first demonstrated by \citet{2305.02301} in the off-policy setting, becomes even more powerful when combined with on-policy generation, and has made on-policy CoT distillation the de facto standard..."

### ⚠️ Uncited "de facto standard" claim

The "de facto standard" phrasing is a strong claim that lacks proper support. What evidence shows it's THE standard? DeepSeek-R1 and its followers could support this, or a reference to the widespread adoption pattern.

### 🔍 Missing synthesis opportunity: White-box subsection ending

The white-box subsection (§5.1) ends with a long passage about Delta-KD, Veto, PromptKD, TAID that's excellent in describing individual methods and their spectrum (problem-level → token-level → target-level → teacher-level). But it could be sharpened with a **practitioner takeaway**: "When should you use which granularity?" Currently it ends with "Because these four granularities are orthogonal, they can be combined..." — this is good synthesis but leaves the reader without concrete guidance.

### 🔍 Missing connection: CoT-OPD formula in section intro

**Lines 780-789**: The section intro presents a "CoT-OPD" loss formula that's not attributed to any specific paper. It appears to be a general formulation. This is fine for a survey, but should be explicitly marked as "a general formulation that encompasses methods such as GKD, DistiLLM, and their variants" to avoid confusion about whether it's from a specific paper.

### 🔍 Weak argumentation: "path-dependent" claim lacks citation

**Lines 776-779**: The path-dependence argument for reasoning is presented as an insight with no citation. While it's conceptually correct, it's a strong architectural claim ("This insight motivates the on-policy formulation"). Could cite GKD's original motivation, or the exposure bias literature (e.g., Bengio et al. scheduled sampling), or Singh et al. 2024 (2309.11235) who formalize this argument.

### 🔍 Potential unsupported claim: "RLSD surpasses GRPO trained for 400 steps on Qwen3-VL-8B-Instruct, demonstrating 2× sample efficiency"

**Line ~904**: Need to verify "200 training steps" vs "400 steps" and the "2×" characterization. The yang2026selfdistilled paper should be checked in next VERIFY round.

### 🔍 PAINT "+2.1 over OPSD" and "+2.9 over GRPO" — no benchmark specified

**Line ~910**: These numbers are presented without specifying which benchmark(s). Should state "on competition-level mathematics (AIME 2024/2025, average)" or whatever the actual benchmark is.

### 🔍 SRPO "+3.4% over GRPO and +6.3% over SDPO alone" — no benchmark specified

Similar issue — numbers without benchmark context.

### 🔍 Black-box section: PRISM paragraph is very long (12+ lines)

The PRISM paragraph starting at "PRISM~\citep{wang2026prism} introduces..." is excessively long for a single unbroken paragraph. It tries to cover: (1) the architectural innovation, (2) the pipeline position, (3) the MoE discriminator, (4) the adversarial game mechanism, (5) why disentangled feedback matters, (6) quantitative results. Could be split into two paragraphs after "...providing differentiated feedback through its expert routing."

### 🔍 Missing cross-reference: §5.1 → §6

The white-box section discusses token-level weighting (SelecTKD, AdaSwitch, Token-Adaptive KD) which overlaps heavily with §6 Training Dynamics (token/sample weighting). A forward reference like "These token-selection mechanisms complement the weighting schemes discussed in Section~\ref{sec:dynamics}" would help readers navigate.

### 📝 Style: Several long sentences could be split

- Line 797: "SelecTKD~\citep{2510.24021} routes based on student-teacher agreement, applying a propose-and-verify mechanism where..." (47 words before the period) — OK but pushing it
- The DSKD paragraph has a very long final sentence (line ~825) about "enabling distillation across different architectures..."

### 📝 Prose ban check

No semicolons found ✅  
No prose colons found (only structural/math) ✅  
No "it's important to note" or similar filler ✅

## Verification Queue (for Round 21 VERIFY)

| Claim | Paper | Priority |
|-------|-------|----------|
| "1,000× less data" | 2305.02301 | HIGH — likely wrong |
| 2305.02301 as on-policy cite | 2305.02301 | HIGH — misleading |
| RLSD "200 steps surpasses GRPO 400 steps" | yang2026selfdistilled | MEDIUM |
| PAINT "+2.1 over OPSD, +2.9 over GRPO" benchmark | wang2026paint | MEDIUM |
| SRPO "+3.4% over GRPO, +6.3% over SDPO" benchmark | li2026unifying/2604.02288 | MEDIUM |
| π-Play "surpasses Search-R1" | zhang2026piplay | LOW |
| Lion "competitive on BBH/AGIEval" | 2305.12870 | LOW (checked — accurate) |

## Already Verified This Round (spot checks)

| Claim | Paper | Verdict |
|-------|-------|---------|
| SPIN 5.94→6.78 MT-Bench, 3 iterations | 2401.01335 | ✅ Accurate |
| CRISP 57-59% token reduction, +9-16pp accuracy | 2603.05433 | ✅ Accurate |
| OVD +12.9% EM web QA, +25.7% math | 2601.21968 | ✅ Accurate |
| SD-ZERO 68.3% AIME2024 vs GRPO 62.5% | 2604.12002 | ✅ Accurate |
| SSD Qwen3-30B 42.4%→55.3% LiveCodeBench v6 | 2604.01193 | ✅ Accurate |
| LUFFY +6.4 avg over RLVR | 2504.14945 | ✅ Accurate |
| OPSD single rollout vs GRPO's 8, matches at 4B/8B | 2601.18734 | ✅ Accurate |
| ThinkTuning +3.85% over zero-shot, +2.08/2.23/3.99% over GRPO | 2508.07616 | ✅ Accurate |

## Overall Assessment

§5 is one of the strongest sections in the survey. The narrative arc (white-box → black-box → self-distillation) is well-motivated, the synthesis paragraphs are insightful, and the writing is generally tight. The main issues are:
1. One factual error (1000× less data)
2. One misleading citation (2305.02301 for on-policy)
3. A few numbers without benchmark context
4. Minor structural issues (PRISM paragraph too long, missing cross-ref to §6)

Priority for next rounds: fix the factual error and misleading citation in DEEPEN (round 22).
