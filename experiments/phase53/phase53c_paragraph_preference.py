# Run from the historical research workspace with phase53_hierarchical_ablation.py available.
exec(open('/mnt/data/phase53_hierarchical_ablation.py').read().split('DEV_FOLIOS=')[0])

def gen_pref(seed,para_bias=0.1,n_pref=1,line_strength=0.0):
 r=random.Random(seed);fam=roots(seed+99173);pages={};state=r.randrange(SPEC['nroots']);global_i=0
 for f,meta in LAY.items():
  lines=[];pref=r.sample(range(SPEC['nroots']),n_pref)
  for li,x in enumerate(meta):
   if x['start'] or li==0:
    pref=r.sample(range(SPEC['nroots']),n_pref);state=r.randrange(SPEC['nroots'])
   line=[]
   for k in range(x['n']):
    if global_i%SPEC['block']==0:state=r.randrange(SPEC['nroots'])
    if r.random()<para_bias:j=r.choice(pref)
    elif r.random()<SPEC['state_use']:j=state
    else:j=r.randrange(SPEC['nroots'])
    base=r.choice(fam[j]);pp=SPEC['prefix_p'];sp=SPEC['suffix_p']
    pos='first' if k==0 else 'last' if k==x['n']-1 else 'middle'
    if line_strength:
     if pos=='first':pp=min(.95,pp+line_strength);sp=max(0,sp-line_strength/2)
     elif pos=='last':sp=min(.95,sp+line_strength);pp=max(0,pp-line_strength/2)
     else:pp=max(0,pp-line_strength/8);sp=max(0,sp-line_strength/8)
    if r.random()<pp:base=r.choice(['','q'])+base
    if r.random()<sp:base+=r.choice(['n','r','y'])
    line.append(tuple(base));global_i+=1
   lines.append(line)
  pages[f]=lines
 return pages
TARGET={'density141':matched_density(V,61000,nwin=20),'local_excess':local_excess(V,61001,nshuf=1),'boundary_gap':boundary_gap(V),'line_mi':linepos_mi(V)}
line_rows=[]
for i,ls in enumerate([0.10,0.20,0.25,0.30,0.35,0.40]):
 P=gen_pref(61100+i,0,1,ls);line_rows.append((ls,linepos_mi(P)))
best_ls=min(line_rows,key=lambda x:abs(x[1]-TARGET['line_mi']))[0]
rows=[]
for n_pref in [1,2,4]:
 for pb in [0.05,0.10,0.15,0.20,0.30,0.40]:
  P=gen_pref(62000+n_pref*100+int(pb*100),pb,n_pref,0)
  m2={'density141':matched_density(P,62100+n_pref,nwin=10),'local_excess':local_excess(P,62200+n_pref,nshuf=1),'boundary_gap':boundary_gap(P),'line_mi':linepos_mi(P)}
  P3=gen_pref(63000+n_pref*100+int(pb*100),pb,n_pref,best_ls)
  m3={'density141':matched_density(P3,63100+n_pref,nwin=10),'local_excess':local_excess(P3,63200+n_pref,nshuf=1),'boundary_gap':boundary_gap(P3),'line_mi':linepos_mi(P3)}
  for model,v in [('M2P',m2),('M3P',m3)]:
   scales={'density141':.10,'local_excess':.03,'boundary_gap':.05,'line_mi':.05}
   d=sum(((v[k]-TARGET[k])/scales[k])**2 for k in scales)
   rows.append({'model':model,'n_pref':n_pref,'para_bias':pb,'line_strength':best_ls if model=='M3P' else 0,'metrics':v,'distance':d})
best={m:min((x for x in rows if x['model']==m),key=lambda z:z['distance']) for m in ['M2P','M3P']}
out={'phase':'53C','status':'development/model selection','target':TARGET,'line_calibration':line_rows,'selected_line_strength':best_ls,'best':best,'rows':rows}
Path('/mnt/data/phase53c_paragraph_preference_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'target':TARGET,'line_calibration':line_rows,'best':best},indent=2))
