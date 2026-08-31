#!/usr/bin/env python3
"""Issue #58D Stage-A source/population audit.

This executable is deliberately incapable of computing pairwise occupancy
associations, residual graphs, graph energies, or cross-reading similarities.
It audits source identity, parser compatibility, frozen-leaf support, metadata,
and token-position support only.

Usage:
  python source_audit58d.py ZL3b-n.txt IT2a-n.txt GC2a-n.txt RETRIEVED_AT
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
sys.path.insert(0, str(EXPERIMENTS / "issue26-music"))
sys.path.insert(0, str(EXPERIMENTS / "occupancy-graph-stability"))
sys.path.insert(0, str(EXPERIMENTS / "phase63"))

import issue26e_core as e  # noqa: E402
import source_audit as sa  # noqa: E402
import phase63b_common as p63  # noqa: E402

IT_URL = "https://www.voynich.nu/data/IT2a-n.txt"
GC_URL = "https://www.voynich.nu/data/GC2a-n.txt"
HISTORICAL = {
    "IT2a": {
        "sha256": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
        "git_blob_sha1": "4d6d3f2537b1f507a257529b49c94af7d6e03446",
        "byte_size": 342104,
        "line_count": 5444,
        "header": "#=IVTFF EvaT 2.0 M 3",
        "alphabet": "EvaT",
    },
    "GC2a": {
        "sha256": "b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f",
        "git_blob_sha1": "8417a644fbd9c11cdaf85224f29cafee9ba1bdb0",
        "byte_size": 314916,
        "line_count": 5822,
        "header": "#=IVTFF v101 2.0 M 6",
        "alphabet": "v101",
    },
}
EXPECTED_ZL_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
META_GROUPS = ("AH", "BH", "BB", "BS")
POSITIONS = ("singleton", "initial", "interior", "final")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def source_identity(path: Path, label: str, url: str) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig", errors="strict")
    lines = text.splitlines()
    hist = HISTORICAL[label]
    got = {
        "url": url,
        "byte_size": len(raw),
        "line_count": len(lines),
        "sha256": sha256(raw),
        "git_blob_sha1": git_blob_sha1(raw),
        "header_lines": lines[:3],
        "header": lines[0].strip() if lines else "",
    }
    got["historical_authority"] = hist
    got["matches_phase63b_exact_bytes"] = (
        got["sha256"] == hist["sha256"]
        and got["git_blob_sha1"] == hist["git_blob_sha1"]
        and got["byte_size"] == hist["byte_size"]
        and got["line_count"] == hist["line_count"]
    )
    got["header_matches_expected_alphabet"] = got["header"].startswith(
        f"#=IVTFF {hist['alphabet']} "
    )
    return got


def parse_phase63_without_identity_gate(path: Path, alphabet: str):
    """Reproduce frozen Phase63B W1 parsing without enforcing the old hash."""
    out = []
    current = None
    current_page = None
    pid_by_page = {}
    audit = Counter()

    def close():
        nonlocal current
        if current is not None:
            out.append(current)
            current = None

    for rawline in path.read_text(encoding="utf-8-sig", errors="strict").splitlines():
        m = p63.LOCUS_RE.match(rawline)
        if not m:
            continue
        page, num, code, body = m.groups()
        if not p63.generic_is_p(code):
            continue
        audit["P_loci_seen"] += 1
        if current_page is not None and page != current_page:
            close()
        current_page = page
        start, end, tokens, excluded = p63.tokenize_body(body, alphabet, "W1")
        audit["excluded_uncertain_or_unreadable_tokens"] += excluded
        if start:
            close()
            pid_by_page[page] = pid_by_page.get(page, 0) + 1
            current = {
                "id": f"{page}:p{pid_by_page[page]}",
                "page": page,
                "leaf": p63.physical_leaf(page),
                "lines": [],
            }
            audit["paragraph_starts_consumed"] += 1
        if current is not None:
            if tokens:
                current["lines"].append(["".join(tok) for tok in tokens])
            if end:
                close()
        elif tokens:
            audit["ignored_nonempty_P_lines_outside_paragraph"] += 1
    close()
    return out, dict(audit)


def meta_group(lval, ival):
    if (lval, ival) == ("A", "H"):
        return "AH"
    if (lval, ival) == ("B", "H"):
        return "BH"
    if (lval, ival) == ("B", "B"):
        return "BB"
    if (lval, ival) == ("B", "S"):
        return "BS"
    return None


def position_category(index: int, n: int) -> str:
    if n == 1:
        return "singleton"
    if index == 0:
        return "initial"
    if index == n - 1:
        return "final"
    return "interior"


def audit_it2a(path: Path, frozen_folds, frozen_universe):
    identity = source_identity(path, "IT2a", IT_URL)
    text = path.read_text(encoding="utf-8-sig", errors="strict")
    pages, page_header_counts = sa.parse_page_metadata(text)
    items, p63_audit = parse_phase63_without_identity_gate(path, "EvaT")
    leaf_to_fold = {int(leaf): f for f, fold in enumerate(frozen_folds) for leaf in fold}
    parser = e.SlotParser()
    e.validate_parser(parser)

    total_clean = total_accepted = total_ambiguous = total_minmax_diff = 0
    overlap_clean = overlap_accepted = 0
    fold_accepted = [0] * 5
    fold_clean = [0] * 5
    observed_leaves = set()
    analyzed_pages = set()
    accepted_position = Counter()
    clean_position = Counter()
    accepted_group = Counter()
    clean_group = Counter()
    page_meta_missing = Counter()

    for item in items:
        leaf = item["leaf"]
        if leaf is None:
            continue
        leaf = int(leaf)
        observed_leaves.add(leaf)
        analyzed_pages.add(item["page"])
        meta = pages.get(item["page"], {})
        lval = meta.get("L", sa.MISSING)
        ival = meta.get("I", sa.MISSING)
        if lval == sa.MISSING:
            page_meta_missing["L"] += 1
        if ival == sa.MISSING:
            page_meta_missing["I"] += 1
        mg = meta_group(lval, ival)
        for line in item["lines"]:
            n = len(line)
            for idx, tok in enumerate(line):
                total_clean += 1
                pos = position_category(idx, n)
                clean_position[pos] += 1
                if mg:
                    clean_group[mg] += 1
                parses = parser.parses(tok)
                accepted = bool(parses)
                if len(parses) > 1:
                    total_ambiguous += 1
                if accepted:
                    total_accepted += 1
                    accepted_position[pos] += 1
                    if mg:
                        accepted_group[mg] += 1
                    if parses[0] != parses[-1]:
                        total_minmax_diff += 1
                if leaf in frozen_universe:
                    overlap_clean += 1
                    f = leaf_to_fold[leaf]
                    fold_clean[f] += 1
                    if accepted:
                        overlap_accepted += 1
                        fold_accepted[f] += 1

    shared = observed_leaves & frozen_universe
    only_it = observed_leaves - frozen_universe
    only_zl = frozen_universe - observed_leaves
    coverage = overlap_accepted / overlap_clean if overlap_clean else 0.0
    exact_identity = bool(identity["matches_phase63b_exact_bytes"])
    identity_ok = bool(identity["header_matches_expected_alphabet"])
    gates = {
        "identity_unambiguous_it2a_evat": identity_ok,
        "source_version_drift_understood": exact_identity,
        "phase63_parser_semantics_work_without_new_normalization": True,
        "parser_min_coverage_ge_0_60": coverage >= 0.60,
        "shared_leaves_ge_80": len(shared) >= 80,
        "each_fold_accepted_ge_300": all(x >= 300 for x in fold_accepted),
        "scientific_pair_or_residual_metrics_computed": False,
    }
    authorized = all([
        gates["identity_unambiguous_it2a_evat"],
        gates["source_version_drift_understood"],
        gates["phase63_parser_semantics_work_without_new_normalization"],
        gates["parser_min_coverage_ge_0_60"],
        gates["shared_leaves_ge_80"],
        gates["each_fold_accepted_ge_300"],
    ])
    return {
        "identity": identity,
        "phase63_w1_source_parser_audit": p63_audit,
        "population": {
            "paragraphs": len(items),
            "pages": len(analyzed_pages),
            "physical_leaves": len(observed_leaves),
            "clean_tokens": total_clean,
            "slot_parser_accepted_tokens": total_accepted,
            "slot_parser_rejected_tokens": total_clean - total_accepted,
            "slot_parser_coverage": total_accepted / total_clean if total_clean else 0.0,
            "ambiguous_tokens_more_than_one_legal_parse": total_ambiguous,
            "tokens_where_min_and_max_selected_parse_differ": total_minmax_diff,
        },
        "shared_universe": {
            "shared_physical_leaves": len(shared),
            "shared_leaf_numbers": sorted(shared),
            "only_it2a_leaf_numbers": sorted(only_it),
            "only_zl58c_leaf_numbers": sorted(only_zl),
            "clean_tokens_on_shared_leaves": overlap_clean,
            "accepted_tokens_on_shared_leaves": overlap_accepted,
            "slot_parser_coverage_on_shared_leaves": coverage,
            "fold_clean_tokens": fold_clean,
            "fold_accepted_tokens": fold_accepted,
        },
        "metadata": {
            "page_header_value_counts_L": dict(sorted(page_header_counts["L"].items())),
            "page_header_value_counts_I": dict(sorted(page_header_counts["I"].items())),
            "paragraphs_with_missing_page_metadata": dict(page_meta_missing),
            "clean_token_support_by_group": {g: int(clean_group[g]) for g in META_GROUPS},
            "accepted_token_support_by_group": {g: int(accepted_group[g]) for g in META_GROUPS},
        },
        "token_position": {
            "clean": {p: int(clean_position[p]) for p in POSITIONS},
            "accepted": {p: int(accepted_position[p]) for p in POSITIONS},
        },
        "authorization_gates": gates,
        "disposition": (
            "AUTHORIZED_FOR_TARGET_PLAN"
            if authorized
            else "SOURCE/REPRESENTATION AUDIT DOES NOT AUTHORIZE EXACT IT2A TARGET"
        ),
    }


def audit_gc2a(path: Path):
    identity = source_identity(path, "GC2a", GC_URL)
    text = path.read_text(encoding="utf-8-sig", errors="strict")
    pages, page_header_counts = sa.parse_page_metadata(text)
    items, p63_audit = parse_phase63_without_identity_gate(path, "v101")
    leaves = {int(item["leaf"]) for item in items if item["leaf"] is not None}
    clean_tokens = sum(len(line) for item in items for line in item["lines"])
    return {
        "identity": identity,
        "phase63_w1_source_parser_audit": p63_audit,
        "population": {
            "paragraphs": len(items),
            "pages": len({item["page"] for item in items}),
            "physical_leaves": len(leaves),
            "native_tokens": clean_tokens,
        },
        "metadata": {
            "page_header_value_counts_L": dict(sorted(page_header_counts["L"].items())),
            "page_header_value_counts_I": dict(sorted(page_header_counts["I"].items())),
        },
        "exact_12slot_target_status": "NOT_AUTHORIZED_BY_STAGE_A_PLAN_V101_MAPPING_WOULD_BE_REQUIRED",
    }


def main(zl_path: Path, it_path: Path, gc_path: Path, retrieved_at: str):
    zl_raw = zl_path.read_bytes()
    zl_blob = git_blob_sha1(zl_raw)
    if zl_blob != EXPECTED_ZL_BLOB:
        raise SystemExit(f"ZL source blob mismatch: {zl_blob} != {EXPECTED_ZL_BLOB}")
    zl_items = e.parse_voynich(zl_path)
    frozen_folds = [set(map(int, fold)) for fold in e.physical_leaf_folds(zl_items)]
    frozen_universe = set().union(*frozen_folds)
    if len(frozen_universe) != 99:
        raise SystemExit(f"unexpected frozen ZL leaf universe: {len(frozen_universe)}")

    out = {
        "issue": 66,
        "phase": "58D-StageA",
        "scope": "source_identity_population_parser_compatibility_only_no_pair_or_residual_scoring",
        "retrieved_at": retrieved_at,
        "frozen_reference": {
            "zl3b_git_blob_sha1": zl_blob,
            "physical_leaf_count": len(frozen_universe),
            "fold_leaf_sets": [sorted(f) for f in frozen_folds],
        },
        "IT2a": audit_it2a(it_path, frozen_folds, frozen_universe),
        "GC2a": audit_gc2a(gc_path),
        "scientific_pair_or_residual_metrics_computed": False,
        "forbidden_metric_names_absent_by_design": [
            "Yule_Q",
            "residual_Z",
            "residual_energy",
            "graph_correlation",
            "edge_sign_agreement",
            "target_p_value",
        ],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: source_audit58d.py ZL3b-n.txt IT2a-n.txt GC2a-n.txt RETRIEVED_AT"
        )
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4])
