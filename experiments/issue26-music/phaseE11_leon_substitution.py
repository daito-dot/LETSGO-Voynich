#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from numba import njit

import issue26e_core as e

ALPHABET = tuple("abcdefghiklmnopqrstuvwxyz")
A = len(ALPHABET)
AI = {c: i for i, c in enumerate(ALPHABET)}
ALPHA = 0.1
COMPOUNDS = ("cth", "ckh", "cph", "cfh", "ch", "sh")
CREMMA_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
RESTARTS = 16
STEPS = 30_000
T0 = 0.05
T1 = 0.00005
EPS = 1e-12


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


def tokenize_glyphs(token: str):
    token = token.lower()
    out = []
    i = 0
    while i < len(token):
        hit = None
        for c in COMPOUNDS:
            if token.startswith(c, i):
                hit = c
                break
        if hit is not None:
            out.append(hit)
            i += len(hit)
        else:
            ch = token[i]
            if "a" <= ch <= "z":
                out.append(ch)
            else:
                raise RuntimeError(f"nonalphabetic Voynich character in normalized token {token!r}")
            i += 1
    return out


def load_latin(root: Path):
    runs = []
    lexicon = Counter()
    files = 0
    for rel in CREMMA_DIRS:
        d = root / rel
        if not d.is_dir():
            raise RuntimeError(f"missing CREMMA directory {d}")
        for p in sorted(d.rglob("*.txt")):
            files += 1
            text = p.read_text(encoding="utf-8", errors="replace")
            # E11 amendment: ignore all nonletters within a physical line.
            for raw in text.splitlines():
                chars = []
                for ch in raw:
                    c = norm_letter(ch)
                    if c is not None:
                        chars.append(c)
                if len(chars) >= 4:
                    runs.append("".join(chars))
            # Word boundaries are retained only for readability diagnostics.
            for tok in re.findall(r"[A-Za-zÀ-ÿ]+", text):
                chars = []
                valid = True
                for ch in tok:
                    c = norm_letter(ch)
                    if c is None:
                        # alphabetic characters outside the frozen normalized alphabet invalidate word match
                        if ch.isalpha():
                            valid = False
                            break
                        continue
                    chars.append(c)
                w = "".join(chars)
                if valid and len(w) >= 3:
                    lexicon[w] += 1
    if not runs:
        raise RuntimeError("no Latin runs")
    return runs, lexicon, {
        "files": files,
        "runs": len(runs),
        "chars": sum(map(len, runs)),
        "lexicon": len(lexicon),
        "alphabet": "".join(ALPHABET),
    }


class LM4:
    def __init__(self, runs):
        c3 = np.zeros(A ** 3, dtype=np.int64)
        c4 = np.zeros(A ** 4, dtype=np.int64)
        self.c4_counter = Counter()
        for s in runs:
            xs = [AI[c] for c in s]
            for i in range(3, len(xs)):
                h = (xs[i-3] * A + xs[i-2]) * A + xs[i-1]
                q = h * A + xs[i]
                c3[h] += 1
                c4[q] += 1
                self.c4_counter[s[i-3:i+1]] += 1
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
                q = (((xs[i-3] * A + xs[i-2]) * A + xs[i-1]) * A + xs[i])
                nll += float(self.cost[q])
                n += 1
        return (nll / n if n else float("inf")), n


def latin_self_baseline(runs):
    rows = []
    for f in range(5):
        train = [s for i, s in enumerate(runs) if i % 5 != f]
        held = [s for i, s in enumerate(runs) if i % 5 == f]
        lm = LM4(train)
        ce, n = lm.score_plain_runs(held)
        rows.append({"fold": f, "cross_entropy": ce, "scored_chars": n})
    chars = Counter("".join(runs))
    total = sum(chars.values())
    top5 = sum(v for _, v in chars.most_common(5)) / total
    return {
        "mean_cross_entropy": statistics.fmean(r["cross_entropy"] for r in rows),
        "folds": rows,
        "char_counts": dict(chars.most_common()),
        "top5_char_fraction": top5,
    }


def build_voynich_records(zl: Path):
    items = e.parse_voynich(zl)
    folds = e.physical_leaf_folds(items)
    if len(folds) != 5:
        raise RuntimeError(f"expected 5 physical-leaf folds, got {len(folds)}")
    universe = set().union(*folds)
    tmp = []
    glyph_counts = Counter()
    for it in items:
        if it["leaf"] not in universe:
            continue
        for li, line in enumerate(it["lines"]):
            toks = []
            seq = []
            for tok in line:
                gs = tokenize_glyphs(tok)
                if not gs:
                    continue
                toks.append(gs)
                seq.extend(gs)
                glyph_counts.update(gs)
            if seq:
                tmp.append({
                    "leaf": it["leaf"], "page": it["page"], "paragraph": it["id"],
                    "line_index": li, "tokens_glyph": toks, "seq_glyph": seq,
                })
    labels = sorted(glyph_counts)
    gi = {g: i for i, g in enumerate(labels)}
    records = []
    for r in tmp:
        records.append({
            "leaf": r["leaf"], "page": r["page"], "paragraph": r["paragraph"],
            "line_index": r["line_index"],
            "tokens": [np.asarray([gi[g] for g in t], dtype=np.int16) for t in r["tokens_glyph"]],
            "seq": np.asarray([gi[g] for g in r["seq_glyph"]], dtype=np.int16),
        })
    return records, folds, labels, glyph_counts


def pattern_arrays_from_sequences(seqs, M):
    ctr = Counter()
    for s in seqs:
        for i in range(len(s) - 3):
            ctr[(int(s[i]), int(s[i+1]), int(s[i+2]), int(s[i+3]))] += 1
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
def swap_delta(key, i, j, M, pats, counts, offsets, incident, lm_cost, marks, stamp, total_count):
    stamp += 1
    old_i = key[i]
    old_j = key[j]
    delta_total = 0.0

    if i < M:
        for z in range(offsets[i], offsets[i+1]):
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
        for z in range(offsets[j], offsets[j+1]):
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
def anneal_one(initial_key, seed, M, pats, counts, offsets, incident, lm_cost):
    key = initial_key.copy()
    total_count = 0
    for x in counts:
        total_count += x
    marks = np.zeros(pats.shape[0], dtype=np.int32)
    stamp = 0
    np.random.seed(seed)
    current = full_score(key, pats, counts, lm_cost)
    T = T0
    ratio = math.exp(math.log(T1 / T0) / (STEPS - 1))

    for _ in range(STEPS):
        i = np.random.randint(0, A)
        j = np.random.randint(0, A - 1)
        if j >= i:
            j += 1
        d, stamp = swap_delta(key, i, j, M, pats, counts, offsets, incident,
                              lm_cost, marks, stamp, total_count)
        if d <= 0.0 or np.random.random() < math.exp(-d / T):
            tmp = key[i]; key[i] = key[j]; key[j] = tmp
            current += d
        T *= ratio

    # Exact deterministic steepest pair-swap descent.
    while True:
        best_d = -EPS
        best_i = -1
        best_j = -1
        for i in range(A - 1):
            for j in range(i + 1, A):
                d, stamp = swap_delta(key, i, j, M, pats, counts, offsets, incident,
                                      lm_cost, marks, stamp, total_count)
                if d < best_d:
                    best_d = d
                    best_i = i
                    best_j = j
        if best_i < 0:
            break
        tmp = key[best_i]; key[best_i] = key[best_j]; key[best_j] = tmp
        current += best_d

    return key, full_score(key, pats, counts, lm_cost)


def optimize_key(seqs, M, lm_cost, fold):
    pats, counts, offsets, incident = pattern_arrays_from_sequences(seqs, M)
    best_key = None
    best_ce = float("inf")
    restart_rows = []
    for r in range(RESTARTS):
        seed = seed32(f"Issue26E11:LeonMonoSub:v1:{fold}:{r}")
        rng = np.random.default_rng(seed)
        initial = rng.permutation(A).astype(np.int16)
        key, ce = anneal_one(initial, seed, M, pats, counts, offsets, incident, lm_cost)
        t = tuple(int(x) for x in key)
        restart_rows.append({"restart": r, "seed": seed, "cross_entropy": float(ce)})
        if ce < best_ce - EPS or (abs(ce - best_ce) <= EPS and (best_key is None or t < tuple(int(x) for x in best_key))):
            best_ce = float(ce)
            best_key = key.copy()
    return best_key, best_ce, restart_rows


def score_key_on_seqs(key, seqs, M, lm_cost):
    pats, counts, _, _ = pattern_arrays_from_sequences(seqs, M)
    ce = float(full_score(key, pats, counts, lm_cost))
    return ce, int(counts.sum())


def decode_seq(seq, key):
    return "".join(ALPHABET[int(key[int(g)])] for g in seq)


def diagnostics_records(records, key, lm, lexicon, fold=None):
    line_texts = []
    char_counts = Counter()
    gram_counts = Counter()
    samples = []
    hits = []
    seen_hits = set()
    scored = 0
    nll = 0.0
    for rec in records:
        plain_seq = decode_seq(rec["seq"], key)
        line_texts.append(plain_seq)
        char_counts.update(plain_seq)
        for i in range(len(plain_seq) - 3):
            q = plain_seq[i:i+4]
            gram_counts[q] += 1
            idx = (((AI[q[0]] * A + AI[q[1]]) * A + AI[q[2]]) * A + AI[q[3]])
            nll += float(lm.cost[idx]); scored += 1
        decoded_tokens = [decode_seq(t, key) for t in rec["tokens"]]
        spaced = " ".join(decoded_tokens)
        if len(spaced) >= 12 and len(samples) < 20:
            samples.append({"page": rec["page"], "line_index": rec["line_index"], "text": spaced[:160]})
        for ti, w in enumerate(decoded_tokens):
            if len(w) < 4:
                continue
            freq = int(lexicon.get(w, 0))
            if not freq:
                continue
            hk = (w, rec["page"], rec["line_index"], ti)
            if hk in seen_hits:
                continue
            seen_hits.add(hk)
            hits.append({"word": w, "length": len(w), "corpus_frequency": freq,
                         "page": rec["page"], "line_index": rec["line_index"], "token_index": ti,
                         "context": " ".join(decoded_tokens[max(0,ti-3):ti+4]), "fold": fold})
    total = sum(char_counts.values())
    top5 = sum(v for _, v in char_counts.most_common(5)) / total if total else 1.0
    hits.sort(key=lambda z: (-z["length"], -z["corpus_frequency"], z["word"], z["page"], z["line_index"], z["token_index"]))
    return {
        "cross_entropy": nll / scored if scored else float("inf"),
        "scored_chars": scored,
        "decoded_chars": total,
        "lines": len(records),
        "top5_char_fraction": top5,
        "char_counts": dict(char_counts.most_common()),
        "samples": samples,
        "whole_token_lexicon_hits": hits[:100],
        "distinct_hits_ge6": len({h["word"] for h in hits if h["length"] >= 6}),
        "top_4grams": [{"ngram": q, "decoded_count": int(c), "latin_count": int(lm.c4_counter.get(q, 0))}
                       for q, c in gram_counts.most_common(50)],
    }


def key_mapping(key, labels):
    return {labels[i]: ALPHABET[int(key[i])] for i in range(len(labels))}


def run_voynich(records, folds, labels, glyph_counts, lm, lexicon):
    M = len(labels)
    universe = set().union(*folds)
    rows = []
    keys = []
    for f, held in enumerate(folds):
        train_records = [r for r in records if r["leaf"] in universe and r["leaf"] not in held]
        held_records = [r for r in records if r["leaf"] in held]
        key, tr_ce, restarts = optimize_key([r["seq"] for r in train_records], M, lm.cost, f)
        dg = diagnostics_records(held_records, key, lm, lexicon, fold=f)
        keys.append(key.copy())
        rows.append({"fold": f, "held_leaves": sorted(held), "training_cross_entropy": tr_ce,
                     "mapping": key_mapping(key, labels), "full_permutation": [ALPHABET[int(x)] for x in key],
                     "held": dg, "restart_scores": restarts})

    # Pooled held-out objective under fold-specific keys.
    pooled_nll = sum(r["held"]["cross_entropy"] * r["held"]["scored_chars"] for r in rows)
    pooled_n = sum(r["held"]["scored_chars"] for r in rows)
    pooled_ce = pooled_nll / pooled_n
    mean_ce = statistics.fmean(r["held"]["cross_entropy"] for r in rows)

    # Key stability.
    total_occ = sum(glyph_counts.values())
    weighted_stability = 0.0
    glyph_stability = {}
    for gi, label in enumerate(labels):
        vals = [int(k[gi]) for k in keys]
        c = Counter(vals)
        modal_idx, modal_n = min(c.items(), key=lambda kv: (-kv[1], ALPHABET[kv[0]]))
        st = modal_n / 5
        weight = glyph_counts[label] / total_occ
        weighted_stability += weight * st
        glyph_stability[label] = {"modal_plaintext": ALPHABET[modal_idx], "modal_count": modal_n,
                                  "stability": st, "occurrences": int(glyph_counts[label]), "weight": weight}
    key_tuples = [tuple(int(x) for x in k[:M]) for k in keys]
    rec = Counter(key_tuples)
    _, exact_rec = min(rec.items(), key=lambda kv: (-kv[1], kv[0]))
    pairwise = []
    for i in range(5):
        for j in range(i+1, 5):
            agree = sum(1 for g in range(M) if keys[i][g] == keys[j][g]) / M
            weight_agree = sum(glyph_counts[labels[g]] for g in range(M) if keys[i][g] == keys[j][g]) / total_occ
            pairwise.append({"fold_a": i, "fold_b": j, "glyph_agreement": agree,
                             "occurrence_weighted_agreement": weight_agree})

    # Pooled readability diagnostics: each record appears once in its held-out fold.
    pooled_char = Counter()
    pooled_grams = Counter()
    pooled_hits = []
    hit_folds = set()
    for row in rows:
        d = row["held"]
        pooled_char.update(d["char_counts"])
        for q in d["top_4grams"]:
            # top-50 truncation is not enough for a complete pooled ranking; keep descriptive fold rows instead.
            pass
        for h in d["whole_token_lexicon_hits"]:
            pooled_hits.append(h)
            if h["length"] >= 6:
                hit_folds.add(row["fold"])
    total_chars = sum(pooled_char.values())
    top5 = sum(v for _, v in pooled_char.most_common(5)) / total_chars if total_chars else 1.0
    distinct6 = sorted({h["word"] for h in pooled_hits if h["length"] >= 6})

    return {
        "mean_held_cross_entropy": mean_ce,
        "pooled_held_cross_entropy": pooled_ce,
        "weighted_key_stability": weighted_stability,
        "exact_full_key_recurrence": int(exact_rec),
        "glyph_stability": glyph_stability,
        "pairwise_mapping_agreement": pairwise,
        "pooled_top5_char_fraction": top5,
        "pooled_char_counts": dict(pooled_char.most_common()),
        "distinct_whole_token_hits_ge6": distinct6,
        "distinct_whole_token_hits_ge6_count": len(distinct6),
        "folds_with_hits_ge6": sorted(hit_folds),
        "folds": rows,
    }


def split_topm_runs(latin_runs, top_set, target_events):
    out = []
    total = 0
    for s in latin_runs:
        cur = []
        chunks = []
        for ch in s:
            if ch in top_set:
                cur.append(ch)
            else:
                if cur:
                    chunks.append("".join(cur)); cur = []
        if cur:
            chunks.append("".join(cur))
        for chunk in chunks:
            if total >= target_events:
                break
            remaining = target_events - total
            use = chunk[:remaining]
            if use:
                out.append(use)
                total += len(use)
        if total >= target_events:
            break
    if total < min(target_events, 1000):
        raise RuntimeError(f"positive control too short: {total}")
    return out, total


def run_positive_control(latin_runs, labels, glyph_counts, lm, target_events):
    M = len(labels)
    freq = Counter("".join(latin_runs))
    top_plain = [c for c, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:M]]
    top_set = set(top_plain)
    runs, events = split_topm_runs(latin_runs, top_set, target_events)
    rng = np.random.default_rng(seed32("Issue26E11:PositiveKey:v1"))
    cipher_order = rng.permutation(M).tolist()
    plain_to_cipher = {top_plain[i]: int(cipher_order[i]) for i in range(M)}
    true_decode = np.full(M, -1, dtype=np.int16)
    for p, cidx in plain_to_cipher.items():
        true_decode[cidx] = AI[p]
    if np.any(true_decode < 0):
        raise RuntimeError("positive key incomplete")
    encoded = [np.asarray([plain_to_cipher[ch] for ch in s], dtype=np.int16) for s in runs]
    fold_ids = [i % 5 for i in range(len(encoded))]
    symbol_counts = np.zeros(M, dtype=np.int64)
    for s in encoded:
        for x in s:
            symbol_counts[int(x)] += 1
    rows = []
    recovered_keys = []
    for f in range(5):
        train = [s for i, s in enumerate(encoded) if fold_ids[i] != f]
        held = [s for i, s in enumerate(encoded) if fold_ids[i] == f]
        key, tr_ce, restarts = optimize_key(train, M, lm.cost, f)
        rec_ce, rec_n = score_key_on_seqs(key, held, M, lm.cost)
        # complete true full key with unused plaintext letters for scoring
        used = set(int(x) for x in true_decode)
        unused = [i for i in range(A) if i not in used]
        true_full = np.asarray(list(true_decode) + unused, dtype=np.int16)
        true_ce, true_n = score_key_on_seqs(true_full, held, M, lm.cost)
        exact = sum(int(key[i]) == int(true_decode[i]) for i in range(M)) / M
        weighted = sum(symbol_counts[i] for i in range(M) if int(key[i]) == int(true_decode[i])) / symbol_counts.sum()
        recovered_keys.append(tuple(int(x) for x in key[:M]))
        rows.append({"fold": f, "training_cross_entropy": tr_ce, "recovered_held_cross_entropy": rec_ce,
                     "true_held_cross_entropy": true_ce, "held_scored_chars": rec_n,
                     "exact_key_accuracy": exact, "occurrence_weighted_key_accuracy": weighted,
                     "recovered_mapping": key_mapping(key, labels),
                     "restart_scores": restarts})
    mean_rec = statistics.fmean(r["recovered_held_cross_entropy"] for r in rows)
    mean_true = statistics.fmean(r["true_held_cross_entropy"] for r in rows)
    mean_weighted = statistics.fmean(r["occurrence_weighted_key_accuracy"] for r in rows)
    rec = Counter(recovered_keys)
    _, exact_rec = min(rec.items(), key=lambda kv: (-kv[1], kv[0]))
    passed = abs(mean_rec - mean_true) <= 0.05 and mean_weighted >= 0.95
    return {
        "passed": passed,
        "events": events,
        "runs": len(runs),
        "top_plaintext_letters": top_plain,
        "true_cipher_to_plaintext": {labels[i]: ALPHABET[int(true_decode[i])] for i in range(M)},
        "mean_recovered_held_cross_entropy": mean_rec,
        "mean_true_held_cross_entropy": mean_true,
        "mean_occurrence_weighted_key_accuracy": mean_weighted,
        "exact_recovered_key_recurrence": int(exact_rec),
        "folds": rows,
    }


def classify(pos, voy, baseline):
    if not pos["passed"]:
        return "SOLVER INADEQUATE", {"reason": "mandatory known-cipher positive control failed"}
    ce_ok = voy["pooled_held_cross_entropy"] <= baseline["mean_cross_entropy"] + 0.50
    stab_ok = voy["weighted_key_stability"] >= 0.90
    exact_ok = voy["exact_full_key_recurrence"] >= 3
    char_ok = voy["pooled_top5_char_fraction"] <= baseline["top5_char_fraction"] + 0.15
    lex_ok = voy["distinct_whole_token_hits_ge6_count"] >= 10 and len(voy["folds_with_hits_ge6"]) >= 3
    gates = {"ce": ce_ok, "weighted_stability": stab_ok, "exact_key_recurrence": exact_ok,
             "noncollapse": char_ok, "lexicon": lex_ok}
    if ce_ok and stab_ok and exact_ok and char_ok and lex_ok:
        return "LEON-LIKE MONOALPHABETIC PLAINTEXT LEAD", gates
    if ce_ok and (not stab_ok or not exact_ok):
        return "LATIN-LIKE BUT KEY-UNSTABLE", gates
    if stab_ok and exact_ok and (not ce_ok or not (char_ok and lex_ok)):
        return "STABLE NON-LANGUAGE OPTIMUM", gates
    return "NO READABLE LEON-LIKE MONOALPHABETIC PLAINTEXT", gates


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr)
        return 2
    zl = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")

    latin_runs, lexicon, latin_meta = load_latin(root)
    baseline = latin_self_baseline(latin_runs)
    lm = LM4(latin_runs)
    records, folds, labels, glyph_counts = build_voynich_records(zl)
    M = len(labels)
    total_events = sum(len(r["seq"]) for r in records)

    base_out = {
        "experiment": "Issue26E11 Leon-style musical-glyph monoalphabetic substitution probe",
        "representation": {
            "glyph_labels": labels, "glyph_count": M,
            "glyph_occurrences": {g: int(glyph_counts[g]) for g in labels},
            "total_glyph_events": total_events,
            "compounds": list(COMPOUNDS),
            "physical_line_count": len(records),
        },
        "latin_population": latin_meta,
        "latin_self_baseline": baseline,
        "optimizer": {"restarts": RESTARTS, "steps_per_restart": STEPS, "T0": T0, "T1": T1},
    }

    if M > A:
        base_out.update({"classification": "STRICT MODEL INAPPLICABLE",
                         "reason": f"Voynich grapheme alphabet M={M} exceeds plaintext alphabet A={A}"})
        json.dump(base_out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True); print()
        return 0

    pos = run_positive_control(latin_runs, labels, glyph_counts, lm, total_events)
    voy = run_voynich(records, folds, labels, glyph_counts, lm, lexicon)
    classification, gates = classify(pos, voy, baseline)
    base_out.update({"classification": classification, "classification_gates": gates,
                     "positive_control": pos, "voynich_primary": voy})
    json.dump(base_out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
