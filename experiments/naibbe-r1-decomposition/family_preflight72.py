#!/usr/bin/env python3
"""Issue #72 family-support preflight.

Constructs every preregistered counterfactual realization and freezes support /
surface identities before target scorer code exists. No real R1 pair or residual
quantity is computed.
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Dict, Sequence

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("phase62", "phase64", "issue26-music", "naibbe-r1-decomposition"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as b  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402
import source_audit72 as s  # noqa: E402

PARENT_MAIN = "ce49de68a3bd308b9432f5904b5368fc4c6f9c8f"
EXPECTED_CREMMA = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_NAIBBE = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
SUPPORT_GATE = 0.60
MANUSCRIPTS = tuple(n64.MANUSCRIPTS)
PRIMARY_SEEDS = tuple(6480000 + 100 * i for i in range(len(MANUSCRIPTS)))
ALLOWED_AXES = set("PLSTGI")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_seed(label: str) -> int:
    return s.stable_seed(label)


def canonical_items_payload(items: Sequence[b.Item]) -> bytes:
    return s.canonical_items_payload(items)


def surface_sha(items: Sequence[b.Item]) -> str:
    return s.surface_sha(items)


def parser_support(items: Sequence[b.Item], parser: e.SlotParser) -> dict:
    return s.parser_support(items, parser)


def pooled(items_by_manuscript: dict):
    return [it for m in MANUSCRIPTS for it in items_by_manuscript[m]]


def original_sources(cremma_root: Path):
    return {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }


def published_surfaces(module, sources, original_map):
    out, diags = {}, {}
    for mi, m in enumerate(MANUSCRIPTS):
        primary, _raw, diag = n64.encrypt_manuscript(module, sources[m], m, original_map, PRIMARY_SEEDS[mi])
        out[m] = primary
        diags[m] = diag
    return out, diags


def generate_with_map(module, sources, glyph_map, parser, axis: str, rid: str, invariant: dict):
    by_m, diags = {}, {}
    for mi, m in enumerate(MANUSCRIPTS):
        primary, _raw, diag = n64.encrypt_manuscript(module, sources[m], m, glyph_map, PRIMARY_SEEDS[mi])
        by_m[m] = primary
        diags[m] = diag
    pp = pooled(by_m)
    return {
        "axis": axis,
        "realization": rid,
        "surface_sha256": surface_sha(pp),
        "support": parser_support(pp, parser),
        "generation_completed": True,
        "ambiguity_retries_by_manuscript": {m: int(diags[m]["ambiguity_retries"]) for m in MANUSCRIPTS},
        "primary_cipher_tokens_by_manuscript": {m: int(diags[m]["primary_cipher_tokens"]) for m in MANUSCRIPTS},
        "map_sha256": s.map_sha(glyph_map),
        "invariants": invariant,
    }, by_m


def p_source_items(module, items: Sequence[b.Item], manuscript: str, r: int):
    out=[]; checked=0
    for it in items:
        lines=[]
        for li,line in enumerate(it.lines):
            eff=s.source_line_effective(module,line)
            chars=list(eff); shuffled=list(chars)
            if r == 0:
                label=f"issue72:P:pilot0:{manuscript}:{it.item_id}:{li}"
            else:
                label=f"issue72:P:family:{r}:{manuscript}:{it.item_id}:{li}"
            random.Random(stable_seed(label)).shuffle(shuffled)
            if len(shuffled)!=len(chars) or collections.Counter(shuffled)!=collections.Counter(chars):
                raise RuntimeError(f"P{r} line invariant failed")
            checked += 1
            lines.append([tuple("".join(shuffled))] if shuffled else [])
        out.append(b.Item(item_id=it.item_id,document=it.document,lines=lines,leaf=it.leaf))
    return out, checked


def generate_P(module, sources, original_map, parser, r: int):
    transformed={}; checked={}
    for m in MANUSCRIPTS:
        transformed[m],checked[m]=p_source_items(module,sources[m],m,r)
    return generate_with_map(module,transformed,original_map,parser,"P",f"P{r}",{
        "per_line_length_and_character_multiset_preserved": True,
        "lines_checked_by_manuscript": checked,
    })


def derangement(items, label):
    return s.derangement(items,label)


def map_L(module, original, r: int):
    label = "issue72:L:pilot0:global-effective-letter-permutation" if r==0 else f"issue72:L:family:{r}:global-effective-letter-permutation"
    perm=derangement(n64.EFFECTIVE_LETTERS,label)
    out=dict(original)
    for state in module.STATES:
        for table in module.TABLES:
            before=[]; after=[]
            for letter in n64.EFFECTIVE_LETTERS:
                code=f"{state}_{table}_{letter}"
                src=f"{state}_{table}_{perm[letter]}"
                before.append(original[code]); out[code]=original[src]; after.append(out[code])
            if collections.Counter(before)!=collections.Counter(after):
                raise RuntimeError(f"L{r} table-state invariant failed")
    return out,{"label":label,"effective_letter_permutation":perm,"fixed_points":sum(k==v for k,v in perm.items()),"table_state_effective_value_multisets_preserved":True}


def map_S(module, original, shift: int):
    states=list(module.STATES); out=dict(original)
    for table in module.TABLES:
        for letter in n64.EFFECTIVE_LETTERS:
            before=[original[f"{st}_{table}_{letter}"] for st in states]
            for i,st in enumerate(states):
                source_state=states[(i-shift)%len(states)]
                out[f"{st}_{table}_{letter}"]=original[f"{source_state}_{table}_{letter}"]
            after=[out[f"{st}_{table}_{letter}"] for st in states]
            if collections.Counter(before)!=collections.Counter(after):
                raise RuntimeError(f"S shift {shift} invariant failed")
    return out,{"state_rotation_shift":shift,"table_letter_three_value_multisets_preserved":True}


def map_T(module, original, shift: int):
    tables=list(module.TABLES); out=dict(original)
    for state in module.STATES:
        for letter in n64.EFFECTIVE_LETTERS:
            before=[original[f"{state}_{t}_{letter}"] for t in tables]
            for i,t in enumerate(tables):
                dest=tables[(i+shift)%len(tables)]
                out[f"{state}_{dest}_{letter}"]=original[f"{state}_{t}_{letter}"]
            after=[out[f"{state}_{t}_{letter}"] for t in tables]
            if collections.Counter(before)!=collections.Counter(after):
                raise RuntimeError(f"T shift {shift} invariant failed")
    return out,{"table_rotation_shift":shift,"state_letter_six_value_multisets_preserved":True,"published_table_weights_unchanged":True}


def map_G(module, original, r: int):
    label="issue72:G:pilot0:global-effective-cell-permutation" if r==0 else f"issue72:G:family:{r}:global-effective-cell-permutation"
    keys=[f"{state}_{table}_{letter}" for state in module.STATES for table in module.TABLES for letter in n64.EFFECTIVE_LETTERS]
    values=[original[k] for k in keys]; shuffled=list(values)
    random.Random(stable_seed(label)).shuffle(shuffled)
    out=dict(original)
    for k,v in zip(keys,shuffled): out[k]=v
    if collections.Counter(values)!=collections.Counter(out[k] for k in keys):
        raise RuntimeError(f"G{r} global cell invariant failed")
    return out,{"label":label,"effective_cell_instances":len(keys),"global_effective_value_multiset_preserved":True,"duplicate_values_permuted_as_cell_instances":True}


def permute_inventory(published_by_m: dict, r: int):
    label="issue72:I:pilot0:published-primary-token-instance-permutation" if r==0 else f"issue72:I:family:{r}:published-primary-token-instance-permutation"
    flat=[]; skeleton=[]
    for m in MANUSCRIPTS:
        for it in published_by_m[m]:
            lens=[]
            for line in it.lines:
                lens.append(len(line)); flat.extend(tuple(tok) for tok in line)
            skeleton.append((m,it,lens))
    before=collections.Counter("".join(tok) for tok in flat)
    shuffled=list(flat); random.Random(stable_seed(label)).shuffle(shuffled); cursor=0
    out={m:[] for m in MANUSCRIPTS}
    for m,src,lens in skeleton:
        lines=[]
        for n in lens:
            line=[tuple(shuffled[cursor+i]) for i in range(n)]; cursor+=n; lines.append(line)
        out[m].append(b.Item(item_id=src.item_id,document=src.document,lines=lines,leaf=src.leaf))
    if cursor!=len(shuffled): raise RuntimeError(f"I{r} cursor mismatch")
    after=collections.Counter("".join(tok) for m in MANUSCRIPTS for it in out[m] for line in it.lines for tok in line)
    if before!=after: raise RuntimeError(f"I{r} token multiset invariant failed")
    return out,{"label":label,"token_instances":len(flat),"distinct_token_types":len(before),"exact_global_whole_token_multiset_preserved":True,"exact_item_line_token_count_layout_preserved":True}


def load_stageA():
    root=HERE.parent/"source-audit"
    p=root/"source_audit.json"
    if not p.exists(): raise RuntimeError("permanent Stage A source audit missing")
    r=json.loads(p.read_text(encoding="utf-8"))
    if r["counterfactual_R1_scored"] is not False or any(r["forbidden_quantities_computed"].values()):
        raise RuntimeError("Stage A target firewall not clean")
    axes_file=root/"TARGET_ELIGIBLE_AXES.txt"
    if not axes_file.exists(): raise RuntimeError("Stage A eligible-axis file missing")
    raw=[x.strip() for x in axes_file.read_text(encoding="utf-8").splitlines() if x.strip()]
    axes=[]
    for x in raw:
        axis=x[0]
        if axis not in ALLOWED_AXES: raise RuntimeError(f"unexpected Stage A axis label {x!r}")
        axes.append(axis)
    if len(set(axes))!=len(axes): raise RuntimeError("duplicate Stage A eligible axis")
    return r,axes,sha256_file(p)


def main(cremma_root: Path, naibbe_root: Path):
    stageA,stageA_axes,stageA_sha=load_stageA()
    if b.verify_cremma_commit(cremma_root)!=EXPECTED_CREMMA: raise RuntimeError("CREMMA authority mismatch")
    module=n64.load_naibbe(naibbe_root)
    if s.git_blob((naibbe_root/"naibbe_v2.py").read_bytes())!=s.EXPECTED_ENCODER_BLOB: raise RuntimeError("Naibbe encoder blob mismatch")
    if s.git_blob((naibbe_root/"references"/"naibbe_tables.csv").read_bytes())!=s.EXPECTED_TABLE_BLOB: raise RuntimeError("Naibbe table blob mismatch")

    parser=e.SlotParser(); parser_validation=e.validate_parser(parser)
    sources={name:b.parse_latin_manuscript(cremma_root,name,rel) for name,rel in b.PRIMARY_MANUSCRIPTS.items()}
    original_map=dict(module.placeholder_to_glyph)
    published_by_m,published_diags=published_surfaces(module,sources,original_map)
    published_pool=pooled(published_by_m)
    if surface_sha(published_pool)!=s.EXPECTED_POOLED_SHA: raise RuntimeError("published pooled surface changed")

    records=[]
    r0_stageA={k:v for k,v in stageA["support_pilots"].items()}

    def add(record):
        axis=record["axis"]
        if record["realization"] in {"P0","L0","S1","T1","G0","I0"}:
            key={"P0":"P0","L0":"L0","S1":"S0","T1":"T0","G0":"G0","I0":"I0"}[record["realization"]]
            if axis in stageA_axes:
                expected=r0_stageA[key]
                if record["surface_sha256"]!=expected["surface_sha256"]:
                    raise RuntimeError(f"{record['realization']} Stage A surface SHA mismatch")
                if record["support"]!=expected["support"]:
                    raise RuntimeError(f"{record['realization']} Stage A support mismatch")
        records.append(record)

    if "P" in stageA_axes:
        for r in range(5):
            rec,_=generate_P(module,sources,original_map,parser,r); add(rec)
    if "L" in stageA_axes:
        for r in range(5):
            mp,inv=map_L(module,original_map,r); rec,_=generate_with_map(module,sources,mp,parser,"L",f"L{r}",inv); add(rec)
    if "S" in stageA_axes:
        for shift in (1,2):
            mp,inv=map_S(module,original_map,shift); rec,_=generate_with_map(module,sources,mp,parser,"S",f"S{shift}",inv); add(rec)
    if "T" in stageA_axes:
        for shift in (1,2,3,4,5):
            mp,inv=map_T(module,original_map,shift); rec,_=generate_with_map(module,sources,mp,parser,"T",f"T{shift}",inv); add(rec)
    if "G" in stageA_axes:
        for r in range(5):
            mp,inv=map_G(module,original_map,r); rec,_=generate_with_map(module,sources,mp,parser,"G",f"G{r}",inv); add(rec)
    if "I" in stageA_axes:
        for r in range(5):
            by_m,inv=permute_inventory(published_by_m,r); pp=pooled(by_m)
            add({"axis":"I","realization":f"I{r}","surface_sha256":surface_sha(pp),"support":parser_support(pp,parser),"generation_completed":True,"ambiguity_retries_by_manuscript":None,"primary_cipher_tokens_by_manuscript":None,"map_sha256":None,"invariants":inv})

    by_axis={a:[] for a in stageA_axes}
    for rec in records: by_axis[rec["axis"]].append(rec)
    expected_n={"P":5,"L":5,"S":2,"T":5,"G":5,"I":5}
    axis_status={}
    authorized=[]
    for axis in stageA_axes:
        rr=by_axis[axis]
        if len(rr)!=expected_n[axis]: raise RuntimeError(f"axis {axis} realization count mismatch")
        all_ok=all(x["generation_completed"] and x["support"]["coverage"]>=SUPPORT_GATE for x in rr)
        axis_status[axis]={"planned_realizations":expected_n[axis],"all_realizations_support_eligible":all_ok,"min_coverage":min(x["support"]["coverage"] for x in rr),"max_coverage":max(x["support"]["coverage"] for x in rr),"realization_ids":[x["realization"] for x in rr]}
        if all_ok: authorized.append(axis)

    result={
        "phase":"Issue72-family-support-preflight",
        "parent_main":PARENT_MAIN,
        "counterfactual_R1_scored":False,
        "forbidden_quantities_computed":{"pair_Q":False,"residual_Z":False,"residual_energy":False,"residual_reliability":False,"target_topology":False,"R1_p_values":False,"per_edge_differences":False},
        "StageA_machine_audit_sha256":stageA_sha,
        "StageA_support_eligible_axes":stageA_axes,
        "parser":{"policy":"min","support_gate":SUPPORT_GATE,"validation":parser_validation},
        "published_primary":{"surface_sha256":surface_sha(published_pool),"support":parser_support(published_pool,parser),"ambiguity_retries_by_manuscript":{m:int(published_diags[m]["ambiguity_retries"]) for m in MANUSCRIPTS}},
        "realizations":records,
        "axis_support_status":axis_status,
        "target_authorized_axes":authorized,
        "target_authorized_realizations":[x["realization"] for x in records if x["axis"] in authorized],
        "target_scored_family_frozen":True,
    }
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit(f"usage: {sys.argv[0]} CREMMA_ROOT NAIBBE_ROOT")
    main(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
