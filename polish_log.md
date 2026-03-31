# 10-Round Polish Log

## Round 1: Narrative Flow
- Fixed: Improved transition in §4.3 Hybrid — added explicit list of four optimization dimensions ("compute efficiency, capacity gap bridging, curriculum design, and novel paradigms") instead of vague "by the optimization dimension they target"
- Fixed: Rewrote §4.3.4 Novel Paradigms intro — added "that reframe what distillation means" for clearer signposting
- Fixed: Added transition between TSD-KD and DASD/DDT in Novel Paradigms — "The remaining two methods in this category challenge the SFT-based distillation paradigm itself"
- Fixed: Added explicit transition sentence between adversarial and preference-based black-box methods in §5.1 — "Moving beyond adversarial objectives, a second family of black-box methods constructs supervision through preference pairs rather than discriminator scores."
- Fixed: Rewrote §5.2.3 Reward-Free Alignment intro — added thematic framing "A recurring theme...the key insight is that structured feedback from the environment or from the model's own historical behavior can substitute for scalar rewards"
- Fixed: Added inter-paragraph connectors in §5.2.3 — "While SDPO targets credit assignment, TMS addresses a different RL benefit: retention" and "A complementary challenge arises when standard RL itself fails"
- Fixed: Expanded §5.2.2 Privileged Information intro — added "Rather than pitting the model against itself in a zero-sum game...This asymmetry injects fresh information into the loop"
- Compile: ✅ 0 errors, 37 pages

## Round 2: Citation Accuracy
- Verified: All \citep/\citet usages are contextually appropriate
- Verified: No undefined citation keys (checked main.log)
- Verified: DAgger/ross2011reduction correctly cited in §2.3 exposure bias context
- Verified: kim2016sequence correctly cited for sequence-level KD
- Verified: PRMs cited with correct paper (2305.20050)
- No changes needed — all citations are accurate
- Compile: ✅ 0 errors, 37 pages

## Round 3: Mathematical Formulas
- Verified: All 25+ equation environments match (begin/end pairs balanced)
- Verified: All equation labels (eq:gkd, eq:distillm, eq:todi, eq:minillm_final, eq:cot_opd, eq:rlkd, eq:scaling) are referenced in text
- Verified: Symbol consistency — §4 uses \ptheta/\pteacher (token-level), §6 uses P_\theta/P_T (trajectory-level) as documented in §6 intro
- Verified: Custom macros (\ptheta, \pteacher, \KL, \loss, \pdata) used consistently
- No formula errors or missing equations found
- Compile: ✅ 0 errors, 37 pages

## Round 4: English Grammar and Style
- Fixed: §7 "the off-policy ceiling; the maximum achievable..." → em-dashes (semicolons used as parenthetical markers)
- Fixed: §8 opening "the theoretical foundations remain sparse" — fixed nested parentheses and semicolons with em-dashes
- Fixed: §8.7 "Distill $\to$ RL or RL $\to$ Distill." — fixed missing closing parenthesis
- Fixed: §8.7 "the on-policy training distribution; not the reward signal per se;" → em-dashes
- Fixed: §7 GPU Memory "and; critically; the KV cache" → em-dashes
- Fixed: §6 intro — removed redundant "Kullback-Leibler (KL)" (already defined in §2)
- Fixed: §6 intro — removed redundant expansion of "LLM" and "OPD" and "CoT" (all already defined earlier)
- Fixed: §8.5 comma splice "Third, \emph{safety-critical credit assignment}," → colon
- Compile: ✅ 0 errors, 37 pages

## Round 5: Logical Coherence
- Verified: All section openings clearly state scope (§4 lists four subsections, §5 explains two regimes, §6 explains reasoning context)
- Fixed: Added transition between TSD-KD and DASD in §4.3.4 — "The remaining two methods in this category challenge the SFT-based distillation paradigm itself" (connects preference-based methods to SFT-critique methods)
- Verified: §4 progression is logical: fixed divergences → adaptive → token weighting → cross-architecture → theory
- Verified: §5 progression is logical: black-box → self-play → privileged info → compression → reward-free → saturation analysis
- Verified: §6 progression: CoT distillation → reward-guided → DeepSeek-R1 case study → post-R1 methods
- No logical jumps or gaps found beyond the transition fix above
- Compile: ✅ 0 errors, 37 pages

## Round 6: Redundancy Check
- Fixed: OPSDC was described in full detail in both §5.2.3 and §6. Trimmed §6 version to cross-reference §5 ("As discussed in Section~\ref{subsec:self_distill}") while keeping the AIME 2024 results unique to §6
- Fixed: SDFT was described in full detail in both §5.2.4 and §8.7. Trimmed §8.7 version to cross-reference §5 ("introduced in Section~\ref{subsec:self_distill}") while preserving the RL-alternative framing unique to §8
- Verified: §2.5 Unified View and §4.1 overlap is intentional and properly cross-referenced ("As established in the unified framework of Section~\ref{subsec:unified_view}")
- Verified: §5 SPIN description and §5.4 saturation analysis are complementary (description vs. analysis)
- No other harmful redundancies found
- Compile: ✅ 0 errors, 37 pages

## Round 7: Table and Figure References
- Verified: Figure 1 (fig:forward_vs_reverse_kl) — referenced in §4.1 cross-method analysis
- Verified: Figure 2 (fig:taxonomy_tree) — referenced in §3 taxonomy intro
- Verified: Table 1 (tab:white_box_comparison) — referenced in §4.1 and §9 Conclusion
- Verified: Table 2 (tab:experimental_configs) — referenced in §4.1 and §9 Conclusion
- Verified: All 4 floats (2 figure*, 2 table*) are referenced at appropriate locations
- Verified: Captions accurately describe table/figure contents
- No unreferenced floats or misplaced references
- Compile: ✅ 0 errors, 37 pages

## Round 8: LaTeX Formatting
- Verified: Em-dashes consistently use `---` throughout (no spaced em-dashes)
- Verified: En-dashes correctly used for ranges (e.g., "57--59\%", "$6.7$--$12\times$")
- Verified: No double spaces in running text (only in math/TikZ environments)
- Verified: \textbf and \textit usage is consistent for method names and emphasis
- Verified: `\,` spacing used appropriately in units (e.g., "$\sim$140\,GB")
- Verified: Equation punctuation style is consistently omitted (valid style, consistent throughout)
- Note: One overfull hbox at line 542 (Entropy-Aware equation) — cosmetic, not actionable without equation reformulation
- Compile: ✅ 0 errors, 37 pages

## Round 9: Terminology Unification
- Verified: "on-policy" consistently hyphenated throughout (no "on policy" without hyphen)
- Verified: "off-policy" consistently hyphenated throughout
- Verified: "self-distillation" consistently hyphenated
- Verified: "chain-of-thought" lowercase in running text, "Chain-of-Thought" in section titles — correct convention
- Verified: PPO defined on first use (line 463, §3 Outcome-Based Feedback)
- Verified: DPO defined on first use (line 463, same context)
- Verified: SFT well-known abbreviation; defined in text at line 920 (§6.3)
- Verified: KD defined in §1 Introduction
- Verified: OPD defined in §1 Introduction
- Verified: CoT defined in §1 Introduction
- No terminology inconsistencies found
- Compile: ✅ 0 errors, 37 pages

## Round 10: Final Read-through
- Fixed: §9 Conclusion "Key Findings" — semicolons used as parenthetical markers replaced with em-dashes ("from $y \sim \pdata$ to $y \sim \ptheta$")
- Fixed: §9 Conclusion "Key Findings" — "sparse outcome rewards; KD provides stability" → colon
- Fixed: §9 Conclusion "Practical Takeaways" — "on-policy generation; typically $3\text{--}8\times$..." → em-dashes
- Fixed: §9 Conclusion "Looking Ahead" — "lifecycle; from pre-training through deployment" → em-dash
- Fixed: §8.6 VOLD — "VOLD's key finding; that..." → em-dashes
- Fixed: §8.8 Practical Guidelines — "clear exposure bias; performing well" → em-dash
- Fixed: §8.8 Practical Guidelines — "The hybrid approach; off-policy SFT warm-up" → em-dashes
- Fixed: §6.2 RLAD — "selective imitation strategy; the student follows" → colon
- Fixed: §7 Speculative KD — "verifies in parallel produces" → "verifies in parallel, producing" (missing comma created a run-on)
- Compile: ✅ 0 errors, 37 pages

---

## Summary of All Changes

**Total edits: 25 targeted modifications across 10 rounds**

### By category:
- **Narrative flow improvements**: 7 edits (transitions, connectors, thematic framing)
- **Semicolon→em-dash corrections**: 12 edits (systematic replacement of semicolons misused as parenthetical markers)
- **Redundancy reduction**: 2 edits (OPSDC and SDFT cross-referenced instead of duplicated)
- **Grammar fixes**: 3 edits (missing parenthesis, comma splice, run-on sentence)
- **Terminology cleanup**: 1 edit (removed redundant abbreviation re-definitions)

### What was NOT changed (per constraints):
- §1 Introduction content — untouched
- §2 Background content — untouched
- Table 1 and Table 2 content — untouched
- No citations were deleted
- All 10 rounds compiled with 0 errors
