#!/usr/bin/env python3
"""Issue #191 Stage 1: preregistered held-out productivity first reveal.

Scientific authorities:
  GitHub Issue #191
  research/ISSUE191_PRODUCTIVITY_STAGE0_PLAN_20260908.md
  research/ISSUE191_PRODUCTIVITY_STAGE1_PLAN_20260908.md

No scientific threshold or model choice is selected in this executable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
ROOT = HERE.parents[2]
for rel in (
    "issue191-productivity",
    "issue26-music",
    "phase62",
    "phase63",
    "occupancy-generation-hierarchy",
    "occupancy-graph-independent-transcription",
):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import issue191_stage0 as S0  # noqa: E402
import issue26e_core as e  # noqa: E402
import phase63b_common as p63  # noqa: E402
import phase58d_independent_residual as d58  # noqa: E402
import ogh_c as C  # noqa: E402


SCHEMA = "issue191-productivity-stage1-v1"
READINGS = ("ZL3b", "IT2a")
N_FOLDS = 5
C2_REPS = 1000
C3_REPS = 100
C2_ALPHA = 0.01
V2_RATIO_BAND = (0.5, 2.0)

ZL_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
ZL_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
IT_SHA256 = "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"
IT_BLOB = "4d6d3f2537b1f507a257529b49c94af7d6e03446"

EXPECTED_ZL_ACCEPTED = [4430, 4810, 5516, 5447, 4868]
EXPECTED_ZL_TOTAL = 25071
EXPECTED_ZL_HISTORICAL_OOV = [
    0.07652370203160275,
    0.07567567567567568,
    0.06617113850616385,
    0.06370479162841935,
    0.06963845521774858,
]
EXPECTED_ZL_HISTORICAL_MEAN_OOV = 0.07034275261192205
EXPECTED_IT_VISIBLE = 34411
EXPECTED_IT_ACCEPTED = 28280
EXPECTED_IT_REJECTED = 6131
EXPECTED_IT_FOLD_ACCEPTED = [4976, 5416, 6261, 6197, 5430]
EXPECTED_SUPPORT_RAW_SHA256 = "35ea31eb5d0a1f0484623ee8a29058f1c5bc339117e378b594f26c7c23aee0dc"

REPO_AUTHORITIES = {
    "stage0_helpers": (
        "experiments/issue191-productivity/issue191_stage0.py",
        "3bb6361f721e9cb8069846a79549652596aa287f",
    ),
    "zl_parser": (
        "experiments/phase62/phase62b_n0.py",
        "e0ada366845c7a6c5a5dd75de91fe262b72a94b6",
    ),
    "it_parser": (
        "experiments/phase63/phase63b_common.py",
        "99cc6d49669c67432b4798b81c8250a17b3fbb38",
    ),
    "support_audit": (
        "experiments/occupancy-graph-independent-transcription/source-audit/issue66_source_audit_support_complete.json",
        "5de44d197ec60129d3df0bdcc95354b3dd38ba42",
    ),
    "ogh_c": (
        "experiments/occupancy-generation-hierarchy/ogh_c.py",
        "742513b5ccfcd088e93b8e9480ac02cbc792e986",
    ),
    "slot_parser": (
        "experiments/issue26-music/issue26e_core.py",
        "8bafba7f2bce4cf77c9001c729936c1ce619759b",
    ),
    "phase58d": (
        "experiments/occupancy-graph-independent-transcription/phase58d_independent_residual.py",
        "161f721a325a53632f3d6d917ec5a27da48e2944",
    ),
    "historical_source_workflow": (
        ".github/workflows/issue115-phase4b-it2a-gate0.yml",
        "b715fced15212861618b03fbfe220030e5c5f8de",
    ),
}

ANNOTATION_LABELS = (
    "KNOWN_SHAPE_NEW_VALUE_COMBINATION",
    "NEW_OCCUPIED_SLOT_SHAPE",
    "ALL_COMPONENT_UNITS_SEEN",
    "EDIT1_FAMILY_INNOVATION",
    "OTHER_PARSER_ACCEPTED_INNOVATION",
)

TokenType = Tuple[Tuple[int, str], ...]


class ProtocolInvalid(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require(cond: bool, message: str) -> None:
    if not cond:
        raise ProtocolInvalid(message)


def verify_repo_authorities() -> dict:
    out = {}
    for role, (rel, expected) in REPO_AUTHORITIES.items():
        data = (ROOT / rel).read_bytes()
        got = git_blob_sha1(data)
        require(got == expected, f"repository authority mismatch {role}: {got} != {expected}")
        out[role] = {"path": rel, "git_blob_sha1": got}
    raw_support = (ROOT / REPO_AUTHORITIES["support_audit"][0]).read_bytes()
    support_sha = sha256_bytes(raw_support)
    require(support_sha == EXPECTED_SUPPORT_RAW_SHA256, "support audit raw SHA-256 mismatch")
    out["support_audit"]["sha256"] = support_sha
    return out


def source_identity(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "sha256": sha256_bytes(data),
        "git_blob_sha1": git_blob_sha1(data),
        "byte_size": len(data),
        "line_count": len(data.splitlines()),
        "first_line": data.decode("utf-8-sig", errors="strict").splitlines()[0].strip(),
    }


def canonical_from_int(seq: Sequence[int]) -> TokenType:
    return tuple((int(C.UNITS[int(u)][0]), str(C.UNITS[int(u)][1])) for u in seq)


def canonical_from_pick(picked) -> TokenType:
    sig, vals = picked
    return tuple((int(s), str(vals[s])) for s in sig)


def int_from_canonical(t: TokenType) -> tuple[int, ...]:
    try:
        return tuple(int(C.UNIT_INDEX[(int(s), str(v))]) for s, v in t)
    except KeyError as exc:
        raise ProtocolInvalid(f"canonical unit missing from frozen OGH-C inventory: {exc}") from exc


def type_surface(t: TokenType) -> str:
    return "".join(v for _s, v in t)


def type_shape(t: TokenType) -> tuple[int, ...]:
    return tuple(s for s, _v in t)


def expected_subset_distinct(counts: Iterable[int], population_n: int, sample_n: int) -> float:
    """Expected discovered count for a selected subset of types in a full population."""
    counts = [int(c) for c in counts if int(c) > 0]
    require(0 <= sample_n <= population_n, "rarefaction sample outside population")
    if sample_n == 0 or not counts:
        return 0.0
    den = S0.log_choose(population_n, sample_n)
    ans = 0.0
    for c in counts:
        require(c <= population_n, "type count exceeds rarefaction population")
        if sample_n > population_n - c:
            p_unseen = 0.0
        else:
            p_unseen = math.exp(S0.log_choose(population_n - c, sample_n) - den)
            p_unseen = min(1.0, max(0.0, p_unseen))
        ans += 1.0 - p_unseen
    return float(ans)


class NoveltyIndex:
    """Efficient implementation of the Stage-0 non-exclusive annotations."""

    def __init__(self, train_types: Iterable[TokenType]):
        self.train_types = set(train_types)
        self.train_shapes = {type_shape(t) for t in self.train_types}
        self.train_units = {u for t in self.train_types for u in t}
        self.train_surfaces = {type_surface(t) for t in self.train_types}
        self.same_len_patterns = set()
        self.train_deletions = set()
        for s in self.train_surfaces:
            for i in range(len(s)):
                self.same_len_patterns.add((len(s), i, s[:i], s[i + 1 :]))
                self.train_deletions.add(s[:i] + s[i + 1 :])

    def edit1(self, s: str) -> bool:
        # Novel canonical surfaces cannot equal a training canonical surface;
        # guard anyway to preserve exact distance-one semantics.
        if s in self.train_surfaces:
            return False
        for i in range(len(s)):
            if s[:i] + s[i + 1 :] in self.train_surfaces:
                return True
            if (len(s), i, s[:i], s[i + 1 :]) in self.same_len_patterns:
                return True
        return s in self.train_deletions

    def flags(self, t: TokenType) -> dict[str, bool]:
        require(t not in self.train_types, "annotation requested for training-seen type")
        shape = type_shape(t)
        edit1 = self.edit1(type_surface(t))
        known_shape = shape in self.train_shapes
        return {
            "KNOWN_SHAPE_NEW_VALUE_COMBINATION": known_shape,
            "NEW_OCCUPIED_SLOT_SHAPE": not known_shape,
            "ALL_COMPONENT_UNITS_SEEN": all(u in self.train_units for u in t),
            "EDIT1_FAMILY_INNOVATION": edit1,
            "OTHER_PARSER_ACCEPTED_INNOVATION": not edit1,
        }


def annotation_summary(novel_types: Iterable[TokenType], index: NoveltyIndex) -> dict:
    novel = sorted(set(novel_types))
    counts = Counter()
    intersections = Counter()
    known_edit1 = 0
    new_edit1 = 0
    for t in novel:
        flags = index.flags(t)
        for label, yes in flags.items():
            if yes:
                counts[label] += 1
        sig = tuple(sorted(k for k, yes in flags.items() if yes))
        intersections[" & ".join(sig)] += 1
        if flags["KNOWN_SHAPE_NEW_VALUE_COMBINATION"] and flags["EDIT1_FAMILY_INNOVATION"]:
            known_edit1 += 1
        if flags["NEW_OCCUPIED_SLOT_SHAPE"] and flags["EDIT1_FAMILY_INNOVATION"]:
            new_edit1 += 1
    n = len(novel)
    return {
        "n_novel_distinct": n,
        "counts": {k: int(counts.get(k, 0)) for k in ANNOTATION_LABELS},
        "shares": {k: (float(counts.get(k, 0) / n) if n else None) for k in ANNOTATION_LABELS},
        "intersections": dict(sorted(intersections.items())),
        "known_shape_x_edit1_count": int(known_edit1),
        "new_shape_x_edit1_count": int(new_edit1),
    }


def load_zl(zl_path: Path) -> dict:
    sid = source_identity(zl_path)
    require(sid["sha256"] == ZL_SHA256, "ZL3b SHA-256 mismatch")
    require(sid["git_blob_sha1"] == ZL_BLOB, "ZL3b Git blob mismatch")

    vitems, folds_raw, parsed = C.load_corpus(zl_path)
    folds = [set(map(int, f)) for f in folds_raw]
    common_folds = [set(map(int, f)) for f in d58.frozen_folds_from_zl(zl_path)]
    require(len(folds) == N_FOLDS and folds == common_folds, "ZL fold lineage differs from Phase58D")
    require(len(set().union(*folds)) == 99, "ZL fold universe is not 99 physical leaves")

    fold_tokens: List[List[TokenType]] = [[] for _ in range(N_FOLDS)]
    fold_visible = [0] * N_FOLDS
    for f in range(N_FOLDS):
        leaves = folds[f]
        for it in vitems:
            if it.leaf is None or int(it.leaf) not in leaves:
                continue
            plines = parsed[it.item_id]
            require(len(plines) == len(it.lines), "ZL parsed/source line mismatch")
            for source_line, parsed_line in zip(it.lines, plines):
                require(len(source_line) == len(parsed_line), "ZL parsed/source token mismatch")
                fold_visible[f] += len(source_line)
                for seq in parsed_line:
                    if seq is not None:
                        fold_tokens[f].append(canonical_from_int(seq))

    accepted = [len(x) for x in fold_tokens]
    require(accepted == EXPECTED_ZL_ACCEPTED, f"ZL accepted support mismatch: {accepted}")
    require(sum(accepted) == EXPECTED_ZL_TOTAL, "ZL accepted total mismatch")
    return {
        "reading": "ZL3b",
        "source_identity": sid,
        "folds": [sorted(x) for x in folds],
        "fold_tokens": fold_tokens,
        "fold_visible": fold_visible,
        "source_parser_audit": None,
    }


def load_it(it_path: Path, zl_path: Path) -> dict:
    sid = source_identity(it_path)
    require(sid["sha256"] == IT_SHA256, "IT2a SHA-256 mismatch")
    require(sid["git_blob_sha1"] == IT_BLOB, "IT2a Git blob mismatch")
    require(sid["byte_size"] == 342104, "IT2a byte-size mismatch")
    require(sid["line_count"] == 5444, "IT2a line-count mismatch")
    require(sid["first_line"] == "#=IVTFF EvaT 2.0 M 3", "IT2a header mismatch")

    paragraphs, audit = p63.parse_ivtff(it_path, "IT2a", "W1")
    folds = [set(map(int, f)) for f in d58.frozen_folds_from_zl(zl_path)]
    require(len(folds) == N_FOLDS and len(set().union(*folds)) == 99, "IT fold authority mismatch")
    leaf_to_fold = {leaf: f for f, leaves in enumerate(folds) for leaf in leaves}
    require(len(leaf_to_fold) == 99, "IT fold leaf collision")

    parser = e.SlotParser()
    e.validate_parser(parser)
    fold_tokens: List[List[TokenType]] = [[] for _ in range(N_FOLDS)]
    fold_visible = [0] * N_FOLDS
    for par in paragraphs:
        if par.leaf is None or int(par.leaf) not in leaf_to_fold:
            continue
        f = leaf_to_fold[int(par.leaf)]
        for token_units in par.lines:
            for units in token_units:
                surface = "".join(units)
                fold_visible[f] += 1
                picked = parser.pick(surface, "min")
                if picked is not None:
                    fold_tokens[f].append(canonical_from_pick(picked))

    accepted = [len(x) for x in fold_tokens]
    visible = sum(fold_visible)
    total = sum(accepted)
    require(visible == EXPECTED_IT_VISIBLE, f"IT visible support mismatch: {visible}")
    require(total == EXPECTED_IT_ACCEPTED, f"IT accepted support mismatch: {total}")
    require(visible - total == EXPECTED_IT_REJECTED, "IT rejected support mismatch")
    require(accepted == EXPECTED_IT_FOLD_ACCEPTED, f"IT fold accepted mismatch: {accepted}")

    support = d58.load_support_audit()
    require(support["IT2a"]["population"]["clean_tokens"] == visible, "IT support-audit visible mismatch")
    require(support["IT2a"]["population"]["slot_parser_accepted_tokens"] == total, "IT support-audit accepted mismatch")
    require(support["IT2a"]["shared_universe"]["fold_accepted_tokens"] == accepted, "IT support-audit fold mismatch")

    return {
        "reading": "IT2a",
        "source_identity": sid,
        "folds": [sorted(x) for x in folds],
        "fold_tokens": fold_tokens,
        "fold_visible": fold_visible,
        "source_parser_audit": audit,
    }


def rarefaction(counter: Counter, train_vocab: set[TokenType]) -> list[dict]:
    N = int(sum(counter.values()))
    novel_counts = [int(c) for t, c in counter.items() if t not in train_vocab]
    rows = []
    for q in S0.RAREFACTION_FRACTIONS:
        n = S0.rarefaction_sample_size(N, q)
        rows.append({
            "fraction": float(q),
            "sample_n": int(n),
            "all_distinct_expected": float(S0.expected_distinct_without_replacement(counter.values(), n)),
            "training_unseen_distinct_expected": expected_subset_distinct(novel_counts, N, n),
        })
    return rows


def observed_reading(data: dict) -> dict:
    fold_tokens = data["fold_tokens"]
    rows = []
    total_annotation_counts = Counter()
    total_intersections = Counter()
    for f in range(N_FOLDS):
        train = [t for g in range(N_FOLDS) if g != f for t in fold_tokens[g]]
        held = fold_tokens[f]
        train_vocab = set(train)
        held_counter = Counter(held)
        held_vocab = set(held_counter)
        novel = held_vocab - train_vocab
        new_token_count = int(sum(c for t, c in held_counter.items() if t in novel))
        ann = annotation_summary(novel, NoveltyIndex(train_vocab))
        total_annotation_counts.update(ann["counts"])
        total_intersections.update(ann["intersections"])
        rows.append({
            "fold": f,
            "visible_tokens": int(data["fold_visible"][f]),
            "parsed_tokens": len(held),
            "rejected_visible_tokens": int(data["fold_visible"][f] - len(held)),
            "train_parsed_tokens": len(train),
            "train_distinct_types": len(train_vocab),
            "heldout_distinct_types": len(held_vocab),
            "new_type_token_count": new_token_count,
            "new_type_token_rate": float(new_token_count / len(held)),
            "novel_distinct_type_count": len(novel),
            "novel_distinct_type_share": float(len(novel) / len(held_vocab)),
            "rarefaction": rarefaction(held_counter, train_vocab),
            "annotations": ann,
        })
    mean_oov = float(np.mean([r["new_type_token_rate"] for r in rows]))
    incidence = int(sum(r["novel_distinct_type_count"] for r in rows))
    known = int(total_annotation_counts["KNOWN_SHAPE_NEW_VALUE_COMBINATION"])
    edit1 = int(total_annotation_counts["EDIT1_FAMILY_INNOVATION"])
    summary = {
        "mean_five_fold_new_type_token_rate": mean_oov,
        "total_fold_novel_distinct_type_incidence": incidence,
        "all_folds_nonzero_new_type_token_mass": all(r["new_type_token_count"] > 0 for r in rows),
        "annotation_incidence_counts": {k: int(total_annotation_counts[k]) for k in ANNOTATION_LABELS},
        "annotation_intersections": dict(sorted(total_intersections.items())),
        "known_shape_share_of_novel_incidence": float(known / incidence) if incidence else None,
        "edit1_share_of_novel_incidence": float(edit1 / incidence) if incidence else None,
    }
    return {"folds": rows, "summary": summary}


def c2_null(reading: str, fold_tokens: Sequence[Sequence[TokenType]], observed: dict) -> dict:
    fold_counts = [len(x) for x in fold_tokens]
    pool = [t for fold in fold_tokens for t in fold]
    vocab = sorted(set(pool))
    tid = {t: i for i, t in enumerate(vocab)}
    type_ids = np.asarray([tid[t] for t in pool], dtype=np.int64)
    totals = np.bincount(type_ids, minlength=len(vocab)).astype(np.int64)

    # Independent implementation of the observed physical-fold statistic.
    observed_labels = np.concatenate([
        np.full(len(fold_tokens[f]), f, dtype=np.int8) for f in range(N_FOLDS)
    ])

    def stats(labels: np.ndarray):
        joint = np.bincount(type_ids * N_FOLDS + labels, minlength=len(vocab) * N_FOLDS).reshape(len(vocab), N_FOLDS)
        novel = (joint > 0) & (joint == totals[:, None])
        rates = []
        for f in range(N_FOLDS):
            n_new = int(joint[:, f][novel[:, f]].sum())
            rates.append(float(n_new / fold_counts[f]))
        return float(np.mean(rates)), int(novel.sum())

    direct_oov, direct_inc = stats(observed_labels)
    expected_oov = float(observed["summary"]["mean_five_fold_new_type_token_rate"])
    expected_inc = int(observed["summary"]["total_fold_novel_distinct_type_incidence"])
    require(math.isclose(direct_oov, expected_oov, rel_tol=0.0, abs_tol=1e-15), f"C2 observed OOV implementation mismatch {reading}")
    require(direct_inc == expected_inc, f"C2 observed incidence implementation mismatch {reading}")

    null_oov = []
    null_inc = []
    for rep in range(C2_REPS):
        ns = f"Issue191:C2:{reading}:perm:{rep}"
        labels = np.asarray(S0.c2_fold_assignment(fold_counts, ns), dtype=np.int64)
        require([int(np.sum(labels == f)) for f in range(N_FOLDS)] == fold_counts, f"C2 fold counts changed {reading} rep {rep}")
        a, b = stats(labels)
        require(math.isfinite(a), f"C2 nonfinite OOV {reading} rep {rep}")
        null_oov.append(a)
        null_inc.append(b)

    p_oov = float((1 + sum(x >= expected_oov for x in null_oov)) / (C2_REPS + 1))
    p_inc = float((1 + sum(x >= expected_inc for x in null_inc)) / (C2_REPS + 1))
    return {
        "control": "C2_EXCHANGEABLE_FINITE_OBSERVED_INVENTORY",
        "permutations": C2_REPS,
        "fold_counts": fold_counts,
        "global_token_count": len(pool),
        "global_distinct_type_count": len(vocab),
        "observed_mean_five_fold_oov": expected_oov,
        "observed_total_fold_novel_distinct_incidence": expected_inc,
        "mean_oov_p_upper": p_oov,
        "novel_incidence_p_upper": p_inc,
        "null_mean_oov_summary": {
            "mean": float(np.mean(null_oov)),
            "q025": S0.linear_quantile(null_oov, 0.025),
            "median": S0.linear_quantile(null_oov, 0.5),
            "q975": S0.linear_quantile(null_oov, 0.975),
        },
        "null_novel_incidence_summary": {
            "mean": float(np.mean(null_inc)),
            "q025": S0.linear_quantile(null_inc, 0.025),
            "median": S0.linear_quantile(null_inc, 0.5),
            "q975": S0.linear_quantile(null_inc, 0.975),
        },
        "null_mean_oov_by_permutation": null_oov,
        "null_novel_incidence_by_permutation": null_inc,
    }


def metric_mc_summary(values: Sequence[float | None], observed: float | None) -> dict:
    if observed is None or any(v is None or not math.isfinite(float(v)) for v in values):
        return {"observed": observed, "v2_mean": None, "v2_q025": None, "v2_q975": None, "observed_over_v2_mean": None}
    xs = [float(v) for v in values]
    m = float(np.mean(xs))
    return {
        "observed": float(observed),
        "v2_mean": m,
        "v2_q025": S0.linear_quantile(xs, 0.025),
        "v2_q975": S0.linear_quantile(xs, 0.975),
        "observed_over_v2_mean": (float(observed / m) if m != 0.0 else None),
    }


def c3_v2(reading: str, fold_tokens: Sequence[Sequence[TokenType]], observed: dict) -> dict:
    parser = e.SlotParser()
    e.validate_parser(parser)
    per_fold = []
    rep_metrics_by_fold: List[List[dict]] = []

    for f in range(N_FOLDS):
        train = [t for g in range(N_FOLDS) if g != f for t in fold_tokens[g]]
        train_vocab = set(train)
        train_int = [int_from_canonical(t) for t in train]
        model = C.V2Model(train_int)
        index = NoveltyIndex(train_vocab)
        n_generate = len(fold_tokens[f])
        cache: Dict[str, TokenType] = {}
        reps = []
        for rep in range(C3_REPS):
            ns = f"Issue191:C3:{reading}:fold:{f}:rep:{rep}"
            rng = np.random.default_rng(S0.stable_seed(ns))
            generated = Counter()
            for _ in range(n_generate):
                latent = model.sample(rng)
                surface = C.units_to_string(latent)
                canon = cache.get(surface)
                if canon is None:
                    picked = parser.pick(surface, "min")
                    require(picked is not None, f"V2 generated parser-rejected surface {reading} fold {f} rep {rep}: {surface!r}")
                    canon = canonical_from_pick(picked)
                    cache[surface] = canon
                generated[canon] += 1
            novel = set(generated) - train_vocab
            new_token_count = int(sum(c for t, c in generated.items() if t in novel))
            ann = annotation_summary(novel, index)
            reps.append({
                "rep": rep,
                "generated_tokens": n_generate,
                "new_type_token_count": new_token_count,
                "new_type_token_rate": float(new_token_count / n_generate),
                "novel_distinct_type_count": len(novel),
                "known_shape_novel_count": int(ann["counts"]["KNOWN_SHAPE_NEW_VALUE_COMBINATION"]),
                "edit1_novel_count": int(ann["counts"]["EDIT1_FAMILY_INNOVATION"]),
            })
        rep_metrics_by_fold.append(reps)
        per_fold.append({
            "fold": f,
            "generated_tokens_per_rep": n_generate,
            "training_tokens": len(train),
            "training_distinct_types": len(train_vocab),
            "v2_observed_contexts": int(model.observed_contexts),
            "v2_free_parameters": int(model.free_parameters),
            "reparse_cache_distinct_surfaces": len(cache),
            "all_100_reps_nonzero_new_type_mass": all(x["new_type_token_count"] > 0 for x in reps),
            "new_type_token_rate_by_rep": [x["new_type_token_rate"] for x in reps],
            "new_type_token_count_by_rep": [x["new_type_token_count"] for x in reps],
            "novel_distinct_type_count_by_rep": [x["novel_distinct_type_count"] for x in reps],
        })

    combined = []
    for rep in range(C3_REPS):
        rows = [rep_metrics_by_fold[f][rep] for f in range(N_FOLDS)]
        incidence = int(sum(x["novel_distinct_type_count"] for x in rows))
        known = int(sum(x["known_shape_novel_count"] for x in rows))
        edit1 = int(sum(x["edit1_novel_count"] for x in rows))
        combined.append({
            "rep": rep,
            "mean_five_fold_new_type_token_rate": float(np.mean([x["new_type_token_rate"] for x in rows])),
            "total_fold_novel_distinct_type_incidence": incidence,
            "known_shape_share_of_novel_incidence": (float(known / incidence) if incidence else None),
            "edit1_share_of_novel_incidence": (float(edit1 / incidence) if incidence else None),
            "all_folds_nonzero_new_type_mass": all(x["new_type_token_count"] > 0 for x in rows),
        })

    obs = observed["summary"]
    strong_nonzero = all(x["all_folds_nonzero_new_type_mass"] for x in combined)
    oov_summary = metric_mc_summary(
        [x["mean_five_fold_new_type_token_rate"] for x in combined],
        obs["mean_five_fold_new_type_token_rate"],
    )
    novel_summary = metric_mc_summary(
        [float(x["total_fold_novel_distinct_type_incidence"]) for x in combined],
        float(obs["total_fold_novel_distinct_type_incidence"]),
    )
    known_summary = metric_mc_summary(
        [x["known_shape_share_of_novel_incidence"] for x in combined],
        obs["known_shape_share_of_novel_incidence"],
    )
    edit_summary = metric_mc_summary(
        [x["edit1_share_of_novel_incidence"] for x in combined],
        obs["edit1_share_of_novel_incidence"],
    )
    return {
        "control": "C3_FROZEN_PRODUCTIVE_V2",
        "reps_per_fold": C3_REPS,
        "generated_surface_reparsed_with_slotparser_min": True,
        "nonzero_every_realization_every_fold": strong_nonzero,
        "per_fold": per_fold,
        "combined_by_rep": combined,
        "comparison": {
            "mean_five_fold_new_type_token_rate": oov_summary,
            "total_fold_novel_distinct_type_incidence": novel_summary,
            "known_shape_share_of_novel_incidence": known_summary,
            "edit1_share_of_novel_incidence": edit_summary,
        },
    }


def self_test() -> dict:
    # Exact subset rarefaction: two A tokens in population A,A,B,B; one draw hits A with prob 1/2.
    require(math.isclose(expected_subset_distinct([2], 4, 1), 0.5, rel_tol=0.0, abs_tol=1e-12), "subset rarefaction toy failed")
    train = {
        ((0, "q"), (1, "o")),
        ((0, "s"), (1, "o")),
        ((4, "ch"), (6, "e")),
    }
    idx = NoveltyIndex(train)
    toys = [
        ((0, "q"), (1, "y")),
        ((0, "q"), (6, "e")),
        ((4, "sh"), (6, "e")),
    ]
    for t in toys:
        fast = idx.flags(t)
        slow = S0.novelty_flags(t, train)
        require(fast == slow, f"optimized annotation differs from Stage0 helper for {t}: {fast} != {slow}")
    require(C2_REPS == S0.C2_PERMUTATIONS == 1000, "C2 replication count drift")
    require(C3_REPS == S0.C3_REPS_PER_FOLD == 100, "C3 replication count drift")
    require(tuple(S0.RAREFACTION_FRACTIONS) == (0.10, 0.25, 0.50, 0.75, 1.00), "rarefaction checkpoint drift")
    return {"subset_rarefaction": "PASS", "optimized_annotations": "PASS", "stage0_constants": "PASS"}


def classify(readings: dict) -> tuple[str | None, str, dict]:
    zl = readings["ZL3b"]
    it = readings["IT2a"]
    nonzero = {
        "ZL3b": bool(zl["observed"]["summary"]["all_folds_nonzero_new_type_token_mass"]),
        "IT2a": bool(it["observed"]["summary"]["all_folds_nonzero_new_type_token_mass"]),
    }
    c2_pass = {
        r: bool(readings[r]["c2"]["mean_oov_p_upper"] <= C2_ALPHA and readings[r]["c2"]["novel_incidence_p_upper"] <= C2_ALPHA)
        for r in READINGS
    }
    c3_nonzero = {r: bool(readings[r]["c3"]["nonzero_every_realization_every_fold"]) for r in READINGS}
    ratios = {
        r: readings[r]["c3"]["comparison"]["mean_five_fold_new_type_token_rate"]["observed_over_v2_mean"]
        for r in READINGS
    }
    ratio_pass = {
        r: bool(ratios[r] is not None and V2_RATIO_BAND[0] <= ratios[r] <= V2_RATIO_BAND[1])
        for r in READINGS
    }
    gates = {
        "observed_nonzero_every_fold": nonzero,
        "c2_both_primary_tests_p_le_0_01": c2_pass,
        "c3_nonzero_every_rep_every_fold": c3_nonzero,
        "observed_over_v2_mean_oov_ratio": ratios,
        "observed_over_v2_mean_oov_within_0_5_to_2_0": ratio_pass,
    }

    if not nonzero["ZL3b"] and not nonzero["IT2a"]:
        return "NO_HELDOUT_PRODUCTIVITY", "FROZEN_LABEL", gates
    if nonzero["ZL3b"] != nonzero["IT2a"]:
        return "READING_UNSTABLE", "FROZEN_LABEL", gates
    if not nonzero["ZL3b"] or not nonzero["IT2a"]:
        return "NO_HELDOUT_PRODUCTIVITY", "FROZEN_LABEL", gates
    if not c2_pass["ZL3b"] or not c2_pass["IT2a"]:
        return "PRODUCTIVE_FORMS_PRESENT_BUT_FINITE_NULL_NOT_REJECTED", "FROZEN_LABEL", gates
    if all(c3_nonzero.values()) and all(ratio_pass.values()):
        return "R11_PRODUCTIVITY_PROMOTED", "FROZEN_LABEL", gates
    return None, "NO_FROZEN_LABEL_APPLIES_C3_MISMATCH", gates


def run(zl_path: Path, it_path: Path) -> dict:
    authorities = verify_repo_authorities()
    tests = self_test()
    zl = load_zl(zl_path)
    it = load_it(it_path, zl_path)
    require(zl["folds"] == it["folds"], "reading fold universes differ")

    readings = {}
    for data in (zl, it):
        name = data["reading"]
        observed = observed_reading(data)
        if name == "ZL3b":
            got = [x["new_type_token_rate"] for x in observed["folds"]]
            require(all(math.isclose(a, b, rel_tol=0.0, abs_tol=1e-15) for a, b in zip(got, EXPECTED_ZL_HISTORICAL_OOV)), f"ZL observed OOV does not replay historical V+: {got}")
            require(math.isclose(observed["summary"]["mean_five_fold_new_type_token_rate"], EXPECTED_ZL_HISTORICAL_MEAN_OOV, rel_tol=0.0, abs_tol=1e-15), "ZL historical mean OOV mismatch")
        c2 = c2_null(name, data["fold_tokens"], observed)
        c3 = c3_v2(name, data["fold_tokens"], observed)
        readings[name] = {
            "source_identity": data["source_identity"],
            "source_parser_audit": data["source_parser_audit"],
            "support": {
                "physical_leaves": len(set().union(*[set(x) for x in data["folds"]])),
                "visible_tokens_by_fold": [int(x) for x in data["fold_visible"]],
                "visible_tokens_total": int(sum(data["fold_visible"])),
                "parsed_tokens_by_fold": [len(x) for x in data["fold_tokens"]],
                "parsed_tokens_total": int(sum(len(x) for x in data["fold_tokens"])),
                "rejected_visible_tokens_total": int(sum(data["fold_visible"]) - sum(len(x) for x in data["fold_tokens"])),
            },
            "fold_leaf_numbers": data["folds"],
            "observed": observed,
            "c1": {
                "control": "C1_CLOSED_TRAINING_VOCABULARY_LOOKUP",
                "new_type_token_rate_by_construction": 0.0,
                "novel_distinct_type_count_by_construction": 0,
                "statistical_null": False,
            },
            "c2": c2,
            "c3": c3,
        }

    label, resolution, gates = classify(readings)
    return {
        "schema": SCHEMA,
        "issue": 191,
        "parent_issue": 172,
        "scientific_first_reveal": True,
        "authorities": authorities,
        "self_test": tests,
        "representation": {
            "slot_parser_policy": "min",
            "n_slots": 12,
            "n_units": len(C.UNITS),
            "canonical_type": "ordered (slot,value) unit sequence",
            "canonical_surface": "concatenated unit values",
            "readings_are_independent_manuscripts": False,
        },
        "controls": {
            "c1": "closed training-vocabulary lookup; zero novelty by construction",
            "c2": "1000 deterministic exchangeable complete-observed-inventory fold-label permutations",
            "c3": "frozen OGH-C V2; 100 deterministic realizations/fold; generated surfaces reparsed by SlotParser(min)",
        },
        "readings": readings,
        "promotion_gates": gates,
        "outcome_label": label,
        "label_resolution": resolution,
        "r11_promoted": label == "R11_PRODUCTIVITY_PROMOTED",
        "interpretation_firewall": {
            "infinite_vocabulary_proved": False,
            "semantics_inferred": False,
            "language_or_cipher_family_inferred": False,
            "it2a_counted_as_independent_manuscript": False,
            "retroactive_scorecard_rescore_licensed": False,
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("zl", nargs="?")
    ap.add_argument("it", nargs="?")
    ap.add_argument("out", nargs="?")
    args = ap.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return
    if not args.run or not args.zl or not args.it or not args.out:
        ap.error("use --self-test or --run ZL3b IT2a OUT.json")
    out_path = Path(args.out)
    try:
        result = run(Path(args.zl), Path(args.it))
    except ProtocolInvalid as exc:
        result = {
            "schema": SCHEMA,
            "issue": 191,
            "scientific_first_reveal": True,
            "outcome_label": "INVALID",
            "label_resolution": "FROZEN_LABEL",
            "r11_promoted": False,
            "invalid_reason": str(exc),
        }
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
