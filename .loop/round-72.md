# Round 72 — VERIFY §5 Signal Source

**Mode:** VERIFY  
**Section:** 5-Signal-Source  
**Time:** 2026-05-09 05:00 UTC

## Claims Verified

### 1. MTP <5% drop (2602.06019) — from pending_verify

**Survey text:** "achieving >3× faster decoding at typically 3–7% accuracy drop (model-dependent)"  
**Paper abstract:** "more than 3× faster at <5% drop in accuracy on GSM8K"  
**Paper intro:** "between 2× and 5× acceleration with minimal impact on generation quality"

**Verdict:** CONSISTENT. The abstract headline "<5% on GSM8K" is a single-benchmark cherry-pick. The survey's "3–7% model-dependent" is a fair characterization of the full results across models/benchmarks (the paper shows variation across Qwen3-4B/8B/14B models). The >3× speedup claim is exact match. No change needed.

### 2. CRISP 57–59% token reduction + 9–16pp accuracy (2603.05433)

**Survey text:** "reducing chain-of-thought token count by 57–59% on MATH-500 while improving accuracy by 9–16 percentage points"  
**Paper abstract:** "57–59% token reduction on MATH-500 while improving accuracy by 9–16 points absolute"

**Verdict:** EXACT MATCH. ✅ No change needed.

### 3. SSD Qwen3-30B-Instruct 42.4% → 55.3% LiveCodeBench v6 (zhang2026embarrassingly / 2604.01193)

**Survey text:** "SSD improves Qwen3-30B-Instruct from 42.4% to 55.3%"  
**Paper abstract & multiple sources:** "SSD improves Qwen3-30B-Instruct from 42.4% to 55.3% pass@1 on LiveCodeBench v6"

**Verdict:** EXACT MATCH. ✅ No change needed.

## Summary

All 3 claims verified accurate. No edits to main.tex required this round.

## Pending Verify Update

- Removed: "MTP <5% drop clarification (actually 3-7% by model)" — verified consistent
- Remaining queue: 11 items (see state.json)

## Next Round

Round 73: DEEPEN on §5 — strengthen transition between §5.2 and §5.3, add conceptual bridge.
