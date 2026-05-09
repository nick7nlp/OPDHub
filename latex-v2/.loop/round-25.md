# Round 25 — Applications DEEPEN

**Mode:** DEEPEN  
**Section:** §8 Applications, Systems, and Emerging Domains  
**Focus:** Emerging Domains subsection — strengthening logical flow and eliminating parallel listing

## Changes Made

### 1. Multimodal OPD paragraph (major restructure)
- Added framing question ("can OPD transfer across modality boundaries?") to motivate the subsection
- Reorganized VOLD → Video-OPD/X-OPD/CORD → KEPO into a logical progression:
  - VOLD: establishes cross-modal transfer is possible (text teacher → VLM student)
  - Video-OPD/X-OPD/CORD: extends along two axes (temporal depth, modality self-alignment)
  - KEPO: identifies the prerequisite (dense bootstrapping when initial solve rates ≈ 0)
- Added synthesis paragraph mapping the complete pipeline: KEPO → VOLD → X-OPD/CORD
- Connected VOLD's finding explicitly to what's transferable (reasoning structure, not perceptual grounding)
- Merged X-OPD and CORD discussion to show they share the same insight (intra-model cross-modal self-teaching)

### 2. Embodied intelligence paragraph (major restructure)
- Reorganized from arbitrary listing order to a spectrum: cognitive → planning → motor control
  - HY-Embodied (spatial reasoning, cognitive end)
  - OPD-AV + GUI-SD (planning, intermediate — error compounding through time)
  - VLA-OPD (continuous motor control, physical end)
- Added explicit thesis: OPD becomes MORE critical as we move from cognitive to physical tasks
- Connected distributional mismatch consequences to task physicality (quality degradation → physical failure)
- Added forward-looking synthesis about simulator integration needs

## Compile Result
- 62 pages, 124 citations
- 0 errors, 0 undefined references/citations

## Assessment
The Emerging Domains subsection was the weakest part of §8 — mostly parallel listing of methods without explaining why they appear in this order or what connects them. The DEEPEN pass transforms both major paragraphs from "here are N methods" into "here is a progression along axis X, and here is what it tells us about OPD's requirements."
