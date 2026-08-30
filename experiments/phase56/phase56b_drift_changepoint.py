#!/usr/bin/env python3
"""Phase56B: compare smooth physical drift with discrete regimes.

Consumes the audited 56A page-side CSV. Evaluation is block-held-out and
restricted to sufficiently populated section/Currier/hand strata where possible.
"""
import argparse,csv,json,math
from collections import Counter,defaultdict
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error

FEATURES=['ttr','mean_len','sd_len','edit1_fraction','local_prev10','linepos_mi','first_entropy','last_entropy','unit_entropy','kt_mass','k_share_within_kt']

def load(path):
    rows=list(csv.DictReader(open(path,encoding='utf-8')))
    keep=[]
    for r in rows:
        if int(float(r['n_tokens'])) < 40: continue
        x=[]
        try:x=[float(r[f]) for f in FEATURES]
        except (ValueError,KeyError):continue
        if not all(math.isfinite(v) for v in x):continue
        r['_x']=x;r['_leaf']=int(r['physical_leaf']);keep.append(r)
    return keep

def interp_predict(train,test):
    # distance-weighted smooth prediction from physical neighbors within stratum
    out=[]
    for q in test:
        cand=[r for r in train if (r['section'],r['currier'],r['hand'])==(q['section'],q['currier'],q['hand'])]
        if len(cand)<2:cand=[r for r in train if r['section']==q['section']]
        if not cand:continue
        ds=np.array([abs(r['_leaf']-q['_leaf']) for r in cand],float)
        w=1/(1+ds);X=np.array([r['_x'] for r in cand]);out.append((q['_x'],np.average(X,axis=0,weights=w)))
    return out

def nearest_regime_predict(train,test,k):
    X=np.array([r['_x'] for r in train]);sc=StandardScaler().fit(X);Z=sc.transform(X)
    km=KMeans(n_clusters=min(k,len(train)),random_state=5602,n_init=20).fit(Z)
    centers=np.array([X[km.labels_==j].mean(axis=0) for j in range(km.n_clusters)])
    out=[]
    for q in test:
        z=sc.transform([q['_x']])[0]
        # regime assignment uses only metadata/physical neighborhood proxy: choose modal cluster among nearest physical training sides
        cand=sorted(range(len(train)),key=lambda i:(0 if train[i]['section']==q['section'] else 1,abs(train[i]['_leaf']-q['_leaf'])))[:8]
        lab=Counter(km.labels_[cand]).most_common(1)[0][0]
        out.append((q['_x'],centers[lab]))
    return out

def baseline(train,test):
    by=defaultdict(list)
    for r in train:by[r['section']].append(r['_x'])
    glob=np.mean([r['_x'] for r in train],axis=0);out=[]
    for q in test:out.append((q['_x'],np.mean(by[q['section']],axis=0) if by[q['section']] else glob))
    return out

def mse(pairs):
    if not pairs:return None
    a=np.array([x for x,y in pairs]);b=np.array([y for x,y in pairs]);return float(np.mean((a-b)**2))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('page_csv');ap.add_argument('--out',default='phase56b_results.json');a=ap.parse_args()
    rows=load(a.page_csv); leaves=sorted(set(r['_leaf'] for r in rows)); blocks=np.array_split(leaves,5)
    folds=[]
    for bi,b in enumerate(blocks):
        b=set(int(x) for x in b);tr=[r for r in rows if r['_leaf'] not in b];te=[r for r in rows if r['_leaf'] in b]
        z={'fold':bi,'n_train':len(tr),'n_test':len(te),'section_baseline':mse(baseline(tr,te)),'smooth_physical':mse(interp_predict(tr,te))}
        for k in [2,3,4,6,8]:z[f'regime_k{k}']=mse(nearest_regime_predict(tr,te,k))
        folds.append(z)
    keys=[k for k in folds[0] if k not in {'fold','n_train','n_test'}]
    summary={k:float(np.mean([f[k] for f in folds if f[k] is not None])) for k in keys}
    out={'phase':'56B','status':'development','n_page_sides':len(rows),'features':FEATURES,'cv':'5 contiguous physical-leaf blocks','folds':folds,'mean_mse':summary}
    open(a.out,'w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
