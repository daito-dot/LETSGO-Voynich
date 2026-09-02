#!/usr/bin/env python3
"""Issue #84 Phase A — cross-linguistic / cross-transcription baselines.

Authority: PLAN_A.md (frozen before this executable).

usage: python3 phase84a.py DATA_DIR BIBLE_DIR CREMMA_ROOT OUT_DIR [--only LABEL,...]
DATA_DIR holds the voynich.nu IVTFF files (ZL3b-n.txt IT2a-n.txt VT0e-n.txt
RF1b-e.txt GC2a-n.txt CD2a-n.txt FG2a-n.txt).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import unicodedata
import zlib
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("phase62", "phase63", "issue26-music", "occupancy-generation-hierarchy"):
    sys.path.insert(0, str(EXPERIMENTS / rel))
import phase62b_n0 as b  # noqa: E402
import phase63b_common as p63  # noqa: E402

N_TOKENS_BIBLE = 32570
BINS = ((1, 2), (3, 5), (6, 10), (11, 20), (21, 40), (41, 80), (81, 160), (161, 320))
Q2_REPS = 50
Q1_REPS = 20
Q1B_REPS = 5
MI_DISTANCES = (1, 2, 5, 20)
VOYNICH = {
    "ZL3b": ("ZL3b-n.txt", "eva"),
    "IT2a": ("IT2a-n.txt", "eva"),
    "VT0e": ("VT0e-n.txt", "eva"),
    "RF1b": ("RF1b-e.txt", "eva"),
    "GC2a": ("GC2a-n.txt", "v101"),
    "CD2a": ("CD2a-n.txt", "chars"),
    "FG2a": ("FG2a-n.txt", "chars"),
}
LOCUS = re.compile(r"^<(f[0-9]+[rv][0-9]*)\.(\d+),(@?[^>]*)>\s*(.*)$")
# frozen EVA composite collapse: each composite becomes one upper-case unit symbol
COMPOSITES = (("cth", "T"), ("ckh", "K"), ("cph", "P"), ("cfh", "F"), ("ch", "C"), ("sh", "S"))


def seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(f"issue84A:{label}".encode()).digest()[:8], "big") % (2**32)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ------------------------------------------------------------------ Voynich

def clean_body(body: str) -> str:
    body = body.replace("<%>", " ").replace("<$>", " ")
    body = re.sub(r"<![^>]*>", " ", body)
    body = re.sub(r"<[^>]*>", " ", body)
    body = re.sub(r"\{[^}]*\}", " ", body)
    body = re.sub(r"@\d+;", "", body)
    body = re.sub(r"\[([^\]:]*):[^\]]*\]", r"\1", body)  # first alternative of [a:b]
    return body


def eva_units(tok: str):
    t = re.sub(r"[^a-z]", "", tok.lower())
    for src, dst in COMPOSITES:
        t = t.replace(src, dst)
    return tuple(t)


def chars_units(tok: str):
    return tuple(re.sub(r"[^A-Za-z0-9]", "", tok))


def parse_voynich_generic(path: Path, kind: str):
    """documents = pages; returns list of (page, [token_unit_tuples])"""
    docs = defaultdict(list)
    for raw in path.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
        m = LOCUS.match(raw)
        if not m or "P" not in m.group(3):
            continue
        page = m.group(1)
        for tok in re.split(r"[.,\s]+", clean_body(m.group(4))):
            u = eva_units(tok) if kind == "eva" else chars_units(tok)
            if u:
                docs[page].append(u)
    return list(docs.items())


def parse_voynich_v101(path: Path):
    pars, _ = p63.parse_ivtff(path, "GC2a", "W1")
    docs = defaultdict(list)
    for par in pars:
        for line in par.lines:
            docs[par.page].extend(tuple(t) for t in line)
    return list(docs.items())


# ------------------------------------------------------------------ Bible

SEG = re.compile(r"<seg id=[\'\"]b\.([^.\'\"]+)\.(\d+)\.(\d+)[\'\"][^>]*>(.*?)</seg>", re.S)


def clean_word(w: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFC", w) if unicodedata.category(ch)[0] in "LM").lower()


def parse_bible(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    books = []
    chapters = defaultdict(list)
    order = []
    for book, ch, _v, seg in SEG.findall(text):
        if book not in books:
            books.append(book)
        key = (book, int(ch))
        if key not in chapters:
            order.append(key)
        for w in seg.split():
            cw = clean_word(w)
            if cw:
                chapters[key].append(tuple(cw))
    start = next((i for i, bk in enumerate(books) if bk.upper().startswith("MAT")), None)
    if start is None:
        return None, books
    nt_books = set(books[start:])
    docs, n = [], 0
    for key in order:
        if key[0] not in nt_books:
            continue
        take = chapters[key][: N_TOKENS_BIBLE - n]
        if take:
            docs.append((f"{key[0]}.{key[1]}", take))
            n += len(take)
        if n >= N_TOKENS_BIBLE:
            break
    return docs, books


# ------------------------------------------------------------------ statistics

def to_ids(docs):
    vocab = {}
    ids, doc_id = [], []
    for di, (_name, toks) in enumerate(docs):
        for t in toks:
            ids.append(vocab.setdefault(t, len(vocab)))
            doc_id.append(di)
    return np.asarray(ids, dtype=np.int64), np.asarray(doc_id, dtype=np.int64), len(vocab)


def shuffle_within_docs(ids, doc_id, rng):
    out = ids.copy()
    bounds = np.flatnonzero(np.diff(doc_id)) + 1
    for seg in np.split(np.arange(len(ids)), bounds):
        out[seg] = rng.permutation(out[seg])
    return out


def repeat_rates(ids, doc_id):
    n = len(ids)
    rates = []
    for lo, hi in BINS:
        acc = np.zeros(n, dtype=bool)
        valid = np.zeros(n, dtype=bool)
        for d in range(lo, hi + 1):
            if d >= n:
                break
            same_doc = doc_id[d:] == doc_id[:-d]
            acc[d:] |= (ids[d:] == ids[:-d]) & same_doc
            if d == lo:
                valid[d:] = same_doc
        rates.append(float(acc[valid].mean()) if valid.any() else float("nan"))
    return np.asarray(rates)


def q2(ids, doc_id, label):
    obs = repeat_rates(ids, doc_id)
    rng = np.random.default_rng(seed(f"Q2:{label}"))
    nulls = np.array([repeat_rates(shuffle_within_docs(ids, doc_id, rng), doc_id) for _ in range(Q2_REPS)])
    med = np.median(nulls, axis=0)
    sd = nulls.std(axis=0) + 1e-12
    return {"observed": obs.tolist(), "null_median": med.tolist(), "excess": (obs - med).tolist(), "z": ((obs - med) / sd).tolist()}


def mi_at(ids, doc_id, d):
    same = doc_id[d:] == doc_id[:-d]
    x, y = ids[:-d][same], ids[d:][same]
    n = len(x)
    V = int(ids.max()) + 1
    key = x * V + y
    uk, kc = np.unique(key, return_counts=True)
    px = np.bincount(x, minlength=V) / n
    py = np.bincount(y, minlength=V) / n
    kx, ky = uk // V, uk % V
    pxy = kc / n
    return float(np.sum(pxy * np.log2(pxy / (px[kx] * py[ky]))))


def q1(ids, doc_id, label):
    out = {}
    rng = np.random.default_rng(seed(f"Q1:{label}"))
    for d in MI_DISTANCES:
        obs = mi_at(ids, doc_id, d)
        nulls = [mi_at(shuffle_within_docs(ids, doc_id, rng), doc_id, d) for _ in range(Q1_REPS)]
        out[f"d{d}"] = {"observed": obs, "null_mean": float(np.mean(nulls)), "corrected": obs - float(np.mean(nulls))}
    raw = ids.astype(np.uint16).tobytes()
    c0 = len(zlib.compress(raw, 9))
    cs = [len(zlib.compress(shuffle_within_docs(ids, doc_id, rng).astype(np.uint16).tobytes(), 9)) for _ in range(Q1B_REPS)]
    out["q1b_zlib_bits_per_token"] = float((np.mean(cs) - c0) * 8 / len(ids))
    return out


class UnitChain2:
    def __init__(self, tokens):
        self.c = defaultdict(Counter)
        self.c1 = defaultdict(Counter)
        alpha = set()
        for tok in tokens:
            seq = ("^", "^") + tuple(tok) + ("$",)
            for i in range(2, len(seq)):
                self.c[seq[i - 2:i]][seq[i]] += 1
                self.c1[seq[i - 1]][seq[i]] += 1
                alpha.add(seq[i])
        self.V = len(alpha) + 1

    def bits(self, tok):
        seq = ("^", "^") + tuple(tok) + ("$",)
        lp = 0.0
        for i in range(2, len(seq)):
            c1 = self.c1[seq[i - 1]]
            n1 = sum(c1.values())
            p1 = (c1[seq[i]] + 0.5) / (n1 + 0.5 * self.V)
            c2 = self.c[seq[i - 2:i]]
            n2 = sum(c2.values())
            lp += math.log2((c2[seq[i]] + p1) / (n2 + 1.0))
        return -lp


def q3(docs):
    folds = [docs[i::5] for i in range(5)]
    bt, bu, oov = [], [], []
    for f in range(5):
        tr = [t for g in range(5) if g != f for _n, toks in folds[g] for t in toks]
        te = [t for _n, toks in folds[f] for t in toks]
        if not tr or not te:
            continue
        m = UnitChain2(tr)
        types = set(tr)
        bits = [m.bits(t) for t in te]
        bt.append(float(np.mean(bits)))
        bu.append(float(sum(bits) / sum(len(t) for t in te)))
        oov.append(float(np.mean([t not in types for t in te])))
    return {"bits_per_token": float(np.mean(bt)), "bits_per_unit": float(np.mean(bu)), "heldout_oov_type_rate": float(np.mean(oov))}


def score(label, docs):
    ids, doc_id, V = to_ids(docs)
    return {
        "label": label,
        "n_tokens": int(len(ids)),
        "n_types": V,
        "n_docs": len(docs),
        "mean_doc_tokens": float(len(ids) / len(docs)),
        "mean_token_units": float(np.mean([len(t) for _n, toks in docs for t in toks])),
        "Q1": q1(ids, doc_id, label),
        "Q2": q2(ids, doc_id, label),
        "Q3": q3(docs),
    }


def classify(results):
    voy = results["voynich"]
    mi_v = [v["Q1"]["d1"]["corrected"] for v in voy.values()]
    far_v = [max(v["Q2"]["z"][6], v["Q2"]["z"][7]) for v in voy.values()]
    langs = {k: v for k, v in results["languages"].items() if v.get("status") == "SCORED"}
    mi_l = {k: v["Q1"]["d1"]["corrected"] for k, v in langs.items()}
    far_l = {k: max(v["Q2"]["z"][6], v["Q2"]["z"][7]) for k, v in langs.items()}
    inside = sorted(k for k in langs if mi_l[k] <= max(mi_v) and far_l[k] <= 2.0)
    robust = all(m < min(mi_l.values()) for m in mi_v) and all(z <= 2.0 for z in far_v)
    allmi = sorted(mi_l.values())
    ranks = {}
    for k, v in voy.items():
        m = v["Q1"]["d1"]["corrected"]
        ranks[k] = {
            "MI_d1": m,
            "far_z_max": max(v["Q2"]["z"][6], v["Q2"]["z"][7]),
            "short_z_min": min(v["Q2"]["z"][:4]),
            "MI_percentile_among_languages": float(100 * sum(x <= m for x in allmi) / len(allmi)),
        }
    return {
        "n_languages_scored": len(langs),
        "voynich_MI_d1_range": [min(mi_v), max(mi_v)],
        "language_MI_d1_range": [min(mi_l.values()), max(mi_l.values())],
        "language_MI_d1_min_language": min(mi_l, key=mi_l.get),
        "languages_inside_voynich_regime": inside,
        "language_regime_classification": "NO NATURAL LANGUAGE IN VOYNICH REGIME" if not inside else "SOME NATURAL LANGUAGES IN VOYNICH REGIME",
        "transcription_classification": "VOYNICH REGIME TRANSCRIPTION-ROBUST" if robust else "VOYNICH REGIME TRANSCRIPTION-DEPENDENT",
        "voynich_readings": ranks,
        "languages_with_nonpositive_far_excess": sorted(k for k in langs if far_l[k] <= 2.0),
    }


# ------------------------------------------------------------------ main

def main(argv):
    data, bible, cremma, out_dir = (Path(x).resolve() for x in argv[1:5])
    only = set(argv[6].split(",")) if len(argv) > 6 and argv[5] == "--only" else None
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {"schema": "issue84-phaseA-v1", "plan": "experiments/cross-linguistic-baselines/PLAN_A.md", "sources": {}, "voynich": {}, "languages": {}, "anchors": {}}
    for label, (fname, kind) in VOYNICH.items():
        if only and label not in only:
            continue
        p = data / fname
        results["sources"][label] = {"file": fname, "sha256": sha256_file(p)}
        docs = parse_voynich_v101(p) if kind == "v101" else parse_voynich_generic(p, kind)
        r = score(label, docs)
        results["voynich"][label] = r
        print(label, json.dumps({k: r[k] for k in ("n_tokens", "n_types", "n_docs")}), "MI1=%.3f" % r["Q1"]["d1"]["corrected"], "z=", [round(z, 1) for z in r["Q2"]["z"]], "bits/tok=%.2f" % r["Q3"]["bits_per_token"], file=sys.stderr, flush=True)
    skip_untok = {"Chinese.xml", "Japanese.xml", "Thai.xml", "Vietnamese.xml"}
    for p in sorted((bible / "bibles").glob("*.xml")):
        lang = p.stem
        if only and lang not in only:
            continue
        if p.name in skip_untok:
            results["languages"][lang] = {"status": "EXCLUDED_UNTOKENIZED_DUPLICATE"}
            continue
        docs, books = parse_bible(p)
        if docs is None:
            results["languages"][lang] = {"status": "NO_NT_MARKER", "books": books[:5]}
            continue
        n = sum(len(t) for _n, t in docs)
        if n < N_TOKENS_BIBLE:
            results["languages"][lang] = {"status": "INSUFFICIENT_SIZE", "nt_tokens": n}
            print(lang, "INSUFFICIENT_SIZE", n, file=sys.stderr, flush=True)
            continue
        r = score(lang, docs)
        r["status"] = "SCORED"
        r["sha256"] = sha256_file(p)
        results["languages"][lang] = r
        print(lang, "MI1=%.3f" % r["Q1"]["d1"]["corrected"], "z=", [round(z, 1) for z in r["Q2"]["z"]], "bits/tok=%.2f" % r["Q3"]["bits_per_token"], file=sys.stderr, flush=True)
    if not only:
        litems = []
        for name, rel in b.PRIMARY_MANUSCRIPTS.items():
            litems.extend(b.parse_latin_manuscript(cremma, name, rel))
        ldocs = defaultdict(list)
        for it in litems:
            for line in it.lines:
                ldocs[it.document].extend(tuple(t) for t in line)
        results["anchors"]["CREMMA_Latin_graphematic"] = score("CREMMA", list(ldocs.items()))
        import ogh_a as A  # noqa: E402
        import ogh_c as C  # noqa: E402
        in_a, _ = A.load_admissible()
        vi, vf, parsed = C.load_corpus(data / "ZL3b-n.txt")
        gitems, _ = C.generate_manuscript("V2", 0, vi, vf, parsed, in_a)
        gdocs = defaultdict(list)
        for it in gitems:
            for line in it.lines:
                gdocs[it.document].extend(eva_units("".join(t)) for t in line)
        results["anchors"]["V2_memoryless_generator"] = score("V2", list(gdocs.items()))
        results["classification"] = classify(results)
    (out_dir / "phase84a_results.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    if "classification" in results:
        print(json.dumps(results["classification"], indent=1))


if __name__ == "__main__":
    main(sys.argv)
