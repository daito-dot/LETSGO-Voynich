#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import phaseE12_porta_probe as base


def rename_population_fields(result):
    for row in result["folds"]:
        if "cluster_train_counts" in row:
            row["training_raw_code_counts"] = row.pop("cluster_train_counts")
    return result


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr)
        return 2

    zl = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    if base.e.git_blob_sha1(zl.read_bytes()) != base.e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")

    parser = base.e.SlotParser()
    validation = base.e.validate_parser(parser)
    items = base.e.parse_voynich(zl)
    runs, lexicon, lmeta = base.load_latin(root)
    lm4 = base.LM4(runs)
    bg = base.bigram_cost(runs)
    baseline = base.latin_self_baseline(runs)

    # Pre-reveal correction: match the positive-control event count to the
    # exact eligible physical-leaf universe used by the five-fold analysis.
    folds = base.e.physical_leaf_folds(items)
    all_leaves = set().union(*folds)
    vectors = base.training_vectors(items, all_leaves, parser, "min")
    full_km = base.KMeansK().fit(vectors)
    _, full_raw_counts, full_meta = base.raw_streams(items, all_leaves, parser, "min", full_km)
    pos = base.positive_control(runs, int(full_raw_counts.sum()), lm4, bg)

    primary = rename_population_fields(base.run_voynich_policy(items, parser, "min", lm4, bg, lexicon))
    sensitivity = rename_population_fields(base.run_voynich_policy(items, parser, "max", lm4, bg, lexicon))
    classification, gates = base.classify(primary, baseline, pos)

    out = {
        "experiment": "Issue26E12 Porta 1602 11x2 musical-cipher plaintext probe",
        "classification": classification,
        "interpretation": gates,
        "historical_table_low_to_high": ["".join(r) for r in base.PORTA_TABLE],
        "historical_supported_alphabet": "".join(base.ALPHABET),
        "voynich_binary_factor": {"slot": base.DURATION_SLOT, "states": list(base.DURATION_STATES)},
        "voynich_pitch_projection": {"k": 11, "status": "HYPOTHESIS-SIDE PORTA-IMPOSED TRAIN-ONLY CLUSTERING"},
        "latin_population": lmeta,
        "latin_self_baseline": baseline,
        "positive_control": pos,
        "full_primary_population": full_meta,
        "analysis_leaf_count": len(all_leaves),
        "slot_parser_validation": validation,
        "primary_min": primary,
        "max_sensitivity": sensitivity,
        "pre_reveal_technical_corrections": [
            "positive-control target count restricted to exact eligible physical-leaf fold universe",
            "misnamed cluster_train_counts output renamed training_raw_code_counts; values are unchanged",
        ],
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
