#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.stats import rankdata

def sha256_file(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def parse_eva_label(raw,view='W1'):
 if view not in {'W1','W2'}:raise ValueError(view)
 if any(c in raw for c in '?[]'):raise ValueError('uncertain')
 s=raw.replace('<->','|').replace('<~>','|');s=re.sub(r'<[^>]*>','',s).replace('{','').replace('}','');atoms={}
 def prot(m):
  k=f'\uE000{len(atoms)}\uE001';atoms[k]=m.group(0);return k
 s=re.sub(r'@[0-9]+;',prot,s).replace('.','|').replace(',','|' if view=='W1' else '');s=re.sub(r'\s+','|',s);out=[];i=0;keys=sorted(atoms,key=len,reverse=True)
 while i<len(s):
  if s[i]=='|':
   if out and out[-1]!='|':out.append('|')
   i+=1;continue
  hit=False
  for k in keys:
   if s.startswith(k,i):out.append(atoms[k]);i+=len(k);hit=True;break
  if hit:continue
  c=s[i]
  if c.isascii() and c.isalpha():out.append(c.lower());i+=1
  else:raise ValueError(c)
 while out and out[-1]=='|':out.pop()
 return out
def lev(a,b):
 p=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  q=[i]
  for j,y in enumerate(b,1):q.append(min(q[-1]+1,p[j]+1,p[j-1]+(x!=y)))
  p=q
 return p[-1]
def nlev(a,b):return lev(a,b)/max(len(a),len(b))
def rho(x,y):
 x=rankdata(x);y=rankdata(y)
 if len(x)<2:raise ValueError('undefined')
 return float(np.corrcoef(x,y)[0,1])
def pairs(n):return [(i,j) for i in range(n) for j in range(i+1,n)]
def rr(v,t):
 ij=pairs(len(v));return rho([v[i][j] for i,j in ij],[t[i][j] for i,j in ij])
def T(rows):
 z=[(len(pairs(len(v))),rr(v,t)) for v,t in rows];return sum(w*r for w,r in z)/sum(w for w,_ in z)
def pm(m,p):return [[m[p[i]][p[j]] for j in range(len(p))] for i in range(len(p))]
def exact(rows):
 ps=[list(itertools.permutations(range(len(v)))) for v,_ in rows];o=T(rows);z=[]
 for joint in itertools.product(*ps):z.append(T([(v,pm(t,p)) for (v,t),p in zip(rows,joint)]))
 return o,sum(x>=o-1e-15 for x in z)/len(z),z
def simimg(i):
 im=Image.new('RGB',(173+17*i,121+11*i),'white');d=ImageDraw.Draw(im);d.ellipse((15+i*3,10,90+i*5,90),fill=(20+20*i,90+10*i,40+5*i));d.line((10,110,150,20+i*4),fill='black',width=4+i);return im
def prep(im,torch):
 side=max(im.size);sq=Image.new('RGB',(side,side),'white');sq.paste(im,((side-im.width)//2,(side-im.height)//2));sq=sq.resize((518,518),Image.Resampling.BICUBIC);x=torch.from_numpy(np.asarray(sq,dtype=np.float32)/255).permute(2,0,1);return ((x-torch.tensor([.485,.456,.406])[:,None,None])/torch.tensor([.229,.224,.225])[:,None,None]).unsqueeze(0)
def dino(repo,w):
 sys.path.insert(0,str(repo));import torch
 from dinov2.models.vision_transformer import vit_small
 m=vit_small(patch_size=14,img_size=518,init_values=1.0,block_chunks=0);m.load_state_dict(torch.load(w,map_location='cpu',weights_only=True),strict=True);m.eval();vs=[]
 with torch.inference_mode():
  for i in range(2):
   z=m.forward_features(prep(simimg(i),torch))['x_norm_clstoken'][0];z/=torch.linalg.vector_norm(z);vs.append(z.cpu().numpy())
 return {'dimension':len(vs[0]),'norms':[float(np.linalg.norm(v)) for v in vs],'cosine_distance':float(1-np.dot(vs[0],vs[1]))}
def main():
 a=argparse.ArgumentParser();a.add_argument('--dinov2-repo',required=True);a.add_argument('--weights',required=True);a.add_argument('--expected-weight-sha256',required=True);a.add_argument('--out',required=True);a=a.parse_args();h=sha256_file(a.weights)
 if h!=a.expected_weight_sha256:raise RuntimeError('weight hash')
 pt={'w1':parse_eva_label('Ch{e}dy,ok.<->@123;','W1'),'w2':parse_eva_label('Ch{e}dy,ok.<->@123;','W2')};assert pt['w1']==['c','h','e','d','y','|','o','k','|','@123;'];assert pt['w2']==['c','h','e','d','y','o','k','|','@123;'];assert nlev(list('abc'),list('adc'))==1/3
 v1=[[0,.1,.8],[.1,0,.7],[.8,.7,0]];t1=[[0,.2,.9],[.2,0,.6],[.9,.6,0]];v2=[[0,.15,.65],[.15,0,.9],[.65,.9,0]];t2=[[0,.25,.55],[.25,0,.95],[.55,.95,0]];o,p,z=exact([(v1,t1),(v2,t2)]);assert len(z)==36
 di=dino(Path(a.dinov2_repo),Path(a.weights));assert di['dimension']==384
 r={'schema':'phase65b-synthetic-preflight-v1','mode':'SYNTHETIC_ONLY','p25_inputs_read':False,'parser_tests':pt,'normalized_levenshtein_abc_adc':1/3,'synthetic_exact_null':{'assignments':len(z),'T_observed':o,'p_exact':p,'min':min(z),'max':max(z)},'dino':di,'weights_sha256':h,'versions':{'python':sys.version,'numpy':np.__version__,'pillow':__import__('PIL').__version__,'scipy':__import__('scipy').__version__}}
 Path(a.out).write_text(json.dumps(r,indent=2)+'\n');print('SYNTHETIC PREFLIGHT PASS; P25 inputs read=false')
if __name__=='__main__':main()
