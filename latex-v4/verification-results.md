# v4 全文核对校验结果（2026-06-06）

经过六阶段系统核查，**52 篇新插入论文 + 现有结构** 全部通过。

## 阶段 0：编译基线
- 清空 .aux/.bbl/.log/.pdf 后重新构建：pdflatex × 4 + bibtex × 1
- **结果**：0 undefined ref/cite，0 Warning，**84 pages, 626 KB**

## 阶段 1：cite-key vs .bib entry 对齐
| 指标 | 值 |
|---|---:|
| 唯一 \cite* keys | 208 |
| references.bib + references_background.bib 条目 | 208 |
| Cited but missing | **0** |
| Entry but unused | **0** |
| .bib 重复 key | **0** |

完美 1:1 对齐。

## 阶段 2：52 篇方法描述事实核对
逐篇对比 paper_notes.json 的 `summary` + `key_components` + `on_policy_mechanism` 与 main.tex 中的描述：
- 52/52 篇均有且仅有 1 次 \citep（无遗漏，无重复）
- 关键参数全部对得上：
  - ORPO-Distill: `K=8, λ=1, ϕ=0.5` ✓
  - MAIGO: `21.7% LiC reduction` ✓
  - Skill-Conditioned Gated SD: `r ∈ {-1, +1}` ✓
- 50 个新方法名（ORPO-Distill / OPD+ / Bridging / DuDi / OmniOPD / AVSD / SSD / ROSD / VPG / HINT-SD / SD-Search / Search-E1 / MAIGO / Canonical-Context / COMAP / Vision-OPD / TOD Proactivity / It-Takes-Two / OPCT / Visual-Advantage OPD / Filter-Then-Reweight / Less-is-More / DeltaPrompts / f-OPD / TRBB / Adaptive Teacher Refresh / CEI / POPD-TOPD / SafeSteer / MOTAB / Counteraction MOPD / Physics-Guided SD / Safety-Tax-OPD 等）全部在 main.tex 中至少出现一次。
- 0 处误归属（每篇放在与其 method 主旨匹配的章节）。

## 阶段 3：cross-ref 完整性
- \label 数: 46
- \ref 数（unique）: 37
- Refs without label（broken refs）: **0**
- 9 个 orphan labels 都是 `sec:intro` / `sec:conclusion` / `subsec:emerging` 等顶级章节锚点，未被 \ref 是常态，不算缺陷。

## 阶段 4：写作铁律严格自查（仅对 21 段新插入内容）
精确段落级 grep（boundary = 第一个 `\n\n` 段尾）：

| 类别 | 命中 |
|---|---:|
| AI-taste（delves/reveals/highlights/notably/significantly/novel/leverages/...）| **0** |
| Overclaim（confirms/demonstrates/the best/the optimal/the standard/must/always/never/eliminates/guarantees/...）| **0** |
| Intensifier（particularly/remarkably/dramatically/...）| **0** |
| em-dash / en-dash / triple-dash | **0** |
| prose colon `[a-z]: [a-z]` | **0** |
| prose semicolon `[a-z]; [a-z]` | **0** |
| sentence-start However/Moreover/Furthermore/Additionally | **0** |
| 平行罗列 anti-pattern | **0** |

**21 段新内容总长 33,735 字符，0 违规。**

## 阶段 5：数字、命名、casing 一致性
- OPD / OPSD / RLVR / GRPO 全文大小写一致（OPD=363, OPSD=48, RLVR=28, GRPO=72）
- "On-Policy Distillation"（Title Case，标题用） vs "on-policy distillation"（lowercase，body 用）：4 vs 41，符合 CLAUDE.md 约定
- 所有数学符号在 inline math 内（`$K{=}8$`, `$\phi{=}0.5$`, `$\lambda{=}1$`），未泄漏到 prose
- Qwen3 / Llama-family / Southeast Asian 等模型/语种命名一致

## 阶段 6：与 v3 基线（main.tex.bak.20260603）的违规增量
| 词族 | v3 基线 | v4 (插完52篇) | Delta |
|---|---:|---:|---:|
| AI-taste 18 词总和 | (...) | (...) | **+0** |
| Overclaim 14 词总和 | (...) | (...) | **+0** |
| `the standard` | 6 | 5 | -1（修订时换为 conventional）|
| `must` | 22 | 21 | -1 |
| `guarantees` | 8 | 7 | -1 |

**新插入 21 段未引入任何新违规，反而顺手优化掉 3 处既有 hit。**

---

## 最终交付
- main.tex（1 419 行，353 KB）
- references.bib（190 条 OPD 方法）+ references_background.bib（18 条背景）= 208 条 .bib，与 \cite 1:1
- main.pdf（84 页，626 KB）
- 备份：references.bib.bak.20260606-pre52, main.tex.bak.20260603
- 计划文档：insertion-plan-52.md
- 历史日志：CHANGELOG-v4.md（已附 2026-06-06 条目）

**结论**：v4 已达到 0 undefined / 0 Warning / 0 写作铁律违规的可发布水准。

---

## 第二轮深度校验（2026-06-06，多角度）

### 阶段 A：方法简称是否生造（5 处修正）
比对每篇 paper_notes 标题/摘要 vs 我使用的方法简称，发现 5 处生造或不严谨：

| arxiv | 修正前（生造） | 修正后（忠实于论文） |
|---|---|---|
| 2606.00424 | Weak-Critics OPD | On-Policy Critique Distillation |
| 2605.17497 | SSD | Self-Supervised OPD |
| 2605.20258 | It-Takes-Two | It Takes Two |
| 2606.03532 | Adaptive Teacher Refresh | Adaptive Teacher-Refresh |
| 2606.05122 | Self-Evaluation OPD | \citet{2606.05122} |
| 2605.15239 | Reducing-the-Safety-Tax-OPD | \citet{2605.15239} |

剩余的 "Token-Teachability OPD" / "World-Model PI" / "Decomposed-OPD" / "TOD Proactivity" / "Canonical-Context OPD" / "Counteraction-Aware MOPD" 都与论文标题或 paper_notes 关键词一致，保留。

### 阶段 B：时序声明核对
对所有 "extends/builds on/parallels/inverts/follows/recovers" 等时序触发词逐一检查：
- Distributional DAgger (2606) ←returns to← DAgger (2010) ←motivates→ GKD (2023) ✓
- Direction-Adaptive (2605.22) ←similar in spirit to← AntiSD (2605.11) ✓ (later, similar concept)
- World-Model PI (2606.03) ←extends← AVSD/Critique (2605.20+2606.00) ✓
- SD-PG (2606.04) ←builds on← RLSD (2604.03) ✓
- Visual-Adv-OPD (2605.21) ←parallels← Decomposed-OPD (2606.00) ✓
- POPD/TOPD (2605.31) ←consistent with← FOPD (2602.15) ✓

无反向 chronology。

### 阶段 C：Tables 漏行检测 + 修正
原 Tables 4-7 (fixed/adaptive/RL/whitebox/blackbox/selfdistill/efficiency) **缺 48 个新行**。逐表补全：
- `tab:methods_fixed_div`: +5 行 (OPD+ / Bridging / Decomposed-OPD / Surgical-PT / Distributional DAgger)
- `tab:methods_adaptive_div`: +6 行 (Position-Weighted-OPSD / Direction-Adaptive / Token-Teachability / Lookahead / RAFT / Trust-Region OPD)
- `tab:methods_rl`: +4 行 (AMR-SD / OPPO / StepOPSD / Self-Eval OPD)
- `tab:methods_whitebox`: +2 行 (Pair-In Pair-Out / DuDi)
- `tab:methods_blackbox`: +2 行 (ORPO-Distill / OmniOPD)
- `tab:methods_selfdistill`: +19 行（含 §5.3.1×6 + §5.3.2×12 + §5.3.3×1）通过新增 \multicolumn 分组标题"Recent additions (2026 batch)"
- `tab:methods_efficiency`: +10 行（含 §6.1×3 + §6.2×5 + §6.3×2）通过新增 \multicolumn 分组标题
- §7.2 / §8.1 无表（prose-only），不需补

### 阶段 D：插入接缝流畅性（2 处修正）
检查 21 段插入处的"prev tail → NEW first → NEXT first"：
1. **§6.1→§6.2 接缝**: 原 reactive→proactive 过渡段在我新插入的 "Multimodal advantage" 段前，造成 "motivating the curriculum methods below" 之后突然又出现 weighting 内容。**修复**：把过渡段移到新段之后，恢复 "weighting 末尾→curriculum 开头" 的自然顺序。
2. **§8.1 五-pattern 列表**: 我的 "Safety-tax reduction" 段插在 4th 与 5th pattern 之间，可能让读者误以为它是 6th pattern。**修复**：把它移到"These five patterns reflect..."总结段之后，改写开头为"Orthogonal to the five deployment patterns above..."明确边界。

### 阶段 E：评价/Limitation/Novelty 用词
21 段插入内 0 命中：limitation / weakness / novelty / breakthrough / SOTA / pioneers / unique / unprecedented / paradigm shift。
"exceeded" 命中 1 次但是技术阈值描述（divergence threshold is exceeded），放行。

### 阶段 F：跨节引用语义对应
新段中所有 6 处 Section~\ref：
| 引用 | 目标 label → section title | 准确性 |
|---|---|---|
| Section~\ref{subsec:adaptive_div} | "Adaptive Divergence Objectives" | ✓ |
| Section~\ref{subsec:fixed_div} (×2) | "Fixed Divergence Objectives" | ✓ |
| Section~\ref{subsec:external_feedback} | "External Feedback" | ✓ |
| Section~\ref{subsec:compute} | "Compute Optimization" | ✓ |
| Section~\ref{subsec:self_pi} | "Privileged Information" | ✓ |

### 阶段 G：全文铁律最终扫
- em-dash / en-dash / triple-dash / prose colon / prose semicolon / sentence-start However-Moreover-Furthermore-Additionally：**全部 0**
- 既有命中（the best×3 / the optimal×7 / must×21 / never×5 / guarantees×7 等）均为 v3 baseline 即有的技术描述（"the best-tuned baseline"、"theoretical guarantees" 等），不是我新引入。

## 最终编译
- pdflatex × 4 + bibtex × 1
- **0 undefined ref / cite, 0 Warning, 84 pages, 632 KB**

## 第二轮校验小结
- 5 处方法名生造已修正
- 2 处段落接缝已修复
- 7 张分类表共补 48 行（每表附"Recent additions (2026 batch)"分组标题）
- cross-section refs / chronology / 写作铁律全清
