#!/usr/bin/env python3
"""OPD second-opinion verifier — Phase 3.7 in the pipeline.

After deep-read (Phase 2) + triage (Phase 3) + 3-condition filter (Phase 3.5),
this script re-checks surviving candidates by sending a focused OPD-3-condition
query to a DIFFERENT model (Gemini by default, since deep-read uses Claude).

Purpose: catch false positives that slip through deep-read + 3-cond filter.
6/26 实战证明: deep-read 50% 误判率, 3-cond filter 只挡住了部分, 3 篇非 OPD 论文
进了 README（RL+KL anchor, 非 LLM 模态, off-policy）。这个二次验证用不同模型
交叉检查, 只问最核心的 3 个条件。

Usage:
    python3 opd_second_opinion.py --aids 2606.25442,2606.25800 --model gemini
    python3 opd_second_opinion.py --aids 2606.25442 --model claude-sonnet

Output: JSON array with verdict per paper:
    [{"aid": "...", "verdict": "CONFIRM"|"REJECT"|"UNCERTAIN", "reasoning": "..."}]
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.expanduser("~/clawd/lib"))
sys.path.insert(0, os.path.expanduser("~/clawd"))

SURVEY_ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
NOTES_PATH = SURVEY_ROOT / "notes" / "paper_notes.json"


def log(*args, **kw):
    print(*args, file=sys.stderr, **kw)


def extract_pdf_text(pdf_path: Path, max_chars: int = 30_000) -> str:
    """Extract first ~30K chars from PDF (enough for methods section)."""
    try:
        import pdfplumber
    except ImportError:
        log("ERROR: pdfplumber not installed")
        sys.exit(2)

    pages_text = []
    total_chars = 0
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            try:
                t = page.extract_text() or ""
            except Exception:
                t = ""
            pages_text.append(t)
            total_chars += len(t)
            if total_chars > max_chars:
                break
    return "\n".join(pages_text)[:max_chars]


def find_pdf(aid: str) -> Path | None:
    for d in sorted(SURVEY_ROOT.glob("pdfs/*/"), reverse=True):
        if d.name == "by-aid":
            continue
        p = d / f"{aid}.pdf"
        if p.exists():
            return p
    return None


SECOND_OPINION_PROMPT = """You are an expert reviewer checking whether a paper qualifies as On-Policy Distillation (OPD).

OPD requires ALL THREE conditions:
  (C1) Student generates its own rollouts DURING the training loop
  (C2) A SEPARATE, MORE CAPABLE teacher provides logit-level supervision on those student rollouts
  (C3) The loss is KL/distributional divergence (not MSE, not reward, not SFT on text)

CRITICAL: These are NOT OPD:
- RL + KL anchor: D_KL(π_θ ∥ π_ref) where π_ref is the student's OWN initial checkpoint (not a teacher)
- Robotics/GNN/image generation (non-LLM domain)
- Off-policy: student learns from teacher-generated text (teacher does the generating, not student)
- System papers that apply existing KD without novel method
- Expert trace SFT: learning from expert text without logit supervision

Read this paper excerpt and answer:

1. Does the student generate its own rollouts during training? (C1) — yes/no/unclear
2. Is there a SEPARATE, MORE CAPABLE teacher providing LOGIT supervision? (C2) — yes/no/unclear
   (KL anchor to own SFT checkpoint = NO. Self-distillation from same model = MAYBE.)
3. Is the loss a KL/distributional divergence? (C3) — yes/no/unclear
4. Is the output modality text/language? — yes/no
5. Does the paper propose a NOVEL OPD method (not just apply existing KD)? — yes/no

Final verdict: CONFIRM (all conditions met) / REJECT (any condition fails) / UNCERTAIN

Respond in JSON:
{
  "C1_student_rollouts": "yes/no/unclear",
  "C1_evidence": "brief evidence",
  "C2_teacher_logits": "yes/no/unclear",
  "C2_evidence": "brief evidence — is the teacher a separate, more capable model?",
  "C3_kl_loss": "yes/no/unclear",
  "C3_evidence": "brief evidence",
  "text_modality": "yes/no",
  "novel_method": "yes/no",
  "verdict": "CONFIRM/REJECT/UNCERTAIN",
  "reasoning": "one-sentence summary"
}

Paper text:
"""


def call_llm(prompt: str, model: str = "gemini") -> str:
    """Call LLM API for second opinion."""
    import requests
    from config import cfg

    api_key = f"{cfg['api']['user']}:{cfg['api']['apikey']}"

    # Gemini path (default for second opinion — cross-model verification)
    gemini_models = {
        "gemini": "naci_default/gemini-3.1-pro-preview",
        "gemini-pro": "naci_default/gemini-3.1-pro-preview",
    }
    claude_models = {
        "claude-sonnet": "api_aws_third_anthropic.claude-sonnet-4-6",
    }

    if model in claude_models:
        model_id = claude_models[model]
        url = "http://llm-api.model-eval.woa.com/v1/messages"
        payload = {
            "model": model_id,
            "max_tokens": 2000,
            "system": "Output ONLY valid JSON. No markdown fences.",
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        r.raise_for_status()
        data = r.json()
        for blk in data.get("content", []):
            if blk.get("type") == "text":
                return blk["text"]
        raise RuntimeError(f"no text in response: {data}")
    else:
        model_id = gemini_models.get(model, model)
        url = "http://llm-api.model-eval.woa.com/v1/chat/completions"
        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": "Output ONLY valid JSON. No markdown."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 2000,
            "temperature": 0.1,
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


def verify_paper(aid: str, model: str) -> dict:
    """Get second opinion on a single paper."""
    pdf = find_pdf(aid)
    if not pdf:
        return {"aid": aid, "verdict": "UNCERTAIN", "reasoning": "PDF not found"}

    log(f"[2nd-opinion] {aid} ← {pdf.name} (model={model})")
    text = extract_pdf_text(pdf)
    prompt = SECOND_OPINION_PROMPT + text

    try:
        raw = call_llm(prompt, model)
    except Exception as e:
        return {"aid": aid, "verdict": "UNCERTAIN", "reasoning": f"LLM error: {e}"}

    # Parse JSON
    raw_clean = raw.strip()
    if raw_clean.startswith("```"):
        first_nl = raw_clean.find("\n")
        if first_nl != -1:
            raw_clean = raw_clean[first_nl + 1:]
        if raw_clean.rstrip().endswith("```"):
            raw_clean = raw_clean.rstrip()[:-3].rstrip()

    try:
        result = json.loads(raw_clean)
    except json.JSONDecodeError:
        return {"aid": aid, "verdict": "UNCERTAIN", "reasoning": f"JSON parse error: {raw[:200]}"}

    result["aid"] = aid
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aids", required=True, help="Comma-separated arxiv IDs")
    ap.add_argument("--model", default="gemini", help="Model for second opinion (default: gemini)")
    ap.add_argument("--format", choices=["json", "table"], default="json")
    args = ap.parse_args()

    aids = [a.strip() for a in args.aids.split(",") if a.strip()]
    results = []
    for aid in aids:
        r = verify_paper(aid, args.model)
        results.append(r)
        verdict = r.get("verdict", "?")
        reasoning = r.get("reasoning", "")[:100]
        log(f"[2nd-opinion] {aid}: {verdict} — {reasoning}")

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"{'aid':<14} {'verdict':<10} reasoning")
        print("=" * 80)
        for r in results:
            print(f"{r['aid']:<14} {r.get('verdict', '?'):<10} {r.get('reasoning', '')[:60]}")

    # Summary
    n_confirm = sum(1 for r in results if r.get("verdict") == "CONFIRM")
    n_reject = sum(1 for r in results if r.get("verdict") == "REJECT")
    n_uncertain = sum(1 for r in results if r.get("verdict") not in ("CONFIRM", "REJECT"))
    log(f"\n[2nd-opinion] summary: {n_confirm} CONFIRM, {n_reject} REJECT, {n_uncertain} UNCERTAIN")


if __name__ == "__main__":
    main()
