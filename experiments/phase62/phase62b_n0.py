#!/usr/bin/env python3
"""Phase62B N0 structured-medieval baseline.

Implements experiments/phase62/PLAN.md and IMPLEMENTATION_B.md.
This executable evaluates N0 only. It intentionally contains no C0/A1
comparison and no implementation of the sealed prospective H62-P1 statistic.

Usage:
  python experiments/phase62/phase62b_n0.py /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT
"""
from __future__ import annotations

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
PRIMARY_MANUSCRIPTS = {
    "BIS193": "data/BIS-193",
    "CLM13027": "data/CLM13027",
    "Mazarine915": "data/Mazarine915",
    "UBL758": "data/UBL758",
}
SENSITIVITY_MANUSCRIPTS = {"H318": "data/H318"}
NULL_REPS = 100
STABLE_EPS = 1e-9

HP = re.compile(r"^<(?P<p>f\d+[rv]\d*)>\s+<!\s*(?P<m>.*?)>")
LP = re.compile(r"^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<c>[^>]*)>\s+(?P<b>.*)$")
LEAF_RE = re.compile(r"f(\d+)")

Unit = str
Token = Tuple[Unit, ...]
Line = List[Token]


@dataclass
class Item:
    item_id: str
    document: str
    lines: List[Line]
    leaf: Optional[int] = None


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def stable_seed(label: str, offset: int = 0) -> int:
    b = hashlib.sha256(label.encode("utf-8")).digest()
    return int.from_bytes(b[:8], "big") % (2**31 - 1) + offset


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
                words.append("".join(cur).lower())
                cur = []
    if cur:
        words.append("".join(cur).lower())
    return words


def latin_units(word: str) -> Token:
    units: List[str] = []
    for ch in unicodedata.normalize("NFC", word):
        cat = unicodedata.category(ch)
        if cat.startswith("M") and units:
            units[-1] += ch
        else:
            units.append(ch)
    return tuple(units)


def latin_line(text: str) -> Line:
    return [latin_units(w) for w in latin_word_strings(text) if w]


def voynich_token_strings(body: str) -> Tuple[bool, List[str]]:
    start = "<%>" in body
    body = body.replace("<%>", " ")
    body = re.sub(r"<[^>]*>", " ", body)
    toks = [re.sub(r"[^A-Za-z]", "", x).lower() for x in re.split(r"[.\s]+", body)]
    return start, [x for x in toks if x]


def voynich_line(body: str) -> Tuple[bool, Line]:
    start, words = voynich_token_strings(body)
    return start, [tuple(w) for w in words]


def parse_voynich(path: Path) -> List[Item]:
    items: List[Item] = []
    pid: Dict[str, int] = defaultdict(int)
    current: Dict[str, Item] = {}
    for s in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = LP.match(s)
        if not m or "P" not in m.group("c"):
            continue
        page = m.group("loc").split(".")[0]
        start, toks = voynich_line(m.group("b"))
        if start:
            if page in current:
                items.append(current.pop(page))
            pid[page] += 1
            mm = LEAF_RE.match(page)
            leaf = int(mm.group(1)) if mm else None
            current[page] = Item(f"{page}:p{pid[page]}", page, [], leaf)
        if toks and page in current:
            current[page].lines.append(toks)
    items.extend(current.values())
    items.sort(key=lambda x: (x.leaf if x.leaf is not None else 10**9, x.document, x.item_id))
    return items


def close_item(current: Optional[Item], out: List[Item]) -> None:
    if current is not None:
        out.append(current)


def parse_latin_file(path: Path, root: Path, manuscript: str) -> List[Item]:
    out: List[Item] = []
    current: Optional[Item] = None
    marker_no = 0
    rel = str(path.relative_to(root))
    for source_line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if "¶" not in raw:
            if current is not None:
                toks = latin_line(raw)
                if toks:
                    current.lines.append(toks)
            continue

        parts = raw.split("¶")
        prefix = parts[0]
        if current is not None:
            ptoks = latin_line(prefix)
            if ptoks:
                current.lines.append(ptoks)

        for segment in parts[1:]:
            close_item(current, out)
            marker_no += 1
            current = Item(
                item_id=f"{rel}:{source_line_no}:pilcrow{marker_no}",
                document=manuscript,
                lines=[latin_line(segment)],
                leaf=None,
            )
    close_item(current, out)
    return out


def parse_latin_manuscript(root: Path, manuscript: str, rel_dir: str) -> List[Item]:
    d = root / rel_dir
    if not d.is_dir():
        raise RuntimeError(f"missing manuscript directory: {d}")
    out: List[Item] = []
    for p in sorted(d.rglob("*.txt")):
        out.extend(parse_latin_file(p, root, manuscript))
    return out


def base_eligible(item: Item) -> bool:
    return len(item.lines) >= 3 and len(item.lines[0]) >= 5 and len(item.lines[2]) >= 5


def valid_pseudo_indices(item: Item) -> List[int]:
    return [
        j
        for j in range(1, len(item.lines) - 2)
        if len(item.lines[j]) >= 5 and len(item.lines[j + 2]) >= 5
    ]


def s1_eligible(item: Item) -> bool:
    return base_eligible(item) and bool(valid_pseudo_indices(item))


def edit1(a: Token, b: Token) -> bool:
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    i = j = differences = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            differences += 1
            j += 1
            if differences > 1:
                return False
    return True


def entropy(values: Sequence[Unit]) -> float:
    c = Counter(values)
    if not c:
        return 0.0
    total = sum(c.values())
    return -sum((n / total) * math.log2(n / total) for n in c.values())


def feature8(line: Line) -> np.ndarray:
    if len(line) < 5:
        raise ValueError("feature8 requires >=5 tokens")
    toks = line[:5]
    lens = np.array([len(t) for t in toks], dtype=float)
    flat = [u for t in toks for u in t]
    edit_frac = sum(
        any(edit1(a, b) for j, b in enumerate(toks) if j != i)
        for i, a in enumerate(toks)
    ) / 5.0
    return np.array(
        [
            len(set(toks)) / 5.0,
            float(lens.mean()),
            float(lens.std()),
            float(len(set(flat))),
            entropy(flat),
            entropy([t[0] for t in toks if t]),
            entropy([t[-1] for t in toks if t]),
            edit_frac,
        ],
        dtype=float,
    )


def training_sd(items: Sequence[Item]) -> np.ndarray:
    rows = [feature8(line) for it in items if base_eligible(it) for line in it.lines if len(line) >= 5]
    if not rows:
        raise RuntimeError("no eligible lines for feature scaling")
    sd = np.std(np.array(rows, dtype=float), axis=0)
    sd[sd == 0] = 1.0
    return sd


def item_contrast(item: Item, sd: np.ndarray) -> np.ndarray:
    real = (feature8(item.lines[2]) - feature8(item.lines[0])) / sd
    pseudos = [
        (feature8(item.lines[j + 2]) - feature8(item.lines[j])) / sd
        for j in valid_pseudo_indices(item)
    ]
    if not pseudos:
        raise ValueError("S1 item has no pseudo boundary")
    return real - np.mean(np.array(pseudos, dtype=float), axis=0)


def contrasts(items: Sequence[Item], sd: np.ndarray) -> np.ndarray:
    rows = [item_contrast(it, sd) for it in items if s1_eligible(it)]
    return np.array(rows, dtype=float) if rows else np.zeros((0, 8), dtype=float)


def s1_projection(items: Sequence[Item], sd: np.ndarray, direction: np.ndarray) -> Tuple[Optional[float], int, List[float]]:
    d = contrasts(items, sd)
    if len(d) == 0:
        return None, 0, [0.0] * 8
    mean_delta = np.mean(d, axis=0)
    return float(mean_delta @ direction), int(len(d)), [float(x) for x in mean_delta]


def eta2(x: np.ndarray, groups: np.ndarray) -> float:
    if len(x) == 0:
        return 0.0
    mu = float(np.mean(x))
    total = float(np.sum((x - mu) ** 2))
    if total == 0:
        return 0.0
    between = 0.0
    for g in sorted(set(groups.tolist())):
        mask = groups == g
        between += int(mask.sum()) * (float(np.mean(x[mask])) - mu) ** 2
    return between / total


def s3_line_position(items: Sequence[Item]) -> dict:
    rows: List[np.ndarray] = []
    groups: List[int] = []
    for it in items:
        if not base_eligible(it):
            continue
        for i, line in enumerate(it.lines):
            if len(line) >= 5:
                rows.append(feature8(line))
                groups.append(min(i, 3))
    if not rows:
        return {"mean_eta2": None, "max_eta2": None, "per_feature": [], "n_lines": 0, "group_counts": {}}
    X = np.array(rows, dtype=float)
    g = np.array(groups, dtype=int)
    vals = [eta2(X[:, j], g) for j in range(8)]
    return {
        "mean_eta2": float(np.mean(vals)),
        "max_eta2": float(np.max(vals)),
        "per_feature": [float(x) for x in vals],
        "n_lines": int(len(rows)),
        "group_counts": {str(k): int(np.sum(g == k)) for k in sorted(set(g.tolist()))},
    }


def build_neighbors(vocabulary: Iterable[Token]) -> Dict[Token, Set[Token]]:
    vocab = set(vocabulary)
    neigh: Dict[Token, Set[Token]] = {w: set() for w in vocab}

    substitution_groups: Dict[Tuple[int, int, Token, Token], List[Token]] = defaultdict(list)
    for w in vocab:
        for i in range(len(w)):
            substitution_groups[(len(w), i, w[:i], w[i + 1:])].append(w)
    for group in substitution_groups.values():
        if len(group) > 1:
            for w in group:
                neigh[w].update(x for x in group if x != w)

    for longer in vocab:
        if not longer:
            continue
        for i in range(len(longer)):
            shorter = longer[:i] + longer[i + 1:]
            if shorter in vocab and shorter != longer:
                neigh[longer].add(shorter)
                neigh[shorter].add(longer)
    return neigh


def included_lines(items: Sequence[Item]) -> List[Line]:
    return [line for it in items if base_eligible(it) for line in it.lines if line]


def local_prev10(lines: Sequence[Line], neighbors: Dict[Token, Set[Token]]) -> float:
    hit = 0
    n = 0
    for line in lines:
        for i, tok in enumerate(line):
            prev = line[max(0, i - 10):i]
            nb = neighbors.get(tok, set())
            hit += int(any(x in nb for x in prev))
            n += 1
    return hit / n if n else 0.0


def s2_locality(items: Sequence[Item], label: str, null_reps: int = NULL_REPS) -> dict:
    lines = included_lines(items)
    pooled = [t for line in lines for t in line]
    vocab = set(pooled)
    neighbors = build_neighbors(vocab)
    observed = local_prev10(lines, neighbors)
    counts = [len(line) for line in lines]
    nulls: List[float] = []
    base_seed = stable_seed(f"phase62b:S2:{label}")
    for r in range(null_reps):
        shuffled = list(pooled)
        random.Random(base_seed + r).shuffle(shuffled)
        made: List[Line] = []
        k = 0
        for c in counts:
            made.append(shuffled[k:k + c])
            k += c
        nulls.append(local_prev10(made, neighbors))
    med = float(statistics.median(nulls)) if nulls else 0.0
    q025 = float(np.quantile(np.array(nulls), 0.025)) if nulls else 0.0
    q975 = float(np.quantile(np.array(nulls), 0.975)) if nulls else 0.0
    return {
        "observed": float(observed),
        "null_median": med,
        "null_q025": q025,
        "null_q975": q975,
        "excess": float(observed - med),
        "n_lines": len(lines),
        "n_tokens": len(pooled),
        "n_types": len(vocab),
        "null_reps": null_reps,
    }


def physical_leaf_folds(items: Sequence[Item]) -> List[Set[int]]:
    leaves = sorted({it.leaf for it in items if it.leaf is not None and base_eligible(it)})
    return [set(leaves[i::5]) for i in range(5)]


def by_leaves(items: Sequence[Item], leaves: Set[int], include: bool) -> List[Item]:
    return [it for it in items if it.leaf is not None and ((it.leaf in leaves) == include)]


def mean_optional(values: Sequence[Optional[float]]) -> Optional[float]:
    vv = [x for x in values if x is not None]
    return float(np.mean(vv)) if vv else None


def ratio(model: Optional[float], target: Optional[float]) -> Optional[float]:
    if model is None or target is None or target <= STABLE_EPS:
        return None
    return model / target


def relative_error(model: Optional[float], target: Optional[float]) -> Optional[float]:
    if model is None or target is None:
        return None
    return abs(model - target) / max(abs(target), STABLE_EPS)


def manuscript_static_metrics(items: Sequence[Item], label: str) -> dict:
    s2 = s2_locality(items, label)
    s3 = s3_line_position(items)
    return {
        "counts": {
            "items_total": len(items),
            "base_eligible": sum(base_eligible(x) for x in items),
            "s1_eligible": sum(s1_eligible(x) for x in items),
        },
        "S2": s2,
        "S3": s3,
    }


def aggregate_manuscripts(ms: Dict[str, dict]) -> dict:
    s1 = mean_optional([v["S1"]["projection"] for v in ms.values()])
    s2 = mean_optional([v["S2"]["excess"] for v in ms.values()])
    s3 = mean_optional([v["S3"]["mean_eta2"] for v in ms.values()])
    return {"S1": s1, "S2": s2, "S3": s3}


def verify_cremma_commit(root: Path) -> str:
    try:
        got = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    except Exception as exc:
        raise RuntimeError(f"cannot verify CREMMA git commit: {exc}")
    if got != EXPECTED_CREMMA_COMMIT:
        raise RuntimeError(f"CREMMA commit mismatch: {got} != {EXPECTED_CREMMA_COMMIT}")
    return got


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt /path/to/CREMMA-Medieval-LAT", file=sys.stderr)
        return 2

    voynich_path = Path(sys.argv[1]).resolve()
    cremma_root = Path(sys.argv[2]).resolve()
    vdata = voynich_path.read_bytes()
    vblob = git_blob_sha1(vdata)
    if vblob != EXPECTED_ZL3B_BLOB:
        raise RuntimeError(f"ZL3b blob mismatch: {vblob} != {EXPECTED_ZL3B_BLOB}")
    ccommit = verify_cremma_commit(cremma_root)

    vitems = parse_voynich(voynich_path)
    folds = physical_leaf_folds(vitems)

    primary_items = {
        name: parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in PRIMARY_MANUSCRIPTS.items()
    }
    sensitivity_items = {
        name: parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in SENSITIVITY_MANUSCRIPTS.items()
    }

    primary_static = {
        name: manuscript_static_metrics(items, f"N0:{name}")
        for name, items in primary_items.items()
    }
    sensitivity_static = {
        name: manuscript_static_metrics(items, f"SENS:{name}")
        for name, items in sensitivity_items.items()
    }

    fold_results = []
    for fi, test_leaves in enumerate(folds):
        train = by_leaves(vitems, test_leaves, include=False)
        test = by_leaves(vitems, test_leaves, include=True)
        sd = training_sd(train)
        dtrain = contrasts(train, sd)
        if len(dtrain) == 0:
            raise RuntimeError(f"fold {fi}: no S1 training contrasts")
        direction = np.mean(dtrain, axis=0)
        dn = float(np.linalg.norm(direction))
        if dn == 0:
            raise RuntimeError(f"fold {fi}: zero S1 direction")
        direction /= dn

        v_s1, v_n_s1, v_delta = s1_projection(test, sd, direction)
        v_s2 = s2_locality(test, f"Voynich:fold{fi}")
        v_s3 = s3_line_position(test)
        target = {"S1": v_s1, "S2": v_s2["excess"], "S3": v_s3["mean_eta2"]}

        manuscript_results = {}
        for name, items in primary_items.items():
            p, n_s1, delta = s1_projection(items, sd, direction)
            manuscript_results[name] = {
                "S1": {"projection": p, "n_items": n_s1, "mean_delta8": delta},
                "S2": primary_static[name]["S2"],
                "S3": primary_static[name]["S3"],
                "counts": primary_static[name]["counts"],
            }

        agg = aggregate_manuscripts(manuscript_results)
        fold_ratio = {k: ratio(agg[k], target[k]) for k in ("S1", "S2", "S3")}
        fold_error = {k: relative_error(agg[k], target[k]) for k in ("S1", "S2", "S3")}

        lomo = {}
        names = sorted(manuscript_results)
        for omitted in names:
            kept = {k: v for k, v in manuscript_results.items() if k != omitted}
            aa = aggregate_manuscripts(kept)
            lomo[omitted] = {
                "aggregate": aa,
                "ratio_to_voynich": {k: ratio(aa[k], target[k]) for k in ("S1", "S2", "S3")},
                "relative_error": {k: relative_error(aa[k], target[k]) for k in ("S1", "S2", "S3")},
            }

        sens = {}
        for name, items in sensitivity_items.items():
            p, n_s1, delta = s1_projection(items, sd, direction)
            vals = {
                "S1": p,
                "S2": sensitivity_static[name]["S2"]["excess"],
                "S3": sensitivity_static[name]["S3"]["mean_eta2"],
            }
            sens[name] = {
                "counts": sensitivity_static[name]["counts"],
                "metrics": vals,
                "ratio_to_voynich": {k: ratio(vals[k], target[k]) for k in vals},
                "S1_n_items": n_s1,
                "S1_mean_delta8": delta,
            }

        fold_results.append(
            {
                "fold": fi,
                "test_leaves": sorted(test_leaves),
                "voynich": {
                    "counts": {
                        "items_total": len(test),
                        "base_eligible": sum(base_eligible(x) for x in test),
                        "s1_eligible": v_n_s1,
                    },
                    "S1": {"projection": v_s1, "mean_delta8": v_delta},
                    "S2": v_s2,
                    "S3": v_s3,
                },
                "N0_manuscripts": manuscript_results,
                "N0_equal_manuscript_aggregate": agg,
                "N0_ratio_to_voynich": fold_ratio,
                "N0_relative_error": fold_error,
                "leave_one_manuscript_out": lomo,
                "sensitivities": sens,
            }
        )

    keys = ("S1", "S2", "S3")
    target_means = {
        "S1": float(np.mean([f["voynich"]["S1"]["projection"] for f in fold_results])),
        "S2": float(np.mean([f["voynich"]["S2"]["excess"] for f in fold_results])),
        "S3": float(np.mean([f["voynich"]["S3"]["mean_eta2"] for f in fold_results])),
    }
    n0_means = {k: float(np.mean([f["N0_equal_manuscript_aggregate"][k] for f in fold_results])) for k in keys}
    ratios_of_means = {k: ratio(n0_means[k], target_means[k]) for k in keys}
    mean_fold_ratios = {
        k: mean_optional([f["N0_ratio_to_voynich"][k] for f in fold_results])
        for k in keys
    }
    mean_fold_errors = {
        k: mean_optional([f["N0_relative_error"][k] for f in fold_results])
        for k in keys
    }

    per_manuscript = {}
    for name in PRIMARY_MANUSCRIPTS:
        per_manuscript[name] = {
            "S1_mean_across_voynich_folds": mean_optional([f["N0_manuscripts"][name]["S1"]["projection"] for f in fold_results]),
            "S2": primary_static[name]["S2"]["excess"],
            "S3": primary_static[name]["S3"]["mean_eta2"],
            "counts": primary_static[name]["counts"],
            "S2_detail": primary_static[name]["S2"],
            "S3_detail": primary_static[name]["S3"],
        }

    lomo_summary = {}
    for omitted in PRIMARY_MANUSCRIPTS:
        lomo_summary[omitted] = {
            "aggregate_mean": {
                k: float(np.mean([f["leave_one_manuscript_out"][omitted]["aggregate"][k] for f in fold_results]))
                for k in keys
            },
            "ratio_of_means_to_voynich": {},
        }
        for k in keys:
            m = lomo_summary[omitted]["aggregate_mean"][k]
            lomo_summary[omitted]["ratio_of_means_to_voynich"][k] = ratio(m, target_means[k])

    gate = {
        k: (ratios_of_means[k] is not None and 0.5 <= ratios_of_means[k] <= 2.0)
        for k in keys
    }
    materially_competitive = all(gate.values())

    out = {
        "phase": "62B",
        "family": "N0 source-native structured medieval plaintext",
        "scope_firewall": "N0 only; C0/A1/H62-P1 not evaluated",
        "inputs": {
            "voynich_bytes": len(vdata),
            "voynich_git_blob_sha1": vblob,
            "cremma_commit": ccommit,
            "primary_manuscripts": PRIMARY_MANUSCRIPTS,
            "sensitivity_manuscripts": SENSITIVITY_MANUSCRIPTS,
        },
        "implementation": {
            "fixed_line_tokens_for_S1_S3": 5,
            "feature_dimension": 8,
            "S2_null_reps": NULL_REPS,
            "outer_folds": 5,
        },
        "source_counts": {
            "voynich": {
                "items_total": len(vitems),
                "base_eligible": sum(base_eligible(x) for x in vitems),
                "s1_eligible": sum(s1_eligible(x) for x in vitems),
            },
            "primary": {name: primary_static[name]["counts"] for name in PRIMARY_MANUSCRIPTS},
            "sensitivities": {name: sensitivity_static[name]["counts"] for name in SENSITIVITY_MANUSCRIPTS},
        },
        "folds": fold_results,
        "across_fold": {
            "voynich_mean": target_means,
            "N0_equal_manuscript_mean": n0_means,
            "N0_ratio_of_means_to_voynich": ratios_of_means,
            "N0_mean_fold_ratio": mean_fold_ratios,
            "N0_mean_fold_relative_error": mean_fold_errors,
            "broad_regime_gate_0.5_to_2.0": gate,
            "materially_competitive_under_frozen_rule": materially_competitive,
        },
        "per_manuscript": per_manuscript,
        "leave_one_manuscript_out_summary": lomo_summary,
        "decision": (
            "N0 is materially competitive on the frozen exposed S1-S3 gate; proceed to already-frozen Phase62C without altering C0/A1/H62-P1."
            if materially_competitive
            else "N0 does not satisfy the frozen broad-regime gate on all S1-S3 targets; record which dimensions fail and proceed to already-frozen Phase62C without altering C0/A1/H62-P1."
        ),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
