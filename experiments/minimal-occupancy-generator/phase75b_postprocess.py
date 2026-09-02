#!/usr/bin/env python3
"""Generate the deterministic Issue #75 Phase-B post-reveal report and M3 license.

Reporting-only code. It reads the permanently frozen Phase-B authority and does
not score, fit, regenerate, reroll, or alter any scientific case.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRST = HERE / "stage-b-first-reveal"
B0 = HERE / "stage-b0"

EXPECTED_SCI_HEAD = "693f627910f5775406da410ec4d7157a161021e4"
EXPECTED_RUN = 33504481315
EXPECTED_ARTIFACT_ID = 9799146088
EXPECTED_ARTIFACT_DIGEST = "sha256:1a0ac70625f70ad87b591b3a4500073a3329a0ca1ef8e691ffb5c8e6c6890d43"
EXPECTED_AGG_SHA = "f0c5e9e210f3cf9bd0fa9c9b818c0ee61649a906b051998346db1583c60fb566"
EXPECTED_PLAN = "f09ba414de015eabd1eef03f275be68b82752d7f"
EXPECTED_B0_SHA = "9c180c7026e4f9464954dd029b71973cc1890f25223af6152959649dde57e834"
EXPECTED_PHASE_A_SHA = "fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540"
EXPECTED_DELTA = 0.009768313008182594
INSUFFICIENT = "M2_GENERIC_KRS_SHAPE_DESCRIPTORS_INSUFFICIENT_STATEFUL_CONFIGURATION_RULE_REQUIRED"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fmt(x, n=6):
    return "NA" if x is None else f"{float(x):.{n}f}"


def main() -> int:
    agg_path = FIRST / "phase75b_aggregate.json"
    auth_path = FIRST / "ARTIFACT_AUTHORITY.txt"
    sums_path = FIRST / "SHA256SUMS.txt"
    for p in (agg_path, auth_path, sums_path, B0 / "generator_authority.json"):
        if not p.exists():
            raise RuntimeError(f"required Phase-B authority missing: {p}")

    digest = sha256(agg_path)
    if digest != EXPECTED_AGG_SHA:
        raise RuntimeError(f"Phase-B aggregate SHA changed: {digest}")
    if digest not in sums_path.read_text(encoding="utf-8"):
        raise RuntimeError("Phase-B aggregate absent from frozen SHA256SUMS")

    auth = auth_path.read_text(encoding="utf-8")
    required_authority_lines = {
        f"source_workflow_run={EXPECTED_RUN}",
        f"source_artifact_id={EXPECTED_ARTIFACT_ID}",
        f"source_artifact_digest={EXPECTED_ARTIFACT_DIGEST}",
        f"aggregate_sha256={EXPECTED_AGG_SHA}",
        f"scientific_head={EXPECTED_SCI_HEAD}",
    }
    for line in required_authority_lines:
        if line not in auth:
            raise RuntimeError(f"permanent artifact authority mismatch: {line}")

    r = json.loads(agg_path.read_text(encoding="utf-8"))
    assert r["schema"] == "issue75-phaseB-m2-aggregate-v1"
    assert r["status"] == "PHASE_B_M2_COMPLETE_31_CASE_POPULATION_AGGREGATED"
    assert r["scientific_head"] == EXPECTED_SCI_HEAD
    assert r["plan_b_commit"] == EXPECTED_PLAN
    assert r["phase_b0_authority_sha256"] == EXPECTED_B0_SHA
    assert r["phase_a_positive_control_aggregate_sha256"] == EXPECTED_PHASE_A_SHA
    assert r["population"]["total_results"] == 31
    assert r["population"]["complete_population"] is True
    assert r["population"]["no_drops"] is True
    assert r["population"]["no_rerolls"] is True
    assert r["frozen_phase_a_positive_control"]["positive_control_valid"] is True
    assert r["frozen_phase_a_positive_control"]["delta_plus_q95"] == EXPECTED_DELTA
    assert r["primary"]["classification"] == INSUFFICIENT
    assert r["primary"]["no_material_loss"] is False
    assert r["primary"]["gap_M2"] == -0.6777560206049392
    assert all(v is False for v in r["guardrails"].values())

    if sha256(B0 / "generator_authority.json") != EXPECTED_B0_SHA:
        raise RuntimeError("Phase-B0 repository SHA changed")
    b0 = json.loads((B0 / "generator_authority.json").read_text(encoding="utf-8"))

    m = r["measurement"]
    primary = r["primary"]
    sens = r["nonpromoting_tolerance_sensitivity"]
    wmed = m["reliability_W"]["finite"]["median"]
    class_counts = [b0["fit"][str(f)]["descriptor_class_count"] for f in range(5)]
    train_distinct = [b0["fit"][str(f)]["training_distinct_signatures"] for f in range(5)]
    generated_distinct = [c["distinct_signatures"] for c in b0["cases"]]

    report = f"""# Issue #75 Phase B — generic K/R/S occupancy-shape result

Date: 2026-09-01  
Status: **COMPLETE / FIRST-REVEAL AUTHORITY PERMANENTLY FROZEN**

## Primary result

Frozen classification:

`{INSUFFICIENT}`

Generic occupancy geometry — occupied-slot count `K`, contiguous occupied-run count `R`, occupied span `S`, plus slot main effects — is materially insufficient to reproduce the replicated Voynich R1 topology.

## Exact authority

- scientific head: `{EXPECTED_SCI_HEAD}`
- first-reveal run: `{EXPECTED_RUN}` — success
- artifact ID: `{EXPECTED_ARTIFACT_ID}`
- artifact digest: `{EXPECTED_ARTIFACT_DIGEST}`
- complete population: `31/31`
- drops: `0`
- rerolls: `0`
- aggregate SHA-256: `{EXPECTED_AGG_SHA}`
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
| median p_exist | `{fmt(m['p_exist']['median'], 9)}` |
| median sign agreement ZL3b | `{fmt(m['sign_ZL3b']['median'], 3)}/66` |
| median sign agreement IT2a | `{fmt(m['sign_IT2a']['median'], 3)}/66` |
| paired median gap vs frozen M+ center | `{fmt(primary['gap_M2'], 9)}` |
| allowed loss q95 | `-{EXPECTED_DELTA}` |
| no material loss | `false` |

The preregistered sufficiency rule was `gap_M2 >= -{EXPECTED_DELTA}`. Observed `gap_M2={primary['gap_M2']}` is far outside that tolerance.

## What changed from M1

Phase A M1 knew slot main effects and exact occupied-slot count `K`, yet had median topology correlation near `-0.17`. M2 additionally knows whether occupied positions form one or several runs and how wide their span is. That raises median topology correlation to about `0.29`, so coarse geometry contains real information, but most of the empirical-pattern topology remains unexplained.

The important distinction is therefore:

`slot prevalence` — insufficient

`+ occupied count K` — strong dependencies, wrong geometry

`+ coarse run/span geometry` — partial recovery only

`+ compact configuration/state rule` — now required frontier

`empirical complete-signature inventory` — sufficient positive control

## Non-memorization audit

M2 has zero explicit slot-pair interaction parameters and zero complete-signature-specific parameters. It conditions on generic `(K,R,S)` classes and uses slot main effects within class.

Target-blind B0 diagnostics:

- descriptor classes by fold: `{class_counts}`
- training distinct complete signatures by fold: `{train_distinct}`
- generated distinct complete signatures across 31 reps: `{min(generated_distinct)}..{max(generated_distinct)}`

Thus M2 is materially coarser than empirical-signature resampling and is not a disguised replay of the empirical inventory.

## Sensitivity

The primary q95 tolerance remains authoritative. Non-promoting checks agree:

- q90 delta: `{sens['q90_delta_plus']}`; no-material-loss `{str(bool(sens['q90_no_material_loss'])).lower()}`
- q99 delta: `{sens['q99_delta_plus']}`; no-material-loss `{str(bool(sens['q99_no_material_loss'])).lower()}`

## Licensed next frontier

The preregistered rule licenses M3: a separately preregistered compact state/transition occupancy generator may now be tested. M3 must be interpretable as a generator and must not fit selected target edges or optimize the 66-edge target loss.

This license comes from the frozen Phase-B outcome only. The earlier failed Phase-C workflow attempts are not scientific evidence and must not be treated as an M3 result.

## Boundaries

This result concerns the 12-slot occupancy representation only. It does not identify slot meanings, literal token spellings, plaintext, cipher tables, natural-language word boundaries, historical Naibbe use, or decipherment.
"""

    marker = f"""# Issue #75 Phase B — M2 insufficient; M3 licensed

Date: 2026-09-01  
Classification: `{INSUFFICIENT}`

- first-reveal run: `{EXPECTED_RUN}`
- scientific head: `{EXPECTED_SCI_HEAD}`
- artifact ID: `{EXPECTED_ARTIFACT_ID}`
- aggregate SHA-256: `{EXPECTED_AGG_SHA}`
- gap M2: `{primary['gap_M2']}`
- frozen q95 delta: `{EXPECTED_DELTA}`
- no material loss: `false`

A separately preregistered compact state/transition M3 generator is scientifically licensed. No failed Phase-C workflow attempt is promoted to evidence by this marker.
"""

    ledger = f"""# Hypothesis ledger addendum — Issue #75 Phase B

Status: **PHASE B COMPLETE / M3 LICENSED**

## H75-M2 — generic K/R/S occupancy geometry plus slot main effects is sufficient

Prediction: a cross-fitted M2-KRS generator should fall within frozen Phase-A M+ variation if coarse occupancy geometry carries the required R1 information.

Frozen test: 31 target-blind M2 corpora; candidate-owned reference/test calibration; ZL3b and IT2a separate; `T=min(R_ZL3b,R_IT2a)`; paired comparison to frozen M+ center; allowed loss `{EXPECTED_DELTA}`.

Result: **rejected**.

- median T: `{m['T']['median']}`
- median R ZL3b: `{m['R_ZL3b']['median']}`
- median R IT2a: `{m['R_IT2a']['median']}`
- median gap vs M+ center: `{primary['gap_M2']}`
- no material loss: `false`

Interpretation: `(K,R,S)` geometry recovers a nontrivial part of topology but is far from sufficient. A compact state/configuration mechanism beyond coarse geometry is required by the tested hierarchy.

Authority: `experiments/minimal-occupancy-generator/stage-b-first-reveal/phase75b_aggregate.json`, SHA-256 `{EXPECTED_AGG_SHA}`.
"""

    (HERE / "REPORT_B.md").write_text(report, encoding="utf-8")
    (HERE / "DECISION_B_M3_LICENSED.md").write_text(marker, encoding="utf-8")
    (ROOT / "research" / "HYPOTHESIS_LEDGER_ADDENDUM_ISSUE75_PHASE_B.md").write_text(ledger, encoding="utf-8")

    print(json.dumps({
        "classification": INSUFFICIENT,
        "aggregate_sha256": EXPECTED_AGG_SHA,
        "T_median": m["T"]["median"],
        "R_ZL3b_median": m["R_ZL3b"]["median"],
        "R_IT2a_median": m["R_IT2a"]["median"],
        "E_median": m["residual_energy"]["median"],
        "W_median": wmed,
        "gap_M2": primary["gap_M2"],
        "delta_plus_q95": EXPECTED_DELTA,
        "marker": "DECISION_B_M3_LICENSED.md",
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
