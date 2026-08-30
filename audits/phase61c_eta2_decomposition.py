#!/usr/bin/env python3
"""Audit Phase61C held-out line-position eta2 by feature.

Replays the frozen Phase61C selected parameter pair and held-out seeds, then
reports which of the 11 structural features carry the aggregate eta2 match.
No accepted result is modified.
"""
from __future__ import annotations
import importlib.util
import json
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "experiments/phase61/phase61c_joint_model.py"
RESULTS = ROOT / "experiments/phase61/phase61c_results.json"
DATA = ROOT / "eva_zl3b.txt"
URL = "https://raw.githubusercontent.com/Aspect-Research/voynich-autoexploration/master/data/transcriptions/eva_zl3b.txt"
NAMES = [
    "ttr", "mean_len", "sd_len", "unit_inventory", "unit_entropy",
    "first_entropy", "last_entropy", "edit1_fraction", "local_prev10",
    "kt_mass", "k_share",
]
GROUPS = {
    "all11": list(range(11)),
    "near_family_only": [7, 8],
    "without_near_family": [0, 1, 2, 3, 4, 5, 6, 9, 10],
    "entry_shape_related": [1, 5, 6, 9, 10],
    "without_near_family_or_kt": [0, 1, 2, 3, 4, 5, 6],
}

spec = importlib.util.spec_from_file_location("p61c", SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def obtain() -> bytes:
    if DATA.exists():
        data = DATA.read_bytes()
    else:
        with urllib.request.urlopen(URL, timeout=60) as r:
            data = r.read()
        DATA.write_bytes(data)
    got = m.git_blob_sha1(data)
    if got != m.EXPECTED_GIT_BLOB_SHA1:
        raise RuntimeError(f"blob mismatch {got}")
    return data


def mean_group(v, idx):
    return float(np.mean([v[i] for i in idx]))


def main():
    obtain()
    paragraphs, _ = m.parse(str(DATA))
    frozen = json.loads(RESULTS.read_text())
    selected = [f["selected"] for f in frozen["folds"]]
    vocab = sorted(set(m.all_tokens(paragraphs)))
    neighbors = m.build_neighbors(vocab)
    folds = m.physical_leaf_folds(paragraphs)

    fold_rows = []
    real_vecs = []
    gen_vecs = []
    for fi, test_leaves in enumerate(folds):
        train = m.subset(paragraphs, test_leaves, include=False)
        test = m.subset(paragraphs, test_leaves, include=True)
        strength = float(selected[fi]["entry_strength"])
        local_p = float(selected[fi]["local_family_p"])
        scores = m.learn_shape_scores(train, vocab)
        cum = m.entry_cumulative(vocab, scores, strength)

        _, _, real_vec = m.line_eta2(test)
        rep_vecs = []
        for r in range(m.TEST_REPS):
            seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10 + r
            gen = m.generate_layout(test, vocab, neighbors, cum, local_p, seed)
            _, _, gv = m.line_eta2(gen)
            rep_vecs.append(gv)
        gen_vec = np.mean(np.array(rep_vecs, float), axis=0).tolist()
        real_vecs.append(real_vec)
        gen_vecs.append(gen_vec)
        fold_rows.append({
            "fold": fi,
            "selected": selected[fi],
            "real_eta2_by_feature": dict(zip(NAMES, map(float, real_vec))),
            "generated_eta2_by_feature": dict(zip(NAMES, map(float, gen_vec))),
            "group_means": {
                g: {
                    "real": mean_group(real_vec, idx),
                    "generated": mean_group(gen_vec, idx),
                    "ratio": (mean_group(gen_vec, idx) / mean_group(real_vec, idx)) if mean_group(real_vec, idx) else None,
                }
                for g, idx in GROUPS.items()
            },
        })

    real_mean = np.mean(np.array(real_vecs, float), axis=0)
    gen_mean = np.mean(np.array(gen_vecs, float), axis=0)
    feature_summary = {}
    for i, name in enumerate(NAMES):
        feature_summary[name] = {
            "real": float(real_mean[i]),
            "generated": float(gen_mean[i]),
            "ratio": float(gen_mean[i] / real_mean[i]) if real_mean[i] else None,
            "share_of_real_all11": float(real_mean[i] / real_mean.mean()) if real_mean.mean() else None,
            "share_of_generated_all11": float(gen_mean[i] / gen_mean.mean()) if gen_mean.mean() else None,
        }

    groups = {}
    for g, idx in GROUPS.items():
        rr = float(np.mean(real_mean[idx]))
        gg = float(np.mean(gen_mean[idx]))
        groups[g] = {"real": rr, "generated": gg, "ratio": gg / rr if rr else None}

    out = {
        "audit": "Phase61C held-out line-position eta2 feature decomposition",
        "input_git_blob_sha1": m.EXPECTED_GIT_BLOB_SHA1,
        "frozen_selected_parameters": selected,
        "feature_summary": feature_summary,
        "group_summary": groups,
        "folds": fold_rows,
        "interpretation_guardrail": "The all11 line-position eta2 target is not statistically independent of local-prev10 because edit1_fraction and local_prev10 are two of the 11 averaged coordinates. Report without-near-family sensitivity separately.",
    }
    Path("phase61c_eta2_decomposition_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
