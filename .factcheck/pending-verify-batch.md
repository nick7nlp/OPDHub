# Fact-Check: OPD Survey V2 — Pending Verify Claims

Generated: 2026-05-09

---

## 1. [§1/§7] "calibration-capability gap" — 是否是自造术语？

**Claim:** "calibration-capability gap" 是论文中使用的术语

**Source:** Web search for exact phrase "calibration-capability gap"

**Evidence:** 在 DuckDuckGo 搜索 `"calibration-capability gap"` 返回 **0 结果**。额外搜索 `"calibration-capability gap" LLM distillation` 和 `"calibration capability gap" knowledge distillation` 也返回 0 结果。未找到任何其他学术论文使用该术语。

**Verdict:** ⚠️ Imprecise — 该术语很可能是综述自创的。未找到任何先前文献使用此确切短语。如作为综述的概念创新应明确标注为"we term/introduce"；如果不是，则需提供引用。

---

## 2. [§7.2/§8.2] TT-OPD: 54.5%→49% collapse / KL 2.637→0.343 / 7.82→5.52 turns

**Claim:** TT-OPD 论文中报告了 54.5%→49% accuracy collapse、KL 从 2.637→0.343、turns 从 7.82→5.52

**Source:** arXiv:2605.02943 ("Healthcare AI GYM for Medical Agents")

**Evidence:** 从论文 GitHub README (github.com/minstar/Healthcare_GYM) 的 ablation table 验证:
- **54.5%→49%**: 对应 Variant (3) "EMA + outcome hints (no length ctrl)" = "54.5% plateau → 49.0%" ✅ 匹配
- **7.82→5.52 turns**: 实际数据 — Variant (1) "Periodic teacher reset" 显示 7.65→5.52 turns；Variant (2) "EMA teacher (no conditioning)" 显示 7.82→6.23 turns。综述将 7.82 和 5.52 合并自不同 variants。
- **KL 2.637→0.343**: GitHub 页面中报告的 KL 值范围为 0.2–3.0（Failure Mode 3 中出现 KL 0.7–3.0），但未找到确切的 "2.637→0.343" 数字对。

**Verdict:** ⚠️ Imprecise — 54.5%→49% 准确匹配。但 "7.82→5.52 turns" 混合了两个不同 ablation variants 的数据（7.82 来自 variant 2，5.52 来自 variant 1）。KL "2.637→0.343" 未能在公开数据中验证到精确匹配。

---

## 3. [§7.3] Stable-OPD (luo2026demystifying) +7.2% KL asymmetry

**Claim:** Stable-OPD 通过 KL asymmetry 方法提升 +7.2%

**Source:** arXiv:2604.08527 ("Length Inflation and Stabilization Strategies for Large Language Models", by Feng Luo et al.)

**Evidence:** 论文 abstract 明确表述: "Across multiple math reasoning datasets, our approach prevents truncation collapse, stabilizes training dynamics, and **improves performance by 7.2% on average**." 论文正文确认方法包含 "reference-based divergence constraint with rollout mixture distillation"。

**Verdict:** ⚠️ Imprecise — "+7.2%" 数字正确（来自 abstract）。但论文标题是 "Length Inflation and Stabilization Strategies"，不是 "demystifying"，且 citation key "luo2026demystifying" 与实际论文标题不匹配。此外，方法的核心是 "reference-based divergence constraint + rollout mixture distillation"，将其简称为 "KL asymmetry" 可能是简化/误导性描述。论文分析的是 reverse-KL advantage 对 repetitive tokens 的 asymmetric 偏好（repetitive tokens receive larger advantages），这可能是 "KL asymmetry" 的来源。

---

## 4. [§9] DeepSeek-R1 AIME 28.9/55.5/69.7/72.6 for 1.5B/7B/14B/32B

**Claim:** DeepSeek-R1 蒸馏模型在 AIME 2024 上的 pass@1 分数为 1.5B=28.9, 7B=55.5, 14B=69.7, 32B=72.6

**Source:** arXiv:2501.12948 / GitHub (github.com/deepseek-ai/DeepSeek-R1)

**Evidence:** GitHub README 中的 benchmark table 明确列出:
| Model | AIME 2024 pass@1 |
|-------|-----------------|
| DeepSeek-R1-Distill-Qwen-1.5B | **28.9** |
| DeepSeek-R1-Distill-Qwen-7B | **55.5** |
| DeepSeek-R1-Distill-Qwen-14B | **69.7** |
| DeepSeek-R1-Distill-Qwen-32B | **72.6** |

**Verdict:** ✅ Correct — 所有四个数字完全匹配原文数据。

---

## 5. [§8.1] KAT-Coder-V2 SWE-bench 79.6%

**Claim:** KAT-Coder-V2 在 SWE-bench Verified 上达到 79.6%

**Source:** arXiv:2603.27703 ("KAT-Coder-V2 Technical Report")

**Evidence:** 论文 abstract 明确表述: "KAT-Coder-V2 achieves **79.6% on SWE-bench Verified** (vs. Claude Opus 4.6 at 80.8%)"

**Verdict:** ✅ Correct — 数字完全匹配。

---

## 6. [§8.1] Nemotron-Cascade-2 "20x fewer params than V3.2-Speciale"

**Claim:** Nemotron-Cascade-2 使用比 DeepSeek-V3.2-Speciale 少 20 倍的参数

**Source:** arXiv:2603.19220 ("Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation")

**Evidence:** 论文 abstract 明确表述: "It is the second open-weight LLM, after DeepSeekV3.2-Speciale-671B-A37B, to achieve Gold Medal-level performance in the 2025 International Mathematical Olympiad (IMO)... demonstrating remarkably high intelligence density with **20x fewer parameters**."
- Nemotron-Cascade-2: 30B MoE, 3B activated
- DeepSeekV3.2-Speciale: 671B total, A37B activated
- 比较基于总参数: 671B / 30B ≈ 22x（约 20x）

**Verdict:** ✅ Correct — 论文原文确认 "20x fewer parameters" 的对比对象就是 DeepSeekV3.2-Speciale。

---

## 7. [§8.2] VOLD Qwen2.5-VL-3B 27.1→32.0 MMMU-Pro

**Claim:** VOLD 方法将 Qwen2.5-VL-3B 在 MMMU-Pro 上从 27.1 提升到 32.0

**Source:** arXiv:2510.23497 / 项目主页 (walidbousselham.com/VOLD/)

**Evidence:** 项目主页 Table 1 明确列出:
| Model | MMMU-Pro (Vision) |
|-------|------------------|
| Qwen2.5-VL-3B (baseline) | **27.1** |
| VOLD (Ours) | **32.0** |

**Verdict:** ✅ Correct — 数字完全匹配。

---

## 8. [§8.2] HY-Embodied "16/22 benchmarks"

**Claim:** HY-Embodied MoT-2B 在 22 个 benchmarks 中的 16 个上取得最佳表现

**Source:** arXiv:2604.07430 ("Embodied Foundation Models for Real-World Agents")

**Evidence:** 论文 abstract 明确表述: "Our MoT-2B model **outperforms similarly sized state-of-the-art models on 16 benchmarks**" 以及 "spanning visual perception, spatial reasoning, and embodied understanding"。在 §1 Introduction 中进一步确认: "Our HY-Embodied-0.5-MoT-2B achieves the best performance on **16 out of 22 benchmarks** among compared generalist and specialist embodied VLMs of similar sizes."

**Verdict:** ✅ Correct — "16/22 benchmarks" 完全匹配原文。

---

## 9. [§8.2] GUI-SD "SOTA on 6 benchmarks"

**Claim:** GUI-SD 在 6 个 benchmarks 上达到 SOTA

**Source:** arXiv:2605.00642 / 项目主页 (zhangyan-ucas.github.io/GUI-SD/)

**Evidence:** 论文 abstract: "Extensive experiments on **six representative GUI grounding benchmarks** show that GUI-SD consistently outperforms GRPO-based methods and naive OPSD in both accuracy and training efficiency." 项目主页 results table 列出 6 个 benchmarks: SSP (ScreenSpot-Pro), SS2, UIV, OSW-G, OSW-GR, MMG。GUI-SD 在所有 6 个上均为最优。

注意：原文说的是 "consistently outperforms" 而非严格的 "SOTA on all 6"。项目主页 Comparison with SOTA 部分显示 GUI-SD 在部分 benchmarks 上超过了其他 SOTA 方法（如 ScreenSpot-Pro 60.7% vs Propose-then-Critic 58.7%），但 "SOTA on 6 benchmarks" 是相对于 GRPO-based methods 和 naive OPSD 的比较。

**Verdict:** ⚠️ Imprecise — GUI-SD 确实在 6 个 benchmarks 上测试并显示优于 GRPO/naive OPSD。但 "SOTA" 需要看对比范围：相对于同类方法确实最优，但并非在所有 6 个 benchmarks 上绝对 SOTA（有些 test-time scaling 或大模型蒸馏方法在个别 benchmark 上更高）。综述的表述若为 "outperforms GRPO on 6 benchmarks" 则完全准确。

---

## 10. [§8.2] MAD-OPD OPAD +2.4% over single-teacher

**Claim:** MAD-OPD 在 OPAD metric 上比 single-teacher 提升 +2.4%

**Source:** arXiv:2605.01347 ("Multi-Agent Debate-driven On-Policy Distillation")

**Evidence:** 根据之前的搜索和 fetch 确认论文存在且涉及多教师辩论框架的 on-policy distillation (Alibaba/HUST)。论文 abstract 中提到在 agentic 场景上的改进。由于 HTML 版本截断，无法直接验证精确的 "+2.4%" 数字在表格中的位置。

**Verdict:** ⚠️ Inconclusive — 论文确实存在于 arXiv:2605.01347，内容关于 multi-agent debate-driven OPD，但无法从公开可读内容中精确验证 "+2.4% over single-teacher" 这个具体数字。

---

## 11. [§8.2] Skill-SD +14% over GRPO on AppWorld

**Claim:** Skill-SD 在 AppWorld 上比 GRPO 提升 +14%

**Source:** arXiv:2604.10674 / 项目主页 (skill-sd.github.io)

**Evidence:** 项目主页 abstract 明确表述: "Skill-SD substantially outperforms the standard RL baseline, improving both **vanilla GRPO (+14.0%/+10.9% on AppWorld/Sokoban)** and vanilla OPD (+42.1%/+40.6%)."

Results table 验证:
| Method | AppWorld Acc. |
|--------|-------------|
| Base Model | 8.8% |
| Vanilla GRPO | 50.9% |
| Skill-SD (Ours) | **64.9%** |

64.9% - 50.9% = **+14.0%** (absolute percentage points)

**Verdict:** ✅ Correct — "+14%" (实际为 +14.0 pp) over GRPO on AppWorld 完全匹配原文。

---

## Summary

| # | Claim | Verdict |
|---|-------|---------|
| 1 | "calibration-capability gap" 术语 | ⚠️ 可能自造，无先例引用 |
| 2 | TT-OPD 54.5%→49% / KL 2.637→0.343 / 7.82→5.52 | ⚠️ 部分匹配，部分混合不同 variants |
| 3 | Stable-OPD +7.2% | ⚠️ 数字正确，"KL asymmetry" 描述略简化 |
| 4 | DeepSeek-R1 AIME 28.9/55.5/69.7/72.6 | ✅ 完全正确 |
| 5 | KAT-Coder-V2 SWE-bench 79.6% | ✅ 完全正确 |
| 6 | Nemotron-Cascade-2 "20x fewer params" | ✅ 完全正确 |
| 7 | VOLD MMMU-Pro 27.1→32.0 | ✅ 完全正确 |
| 8 | HY-Embodied 16/22 benchmarks | ✅ 完全正确 |
| 9 | GUI-SD "SOTA on 6 benchmarks" | ⚠️ 表述略过度，应为 "outperforms GRPO on 6 benchmarks" |
| 10 | MAD-OPD +2.4% over single-teacher | ⚠️ 无法从公开页面精确验证 |
| 11 | Skill-SD +14% over GRPO on AppWorld | ✅ 完全正确 |

**Overall: 6/11 ✅ Correct, 5/11 ⚠️ Imprecise/Inconclusive, 0/11 ❌ Wrong**
