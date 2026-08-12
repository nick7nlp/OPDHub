#!/usr/bin/env python3
"""Sync the taxonomy-tree badge counts in latex-v5/main.tex.

Each leaf of the forest taxonomy declares a count badge and then lists the
methods it covers. The badge should equal the number of methods actually listed
in that leaf, otherwise the figure contradicts itself. This recomputes every
badge from its own citation list and reports what changed.

Read-only unless --write is passed.
"""

import re
import sys
from pathlib import Path

MAIN = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/latex-v5/main.tex")

LEAF = re.compile(
    r"(\\textbf\{(?P<name>[\d.]+ [^}]+)\}~\{\\tikz\[baseline=-0\.5ex\]"
    r"\\node\[badge=(?P<colour>\w+)\]\{)(?P<count>\d+)(\};\})(?P<body>.*?)(?=\}, leaf=)",
    re.S,
)


def main() -> int:
    write = "--write" in sys.argv
    text = MAIN.read_text()
    tree_m = re.search(r"\\begin\{forest\}(.*?)\\end\{forest\}", text, re.S)
    if not tree_m:
        print("no forest block found", file=sys.stderr)
        return 1
    tree = tree_m.group(1)

    changes = []

    def fix(m: re.Match) -> str:
        listed = len(re.findall(r"\\citep\{", m.group("body")))
        declared = int(m.group("count"))
        if listed != declared:
            changes.append((m.group("name"), declared, listed))
        return f"{m.group(1)}{listed}{m.group(5)}{m.group('body')}"

    new_tree = LEAF.sub(fix, tree)

    print(f"{'leaf':44s} {'was':>5s} {'now':>5s}")
    for name, was, now in changes:
        print(f"{name[:43]:44s} {was:>5d} {now:>5d}")
    print(f"\n{len(changes)} badge(s) out of sync")

    if not changes:
        return 0
    if not write:
        print("(dry run; pass --write to apply)")
        return 0

    MAIN.write_text(text[: tree_m.start(1)] + new_tree + text[tree_m.end(1) :])
    print("applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
