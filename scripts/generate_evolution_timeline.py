"""Generate Evolution Timeline figure for the Awesome-LLM-On-Policy-Distillation README.

Replaces the hand-drawn assets/evolution-timeline.png. Content is sourced from
the README Hall of Fame so the figure stays aligned with the canonical
era / paper assignment whenever Hall of Fame is updated.

Style: COLM template (TeX Gyre Pagella) + 宋瓷雅色系 palette, matching
generate_atlas_heatmap.py and generate_loss_taxonomy.py.

Output:
    Awesome-LLM-On-Policy-Distillation/assets/evolution-timeline.png
    Awesome-LLM-On-Policy-Distillation/assets/evolution-timeline.pdf
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
ASSETS = ROOT / "Awesome-LLM-On-Policy-Distillation" / "assets"

# 宋瓷雅色系 — 5 era colors mirror generate_loss_taxonomy.py palette
PALETTE = {
    "pre":       "#525C68",  # 黛灰 — pre-2023 background
    "found":     "#5698C3",  # 天青 — 2023 foundations
    "evol":      "#75B975",  # 松花 — 2024 evolution
    "frontier1": "#C04851",  # 胭脂 — 2025-2026 frontier (left half)
    "frontier2": "#6E2C42",  # 紫檀 — 2026 industrial / agentic
}

matplotlib.rcParams.update({
    "font.family": "serif",
    "font.serif": ["TeX Gyre Pagella", "Palatino", "serif"],
    "font.size": 11,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "axes.linewidth": 0.0,
})


# Era cards. Each card: (label, year_range, color_key, papers).
# Content mirrors README Hall of Fame and the latex-v4 §3 narrative.
ERAS: List[Tuple[str, str, str, List[str]]] = [
    ("Pre-OPD", "2015–2017", "pre", [
        "Hinton KD (soft targets)",
        "Seq-KD (Kim & Rush)",
    ]),
    ("Foundations", "2023", "found", [
        "GKD (DAgger for LLMs)",
        "MiniLLM (Reverse-KL)",
        "f-Divergence KD",
        "Lion (black-box OPD)",
    ]),
    ("Evolution", "2024", "evol", [
        "DistiLLM (skew-KL)",
        "Speculative KD",
        "SPIN (self-play)",
        "AKL (adaptive)",
    ]),
    ("Frontier · Methods", "2025–2026", "frontier1", [
        "OPSD (privileged info)",
        "AlignDistil (RLHF bridge)",
        "Rethinking OPD (field guide)",
        "SCOPE (diversity collapse)",
        "SDZero (binary→dense)",
    ]),
    ("Frontier · Agentic & Industrial", "2026", "frontier2", [
        "SOD (step-wise OPD)",
        "TCOD (multi-turn agents)",
        "Uni-OPD (dual-perspective)",
        "DeepSeek-V4 (multi-domain)",
        "Qwen3 / Gemma-2 / MiMo",
    ]),
]


def draw_era_card(ax, x, y, w, h, era_label, year_label, color, papers):
    """Render one era card with rounded corners, title bar, and bullet list."""
    # Card background
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=1.2, edgecolor=color, facecolor=color + "15", zorder=2,
    )
    ax.add_patch(box)

    # Title bar (filled rectangle at top)
    title_h = 0.42
    title_box = FancyBboxPatch(
        (x, y + h - title_h), w, title_h,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=0, edgecolor="none", facecolor=color, zorder=3,
    )
    ax.add_patch(title_box)
    ax.text(x + w / 2, y + h - title_h / 2, era_label,
            ha="center", va="center", color="white",
            fontsize=11, fontweight="bold", zorder=4)
    ax.text(x + w / 2, y + h - title_h - 0.18, year_label,
            ha="center", va="center", color=color,
            fontsize=9.5, fontweight="bold", style="italic", zorder=4)

    # Paper bullet list
    bullet_top = y + h - title_h - 0.42
    line_h = 0.28
    for i, p in enumerate(papers):
        ax.text(x + 0.18, bullet_top - i * line_h,
                f"• {p}", ha="left", va="top",
                fontsize=8.6, color="#2c2c2c", zorder=4)


def build_figure() -> plt.Figure:
    n_eras = len(ERAS)
    card_w = 3.05
    card_gap = 0.45
    card_h = 2.95

    fig_w = card_w * n_eras + card_gap * (n_eras - 1) + 1.0
    fig_h = card_h + 2.20
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.set_aspect("equal")
    ax.axis("off")

    # Title block — pinned to the top so it never overlaps the era cards.
    title_y = fig_h - 0.50
    subtitle_y = fig_h - 0.92
    ax.text(fig_w / 2, title_y,
            "Evolution of On-Policy Distillation for LLMs",
            ha="center", va="center", fontsize=17, fontweight="bold",
            color="#1c1c1c")
    ax.text(fig_w / 2, subtitle_y,
            "2015  →  2026",
            ha="center", va="center", fontsize=11,
            color="#525C68", style="italic")

    # Baseline arrow — close to the cards, not at the very bottom.
    arrow_y = 0.45
    arrow = FancyArrowPatch(
        (0.4, arrow_y), (fig_w - 0.4, arrow_y),
        arrowstyle="->", mutation_scale=22,
        linewidth=1.6, color="#525C68", zorder=1,
    )
    ax.add_patch(arrow)

    # Era cards
    card_y = 0.85
    x = 0.5
    for label, year, color_key, papers in ERAS:
        color = PALETTE[color_key]
        draw_era_card(ax, x, card_y, card_w, card_h, label, year, color, papers)

        # Tick + connector to baseline
        cx = x + card_w / 2
        ax.plot([cx, cx], [card_y, arrow_y + 0.04],
                color=color, linewidth=1.0, linestyle=(0, (2, 2)),
                alpha=0.55, zorder=1)
        ax.plot(cx, arrow_y, marker="o", color=color, markersize=8,
                markeredgecolor="white", markeredgewidth=1.2, zorder=3)
        x += card_w + card_gap

    # "You are here" marker on the rightmost era
    last_x = 0.5 + (n_eras - 1) * (card_w + card_gap) + card_w / 2
    ax.annotate(
        "you are here",
        xy=(last_x, arrow_y), xytext=(last_x - 1.1, arrow_y - 0.30),
        fontsize=9, color=PALETTE["frontier2"], fontweight="bold",
        style="italic",
        arrowprops=dict(arrowstyle="->", color=PALETTE["frontier2"], lw=1.0),
        ha="center",
    )

    # Inflection point label between Evolution and Frontier
    inflect_x = 0.5 + 2 * (card_w + card_gap) + card_w + card_gap / 2
    ax.plot(inflect_x, arrow_y, marker="*", color="#C04851",
            markersize=18, markeredgecolor="white", markeredgewidth=1.0,
            zorder=4)
    ax.text(inflect_x, arrow_y - 0.25,
            "inflection point  ·  reasoning models",
            ha="center", va="top", fontsize=8.4,
            color="#C04851", style="italic")

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig


def main() -> None:
    fig = build_figure()
    out_png = ASSETS / "evolution-timeline.png"
    out_pdf = ASSETS / "evolution-timeline.pdf"
    fig.savefig(out_png, bbox_inches="tight", facecolor="white", dpi=200)
    fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out_png}")
    print(f"wrote {out_pdf}")


if __name__ == "__main__":
    main()
