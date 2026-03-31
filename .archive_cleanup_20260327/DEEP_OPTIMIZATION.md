# Deep Content Optimization — On-Policy Distillation Survey

## 目标
把这篇 27 页综述从"能看"提升到"高质量"。不是砍内容，是加深度。

## 当前问题诊断

### 1. 方法描述缺乏深度对比
当前每个方法都是独立描述的"四段式"（Key Idea / Objective / Comparison / Strengths-Limitations），但方法之间缺乏真正的横向对比和洞察。
**需要做的**：
- 在 Section 4.1 末尾加一段深入的横向分析：Token-level 方法之间的核心差异是什么？为什么 GKD 选 JSD 而 DistiLLM 选 Skew KL？在什么任务上哪个更好？
- 在 Section 4 末尾的 Theoretical Analysis 要更有 insight，不只是复述 Forward/Reverse KL 的性质

### 2. 实验结果几乎没有
整篇论文引用了 44 篇 paper 但几乎没有对比它们的实验结果。
**需要做的**：
- 在 Table 1 后面加一个 Table 2：Performance Comparison，列出主要方法在 GSM8K/MATH/HumanEval/MT-Bench 等 benchmark 上的结果
- 至少覆盖 GKD, MiniLLM, DistiLLM, SPIN, DeepSeek-R1 distillation 的数字
- 标注 teacher/student 模型大小

### 3. Section 6 (Reasoning Distillation) 缺少对 DeepSeek-R1 distillation 结果的具体分析
DeepSeek-R1 是本文的核心 motivating example，但 Section 6.3 只讲了为什么小模型不能直接 RL，没有分析 DeepSeek-R1 的具体 distillation 配方和结果（比如 R1-Distill-7B 在 AIME 上 73.3%、MATH-500 上 94.3%）。
**需要做的**：
- 补充 DeepSeek-R1 的具体 distillation 数据
- 分析不同 student size (1.5B, 7B, 8B, 14B, 32B, 70B) 的 scaling 行为
- 讨论 Qwen3 等后续工作是如何继承和改进这个 pipeline 的

### 4. Section 7 (Systems) 的 Compute-Quality Tradeoff 过于理论
当前的 FLOP 公式是正确的，但缺少实际的数字和案例。
**需要做的**：
- 用实际例子：比如用 70B teacher 蒸馏 7B student，on-policy vs off-policy 的 GPU hours 差异
- 引用具体论文中报告的训练成本

### 5. Section 8 (Future) 有些方向过于形式化
一些 future direction 写了漂亮的公式但缺乏实质内容（比如 8.3 Dynamic Curriculum, 8.8 Practical Guidelines）。
**需要做的**：
- 8.1 Distillation Scaling Laws: 补充 DeepSeek/Qwen 等实际的 scaling 观察
- 8.5 Agent-Level OPD: 结合 2025-2026 年 agent 的发展，写出更具体的挑战
- 8.8 Practical Guidelines: 要么删掉（不够深），要么大幅扩充为真正有用的 decision framework

### 6. 写作风格可以更犀利
不需要删内容，但一些地方可以更 sharp：
- "The most triumphant leap" → "A significant advance"
- "fundamentally radical transformation" → 直接说转变了什么
- 适度减少过度修饰但不要改变信息密度

## 关键指令
1. **不要删减内容**，只增加深度
2. **不要改动任何 \cite{} key**
3. **可以增加新的 subsection 或 paragraph**
4. **references.bib 不要动**（引用已经修好了）
5. 编译命令：pdflatex + bibtex + pdflatex × 2
6. 目标页数：27-32 页都可以（质量为王）

