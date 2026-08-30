#!/usr/bin/env python3
"""Phase62C: frozen C0 transform family + frozen Phase61C A1 rescoring.

This executable implements PLAN.md + IMPLEMENTATION_C.md.
It intentionally contains no implementation of the sealed prospective H62-P1
statistic and does not introduce C1, A2, or M0.

Usage:
  python experiments/phase62/phase62c_c0_a1.py /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
import statistics
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

import phase62b_n0 as b

TRANSFORMS = ("C0-0_identity", "C0-1_reverse", "C0-2_allography2", "C0-3_allography3", "C0-4_digraph")
A1_PARAMS = {
    0: (0.5, 0.20),
    1: (0.5, 0.20),
    2: (0.5, 0.30),
    3: (0.5, 0.30),
    4: (0.5, 0.20),
}
REL_EPS = 1e-9
COMPAT_TOL = 1e-6
A1_REPS = 5


def load_phase61_module():
    path = Path(__file__).resolve().parent.parent / "phase61" / "phase61c_joint_model.py"
    spec = importlib.util.spec_from_file_location("phase61c_frozen", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load frozen Phase61C module: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def encoded_atom(tag: str, units: Sequence[str]) -> str:
    # Length-delimited exact source strings make this injective without relying
    # on a separator absent from medieval Unicode transcription.
    return tag + "".join(f"{len(x)}:{x}" for x in units)


def transform_token(tok: b.Token, name: str) -> b.Token:
    if name == "C0-0_identity":
        return tok
    if name == "C0-1_reverse":
        return tuple(reversed(tok))
    if name == "C0-2_allography2":
        return tuple(encoded_atom("A2I" if i == 0 else "A2N", [u]) for i, u in enumerate(tok))
    if name == "C0-3_allography3":
        out = []
        L = len(tok)
        for i, u in enumerate(tok):
            if i == 0:
                cls = "A3I"
            elif i == L - 1:
                cls = "A3F"
            else:
                cls = "A3M"
            out.append(encoded_atom(cls, [u]))
        return tuple(out)
    if name == "C0-4_digraph":
        out = []
        i = 0
        while i < len(tok):
            if i + 1 < len(tok):
                out.append(encoded_atom("D", [tok[i], tok[i + 1]]))
                i += 2
            else:
                out.append(encoded_atom("S", [tok[i]]))
                i += 1
        return tuple(out)
    raise ValueError(name)


def transform_items(items: Sequence[b.Item], name: str) -> List[b.Item]:
    return [
        b.Item(
            item_id=it.item_id,
            document=it.document,
            leaf=it.leaf,
            lines=[[transform_token(tok, name) for tok in line] for line in it.lines],
        )
        for it in items
    ]


def metric_triplet(items: Sequence[b.Item], sd: np.ndarray, direction: np.ndarray, s2: dict, s3: dict) -> dict:
    s1, n, delta = b.s1_projection(items, sd, direction)
    return {
        "S1": s1,
        "S2": s2["excess"],
        "S3": s3["mean_eta2"],
        "S1_n_items": n,
        "S1_mean_delta8": delta,
    }


def aggregate(per_ms: Dict[str, dict]) -> dict:
    return {
        k: float(np.mean([v[k] for v in per_ms.values() if v[k] is not None]))
        for k in ("S1", "S2", "S3")
    }


def rel_mse(model: dict, target: dict) -> float:
    vals = []
    for k in ("S1", "S2", "S3"):
        den = max(abs(target[k]), REL_EPS)
        vals.append(((model[k] - target[k]) / den) ** 2)
    return float(np.mean(vals))


def ratio(model: float, target: float) -> Optional[float]:
    if target <= REL_EPS:
        return None
    return model / target


def static_metrics(items: Sequence[b.Item], label: str, s2_override: Optional[dict] = None) -> dict:
    return {
        "S2": s2_override if s2_override is not None else b.s2_locality(items, label),
        "S3": b.s3_line_position(items),
    }


def s2_with_prebuilt_neighbors(items: Sequence[b.Item], label: str, neighbors: Dict[b.Token, set]) -> dict:
    """Exact Phase62B S2 algorithm with a prebuilt superset neighbor map."""
    lines = b.included_lines(items)
    pooled = [t for line in lines for t in line]
    observed = b.local_prev10(lines, neighbors)
    counts = [len(line) for line in lines]
    nulls = []
    base_seed = b.stable_seed(f"phase62b:S2:{label}")
    for r in range(b.NULL_REPS):
        shuffled = list(pooled)
        random.Random(base_seed + r).shuffle(shuffled)
        made = []
        k = 0
        for c in counts:
            made.append(shuffled[k:k + c])
            k += c
        nulls.append(b.local_prev10(made, neighbors))
    med = float(statistics.median(nulls)) if nulls else 0.0
    arr = np.array(nulls, dtype=float)
    return {
        "observed": float(observed),
        "null_median": med,
        "null_q025": float(np.quantile(arr, 0.025)) if len(arr) else 0.0,
        "null_q975": float(np.quantile(arr, 0.975)) if len(arr) else 0.0,
        "excess": float(observed - med),
        "n_lines": len(lines),
        "n_tokens": len(pooled),
        "n_types": len(set(pooled)),
        "null_reps": b.NULL_REPS,
    }


def convert_p61_paragraphs(paragraphs) -> List[b.Item]:
    return [
        b.Item(
            item_id=f"{p.page}:p{p.pid}",
            document=p.page,
            leaf=p.leaf,
            lines=[[tuple(tok) for tok in line] for line in p.lines],
        )
        for p in paragraphs
    ]


def avg_triplets(values: Sequence[dict]) -> dict:
    return {k: float(np.mean([v[k] for v in values])) for k in ("S1", "S2", "S3")}


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT", file=sys.stderr)
        return 2

    voynich_path = Path(sys.argv[1]).resolve()
    cremma_root = Path(sys.argv[2]).resolve()

    # Reuse Phase62B frozen input checks.
    vdata = voynich_path.read_bytes()
    vblob = b.git_blob_sha1(vdata)
    if vblob != b.EXPECTED_ZL3B_BLOB:
        raise RuntimeError(f"ZL3b blob mismatch: {vblob}")
    ccommit = b.verify_cremma_commit(cremma_root)

    vitems = b.parse_voynich(voynich_path)
    folds = b.physical_leaf_folds(vitems)
    primary_raw = {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }

    # ---------- Phase62B N0 compatibility stage: no fresh C0/A1 outcome yet ----------
    identity_static = {
        name: static_metrics(items, f"N0:{name}")
        for name, items in primary_raw.items()
    }
    contexts = []
    n0_fold_means = []
    for fi, test_leaves in enumerate(folds):
        train = b.by_leaves(vitems, test_leaves, include=False)
        test = b.by_leaves(vitems, test_leaves, include=True)
        sd = b.training_sd(train)
        dtrain = b.contrasts(train, sd)
        direction = np.mean(dtrain, axis=0)
        norm = float(np.linalg.norm(direction))
        if norm == 0:
            raise RuntimeError(f"fold {fi}: zero direction")
        direction /= norm

        train_s1, _, _ = b.s1_projection(train, sd, direction)
        train_s2 = b.s2_locality(train, f"Voynich:trainfold{fi}")
        train_s3 = b.s3_line_position(train)
        train_target = {"S1": train_s1, "S2": train_s2["excess"], "S3": train_s3["mean_eta2"]}

        test_s1, _, _ = b.s1_projection(test, sd, direction)
        test_s2 = b.s2_locality(test, f"Voynich:fold{fi}")
        test_s3 = b.s3_line_position(test)
        heldout = {"S1": test_s1, "S2": test_s2["excess"], "S3": test_s3["mean_eta2"]}

        n0_per = {}
        for name, items in primary_raw.items():
            n0_per[name] = metric_triplet(items, sd, direction, identity_static[name]["S2"], identity_static[name]["S3"])
        n0 = aggregate(n0_per)
        n0_fold_means.append(n0)
        contexts.append({
            "fold": fi,
            "test_leaves": test_leaves,
            "train": train,
            "test": test,
            "sd": sd,
            "direction": direction,
            "train_target": train_target,
            "heldout": heldout,
            "n0_per": n0_per,
            "n0": n0,
        })

    committed = json.loads((Path(__file__).resolve().parent / "phase62b_n0_results.json").read_text(encoding="utf-8"))
    recomputed_n0 = {k: float(np.mean([x[k] for x in n0_fold_means])) for k in ("S1", "S2", "S3")}
    reference_n0 = committed["across_fold"]["N0_equal_manuscript_mean"]
    compatibility = {
        k: abs(recomputed_n0[k] - reference_n0[k]) / max(abs(reference_n0[k]), REL_EPS)
        for k in ("S1", "S2", "S3")
    }
    if any(v > COMPAT_TOL for v in compatibility.values()):
        print(json.dumps({
            "phase": "62C",
            "scientific_status": "NO PHASE62C VERDICT — Phase62B compatibility failed",
            "recomputed_N0": recomputed_n0,
            "reference_N0": reference_n0,
            "relative_discrepancy": compatibility,
        }, indent=2))
        return 4

    # ---------- C0 static candidate preparation after compatibility passes ----------
    transformed = {t: {name: transform_items(items, t) for name, items in primary_raw.items()} for t in TRANSFORMS}
    static = {t: {} for t in TRANSFORMS}
    for t in TRANSFORMS:
        for name, items in transformed[t].items():
            if t == "C0-0_identity":
                static[t][name] = identity_static[name]
            elif t == "C0-1_reverse":
                # Token reversal preserves Levenshtein distance and token order,
                # so S2 is exactly invariant; reuse the identity null result.
                static[t][name] = static_metrics(items, f"C0:{t}:{name}", s2_override=identity_static[name]["S2"])
            else:
                static[t][name] = static_metrics(items, f"C0:{t}:{name}")

    # ---------- Frozen Phase61 A1 setup ----------
    p61 = load_phase61_module()
    p61_paragraphs, _ = p61.parse(str(voynich_path))
    p61_folds = p61.physical_leaf_folds(p61_paragraphs)
    if [sorted(x) for x in p61_folds] != [sorted(x) for x in folds]:
        raise RuntimeError("Phase61/Phase62 physical-leaf folds differ")
    p61_vocab = sorted(set(p61.all_tokens(p61_paragraphs)))
    p61_neighbors = p61.build_neighbors(p61_vocab)
    phase62_neighbor_superset = {
        tuple(k): {tuple(x) for x in vals}
        for k, vals in p61_neighbors.items()
    }

    results = []
    c0_improved_folds = 0
    lomo_improvement_counts = {name: 0 for name in b.PRIMARY_MANUSCRIPTS}

    for ctx in contexts:
        fi = ctx["fold"]
        sd = ctx["sd"]
        direction = ctx["direction"]
        train_target = ctx["train_target"]
        heldout = ctx["heldout"]

        candidates = []
        candidate_per_ms = {}
        for t in TRANSFORMS:
            per = {}
            for name, items in transformed[t].items():
                per[name] = metric_triplet(items, sd, direction, static[t][name]["S2"], static[t][name]["S3"])
            agg = aggregate(per)
            candidates.append({"transform": t, "training_metrics": agg, "training_joint_relative_mse": rel_mse(agg, train_target)})
            candidate_per_ms[t] = per
        candidates.sort(key=lambda x: (x["training_joint_relative_mse"], TRANSFORMS.index(x["transform"])))
        chosen = candidates[0]["transform"]
        c0_per = candidate_per_ms[chosen]
        c0 = aggregate(c0_per)

        n0 = ctx["n0"]
        n0_err = rel_mse(n0, heldout)
        c0_err = rel_mse(c0, heldout)
        if c0_err < n0_err:
            c0_improved_folds += 1

        lomo = {}
        for omitted in b.PRIMARY_MANUSCRIPTS:
            n0_kept = {k: v for k, v in ctx["n0_per"].items() if k != omitted}
            c0_kept = {k: v for k, v in c0_per.items() if k != omitted}
            n0_l = aggregate(n0_kept)
            c0_l = aggregate(c0_kept)
            n0_l_err = rel_mse(n0_l, heldout)
            c0_l_err = rel_mse(c0_l, heldout)
            if c0_l_err < n0_l_err:
                lomo_improvement_counts[omitted] += 1
            lomo[omitted] = {
                "N0": n0_l,
                "C0": c0_l,
                "N0_joint_relative_mse": n0_l_err,
                "C0_joint_relative_mse": c0_l_err,
            }

        # Frozen A1 parameters and exact Phase61 generator/seeds.
        strength, local_p = A1_PARAMS[fi]
        p61_train = p61.subset(p61_paragraphs, ctx["test_leaves"], include=False)
        p61_test = p61.subset(p61_paragraphs, ctx["test_leaves"], include=True)
        shape_scores = p61.learn_shape_scores(p61_train, p61_vocab)
        entry_cum = p61.entry_cumulative(p61_vocab, shape_scores, strength)
        a1_reps = []
        for r in range(A1_REPS):
            seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10 + r
            generated = p61.generate_layout(p61_test, p61_vocab, p61_neighbors, entry_cum, local_p, seed)
            gitems = convert_p61_paragraphs(generated)
            g_s1, _, _ = b.s1_projection(gitems, sd, direction)
            g_s2 = s2_with_prebuilt_neighbors(gitems, f"A1:fold{fi}:rep{r}", phase62_neighbor_superset)
            g_s3 = b.s3_line_position(gitems)
            a1_reps.append({"S1": g_s1, "S2": g_s2["excess"], "S3": g_s3["mean_eta2"]})
        a1 = avg_triplets(a1_reps)

        results.append({
            "fold": fi,
            "test_leaves": sorted(ctx["test_leaves"]),
            "training_voynich": train_target,
            "heldout_voynich": heldout,
            "N0": n0,
            "N0_joint_relative_mse": n0_err,
            "C0_candidates_training": candidates,
            "C0_selected": chosen,
            "C0": c0,
            "C0_joint_relative_mse": c0_err,
            "C0_improves_N0_heldout": c0_err < n0_err,
            "C0_leave_one_manuscript_out": lomo,
            "A1_frozen_parameters": {"entry_strength": strength, "local_family_p": local_p},
            "A1_replicates": a1_reps,
            "A1": a1,
            "A1_joint_relative_mse": rel_mse(a1, heldout),
            "ratios_to_heldout_voynich": {
                "N0": {k: ratio(n0[k], heldout[k]) for k in ("S1", "S2", "S3")},
                "C0": {k: ratio(c0[k], heldout[k]) for k in ("S1", "S2", "S3")},
                "A1": {k: ratio(a1[k], heldout[k]) for k in ("S1", "S2", "S3")},
            },
        })

    target_mean = {k: float(np.mean([x["heldout_voynich"][k] for x in results])) for k in ("S1", "S2", "S3")}
    n0_mean = {k: float(np.mean([x["N0"][k] for x in results])) for k in ("S1", "S2", "S3")}
    c0_mean = {k: float(np.mean([x["C0"][k] for x in results])) for k in ("S1", "S2", "S3")}
    a1_mean = {k: float(np.mean([x["A1"][k] for x in results])) for k in ("S1", "S2", "S3")}

    c0_ratios = {k: ratio(c0_mean[k], target_mean[k]) for k in ("S1", "S2", "S3")}
    a1_ratios = {k: ratio(a1_mean[k], target_mean[k]) for k in ("S1", "S2", "S3")}
    c0_broad = {k: c0_ratios[k] is not None and 0.5 <= c0_ratios[k] <= 2.0 for k in c0_ratios}
    a1_broad = {k: a1_ratios[k] is not None and 0.5 <= a1_ratios[k] <= 2.0 for k in a1_ratios}

    mean_n0_err = float(np.mean([x["N0_joint_relative_mse"] for x in results]))
    mean_c0_err = float(np.mean([x["C0_joint_relative_mse"] for x in results]))
    lomo_majority_conditions = sum(count >= 3 for count in lomo_improvement_counts.values())
    c0_material = (
        c0_improved_folds >= 3
        and mean_c0_err < mean_n0_err
        and lomo_majority_conditions >= 3
    )
    a1_competitive = all(a1_broad.values())

    out = {
        "phase": "62C",
        "scope_firewall": "C0 + frozen A1 common-score evaluation only; no H62-P1/C1/A2/M0",
        "compatibility": {
            "recomputed_N0": recomputed_n0,
            "reference_Phase62B_N0": reference_n0,
            "relative_discrepancy": compatibility,
            "pass": True,
        },
        "inputs": {
            "voynich_git_blob_sha1": vblob,
            "cremma_commit": ccommit,
            "C0_transforms": list(TRANSFORMS),
            "A1_frozen_parameters": {str(k): {"entry_strength": v[0], "local_family_p": v[1]} for k, v in A1_PARAMS.items()},
            "A1_empirical_vocabulary_types": len(p61_vocab),
        },
        "folds": results,
        "across_fold": {
            "voynich_mean": target_mean,
            "N0_mean": n0_mean,
            "C0_selected_mean": c0_mean,
            "A1_frozen_mean": a1_mean,
            "C0_ratio_of_means_to_voynich": c0_ratios,
            "A1_ratio_of_means_to_voynich": a1_ratios,
            "C0_broad_regime_0.5_to_2.0": c0_broad,
            "A1_broad_regime_0.5_to_2.0": a1_broad,
            "N0_mean_joint_relative_mse": mean_n0_err,
            "C0_mean_joint_relative_mse": mean_c0_err,
            "C0_improved_heldout_folds": c0_improved_folds,
            "C0_LOMO_fold_improvement_counts": lomo_improvement_counts,
            "C0_LOMO_conditions_with_majority_improvement": lomo_majority_conditions,
            "C0_materially_improves_N0_under_frozen_rule": c0_material,
            "A1_materially_competitive_under_frozen_common_score_rule": a1_competitive,
            "selected_C0_by_fold": {str(x["fold"]): x["C0_selected"] for x in results},
        },
        "complexity_dependence": {
            "N0": {
                "voynich_boundary_mechanisms": 0,
                "voynich_selected_parameters": 0,
                "target_vocabulary": False,
                "plaintext": True,
            },
            "C0": {
                "voynich_boundary_mechanisms": 0,
                "searched_transform_alternatives": 5,
                "voynich_derived_mapping_or_codebook": False,
                "reversible_to_source_plaintext": True,
            },
            "A1": {
                "voynich_boundary_mechanisms": 1,
                "local_family_mechanisms": 1,
                "max_local_memory_tokens": 10,
                "empirical_voynich_vocabulary_supplied": True,
                "empirical_vocabulary_types": len(p61_vocab),
                "meaningful_plaintext_candidate": False,
            },
        },
        "phase62c_decisions": {
            "C0_material_explanatory_improvement_over_N0": c0_material,
            "A1_common_score_competitive": a1_competitive,
            "next": "Phase62D must freeze the exposed-score structural ranking or unresolved set before the sealed prospective H62-P1 is evaluated.",
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
