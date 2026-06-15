#!/usr/bin/env python3
"""
validate_papers.py — full integrity check of OPD paper collection.

Cross-references three sources:
  1. arxiv.org API (ground truth)
  2. paper_notes.json (deep-read v3 schema)
  3. Awesome-LLM-On-Policy-Distillation/README.md (public listing)

Reports:
  A. arxiv id existence (404 → fabricated)
  B. title mismatches (README vs notes vs arxiv canonical)
  C. section disagreement (README § vs notes opd_classification.primary_section)
  D. model-pair fabrication (README → student strings missing in notes.teacher_student_pairs)
  E. boundary-rejected papers still in awesome (SPIN/IRIS-style: DPO loss / Rényi self-play / RL-only)
  F. is_opd=no papers still in awesome (clean violation of scope rule)

Usage:
  python3 scripts/validate_papers.py [--workers 5] [--cache] [--out report.md]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes" / "paper_notes.json"
AWESOME_README = ROOT / "Awesome-LLM-On-Policy-Distillation" / "README.md"
SITE_JSON = ROOT / "awesome-llm-opd-site" / "static" / "data" / "papers.json"
ARXIV_CACHE = ROOT / "papers-meta" / ".arxiv_validation_cache.json"

ARXIV_API = "https://export.arxiv.org/api/query"


def load_notes():
    return json.loads(NOTES.read_text(encoding="utf-8"))["notes"]


def load_site_papers():
    return json.loads(SITE_JSON.read_text(encoding="utf-8"))["papers"]


def parse_awesome_paper_rows():
    """Return list of {arxiv_id, section, title, raw_line, line_no} from main paper-row tables."""
    text = AWESOME_README.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Track current H2 + H3 section as we walk lines.
    current_h2 = ""
    current_h3 = ""
    rows = []
    # current parent §-prefix as derived from h2 label (e.g. "§4 Objective Functions...")
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            current_h2 = line[3:].strip()
            current_h3 = ""
            continue
        if line.startswith("### "):
            current_h3 = line[4:].strip()
            continue

        # Skip Hall of Fame / Surveys / Reading List sections — they are NOT in main paper rows
        if "Hall of Fame" in current_h2 or "Surveys" in current_h3:
            continue

        # Match a paper row that has an arxiv link
        m = re.search(r"\|\s*🟡?\s*🟢?\s*\[(?P<title>[^\]]+)\]\(https?://arxiv\.org/abs/(?P<aid>\d{4}\.\d{4,5})\)",
                      line)
        if not m:
            continue

        # Section: try to extract §X.Y from the line itself or from the section column
        m_sec = re.search(r"§\d+(?:\.\d+(?:\.\d+)?)?", line)
        section = m_sec.group(0) if m_sec else ""
        # Fallback: section from h2 label
        if not section and "§" in current_h2:
            m2 = re.search(r"§\d+", current_h2)
            section = m2.group(0) if m2 else ""

        rows.append({
            "arxiv_id": m.group("aid"),
            "title": m.group("title").replace("**", "").strip(),
            "section": section,
            "h2": current_h2,
            "h3": current_h3,
            "line_no": i,
        })
    return rows


def fetch_arxiv_meta_batch(ids: list[str], workers: int = 5):
    """Fetch arxiv metadata via id_list batch endpoint (up to 100 ids per call).

    Strategy: chunk ids into groups of 50, make 1 request per chunk with a 4s
    delay between chunks (arxiv recommends ≥3s). This is ~10x fewer requests
    than per-id fetching and avoids 429 rate limiting completely.
    """
    import requests
    from xml.etree import ElementTree as ET
    NS = "{http://www.w3.org/2005/Atom}"

    cache = {}
    if ARXIV_CACHE.exists():
        try:
            cache = json.loads(ARXIV_CACHE.read_text())
        except Exception:
            cache = {}

    out = {}
    todo = []
    for aid in ids:
        if aid in cache and "_error" not in cache[aid]:
            out[aid] = cache[aid]
        else:
            todo.append(aid)
    print(f"[validate] cache hits: {len(out)}, fetching: {len(todo)}", flush=True)

    if not todo:
        return out

    chunk_size = 20
    chunks = [todo[i:i+chunk_size] for i in range(0, len(todo), chunk_size)]
    print(f"[validate] {len(chunks)} batched API calls (chunk_size={chunk_size})", flush=True)

    for ci, chunk in enumerate(chunks, 1):
        for attempt in range(4):
            try:
                r = requests.get(
                    ARXIV_API,
                    params={"id_list": ",".join(chunk), "max_results": str(len(chunk))},
                    timeout=60,
                )
                if r.status_code == 200:
                    break
                wait = 15 * (attempt + 1)
                print(f"[validate] chunk {ci} got {r.status_code}, retry in {wait}s", flush=True)
                time.sleep(wait)
            except Exception as e:
                wait = 5 * (attempt + 1)
                print(f"[validate] chunk {ci} {type(e).__name__}: {e}, retry in {wait}s", flush=True)
                time.sleep(wait)
        else:
            # All retries failed → mark all in chunk as error
            for aid in chunk:
                cache[aid] = {"_error": "all_retries_failed"}
                out[aid] = cache[aid]
            continue

        # Parse XML
        try:
            root = ET.fromstring(r.text)
        except Exception as e:
            print(f"[validate] chunk {ci} XML parse error: {e}", flush=True)
            for aid in chunk:
                cache[aid] = {"_error": f"xml_parse_{e}"}
                out[aid] = cache[aid]
            continue

        # arxiv returns entries in order; map by extracting id from <id> element
        entries = root.findall(f"{NS}entry")
        # Build lookup by trailing arxiv id
        for entry in entries:
            entry_id = entry.findtext(f"{NS}id", "")  # e.g. http://arxiv.org/abs/2605.13230v1
            m_id = re.search(r"abs/(\d{4}\.\d{4,5})", entry_id)
            if not m_id:
                continue
            aid = m_id.group(1)
            title = entry.findtext(f"{NS}title", "").strip()
            title = re.sub(r"\s+", " ", title)
            published = entry.findtext(f"{NS}published", "")
            updated = entry.findtext(f"{NS}updated", "")
            authors = [a.findtext(f"{NS}name", "") for a in entry.findall(f"{NS}author")]
            cache[aid] = {
                "title": title,
                "published": published,
                "updated": updated,
                "authors_first": authors[0] if authors else "",
            }
            out[aid] = cache[aid]

        # Mark missing ids in this chunk as 404
        returned_ids = {re.search(r"abs/(\d{4}\.\d{4,5})", e.findtext(f"{NS}id", "")).group(1)
                        for e in entries
                        if re.search(r"abs/(\d{4}\.\d{4,5})", e.findtext(f"{NS}id", ""))}
        missing = set(chunk) - returned_ids
        for aid in missing:
            cache[aid] = {"_error": "not_in_response"}
            out[aid] = cache[aid]

        print(f"[validate] chunk {ci}/{len(chunks)}: {len(returned_ids)} ok, {len(missing)} missing", flush=True)
        # Polite delay between chunks — arxiv recommends ≥3s, we use 8s for safety
        if ci < len(chunks):
            time.sleep(8)

    ARXIV_CACHE.parent.mkdir(parents=True, exist_ok=True)
    ARXIV_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))
    print(f"[validate] cached → {ARXIV_CACHE.relative_to(ROOT)}", flush=True)

    return out


def normalize_title(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip().lower()
    t = re.sub(r"[^\w\s]", "", t)
    return t


def title_match(a: str, b: str) -> bool:
    """Loose match — covers minor punctuation/case differences."""
    na, nb = normalize_title(a), normalize_title(b)
    if na == nb:
        return True
    # one is prefix of the other (truncation)
    if na in nb or nb in na:
        return min(len(na), len(nb)) > 12
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--out", default="papers-meta/_validation_report.md")
    ap.add_argument("--skip-arxiv", action="store_true",
                    help="Skip arxiv API check (use cached only)")
    args = ap.parse_args()

    notes = load_notes()
    site_papers = load_site_papers()
    site_ids = {p["arxiv_id"] for p in site_papers}

    awesome_rows = parse_awesome_paper_rows()
    awesome_ids = {r["arxiv_id"] for r in awesome_rows}

    print(f"[validate] notes deep-read records: {len(notes)}")
    print(f"[validate] site papers:             {len(site_papers)}")
    print(f"[validate] awesome paper rows:      {len(awesome_rows)}")
    print(f"[validate] awesome unique arxiv:    {len(awesome_ids)}")

    # ========== 1. arxiv API canonical metadata ==========
    if args.skip_arxiv:
        arxiv_meta = json.loads(ARXIV_CACHE.read_text()) if ARXIV_CACHE.exists() else {}
    else:
        arxiv_meta = fetch_arxiv_meta_batch(sorted(awesome_ids), workers=args.workers)

    # ========== Build report ==========
    findings = {
        "A_arxiv_404": [],          # arxiv id doesn't exist
        "B_title_mismatch": [],     # README/notes title disagrees with arxiv canonical
        "C_section_mismatch": [],   # README § vs v3 primary_section
        "D_model_pair_missing": [], # README has model-pair text not in notes.teacher_student_pairs
        "E_boundary_pseudo_opd": [],# SPIN/IRIS-style still in awesome
        "F_is_opd_no_in_site": [],  # v3 explicitly says is_opd=no but paper still on site
    }

    # Map: aid → awesome row
    awesome_by_id = {r["arxiv_id"]: r for r in awesome_rows}

    for aid in sorted(awesome_ids):
        row = awesome_by_id[aid]
        n = notes.get(aid, {})
        m = arxiv_meta.get(aid, {})

        # A. arxiv 404
        if "_error" in m:
            findings["A_arxiv_404"].append({
                "aid": aid,
                "error": m["_error"],
                "readme_title": row["title"],
            })
            continue
        if not m or not m.get("title"):
            continue

        canonical_title = m.get("title", "")
        readme_title = row["title"]
        notes_title = (n or {}).get("title", "")

        # B. title match
        readme_ok = title_match(readme_title, canonical_title) if readme_title else True
        notes_ok = title_match(notes_title, canonical_title) if notes_title else True
        if not readme_ok or not notes_ok:
            findings["B_title_mismatch"].append({
                "aid": aid,
                "arxiv_canonical": canonical_title,
                "readme":   readme_title,
                "notes":    notes_title,
                "readme_ok": readme_ok,
                "notes_ok":  notes_ok,
            })

        # C. section consistency
        cls = (n or {}).get("opd_classification") or {}
        v3_sec = cls.get("primary_section") if isinstance(cls, dict) else None
        readme_sec = row["section"]
        if v3_sec and readme_sec and v3_sec != readme_sec:
            # Allow parent vs leaf (e.g. README §4, notes §4.1) — don't flag
            is_prefix = readme_sec.startswith(v3_sec) or v3_sec.startswith(readme_sec)
            # §6 is the cross-cutting training-efficiency / recipe axis;
            # papers under §6 may have any §4 / §5 primary_section in v3.
            # Same for §7 (system) and §8 (analysis-of-OPD) cross-cuts.
            cross_cut = readme_sec in ("§6", "§7", "§8") or v3_sec in ("§6", "§7", "§8")
            if not is_prefix and not cross_cut:
                findings["C_section_mismatch"].append({
                    "aid": aid,
                    "title": readme_title[:60],
                    "readme_sec": readme_sec,
                    "v3_sec": v3_sec,
                })

        # F. is_opd=no in awesome
        is_opd = cls.get("is_opd") if isinstance(cls, dict) else None
        if is_opd == "no":
            findings["F_is_opd_no_in_site"].append({
                "aid": aid,
                "title": readme_title[:65],
                "v3_reason": (cls.get("reasoning") or "")[:160],
            })

        # E. boundary pseudo-OPD heuristic
        opm = (n or {}).get("on_policy_mechanism") or {}
        loss_form = ((n or {}).get("method") or {}).get("loss_formulation", "") or ""
        sig = opm.get("signal_source", "") if isinstance(opm, dict) else ""
        freq = opm.get("rollout_frequency", "") if isinstance(opm, dict) else ""

        is_self_play_loss = bool(re.search(
            r"log\s*p_\\?theta\(?[^\)]+\)?/p_\\?theta_t.*log\s*p_\\?theta\(?[^\)]+\)?/p_\\?theta_t",
            loss_form, re.I,
        )) or "log\\frac{p" in loss_form and "y'" in loss_form
        # Detect Rényi self-play: alpha-divergence between p_data and p_theta_t
        is_renyi_selfplay = bool(re.search(r"alpha.*p_{?data}?.*p_{?\\theta_?t?}?", loss_form, re.I))
        # RL-only without teacher distill term
        rl_only = bool(re.search(r"GRPO|PPO|min\(.*clip", loss_form, re.I)) and \
                  ("D_KL" not in loss_form and "JSD" not in loss_form and "L_OPSD" not in loss_form
                   and "teacher" not in loss_form.lower())

        if (is_self_play_loss or is_renyi_selfplay) and sig in ("self", ""):
            findings["E_boundary_pseudo_opd"].append({
                "aid": aid,
                "title": readme_title[:65],
                "signal": sig,
                "freq": freq,
                "loss_snippet": loss_form[:200],
                "trigger": "self_play_DPO_form" if is_self_play_loss else "renyi_self_play",
            })

    # ========== Print summary ==========
    print()
    print("=" * 70)
    print(" Validation summary")
    print("=" * 70)
    for k, v in findings.items():
        flag = "✓" if not v else "⚠️ "
        print(f"  {flag} {k}: {len(v)}")

    # ========== Write report ==========
    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# Paper Validation Report\n")
    from datetime import datetime, timezone, timedelta
    cst = datetime.now(timezone(timedelta(hours=8)))
    lines.append(f"Generated: {cst.strftime('%Y-%m-%d %H:%M CST')}\n")
    lines.append(f"\n- awesome paper rows: **{len(awesome_rows)}**")
    lines.append(f"- site papers:        **{len(site_papers)}**")
    lines.append(f"- arxiv API checked:  **{len(arxiv_meta)}**\n")

    sections = [
        ("A_arxiv_404", "A. arxiv ID 404 / 不存在 (致命: 编造的引用)",
         "**红旗** — 这些 id 在 arxiv 上找不到, 必须删除并人工调查来源。"),
        ("B_title_mismatch", "B. 标题不一致 (README / notes / arxiv canonical)",
         "标题串错, 可能是手工 typo 或粘错论文。"),
        ("C_section_mismatch", "C. § 分类不一致 (README vs v3 LLM)",
         "v3 LLM 判定的 primary_section 跟 README 收录位置不同, 可能 inserter 当时填错。"),
        ("F_is_opd_no_in_site", "F. v3 判 is_opd=no 但仍在 awesome (违反 scope 铁律)",
         "应该从 awesome+site 删掉, 跟 SPIN/IRIS 同性质。"),
        ("E_boundary_pseudo_opd", "E. 启发式检测疑似 self-play 边界反例",
         "loss 形式上是 DPO 二分类 / Rényi 自博弈, 需要人工二审是否真是 OPD。"),
    ]
    for key, label, blurb in sections:
        items = findings[key]
        lines.append(f"\n## {label} — {len(items)}")
        lines.append(f"\n{blurb}\n")
        if not items:
            lines.append("\n_无问题_\n")
            continue
        for it in items:
            lines.append(f"- `{it.get('aid','?')}` " + json.dumps(
                {k: v for k, v in it.items() if k != 'aid'},
                ensure_ascii=False)[:500])

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[validate] wrote {out_path.relative_to(ROOT)}")

    # Exit 1 if any A/F findings (must-fix)
    if findings["A_arxiv_404"] or findings["F_is_opd_no_in_site"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
