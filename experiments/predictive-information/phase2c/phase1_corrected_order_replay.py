#!/usr/bin/env python3
"""Issue #98 corrected-order replay of the frozen Phase-1 predictive budget.

This wrapper changes causal item ordering only. It reuses the exact Phase-1 model
families, grids, nested selection, tie rules, parser, folds and scoring code.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PHASE1_PATH = ROOT / "experiments" / "predictive-information" / "phase1" / "phase1_predictive_budget.py"
CORRECTION_PATH = HERE.parent / "order_correction.py"
PROTOCOL_PATH = HERE.parent / "ORDER_CORRECTION_PROTOCOL.md"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P1 = load_module("issue98_phase1_frozen", PHASE1_PATH)
O = load_module("issue98_order_correction", CORRECTION_PATH)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install_corrected_order(zl_path: Path):
    authority = O.load_authority(zl_path)

    def corrected(items):
        return O.ordered(items, authority)

    # All sequential Phase-1 paths dispatch through Issue-81's shared `ordered`.
    # V2 fitting and fold membership remain unchanged.
    P1.I.ordered = corrected
    return authority


def corrected_regression_check(folds_out):
    """B0 is invariant and remains a hard gate; old B1 is comparison only."""
    errors = []
    old_b1_delta = {}
    for row in folds_out:
        f = int(row["fold"])
        ex = P1.PHASE0_EXPECTED[f]
        if abs(float(row["B0_bits_per_token"]) - float(ex["B0"])) > 1e-9:
            errors.append(f"fold{f} B0 {row['B0_bits_per_token']} != {ex['B0']}")
        old_b1_delta[str(f)] = float(row["B1"]["bits_per_token"] - ex["B1"])
    return {
        "pass": not errors,
        "errors": errors,
        "scope": "CORRECTED_ORDER_B0_INVARIANCE_ONLY",
        "historical_B1_delta_bits_per_token": old_b1_delta,
    }


def run(zl_path: Path):
    authority = install_corrected_order(zl_path)
    items, folds, parsed = P1.I.C.load_corpus(zl_path)
    order_validation = O.validate(items, authority)
    if not order_validation["pass"]:
        raise RuntimeError(f"corrected order authority validation failed: {order_validation}")

    old_fold_identity = P1.P0.fold_identity(folds)
    old_fold_hash = P1.P0.fold_hash(folds)
    n_visible = sum(len(line) for it in items for line in it.lines)
    n_accepted = sum(
        seq is not None
        for it in items
        for line in parsed[it.item_id]
        for seq in line
    )

    P1.regression_check = corrected_regression_check
    result = P1.run(zl_path)

    if result["folds"] != old_fold_identity or result["fold_identity_sha256"] != old_fold_hash:
        raise RuntimeError("fold identity changed under order correction")
    if sum(int(r["n_visible"]) for r in result["outer"]) != n_visible:
        raise RuntimeError("visible-token population changed under order correction")
    if sum(int(r["n_scored"]) for r in result["outer"]) != n_accepted:
        raise RuntimeError("parser-accepted population changed under order correction")

    b2_topology = [
        {
            "fold": int(r["fold"]),
            "H": r["B2"]["selected"]["H"],
            "tau": r["B2"]["selected"]["tau"],
            "pi": r["B2"]["selected"]["pi"],
        }
        for r in result["outer"]
    ]
    exact_historical_b2_topology = all(
        x["H"] == "ALL" and abs(float(x["tau"]) - 128.0) <= 1e-12 and abs(float(x["pi"]) - 0.30) <= 1e-12
        for x in b2_topology
    )

    result["schema"] = "issue98-phase1-corrected-order-replay-v1"
    result["phase"] = "ISSUE98_CORRECTED_PHASE1_REPLAY"
    result["order_correction"] = {
        "authority": "raw ZL3b page-header order + numeric paragraph suffix",
        "validation": order_validation,
        "n_visible_tokens": int(n_visible),
        "n_parser_accepted_tokens": int(n_accepted),
        "fold_identity_unchanged": True,
        "B0_invariance_gate_pass": bool(result["regression"]["pass"]),
        "historical_B2_topology_reproduced_all_folds": bool(exact_historical_b2_topology),
        "B2_topology": b2_topology,
        "next_gate": (
            "CORRECTED_PHASE2A_EXACT_TOPOLOGY_REPLAY_LICENSED"
            if exact_historical_b2_topology
            else "STOP_AND_FREEZE_NEW_CORRECTED_PHASE2A_REFERENCE_PROTOCOL"
        ),
    }
    result["authority_hashes"]["ORDER_CORRECTION_PROTOCOL.md"] = sha256_file(PROTOCOL_PATH)
    result["authority_hashes"]["order_correction.py"] = sha256_file(CORRECTION_PATH)
    result["authority_hashes"]["phase1_corrected_order_replay.py"] = sha256_file(HERE)
    result["firewall"]["ordering_only_correction"] = True
    return result


def self_test():
    auth = O.OrderAuthority(
        source_docs=("f1r", "f1v2", "f1v1"),
        global_rank={"f1r": 0, "f1v2": 1, "f1v1": 2},
        by_leaf={1: ("f1r", "f1v2", "f1v1")},
    )
    items = [
        SimpleNamespace(item_id="f1r:p10", document="f1r", leaf=1),
        SimpleNamespace(item_id="f1v1:p1", document="f1v1", leaf=1),
        SimpleNamespace(item_id="f1r:p2", document="f1r", leaf=1),
        SimpleNamespace(item_id="f1v2:p1", document="f1v2", leaf=1),
        SimpleNamespace(item_id="f1r:p1", document="f1r", leaf=1),
    ]
    got = [x.item_id for x in O.ordered(items, auth)]
    expected = ["f1r:p1", "f1r:p2", "f1r:p10", "f1v2:p1", "f1v1:p1"]
    if got != expected:
        raise AssertionError((got, expected))
    v = O.validate(items, auth)
    if not v["pass"]:
        raise AssertionError(v)
    return {
        "ok": True,
        "ordering_only": True,
        "synthetic_numeric_paragraph_fix": True,
        "synthetic_raw_page_side_fix": True,
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
    result = run(Path(ns.run[0]))
    Path(ns.run[1]).write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": result["classification"],
        "mean_bits_per_token": result["summaries"]["mean_bits_per_token"],
        "G_local": result["summaries"]["G_local"],
        "Delta_long": result["summaries"]["Delta_long"],
        "Delta_state": result["summaries"]["Delta_state"],
        "Delta_flex": result["summaries"]["Delta_flex"],
        "decision_inputs": result["decision_inputs"],
        "order_correction": result["order_correction"],
        "regression": result["regression"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
