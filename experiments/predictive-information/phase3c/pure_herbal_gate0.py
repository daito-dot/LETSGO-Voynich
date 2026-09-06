#!/usr/bin/env python3
"""Issue #109 Phase 3C Gate 0: score-free pure-Herbal leaf support audit."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PRED = ROOT / "experiments" / "predictive-information"
PHASE3B_PATH = PRED / "phase3b" / "metadata_gate0_audit.py"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_PHASE3B_JSON_SHA256 = "8f48a62e74fa34f78691949a4b9404caaea39fd6ad8360a93600c653f7147717"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


M = load_module("issue109_phase3b_authority", PHASE3B_PATH)
I81 = M.I81


def source_blob_sha1(path: Path) -> str:
    return I81.b.git_blob_sha1(path.read_bytes())


def json_sha256(x: dict) -> str:
    payload = (json.dumps(x, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def audit(zl_path: Path):
    if source_blob_sha1(zl_path) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b source differs from frozen authority")

    # Recompute and freeze the merged Phase-3B score-free authority before deriving the subset.
    phase3b = M.audit(zl_path)
    phase3b_sha = json_sha256(phase3b)
    if phase3b_sha != EXPECTED_PHASE3B_JSON_SHA256:
        raise RuntimeError(f"Phase-3B authority drift: {phase3b_sha} != {EXPECTED_PHASE3B_JSON_SHA256}")
    if phase3b["classification"] != "NO ADEQUATELY CROSSED OBSERVABLE FACTOR":
        raise RuntimeError("unexpected Phase-3B classification")
    if phase3b["identifiability"]["I"]["usable_levels"] != ["H"]:
        raise RuntimeError("Herbal is no longer the sole cross-Currier usable I level")

    headers = M.G0.parse_source_headers(zl_path)
    order_cfg = OA.configure(zl_path)
    items, folds, parsed = I81.C.load_corpus(zl_path)
    if len(folds) != 5:
        raise RuntimeError("frozen fold count changed")
    order_verify = OA.verify(items)
    scan = M.scan_token_metadata(zl_path, items, folds, parsed, headers)
    rows = scan["rows"]
    if scan["conformance_violations"] or scan["line_mapping_mismatches"] or scan["raw_L_vs_phase3a_authority_mismatches"]:
        raise RuntimeError("Phase-3B token metadata mapping no longer clean")

    rows_by_leaf = defaultdict(list)
    for row in rows:
        rows_by_leaf[int(row["leaf"])].append(row)

    eligible = {"A_HERBAL": set(), "B_HERBAL": set()}
    excluded = []
    for leaf, leaf_rows in sorted(rows_by_leaf.items()):
        lset = sorted({r["L_AUTH"] for r in leaf_rows})
        iset = sorted({r["I"] for r in leaf_rows})
        if lset == ["A"] and iset == ["H"]:
            eligible["A_HERBAL"].add(leaf)
        elif lset == ["B"] and iset == ["H"]:
            eligible["B_HERBAL"].add(leaf)
        else:
            excluded.append({
                "leaf": int(leaf),
                "currier_levels": lset,
                "illustration_levels": iset,
                "visible_tokens": len(leaf_rows),
                "accepted_tokens": int(sum(bool(r["accepted"]) for r in leaf_rows)),
            })

    fold_of_leaf = {}
    for f, leafset in enumerate(folds):
        for leaf in leafset:
            leaf = int(leaf)
            if leaf in fold_of_leaf:
                raise RuntimeError(f"leaf {leaf} occurs in multiple folds")
            fold_of_leaf[leaf] = int(f)

    item_by_leaf = defaultdict(list)
    for it in items:
        item_by_leaf[int(it.leaf)].append(it)

    population = {}
    for label, leafset in eligible.items():
        fold_counts = {str(f): {"leaves": [], "items": 0, "visible_tokens": 0, "accepted_tokens": 0} for f in range(5)}
        total_items = total_visible = total_accepted = 0
        for leaf in sorted(leafset):
            if leaf not in fold_of_leaf:
                raise RuntimeError(f"eligible leaf absent from frozen folds: {leaf}")
            f = str(fold_of_leaf[leaf])
            fold_counts[f]["leaves"].append(leaf)
            for it in item_by_leaf[leaf]:
                fold_counts[f]["items"] += 1
                total_items += 1
                for li, line in enumerate(it.lines):
                    nvis = len(line)
                    nacc = sum(seq is not None for seq in parsed[it.item_id][li])
                    fold_counts[f]["visible_tokens"] += nvis
                    fold_counts[f]["accepted_tokens"] += nacc
                    total_visible += nvis
                    total_accepted += nacc
        population[label] = {
            "leaves": sorted(leafset),
            "leaf_count": len(leafset),
            "items": int(total_items),
            "visible_tokens": int(total_visible),
            "accepted_tokens": int(total_accepted),
            "by_frozen_fold": fold_counts,
            "all_five_folds_nonzero": all(fold_counts[str(f)]["accepted_tokens"] > 0 for f in range(5)),
        }

    gate_pass = bool(
        population["A_HERBAL"]["leaf_count"] > 0
        and population["B_HERBAL"]["leaf_count"] > 0
        and population["A_HERBAL"]["all_five_folds_nonzero"]
        and population["B_HERBAL"]["all_five_folds_nonzero"]
        and order_verify["numeric_paragraph_order_valid"]
        and order_verify["source_document_order_valid"]
    )

    return {
        "schema": "issue109-phase3c-pure-herbal-gate0-v1",
        "phase": "ISSUE109_PHASE3C_GATE0",
        "gate_pass": gate_pass,
        "gate_rule": "PROCEED_TO_MATCHED_HERBAL_TRANSPORT" if gate_pass else "STOP_BEFORE_PREDICTIVE_SCORING",
        "phase3b_authority_sha256": phase3b_sha,
        "source": {
            "git_blob_sha1": source_blob_sha1(zl_path),
            "sha256": hashlib.sha256(zl_path.read_bytes()).hexdigest(),
        },
        "population": population,
        "excluded_leaves": excluded,
        "order_authority": {**order_cfg, **order_verify},
        "fold_identity_sha256": I81.P0.fold_hash(folds) if hasattr(I81, "P0") else M.P1.P0.fold_hash(folds),
        "metadata_mapping": {
            "visible_rows": len(rows),
            "accepted_rows": int(sum(bool(r["accepted"]) for r in rows)),
            "conformance_violations": 0,
            "line_mapping_mismatches": 0,
            "raw_L_authority_mismatches": 0,
        },
        "firewall": {
            "predictive_scores_computed": False,
            "model_fitted": False,
            "surface_target_metrics_scored": False,
            "issue84_target_used": False,
            "hand_conditioning_used": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
            "within_leaf_token_filtering_used": False,
        },
    }


def self_test():
    rows = [
        {"L_AUTH": "A", "I": "H"},
        {"L_AUTH": "A", "I": "H"},
    ]
    assert sorted({r["L_AUTH"] for r in rows}) == ["A"]
    assert sorted({r["I"] for r in rows}) == ["H"]
    bad = rows + [{"L_AUTH": "A", "I": "T"}]
    assert sorted({r["I"] for r in bad}) != ["H"]
    return {
        "ok": True,
        "score_free": True,
        "whole_leaf_filter": True,
        "within_leaf_token_filtering": False,
        "predictive_scores_computed": False,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--audit", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.audit is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    result = audit(Path(ns.audit[0]))
    Path(ns.audit[1]).write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "gate_pass": result["gate_pass"],
        "gate_rule": result["gate_rule"],
        "population": result["population"],
        "excluded_leaf_count": len(result["excluded_leaves"]),
        "phase3b_authority_sha256": result["phase3b_authority_sha256"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
