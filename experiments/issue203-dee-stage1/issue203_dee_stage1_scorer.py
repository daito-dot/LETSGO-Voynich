#!/usr/bin/env python3
"""Frozen Dee source-attribution scorer for Issue #203.

Scientific contract: GitHub Issue #203 plus the committed preregistration file.
No Voynich data are read by this program.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ALPHA = 0.01
EXPECTED_XLSX_SHA256 = "c339aeac63da1b81560e63b02abb807a187a4003d3df44ebf389d3934055605d"
EXPECTED_CIPHER_SHA256 = "3e0aab0f59160896fa8fdf088c7ee15af2c9bad1eced404f8ed7b6d020a56446"
EXPECTED_PLAIN_SHA256 = "21458f41a44a4ec45938f84bd6c341b0e695bb9f8b2c6fb3afee14bea61d4c27"
EXPECTED_LEDGER_SHA256 = "362bcd4a4edbbc5e93559b11a2e495ee71e897bdb97b28f1802b8a9df647edd5"
PAGE_BREAK = (18, 19)
PRIMARY_SAME_EXPECTED = 147
PRIMARY_CROSS_BEFORE_PAGE_EXPECTED = 26
PRIMARY_CROSS_AFTER_PAGE_EXPECTED = 25


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def col_number(cell_ref: str) -> int:
    m = re.fullmatch(r"([A-Z]+)([0-9]+)", cell_ref)
    if not m:
        raise RuntimeError(f"invalid XLSX cell ref: {cell_ref}")
    n = 0
    for ch in m.group(1):
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n


def row_number(cell_ref: str) -> int:
    m = re.fullmatch(r"([A-Z]+)([0-9]+)", cell_ref)
    if not m:
        raise RuntimeError(f"invalid XLSX cell ref: {cell_ref}")
    return int(m.group(2))


def read_xlsx_cached_cells(path: Path) -> dict[tuple[int, int], str]:
    """Read cached XLSX values using stdlib only; formulas are never evaluated."""
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            for si in root.findall("x:si", ns):
                text = "".join(t.text or "" for t in si.findall(".//x:t", ns))
                shared.append(text)
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    out: dict[tuple[int, int], str] = {}
    for c in sheet.findall(".//x:c", ns):
        ref = c.attrib.get("r")
        if not ref:
            continue
        v = c.find("x:v", ns)
        if v is None or v.text is None:
            continue
        raw = v.text
        typ = c.attrib.get("t")
        value = shared[int(raw)] if typ == "s" else raw
        out[(row_number(ref), col_number(ref))] = value
    return out


def extract_author_streams(path: Path) -> tuple[str, str]:
    if sha256_file(path) != EXPECTED_XLSX_SHA256:
        raise RuntimeError("dee.xlsx SHA-256 mismatch")
    cells = read_xlsx_cached_cells(path)

    def collect(c0: int, c1: int) -> str:
        vals: list[str] = []
        for r in range(15, 40):
            for c in range(c0, c1 + 1):
                v = cells.get((r, c), "")
                if not v:
                    continue
                if len(v) != 1 or not v.isalpha() or not v.isascii():
                    raise RuntimeError(f"unexpected cached stream cell r={r} c={c}: {v!r}")
                vals.append(v.lower())
        return "".join(vals)

    cipher = collect(3, 47)
    plain = collect(52, 96)
    if len(cipher) != 1099 or len(plain) != 1099:
        raise RuntimeError(f"unexpected stream lengths: cipher={len(cipher)} plain={len(plain)}")
    if sha256_bytes(cipher.encode()) != EXPECTED_CIPHER_SHA256:
        raise RuntimeError("author-sheet cipher stream SHA-256 mismatch")
    if sha256_bytes(plain.encode()) != EXPECTED_PLAIN_SHA256:
        raise RuntimeError("author-sheet plaintext stream SHA-256 mismatch")
    return cipher, plain


def load_gate0(ledger_path: Path, gate0_json_path: Path) -> tuple[list[dict], dict]:
    if sha256_file(ledger_path) != EXPECTED_LEDGER_SHA256:
        raise RuntimeError("Gate-0 event ledger SHA-256 mismatch")
    gate = json.loads(gate0_json_path.read_text(encoding="utf-8"))
    frozen_hash = gate["derived_capture_hashes"]["event_ledger_sha256"]
    if frozen_hash != EXPECTED_LEDGER_SHA256:
        raise RuntimeError("Gate-0 JSON ledger hash mismatch")
    rows = []
    with ledger_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            row["boundary_after_group"] = int(row["boundary_after_group"])
            row["left_line"] = int(row["left_line"])
            row["right_line"] = int(row["right_line"])
            row["sheet_offset"] = int(row["sheet_offset"]) if row["sheet_offset"] else None
            rows.append(row)
    if len(rows) != 188:
        raise RuntimeError(f"expected 188 Gate-0 boundaries, got {len(rows)}")
    return rows, gate


def is_page_break(e: dict) -> bool:
    return (e["left_line"], e["right_line"]) == PAGE_BREAK


def fold_of(e: dict) -> int:
    return (e["right_line"] - 1) % 5


def primary_events(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    lexical = [e for e in rows if e["boundary_class"] == "LEXICAL_BOUNDARY"]
    same = [e for e in lexical if e["physical_relation"] == "SAME_PHYSICAL_LINE"]
    cross_before = [e for e in lexical if e["physical_relation"] == "CROSS_PHYSICAL_LINE"]
    cross = [e for e in cross_before if not is_page_break(e)]
    if len(same) != PRIMARY_SAME_EXPECTED:
        raise RuntimeError(f"primary same-line count mismatch: {len(same)}")
    if len(cross_before) != PRIMARY_CROSS_BEFORE_PAGE_EXPECTED:
        raise RuntimeError(f"primary pre-page cross-line count mismatch: {len(cross_before)}")
    if len(cross) != PRIMARY_CROSS_AFTER_PAGE_EXPECTED:
        raise RuntimeError(f"primary post-page cross-line count mismatch: {len(cross)}")
    return same, cross


def all_aligned_events(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    allowed = {"LEXICAL_BOUNDARY", "WITHIN_WORD_SPLIT"}
    aligned = [e for e in rows if e["boundary_class"] in allowed]
    same = [e for e in aligned if e["physical_relation"] == "SAME_PHYSICAL_LINE"]
    cross = [e for e in aligned if e["physical_relation"] == "CROSS_PHYSICAL_LINE" and not is_page_break(e)]
    return same, cross


def event_pair(stream: str, e: dict) -> tuple[str, str]:
    k = e["sheet_offset"]
    if k is None or not (1 <= k < len(stream)):
        raise RuntimeError(f"invalid sheet offset for boundary {e['boundary_after_group']}: {k}")
    return stream[k - 1], stream[k]


def fit(pairs: list[tuple[str, str]]) -> tuple[Counter, dict[str, Counter], Counter]:
    base = Counter()
    cond: dict[str, Counter] = defaultdict(Counter)
    ctx = Counter()
    for x, y in pairs:
        base[y] += 1
        cond[x][y] += 1
        ctx[x] += 1
    return base, dict(cond), ctx


def log2_base(y: str, base: Counter, n: int, vocab_size: int) -> float:
    return math.log2((base[y] + ALPHA) / (n + ALPHA * vocab_size))


def log2_cond(y: str, x: str, cond: dict[str, Counter], ctx: Counter, vocab_size: int) -> float:
    row = cond.get(x)
    xy = row[y] if row is not None else 0
    nx = ctx[x]
    return math.log2((xy + ALPHA) / (nx + ALPHA * vocab_size))


def evaluate_population(stream: str, events: list[dict], vocab: list[str]) -> dict:
    folds = []
    for f in range(5):
        train_e = [e for e in events if fold_of(e) != f]
        test_e = [e for e in events if fold_of(e) == f]
        if not train_e or not test_e:
            raise RuntimeError(f"zero support in fold {f}: train={len(train_e)} test={len(test_e)}")
        train = [event_pair(stream, e) for e in train_e]
        test = [event_pair(stream, e) for e in test_e]
        base, cond, ctx = fit(train)
        n = len(train)
        gains = []
        pos_bits = []
        edge_bits = []
        for x, y in test:
            lp0 = log2_base(y, base, n, len(vocab))
            lp1 = log2_cond(y, x, cond, ctx, len(vocab))
            gains.append(lp1 - lp0)
            pos_bits.append(-lp0)
            edge_bits.append(-lp1)
        folds.append({
            "fold": f,
            "train_event_count": len(train),
            "test_event_count": len(test),
            "test_boundary_ids": [e["boundary_after_group"] for e in test_e],
            "mean_pos_bits": sum(pos_bits) / len(pos_bits),
            "mean_edge_bits": sum(edge_bits) / len(edge_bits),
            "mean_gain_bits": sum(gains) / len(gains),
            "total_gain_bits": sum(gains),
        })
    vals = [x["mean_gain_bits"] for x in folds]
    passed = (sum(vals) / 5 > 0.0) and (sum(v > 0.0 for v in vals) >= 4)
    return {
        "event_count": len(events),
        "folds": folds,
        "fold_gain_bits": vals,
        "mean_fold_gain_bits": sum(vals) / 5,
        "positive_folds": sum(v > 0.0 for v in vals),
        "pass": passed,
    }


def stream_topology(line: dict, cross: dict) -> str:
    if line["pass"] and not cross["pass"]:
        return "LINE_LOCAL"
    if line["pass"] and cross["pass"]:
        return "EDGE_WITH_CROSS_LINE_CONTINUATION"
    if not line["pass"] and not cross["pass"]:
        return "NO_ROBUST_LINE_EDGE"
    return "CROSS_ONLY_OR_UNSTABLE"


def joint_class(plain_topology: str, cipher_topology: str) -> str:
    p = plain_topology == "LINE_LOCAL"
    c = cipher_topology == "LINE_LOCAL"
    if p and c:
        return "LINE_LOCAL_PRESENT_BEFORE_AND_AFTER_CIPHER"
    if c and not p:
        return "CIPHER_STREAM_ONLY_LINE_LOCAL"
    if p and not c:
        return "PLAINTEXT_ONLY_LINE_LOCAL"
    return "NO_SHARED_LINE_LOCAL_TOPOLOGY"


def paired_shift(cipher: dict, plain: dict) -> dict:
    vals = [c - p for c, p in zip(cipher["fold_gain_bits"], plain["fold_gain_bits"])]
    return {
        "fold_delta_bits": vals,
        "mean_fold_delta_bits": sum(vals) / 5,
        "positive_folds": sum(v > 0.0 for v in vals),
        "gating": False,
    }


def score_stream(stream: str, same: list[dict], cross: list[dict]) -> dict:
    vocab = sorted(set(stream))
    line = evaluate_population(stream, same, vocab)
    cross_r = evaluate_population(stream, cross, vocab)
    return {
        "vocabulary": vocab,
        "vocabulary_size": len(vocab),
        "G_line": line,
        "G_cross": cross_r,
        "topology": stream_topology(line, cross_r),
    }


def analyze(xlsx: Path, ledger_path: Path, gate0_json_path: Path) -> dict:
    cipher, plain = extract_author_streams(xlsx)
    rows, gate0 = load_gate0(ledger_path, gate0_json_path)
    same, cross = primary_events(rows)
    all_same, all_cross = all_aligned_events(rows)

    event_fold_map = {
        str(e["boundary_after_group"]): fold_of(e)
        for e in same + cross
    }
    if len(event_fold_map) != len(same) + len(cross):
        raise RuntimeError("duplicate primary boundary IDs")
    for f in range(5):
        if not any(fold_of(e) == f for e in same):
            raise RuntimeError(f"no primary same-line test events in fold {f}")
        if not any(fold_of(e) == f for e in cross):
            raise RuntimeError(f"no primary cross-line test events in fold {f}")

    plain_primary = score_stream(plain, same, cross)
    cipher_primary = score_stream(cipher, same, cross)
    plain_all = score_stream(plain, all_same, all_cross)
    cipher_all = score_stream(cipher, all_same, all_cross)

    within = [e for e in rows if e["boundary_class"] == "WITHIN_WORD_SPLIT"]
    return {
        "experiment": "Issue #203 Dee plaintext-to-cipher R5 source attribution",
        "external_only": True,
        "voynich_accessed": False,
        "alpha": ALPHA,
        "authorities": {
            "dee_xlsx_sha256": EXPECTED_XLSX_SHA256,
            "cipher_stream_sha256": EXPECTED_CIPHER_SHA256,
            "plain_stream_sha256": EXPECTED_PLAIN_SHA256,
            "gate0_event_ledger_sha256": EXPECTED_LEDGER_SHA256,
            "gate0_class": gate0["gate0_class"],
        },
        "fold_rule": "(right_physical_line - 1) mod 5",
        "page_carry_exclusion": {"left_line": 18, "right_line": 19},
        "primary_population": {
            "same_line_lexical_events": len(same),
            "cross_line_lexical_events_after_page_exclusion": len(cross),
            "event_fold_map": event_fold_map,
        },
        "primary": {
            "plaintext": plain_primary,
            "ciphertext": cipher_primary,
            "joint_classification": joint_class(plain_primary["topology"], cipher_primary["topology"]),
        },
        "secondary_non_gating": {
            "paired_transform_shift": {
                "D_line": paired_shift(cipher_primary["G_line"], plain_primary["G_line"]),
                "D_cross": paired_shift(cipher_primary["G_cross"], plain_primary["G_cross"]),
            },
            "all_aligned_boundaries": {
                "same_event_count": len(all_same),
                "cross_event_count_after_page_exclusion": len(all_cross),
                "plaintext": plain_all,
                "ciphertext": cipher_all,
            },
            "within_word_split": {
                "count": len(within),
                "same_line_count": sum(e["physical_relation"] == "SAME_PHYSICAL_LINE" for e in within),
                "cross_line_count": sum(e["physical_relation"] == "CROSS_PHYSICAL_LINE" for e in within),
                "cross_line_left_lines": [e["left_line"] for e in within if e["physical_relation"] == "CROSS_PHYSICAL_LINE"],
                "predictive_score_licensed": False,
            },
        },
    }


def synthetic_preflight() -> None:
    same_pairs = []
    cross_pairs = []
    for f in range(5):
        for j in range(20):
            x = "a" if j % 2 == 0 else "c"
            y = "b" if x == "a" else "d"
            same_pairs.append((f, x, y))
        for j in range(10):
            x = "a" if j % 2 == 0 else "c"
            y = "b" if (j + f) % 2 == 0 else "d"
            cross_pairs.append((f, x, y))

    def eval_pairs(data: list[tuple[int, str, str]]) -> dict:
        vocab = ["a", "b", "c", "d"]
        vals = []
        for f in range(5):
            train = [(x, y) for ff, x, y in data if ff != f]
            test = [(x, y) for ff, x, y in data if ff == f]
            base, cond, ctx = fit(train)
            n = len(train)
            gains = [
                log2_cond(y, x, cond, ctx, len(vocab)) - log2_base(y, base, n, len(vocab))
                for x, y in test
            ]
            vals.append(sum(gains) / len(gains))
        return {"folds": vals, "pass": (sum(vals) / 5 > 0 and sum(v > 0 for v in vals) >= 4)}

    same = eval_pairs(same_pairs)
    cross = eval_pairs(cross_pairs)
    if not same["pass"]:
        raise RuntimeError("synthetic same-line edge was not recovered")
    if len(cross["folds"]) != 5:
        raise RuntimeError("synthetic cross-line fold path failed")
    print("ISSUE203_SYNTHETIC_PREFLIGHT_OK")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", type=Path)
    ap.add_argument("--ledger", type=Path)
    ap.add_argument("--gate0-json", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--synthetic-preflight", action="store_true")
    args = ap.parse_args()
    if args.synthetic_preflight:
        synthetic_preflight()
        return
    if not all([args.xlsx, args.ledger, args.gate0_json]):
        ap.error("--xlsx, --ledger and --gate0-json are required")
    result = analyze(args.xlsx, args.ledger, args.gate0_json)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
