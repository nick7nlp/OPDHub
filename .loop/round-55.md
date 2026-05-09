# Round 55 — READ — §2 Background (lines 109-201)

## 精读发现

### 🔴 事实性问题

1. **DistiLLM "fully on-policy" 描述不准确 (line 191)**
   - Survey 说: "DistiLLM maintains π_mix = p_θ (fully on-policy)"
   - 实际: DistiLLM 的第二个核心贡献就是 "adaptive off-policy approach" — 用 SGO scheduler 动态决定何时用 student-generated outputs vs 固定 dataset。不是 fully on-policy。
   - 修复建议: 改为 "DistiLLM uses an adaptive scheduler that modulates the fraction of student-generated outputs" 或至少说 "the loss is defined over student-generated tokens" 而非 claim fully on-policy。
   - 严重度: ⚠️ 中等 — 会误导读者对 DistiLLM 的理解

2. **TT-OPD KL collapse 描述时间尺度不精确 (line 162)**
   - Survey 说: "KL divergence dropping from 2.637 to 0.343 over training"
   - 实际: 是在 single copy event (step 10, T=30 periodic reset) 的瞬间跌落，不是 "over training"
   - §7 (line 1042) 正确写了 "drops abruptly from its accumulated value to near zero, e.g., 2.637→0.343 at a single copy event"
   - 修复建议: 改为 "drops abruptly from 2.637 to 0.343 at a single teacher-reset event"
   - 严重度: ⚠️ 轻微但与后文不一致

### 🟡 论证薄弱处

3. **(0.95)^10 例子与 DAgger bound 的逻辑衔接 (line 159-161)**
   - 前文讲 DAgger O(εT²) quadratic bound，紧接着用 (0.95)^10 做数值例子
   - 但 (0.95)^10 是 independent error compounding（指数衰减），不是 DAgger bound 的体现
   - DAgger bound 说的是 distributional shift 导致 T² 错误数，比 independent compounding 更糟
   - 这个例子实际上 understates 了 DAgger bound 的严重性
   - 修复建议: 明确说"即使在最简单的 independent-error 假设下已经如此，而 DAgger bound 表明 distributional shift 使实际情况更糟"

4. **§2.4 Distillation Scaling Laws 最后一段过于推测 (line 198-201)**
   - "A natural extension might take the form Quality ∝ N_T^α · N_S^β · D^γ · R^δ" — 这是纯推测公式，无引用支持
   - 老大明确要求 §9 Future Directions 不放 self-invented formulas，但这里也有类似问题
   - 修复建议: 加 hedge ("one could hypothesize") 或 directly state "no such law has been proposed" without inventing a candidate formula

### 🟢 可深化处

5. **GKD JSD best on translation 但缺少 WHY (line 188)**
   - Survey 说 "JSD performs best on translation tasks, and all three divergences yield competitive results on summarization and instruction-following"
   - 但没解释 WHY JSD 在翻译上好 — 因为翻译有 moderate output diversity（不是 unique answer 也不是完全 open-ended），symmetric JSD 刚好 balance mode-seeking/covering
   - 建议 DEEPEN tick 时加 1-2 句 insight

6. **MiniLLM paragraph 缺少 variance reduction 讨论 (line 189-190)**
   - MiniLLM 的核心贡献之一是 single-step decomposition 来 reduce REINFORCE variance
   - Survey 只说 "reformulates optimization via REINFORCE" 但没提为什么 naive REINFORCE 有问题以及 MiniLLM 怎么解决
   - 建议 DEEPEN 时加一句 variance reduction insight

7. **f-divergence 定义中 Q in expectation 而非 P (line 171-172)**
   - Survey correctly writes D_f(P ∥ Q) = E_{y~Q}[f(P(y)/Q(y))]
   - 但后面说 "All these divergences are computable as expectations under the student's own policy (since D_f(P_T ∥ P_θ) = E_{y~p_θ}[f(p_T(y)/p_θ(y))])"
   - 这只对 P=teacher, Q=student 的 ordering 成立（即 Forward KL direction: KL(P_T ∥ P_θ)）
   - 对 Reverse KL (KL(P_θ ∥ P_T))，expectation is under P_θ too，but the f-divergence formula gives E_{y~P_T}[f(P_θ/P_T)]
   - 需要更仔细: D_f(P_T ∥ P_θ) with f(u)=u log u gives Forward KL = E_{P_θ}[(P_T/P_θ)log(P_T/P_θ)] ✅
   - D_f(P_T ∥ P_θ) with f(u)=-log u gives... wait let me verify this
   - Actually: Reverse KL = KL(P_θ ∥ P_T) = D_f(P_θ ∥ P_T) with f(u)=u log u, which = E_{P_T}[(P_θ/P_T)log(P_θ/P_T)]... that's under P_T, not P_θ!
   - 或者: Reverse KL as D_f(P_T ∥ P_θ) with f(u) = -log u gives E_{P_θ}[-log(P_T/P_θ)] = E_{P_θ}[log(P_θ/P_T)] = KL(P_θ ∥ P_T). ✅ 这样 expectation 确实在 P_θ 下
   - OK so both directions CAN be written as f-divergences with expectation under P_θ (the second argument). 
   - Forward KL: D_f(P_T ∥ P_θ) with f(u)=u log u → E_{P_θ}[(P_T/P_θ)log(P_T/P_θ)] ✅ under P_θ
   - Reverse KL: D_f(P_T ∥ P_θ) with f(u)=-log u → E_{P_θ}[-log(P_T/P_θ)] = E_{P_θ}[log(P_θ/P_T)] = KL(P_θ ∥ P_T) ✅ under P_θ
   - The survey's claim is CORRECT. Both choices of f give expectations under P_θ (=Q=second argument). No issue here.

### 🟡 格式/风格问题

8. **Line 113 "on-policy" 带引号不一致**
   - 第一次定义用 ``on-policy'' (TeX double quotes) ✅ 正确
   - 但 elsewhere 用 \emph{on-policy} — 这是 OK 的，first use quotes，subsequent italic

9. **No semicolons found ✅**
   - grep 确认 §2 无分号

10. **No prose colons in wrong places**
    - 检查了全部冒号使用，都在 structural/definitional 位置（"Formally:", "Here,", textbf labels）✅

### 总结

§2 整体质量较高，数学正确，叙事有层次。主要问题是：
1. DistiLLM 描述不准确（中等严重）— 需要 DEEPEN 修复
2. TT-OPD 时间尺度描述与 §7 不一致（轻微）— 需要 POLISH 修复
3. (0.95)^10 例子逻辑衔接可改进 — 需要 DEEPEN 加一句
4. §2.4 speculative formula 需 hedge — 需要 POLISH 修复

下一轮 VERIFY 应聚焦: DistiLLM adaptive off-policy claim 的准确描述
