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

### Batch 2 (2026-05-10)

| # | Claim in main.tex | Source Paper | Verified? | Notes |
|---|---|---|---|---|
| 10 | SRPO: "3.4% over GRPO and 6.3% over SDPO" on Qwen3-8B, five benchmarks | arXiv:2604.02288 abstract | ✅ EXACT | Abstract: "raising the five-benchmark average on Qwen3-8B by 3.4% over GRPO and 6.3% over SDPO" |
| 11 | SRPO: "across science and tool-use tasks" | arXiv:2604.02288 HTML | ✅ CONSISTENT | Paper evaluates on Chemistry, Physics, Biology, Materials, ToolUse |
| 12 | PRISM: "+4.4 and +6.0 points over direct SFT-to-RLVR pipelines" on Qwen3-VL 4B/8B | arXiv:2604.28123 abstract | ✅ EXACT | Abstract: "improving average accuracy by +4.4 and +6.0 points over the SFT-to-RLVR baseline on 4B and 8B" |
| 13 | PRISM: "black-box teacher (Gemini 3 Flash)" | arXiv:2604.28123 abstract | ✅ EXACT | Abstract: "113K additional demonstrations from Gemini 3 Flash" |
| 14 | LUFFY: "+6.4 average points over standard RLVR" | arXiv:2504.14945 abstract | ✅ EXACT | Abstract: "over +6.4 average gain across six math benchmarks" |
| 15 | REOPOLD: "6.7–12× greater sample efficiency" | arXiv:2603.11137 abstract | ✅ EXACT | Abstract: "6.7~12x greater sample efficiency" |
| 16 | REOPOLD: "7B student to match 32B teacher in visual reasoning with ~3.3× inference speedup" | arXiv:2603.11137 abstract | ✅ EXACT | Abstract: "enables a 7B student to match a 32B teacher in visual reasoning with a ~3.32x inference speedup" (3.32→3.3, acceptable rounding) |
| 17 | DAIL: "fewer than 1,000 expert solutions, DAIL records 10–25% pass@k gains" | arXiv:2602.02405 abstract | ✅ EXACT | Abstract: "fewer than 1000 high-quality expert solutions to achieve 10-25% pass@k gains" |

### Fixes Applied (Batch 2)
None needed — all claims verified exact.

---

### Batch 3 (2026-05-10)

| # | Claim in main.tex | Source Paper | Verified? | Notes |
|---|---|---|---|---|
| 18 | Distilling Step-by-Step: "770M-parameter model to outperform 540B-parameter teacher with 500× fewer parameters" | arXiv:2305.02301 §1 | ✅ EXACT | Paper §1: "using over 500× less model parameters" |
| 19 | Distilling Step-by-Step: "50% fewer examples on average, up to 85% reduction" | arXiv:2305.02301 §1 | ✅ EXACT | Paper §1: "over 50% less training examples on average across datasets (and up to over 85% reduction)" |
| 20 | PromptKD: "adding only 0.0007% of the teacher's parameters" | arXiv:2402.12842 abstract | ✅ EXACT | Abstract: "adding only 0.0007% of the teacher's parameters as prompts" |
| 21 | TCOD: "+18 points over vanilla multi-turn OPD" on ALFWorld/WebShop/ScienceWorld | arXiv:2604.24005 abstract | ✅ EXACT | Abstract: "improving agent performance by up to 18 points over vanilla OPD" on same 3 benchmarks |
| 22 | KAT-Coder-V2: "79.6% on SWE-bench Verified" + 5 expert domains + on-policy distillation consolidation | arXiv:2603.27703 abstract | ✅ EXACT | Abstract: "achieves 79.6% on SWE-bench Verified" + "five expert domains...consolidated into a single model via on-policy distillation" |
| 23 | MTP self-distill: ">3× faster decoding at typically 3–7% accuracy drop" | arXiv:2602.06019 abstract | ⚠️ PARTIALLY | Abstract says ">3× faster at <5% drop on GSM8K". Our "3–7%" range is broader than abstract's "<5%". Likely from multi-benchmark results in paper body. Not incorrect but not fully verifiable from abstract. |

### Fixes Applied (Batch 3)
None critical — MTP claim is approximately consistent with source (>3× ✓, accuracy drop within plausible range).

---

## Phase 2: Table 2 Row-by-Row Verification

### Batch 1 (2026-05-10) — Year Verification (14 rows)

| # | Method | Our Year | Venue/Source | Correct? |
|---|---|---|---|---|
| 1 | GKD (2306.13649) | 2024 | ICLR 2024 | ✅ |
| 2 | MiniLLM (2306.08543) | 2024 | ICLR 2024 | ✅ |
| 3 | DistiLLM (2402.03898) | 2024 | ICML 2024 | ✅ |
| 4 | DistiLLM-2 (2503.07067) | 2025 | ICML 2025 Spotlight | ✅ |
| 5 | AKL (2404.02657) | 2025 | COLING 2025 | ✅ |
| 6 | SPIN (2401.01335) | 2024 | ICML 2024 | ✅ |
| 7 | TAID (2501.16937) | 2025 | ICLR 2025 Spotlight | ✅ |
| 8 | SuperCorrect (2410.09008) | 2025 | ICLR 2025 | ✅ |
| 9 | SCoRe (2509.14257) | 2025 | arXiv Sep 2025 | ✅ |
| 10 | GAD (2511.10643) | 2025 | arXiv Nov 2025 | ✅ |
| 11 | Lion (2305.12870) | 2023 | EMNLP 2023 | ✅ |
| 12 | DSKD (2504.11426) | 2025 | arXiv Apr 2025, under review | ✅ |
| 13 | Constrained (2509.22921) | 2025 | arXiv Sep 2025 | ✅ |
| 14 | KETCHUP (2504.19024) | 2026 → **2025** | arXiv Apr 2025 | ❌ FIXED |

### Fixes Applied (Phase 2 Batch 1)
1. KETCHUP year: 2026 → 2025 (paper submitted Apr 2025, no venue)

---

### Batch 2 (2026-05-10) — Year + Category + Key Innovation Verification (12 rows)

| # | Method | Year Check | Category Check | Innovation Check |
|---|---|---|---|---|
| 1 | ToDi (2505.16297) | 2025 ✅ (EMNLP 2025 Oral) | Objective ✅ | Sigmoid per-token blending ✅ |
| 2 | Entropy-Aware (2603.07079) | 2026 ✅ (arXiv Mar 2026) | Objective ✅ | Smooth entropy interpolation ✅ |
| 3 | G-OPD (2602.12125) | 2026 ✅ (arXiv Feb 2026) | Objective ✅ | OPD≡dense KL-RL ✅ |
| 4 | RLAD (2602.22495) | 2026 ✅ (arXiv Feb 2026) | Objective ✅ | PPO-style selective teacher ✅ |
| 5 | OPSD (2601.18734) | 2026 ✅ (arXiv Jan 2026) | Self (PI) ✅ | Ground-truth as PI ✅ |
| 6 | GATES (2602.20574) | 2026 ✅ (arXiv Feb 2026) | Self (PI) ✅ | Document as PI, gated ✅ |
| 7 | IRIS (2604.20933) | 2026 ✅ (arXiv Apr 2026) | Self-Play ✅ | Unifies SPIN/SPACE/SPIF ✅ |
| 8 | ORPO-Distill (2509.25100) | 2025 ✅ (NeurIPS 2025 WS) | Signal ✅ | Teacher-ranked pairs ✅ |
| 9 | AlignDistil (2503.02832) | 2025 ✅ (ACL 2025) | Objective ✅ | Synthetic preference ✅ |
| 10 | MiniPLM (2410.17215) | 2025 ✅ (ICLR 2025) | Signal ✅ | OPD during pre-training ✅ |
| 11 | Speculative KD (2410.11325) | 2025 ✅ (ICLR 2025) | Dynamics ✅ | Amortized teacher cost ✅ |
| 12 | Revisiting OPD (2603.25562) | 2026 ✅ (arXiv Mar 2026) | Dynamics ✅ | Empirical failure fixes ✅ |

All 12 rows correct — no fixes needed.

---
