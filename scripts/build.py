#!/usr/bin/env python3
"""Build OPDHub from public catalog JSON, without network or private notes."""

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
    "4": "§4 Objectives", "5": "§5 Supervision", "6": "§6 Training",
    "7": "§7 Agentic", "8": "§8 Analysis", "9": "§9 Applications",
    "background": "Background",
}
PUBLIC_FIELDS = (
    "paper_id", "title", "authors", "year", "submitted", "paper_url",
    "description", "objective", "mechanism", "home", "code_urls",
    "source_version", "metadata_checked_on", "code_status",
)
SURVEY_BIBTEX = """@article{song2026opdsurvey,
  title  = {A Survey of On-Policy Distillation for Large Language Models},
  author = {Mingyang Song and Mao Zheng},
  journal= {arXiv preprint arXiv:2604.00626},
  year   = {2026}
}"""


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
            "catalog; legacy notes are not a fallback."
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
        # A whitelist prevents local QA fields from leaking into public output.
        record = {field: row[field] for field in PUBLIC_FIELDS}
        pid = record["paper_id"]
        if not isinstance(pid, str) or not pid or pid in seen:
            raise ValueError(f"Empty or duplicate paper_id: {pid!r}")
        seen.add(pid)
        if record["home"] not in SECTION_LABELS:
            raise ValueError(f"{pid}: unsupported home {record['home']!r}")
        if type(record["year"]) is not int:
            raise ValueError(f"{pid}: year must be an integer")
        for field in ("title", "description", "submitted", "paper_url",
                      "metadata_checked_on", "code_status"):
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
        validate_date(record["metadata_checked_on"], f"{pid}: metadata_checked_on", allow_empty=True)
        validate_url(record["paper_url"], f"{pid}: paper_url", allow_empty=True)
        for url in record["code_urls"]:
            validate_url(url, f"{pid}: code_urls")
        # Optional public arXiv metadata is independent of the catalog identity.
        if "arxiv_id" in row:
            if row["arxiv_id"] is not None and not isinstance(row["arxiv_id"], str):
                raise ValueError(f"{pid}: arxiv_id must be a string or null")
            record["arxiv_id"] = row["arxiv_id"]
        for field in ("code_checked_on", "description_source"):
            if field in row:
                if not isinstance(row[field], str):
                    raise ValueError(f"{pid}: {field} must be a string")
                record[field] = row[field]
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
            html_chip(value, value, labels[value]) for value in sorted(labels, key=str.casefold)
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
    short_home = "Background" if record["home"] == "background" else "§" + record["home"]
    badges.append(f'<span class="badge badge-section">{short_home}</span>')
    for index, url in enumerate(record["code_urls"]):
        label = "Code" if len(record["code_urls"]) == 1 else f"Code {index + 1}"
        if record["code_status"].startswith("Unofficial"):
            label = "Unofficial code"
        badges.append(
            f'<a class="badge badge-code" href="{escape(url)}" target="_blank" '
            f'rel="noopener" title="{escape(record["code_status"] or "Code")}">'
            f'<i class="fas fa-code"></i>&nbsp;{label}</a>'
        )
    badges.append(
        '<button type="button" class="badge badge-cite" title="Copy BibTeX to clipboard">'
        '<i class="fas fa-quote-right"></i>&nbsp;<span class="cite-label">Cite</span></button>'
    )
    author_text = f'<span class="paper-authors">{escape("; ".join(record["authors"]))}</span>'
    if len(record["authors"]) > 12:
        preview = "; ".join(record["authors"][:3])
        author_text = (f'<details class="paper-author-list"><summary>{escape(preview)}; '
                       f'and {len(record["authors"]) - 3} more authors</summary>{author_text}</details>')
    details = [author_text]
    details.append(f'<span class="paper-description">{escape(record["description"])}</span>')
    labels = []
    for field, label in (("objective", "Objective"), ("mechanism", "Mechanism")):
        if record[field]:
            labels.append(f'{label}: {escape(field_text(record[field]))}')
    labels.append(f'Year: {record["year"]}')
    if record["submitted"]:
        if len(record["submitted"]) == 10:
            labels.append(f'Submitted: <time datetime="{record["submitted"]}">{record["submitted"]}</time>')
        else:
            labels.append(f'Source date (year only): {record["submitted"]}')
    if record["source_version"] != "":
        labels.append(f'Source version: {escape(field_text(record["source_version"]))}')
    if record["metadata_checked_on"]:
        labels.append(f'Metadata checked: {record["metadata_checked_on"]}')
    details.append('<span class="paper-provenance">' + " · ".join(labels) + '</span>')
    # Embed exactly the public row so search still works when fetching JSON fails.
    fallback = escape(json.dumps(record, ensure_ascii=False))
    return (
        f'<li class="paper-card" data-paper-id="{escape(record["paper_id"])}" '
        f'data-paper="{fallback}" data-home="{record["home"]}" '
        f'data-year="{record["year"]}" data-bibtex="{escape(record["bibtex"])}">'
        f'<span class="paper-title">{escape(record["title"])}</span>'
        f'<span class="paper-meta" style="flex-wrap:wrap">{"".join(badges)}</span>'
        f'<div class="paper-desc">{"<br>".join(details)}</div></li>'
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


def html_monthly_chart(records: list[dict], updated_on: str, start_ym: str = "2025-01") -> str:
    """SVG line chart of paper count per month, starting at `start_ym`.

    Pre-`start_ym` records are excluded entirely. Zero-count months are
    rendered as on-line points so the time axis is continuous.
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
        f'stroke="#e5e5e5" stroke-width="1"/>'
        f'<line x1="{pad_l}" y1="{y_at(max_n):.1f}" x2="{w-pad_r}" y2="{y_at(max_n):.1f}" '
        f'stroke="#e5e5e5" stroke-width="1" stroke-dasharray="2,3"/>'
    )

    # Y-axis labels (0 and max)
    y_labels = (
        f'<text x="{pad_l-8:.1f}" y="{y_at(0)+4:.1f}" text-anchor="end" '
        f'font-size="11" fill="#aaaaaa" font-family="monospace">0</text>'
        f'<text x="{pad_l-8:.1f}" y="{y_at(max_n)+4:.1f}" text-anchor="end" '
        f'font-size="11" fill="#aaaaaa" font-family="monospace">{max_n}</text>'
    )

    # Data-point circles + non-zero count labels
    circles, value_labels = [], []
    for (x, y), m in zip(pts, months):
        c = counts.get(m, 0)
        circles.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" '
            f'fill="#2563eb" stroke="#fff" stroke-width="1.5"/>'
        )
        if c > 0:
            value_labels.append(
                f'<text x="{x:.1f}" y="{y-10:.1f}" text-anchor="middle" '
                f'font-size="11" fill="#444444" font-family="monospace" '
                f'font-weight="600">{c}</text>'
            )

    # X-axis labels — full YYYY-MM at i==0 and every January, MM otherwise
    x_labels = []
    for i, m in enumerate(months):
        yyyy, mm = m.split("-")
        label = f"{yyyy}-{mm}" if (mm == "01" or i == 0) else mm
        x_labels.append(
            f'<text x="{x_at(i):.1f}" y="{h-12:.1f}" text-anchor="middle" '
            f'font-size="11" fill="#aaaaaa" font-family="monospace">{label}</text>'
        )

    svg = (
        f'<svg class="monthly-chart" viewBox="0 0 {w} {h}" '
        f'xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" '
        f'role="img" aria-label="Catalog entries by submitted month from {start_ym}">'
        + grid
        + f'<path d="{path_area}" fill="#2563eb" fill-opacity="0.08"/>'
        + f'<path d="{path_line}" fill="none" stroke="#2563eb" stroke-width="2" '
        + 'stroke-linejoin="round" stroke-linecap="round"/>'
        + "".join(circles)
        + "".join(value_labels)
        + "".join(x_labels)
        + y_labels
        + '</svg>'
    )
    caption = (
        f'<p class="monthly-chart-caption">'
        f'Catalog entries by submitted month '
        f'<span class="muted">&middot; from {start_ym} &middot; '
        f'{total} entries (including background); snapshot {escape(updated_on)}</span>'
        f'</p>'
    )
    return svg + caption


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
        "MONTHLY_CHART": html_monthly_chart(records, updated_on),
        "BIBTEX": escape(SURVEY_BIBTEX),
        "UPDATED_ON": updated_on,
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
    print(f"Built {len(records)} catalog entries; checked snapshot {updated_on}; output: {output}")
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
