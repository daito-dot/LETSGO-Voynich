#!/usr/bin/env python3
"""Issue #109 / #88 Phase 3C matched-Herbal Currier A/B transport.

Reuses the frozen Phase-3A target-support mechanism family on whole-leaf pure
Herbal populations fixed by Phase-3C Gate 0. No model family or grid changes.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PRED = ROOT / "experiments" / "predictive-information"
PHASE3A_PATH = PRED / "phase3a" / "currier_transport.py"
GATE_PATH = HERE.parent / "pure_herbal_gate0.py"
PLAN_PATH = HERE.parent / "TRANSPORT_PLAN.md"
GATE_PROV_PATH = HERE.parent / "PURE_HERBAL_GATE0_PROVENANCE.md"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_GATE_JSON_SHA256 = "ec8c1dcb14f4450fe6e9f42d80ad00a60872719553c5ee46c153287723f705d8"
N_FOLDS = 5
LABELS = ("A", "B")
DIRECTIONS = (("A", "B"), ("B", "A"))
ALL_DOMAIN_REFERENCE = {
    "A": {"pi_LOCAL": 0.14, "alpha_ALL_PREV": 0.09},
    "B": {"pi_LOCAL": 0.16, "alpha_ALL_PREV": 0.19},
    "PREV_classification": "A->B ONLY",
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


T = load_module("issue109_phase3a_transport", PHASE3A_PATH)
G = load_module("issue109_pure_herbal_gate", GATE_PATH)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_sha256(x: dict) -> str:
    payload = (json.dumps(x, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def subset_by_leaves(items, leaves):
    leafset = {int(x) for x in leaves}
    out = [it for it in items if int(it.leaf) in leafset]
    seen = {int(it.leaf) for it in out}
    if seen != leafset:
        raise RuntimeError(f"eligible leaf population mismatch: missing={sorted(leafset-seen)} extra={sorted(seen-leafset)}")
    return out


def herbal_prev_interpretation(prev_classification: str) -> str:
    if prev_classification == "BIDIRECTIONAL TRANSPORT":
        return "HERBAL RESTORES BIDIRECTIONAL PREV TRANSPORT"
    if prev_classification in ("A->B ONLY", "B->A ONLY"):
        return "CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL"
    if prev_classification == "NO BIDIRECTIONAL TRANSPORT":
        return "HERBAL PREV NONTRANSPORT"
    return "SUPPORT INVALID"


def run(zl_path: Path):
    if G.source_blob_sha1(zl_path) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b source differs from frozen authority")

    gate = G.audit(zl_path)
    gate_sha = json_sha256(gate)
    if gate_sha != EXPECTED_GATE_JSON_SHA256:
        raise RuntimeError(f"pure-Herbal Gate authority drift: {gate_sha} != {EXPECTED_GATE_JSON_SHA256}")
    if not gate["gate_pass"]:
        raise RuntimeError("pure-Herbal Gate no longer passes")

    order_cfg = T.install_order(zl_path)
    items, folds, parsed = T.P2B.I.C.load_corpus(zl_path)
    if len(folds) != N_FOLDS:
        raise RuntimeError("frozen fold count changed")
    order_verify = T.OA.verify(items)
    parser = T.P2B.I.e.SlotParser()
    T.P2B.I.e.validate_parser(parser)

    strata = {
        "A": subset_by_leaves(items, gate["population"]["A_HERBAL"]["leaves"]),
        "B": subset_by_leaves(items, gate["population"]["B_HERBAL"]["leaves"]),
    }

    # Hard check: selected items remain whole-leaf subsets with the Gate token populations.
    for lab, gate_key in (("A", "A_HERBAL"), ("B", "B_HERBAL")):
        n_vis = sum(len(line) for it in strata[lab] for line in it.lines)
        n_acc = sum(
            seq is not None
            for it in strata[lab]
            for line in parsed[it.item_id]
            for seq in line
        )
        if n_vis != int(gate["population"][gate_key]["visible_tokens"]):
            raise RuntimeError(f"{lab} visible population drift")
        if n_acc != int(gate["population"][gate_key]["accepted_tokens"]):
            raise RuntimeError(f"{lab} accepted population drift")

    source_params = {
        lab: T.select_source_params(strata[lab], folds, parsed, parser, f"{lab}_HERBAL")
        for lab in LABELS
    }

    target_oracles = {lab: {} for lab in LABELS}
    for lab in LABELS:
        for f in range(N_FOLDS):
            target_oracles[lab][str(f)] = T.select_target_oracle(
                strata[lab], folds, parsed, parser, f, f"{lab}_HERBAL"
            )

    directions = {}
    for source, target in DIRECTIONS:
        key = f"{source}_to_{target}"
        rows = []
        for f in range(N_FOLDS):
            rows.append(T.score_mechanism_target(
                strata[target], folds, parsed, parser, f,
                source_params[source], target_oracles[target][str(f)],
            ))
        directions[key] = {
            "source": source,
            "target": target,
            "source_params": {
                "pi_LOCAL": source_params[source]["pi_LOCAL"],
                "alpha_ALL_PREV": source_params[source]["alpha_ALL_PREV"],
            },
            "outer": rows,
            "summary": T.summarize_direction(rows),
        }
        directions[key]["full_support_diagnostic"] = T.full_support_direction(
            strata[source], strata[target], folds, parsed, parser, source_params[source], rows
        )

    ab = directions["A_to_B"]["summary"]
    ba = directions["B_to_A"]["summary"]
    classifications = {
        "LOCAL40": T.component_classification(ab["G_local_transfer"], ba["G_local_transfer"]),
        "PREV_PARAS": T.component_classification(ab["G_prev_transfer"], ba["G_prev_transfer"]),
        "CORE": T.component_classification(ab["G_core_transfer"], ba["G_core_transfer"]),
    }
    domain_interpretation = herbal_prev_interpretation(classifications["PREV_PARAS"])

    # Target-oracle PREV gains are reported explicitly to distinguish architecture absence from scalar over/under-weighting.
    oracle_prev = {}
    for lab in LABELS:
        vals = []
        for f in range(N_FOLDS):
            row = T.score_mechanism_target(
                strata[lab], folds, parsed, parser, f,
                target_oracles[lab][str(f)], target_oracles[lab][str(f)],
            )
            vals.append(row["gains"]["G_prev_transfer"])
        oracle_prev[lab] = T.stability(vals)

    return T.P2B.B.strict_safe({
        "schema": "issue109-phase3c-matched-herbal-transport-v1",
        "phase": "ISSUE109_PHASE3C_MATCHED_HERBAL_TRANSPORT",
        "classification": classifications,
        "domain_matching_interpretation": domain_interpretation,
        "all_domain_reference": ALL_DOMAIN_REFERENCE,
        "source_parameters": source_params,
        "target_oracles": target_oracles,
        "target_oracle_prev_gain": oracle_prev,
        "directions": directions,
        "population": {
            "A_HERBAL": gate["population"]["A_HERBAL"],
            "B_HERBAL": gate["population"]["B_HERBAL"],
            "whole_leaf_filter": True,
            "within_leaf_token_filtering": False,
        },
        "authority": {
            "gate_json_sha256": gate_sha,
            "expected_gate_json_sha256": EXPECTED_GATE_JSON_SHA256,
            "order": {**order_cfg, **order_verify},
            "fold_identity_sha256": T.P2B.P1.P0.fold_hash(folds),
            "files": {
                "PURE_HERBAL_GATE0_PROVENANCE.md": sha256_file(GATE_PROV_PATH),
                "TRANSPORT_PLAN.md": sha256_file(PLAN_PATH),
                "herbal_transport.py": sha256_file(HERE),
            },
        },
        "firewall": {
            "prediction_only": True,
            "pure_herbal_population_fixed_before_prediction": True,
            "whole_leaf_filter_used": True,
            "within_leaf_token_filtering_used": False,
            "target_support_used_for_primary_emission_and_edit_index": True,
            "source_target_tokens_used_for_source_parameter_selection": False,
            "H_tau_window_reselected": False,
            "edit_relation_changed": False,
            "history_pool_changed": False,
            "folds_changed": False,
            "surface_target_metrics_scored": False,
            "issue84_target_used": False,
            "hand_conditioning_used": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
            "future_test_tokens_used": False,
        },
    })


def self_test():
    assert herbal_prev_interpretation("BIDIRECTIONAL TRANSPORT") == "HERBAL RESTORES BIDIRECTIONAL PREV TRANSPORT"
    assert herbal_prev_interpretation("A->B ONLY") == "CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL"
    assert herbal_prev_interpretation("B->A ONLY") == "CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL"
    assert herbal_prev_interpretation("NO BIDIRECTIONAL TRANSPORT") == "HERBAL PREV NONTRANSPORT"
    return {
        "ok": True,
        "frozen_gate_sha256": EXPECTED_GATE_JSON_SHA256,
        "all_domain_reference": ALL_DOMAIN_REFERENCE,
        "interpretation_rule": True,
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
        "domain_matching_interpretation": out["domain_matching_interpretation"],
        "source_parameters": {
            lab: {
                "pi_LOCAL": out["source_parameters"][lab]["pi_LOCAL"],
                "alpha_ALL_PREV": out["source_parameters"][lab]["alpha_ALL_PREV"],
            } for lab in LABELS
        },
        "target_oracle_prev_gain": out["target_oracle_prev_gain"],
        "directions": {
            k: {
                "summary": v["summary"],
                "oracle_params": [r["oracle"] for r in v["outer"]],
                "full_support_classification": v["full_support_diagnostic"]["classification"],
            } for k, v in out["directions"].items()
        },
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
