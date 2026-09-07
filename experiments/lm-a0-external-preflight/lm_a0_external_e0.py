#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from lxml import etree

TEI = "{http://www.tei-c.org/ns/1.0}"
EXCLUDED_ANCESTORS = {"fw"}


def lname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def norm_lex(s: str) -> str:
    s = unicodedata.normalize("NFC", s).casefold()
    out = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("M"):
            out.append(ch)
        else:
            out.append(" ")
    return " ".join("".join(out).split())


def rendered_text(el: etree._Element) -> str:
    return "".join(el.itertext())


@dataclass
class Occ:
    line_idx: int
    page: str | None
    surface: str
    expanded: str
    abbreviated: int
    source: str


def tokenize_plain(text: str) -> list[str]:
    n = norm_lex(text)
    return [t for t in n.split() if t]


def collect_lines(book: etree._Element) -> tuple[list[list[Occ]], dict]:
    """Walk TEI document order and split at physical <lb> milestones."""
    lines: list[list[Occ]] = [[]]
    line_break_no_after: set[int] = set()
    line_ambiguous_choice: set[int] = set()
    page = None
    malformed_choice = 0
    excluded_choice_lb = 0
    excluded_expan_error = 0
    excluded_multi_expansion = 0

    def append_plain(text: str | None, source: str = "literal") -> None:
        if not text:
            return
        for tok in tokenize_plain(text):
            lines[-1].append(Occ(len(lines) - 1, page, tok, tok, 0, source))

    def walk(el: etree._Element) -> None:
        nonlocal page, malformed_choice, excluded_choice_lb
        nonlocal excluded_expan_error, excluded_multi_expansion
        tag = lname(el.tag)
        if tag in EXCLUDED_ANCESTORS or tag == "teiHeader":
            return
        if tag == "pb":
            page = el.get("n") or el.get("facs")
            return
        if tag == "lb":
            prev = len(lines) - 1
            if el.get("break") == "no":
                line_break_no_after.add(prev)
            lines.append([])
            return
        if tag == "choice":
            abbr = el.find(f"{TEI}abbr")
            expan = el.find(f"{TEI}expan")
            if abbr is None or expan is None:
                malformed_choice += 1
                return
            if abbr.find(f".//{TEI}lb") is not None or expan.find(f".//{TEI}lb") is not None:
                excluded_choice_lb += 1
                line_ambiguous_choice.add(len(lines) - 1)
                # Preserve physical line count from one branch only, but do not
                # treat a split word as an eligible lexical occurrence.
                for n in abbr.iter():
                    if n is not abbr and lname(n.tag) == "lb":
                        prev = len(lines) - 1
                        if n.get("break") == "no":
                            line_break_no_after.add(prev)
                        lines.append([])
                        line_ambiguous_choice.add(len(lines) - 1)
                return
            a = norm_lex(rendered_text(abbr))
            e = norm_lex(rendered_text(expan))
            if not a or not e:
                malformed_choice += 1
                return
            if e == "error":
                excluded_expan_error += 1
                return
            if len(e.split()) != 1:
                excluded_multi_expansion += 1
                return
            lines[-1].append(Occ(len(lines) - 1, page, a, e, int(a != e), "choice"))
            return

        append_plain(el.text)
        for child in el:
            walk(child)
            append_plain(child.tail)

    walk(book)

    bad = set(line_ambiguous_choice)
    for i in line_break_no_after:
        bad.add(i)
        bad.add(i + 1)

    eligible_lines: list[list[Occ]] = []
    for i, line in enumerate(lines):
        if i in bad or not line:
            continue
        for o in line:
            o.line_idx = len(eligible_lines)
        eligible_lines.append(line)

    meta = {
        "raw_physical_line_spans": len(lines),
        "eligible_nonempty_lines": len(eligible_lines),
        "excluded_line_indices_count": len(bad),
        "break_no_boundaries": len(line_break_no_after),
        "choices_spanning_lb": excluded_choice_lb,
        "malformed_choices": malformed_choice,
        "expan_error_choices": excluded_expan_error,
        "multiword_expansion_choices": excluded_multi_expansion,
    }
    return eligible_lines, meta


def hypergeom_pmf(n: int, a: int, f: int) -> dict[int, float]:
    lo = max(0, f - (n - a))
    hi = min(a, f)
    den = math.comb(n, f)
    return {
        x: math.comb(a, x) * math.comb(n - a, f - x) / den
        for x in range(lo, hi + 1)
    }


def convolve(d1: dict[int, float], d2: dict[int, float]) -> dict[int, float]:
    out: dict[int, float] = defaultdict(float)
    for x, px in d1.items():
        for y, py in d2.items():
            out[x + y] += px * py
    return dict(out)


def score(lines: list[list[Occ]], final_k: int) -> dict:
    rows = []
    for line in lines:
        line_len = len(line)
        for j, o in enumerate(line):
            rows.append((o, int(j >= max(0, line_len - final_k)), int(j == 0), line_len, j))

    bylex: dict[str, list[tuple]] = defaultdict(list)
    for r in rows:
        bylex[r[0].expanded].append(r)
    eligible = {
        lex: rr
        for lex, rr in bylex.items()
        if any(r[0].abbreviated for r in rr)
        and any(not r[0].abbreviated for r in rr)
    }

    strata = []
    dist = {0: 1.0}
    obs = 0
    exp = 0.0
    var = 0.0
    for lex, rr in eligible.items():
        n = len(rr)
        a = sum(r[0].abbreviated for r in rr)
        f = sum(r[1] for r in rr)
        x = sum(r[0].abbreviated * r[1] for r in rr)
        if f == 0 or f == n:
            continue
        pmf = hypergeom_pmf(n, a, f)
        dist = convolve(dist, pmf)
        e = a * f / n
        v = f * (a / n) * (1 - a / n) * ((n - f) / (n - 1)) if n > 1 else 0.0
        strata.append(
            {
                "lexeme": lex,
                "n": n,
                "a": a,
                "f": f,
                "x": x,
                "expected_x": e,
                "deviation": x - e,
            }
        )
        obs += x
        exp += e
        var += v

    p_ge = sum(p for x, p in dist.items() if x >= obs) if dist else 1.0
    p_le = sum(p for x, p in dist.items() if x <= obs) if dist else 1.0
    p_two = min(1.0, 2 * min(p_ge, p_le))
    z = (obs - exp) / math.sqrt(var) if var > 0 else None

    raw_final = [r for r in rows if r[1]]
    raw_non = [r for r in rows if not r[1]]
    first = [r for r in rows if r[2]]
    nonfirst = [r for r in rows if not r[2]]

    def rate(rr):
        return sum(r[0].abbreviated for r in rr) / len(rr) if rr else None

    return {
        "final_k": final_k,
        "eligible_lexemes_mixed": len(eligible),
        "informative_positional_strata": len(strata),
        "X_observed": obs,
        "X_expected": exp,
        "variance": var,
        "z": z,
        "p_one_sided_enrichment": p_ge,
        "p_two_sided_doubled_tail": p_two,
        "raw_abbreviation_rate_final": rate(raw_final),
        "raw_abbreviation_rate_nonfinal": rate(raw_non),
        "raw_abbreviation_rate_first": rate(first),
        "raw_abbreviation_rate_nonfirst": rate(nonfirst),
        "n_occurrences_all": len(rows),
        "n_abbreviated_all": sum(r[0].abbreviated for r in rows),
        "top_strata_abs_deviation": sorted(
            strata, key=lambda s: abs(s["deviation"]), reverse=True
        )[:20],
    }


def analyze(path: Path) -> dict:
    parser = etree.XMLParser(remove_blank_text=False, recover=False, huge_tree=True)
    tree = etree.parse(str(path), parser)
    root = tree.getroot()
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    books = root.xpath(".//tei:div[@type='book'][@n='07']", namespaces=ns)
    if len(books) != 1:
        raise RuntimeError(f"Expected exactly one Book 07 div, found {len(books)}")
    lines, meta = collect_lines(books[0])
    primary = score(lines, 1)
    sensitivity = score(lines, 2)
    classification = "E0_INVALID_OR_INDETERMINATE"
    if primary["informative_positional_strata"] > 0:
        if (
            primary["X_observed"] > primary["X_expected"]
            and primary["p_one_sided_enrichment"] <= 0.05
            and sensitivity["X_observed"] > sensitivity["X_expected"]
        ):
            classification = "E0_POSITIVE_FEASIBILITY"
        else:
            classification = "E0_NO_EXTERNAL_SUPPORT_ON_THIS_SAMPLE"

    pages = Counter(o.page for line in lines for o in line)
    line_lengths = Counter(len(line) for line in lines)
    return {
        "experiment": "LM-A0 external scribal preflight E0",
        "source": str(path),
        "population_meta": meta,
        "pages_token_counts": dict(sorted((str(k), v) for k, v in pages.items())),
        "line_length_token_counts": dict(sorted(line_lengths.items())),
        "primary_FINAL1": primary,
        "sensitivity_FINAL2": sensitivity,
        "classification": classification,
    }


def synthetic_preflight() -> None:
    xml = '''<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><div type="book" n="07"><p>
<lb n="1"/>alpha <choice><abbr>bt</abbr><expan>beta</expan></choice>
<lb n="2"/>beta gamma
<lb n="3"/>alpha beta
<lb n="4"/>gamma <choice><abbr>bt</abbr><expan>beta</expan></choice>
</p></div></body></text></TEI>'''
    p = Path("/tmp/lm_a0_synthetic.xml")
    p.write_text(xml, encoding="utf-8")
    r = analyze(p)
    assert r["primary_FINAL1"]["eligible_lexemes_mixed"] == 1
    assert r["primary_FINAL1"]["X_observed"] == 2
    assert r["primary_FINAL1"]["X_expected"] == 1.5
    print("SYNTHETIC_PREFLIGHT_OK")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("xml", nargs="?", type=Path)
    ap.add_argument("--synthetic-preflight", action="store_true")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    if args.synthetic_preflight:
        synthetic_preflight()
        return
    if args.xml is None:
        ap.error("xml path required unless --synthetic-preflight")
    result = analyze(args.xml)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
