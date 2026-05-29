# Round 26 — VERIFY §6 Training Dynamics

**Mode**: VERIFY  
**Section**: §6 Training Dynamics and Efficiency (lines 919–1000)  
**Source**: Round 25 READ findings  
**Agent**: cron tick 26  

## Verification Results

| # | Claim | Paper | Verdict | Notes |
|---|-------|-------|---------|-------|
| 1 | Fast OPD: "exposure bias concentrated in early tokens, errors compound most severely" | 2602.15260 §2.2 | ⚠️ **INACCURATE FRAMING** | Paper says "training signals are often concentrated in the prefix" — this is a signal-concentration observation (reverse-KL loss higher in early tokens because student is weaker at high-level planning), NOT an exposure-bias/error-compounding observation. The paper's hypothesis is that prefix contains the most useful distillation signal, and even truncated prefix training suffices. |
| 2 | PACED: "expected gradient magnitude scales as p(1-p)" | 2603.11178 §3, Eq.(3) | ⚠️ **OVERSIMPLIFIED but defensible** | Paper's general leading-order weight family is `w(p) = p^α(1-p)^β` (Beta kernel). The symmetric case α=β=1 gives p(1-p) which the paper calls "the default choice." The asymmetric cases (α≠β) shift the peak. Survey says "scales as p(1-p)" which is the simplest instantiation. Technically the paper presents p(1-p) as ONE choice, not THE unique result. Should mention the general Beta kernel. |
| 3 | AdaSwitch: "maintains a running estimate of the student's cumulative prefix quality" | 2510.07842 §3.2, Eq.(4-5) | ⚠️ **INACCURATE MECHANISM** | Paper's actual mechanism: sliding window of length L over recent token-level divergences (KL/JSD between student and teacher logits). Moving average: d̄_i = (1/L)Σd_j. Threshold: τ = K·d̄_{i-1}. Switches to teacher when divergence exceeds τ. NOT "cumulative prefix quality" — it's "recent divergence history with adaptive threshold." |
| 4 | "Retaining by Doing" — framing suggests paper is specifically about OPD | 2510.18874 | ✅ **DEFENSIBLE** | Paper studies RL vs SFT forgetting broadly and identifies on-policy data (not RL specifically) as the key factor. The paper explicitly tests whether it's the on-policy data or other RL components and concludes it's the on-policy data. Survey's extension to OPD context is valid since OPD also uses on-policy data. Current framing "on-policy data generation itself serves as an implicit rehearsal mechanism" is accurate. |
| 5 | Cost example: "Off-policy ~300 GPU-hours, On-policy ~1,200-1,500 GPU-hours, 4-5× overhead" (70B→7B, 8×H100) | No specific citation | ⚠️ **UNCITED ESTIMATES** | Lightning OPD gives 120→30 GPU-hours for 8B scale (4× ratio). The 300/1200-1500 numbers for 70B→7B do not appear in any cited paper. They are plausible back-of-envelope estimates (3×forward for student gen + 10× forward for 70B teacher scoring), but readers may mistake them for measured values. The 4-5× ratio is consistent with Lightning OPD's 4× and general community consensus. |
| 6 | Semantic Bootstrapping "+10.6% on MATH-500 over GRPO" | 2512.05105, Table 1 | ✅ **ACCURATE** | Paper explicitly states: "SSB training outperforms GRPO training by 10.6% and 10% on MATH-500 and AIME2024 benchmarks, respectively." |
| 7 | Uni-OPD "5 domains, 16 benchmarks" | hou2026uniopd | ❓ **CANNOT VERIFY** | No PDF available. arXiv abstract doesn't mention these specific numbers. Need full paper to confirm. |

## Summary of Verdicts

- ✅ Accurate: 2 claims (Retaining by Doing framing, Semantic Bootstrapping +10.6%)
- ⚠️ Needs fix: 3 claims (Fast OPD framing, PACED p(1-p) oversimplification, AdaSwitch mechanism)
- ⚠️ Needs caveat: 1 claim (cost example uncited)
- ❓ Unverifiable: 1 claim (Uni-OPD 5/16)

## Detailed Fix Recommendations

### Fix 1: Fast OPD (HIGH priority)

**Current**: "Fast OPD observes that exposure bias is concentrated in the early tokens of a sequence, where errors compound most severely."

**Should be**: Fast OPD observes that the useful distillation signal (measured by reverse-KL loss) is concentrated in the prefix of student-generated sequences, because the student is weakest at high-level planning captured in early tokens. It truncates rollouts to a prefix of length k and applies the distillation objective only to this prefix, achieving comparable quality at 2×–47× reduced training FLOPs.

**Rationale**: The paper's §2.2 explicitly measures where loss is concentrated and conjectures "this pattern reflects the student model being weaker at high-level planning captured early in the trajectory." The mechanism is signal concentration, not error compounding.

### Fix 2: PACED (MEDIUM priority)

**Current**: "the expected gradient magnitude scales as p(1-p), which is maximized at p=0.5 and vanishes at both extremes"

**Should be**: Add that p(1-p) is the simplest (symmetric) case of a general Beta-kernel weight w(p)=p^α(1-p)^β. Asymmetric choices (α≠β) shift the peak away from p=0.5 to prioritize harder or easier prompts. Keep the intuition that SNR vanishes at both extremes.

### Fix 3: AdaSwitch (MEDIUM priority)

**Current**: "maintains a running estimate of the student's cumulative prefix quality"

**Should be**: "maintains a sliding window of recent token-level divergences between student and teacher and switches from exploration to guidance when divergence exceeds a context-adaptive threshold (K times the windowed average)"

### Fix 4: Cost example (LOW priority)

Add "representative estimates" qualifier or cite Lightning OPD for the 4× ratio with a note that absolute numbers scale with model size.

## Next Round Action

Round 27 = DEEPEN for §6. Apply fixes 1-3 with targeted edits.
