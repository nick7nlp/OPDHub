# Round 01 — §1 Introduction VERIFY

**Mode**: VERIFY  
**Section**: §1 Introduction  
**Source**: round-01-seed.md (5 priority issues flagged by main's READ)

## Verification Results

| # | Claim | Source checked | Verdict | Action |
|---|-------|---------------|---------|--------|
| 1 | "near-human competence in reasoning, code generation, and multilingual instruction following" | DeepSeek-R1 (2501.12948) reports AIME 79.8%, Codeforces 2029 elo, MMLU 90.8 — "near-human" only on specific benchmarks | ⚠️ Overclaim | Soften to "state-of-the-art performance across reasoning, code generation, and multilingual benchmarks" |
| 2 | "DeepSeek-V4 replacing its mixed RL stage with pure multi-teacher OPD" | DeepSeek-V4 tech report + multiple secondaries confirm: "the mixed RL phase in V3.2 has been entirely replaced by OPD" with domain-specific experts distilled into unified model | ✅ Accurate | Keep as-is |
| 3 | "GKD introduced the first unified on-policy framework for LLM distillation in mid-2023" | GKD paper (2306.13649, ICLR 2024): proposes generalized on-policy KD with multiple divergences + RL integration. BUT MiniLLM (2306.08543) is literally concurrent (also Jun 2023, also ICLR 2024). GKD claims "first to perform distillation and RL fine-tuning at the same time," not "first on-policy framework." Also, GKD experiments use T5 (enc-dec), not decoder-only | ⚠️ Overclaim | Qualify: "GKD~\citep{2306.13649} and MiniLLM~\citep{2306.08543} concurrently introduced the first on-policy frameworks for autoregressive LM distillation in mid-2023" — or keep GKD but add "alongside concurrent work by \citet{2306.08543}" |
| 4 | "architecturally necessary for the next generation of reasoning-capable systems" — unsupported | Revisiting OPD (2603.25562) says OPD is "attractive for long-horizon reasoning and agentic post-training." Luo2026demystifying studies OPD failure modes, implicitly assuming OPD is the standard. DeepSeek-V4 replacing RL with OPD is strongest evidence. But "architecturally necessary" is still our editorial claim | ⚠️ Strong but defensible | Add cite: "making on-policy correction not merely beneficial but arguably architecturally necessary~\citep{2603.25562,deepseekv4}" — the "arguably" hedges + the cites ground it |
| 5 | "calibration-capability gap" term provenance | Found in §7 (L1032): explicitly attributed to CaOPD~\citep{2604.16830} which calls it "The Illusion of Certainty: Decoupling Capability and Calibration." Our term "calibration-capability gap" is our shorthand synthesis of their finding | ✅ Acceptable | Not novel unsupported term — it's our narrative label for a cited phenomenon. No change needed |
| 6 | "Existing surveys...generally retain the classical compression framing" (2402.13116) | Xu et al. 2024 abstract: "KD emerges as a pivotal methodology for transferring advanced capabilities...compressing these models." Their Fig 1 shows "Compress" as a primary role; taxonomy is algorithm/skill/verticalization, not on/off-policy distinction | ✅ Accurate | Our characterization is fair |
| 7 | "off-policy imitation of proprietary LLMs often yields students that reproduce surface style without acquiring the underlying reasoning competence" (2305.15717) | Gudibande et al. 2023 abstract: "imitation models are adept at mimicking ChatGPT's style but not its factuality...there exists a substantial capabilities gap" | ✅ Accurate | Exact match with our paraphrase |

## Summary

- 5/7 claims ✅ verified accurate
- 2/7 claims ⚠️ minor overclaims that need softening
- 0 claims ❌ factually wrong

## Recommended DEEPEN actions (for round 02 or 03)

1. **L85**: Change "near-human competence in reasoning, code generation, and multilingual instruction following" → "state-of-the-art performance across reasoning, code generation, and multilingual benchmarks"
2. **L92**: Change "GKD introduced the first unified on-policy framework for LLM distillation" → "GKD~\citep{2306.13649}, alongside the concurrent MiniLLM~\citep{2306.08543}, introduced the first on-policy frameworks for autoregressive language model distillation" (or keep GKD-focused but add qualifier)
3. **L93**: "making on-policy correction not merely beneficial but architecturally necessary" → add "arguably" + cite `\citep{2603.25562,deepseekv4}` to ground it

These are all minor wording fixes that DEEPEN can batch in ~3 edits.
