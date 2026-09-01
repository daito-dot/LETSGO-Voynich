#!/usr/bin/env python3
"""Issue #72 V2 Stage D1: PT full-pipeline R1 target scorer.

The scientific contract is frozen in STAGE_D_PT_TOTAL_EFFECT_PLAN.md and
STAGE_D1_PT_TARGET_IMPLEMENTATION.md.

For each (j, rep), this program reconstructs the exact frozen D0 PT surface,
requires exact D0 surface/support identity, then (unless --verify-only) applies
the already-frozen B1/B2 R1 measurement and compares it with the exact B2
positive-control baseline for the same historical RNG block.

Usage:
  python d1_pt_r1_target72_v2.py CREMMA_ROOT NAIBBE_ROOT J REP OUTPUT_JSON [--verify-only]
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

HERE = Path(__file__).resolve()
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import b1_r1_calibration72_v2 as b1  # noqa: E402
import d0_pt_support72_v2 as d0  # noqa: E402

STAGE_D_PLAN_COMMIT = "c45c67a665a7e4ad24c1d2706f83c65931d950a9"
D0_PERMANENT_COMMIT = "7056e7ed037af7ff53927d04355821606b59ba6e"
D0_AGG_SHA256 = "17caf1a6c710b367649499a1fbe71be9e969bc295bc868330372620609e7e50e"
B0_SHA256 = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
B2_ARCHIVE_SHA256 = "2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147"
B1_BLOB = "2115e8dec15fca21514c8f57e9f51523d10a77c3"
D0_BLOB = "56e404b524064bb62e64fd32a6601dd1b77ca347"
TARGET68_BLOB = "e94a24fbdfbb922099407313f23a1b87859130b6"
N_REF = 1000
N_FOLDS = 4
N_EDGES = 66
MANUSCRIPTS = ("BIS193", "CLM13027", "Mazarine915", "UBL758")

D0_DIR = HERE.parent / "stage-d0-pt"
D0_AGG = D0_DIR / "stage_d0_pt_support_aggregate.json"
B2_PATH = HERE.parent / "archive" / "stage_b2_calibration.json"
B0_PATH = HERE.parent / "stage_b0_support.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify_static_authorities() -> dict:
    checks = {
        "stage_b0_support_json_sha256": sha256_file(B0_PATH),
        "stage_d0_aggregate_json_sha256": sha256_file(D0_AGG),
        "stage_b2_calibration_json_sha256": sha256_file(B2_PATH),
        "b1_r1_calibration72_v2_py_blob": git_blob_sha1((HERE.parent / "b1_r1_calibration72_v2.py").read_bytes()),
        "d0_pt_support72_v2_py_blob": git_blob_sha1((HERE.parent / "d0_pt_support72_v2.py").read_bytes()),
        "target68_py_blob": git_blob_sha1((HERE.parents[1] / "joint-constraint-tournament" / "target68.py").read_bytes()),
    }
    expected = {
        "stage_b0_support_json_sha256": B0_SHA256,
        "stage_d0_aggregate_json_sha256": D0_AGG_SHA256,
        "stage_b2_calibration_json_sha256": B2_ARCHIVE_SHA256,
        "b1_r1_calibration72_v2_py_blob": B1_BLOB,
        "d0_pt_support72_v2_py_blob": D0_BLOB,
        "target68_py_blob": TARGET68_BLOB,
    }
    if checks != expected:
        raise RuntimeError(f"static authority mismatch: {checks} != {expected}")

    d0agg = json.loads(D0_AGG.read_text(encoding="utf-8"))
    if d0agg["status"] != "STAGE_D0_COMPLETE_PT_SUPPORT_POPULATION_FROZEN_TARGET_BLIND":
        raise RuntimeError("D0 aggregate status changed")
    pop = d0agg["population"]
    if pop["total_results"] != 155 or pop["complete_population"] is not True or pop["no_drops"] is not True or pop["no_rerolls"] is not True:
        raise RuntimeError("D0 complete-population authority changed")
    if d0agg["target_firewall"]["all_assignment_target_access_false"] is not True or d0agg["target_firewall"]["R1_target_scored"] is not False:
        raise RuntimeError("D0 target firewall changed")
    return checks


def load_d0_case(j: int, rep: int) -> dict:
    path = D0_DIR / "individual" / f"PT_j{j}_rep{rep}.json"
    if not path.is_file():
        raise RuntimeError(f"missing frozen D0 case: {path}")
    r = json.loads(path.read_text(encoding="utf-8"))
    if r["status"] != "STAGE_D0_PT_ASSIGNMENT_SUPPORT_FROZEN_TARGET_BLIND":
        raise RuntimeError("D0 case status changed")
    if r["assignment"]["j"] != j or r["assignment"]["rep"] != rep:
        raise RuntimeError("D0 case identity mismatch")
    if r["paired_baseline"]["exact_stage_b0_replay"] is not True:
        raise RuntimeError("D0 paired baseline was not exact")
    if r["pt_surface"]["line_invariants_all_true"] is not True:
        raise RuntimeError("D0 PT inventory invariants were not all true")
    if any(r["target_access"].values()):
        raise RuntimeError("D0 case target firewall was not clean")
    return r


def load_b2_baseline(rep: int) -> dict:
    obj = json.loads(B2_PATH.read_text(encoding="utf-8"))
    if obj["status"] != "EXTENDED UNCHANGED-NAIBBE R1 DISTRIBUTION CALIBRATED":
        raise RuntimeError("B2 calibration status changed")
    pc = obj["positive_control_summary"]
    per = pc["per_rep"]
    if isinstance(per, list):
        matches = [x for x in per if int(x["rep"]) == rep]
        if len(matches) != 1:
            raise RuntimeError(f"B2 per_rep list does not uniquely contain rep{rep}")
        row = matches[0]
    elif isinstance(per, dict):
        if f"rep{rep}" in per:
            row = per[f"rep{rep}"]
        elif str(rep) in per:
            row = per[str(rep)]
        else:
            matches = [x for x in per.values() if isinstance(x, dict) and int(x.get("rep", -1)) == rep]
            if len(matches) != 1:
                raise RuntimeError(f"B2 per_rep map does not uniquely contain rep{rep}")
            row = matches[0]
    else:
        raise RuntimeError("unexpected B2 per_rep schema")

    required = ("coverage", "E", "W", "R_ZL3b", "R_IT2a", "sign_ZL3b", "sign_IT2a")
    missing = [k for k in required if k not in row]
    if missing:
        raise RuntimeError(f"B2 rep{rep} missing exact baseline fields: {missing}; keys={sorted(row)}")

    out = {"rep": rep}
    for k in ("coverage", "E", "W", "R_ZL3b", "R_IT2a"):
        out[k] = float(row[k])
    for k in ("sign_ZL3b", "sign_IT2a"):
        out[k] = int(row[k])

    if rep == 0:
        exact = {
            "E": 3.1784043855151296,
            "W": 0.954726539114345,
            "R_ZL3b": 0.8830282501011794,
            "R_IT2a": 0.9000974100381157,
            "sign_ZL3b": 60,
            "sign_IT2a": 61,
        }
        for k, expected in exact.items():
            got = out[k]
            if isinstance(expected, int):
                if got != expected:
                    raise RuntimeError(f"B2 rep0 exact gate failed {k}: {got} != {expected}")
            elif abs(got - expected) > 1e-12:
                raise RuntimeError(f"B2 rep0 exact gate failed {k}: {got} != {expected}")
    return out


def build_pt_dataset(cremma_root: Path, naibbe_root: Path, j: int, rep: int, frozen: Mapping) -> dict:
    got_cremma = b1.p62b.verify_cremma_commit(cremma_root)
    if got_cremma != b1.t68.EXPECTED_CREMMA:
        raise RuntimeError(f"CREMMA commit mismatch: {got_cremma}")
    mod = b1.n64.load_naibbe(naibbe_root)
    original_map = dict(mod.placeholder_to_glyph)
    sources = {
        name: b1.p62b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b1.p62b.PRIMARY_MANUSCRIPTS.items()
    }
    parser = b1.e.SlotParser()
    b1.e.validate_parser(parser)

    pooled_primary = []
    pooled_raw = []
    lines = []
    visible = 0
    parsed = 0
    per_manuscript = []

    for fold, manuscript in enumerate(MANUSCRIPTS):
        expected = frozen["pt_surface"]["per_manuscript"][manuscript]
        seed = 6480000 + 100 * fold + rep
        if expected["seed"] != seed:
            raise RuntimeError(f"D0 seed mismatch j{j} rep{rep} {manuscript}")
        primary, raw, diag = d0.encrypt_pt_manuscript(
            mod, sources[manuscript], manuscript, original_map, seed, j
        )
        psha = b1.surface_digest(primary)
        rsha = b1.surface_digest(raw)
        if psha != expected["primary_surface_sha256"]:
            raise RuntimeError(f"D0 PT primary surface mismatch j{j} rep{rep} {manuscript}: {psha}")
        if rsha != expected["raw_surface_sha256"]:
            raise RuntimeError(f"D0 PT raw surface mismatch j{j} rep{rep} {manuscript}: {rsha}")
        if int(diag["ambiguity_retries"]) != int(expected["generation_diagnostics"]["ambiguity_retries"]):
            raise RuntimeError(f"D0 PT retry mismatch j{j} rep{rep} {manuscript}")
        if diag["line_invariants_all_true"] is not True:
            raise RuntimeError("PT line invariant failed on D1 reconstruction")

        pooled_primary.extend(primary)
        pooled_raw.extend(raw)
        mv = 0
        mp = 0
        for item in primary:
            for line_index, toks in enumerate(item.lines):
                n_visible = len(toks)
                visible += n_visible
                mv += n_visible
                rows = []
                positions = []
                for idx, tok_units in enumerate(toks):
                    tok = "".join(tok_units)
                    picked = parser.pick(tok, "min")
                    if picked is None:
                        continue
                    vals = picked[1]
                    rows.append(np.fromiter((bool(vals[s]) for s in range(12)), dtype=np.uint8, count=12))
                    positions.append(b1.t68.position_category(idx, n_visible))
                    parsed += 1
                    mp += 1
                if rows:
                    lines.append({
                        "fold": fold,
                        "manuscript": manuscript,
                        "item_id": item.item_id,
                        "line_index": int(line_index),
                        "occ": np.stack(rows),
                        "positions": tuple(positions),
                    })
        es = expected["support"]
        if mv != int(es["visible_tokens"]) or mp != int(es["accepted_tokens"]):
            raise RuntimeError(f"D0 PT support mismatch j{j} rep{rep} {manuscript}: {(mv,mp)}")
        per_manuscript.append({
            "fold": fold,
            "manuscript": manuscript,
            "seed": seed,
            "primary_surface_sha256": psha,
            "raw_surface_sha256": rsha,
            "visible_tokens": int(mv),
            "parsed_tokens": int(mp),
            "coverage": float(mp / mv) if mv else None,
            "ambiguity_retries": int(diag["ambiguity_retries"]),
        })

    pooled_psha = b1.surface_digest(pooled_primary)
    pooled_rsha = b1.surface_digest(pooled_raw)
    fs = frozen["pt_surface"]
    if pooled_psha != fs["primary_pooled_surface_sha256"]:
        raise RuntimeError(f"D0 PT pooled primary mismatch j{j} rep{rep}")
    if pooled_rsha != fs["raw_pooled_surface_sha256"]:
        raise RuntimeError(f"D0 PT pooled raw mismatch j{j} rep{rep}")
    if visible != int(fs["support"]["visible_tokens"]) or parsed != int(fs["support"]["accepted_tokens"]):
        raise RuntimeError(f"D0 PT pooled support mismatch j{j} rep{rep}: {(visible,parsed)}")

    X = np.concatenate([x["occ"] for x in lines], axis=0)
    token_folds = np.concatenate([np.full(len(x["occ"]), x["fold"], np.int8) for x in lines])
    pos_id = np.concatenate([
        np.asarray([b1.b58.POSITION_INDEX.get(p, -1) for p in x["positions"]], dtype=np.int8)
        for x in lines
    ])
    maxlen = max(len(x["occ"]) for x in lines)
    padded = np.zeros((len(lines), maxlen, 12), dtype=np.uint8)
    line_mask = np.zeros((len(lines), maxlen), dtype=bool)
    for i, row in enumerate(lines):
        z = row["occ"]
        padded[i, : len(z)] = z
        line_mask[i, : len(z)] = True
    if not np.array_equal(padded[line_mask], X):
        raise RuntimeError("PT padded/flat candidate order mismatch")

    fold_counts = [int(np.sum(token_folds == f)) for f in range(N_FOLDS)]
    expected_fold_counts = [
        int(fs["per_manuscript"][m]["support"]["accepted_tokens"]) for m in MANUSCRIPTS
    ]
    if fold_counts != expected_fold_counts:
        raise RuntimeError(f"PT fold counts mismatch: {fold_counts} != {expected_fold_counts}")

    return {
        "rep": rep,
        "j": j,
        "visible": int(visible),
        "parsed": int(parsed),
        "coverage": float(parsed / visible),
        "surface_sha256": pooled_psha,
        "raw_surface_sha256": pooled_rsha,
        "per_manuscript": per_manuscript,
        "fold_counts": fold_counts,
        "line_count": len(lines),
        "X": X,
        "token_folds": token_folds,
        "pos_id": pos_id,
        "padded": padded,
        "line_mask": line_mask,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (6, 7):
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT J REP OUTPUT_JSON [--verify-only]")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    j = int(argv[3])
    rep = int(argv[4])
    out = Path(argv[5]).resolve()
    verify_only = len(argv) == 7 and argv[6] == "--verify-only"
    if len(argv) == 7 and not verify_only:
        raise SystemExit("only optional flag is --verify-only")
    if j not in range(31) or rep not in range(5):
        raise SystemExit("J must be 0..30 and REP must be 0..4")

    static = verify_static_authorities()
    frozen = load_d0_case(j, rep)
    baseline = load_b2_baseline(rep)
    d = build_pt_dataset(crem, nai, j, rep, frozen)

    if verify_only:
        result = {
            "schema": "issue72-v2-stage-d1-pt-pretarget-verify-v1",
            "status": "STAGE_D1_PT_RECONSTRUCTION_VERIFIED_TARGET_BLIND",
            "j": j,
            "rep": rep,
            "static_authority": static,
            "surface": {
                "primary_sha256": d["surface_sha256"],
                "raw_sha256": d["raw_surface_sha256"],
                "visible_tokens": d["visible"],
                "parsed_tokens": d["parsed"],
                "coverage": d["coverage"],
                "fold_parsed_tokens": d["fold_counts"],
            },
            "baseline_B2_loaded_without_rescoring": baseline,
            "target_access": {
                "target_loader_called": False,
                "pair_Q_computed": False,
                "residual_Z_computed": False,
                "target_correlation_computed": False,
            },
        }
    else:
        targets, target_authority = b1.t68.load_target_references()
        real_q = b1.t68.q_views_candidate(d, d["X"], True)
        namespace = f"issue72v2:stageD:PT:j{j}:rep{rep}:reference"
        scored = b1.calibration(d, real_q, targets, namespace)
        rz = float(scored["topology"]["ZL3b"]["pearson"])
        ri = float(scored["topology"]["IT2a"]["pearson"])
        result = {
            "schema": "issue72-v2-stage-d1-pt-per-case-r1-v1",
            "status": "STAGE_D1_PT_R1_TARGET_SCORED",
            "scientific_role": "TOTAL_EFFECT_THROUGH_FULL_PUBLISHED_PIPELINE",
            "j": j,
            "rep": rep,
            "reference_namespace": namespace,
            "n_reference": N_REF,
            "static_authority": static,
            "surface": {
                "primary_sha256": d["surface_sha256"],
                "raw_sha256": d["raw_surface_sha256"],
                "visible_tokens": d["visible"],
                "parsed_tokens": d["parsed"],
                "coverage": d["coverage"],
                "fold_parsed_tokens": d["fold_counts"],
                "line_count_with_parsed_token": d["line_count"],
                "per_manuscript": d["per_manuscript"],
            },
            "target_authority": target_authority,
            "PT_R1": scored,
            "baseline_B2": baseline,
            "delta_R_randomized_minus_baseline": {
                "ZL3b": float(rz - baseline["R_ZL3b"]),
                "IT2a": float(ri - baseline["R_IT2a"]),
            },
            "decision_policy": {
                "hard_intervention_threshold_applied": False,
                "readings_averaged": False,
                "coverage_gate_applied": False,
                "baseline_rescored": False,
            },
        }

    raw = canonical_json_bytes(result) + b"\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    visible = {
        "status": result["status"],
        "j": j,
        "rep": rep,
        "surface_sha256": d["surface_sha256"],
        "coverage": d["coverage"],
        "baseline_B2": baseline,
        "output_sha256": sha256_bytes(raw),
    }
    if not verify_only:
        visible["PT_R1"] = {
            "E": result["PT_R1"]["residual_energy"],
            "W": result["PT_R1"]["reliability"]["median"],
            "R_ZL3b": result["PT_R1"]["topology"]["ZL3b"]["pearson"],
            "R_IT2a": result["PT_R1"]["topology"]["IT2a"]["pearson"],
        }
        visible["delta_R"] = result["delta_R_randomized_minus_baseline"]
    print(json.dumps(visible, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
