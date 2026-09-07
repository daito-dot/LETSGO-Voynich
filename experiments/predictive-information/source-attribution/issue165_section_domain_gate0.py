#!/usr/bin/env python3
"""Issue #165 Gate0: score-free section/domain source-attribution audit.

Reproduce the compact Issue #161 authority and Issue #107 IVTFF metadata audit,
freeze pure physical-leaf section/hand labels, and determine which Currier x
section populations have enough common-EVA run-body target support in both
ZL3b and IT2a. Also freeze the deterministic one-leaf section-label placebo.

No real-target section-conditioned probability, likelihood, G_section,
G_placebo, or scientific classification is computed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
CURRIER_DIR = ROOT / "experiments" / "predictive-information" / "common-eva-currier"
PHASE3B_DIR = ROOT / "experiments" / "predictive-information" / "phase3b"
if str(CURRIER_DIR) not in sys.path:
    sys.path.insert(0, str(CURRIER_DIR))
if str(PHASE3B_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE3B_DIR))

import issue161_outcome_factor_gate0 as G161  # noqa: E402
import issue161_outcome_factor_first_reveal as S161  # noqa: E402
import issue155_common_eva_currier_first_reveal as S155  # noqa: E402
import metadata_gate0_audit as M107  # noqa: E402

PLAN_PATH = HERE.parent / "ISSUE165_SECTION_DOMAIN_TRANSPORT_PLAN.md"
ISSUE161_GATE_PATH = CURRIER_DIR / "issue161_outcome_factor_gate0.py"
ISSUE161_GATE_PROVENANCE_PATH = CURRIER_DIR / "ISSUE161_GATE0_PROVENANCE.md"
ISSUE161_SCORER_PATH = CURRIER_DIR / "issue161_outcome_factor_first_reveal.py"
ISSUE161_FIRST_PROVENANCE_PATH = CURRIER_DIR / "ISSUE161_FIRST_REVEAL_PROVENANCE.md"
METADATA_SCANNER_PATH = PHASE3B_DIR / "metadata_gate0_audit.py"

EXPECTED = {
    "issue161_gate_result_sha256": "32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94",
    "issue161_gate_blob": "00e5bddc0484b9472bb4fce9dadb89dd52bf578f",
    "issue161_gate_provenance_blob": "67e91ba26a76898f679a5182828ab3e9f512d49a",
    "issue161_scorer_blob": "d24149977770118505f2147c5aa2bb727631906f",
    "issue161_first_provenance_blob": "73100548fef5dbc0d08a1951e3c0ca5b370cd6f4",
    "issue161_first_result_sha256": "11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031",
    "issue161_merge": "72ff98da2eac4b830dd02eae7623577362c29150",
    "issue107_scanner_blob": "110a6b848df71c4f51ec0d9dd3b262039d1fc66f",
    "issue107_result_sha256": "8f48a01ef4457f38a4e273fe32ea73b9f90817af156be0111bb56a550f443870",
    "plan_blob": "d334092e6c7cd38f76deb48250fa09d8f9468064",
    "fold_sha256": "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b",
    "candidate_sections": ["A", "B", "C", "H", "P", "S", "T", "Z"],
    "min_leaves": 5,
    "min_body_targets": 300,
    "required_support_folds": 4,
    "n_folds": 5,
}

READINGS = ("ZL3b", "IT2a")
REGIMES = ("A", "B")


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G161.git_blob(path)


def verify_entry_authority(zl_path: Path, it_path: Path) -> tuple[dict, dict, dict]:
    pins = (
        (ISSUE161_GATE_PATH, "issue161_gate_blob"),
        (ISSUE161_GATE_PROVENANCE_PATH, "issue161_gate_provenance_blob"),
        (ISSUE161_SCORER_PATH, "issue161_scorer_blob"),
        (ISSUE161_FIRST_PROVENANCE_PATH, "issue161_first_provenance_blob"),
        (METADATA_SCANNER_PATH, "issue107_scanner_blob"),
        (PLAN_PATH, "plan_blob"),
    )
    for path, key in pins:
        actual = git_blob(path)
        if actual != EXPECTED[key]:
            raise RuntimeError(f"frozen blob changed for {path.name}: {actual}")

    gate161 = G161.run_gate(zl_path, it_path)
    gate161_sha = sha256_obj(gate161)
    if gate161_sha != EXPECTED["issue161_gate_result_sha256"]:
        raise RuntimeError(f"Issue161 Gate result SHA changed: {gate161_sha}")
    if not gate161.get("gate_pass"):
        raise RuntimeError("Issue161 Gate no longer passes")
    if gate161["entry_authority"]["fold_identity_sha256"] != EXPECTED["fold_sha256"]:
        raise RuntimeError("physical-leaf fold authority changed")

    metadata = M107.audit(zl_path)
    metadata_sha = sha256_obj(metadata)
    if metadata_sha != EXPECTED["issue107_result_sha256"]:
        raise RuntimeError(f"Issue107 metadata result SHA changed: {metadata_sha}")
    if metadata.get("audit_valid") is not True:
        raise RuntimeError("Issue107 metadata audit no longer valid")
    if metadata.get("classification") != "NO ADEQUATELY CROSSED OBSERVABLE FACTOR":
        raise RuntimeError("Issue107 metadata classification changed")

    gate155 = G161.G158.G155.run_gate(zl_path, it_path)
    gate155_sha = G161.G158.sha256_obj(gate155)
    if gate155_sha != G161.G158.EXPECTED["issue155_gate_result_sha256"]:
        raise RuntimeError("Issue155 Gate no longer reproduces")
    return gate161, metadata, gate155


def resolved_metadata_rows(zl_path: Path):
    headers = M107.G0.parse_source_headers(zl_path)
    items, folds, parsed = M107.I81.C.load_corpus(zl_path)
    scan = M107.scan_token_metadata(zl_path, items, folds, parsed, headers)
    if scan["conformance_violations"]:
        raise RuntimeError("metadata conformance violations reappeared")
    if scan["raw_L_vs_phase3a_authority_mismatches"]:
        raise RuntimeError("metadata Currier authority mismatch reappeared")
    if scan["line_mapping_mismatches"]:
        raise RuntimeError("metadata line mapping mismatch reappeared")
    return scan["rows"]


def pure_leaf_map(rows, var: str) -> tuple[dict[int, str], list[dict]]:
    values = defaultdict(set)
    has_special = defaultdict(bool)
    seen = set()
    for row in rows:
        leaf = int(row["leaf"])
        seen.add(leaf)
        val = str(row[var])
        if val in M107.SPECIAL:
            has_special[leaf] = True
        else:
            values[leaf].add(val)

    pure = {}
    audit = []
    for leaf in sorted(seen):
        vals = sorted(values.get(leaf, set()))
        if (not has_special[leaf]) and len(vals) == 1:
            status = "PURE"
            label = vals[0]
            pure[leaf] = label
        else:
            status = "MIXED_OR_UNUSABLE"
            label = None
        audit.append(
            {
                "leaf": leaf,
                "status": status,
                "label": label,
                "non_special_levels": vals,
                "has_special_or_unresolved": bool(has_special[leaf]),
            }
        )
    return pure, audit


def load_common_runs(zl_path: Path, it_path: Path, gate155: dict):
    leaf_currier = S155.leaf_currier_from_gate(gate155)
    leaf_fold = G161.G158.G155.G151.G148.G145.fold_authority(zl_path)[0]
    parser = G161.G158.G155.G151.G148.G145.E.SlotParser()
    G161.G158.G155.G151.G148.G145.E.validate_parser(parser)
    _zs, zl_lines = G161.G158.G155.G151.G148.G145.source_identity(zl_path, "ZL3b")
    _is, it_lines = G161.G158.G155.G151.G148.G145.source_identity(it_path, "IT2a")
    C145 = S161.C145
    return (
        leaf_currier,
        leaf_fold,
        {
            "ZL3b": C145.clean_runs(zl_lines, leaf_fold, parser),
            "IT2a": C145.clean_runs(it_lines, leaf_fold, parser),
        },
    )


def count_body_support(runs, leaf_currier, pure_i, pure_h=None):
    section = {
        r: {s: {str(f): 0 for f in range(EXPECTED["n_folds"])} for s in EXPECTED["candidate_sections"]}
        for r in REGIMES
    }
    hand_section = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {str(f): 0 for f in range(EXPECTED["n_folds"])})))

    for fold, leaf, _loc, _line_no, run in runs:
        leaf = int(leaf)
        regime = leaf_currier.get(leaf)
        sec = pure_i.get(leaf)
        hand = pure_h.get(leaf) if pure_h is not None else None
        if regime not in REGIMES or sec not in EXPECTED["candidate_sections"]:
            continue
        for ti, record in enumerate(run):
            if ti == 0 or not record["slotparser_accepted"]:
                continue
            section[regime][sec][str(int(fold))] += 1
            if hand is not None:
                hand_section[regime][sec][hand][str(int(fold))] += 1
    frozen_h = {
        r: {
            s: {h: dict(counts) for h, counts in sorted(hands.items())}
            for s, hands in sorted(sections.items())
        }
        for r, sections in sorted(hand_section.items())
    }
    return section, frozen_h


def leaf_counts(leaf_currier, pure_i):
    out = {r: {s: [] for s in EXPECTED["candidate_sections"]} for r in REGIMES}
    for leaf, sec in sorted(pure_i.items()):
        r = leaf_currier.get(int(leaf))
        if r in REGIMES and sec in EXPECTED["candidate_sections"]:
            out[r][sec].append(int(leaf))
    return out


def eligible_sections(leafs, support_by_reading):
    out = {}
    for regime in REGIMES:
        eligible = []
        diagnostics = {}
        for sec in EXPECTED["candidate_sections"]:
            z = support_by_reading["ZL3b"][regime][sec]
            i = support_by_reading["IT2a"][regime][sec]
            z_good = sum(int(z[str(f)]) >= EXPECTED["min_body_targets"] for f in range(EXPECTED["n_folds"]))
            i_good = sum(int(i[str(f)]) >= EXPECTED["min_body_targets"] for f in range(EXPECTED["n_folds"]))
            ok = bool(
                len(leafs[regime][sec]) >= EXPECTED["min_leaves"]
                and z_good >= EXPECTED["required_support_folds"]
                and i_good >= EXPECTED["required_support_folds"]
            )
            diagnostics[sec] = {
                "pure_leaves": leafs[regime][sec],
                "n_pure_leaves": len(leafs[regime][sec]),
                "ZL3b_body_by_fold": z,
                "IT2a_body_by_fold": i,
                "ZL3b_folds_at_or_above_threshold": z_good,
                "IT2a_folds_at_or_above_threshold": i_good,
                "eligible": ok,
            }
            if ok:
                eligible.append(sec)
        out[regime] = {
            "eligible_sections": eligible,
            "n_eligible_sections": len(eligible),
            "scorable": len(eligible) >= 2,
            "diagnostics": diagnostics,
        }
    return out


def scribe_identifiability(leaf_currier, leaf_fold, pure_i, pure_h, eligibility, hand_support):
    # A hand must have >=5 pure leaves and >=300 run-body targets in >=4/5 folds
    # in both readings within the same Currier and same eligible section.
    cells = []
    licensed = []
    for regime in REGIMES:
        for sec in eligibility[regime]["eligible_sections"]:
            hands = sorted(
                {
                    h
                    for leaf, h in pure_h.items()
                    if leaf_currier.get(int(leaf)) == regime and pure_i.get(int(leaf)) == sec
                }
            )
            qualifying = []
            hand_diag = {}
            for hand in hands:
                leaves = sorted(
                    int(leaf)
                    for leaf, h in pure_h.items()
                    if h == hand
                    and leaf_currier.get(int(leaf)) == regime
                    and pure_i.get(int(leaf)) == sec
                )
                z = hand_support["ZL3b"].get(regime, {}).get(sec, {}).get(
                    hand, {str(f): 0 for f in range(EXPECTED["n_folds"])}
                )
                i = hand_support["IT2a"].get(regime, {}).get(sec, {}).get(
                    hand, {str(f): 0 for f in range(EXPECTED["n_folds"])}
                )
                z_good = sum(int(z[str(f)]) >= EXPECTED["min_body_targets"] for f in range(EXPECTED["n_folds"]))
                i_good = sum(int(i[str(f)]) >= EXPECTED["min_body_targets"] for f in range(EXPECTED["n_folds"]))
                ok = bool(
                    len(leaves) >= EXPECTED["min_leaves"]
                    and z_good >= EXPECTED["required_support_folds"]
                    and i_good >= EXPECTED["required_support_folds"]
                )
                hand_diag[hand] = {
                    "pure_leaves": leaves,
                    "n_pure_leaves": len(leaves),
                    "ZL3b_body_by_fold": z,
                    "IT2a_body_by_fold": i,
                    "ZL3b_folds_at_or_above_threshold": z_good,
                    "IT2a_folds_at_or_above_threshold": i_good,
                    "qualifies": ok,
                }
                if ok:
                    qualifying.append(hand)
            cell = {
                "regime": regime,
                "section": sec,
                "qualifying_hands": qualifying,
                "n_qualifying_hands": len(qualifying),
                "scribe_scoring_licensed_here": len(qualifying) >= 2,
                "hands": hand_diag,
            }
            cells.append(cell)
            if cell["scribe_scoring_licensed_here"]:
                licensed.append({"regime": regime, "section": sec, "hands": qualifying})
    return {
        "classification": "SCRIBE_IDENTIFIABLE" if licensed else "SCRIBE_NOT_IDENTIFIABLE",
        "licensed_cells": licensed,
        "cells": cells,
    }


def placebo_maps(leaf_currier, leaf_fold, pure_i, eligibility):
    outer = []
    for f in range(EXPECTED["n_folds"]):
        by_regime = {}
        for regime in REGIMES:
            if not eligibility[regime]["scorable"]:
                by_regime[regime] = {
                    "scorable": False,
                    "eligible_sections": eligibility[regime]["eligible_sections"],
                    "mapping": [],
                    "mapping_sha256": None,
                    "changed_leaves": 0,
                    "invalid_all_labels_unchanged": False,
                }
                continue
            eligible = set(eligibility[regime]["eligible_sections"])
            leaves = sorted(
                int(leaf)
                for leaf, sec in pure_i.items()
                if sec in eligible
                and leaf_currier.get(int(leaf)) == regime
                and int(leaf_fold[int(leaf)]) != f
            )
            if len(leaves) < 2:
                raise RuntimeError(f"fold {f} {regime} has <2 placebo training leaves")
            labels = [pure_i[leaf] for leaf in leaves]
            shifted = labels[1:] + labels[:1]
            mapping = [[leaf, old, new] for leaf, old, new in zip(leaves, labels, shifted)]
            changed = sum(old != new for _, old, new in mapping)
            if changed == 0:
                raise RuntimeError(f"fold {f} {regime} placebo leaves every label unchanged")
            by_regime[regime] = {
                "scorable": True,
                "eligible_sections": eligibility[regime]["eligible_sections"],
                "mapping": mapping,
                "mapping_sha256": sha256_obj(mapping),
                "changed_leaves": changed,
                "n_training_leaves": len(leaves),
                "invalid_all_labels_unchanged": False,
            }
        heldout = sorted(int(leaf) for leaf, ff in leaf_fold.items() if int(ff) == f)
        training = sorted(int(leaf) for leaf, ff in leaf_fold.items() if int(ff) != f)
        overlap = sorted(set(heldout) & set(training))
        if overlap:
            raise RuntimeError(f"fold {f} train/test leaf leakage")
        outer.append(
            {
                "outer_fold": f,
                "heldout_physical_leaves": heldout,
                "training_union_heldout_overlap": overlap,
                "regimes": by_regime,
            }
        )
    return outer


def synthetic_test():
    fake_rows = [
        {"leaf": 1, "I": "H", "H": "2"},
        {"leaf": 1, "I": "H", "H": "2"},
        {"leaf": 2, "I": "S", "H": "3"},
        {"leaf": 2, "I": "S", "H": "3"},
        {"leaf": 3, "I": "H", "H": "2"},
        {"leaf": 3, "I": "S", "H": "2"},
        {"leaf": 4, "I": "MISSING", "H": "UNSET"},
    ]
    pure_i, audit_i = pure_leaf_map(fake_rows, "I")
    pure_h, audit_h = pure_leaf_map(fake_rows, "H")
    if pure_i != {1: "H", 2: "S"}:
        raise AssertionError("synthetic pure-I classification failed")
    if pure_h != {1: "2", 2: "3", 3: "2"}:
        raise AssertionError("synthetic pure-H classification failed")
    leaves = [1, 2, 5]
    labels = ["H", "S", "H"]
    shifted = labels[1:] + labels[:1]
    mapping = list(zip(leaves, labels, shifted))
    if mapping != [(1, "H", "S"), (2, "S", "H"), (5, "H", "H")]:
        raise AssertionError("synthetic left-rotation placebo failed")
    if sum(a != b for _, a, b in mapping) == 0:
        raise AssertionError("synthetic placebo failed to change any label")
    return {
        "ok": True,
        "uses_real_target_likelihood": False,
        "pure_I_rule": True,
        "pure_H_rule": True,
        "left_cyclic_one_leaf_placebo": True,
        "mixed_and_special_leaves_excluded": True,
        "audit_I": audit_i,
        "audit_H": audit_h,
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    gate161, metadata, gate155 = verify_entry_authority(zl_path, it_path)
    rows = resolved_metadata_rows(zl_path)
    pure_i, pure_i_audit = pure_leaf_map(rows, "I")
    pure_h, pure_h_audit = pure_leaf_map(rows, "H")
    pure_i_records = [[leaf, pure_i[leaf]] for leaf in sorted(pure_i)]
    pure_h_records = [[leaf, pure_h[leaf]] for leaf in sorted(pure_h)]

    leaf_currier, leaf_fold, runs = load_common_runs(zl_path, it_path, gate155)
    support = {}
    hand_support = {}
    for reading in READINGS:
        sec, hand = count_body_support(runs[reading], leaf_currier, pure_i, pure_h)
        support[reading] = sec
        hand_support[reading] = hand

    leaves = leaf_counts(leaf_currier, pure_i)
    eligibility = eligible_sections(leaves, support)
    scorable_regimes = [r for r in REGIMES if eligibility[r]["scorable"]]
    if not scorable_regimes:
        raise RuntimeError("no Currier regime has >=2 eligible section levels")

    scribe = scribe_identifiability(
        leaf_currier, leaf_fold, pure_i, pure_h, eligibility, hand_support
    )
    placebo = placebo_maps(leaf_currier, leaf_fold, pure_i, eligibility)
    synthetic = synthetic_test()

    return {
        "schema": "issue165-section-domain-gate0-v1",
        "issue": 165,
        "phase": "SECTION_DOMAIN_SOURCE_ATTRIBUTION_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED SECTION/DOMAIN SCORER",
        "scientific_section_metrics_computed": False,
        "entry_authority": {
            "issue161_gate_reproduced": True,
            "issue161_gate_result_sha256": EXPECTED["issue161_gate_result_sha256"],
            "issue161_gate_blob": EXPECTED["issue161_gate_blob"],
            "issue161_gate_provenance_blob": EXPECTED["issue161_gate_provenance_blob"],
            "issue161_scorer_blob": EXPECTED["issue161_scorer_blob"],
            "issue161_first_provenance_blob": EXPECTED["issue161_first_provenance_blob"],
            "issue161_declared_first_reveal_result_sha256": EXPECTED["issue161_first_result_sha256"],
            "issue161_merge": EXPECTED["issue161_merge"],
            "issue107_metadata_reproduced": True,
            "issue107_metadata_result_sha256": EXPECTED["issue107_result_sha256"],
            "issue107_scanner_blob": EXPECTED["issue107_scanner_blob"],
            "fold_identity_sha256": EXPECTED["fold_sha256"],
            "plan_blob_sha1": git_blob(PLAN_PATH),
        },
        "metadata_authority": {
            "issue107_classification": metadata["classification"],
            "candidate_sections": list(EXPECTED["candidate_sections"]),
            "pure_I_leaf_map": pure_i_records,
            "pure_I_leaf_map_sha256": sha256_obj(pure_i_records),
            "pure_I_leaf_audit": pure_i_audit,
            "pure_H_leaf_map": pure_h_records,
            "pure_H_leaf_map_sha256": sha256_obj(pure_h_records),
            "pure_H_leaf_audit": pure_h_audit,
        },
        "support_thresholds": {
            "min_pure_leaves": EXPECTED["min_leaves"],
            "min_primary_run_body_targets_per_fold": EXPECTED["min_body_targets"],
            "required_folds_at_threshold": EXPECTED["required_support_folds"],
            "required_eligible_sections_per_currier": 2,
        },
        "section_support": support,
        "leaf_support": leaves,
        "eligibility": eligibility,
        "scorable_currier_regimes": scorable_regimes,
        "scribe_identifiability": scribe,
        "placebo_outer": placebo,
        "synthetic_test": synthetic,
        "firewall": {
            "real_target_section_probability_computed": False,
            "real_target_section_likelihood_computed": False,
            "G_section_computed": False,
            "G_placebo_computed": False,
            "scientific_classification_computed": False,
            "heldout_target_outcome_used_for_section_or_leaf_selection": False,
            "mixed_or_unresolved_leaf_scored": False,
            "scribe_model_fitted": False,
            "placebo_permutation_searched_or_repeated": False,
            "currier_fold_representation_or_issue161_model_changed": False,
            "section_by_previous_terminal_interaction_added": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
        },
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue165-section-domain-gate0-v1",
        "issue": 165,
        "phase": "SECTION_DOMAIN_SOURCE_ATTRIBUTION_GATE0",
        "gate_pass": False,
        "gate_disposition": "INVALID SECTION/DOMAIN SOURCE ATTRIBUTION — GATE0 FAILED",
        "scientific_section_metrics_computed": False,
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {
            "post_failure_scientific_repair_allowed": False,
            "post_failure_target_driven_threshold_change_allowed": False,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--run", nargs=3, metavar=("ZL3B", "IT2A", "OUT_JSON"))
    ns = ap.parse_args(argv)
    if ns.self_test:
        print(canonical_json(synthetic_test()), end="")
        return 0
    zl_path = Path(ns.run[0]).resolve()
    it_path = Path(ns.run[1]).resolve()
    out_path = Path(ns.run[2]).resolve()
    try:
        result = run_gate(zl_path, it_path)
        rc = 0
    except Exception as exc:
        result = invalid_result(exc)
        rc = 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
