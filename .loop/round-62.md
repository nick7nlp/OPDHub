# Round 62 — §3.1 Method Landscape DEEPEN

**Mode**: DEEPEN  
**Section**: §3.1 Method Landscape  
**Date**: 2026-05-09 03:11 UTC  
**Assignment**: round=62, 62%5=2→DEEPEN, (62//5)%10=2→3.1-Method-Landscape  
**Input**: Round 60 READ + Round 61 VERIFY

---

## Changes Made

### 1. Replaced R1 example (HIGH priority factual error fix)

**Before**: DeepSeek-R1 example conflated R1's RL training (GRPO + cold-start) with distillation. Falsely claimed GRPO was the "distillation objective" and cold-start data was the "signal source."

**After**: Two examples that genuinely illustrate the three-stage distillation pipeline:
- **GKD** (research prototype): forward KL/JSD objective → white-box teacher logits → interpolated sampling ($\pi_{\text{mix}}$)
- **DeepSeek-R1 distilled models** (industrial deployment): cross-entropy objective → 800K R1-generated reasoning chains → cosine LR + curricula

This correctly distinguishes R1's RL training (which is NOT distillation) from R1's downstream distillation into 1.5B–32B models (which IS on-policy distillation with SFT objective). Also removed the padding "practitioner mirror" sentence that just restated the three axes without adding information.

### 2. Fixed PAINT/PRISM duplication in figure (MEDIUM-HIGH consistency fix)

**Before**: §6.2 Curriculum leaf listed PAINT and PRISM alongside 6 other methods (badge=8), but both have their primary home in §5 (PAINT in §5.3.2 Self-Play, PRISM in §5.2 Black-Box). Figure caption claimed singular placement but actually duplicated.

**After**: Removed PAINT and PRISM from §6.2 leaf, badge 8→6. §6.2 prose (L960) already cross-references them as "methods from earlier sections [that] provide implicit curriculum mechanisms," so no information is lost. Updated figure caption to explicitly note the cross-referencing policy.

### 3. Added field evolution + practitioner takeaway paragraph (MEDIUM deepening)

New synthesis paragraph after the interdependence discussion:
- **Evolutionary trajectory**: Objective axis (2023–2024) → Signal architecture/self-distillation (mid-2025) → Training dynamics (late 2025–2026)
- **Practitioner takeaway**: Most validated path = JSD/adaptive KL + white-box + token weighting. Highest potential frontier = self-distillation + RL-augmented objectives (SD-ZERO, SRPO).

This addresses Round 60 issues #12 (thin prose, no field trends) and #13 (no practitioner takeaway).

---

## Build Verification

```
pdflatex: 0 errors, 0 undefined refs, 60 pages (was 57 baseline → 60 from prior rounds)
Writing rules check: clean (no em-dashes, no new prose colons, no semicolons in my edits)
```

Pre-existing violations (not from this round):
- L1181: one em-dash in §9 (long-standing, POLISH round for §9 will fix)
- L200, L765, L1181: prose colons (structural, pre-existing)

---

## 下一步

- POLISH round (63): line-level prose pass on §3.1. Fix the "incompatible:" colon on L327, tighten the new paragraphs further.
- §3.2 "Distributional observations" paragraph mentions 13 Training Dynamics methods, but with PAINT/PRISM removed from §6.2, the tree shows 4+6+3=13 still correct (PAINT/PRISM were leaf entries, not §3.2 table entries). ✅ consistent.
