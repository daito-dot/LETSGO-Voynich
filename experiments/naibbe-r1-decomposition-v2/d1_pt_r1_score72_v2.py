#!/usr/bin/env python3
"""Issue #72 V2 Stage D1 PT full-pipeline R1 scorer.

For one prospectively frozen PT assignment x historical RNG block, regenerate
exactly the D0 PT surface, prove byte-identity at the primary/raw surface level,
and only then (unless --verify-only) compute the frozen R1 measurement against
ZL3b and IT2a.

Usage:
  python d1_pt_r1_score72_v2.py CREMMA_ROOT NAIBBE_ROOT J REP OUTPUT_JSON [--verify-only]
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import b1_r1_calibration72_v2 as b1  # noqa: E402
import d0_pt_support72_v2 as d0  # noqa: E402

STAGE_D_PLAN_COMMIT = "c45c67a665a7e4ad24c1d2706f83c65931d950a9"
D0_AGG_PATH = HERE / "stage-d0-pt" / "stage_d0_pt_support_aggregate.json"
D0_AGG_SHA256 = "e3039ed40f72e44cc4964efab50d70bc1b113859c77e23ccc97934bb29edb9b8"
D0_REBIND_PATH = HERE / "STAGE_D0_PT_AUTHORITY_REBIND_VALIDATION.json"
D0_REBIND_SHA256 = "cb80833b426d6d9b4d1f307961d862fe02140fcf8f593f870fb3080a39bfc2a0"
D0_INDIV_DIR = HERE / "stage-d0-pt" / "individual"
PT_AUTHORITY_SHA256 = "703991a4b176e78ea18c30210ec730187b446c0c8b14052fc2d25e4a8d8f86e4"
SOURCE_FULL_B0_SHA256 = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
SOURCE_B0_ARTIFACT_ID = 9783720673
J_VALUES = tuple(range(31))
REPS = tuple(range(5))
MANUSCRIPTS = d0.MANUSCRIPTS
N_REF = 1000
N_EDGES = 66
N_FOLDS = 4


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_frozen_d0(j: int, rep: int) -> tuple[dict, dict]:
    if sha256_file(D0_AGG_PATH) != D0_AGG_SHA256:
        raise RuntimeError("D0 aggregate SHA changed")
    if sha256_file(D0_REBIND_PATH) != D0_REBIND_SHA256:
        raise RuntimeError("D0 authority-rebind validation SHA changed")

    reb = json.loads(D0_REBIND_PATH.read_text(encoding="utf-8"))
    if reb["status"] != "D0_COMPLETE_POPULATION_VALIDATED_UNDER_COMPACT_PT_AUTHORITY":
        raise RuntimeError("D0 rebind status changed")
    if reb["licensed_action"] != "REUSE_EXISTING_155_D0_SURFACES_AS_FROZEN_SUPPORT_AUTHORITY_NO_RECOMPUTATION":
        raise RuntimeError("D0 rebind licensed action changed")
    if reb["R1_computed"] or reb["target_loaded"] or reb["scientific_intervention_changed"]:
        raise RuntimeError("D0 rebind firewall changed")
    if reb["compact_pt_authority_sha256"] != PT_AUTHORITY_SHA256:
        raise RuntimeError("D0 compact PT authority changed")
    if reb["source_full_b0_sha256"] != SOURCE_FULL_B0_SHA256:
        raise RuntimeError("D0 source full B0 authority changed")

    agg = json.loads(D0_AGG_PATH.read_text(encoding="utf-8"))
    if agg["status"] != "STAGE_D0_COMPLETE_PT_SUPPORT_POPULATION_FROZEN_TARGET_BLIND":
        raise RuntimeError("D0 aggregate status changed")
    pop = agg["population"]
    if not (pop["complete_population"] and pop["no_drops"] and pop["no_rerolls"] and pop["total_results"] == 155):
        raise RuntimeError("D0 complete-population invariant changed")
    if not agg["target_firewall"]["all_assignment_target_access_false"] or agg["target_firewall"]["R1_target_scored"]:
        raise RuntimeError("D0 aggregate target firewall changed")

    matches = [x for x in agg["results"] if int(x["j"]) == j and int(x["rep"]) == rep]
    if len(matches) != 1:
        raise RuntimeError(f"D0 aggregate assignment lookup failed j{j} rep{rep}: {len(matches)}")
    summary = matches[0]
    path = D0_INDIV_DIR / f"PT_j{j}_rep{rep}.json"
    got_indiv = sha256_file(path)
    if got_indiv != summary["json_sha256"]:
        raise RuntimeError(f"D0 individual SHA mismatch j{j} rep{rep}: {got_indiv}")
    frozen = json.loads(path.read_text(encoding="utf-8"))
    if frozen["status"] != "STAGE_D0_PT_ASSIGNMENT_SUPPORT_FROZEN_TARGET_BLIND":
        raise RuntimeError("D0 individual status changed")
    if frozen["assignment"]["j"] != j or frozen["assignment"]["rep"] != rep:
        raise RuntimeError("D0 individual assignment identity changed")
    if frozen["stage_d_plan_commit"] != STAGE_D_PLAN_COMMIT:
        raise RuntimeError("D0 individual plan authority changed")
    if not frozen["paired_baseline"]["exact_stage_b0_replay"]:
        raise RuntimeError("D0 baseline replay was not exact")
    if not frozen["pt_surface"]["line_invariants_all_true"]:
        raise RuntimeError("D0 PT line invariants were not all true")
    if any(frozen["target_access"].values()):
        raise RuntimeError("D0 individual target firewall changed")
    if frozen["implementation_authority"]["stage_b0_support_json_sha256"] != SOURCE_FULL_B0_SHA256:
        raise RuntimeError("D0 original B0 authority identity changed")
    return frozen, summary


def dataset_from_primary(pooled_items, parser, rep: int) -> dict:
    lines = []
    visible = parsed = 0
    per_ms_counts = {m: {"visible": 0, "parsed": 0} for m in MANUSCRIPTS}

    for item in pooled_items:
        if item.document not in MANUSCRIPTS:
            raise RuntimeError(f"unexpected PT document: {item.document}")
        fold = MANUSCRIPTS.index(item.document)
        for line_index, toks in enumerate(item.lines):
            n_visible = len(toks)
            visible += n_visible
            per_ms_counts[item.document]["visible"] += n_visible
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
                per_ms_counts[item.document]["parsed"] += 1
            if rows:
                lines.append({
                    "fold": fold,
                    "manuscript": item.document,
                    "item_id": item.item_id,
                    "line_index": int(line_index),
                    "occ": np.stack(rows),
                    "positions": tuple(positions),
                })

    if not lines or parsed == 0:
        raise RuntimeError("PT R1 dataset has no parser-accepted lines")
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
    return {
        "rep": int(rep),
        "visible": int(visible),
        "parsed": int(parsed),
        "coverage": float(parsed / visible),
        "fold_counts": fold_counts,
        "line_count": len(lines),
        "per_ms_counts": per_ms_counts,
        "X": X,
        "token_folds": token_folds,
        "pos_id": pos_id,
        "padded": padded,
        "line_mask": line_mask,
    }


def regenerate_and_verify(crem: Path, nai: Path, j: int, rep: int, frozen: Mapping, summary: Mapping) -> tuple[dict, dict]:
    auth = d0.b0.authority(crem, nai)
    b0_authority = d0.load_b0_authority()
    module = d0.b0.n64.load_naibbe(nai)
    original_map = dict(module.placeholder_to_glyph)
    parser = d0.b0.e.SlotParser()
    parser_validation = d0.b0.e.validate_parser(parser)
    sources = {
        name: d0.b0.b.parse_latin_manuscript(crem, name, rel)
        for name, rel in d0.b0.b.PRIMARY_MANUSCRIPTS.items()
    }

    baseline = d0.verify_baseline(module, sources, original_map, parser, rep, b0_authority)
    if baseline["primary_pooled_surface_sha256"] != frozen["paired_baseline"]["primary_pooled_surface_sha256"]:
        raise RuntimeError("D1 paired baseline primary replay mismatch")
    if baseline["raw_pooled_surface_sha256"] != frozen["paired_baseline"]["raw_pooled_surface_sha256"]:
        raise RuntimeError("D1 paired baseline raw replay mismatch")

    pooled_primary = []
    pooled_raw = []
    per_ms = {}
    for mi, manuscript in enumerate(MANUSCRIPTS):
        seed = 6480000 + 100 * mi + rep
        primary, raw, diag = d0.encrypt_pt_manuscript(
            module, sources[manuscript], manuscript, original_map, seed, j
        )
        psha = d0.b0.surface_sha(primary)
        rsha = d0.b0.surface_sha(raw)
        support = d0.b0.parser_support(primary, parser)
        expected = frozen["pt_surface"]["per_manuscript"][manuscript]
        if psha != expected["primary_surface_sha256"]:
            raise RuntimeError(f"D1 PT primary surface mismatch {manuscript}")
        if rsha != expected["raw_surface_sha256"]:
            raise RuntimeError(f"D1 PT raw surface mismatch {manuscript}")
        for key in ("visible_tokens", "accepted_tokens"):
            if int(support[key]) != int(expected["support"][key]):
                raise RuntimeError(f"D1 PT support mismatch {manuscript} {key}")
        if int(diag["ambiguity_retries"]) != int(expected["generation_diagnostics"]["ambiguity_retries"]):
            raise RuntimeError(f"D1 PT retry mismatch {manuscript}")
        if diag["line_invariant_records_sha256"] != expected["generation_diagnostics"]["line_invariant_records_sha256"]:
            raise RuntimeError(f"D1 PT line invariant digest mismatch {manuscript}")
        pooled_primary.extend(primary)
        pooled_raw.extend(raw)
        per_ms[manuscript] = {
            "seed": int(seed),
            "primary_surface_sha256": psha,
            "raw_surface_sha256": rsha,
            "visible_tokens": int(support["visible_tokens"]),
            "parsed_tokens": int(support["accepted_tokens"]),
            "coverage": float(support["coverage"]),
            "ambiguity_retries": int(diag["ambiguity_retries"]),
            "line_invariant_records_sha256": diag["line_invariant_records_sha256"],
        }

    pooled_psha = d0.b0.surface_sha(pooled_primary)
    pooled_rsha = d0.b0.surface_sha(pooled_raw)
    pooled_support = d0.b0.parser_support(pooled_primary, parser)
    if pooled_psha != frozen["pt_surface"]["primary_pooled_surface_sha256"] or pooled_psha != summary["primary_pooled_surface_sha256"]:
        raise RuntimeError("D1 PT pooled primary surface mismatch")
    if pooled_rsha != frozen["pt_surface"]["raw_pooled_surface_sha256"] or pooled_rsha != summary["raw_pooled_surface_sha256"]:
        raise RuntimeError("D1 PT pooled raw surface mismatch")
    if int(pooled_support["visible_tokens"]) != int(summary["visible_tokens"]):
        raise RuntimeError("D1 PT pooled visible mismatch")
    if int(pooled_support["accepted_tokens"]) != int(summary["accepted_tokens"]):
        raise RuntimeError("D1 PT pooled accepted mismatch")

    d = dataset_from_primary(pooled_primary, parser, rep)
    if d["visible"] != pooled_support["visible_tokens"] or d["parsed"] != pooled_support["accepted_tokens"]:
        raise RuntimeError("D1 dataset support disagrees with frozen D0 support")
    expected_fold_counts = [
        int(frozen["pt_surface"]["per_manuscript"][m]["support"]["accepted_tokens"])
        for m in MANUSCRIPTS
    ]
    if d["fold_counts"] != expected_fold_counts:
        raise RuntimeError(f"D1 PT fold-count mismatch: {d['fold_counts']} != {expected_fold_counts}")

    audit = {
        "authority": auth,
        "parser_validation": parser_validation,
        "d0_individual_sha256": str(summary["json_sha256"]),
        "d0_aggregate_sha256": D0_AGG_SHA256,
        "d0_authority_rebind_validation_sha256": D0_REBIND_SHA256,
        "compact_pt_authority_sha256": PT_AUTHORITY_SHA256,
        "source_full_b0_sha256": SOURCE_FULL_B0_SHA256,
        "source_b0_artifact_id": SOURCE_B0_ARTIFACT_ID,
        "paired_baseline_exact_replay": True,
        "pt_primary_exact_d0_replay": True,
        "pt_raw_exact_d0_replay": True,
        "pt_support_exact_d0_replay": True,
        "pt_line_invariant_digests_exact_d0_replay": True,
        "primary_pooled_surface_sha256": pooled_psha,
        "raw_pooled_surface_sha256": pooled_rsha,
        "visible_tokens": int(d["visible"]),
        "parsed_tokens": int(d["parsed"]),
        "coverage": float(d["coverage"]),
        "fold_parsed_tokens": d["fold_counts"],
        "line_count_with_parsed_token": int(d["line_count"]),
        "per_manuscript": per_ms,
    }
    return d, audit


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (6, 7):
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT J REP OUTPUT_JSON [--verify-only]")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    j = int(argv[3])
    rep = int(argv[4])
    output = Path(argv[5]).resolve()
    verify_only = len(argv) == 7 and argv[6] == "--verify-only"
    if len(argv) == 7 and not verify_only:
        raise SystemExit("only optional flag is --verify-only")
    if j not in J_VALUES or rep not in REPS:
        raise SystemExit("J must be 0..30 and REP must be 0..4")

    frozen, summary = load_frozen_d0(j, rep)
    d, audit = regenerate_and_verify(crem, nai, j, rep, frozen, summary)

    if verify_only:
        result = {
            "schema": "issue72-v2-stage-d1-pt-surface-preflight-v1",
            "status": "STAGE_D1_PT_SURFACE_REPLAY_VERIFIED_TARGET_BLIND",
            "scientific_role": "TARGET_BLIND_D1_INPUT_REPLAY_PREFLIGHT",
            "stage_d_plan_commit": STAGE_D_PLAN_COMMIT,
            "assignment": {"j": j, "rep": rep},
            "surface_audit": audit,
            "target_access": {
                "target_references_loaded": False,
                "slot_pair_Q_computed": False,
                "residual_Z_computed": False,
                "target_topology_computed": False,
                "R1_target_rank_or_pvalue_computed": False,
            },
        }
    else:
        # First target access occurs only after the exact D0 surface replay gate.
        targets, target_authority = b1.t68.load_target_references()
        real_q = b1.t68.q_views_candidate(d, d["X"], True)
        namespace = f"issue72v2:stageD:PT:j{j}:rep{rep}:reference"
        primary = b1.calibration(d, real_q, targets, namespace)
        result = {
            "schema": "issue72-v2-stage-d1-pt-r1-score-v1",
            "status": "STAGE_D1_PT_R1_FIRST_REVEAL_ASSIGNMENT_SCORED",
            "scientific_role": "FULL_PIPELINE_PLAINTEXT_ORDER_TOTAL_EFFECT_R1_MEASUREMENT",
            "stage_d_plan_commit": STAGE_D_PLAN_COMMIT,
            "assignment": {"j": j, "rep": rep},
            "surface_audit": audit,
            "target_authority": target_authority,
            "measurement": primary,
            "reference_namespace": namespace,
            "n_reference": N_REF,
            "coverage_policy": "CONTINUOUS_DESCRIPTIVE_NO_HARD_CUTOFF",
            "hard_intervention_threshold_applied": False,
            "target_readings_averaged": False,
            "baseline_delta_computed_here": False,
        }

    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "j": j,
        "rep": rep,
        "verify_only": verify_only,
        "surface_sha256": audit["primary_pooled_surface_sha256"],
        "coverage": audit["coverage"],
        "R_ZL3b": None if verify_only else result["measurement"]["topology"]["ZL3b"]["pearson"],
        "R_IT2a": None if verify_only else result["measurement"]["topology"]["IT2a"]["pearson"],
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
