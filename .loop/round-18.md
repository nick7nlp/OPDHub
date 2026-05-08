# Round 18 — POLISH §4 Objectives

**Mode**: POLISH  
**Section**: §4 Objective Functions and Optimization (lines 570–767)  
**Focus**: Prose colons, filler words, sentence tightening, weak constructions

---

## Changes Made

### 1. Prose colon → em-dash equivalent (line 746)

**Before**: `...documented as \emph{Reward Extrapolation}: the student discovers novel...`  
**After**: `...documented as \emph{Reward Extrapolation}, whereby the student discovers novel...`

理由: 正文禁止冒号，改为逗号+whereby 保持因果关系明确。

### 2. Removed filler "actually" (line 715)

**Before**: "...determines how much of the teacher's distribution is **actually** used..."  
**After**: "...determines how much of the teacher's distribution is used..."

理由: "actually" 是 filler，不增加信息量。

### 3. Tightened REOPOLD sentence (line 749)

**Before**: 一个超长句带嵌套括号解释三个机制  
**After**: 拆成两句——第一句说 interpretation，第二句列三个 mechanism 用冒号引出（结构性冒号 OK）

具体改动: "operationalizes this insight, interpreting...and stabilizing training through X (Y), Z (W), and Q" → "operationalizes this insight by interpreting... It stabilizes training through three mechanisms: X to Y, Z to W, and Q"

### 4. Tightened RLAD trailing clause (line 757)

**Before**: "...ignores it otherwise, a principled solution to the problem that blind KL minimization can drag the student toward suboptimal trajectories on problems the teacher itself struggles with."  
**After**: "...preventing blind KL minimization from dragging the student toward suboptimal trajectories on problems the teacher itself cannot solve."

理由: "struggles with" → "cannot solve" 更精确；去掉 "ignores it otherwise, a principled solution to the problem that" 这种绕路表达。

### 5. Tightened "namely that" construction (line 760)

**Before**: "This exploits a structural property of reasoning chains, namely that errors cascade, so correcting the root cause..."  
**After**: "This exploits the cascading nature of reasoning errors: correcting the root cause..."

理由: "structural property of reasoning chains, namely that errors cascade" → "cascading nature of reasoning errors" 压缩了 10 个词到 5 个，信息不变。此处冒号是结构性的（引出具体机制），保留。

### 6. Removed "simply" filler (line 763)

**Before**: "...rather than simply mimicking its outputs."  
**After**: "...rather than mimicking its outputs."

### 7. "validating empirically that" → "confirming that" (line 587)

**Before**: "...validating empirically that the optimal divergence is data-source-dependent."  
**After**: "...confirming that the optimal divergence is data-source-dependent."

理由: "validating empirically" 是冗余的（上下文已经在讨论实验结果）。

---

## Build Stats

- pdflatex: ✅ clean
- Errors: 0
- Undefined refs: 0
- Citation warnings: 0
- Pages: 58 (unchanged)

## Quality Assessment

§4 整体写作质量很高。没有 AI filler、没有分号、没有 "no one has done X" 式 overclaim。主要问题是个别超长句和零星 filler word。7 处微调后句子更紧凑，信息密度提升。

## No further action needed for this section's prose pass.
