# OPD New Papers Tracking

**Last Updated**: 2026-05-16 14:05 UTC
**Purpose**: 追踪未进综述的新 OPD 论文,scout 每天自动追加

## 收录范围规则 (2026-05-15 确认)

**收录**: 输出是**文本/语言**的模型的 on-policy distillation
- ✅ 自回归 LLM (GPT/Llama/Qwen 等)
- ✅ VLM / AudioLLM / 多模态 LLM (backbone 是 LLM)
- ✅ VLA / Robot+LLM (底层有 LLM backbone)
- ✅ Diffusion Language Model (输出是文本, 如 MDLM/TABOM)
- ✅ Protein Language Model (domain-specific LLM)
- ✅ GUI Agent (LLM-based)

**不收录**: 输出是**图片/视频**的模型
- ❌ T2I Diffusion (Stable Diffusion, FLUX 等)
- ❌ T2I Flow Matching (SD 3.5 等)
- ❌ Video Diffusion / Video Generation
- ❌ 任何纯图像/视频生成管线（即使用 T5/LLM 做 text encoder）

**判定原则**: 看模型最终输出的模态, 不看内部组件。

## 当前待集成 (3 篇)

| # | arXiv ID | Published | Title | Type | §Section | 发现日期 |
|---|----------|-----------|-------|------|----------|----------|
| 1 | 2605.11019 | 5/10 | Efficient LLM Reasoning via Variational Posterior Guidance with Efficiency Awareness | 🚧 第一类(Self-Distill) | §5.3.1+§6 | 5/16 |
| 2 | 2604.20244 | 4/22 | Hybrid Policy Distillation for LLMs | 🚧 第一类(Hybrid) | §4.1+Hybrid | 5/16 |
| 3 | 2604.18963 | 4/21 | Distillation Traps and Guards: A Calibration Knob for LLM Distillability | 📎 第二类(分析) | §7.2 | 5/16 |

**Notes:**
- 2605.11019: VPG-EA framework — parameter-shared posterior (conditioned on reference answer) distills to prior via variational KL. Self-distillation + efficiency optimization.
- 2604.20244: HPD (ICML 2026) — unified view of KD + hybrid forward/reverse KL + approximate on-policy sampling. Code: github.com/zwhong714/Hybrid-Policy-Distillation
- 2604.18963: Distillation traps (tail noise, off-policy instability, teacher-student gap) + calibration knob. Analysis paper directly relevant to OPD failure modes.

## 待确认 (1 篇)

| arXiv ID | Title | 问题 | 日期 |
|----------|-------|------|------|
| 2604.23336 | Efficient Rationale-based Retrieval: On-policy Distillation from Generative Rerankers based on JEPA | LLM backbone 做 on-policy distillation 但最终输出是 embedding/retrieval score, 不是文本生成。边界模糊。 | 5/16 |

## 已集成到 V3 (归档 - 5/12 至 5/16 batch, 共 10 篇)

| # | arXiv ID | Published | Title | §Section | 集成日期 |
|---|----------|-----------|-------|----------|----------|
| 1 | 2605.15113 | 5/14 | Learning from Language Feedback via Variational Policy Distillation | §5.3.3 | 5/16 |
| 2 | 2605.15155 | 5/14 | Self-Distilled Agentic Reinforcement Learning (SDAR) | §4.3+§8.2 | 5/15 |
| 3 | 2605.13643 | 5/13 | Prefix Teach, Suffix Fade: Local Teachability Collapse | §7.2 | 5/15 |
| 4 | 2605.13501 | 5/13 | RWOPD | §8.2+§4.3 | 5/15 |
| 5 | 2605.13255 | 5/13 | EGRSD | §6 | 5/15 |
| 6 | 2605.13230 | 5/13 | TGPO | §4.3 | 5/15 |
| 7 | 2605.12913 | 5/13 | Revisiting DAgger in the Era of LLM-Agents | §8.2 | 5/15 |
| 8 | 2605.12652 | 5/12 | MOPD | §6 | 5/15 |
| 9 | 2605.11853 | 5/12 | GEAR | §6 | 5/15 |
| 10 | 2605.12741 | 5/12 | RESD | §5.3.1+§6 | 5/15 |

## 已排除 (不在收录范围)

| arXiv ID | Title | 排除原因 | 日期 |
|----------|-------|---------|------|
| 2605.15055 | DiffusionOPD: A Unified Perspective of On-Policy Distillation in Diffusion Models | T2I Diffusion, 输出是图片 | 2026-05-15 |
| 2605.14897 | Critic-Driven Voronoi-Quantization for Distilling Deep RL Policies to Explainable Models | Deep RL 控制策略蒸馏, 非语言模型 | 2026-05-15 |
| 2605.14443 | Prompting Policies for Multi-step Reasoning and Tool-Use in Black-box LLMs with Iterative Distillation of Experience | 不是蒸馏 LLM, 而是优化 prompt selector; LLM 本身 frozen | 2026-05-15 |
| 2605.14071 | Distribution Corrected Offline Data Distillation for Large Language Models | 明确 offline, 无 on-policy sampling ("without online rollouts") | 2026-05-15 |
| 2605.13724 | AnyFlow: Any-Step Video Diffusion Model | 视频扩散模型, 输出是视频 | 2026-05-15 |
| 2605.08063 | Flow-OPD: On-Policy Distillation for Flow Matching Models | T2I Flow Matching (SD 3.5), 输出是图片 | 2026-05-15 |
| 2605.05204 | D-OPSD: On-Policy Self-Distillation for Step-Distilled Diffusion Models | T2I Diffusion, 输出是图片 | 2026-05-15 |
| 2605.15190 | RAVEN: Real-time Autoregressive Video Extrapolation with Consistency-model GRPO | Video diffusion, 输出是视频 | 2026-05-16 |
| 2605.15108 | Logging Policy Design for Off-Policy Evaluation | OPE for recommender, 非语言模型蒸馏 | 2026-05-16 |
| 2605.15012 | Boosting Reinforcement Learning with Verifiable Rewards via Randomly Selected Few-Shot Guidance | 纯 RL (RLVR+SFT), 无 distillation | 2026-05-16 |
| 2605.14450 | Stop Overthinking: Unlocking Efficient Listwise Reranking with Minimal Reasoning | IR reranking, 无蒸馏 | 2026-05-16 |
| 2605.12034 | Boosting Omni-Modal Language Models: Staged Post-Training with Visually Debiased Evaluation | Evaluation methodology, 无 OPD | 2026-05-16 |
| 2605.11706 | GRAFT: Graph-Tokenized LLMs for Tool Planning | Tool planning, 无蒸馏 | 2026-05-16 |

## 已集成到 V3 (归档 - 5/9 至 5/12 batch, 共 17 篇)

> 以下论文已在 V3 references.bib 中,不再需要操作。

| arXiv ID | Title | §Section |
|----------|-------|----------|
| 2605.08737 | The Extrapolation Cliff in OPD of Near-Deterministic Structured Outputs | §7.2+§8.2 |
| 2605.08741 | Training with Harnesses: On-Policy Harness Self-Distillation ⭐引用我们 | §5.3.1+§8.2 |
| 2605.08776 | Reasoning Compression with Mixed-Policy Distillation | §5.1 |
| 2605.08873 | CoDistill-GRPO | §4.3 |
| 2605.09253 | Rock Tokens in On-Policy Distillation | §7.2 |
| 2605.09548 | Crosslingual On-Policy Self-Distillation | §5.3.1+§8.2 |
| 2605.09725 | OPD with Best-of-N Teacher Rollout Selection | §5.1 |
| 2605.10889 | Unmasking OPD: Where It Helps, Where It Hurts (Apple) | §7.1+§7.2 |
| 2605.11182 | The Many Faces of OPD: Pitfalls, Mechanisms, Fixes (UIUC) | §7.2 |
| 2605.11458 | Adaptive Teacher Exposure for Self-Distillation (ByteDance) | §5.3.1 |
| 2605.11609 | Anti-Self-Distillation via PMI | §4.1+§5.3.1 |
| 2605.11613 | From Generic Correlation to Input-Specific Credit in OPSD | §4.2+§5.3.1 |
| 2605.11739 | Learning to Foresee: Unlocking Efficiency of OPD ⭐引用我们 | §6+§7.1 |
| 2605.11854 | Self-Distilled Trajectory-Aware Boltzmann Modeling (TABOM) | §5.3.2+§8.2 |
| 2605.12227 | Combining On-Policy Optimization and Distillation for Long-Context | §4.3 |
| 2605.12400 | OGLS-SD: Outcome-Guided Logit Steering | §4.2+§5.3.1 |
| 2605.12483 | Beyond GRPO and OPD: Sparse-to-Dense Reward ⭐引用我们 | §4.3 |

## 资料位置
- **PDF**: `/apdcephfs_cq8/share_1324356/nickmysong/openclaw_fsp/papers/opd/{id}.pdf`
- **BibTeX**: `/apdcephfs_cq8/share_1324356/nickmysong/openclaw_fsp/papers/opd/new_opd_2605_bibtex.bib`
- **GitHub**: 已在 taxonomy sections 标 🟡

## 引用我们综述 (2604.00626) 的论文 - 17 篇确认（截至 2026-05-15）

| # | arXiv ID | Title | Date | Status |
|---|----------|-------|------|--------|
| 1 | 2604.25110 | Knowledge Distillation Must Account for What It Loses | 4月 | 已在 V2 |
| 2 | 2605.00642 | Learn where to Click from Yourself: On-Policy Self-Distillation for GUI Grounding | 5/1 | 已在 V2 |
| 3 | 2605.01347 | MAD-OPD: Breaking the Ceiling in On-Policy Distillation via Multi-Agent Debate | 5/2 | 已在 V2 |
| 4 | 2605.02943 | Healthcare AI GYM for Medical Agents | 5/5 | 已在 V2 |
| 5 | 2605.03677 | Uni-OPD: Unifying On-Policy Distillation with a Dual-Perspective Recipe | 5/5 | 已在 V2 |
| 6 | 2605.05040 | Preference-Based Self-Distillation: Beyond KL Matching via Reward Regularization | 5/7 | 已在 V2 |
| 7 | 2605.06230 | Safactory: A Scalable Agentic Infrastructure for Training Trustworthy Autonomous Intelligence | 5/7 | 待集成 |
| 8 | 2605.06597 | UniSD: Towards a Unified Self-Distillation Framework | 5/7 | 已在 V2 |
| 9 | 2605.07396 | Rubric-based On-policy Distillation | 5/8 | 已在 V2 |
| 10 | 2605.07711 | SimCT: Recovering Lost Supervision for Cross-Tokenizer On-Policy Distillation | 5/8 | 已在 V2 |
| 11 | 2605.07725 | SOD: Step-wise On-policy Distillation for Small Language Models | 5/8 | 已在 V2 |
| 12 | 2605.08737 | The Extrapolation Cliff in On-Policy Distillation of Near-Deterministic Structured Outputs | 5/9 | 待集成 |
| 13 | 2605.08741 | Training with Harnesses: On-Policy Harness Self-Distillation for Complex Reasoning | 5/9 | 待集成 |
| 14 | 2605.11739 | Learning to Foresee: Unveiling the Unlocking Efficiency of On-Policy Distillation | 5/12 | 待集成 |
| 15 | 2605.12483 | Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle | 5/12 | 待集成 |
| 16 | 2605.12652 | Multi-Rollout On-Policy Distillation via Peer Successes and Failures | 5/12 | 待集成 |
| 17 | 2605.13255 | Respecting Self-Uncertainty in On-Policy Self-Distillation for Efficient LLM Reasoning | 5/13 | 待集成 |
| 18 | 2605.13643 | Prefix Teach, Suffix Fade: Local Teachability Collapse in Strong-to-Weak On-Policy Distillation | 5/13 | 待集成 |

**引用增速**: 45 天 18 篇 ≈ 每 2.5 天一篇，5/9 后加速（OPD 方向爆发）

## OPD 论文增长趋势
| 月份 | 论文数 (bib) | 说明 |
|------|-------------|------|
| 2601 (Jan 2025) | 8 | |
| 2602 (Feb) | 14 | |
| 2603 (Mar) | 13 | |
| 2604 (Apr) | 22 | 我们综述发布 (4/1) |
| 2605 (May) | 20 in V2 + **19 new** = 39 | 🔥 爆发!|

**5 月 OPD 论文日均 ~5 篇**--这个方向在加速增长。我们综述发布后(4/1),引用效应带动了更多人做 OPD。

## Scout 维护规则
- 每天 02:40 CST 自动扫描,06:40 CST 补跑
- 新发现的论文追加到本文件("当前待集成" 表)
- V3 集成后:从本文件移除,移到 "已集成" 归档区
- 收录范围:**不限于 autoregressive text LLM**(Diffusion/VLM/Flow Matching/Multimodal 全收)

---

## 【2026-05-13 13:26 老大决策】Self-Generated Data SFT 谱系

### 核心洞察
SPIN / OPSFT / SSD / TABOM 本质是**同一谱系**:self-generated data + SFT,差别在 **rollout-update staleness**。

| 方法 | Rollout 时机 | Staleness |
|------|------------|----------|
| OPSFT (2602.13407) | 每 training step | 严格 on-policy |
| SPIN (2401.01335) | 每 outer iteration | 中度 stale(batch on-policy) |
| SSD (2604.01193) | 训练前一次 | 最 stale(off-policy SFT) |
| TABOM (2605.11854) | 训练前一次(DLM 版本) | 最 stale(off-policy SFT) |

### V3 整改(下次改)
1. §5.3.2 "Minimalist self-distillation" 部分重写为**统一谱系叙事**,明确 rollout-update staleness 光谱
2. **TABOM 加回** GitHub awesome list §5.3.2(之前按纯二元 on-policy 判断删除是不一致的,既然 SSD 留了 TABOM 也该留)
3. Diffusion LM 的 self-distillation 和 autoregressive LM 的 self-distillation **同等对待**

### 判定规则(未来遇到类似论文)
**属于 §5.3.2 的条件**:
- 信号源:model 自己(no teacher / no verifier / no PI)
- 训练方式:在 self-generated data 上做 SFT(cross-entropy / SFT / KL)
- Rollout 频率**不限**(从 pre-training 一次到 per-step 都行)
- 明确区分其 staleness 位置

**不属于 §5.3.2 的**:
- Teacher 拿 PI(reference solution / GT / tools)→ §5.3.1
- Verifier / RLVR / external reward → §5.3.3
- 真正的 external teacher model(不是 self)→ §5.1/§5.2

---

## 【2026-05-13 13:32 老大发现】§5.3.2 / §5.3.3 边界错位

### 问题
§5.3.2 当前有 3 篇用了外部反馈,违反"无外部反馈"的子节定义:

| 论文 | 现在位置 | 实际依赖 | 应该去哪 |
|------|---------|---------|---------|
| RLSD (yang2026selfdistilled) | §5.3.2 + §5.3.3 重复 | 明确用 RLVR environmental feedback | 主归属 §5.3.3 |
| RLRT (kim2026rlrt) | §5.3.2 | GRPO + reward 才能定义 successful rollouts | §5.3.3 |
| OPSFT (zhao2026onpolicy) | §5.3.2 | "outcome verification" 用 GT answer filter | §5.3.1 (PI) 或 §5.3.3,看怎么 frame |

### V3 整改 todo
1. RLSD 主归属 §5.3.3,§5.3.2 末尾只用一句话提及"也有 RLVR-augmented variant"
2. RLRT 移到 §5.3.3(GRPO reward 是显式外部信号)
3. OPSFT 决策:
   - 选项 A:留 §5.3.2,弱化 verification 描述
   - 选项 B:移 §5.3.1(GT answer 当 PI)✅ 推荐
   - 选项 C:移 §5.3.3
4. **§5.3.2 子节标题 'Beyond adversarial games' 重新组织**:
   - 移除上述 3 篇后,剩 SDFT/MTP-SD,归"轻量级 self-as-teacher"
   - 加上"Self-Generated Data SFT 谱系"的统一叙事(含 SPIN/OPSFT/SSD/TABOM)

### 教训
论文 framing(作者怎么 frame 自己)和实际机制(用了什么信号源)是两件事。**分类要看实际机制**,不要被 framing 带跑:
- 论文叫 "self-distilled RLVR" → 不能因为有 "self-distilled" 就放 §5.3.2
- "Outcome verification" 用了 GT → 就是 PI/external,不是纯 self-play

---

## 【2026-05-13 13:45 核实更新】§5.3.2 更严重的错位(5 篇,不是 3 篇)

老大追问后严格对 PDF 核实,§5.3.2 当前 10 篇里实际错位 5 篇:

### 应移出 §5.3.2 的论文

| 论文 | 错位原因(从 PDF 引用) | 应归属 |
|------|----------------------|---------|
| RLSD (2604.03128) | "RLVR environmental feedback" | §5.3.3 |
| RLRT (2605.10781) | 名字就叫 "Rebellious Student: Reversing Teacher Signals for Reasoning Exploration with Self-Distilled RLVR",augments GRPO | §5.3.3 |
| π-Play (2604.14054) | "search tools and interacts with the search engine" + "GRPO using outcome rewards derived from answer correctness" | §5.3.3 |
| OPSFT (2602.13407) | CORRECT(o, a) 用 training set 自带 GT answer a | §5.3.1 (GT answer = PI) |
| SDFT (2601.19897) | "demonstration-conditioned model as its own teacher" - expert demonstrations 是训练时才有的 | §5.3.1 (demos = PI) |

### 真正属于 §5.3.2 的只有 5 篇
- SPIN (2401.01335) - 纯 iterative self-play
- IRIS (2604.20933) - SPIN 的 Rényi 统一框架
- SSD (2604.01193) - 明确 "No verifier, no teacher, no RL, no code execution"
- UniSD (2605.06597) - multi-checkpoint agreement,无外部
- MTP-SD (2602.06019) - frozen self-as-teacher

### V3 整改加强版
1. 把 RLSD / RLRT / π-Play 移到 §5.3.3
2. 把 OPSFT / SDFT 移到 §5.3.1
3. §5.3.2 只保留 5 篇 + TABOM(下次加回)
4. §5.3.2 统一叙事:"Self-Generated Data SFT 谱系":
   - 严格 on-policy: (暂时空,OPSFT 移走了)
   - Batch on-policy: SPIN, IRIS
   - 最 stale: SSD, TABOM
   - Architectural self-distillation: MTP-SD
   - Integrative framework: UniSD

### 这次学到什么
作者论文里说 "no reward" 或 "minimalist" 不等于真的没用外部信号:
- OPSFT 说 "reward-free",但 CORRECT(o, a) 就是用 GT 做 binary reward
- SDFT 说 "no explicit reward function",但用了 demonstrations 当 in-context teacher
- π-Play 说 "without external data",但用了 search engine + outcome reward

**分类要看实际用了什么 oracle 信号,不看作者 framing**。

---

## 【2026-05-13 13:50 老大】§5.3.2 边缘案例多 - 写作时要注意

### 老大原话
"感觉 self play 有很多处于边缘啊,感觉写的时候可以注意下"
"我们现在精读的时候,真的好好分类了么?"

### 写作 note (V3 整改时)
§5.3.2 章节本身就处于多个范式的交界处,多篇论文是**边缘案例**:
- SDFT: demonstration-conditioned 是不是 PI?(我判它是)
- OPSFT: GT-answer-filter 是不是 PI?(我判它是)
- π-Play: 内部 PI + outcome reward 杂交 (横跨 §5.3.1 + §5.3.3)
- RLSD/RLRT: 名字带 RLVR 但作者把它放在 self-distillation 框架下

写 §5.3.2 时**必须明确该章节的硬边界**:
- 不能因为论文用了 "self-distillation" 这个词就放进来
- 如果方法依赖 GT/verifier/reward → 不属于 §5.3.2
- §5.3.2 = "纯 self(无 PI 无 verifier 无外部 reward)" 是**严格的负面定义**
- 在章节开头明确说"以下论文以 self-as-teacher / temperature diversity / iterative checkpoint 为唯一 asymmetry 来源"

### 精读系统现状(老大问的)
**6 篇精读 ≠ 19 篇新论文都精读了**!
- paper_notes.json 只有 6 篇,全是历史经典论文(KD survey, scaling laws...)
- 5/9-5/12 的 19 篇新论文一篇都没经过精读流程
- 之前的分类是用 grep 关键词 + sub-agent 判断做的,没走精读

### 已修复(系统层)
1. **`paper_deep_read_dispatcher.py` 改 reverse sort**:每天优先读最新 PDF(之前是从 1503.* 开始读,新论文要等 90 天)
2. **prompt 大改**:加入 on_policy_mechanism + opd_classification 结构化字段,要求 evidence_quote
3. **cron count 5 → 10**:加快覆盖速度
4. **prompt 内置判定铁律**:明确 "self-distilled ≠ on-policy","no reward ≠ no PI" 等关键陷阱

### V3 整改的硬性 todo
1. 精读 19 篇新 OPD 论文(让 cron 跑几天先覆盖 5/9-5/12 batch)
2. 用精读输出的 primary_section 重新分类
3. §5.3.2 章节移走 5 篇错位论文(RLSD/RLRT/π-Play/OPSFT/SDFT)
4. §5.3.2 重写"硬边界" + 加 staleness 谱系叙事
5. TABOM 加回 §5.3.2(按 staleness 谱系)


---

## 【2026-05-13 13:58 老大尖锐问题】Self-Play 算不算 on-policy?

### 问题
"如果严格按照 on policy 的定义,self play 根本不算 on policy 吧?"

### 严格定义下的回答:**对,大部分不算**

**Strict on-policy**: 计算 gradient 时,sample 必须来自当前正在更新的 π_θ。两次 sample 之间 policy 不能动。

按这个定义:
- PPO/GRPO 都不是 strict on-policy(K-epoch rollout 重用 + importance ratio 修正)
- SPIN/IRIS(batch self-play):每 outer iter sample 一次,inner K epochs SFT → 越来越 off
- SSD/TABOM:sample 一次后做 N epochs SFT → 严重 off-policy
- 真正 strict 的只有 OPSFT 这种"每 step rollout 用完即丢"

### 社区宽松定义
"rollouts come from a recent snapshot of the policy" - staleness 容忍度问题。

### 综述定位的根本张力
§5.3 整个 self-distillation 章节,**严格说大部分论文不是 on-policy**。
- SPIN-family: outer-iter on-policy(K_inner=1 接近,K_inner>1 越来越 off)
- SSD/TABOM: 严重 off-policy SFT on self-generated data
- 真正 strict on-policy 的 self-distillation 只剩有 RL 信号的(π-Play, RLSD, RLRT)

### V3 整改方案
**Option A(保守)**: §5.3 保留,但章节开头明确写 staleness 谱系,承认这些方法处于 OPD 边界。
**Option B(激进,更诚实)**: §5.3 改名 **"Self-Generated Supervision"** 或 **"Teacher-Free Distillation"**,作为 OPD 邻接范式讨论,按 signal source 重新组织(PI / mutual / feedback),不强行套 on-policy 标签。

**倾向 Option B**:更经得起审稿,避免 "你 SPIN 哪算 on-policy" 的尴尬。综述定位调整为 "OPD 及其邻接范式"。

### Action items
1. 等老大决定 Option A vs B
2. V3 §5.3 章节开头**必须**有"on-policy spectrum" 段落,把 staleness 讲清楚
3. Abstract / Intro 不要 overclaim "all of self-distillation is on-policy"


---

## 【2026-05-13 Scout】+2 new, 8 rejected

### ✅ 新确认 (1 篇)

| # | arXiv ID | Published | Title | §Section | Key Contribution |
|---|----------|-----------|-------|----------|------------------|
| 20 | 2605.07177 | 5/8 | HyperEyes: Dual-Grained Efficiency-Aware Reinforcement Learning for Parallel Multimodal Search Agents | §8.2 | OPD micro-level: dense token-level teacher signals on failed student rollouts for multimodal agents (Xiaohongshu+Cambridge) |

### ❌ 排除 (8 篇)

| arXiv ID | Title | 排除原因 |
|----------|-------|---------|
| 2605.10875 | Compute Where it Counts: Self Optimizing Language Models | 推理效率动态分配,不是 KD (ICML'26) |
| 2605.09920 | Verifier-Free RL for LLMs via Intrinsic Gradient-Norm Reward | 纯 RL intrinsic reward,无 teacher/distillation (ACL'26 Findings) |
| 2605.08887 | Ace-Skill: Bootstrapping Multimodal Agents with Prioritized and Clustered Evolution | Self-evolving agents 经验蒸馏,非 OPD |
| 2605.07579 | Your Language Model is Its Own Critic: Reinforcement Learning with Value Estimation from Actor's Internal States | 纯 RL baseline estimation,无 distillation |
| 2605.04559 | Beyond Static Best-of-N: Bayesian List-wise Alignment for LLM-based Recommendation | IR/推荐领域 BoN alignment,非 LLM capability distillation (SIGIR'26) |
| 2605.10518 | Infinite Mask Diffusion for Few-Step Distillation | 标准 MDM 蒸馏加速,无 on-policy student sampling |
| 2605.07820 | Scaling Categorical Flow Maps | Flow matching self-distill 加速,标准 progressive distillation |
| 2605.07274 | Structured Role-Aware Policy Optimization for Multimodal Reasoning | 纯 GRPO + credit assignment,"self-distilled contrasts" 只是命名 |
| 2605.06850 | How to Compress KV Cache in RL Post-Training? Shadow Mask Distillation for Memory-Efficient Alignment | 纯 RL 效率优化（KV cache 压缩后的 off-policy bias 修复），不是 OPD。5/14 删除 |
| 2605.09536 | TAD: Temporal-Aware Trajectory Self-Distillation for Fast and Accurate Diffusion LLM | Off-policy: teacher conditioned on GT response 生成静态 trajectory，student 学预录轨迹，不是 on-policy sampling。5/14 删除 |
| 2605.11651 | Hide to See: Reasoning-prefix Masking for Visual-anchored Thinking in VLM Distillation | 标准 offline KD: teacher (Qwen3-VL-Thinking) 分布直接做监督，student 没有 on-policy rollouts。5/14 删除 |

### Self-Check

```
论文: HyperEyes (2605.07177)
类型: 第一类(OPD方法) - OPD 应用于 multimodal agents
判定级别: Level 2
判定: 收录
证据: Abstract 明确 "we adapt On-Policy Distillation (OPD) to inject dense token-level corrective signals from an external teacher on failed rollouts"
综述状态: 待加入下次综述 (§8.2)

论文: Shadow Mask Distillation (2605.06850)
类型: 不收录
判定级别: Level 2
判定: 不收录
证据: 纯 RL 训练效率优化。解决 KV cache 压缩引入的 off-policy bias,不是 teacher→student 的 OPD 方法。dense/sparse 是同一个模型的不同 attention mask。
综述状态: 不收录(5/14 纠正)
```

## 【2026-05-14 Scout】+4 new, 6 rejected

### ✅ 新确认 (4 篇)
| # | arXiv ID | Date | Title | §Section | Notes |
|---|----------|------|-------|----------|-------|
| 1 | 2605.10189 | 2026-05-11 | ProteinOPD: Towards Effective and Efficient Preference Alignment for Protein Design | §8.2 Emerging Domains | Multi-teacher OPD for protein PLMs; geometric consensus of weighted teachers; student generates protein sequences on-policy |
| 2 | 2605.10194 | 2026-05-11 | TRACE: Distilling Where It Matters via Token-Routed Self On-Policy Alignment | §6.1 + §5.3.1 | Token-routed self-OPD; FKL on key spans, RKL on error spans, GRPO on rest; solves all-token KL collapse in self-OPD |
| 3 | 2605.09329 | 2026-05-10 | Test-Time Speculation | §8.2 Emerging Domains | Online OPD at test-time for speculative decoding; draft(student) generates, target(teacher) provides distribution, draft updates during inference |
| 4 | 2605.06230 | 2026-05-07 | Safactory: A Scalable Agentic Infrastructure for Training Trustworthy Autonomous Intelligence | §8.1 Industrial Deployment | Shanghai AI Lab; unified evolutionary pipeline integrating RL + OPD for agent safety; dedicated §5.3 on on-policy distillation |

### ❌ 排除 (6 篇)
| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.11556 | Hindsight Hint Distillation: Scaffolded Reasoning for SWE Agents from CoT-free Answers | SFT on pre-collected scaffolded trajectories; no real-time teacher feedback in training loop |
| 2605.07327 | Teacher-Feature Drifting: One-Step Diffusion Distillation with Pretrained Diffusion Representations | Image diffusion distillation, not LM |
| 2605.08354 | Auto-Rubric as Reward: From Implicit Preferences to Explicit Multimodal Generative Criteria | RL alignment via rubric-based reward, not OPD |
| 2605.07503 | Diffusion-APO: Trajectory-Aware Direct Preference Alignment for Video Diffusion Transformers | Video diffusion DPO/GRPO, not on-policy distillation |
| 2605.09422 | Perception Without Engagement: Dissecting the Causal Discovery Deficit in LMMs | ⚠️ arXiv ID 错误，2605.09422 实际是无关论文 |
| 2605.07276 | Signal Reshaping for GRPO in Weak-Feedback Agentic Code Repair | Pure GRPO paper; OPD mentioned only as boundary comparison |

### Self-Check

```
论文: ProteinOPD (2605.10189)
类型: 第一类(OPD方法) - 新应用域(蛋白质设计)
判定级别: Level 2
判定: 收录
证据: "distills their knowledge into a shared student via token-level OPD on the student's own trajectories"; "adapts a pretrained PLM into preference-specific teachers"; multi-objective geometric consensus
综述状态: 待加入下次综述 (§8.2)

论文: TRACE (2605.10194)
类型: 第一类(OPD方法) - Token-routed self-OPD
判定级别: Level 2
判定: 收录
证据: "On-policy self-distillation (self-OPD) densifies RLVR by letting a policy teach itself under privileged context"; token-routed FKL/RKL on critical spans; student generates on-policy rollouts
综述状态: 待加入下次综述 (§6.1 + §5.3.1)

论文: Test-Time Speculation (2605.09329)
类型: 第一类(OPD方法) - Test-time online distillation
判定级别: Level 2
判定: 收录
证据: "treating the target as the teacher, the draft as the student, and the target's distribution over the draft tokens as the distillation sample on which the draft performs an optimization step"; satisfies all 3 OPD criteria (student on-policy generation, teacher feedback, distribution update in loop)
综述状态: 待加入下次综述 (§8.2)

论文: Safactory (2605.06230)
类型: 第二类(OPD系统/基础设施)
判定级别: Level 2
判定: 收录
证据: Paper has dedicated §5.3 "On-policy Distillation" section; "Autonomous Evolution Platform for asynchronous reinforcement learning and on-policy distillation"
综述状态: 待加入下次综述 (§8.1)

论文: Hindsight Hint Distillation (2605.11556)
类型: 不收录
判定级别: Level 2
判定: 不收录
证据: Training is SFT on successful hint-scaffolded trajectories collected beforehand. "The model then self-distills these scaffolded trajectories" = offline SFT, no teacher providing real-time feedback during training loop. More akin to iterative RFT with hint synthesis.

论文: Teacher-Feature Drifting (2605.07327)
类型: 不收录
判定级别: Level 1
判定: 不收录
证据: Pure image generation (ImageNet/SDXL), not language model. "One-Step Diffusion Distillation" for image synthesis.
```

## 【2026-05-14 Scout (Evening)】+8 new, 2 rejected

### ✅ 新确认 (8 篇)
| # | arXiv ID | Date | Title | §Section | Notes |
|---|----------|------|-------|----------|-------|
| 1 | 2605.13724 | 2026-05-13 | AnyFlow: Any-Step Video Diffusion Model with On-Policy Flow Map Distillation | §8.2 Emerging Domains | NVIDIA; flow-map backward simulation; on-policy distillation for video diffusion; 1.3B–14B |
| 2 | 2605.13643 | 2026-05-13 | Prefix Teach, Suffix Fade: Local Teachability Collapse in Strong-to-Weak On-Policy Distillation | §7.2 Failure Modes | Qwen3 family; BIC change-point release rule; dense OPD degrades when teacher margin vanishes in suffix |
| 3 | 2605.13501 | 2026-05-13 | Reward-Weighted On-Policy Distillation with an Open Property-Equivalence Verifier for NL-to-SVA Generation | §8.2 + §4.3 | Verifier-reward-weighted FKL; property-equivalence checker; new SOTA on NL2SVA |
| 4 | 2605.13255 | 2026-05-13 | Respecting Self-Uncertainty in On-Policy Self-Distillation for Efficient LLM Reasoning | §6 Training Efficiency | Entropy-guided confidence gate; causal-lookahead variant; Qwen3-4B/8B |
| 5 | 2605.13230 | 2026-05-13 | Teacher-Guided Policy Optimization for LLM Distillation | §4.3 RL-Augmented | Dense directional teacher guidance on RKL; fixes uninformative negative feedback; NLP2CT/NEU |
| 6 | 2605.12913 | 2026-05-13 | Revisiting DAgger in the Era of LLM-Agents | §8.2 Emerging Domains | Turn-level student-teacher interpolation for SWE agents; +3.9pp SWE-bench Verified at 4B |
| 7 | 2605.12652 | 2026-05-12 | Multi-Rollout On-Policy Distillation via Peer Successes and Failures | §6 Training Efficiency | Peer-conditioned teacher signals; success/failure rollout groups; CMU |
| 8 | 2605.11853 | 2026-05-12 | GEAR: Granularity-Adaptive Advantage Reweighting for LLM Agents via Self-Distillation | §6 Training Efficiency | On-policy student vs GT-conditioned teacher divergence; adaptive segment boundaries; +20% over GRPO |

### ❌ 排除 (2 篇)
| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.13665 | Robot Squid Game: Quadrupedal Locomotion for Traversing Narrow Tunnels | Robotics policy distillation (not LLM), quadruped RL |
| 2605.12798 | Emergent and Subliminal Misalignment Through the Lens of Data-Mediated Transfer | Safety/alignment study; uses OPD as experimental condition but not contributing to OPD methodology |

### Self-Check

```
论文: AnyFlow (2605.13724)
类型: 第一类(OPD方法) - Video diffusion on-policy distillation
判定级别: Level 2
判定: 收录
证据: "enabling efficient on-policy distillation that reduces test-time errors (i.e., discretization error in few-step sampling and exposure bias in causal generation)"; flow-map backward simulation decomposes rollout into transitions for on-policy training
综述状态: 待加入下次综述 (§8.2)

论文: Prefix Teach, Suffix Fade (2605.13643)
类型: 第二类(OPD分析) - Failure mode analysis
判定级别: Level 2
判定: 收录
证据: "We demonstrate that this assumption sometimes fails to hold in strong-to-weak OPD settings"; "local teachability collapse" — identifies when dense OPD supervision stops being effective; directly relevant to OPD practitioners
综述状态: 待加入下次综述 (§7.2)

论文: RWOPD (2605.13501)
类型: 第一类(OPD方法) - Verifier-reward-weighted OPD
判定级别: Level 2
判定: 收录
证据: "on-policy distillation method that samples student rollouts, scores them with an open SymbiYosys+Z3 Property-Equivalence Checker (PEC), and applies a verifier-reward-weighted forward-KL gradient from a frozen 14B teacher on verifier-passable rollouts"
综述状态: 待加入下次综述 (§8.2 + §4.3)

论文: EGRSD (2605.13255)
类型: 第一类(OPD方法) - Self-distillation with entropy gating
判定级别: Level 2
判定: 收录
证据: "On-policy self-distillation trains a reasoning model on its own rollouts while a teacher... provides dense token-level supervision"; proposes entropy-guided confidence gate that down-weights high-entropy positions
综述状态: 待加入下次综述 (§6)

论文: TGPO (2605.13230)
类型: 第一类(OPD方法) - RL-augmented OPD
判定级别: Level 2
判定: 收录
证据: "Teacher-Guided Policy Optimization (TGPO), an on-policy algorithm that incorporates dense directional guidance by leveraging teacher predictions conditioned on the student's rollout"; "remains on-policy, the algorithm integrates seamlessly with existing RLVR frameworks"
综述状态: 待加入下次综述 (§4.3)

论文: Revisiting DAgger (2605.12913)
类型: 第一类(OPD方法) - DAgger for LLM agents
判定级别: Level 2
判定: 收录
证据: "collects trajectories through a turn-level interpolation of student and teacher policies, and the student is then trained on these trajectories using supervised labels provided by the teacher"; "By directly interacting with environments, we expose the model to realistic states" — satisfies on-policy generation + teacher feedback
综述状态: 待加入下次综述 (§8.2)

论文: MOPD (2605.12652)
类型: 第一类(OPD方法) - Multi-rollout OPD
判定级别: Level 2
判定: 收录
证据: "Multi-Rollout On-Policy Distillation (MOPD), a peer-conditioned distillation framework that uses the student's local rollout group to construct more informative teacher signals"; "training on student-generated trajectories" with "peer successes and failures"
综述状态: 待加入下次综述 (§6)

论文: GEAR (2605.11853)
类型: 第一类(OPD方法) - Self-distillation credit assignment
判定级别: Level 2
判定: 收录
证据: "GEAR compares an on-policy student with a ground-truth-conditioned teacher to obtain a reference-guided divergence signal for identifying adaptive segment boundaries and modulating local advantage weights"; on-policy generation + privileged teacher supervision
综述状态: 待加入下次综述 (§6)
```

## 【2026-05-15 Scout】+1 new, 1 rejected

### ✅ 新确认 (1 篇)
| # | arXiv ID | Date | Title | §Section | Notes |
|---|----------|------|-------|----------|-------|
| 1 | 2605.12741 | 2026-05-12 | Learning with Rare Success but Rich Feedback via Reflection-Enhanced Self-Distillation | §5.3.1 + §6 | On-policy self-distillation with reflection from failures; teacher conditioned on retrospective reflections + persistent playbook; single-rollout outperforms GRPO 8× samples; Amazon/UCSD |

### ❌ 排除 (1 篇)
| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.13165 | STOP: Structured On-Policy Pruning of Long-Form Reasoning in Low-Data Regimes | On-policy generation + SFT on pruned self-data only; explicitly "cannot rely on large-scale teacher distillation"; no teacher providing token-level supervision in training loop; efficiency technique not OPD |

### Self-Check

```
论文: RESD (2605.12741)
类型: 第一类(OPD方法) - Self-OPD with reflection-enriched teacher
判定级别: Level 2
判定: 收录
证据: "on-policy self-distillation"; "self-teacher provides actionable token-level supervision"; "Reflection-Enhanced Self-Distillation (RESD) transforms raw failure feedback into active corrective supervision"; student generates rollouts, teacher conditioned on retrospective reflections provides dense token-level supervision
综述状态: 待加入下次综述 (§5.3.1 + §6)

论文: STOP (2605.13165)
类型: 不收录
判定级别: Level 2
判定: 不收录
证据: "cannot rely on large-scale teacher distillation or heavy test-time control"; "STOP constructs self-distilled traces from the model" then prunes and does SFT; no teacher supervision in the training loop. Explicitly contrasts with teacher-guided pruning. This is on-policy generation + SFT on curated data (§5.3.2 borderline but no teacher = not OPD).
```

<!-- 2026-05-15 标题全量校验修正，共 45 处 -->

## 【2026-05-16 Scout】+1 new, 3 rejected

### ✅ 新确认 (1 篇)
| # | arXiv ID | Date | Title | §Section | Notes |
|---|----------|------|-------|----------|-------|
| 1 | 2605.15155 | 2026-05-14 | Self-Distilled Agentic Reinforcement Learning | §4.3 + §8.2 | SDAR: OPSD as gated auxiliary to RL for multi-turn agents; sigmoid gate on teacher-endorsed tokens; handles negative teacher rejections; Qwen2.5/Qwen3 on ALFWorld/WebShop/Search-QA; Meituan/ZJU |

### ❌ 排除 (3 篇)
| arXiv ID | Title | Reason |
|----------|-------|--------|
| 2605.15141 | Causal Forcing++: Scalable Few-Step Autoregressive Diffusion Distillation for Real-Time Interactive Video Generation | Video diffusion distillation (output modality = video, not text); outside scope |
| 2605.14417 | Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control | Humanoid robot control; not LLM distillation |
| 2605.09317 | Mem-W: Latent Memory-Native GUI Agents | GUI agent architecture with latent memory; not distillation |

### Self-Check

```
论文: SDAR (2605.15155)
类型: 第一类(OPD方法) - RL-Augmented OPSD for multi-turn agents
判定级别: Level 2
判定: 收录
证据: "On-Policy Self-Distillation (OPSD) complements RL by introducing dense token-level guidance from a teacher branch augmented with privileged context"; SDAR "treats OPSD as a gated auxiliary objective while keeping RL as the primary optimization backbone"; "maps detached token-level signals into a sigmoid gate, strengthening distillation on teacher-endorsed positive-gap tokens"; student generates on-policy rollouts in multi-turn environments, teacher with privileged context provides dense supervision
综述状态: 待加入下次综述 (§4.3 + §8.2)
```
