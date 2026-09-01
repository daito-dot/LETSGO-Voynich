#!/usr/bin/env python3
"""Issue #72 Stage-A Naibbe source/architecture audit.

This executable is deliberately target-blind with respect to new counterfactual
R1 performance. It may inspect source/codebook architecture, build frozen
support-pilot surfaces, and measure direct SlotParser coverage. It MUST NOT
compute pair-Q, residual-Z, energy, reliability, target topology, or R1 p-values.
"""
from __future__ import annotations

import collections
import hashlib
import inspect
import json
import random
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, Sequence

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("phase62", "phase64", "issue26-music"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as b  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402

PARENT_MAIN = "ce49de68a3bd308b9432f5904b5368fc4c6f9c8f"
EXPECTED_NAIBBE = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
EXPECTED_ENCODER_BLOB = "b566ad82e4b6ff0782ecdddebf77718dac44f292"
EXPECTED_TABLE_BLOB = "5cd34fb81d80faf3b4d57dbf1719c05ffde25302"
EXPECTED_DECODER_BLOB = "b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b"
EXPECTED_CREMMA = "292525969ad98380b398e6606a9c2a36d51913ae"
ISSUE68_PREFLIGHT_SHA = "fdd2b1138542bf1b332b20f27a9869ac7a3501038e7d4ec9ccf40910e3b98771"
SUPPORT_GATE = 0.60
MANUSCRIPTS = tuple(n64.MANUSCRIPTS)
PRIMARY_SEEDS = tuple(6480000 + 100 * i for i in range(len(MANUSCRIPTS)))
EXPECTED_SURFACE_SHA = {
    "BIS193": "fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805",
    "CLM13027": "da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77",
    "Mazarine915": "2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d",
    "UBL758": "5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89",
}
EXPECTED_POOLED_SHA = "47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd"
CODE_RE = re.compile(r"^(unigram|prefix|suffix)_(alpha|beta1|beta2|beta3|gamma1|gamma2)_([a-z])$")
EXCLUDED = tuple(x for x in "abcdefghijklmnopqrstuvwxyz" if x not in n64.EFFECTIVE_LETTERS)


def stable_seed(label: str) -> int:
    d = hashlib.sha256(label.encode("utf-8")).digest()
    return int.from_bytes(d[:8], "big") % (2**31 - 1)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def canonical_items_payload(items: Sequence[b.Item]) -> bytes:
    rows = []
    for it in items:
        rows.append({
            "item_id": it.item_id,
            "document": it.document,
            "leaf": it.leaf,
            "lines": [["".join(tok) for tok in line] for line in it.lines],
        })
    return json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def surface_sha(items: Sequence[b.Item]) -> str:
    return hashlib.sha256(canonical_items_payload(items)).hexdigest()


def map_sha(glyph_map: Dict[str, str]) -> str:
    payload = json.dumps(glyph_map, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def parser_support(items: Sequence[b.Item], parser: e.SlotParser) -> dict:
    visible = accepted = 0
    per_doc = collections.Counter()
    per_doc_ok = collections.Counter()
    for it in items:
        for line in it.lines:
            for tok_units in line:
                tok = "".join(tok_units)
                if not tok:
                    continue
                visible += 1
                per_doc[it.document] += 1
                if parser.pick(tok, "min") is not None:
                    accepted += 1
                    per_doc_ok[it.document] += 1
    return {
        "visible_tokens": int(visible),
        "accepted_tokens": int(accepted),
        "coverage": float(accepted / visible) if visible else 0.0,
        "gate": SUPPORT_GATE,
        "eligible": bool(visible and accepted / visible >= SUPPORT_GATE),
        "by_document": {
            k: {
                "visible": int(per_doc[k]),
                "accepted": int(per_doc_ok[k]),
                "coverage": float(per_doc_ok[k] / per_doc[k]) if per_doc[k] else 0.0,
            }
            for k in sorted(per_doc)
        },
    }


def parse_codebook(module):
    parsed = {}
    for code, glyph in module.placeholder_to_glyph.items():
        m = CODE_RE.match(code)
        if not m:
            raise RuntimeError(f"unexpected codebook code: {code!r}")
        state, table, letter = m.groups()
        parsed[(state, table, letter)] = str(glyph)
    expected = len(module.STATES) * len(module.TABLES) * len(module.ALPHABET)
    if len(parsed) != expected:
        raise RuntimeError(f"codebook cell count {len(parsed)} != {expected}")
    return parsed


def counter_dict(values: Iterable[str]) -> dict:
    c = collections.Counter(values)
    return {k: int(v) for k, v in sorted(c.items())}


def codebook_audit(module, parser: e.SlotParser) -> dict:
    cells = parse_codebook(module)
    effective = {
        k: v for k, v in cells.items()
        if k[2] in set(n64.EFFECTIVE_LETTERS)
    }
    excluded = {k: v for k, v in cells.items() if k[2] in set(EXCLUDED)}
    if len(effective) != 6 * 3 * 23 or len(excluded) != 6 * 3 * 3:
        raise RuntimeError("effective/excluded codebook cell counts unexpected")

    values = list(effective.values())
    counts = collections.Counter(values)
    duplicate_values = {k: int(v) for k, v in sorted(counts.items()) if v > 1}

    def cell_support(keys):
        vals = [cells[k] for k in keys]
        ok = [parser.pick(v, "min") is not None for v in vals]
        return {
            "cells": len(vals),
            "accepted_cells": int(sum(ok)),
            "coverage": float(sum(ok) / len(vals)) if vals else None,
            "distinct_values": len(set(vals)),
            "length_min": min(map(len, vals)) if vals else None,
            "length_median": float(__import__("statistics").median(map(len, vals))) if vals else None,
            "length_max": max(map(len, vals)) if vals else None,
        }

    by_state = {}
    state_sets = {}
    for state in module.STATES:
        keys = [k for k in effective if k[0] == state]
        by_state[state] = cell_support(keys)
        state_sets[state] = set(effective[k] for k in keys)

    by_table = {}
    table_sets = {}
    for table in module.TABLES:
        keys = [k for k in effective if k[1] == table]
        by_table[table] = cell_support(keys)
        table_sets[table] = set(effective[k] for k in keys)

    state_overlap = {}
    for i, a in enumerate(module.STATES):
        for bb in module.STATES[i + 1:]:
            state_overlap[f"{a}__{bb}"] = len(state_sets[a] & state_sets[bb])
    table_overlap = {}
    for i, a in enumerate(module.TABLES):
        for bb in module.TABLES[i + 1:]:
            table_overlap[f"{a}__{bb}"] = len(table_sets[a] & table_sets[bb])

    # Collision catalog is internal codebook architecture, not a manuscript R1 statistic.
    catalog = module.bigram_catalog
    catalog_collisions = {k: v for k, v in catalog.items() if len(v) > 1}
    unigram_set = set(module.unigram_glyphs)

    eff_prefix = [
        (f"prefix_{t}_{l}", cells[("prefix", t, l)])
        for t in module.TABLES for l in n64.EFFECTIVE_LETTERS
    ]
    eff_suffix = [
        (f"suffix_{t}_{l}", cells[("suffix", t, l)])
        for t in module.TABLES for l in n64.EFFECTIVE_LETTERS
    ]
    eff_total = eff_unigram_collision = eff_cross_collision = 0
    for pc, pg in eff_prefix:
        for sc, sg in eff_suffix:
            eff_total += 1
            combined = pg + sg
            if combined in unigram_set:
                eff_unigram_collision += 1
            pairs = catalog.get(combined, set())
            if any(pair != (pc, sc) for pair in pairs):
                eff_cross_collision += 1

    return {
        "full_cells": len(cells),
        "effective_letters": list(n64.EFFECTIVE_LETTERS),
        "excluded_normalized_letters": list(EXCLUDED),
        "effective_cells": len(effective),
        "excluded_cells": len(excluded),
        "distinct_effective_glyph_values": len(set(values)),
        "duplicate_effective_glyph_value_count": len(duplicate_values),
        "duplicate_effective_glyph_cell_excess": int(sum(v - 1 for v in counts.values() if v > 1)),
        "duplicate_effective_values": duplicate_values,
        "effective_cell_support": cell_support(list(effective)),
        "by_state": by_state,
        "by_table": by_table,
        "state_distinct_value_overlap": state_overlap,
        "table_distinct_value_overlap": table_overlap,
        "full_bigram_catalog_strings": len(catalog),
        "full_bigram_catalog_collision_strings": len(catalog_collisions),
        "effective_prefix_suffix_pair_attempts": eff_total,
        "effective_pairs_equal_to_unigram_glyph": eff_unigram_collision,
        "effective_pairs_with_cross_bigram_collision": eff_cross_collision,
        "unreachable_cells_are_in_published_collision_catalog": True,
        "reason": "build_bigram_catalog iterates module.ALPHABET (26 letters), while Phase64B projected source uses 23 effective letters",
    }


def source_architecture_audit(module) -> dict:
    rsrc = inspect.getsource(module.respace_plaintext)
    dsrc = inspect.getsource(module.create_card_deck)
    esrc = inspect.getsource(module.encrypt_naibbe)
    ssrc = inspect.getsource(module.respace_line)
    csrc = inspect.getsource(module.clean_line)

    required = [
        ("respace_plaintext_random", "random.random() < (RESPACING / 36)" in rsrc),
        ("deck_random_shuffle", "random.shuffle(deck)" in dsrc),
        ("ambiguity_retry_loop", "for _ in range(MAX_BIGRAM_RETRIES)" in esrc),
        ("unigram_collision_rejection", "combined in unigram_glyphs" in esrc),
        ("cross_bigram_collision_rejection", "any_other" in esrc and "bigram_catalog" in esrc),
        ("space_removal_random", "random.random() < drop_rate" in ssrc),
        ("wjk_normalization", '.replace("W", "UU").replace("J", "I").replace("K", "C")' in csrc),
    ]
    failed = [name for name, ok in required if not ok]
    if failed:
        raise RuntimeError(f"published source architecture assertions failed: {failed}")

    return {
        "call_order": [
            "clean_line",
            "Phase64B project_effective_plaintext",
            "respace_plaintext",
            "create_card_deck / table consumption",
            "state-specific codebook lookup",
            "ambiguity collision retry for bigrams",
            "ciphertext token emission",
            "respace_line 3pct space removal",
        ],
        "rng_dependencies": {
            "plaintext_segmentation": "random.random; depends on current index/remaining length and prior segmentation RNG, not character identity directly",
            "table_deck": "random.shuffle; table choice independent of character identity at draw time, but number/timing of draws depends on unigram/bigram segmentation and collision retries",
            "ambiguity_retry": "accept/reject depends on plaintext letters + selected tables/states + codebook glyph values; retries consume additional deck entries and therefore alter downstream RNG/state trajectory",
            "ciphertext_space_removal": "random.random per emitted token after first; direct decision independent of glyph identity, but token count/RNG state can differ upstream",
            "single_global_rng_stream": True,
        },
        "normalization": {
            "removes_nonletters": True,
            "removes_source_spaces_punctuation": True,
            "W_to_UU": True,
            "J_to_I": True,
            "K_to_C": True,
            "phase64b_drop_only_projection_to_effective_23": True,
        },
        "published_defaults": {
            "RESPACING": module.RESPACING,
            "USE_78_CARD_DECK": module.USE_78_CARD_DECK,
            "SPACE_REMOVAL_RATE": module.SPACE_REMOVAL_RATE,
            "UNAMBIGUOUS": module.UNAMBIGUOUS,
            "MAX_BIGRAM_RETRIES": module.MAX_BIGRAM_RETRIES,
            "CARD_WEIGHTS_78": module.CARD_WEIGHTS[True],
        },
    }


def original_sources(cremma_root: Path):
    return {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }


def source_line_effective(module, line: b.Line) -> str:
    source = n64.string_line(line)
    cleaned = module.clean_line(source)
    eff, _ = n64.project_effective_plaintext(cleaned)
    return eff


def p_source_items(module, items: Sequence[b.Item], manuscript: str):
    out = []
    invariant_lines = 0
    for it in items:
        lines = []
        for li, line in enumerate(it.lines):
            eff = source_line_effective(module, line)
            chars = list(eff)
            rng = random.Random(stable_seed(f"issue72:P:pilot0:{manuscript}:{it.item_id}:{li}"))
            shuffled = list(chars)
            rng.shuffle(shuffled)
            if len(shuffled) != len(chars) or collections.Counter(shuffled) != collections.Counter(chars):
                raise RuntimeError("P0 per-line character invariant failed")
            invariant_lines += 1
            lines.append([tuple("".join(shuffled))] if shuffled else [])
        out.append(b.Item(item_id=it.item_id, document=it.document, lines=lines, leaf=it.leaf))
    return out, {"lines_checked": invariant_lines, "per_line_length_and_character_multiset_preserved": True}


def derangement(items: Sequence[str], label: str):
    base = list(items)
    vals = list(base)
    random.Random(stable_seed(label)).shuffle(vals)
    if any(a == bb for a, bb in zip(base, vals)):
        found = None
        for shift in range(1, len(vals)):
            rotated = vals[shift:] + vals[:shift]
            if all(a != bb for a, bb in zip(base, rotated)):
                found = rotated
                break
        if found is None:
            raise RuntimeError(f"cannot construct deterministic derangement for {label}")
        vals = found
    return dict(zip(base, vals))


def map_L(module, original):
    perm = derangement(n64.EFFECTIVE_LETTERS, "issue72:L:pilot0:global-effective-letter-permutation")
    out = dict(original)
    for state in module.STATES:
        for table in module.TABLES:
            before = []
            after = []
            for letter in n64.EFFECTIVE_LETTERS:
                code = f"{state}_{table}_{letter}"
                source_code = f"{state}_{table}_{perm[letter]}"
                before.append(original[code])
                out[code] = original[source_code]
                after.append(out[code])
            if collections.Counter(before) != collections.Counter(after):
                raise RuntimeError("L0 table-state multiset invariant failed")
    return out, {
        "effective_letter_permutation": perm,
        "fixed_points": sum(k == v for k, v in perm.items()),
        "table_state_effective_value_multisets_preserved": True,
    }


def map_S(module, original):
    out = dict(original)
    states = list(module.STATES)
    for table in module.TABLES:
        for letter in n64.EFFECTIVE_LETTERS:
            before = [original[f"{s}_{table}_{letter}"] for s in states]
            # old unigram -> new prefix, old prefix -> new suffix, old suffix -> new unigram
            for i, s in enumerate(states):
                source_state = states[(i - 1) % len(states)]
                out[f"{s}_{table}_{letter}"] = original[f"{source_state}_{table}_{letter}"]
            after = [out[f"{s}_{table}_{letter}"] for s in states]
            if collections.Counter(before) != collections.Counter(after):
                raise RuntimeError("S0 table-letter state multiset invariant failed")
    return out, {
        "state_rotation": "old unigram->new prefix; old prefix->new suffix; old suffix->new unigram",
        "table_letter_three_value_multisets_preserved": True,
    }


def map_T(module, original):
    out = dict(original)
    tables = list(module.TABLES)
    for state in module.STATES:
        for letter in n64.EFFECTIVE_LETTERS:
            before = [original[f"{state}_{t}_{letter}"] for t in tables]
            for i, t in enumerate(tables):
                dest = tables[(i + 1) % len(tables)]
                out[f"{state}_{dest}_{letter}"] = original[f"{state}_{t}_{letter}"]
            after = [out[f"{state}_{t}_{letter}"] for t in tables]
            if collections.Counter(before) != collections.Counter(after):
                raise RuntimeError("T0 state-letter table multiset invariant failed")
    return out, {
        "table_rotation": "alpha->beta1->beta2->beta3->gamma1->gamma2->alpha",
        "state_letter_six_value_multisets_preserved": True,
        "published_table_weights_unchanged": True,
    }


def map_G(module, original):
    out = dict(original)
    keys = [
        f"{state}_{table}_{letter}"
        for state in module.STATES
        for table in module.TABLES
        for letter in n64.EFFECTIVE_LETTERS
    ]
    values = [original[k] for k in keys]
    shuffled = list(values)
    random.Random(stable_seed("issue72:G:pilot0:global-effective-cell-permutation")).shuffle(shuffled)
    for k, v in zip(keys, shuffled):
        out[k] = v
    if collections.Counter(values) != collections.Counter(out[k] for k in keys):
        raise RuntimeError("G0 global effective-cell multiset invariant failed")
    return out, {
        "effective_cell_instances": len(keys),
        "global_effective_value_multiset_preserved": True,
        "duplicate_values_permuted_as_cell_instances": True,
    }


def permute_published_token_instances(items_by_manuscript: dict):
    # Preserve manuscript/item/line shape and exact pooled whole-token multiset.
    flat = []
    skeleton = []
    for manuscript in MANUSCRIPTS:
        for it in items_by_manuscript[manuscript]:
            line_lengths = []
            for line in it.lines:
                line_lengths.append(len(line))
                flat.extend(tuple(tok) for tok in line)
            skeleton.append((manuscript, it, line_lengths))
    before = collections.Counter("".join(tok) for tok in flat)
    shuffled = list(flat)
    random.Random(stable_seed("issue72:I:pilot0:published-primary-token-instance-permutation")).shuffle(shuffled)
    it_flat = iter(shuffled)
    out = {m: [] for m in MANUSCRIPTS}
    for manuscript, src, line_lengths in skeleton:
        lines = []
        for n in line_lengths:
            lines.append([tuple(next(it_flat)) for _ in range(n)])
        out[manuscript].append(b.Item(item_id=src.item_id, document=src.document, lines=lines, leaf=src.leaf))
    try:
        next(it_flat)
        raise RuntimeError("I0 token iterator not exhausted as expected")
    except StopIteration:
        pass
    after = collections.Counter(
        "".join(tok)
        for manuscript in MANUSCRIPTS
        for it in out[manuscript]
        for line in it.lines
        for tok in line
    )
    if before != after:
        raise RuntimeError("I0 exact token multiset invariant failed")
    # line counts / token counts are preserved by construction.
    return out, {
        "token_instances": sum(before.values()),
        "distinct_token_types": len(before),
        "exact_global_whole_token_multiset_preserved": True,
        "exact_item_line_token_count_layout_preserved": True,
    }


def pooled(items_by_manuscript: dict):
    return [it for m in MANUSCRIPTS for it in items_by_manuscript[m]]


def generate_with_map(module, sources, glyph_map, parser, label):
    by_m = {}
    diags = {}
    for mi, manuscript in enumerate(MANUSCRIPTS):
        primary, _raw, diag = n64.encrypt_manuscript(
            module, sources[manuscript], manuscript, glyph_map, PRIMARY_SEEDS[mi]
        )
        by_m[manuscript] = primary
        diags[manuscript] = diag
    pp = pooled(by_m)
    return {
        "label": label,
        "surface_sha256": surface_sha(pp),
        "support": parser_support(pp, parser),
        "generation_completed": True,
        "ambiguity_retries_by_manuscript": {
            m: int(diags[m]["ambiguity_retries"]) for m in MANUSCRIPTS
        },
        "primary_tokens_by_manuscript": {
            m: int(diags[m]["primary_tokens"]) for m in MANUSCRIPTS
        },
        "map_sha256": map_sha(glyph_map),
    }, by_m


def generate_P(module, sources, original_map, parser):
    transformed = {}
    invariants = {}
    for m in MANUSCRIPTS:
        transformed[m], invariants[m] = p_source_items(module, sources[m], m)
    result, by_m = generate_with_map(module, transformed, original_map, parser, "P0_plaintext_order")
    result["invariants"] = invariants
    return result, by_m


def main(cremma_root: Path, naibbe_root: Path):
    if b.verify_cremma_commit(cremma_root) != EXPECTED_CREMMA:
        raise RuntimeError("CREMMA authority mismatch")
    module = n64.load_naibbe(naibbe_root)
    if git_blob((naibbe_root / "naibbe_v2.py").read_bytes()) != EXPECTED_ENCODER_BLOB:
        raise RuntimeError("encoder blob mismatch")
    if git_blob((naibbe_root / "references" / "naibbe_tables.csv").read_bytes()) != EXPECTED_TABLE_BLOB:
        raise RuntimeError("table blob mismatch")
    if git_blob((naibbe_root / "decrypt_naibbe.py").read_bytes()) != EXPECTED_DECODER_BLOB:
        raise RuntimeError("decoder blob mismatch")

    pf_path = EXPERIMENTS / "joint-constraint-tournament" / "preflight" / "preflight.json"
    if hashlib.sha256(pf_path.read_bytes()).hexdigest() != ISSUE68_PREFLIGHT_SHA:
        raise RuntimeError("Issue68 preflight authority SHA mismatch")
    pf = json.loads(pf_path.read_text(encoding="utf-8"))

    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)
    sources = original_sources(cremma_root)
    original_map = dict(module.placeholder_to_glyph)

    # Reproduce exact already-observed published primary surfaces without pair scoring.
    published_by_m = {}
    published_diag = {}
    for mi, m in enumerate(MANUSCRIPTS):
        primary, _raw, diag = n64.encrypt_manuscript(module, sources[m], m, original_map, PRIMARY_SEEDS[mi])
        got = surface_sha(primary)
        if got != EXPECTED_SURFACE_SHA[m]:
            raise RuntimeError(f"published primary surface SHA mismatch {m}: {got}")
        published_by_m[m] = primary
        published_diag[m] = diag
    published_pool = pooled(published_by_m)
    if surface_sha(published_pool) != EXPECTED_POOLED_SHA:
        raise RuntimeError("published pooled surface SHA mismatch")
    published_support = parser_support(published_pool, parser)
    if published_support["visible_tokens"] != pf["Naibbe_primary"]["pooled_coverage"]["visible_tokens"]:
        raise RuntimeError("published visible token count differs from Issue68 preflight")
    if published_support["accepted_tokens"] != pf["Naibbe_primary"]["pooled_coverage"]["accepted_tokens"]:
        raise RuntimeError("published accepted token count differs from Issue68 preflight")

    arch = source_architecture_audit(module)
    cb = codebook_audit(module, parser)

    # Stage-A support pilots. No pair/residual functions are imported or called.
    p0, _ = generate_P(module, sources, original_map, parser)

    lmap, linv = map_L(module, original_map)
    l0, _ = generate_with_map(module, sources, lmap, parser, "L0_letter_association")
    l0["invariants"] = linv

    smap, sinv = map_S(module, original_map)
    s0, _ = generate_with_map(module, sources, smap, parser, "S0_state_allocation")
    s0["invariants"] = sinv

    tmap, tinv = map_T(module, original_map)
    t0, _ = generate_with_map(module, sources, tmap, parser, "T0_table_allocation")
    t0["invariants"] = tinv

    gmap, ginv = map_G(module, original_map)
    g0, _ = generate_with_map(module, sources, gmap, parser, "G0_global_effective_cell")
    g0["invariants"] = ginv

    i_by_m, iinv = permute_published_token_instances(published_by_m)
    i_pool = pooled(i_by_m)
    i0 = {
        "label": "I0_exact_published_token_inventory",
        "surface_sha256": surface_sha(i_pool),
        "support": parser_support(i_pool, parser),
        "generation_completed": True,
        "invariants": iinv,
        "map_sha256": None,
        "ambiguity_retries_by_manuscript": None,
    }

    pilots = {x["label"].split("_")[0]: x for x in (p0, l0, s0, t0, g0, i0)}
    support_eligible = [k for k, v in pilots.items() if v["support"]["eligible"] and v["generation_completed"]]

    # Feasibility interpretation based only on source/support/invariants.
    feasibility = {
        "P": {
            "mechanically_identifiable": True,
            "scope": "total causal effect of within-line plaintext order through the published single-RNG process",
            "important_mediator": "changed bigram identities can change ambiguity retries and downstream deck/RNG trajectory; this is a causal consequence, not held fixed",
        },
        "L": {
            "mechanically_identifiable": True,
            "scope": "consistent effective-letter association while preserving every table-state reachable glyph multiset",
            "collision_catalog_note": "published collision catalog includes all 26 codebook letters; the intervention preserves full table-state value sets because excluded j/k/w cells remain fixed",
        },
        "S": {
            "mechanically_identifiable": True,
            "scope": "state specialization; changes unigram versus prefix/suffix value allocation while preserving each table-letter three-value multiset",
        },
        "T": {
            "mechanically_identifiable": True,
            "scope": "table allocation under unequal published table weights; preserves each state-letter six-value multiset",
        },
        "G": {
            "mechanically_identifiable": True,
            "scope": "global reachable-cell association with exact effective-value multiset preservation; unreachable 54 cells remain fixed but still participate in collision catalog",
        },
        "I": {
            "mechanically_identifiable": True,
            "scope": "upper-bound exact emitted-token-inventory control; removes source/process association while preserving exact whole-token multiset and line token-count layout",
            "not_a_neutral_historical_null": True,
        },
    }

    result = {
        "phase": "Issue72-StageA-source-architecture-audit",
        "parent_main": PARENT_MAIN,
        "counterfactual_R1_scored": False,
        "forbidden_quantities_computed": {
            "pair_Q": False,
            "residual_Z": False,
            "residual_energy": False,
            "residual_reliability": False,
            "target_topology": False,
            "R1_p_values": False,
            "per_edge_differences": False,
        },
        "source_authority": {
            "Naibbe_commit": EXPECTED_NAIBBE,
            "encoder_blob": EXPECTED_ENCODER_BLOB,
            "table_blob": EXPECTED_TABLE_BLOB,
            "decoder_blob": EXPECTED_DECODER_BLOB,
            "CREMMA_commit": EXPECTED_CREMMA,
            "Issue68_preflight_sha256": ISSUE68_PREFLIGHT_SHA,
        },
        "parser": {
            "authority": "experiments/issue26-music/issue26e_core.py::SlotParser",
            "policy": "min",
            "validation": parser_validation,
            "support_gate": SUPPORT_GATE,
        },
        "architecture": arch,
        "codebook": cb,
        "published_primary_reproduction": {
            "per_manuscript_surface_sha256": {m: surface_sha(published_by_m[m]) for m in MANUSCRIPTS},
            "pooled_surface_sha256": surface_sha(published_pool),
            "support": published_support,
            "ambiguity_retries_by_manuscript": {m: int(published_diag[m]["ambiguity_retries"]) for m in MANUSCRIPTS},
        },
        "support_pilots": pilots,
        "support_eligible_axes": support_eligible,
        "feasibility": feasibility,
        "stageA_classification": (
            "COUNTERFACTUAL DECOMPOSITION INTERFACES IDENTIFIABLE"
            if all(v["mechanically_identifiable"] for v in feasibility.values())
            else "DECOMPOSITION DESIGN NOT IDENTIFIABLE"
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {sys.argv[0]} CREMMA_ROOT NAIBBE_ROOT")
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
