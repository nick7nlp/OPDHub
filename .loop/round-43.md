# Round 43 — POLISH — §9 Future Directions

## 变更摘要

Line-level prose pass，15 处修改。主要改善：

### 改动清单

1. **开头段** — "trace a clear trajectory, from..." → em-dash list（更干净）；删掉 "that the field is"（冗余）；合并 "one in which" 为直接修饰
2. **Scaling laws 段** — "exhibiting rapid diminishing returns in student scale" → "indicating sharply diminishing returns as student capacity grows"（更精确动词 + 自然语序）
3. **Scaling laws 段** — "interacts non-trivially with scale" → "compounds favorably with scale"（"non-trivially" 是 filler，给出具体方向）
4. **Uncertainty 段** — "must incorporate" → "should incorporate"（survey 不用 must 命令读者）；"allowing" → "enabling"
5. **Agent-level 段** — 删 "dramatically"（filler 副词）
6. **Lifelong 段** — "is being updated" → "evolves"（更紧凑）；加 "achieving"（连接后面三个 without 更顺）
7. **Efficiency 段** — 括号注释 → em-dash pair（更 formal）；"A promising underexplored direction is X---MiniPLM shows" → 分成两句（原句过长）；"avoiding" → "skipping"（同前面 "avoid" 重复）
8. **Latent-space 段** — 加逗号 before "bypassing"（分词短语应有逗号）
9. **Privacy 段** — "correspondingly" → "increasingly"（更精确）；逗号分隔 → em-dash（parallel with others）
10. **Diagnostic 段** — "A natural extension of understanding uncertainty" → "A natural extension of uncertainty-aware training"（更具体）；删 "A critical future direction is developing" 改为 "would fill this gap"（避免多个 "direction" 重复）；"This capability" → "Such probes"（更具体指代）
11. **Cross-arch 段** — "can bridge...without imposing prohibitive compute overheads" → "bridge...without prohibitive compute overhead"（删 can + 单数）
12. **Scheduling 段** — "would likely depend" → "would depend"（去 hedge）；"smoothly" 删（filler）；"suggesting" → "implying"（更强）
13. **Closing loop 段** — 逗号分隔列表 → em-dash pair（privacy 等同处理一致化）；"are historically treated" → "The field has historically treated"（主动语态）
14. **Self-improving 段** — 逗号分隔 parenthetical → em-dash pair（一致性）
15. **最后句** — "ensuring that RL-discovered capabilities are not overwritten" → "preventing RL-discovered capabilities from being overwritten"（更 direct）

### 编译结果
- 59 pages
- 0 LaTeX errors
- 0 undefined references
- 无 semicolons，无 prose colons

### 未改动（留给后续 tick）
- 全 section 无 semicolons（已 clean）
- "The logical endpoint of the trajectories surveyed here" 稍重但可接受
- 几个段落仍然偏长（Closing the loop 段 ~8 句），但拆分会破坏论证连贯性
