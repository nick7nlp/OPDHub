# Round 10 — READ §3.1 Method Landscape

**Mode**: READ  
**Section**: §3.1 Method Landscape (lines 207–325)  
**Date**: 2026-05-08 17:31 UTC

## Section Structure

- Line 207: `\subsection{Method Landscape}`
- Lines 209–210: Opening paragraph (2 sentences)
- Lines 212–320: TikZ taxonomy tree figure (code + caption)
- Lines 323–325: Closing prose paragraph (5 sentences)
- Line 326: `\subsection{Method Comparison Table}` begins

§3.1 的 prose 非常精简——只有开头 2 句 + 结尾 5 句，中间全是 TikZ figure。这意味着这段 prose 每一句都很重要，承担了连接 figure 和 §3.2/后续章节的全部叙事责任。

## Issues Found

### 1. ⚠️ Filler word in opening (low priority)
**Line 209**: "The practitioner faces three sequential decisions, **specifically** (1)..."
- "specifically" is filler — the enumeration already makes it specific. Cut it.

### 2. ⚠️ Unsupported claim: "reflects the actual engineering workflow" (medium)
**Line 323**: "The three-stage pipeline is not merely organizational convenience but reflects the actual engineering workflow."
- 谁的 engineering workflow？没有 cite，没有 example。这是一个 assertion without evidence。
- **建议**: 加一个例子或 cite。比如 "as evidenced by DeepSeek-R1's training pipeline \citep{2501.12948} where objective selection (Group Relative Policy Optimization) preceded signal-source decisions (cold-start from DeepSeek-V3)" 或者 soften to "mirrors a common engineering workflow"。

### 3. ⚠️ Overclaim: "Forward KL requires white-box logits, eliminating all black-box signal sources" (medium)
**Line 323**: "Some combinations are incompatible (e.g., Forward KL requires white-box logits, eliminating all black-box signal sources)"
- 数学上 D_KL(p_T || p_S) = E_{p_T}[log(p_T/p_S)] 的确需要 p_T 的 density，但可以用 Monte Carlo approximation from teacher samples：只要能从 teacher 采样，就能用 importance weighting 或 direct sampling 近似 Forward KL。
- 说 "eliminating ALL black-box signal sources" 太绝对了。实际上 GKD 的 on-policy version 也可以做 FKL with teacher samples only。
- **建议**: 改为 "Forward KL in its exact form requires access to the teacher's full output distribution, which precludes purely API-constrained settings where only generated text is available" — 更精确地说明是 exact computation 需要 logits，而非所有形式的 FKL 都不行。

### 4. ⚠️ Missing practical takeaway / synthesis (medium)
**Line 323–325**: 段落解释了 incompatibility 和 synergy，但没有回答 "so what?"。
- 高引综述的特征之一是每段都有 takeaway。这段缺一个 closing insight。
- **建议**: 加一句类似 "This interdependence means that choosing an objective implicitly constrains the viable signal sources, which motivates our decision tree (Section~\ref{subsec:decision_tree}) as a practical navigation aid."

### 5. ⚠️ Short sentence rhythm issue (low)
**Line 324**: "Other combinations are synergistic." — 4个词的句子夹在两个长句之间。
- 修辞上可以接受（rhetorical pivot），但如果后面跟的句子也短就会显得 choppy。目前后面跟了一个长句，OK。保留。

### 6. ✅ Tree method counts verified — all correct
| Category | Badge | Actual count | Status |
|----------|-------|--------------|--------|
| §4.1 Fixed Divergence | 5 | 5 | ✅ |
| §4.2 Adaptive | 3 | 3 | ✅ |
| §4.3 RL-Augmented | 11 | 11 | ✅ |
| §5.1 White-Box | 10 | 10 | ✅ |
| §5.2 Black-Box | 10 | 10 | ✅ |
| §5.3.1 Privileged | 12 | 12 | ✅ |
| §5.3.2 Self-Play | 8 | 8 | ✅ |
| §5.3.3 External | 6 | 6 | ✅ |
| §6.1 Token Weighting | 4 | 4 | ✅ |
| §6.2 Curriculum | 8 | 8 | ✅ |
| §6.3 Compute | 3 | 3 | ✅ |

Total listed: 80 (with PAINT and PRISM each appearing twice — cross-listed in §6.2 from their primary §5 categories). Unique methods: 78. Caption explicitly notes dual-listing policy. ✅

### 7. ℹ️ Classification methodology paragraph belongs to §3.2
Lines 327–336 opening §3.2 — self-referential methodology description. No external claims to verify. Examples (G-OPD → Objective, DSKD → Signal, TIP → Dynamics) verified accurate against actual paper descriptions. ✅

### 8. ⚠️ Potential inconsistency: SelecTKD/AdaSwitch dual-home (low, informational)
- SelecTKD and AdaSwitch are listed in §6.1 (tree) but **extensively discussed** in §5.1 White-Box (line 782). The table classifies them as "Dynamics".
- 这不是 error — 它们的 core contribution 确实是 dynamics（token weighting mechanism），只是 implementation 需要 white-box access。§5.1 讨论它们是在 white-box 的 context 里解释 what kinds of adaptive supervision are possible。
- 但从读者角度，在 §5.1 花 ~10 行详细描述一个"属于 §6.1"的方法可能让人困惑分类依据。
- **建议**: 在 §5.1 加一句 cross-reference note，如 "These methods are classified under Training Dynamics (Section~\ref{sec:dynamics}) owing to their primary contribution in token-level curriculum design, though they require white-box access and are therefore discussed here in the context of what white-box signals enable."

## Summary

§3.1 is lean and functional — 它的工作是引出 taxonomy figure + 解释为什么这个三阶段分类不是 arbitrary。主要问题是:
1. "reflects the actual engineering workflow" 需要 grounding（cite 或 example）
2. "eliminating ALL black-box" 需要 soften/qualify
3. 缺少 practical takeaway sentence

这些都是 DEEPEN/POLISH 轮次可以修的。No urgent factual errors.
