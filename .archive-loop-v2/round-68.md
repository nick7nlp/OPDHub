# Round 68 — DEEPEN on §4-Objectives

**Mode:** DEEPEN  
**Section:** §4 Objective Functions and Optimization  
**Time:** 2026-05-09T04:37Z  

## Changes Made

### 1. Strengthened Fixed→Adaptive bridge (line ~705)
- Added explanation of *why* the mismatch is fundamental rather than just engineering: "not merely an efficiency concern but a fundamental misalignment between the geometry of the loss and the geometry of the target distribution"
- Clarified the concrete reasoning for each divergence's failure mode (mode-seeking optimal for math operators because student must commit; mode-covering optimal for fillers because any synonym suffices)
- Noted that the compromise compounds across sequence length

### 2. Added comparative insight between ToDi and Entropy-Aware OPD
- New paragraph after "confirming that the optimal divergence is indeed position-dependent" explains complementarity:
  - ToDi: conditions on teacher-student gap (pairwise property) → adapts more when student is far
  - Entropy-Aware: conditions on teacher uncertainty alone (marginal property) → stable signal independent of student quality, better for early training
- AKL repositioned as synthesizing elements of both approaches rather than just "more aggressive"

### 3. Strengthened token-level/sequence-level → RL bridge
- Added forward reference to §4.3 RL-augmented methods: "whose resolution foreshadows the RL-augmented methods"
- Added key insight: MiniLLM is already doing policy gradient RL → sequence-level distillation and RL-augmented distillation are not distinct paradigms but endpoints of a continuum parameterized by reward source
- This explicitly connects the three subsections as a unified progression

### 4. Strengthened G-OPD theoretical consequence
- Replaced generic "shared analytical language" with explicit unification: all objectives in the section are special cases of KL-constrained policy optimization with different reward definitions and constraint strengths

## Compilation
- ✅ 0 errors, 60 pages
- Cross-references intact

## Assessment
§4 now has stronger logical cohesion:
- Fixed → Adaptive: explicitly motivated by geometry mismatch
- Adaptive methods: compared by *what signal they condition on* (pairwise vs marginal)
- Token-level → Sequence-level → RL: unified as a single continuum
- G-OPD equivalence: ties the whole section together as special cases of one framework
