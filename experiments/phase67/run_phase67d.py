#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from run_phase67a import center_selected, centered_indices, residualize_visual_on_coverage, rv
from run_phase67c import IMAGE_CHARS, build_all_image_predictors, formal_mask, lev1


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_lexical_matrix(manifest, text_table, mode="family"):
    retained, diag = formal_mask(manifest, text_table)
    blocks = [b["block_id"] for b in manifest["blocks"]]
    vocab = sorted({t for b in blocks for t in retained[b]})
    vi = {v: i for i, v in enumerate(vocab)}
    A = np.zeros((len(blocks), len(vocab)), dtype=float)

    if mode == "exact":
        for i, b in enumerate(blocks):
            c = Counter(retained[b])
            for t, n in c.items():
                A[i, vi[t]] = n
    elif mode == "family":
        # Closed edit1 neighborhoods. Precompute vocabulary neighbors once.
        neighborhoods = {}
        for t in vocab:
            neighborhoods[t] = [j for j, v in enumerate(vocab) if t == v or lev1(t, v)]
        for i, b in enumerate(blocks):
            for t in retained[b]:
                for j in neighborhoods[t]:
                    A[i, j] += 1.0
    else:
        raise ValueError(mode)

    for i in range(A.shape[0]):
        s = float(A[i].sum())
        if s:
            A[i] = np.sqrt(A[i] / s)

    retention = np.array([[diag[b]["retained_fraction"]] for b in blocks], dtype=float)
    return blocks, A, retention, {
        "mode": mode,
        "vocabulary_size": len(vocab),
        "retained_type_counts": {b: len(set(retained[b])) for b in blocks},
        "retained_token_counts": {b: len(retained[b]) for b in blocks},
        "retained_fraction": {b: diag[b]["retained_fraction"] for b in blocks},
    }


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


def run(manifest, text_table, image_table, root_table, mode="family"):
    blocks, Y, retention, text_meta = build_lexical_matrix(manifest, text_table, mode)
    folios = [b["folio"] for b in manifest["blocks"]]
    if blocks != [b["block_id"] for b in manifest["blocks"]]:
        raise ValueError("block order mismatch")
    X_by, usable_by = build_all_image_predictors(image_table, root_table, blocks)

    obs = {ch: char_stats(X_by[ch], usable_by[ch], Y, retention, folios) for ch in IMAGE_CHARS}
    obs_T = max(obs[ch]["rv"] for ch in IMAGE_CHARS)
    winner = max(IMAGE_CHARS, key=lambda ch: obs[ch]["rv"])
    obs_res_T = max(obs[ch]["retention_residualized_rv"] for ch in IMAGE_CHARS)
    res_winner = max(IMAGE_CHARS, key=lambda ch: obs[ch]["retention_residualized_rv"])

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
        ss = {ch: char_stats(X_by[ch], usable_by[ch], Yp, Rp, folios) for ch in IMAGE_CHARS}
        perm_T.append(max(ss[ch]["rv"] for ch in IMAGE_CHARS))
        perm_res_T.append(max(ss[ch]["retention_residualized_rv"] for ch in IMAGE_CHARS))
        for ch in IMAGE_CHARS:
            perm_char[ch].append(ss[ch]["rv"])
            perm_ret[ch].append(ss[ch]["retention_rv"])
            perm_res[ch].append(ss[ch]["retention_residualized_rv"])

    expected = math.prod(math.factorial(v) for v in Counter(folios).values())
    if len(perm_T) != expected or expected != 1152:
        raise AssertionError((len(perm_T), expected))
    if not identity:
        raise AssertionError("identity missing")

    pa = np.asarray(perm_T)
    pra = np.asarray(perm_res_T)
    p_global = float(np.mean(pa >= obs_T - 1e-15))
    p_res_global = float(np.mean(pra >= obs_res_T - 1e-15))
    p_char = {ch: float(np.mean(np.asarray(perm_char[ch]) >= obs[ch]["rv"] - 1e-15)) for ch in IMAGE_CHARS}
    p_ret = {ch: float(np.mean(np.asarray(perm_ret[ch]) >= obs[ch]["retention_rv"] - 1e-15)) for ch in IMAGE_CHARS}
    p_res = {ch: float(np.mean(np.asarray(perm_res[ch]) >= obs[ch]["retention_residualized_rv"] - 1e-15)) for ch in IMAGE_CHARS}

    g = gate(obs[winner])
    rg = gate(obs[res_winner])
    if p_global <= 0.05 and g:
        if p_ret[winner] <= 0.05:
            if p_res_global <= 0.05 and rg:
                classification = "CANDIDATE LEXICAL-FAMILY IMAGE↔BODY ASSOCIATION AFTER RETENTION RESIDUALIZATION — INDEPENDENT REPLICATION REQUIRED"
            else:
                classification = "TEXT-RETENTION CONFOUNDED"
        else:
            classification = "CANDIDATE LEXICAL-FAMILY IMAGE↔BODY ASSOCIATION — INDEPENDENT REPLICATION REQUIRED"
    elif p_global <= 0.05 and not g:
        classification = "UNDERPOWERED / COVERAGE-LIMITED"
    else:
        classification = "NOT SUPPORTED"

    return {
        "schema": "phase67d-result-v1",
        "mode": mode,
        "n_blocks": len(blocks),
        "permutation_count": len(pa),
        "text_meta": text_meta,
        "observed": obs,
        "primary": {"winner": winner, "maxT": obs_T, "global_exact_p": p_global, "coverage_gate_pass": g},
        "retention_residualized": {"winner": res_winner, "maxT": obs_res_T, "global_exact_p": p_res_global, "coverage_gate_pass": rg},
        "uncorrected_p": p_char,
        "retention_only_p": p_ret,
        "retention_residualized_uncorrected_p": p_res,
        "classification": classification,
        "null_summary": {
            "maxT_mean": float(pa.mean()),
            "maxT_q95": float(np.quantile(pa, 0.95)),
            "maxT_max": float(pa.max()),
            "residual_maxT_mean": float(pra.mean()),
            "residual_maxT_q95": float(np.quantile(pra, 0.95)),
            "residual_maxT_max": float(pra.max()),
        },
    }


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=here / "BLOCK_MANIFEST_A.json")
    ap.add_argument("--text", type=Path, default=here / "TEXT_TABLE_A.json")
    ap.add_argument("--image", type=Path, default=here / "IMAGE_ANNOTATION_A.json")
    ap.add_argument("--root", type=Path, default=here / "ROOT_ANNOTATION_B.json")
    ap.add_argument("--mode", choices=["family", "exact"], default="family")
    ap.add_argument("--out", type=Path, default=here / "RESULT_D.json")
    args = ap.parse_args()
    result = run(load_json(args.manifest), load_json(args.text), load_json(args.image), load_json(args.root), args.mode)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "mode": result["mode"],
        "classification": result["classification"],
        "vocabulary_size": result["text_meta"]["vocabulary_size"],
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
