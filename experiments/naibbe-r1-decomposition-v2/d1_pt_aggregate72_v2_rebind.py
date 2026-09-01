#!/usr/bin/env python3
"""Aggregate the complete Issue #72 V2 Stage D1 PT first-reveal population.

This is the post-D0-authority-rebind aggregation adapter for the scorer frozen in
commit 127c86f253a5cc12e3802d0976c96649a2c91524. It does not rescore R1.
It joins each frozen PT score to the already-frozen B2 positive-control baseline
for the same historical RNG block and applies the preregistered Stage D1 law.

Usage:
  python d1_pt_aggregate72_v2_rebind.py INPUT_DIR B2_ARCHIVE OUTPUT_JSON SCIENTIFIC_HEAD
"""
from __future__ import annotations

import glob
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Mapping, Sequence

TARGETS = ("ZL3b", "IT2a")
EXPECTED = {(j, rep) for j in range(31) for rep in range(5)}
SCORE_STATUS = "STAGE_D1_PT_R1_FIRST_REVEAL_ASSIGNMENT_SCORED"
STAGE_D_PLAN_COMMIT = "c45c67a665a7e4ad24c1d2706f83c65931d950a9"
SCORER_FREEZE_COMMIT = "127c86f253a5cc12e3802d0976c96649a2c91524"
PT_AUTHORITY_SHA256 = "703991a4b176e78ea18c30210ec730187b446c0c8b14052fc2d25e4a8d8f86e4"
SOURCE_FULL_B0_SHA256 = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
D0_AGG_SHA256 = "e3039ed40f72e44cc4964efab50d70bc1b113859c77e23ccc97934bb29edb9b8"
D0_REBIND_SHA256 = "cb80833b426d6d9b4d1f307961d862fe02140fcf8f593f870fb3080a39bfc2a0"
B2_ARCHIVE_SHA256 = "2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147"
B2_SCALE = {
    "ZL3b": {"SD": 0.010907479701133605, "MAD": 0.00897810342736527},
    "IT2a": {"SD": 0.008561663953448985, "MAD": 0.005799322835226439},
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def q(xs, p):
    ys = sorted(float(x) for x in xs)
    if not ys:
        return None
    if len(ys) == 1:
        return ys[0]
    z = (len(ys) - 1) * p
    lo = int(math.floor(z))
    hi = int(math.ceil(z))
    if lo == hi:
        return ys[lo]
    return ys[lo] * (hi - z) + ys[hi] * (z - lo)


def summarize(xs):
    ys = [float(x) for x in xs]
    return {
        "n": len(ys),
        "mean": float(statistics.fmean(ys)),
        "median": float(statistics.median(ys)),
        "min": min(ys),
        "q25": q(ys, 0.25),
        "q75": q(ys, 0.75),
        "max": max(ys),
        "sd_population": float(statistics.pstdev(ys)),
    }


def _find_rep(per, rep: int) -> Mapping:
    if isinstance(per, list):
        matches = [x for x in per if isinstance(x, dict) and int(x.get("rep", -1)) == rep]
    elif isinstance(per, dict):
        if f"rep{rep}" in per and isinstance(per[f"rep{rep}"], dict):
            return per[f"rep{rep}"]
        if str(rep) in per and isinstance(per[str(rep)], dict):
            return per[str(rep)]
        matches = [x for x in per.values() if isinstance(x, dict) and int(x.get("rep", -1)) == rep]
    else:
        raise RuntimeError("unexpected B2 per_rep schema")
    if len(matches) != 1:
        raise RuntimeError(f"B2 baseline does not uniquely contain rep{rep}: {len(matches)}")
    return matches[0]


def load_b2_baselines(path: Path) -> dict[int, dict]:
    got = sha256_file(path)
    if got != B2_ARCHIVE_SHA256:
        raise RuntimeError(f"B2 archive SHA mismatch: {got} != {B2_ARCHIVE_SHA256}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("status") != "EXTENDED UNCHANGED-NAIBBE R1 DISTRIBUTION CALIBRATED":
        raise RuntimeError("B2 calibration status changed")
    if obj.get("schema") != "issue72-v2-stage-b2-25rep-positive-control-v1":
        raise RuntimeError(f"B2 calibration schema changed: {obj.get('schema')}")
    if obj.get("issue72_intervention_R1_computed") is not False:
        raise RuntimeError("B2 archive says Issue72 intervention R1 was already computed")
    if obj.get("issue72_intervention_surface_loaded_or_generated") is not False:
        raise RuntimeError("B2 archive says Issue72 intervention surface was already loaded/generated")
    per = obj["per_rep"]
    out = {}
    required = ("coverage", "E", "W", "R_ZL3b", "R_IT2a", "sign_ZL3b", "sign_IT2a")
    for rep in range(5):
        row = _find_rep(per, rep)
        missing = [k for k in required if k not in row]
        if missing:
            raise RuntimeError(f"B2 rep{rep} missing fields: {missing}")
        out[rep] = {
            "rep": rep,
            "coverage": float(row["coverage"]),
            "E": float(row["E"]),
            "W": float(row["W"]),
            "R_ZL3b": float(row["R_ZL3b"]),
            "R_IT2a": float(row["R_IT2a"]),
            "sign_ZL3b": int(row["sign_ZL3b"]),
            "sign_IT2a": int(row["sign_IT2a"]),
        }
    exact_rep0 = {
        "E": 3.1784043855151296,
        "W": 0.954726539114345,
        "R_ZL3b": 0.8830282501011794,
        "R_IT2a": 0.9000974100381157,
        "sign_ZL3b": 60,
        "sign_IT2a": 61,
    }
    for key, expected in exact_rep0.items():
        got_v = out[0][key]
        if isinstance(expected, int):
            if got_v != expected:
                raise RuntimeError(f"B2 rep0 gate failed {key}: {got_v} != {expected}")
        elif abs(got_v - expected) > 1e-12:
            raise RuntimeError(f"B2 rep0 gate failed {key}: {got_v} != {expected}")
    return out


def check_score(r: Mapping, key: tuple[int, int]) -> None:
    j, rep = key
    if r.get("schema") != "issue72-v2-stage-d1-pt-r1-score-v1":
        raise RuntimeError(f"score schema changed {key}: {r.get('schema')}")
    if r.get("status") != SCORE_STATUS:
        raise RuntimeError(f"non-scored input {key}: {r.get('status')}")
    if r.get("stage_d_plan_commit") != STAGE_D_PLAN_COMMIT:
        raise RuntimeError(f"Stage D plan authority changed {key}")
    if r.get("assignment") != {"j": j, "rep": rep}:
        raise RuntimeError(f"assignment identity changed {key}")
    if r.get("reference_namespace") != f"issue72v2:stageD:PT:j{j}:rep{rep}:reference":
        raise RuntimeError(f"reference namespace changed {key}")
    if int(r.get("n_reference", -1)) != 1000:
        raise RuntimeError(f"reference count changed {key}")
    if r.get("coverage_policy") != "CONTINUOUS_DESCRIPTIVE_NO_HARD_CUTOFF":
        raise RuntimeError(f"coverage policy changed {key}")
    if r.get("hard_intervention_threshold_applied") is not False:
        raise RuntimeError(f"hard threshold applied {key}")
    if r.get("target_readings_averaged") is not False:
        raise RuntimeError(f"target readings averaged {key}")
    if r.get("baseline_delta_computed_here") is not False:
        raise RuntimeError(f"scorer unexpectedly computed baseline delta {key}")

    a = r["surface_audit"]
    expected_authority = {
        "d0_aggregate_sha256": D0_AGG_SHA256,
        "d0_authority_rebind_validation_sha256": D0_REBIND_SHA256,
        "compact_pt_authority_sha256": PT_AUTHORITY_SHA256,
        "source_full_b0_sha256": SOURCE_FULL_B0_SHA256,
    }
    for field, expected in expected_authority.items():
        if a.get(field) != expected:
            raise RuntimeError(f"surface authority changed {key} {field}: {a.get(field)}")
    for field in (
        "paired_baseline_exact_replay",
        "pt_primary_exact_d0_replay",
        "pt_raw_exact_d0_replay",
        "pt_support_exact_d0_replay",
        "pt_line_invariant_digests_exact_d0_replay",
    ):
        if a.get(field) is not True:
            raise RuntimeError(f"surface replay gate failed {key} {field}")
    if not (0 < float(a["coverage"]) <= 1):
        raise RuntimeError(f"invalid coverage {key}: {a['coverage']}")

    m = r["measurement"]
    for t in TARGETS:
        topo = m["topology"][t]
        if not math.isfinite(float(topo["pearson"])):
            raise RuntimeError(f"nonfinite R {key} {t}")
        if not 0 <= int(topo["sign_agreement"]) <= 66:
            raise RuntimeError(f"bad sign agreement {key} {t}")
    if not math.isfinite(float(m["residual_energy"])):
        raise RuntimeError(f"nonfinite E {key}")
    if not math.isfinite(float(m["reliability"]["median"])):
        raise RuntimeError(f"nonfinite W {key}")


def main(argv: Sequence[str]) -> int:
    if len(argv) != 5:
        raise SystemExit(f"usage: {argv[0]} INPUT_DIR B2_ARCHIVE OUTPUT_JSON SCIENTIFIC_HEAD")
    inp = Path(argv[1]).resolve()
    b2_path = Path(argv[2]).resolve()
    out = Path(argv[3]).resolve()
    scientific_head = argv[4].strip()
    if len(scientific_head) != 40 or any(c not in "0123456789abcdef" for c in scientific_head):
        raise RuntimeError("SCIENTIFIC_HEAD must be a lowercase 40-hex commit SHA")

    baselines = load_b2_baselines(b2_path)
    paths = sorted(glob.glob(str(inp / "PT_j*_rep*.json")))
    if len(paths) != 155:
        raise RuntimeError(f"need exactly 155 results, found {len(paths)}")

    rows = {}
    target_authority = None
    for p in paths:
        r = json.loads(Path(p).read_text(encoding="utf-8"))
        a = r.get("assignment", {})
        key = (int(a.get("j", -1)), int(a.get("rep", -1)))
        if key not in EXPECTED:
            raise RuntimeError(f"unexpected assignment {key}: {p}")
        if key in rows:
            raise RuntimeError(f"duplicate result {key}")
        check_score(r, key)
        if target_authority is None:
            target_authority = r["target_authority"]
        elif r["target_authority"] != target_authority:
            raise RuntimeError("target authority differs across PT cases")
        rows[key] = r
    if set(rows) != EXPECTED:
        raise RuntimeError("incomplete exact Stage D1 population")

    assignments = []
    per_target_D = {t: [] for t in TARGETS}
    all_case_delta = {t: [] for t in TARGETS}
    all_coverage = []
    for j in range(31):
        block_rows = [rows[(j, rep)] for rep in range(5)]
        entry = {"j": j, "blocks": [], "D": {}, "B2_scale_ratio": {}}
        for rep, r in enumerate(block_rows):
            m = r["measurement"]
            b = baselines[rep]
            rz = float(m["topology"]["ZL3b"]["pearson"])
            ri = float(m["topology"]["IT2a"]["pearson"])
            delta = {"ZL3b": rz - b["R_ZL3b"], "IT2a": ri - b["R_IT2a"]}
            cov = float(r["surface_audit"]["coverage"])
            all_coverage.append(cov)
            entry["blocks"].append({
                "rep": rep,
                "coverage": cov,
                "R_PT_ZL3b": rz,
                "R_PT_IT2a": ri,
                "R_baseline_ZL3b": b["R_ZL3b"],
                "R_baseline_IT2a": b["R_IT2a"],
                "delta_R_ZL3b": delta["ZL3b"],
                "delta_R_IT2a": delta["IT2a"],
                "E_PT": float(m["residual_energy"]),
                "W_PT": float(m["reliability"]["median"]),
                "sign_ZL3b": int(m["topology"]["ZL3b"]["sign_agreement"]),
                "sign_IT2a": int(m["topology"]["IT2a"]["sign_agreement"]),
                "primary_surface_sha256": r["surface_audit"]["primary_pooled_surface_sha256"],
            })
            for t in TARGETS:
                all_case_delta[t].append(float(delta[t]))
        for t in TARGETS:
            field = f"delta_R_{t}"
            ds = [float(x[field]) for x in entry["blocks"]]
            D = float(statistics.fmean(ds))
            entry["D"][t] = D
            entry["B2_scale_ratio"][t] = {
                "D_over_SD": float(D / B2_SCALE[t]["SD"]),
                "D_over_MAD": float(D / B2_SCALE[t]["MAD"]),
            }
            per_target_D[t].append(D)
        entry["direction"] = (
            "both_negative" if entry["D"]["ZL3b"] < 0 and entry["D"]["IT2a"] < 0
            else "both_nonnegative" if entry["D"]["ZL3b"] >= 0 and entry["D"]["IT2a"] >= 0
            else "mixed"
        )
        assignments.append(entry)

    readings = {}
    for t in TARGETS:
        Ds = per_target_D[t]
        nonloss = sum(x >= 0 for x in Ds)
        readings[t] = {
            "D_summary": summarize(Ds),
            "case_delta_summary_155": summarize(all_case_delta[t]),
            "nonloss_count": int(nonloss),
            "loss_count": int(31 - nonloss),
            "p_nonloss": float((1 + nonloss) / 32),
            "B2_scale": B2_SCALE[t],
            "D_over_SD_summary": summarize([x / B2_SCALE[t]["SD"] for x in Ds]),
            "D_over_MAD_summary": summarize([x / B2_SCALE[t]["MAD"] for x in Ds]),
        }
    p_both = max(readings[t]["p_nonloss"] for t in TARGETS)
    direction_counts = {
        direction: sum(a["direction"] == direction for a in assignments)
        for direction in ("both_negative", "both_nonnegative", "mixed")
    }

    result = {
        "schema": "issue72-v2-stage-d1-pt-aggregate-rebind-v1",
        "status": "STAGE_D1_COMPLETE_PT_TOTAL_EFFECT_AGGREGATED",
        "scientific_head": scientific_head,
        "scorer_freeze_commit": SCORER_FREEZE_COMMIT,
        "stage_d_plan_commit": STAGE_D_PLAN_COMMIT,
        "population": {
            "j_values": list(range(31)),
            "reps": list(range(5)),
            "total_results": 155,
            "complete_population": True,
            "no_drops": True,
            "no_rerolls": True,
            "blocks_are_rng_paths_not_independent_texts": True,
        },
        "scientific_role": "WITHIN_LINE_EFFECTIVE_PLAINTEXT_ORDER_FULL_PIPELINE_TOTAL_EFFECT_ON_R1",
        "authorities": {
            "compact_pt_authority_sha256": PT_AUTHORITY_SHA256,
            "source_full_b0_sha256": SOURCE_FULL_B0_SHA256,
            "d0_aggregate_sha256": D0_AGG_SHA256,
            "d0_authority_rebind_validation_sha256": D0_REBIND_SHA256,
            "b2_calibration_archive_sha256": B2_ARCHIVE_SHA256,
            "target_authority": target_authority,
        },
        "paired_b2_baseline": {f"rep{rep}": baselines[rep] for rep in range(5)},
        "readings": readings,
        "p_both": float(p_both),
        "assignment_direction_counts": direction_counts,
        "coverage": summarize(all_coverage),
        "assignments": assignments,
        "aggregation_policy": {
            "D_is_equal_mean_over_rep0_rep4": True,
            "hard_intervention_threshold_applied": False,
            "readings_averaged": False,
            "coverage_gate_applied": False,
            "baseline_rescored": False,
            "B2_scale_is_context_not_threshold": True,
            "p_nonloss_is_finite_randomization_evidence_not_universal_pvalue_gate": True,
        },
        "classification": None,
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(raw, encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "scientific_head": scientific_head,
        "direction_counts": direction_counts,
        "p_nonloss": {t: readings[t]["p_nonloss"] for t in TARGETS},
        "p_both": p_both,
        "D_median": {t: readings[t]["D_summary"]["median"] for t in TARGETS},
        "D_mean": {t: readings[t]["D_summary"]["mean"] for t in TARGETS},
        "coverage": result["coverage"],
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
