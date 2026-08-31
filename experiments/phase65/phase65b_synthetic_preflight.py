#!/usr/bin/env python3
"""Phase65B2 synthetic-only implementation preflight.

No P25 image, P25 label, SOURCE_MANIFEST_B label payload, or CROP_MANIFEST_B crop
is read. The purpose is to freeze and test the exact scientific primitives before
any f102v2 association reveal.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, re, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.stats import rankdata


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()


def parse_eva_label(raw: str, view: str='W1') -> list[str]:
    if view not in {'W1','W2'}: raise ValueError(view)
    if '?' in raw or '[' in raw or ']' in raw: raise ValueError('uncertain label is ineligible')
    s=raw.replace('<->','|').replace('<~>','|')
    s=re.sub(r'<[^>]*>','',s).replace('{','').replace('}','')
    atoms={}
    def protect(m):
        k=f'\uE000{len(atoms)}\uE001'; atoms[k]=m.group(0); return k
    s=re.sub(r'@[0-9]+;', protect, s)
    if view=='W1': s=s.replace('.', '|').replace(',', '|')
    else: s=s.replace('.', '|').replace(',', '')
    s=re.sub(r'\s+','|',s)
    out=[]; i=0; keys=sorted(atoms,key=len,reverse=True)
    while i<len(s):
        if s[i]=='|':
            if out and out[-1] != '|': out.append('|')
            i+=1; continue
        matched=False
        for k in keys:
            if s.startswith(k,i): out.append(atoms[k]); i+=len(k); matched=True; break
        if matched: continue
        c=s[i]
        if c.isascii() and c.isalpha(): out.append(c.lower()); i+=1; continue
        raise ValueError(f'unexpected EVA character: {c!r}')
    while out and out[-1]=='|': out.pop()
    return out


def levenshtein(a:list[str], b:list[str])->int:
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        cur=[i]
        for j,y in enumerate(b,1): cur.append(min(cur[-1]+1, prev[j]+1, prev[j-1]+(x!=y)))
        prev=cur
    return prev[-1]


def normalized_levenshtein(a:list[str], b:list[str])->float:
    if not a or not b: raise ValueError('nonempty sequences required')
    return levenshtein(a,b)/max(len(a),len(b))


def spearman(x,y)->float:
    x=np.asarray(x,float); y=np.asarray(y,float)
    if len(x)!=len(y) or len(x)<2: raise ValueError('bad vectors')
    rx=rankdata(x,method='average'); ry=rankdata(y,method='average')
    if np.all(rx==rx[0]) or np.all(ry==ry[0]): return float('nan')
    return float(np.corrcoef(rx,ry)[0,1])


def pairs(n): return [(i,j) for i in range(n) for j in range(i+1,n)]

def row_rho(v,t):
    ij=pairs(len(v)); return spearman([v[i][j] for i,j in ij],[t[i][j] for i,j in ij])
def weighted_T(rows):
    vals=[(len(pairs(len(v))),row_rho(v,t)) for v,t in rows]
    return sum(w*r for w,r in vals)/sum(w for w,_ in vals)
def permute_matrix(m,p): return [[m[p[i]][p[j]] for j in range(len(p))] for i in range(len(p))]
def exact_null(rows):
    perms=[list(itertools.permutations(range(len(v)))) for v,_ in rows]
    obs=weighted_T(rows); stats=[]
    for joint in itertools.product(*perms):
        stats.append(weighted_T([(v,permute_matrix(t,p)) for (v,t),p in zip(rows,joint)]))
    return obs,sum(x>=obs-1e-15 for x in stats)/len(stats),stats


def synthetic_image(i:int)->Image.Image:
    im=Image.new('RGB',(173+17*i,121+11*i),'white'); d=ImageDraw.Draw(im)
    d.ellipse((15+i*3,10,90+i*5,90),fill=(20+20*i,90+10*i,40+5*i)); d.line((10,110,150,20+i*4),fill=(0,0,0),width=4+i)
    return im

def preprocess(im,torch):
    im=im.convert('RGB'); side=max(im.size); sq=Image.new('RGB',(side,side),(255,255,255)); sq.paste(im,((side-im.width)//2,(side-im.height)//2)); sq=sq.resize((518,518),resample=Image.Resampling.BICUBIC)
    arr=np.asarray(sq,dtype=np.float32)/255.0; x=torch.from_numpy(arr).permute(2,0,1); mean=torch.tensor([0.485,0.456,0.406])[:,None,None]; std=torch.tensor([0.229,0.224,0.225])[:,None,None]
    return ((x-mean)/std).unsqueeze(0)
def dino_smoke(repo,weights):
    sys.path.insert(0,str(repo)); import torch
    from dinov2.models.vision_transformer import vit_small
    model=vit_small(patch_size=14,img_size=518,init_values=1.0,block_chunks=0); model.load_state_dict(torch.load(weights,map_location='cpu',weights_only=True),strict=True); model.eval(); vecs=[]
    with torch.inference_mode():
        for i in range(2):
            z=model.forward_features(preprocess(synthetic_image(i),torch))['x_norm_clstoken'][0]; z=z/torch.linalg.vector_norm(z); vecs.append(z.cpu().numpy())
    return {'dimension':int(vecs[0].shape[0]),'norms':[float(np.linalg.norm(v)) for v in vecs],'cosine_distance':float(1-np.dot(vecs[0],vecs[1]))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dinov2-repo',required=True); ap.add_argument('--weights',required=True); ap.add_argument('--expected-weight-sha256',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    actual=sha256_file(Path(a.weights));
    if actual!=a.expected_weight_sha256: raise RuntimeError('DINO weight hash mismatch')
    pt={'w1':parse_eva_label('Ch{e}dy,ok.<->@123;','W1'),'w2':parse_eva_label('Ch{e}dy,ok.<->@123;','W2')}
    assert pt['w1']==['c','h','e','d','y','|','o','k','|','@123;']; assert pt['w2']==['c','h','e','d','y','o','k','|','@123;']; assert normalized_levenshtein(list('abc'),list('adc'))==1/3
    v1=[[0,.1,.8],[.1,0,.7],[.8,.7,0]]; t1=[[0,.2,.9],[.2,0,.6],[.9,.6,0]]; v2=[[0,.3],[.3,0]]; t2=[[0,.4],[.4,0]]; obs,p,stats=exact_null([(v1,t1),(v2,t2)]); assert len(stats)==12
    dino=dino_smoke(Path(a.dinov2_repo),Path(a.weights)); assert dino['dimension']==384
    out={'schema':'phase65b-synthetic-preflight-v1','mode':'SYNTHETIC_ONLY','p25_inputs_read':False,'parser_tests':pt,'normalized_levenshtein_abc_adc':1/3,'synthetic_exact_null':{'assignments':len(stats),'T_observed':obs,'p_exact':p,'min':min(stats),'max':max(stats)},'dino':dino,'weights_sha256':actual,'versions':{'python':sys.version,'numpy':np.__version__,'pillow':__import__('PIL').__version__,'scipy':__import__('scipy').__version__}}
    Path(a.out).write_text(json.dumps(out,indent=2)+'\n'); print('SYNTHETIC PREFLIGHT PASS; P25 inputs read=false')
if __name__=='__main__': main()
