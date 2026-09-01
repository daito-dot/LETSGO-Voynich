#!/usr/bin/env python3
"""Aggregate Issue #75 Phase B M2-KRS first-reveal population."""
from __future__ import annotations

import glob
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Mapping, Sequence

PLAN_B_COMMIT = "f09ba414de015eabd1eef03f275be68b82752d7f"
B0_SHA256 = "9c180c7026e4f9464954dd029b71973cc1890f25223af6152959649dde57e834"
PHASE_A_AGG_PATH = Path(__file__).resolve().parent / "stage-a-first-reveal" / "phase75a_aggregate.json"
PHASE_A_AGG_SHA256 = "fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540"
FAMILY = "M2-KRS"
N_REPS = 31
PRIMARY_DELTA_PLUS = 0.009768313008182594


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quantile_linear(xs: Sequence[float], q: float) -> float:
    ys = sorted(float(x) for x in xs)
    p = (len(ys) - 1) * q
    lo = int(math.floor(p))
    hi = int(math.ceil(p))
    if lo == hi:
        return ys[lo]
    return float(ys[lo] * (hi - p) + ys[hi] * (p - lo))


def summary(xs: Sequence[float]) -> dict:
    ys = [float(x) for x in xs]
    if len(ys) == 0 or any(not math.isfinite(x) for x in ys):
        raise RuntimeError("invalid required summary")
    return {
        "n": len(ys),
        "min": min(ys),
        "q25": quantile_linear(ys, 0.25),
        "median": float(statistics.median(ys)),
        "q75": quantile_linear(ys, 0.75),
        "max": max(ys),
        "mean": float(statistics.fmean(ys)),
        "sd_population": float(statistics.pstdev(ys)),
    }


def optional_summary(xs: Sequence[float | None]) -> dict:
    vals = [float(x) for x in xs if x is not None and math.isfinite(float(x))]
    return {"n_total": len(xs), "n_finite": len(vals), "finite": None if not vals else summary(vals)}


def load_phase_a() -> dict:
    got = sha256_file(PHASE_A_AGG_PATH)
    if got != PHASE_A_AGG_SHA256:
        raise RuntimeError(f"Phase A aggregate SHA changed: {got}")
    r = json.loads(PHASE_A_AGG_PATH.read_text(encoding="utf-8"))
    if r.get("schema") != "issue75-phaseA-aggregate-v1":
        raise RuntimeError("Phase A aggregate schema changed")
    if r.get("population", {}).get("total_results") != 124 or r.get("population", {}).get("complete_population") is not True:
        raise RuntimeError("Phase A positive-control authority incomplete")
    if r.get("positive_control", {}).get("valid") is not True:
        raise RuntimeError("Phase A positive-control authority not valid")
    if float(r["primary_q95_equivalence"]["delta_plus"]) != PRIMARY_DELTA_PLUS:
        raise RuntimeError("Phase A q95 tolerance changed")
    centers = [float(x) for x in r["paired_values"]["T_plus_center"]]
    if len(centers) != N_REPS:
        raise RuntimeError("Phase A paired center population changed")
    return r


def validate_case(r: Mapping, rep: int) -> None:
    if r.get("schema") != "issue75-phaseB-m2-r1-score-v1":
        raise RuntimeError(f"bad Phase B score schema rep {rep}")
    if r.get("status") != "PHASE_B_M2_FIRST_REVEAL_CASE_SCORED":
        raise RuntimeError(f"bad Phase B score status rep {rep}")
    if r.get("plan_b_commit") != PLAN_B_COMMIT or r.get("family") != FAMILY or int(r.get("rep", -1)) != rep:
        raise RuntimeError(f"Phase B case identity changed rep {rep}")
    if r.get("pair_count") != 66 or r.get("target_readings_averaged") is not False:
        raise RuntimeError(f"Phase B scoring contract changed rep {rep}")
    if r.get("no_case_selection") is not True or r.get("no_reroll") is not True:
        raise RuntimeError(f"Phase B selection guardrail changed rep {rep}")
    a = r.get("candidate_audit", {})
    if a.get("phase_b0_authority_sha256") != B0_SHA256 or a.get("exact_phase_b0_replay") is not True:
        raise RuntimeError(f"Phase B0 replay authority changed rep {rep}")
    if a.get("training_slot_marginals_exact_b0") is not True or a.get("descriptor_distribution_exact_b0") is not True:
        raise RuntimeError(f"Phase B training authority changed rep {rep}")
    if a.get("fit_tolerance_revalidated") is not True or float(a.get("regenerated_fit_max_abs_marginal_error")) > 1e-10:
        raise RuntimeError(f"Phase B fit replay invalid rep {rep}")
    if a.get("tokens") != 25071 or a.get("fold_tokens") != [4430,4810,5516,5447,4868] or a.get("all_zero_count") != 0:
        raise RuntimeError(f"Phase B population changed rep {rep}")
    m = r.get("measurement", {})
    if m.get("reference_namespace") != f"issue75:phaseB:M2-KRS:rep{rep}:reference":
        raise RuntimeError(f"Phase B reference namespace changed rep {rep}")
    if m.get("test_namespace") != f"issue75:phaseB:M2-KRS:rep{rep}:test":
        raise RuntimeError(f"Phase B test namespace changed rep {rep}")
    if m.get("n_reference") != 1000 or m.get("n_test") != 1000 or len(m.get("z_full", [])) != 66:
        raise RuntimeError(f"Phase B null contract changed rep {rep}")
    if not math.isfinite(float(m.get("residual_energy"))) or not 0 < float(m.get("p_exist")) <= 1:
        raise RuntimeError(f"Phase B residual diagnostics invalid rep {rep}")
    for name in ("ZL3b", "IT2a"):
        t = r.get("topology", {}).get(name, {})
        if not math.isfinite(float(t.get("pearson"))) or t.get("sign_denominator") != 66 or not 0 <= int(t.get("sign_agreement")) <= 66:
            raise RuntimeError(f"Phase B topology invalid rep {rep} {name}")
    T = float(r.get("T"))
    if abs(T - min(float(r["topology"]["ZL3b"]["pearson"]), float(r["topology"]["IT2a"]["pearson"]))) > 1e-15:
        raise RuntimeError(f"Phase B T mismatch rep {rep}")
    if any(v is not True for v in r.get("target_access", {}).values()):
        raise RuntimeError(f"Phase B target access record incomplete rep {rep}")


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} INPUT_DIR OUTPUT_JSON SCIENTIFIC_HEAD")
    inp = Path(argv[1]).resolve()
    out = Path(argv[2]).resolve()
    scientific_head = argv[3].strip()

    paths = sorted(glob.glob(str(inp / "*.json")))
    if len(paths) != N_REPS:
        raise RuntimeError(f"need exactly 31 Phase B score JSON files, found {len(paths)}")
    rows = {}
    target_authority = None
    for p in paths:
        r = json.loads(Path(p).read_text(encoding="utf-8"))
        rep = int(r.get("rep", -1))
        if rep not in range(N_REPS) or rep in rows:
            raise RuntimeError(f"unexpected/duplicate Phase B rep {rep}")
        validate_case(r, rep)
        if target_authority is None:
            target_authority = r["target_authority"]
        elif r["target_authority"] != target_authority:
            raise RuntimeError("Phase B target authority differs across reps")
        rows[rep] = r
    if set(rows) != set(range(N_REPS)):
        raise RuntimeError("Phase B complete population mismatch")

    phase_a = load_phase_a()
    plus_center = [float(x) for x in phase_a["paired_values"]["T_plus_center"]]
    T = [float(rows[r]["T"]) for r in range(N_REPS)]
    diffs = [T[r] - plus_center[r] for r in range(N_REPS)]
    gap = float(statistics.median(diffs))
    sufficient = bool(gap >= -PRIMARY_DELTA_PLUS)
    classification = (
        "M2_GENERIC_KRS_SHAPE_DESCRIPTORS_SUFFICIENT"
        if sufficient
        else "M2_GENERIC_KRS_SHAPE_DESCRIPTORS_INSUFFICIENT_STATEFUL_CONFIGURATION_RULE_REQUIRED"
    )

    q90_delta = float(phase_a["nonpromoting_tolerance_sensitivity"]["q90"]["delta_plus"])
    q99_delta = float(phase_a["nonpromoting_tolerance_sensitivity"]["q99"]["delta_plus"])

    result = {
        "schema": "issue75-phaseB-m2-aggregate-v1",
        "status": "PHASE_B_M2_COMPLETE_31_CASE_POPULATION_AGGREGATED",
        "scientific_head": scientific_head,
        "plan_b_commit": PLAN_B_COMMIT,
        "phase_b0_authority_sha256": B0_SHA256,
        "phase_a_positive_control_aggregate_sha256": PHASE_A_AGG_SHA256,
        "population": {
            "family": FAMILY,
            "n_reps": N_REPS,
            "total_results": N_REPS,
            "complete_population": True,
            "no_drops": True,
            "no_rerolls": True,
        },
        "target_authority": target_authority,
        "measurement": {
            "T": summary(T),
            "R_ZL3b": summary([rows[r]["topology"]["ZL3b"]["pearson"] for r in range(N_REPS)]),
            "R_IT2a": summary([rows[r]["topology"]["IT2a"]["pearson"] for r in range(N_REPS)]),
            "sign_ZL3b": summary([rows[r]["topology"]["ZL3b"]["sign_agreement"] for r in range(N_REPS)]),
            "sign_IT2a": summary([rows[r]["topology"]["IT2a"]["sign_agreement"] for r in range(N_REPS)]),
            "residual_energy": summary([rows[r]["measurement"]["residual_energy"] for r in range(N_REPS)]),
            "p_exist": summary([rows[r]["measurement"]["p_exist"] for r in range(N_REPS)]),
            "reliability_W": optional_summary([rows[r]["measurement"]["reliability"]["median"] for r in range(N_REPS)]),
        },
        "frozen_phase_a_positive_control": {
            "MPLUS_A_median_T": float(phase_a["positive_control"]["MPLUS_A_median_T"]),
            "MPLUS_B_median_T": float(phase_a["positive_control"]["MPLUS_B_median_T"]),
            "positive_control_valid": bool(phase_a["positive_control"]["valid"]),
            "T_plus_center": plus_center,
            "delta_plus_q95": PRIMARY_DELTA_PLUS,
        },
        "primary": {
            "D_M2_minus_phaseA_plus_center": diffs,
            "gap_M2": gap,
            "sufficiency_threshold": -PRIMARY_DELTA_PLUS,
            "no_material_loss": sufficient,
            "classification": classification,
        },
        "nonpromoting_tolerance_sensitivity": {
            "q90_delta_plus": q90_delta,
            "q90_no_material_loss": bool(gap >= -q90_delta),
            "q99_delta_plus": q99_delta,
            "q99_no_material_loss": bool(gap >= -q99_delta),
        },
        "guardrails": {
            "target_edge_loss_optimized": False,
            "selected_edges_used": False,
            "readings_averaged": False,
            "phase_a_positive_control_rerun_or_reselected": False,
            "M3_executed": False,
        },
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(raw, encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "T_median": result["measurement"]["T"]["median"],
        "R_ZL3b_median": result["measurement"]["R_ZL3b"]["median"],
        "R_IT2a_median": result["measurement"]["R_IT2a"]["median"],
        "E_median": result["measurement"]["residual_energy"]["median"],
        "W_median": None if result["measurement"]["reliability_W"]["finite"] is None else result["measurement"]["reliability_W"]["finite"]["median"],
        "gap_M2": gap,
        "delta_plus_q95": PRIMARY_DELTA_PLUS,
        "classification": classification,
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
