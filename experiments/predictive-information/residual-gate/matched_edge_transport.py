#!/usr/bin/env python3
"""Issue #130 L4b: support-matched Currier edge-table transport."""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

import numpy as np

HERE = Path(__file__).resolve()
GATE_PATH = HERE.parent / "matched_edge_gate0.py"
PARENT_PATH = HERE.parent / "currier_edge_transport.py"
EXPECTED_GATE_SHA = "a0f48878506369aa9dff60e06b60be13d41d36dd1ceef3a40c4fc63825db66f5"
EXPECTED_PARENT_GATE_SHA = "31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


GATE = load_module("issue130_matched_gate_anchor", GATE_PATH)
PARENT = load_module("issue130_parent_transport", PARENT_PATH)
P1 = PARENT.P1
OA = PARENT.OA
L3 = PARENT.L3
SEEDS = GATE.SEEDS
DIRECTIONS = PARENT.DIRECTIONS
FIXED_K = PARENT.FIXED_K
FIXED_ALPHA = PARENT.FIXED_ALPHA


class MatchedEdgeTable:
    """Outcome-attached source edge table over frozen Gate-selected loci only."""

    def __init__(self):
        self.prev_terminal_first = defaultdict(Counter)
        self.n_events = 0
        self.pairs = set()

    @staticmethod
    def _smoothed_logp(counter: Counter, sym: int) -> float:
        return L3.ExplicitOnsetModel._smoothed_logp(counter, sym)

    def add(self, previous_terminal: int, current_initial: int):
        p = int(previous_terminal)
        y = int(current_initial)
        self.prev_terminal_first[p][y] += 1
        self.n_events += 1
        self.pairs.add((p, y))

    def diagnostics(self) -> dict:
        return {
            "selected_events": int(self.n_events),
            "previous_terminal_contexts": int(len(self.prev_terminal_first)),
            "observed_terminal_initial_pairs": int(len(self.pairs)),
            "current_initial_outcomes": int(len({y for _p, y in self.pairs})),
            "context_counts": {
                str(p): int(sum(c.values()))
                for p, c in sorted(self.prev_terminal_first.items())
            },
        }


def build_outcome_map(zl_path: Path):
    headers = GATE.PARENT.G0.parse_source_headers(zl_path)
    by_doc = {r["document"]: r for r in headers}
    OA.configure(zl_path)
    items, folds, parsed = P1.I.C.load_corpus(zl_path)
    order_verify = OA.verify(items)
    P1.I.ordered = OA.ordered
    outcome = {"A": {}, "B": {}}
    for it in P1.I.ordered(items):
        rec = by_doc.get(it.document)
        if rec is None:
            raise RuntimeError(f"document absent from Currier authority: {it.document}")
        lab = rec["label"]
        if lab not in ("A", "B"):
            continue
        for li, line in enumerate(it.lines):
            if len(line) < 2:
                continue
            prev_syms = P1.token_symbols(line[0])
            if len(prev_syms) < 2:
                raise RuntimeError("visible token lacks raw byte")
            prev_terminal = int(prev_syms[-2])
            for ti in range(1, len(line)):
                syms = P1.token_symbols(line[ti])
                if len(syms) < 2:
                    raise RuntimeError("visible token lacks raw byte")
                event_id = f"{it.document}|{it.item_id}|{li}|{ti}|{prev_terminal}"
                if event_id in outcome[lab]:
                    raise RuntimeError(f"duplicate matched event identity: {event_id}")
                outcome[lab][event_id] = {
                    "previous_terminal": int(prev_terminal),
                    "current_initial": int(syms[0]),
                }
                prev_terminal = int(syms[-2])
    return outcome, items, folds, parsed, by_doc, order_verify


def build_matched_tables(zl_path: Path, gate: dict, outcome: dict):
    score_free_events, _folds, _order = GATE.build_events(zl_path)
    tables = {seed: {} for seed in SEEDS}
    provenance = {seed: {} for seed in SEEDS}

    for seed in SEEDS:
        for lab in ("A", "B"):
            table = MatchedEdgeTable()
            chosen_ids = []
            selected_by_context = {}
            for c in gate["shared_previous_terminal_classes"]:
                c = int(c)
                n = int(gate["context_match_counts"][str(c)]["matched"])
                selected = GATE.choose(score_free_events[lab][c], seed, lab, c, n)
                selected_by_context[str(c)] = int(len(selected))
                for e in selected:
                    eid = e["event_id"]
                    chosen_ids.append(eid)
                    attached = outcome[lab].get(eid)
                    if attached is None:
                        raise RuntimeError(f"selected event missing outcome attachment: {lab} {eid}")
                    if int(attached["previous_terminal"]) != c:
                        raise RuntimeError(f"selected event context drift: {lab} {eid}")
                    table.add(c, int(attached["current_initial"]))

            digest = GATE.selection_digest(chosen_ids)
            expected = gate["selections"][seed][lab]
            if digest != expected["selection_digest_sha256"]:
                raise RuntimeError(f"Gate selection digest mismatch {seed} {lab}: {digest}")
            if len(chosen_ids) != int(expected["selected_total"]):
                raise RuntimeError(f"Gate selected total mismatch {seed} {lab}")
            if selected_by_context != expected["selected_by_context"]:
                raise RuntimeError(f"Gate selected context mismatch {seed} {lab}")
            if table.n_events != int(gate["matched_total_per_regime_per_seed"]):
                raise RuntimeError(f"matched table event count mismatch {seed} {lab}")

            tables[seed][lab] = table
            provenance[seed][lab] = {
                "selection_digest_sha256": digest,
                "selected_total": int(len(chosen_ids)),
                "selected_by_context": selected_by_context,
                "table_diagnostics": table.diagnostics(),
            }

    return tables, provenance


def score_cross_linebody(target_model, items, parsed, source_table: MatchedEdgeTable):
    pos = []
    transferred = []
    accepted = 0
    visible_edges = 0
    fallback = 0
    for it in P1.I.ordered(items):
        for li, line in enumerate(it.lines):
            if len(line) < 2:
                continue
            prev_syms = P1.token_symbols(line[0])
            if len(prev_syms) < 2:
                raise RuntimeError("visible token lacks raw byte")
            prev_terminal = int(prev_syms[-2])
            for ti in range(1, len(line)):
                tok = line[ti]
                syms = P1.token_symbols(tok)
                if len(syms) < 2:
                    raise RuntimeError("visible token lacks raw byte")
                visible_edges += 1
                if parsed[it.item_id][li][ti] is not None:
                    lp_pos = target_model.token_logp(syms, False, prev_terminal, use_identity=False)
                    lp_cross, used_fallback = PARENT.cross_edge_token_logp(
                        target_model, source_table, syms, prev_terminal
                    )
                    pos.append(float(lp_pos))
                    transferred.append(float(lp_cross))
                    fallback += int(used_fallback)
                    accepted += 1
                prev_terminal = int(syms[-2])
    pos = np.asarray(pos, dtype=float)
    transferred = np.asarray(transferred, dtype=float)
    if accepted <= 0 or len(pos) != accepted or len(transferred) != accepted:
        raise RuntimeError("matched transport support mismatch")
    if not np.all(np.isfinite(pos)) or not np.all(np.isfinite(transferred)):
        raise RuntimeError("nonfinite matched transport score")
    return {
        "POS2": pos,
        "SOURCE_EDGE": transferred,
        "n_accepted": int(accepted),
        "n_visible_edges": int(visible_edges),
        "fallback_count": int(fallback),
        "fallback_rate": float(fallback / accepted),
    }


def target_inner_rho(target_items, source_table, folds, parsed, outer_f: int) -> dict:
    total = np.zeros(len(PARENT.RHO_GRID), dtype=float)
    detail = []
    for g in range(P1.N_FOLDS):
        if g == outer_f:
            continue
        tr = PARENT.exclude_folds(target_items, folds, (outer_f, g))
        va = PARENT.include_fold(target_items, folds, g)
        target_model = L3.ExplicitOnsetModel(tr)
        sc = score_cross_linebody(target_model, va, parsed, source_table)
        total += PARENT.ll_grid(sc["POS2"], sc["SOURCE_EDGE"])
        detail.append({
            "inner_fold": int(g),
            "n_accepted": sc["n_accepted"],
            "source_context_fallback_count": sc["fallback_count"],
            "source_context_fallback_rate": sc["fallback_rate"],
        })
    return {
        "selected": PARENT.select_rho(total),
        "inner": detail,
    }


def score_outer(source_label: str, target_label: str, target_items, source_table, folds, parsed, outer_f: int, parent_gate: dict):
    selected = target_inner_rho(target_items, source_table, folds, parsed, outer_f)
    tr = PARENT.exclude_folds(target_items, folds, (outer_f,))
    test = PARENT.include_fold(target_items, folds, outer_f)
    target_model = L3.ExplicitOnsetModel(tr)
    sc = score_cross_linebody(target_model, test, parsed, source_table)

    expected = parent_gate["edge_support_by_currier_and_fold"][target_label][str(outer_f)]
    if sc["n_accepted"] != int(expected["accepted_edge_targets"]):
        raise RuntimeError(f"accepted support regression {source_label}->{target_label} fold{outer_f}")
    if sc["n_visible_edges"] != int(expected["visible_edge_events"]):
        raise RuntimeError(f"visible support regression {source_label}->{target_label} fold{outer_f}")

    rho = float(selected["selected"]["rho"])
    mixed = PARENT.mixed_logps(sc["POS2"], sc["SOURCE_EDGE"], rho)
    pos_bits = PARENT.bits(sc["POS2"])
    mixed_bits = PARENT.bits(mixed)
    return {
        "fold": int(outer_f),
        "source": source_label,
        "target": target_label,
        "n_accepted": sc["n_accepted"],
        "n_visible_edges": sc["n_visible_edges"],
        "target_inner_rho": rho,
        "POS2_bits_per_token": pos_bits,
        "MATCHED_SOURCE_TABLE_bits_per_token": mixed_bits,
        "G_matched": float(pos_bits - mixed_bits),
        "source_context_fallback_count": sc["fallback_count"],
        "source_context_fallback_rate": sc["fallback_rate"],
        "inner_selection": selected,
    }


def seed_stability(values: Sequence[float]) -> dict:
    vals = [float(v) for v in values]
    mean = float(np.mean(vals))
    pos = int(sum(v > 0.0 for v in vals))
    return {
        "values": vals,
        "mean": mean,
        "positive_folds": pos,
        "pass": bool(mean > 0.0 and pos >= 4),
    }


def direction_summary(seed_results: dict) -> dict:
    all_gains = []
    seed_passes = 0
    for seed in SEEDS:
        s = seed_results[seed]["stability"]
        all_gains.extend(float(v) for v in s["values"])
        seed_passes += int(bool(s["pass"]))
    grand_mean = float(np.mean(all_gains))
    overall_pass = bool(seed_passes >= 4 and grand_mean > 0.0)
    return {
        "seed_passes": int(seed_passes),
        "n_seeds": int(len(SEEDS)),
        "grand_mean": grand_mean,
        "n_gains": int(len(all_gains)),
        "overall_pass": overall_pass,
        "all_seed_fold_gains": all_gains,
    }


def directional_class(a_to_b: bool, b_to_a: bool) -> str:
    if a_to_b and b_to_a:
        return "BIDIRECTIONAL"
    if a_to_b:
        return "A→B ONLY"
    if b_to_a:
        return "B→A ONLY"
    return "NONE"


def run(zl_path: Path) -> dict:
    try:
        gate = GATE.audit(zl_path)
        gate_sha = PARENT.json_sha256(gate)
        if gate_sha != EXPECTED_GATE_SHA or not gate["gate_pass"]:
            raise RuntimeError(f"Issue130 Gate authority regression: {gate_sha}")
        parent_gate = GATE.PARENT.audit(zl_path)
        parent_sha = GATE.PARENT.json_sha256(parent_gate)
        if parent_sha != EXPECTED_PARENT_GATE_SHA or not parent_gate["gate_pass"]:
            raise RuntimeError(f"Issue127 parent Gate authority regression: {parent_sha}")

        outcome, items, folds, parsed, by_doc, order_verify = build_outcome_map(zl_path)
        if P1.P0.fold_hash(folds) != parent_gate["phase3a_currier_authority"]["fold_identity_sha256"]:
            raise RuntimeError("fold identity changed")
        if not order_verify["numeric_paragraph_order_valid"] or not order_verify["source_document_order_valid"]:
            raise RuntimeError("source order authority failed")
        for lab in ("A", "B"):
            if len(outcome[lab]) != int(gate["original_visible_edge_events"][lab]):
                raise RuntimeError(f"outcome attachment population mismatch {lab}")

        tables, table_provenance = build_matched_tables(zl_path, gate, outcome)
        by_label = {lab: PARENT.label_items(items, by_doc, lab) for lab in ("A", "B")}

        directions = {}
        for source_label, target_label in DIRECTIONS:
            seed_results = {}
            for seed in SEEDS:
                table = tables[seed][source_label]
                outer = [
                    score_outer(
                        source_label, target_label, by_label[target_label], table,
                        folds, parsed, f, parent_gate,
                    )
                    for f in range(P1.N_FOLDS)
                ]
                stab = seed_stability([r["G_matched"] for r in outer])
                seed_results[seed] = {
                    "source_table": table_provenance[seed][source_label],
                    "outer": outer,
                    "stability": stab,
                    "mean_bits_per_token": {
                        "POS2": float(np.mean([r["POS2_bits_per_token"] for r in outer])),
                        "MATCHED_SOURCE_TABLE": float(np.mean([r["MATCHED_SOURCE_TABLE_bits_per_token"] for r in outer])),
                    },
                    "fallback": {
                        "count": int(sum(r["source_context_fallback_count"] for r in outer)),
                        "n": int(sum(r["n_accepted"] for r in outer)),
                        "rate": float(
                            sum(r["source_context_fallback_count"] for r in outer)
                            / sum(r["n_accepted"] for r in outer)
                        ),
                    },
                }
            directions[f"{source_label}_to_{target_label}"] = {
                "source": source_label,
                "target": target_label,
                "seeds": seed_results,
                "summary": direction_summary(seed_results),
            }

        a_pass = directions["A_to_B"]["summary"]["overall_pass"]
        b_pass = directions["B_to_A"]["summary"]["overall_pass"]
        classification = directional_class(a_pass, b_pass)
    except Exception as exc:
        return {
            "schema": "issue130-matched-edge-transport-v1",
            "phase": "ISSUE130_L4B_MATCHED_TRANSPORT",
            "classification": "INVALID MATCHED GATE / SUPPORT REGRESSION",
            "scored": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    return P1.canonicalize({
        "schema": "issue130-matched-edge-transport-v1",
        "phase": "ISSUE130_L4B_MATCHED_TRANSPORT",
        "classification": classification,
        "scored": True,
        "fixed": {
            "k": FIXED_K,
            "alpha": FIXED_ALPHA,
            "rho_grid": [float(x) for x in PARENT.RHO_GRID],
            "seeds": list(SEEDS),
            "seed_pass_rule": "mean_gt_0_and_positive_folds_ge_4_of_5",
            "direction_pass_rule": "seed_passes_ge_4_of_5_and_grand_mean_gt_0",
            "source_context_fallback": "TARGET_POS2_LINE_BODY_FIRST",
        },
        "gate_authority": {
            "json_sha256": gate_sha,
            "expected_json_sha256": EXPECTED_GATE_SHA,
            "gate_pass": gate["gate_pass"],
            "matched_total_per_regime_per_seed": gate["matched_total_per_regime_per_seed"],
            "n_shared_previous_terminal_classes": gate["n_shared_previous_terminal_classes"],
        },
        "parent_gate_authority": {
            "json_sha256": parent_sha,
            "expected_json_sha256": EXPECTED_PARENT_GATE_SHA,
            "gate_pass": parent_gate["gate_pass"],
        },
        "order_authority": order_verify,
        "directions": directions,
        "firewall": {
            "gate_selection_changed_after_outcome_attachment": False,
            "outcome_used_for_hash_selection": False,
            "target_outer_used_for_rho_selection": False,
            "source_POS2_imported_to_target": False,
            "alpha_k_or_rho_grid_tuned": False,
            "latent_state_fit": False,
            "hand_domain_semantic_conditioning": False,
            "issue84_target_used": False,
        },
    })


def self_test() -> dict:
    if EXPECTED_GATE_SHA != "a0f48878506369aa9dff60e06b60be13d41d36dd1ceef3a40c4fc63825db66f5":
        raise AssertionError("Issue130 Gate SHA changed")
    if EXPECTED_PARENT_GATE_SHA != "31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb":
        raise AssertionError("Issue127 parent Gate SHA changed")
    if len(SEEDS) != 5:
        raise AssertionError("seed count changed")
    x = MatchedEdgeTable()
    x.add(97, 111); x.add(97, 112); x.add(98, 111)
    d = x.diagnostics()
    if d["selected_events"] != 3 or d["previous_terminal_contexts"] != 2 or d["observed_terminal_initial_pairs"] != 3:
        raise AssertionError("matched table diagnostics failed")
    fake = {
        seed: {"stability": {"values": [1.0]*5, "pass": True}}
        for seed in SEEDS
    }
    s = direction_summary(fake)
    if not s["overall_pass"] or s["seed_passes"] != 5 or s["n_gains"] != 25:
        raise AssertionError("direction summary failed")
    return {
        "ok": True,
        "matched_gate_frozen": True,
        "seed_count": len(SEEDS),
        "outcome_blind_selection_reused": True,
        "target_outer_result_calls": 0,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.run is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    out = run(Path(ns.run[0]))
    Path(ns.run[1]).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": out.get("classification"),
        "scored": out.get("scored"),
        "gate_authority": out.get("gate_authority"),
        "directions": {
            key: {
                "summary": val["summary"],
                "seeds": {
                    seed: {
                        "stability": rec["stability"],
                        "mean_bits_per_token": rec["mean_bits_per_token"],
                        "fallback": rec["fallback"],
                        "outer_rhos": [
                            {"fold": r["fold"], "rho": r["target_inner_rho"]}
                            for r in rec["outer"]
                        ],
                    }
                    for seed, rec in val["seeds"].items()
                },
            }
            for key, val in out.get("directions", {}).items()
        },
        "firewall": out.get("firewall"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
