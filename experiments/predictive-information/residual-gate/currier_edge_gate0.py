#!/usr/bin/env python3
"""Issue #127 L4 Gate0: score-free Currier A/B support for terminal→initial edges."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PRED = ROOT / "experiments" / "predictive-information"
G0_PATH = PRED / "phase3a" / "currier_gate0_audit.py"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402

EXPECTED_CURRIER_GATE_SHA = "e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e"
LABELS = ("A", "B")


def load_gate0():
    spec = importlib.util.spec_from_file_location("issue127_phase3a_gate0", G0_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Phase3A Currier Gate0")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


G0 = load_gate0()
P1 = G0.P1


def json_sha256(x: dict) -> str:
    b = (json.dumps(x, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    return hashlib.sha256(b).hexdigest()


def empty_cell():
    return {
        "leaves": set(),
        "documents": set(),
        "items": 0,
        "source_lines": 0,
        "visible_edge_events": 0,
        "accepted_edge_targets": 0,
        "previous_terminal_classes": set(),
        "current_initial_outcomes": set(),
        "terminal_initial_pairs": set(),
    }


def freeze_cell(x: dict) -> dict:
    return {
        "leaves": sorted(int(v) for v in x["leaves"]),
        "documents": sorted(x["documents"]),
        "items": int(x["items"]),
        "source_lines": int(x["source_lines"]),
        "visible_edge_events": int(x["visible_edge_events"]),
        "accepted_edge_targets": int(x["accepted_edge_targets"]),
        "previous_terminal_classes": sorted(int(v) for v in x["previous_terminal_classes"]),
        "current_initial_outcomes": sorted(int(v) for v in x["current_initial_outcomes"]),
        "terminal_initial_pairs": sorted([int(a), int(b)] for a, b in x["terminal_initial_pairs"]),
        "n_previous_terminal_classes": int(len(x["previous_terminal_classes"])),
        "n_current_initial_outcomes": int(len(x["current_initial_outcomes"])),
        "n_terminal_initial_pairs": int(len(x["terminal_initial_pairs"])),
    }


def audit(zl_path: Path) -> dict:
    phase3a = G0.audit(zl_path)
    phase3a_sha = json_sha256(phase3a)
    if phase3a_sha != EXPECTED_CURRIER_GATE_SHA:
        raise RuntimeError(f"Phase3A Currier Gate0 SHA mismatch: {phase3a_sha}")
    if not phase3a["gate_pass"]:
        raise RuntimeError("Phase3A Currier Gate0 no longer passes")
    if phase3a["mixed_AB_leaves_excluded"]:
        raise RuntimeError(f"mixed A/B leaves appeared: {phase3a['mixed_AB_leaves_excluded']}")

    headers = G0.parse_source_headers(zl_path)
    by_doc = {r["document"]: r for r in headers}
    OA.configure(zl_path)
    items, folds, parsed = P1.I.C.load_corpus(zl_path)
    order_verify = OA.verify(items)
    P1.I.ordered = OA.ordered
    if len(folds) != P1.N_FOLDS:
        raise RuntimeError("frozen fold count changed")
    if P1.P0.fold_hash(folds) != phase3a["fold_identity_sha256"]:
        raise RuntimeError("fold identity changed")

    fold_of_leaf = {}
    for f, leaves in enumerate(folds):
        for leaf in leaves:
            leaf = int(leaf)
            if leaf in fold_of_leaf:
                raise RuntimeError(f"leaf {leaf} in multiple folds")
            fold_of_leaf[leaf] = int(f)

    cells = {lab: {str(f): empty_cell() for f in range(P1.N_FOLDS)} for lab in LABELS}
    global_support = {lab: empty_cell() for lab in LABELS}
    excluded_unknown_items = 0

    for it in P1.I.ordered(items):
        if it.document not in by_doc:
            raise RuntimeError(f"document absent from Currier authority: {it.document}")
        lab = by_doc[it.document]["label"]
        if lab not in LABELS:
            excluded_unknown_items += 1
            continue
        leaf = int(it.leaf)
        if leaf not in fold_of_leaf:
            raise RuntimeError(f"eligible leaf absent from folds: {leaf}")
        f = str(fold_of_leaf[leaf])
        targets = (cells[lab][f], global_support[lab])
        for x in targets:
            x["leaves"].add(leaf)
            x["documents"].add(it.document)
            x["items"] += 1

        for li, line in enumerate(it.lines):
            for x in targets:
                x["source_lines"] += 1
            if len(line) < 2:
                continue
            prev_syms = P1.token_symbols(line[0])
            if len(prev_syms) < 2:
                raise RuntimeError("visible token lacks raw byte")
            prev_final = int(prev_syms[-2])
            for ti in range(1, len(line)):
                tok = line[ti]
                syms = P1.token_symbols(tok)
                if len(syms) < 2:
                    raise RuntimeError("visible token lacks raw byte")
                current_initial = int(syms[0])
                accepted = parsed[it.item_id][li][ti] is not None
                for x in targets:
                    x["visible_edge_events"] += 1
                    if accepted:
                        x["accepted_edge_targets"] += 1
                        x["previous_terminal_classes"].add(prev_final)
                        x["current_initial_outcomes"].add(current_initial)
                        x["terminal_initial_pairs"].add((prev_final, current_initial))
                prev_final = int(syms[-2])

    frozen_cells = {
        lab: {f: freeze_cell(x) for f, x in fs.items()}
        for lab, fs in cells.items()
    }
    frozen_global = {lab: freeze_cell(x) for lab, x in global_support.items()}

    all_cells_nonzero = {
        lab: all(frozen_cells[lab][str(f)]["accepted_edge_targets"] > 0 for f in range(P1.N_FOLDS))
        for lab in LABELS
    }
    global_class_support = {
        lab: bool(
            frozen_global[lab]["n_previous_terminal_classes"] >= 2
            and frozen_global[lab]["n_current_initial_outcomes"] >= 2
        )
        for lab in LABELS
    }

    gate_pass = bool(
        phase3a_sha == EXPECTED_CURRIER_GATE_SHA
        and phase3a["gate_pass"]
        and not phase3a["mixed_AB_leaves_excluded"]
        and order_verify["numeric_paragraph_order_valid"]
        and order_verify["source_document_order_valid"]
        and all(all_cells_nonzero.values())
        and all(global_class_support.values())
    )

    return {
        "schema": "issue127-currier-edge-gate0-v1",
        "phase": "ISSUE127_L4_GATE0",
        "gate_pass": gate_pass,
        "gate_rule": "PROCEED_TO_FROZEN_EDGE_TRANSPORT" if gate_pass else "STOP_BEFORE_PREDICTIVE_TRANSPORT",
        "phase3a_currier_authority": {
            "json_sha256": phase3a_sha,
            "expected_json_sha256": EXPECTED_CURRIER_GATE_SHA,
            "gate_pass": phase3a["gate_pass"],
            "mixed_AB_leaves_excluded": phase3a["mixed_AB_leaves_excluded"],
            "fold_identity_sha256": phase3a["fold_identity_sha256"],
            "comment_fallback_records": phase3a["header_metadata"]["comment_fallback_records"],
        },
        "order_authority": order_verify,
        "edge_support_by_currier_and_fold": frozen_cells,
        "global_edge_support": frozen_global,
        "all_cells_nonzero": all_cells_nonzero,
        "global_class_support": global_class_support,
        "excluded_unknown_items": int(excluded_unknown_items),
        "firewall": {
            "probabilities_computed": False,
            "likelihoods_computed": False,
            "bits_per_token_computed": False,
            "transport_scores_computed": False,
            "mixture_strength_selected": False,
            "issue84_target_used": False,
            "semantic_or_image_context_used": False,
            "hand_or_latent_state_used": False,
        },
    }


def self_test() -> dict:
    if EXPECTED_CURRIER_GATE_SHA != "e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e":
        raise AssertionError("Currier authority SHA changed")
    x = empty_cell()
    x["accepted_edge_targets"] = 2
    x["previous_terminal_classes"].update((97, 98))
    x["current_initial_outcomes"].update((99, 100))
    x["terminal_initial_pairs"].add((97, 99))
    y = freeze_cell(x)
    if y["n_previous_terminal_classes"] != 2 or y["n_current_initial_outcomes"] != 2:
        raise AssertionError("support freeze failed")
    return {
        "ok": True,
        "score_free": True,
        "phase3a_authority_sha_frozen": True,
        "probabilities_computed": False,
        "likelihoods_computed": False,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--audit", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.audit is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    out = audit(Path(ns.audit[0]))
    Path(ns.audit[1]).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "gate_pass": out["gate_pass"],
        "gate_rule": out["gate_rule"],
        "phase3a_currier_authority": out["phase3a_currier_authority"],
        "all_cells_nonzero": out["all_cells_nonzero"],
        "global_class_support": out["global_class_support"],
        "edge_support_by_currier_and_fold": out["edge_support_by_currier_and_fold"],
        "global_edge_support": out["global_edge_support"],
        "firewall": out["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
