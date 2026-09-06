#!/usr/bin/env python3
"""Issue #115 Phase 4B IT2a P1/P2 first reveal.

Reuses the already-frozen Phase-4A atom model and scoring functions. IT2a
source/event authority is regenerated and checked before any model is fitted.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional, Sequence

HERE = Path(__file__).resolve()
P4A = HERE.parents[1] / "phase4a"
if str(P4A) not in sys.path:
    sys.path.insert(0, str(P4A))
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import phase4a_boundary_gate0 as A  # noqa: E402
import phase4a_boundary_first_reveal as P  # noqa: E402
import phase4b_it2a_gate0 as B  # noqa: E402

SCHEMA = "issue115-phase4b-it2a-first-reveal-v1"
EXPECTED_FOLD_HASH = "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b"
EXPECTED_REAL_HASH = "465c93d24b7b96e5d48d7e31d524f700beff849c9fae49a302a7f4ba0d62f675"
EXPECTED_MID_HASH = "c8c75745d4878f9695868e3797cd23c82ed6eb1aa047dd49194482778c53ad75"
EXPECTED_P2_HASH = "5a74abbbedc46b7dca38e5afbec5707e72a1c67f9becbb4843e7be0ee52c7505"
EXPECTED_COUNTS = {"real_space": 27436, "mid_token": 24239, "p2_real_space": 23379}


def build_authority(it_path: Path, zl_path: Path) -> dict:
    gate = B.audit(it_path, zl_path)
    if not gate["gate_pass"]:
        raise RuntimeError("merged IT2a Gate0 no longer passes")
    if gate["fold_authority"]["identity_sha256"] != EXPECTED_FOLD_HASH:
        raise RuntimeError("IT2a Gate0 fold identity changed")
    if gate["population"]["real_space"] != EXPECTED_COUNTS["real_space"] or gate["population"]["mid_token"] != EXPECTED_COUNTS["mid_token"] or gate["population"]["p2_real_space"] != EXPECTED_COUNTS["p2_real_space"]:
        raise RuntimeError("IT2a Gate0 event counts changed")
    if gate["population"]["event_id_hashes"] != {
        "real_space_sha256": EXPECTED_REAL_HASH,
        "mid_token_sha256": EXPECTED_MID_HASH,
        "p2_real_space_sha256": EXPECTED_P2_HASH,
    }:
        raise RuntimeError("IT2a Gate0 event hashes changed")

    raw = it_path.read_bytes()
    lines = raw.decode("utf-8-sig", errors="strict").splitlines()
    leaf_fold, fold_identity = A.frozen_fold_authority(zl_path)
    currier = A.page_currier_authority(lines)
    tokens, real, mid, p2 = [], [], [], []
    real_ids, mid_ids, p2_ids = [], [], []

    for source_line_no, line in enumerate(lines, start=1):
        m = A.LOCUS_RE.match(line)
        if not m or "P" not in m.group("code"):
            continue
        loc = m.group("loc")
        page = loc.split(".", 1)[0]
        lm = A.LEAF_RE.match(page)
        if not lm:
            continue
        leaf = int(lm.group(1))
        if leaf not in leaf_fold:
            continue
        fold = int(leaf_fold[leaf])
        c = currier.get(page, "UNKNOWN")
        if c not in ("A", "B"):
            c = "UNKNOWN"

        segments, n_dot = A.split_certain_spaces(m.group("body"))
        atoms_by_segment = []
        for si, token in enumerate(segments):
            atoms = A.atomize_clean(token)
            atoms_by_segment.append(atoms)
            if atoms is None:
                continue
            tokens.append({"id": (loc, source_line_no, si), "fold": fold, "currier": c, "atoms": atoms})
            if len(atoms) >= 4:
                cut = len(atoms) // 2
                eid = (loc, source_line_no, si, len(atoms), cut, fold)
                mid.append({"id": eid, "fold": fold, "currier": c, "atoms": atoms, "cut": cut})
                mid_ids.append(eid)

        if n_dot != len(segments) - 1:
            raise RuntimeError(f"dot/segment mismatch at {loc}")
        for bi in range(n_dot):
            left = atoms_by_segment[bi]
            right = atoms_by_segment[bi + 1]
            if left is None or right is None or len(left) < 2 or len(right) < 2:
                continue
            eid = (loc, source_line_no, bi, len(left), len(right), fold)
            ev = {"id": eid, "fold": fold, "currier": c, "left": left, "right": right}
            real.append(ev); real_ids.append(eid)
            if len(left) >= 3 and len(right) >= 3:
                p2.append(ev); p2_ids.append(eid)

    hashes = {
        "fold_identity_sha256": A.sha256_obj(fold_identity),
        "real_space_sha256": A.sha256_obj(real_ids),
        "mid_token_sha256": A.sha256_obj(mid_ids),
        "p2_real_space_sha256": A.sha256_obj(p2_ids),
    }
    expected = {
        "fold_identity_sha256": EXPECTED_FOLD_HASH,
        "real_space_sha256": EXPECTED_REAL_HASH,
        "mid_token_sha256": EXPECTED_MID_HASH,
        "p2_real_space_sha256": EXPECTED_P2_HASH,
    }
    if hashes != expected:
        raise RuntimeError(f"scorer event authority mismatch: {hashes}")
    if {"real_space": len(real), "mid_token": len(mid), "p2_real_space": len(p2)} != EXPECTED_COUNTS:
        raise RuntimeError("scorer event counts mismatch")
    return {"tokens": tokens, "real": real, "mid": mid, "p2": p2, "gate": gate, "hashes": hashes}


def cross_label(it_class: str) -> str:
    if it_class == "SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY":
        return "VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a"
    if it_class in (
        "SPACE MARKS A RESET BUT EXACT CUT IS WEAK",
        "SPACE POSITION IS LOCALLY PRIVILEGED WITHOUT RESET EVIDENCE",
    ):
        return "PARTIAL CROSS-TRANSCRIPTION BOUNDARY REPLICATION"
    if it_class == "VISIBLE SPACE NOT SUPPORTED AS PRODUCTION BOUNDARY":
        return "CROSS-TRANSCRIPTION BOUNDARY REPLICATION FAILS"
    raise RuntimeError(f"unexpected IT2a class: {it_class}")


def run(it_path: Path, zl_path: Path) -> dict:
    auth = build_authority(it_path, zl_path)
    folds, raws = [], []
    for f in range(5):
        row, raw = P.score_fold(f, auth)
        folds.append(row); raws.append(raw)

    real = [x for r in raws for x in r["real_a"]]
    mid = [x for r in raws for x in r["mid_a"]]
    left = [x for r in raws for x in r["p2_left"]]
    right = [x for r in raws for x in r["p2_right"]]
    fold_d = [x["P1"]["D_RESET"] for x in folds]
    fold_l = [x["P2"]["mean_observed_minus_shift_left"] for x in folds]
    fold_r = [x["P2"]["mean_observed_minus_shift_right"] for x in folds]

    d = P.mean(real) - P.mean(mid)
    p1_pos = sum(v > 0 for v in fold_d)
    p1_pass = d > 0 and p1_pos >= 4
    dl, dr = P.mean(left), P.mean(right)
    nl, nr = sum(v < 0 for v in fold_l), sum(v < 0 for v in fold_r)
    left_pass = dl < 0 and nl >= 4
    right_pass = dr < 0 and nr >= 4
    p2_pass = left_pass and right_pass
    it_class = P.classify(p1_pass, p2_pass)

    cagg = {c: {"real_a": [], "mid_a": [], "p2_left": [], "p2_right": []} for c in ("A", "B", "UNKNOWN")}
    for raw in raws:
        for c in cagg:
            for k in cagg[c]:
                cagg[c][k].extend(raw["currier"][c][k])

    return {
        "schema": SCHEMA,
        "phase": "ISSUE115_PHASE4B_IT2A_FIRST_REVEAL",
        "target_reveal": True,
        "authority": {
            "source_sha256": auth["gate"]["source"]["sha256"],
            "source_git_blob_sha1": auth["gate"]["source"]["git_blob_sha1"],
            "fold_identity_sha256": EXPECTED_FOLD_HASH,
            "event_hashes": {
                "real_space_sha256": EXPECTED_REAL_HASH,
                "mid_token_sha256": EXPECTED_MID_HASH,
                "p2_real_space_sha256": EXPECTED_P2_HASH,
            },
            "counts": EXPECTED_COUNTS,
            "gate_reproduced": True,
        },
        "model": {
            "family": "second_order_raw_eva_atom",
            "additive_alpha": P.ALPHA,
            "token_start_context": [P.BOS, P.BOS],
            "stop_probability": False,
            "training": "IT2a four outer-training physical-leaf folds only",
            "zl3b_fitted_counts_or_parameters_transferred": False,
        },
        "folds": folds,
        "primary": {
            "P1": {
                "pooled_n_real": len(real), "pooled_n_mid": len(mid),
                "pooled_mean_A_real": P.mean(real), "pooled_mean_A_mid": P.mean(mid),
                "pooled_D_RESET": d, "D_RESET_by_fold": fold_d,
                "positive_folds": p1_pos, "pass": bool(p1_pass),
            },
            "P2": {
                "pooled_n": len(left),
                "pooled_mean_observed_minus_shift_left": dl,
                "pooled_mean_observed_minus_shift_right": dr,
                "left_by_fold": fold_l, "right_by_fold": fold_r,
                "left_negative_folds": nl, "right_negative_folds": nr,
                "left_pass": bool(left_pass), "right_pass": bool(right_pass), "pass": bool(p2_pass),
            },
        },
        "it2a_classification": it_class,
        "cross_transcription_replication": cross_label(it_class),
        "secondary_non_authoritative": {"currier": P.summarize_by_currier(cagg)},
        "firewall": {
            "zl3b_target_effect_values_used_for_fit_or_selection": False,
            "slotparser_used_for_event_eligibility": False,
            "parameter_search_performed": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
        },
    }


def self_test() -> None:
    assert cross_label("SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY").startswith("VISIBLE-SPACE")
    assert cross_label("VISIBLE SPACE NOT SUPPORTED AS PRODUCTION BOUNDARY").endswith("FAILS")
    P.self_test()
    print("phase4b self-test OK")


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--self-test", action="store_true")
    g.add_argument("--run", nargs=3, metavar=("IT2A", "ZL3B", "OUT"))
    args = ap.parse_args(argv)
    if args.self_test:
        self_test(); return 0
    result = run(Path(args.run[0]).resolve(), Path(args.run[1]).resolve())
    Path(args.run[2]).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"it2a_classification": result["it2a_classification"], "cross_transcription_replication": result["cross_transcription_replication"], "P1": result["primary"]["P1"], "P2": result["primary"]["P2"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
