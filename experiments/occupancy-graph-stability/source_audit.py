#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "issue26-music"))
import issue26e_core as e

EXPECTED_SOURCE_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_VISIBLE = 32570
EXPECTED_PARSED = 25071

PAGE_HEADER_RE = re.compile(r"^<(?P<page>[^>.]+)>\s+<!\s*(?P<vars>.*?)>")
VAR_RE = re.compile(r"\$([A-Z])=([^\s>]+)")
DATA_RE = re.compile(r"^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<code>[^>]*)>\s+(?P<body>.*)$")
TAG_RE = re.compile(r"\$([LI])=([^\s>]+)")
DIMENSIONS = ("L", "I", "H", "C")
MISSING = "__MISSING__"
POSITION_ORDER = ("singleton", "initial", "interior", "final")


def new_stats():
    return {
        "visible": 0,
        "parsed": 0,
        "leaves": set(),
        "folds": {f: {"visible": 0, "parsed": 0, "leaves": set()} for f in range(5)},
    }


def add(stats, fold, leaf, parsed):
    stats["visible"] += 1
    stats["parsed"] += int(parsed)
    stats["leaves"].add(int(leaf))
    z = stats["folds"][int(fold)]
    z["visible"] += 1
    z["parsed"] += int(parsed)
    z["leaves"].add(int(leaf))


def freeze_stats(stats):
    return {
        "visible_tokens": int(stats["visible"]),
        "parsed_tokens": int(stats["parsed"]),
        "parse_coverage": (stats["parsed"] / stats["visible"]) if stats["visible"] else 0.0,
        "unique_physical_leaves": len(stats["leaves"]),
        "folds": [
            {
                "fold": f,
                "visible_tokens": int(stats["folds"][f]["visible"]),
                "parsed_tokens": int(stats["folds"][f]["parsed"]),
                "unique_physical_leaves": len(stats["folds"][f]["leaves"]),
            }
            for f in range(5)
        ],
    }


def position_category(index, n):
    if n == 1:
        return "singleton"
    if index == 0:
        return "initial"
    if index == n - 1:
        return "final"
    return "interior"


def parse_page_metadata(text):
    pages = {}
    header_value_counts = {d: Counter() for d in DIMENSIONS}
    for raw in text.splitlines():
        m = PAGE_HEADER_RE.match(raw)
        if not m:
            continue
        page = m.group("page")
        vals = dict(VAR_RE.findall(m.group("vars")))
        pages[page] = vals
        for d in DIMENSIONS:
            header_value_counts[d][vals.get(d, MISSING)] += 1
    return pages, header_value_counts


def data_line_tag_audit(text, analyzed_pages):
    lines_with_tags = Counter()
    tag_values = {"L": Counter(), "I": Counter()}
    examples = {"L": [], "I": []}
    for raw in text.splitlines():
        m = DATA_RE.match(raw)
        if not m:
            continue
        page = m.group("loc").split(".")[0]
        if page not in analyzed_pages:
            continue
        tags = TAG_RE.findall(m.group("body"))
        seen = set()
        for dim, value in tags:
            tag_values[dim][value] += 1
            seen.add(dim)
            if len(examples[dim]) < 10:
                examples[dim].append({"page": page, "locus": m.group("loc"), "value": value})
        for dim in seen:
            lines_with_tags[dim] += 1
    return {
        "analyzed_data_lines_with_tag": {d: int(lines_with_tags[d]) for d in ("L", "I")},
        "tag_value_counts": {d: dict(sorted(tag_values[d].items())) for d in ("L", "I")},
        "examples_first_10": examples,
    }


def eligibility_page(values):
    out = []
    for value, stats in sorted(values.items()):
        frozen = freeze_stats(stats)
        ok = (
            value not in {MISSING, "@"}
            and frozen["parsed_tokens"] >= 1000
            and frozen["unique_physical_leaves"] >= 10
            and all(x["parsed_tokens"] >= 100 for x in frozen["folds"])
        )
        if ok:
            out.append(value)
    return out


def eligibility_position(values):
    out = []
    for value in POSITION_ORDER:
        frozen = freeze_stats(values[value])
        ok = (
            frozen["parsed_tokens"] >= 1000
            and all(x["parsed_tokens"] >= 100 for x in frozen["folds"])
        )
        if ok:
            out.append(value)
    return out


def main(path):
    path = Path(path)
    raw = path.read_bytes()
    blob = e.git_blob_sha1(raw)
    if blob != EXPECTED_SOURCE_BLOB:
        raise SystemExit(f"source blob mismatch: {blob} != {EXPECTED_SOURCE_BLOB}")
    text = raw.decode("utf-8", errors="ignore")

    pages, header_counts = parse_page_metadata(text)
    items = e.parse_voynich(path)
    folds = e.physical_leaf_folds(items)
    universe = set().union(*folds)
    leaf_to_fold = {int(leaf): f for f, leaves in enumerate(folds) for leaf in leaves}
    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)

    total = new_stats()
    by_dim = {d: defaultdict(new_stats) for d in DIMENSIONS}
    by_position = defaultdict(new_stats)
    by_li = defaultdict(new_stats)
    analyzed_pages = set()
    analyzed_paragraphs = 0
    physical_lines = 0
    missing_analyzed_pages = {d: set() for d in ("L", "I")}
    at_analyzed_pages = {d: set() for d in ("L", "I")}

    for item in items:
        leaf = item["leaf"]
        if leaf not in universe:
            continue
        leaf = int(leaf)
        fold = int(leaf_to_fold[leaf])
        page = item["page"]
        analyzed_pages.add(page)
        analyzed_paragraphs += 1
        meta = pages.get(page, {})
        lval = meta.get("L", MISSING)
        ival = meta.get("I", MISSING)
        if lval == MISSING:
            missing_analyzed_pages["L"].add(page)
        if ival == MISSING:
            missing_analyzed_pages["I"].add(page)
        if lval == "@":
            at_analyzed_pages["L"].add(page)
        if ival == "@":
            at_analyzed_pages["I"].add(page)

        for toks in item["lines"]:
            physical_lines += 1
            n = len(toks)
            for idx, tok in enumerate(toks):
                parsed = parser.pick(tok, "min") is not None
                pos = position_category(idx, n)
                add(total, fold, leaf, parsed)
                add(by_position[pos], fold, leaf, parsed)
                for d in DIMENSIONS:
                    add(by_dim[d][meta.get(d, MISSING)], fold, leaf, parsed)
                add(by_li[(lval, ival)], fold, leaf, parsed)

    if total["visible"] != EXPECTED_VISIBLE or total["parsed"] != EXPECTED_PARSED:
        raise SystemExit(
            f"population mismatch: visible={total['visible']} parsed={total['parsed']} "
            f"expected={EXPECTED_VISIBLE}/{EXPECTED_PARSED}"
        )

    page_value_counts_analyzed = {d: Counter() for d in DIMENSIONS}
    for page in sorted(analyzed_pages):
        meta = pages.get(page, {})
        for d in DIMENSIONS:
            page_value_counts_analyzed[d][meta.get(d, MISSING)] += 1

    out = {
        "audit_scope": "population_and_external_metadata_only_no_occupancy_pair_scoring",
        "source": {
            "git_blob": blob,
            "expected_git_blob": EXPECTED_SOURCE_BLOB,
        },
        "parser": {
            "policy_for_parseability_count": "min",
            "validation": parser_validation,
        },
        "population": {
            **freeze_stats(total),
            "analyzed_paragraphs": analyzed_paragraphs,
            "physical_lines": physical_lines,
            "analyzed_pages": len(analyzed_pages),
            "fold_leaf_sets": [sorted(map(int, x)) for x in folds],
        },
        "page_headers": {
            "total_page_headers": len(pages),
            "all_header_value_counts": {d: dict(sorted(header_counts[d].items())) for d in DIMENSIONS},
            "analyzed_page_value_counts": {d: dict(sorted(page_value_counts_analyzed[d].items())) for d in DIMENSIONS},
            "missing_analyzed_pages": {d: sorted(missing_analyzed_pages[d]) for d in ("L", "I")},
            "at_analyzed_pages": {d: sorted(at_analyzed_pages[d]) for d in ("L", "I")},
        },
        "token_support_by_page_variable": {
            d: {value: freeze_stats(stats) for value, stats in sorted(by_dim[d].items())}
            for d in DIMENSIONS
        },
        "token_support_LxI": {
            f"L={l}|I={i}": freeze_stats(stats)
            for (l, i), stats in sorted(by_li.items())
        },
        "token_position_support": {
            value: freeze_stats(by_position[value]) for value in POSITION_ORDER
        },
        "text_tag_audit": data_line_tag_audit(text, analyzed_pages),
        "support_screens": {
            "page_variable_rule": {
                "min_total_parsed": 1000,
                "min_each_fold_parsed": 100,
                "min_unique_physical_leaves": 10,
                "exclude_values": [MISSING, "@"],
            },
            "position_rule": {
                "min_total_parsed": 1000,
                "min_each_fold_parsed": 100,
            },
            "eligible_L_values": eligibility_page(by_dim["L"]),
            "eligible_I_values": eligibility_page(by_dim["I"]),
            "eligible_position_values": eligibility_position(by_position),
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: source_audit.py ZL3b-n.txt")
    main(sys.argv[1])
