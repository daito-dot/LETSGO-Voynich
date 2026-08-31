# Issue #58D / #66 Stage-A source/population audit report

Status: **COMPLETE — IT2a AUTHORIZED FOR TARGET PLAN; NO SCIENTIFIC PAIR/RESIDUAL SCORE COMPUTED**

Exact raw authority: `issue66_source_audit.json`.

## Question

Before testing whether the #58C residual token-construction graph survives an independent reading, is IT2a a fair, adequately supported target for the already frozen 12-slot representation without result-driven normalization?

## Result

> **`AUTHORIZED_FOR_TARGET_PLAN`**

All preregistered source/support gates passed.

## Source-version check

The live canonical IT2a retrieved in the workflow is byte-for-byte identical to the independently frozen Phase63B source:

- SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- Git-blob SHA-1 `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- 342,104 bytes
- 5,444 lines
- `#=IVTFF EvaT 2.0 M 3`

Therefore there is no unexplained source-version drift between the earlier independent-transcription work and #58D.

GC2a likewise exactly matches its historical Phase63B source, but remains unsuitable for the *exact* current 12-slot target without a new v101→EVA-compatible representation rule. No such rule was invented after inspection.

## IT2a population and direct parser compatibility

Using the pre-existing Phase63B W1 source parser:

- P-coded loci: 4,118
- paragraphs: 772
- pages: 206
- physical leaves: 99
- clean tokens: 34,411
- excluded uncertain/unreadable tokens: 80

Using the unchanged current 12-slot parser:

- accepted tokens: **28,280**
- rejected: 6,131
- direct coverage: **82.183%**
- tokens with more than one legal parse: 9,492
- tokens where frozen `min` and `max` selections differ: 9,492

The large ambiguity count is therefore a real representation sensitivity and must remain visible. `min` is the confirmatory primary policy and `max` may only be a non-promoting sensitivity analysis.

## Physical-leaf comparability

IT2a covers exactly the same **99/99 physical leaves** as the frozen #58C population.

There are no IT2a-only or ZL3b/#58C-only leaves in the target universe.

Frozen fold support after unchanged-parser acceptance:

- fold0: 4,976
- fold1: 5,416
- fold2: 6,261
- fold3: 6,197
- fold4: 5,430

Every fold exceeds the preregistered minimum of 300 by more than an order of magnitude.

## Stratum support

Accepted-token support under IT2a page metadata:

- AH — Currier A within Herbal: 6,295
- BH — Currier B within Herbal: 2,739
- BB — section B within Currier B: 5,551
- BS — section S within Currier B: 8,744

Accepted token-position support:

- initial: 3,156
- interior: 22,105
- final: 3,006
- singleton: 13

Thus all seven #58C planned non-singleton Currier/section/position groups have substantial Stage-A support. The target plan may prospectively retain the same seven contrasts rather than narrowing them after seeing science.

## Authorization gates

All passed:

1. unambiguous IT2a/Takahashi `EvaT` identity — PASS
2. source drift understood — PASS; in fact exact historical bytes
3. pre-existing source parser works without new normalization — PASS
4. unchanged 12-slot coverage >=60% — PASS at 82.18%
5. >=80 shared physical leaves — PASS at 99
6. >=300 accepted tokens in every frozen fold — PASS, minimum 4,976
7. no pair/residual scientific target metric computed — PASS

## What this does and does not authorize

This audit authorizes a separate **plan-first #58D target replication** using IT2a.

It does not establish that #58C replicated. The audit was deliberately prevented from calculating the 66 target associations, residual energy, ZL3b/IT2a graph similarity, sign agreement, or any target p-value.

The next allowed action is to freeze `PLAN_A.md` for the scientific replication **before** adding its executable.