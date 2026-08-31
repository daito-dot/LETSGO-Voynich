#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

# Frozen historical table reconstructed from the HAB transcription of
# Cod. Guelf. 56 Aug. 4°. Rows: ut, sol, fa, mi, re.
# Columns: ut, fa, sol, mi, re. Cell plaintext is the third letter of
# the angel name. Lalalala duplicates l as the documented filler/joke cell.
OETTINGEN_TABLE = (
    ("q", "r", "s", "t", "u"),
    ("w", "x", "y", "z", "l"),
    ("a", "b", "c", "d", "e"),
    ("l", "m", "n", "o", "p"),
    ("f", "g", "h", "i", "k"),
)


def classify(primary, baseline):
    b = primary["track_b_fitted"]
    d = b["pooled_diagnostics_using_fold_specific_keys"]
    lead = (
        b["exact_key_recurrence"] >= 4
        and b["pooled_cross_entropy"] <= baseline["mean_cross_entropy"] + 0.50
        and d["distinct_lexicon_hits_ge6"] >= 10
        and d["top5_char_fraction"] < 0.80
    )
    classification = "OETTINGEN PLAINTEXT LEAD" if lead else "NO READABLE OETTINGEN PLAINTEXT"
    local_repeat = (
        b["exact_key_recurrence"] >= 4
        and not lead
        and d["top5_char_fraction"] >= 0.90
    )
    return classification, {
        "lead_gate": {
            "key_recurrence_ge4": b["exact_key_recurrence"] >= 4,
            "latin_distance_within_0_50": b["pooled_cross_entropy"] <= baseline["mean_cross_entropy"] + 0.50,
            "distinct_lexicon_hits_ge6_ge10": d["distinct_lexicon_hits_ge6"] >= 10,
            "top5_fraction_lt_0_80": d["top5_char_fraction"] < 0.80,
        },
        "local_optimum_numeric_flag": local_repeat,
        "local_optimum_label": "5X5 LOCAL-OPTIMUM PATTERN REPEATS" if local_repeat else "NO NUMERIC LOCAL-OPTIMUM FLAG",
    }


def main():
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT E10_ENGINE_DIR", file=sys.stderr)
        return 2

    zl = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    engine_dir = Path(sys.argv[3]).resolve()
    sys.path.insert(0, str(engine_dir))

    import phaseE10_sloane351_probe as base

    # The entire E10 engine is reused at its exact frozen scientific SHA;
    # only the externally frozen historical plaintext table is replaced.
    base.TABLE = OETTINGEN_TABLE

    if base.e.git_blob_sha1(zl.read_bytes()) != base.e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")

    parser = base.e.SlotParser()
    validation = base.e.validate_parser(parser)
    items = base.e.parse_voynich(zl)
    runs, lexicon, alphabet, lmeta = base.load_latin(root)
    baseline = base.latin_self_baseline(runs, alphabet)
    lm = base.LM4(runs, alphabet)
    M, perms, axes, spi, ppi = base.key_matrix()

    primary = base.run_policy(items, parser, "min", lm, lexicon, M, perms, axes, spi, ppi)
    sensitivity = base.run_policy(items, parser, "max", lm, lexicon, M, perms, axes, spi, ppi)
    classification, interpretation = classify(primary, baseline)

    out = {
        "experiment": "Issue26E11 Oettingen-Wallerstein 5x5 musical Polybius plaintext probe",
        "status": "FIRST-REVEAL TARGET PROBE",
        "classification": classification,
        "interpretation_gates": interpretation,
        "historical_table": [list(r) for r in OETTINGEN_TABLE],
        "historical_row_order": ["ut", "sol", "fa", "mi", "re"],
        "historical_column_order": ["ut", "fa", "sol", "mi", "re"],
        "historical_note": "25 musical cells encode 24 distinct letters; Lalalala is the duplicate-l filler cell.",
        "engine_dependency": {
            "repository": "daito-dot/LETSGO-Voynich",
            "commit": "39eebc9f3fc1085e506a0b55ed86e43c83dbc579",
            "file": "experiments/issue26-music/phaseE10_sloane351_probe.py",
        },
        "candidate_keys_per_fold": int(M.shape[0]),
        "latin_population": lmeta,
        "latin_self_baseline": baseline,
        "slot_parser_validation": validation,
        "primary_min": primary,
        "max_sensitivity": sensitivity,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
