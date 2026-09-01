#!/usr/bin/env python3
"""Aggregate the complete Issue #72 V2 Stage D1 PT population.

No hard intervention threshold is applied. ZL3b and IT2a remain separate.
Usage: python d1_pt_aggregate72_v2.py INPUT_DIR OUTPUT_JSON
"""
from __future__ import annotations

import glob
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Sequence

TARGETS = ("ZL3b", "IT2a")
EXPECTED = {(j, rep) for j in range(31) for rep in range(5)}
B2_SCALE = {
    "ZL3b": {"SD": 0.010907479701133605, "MAD": 0.00897810342736527},
    "IT2a": {"SD": 0.008561663953448985, "MAD": 0.005799322835226439},
}


def q(xs, p):
    ys = sorted(float(x) for x in xs)
    if not ys:
        return None
    if len(ys) == 1:
        return ys[0]
    z = (len(ys) - 1) * p
    lo = int(math.floor(z)); hi = int(math.ceil(z))
    if lo == hi:
        return ys[lo]
    return ys[lo] * (hi - z) + ys[hi] * (z - lo)


def summarize(xs):
    ys = [float(x) for x in xs]
    return {
        "n": len(ys),
        "mean": float(statistics.fmean(ys)),
        "median": float(statistics.median(ys)),
        "min": min(ys),
        "q25": q(ys, .25),
        "q75": q(ys, .75),
        "max": max(ys),
        "sd_population": float(statistics.pstdev(ys)),
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} INPUT_DIR OUTPUT_JSON")
    inp = Path(argv[1]).resolve(); out = Path(argv[2]).resolve()
    paths = sorted(glob.glob(str(inp / "PT_j*_rep*.json")))
    if len(paths) != 155:
        raise RuntimeError(f"need exactly 155 results, found {len(paths)}")

    rows = {}
    target_authority = None
    static_authority = None
    for p in paths:
        r = json.load(open(p, encoding="utf-8"))
        if r["status"] != "STAGE_D1_PT_R1_TARGET_SCORED":
            raise RuntimeError(f"non-scored input: {p}")
        key = (int(r["j"]), int(r["rep"]))
        if key in rows:
            raise RuntimeError(f"duplicate result {key}")
        if key not in EXPECTED:
            raise RuntimeError(f"unexpected result {key}")
        dp = r["decision_policy"]
        if dp != {
            "hard_intervention_threshold_applied": False,
            "readings_averaged": False,
            "coverage_gate_applied": False,
            "baseline_rescored": False,
        }:
            raise RuntimeError(f"decision policy changed {key}: {dp}")
        if target_authority is None:
            target_authority = r["target_authority"]
        elif r["target_authority"] != target_authority:
            raise RuntimeError("target authority differs across cases")
        if static_authority is None:
            static_authority = r["static_authority"]
        elif r["static_authority"] != static_authority:
            raise RuntimeError("static authority differs across cases")
        rows[key] = r
    if set(rows) != EXPECTED:
        raise RuntimeError("incomplete exact Stage D1 population")

    assignments = []
    per_target_D = {t: [] for t in TARGETS}
    all_case_delta = {t: [] for t in TARGETS}
    all_coverage = []
    for j in range(31):
        block_rows = [rows[(j, rep)] for rep in range(5)]
        entry = {"j": j, "blocks": [], "D": {}, "B2_scale_ratio": {}}
        for rep, r in enumerate(block_rows):
            d = r["delta_R_randomized_minus_baseline"]
            all_coverage.append(float(r["surface"]["coverage"]))
            entry["blocks"].append({
                "rep": rep,
                "coverage": float(r["surface"]["coverage"]),
                "R_PT_ZL3b": float(r["PT_R1"]["topology"]["ZL3b"]["pearson"]),
                "R_PT_IT2a": float(r["PT_R1"]["topology"]["IT2a"]["pearson"]),
                "R_baseline_ZL3b": float(r["baseline_B2"]["R_ZL3b"]),
                "R_baseline_IT2a": float(r["baseline_B2"]["R_IT2a"]),
                "delta_R_ZL3b": float(d["ZL3b"]),
                "delta_R_IT2a": float(d["IT2a"]),
                "E_PT": float(r["PT_R1"]["residual_energy"]),
                "W_PT": float(r["PT_R1"]["reliability"]["median"]),
                "sign_ZL3b": int(r["PT_R1"]["topology"]["ZL3b"]["sign_agreement"]),
                "sign_IT2a": int(r["PT_R1"]["topology"]["IT2a"]["sign_agreement"]),
            })
            for t in TARGETS:
                all_case_delta[t].append(float(d[t]))
        for t in TARGETS:
            ds = [float(r["delta_R_randomized_minus_baseline"][t]) for r in block_rows]
            D = float(statistics.fmean(ds))
            entry["D"][t] = D
            entry["B2_scale_ratio"][t] = {
                "D_over_SD": float(D / B2_SCALE[t]["SD"]),
                "D_over_MAD": float(D / B2_SCALE[t]["MAD"]),
            }
            per_target_D[t].append(D)
        entry["direction"] = (
            "both_negative" if entry["D"]["ZL3b"] < 0 and entry["D"]["IT2a"] < 0
            else "both_nonnegative" if entry["D"]["ZL3b"] >= 0 and entry["D"]["IT2a"] >= 0
            else "mixed"
        )
        assignments.append(entry)

    readings = {}
    for t in TARGETS:
        Ds = per_target_D[t]
        nonloss = sum(x >= 0 for x in Ds)
        readings[t] = {
            "D_summary": summarize(Ds),
            "case_delta_summary_155": summarize(all_case_delta[t]),
            "nonloss_count": int(nonloss),
            "loss_count": int(31 - nonloss),
            "p_nonloss": float((1 + nonloss) / 32),
            "B2_scale": B2_SCALE[t],
            "D_over_SD_summary": summarize([x / B2_SCALE[t]["SD"] for x in Ds]),
            "D_over_MAD_summary": summarize([x / B2_SCALE[t]["MAD"] for x in Ds]),
        }
    p_both = max(readings[t]["p_nonloss"] for t in TARGETS)
    direction_counts = {
        x: sum(a["direction"] == x for a in assignments)
        for x in ("both_negative", "both_nonnegative", "mixed")
    }

    result = {
        "schema": "issue72-v2-stage-d1-pt-aggregate-v1",
        "status": "STAGE_D1_COMPLETE_PT_TOTAL_EFFECT_AGGREGATED",
        "population": {
            "j_values": list(range(31)),
            "reps": list(range(5)),
            "total_results": 155,
            "complete_population": True,
            "blocks_are_rng_paths_not_independent_texts": True,
        },
        "scientific_role": "WITHIN_LINE_EFFECTIVE_PLAINTEXT_ORDER_FULL_PIPELINE_TOTAL_EFFECT_ON_R1",
        "target_authority": target_authority,
        "static_authority": static_authority,
        "readings": readings,
        "p_both": float(p_both),
        "assignment_direction_counts": direction_counts,
        "coverage": summarize(all_coverage),
        "assignments": assignments,
        "aggregation_policy": {
            "D_is_equal_mean_over_rep0_rep4": True,
            "hard_intervention_threshold_applied": False,
            "readings_averaged": False,
            "coverage_gate_applied": False,
            "B2_scale_is_context_not_threshold": True,
            "p_nonloss_is_finite_randomization_evidence_not_universal_pvalue_gate": True,
        },
        "classification": None,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "direction_counts": direction_counts,
        "p_nonloss": {t: readings[t]["p_nonloss"] for t in TARGETS},
        "p_both": p_both,
        "D_median": {t: readings[t]["D_summary"]["median"] for t in TARGETS},
        "D_mean": {t: readings[t]["D_summary"]["mean"] for t in TARGETS},
        "coverage": result["coverage"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
