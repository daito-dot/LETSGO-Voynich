#!/usr/bin/env python3
"""Issue #75 Phase C M3-KRS-CHAIN frozen candidate-owned R1 scorer.

Regenerates one exact target-blind Stage-C0 corpus and requires its frozen
occupancy SHA before target access. --verify-only stops before Q/Z/target load.

Usage:
    python phase75c_score.py ZL3B_PATH REP OUTPUT_JSON [--verify-only]
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

import phase75a_generator_support as a0gen  # noqa: E402
import phase75a_score as a_score  # noqa: E402
import phase75c_generator_support as cgen  # noqa: E402

C0_PATH = HERE / "stage-c0" / "generator_authority.json"
C0_FREEZE_PATH = HERE / "C0_FREEZE_C.md"
FAMILY = "M3-KRS-CHAIN"
N_REPS = 31


def expected_c0_sha() -> str:
    if not C0_FREEZE_PATH.exists():
        raise RuntimeError("C0_FREEZE_C.md missing")
    text = C0_FREEZE_PATH.read_text(encoding="utf-8")
    m = re.search(r"C0 authority SHA-256: `([0-9a-f]{64})`", text)
    if not m:
        raise RuntimeError("C0 authority SHA missing from C0_FREEZE_C.md")
    return m.group(1)


def load_c0() -> tuple[dict, dict[int, dict], str]:
    frozen_sha = expected_c0_sha()
    got = a_score.sha256_file(C0_PATH)
    if got != frozen_sha:
        raise RuntimeError(f"Phase C0 authority SHA changed: {got} != {frozen_sha}")
    r = json.loads(C0_PATH.read_text(encoding="utf-8"))
    if r.get("schema") != "issue75-phaseC0-m3-krs-chain-generator-authority-v1":
        raise RuntimeError("Phase C0 schema changed")
    if r.get("status") != "M3_KRS_CHAIN_31_CORPORA_FROZEN_TARGET_BLIND":
        raise RuntimeError("Phase C0 status changed")
    if r.get("model_definition", {}).get("family") != FAMILY:
        raise RuntimeError("Phase C0 family changed")
    if r.get("model_definition", {}).get("free_continuous_parameters") != 21:
        raise RuntimeError("Phase C0 parameterization changed")
    if r.get("model_definition", {}).get("explicit_nonadjacent_pair_interaction_parameters") != 0:
        raise RuntimeError("Phase C0 introduced nonadjacent pair parameters")
    if any(r.get("target_access", {}).values()):
        raise RuntimeError("Phase C0 target firewall not clean")
    if r.get("no_drops") is not True or r.get("no_rerolls") is not True:
        raise RuntimeError("Phase C0 population integrity changed")
    cases = {int(x["rep"]): x for x in r.get("cases", [])}
    if len(cases) != N_REPS or set(cases) != set(range(N_REPS)):
        raise RuntimeError("Phase C0 case population changed")
    return r, cases, frozen_sha


def descriptor_map(fit: Mapping) -> dict[tuple[int, int, int], dict]:
    return {
        (int(x["K"]), int(x["R"]), int(x["S"])): x
        for x in fit["descriptor_classes"]
    }


def validate_refit(current: Mapping, frozen: Mapping) -> float:
    maxerr = 0.0
    for f in range(5):
        cur = current[str(f)]
        old = frozen[str(f)]
        if cur["target_unary"] != old["target_unary"]:
            raise RuntimeError(f"M3 training unary moments changed fold {f}")
        if cur["target_adjacent_joint"] != old["target_adjacent_joint"]:
            raise RuntimeError(f"M3 training adjacent moments changed fold {f}")
        cdesc = descriptor_map(cur)
        odesc = descriptor_map(old)
        if set(cdesc) != set(odesc):
            raise RuntimeError(f"M3 descriptor support changed fold {f}")
        for d in cdesc:
            for key in ("K", "R", "S", "train_count", "possible_state_count"):
                if cdesc[d][key] != odesc[d][key]:
                    raise RuntimeError(f"M3 descriptor authority changed fold {f} {d} {key}")
            if cdesc[d]["probability"] != odesc[d]["probability"]:
                raise RuntimeError(f"M3 descriptor probability changed fold {f} {d}")
        if cur["descriptor_class_count"] != old["descriptor_class_count"]:
            raise RuntimeError(f"M3 descriptor class count changed fold {f}")
        if cur["training_distinct_signatures"] != old["training_distinct_signatures"]:
            raise RuntimeError(f"M3 training distinct signatures changed fold {f}")
        audit = cur["descriptor_identity_audit"]
        if float(audit["abs_error_K_identity"]) > 1e-12:
            raise RuntimeError(f"M3 K identity failed fold {f}")
        if float(audit["abs_error_adjacent_identity"]) > 1e-12:
            raise RuntimeError(f"M3 adjacent identity failed fold {f}")
        err = float(cur["max_abs_reported_moment_error"])
        if not math.isfinite(err) or err > cgen.FIT_TOL:
            raise RuntimeError(f"M3 refit exceeds frozen tolerance fold {f}: {err}")
        maxerr = max(maxerr, err)
    return maxerr


def build_exact_case(
    src: Path,
    rep: int,
    authority: Mapping,
    cases: Mapping[int, Mapping],
    c0_sha: str,
) -> tuple[dict, np.ndarray, dict]:
    if a0gen.e.git_blob_sha1(src.read_bytes()) != a0gen.EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob mismatch")
    parser = a0gen.e.SlotParser()
    a0gen.e.validate_parser(parser)
    d = a0gen.b58.build_dataset(src, parser, "min")
    if (
        d["source_blob"] != a0gen.EXPECTED_SOURCE_BLOB
        or d["visible"] != a0gen.EXPECTED_VISIBLE
        or d["parsed"] != a0gen.EXPECTED_PARSED
    ):
        raise RuntimeError("frozen ZL3b population changed")
    fold_counts = [int(np.sum(d["token_folds"] == f)) for f in range(5)]
    if fold_counts != a0gen.EXPECTED_FOLD_PARSED:
        raise RuntimeError(f"frozen fold population changed: {fold_counts}")

    fits = cgen.fit_crossfold(d)
    fit_public = {str(f): cgen.serialize_fit(fits[f]) for f in range(5)}
    refit_max_error = validate_refit(fit_public, authority["fit"])
    X = cgen.generate_case(d, fits, rep)
    got_sha = cgen.occupancy_sha(X)
    frozen = cases[rep]
    if got_sha != frozen["occupancy_sha256"]:
        raise RuntimeError(f"M3 exact occupancy SHA changed rep {rep}: {got_sha}")

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
        "rep": rep,
        "occupancy_sha256": got_sha,
        "phase_c0_authority_sha256": c0_sha,
        "tokens": int(len(X)),
        "fold_tokens": fold_counts,
        "all_zero_count": int(np.sum(X.sum(axis=1) == 0)),
        "training_unary_moments_exact_c0": True,
        "training_adjacent_moments_exact_c0": True,
        "descriptor_distribution_exact_c0": True,
        "fit_tolerance_revalidated": True,
        "regenerated_fit_max_abs_reported_moment_error": refit_max_error,
        "exact_phase_c0_replay": True,
        "frozen_case": frozen,
    }
    return candidate, X, audit


def measurement(candidate: Mapping, X: np.ndarray, rep: int) -> dict:
    reference_ns = f"issue75:phaseC:M3-KRS-CHAIN:rep{rep}:reference"
    test_ns = f"issue75:phaseC:M3-KRS-CHAIN:rep{rep}:test"
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

    authority, cases, c0_sha = load_c0()
    candidate, X, audit = build_exact_case(src, rep, authority, cases, c0_sha)
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
            "schema": "issue75-phaseC-m3-r1-preflight-v1",
            "status": "EXACT_C0_M3_CORPUS_REGENERATED_TARGET_BLIND",
            "scientific_role": "PRETARGET_EXACT_M3_REPLAY_PREFLIGHT",
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
            "schema": "issue75-phaseC-m3-r1-score-v1",
            "status": "PHASE_C_M3_FIRST_REVEAL_CASE_SCORED",
            "scientific_role": "KRS_NEAREST_NEIGHBOR_GRAMMAR_COMPLETE_66_EDGE_MEASUREMENT",
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
    print(
        json.dumps(
            {
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
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
