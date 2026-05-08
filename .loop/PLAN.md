# V2 Deep-Read & Polish Loop (2026-05-08 → 2026-05-09)

## Mission
10-hour continuous loop to (1) push writing quality toward high-cited-survey standard,
(2) add deep insight so readers finish with 收获良多, (3) verify every number/claim against
original PDFs (never grep-only — read the actual prose), (4) cite wherever a claim is made.

## Setup
- Paper dir: `/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey/`
- Tex: `latex-v2/main.tex` (1219 lines, 57p, 118 cites, HEAD=7537807)
- PDFs: `pdfs/` has 116 papers; fallback `/tmp/opd_papers/` for PBSD/TT-OPD
- Factcheck reports land in `.factcheck/`
- Round logs in `.loop/round-NN.md`; state in `.loop/state.json`

## Round task rotation

Each 10-minute tick picks ONE section slice and ONE task mode:

| Mode    | What the sub-agent does |
|---------|-------------------------|
| READ    | Read the current section slice + cited PDFs cover-to-cover; produce a "potential issues" list (unsupported claims, missing citations, weak argumentation, places that could be deepened) |
| VERIFY  | Take READ's issues list and cross-check numbers/formulas/method attributions against PDFs; write verdict list |
| DEEPEN  | Rewrite targeted paragraphs to add insight (tie method X to broader trend, explain WHY something works, compare across methods, surface trade-offs) |
| POLISH  | Line-level prose pass: sentence flow, remove filler, fix colons/semicolons, tighten verbs |
| COMPILE | Full pdflatex run + bibtex + pdflatex×2; check page count, citation match, 0 errors; commit with message `loop(rN-<section>-<mode>)` |

## Section priority (round-robin)

1. §1 Introduction (26 lines) — narrative hook, field momentum
2. §2 Background (89 lines) — math correctness, formula derivation
3. §3.1 Method Landscape (119 lines) — taxonomy clarity
4. §3.2 Method Comparison Table (205 lines) — table accuracy
5. §3.3 Decision Tree (33 lines)
6. §4 Objectives (198 lines) — formulas, method claims
7. §5 Signal Source (151 lines) — teacher arch, self-distillation
8. §6 Training Dynamics (82 lines) — TIP/SCOPE/Lightning numbers
9. §7 Understanding OPD (84 lines) — failure modes, decision framework
10. §8 Applications (82 lines) — industrial numbers
11. §9 Future Directions (35 lines) — narrative flow, overclaim check
12. §10 Conclusion (26 lines) — closing argument

## Constraints (enforced every round)

- No `;`, no prose `:` (structural/math OK)
- No self-invented formulas in §9
- No "no one has done X" without citation
- All numerical claims must have a citation or explicit justification
- Never change cite keys silently — if bib entry wrong, update bib
- Never `git reset --hard`; always `merge`/`rebase` on conflict
- Compile+verify BEFORE committing
- Page count target: 55-60 pages (OK if it grows by 2-3 during deepening)

## Git hygiene
- Each round commits on its own (even if only .loop/round-NN.md is new)
- Commit format: `loop(rNN-section-mode): brief change summary`
- Never force-push

## What counts as "high-cited survey" quality (from boss's directive)

Benchmark: surveys like "Attention Is All You Need" isn't a survey, but think
Goodfellow 2014 GAN, Vaswani 2017 (introductions), or genuine literature reviews like
Ruder's ML surveys. Characteristics:
1. **Narrative arcs**, not just method enumeration — each section tells a story
2. **Synthesis over enumeration** — "these 5 methods all address failure mode X via
   mechanism Y, with trade-off Z"
3. **Explain WHY** something works, not just WHAT it does
4. **Connect across sections** — §5 refers back to §2 framework, §7 synthesizes §4-§6
5. **Trade-off tables** with principled columns, not just "method/year/venue"
6. **Takeaways** per section — one-liner answer to "what should a practitioner do"
7. **Grounded future directions** — avoid wishful claims; tie each to specific gap
8. **Citation hygiene** — every number/strong claim has a cite
