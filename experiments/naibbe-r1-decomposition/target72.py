#!/usr/bin/env python3
"""Issue #72 per-realization R1 scorer.

One invocation scores exactly one frozen, family-preflight-authorized
counterfactual realization. Final familywise p-values are assigned only by the
separate aggregate72.py over the complete frozen family.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in (
    "phase62",
    "phase64",
    "issue26-music",
    "naibbe-r1-decomposition",
    "occupancy-graph-stability",
    "occupancy-graph-residual",
    "occupancy-graph-independent-transcription",
    "joint-constraint-tournament",
):
    p=EXPERIMENTS/rel
    if str(p) not in sys.path: sys.path.insert(0,str(p))

import phase62b_n0 as b  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402
import family_preflight72 as fp  # noqa: E402
import phase58b_graph_stability as b58  # noqa: E402
import phase58c_residual_graph as c58  # noqa: E402
import target68 as t68  # noqa: E402

PARENT_MAIN="ce49de68a3bd308b9432f5904b5368fc4c6f9c8f"
EXPECTED_CREMMA="292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_ENCODER_BLOB="b566ad82e4b6ff0782ecdddebf77718dac44f292"
EXPECTED_TABLE_BLOB="5cd34fb81d80faf3b4d57dbf1719c05ffde25302"
N_REF=1000
N_TEST=1000
N_FOLDS=4
N_EDGES=66
PAIRS=b58.PAIRS
MANUSCRIPTS=tuple(n64.MANUSCRIPTS)


def sha256_file(p: Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def array_sha(a: np.ndarray)->str:
    x=np.ascontiguousarray(np.asarray(a,dtype="<f8"))
    return hashlib.sha256(x.tobytes()).hexdigest()


def load_family_freeze():
    root=HERE.parent/"family-preflight"
    p=root/"preflight.json"
    if not p.exists(): raise RuntimeError("family preflight archive missing")
    r=json.loads(p.read_text(encoding="utf-8"))
    if r["counterfactual_R1_scored"] is not False or any(r["forbidden_quantities_computed"].values()):
        raise RuntimeError("family preflight target firewall not clean")
    axes=[x.strip() for x in (root/"TARGET_AUTHORIZED_AXES.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    ids=[x.strip() for x in (root/"TARGET_AUTHORIZED_REALIZATIONS.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    if axes!=r["target_authorized_axes"] or ids!=r["target_authorized_realizations"]:
        raise RuntimeError("family authorization files differ from preflight JSON")
    return r,axes,ids,sha256_file(p)


def load_sources(cremma_root: Path):
    if b.verify_cremma_commit(cremma_root)!=EXPECTED_CREMMA: raise RuntimeError("CREMMA authority mismatch")
    return {name:b.parse_latin_manuscript(cremma_root,name,rel) for name,rel in b.PRIMARY_MANUSCRIPTS.items()}


def generate_one(rid: str, cremma_root: Path, naibbe_root: Path, freeze: dict):
    recs={x["realization"]:x for x in freeze["realizations"]}
    if rid not in recs: raise RuntimeError(f"realization {rid} absent from family preflight")
    expected=recs[rid]
    axis=expected["axis"]
    if axis not in freeze["target_authorized_axes"] or rid not in freeze["target_authorized_realizations"]:
        raise RuntimeError(f"realization {rid} is not target-authorized")

    module=n64.load_naibbe(naibbe_root)
    if fp.s.git_blob((naibbe_root/"naibbe_v2.py").read_bytes())!=EXPECTED_ENCODER_BLOB: raise RuntimeError("encoder blob mismatch")
    if fp.s.git_blob((naibbe_root/"references"/"naibbe_tables.csv").read_bytes())!=EXPECTED_TABLE_BLOB: raise RuntimeError("table blob mismatch")
    sources=load_sources(cremma_root)
    original_map=dict(module.placeholder_to_glyph)
    parser=e.SlotParser()
    published_by_m,_=fp.published_surfaces(module,sources,original_map)
    if fp.surface_sha(fp.pooled(published_by_m))!=fp.s.EXPECTED_POOLED_SHA: raise RuntimeError("published primary authority changed")

    if axis=="P":
        r=int(rid[1:]); record,by_m=fp.generate_P(module,sources,original_map,parser,r)
    elif axis=="L":
        r=int(rid[1:]); mp,inv=fp.map_L(module,original_map,r); record,by_m=fp.generate_with_map(module,sources,mp,parser,"L",rid,inv)
    elif axis=="S":
        shift=int(rid[1:]); mp,inv=fp.map_S(module,original_map,shift); record,by_m=fp.generate_with_map(module,sources,mp,parser,"S",rid,inv)
    elif axis=="T":
        shift=int(rid[1:]); mp,inv=fp.map_T(module,original_map,shift); record,by_m=fp.generate_with_map(module,sources,mp,parser,"T",rid,inv)
    elif axis=="G":
        r=int(rid[1:]); mp,inv=fp.map_G(module,original_map,r); record,by_m=fp.generate_with_map(module,sources,mp,parser,"G",rid,inv)
    elif axis=="I":
        r=int(rid[1:]); by_m,inv=fp.permute_inventory(published_by_m,r); pp=fp.pooled(by_m)
        record={"axis":"I","realization":rid,"surface_sha256":fp.surface_sha(pp),"support":fp.parser_support(pp,parser),"generation_completed":True,"ambiguity_retries_by_manuscript":None,"primary_cipher_tokens_by_manuscript":None,"map_sha256":None,"invariants":inv}
    else:
        raise RuntimeError(f"unsupported axis {axis}")

    if record["surface_sha256"]!=expected["surface_sha256"]: raise RuntimeError(f"{rid} surface SHA differs from frozen preflight")
    if record["support"]!=expected["support"]: raise RuntimeError(f"{rid} support differs from frozen preflight")
    if record["support"]["coverage"]<0.60: raise RuntimeError(f"{rid} unexpectedly below frozen support gate")
    return axis,record,by_m


def build_dataset(by_m: dict):
    parser=e.SlotParser(); lines=[]; visible=parsed=0; per_m=[]
    for fold,m in enumerate(MANUSCRIPTS):
        mv=mp=0
        for item in by_m[m]:
            for li,toks in enumerate(item.lines):
                n_visible=len(toks); visible+=n_visible; mv+=n_visible; rows=[]
                for tok_units in toks:
                    tok="".join(tok_units); picked=parser.pick(tok,"min")
                    if picked is None: continue
                    vals=picked[1]
                    rows.append(np.fromiter((bool(vals[s]) for s in range(12)),dtype=np.uint8,count=12))
                    parsed+=1; mp+=1
                if rows:
                    lines.append({"fold":fold,"manuscript":m,"item_id":item.item_id,"line_index":li,"occ":np.stack(rows)})
        per_m.append({"fold":fold,"manuscript":m,"visible_tokens":mv,"parsed_tokens":mp})
    X=np.concatenate([x["occ"] for x in lines],axis=0)
    token_folds=np.concatenate([np.full(len(x["occ"]),x["fold"],np.int8) for x in lines])
    maxlen=max(len(x["occ"]) for x in lines)
    padded=np.zeros((len(lines),maxlen,12),dtype=np.uint8); mask=np.zeros((len(lines),maxlen),dtype=bool)
    for i,row in enumerate(lines):
        z=row["occ"]; padded[i,:len(z)]=z; mask[i,:len(z)]=True
    if not np.array_equal(padded[mask],X): raise RuntimeError("padded/flat ordering mismatch")
    return {"X":X,"token_folds":token_folds,"padded":padded,"line_mask":mask,"visible":visible,"parsed":parsed,"coverage":parsed/visible,"line_count":len(lines),"per_manuscript":per_m,"fold_counts":[int(np.sum(token_folds==f)) for f in range(4)]}


def q_views(d,X,folds: bool):
    code=b58.pair_codes(X); cf=b58.partition_counts(code,d["token_folds"],N_FOLDS,True); total=cf.sum(axis=0)
    out={"full":b58.q_cond(total)}
    if folds:
        out["held"]=np.stack([b58.q_cond(cf[f]) for f in range(N_FOLDS)])
        out["train"]=np.stack([b58.q_cond(total-cf[f]) for f in range(N_FOLDS)])
    return out


def build_reference(d,base_ns: str):
    ref={"full":np.empty((N_REF,N_EDGES)),"train":np.empty((N_REF,N_FOLDS,N_EDGES)),"held":np.empty((N_REF,N_FOLDS,N_EDGES))}
    for n in range(N_REF):
        Y=c58.shuffled_flat(d,base_ns,n); q=q_views(d,Y,True)
        for k in ref: ref[k][n]=q[k]
        if (n+1)%100==0: print(f"reference {n+1}/{N_REF}",file=sys.stderr,flush=True)
    return {k:np.sort(v,axis=0) for k,v in ref.items()}


def residualize(q,sref,folds: bool):
    out={"full":c58.normal_score_array(q["full"],sref["full"])}
    if folds:
        out["train"]=c58.normal_score_array(q["train"],sref["train"])
        out["held"]=c58.normal_score_array(q["held"],sref["held"])
    return out


def reliability(z):
    vals=[b58.corr(z["train"][f],z["held"][f]) for f in range(N_FOLDS)]
    valid=[float(x) for x in vals if x is not None and math.isfinite(float(x))]
    return {"fold_correlations":vals,"valid_folds":len(valid),"median":None if len(valid)<4 else float(np.median(valid))}


def score(rid: str, cremma_root: Path, naibbe_root: Path, outfile: Path):
    freeze,axes,ids,freeze_sha=load_family_freeze()
    axis,identity,by_m=generate_one(rid,cremma_root,naibbe_root,freeze)
    d=build_dataset(by_m)
    exp=next(x for x in freeze["realizations"] if x["realization"]==rid)
    if (d["visible"],d["parsed"])!=(exp["support"]["visible_tokens"],exp["support"]["accepted_tokens"]): raise RuntimeError("dataset support counts differ after adapter")

    targets,target_authority=t68.load_target_references()
    real_q=q_views(d,d["X"],True)
    ref_ns=f"issue72:{axis}:{rid}:reference-null"; test_ns=f"issue72:{axis}:{rid}:test-null"
    sref=build_reference(d,ref_ns); real_z=residualize(real_q,sref,True)
    E=c58.residual_energy(real_z["full"]); W=reliability(real_z)
    obs={}
    for name,target in targets.items():
        rr=b58.corr(real_z["full"],target)
        obs[name]={"pearson":None if rr is None else float(rr),"sign_agreement":int(t68.sign_agreement(real_z["full"],target)),"sign_denominator":N_EDGES}

    energy=np.empty(N_TEST); corr={k:np.empty(N_TEST) for k in targets}; signs={k:np.empty(N_TEST,dtype=np.int16) for k in targets}
    for n in range(N_TEST):
        Y=c58.shuffled_flat(d,test_ns,n); q=q_views(d,Y,False); z=c58.normal_score_array(q["full"],sref["full"])
        energy[n]=c58.residual_energy(z)
        for name,target in targets.items():
            rr=b58.corr(z,target); corr[name][n]=-1.0 if rr is None else float(rr); signs[name][n]=t68.sign_agreement(z,target)
        if (n+1)%100==0: print(f"test {n+1}/{N_TEST}",file=sys.stderr,flush=True)

    result={
        "phase":"Issue72-counterfactual-R1-realization",
        "first_reveal_head":os.environ.get("TARGET_HEAD_SHA") or os.environ.get("GITHUB_SHA"),
        "family_preflight_sha256":freeze_sha,
        "axis":axis,"realization":rid,"surface_identity":identity,
        "population":{"visible_tokens":d["visible"],"parsed_tokens":d["parsed"],"coverage":d["coverage"],"line_count":d["line_count"],"fold_parsed_tokens":d["fold_counts"],"per_manuscript":d["per_manuscript"]},
        "null":{"reference_namespace":ref_ns,"test_namespace":test_ns,"n_reference":N_REF,"n_test":N_TEST,"reference_sorted_array_sha256":{k:array_sha(v) for k,v in sref.items()},"reference_shapes":{k:list(v.shape) for k,v in sref.items()}},
        "pairs":[list(map(int,p)) for p in PAIRS],
        "real":{"q_full":real_q["full"].tolist(),"z_full":real_z["full"].tolist(),"residual_energy":E,"within_reliability":W,"topology":obs},
        "test_null":{"energy":energy.tolist(),"correlation_by_target":{k:v.tolist() for k,v in corr.items()},"sign_by_target":{k:[int(x) for x in v] for k,v in signs.items()}},
        "target_authority":target_authority,
        "final_familywise_p_values_assigned":False,
    }
    outfile.parent.mkdir(parents=True,exist_ok=True)
    outfile.write_text(json.dumps(result,sort_keys=True,separators=(",",":")),encoding="utf-8")
    print(json.dumps({"scored":rid,"axis":axis,"outfile":str(outfile),"sha256":sha256_file(outfile),"E":E,"W":W["median"]},sort_keys=True))


def self_test():
    X=np.zeros((16,12),dtype=np.uint8)
    for i in range(16): X[i,i%12]=1; X[i,(i+3)%12]=1
    d={"X":X,"token_folds":np.asarray([i%4 for i in range(16)],dtype=np.int8)}
    q=q_views(d,X,True)
    assert q["full"].shape==(66,) and q["train"].shape==(4,66) and q["held"].shape==(4,66)
    assert N_REF==1000 and N_TEST==1000 and len(PAIRS)==66
    print(json.dumps({"Issue72_target_self_test":"ok","real_counterfactual_scored":False,"n_edges":66},sort_keys=True))

if __name__=="__main__":
    if len(sys.argv)==2 and sys.argv[1]=="--self-test": self_test()
    elif len(sys.argv)==6 and sys.argv[1]=="score": score(sys.argv[2],Path(sys.argv[3]).resolve(),Path(sys.argv[4]).resolve(),Path(sys.argv[5]).resolve())
    else: raise SystemExit(f"usage: {sys.argv[0]} --self-test | score RID CREMMA_ROOT NAIBBE_ROOT OUTFILE")
