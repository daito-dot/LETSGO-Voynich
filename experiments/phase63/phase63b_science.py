#!/usr/bin/env python3
"""Phase63B frozen independent-transcription scientific replication.

This executable is committed before any GC-R1/GC-R2/IT-R1/IT-R2/IT-R3
scientific outcome is computed. It implements PLAN_B.md, IMPLEMENTATION_B.md,
and the pre-science PARSER_AMENDMENT_B1.md without adaptive mapping or retuning.

Usage:
  python experiments/phase63/phase63b_science.py ZL3b-n.txt GC2a-n.txt IT2a-n.txt /path/to/CREMMA-Medieval-LAT
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set

import numpy as np

HERE = Path(__file__).resolve().parent
PHASE62 = HERE.parent / "phase62"
if str(PHASE62) not in sys.path:
    sys.path.insert(0, str(PHASE62))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase62b_n0 as b  # noqa: E402
import phase62c_c0_a1 as c  # noqa: E402
import phase62p_h62p1 as p  # noqa: E402
import phase63b_common_b1 as q  # noqa: E402


A1_REPS = 5
EPS = 1e-12
FIXED_C0 = "C0-4_digraph"
VIEWS = ("W1", "W2")
SOURCES = ("ZL3b", "GC2a", "IT2a")

# Exact successful B1 parser-only preflight identities. Scientific execution
# must reproduce these counts before any feature/edit1/profile calculation.
PREFLIGHT_EXPECTED = {
    "ZL3b": {
        "W1": (740, 740, 4115, 34360, 6895, 597, 436, 99, 701, 13),
        "W2": (740, 740, 4115, 31898, 7824, 582, 422, 99, 701, 13),
    },
    "GC2a": {
        "W1": (775, 775, 4130, 36658, 8602, 633, 448, 99, 45, 0),
        "W2": (775, 775, 4130, 34415, 9264, 620, 439, 99, 45, 0),
    },
    "IT2a": {
        "W1": (772, 772, 4117, 34411, 7069, 602, 440, 99, 80, 0),
        "W2": (772, 772, 4117, 34411, 7069, 602, 440, 99, 80, 0),
    },
}
PREFLIGHT_FIELDS = (
    "parsed_paragraphs",
    "paragraph_starts_consumed",
    "nonempty_physical_lines",
    "usable_token_occurrences",
    "usable_token_types",
    "base_eligible_paragraphs",
    "S1_eligible_paragraphs",
    "physical_leaves",
    "excluded_uncertain_or_unreadable_tokens",
    "ignored_nonempty_P_lines_outside_paragraph",
)


def preflight_summary(paragraphs: Sequence[q.NativeParagraph], audit: dict) -> dict:
    its = q.items(paragraphs)
    tokens = [tok for par in paragraphs for line in par.lines for tok in line]
    return {
        "parsed_paragraphs": len(paragraphs),
        "paragraph_starts_consumed": audit["paragraph_starts_consumed"],
        "nonempty_physical_lines": sum(len(par.lines) for par in paragraphs),
        "usable_token_occurrences": len(tokens),
        "usable_token_types": len(set(tokens)),
        "base_eligible_paragraphs": sum(b.base_eligible(it) for it in its),
        "S1_eligible_paragraphs": sum(b.s1_eligible(it) for it in its),
        "physical_leaves": len({par.leaf for par in paragraphs if par.leaf is not None}),
        "excluded_uncertain_or_unreadable_tokens": audit["excluded_uncertain_or_unreadable_tokens"],
        "ignored_nonempty_P_lines_outside_paragraph": audit["ignored_nonempty_P_lines_outside_paragraph"],
    }


def assert_preflight(parsed: Dict[str, Dict[str, Sequence[q.NativeParagraph]]], audits: dict) -> dict:
    observed: dict = {}
    for source in SOURCES:
        observed[source] = {}
        for view in VIEWS:
            got = preflight_summary(parsed[source][view], audits[source][view])
            observed[source][view] = got
            expected = dict(zip(PREFLIGHT_FIELDS, PREFLIGHT_EXPECTED[source][view]))
            if got != expected:
                raise RuntimeError(
                    f"preflight population mismatch for {source} {view}: got={got} expected={expected}"
                )
    return observed


def committed_folds() -> List[Set[int]]:
    c_path = PHASE62 / "phase62c_c0_a1_results.json"
    p_path = PHASE62 / "phase62p_h62p1_results.json"
    cc = json.loads(c_path.read_text(encoding="utf-8"))
    pp = json.loads(p_path.read_text(encoding="utf-8"))
    folds_c = [set(row["test_leaves"]) for row in cc["folds"]]
    folds_p = [set(row["test_leaves"]) for row in pp["folds"]]
    if len(folds_c) != 5 or folds_c != folds_p:
        raise RuntimeError("Phase62C/Phase62P physical-leaf fold authority mismatch")
    if any(not fold for fold in folds_c):
        raise RuntimeError("empty committed Phase62 fold")
    union = set().union(*folds_c)
    if sum(len(x) for x in folds_c) != len(union):
        raise RuntimeError("committed Phase62 fold leaves overlap")
    return folds_c


def leaf_items(paragraphs: Sequence[q.NativeParagraph], leaves: Iterable[int], include: bool) -> List[b.Item]:
    return q.items(q.leaf_subset(paragraphs, leaves, include))


def training_context(paragraphs: Sequence[q.NativeParagraph], test_leaves: Set[int]) -> dict:
    train = leaf_items(paragraphs, test_leaves, include=False)
    test = leaf_items(paragraphs, test_leaves, include=True)
    sd = b.training_sd(train)
    dtrain = b.contrasts(train, sd)
    if len(dtrain) == 0:
        raise RuntimeError("no training S1 contrasts")
    direction = np.mean(dtrain, axis=0)
    norm = float(np.linalg.norm(direction))
    if norm == 0:
        raise RuntimeError("zero training S1 direction")
    direction /= norm
    projection, n_items, mean_delta = b.s1_projection(test, sd, direction)
    if projection is None:
        raise RuntimeError("held-out S1 projection unavailable")
    return {
        "train": train,
        "test": test,
        "sd": sd,
        "direction": direction,
        "projection": float(projection),
        "n_heldout_s1_items": n_items,
        "heldout_mean_delta8": mean_delta,
    }


def observational_view(
    source: str,
    view: str,
    paragraphs: Sequence[q.NativeParagraph],
    zl_paragraphs: Sequence[q.NativeParagraph],
    folds: Sequence[Set[int]],
) -> dict:
    fold_rows = []
    for fi, test_leaves in enumerate(folds):
        ctx = training_context(paragraphs, test_leaves)
        prof = p.raw_profile(ctx["test"], f"Phase63B:{source}:{view}:fold{fi}")
        zl_items = leaf_items(zl_paragraphs, test_leaves, include=True)
        zl_prof = p.raw_profile(zl_items, f"Phase63B:ZL3b:{view}:fold{fi}")
        fold_rows.append({
            "fold": fi,
            "test_leaves": sorted(test_leaves),
            "R1_real_minus_pseudo_projection": ctx["projection"],
            "R1_n_heldout_s1_items": ctx["n_heldout_s1_items"],
            "R1_heldout_mean_delta8": ctx["heldout_mean_delta8"],
            "R2_H62P1": prof,
            "R2_C_short": float(prof["C_short"]),
            "R2_D_profile_to_ZL_same_parser_view": p.profile_distance(prof, zl_prof),
            "ZL_same_parser_view_H62P1": zl_prof,
        })
    projections = [row["R1_real_minus_pseudo_projection"] for row in fold_rows]
    cshorts = [row["R2_C_short"] for row in fold_rows]
    return {
        "source": source,
        "view": view,
        "folds": fold_rows,
        "R1": {
            "positive_folds": sum(x > 0 for x in projections),
            "mean_projection": float(np.mean(projections)),
            "median_projection": float(statistics.median(projections)),
            "fold_values": projections,
        },
        "R2": {
            "positive_C_short_folds": sum(x > 0 for x in cshorts),
            "mean_C_short": float(np.mean(cshorts)),
            "median_C_short": float(statistics.median(cshorts)),
            "fold_values": cshorts,
            "mean_D_profile_to_ZL_same_parser_view": float(np.mean([
                row["R2_D_profile_to_ZL_same_parser_view"] for row in fold_rows
            ])),
        },
    }


def metric_triplet(items: Sequence[b.Item], sd: np.ndarray, direction: np.ndarray, s2: dict, s3: dict) -> dict:
    s1, n, delta = b.s1_projection(items, sd, direction)
    if s1 is None:
        raise RuntimeError("control S1 unavailable")
    return {
        "S1": float(s1),
        "S2": float(s2["excess"]),
        "S3": float(s3["mean_eta2"]),
        "S1_n_items": n,
        "S1_mean_delta8": delta,
    }


def aggregate_triplets(per_ms: Dict[str, dict]) -> dict:
    return {
        k: float(np.mean([row[k] for row in per_ms.values()]))
        for k in ("S1", "S2", "S3")
    }


def latin_controls(cremma_root: Path) -> dict:
    commit = b.verify_cremma_commit(cremma_root)
    raw = {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }
    c0 = {name: c.transform_items(items, FIXED_C0) for name, items in raw.items()}
    n0_static = {
        name: {"S2": b.s2_locality(items, f"N0:{name}"), "S3": b.s3_line_position(items)}
        for name, items in raw.items()
    }
    c0_static = {
        name: {"S2": b.s2_locality(items, f"C0:{FIXED_C0}:{name}"), "S3": b.s3_line_position(items)}
        for name, items in c0.items()
    }

    n0_prof_ms = {name: p.raw_profile(items, f"N0:{name}") for name, items in raw.items()}
    c0_prof_ms = {name: p.raw_profile(items, f"C0:{FIXED_C0}:{name}") for name, items in c0.items()}
    n0_prof = p.aggregate_excess(n0_prof_ms, "N0:equal-manuscript", "manuscript")
    c0_prof = p.aggregate_excess(c0_prof_ms, f"C0:{FIXED_C0}:equal-manuscript", "manuscript")
    return {
        "commit": commit,
        "raw": raw,
        "c0": c0,
        "n0_static": n0_static,
        "c0_static": c0_static,
        "n0_profile": n0_prof,
        "c0_profile": c0_prof,
        "n0_profile_per_manuscript": n0_prof_ms,
        "c0_profile_per_manuscript": c0_prof_ms,
    }


def ratio(model: float, target: float):
    if target <= EPS:
        return None
    return float(model / target)


def strict_wins(a: Sequence[float], bvals: Sequence[float]) -> int:
    if len(a) != len(bvals):
        raise RuntimeError("fold arrays differ in length")
    return sum(x + EPS < y for x, y in zip(a, bvals))


def it_full_transfer_view(
    view: str,
    it_paragraphs: Sequence[q.NativeParagraph],
    folds: Sequence[Set[int]],
    controls: dict,
    it_observational: dict,
) -> dict:
    p61 = c.load_phase61_module()
    fold_rows = []

    for fi, test_leaves in enumerate(folds):
        ctx = training_context(it_paragraphs, test_leaves)
        sd = ctx["sd"]
        direction = ctx["direction"]
        target_items = ctx["test"]

        target_s2 = b.s2_locality(target_items, f"Phase63B:IT2a:{view}:target-S2:fold{fi}")
        target_s3 = b.s3_line_position(target_items)
        target = {
            "S1": ctx["projection"],
            "S2": float(target_s2["excess"]),
            "S3": float(target_s3["mean_eta2"]),
        }
        target_profile = it_observational["folds"][fi]["R2_H62P1"]

        n0_per = {
            name: metric_triplet(items, sd, direction, controls["n0_static"][name]["S2"], controls["n0_static"][name]["S3"])
            for name, items in controls["raw"].items()
        }
        c0_per = {
            name: metric_triplet(items, sd, direction, controls["c0_static"][name]["S2"], controls["c0_static"][name]["S3"])
            for name, items in controls["c0"].items()
        }
        n0_exposed = aggregate_triplets(n0_per)
        c0_exposed = aggregate_triplets(c0_per)

        native_train = q.leaf_subset(it_paragraphs, test_leaves, include=False)
        native_test = q.leaf_subset(it_paragraphs, test_leaves, include=True)
        p61_train = q.to_phase61_paragraphs(native_train, p61)
        p61_test = q.to_phase61_paragraphs(native_test, p61)
        train_vocab = sorted(set(p61.all_tokens(p61_train)))
        if not train_vocab:
            raise RuntimeError(f"IT {view} fold {fi}: empty training vocabulary")
        train_vocab_set = set(train_vocab)
        neighbors = p61.build_neighbors(train_vocab)
        tuple_neighbors = {tuple(k): {tuple(x) for x in vals} for k, vals in neighbors.items()}
        shape_scores = p61.learn_shape_scores(p61_train, train_vocab)
        strength, local_p = c.A1_PARAMS[fi]
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
                raise RuntimeError(f"IT {view} fold {fi} rep {r}: generated type outside training vocabulary")
            gitems = c.convert_p61_paragraphs(generated)
            g_s1, _, _ = b.s1_projection(gitems, sd, direction)
            if g_s1 is None:
                raise RuntimeError(f"IT {view} fold {fi} rep {r}: generated S1 unavailable")
            s2_label = f"Phase63B:IT2a:{view}:A1-S2:fold{fi}:rep{r}"
            g_s2 = c.s2_with_prebuilt_neighbors(gitems, s2_label, tuple_neighbors)
            g_s3 = b.s3_line_position(gitems)
            exposed_reps.append({
                "S1": float(g_s1),
                "S2": float(g_s2["excess"]),
                "S3": float(g_s3["mean_eta2"]),
            })
            profile_label = f"Phase63B:IT2a:{view}:A1-H62P1:fold{fi}:rep{r}"
            profile_reps[f"rep{r}"] = p.raw_profile(gitems, profile_label)
            generation_audit.append({
                "replicate": r,
                "seed": seed,
                "generated_token_occurrences": len(generated_tokens),
                "generated_types": len(set(generated_tokens)),
                "types_outside_training_vocabulary": 0,
            })

        a1_exposed = {
            k: float(np.mean([row[k] for row in exposed_reps]))
            for k in ("S1", "S2", "S3")
        }
        a1_profile = p.aggregate_excess(
            profile_reps,
            f"Phase63B:IT2a:{view}:A1:fold{fi}:mean-E",
            "generator realization",
        )
        profiles = {
            "N0": controls["n0_profile"],
            "C0": controls["c0_profile"],
            "A1_R1": a1_profile,
        }
        comparisons = {
            name: {
                "D_profile": p.profile_distance(prof, target_profile),
                "abs_C_short_diff": p.c_short_diff(prof, target_profile),
            }
            for name, prof in profiles.items()
        }

        fold_rows.append({
            "fold": fi,
            "test_leaves": sorted(test_leaves),
            "target_exposed": target,
            "target_S2_detail": target_s2,
            "target_S3_detail": target_s3,
            "target_H62P1": target_profile,
            "N0_exposed_equal_manuscript": n0_exposed,
            "C0_fixed_digraph_exposed_equal_manuscript": c0_exposed,
            "A1_R1_frozen_parameters": {"entry_strength": strength, "local_family_p": local_p},
            "A1_R1_training_vocabulary_types": len(train_vocab),
            "A1_R1_generation_audit": generation_audit,
            "A1_R1_exposed_replicates": exposed_reps,
            "A1_R1_exposed_mean": a1_exposed,
            "A1_R1_H62P1_replicates": profile_reps,
            "A1_R1_H62P1_profile": a1_profile,
            "H62P1_candidate_profiles": profiles,
            "H62P1_comparisons": comparisons,
        })

    target_mean = {
        k: float(np.mean([row["target_exposed"][k] for row in fold_rows]))
        for k in ("S1", "S2", "S3")
    }
    a1_mean = {
        k: float(np.mean([row["A1_R1_exposed_mean"][k] for row in fold_rows]))
        for k in ("S1", "S2", "S3")
    }
    ratios = {k: ratio(a1_mean[k], target_mean[k]) for k in ("S1", "S2", "S3")}
    scalar_passes = {k: (ratios[k] is not None and 0.5 <= ratios[k] <= 2.0) for k in ratios}

    comp_summary = {}
    for cand in ("N0", "C0", "A1_R1"):
        ds = [row["H62P1_comparisons"][cand]["D_profile"] for row in fold_rows]
        cs = [row["H62P1_comparisons"][cand]["abs_C_short_diff"] for row in fold_rows]
        comp_summary[cand] = {
            "mean_D_profile": float(np.mean(ds)),
            "median_D_profile": float(statistics.median(ds)),
            "mean_abs_C_short_diff": float(np.mean(cs)),
            "D_profile_fold_values": ds,
            "abs_C_short_diff_fold_values": cs,
        }

    a_d = comp_summary["A1_R1"]["D_profile_fold_values"]
    a_c = comp_summary["A1_R1"]["abs_C_short_diff_fold_values"]
    wins = {}
    for baseline in ("N0", "C0"):
        b_d = comp_summary[baseline]["D_profile_fold_values"]
        b_c = comp_summary[baseline]["abs_C_short_diff_fold_values"]
        wins[baseline] = {
            "D_profile_wins": strict_wins(a_d, b_d),
            "abs_C_short_diff_wins": strict_wins(a_c, b_c),
        }

    lower_means = {
        baseline: {
            "lower_mean_D_profile": comp_summary["A1_R1"]["mean_D_profile"] + EPS < comp_summary[baseline]["mean_D_profile"],
            "lower_mean_abs_C_short_diff": comp_summary["A1_R1"]["mean_abs_C_short_diff"] + EPS < comp_summary[baseline]["mean_abs_C_short_diff"],
        }
        for baseline in ("N0", "C0")
    }
    primary_criterion = (
        all(scalar_passes.values())
        and all(v["lower_mean_D_profile"] and v["lower_mean_abs_C_short_diff"] for v in lower_means.values())
        and all(v["D_profile_wins"] >= 3 and v["abs_C_short_diff_wins"] >= 3 for v in wins.values())
    )
    return {
        "view": view,
        "folds": fold_rows,
        "across_fold": {
            "IT_target_exposed_mean": target_mean,
            "A1_R1_exposed_mean": a1_mean,
            "A1_R1_ratio_of_means_to_IT": ratios,
            "A1_R1_scalar_gate_0.5_to_2.0": scalar_passes,
            "H62P1_candidate_summaries": comp_summary,
            "A1_R1_lower_mean_errors_vs_baselines": lower_means,
            "A1_R1_fold_wins_vs_baselines": wins,
            "frozen_IT_R3_criterion_pass": bool(primary_criterion),
        },
    }


def criterion_observational(w1: dict, w2: dict) -> dict:
    r1 = (
        w1["R1"]["positive_folds"] >= 4
        and w1["R1"]["mean_projection"] > 0
        and w2["R1"]["mean_projection"] > 0
    )
    r2 = (
        w1["R2"]["positive_C_short_folds"] >= 4
        and w1["R2"]["mean_C_short"] > 0
        and w2["R2"]["mean_C_short"] > 0
    )
    return {
        "R1_pass": bool(r1),
        "R2_pass": bool(r2),
        "W2_R1_mean_sign_reversal": bool(w1["R1"]["mean_projection"] > 0 and w2["R1"]["mean_projection"] <= 0),
        "W2_R2_mean_sign_reversal": bool(w1["R2"]["mean_C_short"] > 0 and w2["R2"]["mean_C_short"] <= 0),
    }


def main() -> int:
    if len(sys.argv) != 5:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt GC2a-n.txt IT2a-n.txt /path/to/CREMMA-Medieval-LAT", file=sys.stderr)
        return 2

    paths = {
        "ZL3b": Path(sys.argv[1]).resolve(),
        "GC2a": Path(sys.argv[2]).resolve(),
        "IT2a": Path(sys.argv[3]).resolve(),
    }
    cremma_root = Path(sys.argv[4]).resolve()

    # Source identity and B1 preflight firewall before any scientific metric.
    parsed: Dict[str, Dict[str, Sequence[q.NativeParagraph]]] = {s: {} for s in SOURCES}
    audits: dict = {s: {} for s in SOURCES}
    for source in SOURCES:
        for view in VIEWS:
            pars, audit = q.parse_ivtff(paths[source], source, view)
            parsed[source][view] = pars
            audits[source][view] = audit
    preflight = assert_preflight(parsed, audits)

    folds = committed_folds()
    fold_union = set().union(*folds)
    for source in SOURCES:
        for view in VIEWS:
            represented = {par.leaf for par in parsed[source][view] if par.leaf is not None}
            missing = sorted(fold_union - represented)
            if missing:
                raise RuntimeError(f"{source} {view}: committed fold leaves absent: {missing}")

    controls = latin_controls(cremma_root)

    observations: Dict[str, Dict[str, dict]] = {"GC2a": {}, "IT2a": {}}
    for source in ("GC2a", "IT2a"):
        for view in VIEWS:
            observations[source][view] = observational_view(
                source,
                view,
                parsed[source][view],
                parsed["ZL3b"][view],
                folds,
            )

    obs_criteria = {
        source: criterion_observational(observations[source]["W1"], observations[source]["W2"])
        for source in ("GC2a", "IT2a")
    }

    it_r3 = {
        view: it_full_transfer_view(
            view,
            parsed["IT2a"][view],
            folds,
            controls,
            observations["IT2a"][view],
        )
        for view in VIEWS
    }

    gc_obs_pass = obs_criteria["GC2a"]["R1_pass"] and obs_criteria["GC2a"]["R2_pass"]
    it_obs_pass = obs_criteria["IT2a"]["R1_pass"] and obs_criteria["IT2a"]["R2_pass"]
    it_r3_w1_pass = it_r3["W1"]["across_fold"]["frozen_IT_R3_criterion_pass"]
    it_r3_w2_pass = it_r3["W2"]["across_fold"]["frozen_IT_R3_criterion_pass"]
    strong = bool(gc_obs_pass and it_obs_pass and it_r3_w1_pass)

    if strong:
        interpretation = (
            "STRONG REPLICATION — GC independent-alphabet observational effects and IT independent-reading observational/full A1-R1 transfer pass the frozen W1 criteria without W2 observational sign reversal"
        )
    elif gc_obs_pass and it_obs_pass and not it_r3_w1_pass:
        interpretation = (
            "PARTIAL REPLICATION — observational structure is transcription-robust in GC/IT, but frozen A1-R1 does not satisfy the full IT transfer criterion"
        )
    elif it_obs_pass and it_r3_w1_pass and not gc_obs_pass:
        interpretation = (
            "EVA-LINEAGE DEPENDENCE WARNING — IT replication passes but primary independent-alphabet GC observational replication fails"
        )
    elif not gc_obs_pass:
        interpretation = (
            "PRIMARY REPLICATION FAILURE — at least one frozen GC observational criterion fails; current strongest mechanism narrative is materially transcription/representation dependent in tested form"
        )
    else:
        interpretation = "MIXED PHASE63B REPLICATION — frozen criteria do not support a strong-replication classification"

    out = {
        "phase": "63B",
        "scientific_question": "independent transcription/segmentation robustness of entry specialization, recurrence geometry, and frozen A1-R1 transfer",
        "scope_firewall": "no A2/C1/M0, no cross-alphabet mapping, no retuning, fixed C0-4 digraph, W1 primary plus frozen W2 sensitivity",
        "inputs": {
            "source_identity": {source: audits[source]["W1"]["source_identity"] for source in SOURCES},
            "cremma_commit": controls["commit"],
            "folds": [sorted(x) for x in folds],
            "A1_frozen_parameters": {
                str(fi): {"entry_strength": vals[0], "local_family_p": vals[1]}
                for fi, vals in c.A1_PARAMS.items()
            },
            "A1_replicates_per_fold": A1_REPS,
            "H62P1_null_reps": p.NULL_REPS,
            "fixed_C0": FIXED_C0,
        },
        "preflight_identity_verified_before_science": preflight,
        "observational_replication": observations,
        "observational_frozen_criteria": obs_criteria,
        "IT_full_A1_R1_transfer": it_r3,
        "across_phase63B": {
            "GC_R1_R2_pass": bool(gc_obs_pass),
            "IT_R1_R2_pass": bool(it_obs_pass),
            "IT_R3_W1_primary_pass": bool(it_r3_w1_pass),
            "IT_R3_W2_sensitivity_pass": bool(it_r3_w2_pass),
            "strong_replication": strong,
            "interpretation": interpretation,
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
