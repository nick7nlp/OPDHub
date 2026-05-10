# Verification Results — OPD Survey V2

## Phase 1: Numerical Claims Deep Verification

### Batch 1 (2026-05-10)

| # | Claim in main.tex | Source Paper | Verified? | Notes |
|---|---|---|---|---|
| 1 | CRISP: "57–59% token reduction on MATH-500 while improving accuracy by 9–16 points" | arXiv:2603.05433 abstract | ✅ EXACT | Abstract: "57--59% token reduction on MATH-500 while improving accuracy by 9--16 points absolute" |
| 2 | OVD: "+12.9% absolute EM improvement on web QA and +25.7% on math benchmarks" | arXiv:2601.21968 abstract | ✅ EXACT | Abstract: "up to +12.9% absolute improvement in average EM on Web Q&A tasks and a up to +25.7% gain on math benchmarks" |
| 3 | NPD: "8.1× throughput speedup" + "openPangu-Embedded-1B, 68.73%" + "outperforming Qwen3-1.7B" | arXiv:2605.05940 abstract | ✅ EXACT | Abstract: "8.1x speedup over on-policy baselines" + "68.73%, outperforming the substantially larger Qwen3-1.7B" |
| 4 | NPD: "outperforms SFT by +8.09%" | arXiv:2605.05940 abstract | ✅ EXACT | Abstract: "outperforms SFT by 8.09%" |
| 5 | NPD: "Qwen3-1.7B (63.69%)" | arXiv:2605.05940 | ⚠️ UNVERIFIABLE from abstract | Not in abstract; likely from paper's result table. Cannot confirm without full paper access. |
| 6 | SSD: "improves Qwen3-30B-Instruct from 42.4% to 55.3% pass@1 on LiveCodeBench v6" | arXiv:2604.01193 abstract | ✅ EXACT | Abstract: "SSD improves Qwen3-30B-Instruct from 42.4% to 55.3% pass@1 on LiveCodeBench v6" |
| 7 | SCOPE: "+7.3% Pass@32 improvement" | arXiv:2604.10688 abstract | ⚠️ IMPRECISE → FIXED | Paper says "average **relative** improvement of ... 7.30% in Pass@32". Our text didn't specify "relative". Fixed to "7.3% relative Pass@32 gain". |
| 8 | SD-ZERO: "68.3% on AIME 2024, outperforming GRPO (62.5%)" | arXiv:2604.12002 Table 1 | ✅ EXACT (numbers) / ⚠️ IMPRECISE (metric) → FIXED | Paper reports avg@8, not pass@1. Fixed to "68.3% avg@8 on AIME 2024". |
| 9 | Stable-OPD: "+7.2% over vanilla OPD" | arXiv:2604.08527 abstract | ✅ EXACT | Abstract: "improves performance by 7.2% on average" |

### Fixes Applied
1. Line 963: "+7.3% Pass@32 improvement" → "7.3% relative Pass@32 gain"
2. Line 939: "68.3% on AIME 2024" → "68.3% avg@8 on AIME 2024"

---
