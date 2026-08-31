#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from pathlib import Path

import issue26e_core as e

NULL_LATTICES = 100
SWAP_ATTEMPTS = 5000


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def policy_analysis(items, folds, parser, policy):
    universe = set().union(*folds); rows = []; null_by_fold = []
    for f, held in enumerate(folds):
        train = universe - held; vectors = {}
        for it in items:
            if it["leaf"] not in train: continue
            for line in it["lines"]:
                for tok in line:
                    p = parser.pick(tok, policy)
                    if p is not None and tok not in vectors: vectors[tok] = e.feature(p[1])
        km = e.KMeans20().fit(vectors)
        C, train_visible, train_parsed = e.count_matrix(items, train, parser, policy, km)
        H, held_visible, held_parsed = e.count_matrix(items, held, parser, policy, km)

        gmap = e.fit_mapping(C, e.GUIDO)
        gs = e.score_counts(H, held_visible, held_parsed, gmap, e.GUIDO)
        seen = set(); null_acc = []; null_train = []
        for j in range(NULL_LATTICES):
            M = e.swapped_lattice(f"Issue26E:{policy}:fold:{f}:null:{j}", seen, SWAP_ATTEMPTS)
            nm = e.fit_mapping(C, M); ns = e.score_counts(H, held_visible, held_parsed, nm, M)
            null_acc.append(ns["accuracy"]); null_train.append(nm["training_allowed"])
        p_fold = (1 + sum(x >= gs["accuracy"] - e.EPS for x in null_acc)) / (NULL_LATTICES + 1)
        med = statistics.median(null_acc)
        rows.append({
            "fold": f, "held_leaves": sorted(held),
            "training_unique_parsed_types": len(vectors),
            "training_visible_occurrences": train_visible,
            "training_parsed_occurrences": train_parsed,
            "training_occurrences": int(C.sum()),
            "guidonian_training_allowed": gmap["training_allowed"],
            "guidonian_mapping": gmap, "heldout": gs,
            "null_median_accuracy": med,
            "null_q95_accuracy": e.quantile(null_acc, .95),
            "guidonian_minus_null_median": gs["accuracy"] - med,
            "p_fold": p_fold,
            "null_training_allowed_median": statistics.median(null_train),
        })
        null_by_fold.append(null_acc)

    g = [r["heldout"]["accuracy"] for r in rows]; mean_g = statistics.mean(g)
    mean_n = [statistics.mean(null_by_fold[f][j] for f in range(5)) for j in range(NULL_LATTICES)]
    p_global = (1 + sum(x >= mean_g - e.EPS for x in mean_n)) / (NULL_LATTICES + 1)
    med_n = statistics.median(mean_n)
    return {
        "policy": policy, "folds": rows,
        "mean_parse_coverage": statistics.mean(r["heldout"]["parse_coverage"] for r in rows),
        "mean_guidonian_accuracy": mean_g,
        "paired_null_mean_median": med_n,
        "paired_null_mean_q95": e.quantile(mean_n, .95),
        "global_advantage": mean_g - med_n,
        "p_global": p_global,
        "fold_null_median_wins": sum(r["heldout"]["accuracy"] > r["null_median_accuracy"] + e.EPS for r in rows),
        "mean_null_accuracies": mean_n,
    }


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt", file=sys.stderr); return 2
    path = Path(sys.argv[1]).resolve(); data = path.read_bytes(); blob = e.git_blob_sha1(data)
    if blob != e.EXPECTED_ZL3B_BLOB: raise RuntimeError(f"ZL3b blob mismatch {blob}")

    parser = e.SlotParser(); validation = e.validate_parser(parser)
    items = e.parse_voynich(path); folds = e.physical_leaf_folds(items)
    if len(folds) != 5 or any(not x for x in folds): raise RuntimeError(f"bad folds: {folds}")

    primary = policy_analysis(items, folds, parser, "min")
    sensitivity = policy_analysis(items, folds, parser, "max")
    ppass = (primary["mean_parse_coverage"] >= .60 and primary["p_global"] <= .05
             and primary["fold_null_median_wins"] >= 4)
    robust = sensitivity["global_advantage"] > 0 and sensitivity["p_global"] <= .10
    if ppass and robust: verdict = "NARROW GUIDONIAN SLOT-COMPATIBILITY"
    elif ppass: verdict = "PRIMARY POSITIVE / NOT ROBUST TO MAX-PARSE SENSITIVITY"
    else: verdict = "NOT SUPPORTED"

    here = Path(__file__).resolve().parent
    out = {
        "experiment": "Issue26E Guidonian slot-lattice test", "issue": 26,
        "inputs": {
            "voynich_git_blob_sha1": e.EXPECTED_ZL3B_BLOB,
            "slot_provenance_sha256": sha256_file(here/"SLOT_PROVENANCE_E.md"),
            "plan_sha256": sha256_file(here/"PLAN_E.md"),
            "core_sha256": sha256_file(here/"issue26e_core.py"),
            "script_sha256": sha256_file(Path(__file__)),
            "null_lattices_per_fold": NULL_LATTICES,
            "swap_attempts_per_null_round": SWAP_ATTEMPTS,
        },
        "slot_parser_validation": validation,
        "guidonian_invariants": {
            "row_degrees": e.GUIDO.sum(1).astype(int).tolist(),
            "column_degrees": e.GUIDO.sum(0).astype(int).tolist(),
            "allowed_cells": int(e.GUIDO.sum()), "vox_order": list(e.VOX),
            "slot10_state_order": list(e.SLOT10_STATES),
        },
        "folds": [sorted(x) for x in folds], "primary_min": primary,
        "sensitivity_max": sensitivity,
        "decision_conditions": {
            "primary_parse_coverage_ge_0_60": primary["mean_parse_coverage"] >= .60,
            "primary_p_global_le_0_05": primary["p_global"] <= .05,
            "primary_wins_at_least_4_of_5": primary["fold_null_median_wins"] >= 4,
            "max_sensitivity_same_sign": sensitivity["global_advantage"] > 0,
            "max_sensitivity_p_global_le_0_10": sensitivity["p_global"] <= .10,
        },
        "frozen_classification": verdict,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True); print(); return 0


if __name__ == "__main__": raise SystemExit(main())
