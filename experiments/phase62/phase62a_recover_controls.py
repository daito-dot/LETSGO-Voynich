#!/usr/bin/env python3
"""Audit/recover the external Phase59 medieval-entry control source set.

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
from typing import Iterable

EXTERNAL_REPO = "HTR-United/CREMMA-Medieval-LAT"
EXTERNAL_COMMIT = "292525969ad98380b398e6606a9c2a36d51913ae"

HISTORICAL_GROUPS = {
    "H318_recipe": {
        "expected_n": 3,
        "files": ["data/H318/10r.txt"],
        "selection_status": "file identified from the Phase59 recipe context; eligibility to be audited",
    },
    "CLM13027_39r_treatment": {
        "expected_n": 3,
        "files": ["data/CLM13027/39r.txt"],
        "selection_status": "exact page named in Phase59 result key",
    },
    "CLM13027_41r_41v_medical_discussion": {
        "expected_n": 9,
        "files": ["data/CLM13027/41r.txt", "data/CLM13027/41v.txt"],
        "selection_status": "exact pages named in Phase59 result key",
    },
    "UBL758_ecclesiastical": {
        "expected_n": 5,
        "glob": "data/UBL758/*.txt",
        "selection_status": "historical page subset was not recorded; enumerate without choosing by Voynich fit",
    },
    "BIS193_scholastic": {
        "expected_n": 5,
        "glob": "data/BIS-193/*.txt",
        "selection_status": "historical page subset was not recorded; enumerate without choosing by Voynich fit",
    },
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def unicode_lm_tokens(text: str) -> list[str]:
    """Phase52-style graphematic tokenization: NFC Letter/Mark sequences.

    Punctuation/separators are discarded; combining marks remain attached to
    neighboring letters where present. This is not abbreviation expansion.
    """
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
        # Each part after a pilcrow is an explicit source marker. If several
        # markers share one physical line, each is recorded separately.
        for j, after in enumerate(parts[1:], start=1):
            line0 = after
            # Do not allow text after a later same-line pilcrow to leak into
            # this entry's line0.
            if j < len(parts) - 1:
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
                    "token_counts_line0_line1_line2": [len(t0), len(t1), len(t2)],
                    "eligible_phase59_primary": bool(len(t0) >= 5 and len(t2) >= 5),
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
        "eligible_entries": sum(e["eligible_phase59_primary"] for e in entries),
        "entries": entries,
    }


def contiguous_windows(files: list[dict], expected: int, limit: int = 50) -> list[dict]:
    """Diagnostic only: filename-ordered contiguous windows summing to expected.

    This does not select a historical subset. It only shows whether the missing
    historical UBL/BIS page subset can be reconstructed uniquely from counts.
    """
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


def resolve_group(root: Path, spec: dict) -> dict:
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


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/CREMMA-Medieval-LAT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.exists():
        raise SystemExit(f"external checkout not found: {root}")
    out = {
        "purpose": "Phase62A source recovery only; no Voynich tournament scoring",
        "external_repository": EXTERNAL_REPO,
        "external_commit": EXTERNAL_COMMIT,
        "tokenization": "Unicode NFC maximal Letter/Mark sequences; punctuation discarded; abbreviation graphemes retained",
        "boundary_rule": "literal source-native pilcrow U+00B6; line0 is post-marker remainder of source line; line1/line2 are the next two physical transcription lines; primary eligibility requires >=5 tokens in line0 and line2",
        "historical_phase59_expected_counts": {k: v["expected_n"] for k, v in HISTORICAL_GROUPS.items()},
        "groups": {k: resolve_group(root, v) for k, v in HISTORICAL_GROUPS.items()},
        "interpretation_rule": "Counts may identify historical subsets only when the recorded page names or source evidence make the reconstruction unique. Missing UBL/BIS historical subset metadata must not be recovered by choosing the subset that best matches Voynich statistics.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
