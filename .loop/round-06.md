# Round 06 — VERIFY §2 Background

**Mode**: VERIFY  
**Section**: §2 Background (L109–L204)  
**Time**: 2026-05-08 16:51 UTC  
**Source**: Round 05 findings + round-06-seed  

---

## Verification Table

| # | Claim | Source PDF | Verdict | Details |
|---|-------|-----------|---------|---------|
| 1 | "All these divergences are computable as expectations under the student's own policy ($D_f(P_T \| P_\theta) = E_{y\sim p_\theta}[f(p_T(y)/p_\theta(y))]$)" | Math check + 2307.15190 | ✅ CORRECT | Round-05 flagged this as error but it's actually right. $D_f(P\|Q) = E_Q[f(P/Q)]$ with $Q = P_\theta$. For Forward KL with $f(u)=u\log u$: $E_{P_\theta}[(P_T/P_\theta)\log(P_T/P_\theta)] = \sum P_T \log(P_T/P_\theta) = KL(P_T\|P_\theta)$. At the **token level** (per-position vocabulary distribution), all f-divergences are exactly computable given both logit vectors — no sampling over vocab needed. The sampling is over trajectories from $\pi_{\text{mix}}$, not over the divergence itself. |
| 2 | G-OPD "relaxes all four simultaneously" (incl. shared vocabulary) | 2602.12125.pdf | ⚠️ OVERCLAIM | G-OPD paper: all experiments use same-family models (Qwen3-4B → Qwen3-1.7B/4B, Qwen3-30B-A3B → Qwen3-1.7B/4B). The paper mentions "distillation across different model families (Patiño et al., 2025)" as related work by others, NOT as G-OPD's own contribution. G-OPD relaxes (2) i.i.d. data, (3) static teacher (via reward extrapolation beyond teacher boundary), and (4) off-policy. It does NOT address (1) vocabulary mismatch. **Fix needed**: change "all four" to "assumptions (2)–(4)" |
| 3 | GKD: "on-policy sampling (λ=1) with JSD divergence yields the best downstream performance on summarization and translation" | 2306.13649.pdf §4.2–4.3 | ⚠️ PARTIALLY INACCURATE | GKD paper says: (a) "JSD (0.1) on WMT and forward KL on other tasks" (b) "generalized JSD divergences perform better than forward or reverse KL" — this is specifically about WMT (translation), (c) On XSum (summarization): "the choice of divergence doesn't affect performance much with greedy sampling" and mode-seeking is better with temperature sampling, (d) On GSM8K: "forward KL performs quite well." **Fix**: change to "on-policy sampling consistently outperforms off-policy, with JSD performing best on translation (WMT) and competitive results across divergences on other tasks" |
| 4 | GKD π_mix = λp_θ + (1-λ)p_data | 2306.13649.pdf Algorithm 1 | ✅ CORRECT | GKD defines: $L_{GKD} = (1-\lambda)E_{(x,y)\sim(X,Y)}[D] + \lambda E_{x,y\sim p_S}[D]$. The "fixed dataset" $(X,Y)$ can be ground-truth or teacher-generated. Our survey uses $p_{\text{data}}$ for this, which is acceptable. λ is the student data fraction. Round-05 seed worried this should be $p_{\text{teacher}}$ — but no, the dataset is explicitly "teacher-generated or ground-truth" (Alg. 1 line 1). |
| 5 | "higher temperatures risk amplifying noise in the teacher's poorly calibrated tail" | Conceptual / no direct cite found | ❓ UNSUPPORTED | Hinton 2015 doesn't make this specific claim. Busbridge 2502.08606 discusses optimal τ=1 and says "Lower temperatures reduce effectiveness by concentrating probability mass on argmax tokens, diminishing the transfer of relationships between lower-ranked predictions" but doesn't say high-T amplifies tail noise. This is a reasonable inference but lacks a direct citation. **Fix**: soften to "may risk" or add parenthetical "(a phenomenon we discuss further in §7)" |
| 6 | "The student benefits from teacher scale even after the teacher's marginal pre-training gains plateau" | 2502.08606.pdf | ⚠️ MISLEADING ATTRIBUTION | Busbridge et al. actually show the OPPOSITE phenomenon — a **capacity gap** where "a stronger teacher produces a worse student" (their key finding #3). They show "the influence of the teacher cross-entropy upon the student loss follows a power law which transitions between two behaviors." The "teacher size plateaus" finding is about compute-optimal allocation (Section 7), NOT about student benefiting from teacher scale indefinitely. Our claim conflates two different things. **Fix**: rewrite to accurately state Busbridge's finding — teacher scale helps up to a capacity gap, beyond which returns diminish or reverse. |
| 7 | "On-policy rollout budget appears to exhibit a log-linear relationship with downstream quality" | NOT in 2502.08606 | ❌ UNSUPPORTED | Busbridge et al. study off-policy distillation (logit-based KD during pretraining). They do NOT study on-policy rollouts at all. The rollout budget variable R doesn't appear in their paper. Our survey attributes this claim to them but it has no source. **Fix**: either find a paper that shows this (SAIL? GKD? MiniLLM ablations?) or mark explicitly as "we conjecture" |
| 8 | Quality formula $\propto N_T^\alpha \cdot N_S^\beta \cdot D^\gamma \cdot R^\delta$ | NOT from any paper | ⚠️ SPECULATIVE | This formula is our own conjecture. It extends Busbridge's distillation scaling law (which uses $L_S = f(N_S, D_S, L_T)$) by adding an on-policy rollout term R. Should be explicitly flagged as hypothetical. **Fix**: prefix with "A natural extension might take the form..." |
| 9 | MiniLLM α=0.2 | 2306.08543 (per round-05 verification) | ✅ CONFIRMED | Round-05 already confirmed "teacher-mix-in strength α = 0.2 throughout the experiments" from MiniLLM paper. |
| 10 | Busbridge "initiated the study of distillation-specific scaling" | 2502.08606.pdf | ✅ CORRECT | Paper title is literally "Distillation Scaling Laws" and they state "Our work is the first to determine and verify a distillation scaling law." |

---

## Summary of verdicts

- ✅ Correct (no change needed): 5 items (#1, #4, #9, #10, and #1 disproves round-05's "factual error" flag)
- ⚠️ Needs fix: 4 items (#2 G-OPD overclaim, #3 GKD JSD, #6 Busbridge misattribution, #8 speculative formula)
- ❌ Factual error: 1 item (#7 log-linear rollout claim has no source)
- ❓ Unsupported: 1 item (#5 tail noise — soft claim OK if hedged)

## Key correction: Round-05 false alarm

Round-05 flagged "Forward KL computability" as a HIGH priority factual error. After careful verification: it's NOT an error. The f-divergence formulation $D_f(P_T\|P_\theta) = E_{P_\theta}[f(P_T/P_\theta)]$ is mathematically correct and makes Forward KL computable under $P_\theta$ expectations. The confusion arose from conflating the "standard KL(P||Q) = E_P[log P/Q]" form with the f-divergence representation. Since OPD operates at the token level (computing divergence over the full vocabulary distribution at each position), both teacher and student logits are available, making all f-divergences exactly computable regardless of which is P/Q.

## Priority fixes for DEEPEN round

1. **L150**: G-OPD "relaxes all four" → "relaxes assumptions (2)–(4)" (HIGH)
2. **L193**: GKD "JSD yields best on summarization and translation" → more nuanced (MEDIUM)
3. **L198–199**: Busbridge misattribution + unsupported log-linear claim → rewrite §2.4 claims (HIGH)
4. **L134**: tail noise claim → hedge with "may risk" (LOW)

## Cross-references

- Forward KL computability: CLEARED ✅ (remove from pending_verify)
- GKD π_mix: CLEARED ✅ (correct as written)
- MiniLLM α=0.2: CLEARED ✅ (already confirmed)
