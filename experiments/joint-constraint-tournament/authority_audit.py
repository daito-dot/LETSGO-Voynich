#!/usr/bin/env python3
"""Issue #68 Stage-0 authority/replayability audit.

This script scores no new candidate on a joint Voynich battery. It only audits
already-frozen result authorities, fold compatibility, metric interfaces,
historical candidate roles, and structural reversibility properties.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
ROOT = EXPERIMENTS.parent
PHASE62 = EXPERIMENTS / "phase62"
PHASE64 = EXPERIMENTS / "phase64"

sys.path.insert(0, str(PHASE62))
import phase62b_n0 as b  # noqa: E402
import phase62c_c0_a1 as c  # noqa: E402
import phase62p_h62p1 as p  # noqa: E402

EXPECTED = {
    "zl_blob": "2a4533ab9bdfa85db9bad602d590978953055df1",
    "cremma_commit": "292525969ad98380b398e6606a9c2a36d51913ae",
    "h62_first_reveal_sha256": "0e1b687ab73efbc494834f49398ed474230f47bcde4cf4dbcaa46631efd75264",
    "issue58c_raw_sha256": "fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d",
    "issue58d_raw_sha256": "f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6",
    "naibbe_commit": "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2",
    "naibbe_py_blob": "b566ad82e4b6ff0782ecdddebf77718dac44f292",
    "naibbe_table_blob": "5cd34fb81d80faf3b4d57dbf1719c05ffde25302",
}

D_RE = re.compile(r"D(\d+):([A-Za-z0-9_-]+)")
S_RE = re.compile(r"S(\d+):([A-Za-z0-9_-]+)")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_b64(s: str) -> str:
    pad = "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode((s + pad).encode("ascii")).decode("utf-8")


def decode_d_atom(atom: str) -> str:
    m = D_RE.fullmatch(atom)
    if not m:
        raise RuntimeError(f"not a D atom: {atom!r}")
    n = int(m.group(1))
    value = decode_b64(m.group(2))
    if len(value) != n:
        raise RuntimeError(f"D atom length mismatch: {atom!r}")
    return value


def decode_d_stream(payload: str):
    out = []
    pos = 0
    while pos < len(payload):
        m = D_RE.match(payload, pos)
        if not m:
            raise RuntimeError(f"cannot parse D stream at {pos}: {payload!r}")
        atom = m.group(0)
        out.append(decode_d_atom(atom))
        pos = m.end()
    return out


def decode_s_atom(atom: str):
    m = S_RE.fullmatch(atom)
    if not m:
        raise RuntimeError(f"not an S atom: {atom!r}")
    n = int(m.group(1))
    payload = decode_b64(m.group(2))
    if len(payload) != n:
        raise RuntimeError(f"S atom length mismatch: {atom!r}")
    return decode_d_stream(payload)


def decode_c0_stream(item: b.Item, transform: str):
    """Recover source glyph stream per line; token boundaries when preserved."""
    line_streams = []
    line_tokens = []
    for line in item.lines:
        decoded_tokens = []
        if transform == "C0-1_identity":
            for tok in line:
                decoded_tokens.append([decode_d_atom(u) for u in tok])
        elif transform == "C0-2_singleton":
            for tok in line:
                if len(tok) != 1:
                    raise RuntimeError("C0-2 output token must have one unit")
                decoded_tokens.append(decode_s_atom(tok[0]))
        elif transform == "C0-3_reversed":
            for tok in line:
                decoded_tokens.append([decode_d_atom(u) for u in reversed(tok)])
        elif transform == "C0-4_digraph":
            stream = [decode_d_atom(u) for tok in line for u in tok]
            line_streams.append(stream)
            line_tokens.append(None)
            continue
        else:
            raise RuntimeError(transform)
        line_tokens.append(decoded_tokens)
        line_streams.append([u for tok in decoded_tokens for u in tok])
    return line_streams, line_tokens


def c0_reversibility_audit():
    source = b.Item(
        item_id="synthetic",
        document="synthetic",
        lines=[
            [tuple("ab"), tuple("c"), tuple("dé")],
            [tuple("xy"), tuple("zq")],
        ],
        leaf=1,
    )
    source_streams = [[u for tok in line for u in tok] for line in source.lines]
    source_tokens = [[[u for u in tok] for tok in line] for line in source.lines]
    out = {}
    for transform in c.C0_TRANSFORMS:
        transformed = c.transform_items([source], transform)[0]
        streams, tokens = decode_c0_stream(transformed, transform)
        stream_exact = streams == source_streams
        boundary_exact = tokens == source_tokens if transform != "C0-4_digraph" else False
        if not stream_exact:
            raise RuntimeError(f"C0 stream closure failed for {transform}")
        if transform != "C0-4_digraph" and not boundary_exact:
            raise RuntimeError(f"C0 boundary closure failed for {transform}")
        out[transform] = {
            "glyph_stream_exact_without_side_info": stream_exact,
            "source_token_boundaries_exact_without_side_info": boundary_exact,
            "structured_plaintext_closure_status": (
                "EXACT"
                if boundary_exact
                else "REQUIRES_SOURCE_TOKEN_BOUNDARY_SIDE_INFO"
            ),
        }
    return out


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def result_authorities():
    c_res_path = PHASE62 / "phase62c_c0_a1_results.json"
    p_res_path = PHASE62 / "phase62p_h62p1_results.json"
    n_res_path = PHASE62 / "phase62b_n0_results.json"
    naibbe_path = PHASE64 / "phase64b_science_results.json"
    d_path = EXPERIMENTS / "occupancy-graph-independent-transcription" / "first-reveal" / "issue66_independent_residual_results.json"

    c_res = load_json(c_res_path)
    p_res = load_json(p_res_path)
    n_res = load_json(n_res_path)
    naibbe = load_json(naibbe_path)
    issue58d = load_json(d_path)

    if p_res["source"]["voynich_blob"] != EXPECTED["zl_blob"]:
        raise RuntimeError("H62 ZL source authority mismatch")
    if p_res["source"]["cremma_commit"] != EXPECTED["cremma_commit"]:
        raise RuntimeError("H62 CREMMA authority mismatch")
    if issue58d["overall_classification"] != "INDEPENDENT TRANSCRIPTION REPLICATES RESIDUAL TOKEN-CONSTRUCTION CORE":
        raise RuntimeError("#58D classification mismatch")
    if sha256_file(d_path) != EXPECTED["issue58d_raw_sha256"]:
        raise RuntimeError("#58D raw SHA mismatch")
    if len(issue58d["pairs"]) != 66:
        raise RuntimeError("#58D pair-count mismatch")

    folds_c = [row["test_leaves"] for row in c_res["folds"]]
    folds_p = [row["test_leaves"] for row in p_res["folds"]]
    folds_n = [row["test_leaves"] for row in n_res["folds"]]
    if folds_c != folds_p or folds_c != folds_n:
        raise RuntimeError("Phase62 physical-leaf fold authority mismatch")

    h62 = p_res["summary"]["H62P1"]
    if h62["selected_model"] != "A1" or h62["D_profile_unique_fold_wins"] != 5 or h62["C_short_unique_fold_wins"] != 5:
        raise RuntimeError("unexpected frozen H62 leader")

    s1_targets = [float(row["heldout_target"]["S1"]) for row in c_res["folds"]]
    selected_c0 = [row["selected_c0"] for row in c_res["folds"]]
    if selected_c0 != ["C0-4_digraph"] * 5:
        raise RuntimeError(f"unexpected historical selected C0: {selected_c0}")

    return {
        "R1_token_construction": {
            "authority": "Issue58C + Issue58D exact first reveals",
            "issue58d_result_path": str(d_path.relative_to(ROOT)),
            "issue58d_raw_sha256": sha256_file(d_path),
            "issue58d_pair_count": len(issue58d["pairs"]),
            "pooled_ZL_IT_pearson": issue58d["gate_B_cross_reading_topology"]["ALL"]["pearson"],
            "pooled_ZL_IT_sign_agreement": issue58d["gate_B_cross_reading_topology"]["ALL"]["sign_agreement"],
            "status": "REPLAYABLE_WITH_FROZEN_WRAPPER",
            "reason": "historical scorer is authoritative; tournament needs a candidate-output adapter and candidate-owned line-local null calibration without changing the 66-edge definition",
        },
        "R2_H62": {
            "authority_result_path": str(p_res_path.relative_to(ROOT)),
            "result_file_sha256_current_main": sha256_file(p_res_path),
            "frozen_first_reveal_sha256": EXPECTED["h62_first_reveal_sha256"],
            "folds": folds_p,
            "selected_model": h62["selected_model"],
            "mean_D_profile": h62["mean_D_profile"],
            "median_D_profile": h62["median_D_profile"],
            "D_profile_unique_fold_wins": h62["D_profile_unique_fold_wins"],
            "mean_abs_C_short_diff": h62["mean_abs_C_short_diff"],
            "C_short_unique_fold_wins": h62["C_short_unique_fold_wins"],
            "status": "REPLAY_READY",
            "candidate_interface": "phase62p_h62p1.raw_profile(candidate_items, label) + frozen profile_distance/c_short_diff against held-out Voynich fold profile",
        },
        "R3_S1": {
            "authority_code": "experiments/phase62/phase62b_n0.py",
            "authority_result_path": str(c_res_path.relative_to(ROOT)),
            "result_file_sha256_current_main": sha256_file(c_res_path),
            "folds": folds_c,
            "heldout_target_S1_by_fold": s1_targets,
            "mean_heldout_target_S1": float(sum(s1_targets) / len(s1_targets)),
            "status": "REPLAY_READY",
            "candidate_interface": "training_sd/contrasts define frozen training direction; s1_projection(candidate_items, frozen_training_sd, frozen_direction) scores held-out candidate output",
        },
        "B2_Naibbe": {
            "authority_result_path": str(naibbe_path.relative_to(ROOT)),
            "result_file_sha256_current_main": sha256_file(naibbe_path),
            "frozen_classification": naibbe.get("classification"),
            "external_commit": EXPECTED["naibbe_commit"],
            "external_py_blob": EXPECTED["naibbe_py_blob"],
            "external_table_blob": EXPECTED["naibbe_table_blob"],
        },
    }


def complexity_schema():
    return {
        "version": "issue68-stage0-v1",
        "principle": "record access and degrees of freedom dimensionally before choosing any scalar penalty; target plan may freeze ceilings/MDL only before candidate scoring",
        "required_fields": {
            "role": ["control/null", "surface generator only", "reversible transform / decoder candidate"],
            "free_scalar_parameters": "integer plus names",
            "learned_table_cells": "integer plus table identities",
            "fixed_external_table_cells": "integer plus source authority",
            "training_vocabulary_types": "integer or per-fold counts",
            "empirical_target_token_inventory_supplied": "boolean",
            "state_space": "explicit finite states or description",
            "memory_order": "tokens/lines/paragraphs of history used",
            "section_conditioned_parameters": "count",
            "paragraph_conditioned_parameters": "count",
            "heldout_layout_access": "exact fields supplied at generation/scoring time",
            "heldout_target_statistic_access": "must be false for confirmatory target",
            "external_plaintext_source": "authority/corpus if applicable",
            "candidate_specific_preprocessing": "complete frozen rules",
            "decoder_side_information": "what must accompany ciphertext; later target plan must quantify/ceiling",
            "per_item_adaptation": "boolean; normally forbidden",
        },
        "no_scalar_weighting_frozen_in_stage0": True,
    }


def candidate_roles(c0_audit):
    return {
        "B0_N0": {
            "role": "control/null",
            "joint_competitive_eligibility": False,
            "R1_12slot_surface": "INAPPLICABLE_SOURCE_NATIVE_LATIN",
            "R2_H62": "REPLAY_READY",
            "R3_S1": "REPLAY_READY",
            "reversibility": "not an encoding/decoder candidate",
            "target_access": "none beyond common scoring target",
        },
        "B1_C0_4_digraph": {
            "role": "reversible transform / decoder candidate",
            "joint_competitive_eligibility": False,
            "reason": "historical control encoding is not an EVA/12-slot Voynich-surface candidate, so it is a responsibility anchor rather than a joint explanation",
            "R1_12slot_surface": "NOT_COMMON_VOYNICH_ALPHABET",
            "R2_H62": "REPLAY_READY",
            "R3_S1": "REPLAY_READY",
            "reversibility": c0_audit["C0-4_digraph"],
            "decoder_side_information": "source token-boundary mask required for exact structured plaintext closure; glyph stream is exact without it",
        },
        "B2_Naibbe_C1_E0": {
            "role": "reversible transform / decoder candidate",
            "joint_competitive_eligibility": True,
            "R1_12slot_surface": "POTENTIALLY_SCORABLE_VOYNICH_LIKE_OUTPUT",
            "R2_H62": "HISTORICAL_REPLAY_READY",
            "R3_S1": "HISTORICAL_REPLAY_READY",
            "reversibility": "REPLAYABLE_WITH_FROZEN_WRAPPER",
            "decoder_issue": "pinned published script exposes encryption but no explicit decrypt function; primary respaced view removes 3% output spaces, so exact closure must preserve/charge sufficient token-boundary side information or prove self-decoding before promotion",
            "fixed_external_codebook": "6 tables x 3 states x alphabet cells from pinned published CSV; target-aware external design, not fitted by this project",
        },
        "B3_A1_A1_R1": {
            "role": "surface generator only",
            "joint_competitive_eligibility": True,
            "R1_12slot_surface": "SCORABLE_VOYNICH_VOCAB_OUTPUT",
            "R2_H62": "REPLAY_READY_AND_HISTORICAL_LEADER",
            "R3_S1": "REPLAY_READY",
            "reversibility": "NO_DECODER_DEFINED",
            "information_access": {
                "training_side": [
                    "empirical Voynich training vocabulary",
                    "training edit1 neighbor graph",
                    "training entry-shape scores",
                    "historically selected per-fold A1 parameters",
                ],
                "heldout_side": [
                    "true held-out paragraph count",
                    "true held-out line count per paragraph",
                    "true held-out token count per line",
                ],
                "not_supplied": "held-out token identities",
            },
            "complexity_warning": "must not be compared to reversible transforms as if information access were equal",
        },
    }


def output_contract():
    return {
        "version": "issue68-stage0-v1",
        "item": {
            "required": ["item_id", "document_or_page", "ordered_lines"],
            "optional_but_required_for_voynich_leaf_holdout": ["physical_leaf"],
            "line": "ordered list of tokens",
            "token": "ordered glyph-unit sequence plus a deterministic string serialization for scorers that use edit1",
        },
        "responsibility_requirements": {
            "R1": [
                "ordered physical lines",
                "token strings in a prospectively frozen 12-slot-compatible scoring representation",
                "candidate-owned line-local null calibration",
                "pooled ALL scoring does not require Currier/section labels",
            ],
            "R2": ["paragraph/item boundaries", "ordered lines", "token unit sequences/strings"],
            "R3": ["paragraph boundaries", "at least 3 ordered physical lines when eligible", "first-five-token feature access"],
            "reversible_candidate": ["source plaintext identity", "ciphertext output", "decoder side-information record", "decode/re-encode closure record"],
        },
        "recommended_R1_tournament_object": "pooled ALL residual existence under candidate-owned line-local null plus complete-66 topology agreement against both frozen ZL3b and IT2a references; no candidate-driven edge selection",
        "common_holdout_principle": "reuse one physical-leaf fold authority where applicable; keep each responsibility's historical eligibility inside held-out leaves instead of forcing a tiny token-level intersection",
    }


def main():
    authorities = result_authorities()
    c0_audit = c0_reversibility_audit()
    roles = candidate_roles(c0_audit)
    out = {
        "issue": 68,
        "phase": "joint-constraint-tournament-stage0",
        "new_joint_candidate_scores_computed": False,
        "authorities": authorities,
        "c0_reversibility_audit": c0_audit,
        "candidate_roles": roles,
        "complexity_accounting_schema": complexity_schema(),
        "candidate_output_contract": output_contract(),
        "fold_compatibility": {
            "phase62_R2_R3_exact_same_physical_leaf_folds": True,
            "R1_58C_58D_uses_same_99_leaf_stride5_authority": True,
            "recommended_harmonization": "common physical-leaf folds with responsibility-specific historical eligibility; do not force token-level population intersection",
        },
        "stage0_preliminary_disposition": "JOINT TOURNAMENT AUTHORITY READY",
        "remaining_external_checks_before_finalizing_stage0": [
            "replay Phase62C/P on frozen ZL3b + CREMMA and compare with committed results",
            "verify pinned Naibbe source blobs/defaults and confirm no published explicit decrypt path",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
