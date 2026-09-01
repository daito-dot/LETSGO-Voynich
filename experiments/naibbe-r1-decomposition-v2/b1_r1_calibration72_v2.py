#!/usr/bin/env python3
"""Issue #72 V2 Stage B1 unchanged-Naibbe R1 calibration.

Scores exactly one frozen Phase64B rep at a time. This is a positive-control
measurement calibration, not an intervention test. No Issue72 intervention
surface is constructed or loaded, and no B1 PASS/FAIL threshold is applied.

Usage:
  python b1_r1_calibration72_v2.py CREMMA_ROOT NAIBBE_ROOT REP OUTPUT_JSON [--primary-only]
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Mapping, Sequence

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
    "joint-constraint-tournament",
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
import target68 as t68  # noqa: E402

B0_PATH = HERE.parent / "stage_b0_support.json"
B0_SHA256 = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
N_REF = 1000
N_FOLDS = 4
N_EDGES = 66
MANUSCRIPTS = ("BIS193", "CLM13027", "Mazarine915", "UBL758")
REP0_PRIMARY_NS = "issue68:B2:Naibbe:C1-E0:published-respaced:reference-null"
PRIMARY_NS = {
    0: REP0_PRIMARY_NS,
    1: "issue72v2:positive-control:rep1:reference:primary",
    2: "issue72v2:positive-control:rep2:reference:primary",
    3: "issue72v2:positive-control:rep3:reference:primary",
    4: "issue72v2:positive-control:rep4:reference:primary",
}
SECONDARY_NS = {
    r: f"issue72v2:positive-control:rep{r}:reference:secondary" for r in range(5)
}
REP0_FROZEN = {
    "E": 3.1784043855151296,
    "W": 0.954726539114345,
    "ZL3b_R": 0.8830282501011794,
    "IT2a_R": 0.9000974100381157,
    "ZL3b_sign": 60,
    "IT2a_sign": 61,
}
FLOAT_TOL = 1e-12


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_b0() -> dict:
    got = sha256_file(B0_PATH)
    if got != B0_SHA256:
        raise RuntimeError(f"B0 exact raw SHA mismatch: {got} != {B0_SHA256}")
    obj = json.loads(B0_PATH.read_text(encoding="utf-8"))
    if obj["status"] != "UNCHANGED_NAIBBE_REP0_REP4_SURFACES_FROZEN":
        raise RuntimeError("B0 status changed")
    if any(obj["target_access"].values()):
        raise RuntimeError("B0 target firewall was not clean")
    return obj


def canonical_items_payload(items: Sequence[p62b.Item]) -> bytes:
    obj = [
        {
            "item_id": it.item_id,
            "document": it.document,
            "leaf": it.leaf,
            "lines": [["".join(tok) for tok in line] for line in it.lines],
        }
        for it in items
    ]
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def surface_digest(items: Sequence[p62b.Item]) -> str:
    return sha256_bytes(canonical_items_payload(items))


def build_dataset(cremma_root: Path, naibbe_root: Path, rep: int, b0: Mapping) -> dict:
    got_cremma = p62b.verify_cremma_commit(cremma_root)
    if got_cremma != t68.EXPECTED_CREMMA:
        raise RuntimeError(f"CREMMA commit mismatch: {got_cremma}")
    mod = n64.load_naibbe(naibbe_root)
    original_map = dict(mod.placeholder_to_glyph)
    sources = {
        name: p62b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in p62b.PRIMARY_MANUSCRIPTS.items()
    }
    parser = e.SlotParser()
    e.validate_parser(parser)
    frozen = b0["reps"][f"rep{rep}"]

    pooled_items = []
    lines = []
    visible = parsed = 0
    per_manuscript = []

    for fold, manuscript in enumerate(MANUSCRIPTS):
        expected = frozen["per_manuscript"][manuscript]
        seed = 6480000 + 100 * fold + rep
        if expected["seed"] != seed:
            raise RuntimeError(f"B0 seed mismatch for rep{rep} {manuscript}")
        primary, _raw, diag = n64.encrypt_manuscript(
            mod, sources[manuscript], manuscript, original_map, seed
        )
        digest = surface_digest(primary)
        if digest != expected["primary_surface_sha256"]:
            raise RuntimeError(f"B0 surface mismatch rep{rep} {manuscript}: {digest}")
        pooled_items.extend(primary)
        mv = mp = 0
        for item in primary:  # exact existing item order, no sorting
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
                    positions.append(t68.position_category(idx, n_visible))
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
        if mv != expected["support"]["visible_tokens"] or mp != expected["support"]["accepted_tokens"]:
            raise RuntimeError(f"B0 support mismatch rep{rep} {manuscript}: {(mv, mp)}")
        per_manuscript.append({
            "fold": fold,
            "manuscript": manuscript,
            "seed": seed,
            "surface_sha256": digest,
            "visible_tokens": int(mv),
            "parsed_tokens": int(mp),
            "ambiguity_retries": int(diag["ambiguity_retries"]),
        })

    pooled_digest = surface_digest(pooled_items)
    if pooled_digest != frozen["primary_pooled_surface_sha256"]:
        raise RuntimeError(f"B0 pooled surface mismatch rep{rep}: {pooled_digest}")
    if visible != frozen["support"]["visible_tokens"] or parsed != frozen["support"]["accepted_tokens"]:
        raise RuntimeError(f"B0 pooled support mismatch rep{rep}: {(visible, parsed)}")

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
        raise RuntimeError("padded/flat candidate order mismatch")

    fold_counts = [int(np.sum(token_folds == f)) for f in range(N_FOLDS)]
    expected_fold_counts = [
        frozen["per_manuscript"][m]["support"]["accepted_tokens"] for m in MANUSCRIPTS
    ]
    if fold_counts != expected_fold_counts:
        raise RuntimeError(f"fold counts mismatch rep{rep}: {fold_counts} != {expected_fold_counts}")

    return {
        "rep": rep,
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


def build_reference(d: Mapping, namespace: str) -> dict:
    ref = {
        "full": np.empty((N_REF, N_EDGES), dtype=np.float64),
        "train": np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64),
        "held": np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64),
    }
    for n in range(N_REF):
        Y = c58.shuffled_flat(d, namespace, n)
        qv = t68.q_views_candidate(d, Y, True)
        ref["full"][n] = qv["full"]
        ref["train"][n] = qv["train"]
        ref["held"][n] = qv["held"]
        if (n + 1) % 100 == 0:
            print(f"rep{d['rep']} {namespace} reference {n+1}/{N_REF}", file=sys.stderr, flush=True)
    return {k: np.sort(v, axis=0) for k, v in ref.items()}


def calibration(d: Mapping, real_q: Mapping, targets: Mapping[str, np.ndarray], namespace: str) -> dict:
    sref = build_reference(d, namespace)
    real_z = t68.residualize(real_q, sref, True)
    energy = float(c58.residual_energy(real_z["full"]))
    rel = t68.reliability(real_z)
    topology = {}
    for name, target in targets.items():
        rr = b58.corr(real_z["full"], target)
        if rr is None:
            raise RuntimeError(f"undefined topology correlation rep{d['rep']} {name}")
        topology[name] = {
            "pearson": float(rr),
            "sign_agreement": int(d58.sign_agreement(real_z["full"], target)),
            "sign_denominator": N_EDGES,
        }
    return {
        "namespace": namespace,
        "n_reference": N_REF,
        "q_full": real_q["full"].tolist(),
        "z_full": real_z["full"].tolist(),
        "residual_energy": energy,
        "reliability": rel,
        "topology": topology,
        "M_R": float(min(topology["ZL3b"]["pearson"], topology["IT2a"]["pearson"])),
        "M_sign": int(min(topology["ZL3b"]["sign_agreement"], topology["IT2a"]["sign_agreement"])),
    }


def check_rep0_primary(x: Mapping) -> None:
    checks = {
        "E": x["residual_energy"],
        "W": x["reliability"]["median"],
        "ZL3b_R": x["topology"]["ZL3b"]["pearson"],
        "IT2a_R": x["topology"]["IT2a"]["pearson"],
    }
    for name, got in checks.items():
        if got is None or abs(float(got) - REP0_FROZEN[name]) > FLOAT_TOL:
            raise RuntimeError(f"rep0 primary exact replay failed {name}: {got} != {REP0_FROZEN[name]}")
    if x["topology"]["ZL3b"]["sign_agreement"] != REP0_FROZEN["ZL3b_sign"]:
        raise RuntimeError("rep0 ZL sign replay failed")
    if x["topology"]["IT2a"]["sign_agreement"] != REP0_FROZEN["IT2a_sign"]:
        raise RuntimeError("rep0 IT sign replay failed")


def paired_noise(primary: Mapping, secondary: Mapping) -> dict:
    zp = np.asarray(primary["z_full"], dtype=np.float64)
    zs = np.asarray(secondary["z_full"], dtype=np.float64)
    rr = b58.corr(zp, zs)
    if rr is None:
        raise RuntimeError("undefined primary-secondary z correlation")
    return {
        "corr_Z_primary_secondary": float(rr),
        "sign_Z_primary_secondary": int(d58.sign_agreement(zp, zs)),
        "sign_denominator": N_EDGES,
        "abs_delta_E": abs(float(primary["residual_energy"]) - float(secondary["residual_energy"])),
        "abs_delta_W": abs(float(primary["reliability"]["median"]) - float(secondary["reliability"]["median"])),
        "abs_delta_R_ZL3b": abs(float(primary["topology"]["ZL3b"]["pearson"]) - float(secondary["topology"]["ZL3b"]["pearson"])),
        "abs_delta_R_IT2a": abs(float(primary["topology"]["IT2a"]["pearson"]) - float(secondary["topology"]["IT2a"]["pearson"])),
        "abs_delta_sign_ZL3b": abs(int(primary["topology"]["ZL3b"]["sign_agreement"]) - int(secondary["topology"]["ZL3b"]["sign_agreement"])),
        "abs_delta_sign_IT2a": abs(int(primary["topology"]["IT2a"]["sign_agreement"]) - int(secondary["topology"]["IT2a"]["sign_agreement"])),
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (5, 6):
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT REP OUTPUT_JSON [--primary-only]")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    rep = int(argv[3])
    out = Path(argv[4]).resolve()
    primary_only = len(argv) == 6 and argv[5] == "--primary-only"
    if rep not in range(5):
        raise SystemExit("REP must be 0..4")
    if len(argv) == 6 and not primary_only:
        raise SystemExit("only optional flag is --primary-only")

    b0 = load_b0()
    targets, target_authority = t68.load_target_references()
    d = build_dataset(crem, nai, rep, b0)
    real_q = t68.q_views_candidate(d, d["X"], True)
    primary = calibration(d, real_q, targets, PRIMARY_NS[rep])
    if rep == 0:
        # This gate executes before a workflow is allowed to score rep1..rep4.
        check_rep0_primary(primary)

    result = {
        "schema": "issue72-v2-stage-b1-per-rep-r1-calibration-v1",
        "scientific_role": "UNCHANGED_NAIBBE_POSITIVE_CONTROL_CALIBRATION",
        "rep": rep,
        "surface": {
            "sha256": d["surface_sha256"],
            "visible_tokens": d["visible"],
            "parsed_tokens": d["parsed"],
            "coverage": d["coverage"],
            "fold_parsed_tokens": d["fold_counts"],
            "line_count_with_parsed_token": d["line_count"],
            "per_manuscript": d["per_manuscript"],
        },
        "target_authority": target_authority,
        "primary": primary,
        "secondary": None,
        "calibration_noise": None,
        "classification": None,
        "p_values_computed": False,
        "test_nulls_computed": False,
        "issue72_intervention_surface_loaded_or_generated": False,
        "issue72_intervention_R1_computed": False,
    }
    if not primary_only:
        secondary = calibration(d, real_q, targets, SECONDARY_NS[rep])
        result["secondary"] = secondary
        result["calibration_noise"] = paired_noise(primary, secondary)

    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(json.dumps({
        "rep": rep,
        "primary_only": primary_only,
        "surface_sha256": d["surface_sha256"],
        "coverage": d["coverage"],
        "primary": {
            "E": primary["residual_energy"],
            "W": primary["reliability"]["median"],
            "R_ZL3b": primary["topology"]["ZL3b"]["pearson"],
            "R_IT2a": primary["topology"]["IT2a"]["pearson"],
            "sign_ZL3b": primary["topology"]["ZL3b"]["sign_agreement"],
            "sign_IT2a": primary["topology"]["IT2a"]["sign_agreement"],
        },
        "calibration_noise": result["calibration_noise"],
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
