#!/usr/bin/env python3
"""Issue #75 Phase F target-blind M6 generator.

M6-KRS-GATED-2MIX-CHAIN uses the already-frozen Phase-F0 G2 parameters with
no Phase-F fitting. It reconstructs the five cross-fitted full 4095-state
probability vectors and generates exactly 31 deterministic candidate corpora.

No R1 target reference is imported or scored by this executable.

Usage:
    python phase75f_generator_support.py ZL3B_PATH OUTPUT_JSON
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
from scipy.special import expit, logsumexp

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75e_generator_support as egen  # noqa: E402
import phase75f0_stable_runner as stable  # noqa: E402

PLAN_F_PATH = HERE / "PLAN_F.md"
F0_AUTHORITY_PATH = HERE / "stage-f0" / "phase75f0_training_latent_diagnostic.json"

FAMILY = "M6-KRS-GATED-2MIX-CHAIN"
SCHEMA = "issue75-phaseF-m6-krs-gated-2mix-generator-authority-v1"
STATUS = "M6_KRS_GATED_TWO_LATENT_CHAIN_MODES_31_CORPORA_FROZEN_TARGET_BLIND"
F0_AUTHORITY_SHA256 = "999d9990449875708019ad71aa3a1d253afad19edada88cb45eb4204349887c6"
N_FOLDS = 5
N_REPS = 31
N_SLOTS = 12
EXPECTED_SELECTED_STARTS = [3, 6, 4, 7, 6]
PARAMETER_COUNT = 46


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def occupancy_sha(X: np.ndarray) -> str:
    X = np.asarray(X, dtype=np.uint8)
    if X.shape != (egen.cgen.a0.EXPECTED_PARSED, N_SLOTS):
        raise RuntimeError(f"M6 occupancy shape mismatch {X.shape}")
    return sha256_bytes(X.tobytes(order="C"))


def load_f0_authority() -> Mapping:
    if not F0_AUTHORITY_PATH.exists():
        raise RuntimeError("frozen Phase-F0 authority is required")
    actual = sha256_file(F0_AUTHORITY_PATH)
    if actual != F0_AUTHORITY_SHA256:
        raise RuntimeError(f"Phase-F0 authority SHA mismatch {actual}")
    r = json.loads(F0_AUTHORITY_PATH.read_text(encoding="utf-8"))
    if r.get("schema") != "issue75-phaseF0-training-latent-diagnostic-v1":
        raise RuntimeError("unexpected Phase-F0 schema")
    if r.get("status") != "PHASE_F0_TRAINING_ONLY_LATENT_FRONTIER_DIAGNOSTIC_COMPLETE":
        raise RuntimeError("Phase-F0 authority is not complete")
    if r.get("selection", {}).get("classification") != "F0_SELECT_KRS_GATED_TWO_MODE_CHAIN":
        raise RuntimeError("Phase-F0 did not select the M6 G2 family")
    if any(v is not False for v in r.get("guardrails", {}).values()):
        raise RuntimeError("Phase-F0 guardrail authority invalid")
    folds = r.get("outer_folds", [])
    if len(folds) != N_FOLDS or [int(x["fold"]) for x in folds] != list(range(N_FOLDS)):
        raise RuntimeError("Phase-F0 physical fold authority incomplete")
    starts = [int(x["g2"]["selected_start_index"]) for x in folds]
    if starts != EXPECTED_SELECTED_STARTS:
        raise RuntimeError(f"unexpected frozen G2 selected starts {starts}")
    return r


def build_dataset(src: Path) -> Mapping:
    cgen = egen.cgen
    if cgen.a0.e.git_blob_sha1(src.read_bytes()) != cgen.a0.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = cgen.a0.e.SlotParser()
    cgen.a0.e.validate_parser(parser)
    d = cgen.a0.b58.build_dataset(src, parser, "min")
    if d["source_blob"] != cgen.a0.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("source blob authority mismatch")
    if d["visible"] != cgen.a0.EXPECTED_VISIBLE or d["parsed"] != cgen.a0.EXPECTED_PARSED:
        raise RuntimeError("frozen token population mismatch")
    fold_counts = [int(np.sum(np.asarray(d["token_folds"]) == f)) for f in range(N_FOLDS)]
    if fold_counts != cgen.a0.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen fold population mismatch {fold_counts}")
    return d


def reconstruct_standardization(train: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    idx = egen.state_indices(np.asarray(train, dtype=np.uint8))
    did = egen.STATE_DESC_ID[idx]
    desc = np.asarray(egen.DESCRIPTORS, dtype=np.float64)[did]
    mean = np.mean(desc, axis=0)
    sd = np.std(desc, axis=0, ddof=0)
    active = sd > 0.0
    return mean, sd, active


def assert_vector_close(name: str, actual: np.ndarray, frozen: Sequence[float], tol: float = 1e-12) -> None:
    expected = np.asarray(frozen, dtype=np.float64)
    actual = np.asarray(actual, dtype=np.float64)
    if actual.shape != expected.shape or np.any(~np.isfinite(actual)) or np.max(np.abs(actual - expected)) > tol:
        raise RuntimeError(f"{name} mismatch actual={actual.tolist()} frozen={expected.tolist()}")


def descriptor_design(mean: np.ndarray, sd: np.ndarray, active: np.ndarray) -> np.ndarray:
    all_desc = np.asarray(egen.DESCRIPTORS, dtype=np.float64)
    safe_sd = np.where(active, sd, 1.0)
    z = (all_desc - mean[None, :]) / safe_sd[None, :]
    z[:, ~active] = 0.0
    return np.column_stack([np.ones(len(all_desc), dtype=np.float64), z])


def frozen_fold_distribution(d: Mapping, f0_fold: Mapping, fold: int) -> dict:
    X = np.asarray(d["X"], dtype=np.uint8)
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    train = X[folds != fold]
    expected_train = egen.cgen.a0.EXPECTED_PARSED - egen.cgen.a0.EXPECTED_FOLD_PARSED[fold]
    if len(train) != expected_train:
        raise RuntimeError(f"M6 training population mismatch fold {fold}")

    frozen_std = f0_fold["descriptor_standardization"]
    mean, sd, active = reconstruct_standardization(train)
    assert_vector_close(f"fold{fold} mean", mean, frozen_std["mean_K_R_S"])
    assert_vector_close(f"fold{fold} sd", sd, frozen_std["population_sd_K_R_S"])
    frozen_active = np.asarray(frozen_std["active_K_R_S"], dtype=bool)
    if not np.array_equal(active, frozen_active):
        raise RuntimeError(f"fold{fold} active K/R/S mismatch")

    g2 = f0_fold["g2"]
    if g2.get("family") != FAMILY or int(g2.get("free_continuous_parameters")) != PARAMETER_COUNT:
        raise RuntimeError(f"fold{fold} frozen G2 family mismatch")
    if int(g2["selected_start_index"]) != EXPECTED_SELECTED_STARTS[fold]:
        raise RuntimeError(f"fold{fold} selected start mismatch")
    theta0 = np.asarray(g2["selected_theta0"], dtype=np.float64)
    theta1 = np.asarray(g2["selected_theta1"], dtype=np.float64)
    gate = np.asarray(g2["gate_intercept_and_K_R_S_slopes"], dtype=np.float64)
    if theta0.shape != (21,) or theta1.shape != (21,) or gate.shape != (4,):
        raise RuntimeError(f"fold{fold} frozen parameter shape mismatch")
    if np.any(~np.isfinite(theta0)) or np.any(~np.isfinite(theta1)) or np.any(~np.isfinite(gate)):
        raise RuntimeError(f"fold{fold} non-finite frozen parameter")

    # Stable conditional component probabilities over every non-empty state.
    lp0, _mu0 = stable.stable_component_logprob_and_mu(theta0)
    lp1, _mu1 = stable.stable_component_logprob_and_mu(theta1)

    design_desc = descriptor_design(mean, sd, active)
    eta_desc = design_desc @ gate
    gate_desc = expit(eta_desc)
    if np.any(~np.isfinite(gate_desc)) or np.min(gate_desc) <= 0.0 or np.max(gate_desc) >= 1.0:
        raise RuntimeError(f"fold{fold} invalid frozen descriptor gate")

    q = egen.cgen.bgen.q_from_training(train)
    desc_counts = egen.cgen.bgen.descriptor_counts(train)
    q_desc = np.zeros(len(egen.DESCRIPTORS), dtype=np.float64)
    for desc, p in q.items():
        q_desc[egen.DESC_TO_ID[desc]] = float(p)
    if abs(float(q_desc.sum()) - 1.0) > 1e-12:
        raise RuntimeError(f"fold{fold} empirical descriptor distribution not normalized")

    did = egen.STATE_DESC_ID
    g_state = gate_desc[did]
    q_state = q_desc[did]
    log_mix = np.logaddexp(np.log1p(-g_state) + lp0, np.log(g_state) + lp1)
    log_full = np.full(len(log_mix), -np.inf, dtype=np.float64)
    live = q_state > 0.0
    log_full[live] = np.log(q_state[live]) + log_mix[live]
    global_lz = float(logsumexp(log_full[live]))
    prob = np.zeros(len(log_full), dtype=np.float64)
    prob[live] = np.exp(log_full[live] - global_lz)
    psum = float(prob.sum())
    if not math.isfinite(psum) or psum <= 0.0:
        raise RuntimeError(f"fold{fold} invalid full-state probability sum")
    prob /= psum
    if np.any(~np.isfinite(prob)) or np.any(prob < 0.0) or abs(float(prob.sum()) - 1.0) > 1e-12:
        raise RuntimeError(f"fold{fold} full-state distribution normalization failure")

    # Descriptor mass must reproduce the training-only empirical q(d).
    reconstructed_q = np.bincount(did, weights=prob, minlength=len(egen.DESCRIPTORS))
    max_q_error = float(np.max(np.abs(reconstructed_q - q_desc)))
    if max_q_error > 2e-12:
        raise RuntimeError(f"fold{fold} descriptor mass mismatch {max_q_error}")

    classes = []
    for desc in sorted(q):
        di = egen.DESC_TO_ID[desc]
        classes.append({
            "K": int(desc[0]),
            "R": int(desc[1]),
            "S": int(desc[2]),
            "train_count": int(desc_counts[desc]),
            "probability": float(q[desc]),
            "gate_probability_mode1": float(gate_desc[di]),
            "possible_state_count": int(len(egen.cgen.bgen.DESC_TO_INDEX[desc])),
        })

    return {
        "prob": prob,
        "theta0": theta0,
        "theta1": theta1,
        "gate": gate,
        "mean": mean,
        "sd": sd,
        "active": active,
        "gate_desc": gate_desc,
        "descriptor_classes": classes,
        "normalization_audit": {
            "full_state_sum": float(prob.sum()),
            "global_log_normalizer_before_explicit_renormalization": global_lz,
            "explicit_prerenormalization_sum": psum,
            "max_descriptor_mass_error": max_q_error,
            "minimum_live_state_probability": float(np.min(prob[prob > 0.0])),
            "maximum_state_probability": float(np.max(prob)),
        },
    }


def reconstruct_fits(d: Mapping, f0: Mapping) -> dict[int, dict]:
    out = {}
    for fold in range(N_FOLDS):
        out[fold] = frozen_fold_distribution(d, f0["outer_folds"][fold], fold)
    return out


def generate_case(d: Mapping, fits: Mapping[int, Mapping], rep: int) -> np.ndarray:
    if rep not in range(N_REPS):
        raise RuntimeError("Phase-F rep outside frozen range")
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = np.zeros((egen.cgen.a0.EXPECTED_PARSED, N_SLOTS), dtype=np.uint8)
    for fold in range(N_FOLDS):
        mask = folds == fold
        n = int(mask.sum())
        if n != egen.cgen.a0.EXPECTED_FOLD_PARSED[fold]:
            raise RuntimeError(f"M6 held-out population mismatch fold {fold}")
        ns = f"issue75:phaseF:M6-KRS-GATED-2MIX-CHAIN:rep{rep}:fold{fold}:generate"
        out[mask] = egen.cgen.a0.sample_prob(np.asarray(fits[fold]["prob"], dtype=np.float64), n, ns)
    if np.any(out.sum(axis=1) == 0):
        raise RuntimeError("M6 generated all-zero occupancy signature")
    return out


def case_summary(X: np.ndarray, rep: int, folds: np.ndarray) -> dict:
    unary, adj = egen.cgen.empirical_moments(X)
    code = (
        X.astype(np.uint16)
        * (1 << np.arange(N_SLOTS, dtype=np.uint16))[None, :]
    ).sum(axis=1)
    counts = egen.cgen.bgen.descriptor_counts(X)
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
                {
                    "K": int(desc[0]),
                    "R": int(desc[1]),
                    "S": int(desc[2]),
                    "count": int(counts[desc]),
                    "probability": float(counts[desc] / total),
                }
                for desc in sorted(counts)
            ],
        },
        "distinct_signatures": int(len(np.unique(code))),
        "all_zero_count": int(np.sum(X.sum(axis=1) == 0)),
        "pair_Q_computed": False,
        "residual_Z_computed": False,
        "target_topology_loaded": False,
        "target_correlation_computed": False,
    }


def public_fold_fit(fit: Mapping, f0_fold: Mapping, fold: int) -> dict:
    return {
        "fold": fold,
        "f0_selected_start_index": int(f0_fold["g2"]["selected_start_index"]),
        "free_continuous_parameters": PARAMETER_COUNT,
        "component0_theta_free": [float(v) for v in fit["theta0"]],
        "component1_theta_free": [float(v) for v in fit["theta1"]],
        "gate_intercept_and_K_R_S_slopes": [float(v) for v in fit["gate"]],
        "descriptor_standardization": {
            "mean_K_R_S": [float(v) for v in fit["mean"]],
            "population_sd_K_R_S": [float(v) for v in fit["sd"]],
            "active_K_R_S": [bool(v) for v in fit["active"]],
        },
        "minimum_descriptor_gate_probability": float(np.min(fit["gate_desc"])),
        "maximum_descriptor_gate_probability": float(np.max(fit["gate_desc"])),
        "descriptor_classes": list(fit["descriptor_classes"]),
        "normalization_audit": dict(fit["normalization_audit"]),
        "phase_f_refit_performed": False,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 3:
        raise SystemExit(f"usage: {argv[0]} ZL3B_PATH OUTPUT_JSON")
    src = Path(argv[1]).resolve()
    out_path = Path(argv[2]).resolve()
    if not PLAN_F_PATH.exists():
        raise RuntimeError("PLAN_F.md required before Phase-F execution")
    plan_sha = sha256_file(PLAN_F_PATH)
    f0 = load_f0_authority()
    d = build_dataset(src)
    fits = reconstruct_fits(d, f0)

    fit_public = {
        str(fold): public_fold_fit(fits[fold], f0["outer_folds"][fold], fold)
        for fold in range(N_FOLDS)
    }
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    cases = []
    for rep in range(N_REPS):
        Xg = generate_case(d, fits, rep)
        cases.append(case_summary(Xg, rep, folds))
    if len(cases) != N_REPS or {int(x["rep"]) for x in cases} != set(range(N_REPS)):
        raise RuntimeError("M6 generated case population incomplete")
    if len({x["occupancy_sha256"] for x in cases}) != N_REPS:
        raise RuntimeError("M6 generated duplicate occupancy corpora")
    if any(int(x["all_zero_count"]) != 0 for x in cases):
        raise RuntimeError("M6 generated all-zero state")

    authority = {
        "schema": SCHEMA,
        "status": STATUS,
        "scientific_role": "PRETARGET_FROZEN_F0_PARAMETER_KRS_GATED_TWO_MODE_GENERATOR_AUTHORITY",
        "family": FAMILY,
        "plan_f_sha256": plan_sha,
        "phase_f0_authority_sha256": F0_AUTHORITY_SHA256,
        "source": {
            "ZL3b_blob": str(d["source_blob"]),
            "visible_tokens": int(d["visible"]),
            "parsed_tokens": int(d["parsed"]),
            "fold_parsed_tokens": [int(np.sum(folds == f)) for f in range(N_FOLDS)],
            "parser_policy": "SlotParser(min)",
        },
        "model_definition": {
            "family": FAMILY,
            "descriptor": "exact outer-training empirical P(K,R,S)",
            "latent_states": 2,
            "gate": "logit P(Z=1|K,R,S)=a0+aK*zK+aR*zR+aS*zS using frozen Phase-F0 parameters",
            "component_family": "position-specific unary plus nearest-neighbor interactions conditioned on K/R/S",
            "free_parameters_per_component": 21,
            "free_gate_parameters": 4,
            "free_continuous_parameters": PARAMETER_COUNT,
            "explicit_nonadjacent_parameters": 0,
            "generic_distance_parameters": 0,
            "named_distant_pair_parameters": 0,
            "signature_specific_parameters": 0,
            "phase_f_refit_performed": False,
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
        "plan_f_sha256": plan_sha,
        "phase_f0_authority_sha256": F0_AUTHORITY_SHA256,
        "cases": len(cases),
        "selected_starts": EXPECTED_SELECTED_STARTS,
        "gate_probability_ranges": [
            [fit_public[str(f)]["minimum_descriptor_gate_probability"], fit_public[str(f)]["maximum_descriptor_gate_probability"]]
            for f in range(N_FOLDS)
        ],
        "generated_distinct_signature_range": [
            min(x["distinct_signatures"] for x in cases),
            max(x["distinct_signatures"] for x in cases),
        ],
        "target_access": authority["target_access"],
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
