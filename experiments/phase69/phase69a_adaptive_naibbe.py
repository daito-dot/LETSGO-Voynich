#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
PHASE64 = HERE.parent / "phase64"
if str(PHASE64) not in sys.path:
    sys.path.insert(0, str(PHASE64))

import phase64b_naibbe as core  # noqa: E402

CIPHER_REPS = 5
BASE_SEED = 6900000
TIE_EPS = 1e-12


class ModelBlocked(RuntimeError):
    pass


def weighted_choice(candidates: Sequence[Tuple[str, float]], rng: random.Random) -> str:
    if not candidates:
        raise ModelBlocked("empty ciphertext candidate set")
    total = sum(w for _g, w in candidates)
    if total <= 0:
        raise ModelBlocked("non-positive candidate weight total")
    x = rng.random() * total
    acc = 0.0
    for glyph, weight in candidates:
        acc += weight
        if x < acc:
            return glyph
    return candidates[-1][0]


def lev1_str(a: str, b: str) -> bool:
    return core.b.edit1(tuple(a), tuple(b))


def segment_plaintext(cleaned: str, rng: random.Random, respacing: int) -> List[str]:
    text = cleaned.lower().replace(" ", "")
    out: List[str] = []
    i = 0
    while i < len(text):
        if i == len(text) - 1 or rng.random() < (respacing / 36.0):
            out.append(text[i])
            i += 1
        else:
            out.append(text[i:i + 2])
            i += 2
    return out


def respace_tokens(tokens: Sequence[str], rng: random.Random, drop_rate: float) -> List[str]:
    if not tokens:
        return []
    if drop_rate <= 0:
        return list(tokens)
    if drop_rate >= 1:
        return ["".join(tokens)]
    out = [tokens[0]]
    for tok in tokens[1:]:
        if rng.random() < drop_rate:
            out[-1] += tok
        else:
            out.append(tok)
    return out


def build_candidate_catalog(module, glyph_map: Dict[str, str]):
    weights = module.CARD_WEIGHTS[True]
    effective = core.EFFECTIVE_LETTERS

    # Aggregate duplicate glyph realizations, if any, by summing their fixed
    # table weights. The ciphertext token itself, not the table identity, is the
    # emitted object.
    catalog: Dict[str, List[Tuple[str, float]]] = {}
    inverse: Dict[str, set] = defaultdict(set)
    candidate_cardinality = {}

    for letter in effective:
        agg = defaultdict(float)
        for table in module.TABLES:
            code = module.naibbe_tables[table][("unigram", letter)]
            glyph = glyph_map[code]
            agg[glyph] += float(weights[table])
        row = sorted(agg.items())
        if not row:
            raise ModelBlocked(f"no unigram candidates for {letter}")
        catalog[letter] = row
        candidate_cardinality[letter] = len(row)
        for glyph, _weight in row:
            inverse[glyph].add(letter)

    # Published ambiguity rules: not a unigram glyph and no alternative
    # prefix/suffix code pair for the same combined ciphertext string.
    for a in effective:
        for b in effective:
            unit = a + b
            agg = defaultdict(float)
            for tp in module.TABLES:
                pcode = module.naibbe_tables[tp][("prefix", a)]
                pglyph = glyph_map[pcode]
                for ts in module.TABLES:
                    scode = module.naibbe_tables[ts][("suffix", b)]
                    sglyph = glyph_map[scode]
                    combined = pglyph + sglyph
                    if combined in module.unigram_glyphs:
                        continue
                    pairs = module.bigram_catalog.get(combined, set())
                    if any(pair != (pcode, scode) for pair in pairs):
                        continue
                    agg[combined] += float(weights[tp] * weights[ts])
            row = sorted(agg.items())
            if not row:
                raise ModelBlocked(f"no ambiguity-safe bigram candidates for {unit}")
            catalog[unit] = row
            candidate_cardinality[unit] = len(row)
            for glyph, _weight in row:
                inverse[glyph].add(unit)

    return catalog, inverse, candidate_cardinality


def glyph_line(tokens: Sequence[str]) -> core.b.Line:
    return [tuple(x) for x in tokens if x]


def encrypt_manuscript_pair(
    module,
    source_items: Sequence[core.b.Item],
    manuscript: str,
    glyph_map: Dict[str, str],
    mi: int,
    rep: int,
    catalog,
    inverse,
):
    base = BASE_SEED + 100 * mi + rep
    seg_rng = random.Random(base)
    lh0_rng = random.Random(base + 10000)
    lh1_rng = random.Random(base + 20000)
    space0_rng = random.Random(base + 30000)
    space1_rng = random.Random(base + 30000)

    primary0: List[core.b.Item] = []
    primary1: List[core.b.Item] = []
    raw0: List[core.b.Item] = []
    raw1: List[core.b.Item] = []

    diag = {
        "base_seed": base,
        "source_items": len(source_items),
        "source_graphematic_units": 0,
        "published_clean_line_characters": 0,
        "dropped_unsupported_after_clean_line": 0,
        "cleaned_plaintext_characters": 0,
        "plaintext_units": 0,
        "lh1_local_opportunities": 0,
        "lh1_selected_local_hits": 0,
        "lh0_raw_tokens": 0,
        "lh1_raw_tokens": 0,
        "lh0_decode_correct": 0,
        "lh1_decode_correct": 0,
        "decode_total_each_arm": 0,
        "max_recent_history": 0,
    }

    for item in source_items:
        recent1: List[str] = []
        p0_lines = []
        p1_lines = []
        r0_lines = []
        r1_lines = []

        for line in item.lines:
            source = core.string_line(line)
            diag["source_graphematic_units"] += sum(len(tok) for tok in line)
            published_cleaned = module.clean_line(source)
            diag["published_clean_line_characters"] += len(published_cleaned)
            cleaned, dropped = core.project_effective_plaintext(published_cleaned)
            diag["dropped_unsupported_after_clean_line"] += len(dropped)
            diag["cleaned_plaintext_characters"] += len(cleaned)

            units = segment_plaintext(cleaned, seg_rng, module.RESPACING) if cleaned else []
            diag["plaintext_units"] += len(units)
            out0: List[str] = []
            out1: List[str] = []

            for unit in units:
                candidates = catalog.get(unit)
                if not candidates:
                    raise ModelBlocked(f"no candidate catalog entry for plaintext unit {unit!r}")

                g0 = weighted_choice(candidates, lh0_rng)

                local = [
                    (glyph, weight)
                    for glyph, weight in candidates
                    if any(lev1_str(glyph, prev) for prev in recent1[-10:])
                ]
                if local:
                    diag["lh1_local_opportunities"] += 1
                    g1 = weighted_choice(local, lh1_rng)
                    if not any(lev1_str(g1, prev) for prev in recent1[-10:]):
                        raise AssertionError("LH1 selected token missed available edit1 local subset")
                    diag["lh1_selected_local_hits"] += 1
                else:
                    g1 = weighted_choice(candidates, lh1_rng)

                out0.append(g0)
                out1.append(g1)
                recent1.append(g1)
                if len(recent1) > 10:
                    recent1 = recent1[-10:]
                diag["max_recent_history"] = max(diag["max_recent_history"], len(recent1))

                diag["decode_total_each_arm"] += 1
                if inverse.get(g0) == {unit}:
                    diag["lh0_decode_correct"] += 1
                if inverse.get(g1) == {unit}:
                    diag["lh1_decode_correct"] += 1

            diag["lh0_raw_tokens"] += len(out0)
            diag["lh1_raw_tokens"] += len(out1)
            r0_lines.append(glyph_line(out0))
            r1_lines.append(glyph_line(out1))
            # Paired RNG seeds and equal raw-token counts guarantee identical
            # merge/no-merge decisions between the two arms.
            p0_lines.append(glyph_line(respace_tokens(out0, space0_rng, module.SPACE_REMOVAL_RATE)))
            p1_lines.append(glyph_line(respace_tokens(out1, space1_rng, module.SPACE_REMOVAL_RATE)))

        raw0.append(core.b.Item(item.item_id, manuscript, r0_lines, None))
        raw1.append(core.b.Item(item.item_id, manuscript, r1_lines, None))
        primary0.append(core.b.Item(item.item_id, manuscript, p0_lines, None))
        primary1.append(core.b.Item(item.item_id, manuscript, p1_lines, None))

    denom = diag["decode_total_each_arm"]
    diag["lh0_decode_accuracy"] = diag["lh0_decode_correct"] / denom if denom else None
    diag["lh1_decode_accuracy"] = diag["lh1_decode_correct"] / denom if denom else None
    diag["lh1_opportunity_fraction"] = (
        diag["lh1_local_opportunities"] / denom if denom else 0.0
    )
    diag["lh1_selected_hit_fraction"] = (
        diag["lh1_selected_local_hits"] / denom if denom else 0.0
    )
    if diag["lh1_local_opportunities"] != diag["lh1_selected_local_hits"]:
        raise AssertionError("LH1 opportunity/selected-hit mismatch")
    if diag["lh0_decode_accuracy"] != 1.0 or diag["lh1_decode_accuracy"] != 1.0:
        raise ModelBlocked(
            f"raw-token reversibility failure: LH0={diag['lh0_decode_accuracy']} LH1={diag['lh1_decode_accuracy']}"
        )

    return {
        "LH0": {"primary": primary0, "raw": raw0},
        "LH1": {"primary": primary1, "raw": raw1},
        "diagnostics": diag,
    }


def aggregate_arm(per_ms, arm, view):
    ms_aggs = {
        ms: core.aggregate_realizations(
            reps,
            f"Phase69:{arm}:{ms}:{view}",
        )
        for ms, reps in per_ms[arm][view].items()
    }
    return {
        "per_manuscript": ms_aggs,
        "aggregate": core.aggregate_manuscripts(ms_aggs, f"Phase69:{arm}:{view}:equal-manuscript"),
    }


def compute(voynich_path: Path, cremma_root: Path, naibbe_root: Path) -> dict:
    ccommit = core.b.verify_cremma_commit(cremma_root)
    module = core.load_naibbe(naibbe_root)
    original_map = dict(module.placeholder_to_glyph)
    core.set_glyph_map(module, original_map)

    effective_required_codes = {
        f"{state}_{table}_{letter}"
        for state in module.STATES
        for table in module.TABLES
        for letter in core.EFFECTIVE_LETTERS
    }
    if set(original_map) != effective_required_codes or len(original_map) != 414:
        raise ModelBlocked("published effective Naibbe codebook differs from Phase64B authority")

    catalog, inverse, cardinality = build_candidate_catalog(module, original_map)
    ambiguous_raw_tokens = {g: sorted(v) for g, v in inverse.items() if len(v) != 1}
    if ambiguous_raw_tokens:
        raise ModelBlocked(
            "raw ciphertext catalog is not uniquely reversible: "
            + json.dumps(dict(list(ambiguous_raw_tokens.items())[:10]), ensure_ascii=False)
        )

    phase62c = json.loads((core.PHASE62 / "phase62c_c0_a1_results.json").read_text(encoding="utf-8"))
    phase63a = json.loads((core.PHASE63 / "phase63a_training_vocab_results.json").read_text(encoding="utf-8"))
    if core.sha256_file(core.PHASE62 / "phase62p_h62p1_results.json") != core.PHASE62P_SHA256:
        raise RuntimeError("Phase62P authority digest mismatch")
    if core.sha256_file(core.PHASE63 / "phase63a_training_vocab_results.json") != core.PHASE63A_SHA256:
        raise RuntimeError("Phase63A authority digest mismatch")
    contexts, _ = core.fold_contexts(voynich_path, phase62c, phase63a)

    raw_sources = {
        name: core.b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in core.b.PRIMARY_MANUSCRIPTS.items()
    }

    per_ms = {
        "LH0": {"primary": {}, "raw": {}},
        "LH1": {"primary": {}, "raw": {}},
    }
    diagnostics = {}

    for mi, manuscript in enumerate(core.MANUSCRIPTS):
        diagnostics[manuscript] = {}
        for r in range(CIPHER_REPS):
            pair = encrypt_manuscript_pair(
                module,
                raw_sources[manuscript],
                manuscript,
                original_map,
                mi,
                r,
                catalog,
                inverse,
            )
            diagnostics[manuscript][f"rep{r}"] = pair["diagnostics"]
            # Use the same scientific label across paired arms so S2/H62 null
            # shuffles use paired seeds. The data differ; the null RNG does not.
            primary_label = f"Phase69:paired:{manuscript}:rep{r}:primary"
            raw_label = f"Phase69:paired:{manuscript}:rep{r}:raw"
            for arm in ("LH0", "LH1"):
                per_ms[arm]["primary"].setdefault(manuscript, {})[f"rep{r}"] = core.output_metrics(
                    pair[arm]["primary"], primary_label, contexts
                )
                per_ms[arm]["raw"].setdefault(mancript if False else manuscript, {})[f"rep{r}"] = core.output_metrics(
                    pair[arm]["raw"], raw_label, contexts
                )

    arms = {}
    for arm in ("LH0", "LH1"):
        primary = aggregate_arm(per_ms, arm, "primary")
        raw = aggregate_arm(per_ms, arm, "raw")
        primary_eval = core.evaluate_aggregate(primary["aggregate"], contexts, phase63a, f"Phase69:{arm}:primary")
        raw_eval = core.evaluate_aggregate(raw["aggregate"], contexts, phase63a, f"Phase69:{arm}:raw")
        arms[arm] = {
            "primary": primary,
            "primary_evaluation": primary_eval,
            "raw": raw,
            "raw_evaluation": raw_eval,
        }

    c1 = json.loads((PHASE64 / "phase64b_science_results.json").read_text(encoding="utf-8"))
    c1_eval = c1["published_mapping"]["primary_evaluation"]

    lh0 = arms["LH0"]["primary_evaluation"]
    lh1 = arms["LH1"]["primary_evaluation"]
    mechanism = {
        "LH1_S2_strictly_higher_than_LH0": (
            lh1["candidate_exposed_mean"]["S2"] > lh0["candidate_exposed_mean"]["S2"] + TIE_EPS
        ),
        "LH1_mean_abs_C_short_diff_lower_than_LH0": (
            lh1["H62P1_summary"]["mean_abs_C_short_diff"] + TIE_EPS
            < lh0["H62P1_summary"]["mean_abs_C_short_diff"]
        ),
        "LH1_mean_D_profile_lower_than_LH0": (
            lh1["H62P1_summary"]["mean_D_profile"] + TIE_EPS
            < lh0["H62P1_summary"]["mean_D_profile"]
        ),
    }
    mechanism["pass"] = all(mechanism.values())

    vs_c1 = {
        "LH1_S2_higher": lh1["candidate_exposed_mean"]["S2"] > c1_eval["candidate_exposed_mean"]["S2"] + TIE_EPS,
        "LH1_mean_D_lower": lh1["H62P1_summary"]["mean_D_profile"] + TIE_EPS < c1_eval["H62P1_summary"]["mean_D_profile"],
        "LH1_mean_abs_C_short_diff_lower": lh1["H62P1_summary"]["mean_abs_C_short_diff"] + TIE_EPS < c1_eval["H62P1_summary"]["mean_abs_C_short_diff"],
    }

    if not mechanism["pass"]:
        classification = "C2-LH1 NOT COMPETITIVE — LOCAL ADAPTATION DID NOT PRODUCE THE PREDICTED STRUCTURE"
    elif lh1["A1_R1_rival"]:
        classification = "C2-LH1 H62 RIVAL TO A1-R1 — DEVELOPMENTAL"
    elif lh1["structurally_viable"]:
        classification = "C2-LH1 STRUCTURALLY VIABLE MEANINGFUL-TEXT OBFUSCATION MODEL — DEVELOPMENTAL"
    else:
        classification = "C2-LH1 LOCALITY-ONLY PARTIAL"

    total_diag = Counter()
    opportunity_fracs = []
    for ms in diagnostics.values():
        for d in ms.values():
            for k in (
                "source_graphematic_units", "published_clean_line_characters",
                "dropped_unsupported_after_clean_line", "cleaned_plaintext_characters",
                "plaintext_units", "lh1_local_opportunities", "lh1_selected_local_hits",
                "lh0_raw_tokens", "lh1_raw_tokens", "lh0_decode_correct",
                "lh1_decode_correct", "decode_total_each_arm",
            ):
                total_diag[k] += d[k]
            opportunity_fracs.append(d["lh1_opportunity_fraction"])

    return {
        "phase": "69A",
        "hypothesis": "P69-C2-LH1 meaningful plaintext + context-adaptive homophonic obfuscation",
        "classification": classification,
        "inputs": {
            "voynich_git_blob_sha1": core.b.git_blob_sha1(voynich_path.read_bytes()),
            "cremma_commit": ccommit,
            "manuscripts_equal_weight": list(core.MANUSCRIPTS),
            "naibbe_commit": core.NAIBBE_COMMIT,
            "naibbe_v2_blob": core.NAIBBE_PY_BLOB,
            "naibbe_tables_blob": core.NAIBBE_TABLE_BLOB,
            "effective_codebook_cells": len(original_map),
            "candidate_catalog_plaintext_units": len(catalog),
            "candidate_cardinality_summary": {
                "min": min(cardinality.values()),
                "max": max(cardinality.values()),
                "mean": float(np.mean(list(cardinality.values()))),
            },
            "realizations_per_manuscript": CIPHER_REPS,
            "base_seed_formula": "6900000 + 100*manuscript_index + realization",
        },
        "reversibility_and_utilization": {
            "aggregate_counts": dict(total_diag),
            "LH0_decode_accuracy": total_diag["lh0_decode_correct"] / total_diag["decode_total_each_arm"],
            "LH1_decode_accuracy": total_diag["lh1_decode_correct"] / total_diag["decode_total_each_arm"],
            "LH1_opportunity_fraction_global": total_diag["lh1_local_opportunities"] / total_diag["decode_total_each_arm"],
            "LH1_selected_hit_fraction_global": total_diag["lh1_selected_local_hits"] / total_diag["decode_total_each_arm"],
            "LH1_mean_realization_opportunity_fraction": float(np.mean(opportunity_fracs)),
            "per_manuscript_realization": diagnostics,
        },
        "arms": arms,
        "local_adaptation_mechanism_check": mechanism,
        "descriptive_comparison_to_sealed_published_C1_E0": vs_c1,
        "sealed_C1_E0_reference": {
            "S2": c1_eval["candidate_exposed_mean"]["S2"],
            "mean_D_profile": c1_eval["H62P1_summary"]["mean_D_profile"],
            "mean_abs_C_short_diff": c1_eval["H62P1_summary"]["mean_abs_C_short_diff"],
        },
        "claim_limit": "developmental mechanism-compatibility test only; context-adaptive edit1 homophone choice is not historically established and no plaintext/decipherment claim is authorized",
    }


def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt /path/to/CREMMA-Medieval-LAT /path/to/naibbe-cipher", file=sys.stderr)
        return 2
    voynich_path = Path(sys.argv[1]).resolve()
    cremma_root = Path(sys.argv[2]).resolve()
    naibbe_root = Path(sys.argv[3]).resolve()

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        out = compute(voynich_path, cremma_root, naibbe_root)
    stdout = captured.getvalue()
    out["execution_stdout_audit"] = {
        "captured_characters": len(stdout),
        "sha256": hashlib.sha256(stdout.encode("utf-8")).hexdigest(),
        "used_for_scoring": False,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
