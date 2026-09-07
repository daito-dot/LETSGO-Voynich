#!/usr/bin/env python3
"""Frozen ORIFLAMMS E1 scorer for LM-A0 external replication.

Scientific contract: research/LM_A0_EXTERNAL_E1_ORIFLAMMS_SELECTION_PLAN_20260907.md
Roster: experiments/lm-a0-external-preflight/oriflamms_e1_frozen_roster.json

The scorer is intended to be frozen and synthetic-tested before any E1 effect
reveal. It never selects manuscripts from observed abbreviation behavior.
"""
from __future__ import annotations

import argparse
import json
import math
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from lxml import etree

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
TEI = "{http://www.tei-c.org/ns/1.0}"


def lname(tag) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def parse_xml(path: Path) -> etree._ElementTree:
    return etree.parse(
        str(path),
        etree.XMLParser(
            load_dtd=True,
            resolve_entities=True,
            no_network=True,
            recover=False,
            huge_tree=True,
        ),
    )


def norm_lex(s: str) -> str:
    """Frozen E1 normalization: NFC, casefold, trim edge nonletters only."""
    s = unicodedata.normalize("NFC", s).casefold()
    i = 0
    j = len(s)
    while i < j and not (unicodedata.category(s[i]).startswith("L") or unicodedata.category(s[i]).startswith("M")):
        i += 1
    while j > i and not (unicodedata.category(s[j - 1]).startswith("L") or unicodedata.category(s[j - 1]).startswith("M")):
        j -= 1
    return s[i:j]


def render_node(node: etree._Element, mode: str) -> str:
    """Render a word choosing abbr or expan branches in every choice."""
    if mode not in {"surface", "expanded"}:
        raise ValueError(mode)
    tag = lname(node.tag)
    if tag == "lb":
        return ""
    if tag == "del":
        return ""
    if tag == "choice":
        branch_tag = "abbr" if mode == "surface" else "expan"
        branches = node.findall(f"{TEI}{branch_tag}")
        if len(branches) != 1:
            raise ValueError(f"choice has {len(branches)} {branch_tag} branches")
        return render_node(branches[0], mode)

    pieces = [node.text or ""]
    for child in node:
        ctag = lname(child.tag)
        if tag == "choice" and ctag in {"abbr", "expan"}:
            continue
        pieces.append(render_node(child, mode))
        pieces.append(child.tail or "")
    return "".join(pieces)


def has_unresolved_choice(w: etree._Element) -> bool:
    for c in w.xpath(".//tei:choice", namespaces=NS):
        if len(c.findall(f"{TEI}abbr")) != 1 or len(c.findall(f"{TEI}expan")) != 1:
            return True
        e = norm_lex(render_node(c.find(f"{TEI}expan"), "expanded"))
        if e == "error":
            return True
    return False


@dataclass
class Occ:
    manuscript: str
    line_id: str
    surface: str
    expanded: str
    abbreviated: int
    position: int = -1
    line_length: int = -1


def build_manuscript_lines(text: etree._Element, manuscript: str) -> tuple[list[list[Occ]], dict]:
    """Build physical lines from body paragraphs and frozen boundary exclusions.

    Only words inside body <p> blocks are admitted. Ordinary <lb> milestones
    start a new physical line. A word containing an internal <lb break='no'>
    is excluded, and the physical lines on both sides of every such boundary
    are marked bad, as preregistered.
    """
    lines: list[list[Occ]] = []
    bad_lines: set[int] = set()
    audit = Counter()

    paragraphs = text.xpath(".//tei:body//tei:p", namespaces=NS)

    def new_line() -> int:
        lines.append([])
        return len(lines) - 1

    for p_idx, p in enumerate(paragraphs):
        current = new_line()

        def walk(node: etree._Element) -> None:
            nonlocal current
            for child in node:
                tag = lname(child.tag)
                if tag == "fw":
                    audit["fw_blocks_excluded"] += 1
                    continue
                if tag == "w":
                    internal_lbs = child.xpath(".//tei:lb", namespaces=NS)
                    if internal_lbs:
                        audit["split_words_excluded"] += 1
                        bad_lines.add(current)
                        # Every internal physical boundary advances a line and
                        # invalidates the new adjacent line as well.
                        for lb in internal_lbs:
                            audit[f"internal_lb_break_{lb.get('break') or '<none>'}"] += 1
                            current = new_line()
                            bad_lines.add(current)
                        continue
                    if child.xpath(".//tei:del", namespaces=NS):
                        audit["words_with_del_excluded"] += 1
                        continue
                    if has_unresolved_choice(child):
                        audit["unresolved_choice_words_excluded"] += 1
                        continue
                    try:
                        surface = norm_lex(render_node(child, "surface"))
                        expanded = norm_lex(render_node(child, "expanded"))
                    except ValueError:
                        audit["render_error_words_excluded"] += 1
                        continue
                    if not surface or not expanded:
                        audit["empty_render_words_excluded"] += 1
                        continue
                    choices = child.xpath(".//tei:choice[tei:abbr and tei:expan]", namespaces=NS)
                    abbreviated = int(bool(choices) and surface != expanded)
                    lines[current].append(Occ(manuscript, f"{manuscript}:p{p_idx}:l{current}", surface, expanded, abbreviated))
                    audit["candidate_words"] += 1
                    continue
                if tag == "lb":
                    audit[f"external_lb_break_{child.get('break') or '<none>'}"] += 1
                    if child.get("break") == "no":
                        # Frozen compatibility rule: any explicitly nonbreaking
                        # physical split invalidates both adjacent lines.
                        bad_lines.add(current)
                        current = new_line()
                        bad_lines.add(current)
                    else:
                        current = new_line()
                    continue
                walk(child)

        walk(p)

    eligible: list[list[Occ]] = []
    for i, line in enumerate(lines):
        if i in bad_lines or not line:
            continue
        for j, o in enumerate(line):
            o.position = j
            o.line_length = len(line)
        eligible.append(line)

    audit["raw_line_slots"] = len(lines)
    audit["bad_line_slots"] = len(bad_lines)
    audit["eligible_nonempty_lines"] = len(eligible)
    audit["eligible_words"] = sum(len(x) for x in eligible)
    return eligible, dict(audit)


def hypergeom_pmf(n: int, a: int, f: int) -> dict[int, float]:
    lo = max(0, f - (n - a))
    hi = min(a, f)
    den = math.comb(n, f)
    return {x: math.comb(a, x) * math.comb(n - a, f - x) / den for x in range(lo, hi + 1)}


def convolve(a: dict[int, float], b: dict[int, float]) -> dict[int, float]:
    out: dict[int, float] = defaultdict(float)
    for x, px in a.items():
        for y, py in b.items():
            out[x + y] += px * py
    return dict(out)


def score_occurrences(lines_by_ms: dict[str, list[list[Occ]]], final_k: int) -> dict:
    strata: dict[tuple[str, str], list[tuple[Occ, int]]] = defaultdict(list)
    raw_final = []
    raw_nonfinal = []
    per_ms_raw = Counter()

    for ms, lines in lines_by_ms.items():
        for line in lines:
            cutoff = max(0, len(line) - final_k)
            for o in line:
                is_final = int(o.position >= cutoff)
                strata[(ms, o.expanded)].append((o, is_final))
                per_ms_raw[(ms, "n")] += 1
                per_ms_raw[(ms, "a")] += o.abbreviated
                (raw_final if is_final else raw_nonfinal).append(o)

    dist = {0: 1.0}
    pooled_obs = 0
    pooled_exp = 0.0
    pooled_var = 0.0
    informative = []
    per_ms = defaultdict(lambda: {"observed": 0, "expected": 0.0, "variance": 0.0, "informative_strata": 0})

    for (ms, lex), rr in sorted(strata.items()):
        n = len(rr)
        a = sum(o.abbreviated for o, _ in rr)
        f = sum(flag for _, flag in rr)
        if a == 0 or a == n or f == 0 or f == n:
            continue
        x = sum(o.abbreviated * flag for o, flag in rr)
        e = a * f / n
        v = f * (a / n) * (1 - a / n) * ((n - f) / (n - 1)) if n > 1 else 0.0
        dist = convolve(dist, hypergeom_pmf(n, a, f))
        pooled_obs += x
        pooled_exp += e
        pooled_var += v
        per_ms[ms]["observed"] += x
        per_ms[ms]["expected"] += e
        per_ms[ms]["variance"] += v
        per_ms[ms]["informative_strata"] += 1
        informative.append({
            "manuscript": ms,
            "lexeme": lex,
            "n": n,
            "a": a,
            "f": f,
            "x": x,
            "expected": e,
            "deviation": x - e,
        })

    p_ge = sum(p for x, p in dist.items() if x >= pooled_obs)
    p_le = sum(p for x, p in dist.items() if x <= pooled_obs)
    p_two = min(1.0, 2 * min(p_ge, p_le))
    z = (pooled_obs - pooled_exp) / math.sqrt(pooled_var) if pooled_var > 0 else None

    manuscript_diag = []
    for ms in sorted(lines_by_ms):
        m = per_ms.get(ms)
        if not m or m["informative_strata"] == 0:
            manuscript_diag.append({"manuscript": ms, "informative": False})
            continue
        mv = m["variance"]
        manuscript_diag.append({
            "manuscript": ms,
            "informative": True,
            "informative_strata": m["informative_strata"],
            "observed": m["observed"],
            "expected": m["expected"],
            "deviation": m["observed"] - m["expected"],
            "z": (m["observed"] - m["expected"]) / math.sqrt(mv) if mv > 0 else None,
        })

    informative_ms = [m for m in manuscript_diag if m.get("informative")]
    positive_ms = [m for m in informative_ms if m["observed"] > m["expected"]]

    def raw_rate(xs: Iterable[Occ]):
        xs = list(xs)
        return (sum(o.abbreviated for o in xs) / len(xs)) if xs else None

    return {
        "final_k": final_k,
        "informative_strata": len(informative),
        "observed": pooled_obs,
        "expected": pooled_exp,
        "variance": pooled_var,
        "z": z,
        "p_one_sided_enrichment": p_ge,
        "p_two_sided_doubled_tail": p_two,
        "raw_abbreviation_rate_final": raw_rate(raw_final),
        "raw_abbreviation_rate_nonfinal": raw_rate(raw_nonfinal),
        "informative_manuscript_count": len(informative_ms),
        "positive_direction_manuscript_count": len(positive_ms),
        "positive_direction_fraction": (len(positive_ms) / len(informative_ms)) if informative_ms else None,
        "manuscript_diagnostics": manuscript_diag,
        "top_strata_abs_deviation": sorted(informative, key=lambda r: abs(r["deviation"]), reverse=True)[:30],
    }


def analyze(words_path: Path, roster_path: Path) -> dict:
    roster_doc = json.load(open(roster_path, encoding="utf-8"))
    if roster_doc.get("effect_statistics_computed") is not False:
        raise RuntimeError("roster authority is not effect-sealed")
    roster = roster_doc["eligible_roster"]
    selected = {int(r["ordinal_1based"]): r for r in roster}
    if len(selected) != 23:
        raise RuntimeError(f"expected frozen 23-manuscript roster, got {len(selected)}")

    tree = parse_xml(words_path)
    teis = tree.xpath("/tei:teiCorpus/tei:TEI", namespaces=NS)
    if len(teis) != 102:
        raise RuntimeError(f"expected pinned 102-document word corpus, got {len(teis)}")

    lines_by_ms = {}
    extraction_audit = {}
    for ordinal, r in selected.items():
        tei = teis[ordinal - 1]
        texts = tei.xpath("./tei:text", namespaces=NS)
        if len(texts) != 1:
            raise RuntimeError(f"ordinal {ordinal}: expected one text, got {len(texts)}")
        ms = r["text_n"]
        lines, audit = build_manuscript_lines(texts[0], ms)
        lines_by_ms[ms] = lines
        extraction_audit[ms] = audit

    primary = score_occurrences(lines_by_ms, 1)
    sensitivity = score_occurrences(lines_by_ms, 2)

    invalid = primary["informative_manuscript_count"] == 0
    if invalid:
        classification = "E1_INVALID_OR_INDETERMINATE"
    else:
        replicated = (
            len(selected) >= 3
            and primary["observed"] > primary["expected"]
            and primary["p_one_sided_enrichment"] <= 0.05
            and primary["positive_direction_fraction"] is not None
            and primary["positive_direction_fraction"] >= (2 / 3)
            and sensitivity["observed"] > sensitivity["expected"]
        )
        classification = "E1_REPLICATED_EXTERNAL_SUPPORT" if replicated else "E1_NO_REPLICATION"

    return {
        "experiment": "LM-A0 ORIFLAMMS E1 external replication",
        "roster_count": len(selected),
        "roster_text_n": [r["text_n"] for r in roster],
        "extraction_audit": extraction_audit,
        "primary_FINAL1": primary,
        "sensitivity_FINAL2": sensitivity,
        "classification": classification,
    }


def synthetic_preflight() -> None:
    # Synthetic corpus: one document in slot 1, with beta occurring both
    # abbreviated and unabbreviated. One split word with break=no invalidates
    # its adjacent lines. This checks line construction, branch rendering and
    # the hypergeometric scorer without any ORIFLAMMS target data.
    xml = '''<?xml version="1.0"?><teiCorpus xmlns="http://www.tei-c.org/ns/1.0">
<TEI><text><body><p><lb/><w>alpha</w><w><choice><abbr>bt</abbr><expan>beta</expan></choice></w>
<lb/><w>beta</w><w>gamma</w>
<lb/><w>alpha</w><w><choice><abbr>b</abbr><expan>beta</expan></choice></w>
<lb/><w><seg>gam</seg><lb break="no"/><seg>ma</seg></w><w>beta</w>
<lb/><w>beta</w><w>delta</w></p></body></text></TEI>
''' + ''.join('<TEI><text><body><p><lb/><w>x</w></p></body></text></TEI>' for _ in range(101)) + '</teiCorpus>'
    wp = Path('/tmp/oriflamms_e1_synth.xml')
    wp.write_text(xml, encoding='utf-8')
    roster = {
        "effect_statistics_computed": False,
        "eligible_roster": [
            {"text_n": str(i), "ordinal_1based": i, "idno": f"S{i}"}
            for i in range(1, 24)
        ],
    }
    rp = Path('/tmp/oriflamms_e1_synth_roster.json')
    rp.write_text(json.dumps(roster), encoding='utf-8')
    r = analyze(wp, rp)
    assert r['roster_count'] == 23
    assert r['extraction_audit']['1']['split_words_excluded'] == 1
    assert r['extraction_audit']['1']['internal_lb_break_no'] == 1
    assert r['primary_FINAL1']['informative_strata'] >= 1
    print('SYNTHETIC_E1_PREFLIGHT_OK')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('words', nargs='?', type=Path)
    ap.add_argument('roster', nargs='?', type=Path)
    ap.add_argument('--out', type=Path)
    ap.add_argument('--synthetic-preflight', action='store_true')
    args = ap.parse_args()
    if args.synthetic_preflight:
        synthetic_preflight()
        return
    if args.words is None or args.roster is None:
        ap.error('words and roster are required unless --synthetic-preflight')
    result = analyze(args.words, args.roster)
    s = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.write_text(s, encoding='utf-8')
    else:
        print(s)


if __name__ == '__main__':
    main()
