#!/usr/bin/env python3
"""Execution-only shard runner for frozen Issue #75 Phase F0.

Usage:
    python phase75f0_shard_runner.py ZL3B_PATH FOLD FAMILY OUTPUT_JSON

FAMILY is G2 or G3. Scientific definitions are imported from the frozen F0
implementation plus its normalization-only repair. This file changes scheduling
only and never loads target topology.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.special import expit

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75f0_stable_runner as stable  # noqa: E402

f0 = stable.f0
real_egen = stable.real_egen

SHARD_PLAN = HERE / "F0_EXECUTION_SHARDING_PLAN.md"


def serialize_vector(v: np.ndarray) -> list[float]:
    return [float(x) for x in np.asarray(v, dtype=np.float64)]


def main(argv: Sequence[str]) -> int:
    if len(argv) != 5:
        raise SystemExit(f"usage: {argv[0]} ZL3B_PATH FOLD FAMILY OUTPUT_JSON")
    src = Path(argv[1]).resolve()
    fold = int(argv[2])
    family = str(argv[3]).upper()
    out_path = Path(argv[4]).resolve()
    if fold not in range(5):
        raise RuntimeError("fold must be 0..4")
    if family not in {"G2", "G3"}:
        raise RuntimeError("family must be G2 or G3")
    if not SHARD_PLAN.exists():
        raise RuntimeError("F0 sharding plan required")

    cgen = real_egen.cgen
    if cgen.a0.e.git_blob_sha1(src.read_bytes()) != cgen.a0.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = cgen.a0.e.SlotParser()
    cgen.a0.e.validate_parser(parser)
    d = cgen.a0.b58.build_dataset(src, parser, "min")
    if d["source_blob"] != cgen.a0.EXPECTED_SOURCE_BLOB or d["visible"] != cgen.a0.EXPECTED_VISIBLE or d["parsed"] != cgen.a0.EXPECTED_PARSED:
        raise RuntimeError("frozen source population mismatch")
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    X = np.asarray(d["X"], dtype=np.uint8)
    fold_counts = [int(np.sum(folds == f)) for f in range(5)]
    if fold_counts != cgen.a0.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen physical fold mismatch: {fold_counts}")

    train = X[folds != fold]
    hold = X[folds == fold]
    expected_train = cgen.a0.EXPECTED_PARSED - cgen.a0.EXPECTED_FOLD_PARSED[fold]
    if len(train) != expected_train or len(hold) != cgen.a0.EXPECTED_FOLD_PARSED[fold]:
        raise RuntimeError("outer fold population mismatch")
    train_counts = f0.counts_for(train)
    hold_counts = f0.counts_for(hold)

    m5 = real_egen.fit_m5(train, do_gradient_audit=(fold == 0))
    m5_train_ll = f0.m5_loglik(m5, train_counts)
    if abs(m5_train_ll - float(m5["selected_log_likelihood"])) > f0.NEST_TOL:
        raise RuntimeError("refitted M5 likelihood mismatch")
    m5_hold_ll = f0.m5_loglik(m5, hold_counts)
    hm5 = float(m5_hold_ll / float(len(hold)))

    m5_public = {
        "family": f0.FAMILY_M5,
        "free_continuous_parameters": 43,
        "selected_start_index": int(m5["selected_start_index"]),
        "training_conditional_log_likelihood": float(m5_train_ll),
        "heldout_conditional_log_likelihood": float(m5_hold_ll),
        "heldout_nats_per_token": hm5,
        "pi": float(m5["pi"]),
    }

    if family == "G2":
        g2 = f0.fit_g2(train, m5, do_gradient_audit=(fold == 0))
        standard = g2["standardization"]
        design = np.asarray(standard["design_state"], dtype=np.float64)
        x = np.asarray(g2["x"], dtype=np.float64)
        hold_ll = f0.g2_loglik(x, hold_counts, design)
        h = float(hold_ll / float(len(hold)))
        gate = x[42:46]
        gate_desc_prob = expit(np.asarray(standard["design_desc"], dtype=np.float64) @ gate)
        candidate = {
            "family": f0.FAMILY_G2,
            "free_continuous_parameters": f0.G2_FREE,
            "selected_start_index": int(g2["selected_start_index"]),
            "training_conditional_log_likelihood": float(g2["selected_log_likelihood"]),
            "training_gain_over_m5": float(g2["training_gain_over_m5"]),
            "heldout_conditional_log_likelihood": float(hold_ll),
            "heldout_nats_per_token": h,
            "heldout_gain_over_m5_nats_per_token": float(h - hm5),
            "descriptor_standardization": {
                "mean_K_R_S": serialize_vector(standard["mean"]),
                "population_sd_K_R_S": serialize_vector(standard["sd"]),
                "active_K_R_S": [bool(z) for z in np.asarray(standard["active"])],
            },
            "gate_intercept_and_K_R_S_slopes": serialize_vector(gate),
            "minimum_descriptor_gate_probability": float(np.min(gate_desc_prob)),
            "maximum_descriptor_gate_probability": float(np.max(gate_desc_prob)),
            "selected_theta0": serialize_vector(x[0:21]),
            "selected_theta1": serialize_vector(x[21:42]),
            "all_starts": g2["all_starts"],
            "gradient_audit": g2["gradient_audit"],
        }
    else:
        g3 = f0.fit_g3(train, m5, do_gradient_audit=(fold == 0))
        x = np.asarray(g3["x"], dtype=np.float64)
        hold_ll = f0.g3_loglik(x, hold_counts)
        h = float(hold_ll / float(len(hold)))
        candidate = {
            "family": f0.FAMILY_G3,
            "free_continuous_parameters": f0.G3_FREE,
            "selected_start_index": int(g3["selected_start_index"]),
            "training_conditional_log_likelihood": float(g3["selected_log_likelihood"]),
            "training_gain_over_m5": float(g3["training_gain_over_m5"]),
            "heldout_conditional_log_likelihood": float(hold_ll),
            "heldout_nats_per_token": h,
            "heldout_gain_over_m5_nats_per_token": float(h - hm5),
            "global_weights": serialize_vector(g3["weights"]),
            "selected_theta0": serialize_vector(x[0:21]),
            "selected_theta1": serialize_vector(x[21:42]),
            "selected_theta2": serialize_vector(x[42:63]),
            "all_starts": g3["all_starts"],
            "gradient_audit": g3["gradient_audit"],
        }

    if not math.isfinite(candidate["heldout_nats_per_token"]):
        raise RuntimeError("non-finite heldout score")
    output = {
        "schema": "issue75-phaseF0-fold-family-shard-v1",
        "status": "PHASE_F0_FOLD_FAMILY_SHARD_COMPLETE_TARGET_BLIND",
        "execution_role": "EXECUTION_ONLY_SHARD_OF_FROZEN_PHASE_F0",
        "sharding_plan_sha256": f0.sha256_file(SHARD_PLAN),
        "fold": int(fold),
        "candidate_key": family,
        "source": {
            "ZL3b_blob": str(d["source_blob"]),
            "visible_tokens": int(d["visible"]),
            "parsed_tokens": int(d["parsed"]),
            "fold_parsed_tokens": fold_counts,
            "parser_policy": "SlotParser(min)",
        },
        "training_tokens": int(len(train)),
        "heldout_tokens": int(len(hold)),
        "m5": m5_public,
        "candidate": candidate,
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
        "fold": fold,
        "candidate_key": family,
        "m5_heldout_nats_per_token": hm5,
        "candidate_heldout_nats_per_token": candidate["heldout_nats_per_token"],
        "gain_nats_per_token": candidate["heldout_gain_over_m5_nats_per_token"],
        "selected_start": candidate["selected_start_index"],
        "output_sha256": f0.sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
