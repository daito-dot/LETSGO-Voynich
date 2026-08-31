#!/usr/bin/env python3
"""Phase66A direct-music screen.

Implements experiments/phase66/PLAN_A.md. Scientific output is JSON on stdout.
No parameter selection is performed after reveal.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import re
import statistics
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_CREMMA_COMMIT = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_CHANT_BLOB = "616fcd986226873cb1f58b8711c1936ad0794af4"
PRIMARY_MANUSCRIPTS = {
    "BIS193": "data/BIS-193",
    "CLM13027": "data/CLM13027",
    "Mazarine915": "data/Mazarine915",
    "UBL758": "data/UBL758",
}
PITCH_ALPHABET = "89abcdefghijklmnopqrs"
BARLINES = set("345")
NULL_REPS = 500
EPS = 1e-12

LP = re.compile(r"^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<c>[^>]*)>\s+(?P<b>.*)$")
LEAF_RE = re.compile(r"f(\d+)")


@dataclass
class Item:
    item_id: str
    document: str
    sequences: List[List[str]]
    leaf: Optional[int] = None


@dataclass
class StateItem:
    item_id: str
    document: str
    sequences: List[List[int]]
    leaf: Optional[int] = None


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_seed(label: str, replicate: int) -> int:
    raw = hashlib.sha256(f"{label}:{replicate}".encode("utf-8")).digest()
    return int.from_bytes(raw[:8], "big")


def normalize_ascii_token(token: str) -> str:
    folded = unicodedata.normalize("NFKD", token.lower())
    return "".join(ch for ch in folded if "a" <= ch <= "z")


def voynich_token_strings(body: str) -> Tuple[bool, List[str]]:
    start = "<%>" in body
    body = body.replace("<%>", " ")
    body = re.sub(r"<[^>]*>", " ", body)
    toks = [re.sub(r"[^A-Za-z]", "", x).lower() for x in re.split(r"[.\s]+", body)]
    return start, [x for x in toks if x]


def parse_voynich(path: Path) -> List[Item]:
    pid: Dict[str, int] = defaultdict(int)
    current: Dict[str, Item] = {}
    out: List[Item] = []
    for s in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = LP.match(s)
        if not m or "P" not in m.group("c"):
            continue
        page = m.group("loc").split(".")[0]
        start, toks = voynich_token_strings(m.group("b"))
        if start:
            if page in current:
                out.append(current.pop(page))
            pid[page] += 1
            lm = LEAF_RE.match(page)
            leaf = int(lm.group(1)) if lm else None
            current[page] = Item(f"{page}:p{pid[page]}", page, [], leaf)
        if toks and page in current:
            current[page].sequences.append(toks)
    out.extend(current.values())
    out.sort(key=lambda x: (x.leaf if x.leaf is not None else 10**9, x.document, x.item_id))
    return out


def phase62_base_eligible(item: Item) -> bool:
    return (
        len(item.sequences) >= 3
        and len(item.sequences[0]) >= 5
        and len(item.sequences[2]) >= 5
    )


def physical_leaf_folds(items: Sequence[Item]) -> List[Set[int]]:
    leaves = sorted({it.leaf for it in items if it.leaf is not None and phase62_base_eligible(it)})
    return [set(leaves[i::5]) for i in range(5)]


def latin_word_strings(text: str) -> List[str]:
    text = unicodedata.normalize("NFC", text)
    words: List[str] = []
    cur: List[str] = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("M"):
            cur.append(ch)
        else:
            if cur:
                w = normalize_ascii_token("".join(cur))
                if w:
                    words.append(w)
                cur = []
    if cur:
        w = normalize_ascii_token("".join(cur))
        if w:
            words.append(w)
    return words


def parse_latin_file(path: Path, root: Path, manuscript: str) -> List[Item]:
    out: List[Item] = []
    current: Optional[Item] = None
    marker_no = 0
    rel = str(path.relative_to(root))
    for source_line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if "¶" not in raw:
            if current is not None:
                toks = latin_word_strings(raw)
                if toks:
                    current.sequences.append(toks)
            continue

        parts = raw.split("¶")
        prefix = parts[0]
        if current is not None:
            toks = latin_word_strings(prefix)
            if toks:
                current.sequences.append(toks)

        for segment in parts[1:]:
            if current is not None:
                out.append(current)
            marker_no += 1
            current = Item(
                f"{rel}:{source_line_no}:pilcrow{marker_no}",
                manuscript,
                [],
                None,
            )
            toks = latin_word_strings(segment)
            if toks:
                current.sequences.append(toks)
    if current is not None:
        out.append(current)
    return out


def parse_latin_manuscript(root: Path, manuscript: str, rel_dir: str) -> List[Item]:
    d = root / rel_dir
    if not d.is_dir():
        raise RuntimeError(f"missing manuscript directory: {d}")
    out: List[Item] = []
    for p in sorted(d.rglob("*.txt")):
        out.extend(parse_latin_file(p, root, manuscript))
    return out


def verify_git_commit(root: Path, expected: str, label: str) -> str:
    got = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if got != expected:
        raise RuntimeError(f"{label} commit mismatch: {got} != {expected}")
    return got


def token_feature(token: str) -> np.ndarray:
    t = normalize_ascii_token(token)
    if not t:
        raise ValueError("empty normalized token")
    v = np.zeros(79, dtype=float)
    v[0] = len(t)
    n = float(len(t))
    for ch in t:
        v[1 + ord(ch) - 97] += 1.0 / n
    v[27 + ord(t[0]) - 97] = 1.0
    v[53 + ord(t[-1]) - 97] = 1.0
    return v


class FrozenKMeans:
    def __init__(self, k: int):
        self.k = k
        self.mean: Optional[np.ndarray] = None
        self.sd: Optional[np.ndarray] = None
        self.centroids: Optional[np.ndarray] = None

    def fit(self, tokens: Iterable[str]) -> "FrozenKMeans":
        types = sorted({normalize_ascii_token(t) for t in tokens if normalize_ascii_token(t)})
        if len(types) < self.k:
            raise RuntimeError(f"not enough unique types for k={self.k}: {len(types)}")
        raw = np.vstack([token_feature(t) for t in types])
        mean = raw.mean(axis=0)
        sd = raw.std(axis=0)
        sd[sd == 0] = 1.0
        x = (raw - mean) / sd

        chosen: List[int] = [0]
        while len(chosen) < self.k:
            c = x[np.array(chosen)]
            d2 = ((x[:, None, :] - c[None, :, :]) ** 2).sum(axis=2).min(axis=1)
            for idx in chosen:
                d2[idx] = -1.0
            maxv = float(d2.max())
            candidates = [i for i, val in enumerate(d2) if abs(float(val) - maxv) <= 1e-12]
            chosen.append(min(candidates, key=lambda i: types[i]))

        centroids = x[np.array(chosen)].copy()
        prev_assign: Optional[np.ndarray] = None
        for _ in range(100):
            d2 = ((x[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
            assign = np.argmin(d2, axis=1)
            if prev_assign is not None and np.array_equal(assign, prev_assign):
                break
            newc = centroids.copy()
            used_replacements: Set[int] = set()
            own_dist = d2[np.arange(len(x)), assign]
            for j in range(self.k):
                members = x[assign == j]
                if len(members):
                    newc[j] = members.mean(axis=0)
                else:
                    order = sorted(
                        range(len(types)),
                        key=lambda i: (-float(own_dist[i]), types[i]),
                    )
                    pick = next(i for i in order if i not in used_replacements)
                    used_replacements.add(pick)
                    newc[j] = x[pick]
            centroids = newc
            prev_assign = assign

        self.mean = mean
        self.sd = sd
        self.centroids = centroids
        return self

    def transform_token(self, token: str) -> int:
        if self.mean is None or self.sd is None or self.centroids is None:
            raise RuntimeError("model not fitted")
        t = normalize_ascii_token(token)
        if not t:
            raise ValueError("empty evaluation token")
        x = (token_feature(t) - self.mean) / self.sd
        d2 = ((self.centroids - x) ** 2).sum(axis=1)
        return int(np.argmin(d2))


def state_items(items: Sequence[Item], model: FrozenKMeans, final_only: bool = False) -> List[StateItem]:
    out: List[StateItem] = []
    for it in items:
        seqs: List[List[int]] = []
        if final_only:
            if it.sequences and len(it.sequences[-1]) >= 5:
                seqs = [[model.transform_token(t) for t in it.sequences[-1]]]
        else:
            for seq in it.sequences:
                if len(seq) >= 5:
                    seqs.append([model.transform_token(t) for t in seq])
        if seqs:
            out.append(StateItem(it.item_id, it.document, seqs, it.leaf))
    return out


def chant_pitch_index(ch: str) -> Optional[int]:
    c = ch.lower() if ch.isalpha() else ch
    try:
        return PITCH_ALPHABET.index(c)
    except ValueError:
        return None


def parse_chants(path: Path, modulo: int = 7, ending_filter: Optional[str] = None) -> List[StateItem]:
    out: List[StateItem] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            vol = (row.get("volpiano") or "").strip()
            if not vol:
                continue
            phrases: List[Tuple[List[int], Optional[str]]] = []
            cur: List[int] = []
            for ch in vol:
                if ch in BARLINES:
                    phrases.append((cur, ch))
                    cur = []
                    continue
                idx = chant_pitch_index(ch)
                if idx is not None:
                    cur.append(idx % modulo)
            if cur:
                phrases.append((cur, None))
            seqs = [seq for seq, end in phrases if len(seq) >= 5 and (ending_filter is None or end == ending_filter)]
            if seqs:
                cid = row.get("id") or row.get("cantus_id") or f"chant:{len(out)}"
                out.append(StateItem(cid, "CHANT", seqs, None))
    return out


def collision(values: Sequence[Tuple[int, ...] | int]) -> float:
    if not values:
        return 0.0
    c = Counter(values)
    n = float(sum(c.values()))
    return sum((v / n) ** 2 for v in c.values())


def motif_mass(items: Sequence[StateItem], ngram: int) -> Tuple[float, int]:
    repeated = 0
    total = 0
    for it in items:
        c: Counter[Tuple[int, ...]] = Counter()
        for seq in it.sequences:
            for i in range(len(seq) - ngram + 1):
                c[tuple(seq[i:i + ngram])] += 1
        item_total = sum(c.values())
        if item_total:
            repeated += sum(max(v - 1, 0) for v in c.values())
            total += item_total
    return (repeated / total if total else 0.0), total


def raw_metrics(items: Sequence[StateItem]) -> Dict[str, float]:
    seqs = [s for it in items for s in it.sequences if len(s) >= 5]
    finals = [s[-1] for s in seqs]
    body = [x for s in seqs for x in s[:-1]]
    final2 = [(s[-2], s[-1]) for s in seqs]
    body2 = [(s[i], s[i + 1]) for s in seqs for i in range(max(0, len(s) - 2))]
    m3, _ = motif_mass(items, 3)
    m4, _ = motif_mass(items, 4)
    return {
        "M1": collision(finals) - collision(body),
        "M2": collision(final2) - collision(body2),
        "M3": m3,
        "M4": m4,
    }


def shuffle_items(items: Sequence[StateItem], rng: random.Random) -> List[StateItem]:
    out: List[StateItem] = []
    for it in items:
        seqs: List[List[int]] = []
        for seq in it.sequences:
            q = list(seq)
            rng.shuffle(q)
            seqs.append(q)
        out.append(StateItem(it.item_id, it.document, seqs, it.leaf))
    return out


def evaluate(items: Sequence[StateItem], label: str) -> dict:
    observed = raw_metrics(items)
    null_rows: List[Dict[str, float]] = []
    for r in range(NULL_REPS):
        rng = random.Random(stable_seed(label, r))
        null_rows.append(raw_metrics(shuffle_items(items, rng)))

    metrics: Dict[str, dict] = {}
    zvec: List[float] = []
    for key in ("M1", "M2", "M3", "M4"):
        vals = [row[key] for row in null_rows]
        mean = statistics.fmean(vals)
        sd = math.sqrt(statistics.fmean([(v - mean) ** 2 for v in vals]))
        obs = observed[key]
        z = (obs - mean) / sd if sd > 0 else 0.0
        extreme = sum(abs(v - mean) >= abs(obs - mean) - 1e-15 for v in vals)
        p = (1 + extreme) / (NULL_REPS + 1)
        metrics[key] = {
            "observed": obs,
            "null_mean": mean,
            "null_sd": sd,
            "Z": z,
            "p_two_sided": p,
        }
        zvec.append(z)

    n_sequences = sum(len(it.sequences) for it in items)
    n_events = sum(len(seq) for it in items for seq in it.sequences)
    m3_count = motif_mass(items, 3)[1]
    m4_count = motif_mass(items, 4)[1]
    return {
        "label": label,
        "counts": {
            "items": len(items),
            "sequences": n_sequences,
            "events": n_events,
            "threegrams": m3_count,
            "fourgrams": m4_count,
        },
        "metrics": metrics,
        "Z_vector": zvec,
        "null_reps": NULL_REPS,
    }


def all_tokens(items: Sequence[Item]) -> Iterable[str]:
    for it in items:
        for seq in it.sequences:
            for t in seq:
                yield t


def euclidean(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def mean_vector(vectors: Sequence[Sequence[float]]) -> List[float]:
    return [statistics.fmean(row[j] for row in vectors) for j in range(len(vectors[0]))]


def run_primary(vitems: List[Item], latin_by_ms: Dict[str, List[Item]], chant_path: Path, k: int = 7) -> dict:
    folds = physical_leaf_folds(vitems)
    fold_union = set().union(*folds)
    vfolds: List[dict] = []
    for fi, test_leaves in enumerate(folds):
        train = [it for it in vitems if it.leaf in fold_union and it.leaf not in test_leaves]
        test = [it for it in vitems if it.leaf in test_leaves]
        km = FrozenKMeans(k).fit(all_tokens(train))
        ev = evaluate(state_items(test, km), f"phase66a:voynich:k{k}:fold{fi}")
        ev["fold"] = fi
        ev["test_leaves"] = sorted(test_leaves)
        ev["training_type_count"] = len({normalize_ascii_token(x) for x in all_tokens(train) if normalize_ascii_token(x)})
        vfolds.append(ev)

    latin_all = [it for ms in PRIMARY_MANUSCRIPTS for it in latin_by_ms[ms]]
    lkm = FrozenKMeans(k).fit(all_tokens(latin_all))
    latin_results: Dict[str, dict] = {}
    for ms in PRIMARY_MANUSCRIPTS:
        latin_results[ms] = evaluate(state_items(latin_by_ms[ms], lkm), f"phase66a:latin:k{k}:{ms}")
    latin_vec = mean_vector([latin_results[ms]["Z_vector"] for ms in PRIMARY_MANUSCRIPTS])

    chant_items = parse_chants(chant_path, modulo=k)
    chant = evaluate(chant_items, f"phase66a:chant:k{k}:all")
    chant_vec = chant["Z_vector"]

    distances: List[dict] = []
    for row in vfolds:
        vv = row["Z_vector"]
        dm = euclidean(vv, chant_vec)
        dl = euclidean(vv, latin_vec)
        distances.append({
            "fold": row["fold"],
            "D_music": dm,
            "D_latin": dl,
            "music_closer": dm < dl,
        })

    voy_mean = mean_vector([r["Z_vector"] for r in vfolds])
    wins = sum(r["music_closer"] for r in distances)
    mean_dm = statistics.fmean(r["D_music"] for r in distances)
    mean_dl = statistics.fmean(r["D_latin"] for r in distances)
    same_m1 = (voy_mean[0] > 0 and chant_vec[0] > 0) or (voy_mean[0] < 0 and chant_vec[0] < 0)
    same_m2 = (voy_mean[1] > 0 and chant_vec[1] > 0) or (voy_mean[1] < 0 and chant_vec[1] < 0)
    c4_m1 = abs(voy_mean[0] - chant_vec[0]) < abs(voy_mean[0] - latin_vec[0])
    c4_m2 = abs(voy_mean[1] - chant_vec[1]) < abs(voy_mean[1] - latin_vec[1])
    conditions = {
        "C1_music_closer_at_least_4_of_5": wins >= 4,
        "C2_mean_music_distance_smaller": mean_dm < mean_dl,
        "C3_M1_M2_same_sign_as_chant": same_m1 and same_m2,
        "C4_at_least_one_cadence_coordinate_closer_to_chant": c4_m1 or c4_m2,
    }
    if wins < 4:
        classification = "DIRECT-MUSIC SCREEN NEGATIVE"
    elif all(conditions.values()):
        classification = "DIRECT-MUSIC SCREEN POSITIVE"
    else:
        classification = "MIXED"

    return {
        "k": k,
        "voynich_folds": vfolds,
        "latin_manuscripts": latin_results,
        "latin_equal_weight_Z_vector": latin_vec,
        "chant": chant,
        "voynich_mean_Z_vector": voy_mean,
        "distances": distances,
        "distance_summary": {
            "music_closer_folds": wins,
            "mean_D_music": mean_dm,
            "mean_D_latin": mean_dl,
        },
        "conditions": conditions,
        "classification": classification,
    }


def run_paragraph_final(vitems: List[Item], k: int = 7) -> dict:
    folds = physical_leaf_folds(vitems)
    fold_union = set().union(*folds)
    rows: List[dict] = []
    for fi, test_leaves in enumerate(folds):
        train = [it for it in vitems if it.leaf in fold_union and it.leaf not in test_leaves]
        test = [it for it in vitems if it.leaf in test_leaves]
        km = FrozenKMeans(k).fit(all_tokens(train))
        ev = evaluate(state_items(test, km, final_only=True), f"phase66a:sensitivity:paragraph-final:k{k}:fold{fi}")
        ev["fold"] = fi
        ev["test_leaves"] = sorted(test_leaves)
        rows.append(ev)
    return {"voynich_folds": rows, "mean_Z_vector": mean_vector([r["Z_vector"] for r in rows])}


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT /path/to/test-chants.csv",
            file=sys.stderr,
        )
        return 2

    vpath = Path(sys.argv[1]).resolve()
    cremma = Path(sys.argv[2]).resolve()
    chant_path = Path(sys.argv[3]).resolve()
    if git_blob_sha1(vpath.read_bytes()) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b blob mismatch")
    verify_git_commit(cremma, EXPECTED_CREMMA_COMMIT, "CREMMA")
    if git_blob_sha1(chant_path.read_bytes()) != EXPECTED_CHANT_BLOB:
        raise RuntimeError("plainchant blob mismatch")

    vitems = parse_voynich(vpath)
    latin_by_ms = {
        ms: parse_latin_manuscript(cremma, ms, rel)
        for ms, rel in PRIMARY_MANUSCRIPTS.items()
    }

    primary = run_primary(vitems, latin_by_ms, chant_path, k=7)
    paragraph_final = run_paragraph_final(vitems, k=7)
    chant4_items = parse_chants(chant_path, modulo=7, ending_filter="4")
    chant4 = None
    if sum(len(x.sequences) for x in chant4_items) >= 100:
        chant4 = evaluate(chant4_items, "phase66a:sensitivity:chant-ending4:k7")
    k6 = run_primary(vitems, latin_by_ms, chant_path, k=6)

    here = Path(__file__).resolve().parent
    plan = here / "PLAN_A.md"
    result = {
        "experiment": "Phase66A direct-music screen",
        "issue": 26,
        "inputs": {
            "voynich_git_blob_sha1": EXPECTED_ZL3B_BLOB,
            "cremma_commit": EXPECTED_CREMMA_COMMIT,
            "plainchant_git_blob_sha1": EXPECTED_CHANT_BLOB,
            "plainchant_source_commit": "ab3edb742a718fe5c3fd40550c54f104fe9b6078",
            "plan_sha256": sha256_file(plan),
            "script_sha256": sha256_file(Path(__file__)),
        },
        "primary": primary,
        "sensitivities": {
            "voynich_paragraph_final_lines": paragraph_final,
            "chant_barline4_only": chant4,
            "k6_solmization": k6,
        },
        "frozen_primary_classification": primary["classification"],
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
