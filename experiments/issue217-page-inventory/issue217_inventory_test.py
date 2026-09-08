#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import itertools
import json
import math
import re
from pathlib import Path

H_FOLIOS = ("f87", "f90", "f93", "f96")
P_FOLIOS = ("f88", "f89", "f99", "f100", "f101", "f102")
FOLIOS = H_FOLIOS + P_FOLIOS
OBS_H = frozenset(H_FOLIOS)

PAGE_RE = re.compile(r"^(f\d+[rv]\d*)$")
LOCUS_RE = re.compile(r"^<(?P<page>f\d+[rv]\d*)\.[^,>]+,(?P<code>[^>]+)>\s*(?P<text>.*)$")
FOLIO_RE = re.compile(r"^(f\d+)")
ALT_RE = re.compile(r"\[([^:\]]+):[^\]]+\]")
COMMENT_RE = re.compile(r"\{[^}]*\}")
ANGLE_RE = re.compile(r"<[^>]*>")
TOKEN_RE = re.compile(r"[a-z]+")


def physical_folio(page_id: str) -> str | None:
    m = FOLIO_RE.match(page_id)
    return m.group(1) if m else None


def is_paragraph_code(code: str) -> bool:
    # IVTFF locus codes include a position marker followed by locus type,
    # e.g. @P0, +P0, =P0. P is the running-paragraph locus type.
    return bool(re.search(r"(?:^|[@+=*])P\d*$", code))


def clean_tokens(text: str) -> list[str]:
    text = COMMENT_RE.sub(" ", text)
    # Deterministically retain the first IVTFF alternative.
    for _ in range(4):
        new = ALT_RE.sub(lambda m: m.group(1), text)
        if new == text:
            break
        text = new
    text = ANGLE_RE.sub(" ", text)
    text = text.replace(".", " ").replace(",", " ").lower()
    return [tok for tok in text.split() if TOKEN_RE.fullmatch(tok)]


def parse_folios(path: Path) -> tuple[dict[str, collections.Counter[str]], dict[str, int]]:
    counts = {f: collections.Counter() for f in FOLIOS}
    loci = collections.Counter()
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = LOCUS_RE.match(raw)
        if not m or not is_paragraph_code(m.group("code")):
            continue
        folio = physical_folio(m.group("page"))
        if folio not in counts:
            continue
        toks = clean_tokens(m.group("text"))
        counts[folio].update(toks)
        loci[folio] += 1
    return counts, dict(loci)


def normalize(counter: collections.Counter[str]) -> dict[str, float]:
    total = sum(counter.values())
    if total <= 0:
        return {}
    return {k: v / total for k, v in counter.items()}


def js_bits(p: dict[str, float], q: dict[str, float]) -> float:
    keys = set(p) | set(q)
    out = 0.0
    for k in keys:
        a = p.get(k, 0.0)
        b = q.get(k, 0.0)
        m = 0.5 * (a + b)
        if a > 0:
            out += 0.5 * a * math.log2(a / m)
        if b > 0:
            out += 0.5 * b * math.log2(b / m)
    return out


def centroid(docs: list[dict[str, float]]) -> dict[str, float]:
    if not docs:
        raise ValueError("empty centroid class")
    c = collections.defaultdict(float)
    w = 1.0 / len(docs)
    for d in docs:
        for k, v in d.items():
            c[k] += w * v
    return dict(c)


def separation(docs: dict[str, dict[str, float]], h_set: frozenset[str]) -> dict[str, float]:
    h = sorted(h_set)
    p = sorted(set(FOLIOS) - set(h_set))
    cross = [js_bits(docs[a], docs[b]) for a in h for b in p]
    within = [js_bits(docs[a], docs[b]) for a, b in itertools.combinations(h, 2)]
    within += [js_bits(docs[a], docs[b]) for a, b in itertools.combinations(p, 2)]
    mc = sum(cross) / len(cross)
    mw = sum(within) / len(within)
    return {"mean_cross_js_bits": mc, "mean_within_js_bits": mw, "T": mc - mw}


def balanced_accuracy(truth: dict[str, str], pred: dict[str, str]) -> float:
    recalls = []
    for cls in ("H", "P"):
        members = [f for f in FOLIOS if truth[f] == cls]
        recalls.append(sum(pred[f] == cls for f in members) / len(members))
    return sum(recalls) / 2.0


def lofo_ba(docs: dict[str, dict[str, float]], h_set: frozenset[str]) -> float:
    truth = {f: ("H" if f in h_set else "P") for f in FOLIOS}
    pred = {}
    for held in FOLIOS:
        train_h = [docs[f] for f in FOLIOS if f != held and truth[f] == "H"]
        train_p = [docs[f] for f in FOLIOS if f != held and truth[f] == "P"]
        ch = centroid(train_h)
        cp = centroid(train_p)
        dh = js_bits(docs[held], ch)
        dp = js_bits(docs[held], cp)
        pred[held] = "H" if dh < dp else "P"
    return balanced_accuracy(truth, pred)


def analyze(path: Path, reading: str) -> dict:
    counts, loci = parse_folios(path)
    missing = [f for f in FOLIOS if sum(counts[f].values()) == 0]
    if missing:
        return {"reading": reading, "comparable": False, "missing_folios": missing}

    docs = {f: normalize(counts[f]) for f in FOLIOS}
    assignments = [frozenset(x) for x in itertools.combinations(FOLIOS, 4)]
    obs_sep = separation(docs, OBS_H)
    sep_null = [separation(docs, h)["T"] for h in assignments]
    p_sep = sum(x >= obs_sep["T"] - 1e-15 for x in sep_null) / len(sep_null)

    obs_ba = lofo_ba(docs, OBS_H)
    ba_null = [lofo_ba(docs, h) for h in assignments]
    p_ba = sum(x >= obs_ba - 1e-15 for x in ba_null) / len(ba_null)

    vocab = sorted(set().union(*(set(c) for c in counts.values())))
    return {
        "reading": reading,
        "comparable": True,
        "folio_token_counts": {f: sum(counts[f].values()) for f in FOLIOS},
        "folio_paragraph_loci": {f: loci.get(f, 0) for f in FOLIOS},
        "union_vocabulary_types": len(vocab),
        "primary": {
            **obs_sep,
            "exact_assignments": len(assignments),
            "exact_one_sided_p": p_sep,
            "pass": bool(obs_sep["T"] > 0 and p_sep <= 0.05),
        },
        "lofo_nearest_centroid": {
            "balanced_accuracy": obs_ba,
            "exact_assignments": len(assignments),
            "exact_one_sided_p": p_ba,
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zl3b", type=Path, required=True)
    ap.add_argument("--it2a", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    zl = analyze(args.zl3b, "ZL3b")
    it = analyze(args.it2a, "IT2a")
    if not zl.get("comparable") or not it.get("comparable"):
        classification = "READING_NONCOMPARABLE"
    elif not zl["primary"]["pass"]:
        classification = "NO_DETECTED_PAGE_INVENTORY_ASSOCIATION"
    elif it["primary"]["T"] > 0 and it["primary"]["exact_one_sided_p"] <= 0.05:
        classification = "REPLICATED_PAGE_INVENTORY_ASSOCIATION"
    else:
        classification = "PRIMARY_ONLY_NOT_REPLICATED"

    result = {
        "issue": 217,
        "population": {
            "section": "pharmaceutical", "currier": "A", "hand": "1",
            "H_folios": list(H_FOLIOS), "P_folios": list(P_FOLIOS),
            "permutation_unit": "physical_folio",
        },
        "tokenization": "Issue #217 frozen generic IVTFF paragraph-token cleaner",
        "classification": classification,
        "ZL3b": zl,
        "IT2a": it,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
