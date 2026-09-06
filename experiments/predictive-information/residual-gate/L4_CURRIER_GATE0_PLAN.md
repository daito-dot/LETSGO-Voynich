# Issue #127 — L4 Currier edge transport Gate 0

Date: 2026-09-06
Status: **SCORE-FREE / FROZEN BEFORE L4 TRANSPORT SCORING**
Parent: Issue #88 / Issue #104 / Issue #125

## Purpose

Before transporting the explicit terminal→initial edge across Currier A/B, verify that the already-frozen Phase 3A Currier authority provides valid edge-event support in all ten Currier × physical-leaf-fold cells.

Gate 0 computes no probabilities, likelihoods, bits/token, gain, mixture weight or transport statistic.

## Currier authority

Recompute `experiments/predictive-information/phase3a/currier_gate0_audit.py` unchanged and require exact JSON SHA-256:

`e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e`

This includes Amendment A for the single missing `$L` page and the existing score-free A/B population/fold authority.

## Edge-event definition

Under the exact eligible Phase 3A A/B population:

- source order is corrected source order;
- physical-leaf folds are unchanged;
- each source line resets edge history;
- each token after the first visible token on a source line defines one visible line-body edge event;
- the previous edge symbol is the final raw byte of the immediately previous visible token;
- the current edge outcome is the initial raw byte of the current visible token;
- a scientific edge target is counted when the current token is accepted by the frozen SlotParser; the previous token need not be parser-accepted, matching Issue #125's observable edge construction.

## Counts only

For each Currier A/B × fold cell, report:

- eligible leaves/documents/items;
- visible source lines;
- visible line-body edge events;
- parser-accepted current-token edge targets;
- observed previous-terminal classes;
- observed current-initial outcomes;
- observed terminal→initial pairs.

Also report the same class/pair support globally by Currier stratum.

## Gate rule

PASS only if:

1. Phase 3A Currier Gate0 reproduces the exact frozen JSON SHA;
2. its own `gate_pass` is true;
3. no eligible physical leaf mixes Currier A/B;
4. corrected source-order and fold authorities remain valid;
5. every A/B × fold cell contains at least one parser-accepted line-body edge target;
6. each global Currier stratum contains at least two previous-terminal classes and at least two current-initial outcomes.

Otherwise STOP before any predictive transport scorer is committed.

## Firewall

Gate 0 must not compute or select:

- edge probabilities;
- POS2/EDGE2 likelihoods;
- B3/mixture code lengths;
- transport gains or penalties;
- source/target scalar strengths;
- Issue #84 surface targets;
- semantic/image/hand/latent-state variables.
