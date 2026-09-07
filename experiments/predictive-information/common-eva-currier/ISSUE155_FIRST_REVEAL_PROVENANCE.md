# Issue #155 — common-EVA support-matched Currier first-reveal provenance

Date: 2026-09-07
Status: **AUTHORITATIVE FIRST REVEAL COMPLETE**

Frozen classification:

> **`COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE`**

## Clean prospective chronology

1. Issue #155 plan and score-free Gate were frozen before target scoring.
2. Gate0 first succeeded in run `34074918456`, result SHA-256 `01f96038407975bc4d7a5944082a5bd2af9137f105edc33bd529cfccd33362f3`.
3. Gate0 PR #156 merged as `920130f721b83902c000c48f951c499a660f0683`.
4. Scientific scorer committed afterward at `ea4c57942937562231f1ce35e60880e263ded28e`, blob `0d57fdd32d298773b5ee38f97c9f104d29fa8377`.
5. **No Issue #155 target workflow existed when that scorer blob was frozen.**
6. First target workflow added afterward at `81ad05e87efaac151a280d4b1a0b553b6e7937f9`.
7. First target run completed successfully without any scientific repair.

## Authoritative first reveal

- Issue: #155
- PR: #157
- workflow: `Issue155 common-EVA Currier first reveal`
- run: `34075146845`
- exact workflow/scoring head: `81ad05e87efaac151a280d4b1a0b553b6e7937f9`
- conclusion: `success`
- scorer blob: `0d57fdd32d298773b5ee38f97c9f104d29fa8377`
- Gate0 result SHA-256: `01f96038407975bc4d7a5944082a5bd2af9137f105edc33bd529cfccd33362f3`
- Gate0 script blob: `f5ab4fa31a92b3c303401da33611ffd5f77b402d`
- Gate0 provenance blob: `ba2f443b24237ed5ee0dce127b1a43ad082481c4`
- frozen plan blob: `1f30d7c62083dbff378612ce7bf177ee7d9fff80`
- Gate0 merge: `920130f721b83902c000c48f951c499a660f0683`
- artifact ID: `10001781210`
- artifact name: `issue155-common-eva-currier-first-reveal-81ad05e87efaac151a280d4b1a0b553b6e7937f9`
- artifact ZIP digest: `sha256:23791cb31e81a706c15c22a0168398d0a8cf7685fb5592606b648540b4bd65d3`
- result JSON SHA-256: `041d7abe8f677da012ae143df9f4f372e88afc2e2b3cc7b359a58a4d7395b737`

All workflow assertions passed, including exact Gate0 reproduction, merged authority blobs, target support, matched-table identity, gain arithmetic, reading-level pass rules, and the frozen joint classification.

## Frozen scoring responsibility

For each target reading and target Currier regime, `POS2` and all non-edge factors are trained target-reading/target-regime natively on the four training folds. The only transported component is the opposite Currier regime's reading-balanced, context-mass-matched BODY previous-terminal→first-atom table.

No primary rho/mixture calibration and no target-native fallback are used.

Within one reading a direction passes iff mean `G_transport > 0` and positive in at least 4/5 folds. A direction is promoted as robust only if it passes independently in both ZL3b and IT2a.

## A→B result

### ZL3b target B

`G_transport` by fold:

`[-0.3348510891865786, -0.31319441252966485, -0.3476417837322998, -0.3389410840396838, -0.16152753282191412]`

- mean `-0.29923118046202823 bit/token`;
- positive `0/5`;
- within-reading pass: **FAIL**.

Same-regime B matched-table gain, non-promoting diagnostic:

`[0.21004621952877578, 0.13767400125780682, 0.16718173044148976, 0.19147034511024685, 0.1462539116627859]`

- mean `+0.17052524160022103`;
- source-transport minus target-native matched gain `-0.46975642206224927`;
- minimum matched-context coverage `0.9986225895316805`.

### IT2a target B

`G_transport` by fold:

`[-0.3164940693564553, -0.30510646388743723, -0.3361776000713945, -0.34219919368447194, -0.19327005036819322]`

- mean `-0.29864947547359044`;
- positive `0/5`;
- within-reading pass: **FAIL**.

Same-regime B matched-table gain:

`[0.2681902700020373, 0.17332406661064503, 0.21132896920629385, 0.22694856367551353, 0.16286698365605545]`

- mean `+0.20853177063010903`;
- source-transport minus target-native matched gain `-0.5071812461036995`;
- minimum matched-context coverage `0.9991843393148451`.

Therefore A→B is not robust in either reading, let alone both.

## B→A result

### ZL3b target A

`G_transport` by fold:

`[-0.5081412980502265, -0.11477888603366715, -0.3618035796634178, -0.45120288817033405, -0.44075878437485194]`

- mean `-0.37533708725849946 bit/token`;
- positive `0/5`;
- within-reading pass: **FAIL**.

Same-regime A matched-table gain:

`[0.021995782253458884, 0.07765431510119036, 0.05101077910257068, 0.028530630327816553, 0.10530368112352129]`

- mean `+0.05689903758171155`;
- source-transport minus target-native matched gain `-0.432236124840211`;
- minimum matched-context coverage `0.9975186104218362`.

### IT2a target A

`G_transport` by fold:

`[-0.5358538385373492, -0.11172098059214441, -0.3692465599328436, -0.38364470863978717, -0.536183427875569]`

- mean `-0.3873299031155387`;
- positive `0/5`;
- within-reading pass: **FAIL**.

Same-regime A matched-table gain:

`[0.040914763906696905, 0.08972459890897966, 0.06902220023573236, 0.06572799427525311, 0.11935254428369646]`

- mean `+0.07694842032207169`;
- source-transport minus target-native matched gain `-0.46427832343761044`;
- minimum matched-context coverage `0.9986693280106453`.

Therefore B→A is also not robust in either reading.

## Joint result

- A→B robust in both readings: **false**;
- B→A robust in both readings: **false**;
- frozen classification: **`COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE`**.

Directional reading differences are small relative to the failure magnitude:

- A→B mean ZL3b−IT2a difference `-0.0005817049884377923 bit/token`;
- B→A mean ZL3b−IT2a difference `+0.011992815857039263`.

Thus the non-transport result itself replicates closely across the two reading lineages.

## Relation to Issue #130

Issue #130's older raw-byte / mixture-family support-matched test classified `MATCHED_TABLE_TRANSPORT: B→A ONLY`.

Issue #155 does **not** reproduce that one-way literal transport under the stabilized common-EVA / reading-balanced direct-table family. Instead, both wrong-regime literal tables are strongly harmful relative to the target-regime POS2 baseline.

Because #155 changes the representation and model family together — notably common-EVA atomization, cross-reading table consolidation, deterministic fractional support matching, and no primary rho mixture — it does not isolate which single change removes the old B→A result. The correct conclusion is narrower:

> **The #130 B→A-only literal-table transport is not stable under the current common-EVA / reading-consolidated direct-table model family.**

## Accepted interpretation

The positive same-regime matched-table gains in all 20 fold cells, alongside strongly negative wrong-regime transport in all 20 corresponding fold cells, support a stronger surface statement:

> **The previous-terminal→next-initial edge is robust across transcription readings, but its concrete conditional mapping is Currier-regime dependent under the stabilized common-EVA representation. Using the opposite Currier regime's literal mapping is worse than ignoring previous-terminal identity altogether.**

This is a predictive regime-specificity result. It does not establish why Currier A/B differ, whether they are chronological stages, or whether one derives from the other.

## Boundary of inference

This result does not establish natural-language words, plaintext, semantics, language/cipher family, authorship/scribe causation, historical direction, production mechanism, artificiality/hoax, or decipherment.

A high-information next gate is to quantify the **incremental information of Currier gating itself** under this stabilized representation: compare one regime-neutral pooled common-EVA edge table against separate A/B tables prospectively, rather than trying additional post-hoc cross-transport repairs.

Refs #88 #125 #127 #130 #134 #139 #145 #148 #151 #155 #156 #157.
