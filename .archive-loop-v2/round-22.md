# Round 22 — DEEPEN §5 Signal Source

**Mode**: DEEPEN  
**Section**: §5 (Signal Source and Teacher Architecture)  
**Date**: 2026-05-08 19:51 UTC  
**Based on**: Round 20 (READ) + Round 21 (VERIFY)

## Changes Made

### 1. ❌→✅ Fixed factual error: "1,000× less data" (line 815)
- **Before**: "enabling it to outperform the teacher on downstream tasks with as little as 1,000× less data"
- **After**: "enabling a 770M-parameter model to outperform a 540B-parameter teacher with 500× fewer parameters and substantially less training data (50% fewer examples on average, up to 85% reduction on some tasks)"
- **Reasoning**: Paper (2305.02301) claims 500× fewer params (770M vs 540B) and 50% less data on average. "1000× less data" was a conflation of separate claims.

### 2. ❌→✅ Fixed misleading citation for "de facto standard" (line 779)
- **Before**: "...is why on-policy CoT distillation has become the de facto standard for instilling multi-step reasoning into smaller models~\citep{2305.02301}"
- **After**: Restructured to: (a) state the conclusion first, (b) credit 2305.02301 as establishing the off-policy principle, (c) cite GKD (2306.13649) for proving on-policy works better, (d) cite DeepSeek-R1 (2501.12948) for scale validation
- **Reasoning**: 2305.02301 (Distilling Step-by-Step) is definitively off-policy (SFT on teacher traces). Cannot be the sole cite for on-policy being the standard.

### 3. ❌→✅ Fixed SRPO table benchmarks (line 522)
- **Before**: "AIME, MATH, Code"
- **After**: "Chem, Phys, Bio, Mat, ToolUse"
- **Reasoning**: Verified in R21 — SRPO's 5 benchmarks are science/tool-use tasks, not math/code.

### 4. ⚠️→✅ Qualified MTP accuracy drop (line ~890)
- **Before**: "$<5\%$ accuracy drop"
- **After**: "typically 3--7\% accuracy drop (model-dependent)"
- **Reasoning**: R21 verified L3.1-8B-Magpie shows <3% but Qwen3-4B shows 7%. The claim is model-dependent.

### 5. 🔍→✅ Added benchmark context to SRPO prose (line ~911)
- **Before**: "SRPO raises the average by 3.4% over GRPO and 6.3% over SDPO alone"
- **After**: "SRPO raises the five-benchmark average on Qwen3-8B by 3.4% over GRPO and 6.3% over SDPO alone across science and tool-use tasks"

### 6. 🔍→✅ Added benchmark context to PAINT numbers (line ~900)
- **Before**: "On competition-level mathematics, PAINT achieves..."
- **After**: "On competition-level mathematics (AIME 2024/2025 and HMMT 2025 average), PAINT achieves..."

### 7. 🔍→✅ Added citation for "path-dependent" claim (line 775)
- Added `\citep{2306.13649}` to the path-dependence insight, since GKD explicitly motivates on-policy generation to address train-inference distribution mismatch (a form of path-dependency).

### 8. 🔍→✅ Added cross-reference §5.1 → §6
- At end of token-level adaptive supervision paragraph: "These token-selection mechanisms complement the sample-level and token-level weighting schemes discussed in Section~\ref{sec:dynamics}."

### 9. ✏️ Clarified Distilling Step-by-Step as off-policy ancestor
- Added explicit note that it's "technically off-policy (the student fine-tunes on static teacher-generated rationales)" but is "the conceptual ancestor of on-policy CoT distillation"
- This prevents readers from confusing it as an on-policy method despite being in §5.2.

## Build Results
- pdflatex: ✅ no errors
- Pages: 58 (within 55-60 target)
- No undefined citations
- No LaTeX errors

## Not Addressed This Round (lower priority, for future rounds)
- PRISM paragraph too long (structural, for POLISH round)
- "CoT-OPD" formula attribution clarity (minor, for READ of next pass)
- RLSD / SSD benchmark context (already has model names, lower priority)
