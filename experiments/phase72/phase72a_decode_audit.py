#!/usr/bin/env python3
"""Phase72A: source-only feasibility audit of real historical ciphertexts.

This program never imports the Voynich scoring modules and contains no S1/S2/S3/H62
implementation. It audits an independently maintained DECODE metadata snapshot and,
optionally, the public DECODE REST record-detail endpoint.

Usage:
  python experiments/phase72/phase72a_decode_audit.py \
      /path/to/Decode2LOD/populated_decryptontology.ttl \
      --out phase72a_audit.json \
      --details-out phase72a_external_details.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import requests
from rdflib import Graph, Namespace, RDF

DECRYPT = Namespace("https://de-crypt.org/r/")
API_BASE = "https://de-crypt.org/decrypt-web/api"
START_YEAR_MIN = 1400
START_YEAR_MAX = 1600
MAX_DETAIL_RECORDS = 500
REQUEST_DELAY_SECONDS = 0.05


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def one(g: Graph, subj, pred) -> str | None:
    values = [str(x) for x in g.objects(subj, pred)]
    if not values:
        return None
    return values[0] if len(values) == 1 else " | ".join(sorted(set(values)))


def int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        m = re.search(r"\b(1[0-9]{3})\b", value)
        return int(m.group(1)) if m else None


def extract_metadata(ttl_path: Path) -> Tuple[List[dict], dict]:
    g = Graph()
    g.parse(ttl_path, format="turtle")
    subjects = sorted(set(g.subjects(RDF.type, DECRYPT.Record)), key=str)
    rows: List[dict] = []
    for s in subjects:
        row = {
            "uri": str(s),
            "id": one(g, s, DECRYPT.hasID),
            "name": one(g, s, DECRYPT.hasName),
            "start_year": int_or_none(one(g, s, DECRYPT.hasStartYear)),
            "creation_date": one(g, s, DECRYPT.hasCreationDate),
            "record_type": one(g, s, DECRYPT.hasRecordType),
            "cipher_types": one(g, s, DECRYPT.hasCipherTypes),
            "symbol_sets": one(g, s, DECRYPT.hasSymbolSets),
            "status": one(g, s, DECRYPT.hasStatus),
            "private_ciphertext": one(g, s, DECRYPT.hasPrivateCiphertext),
            "number_of_pages": int_or_none(one(g, s, DECRYPT.hasNumberOfPages)),
            "cleartext_lang": one(g, s, DECRYPT.hasCleartextLanguage),
            "author": one(g, s, DECRYPT.hasAuthor),
            "current_country": one(g, s, DECRYPT.hasCurrentCountry),
            "current_city": one(g, s, DECRYPT.hasCurrentCity),
            "current_holder": one(g, s, DECRYPT.hasCurrentHolder),
            "additional_information": one(g, s, DECRYPT.hasAdditionalInformation),
        }
        rows.append(row)

    distributions = {
        "record_type": Counter((r["record_type"] or "<NULL>") for r in rows),
        "status": Counter((r["status"] or "<NULL>") for r in rows),
        "cipher_types": Counter((r["cipher_types"] or "<NULL>") for r in rows),
        "symbol_sets": Counter((r["symbol_sets"] or "<NULL>") for r in rows),
        "country": Counter((r["current_country"] or "<NULL>") for r in rows),
    }
    return rows, {k: dict(v.most_common()) for k, v in distributions.items()}


def is_public_ciphertext(row: dict) -> bool:
    year = row.get("start_year")
    if year is None or not (START_YEAR_MIN <= year <= START_YEAR_MAX):
        return False
    rt = (row.get("record_type") or "").lower()
    if not ("cipher" in rt or "crypt" in rt):
        return False
    if "key" in rt and "ciphertext" not in rt:
        return False
    priv = (row.get("private_ciphertext") or "").strip().lower()
    if priv in {"true", "1", "yes"}:
        return False
    return bool(row.get("id"))


def walk(value: Any, path: str = "") -> Iterable[Tuple[str, Any]]:
    if isinstance(value, dict):
        for k, v in value.items():
            p = f"{path}.{k}" if path else str(k)
            yield p, v
            yield from walk(v, p)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            p = f"{path}[{i}]"
            yield p, v
            yield from walk(v, p)


def detail_signature(detail: Any) -> dict:
    field_paths = []
    text_candidates = []
    boundary_candidates = []
    for path, value in walk(detail):
        leaf = path.lower()
        if any(x in leaf for x in ("transcript", "ciphertext", "cleartext", "plaintext", "decrypt")):
            field_paths.append(path)
            if isinstance(value, str):
                text_candidates.append({
                    "path": path,
                    "chars": len(value),
                    "lines": value.count("\n") + (1 if value else 0),
                    "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
                })
        if any(x in leaf for x in ("line", "page", "message", "paragraph", "segment")):
            if isinstance(value, (str, int, float, bool)) or value is None:
                boundary_candidates.append({"path": path, "value_type": type(value).__name__})
            elif isinstance(value, (list, dict)):
                boundary_candidates.append({"path": path, "value_type": type(value).__name__, "size": len(value)})
    return {
        "all_top_level_keys": sorted(detail.keys()) if isinstance(detail, dict) else [],
        "relevant_field_paths": sorted(set(field_paths)),
        "text_candidates": text_candidates,
        "boundary_candidate_paths": boundary_candidates[:200],
        "has_machine_readable_text_candidate": any(x["chars"] >= 20 for x in text_candidates),
        "has_multiline_text_candidate": any(x["lines"] >= 2 and x["chars"] >= 20 for x in text_candidates),
        "detail_sha256": hashlib.sha256(
            json.dumps(detail, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
    }


def fetch_detail(session: requests.Session, record_id: str) -> Tuple[Any | None, str | None]:
    url = f"{API_BASE}/view/records/{record_id}"
    last_error = None
    for attempt in range(3):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            return r.json(), None
        except Exception as exc:  # source audit: preserve error and retry boundedly
            last_error = f"{type(exc).__name__}: {exc}"
            time.sleep(0.5 * (attempt + 1))
    return None, last_error


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ttl")
    ap.add_argument("--out", required=True)
    ap.add_argument("--details-out", required=True)
    ap.add_argument("--skip-live-details", action="store_true")
    args = ap.parse_args()

    ttl_path = Path(args.ttl).resolve()
    rows, distributions = extract_metadata(ttl_path)
    candidates = sorted(
        [r for r in rows if is_public_ciphertext(r)],
        key=lambda r: (r["start_year"], str(r["id"])),
    )

    if len(candidates) > MAX_DETAIL_RECORDS:
        live_candidates = candidates[:MAX_DETAIL_RECORDS]
        detail_truncated = True
    else:
        live_candidates = candidates
        detail_truncated = False

    external_details: Dict[str, Any] = {}
    detail_summaries = []
    errors = []
    if not args.skip_live_details:
        session = requests.Session()
        session.headers.update({"User-Agent": "LETSGO-Voynich-Phase72-source-audit/1.0"})
        for i, row in enumerate(live_candidates):
            rid = str(row["id"])
            detail, error = fetch_detail(session, rid)
            if error:
                errors.append({"id": rid, "error": error})
            else:
                external_details[rid] = detail
                sig = detail_signature(detail)
                detail_summaries.append({
                    "id": rid,
                    "start_year": row["start_year"],
                    "name": row["name"],
                    "record_type": row["record_type"],
                    "cipher_types": row["cipher_types"],
                    "symbol_sets": row["symbol_sets"],
                    "country": row["current_country"],
                    "holder": row["current_holder"],
                    **sig,
                })
            if i + 1 < len(live_candidates):
                time.sleep(REQUEST_DELAY_SECONDS)

    transcribed = [x for x in detail_summaries if x["has_machine_readable_text_candidate"]]
    multiline = [x for x in detail_summaries if x["has_multiline_text_candidate"]]
    family_groups = sorted(set(
        (x.get("cipher_types") or "<NULL>")
        for x in transcribed
    ))
    holders = sorted(set(
        (x.get("holder") or x.get("country") or "<NULL>")
        for x in transcribed
    ))

    if len(transcribed) >= 10 and len(family_groups) >= 2 and len(multiline) >= 5:
        feasibility = "P72-EXT READY"
    elif len(transcribed) >= 10:
        feasibility = "P72-EXT TRANSCRIPTION READY / BOUNDARY BLOCKED"
    else:
        feasibility = "P72-EXT UNDERPOWERED"

    audit = {
        "phase": "72A",
        "status": "SOURCE_FEASIBILITY_ONLY_NO_VOYNICH_SCORE",
        "authority": {
            "ttl_path_name": ttl_path.name,
            "ttl_sha256": sha256_file(ttl_path),
            "api_base": API_BASE,
        },
        "filters": {
            "start_year_min": START_YEAR_MIN,
            "start_year_max": START_YEAR_MAX,
            "record_type_contains_cipher_or_crypt": True,
            "exclude_key_only_when_identifiable": True,
            "exclude_private_true": True,
        },
        "metadata": {
            "all_records": len(rows),
            "distributions": distributions,
            "candidate_records": len(candidates),
            "candidates": candidates,
        },
        "live_detail_audit": {
            "attempted": len(live_candidates) if not args.skip_live_details else 0,
            "candidate_cap": MAX_DETAIL_RECORDS,
            "truncated_by_cap": detail_truncated,
            "successes": len(detail_summaries),
            "errors": errors,
            "records_with_text_candidate": len(transcribed),
            "records_with_multiline_text_candidate": len(multiline),
            "text_candidate_cipher_family_groups": family_groups,
            "text_candidate_holder_or_country_groups": holders,
            "detail_summaries": detail_summaries,
        },
        "feasibility_classification": feasibility,
        "scientific_metrics_called": False,
        "next_gate": "Freeze exact record population/parser/boundary/statistic in PLAN_B.md before any external-cipher S1 score.",
    }

    Path(args.out).write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.details_out).write_text(json.dumps(external_details, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "all_records": len(rows),
        "candidate_records": len(candidates),
        "detail_successes": len(detail_summaries),
        "detail_errors": len(errors),
        "records_with_text_candidate": len(transcribed),
        "records_with_multiline_text_candidate": len(multiline),
        "cipher_family_groups": len(family_groups),
        "holder_or_country_groups": len(holders),
        "classification": feasibility,
        "scientific_metrics_called": False,
    }, indent=2))
    print("NO PHASE72 VOYNICH SCIENTIFIC SCORE COMPUTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
