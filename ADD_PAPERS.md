# Task: Integrate 7 new papers into main.tex

All bib entries are already in references.bib. You need to add citations and discussion in the appropriate sections of main.tex.

## New papers to integrate:

### 1. ImitKD \citep{2009.07253} — Section 2 or early Section 4
ImitKD (Lin et al., 2020) is the FIRST on-policy knowledge distillation method for autoregressive models. It uses imitation learning to address exposure bias: the student generates tokens, and the teacher provides supervision on those student-generated sequences. It is a direct precursor to GKD.
WHERE: In Section 2 (Background) when discussing the evolution from off-policy to on-policy, or in the beginning of Section 4 (White-Box methods) as a historical precursor to GKD. Also mention in the Related Work aspect.

### 2. AdaSwitch \citep{2510.07842} — Section 4.1 (Token-Level)
AdaSwitch (Peng et al., 2025) adaptively switches between off-policy teacher guidance and on-policy student exploration during training. It detects whether the student is generating high-quality tokens (explore further) or deviating (switch to teacher guidance). This is a direct hybrid on/off-policy method.
WHERE: In Section 4.1 after describing GKD/DistiLLM, as an important hybrid approach. Also add a row to Table 1.

### 3. DistiLLM-2 \citep{2503.07067} — Section 4.1 (Token-Level)
DistiLLM-2 (Ko et al., 2025, ICML 2025) introduces contrastive distillation: it simultaneously increases the likelihood of teacher responses while decreasing that of student responses. It applies different loss functions to teacher-generated vs student-generated data.
WHERE: In Section 4.1 after DistiLLM as its successor. Add a row to Table 1.

### 4. LUFFY \citep{2504.14945} — Section 6 (Reasoning) 
LUFFY (Yan et al., 2025, NeurIPS 2025) = "Learning to reason under off-policy guidance". It combines on-policy RL with off-policy teacher traces, dynamically balancing when to imitate teacher reasoning and when to explore independently. Uses an importance weighting scheme.
WHERE: In Section 6.2 (Reward-Guided OPD) or after DeepSeek-R1 section, as a method that bridges the on-policy/off-policy gap for reasoning.

### 5. MiniPLM \citep{2410.17215} — Section 7 (Systems) or Section 2
MiniPLM (Gu et al., 2024, ICLR 2025) applies KD during pre-training (not fine-tuning). It generates training data offline based on difficulty measured by the teacher, avoiding the cost of online teacher inference.
WHERE: Brief mention in Section 7 (Systems/Scaling) as an example of KD applied at the pre-training stage.

### 6. DistillSpec \citep{2310.08461} — Section 7.1 (Efficiency)
DistillSpec (Zhou et al., 2023, ICLR 2024) uses knowledge distillation to align a draft model with a target model for speculative decoding. This is closely related to Speculative KD already discussed.
WHERE: In Section 7.1 alongside Speculative KD \citep{2410.11325}. They are complementary: SpecKD uses speculative decoding to speed up distillation training; DistillSpec uses distillation to improve speculative decoding at inference.

### 7. VOLD \citep{2510.23497} — Section 8 (Future) or Section 6
VOLD (Bousselham et al., 2025) extends on-policy distillation to vision-language models, transferring reasoning from text-only LLMs to VLMs. Uses RL + KD.
WHERE: Brief mention in Section 8 (Future Directions) under multimodal extensions, or in Section 6.

## Instructions
- Read each paper's PDF from the pdfs/ directory to get the key ideas right
- Add 2-4 sentences per paper in the appropriate location
- Add rows to Table 1 for AdaSwitch and DistiLLM-2 
- Keep the writing style consistent with the rest of the paper (clear, direct, no AI-sounding language)
- After editing: pdflatex + bibtex + pdflatex × 2
- Verify 0 bibtex warnings
