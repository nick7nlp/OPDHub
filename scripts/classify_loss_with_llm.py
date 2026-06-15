#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loss-taxonomy classifier for the OPD survey.

Reads notes/paper_notes.json, picks every paper whose nested
opd_classification.is_opd == "yes" (or outer is_opd == "yes"), and asks the
configured LLM to assign one of the 7 mutually-exclusive loss classes defined
in data/loss_taxonomy_schema.json. The result is written to
data/loss_classification.json keyed by arxiv_id.

Default mode is incremental: papers already present in the output (with the
same loss_formulation hash) are skipped. Pass --rerun-all to force re-classify.

Usage:
    python scripts/classify_loss_with_llm.py                # incremental
    python scripts/classify_loss_with_llm.py --rerun-all    # full re-classify
    python scripts/classify_loss_with_llm.py --only 2604.14084 2605.07725
    python scripts/classify_loss_with_llm.py --workers 3
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Paths
ROOT = Path("/apdcephfs_cq8/share_1324356/nickmysong/daily_research/on-policy-distillation-survey")
PAPER_NOTES = ROOT / "notes" / "paper_notes.json"
SCHEMA_PATH = ROOT / "data" / "loss_taxonomy_schema.json"
OUTPUT_PATH = ROOT / "data" / "loss_classification.json"
LOG_PATH = ROOT / "data" / "loss_classification.log"

# llm_client lives in clawd/lib but its current /v1/messages signed-auth path
# is broken on this host; daily-pipeline workers call /v1/messages directly with
# the api-gateway Bearer token. Mirror that pattern here for parity.
sys.path.insert(0, os.path.expanduser("~/clawd/lib"))
from config import cfg  # noqa: E402
import requests  # noqa: E402

CLAUDE_MODELS = {
    "claude": "api_aws_third_anthropic.claude-opus-4-6-v1",
    "claude-opus": "api_aws_third_anthropic.claude-opus-4-6-v1",
    "claude-opus-4.6": "api_aws_third_anthropic.claude-opus-4-6-v1",
    "claude-opus-4.7": "api_aws_third_anthropic.claude-opus-4-7",
    "claude-sonnet": "api_aws_third_anthropic.claude-sonnet-4-6",
}


def call_claude(system_prompt: str, user_prompt: str, model: str = "claude", max_tokens: int = 2048) -> str:
    """Direct Anthropic Messages API call against the woa gateway."""
    api_key = f"{cfg['api']['user']}:{cfg['api']['apikey']}"
    model_id = CLAUDE_MODELS.get(model, model)
    url = f"{cfg['api']['host']}/v1/messages"
    payload = {
        "model": model_id,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    r = requests.post(url, json=payload, headers=headers, timeout=600)
    r.raise_for_status()
    data = r.json()
    for blk in data.get("content", []):
        if blk.get("type") == "text":
            return blk["text"]
    raise RuntimeError(f"no text block in response: {data}")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH, mode="a"),
    ],
)
log = logging.getLogger("loss-classifier")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_opd_yes(entry: Dict[str, Any]) -> bool:
    """True iff outer or nested classification marks the paper as OPD."""
    if entry.get("is_opd") == "yes":
        return True
    inner = entry.get("opd_classification") or {}
    return inner.get("is_opd") == "yes"


def loss_signature(entry: Dict[str, Any]) -> str:
    """Hash the loss-relevant fields, used to detect content changes."""
    method = entry.get("method") or {}
    payload = json.dumps({
        "loss_formulation": method.get("loss_formulation") or "",
        "training_loop": method.get("training_loop") or "",
        "key_components": method.get("key_components") or "",
        "distance_metric": method.get("distance_metric") or "",
    }, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def build_prompt(arxiv_id: str, entry: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[str, str]:
    """Return (system_prompt, user_prompt) for the classifier."""
    method = entry.get("method") or {}
    title = entry.get("title") or ""
    abstract = entry.get("abstract") or ""
    if len(abstract) > 1500:
        abstract = abstract[:1500] + " ..."

    classes_summary = []
    for c in schema["classes"]:
        classes_summary.append(
            f"- **{c['id']}** ({c['name']}): match when {c['what_to_match']}\n"
            f"    expression: `{c['expression']}`\n"
            f"    do NOT match: {c['do_not_match']}"
        )
    classes_block = "\n".join(classes_summary)
    rules_block = "\n".join(f"- {r}" for r in schema["tie_breaking_rules"])

    system_prompt = (
        "You are a careful machine-learning research auditor. Your task is to read "
        "ONE paper's loss formulation and decide which of seven mutually-exclusive "
        "OPD loss classes best describes its primary training objective. Be precise. "
        "Trust the equation over the prose if they disagree. Output ONLY a JSON object."
    )

    user_prompt = f"""Classify the dominant loss objective of this On-Policy Distillation paper.

# Taxonomy (pick exactly one id)
{classes_block}

# Tie-breaking rules
{rules_block}

# Paper
arxiv_id: {arxiv_id}
title: {title}
abstract: {abstract}

# Method record
training_loop: {method.get('training_loop') or '(empty)'}
loss_formulation (LaTeX): {method.get('loss_formulation') or '(empty)'}
distance_metric: {method.get('distance_metric') or '(empty)'}
key_components: {method.get('key_components') or '(empty)'}

# Output JSON schema (return ONLY this JSON, nothing else)
{{
  "loss_class": "FKL" | "RKL" | "Symmetric" | "f-Divergence" | "KL+RL" | "Preference" | "Other",
  "confidence": "high" | "medium" | "low",
  "evidence": "<<= 25 words pointing to the equation term that drove the decision>>",
  "secondary_class": "<id of a 2nd-best class, or null if obvious>",
  "notes": "<<= 25 words: any caveats, e.g. 'temperature-scaled FKL', 'GRPO with KL ref only no teacher'>>"
}}
"""
    return system_prompt, user_prompt


JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_response(raw: str) -> Optional[Dict[str, Any]]:
    """Extract the JSON object from the model output."""
    if not raw:
        return None
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    m = JSON_RE.search(raw)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


VALID_CLASSES = {"FKL", "RKL", "Symmetric", "f-Divergence", "KL+RL", "Preference", "Other"}


def validate_record(rec: Dict[str, Any]) -> Optional[str]:
    """Return error string if invalid, else None."""
    if rec.get("loss_class") not in VALID_CLASSES:
        return f"loss_class={rec.get('loss_class')!r} not in taxonomy"
    if rec.get("confidence") not in {"high", "medium", "low"}:
        return f"confidence={rec.get('confidence')!r} invalid"
    return None


# ---------------------------------------------------------------------------
# Per-paper classifier
# ---------------------------------------------------------------------------

def classify_one(
    arxiv_id: str,
    entry: Dict[str, Any],
    schema: Dict[str, Any],
    provider: str = "claude",
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Classify a single paper. Returns the record (with metadata)."""
    sys_prompt, user_prompt = build_prompt(arxiv_id, entry, schema)
    t0 = time.time()
    raw = call_claude(sys_prompt, user_prompt, model=model or "claude", max_tokens=2048)
    dur = time.time() - t0

    rec = parse_response(raw) or {}
    err = validate_record(rec) if rec else "no JSON in response"
    if err:
        log.warning("[%s] parse/validate failed: %s | raw[:200]=%s", arxiv_id, err, (raw or "")[:200])
        rec = {
            "loss_class": "Other",
            "confidence": "low",
            "evidence": "(LLM output unparseable)",
            "secondary_class": None,
            "notes": f"FALLBACK: {err}",
        }

    rec.update({
        "arxiv_id": arxiv_id,
        "title": entry.get("title", ""),
        "loss_signature": loss_signature(entry),
        "classified_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_s": round(dur, 1),
        "model": model or provider,
    })
    log.info("[%s] %s (%s, %.1fs) %s", arxiv_id, rec["loss_class"], rec["confidence"], dur, rec.get("evidence", "")[:80])
    return rec


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def load_existing() -> Dict[str, Any]:
    if OUTPUT_PATH.exists():
        with open(OUTPUT_PATH) as f:
            return json.load(f)
    return {"version": "v1", "results": {}}


def save_results(payload: Dict[str, Any]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT_PATH.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    tmp.replace(OUTPUT_PATH)


def select_targets(
    notes: Dict[str, Any],
    existing: Dict[str, Any],
    only: Optional[List[str]],
    rerun_all: bool,
) -> List[str]:
    candidates = [k for k, v in notes.items() if is_opd_yes(v)]
    if only:
        candidates = [k for k in candidates if k in set(only)]
    if rerun_all:
        return candidates
    out: List[str] = []
    results = existing.get("results", {})
    for k in candidates:
        prev = results.get(k)
        sig_now = loss_signature(notes[k])
        if not prev or prev.get("loss_signature") != sig_now:
            out.append(k)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun-all", action="store_true", help="ignore existing results, classify every is_opd=yes paper")
    ap.add_argument("--only", nargs="+", default=None, help="restrict to these arxiv ids")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--provider", default="claude")
    ap.add_argument("--model", default="claude",
                    help="model alias (claude / claude-opus-4.7 / claude-sonnet) or full id")
    ap.add_argument("--dry-run", action="store_true", help="just list what would be classified")
    args = ap.parse_args()

    with open(PAPER_NOTES) as f:
        notes_doc = json.load(f)
    notes = notes_doc.get("notes", notes_doc)  # tolerate either schema

    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    existing = load_existing()
    targets = select_targets(notes, existing, args.only, args.rerun_all)
    log.info("targets: %d (existing results: %d, total is_opd=yes: %d)",
             len(targets),
             len(existing.get("results", {})),
             sum(1 for v in notes.values() if is_opd_yes(v)))
    if args.dry_run:
        for k in targets:
            print(k, "-", notes[k].get("title", "")[:80])
        return

    if not targets:
        log.info("nothing to do.")
        return

    results = existing.get("results", {})
    completed = 0
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        future_to_id = {
            ex.submit(classify_one, k, notes[k], schema, args.provider, args.model): k
            for k in targets
        }
        for fut in cf.as_completed(future_to_id):
            arxiv_id = future_to_id[fut]
            try:
                rec = fut.result()
                results[arxiv_id] = rec
                completed += 1
                if completed % 10 == 0:
                    existing["results"] = results
                    existing["version"] = "v1"
                    existing["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    save_results(existing)
                    log.info("checkpoint: saved %d/%d", completed, len(targets))
            except Exception as e:  # noqa: BLE001
                log.error("[%s] worker failed: %s", arxiv_id, e)

    existing["results"] = results
    existing["version"] = "v1"
    existing["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    existing["taxonomy_schema_version"] = schema.get("version", "unknown")
    save_results(existing)
    log.info("done. wrote %d results to %s", len(results), OUTPUT_PATH)

    # quick distribution print
    from collections import Counter
    dist = Counter(r["loss_class"] for r in results.values())
    log.info("distribution: %s", dict(dist))


if __name__ == "__main__":
    main()
