# Round 37 — DEEPEN §8 Applications

**Mode**: DEEPEN  
**Section**: §8 (Applications, Systems, and Emerging Domains)  
**Time**: 2026-05-08 22:51 UTC  
**Source**: Round 35 (READ) + Round 36 (VERIFY)

---

## Edits Made

### 1. ❌ Fixed: Gemma 2 cascade notation (§8.1)
- **Before**: "27B→9B→2B" implying sequential cascade
- **After**: Explicitly states "distilling the 27B teacher into both the 9B and 2B students independently (parallel distillation rather than cascading)" + adds insight about WHY parallel avoids compounding approximation errors
- **Reasoning**: Round 36 VERIFY confirmed paper says both distilled from 27B independently

### 2. ❌ Fixed: Qwen3 pipeline description (§8.5)
- **Before**: "four-stage pipeline (pre-train → SFT → RL → long-context)" — wrong, conflates pre-training stages with post-training
- **After**: "multi-stage post-training pipeline (cold-start SFT → domain RL for math and code → mode-fusion SFT → general RL)" + notes distillation provides primary transfer for smaller variants
- **Reasoning**: Round 36 VERIFY confirmed actual Qwen3 structure from 2505.09388 §overview

### 3. ❌ Fixed: Missing framework citations (§8.3)
- Added `\citep{}` for OpenRLHF, veRL, vLLM, TensorRT-LLM
- Added 4 new bib entries: hu2024openrlhf, sheng2024verl, kwon2023vllm, nvidia2024tensorrtllm
- All from correct primary sources (arXiv/SOSP/GitHub)

### 4. ⚠️ Fixed: MiMo-V2 "frontier" overclaim (§8.1)
- **Before**: "achieving frontier performance on mathematical reasoning"
- **After**: "achieving strong performance on mathematical reasoning and agentic tasks"
- **Reasoning**: Paper says "strong reasoning and agentic capabilities", never "frontier"

### 5. ⚠️ Fixed: "Any RLHF infra" overclaim (§8.4)
- **Before**: "Any RLHF infrastructure can be directly repurposed for OPD"
- **After**: Qualified to "For reward-guided OPD..." + explains that white-box logit OPD needs additional teacher co-hosting + logit transfer, which existing frameworks already support via teacher-inference process groups
- Adds deeper insight about what the equivalence actually covers vs. what needs extension

### 6. ⚠️ Fixed: 16 GB logit figure underspecified (§8.3)
- **Before**: "$\sim$16\,GB of logit data per batch" — exact figure without config assumptions
- **After**: "can exceed 16\,GB per batch ($[B, T, |V|] \times 2$ bytes in BF16, e.g., $B{=}16, T{=}4096, |V|{=}128$K)" — provides concrete example config

### 7. DEEPEN: CoPD paragraph (§8.1)
- Broke the 30+ word run-on sentence
- Added WHY insight: "The root cause is that experts trained in isolation develop idiosyncratic reasoning strategies that are mutually incompatible when merged"
- Added deeper architectural insight: co-evolution imposes a soft constraint on teacher diversity, preventing the specialization-consolidation gap

### 8. DEEPEN: Agentic distillation synthesis (§8.1)
- Added hedging: "The emerging consensus suggests" instead of stating as fact
- Added cross-reference to hierarchical RL (option boundaries as natural credit assignment unit)
- Added forward-looking connection: future methods may benefit from automated decision-boundary detection
- Cite for support: ross2011reduction (DAgger / compounding errors)

---

## Build Results

| Metric | Value |
|--------|-------|
| Pages | 59 |
| LaTeX Errors | 0 |
| Undefined citations | 0 |
| New bib entries | 4 (openrlhf, verl, vllm, tensorrt-llm) |

---

## Summary

8 targeted edits addressing all 3 ❌ items and 4 ⚠️ items from Round 36 VERIFY. Added insight on WHY parallel distillation avoids cascade errors, WHY co-evolution works (prevents specialization-consolidation gap), and connected agentic granularity principle to hierarchical RL literature. All framework citations now properly added. Build clean.

---

## Remaining §8 Issues (for future rounds)

- OpenClaw-RL underexplained (MEDIUM) — needs deeper mechanism description
- Video-OPD, X-OPD, KEPO shallow (MEDIUM) — no numbers provided
- CORD "SOTA" without concrete number (MEDIUM)
- VLA-OPD "significantly improves" without numbers (MEDIUM)
- >500B / ≤70B thresholds in §8.4 — need citation or hedging
- Several pending_verify items still lack local PDFs
