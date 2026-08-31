#!/usr/bin/env python3
"""Issue #58D preregistered independent-reading residual-graph replication.

PLAN_A.md is the frozen scientific authority and predates this executable.
The primary target is IT2a/Takahashi EvaT with the unchanged 12-slot parser.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
import math
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
sys.path.insert(0, str(EXPERIMENTS / "issue26-music"))
sys.path.insert(0, str(EXPERIMENTS / "occupancy-graph-stability"))
sys.path.insert(0, str(EXPERIMENTS / "occupancy-graph-residual"))
sys.path.insert(0, str(EXPERIMENTS / "phase63"))

import issue26e_core as e  # noqa: E402
import source_audit as sa  # noqa: E402
import phase58b_graph_stability as b  # noqa: E402
import phase58c_residual_graph as c  # noqa: E402
import phase63b_common as p63  # noqa: E402

N_REF = 1000
N_TEST = 1000
N_FOLDS = 5
GROUPS = c.GROUPS
TARGET_GROUPS = c.TARGET_GROUPS
CONTRASTS = c.CONTRASTS
PAIRS = c.PAIRS
REF_NS = "Issue58D:IT2a:ResidualGraph:Reference:LineSlotOccupancyShuffle:v1"
TEST_NS = "Issue58D:IT2a:ResidualGraph:Test:LineSlotOccupancyShuffle:v1"
MAX_REF_NS = "Issue58D:IT2a:ResidualGraph:MaxSensitivityReference:v1"
IT_SHA256 = "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"
IT_BLOB = "4d6d3f2537b1f507a257529b49c94af7d6e03446"
ZL_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
ZL_FIRST_REVEAL_SHA256 = "fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d"
SUPPORT_AUDIT_SHA256 = "35ea31eb5d0a1f0484623ee8a29058f1c5bc339117e378b594f26c7c23aee0dc"

STABLE_REFERENCE_LABELS = (
    "SECTION_B_vs_H",
    "SECTION_B_vs_S",
    "SECTION_H_vs_S",
    "POSITION_interior_vs_final",
)
MODULATED_REFERENCE_LABELS = (
    "CURRIER_H_A_vs_B",
    "POSITION_initial_vs_interior",
    "POSITION_initial_vs_final",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def finite(x) -> bool:
    return x is not None and math.isfinite(float(x))


def sign_agreement(a, d) -> int:
    a = np.asarray(a, dtype=float)
    d = np.asarray(d, dtype=float)
    if a.shape != d.shape:
        raise RuntimeError(f"sign-agreement shape mismatch: {a.shape} != {d.shape}")
    sa_ = np.sign(a)
    sd_ = np.sign(d)
    return int(np.sum((sa_ == sd_) & (sa_ != 0) & (sd_ != 0)))


def position_category(index: int, n_clean: int) -> str:
    if n_clean == 1:
        return "singleton"
    if index == 0:
        return "initial"
    if index == n_clean - 1:
        return "final"
    return "interior"


def frozen_folds_from_zl(zl_path: Path):
    raw = zl_path.read_bytes()
    blob = e.git_blob_sha1(raw)
    if blob != ZL_BLOB:
        raise RuntimeError(f"ZL blob mismatch: {blob} != {ZL_BLOB}")
    items = e.parse_voynich(zl_path)
    folds = [set(map(int, f)) for f in e.physical_leaf_folds(items)]
    if len(folds) != 5 or len(set().union(*folds)) != 99:
        raise RuntimeError("unexpected frozen ZL physical-leaf folds")
    return folds


def build_it_dataset(it_path: Path, zl_path: Path, policy: str):
    if policy not in ("min", "max"):
        raise RuntimeError(f"unknown parser policy: {policy}")
    source_id = p63.verify_source(it_path, "IT2a")
    if source_id["sha256"] != IT_SHA256 or source_id["git_blob_sha1"] != IT_BLOB:
        raise RuntimeError("IT2a source identity mismatch")
    paragraphs, audit = p63.parse_ivtff(it_path, "IT2a", "W1")
    pages, _ = sa.parse_page_metadata(it_path.read_text(encoding="utf-8-sig", errors="strict"))
    folds = frozen_folds_from_zl(zl_path)
    universe = set().union(*folds)
    leaf_to_fold = {int(leaf): fi for fi, leaves in enumerate(folds) for leaf in leaves}

    parser = e.SlotParser()
    e.validate_parser(parser)

    visible = parsed = 0
    lines = []
    clean_position = Counter()
    parsed_position = Counter()
    clean_group = Counter()
    parsed_group = Counter()

    for par in paragraphs:
        if par.leaf is None or int(par.leaf) not in universe:
            continue
        leaf = int(par.leaf)
        fold = int(leaf_to_fold[leaf])
        pm = pages.get(par.page, {})
        mg = b.meta_group(pm.get("L", sa.MISSING), pm.get("I", sa.MISSING))
        for line_index, token_units in enumerate(par.lines):
            clean = ["".join(tok) for tok in token_units]
            n_clean = len(clean)
            visible += n_clean
            rows = []
            positions = []
            for idx, tok in enumerate(clean):
                pos = position_category(idx, n_clean)
                clean_position[pos] += 1
                if mg:
                    clean_group[mg] += 1
                ps = parser.parses(tok)
                if not ps:
                    continue
                picked = ps[0] if policy == "min" else ps[-1]
                vals = picked[1]
                rows.append(np.fromiter((bool(vals[s]) for s in range(12)), dtype=np.uint8, count=12))
                positions.append(pos)
                parsed += 1
                parsed_position[pos] += 1
                if mg:
                    parsed_group[mg] += 1
            if rows:
                lines.append({
                    "leaf": leaf,
                    "fold": fold,
                    "page": par.page,
                    "paragraph": par.item_id,
                    "line_index": int(line_index),
                    "meta_group": mg,
                    "occ": np.stack(rows),
                    "positions": tuple(positions),
                })

    lines.sort(key=lambda x: (x["leaf"], x["page"], x["paragraph"], x["line_index"]))
    X = np.concatenate([x["occ"] for x in lines], axis=0)
    token_folds = np.concatenate([np.full(len(x["occ"]), x["fold"], np.int8) for x in lines])
    meta_id = np.concatenate([
        np.full(len(x["occ"]), b.META_INDEX.get(x["meta_group"], -1), np.int8)
        for x in lines
    ])
    pos_id = np.concatenate([
        np.asarray([b.POSITION_INDEX.get(p, -1) for p in x["positions"]], dtype=np.int8)
        for x in lines
    ])

    maxlen = max(len(x["occ"]) for x in lines)
    padded = np.zeros((len(lines), maxlen, 12), dtype=np.uint8)
    line_mask = np.zeros((len(lines), maxlen), dtype=bool)
    for ni, row in enumerate(lines):
        z = row["occ"]
        padded[ni, : len(z)] = z
        line_mask[ni, : len(z)] = True
    if not np.array_equal(padded[line_mask], X):
        raise RuntimeError("IT2a padded/flat ordering mismatch")

    return {
        "source_identity": source_id,
        "source_parser_audit": audit,
        "folds": [sorted(map(int, f)) for f in folds],
        "visible": int(visible),
        "parsed": int(parsed),
        "X": X,
        "token_folds": token_folds,
        "meta_id": meta_id,
        "pos_id": pos_id,
        "padded": padded,
        "line_mask": line_mask,
        "clean_position": dict(clean_position),
        "parsed_position": dict(parsed_position),
        "clean_group": dict(clean_group),
        "parsed_group": dict(parsed_group),
    }


def load_support_audit():
    path = HERE.parent / "source-audit" / "issue66_source_audit_support_complete.json"
    raw = path.read_bytes()
    got = sha256_bytes(raw)
    if got != SUPPORT_AUDIT_SHA256:
        raise RuntimeError(f"support-audit SHA mismatch: {got} != {SUPPORT_AUDIT_SHA256}")
    obj = json.loads(raw)
    if obj["scientific_pair_or_residual_metrics_computed"] is not False:
        raise RuntimeError("Stage-A firewall flag not false")
    if obj["IT2a"]["disposition"] != "AUTHORIZED_FOR_TARGET_PLAN":
        raise RuntimeError("IT2a not authorized by frozen Stage-A audit")
    return obj


def validate_population(d, support):
    it = support["IT2a"]
    if d["visible"] != it["population"]["clean_tokens"] or d["parsed"] != it["population"]["slot_parser_accepted_tokens"]:
        raise RuntimeError(f"IT population mismatch: {(d['visible'], d['parsed'])}")
    got_fold = [int(np.sum(d["token_folds"] == f)) for f in range(5)]
    exp_fold = it["shared_universe"]["fold_accepted_tokens"]
    if got_fold != exp_fold:
        raise RuntimeError(f"IT fold support mismatch: {got_fold} != {exp_fold}")

    group_fold = {}
    for name, idx in b.META_INDEX.items():
        vals = [int(np.sum((d["meta_id"] == idx) & (d["token_folds"] == f))) for f in range(5)]
        group_fold[name] = vals
        exp = it["metadata"]["accepted_token_support_by_group_fold"][name]
        if vals != exp:
            raise RuntimeError(f"IT group-fold support mismatch {name}: {vals} != {exp}")

    position_fold = {}
    for name, idx in b.POSITION_INDEX.items():
        vals = [int(np.sum((d["pos_id"] == idx) & (d["token_folds"] == f))) for f in range(5)]
        position_fold[name] = vals
        exp = it["token_position"]["accepted_by_fold"][name]
        if vals != exp:
            raise RuntimeError(f"IT position-fold support mismatch {name}: {vals} != {exp}")

    return {
        "fold_accepted_tokens": got_fold,
        "accepted_group_fold": group_fold,
        "accepted_position_fold": position_fold,
    }


def load_zl_first_reveal():
    root = EXPERIMENTS / "occupancy-graph-residual" / "first-reveal"
    parts = sorted(root.glob("issue64_residual_graph_results.json.gz.b64.part*"))
    if not parts:
        raise RuntimeError("missing #58C first-reveal archive parts")
    encoded = "".join("".join(p.read_text(encoding="ascii").split()) for p in parts)
    compressed = base64.b64decode(encoded, validate=True)
    raw = gzip.decompress(compressed)
    got = sha256_bytes(raw)
    if got != ZL_FIRST_REVEAL_SHA256:
        raise RuntimeError(f"#58C raw SHA mismatch: {got} != {ZL_FIRST_REVEAL_SHA256}")
    obj = json.loads(raw)
    if obj.get("overall_classification") != "RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION":
        raise RuntimeError("unexpected #58C frozen classification")
    if obj.get("pairs") != [list(map(int, p)) for p in PAIRS]:
        raise RuntimeError("#58C pair-order mismatch")
    zfull = obj.get("real", {}).get("z_full", {})
    for name in GROUPS:
        if name not in zfull or len(zfull[name]) != 66:
            raise RuntimeError(f"missing #58C z_full group {name}")
    return obj, {name: np.asarray(zfull[name], dtype=float) for name in GROUPS}, got


def delta_geometry_from_full(zfull):
    rs = {}
    for label, s, t, _ in CONTRASTS:
        r = b.corr(zfull[s], zfull[t])
        if r is None:
            raise RuntimeError(f"invalid geometry correlation {label}")
        rs[label] = float(r)
    core = float(np.median([rs[x] for x in STABLE_REFERENCE_LABELS]))
    mod = float(np.median([rs[x] for x in MODULATED_REFERENCE_LABELS]))
    return core, mod, core - mod, rs


def run_test_nulls(d, sref, zl_z):
    pooled_energy = np.empty(N_TEST, dtype=float)
    group_energy_max = np.empty(N_TEST, dtype=float)
    contrast_r_max = np.empty(N_TEST, dtype=float)
    cross_r_max = np.empty(N_TEST, dtype=float)
    cross_a_max = np.empty(N_TEST, dtype=float)
    delta_geometry = np.empty(N_TEST, dtype=float)

    for n in range(N_TEST):
        Y = c.shuffled_flat(d, TEST_NS, n)
        qv = c.q_views(d, Y, include_folds=False)
        zfull = {
            name: c.normal_score_array(qv[name]["full"], sref[name]["full"])
            for name in GROUPS
        }
        pooled_energy[n] = c.residual_energy(zfull["ALL"])
        group_energy_max[n] = max(c.residual_energy(zfull[name]) for name in TARGET_GROUPS)

        rs = []
        for _, s, t, _ in CONTRASTS:
            r = b.corr(zfull[s], zfull[t])
            if r is None:
                raise RuntimeError("invalid IT test-null within-reading correlation")
            rs.append(float(r))
        contrast_r_max[n] = max(rs)

        cr = []
        ca = []
        for name in GROUPS:
            r = b.corr(zl_z[name], zfull[name])
            if r is None:
                raise RuntimeError("invalid IT test-null cross-reading correlation")
            cr.append(float(r))
            ca.append(sign_agreement(zl_z[name], zfull[name]))
        cross_r_max[n] = max(cr)
        cross_a_max[n] = max(ca)

        core, mod, delta, _ = delta_geometry_from_full(zfull)
        delta_geometry[n] = delta

        if (n + 1) % 100 == 0:
            print(f"Issue58D test null {n+1}/{N_TEST}", file=sys.stderr, flush=True)

    return {
        "pooled_energy": pooled_energy,
        "group_energy_max": group_energy_max,
        "contrast_r_max": contrast_r_max,
        "cross_r_max": cross_r_max,
        "cross_a_max": cross_a_max,
        "delta_geometry": delta_geometry,
    }


def classify_cross_topology(zl_z, it_z, nulls):
    out = {}
    for name in GROUPS:
        r = b.corr(zl_z[name], it_z[name])
        if r is None:
            out[name] = {
                "pearson": None,
                "sign_agreement": None,
                "p_R_maxT": None,
                "p_A_maxT": None,
                "classification": "CROSS_READING_TOPOLOGY_INCONCLUSIVE",
            }
            continue
        a = sign_agreement(zl_z[name], it_z[name])
        pr = c.empirical_upper_p(r, nulls["cross_r_max"])
        pa = c.empirical_upper_p(a, nulls["cross_a_max"])
        if r >= 0.70 and pr <= 0.01 and a >= 50 and pa <= 0.01:
            cls = "CROSS_READING_TOPOLOGY_REPLICATED"
        elif r >= 0.40 and pr <= 0.05 and a >= 44 and pa <= 0.05:
            cls = "CROSS_READING_TOPOLOGY_RELATED_BUT_REPRESENTATION_MODULATED"
        elif r < 0.30 and a <= 39 and pr > 0.05 and pa > 0.05:
            cls = "CROSS_READING_TOPOLOGY_DIFFERENT"
        else:
            cls = "CROSS_READING_TOPOLOGY_INCONCLUSIVE"
        out[name] = {
            "pearson": float(r),
            "sign_agreement": int(a),
            "sign_denominator": 66,
            "p_R_maxT": float(pr),
            "p_A_maxT": float(pa),
            "classification": cls,
        }
    return out


def geometry_result(classified, eligibility, null_delta):
    core_vals = [classified[x]["pearson_full"] for x in STABLE_REFERENCE_LABELS]
    mod_vals = [classified[x]["pearson_full"] for x in MODULATED_REFERENCE_LABELS]
    if any(not finite(x) for x in core_vals + mod_vals):
        return {
            "G_core": None,
            "G_mod": None,
            "Delta_geometry": None,
            "p_Delta": None,
            "GEOMETRY_CORE_SUPPORTED": False,
            "MODULATION_ORDER_REPLICATED": False,
        }
    g_core = float(np.median(core_vals))
    g_mod = float(np.median(mod_vals))
    delta = g_core - g_mod
    p_delta = c.empirical_upper_p(delta, null_delta)
    classes = [classified[label]["classification"] for label, _, _, _ in CONTRASTS]
    all_exist = all(eligibility[name]["supported_residual_existence"] for name in TARGET_GROUPS)
    no_diff = all(x != "DIFFERENT_RESIDUAL_OR_MIXTURE" for x in classes)
    good = sum(x in ("STABLE_RESIDUAL", "RELATED_RESIDUAL_BUT_MODULATED") for x in classes)
    broad = bool(all_exist and no_diff and good >= 6)
    return {
        "stable_reference_labels": list(STABLE_REFERENCE_LABELS),
        "modulated_reference_labels": list(MODULATED_REFERENCE_LABELS),
        "G_core": g_core,
        "G_mod": g_mod,
        "Delta_geometry": float(delta),
        "p_Delta": float(p_delta),
        "GEOMETRY_CORE_SUPPORTED": broad,
        "MODULATION_ORDER_REPLICATED": bool(broad and delta > 0 and p_delta <= 0.05),
        "good_within_IT_contrasts": int(good),
    }


def cross_group_breadth(cross):
    good_classes = {
        "CROSS_READING_TOPOLOGY_REPLICATED",
        "CROSS_READING_TOPOLOGY_RELATED_BUT_REPRESENTATION_MODULATED",
    }
    nonall = [cross[name]["classification"] for name in TARGET_GROUPS]
    good = sum(x in good_classes for x in nonall)
    diff = sum(x == "CROSS_READING_TOPOLOGY_DIFFERENT" for x in nonall)
    if good >= 6 and diff == 0:
        cls = "CROSS_READING_GROUP_CORE_BROAD"
    elif good >= 4 and diff <= 1:
        cls = "CROSS_READING_GROUP_CORE_PARTIAL"
    else:
        cls = "CROSS_READING_GROUP_CORE_WEAK_OR_INCONCLUSIVE"
    return {"classification": cls, "replicated_or_related_groups": int(good), "different_groups": int(diff)}


def overall_classification(p_exist, w_all, cross, breadth, geometry):
    if p_exist > 0.01:
        return "ZL3B RESIDUAL GRAPH DOES NOT REPLICATE INDEPENDENTLY"
    if not finite(w_all) or float(w_all) < 0.50:
        return "INDEPENDENT-TRANSCRIPTION REPLICATION INCONCLUSIVE"

    pooled = cross["ALL"]["classification"]
    if pooled == "CROSS_READING_TOPOLOGY_DIFFERENT":
        return "ZL3B RESIDUAL GRAPH DOES NOT REPLICATE INDEPENDENTLY"
    if pooled == "CROSS_READING_TOPOLOGY_INCONCLUSIVE":
        return "INDEPENDENT-TRANSCRIPTION REPLICATION INCONCLUSIVE"

    broad = breadth["classification"]
    geom = bool(geometry["GEOMETRY_CORE_SUPPORTED"])
    if pooled == "CROSS_READING_TOPOLOGY_REPLICATED" and broad == "CROSS_READING_GROUP_CORE_BROAD" and geom:
        return "INDEPENDENT TRANSCRIPTION REPLICATES RESIDUAL TOKEN-CONSTRUCTION CORE"
    if (
        pooled in (
            "CROSS_READING_TOPOLOGY_REPLICATED",
            "CROSS_READING_TOPOLOGY_RELATED_BUT_REPRESENTATION_MODULATED",
        )
        and broad in ("CROSS_READING_GROUP_CORE_BROAD", "CROSS_READING_GROUP_CORE_PARTIAL")
        and geom
    ):
        return "RESIDUAL CONSTRUCTION REPLICATES, TOPOLOGY IS REPRESENTATION-MODULATED"
    return "INDEPENDENT-TRANSCRIPTION REPLICATION INCONCLUSIVE"


def max_sensitivity(it_path: Path, zl_path: Path, support):
    d = build_it_dataset(it_path, zl_path, "max")
    population = validate_population(d, support)
    real_q = c.q_views(d, d["X"], include_folds=True)
    ref = c.build_reference(d, MAX_REF_NS, "Issue58D max reference")
    sref = c.sorted_reference(ref)
    zv = c.residual_views(real_q, sref)
    energies, within, contrasts = c.real_metrics(zv)
    return {
        "namespace": MAX_REF_NS,
        "n_reference": N_REF,
        "population": {"clean_tokens": d["visible"], "parsed_tokens": d["parsed"], **population},
        "energies": energies,
        "within_reliability": within,
        "within_IT_contrasts": contrasts,
    }


def self_test():
    c.self_test()
    a = np.asarray([1.0, -2.0, 0.0, 3.0])
    d = np.asarray([2.0, -1.0, 1.0, -4.0])
    assert sign_agreement(a, d) == 2
    assert len(PAIRS) == 66
    assert REF_NS != TEST_NS != MAX_REF_NS
    print(json.dumps({"Issue58D_self_test": "ok", "n_edges": 66, "n_ref": N_REF, "n_test": N_TEST}, sort_keys=True))


def main(it_path: Path, zl_path: Path):
    support = load_support_audit()
    _, zl_z, zl_raw_sha = load_zl_first_reveal()

    d = build_it_dataset(it_path, zl_path, "min")
    population = validate_population(d, support)

    real_q = c.q_views(d, d["X"], include_folds=True)
    ref = c.build_reference(d, REF_NS, "Issue58D IT2a reference null")
    sref = c.sorted_reference(ref)
    zv = c.residual_views(real_q, sref)
    energies, within, contrasts = c.real_metrics(zv)

    nulls = run_test_nulls(d, sref, zl_z)
    p_exist = c.empirical_upper_p(energies["ALL"], nulls["pooled_energy"])
    eligibility = c.group_eligibility(energies, within, nulls["group_energy_max"])
    classified = c.classify_contrasts(contrasts, eligibility, nulls["contrast_r_max"])
    reg, pos = c.family_classifications(classified)

    cross = classify_cross_topology(zl_z, {name: zv[name]["full"] for name in GROUPS}, nulls)
    breadth = cross_group_breadth(cross)
    geometry = geometry_result(classified, eligibility, nulls["delta_geometry"])
    overall = overall_classification(p_exist, within["ALL"]["median"], cross, breadth, geometry)

    result = {
        "phase": "Issue58D-independent-reading-residual-graph-replication",
        "target_reveal": True,
        "program_object": "internal construction of one space-delimited token; not sentence grammar; spaces not assumed linguistic word boundaries",
        "github_sha": os.environ.get("TARGET_HEAD_SHA") or os.environ.get("GITHUB_SHA"),
        "sources": {
            "IT2a": d["source_identity"],
            "ZL3b_required_blob": ZL_BLOB,
            "ZL3b_first_reveal_raw_sha256": zl_raw_sha,
            "StageA_support_audit_raw_sha256": SUPPORT_AUDIT_SHA256,
        },
        "parser": {"primary_policy": "min", "n_slots": 12, "pair_count": 66},
        "population": {
            "clean_tokens": d["visible"],
            "parsed_tokens": d["parsed"],
            "physical_leaf_folds": d["folds"],
            **population,
        },
        "pairs": [list(map(int, p)) for p in PAIRS],
        "null_design": {
            "reference_namespace": REF_NS,
            "test_namespace": TEST_NS,
            "n_reference": N_REF,
            "n_test": N_TEST,
            "residual_transform": "reference empirical mid-rank normal score",
        },
        "real_IT2a": {
            "q_full": {name: real_q[name]["full"].tolist() for name in GROUPS},
            "z_full": {name: zv[name]["full"].tolist() for name in GROUPS},
            "z_train": {name: zv[name]["train"].tolist() for name in GROUPS},
            "z_held": {name: zv[name]["held"].tolist() for name in GROUPS},
            "energies": energies,
            "within_reliability": within,
        },
        "gate_A_independent_residual_existence": {
            "E_IT_ALL": energies["ALL"],
            "p_exist_IT": p_exist,
            "W_IT_ALL": within["ALL"]["median"],
            "supported": bool(p_exist <= 0.01 and finite(within["ALL"]["median"]) and float(within["ALL"]["median"]) >= 0.50),
        },
        "IT2a_group_existence": eligibility,
        "IT2a_within_reading_contrasts": classified,
        "IT2a_register_section_classification": reg,
        "IT2a_position_classification": pos,
        "gate_B_cross_reading_topology": cross,
        "cross_reading_group_breadth": breadth,
        "gate_C_geometry": geometry,
        "overall_classification": overall,
        "test_null": {
            "pooled_energy_values": nulls["pooled_energy"].tolist(),
            "pooled_energy_summary": c.summary(nulls["pooled_energy"]),
            "group_energy_maxT_values": nulls["group_energy_max"].tolist(),
            "group_energy_maxT_summary": c.summary(nulls["group_energy_max"]),
            "within_IT_similarity_maxT_values": nulls["contrast_r_max"].tolist(),
            "within_IT_similarity_maxT_summary": c.summary(nulls["contrast_r_max"]),
            "cross_reading_correlation_maxT_values": nulls["cross_r_max"].tolist(),
            "cross_reading_correlation_maxT_summary": c.summary(nulls["cross_r_max"]),
            "cross_reading_sign_maxT_values": nulls["cross_a_max"].tolist(),
            "cross_reading_sign_maxT_summary": c.summary(nulls["cross_a_max"]),
            "geometry_delta_values": nulls["delta_geometry"].tolist(),
            "geometry_delta_summary": c.summary(nulls["delta_geometry"]),
        },
        "max_parser_sensitivity": max_sensitivity(it_path, zl_path, support),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
    elif len(sys.argv) == 3:
        main(Path(sys.argv[1]), Path(sys.argv[2]))
    else:
        raise SystemExit(f"usage: {sys.argv[0]} IT2a-n.txt ZL3b-n.txt | --self-test")
