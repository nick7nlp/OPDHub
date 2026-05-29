# Round 17 — DEEPEN §3.2 Method Comparison Table + §4 RLKD fix

**Mode**: DEEPEN  
**Section**: §3.2 Method Comparison Table (+ §4 RLKD correction)  
**Source**: Round 15 READ + Round 16 VERIFY findings

---

## Changes Made

### 1. Softened "plagued" claim (line 330)

**Before**: "...prevents the overlap and confusion that plagued previous multi-dimensional taxonomies."  
**After**: "...reduces the categorization ambiguity that arises when a single method spans multiple dimensions~\citep{2402.13116}."

理由: 原文没有 citation 支持 "plagued" 这个词，加了 cite 引用现有 survey 2402.13116 作为对比参照。

### 2. Added synthesis paragraphs to §3.2 intro

新增两段：

**Table organization** — 读者使用指南，说明 Table 1/2/3 各自用途：
- Table 1: compact 16-method quick reference
- Table 2: full 64-method landscape with year/innovation
- Table 3: concrete experimental configs for practitioners

**Distributional observations** — 方法分布趋势分析：
- Self-distillation 最多 (18 methods, 30%)，几乎全在 2026，paradigm shift
- Training Dynamics 第二 (13 methods, 21%)，反映当前对 rollout 稳定性的关注
- Fixed divergences 只有 6 个（2024 年的早期方法），说明 "哪个 KL 方向" 已基本解决

**数据验证**: 用 awk 逐 category 统计 Table 2 行数确认：Fixed=6, Adaptive=3, RL-Aug=7, Signal-WB=7, Dynamics=13, Self=18, BB=7, Total=61

### 3. Fixed RLKD description in §4 (CRITICAL factual error)

**Before**: 段落标题 "Dense KD + sparse reward"，声称 RLKD "combining token-level KL regularization with trajectory-level reward"，给出公式 `max J(θ) = E[R(x,y) - β KL(p_θ || p_teacher)]`

**After**: 段落标题 "Structure-aware reward as an alternative to dense KL"，准确描述 RLKD 实际方法：
- RLKD 完全不用 KL，用 GSRM (Generative Structure Reward Model) 做 structural alignment
- 实际目标函数是 GRPO with `R_total = α R_GSRM + (1-α) R_outcome`
- 加入 insight：reasoning distillation 不必在 token level 操作

**验证来源**: 读了 `pdfs/2505.16142.pdf` 全文——搜索 "KL", "logit", "token-level", "white-box" 均无匹配。Abstract 明确说是 "RL-based distillation guided by GSRM"。Section 3 确认用 GRPO + weighted reward。

### 4. Table [h] → [ht]

Table 1 placement 从 `[h]` 改为 `[ht]`，避免 LaTeX 无视 [h] 的常见排版问题。

---

## Build Stats

- pdflatex: ✅ clean build
- Errors: 0
- Undefined refs: 0
- Pages: 58 (was 57, +1 from new paragraphs)
- Citations: 118

## Pending (for future rounds)

- Round 15 issue #5 (Table 1 representative imbalance) — cosmetic, low priority
- Round 15 issue #6 (RLAD "Trust Region Ratio" naming) — verified ✅ in round 16 as accurate
- Table 3 missing Dynamics methods (TIP/SCOPE/Lightning experimental configs) — future DEEPEN
- §4 line ~760: KDRL description is correct (verified round 16), no change needed
