# Round 00 — Loop Initialization (2026-05-08 15:51 UTC)

## Baseline
- Tex: `latex-v2/main.tex` @ 1219 lines, 57 pages, 118 citations, 0 errors
- Bib: `latex-v2/references.bib` @ 118 entries
- HEAD: 7537807 (§9 Future Directions expansion)
- PDFs: 116 files in `pdfs/` + 2 in `/tmp/opd_papers/`

## Section line ranges (from grep `\section|\subsection`)
```
L82   §1  Introduction
L109  §2  Background and Unified Math
L122  §2.1 Classical KD
L152  §2.2 Off-Policy Exposure Bias
L164  §2.3 Unified f-Divergence
L195  §2.4 Distillation Scaling Laws
L200  §3  Landscape and Practitioner Guide
L205  §3.1 Method Landscape
L324  §3.2 Method Comparison Table
L529  §3.3 Decision Tree
L562  §4  Objective Functions
L567  §4.1 Fixed Divergence
L710  §4.2 Adaptive Divergence
L729  §4.3 RL-Augmented
L760  §5  Signal Source
L773  §5.1 White-Box
L802  §5.2 Black-Box
L833  §5.3 Self-Distillation
L838  §5.3.1 Privileged Information
L867  §5.3.2 Self-Play
L896  §5.3.3 External Feedback
L911  §6  Training Dynamics
L918  §6.1 Token/Sample Weighting
L939  §6.2 Curriculum
L964  §6.3 Compute Optimization
L993  §7  Understanding OPD
L1000 §7.1 Success Conditions
L1017 §7.2 Failure Modes
L1038 §7.3 Unified Theoretical Perspectives
L1055 §7.4 Decision Framework (On- vs Off-Policy)
L1077 §8  Applications
L1082 §8.1 Industrial Deployment
L1109 §8.2 Emerging Domains
L1130 §8.3 System-Level Integration
L1139 §8.4 When to Use On- vs Off-Policy
L1148 §8.5 Distillation Tax
L1159 §9  Open Problems and Future Directions
L1194 §10 Conclusion
```

## Schedule kickoff
- Cron `opd-v2-deep-read-loop` every 10 min, first run ~23:51:53 CST (15:51:53 UTC)
- Planned end: 2026-05-09 01:50 UTC (10 hours, ~60 ticks)
- Each tick does one (section, mode) from state.json rotation
- State tracker increments `round` at end of each tick

## Task-to-round mapping (first 60 ticks)

```
round 0 → mode=READ    section=§1 Introduction
round 1 → mode=VERIFY  section=§1
round 2 → mode=DEEPEN  section=§1
round 3 → mode=POLISH  section=§1
round 4 → mode=COMPILE section=§1
round 5 → mode=READ    section=§2
... etc
```

Each section gets 5 modes × 1 pass. 12 sections × 5 modes = 60 ticks.

## Pre-existing fact-check hint
Bundle A/B/C researchers spawned earlier — Bundle A returned early with no output; B/C still running. Their outputs (if written) will be in `.factcheck/bundle-*.md` and loop rounds can cross-reference.

## Ready
Loop initialized. Round 00 is this file. Round 01 will be the first cron-triggered agent.
