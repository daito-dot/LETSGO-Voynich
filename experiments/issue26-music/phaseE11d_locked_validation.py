#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np

import phaseE11d_dev3_robustness as dev

base = dev.base
ALPHABET = dev.ALPHABET
AI = dev.AI
A = 24
M = 23
TARGET = 140_423
NVALID = 12
assert len(ALPHABET) == A


def seed32(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode()).digest()[:4], "big") & 0x7fffffff


def rarity_order(latin_runs):
    freq = Counter("".join(latin_runs))
    return tuple(sorted(ALPHABET, key=lambda c: (freq[c], c))), freq


def rotated_runs(latin_runs, idx):
    n = len(latin_runs)
    shift = seed32(f"Issue26E11D:ValidationRuns:v1:{idx}") % n
    return latin_runs[shift:] + latin_runs[:shift], shift


def extract_population(latin_runs, omitted):
    out=[]; total=0
    for s in latin_runs:
        for seg in s.split(omitted):
            if not seg:
                continue
            take=min(len(seg), TARGET-total)
            if take:
                out.append(seg[:take]); total += take
            if total >= TARGET:
                break
        if total >= TARGET:
            break
    if total != TARGET:
        raise RuntimeError(f"validation population short omitted={omitted}: {total} != {TARGET}")
    return out


def hidden_key(idx, omitted):
    allowed=np.asarray([AI[c] for c in ALPHABET if c != omitted],dtype=np.int16)
    rng=np.random.default_rng(seed32(f"Issue26E11D:ValidationKey:v1:{idx}"))
    rng.shuffle(allowed)
    key=np.empty(A,dtype=np.int16)
    key[:M]=allowed
    key[M]=AI[omitted]
    return key


def encrypt(runs,key):
    inv={int(key[g]):g for g in range(M)}
    seqs=[]
    for s in runs:
        seqs.append(np.asarray([inv[AI[ch]] for ch in s],dtype=np.int16))
    return seqs


def counts_for(seqs):
    c=np.zeros(M,dtype=np.int64)
    for s in seqs:
        for x in s: c[int(x)] += 1
    return c


def direct_ce(key,seqs,lm_cost):
    pats,cnts,_,_=base.pattern_arrays_from_sequences(seqs,M)
    if not len(cnts): return float("inf"),0
    ce=float(dev.full24(key,pats,cnts,lm_cost))
    return ce,int(cnts.sum())


def fit_freq_hill(train_seqs,latin_freq,lm_cost):
    symbol_counts=counts_for(train_seqs)
    seed=dev.frequency_seed(symbol_counts,latin_freq)
    pats,cnts,offsets,incident=base.pattern_arrays_from_sequences(train_seqs,M)
    if not len(cnts): raise RuntimeError("no training 4-grams")
    key,solver_ce,accepted=dev.steepest24(seed,pats,cnts,offsets,incident,lm_cost)
    direct=float(dev.full24(key,pats,cnts,lm_cost))
    shared=float(base.full_score(key,pats,cnts,lm_cost))
    discrepancy=max(abs(direct-float(solver_ce)),abs(direct-shared))
    return key,{"training_ce":direct,"solver_ce":float(solver_ce),"shared_ce":shared,
               "score_discrepancy":discrepancy,"accepted_swaps":int(accepted),
               "initial_key":[ALPHABET[int(x)] for x in seed],
               "final_key":[ALPHABET[int(x)] for x in key]}


def held_accuracy(key,true_key,held_seqs):
    counts=counts_for(held_seqs); total=int(counts.sum())
    if not total: return float("nan")
    correct=sum(int(counts[g]) for g in range(M) if int(key[g])==int(true_key[g]))
    return correct/total


def run_validation(idx,latin_runs,rarity,latin_freq,lm_cost):
    rr,shift=rotated_runs(latin_runs,idx)
    omitted=rarity[idx]
    plain=extract_population(rr,omitted)
    true_key=hidden_key(idx,omitted)
    enc=encrypt(plain,true_key)
    fold_ids=[(r+idx)%5 for r in range(len(enc))]
    folds=[]
    for f in range(5):
        train=[s for s,k in zip(enc,fold_ids) if k!=f]
        held=[s for s,k in zip(enc,fold_ids) if k==f]
        key,fit=fit_freq_hill(train,latin_freq,lm_cost)
        acc=held_accuracy(key,true_key,held)
        rec_ce,rec_n=direct_ce(key,held,lm_cost)
        true_ce,true_n=direct_ce(true_key,held,lm_cost)
        if rec_n!=true_n: raise RuntimeError("held score-count mismatch")
        folds.append({
            "fold":f,"training_runs":len(train),"held_runs":len(held),
            "held_chars":sum(map(len,held)),"held_scored_4grams":rec_n,
            "occurrence_weighted_key_accuracy":acc,
            "recovered_held_ce":rec_ce,"true_held_ce":true_ce,"ce_excess":rec_ce-true_ce,
            **fit,
        })
    return {
        "validation_index":idx,"run_rotation_shift":shift,"unused_letter":omitted,
        "plaintext_chars":sum(map(len,plain)),"plaintext_runs":len(plain),
        "true_key":[ALPHABET[int(x)] for x in true_key],
        "mean_weighted_accuracy":statistics.fmean(x["occurrence_weighted_key_accuracy"] for x in folds),
        "mean_recovered_held_ce":statistics.fmean(x["recovered_held_ce"] for x in folds),
        "mean_true_held_ce":statistics.fmean(x["true_held_ce"] for x in folds),
        "mean_ce_excess":statistics.fmean(x["ce_excess"] for x in folds),
        "max_score_discrepancy":max(x["score_discrepancy"] for x in folds),
        "folds":folds,
    }


def classify(vals):
    implementation_ok=max(v["max_score_discrepancy"] for v in vals)<=1e-10
    if not implementation_ok:
        return "VALIDATION IMPLEMENTATION FAILURE",{}
    acc_pass=sum(v["mean_weighted_accuracy"]>=.95 for v in vals)
    ce_pass=sum(v["mean_ce_excess"]<=.05 for v in vals)
    med_acc=statistics.median(v["mean_weighted_accuracy"] for v in vals)
    worst_ce=max(v["mean_ce_excess"] for v in vals)
    worst_acc=min(v["mean_weighted_accuracy"] for v in vals)
    gates={
        "validation_ciphers_accuracy_ge_0_95":acc_pass,
        "validation_ciphers_ce_excess_le_0_05":ce_pass,
        "median_weighted_accuracy":med_acc,
        "worst_ce_excess":worst_ce,
        "worst_weighted_accuracy":worst_acc,
        "gate_11_of_12_accuracy":acc_pass>=11,
        "gate_11_of_12_ce":ce_pass>=11,
        "gate_median_accuracy_ge_0_98":med_acc>=.98,
        "gate_worst_ce_excess_le_0_15":worst_ce<=.15,
        "gate_no_accuracy_below_0_85":worst_acc>=.85,
    }
    passed=all(gates[k] for k in (
        "gate_11_of_12_accuracy","gate_11_of_12_ce","gate_median_accuracy_ge_0_98",
        "gate_worst_ce_excess_le_0_15","gate_no_accuracy_below_0_85"))
    return ("E11D SOLVER VALIDATED" if passed else "E11D SOLVER NOT VALIDATED"),gates


def main():
    if len(sys.argv)!=2:
        print(f"usage: {sys.argv[0]} CREMMA_ROOT",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve()
    latin_runs,_,latin_meta=base.load_latin(root)
    rarity,latin_freq=rarity_order(latin_runs)
    lm=base.LM4(latin_runs)
    vals=[run_validation(i,latin_runs,rarity,latin_freq,lm.cost) for i in range(NVALID)]
    classification,gates=classify(vals)
    out={
        "experiment":"Issue26E11D locked 12-cipher monoalphabetic solver validation",
        "classification":classification,
        "solver":"FREQ-HILL frozen in E11D_SOLVER_FREEZE.md",
        "validation_population":"PLAN_E11D.md + PLAN_E11D_VALIDATION_AMENDMENT.md",
        "latin_population":latin_meta,"rarity_order":"".join(rarity),"target_chars_per_cipher":TARGET,
        "gates":gates,"validations":vals,
    }
    json.dump(out,sys.stdout,ensure_ascii=False,indent=2,sort_keys=True); print(); return 0


if __name__=="__main__": raise SystemExit(main())
