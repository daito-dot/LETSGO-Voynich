#!/usr/bin/env python3
"""Issue #75 Phase A0 target-blind minimal occupancy-generator population.

This executable may parse the frozen ZL3b source into the already-established
12-slot occupancy representation and use training-fold low-order statistics.
It MUST NOT compute pair Q, residual Z, target topology, or any comparison with
Issue58C/Issue58D target vectors.

Usage:
    python phase75a_generator_support.py ZL3B_PATH OUTPUT_JSON
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
for rel in ("issue26-music", "occupancy-graph-stability"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import issue26e_core as e  # noqa: E402
import phase58b_graph_stability as b58  # noqa: E402

PLAN_COMMIT = "8d984cfa61a5616bef61b45248c0a7a5d213fbf8"
EXPECTED_SOURCE_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_VISIBLE = 32570
EXPECTED_PARSED = 25071
EXPECTED_FOLD_PARSED = [4430, 4810, 5516, 5447, 4868]
N_SLOTS = 12
N_FOLDS = 5
N_REPS = 31
FAMILIES = ("M0", "M1", "MPLUS-A", "MPLUS-B")
FIT_TOL = 1e-10
FIT_MAX_ITER = 100
RIDGE = 1e-12


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8], "big")


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def state_space() -> tuple[np.ndarray, np.ndarray]:
    masks = np.arange(1, 1 << N_SLOTS, dtype=np.uint16)
    states = ((masks[:, None] >> np.arange(N_SLOTS, dtype=np.uint16)[None, :]) & 1).astype(np.uint8)
    if states.shape != (4095, 12) or np.any(states.sum(axis=1) == 0):
        raise RuntimeError("non-empty occupancy state-space invariant failed")
    return masks, states


MASKS, STATES = state_space()
K_BY_STATE = STATES.sum(axis=1).astype(np.int8)
STATE_FLOAT = STATES.astype(np.float64)


def logsumexp(x: np.ndarray) -> float:
    m = float(np.max(x))
    return m + math.log(float(np.exp(x - m).sum()))


def softmax(x: np.ndarray) -> np.ndarray:
    m = float(np.max(x))
    w = np.exp(x - m)
    return w / float(w.sum())


def _newton_fit_m0(X: np.ndarray) -> dict:
    target = X.mean(axis=0, dtype=np.float64)
    lam = np.zeros(N_SLOTS, dtype=np.float64)

    def objective(v: np.ndarray) -> float:
        logits = STATE_FLOAT @ v
        return logsumexp(logits) - float(target @ v)

    converged = False
    for it in range(FIT_MAX_ITER):
        logits = STATE_FLOAT @ lam
        p = softmax(logits)
        mu = p @ STATE_FLOAT
        err = target - mu
        maxerr = float(np.max(np.abs(err)))
        if maxerr <= FIT_TOL:
            converged = True
            break
        second = (STATE_FLOAT.T * p) @ STATE_FLOAT
        cov = second - np.outer(mu, mu)
        step_vec = np.linalg.solve(cov + RIDGE * np.eye(N_SLOTS), err)
        old_obj = objective(lam)
        alpha = 1.0
        accepted = False
        for _ in range(40):
            cand = lam + alpha * step_vec
            if objective(cand) < old_obj:
                lam = cand
                accepted = True
                break
            alpha *= 0.5
        if not accepted:
            raise RuntimeError(f"M0 deterministic line search failed at iteration {it}")
    logits = STATE_FLOAT @ lam
    p = softmax(logits)
    mu = p @ STATE_FLOAT
    maxerr = float(np.max(np.abs(target - mu)))
    if not converged and maxerr > FIT_TOL:
        raise RuntimeError(f"M0 fit did not converge: maxerr={maxerr}")
    return {
        "lambda": lam,
        "prob": p,
        "iterations": int(it + 1),
        "target_marginals": target,
        "model_marginals": mu,
        "max_abs_marginal_error": maxerr,
    }


def _m1_distribution(theta: np.ndarray, qk: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lam = np.zeros(N_SLOTS, dtype=np.float64)
    lam[1:] = theta
    prob = np.zeros(len(STATES), dtype=np.float64)
    mu = np.zeros(N_SLOTS, dtype=np.float64)
    for k in range(1, N_SLOTS + 1):
        if qk[k] <= 0:
            continue
        idx = np.flatnonzero(K_BY_STATE == k)
        pk = softmax(STATE_FLOAT[idx] @ lam)
        prob[idx] = qk[k] * pk
        mu += qk[k] * (pk @ STATE_FLOAT[idx])
    if abs(float(prob.sum()) - 1.0) > 1e-12:
        raise RuntimeError("M1 probability normalization failed")
    return prob, mu


def _newton_fit_m1(X: np.ndarray) -> dict:
    target = X.mean(axis=0, dtype=np.float64)
    kvals = X.sum(axis=1).astype(np.int64)
    if np.any((kvals < 1) | (kvals > N_SLOTS)):
        raise RuntimeError("training occupancy contains invalid K")
    nk = np.bincount(kvals, minlength=N_SLOTS + 1).astype(np.float64)
    qk = nk / float(len(X))
    theta = np.zeros(N_SLOTS - 1, dtype=np.float64)
    target_free = target[1:]

    def objective(v: np.ndarray) -> float:
        lam = np.zeros(N_SLOTS, dtype=np.float64)
        lam[1:] = v
        z = 0.0
        for k in range(1, N_SLOTS + 1):
            if qk[k] <= 0:
                continue
            idx = np.flatnonzero(K_BY_STATE == k)
            z += qk[k] * logsumexp(STATE_FLOAT[idx] @ lam)
        return float(z - target_free @ v)

    converged = False
    for it in range(FIT_MAX_ITER):
        lam = np.zeros(N_SLOTS, dtype=np.float64)
        lam[1:] = theta
        mu = np.zeros(N_SLOTS, dtype=np.float64)
        cov_free = np.zeros((N_SLOTS - 1, N_SLOTS - 1), dtype=np.float64)
        for k in range(1, N_SLOTS + 1):
            if qk[k] <= 0:
                continue
            idx = np.flatnonzero(K_BY_STATE == k)
            S = STATE_FLOAT[idx]
            pk = softmax(S @ lam)
            muk = pk @ S
            mu += qk[k] * muk
            Sf = S[:, 1:]
            muf = muk[1:]
            second = (Sf.T * pk) @ Sf
            cov_free += qk[k] * (second - np.outer(muf, muf))
        err_free = target_free - mu[1:]
        maxerr = float(np.max(np.abs(target - mu)))
        if maxerr <= FIT_TOL:
            converged = True
            break
        step_vec = np.linalg.solve(cov_free + RIDGE * np.eye(N_SLOTS - 1), err_free)
        old_obj = objective(theta)
        alpha = 1.0
        accepted = False
        for _ in range(40):
            cand = theta + alpha * step_vec
            if objective(cand) < old_obj:
                theta = cand
                accepted = True
                break
            alpha *= 0.5
        if not accepted:
            raise RuntimeError(f"M1 deterministic line search failed at iteration {it}")
    prob, mu = _m1_distribution(theta, qk)
    maxerr = float(np.max(np.abs(target - mu)))
    if not converged and maxerr > FIT_TOL:
        raise RuntimeError(f"M1 fit did not converge: maxerr={maxerr}")
    lam = np.zeros(N_SLOTS, dtype=np.float64)
    lam[1:] = theta
    return {
        "lambda": lam,
        "prob": prob,
        "qk": qk,
        "iterations": int(it + 1),
        "target_marginals": target,
        "model_marginals": mu,
        "max_abs_marginal_error": maxerr,
    }


def fit_models(d: Mapping) -> dict:
    X = np.asarray(d["X"], dtype=np.uint8)
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = {"M0": {}, "M1": {}}
    for f in range(N_FOLDS):
        train = X[folds != f]
        if len(train) != EXPECTED_PARSED - EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"training population mismatch fold {f}")
        m0 = _newton_fit_m0(train)
        m1 = _newton_fit_m1(train)
        out["M0"][f] = m0
        out["M1"][f] = m1
    return out


def sample_prob(prob: np.ndarray, n: int, namespace: str) -> np.ndarray:
    rng = np.random.default_rng(stable_seed(namespace))
    idx = rng.choice(len(STATES), size=n, replace=True, p=prob)
    return STATES[idx].copy()


def sample_empirical(train: np.ndarray, n: int, namespace: str) -> np.ndarray:
    rng = np.random.default_rng(stable_seed(namespace))
    idx = rng.integers(0, len(train), size=n)
    return train[idx].copy()


def generate_case(d: Mapping, fits: Mapping, family: str, rep: int) -> np.ndarray:
    X = np.asarray(d["X"], dtype=np.uint8)
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = np.zeros_like(X)
    for f in range(N_FOLDS):
        mask = folds == f
        n = int(mask.sum())
        if n != EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"held-out population mismatch fold {f}: {n}")
        ns = f"issue75:phaseA:{family}:rep{rep}:fold{f}:generate"
        if family == "M0":
            gen = sample_prob(fits["M0"][f]["prob"], n, ns)
        elif family == "M1":
            gen = sample_prob(fits["M1"][f]["prob"], n, ns)
        elif family in ("MPLUS-A", "MPLUS-B"):
            train = X[folds != f]
            gen = sample_empirical(train, n, ns)
        else:
            raise RuntimeError(f"unknown family: {family}")
        out[mask] = gen
    if out.shape != (EXPECTED_PARSED, N_SLOTS):
        raise RuntimeError("generated corpus shape mismatch")
    if np.any(out.sum(axis=1) == 0):
        raise RuntimeError("generated all-zero occupancy signature")
    return out


def occupancy_sha(X: np.ndarray) -> str:
    X = np.asarray(X, dtype=np.uint8)
    if X.shape != (EXPECTED_PARSED, N_SLOTS):
        raise RuntimeError("occupancy hash shape mismatch")
    return sha256_bytes(X.tobytes(order="C"))


def case_summary(X: np.ndarray, family: str, rep: int, folds: np.ndarray) -> dict:
    counts = X.sum(axis=1).astype(np.int64)
    code = (X.astype(np.uint16) * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]).sum(axis=1)
    kdist = np.bincount(counts, minlength=N_SLOTS + 1).astype(np.int64)
    return {
        "family": family,
        "rep": rep,
        "occupancy_sha256": occupancy_sha(X),
        "tokens": int(len(X)),
        "fold_tokens": [int(np.sum(folds == f)) for f in range(N_FOLDS)],
        "slot_marginals": [float(v) for v in X.mean(axis=0)],
        "k_counts": [int(v) for v in kdist],
        "distinct_signatures": int(len(np.unique(code))),
        "all_zero_count": int(np.sum(counts == 0)),
        "pair_Q_computed": False,
        "residual_Z_computed": False,
        "target_topology_loaded": False,
        "target_correlation_computed": False,
    }


def serialize_fit(x: Mapping) -> dict:
    out = {
        "lambda": [float(v) for v in x["lambda"]],
        "iterations": int(x["iterations"]),
        "target_marginals": [float(v) for v in x["target_marginals"]],
        "model_marginals": [float(v) for v in x["model_marginals"]],
        "max_abs_marginal_error": float(x["max_abs_marginal_error"]),
    }
    if "qk" in x:
        out["qk"] = [float(v) for v in x["qk"]]
    return out


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} ZL3B_PATH OUTPUT_JSON")
    src = Path(argv[1]).resolve()
    out_path = Path(argv[2]).resolve()

    if e.git_blob_sha1(src.read_bytes()) != EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = e.SlotParser()
    e.validate_parser(parser)
    d = b58.build_dataset(src, parser, "min")
    if d["source_blob"] != EXPECTED_SOURCE_BLOB or d["visible"] != EXPECTED_VISIBLE or d["parsed"] != EXPECTED_PARSED:
        raise RuntimeError("frozen population mismatch")
    fold_counts = [int(np.sum(d["token_folds"] == f)) for f in range(N_FOLDS)]
    if fold_counts != EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"fold population mismatch: {fold_counts}")

    fits = fit_models(d)
    fit_public = {
        fam: {str(f): serialize_fit(fits[fam][f]) for f in range(N_FOLDS)}
        for fam in ("M0", "M1")
    }
    if max(fit_public[fam][str(f)]["max_abs_marginal_error"] for fam in ("M0", "M1") for f in range(N_FOLDS)) > FIT_TOL:
        raise RuntimeError("fitted marginal error exceeds frozen tolerance")

    cases = []
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    for family in FAMILIES:
        for rep in range(N_REPS):
            Xg = generate_case(d, fits, family, rep)
            cases.append(case_summary(Xg, family, rep, folds))

    if len(cases) != len(FAMILIES) * N_REPS:
        raise RuntimeError("generated case population mismatch")
    keys = {(x["family"], x["rep"]) for x in cases}
    expected = {(f, r) for f in FAMILIES for r in range(N_REPS)}
    if keys != expected:
        raise RuntimeError("generated case identities incomplete")
    if len({x["occupancy_sha256"] for x in cases}) != len(cases):
        raise RuntimeError("unexpected duplicate generated corpus SHA")

    result = {
        "schema": "issue75-phaseA0-minimal-occupancy-generator-authority-v1",
        "status": "M0_M1_MPLUS_124_CORPORA_FROZEN_TARGET_BLIND",
        "scientific_role": "PRETARGET_CROSSFITTED_OCCUPANCY_GENERATION_AUTHORITY",
        "plan_commit": PLAN_COMMIT,
        "source": {
            "ZL3b_blob": EXPECTED_SOURCE_BLOB,
            "visible_tokens": EXPECTED_VISIBLE,
            "parsed_tokens": EXPECTED_PARSED,
            "fold_parsed_tokens": EXPECTED_FOLD_PARSED,
            "parser_policy": "min",
        },
        "model_definition": {
            "M0": "nonempty_maxent_slot_main_effects_only",
            "M1": "empirical_K_distribution_plus_conditional_slot_main_effects_no_pair_terms",
            "MPLUS-A": "crossfitted_empirical_signature_resampling_positive_control_bank_A",
            "MPLUS-B": "crossfitted_empirical_signature_resampling_positive_control_bank_B",
            "state_space_nonempty_signatures": 4095,
            "n_reps_per_family": N_REPS,
            "crossfit_folds": N_FOLDS,
        },
        "fit": fit_public,
        "cases": cases,
        "target_access": {
            "Issue58C_target_vector_loaded": False,
            "Issue58D_target_vector_loaded": False,
            "pair_Q_computed": False,
            "residual_Z_computed": False,
            "model_target_correlation_computed": False,
            "model_target_sign_agreement_computed": False,
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
        "fit_max_error": max(fit_public[fam][str(f)]["max_abs_marginal_error"] for fam in ("M0", "M1") for f in range(N_FOLDS)),
        "family_distinct_signature_range": {
            fam: [
                min(x["distinct_signatures"] for x in cases if x["family"] == fam),
                max(x["distinct_signatures"] for x in cases if x["family"] == fam),
            ] for fam in FAMILIES
        },
        "output_sha256": sha256_bytes(raw),
        "target_loaded": False,
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
