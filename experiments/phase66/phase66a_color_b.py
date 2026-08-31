#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

SEED=6602
KS=range(2,7)

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def prepare(p):
    im=cv2.imread(str(p),cv2.IMREAD_COLOR)
    if im is None: raise RuntimeError(f'cannot read {p}')
    lab=cv2.cvtColor(im,cv2.COLOR_BGR2LAB).astype(np.float64)
    H,W=lab.shape[:2]; y,x=np.indices((H,W)); area=H*W
    border=(x<W*.12)|(x>=W*.88)|(y<H*.12)|(y>=H*.88)
    L,a,b=lab[:,:,0],lab[:,:,1],lab[:,:,2]
    chroma=np.sqrt((a-128)**2+(b-128)**2)
    cand=border&(L>=155)&(chroma<=35)
    fallback=False
    if int(cand.sum())<500:
        cand=border&(L>=145); fallback=True
    if int(cand.sum())<500: raise RuntimeError(f'BACKGROUND_FAIL {p.name}')
    bg=np.median(lab[cand],axis=0)
    norm=lab.copy(); shift=np.array([230-bg[0],128-bg[1],128-bg[2]])
    norm+=shift; norm=np.clip(norm,0,255)
    L,a,b=norm[:,:,0],norm[:,:,1],norm[:,:,2]
    chroma=np.sqrt((a-128)**2+(b-128)**2)
    delta=np.sqrt((L-230)**2+(a-128)**2+(b-128)**2)
    raw=(L>=45)&(chroma>=12)&(delta>=18)
    n,labels,stats,_=cv2.connectedComponentsWithStats(raw.astype(np.uint8),8)
    keep=np.zeros(raw.shape,bool)
    for i in range(1,n):
        z=int(stats[i,cv2.CC_STAT_AREA])
        if not (z<20 and z/area<.0008): keep|=(labels==i)
    pts=np.c_[a[keep]-128,b[keep]-128]
    return {'file':p.name,'sha256':sha256(p),'width':W,'height':H,'area':area,
            'background_lab':bg.tolist(),'background_fallback':fallback,'lab_shift':shift.tolist(),
            'mask':keep,'points':pts}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('crop_dir'); ap.add_argument('output'); args=ap.parse_args()
    files=sorted(Path(args.crop_dir).glob('*.png'))
    if len(files)!=24: raise SystemExit(f'expected 24 pngs, got {len(files)}')
    prepared=[prepare(p) for p in files]; pooled=np.vstack([r['points'] for r in prepared])
    rng=np.random.default_rng(SEED); ids=rng.choice(len(pooled),min(20000,len(pooled)),replace=False); sample=pooled[ids]
    scores={}
    for k in KS:
        km=KMeans(n_clusters=k,random_state=SEED,n_init=20).fit(sample)
        scores[str(k)]=float(silhouette_score(sample,km.labels_))
    best=max(scores.values()); chosen=min(int(k) for k,v in scores.items() if v>=best-.01)
    km=KMeans(n_clusters=chosen,random_state=SEED,n_init=20).fit(pooled)
    order=sorted(range(chosen),key=lambda i:(km.cluster_centers_[i,0],km.cluster_centers_[i,1]))
    centers={f'C{j+1}':[float(x) for x in km.cluster_centers_[old]] for j,old in enumerate(order)}
    records=[]; offset=0
    for r in prepared:
        n=len(r['points']); labels=km.labels_[offset:offset+n]; offset+=n; H,W=r['height'],r['width']; yy,xx=np.indices((H,W)); coords=np.argwhere(r['mask'])
        colors={}
        for j,old in enumerate(order):
            cname=f'C{j+1}'; sel=(labels==old); count=int(sel.sum()); frac=count/r['area']; present=count>=25 and frac>=.002
            rec={'pixels':count,'area_fraction':frac,'colored_fraction':count/n if n else 0.0,'present':present}
            if present:
                ys=coords[sel,0]; xs=coords[sel,1]
                rec['x_centroid_norm']=float(xs.mean()/(W-1)) if W>1 else 0.0; rec['y_centroid_norm']=float(ys.mean()/(H-1)) if H>1 else 0.0
                rec['third_fractions']=[float((ys<H/3).mean()),float(((ys>=H/3)&(ys<2*H/3)).mean()),float((ys>=2*H/3).mean())]
            else: rec.update(x_centroid_norm=None,y_centroid_norm=None,third_fractions=None)
            colors[cname]=rec
        records.append({'file':r['file'],'sha256':r['sha256'],'background_lab':r['background_lab'],'background_fallback':r['background_fallback'],'lab_shift':r['lab_shift'],'total_colored_fraction':n/r['area'],'clusters':colors})
    out={'schema':'phase66a-color-b-v1','seed':SEED,'opencv':cv2.__version__,'candidate_k':[2,3,4,5,6],'silhouette_scores':scores,'chosen_k':chosen,'cluster_centers_ab':centers,'pooled_colored_pixels':len(pooled),'records':records}
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
