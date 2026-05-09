# Round 60 — §3.1 Method Landscape READ

**Mode**: READ  
**Section**: §3.1 Method Landscape (L209–L329)  
**Date**: 2026-05-09 02:51 UTC  
**Assignment**: round=60, 60%5=0→READ, (60//5)%10=2→3.1-Method-Landscape

## Structure Overview

§3.1 consists of:
- 1 opening paragraph (L210–211): introduces the "three sequential decisions" framing
- 1 large TikZ forest figure (L213–L323): taxonomy tree with badge counts
- 2 prose paragraphs (L325–L329): explain the pipeline with an example + discuss interdependence

**总体评价**: 节奏上头重脚轻——一个巨大的 figure 占了 115 行 LaTeX，但 narrative prose 只有 ~6 句话。对一个号称 "Method Landscape" 的 subsection 来说，prose 太薄了。高引综述在 taxonomy 展示后通常有一段 **synthesis paragraph** 说明 field evolution / method growth trend / 各 branch 的相对成熟度。

---

## Paragraph-by-Paragraph Issues

### ¶1 Opening (L210–211)
> "The practitioner faces three sequential decisions: (1) what objective to optimize, (2) where the supervisory signal originates, and (3) how to stabilize the resulting training dynamics."

**Issues**:
1. ✅ Clean, direct setup sentence. No issues.
2. **Missing motivational context** — why these three specifically? Is there a design principle or historical reason the field converged on these three axes? A brief "why three" sentence would help (e.g., "These three dimensions emerged independently in the literature but together characterize the full design space..."). Currently jumps to "Figure X illustrates this pipeline" too quickly.
   - **Priority: low** — not wrong, just thin

### ¶2 (L325–326): DeepSeek-R1 as example
> "DeepSeek-R1, for instance, first selects Group Relative Policy Optimization as its objective, then uses cold-start data from DeepSeek-V3 as its signal source, and finally tunes batch size, learning-rate decay, and sampling temperature to stabilize training dynamics."

**Issues**:
3. **❌ Factual inaccuracy / misleading framing** — DeepSeek-R1's main training pipeline is RL (GRPO), NOT distillation. The paper describes two separate pipelines:
   - (a) Training R1 itself: RL with GRPO on top of V3-Base → this is NOT distillation
   - (b) Distilling R1 into smaller models (1.5B–32B): uses SFT on R1-generated CoT data → this IS on-policy distillation, but the objective is cross-entropy/SFT, NOT GRPO
   
   The current text conflates R1's RL training (pipeline a) with distillation (pipeline b). Using R1 as an illustration of the "distillation pipeline's three stages" is misleading because the GRPO step is RL, not a distillation objective.
   
   **Fix options**:
   - Replace the R1 example with one that genuinely goes through all three distillation stages (e.g., GKD: Forward KL objective + white-box teacher logits + interpolated data sources for stability)
   - Or rewrite to use the R1-distilled models as the example: "The DeepSeek-R1-distilled models use cross-entropy as their objective, rely on R1-generated reasoning chains as their signal source, and employ curriculum over difficulty levels to stabilize training"
   - **Priority: HIGH** — this is a factual/framing error in a key illustrative paragraph
   
4. **"cold-start data from DeepSeek-V3"** — "cold-start" in R1 refers to a small set of human-annotated examples used to bootstrap the RL phase (overcome initial incoherence). It's not a "signal source" for distillation — it's a warm-up technique for RL. Misattribution.
   - **Priority: HIGH** — same issue as above

5. **Missing cite for "cold-start"** — the phrase should be attributed to R1 paper's specific usage, currently relies on the single R1 cite at start of sentence. OK but could be more precise.
   - **Priority: low**

### ¶2 continued (L326): practitioner mirror sentence
> "A practitioner navigates the same sequence by choosing an objective (Forward KL? Reverse KL? Adaptive? RL-augmented?), selecting a signal source (white-box logits, black-box API, or self-generated), and addressing the dynamics challenges arising from that combination."

**Issues**:
6. **Structurally fine** but reads as padding — just restates the three axes again. A high-cited survey would use this space to add information, e.g., the relative frequency/popularity of each choice, or how the field has shifted over time.
   - **Priority: low-medium** — opportunity for insight rather than error

### ¶3 (L328–329): Interdependence
> "Crucially, the three stages are not independent..."

**Issues**:
7. **Good insight** — the incompatibility/synergy discussion is genuinely useful. This is the strongest paragraph in §3.1.

8. **Claim without cite**: "Forward KL in its exact token-level form requires access to the teacher's full output distribution" — while this is mathematically self-evident from the definition of KL divergence (needs both p and q), stating it as a finding should either (a) cite a paper that explicitly discusses this constraint, or (b) use "by definition" language to signal it's a mathematical fact rather than an empirical finding.
   - **Priority: low** — mathematically obvious but academic writing benefits from precision

9. **"Our decision tree (Section X) makes such constraints explicit"** — the phrase "our" implies the decision tree is a contribution. If it is indeed novel to this survey, fine. But check: is it? If it's adapted from something else, needs acknowledgement.
   - **Priority: low**

10. **Last sentence overlong** (54 words): "This interdependence implies that an objective choice constrains the viable signal sources and dynamics strategies, making the taxonomy a practical navigation tool rather than a flat catalog of methods." — Could be tightened. The distinction between "practical navigation tool" vs "flat catalog" is good but could be punchier.
    - **Priority: low**

---

## Figure Verification

Badge counts all verified correct (counted manually):
- §4.1: 5 ✅ | §4.2: 3 ✅ | §4.3: 11 ✅
- §5.1: 10 ✅ | §5.2: 10 ✅ | §5.3 total: 26 ✅ (12+8+6)
- §6.1: 4 ✅ | §6.2: 8 ✅ | §6.3: 3 ✅

**Total methods in figure**: 5+3+11+10+10+12+8+6+4+8+3 = 80 methods across all leaves. Note: PAINT appears in both §5.3.2 and §6.2, PRISM appears in both §5.2 and §6.2. This is fine (caption says "Methods that contribute to multiple dimensions are placed under their most distinctive contribution") — but wait, if a method appears in TWO leaves, that contradicts the one-method-one-category rule stated in §3.2? Need to check.

11. **Duplicate entries in figure**: PAINT appears in §5.3.2 (Self-Play) and §6.2 (Curriculum). PRISM appears in §5.2 (Black-Box) and §6.2 (Curriculum). The figure caption says methods are placed "under their most distinctive contribution" (singular), but these appear in two places each. This violates the §3.2 "strict one-method-one-category rule" and inflates badge counts.
    - **Priority: MEDIUM-HIGH** — internal consistency issue. The §5.3 badge shows 26, which includes PAINT, and §6.2 badge shows 8, which also includes PAINT. Either deduplicate or explicitly note in figure caption that some methods appear twice.

---

## Structural / Quality Issues

12. **Prose-to-figure ratio**: 6 sentences of actual prose for a subsection named "Method Landscape" is thin. Compare: a high-cited survey's taxonomy section typically includes:
    - Growth timeline ("the number of methods doubled between 2024 and 2025")
    - Field maturity per branch ("Objective functions are relatively mature with clear winners; training dynamics is still fragmented")
    - Reader takeaway ("the dominant trend is toward RL-augmented objectives with self-distillation signal")
    None of these are present. The section is essentially just "here's a figure, here's why the axes interact."
    - **Priority: MEDIUM** — deepening opportunity, not error

13. **No practitioner takeaway** — Plan says "Takeaways per section" is a high-cited-survey trait. §3.1 has no concrete takeaway paragraph (e.g., "If you are building a distilled model today, the most well-tested path is... while the highest-potential frontier is...").
    - **Priority: MEDIUM** — DEEPEN round should add this

---

## Summary of Issues by Priority

| # | Issue | Priority | Action |
|---|-------|----------|--------|
| 3-4 | DeepSeek-R1 example factually misleading (conflates RL with distillation) | **HIGH** | Replace or rewrite example |
| 11 | PAINT/PRISM appear in 2 figure leaves, violating one-category rule | **MEDIUM-HIGH** | Deduplicate or amend caption |
| 12 | Thin prose — no field trends, no maturity analysis | **MEDIUM** | DEEPEN: add synthesis paragraph |
| 13 | No practitioner takeaway | **MEDIUM** | DEEPEN: add takeaway |
| 6 | Practitioner mirror sentence is padding | **LOW-MEDIUM** | Replace with actual data |
| 1-2, 5, 8-10 | Minor phrasing/citation opportunities | **LOW** | POLISH round |

---

## 下一步建议

- VERIFY round: 核实 R1 paper 的 distillation pipeline 细节，确认 cold-start 的真实含义
- DEEPEN round: (1) 替换 R1 example，(2) 加 field-evolution paragraph，(3) 加 practitioner takeaway
- Check PAINT/PRISM duplication against §3.2 classification table
