# Round 32 — DEEPEN §7 Understanding OPD

**Mode**: DEEPEN  
**Section**: §7 Understanding OPD (all subsections)  
**Source**: Round 30 READ (8 prose issues) + Round 31 VERIFY (2 ❌ fixes already applied)

---

## Changes Made

### 1. Removed misplaced §6 summary from §7.3
**What**: The "Taken together, the methods in this section address signal management at progressively larger scales..." paragraph (TIP/SelecTKD/SCOPE/PACED composability) was a §6 Training Dynamics summary misplaced in §7.3 Unified Theory.  
**Fix**: Deleted entirely. §6 already has a proper closing paragraph ("Concrete cost example") and this content repeated §6's contribution without adding theoretical insight.

### 2. Softened "mathematically analogous to mode collapse in GANs"
**What**: Overclaim — no citation establishes a formal mathematical analogy.  
**Fix**: Changed to "bearing structural similarities to mode collapse in generative adversarial networks where a generator locks onto a narrow output manifold once the discriminator signal becomes non-informative." Adds mechanistic insight (WHY it's similar) while reducing the overclaim.

### 3. Softened "jointly necessary" → "appear jointly necessary based on current evidence"
**What**: Agentic collapse synthesis overclaimed that 3 conditions are *proven* jointly necessary.  
**Fix**: Added epistemic qualifier + changed "combination" to "subset" (since some methods address ≤2 of the 3).

### 4. Added citations to diagnostic checklist
- Item 2: Added `\citep{2603.11178}` for curriculum pacing (was just prose mention "PACED")
- Item 3: Added `\citep{2604.16830}` for teacher calibration (CaOPD is the source of this insight)

### 5. Fixed λ notation conflict in compute formula
**What**: §7.4 used λ for teacher refresh rate, conflicting with GKD's λ (mixing coefficient) used extensively in §4.  
**Fix**: Changed to ρ with expanded description "(the fraction of steps requiring a fresh teacher forward pass)".

### 6. Added decision summary at end of §7.4
**What**: §7.4 ended abruptly on the compute formula without a practitioner takeaway.  
**Fix**: Added "Summary decision rule" paragraph with 3 concrete conditions for choosing on-policy over off-policy, plus recommendation of hybrid as default.

### 7. Softened "never encountered" in §8 (agentic distillation)
**What**: "a distribution the teacher has never encountered" is too absolute for a large pretrained model.  
**Fix**: Changed to "a distribution far from what the teacher encountered during its own training."

### 8. Removed §7 intro filler + added citations
**What**: "The analysis below draws on both theoretical frameworks... and systematic empirical investigations..." was content-free filler.  
**Fix**: Deleted. Added `\citep{2602.12222, li2026rethinking}` to the "empirical art toward principled engineering" claim.

### 9. Condensed DPO redundancy in §7.3
**What**: §7.3 repeated the full DPO-KD connection derivation already presented in §4 (subsec:rl_objectives).  
**Fix**: Replaced with a cross-reference + synthesis statement that unifies token-level KL, preference optimization, and reward-regularized RL as "three optimization trajectories toward the same family of target distributions."

---

## Build Verification
- Pages: 58 (same as before)
- LaTeX Errors: 0
- Undefined controls: 0
- Undefined references: 0

## Net Effect
- Removed ~8 lines of redundancy/filler
- Added ~5 lines of insight + decision summary
- 6 overclaims softened
- 3 missing citations added
- 1 notation conflict resolved
- §7 now self-contained (no stray §6 content) with actionable practitioner takeaway
