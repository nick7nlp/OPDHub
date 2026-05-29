# Round 36 — VERIFY §8 Applications

**Mode**: VERIFY  
**Section**: §8 (Applications, Systems, and Emerging Domains)  
**Time**: 2026-05-08 22:41 UTC  
**Source**: Round 35 READ issues

---

## Verification Table

| # | Claim | PDF Source | Lines | Verdict | Notes |
|---|-------|-----------|-------|---------|-------|
| 1 | Gemma 2 "27B→9B→2B" implies cascade | 2408.00118.pdf §3.2 | 790, 1095 | ⚠️ MISLEADING | Paper says "we use a large language model as a teacher to train small models, namely 2B and 9B" — both distilled from 27B independently (parallel). Notation "27B→9B→2B" implies sequential cascade which is wrong. |
| 2 | MiMo-V2 "frontier performance on mathematical reasoning" | 2601.02780.pdf abstract | 1095 | ⚠️ OVERCLAIM | Paper says "strong reasoning and agentic capabilities" / "designed for fast, strong reasoning." Never uses "frontier" for math specifically. |
| 3 | Qwen3 "one-tenth of the GPU hours" | 2505.09388.pdf §4.4 | 1095 | ✅ | Paper confirms distillation outperforms RL at ~1/10 GPU cost |
| 4 | Qwen3 "improves pass@64 on AIME where RL does not" | 2505.09388.pdf §4.4 | 1095 | ✅ | Confirmed |
| 5 | Nemotron-Cascade 2 "30B MoE, 3B activated" | 2603.19220.pdf | 1097 | ✅ | Exact match |
| 6 | Nemotron "Gold Medal-level on IMO, IOI, ICPC World Finals" | 2603.19220.pdf abstract | 1097 | ✅ | "gold-medal performance on IMO 2025, IOI 2025 and ICPC World Finals 2025" |
| 7 | Nemotron "20× fewer parameters than DeepSeek-V3.2-Speciale" | 2603.19220.pdf | 1097 | ✅ | Direct quote "with 20× fewer parameters" (30B vs 671B ≈ 22×, paper rounds to 20×) |
| 8 | TCOD "+18 points over vanilla multi-turn OPD" | Previously verified Bundle B | 1110 | ✅ | Max gain +18.67 |
| 9 | VOLD "27.1% to 32.0% on MMMU-Pro" | 2510.23497.pdf Table | 1134 | ✅ | Exact figures confirmed in paper's results table |
| 10 | VOLD "text-only teacher... without ever seeing the image" | 2510.23497.pdf §abstract | 1134 | ✅ | Paper confirms text-only teacher framework |
| 11 | TT-OPD "10 of 18 benchmarks" | ttopd.pdf abstract+conclusion | 1134 | ⚠️ DISCREPANCY | Abstract/conclusion say "10 of 18" but Key Findings §5.2 says "12 of 18". Paper is internally inconsistent. Survey uses "10 of 18" (conservative/abstract figure). Defensible but should note. |
| 12 | TT-OPD "+3.9 pp improvement over non-RL baseline" | ttopd.pdf abstract line 28 | 1134 | ✅ | Exact match: "+3.9 pp improvement over the non-RL baseline" |
| 13 | TT-OPD "3.6K+ tasks, 135 domain-specific tools, 828K medical passages" | ttopd.pdf lines 16-17, 92, 869-871 | 1134 | ✅ | All three numbers confirmed across multiple locations in paper |
| 14 | "~16 GB of logit data per batch" | Calculation check | 1143 | ⚠️ UNDERSPECIFIED | Formula given as [B,T,|V|]×2 bytes but B,T not specified. For 16GB: needs e.g. B=16,T=4096,V=128K → 16.8GB. Plausible config but assumptions unstated. Not wrong per se, but should say "can exceed" rather than stating as exact. |
| 15 | OpenRLHF, veRL, vLLM, TensorRT-LLM (no citations) | N/A | 1143 | ❌ MISSING CITES | All four are published works (OpenRLHF: arXiv 2405.11143; veRL: arXiv 2409.19256; vLLM: SOSP'23; TensorRT-LLM: NVIDIA blog/GH). Critical oversight. |
| 16 | Qwen3 "four-stage pipeline (pre-train → SFT → RL → long-context)" | 2505.09388.pdf §overview | 1165 | ❌ INACCURATE | Qwen3's pipeline: Pre-training has 3 stages (General→Reasoning→Long-Context). Post-training has 4 stages (CoT SFT→RL math/code→mode-fusion SFT→general RL). The survey conflates these. "Long-context" is a pre-training stage, not the final post-training stage. |
| 17 | "Any RLHF infrastructure can be directly repurposed for OPD" | Survey synthesis | 1154 | ⚠️ OVERCLAIM | Conceptually true but understates differences: white-box OPD needs full logit access, divergence computation, teacher co-hosting. Standard RLHF only needs scalar rewards. Should qualify with "for reward-guided OPD" or note the logit extension. |

---

## Priority Actions for DEEPEN (Round 37)

### Must Fix (❌)
1. **Gemma 2 notation** (lines 790 + 1095): Change "27B→9B→2B model cascade" → "27B→\{9B, 2B\} parallel distillation" or rephrase to "bridging performance gaps across the 27B, 9B, and 2B model family"
2. **Missing citations** (line 1143): Add \citep{} for OpenRLHF, veRL, vLLM, TensorRT-LLM. Need to add bib entries.
3. **Qwen3 pipeline description** (line 1165): Fix "four-stage pipeline (pre-train → SFT → RL → long-context)" to accurately reflect the actual structure: "multi-stage post-training pipeline (cold-start SFT → domain RL → mode-fusion SFT → general RL)" with distillation for smaller models.

### Should Fix (⚠️)
4. **MiMo-V2 "frontier"** → "strong" (line 1095)
5. **16 GB figure** → add parenthetical with assumed config, or soften to "can exceed 16 GB"
6. **"Any RLHF infra"** → qualify: "For reward-guided OPD, any RLHF infrastructure..."
7. **TT-OPD 10 vs 12** — acceptable as-is (follows abstract), but could footnote the discrepancy

---

## PDFs Not Available for Verification

- DeepSeek-V4: not in pdfs/ (still pending)
- KAT-Coder-V2: not found
- MAD-OPD, Skill-SD: not found
- HY-Embodied, GUI-SD: not found

These remain on pending_verify list. Cannot verify this tick.

---

## Summary

**17 claims checked.** 9 ✅ accurate, 5 ⚠️ need softening/correction, 3 ❌ need fixing (Gemma cascade, missing cites, Qwen3 pipeline). The section has strong factual grounding for most industrial claims but the frameworks paragraph (§8.3) is notably citation-poor, and two descriptive claims about Gemma 2 and Qwen3 pipelines are inaccurate.
