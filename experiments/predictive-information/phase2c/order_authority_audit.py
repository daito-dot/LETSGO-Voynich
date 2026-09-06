#!/usr/bin/env python3
"""Issue #98 Phase 2C Gate 0: score-free ordering authority audit.

Audits whether shared lexical item/document sorting agrees with the numeric/source
order required by causal paragraph histories. No predictive metric is computed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
EXPERIMENTS = ROOT / "experiments"
for rel in ("phase62", "occupancy-generation-hierarchy"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as b  # noqa: E402
import ogh_c as C  # noqa: E402

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
PAGE_RE = re.compile(r"^<((?:f|m)\d+[rv]\d?)>")
LEAF_RE = re.compile(r"^[fm](\d+)")
PARA_RE = re.compile(r":p(\d+)$")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paragraph_number(item_id: str) -> int:
    m = PARA_RE.search(item_id)
    if not m:
        raise RuntimeError(f"item id lacks numeric paragraph suffix: {item_id}")
    return int(m.group(1))


def accepted_tokens(item, parsed) -> int:
    return int(
        sum(
            seq is not None
            for line in parsed[item.item_id]
            for seq in line
        )
    )


def visible_tokens(item) -> int:
    return int(sum(len(line) for line in item.lines))


def source_document_order(raw: str):
    by_leaf = defaultdict(list)
    seen = set()
    all_docs = []
    for line in raw.splitlines():
        m = PAGE_RE.match(line)
        if not m:
            continue
        doc = m.group(1)
        if doc in seen:
            raise RuntimeError(f"duplicate page header in raw source: {doc}")
        seen.add(doc)
        lm = LEAF_RE.match(doc)
        if not lm:
            raise RuntimeError(doc)
        leaf = int(lm.group(1))
        by_leaf[leaf].append(doc)
        all_docs.append(doc)
    return dict(by_leaf), all_docs


def audit(zl_path: Path) -> dict:
    blob = b.git_blob_sha1(zl_path.read_bytes())
    if blob != EXPECTED_ZL3B_BLOB:
        raise RuntimeError(f"ZL3b authority mismatch: {blob}")
    raw = zl_path.read_text(encoding="utf-8")
    items, folds, parsed = C.load_corpus(zl_path)

    by_doc = defaultdict(list)
    for it in items:
        by_doc[it.document].append(it)

    mismatched_docs = []
    max_paragraphs = 0
    max_docs = []
    total_items = len(items)
    total_visible = sum(visible_tokens(it) for it in items)
    total_accepted = sum(accepted_tokens(it, parsed) for it in items)
    order_affected_items = set()
    bag_affected_items = set()

    per_doc_counts = {}
    for doc, group in sorted(by_doc.items()):
        lex = sorted(group, key=lambda x: x.item_id)
        num = sorted(group, key=lambda x: paragraph_number(x.item_id))
        per_doc_counts[doc] = len(group)
        if len(group) > max_paragraphs:
            max_paragraphs = len(group)
            max_docs = [doc]
        elif len(group) == max_paragraphs:
            max_docs.append(doc)

        lex_ids = [x.item_id for x in lex]
        num_ids = [x.item_id for x in num]
        if lex_ids == num_ids:
            continue

        lex_pos = {x: i for i, x in enumerate(lex_ids)}
        num_pos = {x: i for i, x in enumerate(num_ids)}
        affected_order = []
        affected_bag = []
        for item_id in num_ids:
            lprev = lex_ids[: lex_pos[item_id]]
            nprev = num_ids[: num_pos[item_id]]
            if lprev != nprev:
                affected_order.append(item_id)
                order_affected_items.add(item_id)
            if set(lprev) != set(nprev):
                affected_bag.append(item_id)
                bag_affected_items.add(item_id)
        mismatched_docs.append({
            "document": doc,
            "paragraph_count": len(group),
            "lexical_order": lex_ids,
            "numeric_order": num_ids,
            "order_affected_items": affected_order,
            "bag_prefix_affected_items": affected_bag,
        })

    item_map = {it.item_id: it for it in items}
    order_visible = sum(visible_tokens(item_map[x]) for x in order_affected_items)
    order_accepted = sum(accepted_tokens(item_map[x], parsed) for x in order_affected_items)
    bag_visible = sum(visible_tokens(item_map[x]) for x in bag_affected_items)
    bag_accepted = sum(accepted_tokens(item_map[x], parsed) for x in bag_affected_items)

    source_by_leaf, source_docs = source_document_order(raw)
    lexical_by_leaf = defaultdict(list)
    for doc in sorted(by_doc):
        lm = LEAF_RE.match(doc)
        if not lm:
            raise RuntimeError(doc)
        lexical_by_leaf[int(lm.group(1))].append(doc)

    page_order_mismatches = []
    for leaf in sorted(set(source_by_leaf) | set(lexical_by_leaf)):
        src = source_by_leaf.get(leaf, [])
        lex = lexical_by_leaf.get(leaf, [])
        # Compare only page-side documents represented by parsed paragraph items.
        src_parsed = [d for d in src if d in by_doc]
        if src_parsed != lex:
            page_order_mismatches.append({
                "leaf": leaf,
                "source_document_order": src_parsed,
                "lexical_document_order": lex,
            })

    # Folds are defined on numeric physical leaves, so within-leaf reordering
    # cannot change membership. Verify every item leaf occurs in exactly one fold.
    leaf_fold = {}
    for f, leaves in enumerate(folds):
        for leaf in leaves:
            if leaf in leaf_fold:
                raise RuntimeError("leaf occurs in multiple frozen folds")
            leaf_fold[leaf] = f
    missing_fold_items = [it.item_id for it in items if it.leaf not in leaf_fold]
    if missing_fold_items:
        raise RuntimeError("items outside frozen folds")

    gate_pass = not mismatched_docs and not page_order_mismatches
    return {
        "schema": "issue98-phase2c-order-audit-v1",
        "gate_pass": bool(gate_pass),
        "source": {
            "git_blob_sha1": blob,
            "expected_git_blob_sha1": EXPECTED_ZL3B_BLOB,
            "source_sha256": hashlib.sha256(zl_path.read_bytes()).hexdigest(),
        },
        "code": {
            "audit_sha256": sha256_file(HERE),
            "phase62_parser_sha256": sha256_file(EXPERIMENTS / "phase62" / "phase62b_n0.py"),
            "ogh_c_sha256": sha256_file(EXPERIMENTS / "occupancy-generation-hierarchy" / "ogh_c.py"),
        },
        "population": {
            "n_items": total_items,
            "n_documents_with_items": len(by_doc),
            "n_visible_tokens": total_visible,
            "n_parser_accepted_tokens": total_accepted,
            "max_paragraphs_per_document": max_paragraphs,
            "documents_at_max": max_docs,
        },
        "paragraph_order": {
            "mismatched_document_count": len(mismatched_docs),
            "mismatched_documents": mismatched_docs,
            "order_affected_item_count": len(order_affected_items),
            "order_affected_visible_tokens": order_visible,
            "order_affected_accepted_tokens": order_accepted,
            "order_affected_accepted_fraction": float(order_accepted / total_accepted) if total_accepted else 0.0,
            "bag_prefix_affected_item_count": len(bag_affected_items),
            "bag_prefix_affected_visible_tokens": bag_visible,
            "bag_prefix_affected_accepted_tokens": bag_accepted,
            "bag_prefix_affected_accepted_fraction": float(bag_accepted / total_accepted) if total_accepted else 0.0,
        },
        "page_side_order": {
            "source_page_headers": len(source_docs),
            "mismatched_leaf_count": len(page_order_mismatches),
            "mismatches": page_order_mismatches,
        },
        "fold_membership": {
            "n_folds": len(folds),
            "would_change_under_within_leaf_order_fix": False,
            "all_items_in_exactly_one_leaf_fold": True,
        },
        "firewall": {
            "predictive_scores_computed": False,
            "surface_target_metrics_scored": False,
            "semantic_or_image_context_used": False,
        },
        "gate_rule": (
            "PROCEED_PHASE2C" if gate_pass else
            "STOP_AND_CORRECT_ORDER_THEN_RERUN_PREDICTIVE_PHASES"
        ),
    }


def self_test():
    ids = ["f1r:p1", "f1r:p2", "f1r:p10", "f1r:p3"]
    lex = sorted(ids)
    num = sorted(ids, key=paragraph_number)
    assert lex != num
    assert num == ["f1r:p1", "f1r:p2", "f1r:p3", "f1r:p10"]
    return {"ok": True, "score_free": True, "synthetic_mismatch_detected": True}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--audit", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(ns.self_test) + int(ns.audit is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    out = audit(Path(ns.audit[0]))
    Path(ns.audit[1]).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "gate_pass": out["gate_pass"],
        "gate_rule": out["gate_rule"],
        "population": out["population"],
        "paragraph_order": {
            k: v for k, v in out["paragraph_order"].items() if k != "mismatched_documents"
        },
        "mismatched_documents": [
            {"document": d["document"], "paragraph_count": d["paragraph_count"]}
            for d in out["paragraph_order"]["mismatched_documents"]
        ],
        "page_side_order": out["page_side_order"],
        "fold_membership": out["fold_membership"],
        "firewall": out["firewall"],
    }, indent=2, sort_keys=True))
    # Audit mismatch is a scientific gate outcome, not a CI failure.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
