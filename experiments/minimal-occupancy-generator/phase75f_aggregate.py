#!/usr/bin/env python3
"""Aggregate frozen Issue #75 Phase-F M6 first-reveal population."""
from __future__ import annotations
import glob,json,math,statistics,sys
from pathlib import Path
from typing import Mapping,Sequence
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import phase75e_aggregate as ea

PHASE_A=HERE/'stage-a-first-reveal'/'phase75a_aggregate.json'
PHASE_D=HERE/'stage-d-first-reveal'/'phase75d_aggregate.json'
PHASE_E=HERE/'stage-e-first-reveal'/'phase75e_aggregate.json'
F1=HERE/'stage-f1'/'generator_authority.json'
SHA_A='fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540'
SHA_D='c15ffb92030220596cacef9db9cb3bdb26c92607f675c24ff0fa607e16764489'
SHA_E='983aa0370d949690d7e117fbf2f1273f3a157975d51a06a5e149f4ea1861c0c5'
SHA_F1='de7976ca1c3e047c7c6f6bb50facdab797449ba81496312526917673a98661f3'
F0_SHA='999d9990449875708019ad71aa3a1d253afad19edada88cb45eb4204349887c6'
FAMILY='M6-KRS-GATED-2MIX-CHAIN'; N=31; DELTA=0.009768313008182594
SUFF='M6_KRS_GATED_TWO_LATENT_CHAIN_MODES_SUFFICIENT'
INSUFF='M6_KRS_GATED_TWO_LATENT_CHAIN_MODES_INSUFFICIENT_GLOBAL_THREE_MODE_FALLBACK_LICENSED'


def load_controls():
    for p,s,n in ((PHASE_A,SHA_A,'A'),(PHASE_D,SHA_D,'D'),(PHASE_E,SHA_E,'E'),(F1,SHA_F1,'F1')):
        if ea.sha256_file(p)!=s: raise RuntimeError(f'Phase {n} authority SHA changed')
    a=json.loads(PHASE_A.read_text()); d=json.loads(PHASE_D.read_text()); e=json.loads(PHASE_E.read_text()); f1=json.loads(F1.read_text())
    if a.get('schema')!='issue75-phaseA-aggregate-v1' or a.get('positive_control',{}).get('valid') is not True: raise RuntimeError('Phase A control changed')
    if float(a['primary_q95_equivalence']['delta_plus'])!=DELTA: raise RuntimeError('Phase A tolerance changed')
    if d.get('primary',{}).get('classification')!='M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED': raise RuntimeError('Phase D control changed')
    if e.get('primary',{}).get('classification')!='M5_KRS_TWO_LATENT_CHAIN_MODES_INSUFFICIENT_RICHER_LATENT_OR_CONFIGURATION_RULE_REQUIRED': raise RuntimeError('Phase E control changed')
    if f1.get('status')!='M6_KRS_GATED_TWO_LATENT_CHAIN_MODES_31_CORPORA_FROZEN_TARGET_BLIND' or f1.get('phase_f0_authority_sha256')!=F0_SHA or any(f1.get('target_access',{}).values()): raise RuntimeError('Phase F1 authority changed')
    plus=[float(x) for x in a['paired_values']['T_plus_center']]; d4=[float(x) for x in d['primary']['D_M4_minus_phaseA_plus_center']]; d5=[float(x) for x in e['primary']['D_M5_minus_phaseA_plus_center']]
    if len(plus)!=N or len(d4)!=N or len(d5)!=N: raise RuntimeError('paired control population changed')
    t4=[plus[i]+d4[i] for i in range(N)]; t5=[plus[i]+d5[i] for i in range(N)]
    if abs(statistics.median(t4)-float(d['measurement']['T']['median']))>1e-12 or abs(statistics.median(t5)-float(e['measurement']['T']['median']))>1e-12: raise RuntimeError('paired T reconstruction changed')
    if d['target_authority']!=e['target_authority']: raise RuntimeError('target authority changed between D/E')
    return a,d,e,f1,plus,t4,t5


def validate_case(r:Mapping,rep:int,target_authority:Mapping):
    if r.get('schema')!='issue75-phaseF-m6-r1-score-v1' or r.get('status')!='PHASE_F_M6_FIRST_REVEAL_CASE_SCORED': raise RuntimeError(f'bad Phase F score contract rep {rep}')
    if r.get('family')!=FAMILY or int(r.get('rep',-1))!=rep or r.get('pair_count')!=66 or r.get('target_readings_averaged') is not False: raise RuntimeError(f'bad identity/topology rep {rep}')
    if r.get('no_case_selection') is not True or r.get('no_reroll') is not True: raise RuntimeError(f'selection guardrail rep {rep}')
    ca=r.get('candidate_audit',{})
    if ca.get('phase_f1_authority_sha256')!=SHA_F1 or ca.get('phase_f0_authority_sha256')!=F0_SHA or ca.get('exact_phase_f1_replay') is not True or ca.get('frozen_parameters_reconstructed') is not True or ca.get('phase_f_refit_performed') is not False: raise RuntimeError(f'F1 replay failed rep {rep}')
    if ca.get('tokens')!=25071 or ca.get('fold_tokens')!=[4430,4810,5516,5447,4868] or ca.get('all_zero_count')!=0: raise RuntimeError(f'population changed rep {rep}')
    m=r.get('measurement',{})
    if m.get('reference_namespace')!=f'issue75:phaseF:M6-KRS-GATED-2MIX-CHAIN:rep{rep}:reference' or m.get('test_namespace')!=f'issue75:phaseF:M6-KRS-GATED-2MIX-CHAIN:rep{rep}:test': raise RuntimeError(f'null namespace changed rep {rep}')
    if m.get('n_reference')!=1000 or m.get('n_test')!=1000 or len(m.get('z_full',[]))!=66: raise RuntimeError(f'null contract changed rep {rep}')
    if not math.isfinite(float(m.get('residual_energy'))) or not 0<float(m.get('p_exist'))<=1: raise RuntimeError(f'residual diagnostic invalid rep {rep}')
    for name in ('ZL3b','IT2a'):
        t=r.get('topology',{}).get(name,{})
        if not math.isfinite(float(t.get('pearson'))) or t.get('sign_denominator')!=66 or not 0<=int(t.get('sign_agreement'))<=66: raise RuntimeError(f'topology invalid rep {rep} {name}')
    T=float(r.get('T')); expected=min(float(r['topology']['ZL3b']['pearson']),float(r['topology']['IT2a']['pearson']))
    if abs(T-expected)>1e-15: raise RuntimeError(f'T mismatch rep {rep}')
    if r.get('target_authority')!=target_authority: raise RuntimeError(f'target authority changed rep {rep}')
    if any(v is not True for v in r.get('target_access',{}).values()): raise RuntimeError(f'target access record incomplete rep {rep}')


def main(argv:Sequence[str]):
    if len(argv)!=4: raise SystemExit(f'usage: {argv[0]} INPUT_DIR OUTPUT_JSON SCIENTIFIC_HEAD')
    inp=Path(argv[1]).resolve(); out=Path(argv[2]).resolve(); head=argv[3].strip()
    a,d,e,f1,plus,t4,t5=load_controls(); ta=e['target_authority']
    paths=sorted(glob.glob(str(inp/'*.json')))
    if len(paths)!=N: raise RuntimeError(f'need exactly 31 Phase F score JSON files, found {len(paths)}')
    rows={}
    for p in paths:
        r=json.loads(Path(p).read_text()); rep=int(r.get('rep',-1))
        if rep not in range(N) or rep in rows: raise RuntimeError(f'unexpected/duplicate Phase F rep {rep}')
        validate_case(r,rep,ta); rows[rep]=r
    if set(rows)!=set(range(N)): raise RuntimeError('complete Phase F population mismatch')
    T=[float(rows[i]['T']) for i in range(N)]; d6=[T[i]-plus[i] for i in range(N)]; gap=float(statistics.median(d6)); sufficient=bool(gap>=-DELTA)
    vs5=[T[i]-t5[i] for i in range(N)]; vs4=[T[i]-t4[i] for i in range(N)]
    q90=float(a['nonpromoting_tolerance_sensitivity']['q90']['delta_plus']); q99=float(a['nonpromoting_tolerance_sensitivity']['q99']['delta_plus'])
    gates=[f1['fit'][str(f)]['gate_intercept_and_K_R_S_slopes'] for f in range(5)]; starts=[int(f1['fit'][str(f)]['f0_selected_start_index']) for f in range(5)]
    result={'schema':'issue75-phaseF-m6-aggregate-v1','status':'PHASE_F_M6_COMPLETE_31_CASE_POPULATION_AGGREGATED','scientific_head':head,'phase_f1_authority_sha256':SHA_F1,'phase_f0_authority_sha256':F0_SHA,'phase_a_positive_control_aggregate_sha256':SHA_A,'phase_d_m4_aggregate_sha256':SHA_D,'phase_e_m5_aggregate_sha256':SHA_E,'population':{'family':FAMILY,'n_reps':N,'total_results':N,'complete_population':True,'no_drops':True,'no_rerolls':True},'target_authority':ta,'measurement':{'T':ea.summary(T),'R_ZL3b':ea.summary([rows[i]['topology']['ZL3b']['pearson'] for i in range(N)]),'R_IT2a':ea.summary([rows[i]['topology']['IT2a']['pearson'] for i in range(N)]),'sign_ZL3b':ea.summary([rows[i]['topology']['ZL3b']['sign_agreement'] for i in range(N)]),'sign_IT2a':ea.summary([rows[i]['topology']['IT2a']['sign_agreement'] for i in range(N)]),'residual_energy':ea.summary([rows[i]['measurement']['residual_energy'] for i in range(N)]),'p_exist':ea.summary([rows[i]['measurement']['p_exist'] for i in range(N)]),'reliability_W':ea.optional_summary([rows[i]['measurement']['reliability']['median'] for i in range(N)])},'frozen_phase_a_positive_control':{'MPLUS_A_median_T':float(a['positive_control']['MPLUS_A_median_T']),'MPLUS_B_median_T':float(a['positive_control']['MPLUS_B_median_T']),'positive_control_valid':True,'T_plus_center':plus,'delta_plus_q95':DELTA},'primary':{'D_M6_minus_phaseA_plus_center':d6,'gap_M6':gap,'sufficiency_threshold':-DELTA,'no_material_loss':sufficient,'classification':SUFF if sufficient else INSUFF},'secondary_nonpromoting':{'T_M5_reconstructed_from_frozen_phaseE':t5,'T_M4_reconstructed_from_frozen_phaseD':t4,'T_M6_minus_M5':vs5,'summary_T_M6_minus_M5':ea.summary(vs5),'T_M6_minus_M4':vs4,'summary_T_M6_minus_M4':ea.summary(vs4),'q90_delta_plus':q90,'q90_no_material_loss':bool(gap>=-q90),'q99_delta_plus':q99,'q99_no_material_loss':bool(gap>=-q99),'changes_primary_decision':False},'training_only_geometry_gate':{'f0_selected_start_indices':starts,'gate_intercept_and_K_R_S_slopes_by_fold':gates,'phase_f_refit_performed':False},'model_complexity':{'latent_states':2,'free_continuous_parameters_per_fold':46,'free_parameters_per_local_component':21,'free_gate_parameters':4,'explicit_nonadjacent_parameters':0,'generic_distance_parameters':0,'named_distant_pair_parameters':0,'signature_specific_parameters':0},'guardrails':{'target_edge_loss_optimized':False,'target_selected_nonadjacent_edges_used':False,'target_selected_latent_start_used':False,'target_selected_gate_used':False,'readings_averaged':False,'phase_a_positive_control_rerun_or_reselected':False,'phase_e_reselected':False,'post_reveal_model_change_allowed':False}}
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':result['status'],'T_median':result['measurement']['T']['median'],'R_ZL3b_median':result['measurement']['R_ZL3b']['median'],'R_IT2a_median':result['measurement']['R_IT2a']['median'],'E_median':result['measurement']['residual_energy']['median'],'W_median':None if result['measurement']['reliability_W']['finite'] is None else result['measurement']['reliability_W']['finite']['median'],'gap_M6':gap,'median_T_M6_minus_M5':result['secondary_nonpromoting']['summary_T_M6_minus_M5']['median'],'median_T_M6_minus_M4':result['secondary_nonpromoting']['summary_T_M6_minus_M4']['median'],'classification':result['primary']['classification']},ensure_ascii=False,sort_keys=True,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main(sys.argv))
