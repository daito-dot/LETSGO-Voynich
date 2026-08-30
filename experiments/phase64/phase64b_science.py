#!/usr/bin/env python3
"""Official Phase64B first-reveal entrypoint.

Uses the frozen phase64b_naibbe adapter with the pre-result B2 corrections
recorded in PREFLIGHT_AMENDMENT_B2.md:
- exact 414 reachable published codebook cells are required;
- no normalized-away j/k/w cells are synthesized;
- permutation controls score only their preregistered primary respaced view;
- external-module stdout is captured so the scientific artifact is valid JSON.

No scientific candidate, seed, metric, aggregation, threshold, or result-based
selection is changed.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path
from typing import Dict, Sequence

import numpy as np

import phase64b_naibbe as core


def run_mapping_primary_only(
    module,
    mapping_name: str,
    glyph_map: Dict[str, str],
    raw_sources: Dict[str, Sequence[core.b.Item]],
    contexts: Sequence[dict],
) -> dict:
    """Run a frozen mapping permutation and score only the planned primary view.

    encrypt_manuscript still computes/calls published respacing in the exact
    paired RNG sequence; its raw-token return value is simply not scored.
    """
    per_ms_primary = {}
    diagnostics = {}
    for mi, manuscript in enumerate(core.MANUSCRIPTS):
        primary_reps = {}
        rep_diag = {}
        for r in range(core.CIPHER_REPS):
            seed = 6480000 + 100 * mi + r
            primary_items, _raw_items, diag = core.encrypt_manuscript(
                module, raw_sources[manuscript], manuscript, glyph_map, seed
            )
            label = f"Phase64B:{mapping_name}:{manuscript}:rep{r}:published-view"
            primary_reps[f"rep{r}"] = core.output_metrics(primary_items, label, contexts)
            rep_diag[f"rep{r}"] = diag
        per_ms_primary[manuscript] = core.aggregate_realizations(
            primary_reps, f"Phase64B:{mapping_name}:{manuscript}:published-view"
        )
        diagnostics[manuscript] = rep_diag

    return {
        "mapping": mapping_name,
        "primary_published_output": {
            "per_manuscript": per_ms_primary,
            "aggregate": core.aggregate_manuscripts(
                per_ms_primary, f"Phase64B:{mapping_name}:published-view"
            ),
        },
        "raw_token_sensitivity": "NOT_SCORED_FOR_MAPPING_PERMUTATIONS_BY_FROZEN_B2_COMPUTATIONAL_CLARIFICATION",
        "encryption_diagnostics": diagnostics,
    }


def compute(voynich_path: Path, cremma_root: Path, naibbe_root: Path) -> dict:
    ccommit = core.b.verify_cremma_commit(cremma_root)
    module = core.load_naibbe(naibbe_root)
    original_map = dict(module.placeholder_to_glyph)

    effective_required_codes = {
        f"{state}_{table}_{letter}"
        for state in module.STATES
        for table in module.TABLES
        for letter in core.EFFECTIVE_LETTERS
    }
    if set(original_map) != effective_required_codes:
        missing = sorted(effective_required_codes - set(original_map))
        extras = sorted(set(original_map) - effective_required_codes)
        raise RuntimeError(
            f"published Naibbe effective codebook mismatch: missing={missing[:10]} extras={extras[:10]}"
        )

    theoretical_full_grid = {
        f"{state}_{table}_{letter}"
        for state in module.STATES
        for table in module.TABLES
        for letter in module.ALPHABET
    }
    normalized_away_codes = sorted(theoretical_full_grid - effective_required_codes)
    if len(effective_required_codes) != 414 or len(normalized_away_codes) != 54:
        raise RuntimeError("Naibbe B2 effective/full-grid cardinality mismatch")

    phase62c_path = core.PHASE62 / "phase62c_c0_a1_results.json"
    phase62p_path = core.PHASE62 / "phase62p_h62p1_results.json"
    phase63a_path = core.PHASE63 / "phase63a_training_vocab_results.json"
    if core.sha256_file(phase62p_path) != core.PHASE62P_SHA256:
        raise RuntimeError("Phase62P authority digest mismatch")
    if core.sha256_file(phase63a_path) != core.PHASE63A_SHA256:
        raise RuntimeError("Phase63A authority digest mismatch")
    phase62c = json.loads(phase62c_path.read_text(encoding="utf-8"))
    phase62p = json.loads(phase62p_path.read_text(encoding="utf-8"))
    phase63a = json.loads(phase63a_path.read_text(encoding="utf-8"))
    if phase62p["across_fold"]["prospective_profile_leader"] != "A1":
        raise RuntimeError("Phase62P no longer records A1 as prospective leader")
    if not phase63a["across_fold"]["robust_to_heldout_vocabulary_removal"]:
        raise RuntimeError("Phase63A authority no longer records A1-R1 robustness")

    contexts, _vitems = core.fold_contexts(voynich_path, phase62c, phase63a)
    raw_sources = {
        name: core.b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in core.b.PRIMARY_MANUSCRIPTS.items()
    }

    # Published mapping: score both the primary published output and the frozen
    # paired raw-token sensitivity.
    published = core.run_mapping(module, "published", original_map, raw_sources, contexts)
    published_eval = core.evaluate_aggregate(
        published["primary_published_output"]["aggregate"], contexts, phase63a, "published"
    )
    published_raw_eval = core.evaluate_aggregate(
        published["raw_token_sensitivity"]["aggregate"], contexts, phase63a, "published-raw-token"
    )

    # Mapping controls: score only the preregistered primary published-output
    # view; raw-token permutation scoring is redundant and was never a rescue.
    permutations = {}
    for pi in range(core.MAPPING_PERMS):
        pseed = 6490000 + pi
        pmap = core.permuted_mapping(module, original_map, pseed)
        name = f"perm{pi}"
        row = run_mapping_primary_only(module, name, pmap, raw_sources, contexts)
        row["mapping_permutation_seed"] = pseed
        row["primary_evaluation"] = core.evaluate_aggregate(
            row["primary_published_output"]["aggregate"], contexts, phase63a, name
        )
        permutations[name] = row

    perm_aggregate = core.aggregate_permutations(
        permutations,
        "primary_published_output",
        "Phase64B:permutation-control:mean-E",
    )
    perm_eval = core.evaluate_aggregate(
        perm_aggregate, contexts, phase63a, "mapping-permutation-control"
    )

    codebook_specificity = {
        "published_lower_mean_D_profile": (
            published_eval["H62P1_summary"]["mean_D_profile"] + core.TIE_EPS
            < perm_eval["H62P1_summary"]["mean_D_profile"]
        ),
        "published_lower_mean_abs_C_short_diff": (
            published_eval["H62P1_summary"]["mean_abs_C_short_diff"] + core.TIE_EPS
            < perm_eval["H62P1_summary"]["mean_abs_C_short_diff"]
        ),
        "published_lower_exposed_joint_relative_mse": (
            published_eval["joint_relative_mse"] + core.TIE_EPS
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

    core.set_glyph_map(module, original_map)
    return {
        "phase": "64B",
        "hypothesis": "P64-C1-E0 published Naibbe external meaningful-text cipher challenge",
        "scope_firewall": "exact published Naibbe v2 only; no reuse variant, no Voynich-selected parameter, no A2, no post-result locality repair",
        "inputs": {
            "voynich_git_blob_sha1": core.b.git_blob_sha1(voynich_path.read_bytes()),
            "cremma_commit": ccommit,
            "manuscripts_equal_weight": list(core.MANUSCRIPTS),
            "naibbe_commit": core.NAIBBE_COMMIT,
            "naibbe_v2_blob": core.NAIBBE_PY_BLOB,
            "naibbe_tables_blob": core.NAIBBE_TABLE_BLOB,
            "naibbe_readme_blob": core.NAIBBE_README_BLOB,
            "loaded_codebook_entries": len(original_map),
            "effective_required_code_cells": len(effective_required_codes),
            "theoretical_26_letter_grid_cells": len(theoretical_full_grid),
            "normalized_away_jkw_cells": len(normalized_away_codes),
            "normalized_away_jkw_code_names": normalized_away_codes,
            "effective_plaintext_letters": list(core.EFFECTIVE_LETTERS),
            "effective_reachable_codebook_cells": 6 * 3 * len(core.EFFECTIVE_LETTERS),
            "cipher_realizations_per_manuscript": core.CIPHER_REPS,
            "mapping_permutations": core.MAPPING_PERMS,
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
            "phase62p_raw_sha256": core.PHASE62P_SHA256,
            "phase63a_raw_sha256": core.PHASE63A_SHA256,
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


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} ZL3b-n.txt /path/to/CREMMA-Medieval-LAT /path/to/naibbe-cipher",
            file=sys.stderr,
        )
        return 2

    voynich_path = Path(sys.argv[1]).resolve()
    cremma_root = Path(sys.argv[2]).resolve()
    naibbe_root = Path(sys.argv[3]).resolve()

    # The pinned external module prints a diagnostic on import. Capture all
    # internal stdout so the first-reveal file contains exactly one JSON object.
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        out = compute(voynich_path, cremma_root, naibbe_root)

    external_stdout = captured.getvalue()
    out["execution_stdout_audit"] = {
        "captured_characters": len(external_stdout),
        "sha256": hashlib.sha256(external_stdout.encode("utf-8")).hexdigest(),
        "sample_first_500_characters": external_stdout[:500],
        "used_for_scoring": False,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
