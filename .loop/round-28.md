# Round 28 — §6 Training Dynamics — POLISH

## 改动总结

Line-level prose pass on §6 (lines 919–1000). 重点是去 "namely"/"i.e." 冗余、softening overclaims、tightening sentence structure。

## 具体改动 (9 处)

| # | 位置 | 改动 | 原因 |
|---|------|------|------|
| 1 | L943 | "namely (1)..." → ": (1)..." | 去冗余 namely，用结构性冒号引出列表 |
| 2 | L950 | "a more principled solution, namely \emph{curriculum design} that..." → 断句 "a more principled solution. \emph{Curriculum design} actively selects..." | 拆长句，去 namely |
| 3 | L960 | "i.e., a trajectory that..." → ". A trajectory that..." | 去 Latin abbreviation，断句更清晰 |
| 4 | L987 | "(i.e., the teacher's output...)" → "(the teacher's output...)" | 去 i.e.，括号本身已是解释 |
| 5 | L999 | "three stages, namely the teacher..." → "three stages. The teacher..." | 去 namely，断句 |
| 6 | L999 | "uniformly surpass" → "consistently outperform" | overclaim → measured claim |
| 7 | L999 | "strictly lower" → "lower" | 去 overclaim（无 formal proof） |
| 8 | L935 | "The reasoning is that positions..." → "Positions..." | 去弱开头，直接陈述 |
| 9 | L944 | "...per rollout. This motivates..." → "...per rollout, motivating..." | 合并短句，减少 "This" 开头 |
| 10 | L968 | "the on-policy generation step provides a dual benefit..." → 拆长句 + "The observation offers..." | 拆 60+ 词句为两句 |

## 检查项
- [x] 无分号 (仅 math `Beta(p_i; α, β)` 保留)
- [x] 无 prose 冒号 (仅 structural `\textbf{X}:` 和 equation-introducing 冒号)
- [x] 无 "namely" in §6
- [x] 无 "i.e." in §6
- [x] 无 overclaiming ("uniformly surpass" → "consistently outperform")
- [x] 编译通过: 58p, 0 errors, 0 undefined

## Build
- Pages: 58
- Errors: 0
- Undefined: 0
- Citations: 118/118 match
