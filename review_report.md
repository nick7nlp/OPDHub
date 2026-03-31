# Peer Review Report: "Who Decides the Training Distribution? A Survey of On-Policy Distillation for Large Language Models"

## Reviewer 1: Senior Knowledge Distillation (KD) Researcher

### Summary
This survey provides a comprehensive and theoretically grounded overview of On-Policy Distillation (OPD) for Large Language Models. It successfully unifies disparate recent works under a common mathematical framework of sequential decision-making and f-divergence minimization, categorizing the literature based on feedback signal, teacher access, and granularity. The paper highlights the critical shift from static dataset matching to dynamic student-driven trajectory alignment.

### Strengths
1.  **Strong Theoretical Foundation:** The unification of various OPD methods (GKD, MiniLLM, DistiLLM) under a generalized f-divergence and sampling policy framework (Section 2.5) is elegant and provides much-needed mathematical clarity to a fragmented field.
2.  **Insightful Geometric Analysis:** The discussion going beyond the simple mode-seeking/mean-seeking dichotomy to geometric paths in the probability simplex (Section 4.4) offers deep insights into why adaptive divergences work best.
3.  **Comprehensive Taxonomy:** The proposed taxonomy based on feedback signal, teacher access, and granularity is highly logical and structurally sound, making it easy to navigate the fast-growing literature.
4.  **Timely and Relevant:** The survey perfectly captures the current paradigm shift in LLM post-training, especially highlighting the critical role of OPD in reasoning distillation post-DeepSeek-R1.

### Weaknesses
1.  **Over-Claiming Novelty of Exposure Bias:** The concept of exposure bias and its mitigation via on-policy rollouts (DAgger) has been well-known in sequence-to-sequence learning and RL for NLP long before LLMs. While the paper acknowledges ImitKD, it sometimes presents the shift to OPD in LLMs as a more profound theoretical leap than it is; it's largely an application of existing IL/RL principles at a larger scale.
2.  **Missing Discussion on Teacher Capacity/Quality:** A critical aspect of KD is the teacher's capability. The survey lacks an in-depth discussion on how teacher quality, size, and calibration affect OPD. What happens when the teacher is poorly calibrated or only marginally better than the student? 
3.  **Light on Multimodal/Cross-Modal Distillation:** While Section 6.6 briefly touches on multimodal OPD (VOLD, Video-OPD), this area feels underdeveloped given its rising importance. The complexities of cross-modal alignment in an on-policy setting deserve more depth.
4.  **Redundancy in Method Descriptions:** Section 4 sometimes reads like a sequential list of paper summaries rather than a synthesized narrative. Comparing methods directly against the unified framework established in Section 2.5 earlier in the text would improve flow.

### Questions for Authors
1.  Could you elaborate on the theoretical limits of OPD when the capacity gap between the teacher and student is extremely large (e.g., 671B MoE to 1.5B dense)? At what point does the student's representation space fail to capture the teacher's divergence signals?
2.  How do you mathematically reconcile the conflicting goals of exploring novel reasoning paths (RL reward maximization) and strictly matching teacher logits (KL penalty) in the hybrid KD+RL frameworks?

### Missing References
- Consider including foundational IL works beyond DAgger, such as SEARN (Daumé et al., 2006) or Scheduled Sampling (Bengio et al., 2015), to better contextualize the historical roots of addressing exposure bias in sequence generation.
- Relevant work on the calibration of LLM teachers and how it impacts distillation targets.

### Minor Issues
- Figure 3: The notation in the bottom equation ($\beta \cdot D_{\mathrm{KL}}(p_\theta \| p_T)$) slightly conflicts with the text which often uses $p_S$ for student. Ensure consistency.
- Section 4.1: The transition between different divergence methods could use stronger connective tissue to show the evolutionary necessity of each.

### Overall Score & Confidence
**Score:** 8/10 (Accept)
**Confidence:** 5/5 (Expert in the field)

---

## Reviewer 2: ML Systems and Engineering Perspective

### Summary
This paper surveys On-Policy Distillation, emphasizing the shift towards student-driven data generation to mitigate exposure bias. From a systems perspective, the survey is valuable for its discussion of the compute-quality tradeoff and large-scale deployment challenges, providing concrete frameworks for understanding the cost of on-policy versus off-policy methods.

### Strengths
1.  **Practical Cost Analysis:** Section 7.3 provides a highly appreciated, concrete formalization of the compute-quality tradeoff, breaking down FLOPs for on-policy vs. off-policy distillation. The concrete cost example (70B teacher to 7B student) grounds the theory in reality.
2.  **Systems-Level Innovations:** The coverage of Speculative KD, DistillSpec, and efficiency innovations (Section 7.2) directly addresses the primary bottleneck of OPD (teacher inference cost).
3.  **Actionable Guidelines:** Section 8.9 offers excellent, pragmatic decision frameworks for engineering teams trying to select a distillation strategy based on compute budget and model size.
4.  **Rich Tabular Summaries:** Table 1 and Table 2 are highly informative, particularly Table 2's compilation of experimental configurations (model sizes, tasks), which is crucial for practitioners.

### Weaknesses
1.  **Memory Overhead Ignored:** While FLOPs and compute time are analyzed, the survey largely ignores the severe GPU memory overhead of white-box OPD. Maintaining a 70B teacher's weights, activations, and full logits in memory alongside the student is the primary blocker for most practitioners. This systems constraint needs detailed discussion.
2.  **Communication Overheads:** In large-scale distributed training (e.g., ensemble OPD mentioned in 7.1), the communication overhead of moving logits across nodes is massive. The paper misses an opportunity to discuss systems optimizations for logit communication or quantization during distillation.
3.  **Table 2 Readability:** Table 2 is very dense. While informative, categorizing it further or adding a column for "Compute Overhead (Relative to SFT)" would make it much more actionable for systems engineers.
4.  **Serving Infrastructure:** The paper touches on inference acceleration (MTP), but lacks discussion on how the *training* infrastructure needs to be modified to support synchronous or asynchronous teacher scoring.

### Questions for Authors
1.  How do memory constraints impact the choice between token-level (white-box) and sequence-level (black-box/RL) OPD in practice? Are there specific systems optimizations (e.g., logit offloading) that are standard in the industry for white-box methods?
2.  In the compute-quality tradeoff (Section 7.3), how does the batch size impact the relative cost of $C_{on}$ vs $C_{off}$, given that generative inference scales differently with batch size than standard forward passes?

### Missing References
- System-level papers on efficient logit serving and distributed distillation frameworks (e.g., works related to Megatron-LM or DeepSpeed's distillation pipelines).

### Minor Issues
- Section 7.3: The variables $F, B, G$ are introduced but not explicitly defined with their full terms (e.g., Forward, Backward, Generation) in the text immediately preceding the equation, though it's inferable.
- Typo in Section 7.2: "Minitron (2407.14679)" - ensure the citation format matches the rest of the text.

### Overall Score & Confidence
**Score:** 7/10 (Weak Accept)
**Confidence:** 4/5 (Knowledgeable in systems for ML)

---

## Reviewer 3: Theoretical and Statistical Learning Perspective

### Summary
The authors present a survey of On-Policy Distillation, framing it through the lens of imitation learning, f-divergence minimization, and reinforcement learning. The paper successfully formalizes the transition from static dataset matching to dynamic policy alignment and discusses the theoretical implications of different divergence choices on model behavior.

### Strengths
1.  **Rigorous Formalization:** The mathematical treatment in Section 2, particularly the derivation linking classical KD to MSE in the high-temperature limit and the REINFORCE derivation for MiniLLM, is sound and well-presented.
2.  **Exposure Bias Connection:** Explicitly linking exposure bias to the $O(T^2)$ compounding error bound from DAgger (Ross et al., 2011) provides a strong theoretical justification for why OPD is necessary for long-horizon generation.
3.  **Insightful Open Problems:** The discussion on uncertainty-aware OPD (Section 8.2) and the formulation of a dynamic curriculum based on adaptive divergence (Section 8.3) are theoretically interesting and point to valuable future research directions.
4.  **Analysis of Mode Collapse:** The analysis of why self-play saturates (Section 5.3) mathematically connecting it to GAN mode collapse is a very strong theoretical observation.

### Weaknesses
1.  **DAgger Bound Nuance:** The paper quotes the $O(\epsilon T^2)$ bound for off-policy learning and implies OPD perfectly resolves this to $O(\epsilon T)$. However, standard DAgger requires an *interactive* expert that can provide the optimal action in the states visited by the student. In LLM distillation, the teacher often provides merely a distribution over the *next token* given the student's prefix, which may already be out-of-distribution for the teacher itself. The theoretical implications of querying the teacher in states where the teacher's own policy has low support are not fully explored.
2.  **Convergence Guarantees:** The paper touches on the convergence of SPIN, but lacks a broader discussion on the convergence properties of token-level white-box methods. Under what conditions do adaptive divergence methods (like ToDi or AKL) theoretically converge to the global optimum of the teacher's distribution?
3.  **Simplification of KL Constraints:** In Section 6.2 (Reward-Guided OPD), the KL penalty is treated as a simple regularizer. From a theoretical RL perspective, trust-region methods bounds are much more complex. The connection to TRPO/PPO theoretical bounds in the context of sequence generation could be deeper.
4.  **Equation 22 (Scaling Law):** Proposing a scaling law equation with arbitrary additive terms ($E + A/N_S^\alpha + ...$) without theoretical justification for why the terms should be additive rather than multiplicative (or interacting in more complex ways) is weak.

### Questions for Authors
1.  Regarding the DAgger bound: When the student generates a highly hallucinated prefix, the teacher's next-token distribution $P_T(y_t | \hat{y}_{<t})$ might be essentially noise. Does this violate the core assumption of interactive imitation learning, and how does it theoretically impact the $O(\epsilon T)$ bound?
2.  In the formulation of the Distillation-RL Virtuous Loop (Section 8.7), you propose an alternating projection. Can you provide any preliminary theoretical intuition on whether this operator is a contraction, given the highly non-convex nature of LLM parameter spaces?

### Missing References
- Theoretical works on the limits of Imitation Learning when the expert is suboptimal or queried out-of-distribution.
- More rigorous RL theory papers discussing the exact bounds of KL-regularized MDPs.

### Minor Issues
- Section 2.4: The definition of Total Variation Distance is stated, but its specific theoretical limitations for neural network optimization (non-differentiability) could be elaborated further in relation to the other divergences.
- Equation 15: Double check the signs in the min-max formulation for GAD to ensure it aligns perfectly with standard GAN notation conventions.

### Overall Score & Confidence
**Score:** 7/10 (Weak Accept)
**Confidence:** 5/5 (Expert in theoretical ML)
