# On-Policy Distillation Survey — Project Hub

Single source of truth for all OPD-related work: papers, PDFs, notes, scripts, LaTeX manuscripts, and the public Awesome List.

> **Last reorg:** 2026-05-16. Everything OPD-related lives under this directory.

---

## 🗂️ Directory Layout

```
on-policy-distillation-survey/
│
├── README.md                          ← you are here
├── papers-meta/                       ← OPD paper metadata & indices
│   ├── INDEX.md                       ← master index of all 48 OPD papers
│   ├── opd-new-papers.md              ← live tracking of newly discovered OPD papers
│   └── new_opd_2605_bibtex.bib        ← curated BibTeX for May-2026 batch
│
├── pdfs/                              ← classified PDF library (145 total)
│   ├── by-aid/                        ← flat compatibility view: <aid>.pdf → ../<bucket>/<aid>.pdf
│   ├── background/                    ← classics & reference material (4)
│   │   ├── hinton2015distilling.pdf
│   │   ├── kim2016sequence.pdf
│   │   ├── ross2011reduction.pdf
│   │   └── blog-tml-onpolicy-distillation.md
│   ├── pre-2026/                      ← arXiv 2022-2025 (49)
│   ├── 2026-01/  (9)
│   ├── 2026-02/  (15)
│   ├── 2026-03/  (20)
│   ├── 2026-04/  (21)
│   └── 2026-05/  (27)
│
├── notes/                             ← deep-read notes & audit logs
│   ├── 2306.13649.md                  ← per-paper close reading
│   ├── 2605.05040.md
│   ├── new-papers-2605-batch.md       ← May-2026 batch integration analysis
│   ├── reading-pbsd-ttopd-2026-05-08.md
│   ├── audit-2026-05-10-10h.log       ← 10-hour optimization audit
│   ├── audit-2026-05-10-deep-read.md
│   ├── audit-2026-05-11-escalation.md
│   ├── audit-2026-05-11-final-summary.md
│   └── deep-read-2026-05-13.md
│
├── scripts/                           ← project-specific tooling
│   ├── generate_atlas_heatmap.py      ← Awesome List heatmap generator
│   ├── opd_pdf_downloader.py          ← arXiv PDF fetcher
│   ├── verify_opd_titles.py           ← title cross-validation
│   ├── opd-10h-audit-driver.sh        ← 10h optimization driver
│   ├── draw_atlas_fine.py
│   ├── draw_final2.py
│   └── generate_model_atlas.py
│
├── latex-v3/                          ← current working manuscript (78 pages, 170 cites)
│   ├── main.tex
│   ├── references.bib
│   └── ...
├── latex-v2/                          ← prior major version
├── latex-v1.5/                        ← arXiv submission (2026-04-17)
├── latex-v1/                          ← original
│
├── Awesome-LLM-On-Policy-Distillation/   ← independent GitHub repo (153 papers)
│
├── narrative-patches/                 ← in-flight prose changes
├── .factcheck/                        ← fact-check bundles A/B/C
├── .loop/                             ← deep optimization loop logs
├── opd_abbreviation_registry.json     ← controlled vocabulary
├── bib-audit-report.md
└── CHANGES.md
```

---

## 📚 What lives where

### 🔍 Looking for…

| Need | Go to |
|------|-------|
| Find an OPD paper by ID | `papers-meta/INDEX.md` (status table) |
| Get a PDF by arXiv ID | `pdfs/by-aid/<aid>.pdf` (or browse by date bucket) |
| Latest unintegrated OPD papers | `papers-meta/opd-new-papers.md` |
| Per-paper deep-read notes | `notes/<aid>.md` |
| Working LaTeX manuscript | `latex-v3/main.tex` |
| Heatmap regeneration | `scripts/generate_atlas_heatmap.py` |
| Awesome List website | `Awesome-LLM-On-Policy-Distillation/README.md` |

### 🌳 Manuscript versioning

- **V1** — original arXiv preprint baseline
- **V1.5** — arXiv submission 2026-04-17 (53 pages / 101 citations / 0 errors)
- **V2** — 5/9 milestone (59 pages / 124 citations / 0 errors)
- **V3** — current working version (78 pages / 170 citations)

V3 is the active target for COLM 2026.

---

## 🔁 PDF compatibility

Legacy code may reference the flat path `papers/opd/<aid>.pdf`. A symlink keeps it alive:

```
/apdcephfs_cq8/.../openclaw_fsp/papers/opd  →  pdfs/by-aid/
```

Inside `pdfs/by-aid/`, every PDF is a relative symlink to its actual location in the date-bucketed structure. So any of these resolve identically:

```bash
.../on-policy-distillation-survey/pdfs/2026-04/2604.03128.pdf
.../on-policy-distillation-survey/pdfs/by-aid/2604.03128.pdf
.../openclaw_fsp/papers/opd/2604.03128.pdf
```

The original `papers/opd/` and `papers/opd-new/` directories were archived to `papers/.opd-archived-2026-05-16-1134/` (kept for 7 days as safety net before deletion).

---

## 📊 Coverage stats

_Computed from paper_kb at reorg time — see `papers-meta/INDEX.md` for live status._

- 48 OPD papers tracked in paper_kb
- 145 PDFs in `pdfs/` (OPD + baselines + background)
- 27/48 OPD papers have local PDF (56%)
- 42/48 have LLM deep summary (88%)
- 18/48 have curated BibTeX in paper_kb (38%)
- 30/48 cited in V3 (62%)
- 31/48 in Awesome List (65%)

Backlog of resources to acquire is enumerated in `papers-meta/INDEX.md` under "Missing Resources To Backfill".

---

## 🔄 Daily automation

Scout cron `daily-opd-paper-scout` runs at 02:40 CST and appends discoveries to `papers-meta/opd-new-papers.md`. Workspace memory keeps a symlink at `~/.openclaw/workspace/memory/opd-new-papers.md` for backward compatibility.

---

## 📜 Conventions

1. **PDF naming** — always `{arxiv_id}.pdf`. The arXiv ID alone is the canonical identifier.
2. **PDF location** — date bucket is determined by arXiv ID (`YYMM` prefix). New papers go in `pdfs/2026-MM/` automatically.
3. **Background/baseline papers** — anything *not* an OPD paper itself but referenced for context goes in `pdfs/pre-2026/` or `pdfs/background/` (named exceptions).
4. **Notes** — date-prefixed (`YYYY-MM-DD-topic.md`) for audits/reading sessions; `<aid>.md` for per-paper deep reads.
5. **Scripts** — one-purpose, executable, with a docstring at top. Heatmap generator is the single source of truth in `scripts/generate_atlas_heatmap.py`.
