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

import issue26e_core as e

ALPHABET = tuple("abcdefgiklmnopqrstuz")
# Historical Philip alphabet as low->high pitch rank within each duration class.
TABLE = (
    tuple("aeiou"),
    tuple("gfdcb"),
    tuple("klmnp"),
    tuple("ztsrq"),
)
DURATION_STATES = ("", "q", "s", "d")
DURATION_TO_GROUP = (0, 3, 1, 2)  # frozen E8-A min key, raw slot0 index -> Philip duration group
PITCH_STATES = {
    3: ("", "t", "k", "p", "f"),
    5: ("", "cth", "ckh", "cph", "cfh"),
}
CREMMA_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
ALPHA = 0.1


def norm_char(ch: str):
    s = unicodedata.normalize("NFKD", ch.lower())
    s = "".join(c for c in s if "a" <= c <= "z")
    if not s:
        return None
    c = s[0]
    if c == "j": c = "i"
    elif c == "v": c = "u"
    return c


def latin_runs_and_lexicon(root: Path):
    runs = []
    words = Counter()
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
                    if c is None:
                        if len(cur) >= 4: runs.append("".join(cur))
                        cur = []
                    elif c in ALPHABET:
                        cur.append(c)
                    else:
                        if len(cur) >= 4: runs.append("".join(cur))
                        cur = []
                if len(cur) >= 4: runs.append("".join(cur))

            for tok in re.findall(r"[A-Za-zÀ-ÿ]+", text):
                cs = []
                valid = True
                for ch in tok:
                    c = norm_char(ch)
                    if c is None: continue
                    if c not in ALPHABET:
                        valid = False; break
                    cs.append(c)
                w = "".join(cs)
                if valid and len(w) >= 3:
                    words[w] += 1
    if not runs:
        raise RuntimeError("no Latin runs")
    return runs, words, {"files": files, "runs": len(runs), "chars": sum(map(len, runs)), "lexicon": len(words)}


class LM4:
    def __init__(self, runs):
        self.c3 = Counter()
        self.c4 = Counter()
        for s in runs:
            for i in range(3, len(s)):
                self.c3[s[i-3:i]] += 1
                self.c4[s[i-3:i+1]] += 1
        self.v = len(ALPHABET)

    def bits(self, streams):
        nll = 0.0; n = 0
        for s in streams:
            for i in range(3, len(s)):
                h = s[i-3:i]; q = s[i-3:i+1]
                p = (self.c4[q] + ALPHA) / (self.c3[h] + ALPHA * self.v)
                nll -= math.log2(p); n += 1
        return (nll / n if n else float("inf")), n


def duration_group(vals):
    try:
        raw = DURATION_STATES.index(vals[0])
    except ValueError as ex:
        raise RuntimeError(f"unexpected slot0 {vals[0]!r}") from ex
    return DURATION_TO_GROUP[raw]


def pitch_raw(vals, slot):
    try:
        return PITCH_STATES[slot].index(vals[slot])
    except ValueError as ex:
        raise RuntimeError(f"unexpected slot{slot} {vals[slot]!r}") from ex


def decoded_streams(items, leaves, parser, policy, pitch_slot, perm):
    out = []
    meta = []
    for it in items:
        if it["leaf"] not in leaves: continue
        for li, line in enumerate(it["lines"]):
            chars = []
            def flush():
                nonlocal chars
                if len(chars) >= 4:
                    s = "".join(chars)
                    out.append(s)
                    meta.append({"page": it["page"], "paragraph": it["id"], "line_index": li, "text": s})
                chars = []
            for tok in line:
                p = parser.pick(tok, policy)
                if p is None:
                    flush(); continue
                vals = p[1]
                g = duration_group(vals)
                r0 = pitch_raw(vals, pitch_slot)
                rank = perm[r0]
                chars.append(TABLE[g][rank])
            flush()
    return out, meta


def choose_key(items, leaves, parser, policy, lm):
    best = None
    rows = []
    for slot in sorted(PITCH_STATES):
        for perm in itertools.permutations(range(5)):
            streams, _ = decoded_streams(items, leaves, parser, policy, slot, perm)
            ce, n = lm.bits(streams)
            row = (ce, slot, tuple(perm), n)
            rows.append(row)
            if best is None or row[:3] < best[:3]: best = row
    if best is None: raise RuntimeError("no key")
    rows.sort()
    return {"cross_entropy": best[0], "slot": best[1], "perm": list(best[2]), "scored_chars": best[3],
            "runner_up": [{"cross_entropy": r[0], "slot": r[1], "perm": list(r[2]), "scored_chars": r[3]} for r in rows[1:6]]}


def lexicon_hits(stream_meta, lexicon):
    hits = []
    seen = set()
    for m in stream_meta:
        s = m["text"]
        for i in range(len(s)):
            for j in range(i + 4, min(len(s), i + 16) + 1):
                w = s[i:j]
                f = lexicon.get(w, 0)
                if not f: continue
                key = (w, m["page"], m["line_index"], i)
                if key in seen: continue
                seen.add(key)
                hits.append({"word": w, "length": len(w), "corpus_frequency": f,
                             "page": m["page"], "line_index": m["line_index"], "offset": i,
                             "context": s[max(0,i-12):min(len(s),j+12)]})
    hits.sort(key=lambda x: (-x["length"], -x["corpus_frequency"], x["word"], x["page"], x["line_index"], x["offset"]))
    return hits[:50]


def top_ngrams(streams, lm):
    c = Counter()
    for s in streams:
        for i in range(len(s)-3): c[s[i:i+4]] += 1
    out = []
    for q, n in c.most_common(50):
        out.append({"ngram": q, "decoded_count": n, "latin_count": lm.c4.get(q, 0)})
    return out


def run_policy(items, parser, policy, lm, lexicon):
    folds = e.physical_leaf_folds(items)
    if len(folds) != 5: raise RuntimeError(f"expected 5 folds got {len(folds)}")
    universe = set().union(*folds)
    rows = []
    all_samples = []
    all_hits = []
    all_grams = []
    for f, held in enumerate(folds):
        train = universe - held
        key = choose_key(items, train, parser, policy, lm)
        streams, meta = decoded_streams(items, held, parser, policy, key["slot"], tuple(key["perm"]))
        ce, n = lm.bits(streams)
        samples = [m for m in meta if len(m["text"]) >= 12][:20]
        hits = lexicon_hits(meta, lexicon)
        grams = top_ngrams(streams, lm)
        rows.append({"fold": f, "held_leaves": sorted(held), "selected_key": key,
                     "held_cross_entropy": ce, "held_scored_chars": n,
                     "held_streams": len(streams), "sample_count": len(samples),
                     "lexicon_hit_count_reported": len(hits)})
        all_samples.append({"fold": f, "samples": samples})
        all_hits.append({"fold": f, "hits": hits})
        all_grams.append({"fold": f, "ngrams": grams})
    keys = Counter((r["selected_key"]["slot"], tuple(r["selected_key"]["perm"])) for r in rows)
    recurrent, recurrence = min(keys.items(), key=lambda kv: (-kv[1], kv[0]))
    return {"policy": policy,
            "mean_held_cross_entropy": statistics.fmean(r["held_cross_entropy"] for r in rows),
            "exact_pitch_key_recurrence": recurrence,
            "most_recurrent_pitch_key": {"slot": recurrent[0], "perm": list(recurrent[1])},
            "folds": rows, "samples": all_samples, "lexicon_hits": all_hits, "top_4grams": all_grams}


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr); return 2
    zl = Path(sys.argv[1]).resolve(); root = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")
    parser = e.SlotParser(); validation = e.validate_parser(parser)
    items = e.parse_voynich(zl)
    runs, lexicon, lmeta = latin_runs_and_lexicon(root)
    lm = LM4(runs)
    primary = run_policy(items, parser, "min", lm, lexicon)
    sensitivity = run_policy(items, parser, "max", lm, lexicon)
    out = {"experiment": "Issue26E9 Philip plaintext diagnostic probe",
           "status": "EXPLORATORY TARGET-ONLY DIAGNOSTIC; NULL CLASSIFICATION NOT YET RUN",
           "historical_table_low_to_high": ["".join(x) for x in TABLE],
           "fixed_duration_key": {"slot": 0, "raw_states": list(DURATION_STATES), "state_to_group": list(DURATION_TO_GROUP)},
           "pitch_candidates": {str(k): list(v) for k,v in PITCH_STATES.items()},
           "latin_population": lmeta, "slot_parser_validation": validation,
           "primary_min": primary, "max_sensitivity": sensitivity}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print(); return 0

if __name__ == "__main__":
    raise SystemExit(main())
