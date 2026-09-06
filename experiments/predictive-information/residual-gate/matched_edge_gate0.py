#!/usr/bin/env python3
"""Issue #130 L4b Gate0: outcome-blind context-matched Currier edge support."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
PARENT_PATH = HERE.parent / "currier_edge_gate0.py"
EXPECTED_PARENT_SHA = "31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb"
SEEDS = tuple(f"issue130-match-v1-r{i}" for i in range(5))
LABELS = ("A", "B")


def load_parent():
    spec = importlib.util.spec_from_file_location("issue130_parent_gate", PARENT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Issue127 Gate0")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


PARENT = load_parent()
P1 = PARENT.P1
OA = PARENT.OA


def event_hash(seed: str, label: str, context: int, event_id: str) -> str:
    raw = f"{seed}|{label}|{int(context)}|{event_id}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def selection_digest(event_ids) -> str:
    raw = "\n".join(sorted(event_ids)).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def build_events(zl_path: Path):
    headers = PARENT.G0.parse_source_headers(zl_path)
    by_doc = {r["document"]: r for r in headers}
    OA.configure(zl_path)
    items, folds, _parsed = P1.I.C.load_corpus(zl_path)
    order_verify = OA.verify(items)
    P1.I.ordered = OA.ordered

    fold_of_leaf = {}
    for f, leaves in enumerate(folds):
        for leaf in leaves:
            fold_of_leaf[int(leaf)] = int(f)

    events = {lab: defaultdict(list) for lab in LABELS}
    for it in P1.I.ordered(items):
        rec = by_doc.get(it.document)
        if rec is None:
            raise RuntimeError(f"document absent from Currier authority: {it.document}")
        lab = rec["label"]
        if lab not in LABELS:
            continue
        leaf = int(it.leaf)
        if leaf not in fold_of_leaf:
            raise RuntimeError(f"leaf absent from fold authority: {leaf}")
        for li, line in enumerate(it.lines):
            if len(line) < 2:
                continue
            prev_syms = P1.token_symbols(line[0])
            if len(prev_syms) < 2:
                raise RuntimeError("visible token lacks raw byte")
            prev_terminal = int(prev_syms[-2])
            for ti in range(1, len(line)):
                event_id = f"{it.document}|{it.item_id}|{li}|{ti}|{prev_terminal}"
                events[lab][prev_terminal].append({
                    "event_id": event_id,
                    "document": it.document,
                    "leaf": leaf,
                    "fold": int(fold_of_leaf[leaf]),
                    "previous_terminal": prev_terminal,
                })
                syms = P1.token_symbols(line[ti])
                if len(syms) < 2:
                    raise RuntimeError("visible token lacks raw byte")
                prev_terminal = int(syms[-2])
    return events, folds, order_verify


def choose(events_for_context, seed: str, label: str, context: int, n: int):
    ranked = sorted(
        events_for_context,
        key=lambda e: (event_hash(seed, label, context, e["event_id"]), e["event_id"]),
    )
    if n < 0 or n > len(ranked):
        raise RuntimeError("invalid matched selection size")
    return ranked[:n]


def audit(zl_path: Path) -> dict:
    parent = PARENT.audit(zl_path)
    parent_sha = PARENT.json_sha256(parent)
    if parent_sha != EXPECTED_PARENT_SHA or not parent["gate_pass"]:
        raise RuntimeError(f"Issue127 Gate0 authority regression: {parent_sha}")

    events, folds, order_verify = build_events(zl_path)
    contexts_a = set(events["A"])
    contexts_b = set(events["B"])
    shared = sorted(contexts_a & contexts_b)
    only_a = sorted(contexts_a - contexts_b)
    only_b = sorted(contexts_b - contexts_a)
    match = {
        str(c): {
            "A": int(len(events["A"][c])),
            "B": int(len(events["B"][c])),
            "matched": int(min(len(events["A"][c]), len(events["B"][c]))),
        }
        for c in shared
    }
    matched_total = int(sum(v["matched"] for v in match.values()))
    original_total = {
        lab: int(sum(len(v) for v in events[lab].values()))
        for lab in LABELS
    }

    selections = {}
    deterministic_repeat_ok = True
    for seed in SEEDS:
        seed_out = {}
        for lab in LABELS:
            chosen = []
            by_context = {}
            for c in shared:
                n = match[str(c)]["matched"]
                selected = choose(events[lab][c], seed, lab, c, n)
                repeated = choose(events[lab][c], seed, lab, c, n)
                if [e["event_id"] for e in selected] != [e["event_id"] for e in repeated]:
                    deterministic_repeat_ok = False
                chosen.extend(selected)
                by_context[str(c)] = int(len(selected))
            fold_counts = {str(f): 0 for f in range(P1.N_FOLDS)}
            leaves = set()
            docs = set()
            for e in chosen:
                fold_counts[str(e["fold"])] += 1
                leaves.add(int(e["leaf"]))
                docs.add(e["document"])
            ids = [e["event_id"] for e in chosen]
            seed_out[lab] = {
                "selected_total": int(len(chosen)),
                "selected_by_context": by_context,
                "selection_digest_sha256": selection_digest(ids),
                "selected_fold_counts": fold_counts,
                "selected_leaf_count": int(len(leaves)),
                "selected_document_count": int(len(docs)),
            }
        selections[seed] = seed_out

    equal_context_counts = True
    equal_totals = True
    for seed in SEEDS:
        if selections[seed]["A"]["selected_total"] != matched_total or selections[seed]["B"]["selected_total"] != matched_total:
            equal_totals = False
        for c in shared:
            n = match[str(c)]["matched"]
            if selections[seed]["A"]["selected_by_context"][str(c)] != n:
                equal_context_counts = False
            if selections[seed]["B"]["selected_by_context"][str(c)] != n:
                equal_context_counts = False

    gate_pass = bool(
        parent_sha == EXPECTED_PARENT_SHA
        and parent["gate_pass"]
        and len(shared) >= 2
        and matched_total > 0
        and equal_context_counts
        and equal_totals
        and deterministic_repeat_ok
        and order_verify["numeric_paragraph_order_valid"]
        and order_verify["source_document_order_valid"]
    )

    return {
        "schema": "issue130-matched-edge-gate0-v1",
        "phase": "ISSUE130_L4B_GATE0",
        "gate_pass": gate_pass,
        "gate_rule": "PROCEED_TO_MATCHED_TABLE_TRANSPORT" if gate_pass else "STOP_BEFORE_MATCHED_TRANSPORT",
        "parent_gate": {
            "json_sha256": parent_sha,
            "expected_json_sha256": EXPECTED_PARENT_SHA,
            "gate_pass": parent["gate_pass"],
            "phase3a_currier_json_sha256": parent["phase3a_currier_authority"]["json_sha256"],
        },
        "fold_identity_sha256": P1.P0.fold_hash(folds),
        "order_authority": order_verify,
        "seeds": list(SEEDS),
        "shared_previous_terminal_classes": shared,
        "A_only_previous_terminal_classes": only_a,
        "B_only_previous_terminal_classes": only_b,
        "n_shared_previous_terminal_classes": int(len(shared)),
        "original_visible_edge_events": original_total,
        "context_match_counts": match,
        "matched_total_per_regime_per_seed": matched_total,
        "equal_context_counts": equal_context_counts,
        "equal_totals": equal_totals,
        "deterministic_repeat_ok": deterministic_repeat_ok,
        "selections": selections,
        "firewall": {
            "current_initial_outcomes_used_for_selection": False,
            "current_initial_distributions_reported": False,
            "edge_probabilities_computed": False,
            "predictive_scores_computed": False,
            "rho_selected": False,
            "transport_gain_computed": False,
            "latent_or_semantic_variable_used": False,
        },
    }


def self_test() -> dict:
    e = [
        {"event_id": "x", "fold": 0, "leaf": 1, "document": "d"},
        {"event_id": "y", "fold": 0, "leaf": 1, "document": "d"},
        {"event_id": "z", "fold": 0, "leaf": 1, "document": "d"},
    ]
    a = choose(e, SEEDS[0], "A", 97, 2)
    b = choose(e, SEEDS[0], "A", 97, 2)
    if [x["event_id"] for x in a] != [x["event_id"] for x in b]:
        raise AssertionError("hash selection is not deterministic")
    if len(a) != 2:
        raise AssertionError("selection size failed")
    if EXPECTED_PARENT_SHA != "31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb":
        raise AssertionError("parent Gate SHA changed")
    return {
        "ok": True,
        "score_free": True,
        "seed_count": len(SEEDS),
        "outcome_blind_event_identity": True,
        "predictive_result_calls": 0,
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
        "parent_gate": out["parent_gate"],
        "n_shared_previous_terminal_classes": out["n_shared_previous_terminal_classes"],
        "original_visible_edge_events": out["original_visible_edge_events"],
        "matched_total_per_regime_per_seed": out["matched_total_per_regime_per_seed"],
        "equal_context_counts": out["equal_context_counts"],
        "equal_totals": out["equal_totals"],
        "deterministic_repeat_ok": out["deterministic_repeat_ok"],
        "selections": out["selections"],
        "firewall": out["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
