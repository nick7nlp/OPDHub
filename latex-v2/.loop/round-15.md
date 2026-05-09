# Round 15 — DEEPEN — §4 Objective Functions and Optimization

## What Was Done

Strengthened inter-method logical connections in the RL-Augmented Objectives subsection (§4.3). The section had three blocks of methods (joint optimization, preference-based, error localization) that read somewhat as parallel listings with abrupt transitions. DEEPEN edits:

1. **RLKD bridge sentence**: Added opening connector showing how RLKD relates to G-OPD/REOPOLD (progression from token-level KL → variance-reduced token rewards → step-level structural matching as increasing abstraction of "teacher knowledge").

2. **Joint vs Sequential paragraph**: Added explicit framing explaining why joint optimization is needed given the KD+RL complementarity established above. Added KDRL→RLAD progression analysis (uniform regularization → selective trust region mirrors Fixed→Adaptive divergence evolution).

3. **New bold heading "Preference-based objectives as implicit RL"**: Separated DPO methods into their own logical unit with a unifying insight paragraph explaining how token-level KL, step-level structure, and sequence-level preference are all KL-constrained policy optimization at different abstraction levels.

4. **New bold heading "Fine-grained credit assignment"**: Separated SuperCorrect/SCoRe into their own logical unit, framed as addressing the supervision uniformity limitation shared by all prior methods. Added contrast with RLKD (global structural reward vs. local error correction) and flagged their composition as unexplored.

## Findings

- The section's logical flow now follows a clear progression:
  - G-OPD → REOPOLD (dense token-level reward, stabilization)
  - → RLKD (step-level structural matching, abstraction)
  - → KDRL/RLAD (joint optimization, uniform→selective)
  - → AlignDistil/OVD/PBSD (preference as implicit RL)
  - → SuperCorrect/SCoRe (fine-grained credit assignment)
  - → X-KD/TSD-KD (environment reconstruction frontier)
- No factual claims added; all new text is analytical synthesis/connection.
- No AI-taste words introduced (checked: no however/moreover/furthermore/notably).

## Compilation

- 61 pages, 124 bibs, 0 errors, 0 undefined refs/cites
- Clean second pass (cross-references resolved)
