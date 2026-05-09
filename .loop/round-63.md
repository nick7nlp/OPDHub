# Round 63 — POLISH — §3.1 Method Landscape

## 改了什么

Line-level prose polish，目标是消除 prose colon、拆长句、去 filler。

### 修改清单

1. **§3.1 第二段（stages interdependence）**:
   - "incompatible: Forward KL" → "incompatible. Forward KL" — 消除 prose colon
   - "synergistic: RL-augmented" → "synergistic. RL-augmented" — 同上
   - "This interdependence implies that an objective choice constrains" → "An objective choice therefore constrains" — 去掉冗余前缀，直接陈述

2. **§3.1 第一段结尾**:
   - "illustrate that" → "confirm" — 更 crisp

3. **§3.2 Classification methodology**:
   - 原文用 "if...it belongs to...If it introduces...If it solves..." 的长链条件句，重构为独立短句
   - "This strict one-method-one-category rule reduces" → 合并到前一句尾 "reducing..."
   - 删除 prose colon (原 "based on its core contribution dimension: if")

4. **§3.2 Table organization**:
   - 拆长尾句 "enabling practitioners..." → 独立句 "Practitioners can use it to..."

## 写作规则检查

- EM-DASH: ✅ 无违规
- PROSE COLON: ✅ 修复 2 处，无残留
- SEMICOLON: ✅ 无违规
- Filler words: ✅ 无 "moreover/furthermore/notably"

## 编译

- pdflatex 通过, 0 errors, 0 undefined
- 60 pages (与上一 round 一致)
