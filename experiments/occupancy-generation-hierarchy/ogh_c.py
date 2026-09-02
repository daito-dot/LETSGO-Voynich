#!/usr/bin/env python3
"""OGH-C — value-level successor grammar, per-token information budget, cross-token R2/R3 test.

Scientific authority: PLAN_C.md (committed before this executable).

Modes
  --self-test
  --c0 ZL3b OUT.json                       stage C0: held-out bits/token for V0, V1, V2, V+; select V*
  --c1 ZL3b C0.json OUT_DIR                stage C1: generate V0, V*, V+ x 3 reps into the held-out
                                            paragraph skeleton; frozen Phase64B S1/S2/S3/H62 scoring
                                            and evaluation; decision
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("phase62", "phase64", "issue26-music"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
import phase62b_n0 as b  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402
import ogh_a as A  # noqa: E402
import ogh_b as B  # noqa: E402  (patches ogh_a with G7A)

PHASE = "OGH-C"
N_FOLDS = 5
REPS = (0, 1, 2)
UNITS = [(s, v) for s in range(12) for v in e.SLOTS[s]]  # 33 units
UNIT_INDEX = {u: i for i, u in enumerate(UNITS)}
N_UNITS = len(UNITS)
START = N_UNITS          # 33
STOP = N_UNITS + 1       # 34
NONE = N_UNITS + 2       # 35 (second-order "no previous" symbol)
UNIT_SLOT = np.asarray([s for s, _ in UNITS] + [-1, 99, -2])
LN2 = math.log(2.0)


def token_units(parser: e.SlotParser, tok: str):
    picked = parser.pick(tok, "min")
    if picked is None:
        return None
    sig, vals = picked
    return tuple(UNIT_INDEX[(s, vals[s])] for s in sig)


def units_to_string(seq) -> str:
    return "".join(UNITS[u][1] for u in seq)


def allowed_next(prev_unit: int) -> np.ndarray:
    """Units with a strictly later slot than prev (all units from START), plus STOP (not from START)."""
    if prev_unit == START:
        return np.arange(N_UNITS)
    s = UNIT_SLOT[prev_unit]
    later = np.flatnonzero(UNIT_SLOT[:N_UNITS] > s)
    return np.concatenate([later, [STOP]])


ALLOWED = {u: allowed_next(u) for u in list(range(N_UNITS)) + [START]}


# ----------------------------------------------------------------------------
# corpus

def load_corpus(zl_path: Path):
    if b.git_blob_sha1(zl_path.read_bytes()) != b.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b blob mismatch")
    vitems = b.parse_voynich(zl_path)
    folds = b.physical_leaf_folds(vitems)
    parser = e.SlotParser()
    e.validate_parser(parser)
    # per item: parsed unit sequences of its tokens (None if rejected)
    parsed = {}
    for it in vitems:
        parsed[it.item_id] = [[token_units(parser, "".join(tok)) for tok in line] for line in it.lines]
    return vitems, folds, parsed


def fold_sequences(vitems, folds, parsed, f, include):
    items = b.by_leaves(vitems, folds[f], include=include)
    seqs = [u for it in items for line in parsed[it.item_id] for u in line if u is not None]
    return items, seqs


# ----------------------------------------------------------------------------
# models

class V1Model:
    name = "V1"

    def __init__(self, seqs):
        c = defaultdict(Counter)
        for seq in seqs:
            prev = START
            for u in seq:
                c[prev][u] += 1
                prev = u
            c[prev][STOP] += 1
        self.table = {}
        for prev, allowed in ALLOWED.items():
            cnt = np.asarray([c[prev][x] for x in allowed], dtype=float)
            self.table[prev] = (allowed, (cnt + 0.5) / (cnt.sum() + 0.5 * len(allowed)))
        self.free_parameters = sum(len(a) - 1 for a in ALLOWED.values())
        self.observed_contexts = sum(1 for prev in ALLOWED if sum(c[prev].values()) > 0)

    def prob_next(self, prev, prev2=None):
        return self.table[prev]

    def logp(self, seq) -> float:
        lp, prev = 0.0, START
        for u in list(seq) + [STOP]:
            allowed, pr = self.table[prev]
            lp += math.log(pr[np.searchsorted(allowed, u)])
            prev = u
        return lp

    def sample(self, rng) -> tuple:
        out, prev = [], START
        while True:
            allowed, pr = self.table[prev]
            u = int(allowed[rng.choice(len(allowed), p=pr)])
            if u == STOP:
                return tuple(out)
            out.append(u)
            prev = u


class V2Model(V1Model):
    name = "V2"

    def __init__(self, seqs):
        super().__init__(seqs)
        self.v1_table = self.table
        c = defaultdict(Counter)
        for seq in seqs:
            prev2, prev = NONE, START
            for u in list(seq) + [STOP]:
                c[(prev2, prev)][u] += 1
                prev2, prev = prev, u
        self.ctx = {}
        for (p2, p1), cnt in c.items():
            allowed, base = self.v1_table[p1]
            n = np.asarray([cnt[x] for x in allowed], dtype=float)
            self.ctx[(p2, p1)] = (allowed, (n + B.BACKOFF * base) / (n.sum() + B.BACKOFF))
        self.observed_contexts = len(self.ctx)
        self.free_parameters = sum(len(ALLOWED[p1]) - 1 for (_, p1) in self.ctx)  # observed second-order contexts only

    def _dist(self, prev2, prev):
        return self.ctx.get((prev2, prev), self.v1_table[prev])

    def logp(self, seq) -> float:
        lp, prev2, prev = 0.0, NONE, START
        for u in list(seq) + [STOP]:
            allowed, pr = self._dist(prev2, prev)
            lp += math.log(pr[np.searchsorted(allowed, u)])
            prev2, prev = prev, u
        return lp

    def sample(self, rng) -> tuple:
        out, prev2, prev = [], NONE, START
        while True:
            allowed, pr = self._dist(prev2, prev)
            u = int(allowed[rng.choice(len(allowed), p=pr)])
            if u == STOP:
                return tuple(out)
            out.append(u)
            prev2, prev = prev, u


class V0Model:
    """G7A shape grammar x independent slot values (add-1/2)."""
    name = "V0"

    def __init__(self, seqs, in_a):
        masks = np.asarray([sum(1 << UNITS[u][0] for u in seq) for seq in seqs], dtype=np.int64)
        fit = B.fit_g7a(masks, in_a)
        self.p_shape = fit["p"]
        self.value_p = {}
        for s in range(12):
            cnt = Counter(UNITS[u][1] for seq in seqs for u in seq if UNITS[u][0] == s)
            vals = list(e.SLOTS[s])
            n = np.asarray([cnt[v] for v in vals], dtype=float)
            self.value_p[s] = (vals, (n + 0.5) / (n.sum() + 0.5 * len(vals)))
        self.free_parameters = 298 + sum(len(e.SLOTS[s]) - 1 for s in range(12))

    def shape_logp(self, seq) -> float:
        mask = sum(1 << UNITS[u][0] for u in seq)
        return math.log(self.p_shape[mask - 1])

    def logp(self, seq) -> float:
        lp = self.shape_logp(seq)
        for u in seq:
            s, v = UNITS[u]
            vals, pr = self.value_p[s]
            lp += math.log(pr[vals.index(v)])
        return lp

    def sample(self, rng) -> tuple:
        mask = int(rng.choice(A.N_SIG, p=self.p_shape)) + 1
        out = []
        for s in range(12):
            if (mask >> s) & 1:
                vals, pr = self.value_p[s]
                out.append(UNIT_INDEX[(s, vals[rng.choice(len(vals), p=pr)])])
        return tuple(out)


class VPlusModel:
    name = "V+"

    def __init__(self, seqs):
        self.counter = Counter(seqs)
        self.types = list(self.counter)
        n = np.asarray([self.counter[t] for t in self.types], dtype=float)
        self.p = n / n.sum()
        self.total = int(n.sum())
        self.free_parameters = len(self.types) - 1

    def logp(self, seq):
        c = self.counter.get(tuple(seq), 0)
        return math.log(c / self.total) if c else None

    def sample(self, rng) -> tuple:
        return self.types[rng.choice(len(self.types), p=self.p)]


def build(model: str, seqs, in_a):
    if model == "V0":
        return V0Model(seqs, in_a)
    if model == "V1":
        return V1Model(seqs)
    if model == "V2":
        return V2Model(seqs)
    if model == "V+":
        return VPlusModel(seqs)
    raise RuntimeError(model)


def heldout_bits(model, seqs) -> dict:
    lps = [model.logp(s) for s in seqs]
    covered = [x for x in lps if x is not None]
    return {
        "n_tokens": len(seqs),
        "oov_fraction": 1.0 - len(covered) / len(seqs),
        "bits_per_token_covered": float(-np.mean(covered) / LN2) if covered else None,
        "bits_per_token": float(-np.mean(covered) / LN2) if len(covered) == len(seqs) else None,
    }


# ----------------------------------------------------------------------------
# stage C0

def stage_c0(zl_path: Path) -> dict:
    in_a, adm = A.load_admissible()
    vitems, folds, parsed = load_corpus(zl_path)
    out = {"schema": "ogh-c-c0-v1", "phase": PHASE, "target_reveal": False, "cross_token_statistic_computed": False, "environment": A.environment(), "admissible_authority": adm, "units": [[s, v] for s, v in UNITS], "folds": {}}
    per_model = defaultdict(list)
    shape_bits = []
    for f in range(N_FOLDS):
        _, tr = fold_sequences(vitems, folds, parsed, f, False)
        _, he = fold_sequences(vitems, folds, parsed, f, True)
        row = {"n_train_tokens": len(tr), "n_heldout_tokens": len(he), "n_train_types": len(set(tr)), "models": {}}
        for m in ("V0", "V1", "V2", "V+"):
            mod = build(m, tr, in_a)
            hb = heldout_bits(mod, he)
            hb["free_parameters"] = int(mod.free_parameters)
            if hasattr(mod, "observed_contexts"):
                hb["observed_contexts"] = int(mod.observed_contexts)
            row["models"][m] = hb
            per_model[m].append(hb["bits_per_token_covered"])
            if m == "V0":
                sb = float(-np.mean([mod.shape_logp(s) for s in he]) / LN2)
                row["shape_only_bits_per_token_G7A"] = sb
                shape_bits.append(sb)
        out["folds"][str(f)] = row
    summary = {m: {"mean_bits_per_token_covered": float(np.mean(v)), "by_fold": v} for m, v in per_model.items()}
    summary["shape_only_G7A"] = {"mean_bits_per_token": float(np.mean(shape_bits)), "by_fold": shape_bits}
    summary["V+_mean_oov_fraction"] = float(np.mean([out["folds"][str(f)]["models"]["V+"]["oov_fraction"] for f in range(N_FOLDS)]))
    gains = [per_model["V1"][f] - per_model["V2"][f] for f in range(N_FOLDS)]  # bits saved by V2
    positive = int(sum(g > 0 for g in gains))
    selected = "V2" if positive >= 4 else "V1"
    out["summary"] = summary
    out["selection"] = {"V2_bits_saved_over_V1_by_fold": gains, "positive_folds": positive, "selected_content_grammar": selected, "rule": "V2 if bits saved in >= 4/5 folds else V1"}
    return out


# ----------------------------------------------------------------------------
# stage C1

def generate_manuscript(model_name: str, rep: int, vitems, folds, parsed, in_a):
    items = []
    n_tokens = 0
    for f in range(N_FOLDS):
        _, tr = fold_sequences(vitems, folds, parsed, f, False)
        mod = build(model_name, tr, in_a)
        rng = np.random.default_rng(e.stable_seed(f"{PHASE}:{model_name}:fold{f}:rep{rep}"))
        for it in b.by_leaves(vitems, folds[f], include=True):
            lines = []
            for line in it.lines:
                new = []
                for _tok in line:
                    seq = mod.sample(rng)
                    new.append(tuple(units_to_string(seq)))
                    n_tokens += 1
                lines.append(new)
            items.append(b.Item(item_id=it.item_id, document=it.document, lines=lines, leaf=it.leaf))
    items.sort(key=lambda x: (x.leaf if x.leaf is not None else 10**9, x.document, x.item_id))
    return items, n_tokens


def stage_c1(zl_path: Path, c0_path: Path, out_dir: Path) -> dict:
    c0 = json.loads(c0_path.read_text(encoding="utf-8"))
    if c0.get("schema") != "ogh-c-c0-v1":
        raise RuntimeError("stage C0 authority missing")
    vstar = c0["selection"]["selected_content_grammar"]
    in_a, adm = A.load_admissible()
    vitems, folds, parsed = load_corpus(zl_path)
    p62c = json.loads((EXPERIMENTS / "phase62" / "phase62c_c0_a1_results.json").read_text(encoding="utf-8"))
    p63a = json.loads((EXPERIMENTS / "phase63" / "phase63a_training_vocab_results.json").read_text(encoding="utf-8"))
    contexts, _ = n64.fold_contexts(zl_path, p62c, p63a)
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for m in ("V0", vstar, "V+"):
        reps = {}
        for rep in REPS:
            items, n_tok = generate_manuscript(m, rep, vitems, folds, parsed, in_a)
            label = f"{PHASE}:{m}:rep{rep}"
            metrics = n64.output_metrics(items, label, contexts)
            reps[f"rep{rep}"] = metrics
            (out_dir / f"{m.replace('+', 'plus')}_rep{rep}.json").write_text(json.dumps({"schema": "ogh-c-c1-rep-v1", "model": m, "rep": rep, "n_tokens": n_tok, "n_items": len(items), "metrics": metrics}, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
            print(f"{label}: S2={metrics['S2']:.4f} S3={metrics['S3']:.4f} S1f0={metrics['S1_by_fold']['0']['value']:.4f} C_short={metrics['H62P1']['C_short']}", file=sys.stderr, flush=True)
        agg = n64.aggregate_realizations(reps, f"{PHASE}:{m}")
        ev = n64.evaluate_aggregate(agg, contexts, p63a, f"{PHASE}:{m}")
        ev["classification"] = ev["classification"].replace("C1-E0", f"OGH-C {m}")
        results[m] = {"aggregate": agg, "evaluation": ev}
    ev = results[vstar]["evaluation"]
    # decision per PLAN_C section 5 (frozen Phase64B gate fields)
    exp_pass = bool(ev["exposed_gate_pass"])
    h62_viable = bool(ev["H62_viable_vs_N0_C0"])
    if exp_pass and h62_viable:
        decision = "MEMORYLESS TOKEN GRAMMAR REPRODUCES CROSS-TOKEN STRUCTURE"
    elif exp_pass or h62_viable:
        decision = "MEMORYLESS TOKEN GRAMMAR PARTIAL"
    else:
        decision = "MEMORYLESS TOKEN GRAMMAR FAILS CROSS-TOKEN STRUCTURE"
    out = {"schema": "ogh-c-c1-aggregate-v1", "phase": PHASE, "environment": A.environment(), "admissible_authority": adm, "c0_sha256": A.sha256_file(c0_path), "selected_content_grammar": vstar, "models": results, "decision": decision}
    (out_dir / "ogh_c_c1_aggregate.json").write_text(json.dumps(out, sort_keys=True, indent=1, default=float) + "\n", encoding="utf-8")
    return out


def self_test():
    rng = np.random.default_rng(0)
    seqs = [tuple(sorted(rng.choice(N_UNITS, size=rng.integers(1, 5), replace=False), key=lambda u: UNIT_SLOT[u])) for _ in range(300)]
    seqs = [tuple(dict.fromkeys(s)) for s in seqs]
    seqs = [s for s in seqs if len({UNIT_SLOT[u] for u in s}) == len(s)]
    in_a = np.ones(A.N_SIG, dtype=bool)
    for m in ("V0", "V1", "V2", "V+"):
        mod = build(m, seqs, in_a)
        for s in seqs[:20]:
            lp = mod.logp(s)
            assert lp is None or lp <= 1e-12
        smp = mod.sample(rng)
        assert len(smp) >= 1 and all(UNIT_SLOT[a] < UNIT_SLOT[c] for a, c in zip(smp, smp[1:]))
    # exact normalization of V1 from START over all sequences is implied by per-step normalization
    for prev, (allowed, pr) in V1Model(seqs).table.items():
        assert abs(pr.sum() - 1) < 1e-12
    assert units_to_string((UNIT_INDEX[(1, "o")], UNIT_INDEX[(3, "k")], UNIT_INDEX[(8, "a")], UNIT_INDEX[(10, "l")])) == "okal"
    print(json.dumps({"OGH-C_self_test": "ok", "n_units": N_UNITS, "cross_token_statistic_computed": False}))


def main(argv):
    if len(argv) >= 2 and argv[1] == "--self-test":
        self_test()
    elif len(argv) == 4 and argv[1] == "--c0":
        r = stage_c0(Path(argv[2]).resolve())
        Path(argv[3]).write_text(json.dumps(r, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({"summary": r["summary"], "selection": r["selection"]}, indent=1))
    elif len(argv) == 5 and argv[1] == "--c1":
        r = stage_c1(Path(argv[2]).resolve(), Path(argv[3]).resolve(), Path(argv[4]).resolve())
        print(json.dumps({"decision": r["decision"], "selected": r["selected_content_grammar"], "evaluations": {m: {k: v for k, v in r["models"][m]["evaluation"].items() if k in ("classification", "candidate_ratio_of_means_to_voynich", "exposed_gate_pass", "H62P1_summary", "H62_viable_vs_N0_C0", "A1_R1_rival")} for m in r["models"]}}, indent=1, default=str))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
