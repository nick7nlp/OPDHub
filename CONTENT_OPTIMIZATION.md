# Content Optimization Task for On-Policy Distillation Survey

## File: main.tex (current: 27 pages, 44 citations, compiles clean)

## What Has Been Done
- All arXiv IDs verified and corrected
- 15 wrong citation IDs fixed
- 7 non-existent/wrong citations removed
- BibTeX entries now have correct titles and authors from arXiv API
- Compiles with 0 errors, 0 bibtex warnings

## What Needs Optimization

### Priority 1: Writing Quality (reduce verbosity)
The writing is overly verbose with excessive adjectives ("rigorous", "exhaustive", "paramount", "profoundly", "catastrophic"). 

Specific patterns to fix:
- Remove filler phrases like "It is crucial to note that", "We posit the following", "From a rigorous theoretical standpoint"
- Reduce redundant qualifiers: "strict mathematical", "extremely severe", "absolutely no", "fundamentally radical"
- Cut obvious padding sentences that add no information
- Make sentences more direct and concise
- The paper reads like it was written by someone trying to sound impressive. Make it read like it was written by someone who IS impressive (clear, precise, no fluff)

### Priority 2: Tighten Mathematical Content
- Section 2.1 (KD Fundamentals): The high-temperature limit derivation (Eq 3-5) is a textbook result. Keep the key insight but compress the derivation.
- Section 2.3 (Exposure Bias): The MDP formalization is good but could be tighter. The O(T²) bound derivation is the key point - keep that, reduce surrounding text.
- Section 4.3 (MiniLLM REINFORCE derivation): The full 4-line derivation (Eq 12) is the paper's own result. Keep it but make the surrounding explanation more concise.

### Priority 3: Fix Factual Issues
1. The tex says "The False Promise of Imitating Proprietary LLMs \citep{2305.15717}" but the bib entry for 2305.15717 actually IS this paper. However check if the citation context is correct - this paper argues that imitating proprietary LLMs gives a "false promise" due to data distribution mismatch. Verify the claim in the tex matches.

2. 2305.20050 = "Let's Verify Step by Step" (the PRM paper). In the tex it's cited as:
   - Section 3.1: "Process Reward Models (PRMs) \citep{2305.20050}" → This is correct, 2305.20050 IS the PRM paper
   - Section 6.2: "Process Reward Models (PRMs) \citep{2305.20050}" → Also correct

3. In the Taxonomy figure, "OPSD" should be checked. 2601.18734 = "Self-Distilled Reasoner" which the tex calls OPSD. The actual paper title is "Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models". So OPSD may be a short-hand but the full name in text should match.

4. The "Contrastive On-Policy Distillation" paragraph (Section 4.1) currently has NO citation after we removed 2403.14608 (which was wrong). This is a conceptual discussion that needs either: (a) a real citation, or (b) explicit framing as "a proposed direction" rather than citing a specific paper.

### Priority 4: Section Balance
- Section 2 (Background): ~3.5 pages - could be trimmed to ~2.5 pages (compress KD fundamentals)
- Section 4 (White-Box): ~5 pages - well-detailed, keep
- Section 5 (Black-Box): ~2.5 pages - adequate
- Section 6 (Reasoning): ~2.5 pages - could use more depth on DeepSeek-R1 distillation results
- Section 7 (Systems): ~2.5 pages - good
- Section 8 (Future): ~3 pages - some subsections feel formulaic (especially 8.8 "Practical Guidelines")

### Priority 5: Remove Table Entry Without Citation
The Contrastive OPD row in Table 1 no longer has a citation. Either:
- Remove the row entirely
- Or keep it as a described-in-text method without a specific paper reference

### DO NOT CHANGE
- The taxonomy figure (Figure 1) - it works
- The overall section structure
- The core thesis about "who decides the training distribution"
- The arXiv IDs and bib entries (they're now correct)

## Compilation
After edits:
```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```
Target: 0 errors, 0 warnings.
