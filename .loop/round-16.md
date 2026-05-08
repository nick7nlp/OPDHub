# Round 16 — VERIFY §3.2 Method Comparison Table

**Mode**: VERIFY  
**Section**: §3.2 Method Comparison Table  
**Source**: Round 15 READ output (issues flagged)

---

## Verification Results

### 1. ❌ KDRL year in Table 2: "2026" → should be **2025**

- **Bib entry** `2506.02208`: `year = {2025}`, arXiv Jun 2025 (v4 Jan 2026 revision but submission date = 2025)
- **Table 2 line 395**: says `2026`
- **Verdict**: ❌ WRONG. Must fix to 2025.

### 2. ❌ KETCHUP year in Table 2: "2025" → should be **2026**

- **Bib entry** `2504.19024`: `year = {2026}`, venue = EACL 2026
- **Table 2 line 382**: says `2025`
- **Verdict**: ❌ WRONG. Must fix to 2026.

### 3. ⚠️→❌ RLKD signal in Table 2: "White-box" → should be **Reward Model**

**Deep-read of 2505.16142.pdf (RLKD paper):**

RLKD 的实际方法:
1. 用 Generative Structure Reward Model (GSRM) 把 teacher/student reasoning path 各自解析成 meta-reasoning + solving 步骤序列
2. GSRM 按步骤对齐程度打分（structured reward mechanism, Algorithm 1）
3. 这个 reward 和 outcome reward（如 math accuracy）加权后用 GRPO 优化

**关键点**: RLKD 不需要 teacher logits/probabilities。它只需要 teacher 的文本推理路径（pre-generated from DeepSeek-R1, 存储在 OpenR1-Math 数据集里）。GSRM 是一个独立的 7B 模型(Qwen2.5-7B-Instruct fine-tuned)，不是 teacher 本身。

- Paper 全文搜索 "KL", "logit", "token-level", "white-box", "regulariz" → 均无匹配
- Table 1 (line 349) 正确标注为 "Reward Model"
- Table 2 (line 394) 错误标注为 "White-box"

**Verdict**: ❌ WRONG. Signal 应为 "Reward Model" (Structure RM)。

**附带问题**: Survey line 754 的描述也有误 —— "KDRL operationalizes joint optimization by adding an on-policy KL regularizer between student and teacher during RL training" 这个说法是错的（RLAD 论文 2602.22495 也犯了同样的错误描述 KDRL）。实际 KDRL 用的是 GSRM reward in GRPO, 不是 KL regularizer。

### 4. ✅ RLAD "Trust Region Ratio" in Table 2 — ACCURATE

**Deep-read of 2602.22495.pdf (RLAD paper):**

RLAD 的核心组件叫 Trust Region Ratio Distillation (TRRD)。它:
- 用 PPO/GRPO-style likelihood-ratio objective
- Anchor 在 teacher–old-policy mixture 上
- 需要 teacher 的 token-level probability（计算 importance ratio）
- 所以 Signal = "White-box" ✅
- Objective = "Trust Region Ratio" ✅ (shorthand for TRRD)

**Verdict**: ✅ Table 2 对 RLAD 的分类完全准确。

### 5. ⚠️ "plagued previous multi-dimensional taxonomies" (line 331)

- 没有 citation 支持这个 claim
- 作为我们自己 taxonomy 设计 rationale 的描述，可以 soften
- 建议改为 "reduces the categorization ambiguity common in multi-dimensional taxonomies" + 可选 cite 2402.13116

**Verdict**: ⚠️ 需 soften（不是错误，是 overclaim without citation）

### 6. ✅ Survey §4 对 KDRL 的方法描述 (line 754)

Survey 原文: "KDRL operationalizes joint optimization by adding an on-policy KL regularizer between student and teacher during RL training"

**⚠️ 我最初把 RLKD (2505.16142) 和 KDRL (2506.02208) 搞混了！**
- **RLKD** (2505.16142) = "Distilling LLMs' Reasoning via RL" = 用 GSRM reward → Signal = Reward Model
- **KDRL** (2506.02208) = "Post-Training via Unified KD and RL" = 用 teacher KL + rule-based reward → Signal = White-box

验证 KDRL paper (2506.02208): 确实用 token-level Reverse KL with teacher + GRPO reward jointly optimized. Survey 描述 ✅ 准确。

**Verdict**: ✅ §4 描述正确。但 §4 line 748 对 RLKD 的描述说 "combining token-level KL regularization with trajectory-level reward" — 这个是错的（RLKD 不用 KL）。记录供下轮修复。

---

## Summary Table

| Item | Claim | Source | Verdict | Priority |
|------|-------|--------|---------|----------|
| KDRL year | 2026 in Table 2 | bib: 2025, arXiv Jun 2025 | ❌ FIX → DONE | HIGH |
| KETCHUP year | 2025 in Table 2 | bib: 2026 (EACL) | ❌ FIX → DONE | HIGH |
| RLKD signal | White-box in Table 2 | paper 2505.16142: Reward Model (GSRM, no teacher logits) | ❌ FIX → DONE | HIGH |
| KDRL signal | White-box in Table 2 | paper 2506.02208: uses teacher KL (confirmed white-box) | ✅ OK | — |
| RLAD objective | Trust Region Ratio | paper: TRRD = Trust Region Ratio Distillation | ✅ OK | — |
| "plagued" claim | no cite | meta-claim | ⚠️ SOFTEN | MEDIUM |
| KDRL method desc §4 | "KL regularizer" | paper 2506.02208: correct for KDRL | ✅ OK | — |
| RLKD method desc §4 (line 748) | "token-level KL + trajectory reward" | paper 2505.16142: NO KL, only GSRM reward | ❌ needs fix in §4 | MEDIUM |

## Next Steps (for DEEPEN round)

1. ✅ Fix KDRL year: 2026→2025 in Table 2 (DONE this round)
2. ✅ Fix KETCHUP year: 2025→2026 in Table 2 (DONE this round)
3. ✅ Fix RLKD signal: White-box→Reward Model in Table 2 (DONE this round)
4. Soften "plagued" claim (line 331)
5. Fix §4 line 748: RLKD description says "token-level KL + trajectory reward" but RLKD uses only GSRM reward (no KL) — this is a §4 issue, not §3.2
6. Expand §3.2 intro paragraph (distribution observations, usage guide for 3 tables)
