#!/usr/bin/env python3
"""Issue #115 Phase 4B score-free IT2a boundary support audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Optional, Sequence

HERE = Path(__file__).resolve()
P4A = HERE.parents[1] / "phase4a"
if str(P4A) not in sys.path:
    sys.path.insert(0, str(P4A))
import phase4a_boundary_gate0 as G  # noqa: E402

EXPECTED_IT_SHA256 = "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"
EXPECTED_IT_BLOB = "4d6d3f2537b1f507a257529b49c94af7d6e03446"
EXPECTED_IT_BYTES = 342104
EXPECTED_IT_LINES = 5444
EXPECTED_IT_HEADER = "#=IVTFF EvaT 2.0 M 3"
EXPECTED_FOLD_HASH = "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b"
N_FOLDS = 5


def audit(it_path: Path, zl_path: Path) -> dict:
    raw = it_path.read_bytes()
    lines = raw.decode("utf-8-sig", errors="strict").splitlines()
    src = {
        "filename": it_path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "git_blob_sha1": G.git_blob_sha1(raw),
        "bytes": len(raw),
        "lines": len(lines),
        "header": lines[0].strip() if lines else "",
        "provenance_line": lines[1].strip() if len(lines) > 1 else "",
        "version_line": lines[2].strip() if len(lines) > 2 else "",
    }
    expected = {
        "sha256": EXPECTED_IT_SHA256,
        "git_blob_sha1": EXPECTED_IT_BLOB,
        "bytes": EXPECTED_IT_BYTES,
        "lines": EXPECTED_IT_LINES,
        "header": EXPECTED_IT_HEADER,
    }
    got = {k: src[k] for k in expected}
    if got != expected:
        raise RuntimeError(f"IT2a authority mismatch: {got!r} != {expected!r}")

    leaf_fold, fold_identity = G.frozen_fold_authority(zl_path)
    fold_hash = G.sha256_obj(fold_identity)
    if fold_hash != EXPECTED_FOLD_HASH:
        raise RuntimeError(f"frozen fold identity mismatch: {fold_hash}")
    currier = G.page_currier_authority(lines)

    by_fold = {str(f): {"clean_tokens": 0, "real_space": 0, "mid_token": 0, "p2_real_space": 0} for f in range(N_FOLDS)}
    by_currier = {c: {"clean_tokens": 0, "real_space": 0, "mid_token": 0, "p2_real_space": 0} for c in ("A", "B", "UNKNOWN")}
    atom_inventory = Counter()
    mid_lengths = Counter()
    token_unclean = Counter()
    mid_exclusions = Counter()
    real_exclusions = Counter()
    locus_counts = Counter()
    real_ids = []
    mid_ids = []
    p2_ids = []

    for source_line_no, line in enumerate(lines, start=1):
        m = G.LOCUS_RE.match(line)
        if not m or "P" not in m.group("code"):
            continue
        locus_counts["p_loci_total"] += 1
        loc = m.group("loc")
        page = loc.split(".", 1)[0]
        lm = G.LEAF_RE.match(page)
        if not lm:
            locus_counts["p_loci_no_numeric_leaf"] += 1
            continue
        leaf = int(lm.group(1))
        if leaf not in leaf_fold:
            locus_counts["p_loci_outside_frozen_folds"] += 1
            continue
        fold = int(leaf_fold[leaf])
        c = currier.get(page, "UNKNOWN")
        if c not in ("A", "B"):
            c = "UNKNOWN"
        locus_counts["p_loci_in_frozen_folds"] += 1

        segments, n_dot = G.split_certain_spaces(m.group("body"))
        atoms_by_segment = []
        for si, token in enumerate(segments):
            reasons = G.unclean_reasons(token)
            atoms = None if reasons else G.atomize_clean(token)
            if atoms is None and not reasons:
                reasons = ("atomizer_failure",)
            atoms_by_segment.append(atoms)
            if atoms is None:
                for r in reasons:
                    token_unclean[r] += 1
                    mid_exclusions[r] += 1
                continue
            by_fold[str(fold)]["clean_tokens"] += 1
            by_currier[c]["clean_tokens"] += 1
            atom_inventory.update(atoms)
            if len(atoms) < 4:
                mid_exclusions["fewer_than_4_atoms"] += 1
                continue
            cut = len(atoms) // 2
            by_fold[str(fold)]["mid_token"] += 1
            by_currier[c]["mid_token"] += 1
            mid_lengths[str(len(atoms))] += 1
            mid_ids.append((loc, source_line_no, si, len(atoms), cut, fold))

        if n_dot != len(segments) - 1:
            raise RuntimeError(f"dot/segment invariant failed at {loc}")
        for bi in range(n_dot):
            left = atoms_by_segment[bi]
            right = atoms_by_segment[bi + 1]
            if left is None:
                real_exclusions["left_unclean"] += 1
            if right is None:
                real_exclusions["right_unclean"] += 1
            if left is None or right is None:
                continue
            if len(left) < 2:
                real_exclusions["left_fewer_than_2_atoms"] += 1
            if len(right) < 2:
                real_exclusions["right_fewer_than_2_atoms"] += 1
            if len(left) < 2 or len(right) < 2:
                continue
            by_fold[str(fold)]["real_space"] += 1
            by_currier[c]["real_space"] += 1
            eid = (loc, source_line_no, bi, len(left), len(right), fold)
            real_ids.append(eid)
            if len(left) >= 3 and len(right) >= 3:
                by_fold[str(fold)]["p2_real_space"] += 1
                by_currier[c]["p2_real_space"] += 1
                p2_ids.append(eid)
            else:
                real_exclusions["p2_side_fewer_than_3_atoms"] += 1

    support = {
        "real_space_all_folds_nonzero": all(by_fold[str(f)]["real_space"] > 0 for f in range(N_FOLDS)),
        "mid_token_all_folds_nonzero": all(by_fold[str(f)]["mid_token"] > 0 for f in range(N_FOLDS)),
        "p2_real_space_all_folds_nonzero": all(by_fold[str(f)]["p2_real_space"] > 0 for f in range(N_FOLDS)),
    }
    return {
        "schema": "issue115-phase4b-it2a-gate0-v1",
        "phase": "ISSUE115_PHASE4B_IT2A_GATE0",
        "source": src,
        "source_authority_exact_match": True,
        "representation": {
            "primary_real_space": "literal IVTFF '.' certain word-space only",
            "basic_eva_letters": "".join(sorted(G.BASIC_EVA)),
            "connected_composites_longest_match": list(G.CONNECTED_COMPOSITES),
            "mid_cut": "floor(n_atoms/2), >=2 each side",
            "p2_support": ">=3 atoms each observed side",
        },
        "fold_authority": {"identity": fold_identity, "identity_sha256": fold_hash, "n_leaves": len(leaf_fold)},
        "population": {
            "clean_tokens": sum(v["clean_tokens"] for v in by_fold.values()),
            "real_space": len(real_ids),
            "mid_token": len(mid_ids),
            "p2_real_space": len(p2_ids),
            "event_id_hashes": {
                "real_space_sha256": G.sha256_obj(real_ids),
                "mid_token_sha256": G.sha256_obj(mid_ids),
                "p2_real_space_sha256": G.sha256_obj(p2_ids),
            },
        },
        "by_fold": by_fold,
        "by_currier": by_currier,
        "mid_source_token_length_atoms": dict(sorted(mid_lengths.items(), key=lambda kv: int(kv[0]))),
        "raw_atom_inventory_clean_tokens": dict(sorted(atom_inventory.items())),
        "exclusions": {
            "loci": dict(sorted(locus_counts.items())),
            "unclean_token_reasons": dict(sorted(token_unclean.items())),
            "mid_token": dict(sorted(mid_exclusions.items())),
            "real_space": dict(sorted(real_exclusions.items())),
        },
        "support": support,
        "gate_pass": all(support.values()),
        "firewall": {
            "predictive_scores_computed": False,
            "boundary_model_fitted": False,
            "slotparser_used_for_event_eligibility": False,
            "zl3b_phase4_target_scores_read": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
        },
    }


def self_test() -> None:
    assert G.atomize_clean("qokchody") == ("q", "o", "k", "ch", "o", "d", "y")
    assert G.atomize_clean("cthaiin") == ("cth", "a", "i", "i", "n")
    assert G.atomize_clean("or,y") is None
    print("self-test OK")


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--self-test", action="store_true")
    g.add_argument("--audit", nargs=3, metavar=("IT2A", "ZL3B", "OUT"))
    args = ap.parse_args(argv)
    if args.self_test:
        self_test(); return 0
    result = audit(Path(args.audit[0]).resolve(), Path(args.audit[1]).resolve())
    Path(args.audit[2]).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"gate_pass": result["gate_pass"], "population": result["population"], "support": result["support"]}, indent=2, sort_keys=True))
    return 0 if result["gate_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
