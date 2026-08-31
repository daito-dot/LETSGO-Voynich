#!/usr/bin/env python3
"""Generate Issue26E3 structural null catalogs without reading Voynich data.

This provenance helper is not used by the scientific workflow. The generated
compact catalogs are committed/frozen before the E3 scorer.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import random
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

COLS = tuple(range(6))
SUBS = tuple(s for k in (1, 2, 3) for s in itertools.combinations(COLS, k))
PAIRS = tuple(itertools.combinations(COLS, 2))
TRIPLES = tuple(itertools.combinations(COLS, 3))
OVERLAPS = [0] * 5 + [2] * 5 + [3] * 2 + [4] * 3
SEED_LABEL = "Issue26E3:pair-histogram-catalog:v1"
G_ROWS = [
    (0,), (1,), (2,), (0, 3), (1, 4), (2, 5), (0, 3), (0, 1, 4),
    (1, 2, 5), (2, 3), (0, 3, 4), (1, 4, 5), (2, 5), (0, 3),
    (0, 1, 4), (1, 2, 5), (2, 3), (3, 4), (4, 5), (5,),
]


def masks(rows):
    return sorted(sum(1 << c for c in row) for row in rows)


def matrix(rows):
    out = np.zeros((20, 6), dtype=int)
    for r, ss in enumerate(rows):
        out[r, list(ss)] = 1
    return out


def pair_vector(M):
    Q = M.T @ M
    return tuple(int(Q[a, b]) for a, b in PAIRS)


def counts(rows):
    c = collections.Counter(tuple(sorted(x)) for x in rows)
    return tuple(c[s] for s in SUBS)


def write_compact(path, obj):
    Path(path).write_text(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")


def generate_structured(n=100):
    G = matrix(G_ROWS)
    g_count = counts(G_ROWS)
    g_pair = pair_vector(G)
    base_A, base_b = [], []
    for k, count in ((1, 4), (2, 10), (3, 6)):
        base_A.append([int(len(s) == k) for s in SUBS]); base_b.append(count)
    for c in COLS:
        base_A.append([int(c in s) for s in SUBS]); base_b.append(7)
    bounds = Bounds(np.zeros(len(SUBS)), np.full(len(SUBS), 20.0))
    integrality = np.ones(len(SUBS))
    objective = np.array([1.0 + (i + 1) / 1000.0 for i in range(len(SUBS))])
    seed = int.from_bytes(hashlib.sha256(SEED_LABEL.encode()).digest()[:8], "big")
    rng = random.Random(seed)
    seen, catalog, attempts = set(), [], 0
    while len(catalog) < n:
        attempts += 1
        if attempts > 100000:
            raise RuntimeError("catalog generation exhausted")
        vals = OVERLAPS.copy(); rng.shuffle(vals); pv = tuple(vals)
        if pv == g_pair:
            continue
        A, b = list(base_A), list(base_b)
        for (a, c), z in zip(PAIRS, pv):
            A.append([int(a in s and c in s) for s in SUBS]); b.append(z)
        constraint = LinearConstraint(np.array(A, float), np.array(b, float), np.array(b, float))
        result = milp(objective, integrality=integrality, bounds=bounds,
                      constraints=constraint, options={"time_limit": 2})
        if not result.success:
            continue
        cnt = tuple(int(round(x)) for x in result.x)
        if cnt == g_count or cnt in seen:
            continue
        rows = []
        for s, k in zip(SUBS, cnt):
            rows.extend([s] * k)
        M = matrix(rows)
        if sorted(M.sum(1).tolist()) != [1] * 4 + [2] * 10 + [3] * 6:
            raise RuntimeError("row degree validation")
        if M.sum(0).tolist() != [7] * 6 or sorted(pair_vector(M)) != sorted(g_pair):
            raise RuntimeError("overlap validation")
        seen.add(cnt); catalog.append(masks(rows))
    return {
        "attempts_used": attempts,
        "column_degrees": [7] * 6,
        "row_degree_multiset": {"1": 4, "2": 10, "3": 6},
        "row_masks": catalog,
        "seed_label": SEED_LABEL,
        "target_pair_overlap_histogram": {"0": 5, "2": 5, "3": 2, "4": 3},
        "version": 1,
    }


def weak_compositions(n, k):
    for bars in itertools.combinations(range(n + k - 1), k - 1):
        prev, out = -1, []
        for bar in bars + (n + k - 1,):
            out.append(bar - prev - 1); prev = bar
        yield out


def generate_exact():
    G = matrix(G_ROWS); P = {(a, b): int((G[:, a] & G[:, b]).sum()) for a, b in PAIRS}
    gmask = masks(G_ROWS); solutions = []
    for zvals in weak_compositions(6, len(TRIPLES)):
        z = dict(zip(TRIPLES, zvals)); y = {}; ok = True
        for a, b in PAIRS:
            value = P[(a, b)] - sum(z[t] for t in TRIPLES if a in t and b in t)
            if value < 0: ok = False; break
            y[(a, b)] = value
        if not ok or sum(y.values()) != 10:
            continue
        x = {}
        for c in COLS:
            value = 7 - sum(v for s, v in y.items() if c in s) - sum(v for s, v in z.items() if c in s)
            if value < 0: ok = False; break
            x[c] = value
        if not ok or sum(x.values()) != 4:
            continue
        rows = []
        for c, k in x.items(): rows += [(c,)] * k
        for s, k in y.items(): rows += [s] * k
        for s, k in z.items(): rows += [s] * k
        rm = masks(rows)
        solutions.append({"is_guidonian": rm == gmask, "row_masks": rm})
    return {
        "complete_enumeration": True,
        "guidonian_pair_overlap_matrix": (G.T @ G).astype(int).tolist(),
        "method": "enumerate all weak compositions of six degree-3 rows across C(6,3)=20 triples; pair counts determine degree-2 rows and column degrees determine degree-1 rows",
        "solutions": solutions,
        "version": 1,
    }


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("structured"); ap.add_argument("exact")
    args = ap.parse_args()
    write_compact(args.structured, generate_structured())
    write_compact(args.exact, generate_exact())

if __name__ == "__main__":
    main()
