#!/usr/bin/env python3
"""Issue #155: frozen common-EVA support-matched Currier first reveal.

The merged score-free Gate0 is reproduced exactly before any result is
accepted. Target-local POS2 factors are trained separately by reading and
Currier regime. Only the BODY previous-terminal -> first-atom table is replaced
by the opposite Currier regime's reading-balanced, context-mass-matched table
frozen by Gate0. No rho or target-native fallback is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
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

import issue145_common_eva_first_reveal as C145  # noqa: E402
import issue155_common_eva_currier_gate0 as G155  # noqa: E402

PLAN_PATH = CURRIER_DIR / "ISSUE155_COMMON_EVA_CURRIER_PLAN.md"
GATE_PROVENANCE_PATH = CURRIER_DIR / "ISSUE155_GATE0_PROVENANCE.md"
ISSUE151_SCORER_PATH = COMMON_EDGE_DIR / "issue151_shared_edge_first_reveal.py"
PHASE3A_PATH = ROOT / "experiments" / "predictive-information" / "phase3a" / "currier_gate0_audit.py"

EXPECTED_GATE_RESULT_SHA256 = "01f96038407975bc4d7a5944082a5bd2af9137f105edc33bd529cfccd33362f3"
EXPECTED_GATE_SCRIPT_BLOB = "f5ab4fa31a92b3c303401da33611ffd5f77b402d"
EXPECTED_GATE_PROVENANCE_BLOB = "ba2f443b24237ed5ee0dce127b1a43ad082481c4"
EXPECTED_PLAN_BLOB = "1f30d7c62083dbff378612ce7bf177ee7d9fff80"
EXPECTED_GATE_MERGE = "920130f721b83902c000c48f951c499a660f0683"
EXPECTED_ISSUE151_SCORER_BLOB = "2dcd68c8fa68080552a8b90a81e118568b35f8ef"
EXPECTED_PHASE3A_BLOB = "015ee2cda0de53e14d82302aea7e639570db7242"

N_FOLDS = 5
LN2 = math.log(2.0)
TOL = 1e-12
READINGS = ("ZL3b", "IT2a")
DIRECTIONS = ("A_to_B", "B_to_A")

VALID_CLASSES = (
    "COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: BIDIRECTIONAL",
    "COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: A→B ONLY",
    "COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: B→A ONLY",
    "COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE",
    "INVALID COMMON-EVA CURRIER TRANSPORT",
)


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G155.G151.G148.G145.git_blob_sha1(path.read_bytes())


def verify_post_gate_authority(zl_path: Path, it_path: Path) -> tuple[dict, str]:
    if git_blob(G155.HERE) != EXPECTED_GATE_SCRIPT_BLOB:
        raise RuntimeError("merged Issue155 Gate script blob changed")
    if git_blob(GATE_PROVENANCE_PATH) != EXPECTED_GATE_PROVENANCE_BLOB:
        raise RuntimeError("merged Issue155 Gate provenance blob changed")
    if git_blob(PLAN_PATH) != EXPECTED_PLAN_BLOB:
        raise RuntimeError("Issue155 plan blob changed")
    if git_blob(ISSUE151_SCORER_PATH) != EXPECTED_ISSUE151_SCORER_BLOB:
        raise RuntimeError("Issue151 scorer blob changed")
    if git_blob(PHASE3A_PATH) != EXPECTED_PHASE3A_BLOB:
        raise RuntimeError("Phase3A Currier authority blob changed")

    gate = G155.run_gate(zl_path, it_path)
    gate_sha = sha256_obj(gate)
    if gate_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Issue155 Gate result SHA changed: {gate_sha}")
    if not gate.get("gate_pass"):
        raise RuntimeError("Issue155 Gate no longer passes")
    if gate.get("scientific_currier_transport_metrics_computed") is not False:
        raise RuntimeError("Issue155 Gate firewall changed")
    return gate, gate_sha


def table_from_gate(summary: dict, regime: str) -> dict[str, Counter]:
    key = f"{regime}_matched_sparse_rational_counts"
    sha_key = f"{regime}_matched_sparse_rational_table_sha256"
    sparse = summary[key]
    if G155.sha256_obj(sparse) != summary[sha_key]:
        raise RuntimeError(f"Gate {regime} matched-table SHA no longer reproduces")
    out: dict[str, Counter] = defaultdict(Counter)
    for row in sparse:
        if len(row) != 4:
            raise RuntimeError("malformed rational matched-table row")
        ctx, outcome, num, den = row
        value = Fraction(int(num), int(den))
        if value <= 0:
            raise RuntimeError("nonpositive Gate matched-table cell")
        out[str(ctx)][str(outcome)] = value
    return dict(out)


def fractional_categorical_logp(counter: Mapping[str, Fraction], symbol: str) -> float:
    total = sum(counter.values(), Fraction(0, 1))
    c = counter.get(symbol, Fraction(0, 1))
    alpha = Fraction(1, 100)
    p = (c + alpha) / (total + alpha * C145.V)
    return math.log(float(p))


def matched_token_logp(
    target_model: C145.CommonEdgeModel,
    matched_table: Mapping[str, Mapping[str, Fraction]],
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
            raise RuntimeError("BODY target lacks previous terminal")
        ll += fractional_categorical_logp(matched_table.get(previous_terminal, {}), first)
        ll += target_model.categorical_logp(target_model.body_second[first], second)
    for j in range(2, len(syms)):
        ll += target_model.run_model.logp(syms[j - 2 : j], syms[j])
    return float(ll)


def leaf_currier_from_gate(gate: dict) -> dict[int, str]:
    c = gate["currier_physical_leaf_authority"]
    a = set(map(int, c["A_ONLY"]))
    b = set(map(int, c["B_ONLY"]))
    if a & b:
        raise RuntimeError("Gate Currier A/B leaf sets overlap")
    out = {leaf: "A" for leaf in a}
    out.update({leaf: "B" for leaf in b})
    return out


def filter_runs(runs, leaf_currier: Mapping[int, str], regime: str):
    return tuple(run for run in runs if leaf_currier.get(int(run[1])) == regime)


def score_target_regime(
    reading: str,
    target_regime: str,
    target_runs,
    gate: dict,
) -> dict:
    source_regime = "A" if target_regime == "B" else "B"
    direction = f"{source_regime}_to_{target_regime}"
    all_folds = set(range(N_FOLDS))
    outer = []

    for f in range(N_FOLDS):
        train_folds = all_folds - {f}
        target_model = C145.CommonEdgeModel(target_runs, train_folds)
        gate_row = gate["outer"][f]
        matched_summary = gate_row["matched_currier_tables"]
        source_table = table_from_gate(matched_summary, source_regime)
        native_table = table_from_gate(matched_summary, target_regime)
        retained_contexts = set(matched_summary["retained_previous_terminal_contexts"])
        if set(source_table) != retained_contexts or set(native_table) != retained_contexts:
            raise RuntimeError(f"fold {f} matched-table context identity changed")

        log_pos = []
        log_transport = []
        log_native = []
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
                lp_transport = matched_token_logp(
                    target_model, source_table, syms, ti == 0, previous_terminal
                )
                lp_native = matched_token_logp(
                    target_model, native_table, syms, ti == 0, previous_terminal
                )
                visible_clean += 1
                if record["slotparser_accepted"]:
                    log_pos.append(float(lp_pos))
                    log_transport.append(float(lp_transport))
                    log_native.append(float(lp_native))
                    if ti > 0:
                        primary_body += 1
                        if previous_terminal in retained_contexts:
                            supported += 1
                        else:
                            unsupported += 1
                previous_terminal = syms[-2]

        if not log_pos or not (len(log_pos) == len(log_transport) == len(log_native)):
            raise RuntimeError(f"{reading}/{target_regime} fold {f} score alignment failure")
        if not all(math.isfinite(v) for v in log_pos + log_transport + log_native):
            raise RuntimeError(f"{reading}/{target_regime} fold {f} non-finite score")

        n = len(log_pos)
        bits_pos = float(-sum(log_pos) / (n * LN2))
        bits_transport = float(-sum(log_transport) / (n * LN2))
        bits_native = float(-sum(log_native) / (n * LN2))
        g_transport = float(bits_pos - bits_transport)
        g_native = float(bits_pos - bits_native)
        transport_minus_native = float(g_transport - g_native)

        expected = gate_row["target_context_support"][reading][target_regime]
        if visible_clean != int(expected["target_clean_tokens"]):
            raise RuntimeError(f"{reading}/{target_regime} fold {f} clean target support changed")
        if n != int(expected["target_primary_targets"]):
            raise RuntimeError(f"{reading}/{target_regime} fold {f} primary target support changed")
        if primary_body != int(expected["target_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{target_regime} fold {f} BODY target support changed")
        if supported != int(expected["matched_context_supported_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{target_regime} fold {f} matched-context support changed")
        if unsupported != int(expected["matched_context_unsupported_primary_run_body_targets"]):
            raise RuntimeError(f"{reading}/{target_regime} fold {f} unsupported-context support changed")

        outer.append(
            {
                "fold": f,
                "source_regime": source_regime,
                "target_regime": target_regime,
                "n_visible_clean_tokens": visible_clean,
                "n_scored_primary_targets": n,
                "n_scored_run_body_targets": primary_body,
                "matched_context_supported_body_targets": supported,
                "matched_context_unsupported_body_targets": unsupported,
                "bits_POS2_TARGET_REGIME": bits_pos,
                "bits_XEDGE2_SOURCE_MATCHED": bits_transport,
                "bits_EDGE2_TARGET_REGIME_MATCHED": bits_native,
                "G_transport": g_transport,
                "G_target_regime_native_matched": g_native,
                "transport_minus_target_native_matched_gain": transport_minus_native,
                "source_matched_table_sha256": matched_summary[
                    f"{source_regime}_matched_sparse_rational_table_sha256"
                ],
                "target_native_matched_table_sha256": matched_summary[
                    f"{target_regime}_matched_sparse_rational_table_sha256"
                ],
            }
        )

    gains = [float(r["G_transport"]) for r in outer]
    native = [float(r["G_target_regime_native_matched"]) for r in outer]
    mean_gain = float(sum(gains) / N_FOLDS)
    positive = int(sum(g > 0.0 for g in gains))
    passed = bool(mean_gain > 0.0 and positive >= 4)
    native_mean = float(sum(native) / N_FOLDS)
    return {
        "reading": reading,
        "direction": direction,
        "source_regime": source_regime,
        "target_regime": target_regime,
        "outer": outer,
        "primary": {
            "G_transport_by_fold": gains,
            "mean_G_transport": mean_gain,
            "positive_folds": positive,
            "required_positive_folds": 4,
            "mean_must_be_positive": True,
            "pass_within_reading": passed,
            "mean_bits_POS2_TARGET_REGIME": float(
                sum(r["bits_POS2_TARGET_REGIME"] for r in outer) / N_FOLDS
            ),
            "mean_bits_XEDGE2_SOURCE_MATCHED": float(
                sum(r["bits_XEDGE2_SOURCE_MATCHED"] for r in outer) / N_FOLDS
            ),
        },
        "secondary_non_promoting": {
            "G_target_regime_native_matched_by_fold": native,
            "mean_G_target_regime_native_matched": native_mean,
            "transport_to_native_matched_gain_ratio": float(mean_gain / native_mean)
            if native_mean > 0.0
            else None,
            "mean_transport_minus_target_native_matched_gain": float(mean_gain - native_mean),
            "min_matched_context_coverage_fraction": min(
                r["matched_context_supported_body_targets"] / r["n_scored_run_body_targets"]
                for r in outer
            ),
        },
    }


def frozen_class(results: dict) -> tuple[str, dict]:
    a_to_b_robust = bool(
        results["ZL3b"]["A_to_B"]["primary"]["pass_within_reading"]
        and results["IT2a"]["A_to_B"]["primary"]["pass_within_reading"]
    )
    b_to_a_robust = bool(
        results["ZL3b"]["B_to_A"]["primary"]["pass_within_reading"]
        and results["IT2a"]["B_to_A"]["primary"]["pass_within_reading"]
    )
    if a_to_b_robust and b_to_a_robust:
        classification = "COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: BIDIRECTIONAL"
    elif a_to_b_robust:
        classification = "COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: A→B ONLY"
    elif b_to_a_robust:
        classification = "COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: B→A ONLY"
    else:
        classification = "COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE"
    return classification, {
        "A_to_B_robust_in_both_readings": a_to_b_robust,
        "B_to_A_robust_in_both_readings": b_to_a_robust,
    }


def score(zl_path: Path, it_path: Path) -> dict:
    gate, gate_sha = verify_post_gate_authority(zl_path, it_path)
    leaf_currier = leaf_currier_from_gate(gate)
    leaf_fold = G155.G151.G148.G145.fold_authority(zl_path)[0]
    parser = G155.G151.G148.G145.E.SlotParser()
    G155.G151.G148.G145.E.validate_parser(parser)
    _zs, zl_lines = G155.G151.G148.G145.source_identity(zl_path, "ZL3b")
    _is, it_lines = G155.G151.G148.G145.source_identity(it_path, "IT2a")
    all_runs = {
        "ZL3b": C145.clean_runs(zl_lines, leaf_fold, parser),
        "IT2a": C145.clean_runs(it_lines, leaf_fold, parser),
    }
    regime_runs = {
        reading: {
            regime: filter_runs(all_runs[reading], leaf_currier, regime)
            for regime in ("A", "B")
        }
        for reading in READINGS
    }

    results = {}
    for reading in READINGS:
        results[reading] = {
            "A_to_B": score_target_regime(reading, "B", regime_runs[reading]["B"], gate),
            "B_to_A": score_target_regime(reading, "A", regime_runs[reading]["A"], gate),
        }

    classification, joint = frozen_class(results)
    if classification not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")

    return {
        "schema": "issue155-common-eva-currier-first-reveal-v1",
        "issue": 155,
        "phase": "COMMON_EVA_SUPPORT_MATCHED_CURRIER_FIRST_REVEAL",
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
            "issue151_scorer_blob": EXPECTED_ISSUE151_SCORER_BLOB,
            "phase3a_currier_script_blob": EXPECTED_PHASE3A_BLOB,
        },
        "frozen_model": {
            "representation": "Issue145/151 common Basic-EVA",
            "reading_balanced_source_tables": True,
            "reading_weights": {"ZL3b": 0.5, "IT2a": 0.5},
            "context_by_context_A_B_effective_mass_matched": True,
            "target_non_edge_factors": "target-reading and target-Currier native",
            "k": C145.FIXED_K,
            "alpha": C145.FIXED_ALPHA,
            "outcome_vocabulary_size": C145.V,
            "unsupported_exact_context": "empty additive distribution",
            "target_native_fallback": False,
            "primary_rho_mixture_calibration": False,
        },
        "readings": results,
        "primary_joint": {**joint, "classification": classification},
        "secondary_non_promoting": {
            "A_to_B_mean_gain_difference_ZL3b_minus_IT2a": float(
                results["ZL3b"]["A_to_B"]["primary"]["mean_G_transport"]
                - results["IT2a"]["A_to_B"]["primary"]["mean_G_transport"]
            ),
            "B_to_A_mean_gain_difference_ZL3b_minus_IT2a": float(
                results["ZL3b"]["B_to_A"]["primary"]["mean_G_transport"]
                - results["IT2a"]["B_to_A"]["primary"]["mean_G_transport"]
            ),
        },
        "firewall": {
            "post_reveal_currier_label_change": False,
            "post_reveal_atom_mapping_change": False,
            "post_reveal_reading_weight_change": False,
            "post_reveal_context_match_change": False,
            "target_native_fallback": False,
            "primary_rho_mixture_fit": False,
            "hand_section_domain_conditioning": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "semantic_cipher_historical_direction_inference": False,
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
    table = {
        "b": {"c": Fraction(3, 2), "a": Fraction(1, 2)},
        "a": {"b": Fraction(2, 1)},
    }
    syms = C145.token_symbols(("c", "a"))
    seen = matched_token_logp(model, table, syms, False, "b")
    unseen = matched_token_logp(model, table, syms, False, "z")
    if not (math.isfinite(seen) and math.isfinite(unseen)):
        raise AssertionError("synthetic matched-table score non-finite")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "real_target_scores_computed": False,
        "fractional_matched_table_path_synthetic_only": True,
        "k": C145.FIXED_K,
        "alpha": C145.FIXED_ALPHA,
        "V": C145.V,
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue155-common-eva-currier-first-reveal-v1",
        "issue": 155,
        "phase": "COMMON_EVA_SUPPORT_MATCHED_CURRIER_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID COMMON-EVA CURRIER TRANSPORT",
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
