#!/usr/bin/env python3
"""Phase62P: preregistered H62-P1 near-family recurrence-distance profile.

Chronology requirement:
- Phase62D exposed-score ranking must already be committed.
- This executable must be committed before any H62-P1 Voynich value is run.

Usage:
  python experiments/phase62/phase62p_h62p1.py /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np

import phase62b_n0 as b
import phase62c_c0_a1 as c


BINS: Tuple[Tuple[str, int, int], ...] = (
    ("B1", 1, 2),
    ("B2", 3, 5),
    ("B3", 6, 10),
    ("B4", 11, 20),
    ("B5", 21, 40),
)
NULL_REPS = 100
A1_REPS = 5
TIE_EPS = 1e-12


class MissingBin(RuntimeError):
    pass


def flatten_item(item: b.Item) -> List[b.Token]:
    return [tok for line in item.lines for tok in line]


def eligible_sequences(items: Sequence[b.Item]) -> List[Tuple[str, List[b.Token]]]:
    return [
        (it.item_id, flatten_item(it))
        for it in items
        if b.base_eligible(it)
    ]


def bin_rates(
    sequences: Sequence[Tuple[str, Sequence[b.Token]]],
    neighbors: Dict[b.Token, Set[b.Token]],
) -> Tuple[List[float], List[int], List[int]]:
    hits = [0] * len(BINS)
    available = [0] * len(BINS)
    for _item_id, seq in sequences:
        for i, tok in enumerate(seq):
            nb = neighbors.get(tok, set())
            for bi, (_name, lo, hi) in enumerate(BINS):
                if i < hi:
                    continue
                available[bi] += 1
                if any(seq[i - d] in nb for d in range(lo, hi + 1)):
                    hits[bi] += 1
    if any(n == 0 for n in available):
        missing = [BINS[i][0] for i, n in enumerate(available) if n == 0]
        raise MissingBin(f"zero eligible observations in bins: {missing}")
    rates = [hits[i] / available[i] for i in range(len(BINS))]
    return rates, hits, available


def normalize_excess(excess: Sequence[float]) -> dict:
    denom = float(sum(abs(x) for x in excess))
    if denom <= 0:
        return {
            "valid": False,
            "abs_excess_sum": denom,
            "profile": None,
            "C_short": None,
        }
    p = [float(x / denom) for x in excess]
    c_short = float(sum(excess[:3]) / denom)
    return {
        "valid": True,
        "abs_excess_sum": denom,
        "profile": p,
        "C_short": c_short,
    }


def raw_profile(items: Sequence[b.Item], label: str) -> dict:
    sequences = eligible_sequences(items)
    if not sequences:
        raise MissingBin(f"{label}: no base-eligible items")
    vocab = {tok for _item_id, seq in sequences for tok in seq}
    neighbors = b.build_neighbors(vocab)
    try:
        observed, observed_hits, available = bin_rates(sequences, neighbors)
    except MissingBin as exc:
        raise MissingBin(f"{label}: {exc}") from exc

    null_rows: List[List[float]] = []
    base_seed = b.stable_seed(f"phase62p:H62P1:{label}")
    for r in range(NULL_REPS):
        rng = random.Random(base_seed + r)
        shuffled: List[Tuple[str, List[b.Token]]] = []
        for item_id, seq in sequences:
            row = list(seq)
            rng.shuffle(row)
            shuffled.append((item_id, row))
        rates, _hits, null_available = bin_rates(shuffled, neighbors)
        if null_available != available:
            raise RuntimeError(f"{label}: null availability changed")
        null_rows.append(rates)

    arr = np.array(null_rows, dtype=float)
    med = np.median(arr, axis=0)
    q025 = np.quantile(arr, 0.025, axis=0)
    q975 = np.quantile(arr, 0.975, axis=0)
    excess = [float(observed[i] - med[i]) for i in range(len(BINS))]
    norm = normalize_excess(excess)
    return {
        "label": label,
        "n_items": len(sequences),
        "n_tokens": int(sum(len(seq) for _item_id, seq in sequences)),
        "n_types": len(vocab),
        "bins": [x[0] for x in BINS],
        "available_occurrences": available,
        "observed_hits": observed_hits,
        "observed": [float(x) for x in observed],
        "null_median": [float(x) for x in med],
        "null_q025": [float(x) for x in q025],
        "null_q975": [float(x) for x in q975],
        "excess": excess,
        "null_reps": NULL_REPS,
        **norm,
    }


def aggregate_excess(profiles: Dict[str, dict], label: str, aggregation_unit: str) -> dict:
    if not profiles:
        raise RuntimeError(f"{label}: no profiles to aggregate")
    for name, prof in profiles.items():
        if not prof.get("valid"):
            raise RuntimeError(f"{label}: invalid source profile {name}")
    excess = [
        float(np.mean([prof["excess"][i] for prof in profiles.values()]))
        for i in range(len(BINS))
    ]
    norm = normalize_excess(excess)
    if not norm["valid"]:
        raise RuntimeError(f"{label}: aggregate excess has zero L1 mass")
    return {
        "label": label,
        "aggregation_unit": aggregation_unit,
        "members": sorted(profiles),
        "n_members": len(profiles),
        "excess": excess,
        **norm,
    }


def profile_distance(candidate: dict, target: dict) -> float:
    if not candidate.get("valid") or not target.get("valid"):
        raise RuntimeError("profile distance requires valid normalized profiles")
    return float(sum(abs(a - v) for a, v in zip(candidate["profile"], target["profile"])))


def c_short_diff(candidate: dict, target: dict) -> float:
    if candidate.get("C_short") is None or target.get("C_short") is None:
        raise RuntimeError("C_short difference requires valid profiles")
    return float(abs(candidate["C_short"] - target["C_short"]))


def unique_lowest(values: Dict[str, float]) -> Optional[str]:
    best = min(values.values())
    winners = [k for k, v in values.items() if abs(v - best) <= TIE_EPS]
    return winners[0] if len(winners) == 1 else None


def candidate_summary(folds: Sequence[dict], candidate: str) -> dict:
    ds = [f["comparisons"][candidate]["D_profile"] for f in folds]
    cs = [f["comparisons"][candidate]["abs_C_short_diff"] for f in folds]
    return {
        "mean_D_profile": float(np.mean(ds)),
        "median_D_profile": float(statistics.median(ds)),
        "mean_abs_C_short_diff": float(np.mean(cs)),
        "D_profile_fold_values": ds,
        "abs_C_short_diff_fold_values": cs,
    }


def pairwise_wins(folds: Sequence[dict], a: str, bname: str, metric: str) -> int:
    return sum(
        f["comparisons"][a][metric] + TIE_EPS < f["comparisons"][bname][metric]
        for f in folds
    )


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT", file=sys.stderr)
        return 2

    here = Path(__file__).resolve().parent
    decision_path = here / "DECISION_D.md"
    if not decision_path.is_file():
        raise RuntimeError("Phase62D decision freeze missing; H62-P1 reveal forbidden")
    decision_blob = b.git_blob_sha1(decision_path.read_bytes())

    voynich_path = Path(sys.argv[1]).resolve()
    cremma_root = Path(sys.argv[2]).resolve()
    vblob = b.git_blob_sha1(voynich_path.read_bytes())
    if vblob != b.EXPECTED_ZL3B_BLOB:
        raise RuntimeError(f"ZL3b blob mismatch: {vblob} != {b.EXPECTED_ZL3B_BLOB}")
    ccommit = b.verify_cremma_commit(cremma_root)

    phase62c_path = here / "phase62c_c0_a1_results.json"
    phase62c = json.loads(phase62c_path.read_text(encoding="utf-8"))
    selected_c0 = {
        int(k): v
        for k, v in phase62c["across_fold"]["selected_C0_by_fold"].items()
    }
    if set(selected_c0) != set(range(5)):
        raise RuntimeError("Phase62C selected-transform map is incomplete")
    for fi, pair in c.A1_PARAMS.items():
        recorded = phase62c["inputs"]["A1_frozen_parameters"][str(fi)]
        if abs(recorded["entry_strength"] - pair[0]) > TIE_EPS or abs(recorded["local_family_p"] - pair[1]) > TIE_EPS:
            raise RuntimeError(f"A1 parameter mismatch in fold {fi}")

    vitems = b.parse_voynich(voynich_path)
    folds = b.physical_leaf_folds(vitems)
    if len(folds) != 5:
        raise RuntimeError(f"expected five physical-leaf folds, got {len(folds)}")

    primary_raw = {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }

    # N0: compute manuscript profiles first, then equal-weight excess vectors.
    n0_per_ms: Dict[str, dict] = {}
    try:
        for name, items in primary_raw.items():
            n0_per_ms[name] = raw_profile(items, f"N0:{name}")
    except MissingBin as exc:
        print(json.dumps({
            "phase": "62P",
            "scientific_status": "NO H62-P1 VERDICT — frozen missing-bin rule triggered",
            "error": str(exc),
        }, ensure_ascii=False, indent=2))
        return 5
    n0_profile = aggregate_excess(n0_per_ms, "N0:equal-manuscript", "manuscript")

    # C0: only transforms already selected in Phase62C are eligible for this reveal.
    c0_profiles_by_transform: Dict[str, dict] = {}
    c0_per_ms_by_transform: Dict[str, Dict[str, dict]] = {}
    try:
        for transform in sorted(set(selected_c0.values())):
            if transform not in c.TRANSFORMS:
                raise RuntimeError(f"unknown committed C0 transform: {transform}")
            per_ms = {}
            for name, items in primary_raw.items():
                transformed = c.transform_items(items, transform)
                per_ms[name] = raw_profile(transformed, f"C0:{transform}:{name}")
            c0_per_ms_by_transform[transform] = per_ms
            c0_profiles_by_transform[transform] = aggregate_excess(
                per_ms,
                f"C0:{transform}:equal-manuscript",
                "manuscript",
            )
    except MissingBin as exc:
        print(json.dumps({
            "phase": "62P",
            "scientific_status": "NO H62-P1 VERDICT — frozen missing-bin rule triggered",
            "error": str(exc),
        }, ensure_ascii=False, indent=2))
        return 5

    # Frozen A1 setup. No parameter selection occurs here.
    p61 = c.load_phase61_module()
    p61_paragraphs, _ = p61.parse(str(voynich_path))
    p61_folds = p61.physical_leaf_folds(p61_paragraphs)
    if [sorted(x) for x in p61_folds] != [sorted(x) for x in folds]:
        raise RuntimeError("Phase61 and Phase62 physical-leaf folds differ")
    p61_vocab = sorted(set(p61.all_tokens(p61_paragraphs)))
    p61_neighbors = p61.build_neighbors(p61_vocab)
    if len(p61_vocab) != phase62c["inputs"]["A1_empirical_vocabulary_types"]:
        raise RuntimeError("A1 empirical vocabulary size differs from Phase62C")

    fold_results = []
    try:
        for fi, test_leaves in enumerate(folds):
            heldout_items = b.by_leaves(vitems, test_leaves, include=True)
            vprof = raw_profile(heldout_items, f"Voynich:fold{fi}")

            transform = selected_c0[fi]
            c0prof = c0_profiles_by_transform[transform]

            strength, local_p = c.A1_PARAMS[fi]
            p61_train = p61.subset(p61_paragraphs, test_leaves, include=False)
            p61_test = p61.subset(p61_paragraphs, test_leaves, include=True)
            shape_scores = p61.learn_shape_scores(p61_train, p61_vocab)
            entry_cum = p61.entry_cumulative(p61_vocab, shape_scores, strength)

            a1_rep_profiles: Dict[str, dict] = {}
            for r in range(A1_REPS):
                seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10 + r
                generated = p61.generate_layout(
                    p61_test,
                    p61_vocab,
                    p61_neighbors,
                    entry_cum,
                    local_p,
                    seed,
                )
                gitems = c.convert_p61_paragraphs(generated)
                a1_rep_profiles[f"rep{r}"] = raw_profile(gitems, f"A1:fold{fi}:rep{r}")
            a1prof = aggregate_excess(a1_rep_profiles, f"A1:fold{fi}:mean-E", "generator realization")

            candidate_profiles = {
                "N0": n0_profile,
                "C0": c0prof,
                "A1": a1prof,
            }
            comparisons = {
                name: {
                    "D_profile": profile_distance(prof, vprof),
                    "abs_C_short_diff": c_short_diff(prof, vprof),
                }
                for name, prof in candidate_profiles.items()
            }
            d_winner = unique_lowest({k: v["D_profile"] for k, v in comparisons.items()})
            c_winner = unique_lowest({k: v["abs_C_short_diff"] for k, v in comparisons.items()})

            fold_results.append({
                "fold": fi,
                "test_leaves": sorted(test_leaves),
                "voynich": vprof,
                "C0_selected_from_Phase62C": transform,
                "A1_frozen_parameters": {
                    "entry_strength": strength,
                    "local_family_p": local_p,
                },
                "A1_realizations": a1_rep_profiles,
                "A1_fold_profile": a1prof,
                "candidate_profiles": {
                    "N0": n0_profile,
                    "C0": c0prof,
                    "A1": a1prof,
                },
                "comparisons": comparisons,
                "unique_D_profile_winner": d_winner,
                "unique_abs_C_short_diff_winner": c_winner,
            })
    except MissingBin as exc:
        print(json.dumps({
            "phase": "62P",
            "scientific_status": "NO H62-P1 VERDICT — frozen missing-bin rule triggered",
            "error": str(exc),
        }, ensure_ascii=False, indent=2))
        return 5

    candidates = ("N0", "C0", "A1")
    summaries = {name: candidate_summary(fold_results, name) for name in candidates}
    d_wins = {name: sum(f["unique_D_profile_winner"] == name for f in fold_results) for name in candidates}
    c_wins = {name: sum(f["unique_abs_C_short_diff_winner"] == name for f in fold_results) for name in candidates}
    for name in candidates:
        summaries[name]["unique_D_profile_fold_wins"] = d_wins[name]
        summaries[name]["unique_abs_C_short_diff_fold_wins"] = c_wins[name]

    lowest_mean_d = unique_lowest({name: summaries[name]["mean_D_profile"] for name in candidates})
    lowest_median_d = unique_lowest({name: summaries[name]["median_D_profile"] for name in candidates})
    lowest_mean_c = unique_lowest({name: summaries[name]["mean_abs_C_short_diff"] for name in candidates})

    leader = None
    for name in candidates:
        if (
            lowest_mean_d == name
            and lowest_median_d == name
            and d_wins[name] >= 3
            and lowest_mean_c == name
            and c_wins[name] >= 3
        ):
            leader = name
            break

    pairwise_against_a1 = {}
    for competitor in ("N0", "C0"):
        pairwise_against_a1[competitor] = {
            "D_profile_fold_wins_vs_A1": pairwise_wins(fold_results, competitor, "A1", "D_profile"),
            "abs_C_short_diff_fold_wins_vs_A1": pairwise_wins(fold_results, competitor, "A1", "abs_C_short_diff"),
            "lower_mean_D_profile_than_A1": summaries[competitor]["mean_D_profile"] + TIE_EPS < summaries["A1"]["mean_D_profile"],
            "lower_mean_abs_C_short_diff_than_A1": summaries[competitor]["mean_abs_C_short_diff"] + TIE_EPS < summaries["A1"]["mean_abs_C_short_diff"],
        }

    contradiction_by = None
    for competitor, q in pairwise_against_a1.items():
        if (
            q["lower_mean_D_profile_than_A1"]
            and q["lower_mean_abs_C_short_diff_than_A1"]
            and q["D_profile_fold_wins_vs_A1"] >= 3
            and q["abs_C_short_diff_fold_wins_vs_A1"] >= 3
        ):
            contradiction_by = competitor
            break

    if leader == "A1":
        a1_interpretation = "PROSPECTIVE SUPPORT — A1 is the frozen H62-P1 profile leader among tested candidates"
    elif contradiction_by is not None:
        a1_interpretation = f"PROSPECTIVE CONTRADICTION — {contradiction_by} beats A1 under the frozen two-metric/fold-majority rule"
    else:
        a1_interpretation = "INCONCLUSIVE FOR A1 — no frozen-rule prospective support or competitor contradiction"

    out = {
        "phase": "62P",
        "hypothesis": "H62-P1 near-family recurrence-distance profile",
        "scientific_status": "H62-P1 prospective reveal complete",
        "chronology": {
            "phase62d_decision_present": True,
            "phase62d_decision_git_blob_sha1": decision_blob,
            "implementation_freeze_files": [
                "experiments/phase62/IMPLEMENTATION_P.md",
                "experiments/phase62/IMPLEMENTATION_P_EDGE_CASES.md",
                "experiments/phase62/phase62p_h62p1.py",
            ],
        },
        "inputs": {
            "voynich_git_blob_sha1": vblob,
            "cremma_commit": ccommit,
            "phase62c_selected_C0_by_fold": {str(k): v for k, v in selected_c0.items()},
            "A1_frozen_parameters": {
                str(k): {"entry_strength": v[0], "local_family_p": v[1]}
                for k, v in c.A1_PARAMS.items()
            },
            "A1_empirical_vocabulary_types": len(p61_vocab),
            "bins": [{"name": name, "lo": lo, "hi": hi} for name, lo, hi in BINS],
            "null_reps": NULL_REPS,
        },
        "N0_per_manuscript": n0_per_ms,
        "N0_equal_manuscript_profile": n0_profile,
        "C0_per_manuscript_by_selected_transform": c0_per_ms_by_transform,
        "C0_equal_manuscript_profiles_by_selected_transform": c0_profiles_by_transform,
        "folds": fold_results,
        "across_fold": {
            "candidate_summaries": summaries,
            "unique_lowest_mean_D_profile": lowest_mean_d,
            "unique_lowest_median_D_profile": lowest_median_d,
            "unique_lowest_mean_abs_C_short_diff": lowest_mean_c,
            "prospective_profile_leader": leader,
            "pairwise_competitors_vs_A1": pairwise_against_a1,
            "A1_prospective_interpretation": a1_interpretation,
        },
        "firewall": {
            "A2_introduced": False,
            "C1_introduced": False,
            "M0_introduced": False,
            "replacement_holdout_used": False,
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
