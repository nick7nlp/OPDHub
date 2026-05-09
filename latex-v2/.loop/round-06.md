# Round 6 — DEEPEN — Background (§2)

**Time**: 2026-05-09 05:40 UTC  
**Mode**: DEEPEN  
**Section**: Background and Unified Math

## Changes Made

### 1. Strengthened Seq-KD → exposure bias transition (§2.1 end)
- Replaced generic "critical limitation that motivates softer distributional matching methods below" with an explicit two-pronged diagnosis: (a) loss of distributional richness, (b) off-policy training disconnect
- Made the connection to §2.2 mechanistically clear rather than just signposting

### 2. Added bridging paragraph at §2.2 opening
- New 2-sentence lead-in connecting the token-level loss's conditioning on ground-truth prefixes to the distribution mismatch at inference
- Gives the reader a clear "why this matters" before the formalism

### 3. Comparative synthesis paragraph after GKD/MiniLLM/DistiLLM (§2.3)
- Added "Comparative synthesis" paragraph drawing out the tradeoff triangle:
  - GKD: generality + simplicity, but no divergence guidance
  - MiniLLM: precision via Reverse KL, but REINFORCE variance
  - DistiLLM: numerical stability by construction, but hyperparameter/engineering complexity
- Frames the three methods as a progression from algorithmic simplicity to engineering sophistication

### 4. Scaling Laws subsection transition (§2.4)
- Replaced generic "critical open problem" opening with a logical bridge from the f-divergence framework ("what to optimize") to scaling ("how performance scales")
- Added explicit connection between capacity-gap phenomenon and Forward/Reverse KL behavior
- Added label `\label{subsec:f-div}` to the f-divergence subsection for cross-referencing

## Compilation
- ✅ 0 errors, 60 pages, 2-pass clean (no undefined refs)

## Assessment
The Background section now reads as a cohesive argument rather than four adjacent subsections. Each transition carries explicit logical motivation:
- §2.1 → §2.2: "static prefixes create mismatch at inference"
- §2.2 → §2.3: "on-policy resolves bias; the divergence choice governs geometry"
- §2.3 → §2.4: "framework tells us what; scaling tells us how much"
- GKD/MiniLLM/DistiLLM: no longer just described in parallel but explicitly contrasted as solving each other's failure modes
