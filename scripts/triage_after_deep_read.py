#!/usr/bin/env python3
"""Triage scouted papers after deep-read judgment.

For each candidate paper that has been deep-read:
- is_opd == "yes" or "analysis"
    → keep PDF in month bucket + by-aid symlink
    → keep paper_notes.json entry
    → add to Awesome List (manually, this script just prints suggestion)
- is_opd == "no"
    → delete PDF from staging/month-bucket
    → delete by-aid symlink
    → remove paper_notes.json entry
    → append to excluded-papers.md with reason
    → add to known_arxiv_ids.txt to avoid re-scouting
- is_opd not set / schema < v3
    → skip (deep-read not done yet)

Usage:
    python3 triage_after_deep_read.py --candidates 2605.15239,2605.15417,...
    python3 triage_after_deep_read.py --candidates-from-file /path/to/list.txt
    python3 triage_after_deep_read.py --staging-dir   # process all in pdfs/_staging/
    python3 triage_after_deep_read.py --dry-run       # preview only
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SURVEY_ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
PDF_ROOT = SURVEY_ROOT / "pdfs"
STAGING_DIR = PDF_ROOT / "_staging"
BY_AID = PDF_ROOT / "by-aid"
NOTES_DB = SURVEY_ROOT / "notes" / "paper_notes.json"
EXCLUDED_LOG = SURVEY_ROOT / "papers-meta" / "excluded-papers.md"
KNOWN_IDS = SURVEY_ROOT / "papers-meta" / "known_arxiv_ids.txt"
WHITELIST = Path("/root/.openclaw/workspace/memory/opd-new-papers.md")


def load_notes():
    if not NOTES_DB.exists():
        return {"notes": {}, "_meta": {}}
    return json.loads(NOTES_DB.read_text())


def save_notes(db):
    # Schema discipline: 顶级 keys = {'notes', 'last_updated'} only
    db["last_updated"] = datetime.utcnow().isoformat() + "Z"
    # Remove any legacy _meta key from old script versions
    db.pop("_meta", None)
    NOTES_DB.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def find_pdf(paper_id):
    """Find PDF anywhere in pdfs/ tree."""
    by_aid_link = BY_AID / f"{paper_id}.pdf"
    if by_aid_link.exists() or by_aid_link.is_symlink():
        # Resolve symlink to real PDF
        try:
            return [by_aid_link.resolve()]
        except Exception:
            pass
    pdfs = list(PDF_ROOT.rglob(f"{paper_id}.pdf"))
    return pdfs


def append_excluded(paper_id, title, reason):
    EXCLUDED_LOG.parent.mkdir(parents=True, exist_ok=True)
    if not EXCLUDED_LOG.exists():
        EXCLUDED_LOG.write_text(
            "# Excluded Papers (Deep-read judged not OPD)\n\n"
            "Papers that scout candidate-flagged but deep-read determined to be out of OPD scope.\n"
            "These IDs are also added to `known_arxiv_ids.txt` to avoid re-scouting.\n\n"
            "| Date | arXiv ID | Title | Reason |\n"
            "|------|----------|-------|--------|\n"
        )
    today = datetime.utcnow().strftime("%Y-%m-%d")
    line = f"| {today} | {paper_id} | {title[:80]} | {reason[:120]} |\n"
    with EXCLUDED_LOG.open("a") as f:
        f.write(line)


def append_known(paper_id):
    if KNOWN_IDS.exists():
        existing = set(KNOWN_IDS.read_text().split())
        if paper_id in existing:
            return
        with KNOWN_IDS.open("a") as f:
            f.write(f"{paper_id}\n")
    else:
        KNOWN_IDS.write_text(f"{paper_id}\n")


def remove_from_whitelist_pending(paper_id):
    """Remove paper_id from `当前待集成` table in opd-new-papers.md."""
    if not WHITELIST.exists():
        return False
    text = WHITELIST.read_text()
    lines = text.split("\n")
    new_lines = []
    removed = False
    for line in lines:
        # 识别 markdown 表格行 包含 paper_id
        if line.startswith("|") and paper_id in line:
            removed = True
            continue
        new_lines.append(line)
    if removed:
        WHITELIST.write_text("\n".join(new_lines))
    return removed


def triage_paper(paper_id, db, dry_run=False):
    """Returns (action, detail) where action ∈ {keep, exclude, skip}."""
    notes = db.get("notes", {})
    rec = notes.get(paper_id)
    if not rec or rec.get("_schema_version") != "v3":
        return ("skip", f"No v3 deep-read record for {paper_id}")

    cls = rec.get("opd_classification", {}) or {}
    is_opd = cls.get("is_opd", "").lower()
    title = rec.get("title", "Unknown")
    reasoning = cls.get("reasoning", "")

    if is_opd in ("yes", "analysis"):
        return ("keep", f"is_opd={is_opd}; section={cls.get('primary_section', '?')}; title={title[:60]}")

    if is_opd == "no":
        # exclude flow — delete non-OPD PDFs directly (no .trash accumulation)
        action_log = []
        # 1. rm PDF directly (pipeline-scouted papers only; pre-existing background
        #    papers are never passed to triage, so safe to rm here)
        pdfs = find_pdf(paper_id)
        for pdf in pdfs:
            try:
                if not dry_run:
                    pdf.unlink()
                    if pdf.exists():
                        action_log.append(f"FAIL rm failed: {pdf}")
                        continue
                action_log.append(f"rm {pdf.name}")
            except Exception as e:
                action_log.append(f"rm-fail {pdf}: {e}")

        # 2. delete by-aid symlink
        link = BY_AID / f"{paper_id}.pdf"
        if link.is_symlink() or link.exists():
            try:
                if not dry_run:
                    link.unlink()
                action_log.append(f"unlinked {link.name}")
            except Exception as e:
                action_log.append(f"unlink-fail: {e}")

        # 3. remove from notes db
        if not dry_run:
            del notes[paper_id]
        action_log.append("removed from paper_notes.json")

        # 4. log to excluded
        if not dry_run:
            append_excluded(paper_id, title, reasoning or "is_opd=no per deep-read")
            append_known(paper_id)
        action_log.append("logged to excluded-papers.md + known_arxiv_ids.txt")

        # 5. remove from pending whitelist
        if not dry_run:
            removed = remove_from_whitelist_pending(paper_id)
            if removed:
                action_log.append("removed from opd-new-papers.md pending")

        return ("exclude", "; ".join(action_log))

    return ("skip", f"is_opd={is_opd!r} unrecognized")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", help="Comma-separated arxiv IDs")
    ap.add_argument("--candidates-from-file", help="File with one arxiv ID per line")
    ap.add_argument("--staging-dir", action="store_true",
                    help="Process all PDFs found in pdfs/_staging/")
    ap.add_argument("--all-pending", action="store_true",
                    help="Process all paper IDs from opd-new-papers.md `当前待集成` table")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    candidates = []
    if args.candidates:
        candidates = [s.strip() for s in args.candidates.split(",") if s.strip()]
    if args.candidates_from_file:
        candidates += [l.strip() for l in Path(args.candidates_from_file).read_text().splitlines() if l.strip() and not l.startswith("#")]
    if args.staging_dir and STAGING_DIR.exists():
        for p in STAGING_DIR.glob("*.pdf"):
            candidates.append(p.stem)
    if args.all_pending and WHITELIST.exists():
        text = WHITELIST.read_text()
        in_pending = False
        import re
        for line in text.split("\n"):
            if "当前待集成" in line:
                in_pending = True
                continue
            if in_pending and line.startswith("## "):
                break
            m = re.match(r"\|\s*\d+\s*\|\s*(2[56]\d{2}\.\d{4,5})\s*\|", line)
            if m:
                candidates.append(m.group(1))

    candidates = list(dict.fromkeys(candidates))  # dedup, preserve order
    if not candidates:
        print("No candidates specified. Use --candidates / --candidates-from-file / --staging-dir / --all-pending")
        sys.exit(1)

    print(f"[triage] {len(candidates)} candidates {'(DRY RUN)' if args.dry_run else ''}")
    print()

    db = load_notes()
    summary = {"keep": 0, "exclude": 0, "skip": 0}
    for pid in candidates:
        action, detail = triage_paper(pid, db, dry_run=args.dry_run)
        symbol = {"keep": "✅", "exclude": "🗑️", "skip": "⏭️"}[action]
        print(f"  {symbol} {pid:14s} [{action:7s}] {detail}")
        summary[action] += 1

    if not args.dry_run:
        save_notes(db)

    print()
    print(f"[triage] summary: {summary['keep']} kept, {summary['exclude']} excluded, {summary['skip']} skipped")
    if args.dry_run:
        print("[triage] DRY RUN — no changes written.")


if __name__ == "__main__":
    main()
