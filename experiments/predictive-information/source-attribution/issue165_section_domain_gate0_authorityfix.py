#!/usr/bin/env python3
"""Issue #165 Gate0 authority-only wrapper.

The frozen scientific Gate implementation is unchanged. This wrapper corrects
one mistyped copied Issue #107 result SHA before Gate execution, after verifying
the original Gate blob and the additive pre-Gate correction note. No scientific
rule, support threshold, label rule, placebo, model family, or target metric is
changed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
SOURCE_DIR = HERE.parent
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

import issue165_section_domain_gate0 as G165  # noqa: E402

CORRECTION_PATH = SOURCE_DIR / "ISSUE165_PRE_GATE_AUTHORITY_CORRECTION.md"
EXPECTED_ORIGINAL_GATE_BLOB = "adaca5dc387d58542044089aac5faaedc8880ccf"
EXPECTED_CORRECTION_NOTE_BLOB = "01a0c669de59ba43974566e171616682cc5c64f2"
CORRECT_ISSUE107_RESULT_SHA256 = "8f48a62e74fa34f78691949a4b9404caaea39fd6ad8360a93600c653f7147717"
MISTYPED_ISSUE107_RESULT_SHA256 = "8f48a01ef4457f38a4e273fe32ea73b9f90817af156be0111bb56a550f443870"


def canonical_json(obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def verify_and_apply_authority_correction() -> None:
    if G165.git_blob(G165.HERE) != EXPECTED_ORIGINAL_GATE_BLOB:
        raise RuntimeError("original Issue165 Gate blob changed")
    if G165.git_blob(CORRECTION_PATH) != EXPECTED_CORRECTION_NOTE_BLOB:
        raise RuntimeError("Issue165 pre-Gate authority correction note changed")
    if G165.EXPECTED.get("issue107_result_sha256") != MISTYPED_ISSUE107_RESULT_SHA256:
        raise RuntimeError("original Issue165 Gate no longer contains the documented mistyped Issue107 hash")
    G165.EXPECTED["issue107_result_sha256"] = CORRECT_ISSUE107_RESULT_SHA256


def correction_record() -> dict:
    return {
        "authority_only": True,
        "original_gate_blob": EXPECTED_ORIGINAL_GATE_BLOB,
        "correction_note_blob": EXPECTED_CORRECTION_NOTE_BLOB,
        "superseded_mistyped_issue107_result_sha256": MISTYPED_ISSUE107_RESULT_SHA256,
        "correct_issue107_result_sha256": CORRECT_ISSUE107_RESULT_SHA256,
        "scientific_rules_changed": False,
        "real_target_section_metrics_seen_before_correction": False,
    }


def self_test() -> dict:
    verify_and_apply_authority_correction()
    x = G165.synthetic_test()
    return {
        "ok": True,
        "authority_correction": correction_record(),
        "underlying_gate_synthetic": x,
        "uses_real_target_likelihood": False,
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    verify_and_apply_authority_correction()
    result = G165.run_gate(zl_path, it_path)
    result["pre_gate_authority_correction"] = correction_record()
    return result


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue165-section-domain-gate0-v1",
        "issue": 165,
        "phase": "SECTION_DOMAIN_SOURCE_ATTRIBUTION_GATE0",
        "gate_pass": False,
        "gate_disposition": "INVALID SECTION/DOMAIN SOURCE ATTRIBUTION — GATE0 FAILED",
        "scientific_section_metrics_computed": False,
        "error": f"{type(exc).__name__}: {exc}",
        "pre_gate_authority_correction": correction_record(),
        "firewall": {
            "post_failure_scientific_repair_allowed": False,
            "post_failure_target_driven_threshold_change_allowed": False,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--run", nargs=3, metavar=("ZL3B", "IT2A", "OUT_JSON"))
    ns = ap.parse_args(argv)

    if ns.self_test:
        print(canonical_json(self_test()), end="")
        return 0

    zl_path = Path(ns.run[0]).resolve()
    it_path = Path(ns.run[1]).resolve()
    out_path = Path(ns.run[2]).resolve()
    try:
        result = run_gate(zl_path, it_path)
        rc = 0
    except Exception as exc:
        result = invalid_result(exc)
        rc = 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
