#!/usr/bin/env python3
"""Score-free Stage 0 authority checker for Issue #172.

This executable validates only frozen design/authority metadata. It must not load
candidate outputs or compute any Issue #172 R1-R8 scientific target score.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "experiments/joint-mechanism-discrimination/authority_manifest_v1.json"
VALID_REPLAY_CLASSES = {"DIRECT_REPLAY", "FROZEN_ADAPTER", "SEPARATE_ARM", "ACCESS_CONSTRAINT"}
VALID_ROLES = {"CONTROL / NULL", "SURFACE GENERATOR ONLY", "REVERSIBLE TRANSFORM / DECODER CANDIDATE"}
VALID_CURRIER_ACCESS = {"ENDOGENOUS_STATE", "EXOGENOUS_CURRIER_SIDEINFO", "SCORING_ONLY_METADATA"}
REQUIRED_RESPONSIBILITIES = [f"R{i}" for i in range(1, 11)]
EXPECTED_CHRONOLOGY = [
    "plan_commit",
    "manifest_commit",
    "stage0_checker_commit",
    "stage0_workflow_commit",
    "exact_head_green_gate0",
    "stage0_merge",
    "fresh_target_plan_branch",
    "target_plan_commit",
    "scorer_only_commit",
    "workflow_after_scorer_commit",
    "single_first_target_reveal",
]


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check(name: str, condition: bool, detail: Any = None) -> dict[str, Any]:
    return {"name": name, "pass": bool(condition), "detail": detail}


def walk_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def run(manifest_path: Path, output_path: Path) -> int:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks: list[dict[str, Any]] = []

    checks.append(check("schema_version", manifest.get("schema_version") == 1, manifest.get("schema_version")))
    checks.append(check("issue", manifest.get("issue") == 172, manifest.get("issue")))
    checks.append(check("stage_is_authority_only", manifest.get("stage") == "stage0_authority_only", manifest.get("stage")))

    plan = manifest["plan"]
    plan_path = ROOT / plan["path"]
    checks.append(check("plan_exists", plan_path.is_file(), str(plan_path.relative_to(ROOT))))
    if plan_path.is_file():
        checks.append(check("plan_blob", git_blob(plan_path) == plan["blob"], {"actual": git_blob(plan_path), "expected": plan["blob"]}))

    authority_results = []
    for authority in manifest.get("authority_files", []):
        path = ROOT / authority["path"]
        exists = path.is_file()
        actual = git_blob(path) if exists else None
        ok = exists and actual == authority["blob"]
        authority_results.append({"path": authority["path"], "expected_blob": authority["blob"], "actual_blob": actual, "pass": ok})
    checks.append(check("authority_file_blobs", bool(authority_results) and all(x["pass"] for x in authority_results), authority_results))

    responsibilities = manifest.get("responsibilities", {})
    checks.append(check("responsibility_set", list(responsibilities.keys()) == REQUIRED_RESPONSIBILITIES, list(responsibilities.keys())))
    replay_ok = True
    replay_detail = {}
    for rid in REQUIRED_RESPONSIBILITIES:
        classes = responsibilities.get(rid, {}).get("replay_classes", [])
        valid = bool(classes) and set(classes).issubset(VALID_REPLAY_CLASSES)
        replay_ok &= valid
        replay_detail[rid] = classes
    checks.append(check("replay_classes", replay_ok, replay_detail))

    r2 = responsibilities["R2"]["hard_gate"]
    checks.append(check("r2_complete_66", r2["edge_count"] == 66 and r2["sign_agreement_min"] == 50, {"edge_count": r2["edge_count"], "sign_min": r2["sign_agreement_min"]}))
    checks.append(check("r2_frozen_thresholds", r2["coverage_min"] == 0.60 and r2["reliability_min"] == 0.50 and r2["pearson_min_each_reading"] == 0.70 and r2["existence_maxT_p_max"] == 0.01, r2))

    r3 = responsibilities["R3"]["hard_gate"]
    r4 = responsibilities["R4"]["hard_gate"]
    checks.append(check("r3_ratio_and_raw_gate", r3["s2_ratio_min"] == 0.5 and r3["s2_ratio_max"] == 2.0 and r3["h62_raw_ratio_min"] == 0.5, r3))
    checks.append(check("r4_signed_gate", r4["same_sign_required"] is True and r4["wrong_sign_is_automatic_failure"] is True and r4["mean_ratio_min"] == 0.5 and r4["mean_ratio_max"] == 2.0, r4))

    r5 = responsibilities["R5"]
    checks.append(check("r5_two_reading_targets", abs(r5["historical_authority"]["common_eva_zl3b_gain"] - 0.1336232955274749) < 1e-15 and abs(r5["historical_authority"]["common_eva_it2a_gain"] - 0.16184998339508744) < 1e-15, r5["historical_authority"]))
    checks.append(check("r5_line_reset", r5["hard_gate"]["beyond_line_must_not_be_robust_positive"] is True, r5["hard_gate"]))

    r6 = responsibilities["R6"]["hard_gate"]
    checks.append(check("r6_shared_parameter_firewall", r6["per_reading_posthoc_tuning"] is False and r6["same_parameterization_across_readings"] is True and r6["reading_specific_over_shared_must_not_be_robust"] is True, r6))

    r7 = responsibilities["R7"]
    ladder = r7["historical_authority"]["k_ladder"]
    allowed_access = set(r7["hard_gate"]["allowed_access_classes"])
    checks.append(check("r7_k_ladder", ladder == [1, 2, 4, 8, 16] and r7["historical_authority"]["first_sufficient_k"] == 16 and r7["hard_gate"]["k16_must_suffice"] is True and r7["hard_gate"]["k_le_8_must_not_suffice_both_regimes"] is True, {"ladder": ladder, "first_sufficient_k": r7["historical_authority"]["first_sufficient_k"]}))
    checks.append(check("r7_access_enum", allowed_access == VALID_CURRIER_ACCESS, sorted(allowed_access)))

    r8 = responsibilities["R8"]
    target = r8["historical_authority"]["previous_paragraph_gain"]
    gate = r8["hard_gate"]
    checks.append(check("r8_corrected_order", r8["historical_authority"]["corrected_order"] == "raw_page_first_occurrence_then_numeric_paragraph_rank" and gate["no_future_tokens"] is True, r8["historical_authority"]["corrected_order"]))
    checks.append(check("r8_effect_band", abs(gate["previous_paragraph_gain_min"] - 0.5 * target) < 1e-12 and abs(gate["previous_paragraph_gain_max"] - 2.0 * target) < 1e-12 and gate["same_line_inventory_must_not_be_robust_positive"] is True, {"target": target, "min": gate["previous_paragraph_gain_min"], "max": gate["previous_paragraph_gain_max"]}))

    r9 = responsibilities["R9"]["hard_gate"]
    checks.append(check("r9_exact_decoder_gate", r9["decoder_exact_recovery_fraction"] == 1.0 and r9["ambiguous_truth_contained_does_not_pass"] is True and r9["surface_generator_decoder_eligible"] is False, r9))

    r10 = responsibilities["R10"]
    required_candidate_fields = set(r10["required_candidate_fields"])
    checks.append(check("r10_required_accounting_fields", len(required_candidate_fields) == len(r10["required_candidate_fields"]) and {"role", "target_token_identity_access", "currier_access", "candidate_specific_repairs", "per_reading_tuning", "heldout_item_fitting"}.issubset(required_candidate_fields), sorted(required_candidate_fields)))

    roster = manifest.get("candidate_roster", [])
    role_ok = all(c.get("role") in VALID_ROLES for c in roster)
    access_ok = all(c.get("currier_access") in VALID_CURRIER_ACCESS for c in roster)
    heldout_ok = all(c.get("heldout_item_fitting") is not True for c in roster)
    checks.append(check("candidate_roles", role_ok and len(roster) == 5, [{"id": c.get("id"), "role": c.get("role")} for c in roster]))
    checks.append(check("candidate_currier_access", access_ok, [{"id": c.get("id"), "currier_access": c.get("currier_access")} for c in roster]))
    checks.append(check("no_heldout_item_fitting", heldout_ok, [{"id": c.get("id"), "heldout_item_fitting": c.get("heldout_item_fitting")} for c in roster]))

    controls = [c for c in roster if c.get("role") == "CONTROL / NULL"]
    checks.append(check("controls_not_promotion_eligible", all(c.get("promotion_eligible") is False for c in controls), [c["id"] for c in controls]))

    checks.append(check("chronology", manifest.get("chronology") == EXPECTED_CHRONOLOGY, manifest.get("chronology")))

    forbidden = set(manifest.get("forbidden_stage0_fields", []))
    keys = list(walk_keys(manifest))
    # The names are necessarily present in the declaration list. They must not
    # appear as object keys anywhere in the manifest.
    object_keys = []
    def collect_object_keys(value: Any):
        if isinstance(value, dict):
            for key, child in value.items():
                object_keys.append(key)
                collect_object_keys(child)
        elif isinstance(value, list):
            for child in value:
                collect_object_keys(child)
    collect_object_keys(manifest)
    leaked = sorted(forbidden.intersection(object_keys))
    checks.append(check("no_stage0_candidate_result_fields", not leaked, leaked))

    all_pass = all(c["pass"] for c in checks)
    result = {
        "issue": 172,
        "stage": "stage0",
        "classification": "STAGE0 AUTHORITY READY" if all_pass else "STAGE0 AUTHORITY INVALID",
        "score_free": True,
        "candidate_target_scoring_performed": False,
        "git_head": os.environ.get("GITHUB_SHA") or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "manifest": {
            "path": str(manifest_path.relative_to(ROOT)),
            "git_blob": git_blob(manifest_path),
            "sha256": sha256_file(manifest_path),
        },
        "plan": {
            "path": plan["path"],
            "git_blob": git_blob(plan_path) if plan_path.is_file() else None,
            "frozen_commit": plan["commit"],
        },
        "checks": checks,
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"classification": result["classification"], "checks_passed": sum(c["pass"] for c in checks), "checks_total": len(checks), "score_free": True}, indent=2))
    return 0 if all_pass else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=Path("issue172_stage0_gate.json"))
    args = parser.parse_args()
    manifest_path = args.manifest if args.manifest.is_absolute() else (ROOT / args.manifest)
    output_path = args.output if args.output.is_absolute() else (ROOT / args.output)
    return run(manifest_path.resolve(), output_path.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
