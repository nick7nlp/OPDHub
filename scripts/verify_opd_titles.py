#!/usr/bin/env python3
"""Verify OPD paper titles against arXiv."""
import json
import re
import time
import urllib.request
import urllib.error
import sys

ENTRIES = {
    "2605.08737": "ListOPD: Extrapolation Cliff",
    "2605.08741": "OPHSD: Harness Self-Distillation",
    "2605.08776": "MPD: Mixed-Policy Distillation",
    "2605.08873": "CoDistill-GRPO",
    "2605.09253": "Rock Tokens",
    "2605.09548": "COPSD: Crosslingual",
    "2605.09725": "BRTS: Best-of-N Rollout",
    "2605.10889": "Unmasking OPD",
    "2605.11182": "Many Faces of OPD",
    "2605.11458": "ATESD: Adaptive Teacher Exposure",
    "2605.11609": "AntiSD: Anti-Self-Distillation",
    "2605.11613": "CREDIT: Input-Specific Credit",
    "2605.11739": "EffOPD: Efficiency Analysis",
    "2605.11854": "TABOM: Diffusion LM",
    "2605.12227": "dGRPO: Long-Context",
    "2605.12400": "OGLS-SD: Logit Steering",
    "2605.12483": "Beyond GRPO and OPD",
    "2605.07177": "HyperEyes: Dual-Grained Efficiency-Aware RL for Parallel Multimodal Search Agents",
    "2605.10189": "ProteinOPD: Towards Effective and Efficient Preference Alignment for Protein Design",
    "2605.10194": "TRACE: Distilling Where It Matters via Token-Routed Self On-Policy Alignment",
    "2605.09329": "Test-Time Speculation",
    "2605.06230": "Safactory: A Scalable Agentic Infrastructure for Training Trustworthy Autonomous Intelligence",
    "2605.13724": "AnyFlow: Any-Step Video Diffusion Model with On-Policy Flow Map Distillation",
    "2605.13643": "Prefix Teach, Suffix Fade: Local Teachability Collapse in Strong-to-Weak OPD",
    "2605.13501": "RWOPD: Reward-Weighted On-Policy Distillation for NL-to-SVA Generation",
    "2605.13255": "EGRSD: Respecting Self-Uncertainty in On-Policy Self-Distillation",
    "2605.13230": "TGPO: Teacher-Guided Policy Optimization for LLM Distillation",
    "2605.12913": "Revisiting DAgger in the Era of LLM-Agents",
    "2605.12652": "MOPD: Multi-Rollout On-Policy Distillation via Peer Successes and Failures",
    "2605.11853": "GEAR: Granularity-Adaptive Advantage Reweighting via Self-Distillation",
    "2605.12741": "RESD: Learning with Rare Success but Rich Feedback via Reflection-Enhanced Self-Distillation",
    "2605.10875": "SOL: Self Optimizing Language Models",
    "2605.09920": "VIGOR: Verifier-Free RL via Gradient-Norm Reward",
    "2605.08887": "Ace-Skill: Bootstrapping Multimodal Agents",
    "2605.07579": "POISE: RL with Value from Actor's Internal States",
    "2605.04559": "BLADE: Bayesian List-wise Alignment for LLM4Rec",
    "2605.10518": "IMDM: Infinite Mask Diffusion Few-Step Distillation",
    "2605.07820": "Scaling Categorical Flow Maps",
    "2605.07274": "SRPO: Structured Role-Aware Policy Optimization",
    "2605.06850": "Shadow Mask Distillation: KV Cache Compression for Memory-Efficient RL Alignment",
    "2605.09536": "TAD: Temporal-Aware Trajectory Self-Distillation for Diffusion LLM",
    "2605.11651": "Hide to See: Reasoning-prefix Masking for VLM Distillation",
    "2605.11556": "Hindsight Hint Distillation (HHD)",
    "2605.07327": "Teacher-Feature Drifting",
    "2605.08354": "Auto-Rubric as Reward (ARR)",
    "2605.07503": "Diffusion-APO",
    "2605.09422": "ADPO (Anti-Distillation Policy Opt)",
    "2605.07276": "Signal Reshaping for GRPO",
    "2605.13665": "Robot Squid Game: Quadrupedal Locomotion",
    "2605.12798": "Emergent and Subliminal Misalignment Through Data-Mediated Transfer",
    "2605.13165": "STOP: Structured On-Policy Pruning of Long-Form Reasoning",
    "2605.10781": "RLRT",
}

def fetch_arxiv_title(arxiv_id, retries=3):
    """Fetch title from arXiv API."""
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read().decode('utf-8')
            # Extract title from XML
            m = re.search(r'<title[^>]*>(.*?)</title>', data, re.DOTALL)
            if m:
                # Skip the feed title "ArXiv Query..."
                titles = re.findall(r'<title[^>]*>(.*?)</title>', data, re.DOTALL)
                if len(titles) >= 2:
                    title = titles[1].strip()
                    # Clean up whitespace
                    title = re.sub(r'\s+', ' ', title)
                    return title
            return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return f"ERROR: {e}"


def normalize(s):
    """Normalize for comparison."""
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s


results = {"match": [], "mismatch": [], "error": []}

ids = list(ENTRIES.keys())
batch_size = 5

for i in range(0, len(ids), batch_size):
    batch = ids[i:i+batch_size]
    for arxiv_id in batch:
        our_title = ENTRIES[arxiv_id]
        real_title = fetch_arxiv_title(arxiv_id)
        
        if real_title is None or real_title.startswith("ERROR"):
            results["error"].append({"id": arxiv_id, "our": our_title, "error": real_title})
            print(f"❓ {arxiv_id}: {real_title}", flush=True)
        else:
            # Check if our abbreviated title is contained in real title or vice versa
            our_norm = normalize(our_title)
            real_norm = normalize(real_title)
            
            # For abbreviated titles (like "ListOPD: Extrapolation Cliff"), 
            # check if key words match
            # But for full titles, do exact match
            if our_norm == real_norm:
                results["match"].append({"id": arxiv_id, "our": our_title, "real": real_title})
                print(f"✅ {arxiv_id}: OK", flush=True)
            else:
                # Check if it's just an abbreviation (our title words all in real title)
                our_words = set(our_norm.split())
                real_words = set(real_norm.split())
                # If >70% of our words are in real title, it's likely an abbreviation
                overlap = len(our_words & real_words) / max(len(our_words), 1)
                
                results["mismatch"].append({
                    "id": arxiv_id, 
                    "our": our_title, 
                    "real": real_title,
                    "overlap": round(overlap, 2)
                })
                print(f"❌ {arxiv_id}: MISMATCH (overlap={overlap:.0%})", flush=True)
                print(f"   Ours: {our_title}", flush=True)
                print(f"   Real: {real_title}", flush=True)
        
        time.sleep(0.5)  # Rate limit
    
    # Pause between batches
    if i + batch_size < len(ids):
        time.sleep(1)

print(f"\n{'='*60}")
print(f"SUMMARY: {len(results['match'])} match, {len(results['mismatch'])} mismatch, {len(results['error'])} error")
print(f"{'='*60}")

if results["mismatch"]:
    print("\n## MISMATCHES (need review):")
    for item in results["mismatch"]:
        print(f"\n{item['id']} (overlap={item['overlap']}):")
        print(f"  Ours: {item['our']}")
        print(f"  Real: {item['real']}")

if results["error"]:
    print("\n## ERRORS (could not verify):")
    for item in results["error"]:
        print(f"  {item['id']}: {item['error']}")

# Save full results
with open('/root/.openclaw/workspace/scripts/title_verify_results.json', 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
