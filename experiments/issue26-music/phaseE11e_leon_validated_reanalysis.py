#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np

# This imports the exact solver generation that was frozen and validated in E11D.
import phaseE11d_dev3_robustness as dev

base = dev.base
ALPHABET = dev.ALPHABET
AI = dev.AI
A = 24
M = 23
FAMILIES = tuple("ABCDEFGHJKLMNPQRSTUVWXZ")
FI = {f:i for i,f in enumerate(FAMILIES)}
STA_SHA256 = "8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a"
ALT_RE = re.compile(r"\[([^\]:]*):[^\]]*\]")
LOCUS_RE = re.compile(r"^<(?P<folio>f[^.>,]+)\.(?P<locus>[^,>]+),(?P<kind>[^>]+)>\s+(?P<body>.*)$")
CODE_RE = re.compile(r"[A-Z][0-9a-z*]")
ANGLE_RE = re.compile(r"<[^>]*>")
LEAF_RE = re.compile(r"f(\d+)")
assert len(FAMILIES) == M and len(ALPHABET) == A


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_segment(seg: str) -> str:
    seg = ALT_RE.sub(lambda m: m.group(1), seg)
    seg = seg.replace("{", "").replace("}", "")
    seg = ANGLE_RE.sub(" ", seg)
    return seg


def parse_sta(path: Path):
    data = path.read_bytes()
    if sha256_bytes(data) != STA_SHA256:
        raise RuntimeError("official STA source SHA-256 mismatch")
    lines = data.decode("utf-8").splitlines()
    if not lines or lines[0].strip() != "#=IVTFF STA1 2.0 M 5":
        raise RuntimeError("unexpected STA header")

    records=[]
    fam_counts=Counter()
    eligible_source_lines=0
    eligible_events=0
    fros_lines=0
    fros_events=0
    interruption_breaks=0
    unreadable_breaks=0

    for no,raw in enumerate(lines,1):
        m=LOCUS_RE.match(raw)
        if not m or "P" not in m.group("kind"):
            continue

        # Count source-level events after the frozen first-reading alternative rule.
        source_body=ALT_RE.sub(lambda x:x.group(1),m.group("body"))
        source_events=len(CODE_RE.findall(source_body))
        lm=LEAF_RE.match(m.group("folio"))
        if not lm:
            if m.group("folio") == "fRos":
                fros_lines += 1
                fros_events += source_events
            continue
        leaf=int(lm.group(1))
        eligible_source_lines += 1
        eligible_events += source_events

        parts=source_body.split("<->")
        interruption_breaks += max(0,len(parts)-1)
        seg_index=0
        for part in parts:
            qparts=part.split("?")
            unreadable_breaks += max(0,len(qparts)-1)
            for qpart in qparts:
                seg=clean_segment(qpart)
                tokens=[]
                seq=[]
                for word in re.split(r"[.,\s]+",seg):
                    if not word:
                        continue
                    codes=CODE_RE.findall(word)
                    residue=CODE_RE.sub("",word)
                    residue=re.sub(r"[-=$%:]","",residue)
                    if residue:
                        raise RuntimeError(f"unparsed STA residue line {no}: {word!r} -> {residue!r}")
                    if not codes:
                        continue
                    fams=[]
                    for code in codes:
                        fam=code[0]
                        if fam not in FI:
                            raise RuntimeError(f"unexpected STA family {fam} in {code}")
                        idx=FI[fam]
                        fams.append(idx)
                        seq.append(idx)
                        fam_counts[fam] += 1
                    tokens.append(np.asarray(fams,dtype=np.int16))
                if seq:
                    records.append({
                        "leaf":leaf,
                        "page":m.group("folio"),
                        "locus":m.group("locus"),
                        "source_line":no,
                        "segment_index":seg_index,
                        "tokens":tokens,
                        "seq":np.asarray(seq,dtype=np.int16),
                    })
                seg_index += 1

    if tuple(sorted(fam_counts)) != tuple(sorted(FAMILIES)):
        raise RuntimeError("STA family set mismatch")
    if eligible_source_lines != 4119 or eligible_events != 140423:
        raise RuntimeError(f"reconciled target population mismatch: {eligible_source_lines}/{eligible_events}")
    if fros_lines != 11 or fros_events != 166:
        raise RuntimeError(f"fRos reconciliation mismatch: {fros_lines}/{fros_events}")
    if sum(fam_counts.values()) != 140423:
        raise RuntimeError(f"parsed family-event mismatch: {sum(fam_counts.values())}")

    leaves=sorted({r["leaf"] for r in records})
    folds=[set(leaves[i::5]) for i in range(5)]
    return records,folds,fam_counts,{
        "sha256":STA_SHA256,
        "numerical_leaf_source_lines":eligible_source_lines,
        "numerical_leaf_family_events":eligible_events,
        "fros_excluded_lines":fros_lines,
        "fros_excluded_events":fros_events,
        "scoring_segments":len(records),
        "numeric_leaves":len(leaves),
        "interruption_breaks":interruption_breaks,
        "unreadable_breaks":unreadable_breaks,
        "families":dict(sorted(fam_counts.items())),
    }


def symbol_counts(seqs):
    c=np.zeros(M,dtype=np.int64)
    for s in seqs:
        for x in s:
            c[int(x)] += 1
    return c


def fit_freq_hill(train_seqs,latin_freq,lm_cost):
    sc=symbol_counts(train_seqs)
    initial=dev.frequency_seed(sc,latin_freq)
    pats,cnts,offsets,incident=base.pattern_arrays_from_sequences(train_seqs,M)
    key,solver_ce,accepted=dev.steepest24(initial,pats,cnts,offsets,incident,lm_cost)
    direct=float(dev.full24(key,pats,cnts,lm_cost))
    shared=float(base.full_score(key,pats,cnts,lm_cost))
    discrepancy=max(abs(direct-float(solver_ce)),abs(direct-shared))
    return key,{
        "training_cross_entropy":direct,
        "solver_cross_entropy":float(solver_ce),
        "shared_cross_entropy":shared,
        "score_discrepancy":discrepancy,
        "accepted_swaps":int(accepted),
        "initial_key":[ALPHABET[int(x)] for x in initial],
    }


def score_key(key,seqs,lm_cost):
    pats,cnts,_,_=base.pattern_arrays_from_sequences(seqs,M)
    return float(dev.full24(key,pats,cnts,lm_cost)),int(cnts.sum())


def decode_seq(key,seq):
    return "".join(ALPHABET[int(key[int(x)])] for x in seq)


def decode_token(key,tok):
    return "".join(ALPHABET[int(key[int(x)])] for x in tok)


def mapping(key):
    used={ALPHABET[int(key[i])] for i in range(M)}
    unused=sorted(set(ALPHABET)-used)
    if len(unused)!=1:
        raise RuntimeError(f"expected one unused plaintext letter, got {unused}")
    return {FAMILIES[i]:ALPHABET[int(key[i])] for i in range(M)},unused[0]


def fold_diagnostics(records,held_leaves,key,lm,lexicon,fold):
    held=[r for r in records if r["leaf"] in held_leaves]
    seqs=[r["seq"] for r in held]
    ce,n=score_key(key,seqs,lm.cost)
    char_counts=Counter()
    samples=[]
    token_samples=[]
    hits=[]
    grams=Counter()
    for r in held:
        text=decode_seq(key,r["seq"])
        char_counts.update(text)
        grams.update(text[i:i+4] for i in range(max(0,len(text)-3)))
        if len(text)>=12 and len(samples)<20:
            samples.append({"page":r["page"],"locus":r["locus"],"source_line":r["source_line"],"text":text[:160]})
        dwords=[decode_token(key,t) for t in r["tokens"]]
        joined=" ".join(dwords)
        if len(joined.replace(" ",""))>=12 and len(token_samples)<20:
            token_samples.append({"page":r["page"],"locus":r["locus"],"source_line":r["source_line"],"text":joined[:240]})
        for w in dwords:
            if len(w)>=4 and w in lexicon:
                hits.append({"fold":fold,"word":w,"length":len(w),"corpus_frequency":int(lexicon[w]),"page":r["page"],"locus":r["locus"],"source_line":r["source_line"]})
    total=sum(char_counts.values())
    return {
        "held_cross_entropy":ce,
        "held_scored_chars":n,
        "held_events":total,
        "held_segments":len(held),
        "top5_char_fraction":sum(v for _,v in char_counts.most_common(5))/total if total else 1.0,
        "char_counts":dict(char_counts.most_common()),
        "samples":samples,
        "tokenized_samples":token_samples,
        "whole_token_lexicon_hits":hits,
        "distinct_words_ge6":sorted({h["word"] for h in hits if h["length"]>=6}),
        "top_4grams":[{"ngram":g,"decoded_count":int(c),"latin_count":int(lm.c4_counter.get(g,0))} for g,c in grams.most_common(50)],
    }


def weighted_key_stability(keys,fam_counts):
    weights=np.asarray([fam_counts[f] for f in FAMILIES],dtype=np.float64)
    denom=float(weights.sum())
    rows=[]
    for i in range(5):
        for j in range(i+1,5):
            same=np.asarray([int(keys[i][g])==int(keys[j][g]) for g in range(M)],dtype=np.float64)
            agreement=float((same*weights).sum()/denom)
            rows.append({"fold_a":i,"fold_b":j,"weighted_agreement":agreement})
    return statistics.fmean(x["weighted_agreement"] for x in rows),rows


def pooled_diagnostics(fold_rows,lm,baseline,fam_counts,keys):
    total_scored=sum(f["held"]["held_scored_chars"] for f in fold_rows)
    pooled_ce=sum(f["held"]["held_cross_entropy"]*f["held"]["held_scored_chars"] for f in fold_rows)/total_scored
    chars=Counter()
    hits=[]
    for f in fold_rows:
        chars.update(f["held"]["char_counts"])
        hits.extend(f["held"]["whole_token_lexicon_hits"])
    total=sum(chars.values())
    top5=sum(v for _,v in chars.most_common(5))/total
    full_keys=[tuple(int(x) for x in k) for k in keys]
    rec=Counter(full_keys)
    modal_key,exact_recurrence=min(rec.items(),key=lambda kv:(-kv[1],kv[0]))
    stability,pairs=weighted_key_stability(keys,fam_counts)
    distinct6=sorted({h["word"] for h in hits if h["length"]>=6})
    folds6=sorted({h["fold"] for h in hits if h["length"]>=6})
    gates={
        "ce_within_latin_plus_0_50":pooled_ce<=baseline["mean_cross_entropy"]+.50,
        "weighted_key_stability_ge_0_90":stability>=.90,
        "exact_key_recurrence_ge3":exact_recurrence>=3,
        "top5_within_latin_plus_0_15":top5<=baseline["top5_char_fraction"]+.15,
        "ten_distinct_whole_token_words_ge6":len(distinct6)>=10,
        "word_hits_across_3folds":len(folds6)>=3,
    }
    if gates["ce_within_latin_plus_0_50"] and not (gates["weighted_key_stability_ge_0_90"] and gates["exact_key_recurrence_ge3"]):
        classification="LATIN-LIKE BUT KEY-UNSTABLE"
    elif gates["weighted_key_stability_ge_0_90"] and gates["exact_key_recurrence_ge3"] and not (gates["ce_within_latin_plus_0_50"] and gates["top5_within_latin_plus_0_15"] and gates["ten_distinct_whole_token_words_ge6"] and gates["word_hits_across_3folds"]):
        classification="STABLE NON-LANGUAGE OPTIMUM"
    elif all(gates.values()):
        classification="STA-FAMILY LEON-LIKE PLAINTEXT LEAD"
    else:
        classification="NO READABLE STA-FAMILY LEON-LIKE PLAINTEXT"
    return {
        "classification":classification,
        "gates":gates,
        "pooled_cross_entropy":pooled_ce,
        "pooled_scored_chars":total_scored,
        "pooled_events":total,
        "pooled_top5_char_fraction":top5,
        "pooled_char_counts":dict(chars.most_common()),
        "mean_pairwise_occurrence_weighted_key_stability":stability,
        "pairwise_key_stability":pairs,
        "exact_full_key_recurrence":int(exact_recurrence),
        "modal_full_key":[ALPHABET[int(x)] for x in modal_key],
        "distinct_whole_token_words_ge6":distinct6,
        "distinct_whole_token_words_ge6_count":len(distinct6),
        "folds_with_words_ge6":folds6,
        "whole_token_hits_ge6":[h for h in hits if h["length"]>=6],
    }


def main():
    if len(sys.argv)!=3:
        print(f"usage: {sys.argv[0]} ZL3b-STA1.txt CREMMA_ROOT",file=sys.stderr)
        return 2
    sta=Path(sys.argv[1]).resolve()
    root=Path(sys.argv[2]).resolve()
    records,folds,fam_counts,sta_meta=parse_sta(sta)
    latin_runs,lexicon,latin_meta=base.load_latin(root)
    baseline=base.latin_self_baseline(latin_runs)
    lm=base.LM4(latin_runs)
    latin_freq=Counter("".join(latin_runs))

    keys=[]; fold_rows=[]
    implementation_failure=False
    for f,held_leaves in enumerate(folds):
        train=[r["seq"] for r in records if r["leaf"] not in held_leaves]
        key,fit=fit_freq_hill(train,latin_freq,lm.cost)
        if fit["score_discrepancy"]>1e-10:
            implementation_failure=True
        mp,unused=mapping(key)
        held=fold_diagnostics(records,held_leaves,key,lm,lexicon,f)
        keys.append(key.copy())
        fold_rows.append({
            "fold":f,
            "held_leaves":sorted(held_leaves),
            "mapping":mp,
            "unused_plaintext_letter":unused,
            **fit,
            "held":held,
        })

    pooled=pooled_diagnostics(fold_rows,lm,baseline,fam_counts,keys)
    if implementation_failure:
        classification="E11E IMPLEMENTATION FAILURE"
    else:
        classification=pooled["classification"]

    out={
        "experiment":"Issue26E11E validated-solver Leon/STA family substitution re-analysis",
        "classification":classification,
        "epistemic_status":"validated-solver re-analysis after prior invalid-solver target exposure",
        "sta_population":sta_meta,
        "family_order":list(FAMILIES),
        "latin_population":latin_meta,
        "latin_self_baseline":baseline,
        "solver":"FREQ-HILL frozen in E11D_SOLVER_FREEZE.md and validated 12/12 in REPORT_E11D_VALIDATION.md",
        "folds":fold_rows,
        "pooled":pooled,
    }
    json.dump(out,sys.stdout,ensure_ascii=False,indent=2,sort_keys=True)
    print()
    return 0


if __name__=="__main__":
    raise SystemExit(main())
