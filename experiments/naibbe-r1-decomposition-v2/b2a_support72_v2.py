#!/usr/bin/env python3
"""Issue #72 V2 Stage B2a: target-blind unchanged-Naibbe rep5..rep24 support freeze.

This executable extends the Stage B0 positive-control population using the direct
continuation of the already frozen Phase64B seed schedule. It freezes surface
identities and parser support only. It MUST NOT compute pair-Q, residual Z,
E/W, target topology/sign agreement, p-values, or any Issue72 intervention.

Usage:
    python experiments/naibbe-r1-decomposition-v2/b2a_support72_v2.py \
        CREMMA_ROOT NAIBBE_ROOT OUTPUT_JSON
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, Sequence

HERE = Path(__file__).resolve()
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import b0_support72_v2 as b0  # noqa: E402

EXPECTED_B0_SUPPORT_SCRIPT_BLOB = "ef3144591839395c18e1bdf308311bf99562bf9a"
REPS = tuple(range(5, 25))


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT OUTPUT_JSON")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    output = Path(argv[3]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    b0_path = HERE.parent / "b0_support72_v2.py"
    got_b0_blob = git_blob_sha1(b0_path.read_bytes())
    if got_b0_blob != EXPECTED_B0_SUPPORT_SCRIPT_BLOB:
        raise RuntimeError(f"Stage B0 support helper changed: {got_b0_blob}")

    auth = b0.authority(crem, nai)
    module = b0.n64.load_naibbe(nai)
    original_map = dict(module.placeholder_to_glyph)
    parser = b0.e.SlotParser()
    parser_validation = b0.e.validate_parser(parser)
    sources = {
        name: b0.b.parse_latin_manuscript(crem, name, rel)
        for name, rel in b0.b.PRIMARY_MANUSCRIPTS.items()
    }

    reps: Dict[str, dict] = {}
    for rep in REPS:
        pooled_primary = []
        pooled_raw = []
        per_ms = {}
        for mi, manuscript in enumerate(b0.MANUSCRIPTS):
            seed = 6480000 + 100 * mi + rep
            primary, raw, diag = b0.n64.encrypt_manuscript(
                module, sources[manuscript], manuscript, original_map, seed
            )
            psha = b0.surface_sha(primary)
            rsha = b0.surface_sha(raw)
            support = b0.parser_support(primary, parser)
            pooled_primary.extend(primary)
            pooled_raw.extend(raw)
            per_ms[manuscript] = {
                "seed": int(seed),
                "primary_surface_sha256": psha,
                "raw_surface_sha256": rsha,
                "support": support,
                "generation_diagnostics": diag,
            }

        psha = b0.surface_sha(pooled_primary)
        rsha = b0.surface_sha(pooled_raw)
        support = b0.parser_support(pooled_primary, parser)
        reps[f"rep{rep}"] = {
            "rep": int(rep),
            "primary_pooled_surface_sha256": psha,
            "raw_pooled_surface_sha256": rsha,
            "support": support,
            "per_manuscript": per_ms,
        }

    result = {
        "schema": "issue72-v2-stage-b2a-unchanged-naibbe-support-v1",
        "status": "UNCHANGED_NAIBBE_REP5_REP24_SURFACES_FROZEN",
        "parent_main": b0.PARENT_MAIN,
        "scientific_role": "TARGET_BLIND_EXTENDED_POSITIVE_CONTROL_SUPPORT_FREEZE",
        "authority": auth,
        "implementation_authority": {
            "b0_support72_v2.py_git_blob": got_b0_blob,
        },
        "population": {
            "reps": list(REPS),
            "manuscripts": list(b0.MANUSCRIPTS),
            "seed_rule": "6480000 + 100*manuscript_index + rep",
            "selection_rule": "ALL_REP5_THROUGH_REP24_NO_DROPS_NO_REROLLS",
        },
        "parser_validation": parser_validation,
        "coverage_policy": "CONTINUOUS_DESCRIPTIVE_NO_HARD_CUTOFF",
        "target_access": {
            "slot_pair_Q_computed": False,
            "residual_Z_computed": False,
            "E_or_W_computed": False,
            "ZL3b_or_IT2a_target_loaded": False,
            "topology_or_sign_computed": False,
            "R1_pvalue_computed": False,
            "Issue72_intervention_surface_generated": False,
            "Issue72_intervention_R1_computed": False,
        },
        "reps": reps,
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    output.write_bytes(raw)

    print(json.dumps({
        "status": result["status"],
        "output_sha256": sha256_bytes(raw),
        "coverage_min": min(row["support"]["coverage"] for row in reps.values()),
        "coverage_max": max(row["support"]["coverage"] for row in reps.values()),
        "reps": {
            name: {
                "primary_pooled_surface_sha256": row["primary_pooled_surface_sha256"],
                "visible": row["support"]["visible_tokens"],
                "accepted": row["support"]["accepted_tokens"],
                "coverage": row["support"]["coverage"],
            }
            for name, row in reps.items()
        },
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
