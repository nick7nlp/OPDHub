# Round 13 — POLISH §3.1 Method Landscape

**Mode**: POLISH  
**Section**: §3.1 Method Landscape (prose paragraphs after taxonomy figure)  
**Date**: 2026-05-08 18:11 UTC  
**Input**: round-12 DEEPEN output

## Changes Made

### Paragraph 1 (pipeline grounding)

| Before | After | Reason |
|--------|-------|--------|
| "reflects the actual engineering workflow of state-of-the-art systems" | "reflects how state-of-the-art systems are actually built" | Tighter; avoids nominalisation "engineering workflow" |
| "then decides on cold-start data from DeepSeek-V3 as the signal source" | "then uses cold-start data from DeepSeek-V3 as its signal source" | "decides on X as Y" is awkward phrasing; "uses" is direct |
| "address the training dynamics challenges that arise from the chosen combination" | "address the dynamics challenges arising from that combination" | Cut "training" (redundant with §6 framing); participle tighter than relative clause; "that" → shorter |

### Paragraph 2 (interdependence)

| Before | After | Reason |
|--------|-------|--------|
| "RL-augmented objectives (G-OPD) naturally pair with external feedback signal sources" | "RL-augmented objectives such as G-OPD naturally couple with external feedback sources" | (a) Eliminated "pair...pair most naturally" repetition; (b) "couple" varies the verb; (c) "signal sources" → "sources" (redundant within context) |
| "while fixed divergences pair most naturally with white-box sources where the full distribution is available for exact computation" | "while fixed divergences align with white-box sources that expose the full output distribution for exact computation" | "align" avoids double "pair"; active verb "expose" replaces passive "is available"; "full output distribution" explicit |
| "This interdependence means that choosing an objective implicitly constrains" | "This interdependence implies that an objective choice constrains" | "means that" → "implies that" (more academic); "choosing an objective" → "an objective choice" (nominalised = more concise) |

### Not changed (deliberate)
- Figure caption: already clean, no semicolons/prose colons, informative
- Intro sentence (l.209): already tight and clear
- "Crucially," opener: acceptable academic transition word (not filler)
- Structural colons retained (after "sequence:", "incompatible:", "synergistic:")
- No semicolons found anywhere in §3.1

## Verification
- `pdflatex` single pass: 0 errors, 0 undefined references
- No semantic changes (same meaning, tighter expression)

## Metrics
- Words saved: ~18 (from ~195 → ~177 in two paragraphs)
- Repeated word eliminated: "pair"×2 + "naturally"×2 → "couple" + "align"
- Passive→active: 1 instance ("is available" → "expose")
