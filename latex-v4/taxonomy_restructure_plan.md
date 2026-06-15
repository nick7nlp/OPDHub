# OPD Survey Taxonomy Restructure Plan

## 背景

对比 Hallucination Survey (2309.01219) 和 Long CoT Survey (2503.09567) 的分类方法论后，发现我们 §5 Signal Source 的顶层分类存在维度混用问题。本文档给出具体改法，供 agent 执行。

---

## 问题诊断

当前 §5 的顶层三分：

```
§5 Signal Source
├── §5.1 White-Box Logit Supervision (10)
├── §5.2 Black-Box and API-Constrained (10)
└── §5.3 Self-Distillation (55)
```

White-Box 和 Black-Box 是 **teacher access level**（工程约束维度），Self-Distillation 是 **teacher identity**（有没有外部 teacher，方法论维度）。这两个维度并列成 peer categories 不干净。

对比参考：
- Hallucination survey 的 mitigation taxonomy 完全沿单一维度（LLM 生命周期阶段）切分
- Long CoT survey 的三能力维度都属同一维度层级（Short CoT 的约束放松方式）

## 改法：嵌套二级切分

先按 **teacher identity** 分（是否有外部 teacher），再在 External Teacher 内部按 **access level** 分。

### 新结构

```
§5 Signal Source and Teacher Architecture
│
├── §5.1 External Teacher Distillation
│   ├── §5.1.1 White-Box Logit Supervision
│   │   ├── Same-Family Distillation (4 methods)
│   │   └── Cross-Family Distillation (6 methods)
│   └── §5.1.2 Black-Box and API-Constrained (10 methods)
│
└── §5.2 Self-Distillation
    ├── §5.2.1 Privileged Information (23 methods)
    ├── §5.2.2 Pure Self-Distillation (17 methods)
    └── §5.2.3 External Feedback (15 methods)
```

### 对比旧结构

```
旧:
§5.1 White-Box (10)         → 新 §5.1.1
§5.2 Black-Box (10)         → 新 §5.1.2
§5.3 Self-Distillation (55) → 新 §5.2

旧: 3 个 peer categories，混两个维度
新: 2 个 peer categories（External vs Self），内部各自沿一个维度展开
```

---

## 具体修改清单

### 1. §3.1 Method Landscape 文字（~L200-202）

**旧文字：**
> Existing OPD methods can be organized along three axes that correspond to sequential design decisions in the training pipeline: (1) the objective function to optimize, (2) the source of the supervisory signal, and (3) the mechanism for stabilizing training dynamics.

**改为：**
> Existing OPD methods can be organized along three axes that correspond to sequential design decisions in the training pipeline: (1) the objective function to optimize, (2) the source of the supervisory signal, and (3) the mechanism for stabilizing training dynamics. For the signal source axis, we adopt a two-level classification. The first level distinguishes **external teacher distillation** (where a separate, typically stronger model provides supervision) from **self-distillation** (where the model generates its own training signal). The second level within external teacher distillation further separates methods by **access level**: white-box methods that require the teacher's full output distribution versus black-box methods that operate with only generated text or scalar scores. This nested structure reflects the fact that teacher identity (external vs. self) and teacher access level (white-box vs. black-box) are orthogonal design dimensions that should not be conflated.

### 2. §3.1 加正交性论证段（在 L202 之后，taxonomy 图之前）

新增段落：

> **Formal grounding of the three axes.** The unified OPD objective in Eq. (8) decomposes into three independent design choices that map one-to-one onto the taxonomy axes. The $f$-divergence generator $f$ determines the **objective function** (Axis 1: §4), governing whether the student is mode-seeking, mode-covering, or adaptive. The identity and access level of the entity supplying $p_T(\cdot | x, y_{<t})$ determines the **signal source** (Axis 2: §5): an external teacher with full logit access, an external teacher with only text/score outputs, or the model's own conditionally privileged distribution. The sampling policy $\pi_{\mathrm{mix}}$ and its scheduling determine the **training dynamics** (Axis 3: §6), including the interpolation coefficient $\lambda$, curriculum over prompt difficulty, and token-level weighting. These three choices are largely orthogonal: a fixed Forward KL objective (Axis 1) can be paired with either white-box logits or black-box scores (Axis 2) and with either uniform sampling or curriculum-based pacing (Axis 3). The taxonomy thus reflects the structure of the optimization problem itself rather than an ad-hoc grouping.

### 3. Figure 1 (taxonomy tree) 修改

当前 forest 结构（~L277-321）需要改为嵌套结构。改动点：

**旧：**
```
§5 Signal Source and Teacher Architecture
├── §5.1 White-Box Logit Supervision
│   ├── 5.1.1 Same-Family (4)
│   └── 5.1.2 Cross-Family (6)
├── §5.2 Black-Box and API-Constrained (10)
└── §5.3 Self-Distillation
    ├── 5.3.1 Privileged Information (23)
    ├── 5.3.2 Pure Self-Distillation (17)
    └── 5.3.3 External Feedback (15)
```

**新：**
```
§5 Signal Source and Teacher Architecture
├── §5.1 External Teacher Distillation
│   ├── §5.1.1 White-Box Logit Supervision (10)
│   │   ├── Same-Family (4)
│   │   └── Cross-Family (6)
│   └── §5.1.2 Black-Box and API-Constrained (10)
└── §5.2 Self-Distillation (55)
    ├── §5.2.1 Privileged Information (23)
    ├── §5.2.2 Pure Self-Distillation (17)
    └── §5.2.3 External Feedback (15)
```

TikZ forest 代码改动：在 `§5 Signal Source` 节点下，把 White-Box 和 Black-Box 包进一个新的中间节点 `§5.1 External Teacher Distillation`（用 catSigMid 样式），Self-Distillation 升级为 `§5.2`。

具体改法——把 L278-321 的 forest 子树替换为：

```latex
%% ===== Stage 2: Signal Source and Teacher Architecture (§5) =====
[{§5 Signal Source and\\Teacher Architecture}, catSig, edge={draw=sdcolor!60, line width=1.2pt}
  %% --- §5.1 External Teacher ---
  [{{§5.1 External Teacher\\Distillation}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{20};}}, catSigMid, edge={draw=sdcolor!30}
    [{{§5.1.1 White-Box Logit Supervision}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{10};}}, catSigMid, edge={draw=sdcolor!30}
      [{\textbf{Same-Family}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{4};}\\[2pt]%
        MAD-OPD, MPD, BRTS, Pair-In Pair-Out%
        }, leaf=sdcolor, edge={draw=sdcolor!30}]
      [{\textbf{Cross-Family}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{6};}\\[2pt]%
        Veto, PromptKD, DSKD, CSD, SimCT, DuDi%
        }, leaf=sdcolor, edge={draw=sdcolor!30}]
    ]
    [{\textbf{§5.1.2 Black-Box and API-Constrained}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{10};}\\[2pt]%
      Lion, GAD, OVD, LUFFY, DASD,\\[1pt]%
      DDT, PRISM, ROPD, ORPO-Distill, OmniOPD%
      }, leaf=sdcolor, edge={draw=sdcolor!30}]
  ]
  %% --- §5.2 Self-Distillation ---
  [{{§5.2 Self-Distillation}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{55};}}, catSigMid, edge={draw=sdcolor!30}
    [{\textbf{§5.2.1 Privileged Information}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{23};}\\[2pt]%
      OPSD, GATES, π-Distill, OPCD, OEL, HDPO, ...%
      }, leaf=sdcolor, edge={draw=sdcolor!30}]
    [{\textbf{§5.2.2 Pure Self-Distillation}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{17};}\\[2pt]%
      SDFT, MTP-SD, UniSD, VPG, ...%
      }, leaf=sdcolor, edge={draw=sdcolor!30}]
    [{\textbf{§5.2.3 External Feedback}~{\tikz[baseline=-0.5ex]\node[badge=sdcolor]{15};}\\[2pt]%
      SDPO, SD-ZERO, RLSD, SRPO, ...%
      }, leaf=sdcolor, edge={draw=sdcolor!30}]
  ]
]
```

注意：叶节点的完整 cite 列表保持不变，上面用 `...` 省略是为了可读性，实际代码要保留全部 `\citep{}`。

### 4. §5 正文结构调整

**旧节结构：**
```
\section{Signal Source and Teacher Architecture}  % §5
\subsection{White-Box Logit Supervision}          % §5.1
  \subsubsection{Same-Family Distillation}        % §5.1.1
  \subsubsection{Cross-Family Distillation}       % §5.1.2
\subsection{Black-Box and API-Constrained}        % §5.2
\subsection{Self-Distillation}                    % §5.3
  \subsubsection{Privileged Information}          % §5.3.1
  \subsubsection{Pure Self-Distillation}          % §5.3.2
  \subsubsection{External Feedback}               % §5.3.3
```

**新节结构：**
```
\section{Signal Source and Teacher Architecture}  % §5
\subsection{External Teacher Distillation}        % §5.1  ← 新增包裹层
  \subsubsection{White-Box Logit Supervision}     % §5.1.1 (原 §5.1)
    % Same-Family 和 Cross-Family 降为 \paragraph 级别
    \paragraph{Same-Family Distillation.}
    \paragraph{Cross-Family Distillation.}
  \subsubsection{Black-Box and API-Constrained}   % §5.1.2 (原 §5.2)
\subsection{Self-Distillation}                    % §5.2  (原 §5.3)
  \subsubsection{Privileged Information}          % §5.2.1 (原 §5.3.1)
  \subsubsection{Pure Self-Distillation}          % §5.2.2 (原 §5.3.2)
  \subsubsection{External Feedback}               % §5.2.3 (原 §5.3.3)
```

需要改的 label：
- `\label{subsec:white_box}` → 保留，但变为 subsubsection
- `\label{subsec:black_box}` → 保留，但变为 subsubsection
- `\label{subsec:self_distill}` (如果有) → 变为 `\label{subsec:self_distill}`

新增 `\subsection{External Teacher Distillation}` 需要一段引言（2-3 句），内容：

> External teacher distillation assumes access to a separate model whose capabilities exceed the student's on the target task distribution. The teacher's role is to supply corrective signals on the student's on-policy rollouts. The two subsections below distinguish methods by the density of that signal: full logit access (Section~\ref{subsec:white_box}) yields the richest per-token supervision but requires co-hosting the teacher, while API-constrained settings (Section~\ref{subsec:black_box}) sacrifice signal density for deployment flexibility.

### 5. §5 开头段落（~L805-807）修改

**旧：**
> With the objective function fixed (Section~\ref{sec:objectives}), the next design axis concerns \emph{where the teacher signal comes from}: full logit access (white-box), API-only text outputs (black-box), or the model's own internal asymmetries (self-distillation). Each signal source imposes distinct constraints on the applicable objectives and achievable performance.

**改为：**
> With the objective function fixed (Section~\ref{sec:objectives}), the next design axis concerns \emph{where the teacher signal comes from}. We organize signal sources along two levels. The first level distinguishes external teacher distillation, where a separate stronger model provides supervision, from self-distillation, where the model generates its own training signal by exploiting internal asymmetries. Within external teacher distillation, the second level separates white-box methods that access the teacher's full output distribution from black-box methods that operate with only generated text or scalar scores. This nested structure reflects two orthogonal dimensions: teacher identity (who provides the signal) and access level (how much of that signal is observable). Each combination imposes distinct constraints on the applicable objectives and achievable performance.

### 6. §5 第二段（~L807，historical progression）修改

**旧：**
> Historically, signal sources have evolved in step with model access constraints. Early OPD methods (GKD, DistiLLM) assumed full white-box access... This progression from full access through limited access to no external access represents increasing autonomy at the cost of signal density...

**改为：**
> Historically, signal sources have evolved along both dimensions. The access-level dimension progressed first: early OPD methods (GKD, DistiLLM) assumed full white-box access, while the rise of proprietary API-only models (GPT-4, Claude) necessitated black-box methods. The teacher-identity dimension shifted later: self-distillation methods (OPSD, SD-ZERO) removed the external teacher entirely, permitting continuous improvement without access to any stronger model. This two-dimensional progression—from full access to limited access along one axis, and from external teacher to self-teaching along the other—represents increasing autonomy at the cost of signal density, and the two trade-offs are largely independent.

### 7. 全文 \ref 更新

所有引用旧编号的地方需要检查：
- `Section~\ref{subsec:white_box}` → 仍然有效（label 不变，只是层级变了）
- `Section~\ref{subsec:black_box}` → 仍然有效
- 涉及 "§5.1" / "§5.2" / "§5.3" 的**硬编码文字**需要更新：
  - "§5.1 leaf" (L347 caption) → "§5.1.1 leaf"
  - "§5.3 in their report" (L1394 Safactory) → 这引的是 Safactory 论文内部的编号，不是我们的，不改
  - 全局搜索 `\\S 5.1` `\\S 5.2` `\\S 5.3` 确认每处是指我们的还是别人论文的

### 8. Table headers 更新

Tables 5（白盒方法表）和 6（黑盒方法表）的 Category 列值需要从 "Signal" 改为更精确的 "Signal (External/White-Box)" 和 "Signal (External/Black-Box)"，或者保持 "Signal" 不变但在表 caption 里加说明。建议保持 "Signal" 不变以避免表格过宽。

### 9. §3.3 Method Selection Considerations 更新

L491 的 "Teacher access constraints" 段落目前三分（White-box / API-only / no external teacher），改为两层叙述：

> **Teacher identity and access constraints.** The first selection criterion is whether an external teacher is available. When it is, the access level determines which objectives are feasible. White-box logit access enables exact token-level divergence computation... API-only access restricts supervision to generated text or scalar scores... When no external teacher is available, self-distillation methods operate either through privileged information... or through verifier-guided self-improvement...

---

## 不需要改的部分

- §4 Objective Functions：不涉及 signal source 维度，不受影响
- §6 Training Dynamics：不涉及 signal source 维度，不受影响
- §7 Understanding OPD：failure modes 引用的是具体方法名而非 §5 编号，基本不受影响
- §8 Applications：同上
- §9 Future Directions：同上
- 方法归属：所有方法在新旧结构下的归属完全不变，只是层级关系变了

## Takeaway 闭合段（附赠改进）

趁改 §5 结构的同时，在以下位置各加一段 2-3 行的 takeaway paragraph：

1. §5.1 External Teacher Distillation 末尾（§5.1.2 Black-Box 之后）：
   > **Takeaway.** External teacher distillation offers the highest signal density in OPD but imposes access-dependent constraints. White-box methods achieve the tightest distributional alignment through full-vocabulary KL but require co-hosting the teacher, while black-box methods trade signal density for deployment flexibility. The key unresolved tension is that the strongest teachers (proprietary frontier models) are typically accessible only through APIs, precisely the setting where OPD's theoretical advantages are hardest to realize.

2. §5.2 Self-Distillation 末尾（§5.2.3 External Feedback 之后）：
   > **Takeaway.** Self-distillation has emerged as the dominant signal source paradigm by volume (55 of 75 signal-source methods), driven by its zero-cost teacher requirement. The three sub-categories exploit fundamentally different asymmetries: privileged-information methods leverage conditional distribution gaps, pure self-distillation leverages temporal or checkpoint gaps, and external-feedback methods outsource evaluation to verifiers. The principal limitation across all three is self-play saturation (Section~\ref{subsec:failure}): without external grounding, the model's hypothesis space gradually contracts. The practical implication is that self-distillation methods benefit from being composed with at least one external signal source (even a simple rule-based verifier) to prevent distributional collapse.

3. §4 各 subsection 和 §6 各 subsection 也建议加 takeaway，但不在本次改动范围内，可后续补。

---

## 优先级与依赖

1. 先改 §5 正文结构（item 4-6）→ 确保编译通过
2. 再改 taxonomy 图（item 3）→ forest 嵌套层级
3. 再改 §3.1 文字和正交性论证（item 1-2）
4. 最后全局搜索更新 \ref 和硬编码编号（item 7）
5. Takeaway 段可以最后加
