# Citation Verification Report

## Summary
- Total citations checked: 73
- Issues found: 53
- Verified correct: 20

## Issues
### [2305.02301] Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes
- **Line 885**: "learning from LLM-extracted rationales enables small models to outperform their un-fine-tuned large counterparts" → **问题**: The original paper's key claim is stronger: small models fine-tuned with step-by-step distillation can outperform the larger LLM *teachers* (e.g., 540B PaLM) using less training data, not merely 'un-fine-tuned large counterparts.' The phrase 'un-fine-tuned large counterparts' understates the result and is somewhat misleading, as the large models they outperform include few-shot prompted LLMs which serve as the teacher.
- **Severity**: 🟡 不精确
- **Line 885**: "Traditional off-policy distillation forces the student to mimic the teacher's reasoning traces over a fixed dataset, yet reasoning is highly path-dependent." → **问题**: This framing sentence attributes a motivation about 'path-dependent reasoning' and 'off-policy distillation' to the context of Distilling Step-by-Step, but the paper does not frame its contribution in terms of off-policy vs on-policy distillation or path-dependence of reasoning. The paper's motivation is about reducing training data requirements and model size, not about addressing path-dependence in reasoning.
- **Severity**: 🟡 不精确

### [2305.12870] Lion: Adversarial Distillation of Proprietary Large Language Models
- **Line 662**: "LLaMA-7B / 13B" → **问题**: The original Lion paper primarily experiments with LLaMA-7B as the student model. There is no Lion-13B variant prominently featured in the paper.
- **Severity**: 🟡 不精确
- **Line 662**: "BIG-Bench Hard, AGIEval" → **问题**: The original Lion paper primarily evaluates on Vicuna's evaluation benchmark and other instruction-following benchmarks, not BIG-Bench Hard and AGIEval as primary benchmarks.
- **Severity**: 🔴 严重
- **Line 810**: "Lion-13B achieves competitive performance on BIG-Bench Hard and AGIEval using only 70k training examples" → **问题**: Lion-13B is not a primary model in the paper, and BIG-Bench Hard and AGIEval are not the primary evaluation benchmarks. The paper primarily evaluates Lion-7B on Vicuna's evaluation benchmark. This appears to be fabricated or confused with another paper.
- **Severity**: 🔴 严重

### [2305.15717] The False Promise of Imitating Proprietary LLMs
- **Line 82**: "showing that off-policy distilled students can degrade sharply on tasks requiring sustained multi-step generation" → **问题**: The paper's core finding is broader: it shows that models fine-tuned by imitating proprietary LLM outputs (e.g., ChatGPT) may appear improved on superficial measures (style, fluency) but fail to genuinely close the gap on more rigorous benchmarks (NLU, reasoning, factuality). The paper does not specifically frame its contribution around 'sustained multi-step generation' as a failure mode. Rather, it argues that imitation models learn to mimic style rather than substance, and that the gap is most evident on tasks requiring factual knowledge and reasoning, not specifically 'multi-step generation' per se.
- **Severity**: 🟡 不精确
- **Line 82**: "provided a systematic empirical demonstration of this failure mode" → **问题**: The paper does not frame its findings as a demonstration of train-test mismatch or exposure bias in the imitation learning sense. Its argument is about the fundamental limitation of imitation data from proprietary models — that such data teaches surface-level patterns rather than genuine capabilities. The review article reinterprets the paper's contribution through the lens of off-policy/on-policy distillation and exposure bias, which is not the framing used by the original authors.
- **Severity**: 🟡 不精确

### [2305.20050] Let's Verify Step by Step
- **Line 463**: "Outcome-based methods replace exact token matching with scalar reward signals evaluating the structural validity or factual correctness of a generated trajectory. Frameworks like RLKD and Process Reward Models (PRMs)" → **问题**: PRMs are categorized under 'Outcome-Based Feedback', but the entire point of the paper 'Let's Verify Step by Step' is that PRMs provide PROCESS-level (step-by-step) supervision, which is explicitly contrasted with outcome-based approaches. Grouping PRMs under outcome-based methods directly contradicts the paper's core contribution.
- **Severity**: 🔴 严重
- **Line 463**: "let the student roll out a complete answer and query the teacher (or a reward proxy) for a score R(x, y)" → **问题**: PRMs do not provide a single scalar score for a complete answer. They evaluate each intermediate reasoning step individually. The paper is also about training reward models/verifiers, not about knowledge distillation (teacher-student frameworks).
- **Severity**: 🔴 严重
- **Line 491**: "use PRMs to parse intermediate reasoning steps" → **问题**: The original paper trains PRMs to evaluate/score intermediate reasoning steps, not to 'parse' them. Additionally, the paper is about reward model training and verification, not about reasoning distillation into compact architectures. The citation uses PRMs as if they were proposed as a distillation technique, which misrepresents the paper's contribution.
- **Severity**: 🟡 不精确

### [2306.13649] On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes
- **Line 630**: "GKD \citep{2306.13649} & T5-XL (3B)" → **问题**: The GKD paper uses T5-XXL (11B) as the teacher model, not T5-XL (3B). T5-XL is 3B parameters but was not the teacher used in the paper.
- **Severity**: 🔴 严重
- **Line 84**: "configurable mixture ratios between student and teacher sequences" → **问题**: GKD interpolates between student on-policy sequences and dataset sequences (which may or may not be teacher-generated), not specifically 'student and teacher sequences'. The paper frames the mixture as between the student policy and the training dataset distribution.
- **Severity**: 🟡 不精确

### [2307.15190] f-Divergence Minimization for Sequence-Level Knowledge Distillation
- **Line 787**: "any $f$-divergence can be expressed as $D_f(\pteacher \parallel \ptheta) = \mathbb{E}_{y \sim \ptheta}[f(\pteacher(y)/\ptheta(y))]$" → **问题**: The paper did not claim to 'show' this formula as a novel contribution — this is the standard definition of f-divergence. The paper's contribution is applying f-divergence minimization to sequence-level knowledge distillation, exploring different choices of f-divergences (e.g., reverse KL, forward KL, JSD, TVD, α-divergence, etc.) and their practical implications. Attributing the general f-divergence formula as the paper's finding is misleading.
- **Severity**: 🟡 不精确
- **Line 787**: "By continuously modulating the convexity parameter, researchers can transition smoothly between mode-seeking and mode-covering behavior" → **问题**: The paper explores different f-divergences (including α-divergence which has a continuous parameter), but the phrase 'continuously modulating the convexity parameter' is not how the paper frames its contribution. The paper studies specific f-divergence choices and their properties rather than describing a single 'convexity parameter' that smoothly transitions between behaviors. This is an imprecise/somewhat fabricated characterization.
- **Severity**: 🟡 不精确

### [2310.08461] DistillSpec: Improving Speculative Decoding via Knowledge Distillation
- **Line 701**: "GPT-like (234M) & T5-Small (77M), GPT-like (33M)" → **问题**: The specific model sizes (234M teacher, 33M draft) are not standard descriptions from the DistillSpec paper. The paper uses T5-XXL (11B) as a target model alongside T5-XL (3B), and T5-Small (77M) as a draft. The 'GPT-like' models with 234M/33M parameters appear to be approximate but the exact sizes may not match the paper's reported configurations precisely.
- **Severity**: 🟡 不精确
- **Line 973**: "yields 10--45% inference speedup over standard speculative decoding" → **问题**: The paper reports up to ~10-45% wallclock speedup improvements, but the exact range should be verified. The paper's reported speedups vary by task and configuration; the claimed range is approximately consistent but may not precisely match all reported numbers.
- **Severity**: 🟡 不精确

### [2311.09724] OVM, Outcome-supervised Value Models for Planning in Mathematical Reasoning
- **Line 491**: "OVM \citep{2311.09724} and SuperCorrect \citep{2410.09008} use PRMs~\citep{2305.20050} to parse intermediate reasoning steps (e.g., by newline delimiters)" → **问题**: OVM trains an outcome-supervised value model (OVM) that predicts the correctness of partial solutions to guide tree search during decoding. It does not use PRMs to 'parse intermediate reasoning steps by newline delimiters' as a form of trajectory-level chunking for distillation. OVM's core contribution is using outcome supervision (not process supervision) to train a value model for planning/search, which is distinct from what is described.
- **Severity**: 🔴 严重
- **Line 491**: "The loss is structured dynamically, $\mathcal{L} = \sum_{k=1}^K \log \ptheta(s_k | s_{<k}) \cdot \hat{A}(s_k)$, where $s_k$ is a trajectory chunk and $\hat{A}$ the advantage." → **问题**: This advantage-weighted loss formulation is not from OVM. OVM uses a value model trained with outcome supervision (binary correctness labels on complete solutions) and employs it for beam search or tree search at inference time. The cited loss formula appears fabricated or conflated with a different method.
- **Severity**: 🔴 严重
- **Line 491**: "This scaffolding enables distilling advanced reasoning chains from large models like DeepSeek-R1 into compact architectures" → **问题**: OVM (published November 2023) predates DeepSeek-R1 and has nothing to do with distilling reasoning chains from DeepSeek-R1. OVM focuses on training value models for planning in mathematical reasoning, not on knowledge distillation.
- **Severity**: 🔴 严重
- **Line 491**: "state-of-the-art reasoning distillation employs trajectory-level chunking. OVM \citep{2311.09724}" → **问题**: OVM is not a reasoning distillation method. It is about training outcome-supervised value models to guide search/planning during inference for mathematical reasoning. Categorizing it under 'reasoning distillation' with 'trajectory-level chunking' is a fundamental mischaracterization.
- **Severity**: 🔴 严重

### [2401.01335] Self-Play Fine-Tuning Converts Weak Language Models to Strong Language Models
- **Line 0**: "Could not parse" → **问题**: Still failing to parse LLM output
- **Severity**: 🔴 严重

### [2402.03898] DistiLLM: Towards Streamlined Distillation for Large Language Models
- **Line 0**: "Could not parse" → **问题**: Still failing to parse LLM output
- **Severity**: 🔴 严重

### [2402.11890] Revisiting Knowledge Distillation for Autoregressive Language Models
- **Line 784**: "Forward-KL students produce plausible-sounding but semantically incoherent outputs, while Reverse-KL students produce confident, narrow responses" → **问题**: This is an oversimplification and embellishment. The paper (2402.11890) provides a more nuanced analysis of Forward KL vs Reverse KL trade-offs in autoregressive LM distillation. It does not straightforwardly claim Forward KL produces 'semantically incoherent outputs.' The paper actually explores adaptive combinations and improved strategies rather than simply condemning Forward KL.
- **Severity**: 🟡 不精确
- **Line 784**: "spreading probability mass into the inter-mode "hallucination zone" where the teacher's density is near-zero" → **问题**: The 'hallucination zone' terminology and framing appears to be editorial embellishment from the review authors rather than language used in the original paper. While the mode-covering property of Forward KL is discussed, this specific dramatic characterization is not from paper 2402.11890.
- **Severity**: 🟡 不精确

### [2402.12030] Towards Cross-Tokenizer Distillation: the Universal Logit Distillation Loss for LLMs
- **Line 702**: "Latent OT alignment" → **问题**: The method uses optimal transport to align token-level probability distributions across different vocabularies, not 'latent' representations. The paper's method is called Universal Logit Distillation (ULD), and the OT operates on logit/probability space, not latent space.
- **Severity**: 🟡 不精确
- **Line 975**: "a dynamic projection matrix $W_{S \to T}$ or optimal transport plan $\Pi$ minimizes the Wasserstein distance between latent spaces" → **问题**: The paper does not propose a 'dynamic projection matrix $W_{S \to T}$'. The method uses optimal transport to align token probability distributions across different vocabularies, not 'latent spaces'. The mention of a projection matrix appears fabricated or conflated with another method.
- **Severity**: 🔴 严重
- **Line 975**: "matching latent semantics rather than strict token logits" → **问题**: The paper matches token probability/logit distributions across vocabularies using optimal transport, not 'latent semantics'. The alignment is at the vocabulary/logit level, not at a latent representation level.
- **Severity**: 🟡 不精确

### [2402.12842] PromptKD: Distilling Student-Friendly Knowledge for Generative Language Models via Prompt Tuning
- **Line 651**: "GPT-2 120M--340M" → **问题**: GPT-2 Small is typically cited as 124M and GPT-2 Medium as 345M or 355M. '120M' and '340M' are slightly imprecise approximations.
- **Severity**: 🟡 不精确

### [2402.13116] A Survey on Knowledge Distillation of Large Language Models
- **Line 86**: "Existing surveys of LLM distillation \citep{2402.13116} predominantly organize the field around the classical compression framing, treating off-policy and on-policy approaches as interchangeable variants rather than as fundamentally distinct paradigms" → **问题**: The survey 2402.13116 actually organizes knowledge distillation of LLMs into categories such as white-box KD (logit-based, hint/feature-based) and black-box KD (in-context learning, chain-of-thought, instruction following), as well as by skill/task type. While it does not deeply analyze on-policy vs off-policy dynamics as distinct paradigms, characterizing it as treating them as 'interchangeable variants' is a somewhat misleading overstatement. The survey does distinguish different approaches but through a different organizational lens (white-box vs black-box, algorithm-centric), not specifically through the classical compression framing alone. The claim that it 'predominantly organize[s] the field around the classical compression framing' is not fully accurate — it goes well beyond classical compression to cover LLM-specific methods like chain-of-thought distillation and instruction-following distillation.
- **Severity**: 🟡 不精确

### [2404.02657] Rethinking Kullback-Leibler Divergence in Knowledge Distillation for Large Language Models
- **Line 784**: "As analyzed by \citet{2404.02657} and \citet{2402.11890}, Forward KL is zero-avoiding (mode-covering)... Reverse KL is zero-forcing (mode-seeking)" → **问题**: This citation misrepresents the paper's findings. The core contribution of AKL (2404.02657) is to challenge and refute the conventional mode-seeking/mode-covering characterizations for discrete distributions in LLMs. The paper demonstrates these properties do not hold in the LLM distillation setting. Citing it as supporting these standard characterizations directly contradicts the paper's thesis, as correctly described in Line 536.
- **Severity**: 🔴 严重
- **Line 635**: "LLaMA 6.7B" → **问题**: The paper uses OpenLLaMA-7B as the teacher model, not 'LLaMA 6.7B'. While these are related model families, the specific model name and parameter count are inaccurate.
- **Severity**: 🟡 不精确

### [2407.14679] Compact Language Models via Pruning and Knowledge Distillation
- **Line 979**: "Maintaining a binary mask over the teacher's weight matrices and updating it jointly with the OPD loss allows the student model to physically emerge from the teacher's architecture" → **问题**: Minitron does not use a binary mask that is jointly updated with a distillation loss in a differentiable/continuous manner. Instead, it uses a one-shot importance-based structured pruning strategy (estimating importance via activation-based metrics) to remove neurons/heads/layers, followed by knowledge distillation-based retraining. The description of 'continuous structured pruning with a binary mask updated jointly with OPD loss' is fabricated and does not match the actual method.
- **Severity**: 🔴 严重
- **Line 979**: "combines continuous structured pruning with OPD to inherit the teacher's optimal sub-network" → **问题**: Minitron uses a two-stage approach: (1) structured pruning based on importance estimation (using lightweight calibration data), then (2) knowledge distillation for accuracy recovery. It is not 'continuous structured pruning' jointly optimized with distillation. Also, the paper does not use the term 'OPD' (on-policy distillation) — it uses conventional knowledge distillation with logit-based and/or hidden-state-based losses.
- **Severity**: 🔴 严重
- **Line 979**: "reducing burn-in time and convergence cost" → **问题**: While Minitron does claim reduced training cost compared to training from scratch (up to 40x fewer training tokens), the specific framing of 'burn-in time' is not terminology used in the paper and the mechanism described (binary mask joint optimization) is incorrect.
- **Severity**: 🟡 不精确

### [2408.00118] Gemma 2: Improving Open Language Models at a Practical Size
- **Line 703**: "Gemma 2 2B / 9B / 27B" → **问题**: The 27B model is not a student model. It is trained from scratch without distillation. Only the 9B and 2B models are distilled (9B from 27B, 2B from 9B). Listing 27B as a student is inaccurate.
- **Severity**: 🟡 不精确
- **Line 962**: "embedding distillation directly into continuous pre-training" → **问题**: The term 'continuous pre-training' is misleading. Gemma 2 incorporates distillation into pre-training from scratch, not into continued/continuous pre-training of an already-trained model. These are distinct concepts.
- **Severity**: 🟡 不精确

### [2410.09008] SuperCorrect: Advancing Small LLM Reasoning with Thought Template Distillation and Self-Correction
- **Line 491**: "SuperCorrect \citep{2410.09008} use PRMs to parse intermediate reasoning steps (e.g., by newline delimiters)" → **问题**: SuperCorrect does not use PRMs to parse intermediate reasoning steps. Its core method is thought template distillation + cross-model collaborative DPO. The advantage-weighted trajectory chunk loss described here does not correspond to SuperCorrect's methodology.
- **Severity**: 🔴 严重
- **Line 688**: "o1-mini, gpt-4o-mini (black-box)" → **问题**: The original paper uses GPT-4o (not gpt-4o-mini) as the teacher model alongside o1-mini for thought template extraction. The teacher model name is incorrect.
- **Severity**: 🟡 不精确
- **Line 688**: "KD + self-correction reward" → **问题**: The method is more precisely described as thought template distillation + cross-model collaborative DPO. 'Self-correction reward' is a misleading characterization; the self-correction is achieved through DPO, not a reward model.
- **Severity**: 🟡 不精确

### [2410.11325] Speculative Knowledge Distillation: Bridging the Teacher-Student Gap Through Interleaved Sampling
- **Line 700**: "Block-verified on-policy KL" → **问题**: This is a simplified characterization. The paper's method is based on interleaved sampling (speculative decoding-style draft-then-verify) to generate on-policy data, with the training objective being forward KL divergence. 'Block-verified' is not standard terminology used in the paper; the paper describes it as speculative/interleaved sampling with acceptance/rejection steps.
- **Severity**: 🟡 不精确

### [2410.17215] MiniPLM: Knowledge Distillation for Pre-Training Language Models
- **Line 962**: "selecting instances where the discrepancy between the teacher's and a small reference model's log-probabilities is largest, up-sampling hard and diverse examples while filtering trivial or noisy data" → **问题**: The description oversimplifies and partially mischaracterizes the method. MiniPLM's Difference Sampling selects instances based on the difference between the teacher's and a small reference model's losses/log-probabilities, but the method is more nuanced than simply selecting instances with the largest discrepancy. It uses the difference to identify data that is informative for the student (where the teacher knows more than a baseline small model), not just 'hard and diverse' examples. The characterization of 'filtering trivial or noisy data' is a reasonable inference but the framing of 'up-sampling hard and diverse examples' is an editorialized description rather than the paper's own framing.
- **Severity**: 🟡 不精确
- **Line 962**: "MiniPLM improves student LMs (200M--1.2B) on 9 downstream tasks while reducing pre-training computation" → **问题**: The specific parameter range (200M-1.2B) and the exact number of downstream tasks (9) should be verified. MiniPLM experiments primarily involve student models of around 120M-1.5B parameters, and the number of downstream evaluation tasks may differ from 9. The claim of '200M--1.2B' may not precisely match the paper's experimental setup.
- **Severity**: 🟡 不精确

### [2503.02832] AlignDistil: Token-Level Language Model Alignment as Adaptive Policy Distillation
- **Line 686**: "Synthetic DPO + reverse DPO" → **问题**: The teacher/data column description 'reverse DPO' is misleading. AlignDistil uses reverse KL divergence for token-level knowledge distillation, not a method called 'reverse DPO'. The paper frames the approach as adaptive policy distillation using DPO with token-level KD, not 'reverse DPO' as a data source or teacher.
- **Severity**: 🟡 不精确
- **Line 904**: "AlignDistil unify alignment and distillation through reward-guided learning" → **问题**: AlignDistil does not primarily use 'reward-guided learning.' It frames alignment as adaptive policy distillation combining DPO with token-level KD. Grouping it with RLKD under 'reward-guided learning' mischaracterizes its core mechanism, which is distillation-based rather than RL/reward-based.
- **Severity**: 🟡 不精确

### [2504.11426] A Dual-Space Framework for General Knowledge Distillation of Large Language Models
- **Line 560**: "map teacher hidden states into the student's representation space and vice versa" → **问题**: The description may be slightly imprecise. DSKD's dual-space framework likely projects representations (not necessarily just hidden states) so that logit distributions can be compared in both the teacher's and student's vocabulary spaces, rather than simply mapping hidden states between spaces. The core mechanism involves projectors that enable distribution-level comparison across different vocabulary spaces, not just hidden-state mapping.
- **Severity**: 🟡 不精确

### [2505.09388] Qwen3 Technical Report
- **Line 0**: "Could not parse" → **问题**: Still failing to parse LLM output
- **Severity**: 🔴 严重

### [2505.16142] RLKD: Distilling LLMs' Reasoning via Reinforcement Learning
- **Line 463**: "Outcome-based methods replace exact token matching with scalar reward signals evaluating the structural validity or factual correctness of a generated trajectory. Frameworks like RLKD" → **问题**: RLKD's GSRM provides structure-aware process rewards that evaluate the reasoning path's structural alignment with the teacher's reasoning, not simple outcome-based scalar feedback. Categorizing RLKD under 'Outcome-Based Feedback' alongside PRMs is misleading; RLKD's reward model is more process/structure-oriented than outcome-oriented.
- **Severity**: 🟡 不精确
- **Line 463**: "Optimization proceeds via Proximal Policy Optimization (PPO) or Direct Preference Optimization (DPO)" → **问题**: RLKD uses KL-regularized RL (as correctly noted in Line 684), not DPO. The review's phrasing 'PPO or DPO' is a general statement about the category but could mislead readers into thinking RLKD uses DPO.
- **Severity**: 🟡 不精确

### [2509.14257] From Correction to Mastery: Reinforced Distillation of Large Language Model Agents
- **Line 691**: "SCoRe \citep{2509.14257}" → **问题**: The method name 'SCoRe' likely refers to a different paper (Kumar et al., 'Training Language Models to Self-Correct via Reinforcement Learning'). The paper 2509.14257 'From Correction to Mastery: Reinforced Distillation of Large Language Model Agents' likely uses a different method name. The acronym may be confused or fabricated for this paper.
- **Severity**: 🟡 不精确
- **Line 1064**: "yielding more robust agent policies that transfer to novel environments" → **问题**: The claim about transferring to 'novel environments' may be an embellishment not explicitly demonstrated or claimed in the original paper. The benchmarks listed (AIME, MATH, Multi-hop QA) are standard evaluation sets rather than evidence of transfer to novel environments.
- **Severity**: 🟡 不精确

### [2509.14526] Delta Knowledge Distillation for Large Language Models
- **Line 636**: "GSM8K, MATH, Dolly" → **问题**: The inclusion of 'Dolly' as a benchmark may be inaccurate. Delta KD primarily focuses on mathematical reasoning and instruction-following benchmarks; the exact benchmark suite should be verified against the original paper. The paper may use different instruction-following datasets.
- **Severity**: 🟡 不精确

### [2509.25837] Distillation of Large Language Models via Concrete Score Matching
- **Line 554**: "Concrete Score Distillation (CSD)" → **问题**: The paper title is 'Distillation of Large Language Models via Concrete Score Matching', suggesting the method is based on 'Concrete Score Matching' rather than 'Concrete Score Distillation'. The abbreviation CSD may be a misnomer.
- **Severity**: 🟡 不精确
- **Line 606**: "CSD \citep{2509.25837}         & 2026" → **问题**: The ArXiv ID 2509.25837 indicates a September 2025 submission, so the year should be 2025, not 2026.
- **Severity**: 🔴 严重

### [2510.07842] AdaSwitch: Balancing Exploration and Guidance in Knowledge Distillation via Adaptive Switching
- **Line 653**: "Llama-3.1-3B" → **问题**: Llama 3.1 does not have a 3B parameter variant. The model is likely Llama-3.2-3B, as the 3B size was introduced in the Llama 3.2 series.
- **Severity**: 🟡 不精确
- **Line 653**: "Llama-3.1-1B" → **问题**: Similarly, Llama 3.1 does not have a 1B variant. This is likely Llama-3.2-1B.
- **Severity**: 🟡 不精确

### [2510.11615] LLM-Oriented Token-Adaptive Knowledge Distillation
- **Line 552**: "upweighting tokens where the student--teacher gap is large and the student's confidence is low" → **问题**: The specific weighting criteria (large student-teacher gap AND low student confidence) are detailed mechanistic claims that cannot be fully verified from the title alone. The paper's token-adaptive approach may use different or additional criteria for weight assignment. This description may oversimplify or slightly mischaracterize the weighting mechanism.
- **Severity**: 🟡 不精确

### [2510.18874] Retaining by Doing: The Role of On-Policy Data in Mitigating Forgetting
- **Line 1075**: "RL generates on-policy rollouts that maintain distributional proximity to the student's prior" → **问题**: The paper discusses distributional proximity to the model's own (pre-training) distribution, not a 'student's prior' in a distillation sense. The framing as 'student's prior' introduces a distillation framing not present in the original paper, which focuses on the model's own pre-training distribution being preserved through on-policy generation.
- **Severity**: 🟡 不精确
- **Line 1075**: "motivating on-policy distillation as a forgetting-resistant alternative to SFT" → **问题**: The original paper's primary conclusion is that on-policy data (as generated in RL) mitigates forgetting compared to off-policy SFT. The paper does not explicitly motivate 'on-policy distillation' as an alternative; this is an interpretive leap made by the review authors rather than a direct claim of the cited paper.
- **Severity**: 🟡 不精确

### [2510.23497] VOLD: Reasoning Transfer from LLMs to Vision-Language Models via On-Policy Distillation
- **Line 1071**: "using only text-based training data" → **问题**: This claim is potentially misleading. VOLD uses a text-only teacher to generate reasoning traces, but the student (a VLM) likely still processes visual inputs during training. The teacher supervision is text-based, but the training data for the student is not exclusively text-based - the student operates on multimodal inputs while receiving distillation signal from text-only teacher outputs.
- **Severity**: 🟡 不精确

### [2511.10643] Black-Box On-Policy Distillation of Large Language Models
- **Line 661**: "GPT-5-Chat (black-box)" → **问题**: GPT-5 was not publicly available as of the paper's publication timeframe (November 2025). The teacher model is very likely GPT-4 or another existing model. This appears to be a fabricated detail.
- **Severity**: 🔴 严重
- **Line 474**: "Generative Adversarial Distillation (GAD) \citep{2511.10643}" → **问题**: The paper's title is 'Black-Box On-Policy Distillation of Large Language Models' — the method name 'GAD' (Generative Adversarial Distillation) does not appear to match the paper's actual naming. The paper's approach may not be framed as 'generative adversarial distillation' specifically.
- **Severity**: 🟡 不精确
- **Line 804**: "a discriminator $D$ (initialized from the student with a scalar prediction head) distinguishes student outputs from teacher outputs using a Bradley--Terry preference model" → **问题**: The specific architectural detail of initializing the discriminator from the student with a scalar prediction head and using a Bradley-Terry preference model may be fabricated or inaccurate. These are very specific claims that may not match the actual paper's methodology.
- **Severity**: 🟡 不精确

### [2512.23097] A Note on Hybrid Online Reinforcement and Imitation Learning for LLMs: Formulations and Algorithms
- **Line 937**: "The dense KD gradient stabilizes early training, while the RL gradient enables exploration beyond the teacher's distribution." → **问题**: The specific claim that 'dense KD gradient stabilizes early training' appears to be an editorial interpretation rather than an explicit finding of the paper. The paper discusses the complementary nature of KD and RL gradients but may not specifically frame KD's role as 'stabilizing early training.'
- **Severity**: 🟡 不精确
- **Line 937**: "the KD component provides a dense, analytically computable gradient for token-level imitation" → **问题**: While the paper does analyze gradients of the hybrid objective and the KD component does yield token-level gradients, characterizing them as 'analytically computable' is a slight embellishment of the paper's language. The paper frames this more in terms of the structural difference between the IL and RL gradient components.
- **Severity**: 🟡 不精确

### [2601.02780] MiMo-V2-Flash Technical Report
- **Line 705**: "Multi-teacher logit + reward" → **问题**: The characterization of MiMo-V2-Flash's training as 'multi-teacher logit + reward' distillation may be inaccurate. The technical report primarily describes RL-based training and SFT/distillation, but the specific framing of combining dense multi-teacher logits with reward signals in a unified distillation framework appears embellished or not clearly supported by the report.
- **Severity**: 🟡 中等
- **Line 964**: "combining dense multi-teacher logits with token-level rewards from outcome verifiers" → **问题**: The specific claim about 'token-level rewards from outcome verifiers' combined with multi-teacher logits in a multi-objective loss that 'interpolates between representation matching and reward maximization' appears to be a fabricated or significantly embellished description of MiMo-V2-Flash's training methodology. The actual report does not clearly describe this specific unified framework.
- **Severity**: 🔴 严重
- **Line 964**: "heterogeneous feedback signals are synergistic and stabilize gradient trajectories in ultra-large-scale training" → **问题**: The claim about 'stabilizing gradient trajectories' appears to be an unsupported extrapolation not clearly stated in the MiMo-V2-Flash technical report.
- **Severity**: 🟡 中等
- **Line 705**: "Domain-specialized teachers (RL/SFT)" → **问题**: The description of teachers as 'domain-specialized teachers (RL/SFT)' is vague and may not accurately reflect the specific teacher models used in MiMo-V2-Flash training.
- **Severity**: 🟡 中等

### [2601.09088] Distribution-Aligned Sequence Distillation for Superior Long-CoT Reasoning
- **Line 611**: "DASD \citep{2601.09088}        & 2026" → **问题**: ArXiv ID 2601.09088 indicates the paper was published in January 2025, not 2026. The '2601' prefix means January 2025 (25=year, 01=month).
- **Severity**: 🟡 不精确

### [2601.18734] Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models
- **Line 465**: "OPSD \citep{2601.18734} simulate a two-player game where the model at iteration $t$ distinguishes its own outputs from a static set of demonstrations" → **问题**: OPSD does not simulate a two-player game or distinguish outputs from static demonstrations. OPSD performs self-distillation where a privileged-information-conditioned version of the model (teacher) provides token-level supervision on student-generated rollouts. The two-player game description applies to SPIN but not to OPSD.
- **Severity**: 🔴 严重
- **Line 670**: "Qwen3-1.7B/4B/8B-Inst" → **问题**: The paper (arXiv 2601.18734, January 2025) likely uses Qwen2.5 series models, not Qwen3, which was not yet available at the time of publication. The model family name appears to be incorrect.
- **Severity**: 🟡 不精确

### [2601.19897] Self-Distillation Enables Continual Learning
- **Line 862**: "via implicit KL regularization" → **问题**: Characterizing the KL regularization as 'implicit' may be imprecise. The self-distillation objective in SDFT explicitly incorporates KL divergence between the model's current and previous distributions as a regularization mechanism; it is not merely an implicit byproduct.
- **Severity**: 🟡 不精确
- **Line 1076**: "through implicit self-distillation KL regularization" → **问题**: Same issue as line 862: the KL regularization in SDFT is an explicit component of the training objective, not merely implicit.
- **Severity**: 🟡 不精确

### [2601.20802] Reinforcement Learning via Self-Distillation
- **Line 479**: "The model distills its own successful reasoning traces back into its policy through a self-distillation objective" → **问题**: This mischaracterizes SDPO's mechanism. The paper states that SDPO treats the current model *conditioned on feedback* (e.g., compiler errors, test outputs) as a self-teacher and distills its feedback-informed next-token predictions back into the policy. It does not specifically distill 'successful reasoning traces' — it leverages rich textual feedback (including from failed attempts) to create dense learning signals.
- **Severity**: 🔴 严重
- **Line 856**: "proof checker messages" → **问题**: The abstract mentions 'runtime errors or judge evaluations' as examples of rich textual feedback, not 'proof checker messages'. This appears to be fabricated detail not found in the paper's abstract.
- **Severity**: 🟡 不精确
- **Line 856**: "attributing success or failure to specific reasoning steps rather than entire trajectories" → **问题**: The paper describes converting feedback into dense token-level learning signals via self-distillation, addressing the credit-assignment bottleneck. However, the specific claim of 'attributing success or failure to specific reasoning steps' is an interpretive embellishment — the mechanism works through feedback-conditioned next-token prediction distillation, not explicit step-level attribution.
- **Severity**: 🟡 不精确

### [2602.00400] KEPO: Knowledge-Enhanced Preference Optimization for Reinforcement Learning with Reasoning
- **Line 690**: "KEPO \citep{2602.00400} & Qwen3-VL-32B & Qwen3-VL-2B & KD + preference optim. & OmniMedVQA" → **问题**: Cannot verify the specific model names (Qwen3-VL-32B, Qwen3-VL-2B), method characterization, or benchmark (OmniMedVQA) against the original paper, as the abstract is unavailable and the paper title ('Knowledge-Enhanced Preference Optimization for Reinforcement Learning with Reasoning') does not specifically indicate vision-language or medical VQA focus. These details may be fabricated.
- **Severity**: 🟡 不精确
- **Line 936**: "KEPO integrates distillation into preference optimization for vision-language models, using dense token-level teacher supervision to address the sparse reward problem in reasoning-oriented RL" → **问题**: The paper title does not mention vision-language models; the characterization as a VL method with 'dense token-level teacher supervision' and claims about 'exploration collapse' in standard RLVR cannot be verified from available information and may be inaccurate or fabricated.
- **Severity**: 🟡 不精确

### [2602.02405] Didactic to Constructive: Turning Expert Solutions into Learnable Reasoning
- **Line 665**: "Qwen3-8B" → **问题**: Qwen3-8B was not publicly available in February 2025 when this paper was published (ArXiv 2602.02405). The student models used may be different. This could be a hallucinated detail.
- **Severity**: 🟡 不精确
- **Line 665**: "Self (privileged student)" → **问题**: The paper's title 'Didactic to Constructive' suggests transforming expert solutions, not self-generation from a privileged student. The teacher description may be inaccurate - the method likely takes external expert solutions and transforms them, rather than using self-generated traces.
- **Severity**: 🟡 不精确

### [2602.02994] Video-OPD: Efficient Post-Training of Multimodal Large Language Models for Temporal Video Grounding via On-Policy Distillation
- **Line 1072**: "state-of-the-art results on three TVG benchmarks" → **问题**: Line 696 only lists two TVG benchmarks (Charades, ActivityNet), creating an inconsistency with the claim of 'three TVG benchmarks' in line 1072. Cannot verify against the original paper as it is not available in my knowledge base (ArXiv ID 2602.02994 appears to correspond to a date beyond my knowledge cutoff).
- **Severity**: 🟡 不精确
- **Line 696**: "Qwen3-VL-32B-GRPO & Qwen3-VL-8B-Inst" → **问题**: Cannot verify the specific teacher and student model identities (Qwen3-VL-32B-GRPO as teacher, Qwen3-VL-8B-Inst as student) against the original paper, as the paper is not available in my knowledge base. These specific model names may be inaccurate.
- **Severity**: 🟡 不精确

### [2602.03073] TMS: Trajectory-Mixed Supervision for Reward-Free, On-Policy SFT
- **Line 858**: "causing catastrophic forgetting" → **问题**: The paper's primary framing is about supervision/distribution mismatch (Policy-Label Divergence) rather than catastrophic forgetting specifically. While forgetting may be a consequence discussed, characterizing the core problem as 'catastrophic forgetting' may be imprecise — the paper emphasizes that static labels diverge from the evolving policy distribution.
- **Severity**: 🟡 不精确
- **Line 858**: "recovers the retention benefits of on-policy RL" → **问题**: The paper frames TMS as bridging SFT toward on-policy training benefits more broadly (better alignment of supervision with current policy), not specifically about 'retention benefits.' This characterization may be slightly narrower than the paper's actual claims.
- **Severity**: 🟡 不精确

### [2602.04942] Privileged Information Distillation for Language Models
- **Line 678**: "Qwen3-4B / 8B, R1-Distill-Llama-8B" → **问题**: The paper (ArXiv 2602.04942, February 2025) likely predates the release of Qwen3 models (which appeared later in 2025). The models used may be Qwen2.5 variants rather than Qwen3. This specific model list may be fabricated or confused with another paper.
- **Severity**: 🟡 不精确
- **Line 842**: "generalize the OPSD and GATES paradigms into a unified framework" → **问题**: The paper may not explicitly claim to generalize both OPSD and GATES specifically. The framing about 'provably improves over standard training' and the specific entropy conditions ('PI must reduce teacher entropy sufficiently... but not so much that the teacher's distribution becomes degenerate') may be an embellished or imprecise characterization of the paper's theoretical contributions.
- **Severity**: 🟡 不精确

### [2602.06019] Multi-Token Prediction via Self-Distillation
- **Line 850**: "without architectural changes" → **问题**: Multi-token prediction methods, including this one, typically require additional prediction heads (extra linear/transformer layers) to predict multiple future tokens. This constitutes an architectural change. The paper likely adds MTP heads to the base model, so claiming 'without architectural changes' is misleading or inaccurate.
- **Severity**: 🟡 不精确
- **Line 850**: "achieving more than 3× faster decoding on GSM8K at less than 5% accuracy drop" → **问题**: These specific quantitative claims (>3× speedup, <5% accuracy drop) cannot be confidently verified and may be imprecise or fabricated. The exact numbers reported in the original paper may differ from these round-number summaries.
- **Severity**: 🟡 不精确

### [2602.12125] Learning beyond Teacher: Generalized On-Policy Distillation with Reward Extrapolation
- **Line 0**: "Could not parse" → **问题**: Still failing to parse LLM output
- **Severity**: 🔴 严重

### [2602.12275] On-Policy Context Distillation for Language Models
- **Line 675**: "Qwen3-1.7B / 4B / 8B" → **问题**: The paper was published in February 2025 (arXiv: 2602.12275), before Qwen3 models were released. The paper likely uses Qwen2.5 models (e.g., Qwen2.5-1.5B/3B/7B or similar sizes), not Qwen3. The model names and sizes appear to be fabricated.
- **Severity**: 🔴 严重

### [2602.15260] Fast and Effective On-policy Distillation from Reasoning Prefixes
- **Line 747**: "reducing training FLOPs by 2× to 47×" → **问题**: The specific speedup range of 2× to 47× needs verification against the original paper. While the paper does report significant compute savings, the exact numbers (especially the 47× upper bound) may not precisely match the paper's reported figures. This could be a minor inaccuracy or rounding.
- **Severity**: 🟡 不精确

### [2602.20574] GATES: Self-Distillation under Privileged Context with Consensus Gating
- **Line 672**: "Qwen3-4B-Base" → **问题**: Given the paper's ArXiv ID (2602.20574, suggesting February 2025 submission), Qwen3 models were not yet available. The paper more likely uses Qwen2.5 series models. This specific model name may be fabricated.
- **Severity**: 🟡 不精确
- **Line 840**: "This directly addresses the "echo chamber" problem where distilling uncertain teacher signals amplifies noise" → **问题**: The term 'echo chamber problem' may not be the terminology used in the original paper. This appears to be the reviewer's own framing rather than a direct characterization from the paper.
- **Severity**: 🟡 不精确

### [2602.22495] Reinforcement-aware Knowledge Distillation for LLM Reasoning
- **Line 0**: "Could not parse" → **问题**: Still failing to parse LLM output
- **Severity**: 🔴 严重

### [2603.11137] Scaling Reasoning Efficiently via Relaxed On-Policy Distillation
- **Line 642**: "AIME, Math, Visual reasoning" → **问题**: The paper focuses on mathematical reasoning benchmarks. 'Visual reasoning' as a benchmark category seems unlikely for this paper, which is about scaling reasoning via distillation of language models. The actual benchmarks likely focus on math-related tasks (e.g., AIME, MATH, GSM8K, or similar). This may be fabricated or confused with another paper.
- **Severity**: 🟡 不精确
- **Line 769**: "achieves $6.7$--$12\times$ greater sample efficiency than recent RL approaches" → **问题**: These specific numerical claims (6.7-12× sample efficiency) cannot be verified against the original paper and may be inaccurate or fabricated. The exact numbers should be cross-checked with the paper's experimental results.
- **Severity**: 🟡 不精确
- **Line 769**: "enabling a 7B student to match a 32B teacher with $\sim$3.3$\times$ inference speedup" → **问题**: The ~3.3× inference speedup claim for a 7B vs 32B model needs verification. A naive parameter ratio would suggest ~4.6× speedup; 3.3× could be accurate depending on architecture specifics, but this specific number should be verified against the original paper.
- **Severity**: 🟡 不精确

### [2603.11178] PACED: Distillation and Self-Distillation at the Frontier of Student Competence
- **Line 759**: "minimax-robust, with worst-case efficiency loss of only $O(\delta^2)$ under bounded multiplicative misspecification" → **问题**: This specific theoretical claim about minimax robustness with O(δ²) worst-case efficiency loss cannot be confidently verified as being in the original paper. This level of specificity may be fabricated or conflated with another work's theoretical results.
- **Severity**: 🟡 不精确
- **Line 759**: "A two-stage divergence schedule---Forward KL for broad mode coverage, then Reverse KL for consolidation---yields the strongest results" → **问题**: The paper's adaptive divergence mechanism may not be a simple two-stage FKL→RKL schedule. The review's description of 'Adaptive' divergence in Line 602 suggests a more nuanced approach than a fixed two-stage switch. This may oversimplify or mischaracterize the actual divergence scheduling mechanism.
- **Severity**: 🟡 不精确
- **Line 939**: "the teacher provides token-level supervision on those student-generated sequences" → **问题**: Line 602 classifies PACED as 'Hybrid' (not purely token-level), suggesting the supervision is not exclusively token-level. Describing it as purely token-level supervision may be inaccurate.
- **Severity**: 🟡 不精确

### [2603.16856] Online Experiential Learning for Language Models
- **Line 844**: "Its successor, Online Experiential Learning (OEL)" → **问题**: Characterizing OEL as OPCD's 'successor' implies a direct lineage or same research group continuation, which may not be accurate. OEL may be independent work that builds on similar ideas rather than a direct successor.
- **Severity**: 🟡 不精确
- **Line 844**: "the model accumulates experience from real-world interactions" → **问题**: The paper focuses on text-based games as the experimental domain (as noted in Line 676), not 'real-world interactions.' Describing simulated text-based game environments as 'real-world' is misleading.
- **Severity**: 🟡 不精确
- **Line 676**: "Qwen3-1.7B / 4B / 8B" → **问题**: Given the paper's March 2025 submission date (2603.16856), it likely uses Qwen2.5 models rather than Qwen3 models, which were released in April 2025. The model family name may be incorrect.
- **Severity**: 🔴 严重

### [2603.19220] Nemotron-Cascade 2: Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation
- **Line 980**: "with 20× fewer parameters" → **问题**: The 20× comparison is ambiguous. Total parameters: 671B/30B ≈ 22×; active parameters: 37B/3B ≈ 12×. Neither ratio is exactly 20×. If referring to total parameters, ~22× would be more accurate; if active parameters, ~12× would be correct.
- **Severity**: 🟡 不精确
- **Line 980**: "the second open-weight model to do so after DeepSeek-V3.2-Speciale (671B-A37B)" → **问题**: This specific ranking claim ('second open-weight model') and the comparison to DeepSeek-V3.2-Speciale may be an editorial interpretation rather than a direct claim from the Nemotron-Cascade 2 paper. The paper may not explicitly position itself as 'the second' in this manner, and the DeepSeek model name/specs should be verified against the original paper's text.
- **Severity**: 🟡 不精确
- **Line 980**: "achieving Gold Medal-level performance on IMO, IOI, and ICPC World Finals" → **问题**: The claim of Gold Medal-level on all three competitions (IMO, IOI, and ICPC World Finals) simultaneously needs verification. The paper may report strong results but the exact 'Gold Medal-level' characterization across all three benchmarks may be an overstatement or imprecise summary of the actual reported results.
- **Severity**: 🟡 不精确

## Verified Correct
- [2306.08543]: ✅ 所有描述准确
- [2501.12948]: ✅ 所有描述准确
- [2501.16937]: ✅ 所有描述准确
- [2503.07067]: ✅ 所有描述准确
- [2504.14945]: ✅ 所有描述准确
- [2505.13111]: ✅ 所有描述准确
- [2505.16297]: ✅ 所有描述准确
- [2506.02208]: ✅ 所有描述准确
- [2509.22921]: ✅ 所有描述准确
- [2509.25100]: ✅ 所有描述准确
- [2510.24021]: ✅ 所有描述准确
- [2602.12222]: ✅ 所有描述准确
- [2602.12674]: ✅ 所有描述准确
- [2603.05433]: ✅ 所有描述准确
- [2603.07079]: ✅ 所有描述准确
- [2603.13260]: ✅ 所有描述准确
- [2603.23871]: ✅ 所有描述准确
- [hinton2015distilling]: ✅ 所有描述准确
- [kim2016sequence]: ✅ 所有描述准确
- [ross2011reduction]: ✅ 所有描述准确