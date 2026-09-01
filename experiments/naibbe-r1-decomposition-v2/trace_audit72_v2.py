#!/usr/bin/env python3
"""Issue #72 V2 Stage-A trace causal-identification audit.

This executable is intentionally target-blind. It reproduces the exact published
Naibbe realization-0 surfaces, records the realized encryption path, proves that
a trace-only renderer reconstructs the same surface, and audits mechanically
interpretable counterfactual interfaces.

It MUST NOT compute any slot-pair association, residual graph, R1 topology,
or target comparison.

Usage:
    python experiments/naibbe-r1-decomposition-v2/trace_audit72_v2.py \
        /path/to/CREMMA-Medieval-LAT /path/to/naibbe-cipher /tmp/issue72v2
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("phase62", "phase64", "issue26-music"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as b  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402

PARENT_MAIN = "98a04953aabe9e228a17fa5808adf506a0833362"
EXPECTED_NAIBBE = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
EXPECTED_ENCODER_BLOB = "b566ad82e4b6ff0782ecdddebf77718dac44f292"
EXPECTED_TABLE_BLOB = "5cd34fb81d80faf3b4d57dbf1719c05ffde25302"
EXPECTED_DECODER_BLOB = "b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b"
EXPECTED_CREMMA = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_PRIMARY_SURFACE_SHA = {
    "BIS193": "fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805",
    "CLM13027": "da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77",
    "Mazarine915": "2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d",
    "UBL758": "5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89",
}
EXPECTED_POOLED_PRIMARY_SHA = "47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd"
TRACE_SCHEMA = "issue72-v2-naibbe-accepted-event-trace-v1"
MANUSCRIPTS = tuple(n64.MANUSCRIPTS)
EFFECTIVE_LETTERS = tuple(n64.EFFECTIVE_LETTERS)
TABLES = ("alpha", "beta1", "beta2", "beta3", "gamma1", "gamma2")
STATES = ("unigram", "prefix", "suffix")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def verify_git_head(root: Path, expected: str, label: str) -> str:
    got = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if got != expected:
        raise RuntimeError(f"{label} commit mismatch: {got} != {expected}")
    return got


def stable_seed(label: str) -> int:
    d = hashlib.sha256(label.encode("utf-8")).digest()
    return int.from_bytes(d[:8], "big") % (2**31 - 1)


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def item_payload(items: Sequence[b.Item]) -> list:
    return [
        {
            "item_id": it.item_id,
            "document": it.document,
            "leaf": it.leaf,
            "lines": [["".join(tok) for tok in line] for line in it.lines],
        }
        for it in items
    ]


def canonical_items_bytes(items: Sequence[b.Item]) -> bytes:
    return canonical_json_bytes(item_payload(items))


def surface_sha(items: Sequence[b.Item]) -> str:
    return sha256_bytes(canonical_items_bytes(items))


def token_text(tok) -> str:
    return "".join(tok)


def glyph_line(tokens: Sequence[str]) -> b.Line:
    return [tuple(x) for x in tokens if x]


def parser_support(items: Sequence[b.Item], parser: e.SlotParser) -> dict:
    visible = accepted = 0
    by_doc = collections.Counter()
    by_doc_ok = collections.Counter()
    for it in items:
        for line in it.lines:
            for tok_units in line:
                tok = token_text(tok_units)
                if not tok:
                    continue
                visible += 1
                by_doc[it.document] += 1
                if parser.pick(tok, "min") is not None:
                    accepted += 1
                    by_doc_ok[it.document] += 1
    return {
        "visible_tokens": int(visible),
        "accepted_tokens": int(accepted),
        "coverage": float(accepted / visible) if visible else 0.0,
        "stage_a_role": "DESCRIPTIVE_INTERFACE_SUPPORT_ONLY_NO_HARD_CUTOFF",
        "by_document": {
            doc: {
                "visible": int(by_doc[doc]),
                "accepted": int(by_doc_ok[doc]),
                "coverage": float(by_doc_ok[doc] / by_doc[doc]) if by_doc[doc] else 0.0,
            }
            for doc in sorted(by_doc)
        },
    }


def code_key(state: str, table: str, letter: str) -> str:
    return f"{state}_{table}_{letter}"


def effective_cells() -> List[str]:
    return [code_key(s, t, l) for s in STATES for t in TABLES for l in EFFECTIVE_LETTERS]


def full_modified_map(original: Mapping[str, str], replacements: Mapping[str, str]) -> Dict[str, str]:
    out = dict(original)
    out.update(replacements)
    if set(out) != set(original):
        raise RuntimeError("modified map key set changed")
    return out


def letter_rotation_map() -> Dict[str, str]:
    xs = list(EFFECTIVE_LETTERS)
    out = {x: xs[(i + 1) % len(xs)] for i, x in enumerate(xs)}
    if any(k == v for k, v in out.items()):
        raise RuntimeError("EL pilot unexpectedly contains fixed point")
    return out


def state_rotation_map() -> Dict[str, str]:
    return {s: STATES[(i + 1) % len(STATES)] for i, s in enumerate(STATES)}


def table_rotation_map() -> Dict[str, str]:
    return {t: TABLES[(i + 1) % len(TABLES)] for i, t in enumerate(TABLES)}


def mapping_el(original: Mapping[str, str]) -> Tuple[Dict[str, str], dict]:
    pi = letter_rotation_map()
    repl = {}
    for s in STATES:
        for t in TABLES:
            for l in EFFECTIVE_LETTERS:
                repl[code_key(s, t, l)] = original[code_key(s, t, pi[l])]
    return full_modified_map(original, repl), {
        "kind": "EL",
        "definition": "fixed-path effective-letter +1 cyclic reassignment within each state/table",
        "letter_permutation": pi,
        "reachable_value_multiset_preserved_per_state_table": True,
    }


def mapping_es(original: Mapping[str, str]) -> Tuple[Dict[str, str], dict]:
    pi = state_rotation_map()
    repl = {}
    for s in STATES:
        for t in TABLES:
            for l in EFFECTIVE_LETTERS:
                repl[code_key(s, t, l)] = original[code_key(pi[s], t, l)]
    return full_modified_map(original, repl), {
        "kind": "ES",
        "definition": "fixed-path state-value +1 cyclic reassignment within each table/letter",
        "state_permutation": pi,
        "reachable_value_multiset_preserved_per_table_letter": True,
    }


def mapping_et(original: Mapping[str, str]) -> Tuple[Dict[str, str], dict]:
    pi = table_rotation_map()
    repl = {}
    for s in STATES:
        for t in TABLES:
            for l in EFFECTIVE_LETTERS:
                repl[code_key(s, t, l)] = original[code_key(s, pi[t], l)]
    return full_modified_map(original, repl), {
        "kind": "ET",
        "definition": "fixed-path table-value +1 cyclic reassignment within each state/letter",
        "table_permutation": pi,
        "reachable_value_multiset_preserved_per_state_letter": True,
    }


def mapping_eg(original: Mapping[str, str]) -> Tuple[Dict[str, str], dict]:
    cells = effective_cells()
    vals = [original[c] for c in cells]
    shuffled = list(vals)
    rng = random.Random(stable_seed("issue72-v2:EG:pilot0:effective-cell-values"))
    rng.shuffle(shuffled)
    repl = dict(zip(cells, shuffled))
    if collections.Counter(repl.values()) != collections.Counter(vals):
        raise RuntimeError("EG global effective value multiset invariant failed")
    return full_modified_map(original, repl), {
        "kind": "EG",
        "definition": "fixed-path global permutation of 414 effective reachable cell-value instances",
        "permutation_seed": stable_seed("issue72-v2:EG:pilot0:effective-cell-values"),
        "global_effective_value_multiset_preserved": True,
    }


def trace_bigram_legality(module, glyph_map: Mapping[str, str], traces_by_ms: Mapping[str, dict]) -> dict:
    unigram_glyphs = {
        glyph for code, glyph in glyph_map.items() if code.startswith("unigram_")
    }
    catalog = module.build_bigram_catalog(module.ALPHABET, module.TABLES, glyph_map)
    total = admissible = uni_collision = cross_collision = 0
    for msrow in traces_by_ms.values():
        for item in msrow["items"]:
            for line in item["lines"]:
                for ev in line["events"]:
                    if ev["kind"] != "bigram":
                        continue
                    total += 1
                    p = ev["cells"][0]
                    s = ev["cells"][1]
                    pg = glyph_map[p["code"]]
                    sg = glyph_map[s["code"]]
                    combined = pg + sg
                    if combined in unigram_glyphs:
                        uni_collision += 1
                        continue
                    pairs = catalog.get(combined, set())
                    pair = (p["code"], s["code"])
                    if any(x != pair for x in pairs):
                        cross_collision += 1
                        continue
                    admissible += 1
    return {
        "bigram_events": int(total),
        "admissible_under_modified_full_codebook": int(admissible),
        "admissible_fraction": float(admissible / total) if total else None,
        "unigram_collision": int(uni_collision),
        "alternative_bigram_collision": int(cross_collision),
        "role": "DIAGNOSTIC_ONLY_NOT_A_REPAIR_OR_ELIGIBILITY_GATE",
    }


def trace_encrypt_manuscript(
    module,
    source_items: Sequence[b.Item],
    manuscript: str,
    glyph_map: Mapping[str, str],
    seed: int,
    plaintext_transform: Callable[[str, str, int], str] | None = None,
) -> Tuple[List[b.Item], List[b.Item], dict, dict]:
    """Literal instrumented replay of the published encryption call order."""
    random.seed(seed)
    traces = {
        "schema": TRACE_SCHEMA,
        "manuscript": manuscript,
        "seed": seed,
        "items": [],
    }
    primary_items: List[b.Item] = []
    raw_items: List[b.Item] = []
    total_retries = 0
    transformed_lines = 0

    unigram_glyphs = {
        glyph for code, glyph in glyph_map.items() if code.startswith("unigram_")
    }
    catalog = module.build_bigram_catalog(module.ALPHABET, module.TABLES, glyph_map)

    for item in source_items:
        trace_item = {"item_id": item.item_id, "leaf": item.leaf, "lines": []}
        p_lines: List[b.Line] = []
        r_lines: List[b.Line] = []
        for li, line in enumerate(item.lines):
            source = n64.string_line(line)
            published_cleaned = module.clean_line(source)
            cleaned, dropped = n64.project_effective_plaintext(published_cleaned)
            before_transform = cleaned
            if plaintext_transform is not None and cleaned:
                cleaned = plaintext_transform(cleaned, item.item_id, li)
                transformed_lines += int(cleaned != before_transform)

            line_trace = {
                "line_index": li,
                "source_effective_sha256": sha256_bytes(before_transform.encode("utf-8")),
                "source_effective_length": len(before_transform),
                "effective_plaintext": cleaned,
                "unsupported_dropped": dropped,
                "events": [],
                "join_mask_removed": [],
                "deck_count": 0,
                "cards_consumed": 0,
            }

            if not cleaned:
                p_lines.append([])
                r_lines.append([])
                trace_item["lines"].append(line_trace)
                continue

            # Exact respace_plaintext semantics with trace.
            units = []
            i = 0
            while i < len(cleaned):
                if i == len(cleaned) - 1 or random.random() < (module.RESPACING / 36):
                    units.append((i, i + 1, cleaned[i]))
                    i += 1
                else:
                    units.append((i, i + 2, cleaned[i:i + 2]))
                    i += 2

            deck = module.create_card_deck(module.USE_78_CARD_DECK)
            deck_index = 0
            deck_generation = 0
            line_trace["deck_count"] = 1

            def draw_card() -> Tuple[str, int, int]:
                nonlocal deck, deck_index, deck_generation
                if deck_index >= len(deck):
                    deck = module.create_card_deck(module.USE_78_CARD_DECK)
                    deck_index = 0
                    deck_generation += 1
                    line_trace["deck_count"] += 1
                pos = deck_index
                table = deck[deck_index]
                deck_index += 1
                line_trace["cards_consumed"] += 1
                return table, deck_generation, pos

            encrypted: List[str] = []
            for ev_index, (start, end, unit) in enumerate(units):
                if len(unit) == 1:
                    table, dg, dp = draw_card()
                    code = module.naibbe_tables[table][("unigram", unit[0])]
                    glyph = glyph_map.get(code, code)
                    encrypted.append(glyph)
                    line_trace["events"].append({
                        "event_index": ev_index,
                        "kind": "unigram",
                        "source_span": [start, end],
                        "plaintext": unit,
                        "cells": [{
                            "state": "unigram",
                            "table": table,
                            "letter": unit[0],
                            "code": code,
                            "glyph": glyph,
                            "deck_generation": dg,
                            "deck_position": dp,
                        }],
                        "rejected_attempts": [],
                        "retry_count": 0,
                        "forced_after_retry_exhaustion": False,
                        "emitted": glyph,
                    })
                    continue

                rejected = []
                accepted_cells = None
                emitted = None
                forced = False
                for _attempt in range(module.MAX_BIGRAM_RETRIES):
                    tp, dgp, dpp = draw_card()
                    cp = module.naibbe_tables[tp][("prefix", unit[0])]
                    gp = glyph_map.get(cp, cp)
                    ts, dgs, dps = draw_card()
                    cs = module.naibbe_tables[ts][("suffix", unit[1])]
                    gs = glyph_map.get(cs, cs)
                    combined = gp + gs
                    cells = [
                        {
                            "state": "prefix", "table": tp, "letter": unit[0], "code": cp,
                            "glyph": gp, "deck_generation": dgp, "deck_position": dpp,
                        },
                        {
                            "state": "suffix", "table": ts, "letter": unit[1], "code": cs,
                            "glyph": gs, "deck_generation": dgs, "deck_position": dps,
                        },
                    ]
                    if combined in unigram_glyphs:
                        rejected.append({
                            "cells": cells,
                            "combined": combined,
                            "reason": "UNIGRAM_GLYPH_COLLISION",
                        })
                        total_retries += 1
                        continue
                    pairs = catalog.get(combined, set())
                    any_other = any(pair != (cp, cs) for pair in pairs)
                    if any_other:
                        rejected.append({
                            "cells": cells,
                            "combined": combined,
                            "reason": "ALTERNATIVE_BIGRAM_CODE_COLLISION",
                        })
                        total_retries += 1
                        continue
                    accepted_cells = cells
                    emitted = combined
                    break
                if accepted_cells is None:
                    # Match pinned implementation's safety-fuse behavior.
                    accepted_cells = cells
                    emitted = combined
                    forced = True
                encrypted.append(emitted)
                line_trace["events"].append({
                    "event_index": ev_index,
                    "kind": "bigram",
                    "source_span": [start, end],
                    "plaintext": unit,
                    "cells": accepted_cells,
                    "rejected_attempts": rejected,
                    "retry_count": len(rejected),
                    "forced_after_retry_exhaustion": forced,
                    "emitted": emitted,
                })

            # Exact published respace_line semantics while preserving boundary decisions.
            if len(encrypted) < 2:
                primary_tokens = list(encrypted)
                join_removed: List[bool] = []
            else:
                primary_tokens = [encrypted[0]]
                join_removed = []
                for tok in encrypted[1:]:
                    drop = random.random() < module.SPACE_REMOVAL_RATE
                    join_removed.append(bool(drop))
                    if drop:
                        primary_tokens[-1] += tok
                    else:
                        primary_tokens.append(tok)
            line_trace["join_mask_removed"] = join_removed
            line_trace["raw_tokens"] = encrypted
            line_trace["primary_tokens"] = primary_tokens
            r_lines.append(glyph_line(encrypted))
            p_lines.append(glyph_line(primary_tokens))
            trace_item["lines"].append(line_trace)

        raw_items.append(b.Item(item.item_id, manuscript, r_lines, None))
        primary_items.append(b.Item(item.item_id, manuscript, p_lines, None))
        traces["items"].append(trace_item)

    return primary_items, raw_items, traces, {
        "seed": seed,
        "ambiguity_retries": int(total_retries),
        "plaintext_transform_changed_lines": int(transformed_lines),
    }


def render_trace(
    trace: Mapping,
    glyph_map: Mapping[str, str],
) -> Tuple[List[b.Item], List[b.Item], dict]:
    primary: List[b.Item] = []
    raw: List[b.Item] = []
    changed_events = 0
    total_events = 0
    for item in trace["items"]:
        p_lines: List[b.Line] = []
        r_lines: List[b.Line] = []
        for line in item["lines"]:
            encrypted = []
            for ev in line["events"]:
                total_events += 1
                glyphs = [glyph_map[cell["code"]] for cell in ev["cells"]]
                emitted = "".join(glyphs)
                encrypted.append(emitted)
                changed_events += int(emitted != ev["emitted"])
            mask = line["join_mask_removed"]
            if len(encrypted) < 2:
                if mask:
                    raise RuntimeError("trace join mask exists for <2 tokens")
                primary_tokens = list(encrypted)
            else:
                if len(mask) != len(encrypted) - 1:
                    raise RuntimeError("trace join mask length mismatch")
                primary_tokens = [encrypted[0]]
                for drop, tok in zip(mask, encrypted[1:]):
                    if drop:
                        primary_tokens[-1] += tok
                    else:
                        primary_tokens.append(tok)
            r_lines.append(glyph_line(encrypted))
            p_lines.append(glyph_line(primary_tokens))
        raw.append(b.Item(item["item_id"], trace["manuscript"], r_lines, None))
        primary.append(b.Item(item["item_id"], trace["manuscript"], p_lines, None))
    return primary, raw, {
        "events": int(total_events),
        "changed_events": int(changed_events),
        "changed_event_fraction": float(changed_events / total_events) if total_events else 0.0,
        "fixed_path_fields_changed": 0,
    }


def pt_transform(manuscript: str) -> Callable[[str, str, int], str]:
    def transform(cleaned: str, item_id: str, line_index: int) -> str:
        chars = list(cleaned)
        out = list(chars)
        rng = random.Random(stable_seed(f"issue72-v2:PT:pilot0:{manuscript}:{item_id}:{line_index}"))
        rng.shuffle(out)
        if len(out) != len(chars) or collections.Counter(out) != collections.Counter(chars):
            raise RuntimeError("PT character-multiset invariant failed")
        return "".join(out)
    return transform


def fi_surface(published_by_ms: Mapping[str, Sequence[b.Item]]) -> Tuple[Dict[str, List[b.Item]], dict]:
    flat = []
    shapes = []
    before_counter = collections.Counter()
    for ms in MANUSCRIPTS:
        for it in published_by_ms[ms]:
            for li, line in enumerate(it.lines):
                vals = [token_text(tok) for tok in line]
                shapes.append((ms, it.item_id, it.leaf, li, len(vals)))
                flat.extend(vals)
                before_counter.update(vals)
    shuffled = list(flat)
    random.Random(stable_seed("issue72-v2:FI:pilot0:global-primary-token-instances")).shuffle(shuffled)
    cursor = 0
    lines_by_item: MutableMapping[Tuple[str, str, object], Dict[int, b.Line]] = collections.defaultdict(dict)
    for ms, item_id, leaf, li, n in shapes:
        vals = shuffled[cursor:cursor + n]
        cursor += n
        lines_by_item[(ms, item_id, leaf)][li] = glyph_line(vals)
    if cursor != len(shuffled):
        raise RuntimeError("FI refill cursor mismatch")
    after_counter = collections.Counter(shuffled)
    if before_counter != after_counter:
        raise RuntimeError("FI complete-token multiset invariant failed")

    out: Dict[str, List[b.Item]] = {ms: [] for ms in MANUSCRIPTS}
    originals = {
        (ms, it.item_id, it.leaf): it
        for ms in MANUSCRIPTS for it in published_by_ms[ms]
    }
    for ms in MANUSCRIPTS:
        for it in published_by_ms[ms]:
            key = (ms, it.item_id, it.leaf)
            li_map = lines_by_item[key]
            lines = [li_map[i] for i in range(len(it.lines))]
            if [len(x) for x in lines] != [len(x) for x in originals[key].lines]:
                raise RuntimeError("FI per-line token-count invariant failed")
            out[ms].append(b.Item(it.item_id, ms, lines, it.leaf))
    return out, {
        "definition": "global whole-token instance permutation of exact primary surface",
        "seed": stable_seed("issue72-v2:FI:pilot0:global-primary-token-instances"),
        "whole_token_multiset_preserved": True,
        "manuscript_item_line_token_counts_preserved": True,
        "tokens": len(flat),
        "distinct_tokens": len(before_counter),
        "role": "FINAL_SURFACE_SUFFICIENCY_ONLY",
    }


def write_trace_gzip(path: Path, obj) -> dict:
    raw = canonical_json_bytes(obj)
    with path.open("wb") as fout:
        with gzip.GzipFile(filename="", mode="wb", fileobj=fout, mtime=0) as gz:
            gz.write(raw)
    return {
        "raw_json_sha256": sha256_bytes(raw),
        "raw_json_bytes": len(raw),
        "gzip_sha256": sha256_bytes(path.read_bytes()),
        "gzip_bytes": path.stat().st_size,
    }


def check_external_authority(cremma_root: Path, naibbe_root: Path) -> dict:
    verify_git_head(cremma_root, EXPECTED_CREMMA, "CREMMA")
    verify_git_head(naibbe_root, EXPECTED_NAIBBE, "Naibbe")
    files = {
        "encoder": (naibbe_root / "naibbe_v2.py", EXPECTED_ENCODER_BLOB),
        "table": (naibbe_root / "references" / "naibbe_tables.csv", EXPECTED_TABLE_BLOB),
        "decoder": (naibbe_root / "decrypt_naibbe.py", EXPECTED_DECODER_BLOB),
    }
    got = {}
    for label, (path, expected) in files.items():
        blob = git_blob_sha1(path.read_bytes())
        if blob != expected:
            raise RuntimeError(f"{label} blob mismatch: {blob} != {expected}")
        got[label] = blob
    return {
        "cremma_commit": EXPECTED_CREMMA,
        "naibbe_commit": EXPECTED_NAIBBE,
        "naibbe_blobs": got,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT OUTPUT_DIR")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    outdir = Path(argv[3]).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    authority = check_external_authority(crem, nai)
    module = n64.load_naibbe(nai)
    original_map = dict(module.placeholder_to_glyph)
    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)

    sources = {
        name: b.parse_latin_manuscript(crem, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }

    baseline_primary: Dict[str, List[b.Item]] = {}
    baseline_raw: Dict[str, List[b.Item]] = {}
    traces_by_ms: Dict[str, dict] = {}
    replay = {}

    for mi, ms in enumerate(MANUSCRIPTS):
        seed = 6480000 + 100 * mi
        traced_primary, traced_raw, trace, tdiag = trace_encrypt_manuscript(
            module, sources[ms], ms, original_map, seed
        )
        # Independent historical implementation replay at the same seed.
        hist_primary, hist_raw, hdiag = n64.encrypt_manuscript(
            module, sources[ms], ms, original_map, seed
        )
        if canonical_items_bytes(traced_primary) != canonical_items_bytes(hist_primary):
            raise RuntimeError(f"{ms}: instrumented primary replay mismatch")
        if canonical_items_bytes(traced_raw) != canonical_items_bytes(hist_raw):
            raise RuntimeError(f"{ms}: instrumented raw replay mismatch")
        if tdiag["ambiguity_retries"] != hdiag["ambiguity_retries"]:
            raise RuntimeError(f"{ms}: ambiguity retry mismatch")

        trace_primary, trace_raw, rdiag = render_trace(trace, original_map)
        if canonical_items_bytes(trace_primary) != canonical_items_bytes(traced_primary):
            raise RuntimeError(f"{ms}: trace-only primary reconstruction mismatch")
        if canonical_items_bytes(trace_raw) != canonical_items_bytes(traced_raw):
            raise RuntimeError(f"{ms}: trace-only raw reconstruction mismatch")

        psha = surface_sha(traced_primary)
        if psha != EXPECTED_PRIMARY_SURFACE_SHA[ms]:
            raise RuntimeError(f"{ms}: frozen Issue68 primary surface mismatch: {psha}")

        trace_path = outdir / f"trace_{ms}.json.gz"
        trace_file = write_trace_gzip(trace_path, trace)
        baseline_primary[ms] = traced_primary
        baseline_raw[ms] = traced_raw
        traces_by_ms[ms] = trace
        replay[ms] = {
            "seed": seed,
            "primary_surface_sha256": psha,
            "raw_surface_sha256": surface_sha(traced_raw),
            "instrumented_equals_historical_primary": True,
            "instrumented_equals_historical_raw": True,
            "trace_only_equals_instrumented_primary": True,
            "trace_only_equals_instrumented_raw": True,
            "ambiguity_retries": tdiag["ambiguity_retries"],
            "trace_render": rdiag,
            "trace_file": trace_file,
            "parser_support_primary": parser_support(traced_primary, parser),
        }

    pooled_primary = [it for ms in MANUSCRIPTS for it in baseline_primary[ms]]
    pooled_sha = surface_sha(pooled_primary)
    if pooled_sha != EXPECTED_POOLED_PRIMARY_SHA:
        raise RuntimeError(f"pooled Issue68 primary surface mismatch: {pooled_sha}")

    fixed_pilots = {}
    for name, builder in (("EL", mapping_el), ("ES", mapping_es), ("ET", mapping_et), ("EG", mapping_eg)):
        modified_map, definition = builder(original_map)
        per_ms = {}
        all_items = []
        changed = 0
        total = 0
        for ms in MANUSCRIPTS:
            primary, _raw, diag = render_trace(traces_by_ms[ms], modified_map)
            per_ms[ms] = {
                "surface_sha256": surface_sha(primary),
                "parser_support": parser_support(primary, parser),
                "render": diag,
            }
            changed += diag["changed_events"]
            total += diag["events"]
            all_items.extend(primary)
        fixed_pilots[name] = {
            "definition": definition,
            "invariants": {
                "segmentation_held_fixed": True,
                "plaintext_trace_held_fixed": True,
                "accepted_table_schedule_held_fixed": True,
                "accepted_state_schedule_held_fixed": True,
                "retry_history_not_rerun": True,
                "published_spacing_join_mask_held_fixed": True,
                "unauthorized_trace_field_changes": 0,
            },
            "changed_events": int(changed),
            "events": int(total),
            "changed_event_fraction": float(changed / total) if total else 0.0,
            "pooled_surface_sha256": surface_sha(all_items),
            "pooled_parser_support": parser_support(all_items, parser),
            "ambiguity_legality": trace_bigram_legality(module, modified_map, traces_by_ms),
            "by_manuscript": per_ms,
            "interpretation_role": "FIXED_REALIZATION_CONDITIONAL_DIRECT_EMISSION_ABLATION",
        }

    # PT: a total upstream perturbation, not a fixed-path direct effect.
    pt_by_ms = {}
    pt_all = []
    for ms in MANUSCRIPTS:
        mi = MANUSCRIPTS.index(ms)
        seed = 6480000 + 100 * mi
        pp, _rr, ptrace, pdiag = trace_encrypt_manuscript(
            module, sources[ms], ms, original_map, seed, plaintext_transform=pt_transform(ms)
        )
        pt_by_ms[ms] = {
            "surface_sha256": surface_sha(pp),
            "parser_support": parser_support(pp, parser),
            "ambiguity_retries": pdiag["ambiguity_retries"],
            "plaintext_transform_changed_lines": pdiag["plaintext_transform_changed_lines"],
            "trace_raw_json_sha256": sha256_bytes(canonical_json_bytes(ptrace)),
        }
        pt_all.extend(pp)
    pt = {
        "definition": "within-effective-line character-order shuffle; exact character multiset/length preserved; entire pinned pipeline rerun",
        "invariants": {
            "per_line_character_multiset_preserved": True,
            "per_line_character_length_preserved": True,
            "published_codebook_and_algorithm_unchanged": True,
            "downstream_segmentation_table_retry_spacing_allowed_to_change": True,
        },
        "pooled_surface_sha256": surface_sha(pt_all),
        "pooled_parser_support": parser_support(pt_all, parser),
        "by_manuscript": pt_by_ms,
        "interpretation_role": "TOTAL_EFFECT_THROUGH_FULL_PUBLISHED_PIPELINE",
    }

    fi_by_ms, fi_diag = fi_surface(baseline_primary)
    fi_all = [it for ms in MANUSCRIPTS for it in fi_by_ms[ms]]
    fi = {
        "definition": fi_diag,
        "pooled_surface_sha256": surface_sha(fi_all),
        "pooled_parser_support": parser_support(fi_all, parser),
        "by_manuscript": {
            ms: {
                "surface_sha256": surface_sha(fi_by_ms[ms]),
                "parser_support": parser_support(fi_by_ms[ms], parser),
            }
            for ms in MANUSCRIPTS
        },
        "interpretation_role": "FINAL_SURFACE_INVENTORY_LAYOUT_SUFFICIENCY_ONLY",
    }

    result = {
        "schema": "issue72-v2-stage-a-trace-audit-result-v1",
        "status": "TRACE-IDENTIFIED INTERVENTION SET READY FOR TARGET DESIGN",
        "parent_main": PARENT_MAIN,
        "target_access": {
            "counterfactual_pair_Q_computed": False,
            "counterfactual_residual_Z_computed": False,
            "counterfactual_R1_energy_or_W_computed": False,
            "counterfactual_target_topology_computed": False,
            "counterfactual_R1_pvalue_computed": False,
            "ZL3b_IT2a_target_vectors_loaded": False,
        },
        "authority": authority,
        "parser_validation": parser_validation,
        "coverage_policy": "DESCRIPTIVE_ONLY_IN_STAGE_A_NO_0_60_GATE",
        "baseline_replay": replay,
        "pooled_baseline_primary_surface_sha256": pooled_sha,
        "fixed_path_emission_pilots": fixed_pilots,
        "plaintext_total_pipeline_pilot": pt,
        "final_surface_sufficiency_pilot": fi,
        "interpretation_guardrails": [
            "EL_ES_ET_EG are fixed-realization conditional emission ablations, not valid rerun Naibbe ciphertext families",
            "PT estimates a total upstream perturbation effect through the full published pipeline, not a direct plaintext-order effect",
            "FI can establish final-surface inventory/layout sufficiency only and cannot identify upstream codebook/process origin",
            "No Stage-A parser coverage value is a hard scientific cutoff",
        ],
    }

    result_path = outdir / "stage_a_trace_audit.json"
    result_path.write_bytes(canonical_json_bytes(result) + b"\n")
    manifest = {
        "result_sha256": sha256_bytes(result_path.read_bytes()),
        "result_bytes": result_path.stat().st_size,
        "trace_schema": TRACE_SCHEMA,
        "trace_files": {
            p.name: sha256_bytes(p.read_bytes())
            for p in sorted(outdir.glob("trace_*.json.gz"))
        },
    }
    (outdir / "MANIFEST.json").write_bytes(canonical_json_bytes(manifest) + b"\n")
    print(json.dumps({
        "status": result["status"],
        "pooled_baseline_primary_surface_sha256": pooled_sha,
        "result_sha256": manifest["result_sha256"],
        "fixed_path_pilots": {
            k: {
                "coverage": v["pooled_parser_support"]["coverage"],
                "changed_event_fraction": v["changed_event_fraction"],
                "ambiguity_admissible_fraction": v["ambiguity_legality"]["admissible_fraction"],
            }
            for k, v in fixed_pilots.items()
        },
        "PT_coverage": pt["pooled_parser_support"]["coverage"],
        "FI_coverage": fi["pooled_parser_support"]["coverage"],
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
