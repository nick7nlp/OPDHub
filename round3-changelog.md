# Round 3 Changelog — OPD Survey Narrative Improvements

Date: 2026-04-19

## Overview

Third-round deep rewrite focusing on adding recursive structure, cross-section connectivity,
and analytical depth to the sections that still showed "method list" characteristics.
Primary focus areas: §6 Understanding OPD, §5.1 Privileged Information, §8 Open Problems,
and transition paragraphs throughout.

---

## 1. §1 Introduction — Roadmap Paragraph Rewrite

**What changed:** The final roadmap paragraph was rewritten to explain *why* the section ordering is meaningful rather than merely listing what each section covers.

**Why:** The original roadmap was a neutral summary ("Section X covers Y"). The revision adds analytical commentary: §4's subsections address cumulative challenges (each subsection addresses a failure mode revealed by the previous), §5's three subsections trace an arc from richest to most minimal signal, §6 shows how success conditions and failure modes share theoretical roots.

**Main thread:** The roadmap now argues a structural thesis: the paper is not an alphabetical survey but a causally organized argument about why on-policy training works and when it doesn't.

---

## 2. §5 Self-Distillation — Section Introduction Rewrite

**What changed:** The section introduction was substantially expanded to introduce the three subsections (Privileged Information, Self-Play, External Feedback) as a logical progression rather than independent categories.

**Why:** Original intro used neutral labels without explaining the relationship between categories. The revision frames the three subsections as an arc from "richest internal signal" (PI with ground truth) through "most minimal signal" (pure self-play, accepting saturation risk) to "external grounding" (environmental feedback that breaks saturation). This arc reflects the fundamental tension in self-distillation: the most saturation-resistant methods are also the most dependent on external signals.

**Main thread:** Information richness → minimalism → environmental grounding. The tension is that independence from external signals creates vulnerability to saturation.

---

## 3. §5.1 Privileged Information — Deep Rewrite

**What changed:** Complete restructuring of the subsection with:
- Added a framing paragraph that describes the "expanding arc" of what counts as privileged information
- Added cross-references connecting OPSD's cliff-prompt problem to PACED's gradient SNR analysis (§4.2)
- Added explanation of how GATES's consensus gating serves the same functional role as SCOPE's rollout routing
- Added connection showing how OPSDC's conciseness-PI approach sidesteps the self-play saturation problem (§5.2)
- Added a closing insight noting that PI-based methods can, in specific dimensions, surpass teacher-guided distillation

**Why:** Original subsection described four methods in sequence without explaining how they relate to each other or to the broader teacher-guided section. The revision shows that: (a) HDPO patches a vulnerability left open by OPSD; (b) GATES generalizes OPSD's insight while introducing a new problem OPSD avoids; (c) the theoretical framework of \citet{2602.04942} unifies both; (d) OPCD/OEL extend the PI concept temporally; (e) OPSDC exploits a structural gap unreachable by pure self-play.

**Main thread:** Expanding arc of PI from factual ground-truth → contextual cues → behavioral priors → deployment-time efficiency targets. Each step expands reach while introducing new reliability challenges.

---

## 4. §5.2 Self-Play — Added Closing Transition

**What changed:** Added a closing sentence after the SSD/minimalist section that (a) states the fundamental insight (diversity from sampling is sufficient when base model is capable) and (b) explicitly names the boundary of pure self-play (bounded by pre-training distribution information) to motivate the External Feedback section.

**Why:** Original subsection ended abruptly. The transition makes the logical necessity of external feedback clear.

---

## 5. §5.3 External Feedback — Added Closing Transition

**What changed:** Added a closing paragraph after SSB that (a) summarizes the arc from SD-ZERO through RLSD/SDPO/SRPO as increasing coupling between self-distillation and environmental grounding, and (b) explicitly raises the saturation stability question to motivate the saturation analysis section.

**Why:** The saturation analysis was previously a section that appeared without a motivating question. The transition creates narrative demand.

---

## 6. §5 Saturation Analysis — Added Cross-Reference to §6

**What changed:** Extended the closing sentence of the epistemic verbalization failure mode with a cross-reference connecting self-distillation's calibration degradation to the teacher uncertainty problem in §6.2/§6.3, noting that both pathologies share the same root cause (suppression of distributional uncertainty).

**Why:** Epistemic verbalization degradation and teacher overconfidence were analyzed independently in two different sections. The cross-reference reveals their structural unity and foreshadows the §6 theoretical synthesis.

---

## 7. §6 Understanding OPD — Section Introduction Rewrite

**What changed:** The section introduction was completely rewritten. Original: brief statement that §6 covers the "why and when" of OPD. New version: explicitly explains that the four subsections (Success Conditions → Failure Modes → Theory → On-vs-Off) form a *cumulative argument*, not independent analyses.

**Why:** Previously read as four parallel topics. Revision makes the logical dependency explicit: success conditions identify preconditions that theory must explain; failure modes motivate the specific algorithmic choices (adaptive divergences, curriculum weighting, hybrid RL) that the theory grounds; both inform the cost-benefit analysis.

**Main thread:** The four §6 subsections are not independent perspectives but a single cumulative argument from preconditions → failure diagnosis → theoretical explanation → practical implications.

---

## 8. §6.1 Success Conditions — Added Closing Insight

**What changed:** Added a closing paragraph that (a) distills the key principle (OPD benefit scales with the "exploitable gap"), (b) identifies the productive regime between too-small and too-large gaps, and (c) explicitly links this to the failure-mode analysis that follows.

**Why:** Original subsection ended with a finding about trajectory-depth degradation without synthesizing a principle or transitioning. The revision provides both.

---

## 9. §6.2 Failure Modes — Rewritten Introduction + Added Cross-Reference

**What changed:** 
- Rewrote the introductory paragraph to explicitly contrast failure modes (mechanistic, can arise even when preconditions hold) with success conditions (structural, about configuration choices)
- Added cross-reference connecting the "unreliable teacher guidance" failure mode to SCOPE's "flawed prefix trap" in §4.2
- Added explanation distinguishing adaptive divergence approaches (which divergence to use) from this work's trust-in-teacher approach (whether to use teacher guidance at all)

**Why:** Original intro was a generic statement. The revision makes the analytical role of the failure-mode subsection explicit within §6's cumulative argument structure.

---

## 10. §6.3 Unified Theoretical Perspectives — Rewritten Introduction

**What changed:** Replaced the generic "several recent works provide theoretical frameworks" intro with a substantive framing paragraph that:
- Raises the question: do success conditions and failure modes share a common theoretical explanation?
- Answers: yes, both arise from the geometry of teacher-student divergence
- Identifies the theoretical payoff: reduces overwhelming algorithmic diversity to a small number of interpretable design decisions

**Why:** Original intro was neutral. The revision positions the theory subsection as providing the *explanation* for the patterns in §6.1 and §6.2.

---

## 11. §6.3 Theory Section — Rewritten Closing Paragraph

**What changed:** The closing paragraph (which previously stated the general insight about OPD/RL/preference optimization being points on a spectrum) was extended with:
- A connection between different failure modes and different regions of the theory's parameter space
- Explicit identification of how flawed-prefix trust failures and gradient anisotropy failures correspond to specific theoretical subproblems
- Transition that positions §6.4 as the practical application of the theoretical insights

**Why:** Original closing was generic. Revision makes the theoretical section "earn" its position by using it to explain §6.2's failure modes and motivate §6.4.

---

## 12. §8 Open Problems — Section Introduction + Connective Tissue

**What changed:** 
- Added a new framing paragraph explaining that the 8 open directions are not independent but form a "logically connected agenda": scaling laws determine when OPD is worth investing in; teacher calibration and curriculum design determine the ceiling; vocabulary mismatch limits applicability; agentic/multimodal extensions expand the domains; privacy and distillation-RL closure address deployment constraints
- Added bridging sentences between each paragraph to link consecutive directions:
  - Scaling laws → Teacher Calibration: "scaling laws determine when to invest; teacher calibration determines the quality ceiling"
  - Teacher Calibration → Dynamic Curriculum: "a reliable signal wasted on wrong-difficulty prompts"
  - Dynamic Curriculum → Latent Space: "effective curriculum requires commensurable representation spaces"  
  - Latent Space → Agentic: "vocabulary mismatch is a prerequisite challenge for agentic tool-call schemas"
  - Agentic → Multimodal: "temporal extension and modality extension interact in robot manipulation"
  - Multimodal → Privacy: "both agentic and multimodal deployment occurs in regulated environments"
  - Privacy → RL Loop Closure: "privacy constraints impose structure on distillation-RL alternation"
  - RL Loop Closure → Evaluation: "if the loop never closes, what counts as a valid benchmark?"

**Why:** Original Open Problems read as a wish list of 8 independent items. The revision creates a narrative where each direction motivates the next.

---

## New Cross-Section References Added

| From | To | Nature of Connection |
|------|-----|----------------------|
| §5.1 OPSD cliff-prompt | §4.2 PACED gradient SNR vanishing | Same phenomenon (zero gradient at performance boundary), different solutions (signal augmentation vs. curriculum selection) |
| §5.1 GATES consensus gating | §4.2 SCOPE rollout routing | Same functional role: attenuation of unreliable supervision signals |
| §5.1 OPSDC conciseness-PI | §5.2 Self-play saturation | PI sidesteps saturation by providing structurally different reference policy |
| §5.3 External Feedback closing | §5 Saturation Analysis | Environmental coupling as saturation prevention |
| §5 Saturation Analysis epistemic verbalization | §6.3 Teacher uncertainty | Both pathologies = distributional uncertainty suppression |
| §6.2 Failure modes intro | §4.2 SCOPE flawed prefix trap | Same failure mode identified independently in two sections |
| §6.3 Theory closing | §6.2 Failure modes | Theory subsection explicitly explains failure mode patterns |

---

## Compilation Results

- **Compiler:** pdflatex (run twice for cross-references)
- **Pages:** 49
- **Errors:** 0
- **Warnings:** Only pre-existing minor warnings (font shape unavailable, hyperref token warnings) — none introduced by edits
- **File size:** ~493 KB

---

## Summary of Round 3 Improvements

Round 3 focused on the connective tissue of the paper rather than individual section rewrites. The key insight applied throughout is that "analysis" in a survey means showing how methods relate to each other and how sections explain each other, not just describing what each method does. Specific improvements:

1. §6 Understanding OPD now forms a genuine cumulative argument across its four subsections
2. §5 Self-Distillation now presents its three subsections as a logical arc from richest to most minimal signal, explaining why external feedback is necessary
3. §5.1 Privileged Information now shows OPSD→GATES→\citet{2602.04942}→OPCD→OEL as a genuine progression of relaxation and extension, each addressing limitations of the previous
4. §8 Open Problems now has explicit connective tissue showing each direction motivates the next, converting a wish list into a logical research agenda
5. The Introduction roadmap now explains *why* the section ordering is meaningful
6. Cross-references between §4.2, §5.1, §5.2, §5.3, §5 saturation, and §6 reveal structural connections previously invisible
