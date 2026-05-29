# Round 47 — DEEPEN — §10 Conclusion

**Mode**: DEEPEN  
**Section**: §10 Conclusion  
**Assignment**: round 47 % 5 = 2 → DEEPEN; (47 // 5) % 10 = 9 → 10-Conclusion  
**Source**: round-45 READ + round-46 VERIFY findings

---

## Changes Made

### 1. Added citation for error-compounding claim (Issue #4, VERIFY ✅)
**Before**: "...where error compounding is most severe."  
**After**: "...where error compounding is most severe~\citep{2306.08543,2306.13649}."  
**Rationale**: MiniLLM Fig 6 shows ExAccErr accumulates with generation length; GKD §2 discusses "cascading effect." Both directly support this claim.

### 2. Added cite for "higher variance" in practical takeaways (Issue #9)
**Before**: "...are preferable despite higher variance."  
**After**: "...are preferable despite higher gradient variance inherent to REINFORCE-style estimators~\citep{2306.08543}."  
**Rationale**: MiniLLM discusses this explicitly in its variance reduction section.

### 3. Added cross-ref + cite for gap claims in Looking Ahead (Issues #13-15)
**Before**: "The absence of distillation scaling laws, the unsolved problem of teacher uncertainty quantification, and the challenge of lifelong adaptation without catastrophic forgetting stand as..."  
**After**: "The absence of distillation scaling laws (Section~\ref{sec:future}), the unsolved problem of teacher uncertainty quantification, and the challenge of lifelong adaptation without catastrophic forgetting~\citep{kirkpatrick2017overcoming} stand as..."  
**Rationale**: Cross-ref to §9 grounds the scaling laws gap; Kirkpatrick (2017) EWC is the canonical continual learning reference.  
**Bib addition**: `kirkpatrick2017overcoming` (PNAS 2017, 10k+ cites).

### 4. Softened "architectural necessity" → "core component" (Issue #16, VERIFY ❌)
**Before**: "...will transition from an optional training enhancement to an architectural necessity."  
**After**: "...will transition from an optional training enhancement to a core component of the LLM training stack."  
**Rationale**: No paper explicitly claims OPD is "architecturally necessary." "Core component" is strong but defensible.

### 5. Fixed "8-10 papers per month" → "more than ten" (Issue #17, VERIFY ⚠️)
**Before**: "(approximately 8--10 new OPD papers per month)"  
**After**: "(more than ten new OPD papers per month through early 2026)"  
**Rationale**: Our bib has 59 papers Jan-Apr 2026 = ~15/month. "More than ten" is conservative and directly defensible.

### 6. Condensed MSD paragraph (Issue #23/#26)
Reduced from ~8 sentences of method detail to 2 focused sentences. Kept the key result (generalizes to unseen languages + challenging jailbreaks) and the mechanism's essence (upweighting safety-critical tokens via teacher confidence × student disagreement), but removed the tutorial-level explanation of DPSW internals that belongs in §8, not a conclusion.

### 7. Fixed "orders of magnitude" → "by an order of magnitude or more" (Issue #25, VERIFY ⚠️)
**Rationale**: 70B→7B = 10x (one order); only extreme 405B→7B approaches two orders. "An order of magnitude or more" is accurate without overclaiming.

### 8. Added stronger closing sentence (Issue from round-45 structural observation)
**Before**: Ended on carbon accounting ("...amortized across billions of inference calls.")  
**After**: Added a closing vision sentence about the convergence of distillation, RL, and self-play into unified on-policy training, with the insight that next-gen LLMs won't be trained once and deployed, but will continuously refine through interactions.  
**Rationale**: High-cited surveys end on trajectory/vision, not accounting.

### 9. Added compute cross-ref (Issue #24)
Added "(Section~\ref{subsec:compute})" after "4-5x over off-policy SFT" to ground this number.

---

## Build Verification

```
pdflatex × 4 + bibtex × 1
Pages: 59 (unchanged)
LaTeX Errors: 0
Undefined citations: 0
Font warning: fontawesometwo/b/n (cosmetic, pre-existing)
```

---

## Net effect on conclusion quality

- **Citations added**: 3 new cite references + 1 new bib entry (kirkpatrick2017overcoming)
- **Cross-refs added**: 2 (sec:future, subsec:compute)
- **Overclaims fixed**: 2 ("architectural necessity", "orders of magnitude")
- **Structural improvement**: MSD paragraph cut from ~8 sentences to 2; stronger closing hook
- **Line count change**: reduced by ~4 lines (MSD condensation offsets additions)

所有 VERIFY round 的 high-priority issues 已 fix。剩余 #12 (grand philosophy claim) 属于 POLISH 层面，留给 round-48。
