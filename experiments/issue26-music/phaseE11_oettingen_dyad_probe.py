#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import issue26e_core as e

ALPHA = 0.1
CREMMA_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
ALPHABET = tuple("abcdefghiklmnopqrstuwxyz")  # historical 24-letter key: no j/v
TONES = ("ut", "re", "mi", "fa", "sol")
SLOT_STATES = {
    3: ("", "t", "k", "p", "f"),
    5: ("", "cth", "ckh", "cph", "cfh"),
}
# HAB editorial reduction of the angel table. First note indexes rows, second columns.
HISTORICAL = {
    ("ut", "ut"): "q", ("ut", "fa"): "r", ("ut", "sol"): "s", ("ut", "mi"): "t", ("ut", "re"): "u",
    ("sol", "ut"): "w", ("sol", "fa"): "x", ("sol", "sol"): "y", ("sol", "mi"): "z", ("sol", "re"): None,
    ("fa", "ut"): "a", ("fa", "fa"): "b", ("fa", "sol"): "c", ("fa", "mi"): "d", ("fa", "re"): "e",
    ("mi", "ut"): "l", ("mi", "fa"): "m", ("mi", "sol"): "n", ("mi", "mi"): "o", ("mi", "re"): "p",
    ("re", "ut"): "f", ("re", "fa"): "g", ("re", "sol"): "h", ("re", "mi"): "i", ("re", "re"): "k",
}
PERMS = tuple(itertools.permutations(range(5)))


def stable_seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8], "big")


def norm_letter(ch: str):
    s = unicodedata.normalize("NFKD", ch.lower())
    s = "".join(c for c in s if "a" <= c <= "z")
    if not s:
        return None
    c = s[0]
    if c == "j": c = "i"
    elif c == "v": c = "u"
    return c if c in ALPHABET else None


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
                    c = norm_letter(ch)
                    if c is None:
                        if len(cur) >= 4: runs.append("".join(cur))
                        cur = []
                    else:
                        cur.append(c)
                if len(cur) >= 4: runs.append("".join(cur))
            for tok in re.findall(r"[A-Za-zÀ-ÿ]+", text):
                cs = []
                valid = True
                for ch in tok:
                    c = norm_letter(ch)
                    if c is None:
                        # J/V normalize into the alphabet; other unsupported letters invalidate.
                        z = unicodedata.normalize("NFKD", ch.lower())
                        if any("a" <= q <= "z" for q in z): valid = False
                        continue
                    cs.append(c)
                w = "".join(cs)
                if valid and len(w) >= 3: lexicon[w] += 1
    if not runs:
        raise RuntimeError("no Latin runs")
    return runs, lexicon, {"files": files, "runs": len(runs), "chars": sum(map(len, runs)), "lexicon": len(lexicon), "alphabet": "".join(ALPHABET)}


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


def latin_self_baseline(runs):
    rows = []
    for f in range(5):
        tr = [s for i,s in enumerate(runs) if i % 5 != f]
        he = [s for i,s in enumerate(runs) if i % 5 == f]
        lm = LM4(tr); ce, n = lm.bits(he)
        rows.append({"fold": f, "cross_entropy": ce, "scored_chars": n})
    return {"mean_cross_entropy": statistics.fmean(r["cross_entropy"] for r in rows), "folds": rows}


def raw_note_runs(items, leaves, parser, policy, slot):
    idx = {v:i for i,v in enumerate(SLOT_STATES[slot])}
    out = []; meta = []
    for it in items:
        if it["leaf"] not in leaves: continue
        for li, line in enumerate(it["lines"]):
            cur = []
            def flush():
                nonlocal cur
                if cur:
                    out.append(tuple(cur))
                    meta.append({"page": it["page"], "paragraph": it["id"], "line_index": li})
                cur = []
            for tok in line:
                p = parser.pick(tok, policy)
                if p is None:
                    flush(); continue
                vals = p[1]
                if vals[slot] not in idx:
                    raise RuntimeError(f"unexpected slot{slot} state {vals[slot]!r}")
                cur.append(idx[vals[slot]])
            flush()
    return out, meta


def decode_runs(runs, meta, perm, phase):
    streams = []; rows = []
    dyads = illegal = unpaired = 0
    for raw, m in zip(runs, meta):
        start = phase
        if len(raw) <= start:
            unpaired += len(raw); continue
        cur = []
        def flush_text():
            nonlocal cur
            if cur:
                text = "".join(cur)
                streams.append(text); rows.append({**m, "text": text})
            cur = []
        i = start
        while i + 1 < len(raw):
            a = TONES[perm[raw[i]]]; b = TONES[perm[raw[i+1]]]
            dyads += 1
            ch = HISTORICAL[(a,b)]
            if ch is None:
                illegal += 1; flush_text()
            else:
                cur.append(ch)
            i += 2
        if i < len(raw): unpaired += 1
        if phase == 1 and raw: unpaired += 1
        flush_text()
    return streams, rows, {"dyads": dyads, "illegal_dyads": illegal,
                           "illegal_rate": illegal/dyads if dyads else 1.0,
                           "unpaired_notes": unpaired, "raw_runs": len(runs)}


def choose_key(items, leaves, parser, policy, lm, phase):
    best = None
    candidates = []
    for slot in sorted(SLOT_STATES):
        runs, meta = raw_note_runs(items, leaves, parser, policy, slot)
        for perm in PERMS:
            streams, _, d = decode_runs(runs, meta, perm, phase)
            ce, n = lm.bits(streams)
            rank = (d["illegal_rate"], ce, slot, perm)
            row = {"slot": slot, "perm": list(perm), "illegal_rate": d["illegal_rate"],
                   "cross_entropy": ce, "scored_chars": n, "decoded_dyads": d["dyads"]}
            candidates.append((rank, row))
            if best is None or rank < best[0]: best = (rank, row)
    if best is None: raise RuntimeError("no candidate key")
    candidates.sort(key=lambda z:z[0])
    out = dict(best[1])
    out["runner_up"] = [z[1] for z in candidates[1:6]]
    return out


def lexicon_hits(rows, lexicon, cap=100):
    hits = []; seen = set()
    for m in rows:
        s = m["text"]
        for i in range(len(s)):
            for j in range(i+6, min(len(s), i+18)+1):
                w = s[i:j]; freq = lexicon.get(w, 0)
                if not freq: continue
                key = (w, m["page"], m["line_index"], i)
                if key in seen: continue
                seen.add(key)
                hits.append({"word":w,"length":len(w),"corpus_frequency":int(freq),
                             "page":m["page"],"line_index":m["line_index"],"offset":i,
                             "context":s[max(0,i-12):min(len(s),j+12)]})
    hits.sort(key=lambda z:(-z["length"],-z["corpus_frequency"],z["word"],z["page"],z["line_index"],z["offset"]))
    return hits[:cap]


def population_diag(streams, rows, d, lm, lexicon):
    ce, n = lm.bits(streams)
    chars = Counter("".join(streams)); total = sum(chars.values())
    hits = lexicon_hits(rows, lexicon)
    grams = Counter()
    for s in streams:
        grams.update(s[i:i+4] for i in range(len(s)-3))
    samples = [m for m in rows if len(m["text"]) >= 12][:25]
    distinct6 = sorted({h["word"] for h in hits if h["length"] >= 6})
    longest = max((h["length"] for h in hits), default=0)
    return {**d, "cross_entropy": ce, "scored_chars": n, "decoded_chars": total,
            "plaintext_streams": len(streams),
            "top5_char_fraction": sum(v for _,v in chars.most_common(5))/total if total else 1.0,
            "char_counts": dict(chars.most_common()), "samples": samples,
            "distinct_lexicon_hits_ge6": len(distinct6), "distinct_words_ge6": distinct6[:100],
            "longest_lexicon_hit": longest, "lexicon_hits": hits,
            "top_4grams":[{"ngram":q,"decoded_count":int(c),"latin_count":int(lm.c4.get(q,0))} for q,c in grams.most_common(50)]}


def shuffle_control(streams, lm, reps=1000):
    obs, _ = lm.bits(streams)
    null = []
    for r in range(reps):
        rng = random.Random(stable_seed(f"Issue26E11:HeldStreamShuffle:v1:{r}"))
        ss = []
        for s in streams:
            a = list(s); rng.shuffle(a); ss.append("".join(a))
        ce, _ = lm.bits(ss); null.append(ce)
    le = sum(x <= obs for x in null)
    ys = sorted(null)
    def quantile(q):
        p=(len(ys)-1)*q; lo=math.floor(p); hi=math.ceil(p)
        return ys[lo] if lo==hi else ys[lo]*(hi-p)+ys[hi]*(p-lo)
    return {"observed_ce":obs,"reps":reps,"null_median":statistics.median(null),
            "null_q05":quantile(.05),"null_q95":quantile(.95),"null_min":min(null),
            "count_null_le_observed":le,"lower_tail_p":(1+le)/(reps+1)}


def run_policy(items, parser, policy, lm, lexicon, phase):
    folds=e.physical_leaf_folds(items)
    universe=set().union(*folds)
    fr=[]; pooled_streams=[]; pooled_rows=[]; totals=Counter(); keys=[]
    for f,held in enumerate(folds):
        train=universe-held
        key=choose_key(items,train,parser,policy,lm,phase)
        runs,meta=raw_note_runs(items,held,parser,policy,key["slot"])
        streams,rows,d=decode_runs(runs,meta,tuple(key["perm"]),phase)
        diag=population_diag(streams,rows,d,lm,lexicon)
        fr.append({"fold":f,"held_leaves":sorted(held),"selected_key":key,"held":diag})
        pooled_streams.extend(streams); pooled_rows.extend(rows)
        for z in ("dyads","illegal_dyads","unpaired_notes","raw_runs"): totals[z]+=d[z]
        keys.append((key["slot"],tuple(key["perm"])))
    pooled_d={"dyads":totals["dyads"],"illegal_dyads":totals["illegal_dyads"],
              "illegal_rate":totals["illegal_dyads"]/totals["dyads"] if totals["dyads"] else 1.0,
              "unpaired_notes":totals["unpaired_notes"],"raw_runs":totals["raw_runs"]}
    pooled=population_diag(pooled_streams,pooled_rows,pooled_d,lm,lexicon)
    kc=Counter(keys); recurrent,count=min(kc.items(),key=lambda kv:(-kv[1],kv[0]))
    sc=shuffle_control(pooled_streams,lm)
    return {"policy":policy,"phase":phase,"folds":fr,"exact_key_recurrence":count,
            "most_recurrent_key":{"slot":recurrent[0],"perm":list(recurrent[1])},
            "pooled":pooled,"sequence_order_control":sc}


def classify(primary, latin_base):
    p=primary["pooled"]; s=primary["sequence_order_control"]
    gates={
        "key_recurrence_ge4": primary["exact_key_recurrence"]>=4,
        "ce_within_0p50_of_latin": p["cross_entropy"] <= latin_base+0.50,
        "shuffle_p_le_0p001": s["lower_tail_p"] <= .001,
        "illegal_rate_le_0p01": p["illegal_rate"] <= .01,
        "top5_le_0p80": p["top5_char_fraction"] <= .80,
        "lexicon_5_distinct_ge6": p["distinct_lexicon_hits_ge6"] >= 5,
        "lexicon_one_ge8": p["longest_lexicon_hit"] >= 8,
    }
    if all(gates.values()): label="DYADIC MUSIC-CIPHER PLAINTEXT LEAD"
    elif s["lower_tail_p"] <= .01: label="ORDERED BUT NOT READABLE"
    else: label="NO OETTINGEN PLAINTEXT SIGNAL"
    return label,gates


def main():
    if len(sys.argv)!=3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT",file=sys.stderr); return 2
    zl=Path(sys.argv[1]).resolve(); root=Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes())!=e.EXPECTED_ZL3B_BLOB: raise RuntimeError("ZL blob mismatch")
    parser=e.SlotParser(); validation=e.validate_parser(parser); items=e.parse_voynich(zl)
    runs,lexicon,lmeta=load_latin(root); lm=LM4(runs); baseline=latin_self_baseline(runs)
    primary=run_policy(items,parser,"min",lm,lexicon,0)
    label,gates=classify(primary,baseline["mean_cross_entropy"])
    max0=run_policy(items,parser,"max",lm,lexicon,0)
    min1=run_policy(items,parser,"min",lm,lexicon,1)
    max1=run_policy(items,parser,"max",lm,lexicon,1)
    out={"experiment":"Issue26E11 Oettingen-Wallerstein sequential-dyad music-cipher probe",
         "classification":label,"lead_gates":gates,
         "historical_key":{"tones":list(TONES),"row_first_note":["ut","sol","fa","mi","re"],
                           "column_second_note":["ut","fa","sol","mi","re"],
                           "matrix":[["q","r","s","t","u"],["w","x","y","z",None],["a","b","c","d","e"],["l","m","n","o","p"],["f","g","h","i","k"]]},
         "latin_population":lmeta,"latin_self_baseline":baseline,"slot_parser_validation":validation,
         "candidate_keys_per_fold":240,
         "primary_min_phase0":primary,"max_phase0_sensitivity":max0,
         "min_phase1_sensitivity":min1,"max_phase1_sensitivity":max1}
    json.dump(out,sys.stdout,ensure_ascii=False,indent=2,sort_keys=True); print(); return 0

if __name__=="__main__": raise SystemExit(main())
