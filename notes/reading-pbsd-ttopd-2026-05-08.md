# PBSD + TT-OPD 精读笔记（2026-05-08）

## PBSD (2605.05040) — Preference-Based Self-Distillation

### 作者
Xin Yu (Penn State + TikTok intern), Liuchen Liao, Yiwen Zhang, Yingchen Yu, Lingzhou Xue (PSU), Qinzhen Guo (TikTok/ByteDance, corresponding)

### 核心贡献
1. **Reward-regularized objective**（Eq. 3）：
   - max_π E[r(x,y)] - β * D_KL(π || π_teach)
   - 关键：这里 KL 是对 **teacher**（不是 base 模型，和 RLHF 不同）
2. **解析最优**（Prop 1, Eq. 4）：
   - π*(y|x) ∝ π_teach(y|x) * exp(r(x,y)/β)
   - **reward-tilted teacher distribution** — teacher 提供支撑（support）+ inductive bias，reward 重新分配概率质量
3. **Prop 2**：π* 在 reward-regularized objective 下**严格优于** teacher 本身（当 r 非常数时）
4. **实现**（DPO 风格，Eq. 10）：
   - y+ ~ π_teach (better-conditioned teacher 采样)
   - y- ~ π_θ (student on-policy 采样)
   - preference margin: m_θ = β * [log(π_θ(y+)/π_teach(y+)) - log(π_θ(y-)/π_teach(y-))]
   - 最大化 log σ(m_θ) — 经典 DPO logistic 形式，但作为 self-distillation 机制

### 关键设定
- **Teacher = 同一 base 模型 + privileged context c**（不是外部大模型）
- c 可以是：expert demonstrations, reference reasoning, tool/API info, retrieved evidence
- **on-policy**：y- 从当前 student 采样（不是 fixed dataset）
- **provably superior**：理论保证 target policy > teacher policy（reward 非平凡时）

### 动机
- KL matching 的问题：
  - 训练不稳定，会退化 reasoning performance
  - 压制 epistemic verbalization（模型表达不确定性、自我检查、纠错的能力）
  - teacher 是同一个模型只换 prompt，**缺少 exploratory diversity**
- 作者视角：teacher 定义 support + inductive bias，**不应该被无差别复制**

### 实验
- 数学推理 + tool-use benchmark
- 多个 model scale
- 结果：PBSD 在可比 baseline 中平均性能最强，**训练稳定性更好**

### 引用我们综述
✓ Song and Zheng (2026) — bib.bib18
- Introduction 引用：OPD 作为 post-training 重要范式

### 综述分类决策
**最佳归属：§5 Self-Distillation（self-distillation 的 beyond-KL 新范式）**

候选 subsection：
- **§5.1 Privileged Information**：是 context-augmented teacher（c），属于 PI 框架
- **§5.5 Reward-Free Alignment**：使用 preference learning (DPO 风格)，无外部 reward model

判断：
- PBSD 的核心创新不是 PI 本身（PI 只是 teacher 的构造方式），而是**对 PI-based self-distillation 用 preference learning 代替 KL matching**
- 与 §5.5 的关联更深：DPO 风格 + pairwise preference + no reward model
- 但它又依赖 PI 作为 teacher

**折中方案**：放在 **§5.5 Reward-Free Alignment**（preference learning 驱动的 self-distillation），因为 PBSD 的 "preference-based" 是核心标识，PI 是手段不是目的。同时在 §5.1 提一句作为 PI-based + preference 的代表。

### 在综述中的叙事位置
和以下论文形成递进：
- SPIN (self-play, 纯 KL) → IRIS (tuned R-KL) → π-Play (internal PI) → **PBSD (preference-learning 替代 KL)**
- 代表 **"beyond KL matching"** 的理论突破：不是调整 KL 变体，而是从根本上换目标函数

---

## TT-OPD (2605.02943) — Turn-level Truncated OPD

### 作者
Minbyul Jeong (first author), corresponding email hints Korean team (可能是 KAIST/Korean institution)

### 核心贡献
1. **Healthcare AI GYM 环境**（主要贡献之一）：
   - Gymnasium-compatible，10 个临床领域，3.6K+ tasks, 135 tools, 828K passages
   - 5D reward: accuracy / procedure / safety / format / coherence
2. **TT-OPD 方法**：
   - **EMA teacher**：gradient-free，不显式更新
   - **Outcome-privileged hints**：teacher 的 context 里注入 correctness signals（ground-truth answer），student 看不到
   - **Turn-level KL regularization**：每一轮对话都加 KL（不是只在终止时）
   - Length-controlled reward shaping

### 诊断的失败模式
三个 agentic RL 特有的 pathology：
1. **Response Explosion**：长度单调爆炸到上限（token coverage 当作任务完成代理）
2. **Multi-turn Collapse**：多轮 agent → verbose single-turn monologue（单轮 verbose 是 lower-energy path）
3. **Distillation Instability**：标准 OPD 在 agentic 场景失效（trajectory space 组合爆炸，teacher 快速 stale）

这三个问题的共同根因：**sparse terminal reward 与 sequential trajectory 结构性错配**。

### 关键设定
- **Self-distillation**：EMA teacher = student 的 moving average
- **Outcome-privileged**：teacher context 包含 correctness hint（答案），student 不包含
- **Turn-level dense KL**：每轮都加，不是只在 episode end
- 基于 GRPO framework + verl pipeline

### 实验
- 18 benchmarks: MC QA / visual QA / EHR / long-form
- TT-OPD 在 10/18 benchmark 达 SOTA，平均 +3.9pp vs non-RL baseline
- MedQA 87.1% (+16.4pp), MedMCQA 66.2%, MIMIC-III 62.7%
- Sustained tool use: 7.0-7.4 turns, controlled length 5.7-9.3K tokens
- 四个 ablation variant 追踪失败进展（KL collapse → response explosion）

### 关键发现
- **Agentic-textual transfer gap**：agentic RL 改进 procedural competence，但**不迁移**到 text-based QA（format-reward dilution）

### 引用我们综述
✓ Song and Zheng (2026) — bib.bib25
- Related Work 明确引用：提到我们的综述将 agent-level OPD 识别为 open problem
- 这个引用特别重要，因为 TT-OPD 正是回应了我们综述里提出的 open problem！

### 综述分类决策
**最佳归属：§8.3 Agentic OPD（多轮 agent 蒸馏）**

原因：
- TT-OPD 本身是 agentic 场景的 OPD 方法（多轮 tool-use trajectory）
- 直接回应我们综述提出的 agent-level OPD open problem
- EMA teacher + outcome-privileged PI + turn-level KL 的组合点就是 agentic

次要位置：
- **§5.1 Privileged Information**（outcome-privileged hints 是 PI 的 agentic 变体）
- **§6.2 Training Dynamics**（EMA teacher = dynamics，和 CaOPD、PRISM 等 dynamics 工作对比）

**推荐**：主位置 §8.3 Agentic（深度分析失败模式+方法设计），§5.1 table 中 briefly 引用（作为 outcome-privileged PI 的 agentic 代表）。

### 在综述中的叙事位置
- §8.3 Agentic 章节已有 TCOD、MAD-OPD、GUI-SD 等 agentic 方法
- TT-OPD 是第一个系统诊断 agentic OPD 失败模式（3 pathology + 根因分析）的工作
- 可以作为 §8.3 的 theoretical anchor，连接 §6.2 Dynamics 和 §5.1 PI

---

## 两篇论文的共同特征
- 都引用了我们综述 ✓（3 篇之外又新增 2 篇！）
- 都是 self-distillation 方向
- 都 "beyond naive KL matching"：
  - PBSD: preference learning 代替 KL
  - TT-OPD: outcome-privileged + turn-level dense KL + EMA
- 时间点：PBSD 5/6, TT-OPD 5/1 (按 arXiv 提交日期)

## 引用我们综述的论文已增加到 5 篇
| Paper | arXiv | 引用位置 |
|-------|-------|---------|
| Uni-OPD | 2605.03677 | Intro + Related Work |
| MAD-OPD | 2605.01347 | 参考文献 [33] |
| GUI-SD | 2605.00642 | Related Work × 2 |
| **PBSD** | **2605.05040** | **Intro (OPD post-training paradigm)** |
| **TT-OPD** | **2605.02943** | **Related Work (agent-level OPD as open problem)** |

5/11 篇新论文引用综述（45% 引用率，老大要的"影响力"指标有了）。
