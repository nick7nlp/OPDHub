# Round 02 — §1 Introduction DEEPEN

**Mode**: DEEPEN  
**Section**: §1 Introduction  
**Source**: round-01.md (VERIFY findings) + round-01-seed.md (READ issues)

## Changes made (5 targeted edits)

### 1. Overclaim fix: "near-human competence" → SOTA language
- **Before**: "achieving near-human competence in reasoning, code generation, and multilingual instruction following"
- **After**: "achieving state-of-the-art performance across reasoning, code generation, and multilingual benchmarks"
- **Why**: Round-01 VERIFY showed "near-human" is overclaim — papers show benchmark wins (AIME 79.8%, Codeforces 2029 elo), not general human-level competence

### 2. KD re-purposing narrative deepened (¶1)
- **Before**: "What was once a compression tool has become a general mechanism for moving capabilities across model scales"
- **After**: "What was originally a model compression technique, designed to transfer knowledge from a large classifier into a smaller one of the same architecture, has become a general mechanism for moving capabilities across model scales and even across architectural families"
- **Why**: Makes the paradigm shift more explicit — from same-arch compression to cross-arch capability transfer. This is why DeepSeek-R1 (MoE→dense) is such a compelling example right after

### 3. Verb strengthening (¶3)
- **Before**: "drifts into the very states it would visit at deployment"
- **After**: "populates the very states it would visit at deployment"
- **Why**: "drifts" implies passivity/accident; "populates" implies active/intentional, which better matches OPD's purposeful exploration

### 4. GKD "first unified" → concurrent acknowledgment
- **Before**: "GKD introduced the first unified on-policy framework for LLM distillation in mid-2023, and fewer than three years later"
- **After**: "GKD, alongside the concurrent MiniLLM, introduced the first on-policy frameworks for autoregressive LM distillation in mid-2023, and fewer than two years later"
- **Why**: Round-01 VERIFY confirmed MiniLLM (2306.08543) is literally concurrent (both Jun 2023, both ICLR 2024). Also fixed "three years" to "two years" (2023.6→2025.5 ≈ 2 years)

### 5. "architecturally necessary" grounded with cites
- **Before**: "making on-policy correction not merely beneficial but architecturally necessary for the next generation of reasoning-capable systems."
- **After**: "making on-policy correction not merely beneficial but arguably architecturally necessary for the next generation of reasoning-capable systems~\citep{2603.25562,deepseekv4}."
- **Why**: Editorial claim was unsupported. "arguably" hedges appropriately; \citep{2603.25562} (Revisiting OPD) and \citep{deepseekv4} provide evidence base

## Build verification
- `pdflatex` pass: ✅ clean
- 0 LaTeX errors, 0 undefined controls, 0 undefined citations
- Page count: 57 (unchanged)

## Remaining §1 issues for future rounds
- ¶1 sentence 2 is 60+ words — could benefit from splitting (POLISH mode)
- ¶4 "gradually exposing the fact that" — could be tighter (POLISH mode)
- The "fewer than two years" claim is correct for 2023→2025, but survey text goes to 2026 — OK because the cited literature already existed by mid-2025

## 质量评估
五处改动全部精确对应 VERIFY 发现的问题。没有大规模重写，都是 surgical edit。¶1 的 re-purposing narrative 让读者更清楚为什么 DeepSeek-R1 是 milestone — 不只是 scale up KD，而是跨架构(MoE→dense)的 capability transfer。
