# OPD 综述全文循环校验报告
**日期**: 2026-03-30
**版本**: main.tex (37页, 73 bib, ~45 公式)
**方法**: 8 维度全覆盖 (2 researcher sub-agent + 自动化脚本 + 手动验证)

---

## 维度 1: 方法描述准确性 ✅ 基本通过

已验证核心方法: GKD, MiniLLM, DistiLLM, ToDi, AKL, DSKD, REOPOLD, SuperCorrect, OPSDC, DeepSeek-R1, SPIN, OPSD, GATES, SDPO, RLKD, LUFFY, GAD, Lion, DAIL 等。

### 发现问题
1. **DAIL Teacher 标注错误** (Table 2, L665)
   - 当前: `Self (privileged student)`
   - 实际: DAIL 用的是外部 expert human solutions（非 self-distillation），应标为 `Expert solutions (black-box)` 或类似
   - 严重性: ❌ 需修正

---

## 维度 2: 数值声明验证 ✅ 基本通过

### 发现问题
1. **OPSDC 数字范围不一致** (L477 vs L849/L942)
   - L477: "reduces reasoning trace length by **41--59%**"（混合了 MATH-500 和 AIME 的数据）
   - L849/L942: "57--59% on MATH-500" + "41% on AIME 2024"（正确，分 benchmark 报告）
   - 建议: L477 改为具体说明 benchmark，如 "41--59% across benchmarks"
   - 严重性: ⚠️ 轻微

2. **REOPOLD 3.3× vs 3.32×** (正文)
   - 当前: "~3.3×"
   - 原文: "~3.32×"
   - 严重性: ⚠️ 极轻微，可忽略

---

## 维度 3: BibTeX venue 验证 ✅ 基本通过

### 发现问题
1. **2603.13260 (TSD-KD)**: 当前标为 `arXiv preprint` → 已被 **ICLR 2026** 接收
   - 严重性: ❌ 需更新

2. **2602.02405 (DAIL)**: 标为 `Proceedings of ICML 2026` 但 arXiv 无 comments 确认
   - 严重性: ⚠️ 可能正确但无法验证

3. **2602.12222 (DDT)**: 标为 `Proceedings of ICML 2026` 但 arXiv 无 comments 确认
   - 严重性: ⚠️ 可能正确但无法验证

其余 70 条均已正确标注 venue。

---

## 维度 4: 公式方向正确性 ✅ 全部通过

逐个检查了全部 ~30 个含 KL 的公式：
- 所有 Forward KL: KL(P_T || P_θ) 方向正确 ✅
- 所有 Reverse KL: KL(P_θ || P_T) 方向正确 ✅
- MiniLLM REINFORCE 梯度推导正确 ✅
- DistiLLM Skew Reverse KL 正确 ✅
- Entropy-Aware OPD 混合方向正确 ✅
- SPIN log ratio 方向正确 ✅
- RLKD 梯度结构正确 ✅
- Figure 2 Forward/Reverse KL 图示与公式一致 ✅

---

## 维度 5: 全文符号一致性 ⚠️ 有系统性问题

### 发现问题
1. **小写 p vs 大写 P 混用** (系统性)
   - 正文 Section 2 声明: "lowercase p for token-level, uppercase P for sequence-level"
   - 实际: Section 4 (White-Box Methods) 中，轨迹采样写 `y ~ p_θ`（小写），但采样的是 sequence-level 分布，应该用 `P_θ`
   - 影响范围: Eq 14-18, 20-22, 25-26 等约 10+ 个公式
   - **但 Section 6 (Reasoning) 添加了免责声明统一用大写 P**
   - 严重性: ⚠️ 中等。Section 4 没有类似声明，建议在 Section 4 开头也加说明，或统一
   
2. **\loss vs \mathcal{L} 混用**
   - `\loss` (= `\mathcal{L}`): 10 处（Sections 2-3）
   - `\mathcal{L}`: 18 处（Sections 4-8）
   - 两者渲染结果相同（\loss 定义为 \mathcal{L}），不影响输出
   - 严重性: ⚠️ 极轻微，源码级不一致

3. **P_{mathcal{T}} vs P_T (teacher sequence-level)**
   - Section 2: 使用 `P_{\mathcal{T}}(y|x)` (5处)
   - Section 4+: 使用 `P_T(y|x)` (22处)
   - 严重性: ⚠️ 轻微，但不完全一致

---

## 维度 6: Table 间同步一致性 ❌ 有遗漏

### Taxonomy Tree (Fig 3) Granularity 维度遗漏

| 方法 | Table 1 Granularity | Taxonomy Tree Granularity | 状态 |
|------|---------------------|---------------------------|------|
| G-OPD | Token | ❌ 未列入 Token-Level | 缺失 |
| DSKD | Token | ❌ 未列入 Token-Level | 缺失 |
| REOPOLD | Token | ❌ 未列入 Token-Level | 缺失 |
| TSD-KD | Token | ❌ 未列入 Token-Level | 缺失 |
| DASD | Seq. | ❌ 未列入 Seq-Level | 缺失 |
| DDT | Seq. | ❌ 未列入 Seq-Level | 缺失 |
| Fast OPD | Hybrid | ❌ 未列入 Hybrid | 缺失 |

### Feedback Signal 和 Teacher Access 维度
✅ 已包含所有 Table 1 方法（确认 Logit-Based 包含 REOPOLD/TSD-KD/DASD/DDT，White-Box 也包含）

### Citation 完整性
✅ 72 个 cite keys 全部有对应 bib entry，无遗漏

---

## 维度 7: 格式检查 ⚠️ 有问题

### Em Dashes (---) 在正文中
- 共 23 处在正文段落中使用 em dash
- 用户偏好: "论文正文叙述不用破折号（---）"
- 严重性: ❌ 需批量替换

### LLaMA vs Llama
- L80 (Intro): "LLaMA" → 这里指 Meta 的 LLaMA v1，历史名称正确
- L635 (Table, AKL): "LLaMA 6.7B" → 同上，LLaMA v1 时代
- L647 (Table, MiniLLM): "LLaMA-13B", "LLaMA 7B" → 同上
- L662 (Table, Lion): "LLaMA-7B / 13B" → 同上
- 严重性: ✅ 可接受（LLaMA v1 的历史正式名称就是 "LLaMA"）

### 其他
- 无 undefined references ✅
- 无 TODO/FIXME (TODO check 已清理) ✅
- 无 sentence-initial bare \citep ✅
- 无 double spaces ✅

---

## 维度 8: 多模型语义审读 ⚠️ 有问题

### 逻辑一致性 ✅
- Forward KL mode-covering → Figure 2 hallucination zone → 公式方向 全部自洽
- Reverse KL mode-seeking → Figure 2 mode dropped → 公式方向 全部自洽
- MiniLLM REINFORCE 推导 → reward 解释 全部自洽

### 分类一致性
1. **DAIL 分类矛盾** ❌
   - Taxonomy Tree + 正文: Black-Box 方法
   - Table 2: Teacher = "Self (privileged student)" → 暗示 Self-Distillation
   - 需要修正 Table 2 的 Teacher 列

### 文本冗余
1. **AKL 描述重复** ⚠️
   - Section 4.1.1 和 Section 4.4 都详述了 AKL 打破 "FKL/RKL 二分法" 的论述
   - 建议: Section 4.4 简化为引用 4.1.1 的内容

2. **GATES/SDPO/Priv.Info.Distill 描述重复** ⚠️
   - Section 3.2 (Taxonomy) 已详细描述了这些方法的机制
   - Section 5.2 又几乎重复了一遍
   - 建议: Section 3.2 只做概述，详情放 Section 5.2

3. **OPSDC 三次描述** ⚠️
   - L477 (Section 3.2), L849 (Section 5.2.3), L942 (Section 6.3) 三处描述
   - 且数字口径不统一 (41--59% vs 57--59%)

---

## 修复优先级

### P0 (必须修复)
1. **Em dashes 批量替换** - 23 处正文 em dash
2. **Taxonomy Tree Granularity 补全** - 7 个方法缺失
3. **DAIL Table 2 Teacher 修正** - 分类错误

### P1 (建议修复)
4. **OPSDC L477 数字口径统一**
5. **TSD-KD bib venue 更新** - arXiv → ICLR 2026
6. **文本冗余精简** - AKL + GATES/SDPO + OPSDC 重复描述

### P2 (可选)
7. Section 4 开头添加符号说明（p vs P 在 on-policy 上下文）
8. REOPOLD 3.3× → 3.32×
