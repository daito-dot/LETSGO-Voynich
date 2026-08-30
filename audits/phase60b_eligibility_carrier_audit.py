#!/usr/bin/env python3
"""Second-stage Phase60B audit: recover eligibility and signed carrier effects.

Read-only diagnostic. It tests plausible historical eligibility conventions against
the frozen Phase60B n=380 result, then reports signed standardized real-minus-pseudo
feature deltas under true physical-leaf cross-fitting for the best matching convention.
"""
from __future__ import annotations
import argparse, json, random, re
from collections import defaultdict
from pathlib import Path
import numpy as np
import phase60b_crossfit_audit as a


def parse_candidates(text: str, exclude_first: bool, min_tokens: int):
    headers={}; pars=defaultdict(list); pid=defaultdict(int)
    for s in text.splitlines():
        h=a.HP.match(s)
        if h:
            headers[h.group('p')]=dict(re.findall(r'\$(\w)=([^\s>]+)',h.group('m'))); continue
        m=a.LP.match(s)
        if not m or 'P' not in m.group('c'): continue
        page=m.group('loc').split('.')[0]; start,z=a.tokens(m.group('b'))
        if exclude_first: z=z[1:] if len(z)>1 else []
        if start: pid[page]+=1
        if z and pid[page]: pars[(page,pid[page])].append(z)
    records=[]
    for (page,_),LL in pars.items():
        if len(LL)>=3 and len(LL[0])>=min_tokens and len(LL[2])>=min_tokens:
            records.append((page,int(re.match(r'f(\d+)',page).group(1)),headers.get(page,{}).get('I','?'),LL))
    return records


def paired_count(records, min_tokens):
    n=0
    for _page,_leaf,_sec,LL in records:
        ok=False
        for j in range(1,len(LL)-2):
            if len(LL[j])>=min_tokens and len(LL[j+2])>=min_tokens:
                ok=True; break
        n+=int(ok)
    return n


def sd_train(records,mode,min_tokens):
    X=[a.feat(L,mode) for _,_,_,LL in records for L in LL if len(L)>=min_tokens]
    sd=np.std(np.array(X),axis=0);sd[sd==0]=1
    return sd


def signed_crossfit(records,mode,min_tokens):
    leaves=np.unique([r[1] for r in records]); folds=[set(leaves[i::5]) for i in range(5)]
    rows=[]; fold_summary=[]
    for fi,testleaves in enumerate(folds):
        tr=[r for r in records if r[1] not in testleaves]; te=[r for r in records if r[1] in testleaves]
        sd=sd_train(tr,mode,min_tokens)
        train_trans=np.array([(a.feat(r[3][2],mode)-a.feat(r[3][0],mode))/sd for r in tr])
        direction=train_trans.mean(0); nn=np.linalg.norm(direction); direction=direction/nn if nn else direction
        fp=[]
        for page,leaf,sec,LL in te:
            pseudo=[]
            for j in range(1,len(LL)-2):
                if len(LL[j])>=min_tokens and len(LL[j+2])>=min_tokens:
                    pseudo.append((a.feat(LL[j+2],mode)-a.feat(LL[j],mode))/sd)
            if not pseudo: continue
            delta=(a.feat(LL[2],mode)-a.feat(LL[0],mode))/sd-np.mean(pseudo,axis=0)
            proj=float(delta@direction);fp.append(proj)
            rows.append({'fold':fi,'page':page,'leaf':leaf,'section':sec,'projection':proj,'delta':delta})
        fold_summary.append({'fold':fi,'n':len(fp),'mean_projection':float(np.mean(fp)) if fp else None})
    D=np.array([r['delta'] for r in rows]); signed=D.mean(0)
    byleaf=defaultdict(list)
    for r in rows:byleaf[r['leaf']].append(r)
    ids=sorted(byleaf);rng=random.Random(60991+a.MODES.index(mode));boots=[]
    for _ in range(4000):
        sample=[rng.choice(ids) for _ in ids]
        rr=[x for leaf in sample for x in byleaf[leaf]]
        boots.append(np.mean(np.array([x['delta'] for x in rr]),axis=0))
    B=np.array(boots); stable={}
    for i,name in enumerate(a.NAMES):
        lo,hi=float(np.quantile(B[:,i],.025)),float(np.quantile(B[:,i],.975))
        if lo>0 or hi<0:stable[name]={'effect':float(signed[i]),'boot95':[lo,hi]}
    return {'n':len(rows),'mean_projection':float(np.mean([r['projection'] for r in rows])),
            'folds':fold_summary,'signed_effects':dict(zip(a.NAMES,map(float,signed))),
            'stable_signed_effects':stable}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',default='eva_zl3b.txt');ap.add_argument('--out',default='phase60b_eligibility_carrier_audit_results.json');args=ap.parse_args()
    data=a.get_source(Path(args.source));text=data.decode('utf-8',errors='ignore')
    scenarios=[]
    for exclude_first in [False,True]:
        for min_tokens in [4,5,6,7,8]:
            rec=parse_candidates(text,exclude_first,min_tokens)
            scenarios.append({'exclude_first_token':exclude_first,'min_tokens':min_tokens,'eligible':len(rec),'paired':paired_count(rec,min_tokens)})
    best=min(scenarios,key=lambda x:(abs(x['paired']-380),abs(x['eligible']-380)))
    records=parse_candidates(text,best['exclude_first_token'],best['min_tokens'])
    out={'audit':'Phase60B eligibility and signed-carrier sensitivity','target_historical_n':380,'scenarios':scenarios,'closest_scenario':best,
         'corrected_train_only_crossfit':{m:signed_crossfit(records,m,best['min_tokens']) for m in a.MODES}}
    Path(args.out).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
