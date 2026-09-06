#!/usr/bin/env python3
"""Issue #90 / Issue #88 Phase 0 first reveal.

The selector is NOT rerun here. This executable consumes the immutable
score-free Preflight-B JSON authority, reproduces its frozen selected
populations byte-for-byte, and only then exposes S2/H62/R1.

Modes:
  --self-test
  --stage1 ZL3B PREFLIGHT_B.json OUT.json
  --r1 ZL3B PREFLIGHT_B.json REP OUT.json
  --aggregate STAGE1.json R1_DIR OUT.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Dict

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import phase0_preflight as P  # noqa: E402

I = P.I
PHASE = "ISSUE90_PHASE0"
REPS = (0, 1, 2)
PREFLIGHT_SCHEMA = "issue90-phase0-preflight-b-v1"
PREFLIGHT_JSON_SHA256 = "e016e0da642277adc86b257851eba459e946e40015622d127cb13b85afed33d4"
PREFLIGHT_SELECTION_SHA256 = "8eb8c32709cdf65949e328ad9094f772dc512da52e1241232c44ed72ec856206"
PREFLIGHT_FOLD_SHA256 = "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b"
EXPECTED_GENERATION = {
    0: "ee594b3a8b3c3881f0c2aace1c7e5f694d8c6bada8b17ef22e831c2e9b161ee4",
    1: "560ca8529279354850420b92fee177b7980436ced6abfe760b79a4b68342fdea",
    2: "a8971db75d1cedc79c2bed379d3e5393e1b976abd3d338be356a17369efbb002",
}
TIE_EPS = 1e-12


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_preflight(path: Path) -> dict:
    if sha256_file(path) != PREFLIGHT_JSON_SHA256:
        raise RuntimeError("Preflight-B JSON SHA-256 mismatch")
    x = json.loads(path.read_text(encoding="utf-8"))
    if x.get("schema") != PREFLIGHT_SCHEMA:
        raise RuntimeError("Preflight-B schema mismatch")
    if x.get("target_score_calls") != 0:
        raise RuntimeError("Preflight authority is not score-free")
    if x.get("selection_sha256") != PREFLIGHT_SELECTION_SHA256:
        raise RuntimeError("Preflight selection authority mismatch")
    if x.get("fold_identity_sha256") != PREFLIGHT_FOLD_SHA256:
        raise RuntimeError("Preflight fold authority mismatch")
    if not x.get("deterministic_selection") or not x.get("deterministic_generation"):
        raise RuntimeError("Preflight determinism gate failed")
    if not x["outer_heldout_predictive"]["summary"]["predictive_criterion_pass"]:
        raise RuntimeError("Frozen selected family failed the preregistered predictive criterion")
    for rep, expected in EXPECTED_GENERATION.items():
        got = x["score_free_generation"][f"rep{rep}"]["items_sha256"]
        if got != expected:
            raise RuntimeError(f"Preflight generation hash authority mismatch for rep{rep}")
    return x


def runtime_selections(preflight: dict) -> Dict[str, dict]:
    out = {}
    for f, row in preflight["selections"].items():
        sel = dict(row["selected"])
        if sel.get("family") != "DECAY40":
            raise RuntimeError(f"frozen selected family unexpectedly changed: {sel}")
        tau = sel.get("tau")
        sel["tau"] = math.inf if tau == "INF" else float(tau)
        sel["pi"] = float(sel["pi"])
        out[str(f)] = {"selected": sel}
    return out


def load_target_contexts(zl_path: Path):
    p62c = json.loads((ROOT / "experiments" / "phase62" / "phase62c_c0_a1_results.json").read_text(encoding="utf-8"))
    p63a = json.loads((ROOT / "experiments" / "phase63" / "phase63a_training_vocab_results.json").read_text(encoding="utf-8"))
    contexts, _ = I.n64.fold_contexts(zl_path, p62c, p63a)
    return contexts, p63a


def target_ranges(contexts) -> dict:
    s2 = [float(ctx["target_exposed"]["S2"]) for ctx in contexts]
    raw = [float(ctx["target_H62P1"]["abs_excess_sum"]) for ctx in contexts]
    return {
        "S2_by_fold": s2,
        "S2_interval": [float(min(s2)), float(max(s2))],
        "H62_raw_abs_excess_sum_by_fold": raw,
        "H62_raw_interval": [float(min(raw)), float(max(raw))],
    }


def generate_frozen(zl_path: Path, preflight: dict, rep: int):
    if rep not in REPS:
        raise RuntimeError("rep outside frozen set")
    vitems, folds, parsed = I.C.load_corpus(zl_path)
    selections = runtime_selections(preflight)
    items, diagnostics, support = P.generate_selected(vitems, folds, parsed, selections, rep, I.e.SlotParser())
    got = I.generated_items_hash(items)
    expected = EXPECTED_GENERATION[rep]
    if got != expected:
        raise RuntimeError(f"frozen generation hash mismatch rep{rep}: {got} != {expected}")
    return items, diagnostics, support, folds, got


def surface_gates(aggregate: dict, evaluation: dict, contexts, p63a, preflight: dict) -> dict:
    tr = target_ranges(contexts)
    cand_s2 = float(aggregate["S2"])
    cand_raw = float(aggregate["H62P1"]["abs_excess_sum"])
    s2_lo, s2_hi = tr["S2_interval"]
    raw_lo, raw_hi = tr["H62_raw_interval"]
    s2_pass = bool(s2_lo - TIE_EPS <= cand_s2 <= s2_hi + TIE_EPS)
    raw_pass = bool(raw_lo - TIE_EPS <= cand_raw <= raw_hi + TIE_EPS)

    h62 = evaluation["H62P1_summary"]
    a1 = p63a["across_fold"]["A1_R1_H62P1_summary"]
    profile_pass = bool(
        float(h62["mean_D_profile"]) <= float(a1["mean_D_profile"]) + TIE_EPS
        and float(h62["mean_abs_C_short_diff"]) <= float(a1["mean_abs_C_short_diff"]) + TIE_EPS
    )
    predictive = preflight["outer_heldout_predictive"]["summary"]
    predictive_pass = bool(predictive["predictive_criterion_pass"])

    return {
        "predictive": {
            "pass": predictive_pass,
            "X0_mean_bits_per_token": float(predictive["X0_mean_bits_per_token"]),
            "selected_mean_bits_per_token": float(predictive["selected_mean_bits_per_token"]),
            "gain_vs_X0_bits_per_token": float(predictive["selected_mean_gain_vs_X0"]),
            "gain_by_fold": [float(v) for v in predictive["selected_gain_by_fold"]],
            "positive_gain_folds": int(predictive["selected_positive_gain_folds"]),
        },
        "S2": {
            "candidate": cand_s2,
            "target_by_fold": tr["S2_by_fold"],
            "immutable_target_interval": tr["S2_interval"],
            "pass": s2_pass,
        },
        "H62_raw": {
            "candidate_abs_excess_sum": cand_raw,
            "target_by_fold": tr["H62_raw_abs_excess_sum_by_fold"],
            "immutable_target_interval": tr["H62_raw_interval"],
            "pass": raw_pass,
        },
        "H62_profile": {
            "candidate": h62,
            "A1_R1_frozen_comparator": a1,
            "pass": profile_pass,
        },
        "local_surface_without_R1_pass": bool(predictive_pass and s2_pass and raw_pass and profile_pass),
    }


def stage1(zl_path: Path, preflight_path: Path) -> dict:
    preflight = load_preflight(preflight_path)
    contexts, p63a = load_target_contexts(zl_path)
    reps = {}
    generation = {}
    for rep in REPS:
        items, diagnostics, support, _folds, got = generate_frozen(zl_path, preflight, rep)
        metrics = I.n64.output_metrics(items, f"{PHASE}:SELECTED:rep{rep}", contexts)
        reps[f"rep{rep}"] = metrics
        generation[f"rep{rep}"] = {
            "items_sha256": got,
            "score_free_expected_sha256": EXPECTED_GENERATION[rep],
            "hash_match": True,
            "support": support,
            "fold_diagnostics": diagnostics,
        }
    aggregate = I.n64.aggregate_realizations(reps, f"{PHASE}:SELECTED")
    evaluation = I.n64.evaluate_aggregate(aggregate, contexts, p63a, f"{PHASE}:SELECTED")
    gates = surface_gates(aggregate, evaluation, contexts, p63a, preflight)

    s2_rep = [float(reps[f"rep{r}"]["S2"]) for r in REPS]
    raw_rep = [float(reps[f"rep{r}"]["H62P1"]["abs_excess_sum"]) for r in REPS]
    gates["stochastic_diagnostics"] = {
        "S2_by_rep": s2_rep,
        "S2_range": [min(s2_rep), max(s2_rep)],
        "S2_sd": float(np.std(s2_rep, ddof=0)),
        "H62_raw_by_rep": raw_rep,
        "H62_raw_range": [min(raw_rep), max(raw_rep)],
        "H62_raw_sd": float(np.std(raw_rep, ddof=0)),
        "candidate_variation_changes_pass_band": False,
    }

    out = {
        "schema": "issue90-phase0-stage1-v1",
        "phase": PHASE,
        "target_reveal": True,
        "source_blob": I.b.git_blob_sha1(zl_path.read_bytes()),
        "preflight_authority": {
            "json_sha256": PREFLIGHT_JSON_SHA256,
            "selection_sha256": PREFLIGHT_SELECTION_SHA256,
            "fold_identity_sha256": PREFLIGHT_FOLD_SHA256,
            "run_id": 34016904359,
            "artifact_id": 9984254233,
            "artifact_digest": "sha256:a326b27fd5ed4c6caed371970c14ef347770f6a2732b818ca7ffee831b94c4a5",
        },
        "frozen_selections": {f: row["selected"] for f, row in preflight["selections"].items()},
        "frozen_predictive": preflight["outer_heldout_predictive"],
        "realizations": reps,
        "generation": generation,
        "aggregate": aggregate,
        "frozen_phase64_evaluation": evaluation,
        "phase0_gates": gates,
        "descriptive_only": {
            "S1": aggregate.get("S1_by_fold"),
            "S3": aggregate.get("S3"),
        },
        "interpretation_boundary": {
            "plaintext_recovered": False,
            "semantic_content_tested": False,
            "historical_generator_identified": False,
            "decipherment_established": False,
        },
    }
    return out


def r1(zl_path: Path, preflight_path: Path, rep: int) -> dict:
    preflight = load_preflight(preflight_path)
    items, _diagnostics, _support, folds, got = generate_frozen(zl_path, preflight, rep)
    old_phase = I.PHASE
    try:
        I.PHASE = PHASE
        out = I.score_r1(items, "SELECTED", rep, folds)
    finally:
        I.PHASE = old_phase
    out["status"] = "OK"
    out["generated_items_sha256"] = got
    out["preflight_expected_sha256"] = EXPECTED_GENERATION[rep]
    out["preflight_json_sha256"] = PREFLIGHT_JSON_SHA256
    return out


def aggregate_final(stage1_path: Path, r1_dir: Path) -> dict:
    s1 = json.loads(stage1_path.read_text(encoding="utf-8"))
    if s1.get("schema") != "issue90-phase0-stage1-v1":
        raise RuntimeError("stage1 authority mismatch")
    r1s = {}
    for rep in REPS:
        p = r1_dir / f"selected_rep{rep}.json"
        x = json.loads(p.read_text(encoding="utf-8"))
        if x.get("status") != "OK" or int(x.get("rep", -1)) != rep:
            raise RuntimeError(f"R1 authority mismatch rep{rep}")
        if x.get("generated_items_sha256") != EXPECTED_GENERATION[rep]:
            raise RuntimeError(f"R1 generation mismatch rep{rep}")
        r1s[f"rep{rep}"] = x
    r1_all = bool(all(x["R1_pass"] for x in r1s.values()))
    g = s1["phase0_gates"]
    all_pass = bool(g["local_surface_without_R1_pass"] and r1_all)
    if all_pass:
        classification = "LOCAL-CLOSURE SUFFICIENT"
    elif g["predictive"]["pass"]:
        classification = "PREDICTIVE BUT SURFACE-INCOMPLETE"
    else:
        classification = "NO STABLE PREDICTIVE GAIN"
    return {
        "schema": "issue90-phase0-final-v1",
        "phase": PHASE,
        "classification": classification,
        "preflight_authority": s1["preflight_authority"],
        "frozen_selections": s1["frozen_selections"],
        "phase0_gates": g,
        "R1": {
            "all_three_pass": r1_all,
            "by_rep": {k: bool(v["R1_pass"]) for k, v in r1s.items()},
            "details": r1s,
        },
        "all_responsibilities_pass": all_pass,
        "next_program_step": "Issue #88 Phase 1 predictive-information budget regardless of Phase-0 classification",
        "interpretation_boundary": s1["interpretation_boundary"],
    }


def self_test():
    # First reveal must be bound to exactly three immutable generation hashes.
    assert tuple(sorted(EXPECTED_GENERATION)) == REPS
    assert len(set(EXPECTED_GENERATION.values())) == 3
    assert len(PREFLIGHT_JSON_SHA256) == 64
    return {"ok": True, "target_scoring_enabled": True, "selector_rerun": False}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--stage1", nargs=3, metavar=("ZL3B", "PREFLIGHT", "OUT"))
    ap.add_argument("--r1", nargs=4, metavar=("ZL3B", "PREFLIGHT", "REP", "OUT"))
    ap.add_argument("--aggregate", nargs=3, metavar=("STAGE1", "R1_DIR", "OUT"))
    ns = ap.parse_args(argv)
    modes = sum([bool(ns.self_test), ns.stage1 is not None, ns.r1 is not None, ns.aggregate is not None])
    if modes != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    if ns.stage1:
        x = stage1(Path(ns.stage1[0]), Path(ns.stage1[1]))
        Path(ns.stage1[2]).write_text(json.dumps(x, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({
            "surface_gates": x["phase0_gates"],
            "generation_hashes": {r:v["items_sha256"] for r,v in x["generation"].items()},
        }, indent=2, sort_keys=True))
        return 0
    if ns.r1:
        rep = int(ns.r1[2])
        x = r1(Path(ns.r1[0]), Path(ns.r1[1]), rep)
        Path(ns.r1[3]).write_text(json.dumps(x, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"rep": rep, "R1_pass": x["R1_pass"], "parser": x["parser"]}, indent=2, sort_keys=True))
        return 0
    x = aggregate_final(Path(ns.aggregate[0]), Path(ns.aggregate[1]))
    Path(ns.aggregate[2]).write_text(json.dumps(x, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": x["classification"],
        "all_responsibilities_pass": x["all_responsibilities_pass"],
        "R1_all_three_pass": x["R1"]["all_three_pass"],
        "phase0_gates": x["phase0_gates"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
