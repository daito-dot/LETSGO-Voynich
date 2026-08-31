#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

import issue26e_core as e

ALPHA = 0.1
CREMMA_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
SLOT3 = ("", "t", "k", "p", "f")
SLOT5 = ("", "cth", "ckh", "cph", "cfh")
# Historical families, pitch order low -> high. S3 p4=h is the preregistered
# computational completion of the sole unused note-system cell.
TABLE = (
    ("a", "e", "i", "o", "u"),
    ("l", "m", "n", "r", "s"),
    ("b", "c", "d", "f", "g"),
    ("t", "q", "p", "k", "h"),
    ("x", "y", "z", "et", "con"),
)


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
    return c


def load_latin(root: Path):
    runs = []
    lexicon = Counter()
    files = 0
    for rel in CREMMA_DIRS:
        d = root / rel
        if not d.is_dir():
            raise RuntimeError(f"missing CREMMA dir: {d}")
        for p in sorted(d.rglob("*.txt")):
            files += 1
            text = p.read_text(encoding="utf-8", errors="replace")
            for raw in text.splitlines():
                cur = []
                for ch in raw:
                    c = norm_letter(ch)
                    if c is None:
                        if len(cur) >= 4:
                            runs.append("".join(cur))
                        cur = []
                    else:
                        cur.append(c)
                if len(cur) >= 4:
                    runs.append("".join(cur))
            for tok in re.findall(r"[A-Za-zÀ-ÿ]+", text):
                w = "".join(c for c in (norm_letter(x) for x in tok) if c is not None)
                if len(w) >= 3:
                    lexicon[w] += 1
    if not runs:
        raise RuntimeError("no Latin runs")
    alphabet = tuple(sorted(set("".join(runs))))
    for row in TABLE:
        for out in row:
            for c in out:
                if c not in alphabet:
                    raise RuntimeError(f"Sloane output char {c!r} absent from frozen Latin alphabet {alphabet}")
    return runs, lexicon, alphabet, {
        "files": files,
        "runs": len(runs),
        "chars": sum(map(len, runs)),
        "lexicon": len(lexicon),
        "alphabet": "".join(alphabet),
    }


class LM4:
    def __init__(self, runs, alphabet):
        self.alphabet = tuple(alphabet)
        self.ai = {c: i for i, c in enumerate(self.alphabet)}
        self.A = len(self.alphabet)
        self.c3 = np.zeros(self.A ** 3, dtype=np.int64)
        self.c4 = np.zeros((self.A ** 3, self.A), dtype=np.int64)
        self.c4_counter = Counter()
        for s in runs:
            xs = [self.ai[c] for c in s]
            for i in range(3, len(xs)):
                h = (xs[i-3] * self.A + xs[i-2]) * self.A + xs[i-1]
                self.c3[h] += 1
                self.c4[h, xs[i]] += 1
                self.c4_counter[s[i-3:i+1]] += 1
        self.neglog = -np.log2((self.c4 + ALPHA) / (self.c3[:, None] + ALPHA * self.A))
        self._build_transducer()

    def _build_transducer(self):
        A = self.A
        off1 = 1
        off2 = off1 + A
        off3 = off2 + A * A
        nstates = off3 + A ** 3
        self.off = (0, off1, off2, off3)
        # state_len/context encodings for a compact <=3-char history automaton
        state_len = np.zeros(nstates, dtype=np.int8)
        state_code = np.zeros(nstates, dtype=np.int32)
        for c in range(A):
            state_len[off1 + c] = 1
            state_code[off1 + c] = c
        for q in range(A * A):
            state_len[off2 + q] = 2
            state_code[off2 + q] = q
        for q in range(A ** 3):
            state_len[off3 + q] = 3
            state_code[off3 + q] = q
        cells = [TABLE[s][p] for s in range(5) for p in range(5)]
        nxt = np.zeros((25, nstates), dtype=np.int32)
        cost = np.zeros((25, nstates), dtype=np.float64)
        cnt = np.zeros((25, nstates), dtype=np.int8)
        for cell, text in enumerate(cells):
            chars = [self.ai[c] for c in text]
            for st in range(nstates):
                ln = int(state_len[st]); code = int(state_code[st]); z = 0.0; n = 0
                for c in chars:
                    if ln == 0:
                        code = c; ln = 1
                    elif ln == 1:
                        code = code * A + c; ln = 2
                    elif ln == 2:
                        code = code * A + c; ln = 3
                    else:
                        z += float(self.neglog[code, c]); n += 1
                        code = ((code % (A * A)) * A) + c
                if ln == 0:
                    ns = 0
                elif ln == 1:
                    ns = off1 + code
                elif ln == 2:
                    ns = off2 + code
                else:
                    ns = off3 + code
                nxt[cell, st] = ns; cost[cell, st] = z; cnt[cell, st] = n
        self.next_state = nxt
        self.cost = cost
        self.count = cnt

    def score_texts(self, texts):
        nll = 0.0; n = 0
        for s in texts:
            if len(s) < 4:
                continue
            xs = [self.ai[c] for c in s]
            for i in range(3, len(xs)):
                h = (xs[i-3] * self.A + xs[i-2]) * self.A + xs[i-1]
                nll += float(self.neglog[h, xs[i]]); n += 1
        return (nll / n if n else float("inf")), n


def latin_self_baseline(runs, alphabet):
    rows = []
    for f in range(5):
        train = [s for i, s in enumerate(runs) if i % 5 != f]
        held = [s for i, s in enumerate(runs) if i % 5 == f]
        lm = LM4(train, alphabet)
        ce, n = lm.score_texts(held)
        rows.append({"fold": f, "cross_entropy": ce, "scored_chars": n})
    return {"mean_cross_entropy": statistics.fmean(r["cross_entropy"] for r in rows), "folds": rows}


def raw_streams(items, leaves, parser, policy):
    out = []
    meta = []
    i3 = {v:i for i,v in enumerate(SLOT3)}
    i5 = {v:i for i,v in enumerate(SLOT5)}
    for it in items:
        if it["leaf"] not in leaves:
            continue
        for li, line in enumerate(it["lines"]):
            cur = []
            def flush():
                nonlocal cur
                if cur:
                    out.append(np.asarray(cur, dtype=np.uint8))
                    meta.append({"page": it["page"], "paragraph": it["id"], "line_index": li})
                cur = []
            for tok in line:
                p = parser.pick(tok, policy)
                if p is None:
                    flush(); continue
                vals = p[1]
                cur.append(i3[vals[3]] * 5 + i5[vals[5]])
            flush()
    return out, meta


def key_matrix():
    perms = np.asarray(list(itertools.permutations(range(5))), dtype=np.uint8)
    style = np.repeat(perms, len(perms), axis=0)
    pitch = np.tile(perms, (len(perms), 1))
    blocks = []
    axes = []
    spi = []
    ppi = []
    for axis in (0, 1):
        M = np.empty((len(style), 25), dtype=np.uint8)
        for r3 in range(5):
            for r5 in range(5):
                raw = r3 * 5 + r5
                if axis == 0:
                    M[:, raw] = style[:, r3] * 5 + pitch[:, r5]
                else:
                    M[:, raw] = style[:, r5] * 5 + pitch[:, r3]
        blocks.append(M)
        axes.extend([axis] * len(style))
        spi.extend(np.repeat(np.arange(120), 120).tolist())
        ppi.extend(np.tile(np.arange(120), 120).tolist())
    return np.vstack(blocks), perms, np.asarray(axes), np.asarray(spi), np.asarray(ppi)


def score_all_keys(streams, M, lm):
    K = M.shape[0]
    nll = np.zeros(K, dtype=np.float64)
    cnt = np.zeros(K, dtype=np.int64)
    rows = np.arange(K)
    for s in streams:
        state = np.zeros(K, dtype=np.int32)
        for raw in s:
            cell = M[:, int(raw)]
            nll += lm.cost[cell, state]
            cnt += lm.count[cell, state]
            state = lm.next_state[cell, state]
    return nll, cnt


def key_desc(k, perms, axes, spi, ppi):
    axis = int(axes[k])
    return {
        "key_index": int(k),
        "style_slot": 3 if axis == 0 else 5,
        "pitch_slot": 5 if axis == 0 else 3,
        "style_perm": perms[int(spi[k])].tolist(),
        "pitch_perm": perms[int(ppi[k])].tolist(),
    }


def literal_key_indices(perms, axes, spi, ppi):
    identity = tuple(range(5)); reverse = tuple(reversed(range(5)))
    pi = {tuple(p): i for i,p in enumerate(perms.tolist())}
    out = []
    for axis in (0, 1):
        for pitch_tuple, name in ((identity, "grammar_pitch_order"), (reverse, "reversed_pitch_order")):
            idx = np.flatnonzero((axes == axis) & (spi == pi[identity]) & (ppi == pi[pitch_tuple]))
            if len(idx) != 1:
                raise RuntimeError("literal key lookup failed")
            out.append((int(idx[0]), name))
    return out


def decode_one(raw, k, M):
    cells = M[k, raw]
    return "".join(TABLE[int(c)//5][int(c)%5] for c in cells)


def decoded_population(streams, meta, k, M):
    texts = []
    rows = []
    for s, m in zip(streams, meta):
        text = decode_one(s, k, M)
        texts.append(text)
        rows.append({**m, "text": text})
    return texts, rows


def lexicon_hits(rows, lexicon, cap=50):
    hits = []
    seen = set()
    for m in rows:
        s = m["text"]
        for i in range(len(s)):
            for j in range(i+4, min(len(s), i+18)+1):
                w = s[i:j]; freq = lexicon.get(w, 0)
                if not freq:
                    continue
                key = (w, m["page"], m["line_index"], i)
                if key in seen:
                    continue
                seen.add(key)
                hits.append({"word": w, "length": len(w), "corpus_frequency": int(freq),
                             "page": m["page"], "line_index": m["line_index"], "offset": i,
                             "context": s[max(0,i-12):min(len(s),j+12)]})
    hits.sort(key=lambda z: (-z["length"], -z["corpus_frequency"], z["word"], z["page"], z["line_index"], z["offset"]))
    return hits[:cap]


def diagnostics(texts, rows, lm, lexicon):
    ce, n = lm.score_texts(texts)
    chars = Counter("".join(texts))
    total = sum(chars.values())
    top5 = sum(v for _,v in chars.most_common(5)) / total if total else 1.0
    grams = Counter()
    for s in texts:
        grams.update(s[i:i+4] for i in range(len(s)-3))
    samples = [m for m in rows if len(m["text"]) >= 12][:20]
    hits = lexicon_hits(rows, lexicon)
    return {
        "cross_entropy": ce,
        "scored_chars": n,
        "decoded_chars": total,
        "streams": len(texts),
        "top5_char_fraction": top5,
        "char_counts": dict(chars.most_common()),
        "samples": samples,
        "lexicon_hits": hits,
        "distinct_lexicon_hits_ge6": len({h["word"] for h in hits if h["length"] >= 6}),
        "top_4grams": [{"ngram": q, "decoded_count": int(c), "latin_count": int(lm.c4_counter.get(q,0))}
                       for q,c in grams.most_common(50)],
    }


def run_policy(items, parser, policy, lm, lexicon, M, perms, axes, spi, ppi):
    folds = e.physical_leaf_folds(items)
    universe = set().union(*folds)
    fs = []
    for held in folds:
        streams, meta = raw_streams(items, held, parser, policy)
        nll, cnt = score_all_keys(streams, M, lm)
        fs.append({"held": held, "streams": streams, "meta": meta, "nll": nll, "cnt": cnt})
    total_nll = sum(x["nll"] for x in fs)
    total_cnt = sum(x["cnt"] for x in fs)

    # Track A: exact deterministic conventions on all eligible-fold leaves.
    track_a = []
    all_streams = sum((x["streams"] for x in fs), [])
    all_meta = sum((x["meta"] for x in fs), [])
    for k, label in literal_key_indices(perms, axes, spi, ppi):
        texts, rows = decoded_population(all_streams, all_meta, k, M)
        track_a.append({"label": label, "key": key_desc(k, perms, axes, spi, ppi),
                        "diagnostics": diagnostics(texts, rows, lm, lexicon)})

    # Track B: exhaustive 28,800-key training selection, held-out decode.
    fold_rows = []
    selected = []
    all_held_texts = []
    all_held_rows = []
    for f, x in enumerate(fs):
        tr_nll = total_nll - x["nll"]
        tr_cnt = total_cnt - x["cnt"]
        ce = np.divide(tr_nll, tr_cnt, out=np.full_like(tr_nll, np.inf), where=tr_cnt>0)
        k = int(np.argmin(ce)); selected.append(k)
        texts, rows = decoded_population(x["streams"], x["meta"], k, M)
        dg = diagnostics(texts, rows, lm, lexicon)
        fold_rows.append({"fold": f, "held_leaves": sorted(x["held"]),
                          "training_cross_entropy": float(ce[k]),
                          "key": key_desc(k, perms, axes, spi, ppi),
                          "held": dg})
        all_held_texts.extend(texts); all_held_rows.extend(rows)
    rec = Counter(selected)
    rk, rc = min(rec.items(), key=lambda kv: (-kv[1], kv[0]))
    weighted_nll = sum(float(fs[f]["nll"][selected[f]]) for f in range(5))
    weighted_cnt = sum(int(fs[f]["cnt"][selected[f]]) for f in range(5))
    track_b = {
        "mean_fold_cross_entropy": statistics.fmean(r["held"]["cross_entropy"] for r in fold_rows),
        "pooled_cross_entropy": weighted_nll / weighted_cnt,
        "exact_key_recurrence": int(rc),
        "most_recurrent_key": key_desc(int(rk), perms, axes, spi, ppi),
        "folds": fold_rows,
        "pooled_diagnostics_using_fold_specific_keys": diagnostics(all_held_texts, all_held_rows, lm, lexicon),
    }
    return {"policy": policy, "track_a_literal": track_a, "track_b_fitted": track_b}


def classify(primary, baseline):
    base = baseline["mean_cross_entropy"]
    direct = []
    for row in primary["track_a_literal"]:
        d = row["diagnostics"]
        if d["cross_entropy"] <= base + 0.30 and d["distinct_lexicon_hits_ge6"] >= 10 and d["top5_char_fraction"] < 0.80:
            direct.append(row["label"])
    if direct:
        return "DIRECT SLOANE PLAINTEXT LEAD", {"direct_conventions": direct}
    b = primary["track_b_fitted"]
    d = b["pooled_diagnostics_using_fold_specific_keys"]
    if (b["exact_key_recurrence"] >= 4 and b["pooled_cross_entropy"] <= base + 0.50 and
        d["distinct_lexicon_hits_ge6"] >= 10 and d["top5_char_fraction"] < 0.80):
        return "FITTED SLOANE PLAINTEXT LEAD", {}
    return "NO READABLE SLOANE PLAINTEXT", {}


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr); return 2
    zl = Path(sys.argv[1]).resolve(); root = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")
    parser = e.SlotParser(); validation = e.validate_parser(parser)
    items = e.parse_voynich(zl)
    runs, lexicon, alphabet, lmeta = load_latin(root)
    baseline = latin_self_baseline(runs, alphabet)
    lm = LM4(runs, alphabet)
    M, perms, axes, spi, ppi = key_matrix()
    primary = run_policy(items, parser, "min", lm, lexicon, M, perms, axes, spi, ppi)
    sensitivity = run_policy(items, parser, "max", lm, lexicon, M, perms, axes, spi, ppi)
    classification, extra = classify(primary, baseline)
    out = {
        "experiment": "Issue26E10 Sloane 351 late-medieval musical-cipher plaintext probe",
        "classification": classification,
        "classification_detail": extra,
        "historical_table_low_to_high": [list(x) for x in TABLE],
        "h_completion_note": "S3/p4=h is computational completion of the unique unused 5x5 note cell, not a historical note assignment.",
        "latin_population": lmeta,
        "latin_self_baseline": baseline,
        "candidate_keys": int(M.shape[0]),
        "slot_parser_validation": validation,
        "primary_min": primary,
        "max_sensitivity": sensitivity,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print(); return 0


if __name__ == "__main__":
    raise SystemExit(main())
