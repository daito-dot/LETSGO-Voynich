#!/usr/bin/env python3
"""Read-only audit reimplementation for Phase 60B.

This script does not modify accepted experiment files. It compares:
1) the current public implementation's final pooled-direction calculation;
2) a corrected cross-fit using the original global feature scaling;
3) a stricter corrected cross-fit where feature scaling is fit on training leaves only.

The parser, feature set, paragraph eligibility rule, pseudo-boundary construction,
and 5-fold physical-leaf split intentionally mirror the public Phase 60B script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import urllib.request
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np

TRANSCRIPTION_URL = "https://raw.githubusercontent.com/Aspect-Research/voynich-autoexploration/master/data/transcriptions/eva_zl3b.txt"
EXPECTED_GIT_BLOB_SHA1 = "2a4533ab9bdfa85db9bad602d590978953055df1"

HP = re.compile(r'^<(?P<p>f\d+[rv]\d*)>\s+<!\s*(?P<m>.*?)>')
LP = re.compile(r'^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<c>[^>]*)>\s+(?P<b>.*)$')

NAMES = [
    'ttr', 'mean_len', 'sd_len', 'unit_inventory', 'unit_entropy',
    'first_entropy', 'last_entropy', 'edit1_fraction', 'local_prev10',
    'kt_mass', 'k_share'
]
GROUPS = {
    'lexical_diversity': [0],
    'length': [1, 2],
    'edge_entropy': [5, 6],
    'near_family': [7, 8],
    'kt': [9, 10],
}
MODES = ['raw', 'conservative', 'phase56']


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def get_source(path: Path) -> bytes:
    if path.exists():
        data = path.read_bytes()
    else:
        with urllib.request.urlopen(TRANSCRIPTION_URL, timeout=60) as response:
            data = response.read()
        path.write_bytes(data)
    got = git_blob_sha1(data)
    if got != EXPECTED_GIT_BLOB_SHA1:
        raise RuntimeError(f"transcription blob mismatch: got {got}, expected {EXPECTED_GIT_BLOB_SHA1}")
    return data


def tokens(body: str):
    start = '<%>' in body
    body = body.replace('<%>', ' ')
    body = re.sub(r'<[^>]*>', ' ', body)
    z = [re.sub(r'[^A-Za-z]', '', x).lower() for x in re.split(r'[.\s]+', body)]
    return start, [x for x in z if x]


def lev1(a, b):
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


def entropy(v):
    c = Counter(v)
    if not c:
        return 0.0
    q = np.array(list(c.values()), float)
    q /= q.sum()
    return float(-(q * np.log2(q)).sum())


def segment(t, mode):
    comps = []
    if mode == 'conservative':
        comps = ['cth', 'ckh', 'cph', 'cfh', 'ch', 'sh']
    elif mode == 'phase56':
        comps = ['cth', 'ckh', 'cph', 'cfh', 'ch', 'sh', 'iin', 'in', 'ee']
    if not comps:
        return list(t)
    out = []
    i = 0
    comps = sorted(comps, key=len, reverse=True)
    while i < len(t):
        hit = next((c for c in comps if t.startswith(c, i)), None)
        if hit:
            out.append(hit)
            i += len(hit)
        else:
            out.append(t[i])
            i += 1
    return out


@lru_cache(maxsize=None)
def feat_cached(toks_tuple, mode):
    toks = list(toks_tuple)
    units = [segment(t, mode) for t in toks]
    n = len(toks)
    lens = np.array([len(u) for u in units], float)
    flat = [u for x in units for u in x]
    ef = sum(any(lev1(a, b) for j, b in enumerate(toks) if i != j) for i, a in enumerate(toks)) / n
    loc = sum(any(lev1(a, b) for b in toks[max(0, i - 10):i]) for i, a in enumerate(toks)) / n
    kt = sum(('k' in t or 't' in t) for t in toks) / n
    k = sum(t.count('k') for t in toks)
    tt = sum(t.count('t') for t in toks)
    return np.array([
        len(set(toks)) / n,
        lens.mean(),
        lens.std(),
        len(set(flat)),
        entropy(flat),
        entropy([u[0] for u in units]),
        entropy([u[-1] for u in units]),
        ef,
        loc,
        kt,
        k / (k + tt) if k + tt else 0.0,
    ])


def feat(toks, mode):
    return feat_cached(tuple(toks), mode)


def parse(text: str):
    headers = {}
    pars = defaultdict(list)
    pid = defaultdict(int)
    for s in text.splitlines():
        h = HP.match(s)
        if h:
            headers[h.group('p')] = dict(re.findall(r'\$(\w)=([^\s>]+)', h.group('m')))
            continue
        m = LP.match(s)
        if not m or 'P' not in m.group('c'):
            continue
        page = m.group('loc').split('.')[0]
        start, z = tokens(m.group('b'))
        if start:
            pid[page] += 1
        if z and pid[page]:
            pars[(page, pid[page])].append(z)
    records = []
    for (page, _p), lines in pars.items():
        if len(lines) >= 3 and len(lines[0]) >= 5 and len(lines[2]) >= 5:
            records.append((
                page,
                int(re.match(r'f(\d+)', page).group(1)),
                headers.get(page, {}).get('I', '?'),
                lines,
            ))
    return records


def sd_from_records(records, mode):
    all_lines = [feat(line, mode) for _, _, _, lines in records for line in lines if len(line) >= 5]
    sd = np.std(np.array(all_lines), axis=0)
    sd[sd == 0] = 1.0
    return sd


def train_direction(train_records, mode, sd):
    transitions = np.array([
        (feat(r[3][2], mode) - feat(r[3][0], mode)) / sd
        for r in train_records
    ])
    d = transitions.mean(0)
    norm = np.linalg.norm(d)
    return d / norm if norm else d


def heldout_delta(record, mode, sd):
    _page, _leaf, _sec, lines = record
    pseudo = []
    for j in range(1, len(lines) - 2):
        if len(lines[j]) >= 5 and len(lines[j + 2]) >= 5:
            pseudo.append((feat(lines[j + 2], mode) - feat(lines[j], mode)) / sd)
    if not pseudo:
        return None
    real = (feat(lines[2], mode) - feat(lines[0], mode)) / sd
    return real - np.mean(pseudo, axis=0)


def summarize_crossfit(records, mode, train_only_scaling):
    leaves = np.array([r[1] for r in records])
    unique_leaves = np.unique(leaves)
    folds = [set(unique_leaves[i::5]) for i in range(5)]
    global_sd = sd_from_records(records, mode)

    rows = []
    fold_summary = []
    for fold_index, test_leaves in enumerate(folds):
        train = [r for r in records if r[1] not in test_leaves]
        test = [r for r in records if r[1] in test_leaves]
        sd = sd_from_records(train, mode) if train_only_scaling else global_sd
        direction = train_direction(train, mode, sd)
        fold_proj = []
        for record in test:
            delta = heldout_delta(record, mode, sd)
            if delta is None:
                continue
            full = float(delta @ direction)
            coord = delta * direction
            losses = {}
            for group, removed in GROUPS.items():
                keep = [i for i in range(len(NAMES)) if i not in removed]
                d = direction[keep]
                n = np.linalg.norm(d)
                if n:
                    d = d / n
                ablated = float(delta[keep] @ d)
                losses[group] = full - ablated
            rows.append({
                'fold': fold_index,
                'page': record[0],
                'leaf': int(record[1]),
                'section': record[2],
                'projection': full,
                'coord': coord,
                'ablation_loss': losses,
            })
            fold_proj.append(full)
        fold_summary.append({
            'fold': fold_index,
            'n': len(fold_proj),
            'mean_projection': float(np.mean(fold_proj)) if fold_proj else None,
            'train_leaves': len(set(r[1] for r in train)),
            'test_leaves': len(test_leaves),
        })

    mean_projection = float(np.mean([r['projection'] for r in rows]))
    coordinate = np.mean(np.array([r['coord'] for r in rows]), axis=0)
    ablation = {
        group: float(np.mean([r['ablation_loss'][group] for r in rows]))
        for group in GROUPS
    }
    sections = {}
    for sec in 'HBPST':
        vals = [r['projection'] for r in rows if r['section'] == sec]
        if vals:
            sections[sec] = {
                'n': len(vals),
                'mean_projection': float(np.mean(vals)),
                'positive_fraction': float(np.mean(np.array(vals) > 0)),
            }

    # Deterministic physical-leaf cluster bootstrap of cross-fitted coordinate contributions.
    by_leaf = defaultdict(list)
    for r in rows:
        by_leaf[r['leaf']].append(r)
    leaf_ids = sorted(by_leaf)
    rng = random.Random(60020 + MODES.index(mode) + (100 if train_only_scaling else 0))
    boots = []
    for _ in range(2000):
        sampled = [rng.choice(leaf_ids) for _ in leaf_ids]
        sample_rows = [row for leaf in sampled for row in by_leaf[leaf]]
        boots.append(np.mean(np.array([row['coord'] for row in sample_rows]), axis=0))
    B = np.array(boots)
    ci = {
        name: [float(np.quantile(B[:, i], 0.025)), float(np.quantile(B[:, i], 0.975))]
        for i, name in enumerate(NAMES)
    }
    stable = {
        name: {
            'effect': float(coordinate[i]),
            'boot95': ci[name],
        }
        for i, name in enumerate(NAMES)
        if ci[name][0] > 0 or ci[name][1] < 0
    }

    return {
        'n': len(rows),
        'mean_projection': mean_projection,
        'folds': fold_summary,
        'coordinate_contribution': dict(zip(NAMES, map(float, coordinate))),
        'stable_coordinate_effects': stable,
        'group_ablation_loss': ablation,
        'sections': sections,
    }


def summarize_legacy_public(records, mode):
    # Mirrors the current public implementation's final pooled held-out direction.
    sd = sd_from_records(records, mode)
    leaves = np.array([r[1] for r in records])
    unique_leaves = np.unique(leaves)
    folds = [set(unique_leaves[i::5]) for i in range(5)]
    deltas = []
    sections = []
    for test_leaves in folds:
        train = [r for r in records if r[1] not in test_leaves]
        test = [r for r in records if r[1] in test_leaves]
        _unused_training_direction = train_direction(train, mode, sd)
        for record in test:
            delta = heldout_delta(record, mode, sd)
            if delta is not None:
                deltas.append(delta)
                sections.append(record[2])
    D = np.array(deltas)
    direction = D.mean(0)
    direction /= np.linalg.norm(direction)
    coord = D.mean(0) * direction
    full = float(np.mean(D @ direction))
    ablation = {}
    for group, removed in GROUPS.items():
        keep = [i for i in range(len(NAMES)) if i not in removed]
        d = direction[keep]
        d /= np.linalg.norm(d)
        ablation[group] = float(full - np.mean(D[:, keep] @ d))
    return {
        'n': len(D),
        'mean_projection': full,
        'coordinate_contribution': dict(zip(NAMES, map(float, coord))),
        'group_ablation_loss': ablation,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='eva_zl3b.txt')
    parser.add_argument('--out', default='phase60b_crossfit_audit_results.json')
    args = parser.parse_args()

    data = get_source(Path(args.source))
    records = parse(data.decode('utf-8', errors='ignore'))

    accepted = {
        'raw': {'crossfit_mean': 1.0072, 'group_ablation_loss': {'near_family': 0.164, 'kt': 0.379, 'length': 0.126, 'lexical_diversity': -0.123, 'edge_entropy': -0.019}},
        'conservative': {'crossfit_mean': 0.9194, 'group_ablation_loss': {'near_family': 0.253, 'kt': 0.337, 'length': 0.046, 'lexical_diversity': -0.133, 'edge_entropy': -0.024}},
        'phase56': {'crossfit_mean': 1.1182, 'group_ablation_loss': {'near_family': 0.250, 'kt': 0.326, 'length': 0.138, 'lexical_diversity': -0.106, 'edge_entropy': -0.012}},
    }

    results = {}
    for mode in MODES:
        results[mode] = {
            'accepted_reference': accepted[mode],
            'legacy_public_reimplementation': summarize_legacy_public(records, mode),
            'corrected_crossfit_global_scaling': summarize_crossfit(records, mode, train_only_scaling=False),
            'corrected_crossfit_train_only_scaling': summarize_crossfit(records, mode, train_only_scaling=True),
        }

    out = {
        'audit': 'Phase60B cross-fit and scaling sensitivity',
        'source_git_blob_sha1': EXPECTED_GIT_BLOB_SHA1,
        'n_eligible_paragraphs': len(records),
        'changes_under_test': [
            'retain fold-specific training direction for held-out projection',
            'fit feature standard deviations on training physical leaves only',
            'cluster-bootstrap already cross-fitted coordinate contributions by physical leaf',
        ],
        'results': results,
    }
    Path(args.out).write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
