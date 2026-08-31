#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PHASE67 = HERE.parent / "phase67"
sys.path.insert(0, str(PHASE67))

from run_phase67a import center_selected, centered_indices, residualize_visual_on_coverage, rv  # noqa: E402
from run_phase67c import (  # noqa: E402
    IMAGE_CHARS,
    build_all_image_predictors,
    formal_mask,
    lev1,
)

LANES = ("exact_token", "edit1_anchor_family")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def hellinger_rows(A: np.ndarray) -> np.ndarray:
    out = np.zeros_like(A, dtype=float)
    sums = A.sum(axis=1)
    nz = sums > 0
    if np.any(nz):
        out[nz] = np.sqrt(A[nz] / sums[nz, None])
    return out


def build_lexical(manifest: dict, text_table: dict):
    retained, mask_diag = formal_mask(manifest, text_table)
    blocks = [b["block_id"] for b in manifest["blocks"]]

    df = Counter()
    all_types = set()
    for bid in blocks:
        toks = retained[bid]
        all_types.update(toks)
        df.update(set(toks))
    vocab = sorted(t for t, n in df.items() if n >= 2)
    vidx = {t: i for i, t in enumerate(vocab)}

    exact_counts = np.zeros((len(blocks), len(vocab)), dtype=float)
    family_counts = np.zeros((len(blocks), len(vocab)), dtype=float)
    retention = np.zeros((len(blocks), 1), dtype=float)
    per_block = {}

    for i, bid in enumerate(blocks):
        toks = retained[bid]
        for t in toks:
            j = vidx.get(t)
            if j is not None:
                exact_counts[i, j] += 1.0
            for k, anchor in enumerate(vocab):
                if t == anchor or lev1(t, anchor):
                    family_counts[i, k] += 1.0
        retention[i, 0] = mask_diag[bid]["retained_fraction"]
        exact_hits = int(exact_counts[i].sum())
        family_hits = int(family_counts[i].sum())
        per_block[bid] = {
            "retained_tokens": len(toks),
            "retained_distinct_types": len(set(toks)),
            "exact_vocab_occurrences": exact_hits,
            "exact_vocab_fraction_of_retained": (exact_hits / len(toks)) if toks else 0.0,
            "edit1_anchor_hits": family_hits,
            "L1_nonzero": bool(exact_hits),
            "L2_nonzero": bool(family_hits),
        }

    lanes = {
        "exact_token": hellinger_rows(exact_counts),
        "edit1_anchor_family": hellinger_rows(family_counts),
    }

    l1_nonzero = int(np.sum(exact_counts.sum(axis=1) > 0))
    l2_nonzero = int(np.sum(family_counts.sum(axis=1) > 0))
    feasibility = {
        "vocab_size_ge_5": len(vocab) >= 5,
        "L1_nonzero_paragraphs_ge_10": l1_nonzero >= 10,
        "L2_nonzero_paragraphs_ge_10": l2_nonzero >= 10,
    }
    feasibility["pass"] = all(feasibility.values())

    meta = {
        "retained_token_total": int(sum(len(retained[b]) for b in blocks)),
        "retained_distinct_types": len(all_types),
        "vocab_document_frequency_threshold": 2,
        "vocab_size": len(vocab),
        "vocab": vocab,
        "L1_nonzero_paragraphs": l1_nonzero,
        "L2_nonzero_paragraphs": l2_nonzero,
        "feasibility": feasibility,
        "formal_mask_global": {
            k: int(sum(d[k] for d in mask_diag.values()))
            for k in ["cleaned_tokens", "entry_masked", "local_edit1_masked", "innovation_retained"]
        },
        "per_block": per_block,
    }
    clean_total = meta["formal_mask_global"]["cleaned_tokens"]
    meta["formal_mask_global"]["retained_fraction"] = (
        meta["formal_mask_global"]["innovation_retained"] / clean_total if clean_total else 0.0
    )
    return blocks, lanes, retention, meta


def cell_stats(X, usable, Y, retention, folios):
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
        yield np.asarray(perm, dtype=int)


def coverage_gate(s):
    return s["n"] >= 8 and len(s["folios"]) >= 3


def run(manifest, text_table, image_table, root_table):
    blocks, lane_Y, retention, lexical_meta = build_lexical(manifest, text_table)
    expected_blocks = [b["block_id"] for b in manifest["blocks"]]
    if blocks != expected_blocks:
        raise ValueError("block order mismatch")

    if not lexical_meta["feasibility"]["pass"]:
        return {
            "schema": "phase68a-result-v1",
            "classification": "BLOCKED / LEXICAL REPRESENTATION TOO SPARSE",
            "n_blocks": len(blocks),
            "lexical_meta": lexical_meta,
        }

    folios = [b["folio"] for b in manifest["blocks"]]
    X_by, usable_by = build_all_image_predictors(image_table, root_table, blocks)

    observed = {}
    for ch in IMAGE_CHARS:
        observed[ch] = {}
        for lane in LANES:
            observed[ch][lane] = cell_stats(
                X_by[ch], usable_by[ch], lane_Y[lane], retention, folios
            )

    cells = [(ch, lane) for ch in IMAGE_CHARS for lane in LANES]
    winner = max(cells, key=lambda z: observed[z[0]][z[1]]["rv"])
    obs_T = observed[winner[0]][winner[1]]["rv"]
    res_winner = max(cells, key=lambda z: observed[z[0]][z[1]]["retention_residualized_rv"])
    obs_res_T = observed[res_winner[0]][res_winner[1]]["retention_residualized_rv"]

    perm_T = []
    perm_res_T = []
    perm_cell = {z: [] for z in cells}
    perm_res_cell = {z: [] for z in cells}
    perm_ret = {ch: [] for ch in IMAGE_CHARS}
    identity = False

    for perm in all_within_folio_permutations(folios):
        if np.array_equal(perm, np.arange(len(perm))):
            identity = True
        Rp = retention[perm]
        ss = {}
        for ch in IMAGE_CHARS:
            ss[ch] = {}
            for lane in LANES:
                ss[ch][lane] = cell_stats(
                    X_by[ch], usable_by[ch], lane_Y[lane][perm], Rp, folios
                )
        perm_T.append(max(ss[ch][lane]["rv"] for ch, lane in cells))
        perm_res_T.append(
            max(ss[ch][lane]["retention_residualized_rv"] for ch, lane in cells)
        )
        for z in cells:
            ch, lane = z
            perm_cell[z].append(ss[ch][lane]["rv"])
            perm_res_cell[z].append(ss[ch][lane]["retention_residualized_rv"])
        for ch in IMAGE_CHARS:
            # retention RV is lane-invariant; use the first lane's calculation.
            perm_ret[ch].append(ss[ch][LANES[0]]["retention_rv"])

    expected_n = math.prod(math.factorial(v) for v in Counter(folios).values())
    if len(perm_T) != expected_n or expected_n != 1152:
        raise AssertionError((len(perm_T), expected_n))
    if not identity:
        raise AssertionError("identity permutation missing")

    perm_Ta = np.asarray(perm_T)
    perm_Ra = np.asarray(perm_res_T)
    p_global = float(np.mean(perm_Ta >= obs_T - 1e-15))
    p_res_global = float(np.mean(perm_Ra >= obs_res_T - 1e-15))

    p_cell = {
        f"{ch}::{lane}": float(
            np.mean(np.asarray(perm_cell[(ch, lane)]) >= observed[ch][lane]["rv"] - 1e-15)
        )
        for ch, lane in cells
    }
    p_res_cell = {
        f"{ch}::{lane}": float(
            np.mean(
                np.asarray(perm_res_cell[(ch, lane)])
                >= observed[ch][lane]["retention_residualized_rv"] - 1e-15
            )
        )
        for ch, lane in cells
    }
    p_ret = {
        ch: float(
            np.mean(
                np.asarray(perm_ret[ch])
                >= observed[ch][LANES[0]]["retention_rv"] - 1e-15
            )
        )
        for ch in IMAGE_CHARS
    }

    primary_stat = observed[winner[0]][winner[1]]
    residual_stat = observed[res_winner[0]][res_winner[1]]
    primary_gate = coverage_gate(primary_stat)
    residual_gate = coverage_gate(residual_stat)

    if p_global <= 0.05 and primary_gate:
        if p_ret[winner[0]] <= 0.05:
            if p_res_global <= 0.05 and residual_gate:
                classification = (
                    "CANDIDATE FORMAL-RESIDUAL LEXICAL IMAGE↔BODY ASSOCIATION "
                    "AFTER RETENTION RESIDUALIZATION — INDEPENDENT REPLICATION REQUIRED"
                )
            else:
                classification = "TEXT-RETENTION CONFOUNDED"
        else:
            classification = (
                "CANDIDATE FORMAL-RESIDUAL LEXICAL IMAGE↔BODY ASSOCIATION — "
                "INDEPENDENT REPLICATION REQUIRED"
            )
    elif p_global <= 0.05 and not primary_gate:
        classification = "UNDERPOWERED / IMAGE-COVERAGE LIMITED"
    else:
        classification = "NOT SUPPORTED"

    return {
        "schema": "phase68a-result-v1",
        "classification": classification,
        "n_blocks": len(blocks),
        "permutation_count": int(len(perm_Ta)),
        "lexical_meta": lexical_meta,
        "observed": observed,
        "primary": {
            "winner_character": winner[0],
            "winner_lane": winner[1],
            "maxT": obs_T,
            "global_exact_p": p_global,
            "coverage_gate_pass": primary_gate,
        },
        "retention_residualized": {
            "winner_character": res_winner[0],
            "winner_lane": res_winner[1],
            "maxT": obs_res_T,
            "global_exact_p": p_res_global,
            "coverage_gate_pass": residual_gate,
        },
        "uncorrected_cell_p": p_cell,
        "retention_only_p_by_character": p_ret,
        "retention_residualized_cell_p": p_res_cell,
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=PHASE67 / "BLOCK_MANIFEST_A.json")
    ap.add_argument("--text", type=Path, default=PHASE67 / "TEXT_TABLE_A.json")
    ap.add_argument("--image", type=Path, default=PHASE67 / "IMAGE_ANNOTATION_A.json")
    ap.add_argument("--root", type=Path, default=PHASE67 / "ROOT_ANNOTATION_B.json")
    ap.add_argument("--out", type=Path, default=HERE / "RESULT_A.json")
    args = ap.parse_args()

    result = run(
        load_json(args.manifest),
        load_json(args.text),
        load_json(args.image),
        load_json(args.root),
    )
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "classification": result["classification"],
        "lexical_feasibility": result["lexical_meta"]["feasibility"],
        "vocab_size": result["lexical_meta"]["vocab_size"],
        "L1_nonzero": result["lexical_meta"]["L1_nonzero_paragraphs"],
        "L2_nonzero": result["lexical_meta"]["L2_nonzero_paragraphs"],
    }
    if "primary" in result:
        summary.update({
            "winner_character": result["primary"]["winner_character"],
            "winner_lane": result["primary"]["winner_lane"],
            "maxT": result["primary"]["maxT"],
            "p": result["primary"]["global_exact_p"],
            "residual_p": result["retention_residualized"]["global_exact_p"],
            "nperm": result["permutation_count"],
        })
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
