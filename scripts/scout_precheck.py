#!/usr/bin/env python3
"""
OPD Scout Pre-Check: Weekend skip + Fast dedup refresh.

Usage (called at the start of daily-opd-paper-pipeline):
    python3 scripts/scout_precheck.py [--refresh-ids] [--check-weekend]

Exit codes:
    0 = proceed with full scout
    1 = skip today (weekend with no new arXiv submissions)
    2 = error

Actions:
    --refresh-ids: Regenerate papers-meta/known_arxiv_ids.txt from all 4 sources
    --check-weekend: Check if today is a weekend (Sat/Sun) with no new arXiv submissions
                     (arXiv doesn't post new papers on Sat/Sun)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

SURVEY_DIR = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
KNOWN_IDS_FILE = SURVEY_DIR / "papers-meta" / "known_arxiv_ids.txt"

ARXIV_ID_PATTERN = re.compile(r'\b(\d{4}\.\d{4,5})\b')


def refresh_known_ids() -> int:
    """Regenerate known_arxiv_ids.txt from all 5 sources."""
    all_ids = set()

    # 1. references.bib
    bib_path = SURVEY_DIR / "latex-v3" / "references.bib"
    if bib_path.exists():
        text = bib_path.read_text(errors='ignore')
        all_ids.update(ARXIV_ID_PATTERN.findall(text))

    # 2. opd-new-papers.md (contains BOTH confirmed and rejected — all are "known")
    opd_new = SURVEY_DIR / "papers-meta" / "opd-new-papers.md"
    if opd_new.exists():
        text = opd_new.read_text(errors='ignore')
        all_ids.update(ARXIV_ID_PATTERN.findall(text))

    # 3. paper_notes.json (DB keys)
    db_path = SURVEY_DIR / "notes" / "paper_notes.json"
    if db_path.exists():
        with open(db_path) as f:
            db = json.load(f)
        notes = db.get("notes", db)
        for key in notes:
            if ARXIV_ID_PATTERN.match(key):
                all_ids.add(key)

    # 4. excluded-papers.md (rejected papers must stay in known to prevent re-scouting)
    excluded = SURVEY_DIR / "papers-meta" / "excluded-papers.md"
    if excluded.exists():
        text = excluded.read_text(errors='ignore')
        all_ids.update(ARXIV_ID_PATTERN.findall(text))

    # 5. Awesome List README
    readme = SURVEY_DIR / "Awesome-LLM-On-Policy-Distillation" / "README.md"
    if readme.exists():
        text = readme.read_text(errors='ignore')
        all_ids.update(ARXIV_ID_PATTERN.findall(text))

    # Write sorted
    sorted_ids = sorted(all_ids)
    KNOWN_IDS_FILE.write_text("\n".join(sorted_ids) + "\n")
    print(f"✅ Refreshed known_arxiv_ids.txt: {len(sorted_ids)} IDs")
    return len(sorted_ids)


def check_weekend() -> bool:
    """
    Check if today is a weekend (no new arXiv submissions expected).
    
    arXiv submission schedule (UTC):
    - Mon 14:00 → Tue papers (submitted Thu 14:00 - Mon 14:00)
    - Tue 14:00 → Wed papers
    - Wed 14:00 → Thu papers
    - Thu 14:00 → Fri papers
    - Fri 14:00 → Mon papers (submitted Thu 14:00 - Fri 14:00)
    
    So: Saturday and Sunday have NO new listings.
    Monday before 14:00 UTC also has no new listings (Friday's batch).
    
    Our scout runs at 02:40 CST = 18:40 UTC (previous day's papers).
    - Saturday 18:40 UTC: Friday's papers already out → worth scanning
    - Sunday 18:40 UTC: No new papers since Friday → SKIP
    - Monday 02:40 CST = Sunday 18:40 UTC: Still no new papers → SKIP
    
    Wait, let me reconsider for CST (UTC+8):
    - Scout runs 02:40 CST daily
    - Saturday 02:40 CST = Friday 18:40 UTC → Friday papers just posted → SCAN
    - Sunday 02:40 CST = Saturday 18:40 UTC → No new papers → SKIP
    - Monday 02:40 CST = Sunday 18:40 UTC → No new papers (Mon batch not out until Mon 14:00 UTC = Mon 22:00 CST) → SKIP
    
    Actually the retry runs at 06:40 CST on failure, and Monday's papers appear Mon 20:00 UTC = Tue 04:00 CST.
    So Monday scout at 02:40 CST still has no new papers. The retry at 06:40 CST on Tuesday would catch them.
    
    Conclusion: Skip on Sunday and Monday (CST).
    """
    # Use CST (UTC+8) since that's when the cron runs
    now_utc = datetime.now(timezone.utc)
    cst = timezone(timedelta(hours=8))
    now_cst = now_utc.astimezone(cst)
    
    weekday = now_cst.weekday()  # 0=Monday, 6=Sunday
    
    # Sunday (6) or Monday (0) in CST = no new arXiv papers available
    if weekday in (0, 6):  # Monday or Sunday
        print(f"📅 Today is {now_cst.strftime('%A')} (CST). No new arXiv submissions expected.")
        print("   Recommending: SKIP full scan, only check retry queue.")
        return True
    
    return False


def main():
    parser = argparse.ArgumentParser(description="OPD Scout Pre-Check")
    parser.add_argument("--refresh-ids", action="store_true", help="Refresh known IDs file")
    parser.add_argument("--check-weekend", action="store_true", help="Check weekend skip")
    parser.add_argument("--both", action="store_true", help="Do both checks")
    args = parser.parse_args()

    if args.both or (args.refresh_ids and args.check_weekend):
        refresh_known_ids()
        if check_weekend():
            sys.exit(1)  # Signal: skip
        sys.exit(0)  # Signal: proceed

    if args.refresh_ids:
        refresh_known_ids()
        sys.exit(0)

    if args.check_weekend:
        if check_weekend():
            sys.exit(1)
        print("✅ Weekday — proceed with full scan.")
        sys.exit(0)

    # Default: do both
    refresh_known_ids()
    if check_weekend():
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
