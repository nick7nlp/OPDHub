# Round 15 — READ §3.2 Method Comparison Table

**Mode**: READ  
**Section**: §3.2 Method Comparison Table (lines 328–532)  
**Scope**: Introductory paragraph + Table 1 (compact) + Table 2 (comprehensive) + Table 3 (experimental configs)

---

## Issues Found

### 1. Year Discrepancies (❌ factual)

| Method | Table year | Bib year | Correct | Note |
|--------|-----------|----------|---------|------|
| KDRL `2506.02208` | 2026 | 2025 | **2025** (arXiv Jun 2025) | Table wrong, must fix to 2025 |
| KETCHUP `2504.19024` | 2025 | 2026 | **2026** (EACL 2026) | Table wrong, must fix to 2026 |

### 2. Signal Source Misattribution (⚠️ accuracy)

- **RLKD** (`2505.16142`) in Table 2: listed as Signal = "White-box"
  - 实际上 RLKD 用的是 Generative Structure Reward Model (GSRM) 来对比 teacher/student 的推理结构，不是直接用 teacher logits
  - 小 Table 1 正确标注为 "Reward Model"，但大 Table 2 写了 "White-box"
  - 应改为 "Reward Model" 或 "Structure RM"

### 3. Unsupported Claims (missing cite / needs softening)

- **Line 336**: "...prevents the overlap and confusion that plagued previous multi-dimensional taxonomies"
  - 没有 citation 说明哪些 taxonomies 有这个问题。要么加 cite（比如 2402.13116 的 survey），要么改成 "...aims to reduce categorization ambiguity"
  
### 4. Prose Issues

- **Introductory paragraph** 只有一段（8 行），太单薄。作为包含 3 个大表的 subsection，缺少:
  - 对 Table 1 vs Table 2 vs Table 3 各自用途的简要说明（读者如何使用这三个表）
  - 各 category 方法数量分布的观察（e.g., "Dynamics dominates with 13 methods, reflecting the field's current focus on training stability"）
  - 时间趋势观察（e.g., "Self-distillation methods cluster entirely in 2026, indicating an emerging paradigm shift"）

### 5. Table Design Observations

- **Table 1** (compact, `table[h]`): 16 methods, 5 columns. 作为 quick-reference 很好，但:
  - 没有 year 列，读者无法判断时间线
  - "Objective (Fixed)" / "Objective (Adaptive)" / "Objective (RL)" 三个 category 各有 2-3 个代表方法，但 Dynamics 只有 2 个代表（TIP, PACED），而 Table 2 里 Dynamics 有 13 个方法。代表性选取不均衡

- **Table 2** (comprehensive, `table*[t]`): 64 methods, 7 columns. 信息量充足，但:
  - "Key Innovation" 列部分 entry 太短不够 informative（如 "Signal isolation" for Delta-KD，"Input-side distillation" for PromptKD）
  - 部分 entry 太长超出一行可能导致排版溢出

- **Table 3** (experimental configs): 覆盖 Math/Instruction/Industrial/Multimodal/Self-Distill/Black-Box 6 个 domain。
  - 但缺少 Training Dynamics 方法的 experimental config（TIP/SCOPE/Lightning/PACED 等都没出现在 Table 3）
  - "Industrial Scale" 7 个 entry 内容丰富，但 MiMo-V2 teacher 列写 "Domain specialists" 太模糊

### 6. Consistency Issues

- Table 2 中 "RLAD" 列为 "Trust Region Ratio"。实际 RLAD = Reinforcement Learning-Augmented Distillation, 用 PPO-style ratio clipping。"Trust Region Ratio" 作为 Divergence/Objective 列的值 不太准确——应该是 "Clipped PPO + KL" 或类似表述
  
- Table 2 "Constrained `\citep{2509.22921}`" — method name 只写 "Constrained" 太模糊。原文标题是 "Rethinking LLM Distillation: A CMDP Perspective"，建议改为 "CMDP-KD" 或保留但在 Key Innovation 列补全

### 7. Missing Methods (potential gaps)

- Table 2 的 Black-Box section 有 7 个方法，但 DAIL 的分类值得讨论:
  - DAIL (`2602.02405`) 标注为 "Mixed-policy decoding"。这个 technically 结合了 on-policy（student decode）和 black-box teacher，分类为 Signal (Black-Box) 合理
  
- Table 3 缺少 DSKD 的 experimental config（作为 cross-architecture 方法的代表，应该有一行）

### 8. 格式细节

- Table 1 用 `\begin{table}[h]`，Table 2/3 用 `\begin{table*}[t]`。Table 1 的 `[h]` 可能导致排版问题（LaTeX 经常无视 [h]），建议改为 `[t]` 或 `[ht]`
- Table 2 的 Self-Distillation subsection 有 18 个方法——占了大 table 的 ~28%，可以考虑是否需要进一步分 sub-category（目前已有 Self-Play / Self-PI / Self-EF 标注，不错）

---

## Priority for VERIFY (next round)

1. ❌ KDRL year: 2026 → 2025（确认 done，直接改）
2. ❌ KETCHUP year: 2025 → 2026（确认 done，直接改）
3. ⚠️ RLKD signal: verify whether it uses white-box logits at all or purely reward model
4. ⚠️ RLAD "Trust Region Ratio" 准确性

## Summary

§3.2 是纯表格+分类 methodology 段，prose 层面问题不多但确实太薄。三个表信息密度高但有两个 year 错误和一个 signal 分类问题。最需要的改进是：(1) 修 year 错误 (2) 补充 intro 段的 synthesis（分布观察、时间趋势、使用指引）(3) 审查 RLKD signal 分类。
