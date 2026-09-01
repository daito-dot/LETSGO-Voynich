#!/usr/bin/env python3
"""Target-blind implementation recovery wrapper for Issue #72 V2 Stage C1.

The frozen C0 mask universe contains token-bearing lines only because it was
constructed from token positions. The original C1 scorer included empty lines
in its reconstruction lookup. This wrapper changes only that lookup domain:
empty reconstructed lines are omitted, matching C0 exactly.

No R1 statistic, target loading, null namespace, support mask, axis,
assignment, or scientific interpretation is changed.
"""
from __future__ import annotations

import sys

import c1_r1_target72_v2 as base


def nonempty_line_lookup(items_by_rep_ms):
    out = {}
    for rep in base.REPS:
        for ms in base.MANUSCRIPTS:
            for it in items_by_rep_ms[rep][ms]:
                for li, line in enumerate(it.lines):
                    if len(line) == 0:
                        continue
                    key = (rep, ms, it.item_id, int(li))
                    if key in out:
                        raise RuntimeError(f"duplicate nonempty line key {key}")
                    out[key] = line
    return out


base.line_lookup = nonempty_line_lookup

if __name__ == "__main__":
    raise SystemExit(base.main(sys.argv))
