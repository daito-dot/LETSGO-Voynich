#!/usr/bin/env python3
"""Phase60B feature attribution.

Requires a local ZL3b/EVA transcription. The repository intentionally does not
redistribute that third-party source. Usage:
  python phase60b_feature_attribution.py /path/to/eva_zl3b.txt

Implements physical-leaf cross-fitted real paragraph line0->line2 versus
internal pseudo-boundary comparisons across three EVA unit representations.
"""
import re, sys, json
import numpy as np
from collections import defaultdict, Counter

SRC=sys.argv[1] if len(sys.argv)>1 else "eva_zl3b.txt"
raw=open(SRC,encoding="utf-8",errors="ignore").read().splitlines()
HP=re.compile(r'^<(?P<p>f\d+[rv]\d*)>\s+<!\s*(?P<m>.*?)>')
LP=re.compile(r'^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<c>[^>]*)>\s+(?P<b>.*)$')
headers={}; pars=defaultdict(list); pid=defaultdict(int)
def tokens(body):
    st='<%>' in body; body=body.replace('<%>',' '); body=re.sub(r'<[^>]*>',' ',body)
    z=[re.sub(r'[^A-Za-z]','',x).lower() for x in re.split(r'[.\s]+',body)]
    return st,[x for x in z if x]
for s in raw:
    h=HP.match(s)
    if h: headers[h.group('p')]=dict(re.findall(r'\$(\w)=([^\s>]+)',h.group('m'))); continue
    m=LP.match(s)
    if not m or 'P' not in m.group('c'): continue
    page=m.group('loc').split('.')[0]; st,z=tokens(m.group('b'))
    if st: pid[page]+=1
    if z and pid[page]: pars[(page,pid[page])].append(z)

def lev1(a,b):
    if a==b or abs(len(a)-len(b))>1:return False
    if len(a)==len(b):return sum(x!=y for x,y in zip(a,b))==1
    if len(a)>len(b):a,b=b,a
    i=j=d=0
    while i<len(a) and j<len(b):
        if a[i]==b[j]:i+=1;j+=1
        else:d+=1;j+=1
        if d>1:return False
    return True

def entropy(v):
    c=Counter(v)
    if not c:return 0.
    q=np.array(list(c.values()),float);q/=q.sum();return float(-(q*np.log2(q)).sum())

def segment(t,mode):
    comps=[]
    if mode=='conservative': comps=['cth','ckh','cph','cfh','ch','sh']
    elif mode=='phase56': comps=['cth','ckh','cph','cfh','ch','sh','iin','in','ee']
    if not comps:return list(t)
    out=[];i=0
    comps=sorted(comps,key=len,reverse=True)
    while i<len(t):
        hit=next((c for c in comps if t.startswith(c,i)),None)
        if hit:out.append(hit);i+=len(hit)
        else:out.append(t[i]);i+=1
    return out

def feat(toks,mode):
    units=[segment(t,mode) for t in toks]; n=len(toks); lens=np.array([len(u) for u in units],float)
    flat=[u for x in units for u in x]
    ef=sum(any(lev1(a,b) for j,b in enumerate(toks) if i!=j) for i,a in enumerate(toks))/n
    loc=sum(any(lev1(a,b) for b in toks[max(0,i-10):i]) for i,a in enumerate(toks))/n
    kt=sum(('k' in t or 't' in t) for t in toks)/n; k=sum(t.count('k') for t in toks); tt=sum(t.count('t') for t in toks)
    return np.array([len(set(toks))/n,lens.mean(),lens.std(),len(set(flat)),entropy(flat),entropy([u[0] for u in units]),entropy([u[-1] for u in units]),ef,loc,kt,k/(k+tt) if k+tt else 0.])

names=['ttr','mean_len','sd_len','unit_inventory','unit_entropy','first_entropy','last_entropy','edit1_fraction','local_prev10','kt_mass','k_share']
groups={'lexical_diversity':[0],'length':[1,2],'edge_entropy':[5,6],'near_family':[7,8],'kt':[9,10]}
records=[]
for (page,p),LL in pars.items():
    if len(LL)>=3 and len(LL[0])>=5 and len(LL[2])>=5:
        records.append((page,int(re.match(r'f(\d+)',page).group(1)),headers.get(page,{}).get('I','?'),LL))

def run(mode):
    all_lines=[feat(L,mode) for _,_,_,LL in records for L in LL if len(L)>=5]
    sd=np.std(np.array(all_lines),axis=0);sd[sd==0]=1
    leaves=np.array([r[1] for r in records]); ul=np.unique(leaves); folds=[set(ul[i::5]) for i in range(5)]
    deltas=[]; secs=[]
    for testleaves in folds:
        tr=[r for r in records if r[1] not in testleaves]; te=[r for r in records if r[1] in testleaves]
        train_trans=np.array([(feat(r[3][2],mode)-feat(r[3][0],mode))/sd for r in tr])
        direction=train_trans.mean(0); norm=np.linalg.norm(direction); direction=direction/norm if norm else direction
        for page,leaf,sec,LL in te:
            pseudo=[]
            for j in range(1,len(LL)-2):
                if len(LL[j])>=5 and len(LL[j+2])>=5:pseudo.append((feat(LL[j+2],mode)-feat(LL[j],mode))/sd)
            if not pseudo:continue
            real=(feat(LL[2],mode)-feat(LL[0],mode))/sd
            deltas.append(real-np.mean(pseudo,axis=0));secs.append(sec)
    D=np.array(deltas); direction=D.mean(0); direction/=np.linalg.norm(direction)
    coord=D.mean(0)*direction
    full=float(np.mean(D@direction))
    ablation={}
    for g,ix in groups.items():
        keep=[i for i in range(11) if i not in ix]; d=direction[keep]; d=d/np.linalg.norm(d)
        ablation[g]=float(full-np.mean(D[:,keep]@d))
    section={s:{'n':int(sum(x==s for x in secs)),'mean_projection':float(np.mean((D@direction)[np.array(secs)==s]))} for s in 'HBPST' if s in secs}
    return {'n':len(D),'mean_projection':full,'coordinate_contribution':dict(zip(names,map(float,coord))),'group_ablation_loss':ablation,'sections':section}

out={m:run(m) for m in ['raw','conservative','phase56']}
print(json.dumps(out,indent=2,ensure_ascii=False))
