#!/usr/bin/env python3
"""Issue #72 complete counterfactual-family aggregation.

Consumes exactly the frozen per-realization first-reveal files and applies one
maxT family over all scored realizations and both target readings.
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import sys
from pathlib import Path

import numpy as np

BASELINE_MIN_R = 0.8830282501011794
N_TEST = 1000
P_GATE = 0.01
W_GATE = 0.50
R_GATE = 0.70
SIGN_GATE = 50
STRONG_REL = 0.90
COLLAPSE_REL = 0.70
TARGETS = ("ZL3b", "IT2a")


def sha256_file(p: Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def emp_upper(obs, null):
    a=np.asarray(null)
    return float((1+np.sum(a>=obs))/(len(a)+1))


def load_freeze(root: Path):
    p=root/"family-preflight"/"preflight.json"
    r=json.loads(p.read_text(encoding="utf-8"))
    ids=[x.strip() for x in (root/"family-preflight"/"TARGET_AUTHORIZED_REALIZATIONS.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    axes=[x.strip() for x in (root/"family-preflight"/"TARGET_AUTHORIZED_AXES.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    if ids!=r["target_authorized_realizations"] or axes!=r["target_authorized_axes"]: raise RuntimeError("family freeze text files differ from JSON")
    return r,axes,ids,sha256_file(p)


def aggregate(input_dir: Path, project_root: Path, outfile: Path):
    freeze,axes,ids,freeze_sha=load_freeze(project_root/"experiments"/"naibbe-r1-decomposition")
    files=sorted(input_dir.glob("score-*.json"))
    rows={}
    input_hashes={}
    for p in files:
        r=json.loads(p.read_text(encoding="utf-8")); rid=r["realization"]
        if rid in rows: raise RuntimeError(f"duplicate realization result {rid}")
        rows[rid]=r; input_hashes[rid]=sha256_file(p)
    if set(rows)!=set(ids): raise RuntimeError(f"realization artifact set mismatch: got={sorted(rows)} expected={sorted(ids)}")
    if not ids: raise RuntimeError("no target-authorized realization exists")

    heads={r["first_reveal_head"] for r in rows.values()}
    if len(heads)!=1: raise RuntimeError(f"realization results came from multiple heads: {heads}")
    for rid,r in rows.items():
        if r["family_preflight_sha256"]!=freeze_sha: raise RuntimeError(f"{rid} family-preflight SHA mismatch")
        if len(r["pairs"])!=66: raise RuntimeError(f"{rid} pair count mismatch")
        if len(r["test_null"]["energy"])!=N_TEST: raise RuntimeError(f"{rid} test-null energy length mismatch")
        for t in TARGETS:
            if len(r["test_null"]["correlation_by_target"][t])!=N_TEST or len(r["test_null"]["sign_by_target"][t])!=N_TEST: raise RuntimeError(f"{rid}/{t} null length mismatch")

    M_E=np.max(np.stack([np.asarray(rows[rid]["test_null"]["energy"],float) for rid in ids]),axis=0)
    corr_arrays=[]; sign_arrays=[]
    for rid in ids:
        for t in TARGETS:
            corr_arrays.append(np.asarray(rows[rid]["test_null"]["correlation_by_target"][t],float))
            sign_arrays.append(np.asarray(rows[rid]["test_null"]["sign_by_target"][t],float))
    M_R=np.max(np.stack(corr_arrays),axis=0)
    M_A=np.max(np.stack(sign_arrays),axis=0)

    per_real={}
    for rid in ids:
        r=rows[rid]; E=float(r["real"]["residual_energy"]); W=r["real"]["within_reliability"]
        pE=emp_upper(E,M_E)
        exist=bool(W["valid_folds"]>=4 and W["median"] is not None and float(W["median"])>=W_GATE and pE<=P_GATE)
        topo={}; minR=1.0; all_topo=True
        for t in TARGETS:
            obs=r["real"]["topology"][t]; rr=obs["pearson"]; aa=int(obs["sign_agreement"])
            rv=-1.0 if rr is None else float(rr); minR=min(minR,rv)
            pR=emp_upper(rv,M_R); pA=emp_upper(aa,M_A)
            passed=bool(rv>=R_GATE and pR<=P_GATE and aa>=SIGN_GATE and pA<=P_GATE)
            all_topo &= passed
            topo[t]={"pearson":None if rr is None else rv,"sign_agreement":aa,"sign_denominator":66,"p_R_maxT_complete_counterfactual_family_x_readings":pR,"p_sign_maxT_complete_counterfactual_family_x_readings":pA,"pass":passed}
        rel=float(minR/BASELINE_MIN_R)
        full=bool(exist and all_topo)
        per_real[rid]={"axis":r["axis"],"surface_sha256":r["surface_identity"]["surface_sha256"],"E":E,"W":W,"p_exist_maxT_complete_counterfactual_family":pE,"existence_pass":exist,"topology":topo,"min_target_pearson":minR,"relative_to_published_min_topology":rel,"full_R1_pass":full,"strong_retained_realization":bool(full and rel>=STRONG_REL)}

    by_axis={a:[] for a in axes}
    for rid in ids: by_axis[per_real[rid]["axis"]].append(rid)
    axis_results={}
    for axis in axes:
        rr=by_axis[axis]; n=len(rr); q=math.ceil(2*n/3)
        full_count=sum(per_real[x]["full_R1_pass"] for x in rr)
        strong_count=sum(per_real[x]["strong_retained_realization"] for x in rr)
        median_rel=float(statistics.median(per_real[x]["relative_to_published_min_topology"] for x in rr))
        if strong_count>=q and median_rel>=STRONG_REL:
            cls="R1_RETAINED"
        elif full_count==0 and median_rel<COLLAPSE_REL:
            cls="R1_COLLAPSED"
        else:
            cls="R1_MODULATED"
        axis_results[axis]={"realizations":rr,"N":n,"two_thirds_ceiling_Q":q,"full_R1_pass_count":full_count,"strong_count":strong_count,"median_relative_topology":median_rel,"classification":cls}

    required=bool("I" in axis_results and "P" in axis_results and any(a in axis_results for a in "LSTG"))
    if not required:
        global_cls="R1 DECOMPOSITION INCONCLUSIVE"
    else:
        I=axis_results["I"]["classification"]; P=axis_results["P"]["classification"]
        codebook=[axis_results[a]["classification"] for a in "LSTG" if a in axis_results]
        any_cb_collapse=any(x=="R1_COLLAPSED" for x in codebook)
        if I=="R1_RETAINED":
            global_cls="R1 IS PREDOMINANTLY CODEBOOK/INVENTORY-EMBEDDED"
        elif I=="R1_COLLAPSED" and P=="R1_RETAINED" and any_cb_collapse:
            global_cls="R1 DEPENDS MATERIALLY ON CODEBOOK ASSOCIATION/STATE STRUCTURE"
        elif I=="R1_COLLAPSED" and not any_cb_collapse:
            global_cls="R1 DEPENDS MATERIALLY ON ENCRYPTION/PLAINTEXT PROCESS"
        elif I=="R1_COLLAPSED" and P=="R1_COLLAPSED" and any_cb_collapse:
            global_cls="R1 ORIGIN IS MIXED"
        else:
            global_cls="R1 ORIGIN IS MIXED"

    result={
        "phase":"Issue72-R1-codebook-process-decomposition-first-reveal",
        "first_reveal_head":next(iter(heads)),
        "family_preflight_sha256":freeze_sha,
        "target_authorized_axes":axes,
        "target_authorized_realizations":ids,
        "published_Naibbe_reference":{"ZL3b_pearson":0.8830282501011794,"IT2a_pearson":0.9000974100381157,"min_target_pearson_B":BASELINE_MIN_R,"R1":"PASS","R2":"FAIL","R3":"FAIL","R4":"FAIL","overall":"NOT COMPETITIVE"},
        "maxT_family":{"realization_count":len(ids),"target_readings":list(TARGETS),"n_test":N_TEST,"energy_max_values":M_E.tolist(),"correlation_max_values_over_realizations_x_readings":M_R.tolist(),"sign_max_values_over_realizations_x_readings":[int(x) for x in M_A],"energy_summary":{"min":float(np.min(M_E)),"median":float(np.median(M_E)),"q95":float(np.quantile(M_E,.95)),"max":float(np.max(M_E))},"correlation_summary":{"min":float(np.min(M_R)),"median":float(np.median(M_R)),"q95":float(np.quantile(M_R,.95)),"max":float(np.max(M_R))},"sign_summary":{"min":int(np.min(M_A)),"median":float(np.median(M_A)),"q95":float(np.quantile(M_A,.95)),"max":int(np.max(M_A))}},
        "per_realization":per_real,
        "axis_results":axis_results,
        "global_requirements_available":required,
        "frozen_global_classification":global_cls,
        "input_realization_json_sha256":input_hashes,
        "interpretation_boundary":{"Naibbe_repaired":False,"R2_rescored":False,"R3_rescored":False,"R4_rescored":False,"plaintext_recovered":False,"historical_identity_established":False,"decipherment_established":False},
    }
    outfile.parent.mkdir(parents=True,exist_ok=True); outfile.write_text(json.dumps(result,sort_keys=True,separators=(",",":")),encoding="utf-8")
    print(json.dumps({"global":global_cls,"axes":{a:v["classification"] for a,v in axis_results.items()},"outfile":str(outfile),"sha256":sha256_file(outfile)},sort_keys=True))


def self_test():
    null=np.asarray([0.1,0.2,0.3]); assert emp_upper(.25,null)==0.5
    assert math.ceil(2*5/3)==4 and math.ceil(2*2/3)==2
    print(json.dumps({"Issue72_aggregate_self_test":"ok","real_counterfactual_scored":False},sort_keys=True))

if __name__=="__main__":
    if len(sys.argv)==2 and sys.argv[1]=="--self-test": self_test()
    elif len(sys.argv)==4: aggregate(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve(),Path(sys.argv[3]).resolve())
    else: raise SystemExit(f"usage: {sys.argv[0]} --self-test | INPUT_DIR PROJECT_ROOT OUTFILE")
