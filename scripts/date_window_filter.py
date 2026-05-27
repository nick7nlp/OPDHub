#!/usr/bin/env python3
"""
DATE WINDOW filter for OPD daily scout — code-level enforcement.

Purpose: 5/19 老大明确, daily scout 只接收"今天 + 昨天"提交的 arXiv 论文.
不能依靠 LLM agent 自觉, 必须代码层强制.

Usage:
    # As library:
    from date_window_filter import is_within_date_window
    assert is_within_date_window('2605.15239')  # accepts iff today is 2026-05 or yesterday was 2026-05
    
    # As CLI filter (stdin → stdout):
    cat candidates.txt | python3 scripts/date_window_filter.py
    # outputs only the IDs within the window
    
    # Validation hook (used by triage / batch_deep_read):
    python3 scripts/date_window_filter.py --check 2502.02671
    # exit 0 if accepted, exit 2 if outside window

Tests:
    python3 scripts/date_window_filter.py --self-test
"""

from __future__ import annotations
import argparse
import re
import sys
from datetime import datetime, timedelta, timezone

ARXIV_ID_RE = re.compile(r'\b(\d{4})\.(\d{4,5})\b')


def get_window_yymms(today: datetime | None = None) -> set[str]:
    """
    Return the set of allowed YYMM prefixes for today's daily scout.
    
    Rules:
    - Today (today.year, today.month) → always allowed
    - Yesterday (today - 1 day) → always allowed
    
    On month boundaries (e.g. today = 2026-06-01, yesterday = 2026-05-31),
    both '2606' and '2605' are allowed.
    """
    if today is None:
        # Use CST (UTC+8) since cron schedule is in CST
        cst = timezone(timedelta(hours=8))
        today = datetime.now(cst)
    
    yesterday = today - timedelta(days=1)
    
    today_yymm = f'{(today.year - 2000) % 100:02d}{today.month:02d}'
    yest_yymm = f'{(yesterday.year - 2000) % 100:02d}{yesterday.month:02d}'
    
    return {today_yymm, yest_yymm}


def parse_arxiv_yymm(arxiv_id: str) -> str | None:
    """Extract YYMM prefix from arxiv_id like '2605.15239'."""
    m = ARXIV_ID_RE.match(arxiv_id.strip())
    if not m:
        return None
    return m.group(1)


def is_within_date_window(arxiv_id: str, today: datetime | None = None) -> bool:
    """
    Check if arxiv_id was submitted today or yesterday.
    
    >>> # Frozen test: today = 2026-05-19
    >>> from datetime import datetime, timezone, timedelta
    >>> cst = timezone(timedelta(hours=8))
    >>> t = datetime(2026, 5, 19, 12, 0, tzinfo=cst)
    >>> is_within_date_window('2605.15239', today=t)
    True
    >>> is_within_date_window('2604.20244', today=t)
    False
    >>> is_within_date_window('2502.02671', today=t)
    False
    """
    yymm = parse_arxiv_yymm(arxiv_id)
    if yymm is None:
        return False
    return yymm in get_window_yymms(today)


def self_test() -> int:
    """Self-test the function with frozen dates."""
    cst = timezone(timedelta(hours=8))
    
    cases = [
        # (today, arxiv_id, expected)
        # Mid-month: only current month allowed
        (datetime(2026, 5, 19, 12, 0, tzinfo=cst), '2605.15239', True),
        (datetime(2026, 5, 19, 12, 0, tzinfo=cst), '2605.11019', True),
        (datetime(2026, 5, 19, 12, 0, tzinfo=cst), '2604.20244', False),
        (datetime(2026, 5, 19, 12, 0, tzinfo=cst), '2502.02671', False),
        (datetime(2026, 5, 19, 12, 0, tzinfo=cst), '2510.02227', False),
        
        # Month boundary: both prev and current month allowed
        (datetime(2026, 6, 1, 12, 0, tzinfo=cst), '2606.00001', True),
        (datetime(2026, 6, 1, 12, 0, tzinfo=cst), '2605.99999', True),
        (datetime(2026, 6, 1, 12, 0, tzinfo=cst), '2604.99999', False),
        
        # Year boundary: both 2025-12 and 2026-01 allowed when today is 2026-01-01
        (datetime(2026, 1, 1, 12, 0, tzinfo=cst), '2601.00001', True),
        (datetime(2026, 1, 1, 12, 0, tzinfo=cst), '2512.99999', True),
        (datetime(2026, 1, 1, 12, 0, tzinfo=cst), '2511.99999', False),
        
        # Within month, day 2: today + yesterday both same yymm
        (datetime(2026, 5, 2, 12, 0, tzinfo=cst), '2605.00001', True),
        (datetime(2026, 5, 2, 12, 0, tzinfo=cst), '2604.99999', False),
        
        # Malformed IDs
        (datetime(2026, 5, 19, 12, 0, tzinfo=cst), 'not-an-id', False),
        (datetime(2026, 5, 19, 12, 0, tzinfo=cst), '', False),
    ]
    
    passed = 0
    failed = 0
    for today, aid, expected in cases:
        actual = is_within_date_window(aid, today=today)
        ok = actual == expected
        status = '✓' if ok else '✗'
        print(f"  {status} today={today.date()} id={aid!r:18} expect={expected} got={actual}")
        if ok:
            passed += 1
        else:
            failed += 1
    
    print(f"\n{passed}/{passed+failed} passed")
    return 0 if failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="DATE WINDOW filter for OPD daily scout")
    parser.add_argument('--check', metavar='ARXIV_ID', help='Check single ID, exit 0 if in window, 2 if outside')
    parser.add_argument('--self-test', action='store_true', help='Run self-tests')
    parser.add_argument('--show-window', action='store_true', help='Print allowed YYMM prefixes for today')
    args = parser.parse_args()
    
    if args.self_test:
        sys.exit(self_test())
    
    if args.show_window:
        window = sorted(get_window_yymms())
        print(f"Today (CST): {datetime.now(timezone(timedelta(hours=8))).date()}")
        print(f"Allowed YYMM prefixes: {window}")
        sys.exit(0)
    
    if args.check:
        if is_within_date_window(args.check):
            print(f"✓ {args.check}: within window {sorted(get_window_yymms())}")
            sys.exit(0)
        else:
            print(f"✗ {args.check}: OUTSIDE window {sorted(get_window_yymms())}")
            sys.exit(2)
    
    # Default: filter stdin
    window = get_window_yymms()
    accepted = 0
    rejected = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if is_within_date_window(line):
            print(line)
            accepted += 1
        else:
            print(f"  REJECT (outside window): {line}", file=sys.stderr)
            rejected += 1
    print(f"  Window: {sorted(window)}, accepted={accepted}, rejected={rejected}", file=sys.stderr)


if __name__ == '__main__':
    main()
