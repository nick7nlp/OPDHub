# Round 24 — Applications (§8) — VERIFY

**Date**: 2026-05-09T07:18Z
**Section**: §8 Applications, Systems, and Emerging Domains
**Mode**: VERIFY

## Claims Verified This Round

### 1. KAT-Coder-V2: 79.6% on SWE-bench Verified ✅ CORRECT
- **Source**: arXiv:2603.27703 (ADS abstract confirms "79.6% on SWE-bench Verified")
- **Context**: Paper also reports 88.7 on PinchBench, 46.8 Terminal-Bench Hard, 93.9 tau²-Bench
- **Status**: VERIFIED

### 2. Nemotron-Cascade 2: Gold Medal on IMO/IOI/ICPC + 20× fewer params ✅ CORRECT
- **Source**: https://research.nvidia.com/labs/nemotron/nemotron-cascade-2/
- **Exact quote**: "the second open-weight LLM, after DeepSeek-V3.2-Speciale-671B-A37B, to achieve Gold Medal-level 🏅 performance in the 2025 IMO, IOI, and ICPC World Finals, demonstrating remarkably high intelligence density with 20× fewer parameters"
- **Math**: 671B total / 30B total ≈ 22× (rounded to 20× in their paper)
- **Status**: VERIFIED

### 3. H100 NVLink: 900 GB/s ✅ CORRECT
- **Source**: NVIDIA official H100 product page (nvidia.com/en-us/data-center/h100/)
- **Exact quote**: "fourth-generation NVLink, which offers 900 gigabytes per second (GB/s) of GPU-to-GPU interconnect"
- **Note**: This is bidirectional bandwidth for H100 SXM5 NVLink (18 links × 25 GB/s × 2 directions = 900 GB/s)
- **Status**: VERIFIED

### 4. VOLD: Qwen2.5-VL-3B → MMMU-Pro improvement ⚠️ PARTIALLY VERIFIED
- **Source**: arXiv:2510.23497v2 HTML
- **Confirmed**: Paper uses Qwen2.5-VL-3B as student, evaluates on MMMU-Pro, reports "significant" improvements
- **Specific numbers (27.1% → 32.0%)**: Not visible in available HTML (results table truncated). Numbers are plausible given the paper's claims of state-of-the-art improvement.
- **Status**: PLAUSIBLE (model+benchmark confirmed, exact numbers from results table not reachable in HTML)

## Remaining in Queue (for next VERIFY round)
- Skill-SD: +14.0% over GRPO on AppWorld, +10.9% on Sokoban

## Summary
- 3 claims fully verified ✅
- 1 claim partially verified (model/benchmark confirmed, exact numbers plausible but table not accessible)
- 1 claim deferred to next round
- No corrections needed to main.tex this round
