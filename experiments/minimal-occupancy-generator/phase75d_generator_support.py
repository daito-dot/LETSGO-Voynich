#!/usr/bin/env python3
"""Issue #75 Phase D0 target-blind M4-KRS-DISTANCE generator.

Fits the preregistered descriptor-conditioned distance-banded maximum-entropy
model by physical-leaf cross-fitting and freezes 31 occupancy corpora without
computing Q/Z or loading any target topology.

Usage:
    python phase75d_generator_support.py ZL3B_PATH OUTPUT_JSON
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
import phase75b_generator_support as bgen  # noqa: E402

PLAN_D_PATH = HERE / "PLAN_D.md"
FAMILY = "M4-KRS-DISTANCE"
N_REPS = 31
N_FOLDS = 5
N_SLOTS = 12
DISTANCES = tuple(range(2, 12))
FREE_DISTANCES = tuple(range(3, 12))
N_DISTANCE = len(DISTANCES)
N_FREE = 20
FIT_TOL = 1e-10
FIT_MAX_ITER = 160
RIDGE = 1e-12

STATES = a0.STATES
STATE_FLOAT = a0.STATE_FLOAT
STATE_DISTANCE = np.stack(
    [
        (STATES[:, : N_SLOTS - d] * STATES[:, d:]).sum(axis=1)
        for d in DISTANCES
    ],
    axis=1,
).astype(np.float64)
FREE_FEATURES = np.concatenate([STATE_FLOAT[:, 1:], STATE_DISTANCE[:, 1:]], axis=1)
if FREE_FEATURES.shape != (4095, N_FREE):
    raise RuntimeError("M4 free-feature state space mismatch")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def empirical_moments(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X = np.asarray(X, dtype=np.float64)
    unary = X.mean(axis=0)
    distance = np.asarray(
        [
            np.mean((X[:, : N_SLOTS - d] * X[:, d:]).sum(axis=1))
            for d in DISTANCES
        ],
        dtype=np.float64,
    )
    return unary, distance


def descriptor_identity_audit(
    unary: np.ndarray,
    distance: np.ndarray,
    q: Mapping[tuple[int, int, int], float],
) -> dict:
    expected_k = float(sum(float(p) * d[0] for d, p in q.items()))
    expected_nonadj = float(
        sum(
            float(p) * (math.comb(int(d[0]), 2) - (int(d[0]) - int(d[1])))
            for d, p in q.items()
        )
    )
    observed_k = float(np.sum(unary))
    observed_nonadj = float(np.sum(distance))
    err_k = abs(observed_k - expected_k)
    err_nonadj = abs(observed_nonadj - expected_nonadj)
    if err_k > 1e-12 or err_nonadj > 1e-12:
        raise RuntimeError(
            "descriptor moment identities failed: "
            f"K={err_k:.17g}, nonadjacent={err_nonadj:.17g}"
        )
    return {
        "expected_K_from_descriptor_q": expected_k,
        "observed_sum_unary": observed_k,
        "abs_error_K_identity": err_k,
        "expected_nonadjacent_pairs_from_descriptor_q": expected_nonadj,
        "observed_sum_distance_joint": observed_nonadj,
        "abs_error_nonadjacent_identity": err_nonadj,
    }


def distribution(
    theta: np.ndarray,
    q: Mapping[tuple[int, int, int], float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    theta = np.asarray(theta, dtype=np.float64)
    if theta.shape != (N_FREE,):
        raise RuntimeError("M4 theta shape mismatch")
    prob = np.zeros(len(STATES), dtype=np.float64)
    unary = np.zeros(N_SLOTS, dtype=np.float64)
    distance = np.zeros(N_DISTANCE, dtype=np.float64)
    for desc in sorted(q):
        idx = bgen.DESC_TO_INDEX[desc]
        logits = FREE_FEATURES[idx] @ theta
        pd = a0.softmax(logits)
        w = float(q[desc])
        prob[idx] = w * pd
        unary += w * (pd @ STATE_FLOAT[idx])
        distance += w * (pd @ STATE_DISTANCE[idx])
    if abs(float(prob.sum()) - 1.0) > 1e-12:
        raise RuntimeError("M4 probability normalization failed")
    return prob, unary, distance


def fit_m4(X: np.ndarray) -> dict:
    X = np.asarray(X, dtype=np.uint8)
    target_unary, target_distance = empirical_moments(X)
    q = bgen.q_from_training(X)
    identity = descriptor_identity_audit(target_unary, target_distance, q)
    target_free = np.concatenate([target_unary[1:], target_distance[1:]])
    theta = np.zeros(N_FREE, dtype=np.float64)

    def objective(v: np.ndarray) -> float:
        z = 0.0
        for desc in sorted(q):
            idx = bgen.DESC_TO_INDEX[desc]
            z += float(q[desc]) * a0.logsumexp(FREE_FEATURES[idx] @ v)
        return float(z - target_free @ v)

    converged = False
    for it in range(FIT_MAX_ITER):
        model_unary = np.zeros(N_SLOTS, dtype=np.float64)
        model_distance = np.zeros(N_DISTANCE, dtype=np.float64)
        covariance = np.zeros((N_FREE, N_FREE), dtype=np.float64)
        for desc in sorted(q):
            idx = bgen.DESC_TO_INDEX[desc]
            F = FREE_FEATURES[idx]
            pd = a0.softmax(F @ theta)
            w = float(q[desc])
            muf = pd @ F
            model_unary += w * (pd @ STATE_FLOAT[idx])
            model_distance += w * (pd @ STATE_DISTANCE[idx])
            second = (F.T * pd) @ F
            covariance += w * (second - np.outer(muf, muf))

        full_error = np.concatenate(
            [target_unary - model_unary, target_distance - model_distance]
        )
        maxerr = float(np.max(np.abs(full_error)))
        if maxerr <= FIT_TOL:
            converged = True
            break

        model_free = np.concatenate([model_unary[1:], model_distance[1:]])
        err_free = target_free - model_free
        step = np.linalg.solve(covariance + RIDGE * np.eye(N_FREE), err_free)
        old_obj = objective(theta)
        alpha = 1.0
        accepted = False
        for _ in range(80):
            cand = theta + alpha * step
            _p2, u2, d2 = distribution(cand, q)
            err2 = float(
                np.max(
                    np.abs(
                        np.concatenate([target_unary - u2, target_distance - d2])
                    )
                )
            )
            obj2 = objective(cand)
            slack = 1e-12 * max(1.0, abs(old_obj))
            if err2 < maxerr and obj2 <= old_obj + slack:
                theta = cand
                accepted = True
                break
            alpha *= 0.5
        if not accepted:
            raise RuntimeError(
                f"M4 deterministic moment damping failed at iteration {it}: "
                f"maxerr={maxerr:.17g}"
            )

    prob, model_unary, model_distance = distribution(theta, q)
    maxerr = float(
        np.max(
            np.abs(
                np.concatenate(
                    [target_unary - model_unary, target_distance - model_distance]
                )
            )
        )
    )
    if not converged and maxerr > FIT_TOL:
        raise RuntimeError(f"M4 fit did not converge: maxerr={maxerr}")

    h = np.zeros(N_SLOTS, dtype=np.float64)
    h[1:] = theta[:11]
    J_distance = {2: 0.0}
    for i, d in enumerate(FREE_DISTANCES):
        J_distance[d] = float(theta[11 + i])

    counts = bgen.descriptor_counts(X)
    code = (
        X.astype(np.uint16)
        * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]
    ).sum(axis=1)
    descriptor_classes = []
    for desc in sorted(q):
        descriptor_classes.append(
            {
                "K": int(desc[0]),
                "R": int(desc[1]),
                "S": int(desc[2]),
                "train_count": int(counts[desc]),
                "probability": float(q[desc]),
                "possible_state_count": int(len(bgen.DESC_TO_INDEX[desc])),
            }
        )

    return {
        "h": h,
        "J_distance": J_distance,
        "prob": prob,
        "descriptor_q": q,
        "descriptor_classes": descriptor_classes,
        "descriptor_class_count": len(descriptor_classes),
        "descriptor_entropy_nats": bgen.descriptor_entropy(q),
        "training_distinct_signatures": int(len(np.unique(code))),
        "iterations": int(it + 1),
        "target_unary": target_unary,
        "target_distance_joint": target_distance,
        "model_unary": model_unary,
        "model_distance_joint": model_distance,
        "descriptor_identity_audit": identity,
        "max_abs_reported_moment_error": maxerr,
    }


def serialize_fit(x: Mapping) -> dict:
    return {
        "h": [float(v) for v in x["h"]],
        "J_distance": {str(d): float(x["J_distance"][d]) for d in DISTANCES},
        "gauge": {"h_0": 0.0, "J_2": 0.0},
        "free_unary_parameters": 11,
        "free_distance_parameters": 9,
        "free_continuous_parameters": N_FREE,
        "descriptor_classes": list(x["descriptor_classes"]),
        "descriptor_class_count": int(x["descriptor_class_count"]),
        "descriptor_entropy_nats": float(x["descriptor_entropy_nats"]),
        "training_distinct_signatures": int(x["training_distinct_signatures"]),
        "iterations": int(x["iterations"]),
        "target_unary": [float(v) for v in x["target_unary"]],
        "target_distance_joint": [float(v) for v in x["target_distance_joint"]],
        "model_unary": [float(v) for v in x["model_unary"]],
        "model_distance_joint": [float(v) for v in x["model_distance_joint"]],
        "distance_labels": [int(d) for d in DISTANCES],
        "descriptor_identity_audit": dict(x["descriptor_identity_audit"]),
        "max_abs_reported_moment_error": float(x["max_abs_reported_moment_error"]),
    }


def fit_crossfold(d: Mapping) -> dict[int, dict]:
    X = np.asarray(d["X"], dtype=np.uint8)
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = {}
    for f in range(N_FOLDS):
        train = X[folds != f]
        if len(train) != a0.EXPECTED_PARSED - a0.EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"M4 training population mismatch fold {f}")
        out[f] = fit_m4(train)
    return out


def generate_case(d: Mapping, fits: Mapping[int, Mapping], rep: int) -> np.ndarray:
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = np.zeros((a0.EXPECTED_PARSED, N_SLOTS), dtype=np.uint8)
    for f in range(N_FOLDS):
        mask = folds == f
        n = int(mask.sum())
        if n != a0.EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"M4 held-out population mismatch fold {f}")
        ns = f"issue75:phaseD:M4-KRS-DISTANCE:rep{rep}:fold{f}:generate"
        out[mask] = a0.sample_prob(
            np.asarray(fits[f]["prob"], dtype=np.float64), n, ns
        )
    if np.any(out.sum(axis=1) == 0):
        raise RuntimeError("M4 generated all-zero occupancy signature")
    return out


def occupancy_sha(X: np.ndarray) -> str:
    X = np.asarray(X, dtype=np.uint8)
    if X.shape != (a0.EXPECTED_PARSED, N_SLOTS):
        raise RuntimeError("M4 occupancy shape mismatch")
    return sha256_bytes(X.tobytes(order="C"))


def descriptor_summary(X: np.ndarray) -> dict:
    counts = bgen.descriptor_counts(X)
    total = float(len(X))
    return {
        "class_count": int(len(counts)),
        "classes": [
            {
                "K": int(desc[0]),
                "R": int(desc[1]),
                "S": int(desc[2]),
                "count": int(counts[desc]),
                "probability": float(counts[desc] / total),
            }
            for desc in sorted(counts)
        ],
    }


def case_summary(X: np.ndarray, rep: int, folds: np.ndarray) -> dict:
    unary, distance = empirical_moments(X)
    code = (
        X.astype(np.uint16)
        * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]
    ).sum(axis=1)
    return {
        "family": FAMILY,
        "rep": rep,
        "occupancy_sha256": occupancy_sha(X),
        "tokens": int(len(X)),
        "fold_tokens": [int(np.sum(folds == f)) for f in range(N_FOLDS)],
        "slot_marginals": [float(v) for v in unary],
        "distance_joint_occupancies": [float(v) for v in distance],
        "distance_labels": [int(d) for d in DISTANCES],
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

    if not PLAN_D_PATH.exists():
        raise RuntimeError("PLAN_D.md is required before Phase-D execution")
    plan_sha = sha256_file(PLAN_D_PATH)

    if a0.e.git_blob_sha1(src.read_bytes()) != a0.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = a0.e.SlotParser()
    a0.e.validate_parser(parser)
    d = a0.b58.build_dataset(src, parser, "min")
    if (
        d["source_blob"] != a0.EXPECTED_SOURCE_BLOB
        or d["visible"] != a0.EXPECTED_VISIBLE
        or d["parsed"] != a0.EXPECTED_PARSED
    ):
        raise RuntimeError("frozen source population mismatch")
    fold_counts = [int(np.sum(d["token_folds"] == f)) for f in range(N_FOLDS)]
    if fold_counts != a0.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen fold population mismatch: {fold_counts}")

    fits = fit_crossfold(d)
    fit_public = {str(f): serialize_fit(fits[f]) for f in range(N_FOLDS)}
    max_fit_err = max(
        fit_public[str(f)]["max_abs_reported_moment_error"]
        for f in range(N_FOLDS)
    )
    if max_fit_err > FIT_TOL:
        raise RuntimeError(f"M4 fit error exceeds tolerance: {max_fit_err}")

    folds = np.asarray(d["token_folds"], dtype=np.int8)
    cases = []
    for rep in range(N_REPS):
        Xg = generate_case(d, fits, rep)
        cases.append(case_summary(Xg, rep, folds))
    if len(cases) != N_REPS or {x["rep"] for x in cases} != set(range(N_REPS)):
        raise RuntimeError("M4 generated case population incomplete")
    if len({x["occupancy_sha256"] for x in cases}) != N_REPS:
        raise RuntimeError("M4 generated duplicate occupancy corpora")

    authority = {
        "schema": "issue75-phaseD0-m4-krs-distance-generator-authority-v1",
        "status": "M4_KRS_DISTANCE_31_CORPORA_FROZEN_TARGET_BLIND",
        "scientific_role": "PRETARGET_CROSSFITTED_KRS_DISTANCE_BANDED_GENERATOR_AUTHORITY",
        "family": FAMILY,
        "plan_d_sha256": plan_sha,
        "source": {
            "ZL3b_blob": str(d["source_blob"]),
            "visible_tokens": int(d["visible"]),
            "parsed_tokens": int(d["parsed"]),
            "fold_parsed_tokens": fold_counts,
            "parser_policy": "SlotParser(min)",
        },
        "model_definition": {
            "family": FAMILY,
            "descriptor": "exact training-only empirical P(K,R,S)",
            "conditional_family": "position-specific unary plus shared nonadjacent separation-distance interactions",
            "distance_terms": [int(d) for d in DISTANCES],
            "free_distance_terms": [int(d) for d in FREE_DISTANCES],
            "free_unary_parameters": 11,
            "free_distance_parameters": 9,
            "free_continuous_parameters": N_FREE,
            "explicit_pair_specific_nonadjacent_parameters": 0,
            "empirical_signature_specific_parameters": 0,
            "latent_state_parameters": 0,
            "gauges": {"h_0": 0.0, "J_2": 0.0},
            "state_space_nonempty_signatures": int(len(STATES)),
            "fit_tolerance": FIT_TOL,
            "fit_method": "exact deterministic damped Newton moment matching",
        },
        "fit": fit_public,
        "cases": cases,
        "target_access": {
            "pair_Q_computed": False,
            "residual_Z_computed": False,
            "Issue58C_target_vector_loaded": False,
            "Issue58D_target_vector_loaded": False,
            "target_correlation_computed": False,
            "target_sign_agreement_computed": False,
            "T_computed": False,
        },
        "no_drops": True,
        "no_rerolls": True,
        "fit_max_abs_reported_moment_error": float(max_fit_err),
    }

    raw = canonical_json_bytes(authority) + b"\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(
        json.dumps(
            {
                "status": authority["status"],
                "family": FAMILY,
                "plan_d_sha256": plan_sha,
                "cases": len(cases),
                "fit_max_abs_reported_moment_error": max_fit_err,
                "descriptor_class_counts": [
                    fit_public[str(f)]["descriptor_class_count"] for f in range(N_FOLDS)
                ],
                "generated_distinct_signature_range": [
                    min(x["distinct_signatures"] for x in cases),
                    max(x["distinct_signatures"] for x in cases),
                ],
                "target_access": authority["target_access"],
                "output_sha256": sha256_bytes(raw),
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
