#!/usr/bin/env python3
from __future__ import annotations
import argparse, itertools, json, math, hashlib
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.stats import rankdata

MORPH_FIELDS=["leaf_composition","leaf_arrangement","leaf_margin"]
BINARY_CLUSTERS=["C1","C2"]
CONT_CLUSTERS=["C1","C2","C3"]


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def spearman(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    rx=rankdata(x,method='average'); ry=rankdata(y,method='average')
    if len(x)<2 or np.all(rx==rx[0]) or np.all(ry==ry[0]): return float('nan')
    return float(np.corrcoef(rx,ry)[0,1])


def unordered_pairs(n): return [(i,j) for i in range(n) for j in range(i+1,n)]


def row_rho(a,b):
    ij=unordered_pairs(len(a))
    return spearman([a[i][j] for i,j in ij],[b[i][j] for i,j in ij])


def permute_matrix(m,p): return [[m[p[i]][p[j]] for j in range(len(p))] for i in range(len(p))]


def _row_fast_context(row):
    n=len(row['ids']); ij=unordered_pairs(n)
    xv=np.asarray([row['image'][i][j] for i,j in ij],float)
    yv=np.asarray([row['text'][i][j] for i,j in ij],float)
    xr=rankdata(xv,method='average'); yr=rankdata(yv,method='average')
    if np.all(xr==xr[0]) or np.all(yr==yr[0]): return None
    xc=xr-xr.mean(); yc=yr-yr.mean()
    xn=float(np.linalg.norm(xc)); yn=float(np.linalg.norm(yc))
    yrm=np.zeros((n,n),float)
    for (i,j),r in zip(ij,yr): yrm[i,j]=yrm[j,i]=r
    return {'row':row['row'],'ids':row['ids'],'ij':ij,'xc':xc,'xn':xn,'yn':yn,'yrm':yrm,'rho_obs':float(np.dot(xc,yc)/(xn*yn)),'weight':len(ij)}


def _rho_perm(ctx,p):
    yp=np.asarray([ctx['yrm'][p[i],p[j]] for i,j in ctx['ij']],float)
    yp-=yp.mean()
    return float(np.dot(ctx['xc'],yp)/(ctx['xn']*ctx['yn']))


def exact_page_stat(rows,min_usable=2):
    ctxs=[c for c in (_row_fast_context(r) for r in rows) if c is not None]
    if len(ctxs)<min_usable:
        return {'status':'BLOCKED','reason':'fewer than two usable physical rows','usable_rows':len(ctxs)}
    denom=sum(c['weight'] for c in ctxs)
    observed=sum(c['weight']*c['rho_obs'] for c in ctxs)/denom
    perms=[list(itertools.permutations(range(len(c['ids'])))) for c in ctxs]
    n_perm=math.prod(len(p) for p in perms)
    ge=0; vals=np.empty(n_perm,float); z=0
    for joint in itertools.product(*perms):
        total=sum(c['weight']*_rho_perm(c,p) for c,p in zip(ctxs,joint))
        t=total/denom; vals[z]=t; z+=1
        if t>=observed-1e-15: ge+=1
    qs=np.quantile(vals,[0,.01,.025,.05,.5,.95,.975,.99,1]).tolist()
    p=ge/n_perm
    return {
      'status':'OK','T_observed':observed,'p_exact_one_sided':p,'n_permutations':n_perm,
      'page_pass':bool(observed>=0.20 and p<=0.05),
      'row_rho':{c['row']:c['rho_obs'] for c in ctxs},
      'row_pair_counts':{c['row']:c['weight'] for c in ctxs},
      'permutation_quantiles':dict(zip(['min','q01','q025','q05','median','q95','q975','q99','max'],qs))
    }


def load_morph(path):
    d=json.load(open(path)); fields=d['field_order']; ix={f:i for i,f in enumerate(fields)}
    out={}
    for rec in d['records']:
        oid=rec[0]; out[oid]={f:rec[1+ix[f]] for f in MORPH_FIELDS}
    return out


def load_color(path):
    d=json.load(open(path)); out={}
    for r in d['records']:
        oid=r['object_id']
        out[oid]={
            'C1':{'present':bool(r['C1_present']),'area_fraction':float(r['C1_area_fraction'])},
            'C2':{'present':bool(r['C2_present']),'area_fraction':float(r['C2_area_fraction'])},
            'C3':{'present':False,'area_fraction':float(r['C3_area_fraction'])}
        }
    if len(out)!=24: raise RuntimeError(f'expected 24 color records, got {len(out)}')
    return out,d


def load_labels(path):
    d=json.load(open(path)); out={}
    for u in d['p25_locus_freeze']['units']:
        if u['confidence_flags']['phase63b_65b_confidence_eligible']:
            out[u['object_id']]={'page':u['page'],'raw':u['transcription_raw'],'locus':u['zl3b_locus']}
    if len(out)!=24: raise RuntimeError(f'expected 24 labels, got {len(out)}')
    return out,d


def glyphs(raw): return [c for c in raw if c!='.']


def bigrams(raw):
    s=set()
    for word in raw.split('.'):
        for i in range(len(word)-1): s.add(word[i:i+2])
    return s


def jaccard(a,b):
    a=set(a); b=set(b); u=a|b
    return 0.0 if not u else 1-len(a&b)/len(u)


def verify_text_freeze(labels,freeze):
    raws=[v['raw'] for v in labels.values()]
    alphabet=set(''.join(''.join(glyphs(r)) for r in raws))
    prev_u={c:sum(c in set(glyphs(r)) for r in raws) for c in alphabet}
    got_u=sorted([c for c,n in prev_u.items() if 4<=n<=20])
    all_b=set().union(*(bigrams(r) for r in raws))
    prev_b={bg:sum(bg in bigrams(r) for r in raws) for bg in all_b}
    got_b=sorted([bg for bg,n in prev_b.items() if 3<=n<=12])
    lengths=[len(glyphs(r)) for r in raws]
    if got_u!=freeze['retained_unigrams'] or got_b!=freeze['retained_bigrams']:
        raise RuntimeError(f'text freeze mismatch unigrams={got_u} bigrams={got_b}')
    if [min(lengths),max(lengths)]!=[freeze['length_range']['min'],freeze['length_range']['max']]:
        raise RuntimeError('length range mismatch')
    return {'retained_unigrams':got_u,'retained_bigrams':got_b,'length_range':[min(lengths),max(lengths)]}


def text_feature(raw,freeze):
    gs=glyphs(raw)
    return {'length':len(gs),'first':gs[0],'last':gs[-1],
            'unigrams':set(gs)&set(freeze['retained_unigrams']),
            'bigrams':bigrams(raw)&set(freeze['retained_bigrams'])}


def text_distance(a,b,freeze):
    span=freeze['length_range']['max']-freeze['length_range']['min']
    ds=[abs(a['length']-b['length'])/span,
        0.0 if a['first']==b['first'] else 1.0,
        0.0 if a['last']==b['last'] else 1.0,
        jaccard(a['unigrams'],b['unigrams']),jaccard(a['bigrams'],b['bigrams'])]
    return float(np.mean(ds))


def image_scalers(color):
    out={}
    for c in CONT_CLUSTERS:
        vals=[x[c]['area_fraction'] for x in color.values()]
        out[c]=(min(vals),max(vals))
    return out


def image_distance(oa,ob,morph,color,scalers):
    md=[]
    for f in MORPH_FIELDS:
        a=morph[oa][f]; b=morph[ob][f]
        if a!='U' and b!='U': md.append(0.0 if a==b else 1.0)
    I1=float(np.mean(md)) if md else None
    I2=float(np.mean([0.0 if color[oa][c]['present']==color[ob][c]['present'] else 1.0 for c in BINARY_CLUSTERS]))
    cds=[]
    for c in CONT_CLUSTERS:
        lo,hi=scalers[c]; den=hi-lo
        xa=0.0 if den==0 else (color[oa][c]['area_fraction']-lo)/den
        xb=0.0 if den==0 else (color[ob][c]['area_fraction']-lo)/den
        cds.append(abs(xa-xb))
    I3=float(np.mean(cds))
    return float(np.mean([x for x in [I1,I2,I3] if x is not None])),{'I1':I1,'I2':I2,'I3':I3}


def row_name(oid): return oid.split('.')[0]


def page_ids(labels,page):
    xs=[oid for oid,v in labels.items() if v['page']==page]
    def key(oid):
        r,n=oid.split('.'); order={'T':0,'M':1,'B':2,'L2':0,'L3':1}
        return (order[r],int(n))
    return sorted(xs,key=key)


def build_real_rows(page,morph,color,labels,freeze):
    ids=page_ids(labels,page); scalers=image_scalers(color)
    tf={oid:text_feature(labels[oid]['raw'],freeze) for oid in labels}
    groups=defaultdict(list)
    for oid in ids: groups[row_name(oid)].append(oid)
    rows=[]; diag={}
    for row,rids in groups.items():
        n=len(rids); im=[[0.0]*n for _ in range(n)]; tx=[[0.0]*n for _ in range(n)]; comp={}
        for i in range(n):
            for j in range(i+1,n):
                d,c=image_distance(rids[i],rids[j],morph,color,scalers); im[i][j]=im[j][i]=d
                comp[f'{rids[i]}|{rids[j]}']=c
                td=text_distance(tf[rids[i]],tf[rids[j]],freeze); tx[i][j]=tx[j][i]=td
        rows.append({'row':row,'ids':rids,'image':im,'text':tx})
        diag[row]={'ids':rids,'image_distance':im,'text_distance':tx,'image_components':comp}
    return rows,diag


def synthetic_rows(sizes,aligned=True):
    rows=[]
    for ri,n in enumerate(sizes):
        z=np.arange(n,dtype=float); im=np.abs(z[:,None]-z[None,:]).tolist()
        if aligned: t=np.abs(z[:,None]-z[None,:]).tolist()
        else:
            q=np.array([(i*3+1)%n for i in range(n)],dtype=float)
            t=np.abs(q[:,None]-q[None,:]).tolist()
        rows.append({'row':f'R{ri+1}','ids':[f'R{ri+1}.{i+1}' for i in range(n)],'image':im,'text':t})
    return rows


def run_synthetic():
    a=exact_page_stat(synthetic_rows([6,5],True)); b=exact_page_stat(synthetic_rows([4,5,4],True))
    indep=exact_page_stat(synthetic_rows([6,5],False))
    morph={'A':{f:'U' for f in MORPH_FIELDS},'B':{f:'U' for f in MORPH_FIELDS}}
    color={'A':{c:{'present':False,'area_fraction':0.0} for c in CONT_CLUSTERS},
           'B':{c:{'present':True if c=='C1' else False,'area_fraction':0.5 if c=='C1' else 0.0} for c in CONT_CLUSTERS}}
    d,parts=image_distance('A','B',morph,color,image_scalers(color))
    test=synthetic_rows([4,3],True)[0]; ctx=_row_fast_context(test); p=(2,0,3,1)
    direct=row_rho(test['image'],permute_matrix(test['text'],p)); fast=_rho_perm(ctx,p)
    checks={
      'primary_perm_count':a.get('n_permutations')==86400,
      'replication_perm_count':b.get('n_permutations')==69120,
      'aligned_primary_positive_low_p':a.get('T_observed',-9)>0 and a.get('p_exact_one_sided',1)<=0.05,
      'aligned_replication_positive_low_p':b.get('T_observed',-9)>0 and b.get('p_exact_one_sided',1)<=0.05,
      'independent_not_forced_positive_pass':not indep.get('page_pass',False),
      'u_morphology_not_imputed':parts['I1'] is None and math.isfinite(d),
      'optimized_equals_direct_spearman':abs(direct-fast)<1e-12,
    }
    return {'schema':'phase66b-synthetic-preflight-v1','checks':checks,'all_pass':all(checks.values()),
            'aligned_primary':a,'aligned_replication':b,'independence_control':indep,
            'u_handling':{'distance':d,'parts':parts}}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=['synthetic','science'],required=True); ap.add_argument('--out',required=True)
    ap.add_argument('--page',choices=['f102v2','f100v']); ap.add_argument('--role',choices=['primary','replication'])
    ap.add_argument('--morphology'); ap.add_argument('--color-features'); ap.add_argument('--source-manifest'); ap.add_argument('--text-freeze')
    args=ap.parse_args()
    if args.mode=='synthetic':
        out=run_synthetic(); Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'all_pass':out['all_pass'],'checks':out['checks']})); return 0 if out['all_pass'] else 2
    req=[args.page,args.role,args.morphology,args.color_features,args.source_manifest,args.text_freeze]
    if any(x is None for x in req): raise SystemExit('science mode missing args')
    if (args.page,args.role) not in [('f102v2','primary'),('f100v','replication')]: raise SystemExit('chronology guard')
    morph=load_morph(args.morphology); color,colorraw=load_color(args.color_features)
    labels,_=load_labels(args.source_manifest); freeze=json.load(open(args.text_freeze))
    tv=verify_text_freeze(labels,freeze); rows,diag=build_real_rows(args.page,morph,color,labels,freeze)
    stat=exact_page_stat(rows)
    out={'schema':'phase66b-science-result-v1','page':args.page,'role':args.role,'statistic':stat,
         'text_freeze_verification':tv,
         'input_sha256':{'morphology':sha256_file(args.morphology),'color_features':sha256_file(args.color_features),
                         'source_manifest':sha256_file(args.source_manifest),'text_freeze':sha256_file(args.text_freeze)},
         'color_summary':{'chosen_k':colorraw['chosen_k']},'rows':diag}
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'page':args.page,'role':args.role,'T':stat.get('T_observed'),
                      'p':stat.get('p_exact_one_sided'),'pass':stat.get('page_pass'),'n':stat.get('n_permutations')}))
    return 0

if __name__=='__main__': raise SystemExit(main())
