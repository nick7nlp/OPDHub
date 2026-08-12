#!/usr/bin/env python3
"""Insert agent-written paragraph blocks into latex-v5/main.tex.

Input file format:

    ===SECTION <label>===
    <one or more paragraphs, one line each, blank-line separated>
    ===SECTION <label>===
    ...

Each block is appended at the end of the subsection carrying that label, i.e.
immediately before the next \subsection or \section. Refuses to insert a block
whose citations are not all present in references.bib, and refuses to duplicate
text already in the file.
"""

import re
import sys
from pathlib import Path

ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
MAIN = ROOT / "latex-v5/main.tex"
BIB = ROOT / "latex-v5/references.bib"


def parse(path: Path) -> dict[str, list[str]]:
    blocks, label = {}, None
    for raw in path.read_text().split("\n"):
        m = re.match(r"^===SECTION\s+(\S+?)\s*===$", raw.strip())
        if m:
            label = m.group(1)
            blocks[label] = []
            continue
        if label is not None:
            blocks[label].append(raw)
    return {k: v for k, v in blocks.items() if any(l.strip() for l in v)}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: v5_insert_blocks.py <blocks.txt>", file=sys.stderr)
        return 2

    blocks = parse(Path(sys.argv[1]))
    if not blocks:
        print("no blocks parsed", file=sys.stderr)
        return 1

    bib_keys = set(re.findall(r"^@\w+\{([^,]+)", BIB.read_text(), re.M))
    lines = MAIN.read_text().split("\n")

    # Validate before touching the file.
    plan = []
    for label, body in blocks.items():
        try:
            i = next(i for i, l in enumerate(lines) if l.strip() == f"\\label{{{label}}}")
        except StopIteration:
            print(f"label not found: {label}", file=sys.stderr)
            return 1
        cites = set(re.findall(r"\\cite[tp]\{([^}]+)\}", "\n".join(body)))
        cites = {c.strip() for group in cites for c in group.split(",")}
        missing = sorted(c for c in cites if c not in bib_keys)
        if missing:
            print(f"{label}: citations missing from bib: {missing}", file=sys.stderr)
            return 1
        first = next((l for l in body if l.strip()), "")
        if first and first[:80] in "\n".join(lines):
            print(f"{label}: content appears already inserted; aborting", file=sys.stderr)
            return 1
        plan.append((i, label, [l for l in body if l is not None], len(cites)))

    # Insert bottom-up so earlier indices stay valid.
    for i, label, body, ncite in sorted(plan, key=lambda x: -x[0]):
        j = next(
            k for k in range(i + 1, len(lines))
            if lines[k].startswith("\\subsection") or lines[k].startswith("\\section")
        )
        while j > i and not lines[j - 1].strip():
            j -= 1
        trimmed = list(body)
        while trimmed and not trimmed[0].strip():
            trimmed.pop(0)
        while trimmed and not trimmed[-1].strip():
            trimmed.pop()
        lines[j:j] = [""] + trimmed
        print(f"{label}: inserted {len(trimmed)} lines, {ncite} citations")

    MAIN.write_text("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
