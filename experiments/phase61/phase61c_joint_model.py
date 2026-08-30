#!/usr/bin/env python3
"""Phase61C A1 joint-model test.

This executable implements the frozen PLAN_C.md + IMPLEMENTATION_C.md contract.
It requires a local copy of the exact ZL3b/EVA v3b transcription and does not
redistribute that third-party source.

Usage:
  python experiments/phase61/phase61c_joint_model.py /path/to/ZL3b-n.txt

The script first runs a Phase61B compatibility audit. If that audit fails it
emits no Phase61C scientific verdict.
"""
from __future__ import annotations

import bisect
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

EXPECTED_GIT_BLOB_SHA1 = "2a4533ab9bdfa85db9bad602d590978953055df1"
ENTRY_STRENGTH_GRID = (0.5, 1.0, 1.5, 2.0)
LOCAL_P_GRID = (0.05, 0.10, 0.20, 0.30)
TRAIN_REPS = 3
TEST_REPS = 5

REFERENCE_61B = {
    "edit1_type_density": 0.80374,
    "local_prev10_fraction": 0.09778,
    "line_position_eta2_mean": 0.03115,
    "line_position_eta2_max": 0.08810,
    "entry_pseudo_norm": 1.28505,
}
AUDIT_REL_TOL = {
    "edit1_type_density": 0.10,
    "local_prev10_fraction": 0.30,
    "line_position_eta2_mean": 0.40,
    "entry_pseudo_norm": 0.40,
}

HP = re.compile(r"^<(?P<p>f\d+[rv]\d*)>\s+<!\s*(?P<m>.*?)>")
LP = re.compile(r"^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<c>[^>]*)>\s+(?P<b>.*)$")
LEAF_RE = re.compile(r"f(\d+)")


@dataclass
class Paragraph:
    page: str
    pid: int
    leaf: int
    section: str
    lines: List[List[str]]


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def tokenize_line(body: str) -> Tuple[bool, List[str]]:
    start = "<%>" in body
    body = body.replace("<%>", " ")
    body = re.sub(r"<[^>]*>", " ", body)
    toks = [re.sub(r"[^A-Za-z]", "", x).lower() for x in re.split(r"[.\s]+", body)]
    return start, [x for x in toks if x]


def parse(path: str) -> Tuple[List[Paragraph], Dict[str, Dict[str, str]]]:
    raw = open(path, encoding="utf-8", errors="ignore").read().splitlines()
    headers: Dict[str, Dict[str, str]] = {}
    par_lines: Dict[Tuple[str, int], List[List[str]]] = defaultdict(list)
    pid: Dict[str, int] = defaultdict(int)
    order: List[Tuple[str, int]] = []

    for s in raw:
        h = HP.match(s)
        if h:
            headers[h.group("p")] = dict(re.findall(r"\$(\w)=([^\s>]+)", h.group("m")))
            continue
        m = LP.match(s)
        if not m or "P" not in m.group("c"):
            continue
        page = m.group("loc").split(".")[0]
        start, toks = tokenize_line(m.group("b"))
        if start:
            pid[page] += 1
            order.append((page, pid[page]))
        if toks and pid[page]:
            par_lines[(page, pid[page])].append(toks)

    out: List[Paragraph] = []
    for page, p in order:
        lines = par_lines.get((page, p), [])
        if not lines:
            continue
        mm = LEAF_RE.match(page)
        if not mm:
            continue
        out.append(
            Paragraph(
                page=page,
                pid=p,
                leaf=int(mm.group(1)),
                section=headers.get(page, {}).get("I", "?"),
                lines=lines,
            )
        )
    return out, headers


def lev1(a: str, b: str) -> bool:
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    i = j = d = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            d += 1
            j += 1
        if d > 1:
            return False
    return True


def entropy(v: Sequence[str]) -> float:
    c = Counter(v)
    if not c:
        return 0.0
    q = np.array(list(c.values()), dtype=float)
    q /= q.sum()
    return float(-(q * np.log2(q)).sum())


def feat(toks: Sequence[str]) -> np.ndarray:
    n = len(toks)
    lens = np.array([len(t) for t in toks], dtype=float)
    flat = [ch for t in toks for ch in t]
    edit1_fraction = sum(
        any(lev1(a, b) for j, b in enumerate(toks) if i != j)
        for i, a in enumerate(toks)
    ) / n
    local_prev10 = sum(
        any(lev1(a, b) for b in toks[max(0, i - 10):i])
        for i, a in enumerate(toks)
    ) / n
    kt_mass = sum(("k" in t or "t" in t) for t in toks) / n
    kc = sum(t.count("k") for t in toks)
    tc = sum(t.count("t") for t in toks)
    return np.array(
        [
            len(set(toks)) / n,
            lens.mean(),
            lens.std(),
            len(set(flat)),
            entropy(flat),
            entropy([t[0] for t in toks]),
            entropy([t[-1] for t in toks]),
            edit1_fraction,
            local_prev10,
            kt_mass,
            kc / (kc + tc) if kc + tc else 0.0,
        ],
        dtype=float,
    )


def eligible(p: Paragraph) -> bool:
    return len(p.lines) >= 3 and len(p.lines[0]) >= 5 and len(p.lines[2]) >= 5


def eligible_deltas(paragraphs: Sequence[Paragraph], sd: np.ndarray) -> np.ndarray:
    ds: List[np.ndarray] = []
    for p in paragraphs:
        if not eligible(p):
            continue
        pseudos = []
        for j in range(1, len(p.lines) - 2):
            if len(p.lines[j]) >= 5 and len(p.lines[j + 2]) >= 5:
                pseudos.append((feat(p.lines[j + 2]) - feat(p.lines[j])) / sd)
        if not pseudos:
            continue
        real = (feat(p.lines[2]) - feat(p.lines[0])) / sd
        ds.append(real - np.mean(pseudos, axis=0))
    if not ds:
        return np.zeros((0, 11), dtype=float)
    return np.array(ds, dtype=float)


def feature_sd(paragraphs: Sequence[Paragraph]) -> np.ndarray:
    vv = [feat(line) for p in paragraphs for line in p.lines if len(line) >= 5]
    sd = np.std(np.array(vv, dtype=float), axis=0)
    sd[sd == 0] = 1.0
    return sd


def local_prev10_fraction(paragraphs: Sequence[Paragraph]) -> float:
    hit = 0
    n = 0
    for p in paragraphs:
        for line in p.lines:
            for i, a in enumerate(line):
                hit += int(any(lev1(a, b) for b in line[max(0, i - 10):i]))
                n += 1
    return hit / n if n else 0.0


def eta2(x: np.ndarray, g: np.ndarray) -> float:
    mu = float(np.mean(x))
    ss_total = float(np.sum((x - mu) ** 2))
    if ss_total == 0:
        return 0.0
    ss_between = 0.0
    for k in sorted(set(g.tolist())):
        mask = g == k
        ss_between += int(mask.sum()) * (float(np.mean(x[mask])) - mu) ** 2
    return ss_between / ss_total


def line_eta2(paragraphs: Sequence[Paragraph]) -> Tuple[float, float, List[float]]:
    vv = []
    gg = []
    for p in paragraphs:
        for i, line in enumerate(p.lines):
            if len(line) >= 5:
                vv.append(feat(line))
                gg.append(min(i, 3))
    if not vv:
        return 0.0, 0.0, [0.0] * 11
    X = np.array(vv, dtype=float)
    g = np.array(gg, dtype=int)
    es = [eta2(X[:, j], g) for j in range(X.shape[1])]
    return float(np.mean(es)), float(np.max(es)), [float(x) for x in es]


def all_tokens(paragraphs: Sequence[Paragraph]) -> List[str]:
    return [t for p in paragraphs for line in p.lines for t in line]


def build_neighbors(vocab: Sequence[str]) -> Dict[str, List[str]]:
    vs = set(vocab)
    alphabet = sorted(set("".join(vocab)))
    out: Dict[str, List[str]] = {}
    for w in vocab:
        cand = set()
        L = len(w)
        for i in range(L):
            x = w[:i] + w[i + 1:]
            if x in vs and x != w:
                cand.add(x)
        for i, old in enumerate(w):
            for c in alphabet:
                if c == old:
                    continue
                x = w[:i] + c + w[i + 1:]
                if x in vs:
                    cand.add(x)
        for i in range(L + 1):
            for c in alphabet:
                x = w[:i] + c + w[i:]
                if x in vs:
                    cand.add(x)
        out[w] = sorted(cand)
    return out


def edit1_type_density_from_neighbors(types: Iterable[str], neighbors: Dict[str, List[str]]) -> float:
    ts = set(types)
    if not ts:
        return 0.0
    return sum(any(v in ts for v in neighbors.get(t, ())) for t in ts) / len(ts)


def physical_leaf_folds(paragraphs: Sequence[Paragraph]) -> List[set]:
    leaves = sorted(set(p.leaf for p in paragraphs if eligible(p)))
    return [set(leaves[i::5]) for i in range(5)]


def subset(paragraphs: Sequence[Paragraph], leaves: set, include: bool = True) -> List[Paragraph]:
    return [p for p in paragraphs if (p.leaf in leaves) == include]


def phase60b_entry_norm(paragraphs: Sequence[Paragraph]) -> float:
    records = [p for p in paragraphs if eligible(p)]
    sd = feature_sd(records)
    folds = physical_leaf_folds(records)
    ds = []
    for test_leaves in folds:
        train = subset(records, test_leaves, include=False)
        test = subset(records, test_leaves, include=True)
        train_trans = np.array([(feat(p.lines[2]) - feat(p.lines[0])) / sd for p in train])
        direction = np.mean(train_trans, axis=0)
        nn = float(np.linalg.norm(direction))
        if nn:
            direction /= nn
        for p in test:
            pseudos = []
            for j in range(1, len(p.lines) - 2):
                if len(p.lines[j]) >= 5 and len(p.lines[j + 2]) >= 5:
                    pseudos.append((feat(p.lines[j + 2]) - feat(p.lines[j])) / sd)
            if not pseudos:
                continue
            real = (feat(p.lines[2]) - feat(p.lines[0])) / sd
            ds.append(real - np.mean(pseudos, axis=0))
    D = np.array(ds, dtype=float)
    return float(np.linalg.norm(np.mean(D, axis=0)))


def compatibility_audit(paragraphs: Sequence[Paragraph], neighbors: Dict[str, List[str]]) -> dict:
    toks = all_tokens(paragraphs)
    types = sorted(set(toks))
    eta_mean, eta_max, _ = line_eta2(paragraphs)
    observed = {
        "edit1_type_density": edit1_type_density_from_neighbors(types, neighbors),
        "local_prev10_fraction": local_prev10_fraction(paragraphs),
        "line_position_eta2_mean": eta_mean,
        "line_position_eta2_max": eta_max,
        "entry_pseudo_norm": phase60b_entry_norm(paragraphs),
    }
    rel = {k: abs(observed[k] - REFERENCE_61B[k]) / abs(REFERENCE_61B[k]) for k in REFERENCE_61B}
    passes = {k: rel[k] <= tol for k, tol in AUDIT_REL_TOL.items()}
    return {
        "reference": REFERENCE_61B,
        "observed": observed,
        "relative_error": rel,
        "gated_metrics": passes,
        "pass": all(passes.values()),
    }


def shape(t: str) -> Tuple[int, int, str, str]:
    return (int("k" in t or "t" in t), min(len(t), 8), t[0], t[-1])


def learn_shape_scores(train: Sequence[Paragraph], vocab: Sequence[str]) -> Dict[Tuple[int, int, str, str], float]:
    ec = Counter()
    bc = Counter()
    for p in train:
        for i, line in enumerate(p.lines):
            for t in line:
                (ec if i == 0 else bc)[shape(t)] += 1
    shapes = sorted(set(shape(t) for t in vocab) | set(ec) | set(bc))
    E = sum(ec.values())
    B = sum(bc.values())
    S = len(shapes)
    out = {}
    for s in shapes:
        pe = (ec[s] + 1.0) / (E + S)
        pb = (bc[s] + 1.0) / (B + S)
        out[s] = math.log(pe / pb)
    return out


def entry_cumulative(vocab: Sequence[str], scores: dict, strength: float) -> List[float]:
    weights = [math.exp(strength * scores.get(shape(t), 0.0)) for t in vocab]
    total = sum(weights)
    acc = 0.0
    out = []
    for w in weights:
        acc += w / total
        out.append(acc)
    out[-1] = 1.0
    return out


def weighted_draw(vocab: Sequence[str], cumulative: Sequence[float], rng: random.Random) -> str:
    return vocab[bisect.bisect_left(cumulative, rng.random())]


def generate_layout(
    layout: Sequence[Paragraph],
    vocab: Sequence[str],
    neighbors: Dict[str, List[str]],
    entry_cum: Sequence[float],
    local_p: float,
    seed: int,
) -> List[Paragraph]:
    rng = random.Random(seed)
    out: List[Paragraph] = []
    recent_by_leaf: Dict[int, List[str]] = defaultdict(list)
    for p in layout:
        glines: List[List[str]] = []
        recent = recent_by_leaf[p.leaf]
        for li, line in enumerate(p.lines):
            gline = []
            for _ in line:
                if li == 0:
                    t = weighted_draw(vocab, entry_cum, rng)
                elif rng.random() < local_p and recent:
                    parent = recent[rng.randrange(max(0, len(recent) - 10), len(recent))]
                    nbs = neighbors.get(parent, [])
                    t = nbs[rng.randrange(len(nbs))] if nbs else vocab[rng.randrange(len(vocab))]
                else:
                    t = vocab[rng.randrange(len(vocab))]
                gline.append(t)
                recent.append(t)
                if len(recent) > 10:
                    del recent[:-10]
            glines.append(gline)
        out.append(Paragraph(p.page, p.pid, p.leaf, p.section, glines))
    return out


def metric_bundle(
    paragraphs: Sequence[Paragraph],
    sd: np.ndarray,
    direction: np.ndarray,
    neighbors: Dict[str, List[str]],
) -> dict:
    D = eligible_deltas(paragraphs, sd)
    entry = float(np.mean(D @ direction)) if len(D) else 0.0
    eta_mean, eta_max, _ = line_eta2(paragraphs)
    toks = all_tokens(paragraphs)
    types = set(toks)
    return {
        "entry_projection": entry,
        "local_prev10_fraction": local_prev10_fraction(paragraphs),
        "line_position_eta2_mean": eta_mean,
        "line_position_eta2_max": eta_max,
        "edit1_type_density": edit1_type_density_from_neighbors(types, neighbors),
        "n_tokens": len(toks),
        "n_types": len(types),
    }


def average_bundles(bb: Sequence[dict]) -> dict:
    keys = [
        "entry_projection",
        "local_prev10_fraction",
        "line_position_eta2_mean",
        "line_position_eta2_max",
        "edit1_type_density",
    ]
    return {k: float(np.mean([b[k] for b in bb])) for k in keys}


def rel_mse(gen: dict, real: dict) -> float:
    keys = ("entry_projection", "local_prev10_fraction", "line_position_eta2_mean")
    vals = []
    for k in keys:
        den = abs(real[k]) if abs(real[k]) > 1e-12 else 1e-12
        vals.append(((gen[k] - real[k]) / den) ** 2)
    return float(np.mean(vals))


def run_phase61c(paragraphs: Sequence[Paragraph], neighbors: Dict[str, List[str]]) -> dict:
    vocab = sorted(set(all_tokens(paragraphs)))
    folds = physical_leaf_folds(paragraphs)
    fold_results = []

    for fi, test_leaves in enumerate(folds):
        train = subset(paragraphs, test_leaves, include=False)
        test = subset(paragraphs, test_leaves, include=True)
        sd = feature_sd(train)
        Dtr = eligible_deltas(train, sd)
        direction = np.mean(Dtr, axis=0)
        norm = float(np.linalg.norm(direction))
        if norm == 0:
            raise RuntimeError(f"zero training direction in fold {fi}")
        direction /= norm

        real_train = metric_bundle(train, sd, direction, neighbors)
        real_test = metric_bundle(test, sd, direction, neighbors)
        scores = learn_shape_scores(train, vocab)
        cums = {s: entry_cumulative(vocab, scores, s) for s in ENTRY_STRENGTH_GRID}

        candidates = []
        for si, strength in enumerate(ENTRY_STRENGTH_GRID):
            for pi, local_p in enumerate(LOCAL_P_GRID):
                reps = []
                for r in range(TRAIN_REPS):
                    seed = 6100000 + fi * 100000 + si * 10000 + pi * 1000 + r
                    gen = generate_layout(train, vocab, neighbors, cums[strength], local_p, seed)
                    reps.append(metric_bundle(gen, sd, direction, neighbors))
                avg = average_bundles(reps)
                candidates.append(
                    {
                        "entry_strength": strength,
                        "local_family_p": local_p,
                        "train_generated": avg,
                        "train_relative_mse": rel_mse(avg, real_train),
                    }
                )

        candidates.sort(key=lambda x: (x["train_relative_mse"], x["entry_strength"], x["local_family_p"]))
        chosen = candidates[0]
        strength = chosen["entry_strength"]
        local_p = chosen["local_family_p"]

        test_reps = []
        for r in range(TEST_REPS):
            seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10 + r
            gen = generate_layout(test, vocab, neighbors, cums[strength], local_p, seed)
            test_reps.append(metric_bundle(gen, sd, direction, neighbors))
        gen_test = average_bundles(test_reps)

        fold_results.append(
            {
                "fold": fi,
                "test_leaves": sorted(test_leaves),
                "n_train_paragraphs": len(train),
                "n_test_paragraphs": len(test),
                "selected": {"entry_strength": strength, "local_family_p": local_p},
                "train_real": real_train,
                "train_generated": chosen["train_generated"],
                "train_relative_mse": chosen["train_relative_mse"],
                "heldout_real": real_test,
                "heldout_generated": gen_test,
                "heldout_ratio": {
                    k: (gen_test[k] / real_test[k] if abs(real_test[k]) > 1e-12 else None)
                    for k in ("entry_projection", "local_prev10_fraction", "line_position_eta2_mean")
                },
                "candidate_scorecard": candidates,
            }
        )

    primary = ("entry_projection", "local_prev10_fraction", "line_position_eta2_mean")
    ratio_of_means = {}
    mean_fold_ratio = {}
    for k in primary:
        rg = float(np.mean([f["heldout_generated"][k] for f in fold_results]))
        rr = float(np.mean([f["heldout_real"][k] for f in fold_results]))
        ratio_of_means[k] = rg / rr if abs(rr) > 1e-12 else None
        vals = [f["heldout_ratio"][k] for f in fold_results if f["heldout_ratio"][k] is not None]
        mean_fold_ratio[k] = float(np.mean(vals)) if vals else None

    gate = {k: (ratio_of_means[k] is not None and 0.5 <= ratio_of_means[k] <= 2.0) for k in primary}
    survives = all(gate.values())
    return {
        "phase": "61C",
        "model": "A1: boundary-aware entry mixture + one local-family body activation mechanism",
        "parameter_grids": {"entry_strength": list(ENTRY_STRENGTH_GRID), "local_family_p": list(LOCAL_P_GRID)},
        "selection": "per outer physical-leaf fold; 3 training stochastic replicates; minimum mean squared relative error over entry projection, local-prev10, and line-position eta2 mean",
        "heldout_replicates_per_fold": TEST_REPS,
        "folds": fold_results,
        "heldout_ratio_of_means": ratio_of_means,
        "heldout_mean_fold_ratio": mean_fold_ratio,
        "broad_regime_gate_0.5_to_2.0": gate,
        "status": "A1 SURVIVES first joint gate" if survives else "A1 FAILS joint gate",
        "decision": (
            "Retain G/A1 as a viable structural family, freeze A1, count its complexity increment, and move to direct N0/B0 comparison."
            if survives
            else "Freeze A1 failure. Do not create A2 before the N0/B0 comparison required by ROADMAP.md."
        ),
        "complexity_increment_vs_A0": "one local-family mechanism plus one fitted global scalar local_family_p; entry_strength remains an A0 parameter",
        "edit1_density_caveat": "non-independent because A1 uses the empirical Voynich prose token-type inventory",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt", file=sys.stderr)
        return 2
    path = sys.argv[1]
    data = open(path, "rb").read()
    blob = git_blob_sha1(data)
    if blob != EXPECTED_GIT_BLOB_SHA1:
        print(json.dumps({"error": "input Git blob SHA-1 mismatch", "observed": blob, "expected": EXPECTED_GIT_BLOB_SHA1}, indent=2))
        return 3

    paragraphs, _ = parse(path)
    vocab = sorted(set(all_tokens(paragraphs)))
    neighbors = build_neighbors(vocab)
    audit = compatibility_audit(paragraphs, neighbors)
    output = {
        "input": {"bytes": len(data), "git_blob_sha1": blob, "paragraphs": len(paragraphs), "prose_tokens": len(all_tokens(paragraphs)), "prose_types": len(vocab)},
        "phase61b_compatibility_audit": audit,
    }
    if not audit["pass"]:
        output["phase61c"] = None
        output["scientific_status"] = "NO PHASE61C VERDICT — compatibility gate failed"
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 4

    output["phase61c"] = run_phase61c(paragraphs, neighbors)
    output["scientific_status"] = output["phase61c"]["status"]
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
