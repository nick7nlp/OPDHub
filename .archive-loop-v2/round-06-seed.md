# Round 06 seed — §2 Background deep-read (manual, by main)

**Pre-seeded.** §2 covers L109–L198 (Background and Unified Math).

## Paragraph-by-paragraph analysis

### §2.0 Intro (L112) — "To understand why on-policy training is necessary"
- ✓ clean setup

### §2.0.1 "Defining 'on-policy'" (L114-L116)
- Formula and text look correct
- ✓ non-stationary optimization landscape articulated well

### §2.0.2 Notation (L118)
- Comprehensive. ✓

### §2.1 Classical KD (L122)

#### ¶1 Hinton + temperature
- Formula and gradient derivation look correct
- **Claim**: "In the high-temperature limit ($\tau \to \infty$), a Taylor expansion $\exp(z_i/\tau) \approx 1 + z_i/\tau$ shows that the gradient reduces to $\frac{1}{|V|}(z_i^{\mathcal{S}} - z_i^{\mathcal{T}})$"
  - ⚠️ This derivation is NOT quite right. The standard derivation gets $\frac{1}{\tau^2}$ factor not $\frac{1}{|V|}$. Hinton's original paper (section 2.1) shows the gradient in high-τ limit is approximately $\frac{1}{N T^2}(z_i - v_i)$ where N is batch. **VERIFY PRIORITY: HIGH**
  - Check Hinton et al. 2015 "Distilling the Knowledge in a Neural Network" section 2.1 for the exact derivation.
- **Claim**: "In practice, LLM distillation operates at moderate temperatures ($\tau \in [1, 3]$)"
  - ⚠️ no citation; many LLM distillation papers use $\tau = 1$. Add cite or soften.

#### ¶2 Token-KD formula ✓

#### ¶3 Seq-KD (Kim & Rush 2016)
- \citet{kim2016sequence}: formula + Dirac approximation
- ✓ matches paper

#### ¶4 Modern re-examination cite ~\citep{2402.11890}
- What is 2402.11890? Likely Gu et al. 2024 "Minillm" or similar re-examination paper. **VERIFY PRIORITY: MEDIUM** — check citation correctness

#### ¶5 "From classical KD to on-policy" — 4-condition relaxation story
- ⚠️ This is a nice pedagogical frame but is it citable? The 4 conditions (shared vocab, i.i.d., static teacher, off-policy) are partially fictional categorization. Might want to mark "we decompose" or cite original
- ✓ Each relaxation citation looks correct (Seq-KD, GKD, DSKD, G-OPD)

### §2.2 Off-Policy Exposure Bias (L152)

#### ¶1 DAgger bound
- ✓ formula correct
- Citation \citep{ross2011reduction} ✓

#### ¶2 Concrete example: 10 steps × 0.95^10 ≈ 60%
- ⚠️ This calculation is mathematically trivial (0.95^10 = 0.5987) but phrased as if it derives from DAgger theorem specifically. It's actually a naive per-step independence argument, NOT the DAgger bound. The DAgger bound is about state distribution mismatch, which is harder to quantify. **FIX**: clarify that this is a "simplified illustration of per-step error propagation" distinct from the formal O(εT²) regret bound.

#### ¶3 Remark on DAgger in LLMs
- ✓ insightful observation about teacher's own OOD prefix response
- This is a good synthesis paragraph

### §2.3 Unified f-Divergence (L164)

#### ¶1 OPD objective formula ✓

#### ¶2 f-divergence definition
- \citep{2307.15190} — verify this is a proper f-divergence reference (not just someone who used it)
- The definition is standard textbook ✓

#### ¶3 Forward/Reverse/JSD/α-divergence
- Forward KL: mode-covering (zero-avoiding) ✓
- Reverse KL: mode-seeking (zero-forcing) ✓
- **JSD formula**: $f(u) = u\log u - (u+1)\log\frac{u+1}{2}$
  - Standard JSD in f-divergence form uses $f(u) = u \log \frac{2u}{u+1} + \log \frac{2}{u+1}$ or equivalent
  - Let's verify: JSD(P||Q) = ½KL(P||M) + ½KL(Q||M), M = (P+Q)/2
  - In f-form, $D_f(P||Q) = \E_Q[f(u)]$ with $u = P/Q$
  - JSD as f-divergence: $f_{JSD}(u) = u \log \frac{2u}{u+1} + \log \frac{2}{u+1}$ — this is the canonical form
  - Our formula $f(u) = u\log u - (u+1)\log\frac{u+1}{2}$ — let me expand: $= u \log u - (u+1) \log(u+1) + (u+1)\log 2$
  - Canonical JSD: $f(u) = u\log\frac{2u}{u+1} + \log\frac{2}{u+1} = u(\log 2 + \log u - \log(u+1)) + \log 2 - \log(u+1) = u\log 2 + u\log u - u\log(u+1) + \log 2 - \log(u+1) = (u+1)\log 2 + u\log u - (u+1)\log(u+1)$
  - Now our formula: $u\log u - (u+1)\log\frac{u+1}{2} = u\log u - (u+1)\log(u+1) + (u+1)\log 2$ = SAME ✓
  - **VERDICT**: ✓ formula IS correct, just expressed in a slightly unusual form. OK.

#### ¶4 Task-geometry guidance (unique answer → RKL, many answers → FKL)
- ✓ good practical insight
- "All these divergences are computable as expectations under the student's own policy (since $D_f(P_T \parallel P_\theta) = \E_{y \sim \ptheta}[f(\pteacher(y)/\ptheta(y))]$)"
  - ⚠️ This is the definition of f-divergence under Q — check that Q = student (P_θ) is the second argument. In the OPD loss formula above, $\mathcal{D}_f(\pteacher, \ptheta)$ — the argument order is ambiguous without specifying which is P and which is Q. Need to clarify: when $D_f(P_T \| P_\theta)$, the expectation is under P_θ by the f-divergence definition $D_f(P \| Q) = \E_{y \sim Q}[f(P/Q)]$

#### ¶5 GKD / MiniLLM / DistiLLM mapping
- **GKD** ~\citep{2306.13649}: π_mix = λ p_θ + (1-λ) p_data
  - ⚠️ GKD original paper uses $\lambda p_\theta + (1-\lambda) p_{teacher}$ (not p_data)! The mix is student-generated vs teacher-generated, not student vs real data. **VERIFY PRIORITY: HIGH** — check GKD paper §3
- **MiniLLM** ~\citep{2306.08543}: Reverse KL + π_mix = (1-α)p_θ + α p_T, α = 0.2
  - ⚠️ Verify α = 0.2 in MiniLLM paper (might be a typo for 0.5 or another value). Actually MiniLLM uses teacher-mix with α being the teacher mix weight for reward hacking mitigation
  - **VERIFY PRIORITY: MEDIUM**
- **DistiLLM** ~\citep{2402.03898}: skewed KL
  - ✓ skew-KL is DistiLLM's named contribution

#### ¶6 Closing synthesis (design space = {π_mix, f, arg order})
- ✓ clean

### §2.4 Distillation Scaling Laws (L195)

- **Claim**: "\citet{2502.08606} initiated the study of distillation-specific scaling"
  - ✓ this is Busbridge et al. "Distillation Scaling Laws" 2025 — their paper is titled exactly that
- **Claim**: "On-policy rollout budget appears to exhibit a log-linear relationship with downstream quality"
  - ⚠️ unsupported. No citation. Either add cite or mark as "we conjecture"
- **Formula**: $\text{Quality} \propto N_T^\alpha \cdot N_S^\beta \cdot D^\gamma \cdot R^\delta$
  - ⚠️ This proposed form is speculative. OK as a motivating conjecture, but should be flagged as "a natural conjecture is"

## Top-5 priority issues for VERIFY/DEEPEN

| # | Issue | Priority | Fix |
|---|-------|----------|-----|
| 1 | Hinton τ→∞ gradient derivation: $\frac{1}{|V|}$ likely wrong (should be $\frac{1}{\tau^2}$ or $\frac{1}{N\tau^2}$) | HIGH | Read Hinton 2015 §2.1, fix formula |
| 2 | GKD π_mix = λp_θ + (1-λ)p_data — might be p_teacher in original | HIGH | Read GKD paper §3 |
| 3 | MiniLLM α = 0.2 — verify in paper | MED | Read 2306.08543 §3 |
| 4 | §2.2 0.95^10 ≈ 60% attribution to DAgger bound is imprecise | MED | Reword: "simple multiplicative illustration distinct from formal O(εT²)" |
| 5 | §2.3 f-divergence argument ordering: clarify $D_f(P_T \| P_\theta)$ has expectation under $P_\theta$ | LOW | One-line clarification |

## Bonus findings
- §2.4 scaling-law conjectures should be marked "we conjecture" or add cites
- Moderate-temperature claim $\tau \in [1,3]$ lacks cite
- The 4-condition decomposition in §2.1 is pedagogically nice but should be explicitly marked "we decompose"
