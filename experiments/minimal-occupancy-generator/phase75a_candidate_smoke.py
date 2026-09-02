#!/usr/bin/env python3
"""Issue #75 Phase A target-blind candidate-null execution smoke.

This wrapper exercises the already-frozen candidate-owned Q/Z/null machinery
for one exact Stage-A0 corpus but deliberately never calls the target loader.
It is an implementation smoke test only, not a scientific target result.

Usage:
    python phase75a_candidate_smoke.py ZL3B_PATH FAMILY REP OUTPUT_JSON
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75a_score as score  # noqa: E402


def main(argv: Sequence[str]) -> int:
    if len(argv) != 5:
        raise SystemExit(f"usage: {argv[0]} ZL3B_PATH FAMILY REP OUTPUT_JSON")
    src = Path(argv[1]).resolve()
    family = argv[2]
    rep = int(argv[3])
    out = Path(argv[4]).resolve()
    if family not in score.FAMILIES or rep not in range(score.N_REPS):
        raise SystemExit("invalid family/rep")

    authority, cases = score.load_a0_authority()
    candidate, X, audit = score.build_exact_case(src, family, rep, authority, cases)
    measurement = score.candidate_measurement(candidate, X, family, rep)
    if not math.isfinite(float(measurement["residual_energy"])):
        raise RuntimeError("non-finite candidate residual energy")
    p = float(measurement["p_exist"])
    if not 0.0 < p <= 1.0:
        raise RuntimeError("invalid candidate p_exist")
    if len(measurement["z_full"]) != 66:
        raise RuntimeError("candidate residual vector is not complete 66-edge vector")

    result = {
        "schema": "issue75-phaseA-candidate-null-smoke-v1",
        "status": "CANDIDATE_OWNED_NULL_EXECUTION_VERIFIED_TARGET_BLIND",
        "scientific_role": "PRETARGET_IMPLEMENTATION_SMOKE_ONLY",
        "plan_commit": score.PLAN_COMMIT,
        "family": family,
        "rep": rep,
        "candidate_audit": audit,
        "measurement": measurement,
        "target_access": {
            "pair_Q_computed": True,
            "residual_Z_computed": True,
            "candidate_reference_null_computed": True,
            "candidate_test_null_computed": True,
            "Issue58C_target_vector_loaded": False,
            "Issue58D_target_vector_loaded": False,
            "target_correlation_computed": False,
            "target_sign_agreement_computed": False,
            "T_computed": False,
        },
    }
    raw = score.canonical_json_bytes(result) + b"\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "family": family,
        "rep": rep,
        "occupancy_sha256": audit["occupancy_sha256"],
        "E": measurement["residual_energy"],
        "p_exist": measurement["p_exist"],
        "W": measurement["reliability"]["median"],
        "target_loaded": False,
        "output_sha256": score.sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
