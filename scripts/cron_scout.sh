#!/usr/bin/env bash
# OPD daily scout — host cron entry.
#
# Cron schedule (intended): every weekday at 09:30 CST
#   30 9 * * 1-5 /apdcephfs_cq8/.../scripts/cron_scout.sh
#
# What it does:
#   1. Phase 0 PRE-CHECK (skips weekend automatically).
#   2. Phase 1 SCOUT (scout_arxiv.py --download --max 50).
#   3. Appends a result block to papers-meta/_pipeline_queue.md.
#
# Phase 2-7 follow-up now automated by cron_pipeline_phase2_7.sh (10:30 CST).
#
# Daily workflow:
#   - 09:30 this cron downloads candidates to pdfs/_staging/
#   - 10:30 cron_pipeline_phase2_7.sh runs deep-read + triage + insert + push

set -u

# cron strips env, ensure python3 + git resolve
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
export HOME="${HOME:-/root}"

PROJECT_ROOT="/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey"
LOG_DIR="${PROJECT_ROOT}/logs"
QUEUE="${PROJECT_ROOT}/papers-meta/_pipeline_queue.md"
SCOUT_OUT="/tmp/scout_arxiv_results.json"

mkdir -p "${LOG_DIR}"
DATE_CST=$(TZ='Asia/Shanghai' date '+%Y-%m-%d (%a)')
TIME_CST=$(TZ='Asia/Shanghai' date '+%H:%M')
LOG="${LOG_DIR}/cron-scout-$(TZ='Asia/Shanghai' date '+%Y-%m-%d').log"

cd "${PROJECT_ROOT}" || exit 2

# Phase 0 PRE-CHECK — exit 0 on weekday (proceed), exit 1 on weekend (skip silently)
if ! python3 scripts/scout_precheck.py --both >> "${LOG}" 2>&1; then
    {
        echo ""
        echo "## ${DATE_CST} — weekend skip (PRE-CHECK exit 1)"
        echo ""
    } >> "${QUEUE}"
    exit 0
fi

# Phase 1 SCOUT
python3 scripts/scout_arxiv.py --download --max 120 --output "${SCOUT_OUT}" >> "${LOG}" 2>&1
SCOUT_RC=$?

if [ ${SCOUT_RC} -ne 0 ]; then
    {
        echo ""
        echo "## ${DATE_CST} ${TIME_CST} — ❌ SCOUT FAILED (exit ${SCOUT_RC})"
        echo ""
        echo "See ${LOG} for details."
        echo ""
    } >> "${QUEUE}"
    exit "${SCOUT_RC}"
fi

# Parse candidate count
CAND=$(python3 -c "import json; d=json.loads(open('${SCOUT_OUT}').read()); print(len(d['new_candidates']))" 2>/dev/null || echo 0)

{
    echo ""
    echo "## ${DATE_CST} ${TIME_CST} — scout completed"
    echo ""
    if [ "${CAND}" -eq 0 ]; then
        echo "**0 candidates.** No follow-up needed."
    else
        echo "**${CAND} candidates** downloaded to \`pdfs/_staging/\`. Follow-up Phase 2-7 **pending**."
        echo ""
        python3 -c "
import json
d = json.loads(open('${SCOUT_OUT}').read())
for c in d['new_candidates']:
    print(f'- \`{c[\"arxiv_id\"]}\`  {c[\"title\"][:110]}')
"
    fi
    echo ""
} >> "${QUEUE}"

exit 0
