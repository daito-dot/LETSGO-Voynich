#!/usr/bin/env python3
"""Phase72B source-only audit of open historical records in cipher_benchmark.

No Voynich scorer is imported and no S1/S2/S3/H62 value is computed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

MAX_YEAR = 1900


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_jsonl(path: Path) -> List[dict]:
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except Exception as exc:
            raise RuntimeError(f"manifest JSON error line {n}: {exc}") from exc
    return out


def page_key(value: Any, fallback: str) -> Tuple[int, int, str]:
    s = "" if value is None else str(value).strip().lower()
    m = re.search(r"(\d+)([rvab]?)", s)
    if not m:
        return (10**9, 9, s or fallback)
    side = {"": 0, "r": 0, "a": 0, "v": 1, "b": 1}.get(m.group(2), 2)
    return (int(m.group(1)), side, s)


def declared_transcription(record: dict, root: Path) -> Tuple[str | None, Path | None, List[Path]]:
    """Resolve the manifest transcription path under the frozen two-base rule.

    The benchmark manifest stores paths relative to benchmark/ for its bundled
    sources, while some compatible manifests may use repository-relative paths.
    This source-only compatibility rule was frozen before any Voynich score.
    """
    for field in ("transcription_canonical_file", "transcription_diplomatic_file"):
        rel = record.get(field)
        if not rel:
            continue
        candidates = [root / rel, root / "benchmark" / rel]
        for path in candidates:
            if path.is_file():
                return field, path, candidates
        return field, candidates[-1], candidates
    return None, None, []


def nonempty_lines(text: str) -> List[str]:
    return [x.strip() for x in text.splitlines() if x.strip()]


def ws_tokens(line: str) -> List[str]:
    return [x for x in re.split(r"\s+", line.strip()) if x]


def line_shape(text: str) -> dict:
    lines = nonempty_lines(text)
    counts = [len(ws_tokens(x)) for x in lines]
    base = len(lines) >= 3 and counts[0] >= 5 and counts[2] >= 5
    pseudos = [
        j for j in range(1, max(1, len(lines) - 2))
        if j + 2 < len(lines) and counts[j] >= 5 and counts[j + 2] >= 5
    ]
    return {
        "nonempty_lines": len(lines),
        "whitespace_tokens_total": sum(counts),
        "whitespace_token_counts_by_line": counts,
        "line0_and_line2_ge5": base,
        "valid_internal_j_to_jplus2_indices": pseudos,
        "entry_shape_eligible": bool(base and pseudos),
        "characters_nonspace": sum(sum(not c.isspace() for c in x) for x in lines),
    }


def date_ok(record: dict) -> bool:
    latest = record.get("date_latest_year")
    if latest is None:
        return True
    try:
        return int(latest) <= MAX_YEAR
    except Exception:
        return False


def source_record_group(record: dict) -> str:
    sr = record.get("source_record_id")
    return str(sr) if sr not in (None, "") else str(record.get("id"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("benchmark_root")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.benchmark_root).resolve()
    manifest = root / "benchmark" / "manifest" / "records.jsonl"
    schema = root / "benchmark" / "manifest" / "schema.json"
    records = load_jsonl(manifest)

    filtered = []
    missing_declared = []
    rights = Counter()
    sources_all = Counter()
    resolution_modes = Counter()
    for r in records:
        rights[str(r.get("rights_class"))] += 1
        sources_all[str(r.get("source"))] += 1
        if bool(r.get("synthetic", False)):
            continue
        if r.get("rights_class") != "open":
            continue
        if not date_ok(r):
            continue
        field, path, attempted = declared_transcription(r, root)
        if field is None or path is None:
            continue
        if not path.is_file():
            missing_declared.append({
                "id": r.get("id"),
                "field": field,
                "declared_path": r.get(field),
                "attempted_paths": [str(x.relative_to(root)) for x in attempted],
            })
            continue
        rel_resolved = str(path.relative_to(root))
        if rel_resolved.startswith("benchmark/"):
            resolution_modes["benchmark_relative"] += 1
        else:
            resolution_modes["repository_relative"] += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        filtered.append({
            "id": r.get("id"),
            "source": r.get("source"),
            "source_record_id": r.get("source_record_id"),
            "source_group_key": source_record_group(r),
            "status": r.get("status"),
            "rights_class": r.get("rights_class"),
            "synthetic": bool(r.get("synthetic", False)),
            "cipher_type": r.get("cipher_type"),
            "plaintext_language": r.get("plaintext_language"),
            "date_or_century": r.get("date_or_century"),
            "date_earliest_year": r.get("date_earliest_year"),
            "date_latest_year": r.get("date_latest_year"),
            "manuscript_page": r.get("manuscript_page"),
            "word_boundaries": r.get("word_boundaries"),
            "transcription_field": field,
            "transcription_declared_path": r.get(field),
            "transcription_file": rel_resolved,
            "transcription_sha256": sha256_file(path),
            "line_shape": line_shape(text),
            "source_url": r.get("source_url"),
            "provenance": r.get("provenance"),
            "upstream_provenance": r.get("upstream_provenance"),
            "notes": r.get("notes"),
        })

    groups: Dict[Tuple[str, str], List[dict]] = defaultdict(list)
    for row in filtered:
        groups[(str(row["source"]), row["source_group_key"])].append(row)

    first_entries = []
    for (source, group_key), rows in sorted(groups.items()):
        ordered = sorted(rows, key=lambda x: page_key(x.get("manuscript_page"), str(x.get("id"))))
        first = ordered[0]
        first_entries.append({
            **first,
            "group_record_count": len(rows),
            "group_record_ids": [x["id"] for x in ordered],
            "first_page_by_frozen_manifest_page_order": True,
        })

    eligible_entries = [x for x in first_entries if x["line_shape"]["entry_shape_eligible"]]
    source_entry_counts = Counter(str(x["source"]) for x in first_entries)
    source_eligible_counts = Counter(str(x["source"]) for x in eligible_entries)
    source_record_counts = Counter(str(x["source"]) for x in filtered)

    if (
        len(first_entries) >= 20
        and len(source_entry_counts) >= 2
        and len(eligible_entries) >= 10
        and len(source_eligible_counts) >= 2
    ):
        classification = "P72-BENCH READY"
    elif len(first_entries) >= 20:
        classification = "P72-BENCH TEXT READY / ENTRY-SHAPE BLOCKED"
    else:
        classification = "P72-BENCH UNDERPOWERED"

    out = {
        "phase": "72B",
        "status": "SOURCE_FEASIBILITY_ONLY_NO_VOYNICH_SCORE",
        "authority": {
            "benchmark_root_name": root.name,
            "manifest_git_blob_expected": "9dfedda0597185eda64e8166535fa1d0aa0898f5",
            "schema_git_blob_expected": "f07533cce267bb17110c8a3327385d7e586eee20",
            "manifest_sha256": sha256_file(manifest),
            "schema_sha256": sha256_file(schema),
        },
        "source_path_compatibility": {
            "rule": ["repository_relative", "benchmark_relative"],
            "resolution_mode_counts": dict(resolution_modes.most_common()),
            "first_zero_record_audit_disposition": "SOURCE_PATH_BASE_MISMATCH_NOT_UNDERPOWERED",
        },
        "filters": {
            "synthetic_false_or_absent": True,
            "rights_class": "open",
            "transcription_declared_and_exists": True,
            "date_latest_year_max_when_present": MAX_YEAR,
            "transcription_preference": ["transcription_canonical_file", "transcription_diplomatic_file"],
        },
        "manifest_inventory": {
            "all_records": len(records),
            "rights_distribution": dict(rights.most_common()),
            "source_distribution_all": dict(sources_all.most_common()),
            "declared_transcription_missing_on_disk": missing_declared,
        },
        "historical_open_transcribed_records": {
            "count": len(filtered),
            "source_counts": dict(source_record_counts.most_common()),
            "records": filtered,
        },
        "source_record_first_entries": {
            "count": len(first_entries),
            "source_counts": dict(source_entry_counts.most_common()),
            "entries": first_entries,
        },
        "entry_shape_eligible_first_entries": {
            "count": len(eligible_entries),
            "source_counts": dict(source_eligible_counts.most_common()),
            "entries": eligible_entries,
        },
        "feasibility_classification": classification,
        "scientific_metrics_called": False,
        "next_gate": "If READY, freeze exact source-record IDs, parser, boundary rule, representation and statistic in PLAN_C.md before any historical-cipher vs Voynich S1 score.",
    }
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "manifest_records": len(records),
        "historical_open_transcribed_records": len(filtered),
        "source_collections_with_records": len(source_record_counts),
        "source_record_first_entries": len(first_entries),
        "source_collections_with_entries": len(source_entry_counts),
        "entry_shape_eligible_first_entries": len(eligible_entries),
        "source_collections_with_eligible_entries": len(source_eligible_counts),
        "source_record_counts": dict(source_record_counts.most_common()),
        "source_eligible_counts": dict(source_eligible_counts.most_common()),
        "path_resolution_modes": dict(resolution_modes.most_common()),
        "missing_declared_transcriptions": len(missing_declared),
        "classification": classification,
        "scientific_metrics_called": False,
    }, ensure_ascii=False, indent=2))
    print("NO PHASE72 VOYNICH SCIENTIFIC SCORE COMPUTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
