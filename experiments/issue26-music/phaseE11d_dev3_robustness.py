#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from numba import njit

import phaseE11d_dev2_runner as r

# Importing DEV2 runner patches the shared E11 module to the exact 24-letter alphabet.
d = r.d
base = d.base
ALPHABET = d.ALPHABET
AI = d.AI
A = 24
M = 23
TARGET = 40_000
STEPS = 60_000
T1 = 0.00005
EPS = 1e-12
UNUSED = ("q", "x", "z", "y", "k", "w")
CANDIDATE_ORDER = ("FREQ-HILL", "T001", "T005", "T020")
assert len(ALPHABET) == A


def build_case_runs(latin_runs, omitted):
    allowed = set(ALPHABET) - {omitted}
    out = []
    total = 0
    for s in latin_runs:
        cur = []
        for ch in s:
            if ch in allowed:
                cur.append(ch)
            else:
                if cur:
                    take = min(len(cur), TARGET - total)
                    if take:
                        out.append("".join(cur[:take]))
                        total += take
                    cur = []
                if total >= TARGET:
                    break
        if total >= TARGET:
            break
        if cur:
            take = min(len(cur), TARGET - total)
            if take:
                out.append("".join(cur[:take]))
                total += take
        if total >= TARGET:
            break
    if total != TARGET:
        raise RuntimeError(f"DEV3 population short for omitted={omitted}: {total} != {TARGET}")
    return out


def hidden_key(omitted):
    allowed = [AI[c] for c in ALPHABET if c != omitted]
    rng = np.random.default_rng(base.seed32(f"Issue26E11D:Dev3Key:v1:{omitted}"))
    vals = np.asarray(allowed, dtype=np.int16)
    rng.shuffle(vals)
    key = np.empty(A, dtype=np.int16)
    key[:M] = vals
    key[M] = AI[omitted]
    return key


def encrypt(plain_runs, key):
    inv = {int(key[g]): g for g in range(M)}
    seqs = []
    symbol_counts = np.zeros(M, dtype=np.int64)
    for s in plain_runs:
        xs = np.asarray([inv[AI[ch]] for ch in s], dtype=np.int16)
        seqs.append(xs)
        for x in xs:
            symbol_counts[int(x)] += 1
    return seqs, symbol_counts


def frequency_seed(symbol_counts, latin_freq):
    cipher_rank = sorted(range(M), key=lambda g: (-int(symbol_counts[g]), g))
    plain_rank = sorted(range(A), key=lambda p: (-int(latin_freq[ALPHABET[p]]), ALPHABET[p]))
    key = np.empty(A, dtype=np.int16)
    for g, p in zip(cipher_rank, plain_rank[:M]):
        key[g] = p
    key[M] = plain_rank[M]
    return key


@njit(cache=False)
def full24(key, pats, counts, lm_cost):
    nll = 0.0
    total = 0
    for p in range(pats.shape[0]):
        a = int(key[pats[p, 0]])
        b = int(key[pats[p, 1]])
        c = int(key[pats[p, 2]])
        e = int(key[pats[p, 3]])
        q = (((a * 24 + b) * 24 + c) * 24 + e)
        nll += counts[p] * lm_cost[q]
        total += counts[p]
    return nll / total


@njit(cache=False)
def delta24(key, i, j, pats, counts, offsets, incident, lm_cost, marks, stamp, total_count):
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
            p0=pats[pidx,0]; p1=pats[pidx,1]; p2=pats[pidx,2]; p3=pats[pidx,3]
            o0=key[p0]; o1=key[p1]; o2=key[p2]; o3=key[p3]
            n0=old_j if p0==i else (old_i if p0==j else o0)
            n1=old_j if p1==i else (old_i if p1==j else o1)
            n2=old_j if p2==i else (old_i if p2==j else o2)
            n3=old_j if p3==i else (old_i if p3==j else o3)
            oq=(((o0*24+o1)*24+o2)*24+o3)
            nq=(((n0*24+n1)*24+n2)*24+n3)
            delta_total += counts[pidx] * (lm_cost[nq] - lm_cost[oq])
    if j < M:
        for z in range(offsets[j], offsets[j + 1]):
            pidx = incident[z]
            if marks[pidx] == stamp:
                continue
            marks[pidx] = stamp
            p0=pats[pidx,0]; p1=pats[pidx,1]; p2=pats[pidx,2]; p3=pats[pidx,3]
            o0=key[p0]; o1=key[p1]; o2=key[p2]; o3=key[p3]
            n0=old_j if p0==i else (old_i if p0==j else o0)
            n1=old_j if p1==i else (old_i if p1==j else o1)
            n2=old_j if p2==i else (old_i if p2==j else o2)
            n3=old_j if p3==i else (old_i if p3==j else o3)
            oq=(((o0*24+o1)*24+o2)*24+o3)
            nq=(((n0*24+n1)*24+n2)*24+n3)
            delta_total += counts[pidx] * (lm_cost[nq] - lm_cost[oq])
    return delta_total / total_count, stamp


@njit(cache=False)
def steepest24(initial, pats, counts, offsets, incident, lm_cost):
    key = initial.copy()
    total_count = 0
    for x in counts:
        total_count += x
    marks = np.zeros(pats.shape[0], dtype=np.int32)
    stamp = 0
    current = full24(key, pats, counts, lm_cost)
    accepted = 0
    while accepted < 100:
        best_d = -EPS
        best_i = -1
        best_j = -1
        for i in range(A - 1):
            for j in range(i + 1, A):
                dd, stamp = delta24(key, i, j, pats, counts, offsets, incident, lm_cost, marks, stamp, total_count)
                if dd < best_d:
                    best_d = dd
                    best_i = i
                    best_j = j
        if best_i < 0:
            break
        tmp = key[best_i]; key[best_i] = key[best_j]; key[best_j] = tmp
        current += best_d
        accepted += 1
    return key, full24(key, pats, counts, lm_cost), accepted


@njit(cache=False)
def anneal24(initial, seed, t0, pats, counts, offsets, incident, lm_cost):
    key = initial.copy()
    total_count = 0
    for x in counts:
        total_count += x
    marks = np.zeros(pats.shape[0], dtype=np.int32)
    stamp = 0
    np.random.seed(seed)
    current = full24(key, pats, counts, lm_cost)
    temp = t0
    ratio = math.exp(math.log(T1 / t0) / (STEPS - 1))
    for _ in range(STEPS):
        i = np.random.randint(0, A)
        j = np.random.randint(0, A - 1)
        if j >= i:
            j += 1
        dd, stamp = delta24(key, i, j, pats, counts, offsets, incident, lm_cost, marks, stamp, total_count)
        if dd <= 0.0 or np.random.random() < math.exp(-dd / temp):
            tmp = key[i]; key[i] = key[j]; key[j] = tmp
            current += dd
        temp *= ratio
    # Exact same deterministic steepest finalizer.
    while True:
        best_d = -EPS
        best_i = -1
        best_j = -1
        for i in range(A - 1):
            for j in range(i + 1, A):
                dd, stamp = delta24(key, i, j, pats, counts, offsets, incident, lm_cost, marks, stamp, total_count)
                if dd < best_d:
                    best_d = dd
                    best_i = i
                    best_j = j
        if best_i < 0:
            break
        tmp = key[best_i]; key[best_i] = key[best_j]; key[best_j] = tmp
        current += best_d
    return key, full24(key, pats, counts, lm_cost)


def perturb(seed_key, candidate, omitted, start):
    key = seed_key.copy()
    if start == 0:
        return key
    rng = np.random.default_rng(base.seed32(f"Issue26E11D:Dev3:{candidate}:{omitted}:{start}:init"))
    for _ in range(start):
        i, j = (int(x) for x in rng.choice(A, size=2, replace=False))
        key[i], key[j] = key[j], key[i]
    return key


def metrics(key, true_key, symbol_counts):
    exact = sum(int(key[g]) == int(true_key[g]) for g in range(M)) / M
    denom = int(symbol_counts.sum())
    weighted = sum(int(symbol_counts[g]) for g in range(M) if int(key[g]) == int(true_key[g])) / denom
    return float(exact), float(weighted)


def result_row(candidate, key, solver_ce, true_key, true_ce, symbol_counts, pats, counts, lm_cost, extra=None):
    direct = float(full24(key, pats, counts, lm_cost))
    shared = float(base.full_score(key, pats, counts, lm_cost))
    exact, weighted = metrics(key, true_key, symbol_counts)
    out = {
        "candidate": candidate,
        "direct_ce": direct,
        "solver_ce": float(solver_ce),
        "shared_full_score_ce": shared,
        "max_score_discrepancy": max(abs(direct - float(solver_ce)), abs(direct - shared)),
        "true_ce": float(true_ce),
        "ce_excess": direct - float(true_ce),
        "exact_key_accuracy": exact,
        "occurrence_weighted_key_accuracy": weighted,
        "key": [ALPHABET[int(x)] for x in key],
    }
    if extra:
        out.update(extra)
    return out


def run_case(omitted, latin_runs, latin_freq, lm_cost):
    plain_runs = build_case_runs(latin_runs, omitted)
    true_key = hidden_key(omitted)
    seqs, symbol_counts = encrypt(plain_runs, true_key)
    pats, counts, offsets, incident = base.pattern_arrays_from_sequences(seqs, M)
    true_ce = float(full24(true_key, pats, counts, lm_cost))
    fseed = frequency_seed(symbol_counts, latin_freq)

    rows = []
    hkey, hce, accepted = steepest24(fseed, pats, counts, offsets, incident, lm_cost)
    rows.append(result_row("FREQ-HILL", hkey, hce, true_key, true_ce, symbol_counts, pats, counts, lm_cost,
                           {"accepted_swaps": int(accepted)}))

    for candidate, t0 in (("T020", .020), ("T005", .005), ("T001", .001)):
        best = None
        restart_rows = []
        for start in range(4):
            init = perturb(fseed, candidate, omitted, start)
            seed = base.seed32(f"Issue26E11D:Dev3:{candidate}:{omitted}:{start}:anneal")
            key, ce = anneal24(init, seed, t0, pats, counts, offsets, incident, lm_cost)
            kt = tuple(int(x) for x in key)
            restart_rows.append({"start": start, "seed": int(seed), "ce": float(ce)})
            cand = (float(ce), kt, key.copy())
            if best is None or cand[:2] < best[:2]:
                best = cand
        rows.append(result_row(candidate, best[2], best[0], true_key, true_ce, symbol_counts, pats, counts, lm_cost,
                               {"T0": t0, "starts": restart_rows}))

    return {
        "omitted": omitted,
        "events": int(symbol_counts.sum()),
        "runs": len(plain_runs),
        "true_ce": true_ce,
        "frequency_seed": [ALPHABET[int(x)] for x in fseed],
        "true_key": [ALPHABET[int(x)] for x in true_key],
        "candidates": rows,
    }


def aggregate(cases):
    out = {}
    for candidate in ("FREQ-HILL", "T020", "T005", "T001"):
        rows = [next(x for x in c["candidates"] if x["candidate"] == candidate) for c in cases]
        out[candidate] = {
            "mean_weighted_accuracy": statistics.fmean(x["occurrence_weighted_key_accuracy"] for x in rows),
            "worst_weighted_accuracy": min(x["occurrence_weighted_key_accuracy"] for x in rows),
            "cases_weighted_ge_0_95": sum(x["occurrence_weighted_key_accuracy"] >= .95 for x in rows),
            "mean_ce_excess": statistics.fmean(x["ce_excess"] for x in rows),
            "worst_ce_excess": max(x["ce_excess"] for x in rows),
            "exact_keys": sum(x["exact_key_accuracy"] == 1.0 for x in rows),
            "max_score_discrepancy": max(x["max_score_discrepancy"] for x in rows),
            "development_robust": all(x["occurrence_weighted_key_accuracy"] >= .95 and x["ce_excess"] <= .05 for x in rows),
        }
    robust = [c for c in CANDIDATE_ORDER if out[c]["development_robust"]]
    out["preferred_robust_candidate"] = robust[0] if robust else None
    return out


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} CREMMA_ROOT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    latin_runs, _, latin_meta = base.load_latin(root)
    latin_freq = Counter("".join(latin_runs))
    lm = base.LM4(latin_runs)
    cases = [run_case(o, latin_runs, latin_freq, lm.cost) for o in UNUSED]
    agg = aggregate(cases)
    result = {
        "experiment": "Issue26E11D DEV3 Voynich-blind robustness battery",
        "status": "DEVELOPMENT ONLY — LOCKED VALIDATION NOT OPENED — NO VOYNICH INPUT",
        "latin_population": latin_meta,
        "target_events_per_case": TARGET,
        "unused_letters": list(UNUSED),
        "cases": cases,
        "aggregate": agg,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
