#!/usr/bin/env python3
"""Derive Stage D PT baseline authority from the exact target-blind B0 artifact.

Transport/provenance utility only. It retains exactly the B0 fields needed to
prove unchanged baseline replay before PT generation. It computes no pair-Q,
residual-Z, target topology, R1 score, or intervention result.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence

EXPECTED_FULL_SHA = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
SOURCE_RUN = 33462658689
SOURCE_JOB = 99715920669
SOURCE_ARTIFACT_ID = 9783720673
SOURCE_ARTIFACT_ZIP_SHA256 = "0bdb5022c5c348b0898a8de253c2b644576c2654c19710059edabc79bb3b03b5"
MANUSCRIPTS = ("BIS193", "CLM13027", "Mazarine915", "UBL758")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} FULL_B0_JSON OUTPUT_PT_AUTHORITY_JSON")
    src_path = Path(argv[1]).resolve()
    out_path = Path(argv[2]).resolve()
    full_raw = src_path.read_bytes()
    got_full = sha256(full_raw)
    if got_full != EXPECTED_FULL_SHA:
        raise RuntimeError(f"full B0 SHA mismatch: {got_full} != {EXPECTED_FULL_SHA}")
    src = json.loads(full_raw)
    if src["status"] != "UNCHANGED_NAIBBE_REP0_REP4_SURFACES_FROZEN":
        raise RuntimeError("unexpected B0 status")
    if set(src["reps"]) != {f"rep{i}" for i in range(5)}:
        raise RuntimeError("unexpected B0 rep population")
    if any(src["target_access"].values()):
        raise RuntimeError("B0 target firewall not clean")

    out = {
        "schema": "issue72-v2-stage-d0-pt-baseline-authority-v1",
        "status": src["status"],
        "scientific_role": "TARGET_BLIND_BASELINE_REPLAY_AUTHORITY_FOR_STAGE_D_PT",
        "source_artifact": {
            "workflow_run": SOURCE_RUN,
            "job": SOURCE_JOB,
            "artifact_id": SOURCE_ARTIFACT_ID,
            "artifact_zip_sha256": SOURCE_ARTIFACT_ZIP_SHA256,
            "full_stage_b0_json_sha256": EXPECTED_FULL_SHA,
        },
        "target_access": dict(src["target_access"]),
        "reps": {},
    }

    for rep in range(5):
        key = f"rep{rep}"
        row = src["reps"][key]
        dst = {
            "rep": int(row["rep"]),
            "primary_pooled_surface_sha256": row["primary_pooled_surface_sha256"],
            "raw_pooled_surface_sha256": row["raw_pooled_surface_sha256"],
            "support": {
                k: row["support"][k]
                for k in ("visible_tokens", "accepted_tokens", "coverage")
            },
            "per_manuscript": {},
        }
        for manuscript in MANUSCRIPTS:
            x = row["per_manuscript"][manuscript]
            dst["per_manuscript"][manuscript] = {
                "seed": int(x["seed"]),
                "primary_surface_sha256": x["primary_surface_sha256"],
                "raw_surface_sha256": x["raw_surface_sha256"],
                "support": {
                    k: x["support"][k]
                    for k in ("visible_tokens", "accepted_tokens", "coverage")
                },
                "ambiguity_retries": int(x["generation_diagnostics"]["ambiguity_retries"]),
            }
        out["reps"][key] = dst

    raw = (json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(json.dumps({
        "status": out["status"],
        "scientific_role": out["scientific_role"],
        "source_full_sha256": got_full,
        "derived_pt_authority_sha256": sha256(raw),
        "derived_bytes": len(raw),
        "target_loaded": False,
        "R1_computed": False,
        "PT_surface_generated": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
