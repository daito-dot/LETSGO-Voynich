# Issue #26E14 pre-executable amendment — positive-control identifiability

Status: **FROZEN BEFORE E14 EXECUTABLE / REVEAL**

Parent plan: `PLAN_E14.md` first committed at `0803c49af02ea11b5604a213cf735bafb425acd2`.

## Logical correction

The parent positive-control section required recovery of a hidden `count_slot` label (slot6 vs slot9). That label is a property of the **Voynich representation**, not of the historical Kircher 6×4 cipher itself. A synthetic Kircher event stream has one four-state count coordinate and therefore contains no principled observation that could distinguish the names “slot6” and “slot9.” Requiring recovery of an unobservable label is invalid.

This was caught before any E14 executable or E14 score existed.

## Frozen replacement positive control

The mandatory synthetic control validates the actual finite historical key solver:

1. use frozen supported CREMMA Latin at approximately the eligible Voynich event volume;
2. encode through the exact frozen Kircher 6×4 table;
3. apply a deterministic hidden permutation of the six instrument-row labels;
4. preserve the four count columns exactly in their primary ordinal order;
5. expose only the resulting six-state row + four-state count events;
6. fit all `6! = 720` instrument permutations on training runs using the identical external 4-gram objective;
7. freeze the best key and decode held-out runs.

Run five deterministic hidden-row controls.

PASS requires all:

- exact hidden six-row permutation recovered in >=4/5 controls;
- mean occurrence-weighted decoded-letter accuracy >=`.99`;
- mean recovered held-out 4-gram CE within `.02 bits/char` of the true-key held-out CE.

If this fails: `SOLVER INADEQUATE` and no Voynich negative inference.

## Count-slot selection authority

Whether real Voynich prefers slot6 or slot9 is **not** part of the synthetic solver qualification. It remains a prospective target-side model-selection question and is evaluated only by:

- training-only selection from the two preregistered repeated-unit slots;
- exact `(count_slot, instrument_permutation)` recurrence across the five untouched physical-leaf folds;
- absolute held-out language/readability gates.

All other E14 rules remain unchanged.
