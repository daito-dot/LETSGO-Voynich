#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
import cv2
import numpy as np

CLASSES = ["brown","red","yellow_ochre","green","blue","other_chromatic"]

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def classify(h,s,v):
    chrom=(s>=50)&(v>=35)
    out=np.full(h.shape,-1,np.int8)
    brown=chrom&(h>=5)&(h<=25)&(v<=180); out[brown]=0
    red=chrom&(((h<=10)|(h>=170)))&(s>=65)&(v>80)&(out<0); out[red]=1
    yellow=chrom&(h>=11)&(h<=34)&(out<0); out[yellow]=2
    green=chrom&(h>=35)&(h<=95)&(out<0); out[green]=3
    blue=chrom&(h>=96)&(h<=135)&(out<0); out[blue]=4
    out[chrom&(out<0)]=5
    return out

def clean(mask, area):
    n, lab, stats, _=cv2.connectedComponentsWithStats(mask.astype(np.uint8),8)
    keep=np.zeros(mask.shape,bool)
    for i in range(1,n):
        a=int(stats[i,cv2.CC_STAT_AREA])
        if not (a<25 and a/area<0.001): keep|=(lab==i)
    return keep

def measure(path):
    bgr=cv2.imread(str(path),cv2.IMREAD_COLOR)
    if bgr is None: raise RuntimeError(f"cannot read {path}")
    hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
    h,s,v=[hsv[:,:,i] for i in range(3)]
    cls=classify(h,s,v); H,W=h.shape; area=H*W
    result={"file":path.name,"sha256":sha256(path),"width":W,"height":H,"area":area,"colors":{}}
    yy,xx=np.indices((H,W))
    for idx,name in enumerate(CLASSES):
        m=clean(cls==idx,area); count=int(m.sum()); frac=count/area
        present=(count>=25 and frac>=0.002)
        rec={"pixels":count,"area_fraction":frac,"present":present}
        if present:
            rec["x_centroid_norm"]=float(xx[m].mean()/(W-1)) if W>1 else 0.0
            rec["y_centroid_norm"]=float(yy[m].mean()/(H-1)) if H>1 else 0.0
            thirds=[yy < H/3,(yy>=H/3)&(yy<2*H/3),yy>=2*H/3]
            rec["third_fractions"]=[float((m&t).sum()/count) for t in thirds]
        else:
            rec["x_centroid_norm"]=None; rec["y_centroid_norm"]=None; rec["third_fractions"]=None
        result["colors"][name]=rec
    result["low_chroma_bright_fraction"]=float(((s<50)&(v>=160)).sum()/area)
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("crop_dir"); ap.add_argument("output")
    a=ap.parse_args(); root=Path(a.crop_dir)
    files=sorted(root.glob("*.png"))
    if len(files)!=24: raise SystemExit(f"expected 24 pngs, got {len(files)}")
    out={"schema":"phase66a-color-measure-v1","opencv":cv2.__version__,"n":len(files),"records":[measure(p) for p in files]}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
if __name__=="__main__": main()
