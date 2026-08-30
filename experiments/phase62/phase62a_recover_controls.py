#!/usr/bin/env python3
"""Audit/recover Phase59 controls and enumerate objective Phase62 candidates.

This script is deliberately descriptive. It does NOT score N0/B0 against
Voynich and therefore cannot expose the Phase62 tournament outcome.

Usage:
    python experiments/phase62/phase62a_recover_controls.py /path/to/CREMMA-Medieval-LAT

The external checkout must be pinned to:
    HTR-United/CREMMA-Medieval-LAT
    292525969ad98380b398e6606a9c2a36d51913ae
"""
from __future__ import annotations

import hashlib
import json
import sys
import unicodedata
from pathlib import Path

EXTERNAL_REPO = "HTR-United/CREMMA-Medieval-LAT"
EXTERNAL_COMMIT = "292525969ad98380b398e6606a9c2a36d51913ae"
CORPUS_WIDE_MIN_ELIGIBLE = 5

# Historical Phase59 development groups. These counts are exposed and are used
# only to audit recoverability, never to choose a new subset by Voynich fit.
HISTORICAL_GROUPS = {
    "H318_recipe": {
        "expected_n": 3,
        "files": ["data/H318/10r.txt"],
        "selection_status": "file identified from the Phase59 recipe context; exact historical item subset was not stored",
    },
    "CLM13027_39r_treatment": {
        "expected_n": 3,
        "files": ["data/CLM13027/39r.txt"],
        "selection_status": "exact page named in Phase59 result key; exact historical item subset was not stored",
    },
    "CLM13027_41r_41v_medical_discussion": {
        "expected_n": 9,
        "files": ["data/CLM13027/41r.txt", "data/CLM13027/41v.txt"],
        "selection_status": "exact pages named in Phase59 result key; exact historical item subset was not stored",
    },
    "UBL758_ecclesiastical": {
        "expected_n": 5,
        "glob": "data/UBL758/*.txt",
        "selection_status": "historical page subset was not recorded; enumerate without choosing by Voynich fit",
    },
    "BIS193_scholastic": {
        "expected_n": 5,
        "glob": "data/BIS-193/*.txt",
        "selection_status": "historical five-entry subset was not recorded; enumerate without choosing by Voynich fit",
    },
}

# These five manuscripts were fixed in Phase52 before the Phase62 tournament.
PHASE52_PANEL = {
    "Arras861_literary": "data/Arras-861/*.txt",
    "CLM13027_medical": "data/CLM13027/*.txt",
    "H318_medical_recipes": "data/H318/*.txt",
    "UBL758_ecclesiastical": "data/UBL758/*.txt",
    "BIS193_scholastic": "data/BIS-193/*.txt",
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def unicode_lm_tokens(text: str) -> list[str]:
    """NFC maximal Letter/Mark sequences; no abbreviation expansion."""
    text = unicodedata.normalize("NFC", text)
    out: list[str] = []
    cur: list[str] = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("M"):
            cur.append(ch)
        else:
            if cur:
                out.append("".join(cur).lower())
                cur = []
    if cur:
        out.append("".join(cur).lower())
    return out


def marker_entries(path: Path, root: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    entries: list[dict] = []
    for i, line in enumerate(lines):
        if "¶" not in line:
            continue
        parts = line.split("¶")
        for j, after in enumerate(parts[1:], start=1):
            line0 = after
            line1 = lines[i + 1] if i + 1 < len(lines) else ""
            line2 = lines[i + 2] if i + 2 < len(lines) else ""
            t0 = unicode_lm_tokens(line0)
            t1 = unicode_lm_tokens(line1)
            t2 = unicode_lm_tokens(line2)
            entries.append(
                {
                    "path": str(path.relative_to(root)),
                    "source_line_1based": i + 1,
                    "marker_index_on_line": j,
                    "entry_id": f"{path.relative_to(root)}:{i+1}:pilcrow{j}",
                    "token_counts_line0_line1_line2": [len(t0), len(t1), len(t2)],
                    "eligible_phase62": bool(len(t0) >= 5 and len(t2) >= 5),
                    "line0_preview": " ".join(t0[:12]),
                    "line1_preview": " ".join(t1[:8]),
                    "line2_preview": " ".join(t2[:8]),
                }
            )
    return entries


def audit_file(path: Path, root: Path) -> dict:
    data = path.read_bytes()
    entries = marker_entries(path, root)
    return {
        "path": str(path.relative_to(root)),
        "bytes": len(data),
        "git_blob_sha1": git_blob_sha1(data),
        "pilcrow_markers": len(entries),
        "eligible_entries": sum(e["eligible_phase62"] for e in entries),
        "entries": entries,
    }


def audit_paths(paths: list[Path], root: Path, include_manifest: bool = True) -> dict:
    audits = [audit_file(p, root) for p in sorted(paths)]
    eligible = [e for a in audits for e in a["entries"] if e["eligible_phase62"]]
    out = {
        "scanned_file_count": len(audits),
        "files_with_pilcrows": sum(bool(a["pilcrow_markers"]) for a in audits),
        "pilcrow_markers": sum(a["pilcrow_markers"] for a in audits),
        "eligible_entries": len(eligible),
        "eligible_by_file": {a["path"]: a["eligible_entries"] for a in audits if a["eligible_entries"]},
        "source_blobs_with_eligible_entries": {a["path"]: a["git_blob_sha1"] for a in audits if a["eligible_entries"]},
    }
    if include_manifest:
        out["eligible_entry_ids"] = [e["entry_id"] for e in eligible]
    return out


def contiguous_windows(files: list[dict], expected: int, limit: int = 50) -> list[dict]:
    arr = sorted(files, key=lambda x: x["path"])
    out = []
    for i in range(len(arr)):
        total = 0
        for j in range(i, len(arr)):
            total += arr[j]["eligible_entries"]
            if total == expected:
                out.append({"files": [x["path"] for x in arr[i:j+1]], "eligible_entries": total})
                if len(out) >= limit:
                    return out
            if total > expected:
                break
    return out


def resolve_historical_group(root: Path, spec: dict) -> dict:
    if "files" in spec:
        paths = [root / x for x in spec["files"]]
    else:
        paths = sorted(root.glob(spec["glob"]))
    missing = [str(p.relative_to(root)) for p in paths if not p.exists()]
    audits = [audit_file(p, root) for p in paths if p.exists()]
    with_markers = [a for a in audits if a["pilcrow_markers"]]
    expected = spec["expected_n"]
    return {
        "expected_phase59_n": expected,
        "selection_status": spec["selection_status"],
        "missing_files": missing,
        "scanned_file_count": len(audits),
        "files_with_pilcrows": with_markers,
        "eligible_total_across_scanned_files": sum(a["eligible_entries"] for a in audits),
        "single_file_count_matches": [a["path"] for a in with_markers if a["eligible_entries"] == expected],
        "contiguous_filename_windows_summing_to_expected": contiguous_windows(with_markers, expected),
    }


def corpus_wide(root: Path) -> dict:
    rows = {}
    for d in sorted((root / "data").iterdir()):
        if not d.is_dir():
            continue
        paths = sorted(d.rglob("*.txt"))
        if not paths:
            continue
        a = audit_paths(paths, root, include_manifest=False)
        rows[d.name] = a
    eligible_docs = {
        k: v for k, v in rows.items()
        if v["eligible_entries"] >= CORPUS_WIDE_MIN_ELIGIBLE
    }
    return {
        "selection_rule": f"all immediate data/ manuscript directories with >= {CORPUS_WIDE_MIN_ELIGIBLE} eligible literal-pilcrow entries; rule uses no Voynich statistics",
        "all_manuscripts": rows,
        "selected_manuscripts": eligible_docs,
        "selected_names": sorted(eligible_docs),
        "n_selected": len(eligible_docs),
        "selected_total_eligible_entries": sum(v["eligible_entries"] for v in eligible_docs.values()),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/CREMMA-Medieval-LAT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.exists():
        raise SystemExit(f"external checkout not found: {root}")

    historical = {k: resolve_historical_group(root, v) for k, v in HISTORICAL_GROUPS.items()}
    panel = {
        k: {"glob": pattern, **audit_paths(list(root.glob(pattern)), root)}
        for k, pattern in PHASE52_PANEL.items()
    }
    cw = corpus_wide(root)

    out = {
        "purpose": "Phase62A source recovery and candidate-manifest enumeration only; no Voynich tournament scoring",
        "external_repository": EXTERNAL_REPO,
        "external_commit": EXTERNAL_COMMIT,
        "tokenization": "Unicode NFC maximal Letter/Mark sequences; punctuation discarded; abbreviation graphemes retained",
        "boundary_rule": "literal source-native pilcrow U+00B6; line0 is post-marker remainder of source line; line1/line2 are the next two physical transcription lines; eligibility requires >=5 tokens in line0 and line2",
        "historical_phase59_recovery": historical,
        "phase52_panel_basis": "all eligible pilcrow entries in the five manuscripts fixed earlier by Phase52: Arras861, CLM13027, H318, UBL758, BIS193",
        "phase52_panel": panel,
        "phase52_panel_totals": {
            "manuscripts": len(panel),
            "eligible_entries": sum(v["eligible_entries"] for v in panel.values()),
        },
        "corpus_wide_structured_candidates": cw,
        "interpretation_rule": "Historical Phase59 subsets are recoverable only when recorded source/page evidence makes reconstruction unique. Missing historical item metadata must never be reconstructed by choosing items that best match Voynich. Phase62 may instead use objective rules fixed without Voynich scoring: the pre-existing Phase52 manuscript panel and/or the corpus-wide literal-pilcrow threshold panel, with manuscript-level weighting and a separately frozen tournament plan.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
