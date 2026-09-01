#!/usr/bin/env python3
"""Aggregate exactly ten frozen Phase-F0 fold-family shards.

Usage:
    python phase75f0_shard_aggregate.py SHARD_DIR OUTPUT_JSON
"""
from __future__ import annotations

import glob
import json
import math
import sys
from pathlib import Path
from typing import Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75f0_stable_runner as stable  # noqa: E402

f0 = stable.f0
SHARD_PLAN = HERE / "F0_EXECUTION_SHARDING_PLAN.md"

M5_EQ_TOL = 1e-10


def close(a: float, b: float, tol: float = M5_EQ_TOL) -> bool:
    return bool(math.isfinite(float(a)) and math.isfinite(float(b)) and abs(float(a) - float(b)) <= tol)


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} SHARD_DIR OUTPUT_JSON")
    shard_dir = Path(argv[1]).resolve()
    out_path = Path(argv[2]).resolve()
    if not SHARD_PLAN.exists():
        raise RuntimeError("F0 sharding plan required")

    paths = sorted(Path(p) for p in glob.glob(str(shard_dir / "phase75f0_shard_fold*_G*.json")))
    if len(paths) != 10:
        raise RuntimeError(f"expected exactly 10 shard files, got {len(paths)}")
    shards = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    by_key = {}
    expected_source = None
    for s in shards:
        if s.get("schema") != "issue75-phaseF0-fold-family-shard-v1" or s.get("status") != "PHASE_F0_FOLD_FAMILY_SHARD_COMPLETE_TARGET_BLIND":
            raise RuntimeError("invalid shard schema/status")
        key = (int(s["fold"]), str(s["candidate_key"]))
        if key in by_key:
            raise RuntimeError(f"duplicate shard {key}")
        if key[0] not in range(5) or key[1] not in {"G2", "G3"}:
            raise RuntimeError(f"invalid shard key {key}")
        if any(v is not False for v in s["guardrails"].values()):
            raise RuntimeError(f"guardrail violation shard {key}")
        if expected_source is None:
            expected_source = s["source"]
        elif s["source"] != expected_source:
            raise RuntimeError("source provenance disagreement across shards")
        by_key[key] = s
    if set(by_key) != {(f, k) for f in range(5) for k in ("G2", "G3")}:
        raise RuntimeError("incomplete fold-family shard lattice")

    outer = []
    for fold in range(5):
        s2 = by_key[(fold, "G2")]
        s3 = by_key[(fold, "G3")]
        if s2["training_tokens"] != s3["training_tokens"] or s2["heldout_tokens"] != s3["heldout_tokens"]:
            raise RuntimeError(f"population disagreement fold {fold}")
        m2, m3 = s2["m5"], s3["m5"]
        if int(m2["selected_start_index"]) != int(m3["selected_start_index"]):
            raise RuntimeError(f"M5 selected-start disagreement fold {fold}")
        for field in ("training_conditional_log_likelihood", "heldout_conditional_log_likelihood", "heldout_nats_per_token", "pi"):
            if not close(m2[field], m3[field]):
                raise RuntimeError(f"M5 {field} disagreement fold {fold}: {m2[field]} vs {m3[field]}")
        g2 = s2["candidate"]
        g3 = s3["candidate"]
        if g2["family"] != f0.FAMILY_G2 or g3["family"] != f0.FAMILY_G3:
            raise RuntimeError("candidate family mismatch")
        hg2 = float(g2["heldout_nats_per_token"])
        hg3 = float(g3["heldout_nats_per_token"])
        outer.append({
            "fold": fold,
            "training_tokens": int(s2["training_tokens"]),
            "heldout_tokens": int(s2["heldout_tokens"]),
            "descriptor_standardization": g2["descriptor_standardization"],
            "m5": m2,
            "g2": {k: v for k, v in g2.items() if k != "descriptor_standardization"},
            "g3": g3,
            "direct_g3_minus_g2_nats_per_token": float(hg3 - hg2),
        })

    d2 = [float(r["g2"]["heldout_gain_over_m5_nats_per_token"]) for r in outer]
    d3 = [float(r["g3"]["heldout_gain_over_m5_nats_per_token"]) for r in outer]
    d32 = [float(r["direct_g3_minus_g2_nats_per_token"]) for r in outer]
    s2 = f0.predictive_support(d2)
    s3 = f0.predictive_support(d3)
    n32 = int(np.sum(np.asarray(d32, dtype=float) > 0.0))
    m32 = float(np.median(np.asarray(d32, dtype=float)))

    if s2["supported"] and not s3["supported"]:
        classification = "F0_SELECT_KRS_GATED_TWO_MODE_CHAIN"
    elif s3["supported"] and not s2["supported"]:
        classification = "F0_SELECT_GLOBAL_THREE_MODE_CHAIN"
    elif s2["supported"] and s3["supported"]:
        classification = "F0_SELECT_GLOBAL_THREE_MODE_CHAIN" if (n32 >= 4 and m32 >= f0.PREDICTIVE_GAIN_MIN) else "F0_SELECT_KRS_GATED_TWO_MODE_CHAIN"
    else:
        classification = "F0_GLOBAL_MIXTURE_EXTENSIONS_NOT_PREDICTIVELY_SUPPORTED_WITHIN_TOKEN_STATE_FRONTIER_REQUIRED"

    output = {
        "schema": "issue75-phaseF0-training-latent-diagnostic-v1",
        "status": "PHASE_F0_TRAINING_ONLY_LATENT_FRONTIER_DIAGNOSTIC_COMPLETE",
        "scientific_role": "PRETARGET_ARCHITECTURE_DISCRIMINATION_BY_PHYSICAL_LEAF_PREDICTIVE_OCCUPANCY_LIKELIHOOD",
        "execution_mode": "EXACT_TEN_SHARD_EXECUTION_ONLY_FALLBACK",
        "plan_f0_sha256": f0.sha256_file(f0.PLAN_PATH),
        "implementation_clarification_sha256": f0.sha256_file(f0.CLARIFICATION_PATH),
        "sharding_plan_sha256": f0.sha256_file(SHARD_PLAN),
        "source": expected_source,
        "families": {
            "baseline": {"name": f0.FAMILY_M5, "free_continuous_parameters": 43},
            "g2": {"name": f0.FAMILY_G2, "free_continuous_parameters": f0.G2_FREE, "explicit_nonadjacent_parameters": 0, "generic_distance_parameters": 0, "signature_specific_parameters": 0},
            "g3": {"name": f0.FAMILY_G3, "free_continuous_parameters": f0.G3_FREE, "explicit_nonadjacent_parameters": 0, "generic_distance_parameters": 0, "signature_specific_parameters": 0},
        },
        "outer_folds": outer,
        "support": {
            "g2_over_m5": s2,
            "g3_over_m5": s3,
            "g3_over_g2": {
                "positive_fold_count": n32,
                "median_gain_nats_per_token": m32,
                "displacement_requires_positive_folds": 4,
                "displacement_requires_median_gain_nats_per_token": f0.PREDICTIVE_GAIN_MIN,
            },
        },
        "selection": {"classification": classification, "rule_frozen_before_executable": True},
        "guardrails": {
            "reference_residual_vector_loaded": False,
            "reference_correlation_computed": False,
            "reference_sign_agreement_computed": False,
            "candidate_pair_terms_selected": False,
            "random_restarts": False,
            "rerolls": False,
        },
    }
    raw = f0.canonical_json_bytes(output) + b"\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(json.dumps({
        "status": output["status"],
        "execution_mode": output["execution_mode"],
        "classification": classification,
        "g2_fold_gains": d2,
        "g2_median_gain": s2["median_gain_nats_per_token"],
        "g2_supported": s2["supported"],
        "g3_fold_gains": d3,
        "g3_median_gain": s3["median_gain_nats_per_token"],
        "g3_supported": s3["supported"],
        "g3_minus_g2_fold_gains": d32,
        "g3_minus_g2_median_gain": m32,
        "output_sha256": f0.sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
