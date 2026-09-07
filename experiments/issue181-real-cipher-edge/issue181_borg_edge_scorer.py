#!/usr/bin/env python3
"""Frozen external Borg R5-like edge scorer for Issue #181.

Scientific contract:
  research/ISSUE181_REAL_CIPHER_EDGE_GATE0_PLAN_20260907.md

This scorer uses only committed Borg canonical ciphertext transcriptions. It
scores the first-symbol factor that differs between a position-only model and
an immediately-previous-unit-terminal-conditioned model, separately within
physical lines and across physical line breaks.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ATOM_RE = re.compile(r"^S[0-9]{3,4}$")
ALPHA = 0.01


def parse_page(path: Path) -> dict:
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        units = []
        for chunk in raw.split("|"):
            chunk = chunk.strip()
            if not chunk:
                raise RuntimeError(f"{path.name}: empty unit in non-empty line")
            atoms = chunk.split()
            bad = [a for a in atoms if not ATOM_RE.fullmatch(a)]
            if bad:
                raise RuntimeError(f"{path.name}: invalid atoms {bad}")
            units.append(atoms)
        lines.append(units)
    return {
        "page_id": path.name.removesuffix(".canonical.txt"),
        "lines": lines,
    }


def load_corpus(root: Path) -> tuple[list[dict], list[str]]:
    pages = [parse_page(p) for p in sorted(root.glob("borg_*.canonical.txt"))]
    pages = [p for p in pages if any(p["lines"])]
    pages.sort(key=lambda p: p["page_id"])
    vocab = sorted({a for p in pages for line in p["lines"] for unit in line for a in unit})
    if not pages:
        raise RuntimeError("no non-empty Borg canonical pages")
    if not vocab:
        raise RuntimeError("empty atom vocabulary")
    return pages, vocab


def assign_folds(pages: list[dict]) -> dict[str, int]:
    return {p["page_id"]: i % 5 for i, p in enumerate(pages)}


def same_line_events(page: dict) -> list[tuple[str, str]]:
    out = []
    for line in page["lines"]:
        for prev, cur in zip(line, line[1:]):
            out.append((prev[-1], cur[0]))
    return out


def cross_line_events(page: dict) -> list[tuple[str, str]]:
    lines = page["lines"]
    return [(a[-1][-1], b[0][0]) for a, b in zip(lines, lines[1:])]


def fit(events: list[tuple[str, str]]) -> tuple[Counter, dict[str, Counter], Counter]:
    base = Counter()
    cond: dict[str, Counter] = defaultdict(Counter)
    ctx = Counter()
    for x, y in events:
        base[y] += 1
        cond[x][y] += 1
        ctx[x] += 1
    return base, dict(cond), ctx


def log2_base(y: str, base: Counter, n: int, vocab_size: int) -> float:
    return math.log2((base[y] + ALPHA) / (n + ALPHA * vocab_size))


def log2_cond(y: str, x: str, cond: dict[str, Counter], ctx: Counter, vocab_size: int) -> float:
    row = cond.get(x)
    xy = row[y] if row is not None else 0
    nx = ctx[x]
    return math.log2((xy + ALPHA) / (nx + ALPHA * vocab_size))


def evaluate_events(
    train_events: list[tuple[str, str]],
    test_events: list[tuple[str, str]],
    vocab_size: int,
) -> dict:
    if not train_events or not test_events:
        raise RuntimeError("zero train/test event support")
    base, cond, ctx = fit(train_events)
    n = len(train_events)
    gains = []
    pos_nll = []
    edge_nll = []
    for x, y in test_events:
        lp0 = log2_base(y, base, n, vocab_size)
        lp1 = log2_cond(y, x, cond, ctx, vocab_size)
        gains.append(lp1 - lp0)
        pos_nll.append(-lp0)
        edge_nll.append(-lp1)
    return {
        "test_event_count": len(test_events),
        "train_event_count": len(train_events),
        "train_previous_terminal_contexts": len(ctx),
        "mean_pos_bits": sum(pos_nll) / len(pos_nll),
        "mean_edge_bits": sum(edge_nll) / len(edge_nll),
        "mean_gain_bits": sum(gains) / len(gains),
        "median_gain_bits": sorted(gains)[len(gains) // 2],
        "total_gain_bits": sum(gains),
    }


def passes(vals: list[float]) -> bool:
    return (sum(vals) / len(vals) > 0.0) and (sum(v > 0.0 for v in vals) >= 4)


def analyze(root: Path) -> dict:
    pages, vocab = load_corpus(root)
    fold_of = assign_folds(pages)
    per_page_same = {p["page_id"]: same_line_events(p) for p in pages}
    per_page_cross = {p["page_id"]: cross_line_events(p) for p in pages}

    folds = []
    page_diagnostics = []
    for f in range(5):
        train_ids = [p["page_id"] for p in pages if fold_of[p["page_id"]] != f]
        test_ids = [p["page_id"] for p in pages if fold_of[p["page_id"]] == f]

        train_same = [e for pid in train_ids for e in per_page_same[pid]]
        test_same = [e for pid in test_ids for e in per_page_same[pid]]
        train_cross = [e for pid in train_ids for e in per_page_cross[pid]]
        test_cross = [e for pid in test_ids for e in per_page_cross[pid]]

        same = evaluate_events(train_same, test_same, len(vocab))
        cross = evaluate_events(train_cross, test_cross, len(vocab))
        folds.append({
            "fold": f,
            "test_page_count": len(test_ids),
            "same_line": same,
            "cross_line": cross,
        })

        # Frozen non-gating page diagnostic using the exact fold-trained
        # same-line model. Pages with no same-line edge are reported null.
        base, cond, ctx = fit(train_same)
        n = len(train_same)
        for pid in test_ids:
            ev = per_page_same[pid]
            if not ev:
                page_diagnostics.append({"page_id": pid, "fold": f, "same_line_event_count": 0, "mean_gain_bits": None})
                continue
            gs = [
                log2_cond(y, x, cond, ctx, len(vocab)) - log2_base(y, base, n, len(vocab))
                for x, y in ev
            ]
            page_diagnostics.append({
                "page_id": pid,
                "fold": f,
                "same_line_event_count": len(ev),
                "mean_gain_bits": sum(gs) / len(gs),
            })

    g_line = [x["same_line"]["mean_gain_bits"] for x in folds]
    g_cross = [x["cross_line"]["mean_gain_bits"] for x in folds]
    line_pass = passes(g_line)
    cross_pass = passes(g_cross)
    if line_pass and not cross_pass:
        classification = "EXTERNAL LINE-LOCAL EDGE"
    elif line_pass and cross_pass:
        classification = "EXTERNAL EDGE WITH CROSS-LINE CONTINUATION"
    else:
        classification = "NO ROBUST EXTERNAL EDGE"

    line_lengths = Counter(len(line) for p in pages for line in p["lines"])
    nonnull_page = [x["mean_gain_bits"] for x in page_diagnostics if x["mean_gain_bits"] is not None]
    return {
        "experiment": "Issue #181 Borg external R5-like edge reveal",
        "external_only": True,
        "alpha": ALPHA,
        "vocabulary_size": len(vocab),
        "vocabulary": vocab,
        "page_count": len(pages),
        "fold_rule": "lexicographic non-empty page order; index modulo 5",
        "folds": folds,
        "primary": {
            "G_line_fold_bits": g_line,
            "G_line_mean_bits": sum(g_line) / 5,
            "G_line_positive_folds": sum(v > 0 for v in g_line),
            "G_line_pass": line_pass,
            "G_cross_fold_bits": g_cross,
            "G_cross_mean_bits": sum(g_cross) / 5,
            "G_cross_positive_folds": sum(v > 0 for v in g_cross),
            "G_cross_pass": cross_pass,
            "classification": classification,
        },
        "diagnostics": {
            "line_length_in_units": dict(sorted(line_lengths.items())),
            "page_same_line_mean_gain": page_diagnostics,
            "page_same_line_positive_fraction": (
                sum(v > 0 for v in nonnull_page) / len(nonnull_page) if nonnull_page else None
            ),
        },
    }


def synthetic_preflight() -> None:
    root = Path("/tmp/issue181_edge_synth")
    root.mkdir(parents=True, exist_ok=True)
    # Ten pages, two equally common within-line X->Y mappings. Cross-line
    # transitions alternate, so the fixture exercises both pathways without
    # encoding any external target result.
    for i in range(10):
        rows = []
        for j in range(20):
            if j % 2 == 0:
                rows.append("S001 | S002 | S001 | S002")
            else:
                rows.append("S003 | S004 | S003 | S004")
        (root / f"borg_{i:04d}r.canonical.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    r = analyze(root)
    assert r["page_count"] == 10
    assert r["vocabulary_size"] == 4
    assert len(r["folds"]) == 5
    assert all(x["same_line"]["test_event_count"] > 0 for x in r["folds"])
    assert all(x["cross_line"]["test_event_count"] > 0 for x in r["folds"])
    assert r["primary"]["G_line_pass"] is True
    print("SYNTHETIC_EDGE_PREFLIGHT_OK")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--synthetic-preflight", action="store_true")
    args = ap.parse_args()
    if args.synthetic_preflight:
        synthetic_preflight()
        return
    if args.root is None:
        ap.error("root is required unless --synthetic-preflight")
    result = analyze(args.root)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
