#!/usr/bin/env python3
"""Aggregate Issue #75 Phase C M3-KRS-CHAIN first-reveal population."""
from __future__ import annotations

import glob
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve().parent
PHASE_A_AGG_PATH = HERE / "stage-a-first-reveal" / "phase75a_aggregate.json"
PHASE_A_AGG_SHA256 = "fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540"
C0_FREEZE_PATH = HERE / "C0_FREEZE_C.md"
FAMILY = "M3-KRS-CHAIN"
N_REPS = 31
PRIMARY_DELTA_PLUS = 0.009768313008182594
SUFFICIENT = "M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_SUFFICIENT"
INSUFFICIENT = "M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_c0_sha() -> str:
    import re
    text = C0_FREEZE_PATH.read_text(encoding="utf-8")
    m = re.search(r"C0 authority SHA-256: `([0-9a-f]{64})`", text)
    if not m:
        raise RuntimeError("C0 SHA missing from freeze metadata")
    return m.group(1)


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
    if not ys or any(not math.isfinite(x) for x in ys):
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
    if r.get("positive_control", {}).get("valid") is not True:
        raise RuntimeError("Phase A positive control is not valid")
    if float(r["primary_q95_equivalence"]["delta_plus"]) != PRIMARY_DELTA_PLUS:
        raise RuntimeError("Phase A q95 tolerance changed")
    if r.get("population", {}).get("total_results") != 124:
        raise RuntimeError("Phase A complete population changed")
    centers = [float(x) for x in r["paired_values"]["T_plus_center"]]
    if len(centers) != N_REPS:
        raise RuntimeError("Phase A paired center population changed")
    return r


def validate_case(r: Mapping, rep: int, c0_sha: str) -> None:
    if r.get("schema") != "issue75-phaseC-m3-r1-score-v1":
        raise RuntimeError(f"bad Phase C score schema rep {rep}")
    if r.get("status") != "PHASE_C_M3_FIRST_REVEAL_CASE_SCORED":
        raise RuntimeError(f"bad Phase C score status rep {rep}")
    if r.get("family") != FAMILY or int(r.get("rep", -1)) != rep:
        raise RuntimeError(f"Phase C case identity changed rep {rep}")
    if r.get("pair_count") != 66 or r.get("target_readings_averaged") is not False:
        raise RuntimeError(f"Phase C scoring contract changed rep {rep}")
    if r.get("no_case_selection") is not True or r.get("no_reroll") is not True:
        raise RuntimeError(f"Phase C selection guardrail changed rep {rep}")
    a = r.get("candidate_audit", {})
    if a.get("phase_c0_authority_sha256") != c0_sha or a.get("exact_phase_c0_replay") is not True:
        raise RuntimeError(f"Phase C0 replay authority changed rep {rep}")
    if a.get("training_unary_moments_exact_c0") is not True:
        raise RuntimeError(f"Phase C unary authority changed rep {rep}")
    if a.get("training_adjacent_moments_exact_c0") is not True:
        raise RuntimeError(f"Phase C adjacent authority changed rep {rep}")
    if a.get("descriptor_distribution_exact_c0") is not True:
        raise RuntimeError(f"Phase C descriptor authority changed rep {rep}")
    if a.get("fit_tolerance_revalidated") is not True or float(a.get("regenerated_fit_max_abs_reported_moment_error")) > 1e-10:
        raise RuntimeError(f"Phase C fit replay invalid rep {rep}")
    if a.get("tokens") != 25071 or a.get("fold_tokens") != [4430,4810,5516,5447,4868] or a.get("all_zero_count") != 0:
        raise RuntimeError(f"Phase C population changed rep {rep}")
    m = r.get("measurement", {})
    if m.get("reference_namespace") != f"issue75:phaseC:M3-KRS-CHAIN:rep{rep}:reference":
        raise RuntimeError(f"Phase C reference namespace changed rep {rep}")
    if m.get("test_namespace") != f"issue75:phaseC:M3-KRS-CHAIN:rep{rep}:test":
        raise RuntimeError(f"Phase C test namespace changed rep {rep}")
    if m.get("n_reference") != 1000 or m.get("n_test") != 1000 or len(m.get("z_full", [])) != 66:
        raise RuntimeError(f"Phase C null contract changed rep {rep}")
    if not math.isfinite(float(m.get("residual_energy"))) or not 0 < float(m.get("p_exist")) <= 1:
        raise RuntimeError(f"Phase C residual diagnostics invalid rep {rep}")
    for name in ("ZL3b", "IT2a"):
        t = r.get("topology", {}).get(name, {})
        if not math.isfinite(float(t.get("pearson"))) or t.get("sign_denominator") != 66 or not 0 <= int(t.get("sign_agreement")) <= 66:
            raise RuntimeError(f"Phase C topology invalid rep {rep} {name}")
    T = float(r.get("T"))
    if abs(T - min(float(r["topology"]["ZL3b"]["pearson"]), float(r["topology"]["IT2a"]["pearson"]))) > 1e-15:
        raise RuntimeError(f"Phase C T mismatch rep {rep}")
    if any(v is not True for v in r.get("target_access", {}).values()):
        raise RuntimeError(f"Phase C target access record incomplete rep {rep}")


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} INPUT_DIR OUTPUT_JSON SCIENTIFIC_HEAD")
    inp = Path(argv[1]).resolve()
    out = Path(argv[2]).resolve()
    scientific_head = argv[3].strip()
    c0_sha = expected_c0_sha()

    paths = sorted(glob.glob(str(inp / "*.json")))
    if len(paths) != N_REPS:
        raise RuntimeError(f"need exactly 31 Phase C score JSON files, found {len(paths)}")
    rows = {}
    target_authority = None
    for p in paths:
        r = json.loads(Path(p).read_text(encoding="utf-8"))
        rep = int(r.get("rep", -1))
        if rep not in range(N_REPS) or rep in rows:
            raise RuntimeError(f"unexpected/duplicate Phase C rep {rep}")
        validate_case(r, rep, c0_sha)
        if target_authority is None:
            target_authority = r["target_authority"]
        elif r["target_authority"] != target_authority:
            raise RuntimeError("Phase C target authority differs across reps")
        rows[rep] = r
    if set(rows) != set(range(N_REPS)):
        raise RuntimeError("Phase C complete population mismatch")

    phase_a = load_phase_a()
    plus_center = [float(x) for x in phase_a["paired_values"]["T_plus_center"]]
    T = [float(rows[r]["T"]) for r in range(N_REPS)]
    diffs = [T[r] - plus_center[r] for r in range(N_REPS)]
    gap = float(statistics.median(diffs))
    sufficient = bool(gap >= -PRIMARY_DELTA_PLUS)
    classification = SUFFICIENT if sufficient else INSUFFICIENT
    q90_delta = float(phase_a["nonpromoting_tolerance_sensitivity"]["q90"]["delta_plus"])
    q99_delta = float(phase_a["nonpromoting_tolerance_sensitivity"]["q99"]["delta_plus"])

    result = {
        "schema": "issue75-phaseC-m3-aggregate-v1",
        "status": "PHASE_C_M3_COMPLETE_31_CASE_POPULATION_AGGREGATED",
        "scientific_head": scientific_head,
        "phase_c0_authority_sha256": c0_sha,
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
            "D_M3_minus_phaseA_plus_center": diffs,
            "gap_M3": gap,
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
        "model_complexity": {
            "free_continuous_parameters_per_fold": 21,
            "free_unary_parameters": 11,
            "free_adjacent_interaction_parameters": 10,
            "explicit_nonadjacent_pair_interaction_parameters": 0,
            "empirical_signature_specific_parameters": 0,
        },
        "guardrails": {
            "target_edge_loss_optimized": False,
            "selected_nonadjacent_edges_used": False,
            "readings_averaged": False,
            "phase_a_positive_control_rerun_or_reselected": False,
            "post_reveal_r1_model_added": False,
        },
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(raw, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "T_median": result["measurement"]["T"]["median"],
                "R_ZL3b_median": result["measurement"]["R_ZL3b"]["median"],
                "R_IT2a_median": result["measurement"]["R_IT2a"]["median"],
                "E_median": result["measurement"]["residual_energy"]["median"],
                "W_median": None if result["measurement"]["reliability_W"]["finite"] is None else result["measurement"]["reliability_W"]["finite"]["median"],
                "gap_M3": gap,
                "delta_plus_q95": PRIMARY_DELTA_PLUS,
                "classification": classification,
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
