#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from pathlib import Path

import numpy as np
import issue26e_core as e

IT_SHA256 = "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"
FIXED_MAX_STATE_TO_VOX = (0, 3, 4, 1, 2, 5)
SWAP_ATTEMPTS = 5000
FOLDS = [
    {1,6,11,17,22,27,32,37,42,47,52,57,68,77,82,87,94,101,106,113},
    {2,7,13,18,23,28,33,38,43,48,53,58,69,78,83,88,95,102,107,114},
    {3,8,14,19,24,29,34,39,44,49,54,65,70,79,84,89,96,103,108,115},
    {4,9,15,20,25,30,35,40,45,50,55,66,75,80,85,90,99,104,111,116},
    {5,10,16,21,26,31,36,41,46,51,56,67,76,81,86,93,100,105,112},
]
ORIGINAL_MIN = {
    "coverage": 0.769422745638643,
    "A": 0.8509664380470466,
    "null_median": 0.8412499079974372,
    "p": 0.009900990099009901,
    "wins": 5,
}
ORIGINAL_MAX = {
    "coverage": 0.769422745638643,
    "A": 0.8439032769036159,
    "null_median": 0.8186132826610175,
    "p": 0.009900990099009901,
    "wins": 5,
}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fit_types(items, train, parser, policy):
    vectors = {}
    for it in items:
        if it["leaf"] not in train: continue
        for line in it["lines"]:
            for tok in line:
                p = parser.pick(tok, policy)
                if p is not None and tok not in vectors: vectors[tok] = e.feature(p[1])
    return e.KMeans20().fit(vectors), len(vectors)


def fit_fixed_columns(C, lattice, perm=FIXED_MAX_STATE_TO_VOX):
    W = np.zeros((20,20), dtype=np.int64)
    for s,v in enumerate(perm): W += C[:,s,None] * lattice[None,:,v]
    score,_ = e.assignment_score(W); rows = e.lex_assignment(W, score)
    return {"training_allowed": int(score), "state_to_vox": list(perm), "cluster_to_row": rows.tolist()}


def summarize(guid, null_by_fold, fold_rows):
    mean_g = statistics.mean(guid)
    n = len(null_by_fold[0])
    mean_null = [statistics.mean(null_by_fold[f][j] for f in range(5)) for j in range(n)]
    med = statistics.median(mean_null)
    return {
        "mean_guidonian_accuracy": mean_g,
        "paired_null_mean_median": med,
        "paired_null_mean_q95": e.quantile(mean_null, .95),
        "paired_null_mean_min": min(mean_null),
        "paired_null_mean_max": max(mean_null),
        "global_advantage": mean_g - med,
        "p_global": (1 + sum(x >= mean_g - e.EPS for x in mean_null)) / (n + 1),
        "fold_null_median_wins": sum(r["guidonian_accuracy"] > r["null_median_accuracy"] + e.EPS for r in fold_rows),
    }


def run_policy(items, parser, policy, n_null, label_prefix, fixed_columns=False, capture_first100=False):
    universe = set().union(*FOLDS); fold_rows=[]; null_by_fold=[]; first100_by_fold=[]
    coverages=[]; guid=[]
    for f, held in enumerate(FOLDS):
        train = universe - held; km, ntypes = fit_types(items, train, parser, policy)
        C,tvis,tpar = e.count_matrix(items, train, parser, policy, km)
        H,hvis,hpar = e.count_matrix(items, held, parser, policy, km)
        gmap = fit_fixed_columns(C,e.GUIDO) if fixed_columns else e.fit_mapping(C,e.GUIDO)
        gs = e.score_counts(H,hvis,hpar,gmap,e.GUIDO)
        coverages.append(gs["parse_coverage"]); guid.append(gs["accuracy"])
        seen=set(); null=[]
        for j in range(n_null):
            if label_prefix == "Issue26E": label=f"Issue26E:{policy}:fold:{f}:null:{j}"
            else: label=f"{label_prefix}:fold:{f}:null:{j}"
            M=e.swapped_lattice(label,seen,SWAP_ATTEMPTS)
            nm=fit_fixed_columns(C,M) if fixed_columns else e.fit_mapping(C,M)
            ns=e.score_counts(H,hvis,hpar,nm,M); null.append(ns["accuracy"])
        first100_by_fold.append(null[:100])
        med=statistics.median(null)
        fold_rows.append({
            "fold":f,"held_leaves":sorted(held),"training_unique_parsed_types":ntypes,
            "training_visible_occurrences":tvis,"training_parsed_occurrences":tpar,
            "heldout_visible_occurrences":hvis,"heldout_parsed_occurrences":hpar,
            "parse_coverage":gs["parse_coverage"],"guidonian_accuracy":gs["accuracy"],
            "guidonian_training_allowed":gmap["training_allowed"],"guidonian_mapping":gmap,
            "null_median_accuracy":med,"null_q95_accuracy":e.quantile(null,.95),
            "guidonian_minus_null_median":gs["accuracy"]-med,
            "p_fold":(1+sum(x>=gs["accuracy"]-e.EPS for x in null))/(n_null+1),
        }); null_by_fold.append(null)
    out=summarize(guid,null_by_fold,fold_rows)
    out.update({"policy":policy,"n_null":n_null,"mean_parse_coverage":statistics.mean(coverages),"folds":fold_rows})
    if capture_first100:
        s100=summarize(guid,first100_by_fold,[{
            "guidonian_accuracy":fold_rows[f]["guidonian_accuracy"],
            "null_median_accuracy":statistics.median(first100_by_fold[f])} for f in range(5)])
        s100["mean_parse_coverage"]=statistics.mean(coverages); out["first100_replay"]=s100
    return out


def assert_replay(x, expected, label):
    r=x["first100_replay"]
    checks={
        "coverage":abs(r["mean_parse_coverage"]-expected["coverage"])<=1e-12,
        "A":abs(r["mean_guidonian_accuracy"]-expected["A"])<=1e-12,
        "null_median":abs(r["paired_null_mean_median"]-expected["null_median"])<=1e-12,
        "p":abs(r["p_global"]-expected["p"])<=1e-12,
        "wins":r["fold_null_median_wins"]==expected["wins"],
    }
    if not all(checks.values()): raise RuntimeError(f"{label} first100 replay mismatch: {checks} {r}")
    return checks


def gate_refit(minx,maxx):
    return (minx["mean_parse_coverage"]>=.60 and minx["p_global"]<=.05 and
            minx["fold_null_median_wins"]>=4 and maxx["global_advantage"]>0 and maxx["p_global"]<=.10)


def gate_fixed(x):
    return (x["mean_parse_coverage"]>=.60 and x["p_global"]<=.05 and x["global_advantage"]>0 and x["fold_null_median_wins"]>=4)


def main():
    if len(sys.argv)!=3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt IT2a-n.txt",file=sys.stderr); return 2
    zl=Path(sys.argv[1]).resolve(); it=Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes())!=e.EXPECTED_ZL3B_BLOB: raise RuntimeError("ZL blob mismatch")
    if hashlib.sha256(it.read_bytes()).hexdigest()!=IT_SHA256: raise RuntimeError("IT2a SHA256 mismatch")
    parser=e.SlotParser(); validation=e.validate_parser(parser)
    zl_items=e.parse_voynich(zl); it_items=e.parse_voynich(it)

    # E2-A: exact first 100 null labels plus 900 extension.
    zlmin=run_policy(zl_items,parser,"min",1000,"Issue26E",capture_first100=True)
    zlmax=run_policy(zl_items,parser,"max",1000,"Issue26E",capture_first100=True)
    replay={"min":assert_replay(zlmin,ORIGINAL_MIN,"min"),"max":assert_replay(zlmax,ORIGINAL_MAX,"max")}
    A_pass=gate_refit(zlmin,zlmax)

    # E2-B: independent IT architecture refit.
    itmin=run_policy(it_items,parser,"min",100,"Issue26E2:IT:refit:min")
    itmax=run_policy(it_items,parser,"max",100,"Issue26E2:IT:refit:max")
    B_pass=gate_refit(itmin,itmax)

    # E2-C: prospective frozen six-state map, IT max parser, row mapping only.
    itfixed=run_policy(it_items,parser,"max",100,"Issue26E2:IT:fixed",fixed_columns=True)
    C_pass=gate_fixed(itfixed)

    if not A_pass: verdict="ORIGINAL E NOT STABLE"
    elif B_pass and C_pass: verdict="STRONG GUIDONIAN SLOT REPLICATION"
    elif B_pass or C_pass: verdict="PARTIAL GUIDONIAN SLOT REPLICATION"
    else: verdict="ZL-ONLY / NOT INDEPENDENTLY REPLICATED"

    here=Path(__file__).resolve().parent
    out={
        "experiment":"Issue26E2 high-resolution + IT2a replication","issue":26,
        "inputs":{"zl_blob_sha1":e.EXPECTED_ZL3B_BLOB,"it_sha256":IT_SHA256,
                  "plan_sha256":sha256_file(here/"PLAN_E2.md"),"core_sha256":sha256_file(here/"issue26e_core.py"),
                  "script_sha256":sha256_file(Path(__file__)),"fixed_max_state_to_vox":list(FIXED_MAX_STATE_TO_VOX)},
        "slot_parser_validation":validation,"first100_replay_assertions":replay,
        "E2A_ZL_min_1000":zlmin,"E2A_ZL_max_1000":zlmax,
        "E2B_IT_min_refit":itmin,"E2B_IT_max_refit":itmax,"E2C_IT_max_fixed_map":itfixed,
        "gates":{"E2A_high_resolution":A_pass,"E2B_IT_refit":B_pass,"E2C_IT_fixed_map":C_pass},
        "frozen_classification":verdict,
    }
    json.dump(out,sys.stdout,ensure_ascii=False,indent=2,sort_keys=True); print(); return 0

if __name__=="__main__": raise SystemExit(main())
