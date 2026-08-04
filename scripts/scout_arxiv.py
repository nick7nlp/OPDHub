#!/usr/bin/env python3
"""
OPD Daily Scout v3 — RSS-first + API verify + S2 cross-check.

Architecture (2026-05-29 重写):
  PRIMARY:  RSS feeds (rss.arxiv.org/rss/cs.{CL,LG,AI}) — no rate limit, has abstracts
  VERIFY:   arXiv id_list endpoint (usually not rate-limited even when search is)
  CROSS:    Semantic Scholar (recovers papers RSS missed)

Why: This machine's IP is persistently rate-limited by both arXiv search API and S2.
RSS feeds are immune to rate limiting and return all today's new papers.

5/19 纪律: scout 必须代码层强制 DATE WINDOW.
5/29 改造: urllib scout → RSS-primary + requests + S2 cross-check (openclaw 方法).

Usage:
    python3 scripts/scout_arxiv.py --download
    python3 scripts/scout_arxiv.py --dry-run
    python3 scripts/scout_arxiv.py --max 30
"""

from __future__ import annotations
import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests

SURVEY_ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
KNOWN_IDS = SURVEY_ROOT / "papers-meta" / "known_arxiv_ids.txt"
PDF_ROOT = SURVEY_ROOT / "pdfs"
STAGING = SURVEY_ROOT / "pdfs" / "_staging"

sys.path.insert(0, str(SURVEY_ROOT / "scripts"))
try:
    from date_window_filter import is_within_date_window, get_window_yymms
except ImportError:
    print("[scout] FATAL: date_window_filter.py not found", file=sys.stderr)
    sys.exit(2)

# ============================================================================
# Config
# ============================================================================

RSS_CATEGORIES = ["cs.CL", "cs.LG", "cs.AI"]

# Loose keyword filter for RSS (intentionally broad — deep-read decides)
OPD_KEYWORDS = [
    "distill", "on-policy", "on policy", "self-play",
    "student", "teacher", "knowledge transfer", "rollout",
    "imitation", "gkd", "reverse kl", "self-distillation",
    "online distillation", "interactive distillation",
]

# Title-level reject keywords (proven reliable from cron runs)
REJECT_TITLE_KEYWORDS = [
    "image segmentation", "object detection", "point cloud", "gaussian splatting",
    "video prediction", "image clustering", "face", "human mesh", "ultrasound",
    "pathology", "endoscopy", "dental", "gastro", "medical image",
    "molecular", "time series", "pde", "weather", "reactor",
    "recommendation", "kubernetes", "click-through",
    "speaker", "speech", "audio",
    "speculative decoding",
]

# S2 queries (less restrictive for cross-check)
S2_QUERY_TERMS = [
    "on-policy distillation language model",
    "online knowledge distillation LLM",
    "self-distillation language model 2026",
    "reverse KL distillation student rollout",
]

ARXIV_API = "https://export.arxiv.org/api/query"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = "title,authors,year,abstract,externalIds,publicationDate"

MAX_RETRIES = 1  # S2/API often fully blocked; don't waste time
BACKOFF_BASE = 5  # seconds


def cst_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=8)))


def build_window_dates() -> tuple[str, str, str, str]:
    """Return (yest_str, today_end_str, yest_human, today_human)."""
    now_cst = cst_now()
    yesterday = now_cst - timedelta(days=1)
    yest_str = (yesterday.astimezone(timezone.utc).strftime("%Y%m%d")) + "0000"
    today_end_str = (now_cst.astimezone(timezone.utc).strftime("%Y%m%d")) + "2359"
    return yest_str, today_end_str, yesterday.strftime("%Y-%m-%d"), now_cst.strftime("%Y-%m-%d")


def _create_session() -> requests.Session:
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": "OPD-DailyScout/3.0 (academic research tool; RSS-primary)",
    })
    return sess


# ============================================================================
# RSS Feed Search (PRIMARY — no rate limit)
# ============================================================================

def search_rss(session: requests.Session) -> list[dict]:
    """Fetch today's papers from arXiv RSS feeds. Never rate-limited."""
    all_items: list[dict] = []

    for cat in RSS_CATEGORIES:
        url = f"https://rss.arxiv.org/rss/{cat}"
        try:
            resp = session.get(url, timeout=30)
            if resp.status_code != 200:
                print(f"[scout/rss] HTTP {resp.status_code} for {cat}", file=sys.stderr)
                continue

            data = resp.text
            items = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)
            cat_count = 0

            for item in items:
                # Filter out replace/replace-cross (stale re-announces)
                ann_m = re.search(r'<arxiv:announce_type>(.*?)</arxiv:announce_type>', item)
                ann_type = ann_m.group(1) if ann_m else "new"
                if ann_type.startswith("replace"):
                    continue

                # Keyword match (loose)
                lower = item.lower()
                if not any(kw in lower for kw in OPD_KEYWORDS):
                    continue

                # Title-level reject
                title_m = re.search(r'<title>(.*?)</title>', item)
                title = title_m.group(1).strip() if title_m else ""
                title_lower = title.lower()
                if any(rk in title_lower for rk in REJECT_TITLE_KEYWORDS):
                    continue

                # Extract ID
                link_m = re.search(r'<link>(.*?)</link>', item)
                if not link_m:
                    continue
                link = link_m.group(1).strip()
                id_m = re.search(r'/abs/(\d{4}\.\d{4,5})', link)
                if not id_m:
                    continue
                aid = id_m.group(1)

                # Extract abstract from <description>
                desc_m = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
                abstract = ""
                if desc_m:
                    abstract = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip()
                    # Often starts with "Abstract: " prefix from arXiv
                    abstract = re.sub(r'^Abstract:\s*', '', abstract, flags=re.IGNORECASE)
                    abstract = abstract[:500]

                all_items.append({
                    "arxiv_id": aid,
                    "title": re.sub(r'\s+', ' ', title).strip(),
                    "abstract": abstract,
                    "published": "",  # Will verify via API
                    "pdf_url": f"https://arxiv.org/pdf/{aid}.pdf",
                    "matched_query": f"rss/{cat}",
                    "source": "rss",
                    "announce_type": ann_type,
                })
                cat_count += 1

            print(f"[scout/rss] {cat}: {len(items)} total items, {cat_count} OPD-keyword matches",
                  flush=True)

        except Exception as e:
            print(f"[scout/rss] error fetching {cat}: {e}", file=sys.stderr)

    # Deduplicate by arxiv_id (cross-listed papers appear in multiple categories)
    seen: set[str] = set()
    deduped: list[dict] = []
    for item in all_items:
        if item["arxiv_id"] not in seen:
            seen.add(item["arxiv_id"])
            deduped.append(item)
        else:
            # Merge matched_query
            for d in deduped:
                if d["arxiv_id"] == item["arxiv_id"]:
                    d["matched_query"] += f"; {item['matched_query']}"
                    break
    return deduped


# ============================================================================
# arXiv id_list verify (usually works even when search is blocked)
# ============================================================================

def verify_date_via_api(session: requests.Session, aid: str) -> Optional[str]:
    """Use arXiv id_list endpoint to get v1 published date. Returns ISO date or None."""
    url = f"{ARXIV_API}?id_list={aid}"
    try:
        resp = session.get(url, timeout=20)
        if resp.status_code == 429:
            time.sleep(3)
            resp = session.get(url, timeout=20)
        if resp.status_code != 200:
            return None
        m = re.search(r'<published>(.*?)</published>', resp.text)
        return m.group(1) if m else None
    except Exception:
        return None


# ============================================================================
# Semantic Scholar cross-check
# ============================================================================

def search_s2(session: requests.Session, query: str, year_range: str = "", limit: int = 20) -> list[dict]:
    """Search S2 with retry. Returns papers with arXiv IDs only."""
    params = {"query": query, "limit": min(limit, 100), "fields": S2_FIELDS}
    if year_range:
        params["year"] = year_range

    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = session.get(S2_API, params=params, timeout=20)
            if resp.status_code == 429:
                wait = BACKOFF_BASE * (2 ** attempt)
                if attempt < MAX_RETRIES:
                    print(f"[scout/s2] 429, retry in {wait}s...", file=sys.stderr, flush=True)
                    time.sleep(wait)
                    continue
                return []
            if resp.status_code != 200:
                return []

            results = []
            for item in resp.json().get("data", []):
                ext_ids = item.get("externalIds", {}) or {}
                arxiv_id = ext_ids.get("ArXiv", "") or ""
                if not arxiv_id:
                    continue
                results.append({
                    "arxiv_id": arxiv_id,
                    "title": item.get("title", ""),
                    "abstract": (item.get("abstract", "") or "")[:500],
                    "published": item.get("publicationDate", "") or "",
                    "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                    "matched_query": f"s2:{query[:40]}",
                    "source": "semantic_scholar",
                })
            return results
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF_BASE * (2 ** attempt))
            else:
                return []
        except Exception as e:
            print(f"[scout/s2] error: {e}", file=sys.stderr)
            return []
    return []


# ============================================================================
# PDF download
# ============================================================================

def download_pdf(session: requests.Session, url: str, dest: Path, timeout: int = 60) -> bool:
    """Download PDF; return True on success."""
    try:
        resp = session.get(url, timeout=timeout, stream=True)
        if resp.status_code != 200:
            return False
        data = resp.content
        if len(data) < 10000:
            return False
        if not data.startswith(b"%PDF"):
            return False
        dest.write_bytes(data)
        return True
    except Exception as e:
        print(f"[scout] download fail {url}: {e}", file=sys.stderr)
        return False


# ============================================================================
# Utilities
# ============================================================================

def load_known() -> set[str]:
    if not KNOWN_IDS.exists():
        return set()
    return set(KNOWN_IDS.read_text().split())


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(description="OPD Daily Scout v3 — RSS-first")
    ap.add_argument("--download", action="store_true", help="Download PDFs to monthly dirs (pdfs/YYYY-MM/)")
    ap.add_argument("--dry-run", action="store_true", help="No download")
    ap.add_argument("--max", type=int, default=30, help="Max candidates total")
    ap.add_argument("--output", default="/tmp/scout_arxiv_results.json")
    ap.add_argument("--skip-s2", action="store_true", help="Skip Semantic Scholar cross-check")
    ap.add_argument("--skip-verify", action="store_true", help="Skip date verification via API")
    ap.add_argument("--days-back", type=int, default=1,
                    help="Date window: how many days before today to accept (default 1 = today + yesterday). "
                         "Use --days-back 5 for catch-up after pipeline gaps.")
    args = ap.parse_args()

    yest_str, today_end_str, yest_h, today_h = build_window_dates()
    window_yymms = get_window_yymms(days_back=args.days_back)
    now_cst = cst_now()
    s2_year_range = f"{now_cst.year - 1}-{now_cst.year}"

    print(f"[scout] DATE WINDOW (CST): {yest_h} → {today_h}  (days_back={args.days_back})", flush=True)
    print(f"[scout] accepting YYMM prefixes: {sorted(window_yymms)}", flush=True)
    print(f"[scout] architecture: RSS-primary + API-verify + S2-crosscheck", flush=True)

    known = load_known()
    print(f"[scout] known IDs to skip: {len(known)}", flush=True)

    session = _create_session()
    all_results: dict[str, dict] = {}  # aid → result

    # === Phase 1: RSS feeds (PRIMARY) ===
    print(f"\n[scout] === Phase 1: RSS feeds ({len(RSS_CATEGORIES)} categories) ===", flush=True)
    rss_results = search_rss(session)
    for r in rss_results:
        all_results[r["arxiv_id"]] = r
    print(f"[scout/rss] total unique candidates: {len(rss_results)}", flush=True)

    # === Phase 2: S2 cross-check (catches papers RSS might miss) ===
    s2_added = 0
    if not args.skip_s2:
        print(f"\n[scout] === Phase 2: S2 cross-check ({len(S2_QUERY_TERMS)} queries) ===", flush=True)
        for i, q in enumerate(S2_QUERY_TERMS):
            results = search_s2(session, q, year_range=s2_year_range, limit=15)
            for r in results:
                if r["arxiv_id"] not in all_results:
                    all_results[r["arxiv_id"]] = r
                    s2_added += 1
            if i < len(S2_QUERY_TERMS) - 1:
                time.sleep(2)
        print(f"[scout/s2] added {s2_added} papers not found in RSS", flush=True)
    else:
        print(f"\n[scout] === Phase 2: S2 cross-check SKIPPED ===", flush=True)

    print(f"\n[scout] combined unique: {len(all_results)} (RSS: {len(rss_results)}, S2-extra: {s2_added})",
          flush=True)

    # === DATE WINDOW filter ===
    # RSS-sourced candidates are already guaranteed fresh by announce_type=new/cross
    # (stale replace/replace-cross re-announces are dropped in search_rss()). Applying
    # the YYMM-prefix window on top of that is redundant AND actively harmful at month
    # boundaries: arXiv IDs reflect submission month, not announcement date, so a paper
    # submitted late last month but announced in the first day(s) of this month still
    # carries last month's prefix. With days_back=1, "yesterday" is also already in the
    # new month by day 2, so 100% of that day's genuinely-new RSS candidates get rejected.
    # Confirmed recurring: 2026-07-02 (63 rejected, 0 kept) and 2026-08-04 (45 rejected,
    # 0 kept) both hit this. RSS's own freshness guarantee is the correct signal here —
    # only S2-sourced candidates (which don't carry that guarantee) need the YYMM check.
    in_window = []
    rejected_dw = []
    for aid, r in all_results.items():
        if r.get("source") != "semantic_scholar" or is_within_date_window(aid, days_back=args.days_back):
            in_window.append(r)
        else:
            rejected_dw.append(aid)

    if rejected_dw:
        print(f"[scout] ⚠️ {len(rejected_dw)} rejected by DATE WINDOW: {rejected_dw[:10]}", flush=True)

    # === Dedup against known ===
    new_candidates = [r for r in in_window if r["arxiv_id"] not in known]
    skipped_known = [r["arxiv_id"] for r in in_window if r["arxiv_id"] in known]
    if skipped_known:
        print(f"[scout] {len(skipped_known)} skipped (already known)", flush=True)

    # === Phase 3: Date verification via API (only for S2-sourced papers) ===
    # RSS announce_type=new/cross + YYMM prefix already guarantees today's papers.
    # Only S2-sourced papers need API verification (they might be older).
    s2_candidates = [c for c in new_candidates if c.get("source") == "semantic_scholar"]
    rss_candidates = [c for c in new_candidates if c.get("source") != "semantic_scholar"]

    if not args.skip_verify and s2_candidates:
        print(f"\n[scout] === Phase 3: verifying {len(s2_candidates)} S2-sourced candidates via id_list API ===",
              flush=True)
        cst = timezone(timedelta(hours=8))
        window_start = (now_cst - timedelta(days=2)).date()
        verified_s2 = []
        for c in s2_candidates:
            pub_iso = verify_date_via_api(session, c["arxiv_id"])
            if pub_iso:
                try:
                    pub_date = datetime.fromisoformat(pub_iso.replace("Z", "+00:00")).astimezone(cst).date()
                    c["published"] = pub_iso
                    if pub_date >= window_start:
                        verified_s2.append(c)
                    else:
                        print(f"[scout/verify] {c['arxiv_id']} rejected: published {pub_date} < window {window_start}",
                              flush=True)
                except (ValueError, TypeError):
                    verified_s2.append(c)
            else:
                verified_s2.append(c)  # API unresponsive, trust YYMM filter
            time.sleep(1)
        print(f"[scout/verify] {len(verified_s2)}/{len(s2_candidates)} S2 papers passed", flush=True)
        new_candidates = rss_candidates + verified_s2
    else:
        if s2_candidates and args.skip_verify:
            print(f"\n[scout] === Phase 3: SKIPPED (--skip-verify) ===", flush=True)
        elif not s2_candidates:
            print(f"\n[scout] === Phase 3: no S2-sourced papers to verify ===", flush=True)

    # Limit
    new_candidates = new_candidates[:args.max]
    print(f"\n[scout] ✅ {len(new_candidates)} new candidates for deep-read", flush=True)

    # === Download PDFs ===
    if args.download and not args.dry_run:
        STAGING.mkdir(parents=True, exist_ok=True)
        for c in new_candidates:
            aid = c["arxiv_id"]
            dest = STAGING / f"{aid}.pdf"
            if dest.exists():
                c["pdf_path"] = str(dest)
                c["downloaded"] = "already-existed"
                continue
            ok = download_pdf(session, c["pdf_url"], dest)
            c["pdf_path"] = str(dest) if ok else None
            c["downloaded"] = "ok" if ok else "fail"
            time.sleep(2)

    # === Output ===
    out = {
        "generated_at": cst_now().isoformat(),
        "date_window_cst": {"from": yest_h, "to": today_h},
        "window_yymms": sorted(window_yymms),
        "architecture": "rss-primary + api-verify + s2-crosscheck",
        "sources": {
            "rss": {"candidates": len(rss_results)},
            "s2": {"extra_added": s2_added},
        },
        "raw_results": len(all_results),
        "rejected_by_date_window": len(rejected_dw),
        "skipped_known": len(skipped_known),
        "new_candidates": new_candidates,
    }
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"[scout] wrote {args.output}", flush=True)

    # Summary for LLM agent
    print()
    print(f"## Scout Summary: {len(new_candidates)} new in-window candidates")
    print()
    if not new_candidates:
        print("(no new OPD-relevant candidates today)")
    else:
        for c in new_candidates:
            status = c.get("downloaded", "not-downloaded")
            src = c.get("source", "?")
            print(f"  - {c['arxiv_id']} [{src}/{status}] {c['title'][:80]}")


if __name__ == "__main__":
    main()
