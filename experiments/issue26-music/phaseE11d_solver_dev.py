#!/usr/bin/env python3
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np

import phaseE11_leon_substitution as base

# Frozen E11C specification: 24 Latin letters after j->i and v->u.
ALPHABET = tuple("abcdefghiklmnopqrstuwxyz")
assert len(ALPHABET) == 24 and "j" not in ALPHABET and "v" not in ALPHABET
base.ALPHABET = ALPHABET
base.A = len(ALPHABET)
base.AI = {c:i for i,c in enumerate(ALPHABET)}

# E11D development parameters. These are tunable on the already-revealed synthetic
# development control only. Locked validation must not be emitted by this script.
DEV_RESTARTS = 12
DEV_STEPS = 100_000
DEV_T0 = 0.50
DEV_T1 = 0.00010
TARGET_EVENTS = 140_423
M = 23

# base.anneal_one is Numba-lazy; these constants are read when first compiled in this process.
base.STEPS = DEV_STEPS
base.T0 = DEV_T0
base.T1 = DEV_T1


def encode_development(latin_runs):
    freq = Counter("".join(latin_runs))
    top_plain = [c for c,_ in sorted(freq.items(), key=lambda kv:(-kv[1],kv[0]))[:M]]
    runs, events = base.split_topm_runs(latin_runs, set(top_plain), TARGET_EVENTS)
    rng = np.random.default_rng(base.seed32("Issue26E11C:PositiveKey:v1"))
    cipher_order = rng.permutation(M).tolist()
    plain_to_cipher = {top_plain[i]:int(cipher_order[i]) for i in range(M)}
    true_decode = np.full(M, -1, dtype=np.int16)
    for p,cidx in plain_to_cipher.items():
        true_decode[cidx] = base.AI[p]
    encoded = [np.asarray([plain_to_cipher[ch] for ch in s], dtype=np.int16) for s in runs]
    return encoded, true_decode, top_plain, events


def frequency_seed(train, latin_runs):
    c = Counter()
    for s in train:
        c.update(int(x) for x in s)
    pf = Counter("".join(latin_runs))
    cipher_rank = [x for x,_ in sorted(c.items(), key=lambda kv:(-kv[1],kv[0]))]
    if len(cipher_rank) != M:
        missing = [i for i in range(M) if i not in c]
        cipher_rank += missing
    plain_rank = [base.AI[ch] for ch,_ in sorted(pf.items(), key=lambda kv:(-kv[1],kv[0]))]
    if len(plain_rank) != base.A:
        raise RuntimeError("plaintext alphabet frequency mismatch")
    key = np.full(base.A, -1, dtype=np.int16)
    for ci,pi in zip(cipher_rank,plain_rank[:M]):
        key[ci] = pi
    used = set(int(x) for x in key[:M])
    unused = [i for i in range(base.A) if i not in used]
    if len(unused) != 1:
        raise RuntimeError(f"frequency seed unused mismatch {unused}")
    key[M] = unused[0]
    return key


def perturb(key, seed, swaps):
    rng = np.random.default_rng(seed)
    out = key.copy()
    for _ in range(swaps):
        i,j = rng.choice(base.A, size=2, replace=False)
        out[i],out[j] = out[j],out[i]
    return out


def optimize_v2(train, lm, latin_runs, fold):
    pats,counts,offsets,incident = base.pattern_arrays_from_sequences(train,M)
    starts = []
    fseed = frequency_seed(train,latin_runs)
    starts.append(("frequency", fseed))
    for r in range(1,8):
        seed = base.seed32(f"Issue26E11D:DevPerturb:v1:{fold}:{r}")
        starts.append((f"freq_perturb_{r}", perturb(fseed,seed,1 + (r//2))))
    for r in range(4):
        seed = base.seed32(f"Issue26E11D:DevRandom:v1:{fold}:{r}")
        rng = np.random.default_rng(seed)
        starts.append((f"random_{r}",rng.permutation(base.A).astype(np.int16)))
    if len(starts) != DEV_RESTARTS:
        raise RuntimeError("restart population mismatch")

    best = None; rows=[]
    for r,(kind,initial) in enumerate(starts):
        seed = base.seed32(f"Issue26E11D:DevAnneal:v1:{fold}:{r}")
        key,ce = base.anneal_one(initial,seed,M,pats,counts,offsets,incident,lm.cost)
        tup = tuple(int(x) for x in key)
        row={"restart":r,"kind":kind,"seed":seed,"training_cross_entropy":float(ce)}
        rows.append(row)
        cand=(float(ce),tup,key.copy(),kind)
        if best is None or cand[:2] < best[:2]:
            best=cand
    return best[2],best[0],best[3],rows


def score_true(true_decode, held, lm):
    used=set(int(x) for x in true_decode)
    unused=[i for i in range(base.A) if i not in used]
    if len(unused)!=1: raise RuntimeError("true unused mismatch")
    full=np.asarray(list(true_decode)+unused,dtype=np.int16)
    ce,n=base.score_key_on_seqs(full,held,M,lm.cost)
    return full,ce,n


def main():
    if len(sys.argv)!=2:
        print(f"usage: {sys.argv[0]} CREMMA_ROOT",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve()
    latin_runs,_,latin_meta=base.load_latin(root)
    lm=base.LM4(latin_runs)
    encoded,true_decode,top_plain,events=encode_development(latin_runs)
    fold_ids=[i%5 for i in range(len(encoded))]
    symbol_counts=np.zeros(M,dtype=np.int64)
    for s in encoded:
        for x in s: symbol_counts[int(x)]+=1

    rows=[]
    for f in range(5):
        train=[s for i,s in enumerate(encoded) if fold_ids[i]!=f]
        held=[s for i,s in enumerate(encoded) if fold_ids[i]==f]
        key,tr_ce,kind,restarts=optimize_v2(train,lm,latin_runs,f)
        rec_ce,n=base.score_key_on_seqs(key,held,M,lm.cost)
        _,true_ce,_=score_true(true_decode,held,lm)
        exact=sum(int(key[i])==int(true_decode[i]) for i in range(M))/M
        weighted=sum(symbol_counts[i] for i in range(M) if int(key[i])==int(true_decode[i]))/symbol_counts.sum()
        rows.append({"fold":f,"selected_start_kind":kind,"training_cross_entropy":tr_ce,
                     "recovered_held_cross_entropy":rec_ce,"true_held_cross_entropy":true_ce,
                     "held_scored_chars":n,"exact_key_accuracy":exact,
                     "occurrence_weighted_key_accuracy":weighted,
                     "recovered_mapping":base.key_mapping(key,[f"C{i:02d}" for i in range(M)]),
                     "restart_scores":restarts})

    mean_rec=statistics.fmean(r["recovered_held_cross_entropy"] for r in rows)
    mean_true=statistics.fmean(r["true_held_cross_entropy"] for r in rows)
    mean_w=statistics.fmean(r["occurrence_weighted_key_accuracy"] for r in rows)
    passed=mean_w>=.95 and abs(mean_rec-mean_true)<=.05
    out={"experiment":"Issue26E11D Voynich-blind solver development control",
         "status":"DEVELOPMENT ONLY — VALIDATION NOT OPENED",
         "development_passed":passed,
         "solver":{"restarts":DEV_RESTARTS,"steps":DEV_STEPS,"T0":DEV_T0,"T1":DEV_T1,
                   "starts":"1 frequency + 7 frequency-perturbed + 4 random",
                   "finalizer":"deterministic steepest pair-swap descent"},
         "latin_population":latin_meta,"target_events":TARGET_EVENTS,"encoded_events":events,
         "top_plaintext_letters":top_plain,
         "mean_recovered_held_cross_entropy":mean_rec,"mean_true_held_cross_entropy":mean_true,
         "mean_occurrence_weighted_key_accuracy":mean_w,"folds":rows}
    json.dump(out,sys.stdout,ensure_ascii=False,indent=2,sort_keys=True); print(); return 0

if __name__=="__main__": raise SystemExit(main())
