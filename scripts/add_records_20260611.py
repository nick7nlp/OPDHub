#!/usr/bin/env python3
"""
One-shot script: add 12 candidate OPD papers processed on 2026-06-11.
Run from survey root:
  python3 scripts/add_records_20260611.py
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

SURVEY_ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
NOTES_PATH = SURVEY_ROOT / "notes" / "paper_notes.json"
KNOWN_IDS_PATH = SURVEY_ROOT / "papers-meta" / "known_arxiv_ids.txt"
READ_DATE = "2026-06-11"

# ---------- helpers ----------

def unspec_ts():  # unspecified teacher/student pair placeholder
    return {
        "teacher": {"name": "unspecified", "family": "unspecified", "size_B": None,
                    "type": "dense", "moe_active_B": None, "is_self": False, "is_api_only": False},
        "student": {"name": "unspecified", "family": "unspecified", "size_B": None,
                    "type": "dense", "init_from": "unspecified", "is_self": False},
        "vocab_match": "shared",
        "scenario": "main",
    }

def base_setup():
    return {"compute_budget": "unspecified", "tokens_seen_B": None, "context_length": None,
            "rollout_batch_size": None, "kl_coeff": None, "rl_algorithm": "unspecified",
            "stabilization_tricks": []}

def no_openness():
    return {"code_url": None, "model_url": None, "data_url": None}

def no_theory():
    return {"has_convergence_proof": False, "has_bound": False, "notes": ""}

# ============================================================
# NEW RECORDS
# ============================================================
NEW_RECORDS = {

# ───────────────────────────────────────────────────────────
# 1. 2606.06712  OPDLM — §5.3.2  (YES)
# ───────────────────────────────────────────────────────────
"2606.06712": {
    "_schema_version": "v3",
    "paper_id": "2606.06712",
    "title": "Data-Efficient Autoregressive-to-Diffusion Language Models via On-Policy Distillation",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Xingyu Su",
    "affiliation_primary": "unspecified",
    "summary": "Self-distillation converts AR LM to diffusion LM; 15x-7000x fewer training tokens",
    "method": {
        "training_loop": (
            "Frozen original AR model serves as teacher. "
            "Bidirectional diffusion LM student generates its own on-policy trajectories. "
            "Self-distillation from frozen teacher guides student, eliminating train-inference mismatch."
        ),
        "loss_formulation": "L_OPDLM = KL(pi_student_diffusion(y|x) || pi_teacher_AR(y|x)) over on-policy student trajectories",
        "data_source": "unspecified",
        "key_components": [
            "Frozen AR teacher (original model)",
            "Bidirectional diffusion LM student",
            "On-policy trajectory generation for diffusion LM",
            "Self-distillation for knowledge retention",
            "Train-inference mismatch elimination",
        ],
    },
    "novelty": (
        "First application of on-policy self-distillation to AR→DLM conversion; "
        "eliminates the train-inference mismatch unique to diffusion generation and achieves "
        "15x–7000x data efficiency vs standard DLM pretraining."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "self",
        "evidence_quote": (
            "eliminates the train-inference mismatch in DLMs, "
            "while distillation from the original model enhances knowledge retention"
        ),
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§5.3.2",
        "secondary_sections": ["§8.2"],
        "reasoning": (
            "Student (diffusion LM) generates on-policy trajectories; frozen original AR model "
            "acts as self-teacher; distillation is the main training objective. "
            "Fits §5.3.2 (pure self-distillation, frozen-copy teacher)."
        ),
    },
    "teacher_student_pairs": [
        {
            "teacher": {"name": "Frozen AR LM (original)", "family": "unspecified", "size_B": None,
                        "type": "dense", "moe_active_B": None, "is_self": True, "is_api_only": False},
            "student": {"name": "Bidirectional Diffusion LM", "family": "unspecified", "size_B": None,
                        "type": "dense", "init_from": "base", "is_self": True},
            "vocab_match": "shared",
            "scenario": "main",
        }
    ],
    "training_setup": {**base_setup(), "rl_algorithm": "pure-KD"},
    "datasets": [],
    "benchmarks": [],
    "key_findings": [
        "15x to 7,000x fewer training tokens vs standard DLM pretraining across diverse tasks",
        "Eliminates train-inference mismatch that standard DLM training suffers from",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "",
    "openness": no_openness(),
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "yes", "score": 4,
        "rationale": "Directly applies on-policy self-distillation to AR→DLM conversion; data-efficiency framing highlights value of on-policy signal for diffusion generation.",
    },
    "comparable_papers": [],
    "score": 4,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 2. 2606.07082  Geometry of OPD — §7.1  (ANALYSIS)
# ───────────────────────────────────────────────────────────
"2606.07082": {
    "_schema_version": "v3",
    "paper_id": "2606.07082",
    "title": "On the Geometry of On-Policy Distillation",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Zhennan Shen",
    "affiliation_primary": "unspecified",
    "summary": "Geometry analysis of OPD: subspace locking in parameter-space trajectories",
    "method": {
        "training_loop": (
            "Analysis only: compare parameter-space trajectories of OPD, SFT, and RL training runs. "
            "Measure weight update magnitude, principal-direction avoidance, and rank of cumulative update subspace. "
            "Run control experiments with token sparsification and off-policy rollouts."
        ),
        "loss_formulation": "n/a (analysis paper)",
        "data_source": "unspecified",
        "key_components": [
            "Parameter-space trajectory analysis",
            "Subspace locking discovery",
            "OPD vs SFT vs RL comparison",
            "Token sparsification ablation",
            "Off-policy rollout control experiment",
        ],
    },
    "novelty": (
        "Discovers 'subspace locking' — cumulative OPD updates converge into a narrow "
        "low-dimensional channel early in training. OPD affects fewer weights and avoids "
        "principal directions more strongly than SFT/RL. Locked subspace hurts SFT but not OPD."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "external-teacher",
        "evidence_quote": "OPD updates affect fewer weights and avoid principal directions more strongly",
    },
    "opd_classification": {
        "is_opd": "analysis",
        "primary_section": "§7.1",
        "secondary_sections": ["§7.3"],
        "reasoning": (
            "Empirical geometry analysis of OPD parameter-space dynamics; no new training method. "
            "Subspace locking is an empirical finding that explains OPD's sample efficiency."
        ),
    },
    "teacher_student_pairs": [],
    "training_setup": {**base_setup(), "rl_algorithm": "n/a"},
    "datasets": [],
    "benchmarks": [],
    "key_findings": [
        "OPD updates affect fewer weights and avoid principal directions more strongly than SFT or RL",
        "Subspace locking: cumulative OPD updates converge into a narrow low-dimensional channel early in training",
        "Locked subspace maintains OPD performance but substantially degrades SFT results",
        "Token sparsification and off-policy rollout generation preserve rank dynamics",
        "Combining OPD with RL alters the rank dynamics, suggesting different update geometry",
    ],
    "ablations_summary": (
        "Token sparsification and off-policy rollout generation preserve rank dynamics; "
        "OPD+RL combination alters geometry, confirming OPD has its own update geometry."
    ),
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "",
    "openness": no_openness(),
    "theory": {"has_convergence_proof": False, "has_bound": False,
                "notes": "Geometric analysis of parameter-space trajectories; subspace locking theory."},
    "relevance_to_opd": {
        "is_opd": "analysis", "score": 5,
        "rationale": "Directly analyzes OPD geometry in parameter space; subspace locking discovery provides mechanistic understanding of why OPD differs from SFT and RL.",
    },
    "comparable_papers": [],
    "score": 5,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 3. 2606.09304  SG-OPD — §5.3.3  (YES)
# ───────────────────────────────────────────────────────────
"2606.09304": {
    "_schema_version": "v3",
    "paper_id": "2606.09304",
    "title": "SG-OPD: Sign-Gated On-Policy Distillation via Sign-Consistency Gating and Phased Teacher Sampling",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Haoran Xu",
    "affiliation_primary": "unspecified",
    "summary": "Sign-consistency gating + phased teacher sampling for verifier-guided OPD; +1.98/+7.50 on math",
    "method": {
        "training_loop": (
            "Phase 1 (init): phased teacher sampling calibrates the student's starting distribution. "
            "Phase 2 (training): student generates on-policy rollouts; "
            "binary verifier evaluates teacher trustworthiness at two granularities "
            "(per-sample, per-question); sign-consistency gate selectively applies "
            "distillation updates where gradient signs are consistent."
        ),
        "loss_formulation": (
            "L_SG-OPD = sum_t sign_gate(v_t) * KL(pi_student(y_t|x,y<t) || pi_teacher(y_t|x,y<t)); "
            "sign_gate(v) = 1 iff verifier trust signal v and gradient sign are consistent"
        ),
        "data_source": "mathematical reasoning benchmarks",
        "key_components": [
            "Binary verifier as teacher trust signal",
            "Sign-consistency gating",
            "Phased teacher sampling (initialization)",
            "Two-granularity trust evaluation (per-sample, per-question)",
        ],
    },
    "novelty": (
        "Uses gradient sign consistency + binary verifier to selectively gate teacher "
        "distillation updates, preventing noisy/incorrect teacher signals from corrupting "
        "student training. Phased initialization improves cold-start."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "external-teacher",
        "evidence_quote": "a binary verifier as a trust signal for the teacher at two complementary granularities",
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§5.3.3",
        "secondary_sections": ["§4.2"],
        "reasoning": (
            "Binary verifier provides external feedback to gate teacher trust in OPD; "
            "fits §5.3.3 (verifier-guided distillation). Sign-consistency gating is also "
            "adaptive weighting (§4.2)."
        ),
    },
    "teacher_student_pairs": [unspec_ts()],
    "training_setup": {
        **base_setup(),
        "stabilization_tricks": ["sign-consistency gating", "phased teacher sampling"],
    },
    "datasets": [],
    "benchmarks": [
        {"name": "math reasoning (per-sample level)", "metric": "avg gain over standard OPD",
         "student_baseline": None, "student_after_OPD": None, "delta": 1.98,
         "teacher_score": None, "gap_closed_pct": None, "is_main_result": True},
        {"name": "math reasoning (per-question level)", "metric": "avg gain over standard OPD",
         "student_baseline": None, "student_after_OPD": None, "delta": 7.50,
         "teacher_score": None, "gap_closed_pct": None, "is_main_result": True},
    ],
    "key_findings": [
        "Average gains of +1.98 (per-sample) and +7.50 (per-question) over standard OPD on math reasoning benchmarks",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "",
    "openness": no_openness(),
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "yes", "score": 4,
        "rationale": "Directly improves OPD by gating teacher signal via sign consistency and verifier trust; addresses teacher signal reliability in standard OPD.",
    },
    "comparable_papers": [],
    "score": 4,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 4. 2606.09348  PBSD — §5.3.1  (YES)
# ───────────────────────────────────────────────────────────
"2606.09348": {
    "_schema_version": "v3",
    "paper_id": "2606.09348",
    "title": "PBSD: Privileged Bayesian Self-Distillation for Long-Horizon Credit Assignment",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Yang Tian",
    "affiliation_primary": "unspecified",
    "summary": "Bayesian privileged self-distillation converts sparse trajectory rewards to turn-level credits",
    "method": {
        "training_loop": (
            "Student generates on-policy trajectories (standard RL loop). "
            "Compute Bayes-calibrated turn-level credit signal by comparing "
            "log pi(a_t|h_t, GT_answer) vs log pi(a_t|h_t) (with/without privileged answer). "
            "Dense turn-level rewards replace sparse trajectory-level outcome supervision "
            "for policy gradient update."
        ),
        "loss_formulation": (
            "r_turn(t) = log pi(a_t | h_t, GT_answer) - log pi(a_t | h_t); "
            "L_PBSD = -E_rollout[sum_t r_turn(t) * advantage(t)]"
        ),
        "data_source": "unspecified (multiple domains per abstract)",
        "key_components": [
            "Bayes-calibrated turn-level credit signal",
            "Model with vs without GT-answer conditioning",
            "Sparse-to-dense reward conversion",
            "Privileged information (GT answer) as self-teacher",
        ],
    },
    "novelty": (
        "Reframes the credit assignment problem as Bayesian inference: turn-level "
        "credit = likelihood ratio between answer-conditioned and unconditional model. "
        "Converts sparse outcome supervision to dense per-turn rewards without external verifier. "
        "Also transfers knowledge from shorter to longer contexts during inference."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "self",
        "signal_source": "PI(GT)",
        "evidence_quote": "transforms sparse outcome supervision into fine-grained intermediate rewards compatible with standard policy optimization",
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§5.3.1",
        "secondary_sections": ["§4.3"],
        "reasoning": (
            "Self-distillation where privileged info (GT answer) conditions the teacher "
            "distribution; Bayesian credit decomposition uses PI(GT) to provide dense "
            "supervision over student's on-policy rollouts. Fits §5.3.1."
        ),
    },
    "teacher_student_pairs": [
        {
            "teacher": {"name": "Same model w/ GT answer conditioning", "family": "unspecified",
                        "size_B": None, "type": "dense", "moe_active_B": None,
                        "is_self": True, "is_api_only": False},
            "student": {"name": "Same model w/o GT answer conditioning", "family": "unspecified",
                        "size_B": None, "type": "dense", "init_from": "unspecified", "is_self": True},
            "vocab_match": "shared",
            "scenario": "main",
        }
    ],
    "training_setup": base_setup(),
    "datasets": [],
    "benchmarks": [],
    "key_findings": [
        "Converts trajectory-level rewards into Bayes-calibrated turn-level credit signals",
        "Improvements across different domains and conditions per abstract",
        "Transfers knowledge from shorter to longer contexts during inference",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "",
    "openness": no_openness(),
    "theory": {"has_convergence_proof": False, "has_bound": False,
                "notes": "Bayesian formulation for credit assignment as likelihood ratio."},
    "relevance_to_opd": {
        "is_opd": "yes", "score": 4,
        "rationale": "Privileged Bayesian self-distillation for long-horizon RL; GT-answer conditioning provides dense per-turn teacher signal over student's own on-policy rollouts.",
    },
    "comparable_papers": [],
    "score": 4,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 5. 2606.10385  AR-OPD — §5.3.1  (YES)
# ───────────────────────────────────────────────────────────
"2606.10385": {
    "_schema_version": "v3",
    "paper_id": "2606.10385",
    "title": "Beyond Absolute Imitation: Anchored Residual Guidance for Privileged On-Policy Distillation",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Wenhao Zhang",
    "affiliation_primary": "unspecified",
    "summary": "AR-OPD: anchor + oracle residual splits privileged signal to prevent hindsight leakage",
    "method": {
        "training_loop": (
            "Student generates on-policy rollouts. "
            "Oracle privileged signal decomposed into: "
            "(1) locally-achievable anchor target (no hindsight required), "
            "(2) oracle foresight as controlled residual adjustment. "
            "L = L_anchor(rollout, anchor) + alpha * L_residual(rollout, oracle_foresight). "
            "Prevents student from learning locally-unsupported shortcuts."
        ),
        "loss_formulation": (
            "L_AR-OPD = L_imitation(student_rollout, anchor) + alpha * delta_guidance(oracle_foresight); "
            "anchor = locally achievable sub-target; oracle_foresight = residual oracle signal"
        ),
        "data_source": "unspecified",
        "key_components": [
            "Anchored residual decomposition of oracle signal",
            "Locally-achievable anchor target",
            "Oracle foresight as controlled residual",
            "Hindsight leakage reduction",
        ],
    },
    "novelty": (
        "Identifies that treating oracle as single imitation target causes students to learn "
        "locally-unsupported shortcuts (hindsight leakage). AR-OPD decomposes oracle supervision "
        "into anchor + residual, enabling oracle guidance without shortcuts."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "PI(GT)",
        "evidence_quote": "students to learn locally unsupported shortcuts rather than valid reasoning steps",
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§5.3.1",
        "secondary_sections": [],
        "reasoning": (
            "Addresses hindsight leakage in privileged on-policy distillation; oracle/GT "
            "info is the privileged teacher signal; anchored residual decomposition is a "
            "principled improvement to §5.3.1 PI-OPD methods."
        ),
    },
    "teacher_student_pairs": [
        {
            "teacher": {"name": "Oracle (privileged GT)", "family": "unspecified",
                        "size_B": None, "type": "dense", "moe_active_B": None,
                        "is_self": True, "is_api_only": False},
            "student": {"name": "Student model", "family": "unspecified",
                        "size_B": None, "type": "dense", "init_from": "unspecified", "is_self": True},
            "vocab_match": "shared",
            "scenario": "main",
        }
    ],
    "training_setup": base_setup(),
    "datasets": [],
    "benchmarks": [
        {"name": "unspecified reasoning benchmark", "metric": "accuracy",
         "student_baseline": None, "student_after_OPD": None, "delta": 2.3,
         "teacher_score": None, "gap_closed_pct": None, "is_main_result": True,
         "_note": "+2.3 over full privileged OPD"},
        {"name": "unspecified reasoning benchmark", "metric": "vs SFT baseline",
         "student_baseline": None, "student_after_OPD": None, "delta": 7.9,
         "teacher_score": None, "gap_closed_pct": None, "is_main_result": True,
         "_note": "+7.9 vs supervised fine-tuning"},
        {"name": "long-horizon trajectories >768 tokens", "metric": "accuracy",
         "student_baseline": None, "student_after_OPD": None, "delta": 7.2,
         "teacher_score": None, "gap_closed_pct": None, "is_main_result": True},
    ],
    "key_findings": [
        "+2.3 points over full privileged OPD (absolute imitation baseline)",
        "+7.9 points vs supervised fine-tuning",
        "Reduced hindsight leakage by 21.7%",
        "+7.2-point advantage on long-horizon trajectories exceeding 768 tokens",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": ["Absolute imitation causes locally-unsupported shortcuts and hindsight leakage"],
    "compute_efficiency": "",
    "openness": no_openness(),
    "theory": {"has_convergence_proof": False, "has_bound": False,
                "notes": "Hindsight leakage analysis; anchor decomposition principle."},
    "relevance_to_opd": {
        "is_opd": "yes", "score": 5,
        "rationale": "Principled decomposition of oracle signal in privileged OPD; identifies and quantifies hindsight leakage (21.7% reduction); strong results on long-horizon tasks.",
    },
    "comparable_papers": [],
    "score": 5,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 6. 2606.07000  PTD-PO — §5.3.1  (YES)
# ───────────────────────────────────────────────────────────
"2606.07000": {
    "_schema_version": "v3",
    "paper_id": "2606.07000",
    "title": "Teaching the Way, Not the Answer: Privileged Tutoring Distillation for Multimodal Policy Optimization",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Shizhe Xiang",
    "affiliation_primary": "unspecified",
    "summary": "Top-K JSD privileged tutoring with spatial+reasoning hints for multimodal policy optimization",
    "method": {
        "training_loop": (
            "Teacher (with privileged info) constructs structured hints: "
            "spatial attention guidance + intermediate textual reasoning steps (no final answer exposed). "
            "Student LVLM generates on-policy rollouts; "
            "Top-K Jensen-Shannon divergence objective aligns student to privileged teacher distribution "
            "while preventing entropy collapse."
        ),
        "loss_formulation": (
            "L_PTD = Top-K JSD(pi_student || pi_teacher_privileged); "
            "Top-K selects K most informative tokens for divergence computation"
        ),
        "data_source": "multimodal reasoning datasets (2B-8B parameter VLMs)",
        "key_components": [
            "Structured privileged hints (spatial attention + intermediate reasoning steps)",
            "No answer exposure to student policy",
            "Top-K Jensen-Shannon divergence objective",
            "Entropy collapse prevention",
            "2B-8B LVLM evaluation",
        ],
    },
    "novelty": (
        "Constructs privileged hints from spatial attention and intermediate reasoning steps "
        "without exposing the final answer, enabling richer supervision than standard RLVR "
        "while avoiding answer-leakage of full privileged OPD. Top-K JSD stabilizes training."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "PI(reference)",
        "evidence_quote": "dense guidance without exposing the answer to the student policy",
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§5.3.1",
        "secondary_sections": ["§4.1"],
        "reasoning": (
            "Privileged teacher provides structured hints (spatial attention + reasoning steps) "
            "without answer leakage; student optimized on-policy via Top-K JSD. "
            "§5.3.1 (privileged info) primary; §4.1 (new divergence: Top-K JSD) secondary."
        ),
    },
    "teacher_student_pairs": [
        {
            "teacher": {"name": "Privileged LVLM teacher", "family": "unspecified",
                        "size_B": None, "type": "dense", "moe_active_B": None,
                        "is_self": True, "is_api_only": False},
            "student": {"name": "LVLM student (2B-8B)", "family": "unspecified",
                        "size_B": None, "type": "dense", "init_from": "unspecified", "is_self": True},
            "vocab_match": "shared",
            "scenario": "main",
        }
    ],
    "training_setup": base_setup(),
    "datasets": [],
    "benchmarks": [
        {"name": "multimodal reasoning (various)", "metric": "vs RLVR and distillation baselines",
         "student_baseline": None, "student_after_OPD": None, "delta": None,
         "teacher_score": None, "gap_closed_pct": None, "is_main_result": True,
         "_note": "consistently outperforms RLVR and distillation baselines across 2B-8B models"},
    ],
    "key_findings": [
        "Consistently outperforms RLVR and distillation baselines across 2B to 8B parameter models",
        "Top-K JSD objective stabilizes training and reduces computational demands",
        "Structured privileged hints provide richer signal than RLVR without answer leakage",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "",
    "openness": no_openness(),
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "yes", "score": 4,
        "rationale": "Multimodal privileged OPD with structured hints; Top-K JSD is a novel divergence for distillation; demonstrates on-policy privileged training across 2B-8B VLMs.",
    },
    "comparable_papers": [],
    "score": 4,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 7. 2606.07006  RASFT — §4.2  (YES)
# ───────────────────────────────────────────────────────────
"2606.07006": {
    "_schema_version": "v3",
    "paper_id": "2606.07006",
    "title": "RASFT: Rollout-Adaptive Supervised Fine-Tuning for Reasoning",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Yongliang Miao",
    "affiliation_primary": "unspecified",
    "summary": "Rollout-adaptive SFT: expert guidance when struggling; own solutions + KL when competent",
    "method": {
        "training_loop": (
            "Generate on-policy rollouts to assess model competence per problem. "
            "If model struggles: strengthen SFT signal from expert demonstrations. "
            "If model shows competent reasoning: incorporate own correct solutions "
            "while constraining drift from reference model via KL penalty. "
            "Adaptive weighting interpolates between regimes."
        ),
        "loss_formulation": (
            "L_RASFT = alpha(competence) * L_expert_SFT + "
            "(1 - alpha(competence)) * [L_self_rollout + beta * KL(pi_student || pi_ref)]; "
            "alpha(competence) is high when model struggles, low when competent"
        ),
        "data_source": "mathematical and code reasoning benchmarks",
        "key_components": [
            "Rollout-based competence assessment",
            "Adaptive interpolation between expert-guided SFT and self-rollout training",
            "KL constraint to reference model",
            "Curriculum that transitions with model competence",
        ],
    },
    "novelty": (
        "Adaptive distillation curriculum that transitions from expert-guided SFT "
        "to own-rollout training based on model competence, combining advantages of "
        "teacher guidance (when needed) and on-policy self-improvement (when capable)."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "external-teacher",
        "evidence_quote": "dynamically adjusts expert guidance based on how well the current model performs on each problem",
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§4.2",
        "secondary_sections": ["§6.2"],
        "reasoning": (
            "Adaptive distillation that weights teacher guidance vs self-rollout based on "
            "competence assessment; rollout-based curriculum is §4.2 (adaptive divergence/curriculum) "
            "with §6.2 secondary (scheduling/curriculum tricks)."
        ),
    },
    "teacher_student_pairs": [
        {
            "teacher": {"name": "Expert model (demonstrations)", "family": "unspecified",
                        "size_B": None, "type": "dense", "moe_active_B": None,
                        "is_self": False, "is_api_only": False},
            "student": {"name": "Reasoning student", "family": "unspecified",
                        "size_B": None, "type": "dense", "init_from": "unspecified", "is_self": False},
            "vocab_match": "shared",
            "scenario": "main",
        }
    ],
    "training_setup": {
        **base_setup(),
        "stabilization_tricks": ["KL constraint to reference model", "rollout-based competence assessment"],
    },
    "datasets": [],
    "benchmarks": [],
    "key_findings": [
        "Outperforms conventional SFT and RL baselines on math and code reasoning",
        "Adaptive curriculum transitions smoothly from expert guidance to self-rollout training",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "",
    "openness": {"code_url": "public (no URL in abstract)", "model_url": None, "data_url": None},
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "yes", "score": 4,
        "rationale": "Adaptive OPD curriculum that combines expert teacher guidance with own on-policy rollouts based on competence; directly addresses the explore-exploit tradeoff in OPD.",
    },
    "comparable_papers": [],
    "score": 4,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 8. 2606.08432  TRD — §6.2  (YES)
# ───────────────────────────────────────────────────────────
"2606.08432": {
    "_schema_version": "v3",
    "paper_id": "2606.08432",
    "title": "Trajectory-Refined Distillation",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Li Jiang",
    "affiliation_primary": "unspecified",
    "summary": "Trajectory-level distillation corrects prefix-failure fragmented gradients via teacher guidance",
    "method": {
        "training_loop": (
            "Standard on-policy distillation loop. "
            "Identify 'prefix failure' states where student output is problematic, "
            "causing fragmented gradients that token-level interventions cannot fix. "
            "Teacher corrects problematic student trajectory prefixes at the trajectory level. "
            "Recompute distillation loss on teacher-refined trajectories. "
            "Expose students to alternative valid reasoning paths from teacher corrections."
        ),
        "loss_formulation": (
            "L_TRD = L_distill(student | teacher-refined-trajectory); "
            "trajectory refinement: teacher corrects prefix failures in student rollouts"
        ),
        "data_source": "unspecified (multiple benchmarks and model sizes)",
        "key_components": [
            "Prefix failure detection",
            "Trajectory-level teacher correction",
            "On-policy alignment maintenance",
            "Alternative reasoning path exposure",
        ],
    },
    "novelty": (
        "Identifies 'prefix failure' — a trajectory-level error mode in OPD causing "
        "fragmented gradients that token-level fixes cannot address. "
        "TRD corrects failures at the trajectory level via teacher guidance while "
        "maintaining on-policy alignment. Works for both standard OPD and self-distillation."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "external-teacher",
        "evidence_quote": "corrects problematic student outputs using teacher guidance while maintaining on-policy alignment",
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§6.2",
        "secondary_sections": ["§7.2"],
        "reasoning": (
            "Trajectory-level correction is a training stabilization/efficiency technique for OPD; "
            "prefix failure analysis is a failure mode diagnostic (§7.2 secondary)."
        ),
    },
    "teacher_student_pairs": [unspec_ts()],
    "training_setup": {
        **base_setup(),
        "stabilization_tricks": ["trajectory-level prefix correction", "teacher-guided rollout refinement"],
    },
    "datasets": [],
    "benchmarks": [],
    "key_findings": [
        "Prefix failure causes fragmented gradients that token-level interventions cannot resolve",
        "Trajectory-level correction improves accuracy and reasoning breadth across benchmarks and model sizes",
        "Works for both standard on-policy distillation and self-distillation variants",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": ["Prefix failure: fragmented gradients from problematic trajectory prefixes"],
    "compute_efficiency": "",
    "openness": {"code_url": "public GitHub (no URL in abstract)", "model_url": None, "data_url": None},
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "yes", "score": 4,
        "rationale": "Addresses a specific OPD failure mode (prefix failure) with trajectory-level correction; applies to both standard and self-distillation OPD settings.",
    },
    "comparable_papers": [],
    "score": 4,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 9. 2606.09091  GNDPO — §4.2  (YES)
# ───────────────────────────────────────────────────────────
"2606.09091": {
    "_schema_version": "v3",
    "paper_id": "2606.09091",
    "title": "Stabilizing On-Policy Distillation for MLLM Reasoning with Global Normalization",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Dongze Hao",
    "affiliation_primary": "unspecified",
    "summary": "Global KL normalization to batch-relative advantages stabilizes OPD gradient magnitudes",
    "method": {
        "training_loop": (
            "Standard on-policy KL distillation loop for MLLM. "
            "Compute per-token KL(student || teacher). "
            "Normalize raw KL values to batch-relative advantage scores "
            "(subtract batch mean, divide by batch std). "
            "Use normalized KL advantages as distillation signal to prevent gradient explosion "
            "while preserving fine-grained token-level instruction."
        ),
        "loss_formulation": (
            "L_GNDPO = -sum_t normalize_batch(KL_t) * gradient_signal; "
            "normalize_batch(KL_t) = (KL_t - mu_batch) / sigma_batch"
        ),
        "data_source": "multimodal reasoning datasets",
        "key_components": [
            "Per-token KL computation",
            "Batch-relative normalization of KL values",
            "Gradient explosion prevention",
            "Fine-grained distillation signal preservation",
        ],
    },
    "novelty": (
        "Identifies that token-level KL distillation causes gradient instability due to "
        "misaligned magnitudes across states. Global normalization of KL to batch-relative "
        "advantages (analogous to GRPO advantage normalization) resolves this without "
        "losing fine-grained token-level supervision."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "external-teacher",
        "evidence_quote": "transforms raw KL measurements into batch-relative advantage scores",
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§4.2",
        "secondary_sections": ["§6"],
        "reasoning": (
            "Normalization of KL signal to batch-relative advantages is an adaptive "
            "modification of the distillation divergence (§4.2); primary motivation is "
            "stabilization (§6 secondary)."
        ),
    },
    "teacher_student_pairs": [unspec_ts()],
    "training_setup": {
        **base_setup(),
        "stabilization_tricks": ["global batch normalization of KL values", "batch-relative advantage scaling"],
    },
    "datasets": [],
    "benchmarks": [],
    "key_findings": [
        "Token-level KL distillation causes gradient explosion due to misaligned magnitudes",
        "Global normalization to batch-relative advantages resolves instability",
        "Improved training stability and performance on multimodal reasoning tasks",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": ["Gradient explosion from misaligned token-level KL magnitudes in standard OPD"],
    "compute_efficiency": "",
    "openness": {"code_url": "public GitHub (no URL in abstract)", "model_url": None, "data_url": None},
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "yes", "score": 4,
        "rationale": "Directly stabilizes on-policy KL distillation for MLLMs via global normalization; addresses a known instability in token-level OPD that limits its application to multimodal tasks.",
    },
    "comparable_papers": [],
    "score": 4,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 10. 2606.09456  Cross-Tokenizer OPD — §5.1  (YES)
# ───────────────────────────────────────────────────────────
"2606.09456": {
    "_schema_version": "v3",
    "paper_id": "2606.09456",
    "title": "Breaking the Tokenizer Barrier: On-Policy Distillation across Model Families",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Yifan Niu",
    "affiliation_primary": "unspecified",
    "summary": "Token-mapping enables on-policy distillation across model families with different tokenizers",
    "method": {
        "training_loop": (
            "Student (family A) generates on-policy rollouts. "
            "Token-mapping algorithm aligns teacher (family B) token probabilities "
            "to student vocabulary space, preserving signal fidelity across tokenizers. "
            "Compute cross-tokenizer KL distillation loss. "
            "Significantly more compute-efficient than baselines."
        ),
        "loss_formulation": (
            "L_cross-tok = KL(pi_student(y) || T(pi_teacher(y'))); "
            "T = token-mapping function aligning teacher vocabulary to student vocabulary"
        ),
        "data_source": "unspecified",
        "key_components": [
            "Token-mapping algorithm (cross-tokenizer alignment)",
            "Signal fidelity preservation across vocabularies",
            "Cross-family teacher-student OPD",
            "Compute efficiency over baselines",
        ],
    },
    "novelty": (
        "Removes the same-tokenizer constraint in OPD, enabling cross-family teacher-student "
        "pairs (e.g., LLaMA → Qwen) through a token-mapping algorithm. Opens new teacher-student "
        "pairings and is significantly more compute-efficient than alternatives."
    ),
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "logits",
        "signal_source": "external-teacher",
        "evidence_quote": "teacher and student models to share the same tokenizer",
    },
    "opd_classification": {
        "is_opd": "yes",
        "primary_section": "§5.1",
        "secondary_sections": ["§5.2"],
        "reasoning": (
            "White-box teacher logit supervision across different tokenizer families; "
            "cross-tokenizer token-mapping is the technical contribution enabling §5.1 "
            "across model families. §5.2 secondary as the constraint resembles API-constrained scenario."
        ),
    },
    "teacher_student_pairs": [
        {
            "teacher": {"name": "Cross-family teacher (family B)", "family": "unspecified",
                        "size_B": None, "type": "dense", "moe_active_B": None,
                        "is_self": False, "is_api_only": False},
            "student": {"name": "Cross-family student (family A)", "family": "unspecified",
                        "size_B": None, "type": "dense", "init_from": "unspecified", "is_self": False},
            "vocab_match": "cross-tokenizer",
            "scenario": "main",
        }
    ],
    "training_setup": {
        **base_setup(),
        "stabilization_tricks": ["cross-tokenizer token-mapping"],
    },
    "datasets": [],
    "benchmarks": [],
    "key_findings": [
        "Token-mapping algorithm preserves distillation signal fidelity across different tokenizers",
        "Significantly more compute-efficient than baselines for cross-family OPD",
        "Enables new teacher-student pairings previously impossible due to tokenizer mismatch",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "significantly more compute-efficient than baselines (per abstract)",
    "openness": no_openness(),
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "yes", "score": 5,
        "rationale": "Removes a fundamental barrier in OPD (same-tokenizer requirement) via cross-tokenizer token-mapping; enables cross-family distillation with compute efficiency gains.",
    },
    "comparable_papers": [],
    "score": 5,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 11. 2606.06840  Characterize Then Distill — EDGE
# ───────────────────────────────────────────────────────────
"2606.06840": {
    "_schema_version": "v3",
    "paper_id": "2606.06840",
    "title": "Characterize Then Distill: Mechanistic Reasoning in Large Output Spaces",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Debjyoti Saha Roy",
    "affiliation_primary": "unspecified",
    "summary": "Characterize multi-label reasoning phases (shortlisting + refinement) to guide distillation",
    "method": {
        "training_loop": "Offline distillation: characterize reasoning into two separable phases (shortlisting, refinement); leverage phase characterization to create improved distillation strategy.",
        "loss_formulation": "unspecified (phase-aware distillation, no on-policy rollouts described)",
        "data_source": "multi-label reasoning datasets",
        "key_components": [
            "Two-phase reasoning characterization (shortlisting + refinement)",
            "Phase-aware distillation strategy",
        ],
    },
    "novelty": "Identifies two separable reasoning phases in multi-label selection and exploits the separation to guide distillation.",
    "on_policy_mechanism": {
        "student_rollout_in_training": "no",
        "rollout_frequency": "n/a",
        "teacher_signal": "logits",
        "signal_source": "external-teacher",
        "evidence_quote": "consistently outperforms standard distillation",
    },
    "opd_classification": {
        "is_opd": "edge",
        "primary_section": "§5.1",
        "_manual_audit_note": (
            "No on-policy student rollouts mentioned; appears to be offline/static distillation "
            "of reasoning phases. OPD condition 1 (student generates rollouts on-policy) is not satisfied. "
            "Rejected as OPD; relevant to distillation literature broadly."
        ),
    },
    "teacher_student_pairs": [],
    "training_setup": base_setup(),
    "datasets": [],
    "benchmarks": [],
    "key_findings": ["Consistently outperforms standard distillation on multi-label tasks"],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "",
    "openness": no_openness(),
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "edge", "score": 2,
        "rationale": "Offline distillation of reasoning phase structure; no on-policy rollouts from student.",
    },
    "comparable_papers": [],
    "score": 2,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

# ───────────────────────────────────────────────────────────
# 12. 2606.09871  SD-GRPO — EDGE
# ───────────────────────────────────────────────────────────
"2606.09871": {
    "_schema_version": "v3",
    "paper_id": "2606.09871",
    "title": "SD-GRPO: Verifiable Segment Decomposition for Long-Form Vision-Language Generation",
    "venue": "arXiv 2026",
    "year": 2026,
    "authors_first": "Hyunwoong Kim",
    "affiliation_primary": "unspecified",
    "summary": "Segment-decomposed GRPO with per-segment verifiable rewards for long-form VLM generation",
    "method": {
        "training_loop": "GRPO with per-segment verifiable rewards; processes per-segment rewards across rollout group yielding vector of per-segment advantages; no teacher distribution used.",
        "loss_formulation": "L_SD-GRPO = GRPO(per-segment advantages); no teacher KL term",
        "data_source": "multi-panel captioning, multi-chart QA, scientific figure captioning",
        "key_components": [
            "Segment decomposition of long-form outputs",
            "Per-segment verifiable rewards",
            "Vector of per-segment advantages",
            "GRPO optimization",
        ],
    },
    "novelty": "Decomposes long-form VLM outputs into verifiable segments for per-segment GRPO reward, addressing the scalar reward limitation for multi-segment outputs.",
    "on_policy_mechanism": {
        "student_rollout_in_training": "yes",
        "rollout_frequency": "per-outer-iter",
        "teacher_signal": "none",
        "signal_source": "verifier-RLVR",
        "evidence_quote": "per-segment rewards across the rollout group, yielding a vector of per-segment advantages",
    },
    "opd_classification": {
        "is_opd": "edge",
        "primary_section": "§4.3",
        "_manual_audit_note": (
            "Pure RLVR/GRPO with verifiable segment rewards; no teacher distribution providing "
            "distillation signal. OPD condition 2 (teacher supervision) is not satisfied. "
            "Uses on-policy rollouts but distillation objective is absent. Classified as edge (RLVR)."
        ),
    },
    "teacher_student_pairs": [],
    "training_setup": {**base_setup(), "rl_algorithm": "GRPO"},
    "datasets": [],
    "benchmarks": [],
    "key_findings": [
        "Per-segment GRPO advantages improve long-form VLM generation over single-scalar GRPO",
        "Compatible with other GRPO frameworks with minimal implementation complexity",
    ],
    "ablations_summary": "unspecified (abstract-only read)",
    "limitations": "unspecified (abstract-only read)",
    "failure_modes": [],
    "compute_efficiency": "",
    "openness": no_openness(),
    "theory": no_theory(),
    "relevance_to_opd": {
        "is_opd": "edge", "score": 2,
        "rationale": "Pure RLVR with segment decomposition; no teacher distribution; fails OPD condition 2.",
    },
    "comparable_papers": [],
    "score": 2,
    "_success": True, "_read_date": READ_DATE, "_attempts": 1,
},

}  # end NEW_RECORDS


# ============================================================
# MAIN: backup → load → update → save
# ============================================================
def main():
    # 1. Backup
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = NOTES_PATH.parent / f"paper_notes.json.bak-{ts}"
    shutil.copy2(NOTES_PATH, backup_path)
    print(f"✓ Backed up to {backup_path}")

    # 2. Load
    with open(NOTES_PATH) as f:
        db = json.load(f)
    notes = db["notes"]
    print(f"  Existing records: {len(notes)}")

    # 3. Check for conflicts
    conflicts = [aid for aid in NEW_RECORDS if aid in notes]
    if conflicts:
        print(f"⚠️  Already present (will overwrite): {conflicts}")

    # 4. Update
    for aid, rec in NEW_RECORDS.items():
        notes[aid] = rec

    db["last_updated"] = f"{READ_DATE}T00:00:00Z"

    # 5. Save
    with open(NOTES_PATH, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved {len(NEW_RECORDS)} new records → {NOTES_PATH}")
    print(f"  New total: {len(notes)} records")

    # 6. Update known_arxiv_ids.txt
    existing_ids = set(KNOWN_IDS_PATH.read_text().splitlines())
    new_ids = [aid for aid in NEW_RECORDS if aid not in existing_ids]
    if new_ids:
        with open(KNOWN_IDS_PATH, "a") as f:
            for aid in sorted(new_ids):
                f.write(aid + "\n")
        print(f"✓ Added {len(new_ids)} IDs to known_arxiv_ids.txt: {new_ids}")
    else:
        print("  All IDs already in known_arxiv_ids.txt")

    # 7. Print summary
    yes_papers = [(aid, r) for aid, r in NEW_RECORDS.items()
                  if r["opd_classification"]["is_opd"] in ("yes", "analysis")]
    edge_papers = [(aid, r) for aid, r in NEW_RECORDS.items()
                   if r["opd_classification"]["is_opd"] == "edge"]
    print(f"\n── Summary ──")
    print(f"  YES/ANALYSIS: {len(yes_papers)}")
    for aid, r in yes_papers:
        sec = r["opd_classification"]["primary_section"]
        print(f"    {aid}  {sec}  {r['title'][:60]}")
    print(f"  EDGE: {len(edge_papers)}")
    for aid, r in edge_papers:
        print(f"    {aid}  {r['title'][:60]}")


if __name__ == "__main__":
    main()
