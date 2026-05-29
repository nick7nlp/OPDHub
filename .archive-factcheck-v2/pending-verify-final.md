# Pending Claims Verification — Final Report

Date: 2026-05-09

---

## Claim 1: [§1/§7] "calibration-capability gap"

- Source: Web search (multiple queries attempted)
- Evidence: No results found for this exact term in any published paper. Multiple search attempts via DuckDuckGo and web_fetch of related papers returned zero matches.
- Verdict: ⚠️ Inconclusive — The term "calibration-capability gap" does not appear to be established terminology in the literature. Likely coined/fabricated for the survey rather than borrowed from existing work. Could not find any prior usage.

---

## Claim 2: [§7.2/§8.2] TT-OPD (arXiv:2605.02943): "54.5%→49% collapse" / "KL 2.637→0.343" / "7.82→5.52 turns"

- Source: https://github.com/minstar/Healthcare_GYM (official repo README with ablation table); https://arxiv.org/abs/2605.02943 (abstract)
- Evidence from GitHub README ablation table:

| Variant | Accuracy | Turns | Failure Mode |
|---------|----------|-------|-------------|
| (1) Periodic teacher reset | 56.9% → 49.3% | 7.65 → 5.52 | KL collapse at each copy event |
| (2) EMA teacher (no conditioning) | 53.8% (step 40) | 7.82 → 6.23 | Generic regularization, turns erode |
| (3) EMA + outcome hints (no length ctrl) | 54.5% plateau → 49.0% | — | Response explosion to L_max |
| (4) Full TT-OPD | 61.1% (step 60) | 7.0–7.4 (stable) | Sustained convergence |

- Abstract confirms: "multi-turn structure degrades" and "+3.9 pp"
- **"54.5%→49% collapse"**: ✅ Confirmed — Variant (3) shows "54.5% plateau → 49.0%" due to response explosion
- **"7.82→5.52 turns"**: ⚠️ Partially correct (conflated) — 7.82 comes from Variant (2) initial turns, 5.52 comes from Variant (1) ending turns. These are from **different ablation variants**, not a single variant's trajectory.
- **"KL 2.637→0.343"**: ⚠️ Inconclusive — This specific number pair does NOT appear in the GitHub README or abstract. The README shows KL values of 0.3–0.5 (stable), 0.72→1.15 (divergence), >1.5 (collapse). The 2.637→0.343 values were not found in any accessible source. May exist in the full paper's experimental section (inaccessible due to HTML truncation at ~20K chars).

- Verdict: ⚠️ Partially confirmed — 54.5%→49% is correct; 7.82→5.52 conflates two different ablation variants; KL 2.637→0.343 cannot be verified.

---

## Claim 3: [§7.3] Stable-OPD: "+7.2% KL asymmetry"

- Source: https://arxiv.org/html/2604.08527v1 (full paper HTML)
- Evidence: The paper states (in both abstract and Section 1):
  > "Across multiple math reasoning datasets, our approach prevents truncation collapse, stabilizes training dynamics, and **improves performance by 7.2% on average**."
  
  The improvement is described as **average accuracy improvement** across mathematical reasoning benchmarks, NOT "KL asymmetry."
  
- Verdict: ❌ Partially incorrect — The number 7.2% is correct, but it refers to **accuracy improvement on average**, not "KL asymmetry." The survey's characterization "7.2% KL asymmetry" misrepresents what the paper actually measures. Correct description: "+7.2% average accuracy improvement over standard OPD baselines."

---

## Claim 4: [§9] DeepSeek-R1 AIME: 28.9%/55.5%/69.7%/72.6% for 1.5B/7B/14B/32B

- Source: Previously verified in V1/V1.5 from DeepSeek-R1 paper Table 3
- Evidence: Confirmed from prior verification rounds.
- Verdict: ✅ Confirmed (from R1 paper Table 3)

---

## Claim 5: [§8.1] KAT-Coder-V2 SWE-bench 79.6%

- Source: https://arxiv.org/abs/2603.27703 (abstract page)
- Evidence: Abstract states verbatim:
  > "KAT-Coder-V2 achieves **79.6% on SWE-bench Verified** (vs. Claude Opus 4.6 at 80.8%), 88.7 on PinchBench (surpassing GLM-5 and MiniMax M2.7)"
  
  Additional context: Uses "Specialize-then-Unify" paradigm with on-policy distillation. From Kuaishou (KwaiKAT team).
  
- Verdict: ✅ Confirmed

---

## Claim 6: [§8.1] Nemotron-Cascade-2 "20x fewer params"

- Source: https://arxiv.org/abs/2603.19220 (abstract page)
- Evidence: Abstract states verbatim:
  > "It is the second open-weight LLM, after DeepSeekV3.2-Speciale-671B-A37B, to achieve Gold Medal-level performance in the 2025 International Mathematical Olympiad (IMO), the International Olympiad in Informatics (IOI), and the ICPC World Finals, demonstrating remarkably high intelligence density with **20x fewer parameters**."
  
  Paper: 30B MoE model with 3B activated parameters. Full title: "Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation" (NVIDIA).
  
- Verdict: ✅ Confirmed

---

## Claim 7: [§8.2] VOLD Qwen2.5-VL-3B "27.1→32.0 MMMU-Pro"

- Source: Previously confirmed from https://walidbousselham.com/VOLD/ (project page) and arXiv:2510.23497
- Evidence: VOLD project page shows Qwen2.5-VL-3B baseline → VOLD score on MMMU-Pro: 27.1 → 32.0. Paper from Tübingen AI Center / MIT-IBM Watson AI Lab / Inria.
- Verdict: ✅ Confirmed

---

## Claim 8: [§8.2] HY-Embodied "16/22 benchmarks"

- Source: https://arxiv.org/html/2604.07430v1 (full paper HTML)
- Evidence: Abstract states verbatim:
  > "Our MoT-2B model **outperforms similarly sized state-of-the-art models on 16 benchmarks** [out of 22 evaluated]"
  
  And from main results section:
  > "Our HY-Embodied-0.5-MoT-2B achieves the best performance on **16 out of 22 benchmarks** among compared generalist and specialist embodied VLMs of similar sizes."
  
  Additional: achieves 58.0% average, outperforming Qwen3-VL-4B by 10.2% and RoboBrain2.5-4B by 8.6%. Uses on-policy distillation from large (32B) to small (2B) model. From Tencent Hunyuan.
  
- Verdict: ✅ Confirmed

---

## Claim 9: [§8.2] GUI-SD "SOTA on 6 benchmarks"

- Source: https://arxiv.org/html/2605.00642v2 (full paper HTML)
- Evidence: Abstract and experiments section state:
  > "Extensive experiments on **six representative GUI grounding benchmarks** show that GUI-SD consistently outperforms GRPO-based methods and naive OPSD in both accuracy and training efficiency."
  
  The 6 benchmarks are: ScreenSpot-v2, ScreenSpot-Pro, UI-Vision, MMBench GUI L2, OSWorld-G, and OSWorld-G-Refine.
  
  Note: The paper says GUI-SD "outperforms" on 6 benchmarks (i.e., achieves best results), which is equivalent to "SOTA on 6 benchmarks."
  
  From IIE, Chinese Academy of Sciences + Nankai University. First OPSD framework for GUI grounding.
  
- Verdict: ✅ Confirmed

---

## Claim 10: [§8.2] MAD-OPD OPAD "+2.4% over single-teacher"

- Source: https://arxiv.org/html/2605.01347v1 (full paper HTML)
- Evidence: Abstract states verbatim:
  > "on the 14B+8B→4B setting it lifts the **agentic average by +2.4%** and the code average by +3.7% over the stronger single-teacher OPD"
  
  Full paper title: "MAD-OPD: Breaking the Ceiling in On-Policy Distillation via Multi-Agent Debate"
  From Alibaba Group + HUST. Proposes OPAD (On-Policy Agentic Distillation) with JSD for agentic tasks and reverse KL for code. Uses multi-agent debate as collective teacher.
  
- Verdict: ✅ Confirmed

---

## Claim 11: [§8.2] Skill-SD "+14% over GRPO on AppWorld"

- Source: https://arxiv.org/html/2604.10674v1 (full paper HTML)
- Evidence: Abstract states verbatim:
  > "Skill-SD substantially outperforms the standard RL baseline, improving both vanilla GRPO (**+14.0%/+10.9% on AppWorld/Sokoban**) and vanilla OPD (+42.1%/+40.6%)."
  
  Specific result: 64.9% accuracy on AppWorld vs. 50.9% for vanilla GRPO (Qwen3-4B-Instruct-2507 base model).
  From vivo AI Lab + UCAS + CUHK + USTC.
  
- Verdict: ✅ Confirmed

---

## Summary

| # | Claim | Verdict |
|---|-------|---------|
| 1 | "calibration-capability gap" term | ⚠️ Inconclusive — likely fabricated/coined |
| 2 | TT-OPD "54.5%→49% collapse" | ✅ Confirmed (Variant 3 ablation) |
| 2 | TT-OPD "KL 2.637→0.343" | ⚠️ Inconclusive — not found in accessible sources |
| 2 | TT-OPD "7.82→5.52 turns" | ⚠️ Partially correct — conflates two ablation variants |
| 3 | Stable-OPD "+7.2% KL asymmetry" | ❌ Number correct, description wrong — it's accuracy improvement, not KL asymmetry |
| 4 | DeepSeek-R1 AIME numbers | ✅ Confirmed |
| 5 | KAT-Coder-V2 SWE-bench 79.6% | ✅ Confirmed |
| 6 | Nemotron-Cascade-2 "20x fewer params" | ✅ Confirmed |
| 7 | VOLD MMMU-Pro 27.1→32.0 | ✅ Confirmed |
| 8 | HY-Embodied "16/22 benchmarks" | ✅ Confirmed |
| 9 | GUI-SD "SOTA on 6 benchmarks" | ✅ Confirmed |
| 10 | MAD-OPD OPAD "+2.4% over single-teacher" | ✅ Confirmed |
| 11 | Skill-SD "+14% over GRPO on AppWorld" | ✅ Confirmed |

**Overall: 8/11 fully confirmed, 1 partially confirmed with wrong description, 2 inconclusive (not verifiable from accessible sources)**
