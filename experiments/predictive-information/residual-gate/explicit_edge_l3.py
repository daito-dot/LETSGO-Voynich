#!/usr/bin/env python3
"""Issue #125 L3: explicit line-position versus previous-terminal edge identity."""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Sequence

import numpy as np

HERE = Path(__file__).resolve()
L2_PATH = HERE.parent / "line_reset_l2.py"


def load_l2():
    spec = importlib.util.spec_from_file_location("issue125_l2_anchor", L2_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Issue123 L2 authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


L2 = load_l2()
L1 = L2.L1
R = L2.R
P1 = L2.P1
C1 = L2.C1
OA = L2.OA
FIXED_K = 2
FIXED_ALPHA = 0.01
LN2 = math.log(2.0)
EXPERTS = ("RESET2", "POS2", "EDGE2")
PARA_STATES = ("ENTRY", "BODY")
LINE_STATES = ("FIRST", "MIDDLE", "FINAL", "SINGLE")
PARENT_G_LINE = (
    0.03339038902518254,
    0.02093212050888482,
    0.03017008407788957,
    0.02839973265948892,
    0.03291474485290813,
)
PARENT_RESET_W = (0.04, 0.04, 0.04, 0.04, 0.04)
PARENT_EDGE_W = (0.15, 0.16, 0.15, 0.15, 0.15)
EQUIV_TOL = 1e-12


class ExplicitOnsetModel:
    """Exact factorization of fixed-k2 LINECONT2 plus a pooled-body POS2 variant."""

    def __init__(self, items):
        self.line_model = L2.train_line_family(items)
        self.line_start_first = Counter()
        self.line_body_first = Counter()
        self.prev_terminal_first = defaultdict(Counter)
        self.line_start_second = defaultdict(Counter)
        self.line_body_second = defaultdict(Counter)
        self.shared_within_contexts = set()
        self.line_start_tokens = 0
        self.line_body_tokens = 0

        for it in P1.I.ordered(items):
            for line in it.lines:
                prev_final = None
                for ti, tok in enumerate(line):
                    syms = P1.token_symbols(tok)
                    if len(syms) < 2:
                        raise RuntimeError("visible token has no raw byte before END_TOKEN")
                    first = int(syms[0])
                    second = int(syms[1])
                    if ti == 0:
                        self.line_start_tokens += 1
                        self.line_start_first[first] += 1
                        self.line_start_second[first][second] += 1
                    else:
                        if prev_final is None:
                            raise RuntimeError("missing previous terminal at line-body token")
                        self.line_body_tokens += 1
                        self.line_body_first[first] += 1
                        self.prev_terminal_first[int(prev_final)][first] += 1
                        self.line_body_second[first][second] += 1
                    for j in range(2, len(syms)):
                        self.shared_within_contexts.add((int(syms[j - 2]), int(syms[j - 1])))
                    prev_final = int(syms[-2])

        if self.line_start_tokens <= 0 or self.line_body_tokens <= 0:
            raise RuntimeError("empty onset population")

    @staticmethod
    def _smoothed_logp(counter: Counter, sym: int) -> float:
        total = int(sum(counter.values()))
        c = int(counter.get(int(sym), 0))
        return math.log((float(c) + FIXED_ALPHA) / (float(total) + FIXED_ALPHA * P1.BYTE_V))

    def token_logp(self, syms: Sequence[int], line_start: bool, prev_final: int | None, use_identity: bool) -> float:
        syms = [int(x) for x in syms]
        if len(syms) < 2:
            raise RuntimeError("invalid token symbol sequence")
        first, second = syms[0], syms[1]
        ll = 0.0

        if line_start:
            ll += self._smoothed_logp(self.line_start_first, first)
            ll += self._smoothed_logp(self.line_start_second[first], second)
        else:
            if prev_final is None:
                raise RuntimeError("line-body token lacks previous terminal")
            if use_identity:
                ll += self._smoothed_logp(self.prev_terminal_first[int(prev_final)], first)
            else:
                ll += self._smoothed_logp(self.line_body_first, first)
            ll += self._smoothed_logp(self.line_body_second[first], second)

        for j in range(2, len(syms)):
            ll += self.line_model.logp(syms[j - 2:j], syms[j], FIXED_K, FIXED_ALPHA)
        return float(ll)

    def diagnostics(self) -> dict:
        return {
            "line_start_tokens": int(self.line_start_tokens),
            "line_body_tokens": int(self.line_body_tokens),
            "line_start_first_outcomes": int(len(self.line_start_first)),
            "line_body_first_outcomes": int(len(self.line_body_first)),
            "previous_terminal_contexts": int(len(self.prev_terminal_first)),
            "previous_terminal_transitions": int(sum(len(c) for c in self.prev_terminal_first.values())),
            "line_start_second_contexts": int(len(self.line_start_second)),
            "line_body_second_contexts": int(len(self.line_body_second)),
            "shared_within_k2_contexts": int(len(self.shared_within_contexts)),
            "line_model_k2": self.line_model.diagnostics(FIXED_K),
        }


def explicit_token_logps(model: ExplicitOnsetModel, items, parsed, use_identity: bool):
    accepted: List[float] = []
    n_visible = 0
    for it in P1.I.ordered(items):
        for li, line in enumerate(it.lines):
            prev_final = None
            for ti, tok in enumerate(line):
                syms = P1.token_symbols(tok)
                ll = model.token_logp(syms, ti == 0, prev_final, use_identity)
                n_visible += 1
                if parsed[it.item_id][li][ti] is not None:
                    accepted.append(float(ll))
                prev_final = int(syms[-2])
    arr = np.asarray(accepted, dtype=float)
    if len(arr) == 0 or not np.all(np.isfinite(arr)):
        raise RuntimeError("invalid explicit expert log probabilities")
    return arr, int(n_visible)


def reset_token_logps(items, parsed, tr):
    model = P1.train_byte_family(tr, True)
    logp, n_visible = R.token_byte_logps(model, items, parsed, True, FIXED_K, FIXED_ALPHA)
    return model, logp, n_visible


def target_state_records(items, parsed):
    return L2.target_state_records(items, parsed)


def aggregate_delta(delta: np.ndarray, records: Sequence[dict], field: str, universe: Sequence[str]) -> dict:
    return L2.aggregate_delta(delta, records, field, universe)


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


def evaluate_experts(tr, ev, parsed):
    explicit = ExplicitOnsetModel(tr)
    reset_model, log_reset, n_reset = reset_token_logps(ev, parsed, tr)
    log_pos, n_pos = explicit_token_logps(explicit, ev, parsed, use_identity=False)
    log_edge, n_edge = explicit_token_logps(explicit, ev, parsed, use_identity=True)
    log_line, n_line = L2.line_token_logps(explicit.line_model, ev, parsed)
    if not (len(log_reset) == len(log_pos) == len(log_edge) == len(log_line)):
        raise RuntimeError("expert accepted support mismatch")
    if not (n_reset == n_pos == n_edge == n_line):
        raise RuntimeError("expert visible support mismatch")
    max_abs = float(np.max(np.abs(log_edge - log_line))) if len(log_edge) else 0.0
    if max_abs > EQUIV_TOL:
        raise RuntimeError(f"EDGE2 != LINECONT2: max_abs_logp={max_abs}")
    return {
        "RESET2": log_reset,
        "POS2": log_pos,
        "EDGE2": log_edge,
        "n_visible": int(n_edge),
        "equivalence_max_abs_logp": max_abs,
        "reset_model": reset_model,
        "explicit_model": explicit,
    }


def tune_weights(vitems, folds, parsed, outer_f: int, parser, core: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    totals = {name: np.zeros(len(R.W_GRID), dtype=float) for name in EXPERTS}
    inner = []

    for inner_g in range(P1.N_FOLDS):
        if inner_g == outer_f:
            continue
        tr, va, p_core = R.core_probs_for_split(
            vitems, folds, parsed, (outer_f, inner_g), inner_g, parser, rec_sel, state_sel
        )
        log_core = np.log(p_core)
        ev = evaluate_experts(tr, va, parsed)
        if len(ev["RESET2"]) != len(log_core):
            raise RuntimeError(f"inner core/expert support mismatch outer={outer_f} inner={inner_g}")
        for name in EXPERTS:
            for wi, w in enumerate(R.W_GRID):
                totals[name][wi] += float(np.sum(R.mixed_logps(log_core, ev[name], float(w))))
        inner.append({
            "inner_fold": int(inner_g),
            "n_scored": int(len(log_core)),
            "n_visible": int(ev["n_visible"]),
            "core_bits_per_token": R.bits_from_logs(log_core),
            "equivalence_max_abs_logp": float(ev["equivalence_max_abs_logp"]),
            "raw_bits": {name: R.bits_from_logs(ev[name]) for name in EXPERTS},
            "training_diagnostics": ev["explicit_model"].diagnostics(),
        })

    return {name: R.select_weight(totals[name]) for name in EXPERTS}, inner


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

    ev = evaluate_experts(tr, test, parsed)
    if len(ev["RESET2"]) != len(log_core):
        raise RuntimeError(f"outer core/expert support mismatch fold={outer_f}")

    expected_n = int(core["outer"][outer_f]["n_scored"])
    expected_visible = int(core["outer"][outer_f]["n_visible"])
    if len(log_core) != expected_n or int(ev["n_visible"]) != expected_visible:
        raise RuntimeError(f"outer support regression fold={outer_f}")

    experts = {}
    log_mix = {}
    for name in EXPERTS:
        w = float(weights[name]["w"])
        lm = R.mixed_logps(log_core, ev[name], w)
        log_mix[name] = lm
        if name == "RESET2":
            diag = ev["reset_model"].diagnostics(FIXED_K)
        else:
            diag = ev["explicit_model"].diagnostics()
        experts[name] = {
            "selected": {"k": FIXED_K, "alpha": FIXED_ALPHA, "w": w},
            "raw_bits_per_token": R.bits_from_logs(ev[name]),
            "mix_bits_per_token": R.bits_from_logs(lm),
            "n_accepted": expected_n,
            "n_visible": expected_visible,
            "inner_weight_log_likelihood": float(weights[name]["log_likelihood"]),
            "model_diagnostics": diag,
        }

    bits_reset = float(experts["RESET2"]["mix_bits_per_token"])
    bits_pos = float(experts["POS2"]["mix_bits_per_token"])
    bits_edge = float(experts["EDGE2"]["mix_bits_per_token"])
    g_position = float(bits_reset - bits_pos)
    g_identity = float(bits_pos - bits_edge)
    g_parent = float(bits_reset - bits_edge)

    records = target_state_records(test, parsed)
    if len(records) != expected_n:
        raise RuntimeError(f"target-state support mismatch fold={outer_f}")
    d_position = (log_mix["POS2"] - log_mix["RESET2"]) / LN2
    d_identity = (log_mix["EDGE2"] - log_mix["POS2"]) / LN2
    if abs(float(np.mean(d_position)) - g_position) > 1e-12:
        raise RuntimeError("G_position diagnostic sum mismatch")
    if abs(float(np.mean(d_identity)) - g_identity) > 1e-12:
        raise RuntimeError("G_identity diagnostic sum mismatch")
    if abs((g_position + g_identity) - g_parent) > 1e-12:
        raise RuntimeError("edge arithmetic decomposition mismatch")

    diagnostics = {
        "RESET2_TO_POS2": {
            "paragraph_state": aggregate_delta(d_position, records, "paragraph_state", PARA_STATES),
            "line_state": aggregate_delta(d_position, records, "line_state", LINE_STATES),
        },
        "POS2_TO_EDGE2": {
            "paragraph_state": aggregate_delta(d_identity, records, "paragraph_state", PARA_STATES),
            "line_state": aggregate_delta(d_identity, records, "line_state", LINE_STATES),
        },
    }

    return {
        "fold": int(outer_f),
        "n_scored": expected_n,
        "n_visible": expected_visible,
        "bits_B3": bits_core,
        **experts,
        "G_position": g_position,
        "G_identity": g_identity,
        "G_parent_RESET2_vs_EDGE2": g_parent,
        "equivalence_max_abs_logp": float(ev["equivalence_max_abs_logp"]),
        "inner": inner,
        "diagnostics": diagnostics,
    }


def verify_parent_regression(outer: Sequence[dict]) -> dict:
    for f, r in enumerate(outer):
        got = float(r["G_parent_RESET2_vs_EDGE2"])
        if abs(got - PARENT_G_LINE[f]) > 1e-12:
            raise RuntimeError(f"Issue123 G_line regression fold {f}: {got} != {PARENT_G_LINE[f]}")
        wr = float(r["RESET2"]["selected"]["w"])
        we = float(r["EDGE2"]["selected"]["w"])
        if abs(wr - PARENT_RESET_W[f]) > 1e-12:
            raise RuntimeError(f"Issue123 RESET2 weight regression fold {f}: {wr}")
        if abs(we - PARENT_EDGE_W[f]) > 1e-12:
            raise RuntimeError(f"Issue123 LINECONT2/EDGE2 weight regression fold {f}: {we}")
        if float(r["equivalence_max_abs_logp"]) > EQUIV_TOL:
            raise RuntimeError(f"outer edge equivalence failure fold {f}")
        for row in r["inner"]:
            if float(row["equivalence_max_abs_logp"]) > EQUIV_TOL:
                raise RuntimeError(f"inner edge equivalence failure outer {f} inner {row['inner_fold']}")
    return {
        "valid": True,
        "G_line": [float(r["G_parent_RESET2_vs_EDGE2"]) for r in outer],
        "RESET2_w": [float(r["RESET2"]["selected"]["w"]) for r in outer],
        "EDGE2_w": [float(r["EDGE2"]["selected"]["w"]) for r in outer],
        "max_outer_equivalence_abs_logp": float(max(r["equivalence_max_abs_logp"] for r in outer)),
        "max_inner_equivalence_abs_logp": float(max(row["equivalence_max_abs_logp"] for r in outer for row in r["inner"])),
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
        parent = verify_parent_regression(outer)
    except Exception as exc:
        return {
            "schema": "issue125-explicit-edge-l3-v1",
            "phase": "ISSUE125_L3",
            "classification": "INVALID EDGE DECOMPOSITION / SUPPORT REGRESSION",
            "scored": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    g_position = [float(r["G_position"]) for r in outer]
    g_identity = [float(r["G_identity"]) for r in outer]
    s_position = P1.stability(g_position)
    s_identity = P1.stability(g_identity)

    if s_identity["pass"]:
        classification = "TERMINAL→INITIAL IDENTITY ADDS ROBUST LINE-LOCAL INFORMATION"
    elif s_position["pass"]:
        classification = "LINE-POSITION ONSET EXPLAINS LINECONT2 ADVANTAGE"
    else:
        classification = "NEITHER COMPACT ONSET COMPONENT ROBUSTLY EXPLAINS L2"

    pooled = {
        comp: {
            "paragraph_state": pool_aggregates(outer, comp, "paragraph_state", PARA_STATES),
            "line_state": pool_aggregates(outer, comp, "line_state", LINE_STATES),
        }
        for comp in ("RESET2_TO_POS2", "POS2_TO_EDGE2")
    }

    return P1.canonicalize({
        "schema": "issue125-explicit-edge-l3-v1",
        "phase": "ISSUE125_L3",
        "classification": classification,
        "scored": True,
        "fixed_expert": {"k": FIXED_K, "alpha": FIXED_ALPHA, "byte_v": P1.BYTE_V},
        "source": {
            "git_blob_sha1": P1.I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": P1.EXPECTED_ZL3B_BLOB,
        },
        "fold_identity_sha256": core["fold_identity_sha256"],
        "core_authority": core_authority,
        "parent_issue123_regression": parent,
        "outer": outer,
        "summaries": {
            "G_position": s_position,
            "G_identity": s_identity,
            "mean_bits_per_token": {
                "B3": float(np.mean([r["bits_B3"] for r in outer])),
                "MIX_RESET2": float(np.mean([r["RESET2"]["mix_bits_per_token"] for r in outer])),
                "MIX_POS2": float(np.mean([r["POS2"]["mix_bits_per_token"] for r in outer])),
                "MIX_EDGE2": float(np.mean([r["EDGE2"]["mix_bits_per_token"] for r in outer])),
            },
        },
        "pooled_diagnostics": pooled,
        "diagnostic_status": "NON_CLASSIFICATION_INPUT_EXCEPT_PREDECLARED_G_POSITION_AND_G_IDENTITY",
        "firewall": {
            "latent_state_fit": False,
            "segmentation_changed": False,
            "currier_hand_domain_conditioning": False,
            "target_scorecard_used": False,
            "semantic_or_image_context_used": False,
        },
    })


def self_test() -> dict:
    base = L2.self_test()
    if not base.get("ok"):
        raise AssertionError("Issue123 anchor self-test failed")
    c = Counter({1: 2, 2: 1})
    lp = ExplicitOnsetModel._smoothed_logp(c, 1)
    expected = math.log((2.0 + FIXED_ALPHA) / (3.0 + FIXED_ALPHA * P1.BYTE_V))
    if abs(lp - expected) > 1e-15:
        raise AssertionError("smoothed onset probability failed")
    if EXPERTS != ("RESET2", "POS2", "EDGE2"):
        raise AssertionError("expert order changed")
    return {
        "ok": True,
        "issue123_anchor": True,
        "fixed_k": FIXED_K,
        "fixed_alpha": FIXED_ALPHA,
        "edge_equivalence_tolerance": EQUIV_TOL,
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
        "G_position": out.get("summaries", {}).get("G_position"),
        "G_identity": out.get("summaries", {}).get("G_identity"),
        "mean_bits": out.get("summaries", {}).get("mean_bits_per_token"),
        "weights": {
            str(r["fold"]): {name: r[name]["selected"] for name in EXPERTS}
            for r in out.get("outer", [])
        },
        "parent_issue123_regression": out.get("parent_issue123_regression"),
        "pooled_diagnostics": out.get("pooled_diagnostics"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
