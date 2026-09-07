#!/usr/bin/env python3
"""Issue #188: score-free Casebooks structural composability audit."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

EXPECTED_CASEBOOKS_COMMIT = "9d42295d72b5ba8889575a32d79311cc72bce73a"
MARKER = "NO ISSUE188 SCIENTIFIC S1 SCORE COMPUTED"
TEI = "http://www.tei-c.org/ns/1.0"
CB = "http://www.magicandmedicine.hps.cam.ac.uk/ns/1.0"
SKIP_TAGS = {"note", "reg", "corr", "expan"}
CHOICE_PREF = ("orig", "sic", "abbr")
DOCTYPE_RE = re.compile(r"<!DOCTYPE\s+TEI\s*\[.*?\]>", re.DOTALL)
ENTITY_RE = re.compile(r"&([A-Za-z_][A-Za-z0-9_.:-]*);")
PREDEFINED = {"amp", "lt", "gt", "quot", "apos"}
OPAQUE_ENTITY = "\ue000"  # Unicode Co, deliberately not a Letter/Mark token.


def local(el) -> str:
    tag = el.tag
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def git_head(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def standalone_xml(path: Path) -> tuple[str, int]:
    text = path.read_text(encoding="utf-8")
    text = DOCTYPE_RE.sub("", text)
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        if m.group(1) in PREDEFINED:
            return m.group(0)
        n += 1
        return OPAQUE_ENTITY

    return ENTITY_RE.sub(repl, text), n


def word_tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFC", text)
    out, cur = [], []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("M"):
            cur.append(ch)
        elif cur:
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
    return "#translation" in (el.attrib.get("decls") or "").split()


def walk(el, out: DiplomaticLines):
    tag = local(el)
    if is_translation(el) or tag in SKIP_TAGS:
        return
    if tag == "lb":
        out.lb()
        return
    if tag == "choice":
        children = list(el)
        chosen = None
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
    return [word_tokens(x) for x in d.lines], d.leading_nonspace_before_first_lb


def eligible(lines: list[list[str]]) -> bool:
    if len(lines) < 3 or len(lines[0]) < 5 or len(lines[2]) < 5:
        return False
    return any(len(lines[j]) >= 5 and len(lines[j + 2]) >= 5 for j in range(1, len(lines) - 2))


def audit_case_path(path_s: str) -> dict:
    path = Path(path_s)
    try:
        text, entity_refs = standalone_xml(path)
        root = ET.fromstring(text)
        ps = root.findall(f".//{{{TEI}}}text/{{{TEI}}}body//{{{TEI}}}p")

        volume = "UNKNOWN"
        for alt in root.findall(f".//{{{TEI}}}sourceDesc//{{{TEI}}}altIdentifier"):
            if alt.attrib.get("type") == "fn_number":
                idno = alt.find(f"{{{TEI}}}idno")
                if idno is not None and idno.attrib.get("n"):
                    volume = idno.attrib["n"]
                    break
        hands = sorted({x.attrib.get("sameAs") for x in root.findall(f".//{{{TEI}}}profileDesc/{{{TEI}}}handNotes/{{{TEI}}}handNote") if x.attrib.get("sameAs")})
        hand_set = "+".join(hands) if hands else "UNKNOWN"
        practice_el = root.find(f".//{{{TEI}}}profileDesc//{{{CB}}}practice")
        practice = practice_el.attrib.get("name", "UNKNOWN") if practice_el is not None else "UNKNOWN"
        cats = sorted({x.attrib.get("target") for x in root.findall(f".//{{{TEI}}}profileDesc/{{{TEI}}}textClass/{{{TEI}}}catRef") if x.attrib.get("target")})

        n_eligible = n_lines = n_tokens = lead_anom = 0
        for p in ps:
            lines, leading = paragraph_lines(p)
            n_lines += len(lines)
            n_tokens += sum(len(x) for x in lines)
            lead_anom += int(leading)
            n_eligible += int(eligible(lines))
        return {
            "ok": True,
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
            "opaque_entity_refs": entity_refs,
        }
    except Exception as exc:
        return {"ok": False, "case": path.stem, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--casebooks", required=True, type=Path)
    args = ap.parse_args()
    repo = args.casebooks.resolve()
    head = git_head(repo)
    if head != EXPECTED_CASEBOOKS_COMMIT:
        raise RuntimeError(f"Casebooks authority changed: {head}")

    files = sorted((repo / "cases").glob("CASE*.xml"), key=lambda p: p.name)
    workers = min(4, max(1, os.cpu_count() or 1))
    rows, failures = [], []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for row in ex.map(audit_case_path, (str(p) for p in files), chunksize=250):
            (rows if row.get("ok") else failures).append(row)

    eligible_rows = [r for r in rows if r["eligible_paragraphs"] > 0]
    volume_eligible, hand_eligible = Counter(), Counter()
    practice_eligible, consultation_eligible = Counter(), Counter()
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
    admitted = bool(not failures and total_eligible >= 100 and len(eligible_rows) >= 100 and strong_volumes >= 5 and strong_hands >= 2)

    out = {
        "schema": "issue188-r4-casebooks-gate0-v2-transport",
        "issue": 188,
        "stage": "score_free_composability",
        "marker": MARKER,
        "scientific_score_computed": False,
        "casebooks_commit": head,
        "transport": {
            "doctype_removed": True,
            "non_predefined_named_entities": "opaque_private_use_placeholder",
            "placeholder_unicode_category": unicodedata.category(OPAQUE_ENTITY),
            "parallel_workers": workers,
        },
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
            "opaque_entity_refs": sum(r["opaque_entity_refs"] for r in rows),
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
        "eligible_case_support": eligible_rows,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if admitted else 4


if __name__ == "__main__":
    raise SystemExit(main())
