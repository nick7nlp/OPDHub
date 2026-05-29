# On-Policy Distillation Survey — Project Hub

Single source of truth for all OPD-related work: papers, PDFs, notes, scripts, LaTeX manuscripts, and the public Awesome List.

> **Last updated:** 2026-05-28.

---

## 🗂️ Directory Layout

```
on-policy-distillation-survey/
│
├── README.md                          ← you are here
├── papers-meta/                       ← OPD paper metadata & indices
│   ├── INDEX.md                       ← master index
│   ├── opd-new-papers.md              ← live tracking of newly discovered OPD papers
│   ├── excluded-papers.md             ← rejected papers log with reasons
│   └── new_opd_2605_bibtex.bib        ← curated BibTeX for May-2026 batch
│
├── pdfs/                              ← classified PDF library (197 unique)
│   ├── by-aid/                        ← flat symlink view: <aid>.pdf → ../<bucket>/<aid>.pdf
│   ├── background/                    ← 20 reference/baseline papers (not OPD themselves)
│   ├── pre-2026/                      ← OPD method papers, arXiv 2022-2025
│   ├── 2026-{01..05}/                 ← OPD method papers, by month
│   └── .trash-YYYY-MM-DD/            ← rejected papers (7-day retention)
│
├── notes/                             ← deep-read notes & pipeline output
│   ├── paper_notes.json               ← 🔑 PRIMARY DB: 183 entries, V3 schema
│   ├── validation_report.md           ← latest validation cycle report
│   ├── <aid>.md                       ← per-paper manual close reading (legacy)
│   └── audit-*.md / deep-read-*.md    ← audit & reading session logs
│
├── scripts/                           ← project-specific tooling
│   ├── generate_atlas_heatmap.py      ⭐ AUTHORITATIVE heatmap generator (only copy)
│   ├── generate_index.py             ← INDEX.md generator
│   └── .deprecated/                   ← old scripts kept for reference
│
├── schema/                            ← paper_notes V3 schema documentation
│   └── paper_notes_v3.md
│
├── latex-v4/                          ← CURRENT working manuscript (COLM 2026)
│   ├── main.tex                       ← 1473 lines
│   ├── references.bib                 ← 149 OPD method entries
│   └── references_background.bib      ← 18 background/tool entries
├── latex-v3/                          ← prior milestone (COLM 2026 submission base)
├── latex-v2/                          ← prior milestone (59p / 124 cites)
├── latex-v1.5/                        ← arXiv submission 2026-04-17 (53p / 101 cites)
├── latex-v1/                          ← original
│
├── Awesome-LLM-On-Policy-Distillation/   ← GitHub repo (175 🟢 papers)
│
└── .archive-*/                        ← historical V2-era logs (loop/factcheck/patches)
```

---

## 📊 Coverage Stats (2026-05-28)

| Source | Count | Description |
|--------|-------|-------------|
| paper_notes.json (DB) | **183** | Full V3-schema deep-read notes (−1 ThinkTuning audit reject, +1 daily scout 2605.28014) |
| PDFs OPD | **177** | OPD method papers across date buckets (−1 ThinkTuning to trash, +1 daily 2605.28014) |
| PDFs background | **20** | Classic KD / scaling law / game-theoretic refs |
| V4 references.bib | **149** | OPD papers cited in current manuscript |
| V4 references_background.bib | **18** | Background refs (17 bg PDFs + 1 URL-only) |
| Awesome List 🟢 | **174** | Verified OPD papers on GitHub |
| Heatmap | **90 models, 844 pairs** | From DB + README (regenerated 2026-05-28 post-ThinkTuning cleanup) |

### Alignment Rule
```
DB (183) ⊃ V4 bib (149) — DB has 34 papers pending V4 integration (backlog)
Awesome 🟢 (174) = DB minus analysis-only/non-method entries
PDFs on disk: 197 (177 OPD + 20 background)
V4 bib (149) + V4 background bib (18) = survey citations
```

---

## 📚 What lives where

| Need | Go to |
|------|-------|
| Find an OPD paper by ID | `papers-meta/INDEX.md` |
| Get a PDF by arXiv ID | `pdfs/by-aid/<aid>.pdf` |
| Latest unintegrated papers | `papers-meta/opd-new-papers.md` |
| Excluded/rejected papers & reasons | `papers-meta/excluded-papers.md` |
| Structured paper data (T/S pairs, benchmarks) | `notes/paper_notes.json` |
| Working LaTeX manuscript | `latex-v4/main.tex` |
| Heatmap regeneration | `scripts/generate_atlas_heatmap.py` |
| Awesome List | `Awesome-LLM-On-Policy-Distillation/README.md` |

---

## 🌳 Manuscript Versioning

| Version | Date | Stats | Status |
|---------|------|-------|--------|
| V1 | 2026-04 | original | archived |
| V1.5 | 2026-04-17 | 53p / 101 cites / 0 err | arXiv submission |
| V2 | 2026-05-09 | 59p / 124 cites / 0 err | milestone |
| V3 | 2026-05-23 | 1405 lines / 150 bib | COLM 2026 submission base |
| **V4** | **active** | **1473 lines / 149 bib** | **V4 update in progress** |

---

## 🔍 Full Corpus Audit (2026-05-28)

对全库 159 篇 `is_opd=yes` 论文做了逐篇人工审计，结论：

### 明确误判 (2 篇，已处理)

| arXiv ID | Name | 原分类 | 问题 | 处置 |
|----------|------|--------|------|------|
| 2604.20933 | IRIS | §5.3.2 Self-Distill | Pure self-improvement RL。Rényi iterative self-play，无 teacher，无 distribution matching，reward 只是 self-to-prev log-ratio。与 SPIN 不同（SPIN 有 p_data 做 target）| PDF → `background/`，V4 正文已排除（scope boundary）|
| 2508.07616 | ThinkTuning | §5.2 Black-Box | 标题自己说 "without Distillation"。Teacher 只提供 thought templates (文本 data), 不提供 logit distribution。Loss 是 PPO on augmented data，不是 KL to teacher | 全库清理完成 (2026-05-28): V4 cite + bib + DB + INDEX + Awesome 全移除; PDF → `pdfs/.trash-2026-05-28-thinktuning/` |

### Borderline 保留 (3 篇，有争议但在谱系内)

| arXiv ID | Name | 理由 |
|----------|------|------|
| 2604.02288 | SDPO | Self-distill + DPO, 训练信号是 self-generated preference pairs |
| 2605.05040 | PBSD | Preference-based self-distill, DPO-style reward-regularized KL |
| 2605.21851 | OPPO | On-policy preference optimization, boundary 在 RL vs distill |

### 三条件过滤 REJECT (同日, 4 篇)

| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.16941 | WINO+ (Roll Out and Roll Back) | rollout once-before-training → off-policy SFT |
| 2605.19776 | PSDISTILL | RL-only (GRPO) + 无 teacher-distill term |
| 2605.19447 | SERL | RL agent framework, 无 teacher model |
| 2605.22675 | SPD | NTP loss on self-outputs, no teacher, paper 自己标 "On-Policy Self-Distillation = ×" |

**误判率**: 2/159 ≈ 1.3%（得益于 V3 deep-read 精读质量）

---

## 🔄 Awesome List 整理 (2026-05-28)

| 操作 | 数量 | 说明 |
|------|------|------|
| Demote 🟢→🟡 | 26 篇 | Post-V4 papers（已 V3 精读 but 尚未 cite in V4 manuscript）|
| Remove non-OPD | 4 篇 | MixSD (off-policy), Decoupling-KL (analysis), WINO+ (off-policy), SPD (not OPD) |
| Heatmap 重建 | 90 models / 842 pairs | `generate_atlas_heatmap.py` regenerated |

---

## 📝 Background 目录新增 (2026-05-28)

`pdfs/background/` 新增 3 篇（17→20）：

| File | Paper | 归类理由 |
|------|-------|----------|
| 2604.20933.pdf | IRIS (Rényi Iterative Self-play) | Game-theoretic self-play, 非 OPD |
| 2401.01335.pdf | SPIN (Self-Play Fine-Tuning) | Game-theoretic self-play, 非 OPD |
| 2605.18141.pdf | A Brief Overview of OPD | Survey/overview, 作为 reference 保留 |

---

## 🛠️ Writing Skill 更新 (2026-05-28)

`academic-rigor` skill 新增/更新 references：

| File | 内容 |
|------|------|
| `opd-full-corpus-audit-workflow.md` (新建) | 全库审计 5 步流程 + 4 种高风险 pattern 自动检测 |
| `opd-triage-false-negative-cases.md` (更新) | 假阴性案例库，补充 IRIS/ThinkTuning 误判分析 |
| `awesome-list-update-workflow.md` (更新) | Awesome list 更新流程，补充 demote/promote 规范 |

---

## 🔁 PDF Compatibility

Legacy code may reference `papers/opd/<aid>.pdf`. A symlink keeps it alive:
```
/apdcephfs_cq8/.../openclaw_fsp/papers/opd  →  pdfs/by-aid/
```

---

## 🔄 Daily Automation

| Cron | Time (CST) | What |
|------|------------|------|
| `daily-opd-paper-pipeline` | 02:40 | Scout new papers + deep-read |
| `opd-scout-retry` | 06:40 | Retry failed scouts |

---

## 📜 Conventions

1. **PDF naming** — always `{arxiv_id}.pdf`
2. **PDF location** — date bucket by arXiv ID (`YYMM` prefix)
3. **Background papers** — in `pdfs/background/` (referenced for context, not OPD; includes game-theoretic self-play + classic KD + scaling law)
4. **Notes DB** — `paper_notes.json` is the single structured source; `.md` files are supplementary
5. **Scripts** — `generate_atlas_heatmap.py` is the ONLY heatmap script; all others deprecated
6. **Rejected papers** — move PDF to `.trash-YYYY-MM-DD/`, remove from DB, log to `papers-meta/excluded-papers.md`, 7-day retention
7. **OPD 三条件判定** — (1) training-time student rollouts (2) concurrent teacher supervision (3) per-step/iter weight updates. 三条全满足才是 OPD
8. **Audit cadence** — 每次大版本 (V3→V4) 或累积 >20 篇新论文时做一次 full corpus audit
