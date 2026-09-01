#!/usr/bin/env python3
"""Aggregate Issue #75 Phase E M5-KRS-2MIX-CHAIN first-reveal population."""
from __future__ import annotations

import glob
import hashlib
import json
import math
import re
import statistics
import sys
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve().parent
PHASE_A_PATH = HERE / "stage-a-first-reveal" / "phase75a_aggregate.json"
PHASE_C_PATH = HERE / "stage-c-first-reveal" / "phase75c_aggregate.json"
PHASE_D_PATH = HERE / "stage-d-first-reveal" / "phase75d_aggregate.json"
E0_PATH = HERE / "stage-e0" / "generator_authority.json"
E0_FREEZE_PATH = HERE / "E0_FREEZE_E.md"
PHASE_A_SHA = "fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540"
PHASE_C_SHA = "34affe98b68a1e410ea3d4384a917450c2b58e7a8e02a30da8befa660712421a"
PHASE_D_SHA = "c15ffb92030220596cacef9db9cb3bdb26c92607f675c24ff0fa607e16764489"
E0_SHA = "4c406e60872f8fcfd27901cc41901db04c1aa192fa9ee91a14c01ea3dbe46a89"
FAMILY = "M5-KRS-2MIX-CHAIN"
N_REPS = 31
DELTA = 0.009768313008182594
SUFFICIENT = "M5_KRS_TWO_LATENT_CHAIN_MODES_SUFFICIENT"
INSUFFICIENT = "M5_KRS_TWO_LATENT_CHAIN_MODES_INSUFFICIENT_RICHER_LATENT_OR_CONFIGURATION_RULE_REQUIRED"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def quantile(xs: Sequence[float], q: float) -> float:
    ys = sorted(float(x) for x in xs)
    p = (len(ys) - 1) * q
    lo, hi = int(math.floor(p)), int(math.ceil(p))
    return ys[lo] if lo == hi else float(ys[lo] * (hi-p) + ys[hi] * (p-lo))


def summary(xs: Sequence[float]) -> dict:
    ys = [float(x) for x in xs]
    if not ys or any(not math.isfinite(x) for x in ys):
        raise RuntimeError("invalid required summary")
    return {
        "n": len(ys), "min": min(ys), "q25": quantile(ys,.25),
        "median": float(statistics.median(ys)), "q75": quantile(ys,.75),
        "max": max(ys), "mean": float(statistics.fmean(ys)),
        "sd_population": float(statistics.pstdev(ys)),
    }


def optional_summary(xs: Sequence[float | None]) -> dict:
    vals=[float(x) for x in xs if x is not None and math.isfinite(float(x))]
    return {"n_total":len(xs),"n_finite":len(vals),"finite":None if not vals else summary(vals)}


def load_controls() -> tuple[dict,dict,dict,dict,list[float],list[float],list[float]]:
    for p,sha,name in ((PHASE_A_PATH,PHASE_A_SHA,'A'),(PHASE_C_PATH,PHASE_C_SHA,'C'),(PHASE_D_PATH,PHASE_D_SHA,'D'),(E0_PATH,E0_SHA,'E0')):
        if sha256_file(p)!=sha:
            raise RuntimeError(f"Phase {name} authority SHA changed")
    a=json.loads(PHASE_A_PATH.read_text(encoding='utf-8'))
    c=json.loads(PHASE_C_PATH.read_text(encoding='utf-8'))
    d=json.loads(PHASE_D_PATH.read_text(encoding='utf-8'))
    e0=json.loads(E0_PATH.read_text(encoding='utf-8'))
    if a.get('schema')!='issue75-phaseA-aggregate-v1' or a.get('positive_control',{}).get('valid') is not True:
        raise RuntimeError('Phase A positive-control authority changed')
    if float(a['primary_q95_equivalence']['delta_plus'])!=DELTA:
        raise RuntimeError('Phase A q95 tolerance changed')
    if c.get('primary',{}).get('classification')!='M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED':
        raise RuntimeError('Phase C classification changed')
    if d.get('primary',{}).get('classification')!='M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED':
        raise RuntimeError('Phase D classification changed')
    if e0.get('schema')!='issue75-phaseE0-m5-krs-2mix-chain-generator-authority-v1' or any(e0.get('target_access',{}).values()):
        raise RuntimeError('Phase E0 target-blind authority changed')
    plus=[float(x) for x in a['paired_values']['T_plus_center']]
    d3=[float(x) for x in c['primary']['D_M3_minus_phaseA_plus_center']]
    d4=[float(x) for x in d['primary']['D_M4_minus_phaseA_plus_center']]
    if len(plus)!=N_REPS or len(d3)!=N_REPS or len(d4)!=N_REPS:
        raise RuntimeError('paired control population changed')
    t3=[plus[i]+d3[i] for i in range(N_REPS)]
    t4=[plus[i]+d4[i] for i in range(N_REPS)]
    if abs(statistics.median(t3)-float(c['measurement']['T']['median']))>1e-12:
        raise RuntimeError('Phase C T reconstruction mismatch')
    if abs(statistics.median(t4)-float(d['measurement']['T']['median']))>1e-12:
        raise RuntimeError('Phase D T reconstruction mismatch')
    return a,c,d,e0,plus,t3,t4


def validate_case(r: Mapping, rep: int, frozen_target_authority: Mapping) -> None:
    if r.get('schema')!='issue75-phaseE-m5-r1-score-v1' or r.get('status')!='PHASE_E_M5_FIRST_REVEAL_CASE_SCORED':
        raise RuntimeError(f'bad Phase E score contract rep {rep}')
    if r.get('family')!=FAMILY or int(r.get('rep',-1))!=rep:
        raise RuntimeError(f'bad Phase E identity rep {rep}')
    if r.get('pair_count')!=66 or r.get('target_readings_averaged') is not False:
        raise RuntimeError(f'bad topology contract rep {rep}')
    if r.get('no_case_selection') is not True or r.get('no_reroll') is not True:
        raise RuntimeError(f'selection guardrail failed rep {rep}')
    a=r.get('candidate_audit',{})
    if a.get('phase_e0_authority_sha256')!=E0_SHA or a.get('exact_phase_e0_replay') is not True or a.get('frozen_parameters_reconstructed') is not True:
        raise RuntimeError(f'E0 replay failed rep {rep}')
    if a.get('tokens')!=25071 or a.get('fold_tokens')!=[4430,4810,5516,5447,4868] or a.get('all_zero_count')!=0:
        raise RuntimeError(f'population changed rep {rep}')
    if len(a.get('fit_audits',{}))!=5:
        raise RuntimeError(f'fit audit missing rep {rep}')
    m=r.get('measurement',{})
    if m.get('reference_namespace')!=f'issue75:phaseE:M5-KRS-2MIX-CHAIN:rep{rep}:reference' or m.get('test_namespace')!=f'issue75:phaseE:M5-KRS-2MIX-CHAIN:rep{rep}:test':
        raise RuntimeError(f'null namespace changed rep {rep}')
    if m.get('n_reference')!=1000 or m.get('n_test')!=1000 or len(m.get('z_full',[]))!=66:
        raise RuntimeError(f'null contract changed rep {rep}')
    if not math.isfinite(float(m.get('residual_energy'))) or not 0<float(m.get('p_exist'))<=1:
        raise RuntimeError(f'residual diagnostic invalid rep {rep}')
    for name in ('ZL3b','IT2a'):
        t=r.get('topology',{}).get(name,{})
        if not math.isfinite(float(t.get('pearson'))) or t.get('sign_denominator')!=66 or not 0<=int(t.get('sign_agreement'))<=66:
            raise RuntimeError(f'topology invalid rep {rep} {name}')
    T=float(r.get('T'))
    if abs(T-min(float(r['topology']['ZL3b']['pearson']),float(r['topology']['IT2a']['pearson'])))>1e-15:
        raise RuntimeError(f'T mismatch rep {rep}')
    if r.get('target_authority')!=frozen_target_authority:
        raise RuntimeError(f'target authority changed rep {rep}')
    if any(v is not True for v in r.get('target_access',{}).values()):
        raise RuntimeError(f'target access record incomplete rep {rep}')


def main(argv: Sequence[str]) -> int:
    if len(argv)!=4:
        raise SystemExit(f'usage: {argv[0]} INPUT_DIR OUTPUT_JSON SCIENTIFIC_HEAD')
    inp,out,head=Path(argv[1]).resolve(),Path(argv[2]).resolve(),argv[3].strip()
    a,c,d,e0,plus,t3,t4=load_controls()
    target_authority=d['target_authority']
    if c['target_authority']!=target_authority:
        raise RuntimeError('frozen target authority changed between C and D')

    paths=sorted(glob.glob(str(inp/'*.json')))
    if len(paths)!=N_REPS:
        raise RuntimeError(f'need exactly 31 Phase E score JSON files, found {len(paths)}')
    rows={}
    for p in paths:
        r=json.loads(Path(p).read_text(encoding='utf-8'))
        rep=int(r.get('rep',-1))
        if rep not in range(N_REPS) or rep in rows:
            raise RuntimeError(f'unexpected/duplicate Phase E rep {rep}')
        validate_case(r,rep,target_authority)
        rows[rep]=r
    if set(rows)!=set(range(N_REPS)):
        raise RuntimeError('complete Phase E population mismatch')

    T=[float(rows[r]['T']) for r in range(N_REPS)]
    d5=[T[i]-plus[i] for i in range(N_REPS)]
    gap=float(statistics.median(d5))
    sufficient=bool(gap>=-DELTA)
    q90=float(a['nonpromoting_tolerance_sensitivity']['q90']['delta_plus'])
    q99=float(a['nonpromoting_tolerance_sensitivity']['q99']['delta_plus'])
    vs3=[T[i]-t3[i] for i in range(N_REPS)]
    vs4=[T[i]-t4[i] for i in range(N_REPS)]
    pis=[float(e0['fit'][str(f)]['pi']) for f in range(5)]
    llg=[float(e0['fit'][str(f)]['selected_log_likelihood_gain_over_m3']) for f in range(5)]
    starts=[int(e0['fit'][str(f)]['selected_start_index']) for f in range(5)]

    result={
        'schema':'issue75-phaseE-m5-aggregate-v1',
        'status':'PHASE_E_M5_COMPLETE_31_CASE_POPULATION_AGGREGATED',
        'scientific_head':head,
        'phase_e0_authority_sha256':E0_SHA,
        'phase_a_positive_control_aggregate_sha256':PHASE_A_SHA,
        'phase_c_m3_aggregate_sha256':PHASE_C_SHA,
        'phase_d_m4_aggregate_sha256':PHASE_D_SHA,
        'population':{'family':FAMILY,'n_reps':N_REPS,'total_results':N_REPS,'complete_population':True,'no_drops':True,'no_rerolls':True},
        'target_authority':target_authority,
        'measurement':{
            'T':summary(T),
            'R_ZL3b':summary([rows[r]['topology']['ZL3b']['pearson'] for r in range(N_REPS)]),
            'R_IT2a':summary([rows[r]['topology']['IT2a']['pearson'] for r in range(N_REPS)]),
            'sign_ZL3b':summary([rows[r]['topology']['ZL3b']['sign_agreement'] for r in range(N_REPS)]),
            'sign_IT2a':summary([rows[r]['topology']['IT2a']['sign_agreement'] for r in range(N_REPS)]),
            'residual_energy':summary([rows[r]['measurement']['residual_energy'] for r in range(N_REPS)]),
            'p_exist':summary([rows[r]['measurement']['p_exist'] for r in range(N_REPS)]),
            'reliability_W':optional_summary([rows[r]['measurement']['reliability']['median'] for r in range(N_REPS)]),
        },
        'frozen_phase_a_positive_control':{
            'MPLUS_A_median_T':float(a['positive_control']['MPLUS_A_median_T']),
            'MPLUS_B_median_T':float(a['positive_control']['MPLUS_B_median_T']),
            'positive_control_valid':True,
            'T_plus_center':plus,
            'delta_plus_q95':DELTA,
        },
        'primary':{
            'D_M5_minus_phaseA_plus_center':d5,
            'gap_M5':gap,
            'sufficiency_threshold':-DELTA,
            'no_material_loss':sufficient,
            'classification':SUFFICIENT if sufficient else INSUFFICIENT,
        },
        'secondary_nonpromoting':{
            'T_M3_reconstructed_from_frozen_phaseC':t3,
            'T_M4_reconstructed_from_frozen_phaseD':t4,
            'T_M5_minus_M3':vs3,
            'summary_T_M5_minus_M3':summary(vs3),
            'T_M5_minus_M4':vs4,
            'summary_T_M5_minus_M4':summary(vs4),
            'q90_delta_plus':q90,
            'q90_no_material_loss':bool(gap>=-q90),
            'q99_delta_plus':q99,
            'q99_no_material_loss':bool(gap>=-q99),
            'changes_primary_decision':False,
        },
        'training_only_latent_fit':{
            'selected_start_indices':starts,
            'pi_by_fold':pis,
            'pi_summary':summary(pis),
            'conditional_log_likelihood_gain_over_M3_by_fold':llg,
            'conditional_log_likelihood_gain_summary':summary(llg),
        },
        'model_complexity':{
            'latent_states':2,
            'free_continuous_parameters_per_fold':43,
            'free_parameters_per_local_component':21,
            'free_gate_parameters':1,
            'explicit_nonadjacent_parameters':0,
            'generic_distance_parameters':0,
            'named_distant_pair_parameters':0,
            'signature_specific_parameters':0,
        },
        'guardrails':{
            'target_edge_loss_optimized':False,
            'target_selected_nonadjacent_edges_used':False,
            'target_selected_latent_start_used':False,
            'readings_averaged':False,
            'phase_a_positive_control_rerun_or_reselected':False,
            'phase_c_reselected':False,
            'phase_d_reselected':False,
            'post_reveal_model_change_allowed':False,
        },
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({
        'status':result['status'],
        'T_median':result['measurement']['T']['median'],
        'R_ZL3b_median':result['measurement']['R_ZL3b']['median'],
        'R_IT2a_median':result['measurement']['R_IT2a']['median'],
        'E_median':result['measurement']['residual_energy']['median'],
        'W_median':None if result['measurement']['reliability_W']['finite'] is None else result['measurement']['reliability_W']['finite']['median'],
        'gap_M5':gap,
        'median_T_M5_minus_M3':result['secondary_nonpromoting']['summary_T_M5_minus_M3']['median'],
        'median_T_M5_minus_M4':result['secondary_nonpromoting']['summary_T_M5_minus_M4']['median'],
        'classification':result['primary']['classification'],
    },ensure_ascii=False,sort_keys=True,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main(sys.argv))
