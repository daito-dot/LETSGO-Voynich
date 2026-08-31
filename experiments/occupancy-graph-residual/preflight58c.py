#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
RESIDUAL_DIR = HERE.parent
STABILITY_DIR = HERE.parents[1] / "occupancy-graph-stability"
sys.path.insert(0, str(RESIDUAL_DIR))
sys.path.insert(0, str(STABILITY_DIR))
import phase58b_graph_stability as b
import phase58c_residual_graph as r

EXPECTED_ALL_FOLDS = [4430, 4810, 5516, 5447, 4868]


def main(path):
    if r.REFERENCE_NS == r.TEST_NS or r.REFERENCE_NS == r.MAX_REFERENCE_NS or r.TEST_NS == r.MAX_REFERENCE_NS:
        raise RuntimeError("null seed namespaces overlap")
    if r.N_REF != 1000 or r.N_TEST != 1000:
        raise RuntimeError("frozen null counts changed")
    if len(r.PAIRS) != 66:
        raise RuntimeError("pair count changed")

    parser = b.e.SlotParser()
    d = b.build_dataset(Path(path), parser, "min")
    support = b.validate_support(d)
    all_folds = [int(np.sum(d["token_folds"] == f)) for f in range(5)]
    if all_folds != EXPECTED_ALL_FOLDS:
        raise RuntimeError(f"ALL fold support mismatch: {all_folds}")

    # Population/null geometry only: verify exact line x slot marginals,
    # but do not calculate any real or null pair graph score.
    Y_ref = r.shuffled_flat(d, r.REFERENCE_NS, 0)
    Y_test = r.shuffled_flat(d, r.TEST_NS, 0)
    if Y_ref.shape != d["X"].shape or Y_test.shape != d["X"].shape:
        raise RuntimeError("null flat shape mismatch")
    if np.array_equal(Y_ref, Y_test):
        raise RuntimeError("reference/test null draws unexpectedly identical")

    # Frozen residual transform validation uses synthetic numbers only.
    refs = np.linspace(-1.0, 1.0, r.N_REF, dtype=float)[:, None]
    z0 = r.normal_score_array(np.asarray([0.0]), refs)
    tied = np.zeros((r.N_REF, 1), dtype=float)
    ztie = r.normal_score_array(np.asarray([0.0]), tied)
    if abs(float(z0[0])) >= 0.01 or abs(float(ztie[0])) >= 1e-12:
        raise RuntimeError("normal-score synthetic validation failed")

    out = {
        "scope": "preflight_only_no_real_or_null_pair_graph_scoring",
        "source_blob": d["source_blob"],
        "visible_tokens": d["visible"],
        "parsed_tokens": d["parsed"],
        "all_fold_parsed_tokens": all_folds,
        "group_support": support,
        "pair_count": len(r.PAIRS),
        "reference_namespace": r.REFERENCE_NS,
        "test_namespace": r.TEST_NS,
        "max_sensitivity_reference_namespace": r.MAX_REFERENCE_NS,
        "n_reference": r.N_REF,
        "n_test": r.N_TEST,
        "null_shapes": {"reference": list(Y_ref.shape), "test": list(Y_test.shape)},
        "normal_score_synthetic": {"center": float(z0[0]), "all_tied_center": float(ztie[0])},
    }
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} SOURCE")
    main(Path(sys.argv[1]))
