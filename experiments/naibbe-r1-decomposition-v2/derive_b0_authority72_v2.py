#!/usr/bin/env python3
"""Derive the compact Issue #72 V2 B0 execution authority from the exact B0 artifact.

This is a transport/provenance utility only. It computes no R1 statistic.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence

EXPECTED_FULL_SHA = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
EXPECTED_COMPACT_SHA = "d38ab785b421bcd7eea0e48fb03d5c6f55d8f733dc662fc4793a1f7c0d161d28"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} FULL_B0_JSON OUTPUT_COMPACT_JSON")
    src_path = Path(argv[1]).resolve()
    out_path = Path(argv[2]).resolve()
    full_raw = src_path.read_bytes()
    got_full = sha256(full_raw)
    if got_full != EXPECTED_FULL_SHA:
        raise RuntimeError(f"full B0 SHA mismatch: {got_full} != {EXPECTED_FULL_SHA}")
    src = json.loads(full_raw)
    if src["status"] != "UNCHANGED_NAIBBE_REP0_REP4_SURFACES_FROZEN":
        raise RuntimeError("unexpected B0 status")
    if any(src["target_access"].values()):
        raise RuntimeError("B0 target firewall not clean")

    out = {
        "schema": "issue72-v2-stage-b0-compact-authority-v1",
        "status": src["status"],
        "source_artifact": {
            "workflow_run": 33462658689,
            "job": 99715920669,
            "artifact_id": 9783720673,
            "artifact_zip_sha256": "0bdb5022c5c348b0898a8de253c2b644576c2654c19710059edabc79bb3b03b5",
            "full_stage_b0_json_sha256": EXPECTED_FULL_SHA,
        },
        "target_access": src["target_access"],
        "reps": {},
    }
    for key, row in src["reps"].items():
        dst = {
            "rep": row["rep"],
            "primary_pooled_surface_sha256": row["primary_pooled_surface_sha256"],
            "support": {x: row["support"][x] for x in ("visible_tokens", "accepted_tokens", "coverage")},
            "per_manuscript": {},
        }
        for manuscript, x in row["per_manuscript"].items():
            dst["per_manuscript"][manuscript] = {
                "seed": x["seed"],
                "primary_surface_sha256": x["primary_surface_sha256"],
                "support": {y: x["support"][y] for y in ("visible_tokens", "accepted_tokens", "coverage")},
            }
        out["reps"][key] = dst

    raw = (json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    got_compact = sha256(raw)
    if got_compact != EXPECTED_COMPACT_SHA:
        raise RuntimeError(f"compact B0 SHA mismatch: {got_compact} != {EXPECTED_COMPACT_SHA}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(json.dumps({
        "full_B0_sha256": got_full,
        "compact_B0_sha256": got_compact,
        "compact_bytes": len(raw),
        "R1_target_computed": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
