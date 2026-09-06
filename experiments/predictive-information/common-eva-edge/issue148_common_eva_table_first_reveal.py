#!/usr/bin/env python3
"""Issue #148: frozen bidirectional common-EVA literal edge-table transport.

The merged score-free Gate0 is reproduced exactly before any target score is
computed. For each direction, only the BODY first-atom conditional table is
transported from the source reading; every other factor is target-native.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
COMMON_DIR = ROOT / "experiments" / "predictive-information" / "common-eva-edge"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

import issue145_common_eva_first_reveal as C145  # noqa: E402
import issue148_common_eva_table_gate0 as G148  # noqa: E402

GATE_PROVENANCE_PATH = COMMON_DIR / "ISSUE148_GATE0_PROVENANCE.md"
ISSUE145_SCORER_PATH = COMMON_DIR / "issue145_common_eva_first_reveal.py"

EXPECTED_GATE_RESULT_SHA256 = "f324264b814ef02d8de70b804754750ec579f8a9e0d8dffb0f1575439867d1bf"
EXPECTED_GATE_SCRIPT_BLOB = "a8029aac50ccc6e09ec975b7b86a1bde44415f9f"
EXPECTED_GATE_PROVENANCE_BLOB = "7f97b9731a6e72e2456ede436e837a3735f265fd"
EXPECTED_GATE_MERGE = "2bbaf46f4c420ae87169cacb39e5dc0dc9cd6425"
EXPECTED_ISSUE145_SCORER_BLOB = "ce8a167c607fbcf2807f567439ab6837471f4f07"

# Exact fold gains from the frozen Issue #145 result artifact
# (artifact 9997826217, result SHA-256
# 663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2).
# These are authority-reproduction constants only; they do not enter the
# Issue #148 transport probabilities or classification rule.
EXPECTED_NATIVE_GAINS = {
    "ZL3b": [
        0.14018577117719566,
        0.11070803603214441,
        0.13822277819933482,
        0.1481459433840746,
        0.13085394871093636,
    ],
    "IT2a": [
        0.16849676408952696,
        0.13944957564829674,
        0.16568837103531342,
        0.18034394031427348,
        0.15527126588802687,
    ],
}

N_FOLDS = 5
LN2 = math.log(2.0)
TOL = 1e-12

VALID_CLASSES = (
    "COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS",
    "COMMON-EVA LITERAL EDGE TABLE TRANSPORTS ZL3B→IT2A ONLY",
    "COMMON-EVA LITERAL EDGE TABLE TRANSPORTS IT2A→ZL3B ONLY",
    "COMMON-EVA LITERAL EDGE TABLE TRANSPORTS NEITHER DIRECTION",
    "INVALID CROSS-READING TABLE TRANSPORT",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_post_gate_authority(zl_path: Path, it_path: Path) -> tuple[dict, str]:
    if G148.G145.git_blob_sha1(G148.HERE.read_bytes()) != EXPECTED_GATE_SCRIPT_BLOB:
        raise RuntimeError("merged Issue148 Gate script blob changed")
    if G148.G145.git_blob_sha1(GATE_PROVENANCE_PATH.read_bytes()) != EXPECTED_GATE_PROVENANCE_BLOB:
        raise RuntimeError("merged Issue148 Gate provenance blob changed")
    if G148.G145.git_blob_sha1(ISSUE145_SCORER_PATH.read_bytes()) != EXPECTED_ISSUE145_SCORER_BLOB:
        raise RuntimeError("Issue145 common-EVA scorer blob changed")

    gate = G148.run_gate(zl_path, it_path)
    gate_sha = sha256_text(G148.canonical_json(gate))
    if not gate.get("gate_pass"):
        raise RuntimeError("Issue148 Gate no longer passes")
    if gate_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Issue148 Gate result SHA changed: {gate_sha}")
    if gate.get("scientific_transport_metrics_computed") is not False:
        raise RuntimeError("Issue148 Gate firewall changed")
    return gate, gate_sha


def cross_token_logp(
    target_model: C145.CommonEdgeModel,
    source_model: C145.CommonEdgeModel,
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
            raise RuntimeError("BODY target token lacks previous terminal")
        source_counter = source_model.prev_terminal_first.get(previous_terminal, Counter())
        ll += target_model.categorical_logp(source_counter, first)
        ll += target_model.categorical_logp(target_model.body_second[first], second)

    for j in range(2, len(syms)):
        ll += target_model.run_model.logp(syms[j - 2 : j], syms[j])
    return float(ll)


def score_direction(
    source_label: str,
    target_label: str,
    source_runs,
    target_runs,
    gate: dict,
) -> dict:
    all_folds = set(range(N_FOLDS))
    outer = []

    for f in range(N_FOLDS):
        train_folds = all_folds - {f}
        target_model = C145.CommonEdgeModel(target_runs, train_folds)
        source_model = C145.CommonEdgeModel(source_runs, train_folds)

        log_pos = []
        log_native = []
        log_cross = []
        visible_clean = 0
        primary_body = 0
        supported_context = 0
        unsupported_context = 0

        for fold, _leaf, _loc, _line_no, run in target_runs:
            if int(fold) != f:
                continue
            previous_terminal = None
            for ti, record in enumerate(run):
                syms = C145.token_symbols(record["atoms"])
                lp_pos = target_model.token_logp(syms, ti == 0, previous_terminal, False)
                lp_native = target_model.token_logp(syms, ti == 0, previous_terminal, True)
                lp_cross = cross_token_logp(
                    target_model, source_model, syms, ti == 0, previous_terminal
                )
                visible_clean += 1

                if record["slotparser_accepted"]:
                    log_pos.append(float(lp_pos))
                    log_native.append(float(lp_native))
                    log_cross.append(float(lp_cross))
                    if ti > 0:
                        primary_body += 1
                        if previous_terminal in source_model.prev_terminal_first:
                            supported_context += 1
                        else:
                            unsupported_context += 1
                previous_terminal = syms[-2]

        if not log_pos or not (len(log_pos) == len(log_native) == len(log_cross)):
            raise RuntimeError(f"{source_label}->{target_label} fold {f} score alignment failure")
        if not all(math.isfinite(v) for v in log_pos + log_native + log_cross):
            raise RuntimeError(f"{source_label}->{target_label} fold {f} non-finite score")

        n = len(log_pos)
        bits_pos = float(-sum(log_pos) / (n * LN2))
        bits_native = float(-sum(log_native) / (n * LN2))
        bits_cross = float(-sum(log_cross) / (n * LN2))
        g_native = float(bits_pos - bits_native)
        g_transport = float(bits_pos - bits_cross)

        if not math.isclose(
            g_native, EXPECTED_NATIVE_GAINS[target_label][f], rel_tol=0.0, abs_tol=TOL
        ):
            raise RuntimeError(
                f"{target_label} fold {f} native Issue145 gain failed to reproduce: {g_native}"
            )

        gate_row = gate["directions"][f"{source_label}_to_{target_label}"]["outer"][f]
        gate_target = gate_row["target_test"]
        if visible_clean != int(gate_target["target_clean_tokens"]):
            raise RuntimeError(f"{target_label} fold {f} clean target support changed")
        if n != int(gate_target["target_primary_targets"]):
            raise RuntimeError(f"{target_label} fold {f} primary target support changed")
        if primary_body != int(gate_target["target_primary_run_body_targets"]):
            raise RuntimeError(f"{target_label} fold {f} BODY support changed")
        if supported_context != int(
            gate_target["source_context_supported_primary_run_body_targets"]
        ):
            raise RuntimeError(f"{source_label}->{target_label} fold {f} supported-context count changed")
        if unsupported_context != int(
            gate_target["source_context_unsupported_primary_run_body_targets"]
        ):
            raise RuntimeError(f"{source_label}->{target_label} fold {f} unsupported-context count changed")

        outer.append(
            {
                "fold": f,
                "n_visible_clean_tokens": visible_clean,
                "n_scored_primary_targets": n,
                "n_scored_run_body_targets": primary_body,
                "source_context_supported_body_targets": supported_context,
                "source_context_unsupported_body_targets": unsupported_context,
                "source_context_coverage_fraction": float(supported_context / primary_body),
                "bits_POS2_TARGET": bits_pos,
                "bits_EDGE2_TARGET": bits_native,
                "bits_XEDGE2_SOURCE_TO_TARGET": bits_cross,
                "G_common_target_native": g_native,
                "G_transport": g_transport,
                "transport_minus_target_native_gain": float(g_transport - g_native),
            }
        )

    gains = [float(r["G_transport"]) for r in outer]
    mean_gain = float(sum(gains) / N_FOLDS)
    positive = int(sum(g > 0.0 for g in gains))
    passed = bool(mean_gain > 0.0 and positive >= 4)
    native_mean = float(sum(r["G_common_target_native"] for r in outer) / N_FOLDS)
    retention = float(mean_gain / native_mean) if native_mean > 0.0 else None

    return {
        "source": source_label,
        "target": target_label,
        "outer": outer,
        "primary": {
            "G_transport_by_fold": gains,
            "mean_G_transport": mean_gain,
            "positive_folds": positive,
            "required_positive_folds": 4,
            "mean_must_be_positive": True,
            "pass": passed,
            "mean_bits_POS2_TARGET": float(sum(r["bits_POS2_TARGET"] for r in outer) / N_FOLDS),
            "mean_bits_XEDGE2_SOURCE_TO_TARGET": float(
                sum(r["bits_XEDGE2_SOURCE_TO_TARGET"] for r in outer) / N_FOLDS
            ),
        },
        "secondary_non_promoting": {
            "mean_target_native_G_common": native_mean,
            "transport_retention_ratio": retention,
            "mean_transport_minus_target_native_gain": float(mean_gain - native_mean),
            "min_source_context_coverage_fraction": min(
                float(r["source_context_coverage_fraction"]) for r in outer
            ),
        },
    }


def frozen_class(zl_to_it_pass: bool, it_to_zl_pass: bool) -> str:
    if zl_to_it_pass and it_to_zl_pass:
        return "COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS"
    if zl_to_it_pass:
        return "COMMON-EVA LITERAL EDGE TABLE TRANSPORTS ZL3B→IT2A ONLY"
    if it_to_zl_pass:
        return "COMMON-EVA LITERAL EDGE TABLE TRANSPORTS IT2A→ZL3B ONLY"
    return "COMMON-EVA LITERAL EDGE TABLE TRANSPORTS NEITHER DIRECTION"


def score(zl_path: Path, it_path: Path) -> dict:
    gate, gate_sha = verify_post_gate_authority(zl_path, it_path)
    fold_identity = gate["issue145_authority"]["fold_identity_sha256"]
    if fold_identity != G148.EXPECTED["fold_sha256"]:
        raise RuntimeError("fold authority changed after Gate")

    leaf_fold = G148.G145.fold_authority(zl_path)[0]
    parser = G148.G145.E.SlotParser()
    G148.G145.E.validate_parser(parser)
    _zs, zl_lines = G148.G145.source_identity(zl_path, "ZL3b")
    _is, it_lines = G148.G145.source_identity(it_path, "IT2a")
    zl_runs = C145.clean_runs(zl_lines, leaf_fold, parser)
    it_runs = C145.clean_runs(it_lines, leaf_fold, parser)

    zl_to_it = score_direction("ZL3b", "IT2a", zl_runs, it_runs, gate)
    it_to_zl = score_direction("IT2a", "ZL3b", it_runs, zl_runs, gate)
    classification = frozen_class(
        bool(zl_to_it["primary"]["pass"]), bool(it_to_zl["primary"]["pass"])
    )
    if classification not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")

    return {
        "schema": "issue148-common-eva-table-first-reveal-v1",
        "issue": 148,
        "phase": "COMMON_EVA_LITERAL_TABLE_TRANSPORT_FIRST_REVEAL",
        "scored": True,
        "classification": classification,
        "authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": gate_sha,
            "gate0_expected_sha256": EXPECTED_GATE_RESULT_SHA256,
            "gate0_script_blob": EXPECTED_GATE_SCRIPT_BLOB,
            "gate0_provenance_blob": EXPECTED_GATE_PROVENANCE_BLOB,
            "gate0_merge": EXPECTED_GATE_MERGE,
            "issue145_scorer_blob": EXPECTED_ISSUE145_SCORER_BLOB,
            "fold_identity_sha256": fold_identity,
        },
        "frozen_transport": {
            "transported_object": "BODY P(first_common_atom | previous_terminal_common_atom) raw source counts",
            "all_non_edge_factors": "target-native",
            "k": C145.FIXED_K,
            "alpha": C145.FIXED_ALPHA,
            "outcome_vocabulary_size": C145.V,
            "unseen_source_context": "empty exact-context additive smoothing = 1/32",
            "target_native_fallback": False,
            "scalar_temperature_mixture_calibration": False,
        },
        "directions": {
            "ZL3b_to_IT2a": zl_to_it,
            "IT2a_to_ZL3b": it_to_zl,
        },
        "primary_joint": {
            "ZL3b_to_IT2a_pass": bool(zl_to_it["primary"]["pass"]),
            "IT2a_to_ZL3b_pass": bool(it_to_zl["primary"]["pass"]),
            "classification": classification,
        },
        "secondary_non_promoting": {
            "mean_transport_gain_directional_difference_ZL3b_to_IT2a_minus_IT2a_to_ZL3b": float(
                zl_to_it["primary"]["mean_G_transport"]
                - it_to_zl["primary"]["mean_G_transport"]
            ),
        },
        "firewall": {
            "post_reveal_atom_mapping_change": False,
            "post_reveal_support_matching": False,
            "target_native_edge_counts_used_in_transport_table": False,
            "transport_scalar_or_temperature_fit": False,
            "target_native_fallback_in_transport": False,
            "currier_hand_section_conditioned_transport": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "semantic_cipher_historical_direction_inference": False,
        },
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue148-common-eva-table-first-reveal-v1",
        "issue": 148,
        "phase": "COMMON_EVA_LITERAL_TABLE_TRANSPORT_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID CROSS-READING TABLE TRANSPORT",
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {
            "post_failure_table_repair_allowed": False,
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
    source_runs = (
        (0, 1, "f1r.1", 1, (
            {"raw": "ab", "atoms": ("a", "b"), "slotparser_accepted": True, "segment_index": 0},
            {"raw": "ba", "atoms": ("b", "a"), "slotparser_accepted": True, "segment_index": 1},
        )),
        (1, 2, "f2r.1", 2, (
            {"raw": "ca", "atoms": ("c", "a"), "slotparser_accepted": True, "segment_index": 0},
            {"raw": "ac", "atoms": ("a", "c"), "slotparser_accepted": True, "segment_index": 1},
        )),
    )
    target_model = C145.CommonEdgeModel(target_runs, {0, 1})
    source_model = C145.CommonEdgeModel(source_runs, {0, 1})
    syms = C145.token_symbols(("c", "a"))
    value = cross_token_logp(target_model, source_model, syms, False, "b")
    if not math.isfinite(value):
        raise AssertionError("synthetic cross-table score is not finite")
    unseen = cross_token_logp(target_model, source_model, syms, False, "z")
    if not math.isfinite(unseen):
        raise AssertionError("synthetic unseen-context score is not finite")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "cross_table_score_path_synthetic_only": True,
        "fixed_k": C145.FIXED_K,
        "fixed_alpha": C145.FIXED_ALPHA,
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
