#!/usr/bin/env python3
"""Aggregate Issue #72 V2 Stage B2b into a 25-rep unchanged-Naibbe calibration.

Inputs:
- exact Stage B1 aggregate raw JSON (rep0..rep4, including full z vectors)
- directory containing exactly rep5.json .. rep24.json from B2b

This executable reports continuous measurement variation only. It derives no
hard intervention threshold and has no access to Issue72 intervention surfaces.
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

HERE = Path(__file__).resolve()
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import b1_r1_calibration72_v2 as b1  # noqa: E402

B1_RAW_SHA256 = "b37d285b25d17623fa19910ff3f8f4586846bb8f19825c3dbdd6e8b19bb2e31d"
B2A_RAW_SHA256 = "1076940701ea7621bbaccaafa08e4f3d0b34a06af5cfb364e56fcdbdf620d83c"
REPS = tuple(range(25))
NEW_REPS = tuple(range(5, 25))
COORDS = (
    "coverage", "E", "W", "R_ZL3b", "R_IT2a", "M_R",
    "sign_ZL3b", "sign_IT2a", "M_sign",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json_exact(path: Path, expected_sha: str, label: str) -> dict:
    raw = path.read_bytes()
    got = sha256_bytes(raw)
    if got != expected_sha:
        raise RuntimeError(f"{label} SHA mismatch: {got} != {expected_sha}")
    return json.loads(raw)


def row_from_b1(rep: int, x: Mapping) -> dict:
    p = x["primary"]
    s = x["surface"]
    return {
        "rep": rep,
        "population": "historical_rep0_rep4",
        "surface_sha256": s["sha256"],
        "coverage": float(s["coverage"]),
        "E": float(p["residual_energy"]),
        "W": float(p["reliability"]["median"]),
        "R_ZL3b": float(p["topology"]["ZL3b"]["pearson"]),
        "R_IT2a": float(p["topology"]["IT2a"]["pearson"]),
        "M_R": float(p["M_R"]),
        "sign_ZL3b": int(p["topology"]["ZL3b"]["sign_agreement"]),
        "sign_IT2a": int(p["topology"]["IT2a"]["sign_agreement"]),
        "M_sign": int(p["M_sign"]),
        "z_full": [float(v) for v in p["z_full"]],
        "q_full": [float(v) for v in p["q_full"]],
    }


def row_from_b2b(rep: int, x: Mapping) -> dict:
    if x["schema"] != "issue72-v2-stage-b2b-per-rep-r1-calibration-v1":
        raise RuntimeError(f"rep{rep}: unexpected schema")
    if x["rep"] != rep:
        raise RuntimeError(f"rep{rep}: rep id mismatch")
    if x["support_authority"]["b2a_raw_sha256"] != B2A_RAW_SHA256:
        raise RuntimeError(f"rep{rep}: B2a authority mismatch")
    if x["hard_threshold_applied"] or x["p_values_computed"] or x["test_nulls_computed"]:
        raise RuntimeError(f"rep{rep}: forbidden decision procedure present")
    if x["issue72_intervention_surface_loaded_or_generated"] or x["issue72_intervention_R1_computed"]:
        raise RuntimeError(f"rep{rep}: intervention firewall violated")
    p = x["primary"]
    s = x["surface"]
    if s["sha256"] != x["support_authority"]["frozen_surface_sha256"]:
        raise RuntimeError(f"rep{rep}: surface authority mismatch")
    return {
        "rep": rep,
        "population": "prospective_extension_rep5_rep24",
        "surface_sha256": s["sha256"],
        "coverage": float(s["coverage"]),
        "E": float(p["residual_energy"]),
        "W": float(p["reliability"]["median"]),
        "R_ZL3b": float(p["topology"]["ZL3b"]["pearson"]),
        "R_IT2a": float(p["topology"]["IT2a"]["pearson"]),
        "M_R": float(p["M_R"]),
        "sign_ZL3b": int(p["topology"]["ZL3b"]["sign_agreement"]),
        "sign_IT2a": int(p["topology"]["IT2a"]["sign_agreement"]),
        "M_sign": int(p["M_sign"]),
        "z_full": [float(v) for v in p["z_full"]],
        "q_full": [float(v) for v in p["q_full"]],
    }


def summary(values: Sequence[float]) -> dict:
    vals = [float(v) for v in values]
    med = float(statistics.median(vals))
    mad = float(statistics.median(abs(v - med) for v in vals))
    ordered = sorted(vals)
    return {
        "n": len(vals),
        "mean": float(statistics.fmean(vals)),
        "median": med,
        "MAD": mad,
        "population_sd": float(statistics.pstdev(vals)),
        "min": ordered[0],
        "max": ordered[-1],
        "range": ordered[-1] - ordered[0],
        "order_statistics": [
            {"rank": i + 1, "empirical_cdf": float((i + 1) / len(vals)), "value": v}
            for i, v in enumerate(ordered)
        ],
    }


def rep0_location(values: Sequence[float], rep0_value: float) -> dict:
    vals = [float(v) for v in values]
    eps = 1e-15
    below = sum(v < rep0_value - eps for v in vals)
    equal = sum(abs(v - rep0_value) <= eps for v in vals)
    above = len(vals) - below - equal
    return {
        "value": float(rep0_value),
        "count_below": int(below),
        "count_equal": int(equal),
        "count_above": int(above),
        "empirical_midrank_fraction": float((below + 0.5 * equal) / len(vals)),
    }


def old_range_transport(old_values: Sequence[float], new_values: Sequence[float]) -> dict:
    lo, hi = min(old_values), max(old_values)
    eps = 1e-15
    below = sum(v < lo - eps for v in new_values)
    above = sum(v > hi + eps for v in new_values)
    within = len(new_values) - below - above
    return {
        "historical_rep0_rep4_min": float(lo),
        "historical_rep0_rep4_max": float(hi),
        "new_rep5_rep24_below": int(below),
        "new_rep5_rep24_within": int(within),
        "new_rep5_rep24_above": int(above),
    }


def pairwise(rows: Sequence[Mapping]) -> tuple[list[dict], dict]:
    pairs = []
    for i in range(len(rows)):
        zi = np.asarray(rows[i]["z_full"], dtype=np.float64)
        if zi.shape != (66,):
            raise RuntimeError(f"rep{rows[i]['rep']}: z length != 66")
        for j in range(i + 1, len(rows)):
            zj = np.asarray(rows[j]["z_full"], dtype=np.float64)
            rr = b1.b58.corr(zi, zj)
            if rr is None:
                raise RuntimeError(f"undefined z correlation rep{rows[i]['rep']} rep{rows[j]['rep']}")
            ss = b1.d58.sign_agreement(zi, zj)
            pairs.append({
                "rep_a": int(rows[i]["rep"]),
                "rep_b": int(rows[j]["rep"]),
                "pearson": float(rr),
                "sign_agreement": int(ss),
                "sign_denominator": 66,
            })
    if len(pairs) != math.comb(25, 2):
        raise RuntimeError("expected 300 pairwise comparisons")
    return pairs, {
        "pearson": summary([p["pearson"] for p in pairs]),
        "sign_agreement": summary([p["sign_agreement"] for p in pairs]),
    }


def verify_b1_internal_replay(b1raw: Mapping, rows: Sequence[Mapping]) -> None:
    old = rows[:5]
    pairs, sm = pairwise(old + [
        # pairwise() is fixed at 25; do a direct 5-rep check here instead.
    ]) if False else (None, None)
    vals_r = []
    vals_s = []
    for i in range(5):
        zi = np.asarray(old[i]["z_full"], dtype=np.float64)
        for j in range(i + 1, 5):
            zj = np.asarray(old[j]["z_full"], dtype=np.float64)
            rr = b1.b58.corr(zi, zj)
            if rr is None:
                raise RuntimeError("B1 replay correlation undefined")
            vals_r.append(float(rr))
            vals_s.append(float(b1.d58.sign_agreement(zi, zj)))
    auth = b1raw["pairwise_primary_residual_topology_summary"]
    for key, vals in (("pearson", vals_r), ("sign_agreement", vals_s)):
        got = summary(vals)
        for stat in ("min", "median", "max", "range", "MAD"):
            if abs(float(got[stat]) - float(auth[key][stat])) > 1e-12:
                raise RuntimeError(f"B1 internal aggregate replay failed {key}.{stat}")


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} B1_RAW_JSON B2B_REP_DIR OUTPUT_JSON")
    b1_path = Path(argv[1]).resolve()
    rep_dir = Path(argv[2]).resolve()
    out = Path(argv[3]).resolve()

    b1raw = load_json_exact(b1_path, B1_RAW_SHA256, "Stage B1 aggregate")
    if b1raw["status"] != "UNCHANGED-NAIBBE R1 STOCHASTIC VARIATION CHARACTERIZED":
        raise RuntimeError("Stage B1 status changed")
    if b1raw["hard_intervention_threshold_derived"]:
        raise RuntimeError("Stage B1 unexpectedly derived a hard threshold")

    rows = [row_from_b1(r, b1raw["per_rep"][f"rep{r}"]) for r in range(5)]
    for rep in NEW_REPS:
        path = rep_dir / f"rep{rep}.json"
        if not path.is_file():
            raise RuntimeError(f"missing B2b result: {path}")
        rows.append(row_from_b2b(rep, json.loads(path.read_text(encoding="utf-8"))))
    if [r["rep"] for r in rows] != list(REPS):
        raise RuntimeError("25-rep order/population mismatch")

    verify_b1_internal_replay(b1raw, rows)
    pair_rows, pair_summary = pairwise(rows)

    coordinate_summary = {}
    rep0_loc = {}
    old_range = {}
    for coord in COORDS:
        values = [r[coord] for r in rows]
        coordinate_summary[coord] = summary(values)
        rep0_loc[coord] = rep0_location(values, rows[0][coord])
        old_range[coord] = old_range_transport(values[:5], values[5:])

    result = {
        "schema": "issue72-v2-stage-b2-25rep-positive-control-v1",
        "status": "EXTENDED UNCHANGED-NAIBBE R1 DISTRIBUTION CALIBRATED",
        "scientific_role": "T2_UNCHANGED_MECHANISM_VARIATION_SCALE_NOT_HARD_THRESHOLD",
        "population": {
            "n": 25,
            "reps": list(REPS),
            "historical_reps": list(range(5)),
            "prospective_extension_reps": list(NEW_REPS),
            "selection_rule": "ALL_REP0_THROUGH_REP24_NO_RESULT_BASED_DROPS",
        },
        "authorities": {
            "stage_b1_raw_sha256": B1_RAW_SHA256,
            "stage_b2a_raw_sha256": B2A_RAW_SHA256,
        },
        "per_rep": rows,
        "coordinate_summary": coordinate_summary,
        "pairwise_residual_topology": pair_rows,
        "pairwise_residual_topology_summary": pair_summary,
        "rep0_location": rep0_loc,
        "historical_five_range_transport": old_range,
        "decision_policy": {
            "hard_intervention_threshold_derived": False,
            "worst_positive_is_fail_cutoff": False,
            "gaussian_tail_used_as_truth_region": False,
            "future_use": "EMPIRICAL_EFFECT_SCALE_AND_POSITIVE_CONTROL_REFERENCE_ONLY",
        },
        "issue72_intervention_surface_loaded_or_generated": False,
        "issue72_intervention_R1_computed": False,
    }

    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "output_sha256": sha256_bytes(raw),
        "coordinates": {
            k: {x: coordinate_summary[k][x] for x in ("mean", "median", "MAD", "population_sd", "min", "max")}
            for k in COORDS
        },
        "pairwise": {
            "pearson": {x: pair_summary["pearson"][x] for x in ("min", "median", "max")},
            "sign": {x: pair_summary["sign_agreement"][x] for x in ("min", "median", "max")},
        },
        "rep0_location": rep0_loc,
        "old_five_range_transport": old_range,
        "hard_threshold_derived": False,
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
