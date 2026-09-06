#!/usr/bin/env python3
"""Issue #100 C2: rerun Phase-2A source attribution under source order.

C1 independently reselected the same long-history architecture as legacy Phase 1
(H=ALL, tau=128, pi=.30), so the preregistered Phase-2A control family remains
algebraically applicable. Only the causal item order and corrected LOCAL40
per-fold parameters/reference code lengths are changed.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PRED = ROOT / "experiments" / "predictive-information"
PHASE2A_PATH = PRED / "phase2a" / "phase2a_amended.py"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402

CORRECTED = {
    0: {"A0": 9.74133358571672, "A2": 9.703129096315228, "local_pi": .21},
    1: {"A0": 9.653977794584556, "A2": 9.611477410270004, "local_pi": .21},
    2: {"A0": 9.440059238964276, "A2": 9.381483548665923, "local_pi": .21},
    3: {"A0": 9.47837639594045, "A2": 9.415300895065752, "local_pi": .21},
    4: {"A0": 9.658088048445927, "A2": 9.619454947593933, "local_pi": .22},
}

LEGACY = {
    "A0_LOCAL40": 9.5961811202,
    "A2_ORDERED128_FIXED": 9.5492540389,
    "A5_LOCAL_PLUS_PREFIX_CV": 9.5518752000,
    "A6_RANDOM_LAG_CV": 9.5690181087,
    "G_prefix_cond": 0.0443059201,
    "G_order_hybrid": 0.0026211611,
    "G_order_random_cv": 0.0197640698,
}


def load_phase2a():
    spec = importlib.util.spec_from_file_location("issue100_phase2a_base", PHASE2A_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase-2A amended authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


A = load_phase2a()


def run(zl_path: Path):
    order_config = OA.configure(zl_path)
    vitems, _folds, _parsed = A.I.C.load_corpus(zl_path)
    order_verify = OA.verify(vitems)

    # Install the versioned causal order across the shared imported module graph.
    A.I.ordered = OA.ordered
    A.B.I.ordered = OA.ordered
    A.P1.I.ordered = OA.ordered

    # Interface-only compatibility retained from the authoritative Phase-2A
    # runner. The base module defines mix_probs locally but references the same
    # helper through the imported Phase-1 namespace in score_outer.
    A.P1.mix_probs = A.B.mix_probs

    # C1 is now frozen. Replace only the regression/local-reference constants;
    # the long-history architecture remains H=ALL,tau=128,pi=.30 in 5/5 folds.
    A.B.PHASE1_EXPECTED.clear()
    A.B.PHASE1_EXPECTED.update({f: dict(v) for f, v in CORRECTED.items()})

    out = A.run(zl_path)
    means = out["summaries"]["mean_bits_per_token"]
    contrasts = out["summaries"]
    out["schema"] = "issue100-c2-phase2a-source-order-v1"
    out["phase"] = "ISSUE100_C2_PHASE2A_SOURCE_ORDER"
    out["order_authority"] = {**order_config, **order_verify}
    out["c1_reference"] = {
        "B1_local": {str(f): {"pi": CORRECTED[f]["local_pi"], "bits_per_token": CORRECTED[f]["A0"]} for f in CORRECTED},
        "B2_long": {str(f): {"H": "ALL", "tau": 128.0, "pi": .30, "bits_per_token": CORRECTED[f]["A2"]} for f in CORRECTED},
        "same_long_architecture_as_legacy": True,
    }
    out["legacy_comparison"] = {
        "mean_bits_per_token": {
            key: {
                "legacy": float(LEGACY[key]),
                "corrected": float(means[key]),
                "corrected_minus_legacy": float(means[key] - LEGACY[key]),
            }
            for key in ("A0_LOCAL40", "A2_ORDERED128_FIXED", "A5_LOCAL_PLUS_PREFIX_CV", "A6_RANDOM_LAG_CV")
        },
        "contrasts": {
            key: {
                "legacy": float(LEGACY[key]),
                "corrected": float(contrasts[key]["mean"]),
                "corrected_minus_legacy": float(contrasts[key]["mean"] - LEGACY[key]),
                "corrected_positive_folds": int(contrasts[key]["positive_folds"]),
                "corrected_pass": bool(contrasts[key]["pass"]),
            }
            for key in ("G_prefix_cond", "G_order_hybrid", "G_order_random_cv")
        },
    }
    out["correction_firewall"] = {
        "source_order_fixed_before_C2_selection": True,
        "C1_frozen_before_C2": True,
        "old_outer_results_used_for_selection": False,
        "candidate_or_grid_extended": False,
        "future_test_tokens_used": False,
        "surface_target_metrics_scored": False,
    }
    return A.B.strict_safe(out)


def self_test():
    base = A.self_test()
    if not base.get("ok"):
        raise AssertionError("Phase-2A amended self-test failed")
    if any(v["A2"] >= v["A0"] for v in CORRECTED.values()):
        raise AssertionError("corrected C1 long reference is not predictive")
    if A.P1 is A.B:
        raise AssertionError("unexpected module identity")
    return {
        "ok": True,
        "phase2a_base_self_test": True,
        "source_order_adapter": True,
        "C1_same_long_architecture": True,
        "interface_alias_installed_at_run": True,
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
        "mean_bits_per_token": out["summaries"]["mean_bits_per_token"],
        "G_prefix_cond": out["summaries"]["G_prefix_cond"],
        "G_order_hybrid": out["summaries"]["G_order_hybrid"],
        "G_order_random_cv": out["summaries"]["G_order_random_cv"],
        "A5_rho": {f:r["A5"]["selected_rho"] for f,r in out["amended_selection"].items()},
        "A6_pi": {f:r["A6"]["selected_pi"] for f,r in out["amended_selection"].items()},
        "legacy_comparison": out["legacy_comparison"],
        "correction_firewall": out["correction_firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
