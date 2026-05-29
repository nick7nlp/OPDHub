# Round 30 — READ §7 Understanding OPD (lines 1001–1084)

**Mode**: READ  
**Section**: §7 Understanding OPD: Theory, Failure Modes, and Cost  
**Subsections**: 7.1 Success Conditions, 7.2 Failure Modes, 7.3 Unified Theoretical Perspectives, 7.4 On-Policy vs. Off-Policy Decision Framework  

---

## §7 Intro Paragraph (lines 1001–1007)

整体写得不错，开头交代了前面章节在干嘛（what/where/how），然后转向 why/when。但有几个问题：

- **过度连接词堆叠**："These four dimensions of understanding are not independent but form a cumulative argument"——"four dimensions" 但后面只列了 success/failure/theory/cost，是四个吗？数数是四个，但 intro para 说的是 "why and when" 两个问题，后面又说四个维度。有点混乱。
- **"empirical art toward a principled engineering discipline"** 这个说法没有 citation。这是一个 claim（OPD 目前是 empirical art）但没给证据。可以引 DDT 或 li2026rethinking 来佐证。
- 最后一句 "The analysis below draws on both theoretical frameworks (imitation learning bounds, information geometry, RL convergence theory) and systematic empirical investigations..." 太模糊，属于 filler。能删就删。

## §7.1 Success Conditions (lines 1008–1024)

**优点**: 非常好的结构——讲了两个 necessary conditions，然后归纳出 "exploitable gap" 原则，最后给出 diagnostic checklist。高引综述质感。

**问题**:
1. **Unsupported claim**: "reverse distillation experiments show that same-family 1.5B and 7B teachers become distributionally indistinguishable from the student's perspective" — 这个 claim 只引了 li2026rethinking，但"distributionally indistinguishable"措辞很强。需要验证原文是否用了这么强的表述。
2. **Unsupported claim**: "instability originating at later tokens and propagating backward" — 也是 li2026rethinking 的说法，但"propagating backward"这个方向性需要验证。原文是说 later tokens 不稳定还是说不稳定会 backward propagate？
3. **Missing cite on checklist item 3**: "Verify that the teacher's confidence correlates with correctness on student-generated prefixes" — 这个 calibration 观察来自哪篇？CaOPD (2604.16830)? 还是 li2026rethinking? 需要加引用。
4. **Minor**: Checklist item 2 引用 PACED 但没给 cite key。应该加 `\citep{...}`。

## §7.2 Failure Modes (lines 1025–1045)

**优点**: 结构极好——按 root cause 分类而不是按 symptom。从 flawed prefix trap → SNR collapse → epistemic suppression → self-play saturation → precision-recall tradeoff → calibration-capability gap → agentic collapse。递进清晰。

**问题**:
1. **Numerical claims to verify**:
   - "KL collapse (divergence drops from $2.637$ to $0.343$ at every copy event)" — from ttopd2026. 在 pending_verify 里已经有了。
   - "turns drop from 7.82 to 5.52 per episode" — same paper.
   - "accuracy collapses from 54.5\% to 49.0\%" — same paper.
   - 这三个数字是本 section 的核心定量 claims，下一轮 VERIFY 必须核实。

2. **Unsupported analytical claim**: "mathematically analogous to mode collapse in generative adversarial networks" — 自 Ouroboros 段。这个类比没有 citation。谁做了这个 formal analogy？如果是我们自己的观察，需要 soften 为 "bears similarities to" 而非 "mathematically analogous"，除非有文献支撑。

3. **Missing cite**: "On-policy generation can shift this tradeoff by allowing the student to explore its own distribution" in precision-recall 段——这是 2505.13111 的观察还是我们自己的推断？如果是后者，需要标注为 "we hypothesize" 或加 cite。

4. **潜在逻辑跳跃**: Agentic collapse 段末尾总结 "Stable teacher dynamics, explicit regularizers on trajectory structure, and granularity-matched credit assignment are jointly necessary" — "jointly necessary" 是很强的 claim。原文的四种方法各解决了不同子集，不等于三者 jointly necessary。应 soften 为 "appear jointly necessary based on the evidence" 或类似。

5. **Prose issue**: "causing all subsequent teacher supervision to operate on a distribution the teacher has never encountered" — "never encountered" 太绝对，teacher 是大模型，会 generalize。应该改为 "a distribution far from the teacher's training regime"。

## §7.3 Unified Theoretical Perspectives (lines 1046–1062)

**优点**: 精彩的理论综合段。把 f-divergence → head-tail → GRPO=self-distill → length inflation → DPO connection → KD+RL decomposition 串成一条线。

**问题**:
1. **Out-of-place paragraph**: "Taken together, the methods in this section address signal management at progressively larger scales. Token weighting (TIP, SelecTKD, AdaKD) handles within-sequence heterogeneity..." — 这段讲的是 §6 Training Dynamics 的内容总结，放在 §7.3 Unified Theoretical Perspectives 里很突兀。它更像是 §6 的结尾段而不是 §7.3 的中间段。**建议移到 §6 末尾或删除**。

2. **Unsupported claim**: "+7.2% over vanilla OPD" for Stable-OPD — 在 pending_verify 里已有。需要下一轮验证这个数字具体指什么 benchmark。

3. **Missing connection**: DPO connection 段最后说 "and are most useful when constructing preference pairs is cheaper than computing full teacher logits" — 这是一个实用洞察但没有 citation。是我们的推断吗？如果是，需要 soften。

4. **Overclaim**: "the choice between GRPO-style RL and explicit self-distillation is often a matter of implementation convenience rather than fundamental algorithmic difference" — li2026unifying 的 equivalence 是 "under certain conditions"。这里把它泛化为 "often" 可能 overclaim。需要验证原文的 conditions 有多 restrictive。

## §7.4 On-Policy vs Off-Policy Decision Framework (lines 1063–1084)

**优点**: 非常 practical 的决策框架。DeepSeek-R1 anomaly → off-policy ceiling → distillation vs RL → hybrid pipeline → compute formula。读者看完能做决策。

**问题**:
1. **Numerical claims to verify**:
   - "R1-Distill-Qwen-7B reaches 55.5% and R1-Distill-Qwen-32B reaches 72.6%" — 在 pending_verify 里。
   - "GRPO on Qwen2.5-32B-Base achieves only 47.0%" — same paper.
   - "~800K chain-of-thought traces" — verify this number from DeepSeek-R1 paper.

2. **Unsupported strong claim**: "The off-policy ceiling, the maximum achievable performance regardless of data volume, is strictly lower" — DDT (2602.12222) 说了这个吗？"strictly lower" 是 formal statement 还是 empirical observation？如果是 formal proof，OK；如果是 empirical，应该 soften。

3. **Missing cite**: "the transition point depends on the student's initial capability. Weaker students benefit from extended off-policy warmup" — 这个 general rule 引了 li2026rethinking，但也可以引 DDT 来补充。

4. **Formula notation**: Compute formula 里 $\lambda \in (0, 1]$ 是 "teacher supervision refresh rate" — 但前面 GKD 里 $\lambda$ 是 mixing coefficient。变量名冲突可能让读者困惑。建议用不同符号或加 subscript。

5. **Missing transition**: §7.4 最后一句突然提到 "Section~\ref{subsec:budget}" 但没有 explicit takeaway。读者看完 §7.4 应该能回答 "所以我应该用 on-policy 还是 off-policy？" 但最后结束在 compute formula 上，缺乏一个 concise decision rule summary。

---

## Priority Issues for Next Rounds (VERIFY + DEEPEN)

### Must Verify (VERIFY mode):
1. TT-OPD numbers: KL 2.637→0.343, turns 7.82→5.52, accuracy 54.5%→49.0%
2. Stable-OPD "+7.2% over vanilla OPD" — which benchmark?
3. li2026rethinking "distributionally indistinguishable" — exact wording
4. li2026rethinking "instability propagating backward" — direction claim
5. DDT "strictly lower" off-policy ceiling — formal or empirical?
6. DeepSeek-R1 "~800K traces" + AIME numbers
7. li2026unifying equivalence conditions — how restrictive?

### Must Fix (DEEPEN/POLISH mode):
1. Move the "Taken together, the methods in this section..." paragraph from §7.3 — it belongs in §6
2. Soften "mathematically analogous to mode collapse in GANs" unless cited
3. Soften "jointly necessary" in agentic collapse synthesis
4. Add cite to checklist item 3 (teacher calibration)
5. Add PACED cite to checklist item 2
6. Fix $\lambda$ notation conflict in compute formula
7. Add concise decision summary at end of §7.4
8. Soften "never encountered" to "far from training regime"

### Synthesis Observations:
- §7 整体是本综述最有质感的章节之一。结构好、insight 密度高、practitioner checklist 实用。
- 主要弱点在 §7.3 中间混入了 §6 的总结段落（格格不入），以及几处 overclaim 需要 soften。
- 和高引综述标准对比：narrative arc ✅, synthesis over enumeration ✅, explain WHY ✅, trade-off analysis ✅, citation hygiene 大部分 OK 但有 5-6 处需要补/验。
