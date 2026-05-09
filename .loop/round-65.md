# Round 65 — READ on 4-Objectives

**Time**: 2026-05-09 04:02 UTC  
**Mode**: READ  
**Section**: §4 Objective Functions and Optimization (lines 573–770)

## Findings

### Language / AI-taste
1. **Line 583**: "However, pure KL divergences exhibit numerical instability..." — sentence-initial However (AI taste). Can replace with "Pure KL divergences, however, exhibit..." or restructure.
2. **Line 715 (approx)**: Mid-paragraph "However, REINFORCE estimation in massive combinatorial output spaces..." — second However in section. Could use "Yet" or restructure.

### Structural Observations (no action needed — observations only)
3. The section has excellent logical flow: Fixed → Adaptive → RL-augmented, with clear transitions explaining *why* each escalation is needed.
4. The figure (KL divergence visualization) is well-placed between Fixed Divergence discussion and the transition paragraph.
5. Cross-references are solid (Section~\ref{subsec:weighting}, \S\ref{sec:objectives}).

### Claims to Verify (new additions to pending_verify)
6. **REOPOLD 6.7–12× sample efficiency + 7B matches 32B + 3.3× speedup** — source: 2603.11137. Not yet verified.
7. **RLKD 0.1% data surpasses SFT-RL** — source: 2505.16142. Not yet verified.
8. **Lightning OPD 4× speedup** — source: wu2026lightning. Not yet verified.
9. **DistiLLM-2 asymmetric objectives "consistent improvements"** — source: 2503.07067. Vague claim, should verify at least direction.

### Potential Overclaims
10. "mathematically equivalent to policy gradient RL" (MiniLLM) — this is correct but the word "equivalent" is strong. It's an equivalence under specific assumptions (log-derivative trick, infinite samples). Acceptable as-is since the derivation is shown.
11. "no fixed divergence is ever optimal" (end of §4.2) — strong universal claim. The evidence supports it for the tested settings (math reasoning + open-ended generation) but may not hold for all tasks. Consider adding "across tested settings" qualifier.

### Style Issues
12. The paragraph starting "The fixed-divergence family faces an inherent limitation..." (line ~719) is quite long. Paragraph is well-structured though — no action needed.
13. No prose semicolons ✅
14. No prose colons in narrative position ✅ (only mathematical definition lead-ins)
15. "novel" appears twice — both in appropriate technical contexts (not marketing)

## Priority Actions for VERIFY round
- REOPOLD numbers (2603.11137)
- "no fixed divergence is ever optimal" — check if ToDi/AKL/EA papers qualify this
- RLKD 0.1% claim (2505.16142)

## Priority Actions for POLISH round
- Replace 2× sentence-initial "However"
- Consider qualifying "no fixed divergence is ever optimal" with "across evaluated settings"
