#!/usr/bin/env python3
"""Exploratory falsification probes against the OGH synthesis
("small grammar, thin content, local repetition").

Statistics are fixed in this file before any value is inspected. Three corpora:
Voynich ZL3b paragraphs, CREMMA medieval Latin (four Phase62 primary manuscripts),
and the OGH-C memoryless V2 generator placed in the Voynich skeleton.

P1  information density: cross-fitted 2nd-order character-chain cross-entropy,
    bits/token and bits/character; held-out type OOV rate.
P2  long-range exact-repeat excess: P(w_i == w_{i-d}) within document, minus
    within-document shuffle null, for distance bins up to 320 tokens.
P3  adjacent-token mutual information, null-corrected (within-document shuffle).

Exploratory: no gate, no classification, no preregistration. Values may not
be reused as confirmatory targets.
"""
from __future__ import annotations

import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[2]
for rel in ("phase62", "phase64", "issue26-music", "occupancy-generation-hierarchy"):
    sys.path.insert(0, str(EXPERIMENTS / rel))
import phase62b_n0 as b  # noqa: E402
import ogh_a as A  # noqa: E402
import ogh_c as C  # noqa: E402

BINS = ((1, 2), (3, 5), (6, 10), (11, 20), (21, 40), (41, 80), (81, 160), (161, 320))
NULL_REPS = 50
SEED = 8181


def doc_sequences(items):
    """Concatenate items (paragraphs) per document in given order -> list of token-string sequences."""
    docs = defaultdict(list)
    for it in items:
        for line in it.lines:
            docs[it.document].extend("".join(t) for t in line)
    return [seq for seq in docs.values() if len(seq) >= 2]


def five_folds_by_items(items):
    return [items[i::5] for i in range(5)]


# ---------------- P1: character-chain information density ----------------

class CharChain2:
    def __init__(self, tokens, order=2):
        self.order = order
        self.c = defaultdict(Counter)
        self.c1 = defaultdict(Counter)
        self.alpha = set()
        for tok in tokens:
            seq = ["^"] * order + list(tok) + ["$"]
            for i in range(order, len(seq)):
                self.c[tuple(seq[i - order:i])][seq[i]] += 1
                self.c1[seq[i - 1]][seq[i]] += 1
                self.alpha.add(seq[i])
        self.V = len(self.alpha) + 1

    def logp_next(self, ctx, x):
        # back-off: order-2 counts with one pseudo-count of order-1 add-1/2 estimate
        c1 = self.c1[ctx[-1]]
        n1 = sum(c1.values())
        p1 = (c1[x] + 0.5) / (n1 + 0.5 * self.V)
        c2 = self.c[ctx]
        n2 = sum(c2.values())
        return math.log((c2[x] + p1) / (n2 + 1.0))

    def bits(self, tok):
        seq = ["^"] * self.order + list(tok) + ["$"]
        return -sum(self.logp_next(tuple(seq[i - self.order:i]), seq[i]) for i in range(self.order, len(seq))) / math.log(2)


def p1_density(folds_train_test):
    bt, bc, oov, ntok, nch = [], [], [], 0, 0
    for tr, te in folds_train_test:
        m = CharChain2(tr)
        types = set(tr)
        bits = [m.bits(t) for t in te]
        bt.append(float(np.mean(bits)))
        bc.append(float(sum(bits) / sum(len(t) for t in te)))
        oov.append(float(np.mean([t not in types for t in te])))
        ntok += len(te)
        nch += sum(len(t) for t in te)
    return {"bits_per_token": float(np.mean(bt)), "bits_per_char": float(np.mean(bc)), "heldout_oov_type_rate": float(np.mean(oov)), "mean_token_length": nch / ntok, "n_heldout_tokens": ntok, "by_fold_bits_per_token": bt}


# ---------------- P2: long-range exact-repeat excess ----------------

def repeat_rates(seqs):
    hits = np.zeros(len(BINS))
    avail = np.zeros(len(BINS))
    for seq in seqs:
        n = len(seq)
        for bi, (lo, hi) in enumerate(BINS):
            for i in range(lo, n):
                avail[bi] += 1
                if any(seq[i - d] == seq[i] for d in range(lo, min(hi, i) + 1)):
                    hits[bi] += 1
    return hits / np.maximum(avail, 1), avail


def p2_longrange(seqs, label):
    obs, avail = repeat_rates(seqs)
    rng = random.Random(SEED)
    nulls = []
    for _ in range(NULL_REPS):
        sh = []
        for seq in seqs:
            s = list(seq)
            rng.shuffle(s)
            sh.append(s)
        nulls.append(repeat_rates(sh)[0])
    nulls = np.array(nulls)
    med = np.median(nulls, axis=0)
    sd = nulls.std(axis=0) + 1e-12
    return {"label": label, "bins": [list(x) for x in BINS], "observed": obs.tolist(), "null_median": med.tolist(), "excess": (obs - med).tolist(), "excess_over_null_sd": ((obs - med) / sd).tolist(), "relative_excess": ((obs - med) / np.maximum(med, 1e-12)).tolist(), "available": avail.tolist(), "n_docs": len(seqs), "n_tokens": int(sum(len(s) for s in seqs))}


# ---------------- P3: adjacent mutual information (null-corrected) ----------------

def mi_at_distance(seqs, d):
    joint = Counter()
    for seq in seqs:
        for i in range(d, len(seq)):
            joint[(seq[i - d], seq[i])] += 1
    n = sum(joint.values())
    a = Counter(); c = Counter()
    for (x, y), k in joint.items():
        a[x] += k; c[y] += k
    mi = 0.0
    for (x, y), k in joint.items():
        mi += k / n * math.log2(k * n / (a[x] * c[y]))
    return mi


def p3_mi(seqs, label):
    out = {"label": label}
    rng = random.Random(SEED + 1)
    for d in (1, 2, 5, 20):
        obs = mi_at_distance(seqs, d)
        nulls = []
        for _ in range(20):
            sh = []
            for seq in seqs:
                s = list(seq); rng.shuffle(s); sh.append(s)
            nulls.append(mi_at_distance(sh, d))
        out[f"d{d}"] = {"observed_bits": obs, "null_mean_bits": float(np.mean(nulls)), "corrected_bits": obs - float(np.mean(nulls))}
    return out


def main(zl_path: Path, cremma_root: Path, out_path: Path):
    corpora = {}
    # Voynich
    vitems = b.parse_voynich(zl_path)
    folds = b.physical_leaf_folds(vitems)
    vtok_folds = []
    for f in range(5):
        tr = [w for it in b.by_leaves(vitems, folds[f], False) for line in it.lines for w in ("".join(t) for t in line)]
        te = [w for it in b.by_leaves(vitems, folds[f], True) for line in it.lines for w in ("".join(t) for t in line)]
        vtok_folds.append((tr, te))
    corpora["Voynich_ZL3b"] = {"items": vitems, "folds": vtok_folds}
    # Latin, four primary manuscripts pooled, five folds by item interleave within manuscript
    litems = []
    lfolds = [([], []) for _ in range(5)]
    for name, rel in b.PRIMARY_MANUSCRIPTS.items():
        ms = b.parse_latin_manuscript(cremma_root, name, rel)
        litems.extend(ms)
        parts = five_folds_by_items(ms)
        for f in range(5):
            te = [w for it in parts[f] for line in it.lines for w in ("".join(t) for t in line)]
            tr = [w for g in range(5) if g != f for it in parts[g] for line in it.lines for w in ("".join(t) for t in line)]
            lfolds[f][0].extend(tr); lfolds[f][1].extend(te)
    corpora["Latin_CREMMA4"] = {"items": litems, "folds": lfolds}
    # memoryless V2 generator in the Voynich skeleton (rep 0)
    in_a, _ = A.load_admissible()
    vi, vf, parsed = C.load_corpus(zl_path)
    gitems, _ = C.generate_manuscript("V2", 0, vi, vf, parsed, in_a)
    corpora["V2_memoryless_generator"] = {"items": gitems, "folds": None}

    result = {"schema": "ogh-falsification-probes-v1", "exploratory": True, "null_reps": NULL_REPS, "environment": A.environment(), "P1": {}, "P2": {}, "P3": {}}
    for name, c in corpora.items():
        if c["folds"] is not None:
            result["P1"][name] = p1_density(c["folds"])
            print(name, "P1", json.dumps({k: round(v, 3) if isinstance(v, float) else v for k, v in result["P1"][name].items() if k != "by_fold_bits_per_token"}), file=sys.stderr, flush=True)
        seqs = doc_sequences(c["items"])
        result["P2"][name] = p2_longrange(seqs, name)
        print(name, "P2 excess", [round(x, 4) for x in result["P2"][name]["excess"]], "z", [round(x, 1) for x in result["P2"][name]["excess_over_null_sd"]], file=sys.stderr, flush=True)
        result["P3"][name] = p3_mi(seqs, name)
        print(name, "P3", {k: round(v["corrected_bits"], 3) for k, v in result["P3"][name].items() if k != "label"}, file=sys.stderr, flush=True)
    out_path.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
