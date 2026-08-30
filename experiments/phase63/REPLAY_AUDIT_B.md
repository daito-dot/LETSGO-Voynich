# Phase 63B clean replay audit

Status: **exact raw-byte replay confirmed**.

This audit does not create a new scientific result. The first reveal remains authoritative. The purpose is to test whether the unchanged frozen Phase63B executable reproduces that result on a separate GitHub-hosted runner.

## First-reveal authority

- scientific head: `31746c4d318929b602b35c288e36e83001200509`
- Actions run: `33334225091`
- job: `99318112772`
- artifact: `9738599590`
- artifact ZIP SHA-256: `4b9448e655d539528357ee4b51de1ebdea70003730c593f49c96bdbb4a6d9324`
- raw `phase63b_science_results.json` SHA-256: `77653133af22cd26141bc695a8ee6243cc3d924ba44a41a685cb148b9167db91`

The exact first-reveal artifact was separately downloaded, hash-verified and committed before this replay audit was interpreted.

## Clean replay

- Actions run: `33334631706`
- job: `99319212644`
- replay artifact: `9738711593`
- replay artifact ZIP SHA-256: `7e6ddca3223bf183ea4036c84325b7761fedab7e57507b083c58b389381e5d05`
- replay raw JSON SHA-256: `77653133af22cd26141bc695a8ee6243cc3d924ba44a41a685cb148b9167db91`

The replay used the same exact external source identities/hashes, same parser, same committed folds, same labels/seeds, same frozen A1 parameters and same `phase63b_science.py` scientific implementation.

## Comparison

The audit recursively compared the parsed first-reveal and replay JSON objects.

Results:

- first raw SHA-256 = replay raw SHA-256;
- recursive structural/value differences: **0**;
- non-numeric differences: **0**;
- maximum absolute numeric difference: **0.0**;
- overall Phase63B verdict unchanged;
- GC/IT observational frozen criteria unchanged;
- IT-R3 W1/W2 pass/fail decisions unchanged.

Therefore Phase63B is **exactly replay-deterministic in this clean cross-run audit**, including raw JSON bytes.

## Interpretation rule

This strengthens reproducibility confidence only. It does not increase the scientific claim beyond the frozen Phase63B result and does not convert strong structural replication into historical or semantic identification.
