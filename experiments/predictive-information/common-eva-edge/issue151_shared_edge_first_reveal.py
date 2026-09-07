#!/usr/bin/env python3
"""Issue #151: frozen shared common-EVA edge-table first reveal.

The merged score-free Gate0 is reproduced exactly before any Issue #151 target
score is accepted. For each target reading and physical-leaf outer fold, only
the BODY previous-terminal -> first-atom table is replaced by the prospectively
frozen 0.5/0.5 reading-balanced training-count consensus. All non-edge factors
remain target-native.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
COMMON_DIR = ROOT / "experiments" / "predictive-information" / "common-eva-edge"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

import issue145_common_eva_first_reveal as C145  # noqa: E402
import issue151_shared_edge_gate0 as G151  # noqa: E402

GATE_PROVENANCE_PATH = COMMON_DIR / "ISSUE151_GATE0_PROVENANCE.md"
PLAN_PATH = COMMON_DIR / "ISSUE151_SHARED_EDGE_CONSOLIDATION_PLAN.md"
ISSUE145_SCORER_PATH = COMMON_DIR / "issue145_common_eva_first_reveal.py"
ISSUE148_SCORER_PATH = COMMON_DIR / "issue148_common_eva_table_first_reveal.py"

EXPECTED_GATE_RESULT_SHA256 = "bcc6c6bd5600ef9f74484807b51ef1db454613bae2bbd351d90f089c8693eea2"
EXPECTED_GATE_SCRIPT_BLOB = "d5e3bd22501f8caebabc7c2728bc7f8d5cb59018"
EXPECTED_GATE_PROVENANCE_BLOB = "609ee5f208cfdb3739749d8d82e34d68e4803dd6"
EXPECTED_PLAN_BLOB = "e903bfbdd3742e578f784dc9c358f98f44ad42d2"
EXPECTED_GATE_MERGE = "dea1fc30e9e426adaee290bd1cb357478edf96bf"
EXPECTED_ISSUE145_SCORER_BLOB = "ce8a167c607fbcf2807f567439ab6837471f4f07"
EXPECTED_ISSUE148_SCORER_BLOB = "7847c0fea1dcfc4ace5752d0188d70e3739679d3"
EXPECTED_ISSUE145_RESULT_SHA256 = "663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2"
EXPECTED_ISSUE148_RESULT_SHA256 = "305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923"

EXPECTED_NATIVE_GAINS = {
    "ZL3b": [
        0.1401857712184782,
        0.11070803603016977,
        0.13822277815269501,
        0.14814594340112208,
        0.13085394883490942,
    ],
    "IT2a": [
        0.16849676408952696,
        0.13944957574347505,
        0.16568837114283141,
        0.1803439402500029,
        0.15527126574960093,
    ],
}

N_FOLDS = 5
LN2 = math.log(2.0)
TOL = 1e-12

VALID_CLASSES = (
    "ONE SHARED COMMON-EVA EDGE TABLE SUFFICES",
    "ZL3B RETAINS READING-SPECIFIC EDGE INFORMATION",
    "IT2A RETAINS READING-SPECIFIC EDGE INFORMATION",
    "BOTH READINGS RETAIN READING-SPECIFIC EDGE INFORMATION",
    "INVALID SHARED EDGE CONSOLIDATION",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G151.G148.G145.git_blob_sha1(path.read_bytes())


def verify_post_gate_authority(zl_path: Path, it_path: Path) -> tuple[dict, str]:
    if git_blob(G151.HERE) != EXPECTED_GATE_SCRIPT_BLOB:
        raise RuntimeError("merged Issue151 Gate script blob changed")
    if git_blob(GATE_PROVENANCE_PATH) != EXPECTED_GATE_PROVENANCE_BLOB:
        raise RuntimeError("merged Issue151 Gate provenance blob changed")
    if git_blob(PLAN_PATH) != EXPECTED_PLAN_BLOB:
        raise RuntimeError("Issue151 frozen plan blob changed")
    if git_blob(ISSUE145_SCORER_PATH) != EXPECTED_ISSUE145_SCORER_BLOB:
        raise RuntimeError("Issue145 scorer blob changed")
    if git_blob(ISSUE148_SCORER_PATH) != EXPECTED_ISSUE148_SCORER_BLOB:
        raise RuntimeError("Issue148 scorer blob changed")

    gate = G151.run_gate(zl_path, it_path)
    gate_sha = sha256_text(G151.canonical_json(gate))
    if gate_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Issue151 Gate result SHA changed: {gate_sha}")
    if not gate.get("gate_pass"):
        raise RuntimeError("Issue151 Gate no longer passes")
    if gate.get("scientific_shared_table_metrics_computed") is not False:
        raise RuntimeError("Issue151 Gate firewall changed")
    if gate["entry_authority"]["issue145_declared_first_reveal_result_sha256"] != EXPECTED_ISSUE145_RESULT_SHA256:
        raise RuntimeError("Issue145 declared first-reveal authority changed")
    if gate["entry_authority"]["issue148_declared_first_reveal_result_sha256"] != EXPECTED_ISSUE148_RESULT_SHA256:
        raise RuntimeError("Issue148 declared first-reveal authority changed")
    return gate, gate_sha


def fractional_categorical_logp(counter: Mapping[str, float], symbol: str) -> float:
    total = float(sum(float(v) for v in counter.values()))
    c = float(counter.get(symbol, 0.0))
    return math.log((c + C145.FIXED_ALPHA) / (total + C145.FIXED_ALPHA * C145.V))


def shared_token_logp(
    target_model: C145.CommonEdgeModel,
    shared_counts: Mapping[str, Counter],
    syms: Sequence[str],
    is_run_start: bool,
    previous_terminal: str | None,
) -> float:
    syms = list(syms)
    if len(syms) < 2:
        raise RuntimeError("invalid common-EVA token sequence")
    first, second = syms[0], syms[1]
    ll = 0.0
    if is_run_start:
        ll += target_model.categorical_logp(target_model.start_first, first)
        ll += target_model.categorical_logp(target_model.start_second[first], second)
    else:
        if previous_terminal is None:
            raise RuntimeError("shared BODY target lacks previous terminal")
        ll += fractional_categorical_logp(shared_counts.get(previous_terminal, Counter()), first)
        ll += target_model.categorical_logp(target_model.body_second[first], second)

    for j in range(2, len(syms)):
        ll += target_model.run_model.logp(syms[j - 2 : j], syms[j])
    return float(ll)


def score_reading(
    target_label: str,
    target_runs,
    other_label: str,
    other_runs,
    gate: dict,
) -> dict:
    all_folds = set(range(N_FOLDS))
    outer = []

    for f in range(N_FOLDS):
        train_folds = all_folds - {f}
        target_model = C145.CommonEdgeModel(target_runs, train_folds)
        other_model = C145.CommonEdgeModel(other_runs, train_folds)
        shared_counts, shared_summary = G151.balanced_consensus(
            target_model.prev_terminal_first, other_model.prev_terminal_first
        )

        gate_row = gate["outer"][f]
        expected_shared = gate_row["shared_training_table"]
        if shared_summary["dense_31x31_observed_atom_matrix_sha256"] != expected_shared[
            "dense_31x31_observed_atom_matrix_sha256"
        ]:
            raise RuntimeError(f"{target_label} fold {f} shared-table identity changed")
        if shared_summary["matrix_total_mass"] != expected_shared["matrix_total_mass"]:
            raise RuntimeError(f"{target_label} fold {f} shared-table mass changed")
        if shared_summary["weights"] != {"ZL3b": 0.5, "IT2a": 0.5}:
            raise RuntimeError("shared-table weights changed")

        log_pos = []
        log_native = []
        log_shared = []
        visible_clean = 0
        primary_body = 0
        consensus_supported = 0
        consensus_unsupported = 0
        contexts = {ctx for ctx, counts in shared_counts.items() if counts}

        for fold, _leaf, _loc, _line_no, run in target_runs:
            if int(fold) != f:
                continue
            previous_terminal = None
            for ti, record in enumerate(run):
                syms = C145.token_symbols(record["atoms"])
                lp_pos = target_model.token_logp(syms, ti == 0, previous_terminal, False)
                lp_native = target_model.token_logp(syms, ti == 0, previous_terminal, True)
                lp_shared = shared_token_logp(
                    target_model, shared_counts, syms, ti == 0, previous_terminal
                )
                visible_clean += 1

                if record["slotparser_accepted"]:
                    log_pos.append(float(lp_pos))
                    log_native.append(float(lp_native))
                    log_shared.append(float(lp_shared))
                    if ti > 0:
                        primary_body += 1
                        if previous_terminal in contexts:
                            consensus_supported += 1
                        else:
                            consensus_unsupported += 1
                previous_terminal = syms[-2]

        if not log_pos or not (len(log_pos) == len(log_native) == len(log_shared)):
            raise RuntimeError(f"{target_label} fold {f} score alignment failure")
        if not all(math.isfinite(v) for v in log_pos + log_native + log_shared):
            raise RuntimeError(f"{target_label} fold {f} non-finite target score")

        n = len(log_pos)
        bits_pos = float(-sum(log_pos) / (n * LN2))
        bits_native = float(-sum(log_native) / (n * LN2))
        bits_shared = float(-sum(log_shared) / (n * LN2))
        g_native = float(bits_pos - bits_native)
        g_shared = float(bits_pos - bits_shared)
        g_specific = float(bits_shared - bits_native)

        if not math.isclose(
            g_native, EXPECTED_NATIVE_GAINS[target_label][f], rel_tol=0.0, abs_tol=TOL
        ):
            raise RuntimeError(
                f"{target_label} fold {f} native Issue145 gain failed to reproduce: {g_native}"
            )
        if not math.isclose(g_native, g_shared + g_specific, rel_tol=0.0, abs_tol=TOL):
            raise RuntimeError(f"{target_label} fold {f} gain decomposition failed")

        target_gate = gate_row[f"{target_label}_target_context_support"]
        if visible_clean != int(target_gate["target_clean_tokens"]):
            raise RuntimeError(f"{target_label} fold {f} clean target support changed")
        if n != int(target_gate["target_primary_targets"]):
            raise RuntimeError(f"{target_label} fold {f} primary target support changed")
        if primary_body != int(target_gate["target_primary_run_body_targets"]):
            raise RuntimeError(f"{target_label} fold {f} primary BODY support changed")
        if consensus_supported != int(target_gate["consensus_context_supported_primary_run_body_targets"]):
            raise RuntimeError(f"{target_label} fold {f} consensus-supported support changed")
        if consensus_unsupported != int(target_gate["consensus_context_unsupported_primary_run_body_targets"]):
            raise RuntimeError(f"{target_label} fold {f} consensus-unsupported support changed")

        outer.append(
            {
                "fold": f,
                "n_visible_clean_tokens": visible_clean,
                "n_scored_primary_targets": n,
                "n_scored_run_body_targets": primary_body,
                "consensus_context_supported_body_targets": consensus_supported,
                "consensus_context_unsupported_body_targets": consensus_unsupported,
                "bits_POS2_TARGET": bits_pos,
                "bits_EDGE2_NATIVE_TARGET": bits_native,
                "bits_EDGE2_SHARED": bits_shared,
                "G_native": g_native,
                "G_shared": g_shared,
                "G_specific_native_over_shared": g_specific,
                "shared_table_dense_31x31_sha256": shared_summary[
                    "dense_31x31_observed_atom_matrix_sha256"
                ],
                "shared_table_mass": shared_summary["matrix_total_mass"],
            }
        )

    g_shared_by_fold = [float(r["G_shared"]) for r in outer]
    g_specific_by_fold = [float(r["G_specific_native_over_shared"]) for r in outer]
    mean_shared = float(sum(g_shared_by_fold) / N_FOLDS)
    mean_specific = float(sum(g_specific_by_fold) / N_FOLDS)
    positive_shared = int(sum(g > 0.0 for g in g_shared_by_fold))
    positive_specific = int(sum(g > 0.0 for g in g_specific_by_fold))
    shared_useful = bool(mean_shared > 0.0 and positive_shared >= 4)
    specific_robust = bool(mean_specific > 0.0 and positive_specific >= 4)
    native_mean = float(sum(r["G_native"] for r in outer) / N_FOLDS)

    return {
        "target": target_label,
        "other_reading_in_shared_table": other_label,
        "outer": outer,
        "primary": {
            "G_shared_by_fold": g_shared_by_fold,
            "mean_G_shared": mean_shared,
            "positive_G_shared_folds": positive_shared,
            "shared_useful": shared_useful,
            "G_specific_by_fold": g_specific_by_fold,
            "mean_G_specific": mean_specific,
            "positive_G_specific_folds": positive_specific,
            "reading_specific_residual_robust": specific_robust,
            "required_positive_folds": 4,
            "mean_must_be_positive": True,
            "mean_bits_POS2_TARGET": float(sum(r["bits_POS2_TARGET"] for r in outer) / N_FOLDS),
            "mean_bits_EDGE2_SHARED": float(sum(r["bits_EDGE2_SHARED"] for r in outer) / N_FOLDS),
            "mean_bits_EDGE2_NATIVE_TARGET": float(
                sum(r["bits_EDGE2_NATIVE_TARGET"] for r in outer) / N_FOLDS
            ),
        },
        "secondary_non_promoting": {
            "mean_target_native_G": native_mean,
            "shared_gain_retention_ratio": float(mean_shared / native_mean) if native_mean > 0.0 else None,
            "mean_shared_minus_native_gain": float(mean_shared - native_mean),
        },
    }


def frozen_class(zl: dict, it: dict) -> str:
    if not (zl["primary"]["shared_useful"] and it["primary"]["shared_useful"]):
        return "INVALID SHARED EDGE CONSOLIDATION"
    z_specific = bool(zl["primary"]["reading_specific_residual_robust"])
    i_specific = bool(it["primary"]["reading_specific_residual_robust"])
    if z_specific and i_specific:
        return "BOTH READINGS RETAIN READING-SPECIFIC EDGE INFORMATION"
    if z_specific:
        return "ZL3B RETAINS READING-SPECIFIC EDGE INFORMATION"
    if i_specific:
        return "IT2A RETAINS READING-SPECIFIC EDGE INFORMATION"
    return "ONE SHARED COMMON-EVA EDGE TABLE SUFFICES"


def score(zl_path: Path, it_path: Path) -> dict:
    gate, gate_sha = verify_post_gate_authority(zl_path, it_path)

    leaf_fold = {
        int(leaf): int(fold)
        for fold, leaves in enumerate(
            G151.G148.G145.fold_authority(zl_path)[1]
        )
        for leaf in leaves
    }
    parser = G151.G148.G145.E.SlotParser()
    G151.G148.G145.E.validate_parser(parser)
    _zs, zl_lines = G151.G148.G145.source_identity(zl_path, "ZL3b")
    _is, it_lines = G151.G148.G145.source_identity(it_path, "IT2a")
    zl_runs = C145.clean_runs(zl_lines, leaf_fold, parser)
    it_runs = C145.clean_runs(it_lines, leaf_fold, parser)

    zl = score_reading("ZL3b", zl_runs, "IT2a", it_runs, gate)
    it = score_reading("IT2a", it_runs, "ZL3b", zl_runs, gate)
    classification = frozen_class(zl, it)
    if classification not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")

    return {
        "schema": "issue151-shared-edge-first-reveal-v1",
        "issue": 151,
        "phase": "SHARED_COMMON_EVA_EDGE_CONSOLIDATION_FIRST_REVEAL",
        "scored": True,
        "classification": classification,
        "authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": gate_sha,
            "gate0_expected_sha256": EXPECTED_GATE_RESULT_SHA256,
            "gate0_script_blob": EXPECTED_GATE_SCRIPT_BLOB,
            "gate0_provenance_blob": EXPECTED_GATE_PROVENANCE_BLOB,
            "plan_blob": EXPECTED_PLAN_BLOB,
            "gate0_merge": EXPECTED_GATE_MERGE,
            "issue145_scorer_blob": EXPECTED_ISSUE145_SCORER_BLOB,
            "issue148_scorer_blob": EXPECTED_ISSUE148_SCORER_BLOB,
            "issue145_result_sha256": EXPECTED_ISSUE145_RESULT_SHA256,
            "issue148_result_sha256": EXPECTED_ISSUE148_RESULT_SHA256,
        },
        "frozen_shared_table": {
            "count_formula": "0.5*C_ZL3b + 0.5*C_IT2a",
            "weights": {"ZL3b": 0.5, "IT2a": 0.5},
            "all_non_edge_factors": "target-native",
            "k": C145.FIXED_K,
            "alpha": C145.FIXED_ALPHA,
            "outcome_vocabulary_size": C145.V,
            "unseen_exact_context": "empty exact-context additive smoothing",
            "target_native_fallback": False,
            "scalar_temperature_calibration_interpolation_mixture": False,
        },
        "readings": {"ZL3b": zl, "IT2a": it},
        "primary_joint": {
            "ZL3b_shared_useful": bool(zl["primary"]["shared_useful"]),
            "IT2a_shared_useful": bool(it["primary"]["shared_useful"]),
            "ZL3b_specific_residual_robust": bool(
                zl["primary"]["reading_specific_residual_robust"]
            ),
            "IT2a_specific_residual_robust": bool(
                it["primary"]["reading_specific_residual_robust"]
            ),
            "classification": classification,
        },
        "secondary_non_promoting": {
            "mean_G_shared_difference_ZL3b_minus_IT2a": float(
                zl["primary"]["mean_G_shared"] - it["primary"]["mean_G_shared"]
            ),
            "mean_G_specific_difference_ZL3b_minus_IT2a": float(
                zl["primary"]["mean_G_specific"] - it["primary"]["mean_G_specific"]
            ),
        },
        "firewall": {
            "post_reveal_weight_change": False,
            "post_reveal_atom_mapping_change": False,
            "post_reveal_support_matching": False,
            "target_native_fallback_in_shared_table": False,
            "scalar_temperature_calibration_interpolation_mixture_fit": False,
            "currier_hand_section_conditioned_shared_table": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "semantic_cipher_historical_direction_inference": False,
        },
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue151-shared-edge-first-reveal-v1",
        "issue": 151,
        "phase": "SHARED_COMMON_EVA_EDGE_CONSOLIDATION_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID SHARED EDGE CONSOLIDATION",
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {
            "post_failure_weight_repair_allowed": False,
            "post_failure_target_driven_change_allowed": False,
        },
    }


def self_test() -> dict:
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
    other_runs = (
        (0, 3, "f3r.1", 3, (
            {"raw": "ab", "atoms": ("a", "b"), "slotparser_accepted": True, "segment_index": 0},
            {"raw": "ba", "atoms": ("b", "a"), "slotparser_accepted": True, "segment_index": 1},
        )),
        (1, 4, "f4r.1", 4, (
            {"raw": "ca", "atoms": ("c", "a"), "slotparser_accepted": True, "segment_index": 0},
            {"raw": "ac", "atoms": ("a", "c"), "slotparser_accepted": True, "segment_index": 1},
        )),
    )
    target = C145.CommonEdgeModel(target_runs, {0, 1})
    other = C145.CommonEdgeModel(other_runs, {0, 1})
    shared, _summary = G151.balanced_consensus(target.prev_terminal_first, other.prev_terminal_first)
    syms = C145.token_symbols(("c", "a"))
    value = shared_token_logp(target, shared, syms, False, "b")
    unseen = shared_token_logp(target, shared, syms, False, "z")
    if not (math.isfinite(value) and math.isfinite(unseen)):
        raise AssertionError("synthetic shared-table score is not finite")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "real_target_scores_computed": False,
        "shared_fractional_probability_path_synthetic_only": True,
        "weights": {"ZL3b": 0.5, "IT2a": 0.5},
        "k": C145.FIXED_K,
        "alpha": C145.FIXED_ALPHA,
        "V": C145.V,
    }


def canonical_json(obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


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
