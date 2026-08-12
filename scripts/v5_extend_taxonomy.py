#!/usr/bin/env python3
"""Add the V5 backlog papers to the taxonomy tree and give agentic OPD its own branch.

The tree is the reader's entry point to the survey, so a method discussed in the
body but absent from the tree is a real gap. This adds each new paper to the leaf
matching where the body actually discusses it, creates a Stage-4 branch for the
agentic methods of Section 7, and recomputes every badge from its own listing.

Idempotent: refuses to run if the agentic branch already exists.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
MAIN = ROOT / "latex-v5/main.tex"

# Short display names, taken from each paper's own title or stated method name.
NAME = {
    "2606.17199": "PowerOPD", "2607.06855": "GEOSD", "2607.16872": "TOPD",
    "2607.22334": "BPM", "2608.01263": "FP-OPD", "2608.01735": "DAPD",
    "2608.09447": "WDL-OPD", "2608.09745": "SR-OPSD", "2608.09836": "TIDE",
    "2606.10369": "PADD", "2606.30626": "DOPD", "2607.04751": "TOP-D",
    "2607.10805": "AD-OPSD", "2607.16955": "CADENCE", "2607.24771": "RoCo-ACE",
    "2607.26057": "Relay-OPD", "2608.00782": "RSTG", "2608.07935": "SDS",
    "2607.04037": "RG-OPD", "2607.05394": "Direct-OPD", "2607.18082": "CriPO",
    "2607.29209": "SAF-OPD", "2608.04419": "SPOT",
    "2606.30406": "MOPD", "2606.30518": "RAPS-DA", "2607.04425": "UI-MOPD",
    "2607.22629": "Masked Distill", "2607.26246": "W2S-OPD",
    "2608.01589": "PS-OPSD", "2608.03092": "SMOPD", "2608.08726": "PAST",
    "2606.19327": "RCSD", "2607.04428": "dOPSD", "2607.15736": "BIRD",
    "2608.02139": "SPEE", "2608.02948": "RuPI", "2608.05131": "OPD-V",
    "2608.08764": "CODA", "2608.09555": "BCSD", "2608.09826": "SKALD",
    "2606.30345": "DRIFT", "2607.23125": "NOPD",
    "2607.18110": "EL",
    "2606.28562": "SEAD", "2607.07050": "Behavior Leverage",
    "2608.04408": "Counterfactual Recov.", "2608.08176": "Capacity-Matched",
    "2607.13124": "ShortOPD", "2607.29494": "Adaptive FastOPD",
    "2608.06802": "Simple-OPD", "2606.24143": "AsyncOPD",
    "2605.16826": "Decoupling KL", "2606.30923": "Noisy-Expert Optimality",
    "2607.23731": "Outcome-Confounded", "2608.09263": "Privileged Likelihood",
    "2606.26091": "Diversity Loss", "2607.13399": "Demystifying OPD",
    "2608.04794": "PI Bias", "2608.09228": "OP2SD",
    # Section 7, agentic and multi-turn
    "2606.27814": "ATOD", "2605.29584": "GAPD", "2608.07371": "TRIAL",
    "2608.01837": "PCSD", "2606.29502": "UCOB", "2606.29863": "KbSD",
    "2608.07068": "MemOPD", "2607.04763": "ReOPD", "2608.01953": "FTB",
    "2608.08960": "CAPS", "2607.05804": "TurnOPD", "2607.29078": "DASH-OPD",
    "2607.24720": "Physics of Multi-Turn", "2606.30044": "Two-Phase Agentic",
}

# Existing leaf -> papers to append. Mirrors where the body prose discusses each.
APPEND = {
    "4.1 Fixed Divergence Objectives": [
        "2606.17199", "2607.06855", "2608.09836", "2607.16872",
        "2607.22334", "2608.01263", "2608.01735", "2608.09447", "2608.09745",
    ],
    "4.2 Adaptive Divergence Objectives": [
        "2606.30626", "2607.10805", "2607.24771", "2607.04751",
        "2607.16955", "2606.10369", "2607.26057", "2608.00782", "2608.07935",
    ],
    "4.3 RL-Augmented Objectives": [
        "2607.04037", "2608.04419", "2607.18082", "2607.29209", "2607.05394",
    ],
    "5.2.1 Privileged Information": [
        "2606.19327", "2608.02948", "2608.09826", "2608.08726", "2607.04428",
        "2608.02139", "2607.15736", "2608.05131", "2608.09555", "2608.08764",
    ],
    "5.2.2 Pure Self-Distillation": ["2606.30345", "2607.23125"],
    "5.2.3 External Feedback": ["2607.18110"],
    "6.1 Token and Sample Weighting": [
        "2606.28562", "2607.07050", "2608.04408", "2608.08176",
    ],
    "6.2 Curriculum and Difficulty Adaptation": [
        "2607.13124", "2607.29494", "2608.06802",
    ],
    "6.3 Compute Optimization": ["2606.24143"],
}

# White-box logit supervision sits under a Same-Family / Cross-Family split.
APPEND_NESTED = {
    "Same-Family": ["2606.30406", "2608.03092", "2607.22629", "2608.01589"],
    "Cross-Family": ["2607.26246", "2606.30518", "2607.04425"],
}

# New Stage-4 branch for Section 7.
AGENTIC = [
    ("7.2 Turn-Level Credit", ["2606.27814", "2605.29584", "2608.07371",
                               "2608.01837", "2606.29502", "2606.29863"]),
    ("7.3 State and Memory Alignment", ["2608.07068", "2607.04763",
                                        "2608.01953", "2608.08960"]),
    ("7.4 Temporal Depth and Budget", ["2607.05804", "2607.29078"]),
    ("7.5 Agentic Failure Modes", ["2607.24720", "2606.30044"]),
]

# Analysis papers belong to Section 8, which the tree does not enumerate.
ANALYSIS_ONLY = ["2605.16826", "2606.30923", "2607.23731", "2608.09263",
                 "2606.26091", "2607.13399", "2608.04794", "2608.09228"]


def cite_lines(aids: list[str], per_line: int = 3, indent: str = "        ") -> str:
    items = [f"{NAME[a]}~\\citep{{{a}}}" for a in aids]
    out = []
    for i in range(0, len(items), per_line):
        chunk = ", ".join(items[i : i + per_line])
        out.append(f"{indent}{chunk},\\\\[1pt]%")
    return "\n".join(out)


def append_to_leaf(text: str, leaf: str, aids: list[str]) -> str:
    """Insert citations at the end of a leaf's method list."""
    pat = re.compile(
        r"(\\textbf\{" + re.escape(leaf) + r"\}.*?)(%\s*\n\s*\}, leaf=)", re.S
    )
    m = pat.search(text)
    if not m:
        raise SystemExit(f"leaf not found: {leaf}")
    indent = "          " if leaf.startswith(("5.", "Same", "Cross")) else "        "
    added = ",\\\\[1pt]%\n" + cite_lines(aids, indent=indent).rstrip(",\\\\[1pt]%\n")
    added = added.rstrip()
    if added.endswith(",\\\\[1pt]%"):
        added = added[: -len(",\\\\[1pt]%")]
    return text[: m.start(2)] + added + text[m.start(2) :]


def main() -> int:
    text = MAIN.read_text()
    if "S 7 Agentic" in text:
        sys.exit("agentic branch already present; aborting")

    notes = json.loads((ROOT / "notes/paper_notes.json").read_text())["notes"]
    all_new = (
        [a for v in APPEND.values() for a in v]
        + [a for v in APPEND_NESTED.values() for a in v]
        + [a for _, v in AGENTIC for a in v]
        + ANALYSIS_ONLY
    )
    missing_name = [a for a in all_new if a not in NAME]
    if missing_name:
        sys.exit(f"no display name for: {missing_name}")
    dupes = {a for a in all_new if all_new.count(a) > 1}
    if dupes:
        sys.exit(f"assigned to more than one leaf: {sorted(dupes)}")
    unknown = [a for a in all_new if a not in notes]
    if unknown:
        sys.exit(f"not in notes DB: {unknown}")
    print(f"placing {len(all_new)} papers ({len(ANALYSIS_ONLY)} are analysis-only, no tree leaf)")

    for leaf, aids in {**APPEND, **APPEND_NESTED}.items():
        text = append_to_leaf(text, leaf, aids)
        print(f"  {leaf}: +{len(aids)}")

    MAIN.write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
