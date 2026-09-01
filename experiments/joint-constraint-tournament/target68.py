#!/usr/bin/env python3
"""Issue #68 preregistered first joint-constraint R1 target scorer.

Scientific authority: experiments/joint-constraint-tournament/PLAN_A.md
Implementation freezes: IMPLEMENTATION_TARGET.md / IMPLEMENTATION_TARGET_ORDER.md

A1 failed the preregistered representation gate in the target-free preflight.
This executable MUST NOT compute any real A1 pair-Q/residual graph. The only
real R1 candidate scored here is the representation-compatible frozen Naibbe
C1-E0 published respaced realization-0 surface.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Sequence

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in (
    "phase62",
    "phase64",
    "issue26-music",
    "occupancy-graph-stability",
    "occupancy-graph-residual",
    "occupancy-graph-independent-transcription",
):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as p62b  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402
import phase58b_graph_stability as b58  # noqa: E402
import phase58c_residual_graph as c58  # noqa: E402
import phase58d_independent_residual as d58  # noqa: E402

DESIGN_MAIN = "b2298d7fe251070dacd21852ae3b5a1dac95fe65"
PREFLIGHT_SHA256 = "fdd2b1138542bf1b332b20f27a9869ac7a3501038e7d4ec9ccf40910e3b98771"
ISSUE58D_SHA256 = "f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6"
ISSUE58C_SHA256 = "fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d"
EXPECTED_CREMMA = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_NAIBBE = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
N_REF = 1000
N_TEST = 1000
N_FOLDS = 4
N_EDGES = 66
PAIRS = b58.PAIRS
REF_NS = "issue68:B2:Naibbe:C1-E0:published-respaced:reference-null"
TEST_NS = "issue68:B2:Naibbe:C1-E0:published-respaced:test-null"
MANUSCRIPTS = ("BIS193", "CLM13027", "Mazarine915", "UBL758")
SEEDS = (6480000, 6480100, 6480200, 6480300)
EXPECTED_SURFACE_SHA = {
    "BIS193": "fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805",
    "CLM13027": "da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77",
    "Mazarine915": "2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d",
    "UBL758": "5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89",
}
EXPECTED_POOLED_SURFACE_SHA = "47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd"
EXPECTED_VISIBLE = 33574
EXPECTED_PARSED = 29759
COVERAGE_GATE = 0.60


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_items_payload(items: Sequence[p62b.Item]) -> bytes:
    obj = []
    for it in items:
        obj.append({
            "item_id": it.item_id,
            "document": it.document,
            "leaf": it.leaf,
            "lines": [["".join(tok) for tok in line] for line in it.lines],
        })
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def surface_digest(items: Sequence[p62b.Item]) -> str:
    return sha256_bytes(canonical_items_payload(items))


def position_category(index: int, n_visible: int) -> str:
    if n_visible == 1:
        return "singleton"
    if index == 0:
        return "initial"
    if index == n_visible - 1:
        return "final"
    return "interior"


def load_preflight() -> dict:
    path = HERE.parent / "preflight" / "preflight.json"
    got = sha256_file(path)
    if got != PREFLIGHT_SHA256:
        raise RuntimeError(f"preflight SHA mismatch: {got} != {PREFLIGHT_SHA256}")
    r = json.loads(path.read_text(encoding="utf-8"))
    if r["target_reveal"] is not False or r["real_candidate_pair_or_residual_metrics_computed"] is not False:
        raise RuntimeError("preflight target firewall was not clean")
    if r["preflight_dispositions"]["A1_R1_representation"] != "FAIL_REPRESENTATION_COMPATIBILITY":
        raise RuntimeError("A1 representation disposition changed")
    if r["preflight_dispositions"]["Naibbe_R1_representation"] != "AUTHORIZED_FOR_R1_REVEAL":
        raise RuntimeError("Naibbe was not authorized for R1 reveal")
    if r["preflight_dispositions"]["Naibbe_R4_primary"] != "FAIL":
        raise RuntimeError("Naibbe R4 pretarget disposition changed")
    return r


def load_target_references():
    # #58C exact first reveal is reconstructed by the already-audited #58D loader.
    _, zl_views, raw58c = d58.load_zl_first_reveal()
    if raw58c != ISSUE58C_SHA256:
        raise RuntimeError(f"#58C exact raw SHA mismatch: {raw58c}")
    zl = np.asarray(zl_views["ALL"], dtype=np.float64)

    p58d = EXPERIMENTS / "occupancy-graph-independent-transcription" / "first-reveal" / "issue66_independent_residual_results.json"
    got58d = sha256_file(p58d)
    if got58d != ISSUE58D_SHA256:
        raise RuntimeError(f"#58D exact raw SHA mismatch: {got58d}")
    r58d = json.loads(p58d.read_text(encoding="utf-8"))
    expected_pairs = [list(map(int, p)) for p in PAIRS]
    if r58d["pairs"] != expected_pairs:
        raise RuntimeError("#58D pair order differs from target scorer")
    it = np.asarray(r58d["real_IT2a"]["z_full"]["ALL"], dtype=np.float64)
    if zl.shape != (N_EDGES,) or it.shape != (N_EDGES,) or not np.all(np.isfinite(zl)) or not np.all(np.isfinite(it)):
        raise RuntimeError("invalid frozen target residual vector")

    r = b58.corr(zl, it)
    a = d58.sign_agreement(zl, it)
    frozen = r58d["gate_B_cross_reading_topology"]["ALL"]
    if r is None or abs(float(r) - float(frozen["pearson"])) > 1e-12 or a != frozen["sign_agreement"]:
        raise RuntimeError("frozen ZL3b/IT2a target-vector cross-check failed")
    if abs(float(r) - 0.9884483852763541) > 1e-12 or a != 65:
        raise RuntimeError("unexpected frozen pooled target topology")
    return {
        "ZL3b": zl,
        "IT2a": it,
    }, {
        "Issue58C_raw_sha256": raw58c,
        "Issue58D_raw_sha256": got58d,
        "ZL3b_IT2a_pearson": float(r),
        "ZL3b_IT2a_sign_agreement": int(a),
        "sign_denominator": N_EDGES,
    }


def build_naibbe_dataset(cremma_root: Path, naibbe_root: Path, preflight: dict):
    got_cremma = p62b.verify_cremma_commit(cremma_root)
    if got_cremma != EXPECTED_CREMMA:
        raise RuntimeError(f"CREMMA commit mismatch: {got_cremma}")
    mod = n64.load_naibbe(naibbe_root)
    original_map = dict(mod.placeholder_to_glyph)
    sources = {
        name: p62b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in p62b.PRIMARY_MANUSCRIPTS.items()
    }
    parser = e.SlotParser()
    expected_pf = {x["manuscript"]: x for x in preflight["Naibbe_primary"]["per_manuscript"]}

    pooled_items = []
    lines = []
    per_manuscript = []
    visible = parsed = 0

    for fold, manuscript in enumerate(MANUSCRIPTS):
        seed = SEEDS[fold]
        primary, _raw, diag = n64.encrypt_manuscript(mod, sources[manuscript], manuscript, original_map, seed)
        digest = surface_digest(primary)
        if digest != EXPECTED_SURFACE_SHA[manuscript]:
            raise RuntimeError(f"surface SHA mismatch {manuscript}: {digest}")
        pf = expected_pf[manuscript]
        if pf["surface_sha256"] != digest or pf["seed"] != seed:
            raise RuntimeError(f"preflight surface identity mismatch: {manuscript}")
        pooled_items.extend(primary)

        mv = mp = 0
        for item in primary:  # frozen existing item order; do not sort
            for line_index, toks in enumerate(item.lines):
                n_visible = len(toks)
                visible += n_visible
                mv += n_visible
                rows = []
                positions = []
                for idx, tok_units in enumerate(toks):
                    tok = "".join(tok_units)
                    picked = parser.pick(tok, "min")
                    if picked is None:
                        continue
                    vals = picked[1]
                    rows.append(np.fromiter((bool(vals[s]) for s in range(12)), dtype=np.uint8, count=12))
                    positions.append(position_category(idx, n_visible))
                    parsed += 1
                    mp += 1
                if rows:
                    lines.append({
                        "fold": fold,
                        "manuscript": manuscript,
                        "item_id": item.item_id,
                        "line_index": int(line_index),
                        "occ": np.stack(rows),
                        "positions": tuple(positions),
                    })

        if mv != pf["coverage"]["visible_tokens"] or mp != pf["coverage"]["accepted_tokens"]:
            raise RuntimeError(f"preflight coverage count mismatch for {manuscript}: {(mv, mp)}")
        per_manuscript.append({
            "fold": fold,
            "manuscript": manuscript,
            "seed": seed,
            "surface_sha256": digest,
            "visible_tokens": int(mv),
            "parsed_tokens": int(mp),
            "generation_diagnostics": diag,
        })

    pooled_digest = surface_digest(pooled_items)
    if pooled_digest != EXPECTED_POOLED_SURFACE_SHA:
        raise RuntimeError(f"pooled surface SHA mismatch: {pooled_digest}")
    if visible != EXPECTED_VISIBLE or parsed != EXPECTED_PARSED:
        raise RuntimeError(f"pooled candidate population mismatch: {(visible, parsed)}")
    if preflight["Naibbe_primary"]["pooled_surface_sha256"] != pooled_digest:
        raise RuntimeError("preflight pooled surface SHA differs")

    # IMPORTANT: preserve line list exactly in construction order fixed before scorer.
    X = np.concatenate([x["occ"] for x in lines], axis=0)
    token_folds = np.concatenate([np.full(len(x["occ"]), x["fold"], np.int8) for x in lines])
    pos_id = np.concatenate([
        np.asarray([b58.POSITION_INDEX.get(p, -1) for p in x["positions"]], dtype=np.int8)
        for x in lines
    ])
    maxlen = max(len(x["occ"]) for x in lines)
    padded = np.zeros((len(lines), maxlen, 12), dtype=np.uint8)
    line_mask = np.zeros((len(lines), maxlen), dtype=bool)
    for i, row in enumerate(lines):
        z = row["occ"]
        padded[i, : len(z)] = z
        line_mask[i, : len(z)] = True
    if not np.array_equal(padded[line_mask], X):
        raise RuntimeError("candidate padded/flat ordering mismatch")

    fold_counts = [int(np.sum(token_folds == f)) for f in range(N_FOLDS)]
    expected_fold_counts = [expected_pf[m]["coverage"]["accepted_tokens"] for m in MANUSCRIPTS]
    if fold_counts != expected_fold_counts:
        raise RuntimeError(f"candidate fold support mismatch: {fold_counts} != {expected_fold_counts}")

    return {
        "visible": int(visible),
        "parsed": int(parsed),
        "coverage": float(parsed / visible),
        "surface_sha256": pooled_digest,
        "per_manuscript": per_manuscript,
        "fold_counts": fold_counts,
        "line_count": len(lines),
        "X": X,
        "token_folds": token_folds,
        "pos_id": pos_id,
        "padded": padded,
        "line_mask": line_mask,
    }


def q_views_candidate(d, X, include_folds: bool):
    code = b58.pair_codes(X)
    cf = b58.partition_counts(code, d["token_folds"], N_FOLDS, True)
    total = cf.sum(axis=0)
    out = {"full": b58.q_cond(total)}
    if include_folds:
        out["held"] = np.stack([b58.q_cond(cf[f]) for f in range(N_FOLDS)])
        out["train"] = np.stack([b58.q_cond(total - cf[f]) for f in range(N_FOLDS)])
    return out


def build_reference(d):
    ref = {
        "full": np.empty((N_REF, N_EDGES), dtype=np.float64),
        "train": np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64),
        "held": np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64),
    }
    for n in range(N_REF):
        Y = c58.shuffled_flat(d, REF_NS, n)
        qv = q_views_candidate(d, Y, True)
        ref["full"][n] = qv["full"]
        ref["train"][n] = qv["train"]
        ref["held"][n] = qv["held"]
        if (n + 1) % 100 == 0:
            print(f"Issue68 Naibbe reference null {n+1}/{N_REF}", file=sys.stderr, flush=True)
    return {k: np.sort(v, axis=0) for k, v in ref.items()}


def residualize(qv, sref, include_folds: bool):
    out = {"full": c58.normal_score_array(qv["full"], sref["full"])}
    if include_folds:
        out["train"] = c58.normal_score_array(qv["train"], sref["train"])
        out["held"] = c58.normal_score_array(qv["held"], sref["held"])
    return out


def sign_agreement(a, b) -> int:
    return d58.sign_agreement(a, b)


def reliability(zv):
    vals = [b58.corr(zv["train"][f], zv["held"][f]) for f in range(N_FOLDS)]
    valid = [float(x) for x in vals if x is not None and math.isfinite(float(x))]
    med = None if len(valid) < 4 else float(np.median(valid))
    return {"fold_correlations": vals, "valid_folds": len(valid), "median": med}


def test_nulls(d, sref, targets):
    energies = np.empty(N_TEST, dtype=np.float64)
    rmax = np.empty(N_TEST, dtype=np.float64)
    amax = np.empty(N_TEST, dtype=np.float64)
    r_by_target = {name: np.empty(N_TEST, dtype=np.float64) for name in targets}
    a_by_target = {name: np.empty(N_TEST, dtype=np.float64) for name in targets}

    for n in range(N_TEST):
        Y = c58.shuffled_flat(d, TEST_NS, n)
        q = q_views_candidate(d, Y, False)
        z = c58.normal_score_array(q["full"], sref["full"])
        energies[n] = c58.residual_energy(z)
        rs, aa = [], []
        for name, target in targets.items():
            rr = b58.corr(z, target)
            rv = -1.0 if rr is None else float(rr)
            av = sign_agreement(z, target)
            r_by_target[name][n] = rv
            a_by_target[name][n] = av
            rs.append(rv)
            aa.append(av)
        rmax[n] = max(rs)
        amax[n] = max(aa)
        if (n + 1) % 100 == 0:
            print(f"Issue68 Naibbe test null {n+1}/{N_TEST}", file=sys.stderr, flush=True)
    return {
        "energy": energies,
        "correlation_maxT": rmax,
        "sign_maxT": amax,
        "correlation_by_target": r_by_target,
        "sign_by_target": a_by_target,
    }


def topology_result(z, targets, nulls):
    out = {}
    for name, target in targets.items():
        rr = b58.corr(z, target)
        if rr is None:
            r = None
            pr = None
            a = sign_agreement(z, target)
            pa = c58.empirical_upper_p(a, nulls["sign_maxT"])
            passed = False
        else:
            r = float(rr)
            a = sign_agreement(z, target)
            pr = c58.empirical_upper_p(r, nulls["correlation_maxT"])
            pa = c58.empirical_upper_p(a, nulls["sign_maxT"])
            passed = bool(r >= 0.70 and pr <= 0.01 and a >= 50 and pa <= 0.01)
        out[name] = {
            "pearson": r,
            "sign_agreement": int(a),
            "sign_denominator": N_EDGES,
            "p_R_maxT_over_target_readings": pr,
            "p_sign_maxT_over_target_readings": float(pa),
            "effect_and_familywise_gate_pass": passed,
        }
    return out


def candidate_classifications(preflight, r1_pass):
    a1_r2 = bool(preflight["historical_frozen_responsibilities"]["A1"]["R2"]["pass"])
    a1_r3 = bool(preflight["historical_frozen_responsibilities"]["A1"]["R3"]["pass"])
    n_r2 = bool(preflight["historical_frozen_responsibilities"]["Naibbe_C1_E0"]["R2"]["pass"])
    n_r3 = bool(preflight["historical_frozen_responsibilities"]["Naibbe_C1_E0"]["R3"]["pass"])
    n_r4 = bool(preflight["Naibbe_primary"]["R4_primary_rep0_aggregate"]["R4_primary_pass_100pct_unique_exact"])
    r5 = True

    a1_struct = int(False) + int(a1_r2) + int(a1_r3)
    if not r5:
        a1_cls = "OVERFIT / ACCESS-VIOLATION"
    elif False and a1_r2 and a1_r3:
        a1_cls = "JOINT-CONSTRAINT COMPETITIVE SURFACE GENERATOR"
    elif a1_struct == 2:
        a1_cls = "PARTIAL STRUCTURAL MODEL"
    else:
        a1_cls = "NOT COMPETITIVE"

    n_struct = int(bool(r1_pass)) + int(n_r2) + int(n_r3)
    if not r5:
        n_cls = "OVERFIT / ACCESS-VIOLATION"
    elif r1_pass and n_r2 and n_r3 and n_r4:
        n_cls = "JOINT-CONSTRAINT COMPETITIVE DECODER"
    elif n_struct == 2 or (r1_pass and n_r2 and n_r3 and not n_r4):
        n_cls = "PARTIAL STRUCTURAL DECODER MODEL"
    else:
        n_cls = "NOT COMPETITIVE"

    if n_cls == "JOINT-CONSTRAINT COMPETITIVE DECODER":
        global_cls = "REVERSIBLE FAMILY JOINT-CONSTRAINT COMPETITIVE"
    elif a1_cls == "JOINT-CONSTRAINT COMPETITIVE SURFACE GENERATOR":
        global_cls = "SURFACE GENERATOR JOINT-COMPETITIVE; INVERSE MECHANISM STILL OPEN"
    else:
        global_cls = "NO TESTED FAMILY JOINT-CONSTRAINT COMPETITIVE"

    return {
        "A1_A1R1": {
            "R1": False,
            "R1_reason": "FAIL_REPRESENTATION_COMPATIBILITY",
            "real_R1_pair_or_residual_metrics_computed": False,
            "R2": a1_r2,
            "R3": a1_r3,
            "R4": None,
            "R5": r5,
            "classification": a1_cls,
        },
        "Naibbe_C1_E0": {
            "R1": bool(r1_pass),
            "R2": n_r2,
            "R3": n_r3,
            "R4": n_r4,
            "R5": r5,
            "classification": n_cls,
        },
        "global_classification": global_cls,
    }


def self_test():
    assert len(PAIRS) == 66
    assert N_REF == 1000 and N_TEST == 1000 and N_FOLDS == 4
    assert REF_NS != TEST_NS
    X = np.zeros((12, 12), dtype=np.uint8)
    for i in range(12):
        X[i, i] = 1
        X[i, (i + 1) % 12] = 1
    d = {
        "X": X,
        "token_folds": np.asarray([i % 4 for i in range(12)], dtype=np.int8),
    }
    q = q_views_candidate(d, X, True)
    assert q["full"].shape == (66,)
    assert q["train"].shape == (4, 66)
    assert q["held"].shape == (4, 66)
    assert sign_agreement(np.asarray([1.0, -1.0, 1.0]), np.asarray([2.0, -2.0, -3.0])) == 2
    print(json.dumps({"Issue68_target_self_test": "ok", "n_edges": 66, "n_ref": 1000, "n_test": 1000, "real_candidate_target_scored": False}, sort_keys=True))


def main(cremma_root: Path, naibbe_root: Path):
    preflight = load_preflight()
    targets, target_authority = load_target_references()
    d = build_naibbe_dataset(cremma_root, naibbe_root, preflight)
    if d["coverage"] < COVERAGE_GATE:
        raise RuntimeError("Naibbe unexpectedly failed frozen representation gate at reveal")

    real_q = q_views_candidate(d, d["X"], True)
    sref = build_reference(d)
    real_z = residualize(real_q, sref, True)
    E = c58.residual_energy(real_z["full"])
    W = reliability(real_z)

    nulls = test_nulls(d, sref, targets)
    p_exist = c58.empirical_upper_p(E, nulls["energy"])
    existence_pass = bool(W["valid_folds"] >= 4 and W["median"] is not None and W["median"] >= 0.50 and p_exist <= 0.01)
    topology = topology_result(real_z["full"], targets, nulls)
    r1_pass = bool(existence_pass and all(x["effect_and_familywise_gate_pass"] for x in topology.values()))
    classes = candidate_classifications(preflight, r1_pass)

    result = {
        "phase": "Issue68-first-joint-constraint-R1-reveal",
        "target_reveal": True,
        "github_sha": os.environ.get("TARGET_HEAD_SHA") or os.environ.get("GITHUB_SHA"),
        "design_main": DESIGN_MAIN,
        "program_object": "complete residual token-construction graph under the frozen 12-slot representation; not sentence grammar or decipherment",
        "preflight_authority": {
            "sha256": PREFLIGHT_SHA256,
            "A1_R1_representation": preflight["preflight_dispositions"]["A1_R1_representation"],
            "Naibbe_R1_representation": preflight["preflight_dispositions"]["Naibbe_R1_representation"],
            "Naibbe_R4_primary": preflight["preflight_dispositions"]["Naibbe_R4_primary"],
        },
        "target_authority": target_authority,
        "pairs": [list(map(int, p)) for p in PAIRS],
        "candidate": {
            "name": "Naibbe_C1_E0",
            "view": "published_respaced_rep0",
            "surface_sha256": d["surface_sha256"],
            "per_manuscript": d["per_manuscript"],
            "population": {
                "visible_tokens": d["visible"],
                "parsed_tokens": d["parsed"],
                "coverage": d["coverage"],
                "coverage_gate": COVERAGE_GATE,
                "representation_compatible": True,
                "line_count_with_at_least_one_parsed_token": d["line_count"],
                "fold_parsed_tokens": d["fold_counts"],
            },
        },
        "null_design": {
            "reference_namespace": REF_NS,
            "test_namespace": TEST_NS,
            "n_reference": N_REF,
            "n_test": N_TEST,
            "candidate_family_after_representation_gate": ["Naibbe_C1_E0"],
            "target_reading_family": ["ZL3b", "IT2a"],
            "residual_transform": "candidate-owned reference empirical mid-rank normal score",
            "line_order": "BIS193,CLM13027,Mazarine915,UBL758; existing generated item order; line index; accepted token order",
        },
        "real_Naibbe_R1": {
            "q_full": real_q["full"].tolist(),
            "z_full": real_z["full"].tolist(),
            "residual_energy": E,
            "within_reliability": W,
        },
        "R1_residual_existence": {
            "E": E,
            "W": W["median"],
            "valid_reliability_folds": W["valid_folds"],
            "p_exist_maxT_candidate_family": p_exist,
            "pass": existence_pass,
        },
        "R1_topology": topology,
        "R1_pass": r1_pass,
        "test_null": {
            "energy_values": nulls["energy"].tolist(),
            "energy_summary": c58.summary(nulls["energy"]),
            "correlation_maxT_over_target_readings_values": nulls["correlation_maxT"].tolist(),
            "correlation_maxT_over_target_readings_summary": c58.summary(nulls["correlation_maxT"]),
            "sign_maxT_over_target_readings_values": [int(x) for x in nulls["sign_maxT"]],
            "sign_maxT_over_target_readings_summary": c58.summary(nulls["sign_maxT"]),
            "correlation_by_target_summary": {k: c58.summary(v) for k, v in nulls["correlation_by_target"].items()},
            "sign_by_target_summary": {k: c58.summary(v) for k, v in nulls["sign_by_target"].items()},
        },
        "historical_frozen_responsibilities": preflight["historical_frozen_responsibilities"],
        "Naibbe_R4_pretarget": preflight["Naibbe_primary"]["R4_primary_rep0_aggregate"],
        "candidate_classifications": classes,
        "interpretation_boundary": {
            "plaintext_recovered": False,
            "historical_identity_established": False,
            "spaces_proven_linguistic_words": False,
            "decipherment_established": False,
        },
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
    elif len(sys.argv) == 3:
        main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    else:
        raise SystemExit(f"usage: {sys.argv[0]} CREMMA_ROOT NAIBBE_ROOT | --self-test")
