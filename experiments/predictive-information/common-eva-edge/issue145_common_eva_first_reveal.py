#!/usr/bin/env python3
"""Issue #145: frozen common-EVA dual-reading POS2/EDGE2 first reveal.

The merged score-free Gate0 is reproduced byte-for-byte in canonical JSON
before any predictive probability is computed. The scorer then applies the
prospectively frozen Issue #125 factorization to the already-existing common
Basic-EVA atom representation for ZL3b and Takahashi/IT2a.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Sequence

import issue145_common_eva_gate0 as GATE

ROOT = GATE.ROOT
GATE_PROVENANCE_PATH = (
    ROOT
    / "experiments"
    / "predictive-information"
    / "common-eva-edge"
    / "ISSUE145_GATE0_PROVENANCE.md"
)

EXPECTED_GATE_RESULT_SHA256 = "563573e81c931133aaa9877bcf79a57a40ebb3e2a946183cac3f6e922d65eb48"
EXPECTED_GATE_SCRIPT_BLOB = "80585066e746f42ac10554aaaeece793682a0b84"
EXPECTED_GATE_PROVENANCE_BLOB = "e98d2fffac1d2500623a7f8660343ead67218332"
EXPECTED_GATE_MERGE = "692b141ac8457f4026ae482a4a8ae79a4f0fef50"

FIXED_K = 2
FIXED_ALPHA = 0.01
END_TOKEN = "<END_TOKEN>"
BOS = "<BOS>"
V = 32
N_FOLDS = 5
LN2 = math.log(2.0)
EQUIV_TOL = 1e-12

VALID_CLASSES = (
    "COMMON-EVA EDGE ROBUST IN BOTH READINGS",
    "COMMON-EVA EDGE ROBUST IN ZL3B ONLY",
    "COMMON-EVA EDGE ROBUST IN IT2A ONLY",
    "COMMON-EVA EDGE NOT ROBUST IN EITHER READING",
    "INVALID COMMON-REPRESENTATION EDGE TEST",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def token_symbols(atoms: Sequence[str]) -> list[str]:
    if not atoms:
        raise RuntimeError("clean token emitted no common-EVA atoms")
    for atom in atoms:
        if atom not in GATE.ATOM_OUTCOMES:
            raise RuntimeError(f"atom outside frozen common inventory: {atom!r}")
    return list(atoms) + [END_TOKEN]


def clean_runs(lines: Sequence[str], leaf_fold: dict[int, int], parser):
    """Return immutable clean runs under the merged Gate semantics."""
    runs = []
    for source_line_no, line in enumerate(lines, start=1):
        m = GATE.G.LOCUS_RE.match(line)
        if not m or "P" not in m.group("code"):
            continue
        loc = m.group("loc")
        page = loc.split(".", 1)[0]
        lm = GATE.G.LEAF_RE.match(page)
        if not lm:
            continue
        leaf = int(lm.group(1))
        if leaf not in leaf_fold:
            continue
        fold = int(leaf_fold[leaf])
        segments, n_dot = GATE.G.split_certain_spaces(m.group("body"))
        if n_dot != len(segments) - 1:
            raise RuntimeError(f"dot/segment invariant failed at {loc}")

        current = []
        for segment_index, raw in enumerate(segments):
            atoms, _reasons = GATE.clean_atoms(raw)
            if atoms is None:
                if current:
                    runs.append((fold, leaf, loc, source_line_no, tuple(current)))
                    current = []
                continue
            current.append(
                {
                    "raw": raw,
                    "atoms": tuple(atoms),
                    "slotparser_accepted": bool(parser.parses(raw)),
                    "segment_index": int(segment_index),
                }
            )
        if current:
            runs.append((fold, leaf, loc, source_line_no, tuple(current)))
    return tuple(runs)


class K2RunModel:
    """Exact fixed-k2 counts across each maximal clean run."""

    def __init__(self) -> None:
        self.counts: dict[tuple[str, str], Counter] = defaultdict(Counter)
        self.totals: Counter = Counter()

    @staticmethod
    def context(history: Sequence[str]) -> tuple[str, str]:
        h = list(history[-FIXED_K:])
        if len(h) < FIXED_K:
            h = [BOS] * (FIXED_K - len(h)) + h
        return str(h[0]), str(h[1])

    def observe(self, history: Sequence[str], symbol: str) -> None:
        ctx = self.context(history)
        self.counts[ctx][symbol] += 1
        self.totals[ctx] += 1

    def logp(self, history: Sequence[str], symbol: str) -> float:
        ctx = self.context(history)
        n = int(self.totals.get(ctx, 0))
        c = int(self.counts.get(ctx, {}).get(symbol, 0))
        return math.log((float(c) + FIXED_ALPHA) / (float(n) + FIXED_ALPHA * V))

    def diagnostics(self) -> dict:
        return {
            "observed_k2_contexts": len(self.counts),
            "observed_k2_transitions": int(sum(len(v) for v in self.counts.values())),
        }


class CommonEdgeModel:
    """Frozen atom-level POS2_COMMON / EDGE2_COMMON factorization."""

    def __init__(self, runs, train_folds: set[int]) -> None:
        self.run_model = K2RunModel()
        self.start_first: Counter = Counter()
        self.body_first: Counter = Counter()
        self.prev_terminal_first: dict[str, Counter] = defaultdict(Counter)
        self.start_second: dict[str, Counter] = defaultdict(Counter)
        self.body_second: dict[str, Counter] = defaultdict(Counter)
        self.training_clean_tokens = 0
        self.training_run_starts = 0
        self.training_run_bodies = 0

        for fold, _leaf, _loc, _line_no, run in runs:
            if int(fold) not in train_folds:
                continue
            history: list[str] = []
            previous_terminal: str | None = None
            for ti, record in enumerate(run):
                syms = token_symbols(record["atoms"])
                first, second = syms[0], syms[1]
                self.training_clean_tokens += 1
                if ti == 0:
                    self.training_run_starts += 1
                    self.start_first[first] += 1
                    self.start_second[first][second] += 1
                else:
                    if previous_terminal is None:
                        raise RuntimeError("run-body training token lacks previous terminal")
                    self.training_run_bodies += 1
                    self.body_first[first] += 1
                    self.prev_terminal_first[previous_terminal][first] += 1
                    self.body_second[first][second] += 1

                for sym in syms:
                    self.run_model.observe(history, sym)
                    history.append(sym)
                    if len(history) > FIXED_K:
                        history = history[-FIXED_K:]
                previous_terminal = syms[-2]

        if self.training_run_starts <= 0 or self.training_run_bodies <= 0:
            raise RuntimeError("degenerate START/BODY training support")
        if len(self.prev_terminal_first) < 2:
            raise RuntimeError("degenerate previous-terminal atom support")

    @staticmethod
    def categorical_logp(counter: Counter, symbol: str) -> float:
        total = int(sum(counter.values()))
        c = int(counter.get(symbol, 0))
        return math.log((float(c) + FIXED_ALPHA) / (float(total) + FIXED_ALPHA * V))

    def token_logp(
        self,
        syms: Sequence[str],
        is_run_start: bool,
        previous_terminal: str | None,
        use_identity: bool,
    ) -> float:
        syms = list(syms)
        if len(syms) < 2:
            raise RuntimeError("invalid common-EVA token sequence")
        first, second = syms[0], syms[1]
        ll = 0.0
        if is_run_start:
            ll += self.categorical_logp(self.start_first, first)
            ll += self.categorical_logp(self.start_second[first], second)
        else:
            if previous_terminal is None:
                raise RuntimeError("run-body score lacks previous terminal")
            if use_identity:
                ll += self.categorical_logp(self.prev_terminal_first[previous_terminal], first)
            else:
                ll += self.categorical_logp(self.body_first, first)
            ll += self.categorical_logp(self.body_second[first], second)

        for j in range(2, len(syms)):
            ll += self.run_model.logp(syms[j - 2 : j], syms[j])
        return float(ll)

    def diagnostics(self) -> dict:
        return {
            "training_clean_tokens": self.training_clean_tokens,
            "training_run_start_tokens": self.training_run_starts,
            "training_run_body_tokens": self.training_run_bodies,
            "start_first_outcomes": len(self.start_first),
            "body_first_outcomes": len(self.body_first),
            "previous_terminal_atom_contexts": len(self.prev_terminal_first),
            "previous_terminal_to_initial_atom_pairs": int(
                sum(len(v) for v in self.prev_terminal_first.values())
            ),
            "start_second_contexts": len(self.start_second),
            "body_second_contexts": len(self.body_second),
            "run_model_k2": self.run_model.diagnostics(),
        }


def score_fold(model: CommonEdgeModel, runs, test_fold: int) -> dict:
    log_pos = []
    log_edge = []
    log_full = []
    visible_clean = 0
    scored_body = 0
    seen_identity_contexts = 0
    unseen_identity_contexts = 0

    for fold, _leaf, _loc, _line_no, run in runs:
        if int(fold) != int(test_fold):
            continue
        history: list[str] = []
        previous_terminal: str | None = None
        for ti, record in enumerate(run):
            syms = token_symbols(record["atoms"])
            lp_pos = model.token_logp(syms, ti == 0, previous_terminal, False)
            lp_edge = model.token_logp(syms, ti == 0, previous_terminal, True)

            lp_full = 0.0
            for sym in syms:
                lp_full += model.run_model.logp(history, sym)
                history.append(sym)
                if len(history) > FIXED_K:
                    history = history[-FIXED_K:]

            visible_clean += 1
            if record["slotparser_accepted"]:
                log_pos.append(float(lp_pos))
                log_edge.append(float(lp_edge))
                log_full.append(float(lp_full))
                if ti > 0:
                    scored_body += 1
                    if previous_terminal in model.prev_terminal_first:
                        seen_identity_contexts += 1
                    else:
                        unseen_identity_contexts += 1
            previous_terminal = syms[-2]

    if not log_pos or not (len(log_pos) == len(log_edge) == len(log_full)):
        raise RuntimeError("empty or misaligned primary target population")
    if not all(math.isfinite(x) for x in log_pos + log_edge + log_full):
        raise RuntimeError("non-finite held-out log probability")

    max_abs_equiv = max(abs(a - b) for a, b in zip(log_edge, log_full))
    if max_abs_equiv > EQUIV_TOL:
        raise RuntimeError(
            f"EDGE2_COMMON no longer equals full clean-run k2: {max_abs_equiv}"
        )

    n = len(log_pos)
    bits_pos = float(-sum(log_pos) / (n * LN2))
    bits_edge = float(-sum(log_edge) / (n * LN2))
    return {
        "n_visible_clean_tokens": visible_clean,
        "n_scored_primary_targets": n,
        "n_scored_run_body_targets": scored_body,
        "bits_POS2_COMMON": bits_pos,
        "bits_EDGE2_COMMON": bits_edge,
        "G_common": float(bits_pos - bits_edge),
        "EDGE2_COMMON_full_run_k2_max_abs_token_logp": float(max_abs_equiv),
        "identity_context_seen_body_targets": seen_identity_contexts,
        "identity_context_unseen_body_targets": unseen_identity_contexts,
    }


def reading_pass(rows: Sequence[dict]) -> tuple[bool, float, int]:
    gains = [float(r["G_common"]) for r in rows]
    mean_gain = float(sum(gains) / len(gains))
    positive = int(sum(g > 0.0 for g in gains))
    return bool(mean_gain > 0.0 and positive >= 4), mean_gain, positive


def classification(zl_pass: bool, it_pass: bool) -> str:
    if zl_pass and it_pass:
        return "COMMON-EVA EDGE ROBUST IN BOTH READINGS"
    if zl_pass:
        return "COMMON-EVA EDGE ROBUST IN ZL3B ONLY"
    if it_pass:
        return "COMMON-EVA EDGE ROBUST IN IT2A ONLY"
    return "COMMON-EVA EDGE NOT ROBUST IN EITHER READING"


def verify_post_gate_authority(zl_path: Path, it_path: Path) -> tuple[dict, str]:
    if GATE.git_blob_sha1(GATE.HERE.read_bytes()) != EXPECTED_GATE_SCRIPT_BLOB:
        raise RuntimeError("merged Gate0 executable blob changed")
    if not GATE_PROVENANCE_PATH.is_file():
        raise RuntimeError("merged Gate0 provenance missing")
    if GATE.git_blob_sha1(GATE_PROVENANCE_PATH.read_bytes()) != EXPECTED_GATE_PROVENANCE_BLOB:
        raise RuntimeError("merged Gate0 provenance blob changed")

    gate = GATE.run_gate(zl_path, it_path)
    gate_text = GATE.canonical_json(gate)
    gate_sha = sha256_text(gate_text)
    if not gate.get("gate_pass"):
        raise RuntimeError("merged Gate0 no longer passes")
    if gate.get("scientific_target_metrics_computed") is not False:
        raise RuntimeError("Gate0 firewall changed")
    if gate_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Gate0 result SHA changed: {gate_sha}")
    return gate, gate_sha


def score(zl_path: Path, it_path: Path) -> dict:
    gate, gate_sha = verify_post_gate_authority(zl_path, it_path)
    leaf_fold = {
        int(leaf): int(fold)
        for fold, leaves in enumerate(gate["fold_authority"]["identity"])
        for leaf in leaves
    }
    parser = GATE.E.SlotParser()
    GATE.E.validate_parser(parser)

    sources = {}
    for label, path in (("ZL3b", zl_path), ("IT2a", it_path)):
        _source, lines = GATE.source_identity(path, label)
        runs = clean_runs(lines, leaf_fold, parser)
        outer = []
        all_folds = set(range(N_FOLDS))
        gate_reading = gate["readings"][label]
        for f in range(N_FOLDS):
            model = CommonEdgeModel(runs, all_folds - {f})
            row = score_fold(model, runs, f)
            expected = gate_reading["by_fold"][str(f)]
            if row["n_visible_clean_tokens"] != int(expected["clean_tokens"]):
                raise RuntimeError(f"{label} fold {f} clean support changed")
            if row["n_scored_primary_targets"] != int(expected["primary_targets"]):
                raise RuntimeError(f"{label} fold {f} primary support changed")
            if row["n_scored_run_body_targets"] != int(expected["primary_run_body_targets"]):
                raise RuntimeError(f"{label} fold {f} body support changed")
            expected_train = gate_reading["outer_training_support"][f]
            if model.training_clean_tokens != int(expected_train["training_clean_tokens"]):
                raise RuntimeError(f"{label} fold {f} training support changed")
            outer.append({"fold": f, **row, "training_diagnostics": model.diagnostics()})

        passed, mean_gain, positive = reading_pass(outer)
        mean_pos = float(sum(r["bits_POS2_COMMON"] for r in outer) / N_FOLDS)
        mean_edge = float(sum(r["bits_EDGE2_COMMON"] for r in outer) / N_FOLDS)
        sources[label] = {
            "outer": outer,
            "primary": {
                "G_common_by_fold": [float(r["G_common"]) for r in outer],
                "mean_G_common": mean_gain,
                "positive_folds": positive,
                "required_positive_folds": 4,
                "mean_must_be_positive": True,
                "pass": passed,
                "mean_bits_POS2_COMMON": mean_pos,
                "mean_bits_EDGE2_COMMON": mean_edge,
                "EDGE2_COMMON_full_run_k2_max_abs_token_logp": float(
                    max(r["EDGE2_COMMON_full_run_k2_max_abs_token_logp"] for r in outer)
                ),
            },
        }

    zl_pass = bool(sources["ZL3b"]["primary"]["pass"])
    it_pass = bool(sources["IT2a"]["primary"]["pass"])
    frozen_class = classification(zl_pass, it_pass)
    if frozen_class not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")

    zl_mean = float(sources["ZL3b"]["primary"]["mean_G_common"])
    it_mean = float(sources["IT2a"]["primary"]["mean_G_common"])
    fold_differences = [
        float(sources["IT2a"]["outer"][f]["G_common"] - sources["ZL3b"]["outer"][f]["G_common"])
        for f in range(N_FOLDS)
    ]
    ratio = float(it_mean / zl_mean) if zl_mean > 0.0 and it_mean > 0.0 else None

    return {
        "schema": "issue145-common-eva-edge-first-reveal-v1",
        "issue": 145,
        "phase": "COMMON_EVA_DUAL_EDGE_FIRST_REVEAL",
        "scored": True,
        "classification": frozen_class,
        "authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": gate_sha,
            "gate0_expected_sha256": EXPECTED_GATE_RESULT_SHA256,
            "gate0_script_blob": EXPECTED_GATE_SCRIPT_BLOB,
            "gate0_provenance_blob": EXPECTED_GATE_PROVENANCE_BLOB,
            "gate0_merge": EXPECTED_GATE_MERGE,
            "sources": gate["sources"],
            "fold_identity_sha256": gate["fold_authority"]["identity_sha256"],
        },
        "frozen_model": {
            "representation": "Phase4A/4B common Basic-EVA atoms",
            "atom_outcomes": sorted(GATE.ATOM_OUTCOMES),
            "n_atom_outcomes": len(GATE.ATOM_OUTCOMES),
            "END_TOKEN": END_TOKEN,
            "BOS": BOS,
            "outcome_vocabulary_size": V,
            "k": FIXED_K,
            "alpha": FIXED_ALPHA,
            "clean_run_reset": True,
            "unclean_segment_breaks_context": True,
            "hyperparameter_selection": "none",
            "unseen_context_policy": "empty exact-context additive smoothing; no pooled backoff",
        },
        "readings": sources,
        "primary_joint": {
            "ZL3b_pass": zl_pass,
            "IT2a_pass": it_pass,
            "classification": frozen_class,
        },
        "secondary_non_promoting": {
            "G_common_IT2a_minus_ZL3b_by_fold": fold_differences,
            "mean_G_common_IT2a_minus_ZL3b": float(it_mean - zl_mean),
            "mean_gain_ratio_IT2a_over_ZL3b_if_both_positive": ratio,
            "native_reference_only": {
                "ZL3b_Issue125_identity_gain_approx": 0.02026956,
                "IT2a_Issue139_identity_gain": 0.15211188542908544,
                "note": "native-reference numbers do not enter classification",
            },
        },
        "firewall": {
            "target_selected_normalization": False,
            "target_selected_exclusion": False,
            "target_selected_fold_change": False,
            "target_selected_smoothing_or_fallback": False,
            "target_selected_model_family_change": False,
            "token_alignment_by_cross_reading_similarity": False,
            "literal_table_transport_tested": False,
            "currier_hand_section_conditioned_fit": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "semantic_or_cipher_inference": False,
        },
    }


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue145-common-eva-edge-first-reveal-v1",
        "issue": 145,
        "phase": "COMMON_EVA_DUAL_EDGE_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID COMMON-REPRESENTATION EDGE TEST",
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {
            "post_failure_representation_repair_allowed": False,
            "post_failure_target_driven_change_allowed": False,
        },
    }


def self_test() -> dict:
    synthetic_runs = (
        (0, 1, "f1r.1", 1, (
            {"raw": "ab", "atoms": ("a", "b"), "slotparser_accepted": True, "segment_index": 0},
            {"raw": "ca", "atoms": ("c", "a"), "slotparser_accepted": True, "segment_index": 1},
            {"raw": "db", "atoms": ("d", "b"), "slotparser_accepted": True, "segment_index": 2},
        )),
        (1, 2, "f2r.1", 2, (
            {"raw": "aa", "atoms": ("a", "a"), "slotparser_accepted": True, "segment_index": 0},
            {"raw": "bc", "atoms": ("b", "c"), "slotparser_accepted": True, "segment_index": 1},
            {"raw": "da", "atoms": ("d", "a"), "slotparser_accepted": True, "segment_index": 2},
        )),
    )
    model = CommonEdgeModel(synthetic_runs, {0, 1})
    syms = token_symbols(("a", "b"))
    start_pos = model.token_logp(syms, True, None, False)
    start_edge = model.token_logp(syms, True, None, True)
    if abs(start_pos - start_edge) > 1e-15:
        raise AssertionError("START POS2/EDGE2 factors differ")
    empty = CommonEdgeModel.categorical_logp(Counter(), "a")
    if abs(empty - math.log(1.0 / V)) > 1e-15:
        raise AssertionError("empty exact context is not uniform 1/32")
    return {
        "ok": True,
        "target_sources_loaded": False,
        "fixed_k": FIXED_K,
        "fixed_alpha": FIXED_ALPHA,
        "outcome_vocabulary_size": V,
        "start_identity_equal": True,
        "empty_context_uniform": True,
    }


def canonical_json(obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--run", nargs=3, metavar=("ZL3B", "IT2A", "OUT_JSON"))
    ns = ap.parse_args(argv)

    if ns.self_test:
        print(canonical_json(self_test()), end="")
        return 0

    zl_path = Path(ns.run[0]).resolve()
    it_path = Path(ns.run[1]).resolve()
    out_path = Path(ns.run[2]).resolve()
    try:
        result = score(zl_path, it_path)
        rc = 0
    except Exception as exc:
        result = invalid_result(exc)
        rc = 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
