# Round 5 — VERIFY — Background (pending_verify queue)

## Claims Verified

### 1. TT-OPD KL numbers (ttopd2026) — ✅ VERIFIED
- **Claim**: "KL divergence dropping from 2.637 to 0.343 at a single teacher-reset event"
- **Source**: arXiv:2605.02943 (Healthcare AI GYM / TT-OPD paper)
- **Evidence**: Paper Section 6.1 states: "at each copy event, the KL divergence drops abruptly from its accumulated value to near zero (e.g., 2.637→0.343 at step 10 with T=30)"
- **Result**: Numbers exactly match. No correction needed.
- **Note**: BibTeX title "HEALTHCARE AI GYM for Medical Agents" is the actual paper title (paper contributes both the gym AND TT-OPD method). No bib fix needed.

### 2. MiniLLM α=0.2 (2306.08543) — ✅ VERIFIED
- **Claim**: "MiniLLM uses alpha=0.2 for mixture policy stability"
- **Source**: arXiv:2306.08543v6 (MiniLLM, ICLR 2024)
- **Evidence**: Section 3.1 states "We set the teacher-mix-in strength α=0.2 throughout the experiments in Eq. 4"
- **Notation check**: Paper defines `p̃ = α·p_teacher + (1-α)·q_student` with α=0.2 → 20% teacher + 80% student. Survey writes `(1-α)p_θ + α·p_teacher` which with α=0.2 gives the same 20%teacher+80%student. ✅ Consistent.
- **Result**: Correct. No correction needed.

### 3. DistiLLM formula direction (2402.03898) — ✅ VERIFIED (notation difference acknowledged)
- **Claim**: "DistiLLM computes KL(p_teacher || p_tilde) with p_tilde = alpha*p_teacher + (1-alpha)*p_student"
- **Source**: arXiv:2402.03898v2 (DistiLLM, ICML 2024)
- **Evidence**: Paper defines `D_SKL^(α)(p, q_θ) = D_KL(p, (1-α)p + α·q_θ)` where α is the student weight
- **Survey's notation**: Uses α as teacher weight → `KL(teacher || α·teacher + (1-α)·student)`. Mathematically identical (α_survey = 1 - α_paper).
- **Line 193 description**: "computing KL(p_teacher || p̃) ... p̃(y) ≥ α·p_teacher(y) > 0 always" — correct reasoning
- **Line 585 formula**: `KL(p_teacher || α·p_teacher + (1-α)·p_θ)` — consistent with description
- **Result**: Mathematically correct. Notation choice is internally consistent within the survey. No correction needed.

## Summary
All 3 pending_verify items resolved as VERIFIED. No corrections to main.tex required this round. Background section's numerical claims and formula directions are accurate.

## Next
Queue is empty. Advance to DEEPEN mode on Background section (current_section_idx=1).
