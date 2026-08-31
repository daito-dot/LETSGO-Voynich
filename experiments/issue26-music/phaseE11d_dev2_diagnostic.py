#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from numba import njit

import phaseE11_leon_substitution as base

ALPHABET = tuple("abcdefghiklmnopqrstuwxyz")
A = 24
M = 23
TARGET = 70_000
STEPS = 100_000
T1 = 0.00005
assert len(ALPHABET) == A and "j" not in ALPHABET and "v" not in ALPHABET
AI = {c:i for i,c in enumerate(ALPHABET)}

# Patch shared Python-side normalization before any lazy Numba kernel is called.
base.ALPHABET = ALPHABET
base.A = A
base.AI = AI
base.STEPS = STEPS
base.T1 = T1


def build_runs(latin_runs):
    freq = Counter("".join(latin_runs))
    ranked = sorted(ALPHABET, key=lambda c:(-freq[c], c))
    top23 = tuple(ranked[:M])
    omitted = ranked[M]
    allowed = set(top23)
    out=[]; total=0
    for s in latin_runs:
        cur=[]
        for ch in s:
            if ch in allowed:
                cur.append(ch)
            else:
                if cur:
                    take=min(len(cur), TARGET-total)
                    if take:
                        out.append("".join(cur[:take])); total += take
                    cur=[]
                if total >= TARGET:
                    break
        if total >= TARGET:
            break
        if cur:
            take=min(len(cur), TARGET-total)
            if take:
                out.append("".join(cur[:take])); total += take
        if total >= TARGET:
            break
    if total != TARGET:
        raise RuntimeError(f"DEV2 population short: {total} != {TARGET}")
    return out, top23, omitted, freq


def make_hidden(top23, omitted):
    rng=np.random.default_rng(base.seed32("Issue26E11D:Dev2KnownKey:v1"))
    vals=np.asarray([AI[c] for c in top23],dtype=np.int16)
    rng.shuffle(vals)
    key=np.empty(A,dtype=np.int16)
    key[:M]=vals
    key[M]=AI[omitted]
    return key


def encrypt(runs, key):
    inv={int(key[i]):i for i in range(M)}
    seqs=[]; counts=np.zeros(M,dtype=np.int64)
    for s in runs:
        xs=np.asarray([inv[AI[ch]] for ch in s],dtype=np.int16)
        seqs.append(xs)
        for x in xs: counts[int(x)] += 1
    return seqs, counts


def frequency_seed(symbol_counts, latin_freq):
    cipher_rank=sorted(range(M),key=lambda g:(-int(symbol_counts[g]),g))
    plain_rank=sorted(range(A),key=lambda p:(-int(latin_freq[ALPHABET[p]]),ALPHABET[p]))
    key=np.empty(A,dtype=np.int16)
    for g,p in zip(cipher_rank,plain_rank[:M]): key[g]=p
    key[M]=plain_rank[M]
    return key


@njit(cache=False)
def direct_score24(key,pats,counts,lm_cost):
    nll=0.0; total=0
    for p in range(pats.shape[0]):
        a=int(key[pats[p,0]]); b=int(key[pats[p,1]])
        c=int(key[pats[p,2]]); d=int(key[pats[p,3]])
        q=(((a*24+b)*24+c)*24+d)
        nll += counts[p]*lm_cost[q]
        total += counts[p]
    return nll/total


def metrics(key,true_key,symbol_counts):
    exact=sum(int(key[i])==int(true_key[i]) for i in range(M))/M
    total=int(symbol_counts.sum())
    weighted=sum(int(symbol_counts[i]) for i in range(M) if int(key[i])==int(true_key[i]))/total
    return float(exact),float(weighted)


def row(name,key,pats,counts,lm_cost,true_key,symbol_counts,extra=None):
    direct=float(direct_score24(key,pats,counts,lm_cost))
    shared=float(base.full_score(key,pats,counts,lm_cost))
    ex,wt=metrics(key,true_key,symbol_counts)
    r={"stage":name,"direct_ce":direct,"shared_full_score_ce":shared,
       "full_score_abs_diff":abs(direct-shared),"exact_key_accuracy":ex,
       "occurrence_weighted_key_accuracy":wt,
       "key":[ALPHABET[int(x)] for x in key]}
    if extra: r.update(extra)
    return r


def direct_steepest(initial,pats,counts,lm_cost,max_swaps=100):
    key=initial.copy(); cur=float(direct_score24(key,pats,counts,lm_cost)); accepted=[]
    for step in range(max_swaps):
        best_ce=cur; best_pair=None; best_key=None
        for i in range(A-1):
            for j in range(i+1,A):
                cand=key.copy(); cand[i],cand[j]=cand[j],cand[i]
                ce=float(direct_score24(cand,pats,counts,lm_cost))
                if ce < best_ce-1e-12 or (abs(ce-best_ce)<=1e-12 and best_pair is not None and (i,j)<best_pair):
                    best_ce=ce; best_pair=(i,j); best_key=cand
        if best_pair is None:
            break
        key=best_key; accepted.append({"i":best_pair[0],"j":best_pair[1],"ce":best_ce}); cur=best_ce
    return key,accepted


def delta_audit(seed_key,pats,counts,offsets,incident,lm_cost):
    rng=np.random.default_rng(base.seed32("Issue26E11D:Dev2DeltaAudit:v1"))
    total_count=int(counts.sum())
    marks=np.zeros(pats.shape[0],dtype=np.int32); stamp=0
    diffs=[]; rows=[]
    for k in range(200):
        i,j=sorted(int(x) for x in rng.choice(A,size=2,replace=False))
        d_inc,stamp=base.swap_delta(seed_key,i,j,M,pats,counts,offsets,incident,lm_cost,marks,stamp,total_count)
        cand=seed_key.copy(); cand[i],cand[j]=cand[j],cand[i]
        d_full=float(direct_score24(cand,pats,counts,lm_cost)-direct_score24(seed_key,pats,counts,lm_cost))
        diff=abs(float(d_inc)-d_full); diffs.append(diff)
        if k<20:
            rows.append({"i":i,"j":j,"incremental":float(d_inc),"direct":d_full,"abs_diff":diff})
    return {"samples":200,"max_abs_diff":max(diffs),"mean_abs_diff":statistics.fmean(diffs),"first20":rows}


def anneal_from(seed_key,t0,pats,counts,offsets,incident,lm_cost):
    # Shared kernel is the DEV1 implementation under the patched 24-letter constants.
    seed=base.seed32(f"Issue26E11D:Dev2Anneal:v1:{t0:.3f}")
    key,reported=base.anneal_one(seed_key,seed,M,pats,counts,offsets,incident,lm_cost)
    return key,float(reported),seed


def main():
    if len(sys.argv)!=2:
        print(f"usage: {sys.argv[0]} CREMMA_ROOT",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve()
    latin_runs,_,latin_meta=base.load_latin(root)
    lm=base.LM4(latin_runs)
    plain_runs,top23,omitted,latin_freq=build_runs(latin_runs)
    true_key=make_hidden(top23,omitted)
    seqs,symbol_counts=encrypt(plain_runs,true_key)
    pats,counts,offsets,incident=base.pattern_arrays_from_sequences(seqs,M)

    stages=[]
    stages.append(row("true_key",true_key,pats,counts,lm.cost,true_key,symbol_counts))
    fseed=frequency_seed(symbol_counts,latin_freq)
    stages.append(row("frequency_seed",fseed,pats,counts,lm.cost,true_key,symbol_counts))

    hill,accepted=direct_steepest(fseed,pats,counts,lm.cost)
    stages.append(row("direct_full_score_steepest",hill,pats,counts,lm.cost,true_key,symbol_counts,
                      {"accepted_swaps":len(accepted),"swap_trace":accepted}))

    da=delta_audit(fseed,pats,counts,offsets,incident,lm.cost)

    anneal=[]
    for t0 in (0.50,0.020,0.005,0.001):
        base.T0=t0
        key,reported,seed=anneal_from(fseed,t0,pats,counts,offsets,incident,lm.cost)
        rr=row(f"anneal_T0_{t0}",key,pats,counts,lm.cost,true_key,symbol_counts,
               {"kernel_reported_ce":reported,"seed":seed,"T0":t0})
        anneal.append(rr)

    out={
        "experiment":"Issue26E11D DEV2 synthetic solver diagnosis",
        "status":"DEVELOPMENT ONLY — VALIDATION NOT OPENED — NO VOYNICH INPUT",
        "latin_population":latin_meta,
        "diagnostic_events":int(symbol_counts.sum()),
        "diagnostic_runs":len(plain_runs),
        "top23_plaintext_letters":"".join(top23),
        "omitted_plaintext_letter":omitted,
        "stages":stages,
        "incremental_delta_audit":da,
        "annealing":anneal,
    }
    json.dump(out,sys.stdout,ensure_ascii=False,indent=2,sort_keys=True); print(); return 0

if __name__=="__main__": raise SystemExit(main())
