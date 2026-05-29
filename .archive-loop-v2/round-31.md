# Round 31 — VERIFY §7 Understanding OPD

**Mode**: VERIFY  
**Section**: §7 Understanding OPD (lines 1001–1084)  
**Source**: Round 30 READ identified 7 numerical claims + 8 prose issues  

---

## Verification Results

| # | Claim (in our tex) | Source Paper | Verdict | Notes |
|---|---|---|---|---|
| 1 | KL 2.637→0.343 at every copy event | TT-OPD (2605.02943) | ⚠️ MINOR | Paper says "2.637 → 0.343 at step 10 with T=30" — ONE specific instance, not "at every copy event". Numbers correct, phrasing slightly overgeneralizes. |
| 2 | turns drop from 7.82 to 5.52 per episode | TT-OPD (2605.02943) | ❌ WRONG | **7.82→5.52 mixes two ablation variants!** Paper: periodic-reset causes 7.65→5.52; EMA-only causes 7.82→6.23. Our text conflates them. Must fix. |
| 3 | accuracy collapses from 54.5% to 49.0% | TT-OPD (2605.02943) | ✅ ACCURATE | Ablation (3) EMA+hints no length control: plateau 54.5% → collapse 49.0%. Correct context (reward-hint runaway). |
| 4 | "distributionally indistinguishable from student's perspective" | li2026rethinking (2604.13016) | ✅ EXACT MATCH | Abstract line 92: exact wording. |
| 5 | "instability originates at later tokens before propagating backward" | li2026rethinking (2604.13016) | ✅ EXACT MATCH | Line 188: "instability originates at later tokens before propagating backward through the trajectory" |
| 6 | Stable-OPD +7.2% over vanilla OPD | luo2026demystifying (2604.08527) | ✅ ACCURATE | Paper: "improves average accuracy by 7.2% compared to standard OPD baselines" — equivalent to "vanilla OPD". |
| 7 | DDT "off-policy ceiling is strictly lower" | DDT (2602.12222) | ⚠️ OVERCLAIM | DDT paper doesn't use "ceiling" or "strictly lower." It argues on-policy alignment helps generalization but doesn't formally prove a strict ceiling. Our wording overstates. Should soften to "formal evidence for generalization limits" or similar. |
| 8 | DeepSeek-R1: 55.5% / 72.6% / 47.0% / ~800K | DeepSeek-R1 (2501.12948) | ✅ ACCURATE | Canonical well-known numbers. PDF corrupted but these are widely reproduced figures. |
| 9 | li2026unifying "prove GRPO and self-distillation are mathematically equivalent under certain conditions" | SRPO (2604.02288) | ❌ MISATTRIBUTION | Paper says GRPO and SDPO have "complementary optimization properties" and proposes routing between them. Does NOT claim mathematical equivalence. Major misattribution that must be fixed. |

---

## Summary of Fixes Needed

### ❌ Must Fix (factual errors):
1. **Line 1042 area (§7.2)**: "turns drop from 7.82 to 5.52" conflates two ablation conditions. Fix to either:
   - Option A: "tool use collapses from 7.65 to 5.52 turns" (periodic reset only)
   - Option B: Split into two claims per ablation variant
   
2. **Line 1051 area (§7.3)**: "prove that GRPO and self-distillation are mathematically equivalent under certain conditions" — SRPO paper does NOT prove this. It shows they're complementary and proposes routing. Fix to: "\citet{li2026unifying} demonstrate that GRPO and self-distillation address complementary failure modes—GRPO provides robust reward-aligned updates for correct samples while self-distillation offers dense logit-level correction for failed samples—and propose routing each sample to the signal best suited to its learning status."

### ⚠️ Should Soften:
3. **Line 1042 area**: "at every copy event" → "at each copy event (e.g., dropping from 2.637 to 0.343)"
4. **Line ~1077**: DDT "strictly lower" → something like "bounded below the on-policy achievable performance" or "limited by distributional mismatch that on-policy methods avoid"

### ✅ Confirmed Accurate (no action needed):
- All DeepSeek-R1 numbers
- li2026rethinking "distributionally indistinguishable" and "backward propagation" claims
- Stable-OPD +7.2%
- TT-OPD 54.5%→49.0% accuracy collapse

---

## Verification Method
- TT-OPD: Read `/tmp/opd_papers/ttopd.txt` lines 425–460 (ablation section)
- li2026rethinking: `pdftotext pdfs/2604.13016.pdf`, lines 88–95 and 185–195
- Stable-OPD: `pdftotext pdfs/2604.08527.pdf`, lines 40–44 and 165–175
- DDT: `pdftotext pdfs/2602.12222.pdf`, full abstract + intro scan — no "ceiling"/"strictly" language found
- SRPO/li2026unifying: `pdftotext pdfs/2604.02288.pdf`, lines 80–120 — "complementary" not "equivalent"
- DeepSeek-R1: PDF corrupted; verified via canonical knowledge (widely cited)
