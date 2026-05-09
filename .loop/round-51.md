# Round 51 — §1 Introduction VERIFY

**Mode**: VERIFY  
**Section**: §1 Introduction  
**Date**: 2026-05-09 01:11 UTC  
**Source**: Round 50's READ output (8 issues identified)

## Verification Results

| # | Claim/Issue | Source Checked | Verdict | Notes |
|---|-------------|----------------|---------|-------|
| 4 | "textbook instance of exposure bias in interactive IL" citing Ross 2011 | `pdfs/ross2011reduction.pdf` full text | ⚠️ Minor | Ross 2011 never uses "exposure bias" — paper discusses "compounding errors" from i.i.d. violation. Term "exposure bias" coined by Ranzato 2015 (1511.06732). However, Ross 2011 formalizes the exact same phenomenon (train on expert states, compound errors under learner's states). §2.1 already correctly titles this "Off-Policy Exposure Bias" with full formal treatment. §1 usage is stylistically imprecise but factually grounded — the cite is for the *bound*, not the *term*. |
| 5 | $O(\epsilon T^2)$ bound source | `pdfs/ross2011reduction.pdf` intro ¶2 + §2.1 of main.tex | ✅ Accurate | Ross 2011 explicitly states: "a classifier that makes a mistake with probability ε under the distribution of states encountered by the expert can make as many as T²ε mistakes in expectation over T-steps under the distribution of states the classifier itself induces." §2.1 formally presents this as "By the DAgger theorem [Ross 2011], if a policy mimics an expert with per-step error ε under the training distribution, the expected total discrepancy over a trajectory of length T under the learner's own state visitation scales as O(εT²)." Cross-reference complete and accurate. |
| 7 | DAgger $O(\epsilon T)$ reduction claim | `pdfs/ross2011reduction.pdf` Theorem 2.1 + §2.1 remark | ✅ Accurate | DAgger's guarantee is indeed O(εT) where ε is the best-in-class per-step loss. §2.1 includes "Remark: The DAgger bound in LLMs" that properly qualifies the application to LLMs (teacher may be poorly calibrated on OOD student prefixes). Rigorous. |
| 8 | "iterative, self-correcting optimization loop" — overclaim? | Conceptual | ⚠️ Mild | "Self-correcting" implies error detection + correction feedback. OPD does expose error states during training but doesn't have an explicit error-detection mechanism. §7 discusses when OPD fails (self-play saturation, diversity collapse). Suggest softening to "iterative optimization loop in which the training distribution co-evolves with the model" — but low priority since §2.1's Remark already provides the caveat. |
| 9 | "formally equivalent to a KL-constrained form of RL" citing 2602.12125 | `pdfs/2602.12125.pdf` abstract + §3 | ✅ Accurate | Paper explicitly states: "we first theoretically show that OPD is a special case of dense KL-constrained RL where the reward function and the KL regularization are always weighted equally." This is the precise formal proof. Single cite is appropriate — this paper is the one that establishes the formal equivalence for OPD specifically (not the broader RLHF-DPO duality from Rafailov 2023 which is about preference learning, not distillation). |
| 10 | Industrial adoption sentence lacks synthesis | N/A (writing quality, not fact) | — | Deferred to DEEPEN round. Valid observation: "Qwen3, DeepSeek-V4, Gemma 2, MiMo-V2" is enumeration without explaining WHY convergence. |
| 11 | Gemma 2 cite key 2408.00118 | `latex-v2/references.bib` entry | ✅ Correct | Confirmed: "Gemma 2: Improving Open Language Models at a Practical Size", Gemma Team, arXiv:2408.00118, 2024. Correct paper. |
| 15 | "no current treatment offers a unified mathematical account" — exclusive? | Bib scan + knowledge check | ✅ Defensible | Only known LLM KD survey is Xu et al. 2402.13116, which is general KD (covers both on/off-policy, compression framing). No dedicated OPD-only survey found. Claim is accurate as of submission date. |
| 1 | Redundant connectives | N/A (prose style) | — | Deferred to POLISH round. |

## Summary of Verdicts

- ✅ **5 claims verified accurate**: $O(\epsilon T^2)$ bound (Ross 2011), DAgger $O(\epsilon T)$ reduction, KL-RL equivalence (2602.12125), Gemma 2 cite key, "no current treatment" exclusivity
- ⚠️ **2 minor issues**: 
  - "Textbook instance of exposure bias" — term not from Ross 2011 but phenomenon is. Acceptable with current framing since cite is for the bound, not the terminology.
  - "Self-correcting" — mild overclaim, low priority since §2.1 Remark + §7 provide caveats
- **2 deferred to later rounds**: Industrial synthesis (DEEPEN), connective pileup (POLISH)

## Actionable Items for DEEPEN (Round 52)

1. **Optional**: Consider adding "originally termed \emph{compounding error} in imitation learning" parenthetical after "exposure bias" — provides attribution clarity without derailing flow. Low priority.
2. **Recommend**: Soften "self-correcting" → "iterative optimization loop in which the training distribution co-evolves with the model" (or similar). This is a one-phrase edit.
3. **Recommend**: After the industrial examples list, add a synthesis clause explaining WHY diverse teams converge on OPD (e.g., "converging on on-policy training despite strikingly different architectural choices, because longer reasoning chains universally amplify the exposure bias that on-policy correction resolves").

## 补充: Ross 2011 关键段落摘录

From the introduction (p.1, ¶3):
> "In particular, a classifier that makes a mistake with probability ε under the distribution of states/observations encountered by the expert can make as many as T²ε mistakes in expectation over T-steps under the distribution of states the classifier itself induces (Ross and Bagnell, 2010). Intuitively this is because as soon as the learner makes a mistake, it may encounter completely different observations than those under expert demonstration, leading to a compounding of errors."

Key: Ross uses "compounding of errors", not "exposure bias". The bound T²ε is from Ross & Bagnell 2010, formalized in this 2011 paper as Theorem 2.1.
