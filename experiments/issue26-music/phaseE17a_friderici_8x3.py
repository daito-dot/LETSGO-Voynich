#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment

import issue26e_core as e
import phaseE15_bacon_biliteral_carrier as b

ALPHABET = b.ALPHABET
AI = b.AI
A = len(ALPHABET)
ALPHA = b.ALPHA
assert A == 24

# Friderici 8 x 3 row-major table after j->i, v->u normalization.
TABLE = (
    ("a", "b", "c"),
    ("d", "e", "f"),
    ("g", "h", "i"),
    ("k", "l", "m"),
    ("n", "o", "p"),
    ("q", "r", "s"),
    ("t", "u", "w"),
    ("x", "y", "z"),
)
TABLE_INDEX = np.asarray([[AI[c] for c in row] for row in TABLE], dtype=np.int16)
assert np.array_equal(TABLE_INDEX, np.arange(24, dtype=np.int16).reshape(8, 3))

FOUR_SLOTS = {
    0: ("", "q", "s", "d"),
    6: ("", "e", "ee", "eee"),
    9: ("", "i", "ii", "iii"),
}
BIN_SLOT = 11
BIN_STATES = ("", "y")
REP_SLOTS = {
    1: ("", "o", "y"),
    2: ("", "l", "r"),
    4: ("", "ch", "sh"),
    7: ("", "s", "d"),
    8: ("", "o", "a"),
}
REPRESENTATIONS = tuple((fs, rs) for fs in sorted(FOUR_SLOTS) for rs in sorted(REP_SLOTS))
COL_PERMS = tuple(itertools.permutations(range(3)))
ROW_SWAP_PAIRS = tuple(itertools.combinations(range(8), 2))
COL_SWAP_PAIRS = tuple(itertools.combinations(range(3), 2))
N_RANDOM_STARTS = 6
SCORE_TOL = 1e-10
assert len(REPRESENTATIONS) == 15 and len(COL_PERMS) == 6


def seed32(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:4], "big") & 0x7fffffff


def key_tuple(row_perm, col_perm):
    return tuple(int(x) for x in row_perm), tuple(int(x) for x in col_perm)


def mapping_from_key(row_perm, col_perm):
    row = np.asarray(row_perm, dtype=np.int16)
    col = np.asarray(col_perm, dtype=np.int16)
    raw = np.arange(24, dtype=np.int16)
    rr = raw // 3
    cc = raw % 3
    return (row[rr] * 3 + col[cc]).astype(np.int16)


def raw_runs_from_feature_runs(feature_runs, four_slot, rep_slot):
    out = []
    for r in feature_runs:
        four = r["four"][four_slot]
        binary = r["binary"]
        rep = r["rep"][rep_slot]
        row = four.astype(np.int16) * 2 + binary.astype(np.int16)
        cell = row * 3 + rep.astype(np.int16)
        q = dict(r)
        q["cells"] = cell.astype(np.int16)
        out.append(q)
    return out


def build_feature_runs(items, leaves, parser, policy):
    four_index = {s: {v: i for i, v in enumerate(states)} for s, states in FOUR_SLOTS.items()}
    rep_index = {s: {v: i for i, v in enumerate(states)} for s, states in REP_SLOTS.items()}
    bin_index = {v: i for i, v in enumerate(BIN_STATES)}
    out = []
    visible = parsed = 0

    for it in items:
        if it["leaf"] not in leaves:
            continue
        cur = []
        run_index = 0

        def flush():
            nonlocal cur, run_index
            if cur:
                four = {s: np.asarray([x[0][s] for x in cur], dtype=np.uint8) for s in FOUR_SLOTS}
                binary = np.asarray([x[1] for x in cur], dtype=np.uint8)
                rep = {s: np.asarray([x[2][s] for x in cur], dtype=np.uint8) for s in REP_SLOTS}
                out.append({
                    "leaf": it["leaf"],
                    "page": it["page"],
                    "paragraph": it["id"],
                    "run_index": run_index,
                    "four": four,
                    "binary": binary,
                    "rep": rep,
                })
                run_index += 1
            cur = []

        for line in it["lines"]:
            for tok in line:
                visible += 1
                p = parser.pick(tok, policy)
                if p is None:
                    flush()
                    continue
                vals = p[1]
                try:
                    fv = {s: four_index[s][vals[s]] for s in FOUR_SLOTS}
                    bv = bin_index[vals[BIN_SLOT]]
                    rv = {s: rep_index[s][vals[s]] for s in REP_SLOTS}
                except KeyError as ex:
                    raise RuntimeError(f"unexpected E17 slot state in token {tok!r}: {ex}") from ex
                cur.append((fv, bv, rv))
                parsed += 1
        flush()

    return out, {
        "visible_tokens": int(visible),
        "parsed_tokens": int(parsed),
        "parse_coverage": parsed / visible if visible else 0.0,
        "scoring_runs": len(out),
        "carrier_tokens": int(sum(len(x["binary"]) for x in out)),
    }


def cell_counts(raw_runs):
    c = np.zeros(24, dtype=np.int64)
    for r in raw_runs:
        c += np.bincount(r["cells"].astype(np.int64), minlength=24)
    return c


def pattern_counts(raw_runs):
    qcount = np.zeros(24 ** 4, dtype=np.int64)
    for r in raw_runs:
        x = r["cells"].astype(np.int64)
        if len(x) < 4:
            continue
        q = (((x[:-3] * 24 + x[1:-2]) * 24 + x[2:-1]) * 24 + x[3:])
        qcount += np.bincount(q, minlength=24 ** 4)
    nz = np.flatnonzero(qcount)
    if not len(nz):
        raise RuntimeError("no E17 raw-cell tetragrams")
    z = nz.copy()
    d = z % 24; z //= 24
    c = z % 24; z //= 24
    bb = z % 24; z //= 24
    a = z % 24
    pats = np.stack([a, bb, c, d], axis=1).astype(np.int16)
    cnt = qcount[nz].astype(np.int64)
    return pats, cnt


def score_mapping(mapping, pats, counts, lm_cost):
    a = mapping[pats[:, 0]].astype(np.int64)
    bb = mapping[pats[:, 1]].astype(np.int64)
    c = mapping[pats[:, 2]].astype(np.int64)
    d = mapping[pats[:, 3]].astype(np.int64)
    q = (((a * A + bb) * A + c) * A + d)
    n = int(counts.sum())
    nll = float(np.dot(counts.astype(np.float64), lm_cost[q]))
    return nll / n, nll, n


def score_many(mappings, pats, counts, lm_cost):
    # mappings: K x 24
    a = mappings[:, pats[:, 0]].astype(np.int64)
    bb = mappings[:, pats[:, 1]].astype(np.int64)
    c = mappings[:, pats[:, 2]].astype(np.int64)
    d = mappings[:, pats[:, 3]].astype(np.int64)
    q = (((a * A + bb) * A + c) * A + d)
    n = float(counts.sum())
    return (lm_cost[q] * counts[None, :]).sum(axis=1) / n


def independent_run_score(mapping, raw_runs, lm):
    decoded = [mapping[r["cells"]].astype(np.int16) for r in raw_runs]
    ce, n, _ = lm.score_code_runs(decoded)
    return float(ce), int(n)


def unigram_informed_starts(raw_counts, latin_counts):
    total = float(sum(latin_counts.values()))
    probs = np.asarray([(latin_counts[c] + ALPHA) / (total + ALPHA * A) for c in ALPHABET], dtype=np.float64)
    letter_cost = -np.log2(probs)
    starts = []
    for col_perm in COL_PERMS:
        C = np.zeros((8, 8), dtype=np.float64)
        for raw_row in range(8):
            for hist_row in range(8):
                z = 0.0
                for raw_col in range(3):
                    raw_cell = raw_row * 3 + raw_col
                    hist_cell = hist_row * 3 + int(col_perm[raw_col])
                    z += float(raw_counts[raw_cell]) * float(letter_cost[hist_cell])
                C[raw_row, hist_row] = z
        rr, cc = linear_sum_assignment(C)
        row_perm = np.empty(8, dtype=np.int16)
        row_perm[rr] = cc
        starts.append((row_perm, np.asarray(col_perm, dtype=np.int16), "unigram"))
    return starts


def random_starts(label):
    out = []
    for restart in range(N_RANDOM_STARTS):
        rng = np.random.default_rng(seed32(f"Issue26E17A:Restart:v1:{label}:{restart}"))
        row = np.arange(8, dtype=np.int16); rng.shuffle(row)
        col = np.arange(3, dtype=np.int16); rng.shuffle(col)
        out.append((row, col, "random"))
    return out


def neighbor_keys(row_perm, col_perm):
    keys = []
    for a, bb in ROW_SWAP_PAIRS:
        r = row_perm.copy(); r[a], r[bb] = r[bb], r[a]
        keys.append((r, col_perm.copy(), "row", a, bb))
    for a, bb in COL_SWAP_PAIRS:
        c = col_perm.copy(); c[a], c[bb] = c[bb], c[a]
        keys.append((row_perm.copy(), c, "col", a, bb))
    return keys


def hill_climb(start_row, start_col, pats, counts, lm, raw_runs):
    row = start_row.copy(); col = start_col.copy()
    mapping = mapping_from_key(row, col)
    current, _, _ = score_mapping(mapping, pats, counts, lm.cost)
    accepted = 0
    max_verify_diff = 0.0

    while True:
        neigh = neighbor_keys(row, col)
        maps = np.stack([mapping_from_key(r, c) for r, c, *_ in neigh])
        scores = score_many(maps, pats, counts, lm.cost)
        best_i = min(
            range(len(neigh)),
            key=lambda i: (float(scores[i]), tuple(int(x) for x in neigh[i][0]), tuple(int(x) for x in neigh[i][1])),
        )
        best_score = float(scores[best_i])
        if best_score >= current - 1e-12:
            break
        row = neigh[best_i][0].copy(); col = neigh[best_i][1].copy()
        mapping = maps[best_i].copy()
        verify, vn = independent_run_score(mapping, raw_runs, lm)
        diff = abs(verify - best_score)
        max_verify_diff = max(max_verify_diff, diff)
        if diff > SCORE_TOL:
            raise RuntimeError(f"accepted-move full-score verification failure {diff}")
        if vn != int(counts.sum()):
            raise RuntimeError("accepted-move scored-char mismatch")
        current = best_score
        accepted += 1
        if accepted > 200:
            raise RuntimeError("unexpectedly long E17 hill climb")

    return {
        "row_perm": row,
        "col_perm": col,
        "training_cross_entropy": float(current),
        "accepted_swaps": int(accepted),
        "max_verify_diff": float(max_verify_diff),
    }


def fit_product_key(raw_runs, lm, latin_counts, label):
    pats, counts = pattern_counts(raw_runs)
    raw_counts = cell_counts(raw_runs)
    starts = unigram_informed_starts(raw_counts, latin_counts) + random_starts(label)
    # Deduplicate without changing first occurrence/order.
    seen = set(); uniq = []
    for row, col, kind in starts:
        k = key_tuple(row, col)
        if k in seen:
            continue
        seen.add(k); uniq.append((row, col, kind))

    finals = []
    for si, (row, col, kind) in enumerate(uniq):
        z = hill_climb(row, col, pats, counts, lm, raw_runs)
        z["start_index"] = si
        z["start_kind"] = kind
        finals.append(z)
    best = min(
        finals,
        key=lambda z: (
            z["training_cross_entropy"],
            tuple(int(x) for x in z["row_perm"]),
            tuple(int(x) for x in z["col_perm"]),
        ),
    )
    return {
        "row_perm": [int(x) for x in best["row_perm"]],
        "col_perm": [int(x) for x in best["col_perm"]],
        "training_cross_entropy": float(best["training_cross_entropy"]),
        "accepted_swaps": int(best["accepted_swaps"]),
        "max_verify_diff": float(max(z["max_verify_diff"] for z in finals)),
        "distinct_starts": len(uniq),
        "final_local_optima": [
            {
                "row_perm": [int(x) for x in z["row_perm"]],
                "col_perm": [int(x) for x in z["col_perm"]],
                "training_cross_entropy": float(z["training_cross_entropy"]),
                "accepted_swaps": int(z["accepted_swaps"]),
                "start_kind": z["start_kind"],
            }
            for z in finals
        ],
    }


def decode_raw_runs(raw_runs, row_perm, col_perm, fold=None):
    mapping = mapping_from_key(row_perm, col_perm)
    out = []
    for r in raw_runs:
        codes = mapping[r["cells"]].astype(np.int16)
        out.append({
            "fold": fold,
            "leaf": r.get("leaf"),
            "page": r.get("page"),
            "paragraph": r.get("paragraph"),
            "run_index": r.get("run_index"),
            "codes": codes,
            "text": "".join(ALPHABET[int(x)] for x in codes),
        })
    return out


def lexicon_hits(decoded_rows, lexicon, cap=500):
    hits = []
    seen = set()
    for r in decoded_rows:
        s = r["text"]
        for i in range(len(s)):
            for ln in range(4, min(15, len(s) - i) + 1):
                w = s[i:i+ln]
                freq = int(lexicon.get(w, 0))
                if not freq:
                    continue
                key = (r["fold"], r["page"], r["paragraph"], r["run_index"], i, w)
                if key in seen:
                    continue
                seen.add(key)
                hits.append({
                    "fold": r["fold"], "word": w, "length": ln, "corpus_frequency": freq,
                    "page": r["page"], "paragraph": r["paragraph"], "run_index": r["run_index"],
                    "offset": i, "context": s[max(0, i-12):min(len(s), i+ln+12)],
                })
    hits.sort(key=lambda h: (-h["length"], -h["corpus_frequency"], h["word"], h["fold"], h["page"] or "", h["offset"]))
    return hits[:cap]


def diagnostics(decoded_rows, lm, lexicon):
    code_runs = [r["codes"] for r in decoded_rows]
    ce, n, nll = lm.score_code_runs(code_runs)
    chars = Counter("".join(r["text"] for r in decoded_rows))
    total = sum(chars.values())
    top5 = sum(v for _, v in chars.most_common(5)) / total if total else 1.0
    grams = Counter()
    for r in decoded_rows:
        s = r["text"]
        grams.update(s[i:i+4] for i in range(max(0, len(s)-3)))
    hits = lexicon_hits(decoded_rows, lexicon)
    d6 = sorted({h["word"] for h in hits if h["length"] >= 6})
    folds6 = sorted({int(h["fold"]) for h in hits if h["length"] >= 6 and h["fold"] is not None})
    return {
        "cross_entropy": float(ce),
        "nll": float(nll),
        "scored_chars": int(n),
        "decoded_chars": int(total),
        "top5_char_fraction": float(top5),
        "char_counts": dict(chars.most_common()),
        "samples": [
            {k: r[k] for k in ("fold", "page", "paragraph", "run_index", "text")}
            for r in decoded_rows if len(r["text"]) >= 12
        ][:20],
        "lexicon_hits": hits,
        "distinct_words_ge6": d6,
        "distinct_words_ge6_count": len(d6),
        "word_folds_ge6": folds6,
        "top_4grams": [
            {"ngram": g, "decoded_count": int(c), "latin_count": int(lm.c4_counter.get(g, 0))}
            for g, c in grams.most_common(50)
        ],
    }


def fit_target_policy(items, parser, policy, lm, latin_counts, lexicon):
    folds = e.physical_leaf_folds(items)
    universe = set().union(*folds)
    feature_runs, meta = build_feature_runs(items, universe, parser, policy)
    fold_rows = []
    selected_keys = []
    decoded_all = []
    max_verify_diff = 0.0

    for fi, held in enumerate(folds):
        train_leaves = universe - held
        candidates = []
        for four_slot, rep_slot in REPRESENTATIONS:
            all_raw = raw_runs_from_feature_runs(feature_runs, four_slot, rep_slot)
            train_raw = [r for r in all_raw if r["leaf"] in train_leaves]
            label = f"four{four_slot}-rep{rep_slot}:fold{fi}"
            fit = fit_product_key(train_raw, lm, latin_counts, label)
            max_verify_diff = max(max_verify_diff, fit["max_verify_diff"])
            candidates.append({
                "four_slot": four_slot,
                "rep_slot": rep_slot,
                "fit": fit,
                "all_raw": all_raw,
            })
        best = min(
            candidates,
            key=lambda z: (
                z["fit"]["training_cross_entropy"],
                z["four_slot"], z["rep_slot"],
                tuple(z["fit"]["row_perm"]), tuple(z["fit"]["col_perm"]),
            ),
        )
        row_perm = best["fit"]["row_perm"]
        col_perm = best["fit"]["col_perm"]
        held_raw = [r for r in best["all_raw"] if r["leaf"] in held]
        held_decoded = decode_raw_runs(held_raw, row_perm, col_perm, fold=fi)
        hd = diagnostics(held_decoded, lm, lexicon)
        key = (best["four_slot"], best["rep_slot"], tuple(row_perm), tuple(col_perm))
        selected_keys.append(key)
        decoded_all.extend(held_decoded)
        fold_rows.append({
            "fold": fi,
            "held_leaves": sorted(held),
            "four_slot": best["four_slot"],
            "repetition_slot": best["rep_slot"],
            "row_perm": row_perm,
            "col_perm": col_perm,
            "training_cross_entropy": best["fit"]["training_cross_entropy"],
            "accepted_swaps": best["fit"]["accepted_swaps"],
            "distinct_starts": best["fit"]["distinct_starts"],
            "held_cross_entropy": hd["cross_entropy"],
            "held_scored_chars": hd["scored_chars"],
            "held_decoded_chars": hd["decoded_chars"],
            "held_top5_char_fraction": hd["top5_char_fraction"],
        })

    rec = Counter(selected_keys)
    modal, recurrence = min(rec.items(), key=lambda kv: (-kv[1], kv[0]))
    pooled = diagnostics(decoded_all, lm, lexicon)
    return {
        "policy": policy,
        "population": meta,
        "folds": fold_rows,
        "selected_keys": [
            {"four_slot": k[0], "repetition_slot": k[1], "row_perm": list(k[2]), "col_perm": list(k[3])}
            for k in selected_keys
        ],
        "exact_key_recurrence": int(recurrence),
        "modal_key": {
            "four_slot": modal[0], "repetition_slot": modal[1],
            "row_perm": list(modal[2]), "col_perm": list(modal[3]),
        },
        "diagnostics": pooled,
        "max_accepted_move_verify_diff": float(max_verify_diff),
    }


def take_positive_plain_runs(latin_runs, target=40000):
    out = []
    total = 0
    for s in latin_runs:
        if total >= target:
            break
        take = min(len(s), target - total)
        if take >= 4:
            out.append(s[:take])
            total += take
        elif take > 0 and out:
            # Keep the 4-gram boundary model intact: do not create a <4 fragment.
            need = take
            out[-1] += s[:need]
            total += need
    if total != target:
        raise RuntimeError(f"positive population size {total} != {target}")
    return out


def encode_plain_runs(plain_runs, row_perm, col_perm):
    inv_row = np.empty(8, dtype=np.int16)
    inv_col = np.empty(3, dtype=np.int16)
    for raw, hist in enumerate(row_perm): inv_row[int(hist)] = raw
    for raw, hist in enumerate(col_perm): inv_col[int(hist)] = raw
    raw_runs = []
    plain_codes = []
    for ri, s in enumerate(plain_runs):
        pc = np.asarray([AI[c] for c in s], dtype=np.int16)
        hist_row = pc // 3; hist_col = pc % 3
        raw = inv_row[hist_row] * 3 + inv_col[hist_col]
        raw_runs.append({"leaf": ri, "page": None, "paragraph": None, "run_index": ri, "cells": raw.astype(np.int16)})
        plain_codes.append(pc)
    return raw_runs, plain_codes


def positive_control(latin_runs, lm, latin_counts):
    plain_runs = take_positive_plain_runs(latin_runs, 40000)
    rows = []
    exact = 0
    accs = []
    max_ce_diff = 0.0
    max_verify_diff = 0.0

    for ci, col_perm_tuple in enumerate(COL_PERMS):
        for rep in range(2):
            rng = np.random.default_rng(seed32(f"Issue26E17A:PositiveRow:v1:{ci}:{rep}"))
            hidden_row = np.arange(8, dtype=np.int16); rng.shuffle(hidden_row)
            hidden_col = np.asarray(col_perm_tuple, dtype=np.int16)
            raw_runs, plain_codes = encode_plain_runs(plain_runs, hidden_row, hidden_col)
            case_folds = [set(range(f, len(raw_runs), 5)) for f in range(5)]
            case_rows = []
            for f, held_ids in enumerate(case_folds):
                train_raw = [r for r in raw_runs if r["leaf"] not in held_ids]
                held_raw = [r for r in raw_runs if r["leaf"] in held_ids]
                label = f"positive-c{ci}-r{rep}:fold{f}"
                fit = fit_product_key(train_raw, lm, latin_counts, label)
                max_verify_diff = max(max_verify_diff, fit["max_verify_diff"])
                got_row = np.asarray(fit["row_perm"], dtype=np.int16)
                got_col = np.asarray(fit["col_perm"], dtype=np.int16)
                is_exact = np.array_equal(got_row, hidden_row) and np.array_equal(got_col, hidden_col)
                exact += int(is_exact)

                mapping = mapping_from_key(got_row, got_col)
                true_mapping = mapping_from_key(hidden_row, hidden_col)
                decoded = [mapping[r["cells"]] for r in held_raw]
                true_decoded = [true_mapping[r["cells"]] for r in held_raw]
                n = sum(len(x) for x in decoded)
                correct = sum(int(np.count_nonzero(a == bb)) for a, bb in zip(decoded, true_decoded))
                acc = correct / n if n else 0.0
                accs.append(acc)
                got_ce, _, _ = lm.score_code_runs(decoded)
                true_ce, _, _ = lm.score_code_runs(true_decoded)
                ce_diff = abs(got_ce - true_ce)
                max_ce_diff = max(max_ce_diff, ce_diff)
                case_rows.append({
                    "fold": f,
                    "exact_key": bool(is_exact),
                    "decoded_accuracy": float(acc),
                    "recovered_ce": float(got_ce),
                    "true_ce": float(true_ce),
                    "ce_abs_diff": float(ce_diff),
                    "row_perm": fit["row_perm"],
                    "col_perm": fit["col_perm"],
                    "accepted_swaps": fit["accepted_swaps"],
                })
            rows.append({
                "case": f"c{ci}-r{rep}",
                "hidden_row_perm": hidden_row.tolist(),
                "hidden_col_perm": hidden_col.tolist(),
                "folds": case_rows,
            })

    passed = exact == 60 and min(accs) == 1.0 and max_ce_diff <= 1e-10 and max_verify_diff <= SCORE_TOL
    return {
        "passed": bool(passed),
        "exact_key_folds": int(exact),
        "total_folds": 60,
        "min_decoded_accuracy": float(min(accs)),
        "mean_decoded_accuracy": float(statistics.fmean(accs)),
        "max_ce_abs_diff": float(max_ce_diff),
        "max_accepted_move_verify_diff": float(max_verify_diff),
        "cases": rows,
    }


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr)
        return 2

    zl = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    data = zl.read_bytes()
    if e.git_blob_sha1(data) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("frozen ZL3b blob mismatch")

    items = e.parse_voynich(zl)
    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)
    latin_runs, lexicon, latin_meta = b.load_latin(root)
    latin_counts = Counter("".join(latin_runs))
    lm = b.LM4(latin_runs)
    baseline = b.latin_self_baseline(latin_runs)

    pc = positive_control(latin_runs, lm, latin_counts)
    if not pc["passed"]:
        out = {
            "experiment": "Issue26E17A Friderici 8x3 triadic/motif plaintext probe",
            "classification": "SOLVER INADEQUATE",
            "positive_control": pc,
            "latin_self_baseline": baseline,
            "latin_population": latin_meta,
            "parser_validation": parser_validation,
            "representations": [list(x) for x in REPRESENTATIONS],
        }
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        print()
        return 0

    primary = fit_target_policy(items, parser, "min", lm, latin_counts, lexicon)
    d = primary["diagnostics"]
    gates = {
        "exact_complete_key_recurrence_ge4of5": primary["exact_key_recurrence"] >= 4,
        "held_ce_within_latin_plus_0_50": d["cross_entropy"] <= baseline["mean_cross_entropy"] + 0.50,
        "top5_within_latin_plus_0_15": d["top5_char_fraction"] <= baseline["pooled_top5_char_fraction"] + 0.15,
        "at_least_10_distinct_cremma_substrings_ge6": d["distinct_words_ge6_count"] >= 10,
        "ge6_hits_across_at_least_3_folds": len(d["word_folds_ge6"]) >= 3,
        "all_fold_parse_coverage_ge_0_70": primary["population"]["parse_coverage"] >= 0.70,
    }
    lead = all(gates.values())
    classification = "FRIDERICI 8x3 PLAINTEXT LEAD" if lead else "NO READABLE FRIDERICI 8x3 PLAINTEXT"

    max_sensitivity = fit_target_policy(items, parser, "max", lm, latin_counts, lexicon)

    out = {
        "experiment": "Issue26E17A Friderici 8x3 triadic/motif plaintext probe",
        "classification": classification,
        "positive_control": pc,
        "historical_table": [list(r) for r in TABLE],
        "representations": [list(x) for x in REPRESENTATIONS],
        "primary_min": primary,
        "gates": gates,
        "stage_b_required_if_lead": bool(lead),
        "max_sensitivity": max_sensitivity,
        "latin_self_baseline": baseline,
        "latin_population": latin_meta,
        "parser_validation": parser_validation,
        "source": {
            "zl3b_git_blob": e.EXPECTED_ZL3B_BLOB,
            "cremma_commit": "292525969ad98380b398e6606a9c2a36d51913ae",
        },
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
