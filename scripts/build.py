#!/usr/bin/env python3
"""Build OPDHub paper search from the public reading catalog."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


SITE = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = SITE.parent / "Awesome-LLM-On-Policy-Distillation" / "resources" / "catalog.json"
SECTION_LABELS = {
    "4": "Objectives", "5": "Supervision", "6": "Training",
    "7": "Agentic", "8": "Analysis", "9": "Applications",
    "background": "Background",
}
MECHANISM_LABELS = {
    'direct_opd': 'Direct OPD', 'hybrid_opd': 'Mixed / replayed',
    'teacher_mediated_rl': 'Teacher-mediated RL', 'interactive_imitation': 'Interactive imitation',
    'offline_distillation': 'Offline distillation', 'analysis': 'Analysis',
    'application': 'Application', 'background': 'Background',
}
PUBLIC_FIELDS = (
    "paper_id", "title", "authors", "year", "submitted", "paper_url",
    "description", "objective", "mechanism", "home", "code_urls",
    "source_version", "code_status",
)


def validate_date(value: str, field: str, allow_empty: bool = False) -> None:
    """Accept exact ISO dates; never derive dates from an identifier."""
    if allow_empty and value == "":
        return
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{field} must be YYYY-MM-DD")
    date.fromisoformat(value)


def validate_url(value: str, field: str, allow_empty: bool = False) -> None:
    if allow_empty and value == "":
        return
    parsed = urlsplit(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise ValueError(f"{field} must be an HTTP(S) URL")


def load_catalog(path: Path) -> tuple[list[dict], str]:
    """Validate the public schema and retain every row, including background."""
    if not path.is_file():
        raise FileNotFoundError(
            f"Public catalog not found: {path}. Supply --catalog with the real "
            "catalog."
        )
    doc = json.loads(path.read_text(encoding="utf-8"))
    validate_date(doc["updated_on"], "updated_on")
    if not isinstance(doc["papers"], list):
        raise ValueError("papers must be a list")
    records, seen = [], set()
    for row in doc["papers"]:
        missing = set(PUBLIC_FIELDS) - row.keys()
        if missing:
            raise ValueError(f"Missing public fields: {', '.join(sorted(missing))}")
        # Serialize only documented public catalog fields.
        record = {field: row[field] for field in PUBLIC_FIELDS}
        pid = record["paper_id"]
        if not isinstance(pid, str) or not pid or pid in seen:
            raise ValueError(f"Empty or duplicate paper_id: {pid!r}")
        seen.add(pid)
        if record["home"] not in SECTION_LABELS:
            raise ValueError(f"{pid}: unsupported home {record['home']!r}")
        if type(record["year"]) is not int:
            raise ValueError(f"{pid}: year must be an integer")
        for field in ("title", "description", "submitted", "paper_url", "code_status"):
            if not isinstance(record[field], str):
                raise ValueError(f"{pid}: {field} must be a string")
        for field in ("authors", "code_urls"):
            if not isinstance(record[field], list) or not all(
                isinstance(value, str) for value in record[field]
            ):
                raise ValueError(f"{pid}: {field} must be a list of strings")
        for field in ("objective", "mechanism"):
            value = record[field]
            if not isinstance(value, str) and not (
                isinstance(value, list) and all(isinstance(item, str) for item in value)
            ):
                raise ValueError(f"{pid}: {field} must be a string or list of strings")
        if not isinstance(record["source_version"], (str, int)):
            raise ValueError(f"{pid}: source_version must be a string or integer")
        # Software references may only have a public year; do not invent a day.
        if not re.fullmatch(r"\d{4}", record["submitted"]):
            validate_date(record["submitted"], f"{pid}: submitted", allow_empty=True)
        validate_url(record["paper_url"], f"{pid}: paper_url", allow_empty=True)
        for url in record["code_urls"]:
            validate_url(url, f"{pid}: code_urls")
        # Optional public arXiv metadata is independent of the catalog identity.
        if "arxiv_id" in row:
            if row["arxiv_id"] is not None and not isinstance(row["arxiv_id"], str):
                raise ValueError(f"{pid}: arxiv_id must be a string or null")
            record["arxiv_id"] = row["arxiv_id"]
        record["year_month"] = record["submitted"][:7] if len(record["submitted"]) == 10 else ""
        record["bibtex"] = make_bibtex(record)
        records.append(record)
    return records, doc["updated_on"]


def bibtex_text(value: str) -> str:
    """Escape plain catalog text without changing author lists or title casing."""
    substitutions = {
        "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}",
        "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(substitutions.get(char, char) for char in value)


def arxiv_identifier(record: dict) -> str:
    """Identify actual arXiv URLs, including old identifiers and PDF URLs."""
    parsed = urlsplit(record["paper_url"])
    if (parsed.hostname or "").lower() not in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}:
        return ""
    match = re.fullmatch(r"/(?:abs|pdf)/(.+?)(?:\.pdf)?", parsed.path)
    return match.group(1) if match else ""


def make_bibtex(record: dict) -> str:
    """Export only known metadata; @misc also supports software and web sources."""
    key = "opd_" + record["paper_id"].encode("utf-8").hex()
    fields = [f"  title = {{{{{bibtex_text(record['title'])}}}}}"]
    if record["authors"]:
        authors = " and ".join(bibtex_text(author) for author in record["authors"])
        fields.append(f"  author = {{{authors}}}")
    fields.append(f"  year = {{{record['year']}}}")
    if record["paper_url"]:
        fields.append(f"  url = {{{record['paper_url']}}}")
    aid = arxiv_identifier(record)
    if aid:
        fields.extend([f"  eprint = {{{aid}}}", "  archivePrefix = {arXiv}"])
    return "@misc{" + key + ",\n" + ",\n".join(fields) + "\n}"


def field_text(value: str | int | list[str]) -> str:
    return "; ".join(value) if isinstance(value, list) else str(value)


def mechanisms(record: dict) -> list[str]:
    value = record["mechanism"]
    return [item for item in value if item] if isinstance(value, list) else ([value] if value else [])


def html_chip(value: str, label: str, count: int) -> str:
    return (
        f'<button type="button" class="chip" data-value="{escape(value)}" aria-pressed="false">'
        f'{escape(label)}<span class="chip-count">{count}</span></button>'
    )


def html_filter_chips(records: list[dict]) -> dict[str, str]:
    homes = Counter(r["home"] for r in records)
    years = Counter(str(r["year"]) for r in records)
    labels = Counter(value for r in records for value in set(mechanisms(r)))
    return {
        "FILTER_SECTIONS": "\n".join(
            html_chip(home, label, homes[home]) for home, label in SECTION_LABELS.items() if homes[home]
        ),
        "FILTER_MECHANISMS": "\n".join(
            html_chip(value, MECHANISM_LABELS.get(value, value), labels[value])
            for value in sorted(labels, key=str.casefold)
        ),
        "FILTER_YEARS": "\n".join(
            html_chip(year, year, years[year]) for year in sorted(years, reverse=True)
        ),
    }


def render_paper_card(record: dict) -> str:
    source_label = "arXiv" if arxiv_identifier(record) else "Source"
    badges = []
    if record["paper_url"]:
        badges.append(
            f'<a class="badge badge-arxiv" href="{escape(record["paper_url"])}" '
            f'target="_blank" rel="noopener">{source_label}</a>'
        )
    for index, url in enumerate(record["code_urls"]):
        label = "Code" if len(record["code_urls"]) == 1 else f"Code {index + 1}"
        if record["code_status"].startswith("Unofficial"):
            label = "Unofficial code"
        badges.append(
            f'<a class="badge badge-code" href="{escape(url)}" target="_blank" '
            f'rel="noopener" title="{escape(record["code_status"] or "Code")}">'
            f'{label}</a>'
        )
    badges.append(
        '<button type="button" class="badge badge-cite" title="Copy BibTeX to clipboard">'
        '<span class="cite-label">Cite</span></button>'
    )
    author_text = f'<span class="paper-authors">{escape("; ".join(record["authors"]))}</span>'
    if len(record["authors"]) > 5:
        preview = "; ".join(record["authors"][:3])
        author_text = (f'<details class="paper-author-list"><summary>{escape(preview)}; '
                       f'and {len(record["authors"]) - 3} more authors</summary>{author_text}</details>')
    details = [author_text]
    details.append(f'<span class="paper-description">{escape(record["description"])}</span>')
    display_date = record['submitted'] or str(record['year'])
    date_html = f'<span class="paper-date">{escape(display_date)}</span>'
    # Embed exactly the public row so search still works when fetching JSON fails.
    fallback = escape(json.dumps(record, ensure_ascii=False))
    return (
        f'<li class="paper-card" data-paper-id="{escape(record["paper_id"])}" '
        f'data-paper="{fallback}" data-home="{record["home"]}" '
        f'data-year="{record["year"]}" data-bibtex="{escape(record["bibtex"])}">'
        f'<a class="paper-title" href="{escape(record["paper_url"])}" target="_blank" rel="noopener">{escape(record["title"])}</a>'
        f'<div class="paper-meta">{date_html}{"".join(badges)}</div>'
        f'<div class="paper-desc">{"".join(details)}</div></li>'
    )


def html_paper_list(records: list[dict]) -> str:
    parts = []
    for home, label in SECTION_LABELS.items():
        items = [r for r in records if r["home"] == home]
        if not items:
            continue
        items.sort(key=lambda r: (r["submitted"], r["year"], r["paper_id"]), reverse=True)
        parts.append(f'<div class="paper-section-group" data-parent="{home}"><h2>{escape(label)}</h2>')
        parts.append('<ul class="paper-group">')
        parts.extend(render_paper_card(record) for record in items)
        parts.append('</ul></div>')
    return "\n".join(parts)




def build(catalog: Path, site: Path, output: Path) -> int:
    """Write the page and search index only after validating the entire catalog."""
    records, updated_on = load_catalog(catalog)
    payload = {"updated_on": updated_on, "total": len(records), "papers": records}
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    content_hash = hashlib.sha256(serialized.encode("utf-8"))
    for asset in ("static/css/style.css", "static/js/search.js", "static/js/bibtex.js"):
        path = site / asset
        if path.exists():
            content_hash.update(path.read_bytes())
    replacements = {
        **html_filter_chips(records),
        "ASSET_VERSION": content_hash.hexdigest()[:12],
        "PAPER_LIST": html_paper_list(records),
        "PAPER_COUNT": str(len(records)),
    }
    template = (site / "templates" / "index.html.tmpl").read_text(encoding="utf-8")
    # Single-pass substitution keeps literal {{...}} in catalog descriptions intact.
    html = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: replacements[m.group(1)], template)
    output.mkdir(parents=True, exist_ok=True)
    data_dir = output / "static" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(html, encoding="utf-8")
    (data_dir / "papers.json").write_text(serialized, encoding="utf-8")
    print(f"Built {len(records)} catalog entries; updated {updated_on}; output: {output}")
    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help="Path to the real public catalog")
    parser.add_argument("--site-dir", type=Path, default=SITE, help="Site containing templates and static assets")
    parser.add_argument("--output-dir", type=Path, help="Output directory (default: site directory)")
    args = parser.parse_args()
    try:
        build(args.catalog, args.site_dir, args.output_dir or args.site_dir)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Build failed: {exc}\n")


if __name__ == "__main__":
    main()
