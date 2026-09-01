#!/usr/bin/env python3
"""Issue #75 Phase A frozen candidate-owned R1 scorer.

For one preregistered family/replicate, regenerate the exact Stage-A0 occupancy
corpus and require its frozen SHA before any target access. With --verify-only,
stop before pair-Q/residual-Z/target loading. Otherwise compute the candidate's
own line-local residual calibration, then reveal the already-frozen ZL3b and
IT2a target vectors through target68.load_target_references().

Usage:
    python phase75a_score.py ZL3B_PATH FAMILY REP OUTPUT_JSON [--verify-only]
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in (
    "minimal-occupancy-generator",
    "issue26-music",
    "occupancy-graph-stability",
    "occupancy-graph-residual",
    "occupancy-graph-independent-transcription",
    "joint-constraint-tournament",
):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase75a_generator_support as gen  # noqa: E402
import issue26e_core as e  # noqa: E402
import phase58b_graph_stability as b58  # noqa: E402
import target68 as t68  # noqa: E402

PLAN_COMMIT = "8d984cfa61a5616bef61b45248c0a7a5d213fbf8"
A0_AUTHORITY_COMMIT = "c703b2d01c941b6bfd17758f09868c71a200f212"
A0_PATH = HERE.parent / "stage-a0" / "generator_authority.json"
A0_SHA256 = "83e5808576a6416e4b03e302242805509c05d16928403d3a58e5636bdbf9ecd2"
EXPECTED_SOURCE_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
FAMILIES = ("M0", "M1", "MPLUS-A", "MPLUS-B")
N_REPS = 31
N_REF = 1000
N_TEST = 1000
N_FOLDS = 5
N_EDGES = 66


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load_a0_authority() -> tuple[dict, dict[tuple[str, int], dict]]:
    got = sha256_file(A0_PATH)
    if got != A0_SHA256:
        raise RuntimeError(f"Stage A0 authority SHA changed: {got} != {A0_SHA256}")
    r = json.loads(A0_PATH.read_text(encoding="utf-8"))
    if r.get("schema") != "issue75-phaseA0-minimal-occupancy-generator-authority-v1":
        raise RuntimeError("Stage A0 schema changed")
    if r.get("status") != "M0_M1_MPLUS_124_CORPORA_FROZEN_TARGET_BLIND":
        raise RuntimeError("Stage A0 status changed")
    if r.get("plan_commit") != PLAN_COMMIT:
        raise RuntimeError("Stage A0 plan authority changed")
    if any(r.get("target_access", {}).values()):
        raise RuntimeError("Stage A0 target firewall is not clean")
    if r.get("no_drops") is not True or r.get("no_rerolls") is not True:
        raise RuntimeError("Stage A0 population integrity changed")
    cases = {}
    for x in r.get("cases", []):
        key = (str(x["family"]), int(x["rep"]))
        if key in cases:
            raise RuntimeError(f"duplicate Stage A0 case: {key}")
        cases[key] = x
    expected = {(f, rep) for f in FAMILIES for rep in range(N_REPS)}
    if set(cases) != expected:
        raise RuntimeError("Stage A0 case population changed")
    return r, cases


def build_exact_case(src: Path, family: str, rep: int, authority: Mapping, cases: Mapping) -> tuple[dict, np.ndarray, dict]:
    if e.git_blob_sha1(src.read_bytes()) != EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = e.SlotParser()
    e.validate_parser(parser)
    d = b58.build_dataset(src, parser, "min")
    if d["source_blob"] != EXPECTED_SOURCE_BLOB or d["visible"] != gen.EXPECTED_VISIBLE or d["parsed"] != gen.EXPECTED_PARSED:
        raise RuntimeError("frozen ZL3b parsed population changed")
    fold_counts = [int(np.sum(d["token_folds"] == f)) for f in range(N_FOLDS)]
    if fold_counts != gen.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen fold counts changed: {fold_counts}")

    fits = gen.fit_models(d)
    fit_public = {
        fam: {str(f): gen.serialize_fit(fits[fam][f]) for f in range(N_FOLDS)}
        for fam in ("M0", "M1")
    }
    if fit_public != authority["fit"]:
        raise RuntimeError("deterministic M0/M1 fit no longer matches Stage A0 authority")

    X = gen.generate_case(d, fits, family, rep)
    got_sha = gen.occupancy_sha(X)
    frozen = cases[(family, rep)]
    if got_sha != frozen["occupancy_sha256"]:
        raise RuntimeError(f"generated occupancy SHA changed for {(family, rep)}: {got_sha}")
    if int(len(X)) != gen.EXPECTED_PARSED or np.any(X.sum(axis=1) == 0):
        raise RuntimeError("regenerated occupancy population changed")

    padded = np.zeros_like(d["padded"], dtype=np.uint8)
    padded[d["line_mask"]] = X
    if not np.array_equal(padded[d["line_mask"]], X):
        raise RuntimeError("generated padded/flat ordering mismatch")
    candidate = {
        "X": X,
        "token_folds": np.asarray(d["token_folds"], dtype=np.int8),
        "padded": padded,
        "line_mask": np.asarray(d["line_mask"], dtype=bool),
    }
    audit = {
        "family": family,
        "rep": rep,
        "occupancy_sha256": got_sha,
        "stage_a0_authority_sha256": A0_SHA256,
        "stage_a0_authority_commit": A0_AUTHORITY_COMMIT,
        "tokens": int(len(X)),
        "fold_tokens": fold_counts,
        "line_count": int(candidate["line_mask"].shape[0]),
        "line_token_count_digest": sha256_bytes(candidate["line_mask"].sum(axis=1).astype(np.int32).tobytes()),
        "all_zero_count": int(np.sum(X.sum(axis=1) == 0)),
        "frozen_case": frozen,
        "exact_stage_a0_replay": True,
    }
    return candidate, X, audit


def q_views_all(candidate: Mapping, X: np.ndarray, include_folds: bool = True) -> dict:
    code = b58.pair_codes(np.asarray(X, dtype=np.uint8))
    folds = np.asarray(candidate["token_folds"], dtype=np.int64)
    cf = b58.partition_counts(code, folds, N_FOLDS, True)
    total = cf.sum(axis=0)
    out = {"full": b58.q_cond(total)}
    if include_folds:
        out["held"] = np.stack([b58.q_cond(cf[f]) for f in range(N_FOLDS)])
        out["train"] = np.stack([b58.q_cond(total - cf[f]) for f in range(N_FOLDS)])
    return out


def shuffled_flat(candidate: Mapping, namespace: str, null_index: int) -> np.ndarray:
    rng = np.random.default_rng(e.stable_seed(f"{namespace}:{null_index}"))
    padded = np.asarray(candidate["padded"], dtype=np.uint8)
    line_mask = np.asarray(candidate["line_mask"], dtype=bool)
    keys = rng.random(padded.shape)
    keys[~line_mask] = 2.0
    order = np.argsort(keys, axis=1, kind="stable")
    shuffled = np.take_along_axis(padded, order, axis=1)
    shuffled[~line_mask] = 0
    if null_index == 0 and not np.array_equal(padded.sum(axis=1), shuffled.sum(axis=1)):
        raise RuntimeError(f"candidate null failed line x slot marginal preservation: {namespace}")
    return shuffled[line_mask]


def normal_score_array(q: np.ndarray, sorted_ref: np.ndarray) -> np.ndarray:
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


def residual_energy(z: np.ndarray) -> float:
    z = np.asarray(z, dtype=np.float64)
    return float(np.sqrt(np.mean(z * z)))


def finite_corr(a: np.ndarray, b: np.ndarray) -> float | None:
    r = b58.corr(np.asarray(a, dtype=float), np.asarray(b, dtype=float))
    return None if r is None else float(r)


def median_finite(xs: Sequence[float | None], minimum: int = 4) -> float | None:
    vals = [float(x) for x in xs if x is not None and math.isfinite(float(x))]
    return None if len(vals) < minimum else float(np.median(vals))


def build_reference(candidate: Mapping, namespace: str) -> dict:
    full = np.empty((N_REF, N_EDGES), dtype=np.float64)
    train = np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64)
    held = np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64)
    for n in range(N_REF):
        Y = shuffled_flat(candidate, namespace, n)
        qv = q_views_all(candidate, Y, include_folds=True)
        full[n] = qv["full"]
        train[n] = qv["train"]
        held[n] = qv["held"]
    return {
        "full": np.sort(full, axis=0),
        "train": np.sort(train, axis=0),
        "held": np.sort(held, axis=0),
    }


def candidate_measurement(candidate: Mapping, X: np.ndarray, family: str, rep: int) -> dict:
    reference_ns = f"issue75:phaseA:{family}:rep{rep}:reference"
    test_ns = f"issue75:phaseA:{family}:rep{rep}:test"
    if reference_ns == test_ns:
        raise RuntimeError("reference/test namespace collision")

    real_q = q_views_all(candidate, X, include_folds=True)
    sref = build_reference(candidate, reference_ns)
    z_full = normal_score_array(real_q["full"], sref["full"])
    z_train = normal_score_array(real_q["train"], sref["train"])
    z_held = normal_score_array(real_q["held"], sref["held"])
    E = residual_energy(z_full)
    fold_r = [finite_corr(z_train[f], z_held[f]) for f in range(N_FOLDS)]
    W = median_finite(fold_r)

    test_energy = np.empty(N_TEST, dtype=np.float64)
    for n in range(N_TEST):
        Y = shuffled_flat(candidate, test_ns, n)
        q = q_views_all(candidate, Y, include_folds=False)["full"]
        z = normal_score_array(q, sref["full"])
        test_energy[n] = residual_energy(z)
    p_exist = float((1 + int(np.sum(test_energy >= E))) / (N_TEST + 1))

    return {
        "reference_namespace": reference_ns,
        "test_namespace": test_ns,
        "n_reference": N_REF,
        "n_test": N_TEST,
        "residual_energy": E,
        "p_exist": p_exist,
        "reliability": {"fold_correlations": fold_r, "median": W},
        "z_full": [float(v) for v in z_full],
        "test_energy_summary": {
            "min": float(np.min(test_energy)),
            "median": float(np.median(test_energy)),
            "q95": float(np.quantile(test_energy, 0.95)),
            "max": float(np.max(test_energy)),
        },
    }


def sign_agreement(a: np.ndarray, b: np.ndarray) -> int:
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if a.shape != (N_EDGES,) or b.shape != (N_EDGES,):
        raise RuntimeError("sign-agreement vector shape mismatch")
    return int(np.sum(np.sign(a) == np.sign(b)))


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (5, 6):
        raise SystemExit(f"usage: {argv[0]} ZL3B_PATH FAMILY REP OUTPUT_JSON [--verify-only]")
    src = Path(argv[1]).resolve()
    family = argv[2]
    rep = int(argv[3])
    out_path = Path(argv[4]).resolve()
    verify_only = len(argv) == 6 and argv[5] == "--verify-only"
    if family not in FAMILIES or rep not in range(N_REPS):
        raise SystemExit("FAMILY must be M0/M1/MPLUS-A/MPLUS-B and REP must be 0..30")
    if len(argv) == 6 and not verify_only:
        raise SystemExit("only optional flag is --verify-only")

    authority, cases = load_a0_authority()
    candidate, X, audit = build_exact_case(src, family, rep, authority, cases)

    common = {
        "plan_commit": PLAN_COMMIT,
        "family": family,
        "rep": rep,
        "candidate_audit": audit,
        "pair_count": N_EDGES,
        "target_readings_averaged": False,
        "no_case_selection": True,
        "no_reroll": True,
    }

    if verify_only:
        result = {
            "schema": "issue75-phaseA-r1-preflight-v1",
            "status": "EXACT_A0_CORPUS_REGENERATED_TARGET_BLIND",
            "scientific_role": "PRETARGET_EXACT_CORPUS_REPLAY_PREFLIGHT",
            **common,
            "target_access": {
                "pair_Q_computed": False,
                "residual_Z_computed": False,
                "Issue58C_target_vector_loaded": False,
                "Issue58D_target_vector_loaded": False,
                "target_correlation_computed": False,
                "target_sign_agreement_computed": False,
                "T_computed": False,
            },
        }
    else:
        measurement = candidate_measurement(candidate, X, family, rep)
        z = np.asarray(measurement["z_full"], dtype=np.float64)
        targets, target_authority = t68.load_target_references()
        topology = {}
        for name in ("ZL3b", "IT2a"):
            target = np.asarray(targets[name], dtype=np.float64)
            r = finite_corr(z, target)
            if r is None or not math.isfinite(r):
                raise RuntimeError(f"non-finite target topology correlation: {name}")
            topology[name] = {
                "pearson": float(r),
                "sign_agreement": sign_agreement(z, target),
                "sign_denominator": N_EDGES,
            }
        T = float(min(topology["ZL3b"]["pearson"], topology["IT2a"]["pearson"]))
        result = {
            "schema": "issue75-phaseA-r1-score-v1",
            "status": "PHASE_A_GENERATOR_R1_FIRST_REVEAL_CASE_SCORED",
            "scientific_role": "MINIMAL_OCCUPANCY_GENERATOR_COMPLETE_66_EDGE_MEASUREMENT",
            **common,
            "target_authority": target_authority,
            "measurement": measurement,
            "topology": topology,
            "T": T,
            "target_access": {
                "pair_Q_computed": True,
                "residual_Z_computed": True,
                "Issue58C_target_vector_loaded": True,
                "Issue58D_target_vector_loaded": True,
                "target_correlation_computed": True,
                "target_sign_agreement_computed": True,
                "T_computed": True,
            },
        }

    raw = canonical_json_bytes(result) + b"\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "family": family,
        "rep": rep,
        "verify_only": verify_only,
        "occupancy_sha256": audit["occupancy_sha256"],
        "E": None if verify_only else result["measurement"]["residual_energy"],
        "p_exist": None if verify_only else result["measurement"]["p_exist"],
        "W": None if verify_only else result["measurement"]["reliability"]["median"],
        "R_ZL3b": None if verify_only else result["topology"]["ZL3b"]["pearson"],
        "R_IT2a": None if verify_only else result["topology"]["IT2a"]["pearson"],
        "T": None if verify_only else result["T"],
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
