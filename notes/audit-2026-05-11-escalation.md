# OPD Survey V2 — 需老大决策的 5 个结构性问题

**时间**: 2026-05-11 04:41 UTC (audit tick-43)
**来源**: 10h deep-audit (50 ticks，43/50 已完成)
**项目**: `/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/latex-v2/main.tex`

---

## 概览

10 小时 deep-audit 发现 10 个问题，其中 5 个小的已直接修复 + commit。以下 5 个需要重写整段/涉及论文结构决策，等你确认方案后我派 writer 执行。

| # | 章节 | 问题一句话 | 建议方案 |
|---|------|-----------|---------|
| R1 | §5.1 | Cross-Tok KD 公式完全编造 | 重写为 W1 closed-form |
| R2 | §4.2 | ToDi 粒度坍缩（per-pos → per-vocab） | 重写双重求和公式 |
| R3 | §7.3 | 2505.13111 张冠李戴 | 改写为 precision-recall tradeoff |
| R4 | §3.1 | TT-OPD 引用归因错 | 改引用语境或换 evidence |
| R5 | §9 | Future Directions 自编公式 | 删公式改纯叙述 |

---

## R1. §5.1 Cross-Tokenizer KD 公式完全编造 ⭐严重

**现状**: 综述写了一个 latent-space OT 优化公式（带投影矩阵 W_{S→T} + L2² 代价 + coupling π ∈ Π(P_S, P_T)），全是编造的。

**原文 (2402.12030) 实际方法 — ULD loss**:
- 在**概率空间**操作（black-box，只用输出 logits）
- 使用 **Wasserstein-1** 距离（L1 范数），不是 L2²
- **Closed-form** 解：对概率向量排序后逐元素绝对差求和
- **没有**可学习投影矩阵

**建议**: 重写公式为 `L_ULD = Σ_t CE(t) + λ · W_1(p_θS, q_θT)`，其中 W_1 通过排序后 L1 求解。同时删除后文 "alignment maps must be co-trained" 对 Cross-Tok 的适用。

---

## R2. §4.2 ToDi 粒度坍缩

**现状**: 公式用 `w_t`（仅位置级权重）融合两个完整 KL。

**原文 (2505.16297) 实际方法**:
- 权重 `α_{t,i}` 在每个位置 t 的每个词表条目 v_i 有独立值
- 双重求和：`Σ_t Σ_i α_{t,i} D_FKL^{(t,i)} + (1-α_{t,i}) D_RKL^{(t,i)}`
- 这是 ToDi 相对 AKL 的核心创新——AKL 是 per-position uniform，ToDi 是 per-vocabulary-entry

**建议**: 改写公式为双重求和 + `α_{t,i} = σ(log p_T(v_i) - log p_θ(v_i))`

---

## R3. §7.3 论文 2505.13111 描述张冠李戴

**现状**: 综述写该论文 "identify the minimal conditions under which a student can provably benefit from teacher supervision"，还说 "benefit scales with the information gap"。

**原文实际贡献**: 论文证的是 KD 中的 **precision-recall tradeoff** — teacher entropy 越低（越 selective），student precision 越高但 recall 越低。完全不讨论 "minimal conditions" 或 "information gap"。

**建议**: 改写为 "show that KD induces a precision-recall tradeoff modulated by teacher entropy: as the teacher becomes more selective, the student concentrates on high-density modes at the cost of coverage"，重新建立与前文 "exploitable gap" 的逻辑连接。

---

## R4. §3.1 DAgger Remark 误引 TT-OPD

**现状**: 用 TT-OPD 的 periodic-reset KL collapse (2.637→0.343) 作为 "teacher miscalibration on OOD prefixes" 的 evidence。

**问题**: 两个完全不同的 failure mode：
- DAgger failure: student OOD prefix → teacher poorly calibrated → noisy supervision
- TT-OPD failure: θT ← θS 硬拷贝 → KL≈0 → distillation gradient 消失

TT-OPD 证明的是 teacher-student identity collapse，不是 OOD miscalibration。

**建议两选一**:
- A: 删 TT-OPD 引用，换一个真正证明 teacher-on-OOD-prefix-poorly-calibrated 的 evidence
- B: 改引用语境为 "demonstrates that naive OPD without stable teacher dynamics suffers catastrophic instability"（更宽泛的 claim，TT-OPD 能支撑）

---

## R5. §9 Future Directions 自编公式

**现状**: 有一个作者自编的 scaling law 公式 `L(N_S, N_T, D_on) = E + ...`

**违反**: USER.md 硬性规则"综述 Future Directions 不放自编公式/research proposal，纯叙事风格"

**建议两选一**:
- A（推荐）: 删公式，改纯叙述 "A natural conjecture is that the loss follows a joint power-law in student size, teacher size, and rollout budget, with an interaction term capturing capacity-gap interference."
- B: 保留公式但移到 §7.3 作为 "conjectured framework"

---

## 你需要告诉我的

对每个 R1-R5，选一个方案（或给你自己的方案）。确认后我统一派 writer 执行重写 + 编译验证。

如果全部同意建议方案，回复 "全按建议来" 即可。
