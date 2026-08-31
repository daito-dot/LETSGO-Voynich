#!/usr/bin/env python3
"""Issue #26 experiment B: Ptolemaic tonos↔zodiac pairing test.

Implements PLAN_B.md + parser amendment B1 + representation amendment B2.
Scientific result is written as JSON to stdout.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"

PAGE_TO_SIGN = {
    135: "Pisces",
    136: "Aries",
    137: "Aries",
    138: "Taurus",
    139: "Taurus",
    140: "Gemini",
    141: "Cancer",
    142: "Leo",
    143: "Virgo",
    144: "Libra",
    145: "Scorpio",
    146: "Sagittarius",
}
SIGN_POSITION = {
    "Pisces": 135.0,
    "Aries": 136.5,
    "Taurus": 138.5,
    "Gemini": 140.0,
    "Cancer": 141.0,
    "Leo": 142.0,
    "Virgo": 143.0,
    "Libra": 144.0,
    "Scorpio": 145.0,
    "Sagittarius": 146.0,
}
TARGET_PAIRS = (
    ("Gemini", "Leo"),
    ("Taurus", "Virgo"),
    ("Aries", "Libra"),
    ("Pisces", "Scorpio"),
)
TARGET_SIGNS = tuple(sorted({x for p in TARGET_PAIRS for x in p}))

PAGE_RE = re.compile(r"^# page\s+(\d+)\s*$")
LOCUS_RE = re.compile(r"^<[^>]+,([^>]*)>\s*(.*)$")
ANGLE_RE = re.compile(r"<![^>]*>|<[^>]*>")
BRACE_RE = re.compile(r"\{[^}]*\}")
BRACKET_ALT_RE = re.compile(r"\[([^:\]]*):[^\]]*\]")
BRACKET_RE = re.compile(r"\[([^\]]*)\]")


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_lz_body(body: str) -> List[str]:
    body = ANGLE_RE.sub(" ", body)
    body = BRACKET_ALT_RE.sub(lambda m: f" {m.group(1)} ", body)
    body = BRACKET_RE.sub(lambda m: f" {m.group(1)} ", body)
    body = BRACE_RE.sub(" ", body)
    body = re.sub(r"[^A-Za-z.\s]", " ", body)
    return [x.lower() for x in re.split(r"[.\s]+", body) if x and x.isalpha()]


def parse_labels(path: Path) -> Dict[str, List[str]]:
    by_sign: Dict[str, List[str]] = {s: [] for s in SIGN_POSITION}
    page = None
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        pm = PAGE_RE.match(raw)
        if pm:
            page = int(pm.group(1))
            continue
        if page not in PAGE_TO_SIGN:
            continue
        lm = LOCUS_RE.match(raw)
        if not lm:
            continue
        code, body = lm.group(1), lm.group(2)
        if "Lz" not in code:
            continue
        by_sign[PAGE_TO_SIGN[page]].extend(normalize_lz_body(body))
    missing = [s for s, toks in by_sign.items() if not toks]
    if missing:
        raise RuntimeError(f"no Lz tokens for signs: {missing}")
    return by_sign


def ngram_counts(tokens: Sequence[str], n: int) -> Counter[str]:
    c: Counter[str] = Counter()
    for tok in tokens:
        for i in range(len(tok) - n + 1):
            c[tok[i:i+n]] += 1
    return c


def unit_l2_relative(counts: Counter[str], vocab: Sequence[str]) -> List[float]:
    total = sum(counts.values())
    if total <= 0:
        return [0.0] * len(vocab)
    v = [counts[g] / total for g in vocab]
    norm = math.sqrt(sum(x*x for x in v))
    return [x / norm for x in v] if norm > 0 else v


def build_vectors(by_sign: Dict[str, List[str]], mode: str = "combined") -> Dict[str, List[float]]:
    unigrams = list("abcdefghijklmnopqrstuvwxyz")
    bigram_vocab = sorted({g for toks in by_sign.values() for g in ngram_counts(toks, 2)})
    out: Dict[str, List[float]] = {}
    for sign, toks in by_sign.items():
        u = unit_l2_relative(ngram_counts(toks, 1), unigrams)
        b = unit_l2_relative(ngram_counts(toks, 2), bigram_vocab)
        if mode == "unigram":
            out[sign] = u
        elif mode == "bigram":
            out[sign] = b
        elif mode == "combined":
            k = 1.0 / math.sqrt(2.0)
            out[sign] = [k*x for x in u] + [k*x for x in b]
        else:
            raise ValueError(mode)
    return out


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x*y for x, y in zip(a, b)) / (na*nb)


def all_pair_rows(vectors: Dict[str, List[float]]) -> List[dict]:
    rows = []
    signs = sorted(vectors)
    for a, b in itertools.combinations(signs, 2):
        rows.append({
            "a": a,
            "b": b,
            "page_distance": abs(SIGN_POSITION[a] - SIGN_POSITION[b]),
            "similarity": cosine(vectors[a], vectors[b]),
        })
    return rows


def ols_residualize(rows: List[dict]) -> Tuple[float, float]:
    xs = [r["page_distance"] for r in rows]
    ys = [r["similarity"] for r in rows]
    mx = sum(xs)/len(xs)
    my = sum(ys)/len(ys)
    denom = sum((x-mx)**2 for x in xs)
    b = sum((x-mx)*(y-my) for x, y in zip(xs, ys))/denom if denom else 0.0
    a = my - b*mx
    for r in rows:
        r["fitted"] = a + b*r["page_distance"]
        r["residual"] = r["similarity"] - r["fitted"]
    return a, b


def pair_key(a: str, b: str) -> Tuple[str, str]:
    return tuple(sorted((a, b)))  # type: ignore[return-value]


def residual_map(rows: Sequence[dict]) -> Dict[Tuple[str, str], float]:
    return {pair_key(r["a"], r["b"]): r["residual"] for r in rows}


def similarity_map(rows: Sequence[dict]) -> Dict[Tuple[str, str], float]:
    return {pair_key(r["a"], r["b"]): r["similarity"] for r in rows}


def perfect_matchings(items: Tuple[str, ...]):
    if not items:
        yield ()
        return
    first = items[0]
    for i in range(1, len(items)):
        second = items[i]
        rest = items[1:i] + items[i+1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def score_matching(mapping: Dict[Tuple[str, str], float], pairs: Sequence[Tuple[str, str]]) -> float:
    return sum(mapping[pair_key(a,b)] for a,b in pairs) / len(pairs)


def evaluate(by_sign: Dict[str, List[str]], mode: str, residualize: bool = True) -> dict:
    vectors = build_vectors(by_sign, mode)
    rows = all_pair_rows(vectors)
    intercept, slope = ols_residualize(rows)
    value_map = residual_map(rows) if residualize else similarity_map(rows)
    target = score_matching(value_map, TARGET_PAIRS)
    matchings = list(perfect_matchings(TARGET_SIGNS))
    scores = [score_matching(value_map, p) for p in matchings]
    p_ge = sum(x >= target - 1e-15 for x in scores) / len(scores)
    rank_desc = 1 + sum(x > target + 1e-15 for x in scores)
    target_detail = []
    rowmap = {pair_key(r["a"], r["b"]): r for r in rows}
    for a,b in TARGET_PAIRS:
        rr = rowmap[pair_key(a,b)]
        target_detail.append({
            "pair": [a,b],
            "page_distance": rr["page_distance"],
            "similarity": rr["similarity"],
            "fitted": rr["fitted"],
            "residual": rr["residual"],
        })
    return {
        "mode": mode,
        "residualized": residualize,
        "chronology_ols": {"intercept": intercept, "slope_per_page_distance": slope},
        "target_score": target,
        "exact_matchings": len(scores),
        "exact_p_ge": p_ge,
        "rank_desc": rank_desc,
        "null_min": min(scores),
        "null_mean": sum(scores)/len(scores),
        "null_max": max(scores),
        "target_pairs": target_detail,
    }


def leave_one_pair_out(by_sign: Dict[str, List[str]]) -> List[dict]:
    vectors = build_vectors(by_sign, "combined")
    rows = all_pair_rows(vectors)
    ols_residualize(rows)
    rmap = residual_map(rows)
    out = []
    for omitted in TARGET_PAIRS:
        kept = [p for p in TARGET_PAIRS if p != omitted]
        out.append({"omitted": list(omitted), "mean_residual_kept": score_matching(rmap, kept)})
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt", file=sys.stderr)
        return 2
    source = Path(sys.argv[1]).resolve()
    if git_blob_sha1(source.read_bytes()) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b blob mismatch")
    here = Path(__file__).resolve().parent
    by_sign = parse_labels(source)
    primary = evaluate(by_sign, "combined", residualize=True)
    classification = (
        "SUPPORTED CANDIDATE RELATION"
        if primary["exact_p_ge"] <= 0.05 and primary["target_score"] > 0
        else "NOT SUPPORTED"
    )
    result = {
        "experiment": "Issue26B Ptolemaic tonos-zodiac pairing",
        "issue": 26,
        "inputs": {
            "zl3b_git_blob_sha1": EXPECTED_ZL3B_BLOB,
            "plan_sha256": sha256_file(here / "PLAN_B.md"),
            "parser_amendment_sha256": sha256_file(here / "PARSER_AMENDMENT_B1.md"),
            "representation_amendment_sha256": sha256_file(here / "REPRESENTATION_AMENDMENT_B2.md"),
            "script_sha256": sha256_file(Path(__file__)),
        },
        "population": {
            "tokens_per_sign": {s: len(t) for s,t in sorted(by_sign.items())},
            "target_signs": list(TARGET_SIGNS),
            "target_pairs": [list(p) for p in TARGET_PAIRS],
        },
        "primary": primary,
        "sensitivities": {
            "unigram_only": evaluate(by_sign, "unigram", residualize=True),
            "bigram_only": evaluate(by_sign, "bigram", residualize=True),
            "raw_combined_no_chronology_residual": evaluate(by_sign, "combined", residualize=False),
            "leave_one_target_pair_out": leave_one_pair_out(by_sign),
        },
        "frozen_classification": classification,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
