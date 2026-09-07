#!/usr/bin/env python3
"""Issue #165: frozen first reveal for section/domain source attribution.

Only Currier regimes licensed by the merged score-free Gate0 are scored. The
scientific model adds a context-invariant section x next-initial outcome bias on
top of the compact Issue #161 Currier outcome model, plus the frozen one-leaf-
left training-label placebo. No section x previous-terminal interaction exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
SOURCE_DIR = HERE.parent
CURRIER_DIR = ROOT / "experiments" / "predictive-information" / "common-eva-currier"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))
if str(CURRIER_DIR) not in sys.path:
    sys.path.insert(0, str(CURRIER_DIR))

import issue165_section_domain_gate0 as G165  # noqa: E402
import issue165_section_domain_gate0_authorityfix as G165F  # noqa: E402
import issue161_outcome_factor_first_reveal as S161  # noqa: E402
import issue161_outcome_factor_gate0 as G161  # noqa: E402

GATE_PROVENANCE_PATH = SOURCE_DIR / "ISSUE165_GATE0_PROVENANCE.md"
PLAN_PATH = SOURCE_DIR / "ISSUE165_SECTION_DOMAIN_TRANSPORT_PLAN.md"
AUTHORITY_FIX_PATH = SOURCE_DIR / "issue165_section_domain_gate0_authorityfix.py"

EXPECTED_GATE_RESULT_SHA256 = "3b6eededdfe197ed9152b9b0f756dffe34870eaf1a33b810d7e23f84d0d84f1a"
EXPECTED_GATE_BLOB = "adaca5dc387d58542044089aac5faaedc8880ccf"
EXPECTED_AUTHORITY_FIX_BLOB = "8ad582bdea2351606e97e52c0ee733999c11820f"
EXPECTED_GATE_PROVENANCE_BLOB = "15627264ce598c315810458a64482e8f60d9afeb"
EXPECTED_PLAN_BLOB = "d334092e6c7cd38f76deb48250fa09d8f9468064"
EXPECTED_GATE_MERGE = "389043ad2cc55eb15760ed3504fd03fc01253eb9"
EXPECTED_ISSUE161_SCORER_BLOB = "d24149977770118505f2147c5aa2bb727631906f"
EXPECTED_ISSUE161_RESULT_SHA256 = "11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031"
EXPECTED_PURE_I_SHA256 = "47ab536c6806eca5b037bc8cf81bae11069a153c92e4d17162c6381c92025eb1"
EXPECTED_SCORABLE = ("B",)
EXPECTED_ELIGIBLE = {"A": ("H",), "B": ("B", "S")}

READINGS = ("ZL3b", "IT2a")
REGIMES = ("A", "B")
N_FOLDS = 5
LN2 = math.log(2.0)
ALPHA = Fraction(1, 100)
V = 32
TOL = 1e-12

VALID_CLASSES = (
    "SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER A AND B",
    "SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER A ONLY",
    "SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER B ONLY",
    "NO ROBUST SECTION/DOMAIN OUTCOME INFORMATION",
    "INVALID SECTION/DOMAIN SOURCE ATTRIBUTION",
)

C145 = S161.C145


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G161.git_blob(path)


def verify_gate_authority(zl_path: Path, it_path: Path) -> dict:
    pins = (
        (G165.HERE, EXPECTED_GATE_BLOB, "Issue165 original Gate"),
        (AUTHORITY_FIX_PATH, EXPECTED_AUTHORITY_FIX_BLOB, "Issue165 authority-fix wrapper"),
        (GATE_PROVENANCE_PATH, EXPECTED_GATE_PROVENANCE_BLOB, "Issue165 Gate provenance"),
        (PLAN_PATH, EXPECTED_PLAN_BLOB, "Issue165 plan"),
        (S161.HERE, EXPECTED_ISSUE161_SCORER_BLOB, "Issue161 scorer"),
    )
    for path, expected, label in pins:
        actual = git_blob(path)
        if actual != expected:
            raise RuntimeError(f"{label} blob changed: {actual}")

    gate = G165F.run_gate(zl_path, it_path)
    gate_sha = sha256_obj(gate)
    if gate_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Issue165 Gate result SHA changed: {gate_sha}")
    if gate.get("gate_pass") is not True:
        raise RuntimeError("Issue165 Gate no longer passes")
    if gate.get("scientific_section_metrics_computed") is not False:
        raise RuntimeError("Issue165 Gate firewall changed")
    if tuple(gate["scorable_currier_regimes"]) != EXPECTED_SCORABLE:
        raise RuntimeError("Issue165 scorable-regime authority changed")
    for regime in REGIMES:
        got = tuple(gate["eligibility"][regime]["eligible_sections"])
        if got != EXPECTED_ELIGIBLE[regime]:
            raise RuntimeError(f"Issue165 eligible sections changed for {regime}: {got}")
    if gate["metadata_authority"]["pure_I_leaf_map_sha256"] != EXPECTED_PURE_I_SHA256:
        raise RuntimeError("Issue165 pure-I map changed")
    if gate["scribe_identifiability"]["classification"] != "SCRIBE_NOT_IDENTIFIABLE":
        raise RuntimeError("Issue165 scribe identifiability changed")
    return gate


def pure_i_from_gate(gate: dict) -> dict[int, str]:
    return {int(leaf): str(section) for leaf, section in gate["metadata_authority"]["pure_I_leaf_map"]}


def parse_currier_multiplier(gate161: dict, fold: int, regime: str) -> dict[str, Fraction]:
    return S161.parse_vector(gate161["outer"][fold][f"W_{regime}"])


def reading_counts(runs, leaf_currier, pure_i, eligible, outer_fold: int, placebo=None):
    counts = {s: defaultdict(int) for s in eligible}
    for fold, leaf, _loc, _line_no, run in runs:
        if int(fold) == outer_fold:
            continue
        leaf = int(leaf)
        if leaf_currier.get(leaf) != "B":
            continue
        actual = pure_i.get(leaf)
        if actual not in eligible:
            continue
        section = placebo.get(leaf, actual) if placebo is not None else actual
        if section not in eligible:
            raise RuntimeError("placebo assigned an ineligible section")
        for ti, record in enumerate(run):
            if ti == 0:
                continue
            syms = C145.token_symbols(record["atoms"])
            counts[section][syms[0]] += 1
    return counts


def combine_readings(z_counts, i_counts, eligible):
    out = {s: {y: Fraction(0, 1) for y in G161.OUTCOMES} for s in eligible}
    for s in eligible:
        for y in G161.OUTCOMES:
            out[s][y] = Fraction(int(z_counts[s].get(y, 0)), 2) + Fraction(
                int(i_counts[s].get(y, 0)), 2
            )
    return out


def build_section_multipliers(shared_counts, eligible):
    aggregate = {y: sum((shared_counts[s][y] for s in eligible), Fraction(0, 1)) for y in G161.OUTCOMES}
    m_r = sum(aggregate.values(), Fraction(0, 1))
    if m_r <= 0:
        raise RuntimeError("empty Currier eligible-section training aggregate")
    q_r = {y: (aggregate[y] + ALPHA) / (m_r + ALPHA * V) for y in G161.OUTCOMES}

    multipliers = {}
    audit = {}
    for s in eligible:
        m_s = sum(shared_counts[s].values(), Fraction(0, 1))
        if m_s <= 0:
            raise RuntimeError(f"empty section training aggregate: {s}")
        q_s = {y: (shared_counts[s][y] + ALPHA) / (m_s + ALPHA * V) for y in G161.OUTCOMES}
        w = {y: q_s[y] / q_r[y] for y in G161.OUTCOMES}
        rows = [[y, w[y].numerator, w[y].denominator] for y in G161.OUTCOMES]
        multipliers[s] = w
        audit[s] = {
            "shared_training_mass": [m_s.numerator, m_s.denominator],
            "multiplier_rational": rows,
            "multiplier_sha256": sha256_obj(rows),
        }
    aggregate_rows = [[y, aggregate[y].numerator, aggregate[y].denominator] for y in G161.OUTCOMES]
    return multipliers, {
        "currier_eligible_union_mass": [m_r.numerator, m_r.denominator],
        "currier_eligible_union_counts_sha256": sha256_obj(aggregate_rows),
        "sections": audit,
    }


def multiply_and_normalize(base: Mapping[str, Fraction], multiplier: Mapping[str, Fraction]):
    raw = {y: base[y] * multiplier[y] for y in G161.OUTCOMES}
    total = sum(raw.values(), Fraction(0, 1))
    if total <= 0:
        raise RuntimeError("nonpositive section conditional normalizer")
    probs = {y: raw[y] / total for y in G161.OUTCOMES}
    if sum(probs.values(), Fraction(0, 1)) != 1:
        raise RuntimeError("section conditional failed exact normalization")
    return probs


def section_token_logp(
    target_model: C145.CommonEdgeModel,
    pool_table: Mapping[str, Mapping[str, Fraction]],
    currier_multiplier: Mapping[str, Fraction],
    section_multiplier: Mapping[str, Fraction],
    syms: Sequence[str],
    previous_terminal: str,
) -> float:
    syms = list(syms)
    if len(syms) < 2:
        raise RuntimeError("invalid common-EVA token")
    first, second = syms[0], syms[1]
    if previous_terminal in pool_table:
        base = G161.normalized_outcome_conditional(pool_table, previous_terminal, currier_multiplier)
        probs = multiply_and_normalize(base, section_multiplier)
        p = probs[first]
        if p <= 0:
            raise RuntimeError("nonpositive section probability")
        ll = math.log(float(p))
    else:
        ll = -math.log(float(C145.V))
    ll += target_model.categorical_logp(target_model.body_second[first], second)
    for j in range(2, len(syms)):
        ll += target_model.run_model.logp(syms[j - 2 : j], syms[j])
    return float(ll)


def placebo_map_for_fold(gate: dict, fold: int, regime: str) -> dict[int, str]:
    entry = gate["placebo_outer"][fold]["regimes"][regime]
    if entry["scorable"] is not True:
        raise RuntimeError(f"{regime} fold {fold} placebo unexpectedly unscorable")
    mapping = {int(leaf): str(new) for leaf, _old, new in entry["mapping"]}
    if int(entry["changed_leaves"]) <= 0:
        raise RuntimeError("frozen placebo became degenerate")
    return mapping


def score_reading_regime(reading: str, regime: str, all_runs, gate: dict, gate161: dict, gate155: dict) -> dict:
    if regime not in gate["scorable_currier_regimes"]:
        return {
            "reading": reading,
            "regime": regime,
            "status": "UNSCORABLE_BY_FROZEN_SUPPORT",
            "eligible_sections": gate["eligibility"][regime]["eligible_sections"],
        }
    if regime != "B":
        raise RuntimeError("current frozen authority unexpectedly licenses a non-B regime")

    pure_i = pure_i_from_gate(gate)
    leaf_currier = S161.S155.leaf_currier_from_gate(gate155)
    eligible = tuple(gate["eligibility"][regime]["eligible_sections"])
    regime_runs = S161.S155.filter_runs(all_runs[reading], leaf_currier, regime)
    outer = []

    for f in range(N_FOLDS):
        target_model = C145.CommonEdgeModel(regime_runs, set(range(N_FOLDS)) - {f})
        g161 = gate161["outer"][f]
        g155 = gate155["outer"][f]
        matched = g155["matched_currier_tables"]
        a = G161.parse_rational_table(matched["A_matched_sparse_rational_counts"])
        b = G161.parse_rational_table(matched["B_matched_sparse_rational_counts"])
        pool, pool_summary = G161.G158.pool_tables(a, b)
        if pool_summary["pooled_sparse_rational_table_sha256"] != g161["POOL_table_sha256"]:
            raise RuntimeError(f"fold {f} pooled-table identity changed")
        currier_w = parse_currier_multiplier(gate161, f, regime)

        pmap = placebo_map_for_fold(gate, f, regime)
        z_actual = reading_counts(all_runs["ZL3b"], leaf_currier, pure_i, eligible, f)
        i_actual = reading_counts(all_runs["IT2a"], leaf_currier, pure_i, eligible, f)
        z_placebo = reading_counts(all_runs["ZL3b"], leaf_currier, pure_i, eligible, f, pmap)
        i_placebo = reading_counts(all_runs["IT2a"], leaf_currier, pure_i, eligible, f, pmap)
        actual_shared = combine_readings(z_actual, i_actual, eligible)
        placebo_shared = combine_readings(z_placebo, i_placebo, eligible)
        actual_w, actual_audit = build_section_multipliers(actual_shared, eligible)
        placebo_w, placebo_audit = build_section_multipliers(placebo_shared, eligible)

        if actual_audit["currier_eligible_union_counts_sha256"] != placebo_audit["currier_eligible_union_counts_sha256"]:
            raise RuntimeError(f"fold {f} placebo changed Currier union counts")

        log_currier = []
        log_section = []
        log_placebo = []
        by_section = {s: 0 for s in eligible}
        supported = 0
        unsupported = 0

        for fold, leaf, _loc, _line_no, run in regime_runs:
            if int(fold) != f:
                continue
            leaf = int(leaf)
            section = pure_i.get(leaf)
            if section not in eligible:
                continue
            previous_terminal = None
            for ti, record in enumerate(run):
                syms = C145.token_symbols(record["atoms"])
                if ti > 0 and record["slotparser_accepted"]:
                    if previous_terminal is None:
                        raise RuntimeError("BODY target lacks previous terminal")
                    lp_currier = S161.outcome_token_logp(
                        target_model, pool, currier_w, syms, False, previous_terminal
                    )
                    lp_section = section_token_logp(
                        target_model, pool, currier_w, actual_w[section], syms, previous_terminal
                    )
                    lp_placebo = section_token_logp(
                        target_model, pool, currier_w, placebo_w[section], syms, previous_terminal
                    )
                    log_currier.append(lp_currier)
                    log_section.append(lp_section)
                    log_placebo.append(lp_placebo)
                    by_section[section] += 1
                    if previous_terminal in pool:
                        supported += 1
                    else:
                        unsupported += 1
                previous_terminal = syms[-2]

        expected_by_section = {
            s: int(gate["section_support"][reading][regime][s][str(f)]) for s in eligible
        }
        if by_section != expected_by_section:
            raise RuntimeError(
                f"{reading}/{regime}/fold{f} target section support changed: {by_section} != {expected_by_section}"
            )
        n = sum(by_section.values())
        if n <= 0 or not (len(log_currier) == len(log_section) == len(log_placebo) == n):
            raise RuntimeError(f"{reading}/{regime}/fold{f} score alignment failure")
        if not all(math.isfinite(v) for v in log_currier + log_section + log_placebo):
            raise RuntimeError(f"{reading}/{regime}/fold{f} non-finite score")

        bits_currier = float(-sum(log_currier) / (n * LN2))
        bits_section = float(-sum(log_section) / (n * LN2))
        bits_placebo = float(-sum(log_placebo) / (n * LN2))
        g_section = float(bits_currier - bits_section)
        g_placebo = float(bits_placebo - bits_section)

        outer.append(
            {
                "fold": f,
                "reading": reading,
                "regime": regime,
                "eligible_sections": list(eligible),
                "n_scored_primary_run_body_targets": n,
                "targets_by_section": by_section,
                "matched_context_supported_targets": supported,
                "matched_context_unsupported_targets": unsupported,
                "matched_context_coverage_fraction": float(supported / n),
                "bits_EDGE_CURRIER": bits_currier,
                "bits_EDGE_SECTION": bits_section,
                "bits_EDGE_SECTION_SHUFFLED": bits_placebo,
                "G_section": g_section,
                "G_placebo": g_placebo,
                "actual_training": actual_audit,
                "placebo_training": placebo_audit,
                "placebo_mapping_sha256": gate["placebo_outer"][f]["regimes"][regime]["mapping_sha256"],
                "currier_multiplier_sha256": g161[f"W_{regime}_sha256"],
                "POOL_table_sha256": g161["POOL_table_sha256"],
            }
        )

    gs = [float(r["G_section"]) for r in outer]
    gp = [float(r["G_placebo"]) for r in outer]
    mean_gs = float(sum(gs) / N_FOLDS)
    mean_gp = float(sum(gp) / N_FOLDS)
    pos_gs = int(sum(v > 0 for v in gs))
    pos_gp = int(sum(v > 0 for v in gp))
    passed = bool(mean_gs > 0 and pos_gs >= 4 and mean_gp > 0 and pos_gp >= 4)
    return {
        "reading": reading,
        "regime": regime,
        "status": "SCORED",
        "eligible_sections": list(eligible),
        "outer": outer,
        "primary": {
            "G_section_by_fold": gs,
            "mean_G_section": mean_gs,
            "positive_G_section_folds": pos_gs,
            "G_placebo_by_fold": gp,
            "mean_G_placebo": mean_gp,
            "positive_G_placebo_folds": pos_gp,
            "required_positive_folds": 4,
            "pass_within_reading_regime": passed,
        },
    }


def frozen_class(cells: Mapping[str, Mapping[str, dict]], scorable: Sequence[str]) -> tuple[str, dict]:
    robust = {r: False for r in REGIMES}
    for regime in scorable:
        robust[regime] = bool(
            cells["ZL3b"][regime]["primary"]["pass_within_reading_regime"]
            and cells["IT2a"][regime]["primary"]["pass_within_reading_regime"]
        )
    if robust["A"] and robust["B"]:
        cls = "SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER A AND B"
    elif robust["A"]:
        cls = "SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER A ONLY"
    elif robust["B"]:
        cls = "SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER B ONLY"
    else:
        cls = "NO ROBUST SECTION/DOMAIN OUTCOME INFORMATION"
    return cls, {
        "Currier_A_robust_section_information": robust["A"],
        "Currier_B_robust_section_information": robust["B"],
    }


def score(zl_path: Path, it_path: Path) -> dict:
    gate = verify_gate_authority(zl_path, it_path)
    gate161, gate155 = S161.verify_gate_authority(zl_path, it_path)
    _leaf_currier, _leaf_fold, all_runs = G165.load_common_runs(zl_path, it_path, gate155)
    if gate161["entry_authority"]["fold_identity_sha256"] != G165.EXPECTED["fold_sha256"]:
        raise RuntimeError("fold authority changed")

    cells = {
        reading: {
            regime: score_reading_regime(reading, regime, all_runs, gate, gate161, gate155)
            for regime in REGIMES
        }
        for reading in READINGS
    }
    classification, robust = frozen_class(cells, gate["scorable_currier_regimes"])
    if classification not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")

    return {
        "schema": "issue165-section-domain-first-reveal-v1",
        "issue": 165,
        "phase": "SECTION_DOMAIN_SOURCE_ATTRIBUTION_FIRST_REVEAL",
        "scored": True,
        "classification": classification,
        "authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": EXPECTED_GATE_RESULT_SHA256,
            "gate0_original_script_blob": EXPECTED_GATE_BLOB,
            "gate0_authority_fix_blob": EXPECTED_AUTHORITY_FIX_BLOB,
            "gate0_provenance_blob": EXPECTED_GATE_PROVENANCE_BLOB,
            "plan_blob": EXPECTED_PLAN_BLOB,
            "gate0_merge": EXPECTED_GATE_MERGE,
            "issue161_scorer_blob": EXPECTED_ISSUE161_SCORER_BLOB,
            "issue161_declared_result_sha256": EXPECTED_ISSUE161_RESULT_SHA256,
            "fold_identity_sha256": gate["entry_authority"]["fold_identity_sha256"],
            "pure_I_leaf_map_sha256": gate["metadata_authority"]["pure_I_leaf_map_sha256"],
            "scribe_identifiability": gate["scribe_identifiability"]["classification"],
        },
        "frozen_model": {
            "base": "Issue161 shared terminal->initial table + Currier-specific global next-initial bias",
            "section_factor": "reading-shared context-invariant section x next-initial outcome multiplier",
            "reading_pool": "0.5*ZL3b + 0.5*IT2a all-clean-BODY training counts",
            "section_multiplier": "smoothed section outcome probability / smoothed Currier eligible-union outcome probability",
            "alpha": 0.01,
            "V": 32,
            "placebo": "frozen one-leaf-left cyclic training-label rotation",
            "unsupported_exact_context": "unchanged Issue161 empty-additive 1/32",
            "section_by_previous_terminal_interaction": False,
            "target_native_fallback": False,
        },
        "scorable_currier_regimes": list(gate["scorable_currier_regimes"]),
        "cells": cells,
        "primary_joint": {**robust, "classification": classification},
        "firewall": {
            "post_reveal_section_or_leaf_selection": False,
            "post_reveal_multiplier_change": False,
            "post_reveal_currier_or_fold_change": False,
            "post_reveal_placebo_search_or_repeat": False,
            "mixed_or_unresolved_leaf_scored": False,
            "scribe_model_fitted": False,
            "section_by_previous_terminal_interaction_added": False,
            "alpha_temperature_interpolation_fallback_or_mixture_tuned": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "semantic_image_cipher_historical_inference": False,
        },
    }


def self_test() -> dict:
    outcomes = list(G161.OUTCOMES)
    fake = {
        "B": {y: Fraction(0, 1) for y in outcomes},
        "S": {y: Fraction(0, 1) for y in outcomes},
    }
    fake["B"][outcomes[0]] = Fraction(8, 1)
    fake["B"][outcomes[1]] = Fraction(2, 1)
    fake["S"][outcomes[0]] = Fraction(2, 1)
    fake["S"][outcomes[1]] = Fraction(8, 1)
    w, audit = build_section_multipliers(fake, ("B", "S"))
    if not (w["B"][outcomes[0]] > 1 and w["B"][outcomes[1]] < 1):
        raise AssertionError("synthetic section multiplier failed")
    base = {y: Fraction(1, V) for y in outcomes}
    probs = multiply_and_normalize(base, w["B"])
    if sum(probs.values(), Fraction(0, 1)) != 1:
        raise AssertionError("synthetic section normalization failed")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "real_target_section_scores_computed": False,
        "reading_shared_half_plus_half": True,
        "unequal_section_mass_normalized_before_multiplier": True,
        "section_conditional_exactly_normalized": True,
        "section_by_previous_terminal_interaction": False,
        "audit": audit,
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue165-section-domain-first-reveal-v1",
        "issue": 165,
        "phase": "SECTION_DOMAIN_SOURCE_ATTRIBUTION_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID SECTION/DOMAIN SOURCE ATTRIBUTION",
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {
            "post_failure_scientific_repair_allowed": False,
            "post_failure_target_driven_change_allowed": False,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--run", nargs=3, metavar=("ZL3B", "IT2A", "OUT_JSON"))
    ns = ap.parse_args(argv)
    if ns.self_test:
        print(canonical_json(self_test()), end="")
        return 0
    zl_path = Path(ns.run[0]).resolve()
    it_path = Path(ns.run[1]).resolve()
    out_path = Path(ns.run[2]).resolve()
    try:
        result = score(zl_path, it_path)
        rc = 0
    except Exception as exc:
        result = invalid_result(exc)
        rc = 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
