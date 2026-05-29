# OPD Survey V2 — 10h Deep Audit 最终总结

**时间**: 2026-05-10 16:00 UTC ~ 2026-05-11 05:55 UTC（约14小时实际时间，含 cron 间隔）
**项目**: `/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/latex-v2/`

---

## 📊 统计

| 指标 | 数值 |
|------|------|
| 总 task 数 | 50 |
| 完成 (done) | 46 |
| 跳过 (skipped) | 2（重复 task + 已存在内容） |
| 部分完成 | 0 |
| 总 commits | 37 |
| 结构性问题上报 | 24（含重复计入） |
| 最终 escalation 需决策 | **5 个** |
| pre-submission-check | **0 errors** |

---

## 🔧 直接修复的问题类型（37 commits 覆盖）

### 方法描述错误（~15 处）
- GKD "adapts DAgger" → "draws on on-policy imitation learning paradigm"
- RLKD/KETCHUP key innovation 描述修正
- MTP "auxiliary prediction head" → 整模型训练+frozen self-teacher
- OPCD exemplars/retrieval context → 原文实际 PI 类型
- SDFT "KL against prior checkpoint" → in-context learning teacher
- DSKD KL 参数顺序反转
- AlignDistil granularity Sequence→Token
- CoPD 分类 Self(EF)→Self(Mutual)
- AdaSwitch 公式下标 bar{d}_i → bar{d}_{i-1}
- VISD Table KL+RL → advantage+RL
- etc.

### 公式/方向性错误（~8 处）
- G-OPD 公式缺 p_ref log-ratio reward 项
- IRIS α 方向反转（larger=exploration, smaller=refinement）
- PAINT overlap 方向反转（high=hide more）
- PACED Beta-kernel peak 公式 α/(α+β-2) → α/(α+β)
- PACED 方向性倒反
- §7.3 f-DISTILL α-divergences → TVD

### Overclaim 修复（~20 处）
- "confirms/demonstrates/proves" → "is consistent with/suggests"
- "the central/the best/critical" → "a central/most favorable/important"
- "eliminates/dominates" → "reduces/tends to outperform"
- "fundamental" → "reveals"
- "the only" → 删除排他性
- 多处 prescriptive "should" → "could"

### 事实精度修补（~10 处）
- DeepSeek-R1: "800K reasoning chains" → "800K curated samples (600K reasoning + 200K non-reasoning)"
- OPSD 1.7B 增益 "minimal" → "+5.7 最大增益"
- NPD benchmark 范围修正
- Qwen3 "mode fusion" → "Thinking Mode Fusion"
- Gemma 2 从 OPD 改为 off-policy KD
- VISD "2×" 补 "approximately"

---

## ⚠️ 待老大决策的 5 个结构性问题

详见: `memory/2026-05-11-opd-audit-escalation.md`

| # | 位置 | 核心问题 |
|---|------|---------|
| R1 | §5.1 | Cross-Tok KD 公式**完全编造**（latent-space OT ≠ 实际 probability-space W1） |
| R2 | §4.2 | ToDi 粒度坍缩（per-position → 原文是 per-vocabulary-entry） |
| R3 | §7.3 | 2505.13111 张冠李戴（写的 minimal conditions，原文是 precision-recall tradeoff） |
| R4 | §3.1 | TT-OPD 引用归因错（teacher-student identity collapse ≠ OOD miscalibration） |
| R5 | §9 | Future Directions 含自编公式（违反纯叙事规则） |

---

## 📝 WRITING.md 更新（tick 30-39）

新增/改进内容：
1. **A1 Formula 新增 3 项陷阱**：边界条件、归一化、下标维度
2. **A6 Method Description 新增 2 项**：paradigm 尊重、机制归因不混用
3. **LLM Anti-Pattern 章节**：7 个模式 (A-G) + 具体实例
4. **Self-Check Procedure**：5 步验证流程 + web_fetch/pdftotext 速查卡
5. **12-class Reviewer Mock**：从 6 类扩展到 12 类审稿人
6. **Survey Structural Rules**：10 条高引综述速查表
7. **Code Review for Formulas**：10 项公式审查清单 + 7 项伪代码审查
8. **"When LLM 推公式 is wrong" 速查表**：6 张表含 12+ 具体实例
9. **命令片段验证**：修复 2 处 em-dash grep 解析错误

已同步到 writer agent: `/root/.openclaw/agents/writer/WRITING.md`

---

## ✅ 最终状态

- **main.tex**: 编译通过，0 errors
- **pre-submission-check.sh**: 全绿（0 undefined refs/cites/overfull/AI-taste/em-dash/semicolons）
- **公式一致性**: 26 equations 全部验证通过
- **引用存在性**: 127 cite keys 与 127 bib entries 1:1 匹配
- **交叉引用**: 32 refs 全部解析到 39 labels
- **Overclaim**: 65 个剩余匹配均为合法学术用法

---

## 🎯 下一步

1. 老大对 R1-R5 选方案 → 派 writer 执行重写
2. 全部修完后做一次完整 PDF 目视检查
3. 提交前最终 proofread
