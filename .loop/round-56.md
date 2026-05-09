# Round 56 — VERIFY — §2 Background

验证 round 55 READ 发现的事实性问题，逐条查 PDF。

## 验证表

| # | Claim | Source PDF | Verdict | Detail |
|---|-------|-----------|---------|--------|
| 1 | "DistiLLM maintains π_mix = p_θ (fully on-policy)" | 2402.03898 §3.2 | ⚠️ 不准确 | 论文明确称自己 "adaptive off-policy approach"。SGO scheduler 从低概率 ϕ 开始(早期大量使用 fixed dataset 而非 student rollouts)，且使用 replay buffer 复用过期 SGO。标题贡献之一就是 "(2) an adaptive off-policy approach." 严格说，DistiLLM 的 loss 定义在 student tokens 上（token-level matching 用 student 自己的 prefix），但 trajectory sampling 不是纯 p_θ — 它混合 fixed dataset + replay buffer 中的旧 SGO。 |
| 2 | "KL divergence dropping from 2.637 to 0.343 over training" | /tmp/opd_papers/ttopd.pdf §4.1 | ⚠️ 时间描述不精确 | PDF 原文 (line 525-526): "the KL divergence drops abruptly from its accumulated value to near zero (e.g., 2.637 → 0.343 **at step 10 with T=30**)" — 是单次 copy event 的瞬间跌落，不是 "over training" 的渐进过程。附录 (line 1242): "at step 10 in the T=30 variant, KL drops from 2.637 to 0.343, and accuracy begins its monotonic decline shortly after." |
| 3 | (0.95)^10 例子 vs DAgger bound 逻辑 | N/A (理论分析) | ✅ 逻辑可接受 | 重读上下文：survey 先讲 DAgger O(εT²) bound，然后说"即使在最简单的 independent compounding 下也已经很糟"(0.95^10≈60%)。这不是在 illustrate DAgger bound 本身，而是 motivate on-policy 的必要性。逻辑 OK，但 round 55 建议加一句"distributional shift 使实际更糟"是合理的 enhancement，留给 DEEPEN 做。 |
| 4 | §2.4 speculative formula "Quality ∝ N_T^α · N_S^β · D^γ · R^δ" | N/A | ✅ 已 hedge | 原文用 "might take the form" + "remains open"，没有当确定结论。虽然是 self-invented formula，但在 §2 作为"open question illustration"而非 §9 research proposal，且明确标注为推测。可接受，不改。 |
| 5 | "JSD performs best on translation tasks" (GKD) | 2306.13649 Fig.1 caption + §4.2 | ✅ 正确 | GKD paper Fig.1 caption: "we use JSD (0.1) on WMT and forward KL on other tasks." 隐含 JSD 在翻译上最优。Fig.4 展示 divergence 选择影响 quality-diversity tradeoff。Survey 表述 accurate。 |
| 6 | f-divergence expectation under P_θ 的正确性 | 理论验证 | ✅ 正确 | Round 55 已自行验证：D_f(P_T ‖ P_θ) 中 expectation 在 P_θ (second argument) 下。Forward KL (f=u log u): E_{P_θ}[(P_T/P_θ)log(P_T/P_θ)]。Reverse KL as D_f(P_T ‖ P_θ) with f=-log u: E_{P_θ}[-log(P_T/P_θ)] = KL(P_θ ‖ P_T)。Survey's claim correct。 |

## 需要修复的问题

### Issue 1: DistiLLM "fully on-policy" (⚠️ 需 DEEPEN 修)

**当前文本** (line ~191):
> "DistiLLM maintains π_mix = p_θ (fully on-policy) but replaces the KL target..."

**问题**: DistiLLM 论文的两大核心贡献之一就是 "adaptive off-policy approach"。说它 "fully on-policy" 会误导读者。

**修复方向**: 改为描述 DistiLLM 的 token-level loss 在 student prefix 上计算（这是 on-policy 的部分），但 trajectory-level sampling 通过 SGO scheduler 混合 fixed dataset + replay buffer (这是 off-policy 的部分)。建议:
> "DistiLLM computes its loss on student-generated prefixes but employs an adaptive scheduler that gradually increases the fraction of student outputs and caches them in a replay buffer for sample efficiency (an `adaptive off-policy' strategy in the authors' terminology)."

### Issue 2: TT-OPD KL "over training" (⚠️ 需 DEEPEN 修)

**当前文本** (line ~169):
> "Unconditional token-level matching on student-generated prefixes leads to progressive output collapse (KL divergence dropping from 2.637 to 0.343 over training)"

**问题**: "over training" 暗示渐进过程。实际是在 step 10 的单次 teacher-reset event 中瞬间跌落。

**修复方向**:
> "...leads to KL collapse (e.g., KL divergence dropping abruptly from 2.637 to 0.343 at a single teacher-reset event)"

### Non-issues (confirmed OK)

- (0.95)^10 逻辑 ✅ — 作为 motivation 合理，DEEPEN 可加一句加强
- §2.4 speculative formula ✅ — 已 hedge，不动
- GKD JSD on translation ✅ — 准确
- f-divergence expectation ✅ — 数学正确

## 下一步 (Round 57 = DEEPEN §2)

DEEPEN 应:
1. 修复 DistiLLM 描述（Issue 1）
2. 修复 TT-OPD 时间描述（Issue 2）
3. 可选: 加一句 DAgger bound 比 independent compounding 更严重的 insight
4. 可选: MiniLLM variance reduction insight (round 55 suggestion)
