#!/usr/bin/env python3
"""Phase64B frozen external C1-E0 evaluation.

Evaluates the exact published Naibbe v2 cipher, pinned outside this project,
on the already frozen four-manuscript CREMMA Latin panel. No Naibbe parameter
or variant is selected from Voynich outcomes.

Usage:
  python experiments/phase64/phase64b_naibbe.py \
    ZL3b-n.txt /path/to/CREMMA-Medieval-LAT /path/to/naibbe-cipher
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import random
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
PHASE62 = HERE.parent / "phase62"
PHASE63 = HERE.parent / "phase63"
for path in (PHASE62, PHASE63):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import phase62b_n0 as b  # noqa: E402
import phase62p_h62p1 as p  # noqa: E402

NAIBBE_COMMIT = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
NAIBBE_PY_BLOB = "b566ad82e4b6ff0782ecdddebf77718dac44f292"
NAIBBE_TABLE_BLOB = "5cd34fb81d80faf3b4d57dbf1719c05ffde25302"
NAIBBE_README_BLOB = "486782221285186c0f78dd9474b676e067cd4bea"
PHASE62P_SHA256 = "0e1b687ab73efbc494834f49398ed474230f47bcde4cf4dbcaa46631efd75264"
PHASE63A_SHA256 = "bcd05d1823e17b034c0abf984a0af9b0cb31b5a37bd9e604c327ab9aff1937a7"

MANUSCRIPTS = tuple(b.PRIMARY_MANUSCRIPTS)
CIPHER_REPS = 5
MAPPING_PERMS = 5
TIE_EPS = 1e-12
EFFECTIVE_LETTERS = tuple(x for x in "abcdefghijklmnopqrstuvwxyz" if x not in {"j", "k", "w"})


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_git_head(root: Path, expected: str, label: str) -> str:
    import subprocess
    got = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if got != expected:
        raise RuntimeError(f"{label} commit mismatch: {got} != {expected}")
    return got


def verify_blob(path: Path, expected: str, label: str) -> str:
    got = b.git_blob_sha1(path.read_bytes())
    if got != expected:
        raise RuntimeError(f"{label} blob mismatch: {got} != {expected}")
    return got


def load_naibbe(root: Path):
    verify_git_head(root, NAIBBE_COMMIT, "Naibbe")
    verify_blob(root / "naibbe_v2.py", NAIBBE_PY_BLOB, "naibbe_v2.py")
    verify_blob(root / "references" / "naibbe_tables.csv", NAIBBE_TABLE_BLOB, "naibbe_tables.csv")
    verify_blob(root / "README.md", NAIBBE_README_BLOB, "Naibbe README")

    old = Path.cwd()
    try:
        os.chdir(root)
        spec = importlib.util.spec_from_file_location("phase64b_external_naibbe_v2", root / "naibbe_v2.py")
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot construct Naibbe import spec")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        os.chdir(old)

    expected = {
        "RESPACING": 17,
        "USE_78_CARD_DECK": True,
        "SPACE_REMOVAL_RATE": 0.03,
        "UNAMBIGUOUS": True,
        "MAX_BIGRAM_RETRIES": 10000,
    }
    for key, want in expected.items():
        got = getattr(module, key)
        if got != want:
            raise RuntimeError(f"published Naibbe default changed: {key}={got!r} != {want!r}")
    if list(module.TABLES) != ["alpha", "beta1", "beta2", "beta3", "gamma1", "gamma2"]:
        raise RuntimeError("published Naibbe table order changed")
    if list(module.STATES) != ["unigram", "prefix", "suffix"]:
        raise RuntimeError("published Naibbe state order changed")
    if list(module.ALPHABET) != list("abcdefghijklmnopqrstuvwxyz"):
        raise RuntimeError("published Naibbe alphabet changed")
    if module.CARD_WEIGHTS[True] != {
        "alpha": 28, "beta1": 14, "beta2": 11, "beta3": 11, "gamma1": 7, "gamma2": 7
    }:
        raise RuntimeError("published Naibbe 78-card weights changed")
    return module


def set_glyph_map(module, glyph_map: Dict[str, str]) -> None:
    module.placeholder_to_glyph = dict(glyph_map)
    module.unigram_glyphs = {
        glyph for code, glyph in module.placeholder_to_glyph.items()
        if code.startswith("unigram_")
    }
    module.bigram_catalog = module.build_bigram_catalog(
        module.ALPHABET, module.TABLES, module.placeholder_to_glyph
    )


def permuted_mapping(module, original: Dict[str, str], seed: int) -> Dict[str, str]:
    out = dict(original)
    rng = random.Random(seed)
    for state in module.STATES:
        codes = [
            f"{state}_{table}_{letter}"
            for table in module.TABLES
            for letter in EFFECTIVE_LETTERS
        ]
        if any(code not in original for code in codes):
            missing = [code for code in codes if code not in original]
            raise RuntimeError(f"Naibbe effective code cells missing: {missing[:5]}")
        values = [original[code] for code in codes]
        rng.shuffle(values)
        for code, value in zip(codes, values):
            out[code] = value
    return out


def string_line(line: b.Line) -> str:
    return " ".join("".join(tok) for tok in line)


def glyph_line(tokens: Sequence[str]) -> b.Line:
    return [tuple(x) for x in tokens if x]


def project_effective_plaintext(published_cleaned: str) -> Tuple[str, List[str]]:
    """Project published clean_line output onto Naibbe's reachable alphabet.

    The pinned external clean_line uses Unicode isalpha(), so source-native
    medieval alphabetic glyphs can survive even though the published codebook
    has no cell for them. B3 freezes a generic drop-only interface projection:
    no transliteration or expansion is invented here.
    """
    allowed = set(EFFECTIVE_LETTERS)
    dropped = [ch for ch in published_cleaned if ch not in allowed]
    return "".join(ch for ch in published_cleaned if ch in allowed), dropped


def encrypt_manuscript(
    module,
    source_items: Sequence[b.Item],
    manuscript: str,
    glyph_map: Dict[str, str],
    seed: int,
) -> Tuple[List[b.Item], List[b.Item], dict]:
    set_glyph_map(module, glyph_map)
    random.seed(seed)
    module.ambiguity_retries = 0

    primary: List[b.Item] = []
    raw: List[b.Item] = []
    source_units = 0
    published_clean_chars = 0
    cleaned_chars = 0
    dropped_unsupported_chars = 0
    dropped_unsupported_types = set()
    nonempty_source_lines = 0
    nonempty_cleaned_lines = 0
    primary_tokens = 0
    raw_tokens = 0

    for item in source_items:
        p_lines: List[b.Line] = []
        r_lines: List[b.Line] = []
        for line in item.lines:
            source = string_line(line)
            source_units += sum(len(tok) for tok in line)
            if source:
                nonempty_source_lines += 1
            published_cleaned = module.clean_line(source)
            published_clean_chars += len(published_cleaned)
            cleaned, dropped = project_effective_plaintext(published_cleaned)
            dropped_unsupported_chars += len(dropped)
            dropped_unsupported_types.update(dropped)
            cleaned_chars += len(cleaned)
            if cleaned:
                nonempty_cleaned_lines += 1
                encrypted = module.encrypt_naibbe(
                    cleaned,
                    module.naibbe_tables,
                    glyph_map,
                    use_78=module.USE_78_CARD_DECK,
                    pre_plaintext_file=None,
                )
                line_out = " ".join(encrypted)
                # Always consume the published respacing RNG after encryption.
                respaced = module.respace_line(line_out, module.SPACE_REMOVAL_RATE)
                rline = glyph_line(encrypted)
                pline = glyph_line(respaced.split())
            else:
                # Empty line has no respacing RNG calls in the published script.
                rline = []
                pline = []
            raw_tokens += len(rline)
            primary_tokens += len(pline)
            r_lines.append(rline)
            p_lines.append(pline)
        raw.append(b.Item(item.item_id, manuscript, r_lines, None))
        primary.append(b.Item(item.item_id, manuscript, p_lines, None))

    return primary, raw, {
        "seed": seed,
        "source_items": len(source_items),
        "source_graphematic_units": source_units,
        "published_clean_line_characters": published_clean_chars,
        "dropped_unsupported_after_clean_line": dropped_unsupported_chars,
        "dropped_unsupported_character_types": sorted(dropped_unsupported_types),
        "cleaned_plaintext_characters": cleaned_chars,
        "cleaned_to_source_unit_ratio": float(cleaned_chars / source_units) if source_units else None,
        "nonempty_source_lines": nonempty_source_lines,
        "nonempty_cleaned_lines": nonempty_cleaned_lines,
        "primary_cipher_tokens": primary_tokens,
        "raw_cipher_tokens": raw_tokens,
        "ambiguity_retries": int(module.ambiguity_retries),
    }


def fold_contexts(voynich_path: Path, phase62c: dict, phase63a: dict) -> Tuple[List[dict], List[b.Item]]:
    if b.git_blob_sha1(voynich_path.read_bytes()) != b.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b authority blob mismatch")
    vitems = b.parse_voynich(voynich_path)
    folds = b.physical_leaf_folds(vitems)
    if len(folds) != 5:
        raise RuntimeError(f"expected five Voynich folds, got {len(folds)}")
    out = []
    for fi, leaves in enumerate(folds):
        cfold = phase62c["folds"][fi]
        afold = phase63a["folds"][fi]
        if cfold["fold"] != fi or afold["fold"] != fi:
            raise RuntimeError(f"fold authority order mismatch at {fi}")
        if sorted(cfold["test_leaves"]) != sorted(leaves) or sorted(afold["test_leaves"]) != sorted(leaves):
            raise RuntimeError(f"fold leaf authority mismatch at {fi}")
        train = b.by_leaves(vitems, leaves, include=False)
        sd = b.training_sd(train)
        dtrain = b.contrasts(train, sd)
        if len(dtrain) == 0:
            raise RuntimeError(f"fold {fi}: no training S1 contrasts")
        direction = np.mean(dtrain, axis=0)
        norm = float(np.linalg.norm(direction))
        if norm == 0:
            raise RuntimeError(f"fold {fi}: zero S1 direction")
        direction /= norm
        out.append({
            "fold": fi,
            "test_leaves": sorted(leaves),
            "sd": sd,
            "direction": direction,
            "target_exposed": cfold["heldout_voynich"],
            "target_H62P1": afold["heldout_voynich_H62P1"],
            "baseline_H62": {
                "N0": afold["committed_baseline_comparisons"]["N0"],
                "C0": afold["committed_baseline_comparisons"]["C0"],
                "A1_R1": afold["A1_R1_comparison"],
            },
        })
    return out, vitems


def output_metrics(items: Sequence[b.Item], label: str, contexts: Sequence[dict]) -> dict:
    s2 = b.s2_locality(items, label)
    s3 = b.s3_line_position(items)
    if s3["mean_eta2"] is None:
        raise RuntimeError(f"{label}: S3 unavailable")
    prof = p.raw_profile(items, label)
    s1 = {}
    for ctx in contexts:
        value, n, delta = b.s1_projection(items, ctx["sd"], ctx["direction"])
        if value is None:
            raise RuntimeError(f"{label}: S1 unavailable in fold {ctx['fold']}")
        s1[str(ctx["fold"])] = {
            "value": float(value),
            "n_items": n,
            "mean_delta8": delta,
        }
    return {
        "S1_by_fold": s1,
        "S2": float(s2["excess"]),
        "S2_detail": s2,
        "S3": float(s3["mean_eta2"]),
        "S3_detail": s3,
        "H62P1": prof,
    }


def aggregate_realizations(realizations: Dict[str, dict], label: str) -> dict:
    if not realizations:
        raise RuntimeError(f"{label}: no realizations")
    fold_ids = sorted(next(iter(realizations.values()))["S1_by_fold"], key=int)
    s1 = {
        f: float(np.mean([row["S1_by_fold"][f]["value"] for row in realizations.values()]))
        for f in fold_ids
    }
    profile = p.aggregate_excess(
        {name: row["H62P1"] for name, row in realizations.items()},
        f"{label}:mean-E",
        "cipher realization",
    )
    return {
        "S1_by_fold": s1,
        "S2": float(np.mean([row["S2"] for row in realizations.values()])),
        "S3": float(np.mean([row["S3"] for row in realizations.values()])),
        "H62P1": profile,
    }


def aggregate_manuscripts(per_ms: Dict[str, dict], label: str) -> dict:
    if set(per_ms) != set(MANUSCRIPTS):
        raise RuntimeError(f"{label}: manuscript panel mismatch: {sorted(per_ms)}")
    fold_ids = sorted(next(iter(per_ms.values()))["S1_by_fold"], key=int)
    s1 = {
        f: float(np.mean([row["S1_by_fold"][f] for row in per_ms.values()]))
        for f in fold_ids
    }
    profile = p.aggregate_excess(
        {name: row["H62P1"] for name, row in per_ms.items()},
        f"{label}:equal-manuscript-E",
        "manuscript",
    )
    return {
        "S1_by_fold": s1,
        "S2": float(np.mean([row["S2"] for row in per_ms.values()])),
        "S3": float(np.mean([row["S3"] for row in per_ms.values()])),
        "H62P1": profile,
    }


def strict_wins(a: Sequence[float], bvals: Sequence[float]) -> int:
    return sum(x + TIE_EPS < y for x, y in zip(a, bvals))


def joint_relative_mse(fold_metrics: Sequence[dict]) -> float:
    rows = []
    for row in fold_metrics:
        target = row["target_exposed"]
        candidate = row["candidate_exposed"]
        vals = []
        for k in ("S1", "S2", "S3"):
            if target[k] <= TIE_EPS:
                raise RuntimeError(f"non-positive target {k} in joint MSE")
            vals.append(((candidate[k] / target[k]) - 1.0) ** 2)
        rows.append(float(np.mean(vals)))
    return float(np.mean(rows))


def evaluate_aggregate(aggregate: dict, contexts: Sequence[dict], phase63a: dict, label: str) -> dict:
    folds = []
    for ctx in contexts:
        fi = ctx["fold"]
        candidate_exposed = {
            "S1": aggregate["S1_by_fold"][str(fi)],
            "S2": aggregate["S2"],
            "S3": aggregate["S3"],
        }
        comp = {
            "D_profile": p.profile_distance(aggregate["H62P1"], ctx["target_H62P1"]),
            "abs_C_short_diff": p.c_short_diff(aggregate["H62P1"], ctx["target_H62P1"]),
        }
        folds.append({
            "fold": fi,
            "test_leaves": ctx["test_leaves"],
            "target_exposed": ctx["target_exposed"],
            "candidate_exposed": candidate_exposed,
            "candidate_exposed_ratios": {
                k: float(candidate_exposed[k] / ctx["target_exposed"][k])
                for k in ("S1", "S2", "S3")
            },
            "candidate_H62_comparison": comp,
            "baseline_H62_comparisons": ctx["baseline_H62"],
        })

    target_mean = {
        k: float(np.mean([row["target_exposed"][k] for row in folds]))
        for k in ("S1", "S2", "S3")
    }
    candidate_mean = {
        "S1": float(np.mean([row["candidate_exposed"]["S1"] for row in folds])),
        "S2": float(aggregate["S2"]),
        "S3": float(aggregate["S3"]),
    }
    ratios = {k: float(candidate_mean[k] / target_mean[k]) for k in ("S1", "S2", "S3")}
    exposed_gate = {k: 0.5 <= ratios[k] <= 2.0 for k in ratios}

    d = [row["candidate_H62_comparison"]["D_profile"] for row in folds]
    cs = [row["candidate_H62_comparison"]["abs_C_short_diff"] for row in folds]
    h62 = {
        "mean_D_profile": float(np.mean(d)),
        "median_D_profile": float(statistics.median(d)),
        "mean_abs_C_short_diff": float(np.mean(cs)),
        "D_profile_fold_values": d,
        "abs_C_short_diff_fold_values": cs,
    }

    base_summary = phase63a["across_fold"]["committed_H62P1_baseline_summaries"]
    viability_means = {}
    viability_wins = {}
    for base in ("N0", "C0"):
        bd = [row["baseline_H62_comparisons"][base]["D_profile"] for row in folds]
        bc = [row["baseline_H62_comparisons"][base]["abs_C_short_diff"] for row in folds]
        viability_means[base] = {
            "lower_mean_D_profile": h62["mean_D_profile"] + TIE_EPS < base_summary[base]["mean_D_profile"],
            "lower_mean_abs_C_short_diff": h62["mean_abs_C_short_diff"] + TIE_EPS < base_summary[base]["mean_abs_C_short_diff"],
        }
        viability_wins[base] = {
            "D_profile_wins": strict_wins(d, bd),
            "abs_C_short_diff_wins": strict_wins(cs, bc),
        }

    a1_d = [row["baseline_H62_comparisons"]["A1_R1"]["D_profile"] for row in folds]
    a1_c = [row["baseline_H62_comparisons"]["A1_R1"]["abs_C_short_diff"] for row in folds]
    a1_summary = phase63a["across_fold"]["A1_R1_H62P1_summary"]
    rivalry = {
        "lower_mean_D_profile": h62["mean_D_profile"] + TIE_EPS < a1_summary["mean_D_profile"],
        "lower_median_D_profile": h62["median_D_profile"] + TIE_EPS < a1_summary["median_D_profile"],
        "D_profile_wins": strict_wins(d, a1_d),
        "lower_mean_abs_C_short_diff": h62["mean_abs_C_short_diff"] + TIE_EPS < a1_summary["mean_abs_C_short_diff"],
        "abs_C_short_diff_wins": strict_wins(cs, a1_c),
    }

    exposed_pass = all(exposed_gate.values())
    h62_viable = (
        all(v["lower_mean_D_profile"] and v["lower_mean_abs_C_short_diff"] for v in viability_means.values())
        and all(v["D_profile_wins"] >= 3 and v["abs_C_short_diff_wins"] >= 3 for v in viability_wins.values())
    )
    structurally_viable = bool(exposed_pass and h62_viable)
    a1_rival = bool(
        structurally_viable
        and rivalry["lower_mean_D_profile"]
        and rivalry["lower_median_D_profile"]
        and rivalry["D_profile_wins"] >= 3
        and rivalry["lower_mean_abs_C_short_diff"]
        and rivalry["abs_C_short_diff_wins"] >= 3
    )
    jrmse = joint_relative_mse(folds)

    # Frozen PARTIAL operationalization: if the full viability gate fails but
    # at least one substantive predeclared component beats a prior baseline,
    # retain it as partial rather than calling it noncompetitive.
    partial_signal = (
        exposed_pass
        or h62_viable
        or h62["mean_D_profile"] + TIE_EPS < min(base_summary[x]["mean_D_profile"] for x in ("N0", "C0"))
        or h62["mean_abs_C_short_diff"] + TIE_EPS < min(base_summary[x]["mean_abs_C_short_diff"] for x in ("N0", "C0"))
    )
    if a1_rival:
        classification = "C1-E0 H62 RIVAL TO A1-R1"
    elif structurally_viable:
        classification = "C1-E0 STRUCTURALLY VIABLE"
    elif partial_signal:
        classification = "C1-E0 PARTIAL"
    else:
        classification = "C1-E0 NOT COMPETITIVE"

    return {
        "label": label,
        "folds": folds,
        "target_exposed_mean": target_mean,
        "candidate_exposed_mean": candidate_mean,
        "candidate_ratio_of_means_to_voynich": ratios,
        "exposed_gate_0.5_to_2.0": exposed_gate,
        "exposed_gate_pass": exposed_pass,
        "joint_relative_mse": jrmse,
        "H62P1_summary": h62,
        "H62_viability_mean_superiority": viability_means,
        "H62_viability_fold_wins": viability_wins,
        "H62_viable_vs_N0_C0": h62_viable,
        "H62_rivalry_vs_A1_R1": rivalry,
        "structurally_viable": structurally_viable,
        "A1_R1_rival": a1_rival,
        "classification": classification,
    }


def run_mapping(
    module,
    mapping_name: str,
    glyph_map: Dict[str, str],
    raw_sources: Dict[str, Sequence[b.Item]],
    contexts: Sequence[dict],
) -> dict:
    per_ms_primary = {}
    per_ms_raw = {}
    diagnostics = {}
    for mi, manuscript in enumerate(MANUSCRIPTS):
        primary_reps = {}
        raw_reps = {}
        rep_diag = {}
        for r in range(CIPHER_REPS):
            seed = 6480000 + 100 * mi + r
            primary_items, raw_items, diag = encrypt_manuscript(
                module, raw_sources[manuscript], manuscript, glyph_map, seed
            )
            base_label = f"Phase64B:{mapping_name}:{manuscript}:rep{r}"
            primary_reps[f"rep{r}"] = output_metrics(primary_items, base_label + ":published-view", contexts)
            raw_reps[f"rep{r}"] = output_metrics(raw_items, base_label + ":raw-token-view", contexts)
            rep_diag[f"rep{r}"] = diag
        per_ms_primary[manuscript] = aggregate_realizations(
            primary_reps, f"Phase64B:{mapping_name}:{manuscript}:published-view"
        )
        per_ms_raw[manuscript] = aggregate_realizations(
            raw_reps, f"Phase64B:{mapping_name}:{manuscript}:raw-token-view"
        )
        diagnostics[manuscript] = rep_diag

    return {
        "mapping": mapping_name,
        "primary_published_output": {
            "per_manuscript": per_ms_primary,
            "aggregate": aggregate_manuscripts(
                per_ms_primary, f"Phase64B:{mapping_name}:published-view"
            ),
        },
        "raw_token_sensitivity": {
            "per_manuscript": per_ms_raw,
            "aggregate": aggregate_manuscripts(
                per_ms_raw, f"Phase64B:{mapping_name}:raw-token-view"
            ),
        },
        "encryption_diagnostics": diagnostics,
    }


def aggregate_permutations(perm_results: Dict[str, dict], view_key: str, label: str) -> dict:
    aggs = {name: row[view_key]["aggregate"] for name, row in perm_results.items()}
    fold_ids = sorted(next(iter(aggs.values()))["S1_by_fold"], key=int)
    return {
        "S1_by_fold": {
            f: float(np.mean([row["S1_by_fold"][f] for row in aggs.values()]))
            for f in fold_ids
        },
        "S2": float(np.mean([row["S2"] for row in aggs.values()])),
        "S3": float(np.mean([row["S3"] for row in aggs.values()])),
        "H62P1": p.aggregate_excess(
            {name: row["H62P1"] for name, row in aggs.items()},
            label,
            "mapping permutation",
        ),
    }


def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt /path/to/CREMMA-Medieval-LAT /path/to/naibbe-cipher", file=sys.stderr)
        return 2

    voynich_path = Path(sys.argv[1]).resolve()
    cremma_root = Path(sys.argv[2]).resolve()
    naibbe_root = Path(sys.argv[3]).resolve()

    ccommit = b.verify_cremma_commit(cremma_root)
    module = load_naibbe(naibbe_root)
    original_map = dict(module.placeholder_to_glyph)
    if len(original_map) != 6 * 3 * 26:
        raise RuntimeError(f"unexpected Naibbe codebook cell count: {len(original_map)}")

    phase62c_path = PHASE62 / "phase62c_c0_a1_results.json"
    phase62p_path = PHASE62 / "phase62p_h62p1_results.json"
    phase63a_path = PHASE63 / "phase63a_training_vocab_results.json"
    if sha256_file(phase62p_path) != PHASE62P_SHA256:
        raise RuntimeError("Phase62P authority digest mismatch")
    if sha256_file(phase63a_path) != PHASE63A_SHA256:
        raise RuntimeError("Phase63A authority digest mismatch")
    phase62c = json.loads(phase62c_path.read_text(encoding="utf-8"))
    phase62p = json.loads(phase62p_path.read_text(encoding="utf-8"))
    phase63a = json.loads(phase63a_path.read_text(encoding="utf-8"))
    if phase62p["across_fold"]["prospective_profile_leader"] != "A1":
        raise RuntimeError("Phase62P no longer records A1 as prospective leader")
    if not phase63a["across_fold"]["robust_to_heldout_vocabulary_removal"]:
        raise RuntimeError("Phase63A authority no longer records A1-R1 robustness")

    contexts, _vitems = fold_contexts(voynich_path, phase62c, phase63a)
    raw_sources = {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }

    published = run_mapping(module, "published", original_map, raw_sources, contexts)
    published_eval = evaluate_aggregate(
        published["primary_published_output"]["aggregate"], contexts, phase63a, "published"
    )
    published_raw_eval = evaluate_aggregate(
        published["raw_token_sensitivity"]["aggregate"], contexts, phase63a, "published-raw-token"
    )

    permutations = {}
    for pi in range(MAPPING_PERMS):
        pseed = 6490000 + pi
        pmap = permuted_mapping(module, original_map, pseed)
        name = f"perm{pi}"
        row = run_mapping(module, name, pmap, raw_sources, contexts)
        row["mapping_permutation_seed"] = pseed
        row["primary_evaluation"] = evaluate_aggregate(
            row["primary_published_output"]["aggregate"], contexts, phase63a, name
        )
        permutations[name] = row

    perm_aggregate = aggregate_permutations(
        permutations,
        "primary_published_output",
        "Phase64B:permutation-control:mean-E",
    )
    perm_eval = evaluate_aggregate(
        perm_aggregate, contexts, phase63a, "mapping-permutation-control"
    )

    codebook_specificity = {
        "published_lower_mean_D_profile": (
            published_eval["H62P1_summary"]["mean_D_profile"] + TIE_EPS
            < perm_eval["H62P1_summary"]["mean_D_profile"]
        ),
        "published_lower_mean_abs_C_short_diff": (
            published_eval["H62P1_summary"]["mean_abs_C_short_diff"] + TIE_EPS
            < perm_eval["H62P1_summary"]["mean_abs_C_short_diff"]
        ),
        "published_lower_exposed_joint_relative_mse": (
            published_eval["joint_relative_mse"] + TIE_EPS
            < perm_eval["joint_relative_mse"]
        ),
        "published": {
            "mean_D_profile": published_eval["H62P1_summary"]["mean_D_profile"],
            "mean_abs_C_short_diff": published_eval["H62P1_summary"]["mean_abs_C_short_diff"],
            "joint_relative_mse": published_eval["joint_relative_mse"],
        },
        "permutation_control": {
            "mean_D_profile": perm_eval["H62P1_summary"]["mean_D_profile"],
            "mean_abs_C_short_diff": perm_eval["H62P1_summary"]["mean_abs_C_short_diff"],
            "joint_relative_mse": perm_eval["joint_relative_mse"],
        },
    }
    codebook_specificity["published_assignment_gets_specific_credit"] = all([
        codebook_specificity["published_lower_mean_D_profile"],
        codebook_specificity["published_lower_mean_abs_C_short_diff"],
        codebook_specificity["published_lower_exposed_joint_relative_mse"],
    ])

    set_glyph_map(module, original_map)
    out = {
        "phase": "64B",
        "hypothesis": "P64-C1-E0 published Naibbe external meaningful-text cipher challenge",
        "scope_firewall": "exact published Naibbe v2 only; no reuse variant, no Voynich-selected parameter, no A2, no post-result locality repair",
        "inputs": {
            "voynich_git_blob_sha1": b.git_blob_sha1(voynich_path.read_bytes()),
            "cremma_commit": ccommit,
            "manuscripts_equal_weight": list(MANUSCRIPTS),
            "naibbe_commit": NAIBBE_COMMIT,
            "naibbe_v2_blob": NAIBBE_PY_BLOB,
            "naibbe_tables_blob": NAIBBE_TABLE_BLOB,
            "naibbe_readme_blob": NAIBBE_README_BLOB,
            "effective_plaintext_letters": list(EFFECTIVE_LETTERS),
            "effective_reachable_codebook_cells": 6 * 3 * len(EFFECTIVE_LETTERS),
            "cipher_realizations_per_manuscript": CIPHER_REPS,
            "mapping_permutations": MAPPING_PERMS,
            "published_defaults": {
                "RESPACING": module.RESPACING,
                "USE_78_CARD_DECK": module.USE_78_CARD_DECK,
                "SPACE_REMOVAL_RATE": module.SPACE_REMOVAL_RATE,
                "UNAMBIGUOUS": module.UNAMBIGUOUS,
                "MAX_BIGRAM_RETRIES": module.MAX_BIGRAM_RETRIES,
                "CARD_WEIGHTS_78": module.CARD_WEIGHTS[True],
            },
            "cipher_seed_formula": "6480000 + 100*manuscript_index + realization",
            "mapping_permutation_seed_formula": "6490000 + permutation_index",
            "phase62p_raw_sha256": PHASE62P_SHA256,
            "phase63a_raw_sha256": PHASE63A_SHA256,
        },
        "published_mapping": {
            "generation": published,
            "primary_evaluation": published_eval,
            "raw_token_sensitivity_evaluation": published_raw_eval,
        },
        "mapping_permutation_control": {
            "permutations": permutations,
            "aggregate": perm_aggregate,
            "aggregate_evaluation": perm_eval,
        },
        "codebook_specificity": codebook_specificity,
        "frozen_primary_classification": published_eval["classification"],
        "claim_limit": "external C-family mechanism challenge only; no historical identification, semantic recovery, family-wide acceptance/rejection, or decipherment",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
