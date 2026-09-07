#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from lxml import etree

NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def parse_xml(path: Path) -> etree._ElementTree:
    parser = etree.XMLParser(
        load_dtd=True,
        resolve_entities=True,
        no_network=True,
        recover=False,
        huge_tree=True,
    )
    return etree.parse(str(path), parser)


def year_of(value: str | None) -> int | None:
    if not value:
        return None
    m = re.match(r"^\s*(\d{4})", value)
    return int(m.group(1)) if m else None


def one_text(el: etree._Element | None) -> str | None:
    if el is None:
        return None
    s = " ".join("".join(el.itertext()).split())
    return s or None


def date_interval(text: etree._Element) -> tuple[int | None, int | None, str]:
    dates = text.xpath(
        ".//tei:msDesc/tei:history/tei:origin/tei:date",
        namespaces=NS,
    )
    usable: list[tuple[int, int]] = []
    for d in dates:
        when = year_of(d.get("when"))
        nb = year_of(d.get("notBefore"))
        na = year_of(d.get("notAfter"))
        if when is not None:
            usable.append((when, when))
        elif nb is not None and na is not None:
            usable.append((nb, na))
        elif nb is not None or na is not None:
            return None, None, "OPEN_ENDED_DATE"
    if len(usable) == 1:
        return usable[0][0], usable[0][1], "OK"
    if len(usable) == 0:
        return None, None, "NO_USABLE_DATE"
    if len(set(usable)) == 1:
        y0, y1 = usable[0]
        return y0, y1, "OK_DUPLICATE_SAME_DATE"
    return None, None, "DATE_AMBIGUOUS"


def top_texts(tree: etree._ElementTree) -> list[etree._Element]:
    return tree.xpath("/tei:TEI/tei:text/tei:group/tei:text", namespaces=NS)


def metadata_record(text: etree._Element) -> dict:
    n = text.get("n")
    msdescs = text.xpath(".//tei:listWit/tei:witness/tei:msDesc", namespaces=NS)
    unique_ms = len(msdescs) == 1
    ms = msdescs[0] if unique_ms else None
    settlement = one_text(ms.find("tei:msIdentifier/tei:settlement", NS)) if ms is not None else None
    repository = one_text(ms.find("tei:msIdentifier/tei:repository", NS)) if ms is not None else None
    idno = one_text(ms.find("tei:msIdentifier/tei:idno", NS)) if ms is not None else None
    earliest, latest, date_status = date_interval(text)

    scripts = []
    for sn in text.xpath(".//tei:msDesc/tei:physDesc/tei:scriptDesc/tei:scriptNote", namespaces=NS):
        val = sn.get("script") or one_text(sn)
        if val and val not in scripts:
            scripts.append(val)

    languages = []
    for tl in text.xpath(".//tei:msDesc//tei:textLang", namespaces=NS):
        for key in ("mainLang", "otherLangs"):
            val = tl.get(key)
            if val:
                for item in val.split():
                    if item not in languages:
                        languages.append(item)
        txt = one_text(tl)
        if txt and txt not in languages:
            languages.append(txt)

    return {
        "text_n": n,
        "settlement": settlement,
        "repository": repository,
        "idno": idno,
        "manuscript_identity_unambiguous": unique_ms and bool(settlement or repository or idno),
        "earliest": earliest,
        "latest": latest,
        "date_status": date_status,
        "scripts": scripts,
        "languages": languages,
    }


def inventory(metadata_path: Path, word_path: Path) -> dict:
    mtree = parse_xml(metadata_path)
    wtree = parse_xml(word_path)

    meta_texts = top_texts(mtree)
    word_texts = top_texts(wtree)
    meta_by_n: dict[str, list[etree._Element]] = {}
    word_by_n: dict[str, list[etree._Element]] = {}
    for t in meta_texts:
        meta_by_n.setdefault(t.get("n") or "", []).append(t)
    for t in word_texts:
        word_by_n.setdefault(t.get("n") or "", []).append(t)

    records = []
    for n in sorted(meta_by_n, key=lambda x: (int(x) if x.isdigit() else 10**9, x)):
        if len(meta_by_n[n]) != 1:
            rec = {
                "text_n": n,
                "metadata_text_unique": False,
                "word_text_unique": len(word_by_n.get(n, [])) == 1,
                "eligible": False,
                "exclusion_reasons": ["AMBIGUOUS_METADATA_TEXT_N"],
            }
            records.append(rec)
            continue

        rec = metadata_record(meta_by_n[n][0])
        rec["metadata_text_unique"] = True
        wmatches = word_by_n.get(n, [])
        rec["word_text_unique"] = len(wmatches) == 1
        if len(wmatches) == 1:
            wt = wmatches[0]
            rec["has_lb"] = bool(wt.xpath(".//tei:lb", namespaces=NS))
            rec["has_w"] = bool(wt.xpath(".//tei:w", namespaces=NS))
            rec["has_valid_choice"] = bool(
                wt.xpath(".//tei:choice[tei:abbr and tei:expan]", namespaces=NS)
            )
        else:
            rec["has_lb"] = False
            rec["has_w"] = False
            rec["has_valid_choice"] = False

        reasons = []
        if not rec["manuscript_identity_unambiguous"]:
            reasons.append("AMBIGUOUS_MANUSCRIPT_IDENTITY")
        if rec["date_status"] not in {"OK", "OK_DUPLICATE_SAME_DATE"}:
            reasons.append(rec["date_status"])
        if rec["earliest"] is not None and rec["latest"] is not None:
            if not (rec["earliest"] >= 1375 and rec["latest"] <= 1450):
                reasons.append("OUTSIDE_FROZEN_1375_1450_INTERVAL")
        else:
            if "NO_USABLE_DATE" not in reasons and "DATE_AMBIGUOUS" not in reasons and "OPEN_ENDED_DATE" not in reasons:
                reasons.append("NO_CLOSED_DATE_INTERVAL")
        if not rec["word_text_unique"]:
            reasons.append("WORD_TEXT_ASSOCIATION_NOT_UNIQUE")
        if not rec["has_lb"]:
            reasons.append("NO_LB")
        if not rec["has_w"]:
            reasons.append("NO_W")
        if not rec["has_valid_choice"]:
            reasons.append("NO_VALID_CHOICE")
        rec["eligible"] = not reasons
        rec["exclusion_reasons"] = reasons
        records.append(rec)

    roster = [r for r in records if r.get("eligible")]
    return {
        "experiment": "LM-A0 ORIFLAMMS E1 metadata-only inventory",
        "selection_rule": "closed date interval fully contained in 1375-1450 plus unique manuscript identity and structural presence of lb/w/valid choice",
        "effect_statistics_computed": False,
        "metadata_text_count": len(meta_texts),
        "word_text_count": len(word_texts),
        "eligible_manuscript_count": len(roster),
        "eligible_roster": roster,
        "all_records": records,
    }


def synthetic_preflight() -> None:
    dtd = '<!ENTITY foo "<choice><abbr>x</abbr><expan>xyz</expan></choice>">'
    base = Path("/tmp/oriflamms_e1_synth")
    (base / "texts").mkdir(parents=True, exist_ok=True)
    (base / "abbreviations.dtd").write_text(dtd, encoding="utf-8")
    meta = '''<?xml version="1.0"?><!DOCTYPE TEI [<!ENTITY % abbr SYSTEM "abbreviations.dtd"> %abbr;]><TEI xmlns="http://www.tei-c.org/ns/1.0"><text><group><text n="1"><body><listWit><witness><msDesc><msIdentifier><settlement>X</settlement><repository>Y</repository><idno>Z</idno></msIdentifier><physDesc><scriptDesc><scriptNote script="Cursiva"/></scriptDesc></physDesc><history><origin><date when="1410"/></origin></history></msDesc></witness></listWit></body></text></group></text></TEI>'''
    words = '''<?xml version="1.0"?><!DOCTYPE TEI [<!ENTITY % abbr SYSTEM "../abbreviations.dtd"> %abbr;]><TEI xmlns="http://www.tei-c.org/ns/1.0"><text><group><text n="1"><body><p><lb/><w>&foo;</w></p></body></text></group></text></TEI>'''
    (base / "mss-dates.xml").write_text(meta, encoding="utf-8")
    (base / "texts" / "mss-dates-w.xml").write_text(words, encoding="utf-8")
    r = inventory(base / "mss-dates.xml", base / "texts" / "mss-dates-w.xml")
    assert r["eligible_manuscript_count"] == 1
    assert r["eligible_roster"][0]["earliest"] == 1410
    assert r["effect_statistics_computed"] is False
    print("SYNTHETIC_METADATA_PREFLIGHT_OK")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("metadata", nargs="?", type=Path)
    ap.add_argument("words", nargs="?", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--synthetic-preflight", action="store_true")
    args = ap.parse_args()
    if args.synthetic_preflight:
        synthetic_preflight()
        return
    if args.metadata is None or args.words is None:
        ap.error("metadata and words are required unless --synthetic-preflight")
    r = inventory(args.metadata, args.words)
    text = json.dumps(r, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
