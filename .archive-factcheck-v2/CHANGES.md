# Change Log: V1.5 → V2

**V1.5** (arXiv submission, Apr 2026): 101 citations · 53 pages · `latex-v1.5/`
**V2** (current working version, May 2026): 118 citations · 56 pages · `latex-v2/`

---

## Scope Extension

V2 expands V1.5 with **18 new citations** and reorganizes the taxonomy around three major additions: **preference-based self-distillation**, **agentic multi-turn OPD**, and **industrial-scale multi-teacher distillation**.

## New Citations (18)

### Newly surveyed OPD methods (14)

| Citation Key | Paper | arXiv | Integrated in |
|---|---|---|---|
| `pbsd2026` | Preference-Based Self-Distillation (PBSD) | 2605.05040 | §5.3.1 (main), §4.3, Table 1, Table 3, Taxonomy |
| `ttopd2026` | Turn-level Truncated OPD (HEALTHCARE AI GYM) | 2605.02943 | §5.3.1, §7.2, §8.2, Table 1, Table 3, Taxonomy |
| `hou2026uniopd` | Uni-OPD: Dual-Perspective Recipe | 2605.03677 | §6.2, Table 1, Table 3, Taxonomy |
| `chen2026tcod` | TCOD: Trajectory-Curriculum OPD | 2604.24005 | §6.2, §7.2, Table 1, Taxonomy |
| `gu2026copd` | CoPD: Co-evolving Parallel Distillation | 2604.27083 | §5.3.3, §8.1, §9, Table 1, Taxonomy |
| `wang2026prism` | PRISM: Black-box pre-alignment for multimodal OPD | 2604.28123 | §5.2, §6.2, Table 1, Taxonomy |
| `wang2026paint` | PAINT: Partial-solution masking self-distillation | 2604.26573 | §5.3.2, §6.2, Table 1, Taxonomy |
| `wang2026madopd` | MAD-OPD: Multi-Agent Debate OPD | 2605.01347 | §5.1, §6.1, §8.2, Table 1, Table 3, Taxonomy |
| `qin2026msd` | MSD: Multilingual Safety Self-Distillation | 2605.02971 | §5.3.1, Table 1, Table 3, Taxonomy |
| `zhang2026guisd` | GUI-SD: Visual Spatial PI for GUI agents | 2605.00642 | §5.3.1, §8.2, Table 1, Table 3, Taxonomy |
| `2604.16830` | CaOPD: Scaling Law of Miscalibration | arXiv:2604.16830 | §6.2, §7.2, Table 1, Taxonomy |
| `2604.17535` | OPSDL: Short-context → Long-context Self-Distillation | arXiv:2604.17535 | §5.3.1, Table 1, Table 3, Taxonomy |
| `2604.20933` | IRIS: Interpolative Rényi self-play | arXiv:2604.20933 | §5.3.2, Table 1, Taxonomy |
| `2509.14526` | Delta-KD: Base-to-Instruct delta | arXiv:2509.14526 | §5.1, Table 1, Taxonomy |

### Framework/analysis citations (4)

| Citation Key | Paper | Purpose |
|---|---|---|
| `deepseekv4` | DeepSeek-V4 technical report | §8.1 Industrial Deployment, §8.3 Systems |
| `lu2025onpolicy` | On-Policy Self-Distillation analysis | §4.1 sampled-token KL analysis |
| `2501.16937` | TAID: Temporal interpolation for KD | §5.1 signal source, Table 1, Table 3 |
| `2211.09110` | Scaling law reference | §2.4 Distillation Scaling Laws |

## Removed Citation (1)

- `2006.05525` (Gou et al., "Knowledge Distillation: A Survey") — superseded by `2402.13116` (LLM KD Survey) which is the topically appropriate reference for §1 and §7.3 OPD-specific discussion.

## Structural Updates

### §3 Taxonomy Tree
- Method count grew from 66 → **80** across 11 leaves.
- §5.3 split into three 5.3.1/5.3.2/5.3.3 subcategories (Privileged Information / Self-Play / External Feedback).
- §6 Training Dynamics refined into 6.1 Token Weighting / 6.2 Curriculum / 6.3 Compute Optimization.

### §4 Objective Functions
- §4.1 Fixed Divergence: added sampled-token KL framework (`lu2025onpolicy`).
- §4.3 RL-Augmented: added PBSD positioning as DPO-style preference-based self-distillation.

### §5 Signal Source
- §5.3.1 Privileged Information substantially expanded:
  - Added agentic OPD granularity spectrum (trajectory/turn/step/skill)
  - PBSD as context-augmented reference teacher with preference margin loss
  - TT-OPD as turn-level EMA teacher with outcome-conditioned hints
  - OPSDL as short-context → long-context self-distillation
  - MSD as cross-lingual English-CoT PI
  - GUI-SD as visual spatial PI for multimodal agents

### §6 Training Dynamics
- §6.2 Curriculum: added CaOPD (Scaling Law of Miscalibration), TCOD (trajectory-level curriculum), Uni-OPD (dual-perspective data balancing), PAINT (overlap-adaptive curriculum), PRISM (multimodal pre-alignment).

### §7 Understanding OPD
- §7.2 Failure Modes fully rewritten to integrate:
  - Agentic collapse (3 pathologies from TT-OPD, cross-referenced to TCOD, Skill-SD, MAD-OPD, epistemic suppression from `2603.24472`)
  - Calibration-capability gap (CaOPD's "Scaling Law of Miscalibration")
  - Diversity collapse (precision-recall tradeoff)
  - Saturation ceiling (SPIN → IRIS → π-Play trajectory)

### §8 Applications, Systems, and Emerging Domains
- §8.1 Industrial Deployment: added DeepSeek-V4 as third deployment pattern (full-vocab multi-teacher R-KL at 1.6T MoE scale).
- §8.2 Emerging Domains: added CoPD (multi-capability consolidation), TT-OPD (medical multi-turn), GUI-SD (GUI agents).
- §8.3 System-Level: cross-references to DeepSeek-V4 + OSS frameworks (OpenRLHF, veRL, vLLM, TRT-LLM).

### §9 Open Problems
- Added agentic OPD "three conditions" principle (stable teacher dynamics + trajectory regularizers + granularity-matched credit).
- CoPD surfaced as instance of co-evolution future direction.

## Verification

- **118 bib entries** ↔ **118 unique cite keys** used in text (1:1 match, 0 orphans, 0 undefined).
- 2 tables (Comparison Table with 61 methods, Experimental Configs with 39 methods).
- Compiles clean: 56 pages, 0 LaTeX errors (font warnings only).
- All cross-refs verified: `sec:objectives`, `sec:signal`, `sec:dynamics`, `sec:applications`, `subsec:curriculum`, `subsec:failure`, `subsec:theory`, `subsec:industrial`, `subsec:on_vs_off`.

## Narrative Quality Passes

Three rounds of narrative refinement ensure non-enumeration writing:
1. **5/7**: Initial integration of 9 new papers (TCOD/PAINT/PRISM/CoPD/MSD/IRIS/GUI-SD/MAD-OPD/Uni-OPD).
2. **5/7-5/8 10h loop**: language de-AI, wording de-duplication, narrative deepening, format normalization.
3. **5/8**: TT-OPD §5.3.1 and §7.2 rewritten to avoid ablation-dump "enumeration" pattern; positioned within agentic OPD granularity spectrum with cross-references to TCOD/Skill-SD/MAD-OPD/epistemic suppression.
