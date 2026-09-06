#!/usr/bin/env python3
"""Issue #123 residual localization L2: source-line reset scope."""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import List, Sequence

import numpy as np

HERE = Path(__file__).resolve()
L1_PATH = HERE.parent / "boundary_edge_l1.py"


def load_l1():
    spec = importlib.util.spec_from_file_location("issue123_l1_anchor", L1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Issue121 L1 authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


L1 = load_l1()
R = L1.R
P1 = L1.P1
C1 = L1.C1
OA = L1.OA
FIXED_K = 2
FIXED_ALPHA = 0.01
LN2 = math.log(2.0)
POLICIES = ("RESET2", "LINECONT2", "LEAFCONT2")
PARA_STATES = ("ENTRY", "BODY")
LINE_STATES = ("FIRST", "MIDDLE", "FINAL", "SINGLE")
PARENT_G_EDGE = (
    0.013939262960121823,
    0.00811504079524461,
    0.00930042233496664,
    0.010865786933976551,
    0.010940638641795175,
)
PARENT_RESET_W = (0.04, 0.04, 0.04, 0.04, 0.04)
PARENT_LEAF_W = (0.08, 0.08, 0.09, 0.08, 0.09)


def train_line_family(items):
    """Train the Phase-1 byte family with history reset at every source line."""
    model = P1.ByteNGramFamily(max(P1.BYTE_K_GRID))
    current_leaf = None
    for it in P1.I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
        for line in it.lines:
            history: List[int] = []
            for tok in line:
                for sym in P1.token_symbols(tok):
                    model.observe_symbol(history, sym)
                    history.append(int(sym))
                    if len(history) > model.max_k:
                        history = history[-model.max_k :]
    return model


def train_policy(items, policy: str):
    if policy == "RESET2":
        return P1.train_byte_family(items, True)
    if policy == "LEAFCONT2":
        return P1.train_byte_family(items, False)
    if policy == "LINECONT2":
        return train_line_family(items)
    raise ValueError(f"unknown policy {policy}")


def line_token_logps(model, items, parsed):
    accepted: List[float] = []
    n_visible = 0
    current_leaf = None
    for it in P1.I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
        for li, line in enumerate(it.lines):
            history: List[int] = []
            for ti, tok in enumerate(line):
                ll = 0.0
                for sym in P1.token_symbols(tok):
                    ll += model.logp(history, sym, FIXED_K, FIXED_ALPHA)
                    history.append(int(sym))
                    if len(history) > model.max_k:
                        history = history[-model.max_k :]
                n_visible += 1
                if parsed[it.item_id][li][ti] is not None:
                    accepted.append(float(ll))
    arr = np.asarray(accepted, dtype=float)
    if len(arr) == 0 or not np.all(np.isfinite(arr)):
        raise RuntimeError("invalid LINECONT2 token log probabilities")
    return arr, int(n_visible)


def token_logps_policy(model, items, parsed, policy: str):
    if policy == "RESET2":
        return R.token_byte_logps(model, items, parsed, True, FIXED_K, FIXED_ALPHA)
    if policy == "LEAFCONT2":
        return R.token_byte_logps(model, items, parsed, False, FIXED_K, FIXED_ALPHA)
    if policy == "LINECONT2":
        return line_token_logps(model, items, parsed)
    raise ValueError(f"unknown policy {policy}")


def target_state_records(items, parsed):
    out = []
    for it in P1.I.ordered(items):
        for li, line in enumerate(it.lines):
            para = "ENTRY" if li == 0 else "BODY"
            line_state = P1.line4_state(it, li)
            for ti, _tok in enumerate(line):
                if parsed[it.item_id][li][ti] is not None:
                    out.append({"paragraph_state": para, "line_state": line_state})
    return out


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


def pool_aggregates(outer: Sequence[dict], comparison: str, field: str, universe: Sequence[str]) -> dict:
    out = {}
    for label in universe:
        n = 0
        total = 0.0
        for r in outer:
            cell = r["diagnostics"][comparison][field][label]
            n += int(cell["n"])
            total += float(cell["total_delta_bits"])
        out[label] = {
            "n": int(n),
            "total_delta_bits": float(total),
            "mean_delta_bits": float(total / n) if n else None,
        }
    return out


def tune_weights(vitems, folds, parsed, outer_f: int, parser, core: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    totals = {p: np.zeros(len(R.W_GRID), dtype=float) for p in POLICIES}
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
        for policy in POLICIES:
            model = train_policy(tr, policy)
            log_byte, n_visible = token_logps_policy(model, va, parsed, policy)
            if len(log_byte) != len(log_core):
                raise RuntimeError(f"inner support mismatch outer={outer_f} inner={inner_g} {policy}")
            for wi, w in enumerate(R.W_GRID):
                totals[policy][wi] += float(np.sum(R.mixed_logps(log_core, log_byte, float(w))))
            detail[policy] = {
                "n_accepted": int(len(log_byte)),
                "n_visible": int(n_visible),
                "byte_bits_per_token": R.bits_from_logs(log_byte),
            }
        inner.append(detail)

    return {p: R.select_weight(totals[p]) for p in POLICIES}, inner


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

    experts = {}
    log_mix = {}
    for policy in POLICIES:
        model = train_policy(tr, policy)
        log_byte, n_visible = token_logps_policy(model, test, parsed, policy)
        if len(log_byte) != len(log_core):
            raise RuntimeError(f"outer support mismatch fold={outer_f} {policy}")
        w = float(weights[policy]["w"])
        lm = R.mixed_logps(log_core, log_byte, w)
        log_mix[policy] = lm
        experts[policy] = {
            "selected": {"k": FIXED_K, "alpha": FIXED_ALPHA, "w": w},
            "byte_bits_per_token": R.bits_from_logs(log_byte),
            "mix_bits_per_token": R.bits_from_logs(lm),
            "n_accepted": int(len(log_byte)),
            "n_visible": int(n_visible),
            "inner_weight_log_likelihood": float(weights[policy]["log_likelihood"]),
            "model_diagnostics": model.diagnostics(FIXED_K),
        }

    expected_n = int(core["outer"][outer_f]["n_scored"])
    expected_visible = int(core["outer"][outer_f]["n_visible"])
    for policy in POLICIES:
        if experts[policy]["n_accepted"] != expected_n or experts[policy]["n_visible"] != expected_visible:
            raise RuntimeError(f"support regression fold={outer_f} {policy}")

    bits_reset = float(experts["RESET2"]["mix_bits_per_token"])
    bits_line = float(experts["LINECONT2"]["mix_bits_per_token"])
    bits_leaf = float(experts["LEAFCONT2"]["mix_bits_per_token"])
    g_line = float(bits_reset - bits_line)
    g_beyond = float(bits_line - bits_leaf)
    g_parent = float(bits_reset - bits_leaf)

    records = target_state_records(test, parsed)
    if len(records) != expected_n:
        raise RuntimeError(f"target-state support mismatch fold={outer_f}")
    d_line = (log_mix["LINECONT2"] - log_mix["RESET2"]) / LN2
    d_beyond = (log_mix["LEAFCONT2"] - log_mix["LINECONT2"]) / LN2
    if abs(float(np.mean(d_line)) - g_line) > 1e-12:
        raise RuntimeError("G_line diagnostic sum mismatch")
    if abs(float(np.mean(d_beyond)) - g_beyond) > 1e-12:
        raise RuntimeError("G_beyond_line diagnostic sum mismatch")

    diagnostics = {
        "RESET2_TO_LINECONT2": {
            "paragraph_state": aggregate_delta(d_line, records, "paragraph_state", PARA_STATES),
            "line_state": aggregate_delta(d_line, records, "line_state", LINE_STATES),
        },
        "LINECONT2_TO_LEAFCONT2": {
            "paragraph_state": aggregate_delta(d_beyond, records, "paragraph_state", PARA_STATES),
            "line_state": aggregate_delta(d_beyond, records, "line_state", LINE_STATES),
        },
    }

    return {
        "fold": int(outer_f),
        "n_scored": expected_n,
        "n_visible": expected_visible,
        "bits_B3": bits_core,
        **experts,
        "G_line": g_line,
        "G_beyond_line": g_beyond,
        "G_parent_RESET2_vs_LEAFCONT2": g_parent,
        "inner": inner,
        "diagnostics": diagnostics,
    }


def verify_parent_regression(outer: Sequence[dict]) -> dict:
    for f, r in enumerate(outer):
        got = float(r["G_parent_RESET2_vs_LEAFCONT2"])
        if abs(got - PARENT_G_EDGE[f]) > 1e-12:
            raise RuntimeError(f"Issue121 G_edge regression fold {f}: {got} != {PARENT_G_EDGE[f]}")
        wr = float(r["RESET2"]["selected"]["w"])
        wl = float(r["LEAFCONT2"]["selected"]["w"])
        if abs(wr - PARENT_RESET_W[f]) > 1e-12:
            raise RuntimeError(f"Issue121 RESET2 weight regression fold {f}: {wr}")
        if abs(wl - PARENT_LEAF_W[f]) > 1e-12:
            raise RuntimeError(f"Issue121 LEAFCONT2 weight regression fold {f}: {wl}")
    return {
        "valid": True,
        "G_edge": [float(r["G_parent_RESET2_vs_LEAFCONT2"]) for r in outer],
        "RESET2_w": [float(r["RESET2"]["selected"]["w"]) for r in outer],
        "LEAFCONT2_w": [float(r["LEAFCONT2"]["selected"]["w"]) for r in outer],
    }


def run(zl_path: Path) -> dict:
    try:
        core = C1.run(zl_path)
        core_authority = R.verify_core_authority(core)
        P1.I.ordered = OA.ordered
        vitems, folds, parsed = P1.I.C.load_corpus(zl_path)
        if P1.P0.fold_hash(folds) != core["fold_identity_sha256"]:
            raise RuntimeError("fold identity changed")
        parser = P1.I.e.SlotParser()
        P1.I.e.validate_parser(parser)
        outer = [score_outer(vitems, folds, parsed, f, parser, core) for f in range(P1.N_FOLDS)]
        parent_regression = verify_parent_regression(outer)
    except Exception as exc:
        return {
            "schema": "issue123-line-reset-l2-v1",
            "phase": "ISSUE123_L2",
            "classification": "INVALID CORE / SUPPORT REGRESSION",
            "scored": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    g_line = [float(r["G_line"]) for r in outer]
    g_beyond = [float(r["G_beyond_line"]) for r in outer]
    s_line = P1.stability(g_line)
    s_beyond = P1.stability(g_beyond)

    if not s_line["pass"]:
        classification = "LINE-LOCAL CONTEXT FAILS TO REPRODUCE"
    elif s_beyond["pass"]:
        classification = "ROBUST BEYOND-LINE CONTEXT REMAINS"
    else:
        classification = "LINE-LOCAL CONTEXT CAPTURES RESIDUAL; NO ROBUST BEYOND-LINE GAIN"

    pooled = {
        comp: {
            "paragraph_state": pool_aggregates(outer, comp, "paragraph_state", PARA_STATES),
            "line_state": pool_aggregates(outer, comp, "line_state", LINE_STATES),
        }
        for comp in ("RESET2_TO_LINECONT2", "LINECONT2_TO_LEAFCONT2")
    }

    return P1.canonicalize({
        "schema": "issue123-line-reset-l2-v1",
        "phase": "ISSUE123_L2",
        "classification": classification,
        "scored": True,
        "fixed_byte_expert": {"k": FIXED_K, "alpha": FIXED_ALPHA},
        "source": {
            "git_blob_sha1": P1.I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": P1.EXPECTED_ZL3B_BLOB,
        },
        "fold_identity_sha256": core["fold_identity_sha256"],
        "core_authority": core_authority,
        "parent_issue121_regression": parent_regression,
        "outer": outer,
        "summaries": {
            "G_line": s_line,
            "G_beyond_line": s_beyond,
            "mean_bits_per_token": {
                "B3": float(np.mean([r["bits_B3"] for r in outer])),
                "MIX_RESET2": float(np.mean([r["RESET2"]["mix_bits_per_token"] for r in outer])),
                "MIX_LINECONT2": float(np.mean([r["LINECONT2"]["mix_bits_per_token"] for r in outer])),
                "MIX_LEAFCONT2": float(np.mean([r["LEAFCONT2"]["mix_bits_per_token"] for r in outer])),
            },
        },
        "pooled_diagnostics": pooled,
        "diagnostic_status": "NON_CLASSIFICATION_INPUT_EXCEPT_PREDECLARED_G_LINE_AND_G_BEYOND_LINE",
        "firewall": {
            "latent_state_fit": False,
            "byte_hyperparameter_selected_from_L2_outer": False,
            "reset_topology_selected_after_reveal": False,
            "segmentation_changed": False,
            "currier_hand_domain_conditioning": False,
            "semantic_or_image_context_used": False,
        },
    })


def self_test() -> dict:
    base = L1.self_test()
    if not base.get("ok"):
        raise AssertionError("Issue121 anchor self-test failed")
    if POLICIES != ("RESET2", "LINECONT2", "LEAFCONT2"):
        raise AssertionError("policy order changed")
    if FIXED_K != 2 or abs(FIXED_ALPHA - 0.01) > 1e-15:
        raise AssertionError("fixed byte expert changed")
    d = np.asarray([1.0, -1.0, 2.0])
    rec = [
        {"paragraph_state": "BODY", "line_state": "MIDDLE"},
        {"paragraph_state": "ENTRY", "line_state": "FIRST"},
        {"paragraph_state": "BODY", "line_state": "FINAL"},
    ]
    agg = aggregate_delta(d, rec, "paragraph_state", PARA_STATES)
    if agg["BODY"]["n"] != 2 or abs(agg["BODY"]["mean_delta_bits"] - 1.5) > 1e-12:
        raise AssertionError("diagnostic aggregation failed")
    return {
        "ok": True,
        "issue121_anchor": True,
        "fixed_k": FIXED_K,
        "fixed_alpha": FIXED_ALPHA,
        "policies": list(POLICIES),
        "parent_regression_frozen": True,
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
    Path(ns.run[1]).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": out.get("classification"),
        "scored": out.get("scored"),
        "G_line": out.get("summaries", {}).get("G_line"),
        "G_beyond_line": out.get("summaries", {}).get("G_beyond_line"),
        "mean_bits": out.get("summaries", {}).get("mean_bits_per_token"),
        "weights": {
            str(r["fold"]): {p: r[p]["selected"] for p in POLICIES}
            for r in out.get("outer", [])
        },
        "pooled_diagnostics": out.get("pooled_diagnostics"),
        "parent_issue121_regression": out.get("parent_issue121_regression"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
