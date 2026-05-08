# Round 08 — POLISH §2 Background

**Mode**: POLISH  
**Section**: §2 Background and Unified Math (lines 109–201)  
**Scope**: Line-level prose pass

## Changes Made

1. **L111** "must first formalize" → "formalize" — removed filler imperative
2. **L143** "low moderate temperatures" → "low-to-moderate temperatures" — fixed missing hyphen/clarity
3. **L156** parenthetical list "(small teacher-student gap, ...)" → em-dash-offset appositive "---small teacher-student gap, ...---" — tighter typographic rhythm
4. **L156** "frequently fail in the era of heterogeneous model families" → "frequently fail when distilling across heterogeneous model families" — less grandiose, more precise
5. **L158** "becomes more severe as model scale increases, since..." → "intensifies with model scale." (new sentence) — broke overly long compound sentence
6. **L158** "catastrophic for cross-family (relaxation 1)" → "catastrophic for cross-family transfer (relaxation~1)" — added noun "transfer", non-breaking space
7. **L162** "Standard Knowledge Distillation" → "Standard knowledge distillation" — no mid-sentence capitalization
8. **L168** "under the student's own distribution scales quadratically, bounded by $O(\epsilon T^2)$" → "under the learner's own state visitation scales as $O(\epsilon T^2)$" — tighter wording, "scales as" more standard than "bounded by" (it IS the bound)
9. **L173** "requires nuance" → "demands careful qualification" — stronger, less hand-wavy
10. **L175** "Empirical evidence supports this concern. \citet{ttopd2026} observe that..." → "\citet{ttopd2026} provide direct empirical evidence of this failure." — eliminated filler transition sentence, stronger opening
11. **L175** "directly demonstrating the failure mode predicted by this analysis" → "directly demonstrating the predicted failure mode" — trimmed
12. **L175** "This observation provides the theoretical motivation for" → "This observation motivates" — de-nominalized
13. **L195** GKD long sentence broken into two: separated "JSD performs best on translation tasks" into its own sentence for clarity
14. **L199** "A critical gap in the field is" → "A critical open problem is" — "gap in the field" is overused
15. **L199** "This stands in contrast to" → "This contrasts sharply with" — stronger verb
16. **L201** "remains an open problem (Section~\ref{sec:future})" → "remains open (Section~\ref{sec:future})" — removed redundant "problem" (already said "open problem" earlier)
17. **L201** Merged last two sentences of §2.4: "because each rollout step..." folded into "Each rollout step..." as standalone sentence — clearer paragraph flow

## Verification

- `pdflatex` clean build: 0 errors, 0 undefined control sequences
- No semicolons in prose (only math environments)
- No prose colons (all pre-equation/structural)
- Section still compiles without warnings

## 自评

这轮主要砍了 filler words 和 weak verbs，把几个超长句拆成两句。§2 的信息密度已经很高，prose 层面主要是紧凑化。没有动任何数学内容或 claim。
