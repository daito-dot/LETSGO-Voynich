#!/usr/bin/env python3
"""Issue #161: frozen first reveal for outcome-only Currier factorization.

Compare the merged Issue #161 regime-neutral pooled edge, its frozen training-only
context-invariant Currier outcome multiplier, and the full target-regime matched
edge. The primary residual is

    G_interaction = bits(EDGE_OUTCOME) - bits(EDGE_REGIME)

which measures held-out information requiring a Currier-specific
previous-terminal x next-initial interaction after the global next-initial bias
has been supplied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
CURRIER_DIR = HERE.parent
COMMON_EDGE_DIR = ROOT / "experiments" / "predictive-information" / "common-eva-edge"
if str(CURRIER_DIR) not in sys.path:
    sys.path.insert(0, str(CURRIER_DIR))
if str(COMMON_EDGE_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_EDGE_DIR))

import issue161_outcome_factor_gate0 as G161  # noqa: E402
import issue158_currier_gate_first_reveal as S158  # noqa: E402
import issue155_common_eva_currier_first_reveal as S155  # noqa: E402

PLAN_PATH = CURRIER_DIR / "ISSUE161_OUTCOME_ONLY_CURRIER_FACTORIZATION_PLAN.md"
GATE_PATH = CURRIER_DIR / "issue161_outcome_factor_gate0.py"
GATE_PROVENANCE_PATH = CURRIER_DIR / "ISSUE161_GATE0_PROVENANCE.md"

EXPECTED_GATE_RESULT_SHA256 = "32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94"
EXPECTED_GATE_SCRIPT_BLOB = "00e5bddc0484b9472bb4fce9dadb89dd52bf578f"
EXPECTED_GATE_PROVENANCE_BLOB = "67e91ba26a76898f679a5182828ab3e9f512d49a"
EXPECTED_PLAN_BLOB = "68cb29a11cb147c8ecd9e70b3349a4102744e0ed"
EXPECTED_GATE_MERGE = "6192e5cbe0a5212d089f890ca26bb7d9a10eedbf"

N_FOLDS = 5
LN2 = math.log(2.0)
READINGS = ("ZL3b", "IT2a")
REGIMES = ("A", "B")
TOL = 1e-12

# Exact Issue #158 first-reveal G_Currier folds. These are authority guards only;
# they are not used to fit the Issue #161 outcome factor or classification.
EXPECTED_ISSUE158_G_CURRIER = {
    "ZL3b": {
        "A": [
            0.10646751913558283,
            -0.030322382464655462,
            0.05905242821935097,
            0.0882553911635231,
            0.09293071427940092,
        ],
        "B": [
            0.14543917242315452,
            0.08923407706349806,
            0.12107682303940592,
            0.11870601716613827,
            0.03157455662404374,
        ],
    },
    "IT2a": {
        "A": [
            0.11245835151272487,
            -0.04055238906849645,
            0.06170815954563302,
            0.06813721290478014,
            0.13737949599598132,
        ],
        "B": [
            0.15010795690244905,
            0.0850797433871957,
            0.12577230082194646,
            0.12143040779973724,
            0.04045015206662228,
        ],
    },
}

VALID_CLASSES = (
    "CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN BOTH A AND B",
    "CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN A ONLY",
    "CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN B ONLY",
    "NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL",
    "INVALID CURRIER EDGE FACTORIZATION",
)

C145 = S158.C145


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G161.git_blob(path)


def parse_vector(rows: Sequence[Sequence[object]]) -> dict[str, Fraction]:
    out = {}
    for row in rows:
        if len(row) != 3:
            raise RuntimeError("invalid rational vector row")
        y = str(row[0])
        out[y] = Fraction(int(row[1]), int(row[2]))
    if tuple(out) != G161.OUTCOMES:
        raise RuntimeError("frozen outcome vector order changed")
    return out


def verify_gate_authority(zl_path: Path, it_path: Path) -> tuple[dict, dict]:
    if git_blob(GATE_PATH) != EXPECTED_GATE_SCRIPT_BLOB:
        raise RuntimeError("Issue161 Gate script blob changed")
    if git_blob(GATE_PROVENANCE_PATH) != EXPECTED_GATE_PROVENANCE_BLOB:
        raise RuntimeError("Issue161 Gate provenance blob changed")
    if git_blob(PLAN_PATH) != EXPECTED_PLAN_BLOB:
        raise RuntimeError("Issue161 plan blob changed")

    gate161 = G161.run_gate(zl_path, it_path)
    gate161_sha = sha256_obj(gate161)
    if gate161_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Issue161 Gate result SHA changed: {gate161_sha}")
    if not gate161.get("gate_pass"):
        raise RuntimeError("Issue161 Gate no longer passes")
    if gate161.get("scientific_outcome_factor_metrics_computed") is not False:
        raise RuntimeError("Issue161 Gate firewall changed")

    gate155 = G161.G158.G155.run_gate(zl_path, it_path)
    gate155_sha = G161.G158.sha256_obj(gate155)
    if gate155_sha != G161.G158.EXPECTED["issue155_gate_result_sha256"]:
        raise RuntimeError("Issue155 Gate no longer reproduces")
    return gate161, gate155


def outcome_token_logp(
    target_model: C145.CommonEdgeModel,
    pool_table: Mapping[str, Mapping[str, Fraction]],
    multiplier: Mapping[str, Fraction],
    syms: Sequence[str],
    is_run_start: bool,
    previous_terminal: str | None,
) -> float:
    syms = list(syms)
    if len(syms) < 2:
        raise RuntimeError("invalid token symbol sequence")
    first, second = syms[0], syms[1]
    ll = 0.0
    if is_run_start:
        ll += target_model.categorical_logp(target_model.start_first, first)
        ll += target_model.categorical_logp(target_model.start_second[first], second)
    else:
        if previous_terminal is None:
            raise RuntimeError("BODY token lacks previous terminal")
        if previous_terminal in pool_table:
            probs = G161.normalized_outcome_conditional(pool_table, previous_terminal, multiplier)
            p = probs[first]
            if p <= 0:
                raise RuntimeError("nonpositive frozen outcome-only probability")
            ll += math.log(float(p))
        else:
            # Frozen unsupported-exact-context rule from #158/#161 Gate0.
            ll += -math.log(C145.V)
        ll += target_model.categorical_logp(target_model.body_second[first], second)

    for j in range(2, len(syms)):
        ll += target_model.run_model.logp(syms[j - 2 : j], syms[j])
    return float(ll)


def score_cell(
    reading: str,
    regime: str,
    target_runs,
    gate161: dict,
    gate155: dict,
) -> dict:
    all_folds = set(range(N_FOLDS))
    outer = []

    for f in range(N_FOLDS):
        train_folds = all_folds - {f}
        target_model = C145.CommonEdgeModel(target_runs, train_folds)
        g161 = gate161["outer"][f]
        g155 = gate155["outer"][f]
        if int(g161["outer_fold"]) != f or int(g155["outer_fold"]) != f:
            raise RuntimeError("fold order changed")

        matched = g155["matched_currier_tables"]
        a = G161.parse_rational_table(matched["A_matched_sparse_rational_counts"])
        b = G161.parse_rational_table(matched["B_matched_sparse_rational_counts"])
        pool, pool_summary = G161.G158.pool_tables(a, b)
        if pool_summary["pooled_sparse_rational_table_sha256"] != g161["POOL_table_sha256"]:
            raise RuntimeError(f"fold {f} pooled table failed Gate identity")
        regime_table = a if regime == "A" else b
        multiplier = parse_vector(g161[f"W_{regime}"])
        if sha256_obj(g161[f"W_{regime}"]) != g161[f"W_{regime}_sha256"]:
            raise RuntimeError(f"fold {f} multiplier identity changed")

        log_pool = []
        log_outcome = []
        log_regime = []
        visible_clean = 0
        primary_body = 0
        supported = 0
        unsupported = 0

        for fold, _leaf, _loc, _line_no, run in target_runs:
            if int(fold) != f:
                continue
            previous_terminal = None
            for ti, record in enumerate(run):
                syms = C145.token_symbols(record["atoms"])
                lp_pool = S155.matched_token_logp(
                    target_model, pool, syms, ti == 0, previous_terminal
                )
                lp_outcome = outcome_token_logp(
                    target_model, pool, multiplier, syms, ti == 0, previous_terminal
                )
                lp_regime = S155.matched_token_logp(
                    target_model, regime_table, syms, ti == 0, previous_terminal
                )
                visible_clean += 1

                if record["slotparser_accepted"]:
                    log_pool.append(float(lp_pool))
                    log_outcome.append(float(lp_outcome))
                    log_regime.append(float(lp_regime))
                    if ti > 0:
                        primary_body += 1
                        if previous_terminal in pool:
                            supported += 1
                        else:
                            unsupported += 1
                previous_terminal = syms[-2]

        if not log_pool or not (len(log_pool) == len(log_outcome) == len(log_regime)):
            raise RuntimeError(f"{reading}/{regime}/fold{f} score alignment failure")
        if not all(math.isfinite(v) for v in log_pool + log_outcome + log_regime):
            raise RuntimeError(f"{reading}/{regime}/fold{f} non-finite score")

        n = len(log_pool)
        bits_pool = float(-sum(log_pool) / (n * LN2))
        bits_outcome = float(-sum(log_outcome) / (n * LN2))
        bits_regime = float(-sum(log_regime) / (n * LN2))
        g_outcome = float(bits_pool - bits_outcome)
        g_interaction = float(bits_outcome - bits_regime)
        g_currier_reproduced = float(bits_pool - bits_regime)

        if not math.isclose(
            g_currier_reproduced,
            EXPECTED_ISSUE158_G_CURRIER[reading][regime][f],
            rel_tol=0.0,
            abs_tol=TOL,
        ):
            raise RuntimeError(
                f"{reading}/{regime}/fold{f} Issue158 G_Currier failed to reproduce: "
                f"{g_currier_reproduced}"
            )
        if not math.isclose(
            g_outcome + g_interaction, g_currier_reproduced, rel_tol=0.0, abs_tol=TOL
        ):
            raise RuntimeError(f"{reading}/{regime}/fold{f} factorization decomposition failed")

        expected = g161["target_context_support"][reading][regime]
        if visible_clean != int(expected["target_clean_tokens"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} clean support changed")
        if n != int(expected["target_primary_targets"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} primary support changed")
        if primary_body != int(expected["target_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} BODY support changed")
        if supported != int(expected["matched_context_supported_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} matched support changed")
        if unsupported != int(expected["matched_context_unsupported_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} unsupported support changed")

        outer.append(
            {
                "fold": f,
                "reading": reading,
                "regime": regime,
                "n_visible_clean_tokens": visible_clean,
                "n_scored_primary_targets": n,
                "n_scored_run_body_targets": primary_body,
                "matched_context_supported_body_targets": supported,
                "matched_context_unsupported_body_targets": unsupported,
                "matched_context_coverage_fraction": float(supported / primary_body),
                "bits_EDGE_POOL": bits_pool,
                "bits_EDGE_OUTCOME": bits_outcome,
                "bits_EDGE_REGIME": bits_regime,
                "G_outcome": g_outcome,
                "G_interaction": g_interaction,
                "G_Currier_reproduced": g_currier_reproduced,
                "multiplier_sha256": g161[f"W_{regime}_sha256"],
                "outcome_only_conditional_sha256": g161[
                    f"outcome_only_{regime}_conditional_sha256"
                ],
                "POOL_table_sha256": g161["POOL_table_sha256"],
                "target_regime_matched_table_sha256": matched[
                    f"{regime}_matched_sparse_rational_table_sha256"
                ],
            }
        )

    g_interaction = [float(r["G_interaction"]) for r in outer]
    g_outcome = [float(r["G_outcome"]) for r in outer]
    g_currier = [float(r["G_Currier_reproduced"]) for r in outer]
    mean_interaction = float(sum(g_interaction) / N_FOLDS)
    positive_interaction = int(sum(v > 0.0 for v in g_interaction))
    passed = bool(mean_interaction > 0.0 and positive_interaction >= 4)
    mean_outcome = float(sum(g_outcome) / N_FOLDS)
    mean_currier = float(sum(g_currier) / N_FOLDS)

    return {
        "reading": reading,
        "regime": regime,
        "outer": outer,
        "primary": {
            "G_interaction_by_fold": g_interaction,
            "mean_G_interaction": mean_interaction,
            "positive_G_interaction_folds": positive_interaction,
            "required_positive_folds": 4,
            "mean_must_be_positive": True,
            "pass_within_reading_regime": passed,
            "G_outcome_by_fold": g_outcome,
            "mean_G_outcome": mean_outcome,
        },
        "secondary_non_promoting": {
            "G_Currier_reproduced_by_fold": g_currier,
            "mean_G_Currier_reproduced": mean_currier,
            "outcome_capture_fraction_of_mean_G_Currier": (
                float(mean_outcome / mean_currier) if mean_currier != 0.0 else None
            ),
            "min_matched_context_coverage_fraction": min(
                float(r["matched_context_coverage_fraction"]) for r in outer
            ),
            "mean_bits_EDGE_POOL": float(sum(r["bits_EDGE_POOL"] for r in outer) / N_FOLDS),
            "mean_bits_EDGE_OUTCOME": float(
                sum(r["bits_EDGE_OUTCOME"] for r in outer) / N_FOLDS
            ),
            "mean_bits_EDGE_REGIME": float(
                sum(r["bits_EDGE_REGIME"] for r in outer) / N_FOLDS
            ),
        },
    }


def frozen_class(cells: Mapping[str, Mapping[str, dict]]) -> tuple[str, dict]:
    robust = {}
    for regime in REGIMES:
        robust[regime] = bool(
            cells["ZL3b"][regime]["primary"]["pass_within_reading_regime"]
            and cells["IT2a"][regime]["primary"]["pass_within_reading_regime"]
        )

    if robust["A"] and robust["B"]:
        cls = "CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN BOTH A AND B"
    elif robust["A"]:
        cls = "CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN A ONLY"
    elif robust["B"]:
        cls = "CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN B ONLY"
    else:
        cls = "NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL"
    return cls, {
        "Currier_A_context_specific_in_both_readings": robust["A"],
        "Currier_B_context_specific_in_both_readings": robust["B"],
    }


def score(zl_path: Path, it_path: Path) -> dict:
    gate161, gate155 = verify_gate_authority(zl_path, it_path)
    leaf_currier = S155.leaf_currier_from_gate(gate155)
    leaf_fold = G161.G158.G155.G151.G148.G145.fold_authority(zl_path)[0]
    parser = G161.G158.G155.G151.G148.G145.E.SlotParser()
    G161.G158.G155.G151.G148.G145.E.validate_parser(parser)
    _zs, zl_lines = G161.G158.G155.G151.G148.G145.source_identity(zl_path, "ZL3b")
    _is, it_lines = G161.G158.G155.G151.G148.G145.source_identity(it_path, "IT2a")
    all_runs = {
        "ZL3b": C145.clean_runs(zl_lines, leaf_fold, parser),
        "IT2a": C145.clean_runs(it_lines, leaf_fold, parser),
    }
    regime_runs = {
        reading: {
            regime: S155.filter_runs(all_runs[reading], leaf_currier, regime)
            for regime in REGIMES
        }
        for reading in READINGS
    }

    cells = {
        reading: {
            regime: score_cell(
                reading, regime, regime_runs[reading][regime], gate161, gate155
            )
            for regime in REGIMES
        }
        for reading in READINGS
    }
    classification, robust = frozen_class(cells)
    if classification not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")

    return {
        "schema": "issue161-outcome-factor-first-reveal-v1",
        "issue": 161,
        "phase": "OUTCOME_ONLY_CURRIER_FACTORIZATION_FIRST_REVEAL",
        "scored": True,
        "classification": classification,
        "authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": EXPECTED_GATE_RESULT_SHA256,
            "gate0_script_blob": EXPECTED_GATE_SCRIPT_BLOB,
            "gate0_provenance_blob": EXPECTED_GATE_PROVENANCE_BLOB,
            "plan_blob": EXPECTED_PLAN_BLOB,
            "gate0_merge": EXPECTED_GATE_MERGE,
            "issue158_G_Currier_reproduced_foldwise": True,
            "fold_identity_sha256": gate161["entry_authority"]["fold_identity_sha256"],
        },
        "frozen_factorization": {
            "outcome_vocabulary": list(G161.OUTCOMES),
            "V": C145.V,
            "alpha": C145.FIXED_ALPHA,
            "context_invariant_multiplier": True,
            "currier_by_previous_terminal_interaction_in_EDGE_OUTCOME": False,
            "unsupported_exact_context": "empty additive distribution = 1/32",
            "target_native_fallback": False,
            "temperature_interpolation_calibration_mixture": False,
        },
        "cells": cells,
        "primary_joint": {**robust, "classification": classification},
        "secondary_non_promoting": {
            "mean_G_interaction_A_ZL3b_minus_IT2a": float(
                cells["ZL3b"]["A"]["primary"]["mean_G_interaction"]
                - cells["IT2a"]["A"]["primary"]["mean_G_interaction"]
            ),
            "mean_G_interaction_B_ZL3b_minus_IT2a": float(
                cells["ZL3b"]["B"]["primary"]["mean_G_interaction"]
                - cells["IT2a"]["B"]["primary"]["mean_G_interaction"]
            ),
        },
        "firewall": {
            "post_reveal_atom_or_context_selection": False,
            "post_reveal_multiplier_change": False,
            "post_reveal_currier_label_change": False,
            "post_reveal_support_match_change": False,
            "alpha_smoothing_temperature_interpolation_fallback_or_mixture_tuned": False,
            "hand_section_domain_conditioning": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "semantic_cipher_historical_inference": False,
        },
    }


def self_test() -> dict:
    # Target-free synthetic coverage of the scoring path. Reuse Gate0's exact
    # synthetic factorization control and ensure the outcome-only logp is finite.
    s = G161.synthetic_test()
    target_runs = (
        (0, 1, "f1r.1", 1, (
            {"raw": "ab", "atoms": ("a", "b"), "slotparser_accepted": True, "segment_index": 0},
            {"raw": "ca", "atoms": ("c", "a"), "slotparser_accepted": True, "segment_index": 1},
        )),
        (1, 2, "f2r.1", 2, (
            {"raw": "aa", "atoms": ("a", "a"), "slotparser_accepted": True, "segment_index": 0},
            {"raw": "bc", "atoms": ("b", "c"), "slotparser_accepted": True, "segment_index": 1},
        )),
    )
    model = C145.CommonEdgeModel(target_runs, {0, 1})
    pool = {"b": {"c": Fraction(2, 1), "a": Fraction(2, 1)}}
    agg_pool = G161.aggregate_outcomes(pool)
    shifted = {"b": {"c": Fraction(3, 1), "a": Fraction(1, 1)}}
    agg_shifted = G161.aggregate_outcomes(shifted)
    w = G161.build_multiplier(agg_shifted, agg_pool)
    syms = C145.token_symbols(("c", "a"))
    value = outcome_token_logp(model, pool, w, syms, False, "b")
    unseen = outcome_token_logp(model, pool, w, syms, False, "z")
    if not math.isfinite(value) or not math.isfinite(unseen):
        raise AssertionError("synthetic outcome-factor score path non-finite")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "real_target_scores_computed": False,
        "gate_synthetic": s,
        "outcome_factor_score_path_synthetic_only": True,
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue161-outcome-factor-first-reveal-v1",
        "issue": 161,
        "phase": "OUTCOME_ONLY_CURRIER_FACTORIZATION_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID CURRIER EDGE FACTORIZATION",
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
        print(canonical_json(self_test()), end="")
        return 0

    zl_path = Path(ns.run[0]).resolve()
    it_path = Path(ns.run[1]).resolve()
    out_path = Path(ns.run[2]).resolve()
    try:
        result = score(zl_path, it_path)
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
