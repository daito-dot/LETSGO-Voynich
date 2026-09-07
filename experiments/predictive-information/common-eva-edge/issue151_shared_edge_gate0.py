#!/usr/bin/env python3
"""Issue #151 Gate0: score-free shared common-EVA edge-table audit.

This executable verifies entry authority, physical-leaf leakage, training-only
edge counts, the frozen 0.5/0.5 fractional consensus construction and held-out
previous-terminal context support. It deliberately implements no real-target
shared-table probability, likelihood, bits/token, G_shared or G_specific.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
COMMON_DIR = ROOT / "experiments" / "predictive-information" / "common-eva-edge"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

import issue148_common_eva_table_gate0 as G148  # noqa: E402

ISSUE148_GATE_PROVENANCE_PATH = COMMON_DIR / "ISSUE148_GATE0_PROVENANCE.md"
ISSUE148_SCORER_PATH = COMMON_DIR / "issue148_common_eva_table_first_reveal.py"
ISSUE145_SCORER_PATH = COMMON_DIR / "issue145_common_eva_first_reveal.py"
PLAN_PATH = COMMON_DIR / "ISSUE151_SHARED_EDGE_CONSOLIDATION_PLAN.md"

EXPECTED = {
    "issue148_gate_result_sha256": "f324264b814ef02d8de70b804754750ec579f8a9e0d8dffb0f1575439867d1bf",
    "issue148_gate_script_blob": "a8029aac50ccc6e09ec975b7b86a1bde44415f9f",
    "issue148_gate_provenance_blob": "7f97b9731a6e72e2456ede436e837a3735f265fd",
    "issue148_scorer_blob": "7847c0fea1dcfc4ace5752d0188d70e3739679d3",
    "issue148_result_sha256": "305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923",
    "issue148_artifact_id": 10001309613,
    "issue148_artifact_zip_digest": "sha256:cfefd670b00ebb3eae3020a4b5308115ec9172b793ed1fe4b598928718f5c622",
    "issue148_merge": "b7e643a0d3075a9f09dbd9ec3a8f50149cb4a131",
    "issue145_scorer_blob": "ce8a167c607fbcf2807f567439ab6837471f4f07",
    "issue145_result_sha256": "663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2",
    "fold_sha256": "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b",
    "weight_ZL3b": 0.5,
    "weight_IT2a": 0.5,
    "alpha": 0.01,
    "V": 32,
    "n_atom_outcomes": 31,
    "n_folds": 5,
    "min_primary_body": 300,
    "min_consensus_supported_primary_body": 300,
}

ATOM_OUTCOMES = tuple(sorted(G148.G145.ATOM_OUTCOMES))
if len(ATOM_OUTCOMES) != EXPECTED["n_atom_outcomes"]:
    raise RuntimeError("common-EVA atom inventory drifted")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def git_blob(path: Path) -> str:
    return G148.G145.git_blob_sha1(path.read_bytes())


def verify_entry_authority(zl_path: Path, it_path: Path) -> tuple[dict, str, dict[int, int], list[list[int]]]:
    if git_blob(G148.HERE) != EXPECTED["issue148_gate_script_blob"]:
        raise RuntimeError("Issue148 Gate script blob changed")
    if git_blob(ISSUE148_GATE_PROVENANCE_PATH) != EXPECTED["issue148_gate_provenance_blob"]:
        raise RuntimeError("Issue148 Gate provenance blob changed")
    if git_blob(ISSUE148_SCORER_PATH) != EXPECTED["issue148_scorer_blob"]:
        raise RuntimeError("Issue148 scorer blob changed")
    if git_blob(ISSUE145_SCORER_PATH) != EXPECTED["issue145_scorer_blob"]:
        raise RuntimeError("Issue145 scorer blob changed")
    if not PLAN_PATH.is_file():
        raise RuntimeError("Issue151 frozen plan missing")

    gate148 = G148.run_gate(zl_path, it_path)
    gate148_sha = sha256_text(G148.canonical_json(gate148))
    if gate148_sha != EXPECTED["issue148_gate_result_sha256"]:
        raise RuntimeError(f"Issue148 Gate result SHA changed: {gate148_sha}")
    if not gate148.get("gate_pass"):
        raise RuntimeError("Issue148 Gate no longer passes")
    if gate148.get("scientific_transport_metrics_computed") is not False:
        raise RuntimeError("Issue148 Gate firewall changed")

    leaf_fold, identity, fold_sha = G148.G145.fold_authority(zl_path)
    if fold_sha != EXPECTED["fold_sha256"]:
        raise RuntimeError("physical-leaf fold authority changed")
    return gate148, gate148_sha, leaf_fold, identity


def training_edge_counts(records: Sequence[dict], heldout_fold: int) -> tuple[dict[str, Counter], set[int], dict]:
    train = [r for r in records if int(r["fold"]) != heldout_fold]
    body = [r for r in train if not bool(r["is_run_start"])]
    by_context: dict[str, Counter] = defaultdict(Counter)
    for r in body:
        ctx = r["previous_terminal_atom"]
        outcome = r["first_atom"]
        if ctx is None:
            raise RuntimeError("training BODY event missing previous terminal")
        if ctx not in G148.G145.ATOM_OUTCOMES or outcome not in G148.G145.ATOM_OUTCOMES:
            raise RuntimeError("training edge atom escaped common-EVA inventory")
        by_context[str(ctx)][str(outcome)] += 1

    if not train or not body or not by_context:
        raise RuntimeError(f"degenerate training support in fold {heldout_fold}")

    leaves = {int(r["leaf"]) for r in train}
    total = sum(sum(c.values()) for c in by_context.values())
    if total != len(body):
        raise RuntimeError("training BODY count/matrix mass mismatch")

    sparse = {
        ctx: {outcome: int(count) for outcome, count in sorted(counts.items())}
        for ctx, counts in sorted(by_context.items())
    }
    matrix = {
        ctx: [int(by_context.get(ctx, Counter()).get(outcome, 0)) for outcome in ATOM_OUTCOMES]
        for ctx in ATOM_OUTCOMES
    }
    matrix_sha = sha256_text(canonical_json({"atoms": ATOM_OUTCOMES, "matrix": matrix}))
    pairs = sum(len(c) for c in by_context.values())

    return by_context, leaves, {
        "training_clean_tokens": len(train),
        "training_run_body_tokens": len(body),
        "training_leaf_count": len(leaves),
        "n_previous_terminal_contexts": len(by_context),
        "n_observed_context_outcome_pairs": pairs,
        "matrix_total_mass": total,
        "observable_atom_inventory": list(ATOM_OUTCOMES),
        "model_outcome_vocabulary_size_with_END": EXPECTED["V"],
        "END_observed_in_edge_count_matrix": False,
        "sparse_counts": sparse,
        "dense_31x31_observed_atom_matrix_sha256": matrix_sha,
    }


def balanced_consensus(
    zl_counts: Mapping[str, Counter], it_counts: Mapping[str, Counter]
) -> tuple[dict[str, Counter], dict]:
    contexts = sorted(set(zl_counts) | set(it_counts))
    out: dict[str, Counter] = {}
    for ctx in contexts:
        counter = Counter()
        for outcome in ATOM_OUTCOMES:
            z = int(zl_counts.get(ctx, Counter()).get(outcome, 0))
            i = int(it_counts.get(ctx, Counter()).get(outcome, 0))
            value = EXPECTED["weight_ZL3b"] * z + EXPECTED["weight_IT2a"] * i
            if value:
                counter[outcome] = float(value)
        out[ctx] = counter

    # Every consensus count must be exactly the frozen arithmetic mean.
    for ctx in contexts:
        for outcome in ATOM_OUTCOMES:
            expected = 0.5 * int(zl_counts.get(ctx, Counter()).get(outcome, 0)) + 0.5 * int(
                it_counts.get(ctx, Counter()).get(outcome, 0)
            )
            got = float(out[ctx].get(outcome, 0.0))
            if got != expected:
                raise RuntimeError("fractional consensus arithmetic drifted")

    sparse = {
        ctx: {outcome: float(count) for outcome, count in sorted(counts.items())}
        for ctx, counts in sorted(out.items())
        if counts
    }
    matrix = {
        ctx: [float(out.get(ctx, Counter()).get(outcome, 0.0)) for outcome in ATOM_OUTCOMES]
        for ctx in ATOM_OUTCOMES
    }
    total = float(sum(sum(c.values()) for c in out.values()))
    positive_pairs = sum(sum(v > 0.0 for v in c.values()) for c in out.values())
    matrix_sha = sha256_text(canonical_json({"atoms": ATOM_OUTCOMES, "matrix": matrix}))
    return out, {
        "weights": {"ZL3b": 0.5, "IT2a": 0.5},
        "n_previous_terminal_contexts": sum(bool(c) for c in out.values()),
        "n_positive_context_outcome_pairs": positive_pairs,
        "matrix_total_mass": total,
        "sparse_fractional_counts": sparse,
        "dense_31x31_observed_atom_matrix_sha256": matrix_sha,
        "additive_alpha_for_future_scorer": EXPECTED["alpha"],
        "model_outcome_vocabulary_size_with_END": EXPECTED["V"],
        "real_target_probability_computed": False,
    }


def target_context_support(records: Sequence[dict], heldout_fold: int, contexts: set[str]) -> dict:
    test = [r for r in records if int(r["fold"]) == heldout_fold]
    primary = [r for r in test if bool(r["slotparser_accepted"])]
    body = [r for r in primary if not bool(r["is_run_start"])]
    supported = sum(r["previous_terminal_atom"] in contexts for r in body)
    unsupported = len(body) - supported
    if len(body) < EXPECTED["min_primary_body"]:
        raise RuntimeError(f"target primary BODY support below threshold in fold {heldout_fold}")
    if supported < EXPECTED["min_consensus_supported_primary_body"]:
        raise RuntimeError(f"consensus-context-supported BODY support below threshold in fold {heldout_fold}")
    return {
        "target_clean_tokens": len(test),
        "target_primary_targets": len(primary),
        "target_primary_run_body_targets": len(body),
        "consensus_context_supported_primary_run_body_targets": int(supported),
        "consensus_context_unsupported_primary_run_body_targets": int(unsupported),
        "consensus_context_coverage_fraction": float(supported / len(body)) if body else None,
        "heldout_current_first_atom_used_for_support_selection": False,
    }


def synthetic_fractional_test() -> dict:
    z = {
        "a": Counter({"b": 2, "c": 1}),
        "e": Counter({"a": 2}),
    }
    i = {
        "a": Counter({"b": 4, "d": 2}),
        "e": Counter(),
    }
    c, _summary = balanced_consensus(z, i)
    expected = {("a", "b"): 3.0, ("a", "c"): 0.5, ("a", "d"): 1.0, ("e", "a"): 1.0}
    for (ctx, outcome), value in expected.items():
        if float(c.get(ctx, Counter()).get(outcome, 0.0)) != value:
            raise AssertionError("synthetic 0.5/0.5 consensus failed")

    counts = c["a"]
    denom = float(sum(counts.values()) + EXPECTED["alpha"] * EXPECTED["V"])
    p_seen = float((counts["b"] + EXPECTED["alpha"]) / denom)
    p_end = float(EXPECTED["alpha"] / denom)
    if not (math.isfinite(p_seen) and math.isfinite(p_end) and p_seen > p_end > 0.0):
        raise AssertionError("synthetic fractional additive smoothing failed")
    return {
        "ok": True,
        "uses_real_target_data": False,
        "weights": {"ZL3b": 0.5, "IT2a": 0.5},
        "alpha": EXPECTED["alpha"],
        "V": EXPECTED["V"],
        "synthetic_seen_probability_finite": True,
        "synthetic_END_probability_finite": True,
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    gate148, gate148_sha, leaf_fold, fold_identity = verify_entry_authority(zl_path, it_path)

    parser = G148.G145.E.SlotParser()
    G148.G145.E.validate_parser(parser)
    _zs, zl_lines = G148.G145.source_identity(zl_path, "ZL3b")
    _is, it_lines = G148.G145.source_identity(it_path, "IT2a")
    zl_records = G148.clean_events(zl_lines, leaf_fold, parser)
    it_records = G148.clean_events(it_lines, leaf_fold, parser)

    rows = []
    for f in range(EXPECTED["n_folds"]):
        zl_counts, zl_train_leaves, zl_train = training_edge_counts(zl_records, f)
        it_counts, it_train_leaves, it_train = training_edge_counts(it_records, f)
        consensus, consensus_summary = balanced_consensus(zl_counts, it_counts)
        consensus_contexts = {ctx for ctx, counts in consensus.items() if counts}

        heldout_leaves = set(int(x) for x in fold_identity[f])
        overlaps = {
            "ZL3b_training_vs_heldout": sorted(zl_train_leaves & heldout_leaves),
            "IT2a_training_vs_heldout": sorted(it_train_leaves & heldout_leaves),
            "consensus_training_union_vs_heldout": sorted((zl_train_leaves | it_train_leaves) & heldout_leaves),
        }
        if any(overlaps.values()):
            raise RuntimeError(f"fold {f} physical-leaf leakage: {overlaps}")

        zl_target = target_context_support(zl_records, f, consensus_contexts)
        it_target = target_context_support(it_records, f, consensus_contexts)

        # Reproduce target supports already frozen by Issue #148 Gate0.
        exp_z = gate148["directions"]["IT2a_to_ZL3b"]["outer"][f]["target_test"]
        exp_i = gate148["directions"]["ZL3b_to_IT2a"]["outer"][f]["target_test"]
        for label, got, exp in (("ZL3b", zl_target, exp_z), ("IT2a", it_target, exp_i)):
            if got["target_clean_tokens"] != int(exp["target_clean_tokens"]):
                raise RuntimeError(f"{label} fold {f} clean target support changed")
            if got["target_primary_targets"] != int(exp["target_primary_targets"]):
                raise RuntimeError(f"{label} fold {f} primary target support changed")
            if got["target_primary_run_body_targets"] != int(exp["target_primary_run_body_targets"]):
                raise RuntimeError(f"{label} fold {f} primary BODY support changed")

        # Reproduce per-reading training supports from Issue #145 authority carried by #148.
        gate145 = G148.verify_issue145_authority(zl_path, it_path)[0]
        exp_z_train = gate145["readings"]["ZL3b"]["outer_training_support"][f]
        exp_i_train = gate145["readings"]["IT2a"]["outer_training_support"][f]
        if zl_train["training_clean_tokens"] != int(exp_z_train["training_clean_tokens"]):
            raise RuntimeError(f"ZL3b fold {f} training clean support changed")
        if zl_train["training_run_body_tokens"] != int(exp_z_train["training_run_body_tokens"]):
            raise RuntimeError(f"ZL3b fold {f} training BODY support changed")
        if it_train["training_clean_tokens"] != int(exp_i_train["training_clean_tokens"]):
            raise RuntimeError(f"IT2a fold {f} training clean support changed")
        if it_train["training_run_body_tokens"] != int(exp_i_train["training_run_body_tokens"]):
            raise RuntimeError(f"IT2a fold {f} training BODY support changed")

        expected_consensus_mass = 0.5 * zl_train["training_run_body_tokens"] + 0.5 * it_train["training_run_body_tokens"]
        if consensus_summary["matrix_total_mass"] != expected_consensus_mass:
            raise RuntimeError(f"fold {f} consensus total mass changed")

        rows.append(
            {
                "outer_fold": f,
                "heldout_physical_leaves": sorted(heldout_leaves),
                "leakage": overlaps,
                "ZL3b_training": zl_train,
                "IT2a_training": it_train,
                "shared_training_table": consensus_summary,
                "ZL3b_target_context_support": zl_target,
                "IT2a_target_context_support": it_target,
            }
        )

    synthetic = synthetic_fractional_test()
    return {
        "schema": "issue151-shared-edge-gate0-v1",
        "issue": 151,
        "phase": "SHARED_COMMON_EVA_EDGE_CONSOLIDATION_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED SHARED-EDGE SCORER",
        "scientific_shared_table_metrics_computed": False,
        "entry_authority": {
            "issue148_gate_reproduced": True,
            "issue148_gate_result_sha256": gate148_sha,
            "issue148_gate_script_blob": EXPECTED["issue148_gate_script_blob"],
            "issue148_gate_provenance_blob": EXPECTED["issue148_gate_provenance_blob"],
            "issue148_scorer_blob": EXPECTED["issue148_scorer_blob"],
            "issue148_declared_first_reveal_result_sha256": EXPECTED["issue148_result_sha256"],
            "issue148_declared_artifact_id": EXPECTED["issue148_artifact_id"],
            "issue148_declared_artifact_zip_digest": EXPECTED["issue148_artifact_zip_digest"],
            "issue148_merge": EXPECTED["issue148_merge"],
            "issue145_scorer_blob": EXPECTED["issue145_scorer_blob"],
            "issue145_declared_first_reveal_result_sha256": EXPECTED["issue145_result_sha256"],
            "fold_identity_sha256": EXPECTED["fold_sha256"],
            "plan_blob_sha1": git_blob(PLAN_PATH),
        },
        "representation": gate148["representation"],
        "shared_table_contract": {
            "count_formula": "0.5*C_ZL3b + 0.5*C_IT2a",
            "weights": {"ZL3b": 0.5, "IT2a": 0.5},
            "training_physical_leaves": "both readings; outer heldout fold excluded from both",
            "alpha_for_future_scorer": EXPECTED["alpha"],
            "V_with_END_for_future_scorer": EXPECTED["V"],
            "target_native_fallback": False,
            "scalar_temperature_calibration_interpolation_mixture": False,
        },
        "outer": rows,
        "support_thresholds": {
            "min_target_primary_run_body": EXPECTED["min_primary_body"],
            "min_consensus_context_supported_target_primary_run_body": EXPECTED[
                "min_consensus_supported_primary_body"
            ],
        },
        "synthetic_fractional_count_test": synthetic,
        "firewall": {
            "scientific_shared_table_metrics_computed": False,
            "real_target_shared_table_probability_computed": False,
            "real_target_shared_table_likelihood_computed": False,
            "bits_EDGE2_SHARED_computed": False,
            "G_shared_computed": False,
            "G_specific_computed": False,
            "retention_ratio_computed": False,
            "scientific_classification_computed": False,
            "heldout_current_first_atom_used_for_support_selection": False,
            "target_selected_support_matching": False,
            "target_selected_atom_mapping": False,
            "weights_tuned": False,
            "k_alpha_smoothing_or_fallback_tuned": False,
            "currier_hand_section_conditioned_shared_table": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
        },
    }


def self_test() -> dict:
    result = synthetic_fractional_test()
    result.update(
        {
            "target_sources_loaded": False,
            "scientific_shared_table_metrics_computed": False,
            "support_audit_only": True,
        }
    )
    return result


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue151-shared-edge-gate0-v1",
        "issue": 151,
        "phase": "SHARED_COMMON_EVA_EDGE_CONSOLIDATION_GATE0",
        "gate_pass": False,
        "gate_disposition": "INVALID SHARED EDGE CONSOLIDATION — GATE0 FAILED",
        "scientific_shared_table_metrics_computed": False,
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {"scientific_shared_table_metrics_computed": False},
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
