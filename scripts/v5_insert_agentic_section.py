#!/usr/bin/env python3
"""Insert §7 Agentic and Multi-Turn OPD into latex-v5/main.tex.

Moves existing agentic passages into the new section, replaces each origin with a
one-way pointer, and merges the duplicated TCOD mechanism so it is explained once.
Idempotent: refuses to run twice.
"""

import re
import sys
from pathlib import Path

MAIN = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/latex-v5/main.tex")

text = MAIN.read_text()
if "sec:agentic" in text:
    sys.exit("already restructured; aborting")

lines = text.split("\n")


def find(pattern, start=0):
    rx = re.compile(pattern)
    for i in range(start, len(lines)):
        if rx.search(lines[i]):
            return i
    raise SystemExit(f"anchor not found: {pattern}")


# ── 1. capture the passages we migrate ──────────────────────────────────────
i_pi = find(r"^\\textbf\{Outcome-conditioned PI at the turn level")
pi_body = lines[i_pi]
pi_tail = lines[i_pi + 2]          # "Viewed together with TCOD, ..."

i_tcod = find(r"^\\textbf\{Temporal curriculum for multi-turn distillation")
tcod_body = lines[i_tcod]

i_fail = find(r"^\\textbf\{Agentic collapse in multi-turn OPD")
fail_body = lines[i_fail]
fail_tail = lines[i_fail + 2]      # "Taken together, these pathologies ..."

i_blk = find(r"^\\textbf\{Agentic distillation\.\}")
i_blk_end = find(r"^The ladder from trajectory-level control", i_blk)
block = lines[i_blk : i_blk_end + 1]          # L1421..L1431 equivalent

# ── 2. build §7 ────────────────────────────────────────────────────────────
# Drop the TCOD paragraph from the migrated block: its mechanism is described in
# full by tcod_body, which lands in §7.4. Keeping both would restate one method.
block_no_tcod = [l for l in block if not l.startswith(r"At the \emph{trajectory level}, TCOD")]

sec7 = [
    r"\section{Agentic and Multi-Turn On-Policy Distillation}",
    r"\label{sec:agentic}",
    "",
    r"The methods surveyed so far assume a single-turn response: the student emits one "
    r"sequence, the teacher scores it, and supervision ends there. Agentic deployment "
    r"breaks that assumption. When the student acts over many turns in an environment, "
    r"three problems appear that have no single-turn counterpart, namely credit assignment "
    r"across turns, alignment between the teacher's scoring context and the states the "
    r"student actually visited, and the choice of how deep into a trajectory supervision "
    r"should reach. This section collects the mechanisms that exist because of multi-turn "
    r"structure. Mechanisms that happen to be evaluated on agents but do not depend on "
    r"turn structure, such as divergence design (Section~\ref{sec:objectives}) or "
    r"token weighting (Section~\ref{subsec:weighting}), remain in their respective sections.",
    "",
    r"\subsection{Why Single-Turn OPD Breaks Down}",
    r"\label{subsec:agentic_why}",
    "",
    r"The exposure-bias argument of Section~\ref{sec:background} already explains why "
    r"training on teacher-generated text degrades under the student's own distribution: "
    r"the DAgger bound gives error compounding of order $O(\epsilon T)$ once the student "
    r"controls its own state visitation. OPD removes that gap for a single response by "
    r"sampling states from $d_{\ptheta}$. Multi-turn interaction reinstates it one level up.",
    "",
    r"The shift is qualitative rather than one of degree. In single-turn generation a "
    r"flawed token perturbs the remaining tokens of the same sequence, and the teacher can "
    r"still score every prefix the student produced. In an interactive setting a flawed "
    r"action at turn $t$ changes the environment state, so every later observation the "
    r"student conditions on is one the teacher never saw. Supervision is then computed on a "
    r"state distribution that neither policy occupies, which is a stronger failure than "
    r"distributional mismatch within a fixed context. Agents that compress or rewrite their "
    r"history make this explicit: the teacher is asked to score actions under a context the "
    r"student never actually visited (Section~\ref{subsec:agentic_state}).",
    "",
    r"Three consequences organize the rest of this section. Outcome rewards arrive once per "
    r"trajectory while errors are located at particular turns, which is a credit-assignment "
    r"problem (Section~\ref{subsec:agentic_credit}). The teacher's scoring context and the "
    r"student's visited states can diverge, which is a state-alignment problem "
    r"(Section~\ref{subsec:agentic_state}). Supervising all turns from the outset injects "
    r"gradients where the student's state has already drifted, which is a temporal-depth "
    r"problem (Section~\ref{subsec:agentic_depth}). Section~\ref{subsec:agentic_failure} "
    r"catalogues the pathologies that follow when these three are left unaddressed.",
    "",
    r"\subsection{Turn-Level Credit Assignment}",
    r"\label{subsec:agentic_credit}",
    "",
    pi_body,
    "",
    pi_tail,
    "",
    r"\subsection{State and Memory Alignment}",
    r"\label{subsec:agentic_state}",
    "",
    r"Turn-level credit presumes that the teacher and the student share a context. Agents "
    r"that summarize, prune, or rewrite their interaction history violate that premise, and "
    r"the resulting mismatch is distinct from the divergence-level mismatch treated in "
    r"Section~\ref{sec:objectives}.",
    "",
    r"\subsection{Temporal Depth and Rollout Budget}",
    r"\label{subsec:agentic_depth}",
    "",
    tcod_body,
    "",
    r"\subsection{Agentic Failure Modes}",
    r"\label{subsec:agentic_failure}",
    "",
    fail_body,
    "",
    fail_tail,
    "",
    r"\subsection{Granularity of the Distillation Unit}",
    r"\label{subsec:agentic_granularity}",
    "",
] + block_no_tcod + [""]

# ── 3. replace origins with one-way pointers ───────────────────────────────
PTR_PI = (
    r"\textbf{Turn-level PI for agentic reasoning.} Privileged information can also be "
    r"supplied at the level of an interaction turn rather than a single response. Because "
    r"that construction depends on multi-turn trajectory structure, it is treated with the "
    r"other agentic mechanisms in Section~\ref{subsec:agentic_credit}."
)
PTR_TCOD = (
    r"\textbf{Temporal depth as a second axis.} The methods above all select \emph{which "
    r"prompts} to train on. Multi-turn trajectories admit an orthogonal question, namely "
    r"how deep within one trajectory supervision should reach. Since that axis exists only "
    r"when the student acts over many turns, it is developed in "
    r"Section~\ref{subsec:agentic_depth}."
)
PTR_FAIL = (
    r"\textbf{Agentic failure modes.} Multi-turn interaction produces a further family of "
    r"pathologies, in which teacher dynamics interact with trajectory structure. These are "
    r"catalogued in Section~\ref{subsec:agentic_failure}."
)
PTR_BLK = (
    r"\textbf{Agentic distillation.} Multi-turn agentic deployment is the setting where "
    r"OPD's state-distribution argument matters most, and it carries enough distinct "
    r"machinery to be treated separately in Section~\ref{sec:agentic}. In deployment terms "
    r"the recurring pattern is that the granularity of the distillation unit must match the "
    r"granularity at which errors compound in the target task."
)

# apply from the bottom up so earlier indices stay valid
lines[i_blk : i_blk_end + 1] = [PTR_BLK]
lines[i_fail : i_fail + 3] = [PTR_FAIL]
lines[i_tcod] = PTR_TCOD
lines[i_pi : i_pi + 3] = [PTR_PI]

# ── 4. insert §7 before the "Understanding OPD" section ────────────────────
i_und = find(r"^\\section\{Understanding OPD")
lines[i_und:i_und] = sec7

MAIN.write_text("\n".join(lines))
print(f"inserted §7 ({len(sec7)} lines) before line {i_und}")
print("pointers placed at: PI, curriculum, failure-modes, industrial")
