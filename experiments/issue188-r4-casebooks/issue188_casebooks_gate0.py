#!/usr/bin/env python3
"""Issue #188: score-free Casebooks structural composability audit."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from lxml import etree

EXPECTED_CASEBOOKS_COMMIT = "9d42295d72b5ba8889575a32d79311cc72bce73a"
MARKER = "NO ISSUE188 SCIENTIFIC S1 SCORE COMPUTED"
TEI = "http://www.tei-c.org/ns/1.0"
CB = "http://www.magicandmedicine.hps.cam.ac.uk/ns/1.0"
NS = {"tei": TEI, "cb": CB}
XML = "http://www.w3.org/XML/1998/namespace"
SKIP_TAGS = {"note", "reg", "corr", "expan"}
CHOICE_PREF = ("orig", "sic", "abbr")


def local(el) -> str:
    return etree.QName(el).localname


def git_head(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def word_tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFC", text)
    out, cur = [], []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("M"):
            cur.append(ch)
        else:
            if cur:
                out.append("".join(cur).lower())
                cur = []
    if cur:
        out.append("".join(cur).lower())
    return out


class DiplomaticLines:
    def __init__(self):
        self.lines = [""]
        self.seen_lb = False
        self.leading_nonspace_before_first_lb = False

    def add(self, text: str | None):
        if not text:
            return
        if not self.seen_lb and text.strip():
            self.leading_nonspace_before_first_lb = True
        self.lines[-1] += text

    def lb(self):
        if not self.seen_lb and not self.lines[-1].strip():
            self.seen_lb = True
            return
        self.seen_lb = True
        self.lines.append("")


def is_translation(el) -> bool:
    return "#translation" in (el.get("decls") or "").split()


def walk(el, out: DiplomaticLines):
    tag = local(el)
    if is_translation(el) or tag in SKIP_TAGS:
        return
    if tag == "lb":
        out.lb()
        return
    if tag == "choice":
        chosen = None
        children = list(el)
        for wanted in CHOICE_PREF:
            chosen = next((c for c in children if local(c) == wanted), None)
            if chosen is not None:
                break
        if chosen is None:
            chosen = next((c for c in children if local(c) not in {"reg", "corr", "expan"}), None)
        if chosen is not None:
            walk(chosen, out)
        return

    out.add(el.text)
    for child in el:
        walk(child, out)
        out.add(child.tail)


def paragraph_lines(p) -> tuple[list[list[str]], bool]:
    d = DiplomaticLines()
    walk(p, d)
    lines = [word_tokens(x) for x in d.lines]
    # Preserve physical-line positions, including empty/short retained lines.
    return lines, d.leading_nonspace_before_first_lb


def valid_pseudo_indices(lines: list[list[str]]) -> list[int]:
    return [j for j in range(1, len(lines) - 2) if len(lines[j]) >= 5 and len(lines[j + 2]) >= 5]


def eligible(lines: list[list[str]]) -> bool:
    return len(lines) >= 3 and len(lines[0]) >= 5 and len(lines[2]) >= 5 and bool(valid_pseudo_indices(lines))


def first_attr(root, xpath: str, attr: str) -> str | None:
    vals = root.xpath(xpath, namespaces=NS)
    if not vals:
        return None
    return vals[0].get(attr)


def audit_case(path: Path, parser: etree.XMLParser) -> dict:
    tree = etree.parse(str(path), parser)
    root = tree.getroot()
    ps = root.xpath(".//tei:text/tei:body//tei:p", namespaces=NS)

    volume = first_attr(root, ".//tei:sourceDesc//tei:altIdentifier[@type='fn_number']/tei:idno", "n") or "UNKNOWN"
    hands = sorted({x for x in root.xpath(".//tei:profileDesc/tei:handNotes/tei:handNote/@sameAs", namespaces=NS) if x})
    hand_set = "+".join(hands) if hands else "UNKNOWN"
    practice = first_attr(root, ".//tei:profileDesc//cb:practice", "name") or "UNKNOWN"
    cats = sorted({x for x in root.xpath(".//tei:profileDesc/tei:textClass/tei:catRef/@target", namespaces=NS) if x})

    n_eligible = 0
    n_lines = 0
    n_tokens = 0
    lead_anom = 0
    line_count_hist = Counter()
    for p in ps:
        lines, leading = paragraph_lines(p)
        n_lines += len(lines)
        n_tokens += sum(len(x) for x in lines)
        lead_anom += int(leading)
        line_count_hist[len(lines)] += 1
        n_eligible += int(eligible(lines))

    return {
        "case": path.stem,
        "volume": volume,
        "hand_set": hand_set,
        "practice": practice,
        "consultation_classes": cats,
        "paragraphs": len(ps),
        "eligible_paragraphs": n_eligible,
        "physical_lines": n_lines,
        "tokens": n_tokens,
        "leading_text_before_first_lb_paragraphs": lead_anom,
        "line_count_hist": dict(sorted(line_count_hist.items())),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--casebooks", required=True, type=Path)
    args = ap.parse_args()
    repo = args.casebooks.resolve()
    head = git_head(repo)
    if head != EXPECTED_CASEBOOKS_COMMIT:
        raise RuntimeError(f"Casebooks authority changed: {head}")

    parser = etree.XMLParser(load_dtd=True, resolve_entities=True, no_network=True, recover=False, huge_tree=True)
    files = sorted((repo / "cases").glob("CASE*.xml"), key=lambda p: p.name)
    rows, failures = [], []
    for p in files:
        try:
            rows.append(audit_case(p, parser))
        except Exception as exc:
            failures.append({"case": p.stem, "error": f"{type(exc).__name__}: {exc}"})

    eligible_rows = [r for r in rows if r["eligible_paragraphs"] > 0]
    volume_eligible = Counter()
    hand_eligible = Counter()
    practice_eligible = Counter()
    consultation_eligible = Counter()
    for r in rows:
        n = r["eligible_paragraphs"]
        volume_eligible[r["volume"]] += n
        hand_eligible[r["hand_set"]] += n
        practice_eligible[r["practice"]] += n
        for c in r["consultation_classes"]:
            consultation_eligible[c] += n

    total_eligible = sum(r["eligible_paragraphs"] for r in rows)
    strong_volumes = sum(n >= 10 for n in volume_eligible.values())
    strong_hands = sum(n >= 20 for n in hand_eligible.values())
    admitted = bool(
        not failures
        and total_eligible >= 100
        and len(eligible_rows) >= 100
        and strong_volumes >= 5
        and strong_hands >= 2
    )

    out = {
        "schema": "issue188-r4-casebooks-gate0-v1",
        "issue": 188,
        "stage": "score_free_composability",
        "marker": MARKER,
        "scientific_score_computed": False,
        "casebooks_commit": head,
        "extraction": {
            "items": "tei:text/tei:body//tei:p",
            "line_marker": "tei:lb",
            "translation_subtrees_excluded": True,
            "note_subtrees_excluded": True,
            "choice_precedence": list(CHOICE_PREF),
            "normalized_tags_excluded": sorted(SKIP_TAGS - {"note"}),
            "tokenization": "NFC maximal Unicode Letter/Mark sequences, lowercase",
        },
        "totals": {
            "case_files": len(files),
            "parsed_cases": len(rows),
            "parse_failures": len(failures),
            "paragraphs": sum(r["paragraphs"] for r in rows),
            "eligible_paragraphs": total_eligible,
            "cases_with_eligible_paragraph": len(eligible_rows),
            "physical_lines": sum(r["physical_lines"] for r in rows),
            "tokens": sum(r["tokens"] for r in rows),
            "leading_text_before_first_lb_paragraphs": sum(r["leading_text_before_first_lb_paragraphs"] for r in rows),
            "source_volumes": len(volume_eligible),
            "hand_sets": len(hand_eligible),
            "source_volumes_with_at_least_10_eligible": strong_volumes,
            "hand_sets_with_at_least_20_eligible": strong_hands,
        },
        "admission": {
            "all_files_parse": not failures,
            "eligible_paragraphs_ge_100": total_eligible >= 100,
            "eligible_cases_ge_100": len(eligible_rows) >= 100,
            "five_volumes_ge_10": strong_volumes >= 5,
            "two_hand_sets_ge_20": strong_hands >= 2,
            "stage1_licensed": admitted,
        },
        "support_by_volume": dict(volume_eligible.most_common()),
        "support_by_hand_set": dict(hand_eligible.most_common()),
        "support_by_practice": dict(practice_eligible.most_common()),
        "support_by_consultation_class": dict(consultation_eligible.most_common()),
        "parse_failures": failures,
        "case_support": rows,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if admitted else 4


if __name__ == "__main__":
    raise SystemExit(main())
