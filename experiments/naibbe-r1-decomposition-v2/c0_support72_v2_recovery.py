#!/usr/bin/env python3
"""Invariant-only recovery wrapper for Issue #72 V2 Stage C0.

The original C0 implementation failed before target access because its final
unreachable-j/k/w diagnostic directly indexed keys that are absent from the
pinned Naibbe mapping. This wrapper preserves the exact preregistered EL/ES/ET/EG
randomization laws and replaces only that domain check: existing unreachable
keys must retain their value and absent unreachable keys must remain absent.

No target statistic is added or changed here.
"""
from __future__ import annotations

import collections
import sys

import c0_support72_v2 as base


def randomized_map_recovery(original, axis: str, j: int):
    if axis not in base.AXES or not (0 <= j < base.N_ASSIGN):
        raise ValueError("invalid Stage C randomization")
    out = dict(original)
    invariants = {}

    def code(state: str, table: str, letter: str) -> str:
        return f"{state}_{table}_{letter}"

    if axis == "EL":
        order = base.hash_order(len(base.EFFECTIVE_LETTERS), axis, j, "global-effective-letter")
        for state in base.STATES:
            for table in base.TABLES:
                before = [original[code(state, table, l)] for l in base.EFFECTIVE_LETTERS]
                for di, letter in enumerate(base.EFFECTIVE_LETTERS):
                    src_letter = base.EFFECTIVE_LETTERS[order[di]]
                    out[code(state, table, letter)] = original[code(state, table, src_letter)]
                after = [out[code(state, table, l)] for l in base.EFFECTIVE_LETTERS]
                if collections.Counter(before) != collections.Counter(after):
                    raise RuntimeError("EL invariant failed")
        invariants["every_table_state_effective_value_multiset_preserved"] = True
        invariants["global_letter_permutation"] = [base.EFFECTIVE_LETTERS[i] for i in order]

    elif axis == "ES":
        for table in base.TABLES:
            for letter in base.EFFECTIVE_LETTERS:
                group = f"{table}|{letter}"
                order = base.hash_order(len(base.STATES), axis, j, group)
                before = [original[code(s, table, letter)] for s in base.STATES]
                for di, state in enumerate(base.STATES):
                    out[code(state, table, letter)] = before[order[di]]
                after = [out[code(s, table, letter)] for s in base.STATES]
                if collections.Counter(before) != collections.Counter(after):
                    raise RuntimeError("ES invariant failed")
        invariants["every_table_letter_three_value_multiset_preserved"] = True

    elif axis == "ET":
        for state in base.STATES:
            for letter in base.EFFECTIVE_LETTERS:
                group = f"{state}|{letter}"
                order = base.hash_order(len(base.TABLES), axis, j, group)
                before = [original[code(state, t, letter)] for t in base.TABLES]
                for di, table in enumerate(base.TABLES):
                    out[code(state, table, letter)] = before[order[di]]
                after = [out[code(state, t, letter)] for t in base.TABLES]
                if collections.Counter(before) != collections.Counter(after):
                    raise RuntimeError("ET invariant failed")
        invariants["every_state_letter_six_value_multiset_preserved"] = True

    elif axis == "EG":
        keys = [
            code(s, t, l)
            for s in base.STATES
            for t in base.TABLES
            for l in base.EFFECTIVE_LETTERS
        ]
        if len(keys) != 414:
            raise RuntimeError("EG reachable-cell count changed")
        order = base.hash_order(len(keys), axis, j, "global-effective-cell")
        before = [original[k] for k in keys]
        for di, key in enumerate(keys):
            out[key] = before[order[di]]
        after = [out[k] for k in keys]
        if collections.Counter(before) != collections.Counter(after):
            raise RuntimeError("EG invariant failed")
        invariants["global_414_reachable_value_instance_multiset_preserved"] = True

    effective_keys = [
        code(s, t, l)
        for s in base.STATES
        for t in base.TABLES
        for l in base.EFFECTIVE_LETTERS
    ]
    changed_cells = sum(out[k] != original[k] for k in effective_keys)
    invariants["effective_cells"] = 414
    invariants["changed_effective_cells"] = int(changed_cells)
    invariants["changed_effective_cell_fraction"] = float(changed_cells / 414)

    excluded = [
        l for l in tuple("abcdefghijklmnopqrstuvwxyz")
        if l not in set(base.EFFECTIVE_LETTERS)
    ]
    unreachable_keys = [
        code(s, t, l)
        for s in base.STATES
        for t in base.TABLES
        for l in excluded
    ]
    present = [k for k in unreachable_keys if k in original]
    absent = [k for k in unreachable_keys if k not in original]
    if not all(out.get(k) == original[k] for k in present):
        raise RuntimeError("present unreachable j/k/w cell changed")
    if not all(k not in out for k in absent):
        raise RuntimeError("absent unreachable j/k/w cell was introduced")
    invariants["unreachable_jkw_unchanged"] = True
    invariants["unreachable_jkw_present_key_count"] = len(present)
    invariants["unreachable_jkw_absent_key_count"] = len(absent)
    invariants["unreachable_jkw_domain_semantics"] = "PRESENT_VALUES_UNCHANGED_AND_ABSENT_KEYS_REMAIN_ABSENT"
    return out, invariants


base.randomized_map = randomized_map_recovery

if __name__ == "__main__":
    raise SystemExit(base.main(sys.argv))
