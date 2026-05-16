#!/usr/bin/env python3
"""
Generate Teacher × Student Model Atlas Heatmap for Awesome-OPD GitHub repo.

Usage:
    python3 generate_model_atlas.py [--output PATH]

Data source: Table 3 of OPD Survey V3 (latex-v3/main.tex)
Output: model-atlas-heatmap.png + .pdf

Style spec (matching v9 final from 5/13):
- 150 DPI, ~10K px resolution
- Font: TeX Gyre Termes (Times, matches COLM 2026 template)
- Family-grouped sorting with thick separator lines
- All-black cell numbers, large fonts (46-50pt)
- Legend in single full-width row
- Zero-overlap design (no overlapping annotations)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
from collections import defaultdict
import argparse
import os

# ===== CONFIGURATION =====
DPI = 250
CELL_SIZE = 1.0  # inches per cell
FONT_TICK = 46
FONT_CELL = 44
FONT_TITLE = 48
FONT_LEGEND = 30
FONT_MARGIN = 36

# ===== TEACHER-STUDENT PAIR DATA =====
# Extracted from Table 3 of OPD Survey V3 (latex-v3/main.tex)
# Format: (method, teacher_raw, student_raw)
# One entry per unique (teacher, student) pair in the table

RAW_PAIRS = [
    # Mathematical Reasoning
    ("G-OPD", "Qwen3-30B-A3B-Instruct", "Qwen3-1.7B"),
    ("G-OPD", "Qwen3-30B-A3B-Instruct", "Qwen3-4B"),
    ("OPSD", "Self", "Qwen3-1.7B"),
    ("OPSD", "Self", "Qwen3-4B"),
    ("OPSD", "Self", "Qwen3-8B"),
    ("PACED", "Qwen3-14B", "Qwen3-8B"),
    ("KDRL", "Skywork-OR1-Math-7B", "R1-Distill-Qwen-1.5B"),
    ("LUFFY", "DeepSeek-R1", "Qwen2.5-Math-7B"),
    ("LUFFY", "DeepSeek-R1", "Qwen2.5-Math-1.5B"),
    ("AOPD", "Qwen2.5-Math-7B", "Qwen2.5-Math-1.5B"),
    ("AOPD", "Qwen2.5-Math-7B", "Qwen2.5-Math-7B"),
    ("vOPD", "Self", "Qwen3-1.7B"),
    ("vOPD", "Self", "Qwen3-4B"),
    ("vOPD", "Self", "OLMo-3-7B"),

    # Instruction Following & General
    ("GKD", "T5-XL", "T5-Small"),
    ("GKD", "T5-XL", "T5-Base"),
    ("DistiLLM", "GPT-2 XL", "GPT-2"),
    ("AlignDistil", "Self", "Qwen2.5-1.5B"),

    # Industrial Scale
    ("Qwen3", "Qwen3-32B", "Qwen3-0.6B"),
    ("Qwen3", "Qwen3-32B", "Qwen3-1.7B"),
    ("Qwen3", "Qwen3-32B", "Qwen3-4B"),
    ("Qwen3", "Qwen3-32B", "Qwen3-8B"),
    ("Qwen3", "Qwen3-32B", "Qwen3-14B"),
    ("Qwen3", "Qwen3-235B-A22B", "Qwen3-0.6B"),
    ("Qwen3", "Qwen3-235B-A22B", "Qwen3-1.7B"),
    ("Qwen3", "Qwen3-235B-A22B", "Qwen3-4B"),
    ("Qwen3", "Qwen3-235B-A22B", "Qwen3-8B"),
    ("Qwen3", "Qwen3-235B-A22B", "Qwen3-14B"),
    ("Gemma 2", "Gemma-2-27B", "Gemma-2-9B"),
    ("Gemma 2", "Gemma-2-27B", "Gemma-2-2B"),
    ("MiMo-V2", "Domain specialists", "MiMo-V2-Flash"),
    ("KAT-Coder-V2", "5 domain specialists", "Unified agentic coder"),
    ("Nemotron-Cascade 2", "Domain RL/SFT teachers", "Nemotron-30B-MoE"),
    ("DeepSeek-V4", "10+ domain experts", "DeepSeek-V4-Pro"),
    ("ORBIT", "Multi-mode RL experts", "DeepSeek-R1-Distill-Qwen-1.5B"),
    ("ORBIT", "Multi-mode RL experts", "Qwen3-4B"),
    ("ORBIT", "Multi-mode RL experts", "Openmath-Nemotron-7B"),

    # Multimodal & Domain-Specific
    ("SCoRe", "Qwen2.5-72B", "Qwen2.5-7B"),
    ("SCoRe", "Qwen2.5-72B", "Qwen2.5-3B"),
    ("SCoRe", "Qwen2.5-72B", "Llama-3.1-8B"),
    ("VOLD", "Qwen3-8B", "Qwen2.5-VL-3B"),
    ("CORD", "Self (text-mode)", "Self (audio-mode)"),
    ("SKD", "Gemma-7B-IT", "Gemma-2B"),
    ("SKD", "Qwen2-7B", "Qwen2-0.5B"),
    ("ULD", "Llama-2-7B", "OPT-350M"),
    ("ULD", "Llama-2-7B", "Pythia-160M"),
    ("ULD", "Llama-2-7B", "Pythia-1B"),
    ("ULD", "Mistral-7B", "OPT-350M"),
    ("ULD", "Mistral-7B", "Pythia-160M"),
    ("ULD", "Mistral-7B", "Pythia-1B"),
    ("DP-OPD", "GPT-2 Large", "DistilGPT-2"),
    ("Veto", "Qwen2-7B-IT", "Qwen2-0.5B-IT"),
    ("TAID", "Phi-3-mini", "TinyLlama-1.1B"),
    ("TAID", "Llama-2-7B", "TinyLlama-1.1B"),
    ("GUI-SD", "Self", "Qwen3-VL-8B"),
    ("MAD-OPD", "Multi-teacher debate", "Qwen3-1.7B"),
    ("MAD-OPD", "Multi-teacher debate", "Qwen3-4B"),
    ("MAD-OPD", "Multi-teacher debate", "Qwen3-8B"),
    ("MAD-OPD", "Multi-teacher debate", "Qwen3-14B"),
    ("MSD", "Self", "Qwen2.5-7B"),
    ("MSD", "Self", "Llama-3-8B"),
    ("NPD", "Teacher", "openPangu-Embedded-1B"),
    ("SimCT", "Qwen2.5-7B", "Phi-4-mini"),
    ("SimCT", "Phi-4-mini", "Gemma-2-2B-IT"),
    ("Prune-OPD", "R1-Distill-Qwen-7B", "R1-Distill-Qwen-1.5B"),
    ("Prune-OPD", "Qwen3-4B", "Qwen3-1.7B"),
    ("SOD", "Qwen3-4B", "Qwen3-0.6B"),
    ("SOD", "Qwen3-4B", "Qwen3-1.7B"),
    ("LiteGUI", "Qwen3-VL-32B", "2B-3B scale agents"),
    ("Flow-OPD", "GRPO specialists (SD3.5)", "SD 3.5 Medium"),
    ("VISD", "Self", "VideoLLM"),
    ("Uni-OPD", "Multi-teacher", "Qwen3-1.7B"),
    ("Uni-OPD", "Multi-teacher", "Qwen3-4B"),
    ("Uni-OPD", "Multi-teacher", "Qwen3-VL-4B"),

    # Self-Distillation
    ("CRISP", "Self", "Qwen3-8B"),
    ("CRISP", "Self", "Qwen3-14B"),
    ("SD-ZERO", "Self", "Qwen3-4B"),
    ("SD-ZERO", "Self", "OLMo-3-7B"),
    ("π-Play", "Self", "Qwen3-4B"),
    ("π-Play", "Self", "Qwen3-8B"),
    ("SSD", "Self", "Qwen3-30B"),
    ("UniSD", "Self", "Qwen2.5-7B"),
    ("UniSD", "Self", "Qwen2.5-0.5B"),
    ("UniSD", "Self", "Qwen2.5-3B"),
    ("UniSD", "Self", "Llama-3.1-8B"),
    ("UniSD", "Self", "Gemma-3-4B"),
    ("SDPO", "Self", "Qwen3-8B"),
    ("SRPO", "Self", "Qwen3-8B"),
    ("PBSD", "Self", "Qwen3-1.7B"),
    ("PBSD", "Self", "Qwen3-4B"),
    ("PBSD", "Self", "Qwen3-8B"),
    ("TT-OPD", "Self", "Qwen3.5-9B"),
    ("OPSD-Compresses", "Self", "Qwen3-8B"),
    ("OPSD-Compresses", "Self", "R1-Distill-7B"),
    ("OPSD-Compresses", "Self", "AceReason-7B"),

    # Black-Box
    ("GAD", "GPT-5-Chat", "Qwen2.5-14B"),
    ("Lion", "ChatGPT", "LLaMA-7B"),
    ("Lion", "ChatGPT", "LLaMA-13B"),
    ("OVD", "QwQ-32B", "Qwen2.5-3B"),
    ("OVD", "QwQ-32B", "Llama-3.2-3B"),
    ("ROPD", "GPT-5.2", "Qwen3-4B"),
    ("ROPD", "GPT-5.2", "Gemma3-4B"),
    ("ROPD", "Qwen3-30B-A3B", "Qwen3-4B"),
    ("ROPD", "Qwen3-30B-A3B", "Gemma3-4B"),

    # ===== Additional papers from body text (not in Table 3) =====
    # §4.1
    ("f-div", "OPT-13B", "OPT-1.3B"),
    ("f-div", "OPT-6.7B", "OPT-1.3B"),
    ("f-div", "GPT-2 XL", "GPT-2 Medium"),
    ("AKL", "Qwen3-8B", "Qwen3-1.7B"),
    ("AKL", "Qwen2.5-14B", "Qwen2.5-1.5B"),
    ("KL-Control", "Qwen3-8B", "Qwen3-1.7B"),
    ("KL-Control", "Qwen3-8B", "Qwen3-4B"),
    ("AntiSD", "Self", "Self (4B-30B)"),

    # §4.2
    ("TSD-KD", "Gemma-2-27B", "Gemma-2-2B"),
    ("TSD-KD", "Qwen3-8B", "Qwen3-1.7B"),

    # §4.3
    ("CoDistill-GRPO", "Qwen2.5-Math-7B", "Qwen2.5-Math-1.5B"),
    ("CoDistill-GRPO", "Qwen2.5-Math-1.5B", "Qwen2.5-Math-7B"),  # bidirectional
    ("dGRPO", "Qwen3-8B", "Qwen3-4B"),
    ("Sparse-to-Dense", "Qwen3-8B", "Qwen3-1.7B"),
    ("Sparse-to-Dense", "Llama-3.3-70B", "Llama-3.1-8B"),

    # §5.1 additional
    ("MiniLLM", "Qwen3-8B", "Qwen3-1.7B"),
    ("MiniLLM", "Llama-2-13B", "Llama-2-7B"),
    ("MPD", "Qwen3-8B", "Qwen3-1.7B"),
    ("BRTS", "Qwen3-8B", "Qwen3-1.7B"),
    ("Lion-body", "Qwen3-32B", "Qwen3-8B"),
    ("Lion-body", "Qwen3-32B", "Qwen3-4B"),
    ("Lion-body", "Llama-3.1-70B", "Llama-3.1-8B"),
    ("SpecKD", "DeepSeek-R1-7B", "DeepSeek-R1-1.5B"),

    # §5.3.1 additional
    ("OPHSD", "Self", "Qwen3-8B"),
    ("COPSD", "Self", "Qwen3-8B"),
    ("ATESD", "Self", "Qwen3-1.7B"),
    ("ATESD", "Self", "Qwen3-4B"),
    ("ATESD", "Self", "Qwen3-8B"),
    ("TRACE", "Self", "Qwen3-8B"),
    ("GATES", "Self", "Qwen3-8B"),

    # §5.3.2 additional
    ("SPIN", "Self", "Zephyr-7B"),
    ("RLRT", "Self", "Qwen3-8B"),
    ("TABOM", "Self", "DiffusionLM"),

    # §5.3.3 additional
    ("RLSD", "Self", "Qwen3-VL-8B"),
    ("CREDIT", "Self", "Qwen3-8B"),
    ("OGLS-SD", "Self", "Qwen3-8B"),

    # §6 additional
    ("FOPD", "Qwen3-8B", "Qwen3-1.7B"),
    ("Stable-OPD", "DeepSeek-R1-7B", "Qwen3-1.7B"),
    ("Stable-OPD", "DeepSeek-R1-7B", "Qwen2.5-Math-1.5B"),
    ("SCOPE", "Skywork-OR1-7B", "R1-Distill-Qwen-1.5B"),
    ("SCOPE", "Qwen3-8B", "Qwen3-4B"),
    ("Lightning-OPD", "Qwen3-32B", "Qwen3-8B"),
    ("Lightning-OPD", "Qwen3-8B", "Qwen3-4B"),
    ("TIP", "Qwen3-8B", "Qwen3-4B"),
    ("TIP", "Llama-3.1-70B", "Llama-3.1-8B"),
    ("CoPD", "Qwen3-8B", "Qwen3-4B"),
    ("EffOPD", "Self", "Qwen3-8B"),

    # §7
    ("Rethinking-OPD", "Self", "Qwen3-8B"),
    ("Rethinking-OPD", "Self", "Qwen3-1.7B"),
    ("CaOPD", "Self", "Qwen3-8B"),
    ("Degradation", "Self", "DeepSeek-R1-7B"),

    # §8 additional
    ("HyperEyes", "External", "Qwen3-VL-30B"),
    ("ProteinOPD", "Multi-teacher", "ProteinPLM"),
    ("TTS", "Qwen3-32B", "Qwen3-8B"),
    ("TTS", "Llama-3.1-70B", "Llama-3.1-8B"),
    ("Safactory", "Self", "Self (Agent)"),
]

# ===== MODEL NORMALIZATION =====
def normalize_model(name):
    """Normalize model names for display. Returns (canonical_name, family)."""
    name = name.strip()

    # Self-distillation variants
    if name.startswith("Self") or name in ("Teacher",):
        return "Self", "Self"

    # Multi-teacher / domain specialists → collapse
    if any(x in name for x in ("Multi-teacher", "Multi-mode", "Domain", "5 domain",
                                 "10+ domain", "GRPO specialists", "External",
                                 "Multi-teacher debate")):
        return "Multi-Teacher", "Multi-Teacher"

    # Specific model aliases
    # Strategy: merge versions (Llama-2/3/3.1 → by size), merge IT/Base variants
    aliases = {
        # GPT family — merge small variants
        "GPT-2": ("GPT-2 (124M)", "GPT"),
        "GPT-2 Medium": ("GPT-2 (124M)", "GPT"),  # merge into GPT-2
        "GPT-2 XL": ("GPT-2 XL (1.5B)", "GPT"),
        "GPT-2 Large": ("GPT-2 XL (1.5B)", "GPT"),  # merge into XL
        "DistilGPT-2": ("GPT-2 (124M)", "GPT"),  # merge
        "GPT-5-Chat": ("GPT-4/5 (API)", "GPT"),
        "GPT-5.2": ("GPT-4/5 (API)", "GPT"),
        "ChatGPT": ("GPT-4/5 (API)", "GPT"),

        # T5 family
        "T5-XL": ("T5-XL (3B)", "T5"),
        "T5-Small": ("T5-Small/Base", "T5"),
        "T5-Base": ("T5-Small/Base", "T5"),

        # OPT family — merge
        "OPT-350M": ("OPT-≤1.3B", "OPT"),
        "OPT-1.3B": ("OPT-≤1.3B", "OPT"),
        "OPT-6.7B": ("OPT-6.7B/13B", "OPT"),
        "OPT-13B": ("OPT-6.7B/13B", "OPT"),

        # Pythia — merge
        "Pythia-160M": ("Pythia-≤1B", "OPT"),
        "Pythia-1B": ("Pythia-≤1B", "OPT"),

        # LLaMA / Llama family — merge by size bucket
        "LLaMA-7B": ("Llama-7B", "Llama"),
        "LLaMA-13B": ("Llama-13B", "Llama"),
        "Llama-2-7B": ("Llama-7B", "Llama"),
        "Llama-2-13B": ("Llama-13B", "Llama"),
        "Llama-3-8B": ("Llama-8B", "Llama"),
        "Llama-3.1-8B": ("Llama-8B", "Llama"),
        "Llama-3.1-70B": ("Llama-70B", "Llama"),
        "Llama-3.2-3B": ("Llama-3B", "Llama"),
        "Llama-3.3-70B": ("Llama-70B", "Llama"),
        "TinyLlama-1.1B": ("TinyLlama-1.1B", "Llama"),

        # Gemma family
        "Gemma-2B": ("Gemma-2B", "Gemma"),
        "Gemma-7B-IT": ("Gemma-7B", "Gemma"),
        "Gemma-2-2B": ("Gemma-2B", "Gemma"),
        "Gemma-2-2B-IT": ("Gemma-2B", "Gemma"),
        "Gemma-2-9B": ("Gemma-9B", "Gemma"),
        "Gemma-2-27B": ("Gemma-27B", "Gemma"),
        "Gemma-3-4B": ("Gemma-4B", "Gemma"),
        "Gemma3-4B": ("Gemma-4B", "Gemma"),

        # Mistral
        "Mistral-7B": ("Mistral-7B", "Mistral"),
        "Zephyr-7B": ("Mistral-7B", "Mistral"),  # Zephyr is Mistral-7B

        # Phi
        "Phi-3-mini": ("Phi-3/4-mini", "Phi"),
        "Phi-4-mini": ("Phi-3/4-mini", "Phi"),

        # Qwen2 family — merge into Qwen2.5
        "Qwen2-0.5B": ("Qwen2.5-0.5B", "Qwen2.5"),
        "Qwen2-0.5B-IT": ("Qwen2.5-0.5B", "Qwen2.5"),
        "Qwen2-7B": ("Qwen2.5-7B", "Qwen2.5"),
        "Qwen2-7B-IT": ("Qwen2.5-7B", "Qwen2.5"),

        # Qwen2.5 family
        "Qwen2.5-0.5B": ("Qwen2.5-0.5B", "Qwen2.5"),
        "Qwen2.5-1.5B": ("Qwen2.5-1.5B", "Qwen2.5"),
        "Qwen2.5-3B": ("Qwen2.5-3B", "Qwen2.5"),
        "Qwen2.5-7B": ("Qwen2.5-7B", "Qwen2.5"),
        "Qwen2.5-14B": ("Qwen2.5-14B", "Qwen2.5"),
        "Qwen2.5-72B": ("Qwen2.5-72B", "Qwen2.5"),
        "Qwen2.5-Math-1.5B": ("Qwen2.5-Math-1.5B", "Qwen2.5"),
        "Qwen2.5-Math-7B": ("Qwen2.5-Math-7B", "Qwen2.5"),
        "Qwen2.5-VL-3B": ("Qwen2.5-VL-3B", "Qwen2.5"),

        # Qwen3 family
        "Qwen3-0.6B": ("Qwen3-0.6B", "Qwen3"),
        "Qwen3-1.7B": ("Qwen3-1.7B", "Qwen3"),
        "Qwen3-4B": ("Qwen3-4B", "Qwen3"),
        "Qwen3-8B": ("Qwen3-8B", "Qwen3"),
        "Qwen3-14B": ("Qwen3-14B", "Qwen3"),
        "Qwen3-30B": ("Qwen3-30B", "Qwen3"),
        "Qwen3-30B-A3B": ("Qwen3-30B-A3B", "Qwen3"),
        "Qwen3-30B-A3B-Instruct": ("Qwen3-30B-A3B", "Qwen3"),
        "Qwen3-32B": ("Qwen3-32B", "Qwen3"),
        "Qwen3-235B-A22B": ("Qwen3-235B", "Qwen3"),
        "Qwen3-VL-4B": ("Qwen3-VL-4/8B", "Qwen3"),
        "Qwen3-VL-8B": ("Qwen3-VL-4/8B", "Qwen3"),
        "Qwen3-VL-30B": ("Qwen3-VL-30/32B", "Qwen3"),
        "Qwen3-VL-32B": ("Qwen3-VL-30/32B", "Qwen3"),
        "Qwen3.5-9B": ("Qwen3-8B", "Qwen3"),  # merge 3.5-9B into 8B bucket
        "QwQ-32B": ("Qwen3-32B", "Qwen3"),  # QwQ is Qwen3-32B variant

        # DeepSeek family
        "DeepSeek-R1": ("DeepSeek-R1", "DeepSeek"),
        "DeepSeek-R1-7B": ("DS-R1-Distill-7B", "DeepSeek"),
        "R1-Distill-Qwen-7B": ("DS-R1-Distill-7B", "DeepSeek"),
        "R1-Distill-7B": ("DS-R1-Distill-7B", "DeepSeek"),
        "DeepSeek-R1-1.5B": ("DS-R1-Distill-1.5B", "DeepSeek"),
        "R1-Distill-Qwen-1.5B": ("DS-R1-Distill-1.5B", "DeepSeek"),
        "DeepSeek-R1-Distill-Qwen-1.5B": ("DS-R1-Distill-1.5B", "DeepSeek"),
        "DeepSeek-V4-Pro": ("DeepSeek-V4", "DeepSeek"),

        # Other — merge small variants
        "OLMo-3-7B": ("OLMo-7B", "Other"),
        "Skywork-OR1-Math-7B": ("Skywork-7B", "Other"),
        "AceReason-7B": ("OLMo-7B", "Other"),  # merge into 7B Other
        "openPangu-Embedded-1B": ("Other-≤3B", "Other"),
        "Openmath-Nemotron-7B": ("Nemotron-7/30B", "Other"),
        "MiMo-V2-Flash": ("MiMo-V2", "Other"),
        "Nemotron-30B-MoE": ("Nemotron-7/30B", "Other"),
        "Unified agentic coder": ("Other-≤3B", "Other"),
    }

    if name in aliases:
        return aliases[name]

    # Skip non-model entries
    skip_patterns = ["2B-3B scale", "SD 3.5", "VideoLLM", "DiffusionLM",
                     "ProteinPLM", "Self (4B-30B)", "Self (Agent)",
                     "Self (text-mode)", "Self (audio-mode)"]
    for pat in skip_patterns:
        if pat in name:
            return None, None

    # Fallback
    return name, "Unknown"


# ===== FAMILY ORDERING =====
FAMILY_ORDER = [
    "GPT", "T5", "OPT", "Pythia",
    "Llama", "Mistral",
    "Gemma", "Phi",
    "Qwen2", "Qwen2.5", "Qwen3",
    "DeepSeek",
    "Other", "Multi-Teacher", "Self",
]

FAMILY_COLORS = {
    "GPT": "#E57373",
    "T5": "#F06292",
    "OPT": "#BA68C8",
    "Pythia": "#9575CD",
    "Llama": "#7986CB",
    "Mistral": "#64B5F6",
    "Gemma": "#4FC3F7",
    "Phi": "#4DD0E1",
    "Qwen2": "#4DB6AC",
    "Qwen2.5": "#81C784",
    "Qwen3": "#AED581",
    "DeepSeek": "#FFD54F",
    "Other": "#FFB74D",
    "Multi-Teacher": "#A1887F",
    "Self": "#90A4AE",
}


def size_key(model_name):
    """Extract numeric size for sorting within family."""
    import re
    # Extract the largest number (in B or M)
    billions = re.findall(r'(\d+(?:\.\d+)?)B', model_name)
    millions = re.findall(r'(\d+(?:\.\d+)?)M', model_name)
    if billions:
        return max(float(b) for b in billions)
    if millions:
        return max(float(m) for m in millions) / 1000
    # Special cases
    if "XL" in model_name:
        return 1.5
    if "Large" in model_name:
        return 0.774
    if "Base" in model_name:
        return 0.22
    if "Small" in model_name:
        return 0.06
    if "Mini" in model_name or "mini" in model_name:
        return 3.8
    return 0


def build_matrix():
    """Build the teacher×student count matrix from RAW_PAIRS."""
    # Normalize all pairs
    teacher_counts = defaultdict(lambda: defaultdict(int))
    all_teachers = {}  # canonical -> family
    all_students = {}

    for method, teacher_raw, student_raw in RAW_PAIRS:
        t_name, t_fam = normalize_model(teacher_raw)
        s_name, s_fam = normalize_model(student_raw)
        if t_name is None or s_name is None:
            continue
        teacher_counts[t_name][s_name] += 1
        all_teachers[t_name] = t_fam
        all_students[s_name] = s_fam

    # Sort teachers and students by family order, then by size descending
    def sort_key(name, fam_dict):
        fam = fam_dict.get(name, "Unknown")
        fam_idx = FAMILY_ORDER.index(fam) if fam in FAMILY_ORDER else 99
        return (fam_idx, -size_key(name))

    teachers_sorted = sorted(all_teachers.keys(), key=lambda n: sort_key(n, all_teachers))
    students_sorted = sorted(all_students.keys(), key=lambda n: sort_key(n, all_students))

    # Build matrix
    n_t = len(teachers_sorted)
    n_s = len(students_sorted)
    matrix = np.zeros((n_t, n_s), dtype=int)

    for i, t in enumerate(teachers_sorted):
        for j, s in enumerate(students_sorted):
            matrix[i, j] = teacher_counts[t].get(s, 0)

    # Filter out empty rows/cols
    row_mask = matrix.sum(axis=1) > 0
    col_mask = matrix.sum(axis=0) > 0
    matrix = matrix[row_mask][:, col_mask]
    teachers_sorted = [t for t, m in zip(teachers_sorted, row_mask) if m]
    students_sorted = [s for s, m in zip(students_sorted, col_mask) if m]

    return matrix, teachers_sorted, students_sorted, all_teachers, all_students


def generate_heatmap(output_dir):
    """Generate the high-resolution heatmap."""
    matrix, teachers, students, t_fams, s_fams = build_matrix()
    n_t, n_s = matrix.shape

    print(f"Matrix: {n_t} teachers × {n_s} students")
    print(f"Non-zero cells: {(matrix > 0).sum()}")
    print(f"Total pairs: {matrix.sum()}")

    # Figure size
    fig_w = max(n_s * CELL_SIZE + 4, 20)
    fig_h = max(n_t * CELL_SIZE + 4, 20)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # Font setup
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['TeX Gyre Termes', 'Times New Roman', 'DejaVu Serif']

    # Colormap
    colors = ['#FFFFFF', '#EBF5FB', '#AED6F1', '#5DADE2', '#2E86C1', '#1B4F72']
    boundaries = [0, 0.5, 1.5, 2.5, 4.5, 7.5, max(12, matrix.max() + 1)]
    cmap = LinearSegmentedColormap.from_list("opd_atlas", colors, N=256)
    norm = BoundaryNorm(boundaries, cmap.N)

    # Plot
    im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect='equal')

    # Cell annotations
    for i in range(n_t):
        for j in range(n_s):
            val = matrix[i, j]
            if val > 0:
                ax.text(j, i, str(val), ha='center', va='center',
                       fontsize=FONT_CELL, fontweight='bold', color='black')

    # Family separator lines
    def draw_family_lines(items, fam_dict, axis):
        prev_fam = None
        for idx, item in enumerate(items):
            fam = fam_dict.get(item, "Unknown")
            if prev_fam is not None and fam != prev_fam:
                pos = idx - 0.5
                if axis == 'y':
                    ax.axhline(y=pos, color='#2C3E50', linewidth=3, alpha=0.8)
                else:
                    ax.axvline(x=pos, color='#2C3E50', linewidth=3, alpha=0.8)
            prev_fam = fam

    draw_family_lines(teachers, t_fams, 'y')
    draw_family_lines(students, s_fams, 'x')

    # Tick labels with family colors
    ax.set_xticks(range(n_s))
    ax.set_yticks(range(n_t))

    x_labels = ax.set_xticklabels(students, rotation=55, ha='right', fontsize=FONT_TICK)
    y_labels = ax.set_yticklabels(teachers, fontsize=FONT_TICK)

    for label in x_labels:
        name = label.get_text()
        fam = s_fams.get(name, "Unknown")
        color = FAMILY_COLORS.get(fam, "#333333")
        label.set_color(color)

    for label in y_labels:
        name = label.get_text()
        fam = t_fams.get(name, "Unknown")
        color = FAMILY_COLORS.get(fam, "#333333")
        label.set_color(color)

    # Marginal sums
    row_sums = matrix.sum(axis=1)
    col_sums = matrix.sum(axis=0)

    for i, s in enumerate(row_sums):
        ax.text(n_s + 0.3, i, f'{s}', ha='left', va='center',
               fontsize=FONT_MARGIN, color='#555555', style='italic')

    for j, s in enumerate(col_sums):
        ax.text(j, n_t + 0.3, f'{s}', ha='center', va='top',
               fontsize=FONT_MARGIN, color='#555555', style='italic')

    # Title
    ax.set_title(f'Teacher × Student Model Atlas — On-Policy Distillation ({n_t}T × {n_s}S, {(matrix > 0).sum()} cells)',
                fontsize=FONT_TITLE, fontweight='bold', pad=30)

    # Legend — single row across bottom
    legend_patches = []
    seen_fams = set()
    for item in teachers + students:
        fam = t_fams.get(item, s_fams.get(item, "Unknown"))
        if fam not in seen_fams and fam in FAMILY_COLORS:
            seen_fams.add(fam)
            legend_patches.append(mpatches.Patch(
                color=FAMILY_COLORS[fam], label=fam))

    legend = ax.legend(handles=legend_patches, loc='lower center',
                      bbox_to_anchor=(0.5, -0.12), ncol=len(legend_patches),
                      fontsize=FONT_LEGEND, frameon=False)

    # Grid
    ax.set_xlim(-0.5, n_s - 0.5)
    ax.set_ylim(n_t - 0.5, -0.5)

    # Thin grid lines
    for i in range(n_t + 1):
        ax.axhline(y=i - 0.5, color='#EEEEEE', linewidth=0.5)
    for j in range(n_s + 1):
        ax.axvline(x=j - 0.5, color='#EEEEEE', linewidth=0.5)

    plt.tight_layout()

    # Save
    png_path = os.path.join(output_dir, 'model-atlas-heatmap.png')
    pdf_path = os.path.join(output_dir, 'model-atlas-heatmap.pdf')
    plt.savefig(png_path, dpi=DPI, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(pdf_path, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()

    print(f"Saved: {png_path} ({os.path.getsize(png_path) / 1024 / 1024:.1f} MB)")
    print(f"Saved: {pdf_path}")

    # Print statistics
    print(f"\nTop-5 Teachers (by total pairs):")
    for rank, idx in enumerate(np.argsort(-row_sums)[:5]):
        print(f"  {rank+1}. {teachers[idx]}: {row_sums[idx]}")
    print(f"\nTop-5 Students (by total pairs):")
    for rank, idx in enumerate(np.argsort(-col_sums)[:5]):
        print(f"  {rank+1}. {students[idx]}: {col_sums[idx]}")

    return matrix, teachers, students


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate OPD Model Atlas Heatmap")
    parser.add_argument("--output", "-o", default=".",
                       help="Output directory for PNG/PDF")
    args = parser.parse_args()

    generate_heatmap(args.output)
