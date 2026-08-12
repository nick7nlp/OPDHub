#!/usr/bin/env python3
"""Write the 14 multi-turn-specific papers into §7 of latex-v5/main.tex.

Each paragraph is inserted at the end of its target subsection so the existing
migrated passages keep their position and framing.
"""

import re
import sys
from pathlib import Path

MAIN = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/latex-v5/main.tex")
text = MAIN.read_text()
if "ATOD~\\citep{2606.27814}" in text:
    sys.exit("§7 content already written; aborting")

lines = text.split("\n")

CREDIT = [
    r"\textbf{Fusing turn-level teacher signal with outcome reward.} A first group of methods "
    r"treats the teacher's log-probability gap as an additional advantage term inside a policy-gradient "
    r"update, which localizes credit without discarding the outcome reward. "
    r"ATOD~\citep{2606.27814} makes the mixture explicit, forming a token-level advantage "
    r"$A_t = \kappa(s)\,(\log \pi_T(a_t|s_t) - \log \pi_\theta(a_t|s_t))\,w_{k(t)} + \rho(s) A^{\mathrm{GRPO}}_t$ "
    r"in which annealed coefficients shift training from teacher-dominated to reward-dominated, while a "
    r"turn-level soft-OR reweighting concentrates distillation on turns implicated in failure. The reported "
    r"gain of $3.03$ points over plain OPD and $23.62$ over GRPO across three student sizes suggests that "
    r"neither signal alone is sufficient in the multi-turn regime. "
    r"GAPD~\citep{2605.29584} supplies the missing teacher rather than assuming one: entity-anchor matching "
    r"aligns the student's on-policy execution state with a gold execution state, and the current policy "
    r"conditioned on the aligned gold action acts as a self-teacher whose token-level gap "
    r"$d_{i,k} = \log p_{\mathrm{teach}} - \log p_{\mathrm{stud}}$ is clipped and added to the GRPO advantage. "
    r"On GrailQA this raises EM/F1 from $83.9/86.1$ to $87.8/89.5$ over an outcome-only baseline.",
    "",
    r"\textbf{Normalizing hindsight credit across turns.} Hindsight relabeling gives a turn-level signal, but "
    r"its raw magnitude varies systematically along a trajectory, so later turns can dominate purely by scale. "
    r"TRIAL~\citep{2608.07371} normalizes hindsight gap magnitudes to a mean-one profile across turns, "
    r"redistributing dense supervision while preserving the signed direction of each token-level revision, and "
    r"reports WebShop success rising from $56.4\%$ to $75.2\%$ with a $1.7$B student. "
    r"PCSD~\citep{2608.01837} attacks the same instability from the temporal side, deriving token weights from "
    r"the \emph{persistence} of teacher-favoring signals through adaptive window aggregation with exponential "
    r"decay, instead of trusting isolated pointwise disagreement. Its $90.6\%$ ALFWorld result exceeds GRPO by "
    r"$15.6$ points and SDAR by $6.2$. Both results point the same way: in long trajectories the reliability of "
    r"a per-token signal depends on its neighbourhood, not on its instantaneous value.",
    "",
    r"\textbf{Choosing the teacher's context view.} When teacher and student share parameters, the remaining "
    r"design freedom is which context each side sees. UCOB~\citep{2606.29502} removes the fixed direction "
    r"assumed by earlier skill-conditioned methods: at each anchor state the higher-return context view "
    r"(skill or no-skill) becomes the local teacher for the other, so supervision follows measured return "
    r"rather than a prior about which view is stronger, improving ALFWorld success by $23.5$ points over a "
    r"single-direction baseline. KbSD~\citep{2606.29863} instantiates the same asymmetry through knowledge "
    r"boundary hints, where an architecturally identical teacher receives parametric-certainty and "
    r"retrieval-quality cues and the divergence is selected per quadrant, cutting the unreliability rate from "
    r"$64.32\%$ to $47.60\%$ on a $3$B agent.",
]

STATE = [
    r"\textbf{Context rewriting breaks the teacher's scoring context.} Agents with compact memory summarize or "
    r"prune history to stay within a context budget, which means the state the teacher scores is not the state "
    r"the student acted in. MemOPD~\citep{2608.07068} identifies this state mismatch and reconstructs the exact "
    r"invocation state (positions, visibility, and prior content) before computing "
    r"$L_{\mathrm{OPD}}$ over the teacher-visible mask, reporting F1 gains of up to $416.2\%$ over PPO on "
    r"long-horizon retrieval. The size of that margin is less a claim about OPD's strength than an indication "
    r"of how badly misaligned supervision degrades once histories are rewritten.",
    "",
    r"\textbf{Replayed prefixes and the prefix trap.} Live environment interaction is often the dominant cost "
    r"of agentic OPD. ReOPD~\citep{2607.04763} reuses offline teacher trajectories as replayed prefixes and, in "
    r"doing so, isolates a two-sided constraint it terms the \emph{prefix trap}: prefixes far from the student's "
    r"occupancy waste supervision, while prefixes far from the teacher's competence make the teacher's "
    r"log-probabilities unreliable. A step-dependent weighting over $\alpha_t$ balances the two, improving the "
    r"math average from $55.1$ to $57.2$. This is the multi-turn form of the mixture-policy question raised in "
    r"Section~\ref{subsec:f-div}, now posed over trajectory prefixes rather than tokens.",
    "",
    r"\textbf{Validating guidance before trusting it.} Local disagreement between teacher and student is a weak "
    r"proxy for whether the teacher's preferred action is actually reachable. FTB~\citep{2608.01953} executes a "
    r"short teacher bridge at high-disagreement states and compares the teacher-preferred token ratio of the "
    r"induced student continuations, using the outcome to gate the dense term. It outperforms vanilla OPD and "
    r"TCOD-B2F by $16.6$ and $7.6$ points respectively in a $32$B-to-$1.7$B setting, evidence that "
    r"\emph{recoverability} of a divergence matters more than its magnitude.",
    "",
    r"\textbf{Cross-modal state alignment.} The mismatch can also arise from modality rather than memory. "
    r"CAPS~\citep{2608.08960} diagnoses an agentic policy gap in vision--text compression, where a "
    r"visual-history policy underperforms its text-history counterpart on identical decisions, and closes it by "
    r"letting the same model's text-history policy supply capped forward-KL supervision on states visited by "
    r"the visual-history policy. Gains of $5.0\%$ (3B) and $3.4\%$ (7B) on SearchQA come with up to $83.4\%$ "
    r"lower peak memory-context cost, making this a case where OPD buys efficiency rather than raw capability.",
]

DEPTH = [
    r"\textbf{Adaptive rollout depth.} A temporal curriculum fixes the schedule in advance; the depth can also "
    r"be chosen online. TurnOPD~\citep{2607.05804} selects rollout length per update from a survivor-weighted KL "
    r"centroid subject to coverage thresholds, and anneals the objective from token-level to turn-normalized as "
    r"training proceeds, reaching $2.29\times$ faster training on ALFWorld while improving Same-Step Avg@4 from "
    r"$83.0$ to $86.3$. Efficiency and accuracy move together here because supervising turns the student cannot "
    r"yet reach contributes cost without gradient.",
    "",
    r"\textbf{Evidence-driven switching.} DASH-OPD~\citep{2607.29078} replaces fixed or random curricula with "
    r"bidirectional executor switching driven by accumulated multi-turn discrepancy evidence, using hysteresis "
    r"to avoid oscillation near the decision boundary. It reaches $32.85\%$ overall success with a $1.7$B "
    r"student, $5.84$ points above TCOD. Read alongside TCOD's scheduled expansion, the comparison suggests "
    r"that the right supervision depth is a property of the current student rather than of the training step.",
]

FAILURE = [
    r"\textbf{Where OPD helps and where reward suffices.} The pathologies above raise the prior question of "
    r"when dense teacher supervision is the right tool at all. \citet{2607.24720} separate planning "
    r"\emph{patterns}, which carry low mutual information with the task instance, from planning "
    r"\emph{knowledge}, which carries high mutual information, and use the distinction to map the applicability "
    r"boundaries of GRPO and OPD. Under low-quality pre-training data and long horizons, OPD holds a broader "
    r"effective region ($+18.42$ average versus GRPO's $+7.39$ on a 4Opt:8Sub configuration), while cascaded "
    r"multi-teacher OPD shows diminishing returns once teachers share representations. This gives the decision "
    r"framework of Section~\ref{subsec:on_vs_off} a multi-turn counterpart.",
    "",
    r"\textbf{Mode covering across tasks.} A failure mode specific to multi-task agents concerns the divergence "
    r"direction rather than the horizon. \citet{2606.30044} show that forward KL is mode-covering when a single "
    r"student must absorb several task-specific experts, so on-policy refinement alone cannot recover "
    r"single-task RL performance and off-policy initialization alone cannot either; the two phases together "
    r"raise telecom pass\textsuperscript{4} from $57.9\%$ to $69.4\%$ at 8B. The cold-start argument of "
    r"Section~\ref{subsec:curriculum} therefore carries over to the agentic setting, with task interference as "
    r"an additional reason the student's initial policy sits too far from any one expert.",
]


def append_to_subsection(label: str, block: list[str]) -> None:
    """Insert block just before the next \subsection or \section after `label`."""
    i = next(i for i, l in enumerate(lines) if l.strip() == f"\\label{{{label}}}")
    j = next(
        k for k in range(i + 1, len(lines))
        if lines[k].startswith("\\subsection") or lines[k].startswith("\\section")
    )
    while j > i and not lines[j - 1].strip():
        j -= 1
    lines[j:j] = [""] + block


for label, block in [
    ("subsec:agentic_failure", FAILURE),
    ("subsec:agentic_depth", DEPTH),
    ("subsec:agentic_state", STATE),
    ("subsec:agentic_credit", CREDIT),
]:
    append_to_subsection(label, block)

MAIN.write_text("\n".join(lines))
print("wrote 14 papers into §7.2-§7.5")
