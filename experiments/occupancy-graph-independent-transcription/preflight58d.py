#!/usr/bin/env python3
"""Issue #58D preflight.

Reproduces only frozen source/population support and archive identity. It does
not calculate any real IT2a pair Q, residual Z, residual energy, graph
similarity, sign agreement, or target p-value.

The Stage-A support file is verified byte-for-byte against the exact workflow
artifact before population reproduction. The frozen #58C reference is likewise
reconstructed and hash-verified from the repaired permanent transport copy;
the repair itself is documented under the #58C first-reveal archive and did not
change the original scientific bytes. This final pre-PR trigger exists only to
verify the exact branch head after the one-off repair workflow was removed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import phase58d_independent_residual as t  # noqa: E402


def synthetic_null_preservation():
    padded = np.asarray(
        [
            [[1,0,1,0,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0,0,0,0], [1,1,0,0,0,0,0,0,0,0,0,0]],
            [[0,0,0,1,0,0,0,0,0,0,0,0], [1,0,0,1,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]],
        ],
        dtype=np.uint8,
    )
    mask = np.asarray([[True, True, True], [True, True, False]], dtype=bool)
    d = {"padded": padded.copy(), "line_mask": mask}
    y = t.c.shuffled_flat(d, "Issue58D:Preflight:SyntheticNull:v1", 0)
    rebuilt = np.zeros_like(padded)
    rebuilt[mask] = y
    return bool(np.array_equal(padded.sum(axis=1), rebuilt.sum(axis=1)))


def main(it_path: Path, zl_path: Path):
    support = t.load_support_audit()
    d = t.build_it_dataset(it_path, zl_path, "min")
    pop = t.validate_population(d, support)
    zl_obj, _, zl_sha = t.load_zl_first_reveal()
    if not synthetic_null_preservation():
        raise RuntimeError("synthetic line x slot null preservation failed")

    out = {
        "phase": "Issue58D-preflight",
        "scope": "source_population_archive_identity_only_no_real_IT_pair_or_residual_scoring",
        "IT2a_sha256": d["source_identity"]["sha256"],
        "IT2a_git_blob_sha1": d["source_identity"]["git_blob_sha1"],
        "clean_tokens": d["visible"],
        "parsed_tokens": d["parsed"],
        "fold_accepted_tokens": pop["fold_accepted_tokens"],
        "accepted_group_fold": pop["accepted_group_fold"],
        "accepted_position_fold": pop["accepted_position_fold"],
        "physical_leaf_folds": d["folds"],
        "StageA_support_audit_sha256": t.SUPPORT_AUDIT_SHA256,
        "ZL58C_first_reveal_sha256": zl_sha,
        "ZL58C_frozen_classification": zl_obj["overall_classification"],
        "reference_namespace": t.REF_NS,
        "test_namespace": t.TEST_NS,
        "namespaces_distinct": t.REF_NS != t.TEST_NS != t.MAX_REF_NS,
        "synthetic_null_line_slot_marginals_preserved": True,
        "real_IT_pair_or_residual_metrics_computed": False,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {sys.argv[0]} IT2a-n.txt ZL3b-n.txt")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
