#!/usr/bin/env python3
"""Generate the deterministic Issue #75 Phase-B post-reveal report and license marker.

This script does not score, fit, regenerate, or alter any scientific case. It
reads the permanently frozen Phase-B aggregate and target-blind B0 authority,
verifies repository evidence, and writes explanatory/reporting artifacts only.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRST = HERE / "stage-b-first-reveal"
B0 = HERE / "stage-b0"
PHASE_A = HERE / "stage-a-first-reveal"

EXPECTED_SCI_HEAD = "f9b3d0d5e6c05d0a747a9c5d7dd543513d1dc7d2"
EXPECTED_PLAN = "f09ba414de015eabd1eef03f275be68b82752d7f"
EXPECTED_B0_SHA = "9c180c7026e4f9464954dd029b71973cc1890f25223af6152959649dde57e834"
EXPECTED_PHASE_A_SHA = "fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540"
EXPECTED_DELTA = 0.009768313008182594
SUFFICIENT = "M2_GENERIC_KRS_SHAPE_DESCRIPTORS_SUFFICIENT"
INSUFFICIENT = "M2_GENERIC_KRS_SHAPE_DESCRIPTORS_INSUFFICIENT_STATEFUL_CONFIGURATION_RULE_REQUIRED"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fmt(x, n=6):
    if x is None:
        return "NA"
    return f"{float(x):.{n}f}"


def main() -> int:
    agg_path = FIRST / "phase75b_aggregate.json"
    sums_path = FIRST / "SHA256SUMS.txt"
    auth_path = FIRST / "ARTIFACT_AUTHORITY.txt"
    if not agg_path.exists() or not sums_path.exists() or not auth_path.exists():
        raise RuntimeError("permanent Phase-B first-reveal authority is incomplete")
    digest = sha256(agg_path)
    if digest not in sums_path.read_text(encoding="utf-8"):
        raise RuntimeError("Phase-B aggregate SHA not present in frozen checksum authority")

    r = json.loads(agg_path.read_text(encoding="utf-8"))
    if r.get("schema") != "issue75-phaseB-m2-aggregate-v1":
        raise RuntimeError("Phase-B aggregate schema changed")
    if r.get("status") != "PHASE_B_M2_COMPLETE_31_CASE_POPULATION_AGGREGATED":
        raise RuntimeError("Phase-B aggregate status changed")
    if r.get("scientific_head") != EXPECTED_SCI_HEAD:
        raise RuntimeError("Phase-B scientific head changed")
    if r.get("plan_b_commit") != EXPECTED_PLAN:
        raise RuntimeError("Phase-B plan authority changed")
    if r.get("phase_b0_authority_sha256") != EXPECTED_B0_SHA:
        raise RuntimeError("Phase-B0 authority changed")
    if r.get("phase_a_positive_control_aggregate_sha256") != EXPECTED_PHASE_A_SHA:
        raise RuntimeError("Phase-A control authority changed")
    if r.get("population", {}).get("total_results") != 31:
        raise RuntimeError("Phase-B population changed")
    if r.get("population", {}).get("complete_population") is not True:
        raise RuntimeError("Phase-B population incomplete")
    if r.get("population", {}).get("no_drops") is not True or r.get("population", {}).get("no_rerolls") is not True:
        raise RuntimeError("Phase-B population integrity changed")
    if float(r["frozen_phase_a_positive_control"]["delta_plus_q95"]) != EXPECTED_DELTA:
        raise RuntimeError("Phase-A q95 tolerance changed")
    classification = r["primary"]["classification"]
    if classification not in {SUFFICIENT, INSUFFICIENT}:
        raise RuntimeError(f"unexpected Phase-B classification: {classification}")

    b0 = json.loads((B0 / "generator_authority.json").read_text(encoding="utf-8"))
    if sha256(B0 / "generator_authority.json") != EXPECTED_B0_SHA:
        raise RuntimeError("B0 repository SHA changed")

    m = r["measurement"]
    W = m["reliability_W"]["finite"]
    wmed = None if W is None else W["median"]
    p = m["p_exist"]
    primary = r["primary"]
    sens = r["nonpromoting_tolerance_sensitivity"]

    class_counts = [b0["fit"][str(f)]["descriptor_class_count"] for f in range(5)]
    train_distinct = [b0["fit"][str(f)]["training_distinct_signatures"] for f in range(5)]
    generated_distinct = [c["distinct_signatures"] for c in b0["cases"]]

    if classification == SUFFICIENT:
        conclusion = (
            "Generic occupancy geometry (K, contiguous-run count R, and span S) plus slot main effects "
            "is sufficient within the previously frozen empirical-signature positive-control variation."
        )
        next_step = (
            "M3 is not licensed. The current minimum tested sufficient layer is the generic K/R/S shape model. "
            "Future work should test independent responsibilities without adding a richer R1 model merely to improve fit."
        )
        marker_name = "DECISION_B_M2_SUFFICIENT_STOP.md"
        marker_title = "# Issue #75 Phase B — M2 sufficient; M3 not licensed"
    else:
        conclusion = (
            "Generic occupancy geometry (K, contiguous-run count R, and span S) plus slot main effects is still "
            "materially worse than the frozen empirical-signature positive control."
        )
        next_step = (
            "The preregistered outcome licenses M3: a separately preregistered compact state/transition construction "
            "grammar may now be tested. It must not fit the 66 target edges directly."
        )
        marker_name = "DECISION_B_M3_LICENSED.md"
        marker_title = "# Issue #75 Phase B — M2 insufficient; M3 licensed"

    report = f"""# Issue #75 Phase B — generic K/R/S occupancy-shape result

Date: 2026-09-01  
Status: **COMPLETE / FIRST-REVEAL AUTHORITY PERMANENTLY FROZEN**

## Primary result

Frozen classification:

`{classification}`

{conclusion}

## Exact authority

- scientific head: `{EXPECTED_SCI_HEAD}`
- first-reveal run: `33504819493` — success
- complete population: `31/31`
- drops: `0`
- rerolls: `0`
- aggregate SHA-256: `{digest}`
- Phase-B0 SHA-256: `{EXPECTED_B0_SHA}`
- frozen Phase-A positive-control aggregate SHA-256: `{EXPECTED_PHASE_A_SHA}`

## M2-KRS result

| metric | frozen value |
|---|---:|
| median T=min(R_ZL3b,R_IT2a) | `{fmt(m['T']['median'], 9)}` |
| median R ZL3b | `{fmt(m['R_ZL3b']['median'], 9)}` |
| median R IT2a | `{fmt(m['R_IT2a']['median'], 9)}` |
| median residual energy E | `{fmt(m['residual_energy']['median'], 9)}` |
| median fold reliability W | `{fmt(wmed, 9)}` |
| median p_exist | `{fmt(p['median'], 9)}` |
| median sign agreement ZL3b | `{fmt(m['sign_ZL3b']['median'], 3)}/66` |
| median sign agreement IT2a | `{fmt(m['sign_IT2a']['median'], 3)}/66` |
| paired median gap vs frozen M+ center | `{fmt(primary['gap_M2'], 9)}` |
| allowed loss q95 | `-{EXPECTED_DELTA}` |
| no material loss | `{str(bool(primary['no_material_loss'])).lower()}` |

Primary decision rule was frozen before target reveal:

`gap_M2 >= -{EXPECTED_DELTA}`

Observed gap:

`{primary['gap_M2']}`

## Model complexity / non-memorization audit

M2 uses the joint training-only descriptor distribution of:

- `K`: occupied-slot count;
- `R`: number of contiguous occupied runs;
- `S`: occupied span.

Within each descriptor class it uses only slot main effects; it has zero explicit slot-pair interaction parameters and zero empirical complete-signature-specific parameters.

Target-blind B0 diagnostics:

- descriptor classes by fold: `{class_counts}`;
- training distinct complete signatures by fold: `{train_distinct}`;
- generated distinct complete signatures across the 31 reps: `{min(generated_distinct)}..{max(generated_distinct)}`.

Thus M2 is materially coarser than empirical-signature resampling and generates a much broader signature set. Its result is not a disguised replay of the empirical inventory.

## Sensitivity

The primary q95 tolerance remains authoritative. Non-promoting checks:

- q90 allowed variation: `{sens['q90_delta_plus']}`; no-material-loss `{str(bool(sens['q90_no_material_loss'])).lower()}`;
- q99 allowed variation: `{sens['q99_delta_plus']}`; no-material-loss `{str(bool(sens['q99_no_material_loss'])).lower()}`.

## Scientific interpretation

Phase A already showed:

1. individual slot propensity is insufficient;
2. adding occupied-slot count K creates strong dependence but the wrong topology;
3. empirical complete-signature inventory is sufficient as a cross-fitted positive control.

Phase B asks whether coarse generic shape — count, contiguity, and span — bridges that gap.

{conclusion}

## Next frontier

{next_step}

## Boundaries

This result concerns the 12-slot occupancy representation only. It does not identify slot meanings, literal token spellings, plaintext, cipher tables, natural-language word boundaries, historical Naibbe use, or decipherment.
"""

    marker = f"""{marker_title}

Date: 2026-09-01  
Classification: `{classification}`

- Phase-B first-reveal scientific head: `{EXPECTED_SCI_HEAD}`
- aggregate SHA-256: `{digest}`
- gap M2: `{primary['gap_M2']}`
- frozen q95 delta: `{EXPECTED_DELTA}`
- no material loss: `{str(bool(primary['no_material_loss'])).lower()}`

{next_step}
"""

    ledger = f"""# Hypothesis ledger addendum — Issue #75 Phase B

Status: **PHASE B COMPLETE**

## H75-M2 — generic K/R/S occupancy geometry plus slot main effects is sufficient

### Prediction

If the R1-relevant configuration information is primarily coarse binary-shape geometry, then the cross-fitted M2-KRS generator should fall within the frozen Phase-A empirical-signature control variation.

### Frozen test

- 31 target-blind-frozen M2 corpora;
- exact candidate-owned 1000-reference / 1000-test residual calibration;
- ZL3b and IT2a kept separate;
- `T=min(R_ZL3b,R_IT2a)`;
- paired comparison to the exact Phase-A M+ centers;
- allowed material loss `{EXPECTED_DELTA}`.

### Result

Classification: `{classification}`

- median T: `{m['T']['median']}`
- median R ZL3b: `{m['R_ZL3b']['median']}`
- median R IT2a: `{m['R_IT2a']['median']}`
- median gap vs M+ center: `{primary['gap_M2']}`
- no material loss: `{primary['no_material_loss']}`

{conclusion}

## Next licensed inference

{next_step}

Authority: `experiments/minimal-occupancy-generator/stage-b-first-reveal/phase75b_aggregate.json`, SHA-256 `{digest}`.
"""

    (HERE / "REPORT_B.md").write_text(report, encoding="utf-8")
    (HERE / marker_name).write_text(marker, encoding="utf-8")
    (ROOT / "research" / "HYPOTHESIS_LEDGER_ADDENDUM_ISSUE75_PHASE_B.md").write_text(ledger, encoding="utf-8")

    print(json.dumps({
        "classification": classification,
        "aggregate_sha256": digest,
        "T_median": m["T"]["median"],
        "R_ZL3b_median": m["R_ZL3b"]["median"],
        "R_IT2a_median": m["R_IT2a"]["median"],
        "E_median": m["residual_energy"]["median"],
        "W_median": wmed,
        "gap_M2": primary["gap_M2"],
        "delta_plus_q95": EXPECTED_DELTA,
        "marker": marker_name,
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
