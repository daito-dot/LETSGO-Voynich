#!/usr/bin/env python3
"""Issue #90 / Issue #88 Phase 0 score-free preflight.

This executable deliberately contains no S1/S2/H62/R1 target scoring path.
It freezes and validates the target-blind DECAY40/TILT10 model-selection
machinery before the later first-reveal implementation exists.

Modes:
  --self-test
  --preflight ZL3B OUT.json
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PHASE = "ISSUE90_PHASE0"
N_FOLDS = 5
DECAY_RECENT = 40
TILT_RECENT = 10
TAU_GRID = (1.0, 2.0, 4.0, 8.0, 16.0, 32.0)
PI_GRID = tuple(round(x / 100.0, 2) for x in range(0, 31))
BETA_GRID = (0.10, 0.20, 0.40, 0.80, 1.20, 1.60)
REPS = (0, 1, 2)
TIE_EPS = 1e-12
LN2 = math.log(2.0)
EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"


def load_issue81():
    path = ROOT / "experiments" / "cross-token-memory" / "issue81_minimal_memory.py"
    spec = importlib.util.spec_from_file_location("issue81_minimal_memory_phase0_anchor", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import Issue81 authority: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


I = load_issue81()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fold_identity(folds) -> List[List[int]]:
    return [sorted(int(x) for x in fold) for fold in folds]


def fold_hash(folds) -> str:
    return I.sha256_obj(fold_identity(folds))


def fit_training(vitems, folds, parsed, excluded_folds: Sequence[int]):
    excluded_leaves = set()
    for f in excluded_folds:
        excluded_leaves.update(folds[f])
    tr_items = I.b.by_leaves(vitems, excluded_leaves, include=False)
    seqs = I.training_sequences(tr_items, parsed)
    if not seqs:
        raise RuntimeError(f"no training sequences after excluding folds {excluded_folds}")
    v2 = I.C.V2Model(seqs)
    index = I.NeighborIndex(I.training_vocab(tr_items, parsed))
    return tr_items, v2, index


def p0_surface(v2, parser, tok, cache: Dict[object, float]) -> float:
    got = cache.get(tok)
    if got is None:
        got = I.exact_surface_probability(v2, parser, tok)
        cache[tok] = float(got)
    return float(got)


def decay_sources(history, index, tau: float):
    out = []
    recent = history[-DECAY_RECENT:]
    for lag, src in enumerate(reversed(recent), start=1):
        nb = index.neighbors(src)
        if not nb:
            continue
        out.append((lag, src, nb, math.exp(-float(lag) / float(tau))))
    return out


def decay_distribution(history, index, tau: float) -> Tuple[Dict[object, float], int]:
    srcs = decay_sources(history, index, tau)
    if not srcs:
        return {}, 0
    sw = float(sum(x[3] for x in srcs))
    q = defaultdict(float)
    for _lag, _src, nb, wsrc in srcs:
        denom = float(sum(index.counts[x] for x in nb))
        alpha = float(wsrc / sw)
        for t in nb:
            q[t] += alpha * float(index.counts[t] / denom)
    total = float(sum(q.values()))
    if not math.isfinite(total) or abs(total - 1.0) > 1e-10:
        raise RuntimeError(f"DECAY distribution failed normalization: {total}")
    return dict(q), len(srcs)


def activation_counts(history, index) -> Counter:
    out = Counter()
    for src in history[-TILT_RECENT:]:
        for t in index.neighbors(src):
            out[t] += 1
    return out


def activation_base_probs(v2, parser, history, index, cache: Dict[object, float]):
    counts = activation_counts(history, index)
    base = {}
    for t, a in counts.items():
        if a <= 0:
            continue
        p = p0_surface(v2, parser, t, cache)
        if p > 0.0:
            base[t] = p
    return counts, base


def tilt_terms(counts: Counter, base: Dict[object, float], beta: float):
    extra = {}
    extra_total = 0.0
    for t, p in base.items():
        a = int(counts[t])
        if a <= 0:
            continue
        wminus = math.expm1(float(beta) * float(a))
        m = float(p * wminus)
        if m > 0.0:
            extra[t] = m
            extra_total += m
    z = 1.0 + float(extra_total)
    if not math.isfinite(z) or z < 1.0:
        raise RuntimeError(f"invalid TILT normalizer: {z}")
    residual = abs((1.0 / z) + (extra_total / z) - 1.0)
    return z, extra, float(residual)


def tilt_probability(target, p0: float, counts: Counter, base: Dict[object, float], beta: float):
    z, _extra, residual = tilt_terms(counts, base, beta)
    a = int(counts.get(target, 0))
    p = float(p0 * math.exp(float(beta) * float(a)) / z)
    return p, z, residual


def better_record(candidate: dict, best: dict | None) -> bool:
    if best is None:
        return True
    cll = float(candidate["total_log_likelihood"])
    bll = float(best["total_log_likelihood"])
    if cll > bll + TIE_EPS:
        return True
    if abs(cll - bll) > TIE_EPS:
        return False
    # Frozen cross-family tie rule: one-scalar TILT10 before two-scalar DECAY40.
    crank = 0 if candidate["family"] == "TILT10" else 1
    brank = 0 if best["family"] == "TILT10" else 1
    if crank != brank:
        return crank < brank
    if candidate["family"] == "TILT10":
        return float(candidate["beta"]) < float(best["beta"])
    if float(candidate["pi"]) != float(best["pi"]):
        return float(candidate["pi"]) < float(best["pi"])
    return float(candidate["tau"]) < float(best["tau"])


def iter_validation_tokens(items, parsed):
    current_leaf = None
    history = []
    for it in I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            history = []
        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                seq = parsed[it.item_id][li][ti]
                yield tok, seq, history
                history.append(tok)
                if len(history) > DECAY_RECENT:
                    history[:] = history[-DECAY_RECENT:]


def select_outer(vitems, folds, parsed, outer_f: int, parser) -> dict:
    decay_ll = {(tau, pi): 0.0 for tau in TAU_GRID for pi in PI_GRID}
    tilt_ll = {beta: 0.0 for beta in BETA_GRID}
    x0_ll = 0.0
    n_scored = 0
    n_decay_context = {tau: 0 for tau in TAU_GRID}
    n_tilt_context = 0
    inner_details = []
    norm_max = 0.0
    active_base_mass_max = 0.0
    z_min = math.inf
    z_max = 1.0

    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        _tr, v2, index = fit_training(vitems, folds, parsed, (outer_f, inner_g))
        va_items = I.b.by_leaves(vitems, folds[inner_g], include=True)
        p_cache: Dict[object, float] = {}
        inner_n = 0
        inner_decay_context = {tau: 0 for tau in TAU_GRID}
        inner_tilt_context = 0

        for tok, seq, history in iter_validation_tokens(va_items, parsed):
            if seq is None:
                continue
            p0 = p0_surface(v2, parser, tok, p_cache)
            if p0 <= 0.0:
                raise RuntimeError("V2 assigned non-positive probability to parseable validation token")
            x0_ll += math.log(p0)
            n_scored += 1
            inner_n += 1

            for tau in TAU_GRID:
                q, nsrc = decay_distribution(history, index, tau)
                if nsrc:
                    n_decay_context[tau] += 1
                    inner_decay_context[tau] += 1
                    qt = float(q.get(tok, 0.0))
                    for pi in PI_GRID:
                        p = (1.0 - pi) * p0 + pi * qt
                        if p <= 0.0:
                            decay_ll[(tau, pi)] = -math.inf
                        elif math.isfinite(decay_ll[(tau, pi)]):
                            decay_ll[(tau, pi)] += math.log(p)
                else:
                    lp = math.log(p0)
                    for pi in PI_GRID:
                        if math.isfinite(decay_ll[(tau, pi)]):
                            decay_ll[(tau, pi)] += lp

            counts, base = activation_base_probs(v2, parser, history, index, p_cache)
            if base:
                n_tilt_context += 1
                inner_tilt_context += 1
                active_base_mass = float(sum(base.values()))
                active_base_mass_max = max(active_base_mass_max, active_base_mass)
                if active_base_mass > 1.0 + 1e-9:
                    raise RuntimeError(f"activated literal surfaces exceed unit base mass: {active_base_mass}")
            for beta in BETA_GRID:
                p, z, residual = tilt_probability(tok, p0, counts, base, beta)
                norm_max = max(norm_max, residual)
                z_min = min(z_min, z)
                z_max = max(z_max, z)
                if p <= 0.0:
                    tilt_ll[beta] = -math.inf
                elif math.isfinite(tilt_ll[beta]):
                    tilt_ll[beta] += math.log(p)

        inner_details.append({
            "inner_validation_fold": inner_g,
            "n_scored_tokens": inner_n,
            "training_vocab_types": len(index.vocab),
            "decay_context_tokens": {str(t): int(inner_decay_context[t]) for t in TAU_GRID},
            "tilt_context_tokens": int(inner_tilt_context),
        })

    if n_scored <= 0:
        raise RuntimeError(f"outer {outer_f}: no nested validation tokens")

    records = []
    for tau in TAU_GRID:
        for pi in PI_GRID:
            records.append({
                "family": "DECAY40",
                "tau": float(tau),
                "pi": float(pi),
                "total_log_likelihood": float(decay_ll[(tau, pi)]),
            })
    for beta in BETA_GRID:
        records.append({
            "family": "TILT10",
            "beta": float(beta),
            "total_log_likelihood": float(tilt_ll[beta]),
        })

    best = None
    for rec in records:
        if better_record(rec, best):
            best = dict(rec)
    if best is None or not math.isfinite(float(best["total_log_likelihood"])):
        raise RuntimeError(f"outer {outer_f}: no finite selected candidate")

    return {
        "outer_fold": int(outer_f),
        "n_scored_tokens": int(n_scored),
        "x0_total_log_likelihood": float(x0_ll),
        "selected": best,
        "candidate_table": records,
        "inner_folds": inner_details,
        "context": {
            "decay_context_tokens": {str(t): int(n_decay_context[t]) for t in TAU_GRID},
            "tilt_context_tokens": int(n_tilt_context),
        },
        "tilt_normalization": {
            "max_decomposition_residual": float(norm_max),
            "max_activated_base_mass": float(active_base_mass_max),
            "z_min": float(z_min if math.isfinite(z_min) else 1.0),
            "z_max": float(z_max),
        },
    }


def x2_inner_pi(vitems, folds, parsed, outer_f: int, parser):
    return I.inner_cv_pi(vitems, folds, parsed, outer_f, parser)


def score_outer(vitems, folds, parsed, outer_f: int, selected: dict, x2_pi: float, parser) -> dict:
    _tr, v2, index = fit_training(vitems, folds, parsed, (outer_f,))
    test = I.b.by_leaves(vitems, folds[outer_f], include=True)
    p_cache: Dict[object, float] = {}
    log0 = []
    log_selected = []
    log_x2 = []
    n_selected_context = 0
    n_x2_context = 0
    norm_max = 0.0
    z_min = math.inf
    z_max = 1.0

    for tok, seq, history in iter_validation_tokens(test, parsed):
        if seq is None:
            continue
        p0 = p0_surface(v2, parser, tok, p_cache)
        if p0 <= 0.0:
            raise RuntimeError("outer V2 assigned non-positive probability")
        log0.append(math.log(p0))

        qx2, elig = I.memory_q(tok, history, index)
        if elig:
            n_x2_context += 1
            px2 = (1.0 - x2_pi) * p0 + x2_pi * qx2
        else:
            px2 = p0
        if px2 <= 0.0:
            raise RuntimeError("X2 anchor assigned non-positive probability")
        log_x2.append(math.log(px2))

        if selected["family"] == "DECAY40":
            q, nsrc = decay_distribution(history, index, float(selected["tau"]))
            if nsrc:
                n_selected_context += 1
                ps = (1.0 - float(selected["pi"])) * p0 + float(selected["pi"]) * float(q.get(tok, 0.0))
            else:
                ps = p0
        elif selected["family"] == "TILT10":
            counts, base = activation_base_probs(v2, parser, history, index, p_cache)
            if base:
                n_selected_context += 1
            ps, z, residual = tilt_probability(tok, p0, counts, base, float(selected["beta"]))
            norm_max = max(norm_max, residual)
            z_min = min(z_min, z)
            z_max = max(z_max, z)
        else:
            raise RuntimeError(f"unknown selected family: {selected}")
        if ps <= 0.0:
            raise RuntimeError("selected candidate assigned non-positive probability")
        log_selected.append(math.log(ps))

    n = len(log0)
    if n <= 0 or len(log_selected) != n or len(log_x2) != n:
        raise RuntimeError("outer score population mismatch")
    b0 = float(-np.mean(log0) / LN2)
    bs = float(-np.mean(log_selected) / LN2)
    bx2 = float(-np.mean(log_x2) / LN2)
    return {
        "fold": int(outer_f),
        "n_scored_tokens": int(n),
        "selected": selected,
        "x2_pi": float(x2_pi),
        "X0_bits_per_token": b0,
        "X2_HARD10_bits_per_token": bx2,
        "selected_bits_per_token": bs,
        "selected_gain_vs_X0_bits_per_token": float(b0 - bs),
        "X2_gain_vs_X0_bits_per_token": float(b0 - bx2),
        "selected_context_tokens": int(n_selected_context),
        "X2_context_tokens": int(n_x2_context),
        "tilt_normalization": {
            "max_decomposition_residual": float(norm_max),
            "z_min": float(z_min if math.isfinite(z_min) else 1.0),
            "z_max": float(z_max),
        },
        "training_vocab_types": int(len(index.vocab)),
    }


def sample_decay(rng, history, index, tau: float):
    srcs = decay_sources(history, index, tau)
    if not srcs:
        return None, None
    w = np.asarray([x[3] for x in srcs], dtype=float)
    w /= w.sum()
    j = int(rng.choice(len(srcs), p=w))
    lag, src, _nb, _ws = srcs[j]
    tok = index.weighted_choice(rng, src)
    return tok, int(lag)


def sample_tilt(rng, v2, parser, history, index, beta: float, p_cache):
    counts, base = activation_base_probs(v2, parser, history, index, p_cache)
    z, extra, residual = tilt_terms(counts, base, beta)
    if residual > 1e-10:
        raise RuntimeError(f"TILT decomposition residual too large: {residual}")
    extra_total = float(z - 1.0)
    if extra_total <= 0.0:
        seq = v2.sample(rng)
        return I.surface_tuple(I.C.units_to_string(seq)), "base", z, residual, len(base)
    if float(rng.random()) < (1.0 / z):
        seq = v2.sample(rng)
        return I.surface_tuple(I.C.units_to_string(seq)), "base", z, residual, len(base)
    toks = sorted(extra)
    weights = np.asarray([extra[t] for t in toks], dtype=float)
    weights /= weights.sum()
    tok = toks[int(rng.choice(len(toks), p=weights))]
    return tok, "extra", z, residual, len(base)


def parser_support(items, parser):
    visible = 0
    parsed = 0
    lines = 0
    for it in I.ordered(items):
        for line in it.lines:
            lines += 1
            for tok in line:
                visible += 1
                if parser.pick(I.surface(tok), "min") is not None:
                    parsed += 1
    return {
        "visible_tokens": int(visible),
        "parsed_tokens": int(parsed),
        "parser_coverage": float(parsed / visible) if visible else 0.0,
        "lines": int(lines),
    }


def generate_selected(vitems, folds, parsed, selections: dict, rep: int, parser):
    items = []
    diagnostics = {}
    for f in range(N_FOLDS):
        _tr, v2, index = fit_training(vitems, folds, parsed, (f,))
        sel = selections[str(f)]["selected"]
        rng = np.random.default_rng(I.e.stable_seed(f"{PHASE}:SELECTED:fold{f}:rep{rep}"))
        held = I.ordered(I.b.by_leaves(vitems, folds[f], include=True))
        current_leaf = None
        history = []
        n_tokens = 0
        context_n = 0
        decay_attempts = 0
        decay_events = 0
        decay_fallbacks = 0
        lag_counts = Counter()
        tilt_base = 0
        tilt_extra = 0
        tilt_active_context = 0
        tilt_z_min = math.inf
        tilt_z_max = 1.0
        tilt_norm_max = 0.0
        p_cache: Dict[object, float] = {}

        for it in held:
            if it.leaf != current_leaf:
                current_leaf = it.leaf
                history = []
            new_lines = []
            for line in it.lines:
                new_line = []
                for _orig in line:
                    if sel["family"] == "DECAY40":
                        srcs = decay_sources(history, index, float(sel["tau"]))
                        if srcs:
                            context_n += 1
                        if float(rng.random()) < float(sel["pi"]):
                            decay_attempts += 1
                            mem, lag = sample_decay(rng, history, index, float(sel["tau"]))
                            if mem is None:
                                decay_fallbacks += 1
                                seq = v2.sample(rng)
                                out_tok = I.surface_tuple(I.C.units_to_string(seq))
                            else:
                                decay_events += 1
                                lag_counts[int(lag)] += 1
                                out_tok = mem
                        else:
                            seq = v2.sample(rng)
                            out_tok = I.surface_tuple(I.C.units_to_string(seq))
                    elif sel["family"] == "TILT10":
                        out_tok, source, z, residual, active_n = sample_tilt(
                            rng, v2, parser, history, index, float(sel["beta"]), p_cache
                        )
                        if active_n:
                            context_n += 1
                            tilt_active_context += 1
                        if source == "base":
                            tilt_base += 1
                        else:
                            tilt_extra += 1
                        tilt_z_min = min(tilt_z_min, z)
                        tilt_z_max = max(tilt_z_max, z)
                        tilt_norm_max = max(tilt_norm_max, residual)
                    else:
                        raise RuntimeError(f"unknown selected family: {sel}")
                    history.append(out_tok)
                    if len(history) > DECAY_RECENT:
                        history = history[-DECAY_RECENT:]
                    new_line.append(out_tok)
                    n_tokens += 1
                new_lines.append(new_line)
            items.append(I.b.Item(item_id=it.item_id, document=it.document, lines=new_lines, leaf=it.leaf))

        diagnostics[str(f)] = {
            "fold": int(f),
            "selected": sel,
            "n_tokens": int(n_tokens),
            "context_tokens": int(context_n),
            "context_fraction": float(context_n / n_tokens) if n_tokens else 0.0,
            "training_vocab_types": int(len(index.vocab)),
            "DECAY40": {
                "attempts": int(decay_attempts),
                "events": int(decay_events),
                "fallbacks": int(decay_fallbacks),
                "event_rate": float(decay_events / n_tokens) if n_tokens else 0.0,
                "source_lag_counts": {str(k): int(v) for k, v in sorted(lag_counts.items())},
            },
            "TILT10": {
                "base_draws": int(tilt_base),
                "extra_draws": int(tilt_extra),
                "extra_rate": float(tilt_extra / n_tokens) if n_tokens else 0.0,
                "active_context_tokens": int(tilt_active_context),
                "z_min": float(tilt_z_min if math.isfinite(tilt_z_min) else 1.0),
                "z_max": float(tilt_z_max),
                "max_decomposition_residual": float(tilt_norm_max),
            },
        }

    items = I.ordered(items)
    return items, diagnostics, parser_support(items, parser)


def self_test():
    counts = Counter({tuple("a"): 5, tuple("b"): 3, tuple("aa"): 2, tuple("c"): 7})
    idx = I.NeighborIndex(counts)
    history = [tuple("a"), tuple("b"), tuple("a")]
    for tau in TAU_GRID:
        q, n = decay_distribution(history, idx, tau)
        if n and abs(sum(q.values()) - 1.0) > 1e-12:
            raise AssertionError("DECAY synthetic normalization failed")
    syn_counts = Counter({tuple("x"): 1, tuple("y"): 2})
    syn_base = {tuple("x"): 0.2, tuple("y"): 0.1}
    for beta in BETA_GRID:
        z, extra, residual = tilt_terms(syn_counts, syn_base, beta)
        if z <= 1.0 or residual > 1e-12:
            raise AssertionError("TILT algebra normalization failed")
        if abs((1.0 / z) + sum(extra.values()) / z - 1.0) > 1e-12:
            raise AssertionError("TILT decomposition failed")
    # Tie discipline: TILT wins exact cross-family tie.
    a = {"family": "TILT10", "beta": 0.2, "total_log_likelihood": -10.0}
    b = {"family": "DECAY40", "tau": 1.0, "pi": 0.0, "total_log_likelihood": -10.0}
    if not better_record(a, b):
        raise AssertionError("cross-family tie rule failed")
    return {"ok": True, "target_score_calls": 0}


def run_preflight(zl_path: Path):
    if I.b.git_blob_sha1(zl_path.read_bytes()) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b source blob differs from frozen Issue81 authority")
    vitems, folds, parsed = I.C.load_corpus(zl_path)
    if len(folds) != N_FOLDS:
        raise RuntimeError(f"expected {N_FOLDS} folds, got {len(folds)}")
    parser = I.e.SlotParser()
    I.e.validate_parser(parser)

    selections = {str(f): select_outer(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    # Explicit deterministic re-run before any target scorer exists.
    selections_repeat = {str(f): select_outer(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    deterministic_selection = I.canonical_json(selections) == I.canonical_json(selections_repeat)
    if not deterministic_selection:
        raise RuntimeError("nested selection is not deterministic")

    x2_select = {str(f): x2_inner_pi(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    outer = [
        score_outer(
            vitems,
            folds,
            parsed,
            f,
            selections[str(f)]["selected"],
            float(x2_select[str(f)]["selected_pi"]),
            parser,
        )
        for f in range(N_FOLDS)
    ]

    generated = {}
    rep0_hash = None
    for rep in REPS:
        items, diag, support = generate_selected(vitems, folds, parsed, selections, rep, parser)
        h = I.generated_items_hash(items)
        generated[f"rep{rep}"] = {
            "items_sha256": h,
            "support": support,
            "fold_diagnostics": diag,
        }
        if rep == 0:
            rep0_hash = h
    items2, _diag2, _support2 = generate_selected(vitems, folds, parsed, selections, 0, parser)
    rep0_repeat_hash = I.generated_items_hash(items2)
    deterministic_generation = bool(rep0_hash == rep0_repeat_hash)
    if not deterministic_generation:
        raise RuntimeError("fixed-seed selected generation is not deterministic")

    gains = [float(x["selected_gain_vs_X0_bits_per_token"]) for x in outer]
    x2_gains = [float(x["X2_gain_vs_X0_bits_per_token"]) for x in outer]
    selected_mean = float(np.mean([x["selected_bits_per_token"] for x in outer]))
    x0_mean = float(np.mean([x["X0_bits_per_token"] for x in outer]))
    x2_mean = float(np.mean([x["X2_HARD10_bits_per_token"] for x in outer]))
    predictive_pass = bool((x0_mean - selected_mean) > 0.0 and sum(g > 0.0 for g in gains) >= 4)

    plan = HERE.parent / "PLAN.md"
    amend = HERE.parent / "AMENDMENT_A.md"
    impl = HERE.parent / "IMPLEMENTATION_PREFLIGHT.md"
    out = {
        "schema": "issue90-phase0-preflight-v1",
        "phase": PHASE,
        "score_free": True,
        "target_score_calls": 0,
        "source": {
            "path": str(zl_path),
            "git_blob_sha1": I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": EXPECTED_ZL3B_BLOB,
        },
        "authority_hashes": {
            "PLAN.md": sha256_file(plan),
            "AMENDMENT_A.md": sha256_file(amend),
            "IMPLEMENTATION_PREFLIGHT.md": sha256_file(impl),
            "issue81_minimal_memory.py": sha256_file(ROOT / "experiments" / "cross-token-memory" / "issue81_minimal_memory.py"),
            "this_preflight": sha256_file(HERE),
        },
        "folds": fold_identity(folds),
        "fold_identity_sha256": fold_hash(folds),
        "candidate_grid": {
            "DECAY40": {"tau": list(TAU_GRID), "pi": list(PI_GRID)},
            "TILT10": {"beta": list(BETA_GRID)},
        },
        "selections": selections,
        "selection_repeat_sha256": I.sha256_obj(selections_repeat),
        "selection_sha256": I.sha256_obj(selections),
        "deterministic_selection": deterministic_selection,
        "X2_HARD10_replay_selection": x2_select,
        "outer_heldout_predictive": {
            "folds": outer,
            "summary": {
                "X0_mean_bits_per_token": x0_mean,
                "X2_HARD10_mean_bits_per_token": x2_mean,
                "selected_mean_bits_per_token": selected_mean,
                "selected_mean_gain_vs_X0": float(x0_mean - selected_mean),
                "selected_gain_by_fold": gains,
                "selected_positive_gain_folds": int(sum(g > 0.0 for g in gains)),
                "predictive_criterion_pass": predictive_pass,
                "X2_HARD10_mean_gain_vs_X0": float(x0_mean - x2_mean),
                "X2_HARD10_gain_by_fold": x2_gains,
            },
        },
        "score_free_generation": generated,
        "rep0_repeat_sha256": rep0_repeat_hash,
        "deterministic_generation": deterministic_generation,
        "firewall": {
            "S1_scored": False,
            "S2_scored": False,
            "H62_scored": False,
            "R1_target_scored": False,
            "issue84_target_used_for_selection": False,
        },
    }
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--preflight", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    modes = int(bool(ns.self_test)) + int(ns.preflight is not None)
    if modes != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    zl = Path(ns.preflight[0])
    out_path = Path(ns.preflight[1])
    result = run_preflight(zl)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "selection": {f: x["selected"] for f, x in result["selections"].items()},
        "predictive": result["outer_heldout_predictive"]["summary"],
        "target_score_calls": result["target_score_calls"],
        "deterministic_selection": result["deterministic_selection"],
        "deterministic_generation": result["deterministic_generation"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
