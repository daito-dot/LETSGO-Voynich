#!/usr/bin/env python3
"""Issue #184 S0: exact reversible capacity of the frozen SlotParser language.

This executable intentionally has no Voynich corpus input.  Its only scientific
input is the already-frozen `SLOTS`/`SlotParser` adapter definition.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
ISSUE26 = HERE.parents[1] / "issue26-music"
if str(ISSUE26) not in sys.path:
    sys.path.insert(0, str(ISSUE26))

import issue26e_core as core  # noqa: E402


def raw_path_count(slots) -> int:
    return math.prod(1 + len(x) for x in slots) - 1


def enumerate_surfaces(slots):
    """Return the distinct literal language and surfaces with >1 slot path."""
    surfaces: set[str] = set()
    ambiguous: set[str] = set()
    enumerated = 0
    choices = [(None,) + tuple(values) for values in slots]
    for picked in itertools.product(*choices):
        if all(x is None for x in picked):
            continue
        enumerated += 1
        surface = "".join(x for x in picked if x is not None)
        if surface in surfaces:
            ambiguous.add(surface)
        else:
            surfaces.add(surface)
    return surfaces, ambiguous, enumerated


def codebook_digest(codebook: list[str]) -> str:
    h = hashlib.sha256()
    for s in codebook:
        h.update(s.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def exhaustive_view(surfaces: set[str], parser: core.SlotParser, width: int) -> dict:
    n = 1 << width
    codebook = sorted(surfaces)[:n]
    if len(codebook) != n:
        raise RuntimeError(f"requested {width}-bit view but only {len(codebook)} surfaces exist")
    inverse = {s: i for i, s in enumerate(codebook)}
    if len(inverse) != n:
        raise RuntimeError("codebook is not injective")

    accepted = 0
    roundtrip = 0
    ambiguous_parse = 0
    signature_counts = Counter()
    slot_presence = Counter()
    for i, s in enumerate(codebook):
        parses = parser.parses(s)
        if parses:
            accepted += 1
            chosen = parser.pick(s, "min")
            if chosen is None:
                raise RuntimeError("parser.parses nonempty but pick(min) failed")
            signature_counts["-".join(map(str, chosen[0]))] += 1
            for slot in chosen[0]:
                slot_presence[str(slot)] += 1
        if len(parses) > 1:
            ambiguous_parse += 1
        encoded = codebook[i]
        decoded = inverse.get(encoded)
        if decoded == i:
            roundtrip += 1

    return {
        "width_bits": width,
        "codeword_count": n,
        "codebook_sha256_newline_utf8": codebook_digest(codebook),
        "parser_accepted": accepted,
        "roundtrip_exact": roundtrip,
        "ambiguous_parser_codewords": ambiguous_parse,
        "distinct_min_parse_signatures": len(signature_counts),
        "min_parse_slot_presence": dict(sorted(slot_presence.items(), key=lambda kv: int(kv[0]))),
        "first_20_codewords": codebook[:20],
        "last_20_codewords": codebook[-20:],
    }


def synthetic_preflight() -> None:
    tiny = (("a", "b"), ("c",), ("a",))
    surfaces, ambiguous, enumerated = enumerate_surfaces(tiny)
    assert enumerated == raw_path_count(tiny) == 11
    # slot0='a' and slot2='a' collide as literal 'a'
    assert "a" in ambiguous
    assert len(surfaces) < enumerated
    print("SYNTHETIC_ISSUE184_S0_OK")


def run() -> dict:
    slots = core.SLOTS
    analytical = raw_path_count(slots)
    surfaces, ambiguous, enumerated = enumerate_surfaces(slots)
    if enumerated != analytical:
        raise RuntimeError(f"path enumeration mismatch: {enumerated} != {analytical}")
    if not surfaces:
        raise RuntimeError("empty surface language")

    n_unique = len(surfaces)
    k = int(math.floor(math.log2(n_unique)))
    length_dist = Counter(len(s) for s in surfaces)
    parser = core.SlotParser()
    core.validate_parser(parser)

    view = None
    if n_unique >= 65536:
        width = 16
        view = exhaustive_view(surfaces, parser, width)
        exact = view["roundtrip_exact"] == 65536 and view["parser_accepted"] == 65536
        classification = "S0_CAPACITY_16PLUS_EXACT" if exact else "S0_INVALID"
    elif n_unique >= 256:
        width = 8
        view = exhaustive_view(surfaces, parser, width)
        exact = view["roundtrip_exact"] == 256 and view["parser_accepted"] == 256
        classification = "S0_CAPACITY_8_TO_15_EXACT" if exact else "S0_INVALID"
    else:
        classification = "S0_INSUFFICIENT_BYTE_CAPACITY"

    return {
        "experiment": "Issue #184 S0 reversible SlotParser-language capacity",
        "role": "CONTROL / TARGET-AWARE UPPER BOUND",
        "voynich_corpus_accessed": False,
        "g7a_v2_probabilities_accessed": False,
        "r1_r8_scientific_score_computed": False,
        "adapter_authority": {
            "file": "experiments/issue26-music/issue26e_core.py",
            "slots": [list(x) for x in slots],
            "slot_cardinalities": [len(x) for x in slots],
            "total_slot_values": sum(len(x) for x in slots),
            "parser_policy_for_audit": "min",
        },
        "raw_structural_path_count": analytical,
        "distinct_literal_surface_count": n_unique,
        "path_collision_excess": analytical - n_unique,
        "ambiguous_literal_surface_count": len(ambiguous),
        "ambiguous_literal_surface_fraction": len(ambiguous) / n_unique,
        "support_capacity_floor_bits_per_token": k,
        "literal_codepoint_length_distribution": {str(x): length_dist[x] for x in sorted(length_dist)},
        "exhaustive_fixed_block_view": view,
        "classification": classification,
        "interpretation": "support-level exact reversibility only; not an R2 topology pass",
    }


def main() -> None:
    if "--synthetic-preflight" in sys.argv:
        synthetic_preflight()
        return
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    result = run()
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if out:
        out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
