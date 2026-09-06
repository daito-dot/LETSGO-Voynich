#!/usr/bin/env python3
"""Issue #145 Gate0: score-free common-EVA dual-reading support audit.

This executable verifies only source / representation / fold / population /
finite-support authority. It deliberately contains no POS2/EDGE2 probability,
likelihood, code-length, gain, table-similarity, effect-ratio or scientific
classification implementation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
P4A_DIR = ROOT / "experiments" / "predictive-information" / "phase4a"
ISSUE26_DIR = ROOT / "experiments" / "issue26-music"
if str(P4A_DIR) not in sys.path:
    sys.path.insert(0, str(P4A_DIR))
if str(ISSUE26_DIR) not in sys.path:
    sys.path.insert(0, str(ISSUE26_DIR))

import phase4a_boundary_gate0 as G  # noqa: E402
import issue26e_core as E  # noqa: E402

P4A_PATH = ROOT / "experiments" / "predictive-information" / "phase4a" / "phase4a_boundary_gate0.py"
P4B_PATH = ROOT / "experiments" / "predictive-information" / "phase4b" / "phase4b_it2a_gate0.py"
SLOT_PATH = ROOT / "experiments" / "issue26-music" / "issue26e_core.py"

EXPECTED = {
    "ZL3b": {
        "sha256": "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
        "git_blob_sha1": "2a4533ab9bdfa85db9bad602d590978953055df1",
        "header": "#=IVTFF Eva- 2.0 M 5",
    },
    "IT2a": {
        "sha256": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
        "git_blob_sha1": "4d6d3f2537b1f507a257529b49c94af7d6e03446",
        "header": "#=IVTFF EvaT 2.0 M 3",
        "bytes": 342104,
        "lines": 5444,
    },
    "repo_blobs": {
        "phase4a_boundary_gate0.py": "756380dcd6f1b024a359923852627460c0f64dd0",
        "phase4b_it2a_gate0.py": "7520e1a5f2c64a4ccbc3cc0e65668a4e0a5391cb",
        "issue26e_core.py": "8bafba7f2bce4cf77c9001c729936c1ce619759b",
    },
    "fold_sha256": "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b",
    "n_folds": 5,
    "min_primary_per_fold": 300,
    "min_primary_body_per_fold": 300,
    "n_basic_atoms": 25,
    "n_composite_atoms": 6,
    "n_atom_outcomes": 31,
    "V_with_END": 32,
}

ATOM_OUTCOMES = frozenset(G.BASIC_EVA) | frozenset(G.CONNECTED_COMPOSITES)
if len(G.BASIC_EVA) != EXPECTED["n_basic_atoms"]:
    raise RuntimeError("Phase4A Basic-EVA inventory size drifted")
if len(G.CONNECTED_COMPOSITES) != EXPECTED["n_composite_atoms"]:
    raise RuntimeError("Phase4A composite inventory size drifted")
if len(ATOM_OUTCOMES) != EXPECTED["n_atom_outcomes"]:
    raise RuntimeError("common atom outcome inventory size drifted")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def verify_repo_authorities() -> dict:
    paths = {
        "phase4a_boundary_gate0.py": P4A_PATH,
        "phase4b_it2a_gate0.py": P4B_PATH,
        "issue26e_core.py": SLOT_PATH,
    }
    out = {}
    for name, path in paths.items():
        if not path.is_file():
            raise RuntimeError(f"missing repository authority: {path}")
        blob = git_blob_sha1(path.read_bytes())
        expected = EXPECTED["repo_blobs"][name]
        if blob != expected:
            raise RuntimeError(f"repository authority drift for {name}: {blob} != {expected}")
        out[name] = {"path": str(path.relative_to(ROOT)), "git_blob_sha1": blob}
    return out


def source_identity(path: Path, label: str) -> tuple[dict, list[str]]:
    raw = path.read_bytes()
    lines = raw.decode("utf-8-sig", errors="strict").splitlines()
    got = {
        "sha256": sha256_bytes(raw),
        "git_blob_sha1": git_blob_sha1(raw),
        "header": lines[0].strip() if lines else "",
        "bytes": len(raw),
        "lines": len(lines),
    }
    expected = EXPECTED[label]
    for key in ("sha256", "git_blob_sha1", "header"):
        if got[key] != expected[key]:
            raise RuntimeError(f"{label} source authority mismatch at {key}: {got[key]}")
    if label == "IT2a":
        if got["bytes"] != expected["bytes"] or got["lines"] != expected["lines"]:
            raise RuntimeError(f"{label} byte/line authority mismatch")
    return got, lines


def fold_authority(zl_path: Path) -> tuple[dict[int, int], list[list[int]], str]:
    leaf_fold, identity = G.frozen_fold_authority(zl_path)
    fold_sha = G.sha256_obj(identity)
    if fold_sha != EXPECTED["fold_sha256"]:
        raise RuntimeError(f"physical-leaf fold authority drift: {fold_sha}")
    if len(identity) != EXPECTED["n_folds"]:
        raise RuntimeError("physical-leaf fold count drift")
    union = {int(leaf) for fold in identity for leaf in fold}
    if len(union) != len(leaf_fold):
        raise RuntimeError("fold identity contains duplicate leaves")
    return leaf_fold, identity, fold_sha


def clean_atoms(raw: str):
    reasons = G.unclean_reasons(raw)
    if reasons:
        return None, reasons
    atoms = G.atomize_clean(raw)
    if atoms is None:
        return None, ("atomizer_failure",)
    bad = sorted({a for a in atoms if a not in ATOM_OUTCOMES})
    if bad:
        raise RuntimeError(f"atom outside frozen common inventory: {bad}")
    if not atoms:
        raise RuntimeError("clean segment emitted zero atoms")
    return tuple(atoms), ()


def audit_reading(label: str, lines: Sequence[str], leaf_fold: dict[int, int], parser) -> dict:
    by_fold = {
        str(f): {
            "p_loci": 0,
            "clean_tokens": 0,
            "clean_runs": 0,
            "run_start_tokens": 0,
            "run_body_tokens": 0,
            "primary_targets": 0,
            "primary_run_start_targets": 0,
            "primary_run_body_targets": 0,
        }
        for f in range(EXPECTED["n_folds"])
    }
    exclusions = Counter()
    observed_leaves = set()
    observed_pages = set()
    atom_inventory = Counter()
    records = []
    p_loci_total = 0
    p_loci_outside_folds = 0
    certain_segments = 0

    for source_line_no, line in enumerate(lines, start=1):
        m = G.LOCUS_RE.match(line)
        if not m or "P" not in m.group("code"):
            continue
        p_loci_total += 1
        loc = m.group("loc")
        page = loc.split(".", 1)[0]
        lm = G.LEAF_RE.match(page)
        if not lm:
            exclusions["p_locus_no_numeric_leaf"] += 1
            continue
        leaf = int(lm.group(1))
        if leaf not in leaf_fold:
            p_loci_outside_folds += 1
            exclusions["p_locus_outside_frozen_folds"] += 1
            continue
        fold = int(leaf_fold[leaf])
        observed_leaves.add(leaf)
        observed_pages.add(page)
        by_fold[str(fold)]["p_loci"] += 1

        segments, n_dot = G.split_certain_spaces(m.group("body"))
        if n_dot != len(segments) - 1:
            raise RuntimeError(f"dot/segment invariant failed at {label}:{loc}")
        certain_segments += len(segments)

        parsed_segments = []
        for raw in segments:
            atoms, reasons = clean_atoms(raw)
            parsed_segments.append((raw, atoms))
            if atoms is None:
                for reason in reasons:
                    exclusions[f"unclean:{reason}"] += 1

        prev_atoms = None
        run_id = -1
        for si, (raw, atoms) in enumerate(parsed_segments):
            if atoms is None:
                prev_atoms = None
                continue
            is_start = prev_atoms is None
            if is_start:
                run_id += 1
                by_fold[str(fold)]["clean_runs"] += 1
                by_fold[str(fold)]["run_start_tokens"] += 1
            else:
                by_fold[str(fold)]["run_body_tokens"] += 1
            by_fold[str(fold)]["clean_tokens"] += 1
            atom_inventory.update(atoms)

            accepted = bool(parser.parses(raw))
            if accepted:
                by_fold[str(fold)]["primary_targets"] += 1
                if is_start:
                    by_fold[str(fold)]["primary_run_start_targets"] += 1
                else:
                    by_fold[str(fold)]["primary_run_body_targets"] += 1

            records.append(
                {
                    "leaf": leaf,
                    "fold": fold,
                    "loc": loc,
                    "source_line_no": source_line_no,
                    "segment_index": si,
                    "run_id_within_line": run_id,
                    "is_run_start": is_start,
                    "first_atom": atoms[0],
                    "terminal_atom": atoms[-1],
                    "previous_terminal_atom": None if is_start else prev_atoms[-1],
                    "slotparser_accepted": accepted,
                }
            )
            prev_atoms = atoms

    frozen_leaf_universe = set(map(int, leaf_fold.keys()))
    if observed_leaves != frozen_leaf_universe:
        missing = sorted(frozen_leaf_universe - observed_leaves)
        extra = sorted(observed_leaves - frozen_leaf_universe)
        raise RuntimeError(f"{label} observed leaf universe differs from frozen folds; missing={missing} extra={extra}")

    for f in range(EXPECTED["n_folds"]):
        row = by_fold[str(f)]
        if row["primary_targets"] < EXPECTED["min_primary_per_fold"]:
            raise RuntimeError(f"{label} fold {f} primary support below 300: {row['primary_targets']}")
        if row["primary_run_body_targets"] < EXPECTED["min_primary_body_per_fold"]:
            raise RuntimeError(
                f"{label} fold {f} primary run-body support below 300: {row['primary_run_body_targets']}"
            )

    training_support = []
    for heldout in range(EXPECTED["n_folds"]):
        train = [r for r in records if int(r["fold"]) != heldout]
        start_count = sum(bool(r["is_run_start"]) for r in train)
        body = [r for r in train if not bool(r["is_run_start"])]
        body_count = len(body)
        prev_contexts = {r["previous_terminal_atom"] for r in body}
        pairs = {(r["previous_terminal_atom"], r["first_atom"]) for r in body}
        if start_count <= 0 or body_count <= 0:
            raise RuntimeError(f"{label} heldout {heldout} degenerate START/BODY training support")
        if len(prev_contexts) < 2 or len(pairs) < 2:
            raise RuntimeError(f"{label} heldout {heldout} degenerate terminal edge support")
        training_support.append(
            {
                "outer_fold": heldout,
                "training_clean_tokens": len(train),
                "training_run_start_tokens": start_count,
                "training_run_body_tokens": body_count,
                "unique_previous_terminal_atom_contexts": len(prev_contexts),
                "unique_previous_terminal_to_initial_atom_pairs": len(pairs),
            }
        )

    return {
        "label": label,
        "p_loci_total": p_loci_total,
        "p_loci_outside_frozen_folds": p_loci_outside_folds,
        "pages_in_frozen_folds": len(observed_pages),
        "physical_leaves": len(observed_leaves),
        "observed_leaf_numbers": sorted(observed_leaves),
        "certain_space_segments": certain_segments,
        "by_fold": by_fold,
        "totals": {
            key: sum(by_fold[str(f)][key] for f in range(EXPECTED["n_folds"]))
            for key in (
                "p_loci",
                "clean_tokens",
                "clean_runs",
                "run_start_tokens",
                "run_body_tokens",
                "primary_targets",
                "primary_run_start_targets",
                "primary_run_body_targets",
            )
        },
        "atom_inventory_clean_tokens": dict(sorted(atom_inventory.items())),
        "exclusions": dict(sorted(exclusions.items())),
        "outer_training_support": training_support,
        "event_identity_sha256": G.sha256_obj(records),
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    code_authority = verify_repo_authorities()
    zl_source, zl_lines = source_identity(zl_path, "ZL3b")
    it_source, it_lines = source_identity(it_path, "IT2a")
    leaf_fold, fold_identity, fold_sha = fold_authority(zl_path)
    parser = E.SlotParser()
    parser_validation = E.validate_parser(parser)

    zl = audit_reading("ZL3b", zl_lines, leaf_fold, parser)
    it = audit_reading("IT2a", it_lines, leaf_fold, parser)

    for reading in (zl, it):
        seen_atoms = set(reading["atom_inventory_clean_tokens"])
        if not seen_atoms.issubset(ATOM_OUTCOMES):
            raise RuntimeError(f"{reading['label']} emitted atom outside frozen set")

    return {
        "schema": "issue145-common-eva-edge-gate0-v1",
        "issue": 145,
        "phase": "COMMON_EVA_DUAL_EDGE_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED COMMON-EVA DUAL EDGE SCORER",
        "scientific_target_metrics_computed": False,
        "sources": {"ZL3b": zl_source, "IT2a": it_source},
        "repository_authority": code_authority,
        "fold_authority": {
            "identity": fold_identity,
            "identity_sha256": fold_sha,
            "n_leaves": len(leaf_fold),
        },
        "representation": {
            "primary_boundary": "literal IVTFF '.' only",
            "basic_eva_single_atoms": sorted(G.BASIC_EVA),
            "connected_composites_longest_match": list(G.CONNECTED_COMPOSITES),
            "atom_outcomes": sorted(ATOM_OUTCOMES),
            "n_atom_outcomes": len(ATOM_OUTCOMES),
            "END_TOKEN_additional_outcome": True,
            "V_with_END": EXPECTED["V_with_END"],
            "clean_run_reset": "source-line start and immediately after every unclean segment",
            "edge_scope": "within maximal contiguous clean run only",
            "slotparser_primary_current_only": True,
            "previous_clean_token_need_not_be_slotparser_accepted": True,
        },
        "slot_parser_validation": parser_validation,
        "readings": {"ZL3b": zl, "IT2a": it},
        "support_thresholds": {
            "primary_targets_per_fold": EXPECTED["min_primary_per_fold"],
            "primary_run_body_targets_per_fold": EXPECTED["min_primary_body_per_fold"],
            "min_training_previous_terminal_contexts": 2,
            "min_training_terminal_initial_pairs": 2,
        },
        "firewall": {
            "scientific_target_metrics_computed": False,
            "POS2_or_EDGE2_probability_computed": False,
            "likelihood_or_code_length_computed": False,
            "edge_gain_computed": False,
            "cross_reading_effect_ratio_computed": False,
            "literal_table_similarity_computed": False,
            "target_selected_normalization": False,
            "token_alignment_by_surface_similarity": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
        },
    }


def self_test() -> dict:
    assert len(G.BASIC_EVA) == 25
    assert len(G.CONNECTED_COMPOSITES) == 6
    assert len(ATOM_OUTCOMES) == 31
    assert G.atomize_clean("qokchody") == ("q", "o", "k", "ch", "o", "d", "y")
    assert G.atomize_clean("cthaiin") == ("cth", "a", "i", "i", "n")
    assert G.atomize_clean("or,y") is None
    return {
        "ok": True,
        "target_sources_loaded": False,
        "scientific_target_metrics_computed": False,
        "n_atom_outcomes": len(ATOM_OUTCOMES),
        "V_with_END": EXPECTED["V_with_END"],
        "clean_run_reset_frozen": True,
    }


def canonical_json(obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--run", nargs=3, metavar=("ZL3B", "IT2A", "OUT_JSON"))
    ns = ap.parse_args(argv)

    if ns.self_test:
        print(canonical_json(self_test()), end="")
        return 0

    zl_path = Path(ns.run[0]).resolve()
    it_path = Path(ns.run[1]).resolve()
    out_path = Path(ns.run[2]).resolve()
    try:
        result = run_gate(zl_path, it_path)
        rc = 0
    except Exception as exc:
        result = {
            "schema": "issue145-common-eva-edge-gate0-v1",
            "issue": 145,
            "phase": "COMMON_EVA_DUAL_EDGE_GATE0",
            "gate_pass": False,
            "gate_disposition": "INVALID COMMON-REPRESENTATION EDGE TEST — GATE0 FAILED",
            "scientific_target_metrics_computed": False,
            "error": f"{type(exc).__name__}: {exc}",
            "firewall": {"scientific_target_metrics_computed": False},
        }
        rc = 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
