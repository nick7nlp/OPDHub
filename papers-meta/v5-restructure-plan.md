# V5 结构重构方案：新增 §7 Agentic and Multi-Turn OPD

> 2026-08-12。目标：把散落在 7 个章节的 agentic OPD 内容收拢成独立章节，**消除冗余但不丢信息**。

## 1. 切分判据（唯一标准）

| 判据 | 归属 |
|---|---|
| 换成单轮任务，问题依然存在 | **留原章节** |
| 换成单轮任务，问题消失 | **进 §7** |

理由：agentic OPD 不是「OPD 的一个应用领域」，而是产生了单轮不存在的新机制类别（turn 级信用、state 改写错配、跨轮误差累积）。按「问题归属」切分而非「论文归属」切分，才能避免同一篇论文在多章重复展开。

## 2. 现存冗余（必须消除）

同一组论文（TCOD / TT-OPD / Skill-SD / MAD-OPD）在四处各讲一次：

| 现有位置 | 行 | 视角 | 处理 |
|---|---|---|---|
| §5.3.1 Privileged Information | L1077–1079 | turn 级 PI 粒度谱系 | **迁入 §7.2**，原处留指针 |
| §6.2 Curriculum | L1246 | TCOD temporal depth 轴 | **迁入 §7.4**，原处保留难度轴论述 + 指针 |
| §7.2 Failure Modes | L1348–1350 | agentic collapse 三病理 | **迁入 §7.5**，原处留指针 |
| §8.1 Industrial Deployment | L1421–1423 | 误差累积 + TCOD 机制 | **与 L1246 合并**至 §7.4；§8.1 只保留部署视角一句话 |

**关键**：L1246 与 L1421 描述的是 TCOD 的同一机制（控制监督时间深度），当前是实质重复。合并后只在 §7.4 展开一次。

## 3. §7 章节结构

```
§7 Agentic and Multi-Turn On-Policy Distillation        \label{sec:agentic}
   7.1 Why Single-Turn OPD Breaks Down                  \label{subsec:agentic_why}
   7.2 Turn-Level Credit Assignment                     \label{subsec:agentic_credit}
   7.3 State and Memory Alignment                       \label{subsec:agentic_state}
   7.4 Temporal Depth and Rollout Budget                \label{subsec:agentic_depth}
   7.5 Agentic Failure Modes                            \label{subsec:agentic_failure}
```

原 §7 Understanding OPD → **§8**；原 §8 Applications → **§9**；原 §9 Open Problems → **§10**。

### 7.1 Why Single-Turn OPD Breaks Down（新写）

承接 §2.2 exposure bias 的 DAgger 论证，给出多轮版本：
- state occupancy 偏移从 token 级升级到 environment state 级
- 一个错误动作改变整个环境状态，后续教师监督全部落在偏移分布上
- 上下文改写（compact memory）导致教师对**学生未访问过的状态**打分

必须显式 `\citep` §2.2 的 DAgger 界，保持逻辑链不断。

### 7.2 Turn-Level Credit Assignment
迁入：L1077–1079（PI 粒度谱系）
新增：ATOD `2606.27814`、TurnOPD `2607.05804`、Trajectory-Relative `2608.07371`、GAPD `2605.29584`、UCOB `2606.29502`

### 7.3 State and Memory Alignment（全新小节）
新增：MemOPD `2608.07068`、Prefix Replay `2607.04763`、Look Ahead `2608.01953`、Reading-is-not-Reasoning `2608.08960`

### 7.4 Temporal Depth and Rollout Budget
合并：L1246 + L1421（TCOD 机制只讲一次）
新增：DASH-OPD `2607.29078`、PCSD `2608.01837`

### 7.5 Agentic Failure Modes
迁入：L1348–1350（agentic collapse）
新增：KbSD `2606.29863`、Two-Phase Agentic `2606.30044`、Physics of Multi-Turn `2607.24720`

## 4. 新增 73 篇的归属

| 目标 | 篇数 |
|---|---:|
| **§7（多轮独有贡献）** | **14** |
| 留原章节（机制通用） | 59 |

进 §7 的 14 篇：
`2606.29863` `2606.30044` `2607.04763` `2606.27814` `2608.07068` `2607.24720` `2605.29584` `2606.29502` `2608.07371` `2608.08960` `2608.01837` `2608.01953` `2607.05804` `2607.29078`

判据：贡献机制本身依赖多轮结构。反例——跨词表 `2607.22334`、扩散 `2607.16872`、Hellinger `2607.06855` 虽可用于 agent，但机制与轮次无关，**留在 §4**。

## 5. 防止信息丢失的三个机制

**(1) 单向指针，不双向复述**

原章节保留本章视角的论述，末尾加一句指向 §7，**不重复机制细节**：
```latex
% §6.2 末尾
Temporal-depth scheduling, which is specific to multi-turn trajectories,
is treated in Section~\ref{subsec:agentic_depth}.
```
同一机制**只在一处展开**。

**(2) §7.1 承接前文逻辑链**

显式引用 §2.2（`subsec:f-div` 前的 exposure bias 推导），让读者从单轮 DAgger 界自然过渡到多轮状态偏移，不出现概念断层。

**(3) 表格全量保留，正文只讲代表**

§3.2 Method Comparison Table 保留全部 agentic 论文，新增一列标注 `multi-turn`。这样 37+ 篇 agentic 工作全部可检索，但正文只展开有独特机制的，避免正文膨胀。

## 6. 多模态 13 篇：不独立成章

判断：多模态 OPD 的技术问题（视觉 PI、模态 gap）是**PI 的实例化**，未产生新机制类别。
处理：留在 §5.3 + §9 Emerging Domains，在 §5.3 下增设一个归拢小节即可。

## 7. 执行顺序

1. 在 §6 之后插入 §7 骨架与 5 个 label
2. 迁移 4 处现有段落（L1077/L1246/L1348/L1421），原处替换为指针
3. 合并 L1246+L1421 的 TCOD 重复论述
4. 写 §7.1（全新，承接 §2.2）
5. 把 14 篇新论文写入 §7.2–7.5
6. 其余 59 篇按原章节归属写入
7. 更新 §3.2 表格（加 multi-turn 列）
8. 全文 `\ref` 一致性检查 + 编译验证

## 关键文件

- `latex-v5/main.tex` — 结构与正文
- `latex-v5/references.bib` — 新增 73 条（223 → 296）
- `papers-meta/v5-integration-backlog.md` — 73 篇清单
