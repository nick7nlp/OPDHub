# Round 23 — POLISH §5 Signal Source

## 任务
Line-level prose polish pass on §5 (lines 768–918). 修剪弱动词、去冗余短语、tighten sentence structure。

## 改动清单

| 位置 | 原文摘要 | 改动 | 原因 |
|------|---------|------|------|
| ¶1 intro | "creating a core trade-off that practitioners must navigate" | → "a core trade-off that shapes every downstream design decision" | 去掉 "practitioners must navigate"（明显的话不必说）|
| ¶2 CoT | "instilling multi-step reasoning into" | → "transferring multi-step reasoning to" | 更精确 academic verb |
| White-box ¶1 | "which must be executed once per…" | → "executed once per…" | 去掉 unnecessary modal |
| Token-adaptive ¶ | 两句拆成一句 "They also compose…While…" | → 更紧凑的单句 + 独立短句 | 去掉 awkward "While" 开头 |
| Pre-training ¶ | 问句形式 "should it be viewed…?" | → "namely whether…" 陈述句 | 综述里避免 rhetorical question |
| Cross-tok alignment | "co-trained with the student, because…" | → "co-trained with the student because…" | 去掉 comma before "because"（restrictive） |
| Delta-KD | "The answer is not 'everything.'" | 删除 | 空洞过渡句 |
| Delta-KD | "(it wastes gradient budget…)" | → "because it wastes…" | 用 because 连接比括号更流畅 |
| ThinkTuning | "and is particularly effective" | → 去掉逗号 | tighten compound clause |
| GATES | "shows that" | → "demonstrates that" | stronger verb |
| OPSDL | "enabling stable optimization for context length scaling beyond…" | → "and enabling stable optimization for context lengths beyond…" | smoother parallel structure |
| CRISP | "turns out to be trainable inefficiency" | → "is trainable inefficiency" | 去掉 "turns out to be" filler |
| π-Play | "Self-play naturally produces a byproduct. During…" | → 合并为一句 | 减少断裂感 |
| External feedback ¶ | "that pure self-play cannot generate" | → "unavailable to pure self-play" | 更简洁 |
| SRPO | "the distinctive information each carries" | → "the information each carries" | "distinctive" 多余 |
| Closing ¶ | "indicating where future methods…" | → "revealing where future methods…" | stronger verb |

## 同时保留了 working-tree 已有的 4 处改动（前序 tick 未提交的）
- L803: 冒号 → 句号+新句
- L836: "A related challenge…" → "Not all training signal must originate on-policy."
- L881: ":"→ "---"（em-dash in SPIN stable sentence）
- L912: ":"→ ","（saturation analysis）

## 编译
- pdflatex OK, 58 pages, 0 errors, 0 undefined

## 总结
17 处 line-level 改动。主要消除弱动词 (shows → demonstrates, turns out to be → is, instilling → transferring)、去除冗余过渡 (The answer is not "everything")、收紧句子结构（fewer commas, merged fragments）。无内容/引用变动。
