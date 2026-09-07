#!/usr/bin/env python3
"""Issue #191 Stage 0: score-free authority / firewall audit.

This executable MUST NOT open manuscript transcription files. It verifies only
frozen repository authorities, replays already-revealed OGH-C C0 facts, and
self-tests prospectively frozen helper definitions on synthetic toy data.

Scientific authority:
  research/ISSUE191_PRODUCTIVITY_STAGE0_PLAN_20260908.md
  GitHub Issue #191
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKER = "NO ISSUE191 NEW PRODUCTIVITY SCIENTIFIC RESULT COMPUTED"

AUTHORITIES = {
    "ogh_a": (
        "experiments/occupancy-generation-hierarchy/ogh_a.py",
        "396284f8b3c94bd4dcf8114bd7b5fb7233de821b",
    ),
    "ogh_b": (
        "experiments/occupancy-generation-hierarchy/ogh_b.py",
        "844d46ff685ef2d1abbc0c37dcb2f4b1fb75258f",
    ),
    "ogh_c": (
        "experiments/occupancy-generation-hierarchy/ogh_c.py",
        "742513b5ccfcd088e93b8e9480ac02cbc792e986",
    ),
    "report_c": (
        "experiments/occupancy-generation-hierarchy/REPORT_C.md",
        "03d14b586a004f365b97507bc5ad905dc771471a",
    ),
    "information_budget": (
        "experiments/occupancy-generation-hierarchy/stage-c0/information_budget.json",
        "2ba7f2a488c5302acc04b2c1dd3266ccd271f2f1",
    ),
    "slot_parser": (
        "experiments/issue26-music/issue26e_core.py",
        "8bafba7f2bce4cf77c9001c729936c1ce619759b",
    ),
    "phase58d": (
        "experiments/occupancy-graph-independent-transcription/phase58d_independent_residual.py",
        "161f721a325a53632f3d6d917ec5a27da48e2944",
    ),
    "preflight_zl": (
        "experiments/occupancy-generation-hierarchy/preflight/preflight_ZL3b.json",
        "123428983b10d1fee2b74056caa402d067d7b5ae",
    ),
    "preflight_it": (
        "experiments/occupancy-generation-hierarchy/preflight/preflight_IT2a.json",
        "15a206c85dd1fed4653881b17058640139405399",
    ),
    "admissible": (
        "experiments/occupancy-generation-hierarchy/preflight/admissible_signatures.json",
        "ee376d25b83c7ac79d82d1811c9557d193cf9227",
    ),
}

READ_ALLOWLIST = frozenset(path for path, _ in AUTHORITIES.values())
PATHS_READ: list[str] = []

RAREFACTION_FRACTIONS = (0.10, 0.25, 0.50, 0.75, 1.00)
C2_PERMUTATIONS = 1000
C3_REPS_PER_FOLD = 100
C2_NAMESPACE = "Issue191:C2:<reading>:perm:<i>"
C3_NAMESPACE = "Issue191:C3:<reading>:fold:<f>:rep:<r>"

EXPECTED_HISTORICAL = {
    "schema": "ogh-c-c0-v1",
    "folds": 5,
    "selected_content_grammar": "V2",
    "positive_folds": 5,
    "vplus_mean_oov_fraction": 0.07034275261192205,
    "heldout_parsed_by_fold": [4430, 4810, 5516, 5447, 4868],
    "parsed_total": 25071,
    "g7a_shape_bits_mean": 7.009998907083391,
    "v2_bits_mean": 9.708971376158532,
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def stable_seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8], "big")


def read_authority(key: str) -> bytes:
    rel, _ = AUTHORITIES[key]
    if rel not in READ_ALLOWLIST:
        raise RuntimeError(f"Stage0 read firewall denied: {rel}")
    PATHS_READ.append(rel)
    return (ROOT / rel).read_bytes()


def f_eq(a: float, b: float, tol: float = 1e-15) -> bool:
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)


# ---------------------------------------------------------------------------
# Prospectively frozen Stage-1 helper definitions. Stage 0 exercises toy data
# only. These functions do not read files.


def rarefaction_sample_size(n_total: int, fraction: float) -> int:
    if n_total <= 0:
        return 0
    if not (0.0 < fraction <= 1.0):
        raise ValueError(f"bad rarefaction fraction: {fraction}")
    return min(n_total, max(1, math.floor(fraction * n_total)))


def log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def expected_distinct_without_replacement(counts, sample_n: int) -> float:
    """Exact hypergeometric expectation, evaluated in floating log space."""
    counts = [int(c) for c in counts if int(c) > 0]
    N = sum(counts)
    if sample_n < 0 or sample_n > N:
        raise ValueError("sample_n outside population")
    if sample_n == 0:
        return 0.0
    den = log_choose(N, sample_n)
    total = 0.0
    for c in counts:
        if sample_n > N - c:
            p_unseen = 0.0
        else:
            p_unseen = math.exp(log_choose(N - c, sample_n) - den)
        total += 1.0 - p_unseen
    return total


def levenshtein_exactly_one(a: str, b: str) -> bool:
    """True iff ordinary character-level Levenshtein distance is exactly one."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    # len(b) == len(a) + 1; one insertion into a / deletion from b.
    i = 0
    while i < len(a) and a[i] == b[i]:
        i += 1
    return a[i:] == b[i + 1 :]


def canonical_shape(token_type) -> tuple[int, ...]:
    return tuple(int(slot) for slot, _value in token_type)


def canonical_surface(token_type) -> str:
    return "".join(str(value) for _slot, value in token_type)


def novelty_flags(novel_type, train_types) -> dict[str, bool]:
    train_types = {tuple(tuple(u) for u in t) for t in train_types}
    novel_type = tuple(tuple(u) for u in novel_type)
    if novel_type in train_types:
        raise ValueError("novelty_flags requires a training-unseen type")
    shape = canonical_shape(novel_type)
    train_shapes = {canonical_shape(t) for t in train_types}
    train_units = {tuple(u) for t in train_types for u in t}
    s = canonical_surface(novel_type)
    train_surfaces = {canonical_surface(t) for t in train_types}
    edit1 = any(levenshtein_exactly_one(s, x) for x in train_surfaces)
    known_shape = shape in train_shapes
    return {
        "KNOWN_SHAPE_NEW_VALUE_COMBINATION": known_shape,
        "NEW_OCCUPIED_SLOT_SHAPE": not known_shape,
        "ALL_COMPONENT_UNITS_SEEN": all(tuple(u) in train_units for u in novel_type),
        "EDIT1_FAMILY_INNOVATION": edit1,
        "OTHER_PARSER_ACCEPTED_INNOVATION": not edit1,
    }


def annotation_signature(flags: dict[str, bool]) -> tuple[str, ...]:
    return tuple(sorted(k for k, v in flags.items() if v))


def deterministic_permutation(n: int, namespace: str) -> list[int]:
    """SHA-256 rank permutation; avoids RNG-version drift in C2."""
    return sorted(
        range(n),
        key=lambda i: hashlib.sha256(f"{namespace}:token:{i}".encode("utf-8")).digest(),
    )


def c2_fold_assignment(fold_counts, namespace: str) -> list[int]:
    fold_counts = [int(x) for x in fold_counts]
    n = sum(fold_counts)
    order = deterministic_permutation(n, namespace)
    labels = [-1] * n
    at = 0
    for fold, count in enumerate(fold_counts):
        for idx in order[at : at + count]:
            labels[idx] = fold
        at += count
    if at != n or any(x < 0 for x in labels):
        raise RuntimeError("C2 assignment invariant failure")
    return labels


def linear_quantile(values, q: float) -> float:
    xs = sorted(float(x) for x in values)
    if not xs:
        raise ValueError("empty quantile")
    if not (0.0 <= q <= 1.0):
        raise ValueError("q outside [0,1]")
    p = (len(xs) - 1) * q
    lo, hi = math.floor(p), math.ceil(p)
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - p) + xs[hi] * (p - lo)


def helper_self_test() -> dict:
    # Rarefaction: population A,A,B,B; drawing one sees exactly one type.
    assert f_eq(expected_distinct_without_replacement([2, 2], 1), 1.0)
    assert f_eq(expected_distinct_without_replacement([2, 2], 4), 2.0)
    assert rarefaction_sample_size(101, 0.10) == 10
    assert rarefaction_sample_size(101, 1.00) == 101

    assert levenshtein_exactly_one("abc", "abd")
    assert levenshtein_exactly_one("abc", "abxc")
    assert levenshtein_exactly_one("abc", "ac")
    assert not levenshtein_exactly_one("abc", "abc")
    assert not levenshtein_exactly_one("abc", "axyd")

    train = {
        ((0, "q"), (1, "o")),
        ((0, "s"), (1, "o")),
        ((4, "ch"), (6, "e")),
    }
    f1 = novelty_flags(((0, "q"), (1, "y")), train)
    assert f1["KNOWN_SHAPE_NEW_VALUE_COMBINATION"]
    assert f1["ALL_COMPONENT_UNITS_SEEN"] is False
    assert f1["EDIT1_FAMILY_INNOVATION"]
    f2 = novelty_flags(((0, "q"), (6, "e")), train)
    assert f2["NEW_OCCUPIED_SLOT_SHAPE"]
    assert f2["ALL_COMPONENT_UNITS_SEEN"]

    labels = c2_fold_assignment([2, 3, 1], "Issue191:C2:TOY:perm:0")
    assert [labels.count(f) for f in range(3)] == [2, 3, 1]
    assert len(set(deterministic_permutation(20, "a"))) == 20
    assert stable_seed("Issue191:C3:ZL3b:fold:0:rep:0") != stable_seed(
        "Issue191:C3:ZL3b:fold:0:rep:1"
    )
    assert f_eq(linear_quantile([0, 1, 2, 3, 4], 0.5), 2.0)
    return {
        "rarefaction": "PASS",
        "edit_distance": "PASS",
        "annotations": "PASS",
        "c2_assignment": "PASS",
        "seed_namespaces": "PASS",
        "linear_quantile": "PASS",
    }


# ---------------------------------------------------------------------------


def ast_named_assignment(tree: ast.AST, name: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return node.value
    raise KeyError(name)


def class_methods(tree: ast.AST, class_name: str) -> set[str]:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {x.name for x in node.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))}
    return set()


def run() -> dict:
    checks = []

    def check(name: str, ok: bool, detail=None):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    authority_bytes = {}
    for key, (rel, expected) in AUTHORITIES.items():
        try:
            raw = read_authority(key)
            got = git_blob_sha1(raw)
            authority_bytes[key] = raw
            check(f"blob:{key}", got == expected, {"path": rel, "expected": expected, "actual": got})
        except Exception as exc:  # preserve an auditable false admission rather than crashing
            check(f"blob:{key}", False, {"path": rel, "error": repr(exc)})

    # Parser invariants, statically inspected: no module import and no data load.
    try:
        parser_src = authority_bytes["slot_parser"].decode("utf-8")
        parser_tree = ast.parse(parser_src)
        slots = ast.literal_eval(ast_named_assignment(parser_tree, "SLOTS"))
        methods = class_methods(parser_tree, "SlotParser")
        check("parser:12_slots", len(slots) == 12, len(slots))
        check("parser:33_units", sum(len(x) for x in slots) == 33, sum(len(x) for x in slots))
        check("parser:methods", {"parses", "pick"}.issubset(methods) and "def validate_parser" in parser_src, sorted(methods))
        check("parser:stable_seed_sha256", "hashlib.sha256(label.encode()).digest()[:8]" in parser_src, None)
    except Exception as exc:
        check("parser:static_invariants", False, repr(exc))

    try:
        a = authority_bytes["ogh_a"].decode("utf-8")
        check("ogh_a:five_folds", "N_FOLDS = 5" in a, None)
        check("ogh_a:12_slots", "N_SLOTS = 12" in a, None)
        check("ogh_a:parser_import", "import issue26e_core as e" in a, None)
        check("ogh_a:phase58d_import", "import phase58d_independent_residual as d58" in a, None)
        check("ogh_a:it_loader", "d58.build_it_dataset" in a, None)
    except Exception as exc:
        check("ogh_a:static_invariants", False, repr(exc))

    try:
        b = authority_bytes["ogh_b"].decode("utf-8")
        check("ogh_b:g7a", "def fit_g7a" in b and "ELL1, ELL2 = state_contexts()" in b, None)
        check("ogh_b:backoff", "BACKOFF = 1.0" in b, None)
    except Exception as exc:
        check("ogh_b:static_invariants", False, repr(exc))

    try:
        c = authority_bytes["ogh_c"].decode("utf-8")
        required = [
            "UNITS = [(s, v) for s in range(12) for v in e.SLOTS[s]]",
            "def token_units",
            "class V2Model",
            "class VPlusModel",
            'selected = "V2" if positive >= 4 else "V1"',
        ]
        check("ogh_c:v2_vplus_identity", all(x in c for x in required), required)
    except Exception as exc:
        check("ogh_c:static_invariants", False, repr(exc))

    try:
        d = authority_bytes["phase58d"].decode("utf-8")
        required = [
            "N_FOLDS = 5",
            'IT_BLOB = "4d6d3f2537b1f507a257529b49c94af7d6e03446"',
            'ZL_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"',
            "len(set().union(*folds)) != 99",
            "def frozen_folds_from_zl",
            "def build_it_dataset",
        ]
        check("phase58d:common_representation", all(x in d for x in required), required)
    except Exception as exc:
        check("phase58d:static_invariants", False, repr(exc))

    # Historical replay only: values were already exposed by OGH-C.
    historical = {}
    try:
        info = json.loads(authority_bytes["information_budget"].decode("utf-8"))
        fold_keys = sorted(info["folds"], key=int)
        heldout = [int(info["folds"][k]["n_heldout_tokens"]) for k in fold_keys]
        vplus_oov = [float(info["folds"][k]["models"]["V+"]["oov_fraction"]) for k in fold_keys]
        historical = {
            "schema": info.get("schema"),
            "fold_count": len(fold_keys),
            "selected_content_grammar": info["selection"]["selected_content_grammar"],
            "positive_folds": int(info["selection"]["positive_folds"]),
            "vplus_oov_by_fold": vplus_oov,
            "vplus_mean_oov_fraction": float(info["summary"]["V+_mean_oov_fraction"]),
            "heldout_parsed_by_fold": heldout,
            "parsed_total": sum(heldout),
            "g7a_shape_bits_mean": float(info["summary"]["shape_only_G7A"]["mean_bits_per_token"]),
            "v2_bits_mean": float(info["summary"]["V2"]["mean_bits_per_token_covered"]),
        }
        check("history:schema", historical["schema"] == EXPECTED_HISTORICAL["schema"], historical["schema"])
        check("history:five_folds", historical["fold_count"] == EXPECTED_HISTORICAL["folds"], historical["fold_count"])
        check("history:v2_selected", historical["selected_content_grammar"] == "V2" and historical["positive_folds"] == 5, {"selected": historical["selected_content_grammar"], "positive_folds": historical["positive_folds"]})
        check("history:fold_support", heldout == EXPECTED_HISTORICAL["heldout_parsed_by_fold"], heldout)
        check("history:parsed_total", historical["parsed_total"] == EXPECTED_HISTORICAL["parsed_total"], historical["parsed_total"])
        check("history:vplus_mean_oov", f_eq(historical["vplus_mean_oov_fraction"], EXPECTED_HISTORICAL["vplus_mean_oov_fraction"]), historical["vplus_mean_oov_fraction"])
        check("history:g7a_bits", f_eq(historical["g7a_shape_bits_mean"], EXPECTED_HISTORICAL["g7a_shape_bits_mean"]), historical["g7a_shape_bits_mean"])
        check("history:v2_bits", f_eq(historical["v2_bits_mean"], EXPECTED_HISTORICAL["v2_bits_mean"]), historical["v2_bits_mean"])
    except Exception as exc:
        check("history:replay", False, repr(exc))

    try:
        admissible = json.loads(authority_bytes["admissible"].decode("utf-8"))
        check("admissible:4077", int(admissible["n_admissible"]) == 4077, admissible.get("n_admissible"))
        check("admissible:12bit_space", int(admissible["n_total_nonempty"]) == 4095, admissible.get("n_total_nonempty"))
    except Exception as exc:
        check("admissible:content", False, repr(exc))

    try:
        toy = helper_self_test()
        check("helpers:toy_self_test", True, toy)
    except Exception as exc:
        check("helpers:toy_self_test", False, repr(exc))
        toy = {"status": "FAIL", "error": repr(exc)}

    # Explicit read firewall: only the ten frozen non-manuscript authority files.
    unique_reads = sorted(set(PATHS_READ))
    check("firewall:only_allowlisted_files_read", set(unique_reads).issubset(READ_ALLOWLIST), unique_reads)
    check("firewall:all_authorities_read", set(unique_reads) == READ_ALLOWLIST, unique_reads)

    stage1_licensed = all(x["ok"] for x in checks)
    return {
        "schema": "issue191-productivity-stage0-v1",
        "issue": 191,
        "marker": MARKER,
        "scientific_score_computed": False,
        "new_productivity_score_computed": False,
        "manuscript_transcription_opened": False,
        "stage1_licensed": stage1_licensed,
        "checks": checks,
        "historical_replay_only": historical,
        "frozen_stage1_config": {
            "canonical_type": "ordered SlotParser(min) (slot,value) unit sequence",
            "rarefaction_fractions": list(RAREFACTION_FRACTIONS),
            "rarefaction_sample_size": "max(1,floor(q*N)), capped at N",
            "rarefaction_statistic": "sum_t [1-C(N-c_t,n)/C(N,n)]",
            "edit_distance": "ordinary character-level Levenshtein distance exactly 1 on canonical surfaces",
            "c2_permutations": C2_PERMUTATIONS,
            "c2_namespace": C2_NAMESPACE,
            "c2_permutation_algorithm": "sort token indices by SHA256(namespace + ':token:' + index)",
            "c2_pvalue": "(1 + count(null >= observed))/1001",
            "c3_v2_reps_per_fold": C3_REPS_PER_FOLD,
            "c3_namespace": C3_NAMESPACE,
            "c3_rng": "numpy.default_rng(stable_seed(namespace)); stable_seed = first 8 SHA256 bytes, big-endian",
            "c3_interval": "central 95% empirical [q0.025,q0.975], linear interpolation",
            "annotation_labels": [
                "KNOWN_SHAPE_NEW_VALUE_COMBINATION",
                "NEW_OCCUPIED_SLOT_SHAPE",
                "ALL_COMPONENT_UNITS_SEEN",
                "EDIT1_FAMILY_INNOVATION",
                "OTHER_PARSER_ACCEPTED_INNOVATION",
            ],
        },
        "helper_self_test": toy,
        "read_firewall": {
            "allowed_paths": sorted(READ_ALLOWLIST),
            "paths_read": unique_reads,
        },
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
