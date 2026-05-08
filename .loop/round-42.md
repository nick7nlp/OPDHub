# Round 42 — DEEPEN §9-Future-Directions

**Mode**: DEEPEN  
**Section**: §9 Open Problems and Future Directions  
**Date**: 2026-05-09 07:41 CST  
**Input**: Round 40 (READ) + Round 41 (VERIFY) findings

## Changes Made

### 1. Removed self-invented display equation (CRITICAL — boss directive violation)

The scaling law formula `L(N_S, N_T, D_{on}) = E + A/N_S^α + ...` was a "research proposal" style conjecture. Removed entirely and replaced with narrative description of what's known and what gap remains.

### 2. Fixed 2502.08606 characterization (VERIFY finding: inaccurate)

**Before**: "fitting parametric curves that reveal optimal teacher size grows sub-linearly with compute budget"

**After**: Accurately describes the non-monotone relationship discovered in the paper — optimal teacher size (1) grows initially, (2) plateaus slightly above student size, (3) eventually *decreases* due to inference cost domination. Also removed the speculative α/β/γ interpretation.

### 3. Removed self-invented c_t formula (boss directive violation)

**Before**: `c_t = 1 - H(p_teacher(·|x, y_{<t}))/log|V|` — a self-proposed confidence weight formula

**After**: Converted to pure narrative describing the *intuition* (suppress gradient at high-entropy positions) without proposing a specific formula. Added insight about TIP showing *relative* uncertainty matters more than absolute confidence.

### 4. Added Kaplan citation

Added `@article{2001.08361}` (Kaplan et al. 2020, "Scaling Laws for Neural Language Models") to references.bib. Changed bare "Kaplan" to proper `\citep{2001.08361,2203.15556}`.

### 5. Added missing citations in Efficiency paragraph

- Fast OPD → `\citep{2602.15260}`
- Lightning OPD → `\citep{wu2026lightning}`
- Speculative KD → `\citep{2410.11325}`

### 6. Added missing citations in Latent-space paragraph

- VOLD → `\citep{2510.23497}`
- X-OPD → `\citep{2603.24596}`
- CORD → `\citep{hu2026cord}`

### 7. Fixed prose colon

"selective teacher inference:" → "selective teacher inference---" (em-dash)

### 8. Improved narrative structure

- Split the scaling law paragraph into two logical paragraphs (theory from 2502.08606 | empirical from DeepSeek-R1/Qwen3)
- Split the uncertainty paragraph into three (core problem | connection to failure modes | predictive uncertainty frontier)
- Added synthesis insight about TIP: "relative uncertainty (how surprised the teacher is by the student's continuation) matters more than the teacher's absolute confidence"

## Build Verification

- ✅ 59 pages
- ✅ 0 LaTeX errors
- ✅ 0 undefined references
- ✅ All new citations resolve correctly

## Reasoning

The two biggest issues from R40/R41 were both boss-directive violations (self-invented formulas). These had to go regardless of prose quality. The 2502.08606 fix is important for accuracy — the non-monotone relationship is the paper's *main contribution* and our original "sub-linear growth" characterization missed the most interesting finding (that optimal teacher size eventually *decreases*). The uncertainty paragraph rewrite gains insight without prescribing a specific mechanism — it now reads like a survey direction rather than a position paper proposal.

## 总结

本轮核心工作：删除两个自编公式（违反老大"纯叙事"指令）、修正 scaling law 论文的不准确描述（原来写"sub-linearly grows"实际是非单调）、补全 6 个缺失引用、改善段落结构。编译通过，59页，0错误。
