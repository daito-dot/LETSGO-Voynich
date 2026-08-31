#!/usr/bin/env python3
from __future__ import annotations

import math
import sys

import numpy as np
from numba import njit

import phaseE11d_dev2_diagnostic as d

A=24
M=23
STEPS=100_000
T1=.00005
EPS=1e-12


@njit(cache=False)
def swap_delta24(key,i,j,pats,counts,offsets,incident,lm_cost,marks,stamp,total_count):
    stamp += 1
    old_i=key[i]; old_j=key[j]
    delta_total=0.0
    if i < M:
        for z in range(offsets[i],offsets[i+1]):
            pidx=incident[z]
            if marks[pidx] == stamp: continue
            marks[pidx]=stamp
            p0=pats[pidx,0]; p1=pats[pidx,1]; p2=pats[pidx,2]; p3=pats[pidx,3]
            o0=key[p0]; o1=key[p1]; o2=key[p2]; o3=key[p3]
            n0=old_j if p0==i else (old_i if p0==j else o0)
            n1=old_j if p1==i else (old_i if p1==j else o1)
            n2=old_j if p2==i else (old_i if p2==j else o2)
            n3=old_j if p3==i else (old_i if p3==j else o3)
            oldq=(((o0*24+o1)*24+o2)*24+o3)
            newq=(((n0*24+n1)*24+n2)*24+n3)
            delta_total += counts[pidx]*(lm_cost[newq]-lm_cost[oldq])
    if j < M:
        for z in range(offsets[j],offsets[j+1]):
            pidx=incident[z]
            if marks[pidx] == stamp: continue
            marks[pidx]=stamp
            p0=pats[pidx,0]; p1=pats[pidx,1]; p2=pats[pidx,2]; p3=pats[pidx,3]
            o0=key[p0]; o1=key[p1]; o2=key[p2]; o3=key[p3]
            n0=old_j if p0==i else (old_i if p0==j else o0)
            n1=old_j if p1==i else (old_i if p1==j else o1)
            n2=old_j if p2==i else (old_i if p2==j else o2)
            n3=old_j if p3==i else (old_i if p3==j else o3)
            oldq=(((o0*24+o1)*24+o2)*24+o3)
            newq=(((n0*24+n1)*24+n2)*24+n3)
            delta_total += counts[pidx]*(lm_cost[newq]-lm_cost[oldq])
    return delta_total/total_count,stamp


@njit(cache=False)
def anneal24(initial_key,seed,t0,pats,counts,offsets,incident,lm_cost):
    key=initial_key.copy()
    total_count=0
    for x in counts: total_count += x
    marks=np.zeros(pats.shape[0],dtype=np.int32); stamp=0
    np.random.seed(seed)
    current=d.direct_score24(key,pats,counts,lm_cost)
    T=t0
    ratio=math.exp(math.log(T1/t0)/(STEPS-1))
    for _ in range(STEPS):
        i=np.random.randint(0,A)
        j=np.random.randint(0,A-1)
        if j>=i: j+=1
        delta,stamp=swap_delta24(key,i,j,pats,counts,offsets,incident,lm_cost,marks,stamp,total_count)
        if delta<=0.0 or np.random.random()<math.exp(-delta/T):
            tmp=key[i]; key[i]=key[j]; key[j]=tmp
            current += delta
        T *= ratio
    while True:
        best_d=-EPS; best_i=-1; best_j=-1
        for i in range(A-1):
            for j in range(i+1,A):
                delta,stamp=swap_delta24(key,i,j,pats,counts,offsets,incident,lm_cost,marks,stamp,total_count)
                if delta < best_d:
                    best_d=delta; best_i=i; best_j=j
        if best_i<0: break
        tmp=key[best_i]; key[best_i]=key[best_j]; key[best_j]=tmp
        current += best_d
    return key,d.direct_score24(key,pats,counts,lm_cost)


def faithful_anneal_from(seed_key,t0,pats,counts,offsets,incident,lm_cost):
    seed=d.base.seed32(f"Issue26E11D:Dev2Anneal:v1:{t0:.3f}")
    key,reported=anneal24(seed_key,seed,float(t0),pats,counts,offsets,incident,lm_cost)
    return key,float(reported),seed


d.anneal_from=faithful_anneal_from

if __name__=="__main__":
    raise SystemExit(d.main())
