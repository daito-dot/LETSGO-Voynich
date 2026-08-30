#!/usr/bin/env python3
"""Phase 56A canonical multiscale state-matrix builder.

Preserves page-side and physical-leaf identities separately. Input is the local
ZL3b/EVA-derived working transcription; see data/README.md for provenance.

This is intentionally a substrate builder rather than a mechanism model.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

COMPOSITES = ("cth", "ckh", "cph", "cfh", "iin", "ch", "sh", "in", "ee")
LOC_RE = re.compile(r"^<f(?P<leaf>\d+)(?P<side>[rv])(?P<rest>[^>]*)>")


def collapse_token(token: str) -> tuple[str, ...]:
    out, i = [], 0
    while i < len(token):
        for c in COMPOSITES:
            if token.startswith(c, i):
                out.append(c); i += len(c); break
        else:
            if token[i].isalpha(): out.append(token[i])
            i += 1
    return tuple(out)


def edit1(a: tuple[str, ...], b: tuple[str, ...]) -> bool:
    la, lb = len(a), len(b)
    if abs(la-lb) > 1: return False
    if la == lb: return sum(x != y for x,y in zip(a,b)) == 1
    if la > lb: a,b,la,lb = b,a,lb,la
    i=j=diff=0
    while i < la and j < lb:
        if a[i] == b[j]: i+=1; j+=1
        else:
            diff += 1; j += 1
            if diff > 1: return False
    return True


def entropy(c: Counter) -> float:
    n=sum(c.values())
    return -sum((v/n)*math.log2(v/n) for v in c.values() if v) if n else 0.0


def summarize(tokens: list[str]) -> dict:
    units=[collapse_token(t) for t in tokens]
    lens=[len(u) for u in units]
    types=list(set(units))
    near=sum(any(edit1(a,b) for b in types if b != a) for a in types) / len(types) if types else 0.0
    initials=Counter(u[0] for u in units if u)
    finals=Counter(u[-1] for u in units if u)
    flat=Counter(x for u in units for x in u)
    kt=sum(x in {"k","t"} for u in units for x in u)
    k=sum(x == "k" for u in units for x in u)
    return {
        "n_tokens":len(tokens), "n_types":len(set(tokens)),
        "type_token_ratio":len(set(tokens))/len(tokens) if tokens else 0.0,
        "mean_unit_len":mean(lens) if lens else 0.0,
        "median_unit_len":median(lens) if lens else 0.0,
        "unit_inventory":len(flat), "unit_entropy":entropy(flat),
        "initial_entropy":entropy(initials), "final_entropy":entropy(finals),
        "edit1_type_coverage":near,
        "kt_mass":kt/sum(flat.values()) if flat else 0.0,
        "k_share_within_kt":k/kt if kt else 0.0,
    }


def parse(path: Path):
    meta={}
    rows=[]
    current_section=current_currier=current_hand="?"
    paragraph_counter=defaultdict(int)
    for raw in path.read_text(errors="replace").splitlines():
        if raw.startswith("#=IVTFF") or not raw: continue
        # ZL3b metadata lines vary by release; retain recognized $I/$L/$H fields.
        if raw.startswith("#"):
            for key, var in (("$I","section"),("$L","currier"),("$H","hand")):
                m=re.search(re.escape(key)+r"\s*=\s*([^;#]+)", raw)
                if m: meta[var]=m.group(1).strip()
            current_section=meta.get("section",current_section)
            current_currier=meta.get("currier",current_currier)
            current_hand=meta.get("hand",current_hand)
            continue
        m=LOC_RE.match(raw)
        if not m: continue
        leaf=int(m.group("leaf")); side=m.group("side"); rest=m.group("rest")
        page=f"f{leaf}{side}"
        text=raw.split(">",1)[1] if ">" in raw else ""
        # Paragraph start is explicitly encoded by <%> in the working transcription.
        para_start="<%>" in text or ",P" in rest
        if para_start: paragraph_counter[page]+=1
        para=paragraph_counter[page]
        clean=re.sub(r"<[^>]+>"," ",text)
        toks=[t for t in re.findall(r"[a-z]+", clean.lower()) if t]
        if not toks: continue
        rows.append({"page_side":page,"physical_leaf":leaf,"side":side,
                     "section":current_section,"currier":current_currier,"hand":current_hand,
                     "paragraph_id":para,"locator":rest,"paragraph_start":int(para_start),"tokens":toks})
    return rows


def aggregate(rows, keys):
    g=defaultdict(list)
    for r in rows: g[tuple(r[k] for k in keys)].append(r)
    out=[]
    for key, rr in g.items():
        toks=[t for r in rr for t in r["tokens"]]
        d={k:v for k,v in zip(keys,key)}; d.update(summarize(toks)); d["n_lines"]=len(rr)
        out.append(d)
    return out


def write_csv(path, rows):
    if not rows: return
    cols=list(rows[0])
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("transcription"); ap.add_argument("--out",default="phase56_state")
    a=ap.parse_args(); rows=parse(Path(a.transcription)); stem=Path(a.out)
    page=aggregate(rows,["page_side","physical_leaf","side","section","currier","hand"])
    para=aggregate(rows,["page_side","physical_leaf","side","section","currier","hand","paragraph_id"])
    line=[]
    for i,r in enumerate(rows):
        d={k:r[k] for k in ("page_side","physical_leaf","side","section","currier","hand","paragraph_id","paragraph_start")}
        d["line_serial"]=i; d.update(summarize(r["tokens"])); line.append(d)
    write_csv(str(stem)+"_page.csv",page); write_csv(str(stem)+"_paragraph.csv",para); write_csv(str(stem)+"_line.csv",line)
    summary={"schema_version":"56A-v1","n_source_lines":len(rows),"n_page_sides":len(page),"n_paragraph_groups":len(para),"n_line_rows":len(line),
             "page_sections":dict(Counter(str(r["section"]) for r in page)),"page_currier":dict(Counter(str(r["currier"]) for r in page)),"page_hands":dict(Counter(str(r["hand"]) for r in page))}
    Path(str(stem)+"_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__ == "__main__": main()
