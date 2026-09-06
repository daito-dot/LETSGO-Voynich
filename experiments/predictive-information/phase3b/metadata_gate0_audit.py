#!/usr/bin/env python3
"""Issue #107 Phase 3B Gate 0: score-free IVTFF metadata/confounding audit.

Resolves page variables and legal text tags for I/H/C/L at the same P-locus
positions used by the frozen Voynich parser. Computes only metadata/support
counts; no predictive probability or target statistic is available here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PRED = ROOT / "experiments" / "predictive-information"
PHASE1_PATH = PRED / "phase1" / "phase1_predictive_budget.py"
CURRIER_PATH = PRED / "phase3a" / "currier_gate0_audit.py"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
VARIABLES = ("I", "H", "C", "L")
CANDIDATE_PRIORITY = ("H", "I", "C")
TAG_RE = re.compile(r"<@(?P<key>[IHCL])=(?P<value>[^>\s])>")
SPECIAL = {"MISSING", "UNSET", "UNKNOWN_OTHER", "@"}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P1 = load_module("issue107_phase1_loader", PHASE1_PATH)
G0 = load_module("issue107_phase3a_currier_authority", CURRIER_PATH)
I81 = P1.I


def source_blob_sha1(path: Path) -> str:
    return I81.b.git_blob_sha1(path.read_bytes())


def raw_header_distribution(headers, var: str):
    c = Counter()
    for r in headers:
        v = r["fields"].get(var)
        c["MISSING" if v is None else v] += 1
    return dict(sorted(c.items()))


def initial_state(fields: dict):
    out = {}
    for var in VARIABLES:
        v = fields.get(var)
        if v is None:
            out[var] = "MISSING"
        elif v == "@":
            out[var] = "UNSET"
        else:
            out[var] = v
    return out


def stat_bucket():
    return {
        "visible_tokens": 0,
        "accepted_tokens": 0,
        "items": set(),
        "documents": set(),
        "leaves": set(),
        "folds": set(),
    }


def add_stat(bucket, row, accepted: bool):
    bucket["visible_tokens"] += 1
    bucket["accepted_tokens"] += int(bool(accepted))
    bucket["items"].add(row["item_id"])
    bucket["documents"].add(row["document"])
    bucket["leaves"].add(int(row["leaf"]))
    bucket["folds"].add(int(row["fold"]))


def freeze_stat(bucket):
    return {
        "visible_tokens": int(bucket["visible_tokens"]),
        "accepted_tokens": int(bucket["accepted_tokens"]),
        "items": len(bucket["items"]),
        "documents": len(bucket["documents"]),
        "leaves": len(bucket["leaves"]),
        "nonzero_folds": len(bucket["folds"]) if bucket["accepted_tokens"] > 0 else 0,
        "folds": sorted(bucket["folds"]) if bucket["accepted_tokens"] > 0 else [],
    }


def scan_token_metadata(zl_path: Path, items, folds, parsed, headers):
    by_doc = {r["document"]: r for r in headers}
    item_by_id = {it.item_id: it for it in items}
    if len(item_by_id) != len(items):
        raise RuntimeError("duplicate parsed item ids")

    fold_of_leaf = {}
    for f, leafset in enumerate(folds):
        for leaf in leafset:
            leaf = int(leaf)
            if leaf in fold_of_leaf:
                raise RuntimeError(f"leaf {leaf} occurs in multiple folds")
            fold_of_leaf[leaf] = int(f)

    current_page = None
    current_fields = None
    state = None
    pid = defaultdict(int)
    current_item = None
    current_line_index = 0
    seen_lines = defaultdict(int)
    token_rows = []
    tag_events = defaultdict(list)
    conformance = []
    raw_l_authority_mismatches = []

    lines = zl_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for source_line_no, s in enumerate(lines, start=1):
        hm = I81.b.HP.match(s)
        if hm:
            current_page = hm.group("p")
            if current_page not in by_doc:
                raise RuntimeError(f"page header missing from Currier authority: {current_page}")
            current_fields = dict(by_doc[current_page]["fields"])
            state = initial_state(current_fields)
            current_item = None
            current_line_index = 0
            continue

        if current_page is None:
            continue

        tags = [(m.group("key"), m.group("value")) for m in TAG_RE.finditer(s)]
        if tags:
            per_var = defaultdict(list)
            for k, v in tags:
                per_var[k].append(v)
            for k, vals in per_var.items():
                if len(set(vals)) > 1:
                    conformance.append({
                        "source_line": source_line_no,
                        "document": current_page,
                        "variable": k,
                        "reason": "CONFLICTING_TAGS_ON_ONE_LINE",
                        "values": vals,
                    })
                header_value = current_fields.get(k)
                if header_value != "@":
                    conformance.append({
                        "source_line": source_line_no,
                        "document": current_page,
                        "variable": k,
                        "reason": "TAG_WITHOUT_HEADER_AT",
                        "header_value": "MISSING" if header_value is None else header_value,
                        "values": vals,
                    })
                # IVTFF disallows conflicting same-variable tags; retain last only for full audit trace.
                state[k] = vals[-1]
                tag_events[k].append({
                    "source_line": source_line_no,
                    "document": current_page,
                    "value": vals[-1],
                })

        lm = I81.b.LP.match(s)
        if not lm or "P" not in lm.group("c"):
            continue
        page = lm.group("loc").split(".")[0]
        if page != current_page:
            raise RuntimeError(f"locus/header page mismatch line {source_line_no}: {page} != {current_page}")

        start, toks = I81.b.voynich_line(lm.group("b"))
        if start:
            pid[page] += 1
            current_item = f"{page}:p{pid[page]}"
            current_line_index = 0
        if not toks or current_item is None:
            continue
        if current_item not in item_by_id or current_item not in parsed:
            raise RuntimeError(f"source paragraph absent from parsed population: {current_item}")
        it = item_by_id[current_item]
        if current_line_index >= len(it.lines):
            raise RuntimeError(f"source has extra token-bearing line for {current_item}")
        if list(toks) != list(it.lines[current_line_index]):
            raise RuntimeError(f"source/parser token mismatch {current_item} line {current_line_index}")
        p_line = parsed[current_item][current_line_index]
        if len(p_line) != len(toks):
            raise RuntimeError(f"accepted parse line length mismatch {current_item} line {current_line_index}")
        leaf = int(it.leaf)
        if leaf not in fold_of_leaf:
            raise RuntimeError(f"parsed leaf absent from frozen folds: {leaf}")
        l_authority = by_doc[page]["label"]
        if state["L"] in ("A", "B") and l_authority in ("A", "B") and state["L"] != l_authority:
            raw_l_authority_mismatches.append({
                "source_line": source_line_no,
                "document": page,
                "raw_resolved_L": state["L"],
                "phase3a_L_authority": l_authority,
            })
        for ti, _tok in enumerate(toks):
            token_rows.append({
                "item_id": current_item,
                "document": page,
                "leaf": leaf,
                "fold": fold_of_leaf[leaf],
                "line_index": current_line_index,
                "token_index": ti,
                "accepted": p_line[ti] is not None,
                "L_AUTH": l_authority,
                "I": state["I"],
                "H": state["H"],
                "C": state["C"],
                "L_RAW_RESOLVED": state["L"],
            })
        seen_lines[current_item] += 1
        current_line_index += 1

    missing_or_extra_lines = []
    for item_id, it in sorted(item_by_id.items()):
        got = int(seen_lines.get(item_id, 0))
        want = len(it.lines)
        if got != want:
            missing_or_extra_lines.append({"item_id": item_id, "seen": got, "expected": want})

    return {
        "rows": token_rows,
        "tag_events": {k: v for k, v in sorted(tag_events.items())},
        "conformance_violations": conformance,
        "raw_L_vs_phase3a_authority_mismatches": raw_l_authority_mismatches,
        "line_mapping_mismatches": missing_or_extra_lines,
    }


def level_stats(rows, var: str):
    d = defaultdict(stat_bucket)
    for row in rows:
        val = row["L_AUTH"] if var == "L" else row[var]
        add_stat(d[val], row, row["accepted"])
    return {k: freeze_stat(v) for k, v in sorted(d.items())}


def fold_support(rows, var: str):
    levels = sorted({row["L_AUTH"] if var == "L" else row[var] for row in rows})
    out = {}
    for level in levels:
        counts = {str(f): 0 for f in range(5)}
        for row in rows:
            val = row["L_AUTH"] if var == "L" else row[var]
            if val == level and row["accepted"]:
                counts[str(row["fold"])] += 1
        out[level] = counts
    return out


def leaf_mixing(rows, var: str):
    values = defaultdict(set)
    for row in rows:
        if not row["accepted"]:
            continue
        val = row["L_AUTH"] if var == "L" else row[var]
        if val not in SPECIAL:
            values[int(row["leaf"])].add(val)
    mixed = [
        {"leaf": leaf, "levels": sorted(vals)}
        for leaf, vals in sorted(values.items()) if len(vals) > 1
    ]
    return {"mixed_leaf_count": len(mixed), "mixed_leaves": mixed}


def cross_tab(rows, variables):
    d = defaultdict(stat_bucket)
    for row in rows:
        if not row["accepted"]:
            continue
        vals = []
        for var in variables:
            vals.append(row["L_AUTH"] if var == "L" else row[var])
        key = "|".join(vals)
        add_stat(d[key], row, True)
    return {k: freeze_stat(v) for k, v in sorted(d.items())}


def identifiability(rows):
    factors = {}
    for factor in CANDIDATE_PRIORITY:
        levels = sorted({row[factor] for row in rows if row[factor] not in SPECIAL})
        level_diag = {}
        usable = []
        for level in levels:
            by_l = {}
            all_leaves = set()
            for lab in ("A", "B"):
                cell = [r for r in rows if r["accepted"] and r["L_AUTH"] == lab and r[factor] == level]
                folds = sorted({int(r["fold"]) for r in cell})
                leaves = sorted({int(r["leaf"]) for r in cell})
                all_leaves.update(leaves)
                by_l[lab] = {
                    "accepted_tokens": len(cell),
                    "nonzero_folds": len(folds),
                    "folds": folds,
                    "leaves": len(leaves),
                }
            ok = bool(
                by_l["A"]["accepted_tokens"] > 0
                and by_l["B"]["accepted_tokens"] > 0
                and by_l["A"]["nonzero_folds"] >= 4
                and by_l["B"]["nonzero_folds"] >= 4
                and len(all_leaves) >= 2
            )
            level_diag[level] = {
                "cross_currier_usable": ok,
                "A": by_l["A"],
                "B": by_l["B"],
                "union_leaves": len(all_leaves),
            }
            if ok:
                usable.append(level)
        identifiable = len(usable) >= 2
        factors[factor] = {
            "classification": "CROSS-CURRIER IDENTIFIABLE" if identifiable else "NOT ADEQUATELY CROSSED",
            "usable_levels": usable,
            "all_levels": level_diag,
        }
    licensed = next((f for f in CANDIDATE_PRIORITY if factors[f]["classification"] == "CROSS-CURRIER IDENTIFIABLE"), None)
    return factors, licensed


def audit(zl_path: Path):
    if source_blob_sha1(zl_path) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b source differs from frozen authority")

    headers = G0.parse_source_headers(zl_path)
    order_cfg = OA.configure(zl_path)
    items, folds, parsed = I81.C.load_corpus(zl_path)
    order_verify = OA.verify(items)
    if len(folds) != 5:
        raise RuntimeError("frozen fold count changed")

    scan = scan_token_metadata(zl_path, items, folds, parsed, headers)
    rows = scan.pop("rows")
    visible_expected = sum(len(line) for it in items for line in it.lines)
    accepted_expected = sum(seq is not None for it in items for line in parsed[it.item_id] for seq in line)
    visible_scanned = len(rows)
    accepted_scanned = sum(bool(r["accepted"]) for r in rows)

    mapping_valid = bool(
        visible_scanned == visible_expected
        and accepted_scanned == accepted_expected
        and not scan["line_mapping_mismatches"]
    )

    stats = {var: level_stats(rows, var) for var in VARIABLES}
    support = {var: fold_support(rows, var) for var in VARIABLES}
    mixing = {var: leaf_mixing(rows, var) for var in VARIABLES}
    cross_tabs = {
        "LxI": cross_tab(rows, ("L", "I")),
        "LxH": cross_tab(rows, ("L", "H")),
        "LxC": cross_tab(rows, ("L", "C")),
        "IxH": cross_tab(rows, ("I", "H")),
        "LxIxH": cross_tab(rows, ("L", "I", "H")),
    }
    factors, licensed = identifiability(rows)

    conformance_valid = not scan["conformance_violations"]
    l_authority_consistent = not scan["raw_L_vs_phase3a_authority_mismatches"]
    audit_valid = bool(
        mapping_valid
        and conformance_valid
        and l_authority_consistent
        and order_verify["numeric_paragraph_order_valid"]
        and order_verify["source_document_order_valid"]
    )
    if not audit_valid:
        classification = "METADATA / MAPPING INVALID"
        licensed = None
    elif licensed is None:
        classification = "NO ADEQUATELY CROSSED OBSERVABLE FACTOR"
    else:
        classification = f"LICENSE {licensed} FOR CONDITIONAL TRANSPORT"

    return {
        "schema": "issue107-phase3b-metadata-gate0-v1",
        "phase": "ISSUE107_PHASE3B_GATE0",
        "audit_valid": audit_valid,
        "classification": classification,
        "licensed_factor": licensed,
        "candidate_priority": list(CANDIDATE_PRIORITY),
        "source": {
            "git_blob_sha1": source_blob_sha1(zl_path),
            "sha256": hashlib.sha256(zl_path.read_bytes()).hexdigest(),
            "page_headers": len(headers),
        },
        "raw_header_distribution": {var: raw_header_distribution(headers, var) for var in VARIABLES},
        "tag_audit": scan,
        "population_mapping": {
            "visible_expected": int(visible_expected),
            "visible_scanned": int(visible_scanned),
            "accepted_expected": int(accepted_expected),
            "accepted_scanned": int(accepted_scanned),
            "mapping_valid": mapping_valid,
        },
        "resolved_level_stats": stats,
        "accepted_fold_support": support,
        "leaf_mixing": mixing,
        "cross_tabs": cross_tabs,
        "identifiability": factors,
        "order_authority": {**order_cfg, **order_verify},
        "fold_identity_sha256": P1.P0.fold_hash(folds),
        "firewall": {
            "predictive_scores_computed": False,
            "model_fitted": False,
            "surface_target_metrics_scored": False,
            "issue84_target_used": False,
            "image_context_used": False,
            "semantic_or_plaintext_used": False,
            "latent_state_fitted": False,
            "factor_selected_from_support_only": True,
        },
    }


def self_test():
    assert initial_state({"H": "@", "I": "H", "C": "1"}) == {
        "I": "H", "H": "UNSET", "C": "1", "L": "MISSING"
    }
    fake = [
        {"accepted": True, "L_AUTH": "A", "H": "1", "I": "H", "C": "1", "leaf": 1, "fold": 0, "item_id": "x", "document": "f1r"},
        {"accepted": True, "L_AUTH": "B", "H": "1", "I": "H", "C": "2", "leaf": 2, "fold": 1, "item_id": "y", "document": "f2r"},
    ]
    t = cross_tab(fake, ("L", "H"))
    assert t["A|1"]["accepted_tokens"] == 1 and t["B|1"]["accepted_tokens"] == 1
    return {
        "ok": True,
        "score_free": True,
        "page_at_initializes_unset": True,
        "cross_tab": True,
        "predictive_scores_computed": False,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--audit", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.audit is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    result = audit(Path(ns.audit[0]))
    Path(ns.audit[1]).write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    compact = {
        "audit_valid": result["audit_valid"],
        "classification": result["classification"],
        "licensed_factor": result["licensed_factor"],
        "raw_header_distribution": result["raw_header_distribution"],
        "population_mapping": result["population_mapping"],
        "tag_pages": {k: len({e['document'] for e in v}) for k, v in result["tag_audit"]["tag_events"].items()},
        "tag_events": {k: len(v) for k, v in result["tag_audit"]["tag_events"].items()},
        "conformance_violations": result["tag_audit"]["conformance_violations"],
        "identifiability": result["identifiability"],
        "level_stats": result["resolved_level_stats"],
        "fold_support": result["accepted_fold_support"],
    }
    print(json.dumps(compact, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
