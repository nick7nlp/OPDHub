# Round 21 — VERIFY §5 Signal Source

**Mode**: VERIFY  
**Section**: §5 (lines 768–918)  
**Date**: 2026-05-08 19:41 UTC  
**Following up**: Round 20 READ issues

## Verification Results

| # | Claim | Source Paper | Verdict | Detail |
|---|-------|-------------|---------|--------|
| 1 | "1,000× less data" (Distilling Step-by-Step) | 2305.02301 | ❌ WRONG | Paper claims "500× fewer parameters" (770M vs 540B) and "80% of available data" / "50% less training examples on average (up to 85% reduction)". It NEVER says "1000× less data." |
| 2 | \citep{2305.02301} as cite for "on-policy CoT distillation is de facto standard" | 2305.02301 | ❌ MISLEADING | Distilling Step-by-Step is definitively **off-policy** (extracts teacher rationales, then SFT). It demonstrates the VALUE of rationale distillation but is not itself on-policy. Should not be the sole citation for on-policy being "de facto standard." |
| 3 | RLSD "200 steps surpasses GRPO 400 steps" on Qwen3-VL-8B-Instruct | 2604.03128 | ✅ ACCURATE | Figure 1(b) caption: "RLSD at 200 steps already surpasses GRPO trained for twice as many steps." Model confirmed Qwen3-VL-8B-Instruct. |
| 4 | PAINT "+2.1 over OPSD, +2.9 over GRPO" | 2604.26573 | ✅ ACCURATE | Table 1 Macro avg (Avg@12): GRPO=64.0, OPSD=64.8, PAINT=66.9. Differences = 2.1 and 2.9 exactly. Benchmarks: AIME 2024, AIME 2025, HMMT 2025. |
| 5 | SRPO "+3.4% over GRPO, +6.3% over SDPO" | 2604.02288 | ✅ ACCURATE (但 benchmark 描述有误) | Abstract confirms "five-benchmark average on Qwen3-8B by 3.4% over GRPO and 6.3% over SDPO." The 5 benchmarks are **Chemistry, Physics, Biology, Materials, Tool Use** — NOT "AIME, MATH, Code" as erroneously stated in survey Table (line 522). |
| 6 | π-Play "surpasses Search-R1" | 2604.14054 | ✅ ACCURATE | Paper states: surpasses Search-R1 by 6.2%, 5.2%, and 14.5% on Qwen3-4B, Qwen3-4B-Instruct-2507, and Qwen3-8B respectively. |
| 7 | MTP "<5% accuracy drop" at >3× decoding speed | 2602.06019 | ⚠️ MODEL-DEPENDENT | L3.1-8B-Magpie: <3% drop at 3× speed. Qwen3-4B-Inst-2507: 7% drop at 3× speed. The "<5%" is true for one model but not the other. Should qualify. |

## Errors Requiring Fix (Priority Ordered)

### 1. ❌ Line 815: "1,000× less data" → must correct
**Correct claim**: 500× fewer model parameters, with 50% less training data on average (up to 85% reduction). The "1000×" likely conflated two different numbers.
**Fix**: Replace "with as little as 1,000$\times$ less data" → "with 500$\times$ fewer parameters and substantially less training data (50\% fewer examples on average)"

### 2. ❌ Line 783: \citep{2305.02301} for on-policy "de facto standard"
**Problem**: Off-policy paper cited as evidence for on-policy being standard.
**Fix**: Rephrase to acknowledge 2305.02301 established the rationale-distillation principle (off-policy), then cite GKD (2306.13649) or DeepSeek-R1 (2501.12948) for on-policy becoming the standard. E.g.: "This principle, first demonstrated in the off-policy setting by~\citet{2305.02301}, becomes particularly powerful under on-policy generation~\citep{2306.13649}, making on-policy CoT distillation the de facto paradigm for instilling multi-step reasoning."

### 3. ❌ Line 522 (Table): SRPO benchmarks listed as "AIME, MATH, Code" 
**Correct**: Chemistry, Physics, Biology, Materials, Tool Use (5 science/tool-use benchmarks)
**Fix**: Change "AIME, MATH, Code" → "Chem, Phys, Bio, Mat, ToolUse"

### 4. ⚠️ Line 890: MTP "<5% accuracy drop" → qualify
**Fix**: Change "$<5\%$ accuracy drop" → "typically 3--7\% accuracy drop depending on the base model"

### 5. 🔍 Line 911: SRPO "+3.4% / +6.3%" — missing benchmark context
**Fix**: Add "(five-benchmark average on Qwen3-8B)" after the numbers

### 6. 🔍 PAINT "+2.1 / +2.9" — missing benchmark context
**Fix**: Add benchmark specification. Check where this appears in the tex.

## Already Verified & Accurate (no changes needed)

- RLSD 200 steps > GRPO 400 steps on Qwen3-VL-8B-Instruct ✅
- PAINT +2.1/+2.9 (numbers correct, just needs benchmark label) ✅  
- π-Play surpasses Search-R1 ✅
- All 8 claims verified in round 20 spot-checks ✅

## Next Steps (for round 22 DEEPEN)

1. Fix the ❌ errors (1000× less data, misleading cite, SRPO table benchmarks)
2. Add benchmark context to SRPO and PAINT prose claims
3. Qualify MTP accuracy drop
4. These are targeted edits — no full rewrite needed
