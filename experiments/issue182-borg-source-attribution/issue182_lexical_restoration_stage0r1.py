#!/usr/bin/env python3
"""Issue #182 Stage 0-R1 score-free Borg lexical restoration audit.

Scientific contract:
  research/ISSUE182_STAGE1_COMPOSABILITY_AND_STAGE0R1_PLAN_20260907.md

This module computes no terminal->initial likelihood or edge gain. It restores
lexical tokens from the official corrected-Latin source using only the source's
whitespace around the physical-line marker `|`, verifies that the same source
reproduces the committed benchmark plaintext under the benchmark's lossy
extraction, and freezes boundary event IDs/classes for later scoring.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

# The Stage-0 module is in the same directory when this script is executed.
import issue182_alignment_stage0 as stage0

PAGE_SPLIT_RE = re.compile(r"^#page\s+", re.MULTILINE)
FOLIO_RE = re.compile(r"^0*(\d+)(r|v)", re.IGNORECASE)
INTRA_WORD_BAR_RE = re.compile(r"(?<=\S)\|(?=\S)")
ALL_BAR_RE = re.compile(r"\s*\|\s*")


def normalize_folio(name: str) -> str:
    m = FOLIO_RE.match(name.strip())
    if not m:
        return name.strip()
    return f"{int(m.group(1)):04d}{m.group(2).lower()}"


def parse_paged_text(text: str) -> dict[str, str]:
    """Reproduce the benchmark creator's #page block parsing convention."""
    pages: dict[str, str] = {}
    parts = PAGE_SPLIT_RE.split(text)[1:]
    for part in parts:
        lines = part.split("\n")
        if not lines:
            continue
        raw_name = lines[0].strip()
        if not raw_name:
            continue
        norm = normalize_folio(raw_name)
        if norm in pages:
            raise RuntimeError(f"duplicate normalized source page: {raw_name!r} -> {norm}")
        pages[norm] = "\n".join(lines[1:]).strip()
    return pages


def extract_latin_lines(combined_text: str) -> list[str]:
    """Reproduce create_borg_benchmark.py's Latin-line selection rule."""
    out: list[str] = []
    for raw in combined_text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if "|" in line or (line.startswith("[") and line.endswith("]")):
            out.append(line)
    return out


def benchmark_lossy_plaintext(combined_text: str) -> str:
    latin_text = " ".join(extract_latin_lines(combined_text))
    latin_text = ALL_BAR_RE.sub(" ", latin_text)
    return latin_text.strip()


def restored_latin_text(combined_text: str) -> str:
    """Restore only source-native no-whitespace line splits.

    A bar immediately flanked by non-whitespace is removed without inserting a
    space. Every other bar (and surrounding whitespace) becomes one space.
    """
    latin_text = " ".join(extract_latin_lines(combined_text))
    latin_text = INTRA_WORD_BAR_RE.sub("", latin_text)
    latin_text = ALL_BAR_RE.sub(" ", latin_text)
    return latin_text.strip()


def restored_tokens(combined_text: str) -> list[str]:
    # Match the first Stage-0 intended solved-Latin normalization after bar
    # restoration: NFC + casefold, retain bracket contents but not delimiters,
    # keep Unicode letters/marks only as lexical characters.
    text = unicodedata.normalize("NFC", restored_latin_text(combined_text)).casefold()
    text = text.replace("[", "").replace("]", "")
    chars: list[str] = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("M"):
            chars.append(ch)
        else:
            chars.append(" ")
    return [x for x in "".join(chars).split() if x]


def stable_boundary_events(
    page_id: str,
    dlines: list[list[stage0.Group]],
    stable: list[int | None],
) -> list[dict]:
    events: list[dict] = []
    for left, right, physical in stage0.immediate_boundaries(dlines):
        events.append(
            {
                "page_id": page_id,
                "left_flat_index": left,
                "right_flat_index": right,
                "physical_relation": physical,
                "boundary_class": stage0.boundary_class(stable[left], stable[right]),
            }
        )
    return events


def align_tokens(
    page_id: str,
    dip_path: Path,
    can_path: Path,
    tokens: list[str],
    symbol_map: dict[str, str],
    cipher_key: dict[str, str],
) -> tuple[dict, list[dict]]:
    dlines = stage0.parse_diplomatic(dip_path, symbol_map, cipher_key)
    clines = stage0.parse_canonical(can_path)
    stage0.verify_canonical(dlines, clines, page_id)
    groups = stage0.flatten(dlines)
    ali = stage0.align_all_optimal(groups, tokens)
    stable = ali["stable_assignment"]
    events = stable_boundary_events(page_id, dlines, stable)
    counts = Counter(f"{e['physical_relation']}|{e['boundary_class']}" for e in events)
    stable_groups = sum(x is not None for x in stable)
    return (
        {
            "page_id": page_id,
            "cipher_group_count": len(groups),
            "plaintext_token_count": len(tokens),
            "global_matched_characters": ali["global_best"][0],
            "global_matched_cipher_groups": ali["global_best"][1],
            "global_matched_plaintext_tokens": ali["global_best"][2],
            "stable_aligned_group_count": stable_groups,
            "ambiguous_or_unassigned_group_count": len(groups) - stable_groups,
            "boundary_counts": dict(sorted(counts.items())),
        },
        events,
    )


def audit(root: Path, official_source: Path) -> dict:
    trans_dir = root / "benchmark/sources/borg/transcriptions"
    plain_dir = root / "benchmark/sources/borg/plaintext"
    meta_path = root / "benchmark/sources/borg/metadata/borg_symbol_map.json"
    meta = json.load(open(meta_path, encoding="utf-8"))
    symbol_map: dict[str, str] = meta["mapping"]
    cipher_key: dict[str, str] = meta["cipher_key"]
    if len(set(cipher_key.values())) != len(cipher_key):
        raise RuntimeError("published cipher key is not one-to-one")

    source_bytes = official_source.read_bytes()
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    source_text = source_bytes.decode("utf-8-sig")
    source_pages = parse_paged_text(source_text)

    ids = stage0.page_ids_from_canonical(trans_dir)
    if len(ids) != 397:
        raise RuntimeError(f"expected 397 non-empty canonical pages, got {len(ids)}")

    source_compat_mismatches: list[str] = []
    restored_pages: list[dict] = []
    all_events: list[dict] = []
    boundary_totals = Counter()
    totals = Counter()
    old_boundary_totals = Counter()
    changed_event_classes = Counter()

    for page_id in ids:
        folio = page_id.removeprefix("borg_")
        combined = source_pages.get(folio)
        committed_path = plain_dir / f"{page_id}.txt"
        dip_path = trans_dir / f"{page_id}.diplomatic.txt"
        can_path = trans_dir / f"{page_id}.canonical.txt"
        if combined is None or not committed_path.exists():
            source_compat_mismatches.append(page_id)
            continue

        reproduced = benchmark_lossy_plaintext(combined)
        committed = committed_path.read_text(encoding="utf-8").strip()
        if reproduced != committed:
            source_compat_mismatches.append(page_id)
            continue

        new_tokens = restored_tokens(combined)
        page_summary, new_events = align_tokens(
            page_id, dip_path, can_path, new_tokens, symbol_map, cipher_key
        )

        # Recompute the original Stage-0 label population deterministically for
        # score-free class-change accounting. No terminal/initial identities are
        # inspected or emitted.
        old_tokens = stage0.normalize_plain_tokens(committed)
        _, old_events = align_tokens(
            page_id, dip_path, can_path, old_tokens, symbol_map, cipher_key
        )
        if len(new_events) != len(old_events):
            raise RuntimeError(f"{page_id}: immediate event population changed structurally")
        for old, new in zip(old_events, new_events):
            if (
                old["left_flat_index"], old["right_flat_index"], old["physical_relation"]
            ) != (
                new["left_flat_index"], new["right_flat_index"], new["physical_relation"]
            ):
                raise RuntimeError(f"{page_id}: immediate event identity mismatch")
            old_key = f"{old['physical_relation']}|{old['boundary_class']}"
            new_key = f"{new['physical_relation']}|{new['boundary_class']}"
            old_boundary_totals[old_key] += 1
            if old["boundary_class"] != new["boundary_class"]:
                changed_event_classes[
                    f"{old['physical_relation']}|{old['boundary_class']}->{new['boundary_class']}"
                ] += 1

        for event in new_events:
            boundary_totals[f"{event['physical_relation']}|{event['boundary_class']}"] += 1
        all_events.extend(new_events)
        restored_pages.append(page_summary)
        for key in (
            "cipher_group_count",
            "plaintext_token_count",
            "global_matched_characters",
            "global_matched_cipher_groups",
            "global_matched_plaintext_tokens",
            "stable_aligned_group_count",
            "ambiguous_or_unassigned_group_count",
        ):
            totals[key] += page_summary[key]

    source_compat_ok = len(source_compat_mismatches) == 0 and len(restored_pages) == 397
    same_lex = boundary_totals["SAME_PHYSICAL_LINE|LEXICAL_BOUNDARY"]
    cross_lex = boundary_totals["CROSS_PHYSICAL_LINE|LEXICAL_BOUNDARY"]
    cross_within = boundary_totals["CROSS_PHYSICAL_LINE|WITHIN_WORD_SPLIT"]
    valid = source_compat_ok and same_lex >= 100 and cross_lex >= 100 and cross_within >= 1

    return {
        "experiment": "Issue #182 Borg Stage0-R1 official-source lexical restoration",
        "edge_gain_computed": False,
        "official_source": {
            "url": "https://www.su.se/download/18.6856063019d24ef3ecb111e/1774945344171/corrected-Latin-translation.txt",
            "sha256": source_sha256,
            "parsed_page_count": len(source_pages),
        },
        "benchmark_authority": {
            "repository": "matthewdgreen/cipher_benchmark",
            "commit": "729aad62d12483c549e64a2541d4f9255538c8cf",
            "page_population": 397,
            "published_cipher_key_size": len(cipher_key),
        },
        "source_compatibility": {
            "exact_reproduced_page_count": 397 - len(source_compat_mismatches),
            "mismatch_count": len(source_compat_mismatches),
            "mismatch_pages": source_compat_mismatches,
        },
        "restored_alignment_totals": dict(totals),
        "old_stage0_boundary_totals_recomputed": dict(sorted(old_boundary_totals.items())),
        "restored_boundary_totals": dict(sorted(boundary_totals.items())),
        "changed_event_classes": dict(sorted(changed_event_classes.items())),
        "support_gate": {
            "source_compatibility_397_of_397": source_compat_ok,
            "same_restored_lexical_boundary_min_100": same_lex >= 100,
            "cross_restored_lexical_boundary_min_100": cross_lex >= 100,
            "cross_within_word_split_recovered_min_1": cross_within >= 1,
        },
        "classification": (
            "LEXICAL_RESTORATION_AUTHORITY_VALID"
            if valid
            else "STAGE0R1_INVALID_OR_INSUFFICIENT"
        ),
        "pages": restored_pages,
        "events": all_events,
    }


def synthetic_preflight() -> None:
    sample = (
        "#page 0002r\n"
        "alpha|beta gamma | delta\n"
        "This is English.\n"
        "#page 007v\n"
        "[Head] epsilon | zeta\n"
    )
    pages = parse_paged_text(sample)
    assert set(pages) == {"0002r", "0007v"}
    assert benchmark_lossy_plaintext(pages["0002r"]) == "alpha beta gamma delta"
    assert restored_tokens(pages["0002r"]) == ["alphabeta", "gamma", "delta"]
    assert restored_tokens(pages["0007v"]) == ["head", "epsilon", "zeta"]
    stage0.synthetic_preflight()
    print("SYNTHETIC_STAGE0R1_PREFLIGHT_OK")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("benchmark_root", nargs="?", type=Path)
    ap.add_argument("official_source", nargs="?", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--synthetic-preflight", action="store_true")
    args = ap.parse_args()
    if args.synthetic_preflight:
        synthetic_preflight()
        return
    if args.benchmark_root is None or args.official_source is None:
        ap.error("benchmark_root and official_source required unless --synthetic-preflight")
    result = audit(args.benchmark_root, args.official_source)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
