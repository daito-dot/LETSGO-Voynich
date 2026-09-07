#!/usr/bin/env python3
"""Issue #184 S0-R1: canonical SlotParser(min) representative for every mask.

No Voynich corpus or fitted G7A probabilities are read.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
ISSUE26 = HERE.parents[1] / "issue26-music"
if str(ISSUE26) not in sys.path:
    sys.path.insert(0, str(ISSUE26))
import issue26e_core as core  # noqa: E402


def signature(mask: int) -> tuple[int, ...]:
    return tuple(s for s in range(12) if (mask >> s) & 1)


def find_representative(parser: core.SlotParser, mask: int):
    sig = signature(mask)
    value_sets = [core.SLOTS[s] for s in sig]
    best = None
    trials = 0
    for values in itertools.product(*value_sets):
        trials += 1
        surface = "".join(values)
        p = parser.pick(surface, "min")
        if p is not None and p[0] == sig:
            if best is None or surface < best:
                best = surface
    return best, trials


def table_sha(rows) -> str:
    h = hashlib.sha256()
    for r in rows:
        line = f"{r['mask']}\t{r['signature']}\t{r['surface']}\n"
        h.update(line.encode("utf-8"))
    return h.hexdigest()


def synthetic_preflight() -> None:
    # The real parser has well-known ambiguous singleton values: 'd' can be
    # slot 0/7/10 and 'y' slot 1/11 under min parsing.
    p = core.SlotParser()
    core.validate_parser(p)
    assert p.pick("d", "min")[0] == (0,)
    assert p.pick("y", "min")[0] == (1,)
    print("SYNTHETIC_ISSUE184_S0R1_OK")


def run() -> dict:
    parser = core.SlotParser()
    core.validate_parser(parser)
    rows = []
    missing = []
    trials_total = 0
    length_dist = Counter()
    for mask in range(1, 1 << 12):
        surface, trials = find_representative(parser, mask)
        trials_total += trials
        sig = signature(mask)
        if surface is None:
            missing.append({"mask": mask, "signature": list(sig), "trials": trials})
        else:
            check = parser.pick(surface, "min")
            if check is None or check[0] != sig:
                raise RuntimeError(f"closure failure mask={mask} surface={surface!r}")
            length_dist[len(surface)] += 1
            rows.append({
                "mask": mask,
                "signature": list(sig),
                "surface": surface,
                "trials": trials,
            })

    classification = (
        "S0R1_FULL_CANONICAL_MASK_COVERAGE"
        if len(rows) == 4095
        else "S0R1_PARTIAL_CANONICAL_MASK_COVERAGE"
    )
    return {
        "experiment": "Issue #184 S0-R1 canonical occupancy-mask representability",
        "voynich_corpus_accessed": False,
        "g7a_probabilities_accessed": False,
        "r2_scientific_score_computed": False,
        "mask_population": 4095,
        "represented_mask_count": len(rows),
        "missing_mask_count": len(missing),
        "coverage_fraction": len(rows) / 4095,
        "search_trials_total": trials_total,
        "representative_length_distribution": {str(k): length_dist[k] for k in sorted(length_dist)},
        "representative_table_sha256": table_sha(rows),
        "classification": classification,
        "missing_masks": missing,
        "representatives": rows,
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
        print(text)


if __name__ == "__main__":
    main()
