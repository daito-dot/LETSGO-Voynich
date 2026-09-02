#!/usr/bin/env python3
"""Issue #75 Phase B0 target-blind generic K/R/S occupancy generator.

Fits the preregistered M2-KRS model by physical-leaf cross-fitting and freezes
31 generated occupancy corpora without computing Q/Z or loading any target.

Usage:
    python phase75b_generator_support.py ZL3B_PATH OUTPUT_JSON
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75a_generator_support as a0  # noqa: E402

PLAN_B_COMMIT = "f09ba414de015eabd1eef03f275be68b82752d7f"
N_REPS = 31
N_FOLDS = 5
N_SLOTS = 12
FIT_TOL = 1e-10
FIT_MAX_ITER = 100
RIDGE = 1e-12
FAMILY = "M2-KRS"

STATES = a0.STATES
STATE_FLOAT = a0.STATE_FLOAT


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def descriptor_row(x: np.ndarray) -> tuple[int, int, int]:
    idx = np.flatnonzero(x)
    if len(idx) == 0:
        raise RuntimeError("descriptor undefined for all-zero signature")
    k = int(len(idx))
    span = int(idx[-1] - idx[0] + 1)
    runs = 1 + int(np.sum(np.diff(idx) > 1))
    return k, runs, span


STATE_DESC = tuple(descriptor_row(x) for x in STATES)
DESC_KEYS = tuple(sorted(set(STATE_DESC)))
DESC_TO_INDEX = {d: np.array([i for i, x in enumerate(STATE_DESC) if x == d], dtype=np.int64) for d in DESC_KEYS}


def descriptor_counts(X: np.ndarray) -> dict[tuple[int, int, int], int]:
    out: dict[tuple[int, int, int], int] = {}
    for x in np.asarray(X, dtype=np.uint8):
        d = descriptor_row(x)
        out[d] = out.get(d, 0) + 1
    return out


def descriptor_entropy(q: Mapping[tuple[int, int, int], float]) -> float:
    return float(-sum(p * math.log(p) for p in q.values() if p > 0))


def q_from_training(X: np.ndarray) -> dict[tuple[int, int, int], float]:
    counts = descriptor_counts(X)
    n = float(len(X))
    return {d: counts[d] / n for d in sorted(counts)}


def distribution(theta: np.ndarray, q: Mapping[tuple[int, int, int], float]) -> tuple[np.ndarray, np.ndarray]:
    lam = np.zeros(N_SLOTS, dtype=np.float64)
    lam[1:] = theta
    prob = np.zeros(len(STATES), dtype=np.float64)
    mu = np.zeros(N_SLOTS, dtype=np.float64)
    for d in sorted(q):
        p_d = float(q[d])
        idx = DESC_TO_INDEX[d]
        S = STATE_FLOAT[idx]
        pk = a0.softmax(S @ lam)
        prob[idx] = p_d * pk
        mu += p_d * (pk @ S)
    if abs(float(prob.sum()) - 1.0) > 1e-12:
        raise RuntimeError("M2-KRS probability normalization failed")
    return prob, mu


def fit_m2(X: np.ndarray) -> dict:
    X = np.asarray(X, dtype=np.uint8)
    target = X.mean(axis=0, dtype=np.float64)
    q = q_from_training(X)
    theta = np.zeros(N_SLOTS - 1, dtype=np.float64)
    target_free = target[1:]

    def objective(v: np.ndarray) -> float:
        lam = np.zeros(N_SLOTS, dtype=np.float64)
        lam[1:] = v
        z = 0.0
        for d in sorted(q):
            idx = DESC_TO_INDEX[d]
            z += q[d] * a0.logsumexp(STATE_FLOAT[idx] @ lam)
        return float(z - target_free @ v)

    converged = False
    for it in range(FIT_MAX_ITER):
        lam = np.zeros(N_SLOTS, dtype=np.float64)
        lam[1:] = theta
        mu = np.zeros(N_SLOTS, dtype=np.float64)
        cov_free = np.zeros((N_SLOTS - 1, N_SLOTS - 1), dtype=np.float64)
        for d in sorted(q):
            idx = DESC_TO_INDEX[d]
            S = STATE_FLOAT[idx]
            pd = a0.softmax(S @ lam)
            mud = pd @ S
            mu += q[d] * mud
            Sf = S[:, 1:]
            muf = mud[1:]
            second = (Sf.T * pd) @ Sf
            cov_free += q[d] * (second - np.outer(muf, muf))
        maxerr = float(np.max(np.abs(target - mu)))
        if maxerr <= FIT_TOL:
            converged = True
            break
        err_free = target_free - mu[1:]
        step = np.linalg.solve(cov_free + RIDGE * np.eye(N_SLOTS - 1), err_free)
        old_obj = objective(theta)
        alpha = 1.0
        accepted = False
        for _ in range(60):
            cand = theta + alpha * step
            _p2, mu2 = distribution(cand, q)
            err2 = float(np.max(np.abs(target - mu2)))
            obj2 = objective(cand)
            slack = 1e-12 * max(1.0, abs(old_obj))
            if err2 < maxerr and obj2 <= old_obj + slack:
                theta = cand
                accepted = True
                break
            alpha *= 0.5
        if not accepted:
            raise RuntimeError(f"M2-KRS deterministic moment damping failed at iteration {it}: maxerr={maxerr:.17g}")

    prob, mu = distribution(theta, q)
    maxerr = float(np.max(np.abs(target - mu)))
    if not converged and maxerr > FIT_TOL:
        raise RuntimeError(f"M2-KRS fit did not converge: maxerr={maxerr}")

    lam = np.zeros(N_SLOTS, dtype=np.float64)
    lam[1:] = theta
    counts = descriptor_counts(X)
    distinct_codes = np.unique((X.astype(np.uint16) * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]).sum(axis=1))
    class_records = []
    for d in sorted(q):
        k, runs, span = d
        class_records.append({
            "K": k,
            "R": runs,
            "S": span,
            "train_count": int(counts[d]),
            "probability": float(q[d]),
            "possible_state_count": int(len(DESC_TO_INDEX[d])),
        })
    return {
        "lambda": lam,
        "prob": prob,
        "descriptor_q": q,
        "descriptor_classes": class_records,
        "descriptor_class_count": len(class_records),
        "descriptor_entropy_nats": descriptor_entropy(q),
        "training_distinct_signatures": int(len(distinct_codes)),
        "iterations": int(it + 1),
        "target_marginals": target,
        "model_marginals": mu,
        "max_abs_marginal_error": maxerr,
    }


def serialize_fit(x: Mapping) -> dict:
    return {
        "lambda": [float(v) for v in x["lambda"]],
        "descriptor_classes": list(x["descriptor_classes"]),
        "descriptor_class_count": int(x["descriptor_class_count"]),
        "descriptor_entropy_nats": float(x["descriptor_entropy_nats"]),
        "training_distinct_signatures": int(x["training_distinct_signatures"]),
        "iterations": int(x["iterations"]),
        "target_marginals": [float(v) for v in x["target_marginals"]],
        "model_marginals": [float(v) for v in x["model_marginals"]],
        "max_abs_marginal_error": float(x["max_abs_marginal_error"]),
    }


def fit_crossfold(d: Mapping) -> dict[int, dict]:
    X = np.asarray(d["X"], dtype=np.uint8)
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = {}
    for f in range(N_FOLDS):
        train = X[folds != f]
        if len(train) != a0.EXPECTED_PARSED - a0.EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"training population mismatch fold {f}")
        out[f] = fit_m2(train)
    return out


def generate_case(d: Mapping, fits: Mapping[int, Mapping], rep: int) -> np.ndarray:
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    Xout = np.zeros((a0.EXPECTED_PARSED, N_SLOTS), dtype=np.uint8)
    for f in range(N_FOLDS):
        mask = folds == f
        n = int(mask.sum())
        if n != a0.EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"held-out population mismatch fold {f}")
        ns = f"issue75:phaseB:M2-KRS:rep{rep}:fold{f}:generate"
        Xout[mask] = a0.sample_prob(np.asarray(fits[f]["prob"], dtype=np.float64), n, ns)
    if np.any(Xout.sum(axis=1) == 0):
        raise RuntimeError("M2-KRS generated all-zero signature")
    return Xout


def occupancy_sha(X: np.ndarray) -> str:
    X = np.asarray(X, dtype=np.uint8)
    if X.shape != (a0.EXPECTED_PARSED, N_SLOTS):
        raise RuntimeError("M2-KRS occupancy shape mismatch")
    return sha256_bytes(X.tobytes(order="C"))


def descriptor_summary(X: np.ndarray) -> dict:
    counts = descriptor_counts(X)
    total = float(len(X))
    return {
        "class_count": int(len(counts)),
        "classes": [
            {"K": d[0], "R": d[1], "S": d[2], "count": int(counts[d]), "probability": float(counts[d] / total)}
            for d in sorted(counts)
        ],
    }


def case_summary(X: np.ndarray, rep: int, folds: np.ndarray) -> dict:
    code = (X.astype(np.uint16) * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]).sum(axis=1)
    return {
        "family": FAMILY,
        "rep": rep,
        "occupancy_sha256": occupancy_sha(X),
        "tokens": int(len(X)),
        "fold_tokens": [int(np.sum(folds == f)) for f in range(N_FOLDS)],
        "slot_marginals": [float(v) for v in X.mean(axis=0)],
        "descriptor_distribution": descriptor_summary(X),
        "distinct_signatures": int(len(np.unique(code))),
        "all_zero_count": int(np.sum(X.sum(axis=1) == 0)),
        "pair_Q_computed": False,
        "residual_Z_computed": False,
        "target_topology_loaded": False,
        "target_correlation_computed": False,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} ZL3B_PATH OUTPUT_JSON")
    src = Path(argv[1]).resolve()
    out_path = Path(argv[2]).resolve()

    if a0.e.git_blob_sha1(src.read_bytes()) != a0.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = a0.e.SlotParser()
    a0.e.validate_parser(parser)
    d = a0.b58.build_dataset(src, parser, "min")
    if d["source_blob"] != a0.EXPECTED_SOURCE_BLOB or d["visible"] != a0.EXPECTED_VISIBLE or d["parsed"] != a0.EXPECTED_PARSED:
        raise RuntimeError("frozen source population mismatch")
    fold_counts = [int(np.sum(d["token_folds"] == f)) for f in range(N_FOLDS)]
    if fold_counts != a0.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen fold population mismatch: {fold_counts}")

    fits = fit_crossfold(d)
    fit_public = {str(f): serialize_fit(fits[f]) for f in range(N_FOLDS)}
    max_fit_err = max(fit_public[str(f)]["max_abs_marginal_error"] for f in range(N_FOLDS))
    if max_fit_err > FIT_TOL:
        raise RuntimeError(f"M2-KRS fit error exceeds tolerance: {max_fit_err}")

    folds = np.asarray(d["token_folds"], dtype=np.int8)
    cases = []
    for rep in range(N_REPS):
        Xg = generate_case(d, fits, rep)
        cases.append(case_summary(Xg, rep, folds))
    if len(cases) != N_REPS or {x["rep"] for x in cases} != set(range(N_REPS)):
        raise RuntimeError("M2-KRS case population incomplete")
    if len({x["occupancy_sha256"] for x in cases}) != N_REPS:
        raise RuntimeError("unexpected duplicate M2-KRS corpus SHA")

    result = {
        "schema": "issue75-phaseB0-m2-krs-generator-authority-v1",
        "status": "M2_KRS_31_CORPORA_FROZEN_TARGET_BLIND",
        "scientific_role": "PRETARGET_CROSSFITTED_GENERIC_SHAPE_GENERATION_AUTHORITY",
        "plan_b_commit": PLAN_B_COMMIT,
        "source": {
            "ZL3b_blob": a0.EXPECTED_SOURCE_BLOB,
            "visible_tokens": a0.EXPECTED_VISIBLE,
            "parsed_tokens": a0.EXPECTED_PARSED,
            "fold_parsed_tokens": a0.EXPECTED_FOLD_PARSED,
            "parser_policy": "min",
        },
        "model_definition": {
            "family": FAMILY,
            "descriptor": "joint_training_distribution_of_K_occupied_run_count_R_and_occupied_span_S",
            "conditional_model": "descriptor_conditioned_maxent_slot_main_effects_lambda0_fixed_zero",
            "free_slot_main_effects": 11,
            "explicit_pair_interaction_parameters": 0,
            "empirical_signature_specific_parameters": 0,
            "state_space_nonempty_signatures": 4095,
            "n_reps": N_REPS,
            "crossfit_folds": N_FOLDS,
        },
        "fit": fit_public,
        "cases": cases,
        "target_access": {
            "Issue58C_target_vector_loaded": False,
            "Issue58D_target_vector_loaded": False,
            "pair_Q_computed": False,
            "residual_Z_computed": False,
            "target_correlation_computed": False,
            "classification_computed": False,
        },
        "no_drops": True,
        "no_rerolls": True,
    }
    raw = canonical_json_bytes(result) + b"\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "cases": len(cases),
        "fit_max_error": max_fit_err,
        "descriptor_class_count_by_fold": {str(f): fit_public[str(f)]["descriptor_class_count"] for f in range(N_FOLDS)},
        "descriptor_entropy_by_fold": {str(f): fit_public[str(f)]["descriptor_entropy_nats"] for f in range(N_FOLDS)},
        "training_distinct_signatures_by_fold": {str(f): fit_public[str(f)]["training_distinct_signatures"] for f in range(N_FOLDS)},
        "generated_distinct_signature_range": [min(x["distinct_signatures"] for x in cases), max(x["distinct_signatures"] for x in cases)],
        "output_sha256": sha256_bytes(raw),
        "target_loaded": False,
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
