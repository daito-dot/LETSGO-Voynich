#!/usr/bin/env python3
"""Phase63A: training-leaf-only vocabulary robustness for frozen A1.

No parameter selection occurs here. The only scientific intervention relative to
full-vocabulary A1 is that each outer fold may generate only token types observed
on that fold's training leaves.

Usage:
  python experiments/phase63/phase63a_training_vocab.py /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT
"""
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Set

import numpy as np

HERE = Path(__file__).resolve().parent
PHASE62 = HERE.parent / "phase62"
sys.path.insert(0, str(PHASE62))

import phase62b_n0 as b  # noqa: E402
import phase62c_c0_a1 as c  # noqa: E402
import phase62p_h62p1 as p  # noqa: E402


EXPECTED_H62P_RAW_SHA256 = "0e1b687ab73efbc494834f49398ed474230f47bcde4cf4dbcaa46631efd75264"
A1_REPS = 5
EPS = 1e-12


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def average_triplets(rows: Sequence[dict]) -> dict:
    return {k: float(np.mean([r[k] for r in rows])) for k in ("S1", "S2", "S3")}


def ratio(model: float, target: float) -> float:
    if target <= EPS:
        raise RuntimeError(f"non-positive target for historical ratio gate: {target}")
    return float(model / target)


def strict_wins(a: Sequence[float], bvals: Sequence[float]) -> int:
    if len(a) != len(bvals):
        raise RuntimeError("fold arrays differ in length")
    return sum(x + EPS < y for x, y in zip(a, bvals))


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT", file=sys.stderr)
        return 2

    voynich_path = Path(sys.argv[1]).resolve()
    cremma_root = Path(sys.argv[2]).resolve()

    # ---------- Frozen-source and prior-result authority checks ----------
    vblob = b.git_blob_sha1(voynich_path.read_bytes())
    if vblob != b.EXPECTED_ZL3B_BLOB:
        raise RuntimeError(f"ZL3b blob mismatch: {vblob} != {b.EXPECTED_ZL3B_BLOB}")
    ccommit = b.verify_cremma_commit(cremma_root)

    phase62c_path = PHASE62 / "phase62c_c0_a1_results.json"
    phase62p_path = PHASE62 / "phase62p_h62p1_results.json"
    h62p_digest = sha256_file(phase62p_path)
    if h62p_digest != EXPECTED_H62P_RAW_SHA256:
        raise RuntimeError(
            f"committed H62-P1 result digest mismatch: {h62p_digest} != {EXPECTED_H62P_RAW_SHA256}"
        )

    phase62c = json.loads(phase62c_path.read_text(encoding="utf-8"))
    phase62p = json.loads(phase62p_path.read_text(encoding="utf-8"))

    if phase62p["across_fold"]["prospective_profile_leader"] != "A1":
        raise RuntimeError("Phase62P authority does not record A1 as the frozen prospective leader")
    if phase62p["inputs"]["voynich_git_blob_sha1"] != vblob:
        raise RuntimeError("Phase62P Voynich input identity differs")
    if phase62p["inputs"]["cremma_commit"] != ccommit:
        raise RuntimeError("Phase62P CREMMA input identity differs")

    # ---------- Reconstruct exact outer-fold evaluation contexts ----------
    vitems = b.parse_voynich(voynich_path)
    folds = b.physical_leaf_folds(vitems)
    if len(folds) != 5:
        raise RuntimeError(f"expected five physical-leaf folds, got {len(folds)}")

    p61 = c.load_phase61_module()
    paragraphs, _ = p61.parse(str(voynich_path))
    p61_folds = p61.physical_leaf_folds(paragraphs)
    if [sorted(x) for x in p61_folds] != [sorted(x) for x in folds]:
        raise RuntimeError("Phase61/Phase62 physical-leaf folds differ")

    full_vocab: Set[str] = set(p61.all_tokens(paragraphs))
    if len(full_vocab) != phase62p["inputs"]["A1_empirical_vocabulary_types"]:
        raise RuntimeError("full vocabulary size differs from committed Phase62P authority")

    fold_results: List[dict] = []

    for fi, test_leaves in enumerate(folds):
        committed62c = phase62c["folds"][fi]
        committed62p = phase62p["folds"][fi]
        if committed62c["fold"] != fi or committed62p["fold"] != fi:
            raise RuntimeError(f"fold ordering mismatch at {fi}")
        if sorted(committed62c["test_leaves"]) != sorted(test_leaves):
            raise RuntimeError(f"Phase62C leaves differ in fold {fi}")
        if sorted(committed62p["test_leaves"]) != sorted(test_leaves):
            raise RuntimeError(f"Phase62P leaves differ in fold {fi}")

        # The held-out target itself is read from committed Phase62C/62P authority.
        heldout_target = committed62c["heldout_voynich"]
        heldout_profile = committed62p["voynich"]

        # Recompute only the training-side scaling/direction needed to score new output.
        train_items = b.by_leaves(vitems, test_leaves, include=False)
        sd = b.training_sd(train_items)
        dtrain = b.contrasts(train_items, sd)
        direction = np.mean(dtrain, axis=0)
        norm = float(np.linalg.norm(direction))
        if norm == 0:
            raise RuntimeError(f"fold {fi}: zero training direction")
        direction /= norm

        p61_train = p61.subset(paragraphs, test_leaves, include=False)
        p61_test = p61.subset(paragraphs, test_leaves, include=True)
        train_vocab = sorted(set(p61.all_tokens(p61_train)))
        train_vocab_set = set(train_vocab)
        if not train_vocab:
            raise RuntimeError(f"fold {fi}: empty training vocabulary")

        # Leakage/coverage diagnostics. Held-out token identities are inspected only
        # here and in target evaluation; they are not passed to the generator except
        # through the pre-existing layout object's token-count loops.
        test_tokens = p61.all_tokens(p61_test)
        test_types = set(test_tokens)
        missing_types = sorted(test_types - train_vocab_set)
        missing_occurrences = sum(t not in train_vocab_set for t in test_tokens)
        coverage = {
            "training_vocabulary_types": len(train_vocab),
            "full_manuscript_vocabulary_types": len(full_vocab),
            "heldout_observed_types": len(test_types),
            "heldout_types_absent_from_training": len(missing_types),
            "heldout_type_coverage_fraction": float(1.0 - len(missing_types) / len(test_types)) if test_types else 1.0,
            "heldout_observed_token_occurrences": len(test_tokens),
            "heldout_occurrences_with_type_absent_from_training": int(missing_occurrences),
            "heldout_occurrence_coverage_fraction": float(1.0 - missing_occurrences / len(test_tokens)) if test_tokens else 1.0,
        }

        # Exact frozen A1 parameters; verify against both prior result files.
        strength, local_p = c.A1_PARAMS[fi]
        rec62c = phase62c["inputs"]["A1_frozen_parameters"][str(fi)]
        rec62p = phase62p["inputs"]["A1_frozen_parameters"][str(fi)]
        for rec in (rec62c, rec62p):
            if abs(rec["entry_strength"] - strength) > EPS or abs(rec["local_family_p"] - local_p) > EPS:
                raise RuntimeError(f"fold {fi}: frozen A1 parameter authority mismatch")

        neighbors = p61.build_neighbors(train_vocab)
        tuple_neighbors: Dict[b.Token, set] = {
            tuple(k): {tuple(x) for x in vals}
            for k, vals in neighbors.items()
        }
        shape_scores = p61.learn_shape_scores(p61_train, train_vocab)
        entry_cum = p61.entry_cumulative(train_vocab, shape_scores, strength)

        exposed_reps = []
        profile_reps: Dict[str, dict] = {}
        generation_audit = []

        for r in range(A1_REPS):
            seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10 + r
            generated = p61.generate_layout(
                p61_test,
                train_vocab,
                neighbors,
                entry_cum,
                local_p,
                seed,
            )
            generated_tokens = p61.all_tokens(generated)
            outside = sorted(set(generated_tokens) - train_vocab_set)
            if outside:
                raise RuntimeError(f"fold {fi} rep {r}: generated held-out-only token types: {outside[:5]}")
            generation_audit.append({
                "replicate": r,
                "seed": seed,
                "generated_tokens": len(generated_tokens),
                "generated_types": len(set(generated_tokens)),
                "types_outside_training_vocabulary": 0,
            })

            gitems = c.convert_p61_paragraphs(generated)
            g_s1, _, _ = b.s1_projection(gitems, sd, direction)
            # Same S2 label as full-vocabulary A1 pairs permutation RNG streams.
            s2_label = f"A1:fold{fi}:rep{r}"
            g_s2 = c.s2_with_prebuilt_neighbors(gitems, s2_label, tuple_neighbors)
            g_s3 = b.s3_line_position(gitems)
            exposed_reps.append({
                "S1": float(g_s1),
                "S2": float(g_s2["excess"]),
                "S3": float(g_s3["mean_eta2"]),
            })

            # Same H62-P1 label as full-vocabulary A1 pairs null shuffle indices.
            profile_reps[f"rep{r}"] = p.raw_profile(gitems, s2_label)

        exposed = average_triplets(exposed_reps)
        profile = p.aggregate_excess(
            profile_reps,
            f"A1-R1:fold{fi}:mean-E",
            "generator realization",
        )
        d_profile = p.profile_distance(profile, heldout_profile)
        c_diff = p.c_short_diff(profile, heldout_profile)

        baseline_comp = committed62p["comparisons"]
        full_a1_comp = baseline_comp["A1"]
        fold_results.append({
            "fold": fi,
            "test_leaves": sorted(test_leaves),
            "coverage": coverage,
            "frozen_parameters": {"entry_strength": strength, "local_family_p": local_p},
            "generation_audit": generation_audit,
            "heldout_voynich_exposed_target": heldout_target,
            "A1_R1_exposed_replicates": exposed_reps,
            "A1_R1_exposed_mean": exposed,
            "A1_R1_exposed_ratios": {k: ratio(exposed[k], heldout_target[k]) for k in ("S1", "S2", "S3")},
            "heldout_voynich_H62P1": heldout_profile,
            "A1_R1_H62P1_replicates": profile_reps,
            "A1_R1_H62P1_profile": profile,
            "A1_R1_comparison": {
                "D_profile": d_profile,
                "abs_C_short_diff": c_diff,
            },
            "committed_baseline_comparisons": {
                "N0": baseline_comp["N0"],
                "C0": baseline_comp["C0"],
                "full_vocab_A1": full_a1_comp,
            },
            "delta_vs_full_vocab_A1": {
                "D_profile": float(d_profile - full_a1_comp["D_profile"]),
                "abs_C_short_diff": float(c_diff - full_a1_comp["abs_C_short_diff"]),
            },
        })

    # ---------- Frozen across-fold robustness decision ----------
    target_mean = {
        k: float(np.mean([f["heldout_voynich_exposed_target"][k] for f in fold_results]))
        for k in ("S1", "S2", "S3")
    }
    r1_mean = {
        k: float(np.mean([f["A1_R1_exposed_mean"][k] for f in fold_results]))
        for k in ("S1", "S2", "S3")
    }
    r1_ratios = {k: ratio(r1_mean[k], target_mean[k]) for k in ("S1", "S2", "S3")}
    r1_common_pass = {k: 0.5 <= r1_ratios[k] <= 2.0 for k in r1_ratios}

    r1_d = [f["A1_R1_comparison"]["D_profile"] for f in fold_results]
    r1_c = [f["A1_R1_comparison"]["abs_C_short_diff"] for f in fold_results]
    r1_summary = {
        "mean_D_profile": float(np.mean(r1_d)),
        "median_D_profile": float(statistics.median(r1_d)),
        "mean_abs_C_short_diff": float(np.mean(r1_c)),
        "D_profile_fold_values": r1_d,
        "abs_C_short_diff_fold_values": r1_c,
    }

    baseline_summaries = phase62p["across_fold"]["candidate_summaries"]
    fold_wins = {}
    for baseline in ("N0", "C0"):
        bd = [f["committed_baseline_comparisons"][baseline]["D_profile"] for f in fold_results]
        bc = [f["committed_baseline_comparisons"][baseline]["abs_C_short_diff"] for f in fold_results]
        fold_wins[baseline] = {
            "D_profile_wins": strict_wins(r1_d, bd),
            "abs_C_short_diff_wins": strict_wins(r1_c, bc),
        }

    mean_superiority = {
        baseline: {
            "lower_mean_D_profile": r1_summary["mean_D_profile"] + EPS < baseline_summaries[baseline]["mean_D_profile"],
            "lower_mean_abs_C_short_diff": r1_summary["mean_abs_C_short_diff"] + EPS < baseline_summaries[baseline]["mean_abs_C_short_diff"],
        }
        for baseline in ("N0", "C0")
    }

    exposed_survives = all(r1_common_pass.values())
    mean_superiority_pass = all(
        q["lower_mean_D_profile"] and q["lower_mean_abs_C_short_diff"]
        for q in mean_superiority.values()
    )
    fold_majority_pass = all(
        q["D_profile_wins"] >= 3 and q["abs_C_short_diff_wins"] >= 3
        for q in fold_wins.values()
    )
    robust = exposed_survives and mean_superiority_pass and fold_majority_pass

    full_common_ratios = phase62c["across_fold"]["A1_ratio_of_means_to_voynich"]
    full_h62 = baseline_summaries["A1"]
    degradation = {
        "common_ratio_delta_R1_minus_full_A1": {
            k: float(r1_ratios[k] - full_common_ratios[k]) for k in ("S1", "S2", "S3")
        },
        "mean_D_profile_delta_R1_minus_full_A1": float(r1_summary["mean_D_profile"] - full_h62["mean_D_profile"]),
        "median_D_profile_delta_R1_minus_full_A1": float(r1_summary["median_D_profile"] - full_h62["median_D_profile"]),
        "mean_abs_C_short_diff_delta_R1_minus_full_A1": float(
            r1_summary["mean_abs_C_short_diff"] - full_h62["mean_abs_C_short_diff"]
        ),
    }

    coverage_summary = {
        "training_vocabulary_types_mean": float(np.mean([f["coverage"]["training_vocabulary_types"] for f in fold_results])),
        "training_vocabulary_types_min": int(min(f["coverage"]["training_vocabulary_types"] for f in fold_results)),
        "training_vocabulary_types_max": int(max(f["coverage"]["training_vocabulary_types"] for f in fold_results)),
        "heldout_type_coverage_fraction_mean": float(np.mean([f["coverage"]["heldout_type_coverage_fraction"] for f in fold_results])),
        "heldout_occurrence_coverage_fraction_mean": float(np.mean([f["coverage"]["heldout_occurrence_coverage_fraction"] for f in fold_results])),
    }

    if robust:
        interpretation = (
            "ROBUST — A1 exposed and H62-P1 advantages survive removal of held-out-only vocabulary types without retuning"
        )
    else:
        interpretation = (
            "NOT ROBUST — at least one frozen Phase63A retention condition fails after removing held-out-only vocabulary types"
        )

    out = {
        "phase": "63A",
        "hypothesis": "P63-A1-R1 training-only output vocabulary robustness",
        "scope_firewall": "no A2/C1/M0, no parameter retuning, no H62-P1 changes",
        "inputs": {
            "voynich_git_blob_sha1": vblob,
            "cremma_commit": ccommit,
            "committed_H62P1_raw_sha256": h62p_digest,
            "full_manuscript_vocabulary_types": len(full_vocab),
            "A1_frozen_parameters": {
                str(k): {"entry_strength": v[0], "local_family_p": v[1]}
                for k, v in c.A1_PARAMS.items()
            },
            "replicates_per_fold": A1_REPS,
            "H62P1_null_reps": p.NULL_REPS,
        },
        "folds": fold_results,
        "across_fold": {
            "heldout_voynich_exposed_mean": target_mean,
            "A1_R1_exposed_mean": r1_mean,
            "A1_R1_ratio_of_means_to_voynich": r1_ratios,
            "A1_R1_common_gate_0.5_to_2.0": r1_common_pass,
            "A1_R1_H62P1_summary": r1_summary,
            "committed_H62P1_baseline_summaries": {
                k: baseline_summaries[k] for k in ("N0", "C0", "A1")
            },
            "mean_superiority_vs_baselines": mean_superiority,
            "fold_wins_vs_baselines": fold_wins,
            "coverage_summary": coverage_summary,
            "degradation_vs_full_vocab_A1": degradation,
            "frozen_survival_components": {
                "R1_exposed_scalar_retention": exposed_survives,
                "R2_H62P1_mean_superiority": mean_superiority_pass,
                "R3_H62P1_fold_majority_superiority": fold_majority_pass,
            },
            "robust_to_heldout_vocabulary_removal": robust,
            "interpretation": interpretation,
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
