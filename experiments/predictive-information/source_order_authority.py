#!/usr/bin/env python3
"""Versioned causal item-order authority for predictive-information reruns.

The historical parser output is intentionally left unchanged so archived results
remain reproducible. New corrected reruns call `configure(zl_path)` once and then
use `ordered(items)` instead of lexical item-id sorting.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Sequence

PAGE_RE = re.compile(r"^<((?:f|m)\d+[rv]\d?)>")
PARA_RE = re.compile(r":p(\d+)$")
LEAF_RE = re.compile(r"^[fm](\d+)")

_DOC_RANK = None
_SOURCE_DOCS = None
_SOURCE_SHA256 = None


def configure(zl_path: Path):
    global _DOC_RANK, _SOURCE_DOCS, _SOURCE_SHA256
    raw = zl_path.read_text(encoding="utf-8")
    docs = []
    seen = set()
    for line in raw.splitlines():
        m = PAGE_RE.match(line)
        if not m:
            continue
        doc = m.group(1)
        if doc in seen:
            raise RuntimeError(f"duplicate source page header: {doc}")
        seen.add(doc)
        docs.append(doc)
    if not docs:
        raise RuntimeError("no source page headers found")
    _SOURCE_DOCS = tuple(docs)
    _DOC_RANK = {doc: i for i, doc in enumerate(docs)}
    _SOURCE_SHA256 = hashlib.sha256(zl_path.read_bytes()).hexdigest()
    return {
        "source_sha256": _SOURCE_SHA256,
        "source_document_count": len(docs),
        "first_document": docs[0],
        "last_document": docs[-1],
    }


def paragraph_number(item_id: str) -> int:
    m = PARA_RE.search(item_id)
    if not m:
        raise RuntimeError(f"item id lacks numeric paragraph suffix: {item_id}")
    return int(m.group(1))


def document_rank(document: str) -> int:
    if _DOC_RANK is None:
        raise RuntimeError("source_order_authority.configure() was not called")
    if document not in _DOC_RANK:
        raise RuntimeError(f"parsed document absent from raw source authority: {document}")
    return int(_DOC_RANK[document])


def item_key(it):
    return (document_rank(it.document), paragraph_number(it.item_id), it.item_id)


def ordered(items: Sequence):
    return sorted(items, key=item_key)


def verify(items: Sequence) -> dict:
    seq = ordered(items)
    docs = {}
    for it in seq:
        docs.setdefault(it.document, []).append(paragraph_number(it.item_id))
    nonmonotone = {
        doc: nums for doc, nums in docs.items()
        if nums != sorted(nums)
    }
    if nonmonotone:
        raise RuntimeError(f"numeric paragraph order failed: {nonmonotone}")

    # Within every numeric physical leaf, parsed documents must appear in the
    # same relative order as their raw page headers.
    source_by_leaf = {}
    for doc in _SOURCE_DOCS or ():
        lm = LEAF_RE.match(doc)
        if lm:
            source_by_leaf.setdefault(int(lm.group(1)), []).append(doc)
    parsed_by_leaf = {}
    for it in seq:
        parsed_by_leaf.setdefault(int(it.leaf), [])
        if it.document not in parsed_by_leaf[int(it.leaf)]:
            parsed_by_leaf[int(it.leaf)].append(it.document)
    mismatches = {}
    for leaf, parsed_docs in parsed_by_leaf.items():
        src = [d for d in source_by_leaf.get(leaf, []) if d in parsed_docs]
        if src != parsed_docs:
            mismatches[str(leaf)] = {"source": src, "parsed": parsed_docs}
    if mismatches:
        raise RuntimeError(f"source document order verification failed: {mismatches}")

    payload = "\n".join(it.item_id for it in seq).encode("utf-8")
    return {
        "n_items": len(seq),
        "n_documents": len(docs),
        "numeric_paragraph_order_valid": True,
        "source_document_order_valid": True,
        "ordered_item_ids_sha256": hashlib.sha256(payload).hexdigest(),
        "source_sha256": _SOURCE_SHA256,
    }
