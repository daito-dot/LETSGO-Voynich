#!/usr/bin/env python3
"""Issue #121 residual localization L1: same-order boundary-edge control."""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Sequence

import numpy as np

HERE = Path(__file__).resolve()
R_PATH = HERE.parent / "residual_first_reveal.py"


def load_residual():
    spec = importlib.util.spec_from_file_location("issue121_residual_anchor", R_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Issue118 residual authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


R = load_residual()
P1 = R.P1
C1 = R.C1
OA = R.OA
FIXED_K = 2
FIXED_ALPHA = 0.01
LN2 = math.log(2.0)
RELATIONS = (
    "LEAF_START",
    "SAME_LINE",
    "CROSS_LINE_SAME_ITEM",
    "CROSS_ITEM_SAME_DOCUMENT",
    "CROSS_DOCUMENT_SAME_LEAF",
)
PARA_STATES = ("ENTRY", "BODY")
LINE_STATES = ("FIRST", "MIDDLE", "FINAL", "SINGLE")


def relation_label(prev, it, li: int) -> str:
    if prev is None:
        return "LEAF_START"
    if prev["item_id"] == it.item_id and prev["line_index"] == li:
        return "SAME_LINE"
    if prev["item_id"] == it.item_id:
        return "CROSS_LINE_SAME_ITEM"
    document = getattr(it, "document", getattr(it, "page", None))
    if prev["document"] == document:
        return "CROSS_ITEM_SAME_DOCUMENT"
    return "CROSS_DOCUMENT_SAME_LEAF"


def token_byte_records(model, items, parsed, reset_each_token: bool):
    records = []
    current_leaf = None
    history: List[int] = []
    prev = None
    n_visible = 0

    for it in P1.I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            history = []
            prev = None
        document = getattr(it, "document", getattr(it, "page", None))
        for li, line in enumerate(it.lines):
            para_state = "ENTRY" if li == 0 else "BODY"
            line_state = P1.line4_state(it, li)
            for ti, tok in enumerate(line):
                rel = relation_label(prev, it, li)
                if reset_each_token:
                    history = []
                ll = 0.0
                for sym in P1.token_symbols(tok):
                    ll += model.logp(history, sym, FIXED_K, FIXED_ALPHA)
                    history.append(int(sym))
                    if len(history) > model.max_k:
                        history = history[-model.max_k :]
                n_visible += 1
                if parsed[it.item_id][li][ti] is not None:
                    records.append({
                        "logp": float(ll),
                        "relation": rel,
                        "paragraph_state": para_state,
                        "line_state": line_state,
                    })
                prev = {
                    "item_id": it.item_id,
                    "document": document,
                    "line_index": int(li),
                }

    if not records or not all(math.isfinite(r["logp"]) for r in records):
        raise RuntimeError("invalid fixed-k2 byte records")
    return records, int(n_visible)


def tune_weights(vitems, folds, parsed, outer_f: int, parser, core: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    totals = {
        "RESET2": np.zeros(len(R.W_GRID), dtype=float),
        "CONT2": np.zeros(len(R.W_GRID), dtype=float),
    }
    inner = []

    for inner_g in range(P1.N_FOLDS):
        if inner_g == outer_f:
            continue
        tr, va, p_core = R.core_probs_for_split(
            vitems, folds, parsed, (outer_f, inner_g), inner_g, parser, rec_sel, state_sel
        )
        log_core = np.log(p_core)
        detail = {
            "inner_fold": int(inner_g),
            "n_scored": int(len(log_core)),
            "core_bits_per_token": R.bits_from_logs(log_core),
        }
        for fam, reset in (("RESET2", True), ("CONT2", False)):
            model = P1.train_byte_family(tr, reset)
            log_byte, n_visible = R.token_byte_logps(
                model, va, parsed, reset, FIXED_K, FIXED_ALPHA
            )
            if len(log_byte) != len(log_core):
                raise RuntimeError(f"inner support mismatch outer={outer_f} inner={inner_g} {fam}")
            for wi, w in enumerate(R.W_GRID):
                totals[fam][wi] += float(np.sum(R.mixed_logps(log_core, log_byte, float(w))))
            detail[fam] = {
                "n_accepted": int(len(log_byte)),
                "n_visible": int(n_visible),
                "byte_bits_per_token": R.bits_from_logs(log_byte),
            }
        inner.append(detail)

    return {fam: R.select_weight(totals[fam]) for fam in totals}, inner


def aggregate_delta(delta: np.ndarray, records: Sequence[dict], field: str, universe: Sequence[str]) -> dict:
    if len(delta) != len(records):
        raise RuntimeError("diagnostic length mismatch")
    out = {}
    for label in universe:
        vals = [float(delta[i]) for i, r in enumerate(records) if r[field] == label]
        out[label] = {
            "n": int(len(vals)),
            "total_delta_bits": float(sum(vals)),
            "mean_delta_bits": float(sum(vals) / len(vals)) if vals else None,
        }
    unknown = sorted({str(r[field]) for r in records} - set(universe))
    if unknown:
        raise RuntimeError(f"unexpected {field} labels: {unknown}")
    return out


def pool_aggregates(outer: Sequence[dict], path: str, universe: Sequence[str]) -> dict:
    out = {}
    for label in universe:
        n = 0
        total = 0.0
        for r in outer:
            table = r["diagnostics"][path]
            n += int(table[label]["n"])
            total += float(table[label]["total_delta_bits"])
        out[label] = {
            "n": int(n),
            "total_delta_bits": float(total),
            "mean_delta_bits": float(total / n) if n else None,
        }
    return out


def score_outer(vitems, folds, parsed, outer_f: int, parser, core: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    weights, inner = tune_weights(vitems, folds, parsed, outer_f, parser, core)

    tr, test, p_core = R.core_probs_for_split(
        vitems, folds, parsed, (outer_f,), outer_f, parser, rec_sel, state_sel
    )
    log_core = np.log(p_core)
    bits_core = R.bits_from_logs(log_core)
    authority_bits = float(core["outer"][outer_f]["B3"]["bits_per_token"])
    if abs(bits_core - authority_bits) > 1e-12:
        raise RuntimeError(f"B3 regression fold {outer_f}: {bits_core} != {authority_bits}")

    records_by_family = {}
    experts = {}
    for fam, reset in (("RESET2", True), ("CONT2", False)):
        model = P1.train_byte_family(tr, reset)
        records, n_visible = token_byte_records(model, test, parsed, reset)
        log_byte = np.asarray([r["logp"] for r in records], dtype=float)
        if len(log_byte) != len(log_core):
            raise RuntimeError(f"outer support mismatch fold={outer_f} {fam}")
        w = float(weights[fam]["w"])
        log_mix = R.mixed_logps(log_core, log_byte, w)
        experts[fam] = {
            "selected": {"k": FIXED_K, "alpha": FIXED_ALPHA, "w": w},
            "byte_bits_per_token": R.bits_from_logs(log_byte),
            "mix_bits_per_token": R.bits_from_logs(log_mix),
            "n_accepted": int(len(log_byte)),
            "n_visible": int(n_visible),
            "inner_weight_log_likelihood": float(weights[fam]["log_likelihood"]),
            "model_diagnostics": model.diagnostics(FIXED_K),
            "log_mix": log_mix,
        }
        records_by_family[fam] = records

    reset_records = records_by_family["RESET2"]
    cont_records = records_by_family["CONT2"]
    reset_key = [(r["relation"], r["paragraph_state"], r["line_state"]) for r in reset_records]
    cont_key = [(r["relation"], r["paragraph_state"], r["line_state"]) for r in cont_records]
    if reset_key != cont_key:
        raise RuntimeError("RESET2/CONT2 target metadata alignment mismatch")

    expected_n = int(core["outer"][outer_f]["n_scored"])
    expected_visible = int(core["outer"][outer_f]["n_visible"])
    for fam in experts:
        if experts[fam]["n_accepted"] != expected_n or experts[fam]["n_visible"] != expected_visible:
            raise RuntimeError(f"support regression fold={outer_f} {fam}")

    log_reset = experts["RESET2"].pop("log_mix")
    log_cont = experts["CONT2"].pop("log_mix")
    delta_bits = (log_cont - log_reset) / LN2
    mix_reset = float(experts["RESET2"]["mix_bits_per_token"])
    mix_cont = float(experts["CONT2"]["mix_bits_per_token"])
    g_edge = float(mix_reset - mix_cont)
    if abs(float(np.mean(delta_bits)) - g_edge) > 1e-12:
        raise RuntimeError("per-target diagnostic does not sum to G_edge")

    diagnostics = {
        "transition_relation": aggregate_delta(delta_bits, reset_records, "relation", RELATIONS),
        "paragraph_state": aggregate_delta(delta_bits, reset_records, "paragraph_state", PARA_STATES),
        "line_state": aggregate_delta(delta_bits, reset_records, "line_state", LINE_STATES),
    }

    return {
        "fold": int(outer_f),
        "n_scored": expected_n,
        "n_visible": expected_visible,
        "bits_B3": bits_core,
        "RESET2": experts["RESET2"],
        "CONT2": experts["CONT2"],
        "G_edge": g_edge,
        "inner": inner,
        "diagnostics": diagnostics,
    }


def run(zl_path: Path) -> dict:
    try:
        core = C1.run(zl_path)
        core_authority = R.verify_core_authority(core)
    except Exception as exc:
        return {
            "schema": "issue121-boundary-edge-l1-v1",
            "phase": "ISSUE121_L1",
            "classification": "INVALID CORE / SUPPORT REGRESSION",
            "scored": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    P1.I.ordered = OA.ordered
    vitems, folds, parsed = P1.I.C.load_corpus(zl_path)
    if P1.P0.fold_hash(folds) != core["fold_identity_sha256"]:
        raise RuntimeError("fold identity changed")
    parser = P1.I.e.SlotParser()
    P1.I.e.validate_parser(parser)

    outer = [score_outer(vitems, folds, parsed, f, parser, core) for f in range(P1.N_FOLDS)]
    g = [float(r["G_edge"]) for r in outer]
    stable = P1.stability(g)
    if stable["pass"]:
        classification = "BOUNDARY-EDGE RESIDUAL SURVIVES SAME-ORDER CONTROL"
    else:
        classification = "ISSUE118 RESIDUAL DEPENDS ON MODEL-ORDER ASYMMETRY"

    pooled = {
        "transition_relation": pool_aggregates(outer, "transition_relation", RELATIONS),
        "paragraph_state": pool_aggregates(outer, "paragraph_state", PARA_STATES),
        "line_state": pool_aggregates(outer, "line_state", LINE_STATES),
    }

    return P1.canonicalize({
        "schema": "issue121-boundary-edge-l1-v1",
        "phase": "ISSUE121_L1",
        "classification": classification,
        "scored": True,
        "fixed_byte_expert": {"k": FIXED_K, "alpha": FIXED_ALPHA},
        "source": {
            "git_blob_sha1": P1.I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": P1.EXPECTED_ZL3B_BLOB,
        },
        "fold_identity_sha256": core["fold_identity_sha256"],
        "core_authority": core_authority,
        "outer": outer,
        "summaries": {
            "G_edge": stable,
            "mean_bits_per_token": {
                "B3": float(np.mean([r["bits_B3"] for r in outer])),
                "MIX_RESET2": float(np.mean([r["RESET2"]["mix_bits_per_token"] for r in outer])),
                "MIX_CONT2": float(np.mean([r["CONT2"]["mix_bits_per_token"] for r in outer])),
            },
        },
        "pooled_diagnostics": pooled,
        "diagnostic_status": "NON_AUTHORITATIVE_NO_REFIT_NO_CLASSIFICATION_INPUT",
        "firewall": {
            "latent_state_fit": False,
            "byte_hyperparameter_selected_from_L1_outer": False,
            "segmentation_changed": False,
            "observable_regime_conditioned_primary_model": False,
            "semantic_or_image_context_used": False,
        },
    })


def self_test() -> dict:
    base = R.self_test()
    if not base.get("ok"):
        raise AssertionError("Issue118 anchor self-test failed")
    class Fake:
        item_id = "a"
        document = "d"
    f = Fake()
    if relation_label(None, f, 0) != "LEAF_START":
        raise AssertionError("leaf-start relation failed")
    prev = {"item_id": "a", "document": "d", "line_index": 0}
    if relation_label(prev, f, 0) != "SAME_LINE":
        raise AssertionError("same-line relation failed")
    if relation_label(prev, f, 1) != "CROSS_LINE_SAME_ITEM":
        raise AssertionError("cross-line relation failed")
    a = np.asarray([1.0, -1.0, 2.0])
    rec = [
        {"relation":"SAME_LINE","paragraph_state":"BODY","line_state":"MIDDLE"},
        {"relation":"LEAF_START","paragraph_state":"ENTRY","line_state":"FIRST"},
        {"relation":"SAME_LINE","paragraph_state":"BODY","line_state":"FINAL"},
    ]
    agg = aggregate_delta(a, rec, "relation", RELATIONS)
    if agg["SAME_LINE"]["n"] != 2 or abs(agg["SAME_LINE"]["mean_delta_bits"] - 1.5) > 1e-12:
        raise AssertionError("diagnostic aggregation failed")
    return {
        "ok": True,
        "issue118_anchor": True,
        "fixed_k": FIXED_K,
        "fixed_alpha": FIXED_ALPHA,
        "transition_taxonomy": True,
        "target_result_calls": 0,
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
    Path(ns.run[1]).write_text(
        json.dumps(out, indent=2, sort_keys=True, allow_nan=False, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "classification": out["classification"],
        "scored": out.get("scored", False),
        "G_edge": out.get("summaries", {}).get("G_edge"),
        "mean_bits": out.get("summaries", {}).get("mean_bits_per_token"),
        "weights": {
            str(r["fold"]): {"RESET2": r["RESET2"]["selected"], "CONT2": r["CONT2"]["selected"]}
            for r in out.get("outer", [])
        },
        "pooled_diagnostics": out.get("pooled_diagnostics"),
    }, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
