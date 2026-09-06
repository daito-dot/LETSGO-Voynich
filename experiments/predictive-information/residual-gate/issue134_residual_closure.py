#!/usr/bin/env python3
"""Issue #134 predictive residual closure after the augmented observable core.

This scorer is governed by ISSUE134_AUGMENTED_CORE_PLAN.md and may run only
after the score-free Gate0 authority has passed. It fits no hidden state.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

import numpy as np

HERE = Path(__file__).resolve()
GATE_PATH = HERE.parent / "issue134_augmented_core_gate0.py"
L3_PATH = HERE.parent / "explicit_edge_l3.py"
R_PATH = HERE.parent / "residual_first_reveal.py"
EXPECTED_GATE_SHA = "3e11615c731654854b6ad982007d5f340b47d3a0c088cd09ab2af08080489db1"
EXPECTED_CORE_SHA = "0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27"
EXPECTED_OUTER_TARGET_COUNTS = (4430, 4810, 5516, 5447, 4868)
RHO_GRID = np.asarray([round(i / 100.0, 2) for i in range(101)], dtype=float)
W_GRID = np.asarray([round(i / 100.0, 2) for i in range(101)], dtype=float)
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


GATE = load_module("issue134_gate_anchor", GATE_PATH)
L3 = load_module("issue134_l3_anchor", L3_PATH)
R = load_module("issue134_issue118_anchor", R_PATH)
P1 = R.P1
OA = R.OA
FIXED_K = L3.FIXED_K
FIXED_ALPHA = L3.FIXED_ALPHA


def canonical_json(x: dict) -> str:
    return json.dumps(x, indent=2, sort_keys=True, allow_nan=False) + "\n"


def json_sha256(x: dict) -> str:
    return hashlib.sha256(canonical_json(x).encode("utf-8")).hexdigest()


def verify_gate_authority_isolated(zl_path: Path) -> tuple[dict, str]:
    """Replay merged Gate0 in a fresh interpreter to avoid import-state coupling."""
    with tempfile.TemporaryDirectory(prefix="issue134-gate0-") as td:
        out_path = Path(td) / "gate0.json"
        proc = subprocess.run(
            [sys.executable, str(GATE_PATH), "--audit", str(zl_path), str(out_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                "isolated Issue134 Gate0 replay failed: "
                + (proc.stderr.strip() or proc.stdout.strip() or f"exit={proc.returncode}")
            )
        raw = out_path.read_bytes()
        gate_sha = hashlib.sha256(raw).hexdigest()
        gate = json.loads(raw.decode("utf-8"))
        if gate_sha != EXPECTED_GATE_SHA:
            raise RuntimeError(
                f"Issue134 Gate0 SHA mismatch: {gate_sha} != {EXPECTED_GATE_SHA}"
            )
        if not gate.get("gate_pass"):
            raise RuntimeError("Issue134 Gate0 no longer passes")
        return gate, gate_sha


def bits_from_logs(logp: np.ndarray) -> float:
    if len(logp) == 0 or not np.all(np.isfinite(logp)):
        raise RuntimeError("invalid log-probability vector")
    return float(-np.mean(logp) / LN2)


def mix_logs(a: np.ndarray, b: np.ndarray, w: float) -> np.ndarray:
    return R.mixed_logps(np.asarray(a, dtype=float), np.asarray(b, dtype=float), float(w))


def select_grid(total_ll: np.ndarray, grid: np.ndarray) -> dict:
    if total_ll.shape != grid.shape or not np.all(np.isfinite(total_ll)):
        raise RuntimeError("invalid selection grid")
    best_i = 0
    best_ll = float(total_ll[0])
    for i in range(1, len(grid)):
        ll = float(total_ll[i])
        if ll > best_ll + TIE_EPS:
            best_i, best_ll = i, ll
        elif abs(ll - best_ll) <= TIE_EPS and float(grid[i]) < float(grid[best_i]):
            best_i, best_ll = i, ll
    return {"value": float(grid[best_i]), "log_likelihood": float(best_ll)}


def select_params(total_ll: dict[tuple[int, float], float]) -> dict:
    rows = [
        {"k": int(k), "alpha": float(alpha), "total_log_likelihood": float(ll)}
        for (k, alpha), ll in total_ll.items()
    ]
    return R.select_byte_issue118(rows)


class CurrierObservableEdge:
    """Issue125 pooled factors plus preregistered target-regime first-symbol edge."""

    def __init__(self, items, by_doc: dict):
        self.pooled = L3.ExplicitOnsetModel(items)
        self.regime = {"A": defaultdict(Counter), "B": defaultdict(Counter)}
        self.visible_edge_events = {"A": 0, "B": 0, "OTHER": 0}

        for it in P1.I.ordered(items):
            rec = by_doc.get(it.document)
            if rec is None:
                raise RuntimeError(f"document absent from Currier authority: {it.document}")
            raw = str(rec["label"])
            lab = raw if raw in ("A", "B") else "OTHER"
            for line in it.lines:
                if len(line) < 2:
                    continue
                prev_syms = P1.token_symbols(line[0])
                if len(prev_syms) < 2:
                    raise RuntimeError("visible token lacks raw byte")
                prev_final = int(prev_syms[-2])
                for ti in range(1, len(line)):
                    syms = P1.token_symbols(line[ti])
                    if len(syms) < 2:
                        raise RuntimeError("visible token lacks raw byte")
                    first = int(syms[0])
                    self.visible_edge_events[lab] += 1
                    if lab in self.regime:
                        self.regime[lab][prev_final][first] += 1
                    prev_final = int(syms[-2])

    @staticmethod
    def _has(counter: Counter | None) -> bool:
        return counter is not None and int(sum(counter.values())) > 0

    def first_counter(self, target_label: str, prev_final: int):
        if target_label in self.regime:
            native = self.regime[target_label].get(int(prev_final))
            if self._has(native):
                return native, "NATIVE"
        pooled = self.pooled.prev_terminal_first.get(int(prev_final))
        if self._has(pooled):
            return pooled, "POOLED_CONTEXT"
        return self.pooled.line_body_first, "LINE_BODY"

    def token_logp(
        self,
        syms: Sequence[int],
        line_start: bool,
        prev_final: int | None,
        target_label: str,
    ) -> tuple[float, str]:
        syms = [int(x) for x in syms]
        if len(syms) < 2:
            raise RuntimeError("invalid token symbol sequence")
        if line_start:
            return (
                float(self.pooled.token_logp(syms, True, None, use_identity=False)),
                "LINE_START",
            )
        if prev_final is None:
            raise RuntimeError("line-body token lacks previous terminal")

        first, second = syms[0], syms[1]
        counter, route = self.first_counter(target_label, int(prev_final))
        ll = self.pooled._smoothed_logp(counter, first)
        ll += self.pooled._smoothed_logp(self.pooled.line_body_second[first], second)
        for j in range(2, len(syms)):
            ll += self.pooled.line_model.logp(
                syms[j - 2 : j], syms[j], FIXED_K, FIXED_ALPHA
            )
        return float(ll), route

    def diagnostics(self) -> dict:
        pooled_ctx = set(int(x) for x in self.pooled.prev_terminal_first.keys())
        out = {
            "visible_edge_events": {k: int(v) for k, v in self.visible_edge_events.items()},
            "pooled_previous_terminal_contexts": int(len(pooled_ctx)),
            "pooled_issue125_factors": self.pooled.diagnostics(),
        }
        for lab in ("A", "B"):
            native_ctx = set(int(x) for x in self.regime[lab].keys())
            out[f"{lab}_previous_terminal_contexts"] = int(len(native_ctx))
            out[f"{lab}_pooled_only_contexts"] = int(len(pooled_ctx - native_ctx))
        return out


def target_label(it, by_doc: dict) -> str:
    rec = by_doc.get(it.document)
    if rec is None:
        raise RuntimeError(f"document absent from Currier authority: {it.document}")
    raw = str(rec["label"])
    return raw if raw in ("A", "B") else "OTHER"


def observable_token_logps(model: CurrierObservableEdge, items, parsed, by_doc: dict):
    accepted = []
    n_visible = 0
    route_counts = {"LINE_START": 0, "NATIVE": 0, "POOLED_CONTEXT": 0, "LINE_BODY": 0}
    accepted_by_label = {"A": 0, "B": 0, "OTHER": 0}

    for it in P1.I.ordered(items):
        lab = target_label(it, by_doc)
        for li, line in enumerate(it.lines):
            prev_final = None
            for ti, tok in enumerate(line):
                syms = P1.token_symbols(tok)
                lp, route = model.token_logp(syms, ti == 0, prev_final, lab)
                n_visible += 1
                if parsed[it.item_id][li][ti] is not None:
                    accepted.append(float(lp))
                    route_counts[route] += 1
                    accepted_by_label[lab] += 1
                prev_final = int(syms[-2])

    arr = np.asarray(accepted, dtype=float)
    if len(arr) == 0 or not np.all(np.isfinite(arr)):
        raise RuntimeError("invalid observable-edge probabilities")
    return arr, {
        "n_accepted": int(len(arr)),
        "n_visible": int(n_visible),
        "accepted_routes": {k: int(v) for k, v in route_counts.items()},
        "accepted_by_currier": {k: int(v) for k, v in accepted_by_label.items()},
    }


def train_challenger(items, family: str):
    if family == "RESET":
        return P1.train_byte_family(items, True)
    if family == "LINE":
        return L3.L2.train_line_family(items)
    raise ValueError(f"unknown family {family}")


def line_token_logps(model, items, parsed, k: int, alpha: float):
    accepted = []
    n_visible = 0
    for it in P1.I.ordered(items):
        for li, line in enumerate(it.lines):
            history = []
            for ti, tok in enumerate(line):
                ll = 0.0
                for sym in P1.token_symbols(tok):
                    ll += model.logp(history, int(sym), int(k), float(alpha))
                    history.append(int(sym))
                    if len(history) > model.max_k:
                        history = history[-model.max_k :]
                n_visible += 1
                if parsed[it.item_id][li][ti] is not None:
                    accepted.append(float(ll))
    arr = np.asarray(accepted, dtype=float)
    if len(arr) == 0 or not np.all(np.isfinite(arr)):
        raise RuntimeError("invalid LINE challenger probabilities")
    return arr, int(n_visible)


def challenger_logps(model, items, parsed, family: str, k: int, alpha: float):
    if family == "RESET":
        return R.token_byte_logps(model, items, parsed, True, int(k), float(alpha))
    if family == "LINE":
        return line_token_logps(model, items, parsed, int(k), float(alpha))
    raise ValueError(f"unknown family {family}")


def tune_outer(vitems, folds, parsed, outer_f: int, parser, core: dict, by_doc: dict):
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    rho_total = np.zeros(len(RHO_GRID), dtype=float)
    param_total = {
        fam: {
            (int(k), float(alpha)): 0.0
            for k in P1.BYTE_K_GRID
            for alpha in P1.BYTE_ALPHA_GRID
        }
        for fam in FAMILIES
    }
    split_cache = []

    for inner_g in range(P1.N_FOLDS):
        if inner_g == outer_f:
            continue
        tr, va, p_core = R.core_probs_for_split(
            vitems, folds, parsed, (outer_f, inner_g), inner_g, parser, rec_sel, state_sel
        )
        log_core = np.log(p_core)
        edge_model = CurrierObservableEdge(tr, by_doc)
        log_edge, edge_diag = observable_token_logps(edge_model, va, parsed, by_doc)
        if len(log_edge) != len(log_core):
            raise RuntimeError(f"inner core/edge support mismatch outer={outer_f} inner={inner_g}")
        for i, rho in enumerate(RHO_GRID):
            rho_total[i] += float(np.sum(mix_logs(log_core, log_edge, float(rho))))

        candidate_logs = {fam: {} for fam in FAMILIES}
        visible_counts = {}
        for fam in FAMILIES:
            byte_model = train_challenger(tr, fam)
            for k in P1.BYTE_K_GRID:
                for alpha in P1.BYTE_ALPHA_GRID:
                    lp, n_visible = challenger_logps(
                        byte_model, va, parsed, fam, int(k), float(alpha)
                    )
                    if len(lp) != len(log_core):
                        raise RuntimeError(
                            f"inner challenger support mismatch outer={outer_f} inner={inner_g} {fam}"
                        )
                    key = (int(k), float(alpha))
                    param_total[fam][key] += float(np.sum(lp))
                    candidate_logs[fam][key] = lp
                    visible_counts[fam] = int(n_visible)

        split_cache.append({
            "inner_fold": int(inner_g),
            "log_core": log_core,
            "log_edge": log_edge,
            "candidate_logs": candidate_logs,
            "edge_diag": edge_diag,
            "edge_model_diag": edge_model.diagnostics(),
            "visible_counts": visible_counts,
        })

    rho_sel = select_grid(rho_total, RHO_GRID)
    selected_params = {fam: select_params(param_total[fam]) for fam in FAMILIES}
    w_total = {fam: np.zeros(len(W_GRID), dtype=float) for fam in FAMILIES}
    inner_report = []

    for row in split_cache:
        log_aug = mix_logs(row["log_core"], row["log_edge"], rho_sel["value"])
        detail = {
            "inner_fold": row["inner_fold"],
            "n_scored": int(len(log_aug)),
            "bits_B3": bits_from_logs(row["log_core"]),
            "bits_edge_raw": bits_from_logs(row["log_edge"]),
            "bits_augmented_core": bits_from_logs(log_aug),
            "edge_scoring": row["edge_diag"],
            "edge_training": row["edge_model_diag"],
        }
        for fam in FAMILIES:
            sel = selected_params[fam]
            key = (int(sel["k"]), float(sel["alpha"]))
            lp = row["candidate_logs"][fam][key]
            for i, w in enumerate(W_GRID):
                w_total[fam][i] += float(np.sum(mix_logs(log_aug, lp, float(w))))
            detail[fam] = {
                "selected_k": int(sel["k"]),
                "selected_alpha": float(sel["alpha"]),
                "raw_bits": bits_from_logs(lp),
                "n_visible": int(row["visible_counts"][fam]),
            }
        inner_report.append(detail)

    w_sel = {fam: select_grid(w_total[fam], W_GRID) for fam in FAMILIES}
    return {
        "rho": rho_sel,
        "params": selected_params,
        "w": w_sel,
        "inner": inner_report,
    }


def score_outer(vitems, folds, parsed, outer_f: int, parser, core: dict, by_doc: dict):
    tuned = tune_outer(vitems, folds, parsed, outer_f, parser, core, by_doc)
    rec_sel = core["recency_selection"][str(outer_f)]
    state_sel = core["state_selection"][str(outer_f)]
    tr, test, p_core = R.core_probs_for_split(
        vitems, folds, parsed, (outer_f,), outer_f, parser, rec_sel, state_sel
    )
    log_core = np.log(p_core)
    bits_b3 = bits_from_logs(log_core)
    authority_bits = float(core["outer"][outer_f]["B3"]["bits_per_token"])
    if abs(bits_b3 - authority_bits) > 1e-12:
        raise RuntimeError(f"outer B3 regression fold={outer_f}: {bits_b3} != {authority_bits}")
    if len(log_core) != EXPECTED_OUTER_TARGET_COUNTS[outer_f]:
        raise RuntimeError(f"outer target-count regression fold={outer_f}")

    edge_model = CurrierObservableEdge(tr, by_doc)
    log_edge, edge_diag = observable_token_logps(edge_model, test, parsed, by_doc)
    if len(log_edge) != len(log_core):
        raise RuntimeError(f"outer core/edge support mismatch fold={outer_f}")
    rho = float(tuned["rho"]["value"])
    log_aug = mix_logs(log_core, log_edge, rho)

    fam_out = {}
    for fam in FAMILIES:
        sel = tuned["params"][fam]
        model = train_challenger(tr, fam)
        lp, n_visible = challenger_logps(
            model, test, parsed, fam, int(sel["k"]), float(sel["alpha"])
        )
        if len(lp) != len(log_aug):
            raise RuntimeError(f"outer augmented/challenger support mismatch fold={outer_f} {fam}")
        w = float(tuned["w"][fam]["value"])
        lm = mix_logs(log_aug, lp, w)
        fam_out[fam] = {
            "selected": {
                "k": int(sel["k"]),
                "alpha": float(sel["alpha"]),
                "w": w,
            },
            "raw_bits_per_token": bits_from_logs(lp),
            "mix_bits_per_token": bits_from_logs(lm),
            "n_accepted": int(len(lp)),
            "n_visible": int(n_visible),
            "inner_raw_log_likelihood": float(sel["log_likelihood"]),
            "inner_weight_log_likelihood": float(tuned["w"][fam]["log_likelihood"]),
            "model_diagnostics": model.diagnostics(int(sel["k"])),
        }

    expected_visible = int(core["outer"][outer_f]["n_visible"])
    for fam in FAMILIES:
        if fam_out[fam]["n_accepted"] != len(log_core) or fam_out[fam]["n_visible"] != expected_visible:
            raise RuntimeError(f"outer challenger visible/support regression fold={outer_f} {fam}")

    bits_reset = float(fam_out["RESET"]["mix_bits_per_token"])
    bits_line = float(fam_out["LINE"]["mix_bits_per_token"])
    return {
        "fold": int(outer_f),
        "n_scored": int(len(log_core)),
        "n_visible": int(expected_visible),
        "bits_B3": bits_b3,
        "bits_edge_raw": bits_from_logs(log_edge),
        "bits_augmented_core": bits_from_logs(log_aug),
        "augmented_core": {
            "rho": rho,
            "inner_log_likelihood": float(tuned["rho"]["log_likelihood"]),
            "edge_scoring": edge_diag,
            "edge_training": edge_model.diagnostics(),
        },
        "RESET": fam_out["RESET"],
        "LINE": fam_out["LINE"],
        "G_residual": float(bits_reset - bits_line),
        "G_any_line_beyond_augmented_core": float(bits_from_logs(log_aug) - bits_line),
        "inner": tuned["inner"],
    }


def run(zl_path: Path) -> dict:
    try:
        gate, gate_sha = verify_gate_authority_isolated(zl_path)

        core = R.C1.run(zl_path)
        core_authority = R.verify_core_authority(core)
        if core_authority["normalized_sha256"] != EXPECTED_CORE_SHA:
            raise RuntimeError("corrected B3 authority changed")

        P1.I.ordered = OA.ordered
        vitems, folds, parsed = P1.I.C.load_corpus(zl_path)
        if P1.P0.fold_hash(folds) != core["fold_identity_sha256"]:
            raise RuntimeError("fold identity changed")
        if len(folds) != 5:
            raise RuntimeError("outer fold count changed")
        parser = P1.I.e.SlotParser()
        P1.I.e.validate_parser(parser)

        headers = GATE.CUR.G0.parse_source_headers(zl_path)
        by_doc = {r["document"]: r for r in headers}
        if len(by_doc) != len(headers):
            raise RuntimeError("duplicate document in Currier authority")

        outer = [
            score_outer(vitems, folds, parsed, f, parser, core, by_doc)
            for f in range(P1.N_FOLDS)
        ]
    except Exception as exc:
        return {
            "schema": "issue134-residual-closure-v1",
            "phase": "ISSUE134_RESIDUAL_CLOSURE",
            "classification": "INVALID CORE / SUPPORT REGRESSION",
            "scored": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    gains = [float(r["G_residual"]) for r in outer]
    stability = P1.stability(gains)
    if stability["pass"]:
        classification = "ROBUST RESIDUAL REMAINS BEYOND AUGMENTED OBSERVABLE CORE"
    else:
        classification = "NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE"

    return P1.canonicalize({
        "schema": "issue134-residual-closure-v1",
        "phase": "ISSUE134_RESIDUAL_CLOSURE",
        "classification": classification,
        "scored": True,
        "source": {
            "git_blob_sha1": P1.I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": P1.EXPECTED_ZL3B_BLOB,
        },
        "fold_identity_sha256": core["fold_identity_sha256"],
        "gate0_authority": {
            "json_sha256": gate_sha,
            "expected_json_sha256": EXPECTED_GATE_SHA,
            "gate_pass": bool(gate["gate_pass"]),
        },
        "core_authority": core_authority,
        "fixed_observable_edge": {
            "k": FIXED_K,
            "alpha": FIXED_ALPHA,
            "byte_v": P1.BYTE_V,
            "currier_policy": gate["frozen_policy"],
        },
        "grids": {
            "rho": [float(x) for x in RHO_GRID],
            "byte_k": [int(x) for x in P1.BYTE_K_GRID],
            "byte_alpha": [float(x) for x in P1.BYTE_ALPHA_GRID],
            "w": [float(x) for x in W_GRID],
        },
        "selection_rule": {
            "rho": "max pooled inner accepted-token likelihood of B3+observable-edge only; tie smaller rho",
            "byte": "max pooled inner raw-byte accepted-token likelihood; tie smaller k then larger alpha",
            "w": "max pooled inner accepted-token likelihood after rho and byte params frozen; tie smaller w",
        },
        "challengers": {
            "RESET": "byte history resets before every visible-space token",
            "LINE": "byte history resets at each source line and carries only within the line",
        },
        "outer": outer,
        "summaries": {
            "G_residual": stability,
            "mean_bits_per_token": {
                "B3": float(np.mean([r["bits_B3"] for r in outer])),
                "EDGE_RAW": float(np.mean([r["bits_edge_raw"] for r in outer])),
                "AUGMENTED_CORE": float(np.mean([r["bits_augmented_core"] for r in outer])),
                "MIX_RESET": float(np.mean([r["RESET"]["mix_bits_per_token"] for r in outer])),
                "MIX_LINE": float(np.mean([r["LINE"]["mix_bits_per_token"] for r in outer])),
            },
            "G_any_line_beyond_augmented_core": P1.stability(
                [float(r["G_any_line_beyond_augmented_core"]) for r in outer]
            ),
        },
        "firewall": {
            "latent_state_fit": False,
            "writing_hand_conditioning": False,
            "surface_scorecard_used_for_selection": False,
            "semantic_or_image_context_used": False,
            "segmentation_changed": False,
            "outer_targets_used_for_selection": False,
            "post_reveal_grid_extension": False,
        },
        "interpretation_boundary": {
            "entropy_bound_claimed": False,
            "semantic_state_identified": False,
            "plaintext_recovered": False,
            "decipherment_established": False,
        },
    })


def self_test() -> dict:
    if FIXED_K != 2 or abs(FIXED_ALPHA - 0.01) > 1e-15:
        raise AssertionError("Issue125 edge constants changed")
    if EXPECTED_GATE_SHA != "3e11615c731654854b6ad982007d5f340b47d3a0c088cd09ab2af08080489db1":
        raise AssertionError("Gate0 authority changed")
    if tuple(EXPECTED_OUTER_TARGET_COUNTS) != (4430, 4810, 5516, 5447, 4868):
        raise AssertionError("outer target authority changed")

    z = np.zeros(len(RHO_GRID), dtype=float)
    if select_grid(z, RHO_GRID)["value"] != 0.0:
        raise AssertionError("rho tie rule failed")
    if select_grid(np.zeros(len(W_GRID)), W_GRID)["value"] != 0.0:
        raise AssertionError("w tie rule failed")
    p = select_params({(2, 0.01): -1.0, (1, 0.01): -1.0, (1, 1.0): -1.0})
    if p["k"] != 1 or abs(p["alpha"] - 1.0) > 1e-12:
        raise AssertionError("byte parameter tie rule failed")

    a = np.log(np.asarray([0.2, 0.3], dtype=float))
    b = np.log(np.asarray([0.4, 0.1], dtype=float))
    half = mix_logs(a, b, 0.5)
    if not np.allclose(np.exp(half), np.asarray([0.3, 0.2])):
        raise AssertionError("mixture arithmetic failed")

    return {
        "ok": True,
        "gate0_authority_frozen": True,
        "observable_edge_k": FIXED_K,
        "observable_edge_alpha": FIXED_ALPHA,
        "rho_tie_smaller": True,
        "byte_tie_smaller_k_larger_alpha": True,
        "w_tie_smaller": True,
        "latent_state_fit": False,
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
        "scored": out.get("scored"),
        "G_residual": out.get("summaries", {}).get("G_residual"),
        "G_any_line_beyond_augmented_core": out.get("summaries", {}).get("G_any_line_beyond_augmented_core"),
        "mean_bits": out.get("summaries", {}).get("mean_bits_per_token"),
        "selected": {
            str(r["fold"]): {
                "rho": r["augmented_core"]["rho"],
                "RESET": r["RESET"]["selected"],
                "LINE": r["LINE"]["selected"],
                "G_residual": r["G_residual"],
            }
            for r in out.get("outer", [])
        },
    }, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
