#!/usr/bin/env python3
"""Issue #104 Phase 3A Gate 0: score-free Currier A/B authority/support audit."""
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
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
PAGE_HEADER_RE = re.compile(r"^<(?P<doc>(?:f|m)\d+[rv]\d?)>\s+<!\s*(?P<meta>.*?)>")
FIELD_RE = re.compile(r"\$(?P<key>[A-Za-z])=(?P<value>[^\s>]+)")
CURRIER_COMMENT_RE = re.compile(r"Currier(?:'|’)?s\s+language\s+([AB])\b", re.IGNORECASE)
LEAF_RE = re.compile(r"^[fm](\d+)")


def load_phase1():
    spec = importlib.util.spec_from_file_location("issue104_phase1_loader", PHASE1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import frozen Phase-1 loader")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


P1 = load_phase1()


def source_blob_sha1(path: Path) -> str:
    return P1.I.b.git_blob_sha1(path.read_bytes())


def parse_source_headers(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    records = []
    seen = set()
    for i, line in enumerate(lines):
        m = PAGE_HEADER_RE.match(line)
        if not m:
            continue
        doc = m.group("doc")
        if doc in seen:
            raise RuntimeError(f"duplicate page header: {doc}")
        seen.add(doc)
        fields = {x.group("key"): x.group("value") for x in FIELD_RE.finditer(m.group("meta"))}
        label_raw = fields.get("L")
        comments = []
        j = i + 1
        while j < len(lines) and not PAGE_HEADER_RE.match(lines[j]):
            s = lines[j]
            if s.startswith("#"):
                comments.append(s[1:].strip())
            if s.startswith("<"):
                break
            j += 1
        comment_labels = []
        for c in comments:
            cm = CURRIER_COMMENT_RE.search(c)
            if cm:
                comment_labels.append(cm.group(1).upper())
        unique_comments = sorted(set(comment_labels))
        if label_raw in ("A", "B"):
            label = label_raw
            label_source = "HEADER_L"
        elif label_raw is None and len(unique_comments) == 1:
            label = unique_comments[0]
            label_source = "COMMENT_FALLBACK_MISSING_L"
        else:
            label = "UNKNOWN_OTHER"
            label_source = "UNKNOWN_OTHER"
        lm = LEAF_RE.match(doc)
        if not lm:
            raise RuntimeError(f"cannot parse numeric leaf from source document {doc}")
        records.append({
            "document": doc,
            "leaf": int(lm.group(1)),
            "fields": fields,
            "L_raw": label_raw,
            "label": label,
            "label_source": label_source,
            "comment_labels": comment_labels,
            "source_line": i + 1,
        })
    if not records:
        raise RuntimeError("no ZL3b page headers parsed")
    return records


def count_item(it, parsed):
    visible = sum(len(line) for line in it.lines)
    accepted = sum(seq is not None for line in parsed[it.item_id] for seq in line)
    return int(visible), int(accepted)


def audit(zl_path: Path):
    if source_blob_sha1(zl_path) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b source differs from frozen authority")

    headers = parse_source_headers(zl_path)
    by_doc = {r["document"]: r for r in headers}
    label_header_counts = Counter(r["label"] for r in headers)
    label_source_counts = Counter(r["label_source"] for r in headers)
    raw_L_counts = Counter("<MISSING>" if r["L_raw"] is None else r["L_raw"] for r in headers)

    comment_checks = 0
    comment_mismatches = []
    fallback_records = []
    for r in headers:
        if r["label_source"] == "COMMENT_FALLBACK_MISSING_L":
            fallback_records.append({
                "document": r["document"],
                "label": r["label"],
                "comment_labels": r["comment_labels"],
                "source_line": r["source_line"],
            })
        unique_comments = sorted(set(r["comment_labels"]))
        if len(unique_comments) > 1:
            comment_mismatches.append({
                "document": r["document"],
                "reason": "MULTIPLE_CONFLICTING_CURRIER_COMMENTS",
                "L_raw": r["L_raw"],
                "comment_labels": unique_comments,
            })
        for c in r["comment_labels"]:
            comment_checks += 1
            if r["L_raw"] in ("A", "B") and c != r["L_raw"]:
                comment_mismatches.append({
                    "document": r["document"],
                    "reason": "HEADER_COMMENT_CONFLICT",
                    "L_raw": r["L_raw"],
                    "parsed_label": r["label"],
                    "comment_label": c,
                })
            elif r["L_raw"] not in (None, "A", "B"):
                comment_mismatches.append({
                    "document": r["document"],
                    "reason": "NON_AB_HEADER_WITH_CURRIER_COMMENT",
                    "L_raw": r["L_raw"],
                    "parsed_label": r["label"],
                    "comment_label": c,
                })

    order_config = OA.configure(zl_path)
    items, folds, parsed = P1.I.C.load_corpus(zl_path)
    order_verify = OA.verify(items)
    if len(folds) != P1.N_FOLDS:
        raise RuntimeError("frozen fold count changed")

    missing_headers = sorted({it.document for it in items if it.document not in by_doc})
    if missing_headers:
        raise RuntimeError(f"parsed documents absent from source header authority: {missing_headers}")

    item_stats = defaultdict(lambda: {"items": 0, "visible_tokens": 0, "accepted_tokens": 0, "documents": set(), "leaves": set()})
    labels_by_leaf = defaultdict(set)
    docs_by_leaf = defaultdict(set)
    for it in items:
        lab = by_doc[it.document]["label"]
        v, a = count_item(it, parsed)
        s = item_stats[lab]
        s["items"] += 1
        s["visible_tokens"] += v
        s["accepted_tokens"] += a
        s["documents"].add(it.document)
        s["leaves"].add(int(it.leaf))
        docs_by_leaf[int(it.leaf)].add(it.document)
        if lab in ("A", "B"):
            labels_by_leaf[int(it.leaf)].add(lab)

    mixed_leaves = sorted(leaf for leaf, labs in labels_by_leaf.items() if labs == {"A", "B"})
    mixed_set = set(mixed_leaves)

    leaf_classes = {"A_ONLY": [], "B_ONLY": [], "MIXED_AB": [], "UNKNOWN_OTHER_ONLY_OR_PRESENT": []}
    for leaf in sorted(docs_by_leaf):
        labs_all = {by_doc[d]["label"] for d in docs_by_leaf[leaf]}
        ab = labs_all & {"A", "B"}
        unknown = "UNKNOWN_OTHER" in labs_all
        if ab == {"A", "B"}:
            leaf_classes["MIXED_AB"].append(leaf)
        elif ab == {"A"} and not unknown:
            leaf_classes["A_ONLY"].append(leaf)
        elif ab == {"B"} and not unknown:
            leaf_classes["B_ONLY"].append(leaf)
        else:
            leaf_classes["UNKNOWN_OTHER_ONLY_OR_PRESENT"].append(leaf)

    fold_of_leaf = {}
    for f, leafset in enumerate(folds):
        for leaf in leafset:
            if int(leaf) in fold_of_leaf:
                raise RuntimeError(f"leaf {leaf} occurs in multiple frozen folds")
            fold_of_leaf[int(leaf)] = int(f)

    eligible_fold = {
        lab: {str(f): {"leaves": set(), "items": 0, "visible_tokens": 0, "accepted_tokens": 0, "documents": set()} for f in range(P1.N_FOLDS)}
        for lab in ("A", "B")
    }
    excluded = {"mixed_leaf": {"items": 0, "visible_tokens": 0, "accepted_tokens": 0}, "unknown_other": {"items": 0, "visible_tokens": 0, "accepted_tokens": 0}}

    for it in items:
        lab = by_doc[it.document]["label"]
        v, a = count_item(it, parsed)
        leaf = int(it.leaf)
        if leaf in mixed_set:
            excluded["mixed_leaf"]["items"] += 1
            excluded["mixed_leaf"]["visible_tokens"] += v
            excluded["mixed_leaf"]["accepted_tokens"] += a
            continue
        if lab not in ("A", "B"):
            excluded["unknown_other"]["items"] += 1
            excluded["unknown_other"]["visible_tokens"] += v
            excluded["unknown_other"]["accepted_tokens"] += a
            continue
        if leaf not in fold_of_leaf:
            raise RuntimeError(f"eligible leaf {leaf} absent from frozen folds")
        f = str(fold_of_leaf[leaf])
        s = eligible_fold[lab][f]
        s["leaves"].add(leaf)
        s["documents"].add(it.document)
        s["items"] += 1
        s["visible_tokens"] += v
        s["accepted_tokens"] += a

    def freeze_sets(obj):
        out = {}
        for k, v in obj.items():
            if isinstance(v, set):
                out[k] = sorted(v)
            else:
                out[k] = v
        return out

    eligible_fold_json = {
        lab: {f: freeze_sets(stats) for f, stats in fs.items()}
        for lab, fs in eligible_fold.items()
    }
    all_target_folds_nonzero = {
        lab: all(eligible_fold_json[lab][str(f)]["accepted_tokens"] > 0 for f in range(P1.N_FOLDS))
        for lab in ("A", "B")
    }

    item_stats_json = {}
    for lab, s in item_stats.items():
        item_stats_json[lab] = {
            "documents": len(s["documents"]),
            "leaves": len(s["leaves"]),
            "items": int(s["items"]),
            "visible_tokens": int(s["visible_tokens"]),
            "accepted_tokens": int(s["accepted_tokens"]),
        }

    gate_pass = bool(
        not comment_mismatches
        and order_verify["numeric_paragraph_order_valid"]
        and order_verify["source_document_order_valid"]
        and all(all_target_folds_nonzero.values())
    )

    return {
        "schema": "issue104-phase3a-currier-gate0-v2-amendment-a",
        "phase": "ISSUE104_PHASE3A_GATE0",
        "gate_pass": gate_pass,
        "gate_rule": "PROCEED_TO_FROZEN_CURRIER_TRANSPORT" if gate_pass else "STOP_BEFORE_PREDICTIVE_SCORING",
        "source": {
            "git_blob_sha1": source_blob_sha1(zl_path),
            "sha256": hashlib.sha256(zl_path.read_bytes()).hexdigest(),
            "page_header_count": len(headers),
        },
        "header_metadata": {
            "raw_L_distribution": dict(sorted(raw_L_counts.items())),
            "phase3a_label_distribution": dict(sorted(label_header_counts.items())),
            "label_source_distribution": dict(sorted(label_source_counts.items())),
            "comment_fallback_records": fallback_records,
            "currier_comment_checks": int(comment_checks),
            "currier_comment_mismatches": comment_mismatches,
            "amendment_A_applied": True,
        },
        "parsed_population_by_label": dict(sorted(item_stats_json.items())),
        "leaf_classes": leaf_classes,
        "mixed_AB_leaves_excluded": mixed_leaves,
        "eligible_by_label_and_frozen_fold": eligible_fold_json,
        "all_target_folds_nonzero": all_target_folds_nonzero,
        "excluded_population": excluded,
        "order_authority": {**order_config, **order_verify},
        "fold_identity_sha256": P1.P0.fold_hash(folds),
        "firewall": {
            "predictive_scores_computed": False,
            "surface_target_metrics_scored": False,
            "issue84_target_used": False,
            "semantic_or_image_context_used": False,
            "hand_section_scribe_used": False,
            "latent_state_fitted": False,
        },
    }


def self_test():
    sample = "<f1r> <! $Q=A $L=A $H=1>\n# Currier's Language A, hand 1\n<f1r.1,@P0> <%>abc\n<f2v> <! $Q=B $H=2>\n# Currier's language B, hand 2\n"
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "x.txt"
        p.write_text(sample, encoding="utf-8")
        rows = parse_source_headers(p)
    assert [r["label"] for r in rows] == ["A", "B"]
    assert rows[0]["label_source"] == "HEADER_L"
    assert rows[1]["label_source"] == "COMMENT_FALLBACK_MISSING_L"
    assert rows[0]["comment_labels"] == ["A"]
    assert rows[1]["comment_labels"] == ["B"]
    return {
        "ok": True,
        "score_free": True,
        "header_L_parser": True,
        "missing_L_comment_fallback": True,
        "comment_consistency_parser": True,
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
    print(json.dumps({
        "gate_pass": result["gate_pass"],
        "gate_rule": result["gate_rule"],
        "header_metadata": result["header_metadata"],
        "parsed_population_by_label": result["parsed_population_by_label"],
        "leaf_classes": result["leaf_classes"],
        "all_target_folds_nonzero": result["all_target_folds_nonzero"],
        "eligible_by_label_and_frozen_fold": result["eligible_by_label_and_frozen_fold"],
        "excluded_population": result["excluded_population"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
