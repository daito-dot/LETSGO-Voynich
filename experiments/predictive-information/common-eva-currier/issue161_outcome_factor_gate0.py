#!/usr/bin/env python3
"""Issue #161 Gate0: score-free outcome-only Currier factorization audit.

Reproduce the merged Issue #158 authority and its exact support-matched A/B/POOL
training tables. Build the frozen context-invariant Currier outcome multipliers
from training counts only and audit exact normalization for every retained
previous-terminal context. No real-target EDGE_OUTCOME probability, likelihood,
G_outcome, G_interaction, or scientific classification is computed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
CURRIER_DIR = HERE.parent
if str(CURRIER_DIR) not in sys.path:
    sys.path.insert(0, str(CURRIER_DIR))

import issue158_currier_gate_decomposition_gate0 as G158  # noqa: E402

PLAN_PATH = CURRIER_DIR / "ISSUE161_OUTCOME_ONLY_CURRIER_FACTORIZATION_PLAN.md"
ISSUE158_GATE_PROVENANCE_PATH = CURRIER_DIR / "ISSUE158_GATE0_PROVENANCE.md"
ISSUE158_SCORER_PATH = CURRIER_DIR / "issue158_currier_gate_first_reveal.py"
ISSUE158_FIRST_PROVENANCE_PATH = CURRIER_DIR / "ISSUE158_FIRST_REVEAL_PROVENANCE.md"

EXPECTED = {
    "issue158_gate_result_sha256": "605e0a82817f394176a3e19c972ed409dfb15df60c72df22db3c0cc765e31099",
    "issue158_gate_script_blob": "4dbc919f3e9ededa17d2e10f56de46c98456cdea",
    "issue158_gate_provenance_blob": "07595bf7314cfb71763eba1a810bfd3aaa01a239",
    "issue158_scorer_blob": "e7a70a10dd7b663f3482993b0adfa8f804816158",
    "issue158_first_provenance_blob": "0f3c14d2f592dea020c180669670cafca5ba1b05",
    "issue158_first_result_sha256": "eef6aee7cb202d73a7090c7aca0e9a0df404b46373589a8203da2b80ec1c3107",
    "issue158_merge": "1741bed875a582594dc797ef18e30dd2ef3351ce",
    "issue158_gate_merge": "ca77b7030dec12778ffdeb1d04bee0b30fb00b65",
    "issue161_plan_blob": "68cb29a11cb147c8ecd9e70b3349a4102744e0ed",
    "fold_sha256": "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b",
    "n_folds": 5,
    "alpha_num": 1,
    "alpha_den": 100,
    "V": 32,
    "min_primary_body": 300,
    "min_matched_supported_body": 300,
}

READINGS = ("ZL3b", "IT2a")
REGIMES = ("A", "B")
END_TOKEN = "<END_TOKEN>"
ATOM_OUTCOMES = tuple(G158.G155.ATOM_OUTCOMES)
OUTCOMES = ATOM_OUTCOMES + (END_TOKEN,)


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G158.git_blob(path)


def parse_rational_table(sparse: Sequence[Sequence[object]]) -> dict[str, dict[str, Fraction]]:
    return G158.parse_rational_table(sparse)


def row_mass(table: Mapping[str, Mapping[str, Fraction]], ctx: str) -> Fraction:
    return G158.row_mass(table, ctx)


def verify_entry_authority(zl_path: Path, it_path: Path) -> tuple[dict, str, dict]:
    if len(OUTCOMES) != EXPECTED["V"] or len(set(OUTCOMES)) != EXPECTED["V"]:
        raise RuntimeError("frozen 32-outcome vocabulary identity failed")
    if git_blob(G158.HERE) != EXPECTED["issue158_gate_script_blob"]:
        raise RuntimeError("Issue158 Gate script blob changed")
    if git_blob(ISSUE158_GATE_PROVENANCE_PATH) != EXPECTED["issue158_gate_provenance_blob"]:
        raise RuntimeError("Issue158 Gate provenance blob changed")
    if git_blob(ISSUE158_SCORER_PATH) != EXPECTED["issue158_scorer_blob"]:
        raise RuntimeError("Issue158 scorer blob changed")
    if git_blob(ISSUE158_FIRST_PROVENANCE_PATH) != EXPECTED["issue158_first_provenance_blob"]:
        raise RuntimeError("Issue158 first-reveal provenance blob changed")
    if git_blob(PLAN_PATH) != EXPECTED["issue161_plan_blob"]:
        raise RuntimeError("Issue161 frozen plan blob changed")

    gate158 = G158.run_gate(zl_path, it_path)
    gate158_sha = sha256_obj(gate158)
    if gate158_sha != EXPECTED["issue158_gate_result_sha256"]:
        raise RuntimeError(f"Issue158 Gate result SHA changed: {gate158_sha}")
    if not gate158.get("gate_pass"):
        raise RuntimeError("Issue158 Gate no longer passes")
    if gate158.get("scientific_currier_gate_metrics_computed") is not False:
        raise RuntimeError("Issue158 Gate firewall changed")
    if gate158["entry_authority"]["fold_identity_sha256"] != EXPECTED["fold_sha256"]:
        raise RuntimeError("physical-leaf fold authority changed")

    gate155 = G158.G155.run_gate(zl_path, it_path)
    gate155_sha = G158.sha256_obj(gate155)
    if gate155_sha != G158.EXPECTED["issue155_gate_result_sha256"]:
        raise RuntimeError("Issue155 Gate no longer reproduces inside Issue161 Gate")
    return gate158, gate158_sha, gate155


def aggregate_outcomes(table: Mapping[str, Mapping[str, Fraction]]) -> dict[str, Fraction]:
    out = {y: Fraction(0, 1) for y in OUTCOMES}
    for ctx in table:
        for y, value in table[ctx].items():
            if y not in out:
                raise RuntimeError(f"table outcome outside frozen vocabulary: {y!r}")
            out[y] += value
    return out


def rational_vector(vec: Mapping[str, Fraction]) -> list[list[object]]:
    return [[y, vec[y].numerator, vec[y].denominator] for y in OUTCOMES]


def build_multiplier(
    regime_agg: Mapping[str, Fraction], pool_agg: Mapping[str, Fraction]
) -> dict[str, Fraction]:
    alpha = Fraction(EXPECTED["alpha_num"], EXPECTED["alpha_den"])
    out = {}
    for y in OUTCOMES:
        out[y] = (regime_agg[y] + alpha) / (pool_agg[y] + alpha)
        if out[y] <= 0:
            raise RuntimeError("nonpositive outcome multiplier")
    return out


def normalized_outcome_conditional(
    pool_table: Mapping[str, Mapping[str, Fraction]],
    ctx: str,
    multiplier: Mapping[str, Fraction],
) -> dict[str, Fraction]:
    alpha = Fraction(EXPECTED["alpha_num"], EXPECTED["alpha_den"])
    mass = row_mass(pool_table, ctx)
    denom = mass + alpha * EXPECTED["V"]
    if denom <= 0:
        raise RuntimeError("nonpositive pooled smoothing denominator")
    raw = {}
    for y in OUTCOMES:
        base = (pool_table.get(ctx, {}).get(y, Fraction(0, 1)) + alpha) / denom
        raw[y] = base * multiplier[y]
        if raw[y] <= 0:
            raise RuntimeError("nonpositive outcome-only raw probability")
    z = sum(raw.values(), Fraction(0, 1))
    if z <= 0:
        raise RuntimeError("nonpositive outcome-only normalizer")
    probs = {y: raw[y] / z for y in OUTCOMES}
    if sum(probs.values(), Fraction(0, 1)) != Fraction(1, 1):
        raise RuntimeError("outcome-only conditional failed exact normalization")
    return probs


def conditional_identity(
    pool_table: Mapping[str, Mapping[str, Fraction]],
    multiplier: Mapping[str, Fraction],
) -> tuple[str, dict]:
    sparse = []
    min_p = None
    max_p = None
    for ctx in sorted(pool_table):
        probs = normalized_outcome_conditional(pool_table, ctx, multiplier)
        for y in OUTCOMES:
            p = probs[y]
            sparse.append([ctx, y, p.numerator, p.denominator])
            min_p = p if min_p is None or p < min_p else min_p
            max_p = p if max_p is None or p > max_p else max_p
    return sha256_obj(sparse), {
        "n_contexts": len(pool_table),
        "n_context_outcome_cells": len(sparse),
        "all_contexts_exactly_normalized": True,
        "min_probability": [min_p.numerator, min_p.denominator],
        "max_probability": [max_p.numerator, max_p.denominator],
    }


def synthetic_test() -> dict:
    # Pure global outcome shift: both contexts move in the same direction.
    pool_global = {
        "c1": {"a": Fraction(2, 1), "b": Fraction(2, 1)},
        "c2": {"a": Fraction(2, 1), "b": Fraction(2, 1)},
    }
    a_global = {
        "c1": {"a": Fraction(3, 1), "b": Fraction(1, 1)},
        "c2": {"a": Fraction(3, 1), "b": Fraction(1, 1)},
    }
    agg_pool = aggregate_outcomes(pool_global)
    agg_a = aggregate_outcomes(a_global)
    w_a = build_multiplier(agg_a, agg_pool)
    p1 = normalized_outcome_conditional(pool_global, "c1", w_a)
    p2 = normalized_outcome_conditional(pool_global, "c2", w_a)
    if not (w_a["a"] > 1 and w_a["b"] < 1 and p1["a"] > p1["b"] and p2["a"] > p2["b"]):
        raise AssertionError("synthetic global outcome shift not represented")

    # Pure context-specific contrast with unchanged aggregate outcome totals.
    pool_interaction = {
        "c1": {"a": Fraction(2, 1), "b": Fraction(2, 1)},
        "c2": {"a": Fraction(2, 1), "b": Fraction(2, 1)},
    }
    a_interaction = {
        "c1": {"a": Fraction(3, 1), "b": Fraction(1, 1)},
        "c2": {"a": Fraction(1, 1), "b": Fraction(3, 1)},
    }
    agg_pool_i = aggregate_outcomes(pool_interaction)
    agg_a_i = aggregate_outcomes(a_interaction)
    w_i = build_multiplier(agg_a_i, agg_pool_i)
    if any(w_i[y] != Fraction(1, 1) for y in OUTCOMES):
        raise AssertionError("synthetic interaction leaked into global outcome multiplier")
    if a_interaction == pool_interaction:
        raise AssertionError("synthetic interaction failed to differ by context")
    p_c1 = normalized_outcome_conditional(pool_interaction, "c1", w_i)
    p_c2 = normalized_outcome_conditional(pool_interaction, "c2", w_i)
    if p_c1 != p_c2:
        raise AssertionError("unit global multiplier unexpectedly created context interaction")

    return {
        "ok": True,
        "uses_real_target_data": False,
        "global_outcome_shift_represented": True,
        "context_specific_contrast_not_absorbed_by_global_multiplier": True,
        "fixed_alpha": [1, 100],
        "V": EXPECTED["V"],
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    gate158, gate158_sha, gate155 = verify_entry_authority(zl_path, it_path)
    outer = []

    for f in range(EXPECTED["n_folds"]):
        r158 = gate158["outer"][f]
        r155 = gate155["outer"][f]
        if int(r158["outer_fold"]) != f or int(r155["outer_fold"]) != f:
            raise RuntimeError("fold order changed")
        if r158["training_union_heldout_overlap"] != []:
            raise RuntimeError("held-out physical-leaf leakage reappeared")

        matched = r155["matched_currier_tables"]
        a_sparse = matched["A_matched_sparse_rational_counts"]
        b_sparse = matched["B_matched_sparse_rational_counts"]
        if G158.G155.sha256_obj(a_sparse) != matched["A_matched_sparse_rational_table_sha256"]:
            raise RuntimeError(f"fold {f} A matched table identity changed")
        if G158.G155.sha256_obj(b_sparse) != matched["B_matched_sparse_rational_table_sha256"]:
            raise RuntimeError(f"fold {f} B matched table identity changed")
        a = parse_rational_table(a_sparse)
        b = parse_rational_table(b_sparse)

        pool_sparse = r158["pooled_table"]["pooled_sparse_rational_counts"]
        if sha256_obj(pool_sparse) != r158["pooled_table"]["pooled_sparse_rational_table_sha256"]:
            raise RuntimeError(f"fold {f} pooled table identity changed")
        pool = parse_rational_table(pool_sparse)
        if set(a) != set(b) or set(a) != set(pool):
            raise RuntimeError(f"fold {f} retained context sets differ")

        agg_a = aggregate_outcomes(a)
        agg_b = aggregate_outcomes(b)
        agg_pool = aggregate_outcomes(pool)
        total_a = sum(agg_a.values(), Fraction(0, 1))
        total_b = sum(agg_b.values(), Fraction(0, 1))
        total_pool = sum(agg_pool.values(), Fraction(0, 1))
        if not (total_a == total_b == total_pool and total_pool > 0):
            raise RuntimeError(f"fold {f} aggregate effective mass equality failed")
        for y in OUTCOMES:
            if agg_pool[y] != Fraction(1, 2) * agg_a[y] + Fraction(1, 2) * agg_b[y]:
                raise RuntimeError(f"fold {f} pooled aggregate outcome identity failed")

        wa = build_multiplier(agg_a, agg_pool)
        wb = build_multiplier(agg_b, agg_pool)
        wa_vec = rational_vector(wa)
        wb_vec = rational_vector(wb)
        pool_vec = rational_vector(agg_pool)
        a_vec = rational_vector(agg_a)
        b_vec = rational_vector(agg_b)
        sha_a_cond, audit_a = conditional_identity(pool, wa)
        sha_b_cond, audit_b = conditional_identity(pool, wb)

        target_support = r158["target_context_support"]
        for reading in READINGS:
            for regime in REGIMES:
                t = target_support[reading][regime]
                if int(t["target_primary_run_body_targets"]) < EXPECTED["min_primary_body"]:
                    raise RuntimeError(f"{reading}/{regime}/fold{f} BODY support below threshold")
                if int(t["matched_context_supported_primary_run_body_targets"]) < EXPECTED[
                    "min_matched_supported_body"
                ]:
                    raise RuntimeError(f"{reading}/{regime}/fold{f} matched support below threshold")
                if t["heldout_current_first_atom_used_for_context_selection"] is not False:
                    raise RuntimeError("target-outcome context-selection firewall changed")

        outer.append(
            {
                "outer_fold": f,
                "heldout_physical_leaves": r158["heldout_physical_leaves"],
                "training_union_heldout_overlap": [],
                "A_matched_table_sha256": matched["A_matched_sparse_rational_table_sha256"],
                "B_matched_table_sha256": matched["B_matched_sparse_rational_table_sha256"],
                "POOL_table_sha256": r158["pooled_table"]["pooled_sparse_rational_table_sha256"],
                "aggregate_total_mass": [total_pool.numerator, total_pool.denominator],
                "aggregate_A_counts": a_vec,
                "aggregate_B_counts": b_vec,
                "aggregate_POOL_counts": pool_vec,
                "aggregate_A_sha256": sha256_obj(a_vec),
                "aggregate_B_sha256": sha256_obj(b_vec),
                "aggregate_POOL_sha256": sha256_obj(pool_vec),
                "W_A": wa_vec,
                "W_B": wb_vec,
                "W_A_sha256": sha256_obj(wa_vec),
                "W_B_sha256": sha256_obj(wb_vec),
                "outcome_only_A_conditional_sha256": sha_a_cond,
                "outcome_only_B_conditional_sha256": sha_b_cond,
                "outcome_only_A_audit": audit_a,
                "outcome_only_B_audit": audit_b,
                "target_context_support": target_support,
            }
        )

    synthetic = synthetic_test()
    return {
        "schema": "issue161-outcome-factor-gate0-v1",
        "issue": 161,
        "phase": "OUTCOME_ONLY_CURRIER_FACTORIZATION_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED OUTCOME-FACTOR SCORER",
        "scientific_outcome_factor_metrics_computed": False,
        "entry_authority": {
            "issue158_gate_reproduced": True,
            "issue158_gate_result_sha256": gate158_sha,
            "issue158_gate_script_blob": EXPECTED["issue158_gate_script_blob"],
            "issue158_gate_provenance_blob": EXPECTED["issue158_gate_provenance_blob"],
            "issue158_scorer_blob": EXPECTED["issue158_scorer_blob"],
            "issue158_first_provenance_blob": EXPECTED["issue158_first_provenance_blob"],
            "issue158_declared_first_reveal_result_sha256": EXPECTED[
                "issue158_first_result_sha256"
            ],
            "issue158_merge": EXPECTED["issue158_merge"],
            "issue158_gate_merge": EXPECTED["issue158_gate_merge"],
            "fold_identity_sha256": EXPECTED["fold_sha256"],
            "issue161_plan_blob_sha1": git_blob(PLAN_PATH),
        },
        "frozen_factorization": {
            "outcomes": list(OUTCOMES),
            "V": EXPECTED["V"],
            "alpha": [EXPECTED["alpha_num"], EXPECTED["alpha_den"]],
            "aggregate_formula": "G_R(y)=sum_c C_R_MATCH(c,y)",
            "multiplier_formula": "W_R(y)=(G_R(y)+alpha)/(G_POOL(y)+alpha)",
            "conditional_formula": "P_OUTCOME_R(y|c) proportional to P_POOL(y|c)*W_R(y)",
            "context_invariant_multiplier": True,
            "currier_by_previous_terminal_interaction": False,
            "target_native_fallback": False,
            "temperature_interpolation_calibration_mixture": False,
        },
        "outer": outer,
        "support_thresholds": {
            "min_target_primary_run_body": EXPECTED["min_primary_body"],
            "min_matched_context_supported_target_primary_run_body": EXPECTED[
                "min_matched_supported_body"
            ],
        },
        "synthetic_test": synthetic,
        "firewall": {
            "scientific_outcome_factor_metrics_computed": False,
            "real_target_EDGE_OUTCOME_probability_computed": False,
            "real_target_EDGE_OUTCOME_likelihood_computed": False,
            "G_outcome_computed": False,
            "G_interaction_computed": False,
            "scientific_classification_computed": False,
            "heldout_target_outcome_used_for_atom_or_context_selection": False,
            "outcome_multiplier_tuned": False,
            "currier_labels_changed": False,
            "support_match_changed": False,
            "alpha_smoothing_temperature_interpolation_fallback_or_mixture_tuned": False,
            "hand_section_domain_conditioning": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
        },
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue161-outcome-factor-gate0-v1",
        "issue": 161,
        "phase": "OUTCOME_ONLY_CURRIER_FACTORIZATION_GATE0",
        "gate_pass": False,
        "gate_disposition": "INVALID CURRIER EDGE FACTORIZATION — GATE0 FAILED",
        "scientific_outcome_factor_metrics_computed": False,
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {
            "post_failure_scientific_repair_allowed": False,
            "post_failure_target_driven_change_allowed": False,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--run", nargs=3, metavar=("ZL3B", "IT2A", "OUT_JSON"))
    ns = ap.parse_args(argv)

    if ns.self_test:
        print(canonical_json(synthetic_test()), end="")
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
