#!/usr/bin/env python3
"""Aggregate Issue #72 V2 B1 rep0..rep4 positive-control calibrations.

No intervention files are read. No PASS/FAIL threshold is applied.
"""
from __future__ import annotations

import itertools
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("occupancy-graph-stability", "occupancy-graph-independent-transcription"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase58b_graph_stability as b58  # noqa: E402
import phase58d_independent_residual as d58  # noqa: E402

N_EDGES = 66
REP0_FROZEN = {
    "E": 3.1784043855151296,
    "W": 0.954726539114345,
    "ZL3b_R": 0.8830282501011794,
    "IT2a_R": 0.9000974100381157,
    "ZL3b_sign": 60,
    "IT2a_sign": 61,
}
TOL = 1e-12


def median(xs):
    return float(np.median(np.asarray(xs, dtype=float)))


def mad(xs):
    a = np.asarray(xs, dtype=float)
    m = np.median(a)
    return float(np.median(np.abs(a - m)))


def summary(xs):
    vals = [float(x) for x in xs]
    return {
        "values": vals,
        "min": min(vals),
        "max": max(vals),
        "range": max(vals) - min(vals),
        "median": median(vals),
        "MAD": mad(vals),
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} PER_REP_DIR OUTPUT_JSON")
    root = Path(argv[1]).resolve()
    out = Path(argv[2]).resolve()
    reps = {}
    for rep in range(5):
        path = root / f"rep{rep}.json"
        r = json.loads(path.read_text(encoding="utf-8"))
        if r["rep"] != rep or r["classification"] is not None:
            raise RuntimeError(f"invalid rep artifact {rep}")
        if r["secondary"] is None or r["calibration_noise"] is None:
            raise RuntimeError(f"rep{rep} missing independent secondary calibration")
        if r["p_values_computed"] or r["test_nulls_computed"]:
            raise RuntimeError(f"rep{rep} unexpectedly computed confirmatory p-values")
        if r["issue72_intervention_surface_loaded_or_generated"] or r["issue72_intervention_R1_computed"]:
            raise RuntimeError(f"rep{rep} intervention firewall violated")
        reps[rep] = r

    r0 = reps[0]["primary"]
    scalar = {
        "E": r0["residual_energy"],
        "W": r0["reliability"]["median"],
        "ZL3b_R": r0["topology"]["ZL3b"]["pearson"],
        "IT2a_R": r0["topology"]["IT2a"]["pearson"],
    }
    for k, v in scalar.items():
        if abs(float(v) - REP0_FROZEN[k]) > TOL:
            raise RuntimeError(f"rep0 aggregate cross-check failed {k}")
    if r0["topology"]["ZL3b"]["sign_agreement"] != REP0_FROZEN["ZL3b_sign"]:
        raise RuntimeError("rep0 ZL sign aggregate cross-check failed")
    if r0["topology"]["IT2a"]["sign_agreement"] != REP0_FROZEN["IT2a_sign"]:
        raise RuntimeError("rep0 IT sign aggregate cross-check failed")

    coords = {
        "coverage": [reps[i]["surface"]["coverage"] for i in range(5)],
        "E": [reps[i]["primary"]["residual_energy"] for i in range(5)],
        "W": [reps[i]["primary"]["reliability"]["median"] for i in range(5)],
        "R_ZL3b": [reps[i]["primary"]["topology"]["ZL3b"]["pearson"] for i in range(5)],
        "R_IT2a": [reps[i]["primary"]["topology"]["IT2a"]["pearson"] for i in range(5)],
        "M_R": [reps[i]["primary"]["M_R"] for i in range(5)],
        "sign_ZL3b": [reps[i]["primary"]["topology"]["ZL3b"]["sign_agreement"] for i in range(5)],
        "sign_IT2a": [reps[i]["primary"]["topology"]["IT2a"]["sign_agreement"] for i in range(5)],
        "M_sign": [reps[i]["primary"]["M_sign"] for i in range(5)],
    }
    spread = {k: summary(v) for k, v in coords.items()}

    noise_fields = (
        "corr_Z_primary_secondary",
        "sign_Z_primary_secondary",
        "abs_delta_E",
        "abs_delta_W",
        "abs_delta_R_ZL3b",
        "abs_delta_R_IT2a",
        "abs_delta_sign_ZL3b",
        "abs_delta_sign_IT2a",
    )
    noise = {
        field: summary([reps[i]["calibration_noise"][field] for i in range(5)])
        for field in noise_fields
    }

    # Pairwise primary residual-topology stability among unchanged-mechanism reps.
    pairwise = []
    for a, b in itertools.combinations(range(5), 2):
        za = np.asarray(reps[a]["primary"]["z_full"], dtype=float)
        zb = np.asarray(reps[b]["primary"]["z_full"], dtype=float)
        rr = b58.corr(za, zb)
        if rr is None:
            raise RuntimeError(f"undefined pairwise rep correlation {a},{b}")
        pairwise.append({
            "rep_a": a,
            "rep_b": b,
            "pearson_Z": float(rr),
            "sign_agreement_Z": int(d58.sign_agreement(za, zb)),
            "sign_denominator": N_EDGES,
        })

    # Ratios are descriptive resolution diagnostics only; no cutoff is applied.
    resolution = {}
    for coord, noise_field in (
        ("E", "abs_delta_E"),
        ("W", "abs_delta_W"),
        ("R_ZL3b", "abs_delta_R_ZL3b"),
        ("R_IT2a", "abs_delta_R_IT2a"),
    ):
        denom = noise[noise_field]["max"]
        resolution[coord] = {
            "between_rep_primary_range": spread[coord]["range"],
            "max_within_surface_reference_calibration_abs_delta": denom,
            "range_to_max_calibration_noise_ratio": None if denom == 0 else spread[coord]["range"] / denom,
            "role": "DESCRIPTIVE_RESOLUTION_DIAGNOSTIC_NO_THRESHOLD",
        }

    result = {
        "schema": "issue72-v2-stage-b1-unchanged-naibbe-calibration-summary-v1",
        "status": "UNCHANGED-NAIBBE R1 STOCHASTIC VARIATION CHARACTERIZED",
        "classification": None,
        "hard_intervention_threshold_derived": False,
        "positive_control_role": "T2_EFFECT_SCALE_NOT_PASS_FAIL_BOUNDARY",
        "rep0_historical_exact_replay": True,
        "primary_coordinate_spread": spread,
        "reference_calibration_noise": noise,
        "resolution_diagnostics": resolution,
        "pairwise_primary_residual_topology": pairwise,
        "pairwise_primary_residual_topology_summary": {
            "pearson": summary([x["pearson_Z"] for x in pairwise]),
            "sign_agreement": summary([x["sign_agreement_Z"] for x in pairwise]),
        },
        "per_rep": {
            f"rep{i}": {
                "surface": reps[i]["surface"],
                "primary": reps[i]["primary"],
                "secondary": reps[i]["secondary"],
                "calibration_noise": reps[i]["calibration_noise"],
            }
            for i in range(5)
        },
        "guardrails": [
            "No Issue72 intervention R1 quantity was used or computed",
            "No B1 p-value or test-null family was generated",
            "The five-rep positive-control spread is not a hard intervention pass/fail threshold",
            "Later causal tests require prospectively frozen intervention-specific randomization/matched controls",
        ],
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "spread": {k: {x: v[x] for x in ("min", "max", "range", "median", "MAD")} for k, v in spread.items()},
        "noise_max": {k: v["max"] for k, v in noise.items()},
        "pairwise_rep_Z_pearson": result["pairwise_primary_residual_topology_summary"]["pearson"],
        "pairwise_rep_Z_sign": result["pairwise_primary_residual_topology_summary"]["sign_agreement"],
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
