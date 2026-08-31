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
from collections import Counter
from pathlib import Path

import numpy as np

import issue26e_core as e

ALPHABET = tuple("abcdefghiklmnopqrstuwxyz")
AI = {c:i for i,c in enumerate(ALPHABET)}
A = len(ALPHABET)
ALPHA = .1
CREMMA_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
SLOT10 = ("", "d", "l", "r", "m", "n")
COUNT_SLOTS = {
    6: ("", "e", "ee", "eee"),
    9: ("", "i", "ii", "iii"),
}
PERMS = np.asarray(list(itertools.permutations(range(6))), dtype=np.uint8)
assert A == 24 and len(PERMS) == 720


def seed32(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode()).digest()[:4], "big") & 0x7fffffff


def norm_letter(ch: str):
    s = unicodedata.normalize("NFKD", ch.lower())
    s = "".join(c for c in s if "a" <= c <= "z")
    if not s:
        return None
    c = s[0]
    if c == "j": c = "i"
    elif c == "v": c = "u"
    return c if c in AI else None


def load_latin(root: Path):
    runs=[]; lexicon=Counter(); files=0
    for rel in CREMMA_DIRS:
        d=root/rel
        if not d.is_dir(): raise RuntimeError(f"missing CREMMA dir {d}")
        for p in sorted(d.rglob("*.txt")):
            files += 1
            text=p.read_text(encoding="utf-8",errors="replace")
            for raw in text.splitlines():
                cur=[]
                for ch in raw:
                    c=norm_letter(ch)
                    if c is None:
                        if len(cur)>=4: runs.append("".join(cur))
                        cur=[]
                    else:
                        cur.append(c)
                if len(cur)>=4: runs.append("".join(cur))
            for tok in re.findall(r"[A-Za-zÀ-ÿ]+",text):
                w="".join(c for c in (norm_letter(x) for x in tok) if c is not None)
                if len(w)>=4: lexicon[w]+=1
    if not runs: raise RuntimeError("no Latin runs")
    return runs,lexicon,{"files":files,"runs":len(runs),"chars":sum(map(len,runs)),"lexicon":len(lexicon)}


class LM4:
    def __init__(self,runs):
        c3=np.zeros(A**3,dtype=np.int64)
        c4=np.zeros(A**4,dtype=np.int64)
        self.c4_counter=Counter()
        for s in runs:
            xs=[AI[c] for c in s]
            for i in range(3,len(xs)):
                h=(xs[i-3]*A+xs[i-2])*A+xs[i-1]
                q=h*A+xs[i]
                c3[h]+=1; c4[q]+=1; self.c4_counter[s[i-3:i+1]]+=1
        cost=np.empty(A**4,dtype=np.float64)
        for h in range(A**3):
            den=c3[h]+ALPHA*A
            base=h*A
            for c in range(A):
                cost[base+c]=-math.log2((c4[base+c]+ALPHA)/den)
        self.cost=cost

    def score_texts(self,texts):
        nll=0.0; n=0
        for s in texts:
            xs=[AI[c] for c in s]
            for i in range(3,len(xs)):
                q=(((xs[i-3]*A+xs[i-2])*A+xs[i-1])*A+xs[i])
                nll += float(self.cost[q]); n += 1
        return (nll/n if n else float("inf")),n


def top5_fraction(texts):
    c=Counter("".join(texts)); n=sum(c.values())
    return sum(v for _,v in c.most_common(5))/n if n else 1.0


def latin_self_baseline(runs):
    rows=[]
    for f in range(5):
        tr=[s for i,s in enumerate(runs) if i%5!=f]
        he=[s for i,s in enumerate(runs) if i%5==f]
        lm=LM4(tr); ce,n=lm.score_texts(he)
        rows.append({"fold":f,"cross_entropy":ce,"scored_chars":n,"top5_char_fraction":top5_fraction(he)})
    return {
        "mean_cross_entropy":statistics.fmean(x["cross_entropy"] for x in rows),
        "mean_top5_char_fraction":statistics.fmean(x["top5_char_fraction"] for x in rows),
        "pooled_top5_char_fraction":top5_fraction(runs),
        "folds":rows,
    }


def raw_streams(items, leaves, parser, policy, count_slot):
    s10={v:i for i,v in enumerate(SLOT10)}
    sc={v:i for i,v in enumerate(COUNT_SLOTS[count_slot])}
    streams=[]; meta=[]; total_tokens=0; parsed_tokens=0
    for it in items:
        if it["leaf"] not in leaves: continue
        for li,line in enumerate(it["lines"]):
            cur=[]
            def flush():
                nonlocal cur
                if cur:
                    streams.append(np.asarray(cur,dtype=np.uint8))
                    meta.append({"page":it["page"],"paragraph":it["id"],"line_index":li})
                cur=[]
            for tok in line:
                total_tokens += 1
                p=parser.pick(tok,policy)
                if p is None:
                    flush(); continue
                vals=p[1]
                a=vals[10]; b=vals[count_slot]
                if a not in s10 or b not in sc:
                    raise RuntimeError(f"unexpected slot state slot10={a!r} slot{count_slot}={b!r}")
                cur.append(s10[a]*4+sc[b]); parsed_tokens += 1
            flush()
    return streams,meta,{"tokens":total_tokens,"parsed":parsed_tokens,"coverage":parsed_tokens/total_tokens if total_tokens else 0.0}


def patterns(streams):
    ctr=Counter()
    for s in streams:
        for i in range(len(s)-3):
            ctr[(int(s[i]),int(s[i+1]),int(s[i+2]),int(s[i+3]))]+=1
    if not ctr:
        return np.empty((0,4),dtype=np.uint8),np.empty(0,dtype=np.int64)
    ks=sorted(ctr)
    return np.asarray(ks,dtype=np.uint8),np.asarray([ctr[k] for k in ks],dtype=np.int64)


def char_maps(direction=0):
    out=np.empty((720,24),dtype=np.uint8)
    for raw_row in range(6):
        for col in range(4):
            raw=raw_row*4+col
            c=3-col if direction else col
            out[:,raw]=PERMS[:,raw_row]*4+c
    return out


def score_keys(streams,lm,direction=0):
    pats,cnts=patterns(streams)
    if not len(cnts): return np.full(720,np.inf),0
    maps=char_maps(direction)
    nll=np.zeros(720,dtype=np.float64)
    chunk=1500
    for z in range(0,len(cnts),chunk):
        p=pats[z:z+chunk]; w=cnts[z:z+chunk]
        a=maps[:,p[:,0]].astype(np.int32)
        b=maps[:,p[:,1]].astype(np.int32)
        c=maps[:,p[:,2]].astype(np.int32)
        d=maps[:,p[:,3]].astype(np.int32)
        q=(((a*A+b)*A+c)*A+d)
        nll += (lm.cost[q]*w[None,:]).sum(axis=1)
    return nll,int(cnts.sum())


def decode(streams,meta,perm_idx,direction=0):
    perm=PERMS[perm_idx]
    texts=[]; rows=[]
    for s,m in zip(streams,meta):
        chars=[]
        for raw in s:
            rr=int(raw)//4; cc=int(raw)%4
            if direction: cc=3-cc
            chars.append(ALPHABET[int(perm[rr])*4+cc])
        text="".join(chars); texts.append(text); rows.append({**m,"text":text})
    return texts,rows


def all_lexicon_hits(rows,lexicon,fold=None):
    hits=[]
    for m in rows:
        s=m["text"]
        for i in range(len(s)):
            for ln in range(4,min(15,len(s)-i)+1):
                w=s[i:i+ln]; freq=lexicon.get(w,0)
                if freq:
                    x={"word":w,"length":ln,"corpus_frequency":int(freq),"page":m.get("page"),"line_index":m.get("line_index"),"offset":i,"context":s[max(0,i-10):min(len(s),i+ln+10)]}
                    if fold is not None: x["fold"]=fold
                    hits.append(x)
    hits.sort(key=lambda x:(-x["length"],-x["corpus_frequency"],x["word"],str(x["page"]),x["line_index"],x["offset"]))
    return hits


def diagnostics(texts,rows,lm,lexicon,fold=None):
    ce,n=lm.score_texts(texts); chars=Counter("".join(texts)); total=sum(chars.values())
    grams=Counter()
    for s in texts: grams.update(s[i:i+4] for i in range(len(s)-3))
    hits=all_lexicon_hits(rows,lexicon,fold)
    return {
        "cross_entropy":ce,"scored_chars":n,"decoded_chars":total,"streams":len(texts),
        "top5_char_fraction":sum(v for _,v in chars.most_common(5))/total if total else 1.0,
        "char_counts":dict(chars.most_common()),
        "samples":[x for x in rows if len(x["text"])>=12][:20],
        "lexicon_hits":hits,
        "distinct_words_ge6":sorted({x["word"] for x in hits if x["length"]>=6}),
        "top_4grams":[{"ngram":g,"decoded_count":int(c),"latin_count":int(lm.c4_counter.get(g,0))} for g,c in grams.most_common(50)],
    }


def take_latin_prefix(runs,target,offset=0):
    rr=runs[offset:]+runs[:offset] if runs else []
    out=[]; total=0
    for s in rr:
        if total>=target: break
        take=min(len(s),target-total)
        if take>=4: out.append(s[:take]); total+=take
        elif take>0 and out:
            out[-1]+=s[:take]; total+=take
    if total<target: raise RuntimeError(f"Latin control short {total}<{target}")
    return out


def encode_control(plain_runs,hidden_perm):
    inv={int(hidden_perm[r]):r for r in range(6)}
    streams=[]
    for s in plain_runs:
        raw=[]
        for ch in s:
            idx=AI[ch]; hr=idx//4; col=idx%4
            raw.append(inv[hr]*4+col)
        streams.append(np.asarray(raw,dtype=np.uint8))
    return streams


def control_accuracy(streams,perm_idx,true_perm):
    chosen=PERMS[perm_idx]; correct=0; total=0
    for s in streams:
        for raw in s:
            rr=int(raw)//4; col=int(raw)%4
            pred=int(chosen[rr])*4+col
            truth=int(true_perm[rr])*4+col
            correct += pred==truth; total+=1
    return correct/total if total else 0.0


def positive_controls(latin_runs,lm,target_events):
    results=[]
    target=min(target_events,60000)
    for cidx in range(5):
        offset=(cidx*7919)%len(latin_runs)
        plain=take_latin_prefix(latin_runs,target,offset)
        rng=np.random.default_rng(seed32(f"Issue26E14:PositiveRow:v1:{cidx}"))
        hidden=np.arange(6,dtype=np.uint8); rng.shuffle(hidden)
        enc=encode_control(plain,hidden)
        held=[s for i,s in enumerate(enc) if i%5==cidx]
        train=[s for i,s in enumerate(enc) if i%5!=cidx]
        nll,cnt=score_keys(train,lm,0); ce=np.divide(nll,cnt) if cnt else np.full(720,np.inf)
        k=int(np.argmin(ce))
        held_nll,held_cnt=score_keys(held,lm,0)
        true_idx=next(i for i,p in enumerate(PERMS) if np.array_equal(p,hidden))
        acc=control_accuracy(held,k,hidden)
        results.append({
            "control":cidx,"target_chars":target,"hidden_perm":hidden.tolist(),"selected_perm":PERMS[k].tolist(),
            "exact_hidden_perm":bool(k==true_idx),"weighted_letter_accuracy":acc,
            "recovered_held_ce":float(held_nll[k]/held_cnt),"true_held_ce":float(held_nll[true_idx]/held_cnt),
            "held_scored_chars":int(held_cnt),
        })
    exact=sum(x["exact_hidden_perm"] for x in results)
    mean_acc=statistics.fmean(x["weighted_letter_accuracy"] for x in results)
    rec=statistics.fmean(x["recovered_held_ce"] for x in results)
    tru=statistics.fmean(x["true_held_ce"] for x in results)
    passed=(exact>=4 and mean_acc>=.99 and rec-tru<=.02)
    return {"passed":passed,"exact_hidden_perm_controls":exact,"mean_weighted_accuracy":mean_acc,"mean_recovered_held_ce":rec,"mean_true_held_ce":tru,"mean_ce_excess":rec-tru,"controls":results}


def run_policy(items,parser,policy,lm,lexicon,directions=(0,)):
    folds=e.physical_leaf_folds(items)
    fs=[]
    for fi,held in enumerate(folds):
        slot_data={}
        for slot in (6,9):
            streams,meta,cov=raw_streams(items,held,parser,policy,slot)
            dir_scores={}
            for direction in directions:
                nll,cnt=score_keys(streams,lm,direction)
                dir_scores[direction]=(nll,cnt)
            slot_data[slot]={"streams":streams,"meta":meta,"coverage":cov,"scores":dir_scores}
        fs.append({"fold":fi,"held":held,"slots":slot_data})

    totals={}
    for slot in (6,9):
        for direction in directions:
            totals[(slot,direction)]=sum((f["slots"][slot]["scores"][direction][0] for f in fs),np.zeros(720)),sum(f["slots"][slot]["scores"][direction][1] for f in fs)

    selected=[]; fold_rows=[]; pooled_texts=[]; pooled_rows=[]; all_hits=[]
    for f in fs:
        candidates=[]
        for direction in directions:
            for slot in (6,9):
                hn,hc=f["slots"][slot]["scores"][direction]
                tn,tc=totals[(slot,direction)]
                trn=tn-hn; trc=tc-hc
                ce=trn/trc if trc else np.full(720,np.inf)
                for k in range(720):
                    candidates.append((float(ce[k]),direction,slot,k))
        # Explicit tie priority: ascending direction, slot6, lexicographic permutation.
        best=min(candidates,key=lambda x:(x[0],x[1],0 if x[2]==6 else 1,x[3]))
        trce,direction,slot,k=best
        streams=f["slots"][slot]["streams"]; meta=f["slots"][slot]["meta"]
        texts,rows=decode(streams,meta,k,direction)
        dg=diagnostics(texts,rows,lm,lexicon,f["fold"])
        key=(slot,direction,tuple(int(x) for x in PERMS[k]))
        selected.append(key); pooled_texts.extend(texts); pooled_rows.extend(rows); all_hits.extend(dg["lexicon_hits"])
        fold_rows.append({"fold":f["fold"],"held_leaves":sorted(f["held"]),"training_cross_entropy":trce,
                          "count_slot":slot,"count_direction":"reverse" if direction else "ascending",
                          "instrument_perm":PERMS[k].tolist(),"coverage":f["slots"][slot]["coverage"],"held":dg})
    rec=Counter(selected); modal,count=min(rec.items(),key=lambda kv:(-kv[1],kv[0]))
    pooled_ce,pooled_n=lm.score_texts(pooled_texts)
    chars=Counter("".join(pooled_texts)); total=sum(chars.values())
    distinct_ge6=sorted({h["word"] for h in all_hits if h["length"]>=6})
    folds_ge6=sorted({h["fold"] for h in all_hits if h["length"]>=6})
    return {
        "policy":policy,"directions":["reverse" if x else "ascending" for x in directions],
        "exact_key_recurrence":int(count),
        "modal_key":{"count_slot":modal[0],"direction":"reverse" if modal[1] else "ascending","instrument_perm":list(modal[2])},
        "mean_fold_cross_entropy":statistics.fmean(x["held"]["cross_entropy"] for x in fold_rows),
        "pooled_cross_entropy":pooled_ce,"pooled_scored_chars":pooled_n,
        "pooled_top5_char_fraction":sum(v for _,v in chars.most_common(5))/total if total else 1.0,
        "distinct_words_ge6":distinct_ge6,"distinct_words_ge6_count":len(distinct_ge6),"folds_with_words_ge6":folds_ge6,
        "folds":fold_rows,
    }


def classify(primary,baseline,positive):
    if not positive["passed"]: return "SOLVER INADEQUATE",{}
    gates={
        "exact_key_recurrence_ge4":primary["exact_key_recurrence"]>=4,
        "ce_within_0_50":primary["mean_fold_cross_entropy"]<=baseline["mean_cross_entropy"]+.50,
        "top5_within_0_15":primary["pooled_top5_char_fraction"]<=baseline["pooled_top5_char_fraction"]+.15,
        "ten_distinct_words_ge6":primary["distinct_words_ge6_count"]>=10,
        "word_hits_across_3folds":len(primary["folds_with_words_ge6"])>=3,
    }
    if all(gates.values()): return "KIRCHER 6X4 PLAINTEXT LEAD",gates
    return "NO READABLE KIRCHER 6X4 PLAINTEXT",gates


def main():
    if len(sys.argv)!=3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT",file=sys.stderr); return 2
    zl=Path(sys.argv[1]).resolve(); root=Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes())!=e.EXPECTED_ZL3B_BLOB: raise RuntimeError("ZL blob mismatch")
    parser=e.SlotParser(); validation=e.validate_parser(parser); items=e.parse_voynich(zl)
    runs,lexicon,lmeta=load_latin(root); baseline=latin_self_baseline(runs); lm=LM4(runs)
    # Positive-control volume follows the eligible min parsed-token scale but is capped to frozen corpus practicality.
    all_leaves=set().union(*e.physical_leaf_folds(items))
    _,_,cov=raw_streams(items,all_leaves,parser,"min",6)
    positive=positive_controls(runs,lm,cov["parsed"])
    primary=run_policy(items,parser,"min",lm,lexicon,(0,))
    max_sensitivity=run_policy(items,parser,"max",lm,lexicon,(0,))
    reversal_sensitivity=run_policy(items,parser,"min",lm,lexicon,(0,1))
    classification,gates=classify(primary,baseline,positive)
    low=primary["pooled_top5_char_fraction"]>=.90
    out={
        "experiment":"Issue26E14 Kircher 1650 six-instrument x four-count plaintext probe",
        "classification":classification,"anti_collapse":"LOW-DIVERSITY OPTIMUM" if low else "NO LOW-DIVERSITY FLAG",
        "historical_alphabet":"".join(ALPHABET),"historical_table":[list(ALPHABET[r*4:(r+1)*4]) for r in range(6)],
        "interpretation":{"gates":gates},"slot_parser_validation":validation,"latin_population":lmeta,
        "latin_self_baseline":baseline,"positive_control":positive,"primary_min":primary,
        "max_sensitivity":max_sensitivity,"ordinal_reversal_sensitivity":reversal_sensitivity,
    }
    json.dump(out,sys.stdout,ensure_ascii=False,indent=2,sort_keys=True); print(); return 0


if __name__=="__main__": raise SystemExit(main())
