# Round 66 — VERIFY on §4-Objectives

**Mode:** VERIFY  
**Section:** §4 Objective Functions and Optimization  
**Time:** 2026-05-09T04:17Z  

## Claims Verified

### 1. REOPOLD "6.7–12× sample efficiency + 7B matches 32B + 3.3× speedup"
- **Source:** arXiv:2603.11137, abstract + Figure 1
- **Paper says:** "6.7 ∼ 12× greater sample efficiency" and "enables a 7B student to match a 32B teacher in visual reasoning with a ∼ 3.32× inference speedup"
- **Survey says:** "6.7--12$\times$ greater sample efficiency" and "~3.3× inference speedup"
- **Verdict:** ✅ ACCURATE (paper says 3.32×, survey rounds to ~3.3×, acceptable)

### 2. RLKD "0.1% data surpasses SFT-RL pipelines"
- **Source:** arXiv:2505.16142, abstract
- **Paper says:** "RLKD, even when trained on only 0.1% of the data under an RL-only regime, surpasses the performance of standard SFT-RL pipelines"
- **Survey says:** "RLKD trained on only 0.1% of the data under a pure RL regime surpasses standard SFT-RL pipelines"
- **Verdict:** ✅ ACCURATE (verbatim match)

### 3. Lightning OPD "4× speedup under teacher consistency"
- **Source:** arXiv:2604.13010, abstract
- **Paper says:** "Lightning OPD reaches 69.9% on AIME 2024 in just 30 GPU hours, achieving a 4.0x speedup over standard OPD"
- **Survey says:** "4× speedup over standard OPD under a teacher consistency condition"
- **Verdict:** ✅ ACCURATE

## Overclaim Fixed

### "no fixed divergence is ever optimal" (line 738)
- **Issue:** Universal claim without qualification
- **Fix:** Changed to "no single fixed divergence dominates uniformly" and "across evaluated settings"
- **Rationale:** The papers (ToDi, AKL, Entropy-Aware OPD) show this *within their evaluated settings*, not as a universal mathematical truth

## Compilation
- 0 errors, 60 pages
- Only font shape warning (FontAwesome bold, cosmetic)

## Summary
All three numeric claims from §4.3 verified accurate against source papers. Fixed one overclaim (line 738) by qualifying the universality of the adaptive-divergence finding.
