#!/usr/bin/env python3
"""Generate deterministic Issue #75 Phase-C report and next-frontier marker."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRST = HERE / "stage-c-first-reveal"
C0 = HERE / "stage-c0"
PHASE_A = HERE / "stage-a-first-reveal"
SUFFICIENT = "M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_SUFFICIENT"
INSUFFICIENT = "M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED"
PHASE_A_SHA = "fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540"
DELTA = 0.009768313008182594


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fmt(x, n=9):
    if x is None:
        return "NA"
    return f"{float(x):.{n}f}"


def main() -> int:
    agg_path = FIRST / "phase75c_aggregate.json"
    sums_path = FIRST / "SHA256SUMS.txt"
    auth_path = FIRST / "ARTIFACT_AUTHORITY.txt"
    if not agg_path.exists() or not sums_path.exists() or not auth_path.exists():
        raise RuntimeError("permanent Phase-C first-reveal authority is incomplete")
    agg_sha = sha256(agg_path)
    if agg_sha not in sums_path.read_text(encoding="utf-8"):
        raise RuntimeError("Phase-C aggregate SHA not present in frozen checksum authority")
    r = json.loads(agg_path.read_text(encoding="utf-8"))
    if r.get("schema") != "issue75-phaseC-m3-aggregate-v1":
        raise RuntimeError("Phase-C aggregate schema changed")
    if r.get("status") != "PHASE_C_M3_COMPLETE_31_CASE_POPULATION_AGGREGATED":
        raise RuntimeError("Phase-C aggregate status changed")
    if r.get("population", {}).get("total_results") != 31 or r.get("population", {}).get("complete_population") is not True:
        raise RuntimeError("Phase-C population incomplete")
    if r.get("population", {}).get("no_drops") is not True or r.get("population", {}).get("no_rerolls") is not True:
        raise RuntimeError("Phase-C population integrity changed")
    if r.get("phase_a_positive_control_aggregate_sha256") != PHASE_A_SHA:
        raise RuntimeError("Phase-A positive-control authority changed")
    if float(r["frozen_phase_a_positive_control"]["delta_plus_q95"]) != DELTA:
        raise RuntimeError("Phase-A q95 tolerance changed")
    if r.get("model_complexity", {}).get("free_continuous_parameters_per_fold") != 21:
        raise RuntimeError("Phase-C model complexity changed")
    if r.get("model_complexity", {}).get("explicit_nonadjacent_pair_interaction_parameters") != 0:
        raise RuntimeError("Phase-C nonadjacent interaction guardrail changed")
    if any(r.get("guardrails", {}).values()):
        raise RuntimeError("Phase-C guardrail violation in frozen aggregate")

    classification = r["primary"]["classification"]
    if classification not in {SUFFICIENT, INSUFFICIENT}:
        raise RuntimeError(f"unexpected Phase-C classification: {classification}")

    c0_freeze = (HERE / "C0_FREEZE_C.md").read_text(encoding="utf-8")
    msha = re.search(r"C0 authority SHA-256: `([0-9a-f]{64})`", c0_freeze)
    if not msha or r["phase_c0_authority_sha256"] != msha.group(1):
        raise RuntimeError("Phase-C0 authority mismatch")
    c0 = json.loads((C0 / "generator_authority.json").read_text(encoding="utf-8"))
    if sha256(C0 / "generator_authority.json") != msha.group(1):
        raise RuntimeError("Phase-C0 repository SHA changed")

    meas = r["measurement"]
    W = meas["reliability_W"]["finite"]
    wmed = None if W is None else W["median"]
    primary = r["primary"]
    sens = r["nonpromoting_tolerance_sensitivity"]
    class_counts = [c0["fit"][str(f)]["descriptor_class_count"] for f in range(5)]
    train_distinct = [c0["fit"][str(f)]["training_distinct_signatures"] for f in range(5)]
    generated_distinct = [x["distinct_signatures"] for x in c0["cases"]]
    fit_max = max(c0["fit"][str(f)]["max_abs_reported_moment_error"] for f in range(5))

    if classification == SUFFICIENT:
        conclusion = (
            "The compact position-specific nearest-neighbor transition grammar is sufficient within the "
            "previously frozen empirical-signature positive-control variation."
        )
        next_step = (
            "The preregistered rule stops the R1 model-complexity ladder here. A richer nonlocal/latent R1 model "
            "must not be added merely to improve fit. The next research should test whether this occupancy grammar "
            "can be embedded in a reversible/generative mechanism and survive independent R2/R3/R4 responsibilities."
        )
        marker = "DECISION_C_R1_LADDER_STOP.md"
        title = "# Issue #75 Phase C — nearest-neighbor occupancy grammar sufficient; R1 ladder stopped"
    else:
        conclusion = (
            "Even after preserving coarse K/R/S geometry and fitting position-specific nearest-neighbor occupancy "
            "compatibilities, the model remains materially worse than the frozen empirical-signature control."
        )
        next_step = (
            "The frozen outcome licenses a separately preregistered nonlocal or latent configuration model. "
            "No such model has yet been selected or fit. Any next model must remain compact and generic and must not "
            "optimize the frozen 66 target edges directly."
        )
        marker = "DECISION_C_NONLOCAL_LATENT_LICENSED.md"
        title = "# Issue #75 Phase C — nearest-neighbor grammar insufficient; nonlocal/latent frontier licensed"

    report = f"""# Issue #75 Phase C — KRS nearest-neighbor transition grammar result

Date: 2026-09-01  
Status: **COMPLETE / FIRST-REVEAL AUTHORITY PERMANENTLY FROZEN**

## Frozen classification

`{classification}`

{conclusion}

## Exact authority

- scientific head: `{r['scientific_head']}`
- complete population: `31/31`
- drops: `0`
- rerolls: `0`
- aggregate SHA-256: `{agg_sha}`
- Phase-C0 SHA-256: `{r['phase_c0_authority_sha256']}`
- Phase-A positive-control SHA-256: `{PHASE_A_SHA}`

## M3 result

| metric | value |
|---|---:|
| median T=min(R_ZL3b,R_IT2a) | `{fmt(meas['T']['median'])}` |
| median R ZL3b | `{fmt(meas['R_ZL3b']['median'])}` |
| median R IT2a | `{fmt(meas['R_IT2a']['median'])}` |
| median residual energy E | `{fmt(meas['residual_energy']['median'])}` |
| median reliability W | `{fmt(wmed)}` |
| median p_exist | `{fmt(meas['p_exist']['median'])}` |
| median sign agreement ZL3b | `{fmt(meas['sign_ZL3b']['median'],3)}/66` |
| median sign agreement IT2a | `{fmt(meas['sign_IT2a']['median'],3)}/66` |
| paired median gap vs Phase-A M+ center | `{fmt(primary['gap_M3'])}` |
| allowed q95 loss | `-{DELTA}` |
| no material loss | `{str(bool(primary['no_material_loss'])).lower()}` |

Primary decision was frozen before target access:

`gap_M3 >= -{DELTA}`.

Observed gap:

`{primary['gap_M3']}`.

## Model complexity

M3 retains the target-blind training K/R/S descriptor distribution and adds only position-specific nearest-neighbor occupancy compatibility:

- 11 free unary parameters per fold;
- 10 free adjacent interaction parameters per fold;
- total 21 continuous parameters per fold;
- 0 explicit nonadjacent pair-interaction parameters;
- 0 empirical complete-signature-specific parameters.

C0 diagnostics:

- K/R/S descriptor classes by fold: `{class_counts}`;
- training distinct complete signatures by fold: `{train_distinct}`;
- generated distinct signature range: `{min(generated_distinct)}..{max(generated_distinct)}`;
- maximum training moment fit error: `{fit_max}`.

## Sensitivity

The q95 rule above is primary. Non-promoting checks:

- q90 delta `{sens['q90_delta_plus']}` -> no-material-loss `{str(bool(sens['q90_no_material_loss'])).lower()}`;
- q99 delta `{sens['q99_delta_plus']}` -> no-material-loss `{str(bool(sens['q99_no_material_loss'])).lower()}`.

## Scientific interpretation

The Issue #75 ladder now distinguishes four levels:

1. slot marginals alone (M0);
2. marginals + occupied-slot count K (M1);
3. generic K/R/S whole-pattern geometry (M2);
4. K/R/S + position-specific nearest-neighbor transition compatibility (M3).

{conclusion}

## Next frontier

{next_step}

## Boundaries

This remains an occupancy-level result. It does not assign meanings to slots, recover literal token spelling, identify plaintext, establish a cipher table, prove natural-language word boundaries, establish historical Naibbe use, or constitute decipherment.
"""

    marker_text = f"""{title}

Date: 2026-09-01  
Classification: `{classification}`

- scientific head: `{r['scientific_head']}`
- aggregate SHA-256: `{agg_sha}`
- median T: `{meas['T']['median']}`
- gap M3: `{primary['gap_M3']}`
- frozen q95 delta: `{DELTA}`
- no material loss: `{str(bool(primary['no_material_loss'])).lower()}`

{next_step}
"""

    ledger = f"""# Hypothesis ledger addendum — Issue #75 Phase C

Status: **PHASE C COMPLETE**

## H75-M3 — K/R/S-conditioned nearest-neighbor occupancy compatibility is sufficient

### Prediction

A compact model preserving training-only K/R/S geometry and matching only unary occupancies plus the 11 adjacent slot-pair occupancies should reproduce the complete 66-edge target topology within frozen empirical-signature control variation if the unresolved configuration rule is primarily local/sequential.

### Result

Classification: `{classification}`

- median T: `{meas['T']['median']}`
- median R ZL3b: `{meas['R_ZL3b']['median']}`
- median R IT2a: `{meas['R_IT2a']['median']}`
- median gap vs M+ center: `{primary['gap_M3']}`
- allowed loss: `{DELTA}`
- no material loss: `{primary['no_material_loss']}`

{conclusion}

## Licensed next inference

{next_step}

Authority: `experiments/minimal-occupancy-generator/stage-c-first-reveal/phase75c_aggregate.json`, SHA-256 `{agg_sha}`.
"""

    (HERE / "REPORT_C.md").write_text(report, encoding="utf-8")
    (HERE / marker).write_text(marker_text, encoding="utf-8")
    (ROOT / "research" / "HYPOTHESIS_LEDGER_ADDENDUM_ISSUE75_PHASE_C.md").write_text(ledger, encoding="utf-8")

    print(json.dumps({
        "classification": classification,
        "aggregate_sha256": agg_sha,
        "T_median": meas["T"]["median"],
        "R_ZL3b_median": meas["R_ZL3b"]["median"],
        "R_IT2a_median": meas["R_IT2a"]["median"],
        "E_median": meas["residual_energy"]["median"],
        "W_median": wmed,
        "gap_M3": primary["gap_M3"],
        "delta_plus_q95": DELTA,
        "marker": marker,
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
