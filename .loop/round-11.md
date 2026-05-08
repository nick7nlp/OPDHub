# Round 11 — VERIFY §3.1 Method Landscape

**Mode**: VERIFY  
**Section**: §3.1 Method Landscape (lines 320–325 prose)  
**Date**: 2026-05-08 17:41 UTC  
**Input**: round-10.md READ issues

## Claims Verified

### 1. "Forward KL requires white-box logits, eliminating all black-box signal sources"

| Source | Evidence | Verdict |
|--------|----------|---------|
| GKD (2306.13649) §2, Algorithm 1 | Loss `∇θ D(pT ‖ pθS)(y|x)` — for FKL = DKL(pT‖pS), requires full pT(v) for all v∈V at each token position. Line 979: "forward KL at the token level, which is not necessary when one has access to the teacher's log-probabilities, rather than just samples" | FKL needs logits ✅ |
| GKD §3.2 "Choice of Divergence" | "Forward KL requires the student to cover the entire support of the teacher token-level distribution pT" | Full distribution needed ✅ |
| Survey own §5.2 (line 807) | "This information bottleneck eliminates token-level divergence matching and forces methods to operate at the sequence level" | Consistent ✅ |

**Verdict**: ⚠️ **Technically correct but slightly overclaimed.**

The mathematical fact is right — exact token-level FKL = Σ_v p_T(v) log(p_T(v)/p_S(v)) requires knowing p_T(v) for every vocabulary token, which only white-box access provides. No known practical method computes exact FKL in a pure black-box setting.

Round-10 raised the theoretical possibility of Monte Carlo approximation. Analysis:
- You'd need E_{v~p_T}[log(p_T(v)/p_S(v))], which requires samples from p_T AND their density values p_T(v). Even importance sampling requires knowing p_T(v) for the density ratio.
- The only way to do FKL without full logits would be a variational lower bound or proxy, which is no longer "Forward KL" proper.

The word "eliminating" is strong but **accurate for exact FKL**. The survey could add "in its exact form" but this is a stylistic precision issue for DEEPEN, not a factual error.

**Action needed**: Minor — DEEPEN round could optionally insert "in its exact form" for precision, or leave as-is (defensible).

---

### 2. "reflects the actual engineering workflow"

| Source | Evidence | Verdict |
|--------|----------|---------|
| DeepSeek-R1 (2501.12948) | Pipeline: (1) GRPO as objective (RL-augmented) → (2) teacher-generated 800K samples as signal → (3) SFT with cosine decay + batch=64 as training dynamics | Matches ✅ |
| Qwen3 (cited in survey line 554, 964) | "off-policy warmup → on-policy refinement → RL exploration" — multi-stage pipeline that maps to objective/signal/dynamics | Matches ✅ |
| Survey own §6.3 line 964 | "The hybrid SFT+OPD pipeline...Qwen3 follows this two-phase approach" | Consistent ✅ |

**Verdict**: ⚠️ **Claim is reasonable but unsupported in the current prose** — no cite backs it up.

The three-stage decision chain (objective → signal → dynamics) does map to real engineering pipelines (DeepSeek-R1, Qwen3). But the current text makes this assertion without citing any concrete example. This is an evidence gap rather than a factual error.

**Action needed**: DEEPEN round should add a parenthetical cite/example, e.g., "as exemplified by DeepSeek-R1's pipeline \citep{2501.12948} and Qwen3's multi-stage recipe \citep{2505.09388}"

---

### 3. Tree badge counts (re-verified from round-10)

Already verified ✅ in round-10. All 11 categories correct, 80 entries total, 78 unique. No action needed.

---

## Bonus Verifications (from pending_verify list)

### 4. PromptKD 0.0007% parameter addition

| Source | Evidence | Verdict |
|--------|----------|---------|
| PromptKD (2402.12842) line 133 | "state-of-the-art performance by adding prompt parameters equivalent to only 0.0007% of the teacher parameters" | ✅ Exact match |

**Verdict**: ✅ ACCURATE. Resolved from pending.

---

### 5. TIP 50% retention, 2×–9× capacity gap

| Source | Evidence | Verdict |
|--------|----------|---------|
| TIP (2604.14084) Table 3 + text | "retaining 50% of tokens with entropy-based sampling matches or outperforms the all-token baseline" | 50% retention ✅ |
| TIP §7.1 Models | Qwen3 8B→4B (~2×), Llama 70B→8B (~8.75×), Qwen2.5 14B→1.5B (~9×) | "2× to 9×" ✅ |
| TIP text + Soft-OR results | "consistent improvements...across three model families" | ✅ |

**Verdict**: ✅ ACCURATE. Survey claim "50% token retention across three model families with capacity gaps from 2× to 9×" is precisely supported.

---

### 6. SCOPE +5.5% over standard OPD

| Source | Evidence | Verdict |
|--------|----------|---------|
| SCOPE (2604.10688) §Results | "SCOPE yields an average relative improvement of +5.54% over standard OPD" | ✅ |

**Verdict**: ✅ ACCURATE. Survey rounds to "+5.5%" — correct.

---

### 7. Lightning OPD 4× cost reduction

| Source | Evidence | Verdict |
|--------|----------|---------|
| Lightning OPD (2604.13010) line 374 | "Lightning OPD reduces total training cost of OPD by 4.0× at the 8B scale (from 120 to 30 GPU hours)" | ✅ Exact match |

**Verdict**: ✅ ACCURATE.

---

### 8. MTP >3× speedup at <5% accuracy drop (2602.06019)

| Source | Evidence | Verdict |
|--------|----------|---------|
| MTP paper abstract | "decode more than 3× faster on average at <5% drop in accuracy" (on GSM8K) | Abstract claim matches ✅ |
| Detailed results §7 | L3.1-8B: 3× at <3% drop. Qwen3-4B: 3× at 7% drop. | Model-dependent |

**Verdict**: ⚠️ **Defensible but nuanced.** The "<5%" comes from the paper's own abstract and applies to the primary model (L3.1-8B on GSM8K). Other models/settings show 3-7%. Survey's phrasing "achieving >3× faster decoding at <5% accuracy drop" matches the abstract exactly, so not wrong, but a reader might expect this to hold across all configurations. No edit strictly needed (we're repeating their claimed result), but the pending note correctly flagged this nuance.

---

## Summary Table

| # | Claim | Verdict | Action |
|---|-------|---------|--------|
| 1 | FKL eliminates all black-box | ⚠️ Correct but strong wording | Optional: add "in its exact form" (DEEPEN) |
| 2 | Reflects actual workflow | ⚠️ Reasonable but uncited | Add cite (DEEPEN) |
| 3 | Tree badge counts | ✅ All correct | None |
| 4 | PromptKD 0.0007% | ✅ Exact | Resolved from pending |
| 5 | TIP 50%/2×–9× | ✅ Verified | Resolved from pending |
| 6 | SCOPE +5.5% | ✅ Verified | Resolved from pending |
| 7 | Lightning 4× | ✅ Verified | Resolved from pending |
| 8 | MTP <5% drop | ⚠️ Defensible (abstract claim) | Note model-dependence if revisited |

**§3.1 prose: 0 factual errors found. 2 precision/evidence improvements recommended for DEEPEN round.**
