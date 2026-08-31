#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import statistics
import sys
from pathlib import Path

import numpy as np

import issue26e_core as e
import phaseE8_philip_duration as a

VOWELS = tuple("aeiou")
CONSONANTS = tuple("bcdfgklmnpqrstz")
EXPECTED_UNIVERSE = 126126
EXPECTED_PRIMARY_MEAN = 0.19129908493223072
EXPECTED_PRIMARY_FOLDS = (
    0.16711006000869041,
    0.18571262717003223,
    0.18769991148862764,
    0.20508107071913337,
    0.21089175527466988,
)
EXPECTED_PRIMARY_SLOT = 0
EXPECTED_PRIMARY_PERM = (0, 3, 1, 2)
EXPECTED_MAX_MEAN = 0.2140154356929563
EXPECTED_MAX_FOLDS = (
    0.20759348701131514,
    0.22242910323390772,
    0.21736143504764938,
    0.22530398613104008,
    0.19738916704086928,
)
EXPECTED_MAX_SLOT = 6
EXPECTED_MAX_PERM = (0, 3, 2, 1)
EPS = 1e-12


def enumerate_vowel_fixed_partitions():
    parts = []
    cons = tuple(CONSONANTS)
    cons_set = set(cons)
    for g1 in itertools.combinations(cons, 5):
        rem1 = tuple(c for c in cons if c not in set(g1))
        for g2 in itertools.combinations(rem1, 5):
            g3 = tuple(c for c in rem1 if c not in set(g2))
            groups = tuple(sorted((tuple(g1), tuple(g2), tuple(g3))))
            if tuple(g1) != groups[0] or tuple(g2) != groups[1] or tuple(g3) != groups[2]:
                continue
            flat = set().union(*map(set, groups))
            if flat != cons_set:
                raise RuntimeError("partition coverage failure")
            parts.append((VOWELS,) + groups)
    if len(parts) != EXPECTED_UNIVERSE or len(set(parts)) != EXPECTED_UNIVERSE:
        raise RuntimeError(f"unexpected exhaustive universe size: {len(parts)}")
    return parts


def assignment_matrix(parts):
    out = np.empty((len(parts), len(a.ALPHABET)), dtype=np.int8)
    for i, groups in enumerate(parts):
        for gi, group in enumerate(groups):
            for c in group:
                out[i, a.ALPHABET_INDEX[c]] = gi
    return out


def latin_population_arrays(latin_base, assign):
    n = len(assign)
    rows = np.arange(n)
    c1 = np.zeros((n, 4), dtype=np.float64)
    c2 = np.zeros((n, 16), dtype=np.float64)

    for li in range(20):
        c1[rows, assign[:, li]] += float(latin_base["c1"][li])

    for li in range(20):
        for lj in range(20):
            count = int(latin_base["c2"][li, lj])
            if count == 0:
                continue
            pair = assign[:, li].astype(np.int16) * 4 + assign[:, lj].astype(np.int16)
            c2[rows, pair] += float(count)

    c1 /= c1.sum(axis=1, keepdims=True)
    c2 /= c2.sum(axis=1, keepdims=True)
    return c1, c2


def jsd_rows(p, q):
    q = np.asarray(q, dtype=np.float64).reshape(-1)
    p = np.asarray(p, dtype=np.float64)
    m = 0.5 * (p + q[None, :])

    safe_p = np.where(p > 0, p, 1.0)
    safe_m_for_p = np.where(p > 0, m, 1.0)
    term_p = np.where(p > 0, p * (np.log2(safe_p) - np.log2(safe_m_for_p)), 0.0).sum(axis=1)

    qmask = q > 0
    term_q = (
        q[qmask][None, :]
        * (np.log2(q[qmask])[None, :] - np.log2(m[:, qmask]))
    ).sum(axis=1)
    return 0.5 * (term_p + term_q)


def dist_rows(l1, l2, v1, v2):
    return jsd_rows(l1, np.asarray(v1).reshape(-1)) + jsd_rows(l2, np.asarray(v2).reshape(-1))


def sorted_keys():
    return [(slot, perm) for slot in sorted(a.CANDIDATE_SLOTS) for perm in itertools.permutations(range(4))]


def vectorized_policy(fold_stats, l1, l2):
    keys = sorted_keys()
    n = len(l1)
    held = np.empty((5, n), dtype=np.float64)
    key_ids = np.empty((5, n), dtype=np.int16)

    for f, fs in enumerate(fold_stats):
        best_train = np.full(n, np.inf, dtype=np.float64)
        best_held = np.full(n, np.inf, dtype=np.float64)
        best_key = np.full(n, -1, dtype=np.int16)

        for ki, (slot, perm) in enumerate(keys):
            tr1, tr2 = a.permute_stats(fs["train"][slot], perm)
            te1, te2 = a.permute_stats(fs["held"][slot], perm)
            dtr = dist_rows(l1, l2, tr1, tr2)
            mask = dtr < best_train
            if np.any(mask):
                dte = dist_rows(l1[mask], l2[mask], te1, te2)
                best_train[mask] = dtr[mask]
                best_held[mask] = dte
                best_key[mask] = ki

        if np.any(best_key < 0):
            raise RuntimeError(f"fold {f}: key selection failed")
        held[f] = best_held
        key_ids[f] = best_key

    return held, key_ids, keys


def scalar_target_replay(fold_stats, latin_base):
    rows = a.evaluate_partition(fold_stats, latin_base, a.PHILIP_GROUPS)
    return rows


def assert_replay(rows, expected_mean, expected_folds, slot, perm, label):
    vals = tuple(r["held_distance"] for r in rows)
    checks = {
        "mean": abs(statistics.fmean(vals) - expected_mean) <= 1e-12,
        "folds": all(abs(x - y) <= 1e-12 for x, y in zip(vals, expected_folds)),
        "slot": all(r["slot"] == slot for r in rows),
        "perm": all(tuple(r["perm"]) == tuple(perm) for r in rows),
    }
    if not all(checks.values()):
        raise RuntimeError(f"{label} E8-A replay failure: {checks} rows={rows}")
    return checks


def summarize(policy, parts, target_index, held, key_ids, keys, scalar_rows, replay):
    means = held.mean(axis=0)
    target_mean = float(means[target_index])
    scalar_mean = statistics.fmean(r["held_distance"] for r in scalar_rows)
    if abs(target_mean - scalar_mean) > 1e-12:
        raise RuntimeError(f"{policy}: vector/scalar target mismatch {target_mean} vs {scalar_mean}")

    better_strict = int(np.sum(means < target_mean - EPS))
    ties_or_better = int(np.sum(means <= target_mean + EPS))
    rank = 1 + better_strict
    p_cond = ties_or_better / EXPECTED_UNIVERSE
    universe_median = float(np.quantile(means, .5, method="linear"))
    q05 = float(np.quantile(means, .05, method="linear"))
    q01 = float(np.quantile(means, .01, method="linear"))
    minimum = float(means.min())
    fold_medians = np.quantile(held, .5, axis=1, method="linear")
    fold_wins = sum(held[f, target_index] < fold_medians[f] - EPS for f in range(5))

    order = np.argsort(means, kind="stable")
    best_non_target = []
    for idx in order:
        if int(idx) == target_index:
            continue
        best_non_target.append({
            "partition": ["".join(g) for g in parts[int(idx)]],
            "mean_heldout_distance": float(means[int(idx)]),
            "fold_distances": [float(x) for x in held[:, int(idx)]],
            "selected_keys": [
                {"slot": keys[int(key_ids[f, int(idx)])][0],
                 "perm": list(keys[int(key_ids[f, int(idx)])][1])}
                for f in range(5)
            ],
        })
        if len(best_non_target) == 5:
            break

    target_keys = [
        {"slot": keys[int(key_ids[f, target_index])][0],
         "perm": list(keys[int(key_ids[f, target_index])][1])}
        for f in range(5)
    ]

    conditions = {
        "replay": all(replay.values()),
        "p_cond_le_0_05": p_cond <= .05,
        "below_universe_median": target_mean < universe_median - EPS,
        "fold_median_wins_ge_4": fold_wins >= 4,
    }

    if not conditions["replay"]:
        classification = "REPLAY FAILURE / NO CLASSIFICATION"
    elif p_cond > .05:
        classification = "VOWEL ISOLATION EXPLAINS E8A NEAR-HIT"
    elif conditions["below_universe_median"] and conditions["fold_median_wins_ge_4"]:
        classification = "PHILIP CONSONANT SUBDIVISION SURVIVES VOWEL-FIXED CONTROL"
    else:
        classification = "MIXED VOWEL-FIXED SPECIFICITY"

    return {
        "policy": policy,
        "classification": classification,
        "universe_size": EXPECTED_UNIVERSE,
        "target_index": target_index,
        "target_mean_distance": target_mean,
        "rank_strict": rank,
        "ties_or_better": ties_or_better,
        "p_cond": p_cond,
        "universe_median": universe_median,
        "universe_q05": q05,
        "universe_q01": q01,
        "universe_min": minimum,
        "fold_median_wins": fold_wins,
        "target_fold_distances": [float(x) for x in held[:, target_index]],
        "fold_universe_medians": [float(x) for x in fold_medians],
        "target_keys_vectorized": target_keys,
        "target_rows_scalar_replay": scalar_rows,
        "replay_checks": replay,
        "conditions": conditions,
        "best_five_non_philip": best_non_target,
    }


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr)
        return 2

    zl = Path(sys.argv[1]).resolve()
    latin_root = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")

    parser = e.SlotParser()
    validation = e.validate_parser(parser)
    items = e.parse_voynich(zl)
    latin_base, latin_meta = a.latin_letter_counts(latin_root)

    parts = enumerate_vowel_fixed_partitions()
    target = (VOWELS, tuple("bcdfg"), tuple("klmnp"), tuple("qrstz"))
    try:
        target_index = parts.index(target)
    except ValueError as exc:
        raise RuntimeError("Philip target absent from exhaustive universe") from exc

    assign = assignment_matrix(parts)
    l1, l2 = latin_population_arrays(latin_base, assign)

    min_folds = a.build_fold_stats(items, parser, "min")
    min_scalar = scalar_target_replay(min_folds, latin_base)
    min_replay = assert_replay(
        min_scalar, EXPECTED_PRIMARY_MEAN, EXPECTED_PRIMARY_FOLDS,
        EXPECTED_PRIMARY_SLOT, EXPECTED_PRIMARY_PERM, "min"
    )
    min_held, min_keys, key_catalog = vectorized_policy(min_folds, l1, l2)
    primary = summarize("min", parts, target_index, min_held, min_keys, key_catalog, min_scalar, min_replay)

    max_folds = a.build_fold_stats(items, parser, "max")
    max_scalar = scalar_target_replay(max_folds, latin_base)
    max_replay = assert_replay(
        max_scalar, EXPECTED_MAX_MEAN, EXPECTED_MAX_FOLDS,
        EXPECTED_MAX_SLOT, EXPECTED_MAX_PERM, "max"
    )
    max_held, max_keys, max_key_catalog = vectorized_policy(max_folds, l1, l2)
    sensitivity = summarize("max", parts, target_index, max_held, max_keys, max_key_catalog, max_scalar, max_replay)

    here = Path(__file__).resolve().parent
    out = {
        "experiment": "Issue26E8-A2 exhaustive vowel-fixed Philip control",
        "issue": 26,
        "parent_E8A_classification": "PHILIP DURATION-GROUP NOT SUPPORTED",
        "inputs": {
            "zl_blob_sha1": e.EXPECTED_ZL3B_BLOB,
            "cremma_commit": a.EXPECTED_CREMMA_COMMIT,
            "plan_sha256": a.sha256_file(here / "PLAN_E8A2.md"),
            "script_sha256": a.sha256_file(Path(__file__)),
            "parent_script_sha256": a.sha256_file(here / "phaseE8_philip_duration.py"),
            "core_sha256": a.sha256_file(here / "issue26e_core.py"),
        },
        "latin_population": latin_meta,
        "fixed_vowel_group": "aeiou",
        "target_partition": ["aeiou", "bcdfg", "klmnp", "qrstz"],
        "slot_parser_validation": validation,
        "primary_min": primary,
        "max_sensitivity": sensitivity,
        "frozen_primary_classification": primary["classification"],
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
