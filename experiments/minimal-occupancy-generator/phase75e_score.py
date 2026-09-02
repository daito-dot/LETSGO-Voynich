#!/usr/bin/env python3
"""Issue #75 Phase E M5-KRS-2MIX-CHAIN frozen R1 scorer.

Reconstructs one exact Stage-E0 corpus from the permanently frozen target-blind
mixture parameters and requires its occupancy SHA before any target access.
--verify-only stops before Q/Z/targets.

Usage:
    python phase75e_score.py ZL3B_PATH REP OUTPUT_JSON [--verify-only]
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75a_score as a_score  # noqa: E402
import phase75e_generator_support as egen  # noqa: E402

E0_PATH = HERE / "stage-e0" / "generator_authority.json"
E0_FREEZE_PATH = HERE / "E0_FREEZE_E.md"
FAMILY = "M5-KRS-2MIX-CHAIN"
N_REPS = 31


def expected_e0_sha() -> str:
    text = E0_FREEZE_PATH.read_text(encoding="utf-8")
    m = re.search(r"E0 authority SHA-256: `([0-9a-f]{64})`", text)
    if not m:
        raise RuntimeError("E0 authority SHA missing from E0_FREEZE_E.md")
    return m.group(1)


def load_e0() -> tuple[dict, dict[int, dict], str]:
    frozen_sha = expected_e0_sha()
    got = a_score.sha256_file(E0_PATH)
    if got != frozen_sha:
        raise RuntimeError(f"Phase E0 authority SHA changed: {got} != {frozen_sha}")
    r = json.loads(E0_PATH.read_text(encoding="utf-8"))
    if r.get("schema") != "issue75-phaseE0-m5-krs-2mix-chain-generator-authority-v1":
        raise RuntimeError("Phase E0 schema changed")
    if r.get("status") != "M5_KRS_TWO_LATENT_CHAIN_MODES_31_CORPORA_FROZEN_TARGET_BLIND":
        raise RuntimeError("Phase E0 status changed")
    m = r.get("model_definition", {})
    if m.get("family") != FAMILY or m.get("latent_states") != 2 or m.get("free_continuous_parameters") != 43:
        raise RuntimeError("Phase E0 model changed")
    for key in ("explicit_nonadjacent_parameters", "generic_distance_parameters", "named_distant_pair_parameters", "signature_specific_parameters"):
        if m.get(key) != 0:
            raise RuntimeError(f"Phase E0 forbidden flexibility changed: {key}")
    if any(r.get("target_access", {}).values()):
        raise RuntimeError("Phase E0 target firewall not clean")
    if r.get("no_drops") is not True or r.get("no_rerolls") is not True:
        raise RuntimeError("Phase E0 population integrity changed")
    if len(r.get("fit", {})) != 5:
        raise RuntimeError("Phase E0 fit population changed")
    cases = {int(x["rep"]): x for x in r.get("cases", [])}
    if len(cases) != N_REPS or set(cases) != set(range(N_REPS)):
        raise RuntimeError("Phase E0 case population changed")
    return r, cases, frozen_sha


def q_from_frozen_fit(fit: Mapping, X_train: np.ndarray) -> dict[tuple[int, int, int], float]:
    current_counts = egen.cgen.bgen.descriptor_counts(X_train)
    current_q = egen.cgen.bgen.q_from_training(X_train)
    frozen = {
        (int(x["K"]), int(x["R"]), int(x["S"])): x
        for x in fit["descriptor_classes"]
    }
    if set(current_q) != set(frozen):
        raise RuntimeError("Phase E training descriptor support changed")
    for d in sorted(current_q):
        x = frozen[d]
        if int(x["train_count"]) != int(current_counts[d]):
            raise RuntimeError(f"Phase E training descriptor count changed {d}")
        if float(x["probability"]) != float(current_q[d]):
            raise RuntimeError(f"Phase E training descriptor probability changed {d}")
        if int(x["possible_state_count"]) != int(len(egen.cgen.bgen.DESC_TO_INDEX[d])):
            raise RuntimeError(f"Phase E descriptor state-space changed {d}")
    return current_q


def reconstruct_fits(d: Mapping, authority: Mapping) -> tuple[dict[int, dict], dict]:
    X = np.asarray(d["X"], dtype=np.uint8)
    folds = np.asarray(d["token_folds"], dtype=np.int8)
    out = {}
    audits = {}
    for f in range(5):
        train = X[folds != f]
        fit = authority["fit"][str(f)]
        q = q_from_frozen_fit(fit, train)
        t0 = np.asarray(fit["component0"]["theta_free"], dtype=np.float64)
        t1 = np.asarray(fit["component1"]["theta_free"], dtype=np.float64)
        pi = float(fit["pi"])
        if t0.shape != (21,) or t1.shape != (21,) or not (1e-8 < pi < 1-1e-8):
            raise RuntimeError(f"Phase E frozen component parameters invalid fold {f}")
        if fit["free_continuous_parameters"] != 43 or fit["selected_log_likelihood"] < fit["m3_baseline_log_likelihood"] - 1e-8:
            raise RuntimeError(f"Phase E frozen training fit invalid fold {f}")
        prob, norm = egen.mixture_distribution(t0, t1, pi, q)
        if norm["max_descriptor_normalization_error"] > 1e-12 or norm["total_normalization_error"] > 1e-12:
            raise RuntimeError(f"Phase E frozen probability normalization failed fold {f}")
        out[f] = {"prob": prob}
        audits[str(f)] = {
            "selected_start_index": int(fit["selected_start_index"]),
            "pi": pi,
            "selected_log_likelihood_gain_over_m3": float(fit["selected_log_likelihood_gain_over_m3"]),
            "descriptor_distribution_exact_e0": True,
            "frozen_parameter_probability_reconstruction": True,
            "max_descriptor_normalization_error": float(norm["max_descriptor_normalization_error"]),
            "total_normalization_error": float(norm["total_normalization_error"]),
        }
    return out, audits


def build_exact_case(
    src: Path,
    rep: int,
    authority: Mapping,
    cases: Mapping[int, Mapping],
    e0_sha: str,
) -> tuple[dict, np.ndarray, dict]:
    if egen.cgen.a0.e.git_blob_sha1(src.read_bytes()) != egen.cgen.a0.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = egen.cgen.a0.e.SlotParser()
    egen.cgen.a0.e.validate_parser(parser)
    d = egen.cgen.a0.b58.build_dataset(src, parser, "min")
    if d["source_blob"] != egen.cgen.a0.EXPECTED_SOURCE_BLOB or d["visible"] != egen.cgen.a0.EXPECTED_VISIBLE or d["parsed"] != egen.cgen.a0.EXPECTED_PARSED:
        raise RuntimeError("frozen ZL3b population changed")
    fold_counts = [int(np.sum(d["token_folds"] == f)) for f in range(5)]
    if fold_counts != egen.cgen.a0.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen fold population changed: {fold_counts}")

    fits, fit_audits = reconstruct_fits(d, authority)
    X = egen.generate_case(d, fits, rep)
    got_sha = egen.occupancy_sha(X)
    frozen = cases[rep]
    if got_sha != frozen["occupancy_sha256"]:
        raise RuntimeError(f"M5 exact occupancy SHA changed rep {rep}: {got_sha}")

    padded = np.zeros_like(d["padded"], dtype=np.uint8)
    padded[d["line_mask"]] = X
    candidate = {
        "X": X,
        "token_folds": np.asarray(d["token_folds"], dtype=np.int8),
        "padded": padded,
        "line_mask": np.asarray(d["line_mask"], dtype=bool),
    }
    audit = {
        "family": FAMILY,
        "rep": int(rep),
        "occupancy_sha256": got_sha,
        "phase_e0_authority_sha256": e0_sha,
        "tokens": int(len(X)),
        "fold_tokens": fold_counts,
        "all_zero_count": int(np.sum(X.sum(axis=1) == 0)),
        "fit_audits": fit_audits,
        "frozen_parameters_reconstructed": True,
        "exact_phase_e0_replay": True,
        "frozen_case": frozen,
    }
    return candidate, X, audit


def measurement(candidate: Mapping, X: np.ndarray, rep: int) -> dict:
    reference_ns = f"issue75:phaseE:M5-KRS-2MIX-CHAIN:rep{rep}:reference"
    test_ns = f"issue75:phaseE:M5-KRS-2MIX-CHAIN:rep{rep}:test"
    real_q = a_score.q_views_all(candidate, X, include_folds=True)
    sref = a_score.build_reference(candidate, reference_ns)
    z_full = a_score.normal_score_array(real_q["full"], sref["full"])
    z_train = a_score.normal_score_array(real_q["train"], sref["train"])
    z_held = a_score.normal_score_array(real_q["held"], sref["held"])
    E = a_score.residual_energy(z_full)
    fold_r = [a_score.finite_corr(z_train[f], z_held[f]) for f in range(5)]
    W = a_score.median_finite(fold_r)
    test_energy = np.empty(a_score.N_TEST, dtype=np.float64)
    for n in range(a_score.N_TEST):
        Y = a_score.shuffled_flat(candidate, test_ns, n)
        q = a_score.q_views_all(candidate, Y, include_folds=False)["full"]
        z = a_score.normal_score_array(q, sref["full"])
        test_energy[n] = a_score.residual_energy(z)
    p_exist = float((1 + int(np.sum(test_energy >= E))) / (a_score.N_TEST + 1))
    return {
        "reference_namespace": reference_ns,
        "test_namespace": test_ns,
        "n_reference": a_score.N_REF,
        "n_test": a_score.N_TEST,
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


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (4, 5):
        raise SystemExit(f"usage: {argv[0]} ZL3B_PATH REP OUTPUT_JSON [--verify-only]")
    src = Path(argv[1]).resolve()
    rep = int(argv[2])
    out = Path(argv[3]).resolve()
    verify_only = len(argv) == 5 and argv[4] == "--verify-only"
    if rep not in range(N_REPS):
        raise SystemExit("REP must be 0..30")
    if len(argv) == 5 and not verify_only:
        raise SystemExit("only optional flag is --verify-only")

    authority, cases, e0_sha = load_e0()
    candidate, X, audit = build_exact_case(src, rep, authority, cases, e0_sha)
    common = {
        "family": FAMILY,
        "rep": rep,
        "candidate_audit": audit,
        "pair_count": 66,
        "target_readings_averaged": False,
        "no_case_selection": True,
        "no_reroll": True,
    }

    if verify_only:
        result = {
            "schema": "issue75-phaseE-m5-r1-preflight-v1",
            "status": "EXACT_E0_M5_CORPUS_REGENERATED_TARGET_BLIND",
            "scientific_role": "PRETARGET_EXACT_M5_REPLAY_PREFLIGHT",
            **common,
            "target_access": {
                "pair_Q_computed": False,
                "residual_Z_computed": False,
                "Issue58C_target_vector_loaded": False,
                "Issue58D_target_vector_loaded": False,
                "target_correlation_computed": False,
                "T_computed": False,
            },
        }
    else:
        m = measurement(candidate, X, rep)
        z = np.asarray(m["z_full"], dtype=np.float64)
        targets, target_authority = a_score.t68.load_target_references()
        topology = {}
        for name in ("ZL3b", "IT2a"):
            target = np.asarray(targets[name], dtype=np.float64)
            corr = a_score.finite_corr(z, target)
            if corr is None or not math.isfinite(corr):
                raise RuntimeError(f"non-finite topology correlation {name}")
            topology[name] = {
                "pearson": float(corr),
                "sign_agreement": a_score.sign_agreement(z, target),
                "sign_denominator": 66,
            }
        T = float(min(topology["ZL3b"]["pearson"], topology["IT2a"]["pearson"]))
        result = {
            "schema": "issue75-phaseE-m5-r1-score-v1",
            "status": "PHASE_E_M5_FIRST_REVEAL_CASE_SCORED",
            "scientific_role": "TWO_LATENT_LOCAL_CHAIN_COMPLETE_66_EDGE_MEASUREMENT",
            **common,
            "measurement": m,
            "target_authority": target_authority,
            "topology": topology,
            "T": T,
            "target_access": {
                "pair_Q_computed": True,
                "residual_Z_computed": True,
                "Issue58C_target_vector_loaded": True,
                "Issue58D_target_vector_loaded": True,
                "target_correlation_computed": True,
                "T_computed": True,
            },
        }

    raw = a_score.canonical_json_bytes(result) + b"\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "rep": rep,
        "verify_only": verify_only,
        "occupancy_sha256": audit["occupancy_sha256"],
        "E": None if verify_only else result["measurement"]["residual_energy"],
        "p_exist": None if verify_only else result["measurement"]["p_exist"],
        "W": None if verify_only else result["measurement"]["reliability"]["median"],
        "R_ZL3b": None if verify_only else result["topology"]["ZL3b"]["pearson"],
        "R_IT2a": None if verify_only else result["topology"]["IT2a"]["pearson"],
        "T": None if verify_only else result["T"],
        "output_sha256": a_score.sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
