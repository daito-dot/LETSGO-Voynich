#!/usr/bin/env python3
"""Issue #148 Gate0: score-free common-EVA cross-reading table support audit.

This executable verifies source, representation, fold, event and directional
context-support authority only. It deliberately contains no cross-table
predictive scoring implementation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
COMMON_DIR = ROOT / "experiments" / "predictive-information" / "common-eva-edge"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

import issue145_common_eva_gate0 as G145  # noqa: E402

ISSUE145_SCORER_PATH = COMMON_DIR / "issue145_common_eva_first_reveal.py"
ISSUE145_FIRST_PROVENANCE_PATH = COMMON_DIR / "ISSUE145_FIRST_REVEAL_PROVENANCE.md"

EXPECTED = {
    "issue145_gate_result_sha256": "563573e81c931133aaa9877bcf79a57a40ebb3e2a946183cac3f6e922d65eb48",
    "issue145_gate_script_blob": "80585066e746f42ac10554aaaeece793682a0b84",
    "issue145_gate_provenance_blob": "e98d2fffac1d2500623a7f8660343ead67218332",
    "issue145_scorer_blob": "ce8a167c607fbcf2807f567439ab6837471f4f07",
    "issue145_first_provenance_blob": "1cbb43381c57726ecc3a5b5dc5e8efc0c7b732f6",
    "issue145_first_result_sha256": "663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2",
    "issue145_merge": "26ccaa527fc4e1026d031e4773b819137a678f69",
    "fold_sha256": "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b",
    "min_primary_body": 300,
    "min_source_supported_primary_body": 300,
    "n_folds": 5,
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_issue145_authority(zl_path: Path, it_path: Path) -> tuple[dict, str]:
    if G145.git_blob_sha1(G145.HERE.read_bytes()) != EXPECTED["issue145_gate_script_blob"]:
        raise RuntimeError("Issue145 Gate script blob changed")
    gate_prov = COMMON_DIR / "ISSUE145_GATE0_PROVENANCE.md"
    if G145.git_blob_sha1(gate_prov.read_bytes()) != EXPECTED["issue145_gate_provenance_blob"]:
        raise RuntimeError("Issue145 Gate provenance blob changed")
    if G145.git_blob_sha1(ISSUE145_SCORER_PATH.read_bytes()) != EXPECTED["issue145_scorer_blob"]:
        raise RuntimeError("Issue145 scorer blob changed")
    if G145.git_blob_sha1(ISSUE145_FIRST_PROVENANCE_PATH.read_bytes()) != EXPECTED["issue145_first_provenance_blob"]:
        raise RuntimeError("Issue145 first-reveal provenance blob changed")

    gate = G145.run_gate(zl_path, it_path)
    gate_sha = sha256_text(G145.canonical_json(gate))
    if gate_sha != EXPECTED["issue145_gate_result_sha256"]:
        raise RuntimeError(f"Issue145 Gate result SHA changed: {gate_sha}")
    if not gate.get("gate_pass"):
        raise RuntimeError("Issue145 Gate no longer passes")
    if gate["fold_authority"]["identity_sha256"] != EXPECTED["fold_sha256"]:
        raise RuntimeError("fold authority changed")
    return gate, gate_sha


def clean_events(lines: Sequence[str], leaf_fold: dict[int, int], parser) -> tuple[dict, ...]:
    records = []
    for source_line_no, line in enumerate(lines, start=1):
        m = G145.G.LOCUS_RE.match(line)
        if not m or "P" not in m.group("code"):
            continue
        loc = m.group("loc")
        page = loc.split(".", 1)[0]
        lm = G145.G.LEAF_RE.match(page)
        if not lm:
            continue
        leaf = int(lm.group(1))
        if leaf not in leaf_fold:
            continue
        fold = int(leaf_fold[leaf])
        segments, n_dot = G145.G.split_certain_spaces(m.group("body"))
        if n_dot != len(segments) - 1:
            raise RuntimeError(f"dot/segment invariant failed at {loc}")

        previous_atoms = None
        run_id = -1
        for segment_index, raw in enumerate(segments):
            atoms, _reasons = G145.clean_atoms(raw)
            if atoms is None:
                previous_atoms = None
                continue
            is_start = previous_atoms is None
            if is_start:
                run_id += 1
            records.append(
                {
                    "leaf": leaf,
                    "fold": fold,
                    "loc": loc,
                    "source_line_no": source_line_no,
                    "segment_index": segment_index,
                    "run_id": run_id,
                    "is_run_start": is_start,
                    "previous_terminal_atom": None if is_start else previous_atoms[-1],
                    "first_atom": atoms[0],
                    "slotparser_accepted": bool(parser.parses(raw)),
                }
            )
            previous_atoms = atoms
    return tuple(records)


def source_training_summary(records: Sequence[dict], heldout_fold: int) -> dict:
    train = [r for r in records if int(r["fold"]) != heldout_fold]
    body = [r for r in train if not bool(r["is_run_start"])]
    by_context = defaultdict(Counter)
    for r in body:
        ctx = r["previous_terminal_atom"]
        if ctx is None:
            raise RuntimeError("source BODY event missing previous-terminal atom")
        by_context[ctx][r["first_atom"]] += 1
    contexts = set(by_context)
    pairs = {(ctx, outcome) for ctx, counts in by_context.items() for outcome in counts}
    if not train or not body or len(contexts) < 2 or len(pairs) < 2:
        raise RuntimeError(f"degenerate source support for fold {heldout_fold}")
    event_counts = [sum(c.values()) for c in by_context.values()]
    outcome_counts = [len(c) for c in by_context.values()]
    return {
        "training_clean_tokens": len(train),
        "training_run_body_tokens": len(body),
        "previous_terminal_contexts": sorted(contexts),
        "n_previous_terminal_contexts": len(contexts),
        "n_previous_terminal_to_initial_pairs": len(pairs),
        "min_events_per_context": min(event_counts),
        "max_events_per_context": max(event_counts),
        "min_observed_initial_outcomes_per_context": min(outcome_counts),
        "max_observed_initial_outcomes_per_context": max(outcome_counts),
    }


def target_test_support(records: Sequence[dict], heldout_fold: int, source_contexts: set[str]) -> dict:
    test = [r for r in records if int(r["fold"]) == heldout_fold]
    primary = [r for r in test if bool(r["slotparser_accepted"])]
    body = [r for r in primary if not bool(r["is_run_start"])]
    supported = [r for r in body if r["previous_terminal_atom"] in source_contexts]
    unsupported = len(body) - len(supported)
    if len(body) < EXPECTED["min_primary_body"]:
        raise RuntimeError(f"target primary BODY support below threshold in fold {heldout_fold}")
    if len(supported) < EXPECTED["min_source_supported_primary_body"]:
        raise RuntimeError(f"source-context-supported target BODY support below threshold in fold {heldout_fold}")
    return {
        "target_clean_tokens": len(test),
        "target_primary_targets": len(primary),
        "target_primary_run_body_targets": len(body),
        "source_context_supported_primary_run_body_targets": len(supported),
        "source_context_unsupported_primary_run_body_targets": unsupported,
        "source_context_coverage_fraction": float(len(supported) / len(body)) if body else None,
    }


def direction_gate(
    source_label: str,
    target_label: str,
    source_records: Sequence[dict],
    target_records: Sequence[dict],
    gate145: dict,
) -> dict:
    rows = []
    fold_identity = gate145["fold_authority"]["identity"]
    for f in range(EXPECTED["n_folds"]):
        source_train_leaves = {
            int(r["leaf"]) for r in source_records if int(r["fold"]) != f
        }
        target_test_leaves = {
            int(r["leaf"]) for r in target_records if int(r["fold"]) == f
        }
        overlap = sorted(source_train_leaves & target_test_leaves)
        if overlap:
            raise RuntimeError(f"{source_label}->{target_label} fold {f} leaf leakage: {overlap}")

        src = source_training_summary(source_records, f)
        tgt = target_test_support(target_records, f, set(src["previous_terminal_contexts"]))

        expected_target = gate145["readings"][target_label]["by_fold"][str(f)]
        expected_source_train = gate145["readings"][source_label]["outer_training_support"][f]
        if tgt["target_clean_tokens"] != int(expected_target["clean_tokens"]):
            raise RuntimeError(f"{target_label} fold {f} clean target count changed")
        if tgt["target_primary_targets"] != int(expected_target["primary_targets"]):
            raise RuntimeError(f"{target_label} fold {f} primary target count changed")
        if tgt["target_primary_run_body_targets"] != int(expected_target["primary_run_body_targets"]):
            raise RuntimeError(f"{target_label} fold {f} primary BODY count changed")
        if src["training_clean_tokens"] != int(expected_source_train["training_clean_tokens"]):
            raise RuntimeError(f"{source_label} fold {f} training clean count changed")
        if src["training_run_body_tokens"] != int(expected_source_train["training_run_body_tokens"]):
            raise RuntimeError(f"{source_label} fold {f} training BODY count changed")
        if len(target_test_leaves) != len(fold_identity[f]):
            raise RuntimeError(f"target test leaf support changed in fold {f}")

        rows.append(
            {
                "outer_fold": f,
                "source_training_leaf_count": len(source_train_leaves),
                "target_test_leaf_count": len(target_test_leaves),
                "source_training_target_test_leaf_overlap": overlap,
                "source_training": src,
                "target_test": tgt,
            }
        )
    return {
        "source": source_label,
        "target": target_label,
        "outer": rows,
        "min_source_context_coverage_fraction": min(
            float(r["target_test"]["source_context_coverage_fraction"]) for r in rows
        ),
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    gate145, gate145_sha = verify_issue145_authority(zl_path, it_path)
    leaf_fold = {
        int(leaf): int(fold)
        for fold, leaves in enumerate(gate145["fold_authority"]["identity"])
        for leaf in leaves
    }
    parser = G145.E.SlotParser()
    G145.E.validate_parser(parser)

    _zl_source, zl_lines = G145.source_identity(zl_path, "ZL3b")
    _it_source, it_lines = G145.source_identity(it_path, "IT2a")
    zl_records = clean_events(zl_lines, leaf_fold, parser)
    it_records = clean_events(it_lines, leaf_fold, parser)

    zl_to_it = direction_gate("ZL3b", "IT2a", zl_records, it_records, gate145)
    it_to_zl = direction_gate("IT2a", "ZL3b", it_records, zl_records, gate145)

    return {
        "schema": "issue148-common-eva-table-gate0-v1",
        "issue": 148,
        "phase": "COMMON_EVA_LITERAL_TABLE_TRANSPORT_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED CROSS-READING TABLE SCORER",
        "scientific_transport_metrics_computed": False,
        "issue145_authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": gate145_sha,
            "gate0_script_blob": EXPECTED["issue145_gate_script_blob"],
            "gate0_provenance_blob": EXPECTED["issue145_gate_provenance_blob"],
            "scientific_scorer_blob": EXPECTED["issue145_scorer_blob"],
            "first_reveal_provenance_blob": EXPECTED["issue145_first_provenance_blob"],
            "first_reveal_result_sha256": EXPECTED["issue145_first_result_sha256"],
            "merge": EXPECTED["issue145_merge"],
            "fold_identity_sha256": gate145["fold_authority"]["identity_sha256"],
        },
        "representation": gate145["representation"],
        "directions": {
            "ZL3b_to_IT2a": zl_to_it,
            "IT2a_to_ZL3b": it_to_zl,
        },
        "support_thresholds": {
            "min_target_primary_run_body": EXPECTED["min_primary_body"],
            "min_source_context_supported_target_primary_run_body": EXPECTED[
                "min_source_supported_primary_body"
            ],
        },
        "firewall": {
            "scientific_transport_metrics_computed": False,
            "cross_table_target_score_computed": False,
            "target_current_first_atom_used_for_support_selection": False,
            "target_selected_support_matching": False,
            "target_selected_atom_mapping": False,
            "target_selected_k_alpha_strength_or_mixture": False,
            "target_native_edge_fallback_in_transport": False,
            "currier_hand_section_conditioned_transport": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
        },
    }


def self_test() -> dict:
    synthetic = (
        {"leaf": 1, "fold": 0, "is_run_start": True, "previous_terminal_atom": None, "first_atom": "a", "slotparser_accepted": True},
        {"leaf": 1, "fold": 0, "is_run_start": False, "previous_terminal_atom": "a", "first_atom": "b", "slotparser_accepted": True},
        {"leaf": 2, "fold": 1, "is_run_start": True, "previous_terminal_atom": None, "first_atom": "c", "slotparser_accepted": True},
        {"leaf": 2, "fold": 1, "is_run_start": False, "previous_terminal_atom": "c", "first_atom": "d", "slotparser_accepted": True},
        {"leaf": 3, "fold": 2, "is_run_start": False, "previous_terminal_atom": "a", "first_atom": "c", "slotparser_accepted": True},
    )
    src = source_training_summary(synthetic, 2)
    if set(src["previous_terminal_contexts"]) != {"a", "c"}:
        raise AssertionError("synthetic source context support failed")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "scientific_transport_metrics_computed": False,
        "support_audit_only": True,
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
            "schema": "issue148-common-eva-table-gate0-v1",
            "issue": 148,
            "phase": "COMMON_EVA_LITERAL_TABLE_TRANSPORT_GATE0",
            "gate_pass": False,
            "gate_disposition": "INVALID CROSS-READING TABLE TRANSPORT — GATE0 FAILED",
            "scientific_transport_metrics_computed": False,
            "error": f"{type(exc).__name__}: {exc}",
            "firewall": {"scientific_transport_metrics_computed": False},
        }
        rc = 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
