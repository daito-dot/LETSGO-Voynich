#!/usr/bin/env python3
"""OGH-B — one preregistered extension of the G4 successor grammar.

Scientific authority: PLAN_B.md (committed before this executable).

Modes
  --self-test
  --select ZL3b IT2a OUT.json          stage B0: target-blind held-out likelihood selection
  --score SOURCE MODEL REP ZL3b [IT2a] OUT.json   stage B1: frozen R1 scoring of the selected model
  --aggregate DIR OGH_A_AGGREGATE OUT.json        frozen decision against OGH-A G6 anchors

Models G7A (second-order successor) and G7B (K-gated successor) are defined
here and injected into the OGH-A machinery; everything else (skeletons,
admissible set, cross-fitting, R1 scorer, gates) is reused unchanged with
the OGH-B seed/null namespaces.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import numpy as np
from scipy.special import logsumexp

HERE = Path(__file__).resolve()
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
import ogh_a as A  # noqa: E402

A.PHASE = "OGH-B"
NEW_MODELS = ("G7A", "G7B")
A.MODELS = tuple(A.MODELS) + NEW_MODELS
DELTA = 0.009768313008182594
NEAR = 0.03
BACKOFF = 1.0
N_SLOTS = A.N_SLOTS
BITS = A.BITS
COUNTS = A.COUNTS
N_SIG = A.N_SIG

_orig_fit_model = A.fit_model


def g4_conditionals(rows: np.ndarray):
    """G4 conditionals q4[s][ell+1] with add-1/2 smoothing (identical to OGH-A G4)."""
    cond = []
    last = np.full(len(rows), -1, dtype=np.int64)
    for s in range(N_SLOTS):
        ctx = last + 1
        occ = rows[:, s]
        n1 = np.bincount(ctx, weights=occ, minlength=s + 1)
        n0 = np.bincount(ctx, weights=1 - occ, minlength=s + 1)
        cond.append((n1 + 0.5) / (n1 + n0 + 1.0))
        last = np.where(occ == 1, s, last)
    return cond


def state_contexts():
    """For each state and slot s: (ell1, ell2) most recent and second most recent occupied slots before s (-1 if none)."""
    ell1 = np.full((N_SIG, N_SLOTS), -1, dtype=np.int64)
    ell2 = np.full((N_SIG, N_SLOTS), -1, dtype=np.int64)
    l1 = np.full(N_SIG, -1, dtype=np.int64)
    l2 = np.full(N_SIG, -1, dtype=np.int64)
    for s in range(N_SLOTS):
        ell1[:, s] = l1
        ell2[:, s] = l2
        xs = BITS[:, s].astype(np.int64)
        l2 = np.where(xs == 1, l1, l2)
        l1 = np.where(xs == 1, s, l1)
    return ell1, ell2


ELL1, ELL2 = state_contexts()


def fit_g7a(train_masks: np.ndarray, in_a: np.ndarray) -> dict:
    rows = A.masks_to_rows(train_masks).astype(np.int64)
    q4 = g4_conditionals(rows)
    tr1, tr2 = ELL1[train_masks - 1], ELL2[train_masks - 1]
    logp = np.zeros(N_SIG)
    n_ctx = 0
    n_ctx_observed = 0
    for s in range(N_SLOTS):
        # context id = (ell2+1)*(s+1) + (ell1+1); ell2<ell1<s or none
        cid_tr = (tr2[:, s] + 1) * (s + 1) + (tr1[:, s] + 1)
        occ = rows[:, s]
        size = (s + 1) * (s + 1)
        n1 = np.bincount(cid_tr, weights=occ, minlength=size)
        n = np.bincount(cid_tr, minlength=size).astype(np.float64)
        cid_all = (ELL2[:, s] + 1) * (s + 1) + (ELL1[:, s] + 1)
        prior = q4[s][ELL1[:, s] + 1]
        q = (n1[cid_all] + BACKOFF * prior) / (n[cid_all] + BACKOFF)
        xs = BITS[:, s]
        logp += np.where(xs == 1, np.log(q), np.log1p(-q))
        n_ctx += 1 + s + s * (s - 1) // 2
        n_ctx_observed += int(np.sum(n > 0))
    logp[~in_a] = -np.inf
    p = np.exp(logp - logsumexp(logp[in_a]))
    p[~in_a] = 0.0
    return {"p": p, "free_parameters": n_ctx, "contexts_observed_in_training": n_ctx_observed, "backoff_pseudocount": BACKOFF, "fit_ok": True}


def fit_g7b(train_masks: np.ndarray, in_a: np.ndarray) -> dict:
    rows = A.masks_to_rows(train_masks).astype(np.int64)
    q4 = g4_conditionals(rows)
    K_tr = rows.sum(axis=1)
    qK = np.bincount(K_tr, minlength=N_SLOTS + 1).astype(np.float64) / len(rows)
    tr1 = ELL1[train_masks - 1]
    logp_chain = np.zeros(N_SIG)
    n_ctx_observed = 0
    for s in range(N_SLOTS):
        cid_tr = K_tr * (s + 1) + (tr1[:, s] + 1)
        occ = rows[:, s]
        size = (N_SLOTS + 1) * (s + 1)
        n1 = np.bincount(cid_tr, weights=occ, minlength=size)
        n = np.bincount(cid_tr, minlength=size).astype(np.float64)
        cid_all = COUNTS * (s + 1) + (ELL1[:, s] + 1)
        prior = q4[s][ELL1[:, s] + 1]
        q = (n1[cid_all] + BACKOFF * prior) / (n[cid_all] + BACKOFF)
        xs = BITS[:, s]
        logp_chain += np.where(xs == 1, np.log(q), np.log1p(-q))
        n_ctx_observed += int(np.sum(n > 0))
    p = np.zeros(N_SIG)
    for k in range(1, N_SLOTS + 1):
        cls = in_a & (COUNTS == k)
        if qK[k] <= 0 or not cls.any():
            continue
        lp = logp_chain[cls]
        p[cls] = qK[k] * np.exp(lp - logsumexp(lp))
    p /= p.sum()
    n_k = int(np.sum(qK[1:] > 0))
    return {"p": p, "free_parameters": 78 * n_k + (n_k - 1), "K_classes_observed": n_k, "K_distribution": qK[1:].tolist(), "contexts_observed_in_training": n_ctx_observed, "backoff_pseudocount": BACKOFF, "fit_ok": True}


def fit_model(model: str, train_masks: np.ndarray, in_a: np.ndarray) -> dict:
    counts = A.sig_counts(train_masks)
    if np.any(counts[~in_a] > 0):
        raise RuntimeError("observed signature outside admissible set")
    if model == "G7A":
        info = fit_g7a(train_masks, in_a)
    elif model == "G7B":
        info = fit_g7b(train_masks, in_a)
    else:
        return _orig_fit_model(model, train_masks, in_a)
    p = info["p"]
    if not (np.all(p >= 0) and abs(p.sum() - 1.0) < 1e-9):
        raise RuntimeError(f"{model}: invalid probability vector")
    info.update({"model": model, "n_train_tokens": int(len(train_masks))})
    return info


A.fit_model = fit_model


def select(zl_path: Path, it_path: Path) -> dict:
    in_a, adm_info = A.load_admissible()
    out = {"schema": "ogh-b-selection-v1", "phase": "OGH-B", "target_reveal": False, "real_R1_pair_or_residual_metrics_computed": False, "environment": A.environment(), "admissible_authority": adm_info, "arms": {}}
    for source in ("ZL3b", "IT2a"):
        sk = A.build_skeleton(source, zl_path, it_path if source == "IT2a" else None)
        arm = {}
        for m in ("G4", "G7A", "G7B"):
            fits = A.fit_all_folds(sk, m, in_a)
            arm[m] = {
                "heldout_ll_by_fold": [x["heldout_loglik"]["mean_log_likelihood_covered"] for x in fits],
                "heldout_zero_probability_fraction_by_fold": [x["heldout_loglik"]["zero_probability_fraction"] for x in fits],
                "train_ll_by_fold": [x["train_loglik"]["mean_log_likelihood_covered"] for x in fits],
                "free_parameters": fits[0]["fit"]["free_parameters"],
                "per_fold_fit": [{k: v for k, v in x["fit"].items() if k not in ("conditionals_P_occupied_given_last",)} for x in fits],
            }
        for m in NEW_MODELS:
            gains = [a - b for a, b in zip(arm[m]["heldout_ll_by_fold"], arm["G4"]["heldout_ll_by_fold"])]
            arm[m]["gain_over_G4_by_fold"] = gains
            arm[m]["gain_positive_folds"] = int(sum(g > 0 for g in gains))
            arm[m]["median_gain_over_G4"] = float(statistics.median(gains))
            arm[m]["max_heldout_zero_probability_fraction"] = max(arm[m]["heldout_zero_probability_fraction_by_fold"])
            arm[m]["eligible"] = arm[m]["gain_positive_folds"] >= 4 and arm[m]["max_heldout_zero_probability_fraction"] <= 1e-3
        out["arms"][source] = arm
    zl = out["arms"]["ZL3b"]
    elig = [m for m in NEW_MODELS if zl[m]["eligible"]]
    if not elig:
        sel, rule = None, "NO EXTENSION LICENSED"
    elif len(elig) == 1:
        sel, rule = elig[0], "single eligible candidate"
    else:
        ga, gb = zl["G7A"]["median_gain_over_G4"], zl["G7B"]["median_gain_over_G4"]
        if abs(ga - gb) < 0.005:
            sel = "G7A" if zl["G7A"]["free_parameters"] <= zl["G7B"]["free_parameters"] else "G7B"
            rule = "median gains within 0.005 nat/token; parsimony"
        else:
            sel = "G7A" if ga > gb else "G7B"
            rule = "larger median held-out gain"
    out["selection"] = {"selected": sel, "rule": rule, "selection_arm": "ZL3b", "IT2a_used_for_selection": False}
    return out


def aggregate(result_dir: Path, ogh_a_aggregate: Path) -> dict:
    a = json.loads(ogh_a_aggregate.read_text(encoding="utf-8"))
    rows = {}
    for f in sorted(result_dir.glob("*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        if r.get("schema") == "ogh-a-score-v1" and r.get("phase") == "OGH-B":
            rows.setdefault(r["source"], {}).setdefault(r["model"], {})[f"rep{r['rep']}"] = {
                "file": f.name, "sha256": A.sha256_file(f), "E": r["R1_residual_existence"]["E"], "W": r["R1_residual_existence"]["W"],
                "p_exist": r["R1_residual_existence"]["p_exist_maxT_candidate_family"],
                "r_ZL3b": r["R1_topology"]["ZL3b"]["pearson"], "signs_ZL3b": r["R1_topology"]["ZL3b"]["sign_agreement"],
                "r_IT2a": r["R1_topology"]["IT2a"]["pearson"], "signs_IT2a": r["R1_topology"]["IT2a"]["sign_agreement"],
                "R1_pass": r["R1_pass"], "T": min(r["R1_topology"]["ZL3b"]["pearson"], r["R1_topology"]["IT2a"]["pearson"]),
            }
    out = {"schema": "ogh-b-aggregate-v1", "phase": "OGH-B", "environment": A.environment(), "ogh_a_aggregate_sha256": A.sha256_file(ogh_a_aggregate), "delta": DELTA, "near": NEAR, "table": rows, "arms": {}}
    models = sorted({m for s in rows for m in rows[s]})
    if len(models) != 1:
        out["decision"] = "INVALID: expected exactly one scored model"
        return out
    m = models[0]
    ok_all = True
    for source in ("ZL3b", "IT2a"):
        reps = rows.get(source, {}).get(m, {})
        if len(reps) != 3:
            out["decision"] = "INVALID: incomplete population"
            return out
        g6 = statistics.median(min(v["r_ZL3b"], v["r_IT2a"]) for v in a["table"][source]["G6"].values())
        g4 = statistics.median(min(v["r_ZL3b"], v["r_IT2a"]) for v in a["table"][source]["G4"].values())
        g5 = statistics.median(min(v["r_ZL3b"], v["r_IT2a"]) for v in a["table"][source]["G5"].values())
        medT = statistics.median(v["T"] for v in reps.values())
        gate = all(v["R1_pass"] for v in reps.values())
        out["arms"][source] = {"model": m, "median_T": medT, "G4_median_T_OGH_A": g4, "G5_median_T_OGH_A": g5, "G6_median_T_OGH_A": g6, "gap_to_G6": medT - g6, "gain_over_G4": medT - g4, "issue68_gate_all_reps": gate, "within_delta": medT - g6 >= -DELTA, "within_near": medT - g6 >= -NEAR}
    arms = out["arms"]
    if all(x["within_delta"] and x["issue68_gate_all_reps"] for x in arms.values()):
        out["decision"] = "SUCCESSOR GRAMMAR SUFFICIENT UNDER M+ EQUIVALENCE"
    elif all(x["issue68_gate_all_reps"] and x["within_near"] for x in arms.values()):
        out["decision"] = "SUCCESSOR GRAMMAR NEAR-SUFFICIENT"
    else:
        out["decision"] = "SUCCESSOR EXTENSIONS INSUFFICIENT"
    return out


def self_test():
    rng = np.random.default_rng(3)
    in_a = np.ones(N_SIG, dtype=bool)
    masks = rng.choice(np.arange(1, N_SIG + 1), size=5000, p=None)
    for m in NEW_MODELS:
        f = fit_model(m, masks, in_a)
        assert abs(f["p"].sum() - 1) < 1e-9 and np.all(f["p"] >= 0)
    # G7A/G7B with no data beyond prior collapse toward G4 shape on tiny data
    assert fit_model("G7A", masks[:50], in_a)["free_parameters"] == 298
    assert A.PHASE == "OGH-B" and "G7A" in A.MODELS
    assert A.seed_label("ZL3b", "G7A", 0, 0).startswith("OGH-B:")
    print(json.dumps({"OGH-B_self_test": "ok", "real_candidate_target_scored": False}))


def main(argv):
    if len(argv) >= 2 and argv[1] == "--self-test":
        self_test()
    elif len(argv) == 5 and argv[1] == "--select":
        r = select(Path(argv[2]).resolve(), Path(argv[3]).resolve())
        Path(argv[4]).write_text(json.dumps(r, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        summary = {s: {m: {"heldout": r["arms"][s][m]["heldout_ll_by_fold"], "gain": r["arms"][s][m].get("gain_over_G4_by_fold"), "params": r["arms"][s][m]["free_parameters"]} for m in ("G4", "G7A", "G7B")} for s in r["arms"]}
        print(json.dumps({"selection": r["selection"], "arms": summary}, indent=1))
    elif len(argv) in (7, 8) and argv[1] == "--score":
        source, model, rep = argv[2], argv[3], int(argv[4])
        if model not in NEW_MODELS:
            raise SystemExit("OGH-B scores only G7A/G7B")
        zl = Path(argv[5]).resolve()
        it = Path(argv[6]).resolve() if len(argv) == 8 else None
        r = A.score(source, model, rep, zl, it)
        Path(argv[-1]).write_text(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({"source": source, "model": model, "rep": rep, "E": r["R1_residual_existence"]["E"], "W": r["R1_residual_existence"]["W"], "r_ZL3b": r["R1_topology"]["ZL3b"]["pearson"], "signs_ZL3b": r["R1_topology"]["ZL3b"]["sign_agreement"], "r_IT2a": r["R1_topology"]["IT2a"]["pearson"], "signs_IT2a": r["R1_topology"]["IT2a"]["sign_agreement"], "R1_pass": r["R1_pass"]}, sort_keys=True))
    elif len(argv) == 5 and argv[1] == "--aggregate":
        r = aggregate(Path(argv[2]), Path(argv[3]))
        Path(argv[4]).write_text(json.dumps(r, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({"decision": r.get("decision"), "arms": r.get("arms")}, indent=1))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
