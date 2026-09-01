#!/usr/bin/env python3
"""Aggregate the complete Issue #72 V2 Stage C1 first-reveal population.

No hard threshold is applied. The input population must be exactly 124 unique
(axis, randomization) result JSON files: four axes x r0..r30.

Usage:
  python c1_aggregate72_v2.py INPUT_DIR OUTPUT_JSON
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence

import numpy as np

AXES = ("EL", "ES", "ET", "EG")
READINGS = ("ZL3b", "IT2a")
N_ASSIGN = 31
EXPECTED_C0_RAW = "da00a66b77a90eb36a158a9942927a27743e64aba7fac69337ff3a67424d695a"
EXPECTED_C0_GZ = "946d8f8fa61d996a548a344f7e303f804283230ce8bef0d51add473d811e4ed3"
EXPECTED_C0_MANIFEST = "aba822be57bbac0c04a9fa785a0a835eafe192b406fead5cd7166051825f45ae"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dist(xs):
    x = np.asarray(xs, dtype=np.float64)
    if x.shape != (N_ASSIGN,) or not np.all(np.isfinite(x)):
        raise RuntimeError("invalid 31-value distribution")
    return {
        "min": float(np.min(x)),
        "q1_linear": float(np.quantile(x, 0.25, method="linear")),
        "median_linear": float(np.quantile(x, 0.50, method="linear")),
        "q3_linear": float(np.quantile(x, 0.75, method="linear")),
        "max": float(np.max(x)),
        "mean": float(np.mean(x)),
        "values": [float(v) for v in x],
    }


def simple3(xs):
    x = np.asarray(xs, dtype=np.float64)
    return {
        "min": float(np.min(x)),
        "median_linear": float(np.quantile(x, 0.50, method="linear")),
        "max": float(np.max(x)),
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} INPUT_DIR OUTPUT_JSON")
    indir = Path(argv[1]).resolve()
    output = Path(argv[2]).resolve()

    expected = {(a, j) for a in AXES for j in range(N_ASSIGN)}
    rows = {}
    file_hashes = {}
    science_heads = set()
    target_authorities = []

    for path in sorted(indir.rglob("*.json")):
        try:
            r = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if r.get("schema") != "issue72-v2-stage-c1-paired-r1-target-v1":
            continue
        if r.get("status") != "STAGE C1 ASSIGNMENT TARGET SCORED":
            raise RuntimeError(f"unexpected C1 result status: {path}")
        axis = r.get("axis")
        j = int(r.get("randomization"))
        key = (axis, j)
        if key not in expected:
            raise RuntimeError(f"unexpected C1 result identity: {key}")
        if key in rows:
            raise RuntimeError(f"duplicate C1 result: {key}")
        auth = r["authority"]
        if auth["C0_raw_sha256"] != EXPECTED_C0_RAW or auth["C0_gzip_sha256"] != EXPECTED_C0_GZ or auth["C0_manifest_sha256"] != EXPECTED_C0_MANIFEST:
            raise RuntimeError(f"C0 authority mismatch: {key}")
        policy = r["decision_policy"]
        if policy["hard_intervention_threshold_applied"] or policy["readings_averaged"] or policy["coverage_gate_applied"]:
            raise RuntimeError(f"forbidden C1 decision policy: {key}")
        if set(r["topology"]) != set(READINGS):
            raise RuntimeError(f"target reading set mismatch: {key}")
        if len(r["pairs"]) != 66 or len(r["baseline_common"]["z_full"]) != 66 or len(r["randomized_common"]["z_full"]) != 66:
            raise RuntimeError(f"complete-66 vector missing: {key}")
        if len(r["support"]["four_manuscript_fold_counts"]) != 4 or sum(r["support"]["four_manuscript_fold_counts"]) != r["support"]["common_support_count"]:
            raise RuntimeError(f"four-manuscript support mismatch: {key}")
        science_heads.add(r.get("github_sha"))
        target_authorities.append(auth["target_authority"])
        rows[key] = r
        file_hashes[f"{axis}_r{j}"] = {
            "path": str(path.relative_to(indir)),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }

    missing = sorted(expected - set(rows))
    extra = sorted(set(rows) - expected)
    if missing or extra or len(rows) != 124:
        raise RuntimeError(f"incomplete C1 population: n={len(rows)} missing={missing} extra={extra}")
    if len(science_heads) != 1 or None in science_heads:
        raise RuntimeError(f"C1 results do not share one exact scientific head: {science_heads}")
    if any(x != target_authorities[0] for x in target_authorities[1:]):
        raise RuntimeError("target authority differs across C1 results")

    axes = {}
    for axis in AXES:
        ordered = [rows[(axis, j)] for j in range(N_ASSIGN)]
        readings = {}
        for reading in READINGS:
            deltas = [r["topology"][reading]["DELTA_R_randomized_minus_baseline"] for r in ordered]
            basers = [r["topology"][reading]["baseline_pearson"] for r in ordered]
            randrs = [r["topology"][reading]["randomized_pearson"] for r in ordered]
            neg = sum(float(x) < 0 for x in deltas)
            zero = sum(float(x) == 0 for x in deltas)
            pos = sum(float(x) > 0 for x in deltas)
            nonloss = zero + pos
            readings[reading] = {
                "DELTA_R": dist(deltas),
                "direction_counts": {"negative": neg, "zero": zero, "positive": pos},
                "nonloss_count": nonloss,
                "rank_nonloss": float((1 + nonloss) / 32.0),
                "rank_role": "SAMPLED_ASSIGNMENT_MONTE_CARLO_RANK_EVIDENCE_NOT_CLASSICAL_P_VALUE",
                "baseline_common_R": dist(basers),
                "randomized_common_R": dist(randrs),
            }
        both_neg = both_nonneg = mixed = 0
        assignment_directions = []
        for j, r in enumerate(ordered):
            dz = float(r["topology"]["ZL3b"]["DELTA_R_randomized_minus_baseline"])
            di = float(r["topology"]["IT2a"]["DELTA_R_randomized_minus_baseline"])
            if dz < 0 and di < 0:
                cls = "both_negative"; both_neg += 1
            elif dz >= 0 and di >= 0:
                cls = "both_nonnegative"; both_nonneg += 1
            else:
                cls = "mixed"; mixed += 1
            assignment_directions.append({"randomization": j, "ZL3b_delta": dz, "IT2a_delta": di, "class": cls})
        if both_neg + both_nonneg + mixed != N_ASSIGN:
            raise RuntimeError("reading agreement counts do not sum to 31")
        coverage = [r["support"]["randomized_full_coverage"] for r in ordered]
        common_frac = [r["support"]["common_support_fraction"] for r in ordered]
        common_n = [r["support"]["common_support_count"] for r in ordered]
        axes[axis] = {
            "readings": readings,
            "reading_direction_agreement": {
                "both_negative": both_neg,
                "both_nonnegative": both_nonneg,
                "mixed": mixed,
                "assignments": assignment_directions,
            },
            "representation_context": {
                "randomized_full_parser_coverage": simple3(coverage),
                "common_support_fraction": simple3(common_frac),
                "common_support_token_count": simple3(common_n),
            },
        }

    result = {
        "schema": "issue72-v2-stage-c1-paired-r1-aggregate-v1",
        "status": "STAGE C1 COMPLETE FIXED-PATH ASSOCIATION RANDOMIZATION AGGREGATED",
        "target_reveal": True,
        "scientific_head": next(iter(science_heads)),
        "population": {
            "axes": list(AXES),
            "assignments_per_axis": N_ASSIGN,
            "total_results": len(rows),
            "complete_population": True,
        },
        "authority": {
            "C0_raw_sha256": EXPECTED_C0_RAW,
            "C0_gzip_sha256": EXPECTED_C0_GZ,
            "C0_manifest_sha256": EXPECTED_C0_MANIFEST,
            "target_authority": target_authorities[0],
        },
        "aggregation_policy": {
            "quantiles": "numpy.quantile method=linear",
            "hard_intervention_threshold_applied": False,
            "readings_averaged": False,
            "coverage_gate_applied": False,
            "rank_nonloss_formula": "(1 + count[DELTA_R>=0]) / 32",
            "rank_is_classical_exact_pvalue": False,
        },
        "axes": axes,
        "individual_result_files": file_hashes,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    output.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "scientific_head": result["scientific_head"],
        "total_results": len(rows),
        "aggregate_sha256": hashlib.sha256(raw).hexdigest(),
        "axis_summary": {
            a: {
                rd: {
                    "median_delta": axes[a]["readings"][rd]["DELTA_R"]["median_linear"],
                    "mean_delta": axes[a]["readings"][rd]["DELTA_R"]["mean"],
                    "nonloss_count": axes[a]["readings"][rd]["nonloss_count"],
                    "rank_nonloss": axes[a]["readings"][rd]["rank_nonloss"],
                }
                for rd in READINGS
            }
            for a in AXES
        },
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
