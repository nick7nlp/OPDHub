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

    if (has_rl or has_grpo_math) and not has_teacher_distill and sig in ("self", "verifier", "no-supervision"):
        # Exception: if V3 says teacher_signal=logits, the LLM believes there IS teacher logit
        # supervision. In self-distillation scenarios (EMA teacher, privileged context teacher),
        # teacher_signal=logits + signal_source=self is valid OPD (OPSD/self-distill).
        teacher_sig_r3 = opm.get("teacher_signal", "")
        if teacher_sig_r3 not in ("logits",):
            return (
                "REJECT",
                "R3",
                f"RL-only 公式 (rl_keyword={has_rl}, grpo_math={has_grpo_math}) + 无 teacher-distill term + signal_source={sig} "
                f"→ 伪 OPD (典型例 PSDISTILL: D_KL(π_θ ∥ π_ref) 是 ref-policy 正则化, 不是 teacher distill)",
            )

    # Rule 4: KL anchor without real teacher — RL + D_KL(π_θ ∥ π_ref) where π_ref is self/SFT checkpoint
    # Catches: PathRouter, SGPO, PolicyAlign — use KL divergence but π_ref is NOT a more capable teacher
    if (has_rl or has_grpo_math) and sig in ("PI(reference)", "self", "PI(GT)"):
        # Check if teacher_signal indicates no real teacher logit supervision
        teacher_sig = opm.get("teacher_signal", "")
        if teacher_sig in ("none", "self", "reward", "preference"):
            return (
                "REJECT",
                "R4",
                f"RL + KL anchor: signal_source={sig}, teacher_signal={teacher_sig} → "
                f"KL(π_θ∥π_ref) 是 policy regularization, 不是 teacher distillation",
            )

    # Rule 5: Non-LLM modality — robotics, GNN, image gen, speech
    # NOTE: domain field is LLM-generated and unreliable (e.g. robotics papers marked as "agent")
    # So we ALSO scan title/summary directly, regardless of domain value
    datasets = n.get("datasets", {}) or {}
    domain = datasets.get("domain", "") if isinstance(datasets, dict) else ""
    title = n.get("title", "")
    summary_text = n.get("summary", "")
    # Also scan teacher/student model names + the on_policy_mechanism evidence quote —
    # this is where concrete backbone identifiers (e.g. "SD3.5-Medium") and telltale
    # technical details (e.g. "classifier-free guidance", "denoising transitions") live
    # when title/summary stay generic (see 2607.24522 FlowCTS false-KEEP case).
    pairs_text = ""
    for p in (n.get("teacher_student_pairs", []) or []):
        if isinstance(p, dict):
            t = p.get("teacher", {}) if isinstance(p.get("teacher"), dict) else {}
            s = p.get("student", {}) if isinstance(p.get("student"), dict) else {}
            pairs_text += f" {t.get('name','')} {s.get('name','')}"
    evidence_quote = opm.get("evidence_quote", "") or ""
    scope_text = f"{title} | {summary_text} | {domain} | {full_text} | {pairs_text} | {evidence_quote}"

    non_llm_pats = (
        r"\b(robot\w*|VLA|manipulation|motor|locomot|embodied.agent|grasping|sim.to.real)\b",
        r"\b(GNN|graph.neural|molecular|protein)\b",
        r"\b(image.gen|video.gen|T2I|text.to.image)\b",
        r"\b(speech.synth|TTS|voice.clone)\b",
    )
    # Hard non-text generative backbones — image/video diffusion models with ZERO language
    # modeling component. Unlike non_llm_pats above, these NEVER get the OPD-in-title/summary
    # exemption: "Awesome LLM On-Policy Distillation" is scoped to language models, and a paper
    # can't out-argue that scope just by using OPD terminology on a non-text backbone (SD3.5,
    # SDXL, FLUX are definitionally not LLMs). Added after 2607.24522 (FlowCTS) slipped through
    # Exemption 1 because its summary literally said "on-policy distillation for flow models".
    hard_non_text_pats = (
        r"\b(stable.diffusion|SD3\.?5?\b|SDXL|FLUX\.1|rectified.flow|flow.matching|classifier.free.guidance)\b",
    )
    # OPD-in-title exemption: if the paper explicitly targets OPD as its contribution
    # (e.g. "VLA-OPD", "ProteinOPD", "On-Policy Self-Distillation"), it's applying OPD to a new domain → keep
    opd_in_title = bool(re.search(r"\bOPD\b|on.policy.*distill", title, re.I))
    opd_in_summary = bool(re.search(r"\bOPD\b|on.policy.*distill", summary_text, re.I))

    for pat in hard_non_text_pats:
        if re.search(pat, scope_text, re.I):
            return (
                "REJECT",
                "R5",
                f"非文本生成骨干 (无语言模型成分): 匹配 '{pat}' → OUT OF SCOPE (LLM-only survey, OPD 措辞不豁免)",
            )

    for pat in non_llm_pats:
        if re.search(pat, scope_text, re.I):
            # Exemption 1: paper explicitly about OPD applied to this domain
            if opd_in_title or opd_in_summary:
                break
            # Exemption 2: domain is explicitly text/language AND non-LLM keyword NOT in title
            if domain and domain.lower() in ("math", "code", "general", "instruction", "multi-modal"):
                if not re.search(pat, title, re.I):
                    break
            return (
                "REJECT",
                "R5",
                f"非 LLM 模态: 匹配 '{pat}' in title/summary/domain → OUT OF SCOPE",
            )

    # Rule 6: System/engineering paper with no novel OPD method
    # Heuristic: if teacher_signal is "none" or teacher_student_pairs is empty/missing, suspicious
    pairs = n.get("teacher_student_pairs", []) or []
    teacher_sig = opm.get("teacher_signal", "")
    student_rollout = opm.get("student_rollout_in_training", "")

    # If the paper claims OPD but has no teacher signal and no clear student rollout mechanism
    if teacher_sig in ("none",) and student_rollout in ("no", "unclear") and not has_teacher_distill:
        return (
            "REJECT",
            "R6",
            f"无 teacher signal ({teacher_sig}) + 无 student rollout ({student_rollout}) + 无 distill loss → "
            f"系统/应用论文, 非 OPD 方法贡献",
        )

    # 所有规则都过 → 合法 OPD
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
# 6/26 扩充: +12 篇本轮复核删除的非 OPD 论文
SELF_TEST_GOLDEN = [
    # 5/23 原始 14 篇
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
    # 6/26 新增 12 篇 (全部应 REJECT — 非 OPD)
    # RL + KL anchor (no real teacher)
    ("2606.16409", "PathRouter",    "REJECT"),
    ("2606.24064", "SGPO",          "REJECT"),
    ("2606.25442", "PolicyAlign",   "REJECT"),
    # Non-LLM domain
    ("2606.11583", "GNN-co-teach",  "REJECT"),
    ("2606.24089", "DynaWM",        "REJECT"),
    ("2606.14010", "RT-VLA",        "REJECT"),
    ("2606.25800", "ROAD-VLA",      "REJECT"),
    # Off-policy
    ("2606.12400", "Doc-to-Atom",   "REJECT"),
    ("2606.25964", "WinDOM",        "REJECT"),
    # System/application paper
    ("2606.15007", "Nemotron3Ultra", "REJECT"),
    ("2606.18101", "TrustTeacher",  "REJECT"),
    # Expert trace SFT
    ("2606.16215", "PACT",          "REJECT"),
]


def run_self_test(notes_path: str) -> int:
    """对 5/23 14 篇 + 6/26 12 篇黄金 oracle 跑自检, 任何 mismatch 退出码 1."""
    n_total = len(SELF_TEST_GOLDEN)
    print(f"Self-test: {n_total} 篇黄金 oracle (14 from 5/23 + 12 from 6/26), notes_path={notes_path}")
    notes = load_notes(notes_path)
    mismatches = []
    skipped = []
    print()
    print(f"{'#':<3} {'aid':<14} {'name':<16} {'expect':<8} {'auto':<10} {'rule':<6} match")
    print("=" * 100)
    for i, (aid, name, expect) in enumerate(SELF_TEST_GOLDEN, 1):
        verdict, rule, reason = judge_paper(notes, aid)
        # UNKNOWN (not in paper_notes) = skip, not a failure
        # This happens when papers were already deleted from paper_notes by prior triage
        if verdict == "UNKNOWN" and rule == "MISSING":
            print(f"{i:<3} {aid:<14} {name:<16} {expect:<8} {'SKIP':<10} {'N/A':<6} ⏭️  (not in paper_notes)")
            skipped.append((aid, name))
            continue
        ok = "✓" if verdict == expect else "✗"
        if verdict != expect:
            mismatches.append((aid, name, expect, verdict, rule, reason))
        print(f"{i:<3} {aid:<14} {name:<16} {expect:<8} {verdict:<10} {rule:<6} {ok}")

    n_tested = n_total - len(skipped)
    print()
    if skipped:
        print(f"⏭️  Skipped {len(skipped)} papers (not in paper_notes — already triaged out)")
    if mismatches:
        print(f"❌ FAIL: {len(mismatches)}/{n_tested} mismatch (of {n_tested} testable)")
        for aid, name, exp, got, rule, reason in mismatches:
            print(f"  {aid} {name}: expect={exp} got={got} ({rule}) — {reason}")
        return 1
    print(f"✅ PASS: {n_tested}/{n_tested} 一致 (mismatch=0, skipped={len(skipped)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
