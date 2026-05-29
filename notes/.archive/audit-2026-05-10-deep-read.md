# OPD Survey V2 Deep-Read Report

**\u5f00\u59cb**: 2026-05-10 16:00 UTC | **\u9884\u8ba1\u7ed3\u675f**: 2026-05-11 02:00 UTC | **\u9884\u7b97**: 10 hours / 50 ticks
**\u9879\u76ee**: `/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/latex-v2/`
**\u9a71\u52a8**: cron job `opd-10h-deep-audit` (every 12 min)
**\u72b6\u6001\u6587\u4ef6**: `/tmp/opd_audit_state.json`
**\u8fd0\u884c\u65e5\u5fd7**: `memory/2026-05-10-opd-10h-audit.log`

---

## \ud83d\udcca \u4eca\u65e5\u8fd0\u884c\u5217\u8868

| Tick | Section | Status | Commits | Issues | Notes |
|------|---------|--------|---------|--------|-------|
| - | (\u624b\u5de5\u9884\u8d70) MiniLLM REINFORCE \u516c\u5f0f | \u2705 done | `2bd2cb5` | 1 fixed | \u7f3a `-1` entropy \u9879 |
| - | (\u624b\u5de5\u9884\u8d70) DistiLLM SKL \u91c7\u6837\u5206\u5e03 | \u2705 done | `2bd2cb5` | 1 fixed | on-policy \u2192 off-policy |
| - | (\u624b\u5de5\u9884\u8d70) PACED Beta-kernel \u504f\u79fb\u65b9\u5411 | \u2705 done | `8a08c29` | 1 fixed | \u03b1>\u03b2 peak right not left |
| - | (\u624b\u5de5\u9884\u8d70) Gemma2 teacher size unclaim | \u2705 done | `8a08c29` | 1 fixed | "27B teacher" \u2192 "larger teacher" |
| - | (\u624b\u5de5\u9884\u8d70) Stable-OPD \u673a\u5236\u63cf\u8ff0 | \u2705 done | `8a08c29` | 1 fixed | KL gradient asymmetry \u2192 reverse-KL advantage feedback loop |

---

## \ud83d\udd34 \u5df2\u62a5\u544a\u7684\u7ed3\u6784\u95ee\u9898\uff08\u9700\u8001\u5927\u51b3\u7b56\uff09

### KAT-Coder-V2 (li2026katcoderv2 / arXiv 2603.27703)
- [a] \u5728 \u00a78.1 Industrial Deployment
- [b] survey \u5199 "scoring 79.6\\% on SWE-bench Verified" \u548c "decomposes agentic coding into five expert domains"\u2014\u2014\u539f PDF \u6682\u672a\u4e0b\u8f7d\u5230\uff0c\u672a\u9a8c\u8bc1
- [c] \u5efa\u8bae\uff1a(1) \u91cd\u8bd5\u4e0b\u8f7d arxiv 2603.27703 \u9a8c\u8bc1\u6570\u5b57\uff0c(2) \u82e5\u4e0d\u80fd\u9a8c\u8bc1\u5219\u6539\u5199\u6210 hedged \u5f62\u5f0f\u5982 \"reportedly scoring 79.6\\%\" \u6216\u5220\u6570\u5b57\u4fdd\u7559 method \u63cf\u8ff0
- [d] \u539f\u6587\u8bc1\u636e\uff1a\u5f85\u8865\uff08PDF \u5728 16:00 UTC \u4e4b\u540e\u91cd\u4e0b\u6210\u529f\uff09

---

## \ud83d\udfe1 LLM-Generated Formula Errors\uff08\u8db3\u522b\u4eba\u6559\u8bad\uff09

| # | \u9519\u8bef\u7c7b\u578b | \u6848\u4f8b | \u5982\u4f55\u53d1\u73b0 |
|---|---------|------|---------|
| 1 | **\u516c\u5f0f\u7f3a\u9879** | MiniLLM REINFORCE \u7f3a `-1` entropy \u9879 | pdftotext + grep \u539f\u6587 Eq.(2) |
| 2 | **\u91c7\u6837\u5206\u5e03\u53cd** | DistiLLM SKL \u5199\u6210 on-policy\uff08\u539f\u6587\u662f off-policy\uff09 | \u8bfb\u539f\u6587 abstract \u7b2c\u4e00\u53e5 |
| 3 | **\u51e0\u4f55\u5206\u5e03\u65b9\u5411\u53cd** | PACED Beta kernel \u03b1>\u03b2 \u5199\u6210 peak \u5de6\u79fb | \u624b\u52a8\u4ee3\u5165 \u03b1=2,\u03b2=1 \u7b97 |
| 4 | **\u673a\u5236\u8868\u8ff0\u4e0d\u51c6** | Stable-OPD \u673a\u5236 \"KL gradient asymmetry\" \u2192 \u5e94\u4e3a \"reverse-KL advantage \u9988\u73af\" | \u5bf9\u7167\u539f\u6587\u673a\u5236\u90e8\u5206 |
| 5 | **\u67b6\u6784\u8111\u8865** | Gemma2 \"27B teacher\" \u539f\u6587\u53ea\u8bf4 \"larger model\" | grep \u539f\u6587 teacher\u63cf\u8ff0 |

\u8fd9\u4e94\u4e2a\u7c7b\u578b\u5df2\u8fdb WRITING.md \"\ud83e\udd16 LLM \u63a8\u516c\u5f0f / \u5199\u65b9\u6cd5\u63cf\u8ff0\u7684 7 \u4e2a\u9ad8\u9891\u9677\u9631\" \u8282\u3002

---

## \ud83d\udcd6 \u4eca\u65e5\u4e3a\u6b62\u9a8c\u8bc1\u8fc7\u7684 paper \u5217\u8868\uff08\u9010\u7bc7 PDF \u5bf9\u7167\uff09

| arXiv ID | \u8bba\u6587 | \u9a8c\u8bc1\u70b9 | \u7ed3\u8bba |
|----------|------|-------|------|
| 2306.08543 | MiniLLM | REINFORCE Eq.(2) + sampling | \u516c\u5f0f\u4fee\u6b63 |
| 2402.03898 | DistiLLM | SKL formula + paradigm | sampling \u4fee\u6b63 |
| 2401.01335 | SPIN | logistic SPIN loss | \u5b8c\u5168\u6b63\u786e |
| 1503.02531 | Hinton KD | gradient form | \u5b8c\u5168\u6b63\u786e |
| 2603.11178 | PACED | Beta kernel + symmetric default | asymmetry \u504f\u79fb\u65b9\u5411\u4fee\u6b63 |
| 2604.08527 | Stable-OPD | length inflation root cause + 7.2\\% | \u673a\u5236\u4fee\u6b63 |
| 2505.09388 | Qwen3 | 1/10 GPU hours + AIME pass@64 | \u5b8c\u5168\u6b63\u786e |
| 2408.00118 | Gemma 2 | 27B/9B/2B + teacher description | teacher unclaim \u4fee\u6b63 |
| 2603.19220 | Nemotron-Cascade 2 | 30B-A3B + IMO/IOI/ICPC | \u5b8c\u5168\u6b63\u786e |

---

## \ud83d\udeab \u672a\u9a8c\u8bc1\uff08\u5f85 cron tick \u5904\u7406\uff09

\u00a73.2 method comparison table | \u00a74.1 KETCHUP / constrained KD | \u00a74.2 AKL/TAID/DistiLLM-2 | \u00a74.3 G-OPD | \u00a75.1 DSKD / cross-tokenizer | \u00a75.2 Lion/OVD/ThinkTuning/GAD | \u00a75.3.1 OPSD/HDPO/GATES/OPCD/OPSDL/OEL/CRISP/GUI-SD/MSD/PBSD/TT-OPD/VISD | \u00a75.3.2 IRIS/\u03c0-Play/PAINT/SDFT/MTP/Self-Distilled RLVR/SSD | \u00a75.3.3 SD-ZERO/SDPO/RLTF/SRPO | \u00a76 weighting/curriculum/compute | \u00a77 success/failure/theory | \u00a78 industry deployment full check

\u8fd9\u4e9b\u4f1a\u88ab cron job \u9010 tick \u5904\u7406\uff0c\u6bcf tick \u4e00\u4e2a\u5c0f\u8303\u56f4\u3002

---

## \ud83d\udcc8 Cron tick \u8fd0\u884c\u4e2d
\u5982\u9700\u4eba\u5de5\u4ecb\u5165\uff1a
- \u67e5\u770b\u6700\u65b0 tick \u72b6\u6001\uff1a`cat /tmp/opd_audit_state.json`
- \u67e5\u770b\u8fd0\u884c\u65e5\u5fd7\uff1a`tail -50 /root/.openclaw/workspace/memory/2026-05-10-opd-10h-audit.log`
- \u505c\u6389 cron\uff1a\u8c03 cron \u5de5\u5177 action=update \u8bbe enabled=false
- \u67e5\u770b\u6240\u6709 audit commit\uff1a`git log --oneline | grep audit-tick`

---

## §3.2 Method Comparison Table (rows 13-24) — tick 2

### 已直接修复
1. **AlignDistil (line 415)**: Table 2 Granularity "Sequence" → "Token"，Key Innovation "Synthetic preference from rollouts" → "Token-level RLHF via contrastive DPO reward"
   - 证据: 原文标题 "AlignDistil: Token-Level Language Model Alignment"；正文反复强调 token-level reward optimization；Table 3 (line 505) 本身已写 "DPO + token-level KD"

### 结构性问题（待后续 tick 处理）
1. **§4.3 AlignDistil 描述 (line 759)**: "constructs synthetic preference pairs from student rollouts scored by the teacher" 描述不够准确。实际方法是用 DPO + Reverse DPO 模型计算 token-level contrastive reward，不是传统的 preference pair 构造。建议改为："derives token-level rewards from contrastive DPO and reverse DPO models, converting sequence-level RLHF into per-token policy distillation"
   - [a] §4.3 RL-Augmented, line 759
   - [b] AlignDistil 方法描述与原文不一致
   - [c] 改写为对 contrastive DPO reward 的正确描述
   - [d] 原文 Fig.1 caption: "distributions from a DPO model and a reverse DPO model"; Abstract: "token-level reward optimization"

### 验证通过（无问题）
- G-OPD (2602.12125): "KL-Constrained RL, Token/Seq, OPD≡dense KL-RL" ✓
- RLKD (2505.16142): "KD + Reward Model, Sequence, GSRM" ✓
- KDRL (2506.02208): "Joint KD + RL, Token/Seq, On-policy KL regularizer during RL" ✓
- RLAD (2602.22495): "Trust Region Ratio, Token/Seq, PPO-style selective teacher following" ✓
- SuperCorrect (2410.09008): "Template + Cross-DPO, Sequence, Hierarchical thought scaffolding" ✓
- SCoRe (2509.14257): "Earliest-error correction, Sequence" ✓
- DSKD (2504.11426): "Dual-Space KL, Token, Cross-vocabulary projection" ✓
- Cross-Tok. KD (2402.12030): "Latent OT alignment, Token, Optimal transport for tokenizer mismatch" ✓ (TMLR 2025)
- Delta-KD (2509.14526): "Base-to-Instruct delta, Token, Signal isolation" ✓
- PromptKD (2402.12842): "Prompt-based elicitation, Token, Input-side distillation" ✓
- TAID (2501.16937): "Temporal target interpolation, Token, Progressive target revelation" ✓

---

## §4.2 Adaptive Divergence Objectives — 结构性问题

### Issue 1: ToDi (2505.16297) — 粒度描述错误（per-position → per-vocabulary-token）

**[a] 位置**: main.tex line 720-724, ToDi 公式及说明

**[b] 问题**: Survey 将 ToDi 描述为 **per-position** 的 KL 融合：`w_t = σ(log p_T(y_t) - log p_θ(y_t))`，即在每个位置 t 用单一权重融合两个完整的 KL divergence。实际论文 (Eq. 7-8, 10) 是 **per-vocabulary-token** 级别的：`α_{t,i} = sg[σ(log(p(v_i|y_{<t}) / q_θ(v_i|y_{<t})))]`，每个词表条目 v_i 有独立权重，按各自的 teacher/student 概率比决定。

三处关键差异：
1. 权重下标：survey 用 `w_t`（仅位置），paper 用 `α_{t,i}`（位置+词表条目）
2. 权重计算：survey 在 sampled token `y_t` 处求值，paper 在每个词表条目 `v_i` 处求值
3. 融合对象：survey 融合两个完整 KL(全词表)，paper 融合每个 token 对应的 FKL/RKL 分量

这丢失了 ToDi 的核心创新点——论文明确对比 AKL 等方法说"applies FKL/RKL to the entire vocabulary uniformly"是其局限，而 ToDi 的突破是 per-vocabulary-entry control。

**[c] 建议改法**: 重写公式为：
```latex
\loss_{\text{ToDi}} = \sum_{t=1}^{|y|} \sum_{i=1}^{|V|} \alpha_{t,i} \cdot D^{(t,i)}_{\text{FKL}} + (1 - \alpha_{t,i}) \cdot D^{(t,i)}_{\text{RKL}}
```
其中 `α_{t,i} = σ(log p_T(v_i|y_{<t}) - log p_θ(v_i|y_{<t}))`，强调 per-vocabulary-entry granularity。对应文字也需改 `w_t` → `α_{t,i}`，说明是 per-token-per-vocabulary-entry 而非 per-position。

**[d] 原文证据**: 
- Paper Eq. 7: `D^{(t,i)}_{ToDi}(p, q_θ) = α_{t,i} · D^{(t,i)}_{FKL}(p, q_θ) + (1 - α_{t,i}) · D^{(t,i)}_{RKL}(p, q_θ)`
- Paper Eq. 8: `L_{ToDi} = Σ_t Σ_i D^{(t,i)}_{ToDi}(p, q_θ)` (double sum over positions AND vocabulary)
- Paper Eq. 10: `α_{t,i} = sg[σ(log(p(v_i|y_{<t}) / q_θ(v_i|y_{<t})))]`
- Paper Fig. 3 caption: "For each vocabulary token, the contributions of FKL and RKL are dynamically combined using a token-specific weight α_{t,i}"
- Paper §2.2 explicitly criticizes methods that "still dynamically apply FKL and RKL to the entire vocabulary distribution at every sequence position without assigning dynamic weights to individual tokens"

---

### Issue 2: AOPD (2605.06387) — τ 边界条件写反（已修复）

**[a] 位置**: main.tex line ~732, AOPD threshold description

**[b] 问题**: Survey 原文写"τ=1 recovering standard OPD...τ=-1 recovering GKD"。Paper 说的完全相反：
- τ=-1 → G_t = I(P_T - P_S ≤ -1) 几乎永远不触发 → 无 intervention → standard OPD
- τ=1 → G_t = I(P_T - P_S ≤ 1) 几乎永远触发 → intervention everywhere → GKD

**[c] 已直接修复**: 已 swap 两个值。

**[d] 原文证据**: Paper §5.1 最后一段: "Setting τ = −1 disables intervention for all tokens and reduces AOPD to standard OPD, while setting τ = 1 applies supervised distribution matching everywhere and recovers a GKD objective."

---

### LLM-generated formula errors（§4.2 发现的模式）

| 模式 | 具体实例 | 原因分析 |
|------|---------|---------|
| 虚增归一化因子 | AKL: 加了 1/\|V_h\| 使"mean" absolute gap（原文是 raw sum） | LLM 倾向将 sum 转换为 mean（更"标准"），但改变了 head/tail 的相对权重语义 |
| 粒度坍缩 | ToDi: 将 per-vocabulary-entry α_{t,i} 坍缩为 per-position w_t | LLM 用单一下标简化双重下标，丢失核心创新 |
| 边界条件互换 | AOPD: τ=-1 和 τ=1 效果写反 | LLM 在 indicator function I(x ≤ τ) 的逻辑推断上犯错——大 τ 意味着更容易满足条件（更多 intervention），不是更少 |


## §4.3 RL-Augmented Objectives

### [已修复] G-OPD 公式缺项（LLM-generated formula error: 缺因子）
- **位置**: Eq. (G-OPD formula, line ~743)
- **问题**: 原公式 reward 写成 `α log p_T(y_t|y_{<t})`，但 G-OPD 原文 (2602.12125, Eq. 9 & 11) 明确定义 token-level reward 为 `log(π*(y_t|y_{<t}) / π_ref(y_t|y_{<t}))`，即 teacher 与 reference 的 log-ratio。缺少 `-α log p_ref(y_t|y_{<t})` 项。
- **建议改法**: `α log \frac{p_T(y_t|y_{<t})}{p_{ref}(y_t|y_{<t})}` → 已直接修复
- **原文证据**: G-OPD paper Eq. (9): "r_t^OPD = log(π*(y_t|x,y_{<t}) / π_ref(y_t|x,y_{<t})), t=1,...,T"; Eq. (11): "J_{G-OPD}(θ) = max E[λ log(π*/π_ref) - D_KL(π_θ||π_ref)]"
- **LLM 错误模式**: 典型的"公式缺项"（WRITING.md 陷阱1），LLM 将 log-ratio 简化成单纯 log-prob

### [已修复] 2512.23097 gradient 描述用词不准
- **位置**: §4.3 第二段 "Gradient decomposition" 
- **问题**: 原文写 "two orthogonal components"，但 2512.23097 原文没有使用 "orthogonal" 一词，且两个 gradient component 并非数学意义上正交（在同一参数空间）。原文用 "natural decomposition"
- **建议改法**: "orthogonal" → "complementary" → 已直接修复
- **原文证据**: 2512.23097 全文 grep "orthogonal" = 0 命中


## §5.1 White-Box Logit Supervision (tick-7)

### Cross-Tokenizer KD 公式完全错误 [结构性问题 — 需重写]

- **位置**: §5.1 第793-800行附近，Cross-Tokenizer KD 公式及描述
- **问题**: 公式 `\mathcal{L}_{\text{CrossTok}} = \inf_{\pi \in \Pi(P_S, P_T)} \E_{(z_S, z_T) \sim \pi} [ \| W_{S \to T} z_S - z_T \|_2^2 ]` 是编造的，与论文 (2402.12030) 完全不匹配。

  **论文实际方法 (ULD loss)**:
  1. 在 **概率空间** 操作（black-box，只用输出 logits/概率），不是 hidden-state/latent-space
  2. 使用 **Wasserstein-1** 距离（L1 范数），不是 L2² 代价
  3. 有 **closed-form** 解：对概率向量排序后逐元素绝对差求和
  4. 使用 **uniform cost** 假设（所有 token 对的 transport cost = 1）
  5. **没有** 学习的投影矩阵 $W_{S→T}$

  **论文 Eq.(4-5)**:
  ```
  L_ULD = Σ_t CE(t) + λ · W_1(p_θS(·|x^S_{<t}), q_θT(·|x^T_{<t}))
  W_1 = Σ_t Σ_i |p(x^S_{σ_S(i)}|x^S_{<t}) - q(x^T_{σ_T(i)}|x^T_{<t})|
  ```
  其中 σ_S, σ_T 是将概率向量降序排序的 permutation。

- **建议改法**: 重写公式为实际的 ULD loss（Wasserstein-1 closed-form），修改描述为"基于概率空间的最优传输，通过排序后概率匹配实现跨 tokenizer 蒸馏"。
  同时修正下文描述："vocabulary-space alignment" 改为 "probability-space alignment"；删除 "alignment maps must be co-trained" 对 Cross-Tok 的适用（ULD 无可学习参数）。

- **原文证据**: 2402.12030 Eq.(4) `L_ULD = Σ CE(t) + λ × W_1(...)`, Eq.(5) `W_1 = Σ_t Σ_i |p(x^S_{σ_S(i)}|x_{<t}^S) - q(x^T_{σ_T(i)}|x_{<t}^T)|`。
  论文 Section 3.2 明确说 "Under this assumption the Wasserstein distance used in the L_ULD loss becomes..." + closed form + O(n log n) 复杂度。
  论文 Fig.2 标题："Distillation using ULD loss. In block 4, the KL divergence cannot be defined..."
  论文 Contribution 1: "A universal logit distillation loss... versatile to tokenizers and with minimal assumptions about the architectures"

### LLM 错误模式记录

- **编造公式模式**: LLM 将 Cross-Tokenizer KD 凭空编造为一个 latent-space OT 优化问题（带投影矩阵 W_{S→T} 和 L2² 代价），实际是概率空间 W1 距离。属于典型的 "看到 optimal transport 就写 Kantorovich 对偶/coupling 优化" 模板化错误。
- **DSKD KL 参数顺序翻转**: D(p ∥ q^{s→t}) 被写成 KL(P_{S→T} ∥ P_T)，把 teacher 和 student-projected 位置互换。属于典型的 "KL 两个参数搞反" 错误。


## §5.3.1 Privileged Information — OPSD 实验结果

### [已修复] OPSD 1.7B 增益被错误描述为 "minimal"

**位置**: line 854（OPSD 实验描述段落）
**问题**: 原文声称 "At 1.7B scale, however, the gains over GRPO are minimal"，但原论文 Table 2 数据显示 1.7B 是增益最大的尺度。
**原文证据** (2601.18734 Table 2):
- 8B: OPSD 64.8 vs GRPO 64.0 → +0.8
- 4B: OPSD 63.6 vs GRPO 62.7 → +0.9
- 1.7B: OPSD 43.4 vs GRPO 37.7 → **+5.7**（最大增益）
**修改**: 已直接 edit 修正，反映真实数据。保留论文限制性讨论中关于 problem-difficulty ceiling 的理论观点。
**LLM 错误模式**: 典型的 "把理论限制性陈述混淆为实验结论" — 论文 Appendix A 提到 capacity limitation 作为未来方向，LLM 错误地将其当成已有实验结论写入正文。

---

## §3.1 DAgger Remark — TT-OPD 引用归因问题

### [a] 位置
main.tex line ~164, "Remark: The DAgger bound in LLMs" 段落末尾

### [b] 问题
该段落论证 DAgger bound 在 LLM 中失效的原因是：teacher 在 student 的 OOD prefix 上可能 poorly calibrated。然后引用 TT-OPD 的 periodic-reset KL collapse (2.637→0.343) 作为"direct empirical evidence of this failure"。

**但 TT-OPD 的 KL collapse 机制完全不同**：它是因为 periodic hard copy (θT ← θS) 导致 teacher 和 student 瞬间重合从而 KL 归零，摧毁了 distillation gradient。这不是 teacher miscalibration on OOD prefixes 的问题，而是 teacher-student identity collapse 的问题。

两个 failure mode 的因果链对比：
- DAgger failure: student 生成 OOD prefix → teacher 在此 prefix 上输出 poorly calibrated → matching 此 noisy signal destabilizes training
- TT-OPD periodic reset failure: θT ← θS at step T → KL(πθS ∥ πθT) ≈ 0 → distillation gradient vanishes → student drifts without regularization

### [c] 建议改法
两种选择：
1. 删除 TT-OPD 作为 DAgger failure 的 evidence（因为它证明的是不同的 failure mode）
2. 重写引用语境：说 TT-OPD demonstrates that naive OPD without stable teacher dynamics suffers catastrophic instability，作为 "OPD 需要 careful design" 的泛化证据，而非 DAgger-specific evidence

### [d] 原文证据
PDF §6.1(1): "Periodic teacher reset... causes catastrophic KL collapse: at each copy event, the KL divergence drops abruptly from its accumulated value to near zero (e.g., 2.637 → 0.343 at step 10 with T=30), destroying the distillation gradient"

PDF 原文明确是 teacher identity problem，不是 teacher OOD calibration problem。

## §5.3.2 Self-Play (SPIN, IRIS, π-Play, PAINT)

### 已修正（直接 edit + commit）

1. **IRIS α方向错误**（LLM-generated text inversion）
   - 位置: L887, IRIS 描述段
   - 问题: 原文 "lower α encouraging broader distributional coverage (exploration) while higher α concentrates updates" — 与原论文相反
   - 原论文证据: "larger α encourages mode-covering exploration early in training, while smaller α enables mode-seeking refinement near convergence" (2604.20933, L140-141); adaptive schedule "When D̂t large → αt large, promoting [exploration]" (L332)
   - 修正: 改为 "larger α encouraging mode-covering exploration ... while smaller α enables mode-seeking refinement"

2. **PAINT overlap方向错误**（LLM-generated text inversion）
   - 位置: L901, PAINT 描述段
   - 问题: 原文 "revealing more of the reference when the student is close ... and less when far" — 与原论文相反
   - 原论文证据: "Higher overlap means that the rollout already reproduces more of the reference's mathematical structure, so it is safe to hide more" (2604.26573, L292-293); "when the student is poorly aligned (large ε), the teacher should reveal more" (L276-277)
   - 修正: 改为 "hiding more when close (encouraging broader generalization) and revealing more when far (providing stronger corrective guidance)"

### 已验证无误

- SPIN 公式 (Eq 4.7 对照) ✓
- SPIN MT-Bench 5.94→6.78 over 3 iterations (iter 0/1/2) ✓
- SPIN 收敛定理 (p_{θ_{t+1}} = p_data iff optimal) ✓
- SPIN "Nash equilibrium" 表述: 论文未使用该术语，但作为两人零和博弈不动点的game-theoretic解读是合理的editorial interpretation ✓
- IRIS 统一 SPIN/SPACE/SPIF 为 Rényi 特例 (α→1/JS/α=2) ✓
- π-Play 三 agent 架构 (examiner/teacher/student) + QCP + KL penalty + EMA ✓
- π-Play 超越 Search-R1、Dr.Zero，multi-hop gains 最大 ✓
- PAINT +2.1 over OPSD, +2.9 over GRPO (Qwen3-8B) ✓
- PAINT energy-space interpolation + entropy-mismatch sparse loss ✓

### LLM-generated formula/text errors 模式

- **方向反转 (Direction Inversion)**: LLM 写 "lower X = more exploration, higher X = more exploitation" 时约 50% 概率写反。IRIS α 和 PAINT overlap 都是此类。根因: LLM 对 exploration/exploitation 的映射没有确定性记忆，容易按"lower=broader"的直觉模板填充。

## §5.3.3 External Feedback (tick-16)

### 验证结果：主要描述准确

**SD-ZERO** (2604.12002):
- ✅ dual-role architecture (Generator + Reviser) — 原文确认
- ✅ "conditioned on the Generator's output and its binary correctness signal" — 原文确认
- ✅ 68.3% avg@8 on AIME 2024 — Table 1 原文确认
- ✅ GRPO 62.5% — Table 1 原文确认
- ✅ 模型 Qwen3-4B-Instruct — 原文确认

**SDPO** (2601.20802):
- ✅ "structured textual feedback, including runtime errors, failing unit tests, and LLM judge evaluations" — 原文确认（paper 用 "rich textual" 而非 "structured textual"，但无本质偏差）
- ✅ "fine-grained credit assignment attributing success or failure to specific reasoning steps" — 原文多处确认 "logit-level credit assignment"
- ✅ 模型 Qwen3-8B — 原文确认

**RLTF** (2602.02482):
- ✅ "free-form natural language critiques from an automated judge" — abstract 确认 "automated judges routinely critique"
- ✅ "training the model's single-turn policy to match its own feedback-conditioned second-turn generations" — 原文逐字确认

**SRPO** (2604.02288):
- ✅ routing correct/failed samples — 原文确认
- ✅ "correct → GRPO, failed → SDPO logit-level correction" — 原文确认
- ✅ 3.4% over GRPO, 6.3% over SDPO on five-benchmark average — 原文确认
- ✅ "science and tool-use tasks" — 五个 benchmark = Chemistry, Physics, Biology, Materials, Tool Use ✓

**Self-Distilled RLVR / RLSD** (2604.03128):
- ✅ "200 training steps surpasses GRPO trained for 400 steps" — Figure 1 caption 确认
- ✅ Qwen3-VL-8B-Instruct — 原文确认
- ✅ "2× sample efficiency" — 合理解读

### 已修复的问题

| # | 位置 | 问题 | 修复 |
|---|------|------|------|
| 1 | L918 | overclaim: "the richest supervision" | → "the densest supervision" |
| 2 | L918 | overclaim: "eliminates external dependencies entirely" | → "removes external dependencies" |

### 结构性问题（上报）

| # | 位置 | 问题 | 建议 |
|---|------|------|------|
| 1 | L309 ToC | RLSD 列在 §5.3.3 (External Feedback) 导航树，但实际描述在 §5.3.2 (Self-Play) L893 | RLSD 用 RLVR 外部反馈是核心机制之一，可保留分类，但建议移到 §5.3.3 正文 或 在 §5.3.3 加一句交叉引用 |
| 2 | L460 Table | CoPD 归类 "Self (EF)" 但其核心机制是 bidirectional mutual OPD (co-evolution)，非外部验证器 | 建议改 signal type 为 "Mutual" 或移到新分类。CoPD 实际描述在 §8.1 Industrial |
| 3 | L308 badge | §5.3.3 badge=6，但 Table 只有 5 个 Self(EF) 条目 + RLSD 不在 EF table | 与 issue #1 相关，确认后统一修正 badge |


## §6.2 Curriculum and Difficulty Adaptation

### 已直接修复（tick-18 commit）

1. **PACED peak 公式错误**：`p* = α/(α+β-2)` → 正确为 `p* = α/(α+β)`（原论文 Eq.2 明确）
2. **PACED 方向性倒反**：`α > β, peak right = harder` → 实际 `α > β` = peak right = easier（高 pass rate）；`α < β` = harder
3. **PACED "running estimate"**：原文默认 single-pass（K=8 一次估完），非 running estimate。已改为准确描述。
4. **TCOD "escalates exponentially"**：原文只说 "escalates" + "compounding errors"，无 "exponentially" 一词。已去除。
5. **SSB "progressively refining from coarse semantic alignment to fine-grained token-level matching"**：原论文无此机制。实际是 one-shot in-context self-distillation（correct+incorrect exemplars → robust teacher response → KL on logits）。已重写。
6. **Retaining by Doing "implicit rehearsal mechanism"**：原文从不使用 "rehearsal"。核心机制是 reverse KL 的 mode-seeking 特性保留旧 mode，而非 rehearsal。已重写。

### LLM-generated formula errors

- **Beta kernel peak formula**：LLM 把 Beta 分布的 mode 公式 `(α-1)/(α+β-2)` 错误嫁接给了 Beta-kernel 权重函数 `p^α(1-p)^β` 的 peak。后者的 peak 是通过 `dw/dp = 0` 直接求解得到 `p* = α/(α+β)`，不同于 Beta 分布 PDF 的 mode 公式。
  - 这是 LLM 的典型模式：把看似相关但实际不同的公式混淆（Beta 分布 vs Beta-kernel 权重）

### 未修但值得注意

- **Uni-OPD 描述** ✅ 准确，与原文吻合
- **TCOD 描述** ✅ 除了 "exponentially" 外基本准确
- **Cold start (li2026rethinking)** ✅ 准确
- **Hybrid SFT+OPD pipeline** 末段 ✅ 合理


## §7.3 Unified Theoretical Perspectives

### 已直接修复（tick-22 commit）

1. **f-DISTILL 框架覆盖范围错误**：原文声称 "subsumes Forward KL, Reverse KL, JSD, and α-divergences"。实际论文 2307.15190 覆盖的是 Forward KL, Reverse KL, JSD, 和 TVD（Total Variation Distance）。α-divergences 仅在 related work 中提及，非该框架的 explicit special case。已改为 "total variation distance"。
2. **"composable with any divergence choice" 无原文依据**：Stable-OPD 论文（2604.08527）并未声称其方法与任意 divergence 可组合。已删除该声称。

### 结构性问题（需重写）

| # | 位置 | 问题 | 建议改法 | 原文证据 |
|---|------|------|---------|---------|
| 1 | §7.3 第一段末尾两句（关于 2505.13111） | **严重张冠李戴**：综述声称该论文 "identify the minimal conditions under which a student can provably benefit from teacher supervision versus learning from data alone. The benefit scales with the information gap between the teacher's distribution and the data distribution as seen by the student." 但该论文（Cha & Cho, NeurIPS 2025）的实际贡献是 **KD 中的 precision-recall tradeoff**：teacher entropy 越低（越 selective），student precision 越高但 recall 越低。论文完全不讨论 "minimal conditions for benefit" 或 "information gap"。 | 两种修法：(A) 将描述改写为准确反映 precision-recall tradeoff 贡献，但需重新审视与 "exploitable gap" 的逻辑连接是否成立；(B) 如果确实有另一篇讲 "information gap" 的论文，替换 cite key。最可能需要方案 A：改为 "At a more foundational level, \citet{2505.13111} show that KD induces a precision-recall tradeoff modulated by teacher entropy: as the teacher becomes more selective, the student concentrates on high-density modes at the cost of coverage. This explains why matching a selective teacher yields higher-quality outputs and complements the empirical finding of \citet{li2026rethinking} that teacher-student pattern alignment is a precondition for effective distillation." | 原文 abstract: "distillation induces a trade-off between precision and recall in the student model. As the teacher distribution becomes more selective, the student concentrates more probability mass on high-likelihood regions at the expense of coverage, which is a behavior modulated by a single entropy-controlling parameter." |

### LLM-generated description errors

- **2505.13111 "information gap" 编造**：LLM 可能从标题 "Why Knowledge Distillation Works...A Minimal Working Explanation" 中的 "minimal" 推断出 "minimal conditions"，但实际内容与此无关。这是 LLM 根据标题推测内容的典型错误模式。

## §9 Open Problems and Future Directions

### [结构性问题] 自编公式出现在 Future Directions（违反 USER.md + WRITING.md 规则）

**[a] 位置**: §9 "Distillation scaling laws" 段，第 1192-1194 行左右（`\begin{equation} L(N_S, N_T, D_{\text{on}}) = E + ...` 公式）

**[b] 问题**: USER.md 明确要求"综述 Future Directions 不放自编公式/research proposal"。此公式是作者自编的 scaling law conjecture（"a natural conjecture is that..."），虽然有 off-policy 证据作动机，但本质是一个未验证的 research proposal。

**[c] 建议改法**: 
- 方案 A（推荐）：删除公式，改为纯叙述："A natural conjecture is that the on-policy distillation loss follows a joint power-law in student size, teacher size, and on-policy rollout budget, with an additional interaction term capturing the capacity-gap interference between student and teacher."
- 方案 B：保留公式但移到 §7.3 Unified Theoretical Perspectives 作为 "conjectured framework"，§9 只引用

**[d] 原文证据**: USER.md 第 32 行："综述 Future Directions 不放自编公式/research proposal，纯叙事风格（2026-03-30）"；WRITING.md "高引综述 Anti-pattern" 第 1 条："❌ Future Directions 写成 '我们会做 X' / todo list → 应是开放问题"
