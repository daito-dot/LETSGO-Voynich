#!/usr/bin/env python3
"""Phase63B0 source audit.

This script intentionally computes no scientific replication metric. It records
source identity, IVTFF coverage/paragraph metadata, syntax usage, and overlap
needed to freeze the Phase63B replication inputs.

Usage:
  python experiments/phase63/phase63b0_source_audit.py ZL3b-n.txt GC2a-n.txt IT2a-n.txt
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


LOCUS_RE = re.compile(r"^<([^>.]+)\.(\d+),([^>;]+)(?:;[^>]+)?>\s*(.*)$")
PAGE_RE = re.compile(r"^<([^>.]+)>\s*(?:<!.*>)?\s*$")
HIGH_RE = re.compile(r"@([0-9]{3});")
INLINE_RE = re.compile(r"<[^>]*>")
LEAF_RE = re.compile(r"^f(\d+)", re.I)

RESERVED = set("<>.,{}[:]?@;/")


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_phase62_module():
    root = Path(__file__).resolve().parents[1] / "phase62" / "phase62b_n0.py"
    spec = importlib.util.spec_from_file_location("phase62b_n0_for_source_audit", root)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase62 fold authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def physical_leaf(page: str) -> Optional[int]:
    m = LEAF_RE.match(page)
    return int(m.group(1)) if m else None


def locus_generic(code: str) -> Optional[str]:
    # IVTFF code is locator + two-character locus type, e.g. @P0 / +P0 / =Pt.
    # Be conservative if malformed.
    return code[1] if len(code) >= 2 else None


def strip_high_ascii(body: str) -> Tuple[str, int, Set[str]]:
    codes: Set[str] = set()
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        codes.add(m.group(0))
        return ""

    return HIGH_RE.sub(repl, body), count, codes


def source_record(path: Path, label: str, expected_alphabet: str) -> dict:
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    lines = text.splitlines()
    if not lines:
        raise RuntimeError(f"{label}: empty file")
    header = lines[0].strip()
    if not header.startswith(f"#=IVTFF {expected_alphabet} "):
        raise RuntimeError(f"{label}: unexpected header {header!r}")

    pages: Set[str] = set()
    p_pages: Set[str] = set()
    p_leaves: Set[int] = set()
    p_loci: Set[str] = set()
    paragraph_start_loci: Set[str] = set()
    paragraph_end_loci: Set[str] = set()
    locator_counts: Counter[str] = Counter()
    locus_type_counts: Counter[str] = Counter()
    alphabet_chars: Counter[str] = Counter()
    high_codes: Set[str] = set()

    counts = Counter()

    for line in lines:
        pm = PAGE_RE.match(line)
        if pm and "." not in pm.group(1):
            pages.add(pm.group(1))

        lm = LOCUS_RE.match(line)
        if not lm:
            continue
        page, num, code, body = lm.groups()
        if len(code) >= 1:
            locator_counts[code[0]] += 1
        if len(code) >= 3:
            locus_type_counts[code[1:3]] += 1
        if locus_generic(code) != "P":
            continue

        locus_id = f"{page}.{int(num)}"
        counts["P_loci"] += 1
        p_loci.add(locus_id)
        p_pages.add(page)
        leaf = physical_leaf(page)
        if leaf is not None:
            p_leaves.add(leaf)

        starts = body.count("<%>")
        ends = body.count("<$>")
        counts["paragraph_starts"] += starts
        counts["paragraph_ends"] += ends
        if starts:
            paragraph_start_loci.add(locus_id)
        if ends:
            paragraph_end_loci.add(locus_id)

        counts["drawing_interruptions_dash"] += body.count("<->")
        counts["drawing_interruptions_tilde"] += body.count("<~>")
        counts["uncertain_reading_open"] += body.count("[")
        counts["ligature_open"] += body.count("{")
        counts["unreadable_question_marks"] += body.count("?")

        # Count word-space markers only outside inline comments/tags. Paragraph and
        # drawing tags are removed first; definite/uncertain spaces remain.
        body_no_inline = INLINE_RE.sub("", body)
        counts["definite_period_spaces"] += body_no_inline.count(".")
        counts["uncertain_comma_spaces"] += body_no_inline.count(",")

        body_no_high, high_n, codes = strip_high_ascii(body_no_inline)
        counts["high_ascii_occurrences"] += high_n
        high_codes.update(codes)

        # This is only a syntax inventory, not scientific tokenization. Remove
        # current IVTFF reserved syntax; everything else is reported verbatim so
        # v101 digits/punctuation/case are not silently lost.
        for ch in body_no_high:
            if ch.isspace() or ch in RESERVED:
                continue
            alphabet_chars[ch] += 1

    return {
        "label": label,
        "path_name": path.name,
        "byte_size": len(data),
        "sha256": sha256(data),
        "git_blob_sha1": git_blob_sha1(data),
        "header_lines": lines[:3],
        "line_count": len(lines),
        "ivttf_header": header,
        "page_headers": len(pages),
        "P_pages": len(p_pages),
        "P_physical_leaves": len(p_leaves),
        "P_physical_leaf_numbers": sorted(p_leaves),
        **dict(sorted(counts.items())),
        "P_locus_ids": sorted(p_loci),
        "paragraph_start_locus_ids": sorted(paragraph_start_loci),
        "paragraph_end_locus_ids": sorted(paragraph_end_loci),
        "locator_counts_all_loci": dict(sorted(locator_counts.items())),
        "locus_type_counts_all_loci": dict(sorted(locus_type_counts.items())),
        "high_ascii_codes_in_P_text": sorted(high_codes),
        "raw_nonreserved_character_inventory_in_P_text": sorted(alphabet_chars),
        "raw_nonreserved_character_counts_in_P_text": dict(sorted(alphabet_chars.items())),
    }


def pairwise_set_stats(a: Set[str], b: Set[str]) -> dict:
    inter = a & b
    union = a | b
    return {
        "a_count": len(a),
        "b_count": len(b),
        "intersection": len(inter),
        "union": len(union),
        "jaccard": float(len(inter) / len(union)) if union else 1.0,
    }


def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt GC2a-n.txt IT2a-n.txt", file=sys.stderr)
        return 2

    paths = {
        "ZL3b": (Path(sys.argv[1]).resolve(), "Eva-"),
        "GC2a": (Path(sys.argv[2]).resolve(), "v101"),
        "IT2a": (Path(sys.argv[3]).resolve(), "EvaT"),
    }
    records = {
        label: source_record(path, label, alphabet)
        for label, (path, alphabet) in paths.items()
    }

    # Confirm pinned ZL identity before using its Phase62 fold authority.
    phase62 = load_phase62_module()
    if records["ZL3b"]["git_blob_sha1"] != phase62.EXPECTED_ZL3B_BLOB:
        raise RuntimeError(
            f"ZL blob mismatch: {records['ZL3b']['git_blob_sha1']} != {phase62.EXPECTED_ZL3B_BLOB}"
        )
    zitems = phase62.parse_voynich(paths["ZL3b"][0])
    original_folds = phase62.physical_leaf_folds(zitems)

    p_loci = {k: set(v["P_locus_ids"]) for k, v in records.items()}
    pstarts = {k: set(v["paragraph_start_locus_ids"]) for k, v in records.items()}
    leaves = {k: set(v["P_physical_leaf_numbers"]) for k, v in records.items()}
    common_leaves = set.intersection(*leaves.values())

    pairwise = {}
    names = list(records)
    for i, a in enumerate(names):
        for bname in names[i + 1:]:
            pairwise[f"{a}__{bname}"] = {
                "P_locus_overlap": pairwise_set_stats(p_loci[a], p_loci[bname]),
                "paragraph_start_locus_overlap": pairwise_set_stats(pstarts[a], pstarts[bname]),
                "P_physical_leaf_overlap": pairwise_set_stats(
                    {str(x) for x in leaves[a]}, {str(x) for x in leaves[bname]}
                ),
            }

    restricted_folds = {
        str(fi): sorted(set(fold) & common_leaves)
        for fi, fold in enumerate(original_folds)
    }

    out = {
        "phase": "63B0",
        "scope": "source identity/coverage/syntax audit only; no scientific replication metric",
        "canonical_urls": {
            "GC2a": "https://www.voynich.nu/data/GC2a-n.txt",
            "IT2a": "https://www.voynich.nu/data/IT2a-n.txt",
            "ZL3b_mirror_repository": "matthewdgreen/cipher_benchmark",
            "ZL3b_mirror_commit": "315f0cad4de3d021bd4185765c037cf2a28d341c",
            "ZL3b_mirror_path": "benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt",
        },
        "sources": records,
        "pairwise": pairwise,
        "common_P_physical_leaves_all_three": sorted(common_leaves),
        "common_P_physical_leaf_count_all_three": len(common_leaves),
        "phase62_original_folds": {str(i): sorted(f) for i, f in enumerate(original_folds)},
        "phase63B_restricted_folds_by_preregistered_rule": restricted_folds,
        "phase63B_restricted_fold_sizes": {k: len(v) for k, v in restricted_folds.items()},
        "scientific_metrics_computed": False,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
