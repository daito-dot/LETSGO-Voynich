#!/usr/bin/env python3
"""Issue #139: frozen IT2a POS2/EDGE2 independent first reveal.

The score-free Gate0 is re-run and required to reproduce its merged JSON SHA
before any predictive probability is computed. This scorer then applies the
fixed Issue #125 explicit onset factorization directly to the independently
frozen Phase63B W1 IT2a representation, with no hyperparameter selection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

import issue139_it2a_edge_gate0 as G

ROOT = G.ROOT
ISSUE125_PATH = (
    ROOT
    / "experiments"
    / "predictive-information"
    / "residual-gate"
    / "explicit_edge_l3.py"
)
GATE_PROVENANCE_PATH = (
    ROOT
    / "experiments"
    / "predictive-information"
    / "independent-edge"
    / "ISSUE139_GATE0_PROVENANCE.md"
)

EXPECTED_GATE_RESULT_SHA256 = "b97fe44633b088a97e86d5e08a74e9688647b8bb5eeeb7a44a43c98887b80fea"
EXPECTED_GATE_SCRIPT_BLOB = "e5571c92ad8c4ef437b73dac7a246eec3cf2a887"
EXPECTED_GATE_PROVENANCE_BLOB = "47af1106f55effa2adb309ec085d3101334680d8"
EXPECTED_ISSUE125_BLOB = "5b4bead22ed301cba88300af97cef654610648ab"

FIXED_K = 2
FIXED_ALPHA = 0.01
BYTE_END = 256
BYTE_BOS = -1
BYTE_V = 257
LN2 = math.log(2.0)
EQUIV_TOL = 1e-12
N_FOLDS = 5

VALID_CLASSES = (
    "INDEPENDENT EDGE REPLICATION PASSES",
    "INDEPENDENT EDGE REPLICATION FAILS",
    "INVALID INDEPENDENT REPLICATION",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def token_text(tok: Sequence[str]) -> str:
    return "".join(tok)


def token_symbols(tok: Sequence[str]) -> list[int]:
    raw = token_text(tok).encode("utf-8")
    if not raw:
        raise RuntimeError("visible token has no raw byte before END_TOKEN")
    return list(raw) + [BYTE_END]


class K2LineModel:
    """Issue #125 line-contiguous byte counts, retaining only the used k=2 table."""

    def __init__(self) -> None:
        self.counts: dict[tuple[int, int], Counter] = defaultdict(Counter)
        self.totals: Counter = Counter()

    @staticmethod
    def context(history: Sequence[int]) -> tuple[int, int]:
        h = list(history[-FIXED_K:])
        if len(h) < FIXED_K:
            h = [BYTE_BOS] * (FIXED_K - len(h)) + h
        return int(h[0]), int(h[1])

    def observe(self, history: Sequence[int], sym: int) -> None:
        ctx = self.context(history)
        self.counts[ctx][int(sym)] += 1
        self.totals[ctx] += 1

    def logp(self, history: Sequence[int], sym: int) -> float:
        ctx = self.context(history)
        n = int(self.totals.get(ctx, 0))
        c = int(self.counts.get(ctx, {}).get(int(sym), 0))
        return math.log((float(c) + FIXED_ALPHA) / (float(n) + FIXED_ALPHA * BYTE_V))

    def diagnostics(self) -> dict:
        return {
            "observed_k2_contexts": len(self.counts),
            "observed_k2_transitions": int(sum(len(c) for c in self.counts.values())),
        }


class ExplicitOnsetModel:
    """Faithful minimal reimplementation of Issue #125 POS2 / EDGE2."""

    def __init__(self, paragraphs, train_leaves: set[int]) -> None:
        self.line_model = K2LineModel()
        self.line_start_first: Counter = Counter()
        self.line_body_first: Counter = Counter()
        self.prev_terminal_first: dict[int, Counter] = defaultdict(Counter)
        self.line_start_second: dict[int, Counter] = defaultdict(Counter)
        self.line_body_second: dict[int, Counter] = defaultdict(Counter)
        self.shared_within_contexts: set[tuple[int, int]] = set()
        self.line_start_tokens = 0
        self.line_body_tokens = 0
        self.training_tokens = 0

        for paragraph in paragraphs:
            if paragraph.leaf is None or int(paragraph.leaf) not in train_leaves:
                continue
            for line in paragraph.lines:
                history: list[int] = []
                prev_final: int | None = None
                for ti, tok in enumerate(line):
                    syms = token_symbols(tok)
                    if len(syms) < 2:
                        raise RuntimeError("invalid token symbol sequence")
                    first, second = int(syms[0]), int(syms[1])
                    self.training_tokens += 1
                    if ti == 0:
                        self.line_start_tokens += 1
                        self.line_start_first[first] += 1
                        self.line_start_second[first][second] += 1
                    else:
                        if prev_final is None:
                            raise RuntimeError("missing previous terminal at line-body training token")
                        self.line_body_tokens += 1
                        self.line_body_first[first] += 1
                        self.prev_terminal_first[int(prev_final)][first] += 1
                        self.line_body_second[first][second] += 1
                    for j in range(2, len(syms)):
                        self.shared_within_contexts.add((int(syms[j - 2]), int(syms[j - 1])))
                    for sym in syms:
                        self.line_model.observe(history, int(sym))
                        history.append(int(sym))
                        if len(history) > FIXED_K:
                            history = history[-FIXED_K:]
                    prev_final = int(syms[-2])

        if self.line_start_tokens <= 0 or self.line_body_tokens <= 0:
            raise RuntimeError("empty onset training population")
        if len(self.prev_terminal_first) < 2:
            raise RuntimeError("degenerate previous-terminal training support")

    @staticmethod
    def smoothed_logp(counter: Counter, sym: int) -> float:
        total = int(sum(counter.values()))
        c = int(counter.get(int(sym), 0))
        return math.log((float(c) + FIXED_ALPHA) / (float(total) + FIXED_ALPHA * BYTE_V))

    def token_logp(
        self,
        syms: Sequence[int],
        line_start: bool,
        prev_final: int | None,
        use_identity: bool,
    ) -> float:
        syms = [int(x) for x in syms]
        if len(syms) < 2:
            raise RuntimeError("invalid token symbol sequence")
        first, second = syms[0], syms[1]
        ll = 0.0
        if line_start:
            ll += self.smoothed_logp(self.line_start_first, first)
            ll += self.smoothed_logp(self.line_start_second[first], second)
        else:
            if prev_final is None:
                raise RuntimeError("line-body token lacks previous terminal")
            if use_identity:
                ll += self.smoothed_logp(self.prev_terminal_first[int(prev_final)], first)
            else:
                ll += self.smoothed_logp(self.line_body_first, first)
            ll += self.smoothed_logp(self.line_body_second[first], second)
        for j in range(2, len(syms)):
            ll += self.line_model.logp(syms[j - 2 : j], syms[j])
        return float(ll)

    def diagnostics(self) -> dict:
        return {
            "training_tokens": self.training_tokens,
            "line_start_tokens": self.line_start_tokens,
            "line_body_tokens": self.line_body_tokens,
            "line_start_first_outcomes": len(self.line_start_first),
            "line_body_first_outcomes": len(self.line_body_first),
            "previous_terminal_contexts": len(self.prev_terminal_first),
            "previous_terminal_transitions": int(sum(len(c) for c in self.prev_terminal_first.values())),
            "line_start_second_contexts": len(self.line_start_second),
            "line_body_second_contexts": len(self.line_body_second),
            "shared_within_k2_contexts": len(self.shared_within_contexts),
            "line_model_k2": self.line_model.diagnostics(),
        }


def is_primary_target(parser, tok: Sequence[str]) -> bool:
    return bool(parser.parses(token_text(tok)))


def score_test_fold(model: ExplicitOnsetModel, paragraphs, test_leaves: set[int], parser) -> dict:
    log_pos: list[float] = []
    log_edge: list[float] = []
    log_line: list[float] = []
    n_visible = 0
    n_line_body_scored = 0
    seen_edge_context_scored = 0
    unseen_edge_context_scored = 0

    for paragraph in paragraphs:
        if paragraph.leaf is None or int(paragraph.leaf) not in test_leaves:
            continue
        for line in paragraph.lines:
            prev_final: int | None = None
            line_history: list[int] = []
            for ti, tok in enumerate(line):
                syms = token_symbols(tok)
                lp_pos = model.token_logp(syms, ti == 0, prev_final, use_identity=False)
                lp_edge = model.token_logp(syms, ti == 0, prev_final, use_identity=True)

                lp_line = 0.0
                for sym in syms:
                    lp_line += model.line_model.logp(line_history, int(sym))
                    line_history.append(int(sym))
                    if len(line_history) > FIXED_K:
                        line_history = line_history[-FIXED_K:]

                n_visible += 1
                if is_primary_target(parser, tok):
                    log_pos.append(float(lp_pos))
                    log_edge.append(float(lp_edge))
                    log_line.append(float(lp_line))
                    if ti > 0:
                        n_line_body_scored += 1
                        if prev_final in model.prev_terminal_first:
                            seen_edge_context_scored += 1
                        else:
                            unseen_edge_context_scored += 1
                prev_final = int(syms[-2])

    if not log_pos or not (len(log_pos) == len(log_edge) == len(log_line)):
        raise RuntimeError("empty or misaligned held-out primary target population")
    if not all(math.isfinite(v) for v in log_pos + log_edge + log_line):
        raise RuntimeError("non-finite held-out log probability")

    max_abs_equivalence = max(abs(a - b) for a, b in zip(log_edge, log_line))
    if max_abs_equivalence > EQUIV_TOL:
        raise RuntimeError(f"EDGE2 no longer equals LINECONT2: max_abs_logp={max_abs_equivalence}")

    n = len(log_pos)
    bits_pos = float(-sum(log_pos) / (n * LN2))
    bits_edge = float(-sum(log_edge) / (n * LN2))
    g_identity = float(bits_pos - bits_edge)
    return {
        "n_visible_clean_tokens": n_visible,
        "n_scored_primary_targets": n,
        "n_scored_line_body_targets": n_line_body_scored,
        "bits_POS2": bits_pos,
        "bits_EDGE2": bits_edge,
        "G_identity_IT2a": g_identity,
        "EDGE2_LINECONT2_max_abs_token_logp": float(max_abs_equivalence),
        "edge_context_seen_line_body_targets": seen_edge_context_scored,
        "edge_context_unseen_line_body_targets": unseen_edge_context_scored,
    }


def verify_post_gate_authority(it2a_path: Path) -> tuple[dict, str]:
    if G.git_blob_sha1(G.HERE.read_bytes()) != EXPECTED_GATE_SCRIPT_BLOB:
        raise RuntimeError("merged Gate0 executable blob changed")
    if not GATE_PROVENANCE_PATH.is_file():
        raise RuntimeError("merged Gate0 provenance missing")
    if G.git_blob_sha1(GATE_PROVENANCE_PATH.read_bytes()) != EXPECTED_GATE_PROVENANCE_BLOB:
        raise RuntimeError("merged Gate0 provenance blob changed")
    if not ISSUE125_PATH.is_file():
        raise RuntimeError("Issue125 architecture authority missing")
    if G.git_blob_sha1(ISSUE125_PATH.read_bytes()) != EXPECTED_ISSUE125_BLOB:
        raise RuntimeError("Issue125 architecture authority changed")

    gate = G.run_gate(it2a_path)
    gate_text = G.canonical_json(gate)
    gate_sha = sha256_text(gate_text)
    if not gate.get("gate_pass"):
        raise RuntimeError("merged Gate0 does not pass")
    if gate.get("scientific_edge_metrics_computed") is not False:
        raise RuntimeError("Gate0 firewall changed")
    if gate_sha != EXPECTED_GATE_RESULT_SHA256:
        raise RuntimeError(f"Gate0 result SHA changed: {gate_sha}")
    return gate, gate_sha


def score(it2a_path: Path) -> dict:
    gate, gate_sha = verify_post_gate_authority(it2a_path)
    folds = [set(map(int, xs)) for xs in gate["frozen_fold_leaf_sets"]]
    if len(folds) != N_FOLDS:
        raise RuntimeError("Gate0 fold count changed")

    paragraphs, parser_audit = G.p63.parse_ivtff(it2a_path, "IT2a", "W1")
    parser = G.e.SlotParser()
    G.e.validate_parser(parser)
    all_leaves = set().union(*folds)

    outer = []
    for f, test_leaves in enumerate(folds):
        train_leaves = all_leaves - test_leaves
        if train_leaves & test_leaves:
            raise RuntimeError(f"fold {f} train/test overlap")
        model = ExplicitOnsetModel(paragraphs, train_leaves)
        row = score_test_fold(model, paragraphs, test_leaves, parser)
        expected_clean = int(gate["population"]["fold_clean_tokens"][f])
        expected_scored = int(gate["population"]["fold_accepted_tokens"][f])
        expected_line_body = int(gate["population"]["fold_accepted_line_body_tokens"][f])
        expected_training = int(gate["outer_training_support"][f]["training_clean_tokens"])
        if row["n_visible_clean_tokens"] != expected_clean:
            raise RuntimeError(f"fold {f} visible support changed")
        if row["n_scored_primary_targets"] != expected_scored:
            raise RuntimeError(f"fold {f} target support changed")
        if row["n_scored_line_body_targets"] != expected_line_body:
            raise RuntimeError(f"fold {f} line-body target support changed")
        if model.training_tokens != expected_training:
            raise RuntimeError(f"fold {f} training support changed")
        outer.append({
            "fold": f,
            **row,
            "training_diagnostics": model.diagnostics(),
        })

    gains = [float(r["G_identity_IT2a"]) for r in outer]
    mean_gain = float(sum(gains) / len(gains))
    positive_folds = int(sum(g > 0.0 for g in gains))
    passed = bool(mean_gain > 0.0 and positive_folds >= 4)
    classification = (
        "INDEPENDENT EDGE REPLICATION PASSES"
        if passed
        else "INDEPENDENT EDGE REPLICATION FAILS"
    )

    mean_pos = float(sum(r["bits_POS2"] for r in outer) / N_FOLDS)
    mean_edge = float(sum(r["bits_EDGE2"] for r in outer) / N_FOLDS)
    max_equiv = float(max(r["EDGE2_LINECONT2_max_abs_token_logp"] for r in outer))

    result = {
        "schema": "issue139-it2a-edge-first-reveal-v1",
        "issue": 139,
        "phase": "IT2A_EDGE_INDEPENDENT_FIRST_REVEAL",
        "scored": True,
        "classification": classification,
        "authority": {
            "gate0_reproduced": True,
            "gate0_result_sha256": gate_sha,
            "gate0_expected_sha256": EXPECTED_GATE_RESULT_SHA256,
            "source_sha256": gate["source"]["sha256"],
            "source_git_blob_sha1": gate["source"]["git_blob_sha1"],
            "issue125_architecture_blob": EXPECTED_ISSUE125_BLOB,
            "gate_script_blob": EXPECTED_GATE_SCRIPT_BLOB,
            "gate_provenance_blob": EXPECTED_GATE_PROVENANCE_BLOB,
            "parser_audit_reproduced": parser_audit,
        },
        "frozen_model": {
            "k": FIXED_K,
            "alpha": FIXED_ALPHA,
            "END_TOKEN": BYTE_END,
            "BOS": BYTE_BOS,
            "outcome_vocabulary_size": BYTE_V,
            "source_line_hard_reset": True,
            "POS2": "generic line-start / pooled line-body first-symbol factor + line-position second-symbol factor + shared line-trained k2 continuation",
            "EDGE2": "POS2 except line-body first symbol conditions on immediately previous clean visible token terminal raw byte",
            "previous_token_may_be_primary_target_rejected": True,
            "unseen_context_policy": "empty exact-context additive smoothing; no pooled backoff",
            "hyperparameter_selection": "none",
        },
        "outer": outer,
        "primary": {
            "definition": "G_identity_IT2a = bits(POS2) - bits(EDGE2)",
            "G_identity_IT2a_by_fold": gains,
            "mean_G_identity_IT2a": mean_gain,
            "positive_folds": positive_folds,
            "required_positive_folds": 4,
            "mean_must_be_positive": True,
            "pass": passed,
            "mean_bits_POS2": mean_pos,
            "mean_bits_EDGE2": mean_edge,
            "EDGE2_LINECONT2_max_abs_token_logp": max_equiv,
        },
        "diagnostic_status": "NON_PROMOTING_NO_REFIT_NO_CLASSIFICATION_INPUT_EXCEPT_FROZEN_PRIMARY",
        "firewall": {
            "target_driven_normalization": False,
            "target_driven_exclusion": False,
            "target_driven_fold_change": False,
            "target_driven_smoothing_or_fallback": False,
            "target_driven_model_family_change": False,
            "currier_hand_section_conditioned_fit": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "literal_table_equality_required": False,
            "semantic_or_cipher_inference": False,
        },
    }
    if classification not in VALID_CLASSES:
        raise RuntimeError("classification escaped frozen class set")
    return result


def invalid_result(exc: Exception) -> dict:
    return {
        "schema": "issue139-it2a-edge-first-reveal-v1",
        "issue": 139,
        "phase": "IT2A_EDGE_INDEPENDENT_FIRST_REVEAL",
        "scored": False,
        "classification": "INVALID INDEPENDENT REPLICATION",
        "error": f"{type(exc).__name__}: {exc}",
        "firewall": {
            "post_failure_model_repair_allowed": False,
            "post_failure_target_driven_change_allowed": False,
        },
    }


def self_test() -> dict:
    class P:
        def __init__(self, leaf, lines):
            self.leaf = leaf
            self.lines = lines

    paragraphs = [
        P(1, [[tuple("ab"), tuple("ca"), tuple("db")], [tuple("ba"), tuple("cb")]]),
        P(2, [[tuple("aa"), tuple("bc"), tuple("da")], [tuple("ac"), tuple("bd")]]),
    ]
    model = ExplicitOnsetModel(paragraphs, {1, 2})
    syms = token_symbols(tuple("ab"))
    a = model.token_logp(syms, True, None, False)
    b = model.token_logp(syms, True, None, True)
    if abs(a - b) > 1e-15:
        raise AssertionError("line-start POS2/EDGE2 must be identical")
    unseen = ExplicitOnsetModel.smoothed_logp(Counter(), ord("a"))
    if abs(unseen - math.log(1.0 / BYTE_V)) > 1e-15:
        raise AssertionError("empty-context smoothing is not uniform 1/257")
    return {
        "ok": True,
        "target_source_loaded": False,
        "fixed_k": FIXED_K,
        "fixed_alpha": FIXED_ALPHA,
        "outcome_vocabulary_size": BYTE_V,
        "line_start_identity_equal": True,
        "empty_context_uniform": True,
    }


def canonical_json(obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--run", nargs=2, metavar=("IT2A", "OUT_JSON"))
    ns = ap.parse_args(argv)

    if ns.self_test:
        print(canonical_json(self_test()), end="")
        return 0

    it2a_path = Path(ns.run[0]).resolve()
    out_path = Path(ns.run[1]).resolve()
    try:
        result = score(it2a_path)
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
