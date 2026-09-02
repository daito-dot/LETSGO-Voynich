#!/usr/bin/env python3
"""Issue #75 Phase E0 target-blind M5-KRS-2MIX-CHAIN generator.

Fits a two-component mixture of Phase-C local K/R/S-conditioned chain
exponential families by exact conditional likelihood, using only training
physical leaves. No Q/Z or target topology is loaded here.

Usage:
    python phase75e_generator_support.py ZL3B_PATH OUTPUT_JSON
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75c_generator_support as cgen  # noqa: E402

PLAN_E_PATH = HERE / "PLAN_E.md"
FAMILY = "M5-KRS-2MIX-CHAIN"
N_REPS = 31
N_FOLDS = 5
N_SLOTS = 12
N_ADJ = 11
N_COMPONENT_FREE = 21
N_FREE = 43
N_STARTS = 9
PERTURB = 0.10
FIT_TOL = 1e-10
START_TIE_TOL = 1e-10
LL_NEST_TOL = 1e-8
GRAD_VALID_TOL = 1e-6
GRAD_CHECK_TOL = 1e-5
PI_MIN = 1e-8

STATES = cgen.STATES
STATE_FLOAT = cgen.STATE_FLOAT
STATE_ADJ = cgen.STATE_ADJ
FREE_FEATURES = cgen.FREE_FEATURES
if FREE_FEATURES.shape != (4095, 21):
    raise RuntimeError("M5 free feature space mismatch")

STATE_CODES = (
    STATES.astype(np.uint16)
    * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]
).sum(axis=1).astype(np.int64)
if len(np.unique(STATE_CODES)) != 4095 or int(STATE_CODES.min()) != 1 or int(STATE_CODES.max()) != 4095:
    raise RuntimeError("M5 state-code authority mismatch")
CODE_TO_INDEX = np.full(4096, -1, dtype=np.int64)
CODE_TO_INDEX[STATE_CODES] = np.arange(4095, dtype=np.int64)

DESCRIPTORS = tuple(sorted(cgen.bgen.DESC_TO_INDEX))
DESC_TO_ID = {d: i for i, d in enumerate(DESCRIPTORS)}
STATE_DESC_ID = np.full(4095, -1, dtype=np.int64)
for d, idx in cgen.bgen.DESC_TO_INDEX.items():
    STATE_DESC_ID[np.asarray(idx, dtype=np.int64)] = DESC_TO_ID[d]
if np.any(STATE_DESC_ID < 0):
    raise RuntimeError("M5 descriptor-state partition incomplete")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def theta_from_m3_fit(fit: Mapping) -> np.ndarray:
    h = np.asarray(fit["h"], dtype=np.float64)
    J = np.asarray(fit["J_adjacent"], dtype=np.float64)
    theta = np.concatenate([h[1:], J[1:]])
    if theta.shape != (N_COMPONENT_FREE,) or np.any(~np.isfinite(theta)):
        raise RuntimeError("invalid M3 baseline theta")
    return theta


def deterministic_direction(k: int) -> np.ndarray:
    if k not in range(1, 9):
        raise ValueError("split-start index must be 1..8")
    vals = []
    for j in range(N_COMPONENT_FREE):
        text = f"issue75:phaseE:M5-KRS-2MIX-CHAIN:init{k}:coord{j}".encode("utf-8")
        n = int.from_bytes(hashlib.sha256(text).digest()[:8], "big", signed=False)
        vals.append(((n + 0.5) / float(2**64)) - 0.5)
    v = np.asarray(vals, dtype=np.float64)
    norm = float(np.linalg.norm(v))
    if not math.isfinite(norm) or norm <= 0:
        raise RuntimeError("invalid deterministic split direction")
    v /= norm
    return v


def state_indices(X: np.ndarray) -> np.ndarray:
    code = (
        np.asarray(X, dtype=np.uint16)
        * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]
    ).sum(axis=1).astype(np.int64)
    idx = CODE_TO_INDEX[code]
    if np.any(idx < 0):
        raise RuntimeError("training corpus contains invalid/all-zero state")
    return idx


def state_counts(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    idx = state_indices(X)
    counts = np.bincount(idx, minlength=4095).astype(np.float64)
    if abs(float(counts.sum()) - len(X)) > 0:
        raise RuntimeError("training count compression failed")
    return idx, counts


def component_logprob_and_mu(theta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    theta = np.asarray(theta, dtype=np.float64)
    if theta.shape != (N_COMPONENT_FREE,) or np.any(~np.isfinite(theta)):
        raise RuntimeError("invalid component theta")
    logp = np.full(4095, -np.inf, dtype=np.float64)
    mu = np.zeros((len(DESCRIPTORS), N_COMPONENT_FREE), dtype=np.float64)
    for d in DESCRIPTORS:
        did = DESC_TO_ID[d]
        idx = np.asarray(cgen.bgen.DESC_TO_INDEX[d], dtype=np.int64)
        F = FREE_FEATURES[idx]
        logits = F @ theta
        lz = cgen.a0.logsumexp(logits)
        lp = logits - lz
        p = np.exp(lp)
        logp[idx] = lp
        mu[did] = p @ F
        if abs(float(p.sum()) - 1.0) > 1e-12:
            raise RuntimeError(f"component normalization failed descriptor {d}")
    if np.any(~np.isfinite(logp)):
        raise RuntimeError("component state coverage incomplete")
    return logp, mu


def unpack(v: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, float, float]:
    v = np.asarray(v, dtype=np.float64)
    if v.shape != (N_FREE,) or np.any(~np.isfinite(v)):
        raise RuntimeError("invalid M5 parameter vector")
    t0 = v[:21]
    t1 = v[21:42]
    eta = float(v[42])
    pi = float(expit(eta))
    logpi = float(-np.logaddexp(0.0, -eta))
    log1m = float(-np.logaddexp(0.0, eta))
    return t0, t1, eta, pi, logpi if math.isfinite(logpi) else -math.inf


def objective_gradient(v: np.ndarray, counts: np.ndarray) -> tuple[float, np.ndarray]:
    v = np.asarray(v, dtype=np.float64)
    t0 = v[:21]
    t1 = v[21:42]
    eta = float(v[42])
    pi = float(expit(eta))
    logpi = float(-np.logaddexp(0.0, -eta))
    log1m = float(-np.logaddexp(0.0, eta))
    lp0, mu0 = component_logprob_and_mu(t0)
    lp1, mu1 = component_logprob_and_mu(t1)

    obs = np.flatnonzero(counts > 0)
    c = counts[obs]
    la = log1m + lp0[obs]
    lb = logpi + lp1[obs]
    lm = np.logaddexp(la, lb)
    ll = float(c @ lm)
    r1 = np.exp(lb - lm)
    r0 = 1.0 - r1

    Fobs = FREE_FEATURES[obs]
    emp0 = (c * r0) @ Fobs
    emp1 = (c * r1) @ Fobs
    did = STATE_DESC_ID[obs]
    mass0 = np.bincount(did, weights=c * r0, minlength=len(DESCRIPTORS))
    mass1 = np.bincount(did, weights=c * r1, minlength=len(DESCRIPTORS))
    exp0 = mass0 @ mu0
    exp1 = mass1 @ mu1
    g0 = emp0 - exp0
    g1 = emp1 - exp1
    geta = float(np.sum(c * (r1 - pi)))
    grad = np.concatenate([g0, g1, np.asarray([geta])])
    if not math.isfinite(ll) or np.any(~np.isfinite(grad)):
        return math.inf, np.full(N_FREE, np.nan)
    return -ll, -grad


def finite_difference_gradient_check(counts: np.ndarray, theta_m3: np.ndarray) -> dict:
    d = deterministic_direction(1)
    v = np.concatenate([theta_m3 + 0.03 * d, theta_m3 - 0.02 * d, np.asarray([0.17])])
    f, g = objective_gradient(v, counts)
    if not math.isfinite(f) or np.any(~np.isfinite(g)):
        raise RuntimeError("analytic gradient check point non-finite")
    eps = 1e-6
    numeric = np.empty_like(g)
    for j in range(N_FREE):
        vp = v.copy(); vm = v.copy()
        vp[j] += eps; vm[j] -= eps
        fp, _ = objective_gradient(vp, counts)
        fm, _ = objective_gradient(vm, counts)
        numeric[j] = (fp - fm) / (2.0 * eps)
    abs_err = np.abs(g - numeric)
    scale = np.maximum(1.0, np.maximum(np.abs(g), np.abs(numeric)))
    relscaled = abs_err / scale
    max_abs = float(np.max(abs_err))
    max_scaled = float(np.max(relscaled))
    if max(max_abs, max_scaled) > GRAD_CHECK_TOL:
        raise RuntimeError(f"M5 analytic gradient audit failed abs={max_abs} scaled={max_scaled}")
    return {
        "epsilon": eps,
        "max_absolute_error": max_abs,
        "max_scaled_error": max_scaled,
        "tolerance": GRAD_CHECK_TOL,
        "passed": True,
    }


def conditional_loglik(theta: np.ndarray, counts: np.ndarray) -> float:
    lp, _ = component_logprob_and_mu(theta)
    obs = np.flatnonzero(counts > 0)
    return float(counts[obs] @ lp[obs])


def mixture_distribution(t0: np.ndarray, t1: np.ndarray, pi: float, q: Mapping) -> tuple[np.ndarray, dict]:
    lp0, _ = component_logprob_and_mu(t0)
    lp1, _ = component_logprob_and_mu(t1)
    cond0 = np.exp(lp0)
    cond1 = np.exp(lp1)
    prob = np.zeros(4095, dtype=np.float64)
    max_desc_norm_error = 0.0
    for d in sorted(q):
        idx = np.asarray(cgen.bgen.DESC_TO_INDEX[d], dtype=np.int64)
        mix = (1.0 - pi) * cond0[idx] + pi * cond1[idx]
        max_desc_norm_error = max(max_desc_norm_error, abs(float(mix.sum()) - 1.0))
        prob[idx] = float(q[d]) * mix
    total_error = abs(float(prob.sum()) - 1.0)
    if max_desc_norm_error > 1e-12 or total_error > 1e-12:
        raise RuntimeError(f"M5 mixture normalization failed desc={max_desc_norm_error} total={total_error}")
    return prob, {"max_descriptor_normalization_error": max_desc_norm_error, "total_normalization_error": total_error}


def component_expected(theta: np.ndarray, q: Mapping) -> dict:
    _prob, unary, adj = cgen.distribution(theta, q)
    return {
        "unary": [float(x) for x in unary],
        "adjacent_joint": [float(x) for x in adj],
    }


def canonicalize(t0: np.ndarray, t1: np.ndarray, pi: float, q: Mapping) -> tuple[np.ndarray, np.ndarray, float, dict]:
    before, _ = mixture_distribution(t0, t1, pi, q)
    e0 = component_expected(t0, q)
    e1 = component_expected(t1, q)
    u0 = np.asarray(e0["unary"], dtype=np.float64)
    u1 = np.asarray(e1["unary"], dtype=np.float64)

    swap = False
    reason = "slot1"
    diff = float(u0[1] - u1[1])
    if diff > 1e-12:
        swap = True
    elif abs(diff) <= 1e-12:
        reason = "unary_lexicographic"
        decided = False
        for s in range(1, 12):
            ds = float(u0[s] - u1[s])
            if abs(ds) > 1e-12:
                swap = ds > 0
                decided = True
                break
        if not decided:
            reason = "theta_lexicographic"
            for a, b in zip(t0, t1):
                dv = float(a - b)
                if abs(dv) > 1e-15:
                    swap = dv > 0
                    decided = True
                    break
            if not decided:
                reason = "exact_collapsed_order_preserved"
                swap = False

    if swap:
        nt0, nt1, npi = t1.copy(), t0.copy(), float(1.0 - pi)
    else:
        nt0, nt1, npi = t0.copy(), t1.copy(), float(pi)
    after, _ = mixture_distribution(nt0, nt1, npi, q)
    maxdiff = float(np.max(np.abs(before - after)))
    if maxdiff > 1e-15:
        raise RuntimeError(f"M5 label canonicalization changed distribution: {maxdiff}")
    return nt0, nt1, npi, {
        "swapped": bool(swap),
        "reason": reason,
        "max_abs_probability_change": maxdiff,
        "pre_component0_slot1": float(u0[1]),
        "pre_component1_slot1": float(u1[1]),
    }


def optimize_start(start_index: int, v0: np.ndarray, counts: np.ndarray) -> dict:
    result = minimize(
        fun=lambda v: objective_gradient(v, counts),
        x0=np.asarray(v0, dtype=np.float64),
        method="L-BFGS-B",
        jac=True,
        options={"maxiter": 2000, "ftol": 1e-12, "gtol": 1e-8, "maxls": 50},
    )
    f, g = objective_gradient(np.asarray(result.x, dtype=np.float64), counts)
    ll = -float(f)
    grad_inf = float(np.max(np.abs(g)))
    eta = float(result.x[42])
    pi = float(expit(eta))
    finite = bool(math.isfinite(ll) and math.isfinite(pi) and np.all(np.isfinite(result.x)) and np.all(np.isfinite(g)))
    pi_valid = bool(PI_MIN < pi < 1.0 - PI_MIN)
    opt_valid = bool(result.success or grad_inf <= GRAD_VALID_TOL)
    valid = bool(finite and pi_valid and opt_valid)
    return {
        "start_index": int(start_index),
        "initial_log_likelihood": float(-objective_gradient(v0, counts)[0]),
        "final_log_likelihood": ll,
        "optimizer_success": bool(result.success),
        "optimizer_status": int(result.status),
        "optimizer_message": str(result.message),
        "iterations": int(result.nit),
        "function_evaluations": int(result.nfev),
        "gradient_inf_norm": grad_inf,
        "pi": pi,
        "finite": finite,
        "pi_valid": pi_valid,
        "valid": valid,
        "x": np.asarray(result.x, dtype=np.float64),
    }


def fit_m5(X: np.ndarray, do_gradient_audit: bool) -> dict:
    X = np.asarray(X, dtype=np.uint8)
    _idx, counts = state_counts(X)
    q = cgen.bgen.q_from_training(X)
    base = cgen.fit_m3(X)
    theta_m3 = theta_from_m3_fit(base)
    ll_m3 = conditional_loglik(theta_m3, counts)
    grad_audit = finite_difference_gradient_check(counts, theta_m3) if do_gradient_audit else {"passed": True, "performed": False}

    starts = []
    vbase = np.concatenate([theta_m3, theta_m3, np.asarray([0.0])])
    starts.append(optimize_start(0, vbase, counts))
    for k in range(1, 9):
        u = deterministic_direction(k)
        v0 = np.concatenate([theta_m3 + PERTURB * u, theta_m3 - PERTURB * u, np.asarray([0.0])])
        starts.append(optimize_start(k, v0, counts))
    if len(starts) != N_STARTS or not starts[0]["valid"]:
        raise RuntimeError("M5 deterministic start population invalid")

    valid = [s for s in starts if s["valid"]]
    if not valid:
        raise RuntimeError("M5 has no valid optimization start")
    best = valid[0]
    for s in valid[1:]:
        if s["final_log_likelihood"] > best["final_log_likelihood"] + START_TIE_TOL:
            best = s
        elif abs(s["final_log_likelihood"] - best["final_log_likelihood"]) <= START_TIE_TOL and s["start_index"] < best["start_index"]:
            best = s

    if best["final_log_likelihood"] < ll_m3 - LL_NEST_TOL:
        raise RuntimeError(f"M5 selected likelihood below nested M3 baseline: {best['final_log_likelihood']} < {ll_m3}")

    raw = np.asarray(best["x"], dtype=np.float64)
    t0, t1 = raw[:21].copy(), raw[21:42].copy()
    pi = float(expit(float(raw[42])))
    t0, t1, pi, canonical = canonicalize(t0, t1, pi, q)
    prob, norm = mixture_distribution(t0, t1, pi, q)
    c0 = component_expected(t0, q)
    c1 = component_expected(t1, q)
    mix_unary = (1.0 - pi) * np.asarray(c0["unary"]) + pi * np.asarray(c1["unary"])
    mix_adj = (1.0 - pi) * np.asarray(c0["adjacent_joint"]) + pi * np.asarray(c1["adjacent_joint"])

    code = (
        X.astype(np.uint16)
        * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]
    ).sum(axis=1)
    desc_counts = cgen.bgen.descriptor_counts(X)
    desc_classes = [
        {
            "K": int(d[0]), "R": int(d[1]), "S": int(d[2]),
            "train_count": int(desc_counts[d]),
            "probability": float(q[d]),
            "possible_state_count": int(len(cgen.bgen.DESC_TO_INDEX[d])),
        }
        for d in sorted(q)
    ]

    public_starts = []
    for s in starts:
        public_starts.append({k: v for k, v in s.items() if k != "x"})

    return {
        "theta0": t0,
        "theta1": t1,
        "pi": pi,
        "prob": prob,
        "descriptor_q": q,
        "descriptor_classes": desc_classes,
        "descriptor_class_count": len(desc_classes),
        "descriptor_entropy_nats": cgen.bgen.descriptor_entropy(q),
        "training_distinct_signatures": int(len(np.unique(code))),
        "m3_baseline_fit_error": float(base["max_abs_reported_moment_error"]),
        "m3_baseline_log_likelihood": ll_m3,
        "selected_start_index": int(best["start_index"]),
        "selected_log_likelihood": float(best["final_log_likelihood"]),
        "selected_log_likelihood_gain_over_m3": float(best["final_log_likelihood"] - ll_m3),
        "all_starts": public_starts,
        "gradient_audit": grad_audit,
        "canonicalization": canonical,
        "normalization_audit": norm,
        "component0_expected": c0,
        "component1_expected": c1,
        "mixture_unary": [float(x) for x in mix_unary],
        "mixture_adjacent_joint": [float(x) for x in mix_adj],
    }


def serialize_fit(x: Mapping) -> dict:
    t0 = np.asarray(x["theta0"], dtype=np.float64)
    t1 = np.asarray(x["theta1"], dtype=np.float64)
    h0 = np.zeros(12); h1 = np.zeros(12); j0 = np.zeros(11); j1 = np.zeros(11)
    h0[1:] = t0[:11]; j0[1:] = t0[11:]
    h1[1:] = t1[:11]; j1[1:] = t1[11:]
    return {
        "pi": float(x["pi"]),
        "component0": {"h": [float(v) for v in h0], "J_adjacent": [float(v) for v in j0], "theta_free": [float(v) for v in t0]},
        "component1": {"h": [float(v) for v in h1], "J_adjacent": [float(v) for v in j1], "theta_free": [float(v) for v in t1]},
        "free_continuous_parameters": N_FREE,
        "explicit_nonadjacent_parameters": 0,
        "generic_distance_parameters": 0,
        "signature_specific_parameters": 0,
        "descriptor_classes": list(x["descriptor_classes"]),
        "descriptor_class_count": int(x["descriptor_class_count"]),
        "descriptor_entropy_nats": float(x["descriptor_entropy_nats"]),
        "training_distinct_signatures": int(x["training_distinct_signatures"]),
        "m3_baseline_fit_error": float(x["m3_baseline_fit_error"]),
        "m3_baseline_log_likelihood": float(x["m3_baseline_log_likelihood"]),
        "selected_start_index": int(x["selected_start_index"]),
        "selected_log_likelihood": float(x["selected_log_likelihood"]),
        "selected_log_likelihood_gain_over_m3": float(x["selected_log_likelihood_gain_over_m3"]),
        "all_starts": list(x["all_starts"]),
        "gradient_audit": dict(x["gradient_audit"]),
        "canonicalization": dict(x["canonicalization"]),
        "normalization_audit": dict(x["normalization_audit"]),
        "component0_expected": dict(x["component0_expected"]),
        "component1_expected": dict(x["component1_expected"]),
        "mixture_unary": list(x["mixture_unary"]),
        "mixture_adjacent_joint": list(x["mixture_adjacent_joint"]),
    }


def fit_crossfold(d: Mapping) -> dict[int, dict]:
    X = np.asarray(d["X"], dtype=np.uint8)
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = {}
    for f in range(N_FOLDS):
        train = X[folds != f]
        if len(train) != cgen.a0.EXPECTED_PARSED - cgen.a0.EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"M5 training population mismatch fold {f}")
        out[f] = fit_m5(train, do_gradient_audit=(f == 0))
    return out


def generate_case(d: Mapping, fits: Mapping[int, Mapping], rep: int) -> np.ndarray:
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = np.zeros((cgen.a0.EXPECTED_PARSED, N_SLOTS), dtype=np.uint8)
    for f in range(N_FOLDS):
        mask = folds == f
        n = int(mask.sum())
        if n != cgen.a0.EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"M5 held-out population mismatch fold {f}")
        ns = f"issue75:phaseE:M5-KRS-2MIX-CHAIN:rep{rep}:fold{f}:generate"
        out[mask] = cgen.a0.sample_prob(np.asarray(fits[f]["prob"], dtype=np.float64), n, ns)
    if np.any(out.sum(axis=1) == 0):
        raise RuntimeError("M5 generated all-zero occupancy signature")
    return out


def occupancy_sha(X: np.ndarray) -> str:
    X = np.asarray(X, dtype=np.uint8)
    if X.shape != (cgen.a0.EXPECTED_PARSED, N_SLOTS):
        raise RuntimeError("M5 occupancy shape mismatch")
    return sha256_bytes(X.tobytes(order="C"))


def case_summary(X: np.ndarray, rep: int, folds: np.ndarray) -> dict:
    unary, adj = cgen.empirical_moments(X)
    code = (
        X.astype(np.uint16)
        * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]
    ).sum(axis=1)
    counts = cgen.bgen.descriptor_counts(X)
    total = float(len(X))
    return {
        "family": FAMILY,
        "rep": int(rep),
        "occupancy_sha256": occupancy_sha(X),
        "tokens": int(len(X)),
        "fold_tokens": [int(np.sum(folds == f)) for f in range(N_FOLDS)],
        "slot_marginals": [float(v) for v in unary],
        "adjacent_joint_occupancies": [float(v) for v in adj],
        "descriptor_distribution": {
            "class_count": int(len(counts)),
            "classes": [
                {"K": int(d[0]), "R": int(d[1]), "S": int(d[2]), "count": int(counts[d]), "probability": float(counts[d] / total)}
                for d in sorted(counts)
            ],
        },
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
    if not PLAN_E_PATH.exists():
        raise RuntimeError("PLAN_E.md required before Phase-E execution")
    plan_sha = sha256_file(PLAN_E_PATH)

    if cgen.a0.e.git_blob_sha1(src.read_bytes()) != cgen.a0.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = cgen.a0.e.SlotParser()
    cgen.a0.e.validate_parser(parser)
    d = cgen.a0.b58.build_dataset(src, parser, "min")
    if d["source_blob"] != cgen.a0.EXPECTED_SOURCE_BLOB or d["visible"] != cgen.a0.EXPECTED_VISIBLE or d["parsed"] != cgen.a0.EXPECTED_PARSED:
        raise RuntimeError("frozen source population mismatch")
    fold_counts = [int(np.sum(d["token_folds"] == f)) for f in range(N_FOLDS)]
    if fold_counts != cgen.a0.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen fold population mismatch: {fold_counts}")

    fits = fit_crossfold(d)
    fit_public = {str(f): serialize_fit(fits[f]) for f in range(N_FOLDS)}
    for f in range(N_FOLDS):
        x = fit_public[str(f)]
        if x["selected_log_likelihood"] < x["m3_baseline_log_likelihood"] - LL_NEST_TOL:
            raise RuntimeError(f"nested likelihood audit failed fold {f}")
        if x["normalization_audit"]["max_descriptor_normalization_error"] > 1e-12:
            raise RuntimeError(f"normalization audit failed fold {f}")

    folds = np.asarray(d["token_folds"], dtype=np.int8)
    cases = []
    for rep in range(N_REPS):
        Xg = generate_case(d, fits, rep)
        cases.append(case_summary(Xg, rep, folds))
    if len(cases) != N_REPS or {x["rep"] for x in cases} != set(range(N_REPS)):
        raise RuntimeError("M5 generated case population incomplete")
    if len({x["occupancy_sha256"] for x in cases}) != N_REPS:
        raise RuntimeError("M5 generated duplicate occupancy corpora")

    authority = {
        "schema": "issue75-phaseE0-m5-krs-2mix-chain-generator-authority-v1",
        "status": "M5_KRS_TWO_LATENT_CHAIN_MODES_31_CORPORA_FROZEN_TARGET_BLIND",
        "scientific_role": "PRETARGET_CROSSFITTED_TWO_LATENT_LOCAL_CHAIN_GENERATOR_AUTHORITY",
        "family": FAMILY,
        "plan_e_sha256": plan_sha,
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
            "latent_states": 2,
            "gate": "one global pi independent of K/R/S/leaf/line",
            "component_family": "position-specific unary plus nearest-neighbor interactions conditioned on K/R/S",
            "free_parameters_per_component": 21,
            "free_gate_parameters": 1,
            "free_continuous_parameters": 43,
            "explicit_nonadjacent_parameters": 0,
            "generic_distance_parameters": 0,
            "named_distant_pair_parameters": 0,
            "signature_specific_parameters": 0,
            "optimizer": "exact aggregated conditional likelihood; analytic-gradient L-BFGS-B; 9 frozen deterministic starts",
            "start_count": 9,
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
    }
    raw = canonical_json_bytes(authority) + b"\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(json.dumps({
        "status": authority["status"],
        "family": FAMILY,
        "plan_e_sha256": plan_sha,
        "cases": len(cases),
        "selected_starts": [fit_public[str(f)]["selected_start_index"] for f in range(N_FOLDS)],
        "pis": [fit_public[str(f)]["pi"] for f in range(N_FOLDS)],
        "ll_gain_over_m3": [fit_public[str(f)]["selected_log_likelihood_gain_over_m3"] for f in range(N_FOLDS)],
        "generated_distinct_signature_range": [min(x["distinct_signatures"] for x in cases), max(x["distinct_signatures"] for x in cases)],
        "target_access": authority["target_access"],
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
