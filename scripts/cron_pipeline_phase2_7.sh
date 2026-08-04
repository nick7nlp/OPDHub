#!/usr/bin/env bash
# OPD daily pipeline Phase 2-7 — automated follow-up after Phase 1 scout.
#
# Cron schedule (intended): every weekday at 10:30 CST (1h after scout)
#   30 10 * * 1-5 /apdcephfs_cq8/.../scripts/cron_pipeline_phase2_7.sh
#
# What it does:
#   Phase 2: batch deep-read (LLM API) on all un-read PDFs in _staging/
#   Phase 3: triage — keep OPD=yes, exclude OPD=no (mv to trash, log to excluded-papers.md)
#   Phase 3.5: 3-condition filter — reject false-positives (self-play, off-policy, analysis-only)
#   Phase 4: awesome list inserter — add confirmed OPD papers to README
#   Phase 5: refresh known_arxiv_ids.txt
#   Phase 6: (placeholder) loss-evolution / heatmap refresh
#   Phase 7: git commit + push
#
# Safety:
#   - deep-read uses --from-staging --days-back 35 (loose backstop; scout already
#     vetted freshness at download time — see Phase 2 comment for month-boundary rationale)
#   - triage deletes non-OPD PDFs directly (rm, no .trash accumulation)
#   - awesome inserter is idempotent (already_present = skip)
#   - git push only if there are actual changes
#   - all output logged to logs/cron-pipeline-YYYY-MM-DD.log

set -u

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
export HOME="${HOME:-/root}"

PROJECT_ROOT="/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey"
LOG_DIR="${PROJECT_ROOT}/logs"
SCRIPTS="${PROJECT_ROOT}/scripts"
AWESOME_DIR="${PROJECT_ROOT}/Awesome-LLM-On-Policy-Distillation"
NOTES_PATH="${PROJECT_ROOT}/notes/paper_notes.json"
KNOWN_IDS="${PROJECT_ROOT}/papers-meta/known_arxiv_ids.txt"

# Temp files for inter-phase data
DEEP_READ_SUMMARY="/tmp/opd_pipeline_deep_read_summary.json"
TRIAGE_KEEP_JSON="/tmp/opd_pipeline_triage_keep.json"

mkdir -p "${LOG_DIR}"
DATE_CST=$(TZ='Asia/Shanghai' date '+%Y-%m-%d')
TIME_CST=$(TZ='Asia/Shanghai' date '+%H:%M')
LOG="${LOG_DIR}/cron-pipeline-${DATE_CST}.log"

exec >> "${LOG}" 2>&1
echo ""
echo "================================================================"
echo "  OPD Pipeline Phase 2-7  |  ${DATE_CST} ${TIME_CST}"
echo "================================================================"
echo ""

cd "${PROJECT_ROOT}" || { echo "FATAL: cannot cd to ${PROJECT_ROOT}"; exit 2; }

# ──────────────────────────────────────────────
# Phase 2: Deep-read (LLM API)
# ──────────────────────────────────────────────
echo "▶ Phase 2: batch deep-read (--from-staging --days-back 35)"

STAGING_COUNT=$(ls "${PROJECT_ROOT}/pdfs/_staging/"*.pdf 2>/dev/null | wc -l)
echo "  _staging/ has ${STAGING_COUNT} PDFs total"

# days-back=35 (not 2): staging PDFs are already freshness-vetted by scout
# (RSS announce_type=new/cross, or S2 + API date-verify before download), so this
# window is a loose backstop, not the real freshness guarantee. A tight window
# (2) recreates the month-boundary bug: arXiv IDs carry the *submission* month,
# so a paper submitted late last month but announced on day 1-2 of this month
# still has last month's YYMM prefix and gets silently, permanently dropped
# (confirmed: 2026-08-04, 45 papers rejected, 0 processed). 35 days covers any
# realistic submission-to-announcement lag without reintroducing stale papers,
# since staging never accumulates old PDFs (Phase 3/4.5 always drains it).
python3 "${SCRIPTS}/batch_deep_read.py" \
    --from-staging \
    --days-back 35 \
    --workers 3 \
    --model claude \
    --summary-out "${DEEP_READ_SUMMARY}"
DEEP_RC=$?

echo "  deep-read exit code: ${DEEP_RC}"

if [ ! -f "${DEEP_READ_SUMMARY}" ]; then
    echo "  ⚠️  No summary file — deep-read produced nothing (0 new papers?)"
    echo "  Pipeline complete (nothing to do)."
    exit 0
fi

# Parse deep-read results
TOTAL=$(python3 -c "import json; d=json.load(open('${DEEP_READ_SUMMARY}')); print(d.get('total_papers', 0))" 2>/dev/null || echo 0)
OK=$(python3 -c "import json; d=json.load(open('${DEEP_READ_SUMMARY}')); print(d.get('ok', 0))" 2>/dev/null || echo 0)
OPD_YES=$(python3 -c "import json; d=json.load(open('${DEEP_READ_SUMMARY}')); print(d.get('is_opd_yes', 0))" 2>/dev/null || echo 0)
OPD_NO=$(python3 -c "import json; d=json.load(open('${DEEP_READ_SUMMARY}')); print(d.get('is_opd_no', 0))" 2>/dev/null || echo 0)

echo "  deep-read: total=${TOTAL} ok=${OK} opd_yes=${OPD_YES} opd_no=${OPD_NO}"

if [ "${TOTAL}" -eq 0 ]; then
    echo "  0 papers to process — pipeline complete."
    exit 0
fi

# Collect IDs that were successfully deep-read
DEEP_READ_IDS=$(python3 -c "
import json
d = json.load(open('${DEEP_READ_SUMMARY}'))
ids = [r['paper_id'] for r in d.get('results', []) if r.get('status') == 'ok']
print(','.join(ids))
" 2>/dev/null || echo "")

if [ -z "${DEEP_READ_IDS}" ]; then
    echo "  No successful deep-reads — pipeline complete."
    exit 0
fi

echo "  deep-read IDs: ${DEEP_READ_IDS}"
echo ""

# ──────────────────────────────────────────────
# Phase 3: Triage
# ──────────────────────────────────────────────
echo "▶ Phase 3: triage"

python3 "${SCRIPTS}/triage_after_deep_read.py" \
    --candidates "${DEEP_READ_IDS}"
TRIAGE_RC=$?
echo "  triage exit code: ${TRIAGE_RC}"
echo ""

# ──────────────────────────────────────────────
# Phase 3.5: 3-condition filter
# ──────────────────────────────────────────────
echo "▶ Phase 3.5: 3-condition filter"

# Get IDs that survived triage (is_opd=yes in paper_notes after triage)
KEPT_IDS=$(python3 -c "
import json
db = json.load(open('${NOTES_PATH}'))
notes = db.get('notes', {})
candidates = '${DEEP_READ_IDS}'.split(',')
kept = []
for aid in candidates:
    rec = notes.get(aid, {})
    cls = rec.get('opd_classification', {}) or {}
    if cls.get('is_opd', '').lower() in ('yes', 'analysis'):
        kept.append(aid)
print(','.join(kept))
" 2>/dev/null || echo "")

if [ -z "${KEPT_IDS}" ]; then
    echo "  No OPD papers after triage — skipping Phase 3.5-7."
    echo "  Pipeline complete."
    exit 0
fi

echo "  Papers for 3-cond filter: ${KEPT_IDS}"

python3 "${SCRIPTS}/three_condition_filter.py" \
    --aids "${KEPT_IDS}" \
    --format json > /tmp/opd_3cond_result.json
FILTER_RC=$?
echo "  3-cond filter exit code: ${FILTER_RC}"

# Parse filter results — only KEEP verdicts proceed
FINAL_KEEP_IDS=$(python3 -c "
import json
results = json.load(open('/tmp/opd_3cond_result.json'))
keep = [r['aid'] for r in results if r.get('verdict') == 'KEEP']
print(','.join(keep))
" 2>/dev/null || echo "")

# Log rejected papers
python3 -c "
import json
results = json.load(open('/tmp/opd_3cond_result.json'))
for r in results:
    if r.get('verdict') != 'KEEP':
        print(f\"  🚫 {r['aid']}: {r.get('verdict')} — {r.get('reason', '')[:100]}\")
" 2>/dev/null

if [ -z "${FINAL_KEEP_IDS}" ]; then
    echo "  No papers passed 3-condition filter — skipping Phase 3.7-7."
    echo "  Pipeline complete."
    exit 0
fi

echo "  Final KEEP (pre-2nd-opinion): ${FINAL_KEEP_IDS}"
echo ""

# ──────────────────────────────────────────────
# Phase 3.7: Second-opinion verification (cross-model)
# ──────────────────────────────────────────────
echo "▶ Phase 3.7: second-opinion verification (Gemini cross-check)"

python3 "${SCRIPTS}/opd_second_opinion.py" \
    --aids "${FINAL_KEEP_IDS}" \
    --model gemini \
    --format json > /tmp/opd_2nd_opinion_result.json
OPINION_RC=$?
echo "  2nd-opinion exit code: ${OPINION_RC}"

# Parse verdicts: CONFIRM and UNCERTAIN pass through; only explicit REJECT blocks.
# Rationale: deep-read + 3-cond filter already validated these papers. UNCERTAIN
# typically means API timeout or JSON parse error — not a genuine quality signal.
# In July 2026, 15/15 UNCERTAIN papers were confirmed real OPD, so blocking them
# was pure false-negative waste.
VERIFIED_IDS=$(python3 -c "
import json
results = json.load(open('/tmp/opd_2nd_opinion_result.json'))
passed = [r['aid'] for r in results if r.get('verdict') != 'REJECT']
print(','.join(passed))
" 2>/dev/null || echo "")

# Log rejected papers (only explicit REJECT is meaningful now)
python3 -c "
import json
results = json.load(open('/tmp/opd_2nd_opinion_result.json'))
for r in results:
    v = r.get('verdict', '?')
    if v == 'REJECT':
        print(f\"  🚫 {r['aid']}: REJECT — {r.get('reasoning', '')[:100]}\")
    elif v not in ('CONFIRM',):
        print(f\"  ⚠️  {r['aid']}: {v} (passed through) — {r.get('reasoning', '')[:100]}\")
" 2>/dev/null

# Fallback: if 2nd-opinion script fails entirely, pass through (don't block pipeline)
if [ "${OPINION_RC}" -ne 0 ] && [ -z "${VERIFIED_IDS}" ]; then
    echo "  ⚠️  2nd-opinion script failed — falling back to 3-cond filter results"
    VERIFIED_IDS="${FINAL_KEEP_IDS}"
fi

# Health monitor: track consecutive days with 0 CONFIRMs from 2nd-opinion.
# If the Gemini API key expired or config broke, every paper returns UNCERTAIN
# and 2nd-opinion becomes effectively disabled (still harmless but worth flagging).
HEALTH_FILE="${PROJECT_ROOT}/.claude/2nd_opinion_health.txt"
N_CONFIRM=$(python3 -c "
import json
results = json.load(open('/tmp/opd_2nd_opinion_result.json'))
print(sum(1 for r in results if r.get('verdict') == 'CONFIRM'))
" 2>/dev/null || echo 0)
if [ "${N_CONFIRM}" -eq 0 ]; then
    STREAK=$(cat "${HEALTH_FILE}" 2>/dev/null || echo 0)
    STREAK=$((STREAK + 1))
    echo "${STREAK}" > "${HEALTH_FILE}"
    if [ "${STREAK}" -ge 5 ]; then
        echo "  ⚠️  2nd-opinion: 0 CONFIRMs for ${STREAK} consecutive days — Gemini API may be broken"
        ALERT_FILE="${PROJECT_ROOT}/.claude/pipeline_alerts.md"
        {
            echo ""
            echo "## ⚠️ ${DATE_CST} — 2nd-opinion health warning"
            echo ""
            echo "0 CONFIRM verdicts for ${STREAK} consecutive pipeline days. Gemini API/config may need attention."
            echo ""
        } >> "${ALERT_FILE}"
    fi
else
    echo "0" > "${HEALTH_FILE}"
fi

FINAL_KEEP_IDS="${VERIFIED_IDS}"

if [ -z "${FINAL_KEEP_IDS}" ]; then
    echo "  No papers confirmed by 2nd-opinion — skipping Phase 4-7."
    echo "  Pipeline complete."
    exit 0
fi

echo "  Final KEEP (verified): ${FINAL_KEEP_IDS}"
echo ""

# ──────────────────────────────────────────────
# Phase 4: Awesome list inserter
# ──────────────────────────────────────────────
echo "▶ Phase 4: awesome list inserter"

# Build batch JSON for inserter from paper_notes v3 records
python3 -c "
import json
from pathlib import Path

db = json.load(open('${NOTES_PATH}'))
notes = db.get('notes', {})
keep_ids = '${FINAL_KEEP_IDS}'.split(',')
batch = []
for aid in keep_ids:
    rec = notes.get(aid, {})
    cls = rec.get('opd_classification', {}) or {}
    pairs = rec.get('teacher_student_pairs', [])
    # Build model_pair from first pair
    model_pair = ''
    if pairs and isinstance(pairs, list) and len(pairs) > 0:
        p = pairs[0]
        t = p.get('teacher', {}) if isinstance(p.get('teacher'), dict) else {}
        s = p.get('student', {}) if isinstance(p.get('student'), dict) else {}
        t_name = t.get('name', '?')
        s_name = s.get('name', '?')
        model_pair = f'{t_name} → {s_name}'
    # One-line from summary (first sentence)
    summary = rec.get('summary', '')
    one_line = summary.split('。')[0].split('. ')[0][:120] if summary else ''
    # Fix subsections not in inserter mapping
    section = cls.get('primary_section', '')
    _sec_fix = {'§5.1.1': '§5.1', '§5.1.2': '§5.1'}
    section = _sec_fix.get(section, section)
    # Handle openness being str or dict
    openness = rec.get('openness', {})
    code_url = openness.get('code_url') if isinstance(openness, dict) else None
    batch.append({
        'aid': aid,
        'section': section,
        'title': rec.get('title', ''),
        'model_pair': model_pair,
        'one_line': one_line,
        'year': rec.get('year', 2026),
        'code_url': code_url,
    })
Path('${TRIAGE_KEEP_JSON}').write_text(json.dumps(batch, ensure_ascii=False, indent=2))
print(f'Prepared {len(batch)} papers for insertion:')
for b in batch:
    print(f\"  {b['aid']} → {b['section']} | {b['title'][:60]}\")
" 2>/dev/null

python3 "${SCRIPTS}/awesome_list_inserter.py" \
    --batch-from-triage "${TRIAGE_KEEP_JSON}" \
    --commit
INSERT_RC=$?
echo "  inserter exit code: ${INSERT_RC}"
echo ""

# ──────────────────────────────────────────────
# Phase 4.5: Move kept PDFs from staging to month bucket
# ──────────────────────────────────────────────
echo "▶ Phase 4.5: staging cleanup (mv kept PDFs to month bucket)"

python3 -c "
import json, re
from pathlib import Path

staging = Path('${PROJECT_ROOT}/pdfs/_staging')
db = json.load(open('${NOTES_PATH}'))
notes = db.get('notes', {})
moved = 0
deleted = 0
for pdf in sorted(staging.glob('*.pdf')):
    aid = pdf.stem
    if not re.match(r'\d{4}\.\d{4,5}', aid):
        continue
    rec = notes.get(aid, {})
    is_opd = (rec.get('opd_classification', {}) or {}).get('is_opd', '').lower()
    if is_opd in ('yes', 'analysis'):
        # Determine month bucket from arxiv ID (YYMM.NNNNN)
        yymm = aid[:4]
        month_dir = Path('${PROJECT_ROOT}/pdfs') / f'20{yymm[:2]}-{yymm[2:]}'
        month_dir.mkdir(parents=True, exist_ok=True)
        dst = month_dir / pdf.name
        if not dst.exists():
            pdf.rename(dst)
            moved += 1
    elif is_opd == 'no':
        # Non-OPD: delete directly (pipeline-scouted only)
        pdf.unlink()
        deleted += 1
print(f'  Moved {moved} kept PDFs from staging to month buckets')
print(f'  Deleted {deleted} non-OPD PDFs from staging')
remaining = len(list(staging.glob('*.pdf')))
print(f'  Remaining in staging: {remaining}')
" 2>/dev/null
echo ""

# ──────────────────────────────────────────────
# Phase 5: Refresh known_arxiv_ids.txt
# ──────────────────────────────────────────────
echo "▶ Phase 5: refresh known_arxiv_ids.txt"

python3 "${SCRIPTS}/scout_precheck.py" --refresh-ids 2>/dev/null
# Also ensure all processed IDs are in known_ids
python3 -c "
from pathlib import Path
known_path = Path('${KNOWN_IDS}')
existing = set(known_path.read_text().split()) if known_path.exists() else set()
new_ids = '${DEEP_READ_IDS}'.split(',')
added = 0
with known_path.open('a') as f:
    for aid in new_ids:
        if aid and aid not in existing:
            f.write(aid + '\n')
            existing.add(aid)
            added += 1
print(f'  known_arxiv_ids: {added} new IDs added, total {len(existing)}')
" 2>/dev/null
echo ""

# ──────────────────────────────────────────────
# Phase 6: (placeholder) heatmap / stats
# ──────────────────────────────────────────────
echo "▶ Phase 6: (skipped — heatmap/stats manual for now)"
echo ""

# ──────────────────────────────────────────────
# Phase 7: Git commit + push
# ──────────────────────────────────────────────
echo "▶ Phase 7: git commit + push"

# Guard against stale .git/index.lock (a crashed/concurrent git op once left one
# on 2026-07-09, silently blocking 18 days of commits). Remove only if stale
# (>2 min old) so we never clobber a lock from a genuinely in-flight git op.
clear_stale_git_lock() {
    local lock="$1/.git/index.lock"
    if [ -f "${lock}" ]; then
        if [ -z "$(find "${lock}" -mmin -2 2>/dev/null)" ]; then
            rm -f "${lock}" && echo "  cleared stale git lock: ${lock}"
        else
            echo "  ⚠️ recent git lock (<2min) present — leaving it: ${lock}"
        fi
    fi
}

# Survey repo
cd "${PROJECT_ROOT}" || true
clear_stale_git_lock "${PROJECT_ROOT}"
if git diff --quiet && git diff --cached --quiet; then
    echo "  survey repo: no changes"
else
    git add -A
    git commit -m "cron: pipeline Phase 2-7 — ${DATE_CST} (${OK} deep-read, keep ${FINAL_KEEP_IDS})"
    rc=$?
    if [ ${rc} -eq 0 ]; then
        echo "  survey repo: committed"
    else
        echo "  ❌ survey repo: commit FAILED (rc=${rc}) — changes left uncommitted"
    fi
fi

# Awesome repo
cd "${AWESOME_DIR}" || true
clear_stale_git_lock "${AWESOME_DIR}"
if git diff --quiet && git diff --cached --quiet; then
    echo "  awesome repo: no changes"
else
    # Phase 4 inserter already commits, but catch any leftovers
    git add -A
    BADGE=$(python3 -c "
import re
text = open('README.md').read()
m = re.search(r'Papers-(\d+)-blue', text)
print(m.group(1) if m else '?')
" 2>/dev/null || echo "?")
    git commit -m "cron: pipeline ${DATE_CST} — badge=${BADGE}"
    rc=$?
    if [ ${rc} -eq 0 ]; then
        echo "  awesome repo: committed (badge=${BADGE})"
    else
        echo "  ❌ awesome repo: commit FAILED (rc=${rc}) — changes left uncommitted"
    fi
fi

# Push both repos
cd "${PROJECT_ROOT}" || true
git push 2>/dev/null && echo "  survey repo: pushed" || echo "  survey repo: push failed (will retry next run)"

cd "${AWESOME_DIR}" || true
git push 2>/dev/null && echo "  awesome repo: pushed" || echo "  awesome repo: push failed (will retry next run)"

echo ""
echo "================================================================"
echo "  Pipeline complete  |  $(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M')"
echo "================================================================"

exit 0
