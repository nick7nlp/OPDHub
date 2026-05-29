# Round 71 — READ §5 Signal Source and Teacher Architecture

**Mode:** READ  
**Section:** 5-Signal-Source  
**Time:** 2026-05-09 04:52 UTC

## Findings

### Language Issues (for POLISH)

1. **"highlights" (line ~805):** "The distinction between hidden-state alignment (DSKD) and vocabulary-space alignment (Cross-Tokenizer KD) highlights a fundamental design trade-off." → rephrase to avoid AI-flavor word.

2. **"reveals" (line ~834):** "The surprising effectiveness of such coarse supervision reveals that on-policy exploration itself provides a substantial fraction of the learning signal" → rephrase.

3. **"reveals" (line ~890, IRIS paragraph):** "Each step reveals that self-play is not inherently limited" → rephrase.

4. **"novel" (line ~867, GUI-SD):** "Beyond the novel PI type" → rephrase.

5. **"However" (line ~886, SPIN):** "However, this convergence guarantee comes with an inherent limitation." → rephrase.

6. **"However" (line ~898, self-play boundary):** "However, this also exposes the fundamental boundary of pure self-play." → rephrase.

7. **Em-dash "stable---once" (line ~886):** narrative em-dash in SPIN paragraph. → rephrase to period or parenthetical.

### Structural/Logic Issues (for DEEPEN)

8. **§5.1 White-Box long paragraph chains:** The subsection is well-structured with bold leads. No major logic gaps.

9. **§5.2 Black-Box:** Clear progression from adversarial → verbal → preference. Good cross-method insight at the end ("spectrum of signal richness versus access requirements"). Well done.

10. **§5.3 Self-Distillation:** Strong internal logic with three sub-families. The progression from PI → Self-Play → External Feedback is clear. The cross-cutting insight connecting $\pi$-Play and PAINT to the saturation problem is effective.

### Claims to Verify (for VERIFY)

11. **Already in pending_verify:** "MTP <5% drop clarification (actually 3-7% by model)" — paper 2602.06019

12. **New:** "CRISP 57-59% token reduction + 9-16pp accuracy improvement on MATH-500" — should verify against paper 2603.05433

13. **New:** "SSD Qwen3-30B-Instruct 42.4% → 55.3% on LiveCodeBench v6" — verify against zhang2026embarrassingly

14. **New:** "SD-ZERO 68.3% AIME 2024 vs GRPO 62.5%" — verify against he2026selfdistillation

15. **New:** "SRPO +3.4% over GRPO and +6.3% over SDPO on five-benchmark average" — verify against li2026unifying

16. **New:** "Lion-13B 70K training examples, competitive on BIG-Bench Hard and AGIEval" — verify against 2305.12870

### Overall Assessment

§5 is the longest section (~150 lines of dense prose). The writing is generally strong with good cross-method synthesis. The main polish work is removing 2x "However", 2x "reveals", 1x "highlights", 1x "novel", and 1x em-dash. The DEEPEN pass should focus on strengthening the transition between §5.2 (Black-Box) and §5.3 (Self-Distillation), which currently feels like a clean break rather than a conceptual bridge.

## Next Round

Round 72: VERIFY on §5 — process pending_verify items (MTP drop) + verify 2-3 new claims from this READ.
