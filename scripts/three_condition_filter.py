#!/usr/bin/env python3
"""three_condition_filter.py — OPD backlog 3-condition 强制过滤器

把 daily-pipeline / V3 deep-read 标 is_opd=yes 的 candidate 列表过一遍，
按 academic-rigor skill §OPD 判定标准 reject self-play / off-policy SFT /
RL-only(伪 OPD) / analysis-only 论文。

设计原则 (SOUL "重要纪律必须代码层强制"):
- prompt 写规则不够, 必须代码层强制
- 5/23 实战 14 篇 backlog 验证 14/14 一致 (mismatch=0)

用法:
    # 过滤一组 candidate
    python3 three_condition_filter.py --aids 2605.11019,2605.22675,...

    # 单条判定
    python3 three_condition_filter.py --aid 2605.22675

    # 用 --notes-path 指定 paper_notes.json
    python3 three_condition_filter.py --notes-path /path/to/paper_notes.json --aids ...

    # 库函数
    from three_condition_filter import judge_paper
    verdict, reason = judge_paper(notes_db, aid)

输出 (JSON):
    [
      {"aid": "...", "verdict": "KEEP" | "REJECT" | "UNKNOWN", "rule": "R1"|"R2"|"R3"|"OK", "reason": "..."},
      ...
    ]

退出码:
    0 = 全 KEEP 或 至少 1 个 REJECT (正常工作)
    1 = 命令行/输入错误
    2 = 至少 1 个 UNKNOWN (paper_notes 缺失字段，需人工)
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_NOTES_PATH = "/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/notes/paper_notes.json"

OFF_POLICY_FREQS = ("once-before-training", "batch-precomputed", "offline", "static")
ON_POLICY_FREQS = ("per-step", "per-outer-iter", "per-update")

TEACHER_DISTILL_PAT = re.compile(
    r"""
    (KL|JSD|CE|cross.?entropy|divergence|MSE).{0,40}(teacher|π_T|π\^?\{?tch|P\^?\{?tch|oracle) |
    (teacher|π_T|π\^?\{?tch|P\^?\{?tch|oracle).{0,40}(KL|JSD|CE|cross.?entropy|divergence|MSE) |
    L_(distill|OPSD|SSOPD|KD|tch|teacher) |
    distill\w*\s*loss |
    sequence.level.distill |
    token.level.distill |
    forward.KL |
    reverse.KL
    """,
    re.I | re.X,
)

RL_KEYWORD_PAT = re.compile(
    r"\bGRPO\b|\bPPO\b|\bDPO\b|verifier.{0,20}reward|RLHF|RLVR",
    re.I,
)

# GRPO clipping 数学形式 — PSDISTILL 这种公式没写 "GRPO" 字面，但有 min(ρ·a, clip(ρ)·a)
GRPO_MATH_PAT = re.compile(r"min\s*\(\s*ρ.{0,20}clip\s*\(\s*ρ")


def judge_paper(notes_db: dict, aid: str) -> tuple[str, str, str]:
    """对单篇论文跑 3-condition 判定.

    Returns:
        (verdict, rule, reason) 三元组.
        verdict ∈ {"KEEP", "REJECT", "UNKNOWN"}
        rule ∈ {"R1", "R2", "R3", "OK", "MISSING"}
    """
    inner = notes_db.get("notes", notes_db)  # 兼容 {"notes": {...}} 和直接 {...}
    n = inner.get(aid)
    if n is None:
        return ("UNKNOWN", "MISSING", f"{aid} 不在 paper_notes 中, 需先跑 deep-read")

    opm = n.get("on_policy_mechanism", {}) or {}
    cls = n.get("opd_classification", {}) or {}
    method = n.get("method", {}) or {}

    freq = opm.get("rollout_frequency")
    is_opd = cls.get("is_opd")
    sig = opm.get("signal_source", "")

    # Rule 1: off-policy SFT / self-play
    if freq in OFF_POLICY_FREQS:
        return (
            "REJECT",
            "R1",
            f"rollout_frequency={freq} → off-policy SFT 或 self-play (不在 training loop 内 rollout)",
        )

    # Rule 2: V3 自标 no / analysis
    if is_opd in ("no", "analysis"):
        return (
            "REJECT",
            "R2",
            f"V3 精读自标 is_opd={is_opd} → " +
            ("V3 不认为是 OPD" if is_opd == "no" else "analysis-only 论文, 综述 Theory 章可 cite 但不进 backlog"),
        )

    # Rule 3: RL-only loss + no teacher distill + self/verifier signal = 伪 OPD
    loss_formula = method.get("loss_formulation", "") or ""
    training_loop = method.get("training_loop", "") or ""
    components = " ".join(method.get("key_components", []) or [])
    full_text = f"{loss_formula} | {training_loop} | {components}"

    has_teacher_distill = bool(TEACHER_DISTILL_PAT.search(full_text))
    has_rl = bool(RL_KEYWORD_PAT.search(full_text))
    has_grpo_math = bool(GRPO_MATH_PAT.search(full_text))

    if (has_rl or has_grpo_math) and not has_teacher_distill and sig in ("self", "verifier"):
        return (
            "REJECT",
            "R3",
            f"RL-only 公式 (rl_keyword={has_rl}, grpo_math={has_grpo_math}) + 无 teacher-distill term + signal_source={sig} "
            f"→ 伪 OPD (典型例 PSDISTILL: D_KL(π_θ ∥ π_ref) 是 ref-policy 正则化, 不是 teacher distill)",
        )

    # 三条都过 → 合法 OPD
    if freq in ON_POLICY_FREQS:
        teacher_marker = " +teacher-distill" if has_teacher_distill else ""
        return (
            "KEEP",
            "OK",
            f"rollout_frequency={freq}, signal_source={sig}{teacher_marker}",
        )

    return ("UNKNOWN", "MISSING", f"is_opd={is_opd}, rollout_frequency={freq} — 未识别频率, 需人工检查")


def load_notes(notes_path: str | Path) -> dict:
    p = Path(notes_path)
    if not p.exists():
        raise FileNotFoundError(f"paper_notes.json not found: {p}")
    with open(p) as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser(description="OPD backlog 3-condition 过滤器")
    ap.add_argument("--notes-path", default=DEFAULT_NOTES_PATH, help="paper_notes.json 路径")
    ap.add_argument("--aid", help="单条 arxiv id (e.g. 2605.22675)")
    ap.add_argument("--aids", help="多条 arxiv id, 逗号分隔")
    ap.add_argument("--from-stdin", action="store_true", help="从 stdin 读 arxiv id, 每行一个")
    ap.add_argument("--format", choices=["json", "table"], default="json", help="输出格式")
    ap.add_argument("--self-test", action="store_true", help="跑 5/23 14 篇 backlog 自检")
    args = ap.parse_args()

    # 自检模式
    if args.self_test:
        return run_self_test(args.notes_path)

    # 收集 aids
    aids = []
    if args.aid:
        aids.append(args.aid.strip())
    if args.aids:
        aids.extend(x.strip() for x in args.aids.split(",") if x.strip())
    if args.from_stdin:
        aids.extend(line.strip() for line in sys.stdin if line.strip())

    if not aids:
        ap.error("提供 --aid / --aids / --from-stdin / --self-test 之一")

    notes = load_notes(args.notes_path)
    results = []
    has_unknown = False
    for aid in aids:
        verdict, rule, reason = judge_paper(notes, aid)
        if verdict == "UNKNOWN":
            has_unknown = True
        results.append({"aid": aid, "verdict": verdict, "rule": rule, "reason": reason})

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"{'aid':<14} {'verdict':<8} {'rule':<6} reason")
        print("=" * 100)
        for r in results:
            print(f"{r['aid']:<14} {r['verdict']:<8} {r['rule']:<6} {r['reason']}")
        print()
        n_keep = sum(1 for r in results if r["verdict"] == "KEEP")
        n_reject = sum(1 for r in results if r["verdict"] == "REJECT")
        n_unknown = sum(1 for r in results if r["verdict"] == "UNKNOWN")
        print(f"总计: {len(results)} | KEEP {n_keep} | REJECT {n_reject} | UNKNOWN {n_unknown}")

    return 2 if has_unknown else 0


# 5/23 黄金 oracle: 14 篇 backlog + 老大/人工判定
SELF_TEST_GOLDEN = [
    ("2605.22675", "SPD",           "REJECT"),
    ("2605.11019", "VPG-EA",        "KEEP"),
    ("2605.15239", "OPSA",          "KEEP"),
    ("2605.15532", "DeltaPrompts",  "KEEP"),
    ("2605.16826", "Decoupling KL", "REJECT"),
    ("2605.17497", "SSOPD",         "KEEP"),
    ("2605.18299", "SD-Search",     "KEEP"),
    ("2605.17873", "HINT-SD",       "KEEP"),
    ("2605.16865", "MixSD",         "REJECT"),
    ("2605.16941", "WINO+",         "REJECT"),
    ("2605.18740", "Vision-OPD",    "KEEP"),
    ("2605.17862", "f-OPD",         "KEEP"),
    ("2605.19433", "MOTAB",         "KEEP"),
    ("2605.19776", "PSDISTILL",     "REJECT"),
]


def run_self_test(notes_path: str) -> int:
    """对 5/23 14 篇黄金 oracle 跑自检, 任何 mismatch 退出码 1."""
    print(f"Self-test: 5/23 14 篇黄金 oracle, notes_path={notes_path}")
    notes = load_notes(notes_path)
    mismatches = []
    print()
    print(f"{'#':<3} {'aid':<14} {'name':<14} {'expect':<8} {'auto':<8} {'rule':<6} match")
    print("=" * 100)
    for i, (aid, name, expect) in enumerate(SELF_TEST_GOLDEN, 1):
        verdict, rule, reason = judge_paper(notes, aid)
        ok = "✓" if verdict == expect else "✗"
        if verdict != expect:
            mismatches.append((aid, name, expect, verdict, rule, reason))
        print(f"{i:<3} {aid:<14} {name:<14} {expect:<8} {verdict:<8} {rule:<6} {ok}")

    print()
    if mismatches:
        print(f"❌ FAIL: {len(mismatches)}/14 mismatch")
        for aid, name, exp, got, rule, reason in mismatches:
            print(f"  {aid} {name}: expect={exp} got={got} ({rule}) — {reason}")
        return 1
    print(f"✅ PASS: 14/14 一致 (mismatch=0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
