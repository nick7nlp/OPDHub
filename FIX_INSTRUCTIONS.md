# Citation Fix Instructions

## Overview
The main.tex has 15 citation IDs that point to WRONG papers on arXiv. 
Each needs to be fixed: replace the wrong ID in both main.tex AND references.bib.

## Definitive Fixes (ID replacement)

### 1. Llama 2: 2307.15190 → 2307.09288
- In tex: `\citet{2307.15190}` is used for "Llama 2" reference (Section 2.4, nowhere else directly)
- BUT 2307.15190 is actually "f-Divergence Minimization for Sequence-Level KD" by Wen et al.
- The tex ALSO cites 2307.15190 via `\citet{2307.15190}` in Section 4.4 for "unified f-divergence"
- FIX: Replace `2307.15190` with `2307.09288` ONLY where Llama 2 is intended
- For the f-divergence reference, 2307.15190 IS correct (it's the actual paper)
- So we need to ADD 2307.09288 as a new key for Llama 2, and keep 2307.15190 for f-div

Actually, checking more carefully: 2307.15190 is cited as `\citet{2307.15190}` in Section 4.4 only ("proposed a Unified f-divergence perspective"). The Llama 2 reference doesn't appear to be cited anywhere in the current tex! So just fix the bib entry to match the actual paper.

WAIT - the bib entry for 2307.15190 has title "Llama 2" which is WRONG. The correct title for 2307.15190 is "f-Divergence Minimization for Sequence-Level Knowledge Distillation". Fix the bib entry.

### 2. Lion: 2310.01382 → 2305.12870
- In tex: "Lion \citep{2310.01382}" appears in Section 3.1 and Section 5.1
- 2310.01382 is actually "Compressing LLMs: The Truth is Rarely Pure"
- Lion correct ID: 2305.12870
- FIX: Replace ALL occurrences of `2310.01382` with `2305.12870` in both tex and bib

### 3. Zephyr: 2310.06694 → 2310.16944
- In tex: "Zephyr \citep{2310.06694}" appears in Sections 5.1 and 3.2
- 2310.06694 is actually "Sheared LLaMA"
- Zephyr correct ID: 2310.16944
- FIX: Replace ALL occurrences of `2310.06694` with `2310.16944` in both tex and bib

### 4. Minitron: 2311.09829 → 2407.14679
- In tex: "Minitron \citep{2311.09829}" in Section 6.2
- 2311.09829 is actually "FollowEval"
- Minitron correct ID: 2407.14679
- FIX: Replace ALL occurrences of `2311.09829` with `2407.14679`

### 5. Gemma 2: 2406.06608 → 2408.00118
- In tex: "Gemma 2 \citep{2406.06608}" in Section 6.1
- 2406.06608 is actually "The Prompt Report"
- Gemma 2 correct ID: 2408.00118
- FIX: Replace ALL occurrences of `2406.06608` with `2408.00118`

### 6. DSKD: 2502.12018 → 2504.11426
- In tex: "DSKD \citep{2502.12018}" in Sections 3.1 (taxonomy), 4.1
- 2502.12018 is actually "Atom of Thoughts"
- DSKD correct ID: 2504.11426 (or earlier version)
- FIX: Replace ALL occurrences of `2502.12018` with `2504.11426`

### 7. AKL: 2410.14425 → use 2404.02657
- In tex: "AKL \citep{2410.14425}" in Section 4.1
- 2410.14425 is actually "Unlearning Backdoor Attacks"
- AKL is from the paper "Rethinking Kullback-Leibler Divergence in KD" = 2404.02657
- BUT 2404.02657 is ALSO cited separately for "unified f-divergence perspective" in Section 4.4
- FIX: Replace `2410.14425` with `2404.02657` (they're the same paper - AKL IS the "Rethinking KL" paper)

### 8. 2503.04711 → REMOVE
- In tex: cited as "reward-aware OPD frameworks \citep{2503.04711}"
- 2503.04711 is actually a PHYSICS paper about semiconductor nonlinearity!
- FIX: Remove this citation entirely from the tex. Remove from bib.

## Uncertain Fixes (need search or removal)

### 9. 2402.00857 → REMOVE or find correct paper
- In tex: cited for "CoT reasoning distillation \citep{2402.00857, 2405.04434}"
- 2402.00857 is "Early Time Classification" - completely unrelated
- FIX: Remove this citation. The surrounding text still makes sense without it.

### 10. 2405.04434 → REMOVE or find correct paper
- In tex: cited for "CoT reasoning distillation \citep{2402.00857, 2405.04434}"
- 2405.04434 is "DeepSeek-V2" - not about reasoning distillation specifically
- FIX: Remove this citation or replace with a real reasoning distillation paper.

### 11. 2403.14608 → REMOVE or find correct paper
- In tex: cited for "Contrastive On-Policy Distillation \citet{2403.14608}"
- 2403.14608 is "Parameter-Efficient Fine-Tuning Survey" - unrelated
- The "Contrastive On-Policy Distillation" concept is described in the tex but the cited paper doesn't exist
- FIX: This section describes a conceptual method. Remove the specific citation or note it as a proposed direction.

### 12. 2408.06037 → REMOVE or find correct paper  
- In tex: cited as "DistillReasoner \citep{2408.06037}" in Section 6.2
- 2408.06037 is "Hyperion: Unveiling DApp" - completely unrelated
- FIX: Remove this citation. 

### 13. 2310.13332 → Keep as "Democratizing Reasoning Ability"
- In tex: cited alongside 2402.12030 for "cross-tokenizer distillation \citep{2402.12030, 2310.13332}"
- 2310.13332 is "Democratizing Reasoning Ability" - not about cross-tokenizer
- FIX: Remove 2310.13332 from the cross-tokenizer citation. If it's cited nowhere else, remove from bib.

### 14. 2510.24021 → Keep as "SelecTKD" or replace
- In tex: cited alongside 2410.11325 for "Speculative KD \citep{2410.11325, 2510.24021}"
- 2510.24021 is "SelecTKD: Selective Token-Weighted KD" - related but not speculative KD
- FIX: Remove from the speculative KD citation if misleading, or keep if it's a valid secondary reference.

### 15. 2402.12030 (Gemma reference)
- In tex: cited both as cross-tokenizer distillation (correct) AND as Gemma in some places
- 2402.12030 IS "Cross-Tokenizer Distillation" - correct for that use
- BUT if any tex line says "Gemma \citep{2402.12030}", that's wrong. Gemma = 2403.08295
- FIX: Check all uses of 2402.12030 in tex. If used for "Gemma", add 2403.08295 for Gemma instead.

## After Fixing
1. Rebuild references.bib with correct metadata from references_corrected.bib
2. For new IDs (2307.09288, 2305.12870, 2310.16944, etc.), fetch correct bib from arXiv
3. Compile: pdflatex + bibtex + pdflatex + pdflatex
4. Verify 0 warnings
