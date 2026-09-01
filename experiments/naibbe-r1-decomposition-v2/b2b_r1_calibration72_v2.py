#!/usr/bin/env python3
"""Issue #72 V2 Stage B2b: extended unchanged-Naibbe R1 calibration.

Scores exactly one prospectively frozen B2a surface (rep5..rep24) using the
unchanged Stage B1 R1 measurement implementation. This is positive-control
calibration only. It MUST NOT construct/load/score any Issue72 intervention.

Usage:
  python b2b_r1_calibration72_v2.py CREMMA_ROOT NAIBBE_ROOT B2A_JSON REP OUTPUT_JSON
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve()
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import b1_r1_calibration72_v2 as b1  # noqa: E402

B2A_SHA256 = "1076940701ea7621bbaccaafa08e4f3d0b34a06af5cfb364e56fcdbdf620d83c"
B1_SCORER_BLOB = "2115e8dec15fca21514c8f57e9f51523d10a77c3"
VALID_REPS = tuple(range(5, 25))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load_b2a(path: Path) -> dict:
    raw = path.read_bytes()
    got = sha256_bytes(raw)
    if got != B2A_SHA256:
        raise RuntimeError(f"B2a exact raw SHA mismatch: {got} != {B2A_SHA256}")
    obj = json.loads(raw)
    if obj["status"] != "UNCHANGED_NAIBBE_REP5_REP24_SURFACES_FROZEN":
        raise RuntimeError("B2a status changed")
    if obj["coverage_policy"] != "CONTINUOUS_DESCRIPTIVE_NO_HARD_CUTOFF":
        raise RuntimeError("B2a coverage policy changed")
    if obj["population"]["selection_rule"] != "ALL_REP5_THROUGH_REP24_NO_DROPS_NO_REROLLS":
        raise RuntimeError("B2a population selection rule changed")
    if set(obj["reps"]) != {f"rep{i}" for i in VALID_REPS}:
        raise RuntimeError("B2a population changed")
    if any(obj["target_access"].values()):
        raise RuntimeError("B2a target firewall was not clean")
    return obj


def main(argv: Sequence[str]) -> int:
    if len(argv) != 6:
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT B2A_JSON REP OUTPUT_JSON")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    b2a_path = Path(argv[3]).resolve()
    rep = int(argv[4])
    out = Path(argv[5]).resolve()
    if rep not in VALID_REPS:
        raise SystemExit("REP must be 5..24")

    # Freeze reuse of the accepted B1 measurement implementation itself.
    b1_path = HERE.parent / "b1_r1_calibration72_v2.py"
    got_b1_blob = git_blob_sha1(b1_path.read_bytes())
    if got_b1_blob != B1_SCORER_BLOB:
        raise RuntimeError(f"B1 scorer changed: {got_b1_blob} != {B1_SCORER_BLOB}")

    b2a = load_b2a(b2a_path)
    targets, target_authority = b1.t68.load_target_references()

    # build_dataset consumes the same frozen support schema used by B0/B1.
    # Supplying B2a here changes only the authorized rep population, not the
    # parser, source preparation, line ordering, Q statistic, null, or residualization.
    d = b1.build_dataset(crem, nai, rep, b2a)
    frozen = b2a["reps"][f"rep{rep}"]
    if d["surface_sha256"] != frozen["primary_pooled_surface_sha256"]:
        raise RuntimeError("B2a pooled surface identity failed after regeneration")

    real_q = b1.t68.q_views_candidate(d, d["X"], True)
    namespace = f"issue72v2:positive-control-extension:rep{rep}:reference"
    primary = b1.calibration(d, real_q, targets, namespace)

    result = {
        "schema": "issue72-v2-stage-b2b-per-rep-r1-calibration-v1",
        "scientific_role": "EXTENDED_UNCHANGED_NAIBBE_POSITIVE_CONTROL_CALIBRATION",
        "rep": rep,
        "surface": {
            "sha256": d["surface_sha256"],
            "visible_tokens": d["visible"],
            "parsed_tokens": d["parsed"],
            "coverage": d["coverage"],
            "fold_parsed_tokens": d["fold_counts"],
            "line_count_with_parsed_token": d["line_count"],
            "per_manuscript": d["per_manuscript"],
        },
        "support_authority": {
            "b2a_raw_sha256": B2A_SHA256,
            "frozen_surface_sha256": frozen["primary_pooled_surface_sha256"],
            "selection_rule": b2a["population"]["selection_rule"],
        },
        "measurement_authority": {
            "b1_scorer_git_blob": got_b1_blob,
            "reference_namespace": namespace,
            "n_reference": b1.N_REF,
        },
        "target_authority": target_authority,
        "primary": primary,
        "classification": None,
        "hard_threshold_applied": False,
        "p_values_computed": False,
        "test_nulls_computed": False,
        "issue72_intervention_surface_loaded_or_generated": False,
        "issue72_intervention_R1_computed": False,
    }

    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(json.dumps({
        "rep": rep,
        "surface_sha256": d["surface_sha256"],
        "coverage": d["coverage"],
        "E": primary["residual_energy"],
        "W": primary["reliability"]["median"],
        "R_ZL3b": primary["topology"]["ZL3b"]["pearson"],
        "R_IT2a": primary["topology"]["IT2a"]["pearson"],
        "M_R": primary["M_R"],
        "sign_ZL3b": primary["topology"]["ZL3b"]["sign_agreement"],
        "sign_IT2a": primary["topology"]["IT2a"]["sign_agreement"],
        "M_sign": primary["M_sign"],
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
