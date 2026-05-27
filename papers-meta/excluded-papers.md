# OPD Excluded Papers Log

记录被精读后排除的论文及原因。Pipeline 不再考虑这些论文。

## 2026-05-19 Cleanup (V3 deep-read pipeline 第一次系统性清理)

### 老论文 (4 篇 — 超出 daily window)
日期窗口纪律：daily scout 只接当天 + 前一天提交的论文，历史漏论文不进 daily pipeline。

| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2502.02671 | On Teacher Hacking in Language Model Distillation (DeepMind, ICML 2026) | Outside date window (2025-02). V3 verdict: is_opd=analysis (§7.2 失败模式分析), 但属于历史 backfill, 不进 daily |
| 2505.18952 | Online Knowledge Distillation with Reward Guidance | Outside date window (2025-05). V3 verdict: is_opd=yes (§4.3) |
| 2510.02227 | More Than One Teacher: Adaptive Multi-Guidance Policy Optimization | Outside date window (2025-10). V3 verdict: is_opd=yes (§5.3.1) |
| 2602.12262 | T3D: Few-Step Diffusion Language Models via Trajectory Self-Distillation (NeurIPS 2025) | Outside date window (2026-02), 且 V3 verdict: is_opd=no, not-applicable — trajectory 预先一次性生成, 不是 in-loop rollout |

### Not-OPD (1 篇)
| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2605.15417 | f-Trajectory Balance: A Loss Family for Tuning GFlowNets, Generative Models, and LLMs (ICML 2026) | V3 verdict: is_opd=no — 提出 f-divergence loss family for RL fine-tuning, 没有 teacher-student 架构, 不是蒸馏方法 |

### 灰色 (2 篇 — 非 OPD 主线方法)
| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2604.20244 | Hybrid Policy Distillation for LLMs | V3 verdict 判 yes (§4.1), 但只有 single-token sampling 不是 full rollout, 主线非 OPD |
| 2604.18963 | Distillation Traps and Guards: A Calibration Knob for LLM Distillability | V3 verdict 判 yes (§5.1), 但论文核心是 teacher-side calibration, 用 GKD trainer 跑实验, 是 OPD 工具不是 OPD 方法贡献 |

### 本质是 RL (2 篇 — 标榜 distillation 但本质是 RL)
| arXiv ID | Title | Verdict |
|----------|-------|---------|
| 2605.15726 | Nudging Beyond the Comfort Zone: Efficient Strategy-Guided Exploration for **RLVR** | 标题就是 "for RLVR"; verifier reward 是主信号, distillation term 只是辅助 loss; 删掉 distillation term 主要贡献还在, 删掉 RL 部分论文垮掉 → RL 是体, distill 是辅 |
| 2604.02621 | **Reinforcement Learning-based** Knowledge Distillation with LLM-as-a-Judge | 标题就是 "RL-based KD", 用 PPO/GRPO 训练, judge 当 reward signal — 本质是 RLAIF (RL with AI Feedback), 把 teacher 当 reward, 不是 teacher logit distillation |

## Pipeline 改进
- daily scout DATE WINDOW: 只接当天 + 前一天的 arXiv 提交 (今天 yymm 或上月最末尾)
- V3 deep-read 是收录的强制 gate, abstract-only 判断不可信
- RL vs OPD 边界: 看核心目标是不是 distillation, RL 是不是体
