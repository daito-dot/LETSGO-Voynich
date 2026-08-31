#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
LP = re.compile(r"^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<c>[^>]*)>\s+(?P<b>.*)$")
AIN_I_RUN = re.compile(r"a[i]+n")

PREFIX_ORDER = ["che", "o", "qo", "sho", "cho", "ch"]
PUBLISHED_MAP = {"che": 4, "o": 1, "qo": 3, "sho": 5, "cho": 2, "ch": 0}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_tokens(body: str) -> List[str]:
    body = body.replace("<%>", " ")
    body = re.sub(r"<[^>]*>", " ", body)
    out: List[str] = []
    for x in re.split(r"[.\s]+", body):
        t = re.sub(r"[^A-Za-z]", "", x).lower()
        if t:
            out.append(t)
    return out


def records_for_page(lines: Sequence[str], page: str) -> List[Tuple[int, str, str]]:
    out: List[Tuple[int, str, str]] = []
    for line in lines:
        m = LP.match(line)
        if not m:
            continue
        loc = m.group("loc")
        if not loc.startswith(page + "."):
            continue
        n = int(loc.rsplit(".", 1)[1])
        out.append((n, m.group("c"), m.group("b")))
    out.sort()
    return out


def parse_f67_sectors(lines: Sequence[str]) -> List[List[str]]:
    recs = records_for_page(lines, "f67r2")
    sectors: List[List[str]] = []
    current: List[str] | None = None
    for _, code, body in recs:
        if "Ls" in code and len(sectors) >= 12:
            break
        if "@Pb" in code:
            if current is not None:
                sectors.append(current)
            current = []
        if current is not None:
            current.extend(normalized_tokens(body))
    if current is not None and len(sectors) < 12:
        sectors.append(current)
    if len(sectors) != 12:
        raise RuntimeError(f"expected 12 f67r2 sectors, got {len(sectors)}")
    return sectors


def parse_f113_paragraphs(lines: Sequence[str]) -> List[List[str]]:
    recs = records_for_page(lines, "f113r")
    paragraphs: List[List[str]] = []
    current: List[str] | None = None
    for _, code, body in recs:
        if "P" not in code:
            continue
        start = "<%>" in body
        if start:
            if current is not None:
                paragraphs.append(current)
            current = []
        if current is not None:
            current.extend(normalized_tokens(body))
    if current is not None:
        paragraphs.append(current)
    if len(paragraphs) < 8:
        raise RuntimeError(f"expected >=8 f113r paragraphs, got {len(paragraphs)}")
    return paragraphs


def longest_common_contiguous(a: Sequence[str], b: Sequence[str]) -> int:
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    best = 0
    for x in a:
        cur = [0] * (len(b) + 1)
        for j, y in enumerate(b, start=1):
            if x == y:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


def lcs_length(a: Sequence[str], b: Sequence[str]) -> int:
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0] * (len(b) + 1)
        for j, y in enumerate(b, start=1):
            if x == y:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


def jaccard(a: Sequence[str], b: Sequence[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb) if sa | sb else 0.0


def d1_audit(sectors: Sequence[Sequence[str]]) -> dict:
    strict = [any("aiin" in t for t in sec) for sec in sectors]
    broad = [any(AIN_I_RUN.search(t) for t in sec) for sec in sectors]
    expected = [True, True, True, True, False, False, True]
    strict_agree = sum(a == b for a, b in zip(strict[:7], expected))
    broad_agree = sum(a == b for a, b in zip(broad[:7], expected))
    return {
        "expected_first7": expected,
        "strict_aiin_presence_12": strict,
        "strict_first7_agreement": strict_agree,
        "broad_a_i_run_n_presence_12": broad,
        "broad_first7_agreement": broad_agree,
        "pass": strict[:7] == expected,
    }


def circular_opposition_score(root: Sequence[bool], octave: Sequence[bool], shift: int = 0) -> int:
    n = len(root)
    return sum(
        1
        for i, r in enumerate(root)
        if r and octave[((i + n // 2) - shift) % n]
    )


def d2_audit(sectors: Sequence[Sequence[str]]) -> dict:
    roots = [any(t == "ain" for t in sec) for sec in sectors]
    octaves = [any(t.endswith("daiin") for t in sec) for sec in sectors]
    literal_12 = roots[2]
    literal_6 = octaves[8]
    observed = circular_opposition_score(roots, octaves, 0)
    null_scores = [circular_opposition_score(roots, octaves, shift) for shift in range(12)]
    p = sum(x >= observed for x in null_scores) / 12.0
    return {
        "root_exact_ain_presence_12": roots,
        "octave_suffix_daiin_presence_12": octaves,
        "literal_sector3_ain": literal_12,
        "literal_sector9_daiin_suffix": literal_6,
        "observed_opposition_hits": observed,
        "rotation_null_scores": null_scores,
        "exact_p_ge": p,
        "pass": bool(literal_12 and literal_6 and p <= 0.05),
    }


def pair_metrics(a: Sequence[str], b: Sequence[str]) -> dict:
    return {
        "len_a": len(a),
        "len_b": len(b),
        "longest_common_contiguous": longest_common_contiguous(a, b),
        "lcs_length": lcs_length(a, b),
        "token_set_jaccard": jaccard(a, b),
    }


def d3_audit(paragraphs: Sequence[Sequence[str]]) -> dict:
    p6, p7, p8 = list(paragraphs[5]), list(paragraphs[6]), list(paragraphs[7])
    p7_prefix = len(p7) <= len(p6) and p6[:len(p7)] == p7
    p8_suffix = len(p8) <= len(p6) and p6[-len(p8):] == p8 if p8 else False
    concat = p7 + p8 == p6
    return {
        "lengths": {"P6": len(p6), "P7": len(p7), "P8": len(p8)},
        "P7_is_prefix_of_P6": p7_prefix,
        "P8_is_suffix_of_P6": p8_suffix,
        "P7_plus_P8_equals_P6": concat,
        "P6_vs_P7": pair_metrics(p6, p7),
        "P6_vs_P8": pair_metrics(p6, p8),
        "P6_first10": p6[:10],
        "P7_first10": p7[:10],
        "P8_first10": p8[:10],
        "pass": concat,
    }


def classify_prefix(token: str) -> str | None:
    matches = [p for p in PREFIX_ORDER if token.startswith(p)]
    if not matches:
        return None
    return sorted(matches, key=lambda p: (-len(p), p))[0]


def prefix_classes(tokens: Iterable[str]) -> Tuple[List[str], int]:
    classes: List[str] = []
    total = 0
    for token in tokens:
        total += 1
        p = classify_prefix(token)
        if p is not None:
            classes.append(p)
    return classes, total


def intervals(values: Sequence[int]) -> List[int]:
    return [b - a for a, b in zip(values, values[1:])]


def dtw_distance(a: Sequence[int], b: Sequence[int]) -> float:
    if not a or not b:
        return math.inf
    m, n = len(a), len(b)
    inf = float("inf")
    cost = [[inf] * (n + 1) for _ in range(m + 1)]
    plen = [[0] * (n + 1) for _ in range(m + 1)]
    cost[0][0] = 0.0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            candidates = [
                (cost[i - 1][j], plen[i - 1][j]),
                (cost[i][j - 1], plen[i][j - 1]),
                (cost[i - 1][j - 1], plen[i - 1][j - 1]),
            ]
            best_cost, best_len = min(candidates, key=lambda x: (x[0], x[1]))
            cost[i][j] = best_cost + abs(a[i - 1] - b[j - 1])
            plen[i][j] = best_len + 1
    return cost[m][n] / plen[m][n]


def load_chant_intervals(path: Path) -> Tuple[List[int], List[str]]:
    groups = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    events: List[int] = []
    for group in groups:
        for ch in group:
            if not ("a" <= ch <= "z"):
                raise RuntimeError(f"unexpected chant pitch symbol: {ch!r}")
            events.append(ord(ch) - ord("e"))
    return intervals(events), groups


def sequence_for_mapping(classes: Sequence[str], mapping: Dict[str, int]) -> List[int]:
    return [mapping[c] for c in classes]


def d4_audit(paragraphs: Sequence[Sequence[str]], chant_intervals: Sequence[int]) -> dict:
    target_tokens = [t for p in paragraphs[:3] for t in p]
    target_classes, total = prefix_classes(target_tokens)
    published_values = sequence_for_mapping(target_classes, PUBLISHED_MAP)
    pub_intervals = intervals(published_values)
    pub_distance = dtw_distance(pub_intervals, chant_intervals)

    perm_rows: List[Tuple[float, Tuple[int, ...]]] = []
    for perm in itertools.permutations(range(6)):
        mapping = dict(zip(PREFIX_ORDER, perm))
        vals = sequence_for_mapping(target_classes, mapping)
        d = dtw_distance(intervals(vals), chant_intervals)
        perm_rows.append((d, perm))
    rank = 1 + sum(d < pub_distance - 1e-15 for d, _ in perm_rows)
    p_map = sum(d <= pub_distance + 1e-15 for d, _ in perm_rows) / len(perm_rows)

    windows: List[dict] = []
    for start in range(0, len(paragraphs) - 2):
        toks = [t for p in paragraphs[start:start + 3] for t in p]
        classes, ntotal = prefix_classes(toks)
        if len(classes) < 8:
            continue
        vals = sequence_for_mapping(classes, PUBLISHED_MAP)
        d = dtw_distance(intervals(vals), chant_intervals)
        windows.append({
            "start_paragraph": start + 1,
            "mapped_events": len(classes),
            "total_tokens": ntotal,
            "coverage": len(classes) / ntotal if ntotal else 0.0,
            "distance": d,
        })
    target_window = next(w for w in windows if w["start_paragraph"] == 1)
    p_window = sum(w["distance"] <= target_window["distance"] + 1e-15 for w in windows) / len(windows)
    window_rank = 1 + sum(w["distance"] < target_window["distance"] - 1e-15 for w in windows)

    passed = p_map <= 0.05 and p_window <= 0.05
    return {
        "published_prefix_map": PUBLISHED_MAP,
        "target_paragraphs": [1, 2, 3],
        "mapped_events": len(target_classes),
        "total_tokens": total,
        "mapping_coverage": len(target_classes) / total if total else 0.0,
        "published_dtw_interval_distance": pub_distance,
        "mapping_permutations": len(perm_rows),
        "published_mapping_rank": rank,
        "p_map": p_map,
        "eligible_three_paragraph_windows": len(windows),
        "target_window_rank": window_rank,
        "p_window": p_window,
        "window_rows": windows,
        "pass": passed,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/ZL3b-n.txt", file=sys.stderr)
        return 2
    vpath = Path(sys.argv[1]).resolve()
    data = vpath.read_bytes()
    if git_blob_sha1(data) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b blob mismatch")
    lines = data.decode("utf-8", errors="ignore").splitlines()

    here = Path(__file__).resolve().parent
    plan = here / "PLAN_D.md"
    chant_fixture = here / "VENI_CREATOR_STANZA1_PITCH_GROUPS.txt"

    sectors = parse_f67_sectors(lines)
    paragraphs = parse_f113_paragraphs(lines)
    chant_intervals, chant_groups = load_chant_intervals(chant_fixture)

    d1 = d1_audit(sectors)
    d2 = d2_audit(sectors)
    d3 = d3_audit(paragraphs)
    d4 = d4_audit(paragraphs, chant_intervals)
    passes = sum(bool(x["pass"]) for x in (d1, d2, d3, d4))
    if passes == 4:
        classification = "SUPPORTED"
    elif passes >= 2:
        classification = "PARTIAL"
    else:
        classification = "NOT SUPPORTED"

    result = {
        "experiment": "Issue26D public direct-music claim audit",
        "issue": 26,
        "inputs": {
            "voynich_git_blob_sha1": EXPECTED_ZL3B_BLOB,
            "plan_sha256": sha256_file(plan),
            "chant_fixture_sha256": sha256_file(chant_fixture),
            "script_sha256": sha256_file(Path(__file__)),
            "chant_pitch_groups": chant_groups,
        },
        "counts": {
            "f67r2_sectors": len(sectors),
            "f113r_paragraphs": len(paragraphs),
            "chant_interval_events": len(chant_intervals),
        },
        "D1_tetrachord_presence_claim": d1,
        "D2_ain_daiin_opposition": d2,
        "D3_word_for_word_respond": d3,
        "D4_veni_creator_mapping": d4,
        "passed_components": passes,
        "frozen_classification": classification,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
