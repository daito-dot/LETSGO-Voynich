#!/usr/bin/env python3
"""Issue #118 residual-capacity first reveal.

Compares matched B3+byte mixtures where the byte expert either resets at every
visible-space token or carries byte context across tokens on the same physical
leaf. Model selection is inner-fold likelihood only. No latent state is fit.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve()
PRED = HERE.parents[1]
ORDER_DIR = PRED / "order-correction"
C1_PATH = ORDER_DIR / "rerun_phase1_source_order.py"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402


def load_c1():
    spec = importlib.util.spec_from_file_location("issue118_c1_authority", C1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import corrected Phase-1 authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


C1 = load_c1()
P1 = C1.P1
LN2 = math.log(2.0)
W_GRID = np.asarray([round(i / 100.0, 2) for i in range(101)], dtype=float)
TIE_EPS = 1e-12
EXPECTED_CORE_SHA = "0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27"
NORMALIZED_PATH = "recency_selection.3.candidate_table[88].total_log_likelihood"
NORMALIZED_VALUE = -131278.47048215955
NORMALIZED_TOL = 1e-9


def serialized_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_core_authority(core: dict) -> dict:
    """Apply only merged Gate-0 Amendment A and recover the original full SHA."""
    raw_text = serialized_json(core)
    raw_sha = sha256_text(raw_text)
    normalized = copy.deepcopy(core)
    row = normalized["recency_selection"]["3"]["candidate_table"][88]
    if not (row["H"] == 40 and row["tau"] == 64 and abs(float(row["pi"]) - 0.26) <= 1e-15):
        raise RuntimeError(f"Gate-0 normalization row identity changed: {row}")
    observed = float(row["total_log_likelihood"])
    if abs(observed - NORMALIZED_VALUE) > NORMALIZED_TOL:
        raise RuntimeError(
            f"Gate-0 known floating cell moved beyond tolerance: {observed} vs {NORMALIZED_VALUE}"
        )
    row["total_log_likelihood"] = NORMALIZED_VALUE
    normalized_text = serialized_json(normalized)
    normalized_sha = sha256_text(normalized_text)
    if normalized_sha != EXPECTED_CORE_SHA:
        raise RuntimeError(
            f"corrected core/support regression: normalized SHA {normalized_sha} != {EXPECTED_CORE_SHA}"
        )
    return {
        "valid": True,
        "raw_sha256": raw_sha,
        "normalized_sha256": normalized_sha,
        "normalization_path": NORMALIZED_PATH,
        "raw_normalization_value": observed,
        "authority_normalization_value": NORMALIZED_VALUE,
        "absolute_normalization_delta": abs(observed - NORMALIZED_VALUE),
    }


def select_byte_issue118(rows: Sequence[dict]) -> dict:
    """Frozen Issue #118 tie rule: smaller k, then larger alpha."""
    best = None
    for row in rows:
        rec = {
            "k": int(row["k"]),
            "alpha": float(row["alpha"]),
            "log_likelihood": float(row["total_log_likelihood"]),
        }
        if best is None or rec["log_likelihood"] > best["log_likelihood"] + TIE_EPS:
            best = rec
            continue
        if abs(rec["log_likelihood"] - best["log_likelihood"]) <= TIE_EPS:
            if rec["k"] < best["k"]:
                best = rec
            elif rec["k"] == best["k"] and rec["alpha"] > best["alpha"] + TIE_EPS:
                best = rec
    if best is None:
        raise RuntimeError("empty byte candidate table")
    return best


def token_byte_logps(model, items, parsed, reset_each_token: bool, k: int, alpha: float):
    """Selected byte-expert log p(token), preserving all visible history."""
    accepted: List[float] = []
    n_visible = 0
    current_leaf = None
    history: List[int] = []

    for it in P1.I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            history = []
        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                if reset_each_token:
                    history = []
                ll = 0.0
                for sym in P1.token_symbols(tok):
                    ll += model.logp(history, sym, int(k), float(alpha))
                    history.append(int(sym))
                    if len(history) > model.max_k:
                        history = history[-model.max_k :]
                n_visible += 1
                if parsed[it.item_id][li][ti] is not None:
                    accepted.append(float(ll))

    arr = np.asarray(accepted, dtype=float)
    if len(arr) == 0 or not np.all(np.isfinite(arr)):
        raise RuntimeError("invalid selected byte token log probabilities")
    return arr, int(n_visible)


def mixed_logps(log_core: np.ndarray, log_byte: np.ndarray, w: float) -> np.ndarray:
    if len(log_core) != len(log_byte):
        raise RuntimeError("core/byte target population mismatch")
    if w <= 0.0:
        return log_core.copy()
    if w >= 1.0:
        return log_byte.copy()
    return np.logaddexp(math.log1p(-float(w)) + log_core, math.log(float(w)) + log_byte)


def bits_from_logs(logp: np.ndarray) -> float:
    if len(logp) == 0 or not np.all(np.isfinite(logp)):
        raise RuntimeError("invalid log-probability vector")
    return float(-np.mean(logp) / LN2)


def select_weight(total_ll: np.ndarray) -> dict:
    if len(total_ll) != len(W_GRID) or not np.all(np.isfinite(total_ll)):
        raise RuntimeError("invalid mixture likelihood grid")
    best_i = 0
    best_ll = float(total_ll[0])
    for i in range(1, len(W_GRID)):
        ll = float(total_ll[i])
        if ll > best_ll + TIE_EPS:
            best_i, best_ll = i, ll
        elif abs(ll - best_ll) <= TIE_EPS and W_GRID[i] < W_GRID[best_i]:
            best_i, best_ll = i, ll
    return {"w": float(W_GRID[best_i]), "log_likelihood": best_ll}


def core_probs_for_split(
    vitems,
    folds,
    parsed,
    excluded_folds: Sequence[int],
    eval_fold: int,
    parser,
    rec_sel: dict,
    state_sel: dict,
):
    tr, v2, index = P1.fit_training(vitems, folds, parsed, excluded_folds)
    ev = P1.I.b.by_leaves(vitems, folds[eval_fold], include=True)
    models = P1.build_state_models(tr, parsed)
    sf = P1.state_feature_rows(ev, parsed, v2, index, parser, rec_sel["B2"], models)
    probs = P1.state_probs(sf, float(rec_sel["B2"]["pi"]), state_sel["selected"])
    if len(probs) != sf["n_scored"] or np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
        raise RuntimeError("invalid B3 probability vector")
    return tr, ev, np.asarray(probs, dtype=float)


def issue118_byte_selection(core: dict, outer_f: int, family: str) -> dict:
    rows = core["byte_selection"][str(outer_f)]["tables"][family]
    selected = select_byte_issue118(rows)
    legacy = core["byte_selection"][str(outer_f)][family]
    return {
        **selected,
        "matches_phase1_selection": bool(
            int(selected["k"]) == int(legacy["k"])
            and abs(float(selected["alpha"]) - float(legacy["alpha"])) <= TIE_EPS
        ),
    }


def tune_outer_weights(vitems, folds, parsed, outer_f: int, parser, core: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    byte_sel = {
        fam: issue118_byte_selection(core, outer_f, fam)
        for fam in ("RESET", "CONTINUOUS")
    }
    totals = {fam: np.zeros(len(W_GRID), dtype=float) for fam in byte_sel}
    inner = []

    for inner_g in range(P1.N_FOLDS):
        if inner_g == outer_f:
            continue
        tr, va, p_core = core_probs_for_split(
            vitems, folds, parsed, (outer_f, inner_g), inner_g, parser, rec_sel, state_sel
        )
        log_core = np.log(p_core)
        detail = {
            "inner_fold": int(inner_g),
            "n_scored": int(len(log_core)),
            "core_bits_per_token": bits_from_logs(log_core),
        }
        for fam, reset in (("RESET", True), ("CONTINUOUS", False)):
            sel = byte_sel[fam]
            model = P1.train_byte_family(tr, reset)
            log_byte, n_visible = token_byte_logps(
                model, va, parsed, reset, int(sel["k"]), float(sel["alpha"])
            )
            if len(log_byte) != len(log_core):
                raise RuntimeError(f"inner support mismatch outer={outer_f} inner={inner_g} {fam}")
            for wi, w in enumerate(W_GRID):
                totals[fam][wi] += float(np.sum(mixed_logps(log_core, log_byte, float(w))))
            detail[fam] = {
                "n_accepted": int(len(log_byte)),
                "n_visible": int(n_visible),
                "byte_bits_per_token": bits_from_logs(log_byte),
            }
        inner.append(detail)

    tuned = {fam: select_weight(totals[fam]) for fam in totals}
    return byte_sel, tuned, inner


def score_outer(vitems, folds, parsed, outer_f: int, parser, core: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    byte_sel, tuned, inner = tune_outer_weights(vitems, folds, parsed, outer_f, parser, core)

    tr, test, p_core = core_probs_for_split(
        vitems, folds, parsed, (outer_f,), outer_f, parser, rec_sel, state_sel
    )
    log_core = np.log(p_core)
    bits_core = bits_from_logs(log_core)
    authority_bits = float(core["outer"][outer_f]["B3"]["bits_per_token"])
    if abs(bits_core - authority_bits) > 1e-12:
        raise RuntimeError(f"outer B3 regression fold {outer_f}: {bits_core} != {authority_bits}")

    experts = {}
    for fam, reset in (("RESET", True), ("CONTINUOUS", False)):
        sel = byte_sel[fam]
        model = P1.train_byte_family(tr, reset)
        log_byte, n_visible = token_byte_logps(
            model, test, parsed, reset, int(sel["k"]), float(sel["alpha"])
        )
        if len(log_byte) != len(log_core):
            raise RuntimeError(f"outer support mismatch fold={outer_f} {fam}")
        w = float(tuned[fam]["w"])
        log_mix = mixed_logps(log_core, log_byte, w)
        experts[fam] = {
            "selected": {
                "k": int(sel["k"]),
                "alpha": float(sel["alpha"]),
                "w": w,
                "matches_phase1_byte_selection": bool(sel["matches_phase1_selection"]),
            },
            "byte_bits_per_token": bits_from_logs(log_byte),
            "mix_bits_per_token": bits_from_logs(log_mix),
            "n_accepted": int(len(log_byte)),
            "n_visible": int(n_visible),
            "inner_weight_log_likelihood": float(tuned[fam]["log_likelihood"]),
            "model_diagnostics": model.diagnostics(int(sel["k"])),
        }

    expected_n = int(core["outer"][outer_f]["n_scored"])
    expected_visible = int(core["outer"][outer_f]["n_visible"])
    for fam in experts:
        if experts[fam]["n_accepted"] != expected_n or experts[fam]["n_visible"] != expected_visible:
            raise RuntimeError(f"outer core/byte support regression fold={outer_f} {fam}")

    mix_reset = float(experts["RESET"]["mix_bits_per_token"])
    mix_cont = float(experts["CONTINUOUS"]["mix_bits_per_token"])
    return {
        "fold": int(outer_f),
        "n_scored": expected_n,
        "n_visible": expected_visible,
        "bits_B3": bits_core,
        "RESET": experts["RESET"],
        "CONTINUOUS": experts["CONTINUOUS"],
        "G_any": float(bits_core - mix_cont),
        "G_context": float(mix_reset - mix_cont),
        "inner": inner,
    }


def run(zl_path: Path) -> dict:
    # Gate must complete before any residual computation.
    try:
        core = C1.run(zl_path)
        core_authority = verify_core_authority(core)
    except Exception as exc:
        return {
            "schema": "issue118-residual-first-reveal-v1",
            "phase": "ISSUE118_RESIDUAL_GATE",
            "classification": "INVALID CORE / SUPPORT REGRESSION",
            "residual_scored": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    # C1.run already configured source order; explicitly retain the same adapter.
    P1.I.ordered = OA.ordered
    vitems, folds, parsed = P1.I.C.load_corpus(zl_path)
    if P1.P0.fold_hash(folds) != core["fold_identity_sha256"]:
        raise RuntimeError("fold identity changed after core verification")
    parser = P1.I.e.SlotParser()
    P1.I.e.validate_parser(parser)

    outer = [score_outer(vitems, folds, parsed, f, parser, core) for f in range(P1.N_FOLDS)]
    g_context = [float(r["G_context"]) for r in outer]
    g_any = [float(r["G_any"]) for r in outer]
    context_stability = P1.stability(g_context)
    any_stability = P1.stability(g_any)

    if context_stability["pass"]:
        classification = "ROBUST FLEXIBLE SEQUENCE RESIDUAL EXISTS — LOCALIZATION REQUIRED"
    else:
        classification = "NO ROBUST FLEXIBLE SEQUENCE RESIDUAL BEYOND CORRECTED CORE"

    return P1.canonicalize({
        "schema": "issue118-residual-first-reveal-v1",
        "phase": "ISSUE118_RESIDUAL_GATE",
        "classification": classification,
        "residual_scored": True,
        "source": {
            "git_blob_sha1": P1.I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": P1.EXPECTED_ZL3B_BLOB,
        },
        "fold_identity_sha256": core["fold_identity_sha256"],
        "core_authority": core_authority,
        "core_mean_bits_per_token": core["summaries"]["mean_bits_per_token"],
        "grids": {
            "byte_k": list(P1.BYTE_K_GRID),
            "byte_alpha": list(P1.BYTE_ALPHA_GRID),
            "mixture_w": [float(x) for x in W_GRID],
        },
        "outer": outer,
        "summaries": {
            "G_any": any_stability,
            "G_context": context_stability,
            "mean_bits_per_token": {
                "B3": float(np.mean([r["bits_B3"] for r in outer])),
                "MIX_RESET": float(np.mean([r["RESET"]["mix_bits_per_token"] for r in outer])),
                "MIX_CONT": float(np.mean([r["CONTINUOUS"]["mix_bits_per_token"] for r in outer])),
            },
        },
        "selection_rule": {
            "byte": "max inner accepted-token log likelihood; tie smaller k then larger alpha",
            "mixture": "max pooled inner accepted-token log likelihood; tie smaller w",
        },
        "firewall": {
            "latent_state_fit": False,
            "surface_scorecard_used_for_selection": False,
            "semantic_or_image_context_used": False,
            "segmentation_changed": False,
            "candidate_grid_extended": False,
            "future_outer_targets_used_for_selection": False,
        },
        "interpretation_boundary": {
            "entropy_bound_claimed": False,
            "semantic_state_identified": False,
            "plaintext_recovered": False,
            "decipherment_established": False,
        },
        "secondary_localization_status": "NON_AUTHORITATIVE_DIAGNOSTICS_PENDING_PRIMARY_REVEAL",
    })


def self_test() -> dict:
    rows = [
        {"k": 2, "alpha": 0.01, "total_log_likelihood": -10.0},
        {"k": 1, "alpha": 0.01, "total_log_likelihood": -10.0},
        {"k": 1, "alpha": 1.0, "total_log_likelihood": -10.0},
    ]
    sel = select_byte_issue118(rows)
    if sel["k"] != 1 or abs(sel["alpha"] - 1.0) > 1e-12:
        raise AssertionError(f"byte tie rule failed: {sel}")

    wsel = select_weight(np.zeros(len(W_GRID), dtype=float))
    if abs(wsel["w"]) > 1e-12:
        raise AssertionError(f"weight tie rule failed: {wsel}")

    lc = np.log(np.asarray([0.2, 0.3], dtype=float))
    lb = np.log(np.asarray([0.4, 0.1], dtype=float))
    if not np.allclose(mixed_logps(lc, lb, 0.0), lc):
        raise AssertionError("w=0 mixture failed")
    if not np.allclose(mixed_logps(lc, lb, 1.0), lb):
        raise AssertionError("w=1 mixture failed")
    half = mixed_logps(lc, lb, 0.5)
    if not np.allclose(np.exp(half), np.asarray([0.3, 0.2])):
        raise AssertionError("w=.5 mixture failed")

    base = C1.self_test()
    if not base.get("ok"):
        raise AssertionError("corrected Phase-1 base self-test failed")
    return {
        "ok": True,
        "corrected_core_self_test": True,
        "byte_tie_rule": True,
        "weight_tie_rule": True,
        "log_space_mixture": True,
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
        "residual_scored": out.get("residual_scored", False),
        "core_authority": out.get("core_authority"),
        "summaries": out.get("summaries"),
        "outer": [
            {
                "fold": r["fold"],
                "B3": r["bits_B3"],
                "RESET": r["RESET"]["selected"],
                "CONTINUOUS": r["CONTINUOUS"]["selected"],
                "G_any": r["G_any"],
                "G_context": r["G_context"],
            }
            for r in out.get("outer", [])
        ],
    }, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
