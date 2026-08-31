#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
import sys
import tempfile
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

SOURCE_COMMIT = "31819c914061cc6b63bbf4983e33d643ede52e46"
SOURCE_URL = (
    "https://raw.githubusercontent.com/Aspect-Research/voynich-autoexploration/"
    + SOURCE_COMMIT
    + "/data/transcriptions/eva_zl3b.txt"
)
EXPECTED_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
BINS: Tuple[Tuple[str, int, int], ...] = (
    ("L1", 41, 80),
    ("L2", 81, 160),
    ("L3", 161, 320),
)
MIN_LEAF_TOKENS = 321
NULL_REPS = 40
A1_REPS = 50
EPS = 1e-15

HERE = Path(__file__).resolve().parent
PHASE62 = HERE.parent / "phase62"
sys.path.insert(0, str(PHASE62))
import phase62c_c0_a1 as c  # noqa: E402


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def stable_seed(label: str) -> int:
    h = hashlib.sha256(label.encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") % (2**31 - 1)


def fetch_zl3b() -> Tuple[bytes, dict]:
    with urllib.request.urlopen(SOURCE_URL, timeout=60) as r:
        data = r.read()
    blob = git_blob_sha1(data)
    if blob != EXPECTED_BLOB:
        raise RuntimeError(f"ZL3b blob mismatch: {blob} != {EXPECTED_BLOB}")
    return data, {
        "source_commit": SOURCE_COMMIT,
        "source_url": SOURCE_URL,
        "git_blob_sha1": blob,
        "bytes": len(data),
    }


def load_phase61():
    path = HERE.parent / "phase61" / "phase61c_joint_model.py"
    spec = importlib.util.spec_from_file_location("phase61c_joint_model_p69", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Phase61 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def leaf_sequences(paragraphs) -> Dict[int, List[str]]:
    out: Dict[int, List[str]] = defaultdict(list)
    for p in paragraphs:
        for line in p.lines:
            out[p.leaf].extend(line)
    return dict(out)


def eligible_leaf_sequences(paragraphs) -> Dict[int, List[str]]:
    return {
        leaf: seq
        for leaf, seq in leaf_sequences(paragraphs).items()
        if len(seq) >= MIN_LEAF_TOKENS
    }


def rolling_bin_rates_both(
    sequences: Dict[int, Sequence[str]],
    neighbors: Dict[str, set[str]],
) -> Tuple[List[float], List[int], List[float], List[int], List[int]]:
    """Return edit1 and exact recurrence rates in one identical rolling pass."""
    edit_hits = [0] * len(BINS)
    exact_hits = [0] * len(BINS)
    available = [0] * len(BINS)
    empty_neighbors: set[str] = set()

    for _leaf, seq in sequences.items():
        windows = [Counter() for _ in BINS]
        for i, tok in enumerate(seq):
            tok_neighbors = neighbors.get(tok, empty_neighbors)
            for bi, (_name, lo, hi) in enumerate(BINS):
                add_j = i - lo
                rem_j = i - hi - 1
                if add_j >= 0:
                    windows[bi][seq[add_j]] += 1
                if rem_j >= 0:
                    old = seq[rem_j]
                    windows[bi][old] -= 1
                    if windows[bi][old] <= 0:
                        del windows[bi][old]
                if i < hi:
                    continue

                available[bi] += 1
                exact_hits[bi] += int(windows[bi].get(tok, 0) > 0)
                # Counter.keys() is a set-like view; isdisjoint avoids a Python
                # loop over every neighbor while preserving the exact relation.
                edit_hits[bi] += int(
                    bool(tok_neighbors)
                    and not windows[bi].keys().isdisjoint(tok_neighbors)
                )

    if any(n == 0 for n in available):
        raise RuntimeError(f"zero long-range availability: {available}")

    edit_rates = [edit_hits[i] / available[i] for i in range(len(BINS))]
    exact_rates = [exact_hits[i] / available[i] for i in range(len(BINS))]
    return edit_rates, edit_hits, exact_rates, exact_hits, available


def build_edit1_neighbors(p61, sequences: Dict[int, Sequence[str]]) -> Dict[str, set[str]]:
    vocab = sorted({t for seq in sequences.values() for t in seq})
    raw = p61.build_neighbors(vocab)
    return {k: set(v) for k, v in raw.items()}


def restrict_prebuilt_neighbors(
    sequences: Dict[int, Sequence[str]],
    prebuilt_neighbors: Dict[str, Sequence[str]],
) -> Dict[str, set[str]]:
    """Restrict a superset-vocabulary lev1 graph to the observed dataset types.

    A1-R1 generated tokens are asserted to lie inside the training vocabulary.
    The edit1 relation itself is vocabulary-independent, so restricting the
    already-built training graph is exactly equivalent to rebuilding the graph
    from the generated type subset and is substantially faster.
    """
    types = {t for seq in sequences.values() for t in seq}
    return {
        t: set(prebuilt_neighbors.get(t, ())).intersection(types)
        for t in types
    }


def normalize_excess(excess: Sequence[float]) -> dict:
    denom = float(sum(abs(x) for x in excess))
    return {
        "abs_excess_sum": denom,
        "profile": [float(x / denom) for x in excess] if denom > 0 else None,
    }


def profile_dataset(
    p61,
    paragraphs,
    label: str,
    prebuilt_neighbors: Dict[str, Sequence[str]] | None = None,
) -> dict:
    seqs = eligible_leaf_sequences(paragraphs)
    if not seqs:
        raise RuntimeError(f"{label}: no physical leaf has >= {MIN_LEAF_TOKENS} tokens")

    if prebuilt_neighbors is None:
        neighbors = build_edit1_neighbors(p61, seqs)
    else:
        neighbors = restrict_prebuilt_neighbors(seqs, prebuilt_neighbors)

    obs_edit, obs_edit_hits, obs_exact, obs_exact_hits, avail = rolling_bin_rates_both(
        seqs, neighbors
    )

    null_edit = []
    null_exact = []
    seed = stable_seed(f"phase69A:null:{label}")
    for r in range(NULL_REPS):
        rng = random.Random(seed + r)
        shuffled = {}
        for leaf, seq in seqs.items():
            row = list(seq)
            rng.shuffle(row)
            shuffled[leaf] = row
        e, _, x, _, a = rolling_bin_rates_both(shuffled, neighbors)
        if a != avail:
            raise AssertionError("null availability changed")
        null_edit.append(e)
        null_exact.append(x)

    def summarize(observed, observed_hits, null_rows):
        arr = np.asarray(null_rows, dtype=float)
        med = np.median(arr, axis=0)
        excess = [float(observed[i] - med[i]) for i in range(len(BINS))]
        norm = normalize_excess(excess)
        return {
            "observed": [float(x) for x in observed],
            "observed_hits": observed_hits,
            "null_median": [float(x) for x in med],
            "null_q025": [float(x) for x in np.quantile(arr, 0.025, axis=0)],
            "null_q975": [float(x) for x in np.quantile(arr, 0.975, axis=0)],
            "excess": excess,
            "E_long": float(sum(excess)),
            **norm,
        }

    return {
        "label": label,
        "eligible_leaves": sorted(seqs),
        "leaf_token_counts": {str(k): len(v) for k, v in sorted(seqs.items())},
        "n_tokens": int(sum(len(v) for v in seqs.values())),
        "n_types": len({t for seq in seqs.values() for t in seq}),
        "bins": [b[0] for b in BINS],
        "available_occurrences": avail,
        "null_reps": NULL_REPS,
        "edit1": summarize(obs_edit, obs_edit_hits, null_edit),
        "exact": summarize(obs_exact, obs_exact_hits, null_exact),
    }


def mean_profile(profiles: Sequence[dict], mode: str) -> dict:
    rows = [p[mode] for p in profiles]
    excess = [float(np.mean([r["excess"][i] for r in rows])) for i in range(len(BINS))]
    norm = normalize_excess(excess)
    return {
        "mean_E_long": float(np.mean([r["E_long"] for r in rows])),
        "mean_excess": excess,
        **norm,
    }


def profile_l1(a, b) -> float | None:
    if a is None or b is None:
        return None
    return float(sum(abs(x - y) for x, y in zip(a, b)))


def main() -> int:
    data, source_meta = fetch_zl3b()
    p61 = load_phase61()

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "eva_zl3b.txt"
        path.write_bytes(data)
        paragraphs, _headers = p61.parse(str(path))

    folds = p61.physical_leaf_folds(paragraphs)
    if len(folds) != 5:
        raise RuntimeError(f"expected five folds, got {len(folds)}")

    target_profiles = []
    fold_a1_profiles: Dict[int, List[dict]] = {}
    fold_meta = []

    for fi, test_leaves in enumerate(folds):
        p_train = p61.subset(paragraphs, test_leaves, include=False)
        p_test = p61.subset(paragraphs, test_leaves, include=True)
        target = profile_dataset(p61, p_test, f"Voynich:fold{fi}")
        target_profiles.append(target)

        train_vocab = sorted(set(p61.all_tokens(p_train)))
        if not train_vocab:
            raise RuntimeError(f"fold {fi}: empty training vocabulary")
        neighbors = p61.build_neighbors(train_vocab)
        shape_scores = p61.learn_shape_scores(p_train, train_vocab)
        strength, local_p = c.A1_PARAMS[fi]
        entry_cum = p61.entry_cumulative(train_vocab, shape_scores, strength)

        reps = []
        for r in range(A1_REPS):
            seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10 + r
            generated = p61.generate_layout(
                p_test,
                train_vocab,
                neighbors,
                entry_cum,
                local_p,
                seed,
            )
            outside = set(p61.all_tokens(generated)) - set(train_vocab)
            if outside:
                raise RuntimeError(f"fold {fi} rep {r}: generated token outside training vocabulary")
            reps.append(
                profile_dataset(
                    p61,
                    generated,
                    f"A1R1:fold{fi}:rep{r}",
                    prebuilt_neighbors=neighbors,
                )
            )
        fold_a1_profiles[fi] = reps
        fold_meta.append({
            "fold": fi,
            "test_leaves": sorted(test_leaves),
            "target_eligible_leaves": target["eligible_leaves"],
            "training_vocab_types": len(train_vocab),
            "entry_strength": strength,
            "local_family_p": local_p,
        })

    target_edit = mean_profile(target_profiles, "edit1")
    target_exact = mean_profile(target_profiles, "exact")

    a1_rep_edit = []
    a1_rep_exact = []
    for r in range(A1_REPS):
        rows = [fold_a1_profiles[fi][r] for fi in range(5)]
        a1_rep_edit.append(mean_profile(rows, "edit1"))
        a1_rep_exact.append(mean_profile(rows, "exact"))

    def model_check(target, a1_rows):
        sims = [x["mean_E_long"] for x in a1_rows]
        v = target["mean_E_long"]
        mean_a = float(np.mean(sims))
        p_upper = (1 + sum(x >= v - EPS for x in sims)) / (len(sims) + 1)
        return {
            "V_mean_E_long": v,
            "A1_mean_E_long": mean_a,
            "delta_V_minus_A1": float(v - mean_a),
            "p_upper_plus_one": float(p_upper),
            "A1_predictive_E_long": [float(x) for x in sims],
            "A1_q025": float(np.quantile(sims, 0.025)),
            "A1_q975": float(np.quantile(sims, 0.975)),
        }

    primary = model_check(target_edit, a1_rep_edit)
    secondary = model_check(target_exact, a1_rep_exact)

    if primary["p_upper_plus_one"] <= 0.05 and primary["delta_V_minus_A1"] > 0:
        classification = "A1 LONG-RANGE UNDERPREDICTION — PERSISTENT STATE REQUIRED"
    else:
        classification = "NO DETECTED LONG-RANGE EXCESS BEYOND FROZEN A1"

    a1_edit_mean_excess = [float(np.mean([x["mean_excess"][i] for x in a1_rep_edit])) for i in range(len(BINS))]
    a1_edit_norm = normalize_excess(a1_edit_mean_excess)
    a1_exact_mean_excess = [float(np.mean([x["mean_excess"][i] for x in a1_rep_exact])) for i in range(len(BINS))]
    a1_exact_norm = normalize_excess(a1_exact_mean_excess)

    result = {
        "schema": "phase69a-result-v1",
        "status": "SEALED_RESULT",
        "source": source_meta,
        "bins": [{"name": n, "lo": lo, "hi": hi} for n, lo, hi in BINS],
        "min_leaf_tokens": MIN_LEAF_TOKENS,
        "null_reps_per_dataset": NULL_REPS,
        "a1_predictive_reps": A1_REPS,
        "fold_meta": fold_meta,
        "target_fold_profiles": target_profiles,
        "primary_edit1": primary,
        "primary_target_mean_profile": target_edit,
        "primary_A1_mean_excess": a1_edit_mean_excess,
        "primary_A1_mean_profile": a1_edit_norm["profile"],
        "primary_profile_L1_distance": profile_l1(target_edit["profile"], a1_edit_norm["profile"]),
        "secondary_exact": secondary,
        "secondary_target_mean_profile": target_exact,
        "secondary_A1_mean_excess": a1_exact_mean_excess,
        "secondary_A1_mean_profile": a1_exact_norm["profile"],
        "secondary_profile_L1_distance": profile_l1(target_exact["profile"], a1_exact_norm["profile"]),
        "classification": classification,
    }

    out = HERE / "RESULT_A.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": classification,
        "eligible_target_leaves_by_fold": [x["target_eligible_leaves"] for x in fold_meta],
        "primary": {k: primary[k] for k in ["V_mean_E_long", "A1_mean_E_long", "delta_V_minus_A1", "p_upper_plus_one", "A1_q025", "A1_q975"]},
        "primary_target_profile": target_edit["profile"],
        "primary_A1_profile": a1_edit_norm["profile"],
        "primary_profile_L1_distance": result["primary_profile_L1_distance"],
        "secondary_exact": {k: secondary[k] for k in ["V_mean_E_long", "A1_mean_E_long", "delta_V_minus_A1", "p_upper_plus_one"]},
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
