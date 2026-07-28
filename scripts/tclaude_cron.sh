#!/usr/bin/env bash
# OPD daily automation — tclaude-driven, OS-cron-triggered (permanent, unattended).
#
# Design (robust + permanent):
#   OS cron  ->  this wrapper  ->  (1) run the existing phase script directly
#                                  (2) tclaude -p reads the day's log & emits a status line
#
# Why the phase script runs directly (NOT inside `tclaude -p`):
#   Claude Code's Bash tool caps a single command at 10 min; the deep-read
#   pipeline runs far longer, so a synchronous `tclaude -p "run the script"`
#   would be killed mid-run. Running the script directly avoids that ceiling.
#   tclaude is used for the reporting/summary layer, where it adds value and
#   finishes in seconds.
#
# Permanence: this is an OS cron entry, so it never expires and survives reboots
# (unlike tclaude's in-app scheduler, which auto-expires after 7 days and needs a
# live session). Migrated from the old direct-script cron on 2026-07-27.
#
# Usage:  tclaude_cron.sh scout|pipeline
# Cron:   27 9  * * 1-5  .../scripts/tclaude_cron.sh scout
#         27 10 * * 1-5  .../scripts/tclaude_cron.sh pipeline

set -u

# cron strips the environment: make node/tclaude + git + python resolve.
export HOME="${HOME:-/root}"
export PATH="/root/.nvm/versions/node/v24.11.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
# tclaude keeps its auth/config here (not the default ~/.claude).
export CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-/root/.tclaude}"

PROJECT_ROOT="/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey"
SCRIPTS="${PROJECT_ROOT}/scripts"
LOG_DIR="${PROJECT_ROOT}/logs"
TCLAUDE_MODEL="claude-haiku-4-5"   # cheap model — only reads a log and summarizes

mkdir -p "${LOG_DIR}"
cd "${PROJECT_ROOT}" || { echo "FATAL: cannot cd to ${PROJECT_ROOT}" >&2; exit 2; }

DATE_CST=$(TZ='Asia/Shanghai' date '+%Y-%m-%d')
PHASE="${1:-}"

case "${PHASE}" in
  scout)
    TARGET="${SCRIPTS}/cron_scout.sh"
    PHASE_LOG="${LOG_DIR}/cron-scout-${DATE_CST}.log"
    SUMMARY_HINT="读取 ${PHASE_LOG} 末尾与 papers-meta/_pipeline_queue.md 最新追加区块，用一行中文说明：下载了多少候选论文（或 weekend skip / scout 失败）。"
    ;;
  pipeline)
    TARGET="${SCRIPTS}/cron_pipeline_phase2_7.sh"
    PHASE_LOG="${LOG_DIR}/cron-pipeline-${DATE_CST}.log"
    SUMMARY_HINT="读取 ${PHASE_LOG} 末尾，用一行中文说明：deep-read 了多少篇、最终 keep 哪些、git push 是否成功（或 nothing to do / 失败原因）。"
    ;;
  *)
    echo "usage: $0 scout|pipeline" >&2; exit 2 ;;
esac

WRAP_LOG="${LOG_DIR}/cron-tclaude-${PHASE}-${DATE_CST}.log"
{
  echo ""
  echo "======== tclaude-cron ${PHASE} | ${DATE_CST} $(TZ='Asia/Shanghai' date '+%H:%M') ========"
} >> "${WRAP_LOG}"

# (1) Heavy lifting: run the existing, proven phase script directly.
bash "${TARGET}" >> "${WRAP_LOG}" 2>&1
TARGET_RC=$?
echo "[wrapper] ${PHASE} script exit ${TARGET_RC}" >> "${WRAP_LOG}"

# (2) tclaude reviews the log and writes a concise status line (best-effort;
#     failure here never masks the work already done in step 1).
#     Read-only: `default` mode + a read-only allowlist avoids the root/sudo
#     block that `--dangerously-skip-permissions` hits under cron.
timeout 600 tclaude -p "OPD 每日 ${PHASE} 刚由 cron 跑完（脚本退出码 ${TARGET_RC}）。${SUMMARY_HINT} 只做只读检查，不要修改任何文件。" \
    --permission-mode default \
    --allowed-tools "Bash Read" \
    --model "${TCLAUDE_MODEL}" \
    --output-format text >> "${WRAP_LOG}" 2>&1
echo "[wrapper] tclaude summary exit $? @ $(TZ='Asia/Shanghai' date '+%H:%M:%S')" >> "${WRAP_LOG}"
exit 0
