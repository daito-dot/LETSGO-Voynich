#!/usr/bin/env python3
"""Phase63B B1 parser-only preflight; no scientific metric."""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import phase63b_common_b1 as q


def summary(path: Path, label: str, view: str) -> dict:
    paragraphs, audit = q.parse_ivtff(path, label, view)
    its = q.items(paragraphs)
    line_counts = [len(p.lines) for p in paragraphs]
    line_token_counts = [len(line) for p in paragraphs for line in p.lines]
    tokens = [tok for p in paragraphs for line in p.lines for tok in line]
    types = set(tokens)
    basepop = [it for it in its if q.b.base_eligible(it)]
    s1pop = [it for it in basepop if q.b.valid_pseudo_indices(it)]
    leaves = sorted({p.leaf for p in paragraphs if p.leaf is not None})
    return {
        **audit,
        "parsed_paragraphs": len(paragraphs),
        "paragraphs_with_usable_lines": sum(bool(p.lines) for p in paragraphs),
        "nonempty_physical_lines": len(line_token_counts),
        "usable_token_occurrences": len(tokens),
        "usable_token_types": len(types),
        "base_eligible_paragraphs": len(basepop),
        "S1_eligible_paragraphs": len(s1pop),
        "physical_leaves": len(leaves),
        "physical_leaf_numbers": leaves,
        "line_count_per_paragraph": {
            "min": min(line_counts) if line_counts else 0,
            "median": float(statistics.median(line_counts)) if line_counts else 0.0,
            "max": max(line_counts) if line_counts else 0,
        },
        "tokens_per_nonempty_line": {
            "min": min(line_token_counts) if line_token_counts else 0,
            "median": float(statistics.median(line_token_counts)) if line_token_counts else 0.0,
            "max": max(line_token_counts) if line_token_counts else 0,
        },
    }


def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt GC2a-n.txt IT2a-n.txt", file=sys.stderr)
        return 2
    paths = {
        "ZL3b": Path(sys.argv[1]).resolve(),
        "GC2a": Path(sys.argv[2]).resolve(),
        "IT2a": Path(sys.argv[3]).resolve(),
    }
    out = {
        "phase": "63B parser preflight B1",
        "scope": "population/parser counts only; no edit1/features/S1/S2/S3/H62-P1/A1",
        "parser_amendment": "PARSER_AMENDMENT_B1.md",
        "scientific_metrics_computed": False,
        "sources": {
            label: {view: summary(path, label, view) for view in ("W1", "W2")}
            for label, path in paths.items()
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
