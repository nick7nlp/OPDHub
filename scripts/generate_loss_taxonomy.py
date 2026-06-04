#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the loss-taxonomy report from data/loss_classification.json.

Outputs:
  Awesome-LLM-On-Policy-Distillation/resources/loss-taxonomy.md
  Awesome-LLM-On-Policy-Distillation/assets/loss-distribution.png
  Awesome-LLM-On-Policy-Distillation/assets/loss-evolution.png
  data/loss_taxonomy.json   (canonical merged data: classification + paper meta)

Run after classify_loss_with_llm.py. Idempotent.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
PAPER_NOTES = ROOT / "notes" / "paper_notes.json"
SCHEMA = ROOT / "data" / "loss_taxonomy_schema.json"
CLASS_PATH = ROOT / "data" / "loss_classification.json"
TAX_OUT = ROOT / "data" / "loss_taxonomy.json"

AWESOME = ROOT / "Awesome-LLM-On-Policy-Distillation"
ASSETS = AWESOME / "assets"
RES_DIR = AWESOME / "resources"
MD_OUT = RES_DIR / "loss-taxonomy.md"
PNG_DIST = ASSETS / "loss-distribution.png"
PNG_EVO = ASSETS / "loss-evolution.png"

# 宋瓷雅色系 (per global CLAUDE.md)
SONGCI_COLORS = {
    "FKL":          "#5698C3",  # 天青 — base / classical
    "RKL":          "#C04851",  # 胭脂 — mode-seeking
    "Symmetric":    "#75B975",  # 松花 — balanced
    "f-Divergence": "#6E2C42",  # 紫檀 — generalized
    "KL+RL":        "#E89F71",  # 缃叶 — hybrid (warm)
    "Preference":   "#867892",  # 紫绛灰
    "Other":        "#525C68",  # 黛灰 — fallback
}
ORDER = ["FKL", "RKL", "Symmetric", "f-Divergence", "KL+RL", "Preference", "Other"]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def is_opd_yes(entry: dict) -> bool:
    if entry.get("is_opd") == "yes":
        return True
    inner = entry.get("opd_classification") or {}
    return inner.get("is_opd") == "yes"


def parse_yymm(arxiv_id: str):
    """2604.14084 -> (2026, 4)."""
    m = re.match(r"^(\d{2})(\d{2})\.\d{4,5}$", arxiv_id)
    if not m:
        return None
    yy, mm = m.group(1), m.group(2)
    year = 2000 + int(yy)
    month = int(mm)
    if 1 <= month <= 12:
        return year, month
    return None


def load_data():
    notes_doc = json.loads(PAPER_NOTES.read_text())
    notes = notes_doc.get("notes", notes_doc)
    schema = json.loads(SCHEMA.read_text())
    cls = json.loads(CLASS_PATH.read_text())
    # Anchor "last updated" to the underlying classification data, not wall-clock,
    # so re-running the generator with no input change is fully idempotent.
    last_updated = (cls.get("updated_at") or "").split(" ")[0] or datetime.now().strftime("%Y-%m-%d")
    # Restrict to papers actually listed in Awesome README — paper_notes may
    # contain entries we've cleaned out of scope (e.g. is_opd=yes but rollout=no).
    awesome_readme = ROOT / "Awesome-LLM-On-Policy-Distillation" / "README.md"
    if awesome_readme.exists():
        import re as _re
        readme_text = awesome_readme.read_text(encoding="utf-8")
        in_readme = set(_re.findall(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", readme_text))
        results = cls.get("results", {})
        if isinstance(results, dict):
            results = {aid: r for aid, r in results.items() if aid in in_readme}
        elif isinstance(results, list):
            results = [r for r in results if r.get("arxiv_id") in in_readme]
    else:
        results = cls.get("results", {})
    return notes, schema, results, last_updated


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def write_markdown(notes, schema, results, last_updated) -> None:
    today = last_updated
    total = len(results)
    dist = Counter(r["loss_class"] for r in results.values())
    confdist = Counter(r["confidence"] for r in results.values())

    lines = []
    lines.append("# Loss Taxonomy of On-Policy Distillation Papers")
    lines.append("")
    lines.append(f"_Last updated: {today}. Auto-generated from `data/loss_classification.json`."
                 " Re-run `scripts/generate_loss_taxonomy.py` to refresh._")
    lines.append("")
    lines.append(f"Each of the **{total}** OPD papers in this collection is assigned exactly one of seven "
                 "mutually-exclusive loss classes. Classification is performed by an LLM auditor that reads "
                 "each paper's `loss_formulation` (LaTeX), training-loop description, and key components, then "
                 "picks the dominant objective per the rules in `data/loss_taxonomy_schema.json`.")
    lines.append("")
    lines.append("![Loss Distribution](../assets/loss-distribution.png)")
    lines.append("")
    lines.append("## Class definitions (compact)")
    lines.append("")
    for cid in ORDER:
        c = next(c for c in schema["classes"] if c["id"] == cid)
        n = dist.get(cid, 0)
        pct = 100.0 * n / total if total else 0
        lines.append(f"### {cid} — {c['name']}  ·  **{n}** papers ({pct:.1f}%)")
        lines.append("")
        lines.append(f"`{c['expression']}`")
        lines.append("")
        lines.append(f"_Match rule._ {c['what_to_match']}")
        lines.append("")
    lines.append("## Distribution snapshot")
    lines.append("")
    lines.append("| Class | Papers | Share |")
    lines.append("|---|---:|---:|")
    for cid in ORDER:
        n = dist.get(cid, 0)
        pct = 100.0 * n / total if total else 0
        lines.append(f"| {cid} | {n} | {pct:.1f}% |")
    lines.append(f"| **Total** | **{total}** | 100% |")
    lines.append("")
    lines.append(f"_Confidence breakdown: high={confdist.get('high',0)}, "
                 f"medium={confdist.get('medium',0)}, low={confdist.get('low',0)}._")
    lines.append("")
    lines.append("![Loss Evolution Over Time](../assets/loss-evolution.png)")
    lines.append("")

    # Per-class detailed table
    lines.append("## Per-paper assignments")
    lines.append("")
    by_class = defaultdict(list)
    for arxiv_id, rec in results.items():
        by_class[rec["loss_class"]].append((arxiv_id, rec))

    for cid in ORDER:
        rows = sorted(by_class.get(cid, []), key=lambda x: x[0], reverse=True)
        if not rows:
            continue
        lines.append(f"### {cid} ({len(rows)})")
        lines.append("")
        lines.append("| arXiv | Title | Conf | Evidence |")
        lines.append("|---|---|---|---|")
        for arxiv_id, rec in rows:
            title = (rec.get("title") or notes.get(arxiv_id, {}).get("title", "")).replace("|", "\\|")
            if len(title) > 90:
                title = title[:87] + "..."
            ev = (rec.get("evidence") or "").replace("|", "\\|").replace("\n", " ")
            if len(ev) > 130:
                ev = ev[:127] + "..."
            url = f"https://arxiv.org/abs/{arxiv_id}"
            lines.append(f"| [{arxiv_id}]({url}) | {title} | {rec.get('confidence','?')} | {ev} |")
        lines.append("")

    # Tail: methodology
    lines.append("## Methodology")
    lines.append("")
    lines.append("- Source of truth: `notes/paper_notes.json` — every paper marked `is_opd=yes` is included.")
    lines.append("- Classifier: `scripts/classify_loss_with_llm.py` (Claude Opus via woa gateway, "
                 "no thinking, deterministic JSON output).")
    lines.append("- Daily refresh: hooked into the OPD daily-pipeline cron after Phase 5 (Awesome inserter); "
                 "only papers whose `loss_formulation` changed since last run are re-classified.")
    lines.append("- Spot-check policy: any paper with `confidence=low` is reviewed manually before "
                 "the next public refresh.")
    lines.append("")

    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[md] wrote {MD_OUT.relative_to(ROOT)} ({len(lines)} lines)")


# ---------------------------------------------------------------------------
# PNG: distribution bar chart
# ---------------------------------------------------------------------------

def plot_distribution(results) -> None:
    dist = Counter(r["loss_class"] for r in results.values())
    total = sum(dist.values())

    # Sort by count desc; preserves a stable order across rebuilds when ties tie
    # by the canonical taxonomy ORDER.
    canon_idx = {c: i for i, c in enumerate(ORDER)}
    items = sorted(
        [(c, dist.get(c, 0)) for c in ORDER if dist.get(c, 0) > 0],
        key=lambda kv: (-kv[1], canon_idx[kv[0]]),
    )
    labels = [c for c, _ in items]
    counts = [n for _, n in items]
    colors = [SONGCI_COLORS[c] for c in labels]

    # Horizontal bar chart, COLM serif font, songci palette.
    with plt.rc_context({
        "font.family": "serif",
        "font.serif": ["TeX Gyre Pagella", "Palatino", "serif"],
        "font.size": 11,
    }):
        fig_h = max(2.6, 0.55 * len(labels) + 1.2)
        fig, ax = plt.subplots(figsize=(8.6, fig_h))

        y = np.arange(len(labels))
        bars = ax.barh(y, counts, color=colors, edgecolor="none", height=0.62)

        # End-of-bar labels: "<count>  ·  <pct>%"
        max_n = max(counts)
        gap = max_n * 0.018
        for bar, n in zip(bars, counts):
            pct = 100 * n / total if total else 0
            ax.text(bar.get_width() + gap,
                    bar.get_y() + bar.get_height() / 2,
                    f"{n}  ·  {pct:.0f}%",
                    ha="left", va="center", fontsize=10.5,
                    color="#2b2b2b")

        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=11.5)
        ax.invert_yaxis()  # largest at top

        # Title block — small headline + grey subtitle
        ax.set_title("Loss-Objective Distribution",
                     fontsize=14.5, fontweight="bold", color="#1c1c1c",
                     loc="left", pad=18)
        ax.text(0.0, 1.02, f"{total} on-policy distillation papers",
                transform=ax.transAxes, fontsize=10.5,
                color="#525C68", style="italic", va="bottom")

        # Subtle x-grid only; remove all spines except bottom-left where helpful
        ax.set_xlim(0, max_n * 1.18)
        ax.set_xlabel("")
        ax.tick_params(axis="x", labelsize=9.5, colors="#525C68")
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", linestyle="--", linewidth=0.5,
                color="#b0b0b0", alpha=0.55)
        ax.set_axisbelow(True)
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color("#cccccc")
        ax.spines["bottom"].set_linewidth(0.8)

        fig.tight_layout()
        ASSETS.mkdir(parents=True, exist_ok=True)
        fig.savefig(PNG_DIST, dpi=200, facecolor="white", bbox_inches="tight")
        plt.close(fig)
    print(f"[png] wrote {PNG_DIST.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# PNG: stacked-bar evolution by year-month
# ---------------------------------------------------------------------------

def plot_evolution(results) -> None:
    bucket = defaultdict(Counter)  # (year, month) -> Counter
    for arxiv_id, rec in results.items():
        ym = parse_yymm(arxiv_id)
        if not ym:
            continue
        bucket[ym][rec["loss_class"]] += 1

    if not bucket:
        print("[png] no time data, skipping evolution plot")
        return
    months = sorted(bucket.keys())

    # x labels: e.g., '24-06', '24-09', ...
    labels = [f"{y%100:02d}-{m:02d}" for y, m in months]
    counts_per_class = {c: [bucket[ym].get(c, 0) for ym in months] for c in ORDER}

    fig, ax = plt.subplots(figsize=(13, 6))
    bottoms = np.zeros(len(months))
    x = np.arange(len(months))
    for c in ORDER:
        ys = np.array(counts_per_class[c])
        if ys.sum() == 0:
            continue
        ax.bar(x, ys, bottom=bottoms, color=SONGCI_COLORS[c], edgecolor="#2b2b2b",
               linewidth=0.4, label=c)
        bottoms += ys

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=10)
    ax.set_ylabel("Papers", fontsize=12, fontweight="bold")
    ax.set_xlabel("arXiv submission month", fontsize=12, fontweight="bold")
    ax.set_title(f"Evolution of OPD loss objectives over time ({len(results)} papers)",
                 fontsize=13, fontweight="bold", color="#212121", pad=14)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, color="#b0b0b0", alpha=0.6)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.85, ncol=2,
              edgecolor="#999", title="Loss class", title_fontsize=10)

    fig.tight_layout()
    fig.savefig(PNG_EVO, dpi=160, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"[png] wrote {PNG_EVO.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Canonical merged data
# ---------------------------------------------------------------------------

def write_taxonomy_data(notes, results, last_updated) -> None:
    merged = []
    for arxiv_id, rec in sorted(results.items(), reverse=True):
        entry = notes.get(arxiv_id, {})
        merged.append({
            "arxiv_id": arxiv_id,
            "title": rec.get("title") or entry.get("title", ""),
            "loss_class": rec["loss_class"],
            "confidence": rec.get("confidence"),
            "evidence": rec.get("evidence"),
            "secondary_class": rec.get("secondary_class"),
            "notes": rec.get("notes"),
            "loss_formulation_latex": (entry.get("method") or {}).get("loss_formulation"),
            "classified_at": rec.get("classified_at"),
            "model": rec.get("model"),
        })

    payload = {
        "generated_at": last_updated,
        "total": len(merged),
        "distribution": dict(Counter(r["loss_class"] for r in merged)),
        "papers": merged,
    }
    TAX_OUT.parent.mkdir(parents=True, exist_ok=True)
    TAX_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[json] wrote {TAX_OUT.relative_to(ROOT)} (total={len(merged)})")


def main():
    notes, schema, results, last_updated = load_data()
    if not results:
        print("no classification results yet — run scripts/classify_loss_with_llm.py first.")
        return
    write_markdown(notes, schema, results, last_updated)
    plot_distribution(results)
    plot_evolution(results)
    write_taxonomy_data(notes, results, last_updated)
    print(f"\nDone. {len(results)} papers classified.")


if __name__ == "__main__":
    main()
