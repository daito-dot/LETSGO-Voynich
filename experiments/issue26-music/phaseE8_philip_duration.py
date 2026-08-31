#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import random
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np
import issue26e_core as e

EXPECTED_CREMMA_COMMIT = "292525969ad98380b398e6606a9c2a36d51913ae"
MANUSCRIPT_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
CANDIDATE_SLOTS = {
    0: ("", "q", "s", "d"),
    6: ("", "e", "ee", "eee"),
    9: ("", "i", "ii", "iii"),
}
PHILIP_GROUPS = (
    tuple("aeiou"),
    tuple("bcdfg"),
    tuple("klmnp"),
    tuple("qrstz"),
)
ALPHABET = tuple(sorted({c for g in PHILIP_GROUPS for c in g}))
ALPHABET_INDEX = {c: i for i, c in enumerate(ALPHABET)}
NULL_N = 1000
EPS = 1e-12


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_seed(text: str) -> int:
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")


def canonical_partition(groups):
    return tuple(sorted(tuple(sorted(g)) for g in groups))


def target_canonical():
    return canonical_partition(PHILIP_GROUPS)


def make_null_partitions(n=NULL_N):
    seen = {target_canonical()}
    out = []
    for j in range(n):
        attempt = 0
        while True:
            chars = list(ALPHABET)
            rng = random.Random(stable_seed(f"Issue26E8:PhilipPartitionNull:v1:{j}:{attempt}"))
            rng.shuffle(chars)
            key = canonical_partition([chars[k:k + 5] for k in range(0, 20, 5)])
            if key not in seen:
                seen.add(key)
                out.append(key)
                break
            attempt += 1
    if len(out) != n or len(set(out)) != n:
        raise RuntimeError("null partition generation failed")
    return out


def normalize_latin_char(ch: str):
    folded = unicodedata.normalize("NFKD", ch.lower())
    base = "".join(c for c in folded if "a" <= c <= "z")
    if not base:
        return None
    c = base[0]
    if c == "j":
        c = "i"
    elif c == "v":
        c = "u"
    return c


def latin_letter_counts(root: Path):
    c1 = np.zeros(20, dtype=np.int64)
    c2 = np.zeros((20, 20), dtype=np.int64)
    file_count = line_count = retained_runs = retained_letters = retained_pairs = 0

    def add_run(run):
        nonlocal retained_runs, retained_letters, retained_pairs
        if len(run) < 5:
            return
        retained_runs += 1
        retained_letters += len(run)
        retained_pairs += len(run) - 1
        for x in run:
            c1[x] += 1
        for a, b in zip(run, run[1:]):
            c2[a, b] += 1

    for rel in MANUSCRIPT_DIRS:
        d = root / rel
        if not d.is_dir():
            raise RuntimeError(f"missing CREMMA directory: {d}")
        for path in sorted(d.rglob("*.txt")):
            file_count += 1
            for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
                line_count += 1
                cur = []
                for ch in raw:
                    if not unicodedata.category(ch).startswith(("L", "M")):
                        continue
                    c = normalize_latin_char(ch)
                    if c is None:
                        continue
                    if c in ALPHABET_INDEX:
                        cur.append(ALPHABET_INDEX[c])
                    else:
                        add_run(cur)
                        cur = []
                add_run(cur)

    if retained_runs == 0:
        raise RuntimeError("no Latin runs")
    meta = {
        "files": file_count,
        "physical_lines": line_count,
        "retained_runs": retained_runs,
        "retained_letters": retained_letters,
        "retained_pairs": retained_pairs,
    }
    return {"c1": c1, "c2": c2}, meta


def partition_assignment(groups):
    assign = np.full(len(ALPHABET), -1, dtype=int)
    for gi, group in enumerate(groups):
        for c in group:
            assign[ALPHABET_INDEX[c]] = gi
    if (assign < 0).any():
        raise RuntimeError("incomplete partition")
    return assign


def normalize_counts(x):
    a = np.asarray(x, dtype=float)
    s = float(a.sum())
    if s <= 0:
        raise RuntimeError("zero count population")
    return a / s


def latin_stats(base, groups):
    assign = partition_assignment(groups)
    c1 = np.zeros(4, dtype=np.int64)
    c2 = np.zeros((4, 4), dtype=np.int64)
    for a in range(20):
        ga = int(assign[a])
        c1[ga] += int(base["c1"][a])
        for b in range(20):
            c2[ga, int(assign[b])] += int(base["c2"][a, b])
    return normalize_counts(c1), normalize_counts(c2)


def jsd(p, q):
    p = np.asarray(p, dtype=float).reshape(-1)
    q = np.asarray(q, dtype=float).reshape(-1)
    m = 0.5 * (p + q)

    def kl(a, b):
        mask = a > 0
        return float(np.sum(a[mask] * np.log2(a[mask] / b[mask])))

    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def distance(v1, v2, l1, l2):
    return jsd(v1, l1) + jsd(v2, l2)


def voynich_counts(items, leaves, parser, policy, slot):
    states = CANDIDATE_SLOTS[slot]
    si = {s: i for i, s in enumerate(states)}
    c1 = np.zeros(4, dtype=np.int64)
    c2 = np.zeros((4, 4), dtype=np.int64)
    runs = 0

    def add_run(run):
        nonlocal runs
        if len(run) < 5:
            return
        runs += 1
        for x in run:
            c1[x] += 1
        for a, b in zip(run, run[1:]):
            c2[a, b] += 1

    for it in items:
        if it["leaf"] not in leaves:
            continue
        for line in it["lines"]:
            cur = []
            for tok in line:
                p = parser.pick(tok, policy)
                if p is None:
                    add_run(cur)
                    cur = []
                    continue
                val = p[1][slot]
                if val not in si:
                    raise RuntimeError(f"unexpected slot{slot} value {val!r}")
                cur.append(si[val])
            add_run(cur)

    return {
        "c1": c1,
        "c2": c2,
        "runs": runs,
        "events": int(c1.sum()),
        "pairs": int(c2.sum()),
        "state_counts": c1.tolist(),
    }


def permute_stats(raw, perm):
    c1 = np.zeros(4, dtype=np.int64)
    c2 = np.zeros((4, 4), dtype=np.int64)
    for a in range(4):
        c1[perm[a]] += int(raw["c1"][a])
        for b in range(4):
            c2[perm[a], perm[b]] += int(raw["c2"][a, b])
    return normalize_counts(c1), normalize_counts(c2)


def select_key(train_by_slot, l1, l2):
    best = None
    for slot in sorted(CANDIDATE_SLOTS):
        raw = train_by_slot[slot]
        if min(raw["state_counts"]) <= 0:
            continue
        for perm in itertools.permutations(range(4)):
            v1, v2 = permute_stats(raw, perm)
            key = (float(distance(v1, v2, l1, l2)), slot, tuple(perm))
            if best is None or key < best:
                best = key
    if best is None:
        raise RuntimeError("no admissible training key")
    return {"train_distance": best[0], "slot": best[1], "perm": best[2]}


def score_key(held_by_slot, key, l1, l2):
    raw = held_by_slot[key["slot"]]
    v1, v2 = permute_stats(raw, key["perm"])
    return distance(v1, v2, l1, l2), raw


def build_fold_stats(items, parser, policy):
    folds = e.physical_leaf_folds(items)
    if len(folds) != 5:
        raise RuntimeError(f"expected five folds, got {len(folds)}")
    universe = set().union(*folds)
    out = []
    for f, held in enumerate(folds):
        train = universe - held
        out.append({
            "fold": f,
            "held_leaves": sorted(held),
            "train": {slot: voynich_counts(items, train, parser, policy, slot) for slot in CANDIDATE_SLOTS},
            "held": {slot: voynich_counts(items, held, parser, policy, slot) for slot in CANDIDATE_SLOTS},
        })
    return out


def evaluate_partition(fold_stats, latin_base, groups):
    l1, l2 = latin_stats(latin_base, groups)
    rows = []
    for fs in fold_stats:
        key = select_key(fs["train"], l1, l2)
        held_d, held_raw = score_key(fs["held"], key, l1, l2)
        rows.append({
            "fold": fs["fold"],
            "held_distance": float(held_d),
            "slot": int(key["slot"]),
            "perm": list(key["perm"]),
            "train_distance": float(key["train_distance"]),
            "held_events": held_raw["events"],
            "held_pairs": held_raw["pairs"],
            "held_runs": held_raw["runs"],
            "training_state_counts": fs["train"][key["slot"]]["state_counts"],
        })
    return rows


def evaluate_policy(items, parser, policy, latin_base, nulls):
    folds = build_fold_stats(items, parser, policy)
    target_rows = evaluate_partition(folds, latin_base, PHILIP_GROUPS)
    target_mean = statistics.fmean(r["held_distance"] for r in target_rows)

    null_means = []
    fold_nulls = [[] for _ in range(5)]
    for groups in nulls:
        rows = evaluate_partition(folds, latin_base, groups)
        vals = [r["held_distance"] for r in rows]
        null_means.append(statistics.fmean(vals))
        for f, x in enumerate(vals):
            fold_nulls[f].append(x)

    fold_medians = [statistics.median(xs) for xs in fold_nulls]
    fold_wins = sum(target_rows[f]["held_distance"] < fold_medians[f] - EPS for f in range(5))
    key_counts = Counter((r["slot"], tuple(r["perm"])) for r in target_rows)
    recurrent_key, recurrence = min(key_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    sample_pass = all(
        r["held_events"] >= 1000 and r["held_pairs"] >= 500 and min(r["training_state_counts"]) > 0
        for r in target_rows
    )
    p = (1 + sum(x <= target_mean + EPS for x in null_means)) / (len(null_means) + 1)
    null_med = statistics.median(null_means)
    conditions = {
        "p_le_0_05": p <= .05,
        "below_null_median": target_mean < null_med - EPS,
        "fold_median_wins_ge_4": fold_wins >= 4,
        "exact_key_recurrence_ge_4": recurrence >= 4,
        "sample_gate": sample_pass,
    }

    if not sample_pass:
        classification = "INSUFFICIENT SAMPLE"
    elif conditions["p_le_0_05"] and conditions["below_null_median"] and conditions["fold_median_wins_ge_4"]:
        classification = (
            "PHILIP DURATION-GROUP COMPATIBILITY"
            if conditions["exact_key_recurrence_ge_4"]
            else "UNSTABLE FOUR-STATE MATCH / NOT CIPHER SUPPORT"
        )
    else:
        classification = "PHILIP DURATION-GROUP NOT SUPPORTED"

    return {
        "policy": policy,
        "classification": classification,
        "target_mean_distance": target_mean,
        "null_mean_distance_median": null_med,
        "null_mean_distance_q05": e.quantile(null_means, .05),
        "null_mean_distance_min": min(null_means),
        "target_minus_null_median": target_mean - null_med,
        "p_lower": p,
        "fold_median_wins": fold_wins,
        "exact_key_recurrence": recurrence,
        "most_recurrent_key": {"slot": recurrent_key[0], "perm": list(recurrent_key[1])},
        "conditions": conditions,
        "target_folds": [
            dict(
                r,
                null_fold_median=fold_medians[i],
                target_minus_null_fold_median=r["held_distance"] - fold_medians[i],
            )
            for i, r in enumerate(target_rows)
        ],
        "null_count": len(null_means),
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
    latin_base, latin_meta = latin_letter_counts(latin_root)
    nulls = make_null_partitions()

    primary = evaluate_policy(items, parser, "min", latin_base, nulls)
    sensitivity = evaluate_policy(items, parser, "max", latin_base, nulls)

    here = Path(__file__).resolve().parent
    out = {
        "experiment": "Issue26E8 Nicholas Philip duration-group prospective screen",
        "issue": 26,
        "historical_target": {
            "date": 1436,
            "duration_groups": ["".join(g) for g in PHILIP_GROUPS],
            "group_labels": ["quaver", "crotchet", "minim", "semibreve"],
            "five_pitch_contours_reserved_for_E8B_only": ["ascending", "descending", "ascending", "descending"],
        },
        "inputs": {
            "zl_blob_sha1": e.EXPECTED_ZL3B_BLOB,
            "cremma_commit": EXPECTED_CREMMA_COMMIT,
            "plan_sha256": sha256_file(here / "PLAN_E8.md"),
            "script_sha256": sha256_file(Path(__file__)),
            "core_sha256": sha256_file(here / "issue26e_core.py"),
            "null_seed_family": "Issue26E8:PhilipPartitionNull:v1",
            "null_count": NULL_N,
        },
        "latin_population": latin_meta,
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
