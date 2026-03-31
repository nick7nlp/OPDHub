# On-Policy Distillation for LLMs — 2026 年新论文 (Jan–Mar 2026)

> 搜索时间: 2026-03-26
> 搜索范围: arXiv API (all:distill*, all:distilling, all:distillation) + web search
> 筛选标准: 与 on-policy distillation / LLM knowledge distillation 直接相关
> 所有 arXiv ID 已通过 API 验证

---

## 一、核心 On-Policy Distillation 新方法

### 1. Scaling Reasoning Efficiently via Relaxed On-Policy Distillation
- **arXiv ID**: 2603.11137
- **作者**: Jongwoo Ko, Sara Abdali, Young Jin Kim, Tianyi Chen, Pashmina Cameron
- **发表/预印**: arXiv preprint, 2026-03-11
- **核心贡献**: 将 on-policy distillation 理论性地解释为一种 policy optimization，并提出 relaxed on-policy distillation，通过理论和实验表明该方法能稳定训练、避免 negative transfer，高效地将推理能力转移给 capacity-constrained 模型。
- **与 OPD 的关系**: 直接扩展 GKD/DistiLLM 框架，提供 OPD 的理论基础和改进方法
- **建议放入 Section**: Core OPD Methods / Theoretical Foundations
- **BibTeX key 建议**: ko2026relaxed

### 2. Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models
- **arXiv ID**: 2601.18734
- **作者**: Siyan Zhao, Zhihui Xie, Mengchen Liu, Jing Huang, Guan Pang
- **发表/预印**: arXiv preprint, 2026-01-26
- **核心贡献**: 提出 On-Policy Self-Distillation (OPSD)，单个 LLM 同时充当 teacher 和 student（通过不同 context），在 student 自己的 trajectory 上进行 self-distillation。证明 sufficiently capable LLM 可以 rationalize external privileged reasoning traces 并教授自己的 weaker version。
- **与 OPD 的关系**: 将 on-policy distillation 与 self-distillation 统一，无需独立 teacher
- **建议放入 Section**: Core OPD Methods / Self-Distillation
- **BibTeX key 建议**: zhao2026selfdistilled

### 3. Entropy-Aware On-Policy Distillation of Language Models
- **arXiv ID**: 2603.07079
- **作者**: Woogyeol Jin, Taywon Min, Yongjin Yang, Swanand Ravindra Kadhe, Yi Zhou
- **发表/预印**: arXiv preprint, 2026-03-07
- **核心贡献**: 分析 on-policy distillation 使用 reverse KL divergence 时 student 过度 mode-seeking 的问题，提出 entropy-aware 的 distillation 方法，在 teacher 高 confidence 区域和低 confidence 区域使用不同策略，提高蒸馏的稳定性和效果。
- **与 OPD 的关系**: 直接改进 on-policy distillation 的 loss 设计
- **建议放入 Section**: Core OPD Methods / Loss Functions
- **BibTeX key 建议**: jin2026entropy

### 4. Stable On-Policy Distillation through Adaptive Target Reformulation
- **arXiv ID**: 2601.07155
- **作者**: Ijun Jang, Jewon Yeom, Juan Yeo, Hyunggu Lim, Taesup Kim
- **发表/预印**: arXiv preprint, 2026-01-12
- **核心贡献**: 解决 on-policy KD 中因 training-inference distribution mismatch 导致的不稳定性，通过 adaptive target reformulation 动态调整 teacher 的 supervision target，使其适应 student 当前的 generation distribution。
- **与 OPD 的关系**: 直接改进 on-policy distillation 稳定性
- **建议放入 Section**: Core OPD Methods / Training Stability
- **BibTeX key 建议**: jang2026stable

### 5. Learning beyond Teacher: Generalized On-Policy Distillation with Reward Extrapolation
- **arXiv ID**: 2602.12125
- **作者**: Wenkai Yang, Weijie Liu, Ruobing Xie, Kai Yang, Saiyong Yang
- **发表/预印**: arXiv preprint, 2026-02-12
- **核心贡献**: 提出 Generalized OPD with Reward Extrapolation，在 student-generated trajectories 上不仅对齐 teacher logits，还通过 reward extrapolation 让 student 学习超越 teacher 的能力。证明 OPD 经常优于 off-policy distillation 和 RL。
- **与 OPD 的关系**: 核心 OPD 方法，提出"超越 teacher"的蒸馏范式
- **建议放入 Section**: Core OPD Methods / Beyond Teacher
- **BibTeX key 建议**: yang2026beyond

### 6. Fast and Effective On-policy Distillation from Reasoning Prefixes
- **arXiv ID**: 2602.15260
- **作者**: Dongxu Zhang, Zhichao Yang, Sepehr Janghorbani, Jun Han, Andrew Ressler
- **发表/预印**: arXiv preprint, 2026-02-16
- **核心贡献**: 解决 OPD 需要 expensive on-the-fly teacher sampling 的效率问题，通过 reasoning prefixes 策略（student 生成 prefix，teacher 只补全后续部分）大幅减少 teacher 推理开销，同时保留 on-policy 的分布匹配优势。
- **与 OPD 的关系**: 直接解决 OPD 的效率瓶颈
- **建议放入 Section**: Core OPD Methods / Efficient Training
- **BibTeX key 建议**: zhang2026fast

### 7. OVD: On-policy Verbal Distillation
- **arXiv ID**: 2601.21968
- **作者**: Jing Xiong, Hui Shen, Shansan Gong, Yuxin Cheng, Jianghan Shen
- **发表/预印**: arXiv preprint, 2026-01-29
- **核心贡献**: 提出 On-policy Verbal Distillation (OVD)，突破传统 token-level on-policy distillation 需要 student-teacher token alignment 的限制。OVD 在 verbal/sequence level 进行蒸馏，允许 student 和 teacher 使用不同的 tokenizer 或 vocabulary。
- **与 OPD 的关系**: 将 OPD 从 token-level 扩展到 verbal/sequence-level
- **建议放入 Section**: Core OPD Methods / Sequence-Level Distillation
- **BibTeX key 建议**: xiong2026ovd

### 8. On-Policy Context Distillation for Language Models
- **arXiv ID**: 2602.12275
- **作者**: Tianzhu Ye, Li Dong, Xun Wu, Shaohan Huang, Furu Wei
- **发表/预印**: arXiv preprint, 2026-02-12
- **核心贡献**: 提出 On-Policy Context Distillation (OPCD)，将 on-policy distillation 与 context distillation 统一，student 在自己生成的 trajectories 上训练，同时最小化与 context-conditioned teacher 之间的 reverse KL divergence。将 in-context 知识内化到模型参数中。
- **与 OPD 的关系**: 将 OPD 与 context distillation 结合的新范式
- **建议放入 Section**: Core OPD Methods / Context Distillation
- **BibTeX key 建议**: ye2026opcd

---

## 二、Self-Distillation & Self-Play 相关

### 9. On-Policy Self-Distillation for Reasoning Compression (OPSDC)
- **arXiv ID**: 2603.05433
- **作者**: Hejian Sang, Yuanda Xu, Zhengze Zhou, Ran He, Zhipeng Wang
- **发表/预印**: arXiv preprint, 2026-03-05
- **核心贡献**: 提出 OPSDC，让模型通过自蒸馏来压缩自己的推理过程（concise reasoning）。模型从自己的 concise behavior 中学习，将冗长的 reasoning trace 压缩为更精炼的版本，同时保持推理质量。
- **与 OPD 的关系**: 将 on-policy self-distillation 用于 reasoning compression
- **建议放入 Section**: Self-Distillation / Reasoning Efficiency
- **BibTeX key 建议**: sang2026opsdc

### 10. PACED: Distillation and Self-Distillation at the Frontier of Student Competence
- **arXiv ID**: 2603.11178
- **作者**: Yuanda Xu, Hejian Sang, Zhengze Zhou, Ran He, Zhipeng Wang
- **发表/预印**: arXiv preprint, 2026-03-11
- **核心贡献**: 揭示标准蒸馏在两端浪费计算：已掌握的问题（near-zero gradients）和远超能力的问题（incoherent gradients）。提出 PACED，自动选择在 student 能力边界的 "frontier" 样本进行蒸馏，显著提升效率。
- **与 OPD 的关系**: 为 OPD 提供 curriculum / sample selection 策略
- **建议放入 Section**: Training Strategies / Curriculum for Distillation
- **BibTeX key 建议**: xu2026paced

### 11. Reinforcement Learning via Self-Distillation
- **arXiv ID**: 2601.20802
- **作者**: Jonas Hübotter, Frederike Lübeck, Lejs Behric, Anton Baumann, Marco Bagatella
- **发表/预印**: arXiv preprint, 2026-01-28
- **核心贡献**: 将 RL 与 self-distillation 统一，通过 self-distillation 解决 RLVR 中只有 scalar outcome reward 带来的 credit-assignment 困难。模型从自己成功的 trajectories 中 distill dense token-level signals。
- **与 OPD 的关系**: 将 self-distillation 作为 RL 的替代/补充，dense signal 学习
- **建议放入 Section**: Self-Distillation / RL Integration
- **BibTeX key 建议**: hubotter2026rlsd

### 12. Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?
- **arXiv ID**: 2603.24472
- **作者**: Jeonghye Kim, Xufang Luo, Minbeom Kim, Sangmook Lee, Dohyung Kim
- **发表/预印**: arXiv preprint, 2026-03-25
- **核心贡献**: 系统分析 self-distillation 在数学推理中可能导致性能下降的原因。发现 self-distillation 可能 suppress epistemic exploration，导致 response 长度缩短但准确率下降。为 self-distillation 的局限性提供理论解释。
- **与 OPD 的关系**: 对 self-distillation 方法的重要分析/警示
- **建议放入 Section**: Analysis / Limitations of Self-Distillation
- **BibTeX key 建议**: kim2026whysd

### 13. DARC: Decoupled Asymmetric Reasoning Curriculum for LLM Evolution
- **arXiv ID**: 2601.13761
- **作者**: Shengda Fan, Xuyan Ye, Yankai Lin
- **发表/预印**: arXiv preprint, 2026-01-20
- **核心贡献**: 提出 DARC 框架，通过 decoupled asymmetric 的 self-play 实现 LLM 自我进化。解决现有 self-play 框架因 non-stationary objectives 和 bootstrapping errors 导致的不稳定性。
- **与 OPD 的关系**: Self-play + distillation 的组合方法
- **建议放入 Section**: Self-Play / Self-Improvement
- **BibTeX key 建议**: fan2026darc

### 14. Learning While Staying Curious: Entropy-Preserving SFT via Adaptive Self-Distillation
- **arXiv ID**: 2602.02244
- **作者**: Hao Wang, Hao Gu, Hongming Piao, Kaixiong Gong, Yuxiao Ye
- **发表/预印**: arXiv preprint, 2026-02-02
- **核心贡献**: 解决 SFT-then-RL pipeline 中 SFT 阶段的 overconfidence 问题。通过 entropy-preserving self-distillation 在 SFT 阶段保持生成多样性，为后续 RL 阶段留出探索空间。
- **与 OPD 的关系**: Self-distillation 用于改进 SFT→RL pipeline
- **建议放入 Section**: Self-Distillation / Pre-RL Training
- **BibTeX key 建议**: wang2026curious

### 15. Learning from Partial Chain-of-Thought via Truncated-Reasoning Self-Distillation
- **arXiv ID**: 2603.13274
- **作者**: Gianluigi Silvestri, Edoardo Cetin
- **发表/预印**: arXiv preprint, 2026-02-27
- **核心贡献**: 研究 reasoning model 的冗余推理问题，提出 truncated-reasoning self-distillation，让模型从 partial/truncated CoT traces 中学习，在保持准确率的同时大幅减少推理长度。
- **与 OPD 的关系**: Self-distillation + reasoning efficiency
- **建议放入 Section**: Self-Distillation / Reasoning Compression
- **BibTeX key 建议**: silvestri2026truncated

---

## 三、Reasoning Distillation 新进展

### 16. Reinforcement-aware Knowledge Distillation for LLM Reasoning
- **arXiv ID**: 2602.22495
- **作者**: Zhaoyang Zhang, Shuli Jiang, Yantao Shen, Yuting Zhang, Dhananjay Ram
- **发表/预印**: arXiv preprint, 2026-02-26
- **核心贡献**: 指出现有 KD 方法主要为 supervised learning 设计，不适合 RL post-training 后的推理模型。提出 reinforcement-aware KD，在蒸馏过程中保留 RL 训练获得的推理模式（如 backtracking、verification）。
- **与 OPD 的关系**: 将 RL 的 reasoning patterns 纳入 distillation
- **建议放入 Section**: Reasoning Distillation / RL-aware Methods
- **BibTeX key 建议**: zhang2026rkd

### 17. HDPO: Hybrid Distillation Policy Optimization via Privileged Self-Distillation
- **arXiv ID**: 2603.23871
- **作者**: Ken Ding
- **发表/预印**: arXiv preprint, 2026-03-25
- **核心贡献**: 解决 RL 训练中模型对 "cliff" prompts（完全无法解决的问题）的学习信号消失问题。通过 privileged self-distillation，将带有 privileged information 的 teacher 的知识蒸馏到无 privileged access 的 student policy。
- **与 OPD 的关系**: 将 privileged information + on-policy distillation + RL 统一
- **建议放入 Section**: Reasoning Distillation / RL + Distillation Hybrid
- **BibTeX key 建议**: ding2026hdpo

### 18. Privileged Information Distillation for Language Models
- **arXiv ID**: 2602.04942
- **作者**: Emiliano Penaloza, Dheeraj Vattikonda, Nicolas Gontier, Alexandre Lacoste, Laurent Charlin
- **发表/预印**: arXiv preprint, 2026-02-04
- **核心贡献**: 利用 training-time privileged information (PI) 增强 LLM 在 hard/long-horizon settings 中的能力，然后通过 distillation 将 PI-enhanced 能力转移到 inference-time 无法获取 PI 的 policy 上。
- **与 OPD 的关系**: Privileged information + distillation 的新范式
- **建议放入 Section**: Reasoning Distillation / Privileged Information
- **BibTeX key 建议**: penaloza2026privileged

### 19. Long-Chain Reasoning Distillation via Adaptive Prefix Alignment
- **arXiv ID**: 2601.10064
- **作者**: Zhenghao Liu, Zhuoyang Wu, Xinze Li, Yukun Yan, Shuo Wang
- **发表/预印**: arXiv preprint, 2026-01-15
- **核心贡献**: 解决 teacher-generated long reasoning trajectories 与 student 能力不匹配的问题。提出 adaptive prefix alignment，通过动态对齐 teacher 的推理前缀和 student 的推理能力边界来提高蒸馏效果。
- **与 OPD 的关系**: 为长链推理蒸馏提供 alignment 策略
- **建议放入 Section**: Reasoning Distillation / Long-CoT
- **BibTeX key 建议**: liu2026longchain

### 20. Hán Dān Xué Bù or Qīng Chū Yú Lán? A Cognitive Perspective on Reasoning Distillation
- **arXiv ID**: 2601.05019
- **作者**: Yueqing Hu, Xinyang Peng, Shuting Peng, Hanqi Wang, Tianhong Wang
- **发表/预印**: arXiv preprint, 2026-01-08
- **核心贡献**: 从认知科学角度分析 reasoning distillation，发现通过 SFT 的 mimicry-based distillation 未能传递 RL 训练获得的 "natural" cognitive alignment。提出 reasoning distillation 应超越表面模仿。
- **与 OPD 的关系**: 为 reasoning distillation 提供认知科学理论基础
- **建议放入 Section**: Reasoning Distillation / Theoretical Analysis
- **BibTeX key 建议**: hu2026cognitive

### 21. Curriculum Learning for Efficient CoT Distillation via Structure-Aware Masking and GRPO
- **arXiv ID**: 2602.17686
- **作者**: Bowen Yu, Maolin Wang, Sheng Zhang, Binhao Wang, Yi Wen
- **发表/预印**: arXiv preprint, 2026-02-05
- **核心贡献**: 解决 teacher CoT rationales 过于 verbose、小模型难以 reproduce 的问题。通过 structure-aware masking 选择性关注 CoT 中的关键结构，结合 GRPO 优化，实现高效的 CoT 蒸馏。
- **与 OPD 的关系**: CoT distillation 的 curriculum 和 masking 策略
- **建议放入 Section**: Reasoning Distillation / Curriculum Learning
- **BibTeX key 建议**: yu2026curriculum

### 22. Which Reasoning Trajectories Teach Students to Reason Better?
- **arXiv ID**: 2601.14249
- **作者**: Yuming Yang, Mingyoung Lai, Wanxu Zhao, Xiaoran Fan, Zhiheng Xi
- **发表/预印**: arXiv preprint, 2026-01-20
- **核心贡献**: 提出 informative alignment metric，度量哪些 reasoning trajectories 最适合蒸馏。发现更强的 teacher 不一定产生更好的 student，trajectory 与 student 能力的匹配度更关键。
- **与 OPD 的关系**: 数据选择策略，直接影响 OPD 效果
- **建议放入 Section**: Reasoning Distillation / Data Selection
- **BibTeX key 建议**: yang2026trajectories

---

## 四、Speculative Decoding + Distillation

### 23. Self-Distillation for Multi-Token Prediction
- **arXiv ID**: 2603.23911
- **作者**: Guoliang Zhao, Ruobing Xie, An Wang, Shuaipeng Li, Huaibing Xie
- **发表/预印**: arXiv preprint, 2026-03-25
- **核心贡献**: 通过 self-distillation 训练 multi-token prediction (MTP) heads，提高 MTP 的 acceptance rate。解决 MTP heads 预测准确率不足导致加速效果有限的问题。
- **与 OPD 的关系**: Self-distillation + speculative decoding/MTP
- **建议放入 Section**: Speculative Decoding + Distillation
- **BibTeX key 建议**: zhao2026mtp

### 24. Multi-Token Prediction via Self-Distillation
- **arXiv ID**: 2602.06019
- **作者**: John Kirchenbauer, Abhimanyu Hans, Brian Bartoldson, Micah Goldblum, Ashwinee Panda
- **发表/预印**: arXiv preprint, 2026-02-05
- **核心贡献**: 提出将 pretrained autoregressive LM 通过 self-distillation 从 single next-token predictor 转换为 multi-token predictor，无需额外 speculator 模型或复杂 inference pipeline。为加速推理提供新思路。
- **与 OPD 的关系**: Self-distillation 用于推理加速
- **建议放入 Section**: Speculative Decoding + Distillation
- **BibTeX key 建议**: kirchenbauer2026mtp

### 25. Flatter Tokens are More Valuable for Speculative Draft Model Training
- **arXiv ID**: 2601.18902
- **作者**: Jiaming Fan, Daming Cao, Xiangzhong Luo, Jiale Fu, Chonghan Liu
- **发表/预印**: arXiv preprint, 2026-01-26
- **核心贡献**: 从 data-centric 角度研究 speculative decoding 的 draft model 训练，发现 "flatter" tokens（logit distribution 更均匀的 tokens）对 SD acceptance rate 贡献更大。提出基于 token flatness 的数据选择策略。
- **与 OPD 的关系**: 为 SpecKD/DistillSpec 类方法提供 data selection 视角
- **建议放入 Section**: Speculative Decoding + Distillation
- **BibTeX key 建议**: fan2026flatter

### 26. TriSpec: Ternary Speculative Decoding via Lightweight Proxy Verification
- **arXiv ID**: 2601.23180
- **作者**: Haoyun Jiang, Junqi He, Feng Hong, Xinlong Yang, Jianwei Zhang
- **发表/预印**: arXiv preprint, 2026-01-30
- **核心贡献**: 提出 ternary speculative decoding，引入 lightweight proxy verifier（通过 distillation 训练）替代 full target model verification，在 draft-verify pipeline 中实现更高效的推理。
- **与 OPD 的关系**: Distillation 在 speculative decoding verification 中的应用
- **建议放入 Section**: Speculative Decoding + Distillation
- **BibTeX key 建议**: jiang2026trispec

---

## 五、KD Framework & Efficiency

### 27. KDFlow: A User-Friendly and Efficient Knowledge Distillation Framework for LLMs
- **arXiv ID**: 2603.01875
- **作者**: Songming Zhang, Xue Zhang, Tong Zhang, Bojie Hu, Yufeng Chen
- **发表/预印**: arXiv preprint, 2026-03-02
- **核心贡献**: 提出异构训练后端 KD 框架，为 student 和 teacher 使用不同的训练后端（如 FSDP vs vLLM），解决现有框架对 student 和 teacher 使用同一后端导致的效率问题。
- **与 OPD 的关系**: 为 OPD 提供系统层面的工程支撑
- **建议放入 Section**: Systems / Efficient Distillation
- **BibTeX key 建议**: zhang2026kdflow

### 28. X-KD: General Experiential Knowledge Distillation for LLMs
- **arXiv ID**: 2602.12674
- **作者**: Yuang Cai, Yuyu Yuan
- **发表/预印**: arXiv preprint, 2026-02-13
- **核心贡献**: 提出 experiential KD，不仅模仿 teacher 行为，还重现 teacher 的 learning environment，让 student 在类似的 learning experience 中获取知识，而非仅复制输出分布。
- **与 OPD 的关系**: 新的 KD 范式，关注 learning process 而非 output
- **建议放入 Section**: KD Methods / Experience-based
- **BibTeX key 建议**: cai2026xkd

### 29. DWA-KD: Dual-Space Weighting and Time-Warped Alignment for Cross-Tokenizer KD
- **arXiv ID**: 2602.21669
- **作者**: Duc Trung Vu, Pham Khanh Chi, Dat Phi Van, Linh Ngo Van, Sang Dinh
- **发表/预印**: arXiv preprint, 2026-02-25
- **核心贡献**: 解决 cross-tokenizer distillation 的 alignment 问题，通过 dual-space weighting 和 time-warped alignment 使不同 tokenizer 的 teacher 和 student 之间可以有效蒸馏。
- **与 OPD 的关系**: 解决 OPD 中 tokenizer 不匹配问题
- **建议放入 Section**: KD Methods / Cross-Tokenizer
- **BibTeX key 建议**: vu2026dwakd

### 30. Don't Ignore the Tail: Decoupling top-K Probabilities for Efficient LM Distillation
- **arXiv ID**: 2602.20816
- **作者**: Sayantan Dasgupta, Trevor Cohn, Timothy Baldwin
- **发表/预印**: arXiv preprint, 2026-02-24
- **核心贡献**: 分析 KD 中通常只使用 top-K logits 带来的信息损失，提出 decoupled top-K probability method 保留 tail distribution 信息，在高效传输 logits 的同时保持蒸馏质量。
- **与 OPD 的关系**: 改进 logit-level distillation 的效率
- **建议放入 Section**: KD Methods / Efficient Logit Transfer
- **BibTeX key 建议**: dasgupta2026tail

---

## 六、On-Policy + RL/Alignment 交叉

### 31. ORBIT: On-policy Exploration-Exploitation for Controllable Multi-Budget Reasoning
- **arXiv ID**: 2601.08310
- **作者**: Kun Liang, Clive Bai, Xin Xu, Chenming Tang, Sanwoo Lee
- **发表/预印**: arXiv preprint, 2026-01-13
- **核心贡献**: 提出 on-policy exploration-exploitation 框架，实现 controllable multi-budget reasoning：根据问题难度动态分配推理 compute budget，在简单问题上快速推理、难题上深度推理。
- **与 OPD 的关系**: On-policy 训练范式 + reasoning budget control
- **建议放入 Section**: On-Policy Training / Budget Control
- **BibTeX key 建议**: liang2026orbit

### 32. Coverage Improvement and Fast Convergence of On-policy Preference Learning
- **arXiv ID**: 2601.08421
- **作者**: Juno Kim, Jihun Yun, Jason D. Lee, Kwang-Sung Jun
- **发表/预印**: arXiv preprint, 2026-01-13
- **核心贡献**: 为 on-policy preference learning (如 online DPO) 提供理论分析，解释为何 on-policy 方法显著优于 offline 方法。分析 sampling policy 的 coverage 如何随训练演化，建立收敛速率保证。
- **与 OPD 的关系**: 为 on-policy 训练范式提供理论支撑
- **建议放入 Section**: Theoretical Foundations / On-Policy Training
- **BibTeX key 建议**: kim2026coverage

### 33. Ratio-Variance Regularized Policy Optimization for Efficient LLM Fine-tuning
- **arXiv ID**: 2601.03320
- **作者**: Yu Luo, Shuo Han, Yihan Hu, Dong Li, Jianye Hao
- **发表/预印**: arXiv preprint, 2026-01-06
- **核心贡献**: 改进 PPO/GRPO 中的 policy ratio clipping，通过 ratio-variance regularization 替代 hard clipping，提高 on-policy RL 训练稳定性和效率。
- **与 OPD 的关系**: 改进 on-policy 优化的基础算法
- **建议放入 Section**: On-Policy Optimization / Algorithm
- **BibTeX key 建议**: luo2026rvrpo

### 34. Off-Policy Value-Based Reinforcement Learning for Large Language Models
- **arXiv ID**: 2603.23355
- **作者**: Peng-Yuan Wang, Ziniu Li, Tian Xu, Bohan Yang, Tian-Shuo Liu
- **发表/预印**: arXiv preprint, 2026-03-24
- **核心贡献**: 指出当前 LLM RL 方法主要是 on-policy 的（每批数据只用一次），在 long-horizon 任务中效率低。提出 off-policy value-based RL 方法提高 data utilization。与 on-policy 方法形成互补。
- **与 OPD 的关系**: On-policy vs off-policy 的对比分析和互补方案
- **建议放入 Section**: Related Work / Off-Policy Alternatives
- **BibTeX key 建议**: wang2026offpolicy

---

## 七、多模态蒸馏 & 应用

### 35. CORD: Bridging the Audio-Text Reasoning Gap via Weighted On-policy Cross-modal Distillation
- **arXiv ID**: 2601.16547
- **作者**: Jing Hu, Danxiang Zhu, Xianlong Luo, Dan Zhang, Shuwei He
- **发表/预印**: arXiv preprint, 2026-01-23
- **核心贡献**: 提出 weighted on-policy cross-modal distillation，解决 Large Audio Language Models (LALMs) 中 audio modality 导致知识和推理能力退化的问题。通过 on-policy distillation 从 text LLM 向 audio LLM 转移推理能力。
- **与 OPD 的关系**: On-policy distillation 在多模态（audio-text）场景的应用
- **建议放入 Section**: Multi-Modal Distillation / Audio-Text
- **BibTeX key 建议**: hu2026cord

### 36. Video-OPD: Efficient Post-Training of MLLMs for Temporal Video Grounding via On-Policy Distillation
- **arXiv ID**: 2602.02994
- **作者**: Jiaze Li, Hao Yin, Haoran Xu, Boshen Xu, Wenhui Tan
- **发表/预印**: arXiv preprint, 2026-02-03
- **核心贡献**: 将 on-policy distillation 应用到 multimodal LLM 的 temporal video grounding 任务。用 OPD 替代 GRPO 中的 sparse reward，解决 RL 在 video grounding 中 reward signal 稀疏的问题。
- **与 OPD 的关系**: OPD 在 video understanding 领域的应用
- **建议放入 Section**: Multi-Modal Distillation / Video
- **BibTeX key 建议**: li2026videoopd

---

## 八、Industry Practice / Large-Scale System

### 37. Nemotron-Cascade 2: Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation
- **arXiv ID**: 2603.19220
- **作者**: Zhuolin Yang, Zihan Liu, Yang Chen, Wenliang Dai, Boxin Wang (NVIDIA)
- **发表/预印**: arXiv preprint, 2026-03-19
- **核心贡献**: NVIDIA 开源的 30B MoE 模型，使用 cascade RL 和 multi-domain on-policy distillation 进行 post-training。展示了 OPD 在工业级模型训练中的实践，将数学和代码推理能力从大模型蒸馏到小 MoE。
- **与 OPD 的关系**: OPD 的工业级大规模应用案例
- **建议放入 Section**: Industry Practice / Large-Scale OPD
- **BibTeX key 建议**: yang2026nemotron

### 38. Distilling Token-Trained Models into Byte-Level Models
- **arXiv ID**: 2602.01007
- **作者**: Zishuo Bao, Jiaqi Leng, Junxiong Wang, Bowen Peng, Yucheng Lu
- **发表/预印**: arXiv preprint, 2026-02-01
- **核心贡献**: 提出高效的 distillation recipe 将 token-level LLM 蒸馏为 byte-level language model (BLM)，避免从头训练 BLM 的巨大开销。展示 distillation 可以跨越不同 granularity (token vs byte)。
- **与 OPD 的关系**: Distillation 跨 granularity 的新应用
- **建议放入 Section**: Systems / Architecture-Crossing Distillation
- **BibTeX key 建议**: bao2026bytelm

### 39. Distribution-Aligned Sequence Distillation for Superior Long-CoT Reasoning
- **arXiv ID**: 2601.09088
- **作者**: Shaotian Yan, Kaiyuan Liu, Chen Shen, Bing Wang, Sinan Fan
- **发表/预印**: arXiv preprint, 2026-01-14
- **核心贡献**: 提出 distribution-aligned sequence distillation (DASD)，通过对齐 teacher 和 student 的 sequence-level distribution（而非 token-level），实现更稳定的 long-CoT reasoning distillation。
- **与 OPD 的关系**: Sequence-level distribution alignment 的蒸馏方法
- **建议放入 Section**: Reasoning Distillation / Sequence-Level
- **BibTeX key 建议**: yan2026dasd

### 40. Demystifying Low-Rank KD in LLMs: Convergence, Generalization, and Information-Theoretic Guarantees
- **arXiv ID**: 2603.22355
- **作者**: Alberlucia Rafael Soarez, Daniel Kim, Mariana Costa, Alejandro Torre
- **发表/预印**: arXiv preprint, 2026-03-22
- **核心贡献**: 为 low-rank knowledge distillation (如 Low-Rank Clone) 提供理论保证，包括收敛性、泛化界和信息论下界。是 KD 理论方面的重要贡献。
- **与 OPD 的关系**: KD 的理论分析
- **建议放入 Section**: Theoretical Foundations
- **BibTeX key 建议**: soarez2026lowrank

---

## 摘要统计

| 类别 | 数量 |
|------|------|
| 核心 On-Policy Distillation 新方法 | 8 |
| Self-Distillation & Self-Play | 7 |
| Reasoning Distillation | 7 |
| Speculative Decoding + Distillation | 4 |
| KD Framework & Efficiency | 4 |
| On-Policy + RL/Alignment | 4 |
| 多模态蒸馏 | 2 |
| Industry Practice & Systems | 4 |
| **总计** | **40** |

## 与已有 survey 覆盖的互补关系

### 直接扩展已有方法的工作
- **GKD 的后续**: 2603.11137 (Relaxed OPD), 2603.07079 (Entropy-Aware OPD), 2601.07155 (Adaptive Target)
- **MiniLLM/DistiLLM 的后续**: 2602.12125 (Beyond Teacher), 2602.15260 (Fast OPD)
- **SPIN 的后续**: 2601.13761 (DARC), 自博弈新方向
- **SpecKD/DistillSpec 的后续**: 2603.23911, 2602.06019, 2601.18902, 2601.23180

### 新兴方向（survey 可能需要新增 section）
1. **On-policy self-distillation** (无需独立 teacher): 2601.18734, 2603.05433, 2601.20802
2. **Reasoning-aware distillation** (保留 RL reasoning patterns): 2602.22495, 2601.05019
3. **Cross-modal on-policy distillation**: 2601.16547, 2602.02994
4. **On-policy context distillation**: 2602.12275
5. **OPD 理论基础**: 2603.11137, 2601.08421
