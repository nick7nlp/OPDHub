#!/usr/bin/env bash
# OPD daily pipeline Phase 2-7 — automated follow-up after Phase 1 scout.
#
# Cron schedule (intended): every weekday at 10:30 CST (1h after scout)
#   30 10 * * 1-5 /apdcephfs_cq8/.../scripts/cron_pipeline_phase2_7.sh
#
# What it does:
#   Phase 2: batch deep-read (LLM API) on all un-read PDFs in _staging/ (days_back=3)
#   Phase 3: triage — keep OPD=yes, exclude OPD=no (mv to trash, log to excluded-papers.md)
#   Phase 3.5: 3-condition filter — reject false-positives (self-play, off-policy, analysis-only)
#   Phase 4: awesome list inserter — add confirmed OPD papers to README
#   Phase 5: refresh known_arxiv_ids.txt
#   Phase 6: (placeholder) loss-evolution / heatmap refresh
#   Phase 7: git commit + push
#
# Safety:
#   - deep-read uses --from-staging --days-back 3 (covers gaps, dedup built-in)
#   - triage uses safe mv-to-trash (never rm)
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
echo "▶ Phase 2: batch deep-read (--from-staging --days-back 3)"

STAGING_COUNT=$(ls "${PROJECT_ROOT}/pdfs/_staging/"*.pdf 2>/dev/null | wc -l)
echo "  _staging/ has ${STAGING_COUNT} PDFs total"

python3 /root/clawd/scripts/batch_deep_read.py \
    --from-staging \
    --days-back 3 \
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
    echo "  No papers passed 3-condition filter — skipping Phase 4-7."
    echo "  Pipeline complete."
    exit 0
fi

echo "  Final KEEP: ${FINAL_KEEP_IDS}"
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
        t = p.get('teacher', {})
        s = p.get('student', {})
        t_name = t.get('name', '?')
        s_name = s.get('name', '?')
        model_pair = f'{t_name} → {s_name}'
    # One-line from summary (first sentence)
    summary = rec.get('summary', '')
    one_line = summary.split('。')[0].split('. ')[0][:120] if summary else ''
    batch.append({
        'aid': aid,
        'section': cls.get('primary_section', ''),
        'title': rec.get('title', ''),
        'model_pair': model_pair,
        'one_line': one_line,
        'year': rec.get('year', 2026),
        'code_url': (rec.get('openness', {}) or {}).get('code_url'),
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

# Survey repo
cd "${PROJECT_ROOT}" || true
if git diff --quiet && git diff --cached --quiet; then
    echo "  survey repo: no changes"
else
    git add -A
    git commit -m "cron: pipeline Phase 2-7 — ${DATE_CST} (${OK} deep-read, keep ${FINAL_KEEP_IDS})"
    echo "  survey repo: committed"
fi

# Awesome repo
cd "${AWESOME_DIR}" || true
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
    echo "  awesome repo: committed (badge=${BADGE})"
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
