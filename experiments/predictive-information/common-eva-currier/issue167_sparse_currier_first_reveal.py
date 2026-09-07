#!/usr/bin/env python3
"""Issue #167: frozen first reveal for sparse Currier outcome support.

Score only the preregistered K={1,2,4,8,16} sparse multiplier family frozen by
the merged score-free Gate0. For each reading x Currier cell, compare the sparse
model to EDGE_POOL and to the exact full Issue #161 EDGE_OUTCOME ceiling.
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
if str(CURRIER_DIR) not in sys.path:
    sys.path.insert(0, str(CURRIER_DIR))

import issue167_sparse_currier_gate0 as G167  # noqa: E402
import issue161_outcome_factor_first_reveal as S161  # noqa: E402

PLAN_PATH = CURRIER_DIR / "ISSUE167_SPARSE_CURRIER_OUTCOME_PLAN.md"
GATE_PATH = CURRIER_DIR / "issue167_sparse_currier_gate0.py"
GATE_PROVENANCE_PATH = CURRIER_DIR / "ISSUE167_GATE0_PROVENANCE.md"
ISSUE161_FIRST_PROVENANCE_PATH = CURRIER_DIR / "ISSUE161_FIRST_REVEAL_PROVENANCE.md"

EXPECTED_GATE_RESULT_SHA256 = "ff5dfe546333f6e454bb5a36907f88f30ade2ecb36354f20064879e16276484c"
EXPECTED_GATE_SCRIPT_BLOB = "5b3aac1a03ef087340f6e0ffd241a4909476c815"
EXPECTED_GATE_PROVENANCE_BLOB = "f76feea360417e52261bf69dc1425cfceb58963c"
EXPECTED_PLAN_BLOB = "d5b79c64ffc8297672f2de39f6478156ee3442b7"
EXPECTED_GATE_MERGE = "bb56158e907d7253758cc5a0d8bc4dfa2606f1c7"
EXPECTED_ISSUE161_SCORER_BLOB = "d24149977770118505f2147c5aa2bb727631906f"
EXPECTED_ISSUE161_FIRST_PROVENANCE_BLOB = "73100548fef5dbc0d08a1951e3c0ca5b370cd6f4"
EXPECTED_ISSUE161_RESULT_SHA256 = "11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031"
EXPECTED_FOLD_SHA256 = "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b"

N_FOLDS = 5
LN2 = math.log(2.0)
TOL = 1e-12
READINGS = ("ZL3b", "IT2a")
REGIMES = ("A", "B")
KS = (1, 2, 4, 8, 16)
C145 = S161.C145
S155 = S161.S155
G161 = S161.G161

EXPECTED_ISSUE161_G_OUTCOME = {
    "ZL3b": {
        "A": [
            0.12078128912468244,
            -0.02603704408305063,
            0.08226595907739487,
            0.08329802946018283,
            0.08155503804472986,
        ],
        "B": [
            0.12111656997874753,
            0.0885340021846801,
            0.1112354582024313,
            0.10609089038895192,
            0.04290727111000869,
        ],
    },
    "IT2a": {
        "A": [
            0.1284535332574741,
            -0.028767569702601747,
            0.08371366800487756,
            0.06642699141555042,
            0.12204272349820577,
        ],
        "B": [
            0.11973209244976601,
            0.08641004635049399,
            0.11408234842922305,
            0.10975647381687814,
            0.04679266231023327,
        ],
    },
}

VALID_CLASSES = tuple(
    [f"CURRIER OUTCOME BIAS SPARSE SUPPORT: K={k} SUFFICES" for k in KS]
    + [
        "NO TESTED SPARSE CURRIER OUTCOME SUPPORT SUFFICES",
        "INVALID SPARSE CURRIER OUTCOME FACTORIZATION",
    ]
)


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G167.git_blob(path)


def verify_gate_authority(zl_path: Path, it_path: Path) -> tuple[dict, dict, dict]:
    pins = (
        (GATE_PATH, EXPECTED_GATE_SCRIPT_BLOB, "Issue167 Gate script"),
        (GATE_PROVENANCE_PATH, EXPECTED_GATE_PROVENANCE_BLOB, "Issue167 Gate provenance"),
        (PLAN_PATH, EXPECTED_PLAN_BLOB, "Issue167 plan"),
        (S161.HERE, EXPECTED_ISSUE161_SCORER_BLOB, "Issue161 scientific scorer"),
        (
            ISSUE161_FIRST_PROVENANCE_PATH,
            EXPECTED_ISSUE161_FIRST_PROVENANCE_BLOB,
            "Issue161 first-reveal provenance",
        ),
    )
    for path, expected, label in pins:
        actual = git_blob(path)
        if actual != expected:
            raise RuntimeError(f"{label} blob changed: {actual}")

    first_text = ISSUE161_FIRST_PROVENANCE_PATH.read_text(encoding="utf-8")
    if EXPECTED_ISSUE161_RESULT_SHA256 not in first_text:
        raise RuntimeError("Issue161 result identity missing from frozen provenance")

    gate167 = G167.run_gate(zl_path, it_path)
    gate167_sha = sha256_obj(gate167)
    if gate167_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Issue167 Gate result SHA changed: {gate167_sha}")
    if gate167.get("gate_pass") is not True:
        raise RuntimeError("Issue167 Gate no longer passes")
    if gate167.get("scientific_sparse_metrics_computed") is not False:
        raise RuntimeError("Issue167 Gate firewall changed")
    if gate167["entry_authority"]["fold_identity_sha256"] != EXPECTED_FOLD_SHA256:
        raise RuntimeError("Issue167 fold authority changed")

    gate161, gate155 = S161.verify_gate_authority(zl_path, it_path)
    return gate167, gate161, gate155


def score_cell(
    reading: str,
    regime: str,
    target_runs,
    gate167: dict,
    gate161: dict,
    gate155: dict,
) -> dict:
    all_folds = set(range(N_FOLDS))
    outer = []

    for f in range(N_FOLDS):
        target_model = C145.CommonEdgeModel(target_runs, all_folds - {f})
        g167 = gate167["outer"][f]
        g161 = gate161["outer"][f]
        g155 = gate155["outer"][f]
        if not (int(g167["outer_fold"]) == int(g161["outer_fold"]) == int(g155["outer_fold"]) == f):
            raise RuntimeError("fold order changed")

        matched = g155["matched_currier_tables"]
        a = G161.parse_rational_table(matched["A_matched_sparse_rational_counts"])
        b = G161.parse_rational_table(matched["B_matched_sparse_rational_counts"])
        pool, pool_summary = G161.G158.pool_tables(a, b)
        if pool_summary["pooled_sparse_rational_table_sha256"] != g161["POOL_table_sha256"]:
            raise RuntimeError(f"fold {f} pooled table failed Issue161 identity")
        if g167["POOL_table_sha256"] != g161["POOL_table_sha256"]:
            raise RuntimeError(f"fold {f} Issue167/161 pooled table identity differs")

        full = S161.parse_vector(g161[f"W_{regime}"])
        sparse = {}
        for k in KS:
            selected = set(g167["topK"][str(k)]["selected_outcomes"])
            w = G167.sparse_multiplier(full, selected)
            vec = G167.rational_vector(w)
            frozen = g167["topK"][str(k)]["regimes"][regime]
            if sha256_obj(vec) != frozen["sparse_multiplier_sha256"]:
                raise RuntimeError(f"fold {f} K={k} {regime} sparse multiplier identity changed")
            cond_sha, audit = G161.conditional_identity(pool, w)
            if cond_sha != frozen["conditional_sha256"]:
                raise RuntimeError(f"fold {f} K={k} {regime} sparse conditional identity changed")
            if audit["all_contexts_exactly_normalized"] is not True:
                raise RuntimeError(f"fold {f} K={k} {regime} sparse normalization failed")
            sparse[k] = w

        log_pool = []
        log_full = []
        log_sparse = {k: [] for k in KS}
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
                lp_full = S161.outcome_token_logp(
                    target_model, pool, full, syms, ti == 0, previous_terminal
                )
                lp_sparse = {
                    k: S161.outcome_token_logp(
                        target_model, pool, sparse[k], syms, ti == 0, previous_terminal
                    )
                    for k in KS
                }
                visible_clean += 1
                if record["slotparser_accepted"]:
                    log_pool.append(float(lp_pool))
                    log_full.append(float(lp_full))
                    for k in KS:
                        log_sparse[k].append(float(lp_sparse[k]))
                    if ti > 0:
                        primary_body += 1
                        if previous_terminal in pool:
                            supported += 1
                        else:
                            unsupported += 1
                previous_terminal = syms[-2]

        n = len(log_pool)
        if n <= 0 or len(log_full) != n or any(len(log_sparse[k]) != n for k in KS):
            raise RuntimeError(f"{reading}/{regime}/fold{f} score alignment failure")
        all_values = log_pool + log_full + [v for k in KS for v in log_sparse[k]]
        if not all(math.isfinite(v) for v in all_values):
            raise RuntimeError(f"{reading}/{regime}/fold{f} non-finite score")

        bits_pool = float(-sum(log_pool) / (n * LN2))
        bits_full = float(-sum(log_full) / (n * LN2))
        g_outcome = float(bits_pool - bits_full)
        expected_g = EXPECTED_ISSUE161_G_OUTCOME[reading][regime][f]
        if not math.isclose(g_outcome, expected_g, rel_tol=0.0, abs_tol=TOL):
            raise RuntimeError(
                f"{reading}/{regime}/fold{f} Issue161 G_outcome failed to reproduce: {g_outcome}"
            )

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

        k_rows = {}
        for k in KS:
            bits_sparse = float(-sum(log_sparse[k]) / (n * LN2))
            g_sparse = float(bits_pool - bits_sparse)
            g_missing = float(bits_sparse - bits_full)
            if not math.isclose(g_sparse + g_missing, g_outcome, rel_tol=0.0, abs_tol=TOL):
                raise RuntimeError(f"{reading}/{regime}/fold{f}/K{k} decomposition failed")
            k_rows[str(k)] = {
                "bits_EDGE_SPARSE": bits_sparse,
                "G_sparse": g_sparse,
                "G_missing": g_missing,
                "selected_outcomes": g167["topK"][str(k)]["selected_outcomes"],
                "selected_outcomes_sha256": g167["topK"][str(k)]["selected_outcomes_sha256"],
                "sparse_multiplier_sha256": g167["topK"][str(k)]["regimes"][regime][
                    "sparse_multiplier_sha256"
                ],
                "sparse_conditional_sha256": g167["topK"][str(k)]["regimes"][regime][
                    "conditional_sha256"
                ],
            }

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
                "bits_EDGE_OUTCOME_FULL": bits_full,
                "G_outcome_reproduced": g_outcome,
                "Jeffreys_ranking_sha256": g167["Jeffreys_ranking_sha256"],
                "K": k_rows,
            }
        )

    summaries = {}
    for k in KS:
        gs = [float(row["K"][str(k)]["G_sparse"]) for row in outer]
        gm = [float(row["K"][str(k)]["G_missing"]) for row in outer]
        mean_gs = float(sum(gs) / N_FOLDS)
        mean_gm = float(sum(gm) / N_FOLDS)
        pos_gs = int(sum(v > 0 for v in gs))
        pos_gm = int(sum(v > 0 for v in gm))
        useful = bool(mean_gs > 0 and pos_gs >= 4)
        robust_missing = bool(mean_gm > 0 and pos_gm >= 4)
        summaries[str(k)] = {
            "G_sparse_by_fold": gs,
            "mean_G_sparse": mean_gs,
            "positive_G_sparse_folds": pos_gs,
            "useful": useful,
            "G_missing_by_fold": gm,
            "mean_G_missing": mean_gm,
            "positive_G_missing_folds": pos_gm,
            "robust_full_over_sparse_residual": robust_missing,
            "required_positive_folds": 4,
        }

    return {
        "reading": reading,
        "regime": regime,
        "outer": outer,
        "K_summary": summaries,
        "secondary_non_promoting": {
            "G_outcome_reproduced_by_fold": [float(r["G_outcome_reproduced"]) for r in outer],
            "mean_G_outcome_reproduced": float(
                sum(r["G_outcome_reproduced"] for r in outer) / N_FOLDS
            ),
            "min_matched_context_coverage_fraction": min(
                float(r["matched_context_coverage_fraction"]) for r in outer
            ),
        },
    }


def classify(cells: Mapping[str, Mapping[str, dict]]) -> tuple[str, dict]:
    k_summary = {}
    first = None
    for k in KS:
        cell_flags = {}
        all_useful = True
        any_robust_missing = False
        for reading in READINGS:
            for regime in REGIMES:
                key = f"{reading}/{regime}"
                s = cells[reading][regime]["K_summary"][str(k)]
                useful = bool(s["useful"])
                missing = bool(s["robust_full_over_sparse_residual"])
                cell_flags[key] = {
                    "useful": useful,
                    "robust_full_over_sparse_residual": missing,
                }
                all_useful = all_useful and useful
                any_robust_missing = any_robust_missing or missing
        sufficient = bool(all_useful and not any_robust_missing)
        k_summary[str(k)] = {
            "all_four_cells_useful": all_useful,
            "any_cell_robust_full_over_sparse_residual": any_robust_missing,
            "suffices_prospectively": sufficient,
            "cells": cell_flags,
        }
        if sufficient and first is None:
            first = k

    if first is None:
        cls = "NO TESTED SPARSE CURRIER OUTCOME SUPPORT SUFFICES"
    else:
        cls = f"CURRIER OUTCOME BIAS SPARSE SUPPORT: K={first} SUFFICES"
    if cls not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")
    return cls, {"smallest_sufficient_K": first, "K": k_summary}


def score(zl_path: Path, it_path: Path) -> dict:
    gate167, gate161, gate155 = verify_gate_authority(zl_path, it_path)
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
                reading,
                regime,
                regime_runs[reading][regime],
                gate167,
                gate161,
                gate155,
            )
            for regime in REGIMES
        }
        for reading in READINGS
    }
    classification, primary = classify(cells)

    return {
        "schema": "issue167-sparse-currier-outcome-first-reveal-v1",
        "issue": 167,
        "phase": "SPARSE_CURRIER_OUTCOME_FIRST_REVEAL",
        "scored": True,
        "classification": classification,
        "authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": EXPECTED_GATE_RESULT_SHA256,
            "gate0_script_blob": EXPECTED_GATE_SCRIPT_BLOB,
            "gate0_provenance_blob": EXPECTED_GATE_PROVENANCE_BLOB,
            "plan_blob": EXPECTED_PLAN_BLOB,
            "gate0_merge": EXPECTED_GATE_MERGE,
            "issue161_scorer_blob": EXPECTED_ISSUE161_SCORER_BLOB,
            "issue161_first_provenance_blob": EXPECTED_ISSUE161_FIRST_PROVENANCE_BLOB,
            "issue161_declared_first_reveal_result_sha256": EXPECTED_ISSUE161_RESULT_SHA256,
            "issue161_G_outcome_reproduced_foldwise": True,
            "fold_identity_sha256": gate167["entry_authority"]["fold_identity_sha256"],
        },
        "frozen_family": {
            "outcome_vocabulary": list(G167.OUTCOMES),
            "V": 32,
            "alpha": [1, 100],
            "K_ladder": list(KS),
            "training_only_selection_reused_from_merged_Gate0": True,
            "context_invariant_multiplier": True,
            "currier_by_previous_terminal_interaction": False,
            "unsupported_exact_context": "empty additive distribution = 1/32",
            "target_native_fallback": False,
            "retention_percentage_threshold": None,
        },
        "cells": cells,
        "primary_joint": {**primary, "classification": classification},
        "firewall": {
            "post_reveal_outcome_reranking_or_reselection": False,
            "post_reveal_K_ladder_change": False,
            "post_reveal_multiplier_change": False,
            "post_reveal_currier_label_representation_fold_support_or_pooling_change": False,
            "retention_percentage_rescue": False,
            "alpha_ranking_temperature_interpolation_fallback_or_mixture_tuned": False,
            "currier_by_previous_terminal_interaction_added": False,
            "hand_section_domain_conditioning": False,
            "latent_state_fit": False,
            "semantic_cipher_historical_inference": False,
        },
    }


def self_test() -> dict:
    gate_synthetic = G167.synthetic_test()
    fake = {
        reading: {
            regime: {
                "K_summary": {
                    str(k): {
                        "useful": (k >= 4),
                        "robust_full_over_sparse_residual": (k < 4),
                    }
                    for k in KS
                }
            }
            for regime in REGIMES
        }
        for reading in READINGS
    }
    cls, primary = classify(fake)
    if cls != "CURRIER OUTCOME BIAS SPARSE SUPPORT: K=4 SUFFICES":
        raise AssertionError("synthetic hierarchical classification failed")
    if primary["smallest_sufficient_K"] != 4:
        raise AssertionError("synthetic smallest-K selection failed")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "real_target_scores_computed": False,
        "gate_synthetic": gate_synthetic,
        "hierarchical_smallest_K_rule_tested": True,
        "synthetic_expected_K": 4,
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue167-sparse-currier-outcome-first-reveal-v1",
        "issue": 167,
        "phase": "SPARSE_CURRIER_OUTCOME_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID SPARSE CURRIER OUTCOME FACTORIZATION",
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
