#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np
from numba import njit

ALPHABET = tuple("abcdefghiklmnopqrstuwxyz")
A = len(ALPHABET)
AI = {c: i for i, c in enumerate(ALPHABET)}
ALPHA = 0.1
M = 23
TARGET_EVENTS = 140_000
RESTARTS = 8
STEPS = 20_000
T1 = 0.00005
EPS = 1e-12
CREMMA_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
CANDIDATES = (
    ("FREQ-T005", 0.05),
    ("FREQ-T020", 0.20),
    ("FREQ-T080", 0.80),
    ("FREQ-T200", 2.00),
)


def seed32(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:4], "big") & 0x7FFFFFFF


def norm_letter(ch: str):
    s = unicodedata.normalize("NFKD", ch.lower())
    s = "".join(c for c in s if "a" <= c <= "z")
    if not s:
        return None
    c = s[0]
    if c == "j":
        c = "i"
    elif c == "v":
        c = "u"
    return c if c in AI else None


def load_latin(root: Path):
    runs = []
    files = 0
    for rel in CREMMA_DIRS:
        d = root / rel
        if not d.is_dir():
            raise RuntimeError(f"missing CREMMA directory {d}")
        for p in sorted(d.rglob("*.txt")):
            files += 1
            text = p.read_text(encoding="utf-8", errors="replace")
            # Same symmetric line-concatenated normalization frozen for E11C:
            # ignore nonletters inside a physical line, j->i, v->u.
            for raw in text.splitlines():
                chars = []
                for ch in raw:
                    c = norm_letter(ch)
                    if c is not None:
                        chars.append(c)
                if chars:
                    runs.append("".join(chars))
    if not runs:
        raise RuntimeError("no Latin runs")
    return runs, {"files": files, "runs": len(runs), "chars": sum(map(len, runs))}


class LM4:
    def __init__(self, runs):
        c3 = np.zeros(A ** 3, dtype=np.int64)
        c4 = np.zeros(A ** 4, dtype=np.int64)
        for s in runs:
            xs = [AI[c] for c in s]
            for i in range(3, len(xs)):
                h = (xs[i - 3] * A + xs[i - 2]) * A + xs[i - 1]
                q = h * A + xs[i]
                c3[h] += 1
                c4[q] += 1
        cost = np.empty(A ** 4, dtype=np.float64)
        for h in range(A ** 3):
            den = c3[h] + ALPHA * A
            base = h * A
            for c in range(A):
                cost[base + c] = -math.log2((c4[base + c] + ALPHA) / den)
        self.cost = cost

    def score_plain_runs(self, runs):
        nll = 0.0
        n = 0
        for s in runs:
            xs = [AI[c] for c in s]
            for i in range(3, len(xs)):
                q = (((xs[i - 3] * A + xs[i - 2]) * A + xs[i - 1]) * A + xs[i])
                nll += float(self.cost[q])
                n += 1
        return nll / n if n else float("inf")


def top23_plaintext(runs):
    counts = Counter("".join(runs))
    ranked = sorted(ALPHABET, key=lambda c: (-counts[c], c))
    top = tuple(ranked[:23])
    omitted = ranked[23]
    return top, omitted, counts, ranked


def build_control_plain_runs(runs, top23):
    allowed = set(top23)
    out = []
    total = 0
    for s in runs:
        cur = []
        for c in s:
            if c in allowed:
                cur.append(c)
            else:
                if cur and total < TARGET_EVENTS:
                    take = min(len(cur), TARGET_EVENTS - total)
                    if take:
                        out.append("".join(cur[:take]))
                        total += take
                cur = []
                if total >= TARGET_EVENTS:
                    break
        if total >= TARGET_EVENTS:
            break
        if cur:
            take = min(len(cur), TARGET_EVENTS - total)
            if take:
                out.append("".join(cur[:take]))
                total += take
        if total >= TARGET_EVENTS:
            break
    if total != TARGET_EVENTS:
        raise RuntimeError(f"control population short: {total} != {TARGET_EVENTS}")
    return out


def hidden_key(top23, omitted, label):
    rng = np.random.default_rng(seed32(label))
    vals = np.asarray([AI[c] for c in top23], dtype=np.int16)
    rng.shuffle(vals)
    key = np.empty(A, dtype=np.int16)
    key[:M] = vals
    key[M] = AI[omitted]
    if len(set(int(x) for x in key)) != A:
        raise RuntimeError("hidden key is not a permutation")
    return key


def encrypt_runs(plain_runs, key):
    inv = {int(key[i]): i for i in range(M)}
    seqs = []
    counts = np.zeros(M, dtype=np.int64)
    for s in plain_runs:
        xs = np.asarray([inv[AI[c]] for c in s], dtype=np.int16)
        seqs.append(xs)
        for x in xs:
            counts[int(x)] += 1
    return seqs, counts


def pattern_arrays_from_sequences(seqs):
    ctr = Counter()
    for s in seqs:
        for i in range(len(s) - 3):
            ctr[(int(s[i]), int(s[i + 1]), int(s[i + 2]), int(s[i + 3]))] += 1
    if not ctr:
        raise RuntimeError("no cipher tetragrams")
    keys = sorted(ctr)
    pats = np.asarray(keys, dtype=np.int16)
    counts = np.asarray([ctr[k] for k in keys], dtype=np.int64)
    incident = [[] for _ in range(M)]
    for pi, p in enumerate(keys):
        for g in sorted(set(p)):
            incident[g].append(pi)
    offsets = [0]
    flat = []
    for xs in incident:
        flat.extend(xs)
        offsets.append(len(flat))
    return pats, counts, np.asarray(offsets, dtype=np.int32), np.asarray(flat, dtype=np.int32)


@njit(cache=True)
def full_score(key, pats, counts, lm_cost):
    nll = 0.0
    total = 0
    for p in range(pats.shape[0]):
        a = key[pats[p, 0]]
        b = key[pats[p, 1]]
        c = key[pats[p, 2]]
        d = key[pats[p, 3]]
        q = (((a * A + b) * A + c) * A + d)
        nll += counts[p] * lm_cost[q]
        total += counts[p]
    return nll / total


@njit(cache=True)
def swap_delta(key, i, j, pats, counts, offsets, incident, lm_cost, marks, stamp, total_count):
    stamp += 1
    old_i = key[i]
    old_j = key[j]
    delta_total = 0.0
    if i < M:
        for z in range(offsets[i], offsets[i + 1]):
            pidx = incident[z]
            if marks[pidx] == stamp:
                continue
            marks[pidx] = stamp
            p0 = pats[pidx, 0]; p1 = pats[pidx, 1]; p2 = pats[pidx, 2]; p3 = pats[pidx, 3]
            o0 = key[p0]; o1 = key[p1]; o2 = key[p2]; o3 = key[p3]
            n0 = old_j if p0 == i else (old_i if p0 == j else o0)
            n1 = old_j if p1 == i else (old_i if p1 == j else o1)
            n2 = old_j if p2 == i else (old_i if p2 == j else o2)
            n3 = old_j if p3 == i else (old_i if p3 == j else o3)
            oldq = (((o0 * A + o1) * A + o2) * A + o3)
            newq = (((n0 * A + n1) * A + n2) * A + n3)
            delta_total += counts[pidx] * (lm_cost[newq] - lm_cost[oldq])
    if j < M:
        for z in range(offsets[j], offsets[j + 1]):
            pidx = incident[z]
            if marks[pidx] == stamp:
                continue
            marks[pidx] = stamp
            p0 = pats[pidx, 0]; p1 = pats[pidx, 1]; p2 = pats[pidx, 2]; p3 = pats[pidx, 3]
            o0 = key[p0]; o1 = key[p1]; o2 = key[p2]; o3 = key[p3]
            n0 = old_j if p0 == i else (old_i if p0 == j else o0)
            n1 = old_j if p1 == i else (old_i if p1 == j else o1)
            n2 = old_j if p2 == i else (old_i if p2 == j else o2)
            n3 = old_j if p3 == i else (old_i if p3 == j else o3)
            oldq = (((o0 * A + o1) * A + o2) * A + o3)
            newq = (((n0 * A + n1) * A + n2) * A + n3)
            delta_total += counts[pidx] * (lm_cost[newq] - lm_cost[oldq])
    return delta_total / total_count, stamp


@njit(cache=True)
def anneal_one(initial_key, seed, pats, counts, offsets, incident, lm_cost, t0):
    key = initial_key.copy()
    total_count = 0
    for x in counts:
        total_count += x
    marks = np.zeros(pats.shape[0], dtype=np.int32)
    stamp = 0
    np.random.seed(seed)
    current = full_score(key, pats, counts, lm_cost)
    T = t0
    ratio = math.exp(math.log(T1 / t0) / (STEPS - 1))
    for _ in range(STEPS):
        i = np.random.randint(0, A)
        j = np.random.randint(0, A - 1)
        if j >= i:
            j += 1
        d, stamp = swap_delta(key, i, j, pats, counts, offsets, incident, lm_cost, marks, stamp, total_count)
        if d <= 0.0 or np.random.random() < math.exp(-d / T):
            tmp = key[i]; key[i] = key[j]; key[j] = tmp
            current += d
        T *= ratio
    while True:
        best_d = -EPS
        best_i = -1
        best_j = -1
        for i in range(A - 1):
            for j in range(i + 1, A):
                d, stamp = swap_delta(key, i, j, pats, counts, offsets, incident, lm_cost, marks, stamp, total_count)
                if d < best_d:
                    best_d = d; best_i = i; best_j = j
        if best_i < 0:
            break
        tmp = key[best_i]; key[best_i] = key[best_j]; key[best_j] = tmp
        current += best_d
    return key, full_score(key, pats, counts, lm_cost)


def frequency_initial(symbol_counts, latin_counts, restart, seed):
    cipher_rank = sorted(range(M), key=lambda g: (-int(symbol_counts[g]), g))
    latin_rank = sorted(range(A), key=lambda x: (-int(latin_counts[ALPHABET[x]]), ALPHABET[x]))
    key = np.empty(A, dtype=np.int16)
    for g, p in zip(cipher_rank, latin_rank[:M]):
        key[g] = p
    key[M] = latin_rank[M]
    if restart > 0:
        rng = np.random.default_rng(seed)
        for _ in range(2 + (restart % 5)):
            i, j = rng.choice(A, size=2, replace=False)
            tmp = key[i]; key[i] = key[j]; key[j] = tmp
    return key


def solve_control(seqs, symbol_counts, latin_counts, lm_cost, candidate_id, t0, seed_namespace):
    pats, counts, offsets, incident = pattern_arrays_from_sequences(seqs)
    best = None
    restarts = []
    for r in range(RESTARTS):
        seed = seed32(f"{seed_namespace}:{r}")
        initial = frequency_initial(symbol_counts, latin_counts, r, seed)
        key, ce = anneal_one(initial, seed, pats, counts, offsets, incident, lm_cost, t0)
        tup = tuple(int(x) for x in key)
        restarts.append({"restart": r, "seed": seed, "cross_entropy": float(ce)})
        row = (float(ce), tup, key.copy())
        if best is None or row[:2] < best[:2]:
            best = row
    return best[2], best[0], restarts


def key_metrics(recovered, true_key, symbol_counts):
    correct = np.asarray([int(recovered[g]) == int(true_key[g]) for g in range(M)], dtype=np.float64)
    exact = float(correct.mean())
    denom = int(symbol_counts.sum())
    weighted = float(sum(int(symbol_counts[g]) * correct[g] for g in range(M)) / denom)
    return exact, weighted


def key_plain_letters(key):
    return [ALPHABET[int(key[g])] for g in range(M)]


def run_one_control(plain_runs, top23, omitted, latin_counts, lm, key_seed_label, candidate_id, t0, solve_seed_prefix):
    true_key = hidden_key(top23, omitted, key_seed_label)
    seqs, symbol_counts = encrypt_runs(plain_runs, true_key)
    recovered, ce, restart_rows = solve_control(
        seqs, symbol_counts, latin_counts, lm.cost, candidate_id, t0, solve_seed_prefix
    )
    true_ce = float(full_score(true_key, *pattern_arrays_from_sequences(seqs)[:2], lm.cost))
    exact, weighted = key_metrics(recovered, true_key, symbol_counts)
    return {
        "candidate": candidate_id,
        "recovered_cross_entropy": float(ce),
        "true_key_cross_entropy": true_ce,
        "ce_excess": float(ce - true_ce),
        "exact_key_accuracy": exact,
        "occurrence_weighted_key_accuracy": weighted,
        "true_key_letters_by_cipher_symbol": key_plain_letters(true_key),
        "recovered_key_letters_by_cipher_symbol": key_plain_letters(recovered),
        "unused_true_letter": ALPHABET[int(true_key[M])],
        "unused_recovered_letter": ALPHABET[int(recovered[M])],
        "cipher_symbol_counts": symbol_counts.tolist(),
        "restarts": restart_rows,
    }


def candidate_summary(candidate_id, rows):
    return {
        "candidate": candidate_id,
        "mean_weighted_accuracy": statistics.fmean(r["occurrence_weighted_key_accuracy"] for r in rows),
        "worst_weighted_accuracy": min(r["occurrence_weighted_key_accuracy"] for r in rows),
        "mean_exact_accuracy": statistics.fmean(r["exact_key_accuracy"] for r in rows),
        "mean_absolute_ce_excess": statistics.fmean(abs(r["ce_excess"]) for r in rows),
        "controls": rows,
    }


def choose_candidate(summaries):
    ordered = sorted(
        summaries,
        key=lambda s: (
            -s["mean_weighted_accuracy"],
            -s["worst_weighted_accuracy"],
            s["mean_absolute_ce_excess"],
            s["candidate"],
        ),
    )
    return ordered[0]["candidate"], ordered


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} CREMMA_ROOT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    runs, latin_meta = load_latin(root)
    lm = LM4(runs)
    top23, omitted, latin_counts, latin_rank = top23_plaintext(runs)
    control_plain = build_control_plain_runs(runs, top23)
    true_plain_ce = lm.score_plain_runs(control_plain)

    dev_summaries = []
    for candidate_id, t0 in CANDIDATES:
        rows = []
        for control in range(5):
            rows.append(run_one_control(
                control_plain, top23, omitted, latin_counts, lm,
                f"Issue26E11D:DEVKEY:{control}", candidate_id, t0,
                f"Issue26E11D:DEV:{control}:{candidate_id}"
            ))
        dev_summaries.append(candidate_summary(candidate_id, rows))

    selected_id, ordered = choose_candidate(dev_summaries)
    selected_t0 = dict(CANDIDATES)[selected_id]

    cert_rows = []
    for control in range(5):
        cert_rows.append(run_one_control(
            control_plain, top23, omitted, latin_counts, lm,
            f"Issue26E11D:CERTKEY:{control}", selected_id, selected_t0,
            f"Issue26E11D:CERT:{control}:{selected_id}"
        ))

    mean_weighted = statistics.fmean(r["occurrence_weighted_key_accuracy"] for r in cert_rows)
    worst_weighted = min(r["occurrence_weighted_key_accuracy"] for r in cert_rows)
    mean_rec_ce = statistics.fmean(r["recovered_cross_entropy"] for r in cert_rows)
    mean_true_ce = statistics.fmean(r["true_key_cross_entropy"] for r in cert_rows)
    max_excess = max(r["ce_excess"] for r in cert_rows)
    cert_pass = (
        mean_weighted >= 0.98
        and worst_weighted >= 0.95
        and mean_rec_ce - mean_true_ce <= 0.05
        and max_excess <= 0.10
    )

    out = {
        "experiment": "Issue26E11D synthetic-only monoalphabetic solver calibration",
        "information_firewall": "NO VOYNICH INPUT, PARSING, PLAINTEXT, OR SCORING",
        "latin_population": latin_meta,
        "alphabet": "".join(ALPHABET),
        "latin_frequency_rank": latin_rank,
        "top23_plaintext_letters": list(top23),
        "omitted_plaintext_letter": omitted,
        "control_events": sum(map(len, control_plain)),
        "control_runs": len(control_plain),
        "true_plaintext_cross_entropy": true_plain_ce,
        "candidate_family": [{"candidate": c, "T0": t} for c, t in CANDIDATES],
        "development_candidates_ranked": ordered,
        "selected_candidate": selected_id,
        "selected_T0": selected_t0,
        "certification": {
            "passed": cert_pass,
            "mean_occurrence_weighted_key_accuracy": mean_weighted,
            "worst_occurrence_weighted_key_accuracy": worst_weighted,
            "mean_recovered_cross_entropy": mean_rec_ce,
            "mean_true_key_cross_entropy": mean_true_ce,
            "mean_ce_excess": mean_rec_ce - mean_true_ce,
            "max_individual_ce_excess": max_excess,
            "controls": cert_rows,
        },
        "next_authority": "E11E may be planned only if certification.passed is true",
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
