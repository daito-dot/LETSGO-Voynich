#!/usr/bin/env python3
"""OGH-A — minimal occupancy-generation rule for the replicated R1 topology.

Scientific authority: experiments/occupancy-generation-hierarchy/PLAN_A.md
(committed before this executable).

Modes
  --self-test
  --admissible OUT.json                 enumerate SlotParser(min)-admissible signatures
  --preflight SOURCE ZL3b [IT2a] OUT    fit every model per fold, no R1 metric
  --score SOURCE MODEL REP ZL3b [IT2a] OUT   generate rep corpus and run frozen R1 scoring
  --aggregate DIR OUT                   apply the frozen hierarchy classification

SOURCE is ZL3b (primary skeleton) or IT2a (replication skeleton). IT2a scoring
needs both transcription paths because the frozen physical-leaf folds are
defined from ZL3b.

The R1 scorer is the Issue #68 scorer (target68.py) re-hosted for a five-fold
skeleton. Gates, statistics, null operation and residual transform are
unchanged. Frozen ZL3b/IT2a null distributions are never reused: every
candidate corpus owns its reference and test nulls.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import logsumexp

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in (
    "issue26-music",
    "occupancy-graph-stability",
    "occupancy-graph-residual",
    "occupancy-graph-independent-transcription",
    "phase63",
):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import issue26e_core as e  # noqa: E402
import phase58b_graph_stability as b58  # noqa: E402
import phase58c_residual_graph as c58  # noqa: E402
import phase58d_independent_residual as d58  # noqa: E402

PHASE = "OGH-A"
N_SLOTS = 12
N_SIG = 2 ** N_SLOTS - 1  # non-empty signatures, mask 1..4095
N_REF = 1000
N_TEST = 1000
N_FOLDS = 5
N_EDGES = 66
PAIRS = b58.PAIRS
MODELS = ("G0", "G1", "G2", "G3", "G4", "G5", "G6")
NON_PROMOTING = ("G5", "G6")
SOURCES = ("ZL3b", "IT2a")
REPS = (0, 1, 2)
MOMENT_TOL = 1e-6
ISSUE58C_SHA256 = "fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d"
ISSUE58D_SHA256 = "f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6"
ZL_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
ADMISSIBLE_SCHEMA = "ogh-a-admissible-signatures-v1"

MASKS = np.arange(1, N_SIG + 1, dtype=np.int64)
BITS = ((MASKS[:, None] >> np.arange(N_SLOTS)[None, :]) & 1).astype(np.float64)  # (4095, 12)
COUNTS = BITS.sum(axis=1).astype(np.int64)


# ----------------------------------------------------------------------------
# utilities

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def environment():
    return {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
    }


def rows_to_masks(X) -> np.ndarray:
    X = np.asarray(X, dtype=np.int64)
    return (X * (1 << np.arange(N_SLOTS, dtype=np.int64))[None, :]).sum(axis=1)


def masks_to_rows(masks) -> np.ndarray:
    masks = np.asarray(masks, dtype=np.int64)
    return ((masks[:, None] >> np.arange(N_SLOTS)[None, :]) & 1).astype(np.uint8)


# ----------------------------------------------------------------------------
# admissible signature set (representation property of SlotParser(min))

def enumerate_admissible(parser: e.SlotParser):
    """Return {mask: n_strings} for signatures SlotParser(min) can emit.

    A signature S is admissible iff some string built by concatenating one
    value per occupied slot (in slot order) has S as its minimal parse.
    """
    seen_strings = {}
    admissible = {}
    for mask in range(1, N_SIG + 1):
        slots = [s for s in range(N_SLOTS) if (mask >> s) & 1]
        n = 0
        for vals in itertools.product(*[e.SLOTS[s] for s in slots]):
            tok = "".join(vals)
            if tok in seen_strings:
                sig_mask = seen_strings[tok]
            else:
                picked = parser.pick(tok, "min")
                sig_mask = 0
                if picked is not None:
                    for s in picked[0]:
                        sig_mask |= 1 << s
                seen_strings[tok] = sig_mask
            if sig_mask == mask:
                n += 1
        if n:
            admissible[mask] = n
    return admissible, len(seen_strings)


def admissible_payload(parser: e.SlotParser) -> dict:
    t0 = time.time()
    adm, n_strings = enumerate_admissible(parser)
    masks = sorted(adm)
    by_count = {}
    for m in masks:
        by_count[int(bin(m).count("1"))] = by_count.get(int(bin(m).count("1")), 0) + 1
    return {
        "schema": ADMISSIBLE_SCHEMA,
        "parser_policy": "min",
        "parser_validation": e.validate_parser(parser),
        "n_admissible": len(masks),
        "n_total_nonempty": N_SIG,
        "n_distinct_candidate_strings": int(n_strings),
        "by_occupancy_count": {str(k): v for k, v in sorted(by_count.items())},
        "single_slot_admissible": [s for s in range(N_SLOTS) if (1 << s) in adm],
        "masks": masks,
        "realizing_strings_per_mask": [adm[m] for m in masks],
        "seconds": time.time() - t0,
    }


def load_admissible() -> tuple[np.ndarray, dict]:
    path = HERE.parent / "preflight" / "admissible_signatures.json"
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj["schema"] != ADMISSIBLE_SCHEMA or obj["n_total_nonempty"] != N_SIG:
        raise RuntimeError("unexpected admissible-signature file")
    masks = np.asarray(obj["masks"], dtype=np.int64)
    if len(masks) != obj["n_admissible"] or not np.all(np.diff(masks) > 0) or masks.min() < 1 or masks.max() > N_SIG:
        raise RuntimeError("corrupt admissible-signature list")
    in_a = np.zeros(N_SIG, dtype=bool)
    in_a[masks - 1] = True
    return in_a, {"sha256": sha256_file(path), "n_admissible": int(len(masks))}


# ----------------------------------------------------------------------------
# skeletons

def build_skeleton(source: str, zl_path: Path, it_path: Path | None):
    parser = e.SlotParser()
    e.validate_parser(parser)
    if source == "ZL3b":
        d = b58.build_dataset(zl_path, parser, "min")
        b58.validate_support(d)
        ident = {"git_blob_sha1": d["source_blob"], "sha256": sha256_file(zl_path)}
    elif source == "IT2a":
        if it_path is None:
            raise RuntimeError("IT2a skeleton requires the IT2a path")
        d = d58.build_it_dataset(it_path, zl_path, "min")
        support = d58.load_support_audit()
        d58.validate_population(d, support)
        ident = dict(d["source_identity"])
    else:
        raise RuntimeError(f"unknown source {source}")
    masks = rows_to_masks(d["X"])
    return {
        "source": source,
        "identity": ident,
        "visible": int(d["visible"]),
        "parsed": int(d["parsed"]),
        "n_lines": int(d["padded"].shape[0]),
        "fold_counts": [int(np.sum(d["token_folds"] == f)) for f in range(N_FOLDS)],
        "token_folds": d["token_folds"].astype(np.int8),
        "line_mask": d["line_mask"],
        "maxlen": int(d["padded"].shape[1]),
        "observed_masks": masks,
    }


def dataset_from_rows(sk, X: np.ndarray) -> dict:
    X = np.asarray(X, dtype=np.uint8)
    if X.shape != (sk["parsed"], N_SLOTS):
        raise RuntimeError(f"corpus shape {X.shape} != {(sk['parsed'], N_SLOTS)}")
    padded = np.zeros((sk["n_lines"], sk["maxlen"], N_SLOTS), dtype=np.uint8)
    padded[sk["line_mask"]] = X
    if not np.array_equal(padded[sk["line_mask"]], X):
        raise RuntimeError("padded/flat ordering mismatch")
    return {"X": X, "token_folds": sk["token_folds"], "padded": padded, "line_mask": sk["line_mask"]}


# ----------------------------------------------------------------------------
# model fitting: every model is a probability vector over the 4095 non-empty signatures

def sig_counts(masks: np.ndarray) -> np.ndarray:
    return np.bincount(np.asarray(masks, dtype=np.int64) - 1, minlength=N_SIG).astype(np.float64)


def fit_maxent(features: np.ndarray, support: np.ndarray, counts: np.ndarray, label: str) -> dict:
    """Exact maximum-entropy / maximum-likelihood fit by enumeration.

    features: (N_SIG, K); support: bool (N_SIG,); counts: training counts (N_SIG,).
    Features whose empirical moment is exactly 0 or exactly 1 on the support are
    handled as the ML boundary solution: states violating them are removed from
    the support and the feature is dropped.
    """
    n = counts.sum()
    emp = counts / n
    F = features.copy()
    sup = support.copy()
    dropped = []
    while True:
        m = emp @ F
        changed = False
        for k in range(F.shape[1]):
            if k in [x[0] for x in dropped]:
                continue
            if m[k] <= 0.0:
                sup &= F[:, k] == 0
                dropped.append((k, "zero"))
                changed = True
            elif m[k] >= 1.0:
                sup &= F[:, k] == 1
                dropped.append((k, "one"))
                changed = True
        if not changed:
            break
    keep = [k for k in range(F.shape[1]) if k not in [x[0] for x in dropped]]
    Fs = F[sup][:, keep]
    m = emp[sup] @ Fs
    if abs(emp[sup].sum() - 1.0) > 1e-12:
        raise RuntimeError(f"{label}: training mass outside support")
    rank = int(np.linalg.matrix_rank(np.column_stack([np.ones(len(Fs)), Fs]))) - 1

    def nll(theta):
        s = Fs @ theta
        lz = logsumexp(s)
        p = np.exp(s - lz)
        return lz - m @ theta, p @ Fs - m

    theta0 = np.zeros(Fs.shape[1])
    res = minimize(nll, theta0, jac=True, method="L-BFGS-B", options={"maxiter": 20000, "gtol": 1e-12, "ftol": 1e-15, "maxfun": 200000})
    theta = res.x
    for _ in range(3):  # polish
        res2 = minimize(nll, theta, jac=True, method="L-BFGS-B", options={"maxiter": 20000, "gtol": 1e-13, "ftol": 1e-16, "maxfun": 200000})
        theta = res2.x
    s = Fs @ theta
    p_sup = np.exp(s - logsumexp(s))
    moment_err = float(np.max(np.abs(p_sup @ Fs - m))) if Fs.shape[1] else 0.0
    p = np.zeros(N_SIG)
    p[sup] = p_sup
    return {
        "p": p,
        "n_features_nominal": int(F.shape[1]),
        "n_features_dropped_boundary": len(dropped),
        "dropped": [[int(k), why] for k, why in dropped],
        "effective_rank": rank,
        "support_size": int(sup.sum()),
        "max_moment_error": moment_err,
        "fit_ok": bool(moment_err <= MOMENT_TOL),
        "optimizer_iterations": int(res.nit),
    }


def pairwise_features() -> np.ndarray:
    cols = [BITS]
    for i, j in PAIRS:
        cols.append((BITS[:, i] * BITS[:, j])[:, None])
    return np.concatenate(cols, axis=1)


def count_features() -> np.ndarray:
    return np.stack([(COUNTS == k).astype(np.float64) for k in range(1, N_SLOTS + 1)], axis=1)


def fit_model(model: str, train_masks: np.ndarray, in_a: np.ndarray) -> dict:
    counts = sig_counts(train_masks)
    n = counts.sum()
    if np.any(counts[~in_a] > 0):
        raise RuntimeError("observed signature outside admissible set; parser/admissibility inconsistency")
    info = {"model": model, "n_train_tokens": int(n)}
    if model == "G0":
        p_s = (counts @ BITS) / n
        logp = BITS @ np.log(p_s) + (1 - BITS) @ np.log1p(-p_s)
        p = np.exp(logp - logsumexp(logp))  # renormalized over non-empty signatures
        info.update({"free_parameters": 12, "slot_marginals": p_s.tolist(), "fit_ok": True})
    elif model == "G1":
        p = in_a.astype(np.float64) / in_a.sum()
        info.update({"free_parameters": 0, "fit_ok": True})
    elif model == "G2":
        fit = fit_maxent(BITS, in_a, counts, model)
        p = fit.pop("p")
        info.update(fit)
        info["free_parameters"] = 12
    elif model == "G3":
        fit = fit_maxent(np.concatenate([BITS, count_features()], axis=1), in_a, counts, model)
        p = fit.pop("p")
        info.update(fit)
        info["free_parameters"] = 23
    elif model == "G4":
        # left-to-right: P(x_s = 1 | last occupied slot before s), add-1/2 smoothing
        rows = masks_to_rows(train_masks).astype(np.int64)
        cond = []  # per slot s: array over contexts ell in {none(-1)->0, 0..s-1 -> 1..s}
        logp = np.zeros(N_SIG)
        # context for each of the 4095 states at slot s
        last = np.full(N_SIG, -1, dtype=np.int64)
        last_train = np.full(len(rows), -1, dtype=np.int64)
        n_params = 0
        for s in range(N_SLOTS):
            ctx_train = last_train + 1  # 0..s
            occ = rows[:, s]
            n1 = np.bincount(ctx_train, weights=occ, minlength=s + 1)
            n0 = np.bincount(ctx_train, weights=1 - occ, minlength=s + 1)
            q1 = (n1 + 0.5) / (n1 + n0 + 1.0)
            cond.append(q1.tolist())
            n_params += s + 1
            ctx = last + 1
            xs = BITS[:, s].astype(np.int64)
            logp += np.where(xs == 1, np.log(q1[ctx]), np.log1p(-q1[ctx]))
            last = np.where(xs == 1, s, last)
            last_train = np.where(occ == 1, s, last_train)
        logp[~in_a] = -np.inf
        p = np.exp(logp - logsumexp(logp[in_a]))
        p[~in_a] = 0.0
        info.update({"free_parameters": n_params, "conditionals_P_occupied_given_last": cond, "admissible_mass_before_renormalization": float(np.exp(logsumexp(logp[in_a]))), "fit_ok": True})
    elif model == "G5":
        fit = fit_maxent(pairwise_features(), in_a, counts, model)
        p = fit.pop("p")
        info.update(fit)
        info["free_parameters"] = 78
    elif model == "G6":
        p = counts / n
        info.update({"free_parameters": int(np.sum(counts > 0)), "n_observed_signatures": int(np.sum(counts > 0)), "fit_ok": True})
    else:
        raise RuntimeError(f"unknown model {model}")
    if not (np.all(p >= 0) and abs(p.sum() - 1.0) < 1e-9):
        raise RuntimeError(f"{model}: invalid probability vector")
    info["p"] = p
    return info


def loglik(p: np.ndarray, masks: np.ndarray) -> dict:
    idx = np.asarray(masks, dtype=np.int64) - 1
    pm = p[idx]
    covered = pm > 0
    return {
        "n_tokens": int(len(idx)),
        "zero_probability_fraction": float(1.0 - covered.mean()),
        "mean_log_likelihood_covered": float(np.mean(np.log(pm[covered]))) if covered.any() else None,
        "mean_log_likelihood": float(np.mean(np.log(pm))) if covered.all() else None,
    }


def fit_all_folds(sk, model: str, in_a: np.ndarray) -> list[dict]:
    out = []
    for f in range(N_FOLDS):
        tr = sk["observed_masks"][sk["token_folds"] != f]
        he = sk["observed_masks"][sk["token_folds"] == f]
        fit = fit_model(model, tr, in_a)
        p = fit["p"]
        out.append({
            "fold": f,
            "fit": {k: v for k, v in fit.items() if k != "p"},
            "p": p,
            "train_loglik": loglik(p, tr),
            "heldout_loglik": loglik(p, he),
            "model_slot_marginals": (p @ BITS).tolist(),
            "model_count_distribution": np.bincount(COUNTS, weights=p, minlength=N_SLOTS + 1)[1:].tolist(),
            "train_slot_marginals": (sig_counts(tr) @ BITS / len(tr)).tolist(),
            "train_count_distribution": (np.bincount(COUNTS, weights=sig_counts(tr), minlength=N_SLOTS + 1)[1:] / len(tr)).tolist(),
        })
    return out


# ----------------------------------------------------------------------------
# generation

def seed_label(source: str, model: str, fold: int, rep: int) -> str:
    return f"{PHASE}:{source}:{model}:fold{fold}:rep{rep}"


def generate_corpus(sk, model: str, rep: int, in_a: np.ndarray):
    fits = fit_all_folds(sk, model, in_a)
    X = np.zeros((sk["parsed"], N_SLOTS), dtype=np.uint8)
    gen_masks = np.zeros(sk["parsed"], dtype=np.int64)
    for f in range(N_FOLDS):
        sel = np.flatnonzero(sk["token_folds"] == f)
        p = fits[f]["p"]
        rng = np.random.default_rng(e.stable_seed(seed_label(sk["source"], model, f, rep)))
        draw = rng.choice(N_SIG, size=len(sel), replace=True, p=p) + 1
        gen_masks[sel] = draw
        X[sel] = masks_to_rows(draw)
    if not all(x["fit"]["fit_ok"] for x in fits):
        raise RuntimeError(f"{model}: FIT_FAILED in at least one fold")
    return X, gen_masks, fits


# ----------------------------------------------------------------------------
# frozen R1 scoring (Issue #68 scorer semantics, five-fold skeleton)

def load_target_references():
    _, zl_views, raw58c = d58.load_zl_first_reveal()
    if raw58c != ISSUE58C_SHA256:
        raise RuntimeError(f"#58C exact raw SHA mismatch: {raw58c}")
    zl = np.asarray(zl_views["ALL"], dtype=np.float64)
    p58d = EXPERIMENTS / "occupancy-graph-independent-transcription" / "first-reveal" / "issue66_independent_residual_results.json"
    got58d = sha256_file(p58d)
    if got58d != ISSUE58D_SHA256:
        raise RuntimeError(f"#58D exact raw SHA mismatch: {got58d}")
    r58d = json.loads(p58d.read_text(encoding="utf-8"))
    if r58d["pairs"] != [list(map(int, p)) for p in PAIRS]:
        raise RuntimeError("#58D pair order differs from scorer")
    it = np.asarray(r58d["real_IT2a"]["z_full"]["ALL"], dtype=np.float64)
    r = b58.corr(zl, it)
    a = d58.sign_agreement(zl, it)
    if r is None or abs(float(r) - 0.9884483852763541) > 1e-12 or a != 65:
        raise RuntimeError("frozen ZL3b/IT2a target-vector cross-check failed")
    return {"ZL3b": zl, "IT2a": it}, {
        "Issue58C_raw_sha256": raw58c,
        "Issue58D_raw_sha256": got58d,
        "ZL3b_IT2a_pearson": float(r),
        "ZL3b_IT2a_sign_agreement": int(a),
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


def build_reference(d, ns: str, label: str):
    ref = {
        "full": np.empty((N_REF, N_EDGES), dtype=np.float64),
        "train": np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64),
        "held": np.empty((N_REF, N_FOLDS, N_EDGES), dtype=np.float64),
    }
    for n in range(N_REF):
        Y = c58.shuffled_flat(d, ns, n)
        qv = q_views_candidate(d, Y, True)
        ref["full"][n] = qv["full"]
        ref["train"][n] = qv["train"]
        ref["held"][n] = qv["held"]
        if (n + 1) % 250 == 0:
            print(f"{label} reference null {n+1}/{N_REF}", file=sys.stderr, flush=True)
    return {k: np.sort(v, axis=0) for k, v in ref.items()}


def residualize(qv, sref):
    return {
        "full": c58.normal_score_array(qv["full"], sref["full"]),
        "train": c58.normal_score_array(qv["train"], sref["train"]),
        "held": c58.normal_score_array(qv["held"], sref["held"]),
    }


def reliability(zv):
    vals = [b58.corr(zv["train"][f], zv["held"][f]) for f in range(N_FOLDS)]
    valid = [float(x) for x in vals if x is not None and math.isfinite(float(x))]
    med = None if len(valid) < 4 else float(np.median(valid))
    return {"fold_correlations": vals, "valid_folds": len(valid), "median": med}


def test_nulls(d, sref, targets, ns: str, label: str):
    energies = np.empty(N_TEST)
    rmax = np.empty(N_TEST)
    amax = np.empty(N_TEST)
    r_by = {k: np.empty(N_TEST) for k in targets}
    a_by = {k: np.empty(N_TEST) for k in targets}
    for n in range(N_TEST):
        Y = c58.shuffled_flat(d, ns, n)
        q = q_views_candidate(d, Y, False)
        z = c58.normal_score_array(q["full"], sref["full"])
        energies[n] = c58.residual_energy(z)
        rs, aa = [], []
        for name, t in targets.items():
            rr = b58.corr(z, t)
            rv = -1.0 if rr is None else float(rr)
            av = d58.sign_agreement(z, t)
            r_by[name][n] = rv
            a_by[name][n] = av
            rs.append(rv)
            aa.append(av)
        rmax[n] = max(rs)
        amax[n] = max(aa)
        if (n + 1) % 250 == 0:
            print(f"{label} test null {n+1}/{N_TEST}", file=sys.stderr, flush=True)
    return {"energy": energies, "correlation_maxT": rmax, "sign_maxT": amax, "correlation_by_target": r_by, "sign_by_target": a_by}


def topology_result(z, targets, nulls):
    out = {}
    for name, t in targets.items():
        rr = b58.corr(z, t)
        a = d58.sign_agreement(z, t)
        pa = c58.empirical_upper_p(a, nulls["sign_maxT"])
        if rr is None:
            r, pr, passed = None, None, False
        else:
            r = float(rr)
            pr = c58.empirical_upper_p(r, nulls["correlation_maxT"])
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


def score(source: str, model: str, rep: int, zl_path: Path, it_path: Path | None) -> dict:
    if model not in MODELS or rep not in REPS or source not in SOURCES:
        raise RuntimeError("model/rep/source outside the frozen family")
    targets, target_authority = load_target_references()
    in_a, adm_info = load_admissible()
    sk = build_skeleton(source, zl_path, it_path)
    X, gen_masks, fits = generate_corpus(sk, model, rep, in_a)
    d = dataset_from_rows(sk, X)
    label = f"{PHASE} {source} {model} rep{rep}"
    ref_ns = f"{PHASE}:{source}:{model}:rep{rep}:reference-null"
    test_ns = f"{PHASE}:{source}:{model}:rep{rep}:test-null"

    real_q = q_views_candidate(d, d["X"], True)
    sref = build_reference(d, ref_ns, label)
    real_z = residualize(real_q, sref)
    E = c58.residual_energy(real_z["full"])
    W = reliability(real_z)
    nulls = test_nulls(d, sref, targets, test_ns, label)
    p_exist = c58.empirical_upper_p(E, nulls["energy"])
    existence_pass = bool(W["valid_folds"] >= 4 and W["median"] is not None and W["median"] >= 0.50 and p_exist <= 0.01)
    topology = topology_result(real_z["full"], targets, nulls)
    r1_pass = bool(existence_pass and all(x["effect_and_familywise_gate_pass"] for x in topology.values()))

    return {
        "schema": "ogh-a-score-v1",
        "phase": PHASE,
        "target_reveal": True,
        "source": source,
        "model": model,
        "rep": rep,
        "primary_realization": rep == 0,
        "non_promoting_model": model in NON_PROMOTING,
        "environment": environment(),
        "target_authority": target_authority,
        "admissible_authority": adm_info,
        "skeleton": {
            "identity": sk["identity"],
            "visible_tokens": sk["visible"],
            "parsed_tokens": sk["parsed"],
            "n_lines": sk["n_lines"],
            "fold_parsed_tokens": sk["fold_counts"],
            "layout_only": True,
        },
        "generation": {
            "seed_labels": [seed_label(source, model, f, rep) for f in range(N_FOLDS)],
            "corpus_sha256": sha256_bytes(X.tobytes()),
            "generated_signature_count": int(len(np.unique(gen_masks))),
            "generated_slot_marginals": X.mean(axis=0).tolist(),
            "generated_count_distribution": (np.bincount(X.sum(axis=1), minlength=N_SLOTS + 1)[1:] / len(X)).tolist(),
            "per_fold": [{k: v for k, v in x.items() if k != "p"} for x in fits],
        },
        "null_design": {
            "reference_namespace": ref_ns,
            "test_namespace": test_ns,
            "n_reference": N_REF,
            "n_test": N_TEST,
            "residual_transform": "candidate-owned reference empirical mid-rank normal score",
            "null_operation": "within-line, per-slot occupancy permutation across the line's tokens",
        },
        "pairs": [list(map(int, p)) for p in PAIRS],
        "real_R1": {
            "q_full": real_q["full"].tolist(),
            "z_full": real_z["full"].tolist(),
            "residual_energy": E,
            "within_reliability": W,
        },
        "R1_residual_existence": {"E": E, "W": W["median"], "valid_reliability_folds": W["valid_folds"], "p_exist_maxT_candidate_family": p_exist, "pass": existence_pass},
        "R1_topology": topology,
        "R1_pass": r1_pass,
        "test_null": {
            "energy_summary": c58.summary(nulls["energy"]),
            "correlation_maxT_summary": c58.summary(nulls["correlation_maxT"]),
            "sign_maxT_summary": c58.summary(nulls["sign_maxT"]),
            "correlation_by_target_summary": {k: c58.summary(v) for k, v in nulls["correlation_by_target"].items()},
            "sign_by_target_summary": {k: c58.summary(v) for k, v in nulls["sign_by_target"].items()},
            "energy_values": nulls["energy"].tolist(),
            "correlation_maxT_values": nulls["correlation_maxT"].tolist(),
            "sign_maxT_values": [int(x) for x in nulls["sign_maxT"]],
        },
        "interpretation_boundary": {
            "plaintext_recovered": False,
            "historical_identity_established": False,
            "spaces_proven_linguistic_words": False,
            "decipherment_established": False,
        },
    }


# ----------------------------------------------------------------------------
# preflight (target blind)

def preflight(source: str, zl_path: Path, it_path: Path | None) -> dict:
    in_a, adm_info = load_admissible()
    sk = build_skeleton(source, zl_path, it_path)
    obs = sk["observed_masks"]
    if np.any(~in_a[obs - 1]):
        raise RuntimeError("observed signature outside admissible set")
    models = {}
    for model in MODELS:
        fits = fit_all_folds(sk, model, in_a)
        models[model] = {
            "per_fold": [{k: v for k, v in x.items() if k != "p"} for x in fits],
            "all_folds_fit_ok": all(x["fit"]["fit_ok"] for x in fits),
            "mean_heldout_loglik": float(np.mean([x["heldout_loglik"]["mean_log_likelihood"] for x in fits])) if all(x["heldout_loglik"]["mean_log_likelihood"] is not None for x in fits) else None,
            "mean_heldout_loglik_covered": float(np.mean([x["heldout_loglik"]["mean_log_likelihood_covered"] for x in fits])),
            "mean_heldout_zero_probability_fraction": float(np.mean([x["heldout_loglik"]["zero_probability_fraction"] for x in fits])),
            "free_parameters": fits[0]["fit"]["free_parameters"],
        }
        for rep in REPS:
            X, gen_masks, _ = generate_corpus(sk, model, rep, in_a)
            models[model][f"rep{rep}_corpus_sha256"] = sha256_bytes(X.tobytes())
    counts = sig_counts(obs)
    return {
        "schema": "ogh-a-preflight-v1",
        "phase": PHASE,
        "target_reveal": False,
        "real_R1_pair_or_residual_metrics_computed": False,
        "source": source,
        "environment": environment(),
        "admissible_authority": adm_info,
        "skeleton": {"identity": sk["identity"], "visible_tokens": sk["visible"], "parsed_tokens": sk["parsed"], "n_lines": sk["n_lines"], "fold_parsed_tokens": sk["fold_counts"]},
        "observed_signature_inventory": {
            "n_distinct_signatures": int(np.sum(counts > 0)),
            "fraction_of_admissible_used": float(np.sum(counts > 0) / in_a.sum()),
            "slot_marginals": (counts @ BITS / counts.sum()).tolist(),
            "count_distribution": (np.bincount(COUNTS, weights=counts, minlength=N_SLOTS + 1)[1:] / counts.sum()).tolist(),
        },
        "models": models,
    }


# ----------------------------------------------------------------------------
# aggregate

def classify(results_by_model: dict) -> str:
    def ok(m):
        return bool(results_by_model[m]["R1_pass"])
    if ok("G1"):
        return "REPRESENTATION-ADMISSIBILITY DOMINANT"
    if ok("G2") or ok("G3"):
        return "LOWER-ORDER SUFFICIENT"
    if ok("G4"):
        return "COMPACT CONSTRUCTION GRAMMAR SUFFICIENT"
    if ok("G5"):
        return "PAIRWISE-MOMENT SUFFICIENT ONLY"
    if ok("G6"):
        return "INVENTORY-ONLY SUFFICIENT"
    return "NO TESTED TOKEN-IID MODEL SUFFICIENT"


def aggregate(result_dir: Path) -> dict:
    files = sorted(result_dir.glob("*.json"))
    rows = {}
    for f in files:
        r = json.loads(f.read_text(encoding="utf-8"))
        if r.get("schema") != "ogh-a-score-v1":
            continue
        rows[(r["source"], r["model"], r["rep"])] = (f, r)
    expected = {(s, m, rep) for s in SOURCES for m in MODELS for rep in REPS}
    missing = sorted(expected - set(rows))
    table = {}
    for (s, m, rep), (f, r) in sorted(rows.items()):
        table.setdefault(s, {}).setdefault(m, {})[f"rep{rep}"] = {
            "file": f.name,
            "sha256": sha256_file(f),
            "E": r["R1_residual_existence"]["E"],
            "W": r["R1_residual_existence"]["W"],
            "p_exist": r["R1_residual_existence"]["p_exist_maxT_candidate_family"],
            "existence_pass": r["R1_residual_existence"]["pass"],
            "r_ZL3b": r["R1_topology"]["ZL3b"]["pearson"],
            "signs_ZL3b": r["R1_topology"]["ZL3b"]["sign_agreement"],
            "r_IT2a": r["R1_topology"]["IT2a"]["pearson"],
            "signs_IT2a": r["R1_topology"]["IT2a"]["sign_agreement"],
            "p_R_maxT": {k: v["p_R_maxT_over_target_readings"] for k, v in r["R1_topology"].items()},
            "p_sign_maxT": {k: v["p_sign_maxT_over_target_readings"] for k, v in r["R1_topology"].items()},
            "R1_pass": r["R1_pass"],
            "test_null_energy_max": r["test_null"]["energy_summary"]["max"],
            "mean_heldout_loglik": (
                float(np.mean([x["heldout_loglik"]["mean_log_likelihood"] for x in r["generation"]["per_fold"]]))
                if all(x["heldout_loglik"]["mean_log_likelihood"] is not None for x in r["generation"]["per_fold"]) else None
            ),
            "free_parameters": r["generation"]["per_fold"][0]["fit"]["free_parameters"],
        }
    out = {"schema": "ogh-a-aggregate-v1", "phase": PHASE, "environment": environment(), "n_results": len(rows), "missing": [list(x) for x in missing], "table": table}
    verdict = {}
    for s in SOURCES:
        if s in table and all(m in table[s] and "rep0" in table[s][m] for m in MODELS):
            prim = {m: {"R1_pass": table[s][m]["rep0"]["R1_pass"]} for m in MODELS}
            g0 = table[s]["G0"]["rep0"]
            verdict[s] = {
                "classification_rep0": classify(prim),
                "G0_sanity_gate": {"G0_R1_pass": g0["R1_pass"], "G0_E": g0["E"], "G0_test_null_energy_max": g0["test_null_energy_max"], "scorer_valid": (not g0["R1_pass"]) and g0["E"] <= g0["test_null_energy_max"] * 1.5},
                "rep0_pass_pattern": {m: table[s][m]["rep0"]["R1_pass"] for m in MODELS},
                "all_rep_pass_pattern": {m: {k: v["R1_pass"] for k, v in table[s][m].items()} for m in MODELS},
            }
    out["verdict"] = verdict
    if all(s in verdict for s in SOURCES):
        same = verdict["ZL3b"]["rep0_pass_pattern"] == verdict["IT2a"]["rep0_pass_pattern"]
        out["primary_classification"] = verdict["ZL3b"]["classification_rep0"]
        out["replication_arm_classification"] = verdict["IT2a"]["classification_rep0"]
        out["hierarchy_verdict_replicated_across_skeletons"] = bool(same and verdict["ZL3b"]["classification_rep0"] == verdict["IT2a"]["classification_rep0"])
        out["scorer_valid_both_arms"] = bool(verdict["ZL3b"]["G0_sanity_gate"]["scorer_valid"] and verdict["IT2a"]["G0_sanity_gate"]["scorer_valid"])
    return out


# ----------------------------------------------------------------------------

def self_test():
    assert len(PAIRS) == 66 and N_REF == 1000 and N_TEST == 1000 and N_FOLDS == 5
    m = rows_to_masks(masks_to_rows(np.arange(1, 4096)))
    assert np.array_equal(m, np.arange(1, 4096))
    # maxent on a toy support reproduces marginals
    rng = np.random.default_rng(1)
    sup = np.zeros(N_SIG, dtype=bool)
    sup[rng.choice(N_SIG, 300, replace=False)] = True
    cnt = np.zeros(N_SIG)
    idx = np.flatnonzero(sup)
    cnt[idx] = rng.integers(0, 50, size=len(idx))
    fit = fit_maxent(BITS, sup, cnt, "toy")
    assert fit["fit_ok"], fit["max_moment_error"]
    p = fit["p"]
    assert np.all(p[~sup] == 0) and abs(p.sum() - 1) < 1e-9
    emp = cnt / cnt.sum()
    assert np.max(np.abs(p @ BITS - emp @ BITS)) < 1e-6
    # G4 on toy data yields a valid distribution restricted to support
    toy_masks = np.repeat(idx + 1, cnt[idx].astype(int))
    g4 = fit_model("G4", toy_masks, sup)
    assert abs(g4["p"].sum() - 1) < 1e-9 and np.all(g4["p"][~sup] == 0)
    # classification order
    def fake(passes):
        return {m: {"R1_pass": m in passes} for m in MODELS}
    assert classify(fake({"G1", "G2", "G6"})) == "REPRESENTATION-ADMISSIBILITY DOMINANT"
    assert classify(fake({"G3", "G6"})) == "LOWER-ORDER SUFFICIENT"
    assert classify(fake({"G4", "G5", "G6"})) == "COMPACT CONSTRUCTION GRAMMAR SUFFICIENT"
    assert classify(fake({"G5", "G6"})) == "PAIRWISE-MOMENT SUFFICIENT ONLY"
    assert classify(fake({"G6"})) == "INVENTORY-ONLY SUFFICIENT"
    assert classify(fake(set())) == "NO TESTED TOKEN-IID MODEL SUFFICIENT"
    print(json.dumps({"OGH-A_self_test": "ok", "n_edges": 66, "n_ref": N_REF, "n_test": N_TEST, "real_candidate_target_scored": False}, sort_keys=True))


def main(argv):
    if len(argv) >= 2 and argv[1] == "--self-test":
        self_test()
    elif len(argv) == 3 and argv[1] == "--admissible":
        parser = e.SlotParser()
        payload = admissible_payload(parser)
        Path(argv[2]).write_text(json.dumps(payload, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({k: payload[k] for k in ("n_admissible", "n_distinct_candidate_strings", "by_occupancy_count", "single_slot_admissible", "seconds")}, sort_keys=True))
    elif len(argv) in (5, 6) and argv[1] == "--preflight":
        source = argv[2]
        zl = Path(argv[3]).resolve()
        it = Path(argv[4]).resolve() if len(argv) == 6 else None
        out = Path(argv[-1])
        r = preflight(source, zl, it)
        out.write_text(json.dumps(r, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({m: {"fit_ok": v["all_folds_fit_ok"], "params": v["free_parameters"], "heldout_ll": v["mean_heldout_loglik"], "zero_frac": v["mean_heldout_zero_probability_fraction"]} for m, v in r["models"].items()}, sort_keys=True))
    elif len(argv) in (7, 8) and argv[1] == "--score":
        source, model, rep = argv[2], argv[3], int(argv[4])
        zl = Path(argv[5]).resolve()
        it = Path(argv[6]).resolve() if len(argv) == 8 else None
        out = Path(argv[-1])
        r = score(source, model, rep, zl, it)
        out.write_text(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({"source": source, "model": model, "rep": rep, "E": r["R1_residual_existence"]["E"], "W": r["R1_residual_existence"]["W"], "p_exist": r["R1_residual_existence"]["p_exist_maxT_candidate_family"], "r_ZL3b": r["R1_topology"]["ZL3b"]["pearson"], "signs_ZL3b": r["R1_topology"]["ZL3b"]["sign_agreement"], "r_IT2a": r["R1_topology"]["IT2a"]["pearson"], "signs_IT2a": r["R1_topology"]["IT2a"]["sign_agreement"], "R1_pass": r["R1_pass"]}, sort_keys=True))
    elif len(argv) == 4 and argv[1] == "--aggregate":
        r = aggregate(Path(argv[2]))
        Path(argv[3]).write_text(json.dumps(r, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({k: r.get(k) for k in ("n_results", "missing", "primary_classification", "replication_arm_classification", "hierarchy_verdict_replicated_across_skeletons", "scorer_valid_both_arms")}, sort_keys=True))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
