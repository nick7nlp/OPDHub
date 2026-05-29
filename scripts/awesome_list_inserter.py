#!/usr/bin/env python3
"""
awesome_list_inserter.py — Code-level insertion of new papers into the OPD Awesome List.

5/19 老大 directive: Phase 4 GitHub editing 不能继续 LLM-driven, 必须代码层强制.
Risks if LLM-driven: 编造 arxiv URL / 错位 §section / 破坏表格格式 / 算错 badge.

This script:
  1. Reads V3 deep-read record from paper_notes.json[notes][aid] for canonical title/section/abstract.
  2. Validates section anchor exists in README.md.
  3. Generates a properly-formatted entry row.
  4. Inserts at the END of the corresponding §section table (before the next ## anchor or </details>).
  5. Updates the Papers-NNN badge.
  6. Optionally adds a row to the Pending Papers (🟡) summary table.
  7. git add + commit (message uses paper id + section).

Usage:
    python3 scripts/awesome_list_inserter.py --aid 2605.18141 \
        --section §5.3.2 \
        --model-pair "Qwen3-8B → Self" \
        --one-line "EMA teacher with iterative refinement; ..." \
        --code-url "https://github.com/foo/bar" \
        [--dry-run] [--commit]

    # Or batch from triage output:
    python3 scripts/awesome_list_inserter.py --batch-from-triage /tmp/triage_keep.json [--commit]
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SURVEY_ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
AWESOME_DIR = SURVEY_ROOT / "Awesome-LLM-On-Policy-Distillation"
README_PATH = AWESOME_DIR / "README.md"
NOTES_DB = SURVEY_ROOT / "notes" / "paper_notes.json"

# Section anchors (with their emoji + heading text — must match README exactly)
SECTION_HEADINGS = {
    "§4.1": "### 📌 §4.1 Fixed Divergence Objectives",
    "§4.2": "### 🌀 §4.2 Adaptive Divergence Objectives",
    "§4.3": "### 🎮 §4.3 RL-Augmented Objectives",
    "§5.1": "### 🔬 §5.1 White-Box Logit Supervision",
    "§5.2": "### 🕳️ §5.2 Black-Box and API-Constrained",
    "§5.3.1": "#### 💫 §5.3.1 Privileged Information",
    "§5.3.2": "#### ⚔️ §5.3.2 Pure Self-Distillation",
    "§5.3.3": "#### 📣 §5.3.3 External Feedback",
    "§6": "## ⚙️ §6 Training Efficiency and Stabilization",
    "§6.1": "## ⚙️ §6 Training Efficiency and Stabilization",  # alias — flat table
    "§6.2": "## ⚙️ §6 Training Efficiency and Stabilization",
    "§6.3": "## ⚙️ §6 Training Efficiency and Stabilization",
    "§7.1": "### 🎯 §7.1 Success Conditions & Empirical Analyses",
    "§7.2": "### ⚠️ §7.2 Failure Modes & Diagnostics",
    "§7.3": "### 📐 §7.3 Unified Theoretical Perspectives",
    "§8.1": "### 🏭 §8.1 Industrial Deployment",
    "§8.2": "### 🌟 §8.2 Emerging Domains",
}

BADGE_RE = re.compile(r'(<img src="https://img\.shields\.io/badge/Papers-)(\d+)(-blue" alt="Papers">)')
ARXIV_ID_RE = re.compile(r"^\d{4}\.\d{4,5}$")


def load_v3_record(aid: str) -> dict:
    if not NOTES_DB.exists():
        sys.exit(f"❌ {NOTES_DB} not found")
    db = json.loads(NOTES_DB.read_text())
    notes = db.get("notes", {})
    rec = notes.get(aid)
    if not rec:
        sys.exit(f"❌ {aid} not in paper_notes.json[notes]")
    if rec.get("_schema_version") != "v3":
        sys.exit(f"❌ {aid} schema is not v3 (got {rec.get('_schema_version')})")
    return rec


def find_section_block(readme_text: str, section_heading: str) -> tuple[int, int]:
    """
    Return (start_line, end_line) of the §section's paper table block.
    end_line is the last data row of the table (so insert after it).
    """
    lines = readme_text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.strip() == section_heading:
            start = i
            break
    if start is None:
        sys.exit(f"❌ section heading not found: {section_heading!r}")

    # Find the end of this section: next ## or ### at same/higher level
    target_level = section_heading.count("#")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        line = lines[j]
        m = re.match(r"^(#+)\s", line)
        if m and len(m.group(1)) <= target_level:
            end = j
            break

    # Find LAST table row inside [start, end) — must look like `| [...](http... | year | ... |`
    last_row = None
    for j in range(start, end):
        if lines[j].startswith("|") and "https://arxiv.org/abs/" in lines[j]:
            last_row = j
    if last_row is None:
        # fallback: try less strict — any table row starting with | 🟢/🟡 [ or | [
        for j in range(start, end):
            stripped = lines[j].lstrip()
            if stripped.startswith("| 🟢") or stripped.startswith("| 🟡") or (stripped.startswith("| [") and stripped.count("|") >= 3):
                last_row = j
    if last_row is None:
        sys.exit(f"❌ no paper table row found under {section_heading}")

    return start, last_row


def build_entry(aid: str, title: str, model_pair: str, one_line: str,
                year: int, code_url: str | None, status: str = "🟡") -> str:
    arxiv_url = f"https://arxiv.org/abs/{aid}"
    sub = f"📐 {model_pair}; {one_line}" if model_pair else f"📐 {one_line}"
    code_cell = ""
    if code_url:
        code_cell = f"[![Code](https://img.shields.io/badge/Code-GitHub-blue)]({code_url})"
    return f"| {status} [{title}]({arxiv_url}) <br><sub>{sub}</sub> | {year} | {code_cell} |"


def update_badge(readme_text: str, delta: int) -> tuple[str, int, int]:
    m = BADGE_RE.search(readme_text)
    if not m:
        sys.exit("❌ Papers-NNN badge not found")
    old = int(m.group(2))
    new = old + delta
    new_text = BADGE_RE.sub(rf"\g<1>{new}\g<3>", readme_text, count=1)
    return new_text, old, new


def find_pending_table(readme_text: str) -> tuple[int, int]:
    """
    Find the Pending Papers (🟡) table — its data rows.
    Returns (header_line, last_data_line).
    """
    lines = readme_text.split("\n")
    pending_h = None
    for i, line in enumerate(lines):
        if "## 📋 Pending Papers" in line:
            pending_h = i
            break
    if pending_h is None:
        return -1, -1  # absent — caller decides if optional

    # data rows after `| Paper | Section | Why Pending |`
    last_row = None
    for j in range(pending_h, min(pending_h + 100, len(lines))):
        if lines[j].startswith("|") and "https://arxiv.org/abs/" in lines[j]:
            last_row = j
    return pending_h, last_row if last_row else pending_h


def insert_into_section(readme_text: str, section: str, entry_line: str) -> str:
    heading = SECTION_HEADINGS.get(section)
    if not heading:
        sys.exit(f"❌ unknown section: {section!r}; available: {sorted(SECTION_HEADINGS)}")
    _start, last_row = find_section_block(readme_text, heading)
    lines = readme_text.split("\n")
    lines.insert(last_row + 1, entry_line)
    return "\n".join(lines)


def insert_into_pending(readme_text: str, aid: str, title: str, section: str, why: str) -> str:
    h, last = find_pending_table(readme_text)
    if h < 0:
        return readme_text  # no pending table
    lines = readme_text.split("\n")
    arxiv_url = f"https://arxiv.org/abs/{aid}"
    pending_row = f"| 🟡 [{title}]({arxiv_url}) | {section} | {why} |"
    lines.insert(last + 1, pending_row)
    return "\n".join(lines)


def already_present(readme_text: str, aid: str) -> bool:
    return f"https://arxiv.org/abs/{aid}" in readme_text


def insert_one(args, readme_text: str) -> tuple[str, dict]:
    rec = load_v3_record(args.aid)
    # Support both old schema (opd_classification.is_opd = "yes"/"analysis")
    # and new schema (top-level is_opd = True/False)
    cls = rec.get("opd_classification", {})
    is_opd_val = cls.get("is_opd") if cls else rec.get("is_opd")
    if is_opd_val not in ("yes", "analysis", True):
        sys.exit(f"❌ {args.aid} is_opd={is_opd_val!r} — refusing to add")

    title = args.title or rec.get("title", "").strip()
    section = args.section or cls.get("primary_section", "").strip()
    if not title or not section:
        sys.exit(f"❌ missing title ({title!r}) or section ({section!r})")
    if section not in SECTION_HEADINGS:
        sys.exit(f"❌ section {section!r} not in {sorted(SECTION_HEADINGS)}")

    if already_present(readme_text, args.aid):
        return readme_text, {"status": "already_present", "aid": args.aid}

    year = args.year or 2026
    one_line = args.one_line or rec.get("summary", "").strip() or "(see deep-read notes)"
    model_pair = args.model_pair or ""

    entry = build_entry(
        aid=args.aid, title=title, model_pair=model_pair,
        one_line=one_line, year=year, code_url=args.code_url, status="🟡"
    )

    new_text = insert_into_section(readme_text, section, entry)
    why = (cls.get("reasoning") or "Newly added; pending §section confirmation in next survey revision.")[:100]
    new_text = insert_into_pending(new_text, args.aid, title, section, why)
    new_text, old_badge, new_badge = update_badge(new_text, delta=1)

    return new_text, {
        "status": "inserted", "aid": args.aid, "section": section,
        "title": title, "badge_change": f"{old_badge}→{new_badge}",
    }


def git_commit(message: str, dry_run: bool = False):
    if dry_run:
        print(f"[git] DRY: would commit with: {message}")
        return
    subprocess.run(["git", "-C", str(AWESOME_DIR), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(AWESOME_DIR), "commit", "-m", message], check=True)
    print(f"[git] committed: {message}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aid", help="Single arxiv ID")
    ap.add_argument("--section", help="§4.1 / §5.3.2 / §8.2 / etc.")
    ap.add_argument("--title", help="Override title from V3 record")
    ap.add_argument("--model-pair", default="", help="e.g. 'Qwen3-8B → Self'")
    ap.add_argument("--one-line", default="", help="One-line method summary")
    ap.add_argument("--year", type=int)
    ap.add_argument("--code-url", help="Optional code repo URL")
    ap.add_argument("--batch-from-triage", help="JSON file with list of {aid, section, model_pair, one_line, code_url}")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--commit", action="store_true", help="git add + commit after success")
    args = ap.parse_args()

    if not (args.aid or args.batch_from_triage):
        ap.error("must specify --aid or --batch-from-triage")

    readme_text = README_PATH.read_text()
    summary = []

    if args.aid:
        if not ARXIV_ID_RE.match(args.aid):
            sys.exit(f"❌ invalid arxiv id: {args.aid!r}")
        readme_text, info = insert_one(args, readme_text)
        summary.append(info)

    if args.batch_from_triage:
        payload = json.loads(Path(args.batch_from_triage).read_text())
        for item in payload:
            class _A:
                aid = item["aid"]
                section = item.get("section")
                title = item.get("title")
                model_pair = item.get("model_pair", "")
                one_line = item.get("one_line", "")
                year = item.get("year", 2026)
                code_url = item.get("code_url")
            readme_text, info = insert_one(_A(), readme_text)
            summary.append(info)

    inserted = [s for s in summary if s["status"] == "inserted"]
    skipped = [s for s in summary if s["status"] == "already_present"]

    if args.dry_run:
        print("[inserter] DRY RUN")
        for s in summary:
            print(f"  {s}")
        return

    if not inserted:
        print(f"[inserter] No new insertions (already_present: {len(skipped)})")
        return

    README_PATH.write_text(readme_text)
    print(f"[inserter] wrote {README_PATH}")
    for s in inserted:
        print(f"  ✓ {s['aid']} → {s['section']} ({s['badge_change']})")

    if args.commit:
        if len(inserted) == 1:
            i = inserted[0]
            msg = f"Add {i['aid']} to {i['section']} ({i['title'][:60]})"
        else:
            msg = f"Add {len(inserted)} new papers ({', '.join(s['aid'] for s in inserted)})"
        git_commit(msg, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
