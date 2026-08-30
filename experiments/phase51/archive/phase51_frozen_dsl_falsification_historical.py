import re, random, json, math, statistics
from pathlib import Path
from collections import Counter,defaultdict

# Phase50-selected family frozen BEFORE these target dimensions are evaluated.
SPEC=dict(nroots=64,block=4,state_use=0.30,prefix_p=0.22,suffix_p=0.32,variants_per_root=2)
ALPHA='abcdefghiklmnoprstuy'
VPAT=re.compile(r'^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<code>[^>]*)>\s+(?P<body>.*)$')
BAD=re.compile(r'[^a-z]')
COMPOSITES=sorted(['cth','ckh','cph','cfh','ch','sh','iin','in','ee'],key=len,reverse=True)
def clean(b):
 b=b.replace('<->','.'); b=re.sub(r'<[^>]*>','.',b)
 return [p for p in re.split(r'[.,\s]+',b.lower()) if p and not BAD.search(p)]
def coll(t):
 out=[];i=0
 while i<len(t):
  for c in COMPOSITES:
   if t.startswith(c,i):out.append(c);i+=len(c);break
  else:out.append(t[i]);i+=1
 return tuple(out)

def parse_layout():
 by=defaultdict(list)
 for raw in Path('/mnt/data/eva_zl3b(1).txt').read_text().splitlines():
  m=VPAT.match(raw)
  if not m or 'P' not in m.group('code'):continue
  ts=[coll(t) for t in clean(m.group('body'))]
  if len(ts)<=1:continue
  f=re.match(r'f\d+',m.group('loc')).group()
  by[f].append({'n':len(ts)-1,'start':'<%>' in m.group('body')}) # first token excluded
 return by
LAY=parse_layout()

def gen(n,seed):
 r=random.Random(seed); bases=[]
 while len(bases)<SPEC['nroots']:
  s=''.join(r.choice(ALPHA) for _ in range(3))
  if s not in bases:bases.append(s)
 fam=[]
 for s in bases:
  c=r.choice([x for x in ALPHA if x!=s[-1]])
  fam.append([s,s[:-1]+c])
 out=[];state=0
 for i in range(n):
  if i%SPEC['block']==0:state=r.randrange(SPEC['nroots'])
  j=state if r.random()<SPEC['state_use'] else r.randrange(SPEC['nroots'])
  tok=r.choice(fam[j])
  if r.random()<SPEC['prefix_p']:tok=r.choice(['','q'])+tok
  if r.random()<SPEC['suffix_p']:tok+=r.choice(['n','r','y'])
  out.append(tuple(tok))
 return out

def make_pages(seed):
 pages={}; rr=random.Random(seed)
 for f,ls in LAY.items():
  stream=gen(sum(x['n'] for x in ls),rr.randrange(10**9)); j=0; lines=[]
  for x in ls: lines.append(stream[j:j+x['n']]);j+=x['n']
  pages[f]=lines
 return pages

def lev1(a,b):
 if abs(len(a)-len(b))>1:return False
 if len(a)==len(b):return sum(x!=y for x,y in zip(a,b))==1
 if len(a)>len(b):a,b=b,a
 for i in range(len(b)):
  if a==b[:i]+b[i+1:]:return True
 return False

def near(A,B):
 A=set(A);B=set(B)
 if not B:return 0
 return sum(any(a!=b and lev1(a,b) for a in A) for b in B)/len(B)

def boundary_gap(pages):
 vals=defaultdict(lambda:defaultdict(list))
 for f,lines in pages.items():
  meta=LAY[f]
  for i in range(1,len(lines)):
   vals[f][0 if meta[i]['start'] else 1].append(near(lines[i-1],lines[i]))
 fg=[]
 for f,d in vals.items():
  if d[0] and d[1]:fg.append(statistics.mean(d[1])-statistics.mean(d[0]))
 return statistics.mean(fg) if fg else 0

def mi(pairs):
 J=Counter(pairs);n=sum(J.values());cx=Counter(x for x,y in pairs);cy=Counter(y for x,y in pairs)
 return sum((v/n)*math.log2((v/n)/((cx[x]/n)*(cy[y]/n))) for (x,y),v in J.items()) if n else 0

def sig(t):return (t[0],t[-1],min(len(t),7)) if t else ('','',0)
def linepos_mi(pages):
 p=[]
 for lines in pages.values():
  for line in lines:
   for i,t in enumerate(line):p.append(('first' if i==0 else 'last' if i==len(line)-1 else 'middle',sig(t)))
 return mi(p)
def phase4(pages):
 p=[]
 for lines in pages.values():
  for line in lines:
   k=0
   for t in line:
    for u in t:p.append((k%4,u));k+=1
 return mi(p)
def shuffle_tokens(pages,r):
 return {f:[(lambda x:(r.shuffle(x),x)[1])(line[:]) for line in ls] for f,ls in pages.items()}
def period_excess(pages,seed):
 r=random.Random(seed);o=phase4(pages);ns=[phase4(shuffle_tokens(pages,r)) for _ in range(1)]
 return o-statistics.mean(ns)

# Voynich target directly from same layout/preprocessing
V={};
for f,ls in LAY.items():V[f]=[]
# reparse tokens
for raw in Path('/mnt/data/eva_zl3b(1).txt').read_text().splitlines():
 m=VPAT.match(raw)
 if not m or 'P' not in m.group('code'):continue
 ts=[coll(t) for t in clean(m.group('body'))]
 if len(ts)<=1:continue
 f=re.match(r'f\d+',m.group('loc')).group();V[f].append(ts[1:])
vt={'boundary_gap':boundary_gap(V),'line_position_mi':linepos_mi(V),'period4_token_shuffle_excess_mi':period_excess(V,51111)}

R=[]
for k in range(20):
 P=make_pages(51000+k)
 R.append({'boundary_gap':boundary_gap(P),'line_position_mi':linepos_mi(P),'period4_token_shuffle_excess_mi':period_excess(P,52000+k)})
def summ(key):
 x=sorted(r[key] for r in R);v=vt[key]
 return {'voynich':v,'dsl_median':statistics.median(x),'dsl_95':[x[0],x[19]],'dsl_minmax':[x[0],x[-1]],'fraction_dsl_ge_voynich':sum(z>=v for z in x)/len(x)}
out={'phase':51,'status':'frozen-after-phase50-selection; no retuning on these dimensions','spec':SPEC,'layout':'empirical Voynich folio/line/paragraph lengths; generator not informed of line or paragraph boundaries','replicates':20,'results':{k:summ(k) for k in vt},'raw_replicates':R}
Path('/mnt/data/phase51_frozen_dsl_falsification_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'spec':SPEC,'results':out['results']},indent=2))