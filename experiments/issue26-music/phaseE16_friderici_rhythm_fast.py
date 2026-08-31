#!/usr/bin/env python3
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np

import issue26e_core as e
import phaseE15_bacon_biliteral_carrier as b
import phaseE16_friderici_rhythm as m

N = m.N_NULLS
K = len(m.KEYS)


def code_map():
    out = np.zeros((6, 27), dtype=np.int16)
    for pi, perm in enumerate(m.PERMS):
        for raw in range(27):
            a = raw // 9
            c = raw % 9
            d = c // 3
            f = c % 3
            out[pi, raw] = perm[a] * 9 + perm[d] * 3 + perm[f]
    return out


CODEMAP = code_map()
KEY_INDEX = {key: i for i, key in enumerate(m.KEYS)}


def vectorized_null_stats(raw_by_slot, folds, lm):
    leaves = sorted(set().union(*folds))
    leaf_index = {leaf: i for i, leaf in enumerate(leaves)}
    L = len(leaves)

    groups = np.zeros((N, K, L), dtype=np.int32)
    bad = np.zeros((N, K, L), dtype=np.int32)
    cnt = np.zeros((N, K, L), dtype=np.int32)
    nll = np.zeros((N, K, L), dtype=np.float64)

    for slot in sorted(m.CANDIDATE_SLOTS):
        for ri, r in enumerate(raw_by_slot[slot]):
            states = r["states"]
            ln = len(states)
            if ln < 3:
                continue
            li = leaf_index[r["leaf"]]
            batch = np.empty((N, ln), dtype=np.uint8)
            for ni in range(N):
                z = states.copy()
                rng = np.random.default_rng(b.seed32(
                    f"Issue26E16:TernaryShuffle:v1:{ni}:{slot}:{r['paragraph']}:{r['run_index']}"
                ))
                rng.shuffle(z)
                batch[ni] = z

            for phase in range(3):
                ng = (ln - phase) // 3
                if ng <= 0:
                    continue
                z = batch[:, phase:phase + 3 * ng].reshape(N, ng, 3).astype(np.int16)
                rawcode = z[:, :, 0] * 9 + z[:, :, 1] * 3 + z[:, :, 2]
                # mapped shape = permutation × null × group
                mapped = CODEMAP[:, rawcode]
                for pi in range(6):
                    ki = KEY_INDEX[(slot, phase, pi)]
                    codes = mapped[pi]
                    valid = codes < len(m.ALPHABET)
                    groups[:, ki, li] += ng
                    bad[:, ki, li] += ng - valid.sum(axis=1).astype(np.int32)
                    if ng < 4:
                        continue
                    good = valid[:, :-3] & valid[:, 1:-2] & valid[:, 2:-1] & valid[:, 3:]
                    safe = np.where(valid, codes, 0).astype(np.int64)
                    q = (((safe[:, :-3] * len(m.ALPHABET) + safe[:, 1:-2]) * len(m.ALPHABET) + safe[:, 2:-1]) * len(m.ALPHABET) + safe[:, 3:])
                    cnt[:, ki, li] += good.sum(axis=1).astype(np.int32)
                    nll[:, ki, li] += (lm.cost[q] * good).sum(axis=1)

        print(f"vectorized_slot={slot}", file=sys.stderr, flush=True)

    return leaves, groups, bad, nll, cnt


def choose_key(train_g, train_bad, train_nll, train_cnt):
    best = None
    best_i = None
    for ki, (slot, phase, pi) in enumerate(m.KEYS):
        g = int(train_g[ki]); bd = int(train_bad[ki]); c = int(train_cnt[ki])
        inv = bd / g if g else 1.0
        ce = float(train_nll[ki]) / c if c else float("inf")
        t = (inv, ce, slot, phase, tuple(m.PERMS[pi]))
        if best is None or t < best:
            best = t; best_i = ki
    return best_i


def fit_from_arrays(leaves, groups, bad, nll, cnt, folds):
    leaf_index = {leaf: i for i, leaf in enumerate(leaves)}
    total_g = groups.sum(axis=2)
    total_bad = bad.sum(axis=2)
    total_nll = nll.sum(axis=2)
    total_cnt = cnt.sum(axis=2)
    null_rows = []
    null0_details = None

    for ni in range(N):
        selected = []
        fold_rows = []
        pg = pbad = pcnt = 0
        pnll = 0.0
        for fi, held in enumerate(folds):
            hidx = [leaf_index[x] for x in held]
            hg = groups[ni, :, hidx].sum(axis=0)
            hb = bad[ni, :, hidx].sum(axis=0)
            hn = nll[ni, :, hidx].sum(axis=0)
            hc = cnt[ni, :, hidx].sum(axis=0)
            tg = total_g[ni] - hg
            tb = total_bad[ni] - hb
            tn = total_nll[ni] - hn
            tc = total_cnt[ni] - hc
            ki = choose_key(tg, tb, tn, tc)
            key = m.KEYS[ki]
            selected.append(key)
            pg += int(hg[ki]); pbad += int(hb[ki]); pnll += float(hn[ki]); pcnt += int(hc[ki])
            fold_rows.append({
                "fold": fi,
                "slot": int(key[0]),
                "phase": int(key[1]),
                "permutation": list(m.PERMS[key[2]]),
                "held_groups": int(hg[ki]),
                "held_invalid_groups": int(hb[ki]),
                "held_nll": float(hn[ki]),
                "held_scored_chars": int(hc[ki]),
            })
        recurrence = max(Counter(selected).values())
        row = {
            "null_index": ni,
            "pooled_cross_entropy": pnll / pcnt if pcnt else float("inf"),
            "pooled_valid_group_fraction": (pg-pbad) / pg if pg else 0.0,
            "exact_key_recurrence": int(recurrence),
        }
        null_rows.append(row)
        if ni == 0:
            null0_details = {**row, "folds": fold_rows, "selected_keys": selected}
    return null_rows, null0_details


def equivalence_check(raw_by_slot, folds, lm, fast0):
    slow_raw = m.shuffled_by_slot(raw_by_slot, 0)
    slow = m.fit_population(slow_raw, folds, lm)
    checks = {
        "pooled_ce_abs_diff": abs(slow["pooled"]["cross_entropy"] - fast0["pooled_cross_entropy"]),
        "pooled_valid_fraction_abs_diff": abs(slow["pooled"]["valid_group_fraction"] - fast0["pooled_valid_group_fraction"]),
        "recurrence_matches": slow["exact_key_recurrence"] == fast0["exact_key_recurrence"],
        "folds": [],
    }
    ok = (
        checks["pooled_ce_abs_diff"] <= 1e-12
        and checks["pooled_valid_fraction_abs_diff"] <= 1e-12
        and checks["recurrence_matches"]
    )
    for sf, ff in zip(slow["folds"], fast0["folds"]):
        key_ok = (
            sf["slot"] == ff["slot"]
            and sf["phase"] == ff["phase"]
            and sf["permutation"] == ff["permutation"]
        )
        exact_counts = (
            sf["held"]["groups"] == ff["held_groups"]
            and sf["held"]["invalid_groups"] == ff["held_invalid_groups"]
            and sf["held"]["scored_chars"] == ff["held_scored_chars"]
        )
        nll_diff = abs(sf["held"]["nll"] - ff["held_nll"])
        row_ok = key_ok and exact_counts and nll_diff <= 1e-10
        checks["folds"].append({
            "fold": sf["fold"], "key_matches": key_ok,
            "integer_counts_match": exact_counts, "held_nll_abs_diff": nll_diff,
            "passed": row_ok,
        })
        ok = ok and row_ok
    checks["passed"] = bool(ok)
    return checks


def qtile(xs, q):
    return float(np.quantile(np.asarray(xs, dtype=np.float64), q))


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr)
        return 2
    zl = Path(sys.argv[1]).resolve(); root = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b blob mismatch")

    parser = e.SlotParser(); parser_validation = e.validate_parser(parser)
    items = e.parse_voynich(zl); folds = e.physical_leaf_folds(items); universe = set().union(*folds)
    latin_runs, lexicon, latin_meta = b.load_latin(root)
    lm = b.LM4(latin_runs); baseline = b.latin_self_baseline(latin_runs)

    raw_min = {}; pop_min = {}
    for slot in sorted(m.CANDIDATE_SLOTS):
        raw_min[slot], pop_min[slot] = m.build_raw_runs(items, universe, parser, "min", slot)
    target_letters = sum(len(r["states"]) // 3 for r in raw_min[1])
    pos = m.positive_controls(latin_runs, lm, target_letters)
    if not pos["passed"]:
        out = {
            "experiment": "Issue26E16 Friderici three-duration rhythm plaintext probe",
            "implementation": "vectorized-null",
            "classification": "SOLVER INADEQUATE", "positive_control": pos,
            "latin_population": latin_meta, "latin_self_baseline": baseline,
            "candidate_populations": pop_min, "slot_parser_validation": parser_validation,
        }
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True); print(); return 0

    primary = m.summarize(raw_min, folds, lm, lexicon)

    leaves, G, BAD, NLL, CNT = vectorized_null_stats(raw_min, folds, lm)
    nulls, fast0 = fit_from_arrays(leaves, G, BAD, NLL, CNT, folds)
    eq = equivalence_check(raw_min, folds, lm, fast0)
    if not eq["passed"]:
        out = {
            "experiment": "Issue26E16 Friderici three-duration rhythm plaintext probe",
            "implementation": "vectorized-null",
            "classification": "E16 OPTIMIZATION EQUIVALENCE FAILURE",
            "positive_control": pos, "equivalence": eq,
            "primary_min": primary,
            "candidate_populations_min": pop_min,
            "latin_population": latin_meta, "latin_self_baseline": baseline,
            "slot_parser_validation": parser_validation,
        }
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True); print(); return 0

    nce = [x["pooled_cross_entropy"] for x in nulls]
    nv = [x["pooled_valid_group_fraction"] for x in nulls]
    real_ce = primary["pooled"]["cross_entropy"]
    lower = sum(x <= real_ce for x in nce)
    p_lower = (1 + lower) / 201
    med = float(statistics.median(nce)); adv = med - real_ce
    null_summary = {
        "null_count": N, "lower_tail_count": int(lower), "lower_tail_p": float(p_lower),
        "ce_median": med, "ce_q05": qtile(nce, .05), "ce_min": float(min(nce)),
        "real_ce_advantage_below_null_median": float(adv),
        "valid_fraction_median": float(statistics.median(nv)),
        "valid_fraction_q05": qtile(nv, .05), "valid_fraction_q95": qtile(nv, .95),
        "recurrence_distribution": {str(k): int(v) for k, v in sorted(Counter(x["exact_key_recurrence"] for x in nulls).items())},
    }

    dg = primary["diagnostics"]; pooled = primary["pooled"]
    gates = {
        "exact_key_recurrence_ge4": primary["exact_key_recurrence"] >= 4,
        "valid_group_fraction_ge_0_95": pooled["valid_group_fraction"] >= .95,
        "ce_within_latin_plus_0_50": pooled["cross_entropy"] <= baseline["mean_cross_entropy"] + .50,
        "top5_within_latin_plus_0_15": dg["top5_char_fraction"] <= baseline["pooled_top5_char_fraction"] + .15,
        "distinct_words_ge6_ge10": dg["distinct_words_ge6_count"] >= 10,
        "long_words_across_ge3_folds": dg["folds_with_words_ge6"] >= 3,
        "order_null_p_le_0_01": p_lower <= .01,
        "real_ce_at_least_0_10_below_null_median": adv >= .10,
    }
    classification = "FRIDERICI RHYTHM PLAINTEXT LEAD" if all(gates.values()) else "NO READABLE FRIDERICI RHYTHM PLAINTEXT"
    flags = []
    if pooled["valid_group_fraction"] < .80: flags.append("LOW-VALIDITY")
    if dg["top5_char_fraction"] >= .90: flags.append("LOW-DIVERSITY OPTIMUM")

    raw_max = {}; pop_max = {}
    for slot in sorted(m.CANDIDATE_SLOTS):
        raw_max[slot], pop_max[slot] = m.build_raw_runs(items, universe, parser, "max", slot)
    sensitivity = m.summarize(raw_max, folds, lm, lexicon)

    out = {
        "experiment": "Issue26E16 Friderici three-duration rhythm plaintext probe",
        "implementation": "vectorized-null with null0 slow-path equivalence gate",
        "classification": classification, "flags": flags,
        "equivalence": eq,
        "historical_alphabet": "".join(m.ALPHABET),
        "historical_duration_ranks": ["whole", "half", "quarter"],
        "unused_ternary_patterns": ["220", "221", "222"],
        "candidate_slots": {str(k): list(v) for k, v in m.CANDIDATE_SLOTS.items()},
        "key_count": len(m.KEYS), "positive_control": pos,
        "latin_population": latin_meta, "latin_self_baseline": baseline,
        "slot_parser_validation": parser_validation,
        "candidate_populations_min": pop_min, "primary_min": primary,
        "order_null_summary": null_summary, "order_nulls": nulls,
        "gates": gates,
        "candidate_populations_max": pop_max, "max_sensitivity": sensitivity,
        "seed_namespace": "Issue26E16:TernaryShuffle:v1:<null>:<slot>:<paragraph_id>:<run_index>",
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True); print(); return 0


if __name__ == "__main__":
    raise SystemExit(main())
