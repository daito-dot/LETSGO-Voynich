#!/usr/bin/env python3
"""Official Phase64A first-reveal entrypoint.

The underlying implementation in phase64a_inventory_autonomy.py was committed
before reveal. This entrypoint fixes only a pre-result authority-key typo in the
original main() check (`robust` -> the actual committed Phase63A key
`robust_to_heldout_vocabulary_removal`). No scientific method, metric, seed,
model, threshold, or source arm is changed.

Usage:
  python experiments/phase64/phase64a_science.py ZL3b-n.txt IT2a-n.txt
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import phase64a_inventory_autonomy as core


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt IT2a-n.txt", file=sys.stderr)
        return 2

    zl_path = Path(sys.argv[1]).resolve()
    it_path = Path(sys.argv[2]).resolve()

    phase62c_path = core.PHASE62 / "phase62c_c0_a1_results.json"
    phase62p_path = core.PHASE62 / "phase62p_h62p1_results.json"
    phase63a_path = core.PHASE63 / "phase63a_training_vocab_results.json"
    phase63b_path = core.PHASE63 / "phase63b_science_results.json"

    digests = {
        "phase62p": core.sha256_file(phase62p_path),
        "phase63a": core.sha256_file(phase63a_path),
        "phase63b": core.sha256_file(phase63b_path),
    }
    expected = {
        "phase62p": core.EXPECTED_H62P_RAW_SHA256,
        "phase63a": core.EXPECTED_PHASE63A_RAW_SHA256,
        "phase63b": core.EXPECTED_PHASE63B_RAW_SHA256,
    }
    if digests != expected:
        raise RuntimeError(f"committed prior-result authority digest mismatch: got={digests} expected={expected}")

    phase62c = json.loads(phase62c_path.read_text(encoding="utf-8"))
    phase62p = json.loads(phase62p_path.read_text(encoding="utf-8"))
    phase63a = json.loads(phase63a_path.read_text(encoding="utf-8"))
    phase63b = json.loads(phase63b_path.read_text(encoding="utf-8"))

    if phase62p["across_fold"]["prospective_profile_leader"] != "A1":
        raise RuntimeError("Phase62P authority no longer records A1 as prospective leader")
    if not phase63a["across_fold"]["robust_to_heldout_vocabulary_removal"]:
        raise RuntimeError("Phase63A authority no longer records A1-R1 robustness")
    if not phase63b["across_phase63B"]["strong_replication"]:
        raise RuntimeError("Phase63B authority no longer records strong replication")

    zl = core.run_zl(zl_path, phase62c, phase62p, phase63a)
    it = core.run_it(it_path, phase63b)
    zl_pass = bool(zl["across_fold"]["pass"])
    it_pass = bool(it["across_fold"]["pass"])
    classification, interpretation = core.classify(zl_pass, it_pass)

    out = {
        "phase": "64A",
        "hypothesis": "P64-A1-R2 empirical-inventory autonomy under frozen MG0",
        "scope_firewall": "only output-vocabulary source changes; no A2/C1/M0, no parameter retuning, no longer memory, no H62 change, no held-out morphology selection",
        "MG0_contract": {
            "orders": list(core.mg.ORDERS),
            "alpha": core.mg.ALPHA,
            "inner_folds": core.mg.INNER_FOLDS,
            "max_token_length": core.mg.MAX_TOKEN_LENGTH,
            "attempt_multiplier": core.mg.ATTEMPT_MULTIPLIER,
            "distinct_training_types_weighted_once": True,
            "synthetic_vocab_size_equals_training_vocab_size": True,
            "empirical_membership_query_during_sampling": False,
            "ZL_morphology_seed_formula": "6400000 + fold*1000 + replicate",
            "IT_morphology_seed_formula": "7400000 + fold*1000 + replicate",
        },
        "prior_authority_raw_sha256": digests,
        "A1_frozen_parameters": {
            str(fi): {"entry_strength": vals[0], "local_family_p": vals[1]}
            for fi, vals in core.c.A1_PARAMS.items()
        },
        "replicates_per_fold": core.A1_REPS,
        "H62P1_null_reps": core.p.NULL_REPS,
        "ZL_primary": zl,
        "IT_independent": it,
        "across_phase64A": {
            "ZL_primary_pass": zl_pass,
            "IT_independent_pass": it_pass,
            "classification": classification,
            "interpretation": interpretation,
        },
        "claim_limit": "inventory-autonomy only; no semantic emptiness, historical identity, family-level G dominance or decipherment",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
