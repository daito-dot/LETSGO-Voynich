#!/usr/bin/env python3
"""Issue #68 target-free preflight.

Allowed by PLAN_A before the first R1 reveal:
- reconstruct frozen A1/Naibbe primary outputs;
- freeze canonical surface digests and direct 12-slot parser coverage;
- verify historical R2/R3 authorities;
- evaluate Naibbe source-side R4 decoder closure;
- DO NOT compute any real-candidate pair Q, residual Z, energy, reliability,
  topology correlation/sign agreement, R1 p-value, or tournament result.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("phase62", "phase64", "issue26-music"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as b  # noqa: E402
import phase62c_c0_a1 as c  # noqa: E402
import phase62p_h62p1 as h62  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402

BASE_MAIN = "b2298d7fe251070dacd21852ae3b5a1dac95fe65"
EXPECTED_ZL_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_CREMMA = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_NAIBBE = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
EXPECTED_DECRYPT_BLOB = "b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b"
PHASE62C_FIRST_REVEAL_SHA = "1bd44579b7a57d43ea52ddf9d5bf59acb936b3f6fe7b7346010685c50f10bfb2"
PHASE62P_SHA = "0e1b687ab73efbc494834f49398ed474230f47bcde4cf4dbcaa46631efd75264"
COVERAGE_GATE = 0.60
A1_PRIMARY_SEEDS = (6195200, 6295200, 6395300, 6495300, 6595200)
NAIBBE_PRIMARY_SEEDS = (6480000, 6480100, 6480200, 6480300)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a, b_, tol=1e-12):
    return abs(float(a) - float(b_)) <= tol


def canonical_items_payload(items: Sequence[b.Item]) -> bytes:
    obj = []
    for it in items:
        obj.append({
            "item_id": it.item_id,
            "document": it.document,
            "leaf": it.leaf,
            "lines": [["".join(tok) for tok in line] for line in it.lines],
        })
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def surface_digest(items: Sequence[b.Item]) -> str:
    return hashlib.sha256(canonical_items_payload(items)).hexdigest()


def parser_coverage(items: Sequence[b.Item], parser: e.SlotParser):
    visible = accepted = 0
    item_counts = []
    for it in items:
        iv = ia = 0
        for line in it.lines:
            for tok_units in line:
                tok = "".join(tok_units)
                if not tok:
                    continue
                visible += 1
                iv += 1
                if parser.pick(tok, "min") is not None:
                    accepted += 1
                    ia += 1
        item_counts.append({"item_id": it.item_id, "visible": iv, "accepted": ia})
    return {
        "visible_tokens": visible,
        "accepted_tokens": accepted,
        "coverage": accepted / visible if visible else 0.0,
        "gate": COVERAGE_GATE,
        "passes_representation_compatibility": bool(visible and accepted / visible >= COVERAGE_GATE),
        "item_count": len(item_counts),
    }


def load_phase62c_first_reveal():
    path = EXPERIMENTS / "phase62" / "first-reveal" / "phase62c_c0_a1_results_run33313019008.json"
    got = sha256_file(path)
    if got != PHASE62C_FIRST_REVEAL_SHA:
        raise RuntimeError(f"Phase62C first-reveal SHA mismatch: {got}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_decrypt_module(root: Path):
    p = root / "decrypt_naibbe.py"
    got = b.git_blob_sha1(p.read_bytes())
    if got != EXPECTED_DECRYPT_BLOB:
        raise RuntimeError(f"decrypt_naibbe.py blob mismatch: {got}")
    spec = importlib.util.spec_from_file_location("issue68_pinned_naibbe_decrypt", p)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot construct pinned Naibbe decoder import")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if mod.BASIC is not True or mod.MARK_COMPOUND is not True:
        raise RuntimeError("pinned Naibbe decoder defaults changed")
    return mod


# ---------- Published decoder expression parser ----------
# Grammar emitted by decrypt_naibbe.py:
#   expr   := concat ('|' concat)*
#   concat := factor*
#   factor := LETTERS | '(' expr ')' | SPACE | '*'
# '[?]' means unresolved and produces no fully-resolved candidate.


def decode_expression_candidates(text: str) -> set[str]:
    if "[?]" in text:
        return set()
    i = 0

    def product(a: set[str], bset: set[str]) -> set[str]:
        return {x + y for x in a for y in bset}

    def parse_expr(stop: str | None = None) -> set[str]:
        nonlocal i
        alternatives: set[str] = set()
        current: set[str] = {""}
        while i < len(text):
            ch = text[i]
            if stop is not None and ch == stop:
                break
            if ch == "|":
                alternatives.update(current)
                current = {""}
                i += 1
                continue
            if ch == "(":
                i += 1
                sub = parse_expr(")")
                if i >= len(text) or text[i] != ")":
                    raise RuntimeError(f"unbalanced decoder expression: {text!r}")
                i += 1
                current = product(current, sub)
                continue
            if ch == ")":
                if stop != ")":
                    raise RuntimeError(f"unexpected ')' in decoder expression: {text!r}")
                break
            if ch.isspace() or ch == "*":
                i += 1
                continue
            if "a" <= ch.lower() <= "z":
                j = i
                while j < len(text) and "a" <= text[j].lower() <= "z":
                    j += 1
                lit = text[i:j].lower()
                current = {x + lit for x in current}
                i = j
                continue
            raise RuntimeError(f"unsupported decoder notation {ch!r} in {text!r}")
        alternatives.update(current)
        return alternatives

    out = parse_expr(None)
    if i != len(text):
        raise RuntimeError(f"decoder expression not fully consumed: {text!r} at {i}")
    return {x for x in out if x != ""}


def truth_in_token_product(token_candidates: Sequence[set[str]], truth: str) -> bool:
    positions = {0}
    for candidates in token_candidates:
        if not candidates:
            return False
        nxt = set()
        for pos in positions:
            for cand in candidates:
                if truth.startswith(cand, pos):
                    nxt.add(pos + len(cand))
        positions = nxt
        if not positions:
            return False
    return len(truth) in positions


def decoder_closure_for_realization(
    decrypt_mod,
    encoder_mod,
    naibbe_root: Path,
    source_items: Sequence[b.Item],
    cipher_items: Sequence[b.Item],
):
    table = pd.read_csv(naibbe_root / "references" / "naibbe_tables.csv")
    maps = decrypt_mod.build_reverse_mappings(table)
    source_by_id = {it.item_id: it for it in source_items}
    cipher_by_id = {it.item_id: it for it in cipher_items}
    if set(source_by_id) != set(cipher_by_id):
        raise RuntimeError("Naibbe source/cipher item-id mismatch")

    total = unique_exact = truth_contained = unresolved = ambiguous = unique_wrong = 0
    nonempty_truth = 0
    examples = {"unresolved": [], "ambiguous": [], "unique_wrong": [], "truth_not_contained": []}

    for item_id in sorted(source_by_id):
        src = source_by_id[item_id]
        cip = cipher_by_id[item_id]
        if len(src.lines) != len(cip.lines):
            raise RuntimeError(f"Naibbe source/cipher line-count mismatch: {item_id}")
        for li, (sline, cline) in enumerate(zip(src.lines, cip.lines)):
            source = n64.string_line(sline)
            published_cleaned = encoder_mod.clean_line(source)
            truth, _dropped = n64.project_effective_plaintext(published_cleaned)
            if truth:
                nonempty_truth += 1
            total += 1

            token_sets = []
            token_render = []
            for tok_units in cline:
                tok = "".join(tok_units)
                rendered = decrypt_mod.decrypt_naibbe_token(tok, *maps, basic=True, compound=True)
                candidates = decode_expression_candidates(rendered)
                token_render.append({"cipher": tok, "decoder": rendered, "n_candidates": len(candidates)})
                token_sets.append(candidates)

            has_unresolved = any(len(x) == 0 for x in token_sets)
            has_ambiguity = any(len(x) > 1 for x in token_sets)
            contained = truth_in_token_product(token_sets, truth) if token_sets else (truth == "")
            unique_stream = None
            if not has_unresolved and not has_ambiguity:
                unique_stream = "".join(next(iter(x)) for x in token_sets)
            exact = unique_stream == truth if unique_stream is not None else (truth == "" and not token_sets)

            if exact:
                unique_exact += 1
            if contained:
                truth_contained += 1
            if has_unresolved:
                unresolved += 1
            elif has_ambiguity:
                ambiguous += 1
            elif not exact:
                unique_wrong += 1

            row = {
                "item_id": item_id,
                "line": li,
                "truth_len": len(truth),
                "cipher_tokens": len(cline),
                "decoder_tokens": token_render,
            }
            if has_unresolved and len(examples["unresolved"]) < 3:
                examples["unresolved"].append(row)
            if (not has_unresolved and has_ambiguity) and len(examples["ambiguous"]) < 3:
                examples["ambiguous"].append(row)
            if (not has_unresolved and not has_ambiguity and not exact) and len(examples["unique_wrong"]) < 3:
                row["unique_stream_len"] = len(unique_stream or "")
                examples["unique_wrong"].append(row)
            if not contained and len(examples["truth_not_contained"]) < 3:
                examples["truth_not_contained"].append(row)

    return {
        "lines": total,
        "nonempty_truth_lines": nonempty_truth,
        "unique_exact_lines": unique_exact,
        "unique_exact_fraction": unique_exact / total if total else None,
        "truth_contained_lines": truth_contained,
        "truth_contained_fraction": truth_contained / total if total else None,
        "unresolved_lines": unresolved,
        "ambiguous_resolved_lines": ambiguous,
        "unique_wrong_lines": unique_wrong,
        "R4_primary_pass_100pct_unique_exact": bool(total and unique_exact == total),
        "examples": examples,
    }


def historical_r2_a1(phase62p: dict):
    counts = {"D_vs_N0": 0, "D_vs_C0": 0, "C_vs_N0": 0, "C_vs_C0": 0}
    for row in phase62p["folds"]:
        a = row["comparisons"]["A1"]
        n = row["comparisons"]["N0"]
        c0 = row["comparisons"]["C0"]
        counts["D_vs_N0"] += a["D_profile"] < n["D_profile"]
        counts["D_vs_C0"] += a["D_profile"] < c0["D_profile"]
        counts["C_vs_N0"] += a["abs_C_short_diff"] < n["abs_C_short_diff"]
        counts["C_vs_C0"] += a["abs_C_short_diff"] < c0["abs_C_short_diff"]
    return {"fold_wins": counts, "pass": all(v >= 4 for v in counts.values())}


def historical_r2_naibbe(phase64: dict):
    rows = phase64["published_mapping"]["primary_evaluation"]["folds"]
    counts = {"D_vs_N0": 0, "D_vs_C0": 0, "C_vs_N0": 0, "C_vs_C0": 0}
    for row in rows:
        a = row["candidate_H62_comparison"]
        n = row["baseline_H62_comparisons"]["N0"]
        c0 = row["baseline_H62_comparisons"]["C0"]
        counts["D_vs_N0"] += a["D_profile"] < n["D_profile"]
        counts["D_vs_C0"] += a["D_profile"] < c0["D_profile"]
        counts["C_vs_N0"] += a["abs_C_short_diff"] < n["abs_C_short_diff"]
        counts["C_vs_C0"] += a["abs_C_short_diff"] < c0["abs_C_short_diff"]
    return {"fold_wins": counts, "pass": all(v >= 4 for v in counts.values())}


def historical_r3_a1(phase62c_first: dict):
    cand = [float(x["A1"]["S1"]) for x in phase62c_first["folds"]]
    target = [float(x["heldout_voynich"]["S1"]) for x in phase62c_first["folds"]]
    ratio = float(np.mean(cand) / np.mean(target))
    positive = sum(x > 0 for x in cand)
    return {"candidate_fold_values": cand, "target_fold_values": target, "positive_folds": positive, "ratio_of_means": ratio, "pass": bool(positive >= 4 and 0.5 <= ratio <= 2.0)}


def historical_r3_naibbe(phase64: dict):
    rows = phase64["published_mapping"]["primary_evaluation"]["folds"]
    cand = [float(x["candidate_exposed"]["S1"]) for x in rows]
    target = [float(x["target_exposed"]["S1"]) for x in rows]
    ratio = float(np.mean(cand) / np.mean(target))
    positive = sum(x > 0 for x in cand)
    return {"candidate_fold_values": cand, "target_fold_values": target, "positive_folds": positive, "ratio_of_means": ratio, "pass": bool(positive >= 4 and 0.5 <= ratio <= 2.0)}


def generate_a1_primary(zl_path: Path, parser: e.SlotParser, phase62c_first: dict, phase62p: dict):
    if b.git_blob_sha1(zl_path.read_bytes()) != EXPECTED_ZL_BLOB:
        raise RuntimeError("A1 ZL3b source blob mismatch")
    vitems = b.parse_voynich(zl_path)
    folds = b.physical_leaf_folds(vitems)
    p61 = c.load_phase61_module()
    paragraphs, _ = p61.parse(str(zl_path))
    p61_folds = p61.physical_leaf_folds(paragraphs)
    if [sorted(x) for x in folds] != [sorted(x) for x in p61_folds]:
        raise RuntimeError("A1 Phase61/62 fold mismatch")
    vocab = sorted(set(p61.all_tokens(paragraphs)))
    neighbors = p61.build_neighbors(vocab)

    per_fold = []
    pooled = []
    for fi, test_leaves in enumerate(folds):
        strength, local_p = c.A1_PARAMS[fi]
        seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10
        if seed != A1_PRIMARY_SEEDS[fi]:
            raise RuntimeError(f"A1 seed mismatch fold {fi}: {seed}")
        train = p61.subset(paragraphs, test_leaves, include=False)
        test = p61.subset(paragraphs, test_leaves, include=True)
        shape_scores = p61.learn_shape_scores(train, vocab)
        entry_cum = p61.entry_cumulative(vocab, shape_scores, strength)
        generated = p61.generate_layout(test, vocab, neighbors, entry_cum, local_p, seed)
        items = c.convert_p61_paragraphs(generated)

        # Historical-identity checks are allowed preflight; no R1 pair statistic.
        train_items = b.by_leaves(vitems, test_leaves, include=False)
        sd = b.training_sd(train_items)
        direction = np.mean(b.contrasts(train_items, sd), axis=0)
        direction = direction / float(np.linalg.norm(direction))
        s1, _n, _delta = b.s1_projection(items, sd, direction)
        old_s1 = phase62c_first["folds"][fi]["A1_replicates"][0]["S1"]
        if not close(s1, old_s1):
            raise RuntimeError(f"A1 rep0 historical S1 mismatch fold {fi}: {s1} != {old_s1}")
        prof = h62.raw_profile(items, f"A1:fold{fi}:rep0")
        old_prof = phase62p["folds"][fi]["A1_realizations"]["rep0"]
        if prof != old_prof:
            raise RuntimeError(f"A1 rep0 historical H62 profile mismatch fold {fi}")

        cov = parser_coverage(items, parser)
        per_fold.append({"fold": fi, "seed": seed, "surface_sha256": surface_digest(items), "coverage": cov, "historical_S1_rep0": float(s1), "historical_H62_rep0_exact": True})
        pooled.extend(items)
    return {"primary_seeds": list(A1_PRIMARY_SEEDS), "per_fold": per_fold, "pooled_surface_sha256": surface_digest(pooled), "pooled_coverage": parser_coverage(pooled, parser)}


def generate_naibbe_primary(cremma_root: Path, naibbe_root: Path, parser: e.SlotParser, phase64: dict):
    if b.verify_cremma_commit(cremma_root) != EXPECTED_CREMMA:
        raise RuntimeError("CREMMA authority mismatch")
    module = n64.load_naibbe(naibbe_root)
    if n64.NAIBBE_COMMIT != EXPECTED_NAIBBE:
        raise RuntimeError("Naibbe implementation authority mismatch")
    decrypt_mod = load_decrypt_module(naibbe_root)
    original_map = dict(module.placeholder_to_glyph)
    sources = {name: b.parse_latin_manuscript(cremma_root, name, rel) for name, rel in b.PRIMARY_MANUSCRIPTS.items()}
    frozen_diag = phase64["published_mapping"]["generation"]["encryption_diagnostics"]

    rows = []
    pooled = []
    closure_totals = []
    for mi, manuscript in enumerate(n64.MANUSCRIPTS):
        seed = 6480000 + 100 * mi
        if seed != NAIBBE_PRIMARY_SEEDS[mi]:
            raise RuntimeError(f"Naibbe seed mismatch {manuscript}: {seed}")
        primary, _raw, diag = n64.encrypt_manuscript(module, sources[manuscript], manuscript, original_map, seed)
        if diag != frozen_diag[manuscript]["rep0"]:
            raise RuntimeError(f"Naibbe rep0 diagnostics differ from frozen Phase64B: {manuscript}")
        cov = parser_coverage(primary, parser)
        closure = decoder_closure_for_realization(decrypt_mod, module, naibbe_root, sources[manuscript], primary)
        rows.append({"manuscript": manuscript, "seed": seed, "surface_sha256": surface_digest(primary), "coverage": cov, "generation_diagnostics_exact": True, "decoder_closure": closure})
        pooled.extend(primary)
        closure_totals.append(closure)

    total = sum(x["lines"] for x in closure_totals)
    exact = sum(x["unique_exact_lines"] for x in closure_totals)
    contained = sum(x["truth_contained_lines"] for x in closure_totals)
    unresolved = sum(x["unresolved_lines"] for x in closure_totals)
    ambiguous = sum(x["ambiguous_resolved_lines"] for x in closure_totals)
    wrong = sum(x["unique_wrong_lines"] for x in closure_totals)
    aggregate_closure = {
        "lines": total,
        "unique_exact_lines": exact,
        "unique_exact_fraction": exact / total if total else None,
        "truth_contained_lines": contained,
        "truth_contained_fraction": contained / total if total else None,
        "unresolved_lines": unresolved,
        "ambiguous_resolved_lines": ambiguous,
        "unique_wrong_lines": wrong,
        "R4_primary_pass_100pct_unique_exact": bool(total and exact == total),
    }
    return {"primary_seeds": list(NAIBBE_PRIMARY_SEEDS), "per_manuscript": rows, "pooled_surface_sha256": surface_digest(pooled), "pooled_coverage": parser_coverage(pooled, parser), "R4_primary_rep0_aggregate": aggregate_closure}


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT NAIBBE_ROOT")
    zl_path, cremma_root, naibbe_root = map(lambda x: Path(x).resolve(), sys.argv[1:])

    phase62c_first = load_phase62c_first_reveal()
    p62path = EXPERIMENTS / "phase62" / "phase62p_h62p1_results.json"
    if sha256_file(p62path) != PHASE62P_SHA:
        raise RuntimeError("Phase62P exact authority SHA mismatch")
    phase62p = json.loads(p62path.read_text(encoding="utf-8"))
    phase64 = json.loads((EXPERIMENTS / "phase64" / "phase64b_science_results.json").read_text(encoding="utf-8"))
    if phase64["inputs"]["naibbe_commit"] != EXPECTED_NAIBBE or phase64["inputs"]["cremma_commit"] != EXPECTED_CREMMA:
        raise RuntimeError("Phase64B recorded input authority mismatch")
    if phase64["frozen_primary_classification"] != "C1-E0 PARTIAL":
        raise RuntimeError("unexpected frozen Phase64B classification")

    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)

    a1 = generate_a1_primary(zl_path, parser, phase62c_first, phase62p)
    naibbe = generate_naibbe_primary(cremma_root, naibbe_root, parser, phase64)

    historical = {
        "A1": {"R2": historical_r2_a1(phase62p), "R3": historical_r3_a1(phase62c_first)},
        "Naibbe_C1_E0": {"R2": historical_r2_naibbe(phase64), "R3": historical_r3_naibbe(phase64)},
    }

    result = {
        "phase": "Issue68-preflight",
        "base_main": BASE_MAIN,
        "target_reveal": False,
        "real_candidate_pair_or_residual_metrics_computed": False,
        "forbidden_R1_quantities": {"pair_Q": False, "residual_Z": False, "residual_energy": False, "reliability_W": False, "target_topology": False, "R1_p_values": False, "joint_classification": False},
        "parser": {"authority": "experiments/issue26-music/issue26e_core.py::SlotParser", "policy": "min", "gate": COVERAGE_GATE, "validation": parser_validation},
        "A1_primary": a1,
        "Naibbe_primary": naibbe,
        "historical_frozen_responsibilities": historical,
        "preflight_dispositions": {
            "A1_R1_representation": "AUTHORIZED_FOR_R1_REVEAL" if a1["pooled_coverage"]["passes_representation_compatibility"] else "FAIL_REPRESENTATION_COMPATIBILITY",
            "Naibbe_R1_representation": "AUTHORIZED_FOR_R1_REVEAL" if naibbe["pooled_coverage"]["passes_representation_compatibility"] else "FAIL_REPRESENTATION_COMPATIBILITY",
            "Naibbe_R4_primary": "PASS" if naibbe["R4_primary_rep0_aggregate"]["R4_primary_pass_100pct_unique_exact"] else "FAIL",
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
