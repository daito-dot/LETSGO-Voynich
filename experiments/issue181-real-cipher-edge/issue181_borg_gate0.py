#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ATOM_RE = re.compile(r"^S[0-9]{3,4}$")


def parse_page(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    raw_lines = text.splitlines()
    lines: list[list[list[str]]] = []
    malformed = []
    vocab = set()

    for line_no, raw in enumerate(raw_lines, 1):
        if not raw.strip():
            continue
        units = []
        for unit_no, chunk in enumerate(raw.split("|"), 1):
            chunk = chunk.strip()
            if not chunk:
                malformed.append({"line": line_no, "unit": unit_no, "value": chunk, "reason": "empty_unit"})
                continue
            atoms = chunk.split()
            bad = [a for a in atoms if not ATOM_RE.fullmatch(a)]
            if bad:
                malformed.append({"line": line_no, "unit": unit_no, "value": chunk, "reason": "invalid_atom", "atoms": bad})
            vocab.update(a for a in atoms if ATOM_RE.fullmatch(a))
            units.append(atoms)
        lines.append(units)

    same_edges = sum(max(0, len(line) - 1) for line in lines)
    cross_edges = max(0, len(lines) - 1)
    unit_count = sum(len(line) for line in lines)
    atom_count = sum(len(unit) for line in lines for unit in line)
    return {
        "page_id": path.name.removesuffix(".canonical.txt"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "raw_line_count": len(raw_lines),
        "nonempty_line_count": len(lines),
        "unit_count": unit_count,
        "atom_count": atom_count,
        "same_line_edge_count": same_edges,
        "cross_line_edge_count": cross_edges,
        "vocab": sorted(vocab),
        "malformed": malformed,
    }


def audit(root: Path) -> dict:
    files = sorted(root.glob("borg_*.canonical.txt"))
    pages = [parse_page(p) for p in files]
    malformed = [
        {"page_id": p["page_id"], **m}
        for p in pages
        for m in p["malformed"]
    ]
    nonempty = [p for p in pages if p["unit_count"] > 0]
    nonempty = sorted(nonempty, key=lambda p: p["page_id"])

    fold_pages = {str(i): [] for i in range(5)}
    for i, p in enumerate(nonempty):
        fold_pages[str(i % 5)].append(p["page_id"])

    by_id = {p["page_id"]: p for p in nonempty}
    folds = {}
    for f, ids in fold_pages.items():
        folds[f] = {
            "page_count": len(ids),
            "page_ids": ids,
            "physical_nonempty_lines": sum(by_id[x]["nonempty_line_count"] for x in ids),
            "unit_count": sum(by_id[x]["unit_count"] for x in ids),
            "same_line_edge_count": sum(by_id[x]["same_line_edge_count"] for x in ids),
            "cross_line_edge_count": sum(by_id[x]["cross_line_edge_count"] for x in ids),
        }

    vocab = sorted({a for p in nonempty for a in p["vocab"]})
    valid = (
        len(files) > 0
        and len(nonempty) > 0
        and not malformed
        and all(v["same_line_edge_count"] > 0 and v["cross_line_edge_count"] > 0 for v in folds.values())
    )

    return {
        "experiment": "Issue #181 Borg external R5 Gate0",
        "edge_likelihood_computed": False,
        "representation": "canonical S### atoms; literal | cipher-unit boundaries; newline physical lines",
        "canonical_file_count": len(files),
        "nonempty_page_count": len(nonempty),
        "empty_page_count": len(files) - len(nonempty),
        "physical_nonempty_line_count": sum(p["nonempty_line_count"] for p in nonempty),
        "unit_count": sum(p["unit_count"] for p in nonempty),
        "atom_count": sum(p["atom_count"] for p in nonempty),
        "same_line_edge_count": sum(p["same_line_edge_count"] for p in nonempty),
        "cross_line_edge_count": sum(p["cross_line_edge_count"] for p in nonempty),
        "atom_vocabulary": vocab,
        "atom_vocabulary_size": len(vocab),
        "malformed_count": len(malformed),
        "malformed": malformed,
        "folds": folds,
        "page_sha256": {p["page_id"]: p["sha256"] for p in pages},
        "gate0_classification": "GATE0_VALID" if valid else "INVALID_EXTERNAL_REPRESENTATION",
    }


def synthetic_preflight() -> None:
    d = Path("/tmp/issue181_gate0_synth")
    d.mkdir(parents=True, exist_ok=True)
    for i in range(10):
        (d / f"borg_{i:04d}r.canonical.txt").write_text(
            "S001 S002 | S003\nS004 | S005 S006\n", encoding="utf-8"
        )
    r = audit(d)
    assert r["edge_likelihood_computed"] is False
    assert r["gate0_classification"] == "GATE0_VALID"
    assert r["nonempty_page_count"] == 10
    assert all(v["page_count"] == 2 for v in r["folds"].values())
    print("SYNTHETIC_GATE0_OK")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--synthetic-preflight", action="store_true")
    args = ap.parse_args()
    if args.synthetic_preflight:
        synthetic_preflight()
        return
    if args.root is None:
        ap.error("root is required unless --synthetic-preflight")
    r = audit(args.root)
    s = json.dumps(r, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(s, encoding="utf-8")
    else:
        print(s)


if __name__ == "__main__":
    main()
