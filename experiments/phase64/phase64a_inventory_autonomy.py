#!/usr/bin/env python3
"""Phase64A frozen empirical-inventory autonomy ablation.

This executable is committed before the first Phase64A scientific reveal.
It applies the preregistered MG0 replacement to the exact A1-R1 structural
contract on canonical ZL and independent IT2a/W1 arms.

Usage:
  python experiments/phase64/phase64a_inventory_autonomy.py ZL3b-n.txt IT2a-n.txt
"""
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
PHASE62 = HERE.parent / "phase62"
PHASE63 = HERE.parent / "phase63"
for path in (PHASE62, PHASE63, HERE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import phase62b_n0 as b  # noqa: E402
import phase62c_c0_a1 as c  # noqa: E402
import phase62p_h62p1 as p  # noqa: E402
import phase63b_common_b1 as q  # noqa: E402
import phase63b_science as s63b  # noqa: E402
import phase64a_mg0 as mg  # noqa: E402

EXPECTED_PHASE63A_RAW_SHA256 = "bcd05d1823e17b034c0abf984a0af9b0cb31b5a37bd9e604c327ab9aff1937a7"
EXPECTED_PHASE63B_RAW_SHA256 = "77653133af22cd26141bc695a8ee6243cc3d924ba44a41a685cb148b9167db91"
EXPECTED_H62P_RAW_SHA256 = "0e1b687ab73efbc494834f49398ed474230f47bcde4cf4dbcaa46631efd75264"
A1_REPS = 5
EPS = 1e-12


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def average_triplets(rows: Sequence[dict]) -> dict:
    return {k: float(np.mean([row[k] for row in rows])) for k in ("S1", "S2", "S3")}


def ratio(model: float, target: float) -> float:
    if target <= EPS:
        raise RuntimeError(f"non-positive target for historical ratio gate: {target}")
    return float(model / target)


def strict_wins(a: Sequence[float], bvals: Sequence[float]) -> int:
    if len(a) != len(bvals):
        raise RuntimeError("fold arrays differ in length")
    return sum(x + EPS < y for x, y in zip(a, bvals))


def empirical_neighbor_summary(vocab: Sequence[str], neighbors: Dict[str, List[str]]) -> dict:
    degrees = [len(neighbors.get(t, ())) for t in vocab]
    return {
        "types": len(vocab),
        "fraction_with_edit1_neighbor": float(sum(d > 0 for d in degrees) / len(degrees)),
        "mean_edit1_degree": float(statistics.mean(degrees)),
        "max_edit1_degree": int(max(degrees)),
        "length_stats": mg.length_stats(vocab),
    }


def summarize_arm(name: str, fold_rows: Sequence[dict], previous: dict | None = None) -> dict:
    instantiation_failures = [
        {"fold": row["fold"], "failures": row.get("MG0_instantiation_failures", [])}
        for row in fold_rows
        if row.get("MG0_instantiation_failures")
    ]
    if instantiation_failures:
        return {
            "source_arm": name,
            "pass": False,
            "failure_class": "MG0_INSTANTIATION_FAILURE",
            "instantiation_failures": instantiation_failures,
            "previous_A1_R1_authority": previous,
        }

    target_mean = {
        k: float(np.mean([row["heldout_target_exposed"][k] for row in fold_rows]))
        for k in ("S1", "S2", "S3")
    }
    candidate_mean = {
        k: float(np.mean([row["A1_R2_exposed_mean"][k] for row in fold_rows]))
        for k in ("S1", "S2", "S3")
    }
    ratios = {k: ratio(candidate_mean[k], target_mean[k]) for k in ("S1", "S2", "S3")}
    scalar_passes = {k: 0.5 <= ratios[k] <= 2.0 for k in ratios}

    ds = [row["A1_R2_comparison"]["D_profile"] for row in fold_rows]
    cs = [row["A1_R2_comparison"]["abs_C_short_diff"] for row in fold_rows]
    candidate_summary = {
        "mean_D_profile": float(np.mean(ds)),
        "median_D_profile": float(statistics.median(ds)),
        "mean_abs_C_short_diff": float(np.mean(cs)),
        "D_profile_fold_values": ds,
        "abs_C_short_diff_fold_values": cs,
    }

    baseline_summaries = {}
    mean_superiority = {}
    fold_wins = {}
    for baseline in ("N0", "C0"):
        bd = [row["baseline_comparisons"][baseline]["D_profile"] for row in fold_rows]
        bc = [row["baseline_comparisons"][baseline]["abs_C_short_diff"] for row in fold_rows]
        baseline_summaries[baseline] = {
            "mean_D_profile": float(np.mean(bd)),
            "median_D_profile": float(statistics.median(bd)),
            "mean_abs_C_short_diff": float(np.mean(bc)),
            "D_profile_fold_values": bd,
            "abs_C_short_diff_fold_values": bc,
        }
        mean_superiority[baseline] = {
            "lower_mean_D_profile": candidate_summary["mean_D_profile"] + EPS < baseline_summaries[baseline]["mean_D_profile"],
            "lower_mean_abs_C_short_diff": candidate_summary["mean_abs_C_short_diff"] + EPS < baseline_summaries[baseline]["mean_abs_C_short_diff"],
        }
        fold_wins[baseline] = {
            "D_profile_wins": strict_wins(ds, bd),
            "abs_C_short_diff_wins": strict_wins(cs, bc),
        }

    exposed_pass = all(scalar_passes.values())
    mean_pass = all(
        row["lower_mean_D_profile"] and row["lower_mean_abs_C_short_diff"]
        for row in mean_superiority.values()
    )
    fold_pass = all(
        row["D_profile_wins"] >= 3 and row["abs_C_short_diff_wins"] >= 3
        for row in fold_wins.values()
    )
    arm_pass = bool(exposed_pass and mean_pass and fold_pass)

    out = {
        "source_arm": name,
        "heldout_target_exposed_mean": target_mean,
        "A1_R2_exposed_mean": candidate_mean,
        "A1_R2_ratio_of_means_to_target": ratios,
        "A1_R2_scalar_gate_0.5_to_2.0": scalar_passes,
        "A1_R2_H62P1_summary": candidate_summary,
        "baseline_H62P1_summaries": baseline_summaries,
        "mean_superiority_vs_baselines": mean_superiority,
        "fold_wins_vs_baselines": fold_wins,
        "exposed_gate_pass": exposed_pass,
        "H62_mean_superiority_pass": mean_pass,
        "H62_fold_majority_pass": fold_pass,
        "pass": arm_pass,
        "previous_A1_R1_authority": previous,
    }
    if previous:
        prev_ratios = previous.get("exposed_ratios")
        prev_h62 = previous.get("H62P1")
        degradation = {}
        if prev_ratios:
            degradation["exposed_ratio_delta_R2_minus_R1"] = {
                k: float(ratios[k] - prev_ratios[k]) for k in ("S1", "S2", "S3")
            }
        if prev_h62:
            degradation["mean_D_profile_delta_R2_minus_R1"] = float(
                candidate_summary["mean_D_profile"] - prev_h62["mean_D_profile"]
            )
            degradation["mean_abs_C_short_diff_delta_R2_minus_R1"] = float(
                candidate_summary["mean_abs_C_short_diff"] - prev_h62["mean_abs_C_short_diff"]
            )
        out["diagnostic_degradation_vs_A1_R1"] = degradation
    return out


def synth_rep(
    *,
    source: str,
    fi: int,
    r: int,
    p61,
    p61_train,
    p61_test,
    train_vocab: Sequence[str],
    heldout_types: Sequence[str],
    model: mg.MarkovModel,
    mg_cv: dict,
    sd: np.ndarray,
    direction: np.ndarray,
    strength: float,
    local_p: float,
    morph_seed: int,
    a1_seed: int,
    s2_label: str,
    h62_label: str,
) -> dict:
    synth_vocab, sampling = mg.generate_synthetic_vocab(model, len(train_vocab), morph_seed)
    neighbors = p61.build_neighbors(synth_vocab)
    diag = mg.vocabulary_diagnostics(
        synth_vocab,
        train_vocab,
        heldout_types,
        neighbors,
        sampling,
    )
    if diag["synthetic_characters_absent_from_training"]:
        raise RuntimeError(f"{source} fold {fi} rep {r}: synthetic alphabet leakage")

    shape_scores = p61.learn_shape_scores(p61_train, synth_vocab)
    entry_cum = p61.entry_cumulative(synth_vocab, shape_scores, strength)
    generated = p61.generate_layout(
        p61_test,
        synth_vocab,
        neighbors,
        entry_cum,
        local_p,
        a1_seed,
    )
    generated_tokens = p61.all_tokens(generated)
    if any(t not in set(synth_vocab) for t in generated_tokens):
        raise RuntimeError(f"{source} fold {fi} rep {r}: A1 output outside synthetic vocabulary")

    gitems = c.convert_p61_paragraphs(generated)
    g_s1, n_s1, delta = b.s1_projection(gitems, sd, direction)
    if g_s1 is None:
        raise RuntimeError(f"{source} fold {fi} rep {r}: generated S1 unavailable")
    tuple_neighbors = {tuple(k): {tuple(x) for x in vals} for k, vals in neighbors.items()}
    g_s2 = c.s2_with_prebuilt_neighbors(gitems, s2_label, tuple_neighbors)
    g_s3 = b.s3_line_position(gitems)
    profile = p.raw_profile(gitems, h62_label)

    return {
        "replicate": r,
        "MG0": {
            "selected_order": model.order,
            "inner_cv": mg_cv,
            "morphology_seed": morph_seed,
            "diagnostics": diag,
        },
        "A1": {
            "layout_seed": a1_seed,
            "generated_token_occurrences": len(generated_tokens),
            "generated_types_used": len(set(generated_tokens)),
            "S1_n_items": n_s1,
            "S1_mean_delta8": delta,
        },
        "exposed": {
            "S1": float(g_s1),
            "S2": float(g_s2["excess"]),
            "S3": float(g_s3["mean_eta2"]),
        },
        "S2_detail": g_s2,
        "H62P1": profile,
    }


def run_zl(
    voynich_path: Path,
    phase62c: dict,
    phase62p: dict,
    phase63a: dict,
) -> dict:
    vblob = b.git_blob_sha1(voynich_path.read_bytes())
    if vblob != b.EXPECTED_ZL3B_BLOB:
        raise RuntimeError(f"ZL3b blob mismatch: {vblob} != {b.EXPECTED_ZL3B_BLOB}")

    vitems = b.parse_voynich(voynich_path)
    folds = b.physical_leaf_folds(vitems)
    if len(folds) != 5:
        raise RuntimeError(f"ZL expected five folds, got {len(folds)}")

    p61 = c.load_phase61_module()
    paragraphs, _ = p61.parse(str(voynich_path))
    p61_folds = p61.physical_leaf_folds(paragraphs)
    if [sorted(x) for x in p61_folds] != [sorted(x) for x in folds]:
        raise RuntimeError("ZL Phase61/Phase62 folds differ")

    fold_rows = []
    for fi, test_leaves in enumerate(folds):
        c62 = phase62c["folds"][fi]
        p62 = phase62p["folds"][fi]
        a63 = phase63a["folds"][fi]
        for authority in (c62, p62, a63):
            if authority["fold"] != fi or sorted(authority["test_leaves"]) != sorted(test_leaves):
                raise RuntimeError(f"ZL committed fold authority mismatch at {fi}")

        target = c62["heldout_voynich"]
        target_profile = p62["voynich"]
        baseline = {
            "N0": p62["comparisons"]["N0"],
            "C0": p62["comparisons"]["C0"],
        }

        train_items = b.by_leaves(vitems, test_leaves, include=False)
        sd = b.training_sd(train_items)
        dtrain = b.contrasts(train_items, sd)
        direction = np.mean(dtrain, axis=0)
        norm = float(np.linalg.norm(direction))
        if norm == 0:
            raise RuntimeError(f"ZL fold {fi}: zero training S1 direction")
        direction /= norm

        p61_train = p61.subset(paragraphs, test_leaves, include=False)
        p61_test = p61.subset(paragraphs, test_leaves, include=True)
        train_vocab = sorted(set(p61.all_tokens(p61_train)))
        heldout_types = sorted(set(p61.all_tokens(p61_test)))
        empirical_neighbors = p61.build_neighbors(train_vocab)
        empirical_diag = empirical_neighbor_summary(train_vocab, empirical_neighbors)
        model, cv = mg.select_order(train_vocab)

        strength, local_p = c.A1_PARAMS[fi]
        for authority_params in (
            phase62c["inputs"]["A1_frozen_parameters"][str(fi)],
            phase62p["inputs"]["A1_frozen_parameters"][str(fi)],
        ):
            if abs(authority_params["entry_strength"] - strength) > EPS or abs(authority_params["local_family_p"] - local_p) > EPS:
                raise RuntimeError(f"ZL fold {fi}: A1 parameter authority mismatch")

        reps = []
        failures = []
        for r in range(A1_REPS):
            morph_seed = 6400000 + fi * 1000 + r
            a1_seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10 + r
            label = f"A1:fold{fi}:rep{r}"
            try:
                reps.append(synth_rep(
                    source="ZL3b",
                    fi=fi,
                    r=r,
                    p61=p61,
                    p61_train=p61_train,
                    p61_test=p61_test,
                    train_vocab=train_vocab,
                    heldout_types=heldout_types,
                    model=model,
                    mg_cv=cv,
                    sd=sd,
                    direction=direction,
                    strength=strength,
                    local_p=local_p,
                    morph_seed=morph_seed,
                    a1_seed=a1_seed,
                    s2_label=label,
                    h62_label=label,
                ))
            except RuntimeError as exc:
                if str(exc).startswith("MG0 uniqueness failure"):
                    failures.append({"replicate": r, "error": str(exc), "morphology_seed": morph_seed})
                    continue
                raise

        row = {
            "fold": fi,
            "test_leaves": sorted(test_leaves),
            "frozen_parameters": {"entry_strength": strength, "local_family_p": local_p},
            "MG0_outer_training": {
                "training_vocabulary_types": len(train_vocab),
                "heldout_observed_types": len(heldout_types),
                "empirical_training_morphology": empirical_diag,
                "order_selection": cv,
            },
            "MG0_instantiation_failures": failures,
            "heldout_target_exposed": target,
            "heldout_target_H62P1": target_profile,
            "baseline_comparisons": baseline,
            "previous_A1_R1_comparison": a63["A1_R1_comparison"],
            "replicates": reps,
        }
        if not failures and len(reps) == A1_REPS:
            exposed = average_triplets([rep["exposed"] for rep in reps])
            profiles = {f"rep{rep['replicate']}": rep["H62P1"] for rep in reps}
            profile = p.aggregate_excess(profiles, f"Phase64A:ZL:A1-R2:fold{fi}:mean-E", "generator realization")
            row["A1_R2_exposed_mean"] = exposed
            row["A1_R2_H62P1_profile"] = profile
            row["A1_R2_comparison"] = {
                "D_profile": p.profile_distance(profile, target_profile),
                "abs_C_short_diff": p.c_short_diff(profile, target_profile),
            }
        fold_rows.append(row)

    prev = {
        "exposed_ratios": phase63a["across_fold"]["A1_R1_ratio_of_means_to_voynich"],
        "H62P1": phase63a["across_fold"]["A1_R1_H62P1_summary"],
    }
    return {
        "source": "ZL3b",
        "role": "primary canonical autonomy arm",
        "input_git_blob_sha1": vblob,
        "folds": fold_rows,
        "across_fold": summarize_arm("ZL3b", fold_rows, prev),
    }


def run_it(it_path: Path, phase63b: dict) -> dict:
    paragraphs, audit = q.parse_ivtff(it_path, "IT2a", "W1")
    observed_preflight = s63b.preflight_summary(paragraphs, audit)
    expected_preflight = dict(zip(s63b.PREFLIGHT_FIELDS, s63b.PREFLIGHT_EXPECTED["IT2a"]["W1"]))
    if observed_preflight != expected_preflight:
        raise RuntimeError(f"IT W1 preflight mismatch: got={observed_preflight} expected={expected_preflight}")

    if audit["source_identity"]["sha256"] != phase63b["inputs"]["source_identity"]["IT2a"]["sha256"]:
        raise RuntimeError("IT source identity differs from committed Phase63B authority")

    folds = s63b.committed_folds()
    prev_view = phase63b["IT_full_A1_R1_transfer"]["W1"]
    if len(prev_view["folds"]) != 5:
        raise RuntimeError("IT committed Phase63B fold count differs")

    p61 = c.load_phase61_module()
    fold_rows = []
    for fi, test_leaves in enumerate(folds):
        prev_fold = prev_view["folds"][fi]
        if prev_fold["fold"] != fi or sorted(prev_fold["test_leaves"]) != sorted(test_leaves):
            raise RuntimeError(f"IT committed fold authority mismatch at {fi}")

        ctx = s63b.training_context(paragraphs, test_leaves)
        target = prev_fold["target_exposed"]
        target_profile = prev_fold["target_H62P1"]
        baseline = {
            "N0": prev_fold["H62P1_comparisons"]["N0"],
            "C0": prev_fold["H62P1_comparisons"]["C0"],
        }

        native_train = q.leaf_subset(paragraphs, test_leaves, include=False)
        native_test = q.leaf_subset(paragraphs, test_leaves, include=True)
        p61_train = q.to_phase61_paragraphs(native_train, p61)
        p61_test = q.to_phase61_paragraphs(native_test, p61)
        train_vocab = sorted(set(p61.all_tokens(p61_train)))
        heldout_types = sorted(set(p61.all_tokens(p61_test)))
        empirical_neighbors = p61.build_neighbors(train_vocab)
        empirical_diag = empirical_neighbor_summary(train_vocab, empirical_neighbors)
        model, cv = mg.select_order(train_vocab)

        strength, local_p = c.A1_PARAMS[fi]
        authority_params = phase63b["inputs"]["A1_frozen_parameters"][str(fi)]
        if abs(authority_params["entry_strength"] - strength) > EPS or abs(authority_params["local_family_p"] - local_p) > EPS:
            raise RuntimeError(f"IT fold {fi}: A1 parameter authority mismatch")

        reps = []
        failures = []
        for r in range(A1_REPS):
            morph_seed = 7400000 + fi * 1000 + r
            a1_seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10 + r
            s2_label = f"Phase63B:IT2a:W1:A1-S2:fold{fi}:rep{r}"
            h62_label = f"Phase63B:IT2a:W1:A1-H62P1:fold{fi}:rep{r}"
            try:
                reps.append(synth_rep(
                    source="IT2a-W1",
                    fi=fi,
                    r=r,
                    p61=p61,
                    p61_train=p61_train,
                    p61_test=p61_test,
                    train_vocab=train_vocab,
                    heldout_types=heldout_types,
                    model=model,
                    mg_cv=cv,
                    sd=ctx["sd"],
                    direction=ctx["direction"],
                    strength=strength,
                    local_p=local_p,
                    morph_seed=morph_seed,
                    a1_seed=a1_seed,
                    s2_label=s2_label,
                    h62_label=h62_label,
                ))
            except RuntimeError as exc:
                if str(exc).startswith("MG0 uniqueness failure"):
                    failures.append({"replicate": r, "error": str(exc), "morphology_seed": morph_seed})
                    continue
                raise

        row = {
            "fold": fi,
            "test_leaves": sorted(test_leaves),
            "frozen_parameters": {"entry_strength": strength, "local_family_p": local_p},
            "MG0_outer_training": {
                "training_vocabulary_types": len(train_vocab),
                "heldout_observed_types": len(heldout_types),
                "empirical_training_morphology": empirical_diag,
                "order_selection": cv,
            },
            "MG0_instantiation_failures": failures,
            "heldout_target_exposed": target,
            "heldout_target_H62P1": target_profile,
            "baseline_comparisons": baseline,
            "previous_A1_R1_comparison": prev_fold["H62P1_comparisons"]["A1_R1"],
            "replicates": reps,
        }
        if not failures and len(reps) == A1_REPS:
            exposed = average_triplets([rep["exposed"] for rep in reps])
            profiles = {f"rep{rep['replicate']}": rep["H62P1"] for rep in reps}
            profile = p.aggregate_excess(profiles, f"Phase64A:IT2a-W1:A1-R2:fold{fi}:mean-E", "generator realization")
            row["A1_R2_exposed_mean"] = exposed
            row["A1_R2_H62P1_profile"] = profile
            row["A1_R2_comparison"] = {
                "D_profile": p.profile_distance(profile, target_profile),
                "abs_C_short_diff": p.c_short_diff(profile, target_profile),
            }
        fold_rows.append(row)

    prev_across = prev_view["across_fold"]
    prev = {
        "exposed_ratios": prev_across["A1_R1_ratio_of_means_to_IT"],
        "H62P1": prev_across["H62P1_candidate_summaries"]["A1_R1"],
    }
    return {
        "source": "IT2a",
        "view": "W1",
        "role": "independent confirmatory autonomy arm",
        "source_identity": audit["source_identity"],
        "preflight": observed_preflight,
        "folds": fold_rows,
        "across_fold": summarize_arm("IT2a-W1", fold_rows, prev),
    }


def classify(zl_pass: bool, it_pass: bool) -> tuple[str, str]:
    if zl_pass and it_pass:
        return (
            "STRONG INVENTORY-AUTONOMY SUPPORT",
            "Under frozen MG0, A1's tested exposed and prospective structural advantage survives removal of the explicit empirical training-token inventory in both canonical ZL and independent IT arms",
        )
    if zl_pass and not it_pass:
        return (
            "PRIMARY-ONLY SUPPORT / INDEPENDENT FAILURE",
            "Canonical ZL passes the frozen inventory-autonomy gate but independent IT does not",
        )
    if not zl_pass and it_pass:
        return (
            "INCONSISTENT / PRIMARY FAILURE",
            "Independent IT passes but canonical ZL fails the frozen inventory-autonomy gate",
        )
    return (
        "NOT SUPPORTED",
        "Both canonical ZL and independent IT fail the frozen A1-R2/MG0 inventory-autonomy gate",
    )


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt IT2a-n.txt", file=sys.stderr)
        return 2

    zl_path = Path(sys.argv[1]).resolve()
    it_path = Path(sys.argv[2]).resolve()

    phase62c_path = PHASE62 / "phase62c_c0_a1_results.json"
    phase62p_path = PHASE62 / "phase62p_h62p1_results.json"
    phase63a_path = PHASE63 / "phase63a_training_vocab_results.json"
    phase63b_path = PHASE63 / "phase63b_science_results.json"

    digests = {
        "phase62p": sha256_file(phase62p_path),
        "phase63a": sha256_file(phase63a_path),
        "phase63b": sha256_file(phase63b_path),
    }
    expected = {
        "phase62p": EXPECTED_H62P_RAW_SHA256,
        "phase63a": EXPECTED_PHASE63A_RAW_SHA256,
        "phase63b": EXPECTED_PHASE63B_RAW_SHA256,
    }
    if digests != expected:
        raise RuntimeError(f"committed prior-result authority digest mismatch: got={digests} expected={expected}")

    phase62c = json.loads(phase62c_path.read_text(encoding="utf-8"))
    phase62p = json.loads(phase62p_path.read_text(encoding="utf-8"))
    phase63a = json.loads(phase63a_path.read_text(encoding="utf-8"))
    phase63b = json.loads(phase63b_path.read_text(encoding="utf-8"))

    if phase62p["across_fold"]["prospective_profile_leader"] != "A1":
        raise RuntimeError("Phase62P authority no longer records A1 as prospective leader")
    if not phase63a["across_fold"]["robust"]:
        raise RuntimeError("Phase63A authority no longer records A1-R1 robustness")
    if not phase63b["across_phase63B"]["strong_replication"]:
        raise RuntimeError("Phase63B authority no longer records strong replication")

    zl = run_zl(zl_path, phase62c, phase62p, phase63a)
    it = run_it(it_path, phase63b)
    zl_pass = bool(zl["across_fold"]["pass"])
    it_pass = bool(it["across_fold"]["pass"])
    classification, interpretation = classify(zl_pass, it_pass)

    out = {
        "phase": "64A",
        "hypothesis": "P64-A1-R2 empirical-inventory autonomy under frozen MG0",
        "scope_firewall": "only output-vocabulary source changes; no A2/C1/M0, no parameter retuning, no longer memory, no H62 change, no held-out morphology selection",
        "MG0_contract": {
            "orders": list(mg.ORDERS),
            "alpha": mg.ALPHA,
            "inner_folds": mg.INNER_FOLDS,
            "max_token_length": mg.MAX_TOKEN_LENGTH,
            "attempt_multiplier": mg.ATTEMPT_MULTIPLIER,
            "distinct_training_types_weighted_once": True,
            "synthetic_vocab_size_equals_training_vocab_size": True,
            "empirical_membership_query_during_sampling": False,
            "ZL_morphology_seed_formula": "6400000 + fold*1000 + replicate",
            "IT_morphology_seed_formula": "7400000 + fold*1000 + replicate",
        },
        "prior_authority_raw_sha256": digests,
        "A1_frozen_parameters": {
            str(fi): {"entry_strength": vals[0], "local_family_p": vals[1]}
            for fi, vals in c.A1_PARAMS.items()
        },
        "replicates_per_fold": A1_REPS,
        "H62P1_null_reps": p.NULL_REPS,
        "ZL_primary": zl,
        "IT_independent": it,
        "across_phase64A": {
            "ZL_primary_pass": zl_pass,
            "IT_independent_pass": it_pass,
            "classification": classification,
            "interpretation": interpretation,
        },
        "claim_limit": "inventory-autonomy only; no semantic emptiness, historical identity, family-level G dominance or decipherment",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
