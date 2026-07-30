# CLAUDE.md — OPD Survey Project

## On session start

Check `.claude/pipeline_alerts.md` — if it exists and is non-empty, show the user
any recent alerts (pipeline failures, commit errors) before doing anything else.
After the user acknowledges, truncate the file.

## Project conventions

- `notes/paper_notes.json` is the single source of truth for paper metadata (V3 schema).
- `scripts/cron_pipeline_phase2_7.sh` is the daily automation pipeline (Phase 2-7).
- `scripts/tclaude_cron.sh` is the OS-cron-triggered wrapper (permanent, unattended).
- Never modify `Awesome-LLM-On-Policy-Distillation/` files manually — use `scripts/awesome_list_inserter.py`.
- OPD 三条件: (1) student rollouts during training, (2) concurrent teacher supervision, (3) per-step weight updates.
