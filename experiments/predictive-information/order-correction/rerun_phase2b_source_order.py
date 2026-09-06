#!/usr/bin/env python3
"""Issue #100 C3: rerun Phase-2B boundary localization under source order."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PRED = ROOT / "experiments" / "predictive-information"
PHASE2B_PATH = PRED / "phase2b" / "phase2b_boundary_localization.py"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402

CORRECTED = {
    0: {"A0": 9.74133358571672, "A2": 9.703129096315228, "A5": 9.708707246008231, "local_pi": .21, "leaf_rho": .20},
    1: {"A0": 9.653977794584556, "A2": 9.611477410270004, "A5": 9.616829204374666, "local_pi": .21, "leaf_rho": .21},
    2: {"A0": 9.440059238964276, "A2": 9.381483548665923, "A5": 9.381175453451064, "local_pi": .21, "leaf_rho": .19},
    3: {"A0": 9.47837639594045, "A2": 9.415300895065752, "A5": 9.421851096308558, "local_pi": .21, "leaf_rho": .19},
    4: {"A0": 9.658088048445927, "A2": 9.619454947593933, "A5": 9.633401964439729, "local_pi": .22, "leaf_rho": .21},
}

LEGACY_MEANS = {
    "A0_LOCAL40": 9.5961811202,
    "LOCAL_PLUS_LINE_BAG": 9.5961811202,
    "LOCAL_PLUS_CURR_PARA_BAG": 9.5954732856,
    "LOCAL_PLUS_PREV_PARAS_BAG": 9.5439510434,
    "LOCAL_PLUS_LEAF_PREFIX_BAG": 9.5518752000,
    "LOCAL_PLUS_CURR_PARA_ORDERED128": 9.5955931630,
    "LOCAL_PLUS_CURR_PARA_RANDOM_LAG": 9.5955054726,
    "LOCAL_PLUS_PREV_PARAS_ORDERED128": 9.5488434809,
    "LOCAL_PLUS_PREV_PARAS_RANDOM_LAG": 9.5494508993,
    "A2_ORDERED128_STANDALONE": 9.5492540389,
}

LEGACY_CONTRASTS = {
    "G_line_inventory": 0.0,
    "G_within_para_inventory": 0.0007078346,
    "G_cross_para_inventory": 0.0435980855,
    "G_order_within_para": -0.0000876905,
    "G_order_cross_para": 0.0006074185,
}


def load_phase2b():
    spec = importlib.util.spec_from_file_location("issue100_phase2b_base", PHASE2B_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase-2B authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


P2B = load_phase2b()


def run(zl_path: Path):
    order_config = OA.configure(zl_path)
    vitems, _folds, _parsed = P2B.I.C.load_corpus(zl_path)
    order_verify = OA.verify(vitems)

    # Install corrected causal order throughout the imported graph used by
    # boundary_features and any shared helpers.
    P2B.I.ordered = OA.ordered
    P2B.A.I.ordered = OA.ordered
    P2B.B.I.ordered = OA.ordered
    P2B.P1.I.ordered = OA.ordered

    # C1/C2 are frozen. Replace only regression/reference constants. Corrected
    # B2 independently retained H=ALL,tau=128,pi=.30, so TAU_ORDER=128 remains
    # the correct no-search order-control authority for C3.
    P2B.EXPECTED.clear()
    P2B.EXPECTED.update({f: dict(v) for f, v in CORRECTED.items()})
    if abs(float(P2B.TAU_ORDER) - 128.0) > 1e-12:
        raise RuntimeError("Phase-2B tau authority changed unexpectedly")

    out = P2B.run(zl_path)
    means = out["summary"]["mean_bits_per_token"]
    contrasts = out["summary"]["contrasts"]
    out["schema"] = "issue100-c3-phase2b-source-order-v1"
    out["phase"] = "ISSUE100_C3_PHASE2B_SOURCE_ORDER"
    out["order_authority"] = {**order_config, **order_verify}
    out["c1_c2_reference"] = {
        "local": {str(f): {"pi": CORRECTED[f]["local_pi"], "bits_per_token": CORRECTED[f]["A0"]} for f in CORRECTED},
        "long": {str(f): {"H": "ALL", "tau": 128.0, "pi": .30, "bits_per_token": CORRECTED[f]["A2"]} for f in CORRECTED},
        "leaf_prefix_bag": {str(f): {"rho": CORRECTED[f]["leaf_rho"], "bits_per_token": CORRECTED[f]["A5"]} for f in CORRECTED},
        "same_long_architecture_as_legacy": True,
    }
    out["legacy_comparison"] = {
        "mean_bits_per_token": {
            key: {
                "legacy": float(old),
                "corrected": float(means[key]),
                "corrected_minus_legacy": float(means[key] - old),
            }
            for key, old in LEGACY_MEANS.items()
        },
        "contrasts": {
            key: {
                "legacy": float(old),
                "corrected": float(contrasts[key]["mean"]),
                "corrected_minus_legacy": float(contrasts[key]["mean"] - old),
                "corrected_positive_folds": int(contrasts[key]["positive_folds"]),
                "corrected_pass": bool(contrasts[key]["pass"]),
            }
            for key, old in LEGACY_CONTRASTS.items()
        },
    }
    out["correction_firewall"] = {
        "source_order_fixed_before_C3_selection": True,
        "C1_and_C2_frozen_before_C3": True,
        "old_outer_results_used_for_selection": False,
        "boundary_specific_tau_or_window_search": False,
        "candidate_or_grid_extended": False,
        "future_test_tokens_used": False,
        "surface_target_metrics_scored": False,
    }
    return P2B.B.strict_safe(out)


def self_test():
    base = P2B.self_test()
    if not base.get("ok"):
        raise AssertionError("Phase-2B base self-test failed")
    if abs(float(P2B.TAU_ORDER) - 128.0) > 1e-12:
        raise AssertionError("unexpected Phase-2B tau")
    return {
        "ok": True,
        "phase2b_base_self_test": True,
        "source_order_adapter": True,
        "C1_C2_same_long_architecture": True,
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
        "mean_bits_per_token": out["summary"]["mean_bits_per_token"],
        "primary_contrasts": {k: out["summary"]["contrasts"][k] for k in (
            "G_line_inventory", "G_within_para_inventory", "G_cross_para_inventory",
            "G_order_within_para", "G_order_cross_para")},
        "decision_inputs": out["summary"]["decision_inputs"],
        "selected": {str(r["fold"]): r["selected"] for r in out["outer"]},
        "legacy_comparison": out["legacy_comparison"],
        "correction_firewall": out["correction_firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
