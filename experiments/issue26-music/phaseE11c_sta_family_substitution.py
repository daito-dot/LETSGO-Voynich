#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np

import phaseE11_leon_substitution as base

STA_SHA256 = "8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a"
FAMILIES = tuple("ABCDEFGHJKLMNPQRSTUVWXZ")
ALT_RE = re.compile(r"\[([^\]:]+):[^\]]+\]")
LOCUS_RE = re.compile(r"^<(?P<folio>f[^.>,]+)\.(?P<locus>[^,>]+),(?P<kind>[^>]+)>\s+(?P<body>.*)$")
CODE_RE = re.compile(r"[A-Z][0-9a-z*]")
ANGLE_RE = re.compile(r"<[^>]*>")
LEAF_RE = re.compile(r"f(\d+)")


def sha256_bytes(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def clean_segment(seg: str):
    seg = ALT_RE.sub(lambda m: m.group(1), seg)
    seg = seg.replace("{", "").replace("}", "")
    seg = ANGLE_RE.sub(" ", seg)
    return seg


def parse_sta(path: Path):
    data = path.read_bytes()
    if sha256_bytes(data) != STA_SHA256:
        raise RuntimeError("official STA source SHA-256 mismatch")
    lines = data.decode("utf-8").splitlines()
    if not lines or lines[0].strip() != "#=IVTFF STA1 2.0 M 5":
        raise RuntimeError("unexpected STA header")

    labels = list(FAMILIES)
    fi = {f:i for i,f in enumerate(labels)}
    counts = Counter()
    records = []
    source_lines = 0
    unknown_breaks = 0
    interruption_breaks = 0

    for no, raw in enumerate(lines, 1):
        m = LOCUS_RE.match(raw)
        if not m or "P" not in m.group("kind"):
            continue
        lm = LEAF_RE.match(m.group("folio"))
        if not lm:
            continue
        leaf = int(lm.group(1))
        source_lines += 1
        body = ALT_RE.sub(lambda x:x.group(1), m.group("body"))
        # Explicit drawing/text interruption first, then unreadable markers.
        parts = body.split("<->")
        interruption_breaks += max(0, len(parts)-1)
        seg_index = 0
        for part in parts:
            qparts = part.split("?")
            unknown_breaks += max(0, len(qparts)-1)
            for qpart in qparts:
                seg = clean_segment(qpart)
                words = []
                seq = []
                for word in re.split(r"[.,\s]+", seg):
                    if not word:
                        continue
                    codes = CODE_RE.findall(word)
                    residue = CODE_RE.sub("", word)
                    residue = re.sub(r"[-=$%:]", "", residue)
                    if residue:
                        raise RuntimeError(f"unparsed STA residue line {no}: {word!r} -> {residue!r}")
                    if not codes:
                        continue
                    fams = []
                    for code in codes:
                        fam = code[0]
                        if fam not in fi:
                            raise RuntimeError(f"unexpected family {fam} in code {code}")
                        idx = fi[fam]
                        fams.append(idx)
                        seq.append(idx)
                        counts[fam] += 1
                    words.append(np.asarray(fams, dtype=np.int16))
                if seq:
                    records.append({
                        "leaf": leaf,
                        "page": m.group("folio"),
                        "paragraph": m.group("loc"),
                        "line_index": no,
                        "segment_index": seg_index,
                        "tokens": words,
                        "seq": np.asarray(seq, dtype=np.int16),
                    })
                seg_index += 1

    observed = tuple(sorted(counts))
    if observed != tuple(sorted(FAMILIES)):
        raise RuntimeError(f"family set mismatch: {observed} != {tuple(sorted(FAMILIES))}")
    leaves = sorted({r["leaf"] for r in records})
    folds = [set(leaves[i::5]) for i in range(5)]
    return records, folds, labels, counts, {
        "sha256": STA_SHA256,
        "source_running_text_lines": source_lines,
        "scoring_segments": len(records),
        "events": sum(counts.values()),
        "interruption_breaks": interruption_breaks,
        "unreadable_breaks": unknown_breaks,
        "leaves": len(leaves),
        "families": dict(sorted(counts.items())),
    }


def optimize_key_c(seqs, M, lm_cost, fold):
    pats, counts, offsets, incident = base.pattern_arrays_from_sequences(seqs, M)
    best_key = None
    best_ce = float("inf")
    restart_rows = []
    for r in range(base.RESTARTS):
        seed = base.seed32(f"Issue26E11C:STAFamilyMonoSub:v1:{fold}:{r}")
        rng = np.random.default_rng(seed)
        initial = rng.permutation(base.A).astype(np.int16)
        key, ce = base.anneal_one(initial, seed, M, pats, counts, offsets, incident, lm_cost)
        t = tuple(int(x) for x in key)
        restart_rows.append({"restart": r, "seed": seed, "cross_entropy": float(ce)})
        if ce < best_ce - base.EPS or (abs(ce-best_ce) <= base.EPS and (best_key is None or t < tuple(int(x) for x in best_key))):
            best_ce = float(ce)
            best_key = key.copy()
    return best_key, best_ce, restart_rows


def positive_control_c(latin_runs, labels, glyph_counts, lm, target_events):
    M = len(labels)
    freq = Counter("".join(latin_runs))
    top_plain = [c for c, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:M]]
    runs, events = base.split_topm_runs(latin_runs, set(top_plain), target_events)
    rng = np.random.default_rng(base.seed32("Issue26E11C:PositiveKey:v1"))
    cipher_order = rng.permutation(M).tolist()
    plain_to_cipher = {top_plain[i]: int(cipher_order[i]) for i in range(M)}
    true_decode = np.full(M, -1, dtype=np.int16)
    for p, cidx in plain_to_cipher.items():
        true_decode[cidx] = base.AI[p]
    encoded = [np.asarray([plain_to_cipher[ch] for ch in s], dtype=np.int16) for s in runs]
    fold_ids = [i % 5 for i in range(len(encoded))]
    symbol_counts = np.zeros(M, dtype=np.int64)
    for s in encoded:
        for x in s:
            symbol_counts[int(x)] += 1
    rows = []
    recovered_keys = []
    for f in range(5):
        train = [s for i,s in enumerate(encoded) if fold_ids[i] != f]
        held = [s for i,s in enumerate(encoded) if fold_ids[i] == f]
        key, tr_ce, restarts = optimize_key_c(train, M, lm.cost, f)
        rec_ce, rec_n = base.score_key_on_seqs(key, held, M, lm.cost)
        used = set(int(x) for x in true_decode)
        unused = [i for i in range(base.A) if i not in used]
        true_full = np.asarray(list(true_decode) + unused, dtype=np.int16)
        true_ce, _ = base.score_key_on_seqs(true_full, held, M, lm.cost)
        exact = sum(int(key[i]) == int(true_decode[i]) for i in range(M)) / M
        weighted = sum(symbol_counts[i] for i in range(M) if int(key[i]) == int(true_decode[i])) / symbol_counts.sum()
        recovered_keys.append(tuple(int(x) for x in key[:M]))
        rows.append({"fold":f,"training_cross_entropy":tr_ce,"recovered_held_cross_entropy":rec_ce,
                     "true_held_cross_entropy":true_ce,"held_scored_chars":rec_n,
                     "exact_key_accuracy":exact,"occurrence_weighted_key_accuracy":weighted,
                     "recovered_mapping":base.key_mapping(key, labels),"restart_scores":restarts})
    mean_rec = statistics.fmean(r["recovered_held_cross_entropy"] for r in rows)
    mean_true = statistics.fmean(r["true_held_cross_entropy"] for r in rows)
    mean_weighted = statistics.fmean(r["occurrence_weighted_key_accuracy"] for r in rows)
    rec = Counter(recovered_keys)
    _, exact_rec = min(rec.items(), key=lambda kv:(-kv[1],kv[0]))
    return {
        "passed": abs(mean_rec-mean_true) <= .05 and mean_weighted >= .95,
        "events": events,
        "runs": len(runs),
        "top_plaintext_letters": top_plain,
        "true_cipher_to_plaintext": {labels[i]:base.ALPHABET[int(true_decode[i])] for i in range(M)},
        "mean_recovered_held_cross_entropy":mean_rec,
        "mean_true_held_cross_entropy":mean_true,
        "mean_occurrence_weighted_key_accuracy":mean_weighted,
        "exact_recovered_key_recurrence":int(exact_rec),
        "folds":rows,
    }


def add_unused(voy):
    used_all = set(base.ALPHABET)
    for row in voy["folds"]:
        mapped = set(row["mapping"].values())
        row["unused_plaintext_letter"] = sorted(used_all - mapped)
    return voy


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-STA1.txt CREMMA_ROOT", file=sys.stderr)
        return 2
    sta = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    records, folds, labels, fam_counts, sta_meta = parse_sta(sta)
    if len(labels) != 23:
        raise RuntimeError("frozen family count mismatch")

    latin_runs, lexicon, latin_meta = base.load_latin(root)
    baseline = base.latin_self_baseline(latin_runs)
    lm = base.LM4(latin_runs)

    # Redirect the already-audited E11 run_voynich machinery to E11C's frozen seed namespace.
    old_opt = base.optimize_key
    base.optimize_key = optimize_key_c
    try:
        pos = positive_control_c(latin_runs, labels, fam_counts, lm, sta_meta["events"])
        voy = base.run_voynich(records, folds, labels, fam_counts, lm, lexicon)
    finally:
        base.optimize_key = old_opt
    voy = add_unused(voy)
    classification, gates = base.classify(pos, voy, baseline)
    if classification == "LEON-LIKE MONOALPHABETIC PLAINTEXT LEAD":
        classification = "STA-FAMILY LEON-LIKE PLAINTEXT LEAD"
    elif classification == "NO READABLE LEON-LIKE MONOALPHABETIC PLAINTEXT":
        classification = "NO READABLE STA-FAMILY LEON-LIKE PLAINTEXT"

    out = {
        "experiment":"Issue26E11C STA-family Leon-style monoalphabetic substitution test",
        "classification":classification,
        "classification_gates":gates,
        "sta_population":sta_meta,
        "family_labels":labels,
        "latin_population":latin_meta,
        "latin_self_baseline":baseline,
        "optimizer":{"restarts":base.RESTARTS,"steps_per_restart":base.STEPS,"T0":base.T0,"T1":base.T1,
                     "seed_namespace":"Issue26E11C:STAFamilyMonoSub:v1"},
        "positive_control":pos,
        "voynich_primary":voy,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
