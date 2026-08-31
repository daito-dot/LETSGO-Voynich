#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve()
STABILITY_DIR = HERE.parents[1] / "occupancy-graph-stability"
sys.path.insert(0, str(STABILITY_DIR))
import phase58b_graph_stability as b

N_REF = 1000
N_TEST = 1000
N_SLOTS = 12
N_FOLDS = 5
PAIRS = b.PAIRS
N_EDGES = len(PAIRS)
GROUPS = ("ALL", "AH", "BH", "BB", "BS", "initial", "interior", "final")
TARGET_GROUPS = ("AH", "BH", "BB", "BS", "initial", "interior", "final")
CONTRASTS = b.CONTRASTS
REFERENCE_NS = "Issue58C:ResidualGraph:Reference:LineSlotOccupancyShuffle:v1"
TEST_NS = "Issue58C:ResidualGraph:Test:LineSlotOccupancyShuffle:v1"
MAX_REFERENCE_NS = "Issue58C:ResidualGraph:MaxSensitivityReference:v1"


def finite(x):
    return x is not None and math.isfinite(float(x))


def summary(xs):
    a = np.asarray(xs, dtype=float)
    if a.size == 0:
        return None
    return {
        "min": float(np.min(a)),
        "median": float(np.median(a)),
        "q95": float(np.quantile(a, 0.95)),
        "max": float(np.max(a)),
    }


def group_fold_counts(d, X):
    code = b.pair_codes(X)
    fold = d["token_folds"].astype(np.int64)

    all_counts = b.partition_counts(code, fold, N_FOLDS, True)

    meta_ids = np.where(d["meta_id"] >= 0, d["meta_id"].astype(np.int64) * N_FOLDS + fold, -1)
    meta_counts = b.partition_counts(code, meta_ids, len(b.META_GROUPS) * N_FOLDS, True)
    meta_counts = meta_counts.reshape(len(b.META_GROUPS), N_FOLDS, N_EDGES, 11, 2, 2)

    pos_ids = np.where(d["pos_id"] >= 0, d["pos_id"].astype(np.int64) * N_FOLDS + fold, -1)
    pos_counts = b.partition_counts(code, pos_ids, len(b.POSITION_GROUPS) * N_FOLDS, True)
    pos_counts = pos_counts.reshape(len(b.POSITION_GROUPS), N_FOLDS, N_EDGES, 11, 2, 2)

    out = {"ALL": all_counts}
    out.update({name: meta_counts[idx] for name, idx in b.META_INDEX.items()})
    out.update({name: pos_counts[idx] for name, idx in b.POSITION_INDEX.items()})
    return out


def q_views(d, X, include_folds=True):
    counts = group_fold_counts(d, X)
    out = {}
    for name in GROUPS:
        cf = counts[name]
        total = cf.sum(axis=0)
        item = {"full": b.q_cond(total)}
        if include_folds:
            held = np.stack([b.q_cond(cf[f]) for f in range(N_FOLDS)])
            train = np.stack([b.q_cond(total - cf[f]) for f in range(N_FOLDS)])
            item["train"] = train
            item["held"] = held
        out[name] = item
    return out


def shuffled_flat(d, namespace, null_index):
    rng = np.random.default_rng(b.e.stable_seed(f"{namespace}:{null_index}"))
    keys = rng.random(d["padded"].shape)
    keys[~d["line_mask"]] = 2.0
    order = np.argsort(keys, axis=1, kind="stable")
    shuffled = np.take_along_axis(d["padded"], order, axis=1)
    shuffled[~d["line_mask"]] = 0
    if null_index == 0 and not np.array_equal(d["padded"].sum(axis=1), shuffled.sum(axis=1)):
        raise RuntimeError(f"null failed line x slot marginal preservation: {namespace}")
    return shuffled[d["line_mask"]]


def allocate_reference():
    return {
        name: {
            "full": np.empty((N_REF, N_EDGES), dtype=np.float64),
            "train": np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64),
            "held": np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64),
        }
        for name in GROUPS
    }


def build_reference(d, namespace, progress_label):
    ref = allocate_reference()
    for n in range(N_REF):
        Y = shuffled_flat(d, namespace, n)
        qv = q_views(d, Y, include_folds=True)
        for name in GROUPS:
            for view in ("full", "train", "held"):
                ref[name][view][n] = qv[name][view]
        if (n + 1) % 100 == 0:
            print(f"{progress_label} {n+1}/{N_REF}", file=sys.stderr, flush=True)
    return ref


def sorted_reference(ref):
    return {
        name: {view: np.sort(values, axis=0) for view, values in views.items()}
        for name, views in ref.items()
    }


def normal_score_array(q, sorted_ref):
    q = np.asarray(q, dtype=np.float64)
    sr = np.asarray(sorted_ref, dtype=np.float64)
    if sr.shape[0] != N_REF or sr.shape[1:] != q.shape:
        raise RuntimeError(f"reference shape mismatch: ref={sr.shape}, q={q.shape}")
    flat_q = q.reshape(-1)
    flat_sr = sr.reshape(N_REF, -1)
    u = np.empty(len(flat_q), dtype=np.float64)
    for j, val in enumerate(flat_q):
        col = flat_sr[:, j]
        left = int(np.searchsorted(col, val, side="left"))
        right = int(np.searchsorted(col, val, side="right"))
        eq = right - left
        u[j] = (0.5 + left + 0.5 * eq) / (N_REF + 1.0)
    return norm.ppf(u).reshape(q.shape)


def residual_views(real_q, sref):
    out = {}
    for name in GROUPS:
        out[name] = {
            view: normal_score_array(real_q[name][view], sref[name][view])
            for view in ("full", "train", "held")
        }
    return out


def residual_energy(z):
    z = np.asarray(z, dtype=np.float64)
    return float(np.sqrt(np.mean(z * z)))


def real_metrics(zv):
    energies = {name: residual_energy(zv[name]["full"]) for name in GROUPS}
    within = {}
    for name in GROUPS:
        vals = [b.corr(zv[name]["train"][f], zv[name]["held"][f]) for f in range(N_FOLDS)]
        within[name] = {"fold_correlations": vals, "median": b.med(vals)}

    contrasts = {}
    for label, s, t, family in CONTRASTS:
        st = [b.corr(zv[s]["train"][f], zv[t]["held"][f]) for f in range(N_FOLDS)]
        ts = [b.corr(zv[t]["train"][f], zv[s]["held"][f]) for f in range(N_FOLDS)]
        contrasts[label] = {
            "source": s,
            "target": t,
            "family": family,
            "pearson_full": b.corr(zv[s]["full"], zv[t]["full"]),
            "source_to_target_fold": st,
            "source_to_target_median": b.med(st),
            "target_to_source_fold": ts,
            "target_to_source_median": b.med(ts),
        }
    return energies, within, contrasts


def run_test_nulls(d, sref):
    pooled_energy = np.empty(N_TEST, dtype=np.float64)
    group_energy_max = np.empty(N_TEST, dtype=np.float64)
    contrast_r_max = np.empty(N_TEST, dtype=np.float64)
    for n in range(N_TEST):
        Y = shuffled_flat(d, TEST_NS, n)
        qv = q_views(d, Y, include_folds=False)
        zfull = {
            name: normal_score_array(qv[name]["full"], sref[name]["full"])
            for name in GROUPS
        }
        pooled_energy[n] = residual_energy(zfull["ALL"])
        group_energy_max[n] = max(residual_energy(zfull[name]) for name in TARGET_GROUPS)
        rs = []
        for _, s, t, _ in CONTRASTS:
            r = b.corr(zfull[s], zfull[t])
            rs.append(-1.0 if r is None else float(r))
        contrast_r_max[n] = max(rs)
        if (n + 1) % 100 == 0:
            print(f"Issue58C test null {n+1}/{N_TEST}", file=sys.stderr, flush=True)
    return pooled_energy, group_energy_max, contrast_r_max


def empirical_upper_p(real_value, null_values):
    return float((1 + int(np.sum(np.asarray(null_values) >= float(real_value)))) / (len(null_values) + 1))


def group_eligibility(energies, within, group_energy_max):
    out = {}
    for name in TARGET_GROUPS:
        p = empirical_upper_p(energies[name], group_energy_max)
        w = within[name]["median"]
        out[name] = {
            "energy": energies[name],
            "p_E_maxT": p,
            "within_reliability": w,
            "supported_residual_existence": bool(p <= 0.01 and finite(w) and float(w) >= 0.50),
        }
    return out


def classify_contrasts(contrasts, eligibility, contrast_r_max):
    out = {}
    for label, s, t, family in CONTRASTS:
        c = contrasts[label]
        r = c["pearson_full"]
        p = None if r is None else empirical_upper_p(r, contrast_r_max)
        xs = c["source_to_target_median"]
        xt = c["target_to_source_median"]
        ws = eligibility[s]["within_reliability"]
        wt = eligibility[t]["within_reliability"]
        eligible = eligibility[s]["supported_residual_existence"] and eligibility[t]["supported_residual_existence"]

        if not eligible:
            cls = "INCONCLUSIVE_RESIDUAL_BASIS"
        elif any(not finite(v) for v in (r, p, xs, xt, ws, wt)):
            cls = "INCONCLUSIVE_RESIDUAL_STABILITY"
        elif (
            float(r) >= 0.70
            and float(p) <= 0.01
            and float(xs) >= max(0.60, float(wt) - 0.15)
            and float(xt) >= max(0.60, float(ws) - 0.15)
        ):
            cls = "STABLE_RESIDUAL"
        elif float(r) < 0.40 or float(xs) < 0.30 or float(xt) < 0.30:
            cls = "DIFFERENT_RESIDUAL_OR_MIXTURE"
        elif float(r) >= 0.40 and float(p) <= 0.01 and float(xs) >= 0.30 and float(xt) >= 0.30:
            cls = "RELATED_RESIDUAL_BUT_MODULATED"
        else:
            cls = "INCONCLUSIVE_RESIDUAL_STABILITY"

        out[label] = {
            **c,
            "p_R_maxT": p,
            "source_residual_supported": eligibility[s]["supported_residual_existence"],
            "target_residual_supported": eligibility[t]["supported_residual_existence"],
            "classification": cls,
        }
    return out


def family_classifications(classified):
    reg_labels = [label for label, _, _, fam in CONTRASTS if fam == "register_section"]
    pos_labels = [label for label, _, _, fam in CONTRASTS if fam == "position"]

    def family(labels, stable_name, mod_name, diff_name, inc_name):
        cs = [classified[x]["classification"] for x in labels]
        if all(x == "STABLE_RESIDUAL" for x in cs):
            return stable_name
        if any(x == "DIFFERENT_RESIDUAL_OR_MIXTURE" for x in cs):
            return diff_name
        if all(x in ("STABLE_RESIDUAL", "RELATED_RESIDUAL_BUT_MODULATED") for x in cs) and any(
            x == "RELATED_RESIDUAL_BUT_MODULATED" for x in cs
        ):
            return mod_name
        return inc_name

    reg = family(
        reg_labels,
        "REGISTER/SECTION SHARED RESIDUAL GRAPH",
        "REGISTER/SECTION RESIDUAL MODULATION",
        "REGISTER/SECTION MULTIPLE/HIERARCHICAL RESIDUAL GRAMMARS",
        "REGISTER/SECTION RESIDUAL STABILITY INCONCLUSIVE",
    )
    pos = family(
        pos_labels,
        "LINE-POSITION STABLE RESIDUAL GRAPH",
        "LINE-POSITION RESIDUAL MODULATION",
        "LINE-POSITION MATERIALLY CHANGES RESIDUAL GRAPH",
        "LINE-POSITION RESIDUAL STABILITY INCONCLUSIVE",
    )
    return reg, pos


def overall_classification(p_exist_all, w_all, reg, pos):
    if p_exist_all > 0.01:
        return "NO DETECTABLE RESIDUAL GRAPH BEYOND LOWER-ORDER OCCUPANCY ARCHITECTURE"
    if not finite(w_all) or float(w_all) < 0.50:
        return "RESIDUAL TOKEN-CONSTRUCTION RESULT INCONCLUSIVE"
    if reg == "REGISTER/SECTION MULTIPLE/HIERARCHICAL RESIDUAL GRAMMARS" or pos == "LINE-POSITION MATERIALLY CHANGES RESIDUAL GRAPH":
        return "MULTIPLE/HIERARCHICAL RESIDUAL TOKEN GRAMMARS"
    if reg == "REGISTER/SECTION SHARED RESIDUAL GRAPH" and pos == "LINE-POSITION STABLE RESIDUAL GRAPH":
        return "SHARED RESIDUAL TOKEN-CONSTRUCTION GRAPH"
    noninc_reg = reg in ("REGISTER/SECTION SHARED RESIDUAL GRAPH", "REGISTER/SECTION RESIDUAL MODULATION")
    noninc_pos = pos in ("LINE-POSITION STABLE RESIDUAL GRAPH", "LINE-POSITION RESIDUAL MODULATION")
    if noninc_reg and noninc_pos and ("MODULATION" in reg or "MODULATION" in pos):
        return "RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION"
    return "RESIDUAL TOKEN-CONSTRUCTION RESULT INCONCLUSIVE"


def max_sensitivity(path):
    parser = b.e.SlotParser()
    d = b.build_dataset(path, parser, "max")
    support = b.validate_support(d)
    real_q = q_views(d, d["X"], include_folds=True)
    ref = build_reference(d, MAX_REFERENCE_NS, "Issue58C max reference")
    sref = sorted_reference(ref)
    zv = residual_views(real_q, sref)
    energies, within, contrasts = real_metrics(zv)
    return {
        "namespace": MAX_REFERENCE_NS,
        "n_reference_nulls": N_REF,
        "population": {"visible_tokens": d["visible"], "parsed_tokens": d["parsed"], "group_support": support},
        "energies": energies,
        "within_reliability": within,
        "contrasts": contrasts,
    }


def self_test():
    refs = np.linspace(-1.0, 1.0, N_REF, dtype=float)[:, None]
    q = np.asarray([0.0])
    z = normal_score_array(q, refs)
    assert abs(float(z[0])) < 0.01

    tied = np.zeros((N_REF, 1), dtype=float)
    zt = normal_score_array(np.asarray([0.0]), tied)
    assert abs(float(zt[0])) < 1e-12
    zlo = normal_score_array(np.asarray([-1.0]), tied)
    zhi = normal_score_array(np.asarray([1.0]), tied)
    assert zlo[0] < 0 < zhi[0]

    a = np.asarray([1.0, -1.0, 1.0, -1.0])
    assert abs(residual_energy(a) - 1.0) < 1e-12

    assert REFERENCE_NS != TEST_NS != MAX_REFERENCE_NS
    assert len(PAIRS) == 66

    print(json.dumps({"self_test": "ok", "n_edges": N_EDGES, "n_ref": N_REF, "n_test": N_TEST}, sort_keys=True))


def main(path):
    parser = b.e.SlotParser()
    d = b.build_dataset(path, parser, "min")
    support = b.validate_support(d)

    real_q = q_views(d, d["X"], include_folds=True)
    ref = build_reference(d, REFERENCE_NS, "Issue58C reference null")
    sref = sorted_reference(ref)
    zv = residual_views(real_q, sref)
    energies, within, contrasts = real_metrics(zv)

    pooled_null, group_max_null, r_max_null = run_test_nulls(d, sref)
    p_exist_all = empirical_upper_p(energies["ALL"], pooled_null)
    eligibility = group_eligibility(energies, within, group_max_null)
    classified = classify_contrasts(contrasts, eligibility, r_max_null)
    reg, pos = family_classifications(classified)
    overall = overall_classification(p_exist_all, within["ALL"]["median"], reg, pos)

    result = {
        "phase": "Issue58C-null-residual-token-construction-graph",
        "target_reveal": True,
        "program_object": "internal construction of one space-delimited token; not sentence grammar; spaces not assumed linguistic word boundaries",
        "github_sha": os.environ.get("GITHUB_SHA"),
        "source": {
            "required_blob": b.EXPECTED_SOURCE_BLOB,
            "observed_blob": d["source_blob"],
        },
        "parser": {"primary_policy": "min", "n_slots": N_SLOTS},
        "population": {
            "visible_tokens": d["visible"],
            "parsed_tokens": d["parsed"],
            "group_support": support,
            "physical_leaf_folds": d["folds"],
        },
        "pairs": [list(map(int, p)) for p in PAIRS],
        "null_design": {
            "reference_namespace": REFERENCE_NS,
            "test_namespace": TEST_NS,
            "n_reference": N_REF,
            "n_test": N_TEST,
            "residual_transform": "reference empirical mid-rank normal score",
        },
        "real": {
            "q_full": {name: real_q[name]["full"].tolist() for name in GROUPS},
            "z_full": {name: zv[name]["full"].tolist() for name in GROUPS},
            "z_train": {name: zv[name]["train"].tolist() for name in GROUPS},
            "z_held": {name: zv[name]["held"].tolist() for name in GROUPS},
            "energies": energies,
            "within_reliability": within,
        },
        "primary_existence": {
            "E_ALL": energies["ALL"],
            "p_exist_ALL": p_exist_all,
            "W_ALL": within["ALL"]["median"],
            "existence_supported": bool(p_exist_all <= 0.01 and finite(within["ALL"]["median"]) and within["ALL"]["median"] >= 0.50),
        },
        "group_existence": eligibility,
        "contrasts": classified,
        "register_section_classification": reg,
        "position_classification": pos,
        "overall_classification": overall,
        "test_null": {
            "pooled_energy_values": pooled_null.tolist(),
            "pooled_energy_summary": summary(pooled_null),
            "group_energy_maxT_values": group_max_null.tolist(),
            "group_energy_maxT_summary": summary(group_max_null),
            "contrast_similarity_maxT_values": r_max_null.tolist(),
            "contrast_similarity_maxT_summary": summary(r_max_null),
        },
        "max_parser_sensitivity": max_sensitivity(path),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
    elif len(sys.argv) == 2:
        main(Path(sys.argv[1]))
    else:
        raise SystemExit(f"usage: {sys.argv[0]} SOURCE | --self-test")
