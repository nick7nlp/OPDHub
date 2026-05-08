# Round 41 — VERIFY §9-Future-Directions

**Mode**: VERIFY  
**Section**: §9 Open Problems and Future Directions  
**Date**: 2026-05-09 07:31 CST  
**Input**: Round 40 READ output

## Verification Results

### Claim 1: DeepSeek-R1 AIME 28.9→55.5→69.7→72.6 for 1.5B→7B→14B→32B

**Source**: `pdfs/2501.12948.pdf`, Table 16 (distilled model results)  
**Method**: PyMuPDF text extraction, searched for model names + AIME scores  

| Model | AIME 2024 (Pass@1) | Survey Claim |
|-------|---------------------|--------------|
| DeepSeek-R1-Distill-Qwen-1.5B | 28.9 | 28.9 ✅ |
| DeepSeek-R1-Distill-Qwen-7B | 55.5 | 55.5 ✅ |
| DeepSeek-R1-Distill-Qwen-14B | 69.7 | 69.7 ✅ |
| DeepSeek-R1-Distill-Qwen-32B | 72.6 | 72.6 ✅ |

**Verdict**: ✅ All four numbers match exactly.

**Derived arithmetic checks**:
- "steepest gain between 1.5B and 7B (26.6% absolute)": 55.5 - 28.9 = 26.6 ✅
- "14B→32B jump yielding only 2.9%": 72.6 - 69.7 = 2.9 ✅

---

### Claim 2: `2502.08606` "optimal teacher size grows sub-linearly with compute budget"

**Source**: `pdfs/2502.08606.pdf` (Busbridge et al., "Distillation Scaling Laws", ICML 2025)  
**Method**: Full text extraction, read abstract + sections 5.2/5.3 + Appendix D.4.6

**What the paper ACTUALLY says** (key findings from multiple sections):

1. **Lines 1212-1218**: "Student and teacher tokens scale as a power law, with student tokens scaling at a faster rate. Optimal teacher size **increases initially** until it is slightly larger than the student, after which it **plateaus**. This plateau occurs because inference with large teachers is expensive..."

2. **Lines 5107-5111**: "At this point, the teacher solution starts to become the overtrained solution seen in teacher inference, the optimal teacher tokens continue to increase polynomially, but this is not followed with an increase in the teacher size. For sufficiently high compute, corresponding to a large number of student distillation tokens, the compute penalty for teacher size is so large that **optimal teacher size decreases with compute**."

3. **Lines 2985-2987**: The paper refines Zhang et al. 2023a's finding that "optimal teacher scale follows an approximately linear relationship with the student's scale" — showing this is a special case when teachers are compute-optimal.

**Verdict**: ⚠️ **INACCURATE characterization.** The paper shows a **non-monotone** relationship: optimal teacher size (1) increases initially, (2) plateaus at slightly larger than student, (3) eventually **decreases** at high compute. "Grows sub-linearly" is an oversimplification that misses the crucial plateau+decline behavior. The paper's main contribution is the *full scaling law* (Equation 8), not a simple growth characterization.

**Recommended fix**: Replace "fitting parametric curves that reveal optimal teacher size grows sub-linearly with compute budget" with something like "fitting parametric curves that reveal a non-trivial compute-optimal allocation where teacher size plateaus once slightly exceeding the student, while student distillation tokens continue to scale as a power law"

---

### Claim 3: MiniPLM "Difference Sampling" = "selecting training instances based on the log-probability discrepancy between teacher and a reference model"

**Source**: `pdfs/2410.17215.pdf` (MiniPLM, ICLR 2025)  
**Method**: Full text extraction, read Section 2.2 (Difference Sampling)

**What the paper says** (lines 220-259):
- "Difference Sampling refines the pre-training corpus D based on the discrepancy between p [teacher] and the output distribution p_ref from a tiny reference LM"
- Formula: `D' = top-K { log p(x)/p_ref(x) | x ∈ D - D_ref }`
- This is the log-probability ratio (= discrepancy) between teacher and reference model

**Survey says**: "selecting training instances based on the log-probability discrepancy between teacher and a reference model ('Difference Sampling')"

**Verdict**: ✅ Accurate characterization. The survey correctly captures the essence of Difference Sampling.

---

### Claim 4: Kaplan missing citation

**Verification**: Searched `references.bib` for "kaplan" and "2001.08361" — neither exists.  
The line reads: `Chinchilla~\citep{2203.15556}, Kaplan` — "Kaplan" is bare text with no `\citep{}`.

**Verdict**: ❌ Missing citation confirmed. Need to add Kaplan et al. 2020 (arXiv 2001.08361) to bib and cite it properly.

---

### Claim 5: "Fast OPD, Lightning OPD, and Speculative KD have made progress" — missing cites in §9

**Verification**: All three have bib entries:
- Fast OPD: `2602.15260`
- Lightning OPD: `wu2026lightning`  
- Speculative KD: `2410.11325`

But in the "Efficiency frontiers" paragraph (line 1186), they appear WITHOUT `\citep{}` — just bare method names.

**Verdict**: ❌ Citations exist in bib but are NOT used at this mention. Need to add `\citep{2602.15260,wu2026lightning,2410.11325}` after the list.

---

### Claim 6: "VOLD, X-OPD, and CORD provide empirical starting points" — missing cites

**Verification**: All three have bib entries:
- VOLD: `2510.23497`
- X-OPD: `2603.24596`
- CORD: `hu2026cord`

But in the "Latent-space" paragraph (line 1188), they appear WITHOUT `\citep{}`.

**Verdict**: ❌ Citations exist but not used here. Need `\citep{2510.23497,2603.24596,hu2026cord}`.

---

### Claim 7: "DSKD, Cross-Tokenizer KD" — missing cites in latent-space paragraph

**Verification**: Bib entries:
- DSKD: `2504.11426`
- Cross-Tokenizer KD: `2402.12030`

These ARE cited properly in the "Cross-architecture scalability" paragraph with `DSKD~\citep{2504.11426} and Cross-Tokenizer KD~\citep{2402.12030}`. But in the latent-space paragraph they're mentioned without cites.

**Verdict**: ⚠️ They ARE cited in the cross-architecture paragraph (where the detailed discussion is), so the latent-space paragraph's bare mention is acceptable as a cross-reference within the same section. Lower priority — optional fix.

---

## Summary Table

| # | Claim | Source | Verdict | Priority |
|---|-------|--------|---------|----------|
| 1 | DeepSeek-R1 AIME numbers (28.9/55.5/69.7/72.6) | 2501.12948 Table 16 | ✅ Exact match | — |
| 2 | "optimal teacher size grows sub-linearly" | 2502.08606 §5/App D | ⚠️ **Inaccurate** — non-monotone (increase→plateau→decrease) | HIGH |
| 3 | MiniPLM "Difference Sampling" characterization | 2410.17215 §2.2 | ✅ Accurate | — |
| 4 | "Kaplan" bare text, no cite | references.bib | ❌ Missing from bib | HIGH |
| 5 | Fast OPD/Lightning OPD/Speculative KD no cites | references.bib | ❌ Keys exist, not cited here | MEDIUM |
| 6 | VOLD/X-OPD/CORD no cites | references.bib | ❌ Keys exist, not cited here | MEDIUM |
| 7 | DSKD/Cross-Tokenizer KD in latent-space para | references.bib | ⚠️ Cited elsewhere in same section, acceptable | LOW |

## 🎯 Actions for DEEPEN round (R42)

1. **Fix inaccurate claim** about 2502.08606 — rewrite to accurately reflect the non-monotone relationship
2. **Add Kaplan citation** to bib (2001.08361) and fix the bare "Kaplan" text
3. **Add missing \citep{}** for Fast OPD/Lightning OPD/Speculative KD
4. **Add missing \citep{}** for VOLD/X-OPD/CORD
5. (Cross-reference from round 40) **Remove self-invented formulas** — the display equation and inline c_t formula violate boss's directive

## 总结

本轮核心发现：DeepSeek-R1 数字全部精确无误，MiniPLM 描述准确，但 2502.08606 的 scaling law 描述有实质性错误——论文展示的是 teacher size 先增后平再降的非单调关系，不是简单的"sub-linearly grows"。另外 4 处引用缺失需要补上。下一轮 DEEPEN 应优先修复 scaling law 描述和自编公式问题。
