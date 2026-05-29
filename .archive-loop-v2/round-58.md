# Round 58 — POLISH — §2 Background

## Changes

Line-level prose polish pass on §2 (lines 109–206).

### Prose colons removed (2)
1. "The DAgger bound predicts something strictly worse: because..." → split into two sentences with period
2. "amenable to on-policy optimization: because the sampling distribution..." → rewritten as "precisely what makes them amenable to on-policy optimization. The sampling distribution..."

### Paragraph break added (1)
- GKD paragraph (was ~10 lines, single block) — split after divergence comparison into a new paragraph starting "A striking empirical finding is that..." to improve readability

### Punctuation tightened (1)
- "discards all information about...alternative modes, a critical limitation" → em-dash "---a critical limitation" (appositive, clearer boundary)

### Verb repetition fixed (1)
- DistiLLM: "employs an adaptive scheduler" → "uses an adaptive scheduler" (MiniLLM already uses "employs")

## Build verification
- pdflatex: ✅ 59 pages, 0 errors, 0 undefined
- No semicolons in §2 prose
- No remaining prose colons in §2

## Notes
- 整个 §2 现在 prose colon-free，且段落长度更合理
- GKD 那段拆开后读起来轻松多了，后半部分 "sampling policy matters more than divergence choice" 现在独立出来更有 punch
