# Issue #58A — 12-slot occupancy-graph specificity audit

Status: **FIRST REVEAL COMPLETE**

Frozen classification:

> **`BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`**

## Bottom line

Issue #55's slot3×slot5 occupancy exclusion is real in the frozen 12-slot representation, but it is not a uniquely strong edge.

Across all 66 unordered slot pairs, 22 edges survive the preregistered global maxT family-wise criterion with all five physical-leaf held-out gains positive. The historically selected `(3,5)` edge ranks only **22/66** by mean held-out symmetric predictive information gain.

The object of study therefore moves from one selected pair to the **complete signed slot-occupancy graph**: some slot pairs strongly co-occur, while others strongly exclude one another.

This result is structural only. It does not assign semantics, plaintext, music, cipher-table meaning, or historical identity to any slot.

## First-reveal provenance

The audited first reveal was GitHub Actions run **33399104345**, job **99510744309**, triggered by PR #60.

Frozen inputs / code:

- current-main base at experiment start: `7af6623ea3637b31b5f71a5de7b8675757335f83`
- latest pre-executable frozen plan commit: `84243646f5276ed1959f41f2e4c179c7357ead87`
- executable first commit: `37968752114524de1ac4aa0c21489d55cbaa5239`
- audited workflow branch head: `d0588651870f7cb818b74e2d9402bec3c103f412`
- frozen ZL3b source repository commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- frozen ZL3b source Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- numerical dependencies: `numpy==2.2.6`, `scipy==1.16.1`

The workflow verified that the frozen plan commit predates the executable commit and verified the exact source commit/blob before target scoring.

Artifact:

- artifact ID: `9760539131`
- artifact name: `issue58a-occupancy-graph-66674e1a69b013cb398f0d2b3a69b991100d4739`
- artifact ZIP SHA-256: `4dafa489e591a92c0f94a8c9416186fe5f25512d0b1d41a99e52c203b31b8eb6`
- raw `issue58a_results.json` SHA-256: `ae0db7dc72cb890a325ef5313a3375a43efde7c27c9bd5b3fcb0632fb808e152`

The artifact name contains the PR merge-ref SHA supplied by GitHub as `github.sha`; the science step itself explicitly checked out branch head `d058865...`, as recorded in the run log.

## Population

Primary `min` parser population:

- visible tokens: **32,570**
- successfully parsed tokens: **25,071**
- parse coverage: **0.76975745**
- physical lines with parsed tokens: **4,082**
- held-out fold parsed-token counts: **4,430 / 4,810 / 5,516 / 5,447 / 4,868**

Per-slot occupancy counts for slots 0..11:

`8229, 12640, 3852, 10845, 9227, 1341, 9545, 5831, 13565, 5008, 13178, 10230`

## Primary family-wise result

Exactly 1,000 deterministic within-line independent occupancy-relocation null populations were scored across all 66 pairs.

Primary null maxT distribution over mean held-out gain:

- minimum: `0.02697788297`
- median: `0.03337939834`
- q95: `0.03645947227`
- maximum: `0.03933438747`

**22/66** real edges satisfy both:

1. global maxT adjusted `p <= .01`; and
2. all five held-out fold gains positive.

Qualifying edges:

`(0,4), (1,3), (1,4), (3,4), (3,5), (4,6), (4,9), (4,11), (6,7), (6,8), (6,9), (6,10), (6,11), (7,8), (7,10), (7,11), (8,9), (8,10), (8,11), (9,10), (9,11), (10,11)`

This exceeds the frozen threshold of five distinct qualifying edges for the broad-grammar classification.

## Selected `(3,5)` edge

The #55-selected edge remains a genuine held-out dependence:

- rank by mean held-out gain: **22/66**
- mean symmetric gain: **0.04421504450 bits/token**
- five fold gains: `0.04645571, 0.04032638, 0.04346543, 0.04713976, 0.04368794`
- all five positive: **yes**
- global maxT p: **`1/1001 = 0.000999001`**
- pooled phi: **-0.20648429**
- contingency `[[00,01],[10,11]]`: `[[12888,1338],[10842,3]]`
- observed co-occupancy rate: **0.00011966**
- independence-expected co-occupancy rate: **0.02313742**
- observed/expected co-occupancy ratio: **0.00517171**
- exclusion rank among negative-phi edges: **14**

Thus #55 was not a false positive: `(3,5)` really is almost mutually exclusive. What fails is the stronger claim that it is one of the globally dominant or uniquely informative slot relations.

## Token-complexity conditioning

The preregistered strong sensitivity conditions on

`K_other = number of occupied slots outside the tested pair`.

For `(3,5)`:

- conditional mean held-out gain: **0.02635950185 bits/token**
- conditional five folds: `0.02654979, 0.02660808, 0.02513900, 0.02617129, 0.02732935`
- all five conditional folds positive: **yes**
- conditional maxT p: **0.55644356**

Conditional-null maxT distribution:

- minimum: `0.02030861043`
- median: `0.02666280229`
- q95: `0.02956599953`
- maximum: `0.03203522007`

So `(3,5)` still carries positive held-out information after controlling for token occupancy complexity, but it is no longer family-wise exceptional relative to the other 65 edges. This reinforces the broad-grammar interpretation.

## Strongest primary edges

Top ten by primary mean held-out gain:

| rank | pair | mean gain | maxT p | phi | co-occurrence ratio | conditional mean | conditional maxT p |
|---:|:---:|---:|---:|---:|---:|---:|---:|
| 1 | (8,10) | 0.76766689 | 0.000999 | +0.923778 | 1.80824 | 0.57118786 | 0.000999 |
| 2 | (8,11) | 0.39059985 | 0.000999 | -0.701639 | 0.22168 | 0.41994088 | 0.000999 |
| 3 | (10,11) | 0.37255007 | 0.000999 | -0.684763 | 0.21647 | 0.39960348 | 0.000999 |
| 4 | (1,3) | 0.24118912 | 0.000999 | +0.559121 | 1.63506 | 0.27719591 | 0.000999 |
| 5 | (9,10) | 0.21187500 | 0.000999 | +0.471833 | 1.89717 | 0.16693187 | 0.000999 |
| 6 | (6,11) | 0.20568727 | 0.000999 | +0.527540 | 1.81038 | 0.17487930 | 0.000999 |
| 7 | (8,9) | 0.17271464 | 0.000999 | +0.436312 | 1.80430 | 0.13393062 | 0.000999 |
| 8 | (9,11) | 0.15697184 | 0.000999 | -0.403231 | 0.02789 | 0.15457071 | 0.000999 |
| 9 | (6,10) | 0.14057113 | 0.000999 | -0.433987 | 0.47418 | 0.15256776 | 0.000999 |
| 10 | (6,8) | 0.12951463 | 0.000999 | -0.418127 | 0.50886 | 0.14275329 | 0.000999 |

The leading structure contains both strong positive and strong negative edges. This is not well described as a manuscript-wide tendency toward mutual exclusion. It is a signed construction grammar.

The strongest relation, `(8,10)`, is roughly **17.4×** the selected `(3,5)` edge in mean held-out gain (`0.7677` vs `0.0442`) and remains decisively family-wise significant after `K_other` conditioning.

## Parser admissibility

All **66/66** canonical two-slot co-occupancies are admitted by the frozen parser; failures: **none**.

Therefore the observed graph cannot be reduced to the parser simply forbidding the relevant slot combinations by construction.

## `max` parser sensitivity

The non-promoting `max` parser policy changes several occupancy assignments and therefore changes the ordering of the strongest edges, but it does not provide a route to promote `(3,5)` into a unique result. The primary scientific classification remains controlled by the frozen `min` analysis.

## Frozen classification gates

Selected-edge extreme gate:

- selected rank <= 3: **FAIL** (`22`)
- selected maxT p <= .01: **PASS**
- selected all five folds positive: **PASS**
- selected phi < 0: **PASS**

Because the selected-edge extreme gate fails and **22** distinct edges meet the family-wise qualifying criterion, the preregistered classification is mechanically:

> **`BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`**

## Interpretation

The correct update is:

1. retain #55's empirical fact that slot3 and slot5 almost never co-occupy a parsed token;
2. remove any privilege attached to that pair merely because the E10→#55 path exposed it first;
3. model the complete occupancy system, especially the tightly coupled slots 6–11 and the signed triangle involving slots 8, 10 and 11;
4. distinguish positive co-construction edges from negative alternative-construction edges;
5. ask whether this graph is stable across independently frozen manuscript strata and representations before using it to constrain a reversible surface-transform family.

## Protocol limitation discovered at reporting

Issue #58's umbrella specification required register/Currier/token-position stratification or interaction tests to be **predeclared**. The frozen #58A plan did not define those target strata; it defined the complete graph, physical-leaf cross-fit, line-local null, parser ambiguity sensitivity and `K_other` sensitivity only.

Because the first reveal has now occurred, those stratified tests must **not** be added retrospectively to #58A and described as confirmatory. They require a separate plan-first #58B phase.

Likewise, independent-transcription replication remains deferred until the 12-slot construction can be mapped without choosing a representation from the #58A outcome.

This is a scope/protocol limitation, not a reason to alter the #58A classification.

## Next scientific frontier

The next plan-first phase should test whether the **signed occupancy graph**, rather than `(3,5)` alone, is stable across externally defined manuscript strata. The primary candidates must be frozen before scoring and should emphasize graph-level invariants rather than post-hoc pursuit of individual high-scoring edges.

Only after structural stability is established should the project ask whether the occupancy graph constrains an invertible surface-generation/decoding mechanism.
