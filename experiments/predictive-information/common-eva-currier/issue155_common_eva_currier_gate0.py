#!/usr/bin/env python3
"""Issue #155 Gate0: score-free common-EVA support-matched Currier audit.

The Gate reproduces Issue #151 and Phase 3A Currier authority, reuses the
physical-leaf Currier classes in both ZL3b and IT2a, builds training-only
reading-balanced Currier edge counts, matches A/B effective mass exactly by
previous-terminal context using rational arithmetic, and audits held-out
context support. It deliberately implements no real-target transport scoring.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
COMMON_EDGE_DIR = ROOT / "experiments" / "predictive-information" / "common-eva-edge"
PHASE3A_PATH = ROOT / "experiments" / "predictive-information" / "phase3a" / "currier_gate0_audit.py"
PLAN_PATH = HERE.parent / "ISSUE155_COMMON_EVA_CURRIER_PLAN.md"
ISSUE151_GATE_PATH = COMMON_EDGE_DIR / "issue151_shared_edge_gate0.py"
ISSUE151_GATE_PROVENANCE_PATH = COMMON_EDGE_DIR / "ISSUE151_GATE0_PROVENANCE.md"
ISSUE151_SCORER_PATH = COMMON_EDGE_DIR / "issue151_shared_edge_first_reveal.py"
ISSUE151_FIRST_PROVENANCE_PATH = COMMON_EDGE_DIR / "ISSUE151_FIRST_REVEAL_PROVENANCE.md"

if str(COMMON_EDGE_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_EDGE_DIR))

import issue151_shared_edge_gate0 as G151  # noqa: E402

EXPECTED = {
    "issue151_gate_result_sha256": "bcc6c6bd5600ef9f74484807b51ef1db454613bae2bbd351d90f089c8693eea2",
    "issue151_gate_script_blob": "d5e3bd22501f8caebabc7c2728bc7f8d5cb59018",
    "issue151_gate_provenance_blob": "609ee5f208cfdb3739749d8d82e34d68e4803dd6",
    "issue151_scorer_blob": "2dcd68c8fa68080552a8b90a81e118568b35f8ef",
    "issue151_first_provenance_blob": "b599d7a3b4a2c749262231f711c6f14aa6a0cb0e",
    "issue151_first_result_sha256": "cb7d88b88a65df58c8d93d047b8fbfe4d2eda20d4c7314713c9d44e31a9b7355",
    "issue151_merge": "5562f966a5469e9da26406c23f47d60c8c2db17f",
    "phase3a_script_blob": "015ee2cda0de53e14d82302aea7e639570db7242",
    "phase3a_result_sha256": "e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e",
    "fold_sha256": "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b",
    "n_folds": 5,
    "weight_ZL3b_num": 1,
    "weight_ZL3b_den": 2,
    "weight_IT2a_num": 1,
    "weight_IT2a_den": 2,
    "alpha_num": 1,
    "alpha_den": 100,
    "V": 32,
    "min_primary_body": 300,
    "min_matched_context_supported_primary_body": 300,
}

LABELS = ("A", "B")
READINGS = ("ZL3b", "IT2a")
ATOM_OUTCOMES = tuple(sorted(G151.G148.G145.ATOM_OUTCOMES))


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G151.G148.G145.git_blob_sha1(path.read_bytes())


def load_phase3a():
    spec = importlib.util.spec_from_file_location("issue155_phase3a_currier", PHASE3A_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen Phase3A Currier authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def verify_entry_authority(zl_path: Path, it_path: Path):
    if git_blob(ISSUE151_GATE_PATH) != EXPECTED["issue151_gate_script_blob"]:
        raise RuntimeError("Issue151 Gate script blob changed")
    if git_blob(ISSUE151_GATE_PROVENANCE_PATH) != EXPECTED["issue151_gate_provenance_blob"]:
        raise RuntimeError("Issue151 Gate provenance blob changed")
    if git_blob(ISSUE151_SCORER_PATH) != EXPECTED["issue151_scorer_blob"]:
        raise RuntimeError("Issue151 scorer blob changed")
    if git_blob(ISSUE151_FIRST_PROVENANCE_PATH) != EXPECTED["issue151_first_provenance_blob"]:
        raise RuntimeError("Issue151 first-reveal provenance blob changed")
    if git_blob(PHASE3A_PATH) != EXPECTED["phase3a_script_blob"]:
        raise RuntimeError("Phase3A Currier authority script blob changed")
    if not PLAN_PATH.is_file():
        raise RuntimeError("Issue155 frozen plan missing")

    gate151 = G151.run_gate(zl_path, it_path)
    gate151_sha = sha256_obj(gate151)
    if gate151_sha != EXPECTED["issue151_gate_result_sha256"]:
        raise RuntimeError(f"Issue151 Gate result SHA changed: {gate151_sha}")
    if not gate151.get("gate_pass"):
        raise RuntimeError("Issue151 Gate no longer passes")
    if gate151.get("scientific_shared_table_metrics_computed") is not False:
        raise RuntimeError("Issue151 Gate firewall changed")

    P3 = load_phase3a()
    phase3a = P3.audit(zl_path)
    phase3a_sha = hashlib.sha256(
        (json.dumps(phase3a, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    ).hexdigest()
    if phase3a_sha != EXPECTED["phase3a_result_sha256"]:
        raise RuntimeError(f"Phase3A Currier authority SHA changed: {phase3a_sha}")
    if not phase3a.get("gate_pass"):
        raise RuntimeError("Phase3A Currier Gate no longer passes")
    if phase3a.get("fold_identity_sha256") != EXPECTED["fold_sha256"]:
        raise RuntimeError("Phase3A fold authority changed")

    return gate151, gate151_sha, phase3a, phase3a_sha


def physical_currier_map(phase3a: dict, frozen_fold_leaves: set[int]) -> tuple[dict[int, str], dict]:
    classes = phase3a["leaf_classes"]
    a = set(map(int, classes["A_ONLY"]))
    b = set(map(int, classes["B_ONLY"]))
    mixed = set(map(int, classes["MIXED_AB"]))
    unknown = set(map(int, classes["UNKNOWN_OTHER_ONLY_OR_PRESENT"]))
    if a & b or a & mixed or b & mixed:
        raise RuntimeError("Phase3A physical-leaf Currier classes overlap")
    if not a or not b:
        raise RuntimeError("degenerate Currier A/B physical-leaf support")
    if not (a | b).issubset(frozen_fold_leaves):
        raise RuntimeError("eligible Currier leaf outside frozen fold universe")

    mapping = {leaf: "A" for leaf in a}
    mapping.update({leaf: "B" for leaf in b})
    return mapping, {
        "A_ONLY": sorted(a),
        "B_ONLY": sorted(b),
        "MIXED_AB": sorted(mixed),
        "UNKNOWN_OTHER_ONLY_OR_PRESENT": sorted(unknown),
        "eligible_A_count": len(a),
        "eligible_B_count": len(b),
        "eligible_sets_disjoint": True,
        "labels_derived_only_from_ZL3b_phase3a_authority": True,
        "labels_reused_unchanged_for_IT2a": True,
    }


def filter_regime(records: Sequence[dict], leaf_currier: Mapping[int, str], regime: str) -> tuple[dict, ...]:
    return tuple(r for r in records if leaf_currier.get(int(r["leaf"])) == regime)


def integer_edge_counts(records: Sequence[dict], heldout_fold: int) -> tuple[dict[str, Counter], set[int], dict]:
    train = [r for r in records if int(r["fold"]) != heldout_fold]
    body = [r for r in train if not bool(r["is_run_start"])]
    by_context: dict[str, Counter] = defaultdict(Counter)
    for r in body:
        ctx = r["previous_terminal_atom"]
        outcome = r["first_atom"]
        if ctx is None:
            raise RuntimeError("training BODY event missing previous terminal")
        by_context[str(ctx)][str(outcome)] += 1
    leaves = {int(r["leaf"]) for r in train}
    if not body or not by_context:
        raise RuntimeError(f"degenerate Currier training support in fold {heldout_fold}")
    total = int(sum(sum(c.values()) for c in by_context.values()))
    if total != len(body):
        raise RuntimeError("integer edge-count mass mismatch")
    sparse = [
        [ctx, outcome, int(count)]
        for ctx in sorted(by_context)
        for outcome, count in sorted(by_context[ctx].items())
        if count
    ]
    return by_context, leaves, {
        "training_clean_tokens": len(train),
        "training_run_body_tokens": len(body),
        "training_leaf_count": len(leaves),
        "n_previous_terminal_contexts": len(by_context),
        "n_positive_context_outcome_pairs": len(sparse),
        "integer_table_sha256": sha256_obj(sparse),
    }


def reading_balanced_counts(z_counts: Mapping[str, Counter], i_counts: Mapping[str, Counter]) -> dict[str, dict[str, Fraction]]:
    out: dict[str, dict[str, Fraction]] = {}
    contexts = sorted(set(z_counts) | set(i_counts))
    for ctx in contexts:
        row: dict[str, Fraction] = {}
        outcomes = sorted(set(z_counts.get(ctx, Counter())) | set(i_counts.get(ctx, Counter())))
        for outcome in outcomes:
            value = Fraction(int(z_counts.get(ctx, Counter()).get(outcome, 0)), 2) + Fraction(
                int(i_counts.get(ctx, Counter()).get(outcome, 0)), 2
            )
            if value > 0:
                row[outcome] = value
        if row:
            out[ctx] = row
    return out


def row_mass(table: Mapping[str, Mapping[str, Fraction]], ctx: str) -> Fraction:
    return sum(table.get(ctx, {}).values(), Fraction(0, 1))


def rational_sparse(table: Mapping[str, Mapping[str, Fraction]]) -> list[list[object]]:
    return [
        [ctx, outcome, value.numerator, value.denominator]
        for ctx in sorted(table)
        for outcome, value in sorted(table[ctx].items())
        if value > 0
    ]


def support_match(a: Mapping[str, Mapping[str, Fraction]], b: Mapping[str, Mapping[str, Fraction]]):
    retained = [ctx for ctx in sorted(set(a) & set(b)) if row_mass(a, ctx) > 0 and row_mass(b, ctx) > 0]
    if len(retained) < 2:
        raise RuntimeError("fewer than two shared Currier previous-terminal contexts")

    matched: dict[str, dict[str, dict[str, Fraction]]] = {"A": {}, "B": {}}
    context_rows = []
    for ctx in retained:
        ma = row_mass(a, ctx)
        mb = row_mass(b, ctx)
        m = min(ma, mb)
        if m <= 0:
            raise RuntimeError("retained context has nonpositive match mass")
        matched["A"][ctx] = {outcome: value * m / ma for outcome, value in a[ctx].items()}
        matched["B"][ctx] = {outcome: value * m / mb for outcome, value in b[ctx].items()}
        out_a = row_mass(matched["A"], ctx)
        out_b = row_mass(matched["B"], ctx)
        if out_a != m or out_b != m or out_a != out_b:
            raise RuntimeError("exact context-by-context A/B matched mass equality failed")
        context_rows.append(
            {
                "context": ctx,
                "A_unmatched_mass": [ma.numerator, ma.denominator],
                "B_unmatched_mass": [mb.numerator, mb.denominator],
                "matched_mass": [m.numerator, m.denominator],
                "A_scale": [(m / ma).numerator, (m / ma).denominator],
                "B_scale": [(m / mb).numerator, (m / mb).denominator],
            }
        )

    sparse_a = rational_sparse(matched["A"])
    sparse_b = rational_sparse(matched["B"])
    total_match = sum((row_mass(matched["A"], ctx) for ctx in retained), Fraction(0, 1))
    return matched, {
        "retained_previous_terminal_contexts": retained,
        "n_retained_previous_terminal_contexts": len(retained),
        "context_mass_audit": context_rows,
        "total_matched_effective_mass": [total_match.numerator, total_match.denominator],
        "A_matched_sparse_rational_table_sha256": sha256_obj(sparse_a),
        "B_matched_sparse_rational_table_sha256": sha256_obj(sparse_b),
        "A_positive_context_outcome_cells": len(sparse_a),
        "B_positive_context_outcome_cells": len(sparse_b),
        "A_matched_sparse_rational_counts": sparse_a,
        "B_matched_sparse_rational_counts": sparse_b,
        "exact_A_B_context_mass_equality": True,
        "outcome_selected_subsampling": False,
    }


def target_support(records: Sequence[dict], heldout_fold: int, retained_contexts: set[str]) -> dict:
    test = [r for r in records if int(r["fold"]) == heldout_fold]
    primary = [r for r in test if bool(r["slotparser_accepted"])]
    body = [r for r in primary if not bool(r["is_run_start"])]
    supported = sum(str(r["previous_terminal_atom"]) in retained_contexts for r in body)
    unsupported = len(body) - supported
    if len(body) < EXPECTED["min_primary_body"]:
        raise RuntimeError(f"target primary BODY support below 300 in fold {heldout_fold}: {len(body)}")
    if supported < EXPECTED["min_matched_context_supported_primary_body"]:
        raise RuntimeError(
            f"matched-context-supported target BODY support below 300 in fold {heldout_fold}: {supported}"
        )
    return {
        "target_clean_tokens": len(test),
        "target_primary_targets": len(primary),
        "target_primary_run_body_targets": len(body),
        "matched_context_supported_primary_run_body_targets": int(supported),
        "matched_context_unsupported_primary_run_body_targets": int(unsupported),
        "matched_context_coverage_fraction": float(supported / len(body)) if body else None,
        "heldout_current_first_atom_used_for_context_selection": False,
    }


def synthetic_test() -> dict:
    z_a = {"a": Counter({"b": 4, "c": 2}), "d": Counter({"a": 2})}
    i_a = {"a": Counter({"b": 2, "c": 2}), "d": Counter({"a": 4})}
    z_b = {"a": Counter({"b": 8, "c": 4}), "d": Counter({"a": 1})}
    i_b = {"a": Counter({"b": 4, "c": 2}), "d": Counter({"a": 3})}
    a = reading_balanced_counts(z_a, i_a)
    b = reading_balanced_counts(z_b, i_b)
    matched, summary = support_match(a, b)
    if summary["retained_previous_terminal_contexts"] != ["a", "d"]:
        raise AssertionError("synthetic retained contexts changed")
    for ctx in summary["retained_previous_terminal_contexts"]:
        if row_mass(matched["A"], ctx) != row_mass(matched["B"], ctx):
            raise AssertionError("synthetic exact mass match failed")

    alpha = Fraction(EXPECTED["alpha_num"], EXPECTED["alpha_den"])
    counts = matched["A"]["a"]
    total = row_mass(matched["A"], "a")
    p_seen = (counts.get("b", Fraction(0, 1)) + alpha) / (total + alpha * EXPECTED["V"])
    p_end = alpha / (total + alpha * EXPECTED["V"])
    if not (0 < p_end < p_seen < 1):
        raise AssertionError("synthetic additive smoothing failed")
    if not (math.isfinite(float(p_seen)) and math.isfinite(float(p_end))):
        raise AssertionError("synthetic smoothed probability non-finite")
    return {
        "ok": True,
        "uses_real_target_data": False,
        "reading_weights": {"ZL3b": [1, 2], "IT2a": [1, 2]},
        "context_matching": "exact Fraction arithmetic",
        "alpha": [1, 100],
        "V": EXPECTED["V"],
        "seen_probability_finite": True,
        "END_probability_finite": True,
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    gate151, gate151_sha, phase3a, phase3a_sha = verify_entry_authority(zl_path, it_path)

    leaf_fold, fold_identity, fold_sha = G151.G148.G145.fold_authority(zl_path)
    if fold_sha != EXPECTED["fold_sha256"]:
        raise RuntimeError("common-EVA physical-leaf fold authority changed")
    frozen_fold_leaves = set(map(int, leaf_fold))
    leaf_currier, currier_classes = physical_currier_map(phase3a, frozen_fold_leaves)

    parser = G151.G148.G145.E.SlotParser()
    G151.G148.G145.E.validate_parser(parser)
    _zs, zl_lines = G151.G148.G145.source_identity(zl_path, "ZL3b")
    _is, it_lines = G151.G148.G145.source_identity(it_path, "IT2a")
    all_records = {
        "ZL3b": G151.G148.clean_events(zl_lines, leaf_fold, parser),
        "IT2a": G151.G148.clean_events(it_lines, leaf_fold, parser),
    }
    records = {
        reading: {
            regime: filter_regime(all_records[reading], leaf_currier, regime)
            for regime in LABELS
        }
        for reading in READINGS
    }

    observed_clean_leaves = {
        reading: {
            regime: sorted({int(r["leaf"]) for r in records[reading][regime]})
            for regime in LABELS
        }
        for reading in READINGS
    }

    outer = []
    for f in range(EXPECTED["n_folds"]):
        heldout_leaves = set(map(int, fold_identity[f]))
        training = {reading: {} for reading in READINGS}
        counts = {reading: {} for reading in READINGS}
        train_leaves = {reading: {} for reading in READINGS}

        for reading in READINGS:
            for regime in LABELS:
                c, leaves, summary = integer_edge_counts(records[reading][regime], f)
                overlap = sorted(leaves & heldout_leaves)
                if overlap:
                    raise RuntimeError(f"{reading}/{regime} fold {f} training leaf leakage: {overlap}")
                counts[reading][regime] = c
                train_leaves[reading][regime] = leaves
                training[reading][regime] = {**summary, "training_heldout_leaf_overlap": overlap}

        balanced = {
            regime: reading_balanced_counts(counts["ZL3b"][regime], counts["IT2a"][regime])
            for regime in LABELS
        }
        matched, matched_summary = support_match(balanced["A"], balanced["B"])
        retained = set(matched_summary["retained_previous_terminal_contexts"])

        target = {
            reading: {
                regime: target_support(records[reading][regime], f, retained)
                for regime in LABELS
            }
            for reading in READINGS
        }

        # The held-out physical leaf cannot enter the matched table via either reading or regime.
        union_train = set().union(
            *(train_leaves[reading][regime] for reading in READINGS for regime in LABELS)
        )
        union_overlap = sorted(union_train & heldout_leaves)
        if union_overlap:
            raise RuntimeError(f"fold {f} consensus Currier training leakage: {union_overlap}")

        outer.append(
            {
                "outer_fold": f,
                "heldout_physical_leaves": sorted(heldout_leaves),
                "all_reading_regime_training_union_heldout_overlap": union_overlap,
                "training_support": training,
                "matched_currier_tables": matched_summary,
                "target_context_support": target,
            }
        )

    synthetic = synthetic_test()
    return {
        "schema": "issue155-common-eva-currier-gate0-v1",
        "issue": 155,
        "phase": "COMMON_EVA_SUPPORT_MATCHED_CURRIER_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED COMMON-EVA CURRIER SCORER",
        "scientific_currier_transport_metrics_computed": False,
        "entry_authority": {
            "issue151_gate_reproduced": True,
            "issue151_gate_result_sha256": gate151_sha,
            "issue151_gate_script_blob": EXPECTED["issue151_gate_script_blob"],
            "issue151_gate_provenance_blob": EXPECTED["issue151_gate_provenance_blob"],
            "issue151_scorer_blob": EXPECTED["issue151_scorer_blob"],
            "issue151_first_reveal_provenance_blob": EXPECTED["issue151_first_provenance_blob"],
            "issue151_declared_first_reveal_result_sha256": EXPECTED["issue151_first_result_sha256"],
            "issue151_merge": EXPECTED["issue151_merge"],
            "phase3a_currier_reproduced": True,
            "phase3a_currier_result_sha256": phase3a_sha,
            "phase3a_currier_script_blob": EXPECTED["phase3a_script_blob"],
            "fold_identity_sha256": fold_sha,
            "plan_blob_sha1": git_blob(PLAN_PATH),
        },
        "currier_physical_leaf_authority": currier_classes,
        "observed_clean_leaves_by_reading_and_reused_currier_label": observed_clean_leaves,
        "representation": gate151["representation"],
        "support_match_contract": {
            "reading_consensus": "0.5*C_ZL3b,R + 0.5*C_IT2a,R",
            "reading_weights_rational": {"ZL3b": [1, 2], "IT2a": [1, 2]},
            "retain_context_if_positive_in_both_currier_regimes": True,
            "matched_context_mass": "min(M_A(context), M_B(context))",
            "rescaling": "C_R_MATCH(context,outcome)=C_R(context,outcome)*m(context)/M_R(context)",
            "arithmetic": "exact Fraction for Gate0",
            "alpha_for_future_scorer": [1, 100],
            "V_for_future_scorer": EXPECTED["V"],
            "unsupported_target_context_future_rule": "empty exact-context additive distribution",
            "target_native_fallback": False,
            "primary_rho_mixture_calibration": False,
        },
        "outer": outer,
        "support_thresholds": {
            "min_target_primary_run_body": EXPECTED["min_primary_body"],
            "min_matched_context_supported_target_primary_run_body": EXPECTED[
                "min_matched_context_supported_primary_body"
            ],
        },
        "synthetic_test": synthetic,
        "firewall": {
            "scientific_currier_transport_metrics_computed": False,
            "real_target_transport_probability_computed": False,
            "real_target_transport_likelihood_computed": False,
            "transport_bits_per_token_computed": False,
            "G_transport_computed": False,
            "scientific_classification_computed": False,
            "heldout_current_first_atom_used_for_context_selection": False,
            "target_selected_atom_mapping": False,
            "target_selected_support_matching": False,
            "reading_weights_tuned": False,
            "context_match_rule_tuned": False,
            "k_alpha_smoothing_or_fallback_tuned": False,
            "primary_rho_mixture_selected": False,
            "hand_section_domain_conditioning": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
        },
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue155-common-eva-currier-gate0-v1",
        "issue": 155,
        "phase": "COMMON_EVA_SUPPORT_MATCHED_CURRIER_GATE0",
        "gate_pass": False,
        "gate_disposition": "INVALID COMMON-EVA CURRIER TRANSPORT — GATE0 FAILED",
        "scientific_currier_transport_metrics_computed": False,
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {"scientific_currier_transport_metrics_computed": False},
    }


def self_test() -> dict:
    x = synthetic_test()
    x.update(
        {
            "target_sources_loaded": False,
            "scientific_currier_transport_metrics_computed": False,
            "support_audit_only": True,
        }
    )
    return x


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
