#!/usr/bin/env python3
"""Reconcile redundant cross-run M5 metadata for Phase-F0 shard aggregation.

This script does not alter any G2/G3 candidate field. It verifies the frozen
cross-run M5 tolerances, then makes the redundant G3-shard M5 metadata exactly
equal to the corresponding G2-shard M5 metadata so the original exact-equality
aggregator can consume the already-completed ten scientific shards.

Usage:
  python phase75f0_shard_baseline_reconcile.py RAW_DIR OUT_DIR AUDIT_JSON
"""
from __future__ import annotations

import glob
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Sequence

TRAIN_LL_TOL = 1e-3
HOLD_LL_TOL = 1e-3
HOLD_NPT_TOL = 1e-7
PI_TOL = 1e-4


def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} RAW_DIR OUT_DIR AUDIT_JSON")
    raw_dir = Path(argv[1]).resolve()
    out_dir = Path(argv[2]).resolve()
    audit_path = Path(argv[3]).resolve()
    paths = sorted(Path(p) for p in glob.glob(str(raw_dir / "phase75f0_shard_fold*_G*.json")))
    if len(paths) != 10:
        raise RuntimeError(f"expected 10 raw shard JSONs, got {len(paths)}")

    shards = {}
    raw_sha = {}
    for p in paths:
        data = p.read_bytes()
        r = json.loads(data)
        if r.get("schema") != "issue75-phaseF0-fold-family-shard-v1" or r.get("status") != "PHASE_F0_FOLD_FAMILY_SHARD_COMPLETE_TARGET_BLIND":
            raise RuntimeError(f"invalid shard {p.name}")
        key = (int(r["fold"]), str(r["candidate_key"]))
        if key in shards:
            raise RuntimeError(f"duplicate shard {key}")
        shards[key] = r
        raw_sha[key] = sha256(data)
    expected = {(f, k) for f in range(5) for k in ("G2", "G3")}
    if set(shards) != expected:
        raise RuntimeError("incomplete shard lattice")

    out_dir.mkdir(parents=True, exist_ok=False)
    audits = []
    for f in range(5):
        g2 = shards[(f, "G2")]
        g3 = shards[(f, "G3")]
        if g2["source"] != g3["source"] or g2["training_tokens"] != g3["training_tokens"] or g2["heldout_tokens"] != g3["heldout_tokens"]:
            raise RuntimeError(f"source/population mismatch fold {f}")
        m2, m3 = g2["m5"], g3["m5"]
        if int(m2["selected_start_index"]) != int(m3["selected_start_index"]):
            raise RuntimeError(f"M5 selected-start mismatch fold {f}")
        diffs = {
            "training_conditional_log_likelihood": abs(float(m2["training_conditional_log_likelihood"]) - float(m3["training_conditional_log_likelihood"])),
            "heldout_conditional_log_likelihood": abs(float(m2["heldout_conditional_log_likelihood"]) - float(m3["heldout_conditional_log_likelihood"])),
            "heldout_nats_per_token": abs(float(m2["heldout_nats_per_token"]) - float(m3["heldout_nats_per_token"])),
            "pi": abs(float(m2["pi"]) - float(m3["pi"])),
        }
        if not all(math.isfinite(v) for v in diffs.values()):
            raise RuntimeError(f"non-finite M5 difference fold {f}")
        if diffs["training_conditional_log_likelihood"] > TRAIN_LL_TOL:
            raise RuntimeError(f"training LL mismatch fold {f}: {diffs}")
        if diffs["heldout_conditional_log_likelihood"] > HOLD_LL_TOL:
            raise RuntimeError(f"heldout LL mismatch fold {f}: {diffs}")
        if diffs["heldout_nats_per_token"] > HOLD_NPT_TOL:
            raise RuntimeError(f"heldout nat/token mismatch fold {f}: {diffs}")
        if diffs["pi"] > PI_TOL:
            raise RuntimeError(f"pi mismatch fold {f}: {diffs}")

        # Candidate objects remain byte-for-object identical. Only the redundant
        # independently-refitted baseline metadata in the G3 shard is replaced
        # after the numerical-equivalence checks above.
        g2_out = json.loads(json.dumps(g2))
        g3_out = json.loads(json.dumps(g3))
        g3_candidate_before = canonical(g3_out["candidate"])
        g3_out["m5"] = json.loads(json.dumps(g2_out["m5"]))
        if canonical(g3_out["candidate"]) != g3_candidate_before:
            raise RuntimeError("candidate mutation detected")

        for key, obj in (((f, "G2"), g2_out), ((f, "G3"), g3_out)):
            name = f"phase75f0_shard_fold{f}_{key[1]}.json"
            (out_dir / name).write_bytes(canonical(obj))
        audits.append({
            "fold": f,
            "selected_start_index": int(m2["selected_start_index"]),
            "absolute_m5_differences_before_reconciliation": diffs,
            "raw_g2_sha256": raw_sha[(f, "G2")],
            "raw_g3_sha256": raw_sha[(f, "G3")],
            "candidate_fields_modified": False,
        })

    audit = {
        "schema": "issue75-phaseF0-shard-baseline-reconcile-v1",
        "status": "REDUNDANT_M5_METADATA_RECONCILED_WITHIN_FROZEN_NUMERICAL_TOLERANCES",
        "source_run": 33548214504,
        "tolerances": {
            "training_conditional_log_likelihood_total_nat": TRAIN_LL_TOL,
            "heldout_conditional_log_likelihood_total_nat": HOLD_LL_TOL,
            "heldout_nats_per_token": HOLD_NPT_TOL,
            "pi": PI_TOL,
        },
        "folds": audits,
        "candidate_fields_modified": False,
        "model_selection_performed": False,
    }
    audit_raw = canonical(audit)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_bytes(audit_raw)
    print(json.dumps({
        "status": audit["status"],
        "maximum_training_ll_difference": max(x["absolute_m5_differences_before_reconciliation"]["training_conditional_log_likelihood"] for x in audits),
        "maximum_heldout_nats_per_token_difference": max(x["absolute_m5_differences_before_reconciliation"]["heldout_nats_per_token"] for x in audits),
        "candidate_fields_modified": False,
        "audit_sha256": sha256(audit_raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
