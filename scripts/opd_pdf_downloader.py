#!/usr/bin/env python3
"""
OPD PDF Downloader
==================
Download PDFs for all OPD-related papers in paper_kb to CephFS storage.

Supports:
- arXiv papers: https://arxiv.org/pdf/{id}.pdf
- Blog posts (blog:*): fetch HTML and save as markdown
- Tech reports (report:*): download from metadata.source_url

Usage:
    python3 opd_pdf_downloader.py --all          # Download all OPD papers
    python3 opd_pdf_downloader.py --missing       # Only download missing ones
    python3 opd_pdf_downloader.py --ids 2604.13010 2604.16830
    python3 opd_pdf_downloader.py --awesome-list /path/to/README.md
"""
import argparse
import json
import logging
import os
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import List, Optional, Set, Tuple

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# Configuration
DEFAULT_DB_PATH = os.path.expanduser("~/clawd/db/paper_kb.db")
PDF_ROOT = "/apdcephfs_cq8/share_1324356/nickmysong/openclaw_fsp/papers/opd/"
ARXIV_DELAY = 1.0  # seconds between arXiv requests
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def get_db_connection(db_path: str = None) -> sqlite3.Connection:
    """Get a connection to paper_kb database."""
    conn = sqlite3.connect(db_path or DEFAULT_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_opd_papers(conn: sqlite3.Connection) -> List[dict]:
    """Query all OPD-related papers from paper_kb."""
    rows = conn.execute("""
        SELECT arxiv_id, title, pdf_path, pdf_downloaded, metadata, topics
        FROM papers
        WHERE topics LIKE '%on-policy%'
           OR topics LIKE '%distill%'
           OR topics LIKE '%on_policy%'
           OR title LIKE '%on-policy distill%'
           OR title LIKE '%on policy distill%'
        ORDER BY arxiv_id
    """).fetchall()
    return [dict(r) for r in rows]


def get_papers_by_ids(conn: sqlite3.Connection, ids: List[str]) -> List[dict]:
    """Get specific papers by their IDs."""
    placeholders = ",".join(["?"] * len(ids))
    rows = conn.execute(f"""
        SELECT arxiv_id, title, pdf_path, pdf_downloaded, metadata, topics
        FROM papers
        WHERE arxiv_id IN ({placeholders})
    """, ids).fetchall()
    return [dict(r) for r in rows]


def extract_ids_from_awesome_list(filepath: str) -> Set[str]:
    """Extract arXiv IDs from an Awesome List README.md."""
    ids = set()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match arXiv IDs in various formats:
    # - https://arxiv.org/abs/2604.13010
    # - https://arxiv.org/pdf/2604.13010
    # - arxiv:2604.13010
    # - [2604.13010]
    patterns = [
        r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})',
        r'arxiv:(\d{4}\.\d{4,5})',
        r'\[(\d{4}\.\d{4,5})\]',
    ]
    for pat in patterns:
        for match in re.finditer(pat, content):
            ids.add(match.group(1))

    logger.info(f"Extracted {len(ids)} arXiv IDs from awesome list")
    return ids


def pdf_path_for(arxiv_id: str) -> str:
    """Compute the PDF storage path for a given ID."""
    # For blog/report types, use .md extension
    if arxiv_id.startswith("blog:"):
        safe_name = arxiv_id.replace(":", "_").replace("/", "_")
        return os.path.join(PDF_ROOT, f"{safe_name}.md")
    elif arxiv_id.startswith("report:"):
        safe_name = arxiv_id.replace(":", "_").replace("/", "_")
        return os.path.join(PDF_ROOT, f"{safe_name}.pdf")
    else:
        return os.path.join(PDF_ROOT, f"{arxiv_id}.pdf")


def download_arxiv_pdf(arxiv_id: str, dest: str) -> bool:
    """Download a PDF from arXiv."""
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    logger.info(f"Downloading arXiv PDF: {arxiv_id} -> {dest}")

    try:
        resp = requests.get(
            url,
            timeout=120,
            stream=True,
            headers={"User-Agent": USER_AGENT},
        )
        resp.raise_for_status()

        # Verify it's actually a PDF
        content_type = resp.headers.get("Content-Type", "")
        if "pdf" not in content_type and "octet-stream" not in content_type:
            # Check first bytes
            first_chunk = next(resp.iter_content(chunk_size=16))
            if not first_chunk.startswith(b"%PDF"):
                logger.error(f"  Not a PDF: {arxiv_id} (Content-Type: {content_type})")
                return False
            # Write first chunk and continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            tmp = dest + ".tmp"
            with open(tmp, "wb") as f:
                f.write(first_chunk)
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            os.rename(tmp, dest)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            tmp = dest + ".tmp"
            with open(tmp, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            os.rename(tmp, dest)

        size_mb = os.path.getsize(dest) / (1024 * 1024)
        logger.info(f"  Downloaded: {dest} ({size_mb:.1f} MB)")
        return True

    except requests.exceptions.HTTPError as e:
        logger.error(f"  HTTP error for {arxiv_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"  Download failed for {arxiv_id}: {e}")
        # Clean up temp file
        tmp = dest + ".tmp"
        if os.path.exists(tmp):
            os.remove(tmp)
        return False


def download_blog_as_markdown(arxiv_id: str, source_url: str, dest: str) -> bool:
    """Fetch a blog post URL and save as markdown."""
    if not source_url:
        logger.warning(f"  No source_url for blog: {arxiv_id}")
        return False

    logger.info(f"Fetching blog: {arxiv_id} from {source_url}")

    try:
        resp = requests.get(
            source_url,
            timeout=60,
            headers={"User-Agent": USER_AGENT},
        )
        resp.raise_for_status()

        if HAS_BS4:
            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove scripts, styles, nav, footer
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            # Try to find main content
            main = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"content|post|article"))
            if main:
                text = main.get_text(separator="\n", strip=True)
            else:
                text = soup.get_text(separator="\n", strip=True)
        else:
            # Fallback: strip HTML tags with regex
            text = re.sub(r'<[^>]+>', '', resp.text)
            text = re.sub(r'\n{3,}', '\n\n', text)

        # Save as markdown
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        header = f"# Source: {source_url}\n# ID: {arxiv_id}\n# Fetched: {time.strftime('%Y-%m-%d')}\n\n"
        with open(dest, "w", encoding="utf-8") as f:
            f.write(header + text)

        logger.info(f"  Saved blog as markdown: {dest} ({len(text)} chars)")
        return True

    except Exception as e:
        logger.error(f"  Blog fetch failed for {arxiv_id}: {e}")
        return False


def download_report_pdf(arxiv_id: str, source_url: str, dest: str) -> bool:
    """Download a tech report PDF from its source URL."""
    if not source_url:
        logger.warning(f"  No source_url for report: {arxiv_id}")
        return False

    logger.info(f"Downloading report PDF: {arxiv_id} from {source_url}")

    try:
        resp = requests.get(
            source_url,
            timeout=120,
            stream=True,
            headers={"User-Agent": USER_AGENT},
        )
        resp.raise_for_status()

        os.makedirs(os.path.dirname(dest), exist_ok=True)
        tmp = dest + ".tmp"
        with open(tmp, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        os.rename(tmp, dest)

        size_mb = os.path.getsize(dest) / (1024 * 1024)
        logger.info(f"  Downloaded report: {dest} ({size_mb:.1f} MB)")
        return True

    except Exception as e:
        logger.error(f"  Report download failed for {arxiv_id}: {e}")
        tmp = dest + ".tmp"
        if os.path.exists(tmp):
            os.remove(tmp)
        return False


def update_paper_kb(conn: sqlite3.Connection, arxiv_id: str, pdf_path: str):
    """Mark a paper as downloaded in paper_kb."""
    conn.execute("""
        UPDATE papers
        SET pdf_path = ?, pdf_downloaded = 1, updated_at = CURRENT_TIMESTAMP
        WHERE arxiv_id = ?
    """, (pdf_path, arxiv_id))
    conn.commit()


def get_source_url_from_metadata(metadata_str: str) -> str:
    """Extract source_url from metadata JSON string."""
    if not metadata_str:
        return ""
    try:
        meta = json.loads(metadata_str)
        return meta.get("source_url", "")
    except (json.JSONDecodeError, TypeError):
        return ""


def download_paper(conn: sqlite3.Connection, paper: dict, force: bool = False) -> Tuple[bool, str]:
    """Download a single paper. Returns (success, message)."""
    arxiv_id = paper["arxiv_id"]
    dest = pdf_path_for(arxiv_id)

    # Check if already downloaded (skip unless forced)
    if not force:
        if paper.get("pdf_downloaded") and os.path.exists(dest):
            return True, f"Already exists: {arxiv_id}"
        # Also check if the file exists on disk even if DB doesn't reflect it
        if os.path.exists(dest):
            update_paper_kb(conn, arxiv_id, dest)
            return True, f"Found on disk, updated DB: {arxiv_id}"

    success = False

    if arxiv_id.startswith("blog:"):
        source_url = get_source_url_from_metadata(paper.get("metadata", ""))
        success = download_blog_as_markdown(arxiv_id, source_url, dest)
        if success:
            time.sleep(2)  # Be polite to blog servers

    elif arxiv_id.startswith("report:"):
        source_url = get_source_url_from_metadata(paper.get("metadata", ""))
        success = download_report_pdf(arxiv_id, source_url, dest)
        if success:
            time.sleep(2)

    else:
        # Standard arXiv paper
        success = download_arxiv_pdf(arxiv_id, dest)
        if success:
            time.sleep(ARXIV_DELAY)  # Rate limit: max 1 req/sec for arXiv

    if success:
        update_paper_kb(conn, arxiv_id, dest)
        return True, f"Downloaded: {arxiv_id}"
    else:
        return False, f"Failed: {arxiv_id}"


def main():
    parser = argparse.ArgumentParser(description="OPD PDF Downloader")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Download all OPD papers")
    group.add_argument("--missing", action="store_true", help="Download only missing papers")
    group.add_argument("--ids", nargs="+", help="Download specific paper IDs")
    group.add_argument("--awesome-list", type=str, help="Extract IDs from Awesome List and download")
    parser.add_argument("--force", action="store_true", help="Re-download even if already exists")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be downloaded")
    parser.add_argument("--db", default=DEFAULT_DB_PATH, help=f"Database path (default: {DEFAULT_DB_PATH})")
    args = parser.parse_args()

    conn = get_db_connection(args.db)

    # Determine papers to download
    if args.all:
        papers = get_opd_papers(conn)
        logger.info(f"Found {len(papers)} OPD papers total")

    elif args.missing:
        papers = get_opd_papers(conn)
        papers = [p for p in papers if not p.get("pdf_downloaded") or not os.path.exists(pdf_path_for(p["arxiv_id"]))]
        logger.info(f"Found {len(papers)} papers with missing PDFs")

    elif args.ids:
        papers = get_papers_by_ids(conn, args.ids)
        # Also handle IDs not yet in paper_kb
        found_ids = {p["arxiv_id"] for p in papers}
        missing_ids = [i for i in args.ids if i not in found_ids]
        if missing_ids:
            # Create stub entries for papers not in DB
            for mid in missing_ids:
                papers.append({
                    "arxiv_id": mid,
                    "title": "",
                    "pdf_path": "",
                    "pdf_downloaded": 0,
                    "metadata": "",
                    "topics": "",
                })
        logger.info(f"Will download {len(papers)} specified papers")

    elif args.awesome_list:
        ids = extract_ids_from_awesome_list(args.awesome_list)
        if not ids:
            logger.error("No IDs found in awesome list")
            conn.close()
            sys.exit(1)
        papers = get_papers_by_ids(conn, list(ids))
        # Also add IDs not in DB
        found_ids = {p["arxiv_id"] for p in papers}
        for aid in ids:
            if aid not in found_ids:
                papers.append({
                    "arxiv_id": aid,
                    "title": "",
                    "pdf_path": "",
                    "pdf_downloaded": 0,
                    "metadata": "",
                    "topics": "",
                })
        logger.info(f"Will download {len(papers)} papers from awesome list")

    if args.dry_run:
        print(f"\n=== DRY RUN: Would download {len(papers)} papers ===")
        for p in papers:
            dest = pdf_path_for(p["arxiv_id"])
            exists = "✓" if os.path.exists(dest) else "✗"
            print(f"  [{exists}] {p['arxiv_id']}: {p.get('title', '(no title)')[:60]}")
        conn.close()
        return

    # Download papers
    stats = {"total": len(papers), "downloaded": 0, "skipped": 0, "failed": 0}

    for i, paper in enumerate(papers, 1):
        logger.info(f"[{i}/{stats['total']}] Processing {paper['arxiv_id']}")
        success, msg = download_paper(conn, paper, force=args.force)
        if success:
            if "Already" in msg or "Found on disk" in msg:
                stats["skipped"] += 1
            else:
                stats["downloaded"] += 1
        else:
            stats["failed"] += 1
        logger.info(f"  {msg}")

    conn.close()

    # Summary
    print(f"\n{'='*50}")
    print(f"OPD PDF Download Summary")
    print(f"{'='*50}")
    print(f"  Total:      {stats['total']}")
    print(f"  Downloaded: {stats['downloaded']}")
    print(f"  Skipped:    {stats['skipped']} (already exist)")
    print(f"  Failed:     {stats['failed']}")
    print(f"  Storage:    {PDF_ROOT}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
