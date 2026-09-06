#!/usr/bin/env python3
"""Issue #134 first reveal: residual beyond the augmented observable core.

The score-free Gate0 was merged before this executable existed. This scorer
first reproduces that exact Gate authority, then performs only the prospectively
frozen RESET-vs-LINE residual comparison. No latent state is fit.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve()
R_PATH = HERE.parent / "residual_first_reveal.py"
GATE_PATH = HERE.parent / "issue134_augmented_core_gate0.py"

EXPECTED_GATE_RESULT_SHA = "3e11615c731654854b6ad982007d5f340b47d3a0c088cd09ab2af08080489db1"
EXPECTED_CORE_SHA = "0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27"
FIXED_EDGE_K = 2
FIXED_EDGE_ALPHA = 0.01
TIE_EPS = 1e-12
LN2 = math.log(2.0)
FAMILIES = ("RESET", "LINE")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


R = load_module("issue134_residual_base", R_PATH)
GATE = load_module("issue134_gate0_anchor", GATE_PATH)
P1 = R.P1
OA = R.OA
K_GRID = tuple(int(k) for k in P1.BYTE_K_GRID)
ALPHA_GRID = tuple(float(a) for a in P1.BYTE_ALPHA_GRID)
GRID01 = np.asarray([round(i / 100.0, 2) for i in range(101)], dtype=float)


def train_line_family(items):
    """Byte n-gram family with hard reset at every source line."""
    model = P1.ByteNGramFamily(max(K_GRID))
    for it in P1.I.ordered(items):
        for line in it.lines:
            history: List[int] = []
            for tok in line:
                for sym in P1.token_symbols(tok):
                    model.observe_symbol(history, sym)
                    history.append(int(sym))
                    if len(history) > model.max_k:
                        history = history[-model.max_k :]
    return model


def line_token_logps(model, items, parsed, k: int, alpha: float):
    accepted: List[float] = []
    n_visible = 0
    for it in P1.I.ordered(items):
        for li, line in enumerate(it.lines):
            history: List[int] = []
            for ti, tok in enumerate(line):
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
        raise RuntimeError("invalid LINE challenger log probabilities")
    return arr, int(n_visible)


def train_challenger(items, family: str):
    if family == "RESET":
        return P1.train_byte_family(items, True)
    if family == "LINE":
        return train_line_family(items)
    raise ValueError(f"unknown challenger family {family}")


def challenger_logps(model, items, parsed, family: str, k: int, alpha: float):
    if family == "RESET":
        return R.token_byte_logps(model, items, parsed, True, int(k), float(alpha))
    if family == "LINE":
        return line_token_logps(model, items, parsed, int(k), float(alpha))
    raise ValueError(f"unknown challenger family {family}")


def select_byte_candidate(totals: Dict[Tuple[int, float], float]) -> dict:
    best = None
    for (k, alpha), ll in totals.items():
        rec = {"k": int(k), "alpha": float(alpha), "log_likelihood": float(ll)}
        if best is None or rec["log_likelihood"] > best["log_likelihood"] + TIE_EPS:
            best = rec
            continue
        if abs(rec["log_likelihood"] - best["log_likelihood"]) <= TIE_EPS:
            if rec["k"] < best["k"]:
                best = rec
            elif rec["k"] == best["k"] and rec["alpha"] > best["alpha"] + TIE_EPS:
                best = rec
    if best is None:
        raise RuntimeError("empty byte candidate likelihood table")
    return best


def select_mix_grid(total_ll: np.ndarray, name: str) -> dict:
    if total_ll.shape != (len(GRID01),) or not np.all(np.isfinite(total_ll)):
        raise RuntimeError(f"invalid {name} likelihood grid")
    best_i = 0
    best_ll = float(total_ll[0])
    for i in range(1, len(GRID01)):
        ll = float(total_ll[i])
        if ll > best_ll + TIE_EPS:
            best_i, best_ll = i, ll
        # ascending grid makes exact ties retain the smaller value
    return {name: float(GRID01[best_i]), "log_likelihood": best_ll}


def smoothed_logp(counter: Counter, sym: int) -> float:
    total = int(sum(counter.values()))
    c = int(counter.get(int(sym), 0))
    return math.log(
        (float(c) + FIXED_EDGE_ALPHA)
        / (float(total) + FIXED_EDGE_ALPHA * P1.BYTE_V)
    )


def choose_edge_counter(
    regime_prev: dict,
    pooled_prev: dict,
    line_body_first: Counter,
    label: str,
    prev_final: int,
):
    if label in ("A", "B"):
        native = regime_prev[label].get(int(prev_final))
        if native is not None and int(sum(native.values())) > 0:
            return native, "NATIVE"
    pooled = pooled_prev.get(int(prev_final))
    if pooled is not None and int(sum(pooled.values())) > 0:
        return pooled, "POOLED"
    return line_body_first, "LINE_BODY"


class CurrierObservableEdge:
    """Issue #125 explicit onset model with the frozen Issue #134 A/B fallback."""

    def __init__(self, items, by_doc: dict):
        self.line_model = train_line_family(items)
        self.line_start_first = Counter()
        self.line_body_first = Counter()
        self.pooled_prev_first = defaultdict(Counter)
        self.regime_prev_first = {
            "A": defaultdict(Counter),
            "B": defaultdict(Counter),
        }
        self.line_start_second = defaultdict(Counter)
        self.line_body_second = defaultdict(Counter)
        self.line_start_tokens = 0
        self.line_body_tokens = 0

        for it in P1.I.ordered(items):
            rec = by_doc.get(it.document)
            if rec is None:
                raise RuntimeError(f"document absent from Currier authority: {it.document}")
            raw_label = str(rec["label"])
            label = raw_label if raw_label in ("A", "B") else "OTHER"
            for line in it.lines:
                prev_final = None
                for ti, tok in enumerate(line):
                    syms = P1.token_symbols(tok)
                    if len(syms) < 2:
                        raise RuntimeError("visible token lacks raw byte before END_TOKEN")
                    first = int(syms[0])
                    second = int(syms[1])
                    if ti == 0:
                        self.line_start_tokens += 1
                        self.line_start_first[first] += 1
                        self.line_start_second[first][second] += 1
                    else:
                        if prev_final is None:
                            raise RuntimeError("missing previous terminal")
                        self.line_body_tokens += 1
                        self.line_body_first[first] += 1
                        self.pooled_prev_first[int(prev_final)][first] += 1
                        if label in ("A", "B"):
                            self.regime_prev_first[label][int(prev_final)][first] += 1
                        self.line_body_second[first][second] += 1
                    prev_final = int(syms[-2])

        if self.line_start_tokens <= 0 or self.line_body_tokens <= 0:
            raise RuntimeError("empty observable onset population")
        for label in ("A", "B"):
            if len(self.regime_prev_first[label]) < 2:
                raise RuntimeError(f"insufficient {label} previous-terminal support")
        if len(self.pooled_prev_first) < 2:
            raise RuntimeError("insufficient pooled previous-terminal support")

    def token_logp(
        self,
        syms: Sequence[int],
        line_start: bool,
        prev_final: int | None,
        label: str,
    ) -> Tuple[float, str]:
        syms = [int(x) for x in syms]
        if len(syms) < 2:
            raise RuntimeError("invalid token symbol sequence")
        first, second = syms[0], syms[1]
        ll = 0.0

        if line_start:
            ll += smoothed_logp(self.line_start_first, first)
            ll += smoothed_logp(self.line_start_second[first], second)
            source = "LINE_START"
        else:
            if prev_final is None:
                raise RuntimeError("line-body token lacks previous terminal")
            counter, source = choose_edge_counter(
                self.regime_prev_first,
                self.pooled_prev_first,
                self.line_body_first,
                label,
                int(prev_final),
            )
            ll += smoothed_logp(counter, first)
            ll += smoothed_logp(self.line_body_second[first], second)

        for j in range(2, len(syms)):
            ll += self.line_model.logp(
                syms[j - FIXED_EDGE_K : j], syms[j], FIXED_EDGE_K, FIXED_EDGE_ALPHA
            )
        return float(ll), source

    def diagnostics(self) -> dict:
        return {
            "line_start_tokens": int(self.line_start_tokens),
            "line_body_tokens": int(self.line_body_tokens),
            "A_previous_terminal_contexts": int(len(self.regime_prev_first["A"])),
            "B_previous_terminal_contexts": int(len(self.regime_prev_first["B"])),
            "pooled_previous_terminal_contexts": int(len(self.pooled_prev_first)),
            "line_model_k2": self.line_model.diagnostics(FIXED_EDGE_K),
        }


def edge_token_logps(model: CurrierObservableEdge, items, parsed, by_doc: dict):
    accepted: List[float] = []
    n_visible = 0
    fallback_visible = Counter()
    fallback_accepted = Counter()

    for it in P1.I.ordered(items):
        rec = by_doc.get(it.document)
        if rec is None:
            raise RuntimeError(f"document absent from Currier authority: {it.document}")
        raw_label = str(rec["label"])
        label = raw_label if raw_label in ("A", "B") else "OTHER"
        for li, line in enumerate(it.lines):
            prev_final = None
            for ti, tok in enumerate(line):
                syms = P1.token_symbols(tok)
                ll, source = model.token_logp(syms, ti == 0, prev_final, label)
                n_visible += 1
                fallback_visible[source] += 1
                if parsed[it.item_id][li][ti] is not None:
                    accepted.append(float(ll))
                    fallback_accepted[source] += 1
                prev_final = int(syms[-2])

    arr = np.asarray(accepted, dtype=float)
    if len(arr) == 0 or not np.all(np.isfinite(arr)):
        raise RuntimeError("invalid observable-edge log probabilities")
    return arr, int(n_visible), {
        "visible": {k: int(fallback_visible.get(k, 0)) for k in ("LINE_START", "NATIVE", "POOLED", "LINE_BODY")},
        "accepted": {k: int(fallback_accepted.get(k, 0)) for k in ("LINE_START", "NATIVE", "POOLED", "LINE_BODY")},
    }


def grid_log_likelihood(log_a: np.ndarray, log_b: np.ndarray) -> np.ndarray:
    if len(log_a) != len(log_b):
        raise RuntimeError("mixture support mismatch")
    return np.asarray(
        [float(np.sum(R.mixed_logps(log_a, log_b, float(x)))) for x in GRID01],
        dtype=float,
    )


def tune_outer(vitems, folds, parsed, outer_f: int, parser, core: dict, by_doc: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    rho_total = np.zeros(len(GRID01), dtype=float)
    byte_total = {
        fam: {(k, a): 0.0 for k in K_GRID for a in ALPHA_GRID}
        for fam in FAMILIES
    }
    bundles = []

    for inner_g in range(P1.N_FOLDS):
        if inner_g == outer_f:
            continue
        tr, va, p_core = R.core_probs_for_split(
            vitems, folds, parsed, (outer_f, inner_g), inner_g, parser, rec_sel, state_sel
        )
        log_core = np.log(p_core)
        edge_model = CurrierObservableEdge(tr, by_doc)
        log_edge, n_edge_visible, edge_fallback = edge_token_logps(edge_model, va, parsed, by_doc)
        if len(log_edge) != len(log_core):
            raise RuntimeError(f"inner core/edge support mismatch outer={outer_f} inner={inner_g}")
        rho_total += grid_log_likelihood(log_core, log_edge)

        challenger_models = {fam: train_challenger(tr, fam) for fam in FAMILIES}
        for fam in FAMILIES:
            model = challenger_models[fam]
            for k in K_GRID:
                for alpha in ALPHA_GRID:
                    log_byte, n_visible = challenger_logps(model, va, parsed, fam, k, alpha)
                    if len(log_byte) != len(log_core) or n_visible != n_edge_visible:
                        raise RuntimeError(
                            f"inner challenger support mismatch outer={outer_f} inner={inner_g} {fam}"
                        )
                    byte_total[fam][(k, alpha)] += float(np.sum(log_byte))

        bundles.append({
            "inner_fold": int(inner_g),
            "log_core": log_core,
            "log_edge": log_edge,
            "edge_n_visible": int(n_edge_visible),
            "edge_fallback": edge_fallback,
            "edge_model_diagnostics": edge_model.diagnostics(),
            "eval_items": va,
            "challenger_models": challenger_models,
        })

    rho_sel = select_mix_grid(rho_total, "rho")
    byte_sel = {fam: select_byte_candidate(byte_total[fam]) for fam in FAMILIES}
    w_total = {fam: np.zeros(len(GRID01), dtype=float) for fam in FAMILIES}
    inner_out = []

    for b in bundles:
        rho = float(rho_sel["rho"])
        log_aug = R.mixed_logps(b["log_core"], b["log_edge"], rho)
        detail = {
            "inner_fold": int(b["inner_fold"]),
            "n_scored": int(len(log_aug)),
            "n_visible": int(b["edge_n_visible"]),
            "B3_bits_per_token": R.bits_from_logs(b["log_core"]),
            "EDGE_bits_per_token": R.bits_from_logs(b["log_edge"]),
            "AUG_bits_per_token": R.bits_from_logs(log_aug),
            "edge_fallback": b["edge_fallback"],
            "edge_training_diagnostics": b["edge_model_diagnostics"],
            "challengers": {},
        }
        for fam in FAMILIES:
            sel = byte_sel[fam]
            log_byte, n_visible = challenger_logps(
                b["challenger_models"][fam],
                b["eval_items"],
                parsed,
                fam,
                int(sel["k"]),
                float(sel["alpha"]),
            )
            if len(log_byte) != len(log_aug) or n_visible != b["edge_n_visible"]:
                raise RuntimeError(f"inner selected challenger support mismatch {fam}")
            w_total[fam] += grid_log_likelihood(log_aug, log_byte)
            detail["challengers"][fam] = {
                "raw_bits_per_token": R.bits_from_logs(log_byte),
                "n_accepted": int(len(log_byte)),
                "n_visible": int(n_visible),
            }
        inner_out.append(detail)

    w_sel = {fam: select_mix_grid(w_total[fam], "w") for fam in FAMILIES}
    return rho_sel, byte_sel, w_sel, inner_out


def score_outer(vitems, folds, parsed, outer_f: int, parser, core: dict, by_doc: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    rho_sel, byte_sel, w_sel, inner = tune_outer(
        vitems, folds, parsed, outer_f, parser, core, by_doc
    )

    tr, test, p_core = R.core_probs_for_split(
        vitems, folds, parsed, (outer_f,), outer_f, parser, rec_sel, state_sel
    )
    log_core = np.log(p_core)
    bits_core = R.bits_from_logs(log_core)
    authority_bits = float(core["outer"][outer_f]["B3"]["bits_per_token"])
    if abs(bits_core - authority_bits) > 1e-12:
        raise RuntimeError(f"outer B3 regression fold {outer_f}: {bits_core} != {authority_bits}")

    edge_model = CurrierObservableEdge(tr, by_doc)
    log_edge, n_edge_visible, edge_fallback = edge_token_logps(edge_model, test, parsed, by_doc)
    if len(log_edge) != len(log_core):
        raise RuntimeError(f"outer core/edge support mismatch fold={outer_f}")
    rho = float(rho_sel["rho"])
    log_aug = R.mixed_logps(log_core, log_edge, rho)

    expected_n = int(core["outer"][outer_f]["n_scored"])
    expected_visible = int(core["outer"][outer_f]["n_visible"])
    if len(log_aug) != expected_n or n_edge_visible != expected_visible:
        raise RuntimeError(f"outer augmented-core support regression fold={outer_f}")

    experts = {}
    final_logs = {}
    for fam in FAMILIES:
        sel = byte_sel[fam]
        model = train_challenger(tr, fam)
        log_byte, n_visible = challenger_logps(
            model, test, parsed, fam, int(sel["k"]), float(sel["alpha"])
        )
        if len(log_byte) != expected_n or n_visible != expected_visible:
            raise RuntimeError(f"outer challenger support regression fold={outer_f} {fam}")
        w = float(w_sel[fam]["w"])
        log_final = R.mixed_logps(log_aug, log_byte, w)
        final_logs[fam] = log_final
        experts[fam] = {
            "selected": {
                "k": int(sel["k"]),
                "alpha": float(sel["alpha"]),
                "w": w,
            },
            "raw_bits_per_token": R.bits_from_logs(log_byte),
            "mix_bits_per_token": R.bits_from_logs(log_final),
            "n_accepted": int(len(log_byte)),
            "n_visible": int(n_visible),
            "inner_byte_log_likelihood": float(sel["log_likelihood"]),
            "inner_weight_log_likelihood": float(w_sel[fam]["log_likelihood"]),
            "model_diagnostics": model.diagnostics(int(sel["k"])),
        }

    bits_aug = R.bits_from_logs(log_aug)
    bits_reset = float(experts["RESET"]["mix_bits_per_token"])
    bits_line = float(experts["LINE"]["mix_bits_per_token"])
    g_residual = float(bits_reset - bits_line)

    return {
        "fold": int(outer_f),
        "n_scored": expected_n,
        "n_visible": expected_visible,
        "bits_B3": bits_core,
        "observable_edge": {
            "fixed_k": FIXED_EDGE_K,
            "fixed_alpha": FIXED_EDGE_ALPHA,
            "selected_rho": rho,
            "raw_bits_per_token": R.bits_from_logs(log_edge),
            "augmented_core_bits_per_token": bits_aug,
            "inner_rho_log_likelihood": float(rho_sel["log_likelihood"]),
            "fallback": edge_fallback,
            "training_diagnostics": edge_model.diagnostics(),
        },
        "RESET": experts["RESET"],
        "LINE": experts["LINE"],
        "G_aug_vs_B3": float(bits_core - bits_aug),
        "G_reset_beyond_aug": float(bits_aug - bits_reset),
        "G_line_beyond_aug": float(bits_aug - bits_line),
        "G_residual": g_residual,
        "inner": inner,
    }


def residual_stability(values: Sequence[float]) -> dict:
    vals = [float(x) for x in values]
    if len(vals) != 5 or not all(math.isfinite(x) for x in vals):
        raise RuntimeError("invalid five-fold residual vector")
    mean = float(sum(vals) / len(vals))
    positive = int(sum(x > 0.0 for x in vals))
    passed = bool(mean > 0.0 and positive >= 4)
    return {
        "values": vals,
        "mean": mean,
        "positive_folds": positive,
        "pass": passed,
        "rule": "mean > 0 and positive in at least 4/5 untouched outer folds",
    }


def run(zl_path: Path) -> dict:
    # The merged score-free Gate must reproduce exactly before target scoring.
    try:
        gate = GATE.audit(zl_path)
        gate_sha = GATE.json_sha256(gate)
        if not gate["gate_pass"] or gate_sha != EXPECTED_GATE_RESULT_SHA:
            raise RuntimeError(
                f"Issue134 Gate0 authority mismatch: pass={gate['gate_pass']} sha={gate_sha}"
            )

        core = R.C1.run(zl_path)
        core_authority = R.verify_core_authority(core)
        if core_authority["normalized_sha256"] != EXPECTED_CORE_SHA:
            raise RuntimeError("corrected B3 authority changed")

        P1.I.ordered = OA.ordered
        vitems, folds, parsed = P1.I.C.load_corpus(zl_path)
        if P1.P0.fold_hash(folds) != core["fold_identity_sha256"]:
            raise RuntimeError("fold identity changed")
        parser = P1.I.e.SlotParser()
        P1.I.e.validate_parser(parser)
        headers = GATE.CUR.G0.parse_source_headers(zl_path)
        by_doc = {r["document"]: r for r in headers}
        if len(by_doc) != len(headers):
            raise RuntimeError("duplicate document in Currier authority")
    except Exception as exc:
        return {
            "schema": "issue134-residual-first-reveal-v1",
            "phase": "ISSUE134_RESIDUAL_CLOSURE",
            "classification": "INVALID CORE / SUPPORT REGRESSION",
            "residual_scored": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    try:
        outer = [
            score_outer(vitems, folds, parsed, f, parser, core, by_doc)
            for f in range(P1.N_FOLDS)
        ]
        g = [float(r["G_residual"]) for r in outer]
        stability = residual_stability(g)
    except Exception as exc:
        return {
            "schema": "issue134-residual-first-reveal-v1",
            "phase": "ISSUE134_RESIDUAL_CLOSURE",
            "classification": "INVALID CORE / SUPPORT REGRESSION",
            "residual_scored": False,
            "gate_authority": {
                "valid": True,
                "json_sha256": gate_sha,
            },
            "core_authority": core_authority,
            "error": f"{type(exc).__name__}: {exc}",
        }

    classification = (
        "ROBUST RESIDUAL REMAINS BEYOND AUGMENTED OBSERVABLE CORE"
        if stability["pass"]
        else "NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE"
    )

    return P1.canonicalize({
        "schema": "issue134-residual-first-reveal-v1",
        "phase": "ISSUE134_RESIDUAL_CLOSURE",
        "classification": classification,
        "residual_scored": True,
        "gate_authority": {
            "valid": True,
            "json_sha256": gate_sha,
            "expected_json_sha256": EXPECTED_GATE_RESULT_SHA,
        },
        "core_authority": core_authority,
        "source": {
            "git_blob_sha1": P1.I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": P1.EXPECTED_ZL3B_BLOB,
        },
        "fold_identity_sha256": core["fold_identity_sha256"],
        "grids": {
            "observable_edge": {"k": FIXED_EDGE_K, "alpha": FIXED_EDGE_ALPHA},
            "rho": [float(x) for x in GRID01],
            "byte_k": list(K_GRID),
            "byte_alpha": list(ALPHA_GRID),
            "final_w": [float(x) for x in GRID01],
        },
        "currier_policy": {
            "A_or_B": "same-regime previous-terminal table, else pooled previous-terminal table, else pooled LINE_BODY onset",
            "unknown_or_other": "pooled previous-terminal table, else pooled LINE_BODY onset",
            "hand_conditioning": False,
        },
        "outer": outer,
        "summaries": {
            "G_residual": stability,
            "mean_bits_per_token": {
                "B3": float(np.mean([r["bits_B3"] for r in outer])),
                "AUGMENTED_CORE": float(np.mean([r["observable_edge"]["augmented_core_bits_per_token"] for r in outer])),
                "MIX_RESET": float(np.mean([r["RESET"]["mix_bits_per_token"] for r in outer])),
                "MIX_LINE": float(np.mean([r["LINE"]["mix_bits_per_token"] for r in outer])),
            },
            "G_aug_vs_B3_mean": float(np.mean([r["G_aug_vs_B3"] for r in outer])),
            "G_reset_beyond_aug_mean": float(np.mean([r["G_reset_beyond_aug"] for r in outer])),
            "G_line_beyond_aug_mean": float(np.mean([r["G_line_beyond_aug"] for r in outer])),
        },
        "selection_rule": {
            "observable_rho": "max pooled inner accepted-token likelihood; tie smaller rho; challenger excluded",
            "challenger_k_alpha": "max pooled inner raw-byte likelihood; tie smaller k then larger alpha",
            "final_w": "max pooled inner accepted-token likelihood against common augmented core; tie smaller w",
        },
        "firewall": {
            "latent_state_fit": False,
            "writing_hand_conditioning": False,
            "surface_scorecard_used_for_selection": False,
            "semantic_or_image_context_used": False,
            "segmentation_changed": False,
            "candidate_grid_extended": False,
            "outer_targets_used_for_selection": False,
        },
        "interpretation_boundary": {
            "entropy_bound_claimed": False,
            "semantic_state_identified": False,
            "plaintext_recovered": False,
            "decipherment_established": False,
        },
    })


def self_test() -> dict:
    gate_test = GATE.self_test()
    if not gate_test.get("ok") or not gate_test.get("score_free"):
        raise AssertionError("Issue134 Gate0 self-test failed")
    base = R.self_test()
    if not base.get("ok"):
        raise AssertionError("Issue118 residual base self-test failed")

    totals = {
        (2, 0.01): -10.0,
        (1, 0.01): -10.0,
        (1, 1.0): -10.0,
    }
    sel = select_byte_candidate(totals)
    if sel["k"] != 1 or abs(sel["alpha"] - 1.0) > 1e-12:
        raise AssertionError(f"challenger tie rule failed: {sel}")
    if select_mix_grid(np.zeros(len(GRID01)), "rho")["rho"] != 0.0:
        raise AssertionError("rho tie rule failed")
    if select_mix_grid(np.zeros(len(GRID01)), "w")["w"] != 0.0:
        raise AssertionError("w tie rule failed")

    native = {"A": defaultdict(Counter), "B": defaultdict(Counter)}
    pooled = defaultdict(Counter)
    body = Counter({7: 1})
    native["A"][1][2] = 3
    pooled[1][2] = 5
    pooled[3][4] = 2
    if choose_edge_counter(native, pooled, body, "A", 1)[1] != "NATIVE":
        raise AssertionError("native fallback rule failed")
    if choose_edge_counter(native, pooled, body, "B", 1)[1] != "POOLED":
        raise AssertionError("pooled fallback rule failed")
    if choose_edge_counter(native, pooled, body, "OTHER", 3)[1] != "POOLED":
        raise AssertionError("unknown/other pooled rule failed")
    if choose_edge_counter(native, pooled, body, "A", 9)[1] != "LINE_BODY":
        raise AssertionError("LINE_BODY fallback rule failed")

    s = residual_stability([0.1, 0.1, 0.1, 0.1, -0.01])
    if not s["pass"] or s["positive_folds"] != 4:
        raise AssertionError("residual stability rule failed")
    if residual_stability([0.1, 0.1, 0.1, -0.01, -0.01])["pass"]:
        raise AssertionError("3/5 residual must fail")

    return {
        "ok": True,
        "gate_authority_sha_frozen": EXPECTED_GATE_RESULT_SHA,
        "corrected_core_sha_frozen": EXPECTED_CORE_SHA,
        "edge_k": FIXED_EDGE_K,
        "edge_alpha": FIXED_EDGE_ALPHA,
        "challenger_families": list(FAMILIES),
        "challenger_tie_rule": True,
        "rho_tie_rule": True,
        "w_tie_rule": True,
        "currier_fallback_rule": True,
        "residual_stability_rule": True,
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
        "classification": out.get("classification"),
        "residual_scored": out.get("residual_scored", False),
        "gate_authority": out.get("gate_authority"),
        "core_authority": out.get("core_authority"),
        "G_residual": out.get("summaries", {}).get("G_residual"),
        "mean_bits": out.get("summaries", {}).get("mean_bits_per_token"),
        "outer": [
            {
                "fold": r["fold"],
                "rho": r["observable_edge"]["selected_rho"],
                "RESET": r["RESET"]["selected"],
                "LINE": r["LINE"]["selected"],
                "G_residual": r["G_residual"],
            }
            for r in out.get("outer", [])
        ],
    }, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
