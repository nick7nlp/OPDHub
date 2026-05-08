# Round 27 — DEEPEN §6 Training Dynamics

**Mode**: DEEPEN  
**Section**: §6 Training Dynamics and Efficiency  
**Agent**: cron tick 27  
**Source**: Round 25 READ + Round 26 VERIFY findings  

## Edits Applied

### Fix 1: Fast OPD framing (HIGH priority) ✅

**Before**: "observes that exposure bias is concentrated in the early tokens of a sequence, where errors compound most severely"

**After**: "observes that the useful distillation signal (measured by per-token reverse-KL loss) is concentrated in the prefix of student-generated sequences, because the student is weakest at high-level planning decisions captured in early tokens"

**Reasoning**: 原文 (2602.15260 §2.2) 的 argument 是 signal concentration（prefix 包含最多有用信号），不是 error compounding。这是一个 efficiency observation，论文通过测量每个 token 位置的 loss 发现 prefix 贡献最大。还加上了具体的 speedup 数字（2-47×）和 task-dependent truncation 的解释（math 用短 prefix 因为 planning 在开头，open-ended 需要长）。

### Fix 2: PACED Beta-kernel generalization (MEDIUM priority) ✅

**Before**: "the expected gradient magnitude scales as p(1-p), which is maximized at p=0.5 and vanishes at both extremes. PACED's Beta-kernel sampling directly optimizes for this quantity"

**After**: 明确了 p(1-p) 只是 general Beta-kernel family w(p)=p^α(1-p)^β 的对称特殊情况。加了 asymmetric choices 的实际意义——early training 用 α>β（偏 moderate difficulty），late training 用 α<β（偏 hard cases）。这比原来的 "directly optimizes for p(1-p)" 更准确地反映论文内容（论文 emphasis 在 general family 不是单一 symmetric case）。

### Fix 3: AdaSwitch mechanism (MEDIUM priority) ✅

**Before**: "maintains a running estimate of the student's cumulative prefix quality"

**After**: 完整描述了实际机制——sliding window of length L over recent token divergences, running average d̄_i, context-adaptive threshold τ_i = K·d̄_{i-1}。还解释了 WHY adaptive threshold matters（fixed threshold 要么 too aggressive 要么 too permissive）。

### Fix 4: Cost example caveat (LOW priority) ✅

**Before**: 直接说 "~300 GPU-hours" / "~1,200-1,500 GPU-hours" 没有来源

**After**: 加了 "representative estimates based on scaling from reported benchmarks" 和 citation to Lightning OPD for the 4-5× ratio。读者不会误以为这是 measured values 了。

### Enhancement: Spectrum analysis paragraph deepened

**Before**: 简单说 fine-to-coarse tradeoff + practitioner guidance

**After**: 加了 WHY 这个 tradeoff 不仅是理论的——fine-grained methods 恰好在 flawed prefix 最严重时 degrade（因为需要 reliable token-level teacher signals），coarse-grained methods robust 因为一个 bad token 不污染整条 trajectory。加了 concrete examples（reasoning chains vs multi-turn dialogue）。

## Build Status

- ✅ pdflatex pass: 58 pages, 0 errors, 0 undefined references
- No new citations needed (all fixes reference existing methods)

## Summary

4 targeted edits + 1 deepening enhancement。核心改动都是 factual accuracy improvements based on r26 VERIFY。没有 rewrite whole paragraphs，只改 specific claims 和 framing。所有改动提供了更多 WHY（not just WHAT），和更 precise 的 mechanism description。
