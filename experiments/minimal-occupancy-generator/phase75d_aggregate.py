#!/usr/bin/env python3
"""Aggregate Issue #75 Phase D M4-KRS-CHAIN-DISTANCE first-reveal population."""
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
D0_FREEZE_PATH = HERE / "D0_FREEZE_D.md"
PHASE_A_SHA = "fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540"
PHASE_C_SHA = "34affe98b68a1e410ea3d4384a917450c2b58e7a8e02a30da8befa660712421a"
FAMILY = "M4-KRS-CHAIN-DISTANCE"
N_REPS = 31
DELTA = 0.009768313008182594
SUFFICIENT = "M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_SUFFICIENT"
INSUFFICIENT = "M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def expected_d0_sha() -> str:
    text = D0_FREEZE_PATH.read_text(encoding="utf-8")
    m = re.search(r"D0 authority SHA-256: `([0-9a-f]{64})`", text)
    if not m:
        raise RuntimeError("D0 SHA missing from freeze metadata")
    return m.group(1)


def quantile(xs: Sequence[float], q: float) -> float:
    ys = sorted(float(x) for x in xs)
    p = (len(ys)-1)*q
    lo, hi = int(math.floor(p)), int(math.ceil(p))
    return ys[lo] if lo == hi else float(ys[lo]*(hi-p)+ys[hi]*(p-lo))


def summary(xs: Sequence[float]) -> dict:
    ys = [float(x) for x in xs]
    if not ys or any(not math.isfinite(x) for x in ys):
        raise RuntimeError("invalid required summary")
    return {"n":len(ys),"min":min(ys),"q25":quantile(ys,.25),"median":float(statistics.median(ys)),"q75":quantile(ys,.75),"max":max(ys),"mean":float(statistics.fmean(ys)),"sd_population":float(statistics.pstdev(ys))}


def optional_summary(xs: Sequence[float | None]) -> dict:
    vals=[float(x) for x in xs if x is not None and math.isfinite(float(x))]
    return {"n_total":len(xs),"n_finite":len(vals),"finite":None if not vals else summary(vals)}


def load_controls() -> tuple[dict, dict, list[float], list[float]]:
    if sha256_file(PHASE_A_PATH) != PHASE_A_SHA:
        raise RuntimeError("Phase A aggregate SHA changed")
    if sha256_file(PHASE_C_PATH) != PHASE_C_SHA:
        raise RuntimeError("Phase C aggregate SHA changed")
    a=json.loads(PHASE_A_PATH.read_text(encoding="utf-8"))
    c=json.loads(PHASE_C_PATH.read_text(encoding="utf-8"))
    assert a["positive_control"]["valid"] is True
    assert float(a["primary_q95_equivalence"]["delta_plus"]) == DELTA
    plus=[float(x) for x in a["paired_values"]["T_plus_center"]]
    if len(plus)!=N_REPS:
        raise RuntimeError("Phase A paired population changed")
    d3=[float(x) for x in c["primary"]["D_M3_minus_phaseA_plus_center"]]
    if len(d3)!=N_REPS:
        raise RuntimeError("Phase C paired population changed")
    t3=[plus[i]+d3[i] for i in range(N_REPS)]
    return a,c,plus,t3


def validate_case(r: Mapping, rep: int, d0_sha: str) -> None:
    if r.get("schema") != "issue75-phaseD-m4-r1-score-v1" or r.get("status") != "PHASE_D_M4_FIRST_REVEAL_CASE_SCORED":
        raise RuntimeError(f"bad Phase D score contract rep {rep}")
    if r.get("family") != FAMILY or int(r.get("rep",-1)) != rep:
        raise RuntimeError(f"bad Phase D identity rep {rep}")
    if r.get("pair_count") != 66 or r.get("target_readings_averaged") is not False:
        raise RuntimeError(f"bad Phase D topology contract rep {rep}")
    if r.get("no_case_selection") is not True or r.get("no_reroll") is not True:
        raise RuntimeError(f"selection guardrail failed rep {rep}")
    a=r.get("candidate_audit",{})
    if a.get("phase_d0_authority_sha256") != d0_sha or a.get("exact_phase_d0_replay") is not True:
        raise RuntimeError(f"D0 replay failed rep {rep}")
    for key in ("training_unary_moments_exact_d0","training_adjacent_moments_exact_d0","training_distance_moments_exact_d0","descriptor_distribution_exact_d0","rank_29_revalidated","fit_tolerance_revalidated"):
        if a.get(key) is not True:
            raise RuntimeError(f"D0 audit failed rep {rep}: {key}")
    if float(a.get("regenerated_fit_max_abs_reported_moment_error")) > 1e-10:
        raise RuntimeError(f"D0 refit tolerance failed rep {rep}")
    if a.get("tokens") != 25071 or a.get("fold_tokens") != [4430,4810,5516,5447,4868] or a.get("all_zero_count") != 0:
        raise RuntimeError(f"population changed rep {rep}")
    m=r.get("measurement",{})
    if m.get("reference_namespace") != f"issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{rep}:reference" or m.get("test_namespace") != f"issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{rep}:test":
        raise RuntimeError(f"null namespace changed rep {rep}")
    if m.get("n_reference") != 1000 or m.get("n_test") != 1000 or len(m.get("z_full",[])) != 66:
        raise RuntimeError(f"null contract changed rep {rep}")
    if not math.isfinite(float(m.get("residual_energy"))) or not 0 < float(m.get("p_exist")) <= 1:
        raise RuntimeError(f"residual diagnostics invalid rep {rep}")
    for name in ("ZL3b","IT2a"):
        t=r.get("topology",{}).get(name,{})
        if not math.isfinite(float(t.get("pearson"))) or t.get("sign_denominator") != 66 or not 0 <= int(t.get("sign_agreement")) <= 66:
            raise RuntimeError(f"topology invalid rep {rep} {name}")
    T=float(r.get("T"))
    if abs(T-min(float(r["topology"]["ZL3b"]["pearson"]),float(r["topology"]["IT2a"]["pearson"]))) > 1e-15:
        raise RuntimeError(f"T mismatch rep {rep}")
    if any(v is not True for v in r.get("target_access",{}).values()):
        raise RuntimeError(f"target access record incomplete rep {rep}")


def main(argv: Sequence[str]) -> int:
    if len(argv)!=4:
        raise SystemExit(f"usage: {argv[0]} INPUT_DIR OUTPUT_JSON SCIENTIFIC_HEAD")
    inp,out,head=Path(argv[1]).resolve(),Path(argv[2]).resolve(),argv[3].strip()
    d0_sha=expected_d0_sha()
    paths=sorted(glob.glob(str(inp/"*.json")))
    if len(paths)!=N_REPS:
        raise RuntimeError(f"need exactly 31 Phase D score JSON files, found {len(paths)}")
    rows={}; target_authority=None
    for p in paths:
        r=json.loads(Path(p).read_text(encoding="utf-8")); rep=int(r.get("rep",-1))
        if rep not in range(N_REPS) or rep in rows:
            raise RuntimeError(f"unexpected/duplicate Phase D rep {rep}")
        validate_case(r,rep,d0_sha)
        if target_authority is None: target_authority=r["target_authority"]
        elif r["target_authority"] != target_authority: raise RuntimeError("target authority differs across reps")
        rows[rep]=r
    if set(rows)!=set(range(N_REPS)): raise RuntimeError("complete Phase D population mismatch")

    a,c,plus,t3=load_controls()
    T=[float(rows[r]["T"]) for r in range(N_REPS)]
    d4=[T[i]-plus[i] for i in range(N_REPS)]
    gap=float(statistics.median(d4))
    sufficient=bool(gap >= -DELTA)
    q90=float(a["nonpromoting_tolerance_sensitivity"]["q90"]["delta_plus"])
    q99=float(a["nonpromoting_tolerance_sensitivity"]["q99"]["delta_plus"])
    versus_m3=[T[i]-t3[i] for i in range(N_REPS)]

    result={
      "schema":"issue75-phaseD-m4-aggregate-v1",
      "status":"PHASE_D_M4_COMPLETE_31_CASE_POPULATION_AGGREGATED",
      "scientific_head":head,
      "phase_d0_authority_sha256":d0_sha,
      "phase_a_positive_control_aggregate_sha256":PHASE_A_SHA,
      "phase_c_m3_aggregate_sha256":PHASE_C_SHA,
      "population":{"family":FAMILY,"n_reps":N_REPS,"total_results":N_REPS,"complete_population":True,"no_drops":True,"no_rerolls":True},
      "target_authority":target_authority,
      "measurement":{
        "T":summary(T),
        "R_ZL3b":summary([rows[r]["topology"]["ZL3b"]["pearson"] for r in range(N_REPS)]),
        "R_IT2a":summary([rows[r]["topology"]["IT2a"]["pearson"] for r in range(N_REPS)]),
        "sign_ZL3b":summary([rows[r]["topology"]["ZL3b"]["sign_agreement"] for r in range(N_REPS)]),
        "sign_IT2a":summary([rows[r]["topology"]["IT2a"]["sign_agreement"] for r in range(N_REPS)]),
        "residual_energy":summary([rows[r]["measurement"]["residual_energy"] for r in range(N_REPS)]),
        "p_exist":summary([rows[r]["measurement"]["p_exist"] for r in range(N_REPS)]),
        "reliability_W":optional_summary([rows[r]["measurement"]["reliability"]["median"] for r in range(N_REPS)]),
      },
      "frozen_phase_a_positive_control":{
        "MPLUS_A_median_T":float(a["positive_control"]["MPLUS_A_median_T"]),
        "MPLUS_B_median_T":float(a["positive_control"]["MPLUS_B_median_T"]),
        "positive_control_valid":True,"T_plus_center":plus,"delta_plus_q95":DELTA},
      "primary":{"D_M4_minus_phaseA_plus_center":d4,"gap_M4":gap,"sufficiency_threshold":-DELTA,"no_material_loss":sufficient,"classification":SUFFICIENT if sufficient else INSUFFICIENT},
      "secondary_nonpromoting":{"T_M3":t3,"T_M4_minus_M3":versus_m3,"median_T_M4_minus_M3":float(statistics.median(versus_m3)),"phase_c_classification":c["primary"]["classification"]},
      "nonpromoting_tolerance_sensitivity":{"q90_delta_plus":q90,"q90_no_material_loss":bool(gap>=-q90),"q99_delta_plus":q99,"q99_no_material_loss":bool(gap>=-q99)},
      "model_complexity":{"free_continuous_parameters_per_fold":29,"free_unary_parameters":11,"free_adjacent_parameters":10,"free_generic_nonadjacent_distance_parameters":8,"explicit_named_nonadjacent_pair_parameters":0,"empirical_signature_specific_parameters":0,"latent_state_parameters":0},
      "guardrails":{"target_edge_loss_optimized":False,"target_selected_nonadjacent_edges_used":False,"readings_averaged":False,"phase_a_positive_control_rerun_or_reselected":False,"phase_c_reselected":False,"latent_architecture_selected":False,"post_reveal_r1_model_added":False},
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"T_median":result["measurement"]["T"]["median"],"R_ZL3b_median":result["measurement"]["R_ZL3b"]["median"],"R_IT2a_median":result["measurement"]["R_IT2a"]["median"],"E_median":result["measurement"]["residual_energy"]["median"],"W_median":None if result["measurement"]["reliability_W"]["finite"] is None else result["measurement"]["reliability_W"]["finite"]["median"],"gap_M4":gap,"median_T_M4_minus_M3":result["secondary_nonpromoting"]["median_T_M4_minus_M3"],"delta_plus_q95":DELTA,"classification":result["primary"]["classification"]},ensure_ascii=False,sort_keys=True,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main(sys.argv))
