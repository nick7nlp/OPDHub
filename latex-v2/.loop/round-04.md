# Round 4 — READ §2 Background

**Mode:** READ  
**Section:** Background and Unified Math  
**Date:** 2026-05-09T05:25Z

## Summary

Thorough read of the full Background section (~96 lines, 4 subsections: Classical KD, Off-Policy Exposure Bias, Unified f-Divergence Framework, Distillation Scaling Laws). Section is mathematically rigorous and well-structured.

## Findings

### ✅ Strengths
- Clean mathematical progression from classical KD → Seq-KD → on-policy
- The "From classical KD to on-policy" paragraph is excellent — clear relaxation chain with prescriptive guidance
- DAgger Remark is valuable nuance (acknowledges theory limitations)
- f-divergence framework properly unifies GKD/MiniLLM/DistiLLM
- All 14 citations verified present in references.bib

### ⚠️ Issues Found

1. **Mild AI-taste**: "a critical limitation that motivates the softer distributional matching methods below" — "critical limitation" is mildly overblown, consider just "limitation"
2. **Repetition**: "revealing" + "reveals" in same paragraph about temperature (line ~22-24)
3. **Verify**: "KL divergence dropping from 2.637 to 0.343 at a single teacher-reset event" — specific numbers from ttopd2026, should verify
4. **Verify**: MiniLLM uses α=0.2 — should confirm against paper
5. **Verify**: DistiLLM formulation — "$\KL(\pteacher \parallel \tilde{p})$" with $\tilde{p} = \alpha \pteacher + (1-\alpha)\ptheta$ — need to confirm this is the correct divergence direction and mixture definition
6. **Minor**: "This approximation works well when the teacher is highly confident but discards all information" — "all information" is a slight overclaim (it discards non-peak information, not ALL information)
7. **Style**: 4× "This [verb]..." sentence starts — not terrible but could diversify 1-2
8. **No prose semicolons** ✅
9. **No prose colons** ✅ (all colons introduce equations/lists)
10. **No banned AI words** ✅ (However/Moreover/Furthermore etc. absent)

### 📋 Pending Verify Queue (to process in R5)
- `ttopd2026`: KL 2.637→0.343 at teacher-reset
- `2306.08543` (MiniLLM): α=0.2 default
- `2402.03898` (DistiLLM): divergence direction and mixture formula

## No changes made (READ mode)
