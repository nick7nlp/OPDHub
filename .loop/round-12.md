# Round 12 — DEEPEN §3.1 Method Landscape

**Mode**: DEEPEN  
**Section**: §3.1 Method Landscape (lines 207–325 → now 207–337)  
**Date**: 2026-05-08 17:53 UTC  
**Input**: round-10 READ issues + round-11 VERIFY findings

## Changes Made

### 1. Removed filler "specifically" from opening sentence
- Before: "three sequential decisions, specifically (1)..."
- After: "three sequential decisions: (1)..."
- Rationale: The colon + enumeration already makes it specific. One less filler word.

### 2. Grounded "engineering workflow" claim with DeepSeek-R1 cite
- Before: "reflects the actual engineering workflow" (unsupported assertion)
- After: "reflects the actual engineering workflow of state-of-the-art systems. DeepSeek-R1~\citep{2501.12948}, for instance, first selects Group Relative Policy Optimization as its objective, then decides on cold-start data from DeepSeek-V3 as the signal source, and finally tunes batch size, learning-rate decay, and sampling temperature to stabilize training dynamics."
- Rationale: Round-11 VERIFY confirmed DeepSeek-R1 pipeline maps to our three-stage model. Concrete example makes the claim falsifiable rather than hand-wavy.

### 3. Softened FKL overclaim
- Before: "Forward KL requires white-box logits, eliminating all black-box signal sources"
- After: "Forward KL in its exact token-level form requires access to the teacher's full output distribution, which precludes purely API-constrained settings where only generated text is available"
- Rationale: Round-11 verified the math (exact FKL needs p_T(v) for all v). But "eliminating ALL" was too absolute — variational bounds or Monte Carlo proxies could approximate FKL without full logits. The new phrasing is precise: *exact* FKL needs full distribution; purely text-only APIs can't provide it.

### 4. Added structural paragraph break + takeaway sentence
- Split into two paragraphs: (a) pipeline grounding, (b) interdependence analysis
- Added closing insight: "This interdependence means that choosing an objective implicitly constrains the viable signal sources and dynamics strategies, making the taxonomy a practical navigation tool rather than a flat catalog of methods."
- Rationale: Round-10 flagged missing "so what?" — high-cited surveys always close with an actionable insight.

### 5. Structural improvement: "Crucially, the three stages are not independent"
- Added transitional sentence that frames the incompatibility/synergy discussion as a consequence of stage interdependence, not just a list of examples.

## Build Verification
- `pdflatex` clean: 0 errors, 57 pages, 522KB
- Font warning only (fontawesome shape, irrelevant)
- No undefined citations

## What was NOT changed
- TikZ tree figure untouched (all counts verified correct in rounds 10-11)
- Figure caption untouched
- Did not add the SelecTKD/AdaSwitch cross-reference note (that's §5.1, out of scope for this section's DEEPEN)

## Net improvement
§3.1 prose went from 5 sentences to ~10 sentences across two well-structured paragraphs. Added:
- 1 concrete citation (DeepSeek-R1)
- 1 precise qualification ("in its exact token-level form")
- 1 practitioner takeaway (taxonomy = navigation tool)
- Better paragraph structure with clear pivot from "what the pipeline is" to "why stages interact"
