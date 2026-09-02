#!/usr/bin/env python3
"""Issue #75 Phase F0 training-only latent-frontier diagnostic.

Compares, by physical-leaf held-out conditional occupancy likelihood only:
  - M5 global two-mode local chain (43 parameters),
  - G2 K/R/S-gated two-mode local chain (46 parameters),
  - G3 global three-mode local chain (65 parameters).

No residual topology reference is loaded or scored by this executable.

Usage:
    python phase75f0_training_latent_diagnostic.py ZL3B_PATH OUTPUT_JSON
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Callable, Mapping, Sequence

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logsumexp

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75e_generator_support as egen  # noqa: E402

PLAN_PATH = HERE / "PLAN_F0_TRAINING_LATENT_DIAGNOSTIC.md"
CLARIFICATION_PATH = HERE / "IMPLEMENTATION_CLARIFICATION_F0.md"

N_FOLDS = 5
N_STARTS = 9
N_COMPONENT = 21
G2_FREE = 46
G3_FREE = 65
G2_COMPONENT_PERTURB = 0.10
G2_GATE_PERTURB = 0.05
G3_SPLIT_PERTURB = 0.08
TIE_TOL = 1e-10
NEST_TOL = 1e-7
WEIGHT_MIN = 1e-8
GRAD_VALID_TOL = 1e-6
GRAD_CHECK_TOL = 2e-5
PREDICTIVE_GAIN_MIN = 0.01

FAMILY_M5 = "M5-KRS-2MIX-CHAIN"
FAMILY_G2 = "M6-KRS-GATED-2MIX-CHAIN"
FAMILY_G3 = "M6-GLOBAL-3MIX-CHAIN"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def logit(p: float) -> float:
    p = float(p)
    if not (0.0 < p < 1.0):
        raise RuntimeError("invalid probability for logit")
    return float(math.log(p) - math.log1p(-p))


def sha_direction(namespace: str, n: int) -> np.ndarray:
    vals = []
    for j in range(n):
        text = f"{namespace}:coord{j}".encode("utf-8")
        x = int.from_bytes(hashlib.sha256(text).digest()[:8], "big", signed=False)
        vals.append(((x + 0.5) / float(2**64)) - 0.5)
    v = np.asarray(vals, dtype=np.float64)
    norm = float(np.linalg.norm(v))
    if not math.isfinite(norm) or norm <= 0.0:
        raise RuntimeError("invalid deterministic SHA direction")
    return v / norm


def counts_for(X: np.ndarray) -> np.ndarray:
    _idx, counts = egen.state_counts(np.asarray(X, dtype=np.uint8))
    return counts


def descriptor_standardization(X: np.ndarray) -> dict:
    idx = egen.state_indices(np.asarray(X, dtype=np.uint8))
    did = egen.STATE_DESC_ID[idx]
    desc = np.asarray(egen.DESCRIPTORS, dtype=np.float64)[did]
    mean = np.mean(desc, axis=0)
    sd = np.std(desc, axis=0, ddof=0)
    active = sd > 0.0
    safe_sd = np.where(active, sd, 1.0)

    all_desc = np.asarray(egen.DESCRIPTORS, dtype=np.float64)
    zdesc = (all_desc - mean[None, :]) / safe_sd[None, :]
    zdesc[:, ~active] = 0.0
    design_desc = np.column_stack([np.ones(len(all_desc), dtype=np.float64), zdesc])
    design_state = design_desc[egen.STATE_DESC_ID]
    return {
        "mean": mean,
        "sd": sd,
        "active": active,
        "design_desc": design_desc,
        "design_state": design_state,
    }


def m5_loglik(fit: Mapping, counts: np.ndarray) -> float:
    lp0, _ = egen.component_logprob_and_mu(np.asarray(fit["theta0"], dtype=np.float64))
    lp1, _ = egen.component_logprob_and_mu(np.asarray(fit["theta1"], dtype=np.float64))
    pi = float(fit["pi"])
    obs = np.flatnonzero(counts > 0)
    log0 = math.log1p(-pi) + lp0[obs]
    log1 = math.log(pi) + lp1[obs]
    return float(counts[obs] @ np.logaddexp(log0, log1))


def g2_objective_gradient(v: np.ndarray, counts: np.ndarray, design_state: np.ndarray) -> tuple[float, np.ndarray]:
    v = np.asarray(v, dtype=np.float64)
    if v.shape != (G2_FREE,) or np.any(~np.isfinite(v)):
        return math.inf, np.full(G2_FREE, np.nan)
    t0 = v[:21]
    t1 = v[21:42]
    gate = v[42:46]
    lp0, mu0 = egen.component_logprob_and_mu(t0)
    lp1, mu1 = egen.component_logprob_and_mu(t1)

    eta = design_state @ gate
    pi = expit(eta)
    obs = np.flatnonzero(counts > 0)
    c = counts[obs]
    eta_obs = eta[obs]
    pi_obs = pi[obs]
    la = -np.logaddexp(0.0, eta_obs) + lp0[obs]
    lb = -np.logaddexp(0.0, -eta_obs) + lp1[obs]
    lm = np.logaddexp(la, lb)
    ll = float(c @ lm)
    r1 = np.exp(lb - lm)
    r0 = 1.0 - r1

    Fobs = egen.FREE_FEATURES[obs]
    did = egen.STATE_DESC_ID[obs]
    emp0 = (c * r0) @ Fobs
    emp1 = (c * r1) @ Fobs
    mass0 = np.bincount(did, weights=c * r0, minlength=len(egen.DESCRIPTORS))
    mass1 = np.bincount(did, weights=c * r1, minlength=len(egen.DESCRIPTORS))
    g0 = emp0 - mass0 @ mu0
    g1 = emp1 - mass1 @ mu1
    gg = (c * (r1 - pi_obs)) @ design_state[obs]
    grad = np.concatenate([g0, g1, np.asarray(gg, dtype=np.float64)])
    if not math.isfinite(ll) or np.any(~np.isfinite(grad)):
        return math.inf, np.full(G2_FREE, np.nan)
    return -ll, -grad


def g2_loglik(v: np.ndarray, counts: np.ndarray, design_state: np.ndarray) -> float:
    v = np.asarray(v, dtype=np.float64)
    t0, t1, gate = v[:21], v[21:42], v[42:46]
    lp0, _ = egen.component_logprob_and_mu(t0)
    lp1, _ = egen.component_logprob_and_mu(t1)
    obs = np.flatnonzero(counts > 0)
    eta = design_state[obs] @ gate
    lm = np.logaddexp(-np.logaddexp(0.0, eta) + lp0[obs], -np.logaddexp(0.0, -eta) + lp1[obs])
    return float(counts[obs] @ lm)


def g3_logweights(v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    logits = np.asarray([0.0, float(v[63]), float(v[64])], dtype=np.float64)
    lw = logits - logsumexp(logits)
    return lw, np.exp(lw)


def g3_objective_gradient(v: np.ndarray, counts: np.ndarray) -> tuple[float, np.ndarray]:
    v = np.asarray(v, dtype=np.float64)
    if v.shape != (G3_FREE,) or np.any(~np.isfinite(v)):
        return math.inf, np.full(G3_FREE, np.nan)
    theta = [v[0:21], v[21:42], v[42:63]]
    lps = []
    mus = []
    for t in theta:
        lp, mu = egen.component_logprob_and_mu(t)
        lps.append(lp)
        mus.append(mu)
    lw, w = g3_logweights(v)
    obs = np.flatnonzero(counts > 0)
    c = counts[obs]
    terms = np.vstack([lw[k] + lps[k][obs] for k in range(3)])
    lm = logsumexp(terms, axis=0)
    resp = np.exp(terms - lm[None, :])
    ll = float(c @ lm)

    Fobs = egen.FREE_FEATURES[obs]
    did = egen.STATE_DESC_ID[obs]
    grads = []
    for k in range(3):
        wk = c * resp[k]
        emp = wk @ Fobs
        mass = np.bincount(did, weights=wk, minlength=len(egen.DESCRIPTORS))
        grads.append(emp - mass @ mus[k])
    geta1 = float(np.sum(c * (resp[1] - w[1])))
    geta2 = float(np.sum(c * (resp[2] - w[2])))
    grad = np.concatenate([grads[0], grads[1], grads[2], np.asarray([geta1, geta2])])
    if not math.isfinite(ll) or np.any(~np.isfinite(grad)):
        return math.inf, np.full(G3_FREE, np.nan)
    return -ll, -grad


def g3_loglik(v: np.ndarray, counts: np.ndarray) -> float:
    v = np.asarray(v, dtype=np.float64)
    lps = [egen.component_logprob_and_mu(v[k * 21:(k + 1) * 21])[0] for k in range(3)]
    lw, _w = g3_logweights(v)
    obs = np.flatnonzero(counts > 0)
    terms = np.vstack([lw[k] + lps[k][obs] for k in range(3)])
    return float(counts[obs] @ logsumexp(terms, axis=0))


def gradient_check(fun: Callable[[np.ndarray], tuple[float, np.ndarray]], v: np.ndarray) -> dict:
    f, g = fun(np.asarray(v, dtype=np.float64))
    if not math.isfinite(f) or np.any(~np.isfinite(g)):
        raise RuntimeError("gradient audit point is non-finite")
    eps = 1e-6
    numeric = np.empty_like(g)
    for j in range(len(g)):
        vp = np.asarray(v, dtype=np.float64).copy()
        vm = np.asarray(v, dtype=np.float64).copy()
        vp[j] += eps
        vm[j] -= eps
        fp, _ = fun(vp)
        fm, _ = fun(vm)
        numeric[j] = (fp - fm) / (2.0 * eps)
    err = np.abs(g - numeric)
    scale = np.maximum(1.0, np.maximum(np.abs(g), np.abs(numeric)))
    max_abs = float(np.max(err))
    max_scaled = float(np.max(err / scale))
    if max(max_abs, max_scaled) > GRAD_CHECK_TOL:
        raise RuntimeError(f"analytic gradient audit failed abs={max_abs} scaled={max_scaled}")
    return {
        "epsilon": eps,
        "max_absolute_error": max_abs,
        "max_scaled_error": max_scaled,
        "tolerance": GRAD_CHECK_TOL,
        "passed": True,
    }


def public_start(s: Mapping) -> dict:
    return {k: v for k, v in s.items() if k != "x"}


def choose_best(starts: list[dict]) -> dict:
    valid = [s for s in starts if s["valid"]]
    if not valid:
        raise RuntimeError("no valid deterministic optimization start")
    best = valid[0]
    for s in valid[1:]:
        if s["final_log_likelihood"] > best["final_log_likelihood"] + TIE_TOL:
            best = s
        elif abs(s["final_log_likelihood"] - best["final_log_likelihood"]) <= TIE_TOL and s["start_index"] < best["start_index"]:
            best = s
    return best


def optimize_g2(start_index: int, v0: np.ndarray, counts: np.ndarray, design_state: np.ndarray, active: np.ndarray) -> dict:
    result = minimize(
        fun=lambda v: g2_objective_gradient(v, counts, design_state),
        x0=np.asarray(v0, dtype=np.float64),
        method="L-BFGS-B",
        jac=True,
        options={"maxiter": 2000, "ftol": 1e-12, "gtol": 1e-8, "maxls": 50},
    )
    x = np.asarray(result.x, dtype=np.float64)
    f, g = g2_objective_gradient(x, counts, design_state)
    pi_all = expit(design_state @ x[42:46])
    finite = bool(math.isfinite(f) and np.all(np.isfinite(x)) and np.all(np.isfinite(g)) and np.all(np.isfinite(pi_all)))
    weights_valid = bool(float(np.min(pi_all)) > WEIGHT_MIN and float(np.max(pi_all)) < 1.0 - WEIGHT_MIN)
    inactive_zero = bool(np.all(np.abs(x[43:46][~active]) <= 1e-14))
    grad_inf = float(np.max(np.abs(g))) if np.all(np.isfinite(g)) else math.inf
    converged = bool(result.success or grad_inf <= GRAD_VALID_TOL)
    return {
        "start_index": int(start_index),
        "initial_log_likelihood": float(-g2_objective_gradient(v0, counts, design_state)[0]),
        "final_log_likelihood": float(-f),
        "optimizer_success": bool(result.success),
        "optimizer_status": int(result.status),
        "optimizer_message": str(result.message),
        "iterations": int(result.nit),
        "function_evaluations": int(result.nfev),
        "gradient_inf_norm": grad_inf,
        "minimum_gate_probability": float(np.min(pi_all)),
        "maximum_gate_probability": float(np.max(pi_all)),
        "finite": finite,
        "weights_valid": weights_valid,
        "inactive_slopes_zero": inactive_zero,
        "valid": bool(finite and weights_valid and inactive_zero and converged),
        "x": x,
    }


def fit_g2(train: np.ndarray, m5: Mapping, do_gradient_audit: bool) -> dict:
    counts = counts_for(train)
    standard = descriptor_standardization(train)
    active = np.asarray(standard["active"], dtype=bool)
    design = np.asarray(standard["design_state"], dtype=np.float64)
    t0 = np.asarray(m5["theta0"], dtype=np.float64)
    t1 = np.asarray(m5["theta1"], dtype=np.float64)
    eta0 = logit(float(m5["pi"]))

    initial_vectors = []
    base = np.concatenate([t0, t1, np.asarray([eta0, 0.0, 0.0, 0.0])])
    initial_vectors.append(base)
    for k in range(1, 9):
        u = sha_direction(f"issue75:phaseF0:G2:component:init{k}", 21)
        q = sha_direction(f"issue75:phaseF0:G2:gate:init{k}", 3)
        slopes = G2_GATE_PERTURB * q
        slopes[~active] = 0.0
        initial_vectors.append(np.concatenate([t0 + G2_COMPONENT_PERTURB * u, t1 - G2_COMPONENT_PERTURB * u, np.asarray([eta0]), slopes]))

    m5_ll = float(m5["selected_log_likelihood"])
    nested_ll = float(-g2_objective_gradient(initial_vectors[0], counts, design)[0])
    if abs(nested_ll - m5_ll) > NEST_TOL:
        raise RuntimeError(f"G2 nested M5 start mismatch {nested_ll} vs {m5_ll}")
    audit = gradient_check(lambda v: g2_objective_gradient(v, counts, design), initial_vectors[1]) if do_gradient_audit else {"performed": False, "passed": True}
    starts = [optimize_g2(k, v, counts, design, active) for k, v in enumerate(initial_vectors)]
    if len(starts) != N_STARTS:
        raise RuntimeError("G2 start population incomplete")
    best = choose_best(starts)
    if best["final_log_likelihood"] < m5_ll - NEST_TOL:
        raise RuntimeError("G2 selected likelihood below nested M5 baseline")
    x = np.asarray(best["x"], dtype=np.float64)
    return {
        "x": x,
        "standardization": standard,
        "selected_start_index": int(best["start_index"]),
        "selected_log_likelihood": float(best["final_log_likelihood"]),
        "training_gain_over_m5": float(best["final_log_likelihood"] - m5_ll),
        "all_starts": [public_start(s) for s in starts],
        "gradient_audit": audit,
    }


def weights_to_relative_logits(weights: Sequence[float]) -> np.ndarray:
    w = np.asarray(weights, dtype=np.float64)
    if w.shape != (3,) or np.any(w <= 0.0) or not np.isclose(float(w.sum()), 1.0, atol=1e-12):
        raise RuntimeError("invalid G3 initial weights")
    return np.asarray([math.log(float(w[1] / w[0])), math.log(float(w[2] / w[0]))], dtype=np.float64)


def optimize_g3(start_index: int, v0: np.ndarray, counts: np.ndarray) -> dict:
    result = minimize(
        fun=lambda v: g3_objective_gradient(v, counts),
        x0=np.asarray(v0, dtype=np.float64),
        method="L-BFGS-B",
        jac=True,
        options={"maxiter": 2000, "ftol": 1e-12, "gtol": 1e-8, "maxls": 50},
    )
    x = np.asarray(result.x, dtype=np.float64)
    f, g = g3_objective_gradient(x, counts)
    _lw, weights = g3_logweights(x)
    finite = bool(math.isfinite(f) and np.all(np.isfinite(x)) and np.all(np.isfinite(g)) and np.all(np.isfinite(weights)))
    weights_valid = bool(float(np.min(weights)) > WEIGHT_MIN)
    grad_inf = float(np.max(np.abs(g))) if np.all(np.isfinite(g)) else math.inf
    converged = bool(result.success or grad_inf <= GRAD_VALID_TOL)
    return {
        "start_index": int(start_index),
        "initial_log_likelihood": float(-g3_objective_gradient(v0, counts)[0]),
        "final_log_likelihood": float(-f),
        "optimizer_success": bool(result.success),
        "optimizer_status": int(result.status),
        "optimizer_message": str(result.message),
        "iterations": int(result.nit),
        "function_evaluations": int(result.nfev),
        "gradient_inf_norm": grad_inf,
        "weights": [float(z) for z in weights],
        "finite": finite,
        "weights_valid": weights_valid,
        "valid": bool(finite and weights_valid and converged),
        "x": x,
    }


def fit_g3(train: np.ndarray, m5: Mapping, do_gradient_audit: bool) -> dict:
    counts = counts_for(train)
    t0 = np.asarray(m5["theta0"], dtype=np.float64)
    t1 = np.asarray(m5["theta1"], dtype=np.float64)
    pi = float(m5["pi"])
    w0, w1 = 1.0 - pi, pi

    initial_vectors = []
    weights_split0 = np.asarray([w0 / 2.0, w1, w0 / 2.0], dtype=np.float64)
    initial_vectors.append(np.concatenate([t0, t1, t0, weights_to_relative_logits(weights_split0)]))
    for k in range(1, 5):
        u = sha_direction(f"issue75:phaseF0:G3:split:init{k}", 21)
        initial_vectors.append(np.concatenate([t0 + G3_SPLIT_PERTURB * u, t1, t0 - G3_SPLIT_PERTURB * u, weights_to_relative_logits(weights_split0)]))
    weights_split1 = np.asarray([w0, w1 / 2.0, w1 / 2.0], dtype=np.float64)
    for k in range(5, 9):
        u = sha_direction(f"issue75:phaseF0:G3:split:init{k}", 21)
        initial_vectors.append(np.concatenate([t0, t1 + G3_SPLIT_PERTURB * u, t1 - G3_SPLIT_PERTURB * u, weights_to_relative_logits(weights_split1)]))

    m5_ll = float(m5["selected_log_likelihood"])
    nested_ll = float(-g3_objective_gradient(initial_vectors[0], counts)[0])
    if abs(nested_ll - m5_ll) > NEST_TOL:
        raise RuntimeError(f"G3 nested M5 start mismatch {nested_ll} vs {m5_ll}")
    audit = gradient_check(lambda v: g3_objective_gradient(v, counts), initial_vectors[1]) if do_gradient_audit else {"performed": False, "passed": True}
    starts = [optimize_g3(k, v, counts) for k, v in enumerate(initial_vectors)]
    if len(starts) != N_STARTS:
        raise RuntimeError("G3 start population incomplete")
    best = choose_best(starts)
    if best["final_log_likelihood"] < m5_ll - NEST_TOL:
        raise RuntimeError("G3 selected likelihood below nested M5 baseline")
    x = np.asarray(best["x"], dtype=np.float64)
    _lw, weights = g3_logweights(x)
    return {
        "x": x,
        "weights": weights,
        "selected_start_index": int(best["start_index"]),
        "selected_log_likelihood": float(best["final_log_likelihood"]),
        "training_gain_over_m5": float(best["final_log_likelihood"] - m5_ll),
        "all_starts": [public_start(s) for s in starts],
        "gradient_audit": audit,
    }


def serialize_vector(v: np.ndarray) -> list[float]:
    return [float(x) for x in np.asarray(v, dtype=np.float64)]


def predictive_support(delta: Sequence[float]) -> dict:
    d = np.asarray(delta, dtype=np.float64)
    all_positive = bool(np.all(d > 0.0))
    median = float(np.median(d))
    supported = bool(all_positive and median >= PREDICTIVE_GAIN_MIN)
    return {
        "all_five_folds_positive": all_positive,
        "median_gain_nats_per_token": median,
        "minimum_required_median_gain_nats_per_token": PREDICTIVE_GAIN_MIN,
        "supported": supported,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} ZL3B_PATH OUTPUT_JSON")
    src = Path(argv[1]).resolve()
    out_path = Path(argv[2]).resolve()
    if not PLAN_PATH.exists() or not CLARIFICATION_PATH.exists():
        raise RuntimeError("Phase F0 preregistration and implementation clarification are required")

    cgen = egen.cgen
    if cgen.a0.e.git_blob_sha1(src.read_bytes()) != cgen.a0.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = cgen.a0.e.SlotParser()
    cgen.a0.e.validate_parser(parser)
    d = cgen.a0.b58.build_dataset(src, parser, "min")
    if d["source_blob"] != cgen.a0.EXPECTED_SOURCE_BLOB or d["visible"] != cgen.a0.EXPECTED_VISIBLE or d["parsed"] != cgen.a0.EXPECTED_PARSED:
        raise RuntimeError("frozen source population mismatch")
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    X = np.asarray(d["X"], dtype=np.uint8)
    fold_counts = [int(np.sum(folds == f)) for f in range(N_FOLDS)]
    if fold_counts != cgen.a0.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen physical fold mismatch: {fold_counts}")

    results = []
    for f in range(N_FOLDS):
        train = X[folds != f]
        hold = X[folds == f]
        expected_train = cgen.a0.EXPECTED_PARSED - cgen.a0.EXPECTED_FOLD_PARSED[f]
        if len(train) != expected_train or len(hold) != cgen.a0.EXPECTED_FOLD_PARSED[f]:
            raise RuntimeError(f"outer fold population mismatch {f}")
        train_counts = counts_for(train)
        hold_counts = counts_for(hold)

        m5 = egen.fit_m5(train, do_gradient_audit=(f == 0))
        m5_train_ll = m5_loglik(m5, train_counts)
        if abs(m5_train_ll - float(m5["selected_log_likelihood"])) > NEST_TOL:
            raise RuntimeError(f"refitted M5 likelihood mismatch fold {f}")
        m5_hold_ll = m5_loglik(m5, hold_counts)

        g2 = fit_g2(train, m5, do_gradient_audit=(f == 0))
        g2_design = np.asarray(g2["standardization"]["design_state"], dtype=np.float64)
        g2_hold_ll = g2_loglik(np.asarray(g2["x"]), hold_counts, g2_design)

        g3 = fit_g3(train, m5, do_gradient_audit=(f == 0))
        g3_hold_ll = g3_loglik(np.asarray(g3["x"]), hold_counts)

        n_hold = float(len(hold))
        hm5 = float(m5_hold_ll / n_hold)
        hg2 = float(g2_hold_ll / n_hold)
        hg3 = float(g3_hold_ll / n_hold)
        standard = g2["standardization"]
        gate = np.asarray(g2["x"])[42:46]
        gate_desc_prob = expit(np.asarray(standard["design_desc"]) @ gate)

        results.append({
            "fold": f,
            "training_tokens": int(len(train)),
            "heldout_tokens": int(len(hold)),
            "descriptor_standardization": {
                "mean_K_R_S": serialize_vector(standard["mean"]),
                "population_sd_K_R_S": serialize_vector(standard["sd"]),
                "active_K_R_S": [bool(x) for x in np.asarray(standard["active"])],
            },
            "m5": {
                "family": FAMILY_M5,
                "free_continuous_parameters": 43,
                "selected_start_index": int(m5["selected_start_index"]),
                "training_conditional_log_likelihood": float(m5_train_ll),
                "heldout_conditional_log_likelihood": float(m5_hold_ll),
                "heldout_nats_per_token": hm5,
                "pi": float(m5["pi"]),
            },
            "g2": {
                "family": FAMILY_G2,
                "free_continuous_parameters": G2_FREE,
                "selected_start_index": int(g2["selected_start_index"]),
                "training_conditional_log_likelihood": float(g2["selected_log_likelihood"]),
                "training_gain_over_m5": float(g2["training_gain_over_m5"]),
                "heldout_conditional_log_likelihood": float(g2_hold_ll),
                "heldout_nats_per_token": hg2,
                "heldout_gain_over_m5_nats_per_token": float(hg2 - hm5),
                "gate_intercept_and_K_R_S_slopes": serialize_vector(gate),
                "minimum_descriptor_gate_probability": float(np.min(gate_desc_prob)),
                "maximum_descriptor_gate_probability": float(np.max(gate_desc_prob)),
                "selected_theta0": serialize_vector(np.asarray(g2["x"])[0:21]),
                "selected_theta1": serialize_vector(np.asarray(g2["x"])[21:42]),
                "all_starts": g2["all_starts"],
                "gradient_audit": g2["gradient_audit"],
            },
            "g3": {
                "family": FAMILY_G3,
                "free_continuous_parameters": G3_FREE,
                "selected_start_index": int(g3["selected_start_index"]),
                "training_conditional_log_likelihood": float(g3["selected_log_likelihood"]),
                "training_gain_over_m5": float(g3["training_gain_over_m5"]),
                "heldout_conditional_log_likelihood": float(g3_hold_ll),
                "heldout_nats_per_token": hg3,
                "heldout_gain_over_m5_nats_per_token": float(hg3 - hm5),
                "global_weights": serialize_vector(g3["weights"]),
                "selected_theta0": serialize_vector(np.asarray(g3["x"])[0:21]),
                "selected_theta1": serialize_vector(np.asarray(g3["x"])[21:42]),
                "selected_theta2": serialize_vector(np.asarray(g3["x"])[42:63]),
                "all_starts": g3["all_starts"],
                "gradient_audit": g3["gradient_audit"],
            },
            "direct_g3_minus_g2_nats_per_token": float(hg3 - hg2),
        })

    d2 = [float(r["g2"]["heldout_gain_over_m5_nats_per_token"]) for r in results]
    d3 = [float(r["g3"]["heldout_gain_over_m5_nats_per_token"]) for r in results]
    d32 = [float(r["direct_g3_minus_g2_nats_per_token"]) for r in results]
    s2 = predictive_support(d2)
    s3 = predictive_support(d3)
    g3_over_g2_folds = int(np.sum(np.asarray(d32) > 0.0))
    g3_over_g2_median = float(np.median(np.asarray(d32)))

    if s2["supported"] and not s3["supported"]:
        classification = "F0_SELECT_KRS_GATED_TWO_MODE_CHAIN"
    elif s3["supported"] and not s2["supported"]:
        classification = "F0_SELECT_GLOBAL_THREE_MODE_CHAIN"
    elif s2["supported"] and s3["supported"]:
        if g3_over_g2_folds >= 4 and g3_over_g2_median >= PREDICTIVE_GAIN_MIN:
            classification = "F0_SELECT_GLOBAL_THREE_MODE_CHAIN"
        else:
            classification = "F0_SELECT_KRS_GATED_TWO_MODE_CHAIN"
    else:
        classification = "F0_GLOBAL_MIXTURE_EXTENSIONS_NOT_PREDICTIVELY_SUPPORTED_WITHIN_TOKEN_STATE_FRONTIER_REQUIRED"

    output = {
        "schema": "issue75-phaseF0-training-latent-diagnostic-v1",
        "status": "PHASE_F0_TRAINING_ONLY_LATENT_FRONTIER_DIAGNOSTIC_COMPLETE",
        "scientific_role": "PRETARGET_ARCHITECTURE_DISCRIMINATION_BY_PHYSICAL_LEAF_PREDICTIVE_OCCUPANCY_LIKELIHOOD",
        "plan_f0_sha256": sha256_file(PLAN_PATH),
        "implementation_clarification_sha256": sha256_file(CLARIFICATION_PATH),
        "source": {
            "ZL3b_blob": str(d["source_blob"]),
            "visible_tokens": int(d["visible"]),
            "parsed_tokens": int(d["parsed"]),
            "fold_parsed_tokens": fold_counts,
            "parser_policy": "SlotParser(min)",
        },
        "families": {
            "baseline": {"name": FAMILY_M5, "free_continuous_parameters": 43},
            "g2": {"name": FAMILY_G2, "free_continuous_parameters": G2_FREE, "explicit_nonadjacent_parameters": 0, "generic_distance_parameters": 0, "signature_specific_parameters": 0},
            "g3": {"name": FAMILY_G3, "free_continuous_parameters": G3_FREE, "explicit_nonadjacent_parameters": 0, "generic_distance_parameters": 0, "signature_specific_parameters": 0},
        },
        "outer_folds": results,
        "support": {
            "g2_over_m5": s2,
            "g3_over_m5": s3,
            "g3_over_g2": {
                "positive_fold_count": g3_over_g2_folds,
                "median_gain_nats_per_token": g3_over_g2_median,
                "displacement_requires_positive_folds": 4,
                "displacement_requires_median_gain_nats_per_token": PREDICTIVE_GAIN_MIN,
            },
        },
        "selection": {
            "classification": classification,
            "rule_frozen_before_executable": True,
        },
        "guardrails": {
            "reference_residual_vector_loaded": False,
            "reference_correlation_computed": False,
            "reference_sign_agreement_computed": False,
            "candidate_pair_terms_selected": False,
            "random_restarts": False,
            "rerolls": False,
        },
    }
    raw = canonical_json_bytes(output) + b"\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(json.dumps({
        "status": output["status"],
        "classification": classification,
        "g2_fold_gains": d2,
        "g2_median_gain": s2["median_gain_nats_per_token"],
        "g2_supported": s2["supported"],
        "g3_fold_gains": d3,
        "g3_median_gain": s3["median_gain_nats_per_token"],
        "g3_supported": s3["supported"],
        "g3_minus_g2_fold_gains": d32,
        "g3_minus_g2_median_gain": g3_over_g2_median,
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
