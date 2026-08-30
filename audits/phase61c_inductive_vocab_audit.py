#!/usr/bin/env python3
"""Phase61C sensitivity audit with vocabulary learned from training leaves only.

The frozen Phase61C implementation shares the empirical full-manuscript token-type
inventory across outer folds and marks edit1 density non-independent. This audit
asks whether the three primary gate metrics still survive when each fold may use
only token types observed on its training physical leaves.

No accepted experiment file is modified.
"""
from __future__ import annotations
import importlib.util
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "experiments/phase61/phase61c_joint_model.py"
spec = importlib.util.spec_from_file_location("p61c", SRC)
m = importlib.util.module_from_spec(spec)
sys.modules["p61c"] = m
spec.loader.exec_module(m)

TRANSCRIPTION_URL = "https://raw.githubusercontent.com/Aspect-Research/voynich-autoexploration/master/data/transcriptions/eva_zl3b.txt"


def obtain(path: Path) -> None:
    if not path.exists():
        with urllib.request.urlopen(TRANSCRIPTION_URL, timeout=60) as r:
            path.write_bytes(r.read())
    data = path.read_bytes()
    got = m.git_blob_sha1(data)
    if got != m.EXPECTED_GIT_BLOB_SHA1:
        raise RuntimeError(f"blob mismatch: {got}")


def primary_bundle(paragraphs, sd, direction, neighbors):
    b = m.metric_bundle(paragraphs, sd, direction, neighbors)
    return {k: b[k] for k in ("entry_projection", "local_prev10_fraction", "line_position_eta2_mean")}


def avg(bb):
    keys = ("entry_projection", "local_prev10_fraction", "line_position_eta2_mean")
    return {k: float(np.mean([x[k] for x in bb])) for k in keys}


def rel_mse(gen, real):
    return float(np.mean([((gen[k]-real[k]) / max(abs(real[k]), 1e-12))**2 for k in real]))


def run(paragraphs):
    folds = m.physical_leaf_folds(paragraphs)
    fold_results = []
    for fi, test_leaves in enumerate(folds):
        train = m.subset(paragraphs, test_leaves, include=False)
        test = m.subset(paragraphs, test_leaves, include=True)

        vocab = sorted(set(m.all_tokens(train)))
        vocab_set = set(vocab)
        neighbors = m.build_neighbors(vocab)
        test_tokens = m.all_tokens(test)
        test_types = set(test_tokens)
        unseen_types = test_types - vocab_set
        unseen_token_count = sum(t not in vocab_set for t in test_tokens)

        sd = m.feature_sd(train)
        Dtr = m.eligible_deltas(train, sd)
        direction = np.mean(Dtr, axis=0)
        n = float(np.linalg.norm(direction))
        if not n:
            raise RuntimeError(f"zero direction fold {fi}")
        direction /= n

        real_train = primary_bundle(train, sd, direction, neighbors)
        real_test = primary_bundle(test, sd, direction, neighbors)
        scores = m.learn_shape_scores(train, vocab)
        cums = {s: m.entry_cumulative(vocab, scores, s) for s in m.ENTRY_STRENGTH_GRID}

        candidates = []
        for si, strength in enumerate(m.ENTRY_STRENGTH_GRID):
            for pi, local_p in enumerate(m.LOCAL_P_GRID):
                reps = []
                for r in range(m.TRAIN_REPS):
                    seed = 6100000 + fi*100000 + si*10000 + pi*1000 + r
                    gen = m.generate_layout(train, vocab, neighbors, cums[strength], local_p, seed)
                    reps.append(primary_bundle(gen, sd, direction, neighbors))
                g = avg(reps)
                candidates.append((rel_mse(g, real_train), strength, local_p, g))
        candidates.sort(key=lambda x:(x[0],x[1],x[2]))
        score, strength, local_p, _train_gen = candidates[0]

        reps=[]
        for r in range(m.TEST_REPS):
            seed = 6190000 + fi*100000 + int(strength*10)*1000 + int(local_p*100)*10 + r
            gen = m.generate_layout(test, vocab, neighbors, cums[strength], local_p, seed)
            reps.append(primary_bundle(gen, sd, direction, neighbors))
        gen_test=avg(reps)
        ratios={k:(gen_test[k]/real_test[k] if abs(real_test[k])>1e-12 else None) for k in real_test}
        fold_results.append({
            "fold":fi,
            "selected":{"entry_strength":strength,"local_family_p":local_p},
            "train_relative_mse":score,
            "training_vocab_types":len(vocab),
            "heldout_types":len(test_types),
            "heldout_unseen_types":len(unseen_types),
            "heldout_unseen_type_fraction":len(unseen_types)/len(test_types) if test_types else 0.0,
            "heldout_unseen_token_fraction":unseen_token_count/len(test_tokens) if test_tokens else 0.0,
            "heldout_real":real_test,
            "heldout_generated":gen_test,
            "heldout_ratio":ratios,
        })

    keys=("entry_projection","local_prev10_fraction","line_position_eta2_mean")
    real_mean={k:float(np.mean([f["heldout_real"][k] for f in fold_results])) for k in keys}
    gen_mean={k:float(np.mean([f["heldout_generated"][k] for f in fold_results])) for k in keys}
    ratios={k:gen_mean[k]/real_mean[k] for k in keys}
    gate={k:0.5<=ratios[k]<=2.0 for k in keys}
    return {
        "audit":"Phase61C strict inductive-vocabulary sensitivity",
        "change":"each outer fold uses only token types observed in training physical leaves; no held-out token types are available to the generator",
        "folds":fold_results,
        "heldout_real_mean":real_mean,
        "heldout_generated_mean":gen_mean,
        "heldout_ratio_of_means":ratios,
        "broad_regime_gate_0.5_to_2.0":gate,
        "status":"A1 SURVIVES inductive-vocabulary sensitivity" if all(gate.values()) else "A1 FAILS inductive-vocabulary sensitivity",
    }


def main():
    source=ROOT/"eva_zl3b.txt"
    obtain(source)
    paragraphs,_=m.parse(str(source))
    out=run(paragraphs)
    out["input_git_blob_sha1"]=m.EXPECTED_GIT_BLOB_SHA1
    ref=json.loads((ROOT/"experiments/phase61/phase61c_results.json").read_text())
    out["frozen_reference_summary"]={
        "status":ref["status"],
        "heldout_ratio_of_means":ref["heldout_ratio_of_means"],
        "selected":[f["selected"] for f in ref["folds"]],
    }
    p=ROOT/"phase61c_inductive_vocab_audit_results.json"
    p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(out,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
