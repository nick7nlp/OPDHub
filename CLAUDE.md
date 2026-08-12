# CLAUDE.md — OPD Survey Project

## On session start

Check `.claude/pipeline_alerts.md` — if it exists and is non-empty, show the user
any recent alerts (pipeline failures, commit errors) before doing anything else.
After the user acknowledges, truncate the file.

## Project conventions

- `notes/paper_notes.json` is the single source of truth for paper metadata (V3 schema).
- `scripts/cron_pipeline_phase2_7.sh` is the daily automation pipeline (Phase 2-7).
- `scripts/codebuddy_opd_pipeline.sh` is the CodeBuddy-triggered, systemd-managed wrapper: it runs scout then Phase 2-7 under a lock.
- `scripts/tclaude_cron.sh` is retired and retained only as a rollback reference; it must not be scheduled.
- Never modify `Awesome-LLM-On-Policy-Distillation/` files manually — use `scripts/awesome_list_inserter.py`.
- OPD 三条件: (1) student rollouts during training, (2) concurrent teacher supervision, (3) per-step weight updates.

## Scope screening rules

- **三条件是唯一判据，`is_opd=analysis` 不等于合格。** 任何"合格 OPD"清单都必须逐篇校验三条件；
  `rollout_frequency` 为 `once-before-training` / `n/a` 或 `student_rollout_in_training != yes` 的一律剔除。
  （2026-08-12 教训：backlog 曾用 `is_opd in (yes, analysis)` 当合格条件，混入 5 篇离线工作。）
- **技术报告默认不管**，除非确有 OPD 方法创新。已裁定忽略：Kimi K3 `2607.24653`、Motif 3 `2608.09119`、
  Solar Open 2 `2607.20062`、KAT-Coder-V2.5 `2607.05471`、Mach-Mind-4-Flash `2607.09375`、
  OvisOCR2 `2607.13639`、GR2 `2606.31984`、Capek 0.5 `2608.06756`。
- **V4 已发表正文不回改。** 剔除只作用于 V5 及后续；V4 的 `main.tex` / `references.bib` 保持原状。
- **second-opinion (Gemini) 的 REJECT 不可直接采信**：它常以"新颖性/领域/非新方法"为由拒稿，
  而这些都不是 OPD 判据。必须回到三条件与原文公式复核。
