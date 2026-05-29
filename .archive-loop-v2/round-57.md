# Round 57 — DEEPEN — §2 Background

基于 round 55 (READ) 和 round 56 (VERIFY) 的发现，针对性改写 4 处。

## 修改内容

### 1. DAgger bound vs independent compounding (line 160)

**问题**: 原文用 (0.95)^10 ≈ 60% 做例子但没区分 independent error compounding (指数衰减) 和 DAgger bound (quadratic distributional shift)。读者可能以为两者是一回事。

**改动**: 
- 明确说 (0.95)^10 是最简单的 independent-error 假设
- 解释 DAgger bound 预测的 O(εT²) 是**更糟糕的**，因为 distributional shift 导致 per-step accuracy 本身在 off-policy 下退化
- 用 "vicious cycle" 和 "distributional drift amplifying local mistakes" 连接因果

**为什么这样写**: 让读者理解 on-policy 解决的不仅是 probability multiplication 问题（trivial），而是 distribution shift compounding（深层原因）。

### 2. JSD on translation — WHY not just WHAT (line 187)

**问题**: 原文只说 "JSD performs best on translation tasks" 没解释为什么。Round 55 指出应加 insight。

**改动**: 
- 解释 translation 有 moderate output diversity（不是 unique answer 也不是 fully open-ended）
- JSD 的 symmetric nature 刚好 balance mode-covering/seeking，适合这个 intermediate regime
- 额外 insight: sampling policy (on vs off) 的选择比 divergence 选择更重要，当 task geometry 不极端时

### 3. MiniLLM per-step credit assignment insight (line 712)

**问题**: 原文只说 "places optimization in the RL framework"，没解释 WHY single-step decomposition 对推理任务特别重要。

**改动**: 
- 加一句: single-step decomposition 不是 implementation convenience 而是 credit assignment — 能定位哪个 reasoning step 导致偏离
- 连接到 reasoning 任务的核心难题: 需要知道哪一步错了

### 4. f-divergence expectation under p_θ — tractability insight (line 183)

**问题**: 原文说 "amenable to on-policy optimization via policy gradient methods" 但没解释为什么 expectation under p_θ 这个性质重要。

**改动**: 
- 解释: 因为 sampling distribution 就是被优化的 policy，所以梯度直接通过 reparameterized samples 流动，不需要 importance weights
- 这避免了 off-policy corrections 带来的额外 variance

## 编译验证

✅ pdflatex clean build: 59 pages, 0 errors, 0 undefined controls

## Issues 1 & 2 from round 55/56 (DistiLLM + TT-OPD)

这两个在之前某轮已经修好了（DistiLLM 现在正确描述了 adaptive off-policy strategy，TT-OPD 现在写 "at a single teacher-reset event"）。本轮确认状态 OK，不重复修改。
