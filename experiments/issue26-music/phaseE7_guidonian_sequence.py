#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import random
import statistics
import sys
from pathlib import Path

import issue26e_core as e

IT_SHA256 = "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"
N_SHUFFLES = 5000

FOLDS = [
    {1,6,11,17,22,27,32,37,42,47,52,57,68,77,82,87,94,101,106,113},
    {2,7,13,18,23,28,33,38,43,48,53,58,69,78,83,88,95,102,107,114},
    {3,8,14,19,24,29,34,39,44,49,54,65,70,79,84,89,96,103,108,115},
    {4,9,15,20,25,30,35,40,45,50,55,66,75,80,85,90,99,104,111,116},
    {5,10,16,21,26,31,36,41,46,51,56,67,76,81,86,93,100,105,112},
]

EXPECTED_REPLAY = {
    ("ZL", "min"): 0.8509664380470466,
    ("ZL", "max"): 0.8439032769036159,
    ("IT", "min"): 0.8512154779726009,
    ("IT", "max"): 0.8404723923113318,
}

HEX_START_ROWS = (0, 3, 6, 7, 10, 13, 14)
HEX_START_SEMITONES = (0, 5, 10, 12, 17, 22, 24)
VOICE_OFFSETS = (0, 2, 4, 5, 7, 9)
STATE_INDEX = {s: i for i, s in enumerate(e.SLOT10_STATES)}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_cell_model():
    cell_meta = {}
    hex_pitches = []
    for h, (row0, pitch0) in enumerate(zip(HEX_START_ROWS, HEX_START_SEMITONES)):
        pitches = set()
        for vox in range(6):
            row = row0 + vox
            pitch = pitch0 + VOICE_OFFSETS[vox]
            if int(e.GUIDO[row, vox]) != 1:
                raise RuntimeError(f"hexachord decomposition misses GUIDO cell {(row, vox)}")
            key = (row, vox)
            if key in cell_meta:
                raise RuntimeError(f"duplicate hexachord cell {key}")
            cell_meta[key] = {"hex": h, "pitch": pitch, "row": row, "vox": vox}
            pitches.add(pitch)
        hex_pitches.append(frozenset(pitches))

    guido_cells = {tuple(map(int, x)) for x in __import__("numpy").argwhere(e.GUIDO == 1)}
    if set(cell_meta) != guido_cells or len(cell_meta) != 42:
        raise RuntimeError("seven-hexachord decomposition does not equal the frozen 42-cell lattice")

    # The collapsed 20-row representation contains two historical B-fa / square-B-mi
    # row coincidences. Cell-level semitone identity must distinguish them.
    for row in (9, 16):
        fa = cell_meta[(row, 3)]["pitch"]
        mi = cell_meta[(row, 2)]["pitch"]
        if abs(fa - mi) != 1:
            raise RuntimeError(f"B-fa / B-mi pitch separation failed at row {row}: {fa}, {mi}")

    keys = sorted(cell_meta)
    cell_id = {k: i for i, k in enumerate(keys)}
    meta = [cell_meta[k] for k in keys]

    n = len(keys)
    same = [[False] * n for _ in range(n)]
    compatible = [[False] * n for _ in range(n)]
    valid_switch = [[False] * n for _ in range(n)]
    false_row_equal = [[False] * n for _ in range(n)]
    nonoverlap_switch = [[False] * n for _ in range(n)]

    for i, a in enumerate(meta):
        for j, b in enumerate(meta):
            if a["hex"] == b["hex"]:
                same[i][j] = True
                compatible[i][j] = True
                continue
            shared = hex_pitches[a["hex"]] & hex_pitches[b["hex"]]
            valid = (a["pitch"] in shared) or (b["pitch"] in shared)
            valid_switch[i][j] = valid
            compatible[i][j] = valid
            false_row_equal[i][j] = (a["row"] == b["row"] and a["pitch"] != b["pitch"] and not valid)
            nonoverlap_switch[i][j] = not bool(shared)

    return {
        "cell_meta": cell_meta,
        "cell_id": cell_id,
        "meta": meta,
        "hex_pitches": hex_pitches,
        "same": same,
        "compatible": compatible,
        "valid_switch": valid_switch,
        "false_row_equal": false_row_equal,
        "nonoverlap_switch": nonoverlap_switch,
    }


CELL = build_cell_model()


def fit_types(items, train, parser, policy):
    vectors = {}
    for it in items:
        if it["leaf"] not in train:
            continue
        for line in it["lines"]:
            for tok in line:
                p = parser.pick(tok, policy)
                if p is not None and tok not in vectors:
                    vectors[tok] = e.feature(p[1])
    return e.KMeans20().fit(vectors), len(vectors)


def finalize_run(run, runs):
    if len(run) >= 2:
        runs.append(tuple(run))


def heldout_runs(items, held, parser, policy, km, mapping):
    runs = []
    admitted = 0
    parsed = 0
    visible = 0
    singleton_admitted = 0

    for it in items:
        if it["leaf"] not in held:
            continue
        for line in it["lines"]:
            run = []
            for tok in line:
                visible += 1
                p = parser.pick(tok, policy)
                if p is None:
                    if len(run) == 1:
                        singleton_admitted += 1
                    finalize_run(run, runs)
                    run = []
                    continue
                parsed += 1
                vals = p[1]
                cluster = km.predict(e.feature(vals))
                state = STATE_INDEX[vals[10]]
                row = int(mapping["cluster_to_row"][cluster])
                vox = int(mapping["state_to_vox"][state])
                if int(e.GUIDO[row, vox]) != 1:
                    if len(run) == 1:
                        singleton_admitted += 1
                    finalize_run(run, runs)
                    run = []
                    continue
                admitted += 1
                run.append(CELL["cell_id"][(row, vox)])
            if len(run) == 1:
                singleton_admitted += 1
            finalize_run(run, runs)

    return {
        "runs": runs,
        "visible": visible,
        "parsed": parsed,
        "admitted": admitted,
        "singleton_admitted": singleton_admitted,
    }


def transition_counts(runs):
    total = same = switches = valid = false_row = nonoverlap = 0
    compat = 0
    for run in runs:
        for a, b in zip(run, run[1:]):
            total += 1
            if CELL["same"][a][b]:
                same += 1
                compat += 1
            else:
                switches += 1
                if CELL["valid_switch"][a][b]:
                    valid += 1
                    compat += 1
                if CELL["false_row_equal"][a][b]:
                    false_row += 1
                if CELL["nonoverlap_switch"][a][b]:
                    nonoverlap += 1
    return {
        "total": total,
        "compatible": compat,
        "same_hex": same,
        "switches": switches,
        "valid_switches": valid,
        "false_row_equal_invalid_switches": false_row,
        "nonoverlap_switches": nonoverlap,
    }


def ratio(a, b):
    return a / b if b else None


def counts_to_metrics(c):
    return {
        **c,
        "D1_dynamic_compatibility": ratio(c["compatible"], c["total"]),
        "D2_mutation_legality": ratio(c["valid_switches"], c["switches"]),
        "same_hex_fraction": ratio(c["same_hex"], c["total"]),
        "switch_fraction": ratio(c["switches"], c["total"]),
    }


def shuffled_counts(runs, seed):
    rng = random.Random(seed)
    shuffled = []
    for run in runs:
        z = list(run)
        rng.shuffle(z)
        shuffled.append(z)
    return transition_counts(shuffled)


def empirical_upper(obs, nulls):
    return (1 + sum(x >= obs - e.EPS for x in nulls)) / (len(nulls) + 1)


def null_summary(obs, nulls):
    return {
        "observed": obs,
        "null_median": statistics.median(nulls),
        "null_q95": e.quantile(nulls, 0.95),
        "observed_minus_null_median": obs - statistics.median(nulls),
        "p_upper": empirical_upper(obs, nulls),
        "n_null": len(nulls),
    }


def run_policy(items, parser, policy, dataset_label):
    universe = set().union(*FOLDS)
    fold_outputs = []
    null_counts_by_fold = []
    static_acc = []

    for f, held in enumerate(FOLDS):
        train = universe - held
        km, ntypes = fit_types(items, train, parser, policy)
        C, tvis, tpar = e.count_matrix(items, train, parser, policy, km)
        H, hvis, hpar = e.count_matrix(items, held, parser, policy, km)
        mapping = e.fit_mapping(C, e.GUIDO)
        static_score = e.score_counts(H, hvis, hpar, mapping, e.GUIDO)
        static_acc.append(static_score["accuracy"])

        seq = heldout_runs(items, held, parser, policy, km, mapping)
        if seq["visible"] != hvis or seq["parsed"] != hpar:
            raise RuntimeError(f"heldout sequence count mismatch {dataset_label} {policy} fold {f}")
        if seq["admitted"] != static_score["allowed_occurrences"]:
            raise RuntimeError(
                f"dynamic admission mismatch {dataset_label} {policy} fold {f}: "
                f"{seq['admitted']} != {static_score['allowed_occurrences']}"
            )

        obs_counts = transition_counts(seq["runs"])
        obs = counts_to_metrics(obs_counts)
        if obs["total"] <= 0 or obs["D1_dynamic_compatibility"] is None:
            raise RuntimeError(f"no dynamic transitions {dataset_label} {policy} fold {f}")

        null_counts = []
        d1_null = []
        d2_null = []
        zero_switch_nulls = 0
        for j in range(N_SHUFFLES):
            seed = e.stable_seed(f"Issue26E7:{dataset_label}:{policy}:fold:{f}:shuffle:{j}")
            nc = shuffled_counts(seq["runs"], seed)
            null_counts.append(nc)
            d1_null.append(nc["compatible"] / nc["total"])
            if nc["switches"]:
                d2_null.append(nc["valid_switches"] / nc["switches"])
            else:
                zero_switch_nulls += 1

        d1s = null_summary(obs["D1_dynamic_compatibility"], d1_null)
        if obs["D2_mutation_legality"] is None or not d2_null:
            d2s = None
        else:
            d2s = null_summary(obs["D2_mutation_legality"], d2_null)
            d2s["zero_switch_null_replicates"] = zero_switch_nulls

        fold_outputs.append({
            "fold": f,
            "held_leaves": sorted(held),
            "training_unique_parsed_types": ntypes,
            "training_visible_occurrences": tvis,
            "training_parsed_occurrences": tpar,
            "heldout_visible_occurrences": hvis,
            "heldout_parsed_occurrences": hpar,
            "heldout_static_allowed_occurrences": static_score["allowed_occurrences"],
            "heldout_static_accuracy": static_score["accuracy"],
            "heldout_parse_coverage": static_score["parse_coverage"],
            "dynamic_admitted_occurrences": seq["admitted"],
            "dynamic_singleton_admitted_occurrences": seq["singleton_admitted"],
            "dynamic_run_count": len(seq["runs"]),
            "guidonian_mapping": mapping,
            "observed": obs,
            "D1_shuffle": d1s,
            "D2_shuffle": d2s,
        })
        null_counts_by_fold.append(null_counts)

    mean_static = statistics.mean(static_acc)
    expected = EXPECTED_REPLAY[(dataset_label, policy)]
    replay_pass = abs(mean_static - expected) <= 1e-12
    if not replay_pass:
        raise RuntimeError(
            f"static replay mismatch {dataset_label} {policy}: {mean_static} != {expected}"
        )

    actual_counts = {
        k: sum(fr["observed"][k] for fr in fold_outputs)
        for k in [
            "total", "compatible", "same_hex", "switches", "valid_switches",
            "false_row_equal_invalid_switches", "nonoverlap_switches"
        ]
    }
    actual = counts_to_metrics(actual_counts)

    global_d1_null = []
    global_d2_null = []
    global_zero_switch = 0
    for j in range(N_SHUFFLES):
        comp = total = valid = switches = 0
        for f in range(5):
            nc = null_counts_by_fold[f][j]
            comp += nc["compatible"]
            total += nc["total"]
            valid += nc["valid_switches"]
            switches += nc["switches"]
        global_d1_null.append(comp / total)
        if switches:
            global_d2_null.append(valid / switches)
        else:
            global_zero_switch += 1

    global_d1 = null_summary(actual["D1_dynamic_compatibility"], global_d1_null)
    global_d2 = None
    if actual["D2_mutation_legality"] is not None and global_d2_null:
        global_d2 = null_summary(actual["D2_mutation_legality"], global_d2_null)
        global_d2["zero_switch_null_replicates"] = global_zero_switch

    d1_positive_folds = sum(
        fr["D1_shuffle"]["observed_minus_null_median"] > e.EPS for fr in fold_outputs
    )
    d2_eligible_folds = [
        fr for fr in fold_outputs
        if fr["observed"]["switches"] >= 10 and fr["D2_shuffle"] is not None
    ]
    d2_positive_folds = sum(
        fr["D2_shuffle"]["observed_minus_null_median"] > e.EPS for fr in d2_eligible_folds
    )

    return {
        "dataset": dataset_label,
        "policy": policy,
        "n_shuffles": N_SHUFFLES,
        "static_replay": {
            "expected_mean_accuracy": expected,
            "observed_mean_accuracy": mean_static,
            "pass_1e-12": replay_pass,
        },
        "folds": fold_outputs,
        "global_observed": actual,
        "global_D1_shuffle": global_d1,
        "global_D2_shuffle": global_d2,
        "D1_positive_folds": d1_positive_folds,
        "D2_eligible_folds_ge10_switches": len(d2_eligible_folds),
        "D2_positive_eligible_folds": d2_positive_folds,
    }


def classify_primary(x):
    obs = x["global_observed"]
    d1 = x["global_D1_shuffle"]
    d2 = x["global_D2_shuffle"]
    sample_ok = obs["total"] >= 500 and obs["switches"] >= 100
    d1_pass = (
        sample_ok and d1["observed_minus_null_median"] > e.EPS and d1["p_upper"] <= 0.05
        and x["D1_positive_folds"] >= 4
    )
    d2_pass = (
        sample_ok and d2 is not None and d2["observed_minus_null_median"] > e.EPS
        and d2["p_upper"] <= 0.05 and x["D2_positive_eligible_folds"] >= 3
    )
    if d1_pass and d2_pass:
        verdict = "GUIDONIAN STATIC FIT PREDICTS NEW DYNAMICS"
    elif d1_pass and not d2_pass:
        verdict = "SEQUENCE CLUSTERING ONLY / NO MUTATION-SPECIFIC SUPPORT"
    elif d2_pass and not d1_pass:
        verdict = "MUTATION-LOCAL SIGNAL ONLY"
    else:
        verdict = "STATIC COMPATIBILITY DOES NOT PREDICT GUIDONIAN DYNAMICS"
    return {
        "sample_gate": sample_ok,
        "D1_gate": d1_pass,
        "D2_gate": d2_pass,
        "classification": verdict,
    }


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt IT2a-n.txt", file=sys.stderr)
        return 2

    zl = Path(sys.argv[1]).resolve()
    it = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")
    if hashlib.sha256(it.read_bytes()).hexdigest() != IT_SHA256:
        raise RuntimeError("IT2a SHA256 mismatch")

    parser = e.SlotParser()
    validation = e.validate_parser(parser)
    zl_items = e.parse_voynich(zl)
    it_items = e.parse_voynich(it)

    zl_min = run_policy(zl_items, parser, "min", "ZL")
    zl_max = run_policy(zl_items, parser, "max", "ZL")
    it_min = run_policy(it_items, parser, "min", "IT")
    it_max = run_policy(it_items, parser, "max", "IT")

    replay_all = all(
        x["static_replay"]["pass_1e-12"] for x in [zl_min, zl_max, it_min, it_max]
    )
    if not replay_all:
        raise RuntimeError("replay firewall failed")

    primary = classify_primary(zl_min)
    max_sensitivity = classify_primary(zl_max)
    it_min_sensitivity = classify_primary(it_min)
    it_max_sensitivity = classify_primary(it_max)

    here = Path(__file__).resolve().parent
    out = {
        "experiment": "Issue26E7 prospective Guidonian dynamic prediction",
        "issue": 26,
        "inputs": {
            "zl_blob_sha1": e.EXPECTED_ZL3B_BLOB,
            "it_sha256": IT_SHA256,
            "plan_sha256": sha256_file(here / "PLAN_E7.md"),
            "core_sha256": sha256_file(here / "issue26e_core.py"),
            "script_sha256": sha256_file(Path(__file__)),
            "historical_hex_start_rows": list(HEX_START_ROWS),
            "historical_hex_start_semitones": list(HEX_START_SEMITONES),
            "voice_semitone_offsets": list(VOICE_OFFSETS),
        },
        "slot_parser_validation": validation,
        "cell_model_audit": {
            "n_allowed_cells": len(CELL["cell_meta"]),
            "n_hexachords": 7,
            "hex_pitch_sets": [sorted(x) for x in CELL["hex_pitches"]],
            "collapsed_B_rows": [9, 16],
        },
        "ZL_min_primary": zl_min,
        "ZL_max_sensitivity": zl_max,
        "IT_min_transcription_sensitivity": it_min,
        "IT_max_transcription_sensitivity": it_max,
        "replay_firewall_all_four": replay_all,
        "primary_decision": primary,
        "max_policy_descriptive_decision": max_sensitivity,
        "IT_min_descriptive_decision": it_min_sensitivity,
        "IT_max_descriptive_decision": it_max_sensitivity,
        "frozen_classification": primary["classification"],
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
