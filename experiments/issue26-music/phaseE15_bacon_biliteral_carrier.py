#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

import issue26e_core as e

ALPHABET = tuple("abcdefghiklmnopqrstuwxyz")
AI = {c: i for i, c in enumerate(ALPHABET)}
A = len(ALPHABET)
ALPHA = .1
CREMMA_DIRS = ("data/BIS-193", "data/CLM13027", "data/Mazarine915", "data/UBL758")
KEYS = tuple((phase, orient) for phase in range(5) for orient in range(2))
WEIGHTS = np.asarray([16, 8, 4, 2, 1], dtype=np.int16)
N_NULLS = 200
assert A == 24 and len(KEYS) == 10


def seed32(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode()).digest()[:4], "big") & 0x7fffffff


def norm_letter(ch: str):
    s = unicodedata.normalize("NFKD", ch.lower())
    s = "".join(c for c in s if "a" <= c <= "z")
    if not s:
        return None
    c = s[0]
    if c == "j":
        c = "i"
    elif c == "v":
        c = "u"
    return c if c in AI else None


def load_latin(root: Path):
    runs = []
    lexicon = Counter()
    files = 0
    for rel in CREMMA_DIRS:
        d = root / rel
        if not d.is_dir():
            raise RuntimeError(f"missing CREMMA dir {d}")
        for p in sorted(d.rglob("*.txt")):
            files += 1
            text = p.read_text(encoding="utf-8", errors="replace")
            for raw in text.splitlines():
                cur = []
                for ch in raw:
                    c = norm_letter(ch)
                    if c is None:
                        if len(cur) >= 4:
                            runs.append("".join(cur))
                        cur = []
                    else:
                        cur.append(c)
                if len(cur) >= 4:
                    runs.append("".join(cur))
            for tok in re.findall(r"[A-Za-zÀ-ÿ]+", text):
                w = "".join(c for c in (norm_letter(x) for x in tok) if c is not None)
                if len(w) >= 4 and all(c in AI for c in w):
                    lexicon[w] += 1
    if not runs:
        raise RuntimeError("no Latin runs")
    return runs, lexicon, {
        "files": files,
        "runs": len(runs),
        "chars": sum(map(len, runs)),
        "lexicon": len(lexicon),
        "alphabet": "".join(ALPHABET),
    }


class LM4:
    def __init__(self, runs):
        c3 = np.zeros(A ** 3, dtype=np.int64)
        c4 = np.zeros(A ** 4, dtype=np.int64)
        self.c4_counter = Counter()
        for s in runs:
            xs = np.asarray([AI[c] for c in s], dtype=np.int16)
            if len(xs) < 4:
                continue
            for i in range(3, len(xs)):
                h = (int(xs[i-3]) * A + int(xs[i-2])) * A + int(xs[i-1])
                q = h * A + int(xs[i])
                c3[h] += 1
                c4[q] += 1
                self.c4_counter[s[i-3:i+1]] += 1
        cost = np.empty(A ** 4, dtype=np.float64)
        for h in range(A ** 3):
            den = c3[h] + ALPHA * A
            base = h * A
            cost[base:base+A] = -np.log2((c4[base:base+A] + ALPHA) / den)
        self.cost = cost

    def score_code_runs(self, runs):
        nll = 0.0
        n = 0
        for xs in runs:
            if len(xs) < 4:
                continue
            a = xs[:-3].astype(np.int64)
            b = xs[1:-2].astype(np.int64)
            c = xs[2:-1].astype(np.int64)
            d = xs[3:].astype(np.int64)
            q = (((a * A + b) * A + c) * A + d)
            nll += float(self.cost[q].sum())
            n += int(len(q))
        return (nll / n if n else float("inf")), n, nll

    def score_texts(self, texts):
        return self.score_code_runs([np.asarray([AI[c] for c in s], dtype=np.int16) for s in texts])


def top5_fraction_texts(texts):
    c = Counter("".join(texts))
    n = sum(c.values())
    return sum(v for _, v in c.most_common(5)) / n if n else 1.0


def latin_self_baseline(runs):
    rows = []
    for f in range(5):
        train = [s for i, s in enumerate(runs) if i % 5 != f]
        held = [s for i, s in enumerate(runs) if i % 5 == f]
        lm = LM4(train)
        ce, n, _ = lm.score_texts(held)
        rows.append({
            "fold": f,
            "cross_entropy": ce,
            "scored_chars": n,
            "top5_char_fraction": top5_fraction_texts(held),
        })
    return {
        "mean_cross_entropy": statistics.fmean(x["cross_entropy"] for x in rows),
        "pooled_top5_char_fraction": top5_fraction_texts(runs),
        "folds": rows,
    }


def build_raw_runs(items, leaves, parser, policy):
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
                    "leaf": it["leaf"],
                    "page": it["page"],
                    "paragraph": it["id"],
                    "run_index": run_index,
                    "bits": np.asarray(cur, dtype=np.uint8),
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
                vals = p[1]
                state = vals[11]
                if state == "":
                    bit = 0
                elif state == "y":
                    bit = 1
                else:
                    raise RuntimeError(f"unexpected slot11 state {state!r}")
                cur.append(bit)
                parsed += 1
        flush()
    return out, {
        "visible_tokens": visible,
        "parsed_carriers": parsed,
        "parse_coverage": parsed / visible if visible else 0.0,
        "carrier_runs": len(out),
        "carrier_bits": sum(len(x["bits"]) for x in out),
    }


def grouped_codes(bits: np.ndarray, phase: int, orient: int):
    if len(bits) <= phase:
        return np.empty(0, dtype=np.int16)
    z = bits[phase:]
    n = len(z) // 5
    if n <= 0:
        return np.empty(0, dtype=np.int16)
    z = z[:n*5].reshape(n, 5).astype(np.int16)
    if orient:
        z = 1 - z
    return z @ WEIGHTS


def stats_one(bits, phase, orient, lm):
    codes = grouped_codes(bits, phase, orient)
    total = int(len(codes))
    invalid = int(np.count_nonzero(codes >= A))
    if total < 4:
        return total, invalid, 0.0, 0
    valid4 = (codes[:-3] < A) & (codes[1:-2] < A) & (codes[2:-1] < A) & (codes[3:] < A)
    if not np.any(valid4):
        return total, invalid, 0.0, 0
    a = codes[:-3][valid4].astype(np.int64)
    b = codes[1:-2][valid4].astype(np.int64)
    c = codes[2:-1][valid4].astype(np.int64)
    d = codes[3:][valid4].astype(np.int64)
    q = (((a * A + b) * A + c) * A + d)
    return total, invalid, float(lm.cost[q].sum()), int(len(q))


def leaf_key_stats(raw_runs, lm):
    out = {k: defaultdict(lambda: [0, 0, 0.0, 0]) for k in KEYS}
    for r in raw_runs:
        leaf = r["leaf"]
        for k in KEYS:
            g, bad, nll, n = stats_one(r["bits"], k[0], k[1], lm)
            z = out[k][leaf]
            z[0] += g
            z[1] += bad
            z[2] += nll
            z[3] += n
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
        "valid_group_fraction": (g - bad) / g if g else 0.0,
        "invalid_group_fraction": bad / g if g else 1.0,
        "nll": nll,
        "scored_chars": n,
        "cross_entropy": nll / n if n else float("inf"),
    }


def fit_population(raw_runs, folds, lm):
    universe = set().union(*folds)
    stats = leaf_key_stats(raw_runs, lm)
    selected = []
    fold_rows = []
    for fi, held in enumerate(folds):
        train = universe - held
        candidates = []
        for phase, orient in KEYS:
            s = combine_leaf_stats(stats[(phase, orient)], train)
            candidates.append((s["invalid_group_fraction"], s["cross_entropy"], phase, orient, s))
        best = min(candidates, key=lambda x: (x[0], x[1], x[2], x[3]))
        phase, orient = int(best[2]), int(best[3])
        selected.append((phase, orient))
        held_s = combine_leaf_stats(stats[(phase, orient)], held)
        fold_rows.append({
            "fold": fi,
            "held_leaves": sorted(held),
            "phase": phase,
            "orientation": orient,
            "orientation_label": "EMPTY=a,y=b" if orient == 0 else "EMPTY=b,y=a",
            "training": best[4],
            "held": held_s,
        })
    rec = Counter(selected)
    modal, recurrence = min(rec.items(), key=lambda kv: (-kv[1], kv[0]))
    pooled = {"groups": 0, "invalid_groups": 0, "nll": 0.0, "scored_chars": 0}
    for f, key in zip(fold_rows, selected):
        h = f["held"]
        pooled["groups"] += h["groups"]
        pooled["invalid_groups"] += h["invalid_groups"]
        pooled["nll"] += h["nll"]
        pooled["scored_chars"] += h["scored_chars"]
    pooled["valid_group_fraction"] = ((pooled["groups"] - pooled["invalid_groups"]) / pooled["groups"] if pooled["groups"] else 0.0)
    pooled["invalid_group_fraction"] = (pooled["invalid_groups"] / pooled["groups"] if pooled["groups"] else 1.0)
    pooled["cross_entropy"] = (pooled["nll"] / pooled["scored_chars"] if pooled["scored_chars"] else float("inf"))
    return {
        "selected_keys": selected,
        "exact_key_recurrence": int(recurrence),
        "modal_key": {"phase": int(modal[0]), "orientation": int(modal[1])},
        "folds": fold_rows,
        "pooled": pooled,
    }


def decode_one_run(r, phase, orient, fold=None):
    codes = grouped_codes(r["bits"], phase, orient)
    rows = []
    cur = []
    seg = 0
    for code in codes:
        code = int(code)
        if code >= A:
            if cur:
                text = "".join(ALPHABET[x] for x in cur)
                rows.append({
                    "fold": fold, "page": r["page"], "paragraph": r["paragraph"],
                    "run_index": r["run_index"], "decoded_segment": seg, "text": text,
                })
                seg += 1; cur = []
        else:
            cur.append(code)
    if cur:
        text = "".join(ALPHABET[x] for x in cur)
        rows.append({
            "fold": fold, "page": r["page"], "paragraph": r["paragraph"],
            "run_index": r["run_index"], "decoded_segment": seg, "text": text,
        })
    return rows


def selected_decoded_rows(raw_runs, folds, selected_keys):
    rows = []
    for fi, held in enumerate(folds):
        phase, orient = selected_keys[fi]
        for r in raw_runs:
            if r["leaf"] in held:
                rows.extend(decode_one_run(r, phase, orient, fi))
    return rows


def lexicon_hits(rows, lexicon, cap=100):
    hits = []
    for row in rows:
        s = row["text"]
        for i in range(len(s)):
            for ln in range(4, min(15, len(s)-i) + 1):
                w = s[i:i+ln]
                freq = lexicon.get(w, 0)
                if freq:
                    hits.append({
                        "word": w, "length": ln, "corpus_frequency": int(freq),
                        "fold": row.get("fold"), "page": row.get("page"),
                        "paragraph": row.get("paragraph"), "offset": i,
                        "context": s[max(0, i-10):min(len(s), i+ln+10)],
                    })
    hits.sort(key=lambda x: (-x["length"], -x["corpus_frequency"], x["word"], str(x["page"]), x["offset"]))
    return hits[:cap]


def diagnostics(rows, lm, lexicon):
    texts = [x["text"] for x in rows]
    ce, n, _ = lm.score_texts(texts)
    chars = Counter("".join(texts))
    total = sum(chars.values())
    hits = lexicon_hits(rows, lexicon)
    long_words = sorted({x["word"] for x in hits if x["length"] >= 6})
    word_folds = sorted({x["fold"] for x in hits if x["length"] >= 6 and x.get("fold") is not None})
    grams = Counter()
    for s in texts:
        grams.update(s[i:i+4] for i in range(len(s)-3))
    return {
        "cross_entropy": ce,
        "scored_chars": n,
        "decoded_chars": total,
        "top5_char_fraction": sum(v for _, v in chars.most_common(5)) / total if total else 1.0,
        "char_counts": dict(chars.most_common()),
        "samples": [x for x in rows if len(x["text"]) >= 12][:20],
        "lexicon_hits": hits,
        "distinct_words_ge6": long_words,
        "distinct_words_ge6_count": len(long_words),
        "folds_with_words_ge6": len(word_folds),
        "word_folds_ge6": word_folds,
        "top_4grams": [
            {"ngram": g, "decoded_count": int(c), "latin_count": int(lm.c4_counter.get(g, 0))}
            for g, c in grams.most_common(50)
        ],
    }


def literal_phase0(raw_runs, lm, lexicon):
    rows = []
    for orient in (0, 1):
        all_rows = []
        groups = invalid = 0
        for r in raw_runs:
            codes = grouped_codes(r["bits"], 0, orient)
            groups += len(codes); invalid += int(np.count_nonzero(codes >= A))
            all_rows.extend(decode_one_run(r, 0, orient, None))
        dg = diagnostics(all_rows, lm, lexicon)
        rows.append({
            "phase": 0, "orientation": orient,
            "orientation_label": "EMPTY=a,y=b" if orient == 0 else "EMPTY=b,y=a",
            "groups": int(groups), "invalid_groups": int(invalid),
            "valid_group_fraction": (groups-invalid)/groups if groups else 0.0,
            "diagnostics": dg,
        })
    return rows


def encode_letter_code(idx):
    return np.asarray([(idx >> s) & 1 for s in (4, 3, 2, 1, 0)], dtype=np.uint8)


def make_control_runs(latin_runs, target_letters, hidden_phase, hidden_orient, label):
    out = []
    total = 0
    for ri, s in enumerate(latin_runs):
        if total >= target_letters:
            break
        take = min(len(s), target_letters-total)
        if take <= 0:
            break
        text = s[:take]
        bits = np.concatenate([encode_letter_code(AI[c]) for c in text]) if text else np.empty(0, dtype=np.uint8)
        if hidden_orient:
            bits = 1 - bits
        rng = np.random.default_rng(seed32(f"{label}:prefix:{ri}"))
        prefix = rng.integers(0, 2, size=hidden_phase, dtype=np.uint8)
        out.append({"bits": np.concatenate([prefix, bits]), "truth": np.asarray([AI[c] for c in text], dtype=np.int16), "index": ri})
        total += take
    if total < target_letters:
        raise RuntimeError(f"control Latin capacity {total} < {target_letters}")
    return out


def control_metric(runs, indices, phase, orient, lm):
    groups = invalid = n = 0
    nll = 0.0
    for i in indices:
        g, bad, z, m = stats_one(runs[i]["bits"], phase, orient, lm)
        groups += g; invalid += bad; nll += z; n += m
    return {
        "groups": groups, "invalid": invalid,
        "invalid_fraction": invalid/groups if groups else 1.0,
        "ce": nll/n if n else float("inf"), "nll": nll, "scored": n,
    }


def control_accuracy(runs, indices, phase, orient):
    correct = total = valid = 0
    for i in indices:
        pred = grouped_codes(runs[i]["bits"], phase, orient)
        truth = runs[i]["truth"]
        total += len(truth)
        m = min(len(pred), len(truth))
        if m:
            valid += int(np.count_nonzero(pred[:m] < A))
            correct += int(np.count_nonzero(pred[:m] == truth[:m]))
    return correct/total if total else 0.0, valid/total if total else 0.0


def positive_controls(latin_runs, lm, target_letters):
    results = []
    target = min(max(5000, target_letters), 30000)
    for ci in range(5):
        rng = np.random.default_rng(seed32(f"Issue26E15:Positive:v1:{ci}"))
        hidden_phase = int(rng.integers(0, 5))
        hidden_orient = int(rng.integers(0, 2))
        rotated = latin_runs[(ci*997) % len(latin_runs):] + latin_runs[:(ci*997) % len(latin_runs)]
        runs = make_control_runs(rotated, target, hidden_phase, hidden_orient, f"Issue26E15:Positive:v1:{ci}")
        held_idx = [i for i in range(len(runs)) if i % 5 == ci]
        train_idx = [i for i in range(len(runs)) if i % 5 != ci]
        candidates = []
        for phase, orient in KEYS:
            m = control_metric(runs, train_idx, phase, orient, lm)
            candidates.append((m["invalid_fraction"], m["ce"], phase, orient, m))
        best = min(candidates, key=lambda x: (x[0], x[1], x[2], x[3]))
        phase, orient = int(best[2]), int(best[3])
        acc, valid = control_accuracy(runs, held_idx, phase, orient)
        rec = control_metric(runs, held_idx, phase, orient, lm)
        true = control_metric(runs, held_idx, hidden_phase, hidden_orient, lm)
        results.append({
            "control": ci,
            "hidden_phase": hidden_phase, "hidden_orientation": hidden_orient,
            "selected_phase": phase, "selected_orientation": orient,
            "exact_key": bool((phase, orient) == (hidden_phase, hidden_orient)),
            "decoded_letter_accuracy": acc,
            "valid_group_fraction": valid,
            "recovered_held_ce": rec["ce"], "true_held_ce": true["ce"],
            "held_ce_excess": rec["ce"] - true["ce"],
        })
    exact = sum(x["exact_key"] for x in results)
    mean_acc = statistics.fmean(x["decoded_letter_accuracy"] for x in results)
    mean_valid = statistics.fmean(x["valid_group_fraction"] for x in results)
    mean_excess = statistics.fmean(x["held_ce_excess"] for x in results)
    passed = exact >= 4 and mean_acc >= .99 and mean_valid >= .99 and mean_excess <= .02
    return {
        "passed": passed,
        "exact_key_controls": exact,
        "mean_decoded_letter_accuracy": mean_acc,
        "mean_valid_group_fraction": mean_valid,
        "mean_ce_excess": mean_excess,
        "controls": results,
    }


def shuffled_runs(raw_runs, null_index):
    out = []
    for r in raw_runs:
        bits = r["bits"].copy()
        rng = np.random.default_rng(seed32(
            f"Issue26E15:BitShuffle:v1:{null_index}:{r['paragraph']}:{r['run_index']}"
        ))
        rng.shuffle(bits)
        q = dict(r); q["bits"] = bits; out.append(q)
    return out


def qtile(xs, q):
    return float(np.quantile(np.asarray(xs, dtype=np.float64), q))


def summarize_policy(raw_runs, folds, lm, lexicon):
    fit = fit_population(raw_runs, folds, lm)
    rows = selected_decoded_rows(raw_runs, folds, fit["selected_keys"])
    dg = diagnostics(rows, lm, lexicon)
    return {**fit, "diagnostics": dg}


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt CREMMA_ROOT", file=sys.stderr)
        return 2
    zl = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b blob mismatch")

    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)
    items = e.parse_voynich(zl)
    folds = e.physical_leaf_folds(items)
    universe = set().union(*folds)
    latin_runs, lexicon, latin_meta = load_latin(root)
    lm = LM4(latin_runs)
    baseline = latin_self_baseline(latin_runs)

    raw_min, cov_min = build_raw_runs(items, universe, parser, "min")
    target_letters = sum(len(r["bits"]) // 5 for r in raw_min)
    pos = positive_controls(latin_runs, lm, target_letters)
    if not pos["passed"]:
        out = {
            "experiment": "Issue26E15 Bacon biliteral two-difference musical-carrier probe",
            "classification": "SOLVER INADEQUATE",
            "positive_control": pos,
            "latin_population": latin_meta,
            "latin_self_baseline": baseline,
            "primary_population": cov_min,
            "slot_parser_validation": parser_validation,
        }
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True); print(); return 0

    primary = summarize_policy(raw_min, folds, lm, lexicon)
    literal = literal_phase0(raw_min, lm, lexicon)

    null_rows = []
    for ni in range(N_NULLS):
        nr = shuffled_runs(raw_min, ni)
        nf = fit_population(nr, folds, lm)
        null_rows.append({
            "null_index": ni,
            "pooled_cross_entropy": nf["pooled"]["cross_entropy"],
            "pooled_valid_group_fraction": nf["pooled"]["valid_group_fraction"],
            "exact_key_recurrence": nf["exact_key_recurrence"],
        })
        if (ni + 1) % 20 == 0:
            print(f"completed_nulls={ni+1}/{N_NULLS}", file=sys.stderr, flush=True)

    null_ce = [x["pooled_cross_entropy"] for x in null_rows]
    null_valid = [x["pooled_valid_group_fraction"] for x in null_rows]
    real_ce = primary["pooled"]["cross_entropy"]
    lower = sum(x <= real_ce for x in null_ce)
    p_lower = (1 + lower) / (N_NULLS + 1)
    med_ce = float(statistics.median(null_ce))
    adv = med_ce - real_ce
    null_summary = {
        "null_count": N_NULLS,
        "lower_tail_count": int(lower),
        "lower_tail_p": float(p_lower),
        "ce_median": med_ce,
        "ce_q05": qtile(null_ce, .05),
        "ce_min": float(min(null_ce)),
        "real_ce_advantage_below_null_median": float(adv),
        "valid_fraction_median": float(statistics.median(null_valid)),
        "valid_fraction_q05": qtile(null_valid, .05),
        "valid_fraction_q95": qtile(null_valid, .95),
        "recurrence_distribution": {str(k): int(v) for k, v in sorted(Counter(x["exact_key_recurrence"] for x in null_rows).items())},
    }

    dg = primary["diagnostics"]
    pooled = primary["pooled"]
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
    lead = all(gates.values())
    classification = "BACON BILITERAL PLAINTEXT LEAD" if lead else "NO READABLE BACON BILITERAL PLAINTEXT"
    flags = []
    if pooled["valid_group_fraction"] < .80:
        flags.append("LOW-VALIDITY")
    if dg["top5_char_fraction"] >= .90:
        flags.append("LOW-DIVERSITY OPTIMUM")

    raw_max, cov_max = build_raw_runs(items, universe, parser, "max")
    sensitivity = summarize_policy(raw_max, folds, lm, lexicon)

    out = {
        "experiment": "Issue26E15 Bacon biliteral two-difference musical-carrier probe",
        "classification": classification,
        "flags": flags,
        "historical_alphabet": "".join(ALPHABET),
        "code_rule": "five bits, a=0/b=1, values 0..23 row-major alphabet; 24..31 invalid",
        "key_space": [{"phase": p, "orientation": o} for p, o in KEYS],
        "positive_control": pos,
        "latin_population": latin_meta,
        "latin_self_baseline": baseline,
        "slot_parser_validation": parser_validation,
        "primary_population": cov_min,
        "primary_min": primary,
        "literal_phase0": literal,
        "order_null_summary": null_summary,
        "order_nulls": null_rows,
        "gates": gates,
        "max_population": cov_max,
        "max_sensitivity": sensitivity,
        "seed_namespace": "Issue26E15:BitShuffle:v1:<null>:<paragraph_id>:<run_index>",
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
