#!/usr/bin/env python3
"""Issue #158: frozen first reveal for incremental Currier-gate edge information.

The merged score-free Gate0 is reproduced before any target score is accepted.
For each target reading, Currier regime, and physical-leaf fold, POS2 is compared
with an edge model using the fixed 0.5/0.5 regime-neutral pooled table and with
an otherwise identical edge model using the target Currier regime's matched
table. The primary residual is G_Currier = bits(EDGE_POOL)-bits(EDGE_REGIME).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
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

import issue145_common_eva_first_reveal as C145  # noqa: E402
import issue155_common_eva_currier_first_reveal as S155  # noqa: E402
import issue158_currier_gate_decomposition_gate0 as G158  # noqa: E402

PLAN_PATH = CURRIER_DIR / "ISSUE158_CURRIER_GATE_DECOMPOSITION_PLAN.md"
GATE_PROVENANCE_PATH = CURRIER_DIR / "ISSUE158_GATE0_PROVENANCE.md"
ISSUE155_SCORER_PATH = CURRIER_DIR / "issue155_common_eva_currier_first_reveal.py"

EXPECTED_GATE_RESULT_SHA256 = "605e0a82817f394176a3e19c972ed409dfb15df60c72df22db3c0cc765e31099"
EXPECTED_GATE_SCRIPT_BLOB = "4dbc919f3e9ededa17d2e10f56de46c98456cdea"
EXPECTED_GATE_PROVENANCE_BLOB = "07595bf7314cfb71763eba1a810bfd3aaa01a239"
EXPECTED_PLAN_BLOB = "9ae7d7ea54aca4deea76f482b10010114cc1dac7"
EXPECTED_GATE_MERGE = "ca77b7030dec12778ffdeb1d04bee0b30fb00b65"
EXPECTED_ISSUE155_SCORER_BLOB = "0d57fdd32d298773b5ee38f97c9f104d29fa8377"

N_FOLDS = 5
LN2 = math.log(2.0)
READINGS = ("ZL3b", "IT2a")
REGIMES = ("A", "B")

VALID_CLASSES = (
    "CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B",
    "CURRIER GATE ADDS ROBUST EDGE INFORMATION IN A ONLY",
    "CURRIER GATE ADDS ROBUST EDGE INFORMATION IN B ONLY",
    "NO ROBUST CURRIER-GATE EDGE RESIDUAL",
    "INVALID CURRIER-GATE DECOMPOSITION",
)


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def verify_post_gate_authority(zl_path: Path, it_path: Path) -> tuple[dict, str, dict]:
    if G158.git_blob(G158.HERE) != EXPECTED_GATE_SCRIPT_BLOB:
        raise RuntimeError("merged Issue158 Gate script blob changed")
    if G158.git_blob(GATE_PROVENANCE_PATH) != EXPECTED_GATE_PROVENANCE_BLOB:
        raise RuntimeError("merged Issue158 Gate provenance blob changed")
    if G158.git_blob(PLAN_PATH) != EXPECTED_PLAN_BLOB:
        raise RuntimeError("Issue158 plan blob changed")
    if G158.git_blob(ISSUE155_SCORER_PATH) != EXPECTED_ISSUE155_SCORER_BLOB:
        raise RuntimeError("Issue155 first-reveal scorer blob changed")

    gate158 = G158.run_gate(zl_path, it_path)
    gate158_sha = sha256_obj(gate158)
    if gate158_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Issue158 Gate result SHA changed: {gate158_sha}")
    if not gate158.get("gate_pass"):
        raise RuntimeError("Issue158 Gate no longer passes")
    if gate158.get("scientific_currier_gate_metrics_computed") is not False:
        raise RuntimeError("Issue158 Gate firewall changed")
    if gate158["entry_authority"]["plan_blob_sha1"] != EXPECTED_PLAN_BLOB:
        raise RuntimeError("Issue158 Gate plan identity changed")

    gate155 = G158.G155.run_gate(zl_path, it_path)
    gate155_sha = G158.sha256_obj(gate155)
    if gate155_sha != G158.EXPECTED["issue155_gate_result_sha256"]:
        raise RuntimeError("Issue155 Gate no longer reproduces inside Issue158 scorer")
    return gate158, gate158_sha, gate155


def score_cell(
    reading: str,
    regime: str,
    target_runs,
    gate158: dict,
    gate155: dict,
) -> dict:
    all_folds = set(range(N_FOLDS))
    outer = []

    for f in range(N_FOLDS):
        train_folds = all_folds - {f}
        target_model = C145.CommonEdgeModel(target_runs, train_folds)

        gate158_row = gate158["outer"][f]
        gate155_row = gate155["outer"][f]
        if int(gate158_row["outer_fold"]) != f or int(gate155_row["outer_fold"]) != f:
            raise RuntimeError("fold order changed")

        pool_summary = gate158_row["pooled_table"]
        pool_sparse = pool_summary["pooled_sparse_rational_counts"]
        if G158.sha256_obj(pool_sparse) != pool_summary["pooled_sparse_rational_table_sha256"]:
            raise RuntimeError(f"fold {f} pooled-table identity changed")
        pool_table = G158.parse_rational_table(pool_sparse)

        matched_summary = gate155_row["matched_currier_tables"]
        regime_table = S155.table_from_gate(matched_summary, regime)
        retained_contexts = set(matched_summary["retained_previous_terminal_contexts"])
        if set(pool_table) != retained_contexts or set(regime_table) != retained_contexts:
            raise RuntimeError(f"fold {f} retained context identity changed")

        log_pos = []
        log_pool = []
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
                lp_pos = target_model.token_logp(syms, ti == 0, previous_terminal, False)
                lp_pool = S155.matched_token_logp(
                    target_model, pool_table, syms, ti == 0, previous_terminal
                )
                lp_regime = S155.matched_token_logp(
                    target_model, regime_table, syms, ti == 0, previous_terminal
                )
                visible_clean += 1

                if record["slotparser_accepted"]:
                    log_pos.append(float(lp_pos))
                    log_pool.append(float(lp_pool))
                    log_regime.append(float(lp_regime))
                    if ti > 0:
                        primary_body += 1
                        if previous_terminal in retained_contexts:
                            supported += 1
                        else:
                            unsupported += 1
                previous_terminal = syms[-2]

        if not log_pos or not (len(log_pos) == len(log_pool) == len(log_regime)):
            raise RuntimeError(f"{reading}/{regime}/fold{f} score alignment failure")
        if not all(math.isfinite(v) for v in log_pos + log_pool + log_regime):
            raise RuntimeError(f"{reading}/{regime}/fold{f} non-finite score")

        n = len(log_pos)
        bits_pos = float(-sum(log_pos) / (n * LN2))
        bits_pool = float(-sum(log_pool) / (n * LN2))
        bits_regime = float(-sum(log_regime) / (n * LN2))
        g_pool = float(bits_pos - bits_pool)
        g_currier = float(bits_pool - bits_regime)
        g_regime_total = float(bits_pos - bits_regime)
        if not math.isclose(g_pool + g_currier, g_regime_total, rel_tol=0.0, abs_tol=1e-12):
            raise RuntimeError(f"{reading}/{regime}/fold{f} information decomposition failed")

        expected = gate158_row["target_context_support"][reading][regime]
        if visible_clean != int(expected["target_clean_tokens"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} clean target support changed")
        if n != int(expected["target_primary_targets"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} primary target support changed")
        if primary_body != int(expected["target_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} BODY target support changed")
        if supported != int(expected["matched_context_supported_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} matched-context support changed")
        if unsupported != int(expected["matched_context_unsupported_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{regime}/fold{f} unsupported-context support changed")

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
                "bits_POS2_TARGET_REGIME": bits_pos,
                "bits_EDGE_POOL": bits_pool,
                "bits_EDGE_REGIME": bits_regime,
                "G_pool": g_pool,
                "G_Currier": g_currier,
                "G_regime_total": g_regime_total,
                "pooled_table_sha256": pool_summary["pooled_sparse_rational_table_sha256"],
                "target_regime_matched_table_sha256": matched_summary[
                    f"{regime}_matched_sparse_rational_table_sha256"
                ],
            }
        )

    currier = [float(r["G_Currier"]) for r in outer]
    pool = [float(r["G_pool"]) for r in outer]
    total = [float(r["G_regime_total"]) for r in outer]
    mean_currier = float(sum(currier) / N_FOLDS)
    positive_currier = int(sum(g > 0.0 for g in currier))
    passed = bool(mean_currier > 0.0 and positive_currier >= 4)

    return {
        "reading": reading,
        "regime": regime,
        "outer": outer,
        "primary": {
            "G_Currier_by_fold": currier,
            "mean_G_Currier": mean_currier,
            "positive_G_Currier_folds": positive_currier,
            "required_positive_folds": 4,
            "mean_must_be_positive": True,
            "pass_within_reading_regime": passed,
            "G_pool_by_fold": pool,
            "mean_G_pool": float(sum(pool) / N_FOLDS),
        },
        "secondary_non_promoting": {
            "G_regime_total_by_fold": total,
            "mean_G_regime_total": float(sum(total) / N_FOLDS),
            "mean_bits_POS2_TARGET_REGIME": float(
                sum(r["bits_POS2_TARGET_REGIME"] for r in outer) / N_FOLDS
            ),
            "mean_bits_EDGE_POOL": float(sum(r["bits_EDGE_POOL"] for r in outer) / N_FOLDS),
            "mean_bits_EDGE_REGIME": float(sum(r["bits_EDGE_REGIME"] for r in outer) / N_FOLDS),
            "min_matched_context_coverage_fraction": min(
                float(r["matched_context_coverage_fraction"]) for r in outer
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
        classification = "CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B"
    elif robust["A"]:
        classification = "CURRIER GATE ADDS ROBUST EDGE INFORMATION IN A ONLY"
    elif robust["B"]:
        classification = "CURRIER GATE ADDS ROBUST EDGE INFORMATION IN B ONLY"
    else:
        classification = "NO ROBUST CURRIER-GATE EDGE RESIDUAL"
    return classification, {
        "Currier_A_robust_in_both_readings": robust["A"],
        "Currier_B_robust_in_both_readings": robust["B"],
    }


def score(zl_path: Path, it_path: Path) -> dict:
    gate158, gate158_sha, gate155 = verify_post_gate_authority(zl_path, it_path)
    leaf_currier = S155.leaf_currier_from_gate(gate155)
    leaf_fold = G158.G155.G151.G148.G145.fold_authority(zl_path)[0]
    parser = G158.G155.G151.G148.G145.E.SlotParser()
    G158.G155.G151.G148.G145.E.validate_parser(parser)
    _zs, zl_lines = G158.G155.G151.G148.G145.source_identity(zl_path, "ZL3b")
    _is, it_lines = G158.G155.G151.G148.G145.source_identity(it_path, "IT2a")
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
                reading, regime, regime_runs[reading][regime], gate158, gate155
            )
            for regime in REGIMES
        }
        for reading in READINGS
    }
    classification, robust = frozen_class(cells)
    if classification not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")

    return {
        "schema": "issue158-currier-gate-first-reveal-v1",
        "issue": 158,
        "phase": "CURRIER_GATE_INCREMENTAL_INFORMATION_FIRST_REVEAL",
        "scored": True,
        "classification": classification,
        "authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": gate158_sha,
            "gate0_expected_sha256": EXPECTED_GATE_RESULT_SHA256,
            "gate0_script_blob": EXPECTED_GATE_SCRIPT_BLOB,
            "gate0_provenance_blob": EXPECTED_GATE_PROVENANCE_BLOB,
            "plan_blob": EXPECTED_PLAN_BLOB,
            "gate0_merge": EXPECTED_GATE_MERGE,
            "issue155_scorer_blob": EXPECTED_ISSUE155_SCORER_BLOB,
            "fold_identity_sha256": gate158["entry_authority"]["fold_identity_sha256"],
        },
        "frozen_model": {
            "representation": "Issue145/151 common Basic-EVA",
            "currier_authority": "Issue155 Phase3A physical-leaf A_ONLY/B_ONLY",
            "source_tables": "Issue155 exact rational context-mass-matched A/B tables",
            "pooled_table": "C_POOL = 0.5*C_A_MATCH + 0.5*C_B_MATCH",
            "pooled_weights": {"A": 0.5, "B": 0.5},
            "target_non_edge_factors": "target-reading and target-Currier native",
            "k": C145.FIXED_K,
            "alpha": C145.FIXED_ALPHA,
            "outcome_vocabulary_size": C145.V,
            "unsupported_exact_context": "empty additive distribution",
            "target_native_fallback": False,
            "rho_temperature_calibration_interpolation_mixture": False,
        },
        "cells": cells,
        "primary_joint": {**robust, "classification": classification},
        "secondary_non_promoting": {
            "mean_G_Currier_A_ZL3b_minus_IT2a": float(
                cells["ZL3b"]["A"]["primary"]["mean_G_Currier"]
                - cells["IT2a"]["A"]["primary"]["mean_G_Currier"]
            ),
            "mean_G_Currier_B_ZL3b_minus_IT2a": float(
                cells["ZL3b"]["B"]["primary"]["mean_G_Currier"]
                - cells["IT2a"]["B"]["primary"]["mean_G_Currier"]
            ),
        },
        "firewall": {
            "post_reveal_context_or_atom_selection": False,
            "post_reveal_currier_label_change": False,
            "post_reveal_pooled_weight_change": False,
            "post_reveal_support_match_change": False,
            "k_alpha_smoothing_or_fallback_tuned": False,
            "rho_temperature_calibration_interpolation_mixture_fit": False,
            "hand_section_domain_conditioning": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "semantic_cipher_historical_inference": False,
        },
    }


def synthetic_self_test() -> dict:
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
    a = {"b": {"c": G158.Fraction(3, 1), "a": G158.Fraction(1, 1)}}
    b = {"b": {"c": G158.Fraction(1, 1), "a": G158.Fraction(3, 1)}}
    pool, summary = G158.pool_tables(a, b)
    syms = C145.token_symbols(("c", "a"))
    lp_pool = S155.matched_token_logp(model, pool, syms, False, "b")
    lp_a = S155.matched_token_logp(model, a, syms, False, "b")
    lp_unseen = S155.matched_token_logp(model, pool, syms, False, "z")
    if not all(math.isfinite(v) for v in (lp_pool, lp_a, lp_unseen)):
        raise AssertionError("synthetic Currier-gate score non-finite")
    if summary["exact_A_B_POOL_context_mass_equality"] is not True:
        raise AssertionError("synthetic pooled mass equality failed")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "real_target_scores_computed": False,
        "pooled_and_regime_edge_paths_synthetic_only": True,
        "fixed_weights": {"A": [1, 2], "B": [1, 2]},
        "k": C145.FIXED_K,
        "alpha": C145.FIXED_ALPHA,
        "V": C145.V,
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue158-currier-gate-first-reveal-v1",
        "issue": 158,
        "phase": "CURRIER_GATE_INCREMENTAL_INFORMATION_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID CURRIER-GATE DECOMPOSITION",
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
        print(canonical_json(synthetic_self_test()), end="")
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
