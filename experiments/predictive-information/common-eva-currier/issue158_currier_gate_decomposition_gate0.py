#!/usr/bin/env python3
"""Issue #158 Gate0: score-free Currier-gate decomposition audit.

Reproduce Issue #155 authority and exact rational A/B matched tables, then build
the frozen regime-neutral 0.5/0.5 pooled table. No real-target pooled-table
probability, likelihood, bits/token, G_pool, G_Currier, or classification is
computed here.
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

import issue155_common_eva_currier_gate0 as G155  # noqa: E402

PLAN_PATH = CURRIER_DIR / "ISSUE158_CURRIER_GATE_DECOMPOSITION_PLAN.md"
ISSUE155_GATE_PROVENANCE_PATH = CURRIER_DIR / "ISSUE155_GATE0_PROVENANCE.md"
ISSUE155_SCORER_PATH = CURRIER_DIR / "issue155_common_eva_currier_first_reveal.py"
ISSUE155_FIRST_PROVENANCE_PATH = CURRIER_DIR / "ISSUE155_FIRST_REVEAL_PROVENANCE.md"

EXPECTED = {
    "issue155_gate_result_sha256": "01f96038407975bc4d7a5944082a5bd2af9137f105edc33bd529cfccd33362f3",
    "issue155_gate_script_blob": "f5ab4fa31a92b3c303401da33611ffd5f77b402d",
    "issue155_gate_provenance_blob": "ba2f443b24237ed5ee0dce127b1a43ad082481c4",
    "issue155_scorer_blob": "0d57fdd32d298773b5ee38f97c9f104d29fa8377",
    "issue155_first_provenance_blob": "0e2fd1cbf35c2c64cfb5dcfa1529ed8dcc5292d9",
    "issue155_first_result_sha256": "041d7abe8f677da012ae143df9f4f372e88afc2e2b3cc7b359a58a4d7395b737",
    "issue155_merge": "6bd7c6fadb8fc590052496299c13da24f88585a2",
    "fold_sha256": "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b",
    "n_folds": 5,
    "min_primary_body": 300,
    "min_matched_supported_body": 300,
    "alpha_num": 1,
    "alpha_den": 100,
    "V": 32,
}

READINGS = ("ZL3b", "IT2a")
REGIMES = ("A", "B")


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G155.G151.G148.G145.git_blob_sha1(path.read_bytes())


def verify_entry_authority(zl_path: Path, it_path: Path) -> tuple[dict, str]:
    if git_blob(G155.HERE) != EXPECTED["issue155_gate_script_blob"]:
        raise RuntimeError("Issue155 Gate script blob changed")
    if git_blob(ISSUE155_GATE_PROVENANCE_PATH) != EXPECTED["issue155_gate_provenance_blob"]:
        raise RuntimeError("Issue155 Gate provenance blob changed")
    if git_blob(ISSUE155_SCORER_PATH) != EXPECTED["issue155_scorer_blob"]:
        raise RuntimeError("Issue155 scorer blob changed")
    if git_blob(ISSUE155_FIRST_PROVENANCE_PATH) != EXPECTED["issue155_first_provenance_blob"]:
        raise RuntimeError("Issue155 first-reveal provenance blob changed")
    if not PLAN_PATH.is_file():
        raise RuntimeError("Issue158 frozen plan missing")

    gate155 = G155.run_gate(zl_path, it_path)
    gate155_sha = sha256_obj(gate155)
    if gate155_sha != EXPECTED["issue155_gate_result_sha256"]:
        raise RuntimeError(f"Issue155 Gate result SHA changed: {gate155_sha}")
    if not gate155.get("gate_pass"):
        raise RuntimeError("Issue155 Gate no longer passes")
    if gate155.get("scientific_currier_transport_metrics_computed") is not False:
        raise RuntimeError("Issue155 Gate firewall changed")
    if gate155["entry_authority"]["fold_identity_sha256"] != EXPECTED["fold_sha256"]:
        raise RuntimeError("physical-leaf fold authority changed")
    return gate155, gate155_sha


def parse_rational_table(sparse: Sequence[Sequence[object]]) -> dict[str, dict[str, Fraction]]:
    out: dict[str, dict[str, Fraction]] = defaultdict(dict)
    for row in sparse:
        if len(row) != 4:
            raise RuntimeError("malformed rational table row")
        ctx, outcome, num, den = row
        value = Fraction(int(num), int(den))
        if value <= 0:
            raise RuntimeError("nonpositive rational table cell")
        out[str(ctx)][str(outcome)] = value
    return dict(out)


def row_mass(table: Mapping[str, Mapping[str, Fraction]], ctx: str) -> Fraction:
    return sum(table.get(ctx, {}).values(), Fraction(0, 1))


def rational_sparse(table: Mapping[str, Mapping[str, Fraction]]) -> list[list[object]]:
    return [
        [ctx, outcome, value.numerator, value.denominator]
        for ctx in sorted(table)
        for outcome, value in sorted(table[ctx].items())
        if value > 0
    ]


def pool_tables(a: Mapping[str, Mapping[str, Fraction]], b: Mapping[str, Mapping[str, Fraction]]):
    if set(a) != set(b):
        raise RuntimeError("Issue155 matched A/B context sets differ")
    pool: dict[str, dict[str, Fraction]] = {}
    audit = []
    for ctx in sorted(a):
        ma = row_mass(a, ctx)
        mb = row_mass(b, ctx)
        if ma != mb or ma <= 0:
            raise RuntimeError("Issue155 matched A/B context mass equality failed")
        row: dict[str, Fraction] = {}
        for outcome in sorted(set(a[ctx]) | set(b[ctx])):
            value = Fraction(1, 2) * a[ctx].get(outcome, Fraction(0, 1)) + Fraction(
                1, 2
            ) * b[ctx].get(outcome, Fraction(0, 1))
            if value > 0:
                row[outcome] = value
        pool[ctx] = row
        mp = row_mass(pool, ctx)
        if mp != ma or mp != mb:
            raise RuntimeError("pooled context effective mass changed")
        audit.append(
            {
                "context": ctx,
                "A_mass": [ma.numerator, ma.denominator],
                "B_mass": [mb.numerator, mb.denominator],
                "POOL_mass": [mp.numerator, mp.denominator],
                "exact_equal_mass": True,
            }
        )
    sparse = rational_sparse(pool)
    return pool, {
        "n_contexts": len(pool),
        "n_positive_context_outcome_cells": len(sparse),
        "context_mass_audit": audit,
        "pooled_sparse_rational_counts": sparse,
        "pooled_sparse_rational_table_sha256": sha256_obj(sparse),
        "weights": {"A": [1, 2], "B": [1, 2]},
        "exact_A_B_POOL_context_mass_equality": True,
    }


def synthetic_test() -> dict:
    a = {
        "a": {"b": Fraction(3, 1), "c": Fraction(1, 1)},
        "d": {"a": Fraction(2, 1)},
    }
    b = {
        "a": {"b": Fraction(1, 1), "c": Fraction(3, 1)},
        "d": {"a": Fraction(1, 1), "b": Fraction(1, 1)},
    }
    pool, summary = pool_tables(a, b)
    if pool["a"]["b"] != Fraction(2, 1) or pool["a"]["c"] != Fraction(2, 1):
        raise AssertionError("synthetic exact 0.5/0.5 pooling failed")
    if row_mass(pool, "a") != Fraction(4, 1) or row_mass(pool, "d") != Fraction(2, 1):
        raise AssertionError("synthetic pool mass failed")

    alpha = Fraction(EXPECTED["alpha_num"], EXPECTED["alpha_den"])
    total = row_mass(pool, "a")
    p_seen = (pool["a"]["b"] + alpha) / (total + alpha * EXPECTED["V"])
    p_end = alpha / (total + alpha * EXPECTED["V"])
    if not (0 < p_end < p_seen < 1):
        raise AssertionError("synthetic additive smoothing failed")
    if not (math.isfinite(float(p_seen)) and math.isfinite(float(p_end))):
        raise AssertionError("synthetic probability non-finite")
    return {
        "ok": True,
        "uses_real_target_data": False,
        "weights": {"A": [1, 2], "B": [1, 2]},
        "exact_mass_equality": summary["exact_A_B_POOL_context_mass_equality"],
        "alpha": [1, 100],
        "V": EXPECTED["V"],
        "seen_probability_finite": True,
        "END_probability_finite": True,
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    gate155, gate155_sha = verify_entry_authority(zl_path, it_path)
    rows = []
    for f, old in enumerate(gate155["outer"]):
        if int(old["outer_fold"]) != f:
            raise RuntimeError("Issue155 fold order changed")
        if old["all_reading_regime_training_union_heldout_overlap"] != []:
            raise RuntimeError("Issue155 physical-leaf leakage reappeared")
        m = old["matched_currier_tables"]
        a_sparse = m["A_matched_sparse_rational_counts"]
        b_sparse = m["B_matched_sparse_rational_counts"]
        if G155.sha256_obj(a_sparse) != m["A_matched_sparse_rational_table_sha256"]:
            raise RuntimeError(f"fold {f} A matched-table identity changed")
        if G155.sha256_obj(b_sparse) != m["B_matched_sparse_rational_table_sha256"]:
            raise RuntimeError(f"fold {f} B matched-table identity changed")
        a = parse_rational_table(a_sparse)
        b = parse_rational_table(b_sparse)
        _pool, pool_summary = pool_tables(a, b)
        if pool_summary["n_contexts"] != int(m["n_retained_previous_terminal_contexts"]):
            raise RuntimeError(f"fold {f} pooled context count changed")

        target_support = old["target_context_support"]
        for reading in READINGS:
            for regime in REGIMES:
                t = target_support[reading][regime]
                if int(t["target_primary_run_body_targets"]) < EXPECTED["min_primary_body"]:
                    raise RuntimeError(f"{reading}/{regime}/fold{f} target BODY support below threshold")
                if int(t["matched_context_supported_primary_run_body_targets"]) < EXPECTED[
                    "min_matched_supported_body"
                ]:
                    raise RuntimeError(f"{reading}/{regime}/fold{f} matched support below threshold")
                if t["heldout_current_first_atom_used_for_context_selection"] is not False:
                    raise RuntimeError("Issue155 target context support firewall changed")

        rows.append(
            {
                "outer_fold": f,
                "heldout_physical_leaves": old["heldout_physical_leaves"],
                "training_union_heldout_overlap": [],
                "A_matched_table_sha256": m["A_matched_sparse_rational_table_sha256"],
                "B_matched_table_sha256": m["B_matched_sparse_rational_table_sha256"],
                "pooled_table": pool_summary,
                "target_context_support": target_support,
            }
        )

    synthetic = synthetic_test()
    return {
        "schema": "issue158-currier-gate-decomposition-gate0-v1",
        "issue": 158,
        "phase": "CURRIER_GATE_DECOMPOSITION_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED CURRIER-GATE SCORER",
        "scientific_currier_gate_metrics_computed": False,
        "entry_authority": {
            "issue155_gate_reproduced": True,
            "issue155_gate_result_sha256": gate155_sha,
            "issue155_gate_script_blob": EXPECTED["issue155_gate_script_blob"],
            "issue155_gate_provenance_blob": EXPECTED["issue155_gate_provenance_blob"],
            "issue155_scorer_blob": EXPECTED["issue155_scorer_blob"],
            "issue155_first_reveal_provenance_blob": EXPECTED["issue155_first_provenance_blob"],
            "issue155_declared_first_reveal_result_sha256": EXPECTED["issue155_first_result_sha256"],
            "issue155_merge": EXPECTED["issue155_merge"],
            "fold_identity_sha256": EXPECTED["fold_sha256"],
            "plan_blob_sha1": git_blob(PLAN_PATH),
        },
        "pooled_table_contract": {
            "formula": "C_POOL = 0.5*C_A_MATCH + 0.5*C_B_MATCH",
            "weights_rational": {"A": [1, 2], "B": [1, 2]},
            "same_retained_contexts_as_issue155": True,
            "same_context_effective_mass_as_A_and_B": True,
            "arithmetic": "exact Fraction for Gate0",
            "alpha_for_future_scorer": [1, 100],
            "V_for_future_scorer": EXPECTED["V"],
            "unsupported_exact_context_future_rule": "empty additive distribution",
            "target_native_fallback": False,
            "rho_temperature_calibration_interpolation_mixture": False,
        },
        "outer": rows,
        "support_thresholds": {
            "min_target_primary_run_body": EXPECTED["min_primary_body"],
            "min_matched_context_supported_target_primary_run_body": EXPECTED[
                "min_matched_supported_body"
            ],
        },
        "synthetic_test": synthetic,
        "firewall": {
            "scientific_currier_gate_metrics_computed": False,
            "real_target_pooled_probability_computed": False,
            "real_target_pooled_likelihood_computed": False,
            "pooled_bits_per_token_computed": False,
            "G_pool_computed": False,
            "G_Currier_computed": False,
            "scientific_classification_computed": False,
            "heldout_current_first_atom_used_for_context_selection": False,
            "pooled_weights_tuned": False,
            "currier_labels_changed": False,
            "support_match_changed": False,
            "k_alpha_smoothing_or_fallback_tuned": False,
            "rho_or_mixture_fit": False,
            "hand_section_domain_conditioning": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
        },
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue158-currier-gate-decomposition-gate0-v1",
        "issue": 158,
        "phase": "CURRIER_GATE_DECOMPOSITION_GATE0",
        "gate_pass": False,
        "gate_disposition": "INVALID CURRIER-GATE DECOMPOSITION — GATE0 FAILED",
        "scientific_currier_gate_metrics_computed": False,
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {"scientific_currier_gate_metrics_computed": False},
    }


def self_test() -> dict:
    x = synthetic_test()
    x.update(
        {
            "target_sources_loaded": False,
            "scientific_currier_gate_metrics_computed": False,
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
