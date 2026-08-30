#!/usr/bin/env python3
"""Frozen Phase64A MG0 morphology utilities.

MG0 replaces an explicit empirical token inventory with a training-only
low-order character Markov generator. This module contains no Voynich
scorecard or pass/fail logic.
"""
from __future__ import annotations

import hashlib
import math
import random
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

ALPHA = 0.5
ORDERS = (0, 1, 2)
INNER_FOLDS = 5
MAX_TOKEN_LENGTH = 20
ATTEMPT_MULTIPLIER = 200
TIE_EPS = 1e-12
BOS = "<BOS>"
EOS = "<EOS>"


@dataclass
class MarkovModel:
    order: int
    alphabet: Tuple[str, ...]
    counts: Dict[Tuple[str, ...], Counter]
    totals: Dict[Tuple[str, ...], int]

    @property
    def symbols(self) -> Tuple[str, ...]:
        return self.alphabet + (EOS,)

    @property
    def nonzero_transition_cells(self) -> int:
        return sum(len(c) for c in self.counts.values())

    @property
    def observed_contexts(self) -> int:
        return len(self.counts)


def _assert_types(types: Iterable[str]) -> List[str]:
    out = sorted(set(types))
    if not out:
        raise RuntimeError("MG0 requires at least one training type")
    if any(not t for t in out):
        raise RuntimeError("MG0 training vocabulary contains empty token")
    return out


def outer_alphabet(types: Iterable[str]) -> Tuple[str, ...]:
    vv = _assert_types(types)
    alphabet = tuple(sorted(set("".join(vv))))
    if not alphabet:
        raise RuntimeError("MG0 training alphabet is empty")
    if BOS in alphabet or EOS in alphabet:
        raise RuntimeError("MG0 abstract marker collides with one-character alphabet")
    return alphabet


def inner_fold(token: str) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % INNER_FOLDS


def _initial_context(order: int) -> Tuple[str, ...]:
    if order not in ORDERS:
        raise RuntimeError(f"unsupported MG0 order: {order}")
    return tuple([BOS] * order)


def _advance(context: Tuple[str, ...], sym: str, order: int) -> Tuple[str, ...]:
    if order == 0:
        return ()
    return tuple((list(context) + [sym])[-order:])


def fit_model(types: Iterable[str], alphabet: Sequence[str], order: int) -> MarkovModel:
    vv = _assert_types(types)
    alphabet_tuple = tuple(alphabet)
    allowed = set(alphabet_tuple)
    if not allowed:
        raise RuntimeError("MG0 fit alphabet is empty")
    if any(c not in allowed for t in vv for c in t):
        raise RuntimeError("MG0 fit type contains character outside frozen outer alphabet")

    counts: Dict[Tuple[str, ...], Counter] = defaultdict(Counter)
    totals: Dict[Tuple[str, ...], int] = defaultdict(int)
    for token in vv:
        context = _initial_context(order)
        for sym in list(token) + [EOS]:
            counts[context][sym] += 1
            totals[context] += 1
            if sym != EOS:
                context = _advance(context, sym, order)
    return MarkovModel(order, alphabet_tuple, dict(counts), dict(totals))


def probability(model: MarkovModel, context: Tuple[str, ...], sym: str) -> float:
    symbols = model.symbols
    if sym not in symbols:
        return 0.0
    denom = model.totals.get(context, 0) + ALPHA * len(symbols)
    num = model.counts.get(context, {}).get(sym, 0) + ALPHA
    return float(num / denom)


def type_nll_per_symbol(model: MarkovModel, token: str) -> float:
    if not token:
        raise RuntimeError("cannot score empty token")
    if any(c not in set(model.alphabet) for c in token):
        raise RuntimeError("scored token contains character outside frozen outer alphabet")
    context = _initial_context(model.order)
    loss = 0.0
    n = 0
    for sym in list(token) + [EOS]:
        prob = probability(model, context, sym)
        if prob <= 0.0:
            raise RuntimeError("MG0 produced non-positive smoothed probability")
        loss -= math.log(prob)
        n += 1
        if sym != EOS:
            context = _advance(context, sym, model.order)
    return float(loss / n)


def select_order(types: Iterable[str]) -> Tuple[MarkovModel, dict]:
    vv = _assert_types(types)
    alphabet = outer_alphabet(vv)
    assignments = {t: inner_fold(t) for t in vv}
    fold_counts = {str(i): sum(assignments[t] == i for t in vv) for i in range(INNER_FOLDS)}
    if any(v == 0 for v in fold_counts.values()):
        raise RuntimeError(f"empty MG0 inner fold: {fold_counts}")

    scores: Dict[int, float] = {}
    per_fold: Dict[int, List[float]] = {}
    for order in ORDERS:
        token_losses: List[float] = []
        fold_losses: List[float] = []
        for inner in range(INNER_FOLDS):
            train = [t for t in vv if assignments[t] != inner]
            test = [t for t in vv if assignments[t] == inner]
            model = fit_model(train, alphabet, order)
            losses = [type_nll_per_symbol(model, t) for t in test]
            fold_losses.append(float(statistics.mean(losses)))
            token_losses.extend(losses)
        # Equal weight per distinct held-out type across the full nested CV.
        scores[order] = float(statistics.mean(token_losses))
        per_fold[order] = fold_losses

    best = ORDERS[0]
    for order in ORDERS[1:]:
        if scores[order] + TIE_EPS < scores[best]:
            best = order
        elif abs(scores[order] - scores[best]) <= TIE_EPS and order < best:
            best = order

    final = fit_model(vv, alphabet, best)
    return final, {
        "candidate_orders": list(ORDERS),
        "alpha": ALPHA,
        "inner_folds": INNER_FOLDS,
        "inner_fold_type_counts": fold_counts,
        "mean_type_normalized_nll": {str(k): scores[k] for k in ORDERS},
        "per_inner_fold_mean_nll": {str(k): per_fold[k] for k in ORDERS},
        "selected_order": best,
        "tie_epsilon": TIE_EPS,
        "training_types": len(vv),
        "alphabet_size": len(alphabet),
        "observed_contexts_final": final.observed_contexts,
        "nonzero_transition_cells_final": final.nonzero_transition_cells,
    }


def _draw_symbol(model: MarkovModel, context: Tuple[str, ...], rng: random.Random) -> str:
    u = rng.random()
    acc = 0.0
    symbols = model.symbols
    for sym in symbols:
        acc += probability(model, context, sym)
        if u < acc:
            return sym
    # Floating-point guard; exact distribution is normalized analytically.
    return symbols[-1]


def sample_type(model: MarkovModel, rng: random.Random) -> Tuple[str | None, str]:
    context = _initial_context(model.order)
    chars: List[str] = []
    while True:
        sym = _draw_symbol(model, context, rng)
        if sym == EOS:
            if not chars:
                return None, "empty"
            return "".join(chars), "accepted"
        chars.append(sym)
        if len(chars) > MAX_TOKEN_LENGTH:
            return None, "overlength"
        context = _advance(context, sym, model.order)


def generate_synthetic_vocab(model: MarkovModel, target_size: int, seed: int) -> Tuple[List[str], dict]:
    if target_size <= 0:
        raise RuntimeError("synthetic vocabulary target must be positive")
    max_attempts = ATTEMPT_MULTIPLIER * target_size
    rng = random.Random(seed)
    accepted = set()
    empty = 0
    overlength = 0
    duplicate = 0
    attempts = 0
    while len(accepted) < target_size and attempts < max_attempts:
        attempts += 1
        token, reason = sample_type(model, rng)
        if token is None:
            if reason == "empty":
                empty += 1
            elif reason == "overlength":
                overlength += 1
            else:
                raise RuntimeError(f"unknown MG0 rejection reason: {reason}")
            continue
        if token in accepted:
            duplicate += 1
            continue
        accepted.add(token)

    if len(accepted) != target_size:
        raise RuntimeError(
            f"MG0 uniqueness failure: generated {len(accepted)} / {target_size} unique types "
            f"after {attempts} / {max_attempts} attempts"
        )

    return sorted(accepted), {
        "seed": seed,
        "target_types": target_size,
        "generated_unique_types": len(accepted),
        "attempts": attempts,
        "max_attempts": max_attempts,
        "rejected_empty": empty,
        "rejected_overlength": overlength,
        "rejected_duplicate": duplicate,
        "membership_queries_against_empirical_vocab": 0,
        "max_token_length": MAX_TOKEN_LENGTH,
    }


def length_stats(vocab: Sequence[str]) -> dict:
    lengths = [len(t) for t in vocab]
    if not lengths:
        raise RuntimeError("cannot summarize empty vocabulary")
    return {
        "mean": float(statistics.mean(lengths)),
        "sd": float(statistics.pstdev(lengths)),
        "min": int(min(lengths)),
        "max": int(max(lengths)),
    }


def vocabulary_diagnostics(
    synthetic_vocab: Sequence[str],
    training_vocab: Sequence[str],
    heldout_vocab: Sequence[str],
    neighbors: Dict[str, List[str]],
    sampling: dict,
) -> dict:
    synth = set(synthetic_vocab)
    train = set(training_vocab)
    held = set(heldout_vocab)
    if len(synth) != len(synthetic_vocab):
        raise RuntimeError("synthetic vocabulary is not unique")
    degrees = [len(neighbors.get(t, ())) for t in synthetic_vocab]
    synth_chars = set("".join(synthetic_vocab))
    train_chars = set("".join(training_vocab))
    return {
        "sampling": sampling,
        "training_vocabulary_types": len(train),
        "synthetic_vocabulary_types": len(synth),
        "heldout_observed_types": len(held),
        "synthetic_overlap_training_types": len(synth & train),
        "synthetic_overlap_training_fraction": float(len(synth & train) / len(synth)),
        "synthetic_overlap_heldout_types": len(synth & held),
        "synthetic_overlap_heldout_fraction": float(len(synth & held) / len(synth)),
        "training_length_stats": length_stats(sorted(train)),
        "synthetic_length_stats": length_stats(synthetic_vocab),
        "synthetic_types_with_edit1_neighbor": sum(d > 0 for d in degrees),
        "synthetic_fraction_with_edit1_neighbor": float(sum(d > 0 for d in degrees) / len(degrees)),
        "synthetic_mean_edit1_degree": float(statistics.mean(degrees)),
        "synthetic_max_edit1_degree": int(max(degrees)),
        "training_alphabet_size": len(train_chars),
        "synthetic_alphabet_size": len(synth_chars),
        "synthetic_characters_absent_from_training": sorted(synth_chars - train_chars),
        "training_characters_absent_from_synthetic": sorted(train_chars - synth_chars),
    }
