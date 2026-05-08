# Round 40 — READ §9-Future-Directions

**Mode**: READ  
**Section**: §9 Open Problems and Future Directions (lines 1167–1201)  
**Date**: 2026-05-09 07:21 CST

## Section Overview

§9 has 10 subsections (bold-headed paragraphs), ~35 lines of dense prose. It covers: distillation scaling laws, uncertainty-aware feedback, agent-level distillation, efficiency frontiers, latent-space/cross-modal distillation, privacy & evaluation, diagnostic tools, cross-architecture scalability, unified OPD+RLVR scheduling, distillation-RL loop closing, self-improving systems.

## 🚨 Critical Issue: Boss's Directive Violation

**"综述 Future Directions 不放自编公式/research proposal，纯叙事风格"**

Two violations found:
1. **Line 1173–1175**: Display equation `L(N_S, N_T, D_{on}) = E + A/N_S^α + ...` — a self-invented "conjectured" scaling law formula. MUST REMOVE.
2. **Line 1177** (in "Uncertainty-aware feedback"): Inline formula `c_t = 1 - H(p_teacher(·|x, y_{<t}))/log|V|` — a self-proposed confidence weight. Also violates the "no self-invented formulas" rule. MUST REMOVE or convert to narrative description.

## 📝 Unsupported Claims (Missing Citations)

| Location | Claim | Issue |
|----------|-------|-------|
| Line 1169 | "Chinchilla~\citep{2203.15556}, Kaplan" | **"Kaplan" has no cite key** — needs `\citep{2001.08361}` or similar |
| Line 1186 | "Fast OPD, Lightning OPD, and Speculative KD have made progress" | **No cites** — these are cited elsewhere in the paper but should be cited here too |
| Line 1188 | "VOLD, X-OPD, and CORD provide empirical starting points" | **No cites** — same issue, mentioned without `\citep{}` |
| Line 1188 | "DSKD, Cross-Tokenizer KD" | **No cites in this paragraph** — cited in their original section but need repeat citation here |

## ⚠️ Prose Style Issues

| Location | Issue | Suggestion |
|----------|-------|------------|
| Line 1186 | Prose colon: "...selective teacher inference**:** MiniPLM~" | Replace with em-dash or restructure |
| Line 1169 | "A natural conjecture is that..." | This IS a research proposal — violates boss's directive |
| Line 1177 | "Concretely, one could augment..." | Research proposal style — too prescriptive for a survey |
| Line 1196 | "A rigorous theoretical framework... suggesting that..." | Long subordinate-clause chain (77 words between start and period) |

## 🔍 Weak Argumentation / Missing Synthesis

1. **"Distillation scaling laws" paragraph**: Good grounding with DeepSeek-R1 numbers, but the paragraph is half-proposal (the conjectured equation + interpretation). Should be purely narrative about what's known and what gap remains.

2. **"Uncertainty-aware feedback" paragraph**: Proposes a specific formula (`c_t`) — this reads more like a position paper than a survey. Should describe the *direction* without proposing a specific mechanism. TIP cite is good grounding.

3. **"Agent-level" paragraphs (lines 1180–1185)**: Actually well-written — good synthesis of OpenClaw-RL/Skill-SD/TCOD/MAD-OPD with clear sub-problem decomposition. The "three unsolved sub-problems" structure is effective. No major issues.

4. **"Latent-space and cross-modal" (line 1188)**: Asks 3 good questions but doesn't ground them in any specific preliminary result. The VOLD/X-OPD/CORD mention at the end is tacked on rather than woven in as evidence for why these questions are tractable.

5. **"Closing the distillation-RL loop" paragraph (line 1196)**: Very long (~200 words). Synthesizes well (CoPD, KDRL, REOPOLD), but the final sentence about "principled methods for alternating..." is vague. What specific algorithmic challenge remains? The paragraph could be tightened.

6. **"Toward self-improving systems" (line 1200)**: Good narrative arc connecting to §7's saturation analysis. But "connects to deep questions about the limits of self-play in imperfect-information games" — this is a strong claim that would benefit from a game-theory cite or explicit connection.

## 📊 Numerical Claims to Verify (for VERIFY round)

| Claim | Source Cite | Status |
|-------|-------------|--------|
| DeepSeek-R1 AIME 28.9→55.5→69.7→72.6 for 1.5B→7B→14B→32B | `2501.12948` | Already in pending_verify |
| "steepest gain between 1.5B and 7B (26.6% absolute)" | computed | 55.5-28.9=26.6 ✅ math checks out |
| "14B→32B jump yielding only 2.9%" | computed | 72.6-69.7=2.9 ✅ math checks out |
| `2502.08606` "optimal teacher size grows sub-linearly with compute budget" | `2502.08606` | Need to verify this claim against the paper |
| MiniPLM "Difference Sampling" | `2410.17215` | Need to verify this is the correct characterization |

## 🎯 Priority Actions for Next Rounds

1. **HIGH**: Remove both self-invented formulas (display equation + inline c_t). Convert to narrative description.
2. **HIGH**: Add missing citations (Kaplan, Fast OPD/Lightning OPD/Speculative KD, VOLD/X-OPD/CORD, DSKD/Cross-Tokenizer KD).
3. **MEDIUM**: Fix prose colon on line 1186.
4. **MEDIUM**: Tighten "Closing the distillation-RL loop" — it's slightly bloated.
5. **LOW**: Ground the "self-play in imperfect-information games" claim.
6. **LOW**: Better integrate VOLD/X-OPD/CORD into the latent-space paragraph narrative.

## 总结

§9 写得不错，narrative arc 清晰（从 scaling → uncertainty → agents → efficiency → cross-modal → privacy → diagnostics → architecture → RL unification → self-improvement），逻辑递进。主要问题是两个自编公式违反了老大的明确指令，加上若干处引用缺失。论证质量上，agent 部分最好（有具体方法支撑），latent-space 和 self-improving 部分稍弱（grounding 不够）。
