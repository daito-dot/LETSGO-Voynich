#!/usr/bin/env python3
"""Issue #100 C1: rerun the frozen Phase-1 model family under source order."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PRED = ROOT / "experiments" / "predictive-information"
PHASE1_PATH = PRED / "phase1" / "phase1_predictive_budget.py"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402


def load_phase1():
    spec = importlib.util.spec_from_file_location("issue100_phase1_base", PHASE1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase-1 authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


P1 = load_phase1()

LEGACY_MEANS = {
    "B0": 9.7089061017,
    "B1": 9.5961811202,
    "B2": 9.5492540389,
    "B3": 9.5203245471,
}


def run(zl_path: Path):
    if P1.I.b.git_blob_sha1(zl_path.read_bytes()) != P1.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b source differs from frozen authority")
    order_config = OA.configure(zl_path)
    vitems, folds, parsed = P1.I.C.load_corpus(zl_path)
    order_verify = OA.verify(vitems)
    P1.I.ordered = OA.ordered

    if len(folds) != P1.N_FOLDS:
        raise RuntimeError("fold count mismatch")
    parser = P1.I.e.SlotParser()
    P1.I.e.validate_parser(parser)

    recency_selection = {}
    state_selection = {}
    byte_selection = {}
    for f in range(P1.N_FOLDS):
        recency_selection[str(f)] = P1.select_outer_recency(vitems, folds, parsed, f, parser)
        state_selection[str(f)] = P1.select_outer_state(
            vitems, folds, parsed, f, parser, recency_selection[str(f)]["B2"]
        )
        byte_selection[str(f)] = P1.select_outer_byte(vitems, folds, parsed, f)

    outer = [
        P1.outer_score(
            vitems, folds, parsed, f, parser,
            recency_selection[str(f)], state_selection[str(f)], byte_selection[str(f)]
        )
        for f in range(P1.N_FOLDS)
    ]

    # B0 is order-invariant and is the key support/probability regression. B1+
    # are intentionally allowed to change because their causal histories changed.
    b0_errors = []
    for row in outer:
        f = int(row["fold"])
        expected = float(P1.PHASE0_EXPECTED[f]["B0"])
        if abs(float(row["B0_bits_per_token"]) - expected) > 1e-9:
            b0_errors.append(f"fold{f}: {row['B0_bits_per_token']} != {expected}")
    if b0_errors:
        raise RuntimeError("order-invariant B0 regression failed: " + "; ".join(b0_errors))

    g_local = [r["B1"]["gain_vs_B0"] for r in outer]
    d_long = [r["B2"]["increment_vs_B1"] for r in outer]
    d_state = [r["B3"]["increment_vs_B2"] for r in outer]
    d_flex = [r["Delta_flex"] for r in outer]
    d_flex_over_local = [d_flex[i] - g_local[i] for i in range(P1.N_FOLDS)]
    summaries = {
        "G_local": P1.stability(g_local),
        "Delta_long": P1.stability(d_long),
        "Delta_state": P1.stability(d_state),
        "Delta_flex": P1.stability(d_flex),
        "Delta_flex_over_local": P1.stability(d_flex_over_local),
        "mean_bits_per_token": {
            "B0": float(np.mean([r["B0_bits_per_token"] for r in outer])),
            "B1": float(np.mean([r["B1"]["bits_per_token"] for r in outer])),
            "B2": float(np.mean([r["B2"]["bits_per_token"] for r in outer])),
            "B3": float(np.mean([r["B3"]["bits_per_token"] for r in outer])),
            "B4_RESET": float(np.mean([r["B4"]["RESET"]["accepted_bits_per_token"] for r in outer])),
            "B4_CONTINUOUS": float(np.mean([r["B4"]["CONTINUOUS"]["accepted_bits_per_token"] for r in outer])),
        },
    }
    comparable = all(
        r["B4"]["RESET"]["n_accepted"] == r["n_scored"]
        and r["B4"]["CONTINUOUS"]["n_accepted"] == r["n_scored"]
        and r["B4"]["RESET"]["n_all"] == r["n_visible"]
        and r["B4"]["CONTINUOUS"]["n_all"] == r["n_visible"]
        for r in outer
    )
    material = bool(
        summaries["Delta_long"]["pass"]
        or summaries["Delta_state"]["pass"]
        or summaries["Delta_flex_over_local"]["pass"]
    )
    if not comparable:
        classification = "MODEL-CLASS / SUPPORT INCONCLUSIVE"
    elif material:
        classification = "MATERIAL PREDICTIVE INFORMATION REMAINS"
    else:
        classification = "TESTED PREDICTIVE BUDGET NEAR-SATURATED BY SIMPLE CONTEXT"

    corrected_means = summaries["mean_bits_per_token"]
    old_vs_new = {
        k: {
            "legacy": float(v),
            "corrected": float(corrected_means[k]),
            "corrected_minus_legacy": float(corrected_means[k] - v),
        }
        for k, v in LEGACY_MEANS.items()
    }

    return P1.canonicalize({
        "schema": "issue100-c1-phase1-source-order-v1",
        "phase": "ISSUE100_C1_PHASE1_SOURCE_ORDER",
        "classification": classification,
        "source": {
            "git_blob_sha1": P1.I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": P1.EXPECTED_ZL3B_BLOB,
        },
        "order_authority": {**order_config, **order_verify},
        "folds": P1.P0.fold_identity(folds),
        "fold_identity_sha256": P1.P0.fold_hash(folds),
        "grids": {
            "B2_history": [P1.serialize_scale(x) for x in P1.H_GRID],
            "B2_tau": [P1.serialize_scale(x) for x in P1.TAU_GRID],
            "B2_pi": [float(x) for x in P1.PI_GRID],
            "B3_lambda": [float(x) for x in P1.LAMBDA_GRID],
            "B4_k": list(P1.BYTE_K_GRID),
            "B4_alpha": list(P1.BYTE_ALPHA_GRID),
        },
        "outer": outer,
        "recency_selection": recency_selection,
        "state_selection": state_selection,
        "byte_selection": byte_selection,
        "regression": {
            "B0_order_invariant_all_folds": True,
            "old_B1_forced": False,
            "fold_membership_changed": False,
        },
        "summaries": summaries,
        "B4_support_comparable": comparable,
        "decision_inputs": {
            "Delta_long_pass": summaries["Delta_long"]["pass"],
            "Delta_state_pass": summaries["Delta_state"]["pass"],
            "Delta_flex_over_local_pass": summaries["Delta_flex_over_local"]["pass"],
        },
        "legacy_comparison": old_vs_new,
        "firewall": {
            "S1_scored": False,
            "S2_scored": False,
            "H62_scored": False,
            "R1_scored": False,
            "issue84_target_used": False,
            "semantic_or_image_context_used": False,
            "future_test_tokens_used": False,
            "candidate_grid_extended": False,
        },
        "interpretation_boundary": {
            "latent_state_identified": False,
            "semantic_content_tested": False,
            "plaintext_recovered": False,
            "decipherment_established": False,
        },
    })


def self_test():
    base = P1.self_test()
    if not base.get("ok"):
        raise AssertionError("Phase-1 base self-test failed")
    ids = ["x:p1", "x:p10", "x:p2"]
    nums = [OA.paragraph_number(x) for x in ids]
    if nums != [1, 10, 2]:
        raise AssertionError("numeric paragraph parser failed")
    return {
        "ok": True,
        "base_phase1_self_test": True,
        "source_order_adapter": True,
        "surface_target_calls": 0,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.run is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    out = run(Path(ns.run[0]))
    Path(ns.run[1]).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": out["classification"],
        "order_authority": out["order_authority"],
        "mean_bits_per_token": out["summaries"]["mean_bits_per_token"],
        "G_local": out["summaries"]["G_local"],
        "Delta_long": out["summaries"]["Delta_long"],
        "Delta_state": out["summaries"]["Delta_state"],
        "Delta_flex_over_local": out["summaries"]["Delta_flex_over_local"],
        "B1_selected": {str(r['fold']): r['B1']['selected'] for r in out['outer']},
        "B2_selected": {str(r['fold']): r['B2']['selected'] for r in out['outer']},
        "B3_selected": {str(r['fold']): r['B3']['selected'] for r in out['outer']},
        "legacy_comparison": out["legacy_comparison"],
        "firewall": out["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
