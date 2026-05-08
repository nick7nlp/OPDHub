# Round 05 — READ §2 Background (L109–L204)

**Mode**: READ  
**Section**: §2 Background and Unified Math  
**Time**: 2026-05-08 16:41 UTC  

---

## Paragraph-by-paragraph analysis

### §2.0 Opening (L112–L113)
> "To understand why on-policy training is necessary, we must first formalize the compounding geometry of autoregressive generation."

- ✅ Good hook. Sets up logical flow.
- Minor: "compounding geometry" is slightly hand-wavy — the actual mechanism is exposure bias / state-distribution shift, not really "geometry." Consider "compounding error dynamics" or just keep it if the metaphor is intentional.

### §2.0.1 Defining "on-policy" (L114–L120)
- ✅ Formula correct — expectation over student rollouts.
- ✅ Explains non-stationary landscape well.
- ✅ Cross-reference to §6 (compute) is good.
- ⚠️ Missing cite: "non-stationary optimization landscape" is a well-known property of policy gradient methods but isn't cited here. Could cite Sutton & Barto or the DAgger paper.

### §2.0.2 Notation (L122–L124)
- ✅ Comprehensive and clear.
- Minor nit: "In the RL formalization, $\pi$ denotes policies" — but earlier we used $\ptheta$ for student policy. The dual notation ($p$ vs $\pi$) could confuse readers. Could add one sentence clarifying that $p_\theta$ and $\pi_\theta$ refer to the same entity in different formalisms.

### §2.1 Classical KD (L126–L151)

#### ¶1: Hinton formulation + temperature
- ✅ Formula correct (verified against Hinton 2015).
- ✅ Gradient formula ∂L/∂z_i^S = (1/τ)(p_i^S − p_i^T) — correct.
- ✅ High-τ limit → MSE between logits — correct, with the 1/|V|τ² factor and zero-mean assumption.
- ✅ τ² upweighting explanation — correct.
- ✅ τ=1 claim for LLM distillation + cite 2402.11890 — previously verified and fixed in round 2. Good.
- ⚠️ **Unsupported sub-claim**: "higher temperatures risk amplifying noise in the teacher's poorly calibrated tail" — this is plausible reasoning but not directly supported by Hinton (2015). 2402.11890 PDF is corrupt so I can't verify if they make this specific claim. Should either (a) soften to "...may amplify noise..." or (b) find an explicit source. **Flag for VERIFY round.**
- ⚠️ Prose issue: "the large vocabulary already produces richly structured non-peak probabilities without explicit softening" — lacks a citation. This is a widely observed empirical fact but should have a cite (GKD? MiniLLM? DistiLLM?).

#### ¶2: Token-level KD loss (L137–L139)
- ✅ Formula correct.
- ✅ "assumes an error-free history y_{<t}" — good, sets up exposure bias.

#### ¶3: Sequence-level KD (L140–L148)
- ✅ Kim & Rush (2016) formulation correct — sequence KL → intractable → Dirac delta approximation.
- ✅ NLL reduction formula correct.
- ✅ "discards all information about the teacher's uncertainty and alternative modes" — good insight.
- Minor: Could add a sentence on WHY beam-search Dirac is a good approximation (teacher confidence → peaked distribution → Dirac delta captures most mass). This would deepen the analysis.

#### ¶4: Revisiting foundations (L149–L151)
- ✅ Cite to 2402.11890 correct (Zhong et al., ACL 2024).
- ⚠️ Weak argumentation: "classical assumptions (small teacher-student gap, shared vocabulary, similar architectural inductive biases) frequently fail in the era of heterogeneous model families" — this is a strong claim. Which specific results from 2402.11890 demonstrate this? Without naming the experiments, it reads as assertion. Could strengthen by adding "demonstrating X% degradation when..." or at minimum name the failure condition they study.

### §2.1.1 "From classical KD to on-policy" (L153–L162)
- ✅ Historical progression narrative is excellent — clear, prescriptive, not just descriptive.
- ✅ Four assumptions + which paper relaxes which — well structured.
- ✅ Final "prescriptive" paragraph is high-cited-survey quality (tells reader what to DO, not just what exists).
- ⚠️ **Potential overclaim**: "G-OPD relaxes all four simultaneously" — does G-OPD truly relax shared vocabulary? G-OPD (2602.12125) works within the same vocab space. It relaxes (2) i.i.d. data, (3) static teacher (via reward extrapolation), and (4) off-policy. Vocabulary mismatch (1) is DSKD's unique contribution, not G-OPD's. **Flag for VERIFY.**
- Minor: "architecturally necessary" still appears (was flagged in round 00 for softening — check if fixed).

### §2.2 Off-Policy Exposure Bias (L164–L180)
- ✅ DAgger theorem citation (Ross et al., 2011) correct — verified O(εT²) bound matches Theorem 2.1.
- ✅ Practical consequences example: (0.95)^10 ≈ 60% — mathematically correct (0.95^10 = 0.5987 ≈ 60%).
- ✅ "Remark: The DAgger bound in LLMs" paragraph — insightful, addresses a real gap between theory and practice.
- ⚠️ **Missing synthesis opportunity**: The remark explains WHY the DAgger bound may not fully apply (teacher on OOD prefixes is poorly calibrated) but doesn't connect this to specific empirical evidence. Which papers show this failure? TT-OPD's collapse findings (§7.2) would be a perfect cross-reference here. Add: "This phenomenon is empirically documented by TT-OPD~\citep{...}, who observe X% collapse when..."
- ⚠️ **Claim without cite**: "the teacher's conditional distribution may itself become poorly calibrated, because the teacher was never trained on such inputs" — this is a reasonable theoretical argument but lacks a direct citation. Could cite TT-OPD (teacher degradation on student-generated OOD prefixes) or PBSD.
- Minor: "correction strategies that reduce the effective per-step error rate when errors have already occurred" — this is correct but could be stronger by naming the mechanism: on-policy training provides gradient signal on states the student actually visits, enabling recovery from compounding errors.

### §2.3 Unified f-Divergence Framework (L182–L198)

#### ¶1: Generalized on-policy objective (L182–L186)
- ✅ Formula correct — expectation under π_mix, sum over tokens, D_f at each position.
- ✅ Cite to 2307.15190 (f-DISTILL, Wen et al. 2023) correct.
- ✅ f-divergence definition D_f(P||Q) = E_{Q}[f(P/Q)] — correct.
- ⚠️ **Potential confusion**: The f-divergence definition says $E_{y \sim Q}[f(P(y)/Q(y))]$ but then claims "All these divergences are computable as expectations under the student's own policy (since $D_f(P_T \parallel P_\theta) = E_{y\sim p_\theta}[f(p_T(y)/p_\theta(y))]$)." This is correct for the standard definition where Q=p_θ, but for Forward KL, $D_{KL}(P_T\|P_\theta) = E_{P_T}[\log(P_T/P_\theta)]$ — NOT an expectation under p_θ! Forward KL is an expectation under P_T. The claim that "all these divergences are computable as expectations under the student's own policy" is **technically incorrect for Forward KL**. Forward KL requires importance sampling or teacher rollouts to estimate under p_θ. **This is a factual error that needs fixing in DEEPEN.**

#### ¶2: Divergence choice (L188–L193)
- ✅ Forward KL (mode-covering), Reverse KL (mode-seeking), JSD (symmetric) descriptions correct.
- ✅ α-divergence interpolation description correct.
- ⚠️ **Missing nuance**: The bullet on Forward KL says "bridging distinct teacher modes and hallucinating in the inter-mode space" — this is a well-known property but should cite Minka (2005) or Bishop textbook or at least the GKD paper's Figure A.16. Without cite, it reads as assertion.
- ⚠️ **Prose issue**: "The student collapses its mass onto the teacher's single highest peak" — this oversimplifies Reverse KL. Mode-seeking means it picks ONE mode but not necessarily the highest peak; it picks the mode it can best represent given initialization. Minor inaccuracy but could mislead.

#### ¶3: Task geometry paragraph (L194–L196)
- ✅ Good practical insight connecting divergence choice to task type.
- ⚠️ **Missing citation**: "For tasks with a unique correct answer (mathematical proofs, code correctness), Reverse KL's mode-seeking behavior..." — should cite a paper that empirically demonstrates this. MiniLLM shows Reverse KL is better for instruction-following (not specifically math). GKD shows JSD wins for summarization. Is there a paper showing Reverse KL specifically best for math? **Flag for VERIFY.**
- ⚠️ **Factual error (same as above)**: "All these divergences are computable as expectations under the student's own policy" — Forward KL is NOT. This error appears in this paragraph.

#### ¶4: GKD mapping (L198)
- ✅ GKD description matches paper — λ interpolation, agnostic to D_f.
- ✅ "JSD divergence yields the best downstream performance on summarization and translation" — verified in GKD paper ("For GKD, we use JSD (0.1) on WMT and forward KL on other tasks" + their Table shows on-policy JSD best overall). 
- ⚠️ Minor: GKD says forward KL best on non-WMT tasks, but the survey says "JSD divergence yields the best downstream performance on summarization and translation" — need to be precise. GKD actually uses forward KL on XSum/GSM8K and JSD on WMT. **Flag for VERIFY** (may need to soften to "yields competitive or best performance across tasks").

#### ¶5: MiniLLM mapping
- ✅ α=0.2 confirmed from paper ("teacher-mix-in strength α = 0.2 throughout the experiments").
- ✅ REINFORCE reformulation description correct.
- ✅ Reverse KL placement correct.

#### ¶6: DistiLLM mapping
- ✅ SKL formulation verified: KL(p_T || αp_T + (1-α)p_θ) — matches paper definition.
- ✅ "avoids zero-division instability" — correct, the denominator is always ≥ α·p_T > 0.
- ✅ "achieves tractability and stability without policy gradients" — correct (closed-form gradient).

#### ¶7: Closing synthesis
- ✅ "a systematic exploration of a design space governed by three interacting choices" — good synthesis.
- ✅ Three axes (trajectory sampling, divergence generator, argument ordering) clearly named.

### §2.4 Distillation Scaling Laws (L200–L204)
- ✅ Cite to Chinchilla (2203.15556) correct.
- ✅ Cite to Busbridge et al. (2502.08606) correct — verified title "Distillation Scaling Laws."
- ⚠️ **Unsupported claims**: "The student benefits from teacher scale even after the teacher's marginal pre-training gains plateau" — this is an interesting claim but needs a cite. Is this from Busbridge et al.? **Flag for VERIFY.**
- ⚠️ **Unsupported claim**: "On-policy rollout budget appears to exhibit a log-linear relationship with downstream quality" — where is this from? No citation provided. If from Busbridge et al., cite it. If original observation, mark as speculative. **Flag for VERIFY.**
- ⚠️ **Formula without grounding**: "Quality ∝ N_T^α · N_S^β · D^γ · R^δ" — is this from any paper or is it a hypothetical? If hypothetical, it should be marked as such ("A complete law might take the form..."). Currently it reads like it's from a paper.
- ⚠️ **Missing connection**: This subsection could benefit from connecting back to the on-policy framing — HOW does on-policy training change the scaling dynamics compared to off-policy? Is R (rollout budget) the additional axis that on-policy introduces?

---

## Summary of issues by priority

### 🔴 HIGH (factual errors / overclaims needing fix)
1. **L~195: "All these divergences are computable as expectations under the student's own policy"** — Forward KL is NOT. This is a factual error.
2. **L~155: G-OPD "relaxes all four simultaneously"** — G-OPD does NOT relax shared vocabulary (assumption 1). That's DSKD-specific.

### 🟡 MEDIUM (unsupported claims needing cite or softening)
3. **L~134**: "higher temperatures risk amplifying noise in the teacher's poorly calibrated tail" — needs cite or soften.
4. **L~134**: "large vocabulary already produces richly structured non-peak probabilities" — needs cite.
5. **L~149**: Classical assumptions "frequently fail" — needs specific evidence from cited paper.
6. **L~172-175**: DAgger remark lacks empirical cross-reference (TT-OPD collapse is a perfect match).
7. **L~200**: "student benefits from teacher scale even after marginal gains plateau" — needs cite.
8. **L~201**: "log-linear relationship" for rollout budget — needs cite or mark speculative.
9. **L~203**: Quality formula — needs to be marked hypothetical.
10. **L~195**: "Reverse KL best for unique-answer tasks" — needs empirical citation.
11. **L~198**: GKD "JSD yields best on summarization and translation" — actually GKD uses forward KL on XSum. Needs correction.

### 🟢 LOW (synthesis opportunities / minor improvements)
12. Add cross-reference from DAgger remark to §7.2 (TT-OPD collapse findings).
13. Seq-KD paragraph could explain WHY Dirac delta is reasonable (peaked teacher distribution).
14. Notation paragraph could clarify p_θ ≡ π_θ across formalisms.
15. Reverse KL bullet: "single highest peak" → "a single mode" (more accurate).
16. Scaling laws subsection could connect R (rollout budget) back to on-policy framing.

---

## Cross-references to pending_verify items
- "MiniLLM α=0.2" — ✅ CONFIRMED here (matches pending_verify entry).
- "DAgger 0.95^10 example" — ✅ mathematically correct, conceptual illustration (not from a specific paper).

## Next steps
- Round 06 (VERIFY): prioritize items #1, #2, #11 (factual), then #3, #7, #8, #10.
- Round 07 (DEEPEN): fix the Forward KL computability error, soften G-OPD claim, add cross-references.
