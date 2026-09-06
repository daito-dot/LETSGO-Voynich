#!/usr/bin/env python3
"""Issue #92 / Issue #88 Phase 1 predictive-information budget.

Prediction-only confirmatory executable. It never calls S1/S2/H62/R1 scorers.

Usage:
  python phase1_predictive_budget.py --self-test
  python phase1_predictive_budget.py --run ZL3B OUT.json
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PHASE0_DIR = HERE.parent.parent / "phase0"
if str(PHASE0_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE0_DIR))

import phase0_preflight as P0  # noqa: E402

I = P0.I
LN2 = math.log(2.0)
N_FOLDS = 5
TIE_EPS = 1e-12
EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"

H_GRID = (40, 80, 160, 320, "ALL")
TAU_GRID = (16.0, 32.0, 64.0, 128.0, 256.0, math.inf)
PI_GRID = np.asarray([round(i / 100.0, 2) for i in range(31)], dtype=float)
LAMBDA_GRID = np.asarray([0.0, 0.25, 0.50, 0.75, 1.0], dtype=float)
BYTE_K_GRID = tuple(range(7))
BYTE_ALPHA_GRID = (0.01, 0.10, 1.0)
BYTE_END = 256
BYTE_BOS = -1
BYTE_V = 257

PHASE0_EXPECTED = {
    0: {"B0": 9.855350509695006, "B1": 9.74553213453277, "pi": 0.21},
    1: {"B0": 9.771314005898022, "B1": 9.654379389512654, "pi": 0.21},
    2: {"B0": 9.585914491233583, "B1": 9.44552408749662, "pi": 0.20},
    3: {"B0": 9.581375953324109, "B1": 9.478509701296273, "pi": 0.21},
    4: {"B0": 9.750575548278487, "B1": 9.656960288057821, "pi": 0.21},
}


def sha256_file(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def serialize_scale(x):
    if x == "ALL":
        return "ALL"
    if isinstance(x, float) and math.isinf(x):
        return "INF"
    return int(x) if float(x).is_integer() else float(x)


def candidate_defs():
    out = []
    for H in H_GRID:
        for tau in TAU_GRID:
            out.append({"H": H, "tau": tau})
    return out


CANDIDATES = candidate_defs()


def candidate_sort_key(c: dict):
    H = c["H"]
    tau = c["tau"]
    hk = (1, math.inf) if H == "ALL" else (0, float(H))
    tk = (1, math.inf) if math.isinf(float(tau)) else (0, float(tau))
    return hk + tk


def source_distribution(index, tok) -> Dict[tuple, float] | None:
    nb = index.neighbors(tok)
    if not nb:
        return None
    denom = float(sum(index.counts[x] for x in nb))
    if denom <= 0.0:
        return None
    return {x: float(index.counts[x] / denom) for x in nb}


class RecencyAccumulator:
    """Exact Q_decay ratio using time-factor cancellation.

    At target position t, desired source weight exp(-(t-s)/tau) is proportional
    to exp(s/tau); the common exp(-t/tau) cancels in Q's normalization.
    This avoids mutating the whole neighbour-mass map at every token.
    """

    def __init__(self, H, tau: float):
        self.H = None if H == "ALL" else int(H)
        self.tau = float(tau)
        self.reset()

    def reset(self):
        self.queue = deque()
        self.mass = defaultdict(float)
        self.denom = 0.0

    def _raw_weight(self, pos: int) -> float:
        if math.isinf(self.tau):
            return 1.0
        return math.exp(float(pos) / self.tau)

    def prune(self, current_pos: int):
        if self.H is None:
            return
        cutoff = current_pos - self.H
        while self.queue and self.queue[0][0] < cutoff:
            _pos, w, dist = self.queue.popleft()
            if dist is None:
                continue
            self.denom -= w
            for tok, p in dist.items():
                nv = self.mass[tok] - w * p
                if abs(nv) < 1e-14:
                    self.mass.pop(tok, None)
                else:
                    self.mass[tok] = nv
        if self.denom < 0.0 and abs(self.denom) < 1e-9:
            self.denom = 0.0
        if self.denom < -1e-8:
            raise RuntimeError("recency denominator became negative")

    def q(self, target) -> Tuple[float, bool]:
        if self.denom <= 0.0:
            return 0.0, False
        return float(self.mass.get(target, 0.0) / self.denom), True

    def add(self, pos: int, dist: Dict[tuple, float] | None):
        w = self._raw_weight(pos)
        self.queue.append((int(pos), float(w), dist))
        if dist is None:
            return
        self.denom += w
        for tok, p in dist.items():
            self.mass[tok] += w * p


def fit_training(vitems, folds, parsed, excluded_folds: Sequence[int]):
    excluded = set()
    for f in excluded_folds:
        excluded.update(folds[f])
    tr_items = I.b.by_leaves(vitems, excluded, include=False)
    seqs = I.training_sequences(tr_items, parsed)
    if not seqs:
        raise RuntimeError("empty training sequence population")
    v2 = I.C.V2Model(seqs)
    index = I.NeighborIndex(I.training_vocab(tr_items, parsed))
    return tr_items, v2, index


def recency_feature_matrix(items, parsed, v2, index, parser, candidates=CANDIDATES):
    acc = [RecencyAccumulator(c["H"], c["tau"]) for c in candidates]
    p_cache: Dict[object, float] = {}
    p0_rows = []
    q_rows = []
    avail_rows = []
    scored = 0
    visible = 0
    current_leaf = None
    pos = 0

    for it in I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            pos = 0
            for a in acc:
                a.reset()
        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                visible += 1
                for a in acc:
                    a.prune(pos)
                seq = parsed[it.item_id][li][ti]
                if seq is not None:
                    p0 = P0.p0_surface(v2, parser, tok, p_cache)
                    if p0 <= 0.0:
                        raise RuntimeError("V2 assigned non-positive literal probability")
                    qs, av = [], []
                    for a in acc:
                        q, ok = a.q(tok)
                        qs.append(q)
                        av.append(ok)
                    p0_rows.append(p0)
                    q_rows.append(qs)
                    avail_rows.append(av)
                    scored += 1
                dist = source_distribution(index, tok)
                for a in acc:
                    a.add(pos, dist)
                pos += 1

    return {
        "p0": np.asarray(p0_rows, dtype=float),
        "q": np.asarray(q_rows, dtype=float),
        "avail": np.asarray(avail_rows, dtype=bool),
        "n_scored": int(scored),
        "n_visible": int(visible),
    }


def ll_grid(features) -> np.ndarray:
    p0 = features["p0"]
    q = features["q"]
    av = features["avail"]
    total = np.zeros((len(CANDIDATES), len(PI_GRID)), dtype=float)
    chunk = 1024
    for start in range(0, len(p0), chunk):
        stop = min(len(p0), start + chunk)
        b = p0[start:stop, None, None]
        qq = q[start:stop, :, None]
        aa = av[start:stop, :, None]
        pp = PI_GRID[None, None, :]
        probs = np.where(aa, (1.0 - pp) * b + pp * qq, b)
        if np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
            raise RuntimeError("invalid recency probability grid")
        total += np.log(probs).sum(axis=0)
    return total


def select_recency(ll: np.ndarray, restrict_H=None) -> dict:
    best = None
    for ci, c in enumerate(CANDIDATES):
        if restrict_H is not None and c["H"] != restrict_H:
            continue
        for pi_i, pi in enumerate(PI_GRID):
            rec = {
                "candidate_index": ci,
                "H": c["H"],
                "tau": c["tau"],
                "pi": float(pi),
                "log_likelihood": float(ll[ci, pi_i]),
            }
            if best is None or rec["log_likelihood"] > best["log_likelihood"] + TIE_EPS:
                best = rec
                continue
            if abs(rec["log_likelihood"] - best["log_likelihood"]) <= TIE_EPS:
                if rec["pi"] < best["pi"] - TIE_EPS:
                    best = rec
                elif abs(rec["pi"] - best["pi"]) <= TIE_EPS:
                    if candidate_sort_key(rec) < candidate_sort_key(best):
                        best = rec
    if best is None:
        raise RuntimeError("no recency candidate selected")
    return best


def table_rows(ll: np.ndarray, restrict_H=None):
    rows = []
    for ci, c in enumerate(CANDIDATES):
        if restrict_H is not None and c["H"] != restrict_H:
            continue
        for pi_i, pi in enumerate(PI_GRID):
            rows.append({
                "H": serialize_scale(c["H"]),
                "tau": serialize_scale(c["tau"]),
                "pi": float(pi),
                "total_log_likelihood": float(ll[ci, pi_i]),
            })
    return rows


def probability_from_feature(features, selected: dict) -> np.ndarray:
    ci = int(selected["candidate_index"])
    pi = float(selected["pi"])
    p0 = features["p0"]
    q = features["q"][:, ci]
    av = features["avail"][:, ci]
    return np.where(av, (1.0 - pi) * p0 + pi * q, p0)


def bits_from_probs(probs: np.ndarray) -> float:
    if len(probs) == 0 or np.any(probs <= 0.0):
        raise RuntimeError("cannot compute code length")
    return float(-np.log(probs).mean() / LN2)


def line4_state(it, li: int) -> str:
    n = len(it.lines)
    if n == 1:
        return "SINGLE"
    if li == 0:
        return "FIRST"
    if li == n - 1:
        return "FINAL"
    return "MIDDLE"


def line4_records(items, parsed):
    rec = []
    for it in items:
        for li, line in enumerate(it.lines):
            state = line4_state(it, li)
            for ti, _tok in enumerate(line):
                seq = parsed[it.item_id][li][ti]
                if seq is not None:
                    rec.append((state, seq))
    return rec


def build_state_models(tr_items, parsed):
    seqs = I.training_sequences(tr_items, parsed)
    return {
        "ENTRY_BODY": I.ContextV2Model(seqs, I.x3_records(tr_items, parsed)),
        "LINE4": I.ContextV2Model(seqs, line4_records(tr_items, parsed)),
    }


def state_feature_rows(items, parsed, v2, index, parser, b2: dict, state_models: dict):
    c = CANDIDATES[int(b2["candidate_index"])]
    acc = RecencyAccumulator(c["H"], c["tau"])
    p0_cache = {}
    ps_cache = {"ENTRY_BODY": {}, "LINE4": {}}
    rows = []
    current_leaf = None
    pos = 0

    for it in I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            pos = 0
            acc.reset()
        for li, line in enumerate(it.lines):
            states = {
                "ENTRY_BODY": I.ENTRY if li == 0 else I.BODY,
                "LINE4": line4_state(it, li),
            }
            for ti, tok in enumerate(line):
                acc.prune(pos)
                seq = parsed[it.item_id][li][ti]
                if seq is not None:
                    p0 = P0.p0_surface(v2, parser, tok, p0_cache)
                    q, av = acc.q(tok)
                    ps = {}
                    for fam, model in state_models.items():
                        key = (tok, states[fam])
                        if key not in ps_cache[fam]:
                            ps_cache[fam][key] = I.exact_surface_probability(model, parser, tok, states[fam])
                        ps[fam] = float(ps_cache[fam][key])
                        if ps[fam] <= 0.0:
                            raise RuntimeError(f"state model assigned non-positive probability: {fam}")
                    rows.append((p0, q, av, ps["ENTRY_BODY"], ps["LINE4"]))
                dist = source_distribution(index, tok)
                acc.add(pos, dist)
                pos += 1

    a = np.asarray(rows, dtype=float)
    return {
        "p0": a[:, 0],
        "q": a[:, 1],
        "avail": a[:, 2].astype(bool),
        "ENTRY_BODY": a[:, 3],
        "LINE4": a[:, 4],
        "n_scored": int(len(rows)),
    }


def state_ll_grid(features, b2_pi: float):
    out = {}
    p0 = features["p0"][:, None]
    q = features["q"][:, None]
    av = features["avail"][:, None]
    lam = LAMBDA_GRID[None, :]
    for fam in ("ENTRY_BODY", "LINE4"):
        ps = features[fam][:, None]
        base = (1.0 - lam) * p0 + lam * ps
        probs = np.where(av, (1.0 - b2_pi) * base + b2_pi * q, base)
        if np.any(probs <= 0.0):
            raise RuntimeError("invalid state probability")
        out[fam] = np.log(probs).sum(axis=0)
    return out


def select_state(ll_by_family: dict) -> dict:
    best = None
    for fam_rank, fam in enumerate(("ENTRY_BODY", "LINE4")):
        for li, lam in enumerate(LAMBDA_GRID):
            rec = {"family": fam, "lambda": float(lam), "log_likelihood": float(ll_by_family[fam][li])}
            if best is None or rec["log_likelihood"] > best["log_likelihood"] + TIE_EPS:
                best = rec
                continue
            if abs(rec["log_likelihood"] - best["log_likelihood"]) <= TIE_EPS:
                if rec["lambda"] < best["lambda"] - TIE_EPS:
                    best = rec
                elif abs(rec["lambda"] - best["lambda"]) <= TIE_EPS:
                    if fam_rank < (0 if best["family"] == "ENTRY_BODY" else 1):
                        best = rec
    return best


def state_probs(features, b2_pi: float, selected: dict):
    lam = float(selected["lambda"])
    p0 = features["p0"]
    ps = features[selected["family"]]
    base = (1.0 - lam) * p0 + lam * ps
    return np.where(features["avail"], (1.0 - b2_pi) * base + b2_pi * features["q"], base)


class ByteNGramFamily:
    def __init__(self, max_k=6):
        self.max_k = int(max_k)
        self.counts = [defaultdict(Counter) for _ in range(self.max_k + 1)]
        self.totals = [defaultdict(int) for _ in range(self.max_k + 1)]

    @staticmethod
    def context(history: Sequence[int], k: int):
        if k == 0:
            return ()
        h = list(history[-k:])
        if len(h) < k:
            h = [BYTE_BOS] * (k - len(h)) + h
        return tuple(h)

    def observe_symbol(self, history: Sequence[int], sym: int):
        for k in BYTE_K_GRID:
            ctx = self.context(history, k)
            self.counts[k][ctx][int(sym)] += 1
            self.totals[k][ctx] += 1

    def logp(self, history: Sequence[int], sym: int, k: int, alpha: float) -> float:
        ctx = self.context(history, k)
        n = self.totals[k].get(ctx, 0)
        c = self.counts[k].get(ctx, {}).get(int(sym), 0)
        return math.log((float(c) + alpha) / (float(n) + alpha * BYTE_V))

    def diagnostics(self, k: int):
        return {
            "observed_contexts": int(len(self.counts[k])),
            "observed_transitions": int(sum(len(c) for c in self.counts[k].values())),
            "nominal_context_free_parameters": int(len(self.counts[k]) * (BYTE_V - 1)),
        }


def token_symbols(tok) -> List[int]:
    return list(I.surface(tok).encode("utf-8")) + [BYTE_END]


def train_byte_family(items, reset_each_token: bool) -> ByteNGramFamily:
    model = ByteNGramFamily(max(BYTE_K_GRID))
    current_leaf = None
    history = []
    for it in I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            history = []
        for line in it.lines:
            for tok in line:
                if reset_each_token:
                    history = []
                for sym in token_symbols(tok):
                    model.observe_symbol(history, sym)
                    history.append(sym)
                    if len(history) > model.max_k:
                        history = history[-model.max_k:]
    return model


def score_byte_grid(model: ByteNGramFamily, items, parsed, reset_each_token: bool):
    ll_acc = np.zeros((len(BYTE_K_GRID), len(BYTE_ALPHA_GRID)), dtype=float)
    ll_all = np.zeros_like(ll_acc)
    n_acc = 0
    n_all = 0
    current_leaf = None
    histories = {k: [] for k in BYTE_K_GRID}

    for it in I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            histories = {k: [] for k in BYTE_K_GRID}
        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                accepted = parsed[it.item_id][li][ti] is not None
                if reset_each_token:
                    histories = {k: [] for k in BYTE_K_GRID}
                token_ll = np.zeros_like(ll_acc)
                for sym in token_symbols(tok):
                    for ki, k in enumerate(BYTE_K_GRID):
                        hist = histories[k]
                        for ai, alpha in enumerate(BYTE_ALPHA_GRID):
                            token_ll[ki, ai] += model.logp(hist, sym, k, alpha)
                        hist.append(sym)
                        if len(hist) > k:
                            histories[k] = hist[-k:] if k > 0 else []
                    # histories dict was updated per k above
                ll_all += token_ll
                n_all += 1
                if accepted:
                    ll_acc += token_ll
                    n_acc += 1
    return {"ll_accepted": ll_acc, "ll_all": ll_all, "n_accepted": n_acc, "n_all": n_all}


def select_byte(ll: np.ndarray) -> dict:
    best = None
    for ki, k in enumerate(BYTE_K_GRID):
        for ai, alpha in enumerate(BYTE_ALPHA_GRID):
            rec = {"k": int(k), "alpha": float(alpha), "log_likelihood": float(ll[ki, ai])}
            if best is None or rec["log_likelihood"] > best["log_likelihood"] + TIE_EPS:
                best = rec
                continue
            if abs(rec["log_likelihood"] - best["log_likelihood"]) <= TIE_EPS:
                if rec["k"] < best["k"] or (rec["k"] == best["k"] and rec["alpha"] < best["alpha"]):
                    best = rec
    return best


def byte_bits(score: dict, selected: dict, which="accepted"):
    ki = BYTE_K_GRID.index(int(selected["k"]))
    ai = BYTE_ALPHA_GRID.index(float(selected["alpha"]))
    if which == "accepted":
        ll = score["ll_accepted"][ki, ai]
        n = score["n_accepted"]
    else:
        ll = score["ll_all"][ki, ai]
        n = score["n_all"]
    if n <= 0:
        raise RuntimeError("empty byte score")
    return float(-ll / (n * LN2))


def select_outer_recency(vitems, folds, parsed, outer_f: int, parser):
    total = np.zeros((len(CANDIDATES), len(PI_GRID)), dtype=float)
    inner = []
    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        tr, v2, index = fit_training(vitems, folds, parsed, (outer_f, inner_g))
        va = I.b.by_leaves(vitems, folds[inner_g], include=True)
        feat = recency_feature_matrix(va, parsed, v2, index, parser)
        ll = ll_grid(feat)
        total += ll
        inner.append({"inner_fold": inner_g, "n_scored": feat["n_scored"], "n_visible": feat["n_visible"]})
    b1 = select_recency(total, restrict_H=40)
    b2 = select_recency(total, restrict_H=None)
    return {
        "B1": b1,
        "B2": b2,
        "candidate_table": table_rows(total),
        "inner": inner,
    }


def select_outer_state(vitems, folds, parsed, outer_f: int, parser, b2: dict):
    total = {fam: np.zeros(len(LAMBDA_GRID), dtype=float) for fam in ("ENTRY_BODY", "LINE4")}
    inner = []
    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        tr, v2, index = fit_training(vitems, folds, parsed, (outer_f, inner_g))
        models = build_state_models(tr, parsed)
        va = I.b.by_leaves(vitems, folds[inner_g], include=True)
        feat = state_feature_rows(va, parsed, v2, index, parser, b2, models)
        ll = state_ll_grid(feat, float(b2["pi"]))
        for fam in total:
            total[fam] += ll[fam]
        inner.append({
            "inner_fold": inner_g,
            "n_scored": feat["n_scored"],
            "state_models": {
                fam: {
                    "observed_states": int(models[fam].observed_states),
                    "observed_state_contexts": int(models[fam].observed_state_contexts),
                    "free_parameters": int(models[fam].free_parameters),
                } for fam in models
            },
        })
    selected = select_state(total)
    return {
        "selected": selected,
        "table": [
            {"family": fam, "lambda": float(lam), "total_log_likelihood": float(total[fam][li])}
            for fam in ("ENTRY_BODY", "LINE4") for li, lam in enumerate(LAMBDA_GRID)
        ],
        "inner": inner,
    }


def select_outer_byte(vitems, folds, parsed, outer_f: int):
    total = {
        "RESET": np.zeros((len(BYTE_K_GRID), len(BYTE_ALPHA_GRID)), dtype=float),
        "CONTINUOUS": np.zeros((len(BYTE_K_GRID), len(BYTE_ALPHA_GRID)), dtype=float),
    }
    inner = []
    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        excluded = set(folds[outer_f]) | set(folds[inner_g])
        tr = I.b.by_leaves(vitems, excluded, include=False)
        va = I.b.by_leaves(vitems, folds[inner_g], include=True)
        detail = {"inner_fold": inner_g}
        for name, reset in (("RESET", True), ("CONTINUOUS", False)):
            model = train_byte_family(tr, reset)
            score = score_byte_grid(model, va, parsed, reset)
            total[name] += score["ll_accepted"]
            detail[name] = {"n_accepted": score["n_accepted"], "n_all": score["n_all"]}
        inner.append(detail)
    return {
        "RESET": select_byte(total["RESET"]),
        "CONTINUOUS": select_byte(total["CONTINUOUS"]),
        "tables": {
            name: [
                {"k": int(k), "alpha": float(alpha), "total_log_likelihood": float(total[name][ki, ai])}
                for ki, k in enumerate(BYTE_K_GRID) for ai, alpha in enumerate(BYTE_ALPHA_GRID)
            ] for name in total
        },
        "inner": inner,
    }


def outer_score(vitems, folds, parsed, outer_f: int, parser, rec_sel: dict, state_sel: dict, byte_sel: dict):
    tr, v2, index = fit_training(vitems, folds, parsed, (outer_f,))
    test = I.b.by_leaves(vitems, folds[outer_f], include=True)
    feat = recency_feature_matrix(test, parsed, v2, index, parser)
    b0_bits = bits_from_probs(feat["p0"])
    b1_probs = probability_from_feature(feat, rec_sel["B1"])
    b2_probs = probability_from_feature(feat, rec_sel["B2"])
    b1_bits = bits_from_probs(b1_probs)
    b2_bits = bits_from_probs(b2_probs)

    models = build_state_models(tr, parsed)
    sf = state_feature_rows(test, parsed, v2, index, parser, rec_sel["B2"], models)
    b3_probs = state_probs(sf, float(rec_sel["B2"]["pi"]), state_sel["selected"])
    b3_bits = bits_from_probs(b3_probs)

    byte_out = {}
    for name, reset in (("RESET", True), ("CONTINUOUS", False)):
        model = train_byte_family(tr, reset)
        score = score_byte_grid(model, test, parsed, reset)
        selected = byte_sel[name]
        byte_out[name] = {
            "selected": selected,
            "accepted_bits_per_token": byte_bits(score, selected, "accepted"),
            "all_visible_bits_per_token": byte_bits(score, selected, "all"),
            "n_accepted": int(score["n_accepted"]),
            "n_all": int(score["n_all"]),
            "model_diagnostics": model.diagnostics(int(selected["k"])),
        }

    return {
        "fold": int(outer_f),
        "n_scored": int(feat["n_scored"]),
        "n_visible": int(feat["n_visible"]),
        "B0_bits_per_token": b0_bits,
        "B1": {
            "selected": rec_sel["B1"],
            "bits_per_token": b1_bits,
            "gain_vs_B0": float(b0_bits - b1_bits),
        },
        "B2": {
            "selected": rec_sel["B2"],
            "bits_per_token": b2_bits,
            "increment_vs_B1": float(b1_bits - b2_bits),
            "gain_vs_B0": float(b0_bits - b2_bits),
        },
        "B3": {
            "selected": state_sel["selected"],
            "bits_per_token": b3_bits,
            "increment_vs_B2": float(b2_bits - b3_bits),
            "gain_vs_B0": float(b0_bits - b3_bits),
            "state_model_diagnostics": {
                fam: {
                    "observed_states": int(models[fam].observed_states),
                    "observed_state_contexts": int(models[fam].observed_state_contexts),
                    "free_parameters": int(models[fam].free_parameters),
                } for fam in models
            },
        },
        "B4": byte_out,
        "Delta_flex": float(byte_out["RESET"]["accepted_bits_per_token"] - byte_out["CONTINUOUS"]["accepted_bits_per_token"]),
    }


def regression_check(folds_out):
    errors = []
    for row in folds_out:
        f = int(row["fold"])
        ex = PHASE0_EXPECTED[f]
        if abs(row["B0_bits_per_token"] - ex["B0"]) > 1e-9:
            errors.append(f"fold{f} B0 {row['B0_bits_per_token']} != {ex['B0']}")
        if abs(row["B1"]["bits_per_token"] - ex["B1"]) > 1e-9:
            errors.append(f"fold{f} B1 {row['B1']['bits_per_token']} != {ex['B1']}")
        sel = row["B1"]["selected"]
        if sel["H"] != 40 or abs(float(sel["tau"]) - 32.0) > 1e-12 or abs(float(sel["pi"]) - ex["pi"]) > 1e-12:
            errors.append(f"fold{f} B1 selection mismatch: {sel}")
    return {"pass": not errors, "errors": errors}


def stability(values: Sequence[float]):
    vals = [float(x) for x in values]
    return {
        "values": vals,
        "mean": float(np.mean(vals)),
        "positive_folds": int(sum(v > 0.0 for v in vals)),
        "pass": bool(float(np.mean(vals)) > 0.0 and sum(v > 0.0 for v in vals) >= 4),
    }


def canonicalize(obj):
    if isinstance(obj, dict):
        return {k: canonicalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [canonicalize(v) for v in obj]
    if isinstance(obj, float) and math.isinf(obj):
        return "INF" if obj > 0 else "-INF"
    return obj


def run(zl_path: Path):
    if I.b.git_blob_sha1(zl_path.read_bytes()) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b source differs from frozen authority")
    vitems, folds, parsed = I.C.load_corpus(zl_path)
    if len(folds) != N_FOLDS:
        raise RuntimeError("fold count mismatch")
    parser = I.e.SlotParser()
    I.e.validate_parser(parser)

    recency_selection = {}
    state_selection = {}
    byte_selection = {}
    for f in range(N_FOLDS):
        recency_selection[str(f)] = select_outer_recency(vitems, folds, parsed, f, parser)
        state_selection[str(f)] = select_outer_state(vitems, folds, parsed, f, parser, recency_selection[str(f)]["B2"])
        byte_selection[str(f)] = select_outer_byte(vitems, folds, parsed, f)

    outer = [
        outer_score(vitems, folds, parsed, f, parser, recency_selection[str(f)], state_selection[str(f)], byte_selection[str(f)])
        for f in range(N_FOLDS)
    ]
    reg = regression_check(outer)
    if not reg["pass"]:
        raise RuntimeError("Phase-0 B0/B1 regression failed: " + "; ".join(reg["errors"]))

    g_local = [r["B1"]["gain_vs_B0"] for r in outer]
    d_long = [r["B2"]["increment_vs_B1"] for r in outer]
    d_state = [r["B3"]["increment_vs_B2"] for r in outer]
    d_flex = [r["Delta_flex"] for r in outer]
    d_flex_over_local = [d_flex[i] - g_local[i] for i in range(N_FOLDS)]

    summaries = {
        "G_local": stability(g_local),
        "Delta_long": stability(d_long),
        "Delta_state": stability(d_state),
        "Delta_flex": stability(d_flex),
        "Delta_flex_over_local": stability(d_flex_over_local),
        "mean_bits_per_token": {
            "B0": float(np.mean([r["B0_bits_per_token"] for r in outer])),
            "B1": float(np.mean([r["B1"]["bits_per_token"] for r in outer])),
            "B2": float(np.mean([r["B2"]["bits_per_token"] for r in outer])),
            "B3": float(np.mean([r["B3"]["bits_per_token"] for r in outer])),
            "B4_RESET": float(np.mean([r["B4"]["RESET"]["accepted_bits_per_token"] for r in outer])),
            "B4_CONTINUOUS": float(np.mean([r["B4"]["CONTINUOUS"]["accepted_bits_per_token"] for r in outer])),
        },
    }

    comparable = all(
        r["B4"]["RESET"]["n_accepted"] == r["n_scored"]
        and r["B4"]["CONTINUOUS"]["n_accepted"] == r["n_scored"]
        and r["B4"]["RESET"]["n_all"] == r["n_visible"]
        and r["B4"]["CONTINUOUS"]["n_all"] == r["n_visible"]
        for r in outer
    )
    material = bool(
        summaries["Delta_long"]["pass"]
        or summaries["Delta_state"]["pass"]
        or summaries["Delta_flex_over_local"]["pass"]
    )
    if not comparable:
        classification = "MODEL-CLASS / SUPPORT INCONCLUSIVE"
    elif material:
        classification = "MATERIAL PREDICTIVE INFORMATION REMAINS"
    else:
        classification = "TESTED PREDICTIVE BUDGET NEAR-SATURATED BY SIMPLE CONTEXT"

    plan = HERE.parent / "PLAN.md"
    out = {
        "schema": "issue92-phase1-predictive-budget-v1",
        "phase": "ISSUE92_PHASE1",
        "classification": classification,
        "source": {
            "git_blob_sha1": I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": EXPECTED_ZL3B_BLOB,
        },
        "folds": P0.fold_identity(folds),
        "fold_identity_sha256": P0.fold_hash(folds),
        "authority_hashes": {
            "PLAN.md": sha256_file(plan),
            "phase1_predictive_budget.py": sha256_file(HERE),
            "phase0_preflight.py": sha256_file(PHASE0_DIR / "phase0_preflight.py"),
            "issue81_minimal_memory.py": sha256_file(ROOT / "experiments" / "cross-token-memory" / "issue81_minimal_memory.py"),
        },
        "grids": {
            "B2_history": [serialize_scale(x) for x in H_GRID],
            "B2_tau": [serialize_scale(x) for x in TAU_GRID],
            "B2_pi": [float(x) for x in PI_GRID],
            "B3_lambda": [float(x) for x in LAMBDA_GRID],
            "B4_k": list(BYTE_K_GRID),
            "B4_alpha": list(BYTE_ALPHA_GRID),
        },
        "outer": outer,
        "recency_selection": recency_selection,
        "state_selection": state_selection,
        "byte_selection": byte_selection,
        "regression": reg,
        "summaries": summaries,
        "B4_support_comparable": comparable,
        "decision_inputs": {
            "Delta_long_pass": summaries["Delta_long"]["pass"],
            "Delta_state_pass": summaries["Delta_state"]["pass"],
            "Delta_flex_over_local_pass": summaries["Delta_flex_over_local"]["pass"],
        },
        "firewall": {
            "S1_scored": False,
            "S2_scored": False,
            "H62_scored": False,
            "R1_scored": False,
            "issue84_target_used": False,
            "semantic_or_image_context_used": False,
        },
        "interpretation_boundary": {
            "entropy_bound_claimed": False,
            "latent_state_identified": False,
            "semantic_content_tested": False,
            "plaintext_recovered": False,
            "decipherment_established": False,
        },
        "next_program_rule": "If material predictive information remains, proceed to Issue #88 Phase 2 source attribution; otherwise move toward production-unit/boundary and per-unit information questions rather than rich latent-state repair.",
    }
    return canonicalize(out)


def self_test():
    # Verify exact recency ratio against a direct formula on a synthetic neighbour index.
    counts = Counter({tuple("a"): 10, tuple("b"): 7, tuple("c"): 5, tuple("aa"): 4})
    idx = I.NeighborIndex(counts)
    srcs = [tuple("a"), tuple("b"), tuple("c"), tuple("a")]
    acc = RecencyAccumulator(40, 2.0)
    for pos, tok in enumerate(srcs):
        acc.prune(pos)
        acc.add(pos, source_distribution(idx, tok))
    target_pos = len(srcs)
    acc.prune(target_pos)
    for target in counts:
        q1, ok = acc.q(target)
        num = den = 0.0
        for s, src in enumerate(srcs):
            nb = idx.neighbors(src)
            if not nb:
                continue
            w = math.exp(-(target_pos - s) / 2.0)
            den += w
            if target in nb:
                d = float(sum(idx.counts[x] for x in nb))
                num += w * idx.counts[target] / d
        q2 = num / den if den else 0.0
        if abs(q1 - q2) > 1e-12 or ok != bool(den):
            raise AssertionError("recency accumulator mismatch")

    # k=0 reset/continuous models are mathematically identical on the same training corpus.
    if BYTE_V != 257 or BYTE_END != 256:
        raise AssertionError("byte alphabet changed")
    if len(CANDIDATES) != len(H_GRID) * len(TAU_GRID):
        raise AssertionError("candidate grid mismatch")
    return {
        "ok": True,
        "prediction_only": True,
        "candidate_count": len(CANDIDATES),
        "byte_configs_per_condition": len(BYTE_K_GRID) * len(BYTE_ALPHA_GRID),
        "surface_target_calls": 0,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.run is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    result = run(Path(ns.run[0]))
    Path(ns.run[1]).write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": result["classification"],
        "mean_bits_per_token": result["summaries"]["mean_bits_per_token"],
        "G_local": result["summaries"]["G_local"],
        "Delta_long": result["summaries"]["Delta_long"],
        "Delta_state": result["summaries"]["Delta_state"],
        "Delta_flex": result["summaries"]["Delta_flex"],
        "Delta_flex_over_local": result["summaries"]["Delta_flex_over_local"],
        "decision_inputs": result["decision_inputs"],
        "firewall": result["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
