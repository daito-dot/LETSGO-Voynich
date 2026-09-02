#!/usr/bin/env python3
"""Issue #81: minimal cross-token memory on frozen OGH-C V2.

Scientific authorities:
  experiments/cross-token-memory/PLAN_A.md
  experiments/cross-token-memory/IMPLEMENTATION_A.md

Modes:
  --self-test
  --stage1 ZL3b OUT.json
  --r1 ZL3b STAGE1.json MODEL REP OUT.json
  --aggregate STAGE1.json R1_DIR OUT.json
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in (
    "phase62",
    "phase63",
    "phase64",
    "issue26-music",
    "occupancy-generation-hierarchy",
):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as b  # noqa: E402
import phase62p_h62p1 as p62  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402
import ogh_a as A  # noqa: E402
import ogh_c as C  # noqa: E402

PHASE = "ISSUE81"
MODELS = ("X0", "X1", "X2", "X3", "X4")
PRIMARY_MODELS = ("X0", "X1", "X2", "X3")
REPS = (0, 1, 2)
N_FOLDS = 5
PI_GRID = np.linspace(0.0, 1.0, 101)
RECENT = 10
BOS = "<BOS>"
ENTRY = "ENTRY"
BODY = "BODY"
LN2 = math.log(2.0)
TIE_EPS = 1e-12


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=float).encode("utf-8")


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj)).hexdigest()


def seq_from_parse(picked) -> Tuple[int, ...]:
    sig, vals = picked
    return tuple(C.UNIT_INDEX[(s, vals[s])] for s in sig)


def mask_from_seq(seq: Sequence[int]) -> int:
    return int(sum(1 << C.UNITS[u][0] for u in seq))


def surface(tok: b.Token) -> str:
    return "".join(tok)


def surface_tuple(s: str) -> b.Token:
    return tuple(s)


def ordered(items: Sequence[b.Item]) -> List[b.Item]:
    return sorted(items, key=lambda x: (x.leaf if x.leaf is not None else 10**9, x.document, x.item_id))


def training_sequences(items: Sequence[b.Item], parsed: dict) -> List[Tuple[int, ...]]:
    return [
        seq
        for it in items
        for line in parsed[it.item_id]
        for seq in line
        if seq is not None
    ]


def training_vocab(items: Sequence[b.Item], parsed: dict) -> Counter:
    out: Counter = Counter()
    for it in items:
        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                if parsed[it.item_id][li][ti] is not None:
                    out[tok] += 1
    return out


class NeighborIndex:
    """Exact edit-distance-1 queries against a fixed training vocabulary."""

    def __init__(self, counts: Counter):
        self.counts = Counter(counts)
        self.vocab = set(self.counts)
        self.sub = defaultdict(set)
        self.longer_by_deleted = defaultdict(set)
        for w in self.vocab:
            for i in range(len(w)):
                self.sub[(len(w), i, w[:i], w[i + 1:])].add(w)
                self.longer_by_deleted[w[:i] + w[i + 1:]].add(w)
        self.cache: Dict[b.Token, Tuple[b.Token, ...]] = {}

    def neighbors(self, q: b.Token) -> Tuple[b.Token, ...]:
        got = self.cache.get(q)
        if got is not None:
            return got
        out = set()
        for i in range(len(q)):
            out.update(self.sub.get((len(q), i, q[:i], q[i + 1:]), ()))
            shorter = q[:i] + q[i + 1:]
            if shorter in self.vocab and shorter != q:
                out.add(shorter)
        out.update(self.longer_by_deleted.get(q, ()))
        out.discard(q)
        ans = tuple(sorted(x for x in out if b.edit1(q, x)))
        self.cache[q] = ans
        return ans

    def weighted_choice(self, rng: np.random.Generator, src: b.Token) -> b.Token | None:
        nb = self.neighbors(src)
        if not nb:
            return None
        w = np.asarray([self.counts[x] for x in nb], dtype=float)
        w /= w.sum()
        return nb[int(rng.choice(len(nb), p=w))]


class ContextV2Model:
    """A state-conditioned V2 table with frozen V2 as fixed BACKOFF prior."""

    def __init__(self, global_sequences: Sequence[Tuple[int, ...]], records: Sequence[Tuple[object, Tuple[int, ...]]]):
        self.global_model = C.V2Model(global_sequences)
        counts = defaultdict(lambda: defaultdict(Counter))
        for state, seq in records:
            prev2, prev = C.NONE, C.START
            for u in list(seq) + [C.STOP]:
                counts[state][(prev2, prev)][u] += 1
                prev2, prev = prev, u
        self.table = {}
        for state, by_ctx in counts.items():
            for ctx, cnt in by_ctx.items():
                p2, p1 = ctx
                allowed, base = self.global_model._dist(p2, p1)
                n = np.asarray([cnt[x] for x in allowed], dtype=float)
                self.table[(state, p2, p1)] = (
                    allowed,
                    (n + C.B.BACKOFF * base) / (n.sum() + C.B.BACKOFF),
                )
        self.observed_states = len(counts)
        self.observed_state_contexts = len(self.table)
        self.free_parameters = int(sum(len(v[0]) - 1 for v in self.table.values()))

    def _dist(self, state, prev2, prev):
        return self.table.get((state, prev2, prev), self.global_model._dist(prev2, prev))

    def logp(self, seq: Sequence[int], state) -> float:
        lp, prev2, prev = 0.0, C.NONE, C.START
        for u in list(seq) + [C.STOP]:
            allowed, pr = self._dist(state, prev2, prev)
            pos = int(np.searchsorted(allowed, u))
            if pos >= len(allowed) or int(allowed[pos]) != int(u):
                return -math.inf
            lp += math.log(float(pr[pos]))
            prev2, prev = prev, u
        return lp

    def sample(self, rng: np.random.Generator, state) -> Tuple[int, ...]:
        out, prev2, prev = [], C.NONE, C.START
        while True:
            allowed, pr = self._dist(state, prev2, prev)
            u = int(allowed[int(rng.choice(len(allowed), p=pr))])
            if u == C.STOP:
                return tuple(out)
            out.append(u)
            prev2, prev = prev, u


def exact_surface_probability(model, parser: e.SlotParser, tok: b.Token, state=None) -> float:
    total = 0.0
    for picked in parser.parses(surface(tok)):
        seq = seq_from_parse(picked)
        lp = model.logp(seq) if state is None else model.logp(seq, state)
        if math.isfinite(lp):
            total += math.exp(lp)
    return float(total)


def x1_records(items: Sequence[b.Item], parsed: dict) -> List[Tuple[object, Tuple[int, ...]]]:
    rec = []
    current_leaf = None
    prev_known = True
    prev_state = BOS
    for it in ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            prev_known = True
            prev_state = BOS
        for li, line in enumerate(it.lines):
            for ti, _tok in enumerate(line):
                seq = parsed[it.item_id][li][ti]
                if seq is not None and prev_known:
                    rec.append((prev_state, seq))
                if seq is None:
                    prev_known = False
                else:
                    prev_known = True
                    prev_state = mask_from_seq(seq)
    return rec


def x3_records(items: Sequence[b.Item], parsed: dict) -> List[Tuple[str, Tuple[int, ...]]]:
    rec = []
    for it in items:
        for li, line in enumerate(it.lines):
            state = ENTRY if li == 0 else BODY
            for ti, _tok in enumerate(line):
                seq = parsed[it.item_id][li][ti]
                if seq is not None:
                    rec.append((state, seq))
    return rec


def memory_q(target: b.Token, history: Sequence[b.Token], index: NeighborIndex) -> Tuple[float, int]:
    eligible = []
    for src in history[-RECENT:]:
        nb = index.neighbors(src)
        if nb:
            eligible.append((src, nb))
    if not eligible:
        return 0.0, 0
    q = 0.0
    for _src, nb in eligible:
        if target not in nb:
            continue
        denom = float(sum(index.counts[x] for x in nb))
        q += float(index.counts[target] / denom)
    return float(q / len(eligible)), len(eligible)


def sample_memory(rng: np.random.Generator, history: Sequence[b.Token], index: NeighborIndex) -> b.Token | None:
    eligible = [src for src in history[-RECENT:] if index.neighbors(src)]
    if not eligible:
        return None
    src = eligible[int(rng.choice(len(eligible)))]
    return index.weighted_choice(rng, src)


def inner_cv_pi(vitems, folds, parsed, outer_f: int, parser: e.SlotParser) -> dict:
    components = []
    fold_details = []
    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        excluded = set(folds[outer_f]) | set(folds[inner_g])
        tr_items = b.by_leaves(vitems, excluded, include=False)
        va_items = b.by_leaves(vitems, folds[inner_g], include=True)
        seqs = training_sequences(tr_items, parsed)
        v2 = C.V2Model(seqs)
        index = NeighborIndex(training_vocab(tr_items, parsed))
        p_cache: Dict[b.Token, float] = {}
        current_leaf = None
        history: List[b.Token] = []
        rows = []
        for it in ordered(va_items):
            if it.leaf != current_leaf:
                current_leaf = it.leaf
                history = []
            for li, line in enumerate(it.lines):
                for ti, tok in enumerate(line):
                    seq = parsed[it.item_id][li][ti]
                    if seq is not None:
                        pv = p_cache.get(tok)
                        if pv is None:
                            pv = exact_surface_probability(v2, parser, tok)
                            p_cache[tok] = pv
                        qv, eligible = memory_q(tok, history, index)
                        if pv <= 0:
                            raise RuntimeError("V2 assigned non-positive probability to a parseable validation token")
                        rows.append((pv, qv, eligible > 0))
                    history.append(tok)
                    if len(history) > RECENT:
                        history = history[-RECENT:]
        if not rows:
            raise RuntimeError(f"outer {outer_f} inner {inner_g}: no validation tokens")
        components.extend(rows)
        fold_details.append({
            "inner_validation_fold": inner_g,
            "n_tokens": len(rows),
            "n_context_available": int(sum(r[2] for r in rows)),
            "training_vocab_types": len(index.vocab),
        })

    pp = np.asarray([x[0] for x in components], dtype=float)
    qq = np.asarray([x[1] for x in components], dtype=float)
    hh = np.asarray([x[2] for x in components], dtype=bool)
    curve = []
    best_pi = None
    best_ll = -math.inf
    for pi in PI_GRID:
        mix = pp.copy()
        mix[hh] = (1.0 - pi) * pp[hh] + pi * qq[hh]
        if np.any(mix <= 0):
            ll = -math.inf
        else:
            ll = float(np.log(mix).sum())
        curve.append(ll)
        if ll > best_ll + TIE_EPS:
            best_ll = ll
            best_pi = float(pi)
    if best_pi is None:
        raise RuntimeError(f"outer {outer_f}: pi selection failed")
    return {
        "outer_fold": outer_f,
        "selected_pi": best_pi,
        "n_scored_tokens": int(len(pp)),
        "n_context_available": int(hh.sum()),
        "best_total_log_likelihood": best_ll,
        "pi_grid": [float(x) for x in PI_GRID],
        "total_log_likelihood_curve": curve,
        "inner_folds": fold_details,
    }


def fit_outer(vitems, folds, parsed, f: int):
    tr_items = b.by_leaves(vitems, folds[f], include=False)
    seqs = training_sequences(tr_items, parsed)
    if not seqs:
        raise RuntimeError(f"fold {f}: no V2 training sequences")
    v2 = C.V2Model(seqs)
    x1 = ContextV2Model(seqs, x1_records(tr_items, parsed))
    x3 = ContextV2Model(seqs, x3_records(tr_items, parsed))
    index = NeighborIndex(training_vocab(tr_items, parsed))
    return tr_items, v2, x1, x3, index


def outer_cross_entropy(vitems, folds, parsed, f: int, pi: float, parser: e.SlotParser) -> dict:
    _tr, v2, x1, x3, index = fit_outer(vitems, folds, parsed, f)
    test = b.by_leaves(vitems, folds[f], include=True)
    caches = {"X0": {}, "X1": {}, "X3": {}}
    logs = {"X0": [], "X1": [], "X2": [], "X3": [], "X4": []}
    min_code = []
    current_leaf = None
    history: List[b.Token] = []
    prev_known = True
    prev_state = BOS
    n_context = 0
    for it in ordered(test):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            history = []
            prev_known = True
            prev_state = BOS
        for li, line in enumerate(it.lines):
            line_state = ENTRY if li == 0 else BODY
            for ti, tok in enumerate(line):
                seq = parsed[it.item_id][li][ti]
                if seq is not None:
                    p0 = caches["X0"].get(tok)
                    if p0 is None:
                        p0 = exact_surface_probability(v2, parser, tok)
                        caches["X0"][tok] = p0
                    if p0 <= 0:
                        raise RuntimeError("outer V2 surface probability is non-positive")
                    logs["X0"].append(math.log(p0))
                    min_code.append(v2.logp(seq))

                    if prev_known:
                        k1 = (prev_state, tok)
                        p1 = caches["X1"].get(k1)
                        if p1 is None:
                            p1 = exact_surface_probability(x1, parser, tok, prev_state)
                            caches["X1"][k1] = p1
                    else:
                        p1 = p0
                    logs["X1"].append(math.log(p1))

                    k3 = (line_state, tok)
                    p3 = caches["X3"].get(k3)
                    if p3 is None:
                        p3 = exact_surface_probability(x3, parser, tok, line_state)
                        caches["X3"][k3] = p3
                    logs["X3"].append(math.log(p3))

                    qv, eligible = memory_q(tok, history, index)
                    if eligible:
                        n_context += 1
                        p2 = (1.0 - pi) * p0 + pi * qv
                        p4 = (1.0 - pi) * p3 + pi * qv
                    else:
                        p2, p4 = p0, p3
                    if p2 <= 0 or p4 <= 0:
                        raise RuntimeError("selected mixture assigned non-positive held-out probability")
                    logs["X2"].append(math.log(p2))
                    logs["X4"].append(math.log(p4))

                if seq is None:
                    prev_known = False
                else:
                    prev_known = True
                    prev_state = mask_from_seq(seq)
                history.append(tok)
                if len(history) > RECENT:
                    history = history[-RECENT:]

    n = len(logs["X0"])
    out = {
        m: float(-np.mean(logs[m]) / LN2) for m in logs if logs[m]
    }
    out.update({
        "fold": f,
        "selected_pi": float(pi),
        "n_v2_support_tokens": n,
        "n_memory_context_available": n_context,
        "memory_context_fraction": float(n_context / n) if n else None,
        "X0_frozen_min_parse_code_bits_per_token": float(-np.mean(min_code) / LN2) if min_code else None,
        "X1_observed_states": x1.observed_states,
        "X1_observed_state_contexts": x1.observed_state_contexts,
        "X3_observed_states": x3.observed_states,
        "X3_observed_state_contexts": x3.observed_state_contexts,
        "training_vocab_types": len(index.vocab),
    })
    return out


def generated_items_hash(items: Sequence[b.Item]) -> str:
    payload = [
        {
            "item_id": it.item_id,
            "document": it.document,
            "leaf": it.leaf,
            "lines": [[surface(tok) for tok in line] for line in it.lines],
        }
        for it in ordered(items)
    ]
    return sha256_obj(payload)


def generate_candidate(model_name: str, rep: int, vitems, folds, parsed, pi_by_fold: Dict[int, float]):
    if model_name not in MODELS:
        raise RuntimeError(model_name)
    parser = e.SlotParser()
    e.validate_parser(parser)
    items: List[b.Item] = []
    diagnostics = {}
    for f in range(N_FOLDS):
        _tr, v2, x1, x3, index = fit_outer(vitems, folds, parsed, f)
        pi = float(pi_by_fold[f])
        rng = np.random.default_rng(e.stable_seed(f"{PHASE}:{model_name}:fold{f}:rep{rep}"))
        current_leaf = None
        history: List[b.Token] = []
        prev_known = True
        prev_state = BOS
        attempted = actual = fallback = 0
        n_tokens = 0
        held = ordered(b.by_leaves(vitems, folds[f], include=True))
        for it in held:
            if it.leaf != current_leaf:
                current_leaf = it.leaf
                history = []
                prev_known = True
                prev_state = BOS
            lines = []
            for li, line in enumerate(it.lines):
                state = ENTRY if li == 0 else BODY
                new = []
                for _orig in line:
                    out_tok: b.Token
                    if model_name in ("X2", "X4") and float(rng.random()) < pi:
                        attempted += 1
                        mem = sample_memory(rng, history, index)
                        if mem is not None:
                            out_tok = mem
                            actual += 1
                        else:
                            fallback += 1
                            seq = x3.sample(rng, state) if model_name == "X4" else v2.sample(rng)
                            out_tok = surface_tuple(C.units_to_string(seq))
                    elif model_name == "X1":
                        seq = x1.sample(rng, prev_state) if prev_known else v2.sample(rng)
                        out_tok = surface_tuple(C.units_to_string(seq))
                    elif model_name == "X3":
                        seq = x3.sample(rng, state)
                        out_tok = surface_tuple(C.units_to_string(seq))
                    elif model_name == "X4":
                        seq = x3.sample(rng, state)
                        out_tok = surface_tuple(C.units_to_string(seq))
                    else:
                        seq = v2.sample(rng)
                        out_tok = surface_tuple(C.units_to_string(seq))

                    if model_name == "X1":
                        picked = parser.pick(surface(out_tok), "min")
                        if picked is None:
                            prev_known = False
                        else:
                            prev_known = True
                            prev_state = int(sum(1 << s for s in picked[0]))
                    if model_name in ("X2", "X4"):
                        history.append(out_tok)
                        if len(history) > RECENT:
                            history = history[-RECENT:]
                    new.append(out_tok)
                    n_tokens += 1
                lines.append(new)
            items.append(b.Item(item_id=it.item_id, document=it.document, lines=lines, leaf=it.leaf))
        diagnostics[str(f)] = {
            "fold": f,
            "pi": pi,
            "n_tokens": n_tokens,
            "memory_attempts": attempted,
            "memory_events": actual,
            "memory_no_source_fallbacks": fallback,
            "memory_event_rate": float(actual / n_tokens) if n_tokens else 0.0,
            "memory_attempt_rate": float(attempted / n_tokens) if n_tokens else 0.0,
            "training_vocab_types": len(index.vocab),
            "X1_observed_states": x1.observed_states,
            "X1_observed_state_contexts": x1.observed_state_contexts,
            "X1_context_free_parameters": x1.free_parameters,
            "X3_observed_states": x3.observed_states,
            "X3_observed_state_contexts": x3.observed_state_contexts,
            "X3_context_free_parameters": x3.free_parameters,
        }
    items = ordered(items)
    return items, diagnostics


def metric_gates(aggregate: dict, evaluation: dict, contexts: Sequence[dict], p63a: dict) -> dict:
    target_s1 = float(np.mean([ctx["target_exposed"]["S1"] for ctx in contexts]))
    target_s2 = float(np.mean([ctx["target_exposed"]["S2"] for ctx in contexts]))
    cand_s1 = float(np.mean(list(aggregate["S1_by_fold"].values())))
    cand_s2 = float(aggregate["S2"])
    s1_ratio = cand_s1 / target_s1 if abs(target_s1) > TIE_EPS else None
    s2_ratio = cand_s2 / target_s2 if abs(target_s2) > TIE_EPS else None
    s1_sign = bool(cand_s1 * target_s1 > 0)
    s1_pass = bool(s1_sign and s1_ratio is not None and 0.5 <= s1_ratio <= 2.0)
    s2_pass = bool(s2_ratio is not None and 0.5 <= s2_ratio <= 2.0)

    target_raw = [float(ctx["target_H62P1"]["abs_excess_sum"]) for ctx in contexts]
    target_raw_mean = float(np.mean(target_raw))
    cand_raw = float(aggregate["H62P1"]["abs_excess_sum"])
    raw_ratio = cand_raw / target_raw_mean if target_raw_mean > TIE_EPS else None
    raw_pass = bool(raw_ratio is not None and raw_ratio >= 0.5)

    h62 = evaluation["H62P1_summary"]
    a1 = p63a["across_fold"]["A1_R1_H62P1_summary"]
    profile_pass = bool(
        h62["mean_D_profile"] <= a1["mean_D_profile"] + TIE_EPS
        and h62["mean_abs_C_short_diff"] <= a1["mean_abs_C_short_diff"] + TIE_EPS
    )
    x2_responsibility = bool(s2_pass and raw_pass and profile_pass)
    return {
        "S1": {
            "target_mean": target_s1,
            "candidate_mean": cand_s1,
            "ratio": s1_ratio,
            "same_sign": s1_sign,
            "pass": s1_pass,
        },
        "S2": {
            "target_mean": target_s2,
            "candidate": cand_s2,
            "ratio": s2_ratio,
            "pass": s2_pass,
        },
        "H62_raw": {
            "candidate_abs_excess_sum": cand_raw,
            "target_abs_excess_sum_by_fold": target_raw,
            "target_abs_excess_sum_mean": target_raw_mean,
            "ratio_to_target_mean": raw_ratio,
            "ratio_to_each_target_fold": [cand_raw / x if x > TIE_EPS else None for x in target_raw],
            "pass": raw_pass,
        },
        "H62_profile": {
            "candidate": h62,
            "A1_R1_frozen_comparator": a1,
            "pass": profile_pass,
        },
        "X2_responsibility_pass": x2_responsibility,
        "X3_responsibility_pass": s1_pass,
        "cross_token_full_without_R1": bool(s1_pass and s2_pass and raw_pass and profile_pass),
    }


def evaluate_model(model_name: str, pi_by_fold: Dict[int, float], vitems, folds, parsed, contexts, p63a):
    reps = {}
    generation = {}
    for rep in REPS:
        items, diag = generate_candidate(model_name, rep, vitems, folds, parsed, pi_by_fold)
        h = generated_items_hash(items)
        metrics = n64.output_metrics(items, f"{PHASE}:{model_name}:rep{rep}", contexts)
        reps[f"rep{rep}"] = metrics
        generation[f"rep{rep}"] = {"items_sha256": h, "diagnostics": diag}
        print(
            f"{model_name} rep{rep}: S2={metrics['S2']:.6f} "
            f"H62raw={metrics['H62P1']['abs_excess_sum']:.6f} "
            f"Cshort={metrics['H62P1']['C_short']}",
            file=sys.stderr,
            flush=True,
        )
    aggregate = n64.aggregate_realizations(reps, f"{PHASE}:{model_name}")
    evaluation = n64.evaluate_aggregate(aggregate, contexts, p63a, f"{PHASE}:{model_name}")
    gates = metric_gates(aggregate, evaluation, contexts, p63a)
    return {
        "model": model_name,
        "pi_by_fold": {str(k): float(v) for k, v in pi_by_fold.items()},
        "realizations": reps,
        "generation": generation,
        "aggregate": aggregate,
        "frozen_phase64_evaluation": evaluation,
        "issue81_gates": gates,
    }


def stage1(zl_path: Path) -> dict:
    vitems, folds, parsed = C.load_corpus(zl_path)
    parser = e.SlotParser()
    e.validate_parser(parser)
    p62c = json.loads((EXPERIMENTS / "phase62" / "phase62c_c0_a1_results.json").read_text(encoding="utf-8"))
    p63a = json.loads((EXPERIMENTS / "phase63" / "phase63a_training_vocab_results.json").read_text(encoding="utf-8"))
    contexts, _ = n64.fold_contexts(zl_path, p62c, p63a)

    selections = {str(f): inner_cv_pi(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    pi_by_fold = {f: float(selections[str(f)]["selected_pi"]) for f in range(N_FOLDS)}
    cross_entropy = [outer_cross_entropy(vitems, folds, parsed, f, pi_by_fold[f], parser) for f in range(N_FOLDS)]
    ce_summary = {}
    for m in MODELS:
        vals = [row[m] for row in cross_entropy if m in row]
        ce_summary[m] = {"mean_bits_per_token": float(np.mean(vals)), "by_fold": vals}
    ce_summary["X0_frozen_min_parse_code"] = {
        "mean_bits_per_token": float(np.mean([x["X0_frozen_min_parse_code_bits_per_token"] for x in cross_entropy])),
        "by_fold": [x["X0_frozen_min_parse_code_bits_per_token"] for x in cross_entropy],
    }
    ce_summary["X2_exact_surface_bits_saved_vs_X0"] = float(ce_summary["X0"]["mean_bits_per_token"] - ce_summary["X2"]["mean_bits_per_token"])

    zero_pi = {f: 0.0 for f in range(N_FOLDS)}
    results = {
        "X0": evaluate_model("X0", zero_pi, vitems, folds, parsed, contexts, p63a),
        "X1": evaluate_model("X1", zero_pi, vitems, folds, parsed, contexts, p63a),
        "X2": evaluate_model("X2", pi_by_fold, vitems, folds, parsed, contexts, p63a),
        "X3": evaluate_model("X3", zero_pi, vitems, folds, parsed, contexts, p63a),
    }
    x2g = results["X2"]["issue81_gates"]
    x3g = results["X3"]["issue81_gates"]
    x4_licensed = bool(
        x2g["X2_responsibility_pass"]
        and not x2g["S1"]["pass"]
        and x3g["S1"]["pass"]
        and not x3g["X2_responsibility_pass"]
    )
    license_detail = {
        "licensed": x4_licensed,
        "X2_passes_S2_plus_H62": x2g["X2_responsibility_pass"],
        "X2_fails_S1": not x2g["S1"]["pass"],
        "X3_passes_S1": x3g["S1"]["pass"],
        "X3_fails_X2_responsibility": not x3g["X2_responsibility_pass"],
    }
    if x4_licensed:
        results["X4"] = evaluate_model("X4", pi_by_fold, vitems, folds, parsed, contexts, p63a)
    out = {
        "schema": "issue81-stage1-v1",
        "phase": PHASE,
        "target_reveal": True,
        "source_blob": b.git_blob_sha1(zl_path.read_bytes()),
        "plan_sha256": hashlib.sha256((HERE.parent / "PLAN_A.md").read_bytes()).hexdigest(),
        "implementation_sha256": hashlib.sha256((HERE.parent / "IMPLEMENTATION_A.md").read_bytes()).hexdigest(),
        "pi_selection": selections,
        "selected_pi_by_fold": {str(k): v for k, v in pi_by_fold.items()},
        "heldout_cross_entropy": {"folds": cross_entropy, "summary": ce_summary},
        "models": results,
        "X4_license": license_detail,
        "interpretation_boundary": {
            "plaintext_recovered": False,
            "semantic_content_tested": False,
            "decipherment_established": False,
        },
    }
    return out


def candidate_r1_dataset(items: Sequence[b.Item], folds) -> Tuple[dict, dict]:
    parser = e.SlotParser()
    e.validate_parser(parser)
    leaf_fold = {}
    for f, leaves in enumerate(folds):
        for leaf in leaves:
            if leaf in leaf_fold:
                raise RuntimeError("leaf appears in multiple frozen folds")
            leaf_fold[leaf] = f
    line_rows = []
    line_folds = []
    visible = parsed_n = 0
    for it in ordered(items):
        if it.leaf not in leaf_fold:
            raise RuntimeError(f"generated item leaf outside frozen folds: {it.item_id}")
        f = leaf_fold[it.leaf]
        for line in it.lines:
            rr = []
            for tok in line:
                visible += 1
                picked = parser.pick(surface(tok), "min")
                if picked is None:
                    continue
                row = np.zeros(12, dtype=np.uint8)
                row[list(picked[0])] = 1
                rr.append(row)
                parsed_n += 1
            line_rows.append(rr)
            line_folds.append(f)
    if not line_rows:
        raise RuntimeError("candidate has no lines")
    maxlen = max((len(x) for x in line_rows), default=0)
    if maxlen <= 0:
        raise RuntimeError("candidate has no parsable tokens")
    padded = np.zeros((len(line_rows), maxlen, 12), dtype=np.uint8)
    line_mask = np.zeros((len(line_rows), maxlen), dtype=bool)
    fold_pad = np.full((len(line_rows), maxlen), -1, dtype=np.int8)
    for i, (rr, f) in enumerate(zip(line_rows, line_folds)):
        if rr:
            arr = np.stack(rr)
            padded[i, : len(rr)] = arr
            line_mask[i, : len(rr)] = True
            fold_pad[i, : len(rr)] = f
    X = padded[line_mask]
    token_folds = fold_pad[line_mask]
    d = {
        "X": X,
        "token_folds": token_folds,
        "padded": padded,
        "line_mask": line_mask,
    }
    info = {
        "visible_tokens": visible,
        "parsed_tokens": parsed_n,
        "parser_coverage": float(parsed_n / visible) if visible else 0.0,
        "n_lines": len(line_rows),
        "fold_parsed_tokens": [int(np.sum(token_folds == f)) for f in range(N_FOLDS)],
    }
    return d, info


def score_r1(items: Sequence[b.Item], model: str, rep: int, folds) -> dict:
    d, parse_info = candidate_r1_dataset(items, folds)
    targets, target_authority = A.load_target_references()
    label = f"{PHASE} {model} rep{rep}"
    ref_ns = f"{PHASE}:{model}:rep{rep}:reference-null"
    test_ns = f"{PHASE}:{model}:rep{rep}:test-null"
    real_q = A.q_views_candidate(d, d["X"], True)
    sref = A.build_reference(d, ref_ns, label)
    real_z = A.residualize(real_q, sref)
    E = A.c58.residual_energy(real_z["full"])
    W = A.reliability(real_z)
    nulls = A.test_nulls(d, sref, targets, test_ns, label)
    p_exist = A.c58.empirical_upper_p(E, nulls["energy"])
    existence_pass = bool(W["valid_folds"] >= 4 and W["median"] is not None and W["median"] >= 0.50 and p_exist <= 0.01)
    topology = A.topology_result(real_z["full"], targets, nulls)
    parser_gate = bool(parse_info["parser_coverage"] >= 0.60)
    r1_pass = bool(parser_gate and existence_pass and all(x["effect_and_familywise_gate_pass"] for x in topology.values()))
    return {
        "schema": "issue81-r1-v1",
        "phase": PHASE,
        "model": model,
        "rep": rep,
        "target_authority": target_authority,
        "parser": {**parse_info, "coverage_gate_0.60": parser_gate},
        "null_design": {
            "reference_namespace": ref_ns,
            "test_namespace": test_ns,
            "n_reference": A.N_REF,
            "n_test": A.N_TEST,
            "null_operation": "within-line, per-slot occupancy permutation across reparsed generated tokens",
        },
        "real_R1": {
            "q_full": real_q["full"].tolist(),
            "z_full": real_z["full"].tolist(),
            "residual_energy": E,
            "within_reliability": W,
        },
        "R1_residual_existence": {
            "E": E,
            "W": W["median"],
            "valid_reliability_folds": W["valid_folds"],
            "p_exist_maxT_candidate_family": p_exist,
            "pass": existence_pass,
        },
        "R1_topology": topology,
        "R1_pass": r1_pass,
        "test_null": {
            "energy_summary": A.c58.summary(nulls["energy"]),
            "correlation_maxT_summary": A.c58.summary(nulls["correlation_maxT"]),
            "sign_maxT_summary": A.c58.summary(nulls["sign_maxT"]),
            "energy_values": nulls["energy"].tolist(),
            "correlation_maxT_values": nulls["correlation_maxT"].tolist(),
            "sign_maxT_values": [int(x) for x in nulls["sign_maxT"]],
        },
    }


def run_r1(zl_path: Path, stage1_path: Path, model: str, rep: int) -> dict:
    if model not in MODELS or rep not in REPS:
        raise RuntimeError("model/rep outside frozen family")
    s1 = json.loads(stage1_path.read_text(encoding="utf-8"))
    if s1.get("schema") != "issue81-stage1-v1":
        raise RuntimeError("stage1 authority mismatch")
    if model == "X4" and not s1["X4_license"]["licensed"]:
        return {"schema": "issue81-r1-v1", "phase": PHASE, "model": model, "rep": rep, "status": "NOT_LICENSED"}
    if model not in s1["models"]:
        raise RuntimeError(f"{model} absent from stage1 authority")
    vitems, folds, parsed = C.load_corpus(zl_path)
    pi_by_fold = {int(k): float(v) for k, v in s1["models"][model]["pi_by_fold"].items()}
    items, _diag = generate_candidate(model, rep, vitems, folds, parsed, pi_by_fold)
    h = generated_items_hash(items)
    expected = s1["models"][model]["generation"][f"rep{rep}"]["items_sha256"]
    if h != expected:
        raise RuntimeError(f"generation hash mismatch: {h} != {expected}")
    out = score_r1(items, model, rep, folds)
    out["status"] = "OK"
    out["generated_items_sha256"] = h
    return out


def final_classification(model: str, gates: dict, r1_all: bool) -> str:
    full = bool(
        gates["S1"]["pass"]
        and gates["S2"]["pass"]
        and gates["H62_raw"]["pass"]
        and gates["H62_profile"]["pass"]
        and r1_all
    )
    if full:
        return "RECOVERS"
    if model == "X2" and gates["X2_responsibility_pass"]:
        return "PARTIAL"
    if model == "X3" and gates["X3_responsibility_pass"]:
        return "PARTIAL"
    if model == "X4" and (gates["X2_responsibility_pass"] or gates["X3_responsibility_pass"]):
        return "PARTIAL"
    return "INSUFFICIENT"


def aggregate_final(stage1_path: Path, r1_dir: Path) -> dict:
    s1 = json.loads(stage1_path.read_text(encoding="utf-8"))
    if s1.get("schema") != "issue81-stage1-v1":
        raise RuntimeError("stage1 authority mismatch")
    models = {}
    for model, row in s1["models"].items():
        rr = {}
        for rep in REPS:
            pth = r1_dir / f"{model}_rep{rep}.json"
            if not pth.is_file():
                raise RuntimeError(f"missing R1 result: {pth}")
            x = json.loads(pth.read_text(encoding="utf-8"))
            if x.get("model") != model or int(x.get("rep", -1)) != rep:
                raise RuntimeError(f"R1 identity mismatch: {pth}")
            rr[f"rep{rep}"] = x
        r1_all = all(x.get("status") == "OK" and x.get("R1_pass") for x in rr.values())
        gates = row["issue81_gates"]
        cls = final_classification(model, gates, r1_all)
        models[model] = {
            "classification": cls,
            "issue81_gates": gates,
            "R1_all_three_reps_pass": r1_all,
            "R1_reps": rr,
            "pi_by_fold": row["pi_by_fold"],
        }

    recoverers = [m for m in MODELS if m in models and models[m]["classification"] == "RECOVERS"]
    if not recoverers:
        conclusion = "PREDECLARED MINIMAL MEMORY FAMILY INSUFFICIENT"
    elif "X0" in recoverers:
        conclusion = "MEMORYLESS V2 SUFFICIENT — CONTRADICTS PRIOR CROSS-TOKEN FAILURE"
    elif "X1" in recoverers:
        conclusion = "PREVIOUS-TOKEN SHAPE MEMORY SUFFICIENT"
    elif "X2" in recoverers:
        conclusion = "NEAR-FAMILY MEMORY SUFFICIENT"
    elif "X3" in recoverers:
        conclusion = "PARAGRAPH-ENTRY STATE SUFFICIENT"
    elif "X4" in recoverers:
        conclusion = "TWO-COMPONENT X2+X3 MEMORY REQUIRED"
    else:
        conclusion = "RECOVERY WITHOUT UNIQUE MINIMAL LABEL"
    return {
        "schema": "issue81-final-v1",
        "phase": PHASE,
        "stage1_sha256": hashlib.sha256(stage1_path.read_bytes()).hexdigest(),
        "X4_license": s1["X4_license"],
        "heldout_cross_entropy": s1["heldout_cross_entropy"],
        "models": models,
        "recoverers": recoverers,
        "conclusion": conclusion,
        "interpretation_boundary": s1["interpretation_boundary"],
    }


def self_test():
    toy = Counter({tuple("kal"): 4, tuple("kar"): 3, tuple("okal"): 2, tuple("dal"): 2, tuple("dam"): 1})
    idx = NeighborIndex(toy)
    frozen = b.build_neighbors(toy)
    for w in toy:
        if set(idx.neighbors(w)) != set(frozen[w]):
            raise RuntimeError(f"neighbor regression mismatch for {w}")
    rng = np.random.default_rng(1)
    seqs = []
    for _ in range(200):
        seq = C.V2Model.__mro__  # keep import path exercised before constructing synthetic legal rows
        del seq
        slots = sorted(rng.choice(12, size=int(rng.integers(1, 4)), replace=False).tolist())
        uu = tuple(C.UNIT_INDEX[(s, e.SLOTS[s][0])] for s in slots)
        seqs.append(uu)
    records = [(ENTRY if i % 2 == 0 else BODY, s) for i, s in enumerate(seqs)]
    mod = ContextV2Model(seqs, records)
    for state in (ENTRY, BODY, "UNSEEN"):
        smp = mod.sample(rng, state)
        if not smp:
            raise RuntimeError("context model emitted empty token")
        if any(C.UNIT_SLOT[a] >= C.UNIT_SLOT[c] for a, c in zip(smp, smp[1:])):
            raise RuntimeError("context model violated slot order")
    print(json.dumps({"issue81_self_test": "ok", "neighbor_types": len(toy), "context_states": mod.observed_states}))


def main(argv: Sequence[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--self-test":
        self_test()
        return 0
    if len(argv) == 4 and argv[1] == "--stage1":
        out = stage1(Path(argv[2]).resolve())
        Path(argv[3]).write_text(json.dumps(out, sort_keys=True, indent=1, default=float) + "\n", encoding="utf-8")
        print(json.dumps({
            "selected_pi_by_fold": out["selected_pi_by_fold"],
            "cross_entropy": out["heldout_cross_entropy"]["summary"],
            "X4_license": out["X4_license"],
            "gates": {m: r["issue81_gates"] for m, r in out["models"].items()},
        }, indent=1, default=float))
        return 0
    if len(argv) == 7 and argv[1] == "--r1":
        model = argv[4]
        rep = int(argv[5])
        out = run_r1(Path(argv[2]).resolve(), Path(argv[3]).resolve(), model, rep)
        Path(argv[6]).write_text(json.dumps(out, sort_keys=True, indent=1, default=float) + "\n", encoding="utf-8")
        print(json.dumps({"model": model, "rep": rep, "status": out.get("status"), "R1_pass": out.get("R1_pass")}, indent=1))
        return 0
    if len(argv) == 5 and argv[1] == "--aggregate":
        out = aggregate_final(Path(argv[2]).resolve(), Path(argv[3]).resolve())
        Path(argv[4]).write_text(json.dumps(out, sort_keys=True, indent=1, default=float) + "\n", encoding="utf-8")
        print(json.dumps({
            "conclusion": out["conclusion"],
            "recoverers": out["recoverers"],
            "classifications": {m: x["classification"] for m, x in out["models"].items()},
        }, indent=1))
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
