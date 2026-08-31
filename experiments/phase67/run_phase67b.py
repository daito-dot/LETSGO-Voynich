#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from run_phase67a import build_text_matrix, center_selected, centered_indices, residualize_visual_on_coverage, rv

ROOT_STATES = [
    "single_primary_root_like",
    "branched_root_system",
    "fibrous_tufted_roots",
    "swollen_tuberous_or_storage_like",
    "bulb_corm_or_compact_storage_body_like",
    "rhizome_or_horizontal_axis_like",
    "mixed",
]
U = "U"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_root_table(root_table: dict, manifest: dict):
    expected = {b["block_id"]: [o["object_id"] for o in b["fragment_objects"]] for b in manifest["blocks"]}
    got = {r["block_id"]: [o["object_id"] for o in r["objects"]] for r in root_table["records"]}
    if set(expected) != set(got):
        raise ValueError("root block ID mismatch")
    for b in expected:
        if expected[b] != got[b]:
            raise ValueError(f"root object order mismatch for {b}")
    for r in root_table["records"]:
        for o in r["objects"]:
            s = o["root_subterranean_architecture"]
            if s != U and s not in ROOT_STATES:
                raise ValueError(f"illegal root state {s!r} at {r['block_id']}/{o['object_id']}")


def build_root_matrix(root_table: dict, block_order: list[str]):
    rec = {r["block_id"]: r for r in root_table["records"]}
    X = np.zeros((len(block_order), len(ROOT_STATES)), dtype=float)
    coverage = np.zeros((len(block_order), 1), dtype=float)
    usable = np.zeros(len(block_order), dtype=bool)
    for i, b in enumerate(block_order):
        states = [o["root_subterranean_architecture"] for o in rec[b]["objects"]]
        obs = [s for s in states if s != U]
        coverage[i, 0] = len(obs) / len(states) if states else 0.0
        if obs:
            usable[i] = True
            c = Counter(obs)
            X[i] = np.sqrt(np.array([c[s] / len(obs) for s in ROOT_STATES], dtype=float))
    return X, coverage, usable


def centered_stats(X, C, Y, folios, usable):
    idx = centered_indices(folios, usable)
    Xc = center_selected(X, folios, idx)
    Cc = center_selected(C, folios, idx)
    Yc = center_selected(Y, folios, idx)
    Xres = residualize_visual_on_coverage(Xc, Cc)
    return {
        "rv": rv(Xc, Yc),
        "coverage_rv": rv(Cc, Yc),
        "residual_rv": rv(Xres, Yc),
        "n": int(len(idx)),
        "folios": sorted(set(folios[i] for i in idx)),
    }


def all_within_folio_permutations(folios):
    groups = []
    for f in dict.fromkeys(folios):
        idx = [i for i, ff in enumerate(folios) if ff == f]
        groups.append((idx, list(itertools.permutations(idx))))
    for choices in itertools.product(*(g[1] for g in groups)):
        perm = list(range(len(folios)))
        for (idx, _), chosen in zip(groups, choices):
            for dest, src in zip(idx, chosen):
                perm[dest] = src
        yield np.array(perm, dtype=int)


def gate(stat):
    return stat["n"] >= 8 and len(stat["folios"]) >= 3


def run(manifest, text_table, root_table, orders=(1, 2, 3)):
    validate_root_table(root_table, manifest)
    blocks, Y, text_meta = build_text_matrix(text_table, orders=orders)
    mb = [b["block_id"] for b in manifest["blocks"]]
    if blocks != mb:
        raise ValueError("text/manifest block order mismatch")
    folios = [b["folio"] for b in manifest["blocks"]]
    X, C, usable = build_root_matrix(root_table, blocks)
    obs = centered_stats(X, C, Y, folios, usable)

    perm_rv = []
    perm_cov = []
    perm_res = []
    identity = False
    for perm in all_within_folio_permutations(folios):
        if np.array_equal(perm, np.arange(len(perm))):
            identity = True
        s = centered_stats(X, C, Y[perm], folios, usable)
        perm_rv.append(s["rv"])
        perm_cov.append(s["coverage_rv"])
        perm_res.append(s["residual_rv"])

    expected = math.prod(math.factorial(v) for v in Counter(folios).values())
    if len(perm_rv) != expected or expected != 1152:
        raise AssertionError((len(perm_rv), expected))
    if not identity:
        raise AssertionError("identity assignment missing")

    perm_rv = np.asarray(perm_rv)
    perm_cov = np.asarray(perm_cov)
    perm_res = np.asarray(perm_res)
    p = float(np.mean(perm_rv >= obs["rv"] - 1e-15))
    p_cov = float(np.mean(perm_cov >= obs["coverage_rv"] - 1e-15))
    p_res = float(np.mean(perm_res >= obs["residual_rv"] - 1e-15))

    g = gate(obs)
    if p <= 0.05 and g:
        if p_cov <= 0.05 and p_res > 0.05:
            classification = "MORPHOLOGY / OBSERVABILITY CONFOUNDED"
        else:
            classification = "CANDIDATE ROOT↔BODY ASSOCIATION — REPLICATION REQUIRED"
    elif p <= 0.05 and not g:
        classification = "UNDERPOWERED / COVERAGE-LIMITED"
    else:
        classification = "NOT SUPPORTED"

    return {
        "schema": "phase67b-result-v1",
        "orders": list(orders),
        "n_blocks": len(blocks),
        "permutation_count": int(len(perm_rv)),
        "observed": obs,
        "p_values": {"root_rv": p, "coverage_rv": p_cov, "coverage_residualized_root_rv": p_res},
        "operational_gate_pass": g,
        "classification": classification,
        "text_meta": {k: v for k, v in text_meta.items() if k != "tokens"},
        "null_summary": {
            "rv_mean": float(perm_rv.mean()),
            "rv_q95": float(np.quantile(perm_rv, 0.95)),
            "rv_max": float(perm_rv.max()),
            "residual_rv_mean": float(perm_res.mean()),
            "residual_rv_q95": float(np.quantile(perm_res, 0.95)),
            "residual_rv_max": float(perm_res.max()),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).parent
    ap.add_argument("--manifest", type=Path, default=here / "BLOCK_MANIFEST_A.json")
    ap.add_argument("--text", type=Path, default=here / "TEXT_TABLE_A.json")
    ap.add_argument("--root", type=Path, default=here / "ROOT_ANNOTATION_B.json")
    ap.add_argument("--out", type=Path, default=here / "RESULT_B.json")
    ap.add_argument("--orders", default="1,2,3")
    args = ap.parse_args()
    result = run(load_json(args.manifest), load_json(args.text), load_json(args.root), tuple(int(x) for x in args.orders.split(",") if x))
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": result["classification"],
        "rv": result["observed"]["rv"],
        "p": result["p_values"]["root_rv"],
        "coverage_p": result["p_values"]["coverage_rv"],
        "residual_p": result["p_values"]["coverage_residualized_root_rv"],
        "n": result["observed"]["n"],
        "folios": result["observed"]["folios"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
