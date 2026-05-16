#!/bin/bash
# OPD Survey 10-hour deep-audit driver (invoked by cron every 12 min)
# State file: /tmp/opd_audit_state.json
# Log file: /root/.openclaw/workspace/memory/2026-05-10-opd-10h-audit.log

STATE=/tmp/opd_audit_state.json
LOG=/root/.openclaw/workspace/memory/2026-05-10-opd-10h-audit.log
REPORT=/root/.openclaw/workspace/memory/2026-05-10-opd-deep-read-report.md
SURVEY=/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/latex-v2
PDFDIR=/apdcephfs_cq8/share_1324356/nickmysong/openclaw_fsp/papers/opd
TXTDIR=/tmp/opd_pdftxt

mkdir -p $TXTDIR
echo "=== $(date -u +'%F %T UTC') === tick $(cat $STATE 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tick",0))' 2>/dev/null || echo 0)" >> $LOG

# Init state
if [ ! -f $STATE ]; then
  python3 <<'EOF' > $STATE
import json
state = {
  "tick": 0,
  "start": "2026-05-10T16:00:00Z",
  "budget_minutes": 600,
  "phase": "verify",
  "tasks": [
    # Phase 1 (ticks 1-30): section verification
    "§3.1 Method Landscape — verify GKD/MiniLLM/DistiLLM descriptions vs 2306.13649/2306.08543/2402.03898",
    "§3.2 Method Comparison Table (rows 1-12) vs PDFs",
    "§3.2 Method Comparison Table (rows 13-24) vs PDFs",
    "§4.1 Fixed Divergence (GKD, DistiLLM, MiniLLM formulas) vs PDFs",
    "§4.1 KETCHUP, constrained KD (2504.19024, 2509.22921) vs PDFs",
    "§4.2 Adaptive Divergence (AKL, TAID, DistiLLM-2 2503.07067) vs PDFs",
    "§4.3 RL-Augmented (G-OPD, GRPO-related, etc) vs PDFs",
    "§5.1 White-Box Logit (DSKD, cross-tokenizer) vs PDFs",
    "§5.2 Black-Box (Lion, OVD, ThinkTuning, GAD) vs PDFs",
    "§5.3.1 Privileged Info (OPSD, HDPO, GATES) vs PDFs",
    "§5.3.1 Behavioral PI (OPCD, OPSDL, OEL, CRISP, GUI-SD, MSD) vs PDFs",
    "§5.3.1 PBSD (pbsd2026) method description + DPO claim vs PDF",
    "§5.3.1 TT-OPD (ttopd2026) method description vs PDF",
    "§5.3.1 VISD (lin2026visd) method description + 2x claim vs PDF",
    "§5.3.2 Self-Play (SPIN, IRIS, π-Play, PAINT) vs PDFs",
    "§5.3.2 Self-Play (SDFT, MTP, Self-Distilled RLVR, SSD) vs PDFs",
    "§5.3.3 External Feedback (SD-ZERO, SDPO, RLTF, SRPO) vs PDFs",
    "§6.1 Token/Sample Weighting vs PDFs",
    "§6.2 Curriculum (PACED, Uni-OPD, TCOD, Semantic Bootstrap, Retaining by Doing) vs PDFs",
    "§6.3 Compute Optimization vs PDFs",
    "§7.1 Success Conditions vs PDFs",
    "§7.2 Failure Modes vs PDFs",
    "§7.3 Unified Theoretical Perspectives vs PDFs",
    "§7.4 On-Policy vs Off-Policy (DeepSeek-R1 case) vs PDFs",
    "§8.1 Industrial Deployment (Qwen3, DeepSeek-V4, Gemma2, MiMo-V2, KAT-Coder, Nemotron-Cascade, ORBIT) vs PDFs",
    "§8.2 Emerging Domains (VOLD multimodal, cross-lingual, audio) vs PDFs",
    "§8.3 System-Level Integration vs PDFs",
    "§8.4 When to Use vs PDFs",
    "§8.5 Distillation Tax vs PDFs",
    "§9 Open Problems vs PDFs (check for prescriptive overclaim)",
    # Phase 2 (ticks 31-40): WRITING.md rule extraction
    "WRITING.md: Extract 5 new rules from this audit's findings — update A1 Formula / A6 Method Description sections",
    "WRITING.md: Add 'LLM-generated text patterns' anti-pattern section (concrete examples from our fixes)",
    "WRITING.md: Rewrite Self-Check Procedure to include cite-paper rule (`web_fetch arxiv.org/html/ID` + `pdftotext` commands)",
    "WRITING.md: Add '12-class Reviewer Mock' expansion — reviewer-persona checks",
    "WRITING.md: Consolidate high-citation survey structural rules (sampled surveys → extract 10 cross-cutting patterns)",
    "WRITING.md: Code review section for embedded code/formulas",
    "WRITING.md: Add 'When LLM推公式 is wrong' reference table (entropy term / factor / sampling distribution traps)",
    "WRITING.md: Promote WRITING.md → SOUL.md bridge: 1-line link",
    "WRITING.md: Validate example command snippets actually run",
    "WRITING.md: Final compile + sync to writer agent",
    # Phase 3 (ticks 41-50): issue triage
    "Triage report issues — classify by severity (fix/revise/accept-with-hedge)",
    "Apply fixes for severity=fix issues",
    "Apply hedging for severity=hedge issues",
    "Escalate severity=revise issues to boss in report",
    "Re-run pre-submission-check.sh — ensure all greens",
    "Formula consistency final sweep (grep all equations, cross-check symbols)",
    "Citation existence final sweep (verify every \\citep resolves)",
    "Cross-ref final sweep (every \\ref resolves)",
    "Hedging final sweep (check overclaim word list in grep)",
    "Final commit + summary write-up to boss"
  ]
}
json.dump(state, open("/tmp/opd_audit_state.json","w"), indent=2, ensure_ascii=False)
EOF
fi

echo "audit tick begin" >> $LOG
