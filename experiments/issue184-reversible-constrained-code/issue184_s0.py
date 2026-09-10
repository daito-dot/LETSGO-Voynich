from __future__ import annotations

import hashlib
import json
import math
from collections import Counter

SLOTS = (
    ("q", "s", "d"), ("o", "y"), ("l", "r"), ("t", "k", "p", "f"),
    ("ch", "sh"), ("cth", "ckh", "cph", "cfh"), ("e", "ee", "eee"),
    ("s", "d"), ("o", "a"), ("i", "ii", "iii"),
    ("d", "l", "r", "m", "n"), ("y",),
)


class SlotParser:
    def __init__(self):
        self.cache = {}

    def parses(self, token):
        token = token.lower()
        if token in self.cache:
            return self.cache[token]
        out, vals = [], [""] * 12

        def rec(pos, next_slot, sig):
            if pos == len(token):
                out.append((tuple(sig), tuple(vals)))
                return
            for slot in range(next_slot, 12):
                for value in sorted(SLOTS[slot], key=lambda x: (-len(x), x)):
                    if token.startswith(value, pos):
                        vals[slot] = value
                        sig.append(slot)
                        rec(pos + len(value), slot + 1, sig)
                        sig.pop()
                        vals[slot] = ""

        rec(0, 0, [])
        out.sort(key=lambda x: x[0])
        self.cache[token] = out
        return out

    def pick(self, token, policy):
        ps = self.parses(token)
        if not ps:
            return None
        return ps[0] if policy == "min" else ps[-1]


def validate_parser(parser):
    expected = {
        "otedy": ("1-3-6-7-11", "1-3-6-10-11"),
        "okal": ("1-3-8-10", "1-3-8-10"),
        "okol": ("1-3-8-10", "1-3-8-10"),
        "otchdy": ("1-3-4-7-11", "1-3-4-10-11"),
        "qokedy": ("0-1-3-6-7-11", "0-1-3-6-10-11"),
        "chedy": ("4-6-7-11", "4-6-10-11"),
        "y": ("1", "11"),
        "d": ("0", "10"),
        "dain": ("0-8-9-10", "7-8-9-10"),
        "daiin": ("0-8-9-10", "7-8-9-10"),
    }
    got = {}
    for tok, exp in expected.items():
        a, b = parser.pick(tok, "min"), parser.pick(tok, "max")
        if a is None or b is None:
            raise RuntimeError(f"validation token unparseable: {tok}")
        pair = ("-".join(map(str, a[0])), "-".join(map(str, b[0])))
        got[tok] = {"min": pair[0], "max": pair[1]}
        if pair != exp:
            raise RuntimeError(f"validation mismatch {tok}: {pair} != {exp}")
    return got


slot_cardinalities = [len(x) for x in SLOTS]
n_paths = math.prod(1 + n for n in slot_cardinalities) - 1

# Exact dynamic enumeration of structural-path multiplicity per literal surface.
# Start with the all-ABSENT path and remove it after all 12 slots are traversed.
counts = {"": 1}
for vals in SLOTS:
    nxt = {}
    for prefix, mult in counts.items():
        nxt[prefix] = nxt.get(prefix, 0) + mult
        for value in vals:
            surface = prefix + value
            nxt[surface] = nxt.get(surface, 0) + mult
    counts = nxt

empty_mult = counts.pop("")
assert empty_mult == 1
assert sum(counts.values()) == n_paths

u_count = len(counts)
collision_count = n_paths - u_count
multi_surface_count = sum(1 for m in counts.values() if m > 1)
max_parse_multiplicity = max(counts.values())
parse_mult_hist = Counter(counts.values())
length_dist = Counter(map(len, counts.keys()))
k = u_count.bit_length() - 1

# Frozen deterministic practical audit: S0-16 when available, otherwise S0-8.
if u_count >= 65536:
    codebook = sorted(counts.keys())[:65536]
    view_bits = 16
elif u_count >= 256:
    codebook = sorted(counts.keys())[:256]
    view_bits = 8
else:
    codebook = []
    view_bits = 0

parser = SlotParser()
parser_validation = validate_parser(parser)
accepted = 0
roundtrip = 0
inverse = {surface: i for i, surface in enumerate(codebook)}
for i, surface in enumerate(codebook):
    if parser.pick(surface, "min") is not None:
        accepted += 1
    if inverse.get(surface) == i:
        roundtrip += 1

codebook_bytes = ("\n".join(codebook) + ("\n" if codebook else "")).encode("utf-8")
codebook_sha256 = hashlib.sha256(codebook_bytes).hexdigest()

if u_count >= 65536 and roundtrip == 65536 and accepted == 65536:
    classification = "S0_CAPACITY_16PLUS_EXACT"
elif 256 <= u_count < 65536 and roundtrip == 256 and accepted == 256:
    classification = "S0_CAPACITY_8_TO_15_EXACT"
elif u_count < 256:
    classification = "S0_INSUFFICIENT_BYTE_CAPACITY"
else:
    classification = "S0_INVALID"

result = {
    "issue": 184,
    "working_identifier": "RC-A0",
    "classification": classification,
    "slot_cardinalities": slot_cardinalities,
    "slot_value_total": sum(slot_cardinalities),
    "n_paths": n_paths,
    "distinct_literal_surfaces": u_count,
    "collision_count": collision_count,
    "multi_parse_surface_count": multi_surface_count,
    "multi_parse_surface_fraction": multi_surface_count / u_count,
    "max_structural_parse_multiplicity": max_parse_multiplicity,
    "parse_multiplicity_histogram": {str(m): n for m, n in sorted(parse_mult_hist.items())},
    "floor_log2_distinct_surfaces": k,
    "distinct_surface_length_distribution": {str(length): n for length, n in sorted(length_dist.items())},
    "codebook_view_bits": view_bits,
    "codebook_size": len(codebook),
    "codebook_sha256": codebook_sha256,
    "codebook_first": codebook[:10],
    "codebook_last": codebook[-10:],
    "roundtrip_ok": roundtrip,
    "parser_acceptance_ok": accepted,
    "parser_validation": parser_validation,
    "voynich_corpus_accessed": False,
    "g7a_v2_probabilities_accessed": False,
    "r1_r8_scientific_score_computed": False,
}
canonical = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
result["canonical_result_sha256"] = hashlib.sha256(canonical).hexdigest()

print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
with open("issue184_s0_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=True)
    f.write("\n")
