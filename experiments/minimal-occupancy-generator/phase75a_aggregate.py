#!/usr/bin/env python3
"""Aggregate the complete Issue #75 Phase A first-reveal population."""
from __future__ import annotations

import glob
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Mapping, Sequence

PLAN_COMMIT = "8d984cfa61a5616bef61b45248c0a7a5d213fbf8"
SCORER_FREEZE_COMMIT = "21e7bbc176e593ef9fa025113fb17799ca500d8e"
A0_SHA256 = "83e5808576a6416e4b03e302242805509c05d16928403d3a58e5636bdbf9ecd2"
FAMILIES = ("M0", "M1", "MPLUS-A", "MPLUS-B")
N_REPS = 31
EXPECTED = {(f, r) for f in FAMILIES for r in range(N_REPS)}
T_CONTROL_FLOOR = 0.9447148364


def quantile_linear(xs: Sequence[float], q: float) -> float:
    ys = sorted(float(x) for x in xs)
    p = (len(ys) - 1) * q
    lo = int(math.floor(p))
    hi = int(math.ceil(p))
    if lo == hi:
        return ys[lo]
    return float(ys[lo] * (hi - p) + ys[hi] * (p - lo))


def empirical_higher_quantile(xs: Sequence[float], q: float) -> float:
    """Empirical order-statistic quantile: x_(ceil(q*n)), 1-indexed."""
    ys = sorted(float(x) for x in xs)
    if not ys or not 0.0 < q <= 1.0:
        raise ValueError((len(ys), q))
    idx = max(0, min(len(ys) - 1, int(math.ceil(q * len(ys))) - 1))
    return float(ys[idx])


def summary(xs: Sequence[float]) -> dict:
    ys = [float(x) for x in xs]
    if not ys or any(not math.isfinite(x) for x in ys):
        raise RuntimeError("non-finite required summary value")
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
    out = {"n_total": len(xs), "n_finite": len(vals)}
    if vals:
        out["finite"] = summary(vals)
    else:
        out["finite"] = None
    return out


def validate_case(r: Mapping, key: tuple[str, int]) -> None:
    family, rep = key
    if r.get("schema") != "issue75-phaseA-r1-score-v1":
        raise RuntimeError(f"bad score schema {key}")
    if r.get("status") != "PHASE_A_GENERATOR_R1_FIRST_REVEAL_CASE_SCORED":
        raise RuntimeError(f"bad score status {key}")
    if r.get("plan_commit") != PLAN_COMMIT:
        raise RuntimeError(f"plan authority changed {key}")
    if r.get("family") != family or int(r.get("rep", -1)) != rep:
        raise RuntimeError(f"case identity changed {key}")
    if r.get("pair_count") != 66 or r.get("target_readings_averaged") is not False:
        raise RuntimeError(f"R1 measurement contract changed {key}")
    if r.get("no_case_selection") is not True or r.get("no_reroll") is not True:
        raise RuntimeError(f"case-selection guardrail changed {key}")
    audit = r.get("candidate_audit", {})
    if audit.get("stage_a0_authority_sha256") != A0_SHA256 or audit.get("exact_stage_a0_replay") is not True:
        raise RuntimeError(f"Stage A0 replay authority changed {key}")
    if audit.get("tokens") != 25071 or audit.get("fold_tokens") != [4430, 4810, 5516, 5447, 4868]:
        raise RuntimeError(f"candidate population changed {key}")
    if audit.get("all_zero_count") != 0:
        raise RuntimeError(f"zero occupancy signature appeared {key}")
    m = r.get("measurement", {})
    if m.get("reference_namespace") != f"issue75:phaseA:{family}:rep{rep}:reference":
        raise RuntimeError(f"reference namespace changed {key}")
    if m.get("test_namespace") != f"issue75:phaseA:{family}:rep{rep}:test":
        raise RuntimeError(f"test namespace changed {key}")
    if m.get("n_reference") != 1000 or m.get("n_test") != 1000:
        raise RuntimeError(f"null population changed {key}")
    if len(m.get("z_full", [])) != 66:
        raise RuntimeError(f"residual vector length changed {key}")
    if not math.isfinite(float(m.get("residual_energy"))) or not 0.0 < float(m.get("p_exist")) <= 1.0:
        raise RuntimeError(f"invalid residual diagnostics {key}")
    top = r.get("topology", {})
    for target in ("ZL3b", "IT2a"):
        x = top.get(target, {})
        if not math.isfinite(float(x.get("pearson"))) or x.get("sign_denominator") != 66:
            raise RuntimeError(f"invalid topology {key} {target}")
        if not 0 <= int(x.get("sign_agreement")) <= 66:
            raise RuntimeError(f"invalid sign agreement {key} {target}")
    T = float(r.get("T"))
    expected_t = min(float(top["ZL3b"]["pearson"]), float(top["IT2a"]["pearson"]))
    if not math.isfinite(T) or abs(T - expected_t) > 1e-15:
        raise RuntimeError(f"T mismatch {key}")
    ta = r.get("target_access", {})
    if not ta or any(v is not True for v in ta.values()):
        raise RuntimeError(f"target-access record incomplete {key}")


def tolerance_classification(rows: Mapping, q: float) -> dict:
    plus_a = [float(rows[("MPLUS-A", r)]["T"]) for r in range(N_REPS)]
    plus_b = [float(rows[("MPLUS-B", r)]["T"]) for r in range(N_REPS)]
    center = [(a + b) / 2.0 for a, b in zip(plus_a, plus_b)]
    self_diff = [abs(a - b) for a, b in zip(plus_a, plus_b)]
    delta = empirical_higher_quantile(self_diff, q)
    gaps = {}
    ok = {}
    for family in ("M0", "M1"):
        diffs = [float(rows[(family, r)]["T"]) - center[r] for r in range(N_REPS)]
        gap = float(statistics.median(diffs))
        gaps[family] = gap
        ok[family] = bool(gap >= -delta)
    if ok["M0"]:
        cls = "M0_INDEPENDENT_SLOT_MARGINALS_SUFFICIENT"
    elif ok["M1"]:
        cls = "M1_MARGINALS_PLUS_OCCUPANCY_COUNT_SUFFICIENT"
    else:
        cls = "LOW_ORDER_MODELS_INSUFFICIENT_EMPIRICAL_PATTERN_STRUCTURE_REQUIRED"
    return {
        "q": q,
        "empirical_order_statistic_definition": "sorted_x[ceil(q*n)-1]",
        "delta_plus": delta,
        "gap": gaps,
        "no_material_loss": ok,
        "classification_if_positive_control_valid": cls,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} INPUT_DIR OUTPUT_JSON SCIENTIFIC_HEAD")
    inp = Path(argv[1]).resolve()
    out_path = Path(argv[2]).resolve()
    scientific_head = argv[3].strip()

    paths = sorted(glob.glob(str(inp / "*.json")))
    if len(paths) != len(EXPECTED):
        raise RuntimeError(f"need exactly 124 score JSON files, found {len(paths)}")
    rows = {}
    target_authority = None
    for p in paths:
        r = json.loads(Path(p).read_text(encoding="utf-8"))
        key = (str(r.get("family")), int(r.get("rep", -1)))
        if key not in EXPECTED or key in rows:
            raise RuntimeError(f"unexpected/duplicate score result {key}")
        validate_case(r, key)
        if target_authority is None:
            target_authority = r["target_authority"]
        elif r["target_authority"] != target_authority:
            raise RuntimeError("target authority differs across Phase A cases")
        rows[key] = r
    if set(rows) != EXPECTED:
        raise RuntimeError("Phase A complete population mismatch")

    families = {}
    for family in FAMILIES:
        rs = [rows[(family, r)] for r in range(N_REPS)]
        families[family] = {
            "n": N_REPS,
            "T": summary([x["T"] for x in rs]),
            "R_ZL3b": summary([x["topology"]["ZL3b"]["pearson"] for x in rs]),
            "R_IT2a": summary([x["topology"]["IT2a"]["pearson"] for x in rs]),
            "sign_ZL3b": summary([x["topology"]["ZL3b"]["sign_agreement"] for x in rs]),
            "sign_IT2a": summary([x["topology"]["IT2a"]["sign_agreement"] for x in rs]),
            "residual_energy": summary([x["measurement"]["residual_energy"] for x in rs]),
            "p_exist": summary([x["measurement"]["p_exist"] for x in rs]),
            "reliability_W": optional_summary([x["measurement"]["reliability"]["median"] for x in rs]),
        }

    control_a = families["MPLUS-A"]["T"]["median"]
    control_b = families["MPLUS-B"]["T"]["median"]
    control_valid = bool(control_a >= T_CONTROL_FLOOR and control_b >= T_CONTROL_FLOOR)
    primary = tolerance_classification(rows, 0.95)
    if control_valid:
        classification = primary["classification_if_positive_control_valid"]
    else:
        classification = "POSITIVE_CONTROL_CALIBRATION_FAILED_STOP"

    plus_a = [float(rows[("MPLUS-A", r)]["T"]) for r in range(N_REPS)]
    plus_b = [float(rows[("MPLUS-B", r)]["T"]) for r in range(N_REPS)]
    plus_center = [(a + b) / 2.0 for a, b in zip(plus_a, plus_b)]
    plus_self = [abs(a - b) for a, b in zip(plus_a, plus_b)]
    paired = {
        "T_plus_center": plus_center,
        "D_plus_self": plus_self,
        "M0_minus_plus_center": [float(rows[("M0", r)]["T"]) - plus_center[r] for r in range(N_REPS)],
        "M1_minus_plus_center": [float(rows[("M1", r)]["T"]) - plus_center[r] for r in range(N_REPS)],
    }

    result = {
        "schema": "issue75-phaseA-aggregate-v1",
        "status": "PHASE_A_COMPLETE_124_CASE_POPULATION_AGGREGATED",
        "scientific_head": scientific_head,
        "plan_commit": PLAN_COMMIT,
        "scorer_freeze_commit": SCORER_FREEZE_COMMIT,
        "stage_a0_authority_sha256": A0_SHA256,
        "population": {
            "families": list(FAMILIES),
            "n_reps_per_family": N_REPS,
            "total_results": 124,
            "complete_population": True,
            "no_drops": True,
            "no_rerolls": True,
        },
        "target_authority": target_authority,
        "families": families,
        "positive_control": {
            "T_control_floor": T_CONTROL_FLOOR,
            "threshold_source": "T2 lower frozen pooled within-reading residual reliability",
            "MPLUS_A_median_T": control_a,
            "MPLUS_B_median_T": control_b,
            "valid": control_valid,
        },
        "primary_q95_equivalence": primary,
        "paired_values": paired,
        "ordered_classification": classification,
        "nonpromoting_tolerance_sensitivity": {
            "q90": tolerance_classification(rows, 0.90),
            "q99": tolerance_classification(rows, 0.99),
        },
        "model_complexity": {
            "M0": {"slot_main_effect_parameters_per_fold": 12, "pair_interaction_parameters": 0},
            "M1": {"free_slot_main_effect_parameters_per_fold": 11, "K_distribution_independent_probabilities_at_most": 11, "pair_interaction_parameters": 0},
            "MPLUS-A": {"role": "empirical_signature_resampling_positive_control_not_mechanistic_model"},
            "MPLUS-B": {"role": "independent_empirical_signature_resampling_positive_control_bank"},
        },
        "guardrails": {
            "target_edge_loss_optimized": False,
            "selected_edges_used": False,
            "reading_targets_averaged": False,
            "arbitrary_round_R_threshold_used": False,
            "post_reveal_family_added": False,
            "M2_or_M3_executed": False,
        },
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(raw, encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "positive_control_valid": control_valid,
        "MPLUS_A_median_T": control_a,
        "MPLUS_B_median_T": control_b,
        "delta_plus_q95": primary["delta_plus"],
        "gap_M0": primary["gap"]["M0"],
        "gap_M1": primary["gap"]["M1"],
        "classification": classification,
        "T_medians": {f: families[f]["T"]["median"] for f in FAMILIES},
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
