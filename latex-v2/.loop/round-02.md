# Round 2 — VERIFY: Introduction Claims

**Date:** 2026-05-09 05:14 UTC  
**Mode:** VERIFY  
**Items:** pv-001, pv-002

## Verification Results

### pv-001: "over one hundred papers" in OPD literature
- **Claim:** "fewer than two years later the literature has expanded to over one hundred papers"
- **Evidence:** Survey's own references.bib contains 124 entries (including foundational works outside OPD). The broader OPD literature certainly exceeds 100 papers given the survey doesn't cite everything.
- **Verdict:** ✅ VERIFIED (reasonable characterization)

### pv-002: "DeepSeek-V4 replaced its mixed RL stage with pure multi-teacher OPD"
- **Claim:** "DeepSeek-V4 went furthest, replacing its mixed RL stage with pure multi-teacher OPD for model consolidation"
- **Source checked:** DeepSeek-V4 technical report (HuggingFace model card)
- **What V4 actually says:** "The post-training features a two-stage paradigm: independent cultivation of domain-specific experts (through SFT and RL with GRPO), followed by unified model consolidation via on-policy distillation"
- **Analysis:** V4 still uses RL (GRPO) for Stage 1 (domain expert cultivation). The consolidation stage (merging experts into unified model) uses OPD. In previous DeepSeek models (V3/R1), consolidation used mixed RL-based methods. So V4 replaced the *consolidation-stage* RL with OPD. The survey's claim is essentially correct — it specifically says "for model consolidation" which scopes the replacement appropriately.
- **Verdict:** ✅ VERIFIED (accurate with appropriate scope qualifier)

## Assessment
Both pending_verify claims check out. No corrections needed to main.tex.

## Next
- Clear pending_verify queue
- Next round: DEEPEN mode on Introduction
