#!/usr/bin/env python3
"""Issue #167 Gate0: score-free sparse Currier outcome-bias audit.

Reproduce the frozen Issue #161 authority, rank the fixed 32 next-initial
outcomes from training-only A/B matched counts, and construct the preregistered
K={1,2,4,8,16} sparse Currier multiplier family. No held-out sparse target
probability, likelihood, G_sparse, G_missing, or scientific classification is
computed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
CURRIER_DIR = HERE.parent
if str(CURRIER_DIR) not in sys.path:
    sys.path.insert(0, str(CURRIER_DIR))

import issue161_outcome_factor_gate0 as G161  # noqa: E402
import issue161_outcome_factor_first_reveal as S161  # noqa: E402

PLAN_PATH = CURRIER_DIR / "ISSUE167_SPARSE_CURRIER_OUTCOME_PLAN.md"
ISSUE161_GATE_PROVENANCE_PATH = CURRIER_DIR / "ISSUE161_GATE0_PROVENANCE.md"
ISSUE161_FIRST_PROVENANCE_PATH = CURRIER_DIR / "ISSUE161_FIRST_REVEAL_PROVENANCE.md"

EXPECTED = {
    "issue161_gate_result_sha256": "32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94",
    "issue161_gate_script_blob": "00e5bddc0484b9472bb4fce9dadb89dd52bf578f",
    "issue161_gate_provenance_blob": "67e91ba26a76898f679a5182828ab3e9f512d49a",
    "issue161_scorer_blob": "d24149977770118505f2147c5aa2bb727631906f",
    "issue161_first_provenance_blob": "73100548fef5dbc0d08a1951e3c0ca5b370cd6f4",
    "issue161_first_result_sha256": "11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031",
    "issue161_gate_merge": "6192e5cbe0a5212d089f890ca26bb7d9a10eedbf",
    "issue161_science_merge": "72ff98da2eac4b830dd02eae7623577362c29150",
    "issue167_plan_blob": "d5b79c64ffc8297672f2de39f6478156ee3442b7",
    "fold_sha256": "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b",
    "n_folds": 5,
    "alpha_num": 1,
    "alpha_den": 100,
    "V": 32,
}

READINGS = ("ZL3b", "IT2a")
REGIMES = ("A", "B")
KS = (1, 2, 4, 8, 16)
OUTCOMES = tuple(G161.OUTCOMES)


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    return G161.git_blob(path)


def parse_vector(rows: Sequence[Sequence[object]]) -> dict[str, Fraction]:
    out: dict[str, Fraction] = {}
    for row in rows:
        if len(row) != 3:
            raise RuntimeError("malformed rational vector row")
        y, num, den = row
        y = str(y)
        if y in out:
            raise RuntimeError(f"duplicate vector outcome: {y!r}")
        out[y] = Fraction(int(num), int(den))
    if tuple(out) != OUTCOMES:
        raise RuntimeError("rational vector outcome order changed")
    return out


def fraction_decimal(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def probability_vector(agg: Mapping[str, Fraction], total: Fraction) -> dict[str, Fraction]:
    alpha = Fraction(EXPECTED["alpha_num"], EXPECTED["alpha_den"])
    denom = total + alpha * EXPECTED["V"]
    if denom <= 0:
        raise RuntimeError("nonpositive aggregate smoothing denominator")
    q = {y: (agg[y] + alpha) / denom for y in OUTCOMES}
    if sum(q.values(), Fraction(0, 1)) != Fraction(1, 1):
        raise RuntimeError("smoothed aggregate outcome vector failed exact normalization")
    if any(v <= 0 for v in q.values()):
        raise RuntimeError("nonpositive smoothed aggregate outcome probability")
    return q


def jeffreys_ranking(q_a: Mapping[str, Fraction], q_b: Mapping[str, Fraction]) -> tuple[list[str], dict[str, str], dict]:
    j: dict[str, Decimal] = {}
    with localcontext() as ctx:
        ctx.prec = 80
        for y in OUTCOMES:
            qa = fraction_decimal(q_a[y])
            qb = fraction_decimal(q_b[y])
            if qa <= 0 or qb <= 0:
                raise RuntimeError("Jeffreys ranking received nonpositive probability")
            value = (qa - qb) * (qa / qb).ln()
            if value < Decimal("-1e-70"):
                raise RuntimeError(f"negative Jeffreys contribution for {y!r}: {value}")
            if value < 0:
                value = Decimal(0)
            j[y] = +value

    vocab_index = {y: i for i, y in enumerate(OUTCOMES)}
    ranking = sorted(OUTCOMES, key=lambda y: (-j[y], vocab_index[y]))
    if len(ranking) != EXPECTED["V"] or set(ranking) != set(OUTCOMES):
        raise RuntimeError("Jeffreys ranking is not a permutation of the frozen vocabulary")

    tie_groups = []
    start = 0
    while start < len(ranking):
        end = start + 1
        while end < len(ranking) and j[ranking[end]] == j[ranking[start]]:
            end += 1
        if end - start > 1:
            group = ranking[start:end]
            expected_group = sorted(group, key=lambda y: vocab_index[y])
            if group != expected_group:
                raise RuntimeError("Jeffreys exact tie did not follow frozen vocabulary order")
            tie_groups.append(group)
        start = end

    j_text = {y: format(j[y], "f") for y in OUTCOMES}
    return ranking, j_text, {
        "exact_tie_groups_in_rank_order": tie_groups,
        "tie_break": "frozen Issue161 outcome-vocabulary order",
        "decimal_precision": 80,
        "all_J_nonnegative": True,
    }


def sparse_multiplier(full: Mapping[str, Fraction], selected: set[str]) -> dict[str, Fraction]:
    out = {y: (full[y] if y in selected else Fraction(1, 1)) for y in OUTCOMES}
    if any(v <= 0 for v in out.values()):
        raise RuntimeError("nonpositive sparse multiplier")
    for y in OUTCOMES:
        if y not in selected and out[y] != Fraction(1, 1):
            raise RuntimeError("excluded outcome retained a non-unit multiplier")
    return out


def rational_vector(vec: Mapping[str, Fraction]) -> list[list[object]]:
    return [[y, vec[y].numerator, vec[y].denominator] for y in OUTCOMES]


def verify_entry_authority(zl_path: Path, it_path: Path) -> tuple[dict, dict, dict]:
    if len(OUTCOMES) != EXPECTED["V"] or len(set(OUTCOMES)) != EXPECTED["V"]:
        raise RuntimeError("frozen 32-outcome vocabulary identity failed")

    pins = (
        (G161.HERE, EXPECTED["issue161_gate_script_blob"], "Issue161 Gate script"),
        (ISSUE161_GATE_PROVENANCE_PATH, EXPECTED["issue161_gate_provenance_blob"], "Issue161 Gate provenance"),
        (S161.HERE, EXPECTED["issue161_scorer_blob"], "Issue161 scientific scorer"),
        (ISSUE161_FIRST_PROVENANCE_PATH, EXPECTED["issue161_first_provenance_blob"], "Issue161 first-reveal provenance"),
        (PLAN_PATH, EXPECTED["issue167_plan_blob"], "Issue167 plan"),
    )
    for path, expected, label in pins:
        actual = git_blob(path)
        if actual != expected:
            raise RuntimeError(f"{label} blob changed: {actual}")

    first_text = ISSUE161_FIRST_PROVENANCE_PATH.read_text(encoding="utf-8")
    if EXPECTED["issue161_first_result_sha256"] not in first_text:
        raise RuntimeError("Issue161 first-reveal result identity missing from frozen provenance")
    if "NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL" not in first_text:
        raise RuntimeError("Issue161 frozen classification missing from provenance")

    gate161 = G161.run_gate(zl_path, it_path)
    gate161_sha = sha256_obj(gate161)
    if gate161_sha != EXPECTED["issue161_gate_result_sha256"]:
        raise RuntimeError(f"Issue161 Gate result SHA changed: {gate161_sha}")
    if gate161.get("gate_pass") is not True:
        raise RuntimeError("Issue161 Gate no longer passes")
    if gate161.get("scientific_outcome_factor_metrics_computed") is not False:
        raise RuntimeError("Issue161 Gate firewall changed")
    if gate161["entry_authority"]["fold_identity_sha256"] != EXPECTED["fold_sha256"]:
        raise RuntimeError("physical-leaf fold authority changed")

    gate158, _gate158_sha, gate155 = G161.verify_entry_authority(zl_path, it_path)
    return gate161, gate158, gate155


def synthetic_test() -> dict:
    y0, y1 = OUTCOMES[0], OUTCOMES[1]
    pool = {
        "c1": {y0: Fraction(2, 1), y1: Fraction(2, 1)},
        "c2": {y0: Fraction(2, 1), y1: Fraction(2, 1)},
    }
    full = {y: Fraction(1, 1) for y in OUTCOMES}
    full[y0] = Fraction(2, 1)
    full[y1] = Fraction(1, 2)
    sparse = sparse_multiplier(full, {y0})
    if sparse[y0] != Fraction(2, 1) or sparse[y1] != Fraction(1, 1):
        raise AssertionError("synthetic sparse include/exclude rule failed")
    p1 = G161.normalized_outcome_conditional(pool, "c1", sparse)
    p2 = G161.normalized_outcome_conditional(pool, "c2", sparse)
    base = G161.normalized_outcome_conditional(pool, "c1", {y: Fraction(1, 1) for y in OUTCOMES})
    if not p1[y0] > base[y0]:
        raise AssertionError("selected synthetic global shift was not represented")
    if p1 != p2:
        raise AssertionError("context-invariant sparse multiplier created synthetic context interaction")
    return {
        "ok": True,
        "uses_real_target_data": False,
        "selected_global_shift_represented": True,
        "excluded_outcome_multiplier_fixed_to_one": True,
        "previous_terminal_interaction_introduced": False,
        "fixed_K_ladder": list(KS),
        "V": EXPECTED["V"],
    }


def run_gate(zl_path: Path, it_path: Path) -> dict:
    gate161, gate158, gate155 = verify_entry_authority(zl_path, it_path)
    outer = []

    for f in range(EXPECTED["n_folds"]):
        r161 = gate161["outer"][f]
        r158 = gate158["outer"][f]
        r155 = gate155["outer"][f]
        if not (int(r161["outer_fold"]) == int(r158["outer_fold"]) == int(r155["outer_fold"]) == f):
            raise RuntimeError("outer fold order changed")
        if r161["training_union_heldout_overlap"] != [] or r158["training_union_heldout_overlap"] != []:
            raise RuntimeError("held-out physical-leaf leakage reappeared")

        matched = r155["matched_currier_tables"]
        a = G161.parse_rational_table(matched["A_matched_sparse_rational_counts"])
        b = G161.parse_rational_table(matched["B_matched_sparse_rational_counts"])
        pool_sparse = r158["pooled_table"]["pooled_sparse_rational_counts"]
        pool = G161.parse_rational_table(pool_sparse)
        if set(a) != set(b) or set(a) != set(pool):
            raise RuntimeError(f"fold {f} retained context sets differ")
        if matched["A_matched_sparse_rational_table_sha256"] != r161["A_matched_table_sha256"]:
            raise RuntimeError(f"fold {f} A matched-table identity changed")
        if matched["B_matched_sparse_rational_table_sha256"] != r161["B_matched_table_sha256"]:
            raise RuntimeError(f"fold {f} B matched-table identity changed")
        if r158["pooled_table"]["pooled_sparse_rational_table_sha256"] != r161["POOL_table_sha256"]:
            raise RuntimeError(f"fold {f} pooled-table identity changed")

        agg_a = G161.aggregate_outcomes(a)
        agg_b = G161.aggregate_outcomes(b)
        agg_pool = G161.aggregate_outcomes(pool)
        total_a = sum(agg_a.values(), Fraction(0, 1))
        total_b = sum(agg_b.values(), Fraction(0, 1))
        total_pool = sum(agg_pool.values(), Fraction(0, 1))
        if not (total_a == total_b == total_pool and total_pool > 0):
            raise RuntimeError(f"fold {f} exact A/B/POOL aggregate mass equality failed")
        for y in OUTCOMES:
            if agg_pool[y] != (agg_a[y] + agg_b[y]) / 2:
                raise RuntimeError(f"fold {f} pooled aggregate identity failed for {y!r}")

        full_a = G161.build_multiplier(agg_a, agg_pool)
        full_b = G161.build_multiplier(agg_b, agg_pool)
        if sha256_obj(rational_vector(full_a)) != r161["W_A_sha256"]:
            raise RuntimeError(f"fold {f} full W_A identity changed")
        if sha256_obj(rational_vector(full_b)) != r161["W_B_sha256"]:
            raise RuntimeError(f"fold {f} full W_B identity changed")

        q_a = probability_vector(agg_a, total_a)
        q_b = probability_vector(agg_b, total_b)
        ranking, j_text, tie_audit = jeffreys_ranking(q_a, q_b)
        sets = {k: ranking[:k] for k in KS}
        for prev, cur in zip(KS, KS[1:]):
            if not set(sets[prev]) < set(sets[cur]):
                raise RuntimeError(f"fold {f} sparse support nesting failed: K={prev}->{cur}")

        sparse_models = {}
        for k in KS:
            selected = set(sets[k])
            sparse_models[str(k)] = {
                "selected_outcomes": sets[k],
                "selected_outcomes_sha256": sha256_obj(sets[k]),
                "regimes": {},
            }
            for regime, full in (("A", full_a), ("B", full_b)):
                w = sparse_multiplier(full, selected)
                vec = rational_vector(w)
                cond_sha, audit = G161.conditional_identity(pool, w)
                if audit["all_contexts_exactly_normalized"] is not True:
                    raise RuntimeError(f"fold {f} K={k} {regime} conditional normalization failed")
                sparse_models[str(k)]["regimes"][regime] = {
                    "sparse_multiplier_sha256": sha256_obj(vec),
                    "conditional_sha256": cond_sha,
                    "conditional_audit": audit,
                    "nonunit_multiplier_outcomes": [y for y in OUTCOMES if w[y] != Fraction(1, 1)],
                }

        target_support = r161["target_context_support"]
        for reading in READINGS:
            for regime in REGIMES:
                t = target_support[reading][regime]
                if int(t["target_primary_run_body_targets"]) < 300:
                    raise RuntimeError(f"{reading}/{regime}/fold{f} target BODY support changed")
                if int(t["matched_context_supported_primary_run_body_targets"]) < 300:
                    raise RuntimeError(f"{reading}/{regime}/fold{f} matched support changed")
                if t["heldout_current_first_atom_used_for_context_selection"] is not False:
                    raise RuntimeError("held-out current outcome entered support selection")

        q_a_vec = rational_vector(q_a)
        q_b_vec = rational_vector(q_b)
        outer.append(
            {
                "outer_fold": f,
                "heldout_physical_leaves": r161["heldout_physical_leaves"],
                "training_union_heldout_overlap": [],
                "A_matched_table_sha256": r161["A_matched_table_sha256"],
                "B_matched_table_sha256": r161["B_matched_table_sha256"],
                "POOL_table_sha256": r161["POOL_table_sha256"],
                "aggregate_total_mass": [total_pool.numerator, total_pool.denominator],
                "full_W_A_sha256": r161["W_A_sha256"],
                "full_W_B_sha256": r161["W_B_sha256"],
                "q_A": q_a_vec,
                "q_B": q_b_vec,
                "q_A_sha256": sha256_obj(q_a_vec),
                "q_B_sha256": sha256_obj(q_b_vec),
                "Jeffreys_contribution_by_outcome": [[y, j_text[y]] for y in OUTCOMES],
                "Jeffreys_ranking": ranking,
                "Jeffreys_ranking_sha256": sha256_obj(ranking),
                "ranking_audit": tie_audit,
                "topK": sparse_models,
                "target_context_support": target_support,
            }
        )

    synthetic = synthetic_test()
    return {
        "schema": "issue167-sparse-currier-outcome-gate0-v1",
        "issue": 167,
        "phase": "SPARSE_CURRIER_OUTCOME_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED SPARSE CURRIER SCORER",
        "scientific_sparse_metrics_computed": False,
        "entry_authority": {
            "issue161_gate_reproduced": True,
            "issue161_gate_result_sha256": EXPECTED["issue161_gate_result_sha256"],
            "issue161_gate_script_blob": EXPECTED["issue161_gate_script_blob"],
            "issue161_gate_provenance_blob": EXPECTED["issue161_gate_provenance_blob"],
            "issue161_scorer_blob": EXPECTED["issue161_scorer_blob"],
            "issue161_first_provenance_blob": EXPECTED["issue161_first_provenance_blob"],
            "issue161_declared_first_reveal_result_sha256": EXPECTED["issue161_first_result_sha256"],
            "issue161_gate_merge": EXPECTED["issue161_gate_merge"],
            "issue161_science_merge": EXPECTED["issue161_science_merge"],
            "fold_identity_sha256": EXPECTED["fold_sha256"],
            "issue167_plan_blob_sha1": git_blob(PLAN_PATH),
        },
        "frozen_sparse_family": {
            "outcomes": list(OUTCOMES),
            "V": EXPECTED["V"],
            "alpha": [EXPECTED["alpha_num"], EXPECTED["alpha_den"]],
            "K_ladder": list(KS),
            "ranking_formula": "J(y)=(q_A(y)-q_B(y))*ln(q_A(y)/q_B(y))",
            "q_formula": "q_R(y)=(G_R(y)+alpha)/(M+alpha*V)",
            "ranking_source": "training-only exact support-matched A/B aggregate counts",
            "ranking_shared_across_readings_and_regimes_within_fold": True,
            "tie_break": "frozen Issue161 outcome-vocabulary order",
            "sparse_multiplier_formula": "W_R^K(y)=W_R(y) for y in topK else 1",
            "conditional_formula": "P_SPARSE_K_R(y|c) proportional to P_POOL(y|c)*W_R^K(y)",
            "context_invariant_multiplier": True,
            "currier_by_previous_terminal_interaction": False,
            "target_native_fallback": False,
        },
        "outer": outer,
        "synthetic_test": synthetic,
        "firewall": {
            "scientific_sparse_metrics_computed": False,
            "real_target_EDGE_SPARSE_probability_computed": False,
            "real_target_EDGE_SPARSE_likelihood_computed": False,
            "G_sparse_computed": False,
            "G_missing_computed": False,
            "minimal_K_classification_computed": False,
            "heldout_target_outcome_used_for_ranking_or_selection": False,
            "K_ladder_changed": False,
            "ranking_score_tuned": False,
            "currier_labels_representation_folds_support_or_pooling_changed": False,
            "alpha_temperature_interpolation_fallback_or_mixture_tuned": False,
            "currier_by_previous_terminal_interaction_added": False,
            "hand_section_domain_conditioning": False,
            "latent_state_fit": False,
            "semantic_cipher_historical_inference": False,
        },
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue167-sparse-currier-outcome-gate0-v1",
        "issue": 167,
        "phase": "SPARSE_CURRIER_OUTCOME_GATE0",
        "gate_pass": False,
        "gate_disposition": "INVALID SPARSE CURRIER OUTCOME FACTORIZATION — GATE0 FAILED",
        "scientific_sparse_metrics_computed": False,
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
        print(canonical_json(synthetic_test()), end="")
        return 0

    zl_path = Path(ns.run[0]).resolve()
    it_path = Path(ns.run[1]).resolve()
    out_path = Path(ns.run[2]).resolve()
    try:
        result = run_gate(zl_path, it_path)
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
