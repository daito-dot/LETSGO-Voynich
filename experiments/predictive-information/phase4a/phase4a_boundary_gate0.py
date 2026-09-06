#!/usr/bin/env python3
"""Issue #112 / Issue #88 Phase 4A score-free boundary support audit.

This executable freezes the raw Basic-EVA atomization and candidate populations
before any P1/P2 boundary likelihood is implemented.

Modes:
  --self-test
  --audit ZL3B OUT.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3] if len(HERE.parents) >= 4 else HERE.parent
PHASE62 = ROOT / "experiments" / "phase62"
if PHASE62.is_dir() and str(PHASE62) not in sys.path:
    sys.path.insert(0, str(PHASE62))

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_ZL3B_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
N_FOLDS = 5

# EVA-2: these common connected sequences conventionally omit explicit
# connectivity brackets/capitalisation. Longest match is mandatory.
CONNECTED_COMPOSITES: Tuple[str, ...] = ("cfh", "ckh", "cph", "cth", "ch", "sh")
# Basic EVA letters from the EVA-2 reference. 'w' is not a Basic-EVA character.
BASIC_EVA = frozenset("abcdefghijklmnopqrstuvxyz")

PAGE_HEADER_RE = re.compile(r"^<(?P<page>(?:f|m)\d+[rv]\d?)>\s+<!\s*(?P<meta>.*?)>")
LOCUS_RE = re.compile(r"^<(?P<loc>(?:f|m)\d+[rv]\d?\.\d+),(?P<code>[^>]*)>\s+(?P<body>.*)$")
LEAF_RE = re.compile(r"^[fm](\d+)")
CURRIER_RE = re.compile(r"(?:^|\s)\$L=([AB])(?:\s|$)")
HIGH_ASCII_RE = re.compile(r"@\d+;")


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj)).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def strip_structural_markers(body: str) -> str:
    """Remove only documented paragraph/locus edge markers.

    Any occurrence elsewhere remains literal exceptional material and therefore
    makes the affected token unclean.
    """
    s = body.strip()
    if s.startswith("<%>"):
        s = s[3:]
    if s.endswith("<$>"):
        s = s[:-3]
    return s


def split_certain_spaces(body: str) -> Tuple[List[str], int]:
    """Split on literal IVTFF '.' outside markup constructs only.

    Commas, drawing interruptions and exceptional notation are intentionally
    *not* separators here; they make the containing certain-space token unclean.
    """
    s = strip_structural_markers(body)
    segments: List[str] = []
    cur: List[str] = []
    n_dot = 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "<":
            j = s.find(">", i + 1)
            if j < 0:
                cur.append(s[i:])
                i = len(s)
                break
            cur.append(s[i:j + 1])
            i = j + 1
            continue
        if ch == "[":
            j = s.find("]", i + 1)
            if j < 0:
                cur.append(s[i:])
                i = len(s)
                break
            cur.append(s[i:j + 1])
            i = j + 1
            continue
        if ch == "{":
            j = s.find("}", i + 1)
            if j < 0:
                cur.append(s[i:])
                i = len(s)
                break
            cur.append(s[i:j + 1])
            i = j + 1
            continue
        if ch == ".":
            segments.append("".join(cur))
            cur = []
            n_dot += 1
            i += 1
            continue
        cur.append(ch)
        i += 1
    segments.append("".join(cur))
    if len(segments) != n_dot + 1:
        raise RuntimeError("certain-space splitter invariant failed")
    return segments, n_dot


def unclean_reasons(raw: str) -> Tuple[str, ...]:
    reasons = []
    if raw == "":
        reasons.append("empty")
    if "," in raw:
        reasons.append("uncertain_space_comma")
    if "?" in raw:
        reasons.append("illegible_question")
    if "[" in raw or "]" in raw:
        reasons.append("alternative_brackets")
    if "{" in raw or "}" in raw:
        reasons.append("explicit_ligature_braces")
    if HIGH_ASCII_RE.search(raw):
        reasons.append("high_ascii")
    if "<" in raw or ">" in raw:
        reasons.append("inline_or_intrusion_markup")
    if any("A" <= ch <= "Z" for ch in raw):
        reasons.append("uppercase_connectivity")
    if "'" in raw:
        reasons.append("apostrophe_or_tick")
    bad_letters = sorted({ch for ch in raw if "a" <= ch <= "z" and ch not in BASIC_EVA})
    if bad_letters:
        reasons.append("non_basic_eva_letter")
    if raw and any(not ("a" <= ch <= "z" and ch in BASIC_EVA) for ch in raw):
        known = (
            "," in raw or "?" in raw or "[" in raw or "]" in raw or
            "{" in raw or "}" in raw or "<" in raw or ">" in raw or
            HIGH_ASCII_RE.search(raw) is not None or "'" in raw or
            any("A" <= ch <= "Z" for ch in raw)
        )
        if not known:
            reasons.append("other_exceptional_symbol")
    return tuple(sorted(set(reasons)))


def atomize_clean(raw: str) -> Optional[Tuple[str, ...]]:
    if unclean_reasons(raw):
        return None
    out: List[str] = []
    i = 0
    while i < len(raw):
        match = None
        for comp in CONNECTED_COMPOSITES:
            if raw.startswith(comp, i):
                match = comp
                break
        if match is not None:
            out.append(match)
            i += len(match)
        else:
            ch = raw[i]
            if ch not in BASIC_EVA:
                return None
            out.append(ch)
            i += 1
    return tuple(out)


def page_currier_authority(lines: Sequence[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for line in lines:
        m = PAGE_HEADER_RE.match(line)
        if not m:
            continue
        page = m.group("page")
        cm = CURRIER_RE.search(m.group("meta"))
        if cm:
            out[page] = cm.group(1)
    # Frozen Phase-3A Amendment A.
    if "f57v" not in out:
        out["f57v"] = "B"
    return out


def frozen_fold_authority(zl_path: Path):
    try:
        import phase62b_n0 as b
    except Exception as exc:  # pragma: no cover - audit environment only
        raise RuntimeError(f"cannot import frozen fold authority phase62b_n0: {exc}")
    items = b.parse_voynich(zl_path)
    folds = b.physical_leaf_folds(items)
    if len(folds) != N_FOLDS:
        raise RuntimeError("frozen fold count mismatch")
    leaf_fold: Dict[int, int] = {}
    for f, leaves in enumerate(folds):
        for leaf in leaves:
            leaf = int(leaf)
            if leaf in leaf_fold:
                raise RuntimeError("physical leaf appears in multiple folds")
            leaf_fold[leaf] = f
    identity = [sorted(int(x) for x in leaves) for leaves in folds]
    return leaf_fold, identity


def audit(zl_path: Path) -> dict:
    data = zl_path.read_bytes()
    got_blob = git_blob_sha1(data)
    got_sha = hashlib.sha256(data).hexdigest()
    if got_blob != EXPECTED_ZL3B_BLOB or got_sha != EXPECTED_ZL3B_SHA256:
        raise RuntimeError(f"ZL3b authority mismatch blob={got_blob} sha256={got_sha}")
    lines = data.decode("utf-8").splitlines()
    if not lines or lines[0].strip() != "#=IVTFF Eva- 2.0 M 5":
        raise RuntimeError("unexpected ZL3b IVTFF/EVA header")

    leaf_fold, fold_identity = frozen_fold_authority(zl_path)
    currier = page_currier_authority(lines)

    by_fold = {
        str(f): {"real_space": 0, "mid_token": 0, "p2_real_space": 0, "clean_tokens": 0}
        for f in range(N_FOLDS)
    }
    by_currier = {
        "A": {"real_space": 0, "mid_token": 0, "p2_real_space": 0, "clean_tokens": 0},
        "B": {"real_space": 0, "mid_token": 0, "p2_real_space": 0, "clean_tokens": 0},
        "UNKNOWN": {"real_space": 0, "mid_token": 0, "p2_real_space": 0, "clean_tokens": 0},
    }
    atom_inventory = Counter()
    mid_lengths = Counter()
    token_unclean = Counter()
    real_exclusions = Counter()
    mid_exclusions = Counter()
    locus_counts = Counter()
    real_ids = []
    mid_ids = []
    p2_ids = []

    for source_line_no, line in enumerate(lines, start=1):
        m = LOCUS_RE.match(line)
        if not m or "P" not in m.group("code"):
            continue
        locus_counts["p_loci_total"] += 1
        loc = m.group("loc")
        page = loc.split(".", 1)[0]
        lm = LEAF_RE.match(page)
        if not lm:
            locus_counts["p_loci_no_numeric_leaf"] += 1
            continue
        leaf = int(lm.group(1))
        if leaf not in leaf_fold:
            locus_counts["p_loci_outside_frozen_folds"] += 1
            continue
        fold = int(leaf_fold[leaf])
        c = currier.get(page, "UNKNOWN")
        if c not in ("A", "B"):
            c = "UNKNOWN"
        locus_counts["p_loci_in_frozen_folds"] += 1

        segments, n_dot = split_certain_spaces(m.group("body"))
        if n_dot != max(0, len(segments) - 1):
            raise RuntimeError(f"dot count mismatch at {loc}")

        atoms_by_segment: List[Optional[Tuple[str, ...]]] = []
        for si, raw in enumerate(segments):
            reasons = unclean_reasons(raw)
            atoms = None if reasons else atomize_clean(raw)
            if atoms is None and not reasons:
                reasons = ("atomizer_failure",)
            atoms_by_segment.append(atoms)
            if atoms is None:
                for r in reasons:
                    token_unclean[r] += 1
                    mid_exclusions[r] += 1
                continue

            by_fold[str(fold)]["clean_tokens"] += 1
            by_currier[c]["clean_tokens"] += 1
            atom_inventory.update(atoms)
            if len(atoms) < 4:
                mid_exclusions["fewer_than_4_atoms"] += 1
                continue
            cut = len(atoms) // 2
            if cut < 2 or len(atoms) - cut < 2:
                raise RuntimeError("MID_TOKEN cut support invariant failed")
            by_fold[str(fold)]["mid_token"] += 1
            by_currier[c]["mid_token"] += 1
            mid_lengths[str(len(atoms))] += 1
            mid_ids.append((loc, source_line_no, si, len(atoms), cut, fold))

        for bi in range(n_dot):
            left = atoms_by_segment[bi]
            right = atoms_by_segment[bi + 1]
            if left is None:
                real_exclusions["left_unclean"] += 1
            if right is None:
                real_exclusions["right_unclean"] += 1
            if left is None or right is None:
                continue
            if len(left) < 2:
                real_exclusions["left_fewer_than_2_atoms"] += 1
            if len(right) < 2:
                real_exclusions["right_fewer_than_2_atoms"] += 1
            if len(left) < 2 or len(right) < 2:
                continue

            by_fold[str(fold)]["real_space"] += 1
            by_currier[c]["real_space"] += 1
            real_ids.append((loc, source_line_no, bi, len(left), len(right), fold))
            if len(left) >= 3 and len(right) >= 3:
                by_fold[str(fold)]["p2_real_space"] += 1
                by_currier[c]["p2_real_space"] += 1
                p2_ids.append((loc, source_line_no, bi, len(left), len(right), fold))
            else:
                real_exclusions["p2_side_fewer_than_3_atoms"] += 1

    support = {
        "real_space_all_folds_nonzero": all(by_fold[str(f)]["real_space"] > 0 for f in range(N_FOLDS)),
        "mid_token_all_folds_nonzero": all(by_fold[str(f)]["mid_token"] > 0 for f in range(N_FOLDS)),
        "p2_real_space_all_folds_nonzero": all(by_fold[str(f)]["p2_real_space"] > 0 for f in range(N_FOLDS)),
    }
    gate_pass = all(support.values())

    return {
        "schema": "issue112-phase4a-gate0-v1",
        "phase": "ISSUE112_PHASE4A_GATE0",
        "source": {
            "filename": zl_path.name,
            "git_blob_sha1": got_blob,
            "sha256": got_sha,
            "bytes": len(data),
            "header": lines[0].strip(),
        },
        "representation": {
            "primary_real_space": "literal IVTFF '.' certain word-space only",
            "excluded_space_markers": [", uncertain word space", "<-> / <~> drawing interruption"],
            "basic_eva_letters": "".join(sorted(BASIC_EVA)),
            "connected_composites_longest_match": list(CONNECTED_COMPOSITES),
            "mid_cut": "floor(n_atoms/2), requiring >=2 atoms on each side",
            "p2_support_rule": "REAL_SPACE with >=3 atoms on each observed side",
            "structural_edge_markers_removed_only_at_edges": ["<%>", "<$>"],
        },
        "fold_authority": {
            "source": "phase62b_n0.parse_voynich + physical_leaf_folds; membership only",
            "identity": fold_identity,
            "identity_sha256": sha256_obj(fold_identity),
            "n_leaves": len(leaf_fold),
        },
        "population": {
            "real_space": len(real_ids),
            "mid_token": len(mid_ids),
            "p2_real_space": len(p2_ids),
            "event_id_hashes": {
                "real_space_sha256": sha256_obj(real_ids),
                "mid_token_sha256": sha256_obj(mid_ids),
                "p2_real_space_sha256": sha256_obj(p2_ids),
            },
        },
        "by_fold": by_fold,
        "by_currier": by_currier,
        "mid_source_token_length_atoms": dict(sorted(mid_lengths.items(), key=lambda kv: int(kv[0]))),
        "raw_atom_inventory_clean_tokens": dict(sorted(atom_inventory.items())),
        "exclusions": {
            "loci": dict(sorted(locus_counts.items())),
            "unclean_token_reasons": dict(sorted(token_unclean.items())),
            "mid_token": dict(sorted(mid_exclusions.items())),
            "real_space": dict(sorted(real_exclusions.items())),
        },
        "support": support,
        "gate_rule": "REAL_SPACE, MID_TOKEN and P2 REAL_SPACE must each be nonzero in all 5 frozen physical-leaf folds",
        "gate_pass": gate_pass,
        "firewall": {
            "predictive_scores_computed": False,
            "boundary_model_fitted": False,
            "slotparser_used_for_event_eligibility": False,
            "target_surface_metrics_used": False,
            "issue84_target_used": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
        },
    }


def self_test() -> None:
    assert atomize_clean("qokchody") == ("q", "o", "k", "ch", "o", "d", "y")
    assert atomize_clean("cthaiin") == ("cth", "a", "i", "i", "n")
    assert atomize_clean("shckhey") == ("sh", "ckh", "e", "y")
    assert atomize_clean("cphar") == ("cph", "a", "r")
    assert atomize_clean("cfhaiin") == ("cfh", "a", "i", "i", "n")
    assert atomize_clean("or,y") is None
    assert "uncertain_space_comma" in unclean_reasons("or,y")
    assert atomize_clean("d?n") is None
    assert atomize_clean("[sh:ch]y") is None
    assert atomize_clean("{cto}") is None
    assert atomize_clean("@192;chy") is None
    assert atomize_clean("qo<!bar over o>") is None
    assert atomize_clean("qo'ky") is None
    assert atomize_clean("wa") is None
    seg, n = split_certain_spaces("<%>fachys.ykal.ar.ataiin<$>")
    assert n == 3 and seg == ["fachys", "ykal", "ar", "ataiin"]
    seg, n = split_certain_spaces("<%>ol<->o,l,tchey.char<$>")
    assert n == 1 and seg == ["ol<->o,l,tchey", "char"]
    seg, n = split_certain_spaces("qo<!a.b>.ol.[a.b:c].dar")
    assert n == 3 and seg == ["qo<!a.b>", "ol", "[a.b:c]", "dar"]
    seg, n = split_certain_spaces("qo<!a.b>.ol.[a.b:c]")
    assert n == 2 and seg == ["qo<!a.b>", "ol", "[a.b:c]"]
    print("self-test OK")


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--self-test", action="store_true")
    g.add_argument("--audit", nargs=2, metavar=("ZL3B", "OUT"))
    args = ap.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    zl = Path(args.audit[0]).resolve()
    out_path = Path(args.audit[1]).resolve()
    result = audit(zl)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "gate_pass": result["gate_pass"],
        "population": result["population"],
        "support": result["support"],
    }, indent=2, sort_keys=True))
    return 0 if result["gate_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
