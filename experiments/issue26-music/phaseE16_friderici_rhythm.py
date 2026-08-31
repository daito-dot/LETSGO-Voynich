#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

import issue26e_core as e
import phaseE15_bacon_biliteral_carrier as b

ALPHABET = b.ALPHABET
A = len(ALPHABET)
PERMS = tuple(itertools.permutations(range(3)))
CANDIDATE_SLOTS = {
    1: ("", "o", "y"),
    2: ("", "l", "r"),
    4: ("", "ch", "sh"),
    7: ("", "s", "d"),
    8: ("", "o", "a"),
}
KEYS = tuple((slot, phase, pi) for slot in sorted(CANDIDATE_SLOTS) for phase in range(3) for pi in range(6))
N_NULLS = 200
assert len(ALPHABET) == 24 and len(PERMS) == 6 and len(KEYS) == 90


def trits_for_letter(idx: int):
    return np.asarray([idx // 9, (idx // 3) % 3, idx % 3], dtype=np.uint8)


def build_raw_runs(items, leaves, parser, policy, slot):
    states = CANDIDATE_SLOTS[slot]
    si = {v: i for i, v in enumerate(states)}
    out = []
    visible = parsed = 0
    for it in items:
        if it["leaf"] not in leaves:
            continue
        cur = []
        run_index = 0

        def flush():
            nonlocal cur, run_index
            if cur:
                out.append({
                    "leaf": it["leaf"], "page": it["page"], "paragraph": it["id"],
                    "run_index": run_index, "states": np.asarray(cur, dtype=np.uint8),
                })
                run_index += 1
            cur = []

        for line in it["lines"]:
            for tok in line:
                visible += 1
                p = parser.pick(tok, policy)
                if p is None:
                    flush()
                    continue
                state = p[1][slot]
                if state not in si:
                    raise RuntimeError(f"unexpected slot{slot} state {state!r}")
                cur.append(si[state])
                parsed += 1
        flush()
    return out, {
        "slot": slot,
        "states": list(states),
        "visible_tokens": visible,
        "parsed_carriers": parsed,
        "parse_coverage": parsed / visible if visible else 0.0,
        "carrier_runs": len(out),
        "carrier_states": sum(len(x["states"]) for x in out),
    }


def grouped_codes(states: np.ndarray, phase: int, perm):
    if len(states) <= phase:
        return np.empty(0, dtype=np.int16)
    z = states[phase:]
    n = len(z) // 3
    if n <= 0:
        return np.empty(0, dtype=np.int16)
    raw = z[:n*3].reshape(n, 3)
    mapped = np.take(np.asarray(perm, dtype=np.int16), raw)
    return mapped[:, 0] * 9 + mapped[:, 1] * 3 + mapped[:, 2]


def stats_one(states, phase, perm, lm):
    codes = grouped_codes(states, phase, perm)
    total = int(len(codes))
    invalid = int(np.count_nonzero(codes >= A))
    if total < 4:
        return total, invalid, 0.0, 0
    good = (codes[:-3] < A) & (codes[1:-2] < A) & (codes[2:-1] < A) & (codes[3:] < A)
    if not np.any(good):
        return total, invalid, 0.0, 0
    aa = codes[:-3][good].astype(np.int64)
    bb = codes[1:-2][good].astype(np.int64)
    cc = codes[2:-1][good].astype(np.int64)
    dd = codes[3:][good].astype(np.int64)
    q = (((aa * A + bb) * A + cc) * A + dd)
    return total, invalid, float(lm.cost[q].sum()), int(len(q))


def leaf_key_stats(raw_by_slot, lm):
    out = {}
    for slot, runs in raw_by_slot.items():
        for phase in range(3):
            for pi, perm in enumerate(PERMS):
                d = defaultdict(lambda: [0, 0, 0.0, 0])
                for r in runs:
                    g, bad, nll, n = stats_one(r["states"], phase, perm, lm)
                    z = d[r["leaf"]]
                    z[0] += g; z[1] += bad; z[2] += nll; z[3] += n
                out[(slot, phase, pi)] = d
    return out


def combine_leaf_stats(by_leaf, leaves):
    g = bad = n = 0
    nll = 0.0
    for leaf in leaves:
        if leaf not in by_leaf:
            continue
        x = by_leaf[leaf]
        g += int(x[0]); bad += int(x[1]); nll += float(x[2]); n += int(x[3])
    return {
        "groups": g,
        "invalid_groups": bad,
        "valid_group_fraction": (g-bad)/g if g else 0.0,
        "invalid_group_fraction": bad/g if g else 1.0,
        "nll": nll,
        "scored_chars": n,
        "cross_entropy": nll/n if n else float("inf"),
    }


def fit_population(raw_by_slot, folds, lm):
    universe = set().union(*folds)
    stats = leaf_key_stats(raw_by_slot, lm)
    selected = []
    fold_rows = []
    for fi, held in enumerate(folds):
        train = universe - held
        cand = []
        for slot, phase, pi in KEYS:
            s = combine_leaf_stats(stats[(slot, phase, pi)], train)
            cand.append((s["invalid_group_fraction"], s["cross_entropy"], slot, phase, tuple(PERMS[pi]), pi, s))
        best = min(cand, key=lambda x: (x[0], x[1], x[2], x[3], x[4]))
        slot, phase, pi = int(best[2]), int(best[3]), int(best[5])
        key = (slot, phase, pi)
        selected.append(key)
        held_s = combine_leaf_stats(stats[key], held)
        fold_rows.append({
            "fold": fi, "held_leaves": sorted(held), "slot": slot, "phase": phase,
            "permutation": list(PERMS[pi]), "training": best[6], "held": held_s,
        })
    rec = Counter(selected)
    modal, recurrence = min(rec.items(), key=lambda kv: (-kv[1], kv[0]))
    pooled = {"groups": 0, "invalid_groups": 0, "nll": 0.0, "scored_chars": 0}
    for row in fold_rows:
        h = row["held"]
        for k in ("groups", "invalid_groups", "scored_chars"):
            pooled[k] += int(h[k])
        pooled["nll"] += float(h["nll"])
    pooled["valid_group_fraction"] = (pooled["groups"]-pooled["invalid_groups"])/pooled["groups"] if pooled["groups"] else 0.0
    pooled["invalid_group_fraction"] = pooled["invalid_groups"]/pooled["groups"] if pooled["groups"] else 1.0
    pooled["cross_entropy"] = pooled["nll"]/pooled["scored_chars"] if pooled["scored_chars"] else float("inf")
    return {
        "selected_keys": selected,
        "exact_key_recurrence": int(recurrence),
        "modal_key": {"slot": int(modal[0]), "phase": int(modal[1]), "permutation": list(PERMS[modal[2]])},
        "folds": fold_rows,
        "pooled": pooled,
    }


def decode_one_run(r, phase, perm, fold=None):
    codes = grouped_codes(r["states"], phase, perm)
    rows = []
    cur = []
    seg = 0
    for x in codes:
        x = int(x)
        if x >= A:
            if cur:
                rows.append({
                    "fold": fold, "page": r["page"], "paragraph": r["paragraph"],
                    "run_index": r["run_index"], "decoded_segment": seg,
                    "text": "".join(ALPHABET[q] for q in cur),
                })
                seg += 1; cur = []
        else:
            cur.append(x)
    if cur:
        rows.append({
            "fold": fold, "page": r["page"], "paragraph": r["paragraph"],
            "run_index": r["run_index"], "decoded_segment": seg,
            "text": "".join(ALPHABET[q] for q in cur),
        })
    return rows


def selected_rows(raw_by_slot, folds, selected_keys):
    rows = []
    for fi, held in enumerate(folds):
        slot, phase, pi = selected_keys[fi]
        for r in raw_by_slot[slot]:
            if r["leaf"] in held:
                rows.extend(decode_one_run(r, phase, PERMS[pi], fi))
    return rows


def summarize(raw_by_slot, folds, lm, lexicon):
    fit = fit_population(raw_by_slot, folds, lm)
    rows = selected_rows(raw_by_slot, folds, fit["selected_keys"])
    return {**fit, "diagnostics": b.diagnostics(rows, lm, lexicon)}


def make_control_runs(latin_runs, target_letters, hidden_phase, hidden_pi, label):
    perm = PERMS[hidden_pi]
    inv = np.empty(3, dtype=np.uint8)
    for raw, duration in enumerate(perm):
        inv[duration] = raw
    out = []
    total = 0
    for ri, s in enumerate(latin_runs):
        if total >= target_letters:
            break
        take = min(len(s), target_letters-total)
        if take <= 0:
            break
        text = s[:take]
        durations = np.concatenate([trits_for_letter(b.AI[c]) for c in text]) if text else np.empty(0, dtype=np.uint8)
        states = inv[durations]
        rng = np.random.default_rng(b.seed32(f"{label}:prefix:{ri}"))
        prefix = rng.integers(0, 3, size=hidden_phase, dtype=np.uint8)
        out.append({"states": np.concatenate([prefix, states]), "truth": np.asarray([b.AI[c] for c in text], dtype=np.int16)})
        total += take
    if total < target_letters:
        raise RuntimeError(f"control Latin capacity {total} < {target_letters}")
    return out


def control_metric(runs, indices, phase, pi, lm):
    g = bad = n = 0
    nll = 0.0
    perm = PERMS[pi]
    for i in indices:
        a, z, c, d = stats_one(runs[i]["states"], phase, perm, lm)
        g += a; bad += z; nll += c; n += d
    return {
        "groups": g, "invalid": bad,
        "invalid_fraction": bad/g if g else 1.0,
        "ce": nll/n if n else float("inf"), "nll": nll, "scored": n,
    }


def control_accuracy(runs, indices, phase, pi):
    correct = total = valid = 0
    perm = PERMS[pi]
    for i in indices:
        pred = grouped_codes(runs[i]["states"], phase, perm)
        truth = runs[i]["truth"]
        m = min(len(pred), len(truth))
        total += len(truth)
        if m:
            valid += int(np.count_nonzero(pred[:m] < A))
            correct += int(np.count_nonzero(pred[:m] == truth[:m]))
    return correct/total if total else 0.0, valid/total if total else 0.0


def positive_controls(latin_runs, lm, target_letters):
    results = []
    target = min(max(5000, target_letters), 30000)
    for ci in range(5):
        rng = np.random.default_rng(b.seed32(f"Issue26E16:Positive:v1:{ci}"))
        hidden_phase = int(rng.integers(0, 3))
        hidden_pi = int(rng.integers(0, 6))
        off = (ci * 997) % len(latin_runs)
        rotated = latin_runs[off:] + latin_runs[:off]
        runs = make_control_runs(rotated, target, hidden_phase, hidden_pi, f"Issue26E16:Positive:v1:{ci}")
        held = [i for i in range(len(runs)) if i % 5 == ci]
        train = [i for i in range(len(runs)) if i % 5 != ci]
        cand = []
        for phase in range(3):
            for pi in range(6):
                m = control_metric(runs, train, phase, pi, lm)
                cand.append((m["invalid_fraction"], m["ce"], phase, tuple(PERMS[pi]), pi, m))
        best = min(cand, key=lambda x: (x[0], x[1], x[2], x[3]))
        phase, pi = int(best[2]), int(best[4])
        acc, valid = control_accuracy(runs, held, phase, pi)
        rec = control_metric(runs, held, phase, pi, lm)
        tru = control_metric(runs, held, hidden_phase, hidden_pi, lm)
        results.append({
            "control": ci, "hidden_phase": hidden_phase, "hidden_permutation": list(PERMS[hidden_pi]),
            "selected_phase": phase, "selected_permutation": list(PERMS[pi]),
            "exact_key": bool((phase, pi) == (hidden_phase, hidden_pi)),
            "decoded_letter_accuracy": acc, "valid_group_fraction": valid,
            "recovered_held_ce": rec["ce"], "true_held_ce": tru["ce"],
            "held_ce_excess": rec["ce"] - tru["ce"],
        })
    exact = sum(x["exact_key"] for x in results)
    mean_acc = statistics.fmean(x["decoded_letter_accuracy"] for x in results)
    mean_valid = statistics.fmean(x["valid_group_fraction"] for x in results)
    mean_excess = statistics.fmean(x["held_ce_excess"] for x in results)
    passed = exact >= 4 and mean_acc >= .99 and mean_valid >= .99 and mean_excess <= .02
    return {
        "passed": passed, "exact_key_controls": exact,
        "mean_decoded_letter_accuracy": mean_acc,
        "mean_valid_group_fraction": mean_valid,
        "mean_ce_excess": mean_excess, "controls": results,
    }


def shuffled_by_slot(raw_by_slot, null_index):
    out = {}
    for slot, runs in raw_by_slot.items():
        rows = []
        for r in runs:
            states = r["states"].copy()
            rng = np.random.default_rng(b.seed32(
                f"Issue26E16:TernaryShuffle:v1:{null_index}:{slot}:{r['paragraph']}:{r['run_index']}"
            ))
            rng.shuffle(states)
            q = dict(r); q["states"] = states; rows.append(q)
        out[slot] = rows
    return out


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
    for slot in sorted(CANDIDATE_SLOTS):
        raw_min[slot], pop_min[slot] = build_raw_runs(items, universe, parser, "min", slot)
    target_letters = sum(len(r["states"]) // 3 for r in raw_min[1])
    pos = positive_controls(latin_runs, lm, target_letters)
    if not pos["passed"]:
        out = {
            "experiment": "Issue26E16 Friderici three-duration rhythm plaintext probe",
            "classification": "SOLVER INADEQUATE", "positive_control": pos,
            "latin_population": latin_meta, "latin_self_baseline": baseline,
            "candidate_populations": pop_min, "slot_parser_validation": parser_validation,
        }
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True); print(); return 0

    primary = summarize(raw_min, folds, lm, lexicon)

    nulls = []
    for ni in range(N_NULLS):
        nr = shuffled_by_slot(raw_min, ni)
        nf = fit_population(nr, folds, lm)
        nulls.append({
            "null_index": ni,
            "pooled_cross_entropy": nf["pooled"]["cross_entropy"],
            "pooled_valid_group_fraction": nf["pooled"]["valid_group_fraction"],
            "exact_key_recurrence": nf["exact_key_recurrence"],
        })
        if (ni + 1) % 20 == 0:
            print(f"completed_nulls={ni+1}/{N_NULLS}", file=sys.stderr, flush=True)

    nce = [x["pooled_cross_entropy"] for x in nulls]
    nv = [x["pooled_valid_group_fraction"] for x in nulls]
    real_ce = primary["pooled"]["cross_entropy"]
    lower = sum(x <= real_ce for x in nce)
    p_lower = (1 + lower) / 201
    med = float(statistics.median(nce)); adv = med - real_ce
    null_summary = {
        "null_count": N_NULLS, "lower_tail_count": int(lower), "lower_tail_p": float(p_lower),
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
    for slot in sorted(CANDIDATE_SLOTS):
        raw_max[slot], pop_max[slot] = build_raw_runs(items, universe, parser, "max", slot)
    sensitivity = summarize(raw_max, folds, lm, lexicon)

    out = {
        "experiment": "Issue26E16 Friderici three-duration rhythm plaintext probe",
        "classification": classification, "flags": flags,
        "historical_alphabet": "".join(ALPHABET),
        "historical_duration_ranks": ["whole", "half", "quarter"],
        "unused_ternary_patterns": ["220", "221", "222"],
        "candidate_slots": {str(k): list(v) for k, v in CANDIDATE_SLOTS.items()},
        "key_count": len(KEYS), "positive_control": pos,
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
