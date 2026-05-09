# Round 20 — §6 Training Dynamics and Efficiency — DEEPEN

## Task
Strengthen inter-method logical connections and add cross-section synthesis to §6 (Training Dynamics and Efficiency).

## Changes Made

### 1. Uni-OPD transition (§6.2)
- **Before:** Uni-OPD introduced independently as "identifies two bottlenecks"
- **After:** Explicitly positioned as extending PACED's single-criterion (pass rate) by arguing it conflates capability gaps vs. subtle quality failures, motivating the dual-criterion upgrade
- **Why:** Makes the PACED→Uni-OPD progression read as intellectual refinement rather than parallel listing

### 2. TCOD transition (§6.2)
- **Before:** "While the above curricula operate along the difficulty axis..."
- **After:** Explicitly names PACED, Uni-OPD, and self-adjusting methods as all operating on difficulty, then positions TCOD as opening an orthogonal (temporal depth) axis
- **Why:** Clarifies that TCOD is not "another curriculum method" but addresses a fundamentally different dimension

### 3. §6.2→§6.3 transition (Compute Optimization intro)
- **Before:** "OPD requires generating student rollouts and scoring them... Several methods target this bottleneck."
- **After:** Explicitly connects back to §6.1 and §6.2, explaining that weighting improves sample efficiency and curriculum avoids wasteful rollouts, but neither eliminates the systems-level cost bottleneck — which §6.3 addresses orthogonally
- **Why:** Makes the three subsections read as complementary layers rather than independent topics

### 4. Added "Training Efficiency Stack" synthesis (end of §6.3)
- New paragraph at section end synthesizing all three subsections into a composable layered architecture:
  - Layer 1 (Token weighting): gradient-level noise elimination
  - Layer 2 (Curriculum): sampling-level waste elimination  
  - Layer 3 (Compute optimization): systems-level overhead reduction
- Argues these layers are complementary (not substitutive) and that composing all three can compound 2-4× individual gains toward near-parity with off-policy cost

## Compilation
- ✅ 0 errors, 0 undefined refs, 0 undefined cites
- 62 pages, 124 bibliography entries

## Assessment
Section §6 was already strong on individual method analysis and had good intra-subsection synthesis (especially the "design spectrum" paragraph in §6.1 and the "fidelity-efficiency frontier" in §6.3). The main gap was inter-subsection connections — the three subsections read as somewhat independent topics rather than a unified efficiency framework. The edits address this by:
1. Making method-to-method progressions explicit within §6.2
2. Adding a cross-subsection bridge at the §6.2→§6.3 transition
3. Providing a capstone synthesis paragraph that frames the entire section as a composable stack
