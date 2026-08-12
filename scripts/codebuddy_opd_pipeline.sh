#!/usr/bin/env bash
# CodeBuddy-triggered OPD automation.
#
# `dispatch` starts an independent systemd user service so the long-running
# deep-read pipeline is not limited by the CodeBuddy agent Bash wait time.
# `run` executes the existing scout and Phase 2-7 scripts in sequence.

set -u

export HOME="${HOME:-/root}"
export PATH="/root/.nvm/versions/node/v24.11.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
export TZ="Asia/Shanghai"

PROJECT_ROOT="/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey"
SCRIPTS="${PROJECT_ROOT}/scripts"
LOG_DIR="${PROJECT_ROOT}/logs"
ALERT_FILE="${PROJECT_ROOT}/.claude/pipeline_alerts.md"
STATE_DIR="/root/.local/state/codebuddy-scheduler"
LOCK_FILE="${STATE_DIR}/opd-pipeline.lock"
MODE="${1:-run}"
DATE_CST=$(date '+%Y-%m-%d')
RUN_LOG="${LOG_DIR}/codebuddy-opd-${DATE_CST}.log"

mkdir -p "${LOG_DIR}" "${STATE_DIR}"

write_state() {
    local result="$1" exit_code="$2"
    local temporary="${STATE_DIR}/opd-pipeline.json.tmp"
    cat > "${temporary}" <<EOF
{"job":"opd-pipeline","finished_at":"$(date --iso-8601=seconds)","result":"${result}","exit_code":${exit_code},"log":"${RUN_LOG}"}
EOF
    chmod 600 "${temporary}"
    mv "${temporary}" "${STATE_DIR}/opd-pipeline.json"
}

write_alert() {
    local reason="$1"
    {
        echo ""
        echo "## ⚠️ ${DATE_CST} CodeBuddy OPD pipeline — ${reason}"
        echo ""
        echo "Log: \`${RUN_LOG}\`"
        echo ""
        tail -15 "${RUN_LOG}" | sed 's/^/    /'
        echo ""
    } >> "${ALERT_FILE}"
}

run_phase() {
    local phase="$1"
    local target="$2"
    local phase_log="$3"
    local rc=0

    echo "[runner] starting ${phase}: ${target} @ $(date '+%H:%M:%S')"
    bash "${target}"
    rc=$?
    echo "[runner] ${phase} script exit ${rc} @ $(date '+%H:%M:%S')"

    # Trust the script's exit code for success/failure. Only treat terminal
    # pipeline-level markers as failures; per-paper worker errors (e.g.
    # "[batch] ❌ <aid>: worker exit N") are expected attrition, not a run failure.
    if [ "${rc}" -ne 0 ] || grep -qE "FATAL|commit FAILED|push failed|❌ (survey|awesome) repo" "${phase_log}" 2>/dev/null; then
        echo "[runner] ${phase} failure detected (exit ${rc})"
        return 1
    fi
    return 0
}

run_pipeline() {
    local scout_ok=0
    local pipeline_ok=0
    local scout_log="${LOG_DIR}/cron-scout-${DATE_CST}.log"
    local pipeline_log="${LOG_DIR}/cron-pipeline-${DATE_CST}.log"

    exec 9>"${LOCK_FILE}"
    if ! flock -n 9; then
        echo "[runner] another OPD pipeline service is already running; skipping duplicate trigger"
        return 75
    fi

    cd "${PROJECT_ROOT}" || { echo "FATAL: cannot cd to ${PROJECT_ROOT}"; return 2; }
    if [ -n "$(git status --porcelain -- . ':!logs' ':!awesome-llm-opd-site')" ] || [ -n "$(git -C "${PROJECT_ROOT}/Awesome-LLM-On-Policy-Distillation" status --porcelain)" ]; then
        echo "FATAL: repository has uncommitted source changes; refusing automated pipeline commit"
        return 2
    fi
    echo ""
    echo "======== CodeBuddy OPD pipeline | ${DATE_CST} $(date '+%H:%M') ========"

    run_phase "scout" "${SCRIPTS}/cron_scout.sh" "${scout_log}" || scout_ok=1
    run_phase "pipeline" "${SCRIPTS}/cron_pipeline_phase2_7.sh" "${pipeline_log}" || pipeline_ok=1

    if [ "${scout_ok}" -ne 0 ] || [ "${pipeline_ok}" -ne 0 ]; then
        echo "[runner] finished with failures: scout=${scout_ok} pipeline=${pipeline_ok}"
        return 1
    fi

    echo "[runner] completed successfully @ $(date '+%H:%M:%S')"
    return 0
}

case "${MODE}" in
    run)
        run_pipeline >> "${RUN_LOG}" 2>&1
        rc=$?
        if [ "${rc}" -eq 75 ]; then
            write_state "skipped_locked" 75
            exit 0
        fi
        if [ "${rc}" -ne 0 ]; then
            write_state "failed" "${rc}"
            write_alert "FAILURE (exit ${rc})"
            exit "${rc}"
        fi
        write_state "success" 0
        ;;
    *)
        echo "usage: $0 run" >&2
        exit 2
        ;;
esac
