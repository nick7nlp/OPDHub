#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the OPD survey companion site.

Reads:
  notes/paper_notes.json                                — deep-read meta
  data/loss_taxonomy.json                               — per-paper loss class
  Awesome-LLM-On-Policy-Distillation/README.md          — section grouping + 1-line desc
  latex-v4/main.tex                                     — abstract block
  awesome-llm-opd-site/templates/index.html.tmpl        — page template

Writes:
  awesome-llm-opd-site/index.html                       — public page
  awesome-llm-opd-site/data/papers.json                 — fuse.js search index

Idempotent: timestamps anchored to source-data updated_at, not wall-clock.

Run: python3 scripts/build_site.py
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict, OrderedDict
from html import escape
from pathlib import Path

ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
PAPER_NOTES = ROOT / "notes" / "paper_notes.json"
LOSS_TAX = ROOT / "data" / "loss_taxonomy.json"
AWESOME_README = ROOT / "Awesome-LLM-On-Policy-Distillation" / "README.md"
MAIN_TEX = ROOT / "latex-v4" / "main.tex"

SITE = ROOT / "awesome-llm-opd-site"
TEMPLATE = SITE / "templates" / "index.html.tmpl"
INDEX_OUT = SITE / "index.html"
PAPERS_JSON = SITE / "static" / "data" / "papers.json"

# Loss class colors (songci) — kept consistent with generate_loss_taxonomy.py
LOSS_ORDER = ["FKL", "RKL", "Symmetric", "f-Divergence", "KL+RL", "Preference", "Other"]

# === New filter chip dimensions (added 2026-06-02) ===
DOMAIN_ORDER = [
    "Math", "Code", "Reasoning", "Agent", "Multimodal",
    "Alignment", "Inference", "Preference", "General",
]
SIGNAL_ORDER = [
    "External-Teacher", "Self", "Privileged-Info", "Verifier", "Other-Signal",
]
FREQ_ORDER = ["per-step", "per-outer-iter", "once-before-training", "n/a"]
SIZE_ORDER = ["<3B", "3-10B", "10-30B", ">30B", "Unknown"]


def infer_domain(title: str, description: str) -> str:
    """Heuristic domain bucket from title + Awesome README one-liner."""
    t = ((title or "") + " " + (description or "")).lower()
    if any(k in t for k in ["math", "gsm8k", "aime", "math500", "mathreason"]):
        return "Math"
    if any(k in t for k in ["code", "humaneval", "mbpp", "codeforces", "programming"]):
        return "Code"
    if any(k in t for k in ["agent", "tool", "multi-turn", "webshop", "workflow"]):
        return "Agent"
    if any(k in t for k in ["multimodal", "vision", "image", "vlm", "vqa"]):
        return "Multimodal"
    if any(k in t for k in ["reason", "cot", "chain-of-thought", "thinking"]):
        return "Reasoning"
    if any(k in t for k in ["speculative", "decoding", "inference speed"]):
        return "Inference"
    if any(k in t for k in ["safety", "alignment"]):
        return "Alignment"
    if any(k in t for k in ["preference", "dpo"]):
        return "Preference"
    return "General"


def normalize_signal_source(s) -> str:
    """Map raw schema-v3 signal_source string into 5 buckets."""
    if isinstance(s, list):
        s = s[0] if s else ""
    s_low = (s or "").lower().strip()
    if not s_low or s_low == "unknown":
        return "Other-Signal"
    if any(k in s_low for k in ["pi(", "privileged", "hindsight"]):
        return "Privileged-Info"
    if "verifier" in s_low or "rlvr" in s_low:
        return "Verifier"
    if any(k in s_low for k in ["teacher", "oracle", "external"]):
        # Check if it's also "self" — if both, prefer External
        return "External-Teacher"
    if "self" in s_low or "ema" in s_low:
        return "Self"
    return "Other-Signal"


def normalize_rollout_freq(s: str) -> str:
    """Normalize free-text rollout_frequency into 4 fixed buckets."""
    s_low = (s or "").lower()
    if not s_low:
        return "n/a"
    if "per-step" in s_low or "every step" in s_low or "per step" in s_low:
        return "per-step"
    if "outer-iter" in s_low or "outer iter" in s_low or "per epoch" in s_low:
        return "per-outer-iter"
    if any(k in s_low for k in ["before-training", "before training", "precompute",
                                 "pre-compute", "static", "offline"]):
        return "once-before-training"
    return "n/a"


def extract_student_size_bucket(note) -> str:
    """Pull student.size_B from teacher_student_pairs[0] and bucket."""
    if not isinstance(note, dict):
        return "Unknown"
    pairs = note.get("teacher_student_pairs") or []
    if not pairs or not isinstance(pairs[0], dict):
        return "Unknown"
    student = pairs[0].get("student") or {}
    if not isinstance(student, dict):
        return "Unknown"
    b = student.get("size_B")
    if b is None:
        return "Unknown"
    try:
        b = float(b)
    except (TypeError, ValueError):
        return "Unknown"
    if b < 3:
        return "<3B"
    if b < 10:
        return "3-10B"
    if b < 30:
        return "10-30B"
    return ">30B"


# Section ordering for the public site
SECTION_ORDER = [
    ("§4 Objective Functions and Optimization", ["§4.1", "§4.2", "§4.3"]),
    ("§5 Signal Source and Teacher Architecture", ["§5.1", "§5.2", "§5.3"]),
    ("§6 Training Efficiency and Stabilization", ["§6"]),
    ("§7 Understanding OPD", ["§7", "§7.1", "§7.2", "§7.3"]),
    ("§8 Applications, Systems, and Emerging Domains", ["§8", "§8.1", "§8.2", "§8.3"]),
]

SECTION_BLURB = {
    "§4.1": "Fixed Divergence Objectives",
    "§4.2": "Adaptive Divergence Objectives",
    "§4.3": "RL-Augmented Objectives",
    "§5.1": "White-Box Logit Supervision",
    "§5.2": "Black-Box and API-Constrained",
    "§5.3": "Self-Distillation",
    "§6":   "Efficiency, Stability, and Compute",
    "§7":   "Understanding OPD",
    "§7.1": "Success Conditions and Empirical Analyses",
    "§7.2": "Failure Modes and Diagnostics",
    "§7.3": "Unified Theoretical Perspectives",
    "§8":   "Applications and Emerging Domains",
    "§8.1": "Industrial Deployment",
    "§8.2": "Emerging Domains",
    "§8.3": "System-Level Integration",
}

CAROUSEL_FIGURES = []  # carousel removed; kept var only to avoid touching call-sites

BIBTEX = """@article{song2026opdsurvey,
  title  = {A Survey of On-Policy Distillation for Large Language Models},
  author = {Mingyang Song and Mao Zheng},
  journal= {arXiv preprint arXiv:2604.00626},
  year   = {2026}
}"""

# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def is_opd_yes(entry: dict) -> bool:
    if entry.get("is_opd") == "yes":
        return True
    inner = entry.get("opd_classification") or {}
    return inner.get("is_opd") == "yes"


def parse_yymm(arxiv_id: str):
    m = re.match(r"^(\d{2})(\d{2})\.\d{4,5}$", arxiv_id)
    if not m:
        return None, None
    yy, mm = int(m.group(1)), int(m.group(2))
    if not (1 <= mm <= 12):
        return None, None
    return 2000 + yy, mm


def latex_to_text(s: str) -> str:
    """Trim a small subset of LaTeX commands that appear in our prose."""
    if not s:
        return ""
    s = re.sub(r"\\emph\{([^}]*)\}", r"<em>\1</em>", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"<strong>\1</strong>", s)
    s = re.sub(r"\\citep\{[^}]*\}", "", s)
    s = re.sub(r"\\citet\{[^}]*\}", "", s)
    s = re.sub(r"\\cite\{[^}]*\}", "", s)
    s = re.sub(r"\$([^$]+)\$", lambda m: f"<i>{escape(m.group(1))}</i>", s)
    s = s.replace("~", " ")
    return s.strip()


CJK_RE = re.compile(r"[　-〿㐀-䶿一-鿿＀-￯]")


def strip_chinese(text: str) -> str:
    """Strip CJK characters and salvage the surrounding English skeleton.

    Used for fields that mix English math/code names with Chinese
    annotations, e.g. "PPO-style clipped reverse KL (低熵 token)" ->
    "PPO-style clipped reverse KL (token)".

    Drops empty parens, double spaces, dangling punctuation, and tail
    commas/semicolons/periods left over after the strip.
    """
    if not text:
        return ""
    s = CJK_RE.sub(" ", str(text))
    # Drop now-empty parentheses / brackets
    s = re.sub(r"\(\s*\)|\[\s*\]|（\s*）|【\s*】", "", s)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    # Strip trailing/leading punctuation noise
    s = re.sub(r"^[，,;:、。.\s]+|[，,、；;:\s]+$", "", s)
    return s


def english_ratio(text: str) -> float:
    if not text:
        return 0.0
    total = len(text)
    cjk = len(CJK_RE.findall(text))
    return 1 - (cjk / total if total else 0)


# Unicode → LaTeX command map. Some loss_formulation entries use raw unicode
# (e.g. "L = -E_{y~p_θ} Σ ∇_θ log p_θ(...)") which KaTeX can't typeset as math.
# Translating to LaTeX commands lets KaTeX render them as proper symbols.
UNICODE_TO_LATEX = {
    # Greek lowercase
    "α": "\\alpha ", "β": "\\beta ", "γ": "\\gamma ", "δ": "\\delta ",
    "ε": "\\epsilon ", "ζ": "\\zeta ", "η": "\\eta ", "θ": "\\theta ",
    "ι": "\\iota ", "κ": "\\kappa ", "λ": "\\lambda ", "μ": "\\mu ",
    "ν": "\\nu ", "ξ": "\\xi ", "π": "\\pi ", "ρ": "\\rho ",
    "σ": "\\sigma ", "τ": "\\tau ", "υ": "\\upsilon ", "φ": "\\phi ",
    "χ": "\\chi ", "ψ": "\\psi ", "ω": "\\omega ",
    "ϕ": "\\phi ", "ϵ": "\\epsilon ",
    # Greek uppercase
    "Α": "A", "Β": "B", "Γ": "\\Gamma ", "Δ": "\\Delta ", "Ε": "E",
    "Ζ": "Z", "Η": "H", "Θ": "\\Theta ", "Ι": "I", "Κ": "K",
    "Λ": "\\Lambda ", "Μ": "M", "Ν": "N", "Ξ": "\\Xi ", "Π": "\\Pi ",
    "Ρ": "P", "Σ": "\\Sigma ", "Τ": "T", "Υ": "\\Upsilon ",
    "Φ": "\\Phi ", "Χ": "X", "Ψ": "\\Psi ", "Ω": "\\Omega ",
    # Operators / relations
    "∇": "\\nabla ", "∂": "\\partial ", "∞": "\\infty ",
    "∑": "\\sum ", "∏": "\\prod ", "∫": "\\int ",
    "≤": "\\leq ", "≥": "\\geq ", "≠": "\\neq ", "≈": "\\approx ",
    "≡": "\\equiv ", "∈": "\\in ", "∉": "\\notin ", "⊂": "\\subset ",
    "⊆": "\\subseteq ", "∪": "\\cup ", "∩": "\\cap ", "∅": "\\emptyset ",
    "→": "\\to ", "←": "\\leftarrow ", "↔": "\\leftrightarrow ",
    "⇒": "\\Rightarrow ", "⇐": "\\Leftarrow ", "⇔": "\\Leftrightarrow ",
    "·": "\\cdot ", "×": "\\times ", "÷": "\\div ", "±": "\\pm ",
    "∥": "\\|", "‖": "\\|",
    # Special
    "ℓ": "\\ell ", "ℝ": "\\mathbb{R}", "ℕ": "\\mathbb{N}",
    "ℤ": "\\mathbb{Z}", "ℚ": "\\mathbb{Q}", "ℂ": "\\mathbb{C}", "ℰ": "\\mathcal{E}",
    # Tildes (used as approximation in some equations)
    "~": "\\sim ",
    # Fancy quotes that sometimes leak in
    "“": "``", "”": "''", "‘": "`", "’": "'",
}


def unicode_to_latex(s: str) -> str:
    """Translate raw Unicode math symbols into LaTeX commands so KaTeX can
    typeset them. Already-escaped (\\theta etc.) source passes through
    unchanged because nothing in the table starts with a backslash."""
    if not s:
        return s
    return "".join(UNICODE_TO_LATEX.get(ch, ch) for ch in s)


def shorten_pair_name(name: str) -> str:
    """'Qwen3-4B-Base-GRPO' -> 'Qwen3-4B-GRPO'. Drop -Base / -Instruct suffix."""
    if not name:
        return ""
    s = name.split("(")[0].strip()
    s = re.sub(r"-Base(-|$)", r"\1", s)
    return s.rstrip("-").strip()


def fmt_size(b) -> str:
    if b is None:
        return ""
    try:
        b = float(b)
    except (TypeError, ValueError):
        return ""
    if b < 0.1:
        # Tiny models < 100M shown in millions for clarity (e.g. T5-Small 77M)
        return f"{b * 1000:.0f}M"
    if b == int(b):
        return f"{int(b)}B"
    return f"{b:g}B"


def make_cite_key(aid: str, note: dict) -> str:
    """Generate a stable BibTeX cite key like 'smith2026grpo'."""
    year = str(note.get("year") or "2026")
    af = note.get("authors_first") or ""
    name_clean = re.sub(r"[^A-Za-z\s]", "", af).strip()
    parts = name_clean.split()
    last = parts[-1].lower() if parts else "anon"
    title = note.get("title") or aid
    words = re.findall(r"[A-Z][a-z]{2,}", title)
    kw = words[0].lower()[:8] if words else re.sub(r"\D", "", aid)[:6]
    return f"{last}{year}{kw}"


def make_bibtex(aid: str, note: dict, title: str) -> str:
    """Generate minimal arXiv BibTeX entry for a paper."""
    key = make_cite_key(aid, note)
    af = note.get("authors_first") or ""
    author_str = (af + " et al.") if af else "Unknown Authors"
    year = note.get("year") or 2026
    safe_title = (title or "").replace("{", "").replace("}", "")
    lines = [
        f"@article{{{key},",
        f"  title   = {{{safe_title}}},",
        f"  author  = {{{author_str}}},",
        f"  journal = {{arXiv preprint arXiv:{aid}}},",
        f"  year    = {{{year}}}",
        "}",
    ]
    return "\n".join(lines)


def compute_recent_months(n: int = 3) -> list:
    """Return the n most recent YYYY-MM strings (e.g. ['2026-06', '2026-05', '2026-04'])."""
    import datetime
    today = datetime.date.today()
    months = []
    y, m = today.year, today.month
    for _ in range(n):
        months.append(f"{y}-{m:02d}")
        m -= 1
        if m == 0:
            m, y = 12, y - 1
    return months


def attr_escape(s: str) -> str:
    """HTML-escape a string for use in a double-quoted attribute, including newlines."""
    return escape(s, quote=True).replace("\n", "&#10;").replace("\r", "")


def make_cite_key(aid: str, note: dict) -> str:
    """Generate a stable BibTeX cite key like 'smith2026grpo'."""
    year = str(note.get("year") or "2026")
    af = note.get("authors_first") or ""
    name_clean = re.sub(r"[^A-Za-z\s]", "", af).strip()
    parts = name_clean.split()
    last = parts[-1].lower() if parts else "anon"
    title = note.get("title") or aid
    words = re.findall(r"[A-Z][a-z]{2,}", title)
    kw = words[0].lower()[:8] if words else re.sub(r"\D", "", aid)[:6]
    return f"{last}{year}{kw}"


def make_bibtex(aid: str, note: dict, title: str) -> str:
    """Generate minimal arXiv BibTeX entry for a paper."""
    key = make_cite_key(aid, note)
    af = note.get("authors_first") or ""
    author_str = (af + " et al.") if af else "Unknown Authors"
    year = note.get("year") or 2026
    safe_title = (title or "").replace("{", "").replace("}", "")
    lines = [
        f"@article{{{key},",
        f"  title   = {{{safe_title}}},",
        f"  author  = {{{author_str}}},",
        f"  journal = {{arXiv preprint arXiv:{aid}}},",
        f"  year    = {{{year}}}",
        "}",
    ]
    return "\n".join(lines)


def compute_recent_months(n: int = 3) -> list:
    """Return the n most recent YYYY-MM strings (e.g. ['2026-06', '2026-05', '2026-04'])."""
    import datetime
    today = datetime.date.today()
    months = []
    y, m = today.year, today.month
    for _ in range(n):
        months.append(f"{y}-{m:02d}")
        m -= 1
        if m == 0:
            m, y = 12, y - 1
    return months


def attr_escape(s: str) -> str:
    """HTML-escape a string for use in a double-quoted attribute, including newlines."""
    return escape(s, quote=True).replace("\n", "&#10;").replace("\r", "")


def load_abstract() -> str:
    txt = MAIN_TEX.read_text(encoding="utf-8")
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", txt, re.DOTALL)
    if not m:
        return ""
    return latex_to_text(m.group(1).strip())


def load_paper_notes():
    doc = json.loads(PAPER_NOTES.read_text(encoding="utf-8"))
    return doc.get("notes", doc), doc.get("last_updated", "")


def load_loss_tax():
    doc = json.loads(LOSS_TAX.read_text(encoding="utf-8"))
    by_id = {p["arxiv_id"]: p for p in doc.get("papers", [])}
    return by_id, doc.get("generated_at", "")


# ---------------------------------------------------------------------------
# Awesome README parsing
# ---------------------------------------------------------------------------

# Match any markdown row containing an arxiv link. We don't care about exact
# column layout — README has multiple table styles (Hall of Fame, trends,
# main §4-§8). We extract the title + arxiv id, then synthesize the section
# from the surrounding H3 heading and an optional inline §X.Y cell.
ARXIV_LINK_RE = re.compile(
    r"\[(?P<title>(?:\*\*)?[^\]]+?(?:\*\*)?)\]\(https?://arxiv\.org/abs/(?P<aid>[\w\.\-]+)\)"
)
INLINE_SECTION_RE = re.compile(r"\|\s*(§\d(?:\.\d+)?(?:\.\d+)?)\s*\|")
SUB_DESC_RE = re.compile(r"<sub>[^<]*?(?:📐|💡|🎯)?\s*(?P<desc>[^<]+)</sub>")
# Code badge: [![Code](https://img.shields.io/badge/Code-...)](URL)
# We capture the URL after the second `](`; URL is anything until next `)`.
CODE_BADGE_RE = re.compile(
    r"\[!\[Code\]\([^)]*\)\]\((?P<url>https?://[^)]+)\)"
)
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*$")

# H3 heading -> canonical section. Driven by the actual headings in the
# Awesome README; if a new heading is added the parser will fall back to
# regex extraction.
H3_TO_SECTION = {
    "📌 §4.1 Fixed Divergence Objectives":       "§4.1",
    "🌀 §4.2 Adaptive Divergence Objectives":    "§4.2",
    "🎮 §4.3 RL-Augmented Objectives":            "§4.3",
    "🔬 §5.1 White-Box Logit Supervision":        "§5.1",
    "🕳️ §5.2 Black-Box and API-Constrained":      "§5.2",
    "🔁 §5.3 Self-Distillation":                  "§5.3",
    "🏭 §8.1 Industrial Deployment":              "§8.1",
    "🌟 §8.2 Emerging Domains":                   "§8.2",
    "🔧 §8.3 System-Level Integration":           "§8.3",
    "🎯 §7.1 Success Conditions & Empirical Analyses": "§7.1",
    "⚠️ §7.2 Failure Modes & Diagnostics":        "§7.2",
    "📐 §7.3 Unified Theoretical Perspectives":   "§7.3",
}

# H2 fallback when no H3 is active (e.g. §6 has no H3 sub-sections).
H2_TO_SECTION = {
    "⚙️ §6 Training Efficiency and Stabilization":     "§6",
    "🚀 §8 Applications, Systems, and Emerging Domains": "§8",
    "🧠 §7 Understanding OPD":                          "§7",
}


def normalize_section(s: str) -> str:
    """'§4.1 Fixed Divergence Objectives' -> '§4.1'."""
    if not s:
        return ""
    m = re.match(r"(§\d(?:\.\d+)?)", s)
    return m.group(1) if m else s.strip()


def parse_awesome_readme():
    """Yield {arxiv_id, title, section, description, code_url}.

    The README contains 3 table layouts:
      A) | [Title](url) | §X.Y | description |
      B) | [**Title**](url) | Why Read It |    (Hall of Fame)
      C) | [Title](url) <br><sub>📐 desc</sub> | YYYY | resources |  (§4-§8 main)

    A paper may appear in multiple tables. We MERGE rows by arxiv_id,
    preferring: (i) longest title, (ii) longest description, (iii) any
    code_url that turns up in any of its rows. The section is taken from
    the first row that has a real §X.Y assignment (Hall of Fame rows
    contribute "Hall of Fame" only if no real section row exists).
    """
    text = AWESOME_README.read_text(encoding="utf-8")
    current_h2 = ""
    current_h3 = ""
    current_h2_section = ""
    current_h3_section = ""
    by_id: "dict[str, dict]" = {}

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        m2 = H2_RE.match(line)
        if m2:
            current_h2 = m2.group(1).strip()
            current_h3 = ""
            current_h2_section = H2_TO_SECTION.get(current_h2, "")
            current_h3_section = ""
            continue

        m3 = H3_RE.match(line)
        if m3:
            current_h3 = m3.group(1).strip()
            current_h3_section = H3_TO_SECTION.get(current_h3, "")
            continue

        if not line.startswith("|") or "arxiv.org/abs/" not in line:
            continue

        m = ARXIV_LINK_RE.search(line)
        if not m:
            continue

        aid = m.group("aid").strip()
        title = m.group("title").strip().strip("*").strip()

        # Section resolution
        inline = INLINE_SECTION_RE.search(line)
        if inline:
            section = inline.group(1)
        elif current_h3_section:
            section = current_h3_section
        elif current_h2_section:
            section = current_h2_section
        else:
            section = ""

        # Skip rows from "Pending Papers" / "Survey Version History" / etc.
        if section == "" and current_h2 not in H2_TO_SECTION:
            if "Hall of Fame" in current_h2 or current_h2.startswith("🏆"):
                section = "Hall of Fame"
            else:
                continue

        # Description extraction
        desc = ""
        sub = SUB_DESC_RE.search(line)
        if sub:
            desc = sub.group("desc").strip()
        else:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 3:
                for c in reversed(cells):
                    if c and c != section and "arxiv.org" not in c:
                        desc = c
                        break

        code_m = CODE_BADGE_RE.search(line)
        code_url = code_m.group("url") if code_m else ""

        prev = by_id.get(aid)
        if prev is None:
            by_id[aid] = {
                "arxiv_id": aid,
                "title": title,
                "section": section,
                "description": desc,
                "code_url": code_url,
                "_h2": current_h2,
                "_h3": current_h3,
            }
        else:
            # Merge: prefer real §X.Y section over "Hall of Fame"
            if prev["section"] in ("", "Hall of Fame") and section and section != "Hall of Fame":
                prev["section"] = section
                prev["_h2"] = current_h2
                prev["_h3"] = current_h3
            # Prefer longer title
            if len(title) > len(prev["title"]):
                prev["title"] = title
            # Prefer longer / non-empty description
            if len(desc) > len(prev["description"]):
                prev["description"] = desc
            # Prefer any code_url over none
            if code_url and not prev["code_url"]:
                prev["code_url"] = code_url

    return list(by_id.values())


# ---------------------------------------------------------------------------
# JOIN + record assembly
# ---------------------------------------------------------------------------

def build_records():
    notes, _last_notes = load_paper_notes()
    loss_by_id, _last_tax = load_loss_tax()
    awesome_rows = parse_awesome_readme()

    # awesome row is the SOURCE OF TRUTH for which papers appear on the site
    # (we want every catalog entry, even those still pending deep-read).
    seen = set()
    records = []
    for row in awesome_rows:
        aid = row["arxiv_id"]
        if aid in seen:
            continue
        seen.add(aid)
        note = notes.get(aid, {}) if isinstance(notes, dict) else {}

        year, month = parse_yymm(aid) if re.match(r"^\d{4}\.\d{4,5}$", aid) else (None, None)
        # fallback to deep-read year
        if not year:
            try:
                year = int(note.get("year")) if note.get("year") else None
            except (TypeError, ValueError):
                year = None

        title = row["title"] or note.get("title", "") or aid

        method = (note.get("method") or {}) if isinstance(note, dict) else {}
        key_components = method.get("key_components") or ""
        if isinstance(key_components, list):
            key_components = " ".join(str(x) for x in key_components)

        loss_class = (loss_by_id.get(aid) or {}).get("loss_class")

        # New chip dimensions
        domain = infer_domain(title, row.get("description", ""))
        opd_cls = (note.get("opd_classification") or {}) if isinstance(note, dict) else {}
        opm = (note.get("on_policy_mechanism") or {}) if isinstance(note, dict) else {}
        signal_source = normalize_signal_source(
            opd_cls.get("signal_source") or opm.get("signal_source") or ""
        )
        rollout_freq = normalize_rollout_freq(opm.get("rollout_frequency") or "")
        student_size = extract_student_size_bucket(note)

        # === Public-safe expandable detail fields (English-only, paper-derived) ===

        # 1. Pair: "Qwen3-8B → Qwen3-0.6B (8B → 0.6B)"
        ts_pairs = note.get("teacher_student_pairs") or [] if isinstance(note, dict) else []
        pair_html = ""
        if ts_pairs and isinstance(ts_pairs[0], dict):
            t = ts_pairs[0].get("teacher") or {}
            s = ts_pairs[0].get("student") or {}
            tn = shorten_pair_name(t.get("name", "")) if isinstance(t, dict) else ""
            sn = shorten_pair_name(s.get("name", "")) if isinstance(s, dict) else ""
            tb = fmt_size(t.get("size_B")) if isinstance(t, dict) else ""
            sb = fmt_size(s.get("size_B")) if isinstance(s, dict) else ""
            if tn and sn:
                t_label = f"{escape(tn)}" + (f" <span class=\"size-badge\">{escape(tb)}</span>" if tb else "")
                s_label = f"{escape(sn)}" + (f" <span class=\"size-badge\">{escape(sb)}</span>" if sb else "")
                if isinstance(s, dict) and s.get("is_self"):
                    pair_html = f"{s_label} <span class=\"pair-arrow\">↻</span> <em>self-distill</em>"
                else:
                    pair_html = f"{t_label} <span class=\"pair-arrow\">→</span> {s_label}"

        # 2. Method: bullet list of key_components, English-only items
        method_items = []
        kc = method.get("key_components") or []
        if isinstance(kc, list):
            for item in kc[:5]:
                cleaned = strip_chinese(str(item))
                if cleaned and english_ratio(cleaned) > 0.5 and len(cleaned) >= 5:
                    method_items.append(cleaned)

        # 3. Result: top 3 benchmarks with numerical deltas
        result_items = []
        bm = note.get("benchmarks") if isinstance(note, dict) else None
        if not isinstance(bm, list):
            bm = []
        for b in bm[:6]:
            if not isinstance(b, dict):
                continue
            bname = strip_chinese(b.get("name") or "")
            if not bname or english_ratio(bname) < 0.5:
                continue
            base = b.get("student_baseline")
            after = b.get("student_after_OPD")
            delta = b.get("delta")
            gap = b.get("gap_closed_pct")
            if base is not None and after is not None:
                line = f"{bname}: {base}% → {after}%"
                if delta is not None:
                    line += f" <span class=\"delta-up\">(+{delta})</span>" if (isinstance(delta, (int, float)) and delta > 0) else f" ({delta})"
                result_items.append(line)
            elif gap is not None:
                result_items.append(f"{bname}: {gap}% gap closed")
            elif after is not None:
                result_items.append(f"{bname}: {after}%")
            if len(result_items) >= 3:
                break

        # 4. Equation: loss formulation, full first-line LaTeX (KaTeX-rendered client-side).
        # No truncation — KaTeX needs balanced LaTeX. If a paper's first line is
        # malformed for any reason, the JS init script silently hides the block.
        loss_eq = method.get("loss_formulation") or ""
        # Pick first non-empty line (some entries put alignment scaffolding on later lines)
        first_line = ""
        for ln in loss_eq.split("\n"):
            ln = ln.strip()
            if ln:
                first_line = ln
                break
        # Strip any CJK that snuck into the math (rare, defensive)
        first_line = strip_chinese(first_line)
        # Translate raw Unicode math symbols into LaTeX commands so KaTeX
        # renders e.g. "Σ ∇_θ" as proper symbols instead of falling back to text.
        first_line = unicode_to_latex(first_line)
        equation_text = first_line if first_line and english_ratio(first_line) > 0.7 else ""
        # Drop prose-y "equations" — entries with no LaTeX commands AND no `=` /
        # `<` / `>` / `:=` AND lots of English words are paraphrases of the
        # method, not formulas. Rendering them in displayMode makes them look
        # like garbled math; better to omit and let users click arXiv.
        if equation_text:
            has_latex = "\\" in equation_text
            has_assign = bool(re.search(r"[=<>]|:=", equation_text))
            word_count = len(re.findall(r"\b[a-z]{3,}\b", equation_text))
            if not has_latex and not has_assign and word_count >= 5:
                equation_text = ""

        # 5. Who: authors_first et al · affiliation · venue
        who_parts = []
        af = note.get("authors_first", "") if isinstance(note, dict) else ""
        if af:
            who_parts.append(f"{strip_chinese(af)} et al")
        aff = note.get("affiliation_primary", "") if isinstance(note, dict) else ""
        if aff:
            who_parts.append(strip_chinese(aff))
        venue = note.get("venue") if isinstance(note, dict) else None
        if venue and isinstance(venue, str) and english_ratio(venue) > 0.5:
            who_parts.append(strip_chinese(venue))
        who_text = " · ".join(p for p in who_parts if p)

        records.append({
            "arxiv_id": aid,
            "title": title,
            "code_url": row.get("code_url", "") or "",
            "year": year,
            "month": month,
            "year_month": (f"{year}-{month:02d}" if year and month else (str(year) if year else "")),
            "section": row["section"],
            "section_blurb": SECTION_BLURB.get(row["section"], ""),
            "loss_class": loss_class or "Other",
            "domain": domain,
            "signal_source": signal_source,
            "rollout_freq": rollout_freq,
            "student_size": student_size,
            "description": row["description"],
            # search-only fields
            "key_components_search": key_components,
            # public-safe rendered HTML fragments
            "pair_html":     pair_html,
            "method_items":  method_items,
            "result_items":  result_items,
            "equation_text": equation_text,
            "who_text":      who_text,
            "bibtex":        make_bibtex(aid, note, title),
        })
    # 2026-06-02 (revised): Hall of Fame papers are legitimate OPD papers — keep
    # them on site, but remap their "Hall of Fame" parser-section to the v3 LLM's
    # opd_classification.primary_section so they group correctly under §4-§8.
    # (The previous "drop entirely" rule applied only to badly-categorized "Other".)
    for r in records:
        if r["section"] == "Hall of Fame":
            n = notes.get(r["arxiv_id"], {}) if isinstance(notes, dict) else {}
            cls = n.get("opd_classification") if isinstance(n, dict) else None
            ps = cls.get("primary_section") if isinstance(cls, dict) else None
            if ps:
                r["section"] = ps
                r["section_blurb"] = SECTION_BLURB.get(ps, "")
    # Any HoF row that still couldn't be remapped (no v3 section) is discarded.
    records = [r for r in records if r["section"] != "Hall of Fame"]
    return records


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

def html_carousel():
    items = []
    for src, caption in CAROUSEL_FIGURES:
        items.append(
            '<div class="item">'
            '<div class="image-container">'
            f'<img src="{src}" alt="{escape(caption)}"/>'
            '</div>'
            f'<h2 class="subtitle has-text-centered carousel-caption">{escape(caption)}</h2>'
            '</div>'
        )
    return "\n        ".join(items)


def html_chip(group: str, value: str, count: int) -> str:
    label = escape(value)
    return (f'<span class="chip" data-value="{escape(value)}">'
            f'{label}<span class="chip-count">{count}</span></span>')


def html_filter_chips(records):
    sec_count = Counter(r["section"] for r in records if r["section"])
    loss_count = Counter(r["loss_class"] for r in records)
    year_count = Counter(str(r["year"]) for r in records if r["year"])
    domain_count = Counter(r["domain"] for r in records)
    sig_count = Counter(r["signal_source"] for r in records)
    freq_count = Counter(r["rollout_freq"] for r in records)
    size_count = Counter(r["student_size"] for r in records)

    # Section chips: include parents §4 §5 §7 §8 + leaves
    section_values = []
    for parent, leaves in SECTION_ORDER:
        prefix = parent.split()[0]  # '§4'
        parent_count = sum(c for s, c in sec_count.items() if s == prefix or s.startswith(prefix + "."))
        section_values.append((prefix, parent_count))
        for leaf in leaves:
            if leaf == prefix:
                continue
            section_values.append((leaf, sec_count.get(leaf, 0)))

    sec_html = "\n        ".join(html_chip("section", v, c) for v, c in section_values if c > 0)
    loss_html = "\n        ".join(html_chip("loss", v, loss_count.get(v, 0))
                                  for v in LOSS_ORDER if loss_count.get(v, 0) > 0)
    years_sorted = sorted(year_count.keys())
    year_html = "\n        ".join(html_chip("year", y, year_count[y]) for y in years_sorted)

    domain_html = "\n        ".join(html_chip("domain", v, domain_count.get(v, 0))
                                     for v in DOMAIN_ORDER if domain_count.get(v, 0) > 0)
    sig_html = "\n        ".join(html_chip("signal", v, sig_count.get(v, 0))
                                  for v in SIGNAL_ORDER if sig_count.get(v, 0) > 0)
    freq_html = "\n        ".join(html_chip("freq", v, freq_count.get(v, 0))
                                   for v in FREQ_ORDER if freq_count.get(v, 0) > 0)
    size_html = "\n        ".join(html_chip("size", v, size_count.get(v, 0))
                                   for v in SIZE_ORDER if size_count.get(v, 0) > 0)

    recent_months = compute_recent_months(3)
    recent_count = Counter(r["year_month"] for r in records if r["year_month"] in recent_months)
    recent_html = "\n        ".join(
        html_chip("recent", ym, recent_count.get(ym, 0))
        for ym in recent_months
        if recent_count.get(ym, 0) > 0
    )

    return sec_html, loss_html, year_html, domain_html, sig_html, freq_html, size_html, recent_html


def loss_badge_class(loss: str) -> str:
    safe = loss.replace("+", "\\+")  # css-escape, but we handle in style.css
    return f"badge-loss-{loss}"


def html_monthly_chart(records, start_ym: str = "2025-01") -> str:
    """SVG line chart of paper count per month, starting at `start_ym`.

    Pre-`start_ym` records are excluded entirely. Zero-count months are
    rendered as on-line points so the time axis is continuous and the
    visual contrast against the recent peak is preserved. Songci 胭脂
    #C04851 stroke + light area fill, Inconsolata mono labels.
    """
    counts: Counter[str] = Counter()
    for r in records:
        ym = r.get("year_month", "")
        if re.match(r"^\d{4}-(0[1-9]|1[0-2])$", ym) and ym >= start_ym:
            counts[ym] += 1
    if not counts:
        return ""

    # Build a continuous month sequence from start_ym to the latest observed month
    def add_month(ym: str) -> str:
        y, m = (int(p) for p in ym.split("-"))
        m += 1
        if m > 12:
            m, y = 1, y + 1
        return f"{y}-{m:02d}"

    last_ym = max(counts.keys())
    months = [start_ym]
    while months[-1] != last_ym:
        months.append(add_month(months[-1]))

    max_n = max(counts.values()) or 1
    total = sum(counts.values())
    n = len(months)

    # Geometry — fixed viewBox, scales responsively via CSS
    pad_l, pad_r, pad_t, pad_b = 32, 16, 28, 36
    w, h = 760, 200
    inner_w = w - pad_l - pad_r
    inner_h = h - pad_t - pad_b
    step = inner_w / max(n - 1, 1)

    def x_at(i: int) -> float:
        return pad_l + i * step

    def y_at(c: float) -> float:
        return pad_t + inner_h * (1 - c / max_n)

    pts = [(x_at(i), y_at(counts.get(m, 0))) for i, m in enumerate(months)]

    # Path strings
    path_line = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    y_baseline = y_at(0)
    path_area = (
        f"M {pts[0][0]:.1f},{y_baseline:.1f} "
        + "L " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        + f" L {pts[-1][0]:.1f},{y_baseline:.1f} Z"
    )

    # Grid lines at 0 and max
    grid = (
        f'<line x1="{pad_l}" y1="{y_at(0):.1f}" x2="{w-pad_r}" y2="{y_at(0):.1f}" '
        f'stroke="#e6dfd8" stroke-width="1"/>'
        f'<line x1="{pad_l}" y1="{y_at(max_n):.1f}" x2="{w-pad_r}" y2="{y_at(max_n):.1f}" '
        f'stroke="#efe9e3" stroke-width="1" stroke-dasharray="2,3"/>'
    )

    # Y-axis labels (0 and max)
    y_labels = (
        f'<text x="{pad_l-8:.1f}" y="{y_at(0)+4:.1f}" text-anchor="end" '
        f'font-size="11" fill="#867892" font-family="Inconsolata,monospace">0</text>'
        f'<text x="{pad_l-8:.1f}" y="{y_at(max_n)+4:.1f}" text-anchor="end" '
        f'font-size="11" fill="#867892" font-family="Inconsolata,monospace">{max_n}</text>'
    )

    # Data-point circles + non-zero count labels
    circles, value_labels = [], []
    for (x, y), m in zip(pts, months):
        c = counts.get(m, 0)
        circles.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" '
            f'fill="#C04851" stroke="#fff" stroke-width="1"/>'
        )
        if c > 0:
            value_labels.append(
                f'<text x="{x:.1f}" y="{y-10:.1f}" text-anchor="middle" '
                f'font-size="11" fill="#525C68" font-family="Inconsolata,monospace" '
                f'font-weight="600">{c}</text>'
            )

    # X-axis labels — full YYYY-MM at i==0 and every January, MM otherwise
    x_labels = []
    for i, m in enumerate(months):
        yyyy, mm = m.split("-")
        label = f"{yyyy}-{mm}" if (mm == "01" or i == 0) else mm
        x_labels.append(
            f'<text x="{x_at(i):.1f}" y="{h-12:.1f}" text-anchor="middle" '
            f'font-size="11" fill="#867892" font-family="Inconsolata,monospace">{label}</text>'
        )

    svg = (
        f'<svg class="monthly-chart" viewBox="0 0 {w} {h}" '
        f'xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" '
        f'role="img" aria-label="Monthly OPD paper count from {start_ym}">'
        + grid
        + f'<path d="{path_area}" fill="#C04851" fill-opacity="0.10"/>'
        + f'<path d="{path_line}" fill="none" stroke="#C04851" stroke-width="2.2" '
        + 'stroke-linejoin="round" stroke-linecap="round"/>'
        + "".join(circles)
        + "".join(value_labels)
        + "".join(x_labels)
        + y_labels
        + '</svg>'
    )
    caption = (
        f'<p class="monthly-chart-caption">'
        f'On-Policy Distillation papers, monthly '
        f'<span class="muted">&middot; from {start_ym} &middot; '
        f'{total} papers</span>'
        f'</p>'
    )
    return svg + caption


def html_paper_list(records):
    # Group by parent section in declared order.
    groups = OrderedDict()
    for parent_label, _leaves in SECTION_ORDER:
        groups[parent_label] = []
    other = []

    def parent_for(section: str) -> str:
        if not section:
            return ""
        prefix = section.split(".")[0]  # '§4.1' -> '§4'
        for label, _ in SECTION_ORDER:
            if label.startswith(prefix + " "):
                return label
        return ""

    for r in records:
        parent = parent_for(r["section"])
        if parent:
            groups[parent].append(r)
        else:
            other.append(r)

    parts = []
    for parent_label, items in groups.items():
        if not items:
            continue
        # sort: newer first by year_month desc, then arxiv_id desc
        items.sort(key=lambda x: (x["year"] or 0, x["month"] or 0, x["arxiv_id"]), reverse=True)
        parts.append(f'<div class="paper-section-group" data-parent="{escape(parent_label)}">')
        parts.append(f'<h2>{escape(parent_label)}</h2>')

        # sub-group by leaf section under this parent
        by_leaf = defaultdict(list)
        for item in items:
            by_leaf[item["section"]].append(item)
        for leaf in sorted(by_leaf.keys()):
            blurb = SECTION_BLURB.get(leaf, "")
            head = f"{escape(leaf)}"
            if blurb:
                head += f" &mdash; <span style=\"color:#777;font-weight:500;\">{escape(blurb)}</span>"
            parts.append(f'<h3>{head}</h3>')
            parts.append('<ul class="paper-group">')
            for r in by_leaf[leaf]:
                parts.append(render_paper_card(r))
            parts.append('</ul>')
        parts.append('</div>')

    # The trailing "Other" bucket is intentionally not rendered:
    # Hall of Fame is filtered out in build_records, and any remaining
    # uncategorised paper is a data-quality issue we want to surface in build
    # logs rather than hide on the site.
    if other:
        ids = ", ".join(r["arxiv_id"] for r in other)
        print(f"[warn] {len(other)} paper(s) with unknown section dropped: {ids}")

    return "\n".join(parts)


def render_paper_card(r: dict) -> str:
    aid = r["arxiv_id"]
    title = escape(r["title"])
    desc = escape(r["description"])
    section = escape(r["section"])
    loss = r["loss_class"]
    ym = r["year_month"]
    arxiv_link = f"https://arxiv.org/abs/{aid}"
    arxiv_text = aid if re.match(r"^\d{4}\.\d{4,5}$", aid) else "link"

    # === Expandable detail panel — 5 distinctly-styled blocks ===
    detail_parts = []

    # Block 1: PAIR (azure)
    if r.get("pair_html"):
        detail_parts.append(
            f'<div class="paper-detail-block detail-pair">'
            f'<div class="paper-detail-label">Pair</div>'
            f'<div class="paper-detail-body pair-line">{r["pair_html"]}</div>'
            f'</div>'
        )

    # Block 2: METHOD (pine)
    method_items = r.get("method_items") or []
    if method_items:
        items = "".join(f"<li>{escape(item)}</li>" for item in method_items)
        detail_parts.append(
            f'<div class="paper-detail-block detail-method">'
            f'<div class="paper-detail-label">Method</div>'
            f'<ul class="paper-detail-list">{items}</ul>'
            f'</div>'
        )

    # Block 3: RESULT (amber)
    result_items = r.get("result_items") or []
    if result_items:
        # result_items already contain inline HTML <span> for delta arrow
        items = "".join(f"<li>{item}</li>" for item in result_items)
        detail_parts.append(
            f'<div class="paper-detail-block detail-result">'
            f'<div class="paper-detail-label">Result</div>'
            f'<ul class="paper-detail-list">{items}</ul>'
            f'</div>'
        )

    # Block 4: LOSS / EQUATION (sandal). LaTeX is stored in data-tex
    # for client-side KaTeX rendering; the textContent shows raw source as
    # a graceful fallback if JS is disabled or KaTeX fails to load.
    eq = r.get("equation_text") or ""
    if eq:
        detail_parts.append(
            f'<div class="paper-detail-block detail-equation">'
            f'<div class="paper-detail-label">Loss</div>'
            f'<div class="paper-detail-eq" data-tex="{escape(eq, quote=True)}">'
            f'<code class="eq-fallback">{escape(eq)}</code>'
            f'</div>'
            f'</div>'
        )

    # Block 5: WHO (muted)
    who = r.get("who_text") or ""
    if who:
        detail_parts.append(
            f'<div class="paper-detail-block detail-who">'
            f'<div class="paper-detail-label">Who</div>'
            f'<div class="paper-detail-body">{escape(who)}</div>'
            f'</div>'
        )

    detail_html = ""
    has_detail = bool(detail_parts)
    if has_detail:
        detail_html = f'<div class="paper-detail">{"".join(detail_parts)}</div>'

    expand_class = " has-detail" if has_detail else ""
    toggle_html = '<span class="paper-expand-toggle" aria-label="toggle details">▾</span>' if has_detail else ""

    # Top-row badges
    badges = [
        f'<a class="badge badge-arxiv" href="{arxiv_link}" target="_blank" rel="noopener">arXiv {escape(ym or arxiv_text)}</a>',
        f'<span class="badge badge-section">{section}</span>',
        f'<span class="badge badge-loss-{escape(loss)}">{escape(loss)}</span>',
    ]
    if r.get("code_url"):
        badges.append(
            f'<a class="badge badge-code" href="{escape(r["code_url"])}" target="_blank" rel="noopener" title="Code repository">'
            f'<i class="fa-brands fa-github"></i>&nbsp;Code</a>'
        )
    badges.append(
        f'<button class="badge badge-cite" title="Copy BibTeX to clipboard">'
        f'<i class="fas fa-quote-right"></i>&nbsp;<span class="cite-label">Cite</span>'
        f'</button>'
    )

    return (
        f'<li class="paper-card{expand_class} loss-{escape(loss)}" '
        f'data-arxiv-id="{escape(aid)}" '
        f'data-section="{section}" '
        f'data-loss="{escape(loss)}" '
        f'data-year="{r["year"] or ""}" '
        f'data-domain="{escape(r.get("domain","") or "")}" '
        f'data-signal="{escape(r.get("signal_source","") or "")}" '
        f'data-freq="{escape(r.get("rollout_freq","") or "")}" '
        f'data-size="{escape(r.get("student_size","") or "")}" '
        f'data-yearmonth="{escape(r.get("year_month","") or "")}" '
        f'data-bibtex="{attr_escape(r.get("bibtex","") or "")}">'
        f'<span class="paper-title">{title}{toggle_html}</span>'
        f'<span class="paper-meta">{"".join(badges)}</span>'
        f'<span class="paper-desc">{desc}</span>'
        f'{detail_html}'
        f'</li>'
    )


# ---------------------------------------------------------------------------
# Search index payload
# ---------------------------------------------------------------------------

def write_papers_json(records, last_updated):
    # Minimal public-safe payload: every field here MUST be derivable from
    # public sources (arXiv metadata + the Awesome list README). We deliberately
    # omit the rich rendered detail (pair_html, method_items, ...) because they
    # are baked into index.html. Search keys are surfaced here for fuse.js.
    payload = {
        "generated_at": last_updated,
        "total": len(records),
        "papers": [
            {
                "arxiv_id":    r["arxiv_id"],
                "title":       r["title"],
                "year":        r["year"],
                "year_month":  r["year_month"],
                "section":     r["section"],
                "loss_class":  r["loss_class"],
                "domain":      r.get("domain", ""),
                "signal":      r.get("signal_source", ""),
                "freq":        r.get("rollout_freq", ""),
                "size":        r.get("student_size", ""),
                "description": r["description"],
                "code_url":    r.get("code_url", ""),
            }
            for r in records
        ],
    }
    PAPERS_JSON.parent.mkdir(parents=True, exist_ok=True)
    PAPERS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[json] wrote {PAPERS_JSON.relative_to(ROOT)} ({len(records)} entries)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def asset_version() -> str:
    """8-char content hash of CSS+JS, for cache-busting query string."""
    import hashlib
    h = hashlib.md5()
    for p in [
        SITE / "static" / "css" / "style.css",
        SITE / "static" / "js" / "search.js",
        SITE / "static" / "js" / "bibtex.js",
    ]:
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:8]


def main():
    records = build_records()

    # Anchor the "last updated" stamp to the loss-taxonomy.generated_at — this
    # is the most recently refreshed input; using wall-clock would break idempotency.
    _, last_tax = load_loss_tax()
    last_updated = (last_tax or "").split(" ")[0] or "2026-06-01"

    sec_html, loss_html, year_html, domain_html, sig_html, freq_html, size_html, recent_html = html_filter_chips(records)
    paper_list_html = html_paper_list(records)
    monthly_chart_html = html_monthly_chart(records)

    template = TEMPLATE.read_text(encoding="utf-8")
    html = (template
            .replace("{{ASSET_VERSION}}",    asset_version())
            .replace("{{MONTHLY_CHART}}",    monthly_chart_html)
            .replace("{{FILTER_SECTIONS}}",  sec_html)
            .replace("{{FILTER_LOSSES}}",    loss_html)
            .replace("{{FILTER_YEARS}}",     year_html)
            .replace("{{FILTER_DOMAINS}}",   domain_html)
            .replace("{{FILTER_SIGNALS}}",   sig_html)
            .replace("{{FILTER_FREQS}}",     freq_html)
            .replace("{{FILTER_SIZES}}",     size_html)
            .replace("{{FILTER_RECENT}}",    recent_html)
            .replace("{{PAPER_LIST}}",       paper_list_html)
            .replace("{{BIBTEX}}",           BIBTEX))

    INDEX_OUT.write_text(html, encoding="utf-8")
    print(f"[html] wrote {INDEX_OUT.relative_to(ROOT)} ({len(records)} papers, {len(html)} bytes)")

    write_papers_json(records, last_updated)
    print(f"\nDone. {len(records)} papers indexed; site ready in {SITE.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
