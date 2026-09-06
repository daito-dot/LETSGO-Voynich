#!/usr/bin/env python3
"""Issue #84 Phase B — preregistered cipher-family map.

Scientific authority:
  experiments/cross-linguistic-baselines/PLAN_B.md
  experiments/cross-linguistic-baselines/AMENDMENT_B0.md

Usage:
  python experiments/cross-linguistic-baselines/phase84b.py \
      /path/to/CREMMA-Medieval-LAT /path/to/naibbe-cipher OUT.json

No candidate parameter is selected from Voynich outcomes.  The Phase-A scorer is
imported unchanged.  All in-house transforms must pass exact decode closure
before any candidate score is computed.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
for rel in ("phase62", "phase64", "cross-linguistic-baselines"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as b  # noqa: E402
import phase64b_naibbe as nb  # noqa: E402
import phase84a as a84  # noqa: E402

PHASE = "84B"
PHASE_A_SHA256 = "86d18560b5999836b7c0d22fa9c3d8dbfd9f11ba246613fd0c2527d5ed5ffe1c"
VOYNICH_LABELS = ("ZL3b", "IT2a", "VT0e", "RF1b", "GC2a", "CD2a", "FG2a")
N_REPS = 5
CANDIDATE_INDEX = {
    "H2": 1,
    "H4": 2,
    "H8": 3,
    "N256-4": 4,
    "NULL10": 5,
    "NULL20": 6,
    "NULL30": 7,
    "TRANS-LINE": 8,
}
PRIMARY_KEYS = ("MI1", "z1_2", "z21_40")

Item = b.Item
Token = b.Token
Line = b.Line


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(obj) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def stable_seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8], "big")


def source_items(raw_sources: Dict[str, Sequence[Item]]) -> List[Item]:
    return [it for name in b.PRIMARY_MANUSCRIPTS for it in raw_sources[name]]


def items_to_docs(items: Sequence[Item]):
    docs: Dict[str, list] = defaultdict(list)
    for it in items:
        for line in it.lines:
            docs[it.document].extend(tuple(tok) for tok in line)
    return list(docs.items())


def copy_items(items: Sequence[Item]) -> List[Item]:
    return [Item(it.item_id, it.document, [[tuple(t) for t in line] for line in it.lines], it.leaf) for it in items]


def assert_same_items(source: Sequence[Item], decoded: Sequence[Item], label: str) -> None:
    if len(source) != len(decoded):
        raise RuntimeError(f"{label}: decoded item count mismatch {len(decoded)} != {len(source)}")
    for i, (x, y) in enumerate(zip(source, decoded)):
        if x.item_id != y.item_id or x.document != y.document or x.leaf != y.leaf:
            raise RuntimeError(f"{label}: item metadata mismatch at {i}")
        if x.lines != y.lines:
            raise RuntimeError(f"{label}: exact decode closure failed at item {x.item_id}")


def all_units(items: Sequence[Item]) -> List[str]:
    return sorted({u for it in items for line in it.lines for tok in line for u in tok})


def all_tokens(items: Sequence[Item]) -> List[Token]:
    return [tuple(tok) for it in items for line in it.lines for tok in line]


def make_sub1_maps(items: Sequence[Item]):
    units = all_units(items)
    enc = {u: f"M{i:04d}" for i, u in enumerate(units)}
    dec = {v: k for k, v in enc.items()}
    return enc, dec


def encode_unit_map(items: Sequence[Item], mapping: Dict[str, str]) -> List[Item]:
    out = []
    for it in items:
        lines = [[tuple(mapping[u] for u in tok) for tok in line] for line in it.lines]
        out.append(Item(it.item_id, it.document, lines, it.leaf))
    return out


def decode_unit_map(items: Sequence[Item], inverse: Dict[str, str]) -> List[Item]:
    out = []
    for it in items:
        lines = [[tuple(inverse[u] for u in tok) for tok in line] for line in it.lines]
        out.append(Item(it.item_id, it.document, lines, it.leaf))
    return out


def make_homophone_maps(items: Sequence[Item], k: int):
    units = all_units(items)
    enc = {u: tuple(f"H{k}_{i:04d}_{j}" for j in range(k)) for i, u in enumerate(units)}
    dec = {atom: u for u, atoms in enc.items() for atom in atoms}
    return enc, dec


def encode_homophone(items: Sequence[Item], k: int, seed: int):
    enc_map, dec_map = make_homophone_maps(items, k)
    rng = random.Random(seed)
    out = []
    for it in items:
        lines = []
        for line in it.lines:
            lines.append([tuple(rng.choice(enc_map[u]) for u in tok) for tok in line])
        out.append(Item(it.item_id, it.document, lines, it.leaf))
    return out, dec_map


def top_codebook(items: Sequence[Item], n: int = 256) -> List[Token]:
    c = Counter(all_tokens(items))
    ranked = sorted(c, key=lambda t: (-c[t], t))
    return ranked[:n]


def encode_nomenclator(
    items: Sequence[Item],
    sub_map: Dict[str, str],
    code_words: Sequence[Token],
    homophones: int,
    seed: int | None,
):
    if homophones < 1:
        raise ValueError("homophones must be >=1")
    code_enc = {
        tuple(w): tuple(f"C{rank:04d}_{j}" for j in range(homophones))
        for rank, w in enumerate(code_words)
    }
    code_dec = {atom: word for word, atoms in code_enc.items() for atom in atoms}
    sub_dec = {v: k for k, v in sub_map.items()}
    rng = random.Random(seed) if seed is not None else None
    out = []
    for it in items:
        lines = []
        for line in it.lines:
            row = []
            for tok in line:
                t = tuple(tok)
                if t in code_enc:
                    atoms = code_enc[t]
                    atom = atoms[0] if rng is None else rng.choice(atoms)
                    row.append((atom,))
                else:
                    row.append(tuple(sub_map[u] for u in t))
            lines.append(row)
        out.append(Item(it.item_id, it.document, lines, it.leaf))

    def decode(encoded: Sequence[Item]) -> List[Item]:
        decoded = []
        for it in encoded:
            lines = []
            for line in it.lines:
                row = []
                for tok in line:
                    if len(tok) == 1 and tok[0] in code_dec:
                        row.append(tuple(code_dec[tok[0]]))
                    else:
                        row.append(tuple(sub_dec[u] for u in tok))
                lines.append(row)
            decoded.append(Item(it.item_id, it.document, lines, it.leaf))
        return decoded

    return out, decode


def encode_nulls(items: Sequence[Item], sub_map: Dict[str, str], p: float, seed: int):
    sub_dec = {v: k for k, v in sub_map.items()}
    null_atoms = tuple(f"NULL_{j}" for j in range(4))
    null_set = set(null_atoms)
    rng = random.Random(seed)
    out = []
    for it in items:
        lines = []
        for line in it.lines:
            row = []
            for tok in line:
                z = []
                for u in tok:
                    z.append(sub_map[u])
                    if rng.random() < p:
                        z.append(rng.choice(null_atoms))
                row.append(tuple(z))
            lines.append(row)
        out.append(Item(it.item_id, it.document, lines, it.leaf))

    def decode(encoded: Sequence[Item]) -> List[Item]:
        decoded = []
        for it in encoded:
            lines = []
            for line in it.lines:
                row = []
                for tok in line:
                    row.append(tuple(sub_dec[u] for u in tok if u not in null_set))
                lines.append(row)
            decoded.append(Item(it.item_id, it.document, lines, it.leaf))
        return decoded

    return out, decode


def line_permutation(seed: int, document: str, item_id: str, line_index: int, n: int) -> List[int]:
    ss = stable_seed(f"issue84B:TRANS-LINE:{seed}:{document}:{item_id}:{line_index}")
    perm = list(range(n))
    random.Random(ss).shuffle(perm)
    return perm


def encode_trans_line(items: Sequence[Item], sub_map: Dict[str, str], seed: int):
    sub_dec = {v: k for k, v in sub_map.items()}
    out = []
    for it in items:
        lines = []
        for li, line in enumerate(it.lines):
            encoded = [tuple(sub_map[u] for u in tok) for tok in line]
            perm = line_permutation(seed, it.document, it.item_id, li, len(encoded))
            lines.append([encoded[j] for j in perm])
        out.append(Item(it.item_id, it.document, lines, it.leaf))

    def decode(encoded_items: Sequence[Item]) -> List[Item]:
        decoded = []
        for it in encoded_items:
            lines = []
            for li, line in enumerate(it.lines):
                perm = line_permutation(seed, it.document, it.item_id, li, len(line))
                restored: List[Token | None] = [None] * len(line)
                for out_pos, original_pos in enumerate(perm):
                    restored[original_pos] = tuple(sub_dec[u] for u in line[out_pos])
                if any(t is None for t in restored):
                    raise RuntimeError("TRANS-LINE inverse permutation incomplete")
                lines.append([t for t in restored if t is not None])
            decoded.append(Item(it.item_id, it.document, lines, it.leaf))
        return decoded

    return out, decode


def make_verbose_maps(items: Sequence[Item]):
    units = all_units(items)
    enc = {u: (f"V{i:04d}a", f"V{i:04d}b") for i, u in enumerate(units)}
    dec = {pair: u for u, pair in enc.items()}
    return enc, dec


def encode_verbose2(items: Sequence[Item], mapping: Dict[str, Tuple[str, str]]) -> List[Item]:
    out = []
    for it in items:
        lines = []
        for line in it.lines:
            row = []
            for tok in line:
                atoms = []
                for u in tok:
                    atoms.extend(mapping[u])
                row.append(tuple(atoms))
            lines.append(row)
        out.append(Item(it.item_id, it.document, lines, it.leaf))
    return out


def decode_verbose2(items: Sequence[Item], inverse: Dict[Tuple[str, str], str]) -> List[Item]:
    out = []
    for it in items:
        lines = []
        for line in it.lines:
            row = []
            for tok in line:
                if len(tok) % 2:
                    raise RuntimeError("VERBOSE2 odd atom count")
                units = []
                for i in range(0, len(tok), 2):
                    pair = (tok[i], tok[i + 1])
                    if pair not in inverse:
                        raise RuntimeError(f"VERBOSE2 unknown atom pair {pair}")
                    units.append(inverse[pair])
                row.append(tuple(units))
            lines.append(row)
        out.append(Item(it.item_id, it.document, lines, it.leaf))
    return out


def equality_relation(tokens: Sequence[Token]) -> List[List[bool]]:
    return [[a == b for b in tokens] for a in tokens]


def primary_values(score: dict) -> dict:
    return {
        "MI1": float(score["Q1"]["d1"]["corrected"]),
        "z1_2": float(score["Q2"]["z"][0]),
        "z21_40": float(score["Q2"]["z"][4]),
    }


def target_intervals(phase_a: dict) -> dict:
    for label in VOYNICH_LABELS:
        if label not in phase_a.get("voynich", {}):
            raise RuntimeError(f"Phase-A target missing {label}")
    vals = {k: [] for k in PRIMARY_KEYS}
    for label in VOYNICH_LABELS:
        v = phase_a["voynich"][label]
        vals["MI1"].append(float(v["Q1"]["d1"]["corrected"]))
        vals["z1_2"].append(float(v["Q2"]["z"][0]))
        vals["z21_40"].append(float(v["Q2"]["z"][4]))
    out = {k: [min(x), max(x)] for k, x in vals.items()}
    if any(not all(math.isfinite(y) for y in interval) or interval[0] > interval[1] for interval in out.values()):
        raise RuntimeError("invalid Phase-A target interval")
    return out


def interval_distance(x: float, interval: Sequence[float]) -> float:
    lo, hi = map(float, interval)
    if x < lo:
        return float(x - lo)
    if x > hi:
        return float(x - hi)
    return 0.0


def summarize_candidate(rows: Sequence[dict], intervals: dict, external: bool = False) -> dict:
    if not rows:
        raise RuntimeError("empty candidate rows")
    pv = [primary_values(r) for r in rows]
    center = {k: float(statistics.median([x[k] for x in pv])) for k in PRIMARY_KEYS}
    responsibilities = {
        "R_MI": intervals["MI1"][0] <= center["MI1"] <= intervals["MI1"][1],
        "R_SHORT": intervals["z1_2"][0] <= center["z1_2"] <= intervals["z1_2"][1],
        "R_MID": intervals["z21_40"][0] <= center["z21_40"] <= intervals["z21_40"][1],
    }
    n = sum(bool(x) for x in responsibilities.values())
    if n == 3:
        classification = "VOYNICH INTER-TOKEN REGIME HIT"
    elif n == 2:
        classification = "PARTIAL INTER-TOKEN HIT (2/3)"
    elif n == 1:
        classification = "PARTIAL INTER-TOKEN HIT (1/3)"
    else:
        classification = "NO INTER-TOKEN HIT"
    return {
        "external_candidate": bool(external),
        "n_realizations": len(rows),
        "primary_per_realization": pv,
        "primary_center_componentwise_median": center,
        "target_intervals": intervals,
        "signed_distance_to_target_interval": {
            k: interval_distance(center[k], intervals[k]) for k in PRIMARY_KEYS
        },
        "responsibilities": responsibilities,
        "n_responsibilities_passed": n,
        "classification": classification,
    }


def check_p0_anchor(score: dict, phase_a: dict) -> dict:
    ref = phase_a["anchors"]["CREMMA_Latin_graphematic"]
    for k in ("n_tokens", "n_types", "n_docs"):
        if score[k] != ref[k]:
            raise RuntimeError(f"P0 anchor mismatch {k}: {score[k]} != {ref[k]}")
    if not np.allclose(score["Q2"]["observed"], ref["Q2"]["observed"], atol=1e-15, rtol=0):
        raise RuntimeError("P0 exact repeat-rate anchor mismatch")
    for d in ("d1", "d2", "d5", "d20"):
        if abs(float(score["Q1"][d]["observed"]) - float(ref["Q1"][d]["observed"])) > 1e-12:
            raise RuntimeError(f"P0 observed MI anchor mismatch {d}")
        if abs(float(score["Q1"][d]["corrected"]) - float(ref["Q1"][d]["corrected"])) > 1e-9:
            raise RuntimeError(f"P0 corrected MI anchor mismatch {d}")
    if not np.allclose(score["Q2"]["z"], ref["Q2"]["z"], atol=1e-8, rtol=0):
        raise RuntimeError("P0 Q2 null-calibrated anchor mismatch")
    return {
        "status": "PASS",
        "n_tokens": score["n_tokens"],
        "n_types": score["n_types"],
        "MI1": score["Q1"]["d1"]["corrected"],
        "z1_2": score["Q2"]["z"][0],
        "z21_40": score["Q2"]["z"][4],
    }


def rep_seed(candidate: str, rep: int) -> int:
    return 8420000 + 100 * CANDIDATE_INDEX[candidate] + rep


def score_rows(label: str, reps: Sequence[Sequence[Item]]) -> List[dict]:
    rows = []
    for ri, items in enumerate(reps):
        print(f"score {label} rep{ri}", file=sys.stderr, flush=True)
        rows.append(a84.score(f"Phase84B:{label}:rep{ri}", items_to_docs(items)))
    return rows


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        print(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT OUT.json", file=sys.stderr)
        return 2

    cremma_root = Path(argv[1]).resolve()
    naibbe_root = Path(argv[2]).resolve()
    out_path = Path(argv[3]).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    phase_a_path = HERE / "first-reveal" / "phase84a_results.json"
    if sha256_file(phase_a_path) != PHASE_A_SHA256:
        raise RuntimeError("Phase-A result SHA-256 mismatch")
    phase_a = json.loads(phase_a_path.read_text(encoding="utf-8"))
    intervals = target_intervals(phase_a)

    cremma_commit = b.verify_cremma_commit(cremma_root)
    raw_sources = {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }
    src = source_items(raw_sources)
    if not src:
        raise RuntimeError("empty CREMMA source")

    # P0 is a source/scorer replay control, not a Phase-B cipher candidate.
    print("preflight P0 anchor", file=sys.stderr, flush=True)
    p0_score = a84.score("CREMMA", items_to_docs(src))
    p0_check = check_p0_anchor(p0_score, phase_a)

    sub_map, sub_inv = make_sub1_maps(src)
    sub1 = encode_unit_map(src, sub_map)
    assert_same_items(src, decode_unit_map(sub1, sub_inv), "SUB1")

    verbose_map, verbose_inv = make_verbose_maps(src)
    verbose2 = encode_verbose2(src, verbose_map)
    assert_same_items(src, decode_verbose2(verbose2, verbose_inv), "VERBOSE2")

    # Equality-relation invariance is checked on a frozen first-200-token sample.
    src_sample = all_tokens(src)[:200]
    sub_sample = all_tokens(sub1)[:200]
    verbose_sample = all_tokens(verbose2)[:200]
    source_relation = equality_relation(src_sample)
    if equality_relation(sub_sample) != source_relation:
        raise RuntimeError("SUB1 token-equality invariance failed")
    if equality_relation(verbose_sample) != source_relation:
        raise RuntimeError("VERBOSE2 token-equality invariance failed")

    code_words = top_codebook(src, 256)
    if len(code_words) != 256:
        raise RuntimeError(f"expected 256 nomenclator words, got {len(code_words)}")

    generated: Dict[str, List[List[Item]]] = {
        "SUB1": [sub1],
        "VERBOSE2": [verbose2],
    }
    closure = {"SUB1": [True], "VERBOSE2": [True]}

    n1, n1_decode = encode_nomenclator(src, sub_map, code_words, homophones=1, seed=None)
    assert_same_items(src, n1_decode(n1), "N256-1")
    generated["N256-1"] = [n1]
    closure["N256-1"] = [True]

    for candidate, k in (("H2", 2), ("H4", 4), ("H8", 8)):
        generated[candidate] = []
        closure[candidate] = []
        for r in range(N_REPS):
            enc, dec_map = encode_homophone(src, k, rep_seed(candidate, r))
            assert_same_items(src, decode_unit_map(enc, dec_map), f"{candidate}:rep{r}")
            generated[candidate].append(enc)
            closure[candidate].append(True)

    generated["N256-4"] = []
    closure["N256-4"] = []
    for r in range(N_REPS):
        enc, decoder = encode_nomenclator(src, sub_map, code_words, homophones=4, seed=rep_seed("N256-4", r))
        assert_same_items(src, decoder(enc), f"N256-4:rep{r}")
        generated["N256-4"].append(enc)
        closure["N256-4"].append(True)

    for candidate, p in (("NULL10", 0.10), ("NULL20", 0.20), ("NULL30", 0.30)):
        generated[candidate] = []
        closure[candidate] = []
        for r in range(N_REPS):
            enc, decoder = encode_nulls(src, sub_map, p, rep_seed(candidate, r))
            assert_same_items(src, decoder(enc), f"{candidate}:rep{r}")
            generated[candidate].append(enc)
            closure[candidate].append(True)

    generated["TRANS-LINE"] = []
    closure["TRANS-LINE"] = []
    for r in range(N_REPS):
        enc, decoder = encode_trans_line(src, sub_map, rep_seed("TRANS-LINE", r))
        assert_same_items(src, decoder(enc), f"TRANS-LINE:rep{r}")
        generated["TRANS-LINE"].append(enc)
        closure["TRANS-LINE"].append(True)

    # Exact published Naibbe source checks are performed before candidate scoring.
    module = nb.load_naibbe(naibbe_root)
    original_map = dict(module.placeholder_to_glyph)
    if len(original_map) != len(module.TABLES) * len(module.STATES) * len(nb.EFFECTIVE_LETTERS):
        raise RuntimeError("unexpected Naibbe codebook size")
    naibbe_primary: List[List[Item]] = []
    naibbe_raw: List[List[Item]] = []
    naibbe_diagnostics = []
    for r in range(N_REPS):
        pitems: List[Item] = []
        ritems: List[Item] = []
        diag = {}
        for mi, manuscript in enumerate(b.PRIMARY_MANUSCRIPTS):
            seed = 6480000 + 100 * mi + r
            primary, raw, d = nb.encrypt_manuscript(
                module, raw_sources[manuscript], manuscript, original_map, seed
            )
            pitems.extend(primary)
            ritems.extend(raw)
            diag[manuscript] = d
        naibbe_primary.append(pitems)
        naibbe_raw.append(ritems)
        naibbe_diagnostics.append(diag)

    # All preregistered generation and exact-closure checks have completed.
    # Candidate scoring starts only below this line.
    candidate_results = {}
    order = (
        "SUB1", "H2", "H4", "H8", "N256-1", "N256-4",
        "NULL10", "NULL20", "NULL30", "TRANS-LINE", "VERBOSE2",
    )
    for candidate in order:
        rows = score_rows(candidate, generated[candidate])
        candidate_results[candidate] = {
            "reversibility": {
                "prerequisite": "T1 exact source closure",
                "all_realizations_pass": all(closure[candidate]),
                "per_realization": closure[candidate],
            },
            "scores": rows,
            "summary": summarize_candidate(rows, intervals, external=False),
        }

    naibbe_rows = score_rows("NAIBBE", naibbe_primary)
    naibbe_raw_rows = score_rows("NAIBBE-RAW-SENSITIVITY", naibbe_raw)
    candidate_results["NAIBBE"] = {
        "reversibility": {
            "prerequisite": "external published mechanism; no new exact diplomatic-CREMMA closure claim",
            "all_realizations_pass": None,
            "note": "Phase64B clean/projection/respacing interface retained exactly; target-aware codebook caveat retained",
        },
        "scores": naibbe_rows,
        "summary": summarize_candidate(naibbe_rows, intervals, external=True),
        "raw_token_sensitivity_nonpromoting": {
            "scores": naibbe_raw_rows,
            "summary": summarize_candidate(naibbe_raw_rows, intervals, external=True),
        },
        "generation_diagnostics": naibbe_diagnostics,
        "frozen_surface_annotation": {
            "R1_rescored_here": False,
            "authority": "Issue #68 / Phase64 frozen Naibbe surface evidence",
            "interpretation": "concrete codebook is target-aware; do not generalize R1 to abstract cipher families",
        },
    }

    hits = [
        name for name, row in candidate_results.items()
        if row["summary"]["classification"] == "VOYNICH INTER-TOKEN REGIME HIT"
    ]
    target_independent_hits = [name for name in hits if name != "NAIBBE"]

    out = {
        "schema": "issue84-phaseB-v1",
        "phase": PHASE,
        "plan": "experiments/cross-linguistic-baselines/PLAN_B.md",
        "prereveal_amendment": "experiments/cross-linguistic-baselines/AMENDMENT_B0.md",
        "inputs": {
            "cremma_commit": cremma_commit,
            "cremma_manuscripts": list(b.PRIMARY_MANUSCRIPTS),
            "phaseA_results_sha256": sha256_file(phase_a_path),
            "naibbe_commit": nb.NAIBBE_COMMIT,
            "naibbe_v2_blob": nb.NAIBBE_PY_BLOB,
            "naibbe_tables_blob": nb.NAIBBE_TABLE_BLOB,
            "naibbe_readme_blob": nb.NAIBBE_README_BLOB,
        },
        "target_authority": {
            "voynich_labels": list(VOYNICH_LABELS),
            "intervals_exact_from_phaseA": intervals,
            "threshold_source": "T2 empirical seven-reading target variation",
            "far_bins_decisive": False,
        },
        "preflight": {
            "P0_phaseA_anchor_replay": p0_check,
            "source_items": len(src),
            "source_tokens": len(all_tokens(src)),
            "source_units": len(all_units(src)),
            "token_equality_sample_n": len(src_sample),
            "SUB1_equality_relation_preserved": True,
            "VERBOSE2_equality_relation_preserved": True,
            "all_inhouse_full_source_decode_closures_passed_before_scoring": True,
        },
        "candidate_design": {
            "stochastic_replicates": N_REPS,
            "seed_formula": "8420000 + 100*candidate_index + replicate",
            "candidate_indices": CANDIDATE_INDEX,
            "nomenclator_top_words": 256,
            "nomenclator_word_list_sha256": canonical_hash([list(x) for x in code_words]),
            "SUB1_unit_map_sha256": canonical_hash(sub_map),
            "null_atoms": 4,
            "naibbe_seed_formula": "6480000 + 100*manuscript_index + realization (reused from Phase64B)",
        },
        "P0_source_anchor_score": p0_score,
        "candidates": candidate_results,
        "across_candidates": {
            "hits": hits,
            "target_independent_inhouse_hits": target_independent_hits,
            "n_hits": len(hits),
            "n_target_independent_hits": len(target_independent_hits),
            "classification_rule": "all three componentwise-median responsibilities inside the exact seven-reading target intervals",
        },
        "claim_limit": (
            "Phase-B operation-family screen only. A hit does not identify plaintext, key, meaning, historical mechanism, "
            "or decipherment; a generic miss rejects only the frozen representative, not every member of the broad family."
        ),
    }
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    compact = {
        name: {
            "center": row["summary"]["primary_center_componentwise_median"],
            "responsibilities": row["summary"]["responsibilities"],
            "classification": row["summary"]["classification"],
        }
        for name, row in candidate_results.items()
    }
    print(json.dumps({"target_intervals": intervals, "candidates": compact, "hits": hits}, indent=1), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
