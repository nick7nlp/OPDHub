---
name: academic-writing
description: Write high-quality academic papers (surveys, research papers, position papers). Covers taxonomy design, figure generation, comprehensive literature coverage, structured writing with citation checking, and LaTeX compilation. Use when writing any academic paper, survey, or comprehensive review.
metadata:
  openclaw:
    emoji: "📝"
---

# Academic Writing Skill

## Overview
This skill produces publication-quality academic papers with comprehensive literature coverage, clear taxonomy figures, detailed comparison tables, and polished writing.

## Paper Types Supported
- **Survey/Review papers**: Comprehensive literature surveys with taxonomy
- **Research papers**: Original contribution papers
- **Position papers**: Opinion/direction papers
- **Tutorial papers**: Educational overview papers

## Survey Writing Pipeline (7 Stages)

### Stage 1: Literature Collection (Wide Net)
**Goal**: 100-200 relevant papers minimum for a survey.

1. **Seed search**: 5-10 key queries across Google Scholar, Semantic Scholar, arXiv
2. **Citation crawling**: For each seed paper, collect its references and citing papers
3. **Snowball expansion**: Repeat for high-relevance papers
4. **Quality filtering**: Keep papers from top venues + highly cited + recent arXiv
5. **Paper KB integration**: All papers enter `paper_kb` with `project:survey:<topic>` tag
6. **Generate one_liners**: LLM-generated 1-sentence summary for each paper

Target: Cover ALL relevant work. Missing a key paper is worse than including a marginal one.

### Stage 2: Taxonomy Design (The Core)
**Goal**: A clear, multi-dimensional classification framework.

A good taxonomy:
- Is **mutually exclusive** and **collectively exhaustive** (MECE)
- Has 2-3 classification dimensions (e.g., by method type × by training signal × by teacher access)
- Maps every collected paper into exactly one primary category
- Reveals the landscape and gaps in the field

Process:
1. Read all paper one_liners and abstracts
2. Identify natural clusters (by method, by application, by technique)
3. Design a hierarchical taxonomy tree
4. Validate: every paper should fit; no category should be empty
5. Create a **TikZ taxonomy figure** (see templates below)

### Stage 3: Outline Generation (Chunk-Merge-Refine)
Inspired by SurveyForge:

1. **Chunk**: Split papers into groups of 30-50
2. **Per-chunk outline**: Generate a section-level outline for each chunk
3. **Merge**: Combine all chunk outlines into a unified outline
4. **Refine**: Remove overlaps, ensure coverage, add cross-references
5. **Subsection outline**: For each section, generate subsection-level outlines with bullet points

### Stage 4: Writing (RAG-Driven, Section by Section)
For each subsection:

1. **Retrieve**: Use paper_kb to find 10-20 most relevant papers for this subsection
2. **Write**: Generate content with specific citations
3. **Citation check**: Verify every \cite{} actually supports the claim
4. **Depth check**: Each subsection should be 500-1000 words with:
   - Clear topic sentence
   - Method description with mathematical formulation where appropriate
   - Comparison with related methods
   - Concrete results/numbers when available
   - Transition to next subsection

### Stage 5: Enhancement (LCE + Cross-references)
**Local Coherence Enhancement** (from SurveyForge):

1. For each subsection, read (previous + current + next)
2. Rewrite current to improve flow and connections
3. Process in interleaved order (even indices first, then odd)

Also add:
- Forward/backward references ("as discussed in Section X", "we will detail in Section Y")
- Summary paragraphs at end of major sections
- Comparison tables consolidating key information

### Stage 6: Figures and Tables
**Required elements**:

1. **Taxonomy figure**: TikZ tree diagram showing the classification
2. **Timeline figure**: Key milestones chronologically
3. **Method comparison table**: Method / Year / Venue / Key Features / Results
4. **Performance comparison table**: Methods × Benchmarks (if applicable)

### Stage 7: Compilation and Review
1. LaTeX compilation (pdflatex × 3 + bibtex)
2. BibTeX verification via bibtex_client
3. Self-review checklist:
   - [ ] Every claim has a citation
   - [ ] Every cited paper is in references
   - [ ] Figures are referenced in text
   - [ ] Tables are referenced in text
   - [ ] No orphaned sections (< 300 words)
   - [ ] Introduction clearly states contributions
   - [ ] Conclusion has forward-looking directions
   - [ ] Abstract covers: problem, approach, scope, findings, implications

## What Makes a Great Survey

Learned from high-impact surveys (Zhao et al. LLM Survey 10k+ citations, Xu et al. KD Survey):

### Structure Patterns
- **Introduction**: Hook → Problem → Why now → Scope → Contributions → Paper organization
- **Background**: Formal definitions, notation, prerequisite knowledge
- **Taxonomy section**: Overview figure + classification criteria explanation
- **Method sections**: Organized by taxonomy, each with subsections
- **Discussion/Analysis**: Cross-cutting analysis, trends, lessons learned
- **Future Directions**: 5-8 concrete, actionable research directions with justification
- **Conclusion**: Summary + key takeaways + call to action

### Quality Indicators
- **Coverage**: No major work missing (check awesome-lists, citation graphs)
- **Depth**: Not just listing papers; analyze, compare, synthesize
- **Insight**: Original observations about trends, gaps, connections
- **Figures**: At least 3-5 figures (taxonomy, timeline, architecture comparison)
- **Tables**: At least 2-3 comparison tables
- **Future directions**: Specific, insightful, not generic ("more research needed")
- **Writing**: Active voice where possible, precise technical language, logical flow

### Common Mistakes to Avoid
- Listing papers without synthesizing them
- Missing recent preprints (check arXiv last 3 months)
- Taxonomy that doesn't cover all papers
- Sections that are too short (< 300 words) or too long (> 3 pages)
- Generic future directions ("scaling up", "more benchmarks")
- Inconsistent notation across sections
- Not explaining why the survey is needed NOW

## TikZ Templates

### Taxonomy Tree
```latex
\begin{figure*}[t]
\centering
\begin{tikzpicture}[
    level 1/.style={sibling distance=45mm, level distance=15mm},
    level 2/.style={sibling distance=22mm, level distance=15mm},
    level 3/.style={sibling distance=15mm, level distance=12mm},
    every node/.style={draw, rounded corners, minimum height=7mm, minimum width=20mm, font=\small, align=center},
    root/.style={fill=blue!20, font=\small\bfseries},
    l1/.style={fill=orange!20},
    l2/.style={fill=green!15},
    edge from parent/.style={draw, -latex}
]
\node[root] {Root Topic}
    child { node[l1] {Category 1}
        child { node[l2] {Sub 1.1} }
        child { node[l2] {Sub 1.2} }
    }
    child { node[l1] {Category 2}
        child { node[l2] {Sub 2.1} }
        child { node[l2] {Sub 2.2} }
    }
    child { node[l1] {Category 3}
        child { node[l2] {Sub 3.1} }
    };
\end{tikzpicture}
\caption{Taxonomy of [Topic].}
\label{fig:taxonomy}
\end{figure*}
```

### Timeline Figure
```latex
\begin{figure*}[t]
\centering
\begin{tikzpicture}[scale=1.0]
    \draw[thick,-latex] (0,0) -- (14,0) node[right] {Time};
    % Year markers
    \foreach \x/\year in {1/2022, 4/2023, 7/2024, 10/2025, 13/2026} {
        \draw (\x,0.15) -- (\x,-0.15) node[below] {\small\year};
    }
    % Events (alternate above/below)
    \foreach \x/\label/\pos in {
        2/{Paper A}/above,
        3.5/{Paper B}/below,
        5/{Paper C}/above
    } {
        \fill[blue!60] (\x,0) circle (3pt);
        \node[\pos, font=\tiny, text width=2cm, align=center] at (\x,0) {\label};
    }
\end{tikzpicture}
\caption{Timeline of key developments.}
\label{fig:timeline}
\end{figure*}
```

### Method Comparison Table
```latex
\begin{table*}[t]
\centering
\caption{Comparison of representative methods.}
\label{tab:comparison}
\resizebox{\textwidth}{!}{
\begin{tabular}{lcccccl}
\toprule
\textbf{Method} & \textbf{Year} & \textbf{Venue} & \textbf{Teacher} & \textbf{Divergence} & \textbf{On-Policy} & \textbf{Key Contribution} \\
\midrule
Method A & 2024 & ICLR & White-box & Forward KL & \checkmark & Description \\
Method B & 2024 & ICML & Black-box & Reverse KL & \checkmark & Description \\
\bottomrule
\end{tabular}
}
\end{table*}
```

## BibTeX Quality
- Always verify via bibtex_client (DBLP > CrossRef > S2 > arXiv)
- Prefer published venue entries over arXiv when available
- Never fabricate BibTeX; if uncertain, use @misc with arXiv ID

## Writing Quality Checklist
- [ ] Abstract: ≤250 words, covers problem/approach/scope/findings
- [ ] Introduction: States 3-5 specific contributions
- [ ] Each section: Opening paragraph summarizes what follows
- [ ] Each subsection: 500-1000 words with substantive analysis
- [ ] Transitions: Every section/subsection connects to the next
- [ ] Future directions: 5+ specific, actionable directions
- [ ] References: 100+ for surveys, 30+ for research papers
- [ ] Figures: ≥3 (taxonomy + timeline + at least one more)
- [ ] Tables: ≥2 (method comparison + results comparison)
- [ ] No unsubstantiated claims (every assertion backed by citation or data)
