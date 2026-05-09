# Round 13 — READ (§4 Objective Functions and Optimization)

**Time**: 2026-05-09 06:25 UTC  
**Section**: Objective Functions and Optimization (lines 586–783)  
**Mode**: READ

## Section Structure

- §4.1 Fixed Divergence Objectives (l.591–733)
  - GKD, DistiLLM/SKL, DistiLLM-2, Figure 1 (KL divergence TikZ)
  - MiniLLM sequence-level RL, KETCHUP, constrained KD
  - Token-vs-sequence tradeoff synthesis paragraph
  - Full-vocabulary vs sampled-token KL (DeepSeek-V4, Lightning OPD)
- §4.2 Adaptive Divergence Objectives (l.734–752)
  - ToDi, Entropy-Aware OPD, AKL
  - Information geometry interpretation
- §4.3 RL-Augmented Objectives (l.753–783)
  - G-OPD (KL-constrained RL equivalence, Reward Extrapolation)
  - KD+RL complementarity, REOPOLD
  - RLKD (Structure-aware reward / GSRM)
  - Joint vs sequential optimization (KDRL, RLAD/TRRD)
  - DPO-based methods (AlignDistil, OVD, PBSD)
  - Error-targeted methods (SuperCorrect, SCoRe)
  - Environment reconstruction (X-KD, TSD-KD)

## Findings

### AI-Taste / Style Issues
1. ✅ No flagged AI-taste words (However/Moreover/Furthermore/Notably/Specifically/reveals/highlights/underscores/novel/crucial/vital) — section is clean
2. ✅ No narrative em-dashes
3. ✅ No prose semicolons
4. ⚠️ **2 prose colons** that could be rewritten:
   - L728: "The cost is high: REINFORCE estimation..." → could use period
   - L747: "is instructive: ToDi conditions..." → could use period
   - L751: "across evaluated settings: no single..." → borderline, leads to result statement
   (Note: colons before equations and after \textbf headers are structural and acceptable)

### Numbers/Claims to Verify (→ pending_verify)
1. **REOPOLD 6.7–12× sample efficiency** and **7B matches 32B with ~3.3× speedup** (l.761, cite 2603.11137)
2. **RLKD "only 0.1% of the data"** surpasses SFT-RL (l.770, cite 2505.16142)
3. **Lightning OPD 4× speedup** under teacher consistency (l.724, cite wu2026lightning)

### Logic/Structure Observations
- 📝 The section has excellent flow: Fixed → Adaptive → RL-augmented with clear progression
- 📝 Cross-references to other sections are well-placed (§subsec:weighting, §subsec:self_pi)
- 📝 The token-vs-sequence tradeoff paragraph effectively bridges §4.1 and §4.3
- 📝 The information geometry interpretation in §4.2 provides genuine insight (Fisher information metric / manifold curvature)
- 📝 The final summary paragraph in §4.3 provides a good hierarchy overview

### Potential Issues
- **No overclaims detected** — claims are appropriately hedged ("consistently outperform" backed by specific benchmarks)
- **Long paragraphs** — L728 paragraph (MiniLLM decomposition) is ~15 lines, dense but acceptable for this technical content
- **Repetitive construction** in §4.3: Three consecutive `\textbf{...}` paragraphs is a common survey pattern, not a problem

### Positive Notes
- Figure 1 (KL divergence) is well-integrated with surrounding text
- The DPO ↔ KL connection paragraph is a genuine insight rarely seen in surveys
- The "from signal matching to environment reconstruction" progression is conceptually strong

## Next Steps
- Round 14: VERIFY the 3 queued claims (REOPOLD numbers, RLKD data fraction, Lightning OPD speedup)
