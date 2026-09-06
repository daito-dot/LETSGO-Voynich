#!/usr/bin/env python3
"""Issue #139 Gate0: score-free IT2a source/fold/support audit.

This executable is deliberately incapable of computing POS2/EDGE2
probabilities, log likelihoods, code lengths, gains, or a scientific result.
It verifies only frozen source identity, parser authority, fold identity,
population counts, literal byte representability, and finite support.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable, Sequence

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PHASE63_DIR = ROOT / "experiments" / "phase63"
ISSUE26_DIR = ROOT / "experiments" / "issue26-music"
if str(PHASE63_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE63_DIR))
if str(ISSUE26_DIR) not in sys.path:
    sys.path.insert(0, str(ISSUE26_DIR))

import phase63b_common as p63  # noqa: E402
import issue26e_core as e  # noqa: E402

P63_PATH = ROOT / "experiments" / "phase63" / "phase63b_common.py"
SLOT_PATH = ROOT / "experiments" / "issue26-music" / "issue26e_core.py"
AUDIT_PATH = (
    ROOT
    / "experiments"
    / "occupancy-graph-independent-transcription"
    / "source-audit"
    / "issue66_source_audit.json"
)

EXPECTED = {
    "source": {
        "sha256": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
        "git_blob_sha1": "4d6d3f2537b1f507a257529b49c94af7d6e03446",
        "byte_size": 342104,
        "line_count": 5444,
        "header": "#=IVTFF EvaT 2.0 M 3",
    },
    "repo_blobs": {
        "phase63b_common.py": "99cc6d49669c67432b4798b81c8250a17b3fbb38",
        "issue26e_core.py": "8bafba7f2bce4cf77c9001c729936c1ce619759b",
        "issue66_source_audit.json": "85c172c113927b91215463ee9297630580b57769",
    },
    "audit_sha256": "bed86e92fcb854b614dfb474cd3bab9e6fc1e5746399fc14bced9f8e4448eddf",
    "P_loci": 4118,
    "paragraphs": 772,
    "pages": 206,
    "physical_leaves": 99,
    "clean_tokens": 34411,
    "excluded_uncertain_tokens": 80,
    "accepted_tokens": 28280,
    "rejected_tokens": 6131,
    "ambiguous_tokens": 9492,
    "minmax_different_tokens": 9492,
    "fold_clean": [6102, 6692, 7528, 7484, 6605],
    "fold_accepted": [4976, 5416, 6261, 6197, 5430],
    "min_test_accepted": 300,
    "min_test_line_body_accepted": 300,
}

FORBIDDEN_SCIENCE = (
    "POS2_probability",
    "EDGE2_probability",
    "log_likelihood",
    "bits_per_token",
    "G_identity_IT2a",
    "scientific_classification",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def source_identity(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig", errors="strict")
    lines = text.splitlines()
    got = {
        "sha256": sha256_bytes(raw),
        "git_blob_sha1": git_blob_sha1(raw),
        "byte_size": len(raw),
        "line_count": len(lines),
        "header": lines[0].strip() if lines else "",
    }
    if got != EXPECTED["source"]:
        raise RuntimeError(f"IT2a source identity mismatch: {got}")
    return got


def verify_repo_authorities() -> dict:
    paths = {
        "phase63b_common.py": P63_PATH,
        "issue26e_core.py": SLOT_PATH,
        "issue66_source_audit.json": AUDIT_PATH,
    }
    out = {}
    for label, path in paths.items():
        if not path.is_file():
            raise RuntimeError(f"missing frozen repository authority: {path}")
        blob = git_blob_sha1(path.read_bytes())
        exp = EXPECTED["repo_blobs"][label]
        if blob != exp:
            raise RuntimeError(f"repository authority drift for {label}: {blob} != {exp}")
        out[label] = {"path": str(path.relative_to(ROOT)), "git_blob_sha1": blob}
    audit_sha = sha256_bytes(AUDIT_PATH.read_bytes())
    if audit_sha != EXPECTED["audit_sha256"]:
        raise RuntimeError(f"Issue66 audit SHA drift: {audit_sha}")
    out["issue66_source_audit.json"]["sha256"] = audit_sha
    return out


def load_frozen_folds() -> tuple[list[set[int]], dict]:
    authority = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    if authority.get("scientific_pair_or_residual_metrics_computed") is not False:
        raise RuntimeError("Issue66 source audit firewall is not intact")
    if authority.get("IT2a", {}).get("disposition") != "AUTHORIZED_FOR_TARGET_PLAN":
        raise RuntimeError("Issue66 did not authorize IT2a target planning")

    archived_identity = authority["IT2a"]["identity"]
    for key, expected in EXPECTED["source"].items():
        if archived_identity.get(key) != expected:
            raise RuntimeError(f"Issue66 archived IT2a identity mismatch at {key}")

    folds_raw = authority["frozen_reference"]["fold_leaf_sets"]
    if len(folds_raw) != 5:
        raise RuntimeError(f"expected five frozen folds, got {len(folds_raw)}")
    folds = [set(map(int, fold)) for fold in folds_raw]
    union: set[int] = set()
    for i, fold in enumerate(folds):
        if not fold:
            raise RuntimeError(f"empty frozen fold {i}")
        overlap = union & fold
        if overlap:
            raise RuntimeError(f"frozen fold overlap at fold {i}: {sorted(overlap)}")
        union.update(fold)
    if len(union) != EXPECTED["physical_leaves"]:
        raise RuntimeError(f"frozen leaf universe size changed: {len(union)}")

    shared = authority["IT2a"]["shared_universe"]
    if list(map(int, shared["fold_clean_tokens"])) != EXPECTED["fold_clean"]:
        raise RuntimeError("Issue66 archived clean fold support changed")
    if list(map(int, shared["fold_accepted_tokens"])) != EXPECTED["fold_accepted"]:
        raise RuntimeError("Issue66 archived accepted fold support changed")
    if int(shared["shared_physical_leaves"]) != EXPECTED["physical_leaves"]:
        raise RuntimeError("Issue66 shared leaf count changed")
    if set(map(int, shared["shared_leaf_numbers"])) != union:
        raise RuntimeError("Issue66 shared leaf universe differs from fold authority")
    return folds, authority


def token_text(tok: Sequence[str]) -> str:
    return "".join(tok)


def token_raw_bytes(tok: Sequence[str]) -> bytes:
    raw = token_text(tok).encode("utf-8")
    if not raw:
        raise RuntimeError("empty literal token byte sequence")
    return raw


def fold_map(folds: Sequence[set[int]]) -> dict[int, int]:
    out = {}
    for f, fold in enumerate(folds):
        for leaf in fold:
            if leaf in out:
                raise RuntimeError(f"duplicate leaf in fold map: {leaf}")
            out[int(leaf)] = int(f)
    return out


def count_population(paragraphs, folds: Sequence[set[int]], parser) -> dict:
    leaf_to_fold = fold_map(folds)
    clean_fold = [0] * 5
    accepted_fold = [0] * 5
    accepted_line_start_fold = [0] * 5
    accepted_line_body_fold = [0] * 5
    clean_line_start_fold = [0] * 5
    clean_line_body_fold = [0] * 5
    clean_total = 0
    accepted_total = 0
    ambiguous_total = 0
    minmax_diff_total = 0
    serialized_utf8_bytes = 0
    observed_leaves = set()
    observed_pages = set()
    nonempty_source_lines = 0
    paragraph_without_frozen_leaf = 0

    for paragraph in paragraphs:
        observed_pages.add(paragraph.page)
        if paragraph.leaf is None:
            paragraph_without_frozen_leaf += 1
            continue
        leaf = int(paragraph.leaf)
        observed_leaves.add(leaf)
        if leaf not in leaf_to_fold:
            raise RuntimeError(f"IT2a contains leaf outside frozen universe: {leaf}")
        f = leaf_to_fold[leaf]
        for line in paragraph.lines:
            if not line:
                raise RuntimeError("Phase63 parser emitted an empty retained source line")
            nonempty_source_lines += 1
            for ti, tok in enumerate(line):
                raw = token_raw_bytes(tok)
                serialized_utf8_bytes += len(raw)
                clean_total += 1
                clean_fold[f] += 1
                if ti == 0:
                    clean_line_start_fold[f] += 1
                else:
                    clean_line_body_fold[f] += 1
                parses = parser.parses(token_text(tok))
                if len(parses) > 1:
                    ambiguous_total += 1
                if parses:
                    accepted_total += 1
                    accepted_fold[f] += 1
                    if ti == 0:
                        accepted_line_start_fold[f] += 1
                    else:
                        accepted_line_body_fold[f] += 1
                    if parses[0] != parses[-1]:
                        minmax_diff_total += 1

    if paragraph_without_frozen_leaf:
        raise RuntimeError(
            f"paragraphs without frozen physical leaf: {paragraph_without_frozen_leaf}"
        )

    return {
        "paragraphs": len(paragraphs),
        "pages": len(observed_pages),
        "physical_leaves": len(observed_leaves),
        "observed_leaf_numbers": sorted(observed_leaves),
        "nonempty_source_lines": nonempty_source_lines,
        "clean_tokens": clean_total,
        "accepted_tokens": accepted_total,
        "rejected_tokens": clean_total - accepted_total,
        "ambiguous_tokens_more_than_one_parse": ambiguous_total,
        "tokens_where_minmax_parse_differ": minmax_diff_total,
        "serialized_utf8_bytes_before_END_TOKEN": serialized_utf8_bytes,
        "fold_clean_tokens": clean_fold,
        "fold_accepted_tokens": accepted_fold,
        "fold_clean_line_start_tokens": clean_line_start_fold,
        "fold_clean_line_body_tokens": clean_line_body_fold,
        "fold_accepted_line_start_tokens": accepted_line_start_fold,
        "fold_accepted_line_body_tokens": accepted_line_body_fold,
    }


def training_support(paragraphs, folds: Sequence[set[int]]) -> list[dict]:
    all_leaves = set().union(*folds)
    out = []
    for outer_f, test_leaves in enumerate(folds):
        train_leaves = all_leaves - test_leaves
        if train_leaves & test_leaves:
            raise RuntimeError(f"train/test leaf overlap in fold {outer_f}")
        line_start_tokens = 0
        line_body_tokens = 0
        previous_terminal_contexts: set[int] = set()
        terminal_to_initial_pairs: set[tuple[int, int]] = set()
        training_token_count = 0

        for paragraph in paragraphs:
            if paragraph.leaf is None or int(paragraph.leaf) not in train_leaves:
                continue
            for line in paragraph.lines:
                previous_raw: bytes | None = None
                for ti, tok in enumerate(line):
                    raw = token_raw_bytes(tok)
                    training_token_count += 1
                    if ti == 0:
                        line_start_tokens += 1
                        if previous_raw is not None:
                            raise RuntimeError("source-line hard-reset invariant failed")
                    else:
                        if previous_raw is None:
                            raise RuntimeError("missing clean previous token in line body")
                        line_body_tokens += 1
                        prev_terminal = int(previous_raw[-1])
                        current_initial = int(raw[0])
                        previous_terminal_contexts.add(prev_terminal)
                        terminal_to_initial_pairs.add((prev_terminal, current_initial))
                    previous_raw = raw

        if line_start_tokens <= 0 or line_body_tokens <= 0:
            raise RuntimeError(f"degenerate onset support in outer fold {outer_f}")
        if len(previous_terminal_contexts) < 2:
            raise RuntimeError(f"degenerate previous-terminal support in outer fold {outer_f}")
        if len(terminal_to_initial_pairs) < 2:
            raise RuntimeError(f"degenerate terminal→initial pair support in outer fold {outer_f}")

        out.append(
            {
                "outer_fold": outer_f,
                "test_leaves": sorted(test_leaves),
                "train_leaf_count": len(train_leaves),
                "test_leaf_count": len(test_leaves),
                "train_test_leaf_overlap": [],
                "training_clean_tokens": training_token_count,
                "training_line_start_tokens": line_start_tokens,
                "training_line_body_tokens": line_body_tokens,
                "unique_previous_terminal_byte_contexts": len(previous_terminal_contexts),
                "unique_previous_terminal_to_initial_byte_pairs": len(terminal_to_initial_pairs),
            }
        )
    return out


def assert_expected_population(pop: dict, folds: Sequence[set[int]], parser_audit: dict) -> None:
    checks = {
        "P_loci": int(parser_audit["P_loci_seen"]),
        "paragraphs": int(pop["paragraphs"]),
        "pages": int(pop["pages"]),
        "physical_leaves": int(pop["physical_leaves"]),
        "clean_tokens": int(pop["clean_tokens"]),
        "excluded_uncertain_tokens": int(parser_audit["excluded_uncertain_or_unreadable_tokens"]),
        "accepted_tokens": int(pop["accepted_tokens"]),
        "rejected_tokens": int(pop["rejected_tokens"]),
        "ambiguous_tokens": int(pop["ambiguous_tokens_more_than_one_parse"]),
        "minmax_different_tokens": int(pop["tokens_where_minmax_parse_differ"]),
    }
    for key, got in checks.items():
        expected = int(EXPECTED[key])
        if got != expected:
            raise RuntimeError(f"population regression at {key}: {got} != {expected}")
    if list(pop["fold_clean_tokens"]) != EXPECTED["fold_clean"]:
        raise RuntimeError(f"clean fold support regression: {pop['fold_clean_tokens']}")
    if list(pop["fold_accepted_tokens"]) != EXPECTED["fold_accepted"]:
        raise RuntimeError(f"accepted fold support regression: {pop['fold_accepted_tokens']}")
    if set(pop["observed_leaf_numbers"]) != set().union(*folds):
        raise RuntimeError("IT2a observed leaves differ from frozen fold universe")
    for f in range(5):
        if int(pop["fold_accepted_tokens"][f]) < EXPECTED["min_test_accepted"]:
            raise RuntimeError(f"insufficient accepted support in test fold {f}")
        if int(pop["fold_accepted_line_body_tokens"][f]) < EXPECTED["min_test_line_body_accepted"]:
            raise RuntimeError(f"insufficient accepted line-body support in test fold {f}")


def run_gate(it2a_path: Path) -> dict:
    code_authority = verify_repo_authorities()
    source = source_identity(it2a_path)
    folds, archived = load_frozen_folds()

    paragraphs, parser_audit = p63.parse_ivtff(it2a_path, "IT2a", "W1")
    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)
    population = count_population(paragraphs, folds, parser)
    assert_expected_population(population, folds, parser_audit)
    support = training_support(paragraphs, folds)

    archived_pop = archived["IT2a"]["population"]
    if int(archived_pop["slot_parser_accepted_tokens"]) != population["accepted_tokens"]:
        raise RuntimeError("Issue66 accepted-target authority no longer reproduces")
    if int(archived_pop["clean_tokens"]) != population["clean_tokens"]:
        raise RuntimeError("Issue66 clean population no longer reproduces")

    return {
        "schema": "issue139-it2a-edge-gate0-v1",
        "issue": 139,
        "phase": "IT2A_EDGE_REPLICATION_GATE0",
        "gate_pass": True,
        "gate_disposition": "PASS — PROCEED TO SEPARATELY COMMITTED FROZEN IT2A EDGE SCORER",
        "scientific_edge_metrics_computed": False,
        "source": source,
        "repository_authority": code_authority,
        "source_parser_audit": parser_audit,
        "slot_parser_validation": parser_validation,
        "frozen_fold_leaf_sets": [sorted(fold) for fold in folds],
        "population": population,
        "outer_training_support": support,
        "representation_contract": {
            "view": "W1",
            "literal_token_bytes": "UTF-8 bytes of unchanged Phase63 W1 token string",
            "END_TOKEN": 256,
            "BOS": -1,
            "outcome_vocabulary_size": 257,
            "fixed_k": 2,
            "fixed_alpha": 0.01,
            "source_line_hard_reset": True,
            "previous_token_may_be_primary_target_rejected": True,
            "primary_current_token_requires_slot_parse": True,
            "unseen_context_policy": "additive smoothing on empty exact context; no pooled backoff",
        },
        "firewall": {
            "target_driven_normalization": False,
            "target_driven_exclusion": False,
            "target_driven_fold_change": False,
            "target_driven_smoothing_or_fallback": False,
            "target_driven_model_family_change": False,
            "currier_hand_section_conditioning": False,
            "latent_state_fit": False,
            "S1_S2_H62_R1_tuning": False,
            "scientific_edge_metrics_computed": False,
            "forbidden_scientific_metric_names": list(FORBIDDEN_SCIENCE),
        },
    }


def self_test() -> dict:
    a = b"abc"
    expected_blob = hashlib.sha1(b"blob 3\0abc").hexdigest()
    if git_blob_sha1(a) != expected_blob:
        raise AssertionError("Git blob SHA helper failed")
    if token_raw_bytes(("a", "b")) != b"ab":
        raise AssertionError("literal token serialization failed")
    folds = [{1, 6}, {2, 7}, {3, 8}, {4, 9}, {5, 10}]
    fm = fold_map(folds)
    if len(fm) != 10 or fm[7] != 1:
        raise AssertionError("synthetic fold map failed")
    return {
        "ok": True,
        "scientific_edge_metrics_computed": False,
        "target_source_loaded": False,
        "fixed_k": 2,
        "fixed_alpha": 0.01,
        "outcome_vocabulary_size": 257,
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
        result = run_gate(it2a_path)
        rc = 0
    except Exception as exc:
        result = {
            "schema": "issue139-it2a-edge-gate0-v1",
            "issue": 139,
            "phase": "IT2A_EDGE_REPLICATION_GATE0",
            "gate_pass": False,
            "gate_disposition": "INVALID INDEPENDENT REPLICATION — GATE0 FAILED",
            "scientific_edge_metrics_computed": False,
            "error": f"{type(exc).__name__}: {exc}",
            "firewall": {
                "scientific_edge_metrics_computed": False,
                "forbidden_scientific_metric_names": list(FORBIDDEN_SCIENCE),
            },
        }
        rc = 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
