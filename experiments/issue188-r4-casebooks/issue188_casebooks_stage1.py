#!/usr/bin/env python3
"""Issue #188 Casebooks one-shot R4/S1 external reveal scorer."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
GATE0_PATH = ROOT / "experiments" / "issue188-r4-casebooks" / "issue188_casebooks_gate0.py"
P62_PATH = ROOT / "experiments" / "phase62" / "phase62b_n0.py"
P62_RESULT_PATH = ROOT / "experiments" / "phase62" / "phase62b_n0_results.json"
PLAN_PATH = ROOT / "research" / "ISSUE188_R4_CASEBOOKS_STAGE1_PLAN_20260908.md"

EXPECTED_GATE0_BLOB = "9792e32a0cb86bd293491701625e8fe2d530aacd"
EXPECTED_P62_BLOB = "e0ada366845c7a6c5a5dd75de91fe262b72a94b6"
EXPECTED_P62_RESULT_BLOB = "e798b3af89fd029660f9a90750985630c3d283ac"
EXPECTED_PLAN_BLOB = "763b2a8c8f5661745a1024d2109b8df8ae9a6a0b"
EXPECTED_CASEBOOKS_COMMIT = "9d42295d72b5ba8889575a32d79311cc72bce73a"
EXPECTED_ZL_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_VOLUME_HASH = "25cc1b61569c4c5933f5b9293e47477107b163ab80bfae323dc5c55fe211dfcc"
TARGET_FOLDS = [0.8061532394902311, 1.4591847522080983, 0.20470443416832568, 0.6808459396801555, 1.2290822859476285]
TARGET_MEAN = 0.8759941302988878
PRIMARY_MIN_SUPPORT = 10
STABLE_MIN = 31


def git_blob(path: Path) -> str:
    b = path.read_bytes()
    return hashlib.sha1(f"blob {len(b)}\0".encode() + b).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def first_attr(root, path: str, attr: str, ns: str):
    el = root.find(path)
    return el.attrib.get(attr) if el is not None else None


def parse_casebooks(repo: Path, G, B):
    items = []
    meta = []
    support_volume = Counter()
    support_practice = Counter()
    support_hand = Counter()
    files = sorted((repo / "cases").glob("CASE*.xml"), key=lambda p: p.name)
    opaque_refs = 0
    parsed = 0
    for path in files:
        text, n_refs = G.standalone_xml(path)
        opaque_refs += n_refs
        root = G.ET.fromstring(text)
        parsed += 1
        volume = "UNKNOWN"
        for alt in root.findall(f".//{{{G.TEI}}}sourceDesc//{{{G.TEI}}}altIdentifier"):
            if alt.attrib.get("type") == "fn_number":
                idno = alt.find(f"{{{G.TEI}}}idno")
                if idno is not None and idno.attrib.get("n"):
                    volume = idno.attrib["n"]
                    break
        hands = sorted({x.attrib.get("sameAs") for x in root.findall(f".//{{{G.TEI}}}profileDesc/{{{G.TEI}}}handNotes/{{{G.TEI}}}handNote") if x.attrib.get("sameAs")})
        hand_set = "+".join(hands) if hands else "UNKNOWN"
        practice_el = root.find(f".//{{{G.TEI}}}profileDesc//{{{G.CB}}}practice")
        practice = practice_el.attrib.get("name", "UNKNOWN") if practice_el is not None else "UNKNOWN"
        ps = root.findall(f".//{{{G.TEI}}}text/{{{G.TEI}}}body//{{{G.TEI}}}p")
        for pi, p in enumerate(ps):
            lines, _leading = G.paragraph_lines(p)
            if not G.eligible(lines):
                continue
            b_lines = [[B.latin_units(w) for w in line if w] for line in lines]
            item = B.Item(item_id=f"{path.stem}:p{pi}", document=path.stem, lines=b_lines, leaf=None)
            if not B.s1_eligible(item):
                raise RuntimeError(f"Gate0/Phase62 eligibility mismatch: {item.item_id}")
            items.append(item)
            meta.append((volume, practice, hand_set))
            support_volume[volume] += 1
            support_practice[practice] += 1
            support_hand[hand_set] += 1
    if parsed != 79881 or len(items) != 1082 or opaque_refs != 0:
        raise RuntimeError(f"Gate0 support identity mismatch: parsed={parsed}, eligible={len(items)}, entities={opaque_refs}")
    if support_practice.get("forman") != 114 or support_practice.get("napier") != 968:
        raise RuntimeError(f"practice support identity mismatch: {support_practice}")
    if support_hand.get("#sforman") != 108 or support_hand.get("#rnapier") != 866:
        raise RuntimeError("principal-hand support identity mismatch")
    return items, meta, support_volume, support_practice, support_hand


def score_group(B, items, contexts):
    vals = []
    for sd, direction in contexts:
        s1, n, _delta = B.s1_projection(items, sd, direction)
        if s1 is None or n == 0:
            raise RuntimeError("empty S1 group")
        vals.append(float(s1))
    return {
        "folds": vals,
        "mean": float(np.mean(vals)),
        "positive_folds": int(sum(v > 0 for v in vals)),
        "n_items": len(items),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zl3b", required=True, type=Path)
    ap.add_argument("--casebooks", required=True, type=Path)
    args = ap.parse_args()

    for path, expected, label in [
        (GATE0_PATH, EXPECTED_GATE0_BLOB, "Gate0 extractor"),
        (P62_PATH, EXPECTED_P62_BLOB, "Phase62B scorer"),
        (P62_RESULT_PATH, EXPECTED_P62_RESULT_BLOB, "Phase62B result"),
        (PLAN_PATH, EXPECTED_PLAN_BLOB, "Stage1 plan"),
    ]:
        got = git_blob(path)
        if got != expected:
            raise RuntimeError(f"{label} blob changed: {got} != {expected}")

    G = load_module(GATE0_PATH, "issue188_gate0_frozen")
    B = load_module(P62_PATH, "issue188_phase62b_frozen")
    if B.EXPECTED_ZL3B_BLOB != EXPECTED_ZL_BLOB:
        raise RuntimeError("Phase62B ZL authority changed")
    if G.git_head(args.casebooks.resolve()) != EXPECTED_CASEBOOKS_COMMIT:
        raise RuntimeError("Casebooks commit changed")
    if B.git_blob_sha1(args.zl3b.read_bytes()) != EXPECTED_ZL_BLOB:
        raise RuntimeError("ZL3b blob changed")

    hist = json.loads(P62_RESULT_PATH.read_text(encoding="utf-8"))
    hist_folds = [float(x["voynich"]["S1"]) for x in hist["folds"]]
    if any(abs(a-b) > 1e-12 for a,b in zip(hist_folds, TARGET_FOLDS)):
        raise RuntimeError("historical target fold constants changed")

    vitems = B.parse_voynich(args.zl3b.resolve())
    folds = B.physical_leaf_folds(vitems)
    contexts = []
    target_replay = []
    for fi, leaves in enumerate(folds):
        train = B.by_leaves(vitems, leaves, include=False)
        test = B.by_leaves(vitems, leaves, include=True)
        sd = B.training_sd(train)
        d = B.contrasts(train, sd)
        direction = np.mean(d, axis=0)
        norm = float(np.linalg.norm(direction))
        if norm == 0:
            raise RuntimeError(f"fold {fi}: zero target direction")
        direction /= norm
        ts1, n, _ = B.s1_projection(test, sd, direction)
        if ts1 is None or abs(float(ts1) - TARGET_FOLDS[fi]) > 1e-12:
            raise RuntimeError(f"fold {fi}: target replay mismatch {ts1}")
        target_replay.append(float(ts1))
        contexts.append((sd, direction))

    items, meta, support_volume, support_practice, support_hand = parse_casebooks(args.casebooks.resolve(), G, B)
    primary_volumes = sorted(v for v, n in support_volume.items() if n >= PRIMARY_MIN_SUPPORT)
    vol_hash = hashlib.sha256(("\n".join(primary_volumes) + "\n").encode()).hexdigest()
    if len(primary_volumes) != 51 or vol_hash != EXPECTED_VOLUME_HASH:
        raise RuntimeError(f"primary-volume authority mismatch: n={len(primary_volumes)} hash={vol_hash}")

    by_volume = defaultdict(list)
    by_practice = defaultdict(list)
    by_hand = defaultdict(list)
    for item, (volume, practice, hand) in zip(items, meta):
        by_volume[volume].append(item)
        by_practice[practice].append(item)
        by_hand[hand].append(item)

    volume_rows = []
    for volume in primary_volumes:
        s = score_group(B, by_volume[volume], contexts)
        s["volume"] = volume
        s["stable_positive"] = bool(s["mean"] > 0 and s["positive_folds"] >= 4)
        s["stable_negative"] = bool(s["mean"] < 0 and s["positive_folds"] <= 1)
        volume_rows.append(s)

    equal_fold_means = [float(np.mean([r["folds"][f] for r in volume_rows])) for f in range(5)]
    equal_mean = float(np.mean(equal_fold_means))
    equal_positive_folds = int(sum(x > 0 for x in equal_fold_means))
    stable_pos = int(sum(r["stable_positive"] for r in volume_rows))
    stable_neg = int(sum(r["stable_negative"] for r in volume_rows))

    practices = {k: score_group(B, by_practice[k], contexts) for k in ("forman", "napier")}
    hands = {k: score_group(B, by_hand[k], contexts) for k in ("#sforman", "#rnapier")}
    pooled = score_group(B, items, contexts)

    repl = bool(
        equal_mean > 0 and equal_positive_folds >= 4 and stable_pos >= STABLE_MIN
        and all(practices[k]["mean"] > 0 and practices[k]["positive_folds"] >= 4 for k in ("forman", "napier"))
    )
    wrong = bool(
        equal_mean < 0 and equal_positive_folds <= 1 and stable_neg >= STABLE_MIN
        and all(practices[k]["mean"] < 0 and practices[k]["positive_folds"] <= 1 for k in ("forman", "napier"))
    )
    classification = "VOYNICH_DIRECTION_REPLICATED" if repl else ("WRONG_SIGN" if wrong else "MIXED_OR_UNSTABLE")
    ratio = float(equal_mean / TARGET_MEAN)
    if classification == "VOYNICH_DIRECTION_REPLICATED":
        magnitude = "R4_MAGNITUDE_COMPATIBLE" if 0.5 <= ratio <= 2.0 else "DIRECTION_ONLY_OUTSIDE_MAGNITUDE_BAND"
    else:
        magnitude = "NOT_APPLICABLE_DIRECTION_NOT_REPLICATED"

    out = {
        "schema": "issue188-r4-casebooks-stage1-v1",
        "issue": 188,
        "classification": classification,
        "magnitude_classification": magnitude,
        "authorities": {
            "casebooks_commit": EXPECTED_CASEBOOKS_COMMIT,
            "gate0_blob": EXPECTED_GATE0_BLOB,
            "phase62b_blob": EXPECTED_P62_BLOB,
            "phase62b_result_blob": EXPECTED_P62_RESULT_BLOB,
            "stage1_plan_blob": EXPECTED_PLAN_BLOB,
            "zl3b_blob": EXPECTED_ZL_BLOB,
            "primary_volume_list_sha256": vol_hash,
        },
        "target_replay": {"folds": target_replay, "mean": float(np.mean(target_replay))},
        "primary_equal_volume": {
            "n_volumes": len(primary_volumes),
            "folds": equal_fold_means,
            "mean": equal_mean,
            "positive_folds": equal_positive_folds,
            "ratio_to_voynich": ratio,
            "stable_positive_volumes": stable_pos,
            "stable_negative_volumes": stable_neg,
            "stable_threshold": STABLE_MIN,
        },
        "practices": practices,
        "principal_hands": hands,
        "pooled_all_eligible": pooled,
        "primary_volumes": volume_rows,
        "support_identity": {
            "eligible_paragraphs": len(items),
            "primary_volumes": len(primary_volumes),
            "forman": support_practice["forman"],
            "napier": support_practice["napier"],
            "sforman": support_hand["#sforman"],
            "rnapier": support_hand["#rnapier"],
        },
        "firewall": {
            "post_reveal_source_or_representation_repair_allowed": False,
            "consultation_class_rescue_allowed": False,
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
