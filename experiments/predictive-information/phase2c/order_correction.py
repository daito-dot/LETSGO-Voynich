#!/usr/bin/env python3
"""Score-free causal-order authority for Issue #98 correction replays.

This module does not score prediction or any Voynich target statistic. It derives
only page-side/document order from the frozen raw ZL3b page headers and numeric
paragraph order from parser item ids.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

PAGE_RE = re.compile(r"^<((?:f|m)\d+[rv]\d?)>")
LEAF_RE = re.compile(r"^[fm](\d+)")
PARA_RE = re.compile(r":p(\d+)$")


@dataclass(frozen=True)
class OrderAuthority:
    source_docs: Tuple[str, ...]
    global_rank: Dict[str, int]
    by_leaf: Dict[int, Tuple[str, ...]]


def paragraph_number(item_id: str) -> int:
    m = PARA_RE.search(item_id)
    if not m:
        raise RuntimeError(f"item id lacks numeric paragraph suffix: {item_id}")
    return int(m.group(1))


def leaf_number(document: str) -> int:
    m = LEAF_RE.match(document)
    if not m:
        raise RuntimeError(f"document lacks numeric physical leaf: {document}")
    return int(m.group(1))


def load_authority(zl_path: Path) -> OrderAuthority:
    raw = zl_path.read_text(encoding="utf-8")
    source_docs: List[str] = []
    seen = set()
    by_leaf_lists = defaultdict(list)
    for line in raw.splitlines():
        m = PAGE_RE.match(line)
        if not m:
            continue
        doc = m.group(1)
        if doc in seen:
            raise RuntimeError(f"duplicate raw page header: {doc}")
        seen.add(doc)
        source_docs.append(doc)
        by_leaf_lists[leaf_number(doc)].append(doc)
    if not source_docs:
        raise RuntimeError("no raw page-header authority found")
    return OrderAuthority(
        source_docs=tuple(source_docs),
        global_rank={doc: i for i, doc in enumerate(source_docs)},
        by_leaf={leaf: tuple(docs) for leaf, docs in by_leaf_lists.items()},
    )


def corrected_key(item, authority: OrderAuthority):
    doc = item.document
    if doc not in authority.global_rank:
        raise RuntimeError(f"parsed document absent from raw page-header authority: {doc}")
    leaf = leaf_number(doc)
    if item.leaf is None or int(item.leaf) != leaf:
        raise RuntimeError(f"item/document leaf mismatch: {item.item_id} document={doc} item.leaf={item.leaf}")
    return (leaf, authority.global_rank[doc], paragraph_number(item.item_id))


def ordered(items: Sequence, authority: OrderAuthority):
    ids = [it.item_id for it in items]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate parsed item ids")
    return sorted(items, key=lambda it: corrected_key(it, authority))


def validate(items: Sequence, authority: OrderAuthority) -> dict:
    ordered_items = ordered(items, authority)
    by_doc = defaultdict(list)
    by_leaf_docs = defaultdict(list)
    for it in ordered_items:
        by_doc[it.document].append(it)
        if not by_leaf_docs[int(it.leaf)] or by_leaf_docs[int(it.leaf)][-1] != it.document:
            by_leaf_docs[int(it.leaf)].append(it.document)

    numeric_ok = True
    for group in by_doc.values():
        nums = [paragraph_number(it.item_id) for it in group]
        if nums != sorted(nums):
            numeric_ok = False
            break

    source_doc_ok = True
    mismatched_leaves = []
    parsed_docs = set(by_doc)
    for leaf, docs in sorted(by_leaf_docs.items()):
        expected = [d for d in authority.by_leaf.get(leaf, ()) if d in parsed_docs]
        if list(docs) != expected:
            source_doc_ok = False
            mismatched_leaves.append({"leaf": leaf, "observed": list(docs), "expected": expected})

    return {
        "n_items": len(items),
        "n_documents": len(by_doc),
        "numeric_paragraph_order_ok": bool(numeric_ok),
        "raw_page_side_order_ok": bool(source_doc_ok),
        "mismatched_leaves": mismatched_leaves,
        "pass": bool(numeric_ok and source_doc_ok),
    }
