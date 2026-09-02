#!/usr/bin/env python3
"""Frozen Phase-F M6 exact replay / R1 scorer. --verify-only is target blind."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
from typing import Mapping, Sequence
import numpy as np

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import phase75e_score as base  # reuses the already-frozen Issue75 null/statistic machinery
import phase75f_generator_support as fgen

a_score=base.a_score
F1_PATH=HERE/'stage-f1'/'generator_authority.json'
FAMILY='M6-KRS-GATED-2MIX-CHAIN'
F1_SHA='de7976ca1c3e047c7c6f6bb50facdab797449ba81496312526917673a98661f3'
F0_SHA='999d9990449875708019ad71aa3a1d253afad19edada88cb45eb4204349887c6'
N_REPS=31


def load_f1():
    if a_score.sha256_file(F1_PATH)!=F1_SHA: raise RuntimeError('Phase F1 authority SHA changed')
    r=json.loads(F1_PATH.read_text(encoding='utf-8'))
    if r.get('schema')!='issue75-phaseF-m6-krs-gated-2mix-generator-authority-v1': raise RuntimeError('Phase F1 schema changed')
    if r.get('status')!='M6_KRS_GATED_TWO_LATENT_CHAIN_MODES_31_CORPORA_FROZEN_TARGET_BLIND': raise RuntimeError('Phase F1 status changed')
    if r.get('family')!=FAMILY or r.get('phase_f0_authority_sha256')!=F0_SHA: raise RuntimeError('Phase F1 identity changed')
    m=r.get('model_definition',{})
    if m.get('latent_states')!=2 or m.get('free_continuous_parameters')!=46 or m.get('free_gate_parameters')!=4: raise RuntimeError('Phase F1 complexity changed')
    if m.get('phase_f_refit_performed') is not False: raise RuntimeError('Phase F refit unexpectedly present')
    for k in ('explicit_nonadjacent_parameters','generic_distance_parameters','named_distant_pair_parameters','signature_specific_parameters'):
        if m.get(k)!=0: raise RuntimeError(f'forbidden flexibility changed: {k}')
    if any(r.get('target_access',{}).values()) or r.get('no_drops') is not True or r.get('no_rerolls') is not True: raise RuntimeError('Phase F1 firewall changed')
    if [int(r['fit'][str(f)]['f0_selected_start_index']) for f in range(5)]!=[3,6,4,7,6]: raise RuntimeError('frozen starts changed')
    cases={int(x['rep']):x for x in r.get('cases',[])}
    if len(cases)!=31 or set(cases)!=set(range(31)): raise RuntimeError('Phase F1 cases changed')
    return r,cases


def build_exact_case(src:Path,rep:int,authority:Mapping,cases:Mapping[int,Mapping]):
    d=fgen.build_dataset(src)
    f0=fgen.load_f0_authority()
    fits=fgen.reconstruct_fits(d,f0)
    X=fgen.generate_case(d,fits,rep)
    got=fgen.occupancy_sha(X)
    if got!=cases[rep]['occupancy_sha256']: raise RuntimeError(f'M6 exact occupancy SHA changed rep {rep}: {got}')
    padded=np.zeros_like(d['padded'],dtype=np.uint8); padded[d['line_mask']]=X
    candidate={'X':X,'token_folds':np.asarray(d['token_folds'],dtype=np.int8),'padded':padded,'line_mask':np.asarray(d['line_mask'],dtype=bool)}
    audit={'family':FAMILY,'rep':rep,'occupancy_sha256':got,'phase_f1_authority_sha256':F1_SHA,'phase_f0_authority_sha256':F0_SHA,'tokens':len(X),'fold_tokens':[int(np.sum(np.asarray(d['token_folds'])==f)) for f in range(5)],'all_zero_count':int(np.sum(X.sum(axis=1)==0)),'frozen_parameters_reconstructed':True,'phase_f_refit_performed':False,'exact_phase_f1_replay':True,'frozen_case':cases[rep]}
    return candidate,X,audit


def measurement(candidate:Mapping,X:np.ndarray,rep:int):
    rns=f'issue75:phaseF:M6-KRS-GATED-2MIX-CHAIN:rep{rep}:reference'
    tns=f'issue75:phaseF:M6-KRS-GATED-2MIX-CHAIN:rep{rep}:test'
    rq=a_score.q_views_all(candidate,X,include_folds=True); sref=a_score.build_reference(candidate,rns)
    z=a_score.normal_score_array(rq['full'],sref['full']); ztr=a_score.normal_score_array(rq['train'],sref['train']); zho=a_score.normal_score_array(rq['held'],sref['held'])
    E=a_score.residual_energy(z); fr=[a_score.finite_corr(ztr[f],zho[f]) for f in range(5)]; W=a_score.median_finite(fr)
    te=np.empty(a_score.N_TEST,dtype=np.float64)
    for n in range(a_score.N_TEST):
        Y=a_score.shuffled_flat(candidate,tns,n); q=a_score.q_views_all(candidate,Y,include_folds=False)['full']; te[n]=a_score.residual_energy(a_score.normal_score_array(q,sref['full']))
    return {'reference_namespace':rns,'test_namespace':tns,'n_reference':a_score.N_REF,'n_test':a_score.N_TEST,'residual_energy':E,'p_exist':float((1+int(np.sum(te>=E)))/(a_score.N_TEST+1)),'reliability':{'fold_correlations':fr,'median':W},'z_full':[float(v) for v in z],'test_energy_summary':{'min':float(np.min(te)),'median':float(np.median(te)),'q95':float(np.quantile(te,.95)),'max':float(np.max(te))}}


def main(argv:Sequence[str]):
    if len(argv) not in (4,5): raise SystemExit(f'usage: {argv[0]} ZL3B_PATH REP OUTPUT_JSON [--verify-only]')
    src=Path(argv[1]).resolve(); rep=int(argv[2]); out=Path(argv[3]).resolve(); verify=len(argv)==5 and argv[4]=='--verify-only'
    if rep not in range(N_REPS): raise SystemExit('REP must be 0..30')
    if len(argv)==5 and not verify: raise SystemExit('only optional flag is --verify-only')
    authority,cases=load_f1(); candidate,X,audit=build_exact_case(src,rep,authority,cases)
    common={'family':FAMILY,'rep':rep,'candidate_audit':audit,'pair_count':66,'target_readings_averaged':False,'no_case_selection':True,'no_reroll':True}
    if verify:
        result={'schema':'issue75-phaseF-m6-r1-preflight-v1','status':'EXACT_F1_M6_CORPUS_REGENERATED_TARGET_BLIND','scientific_role':'PRETARGET_EXACT_M6_REPLAY_PREFLIGHT',**common,'target_access':{'pair_Q_computed':False,'residual_Z_computed':False,'Issue58C_target_vector_loaded':False,'Issue58D_target_vector_loaded':False,'target_correlation_computed':False,'T_computed':False}}
    else:
        m=measurement(candidate,X,rep); z=np.asarray(m['z_full'],dtype=np.float64); targets,ta=a_score.t68.load_target_references(); top={}
        for name in ('ZL3b','IT2a'):
            target=np.asarray(targets[name],dtype=np.float64); corr=a_score.finite_corr(z,target)
            if corr is None or not math.isfinite(corr): raise RuntimeError(f'non-finite topology correlation {name}')
            top[name]={'pearson':float(corr),'sign_agreement':a_score.sign_agreement(z,target),'sign_denominator':66}
        T=float(min(top['ZL3b']['pearson'],top['IT2a']['pearson']))
        result={'schema':'issue75-phaseF-m6-r1-score-v1','status':'PHASE_F_M6_FIRST_REVEAL_CASE_SCORED','scientific_role':'KRS_GATED_TWO_LATENT_LOCAL_CHAIN_COMPLETE_66_EDGE_MEASUREMENT',**common,'measurement':m,'target_authority':ta,'topology':top,'T':T,'target_access':{'pair_Q_computed':True,'residual_Z_computed':True,'Issue58C_target_vector_loaded':True,'Issue58D_target_vector_loaded':True,'target_correlation_computed':True,'T_computed':True}}
    raw=a_score.canonical_json_bytes(result)+b'\n'; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(raw)
    print(json.dumps({'status':result['status'],'rep':rep,'verify_only':verify,'occupancy_sha256':audit['occupancy_sha256'],'E':None if verify else result['measurement']['residual_energy'],'p_exist':None if verify else result['measurement']['p_exist'],'W':None if verify else result['measurement']['reliability']['median'],'R_ZL3b':None if verify else result['topology']['ZL3b']['pearson'],'R_IT2a':None if verify else result['topology']['IT2a']['pearson'],'T':None if verify else result['T'],'output_sha256':a_score.sha256_bytes(raw)},ensure_ascii=False,sort_keys=True,indent=2)); return 0

if __name__=='__main__': raise SystemExit(main(sys.argv))
