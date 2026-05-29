# Round 46 — VERIFY — §10 Conclusion

**Mode**: VERIFY  
**Section**: §10 Conclusion  
**Assignment**: round 46 % 5 = 1 → VERIFY; (46 // 5) % 10 = 9 → 10-Conclusion  
**Source**: round-45 READ findings

---

## Verification Table

| # | Claim | Source Checked | Verdict | Notes |
|---|-------|---------------|---------|-------|
| 4 | "performance gap widening for longer reasoning chains where error compounding is most severe" | MiniLLM (2306.08543) Fig. 6 + GKD (2306.13649) §2 | ✅ Supported | MiniLLM Fig 6 shows ExAccErr accumulates with generation length; GKD discusses "cascading effect where error in prediction at early step affects future predictions." **Fix needed**: add `\citep{2306.08543,2306.13649}` after the claim. |
| 13 | "The absence of distillation scaling laws" — no cite | §9 body discusses this citing 2502.08606 | ⚠️ Defensible | Not a factual error but should add cross-ref `(Section~\ref{sec:future})` or cite `\citep{2502.08606}`. |
| 14 | "unsolved problem of teacher uncertainty quantification" — no cite | §9 discusses this conceptually | ⚠️ Defensible | No specific paper cited in §9 either — this is a known open problem. OK as a gap statement but adding a cross-ref to §9 would strengthen it. |
| 15 | "challenge of lifelong adaptation without catastrophic forgetting" — no cite | General continual learning lit | ⚠️ Needs cite | Well-established problem. Should cite at least one continual learning reference (e.g., Kirkpatrick et al. 2017 EWC, or a CL survey). Currently no CL paper in our bib — adding one would be a §DEEPEN task. |
| 16 | "architectural necessity" | No source found | ❌ Overclaim | This phrase appears in §1 and §10 without citation. No paper explicitly claims OPD is "architecturally necessary." Should soften to "a core training component" or "an increasingly standard practice." |
| 17 | "approximately 8--10 new OPD papers per month" | Our bib: 2026 data | ⚠️ Undercount, but unsourced | Our bib alone has 59 papers Jan–Apr 2026 = ~15/month. But not all are strictly "OPD methods" (some are applications/infra). The field's pace is plausibly 8-10 *method* papers/month + additional application papers. **Recommendation**: change to "approximately 10--15 new papers per month in early 2026" which is directly defensible from our bibliography, or soften to "numerous new papers each month" without committing to a number. |
| 24 | "4--5$\times$ over off-policy SFT" in conclusion (no cite) | Body line 999 cites `wu2026lightning` | ✅ Defensible | Body calculates 1200-1500 vs 300 GPU-hrs = 4-5x; cites Lightning OPD for consistency. Lightning paper itself shows 120 GPU-hrs standard OPD vs 30 GPU-hrs (4x ratio at 8B scale). The body's estimate is a reasonable extrapolation to 70B→7B. Conclusion could add "(Section~\ref{subsec:compute})" cross-ref. |
| 25 | "reduce downstream inference costs by orders of magnitude" | Calculation | ⚠️ Overclaim | Typical teacher/student: 70B→7B = 10x (one order), 405B→7B = 58x (approaching two). "Orders of magnitude" (plural, 100x+) only holds for extreme cases or when including throughput multipliers. **Fix**: change to "by an order of magnitude or more" — accurate for typical cases, defensible for extreme ones. |
| 26 | MSD DPSW mechanism detail in conclusion | MSD paper (2605.02971) | ✅ Accurate | Paper confirms DPSW "adaptively increases penalty on safety-critical tokens by jointly considering teacher and student perspectives." The *accuracy* is fine; the *structural* issue (too much method detail for a conclusion) is a DEEPEN/POLISH concern, not a factual error. |
| 27 | "generalizes to unseen languages and more challenging jailbreak attacks" | MSD paper (2605.02971) abstract + experiments | ✅ Confirmed | Paper explicitly states "generalizes effectively to more challenging datasets and unseen languages." |

---

## Summary of Verdicts

| Verdict | Count | Items |
|---------|-------|-------|
| ✅ Supported/Accurate | 5 | #4 (with cite fix), #24, #26, #27, #17 (defensible range) |
| ⚠️ Needs softening/fix | 4 | #13-14 (add cross-refs), #15 (needs cite), #25 (overclaim) |
| ❌ Overclaim | 1 | #16 ("architectural necessity") |

---

## Recommended Fixes for DEEPEN round

1. **Line ~1212** (error compounding claim): Add `\citep{2306.08543,2306.13649}` after "where error compounding is most severe"
2. **Line ~1222** (three gap claims): Add cross-refs: "The absence of distillation scaling laws (Section~\ref{sec:future}), the unsolved problem of teacher uncertainty quantification, and the challenge of lifelong adaptation without catastrophic forgetting..."
3. **Line ~1222** ("architectural necessity"): Change to "a core component of the LLM training stack" or "an increasingly indispensable training paradigm"
4. **Line ~1229** ("8--10 papers per month"): Change to "more than ten new papers per month" (conservative based on our 15/month in 2026)
5. **Line ~1253** ("orders of magnitude"): Change to "by an order of magnitude or more"
6. **[Defer to later]** #15 — adding a continual learning cite requires a bib addition; flag for a future round

---

## Process Notes

- All PDF reads done via `pdftotext + grep context` — confirmed surrounding paragraphs, not just pattern matches
- MiniLLM Figure 6 caption explicitly says "ExAccErr accumulated with the generation length"
- GKD Section 2: "mismatch can have a cascading effect where error in prediction at early step can affect the future predictions"
- Lightning OPD Table 2: 120 GPU-hrs standard OPD vs 30 for Lightning at 8B scale (4.0x speedup)
- MSD abstract: "generalizes effectively to more challenging datasets and unseen languages"
- Bib count: 59 papers in Jan-Apr 2026 (4 months) = 14.75/month; "8-10" is conservative but could be more precise
