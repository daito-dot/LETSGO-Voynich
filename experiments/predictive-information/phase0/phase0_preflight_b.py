#!/usr/bin/env python3
"""Issue #90 Phase 0 score-free Preflight B.

Thin prereveal Amendment-B wrapper over the archived Preflight-A implementation.
No target-scoring function is introduced here.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import phase0_preflight as P  # noqa: E402

# Amendment B: same bounded 40-token history, one-time scale extension.
P.TAU_GRID = (1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, math.inf)


def normalize_tau_record(rec: dict):
    if rec.get("family") != "DECAY40" or "tau" not in rec:
        return
    value = rec["tau"]
    if value == "INF":
        return
    if math.isinf(float(value)):
        rec["tau"] = "INF"


def strict_json_safe(obj):
    """Losslessly label non-finite diagnostic floats for strict JSON transport."""
    if isinstance(obj, dict):
        return {k: strict_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strict_json_safe(v) for v in obj]
    if isinstance(obj, tuple):
        return [strict_json_safe(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return "INF" if obj > 0 else "-INF"
    return obj


def run(zl_path: Path):
    out = P.run_preflight(zl_path)
    out["schema"] = "issue90-phase0-preflight-b-v1"
    out["amendment_B"] = {
        "history_window": 40,
        "tau_grid": [1, 2, 4, 8, 16, 32, 64, 128, "INF"],
        "INF_definition": "exact uniform weighting over eligible source occurrences within previous at most 40 surface tokens",
        "further_phase0_tau_or_window_extension_licensed": False,
    }
    out["candidate_grid"]["DECAY40"]["tau"] = [1, 2, 4, 8, 16, 32, 64, 128, "INF"]
    out["authority_hashes"]["AMENDMENT_B.md"] = P.sha256_file(HERE.parent / "AMENDMENT_B.md")
    out["authority_hashes"]["PREFLIGHT_A_PROVENANCE.md"] = P.sha256_file(HERE.parent / "PREFLIGHT_A_PROVENANCE.md")
    out["authority_hashes"]["phase0_preflight_A_code.py"] = P.sha256_file(HERE.parent / "phase0_preflight.py")
    out["authority_hashes"]["phase0_preflight_B_wrapper.py"] = P.sha256_file(HERE)

    # Convert exact infinite decay scale to its scientific label before generic transport sanitization.
    for row in out["selections"].values():
        normalize_tau_record(row["selected"])
        for rec in row["candidate_table"]:
            normalize_tau_record(rec)
    for row in out["outer_heldout_predictive"]["folds"]:
        normalize_tau_record(row["selected"])
    for rep in out["score_free_generation"].values():
        for diag in rep["fold_diagnostics"].values():
            normalize_tau_record(diag["selected"])

    out = strict_json_safe(out)
    # Recompute selection hash on the strict serialized authority representation.
    out["selection_sha256"] = P.I.sha256_obj(out["selections"])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--preflight", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.preflight is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        x = P.self_test()
        x["amendment_B_tau_grid"] = [1, 2, 4, 8, 16, 32, 64, 128, "INF"]
        print(json.dumps(x, indent=2, sort_keys=True))
        return 0
    out = run(Path(ns.preflight[0]))
    Path(ns.preflight[1]).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "selection": {f:r["selected"] for f,r in out["selections"].items()},
        "predictive": out["outer_heldout_predictive"]["summary"],
        "selection_sha256": out["selection_sha256"],
        "target_score_calls": out["target_score_calls"],
    }, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
