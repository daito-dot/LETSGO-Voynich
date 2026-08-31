#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

CHARS = ["leaf_composition", "leaf_arrangement", "leaf_margin"]
STATES = {
    "leaf_composition": [
        "simple", "compound_pinnate", "compound_palmate",
        "deeply_divided_uncertain_leaflet_status",
    ],
    "leaf_arrangement": [
        "alternate", "opposite", "whorled_3plus", "basal_or_rosette",
        "single_or_insufficient_nodes",
    ],
    "leaf_margin": [
        "entire_or_nearly_entire", "serrate_or_dentate",
        "crenate_or_rounded_teeth", "lobed_or_incised",
        "spiny_or_aculeate_margin", "mixed",
    ],
}
U = "U"
UNCERTAIN = set("?[]{}@:<>" )


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def clean_tokens(lines: list[str]) -> list[str]:
    text = " ".join(lines)
    text = text.replace("<%>", " ").replace("<$>", " ")
    text = text.replace("<->", " ")
    parts = re.split(r"[.,\s]+", text)
    out = []
    for tok in parts:
        if not tok:
            continue
        if any(ch in tok for ch in UNCERTAIN):
            continue
        if re.fullmatch(r"[a-z]+", tok):
            out.append(tok)
    return out


def ngram_counts(tokens: list[str], n: int) -> Counter:
    c = Counter()
    for tok in tokens:
        for i in range(len(tok) - n + 1):
            c[tok[i:i+n]] += 1
    return c


def build_text_matrix(text_table: dict, orders=(1, 2, 3)):
    records = text_table["records"]
    tokens_by = {r["block_id"]: clean_tokens(r["raw_lines"]) for r in records}
    counts = {n: {b: ngram_counts(toks, n) for b, toks in tokens_by.items()} for n in orders}
    vocabs = {}
    for n in orders:
        df = Counter()
        for b, c in counts[n].items():
            df.update(c.keys())
        vocabs[n] = sorted(g for g, k in df.items() if k >= 2)

    blocks = [r["block_id"] for r in records]
    cols = []
    for n in orders:
        V = vocabs[n]
        A = np.zeros((len(blocks), len(V)), dtype=float)
        for i, b in enumerate(blocks):
            c = counts[n][b]
            total = sum(c[g] for g in V)
            if total:
                A[i] = np.sqrt(np.array([c[g] / total for g in V], dtype=float))
        A /= math.sqrt(len(orders))
        cols.append(A)
    Y = np.concatenate(cols, axis=1) if cols else np.zeros((len(blocks), 0))
    meta = {
        "orders": list(orders),
        "vocab_sizes": {str(n): len(vocabs[n]) for n in orders},
        "token_counts": {b: len(tokens_by[b]) for b in blocks},
        "tokens": tokens_by,
    }
    return blocks, Y, meta


def validate_image_table(image_table: dict, manifest: dict):
    expected = {b["block_id"]: [o["object_id"] for o in b["fragment_objects"]] for b in manifest["blocks"]}
    got = {r["block_id"]: [o["object_id"] for o in r["objects"]] for r in image_table["records"]}
    if set(expected) != set(got):
        raise ValueError(f"image block IDs mismatch: expected={sorted(expected)} got={sorted(got)}")
    for b in expected:
        if expected[b] != got[b]:
            raise ValueError(f"object order mismatch for {b}: expected={expected[b]} got={got[b]}")
    for r in image_table["records"]:
        for obj in r["objects"]:
            for ch in CHARS:
                s = obj["states"][ch]
                if s != U and s not in STATES[ch]:
                    raise ValueError(f"illegal state {s!r} for {ch} at {r['block_id']}/{obj['object_id']}")


def build_visual(image_table: dict, block_order: list[str]):
    rec = {r["block_id"]: r for r in image_table["records"]}
    X_by = {}
    coverage_by = {}
    usable_by = {}
    for ch in CHARS:
        V = STATES[ch]
        X = np.zeros((len(block_order), len(V)), dtype=float)
        coverage = np.zeros(len(block_order), dtype=float)
        usable = np.zeros(len(block_order), dtype=bool)
        for i, b in enumerate(block_order):
            states = [o["states"][ch] for o in rec[b]["objects"]]
            obs = [s for s in states if s != U]
            coverage[i] = len(obs) / len(states) if states else 0.0
            if obs:
                usable[i] = True
                c = Counter(obs)
                X[i] = np.sqrt(np.array([c[s] / len(obs) for s in V], dtype=float))
        X_by[ch] = X
        coverage_by[ch] = coverage[:, None]
        usable_by[ch] = usable
    return X_by, coverage_by, usable_by


def center_within_folio(X, Y, folios, usable):
    idx = []
    for f in sorted(set(folios)):
        members = [i for i, ff in enumerate(folios) if ff == f and usable[i]]
        if len(members) >= 2:
            idx.extend(members)
    idx = np.array(sorted(idx), dtype=int)
    if len(idx) == 0:
        return np.zeros((0, X.shape[1])), np.zeros((0, Y.shape[1])), idx
    Xc = X[idx].copy()
    Yc = Y[idx].copy()
    fi = [folios[i] for i in idx]
    for f in sorted(set(fi)):
        local = np.array([j for j, ff in enumerate(fi) if ff == f], dtype=int)
        Xc[local] -= Xc[local].mean(axis=0, keepdims=True)
        Yc[local] -= Yc[local].mean(axis=0, keepdims=True)
    return Xc, Yc, idx


def rv(X, Y):
    if X.shape[0] < 2 or Y.shape[1] == 0:
        return 0.0
    xy = X.T @ Y
    xx = X.T @ X
    yy = Y.T @ Y
    denom = math.sqrt(float(np.sum(xx * xx)) * float(np.sum(yy * yy)))
    return float(np.sum(xy * xy) / denom) if denom else 0.0


def stats_for_assignment(Y_assigned, X_by, coverage_by, usable_by, folios):
    rv_by = {}
    cov_rv_by = {}
    n_by = {}
    folio_by = {}
    for ch in CHARS:
        Xc, Yc, idx = center_within_folio(X_by[ch], Y_assigned, folios, usable_by[ch])
        rv_by[ch] = rv(Xc, Yc)
        n_by[ch] = int(len(idx))
        folio_by[ch] = sorted(set(folios[i] for i in idx))
        Cc, CY, _ = center_within_folio(coverage_by[ch], Y_assigned, folios, usable_by[ch])
        cov_rv_by[ch] = rv(Cc, CY)
    return rv_by, cov_rv_by, n_by, folio_by


def all_within_folio_permutations(folios: list[str]):
    groups = []
    for f in dict.fromkeys(folios):
        idx = [i for i, ff in enumerate(folios) if ff == f]
        groups.append((idx, list(itertools.permutations(idx))))
    for choices in itertools.product(*(g[1] for g in groups)):
        perm = list(range(len(folios)))
        for (idx, _), chosen in zip(groups, choices):
            for dest, src in zip(idx, chosen):
                perm[dest] = src
        yield np.array(perm, dtype=int)


def coverage_gate(n, contributing_folios):
    return n >= 8 and len(contributing_folios) >= 3


def run(manifest, text_table, image_table, orders=(1, 2, 3)):
    validate_image_table(image_table, manifest)
    blocks, Y, text_meta = build_text_matrix(text_table, orders=orders)
    manifest_blocks = [b["block_id"] for b in manifest["blocks"]]
    if blocks != manifest_blocks:
        raise ValueError("TEXT_TABLE_A record order must equal BLOCK_MANIFEST_A block order")
    folios = [b["folio"] for b in manifest["blocks"]]
    X_by, coverage_by, usable_by = build_visual(image_table, blocks)

    obs_rv, obs_cov_rv, n_by, folio_by = stats_for_assignment(Y, X_by, coverage_by, usable_by, folios)
    obs_T = max(obs_rv.values())
    winner = max(CHARS, key=lambda ch: obs_rv[ch])

    perm_T = []
    perm_cov = {ch: [] for ch in CHARS}
    perm_rv = {ch: [] for ch in CHARS}
    nperm = 0
    identity_found = False
    for perm in all_within_folio_permutations(folios):
        nperm += 1
        if np.array_equal(perm, np.arange(len(perm))):
            identity_found = True
        rv_by, cov_by, _, _ = stats_for_assignment(Y[perm], X_by, coverage_by, usable_by, folios)
        perm_T.append(max(rv_by.values()))
        for ch in CHARS:
            perm_rv[ch].append(rv_by[ch])
            perm_cov[ch].append(cov_by[ch])

    expected_nperm = math.prod(math.factorial(v) for v in Counter(folios).values())
    if nperm != expected_nperm:
        raise AssertionError((nperm, expected_nperm))
    if not identity_found:
        raise AssertionError("identity assignment missing")

    perm_T = np.array(perm_T)
    p_global = float(np.mean(perm_T >= obs_T - 1e-15))
    p_char = {ch: float(np.mean(np.array(perm_rv[ch]) >= obs_rv[ch] - 1e-15)) for ch in CHARS}
    p_cov = {ch: float(np.mean(np.array(perm_cov[ch]) >= obs_cov_rv[ch] - 1e-15)) for ch in CHARS}

    gate = coverage_gate(n_by[winner], folio_by[winner])
    if p_global <= 0.05 and gate:
        classification = "DETECTED"
        if p_cov[winner] <= 0.05:
            classification = "MORPHOLOGY / OBSERVABILITY CONFOUNDED"
    elif p_global <= 0.05 and not gate:
        classification = "UNDERPOWERED / COVERAGE-LIMITED"
    else:
        classification = "NOT SUPPORTED"

    return {
        "schema": "phase67a-result-v1",
        "orders": list(orders),
        "n_blocks": len(blocks),
        "permutation_count": nperm,
        "observed": {
            "rv_by_character": obs_rv,
            "coverage_rv_by_character": obs_cov_rv,
            "maxT": obs_T,
            "winner": winner,
            "usable_blocks": n_by,
            "contributing_folios": folio_by,
        },
        "p_values": {
            "global_maxT": p_global,
            "character_uncorrected": p_char,
            "coverage_control_uncorrected": p_cov,
        },
        "operational_gate_pass": gate,
        "classification": classification,
        "text_meta": text_meta,
        "null_summary": {
            "maxT_mean": float(perm_T.mean()),
            "maxT_q95": float(np.quantile(perm_T, 0.95)),
            "maxT_max": float(perm_T.max()),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=Path(__file__).with_name("BLOCK_MANIFEST_A.json"))
    ap.add_argument("--text", type=Path, default=Path(__file__).with_name("TEXT_TABLE_A.json"))
    ap.add_argument("--image", type=Path, default=Path(__file__).with_name("IMAGE_ANNOTATION_A.json"))
    ap.add_argument("--out", type=Path, default=Path(__file__).with_name("RESULT_A.json"))
    ap.add_argument("--orders", default="1,2,3")
    args = ap.parse_args()
    orders = tuple(int(x) for x in args.orders.split(",") if x)
    result = run(load_json(args.manifest), load_json(args.text), load_json(args.image), orders=orders)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": result["classification"],
        "maxT": result["observed"]["maxT"],
        "p_global": result["p_values"]["global_maxT"],
        "winner": result["observed"]["winner"],
        "nperm": result["permutation_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
