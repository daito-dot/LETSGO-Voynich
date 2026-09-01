#!/usr/bin/env python3
"""Phase-F target-blind M6 candidate-owned-null smoke."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
from typing import Sequence
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import phase75f_score as score

def forbidden(*_a,**_k): raise RuntimeError('TARGET FIREWALL: loader called during Phase-F candidate smoke')

def main(argv:Sequence[str]):
    if len(argv)!=4: raise SystemExit(f'usage: {argv[0]} ZL3B_PATH REP OUTPUT_JSON')
    src=Path(argv[1]).resolve(); rep=int(argv[2]); out=Path(argv[3]).resolve()
    if rep not in range(score.N_REPS): raise SystemExit('REP must be 0..30')
    score.a_score.t68.load_target_references=forbidden
    authority,cases=score.load_f1(); candidate,X,audit=score.build_exact_case(src,rep,authority,cases); m=score.measurement(candidate,X,rep)
    if not math.isfinite(float(m['residual_energy'])) or not 0<float(m['p_exist'])<=1: raise RuntimeError('invalid candidate-null diagnostic')
    if len(m['z_full'])!=66 or m['n_reference']!=1000 or m['n_test']!=1000: raise RuntimeError('candidate-owned null contract changed')
    result={'schema':'issue75-phaseF-m6-candidate-null-smoke-v1','status':'M6_CANDIDATE_OWNED_NULL_EXECUTION_VERIFIED_TARGET_BLIND','scientific_role':'PRETARGET_IMPLEMENTATION_SMOKE_ONLY','family':score.FAMILY,'rep':rep,'candidate_audit':audit,'measurement':m,'target_firewall':'load_target_references monkeypatched to hard fail','target_access':{'pair_Q_computed':True,'residual_Z_computed':True,'candidate_reference_null_computed':True,'candidate_test_null_computed':True,'Issue58C_target_vector_loaded':False,'Issue58D_target_vector_loaded':False,'target_correlation_computed':False,'target_sign_agreement_computed':False,'T_computed':False}}
    raw=score.a_score.canonical_json_bytes(result)+b'\n'; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(raw)
    print(json.dumps({'status':result['status'],'rep':rep,'occupancy_sha256':audit['occupancy_sha256'],'E':m['residual_energy'],'p_exist':m['p_exist'],'W':m['reliability']['median'],'target_loaded':False,'output_sha256':score.a_score.sha256_bytes(raw)},ensure_ascii=False,sort_keys=True,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main(sys.argv))
