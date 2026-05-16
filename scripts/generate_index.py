#!/usr/bin/env python3
"""
Generate OPD INDEX.md from OPD project's OWN data sources.
NO dependency on paper_kb (which is a general-purpose paper DB).

Sources:
1. latex-v3/references.bib  — what V3 actually cites
2. Awesome-LLM-On-Policy-Distillation/README.md  — public catalog
3. pdfs/  — what we actually have locally
4. papers-meta/opd-new-papers.md  — pending integration tracking
"""
import re
from pathlib import Path

SURVEY = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")

# ---------- 1. V3 references.bib ----------
def parse_v3_bib():
    """Returns: {arxiv_id: {"key": citekey, "title": str, "year": str}}"""
    bib_path = SURVEY / "latex-v3" / "references.bib"
    text = bib_path.read_text()
    entries = {}
    
    # Split by @entries
    for entry_match in re.finditer(r'@\w+\{([^,]+),(.*?)(?=\n@\w+\{|\Z)', text, re.DOTALL):
        key = entry_match.group(1).strip()
        body = entry_match.group(2)
        
        title_m = re.search(r'title\s*=\s*[\{"]+(.*?)[\}"]+(?:,|\n)', body, re.DOTALL)
        title = re.sub(r'\s+', ' ', title_m.group(1)).strip() if title_m else "?"
        # Clean LaTeX
        title = re.sub(r'\{|\}', '', title)
        title = title[:80]
        
        year_m = re.search(r'year\s*=\s*[\{"]?(\d{4})', body)
        year = year_m.group(1) if year_m else "-"
        
        # Find arxiv id
        arxiv_id = None
        # Check if cite key itself is an arxiv id (e.g. @article{2211.09110, ...})
        if re.match(r'^\d{4}\.\d{4,5}$', key.strip()):
            arxiv_id = key.strip()
        else:
            for pat in [r'arxiv\s*=\s*\{?([0-9]{4}\.[0-9]{4,5})',
                        r'arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})',
                        r'arXiv:([0-9]{4}\.[0-9]{4,5})',
                        r'eprint\s*=\s*\{?([0-9]{4}\.[0-9]{4,5})',
                        r'journal\s*=.*?([0-9]{4}\.[0-9]{4,5})']:
                m = re.search(pat, body, re.IGNORECASE)
                if m:
                    arxiv_id = m.group(1)
                    break
        
        if arxiv_id:
            entries[arxiv_id] = {"key": key, "title": title, "year": year}
    
    return entries

# ---------- 2. Awesome List ----------
def parse_awesome():
    """Returns: {arxiv_id: title}"""
    md_path = SURVEY / "Awesome-LLM-On-Policy-Distillation" / "README.md"
    text = md_path.read_text()
    entries = {}
    
    # Pattern: [Title](arxiv.org/abs/XXXX.YYYYY)
    for m in re.finditer(r'\[([^\]]+)\]\(https?://arxiv\.org/abs/(\d{4}\.\d{4,5})\)', text):
        title, aid = m.group(1), m.group(2)
        if aid not in entries:
            entries[aid] = title[:80]
    return entries

# ---------- 3. Local PDFs ----------
def get_local_pdfs():
    """Returns: {arxiv_id: relative_path}"""
    out = {}
    for sub in ["background", "pre-2026", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]:
        d = SURVEY / "pdfs" / sub
        if not d.exists():
            continue
        for f in d.iterdir():
            if f.suffix == ".pdf":
                aid = f.stem
                if re.match(r'^\d{4}\.\d{4,5}$', aid):
                    out[aid] = f"pdfs/{sub}/{f.name}"
    return out

# ---------- 4. Pending integration ----------
def parse_pending():
    """Returns: list of arxiv ids waiting for integration"""
    md_path = SURVEY / "papers-meta" / "opd-new-papers.md"
    if not md_path.exists():
        return set()
    text = md_path.read_text()
    pending = set()
    # Find section "## 当前待集成"
    if "当前待集成" in text:
        start = text.index("当前待集成")
        end_match = re.search(r'\n## ', text[start+10:])
        section = text[start:start+10+end_match.start()] if end_match else text[start:]
        for m in re.finditer(r'\b(\d{4}\.\d{4,5})', section):
            pending.add(m.group(1))
    return pending

# ---------- Main ----------
v3 = parse_v3_bib()
awl = parse_awesome()
local = get_local_pdfs()
pending = parse_pending()

print(f"V3 references with arxiv IDs: {len(v3)}")
print(f"Awesome List entries: {len(awl)}")
print(f"Local PDFs: {len(local)}")
print(f"Pending integration: {len(pending)}")

# Union of all arxiv IDs
all_aids = set(v3.keys()) | set(awl.keys()) | set(local.keys()) | pending
print(f"Total unique arxiv IDs across all sources: {len(all_aids)}")

# Get title from any source (V3 priority > Awesome > -)
def get_title(aid):
    if aid in v3:
        return v3[aid]["title"]
    if aid in awl:
        return awl[aid]
    return "?"

def get_year(aid):
    if aid in v3:
        return v3[aid]["year"]
    # From arxiv id YYMM
    return f"20{aid[:2]}"

# Categorize
def category(aid):
    if not re.match(r'^\d{4}\.\d{4,5}$', aid):
        return "other"
    yymm = aid[:4]
    yr, mo = int(yymm[:2]), int(yymm[2:4])
    if yr < 26:
        return "pre-2026"
    return f"2026-{mo:02d}"

# Sort by category then arxiv_id
sorted_aids = sorted(all_aids, key=lambda a: (category(a), a))

# Build INDEX.md
out = []
out.append("# OPD Project — Master Paper Index")
out.append("")
out.append("_Last updated: 2026-05-16. Independent of paper_kb._")
out.append("")
out.append("This index is built **only from OPD project resources**:")
out.append("- `latex-v3/references.bib` — what V3 cites")
out.append("- `Awesome-LLM-On-Policy-Distillation/README.md` — public catalog")
out.append("- `pdfs/` — local PDFs by date bucket")
out.append("- `papers-meta/opd-new-papers.md` — pending integration tracking")
out.append("")
out.append("## Stats")
out.append(f"- V3 cited papers: **{len(v3)}**")
out.append(f"- Awesome List entries: **{len(awl)}**")
out.append(f"- Local PDFs: **{len(local)}**")
out.append(f"- Pending integration: **{len(pending)}**")
out.append(f"- Total unique arxiv IDs: **{len(all_aids)}**")
out.append("")
out.append("## Legend")
out.append("- **PDF**: ✅ = local PDF available")
out.append("- **V3**: ✅ = cited in latex-v3/references.bib")
out.append("- **AwL**: ✅ = listed in Awesome-LLM-On-Policy-Distillation")
out.append("- **Pend**: 🟡 = waiting for V3 integration")
out.append("")
out.append("---")
out.append("")

# Group by category
groups = {}
for aid in sorted_aids:
    groups.setdefault(category(aid), []).append(aid)

cat_order = ["pre-2026", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "other"]
for cat in cat_order:
    if cat not in groups:
        continue
    aids = groups[cat]
    out.append(f"## {cat} ({len(aids)} papers)")
    out.append("")
    out.append("| # | arXiv ID | Title | Year | PDF | V3 | AwL | Pend |")
    out.append("|---|----------|-------|------|-----|----|----|------|")
    for i, aid in enumerate(aids, 1):
        title = get_title(aid).replace("|", "/")
        year = get_year(aid)
        pdf_mark = f"[✅]({local[aid]})" if aid in local else "❌"
        v3_mark = "✅" if aid in v3 else "—"
        awl_mark = "✅" if aid in awl else "—"
        pend_mark = "🟡" if aid in pending else ""
        out.append(f"| {i} | [`{aid}`](https://arxiv.org/abs/{aid}) | {title} | {year} | {pdf_mark} | {v3_mark} | {awl_mark} | {pend_mark} |")
    out.append("")

# Backlog
out.append("---")
out.append("")
out.append("## Backlog")
out.append("")
out.append("### Cited in V3 but missing PDF")
miss_v3_pdf = [aid for aid in v3 if aid not in local]
for aid in sorted(miss_v3_pdf):
    out.append(f"- [`{aid}`](https://arxiv.org/abs/{aid}) — {v3[aid]['title']}")
out.append("")
out.append("### In Awesome List but missing PDF")
miss_awl_pdf = [aid for aid in awl if aid not in local]
for aid in sorted(miss_awl_pdf):
    out.append(f"- [`{aid}`](https://arxiv.org/abs/{aid}) — {awl[aid]}")
out.append("")
out.append("### V3 cited but not in Awesome List (potential add)")
v3_only = [aid for aid in v3 if aid not in awl]
for aid in sorted(v3_only):
    out.append(f"- `{aid}` — {v3[aid]['title']}")
out.append("")
out.append("### Awesome List but not in V3 (potential cite)")
awl_only = [aid for aid in awl if aid not in v3]
for aid in sorted(awl_only):
    out.append(f"- `{aid}` — {awl[aid]}")
out.append("")

(SURVEY / "papers-meta" / "INDEX.md").write_text("\n".join(out))
print(f"\nWrote {SURVEY / 'papers-meta' / 'INDEX.md'}")
