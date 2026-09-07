#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from lxml import etree

NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def lname(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) and "}" in tag else (tag if isinstance(tag, str) else "")


def parse(path: Path):
    return etree.parse(str(path), etree.XMLParser(load_dtd=True, resolve_entities=True, no_network=True, recover=False, huge_tree=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", type=Path)
    ap.add_argument("roster", type=Path)
    args = ap.parse_args()

    roster = json.load(open(args.roster, encoding="utf-8"))["eligible_roster"]
    selected = {int(r["ordinal_1based"]): r for r in roster}
    tree = parse(args.words)
    teis = tree.xpath("/tei:teiCorpus/tei:TEI", namespaces=NS)

    docs = []
    global_lb_break = Counter()
    global_w_child_signatures = Counter()
    global_choice_parent_signatures = Counter()
    for ordinal, tei in enumerate(teis, 1):
        if ordinal not in selected:
            continue
        text = tei.xpath("./tei:text", namespaces=NS)[0]
        lbs = text.xpath(".//tei:lb", namespaces=NS)
        ws = text.xpath(".//tei:w", namespaces=NS)
        choices = text.xpath(".//tei:choice[tei:abbr and tei:expan]", namespaces=NS)
        lb_break = Counter((lb.get("break") or "<none>") for lb in lbs)
        global_lb_break.update(lb_break)
        sigs = Counter()
        for w in ws:
            sig = "/".join(lname(c.tag) for c in w if isinstance(c.tag, str)) or "<text-only>"
            sigs[sig] += 1
            global_w_child_signatures[sig] += 1
        choice_parents = Counter()
        for c in choices:
            p = c.getparent()
            gp = p.getparent() if p is not None else None
            sig = f"{lname(p.tag) if p is not None else '<none>'}/{lname(gp.tag) if gp is not None else '<none>'}"
            choice_parents[sig] += 1
            global_choice_parent_signatures[sig] += 1
        docs.append({
            "ordinal_1based": ordinal,
            "text_n": selected[ordinal]["text_n"],
            "idno": selected[ordinal]["idno"],
            "lb_count": len(lbs),
            "lb_break_values": dict(sorted(lb_break.items())),
            "w_count": len(ws),
            "w_with_descendant_lb": sum(bool(w.xpath(".//tei:lb", namespaces=NS)) for w in ws),
            "valid_choice_count": len(choices),
            "choice_parent_patterns": dict(choice_parents),
            "top_w_child_signatures": sigs.most_common(10),
        })

    out = {
        "audit": "ORIFLAMMS E1 structure-only parser audit after roster freeze",
        "effect_statistic_computed": False,
        "selected_document_count": len(docs),
        "global_lb_break_values": dict(sorted(global_lb_break.items())),
        "global_w_child_signatures": global_w_child_signatures.most_common(20),
        "global_choice_parent_signatures": dict(global_choice_parent_signatures),
        "documents": docs,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
