#!/usr/bin/env python3
"""Issue #68 Stage-0 authority/replayability audit.

This executable MUST NOT score a new joint-tournament candidate. It audits only
already-frozen repository authorities, common-fold compatibility, metric
responsibility boundaries, and structural reversibility facts needed before a
separate target PLAN_A can be frozen.
"""
from __future__ import annotations

import importlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = ROOT / "experiments"
PHASE62 = EXPERIMENTS / "phase62"

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_CREMMA_COMMIT = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_NAIBBE_COMMIT = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
EXPECTED_NAIBBE_ENCRYPT_BLOB = "b566ad82e4b6ff0782ecdddebf77718dac44f292"
EXPECTED_NAIBBE_TABLE_BLOB = "5cd34fb81d80faf3b4d57dbf1719c05ffde25302"
EXPECTED_NAIBBE_DECRYPT_BLOB = "b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b"
EXPECTED_C0_TRANSFORMS = (
    "C0-0_identity",
    "C0-1_reverse",
    "C0-2_allography2",
    "C0-3_allography3",
    "C0-4_digraph",
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_folds(folds: Iterable[Iterable[int]]) -> list[list[int]]:
    return [sorted(int(x) for x in fold) for fold in folds]


def parse_len_units(payload: str) -> list[str]:
    """Invert Phase62C's encoded_atom length-delimited payload."""
    out: list[str] = []
    i = 0
    while i < len(payload):
        m = re.match(r"(\d+):", payload[i:])
        if not m:
            raise AssertionError(f"malformed encoded_atom payload at {payload[i:]!r}")
        n = int(m.group(1))
        i += len(m.group(0))
        unit = payload[i : i + n]
        if len(unit) != n:
            raise AssertionError("encoded_atom payload shorter than declared length")
        out.append(unit)
        i += n
    return out


def inverse_token(tok: Sequence[str], transform: str) -> tuple[str, ...]:
    if transform == "C0-0_identity":
        return tuple(tok)
    if transform == "C0-1_reverse":
        return tuple(reversed(tok))

    recovered: list[str] = []
    if transform == "C0-2_allography2":
        for atom in tok:
            if atom.startswith("A2I"):
                units = parse_len_units(atom[3:])
            elif atom.startswith("A2N"):
                units = parse_len_units(atom[3:])
            else:
                raise AssertionError(f"bad C0-2 atom {atom!r}")
            if len(units) != 1:
                raise AssertionError("C0-2 atom must contain exactly one source unit")
            recovered.extend(units)
        return tuple(recovered)

    if transform == "C0-3_allography3":
        for atom in tok:
            prefix = next((p for p in ("A3I", "A3M", "A3F") if atom.startswith(p)), None)
            if prefix is None:
                raise AssertionError(f"bad C0-3 atom {atom!r}")
            units = parse_len_units(atom[len(prefix) :])
            if len(units) != 1:
                raise AssertionError("C0-3 atom must contain exactly one source unit")
            recovered.extend(units)
        return tuple(recovered)

    if transform == "C0-4_digraph":
        for atom in tok:
            if atom.startswith("D"):
                units = parse_len_units(atom[1:])
                if len(units) != 2:
                    raise AssertionError("C0-4 D atom must contain two source units")
            elif atom.startswith("S"):
                units = parse_len_units(atom[1:])
                if len(units) != 1:
                    raise AssertionError("C0-4 S atom must contain one source unit")
            else:
                raise AssertionError(f"bad C0-4 atom {atom!r}")
            recovered.extend(units)
        return tuple(recovered)

    raise AssertionError(f"unknown transform {transform}")


def item_signature(item) -> tuple:
    return (
        item.item_id,
        item.document,
        item.leaf,
        tuple(tuple(tuple(tok) for tok in line) for line in item.lines),
    )


def inverse_items(items, transform: str, item_cls):
    return [
        item_cls(
            item_id=it.item_id,
            document=it.document,
            leaf=it.leaf,
            lines=[[inverse_token(tok, transform) for tok in line] for line in it.lines],
        )
        for it in items
    ]


def main() -> int:
    # Import the exact current repository Phase62 implementations. No target data
    # outside already-frozen result files are scored here.
    sys.path.insert(0, str(PHASE62))
    b = importlib.import_module("phase62b_n0")
    c = importlib.import_module("phase62c_c0_a1")

    phase62c = load_json(PHASE62 / "phase62c_c0_a1_results.json")
    phase62p = load_json(PHASE62 / "phase62p_h62p1_results.json")
    issue58d = load_json(
        EXPERIMENTS
        / "occupancy-graph-independent-transcription"
        / "first-reveal"
        / "issue66_independent_residual_results.json"
    )
    phase64_source_audit = (
        EXPERIMENTS / "phase64" / "C1_SOURCE_AUDIT_B.md"
    ).read_text(encoding="utf-8")

    # ----- Frozen source authority -----
    assert phase62c["inputs"]["voynich_git_blob_sha1"] == EXPECTED_ZL3B_BLOB
    assert phase62c["inputs"]["cremma_commit"] == EXPECTED_CREMMA_COMMIT
    assert phase62p["inputs"]["voynich_git_blob_sha1"] == EXPECTED_ZL3B_BLOB
    assert phase62p["inputs"]["cremma_commit"] == EXPECTED_CREMMA_COMMIT
    assert issue58d["sources"]["ZL3b_required_blob"] == EXPECTED_ZL3B_BLOB
    assert EXPECTED_NAIBBE_COMMIT in phase64_source_audit
    assert EXPECTED_NAIBBE_ENCRYPT_BLOB in phase64_source_audit
    assert EXPECTED_NAIBBE_TABLE_BLOB in phase64_source_audit
    assert "references/naibbe_tables.csv" in phase64_source_audit

    # ----- Common physical-leaf fold authority -----
    folds_c = normalize_folds(f["test_leaves"] for f in phase62c["folds"])
    folds_p = normalize_folds(f["test_leaves"] for f in phase62p["folds"])
    folds_r1 = normalize_folds(issue58d["population"]["physical_leaf_folds"])
    assert folds_c == folds_p == folds_r1
    flat = [leaf for fold in folds_c for leaf in fold]
    assert len(flat) == 99
    assert len(set(flat)) == 99

    # ----- Responsibility authority -----
    pairs = issue58d["pairs"]
    expected_pairs = [[i, j] for i in range(12) for j in range(i + 1, 12)]
    assert pairs == expected_pairs
    assert issue58d["parser"]["n_slots"] == 12
    assert issue58d["parser"]["pair_count"] == 66
    assert issue58d["parser"]["primary_policy"] == "min"
    assert issue58d["gate_A_independent_residual_existence"]["supported"] is True
    assert issue58d["overall_classification"] == (
        "INDEPENDENT TRANSCRIPTION REPLICATES RESIDUAL TOKEN-CONSTRUCTION CORE"
    )
    assert phase62p["hypothesis"] == "H62-P1 near-family recurrence-distance profile"
    assert phase62p["scientific_status"] == "H62-P1 prospective reveal complete"
    assert all("S1" in fold["heldout_voynich"] for fold in phase62c["folds"])

    # ----- C0 current-code exact structured reversibility -----
    assert tuple(c.TRANSFORMS) == EXPECTED_C0_TRANSFORMS
    assert tuple(phase62c["inputs"]["C0_transforms"]) == EXPECTED_C0_TRANSFORMS

    fixture = [
        b.Item(
            item_id="synthetic-a",
            document="audit",
            leaf=7,
            lines=[
                [("a", "bc", "æ"), ("x",)],
                [("mn", "o", "p", "qr")],
            ],
        ),
        b.Item(
            item_id="synthetic-b",
            document="audit",
            leaf=12,
            lines=[[("α", "ββ"), ("z", "yy", "w")]],
        ),
    ]
    c0_roundtrips: dict[str, bool] = {}
    for transform in c.TRANSFORMS:
        transformed = c.transform_items(fixture, transform)
        recovered = inverse_items(transformed, transform, b.Item)
        ok = [item_signature(x) for x in recovered] == [item_signature(x) for x in fixture]
        assert ok, f"C0 roundtrip failed for {transform}"
        c0_roundtrips[transform] = ok

    selected_c0 = [f["C0_selected"] for f in phase62c["folds"]]
    assert selected_c0 == ["C0-4_digraph"] * 5

    # Frozen numbers below are READ from accepted result artifacts; they are not
    # re-estimated candidate scores in Stage 0.
    r1_all = issue58d["gate_B_cross_reading_topology"]["ALL"]
    r2 = phase62p["across_fold"]
    r3_target = [fold["heldout_voynich"]["S1"] for fold in phase62c["folds"]]

    out = {
        "stage": "Issue68-Stage0-authority-audit",
        "stage0_classification": "JOINT TOURNAMENT AUTHORITY READY",
        "new_joint_candidate_scores_computed": False,
        "common_fold_authority": {
            "n_folds": 5,
            "n_unique_physical_leaves": 99,
            "folds": folds_c,
            "phase62c_equals_phase62p_equals_issue58d": True,
        },
        "sources": {
            "ZL3b_git_blob_sha1": EXPECTED_ZL3B_BLOB,
            "CREMMA_commit": EXPECTED_CREMMA_COMMIT,
            "Naibbe_commit": EXPECTED_NAIBBE_COMMIT,
            "Naibbe_expected_blobs": {
                "naibbe_v2.py": EXPECTED_NAIBBE_ENCRYPT_BLOB,
                "references/naibbe_tables.csv": EXPECTED_NAIBBE_TABLE_BLOB,
                "decrypt_naibbe.py": EXPECTED_NAIBBE_DECRYPT_BLOB,
            },
        },
        "responsibilities": {
            "R1_token_construction": {
                "status": "REPLAYABLE_WITH_FROZEN_WRAPPER",
                "n_slots": 12,
                "n_edges": 66,
                "parser_policy": "min",
                "accepted_cross_reading_ALL": {
                    "pearson": r1_all["pearson"],
                    "sign_agreement": r1_all["sign_agreement"],
                    "sign_denominator": r1_all["sign_denominator"],
                    "p_R_maxT": r1_all["p_R_maxT"],
                    "p_A_maxT": r1_all["p_A_maxT"],
                },
            },
            "R2_H62": {
                "status": "REPLAY_READY",
                "historical_profile_leader": r2["prospective_profile_leader"],
                "historical_A1_interpretation": r2["A1_prospective_interpretation"],
            },
            "R3_signed_S1": {
                "status": "REPLAY_READY",
                "definition_source": "Phase62C held-out signed S1 projection; preserve sign",
                "historical_heldout_target_by_fold": r3_target,
            },
        },
        "candidate_roles": {
            "N0": {
                "role": "context/control baseline",
                "eligible_decoder": False,
                "eligible_R1_voynich_surface": False,
                "reason": "plain medieval-Latin control, not a 12-slot Voynich-surface mechanism",
            },
            "C0": {
                "role": "exactly reversible synthetic/control family",
                "eligible_decoder": True,
                "eligible_R1_voynich_surface": False,
                "structured_roundtrip_exact": True,
                "roundtrip_by_transform": c0_roundtrips,
                "selected_historical_transform_all_folds": "C0-4_digraph",
                "boundary_side_information_required": False,
            },
            "Naibbe_C1_E0": {
                "role": "published target-aware cipher/decoder challenger",
                "eligible_decoder": True,
                "eligible_R1_voynich_surface": True,
                "published_decoder_exists": True,
                "decoder_file": "decrypt_naibbe.py",
                "closure_target": "normalized plaintext letter stream, with ambiguity/loss reported",
                "exact_original_text_roundtrip": False,
                "losses_before_or_during_encryption": [
                    "original plaintext word boundaries/punctuation removed",
                    "W->UU normalization",
                    "J->I normalization",
                    "K->C normalization",
                    "3 percent stochastic ciphertext-space removal in published primary settings",
                ],
                "free_hidden_side_information_allowed": False,
            },
            "A1_A1R1": {
                "role": "Voynich-surface generator comparator",
                "eligible_decoder": False,
                "eligible_R1_voynich_surface": True,
                "decoder_claim_prohibited": True,
                "target_information_access_must_be_charged": True,
            },
        },
        "pre_target_corrections": {
            "C0_boundary_claim": (
                "CORRECTED: current Phase62C C0 transforms preserve item/line/token structure; "
                "C0-4 is length-delimited and exactly structured-reversible without boundary side-info."
            ),
            "Naibbe_decoder_claim": (
                "CORRECTED: decrypt_naibbe.py exists at the pinned Phase64B Naibbe commit; "
                "decoder-role evaluation is permitted, while original orthography/boundaries remain lossy."
            ),
        },
        "target_firewall": {
            "PLAN_A_present_or_executed_here": False,
            "target_candidate_generated_here": False,
            "new_R1_score_generated_here": False,
            "new_R2_score_generated_here": False,
            "new_R3_score_generated_here": False,
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
