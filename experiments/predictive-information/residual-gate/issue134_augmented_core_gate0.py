#!/usr/bin/env python3
"""Issue #134 score-free Gate0 for the augmented observable core.

This audit verifies frozen source/core/Currier/fold/support authorities and that
all outer and outer+inner training populations can construct the preregistered
A/B/pooled terminal-context fallback hierarchy. It deliberately computes no
new Issue #134 predictive probability, likelihood, bits/token or residual.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Iterable, Sequence

HERE = Path(__file__).resolve()
R_PATH = HERE.parent / "residual_first_reveal.py"
CUR_PATH = HERE.parent / "currier_edge_gate0.py"

EXPECTED_CORE_SHA = "0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27"
EXPECTED_CURRIER_EDGE_GATE_SHA = "31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb"
EXPECTED_SOURCE_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_OUTER_TARGET_COUNTS = (4430, 4810, 5516, 5447, 4868)
LABELS = ("A", "B")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


R = load_module("issue134_residual_anchor", R_PATH)
CUR = load_module("issue134_currier_gate_anchor", CUR_PATH)
P1 = R.P1
OA = R.OA


def canonical_json(x: dict) -> str:
    return json.dumps(x, indent=2, sort_keys=True, allow_nan=False) + "\n"


def json_sha256(x: dict) -> str:
    return hashlib.sha256(canonical_json(x).encode("utf-8")).hexdigest()


def sha256_lines(rows: Iterable[str]) -> str:
    payload = "\n".join(sorted(str(x) for x in rows)) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def leaves_for_folds(folds, selected: Sequence[int]) -> set[int]:
    out: set[int] = set()
    for f in selected:
        out.update(int(x) for x in folds[int(f)])
    return out


def select_items(items, leaves: set[int], include: bool):
    if include:
        return [it for it in items if int(it.leaf) in leaves]
    return [it for it in items if int(it.leaf) not in leaves]


def accepted_target_count(items, parsed) -> int:
    n = 0
    for it in P1.I.ordered(items):
        for li, line in enumerate(it.lines):
            for ti, _tok in enumerate(line):
                n += int(parsed[it.item_id][li][ti] is not None)
    return int(n)


def visible_token_count(items) -> int:
    return int(sum(len(line) for it in items for line in it.lines))


def support_audit(items, by_doc: dict) -> dict:
    contexts = {"A": set(), "B": set(), "OTHER": set(), "POOLED": set()}
    event_ids = {"A": [], "B": [], "OTHER": [], "POOLED": []}
    context_ids = {"A": [], "B": [], "OTHER": [], "POOLED": []}
    line_start_tokens = 0
    line_body_tokens = 0
    source_lines = 0
    items_by_label = {"A": 0, "B": 0, "OTHER": 0}
    events_by_label = {"A": 0, "B": 0, "OTHER": 0}

    for it in P1.I.ordered(items):
        rec = by_doc.get(it.document)
        if rec is None:
            raise RuntimeError(f"document absent from Currier authority: {it.document}")
        raw_label = str(rec["label"])
        lab = raw_label if raw_label in LABELS else "OTHER"
        items_by_label[lab] += 1

        for li, line in enumerate(it.lines):
            source_lines += 1
            if not line:
                continue
            line_start_tokens += 1
            prev_syms = P1.token_symbols(line[0])
            if len(prev_syms) < 2:
                raise RuntimeError("visible line-start token lacks raw terminal byte")
            prev_final = int(prev_syms[-2])
            if not (0 <= prev_final <= 255):
                raise RuntimeError(f"previous terminal is not a raw byte: {prev_final}")

            for ti in range(1, len(line)):
                # Outcome-blind Gate: do not inspect the current token's first byte.
                tok = line[ti]
                syms = P1.token_symbols(tok)
                if len(syms) < 2:
                    raise RuntimeError("visible line-body token lacks raw terminal byte")

                line_body_tokens += 1
                events_by_label[lab] += 1
                contexts[lab].add(prev_final)
                contexts["POOLED"].add(prev_final)

                event_id = (
                    f"leaf={int(it.leaf)}|doc={it.document}|item={it.item_id}|"
                    f"line={li}|token={ti}|prev={prev_final}|currier={lab}"
                )
                event_ids[lab].append(event_id)
                event_ids["POOLED"].append(event_id)

                prev_final = int(syms[-2])
                if not (0 <= prev_final <= 255):
                    raise RuntimeError(f"current terminal is not a raw byte: {prev_final}")

    for key in contexts:
        context_ids[key] = [str(v) for v in sorted(contexts[key])]

    fallback = {
        lab: {
            "native_context_count": int(len(contexts[lab])),
            "pooled_context_count": int(len(contexts["POOLED"])),
            "pooled_only_fallback_context_count": int(len(contexts["POOLED"] - contexts[lab])),
        }
        for lab in LABELS
    }
    fallback["UNKNOWN_OR_OTHER"] = {
        "native_context_count": 0,
        "pooled_context_count": int(len(contexts["POOLED"])),
        "pooled_only_fallback_context_count": int(len(contexts["POOLED"])),
    }

    return {
        "items_by_currier": {k: int(v) for k, v in items_by_label.items()},
        "source_lines": int(source_lines),
        "line_start_tokens": int(line_start_tokens),
        "line_body_edge_events": int(line_body_tokens),
        "line_body_edge_events_by_currier": {k: int(v) for k, v in events_by_label.items()},
        "previous_terminal_context_counts": {
            key: int(len(contexts[key])) for key in ("A", "B", "OTHER", "POOLED")
        },
        "previous_terminal_context_digests": {
            key: sha256_lines(context_ids[key]) for key in ("A", "B", "OTHER", "POOLED")
        },
        "outcome_blind_event_digests": {
            key: sha256_lines(event_ids[key]) for key in ("A", "B", "OTHER", "POOLED")
        },
        "fallback_policy_support": fallback,
    }


def split_audit(
    name: str,
    train_items,
    eval_items,
    parsed,
    by_doc: dict,
    expected_eval_targets: int | None = None,
) -> dict:
    train_leaves = sorted({int(it.leaf) for it in train_items})
    eval_leaves = sorted({int(it.leaf) for it in eval_items})
    overlap = sorted(set(train_leaves) & set(eval_leaves))
    support = support_audit(train_items, by_doc)
    eval_targets = accepted_target_count(eval_items, parsed)
    eval_visible = visible_token_count(eval_items)

    criteria = {
        "train_eval_leaf_disjoint": len(overlap) == 0,
        "nonempty_eval_target_population": eval_targets > 0,
        "nonempty_line_start_support": support["line_start_tokens"] > 0,
        "nonempty_line_body_support": support["line_body_edge_events"] > 0,
        "nonempty_A_edge_support": support["line_body_edge_events_by_currier"]["A"] > 0,
        "nonempty_B_edge_support": support["line_body_edge_events_by_currier"]["B"] > 0,
        "A_has_at_least_two_terminal_contexts": support["previous_terminal_context_counts"]["A"] >= 2,
        "B_has_at_least_two_terminal_contexts": support["previous_terminal_context_counts"]["B"] >= 2,
        "pooled_has_at_least_two_terminal_contexts": support["previous_terminal_context_counts"]["POOLED"] >= 2,
    }
    if expected_eval_targets is not None:
        criteria["eval_target_count_matches_core_authority"] = eval_targets == int(expected_eval_targets)

    return {
        "name": name,
        "train_leaf_count": int(len(train_leaves)),
        "eval_leaf_count": int(len(eval_leaves)),
        "train_leaf_digest": sha256_lines(str(x) for x in train_leaves),
        "eval_leaf_digest": sha256_lines(str(x) for x in eval_leaves),
        "leaf_overlap_count": int(len(overlap)),
        "eval_parser_accepted_targets": int(eval_targets),
        "eval_visible_tokens": int(eval_visible),
        "support": support,
        "criteria": criteria,
        "gate_pass": bool(all(criteria.values())),
    }


def audit(zl_path: Path) -> dict:
    # Reproduce only prior authorities before constructing any Issue #134 support.
    core = R.C1.run(zl_path)
    core_authority = R.verify_core_authority(core)
    if core_authority["normalized_sha256"] != EXPECTED_CORE_SHA:
        raise RuntimeError("corrected B3 normalized authority changed")

    currier_gate = CUR.audit(zl_path)
    currier_gate_sha = json_sha256(currier_gate)
    if currier_gate_sha != EXPECTED_CURRIER_EDGE_GATE_SHA:
        raise RuntimeError(
            f"Issue127 Currier edge Gate0 SHA mismatch: {currier_gate_sha} != {EXPECTED_CURRIER_EDGE_GATE_SHA}"
        )
    if not currier_gate["gate_pass"]:
        raise RuntimeError("Issue127 Currier edge Gate0 no longer passes")

    P1.I.ordered = OA.ordered
    vitems, folds, parsed = P1.I.C.load_corpus(zl_path)
    if P1.I.b.git_blob_sha1(zl_path.read_bytes()) != EXPECTED_SOURCE_BLOB:
        raise RuntimeError("frozen ZL3b source blob changed")
    if len(folds) != P1.N_FOLDS or len(folds) != 5:
        raise RuntimeError("physical-leaf fold count changed")
    if P1.P0.fold_hash(folds) != core["fold_identity_sha256"]:
        raise RuntimeError("fold identity changed")

    headers = CUR.G0.parse_source_headers(zl_path)
    by_doc = {r["document"]: r for r in headers}
    if len(by_doc) != len(headers):
        raise RuntimeError("duplicate document in Currier authority")

    outer = []
    inner = []
    for f in range(P1.N_FOLDS):
        outer_leaves = leaves_for_folds(folds, (f,))
        tr_outer = select_items(vitems, outer_leaves, include=False)
        ev_outer = select_items(vitems, outer_leaves, include=True)
        expected_n = int(core["outer"][f]["n_scored"])
        if expected_n != EXPECTED_OUTER_TARGET_COUNTS[f]:
            raise RuntimeError(f"corrected-core target-count authority changed fold={f}: {expected_n}")
        outer.append(
            split_audit(
                f"outer-{f}", tr_outer, ev_outer, parsed, by_doc,
                expected_eval_targets=expected_n,
            )
        )

        for g in range(P1.N_FOLDS):
            if g == f:
                continue
            excluded = leaves_for_folds(folds, (f, g))
            eval_g = leaves_for_folds(folds, (g,))
            tr_inner = select_items(vitems, excluded, include=False)
            ev_inner = select_items(vitems, eval_g, include=True)
            inner.append(
                split_audit(
                    f"outer-{f}-inner-{g}", tr_inner, ev_inner, parsed, by_doc
                )
            )

    all_splits = outer + inner
    gate_pass = bool(
        core_authority["valid"]
        and currier_gate["gate_pass"]
        and len(outer) == 5
        and len(inner) == 20
        and all(row["gate_pass"] for row in all_splits)
    )

    return {
        "schema": "issue134-augmented-core-gate0-v1",
        "phase": "ISSUE134_AUGMENTED_CORE_GATE0",
        "gate_pass": gate_pass,
        "gate_rule": "PROCEED_TO_COMMITTED_PREDICTIVE_SCORER" if gate_pass else "STOP_BEFORE_PREDICTIVE_SCORER",
        "source": {
            "git_blob_sha1": P1.I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": EXPECTED_SOURCE_BLOB,
        },
        "core_authority": core_authority,
        "fold_identity_sha256": core["fold_identity_sha256"],
        "currier_authority": {
            "issue127_gate0_json_sha256": currier_gate_sha,
            "expected_issue127_gate0_json_sha256": EXPECTED_CURRIER_EDGE_GATE_SHA,
            "gate_pass": bool(currier_gate["gate_pass"]),
            "phase3a_currier_authority": currier_gate["phase3a_currier_authority"],
        },
        "frozen_policy": {
            "edge_k": 2,
            "edge_alpha": 0.01,
            "currier_A_or_B": "same-regime previous-terminal table, else pooled previous-terminal table, else pooled LINE_BODY onset",
            "unknown_or_other": "pooled previous-terminal table, else pooled LINE_BODY onset",
            "hand_conditioning": False,
        },
        "outer_expected_target_counts": list(EXPECTED_OUTER_TARGET_COUNTS),
        "outer_splits": outer,
        "inner_splits": inner,
        "split_counts": {"outer": int(len(outer)), "inner": int(len(inner))},
        "firewall": {
            "new_issue134_edge_probabilities_computed": False,
            "new_issue134_challenger_probabilities_computed": False,
            "new_issue134_likelihoods_computed": False,
            "new_issue134_bits_per_token_computed": False,
            "new_issue134_residual_computed": False,
            "outer_outcomes_used_for_selection": False,
            "current_initial_outcomes_exposed": False,
            "latent_state_fit": False,
            "hand_conditioning_used": False,
            "surface_scorecard_used": False,
            "semantic_or_image_context_used": False,
        },
    }


def self_test() -> dict:
    if EXPECTED_CORE_SHA != R.EXPECTED_CORE_SHA:
        raise AssertionError("corrected-core SHA constant drifted")
    if EXPECTED_SOURCE_BLOB != P1.EXPECTED_ZL3B_BLOB:
        raise AssertionError("source blob constant drifted")
    if len(EXPECTED_OUTER_TARGET_COUNTS) != 5:
        raise AssertionError("outer target-count authority changed")
    if sha256_lines(["b", "a"]) != sha256_lines(["a", "b"]):
        raise AssertionError("support digest must be order-independent")
    if sha256_lines(["a"]) == sha256_lines(["b"]):
        raise AssertionError("support digest collision in self-test")
    return {
        "ok": True,
        "score_free": True,
        "corrected_core_authority_frozen": True,
        "currier_edge_gate_authority_frozen": True,
        "outer_target_counts_frozen": True,
        "outcome_blind_event_identity": True,
        "new_issue134_predictive_scores": 0,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--audit", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.audit is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    out = audit(Path(ns.audit[0]))
    Path(ns.audit[1]).write_text(canonical_json(out), encoding="utf-8")
    print(json.dumps({
        "gate_pass": out["gate_pass"],
        "gate_rule": out["gate_rule"],
        "core_authority": out["core_authority"],
        "currier_authority": out["currier_authority"],
        "split_counts": out["split_counts"],
        "outer_target_counts": [r["eval_parser_accepted_targets"] for r in out["outer_splits"]],
        "outer_support": [
            {
                "name": r["name"],
                "previous_terminal_context_counts": r["support"]["previous_terminal_context_counts"],
                "line_body_edge_events_by_currier": r["support"]["line_body_edge_events_by_currier"],
                "gate_pass": r["gate_pass"],
            }
            for r in out["outer_splits"]
        ],
        "firewall": out["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
