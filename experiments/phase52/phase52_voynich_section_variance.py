import re,json,statistics,random
from pathlib import Path
from collections import defaultdict
COMPOSITES=sorted(['cth','ckh','cph','cfh','ch','sh','iin','in','ee'],key=len,reverse=True)
VPAT=re.compile(r'^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<code>[^>]*)>\s+(?P<body>.*)$')

def clean(b):
 b=b.replace('<->','.'); b=re.sub(r'<[^>]*>','.',b)
 return [p for p in re.split(r'[.,\s]+',b.lower()) if p and re.fullmatch(r'[a-z]+',p)]
def coll(t):
 out=[];i=0
 while i<len(t):
  for c in COMPOSITES:
   if t.startswith(c,i):out.append(c);i+=len(c);break
  else:out.append(t[i]);i+=1
 return tuple(out)
def ed1(a,b):
 la,lb=len(a),len(b)
 if abs(la-lb)>1:return False
 if la==lb:return sum(x!=y for x,y in zip(a,b))==1
 if la>lb:a,b=b,a;la,lb=lb,la
 for j in range(lb):
  if a==b[:j]+b[j+1:]:return True
 return False
def coverage(toks):
 types=list(set(toks)); near=set()
 for i,a in enumerate(types):
  for b in types[i+1:]:
   if ed1(a,b):near.add(a);near.add(b)
 return len(near)/len(types) if types else 0
sections={}
def add(nums,sec):
 for n in nums:sections[f'f{n}']=sec
add(list(range(1,12))+list(range(13,26)),'herbal_a')
add(list(range(26,59))+[65,66],'herbal_b')
add(range(67,74),'astronomical')
add(range(75,85),'biological')
add([85,86],'cosmological')
add([87,88,89,90,99,100,101,102],'pharmaceutical')
add([103,104,105,106,107,108,111,112,113,114,115,116],'recipes')
folios=defaultdict(list)
for raw in Path('eva_zl3b(1).txt').read_text().splitlines():
 m=VPAT.match(raw)
 if not m or 'P' not in m.group('code'):continue
 fid=re.match(r'(f\d+)',m.group('loc')).group(1)
 if fid not in sections:continue
 ts=[coll(t) for t in clean(m.group('body'))]
 if len(ts)>1:folios[fid].extend(ts[1:]) # same line-first exclusion
rows=[]
for fid,toks in folios.items():
 if len(toks)>=100:rows.append({'folio':fid,'section':sections[fid],'tokens':len(toks),'types':len(set(toks)),'edit1_type_fraction':coverage(toks)})
by=defaultdict(list)
for r in rows:by[r['section']].append(r['edit1_type_fraction'])
summary={s:{'n_folios':len(v),'median':statistics.median(v),'mean':statistics.mean(v),'min':min(v),'max':max(v),'sd':statistics.stdev(v) if len(v)>1 else None} for s,v in by.items()}
# variance decomposition: unweighted folios, eta^2 section / total
ys=[r['edit1_type_fraction'] for r in rows]; grand=statistics.mean(ys)
ss_total=sum((y-grand)**2 for y in ys)
ss_between=sum(len(by[s])*(statistics.mean(by[s])-grand)**2 for s in by)
eta=ss_between/ss_total if ss_total else 0
# bootstrap medians by section
rng=random.Random(52002)
for s,v in by.items():
 if len(v)>1:
  bs=[statistics.median([rng.choice(v) for _ in v]) for _ in range(3000)];bs.sort()
  summary[s]['median_boot95']=[bs[74],bs[2924]]
out={'phase':'52A','metric':'folio-level edit1 type coverage, line-first token excluded','n_folios':len(rows),'section_eta_squared':eta,'overall':{'median':statistics.median(ys),'min':min(ys),'max':max(ys)},'by_section':summary,'folios':sorted(rows,key=lambda r:(r['section'],r['folio']))}
Path('phase52_voynich_section_variance_results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,indent=2,ensure_ascii=False))
# Matched 141-token contiguous-window sensitivity, 100 windows/folio where possible.
rng=random.Random(52003); matched=[]
for fid,toks in folios.items():
 if len(toks)<141:continue
 vals=[]
 starts=list(range(len(toks)-140))
 for _ in range(100):
  st=rng.choice(starts); vals.append(coverage(toks[st:st+141]))
 matched.append({'folio':fid,'section':sections[fid],'median141':statistics.median(vals),'mean141':statistics.mean(vals)})
bm=defaultdict(list)
for r in matched:bm[r['section']].append(r['median141'])
ms={s:{'n_folios':len(v),'median_of_folio_medians':statistics.median(v),'mean':statistics.mean(v),'min':min(v),'max':max(v)} for s,v in bm.items()}
ys2=[r['median141'] for r in matched];g=statistics.mean(ys2);sst=sum((y-g)**2 for y in ys2);ssb=sum(len(bm[s])*(statistics.mean(bm[s])-g)**2 for s in bm)
out2={'phase':'52A_matched141','n_folios':len(matched),'section_eta_squared':ssb/sst if sst else 0,'overall':{'median':statistics.median(ys2),'min':min(ys2),'max':max(ys2)},'by_section':ms,'folios':matched}
Path('phase52_voynich_section_matched141_results.json').write_text(json.dumps(out2,indent=2,ensure_ascii=False)+'\n')
print('\nMATCHED141\n'+json.dumps(out2,indent=2,ensure_ascii=False))
