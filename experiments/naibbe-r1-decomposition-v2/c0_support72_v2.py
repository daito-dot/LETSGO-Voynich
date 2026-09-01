#!/usr/bin/env python3
"""Issue #72 V2 Stage C0: target-blind fixed-path randomization support freeze.

Extends exact accepted-event traces to historical rep0..rep4, then generates
31 deterministic target-blind assignments for each fixed-path direct-emission
axis EL/ES/ET/EG. No slot-pair Q, residual-Z, target correlation, R1 p-value,
or PT/FI intervention is computed here.

Usage:
  python c0_support72_v2.py CREMMA_ROOT NAIBBE_ROOT B2_RAW_JSON OUTPUT_DIR
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Dict, Mapping, Sequence

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
EXPECTED_CREMMA = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_B2_SHA256 = "2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147"
REPS = tuple(range(5))
N_ASSIGN = 31
AXES = ("EL", "ES", "ET", "EG")
EFFECTIVE_LETTERS = tuple(n64.EFFECTIVE_LETTERS)
STATES = ("unigram", "prefix", "suffix")
TABLES = ("alpha", "beta1", "beta2", "beta3", "gamma1", "gamma2")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def git_head(root: Path) -> str:
    import subprocess
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def load_b2(path: Path) -> dict:
    raw = path.read_bytes()
    if sha256_bytes(raw) != EXPECTED_B2_SHA256:
        raise RuntimeError("Stage B2 raw authority SHA mismatch")
    x = json.loads(raw)
    if x["status"] != "EXTENDED UNCHANGED-NAIBBE R1 DISTRIBUTION CALIBRATED":
        raise RuntimeError("Stage B2 authority status mismatch")
    if x["population"]["reps"] != list(range(25)):
        raise RuntimeError("Stage B2 population mismatch")
    if x["issue72_intervention_R1_computed"] or x["issue72_intervention_surface_loaded_or_generated"]:
        raise RuntimeError("Stage B2 intervention firewall not clean")
    return x


def surface_payload(items: Sequence[b.Item]) -> bytes:
    rows = []
    for it in items:
        rows.append({
            "item_id": it.item_id,
            "document": it.document,
            "leaf": it.leaf,
            "lines": [["".join(tok) for tok in line] for line in it.lines],
        })
    return canonical_json_bytes(rows)


def surface_sha(items: Sequence[b.Item]) -> str:
    return sha256_bytes(surface_payload(items))


def parser_support(items: Sequence[b.Item], parser: e.SlotParser) -> dict:
    visible = accepted = 0
    by_doc = collections.Counter()
    by_doc_ok = collections.Counter()
    for it in items:
        for line in it.lines:
            for units in line:
                tok = "".join(units)
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
        "by_document": {
            k: {
                "visible": int(by_doc[k]),
                "accepted": int(by_doc_ok[k]),
                "coverage": float(by_doc_ok[k] / by_doc[k]) if by_doc[k] else 0.0,
            }
            for k in sorted(by_doc)
        },
    }


def glyph_line(tokens: Sequence[str]) -> b.Line:
    return [tuple(x) for x in tokens if x]


def source_items(cremma_root: Path) -> Dict[str, Sequence[b.Item]]:
    return {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }


def consume_table(module, deck: list[str], deck_index: int) -> tuple[str, list[str], int]:
    if deck_index >= len(deck):
        deck = module.create_card_deck(module.USE_78_CARD_DECK)
        deck_index = 0
    table = deck[deck_index]
    return table, deck, deck_index + 1


def instrumented_line(module, cleaned: str, glyph_map: Mapping[str, str]) -> tuple[list[str], list[dict], list[bool], int]:
    """Mirror pinned published encryption and record accepted-event path."""
    ngrams = module.respace_plaintext(cleaned, None)
    deck = module.create_card_deck(module.USE_78_CARD_DECK)
    deck_index = 0
    encrypted: list[str] = []
    events: list[dict] = []
    retries = 0

    for token in ngrams:
        if len(token) == 1:
            table, deck, deck_index = consume_table(module, deck, deck_index)
            code = module.naibbe_tables[table][("unigram", token)]
            glyph = glyph_map.get(code, code)
            encrypted.append(glyph)
            events.append({
                "plaintext_unit": token,
                "kind": "unigram",
                "accepted_codes": [code],
                "accepted_tables": [table],
                "accepted_states": ["unigram"],
                "retry_count": 0,
            })
            continue

        accepted = False
        last = None
        attempts = []
        for _ in range(module.MAX_BIGRAM_RETRIES):
            tp, deck, deck_index = consume_table(module, deck, deck_index)
            cp = module.naibbe_tables[tp][("prefix", token[0])]
            gp = glyph_map.get(cp, cp)
            ts, deck, deck_index = consume_table(module, deck, deck_index)
            cs = module.naibbe_tables[ts][("suffix", token[1])]
            gs = glyph_map.get(cs, cs)
            combined = gp + gs
            unigram_collision = combined in module.unigram_glyphs
            pairs = module.bigram_catalog.get(combined, set())
            cross_collision = any(pair != (cp, cs) for pair in pairs)
            rejected = bool(unigram_collision or cross_collision)
            attempts.append({
                "prefix_code": cp,
                "suffix_code": cs,
                "prefix_table": tp,
                "suffix_table": ts,
                "rejected": rejected,
                "unigram_collision": bool(unigram_collision),
                "cross_collision": bool(cross_collision),
            })
            last = (tp, ts, cp, cs, combined)
            if rejected:
                retries += 1
                continue
            encrypted.append(combined)
            events.append({
                "plaintext_unit": token,
                "kind": "bigram",
                "accepted_codes": [cp, cs],
                "accepted_tables": [tp, ts],
                "accepted_states": ["prefix", "suffix"],
                "retry_count": len(attempts) - 1,
                "attempts": attempts,
            })
            accepted = True
            break
        if not accepted:
            if last is None:
                raise RuntimeError("bigram retry loop had no attempt")
            tp, ts, cp, cs, combined = last
            encrypted.append(combined)
            events.append({
                "plaintext_unit": token,
                "kind": "bigram",
                "accepted_codes": [cp, cs],
                "accepted_tables": [tp, ts],
                "accepted_states": ["prefix", "suffix"],
                "retry_count": len(attempts) - 1,
                "attempts": attempts,
                "retry_exhausted": True,
            })

    drop_flags: list[bool] = []
    if len(encrypted) >= 2:
        for _tok in encrypted[1:]:
            drop_flags.append(bool(random.random() < module.SPACE_REMOVAL_RATE))
    return encrypted, events, drop_flags, retries


def apply_spacing(raw_tokens: Sequence[str], drop_flags: Sequence[bool]) -> list[str]:
    if not raw_tokens:
        if drop_flags:
            raise RuntimeError("spacing flags on empty line")
        return []
    if len(drop_flags) != max(0, len(raw_tokens) - 1):
        raise RuntimeError("spacing-mask length mismatch")
    out = [raw_tokens[0]]
    for i, tok in enumerate(raw_tokens[1:]):
        if drop_flags[i]:
            out[-1] += tok
        else:
            out.append(tok)
    return out


def trace_manuscript(module, items: Sequence[b.Item], manuscript: str, glyph_map: Mapping[str, str], seed: int):
    n64.set_glyph_map(module, dict(glyph_map))
    random.seed(seed)
    module.ambiguity_retries = 0
    primary: list[b.Item] = []
    raw_items: list[b.Item] = []
    trace_items = []
    total_retries = 0

    for it in items:
        p_lines = []
        r_lines = []
        t_lines = []
        for li, line in enumerate(it.lines):
            source = n64.string_line(line)
            published_cleaned = module.clean_line(source)
            cleaned, dropped = n64.project_effective_plaintext(published_cleaned)
            if cleaned:
                raw_tokens, events, drop_flags, retries = instrumented_line(module, cleaned, glyph_map)
                total_retries += retries
                pub_tokens = apply_spacing(raw_tokens, drop_flags)
            else:
                raw_tokens, events, drop_flags, retries, pub_tokens = [], [], [], 0, []
            r_lines.append(glyph_line(raw_tokens))
            p_lines.append(glyph_line(pub_tokens))
            t_lines.append({
                "line_index": li,
                "published_cleaned": published_cleaned,
                "effective_plaintext": cleaned,
                "dropped_unsupported": dropped,
                "raw_event_count": len(events),
                "events": events,
                "spacing_drop_flags": drop_flags,
            })
        raw_items.append(b.Item(it.item_id, manuscript, r_lines, None))
        primary.append(b.Item(it.item_id, manuscript, p_lines, None))
        trace_items.append({"item_id": it.item_id, "document": manuscript, "lines": t_lines})
    return primary, raw_items, trace_items, total_retries


def render_trace(trace_items: Sequence[dict], manuscript: str, glyph_map: Mapping[str, str]):
    primary: list[b.Item] = []
    raw_items: list[b.Item] = []
    for it in trace_items:
        p_lines = []
        r_lines = []
        for line in it["lines"]:
            raw_tokens = []
            for ev in line["events"]:
                codes = ev["accepted_codes"]
                raw_tokens.append("".join(glyph_map.get(code, code) for code in codes))
            pub_tokens = apply_spacing(raw_tokens, line["spacing_drop_flags"])
            r_lines.append(glyph_line(raw_tokens))
            p_lines.append(glyph_line(pub_tokens))
        raw_items.append(b.Item(it["item_id"], manuscript, r_lines, None))
        primary.append(b.Item(it["item_id"], manuscript, p_lines, None))
    return primary, raw_items


def pooled(items_by_rep_ms: Mapping[int, Mapping[str, Sequence[b.Item]]]) -> list[b.Item]:
    out = []
    for rep in sorted(items_by_rep_ms):
        for ms in b.PRIMARY_MANUSCRIPTS:
            for it in items_by_rep_ms[rep][ms]:
                out.append(b.Item(f"rep{rep}:{it.item_id}", f"rep{rep}:{ms}", it.lines, it.leaf))
    return out


def hash_order(n: int, axis: str, j: int, group: str) -> list[int]:
    rows = []
    for idx in range(n):
        label = f"issue72v2:stageC:{axis}:{j}:{group}:{idx}".encode("utf-8")
        rows.append((hashlib.sha256(label).digest(), idx))
    rows.sort(key=lambda x: (x[0], x[1]))
    return [idx for _h, idx in rows]


def randomized_map(original: Mapping[str, str], axis: str, j: int) -> tuple[dict[str, str], dict]:
    if axis not in AXES or not (0 <= j < N_ASSIGN):
        raise ValueError("invalid Stage C randomization")
    out = dict(original)
    invariants = {}

    def code(state: str, table: str, letter: str) -> str:
        return f"{state}_{table}_{letter}"

    if axis == "EL":
        order = hash_order(len(EFFECTIVE_LETTERS), axis, j, "global-effective-letter")
        for state in STATES:
            for table in TABLES:
                before = [original[code(state, table, l)] for l in EFFECTIVE_LETTERS]
                for di, letter in enumerate(EFFECTIVE_LETTERS):
                    src_letter = EFFECTIVE_LETTERS[order[di]]
                    out[code(state, table, letter)] = original[code(state, table, src_letter)]
                after = [out[code(state, table, l)] for l in EFFECTIVE_LETTERS]
                if collections.Counter(before) != collections.Counter(after):
                    raise RuntimeError("EL invariant failed")
        invariants["every_table_state_effective_value_multiset_preserved"] = True
        invariants["global_letter_permutation"] = [EFFECTIVE_LETTERS[i] for i in order]

    elif axis == "ES":
        for table in TABLES:
            for letter in EFFECTIVE_LETTERS:
                group = f"{table}|{letter}"
                order = hash_order(len(STATES), axis, j, group)
                before = [original[code(s, table, letter)] for s in STATES]
                for di, state in enumerate(STATES):
                    out[code(state, table, letter)] = before[order[di]]
                after = [out[code(s, table, letter)] for s in STATES]
                if collections.Counter(before) != collections.Counter(after):
                    raise RuntimeError("ES invariant failed")
        invariants["every_table_letter_three_value_multiset_preserved"] = True

    elif axis == "ET":
        for state in STATES:
            for letter in EFFECTIVE_LETTERS:
                group = f"{state}|{letter}"
                order = hash_order(len(TABLES), axis, j, group)
                before = [original[code(state, t, letter)] for t in TABLES]
                for di, table in enumerate(TABLES):
                    out[code(state, table, letter)] = before[order[di]]
                after = [out[code(state, t, letter)] for t in TABLES]
                if collections.Counter(before) != collections.Counter(after):
                    raise RuntimeError("ET invariant failed")
        invariants["every_state_letter_six_value_multiset_preserved"] = True

    elif axis == "EG":
        keys = [code(s, t, l) for s in STATES for t in TABLES for l in EFFECTIVE_LETTERS]
        if len(keys) != 414:
            raise RuntimeError("EG reachable-cell count changed")
        order = hash_order(len(keys), axis, j, "global-effective-cell")
        before = [original[k] for k in keys]
        for di, key in enumerate(keys):
            out[key] = before[order[di]]
        after = [out[k] for k in keys]
        if collections.Counter(before) != collections.Counter(after):
            raise RuntimeError("EG invariant failed")
        invariants["global_414_reachable_value_instance_multiset_preserved"] = True

    effective_keys = [code(s, t, l) for s in STATES for t in TABLES for l in EFFECTIVE_LETTERS]
    changed_cells = sum(out[k] != original[k] for k in effective_keys)
    invariants["effective_cells"] = 414
    invariants["changed_effective_cells"] = int(changed_cells)
    invariants["changed_effective_cell_fraction"] = float(changed_cells / 414)
    excluded = [l for l in tuple("abcdefghijklmnopqrstuvwxyz") if l not in set(EFFECTIVE_LETTERS)]
    invariants["unreachable_jkw_unchanged"] = all(
        out[code(s, t, l)] == original[code(s, t, l)]
        for s in STATES for t in TABLES for l in excluded
    )
    return out, invariants


def ambiguity_diagnostics(module, trace_by_rep_ms, glyph_map: Mapping[str, str]) -> dict:
    unigram = {glyph for code, glyph in glyph_map.items() if code.startswith("unigram_")}
    catalog = module.build_bigram_catalog(module.ALPHABET, module.TABLES, glyph_map)
    bigram = admissible = 0
    for rep in sorted(trace_by_rep_ms):
        for ms in b.PRIMARY_MANUSCRIPTS:
            for it in trace_by_rep_ms[rep][ms]:
                for line in it["lines"]:
                    for ev in line["events"]:
                        if ev["kind"] != "bigram":
                            continue
                        bigram += 1
                        cp, cs = ev["accepted_codes"]
                        combined = glyph_map.get(cp, cp) + glyph_map.get(cs, cs)
                        bad1 = combined in unigram
                        pairs = catalog.get(combined, set())
                        bad2 = any(pair != (cp, cs) for pair in pairs)
                        if not (bad1 or bad2):
                            admissible += 1
    return {
        "bigram_events": int(bigram),
        "admissible_bigram_events": int(admissible),
        "admissible_fraction": float(admissible / bigram) if bigram else None,
        "role": "DIAGNOSTIC_ONLY_NOT_A_REPAIR_OR_ELIGIBILITY_GATE",
    }


def iter_positions(items_by_rep_ms: Mapping[int, Mapping[str, Sequence[b.Item]]]):
    for rep in sorted(items_by_rep_ms):
        for ms in b.PRIMARY_MANUSCRIPTS:
            for it in items_by_rep_ms[rep][ms]:
                for li, line in enumerate(it.lines):
                    for ti, units in enumerate(line):
                        yield rep, ms, it.item_id, li, ti, "".join(units)


def common_support(baseline_by_rep_ms, random_by_rep_ms, parser: e.SlotParser) -> dict:
    bpos = list(iter_positions(baseline_by_rep_ms))
    rpos = list(iter_positions(random_by_rep_ms))
    if len(bpos) != len(rpos):
        raise RuntimeError("fixed-path final position count changed")
    line_rows = []
    line_key = None
    mask_chars = []
    visible = common = base_ok = rand_ok = changed = 0

    def flush():
        nonlocal line_key, mask_chars
        if line_key is not None:
            line_rows.append({
                "rep": line_key[0], "manuscript": line_key[1], "item_id": line_key[2],
                "line_index": line_key[3], "visible_positions": len(mask_chars),
                "common_support_count": mask_chars.count("1"), "mask": "".join(mask_chars),
            })
        line_key = None
        mask_chars = []

    for bp, rp in zip(bpos, rpos):
        if bp[:5] != rp[:5]:
            raise RuntimeError("fixed-path final token positions misaligned")
        key = bp[:4]
        if line_key is None:
            line_key = key
        elif key != line_key:
            flush(); line_key = key
        btok, rtok = bp[5], rp[5]
        visible += 1
        bok = parser.pick(btok, "min") is not None
        rok = parser.pick(rtok, "min") is not None
        base_ok += int(bok); rand_ok += int(rok)
        cok = bool(bok and rok)
        common += int(cok)
        changed += int(btok != rtok)
        mask_chars.append("1" if cok else "0")
    flush()

    mask_payload = canonical_json_bytes(line_rows)
    per_rep = {}
    per_ms = {}
    for row in line_rows:
        rk = f"rep{row['rep']}"
        per_rep.setdefault(rk, {"visible": 0, "common": 0})
        per_rep[rk]["visible"] += row["visible_positions"]
        per_rep[rk]["common"] += row["common_support_count"]
        mk = f"rep{row['rep']}:{row['manuscript']}"
        per_ms.setdefault(mk, {"visible": 0, "common": 0})
        per_ms[mk]["visible"] += row["visible_positions"]
        per_ms[mk]["common"] += row["common_support_count"]
    for d in (per_rep, per_ms):
        for v in d.values():
            v["fraction"] = float(v["common"] / v["visible"]) if v["visible"] else None

    return {
        "visible_positions": int(visible),
        "baseline_parser_accepted": int(base_ok),
        "randomized_parser_accepted": int(rand_ok),
        "common_support_count": int(common),
        "common_support_fraction": float(common / visible) if visible else None,
        "changed_final_token_count": int(changed),
        "changed_final_token_fraction": float(changed / visible) if visible else None,
        "per_rep": per_rep,
        "per_rep_manuscript": per_ms,
        "per_line_counts_and_mask": line_rows,
        "mask_payload_sha256": sha256_bytes(mask_payload),
    }


def write_trace_gzip(path: Path, trace_obj) -> tuple[int, str]:
    raw = canonical_json_bytes(trace_obj) + b"\n"
    with path.open("wb") as fout:
        with gzip.GzipFile(filename="", mode="wb", fileobj=fout, compresslevel=9, mtime=0) as gz:
            gz.write(raw)
    data = path.read_bytes()
    return len(data), sha256_bytes(data)


def main(argv: Sequence[str]) -> int:
    if len(argv) != 5:
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT B2_RAW_JSON OUTPUT_DIR")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    b2_path = Path(argv[3]).resolve()
    outdir = Path(argv[4]).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    if git_head(crem) != EXPECTED_CREMMA or git_head(nai) != EXPECTED_NAIBBE:
        raise RuntimeError("external source authority mismatch")
    b2 = load_b2(b2_path)
    module = n64.load_naibbe(nai)
    original_map = dict(module.placeholder_to_glyph)
    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)
    sources = source_items(crem)

    baseline_primary = {}
    baseline_raw = {}
    traces = {}
    baseline_rows = {}
    trace_manifest = {}

    for rep in REPS:
        baseline_primary[rep] = {}
        baseline_raw[rep] = {}
        traces[rep] = {}
        for mi, manuscript in enumerate(b.PRIMARY_MANUSCRIPTS):
            seed = 6480000 + 100 * mi + rep
            hist_p, hist_r, hist_diag = n64.encrypt_manuscript(module, sources[manuscript], manuscript, original_map, seed)
            inst_p, inst_r, trace, retries = trace_manuscript(module, sources[manuscript], manuscript, original_map, seed)
            rend_p, rend_r = render_trace(trace, manuscript, original_map)
            if surface_sha(hist_p) != surface_sha(inst_p) or surface_sha(hist_r) != surface_sha(inst_r):
                raise RuntimeError(f"rep{rep} {manuscript}: instrumented != historical")
            if surface_sha(rend_p) != surface_sha(inst_p) or surface_sha(rend_r) != surface_sha(inst_r):
                raise RuntimeError(f"rep{rep} {manuscript}: trace renderer != instrumented")
            baseline_primary[rep][manuscript] = inst_p
            baseline_raw[rep][manuscript] = inst_r
            traces[rep][manuscript] = trace
            tpath = outdir / f"trace_rep{rep}_{manuscript}.json.gz"
            gz_size, gz_sha = write_trace_gzip(tpath, {
                "schema": "issue72-v2-stage-c0-accepted-event-trace-v1",
                "rep": rep, "manuscript": manuscript, "seed": seed, "trace": trace,
            })
            trace_manifest[f"rep{rep}:{manuscript}"] = {
                "file": tpath.name, "gzip_size": gz_size, "gzip_sha256": gz_sha, "seed": seed,
                "historical_primary_sha256": surface_sha(hist_p), "historical_raw_sha256": surface_sha(hist_r),
                "instrumented_equals_historical_primary": True, "instrumented_equals_historical_raw": True,
                "trace_render_equals_instrumented_primary": True, "trace_render_equals_instrumented_raw": True,
                "historical_ambiguity_retries": int(hist_diag["ambiguity_retries"]),
                "instrumented_ambiguity_retries": int(retries),
            }
            if int(hist_diag["ambiguity_retries"]) != int(retries):
                raise RuntimeError(f"rep{rep} {manuscript}: retry count mismatch")

        plain_pool = [it for ms in b.PRIMARY_MANUSCRIPTS for it in baseline_primary[rep][ms]]
        plain_sha = surface_sha(plain_pool)
        expected = b2["per_rep"][rep]["surface_sha256"]
        if plain_sha != expected:
            raise RuntimeError(f"rep{rep}: Stage B2 baseline SHA mismatch {plain_sha} != {expected}")
        baseline_rows[f"rep{rep}"] = {
            "pooled_primary_surface_sha256": plain_sha,
            "pooled_raw_surface_sha256": surface_sha([it for ms in b.PRIMARY_MANUSCRIPTS for it in baseline_raw[rep][ms]]),
            "parser_support": parser_support(plain_pool, parser),
        }

    pooled_baseline = pooled(baseline_primary)
    pooled_baseline_support = parser_support(pooled_baseline, parser)

    randomizations = {}
    for axis in AXES:
        randomizations[axis] = {}
        for j in range(N_ASSIGN):
            rmap, invariants = randomized_map(original_map, axis, j)
            random_primary = {}
            for rep in REPS:
                random_primary[rep] = {}
                for manuscript in b.PRIMARY_MANUSCRIPTS:
                    rp, _rr = render_trace(traces[rep][manuscript], manuscript, rmap)
                    random_primary[rep][manuscript] = rp
            pooled_random = pooled(random_primary)
            randomizations[axis][f"r{j}"] = {
                "axis": axis,
                "randomization": j,
                "surface_sha256": surface_sha(pooled_random),
                "parser_support": parser_support(pooled_random, parser),
                "common_support": common_support(baseline_primary, random_primary, parser),
                "ambiguity_legality": ambiguity_diagnostics(module, traces, rmap),
                "invariants": invariants,
                "interpretation_role": "FIXED_REALIZATION_CONDITIONAL_DIRECT_EMISSION_ABLATION",
                "retry_history_not_rerun": True,
                "spacing_mask_not_rerun": True,
            }

    result = {
        "schema": "issue72-v2-stage-c0-fixed-path-support-v1",
        "status": "STAGE C0 FIXED-PATH RANDOMIZATION SUPPORT FROZEN",
        "parent_main": PARENT_MAIN,
        "stage_b2_authority_sha256": EXPECTED_B2_SHA256,
        "external_authority": {"CREMMA_commit": EXPECTED_CREMMA, "Naibbe_commit": EXPECTED_NAIBBE},
        "population": {
            "process_reps": list(REPS), "manuscripts": list(b.PRIMARY_MANUSCRIPTS),
            "axes": list(AXES), "randomizations_per_axis": N_ASSIGN,
            "selection_rule": "ALL_HISTORICAL_REP0_REP4_PATHS_AND_ALL_31_PREDECLARED_ASSIGNMENTS",
        },
        "parser_validation": parser_validation,
        "coverage_policy": "CAUSAL_REPRESENTATIONAL_OUTCOME_NO_HARD_CUTOFF",
        "baseline": {"per_rep": baseline_rows, "pooled_five_path_parser_support": pooled_baseline_support},
        "trace_manifest": trace_manifest,
        "randomization_law": {
            "ordering": "SHA256(issue72v2:stageC:{AXIS}:{j}:{GROUP}:{instance_index})",
            "identity_or_fixed_points_rejected": False, "rerolls_allowed": False,
        },
        "randomizations": randomizations,
        "target_access": {
            "slot_pair_Q_computed": False, "residual_Z_computed": False,
            "ZL3b_or_IT2a_target_loaded": False, "target_topology_correlation_computed": False,
            "R1_pvalue_computed": False, "PT_generated_or_scored": False, "FI_generated_or_scored": False,
        },
    }
    raw = canonical_json_bytes(result) + b"\n"
    (outdir / "stage_c0_support.json").write_bytes(raw)
    manifest = {"stage_c0_support_sha256": sha256_bytes(raw), "stage_c0_support_bytes": len(raw), "trace_manifest": trace_manifest}
    (outdir / "MANIFEST.json").write_bytes(canonical_json_bytes(manifest) + b"\n")
    print(json.dumps({
        "status": result["status"], "support_sha256": sha256_bytes(raw), "support_bytes": len(raw),
        "pooled_baseline_coverage": pooled_baseline_support["coverage"],
        "axis_coverage_ranges": {axis: [min(v["parser_support"]["coverage"] for v in randomizations[axis].values()), max(v["parser_support"]["coverage"] for v in randomizations[axis].values())] for axis in AXES},
        "axis_common_support_ranges": {axis: [min(v["common_support"]["common_support_fraction"] for v in randomizations[axis].values()), max(v["common_support"]["common_support_fraction"] for v in randomizations[axis].values())] for axis in AXES},
        "target_access": result["target_access"],
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
