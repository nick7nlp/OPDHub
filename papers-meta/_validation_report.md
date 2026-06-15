# Paper Validation Report

Generated: 2026-06-03 15:55 CST


- awesome paper rows: **199**
- site papers:        **165**
- arxiv API checked:  **180**


## A. arxiv ID 404 / 不存在 (致命: 编造的引用) — 0

**红旗** — 这些 id 在 arxiv 上找不到, 必须删除并人工调查来源。


_无问题_


## B. 标题不一致 (README / notes / arxiv canonical) — 0

标题串错, 可能是手工 typo 或粘错论文。


_无问题_


## C. § 分类不一致 (README vs v3 LLM) — 0

v3 LLM 判定的 primary_section 跟 README 收录位置不同, 可能 inserter 当时填错。


_无问题_


## F. v3 判 is_opd=no 但仍在 awesome (违反 scope 铁律) — 0

应该从 awesome+site 删掉, 跟 SPIN/IRIS 同性质。


_无问题_


## E. 启发式检测疑似 self-play 边界反例 — 0

loss 形式上是 DPO 二分类 / Rényi 自博弈, 需要人工二审是否真是 OPD。


_无问题_
