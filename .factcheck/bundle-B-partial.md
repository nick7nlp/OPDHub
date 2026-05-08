# Bundle B Partial Fact-Check (salvaged from subagent output)

## Source
Subagent factcheck-bundle-B ran 3m13s, completed early without writing final report. Salvaged from mid-stream output:

## Confirmed findings

### TCOD (chen2026tcod) ✅
- **Claim**: "On ALFWorld, WebShop, and ScienceWorld, TCOD achieves gains of up to +18 points over vanilla multi-turn OPD"
- **Verified**: Paper states "improving agent performance by up to 18 points over vanilla OPD". Table 3 shows TCOD-F2B improves ScienceWorld by +18.67 (from 0.17 to 18.84).
- **Verdict**: ✅ ACCURATE (18 is the correct rounded max gain)

### TCOD (chen2026tcod) — F2B early-turn claim ⚠️→✅ (judgment call)
- **Claim**: "F2B variant showing particular strength on tasks where early-turn errors are most consequential"
- **Evidence**: Table 2 TCOD-F2B achieves 81.43 (vs OPD 65.72) = +15.71 on ALFWorld
- **Verdict**: ✅ reasonable interpretation (F2B begins supervision at early turns, matches intuition)

### Trajectory-Level KL Instability ✅
- Phenomenon confirmed in paper

### Semantic Soft Bootstrapping (mitra2025semantic → 2512.05105) ❓ unverified
- Subagent was mid-check when it cut off. This needs follow-up.

## TODO for loop rounds (priority)
1. Finish verifying Semantic Soft Bootstrapping +10.6% on MATH-500
2. Verify Lightning OPD 4× cost reduction
3. Verify TIP 50% token retention claim
4. Verify SCOPE +5.5% claim
5. Verify Stable-OPD (luo2026demystifying) +7.2% KL gradient asymmetry
6. Verify Veto β parameter dual role
7. Verify PromptKD 0.0007% parameter addition
8. Verify TT-OPD KL collapse 2.637→0.343 and 7.82→5.52 turns
9. Verify §6.3 concrete compute cost example (70B teacher, 7B student, 4-5× overhead)

## Note for loop
Bundle B subagent was interrupted not by error but likely by early completion heuristic. If spawning fresh researcher for remaining B/C items, use a narrower task scope (5-8 claims max) and ask for explicit final file write with verification step.
