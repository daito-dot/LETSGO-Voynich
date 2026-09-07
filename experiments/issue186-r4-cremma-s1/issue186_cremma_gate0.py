#!/usr/bin/env python3
"""Issue #186 R4/CREMMA Gate0: score-free composability audit.

This program is deliberately unable to compute the new external S1 reveal.
It verifies frozen authorities, reuses only the historical Phase62B Latin parser
and structural eligibility predicates, and reports support for all 21 externally
registered CREMMA manuscripts.

Usage:
  python experiments/issue186-r4-cremma-s1/issue186_cremma_gate0.py \
    --zl3b /path/to/ZL3b-n.txt --cremma /path/to/CREMMA-Medieval-LAT
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
P62_PATH = ROOT / "experiments" / "phase62" / "phase62b_n0.py"

EXPECTED_P62_BLOB = "e0ada366845c7a6c5a5dd75de91fe262b72a94b6"
EXPECTED_ZL_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_CREMMA_COMMIT = "292525969ad98380b398e6606a9c2a36d51913ae"
NO_SCORE_MARKER = "NO ISSUE186 SCIENTIFIC S1 SCORE COMPUTED"

# Frozen from the Type field of the pinned CREMMA registry before new scoring.
MANUSCRIPTS = (
    ("Egerton821", "Medic.", "data/Egerton821"),
    ("H318", "Medic.", "data/H318"),
    ("CLM13027", "Medic.", "data/CLM13027"),
    ("Latin16195", "Medic.", "data/Latin16195"),
    ("Phi_10a135", "Medic.", "data/Phi_10a135"),
    ("WettF0015", "Schol.", "data/WettF0015"),
    ("BIS-193", "Schol.", "data/BIS-193"),
    ("Mazarine915", "Schol.", "data/Mazarine915"),
    ("PalLat373", "Schol.", "data/PalLat373"),
    ("CCCC-MSS-165", "Schol.", "data/CCCC-MSS-165"),
    ("CCCC-MSS-236", "Lit.", "data/CCCC-MSS-236"),
    ("LaurentianusPluteus33.31", "Lit.", "data/LaurentianusPluteus33.31"),
    ("Arras-861", "Lit.", "data/Arras-861"),
    ("Latin6395", "Lit.", "data/Latin6395"),
    ("LaurentianusPluteus39.34", "Lit.", "data/LaurentianusPluteus39.34"),
    ("Latin8236", "Lit.", "data/Latin8236"),
    ("UBL758", "Eccl.", "data/UBL758"),
    ("SBB_PK_Hdschr25", "Eccl.", "data/SBB_PK_Hdschr25"),
    ("BGO-511", "Eccl.", "data/BGO-511"),
    ("LaurentianusPluteus53.08", "Gramm.", "data/LaurentianusPluteus53.08"),
    ("LaurentianusPluteus53.09", "Gramm.", "data/LaurentianusPluteus53.09"),
)

FORBIDDEN_SCORE_FUNCTIONS = (
    "feature8",
    "training_sd",
    "item_contrast",
    "contrasts",
    "s1_projection",
)


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def git_blob_bytes(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git_blob_file(path: Path) -> str:
    return git_blob_bytes(path.read_bytes())


def git_head(repo: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()


def forbidden_score(*_args: Any, **_kwargs: Any) -> Any:
    raise RuntimeError("Issue186 Gate0 firewall: S1 scoring function is forbidden")


def load_phase62b():
    got = git_blob_file(P62_PATH)
    if got != EXPECTED_P62_BLOB:
        raise RuntimeError(f"Phase62B authority blob changed: {got} != {EXPECTED_P62_BLOB}")

    spec = importlib.util.spec_from_file_location("issue186_phase62b_authority", P62_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Phase62B authority: {P62_PATH}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    if getattr(mod, "EXPECTED_ZL3B_BLOB", None) != EXPECTED_ZL_BLOB:
        raise RuntimeError("Phase62B embedded ZL3b authority differs from Issue186 freeze")
    if getattr(mod, "EXPECTED_CREMMA_COMMIT", None) != EXPECTED_CREMMA_COMMIT:
        raise RuntimeError("Phase62B embedded CREMMA authority differs from Issue186 freeze")
    return mod, got


def install_score_firewall(mod) -> list[str]:
    missing = [name for name in FORBIDDEN_SCORE_FUNCTIONS if not hasattr(mod, name)]
    if missing:
        raise RuntimeError(f"historical score functions missing before firewall: {missing}")
    for name in FORBIDDEN_SCORE_FUNCTIONS:
        setattr(mod, name, forbidden_score)
    for name in FORBIDDEN_SCORE_FUNCTIONS:
        if getattr(mod, name) is not forbidden_score:
            raise RuntimeError(f"failed to install score firewall for {name}")
    return list(FORBIDDEN_SCORE_FUNCTIONS)


def audit_manuscript(B, cremma: Path, name: str, type_label: str, rel_dir: str) -> dict[str, Any]:
    try:
        items = B.parse_latin_manuscript(cremma, name, rel_dir)
        item_total = len(items)
        base_eligible = sum(bool(B.base_eligible(it)) for it in items)
        s1_eligible = sum(bool(B.s1_eligible(it)) for it in items)
        physical_lines = sum(len(it.lines) for it in items)
        nonempty_lines = sum(bool(line) for it in items for line in it.lines)
        token_count = sum(len(line) for it in items for line in it.lines)
        return {
            "name": name,
            "type": type_label,
            "source_path": rel_dir,
            "parse_status": "PARSED",
            "item_total": int(item_total),
            "base_eligible": int(base_eligible),
            "s1_eligible": int(s1_eligible),
            "physical_lines": int(physical_lines),
            "nonempty_lines": int(nonempty_lines),
            "token_count": int(token_count),
            "stage1_structurally_composable": bool(s1_eligible > 0),
        }
    except Exception as exc:  # Gate0 records the failure; it does not repair it.
        return {
            "name": name,
            "type": type_label,
            "source_path": rel_dir,
            "parse_status": "PARSER_OR_SOURCE_FAILURE",
            "error": f"{type(exc).__name__}: {exc}",
            "stage1_structurally_composable": False,
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zl3b", required=True, type=Path)
    ap.add_argument("--cremma", required=True, type=Path)
    args = ap.parse_args()

    zl3b = args.zl3b.resolve()
    cremma = args.cremma.resolve()

    # Authority verification only. ZL3b is deliberately never parsed in Gate0.
    B, phase62b_blob = load_phase62b()
    cremma_head = git_head(cremma)
    zl3b_blob = git_blob_file(zl3b)
    if cremma_head != EXPECTED_CREMMA_COMMIT:
        raise RuntimeError(f"CREMMA commit changed: {cremma_head} != {EXPECTED_CREMMA_COMMIT}")
    if zl3b_blob != EXPECTED_ZL_BLOB:
        raise RuntimeError(f"ZL3b blob changed: {zl3b_blob} != {EXPECTED_ZL_BLOB}")

    firewall_names = install_score_firewall(B)

    rows = [
        audit_manuscript(B, cremma, name, type_label, rel_dir)
        for name, type_label, rel_dir in MANUSCRIPTS
    ]

    class_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        class_rows[row["type"]].append(row)

    class_support = {}
    for type_label, members in sorted(class_rows.items()):
        class_support[type_label] = {
            "listed_manuscripts": len(members),
            "parsed_manuscripts": sum(m["parse_status"] == "PARSED" for m in members),
            "stage1_structurally_composable_manuscripts": sum(
                bool(m["stage1_structurally_composable"]) for m in members
            ),
        }

    parsed = [r for r in rows if r["parse_status"] == "PARSED"]
    parse_failures = [r["name"] for r in rows if r["parse_status"] != "PARSED"]
    gate0_valid = bool(
        phase62b_blob == EXPECTED_P62_BLOB
        and cremma_head == EXPECTED_CREMMA_COMMIT
        and zl3b_blob == EXPECTED_ZL_BLOB
        and len(rows) == 21
        and len(parse_failures) == 0
        and all(getattr(B, name) is forbidden_score for name in FORBIDDEN_SCORE_FUNCTIONS)
    )

    out = {
        "schema": "issue186-r4-cremma-s1-gate0-v1",
        "issue": 186,
        "stage": "gate0_score_free_composability",
        "marker": NO_SCORE_MARKER,
        "scientific_score_computed": False,
        "gate0_valid": gate0_valid,
        "authorities": {
            "phase62b_path": str(P62_PATH.relative_to(ROOT)),
            "phase62b_git_blob": phase62b_blob,
            "expected_phase62b_git_blob": EXPECTED_P62_BLOB,
            "cremma_commit": cremma_head,
            "expected_cremma_commit": EXPECTED_CREMMA_COMMIT,
            "zl3b_git_blob": zl3b_blob,
            "expected_zl3b_git_blob": EXPECTED_ZL_BLOB,
            "zl3b_parsed": False,
        },
        "firewall": {
            "installed_before_external_audit": True,
            "disabled_score_functions": firewall_names,
            "new_s1_fields_emitted": False,
            "posthoc_source_repair_allowed": False,
        },
        "manuscripts": rows,
        "class_support": class_support,
        "totals": {
            "listed_manuscripts": len(rows),
            "parsed_manuscripts": len(parsed),
            "parse_failures": parse_failures,
            "stage1_structurally_composable_manuscripts": sum(
                bool(r["stage1_structurally_composable"]) for r in rows
            ),
            "items": sum(int(r.get("item_total", 0)) for r in parsed),
            "base_eligible": sum(int(r.get("base_eligible", 0)) for r in parsed),
            "s1_eligible": sum(int(r.get("s1_eligible", 0)) for r in parsed),
            "physical_lines": sum(int(r.get("physical_lines", 0)) for r in parsed),
            "nonempty_lines": sum(int(r.get("nonempty_lines", 0)) for r in parsed),
            "tokens": sum(int(r.get("token_count", 0)) for r in parsed),
        },
    }

    sys.stdout.write(canonical_json(out))
    return 0 if gate0_valid else 4


if __name__ == "__main__":
    raise SystemExit(main())
