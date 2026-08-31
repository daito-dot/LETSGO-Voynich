#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import random
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np
from numba import njit

import issue26e_core as e

ALPHA = 0.1
PORTA_TABLE = (
    tuple("abcdefghilm"),  # semibreves, low -> high
    tuple("zyxutsrqpon"),  # minims, low -> high (plaintext n..z descends)
)
ALPHABET = tuple(sorted(set(PORTA_TABLE[0] + PORTA_TABLE[1])))
CHAR_INDEX = {c: i for i, c in enumerate(ALPHABET)}
TABLE_IDX = np.array([[CHAR_INDEX[c] for c in row] for row in PORTA_TABLE], dtype=np.int64)
CREMMA_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
PITCH_K = 11
DURATION_SLOT = 11
DURATION_STATES = ("", "y")


def stable_seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8], "big") & ((1 << 63) - 1)


def norm_char(ch: str):
    s = unicodedata.normalize("NFKD", ch.lower())
    s = "".join(c for c in s if "a" <= c <= "z")
    if not s:
        return None
    c = s[0]
    if c == "j": c = "i"
    elif c == "v": c = "u"
    return c


def load_latin(root: Path):
    runs = []
    lexicon = Counter()
    files = 0
    for rel in CREMMA_DIRS:
        d = root / rel
        if not d.is_dir():
            raise RuntimeError(f"missing CREMMA dir {d}")
        for p in sorted(d.rglob("*.txt")):
            files += 1
            text = p.read_text(encoding="utf-8", errors="replace")
            for raw in text.splitlines():
                cur = []
                for ch in raw:
                    c = norm_char(ch)
                    if c is not None and c in CHAR_INDEX:
                        cur.append(c)
                    else:
                        if len(cur) >= 4:
                            runs.append("".join(cur))
                        cur = []
                if len(cur) >= 4:
                    runs.append("".join(cur))
            for tok in re.findall(r"[A-Za-zÀ-ÿ]+", text):
                out = []
                ok = True
                for ch in tok:
                    c = norm_char(ch)
                    if c is None:
                        continue
                    if c not in CHAR_INDEX:
                        ok = False
                        break
                    out.append(c)
                w = "".join(out)
                if ok and len(w) >= 3:
                    lexicon[w] += 1
    if not runs:
        raise RuntimeError("no supported Latin runs")
    return runs, lexicon, {
        "files": files,
        "runs": len(runs),
        "chars": sum(map(len, runs)),
        "lexicon": len(lexicon),
        "alphabet": "".join(ALPHABET),
    }


class LM4:
    def __init__(self, runs):
        self.c3 = Counter()
        self.c4 = Counter()
        for s in runs:
            for i in range(3, len(s)):
                self.c3[s[i - 3:i]] += 1
                self.c4[s[i - 3:i + 1]] += 1
        self.v = len(ALPHABET)

    def bits(self, streams):
        nll = 0.0
        n = 0
        for s in streams:
            for i in range(3, len(s)):
                h = s[i - 3:i]
                q = s[i - 3:i + 1]
                p = (self.c4[q] + ALPHA) / (self.c3[h] + ALPHA * self.v)
                nll -= math.log2(p)
                n += 1
        return (nll / n if n else float("inf")), n


def bigram_cost(runs):
    prev = np.zeros(len(ALPHABET), dtype=np.int64)
    pair = np.zeros((len(ALPHABET), len(ALPHABET)), dtype=np.int64)
    for s in runs:
        for a, b in zip(s, s[1:]):
            ia = CHAR_INDEX[a]
            ib = CHAR_INDEX[b]
            prev[ia] += 1
            pair[ia, ib] += 1
    cost = np.empty_like(pair, dtype=np.float64)
    for a in range(len(ALPHABET)):
        den = prev[a] + ALPHA * len(ALPHABET)
        for b in range(len(ALPHABET)):
            cost[a, b] = -math.log2((pair[a, b] + ALPHA) / den)
    return cost


def latin_self_baseline(runs):
    buckets = [runs[i::5] for i in range(5)]
    ces = []
    ns = []
    for f in range(5):
        train = [s for i, bucket in enumerate(buckets) if i != f for s in bucket]
        lm = LM4(train)
        ce, n = lm.bits(buckets[f])
        ces.append(ce)
        ns.append(n)
    chars = Counter("".join(runs))
    total = sum(chars.values())
    top5 = sum(n for _, n in chars.most_common(5)) / total if total else 0.0
    return {
        "fold_cross_entropy": ces,
        "fold_scored_chars": ns,
        "mean_cross_entropy": statistics.fmean(ces),
        "top5_char_fraction": top5,
        "char_counts": dict(chars),
    }


FEATURE_LABELS = []
for _s in range(11):
    FEATURE_LABELS.append((_s, ""))
    FEATURE_LABELS.extend((_s, v) for v in e.SLOTS[_s])
FEATURE_INDEX = {v: i for i, v in enumerate(FEATURE_LABELS)}


def morph_feature(vals):
    x = np.zeros(len(FEATURE_LABELS), dtype=np.float64)
    for s in range(11):
        x[FEATURE_INDEX[(s, vals[s])]] = 1.0
    return x


class KMeansK:
    def __init__(self, k=PITCH_K):
        self.k = k

    def fit(self, vectors):
        names = sorted(vectors)
        if len(names) < self.k:
            raise RuntimeError(f"only {len(names)} training token types for k={self.k}")
        X = np.stack([vectors[n] for n in names])
        chosen = [0]
        while len(chosen) < self.k:
            C = X[chosen]
            d = ((X[:, None] - C[None]) ** 2).sum(2).min(1)
            d[chosen] = -1
            md = float(d.max())
            tied = [i for i, z in enumerate(d) if abs(float(z) - md) <= e.EPS]
            chosen.append(min(tied, key=lambda i: names[i]))
        C = X[chosen].copy()
        prev = None
        for _ in range(100):
            D = ((X[:, None] - C[None]) ** 2).sum(2)
            a = D.argmin(1)
            if prev is not None and np.array_equal(a, prev):
                break
            prev = a.copy()
            new = C.copy()
            occupied = set()
            for j in range(self.k):
                idx = np.flatnonzero(a == j)
                if len(idx):
                    new[j] = X[idx].mean(0)
                    occupied.add(j)
            empty = [j for j in range(self.k) if j not in occupied]
            if empty:
                da = D[np.arange(len(X)), a]
                candidates = sorted(range(len(names)), key=lambda i: (-float(da[i]), names[i]))
                used = set()
                for j in empty:
                    i = next(i for i in candidates if i not in used)
                    used.add(i)
                    new[j] = X[i]
            C = new
        self.centroids = C
        self.training_types = len(names)
        return self

    def predict(self, x):
        return int(((self.centroids - x[None]) ** 2).sum(1).argmin())


def training_vectors(items, leaves, parser, policy):
    vectors = {}
    for it in items:
        if it["leaf"] not in leaves:
            continue
        for line in it["lines"]:
            for tok in line:
                p = parser.pick(tok, policy)
                if p is None:
                    continue
                vectors[tok] = morph_feature(p[1])
    return vectors


def raw_streams(items, leaves, parser, policy, km):
    out = []
    raw_counts = np.zeros(22, dtype=np.int64)
    parsed = 0
    visible = 0
    for it in items:
        if it["leaf"] not in leaves:
            continue
        for li, line in enumerate(it["lines"]):
            cur = []
            seg = 0
            def flush():
                nonlocal cur, seg
                if cur:
                    out.append({"page": it["page"], "line_index": li, "segment": seg, "codes": cur})
                    seg += 1
                cur = []
            for tok in line:
                visible += 1
                p = parser.pick(tok, policy)
                if p is None:
                    flush()
                    continue
                vals = p[1]
                if vals[DURATION_SLOT] not in DURATION_STATES:
                    raise RuntimeError(f"unexpected slot11 state {vals[DURATION_SLOT]!r}")
                dur = 0 if vals[DURATION_SLOT] == "" else 1
                cluster = km.predict(morph_feature(vals))
                code = dur * PITCH_K + cluster
                cur.append(code)
                raw_counts[code] += 1
                parsed += 1
            flush()
    return out, raw_counts, {"visible_tokens": visible, "parsed_tokens": parsed, "streams": len(out)}


def raw_bigram_counts(streams):
    C = np.zeros((22, 22), dtype=np.int64)
    total = 0
    for m in streams:
        xs = m["codes"]
        for a, b in zip(xs, xs[1:]):
            C[a, b] += 1
            total += 1
    return C, total


@njit(cache=True)
def _rng_next(state):
    x = state
    x ^= (x << np.uint64(13)) & np.uint64(0xFFFFFFFFFFFFFFFF)
    x ^= x >> np.uint64(7)
    x ^= (x << np.uint64(17)) & np.uint64(0xFFFFFFFFFFFFFFFF)
    return x


@njit(cache=True)
def _rng_float(state):
    state = _rng_next(state)
    z = (state >> np.uint64(11)) & np.uint64((1 << 53) - 1)
    return state, float(z) / float(1 << 53)


@njit(cache=True)
def _score_key(C, total, cost, table_idx, perm, orient):
    if total <= 0:
        return 1e30
    s = 0.0
    for a in range(22):
        da = a // 11
        ca = a % 11
        ra = da if orient == 0 else 1 - da
        la = table_idx[ra, perm[ca]]
        for b in range(22):
            n = C[a, b]
            if n == 0:
                continue
            db = b // 11
            cb = b % 11
            rb = db if orient == 0 else 1 - db
            lb = table_idx[rb, perm[cb]]
            s += n * cost[la, lb]
    return s / total


@njit(cache=True)
def _anneal(C, total, cost, table_idx, orient, seed, steps):
    state = np.uint64(seed if seed != 0 else 1)
    perm = np.arange(11, dtype=np.int64)
    for i in range(10, 0, -1):
        state, u = _rng_float(state)
        j = int(u * (i + 1))
        if j > i:
            j = i
        tmp = perm[i]
        perm[i] = perm[j]
        perm[j] = tmp
    cur = _score_key(C, total, cost, table_idx, perm, orient)
    best = cur
    bestp = perm.copy()
    ratio = 0.00005 / 0.05
    for step in range(steps):
        state, u1 = _rng_float(state)
        state, u2 = _rng_float(state)
        i = int(u1 * 11)
        j = int(u2 * 10)
        if j >= i:
            j += 1
        tmp = perm[i]
        perm[i] = perm[j]
        perm[j] = tmp
        new = _score_key(C, total, cost, table_idx, perm, orient)
        d = new - cur
        frac = step / max(1, steps - 1)
        T = 0.05 * (ratio ** frac)
        accept = d <= 0.0
        if not accept:
            state, u3 = _rng_float(state)
            if u3 < math.exp(-d / T):
                accept = True
        if accept:
            cur = new
            if cur < best - 1e-15:
                best = cur
                bestp = perm.copy()
        else:
            tmp = perm[i]
            perm[i] = perm[j]
            perm[j] = tmp
    perm = bestp.copy()
    cur = best
    while True:
        best_i = -1
        best_j = -1
        best_s = cur
        for i in range(10):
            for j in range(i + 1, 11):
                tmp = perm[i]
                perm[i] = perm[j]
                perm[j] = tmp
                z = _score_key(C, total, cost, table_idx, perm, orient)
                tmp = perm[i]
                perm[i] = perm[j]
                perm[j] = tmp
                if z < best_s - 1e-12:
                    best_s = z
                    best_i = i
                    best_j = j
        if best_i < 0:
            break
        tmp = perm[best_i]
        perm[best_i] = perm[best_j]
        perm[best_j] = tmp
        cur = best_s
    return perm, cur


def fit_key(C, total, cost, label):
    best = None
    for orient in (0, 1):
        for restart in range(24):
            seed = stable_seed(f"Issue26E12:Porta11x2:v1:{label}:{orient}:{restart}")
            perm, score = _anneal(C, total, cost, TABLE_IDX, orient, seed, 40000)
            key = (float(score), orient, tuple(int(x) for x in perm))
            if best is None or key < best:
                best = key
    return {"training_bigram_cross_entropy": best[0], "duration_orientation": best[1], "pitch_permutation": list(best[2])}


def decode_code(code, key):
    dur = code // 11
    cl = code % 11
    row = dur if key["duration_orientation"] == 0 else 1 - dur
    rank = key["pitch_permutation"][cl]
    return PORTA_TABLE[row][rank]


def decode_streams(streams, key):
    out = []
    meta = []
    counts = Counter()
    for m in streams:
        s = "".join(decode_code(c, key) for c in m["codes"])
        if not s:
            continue
        counts.update(s)
        out.append(s)
        meta.append({"page": m["page"], "line_index": m["line_index"], "segment": m["segment"], "text": s})
    return out, meta, counts


def lexicon_substring_hits(meta, lexicon):
    hits = []
    distinct = set()
    for m in meta:
        s = m["text"]
        for i in range(len(s)):
            for L in range(4, min(15, len(s) - i) + 1):
                w = s[i:i + L]
                freq = lexicon.get(w, 0)
                if not freq:
                    continue
                distinct.add(w)
                hits.append({
                    "word": w,
                    "length": L,
                    "corpus_frequency": int(freq),
                    "page": m["page"],
                    "line_index": m["line_index"],
                    "offset": i,
                    "context": s[max(0, i - 10):min(len(s), i + L + 10)],
                })
    hits.sort(key=lambda z: (-z["length"], -z["corpus_frequency"], z["word"], z["page"], z["line_index"], z["offset"]))
    return hits[:100], sorted(distinct)


def diagnostics(streams, meta, counts, lm4, lexicon):
    ce, n = lm4.bits(streams)
    total = sum(counts.values())
    top5 = sum(v for _, v in counts.most_common(5)) / total if total else 0.0
    hits, distinct = lexicon_substring_hits(meta, lexicon)
    d6 = sorted(w for w in distinct if len(w) >= 6)
    grams = Counter()
    for s in streams:
        for i in range(len(s) - 3):
            grams[s[i:i + 4]] += 1
    samples = [m for m in meta if len(m["text"]) >= 12][:20]
    return {
        "cross_entropy": ce,
        "scored_chars": n,
        "char_counts": dict(counts),
        "top5_char_fraction": top5,
        "distinct_lexicon_hits": len(distinct),
        "distinct_lexicon_hits_ge6": len(d6),
        "distinct_words_ge6": d6[:100],
        "lexicon_hits": hits,
        "samples": samples,
        "top_4grams": [{"ngram": q, "decoded_count": int(c), "latin_count": int(lm4.c4.get(q, 0))} for q, c in grams.most_common(50)],
    }


def run_voynich_policy(items, parser, policy, lm4, bg_cost, lexicon):
    folds = e.physical_leaf_folds(items)
    universe = set().union(*folds)
    rows = []
    pooled_counts = Counter()
    pooled_streams = []
    fold_word_sets = []
    for f, held in enumerate(folds):
        train = universe - held
        vectors = training_vectors(items, train, parser, policy)
        km = KMeansK().fit(vectors)
        tr_streams, tr_counts, tr_meta = raw_streams(items, train, parser, policy, km)
        C, total_pairs = raw_bigram_counts(tr_streams)
        key = fit_key(C, total_pairs, bg_cost, f"{policy}:{f}")
        he_streams_raw, he_counts_raw, he_meta_raw = raw_streams(items, held, parser, policy, km)
        decoded, meta, counts = decode_streams(he_streams_raw, key)
        d = diagnostics(decoded, meta, counts, lm4, lexicon)
        pooled_counts.update(counts)
        pooled_streams.extend(decoded)
        fold_word_sets.append(set(d["distinct_words_ge6"]))
        rows.append({
            "fold": f,
            "held_leaves": sorted(held),
            "training_types": km.training_types,
            "cluster_train_counts": tr_counts.tolist(),
            "training_population": tr_meta,
            "held_population": he_meta_raw,
            "selected_key": key,
            "held": d,
        })
    mean_ce = statistics.fmean(r["held"]["cross_entropy"] for r in rows)
    total_chars = sum(pooled_counts.values())
    pooled_top5 = sum(v for _, v in pooled_counts.most_common(5)) / total_chars if total_chars else 0.0
    all_words = set().union(*fold_word_sets) if fold_word_sets else set()
    qualifying_folds = sum(1 for s in fold_word_sets if s)
    orient_counts = Counter(r["selected_key"]["duration_orientation"] for r in rows)
    orient, recurrence = min(orient_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return {
        "policy": policy,
        "mean_held_cross_entropy": mean_ce,
        "duration_orientation_recurrence": recurrence,
        "modal_duration_orientation": orient,
        "pooled_top5_char_fraction": pooled_top5,
        "pooled_char_counts": dict(pooled_counts),
        "distinct_words_ge6": sorted(all_words)[:200],
        "distinct_words_ge6_count": len(all_words),
        "folds_with_any_word_ge6": qualifying_folds,
        "folds": rows,
    }


def inverse_table():
    inv = {}
    for row in range(2):
        for pitch in range(11):
            inv[PORTA_TABLE[row][pitch]] = (row, pitch)
    return inv


def select_runs_to_count(runs, target):
    out = []
    n = 0
    for s in runs:
        if n >= target:
            break
        take = min(len(s), target - n)
        if take >= 4:
            out.append(s[:take])
            n += take
        elif take > 0 and out:
            # Keep LM-valid runs only; slight underfill is acceptable.
            break
    return out


def synthetic_encode(runs, hidden_orient, hidden_perm):
    inv = inverse_table()
    inv_pitch = [0] * 11
    for cluster, pitch in enumerate(hidden_perm):
        inv_pitch[pitch] = cluster
    out = []
    truth = []
    for s in runs:
        codes = []
        chars = []
        for ch in s:
            row, pitch = inv[ch]
            durraw = row if hidden_orient == 0 else 1 - row
            cluster = inv_pitch[pitch]
            codes.append(durraw * 11 + cluster)
            chars.append(ch)
        if codes:
            out.append({"codes": codes})
            truth.append("".join(chars))
    return out, truth


def decode_synthetic(streams, key):
    return ["".join(decode_code(c, key) for c in m["codes"]) for m in streams]


def positive_control(runs, target_count, lm4, bg_cost):
    selected = select_runs_to_count(runs, target_count)
    buckets = [selected[i::5] for i in range(5)]
    rows = []
    for f in range(5):
        rng = random.Random(stable_seed(f"Issue26E12:PositiveKey:v1:{f}"))
        perm = list(range(11))
        rng.shuffle(perm)
        orient = rng.randrange(2)
        all_train = [s for i, b in enumerate(buckets) if i != f for s in b]
        held = buckets[f]
        tr_raw, _ = synthetic_encode(all_train, orient, perm)
        he_raw, he_truth = synthetic_encode(held, orient, perm)
        C, total_pairs = raw_bigram_counts(tr_raw)
        recovered = fit_key(C, total_pairs, bg_cost, f"positive:{f}")
        decoded = decode_synthetic(he_raw, recovered)
        rec_ce, rec_n = lm4.bits(decoded)
        true_ce, true_n = lm4.bits(he_truth)
        correct = total = 0
        for a, b in zip(decoded, he_truth):
            for x, y in zip(a, b):
                correct += int(x == y)
                total += 1
        rows.append({
            "fold": f,
            "hidden_orientation": orient,
            "hidden_pitch_permutation": perm,
            "recovered_key": recovered,
            "true_held_cross_entropy": true_ce,
            "recovered_held_cross_entropy": rec_ce,
            "scored_chars": rec_n,
            "decoded_letter_accuracy": correct / total if total else 0.0,
        })
    mean_true = statistics.fmean(r["true_held_cross_entropy"] for r in rows)
    mean_rec = statistics.fmean(r["recovered_held_cross_entropy"] for r in rows)
    mean_acc = statistics.fmean(r["decoded_letter_accuracy"] for r in rows)
    passed = (mean_rec - mean_true <= 0.05 and mean_acc >= 0.95)
    return {
        "passed": passed,
        "mean_true_held_cross_entropy": mean_true,
        "mean_recovered_held_cross_entropy": mean_rec,
        "mean_decoded_letter_accuracy": mean_acc,
        "folds": rows,
    }


def classify(primary, baseline, pos):
    lowdiv = primary["pooled_top5_char_fraction"] >= 0.90
    if not pos["passed"]:
        return "SOLVER INADEQUATE", {"low_diversity_optimum": lowdiv}
    gates = {
        "ce_within_0_50": primary["mean_held_cross_entropy"] <= baseline["mean_cross_entropy"] + 0.50,
        "top5_within_0_15": primary["pooled_top5_char_fraction"] <= baseline["top5_char_fraction"] + 0.15,
        "ten_distinct_words_ge6": primary["distinct_words_ge6_count"] >= 10,
        "word_hits_across_3folds": primary["folds_with_any_word_ge6"] >= 3,
        "duration_orientation_recurrence_ge4": primary["duration_orientation_recurrence"] >= 4,
    }
    lead = all(gates.values())
    return ("PORTA PLAINTEXT LEAD" if lead else "NO READABLE PORTA PLAINTEXT"), {
        "gates": gates,
        "low_diversity_optimum": lowdiv,
        "low_diversity_label": "LOW-DIVERSITY OPTIMUM" if lowdiv else "NO LOW-DIVERSITY FLAG",
    }


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr)
        return 2
    zl = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")
    parser = e.SlotParser()
    validation = e.validate_parser(parser)
    items = e.parse_voynich(zl)
    runs, lexicon, lmeta = load_latin(root)
    lm4 = LM4(runs)
    bg = bigram_cost(runs)
    baseline = latin_self_baseline(runs)

    # Estimate comparable positive-control size from all primary parsed token events.
    all_leaves = {it["leaf"] for it in items if it["leaf"] is not None}
    vectors = training_vectors(items, all_leaves, parser, "min")
    full_km = KMeansK().fit(vectors)
    _, full_raw_counts, full_meta = raw_streams(items, all_leaves, parser, "min", full_km)
    pos = positive_control(runs, int(full_raw_counts.sum()), lm4, bg)

    primary = run_voynich_policy(items, parser, "min", lm4, bg, lexicon)
    sensitivity = run_voynich_policy(items, parser, "max", lm4, bg, lexicon)
    classification, gates = classify(primary, baseline, pos)

    out = {
        "experiment": "Issue26E12 Porta 1602 11x2 musical-cipher plaintext probe",
        "classification": classification,
        "interpretation": gates,
        "historical_table_low_to_high": ["".join(r) for r in PORTA_TABLE],
        "historical_supported_alphabet": "".join(ALPHABET),
        "voynich_binary_factor": {"slot": DURATION_SLOT, "states": list(DURATION_STATES)},
        "voynich_pitch_projection": {"k": 11, "status": "HYPOTHESIS-SIDE PORTA-IMPOSED TRAIN-ONLY CLUSTERING"},
        "latin_population": lmeta,
        "latin_self_baseline": baseline,
        "positive_control": pos,
        "full_primary_population": full_meta,
        "slot_parser_validation": validation,
        "primary_min": primary,
        "max_sensitivity": sensitivity,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
