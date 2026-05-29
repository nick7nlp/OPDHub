# Round 07 — DEEPEN §2 Background

**Mode**: DEEPEN  
**Section**: §2 Background (L109–L210)  
**Time**: 2026-05-08 17:01 UTC  
**Source**: Round 05 READ + Round 06 VERIFY findings  

---

## Changes Made

### 1. G-OPD overclaim fix (HIGH priority)

**Before**: "G-OPD relaxes all four simultaneously while adding RL-augmented objectives"  
**After**: "G-OPD relaxes assumptions (2)–(4) simultaneously while adding RL-augmented reward extrapolation that pushes the student beyond the teacher's frontier"

**Reasoning**: Round 06 verified that G-OPD (2602.12125) only uses same-family models (Qwen3 family). It does NOT address vocabulary mismatch (assumption 1). Replaced "all four" with "(2)–(4)" and added specificity about what G-OPD's RL augmentation actually does (reward extrapolation beyond teacher boundary).

### 2. GKD JSD claim nuance (MEDIUM priority)

**Before**: "on-policy sampling ($\lambda = 1$) with JSD divergence yields the best downstream performance on summarization and translation"  
**After**: "on-policy sampling ($\lambda = 1$) consistently outperforms off-policy across divergence choices, with JSD performing best on translation and competitive results across divergences on other tasks"

**Reasoning**: Round 06 verified that GKD actually uses forward KL on XSum/GSM8K, and JSD on WMT. The original claim was too strong — JSD isn't universally best, it's the on-policy part that universally helps. Fixed to accurately reflect what the paper shows.

### 3. §2.4 Scaling Laws — complete rewrite (HIGH priority, 2 issues merged)

Rewrote the entire scaling laws subsection to fix:
- **Busbridge misattribution** (claimed "student benefits from teacher scale after plateau" — actually Busbridge shows a capacity GAP where too-strong teacher hurts)
- **Unsupported "log-linear" claim** (no source for this — was attributed to Busbridge who doesn't study on-policy at all)
- **Speculative formula** (now explicitly marked as "A natural extension might take the form...")

New version accurately presents Busbridge's key finding (capacity gap / power law transition between two regimes) and separates it from the speculative extension to on-policy. Also introduces the rollout budget $R$ as a novel axis unique to on-policy distillation.

### 4. Temperature tail noise hedge (LOW priority)

**Before**: "higher temperatures risk amplifying noise in the teacher's poorly calibrated tail~\citep{2402.11890}"  
**After**: "higher temperatures may amplify noise in the teacher's poorly calibrated tail distribution"

Also moved the cite to cover the τ=1 claim specifically (which IS from that paper), and added `|V| > 30,000` to ground the "large vocabulary" claim.

### 5. DAgger remark cross-reference to TT-OPD (synthesis opportunity)

Added empirical evidence sentence linking the theoretical DAgger failure mode to TT-OPD's observed collapse: "KL divergence dropping from 2.637 to 0.343 over training." This connects §2 theory to §7's empirical findings, giving the remark real teeth instead of just theoretical hand-waving.

---

## Verification

- pdflatex: ✅ clean build, 57 pages, 0 errors, 0 undefined references
- Cite keys used: all existing (`ttopd2026`, `2602.12125`, `2306.13649`, `2402.11890`, `2502.08606`, `2203.15556`)
- No new cite keys introduced
- No semicolons or prose colons added
- No sections rewritten wholesale — all targeted edits

## Impact Assessment

These edits improve §2 on three dimensions:
1. **Factual accuracy**: G-OPD and Busbridge claims now match what the papers actually say
2. **Synthesis depth**: DAgger remark now connects theory→empirical evidence (TT-OPD), and scaling laws section explains the WHY (capacity gap mechanism) not just the WHAT
3. **Academic integrity**: speculative formula now clearly marked as conjecture, unsupported claims softened

## Remaining items for future rounds

- Reverse KL "single highest peak" → should be "a single mode" (minor, POLISH round)
- Forward KL inter-mode hallucination claim needs cite (Minka 2005 or GKD fig A.16)
- §2.3 task geometry paragraph "Reverse KL best for unique-answer tasks" still lacks empirical cite
- Notation paragraph could clarify p_θ ≡ π_θ
