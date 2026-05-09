# Round 50 — §1 Introduction READ (Second Cycle)

**Mode**: READ  
**Section**: §1 Introduction (L82–L108)  
**Date**: 2026-05-09 01:01 UTC  
**Focus**: 高引综述标准的叙事弧、深度、reader engagement — 第一轮已解决 fact-check 问题，这轮看更高层

## Paragraph-by-Paragraph Analysis

### ¶1 (Opening — field momentum + DeepSeek-R1 hook)
**Current state**: 开篇不错，从 LLM 进步→成本→distillation 作为 load-bearing technique 的叙事链清晰。DeepSeek-R1 作为 concrete example 恰当。

**Issues found**:
1. **Redundant connective pileup**: 连续三个 transition words "consequently," "accordingly," "originally" 在四句话里出现，读起来有 formulaic survey 的感觉。高引综述（Vaswani intro, Goodfellow GAN intro）的开头往往更 punchy，不靠 adverb 连接而靠 idea 推动。
   - 建议: 删 "accordingly" 或合并前两句的逻辑使过渡自然
2. **"load-bearing techniques" metaphor** — 生动但可能对非英语母语读者不直观。可以保留，但后面紧跟 "shifted in character" 有点 weak 做为句尾。
   - 低优先级，不改也行
3. **¶1 末句太长 (56 words after "most visibly")** — "whose 671B...intact" 虽然第一轮已拆了 double-whose，但仍然是一个很长的 trailing modifier。
   - 可考虑把 "with long chain-of-thought...intact" 提到独立短句强化 impact

### ¶2 (Off-policy fragility + exposure bias)
**Current state**: 叙事紧凑，从 "deceptively fragile" 切入好。$O(\epsilon T^2)$ 公式有理论依据。

**Issues found**:
4. **"This is a textbook instance of exposure bias" — unsupported claim format**: 虽然 cite 了 Ross et al. 2011, 但 Ross 原文是 DAgger/imitation learning，用 "textbook instance" 暗示这是公认等价关系。实际上 exposure bias 这个术语来自 Ranzato et al. 2015 (sequence-level training)，而 Ross 2011 是 covariate shift in interactive IL。两者相关但不完全相同。
   - 建议: 精确化为 "a form of covariate shift analogous to the classical problem in interactive imitation learning~\citep{ross2011reduction}" 或添加 Ranzato 2015 cite
   - **Priority: medium** — 学术精确度问题
5. **$O(\epsilon T^2)$ bound needs source**: 这个具体的 $\epsilon T^2$ bound 来自哪里？Ross 2011 Theorem 2.1 给的是 $O(T^2 \epsilon)$ 对 naive behavioral cloning 的 surrogate loss bound，但那是 finite-horizon MDP setting。把它直接 translate 到 autoregressive LM 需要说明 reduction 是如何成立的。当前文本说 "autoregressive generation amplifies the mismatch quadratically in sequence length, producing an expected discrepancy of $O(\epsilon T^2)$" — 这里 $\epsilon$ 是什么？per-step 错误率？
   - 建议: 要么在 §2 Background 里正式推导这个 bound（如果已有则加 forward ref），要么加一句 brief justification
   - **Priority: medium-high** — 这是核心理论 claim
6. **"compounding error along the trajectory" 缺少直觉解释**: 高引综述会在 formal claim 旁加一个 intuitive 解释。比如 "a misspelled variable name at step 5 propagates into all subsequent reasoning steps that reference it, eventually derailing the proof."
   - 当前只有 "The consequences are most visible on reasoning tasks, where a single early misstep can derail an entire proof or program" — 这还行，但是放在 formal bound 之后，读起来是 afterthought 而非 illustrative
   - 低优先级

### ¶3 (OPD definition — what it is, feedback spectrum, DAgger connection)
**Current state**: 核心定义段落，结构清晰。白盒/黑盒/teacher-free 三分法简洁有效。

**Issues found**:
7. **DAgger $O(\epsilon T)$ claim**: 同样来自 Ross 2011，但原文的 bound 是 $O(\epsilon_{DAgger} T)$ where $\epsilon_{DAgger}$ is the average per-step loss under the *best policy in the class* over visited states。这跟我们这里用的 $\epsilon$ 一样吗？需确认 §2 是否正式定义了这个量。
   - 如果 §2 有 formal 推导则加 "as formalized in Section~\ref{sec:background}" 的 forward ref
   - **Priority: medium** — 和 issue #5 是同一个问题
8. **"iterative, self-correcting optimization loop"** — 稍有 overclaim。OPD 不是 self-correcting in the control-theory sense (no error signal driving convergence). 它 iteratively samples from the student's distribution, but convergence depends on specific conditions (§7 discusses when it fails). "Self-correcting" 可能给读者 false assurance.
   - 建议: 改为 "iterative optimization loop in which the training distribution co-evolves with the model"
   - **Priority: low-medium**

### ¶4 (Research landscape — three branches + industrial adoption)
**Current state**: 结构很好——divergence design / KL-RL equivalence / self-distillation 三条线，收束到 industrial adoption。

**Issues found**:
9. **"formally equivalent to a KL-constrained form of reinforcement learning~\citep{2602.12125}"**: 只 cite 了一篇 (yang2026equivalence)。但这个 equivalence 在 RLHF 文献中早有讨论 (Rafailov et al. 2023 DPO 的 reward-KL duality)。这里是特指 OPD = KL-RL 的等价，还是更广义？如果特指，应确认 2602.12125 确实做了这个 formal proof。
   - **Priority: medium** — verify claim 但不阻塞 READ
10. **Industrial examples 句太 list-like**: "Qwen3, DeepSeek-V4, Gemma 2, and MiMo-V2 treating OPD as a core training ingredient" — 这是 enumeration，不是 synthesis。高引综述会加一句 insight，比如 "converging on OPD despite strikingly different architectural choices" 来解释 WHY 这些不同团队都选了同样路径。
    - **Priority: medium** — 增加 synthesis depth
11. **Gemma 2 cite key**: `2408.00118` — verify this is actually Gemma 2 and not some other paper. Gemma 2 官方 tech report 是 2024 年 6 月发布的。
    - **Priority: low** — 可在 VERIFY round 确认

### ¶5 (Pace of transition — GKD/MiniLLM 2023 → 100+ papers)
**Current state**: 时间线叙事有效。

**Issues found**:
12. **"over one hundred papers"** — 应该有 basis。我们 bib 里有 118 entries + paper_kb 有 400+ OPD 相关。这个 "one hundred" 是保守估计还是 hand-wave？不需要 cite，但需要有内部 basis。
    - 低优先级，数字 defensible
13. **"arguably architecturally necessary"** — 第一轮已加了 "arguably" + cites。Good。✅ 无新问题。
14. **句末 "for the next generation of reasoning-capable systems"** — 有点 vague。什么是 "next generation"? 如果意思是 "for systems targeting multi-step reasoning"，可以更 precise。
    - **Priority: low**

### ¶6 (Gap in community understanding)
**Current state**: 设置 gap 段，逻辑清晰。

**Issues found**:
15. **"no current treatment offers a unified mathematical account"** — strong exclusive claim。要确保这是 true as of our submission date。除了 2402.13116 (Xu et al.)，还有没有其他 OPD-specific surveys？
    - 快速检查: 2402.13116 是 general KD survey；我们的 §1 只 cite 了这一篇 existing survey。如果有其他 2024/2025 OPD surveys 我们没 cite，这个 "no current treatment" 就有问题。
    - **Priority: medium** — VERIFY round 应 check

### ¶7-9 (Contributions list + paper structure + scope)
**Current state**: 标准综述结构段，四点贡献+结构说明+scope delimitation。

**Issues found**:
16. **贡献列表 item 3**: "the flawed prefix trap, self-play saturation, diversity collapse, and the calibration-capability gap" — 这四个 failure mode 名字是否全部在 §7 有 formal 定义和 cite？快速检查:
    - flawed prefix trap — 需确认是我们的术语还是文献中的
    - self-play saturation — SPIN 文献有讨论
    - diversity collapse — 常见术语
    - calibration-capability gap — round-01 确认来自 CaOPD
    - **Priority: low** — 只要 §7 有定义就行
17. **Scope paragraph 有轻微 redundancy**: "We cover methods in which the student generates its own training data during distillation" 基本重复了 ¶3 的 OPD 定义。不是错误，是综述惯例，但稍 verbose。
    - 不需改动

## Summary of Issues (Prioritized)

| # | Issue | Priority | Type | Action for VERIFY/DEEPEN |
|---|-------|----------|------|--------------------------|
| 4 | "textbook instance of exposure bias" — Ross 2011 is covariate shift, not exposure bias (Ranzato 2015) | Medium | Precision | Verify Ross 2011 wording; consider adding Ranzato cite |
| 5 | $O(\epsilon T^2)$ bound source unclear in ¶2 | Medium-High | Rigor | Check if §2 formalizes this; if not, add forward ref or brief justification |
| 7 | DAgger $O(\epsilon T)$ — same precision issue as #5 | Medium | Rigor | Pair with #5 |
| 8 | "self-correcting" — mild overclaim | Low-Medium | Precision | Soften wording |
| 9 | KL-RL equivalence single cite — check if broader literature applies | Medium | Citation | Verify 2602.12125 scope |
| 10 | Industrial adoption sentence lacks synthesis (WHY all converge) | Medium | Depth | Add insight in DEEPEN |
| 1 | Redundant connectives "consequently/accordingly/originally" | Low-Medium | Prose | Fix in POLISH |
| 15 | "no current treatment" — exclusive claim needs verification | Medium | Verification | Check for other OPD surveys |

## 对比第一轮
第一轮 (R01) 解决了 fact-level 问题（overclaim, GKD qualifier, architecturally necessary）。这一轮聚焦:
- **理论精确度**: exposure bias 术语归属、$O(\epsilon T^2)$ bound 出处
- **叙事深度**: industrial convergence 需要 WHY 不只 WHAT
- **reader engagement**: 连接词堆砌、self-correcting overclaim

下一步 VERIFY round 应:
1. 读 Ross 2011 确认 covariate shift vs exposure bias terminology
2. 检查 §2 Background 是否已形式化 $O(\epsilon T^2)$ bound
3. 查 2602.12125 abstract 确认 OPD=KL-RL equivalence 的具体 scope
4. 快速搜索有无其他 OPD-specific survey (2024-2025)
