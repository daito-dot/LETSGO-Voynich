from __future__ import annotations

import hashlib
import itertools
import math
import random
import re
from collections import defaultdict

import numpy as np
from scipy.optimize import linear_sum_assignment

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EPS = 1e-12
LP = re.compile(r"^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<c>[^>]*)>\s+(?P<b>.*)$")
LEAF_RE = re.compile(r"f(\d+)")

SLOTS = (
    ("q", "s", "d"), ("o", "y"), ("l", "r"), ("t", "k", "p", "f"),
    ("ch", "sh"), ("cth", "ckh", "cph", "cfh"), ("e", "ee", "eee"),
    ("s", "d"), ("o", "a"), ("i", "ii", "iii"),
    ("d", "l", "r", "m", "n"), ("y",),
)
VOX = ("ut", "re", "mi", "fa", "sol", "la")
SLOT10_STATES = ("", "d", "l", "r", "m", "n")
GUIDO_ROWS = (
    ("ut",), ("re",), ("mi",), ("fa", "ut"), ("sol", "re"),
    ("la", "mi"), ("fa", "ut"), ("sol", "re", "ut"),
    ("la", "mi", "re"), ("fa", "mi"), ("sol", "fa", "ut"),
    ("la", "sol", "re"), ("la", "mi"), ("fa", "ut"),
    ("sol", "re", "ut"), ("la", "mi", "re"), ("fa", "mi"),
    ("sol", "fa"), ("la", "sol"), ("la",),
)


def git_blob_sha1(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def stable_seed(label):
    return int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "big")


def token_strings(body):
    start = "<%>" in body
    body = re.sub(r"<[^>]*>", " ", body.replace("<%>", " "))
    toks = [re.sub(r"[^A-Za-z]", "", x).lower() for x in re.split(r"[.\s]+", body)]
    return start, [x for x in toks if x]


def parse_voynich(path):
    pid = defaultdict(int); current = {}; out = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = LP.match(raw)
        if not m or "P" not in m.group("c"): continue
        page = m.group("loc").split(".")[0]
        start, toks = token_strings(m.group("b"))
        if start:
            if page in current: out.append(current.pop(page))
            pid[page] += 1
            lm = LEAF_RE.match(page); leaf = int(lm.group(1)) if lm else None
            current[page] = {"id": f"{page}:p{pid[page]}", "page": page, "leaf": leaf, "lines": []}
        if toks and page in current: current[page]["lines"].append(toks)
    out.extend(current.values())
    out.sort(key=lambda x: (x["leaf"] if x["leaf"] is not None else 10**9, x["page"], x["id"]))
    return out


def eligible(item):
    x = item["lines"]
    return len(x) >= 3 and len(x[0]) >= 5 and len(x[2]) >= 5


def physical_leaf_folds(items):
    leaves = sorted({x["leaf"] for x in items if x["leaf"] is not None and eligible(x)})
    return [set(leaves[i::5]) for i in range(5)]


class SlotParser:
    def __init__(self): self.cache = {}

    def parses(self, token):
        token = token.lower()
        if token in self.cache: return self.cache[token]
        out, vals = [], [""] * 12
        def rec(pos, next_slot, sig):
            if pos == len(token): out.append((tuple(sig), tuple(vals))); return
            for slot in range(next_slot, 12):
                for value in sorted(SLOTS[slot], key=lambda x: (-len(x), x)):
                    if token.startswith(value, pos):
                        vals[slot] = value; sig.append(slot)
                        rec(pos + len(value), slot + 1, sig)
                        sig.pop(); vals[slot] = ""
        rec(0, 0, [])
        out.sort(key=lambda x: x[0]); self.cache[token] = out
        return out

    def pick(self, token, policy):
        ps = self.parses(token)
        if not ps: return None
        return ps[0] if policy == "min" else ps[-1]


def validate_parser(parser):
    expected = {
        "otedy": ("1-3-6-7-11", "1-3-6-10-11"),
        "okal": ("1-3-8-10", "1-3-8-10"),
        "okol": ("1-3-8-10", "1-3-8-10"),
        "otchdy": ("1-3-4-7-11", "1-3-4-10-11"),
        "qokedy": ("0-1-3-6-7-11", "0-1-3-6-10-11"),
        "chedy": ("4-6-7-11", "4-6-10-11"),
        "y": ("1", "11"), "d": ("0", "10"),
        "dain": ("0-8-9-10", "7-8-9-10"),
        "daiin": ("0-8-9-10", "7-8-9-10"),
    }
    got = {}
    for tok, exp in expected.items():
        a, b = parser.pick(tok, "min"), parser.pick(tok, "max")
        if a is None or b is None: raise RuntimeError(f"validation token unparseable: {tok}")
        pair = ("-".join(map(str, a[0])), "-".join(map(str, b[0])))
        got[tok] = {"min": pair[0], "max": pair[1]}
        if pair != exp: raise RuntimeError(f"validation mismatch {tok}: {pair} != {exp}")
    return got


def feature_index():
    labels = []
    for s in list(range(10)) + [11]:
        labels.append((s, "")); labels.extend((s, v) for v in SLOTS[s])
    return labels, {v: i for i, v in enumerate(labels)}

FEATURE_LABELS, FEATURE_INDEX = feature_index()


def feature(vals):
    x = np.zeros(len(FEATURE_LABELS), dtype=float)
    for s in list(range(10)) + [11]: x[FEATURE_INDEX[(s, vals[s])]] = 1.0
    return x


class KMeans20:
    def fit(self, vectors):
        names = sorted(vectors)
        if len(names) < 20: raise RuntimeError(f"only {len(names)} parsed training types")
        X = np.stack([vectors[n] for n in names]); chosen = [0]
        while len(chosen) < 20:
            C = X[chosen]; d = ((X[:, None] - C[None]) ** 2).sum(2).min(1)
            d[chosen] = -1; md = float(d.max())
            tied = [i for i, z in enumerate(d) if abs(float(z) - md) <= EPS]
            chosen.append(min(tied, key=lambda i: names[i]))
        C = X[chosen].copy(); prev = None
        for _ in range(100):
            D = ((X[:, None] - C[None]) ** 2).sum(2); a = D.argmin(1)
            if prev is not None and np.array_equal(a, prev): break
            prev = a.copy(); new = C.copy(); occupied = set()
            for j in range(20):
                idx = np.flatnonzero(a == j)
                if len(idx): new[j] = X[idx].mean(0); occupied.add(j)
            empty = [j for j in range(20) if j not in occupied]
            if empty:
                da = D[np.arange(len(X)), a]
                candidates = sorted(range(len(names)), key=lambda i: (-float(da[i]), names[i])); used = set()
                for j in empty:
                    i = next(i for i in candidates if i not in used); used.add(i); new[j] = X[i]
            C = new
        self.centroids = C; return self

    def predict(self, x):
        return int(((self.centroids - x[None]) ** 2).sum(1).argmin())


def guidonian_matrix():
    G = np.zeros((20, 6), dtype=np.int8); vi = {v:i for i,v in enumerate(VOX)}
    for r, vs in enumerate(GUIDO_ROWS):
        for v in vs: G[r, vi[v]] = 1
    rows = [1,1,1,2,2,2,2,3,3,2,3,3,2,2,3,3,2,2,2,1]
    if G.sum(1).tolist() != rows or G.sum(0).tolist() != [7]*6 or int(G.sum()) != 42:
        raise RuntimeError("Guidonian lattice invariant failure")
    return G

GUIDO = guidonian_matrix()


def count_matrix(items, leaves, parser, policy, km):
    C = np.zeros((20,6), dtype=np.int64); si = {s:i for i,s in enumerate(SLOT10_STATES)}
    visible = parsed = 0
    for it in items:
        if it["leaf"] not in leaves: continue
        for line in it["lines"]:
            for tok in line:
                visible += 1; p = parser.pick(tok, policy)
                if p is None: continue
                vals = p[1]; C[km.predict(feature(vals)), si[vals[10]]] += 1; parsed += 1
    return C, visible, parsed


def assignment_score(W):
    rr, cc = linear_sum_assignment(-W); m = np.empty(W.shape[0], dtype=int)
    for a,b in zip(rr,cc): m[a] = b
    return int(W[np.arange(W.shape[0]), m].sum()), m


def lex_assignment(W, optimum):
    n = W.shape[0]; out = np.full(n,-1,dtype=int); avail = set(range(n)); fixed = 0
    for c in range(n):
        for r in sorted(avail):
            remc = list(range(c+1,n)); remr = sorted(avail-{r}); rem = 0
            if remc: rem,_ = assignment_score(W[np.ix_(remc,remr)])
            if fixed + int(W[c,r]) + rem == optimum:
                out[c] = r; avail.remove(r); fixed += int(W[c,r]); break
        if out[c] < 0: raise RuntimeError("lex assignment failure")
    if fixed != optimum: raise RuntimeError("lex assignment score mismatch")
    return out


def fit_mapping(C, lattice):
    best = None
    for perm in itertools.permutations(range(6)):
        W = np.zeros((20,20), dtype=np.int64)
        for s,v in enumerate(perm): W += C[:,s,None] * lattice[None,:,v]
        score,_ = assignment_score(W)
        if best is None or score > best[0] or (score == best[0] and perm < best[1]): best = (score,perm,W)
    score,perm,W = best; rows = lex_assignment(W,score)
    return {"training_allowed":int(score), "state_to_vox":list(perm), "cluster_to_row":rows.tolist()}


def score_counts(H, visible, parsed, mapping, lattice):
    allowed = 0
    for c in range(20):
        r = mapping["cluster_to_row"][c]
        for s in range(6): allowed += int(H[c,s]) * int(lattice[r, mapping["state_to_vox"][s]])
    return {"visible_occurrences":visible, "parsed_occurrences":parsed,
            "parse_coverage":parsed/visible if visible else 0.0,
            "allowed_occurrences":allowed, "accuracy":allowed/parsed if parsed else 0.0}


def swapped_lattice(label, seen, attempts=5000):
    rng = random.Random(stable_seed(label)); M = GUIDO.copy()
    for _round in range(100):
        edges = set(map(tuple, np.argwhere(M == 1)))
        for _ in range(attempts):
            ee = tuple(edges); e1 = ee[rng.randrange(len(ee))]; e2 = ee[rng.randrange(len(ee))]
            if e1 == e2: continue
            r1,c1=e1; r2,c2=e2
            if r1==r2 or c1==c2 or (r1,c2) in edges or (r2,c1) in edges: continue
            edges.remove(e1); edges.remove(e2); edges.add((r1,c2)); edges.add((r2,c1))
        M = np.zeros_like(GUIDO)
        for r,c in edges: M[r,c]=1
        key=M.tobytes()
        if not np.array_equal(M,GUIDO) and key not in seen:
            if not np.array_equal(M.sum(1),GUIDO.sum(1)) or not np.array_equal(M.sum(0),GUIDO.sum(0)):
                raise RuntimeError("degree-preserving null failure")
            seen.add(key); return M
    raise RuntimeError(f"could not make unique null {label}")


def quantile(xs,q):
    ys=sorted(xs); p=(len(ys)-1)*q; lo=math.floor(p); hi=math.ceil(p)
    return ys[lo] if lo==hi else ys[lo]*(hi-p)+ys[hi]*(p-lo)
