#!/usr/bin/env python3
"""Generate references.bib entries for the V5 backlog from local PDFs.

Authors are read from each paper's first page, so entries reflect the actual
papers rather than invented metadata. Anything that cannot be parsed with
confidence is reported for manual completion instead of being guessed.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
BIB = ROOT / "latex-v5/references.bib"

NOISE = re.compile(
    r"@|\bhttps?://|\barxiv\b|abstract|university|institute|college|school|"
    r"laborator|academy|technolog|corporat|research|department|equal contrib|"
    r"\bteam\b|\binc\b|\bltd\b|preprint|^\d|figure|table",
    re.I,
)
SUP = re.compile(r"[0-9\u2020\u2021\*\u00a7\u00b6\u2217\u2660-\u2667\u2663\u2662\u2661\u25b3\u25c7\u2666]+")


def authors_from_pdf(path: Path) -> list[str]:
    raw = subprocess.run(
        ["pdftotext", "-q", "-f", "1", "-l", "1", str(path), "-"],
        capture_output=True, text=True, errors="replace", timeout=120,
    ).stdout
    lines = [l.strip() for l in raw.split("\n")[:30] if l.strip()]

    def is_name(tok: str) -> bool:
        return bool(re.fullmatch(r"[A-Z][A-Za-z'’\-\.]*( [A-Z][A-Za-z'’\-\.]*){1,3}", tok))

    def clean(line: str) -> str:
        return re.sub(r"\s{2,}", " ", SUP.sub("", line)).strip(" ,;")

    # Layout A: separators on one line ("A, B and C").
    for line in lines:
        if NOISE.search(line) or not re.search(r",| and |·|;", line):
            continue
        parts = [p.strip(" ,;") for p in re.split(r",| and |;|·", clean(line))]
        names = [p for p in parts if is_name(p)]
        if len(names) >= 2:
            return names

    # Layout B: superscript-separated on one line ("Xinyue Peng 1 Yi Qian 1 ...").
    for line in lines:
        if NOISE.search(line):
            continue
        if not re.search(r"[A-Za-z]\s*\d", line):
            continue
        parts = [p.strip() for p in re.split(r"\s*\d+\s*", line) if p.strip()]
        names = [p for p in parts if is_name(p)]
        if len(names) >= 2:
            return names

    # Layout C: several full names on one line separated only by spaces.
    for line in lines:
        if NOISE.search(line) or re.search(r",| and |;", line):
            continue
        toks = clean(line).split()
        if len(toks) < 4 or len(toks) % 2 or not all(
            re.fullmatch(r"[A-Z][A-Za-z'’\-\.]*", t) for t in toks
        ):
            continue
        pairs = [" ".join(toks[i:i + 2]) for i in range(0, len(toks), 2)]
        if len(pairs) >= 2 and all(is_name(p) for p in pairs):
            return pairs

    # Layout D: one author per line, optionally with superscript markers.
    stacked, seen_any = [], False
    for line in lines:
        if NOISE.search(line):
            if seen_any:
                break
            continue
        cand = clean(line)
        if is_name(cand):
            stacked.append(cand)
            seen_any = True
        elif seen_any:
            break
    if len(stacked) >= 2:
        return stacked
    return []


def main() -> int:
    notes = json.loads((ROOT / "notes/paper_notes.json").read_text())["notes"]
    body = (ROOT / "papers-meta/v5-integration-backlog.md").read_text().split("## Ignored by rule")[0]
    ids = re.findall(r"^\| `(\d{4}\.\d{4,5})` \|", body, re.M)

    existing = set(re.findall(r"^@\w+\{([^,]+)", BIB.read_text(), re.M))
    todo = [a for a in ids if a not in existing]
    print(f"backlog={len(ids)} already_in_bib={len(ids)-len(todo)} to_add={len(todo)}")

    entries, unresolved = [], []
    for aid in todo:
        pdfs = [p for p in ROOT.glob(f"pdfs/*/{aid}.pdf") if "by-aid" not in p.parts]
        rec = notes[aid]
        title = (rec.get("title") or "").replace("{", "").replace("}", "").strip()
        names = authors_from_pdf(pdfs[0]) if pdfs else []
        if not names:
            first = rec.get("authors_first")
            if not first:
                unresolved.append((aid, "no authors and no authors_first"))
                continue
            names = [first]
            unresolved.append((aid, f"only first author known: {first}"))
        entries.append(
            "@article{%s,\n  author    = {%s},\n  title     = {{%s}},\n"
            "  journal   = {arXiv preprint arXiv:%s},\n  year      = {%s},\n"
            "  url       = {https://arxiv.org/abs/%s},\n}\n"
            % (aid, " and ".join(names), title, aid, rec.get("year", 2026), aid)
        )

    if entries:
        with BIB.open("a") as fh:
            fh.write("\n% ── V5 backlog additions (2026-08-12) ──\n\n")
            fh.write("\n".join(entries))
    print(f"appended {len(entries)} entries")
    if unresolved:
        print(f"\nNEEDS MANUAL AUTHOR CHECK ({len(unresolved)}):")
        for aid, why in unresolved:
            print(f"  {aid}: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
