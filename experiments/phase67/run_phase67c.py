#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from run_phase67a import (
    CHARS as LEAF_CHARS,
    STATES as LEAF_STATES,
    build_visual,
    center_selected,
    centered_indices,
    clean_tokens,
    residualize_visual_on_coverage,
    rv,
)
from run_phase67b import ROOT_STATES

ROOT_CHAR = "root_subterranean_architecture"
IMAGE_CHARS = list(LEAF_CHARS) + [ROOT_CHAR]
U = "U"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


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


def formal_mask(manifest: dict, text_table: dict):
    by_text = {r["block_id"]: r for r in text_table["records"]}
    history = defaultdict(list)
    retained = {}
    diagnostics = {}

    for block in manifest["blocks"]:
        bid = block["block_id"]
        folio = block["folio"]
        rec = by_text[bid]
        keep = []
        n_clean = n_entry = n_local = 0
        hist = history[folio]
        for li, raw in enumerate(rec["raw_lines"]):
            toks = clean_tokens([raw])
            for tok in toks:
                n_clean += 1
                if li == 0:
                    n_entry += 1
                elif any(lev1(tok, prev) for prev in hist[-10:]):
                    n_local += 1
                else:
                    keep.append(tok)
                hist.append(tok)
                if len(hist) > 10:
                    del hist[:-10]
        retained[bid] = keep
        diagnostics[bid] = {
            "cleaned_tokens": n_clean,
            "entry_masked": n_entry,
            "local_edit1_masked": n_local,
            "innovation_retained": len(keep),
            "retained_fraction": (len(keep) / n_clean) if n_clean else 0.0,
        }
    return retained, diagnostics


def ngram_counts(tokens, n):
    c = Counter()
    for tok in tokens:
        for i in range(len(tok) - n + 1):
            c[tok[i:i+n]] += 1
    return c


def build_residual_text(manifest, text_table, orders=(1, 2, 3)):
    retained, diag = formal_mask(manifest, text_table)
    blocks = [b["block_id"] for b in manifest["blocks"]]
    counts = {
        n: {b: ngram_counts(retained[b], n) for b in blocks}
        for n in orders
    }
    vocabs = {}
    cols = []
    for n in orders:
        df = Counter()
        for b in blocks:
            df.update(counts[n][b].keys())
        V = sorted(g for g, k in df.items() if k >= 2)
        vocabs[n] = V
        A = np.zeros((len(blocks), len(V)), dtype=float)
        for i, b in enumerate(blocks):
            c = counts[n][b]
            total = sum(c[g] for g in V)
            if total:
                A[i] = np.sqrt(np.array([c[g] / total for g in V], dtype=float))
        A /= math.sqrt(len(orders))
        cols.append(A)
    Y = np.concatenate(cols, axis=1) if cols else np.zeros((len(blocks), 0))
    retention = np.array([[diag[b]["retained_fraction"]] for b in blocks], dtype=float)
    totals = {
        k: int(sum(d[k] for d in diag.values()))
        for k in ["cleaned_tokens", "entry_masked", "local_edit1_masked", "innovation_retained"]
    }
    totals["retained_fraction"] = (
        totals["innovation_retained"] / totals["cleaned_tokens"]
        if totals["cleaned_tokens"] else 0.0
    )
    meta = {
        "orders": list(orders),
        "vocab_sizes": {str(n): len(vocabs[n]) for n in orders},
        "block_diagnostics": diag,
        "global_diagnostics": totals,
    }
    return blocks, Y, retention, meta


def build_root_visual(root_table: dict, block_order: list[str]):
    rec = {r["block_id"]: r for r in root_table["records"]}
    X = np.zeros((len(block_order), len(ROOT_STATES)), dtype=float)
    usable = np.zeros(len(block_order), dtype=bool)
    for i, bid in enumerate(block_order):
        states = [o["root_subterranean_architecture"] for o in rec[bid]["objects"]]
        obs = [s for s in states if s != U]
        if obs:
            usable[i] = True
            c = Counter(obs)
            X[i] = np.sqrt(np.array([c[s] / len(obs) for s in ROOT_STATES], dtype=float))
    return X, usable


def build_all_image_predictors(image_table, root_table, blocks):
    leaf_X, _, leaf_usable = build_visual(image_table, blocks)
    root_X, root_usable = build_root_visual(root_table, blocks)
    X = dict(leaf_X)
    usable = dict(leaf_usable)
    X[ROOT_CHAR] = root_X
    usable[ROOT_CHAR] = root_usable
    return X, usable


def char_stats(X, usable, Y, retention, folios):
    idx = centered_indices(folios, usable)
    Xc = center_selected(X, folios, idx)
    Yc = center_selected(Y, folios, idx)
    Rc = center_selected(retention, folios, idx)
    Yres = residualize_visual_on_coverage(Yc, Rc)
    return {
        "rv": rv(Xc, Yc),
        "retention_rv": rv(Xc, Rc),
        "retention_residualized_rv": rv(Xc, Yres),
        "n": int(len(idx)),
        "folios": sorted(set(folios[i] for i in idx)),
    }


def all_within_folio_permutations(folios):
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


def gate(s):
    return s["n"] >= 8 and len(s["folios"]) >= 3


def run(manifest, text_table, image_table, root_table, orders=(1, 2, 3)):
    blocks, Y, retention, text_meta = build_residual_text(manifest, text_table, orders)
    expected_blocks = [b["block_id"] for b in manifest["blocks"]]
    if blocks != expected_blocks:
        raise ValueError("block order mismatch")
    folios = [b["folio"] for b in manifest["blocks"]]
    X_by, usable_by = build_all_image_predictors(image_table, root_table, blocks)

    observed = {
        ch: char_stats(X_by[ch], usable_by[ch], Y, retention, folios)
        for ch in IMAGE_CHARS
    }
    obs_T = max(observed[ch]["rv"] for ch in IMAGE_CHARS)
    winner = max(IMAGE_CHARS, key=lambda ch: observed[ch]["rv"])
    obs_res_T = max(observed[ch]["retention_residualized_rv"] for ch in IMAGE_CHARS)
    res_winner = max(IMAGE_CHARS, key=lambda ch: observed[ch]["retention_residualized_rv"])

    perm_T = []
    perm_res_T = []
    perm_char = {ch: [] for ch in IMAGE_CHARS}
    perm_ret = {ch: [] for ch in IMAGE_CHARS}
    perm_res = {ch: [] for ch in IMAGE_CHARS}
    identity = False

    for perm in all_within_folio_permutations(folios):
        if np.array_equal(perm, np.arange(len(perm))):
            identity = True
        Yp = Y[perm]
        Rp = retention[perm]
        ss = {
            ch: char_stats(X_by[ch], usable_by[ch], Yp, Rp, folios)
            for ch in IMAGE_CHARS
        }
        perm_T.append(max(ss[ch]["rv"] for ch in IMAGE_CHARS))
        perm_res_T.append(max(ss[ch]["retention_residualized_rv"] for ch in IMAGE_CHARS))
        for ch in IMAGE_CHARS:
            perm_char[ch].append(ss[ch]["rv"])
            perm_ret[ch].append(ss[ch]["retention_rv"])
            perm_res[ch].append(ss[ch]["retention_residualized_rv"])

    nperm = len(perm_T)
    expected = math.prod(math.factorial(v) for v in Counter(folios).values())
    if nperm != expected or expected != 1152:
        raise AssertionError((nperm, expected))
    if not identity:
        raise AssertionError("identity missing")

    p_global = float(np.mean(np.array(perm_T) >= obs_T - 1e-15))
    p_res_global = float(np.mean(np.array(perm_res_T) >= obs_res_T - 1e-15))
    p_char = {
        ch: float(np.mean(np.array(perm_char[ch]) >= observed[ch]["rv"] - 1e-15))
        for ch in IMAGE_CHARS
    }
    p_ret = {
        ch: float(np.mean(np.array(perm_ret[ch]) >= observed[ch]["retention_rv"] - 1e-15))
        for ch in IMAGE_CHARS
    }
    p_res = {
        ch: float(np.mean(np.array(perm_res[ch]) >= observed[ch]["retention_residualized_rv"] - 1e-15))
        for ch in IMAGE_CHARS
    }

    primary_gate = gate(observed[winner])
    residual_gate = gate(observed[res_winner])
    if p_global <= 0.05 and primary_gate:
        if p_ret[winner] <= 0.05:
            if p_res_global <= 0.05 and residual_gate:
                classification = "CANDIDATE FORMAL-RESIDUAL IMAGE↔BODY ASSOCIATION AFTER RETENTION RESIDUALIZATION — INDEPENDENT REPLICATION REQUIRED"
            else:
                classification = "TEXT-RETENTION CONFOUNDED"
        else:
            classification = "CANDIDATE FORMAL-RESIDUAL IMAGE↔BODY ASSOCIATION — INDEPENDENT REPLICATION REQUIRED"
    elif p_global <= 0.05 and not primary_gate:
        classification = "UNDERPOWERED / COVERAGE-LIMITED"
    else:
        classification = "NOT SUPPORTED"

    perm_Ta = np.array(perm_T)
    perm_Ra = np.array(perm_res_T)
    return {
        "schema": "phase67c-result-v1",
        "orders": list(orders),
        "n_blocks": len(blocks),
        "permutation_count": nperm,
        "mask": text_meta,
        "observed": observed,
        "primary": {"winner": winner, "maxT": obs_T, "global_exact_p": p_global, "coverage_gate_pass": primary_gate},
        "retention_residualized": {"winner": res_winner, "maxT": obs_res_T, "global_exact_p": p_res_global, "coverage_gate_pass": residual_gate},
        "uncorrected_p": p_char,
        "retention_only_p": p_ret,
        "retention_residualized_uncorrected_p": p_res,
        "classification": classification,
        "null_summary": {
            "maxT_mean": float(perm_Ta.mean()),
            "maxT_q95": float(np.quantile(perm_Ta, 0.95)),
            "maxT_max": float(perm_Ta.max()),
            "residual_maxT_mean": float(perm_Ra.mean()),
            "residual_maxT_q95": float(np.quantile(perm_Ra, 0.95)),
            "residual_maxT_max": float(perm_Ra.max()),
        },
    }


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=here / "BLOCK_MANIFEST_A.json")
    ap.add_argument("--text", type=Path, default=here / "TEXT_TABLE_A.json")
    ap.add_argument("--image", type=Path, default=here / "IMAGE_ANNOTATION_A.json")
    ap.add_argument("--root", type=Path, default=here / "ROOT_ANNOTATION_B.json")
    ap.add_argument("--out", type=Path, default=here / "RESULT_C.json")
    ap.add_argument("--orders", default="1,2,3")
    args = ap.parse_args()
    result = run(
        load_json(args.manifest), load_json(args.text), load_json(args.image), load_json(args.root),
        tuple(int(x) for x in args.orders.split(",") if x)
    )
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": result["classification"],
        "mask_global": result["mask"]["global_diagnostics"],
        "winner": result["primary"]["winner"],
        "maxT": result["primary"]["maxT"],
        "p": result["primary"]["global_exact_p"],
        "retention_winner_p": result["retention_only_p"][result["primary"]["winner"]],
        "residual_winner": result["retention_residualized"]["winner"],
        "residual_maxT": result["retention_residualized"]["maxT"],
        "residual_p": result["retention_residualized"]["global_exact_p"],
        "nperm": result["permutation_count"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
