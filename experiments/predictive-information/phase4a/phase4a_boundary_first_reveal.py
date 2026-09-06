#!/usr/bin/env python3
"""Issue #112 / Issue #88 Phase 4A P1/P2 first reveal.

The merged score-free Gate0 representation is regenerated and identity-checked
before any model is fitted. Only then is the frozen second-order raw-EVA atom
model trained and scored on the five held-out physical-leaf folds.

Modes:
  --self-test
  --run ZL3B OUT.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

HERE = Path(__file__).resolve()
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import phase4a_boundary_gate0 as G  # noqa: E402

SCHEMA = "issue112-phase4a-first-reveal-v1"
N_FOLDS = 5
ALPHA = 0.5
BOS = "<BOS>"
OOV = "<OOV>"
LN2 = math.log(2.0)

EXPECTED_FOLD_HASH = "cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b"
EXPECTED_REAL_HASH = "45d456d106c96f3085774bfe3f2b8a4ed1c1a1bc70ae135215ea590d0039752c"
EXPECTED_MID_HASH = "2e05e74a35d31391da976bb7a447694210a26e390397ecb738982cac4134b7af"
EXPECTED_P2_HASH = "ccd7efe6ce35b74fb41e227893d2bd972c2c4db60f9ae2c3830b38da6c45209b"
EXPECTED_COUNTS = {"real_space": 21363, "mid_token": 21313, "p2_real_space": 18696}


def mean(xs: Sequence[float]) -> float:
    if not xs:
        raise RuntimeError("mean of empty sequence")
    return float(sum(xs) / len(xs))


def clean_event_authority(zl_path: Path) -> dict:
    """Regenerate Gate0 token/events, preserving Gate0 event identity order."""
    data = zl_path.read_bytes()
    if G.git_blob_sha1(data) != G.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b Git blob mismatch before event extraction")
    lines = data.decode("utf-8").splitlines()
    leaf_fold, fold_identity = G.frozen_fold_authority(zl_path)
    currier = G.page_currier_authority(lines)

    tokens = []
    real = []
    mid = []
    p2 = []
    real_ids = []
    mid_ids = []
    p2_ids = []

    for source_line_no, line in enumerate(lines, start=1):
        m = G.LOCUS_RE.match(line)
        if not m or "P" not in m.group("code"):
            continue
        loc = m.group("loc")
        page = loc.split(".", 1)[0]
        lm = G.LEAF_RE.match(page)
        if not lm:
            continue
        leaf = int(lm.group(1))
        if leaf not in leaf_fold:
            continue
        fold = int(leaf_fold[leaf])
        c = currier.get(page, "UNKNOWN")
        if c not in ("A", "B"):
            c = "UNKNOWN"

        segments, n_dot = G.split_certain_spaces(m.group("body"))
        atoms_by_segment: List[Optional[Tuple[str, ...]]] = []
        for si, raw in enumerate(segments):
            atoms = G.atomize_clean(raw)
            atoms_by_segment.append(atoms)
            if atoms is None:
                continue
            tokens.append({
                "id": (loc, source_line_no, si),
                "fold": fold,
                "currier": c,
                "atoms": atoms,
            })
            if len(atoms) >= 4:
                cut = len(atoms) // 2
                if cut < 2 or len(atoms) - cut < 2:
                    raise RuntimeError("MID cut invariant failed")
                eid = (loc, source_line_no, si, len(atoms), cut, fold)
                ev = {
                    "id": eid,
                    "fold": fold,
                    "currier": c,
                    "atoms": atoms,
                    "cut": cut,
                }
                mid.append(ev)
                mid_ids.append(eid)

        if n_dot != len(segments) - 1:
            raise RuntimeError(f"dot/segment mismatch at {loc}")
        for bi in range(n_dot):
            left = atoms_by_segment[bi]
            right = atoms_by_segment[bi + 1]
            if left is None or right is None or len(left) < 2 or len(right) < 2:
                continue
            eid = (loc, source_line_no, bi, len(left), len(right), fold)
            ev = {
                "id": eid,
                "fold": fold,
                "currier": c,
                "left": left,
                "right": right,
            }
            real.append(ev)
            real_ids.append(eid)
            if len(left) >= 3 and len(right) >= 3:
                p2.append(ev)
                p2_ids.append(eid)

    return {
        "fold_identity": fold_identity,
        "tokens": tokens,
        "real": real,
        "mid": mid,
        "p2": p2,
        "hashes": {
            "fold_identity_sha256": G.sha256_obj(fold_identity),
            "real_space_sha256": G.sha256_obj(real_ids),
            "mid_token_sha256": G.sha256_obj(mid_ids),
            "p2_real_space_sha256": G.sha256_obj(p2_ids),
        },
    }


def verify_authority(zl_path: Path, auth: dict) -> dict:
    """Run the merged Gate0 audit and require exact frozen identities."""
    gate = G.audit(zl_path)
    expected = {
        "fold_identity_sha256": EXPECTED_FOLD_HASH,
        "real_space_sha256": EXPECTED_REAL_HASH,
        "mid_token_sha256": EXPECTED_MID_HASH,
        "p2_real_space_sha256": EXPECTED_P2_HASH,
    }
    got = auth["hashes"]
    if got != expected:
        raise RuntimeError(f"Phase4A event authority mismatch: {got} != {expected}")
    if gate["fold_authority"]["identity_sha256"] != EXPECTED_FOLD_HASH:
        raise RuntimeError("merged Gate0 fold identity mismatch")
    if gate["population"]["event_id_hashes"]["real_space_sha256"] != EXPECTED_REAL_HASH:
        raise RuntimeError("merged Gate0 REAL_SPACE identity mismatch")
    if gate["population"]["event_id_hashes"]["mid_token_sha256"] != EXPECTED_MID_HASH:
        raise RuntimeError("merged Gate0 MID_TOKEN identity mismatch")
    if gate["population"]["event_id_hashes"]["p2_real_space_sha256"] != EXPECTED_P2_HASH:
        raise RuntimeError("merged Gate0 P2 identity mismatch")
    counts = {
        "real_space": len(auth["real"]),
        "mid_token": len(auth["mid"]),
        "p2_real_space": len(auth["p2"]),
    }
    if counts != EXPECTED_COUNTS or gate["population"]["real_space"] != EXPECTED_COUNTS["real_space"] or gate["population"]["mid_token"] != EXPECTED_COUNTS["mid_token"] or gate["population"]["p2_real_space"] != EXPECTED_COUNTS["p2_real_space"]:
        raise RuntimeError(f"Phase4A frozen event count mismatch: {counts}")
    if gate["gate_pass"] is not True:
        raise RuntimeError("merged Gate0 no longer passes")
    if gate["firewall"]["predictive_scores_computed"] is not False or gate["firewall"]["boundary_model_fitted"] is not False:
        raise RuntimeError("Gate0 firewall authority corrupted")
    return {
        "status": "PASS",
        "source_git_blob_sha1": gate["source"]["git_blob_sha1"],
        "source_sha256": gate["source"]["sha256"],
        "fold_identity_sha256": EXPECTED_FOLD_HASH,
        "event_hashes": {
            "real_space_sha256": EXPECTED_REAL_HASH,
            "mid_token_sha256": EXPECTED_MID_HASH,
            "p2_real_space_sha256": EXPECTED_P2_HASH,
        },
        "counts": counts,
    }


class AtomV2:
    """Frozen second-order atom model with additive alpha=0.5 and one OOV."""

    def __init__(self, sequences: Sequence[Sequence[str]]):
        if not sequences:
            raise RuntimeError("empty atom-model training population")
        atom_types = sorted({x for seq in sequences for x in seq})
        if not atom_types:
            raise RuntimeError("empty atom alphabet")
        self.alphabet = tuple(atom_types)
        self.alphabet_set = set(atom_types)
        self.targets = self.alphabet + (OOV,)
        self.v = len(self.targets)
        self.counts = Counter()
        self.context_totals = Counter()
        self.n_training_tokens = len(sequences)
        self.n_training_atoms = 0
        for seq in sequences:
            p2, p1 = BOS, BOS
            for raw_x in seq:
                x = raw_x
                self.counts[(p2, p1, x)] += 1
                self.context_totals[(p2, p1)] += 1
                self.n_training_atoms += 1
                p2, p1 = p1, x
        self.observed_contexts = len(self.context_totals)

    def map_atom(self, x: str) -> str:
        return x if x in self.alphabet_set else OOV

    def prob(self, x: str, p2: str, p1: str) -> float:
        xx = self.map_atom(x)
        c2 = p2 if p2 == BOS else self.map_atom(p2)
        c1 = p1 if p1 == BOS else self.map_atom(p1)
        denom = float(self.context_totals[(c2, c1)] + ALPHA * self.v)
        num = float(self.counts[(c2, c1, xx)] + ALPHA)
        p = num / denom
        if not (0.0 < p <= 1.0) or not math.isfinite(p):
            raise RuntimeError("invalid smoothed atom probability")
        return p

    def bits(self, x: str, p2: str, p1: str) -> float:
        return -math.log(self.prob(x, p2, p1)) / LN2

    def code_segment(self, seq: Sequence[str]) -> float:
        if not seq:
            raise RuntimeError("cannot code empty segment")
        total = 0.0
        p2, p1 = BOS, BOS
        for x in seq:
            total += self.bits(x, p2, p1)
            p2, p1 = p1, x
        return float(total)

    def distribution_sum(self, p2: str, p1: str) -> float:
        total = 0.0
        for x in self.targets:
            c2 = p2 if p2 == BOS else self.map_atom(p2)
            c1 = p1 if p1 == BOS else self.map_atom(p1)
            denom = float(self.context_totals[(c2, c1)] + ALPHA * self.v)
            total += float(self.counts[(c2, c1, x)] + ALPHA) / denom
        return total


def score_p1(model: AtomV2, left: Sequence[str], right: Sequence[str]) -> dict:
    if len(left) < 2 or len(right) < 2:
        raise RuntimeError("P1 event lacks two atoms per side")
    r0, r1 = right[0], right[1]
    reset = model.bits(r0, BOS, BOS) + model.bits(r1, BOS, r0)
    carry = model.bits(r0, left[-2], left[-1]) + model.bits(r1, left[-1], r0)
    used = (left[-2], left[-1], r0, r1)
    return {
        "reset_bits": float(reset),
        "carry_bits": float(carry),
        "advantage": float(carry - reset),
        "target_oov_atoms": int((r0 not in model.alphabet_set) + (r1 not in model.alphabet_set)),
        "any_used_atom_oov": bool(any(x not in model.alphabet_set for x in used)),
    }


def score_p2(model: AtomV2, left: Sequence[str], right: Sequence[str]) -> dict:
    if len(left) < 3 or len(right) < 3:
        raise RuntimeError("P2 event lacks frozen >=3 atom support")
    observed = model.code_segment(left) + model.code_segment(right)
    shift_left = model.code_segment(left[:-1]) + model.code_segment(tuple(left[-1:]) + tuple(right))
    shift_right = model.code_segment(tuple(left) + tuple(right[:1])) + model.code_segment(right[1:])
    all_atoms = tuple(left) + tuple(right)
    return {
        "observed_bits": float(observed),
        "shift_left_bits": float(shift_left),
        "shift_right_bits": float(shift_right),
        "observed_minus_shift_left": float(observed - shift_left),
        "observed_minus_shift_right": float(observed - shift_right),
        "oov_atoms": int(sum(x not in model.alphabet_set for x in all_atoms)),
        "n_atoms": len(all_atoms),
        "any_atom_oov": bool(any(x not in model.alphabet_set for x in all_atoms)),
    }


def summarize_by_currier(currier_rows: dict) -> dict:
    out = {}
    for c in ("A", "B", "UNKNOWN"):
        row = currier_rows[c]
        rr = row["real_a"]
        mm = row["mid_a"]
        pl = row["p2_left"]
        pr = row["p2_right"]
        out[c] = {
            "n_real": len(rr),
            "n_mid": len(mm),
            "n_p2": len(pl),
            "mean_A_real": mean(rr) if rr else None,
            "mean_A_mid": mean(mm) if mm else None,
            "D_RESET": (mean(rr) - mean(mm)) if rr and mm else None,
            "mean_observed_minus_shift_left": mean(pl) if pl else None,
            "mean_observed_minus_shift_right": mean(pr) if pr else None,
        }
    return out


def score_fold(f: int, auth: dict) -> Tuple[dict, dict]:
    train_sequences = [t["atoms"] for t in auth["tokens"] if int(t["fold"]) != f]
    model = AtomV2(train_sequences)
    real_events = [x for x in auth["real"] if int(x["fold"]) == f]
    mid_events = [x for x in auth["mid"] if int(x["fold"]) == f]
    p2_events = [x for x in auth["p2"] if int(x["fold"]) == f]
    if not real_events or not mid_events or not p2_events:
        raise RuntimeError(f"fold {f}: frozen event support disappeared")

    real_a: List[float] = []
    mid_a: List[float] = []
    p2_left: List[float] = []
    p2_right: List[float] = []
    currier_rows = {
        c: {"real_a": [], "mid_a": [], "p2_left": [], "p2_right": []}
        for c in ("A", "B", "UNKNOWN")
    }
    length_real = defaultdict(list)
    length_mid = defaultdict(list)

    p1_real_target_oov = 0
    p1_mid_target_oov = 0
    p1_real_any_oov = 0
    p1_mid_any_oov = 0
    p2_oov_atoms = 0
    p2_atoms = 0
    p2_any_oov = 0

    for ev in real_events:
        s = score_p1(model, ev["left"], ev["right"])
        a = float(s["advantage"])
        real_a.append(a)
        c = ev["currier"]
        currier_rows[c]["real_a"].append(a)
        length_real[len(ev["right"])].append(a)
        p1_real_target_oov += int(s["target_oov_atoms"])
        p1_real_any_oov += int(s["any_used_atom_oov"])

    for ev in mid_events:
        left = ev["atoms"][:ev["cut"]]
        right = ev["atoms"][ev["cut"]:]
        s = score_p1(model, left, right)
        a = float(s["advantage"])
        mid_a.append(a)
        c = ev["currier"]
        currier_rows[c]["mid_a"].append(a)
        length_mid[len(ev["atoms"])].append(a)
        p1_mid_target_oov += int(s["target_oov_atoms"])
        p1_mid_any_oov += int(s["any_used_atom_oov"])

    for ev in p2_events:
        s = score_p2(model, ev["left"], ev["right"])
        dl = float(s["observed_minus_shift_left"])
        dr = float(s["observed_minus_shift_right"])
        p2_left.append(dl)
        p2_right.append(dr)
        c = ev["currier"]
        currier_rows[c]["p2_left"].append(dl)
        currier_rows[c]["p2_right"].append(dr)
        p2_oov_atoms += int(s["oov_atoms"])
        p2_atoms += int(s["n_atoms"])
        p2_any_oov += int(s["any_atom_oov"])

    d_reset = mean(real_a) - mean(mid_a)
    row = {
        "fold": f,
        "training": {
            "n_tokens": model.n_training_tokens,
            "n_atoms": model.n_training_atoms,
            "atom_types": list(model.alphabet),
            "n_atom_types": len(model.alphabet),
            "target_vocabulary_with_oov": model.v,
            "observed_contexts": model.observed_contexts,
            "alpha": ALPHA,
        },
        "P1": {
            "n_real": len(real_a),
            "n_mid": len(mid_a),
            "mean_A_real": mean(real_a),
            "mean_A_mid": mean(mid_a),
            "D_RESET": float(d_reset),
            "positive_D_RESET": bool(d_reset > 0.0),
        },
        "P2": {
            "n_events": len(p2_left),
            "mean_observed_minus_shift_left": mean(p2_left),
            "mean_observed_minus_shift_right": mean(p2_right),
            "observed_beats_shift_left": bool(mean(p2_left) < 0.0),
            "observed_beats_shift_right": bool(mean(p2_right) < 0.0),
        },
        "oov": {
            "P1_real_target_oov_atoms": p1_real_target_oov,
            "P1_real_target_atoms": 2 * len(real_a),
            "P1_real_target_oov_fraction": p1_real_target_oov / (2 * len(real_a)),
            "P1_real_events_any_used_atom_oov": p1_real_any_oov,
            "P1_real_event_any_used_atom_oov_fraction": p1_real_any_oov / len(real_a),
            "P1_mid_target_oov_atoms": p1_mid_target_oov,
            "P1_mid_target_atoms": 2 * len(mid_a),
            "P1_mid_target_oov_fraction": p1_mid_target_oov / (2 * len(mid_a)),
            "P1_mid_events_any_used_atom_oov": p1_mid_any_oov,
            "P1_mid_event_any_used_atom_oov_fraction": p1_mid_any_oov / len(mid_a),
            "P2_oov_atoms": p2_oov_atoms,
            "P2_atoms": p2_atoms,
            "P2_oov_fraction": p2_oov_atoms / p2_atoms,
            "P2_events_any_atom_oov": p2_any_oov,
            "P2_event_any_atom_oov_fraction": p2_any_oov / len(p2_left),
        },
        "currier_non_authoritative": summarize_by_currier(currier_rows),
        "length_non_authoritative": {
            "real_by_right_token_atoms": {
                str(k): {"n": len(v), "mean_A": mean(v)} for k, v in sorted(length_real.items())
            },
            "mid_by_source_token_atoms": {
                str(k): {"n": len(v), "mean_A": mean(v)} for k, v in sorted(length_mid.items())
            },
        },
    }
    raw = {
        "real_a": real_a,
        "mid_a": mid_a,
        "p2_left": p2_left,
        "p2_right": p2_right,
        "currier": currier_rows,
        "length_real": length_real,
        "length_mid": length_mid,
    }
    return row, raw


def classify(p1_pass: bool, p2_pass: bool) -> str:
    if p1_pass and p2_pass:
        return "SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY"
    if p1_pass and not p2_pass:
        return "SPACE MARKS A RESET BUT EXACT CUT IS WEAK"
    if not p1_pass and p2_pass:
        return "SPACE POSITION IS LOCALLY PRIVILEGED WITHOUT RESET EVIDENCE"
    return "VISIBLE SPACE NOT SUPPORTED AS PRODUCTION BOUNDARY"


def run(zl_path: Path) -> dict:
    auth = clean_event_authority(zl_path)
    authority = verify_authority(zl_path, auth)

    folds = []
    raw_by_fold = []
    for f in range(N_FOLDS):
        row, raw = score_fold(f, auth)
        folds.append(row)
        raw_by_fold.append(raw)

    pooled_real = [x for raw in raw_by_fold for x in raw["real_a"]]
    pooled_mid = [x for raw in raw_by_fold for x in raw["mid_a"]]
    pooled_left = [x for raw in raw_by_fold for x in raw["p2_left"]]
    pooled_right = [x for raw in raw_by_fold for x in raw["p2_right"]]
    fold_d = [float(x["P1"]["D_RESET"]) for x in folds]
    fold_left = [float(x["P2"]["mean_observed_minus_shift_left"]) for x in folds]
    fold_right = [float(x["P2"]["mean_observed_minus_shift_right"]) for x in folds]

    pooled_d = mean(pooled_real) - mean(pooled_mid)
    p1_positive_folds = sum(x > 0.0 for x in fold_d)
    p1_pass = bool(pooled_d > 0.0 and p1_positive_folds >= 4)

    pooled_dl = mean(pooled_left)
    pooled_dr = mean(pooled_right)
    p2_left_negative_folds = sum(x < 0.0 for x in fold_left)
    p2_right_negative_folds = sum(x < 0.0 for x in fold_right)
    p2_left_pass = bool(pooled_dl < 0.0 and p2_left_negative_folds >= 4)
    p2_right_pass = bool(pooled_dr < 0.0 and p2_right_negative_folds >= 4)
    p2_pass = bool(p2_left_pass and p2_right_pass)

    cagg = {
        c: {"real_a": [], "mid_a": [], "p2_left": [], "p2_right": []}
        for c in ("A", "B", "UNKNOWN")
    }
    length_real = defaultdict(list)
    length_mid = defaultdict(list)
    for raw in raw_by_fold:
        for c in cagg:
            for key in cagg[c]:
                cagg[c][key].extend(raw["currier"][c][key])
        for k, vals in raw["length_real"].items():
            length_real[k].extend(vals)
        for k, vals in raw["length_mid"].items():
            length_mid[k].extend(vals)

    return {
        "schema": SCHEMA,
        "phase": "ISSUE112_PHASE4A_FIRST_REVEAL",
        "target_reveal": True,
        "authority": authority,
        "model": {
            "family": "second_order_raw_eva_atom",
            "conditional": "P(x_t | x_{t-2}, x_{t-1})",
            "token_start_context": [BOS, BOS],
            "stop_probability": False,
            "additive_alpha": ALPHA,
            "alphabet_rule": "outer-training atom types plus exactly one OOV bucket",
            "heldout_unseen_atom_mapping": OOV,
            "folds": "original five physical-leaf folds",
        },
        "folds": folds,
        "primary": {
            "P1": {
                "pooled_n_real": len(pooled_real),
                "pooled_n_mid": len(pooled_mid),
                "pooled_mean_A_real": mean(pooled_real),
                "pooled_mean_A_mid": mean(pooled_mid),
                "pooled_D_RESET": pooled_d,
                "D_RESET_by_fold": fold_d,
                "positive_folds": p1_positive_folds,
                "pass_rule": "pooled D_RESET > 0 and positive in >=4/5 folds",
                "pass": p1_pass,
            },
            "P2": {
                "pooled_n": len(pooled_left),
                "pooled_mean_observed_minus_shift_left": pooled_dl,
                "pooled_mean_observed_minus_shift_right": pooled_dr,
                "left_by_fold": fold_left,
                "right_by_fold": fold_right,
                "left_negative_folds": p2_left_negative_folds,
                "right_negative_folds": p2_right_negative_folds,
                "left_pass": p2_left_pass,
                "right_pass": p2_right_pass,
                "pass_rule": "each pooled mean < 0 and negative in >=4/5 folds; both sides required",
                "pass": p2_pass,
            },
        },
        "classification": classify(p1_pass, p2_pass),
        "secondary_non_authoritative": {
            "currier": summarize_by_currier(cagg),
            "length": {
                "real_by_right_token_atoms": {
                    str(k): {"n": len(v), "mean_A": mean(v)} for k, v in sorted(length_real.items())
                },
                "mid_by_source_token_atoms": {
                    str(k): {"n": len(v), "mean_A": mean(v)} for k, v in sorted(length_mid.items())
                },
            },
            "line_position": {
                "status": "NOT_RUN",
                "reason": "no separate score-free line-position support rule was frozen before first reveal",
            },
        },
        "interpretation_firewall": {
            "spaces_proven_natural_language_words": False,
            "semantic_units_identified": False,
            "plaintext_recovered": False,
            "language_identified": False,
            "cipher_family_identified": False,
            "historical_mechanism_identified": False,
            "latent_state_fitted": False,
        },
    }


def self_test() -> None:
    toy = [
        ("a", "b", "a", "b"),
        ("a", "b", "a", "b"),
        ("a", "b", "c"),
        ("c", "a", "b"),
    ]
    m = AtomV2(toy)
    for ctx in ((BOS, BOS), ("a", "b"), ("z", "z"), (BOS, "z")):
        assert abs(m.distribution_sum(*ctx) - 1.0) < 1e-12
    assert m.map_atom("z") == OOV
    p1 = score_p1(m, ("c", "a"), ("b", "a"))
    assert math.isfinite(p1["advantage"])
    p2 = score_p2(m, ("a", "b", "a"), ("b", "a", "b"))
    assert math.isfinite(p2["observed_minus_shift_left"])
    assert math.isfinite(p2["observed_minus_shift_right"])
    assert len(("a", "b", "a") + ("b", "a", "b")) == 6
    assert classify(True, True) == "SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY"
    assert classify(True, False) == "SPACE MARKS A RESET BUT EXACT CUT IS WEAK"
    assert classify(False, True) == "SPACE POSITION IS LOCALLY PRIVILEGED WITHOUT RESET EVIDENCE"
    assert classify(False, False) == "VISIBLE SPACE NOT SUPPORTED AS PRODUCTION BOUNDARY"
    print("self-test OK")


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--self-test", action="store_true")
    g.add_argument("--run", nargs=2, metavar=("ZL3B", "OUT"))
    args = ap.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    zl = Path(args.run[0]).resolve()
    out_path = Path(args.run[1]).resolve()
    result = run(zl)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": result["classification"],
        "P1": result["primary"]["P1"],
        "P2": result["primary"]["P2"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
