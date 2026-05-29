# Round 35 — READ §8 Applications, Systems, and Emerging Domains

**Mode**: READ  
**Section**: §8 (lines 1085–1229, includes §8.1 Industrial, §8.2 Emerging, §8.3 Systems, §8.4 When to Use, §8.5 Budget)  
**Time**: 2026-05-08 22:31 UTC

---

## Paragraph-by-Paragraph Issues

### §8 Intro (lines 1087–1089)
- ✅ Well-structured framing paragraph. No issues.

### §8.1 Industrial Deployment

#### Two-phase distillation pipelines (Qwen3, Gemma 2, MiMo-V2)

1. **Gemma 2 "27B→9B→2B" notation misleading** [ACCURACY]
   - The arrow notation implies a cascade (27B trains 9B, then 9B trains 2B). 
   - Actual paper: 27B is the teacher for BOTH 9B and 2B independently (parallel distillation, not cascading).
   - Fix: change to "(27B→9B, 27B→2B)" or just "bridging performance gaps between the 27B teacher and smaller 9B/2B students"

2. **MiMo-V2 "frontier performance on mathematical reasoning"** [OVERCLAIM-MINOR]
   - The paper claims "strong reasoning and agentic capabilities" but doesn't claim SOTA/frontier on math specifically.
   - Suggestion: soften to "strong performance on mathematical reasoning and agentic tasks"

3. **Qwen3 claims verified** ✅
   - "one-tenth of the GPU hours" — directly from paper (Table 21 comparison)
   - "further improves pass@64 on AIME where RL does not" — confirmed from paper Section 4.4

#### OPD as model consolidation (DeepSeek-V4, KAT-Coder-V2, Nemotron-Cascade 2, CoPD)

4. **DeepSeek-V4 "entirely replaces mixed RL stage with pure multi-teacher OPD"** [PENDING-VERIFY]
   - Still on pending_verify list from earlier rounds. Need to verify against actual paper.
   - The claim "pure" is strong — need PDF confirmation.

5. **DeepSeek-V4 "1.6T-parameter model"** [TO-VERIFY]
   - Need to confirm this figure from the paper.

6. **KAT-Coder-V2 "79.6% on SWE-bench Verified"** [PENDING-VERIFY]
   - On pending_verify list. No local PDF available. Cannot verify this tick.

7. **Nemotron-Cascade 2 claims** ✅
   - "30B MoE, 3B activated" — confirmed from paper
   - "Gold Medal-level on IMO, IOI, ICPC World Finals" — confirmed ("gold-medal performance on IMO 2025, IOI 2025 and ICPC World Finals 2025")
   - "20× fewer parameters than DeepSeek-V3.2-Speciale" — confirmed (671B vs 30B ≈ 22×, paper uses "20×")

8. **CoPD paragraph is very long** [PROSE-DENSITY]
   - The CoPD description is heavy on mechanism detail. Could benefit from tighter writing.
   - "achieving all-in-one integration of text, image, and video reasoning capabilities that surpasses both mixed RLVR and sequential multi-teacher OPD (MOPD), and even domain-specific experts" — this sentence is 30+ words and reads like a run-on.

#### ORBIT (multi-budget reasoning)

9. **No issues with factual claims** — the formula is self-contained and the description is clear.
10. **Good synthesis sentence** at end connecting ORBIT to consolidation pattern ("domain vs compute budget axis"). ✅

#### Agentic Distillation

11. **TCOD "+18 points over vanilla multi-turn OPD"** [VERIFIED-PRIOR]
   - Previously verified in Bundle B (.factcheck/bundle-B.md). ✅ (max gain +18.67)

12. **MAD-OPD OPAD "+2.4% over single-teacher OPD"** [PENDING-VERIFY]
   - On pending_verify list. No local PDF.

13. **Skill-SD "+14.0% over GRPO on AppWorld and +10.9% on Sokoban"** [PENDING-VERIFY]
   - On pending_verify list. No local PDF.

14. **OpenClaw-RL description** [WEAK-ARGUMENTATION]
   - Very brief (one sentence). Compared to TCOD and MAD-OPD which get full paragraphs, OpenClaw-RL is underexplained. What makes "hindsight-guided OPD with a Process Reward Model" distinctive? How does it differ from standard PRM-guided training?

15. **"The optimal granularity appears to be the decision boundary"** [UNSUPPORTED-SYNTHESIS]
   - This is a novel claim/synthesis by the survey authors. It's insightful but currently unsupported by any citation. Either (a) mark as "we conjecture" or (b) find supporting evidence in the cited papers.

16. **Closing summary paragraph** (4 patterns) [GOOD-SYNTHESIS] ✅
   - Excellent high-level synthesis connecting all four patterns. This is the kind of writing that makes high-cited surveys.

### §8.2 Emerging Domains

#### Multimodal OPD

17. **VOLD claims verified** ✅
   - "27.1% to 32.0% on MMMU-Pro" — confirmed from paper
   - "text-only teacher... without ever seeing the image" — confirmed

18. **Video-OPD and X-OPD** [SHALLOW]
   - Each gets only one sentence. No numbers, no mechanism detail. Compare to VOLD and CORD which get full paragraphs. Either expand (what are the key results?) or justify the brevity.

19. **CORD formula** [NO-SPECIFIC-NUMBER]
   - Claims "state-of-the-art speech reasoning performance" without a specific benchmark number. Should include at least one concrete result.

20. **KEPO description** [SHALLOW]
   - Only 2 sentences. "exploration collapse when initial solve rates are near zero" is an interesting claim but no number backs it up. Where does KEPO show this?

#### Embodied Intelligence

21. **HY-Embodied "16 out of 22 benchmarks"** [PENDING-VERIFY]
   - On pending_verify list. No local PDF.

22. **GUI-SD "SOTA on 6 benchmarks"** [PENDING-VERIFY]
   - On pending_verify list. No local PDF.

23. **OPD-AV "5× compression"** [NO-CITE-FOR-NUMBER]
   - The 8B→1.7B ratio is ≈4.7×. Is "5×" an approximation from the paper or is it computed? Should verify.

24. **VLA-OPD** [NO-SPECIFIC-RESULT]
   - "significantly improves sample efficiency over RL and robustness over SFT" — how much? Any number?

25. **Synthesis paragraph** ("on-policy generation is even more critical than in text-only settings") [GOOD but UNSUPPORTED]
   - Insightful claim about why OPD matters more for physical domains. But needs citation or explicit reasoning chain rather than just "the consistent finding across these physical and multimodal domains."

#### Medical agents

26. **TT-OPD "+3.9 percentage-point improvement"** [PENDING-VERIFY]
   - On pending list for exact numbers. Should verify against /tmp/opd_papers/ttopd.pdf.

27. **"10 of 18 benchmarks"** [PENDING-VERIFY]
   - Same.

28. **"3.6K+ tasks, 135 domain-specific tools, 828K medical passages"** [TO-VERIFY]
   - These are specific numbers that should be cross-checked.

### §8.3 System-Level Integration

29. **OpenRLHF, veRL, vLLM, TensorRT-LLM — NO CITATIONS** [MISSING-CITE]
   - All four frameworks are mentioned without \citep{}. These are published works with arXiv papers and should be cited. Critical oversight for a survey.

30. **"16 GB of logit data per batch"** [UNSUPPORTED-CALCULATION]
   - The text says "[B, T, |V|] × 2 bytes in BF16" but doesn't specify B and T. Without those, the 16 GB figure can't be verified. Should either show the calculation (e.g., B=4, T=4096, V=128K → 4×4096×128000×2 = 4.2 GB, not 16 GB) or use a plausible configuration.
   - Let me compute: if B=8, T=2048, V=128K → 8×2048×128000×2 = 4.2 GB. To get 16 GB need B=32, T=2048, V=128K → 16.8 GB. Or B=8, T=4096, V=256K → 16.8 GB. Plausible but should be explicit about assumptions.

31. **DeepSeek-V4 systems paragraph** [TO-VERIFY]
   - Detailed claims about hidden-state caching, prediction-head loading, FP4 quantization-aware training during OPD. These are specific enough to verify against the paper.

### §8.4 When to Use On-Policy vs Off-Policy

32. **"three conditions hold simultaneously: exceptionally strong teacher (>500B), diverse reasoning traces, and relatively small student (≤70B)"** [NOVEL-SYNTHESIS]
   - This is the authors' synthesis/heuristic, not from any single paper. It's reasonable but should be flagged as "we propose" or supported by specific evidence. The 500B and ≤70B thresholds seem arbitrary.

33. **DeepSeek-R1 as exemplar of off-policy regime** ✅
   - Correct — R1 distills to 1.5B-70B models using off-policy data.

34. **"Any RLHF infrastructure can be directly repurposed for OPD"** [OVERCLAIM-MINOR]
   - While conceptually true, this understates the practical differences (logit access, divergence computation, etc. that RLHF doesn't need).

### §8.5 Distillation Tax: Compute Budget Allocation

35. **"Qwen3... four-stage pipeline (pre-train → SFT → RL → long-context)"** [ACCURACY]
   - Need to verify this is exactly Qwen3's pipeline. The paper describes thinking/non-thinking mode training which may not map cleanly to this 4-stage description.

36. **General structure** ✅
   - Three-stage pattern (off-policy warm-up → on-policy logit → reward-guided refinement) is well-motivated by the industrial examples.

---

## Priority Summary

| Priority | Issue | Lines/Claim |
|----------|-------|-------------|
| HIGH | Missing citations for OpenRLHF/veRL/vLLM/TensorRT-LLM | §8.3 |
| HIGH | Gemma 2 "27B→9B→2B" implies cascade but is parallel | §8.1 |
| HIGH | "16 GB logit data" calculation unspecified, potentially wrong | §8.3 |
| MEDIUM | OpenClaw-RL underexplained relative to peers | §8.1 Agentic |
| MEDIUM | Video-OPD, X-OPD, KEPO too shallow (no numbers) | §8.2 |
| MEDIUM | "Decision boundary" synthesis unsupported by cite | §8.1 Agentic |
| MEDIUM | CORD "SOTA" without concrete number | §8.2 |
| MEDIUM | VLA-OPD "significantly improves" without numbers | §8.2 |
| MEDIUM | >500B / ≤70B thresholds in §8.4 seem arbitrary | §8.4 |
| LOW | CoPD description overly long/run-on sentence | §8.1 |
| LOW | MiMo-V2 "frontier" slightly overclaimed | §8.1 |
| LOW | "Any RLHF infra can be repurposed" slight overclaim | §8.4 |

---

## Pending Verifications for VERIFY Round

The following need PDF verification in next round:
1. DeepSeek-V4 "pure multi-teacher OPD" / "1.6T" / systems details (no local PDF found — check if downloaded)
2. KAT-Coder-V2 79.6% SWE-bench (no local PDF)
3. MAD-OPD OPAD +2.4% (no local PDF)
4. Skill-SD +14% AppWorld (no local PDF)
5. HY-Embodied 16/22 (no local PDF)
6. GUI-SD SOTA on 6 benchmarks (no local PDF)
7. TT-OPD numbers (PDF at /tmp/opd_papers/ttopd.pdf)
8. OPD-AV "5× compression" ratio
9. Qwen3 four-stage pipeline accuracy

---

## Structural Observations

**Strengths of §8:**
- The four-pattern taxonomy (two-phase / consolidation / multi-budget / agentic) is excellent organizational structure
- The agentic distillation subsection builds nicely from trajectory→step→skill granularity  
- Synthesis paragraphs at end of §8.1 and end of Embodied Intelligence are strong
- Systems section (§8.3) provides unique value — most surveys skip infra

**Weaknesses:**
- §8.2 is uneven — VOLD gets detailed treatment while Video-OPD/X-OPD/KEPO get drive-by mentions
- §8.3 lacks citations for major frameworks (OpenRLHF, veRL, vLLM)
- §8.4 and §8.5 make semi-novel recommendations without enough hedging ("we suggest" vs stating as fact)
- Several numerical claims remain unverified due to missing PDFs
