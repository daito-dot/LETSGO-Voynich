#!/usr/bin/env python3
"""Issue #176 runtime-recovery wrapper for the frozen Issue #172 scorer.

This file does not reimplement scientific scoring.  It verifies and imports the
frozen v1 scorer, normalizes the historical Phase4A self-test return contract,
and delegates score-free preflight or full scoring to the frozen implementation.

Scientific authority: ISSUE176_RECOVERY_EXECUTION_PLAN.md.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve()
V1_PATH = HERE.with_name("first_reveal_historical_anchor_scorer.py")
EXPECTED_V1_BLOB = "f90f194396acdc50599cf9713dbbeb3ab5b4bed3"
SCHEMA = "issue176-runtime-recovery-v1"


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require_frozen_v1() -> str:
    got = git_blob(V1_PATH)
    if got != EXPECTED_V1_BLOB:
        raise RuntimeError(f"frozen v1 scorer blob changed: {got} != {EXPECTED_V1_BLOB}")
    return got


def load_v1():
    require_frozen_v1()
    spec = importlib.util.spec_from_file_location("issue172_frozen_v1", V1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen Issue172 v1 scorer")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def normalize_r1_return(value):
    if value is None:
        return {"ok": True, "upstream_return": None}
    if isinstance(value, Mapping):
        if value.get("ok") is False:
            raise RuntimeError("historical R1 self-test explicitly reported ok=false")
        return {"ok": True, "upstream_return": dict(value)}
    raise RuntimeError(f"unexpected historical R1 self-test return type: {type(value).__name__}")


def install_r1_self_test_adapter(v1):
    original = v1.R1A.self_test
    if getattr(original, "_issue176_normalized", False):
        raise RuntimeError("Issue176 R1 self-test adapter already installed")

    def normalized():
        # The original historical self-test is invoked exactly once per adapter call.
        return normalize_r1_return(original())

    normalized._issue176_normalized = True
    normalized._issue176_original = original
    v1.R1A.self_test = normalized
    return original


def wrapper_self_test() -> dict:
    v1 = load_v1()
    install_r1_self_test_adapter(v1)
    normalized = v1.R1A.self_test()
    if normalized.get("ok") is not True:
        raise AssertionError("normalized historical R1 self-test did not pass")
    joint = v1.self_test()
    if joint.get("ok") is not True:
        raise AssertionError("frozen v1 target-free joint self-test did not pass after normalization")
    if joint.get("target_sources_loaded") is not False:
        raise AssertionError("target-free self-test unexpectedly loaded target sources")
    if joint.get("real_issue172_candidate_scores_computed") is not False:
        raise AssertionError("target-free self-test unexpectedly computed candidate scores")
    return {
        "schema": SCHEMA,
        "mode": "self-test",
        "ok": True,
        "frozen_v1_blob": require_frozen_v1(),
        "normalized_R1_self_test": normalized,
        "frozen_v1_joint_self_test": joint,
        "target_sources_loaded": False,
        "scientific_candidate_scores_computed": False,
    }


def preflight_only(zl_path: Path, it_path: Path, cremma_root: Path, naibbe_root: Path) -> dict:
    v1 = load_v1()
    install_r1_self_test_adapter(v1)
    pf, *_rest = v1.preflight(zl_path, it_path, cremma_root, naibbe_root)
    if pf.get("scientific_candidate_scores_computed") is not False:
        raise RuntimeError("frozen v1 preflight violated score-free contract")
    return {
        "schema": SCHEMA,
        "mode": "preflight-only",
        "ok": True,
        "frozen_v1_blob": require_frozen_v1(),
        "scientific_candidate_scores_computed": False,
        "preflight": pf,
    }


def invalid_preflight(exc: Exception) -> dict:
    return {
        "schema": SCHEMA,
        "mode": "preflight-only",
        "ok": False,
        "scientific_candidate_scores_computed": False,
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {"scientific_workflow_licensed": False},
    }


def run_science(zl_path: Path, it_path: Path, cremma_root: Path, naibbe_root: Path):
    v1 = load_v1()
    install_r1_self_test_adapter(v1)
    try:
        result = v1.score_all(zl_path, it_path, cremma_root, naibbe_root)
        return result, 0
    except Exception as exc:
        return v1.invalid_result(exc), 1


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--self-test", action="store_true")
    g.add_argument(
        "--preflight-only",
        nargs=5,
        metavar=("ZL3B", "IT2A", "CREMMA_ROOT", "NAIBBE_ROOT", "OUT_JSON"),
    )
    g.add_argument(
        "--run",
        nargs=5,
        metavar=("ZL3B", "IT2A", "CREMMA_ROOT", "NAIBBE_ROOT", "OUT_JSON"),
    )
    ns = ap.parse_args(argv)

    if ns.self_test:
        print(canonical_json(wrapper_self_test()), end="")
        return 0

    args = ns.preflight_only if ns.preflight_only is not None else ns.run
    zl, it, cr, nr, out = map(lambda x: Path(x).resolve(), args)
    out.parent.mkdir(parents=True, exist_ok=True)

    if ns.preflight_only is not None:
        try:
            result = preflight_only(zl, it, cr, nr)
            rc = 0
        except Exception as exc:
            result = invalid_preflight(exc)
            rc = 1
    else:
        result, rc = run_science(zl, it, cr, nr)

    out.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
