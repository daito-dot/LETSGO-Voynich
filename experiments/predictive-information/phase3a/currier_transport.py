#!/usr/bin/env python3
"""Issue #104 / #88 Phase 3A Currier A/B mechanism transport.

Primary arm transfers only LOCAL40 and previous-paragraph mixture strengths across
Currier strata while fitting V2 emission and edit-1 support on target training
leaves. A strict source-support arm is diagnostic only.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Dict, Sequence

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PRED = ROOT / "experiments" / "predictive-information"
P2B_PATH = PRED / "phase2b" / "phase2b_boundary_localization.py"
GATE0_PATH = HERE.parent / "currier_gate0_audit.py"
PLAN_PATH = HERE.parent / "TRANSPORT_PLAN.md"
GATE_PROVENANCE_PATH = HERE.parent / "GATE0_PROVENANCE.md"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_GATE0_JSON_SHA256 = "e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e"
N_FOLDS = 5
GRID = np.asarray([round(i / 100.0, 2) for i in range(31)], dtype=float)
TIE_EPS = 1e-12
LN2 = math.log(2.0)
LABELS = ("A", "B")
DIRECTIONS = (("A", "B"), ("B", "A"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P2B = load_module("issue104_phase2b_authority", P2B_PATH)
G0 = load_module("issue104_currier_gate0_authority", GATE0_PATH)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_sha256(x: dict) -> str:
    b = (json.dumps(x, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    return hashlib.sha256(b).hexdigest()


def install_order(zl_path: Path):
    cfg = OA.configure(zl_path)
    P2B.I.ordered = OA.ordered
    P2B.A.I.ordered = OA.ordered
    P2B.B.I.ordered = OA.ordered
    P2B.P1.I.ordered = OA.ordered
    return cfg


def choose(ll: np.ndarray) -> int:
    best = 0
    for i in range(1, len(GRID)):
        if ll[i] > ll[best] + TIE_EPS:
            best = i
        elif abs(float(ll[i] - ll[best])) <= TIE_EPS and float(GRID[i]) < float(GRID[best]):
            best = i
    return int(best)


def bits(probs: np.ndarray) -> float:
    if len(probs) == 0 or np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
        raise RuntimeError("invalid probability vector")
    return float(-np.log(probs).mean() / LN2)


def label_items(items, by_doc: dict):
    out = {lab: [] for lab in LABELS}
    unknown = []
    for it in items:
        rec = by_doc.get(it.document)
        if rec is None:
            raise RuntimeError(f"parsed document absent from Currier authority: {it.document}")
        lab = rec["label"]
        if lab in LABELS:
            out[lab].append(it)
        else:
            unknown.append(it)
    return out, unknown


def fit_subset(items, folds, parsed, excluded_folds: Sequence[int]):
    return P2B.B.fit_training(items, folds, parsed, excluded_folds)


def validation_features(items, folds, parsed, parser, train_excluded: Sequence[int], validation_fold: int):
    _tr, v2, index = fit_subset(items, folds, parsed, train_excluded)
    va = P2B.I.b.by_leaves(items, folds[validation_fold], include=True)
    if not va:
        raise RuntimeError(f"empty validation item population fold {validation_fold}")
    feat = P2B.boundary_features(va, parsed, v2, index, parser)
    if feat["n_scored"] <= 0:
        raise RuntimeError(f"empty validation token population fold {validation_fold}")
    return feat


def local_curve(feat: dict):
    return P2B.scalar_curve(feat["p0"], feat["q_local"], feat["av_local"])


def prev_curve(feat: dict, pi: float):
    plocal = P2B.local_probs(feat, pi)
    return P2B.scalar_curve(plocal, feat["q_bag"]["PREV_PARAS"], feat["avail"]["PREV_PARAS"])


def select_source_params(items, folds, parsed, parser, label: str):
    """One source-stratum pi/alpha chosen without any opposite-stratum token."""
    ll_pi = np.zeros(len(GRID), dtype=float)
    fold_diag = []
    for f in range(N_FOLDS):
        feat = validation_features(items, folds, parsed, parser, (f,), f)
        ll_pi += local_curve(feat)
        fold_diag.append({
            "fold": int(f),
            "n_scored": int(feat["n_scored"]),
            "n_visible": int(feat["n_visible"]),
            "local_context_available": int(np.sum(feat["av_local"])),
            "prev_context_available": int(np.sum(feat["avail"]["PREV_PARAS"])),
        })
    pi_i = choose(ll_pi)
    pi = float(GRID[pi_i])

    ll_alpha = np.zeros(len(GRID), dtype=float)
    for f in range(N_FOLDS):
        feat = validation_features(items, folds, parsed, parser, (f,), f)
        ll_alpha += prev_curve(feat, pi)
    a_i = choose(ll_alpha)
    alpha = float(GRID[a_i])
    return {
        "label": label,
        "pi_LOCAL": pi,
        "alpha_ALL_PREV": alpha,
        "local_cv_total_log_likelihood": float(ll_pi[pi_i]),
        "prev_cv_total_log_likelihood": float(ll_alpha[a_i]),
        "local_curve": [
            {"pi": float(x), "total_log_likelihood": float(ll_pi[i])}
            for i, x in enumerate(GRID)
        ],
        "prev_curve": [
            {"alpha": float(x), "total_log_likelihood": float(ll_alpha[i])}
            for i, x in enumerate(GRID)
        ],
        "fold_diagnostics": fold_diag,
    }


def select_target_oracle(items, folds, parsed, parser, outer_f: int, label: str):
    """Nested target-only oracle; target outer fold never enters selection."""
    ll_pi = np.zeros(len(GRID), dtype=float)
    inner_diag = []
    for g in range(N_FOLDS):
        if g == outer_f:
            continue
        feat = validation_features(items, folds, parsed, parser, (outer_f, g), g)
        ll_pi += local_curve(feat)
        inner_diag.append({
            "inner_fold": int(g),
            "n_scored": int(feat["n_scored"]),
            "n_visible": int(feat["n_visible"]),
        })
    pi_i = choose(ll_pi)
    pi = float(GRID[pi_i])

    ll_alpha = np.zeros(len(GRID), dtype=float)
    for g in range(N_FOLDS):
        if g == outer_f:
            continue
        feat = validation_features(items, folds, parsed, parser, (outer_f, g), g)
        ll_alpha += prev_curve(feat, pi)
    a_i = choose(ll_alpha)
    alpha = float(GRID[a_i])
    return {
        "target_label": label,
        "outer_fold": int(outer_f),
        "pi_LOCAL": pi,
        "alpha_ALL_PREV": alpha,
        "local_total_log_likelihood": float(ll_pi[pi_i]),
        "prev_total_log_likelihood": float(ll_alpha[a_i]),
        "inner": inner_diag,
    }


def score_mechanism_target(target_items, folds, parsed, parser, outer_f: int, source_params: dict, oracle: dict):
    _tr, v2, index = fit_subset(target_items, folds, parsed, (outer_f,))
    test = P2B.I.b.by_leaves(target_items, folds[outer_f], include=True)
    if not test:
        raise RuntimeError(f"empty target test items fold {outer_f}")
    feat = P2B.boundary_features(test, parsed, v2, index, parser)
    if feat["n_scored"] <= 0:
        raise RuntimeError(f"empty target scored population fold {outer_f}")

    p_v2 = feat["p0"]
    pi_s = float(source_params["pi_LOCAL"])
    a_s = float(source_params["alpha_ALL_PREV"])
    p_local_s = P2B.local_probs(feat, pi_s)
    p_core_s = P2B.mix(p_local_s, feat["q_bag"]["PREV_PARAS"], feat["avail"]["PREV_PARAS"], a_s)

    pi_o = float(oracle["pi_LOCAL"])
    a_o = float(oracle["alpha_ALL_PREV"])
    p_local_o = P2B.local_probs(feat, pi_o)
    p_core_o = P2B.mix(p_local_o, feat["q_bag"]["PREV_PARAS"], feat["avail"]["PREV_PARAS"], a_o)

    b_v2 = bits(p_v2)
    b_local_s = bits(p_local_s)
    b_core_s = bits(p_core_s)
    b_local_o = bits(p_local_o)
    b_core_o = bits(p_core_o)
    return {
        "fold": int(outer_f),
        "n_scored": int(feat["n_scored"]),
        "n_visible": int(feat["n_visible"]),
        "target_training_vocab_types": int(len(index.vocab)),
        "availability": {
            "LOCAL40_fraction": float(np.mean(feat["av_local"])),
            "PREV_PARAS_fraction": float(np.mean(feat["avail"]["PREV_PARAS"])),
        },
        "bits_per_token": {
            "T_V2": b_v2,
            "T_LOCAL_source_pi": b_local_s,
            "T_CORE_source_params": b_core_s,
            "T_LOCAL_target_oracle": b_local_o,
            "T_CORE_target_oracle": b_core_o,
        },
        "gains": {
            "G_local_transfer": float(b_v2 - b_local_s),
            "G_prev_transfer": float(b_local_s - b_core_s),
            "G_core_transfer": float(b_v2 - b_core_s),
            "penalty_local": float(b_local_s - b_local_o),
            "penalty_core": float(b_core_s - b_core_o),
        },
        "oracle": {"pi_LOCAL": pi_o, "alpha_ALL_PREV": a_o},
    }


def token_oov_fraction(test_items, parsed, index):
    n = 0
    oov = 0
    for it in test_items:
        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                if parsed[it.item_id][li][ti] is None:
                    continue
                n += 1
                if tok not in index.vocab:
                    oov += 1
    return {
        "n_scored_tokens": int(n),
        "exact_token_oov": int(oov),
        "exact_token_oov_fraction": float(oov / n) if n else None,
    }


def full_support_direction(source_items, target_items, folds, parsed, parser, source_params: dict, mechanism_rows: list):
    """Strict source-trained emission/support diagnostic. Never affects primary classification."""
    _tr, source_v2, source_index = fit_subset(source_items, folds, parsed, ())
    out = []
    mechanism_by_fold = {int(r["fold"]): r for r in mechanism_rows}
    for f in range(N_FOLDS):
        test = P2B.I.b.by_leaves(target_items, folds[f], include=True)
        diag = token_oov_fraction(test, parsed, source_index)
        rec = {"fold": int(f), **diag}
        try:
            feat = P2B.boundary_features(test, parsed, source_v2, source_index, parser)
            p_v2 = feat["p0"]
            p_local = P2B.local_probs(feat, float(source_params["pi_LOCAL"]))
            p_core = P2B.mix(
                p_local,
                feat["q_bag"]["PREV_PARAS"],
                feat["avail"]["PREV_PARAS"],
                float(source_params["alpha_ALL_PREV"]),
            )
            b_v2 = bits(p_v2)
            b_core = bits(p_core)
            mechanism_core = float(mechanism_by_fold[f]["bits_per_token"]["T_CORE_source_params"])
            rec.update({
                "valid": True,
                "source_support_V2_bits_per_token": b_v2,
                "source_support_CORE_bits_per_token": b_core,
                "mechanism_only_target_support_CORE_bits_per_token": mechanism_core,
                "source_support_CORE_minus_mechanism_CORE": float(b_core - mechanism_core),
                "LOCAL40_context_available_fraction": float(np.mean(feat["av_local"])),
                "PREV_PARAS_context_available_fraction": float(np.mean(feat["avail"]["PREV_PARAS"])),
            })
        except Exception as e:  # diagnostic arm is explicitly allowed to be inconclusive
            rec.update({"valid": False, "error": f"{type(e).__name__}: {e}"})
        out.append(rec)
    return {
        "classification": "VALID" if all(r["valid"] for r in out) else "FULL-SUPPORT INCONCLUSIVE",
        "folds": out,
    }


def stability(vals):
    vals = [float(x) for x in vals]
    mean = float(np.mean(vals))
    pos = int(sum(x > 0.0 for x in vals))
    return {
        "values": vals,
        "mean": mean,
        "positive_folds": pos,
        "pass": bool(mean > 0.0 and pos >= 4),
    }


def component_classification(ab: dict, ba: dict):
    if len(ab.get("values", [])) != N_FOLDS or len(ba.get("values", [])) != N_FOLDS:
        return "SUPPORT / FOLD INVALID"
    if ab["pass"] and ba["pass"]:
        return "BIDIRECTIONAL TRANSPORT"
    if ab["pass"] and not ba["pass"]:
        return "A->B ONLY"
    if ba["pass"] and not ab["pass"]:
        return "B->A ONLY"
    return "NO BIDIRECTIONAL TRANSPORT"


def summarize_direction(rows: list):
    keys = ("G_local_transfer", "G_prev_transfer", "G_core_transfer", "penalty_local", "penalty_core")
    return {k: stability([r["gains"][k] for r in rows]) for k in keys}


def run(zl_path: Path):
    if G0.source_blob_sha1(zl_path) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b source differs from frozen authority")

    # Recompute the score-free gate and require byte-equivalent JSON authority.
    gate = G0.audit(zl_path)
    gate_sha = json_sha256(gate)
    if gate_sha != EXPECTED_GATE0_JSON_SHA256:
        raise RuntimeError(f"Gate-0 authority drift: {gate_sha} != {EXPECTED_GATE0_JSON_SHA256}")
    if not gate["gate_pass"]:
        raise RuntimeError("Gate 0 no longer passes")

    order_cfg = install_order(zl_path)
    items, folds, parsed = P2B.I.C.load_corpus(zl_path)
    if len(folds) != N_FOLDS:
        raise RuntimeError("frozen fold count changed")
    order_verify = OA.verify(items)
    parser = P2B.I.e.SlotParser()
    P2B.I.e.validate_parser(parser)

    headers = G0.parse_source_headers(zl_path)
    by_doc = {r["document"]: r for r in headers}
    strata, unknown = label_items(items, by_doc)
    if not all(strata[lab] for lab in LABELS):
        raise RuntimeError("empty A/B stratum")

    source_params = {
        lab: select_source_params(strata[lab], folds, parsed, parser, lab)
        for lab in LABELS
    }

    target_oracles = {lab: {} for lab in LABELS}
    for lab in LABELS:
        for f in range(N_FOLDS):
            target_oracles[lab][str(f)] = select_target_oracle(strata[lab], folds, parsed, parser, f, lab)

    directions = {}
    for source, target in DIRECTIONS:
        key = f"{source}_to_{target}"
        rows = []
        for f in range(N_FOLDS):
            rows.append(score_mechanism_target(
                strata[target], folds, parsed, parser, f,
                source_params[source], target_oracles[target][str(f)],
            ))
        directions[key] = {
            "source": source,
            "target": target,
            "source_params": {
                "pi_LOCAL": source_params[source]["pi_LOCAL"],
                "alpha_ALL_PREV": source_params[source]["alpha_ALL_PREV"],
            },
            "outer": rows,
            "summary": summarize_direction(rows),
        }
        directions[key]["full_support_diagnostic"] = full_support_direction(
            strata[source], strata[target], folds, parsed, parser, source_params[source], rows
        )

    ab = directions["A_to_B"]["summary"]
    ba = directions["B_to_A"]["summary"]
    classifications = {
        "LOCAL40": component_classification(ab["G_local_transfer"], ba["G_local_transfer"]),
        "PREV_PARAS": component_classification(ab["G_prev_transfer"], ba["G_prev_transfer"]),
        "CORE": component_classification(ab["G_core_transfer"], ba["G_core_transfer"]),
    }

    return P2B.B.strict_safe({
        "schema": "issue104-phase3a-currier-transport-v1",
        "phase": "ISSUE104_PHASE3A_CURRIER_TRANSPORT",
        "classification": classifications,
        "source_parameters": source_params,
        "target_oracles": target_oracles,
        "directions": directions,
        "population": {
            "A_items": len(strata["A"]),
            "B_items": len(strata["B"]),
            "unknown_excluded_items": len(unknown),
            "mixed_AB_leaves": gate["mixed_AB_leaves_excluded"],
            "fold_support": gate["eligible_by_label_and_frozen_fold"],
        },
        "authority": {
            "gate0_json_sha256": gate_sha,
            "expected_gate0_json_sha256": EXPECTED_GATE0_JSON_SHA256,
            "order": {**order_cfg, **order_verify},
            "fold_identity_sha256": P2B.P1.P0.fold_hash(folds),
            "files": {
                "GATE0_PROVENANCE.md": sha256_file(GATE_PROVENANCE_PATH),
                "TRANSPORT_PLAN.md": sha256_file(PLAN_PATH),
                "currier_transport.py": sha256_file(HERE),
            },
        },
        "firewall": {
            "prediction_only": True,
            "target_support_used_for_primary_emission_and_edit_index": True,
            "source_target_tokens_used_for_source_parameter_selection": False,
            "H_tau_window_reselected": False,
            "edit_relation_changed": False,
            "history_pool_changed": False,
            "surface_target_metrics_scored": False,
            "issue84_target_used": False,
            "hand_section_scribe_used": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
            "future_test_tokens_used": False,
        },
    })


def self_test():
    # Selection and classification rules only; real corpus access happens in --run.
    ll = np.zeros(len(GRID), dtype=float)
    ll[5] = 1.0
    assert choose(ll) == 5
    tie = np.zeros(len(GRID), dtype=float)
    assert choose(tie) == 0
    p = component_classification(
        {"pass": True, "values": [1, 1, 1, 1, -1]},
        {"pass": True, "values": [1, 1, 1, 1, 1]},
    )
    assert p == "BIDIRECTIONAL TRANSPORT"
    return {
        "ok": True,
        "frozen_grid": [float(x) for x in GRID],
        "tie_prefers_smaller": True,
        "classification_rule": True,
        "surface_target_calls": 0,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.run is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    out = run(Path(ns.run[0]))
    Path(ns.run[1]).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    compact = {
        "classification": out["classification"],
        "source_parameters": {
            lab: {
                "pi_LOCAL": out["source_parameters"][lab]["pi_LOCAL"],
                "alpha_ALL_PREV": out["source_parameters"][lab]["alpha_ALL_PREV"],
            } for lab in LABELS
        },
        "directions": {
            k: {
                "summary": v["summary"],
                "oracles": [r["oracle"] for r in v["outer"]],
                "full_support_classification": v["full_support_diagnostic"]["classification"],
            } for k, v in out["directions"].items()
        },
        "authority": out["authority"],
    }
    print(json.dumps(compact, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
