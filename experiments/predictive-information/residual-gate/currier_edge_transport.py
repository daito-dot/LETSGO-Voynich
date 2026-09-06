#!/usr/bin/env python3
"""Issue #127 L4: Currier transport of the explicit terminal→initial edge."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Sequence

import numpy as np

HERE = Path(__file__).resolve()
EDGE_PATH = HERE.parent / "explicit_edge_l3.py"
GATE_PATH = HERE.parent / "currier_edge_gate0.py"
EXPECTED_GATE_SHA = "31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb"
RHO_GRID = np.asarray([i / 100.0 for i in range(101)], dtype=float)
TIE_EPS = 1e-12
LN2 = math.log(2.0)
DIRECTIONS = (("A", "B"), ("B", "A"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


L3 = load_module("issue127_l3_anchor", EDGE_PATH)
GATE = load_module("issue127_gate_anchor", GATE_PATH)
P1 = L3.P1
OA = L3.OA
FIXED_K = L3.FIXED_K
FIXED_ALPHA = L3.FIXED_ALPHA


def json_sha256(x: dict) -> str:
    raw = (json.dumps(x, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def label_items(items, by_doc: dict, label: str):
    out = []
    for it in items:
        rec = by_doc.get(it.document)
        if rec is None:
            raise RuntimeError(f"document absent from Currier authority: {it.document}")
        if rec["label"] == label:
            out.append(it)
    return out


def exclude_folds(items, folds, excluded: Sequence[int]):
    leaves = set()
    for f in excluded:
        leaves.update(int(x) for x in folds[int(f)])
    return [it for it in items if int(it.leaf) not in leaves]


def include_fold(items, folds, fold: int):
    leaves = set(int(x) for x in folds[int(fold)])
    return [it for it in items if int(it.leaf) in leaves]


def mixed_logps(log_pos: np.ndarray, log_edge: np.ndarray, rho: float) -> np.ndarray:
    rho = float(rho)
    if rho <= 0.0:
        return np.asarray(log_pos, dtype=float).copy()
    if rho >= 1.0:
        return np.asarray(log_edge, dtype=float).copy()
    return np.logaddexp(math.log1p(-rho) + log_pos, math.log(rho) + log_edge)


def bits(logp: np.ndarray) -> float:
    if len(logp) == 0 or not np.all(np.isfinite(logp)):
        raise RuntimeError("invalid log-probability vector")
    return float(-np.mean(logp) / LN2)


def select_rho(total_ll: np.ndarray) -> dict:
    if total_ll.shape != (len(RHO_GRID),):
        raise RuntimeError("rho grid shape mismatch")
    best_i = 0
    best_ll = float(total_ll[0])
    for i in range(1, len(RHO_GRID)):
        ll = float(total_ll[i])
        if ll > best_ll + TIE_EPS:
            best_i, best_ll = i, ll
        # ties deliberately retain the smaller rho because grid is ascending
    return {"rho": float(RHO_GRID[best_i]), "log_likelihood": best_ll}


def ll_grid(log_pos: np.ndarray, log_edge: np.ndarray) -> np.ndarray:
    if len(log_pos) != len(log_edge):
        raise RuntimeError("POS/EDGE support mismatch")
    return np.asarray([
        float(np.sum(mixed_logps(log_pos, log_edge, float(rho))))
        for rho in RHO_GRID
    ], dtype=float)


def cross_edge_token_logp(target_model, source_model, syms, prev_final: int):
    """Target-local POS2 factors with only first-symbol edge table imported from source."""
    syms = [int(x) for x in syms]
    if len(syms) < 2:
        raise RuntimeError("invalid token symbols")
    first, second = syms[0], syms[1]
    src_counter = source_model.prev_terminal_first.get(int(prev_final))
    fallback = src_counter is None or int(sum(src_counter.values())) <= 0
    if fallback:
        ll = target_model._smoothed_logp(target_model.line_body_first, first)
    else:
        ll = source_model._smoothed_logp(src_counter, first)
    ll += target_model._smoothed_logp(target_model.line_body_second[first], second)
    for j in range(2, len(syms)):
        ll += target_model.line_model.logp(syms[j - 2:j], syms[j], FIXED_K, FIXED_ALPHA)
    return float(ll), bool(fallback)


def score_linebody(target_model, items, parsed, source_model=None):
    """Score accepted current tokens after the first visible token of each source line."""
    pos = []
    native = []
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
            prev_final = int(prev_syms[-2])
            for ti in range(1, len(line)):
                tok = line[ti]
                syms = P1.token_symbols(tok)
                if len(syms) < 2:
                    raise RuntimeError("visible token lacks raw byte")
                visible_edges += 1
                if parsed[it.item_id][li][ti] is not None:
                    lp_pos = target_model.token_logp(syms, False, prev_final, use_identity=False)
                    lp_native = target_model.token_logp(syms, False, prev_final, use_identity=True)
                    pos.append(float(lp_pos))
                    native.append(float(lp_native))
                    if source_model is not None:
                        lp_cross, used_fallback = cross_edge_token_logp(target_model, source_model, syms, prev_final)
                        transferred.append(float(lp_cross))
                        fallback += int(used_fallback)
                    accepted += 1
                prev_final = int(syms[-2])
    pos = np.asarray(pos, dtype=float)
    native = np.asarray(native, dtype=float)
    transferred = np.asarray(transferred, dtype=float) if source_model is not None else None
    if accepted <= 0 or len(pos) != accepted or len(native) != accepted:
        raise RuntimeError("empty or inconsistent line-body support")
    if source_model is not None and len(transferred) != accepted:
        raise RuntimeError("transferred edge support mismatch")
    if not np.all(np.isfinite(pos)) or not np.all(np.isfinite(native)):
        raise RuntimeError("nonfinite native score")
    if transferred is not None and not np.all(np.isfinite(transferred)):
        raise RuntimeError("nonfinite transferred score")
    return {
        "POS2": pos,
        "NATIVE_EDGE": native,
        "SOURCE_EDGE": transferred,
        "n_accepted": int(accepted),
        "n_visible_edges": int(visible_edges),
        "fallback_count": int(fallback),
        "fallback_rate": float(fallback / accepted) if source_model is not None else None,
    }


def source_rho_cv(source_items, folds, parsed) -> dict:
    total = np.zeros(len(RHO_GRID), dtype=float)
    detail = []
    for g in range(P1.N_FOLDS):
        tr = exclude_folds(source_items, folds, (g,))
        va = include_fold(source_items, folds, g)
        model = L3.ExplicitOnsetModel(tr)
        sc = score_linebody(model, va, parsed)
        total += ll_grid(sc["POS2"], sc["NATIVE_EDGE"])
        detail.append({
            "fold": int(g),
            "n_accepted": sc["n_accepted"],
            "POS2_bits": bits(sc["POS2"]),
            "NATIVE_EDGE_bits": bits(sc["NATIVE_EDGE"]),
        })
    selected = select_rho(total)
    return {
        "selected": selected,
        "folds": detail,
        "rho_table": [
            {"rho": float(rho), "pooled_log_likelihood": float(total[i])}
            for i, rho in enumerate(RHO_GRID)
        ],
    }


def target_inner_rhos(target_items, source_full_model, folds, parsed, outer_f: int) -> dict:
    table_total = np.zeros(len(RHO_GRID), dtype=float)
    oracle_total = np.zeros(len(RHO_GRID), dtype=float)
    detail = []
    for g in range(P1.N_FOLDS):
        if g == outer_f:
            continue
        tr = exclude_folds(target_items, folds, (outer_f, g))
        va = include_fold(target_items, folds, g)
        target_model = L3.ExplicitOnsetModel(tr)
        sc = score_linebody(target_model, va, parsed, source_full_model)
        table_total += ll_grid(sc["POS2"], sc["SOURCE_EDGE"])
        oracle_total += ll_grid(sc["POS2"], sc["NATIVE_EDGE"])
        detail.append({
            "inner_fold": int(g),
            "n_accepted": sc["n_accepted"],
            "source_context_fallback_count": sc["fallback_count"],
            "source_context_fallback_rate": sc["fallback_rate"],
        })
    return {
        "source_table_target_rho": select_rho(table_total),
        "target_oracle_rho": select_rho(oracle_total),
        "inner": detail,
    }


def score_target_outer(source_label: str, target_label: str, source_items, target_items, folds, parsed, source_full_model, source_rho: float, outer_f: int, gate: dict) -> dict:
    tr = exclude_folds(target_items, folds, (outer_f,))
    test = include_fold(target_items, folds, outer_f)
    target_model = L3.ExplicitOnsetModel(tr)
    selected = target_inner_rhos(target_items, source_full_model, folds, parsed, outer_f)
    sc = score_linebody(target_model, test, parsed, source_full_model)

    expected_n = int(gate["edge_support_by_currier_and_fold"][target_label][str(outer_f)]["accepted_edge_targets"])
    expected_visible = int(gate["edge_support_by_currier_and_fold"][target_label][str(outer_f)]["visible_edge_events"])
    if sc["n_accepted"] != expected_n or sc["n_visible_edges"] != expected_visible:
        raise RuntimeError(
            f"Gate support regression {source_label}->{target_label} fold{outer_f}: "
            f"{sc['n_accepted']}/{sc['n_visible_edges']} != {expected_n}/{expected_visible}"
        )

    rho_table = float(selected["source_table_target_rho"]["rho"])
    rho_oracle = float(selected["target_oracle_rho"]["rho"])
    models = {
        "POS2": sc["POS2"],
        "FULL_TRANSFER": mixed_logps(sc["POS2"], sc["SOURCE_EDGE"], source_rho),
        "SOURCE_TABLE_TARGET_RHO": mixed_logps(sc["POS2"], sc["SOURCE_EDGE"], rho_table),
        "TARGET_TABLE_SOURCE_RHO": mixed_logps(sc["POS2"], sc["NATIVE_EDGE"], source_rho),
        "TARGET_ORACLE": mixed_logps(sc["POS2"], sc["NATIVE_EDGE"], rho_oracle),
    }
    b = {name: bits(logp) for name, logp in models.items()}
    gains = {
        "G_full": float(b["POS2"] - b["FULL_TRANSFER"]),
        "G_table": float(b["POS2"] - b["SOURCE_TABLE_TARGET_RHO"]),
        "G_strength": float(b["POS2"] - b["TARGET_TABLE_SOURCE_RHO"]),
        "G_oracle": float(b["POS2"] - b["TARGET_ORACLE"]),
    }
    return {
        "fold": int(outer_f),
        "source": source_label,
        "target": target_label,
        "n_accepted": sc["n_accepted"],
        "n_visible_edges": sc["n_visible_edges"],
        "source_rho": float(source_rho),
        "source_table_target_rho": rho_table,
        "target_oracle_rho": rho_oracle,
        "source_context_fallback_count": sc["fallback_count"],
        "source_context_fallback_rate": sc["fallback_rate"],
        "bits_per_token": b,
        **gains,
        "inner_selection": selected,
        "target_training_diagnostics": target_model.diagnostics(),
    }


def stability(vals: Sequence[float]) -> dict:
    x = [float(v) for v in vals]
    return {
        "values": x,
        "mean": float(np.mean(x)),
        "positive_folds": int(sum(v > 0.0 for v in x)),
        "pass": bool(float(np.mean(x)) > 0.0 and sum(v > 0.0 for v in x) >= 4),
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
        gate_sha = GATE.json_sha256(gate)
        if gate_sha != EXPECTED_GATE_SHA or not gate["gate_pass"]:
            raise RuntimeError(f"Issue127 Gate0 authority regression: {gate_sha}")

        headers = GATE.G0.parse_source_headers(zl_path)
        by_doc = {r["document"]: r for r in headers}
        OA.configure(zl_path)
        items, folds, parsed = P1.I.C.load_corpus(zl_path)
        order_verify = OA.verify(items)
        P1.I.ordered = OA.ordered
        if P1.P0.fold_hash(folds) != gate["phase3a_currier_authority"]["fold_identity_sha256"]:
            raise RuntimeError("fold identity changed")
        if not order_verify["numeric_paragraph_order_valid"] or not order_verify["source_document_order_valid"]:
            raise RuntimeError("source-order authority failed")

        by_label = {lab: label_items(items, by_doc, lab) for lab in ("A", "B")}
        source_cv = {lab: source_rho_cv(by_label[lab], folds, parsed) for lab in ("A", "B")}
        source_full_models = {lab: L3.ExplicitOnsetModel(by_label[lab]) for lab in ("A", "B")}

        directions = {}
        for source_label, target_label in DIRECTIONS:
            rho_s = float(source_cv[source_label]["selected"]["rho"])
            outer = [
                score_target_outer(
                    source_label, target_label,
                    by_label[source_label], by_label[target_label], folds, parsed,
                    source_full_models[source_label], rho_s, f, gate,
                )
                for f in range(P1.N_FOLDS)
            ]
            summaries = {
                key: stability([r[key] for r in outer])
                for key in ("G_full", "G_table", "G_strength", "G_oracle")
            }
            summaries["mean_bits_per_token"] = {
                name: float(np.mean([r["bits_per_token"][name] for r in outer]))
                for name in ("POS2", "FULL_TRANSFER", "SOURCE_TABLE_TARGET_RHO", "TARGET_TABLE_SOURCE_RHO", "TARGET_ORACLE")
            }
            directions[f"{source_label}_to_{target_label}"] = {
                "source": source_label,
                "target": target_label,
                "source_rho": rho_s,
                "source_table_diagnostics": source_full_models[source_label].diagnostics(),
                "outer": outer,
                "summaries": summaries,
                "fallback": {
                    "count": int(sum(r["source_context_fallback_count"] for r in outer)),
                    "n": int(sum(r["n_accepted"] for r in outer)),
                    "rate": float(
                        sum(r["source_context_fallback_count"] for r in outer)
                        / sum(r["n_accepted"] for r in outer)
                    ),
                },
            }

        a2b = directions["A_to_B"]["summaries"]
        b2a = directions["B_to_A"]["summaries"]
        classes = {
            "TABLE_TRANSPORT": directional_class(a2b["G_table"]["pass"], b2a["G_table"]["pass"]),
            "EXACT_TRANSPORT": directional_class(a2b["G_full"]["pass"], b2a["G_full"]["pass"]),
            "SOURCE_STRENGTH_COMPATIBILITY": directional_class(a2b["G_strength"]["pass"], b2a["G_strength"]["pass"]),
            "TARGET_NATIVE_EDGE": {
                "A": bool(b2a["G_oracle"]["pass"]),
                "B": bool(a2b["G_oracle"]["pass"]),
            },
        }
    except Exception as exc:
        return {
            "schema": "issue127-currier-edge-transport-v1",
            "phase": "ISSUE127_L4_TRANSPORT",
            "classification": "INVALID GATE / SUPPORT REGRESSION",
            "scored": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    return P1.canonicalize({
        "schema": "issue127-currier-edge-transport-v1",
        "phase": "ISSUE127_L4_TRANSPORT",
        "classification": classes,
        "scored": True,
        "mechanism_only": True,
        "fixed": {
            "k": FIXED_K,
            "alpha": FIXED_ALPHA,
            "rho_grid": [float(x) for x in RHO_GRID],
            "source_context_fallback": "TARGET_POS2_LINE_BODY_FIRST",
            "score_support": "PARSER_ACCEPTED_LINE_BODY_CURRENT_TOKENS",
        },
        "gate_authority": {
            "json_sha256": gate_sha,
            "expected_json_sha256": EXPECTED_GATE_SHA,
            "gate_pass": gate["gate_pass"],
            "phase3a_currier_json_sha256": gate["phase3a_currier_authority"]["json_sha256"],
            "fold_identity_sha256": gate["phase3a_currier_authority"]["fold_identity_sha256"],
        },
        "order_authority": order_verify,
        "source_rho_cv": source_cv,
        "directions": directions,
        "firewall": {
            "target_outer_used_for_selection": False,
            "source_POS2_imported_to_target": False,
            "alpha_or_k_tuned": False,
            "rho_grid_extended": False,
            "B3_refit_or_scored": False,
            "latent_state_fit": False,
            "hand_domain_semantic_conditioning": False,
            "issue84_target_used": False,
            "plaintext_language_cipher_claim": False,
        },
    })


def self_test() -> dict:
    if EXPECTED_GATE_SHA != "31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb":
        raise AssertionError("Gate SHA changed")
    if FIXED_K != 2 or abs(FIXED_ALPHA - 0.01) > 1e-15:
        raise AssertionError("fixed edge model changed")
    a = np.log(np.asarray([0.2, 0.4], dtype=float))
    b = np.log(np.asarray([0.6, 0.2], dtype=float))
    if not np.allclose(mixed_logps(a, b, 0.0), a):
        raise AssertionError("rho=0 mixture failed")
    if not np.allclose(mixed_logps(a, b, 1.0), b):
        raise AssertionError("rho=1 mixture failed")
    mid = np.exp(mixed_logps(a, b, 0.5))
    if not np.allclose(mid, np.asarray([0.4, 0.3])):
        raise AssertionError("rho mixture normalization failed")
    ll = np.zeros(len(RHO_GRID)); ll[17] = 1.0
    if select_rho(ll)["rho"] != 0.17:
        raise AssertionError("rho selection failed")
    return {
        "ok": True,
        "mechanism_only": True,
        "fixed_k": FIXED_K,
        "fixed_alpha": FIXED_ALPHA,
        "rho_grid_n": len(RHO_GRID),
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
        "source_rho": {
            lab: out.get("source_rho_cv", {}).get(lab, {}).get("selected")
            for lab in ("A", "B")
        },
        "directions": {
            key: {
                "summaries": val["summaries"],
                "fallback": val["fallback"],
                "outer_rhos": [
                    {
                        "fold": r["fold"],
                        "source_rho": r["source_rho"],
                        "source_table_target_rho": r["source_table_target_rho"],
                        "target_oracle_rho": r["target_oracle_rho"],
                    }
                    for r in val["outer"]
                ],
            }
            for key, val in out.get("directions", {}).items()
        },
        "gate_authority": out.get("gate_authority"),
        "firewall": out.get("firewall"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
