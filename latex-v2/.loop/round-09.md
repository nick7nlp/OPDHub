# Round 9 — READ: §3 Landscape and Practitioner Guide

**Mode**: READ  
**Section**: Landscape and Practitioner Guide (lines 211–579)  
**Time**: 2026-05-09T06:03Z

## Findings

### Numbers to Fix (VERIFY not needed — direct count)
1. **Line 348 "16 representative methods"** — Table 1 (method_comparison) has 15 entries, not 16
2. **Line 346 "64 methods"** — Table 2 (white_box_comparison) has 61 entries, not 64

### AI-taste Words
3. **Line 334 "Crucially"** — sentence opener AI filler
4. **Line 336 "reveals a clear evolutionary trajectory"** — "reveals" is AI-taste

### Claims to Verify (→ pending_verify)
5. **CRISP "57% token reduction, +9% accuracy"** — In Table 2 Key Innovation column. Need to verify against CRISP paper (2603.05433)

### Observations (no action needed)
- Table 1 semicolon "DAgger for LLMs; interpolation" is in a table cell, not prose — allowed
- "however" in line 336 is mid-sentence, acceptable
- Self-distillation 30% (=18/61=29.5%) — acceptable rounding
- Tree badge counts (5+3+11+10+10+26+4+6+3=78) intentionally exceed Table 2 (61) because tree counts all methods *discussed* in each subsection including methods that appear as secondary contributions
- Prose quality overall good — clear progression from pipeline overview → tables → decision tree
- No prose semicolons or dashes found
- Decision tree is well-structured and actionable

## Next
- VERIFY: Fix count errors (15 and 61), fix AI-taste words
- Queue CRISP claim for pending_verify
