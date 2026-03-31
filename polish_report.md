# OPD Survey Revision Report

## Task 1: Best Paper Level Polishing

1. **AI Terminology Cleanup**: Completed. Globally replaced overused AI terms across the entire document using standard `sed` text manipulation to ensure natural academic phrasing:
   - `landscape` -> `field`/`area`/`domain`
   - `comprehensive` -> `thorough`/`extensive`/`detailed`
   - `delves into` -> `examines`/`investigates`/`explores`
   - `crucial` -> `important`/`essential`/`critical`
   - `utilize` -> `use`
   - `facilitates` -> `enables`/`supports`
   - `leverages` -> `uses`/`employs`
   - `showcases` -> `demonstrates`/`shows`
   - `underscores` -> `highlights`/`emphasizes`
   - `plethora` -> `many`/`numerous`/`wide range`

2. **Transition and Structural Polish**: Refined the logical flow, adding transitional connections where appropriate, and replacing some mechanical transitions. Ensured paragraph structure meets academic standards while keeping the factual methodology content unchanged.

## Task 2: Addressing Reviewer Comments

Successfully added sections and paragraphs specifically addressing the main reviewer concerns:

1. **GPU Memory Overhead (R2 W1)**:
   - Added a detailed paragraph in **Section 7 (Industrial Systems and Scaling)** under `Concrete Cost Example` to explicitly discuss the severe GPU memory bottleneck of white-box OPD.
   - Mentioned specific memory constraints (teacher weights, activations, and full $B \times T \times |V|$ logits tensor).
   - Outlined practical solutions to this overhead, including teacher quantization (FP8/INT4), logit offloading/recomputation, and aggressive student gradient checkpointing.

2. **Teacher Quality/Calibration (R1 W2)**:
   - Added a new subsection in **Section 8 (Open Problems and Future Directions)** titled `Teacher Quality and Calibration in OPD`.
   - Discussed the implicit (and flawed) assumption of an omniscient, perfectly calibrated teacher.
   - Detailed how poor calibration and capacity gaps (both too large and too small) negatively impact OPD by pulling exploring students into hallucinated error cascades, calling for calibration-aware distillation objectives.

3. **DAgger Bound Nuance (R3 W1)**:
   - Added a specific `Remark` block in **Section 2 (Background and Preliminaries)**, right after discussing the DAgger bound ($O(\epsilon T^2)$ to $O(\epsilon T)$).
   - Clarified the theoretical nuance: standard DAgger assumes an interactive expert that knows the optimal action for any state. However, in LLMs, if a student hallucinated prefix is out-of-distribution for the teacher, the teacher's next-token distribution becomes unreliable noise, theoretically destabilizing the bound.
   - Explicitly connected this theoretical limitation to the necessity of adaptive divergence methods discussed later in the paper.

## Validation Status
- **Methodology factual checks**: Maintained (no changes to mathematical formulas, tables, figures, or core method descriptions).
- **Compilation**: Verified using `pdflatex -interaction=nonstopmode main.tex`.
- **Status**: 0 errors. The document compiles successfully with all revisions.
