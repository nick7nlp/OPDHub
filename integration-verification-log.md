# New Paper Integration Verification Log
Date: 2026-04-21

## Papers Integrated
1. **TIP** (2604.14084) → §4.2.1, Table 1, Table 3, Taxonomy Tree
2. **π-Play** (2604.14054) → §5.2, Table 1, Table 3, Taxonomy Tree
3. **ORBIT** (2601.08310) → §7.1, Table 1, Table 3
4. **SCOPE** (2604.10688) → Already present, no changes

## Verification Summary

### Phase 1: Per-Paper Fact Verification (via arXiv HTML fetch)

#### TIP Claims Verified ✅
| Claim | Status | Source |
|-------|--------|--------|
| Soft-OR: s_t = h_hat + d_hat - h_hat·d_hat | ✅ | Eq.5 |
| Q3 = overconfident errors (low h, high δ) | ✅ | Table 1 |
| Proposition 2: entropy-only blind to Q3 | ✅ | §5, Proposition 2 |
| "non-decreasing with f(0)=0" (not "monotonic") | ✅ corrected | Proposition 2 |
| Parameter-free, no extra computation | ✅ | §6 |
| 3 model families: Qwen3, Llama, Qwen2.5 | ✅ | §7.1 |
| Capacity gaps 2× to 9× | ✅ | 8B→4B=2×, 14B→1.5B≈9× |
| Memory reduction up to 47% (not 2×) | ✅ corrected | Table 5 (72→38.1 GB) |

#### π-Play Claims Verified ✅
| Claim | Status | Source |
|-------|--------|--------|
| QCP = question construction path | ✅ | Abstract, §3 |
| 3 co-evolving agents: examiner, teacher, student | ✅ | §3.1 |
| Teacher KL-constrained to track student | ✅ | Eq.2 (β D_KL term) |
| Surpasses Search-R1 by 5-15% (not 6-15%) | ✅ corrected | 6.2%/5.2%/14.5% |
| 2-3× efficiency over Dr.Zero | ✅ | Abstract |
| Data-free (no external data) | ✅ | §3.1 |
| Qwen3 series (4B and 8B) | ✅ | §4.1 |
| RL used (examiner/teacher use rewards) | ✅ | Eq.1, Eq.2 |

#### ORBIT Claims Verified ✅
| Claim | Status | Source |
|-------|--------|--------|
| Expansion-compression: L_{k+1} = L_k/2 | ✅ | §3.1 |
| Multi-teacher Reverse KL fusion | ✅ | Eq.12 |
| Model merging for cold-start | ✅ | §3.2 |
| Cold-start attributed to Jang et al. (not PACED) | ✅ corrected | Ref section |
| 3 models: DeepSeek-1.5B, Qwen3-4B, Nemotron-7B | ✅ | §4.1 |
| 4 reasoning modes (Low/Mid/High/Xhigh) | ✅ | §4.1 |
| 2K-32K token budgets | ✅ | §4.1 |
| "Competitive performance" (not "matching/exceeding") | ✅ corrected | Table 1 |
| 2-7× token savings at lower budgets | ✅ | 2.0-7.6× actual |

### Phase 2: BibTeX Verification ✅
All 3 entries verified against arXiv API:
- xu2026tip: title ✅, authors ✅, ID ✅, no venue
- zhang2026piplay: title ✅, authors ✅, ID ✅, no venue
- liang2026orbit: title ✅, authors ✅, ID ✅, no venue

### Phase 3: Document Consistency ✅
- 100/100 citations match (tex ↔ bib)
- 0 undefined refs/cites
- 0 LaTeX errors
- 0 semicolons in prose
- 0 em-dashes in prose
- Taxonomy tree badges correct (verified per-node)
- Table 1 + Table 3 entries consistent with prose
- New papers do NOT appear in §6/§8 (intentional)

### Phase 4: Corrections Made
1. TIP memory: "up to 2×" → "up to 47%"
2. TIP theory: "monotonic" → "non-decreasing with f(0)=0"
3. π-Play Search-R1: "6-15%" → "5-15%"
4. ORBIT cold-start: \citet{2603.11178} → \citet{2601.07155}
5. ORBIT performance: "matching or exceeding" → "competitive performance"

### Phase 5: GitHub ✅
- 3 papers promoted from 🟡 to 🟢
- TIP moved from Evaluation to Token-Level
- Badge: 92 unique papers
- Push: 6f65b6a

### Final State
- **51 pages** | **100 citations** | **0 errors** | **0 undefined**
- Backup: main.tex.bak-4papers-integrated
