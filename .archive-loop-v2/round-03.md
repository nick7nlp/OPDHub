# Round 03 — POLISH §1 Introduction

**Mode:** POLISH  
**Section:** §1 Introduction (lines 82–108)  
**Date:** 2026-05-08 16:21 UTC

## Changes Made (10 targeted edits)

### 1. Sentence splitting (¶1)
- **Before:** "...cost that only a handful of organizations can sustain, which has turned capability transfer...from an academic curiosity into one of the load-bearing techniques..."
- **After:** Split into two sentences. "This progress...can sustain. Capability transfer...has consequently moved from academic curiosity to one of the load-bearing techniques..."
- **Why:** Original was 60+ words with a nested relative clause. Splitting adds punch.

### 2. Remove double-whose chain (¶1)
- **Before:** "whose 671B...was successfully distilled...and whose long chain-of-thought reasoning survived..."
- **After:** "whose 671B...was distilled...with long chain-of-thought reasoning surviving the transfer largely intact."
- **Why:** Two chained `whose` is grammatically heavy. Also removed filler adverb "successfully" (the fact that it happened already implies success).

### 3. Tighten exposure bias sentence (¶2)
- **Before:** "with the additional twist that autoregressive generation amplifies it quadratically"
- **After:** "compounded by the fact that autoregressive generation amplifies the mismatch quadratically"
- **Why:** "additional twist" is colloquial/filler. "compounded by" is more precise and academic.

### 4. Split long compound sentence (¶2)
- **Before:** "...derail an entire proof or program, and \citet{2305.15717} already warned the community that..."
- **After:** "...derail an entire proof or program. \citet{2305.15717} warned that..."
- **Why:** Two independent clauses → two sentences. Also removed "already" and "the community" (redundant in a survey context).

### 5. Tighten feedback enumeration (¶3)
- **Before:** "this feedback can take the form of...or..."
- **After:** "this feedback ranges from...through...to..."
- **Why:** "ranges from X through Y to Z" is more structured and slightly shorter than "can take the form of X, Y, or Z" for a three-part enumeration.

### 6. Sharpen "made visible" (¶4)
- **Before:** "a series of design choices made visible"
- **After:** "a series of design choices progressively surfaced"
- **Why:** "made visible" is vague. "progressively surfaced" conveys the temporal unfolding.

### 7. Remove "exposing the fact that" (¶4)
- **Before:** "gradually exposing the fact that"
- **After:** "gradually revealing that"
- **Why:** "exposing the fact that" is wordy (4 words → 2).

### 8. Fix double "its own" (¶4)
- **Before:** "from its own generations by exploiting asymmetries in its own context"
- **After:** "from its own generations by exploiting asymmetries in its output distribution across contexts"
- **Why:** "its own...its own" is repetitive. The new version is also more precise (the asymmetry is in distribution, not in "context" itself).

### 9. Strengthen verbs (¶5)
- **Before:** "focused on whether...the current frontier concerns how..."
- **After:** "asked whether...the current frontier asks how..."
- **Why:** "asks" is more direct than "concerns" and parallels with past tense "asked."

### 10. Remove filler adjective (¶5, ¶6)
- **Before:** "This acceleration reflects a deeper structural trend"
- **After:** "This acceleration tracks a structural trend"
- **Why:** "deeper" is filler (deeper than what?). "tracks" is more concrete than "reflects."

- **Before:** "Methods reach the same objective from the vantage points...and they inherit..."
- **After:** "Methods approach the same problem from the vantage points...inheriting..."
- **Why:** "reach the same objective" is semantically off (they don't reach the same objective; they study the same phenomenon). Participial clause tightens two independent clauses into one.

## Verification
- ✅ Compiled with `pdflatex` — 0 errors, 0 undefined references
- ✅ No semicolons introduced
- ✅ No prose colons introduced (structural only)
- ✅ No cite keys changed

## Quality assessment
Introduction now reads more crisply. Long subordinate chains broken up. Filler reduced. Verbs strengthened. No content or citations changed — pure prose-level polish.
