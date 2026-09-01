# Issue #72 V2 — Stage A trace-based causal-identification audit

Status: **PREREGISTERED / TARGET-BLIND — NO COUNTERFACTUAL R1 SCORE AUTHORIZED**

Parent main:

`98a04953aabe9e228a17fa5808adf506a0833362`

Normative evidential protocol:

`research/RESEARCH_PROTOCOL.md`

Historical predecessor:

- PR #73 is closed unmerged and retained only as a superseded pre-reveal design record;
- attempted run `33458765600` stopped in prepare job `99704262365`;
- real `score` and `aggregate` jobs were skipped;
- therefore no Issue #72 counterfactual R1 target quantity has been revealed.

## 1. Scientific purpose

Issue #68 established that published Naibbe reproduces the independently replicated R1 token-construction topology while failing R2, R3 and R4.

The next question is not "how can we make a harder test?" It is:

> **Which parts of the Naibbe generative stack can actually be causally separated when asking why its emitted surface satisfies R1?**

Stage A does not decide where R1 originates. It decides which later interventions would have a valid interpretation.

The central distinction is between:

1. **fixed-realization emission effects** — alter codebook/emission association while holding the exact realized segmentation/table/state/retry/spacing path fixed;
2. **total pipeline effects** — perturb an upstream input and allow every downstream retry/RNG consequence to change naturally;
3. **surface sufficiency controls** — alter only the already-emitted surface and make no claim about upstream cause.

These three roles must not be collapsed.

## 2. Why V1 was not causally identified

Pinned Naibbe uses a shared global Python `random` stream for multiple stages:

- one/two-character plaintext segmentation;
- shuffled weighted table decks;
- extra table-card consumption caused by ambiguity retries;
- later deck reshuffles;
- 3% ciphertext-space removal.

With `UNAMBIGUOUS=True`, a proposed bigram is accepted/rejected from emitted glyph strings and the global unigram/bigram collision catalog.

Therefore changing a glyph/codebook association and rerunning the encoder can change retry counts, which changes downstream card consumption and potentially all later random choices. Such a rerun is a legitimate **total intervention on the pipeline**, but it does not isolate the direct effect of the nominated association.

V2 introduces an auditable accepted-event trace specifically to separate those meanings.

## 3. Exact source authorities

Naibbe:

- repository: `greshko/naibbe-cipher`;
- commit: `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`;
- encoder `naibbe_v2.py` blob: `b566ad82e4b6ff0782ecdddebf77718dac44f292`;
- table `references/naibbe_tables.csv` blob: `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`;
- decoder `decrypt_naibbe.py` blob: `b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b`.

Plaintext authority:

- exact four Phase64B CREMMA manuscripts;
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`.

Published primary surface authority remains the Issue #68 realization-0 population. Stage A must reconstruct its exact identities before any intervention can be considered usable.

No ZL3b/IT2a edge vector or target residual statistic may be loaded by Stage A code.

## 4. Criterion Validity Table — Stage A only

| Claim / responsibility | Construct | Metric / identity | Decision rule | Source | Positive control | Negative / failure control | Licensed failure meaning | Blind spot / limit |
|---|---|---|---|---|---|---|---|---|
| Instrumentation reproduces published Naibbe realization | Byte-identical re-emission from instrumented execution | exact raw and published surface SHA-256 / bytes | exact equality | **T1** | frozen Issue #68 rep0 surfaces | any byte/hash mismatch | instrumentation is not an exact authority; stop | says nothing about R1 cause |
| Accepted-event trace contains enough information for deterministic re-emission | trace-only renderer reproduces instrumented surface without RNG/encryption rerun | exact token sequence + spacing output equality | exact equality | **T1** | original instrumented surface | missing/ambiguous event or mismatch | trace is insufficient for fixed-path intervention; stop | trace captures realized path, not counterfactual retry decisions |
| Trace intervention isolates nominated emission mapping conditional on realized path | all non-nominated trace fields remain identity-equal while only declared lookup value changes | schema-level invariant diff | zero unauthorized field changes | **T1** | identity transform | deliberate mutation of a protected field must fail invariant checker | intervention is not a direct fixed-path ablation | conditional/direct effect only; not total pipeline effect |
| Upstream plaintext perturbation is a total-pipeline intervention | only input plaintext ordering is changed before calling unchanged published pipeline; all downstream changes are allowed and recorded | source multiset equality + unchanged executable/config/source authority | exact nominated input invariant; no downstream equality requirement | **T1** for intervention identity | no-change replay | source multiset/length mismatch | cannot interpret as total effect of plaintext order | cannot isolate direct plaintext effect from downstream mediation |
| Final-surface control is only a sufficiency test | operation starts from frozen final tokens and never claims an upstream mechanism | exact preserved quantities declared by control | exact invariant equality | **T1** | identity final surface | invariant violation | surface control invalid | success cannot identify codebook/process origin |
| 12-slot interface support is measurable without R1 target inspection | fraction of visible clean tokens accepted by unchanged `SlotParser(min)` | coverage as continuous value | **descriptive in Stage A; no eligibility cutoff** | **DESCRIPTIVE / later calibration required** | published Naibbe coverage from #68 | none in Stage A | no causal rejection licensed | parser may select a nonrepresentative subset |

No Stage-A criterion uses "strictness" as justification.

## 5. Required trace schema

The trace must be generated by an instrumented implementation behaviorally equivalent to the pinned published encoder.

At minimum, each source line must record:

### 5.1 Source/normalization

- manuscript and stable source item/line identity;
- exact source text identity/hash where already authorized;
- cleaned/effective plaintext string after the frozen Phase64B projection;
- normalized character positions.

### 5.2 Segmentation event

For every emitted pre-cipher token:

- sequential event index;
- source character span;
- one-character versus two-character unit;
- plaintext letter(s).

### 5.3 Accepted encryption event

For unigram:

- state=`unigram`;
- selected table;
- code key `(state, table, letter)`;
- emitted glyph.

For bigram:

- prefix letter, table, state, code key, glyph;
- suffix letter, table, state, code key, glyph;
- accepted concatenated glyph;
- number of rejected attempts before acceptance.

### 5.4 Retry audit

For every rejected bigram attempt, record enough information to prove why it was rejected without affecting the published execution:

- prefix/suffix selected tables and code keys;
- proposed glyph pair/combined string;
- rejection reason: unigram collision and/or alternative bigram-code collision.

This retry trace is an audit of the realized path. It is not reused to decide counterfactual acceptance under fixed-path emission interventions.

### 5.5 Deck/process position

Record sufficient deterministic indices to audit card consumption and deck reshuffles, including at least:

- deck generation/reshuffle index;
- card position(s) consumed by each accepted/rejected attempt;
- total cards consumed per source line.

The trace need not serialize Python's full RNG internal state if exact byte replay plus event/card identities prove equivalence.

### 5.6 Published output spacing

After encryption, record the exact join mask for the 3% output-space-removal stage:

- between-token boundary index;
- kept-space versus removed-space decision.

A trace-only renderer must be able to emit both:

- raw encrypted tokenized line;
- published respaced line.

## 6. Exact replay tests

Before any counterfactual surface is generated, Stage A must prove all of:

1. pinned source blobs/commits match authority;
2. instrumented baseline execution reproduces the exact Issue #68 primary rep0 surface for every manuscript and pooled population;
3. trace-only renderer reconstructs the exact instrumented raw token sequence;
4. trace-only renderer reconstructs the exact published 3%-space-removal surface;
5. retry counts and accepted cell identities are deterministic on repeated runs;
6. no target R1 artifact/module is imported or opened.

Any exact replay failure yields:

`TRACE AUTHORITY NOT ESTABLISHED`

and Stage A stops without target scoring.

## 7. Candidate fixed-path emission interventions to audit

These are **conditional direct-emission ablations**, not runnable Naibbe cipher variants.

They use the baseline accepted-event trace and do not rerun segmentation, deck selection, ambiguity retries, or spacing RNG.

All emitted values come only from the pinned public codebook under outcome-independent mappings.

### EL — effective-letter association remap on fixed trace

For an accepted cell `(state, table, letter)`, render the glyph stored at:

`(state, table, pi(letter))`

where `pi` is a prospectively generated permutation of the 23 effective letters.

Hold fixed:

- source segmentation;
- original plaintext letter identity in the trace;
- accepted table/state schedule;
- retry history as history only;
- published spacing join mask.

Interpretation if later scored:

> conditional on the exact realized process path, does the published effective-letter-to-glyph association matter for the emitted R1 surface?

It does **not** estimate the total effect of rerunning Naibbe with the remapped codebook.

### ES — state-value association remap on fixed trace

For accepted `(state, table, letter)`, render the glyph from a prospectively fixed permutation/rotation of `state` while preserving original state as a trace field.

Interpretation:

> conditional on realized path, does the published assignment of glyph values to unigram/prefix/suffix roles matter for R1 emission?

### ET — table-value association remap on fixed trace

For accepted `(state, table, letter)`, render the glyph from a prospectively fixed permutation of table labels while preserving the realized selected table schedule.

Interpretation:

> conditional on realized path, does the published allocation of glyph values across weighted table identities matter for R1 emission?

### EG — global reachable-cell value reassignment on fixed trace

Prospectively permute glyph values as cell instances across the 414 effective reachable `(state,table,letter)` cells, with duplicates retained as separate instances.

Interpretation:

> conditional on the exact realized path, is structured cell-to-glyph association beyond the reachable global glyph-value multiset important for R1 emission?

### Ambiguity legality diagnostic

Because EL/ES/ET/EG deliberately hold the realized path fixed, their re-emitted bigrams may no longer satisfy the published `UNAMBIGUOUS` acceptance rule.

Stage A must report, for every proposed intervention realization:

- fraction of re-emitted bigrams that would remain admissible under the pinned ambiguity catalog;
- unigram-collision count;
- alternative-bigram-collision count.

This is a **diagnostic, not a repair gate**.

No post-hoc mapping may be selected to improve legality or parser coverage.

If legality is poor, later interpretation must remain explicitly "fixed-path structural ablation" and must not call the surface a valid Naibbe ciphertext.

## 8. Candidate total-pipeline intervention to audit

### PT — plaintext-order total effect

Within each effective plaintext line, shuffle character order under deterministic target-independent labels while preserving exactly:

- character multiset;
- line length.

Then run the unchanged published pipeline from segmentation through final spacing.

All changed segmentation, tables, retries, deck trajectory and spacing are accepted as downstream consequences.

Later interpretation is limited to:

> total effect of changing plaintext order through the complete published Naibbe pipeline.

It must not be described as a direct plaintext-order effect.

## 9. Candidate final-surface sufficiency control to audit

### FI — final-token inventory/layout sufficiency

Start from the exact frozen published primary token surface.

Prospectively permute complete token instances while preserving the exact declared layout quantities.

Stage A must freeze exactly which quantities are preserved before any R1 score, at minimum:

- total whole-token multiset;
- manuscript/item/line token counts.

Later interpretation is strictly:

> whether that already-produced final token inventory plus preserved layout is sufficient for R1 under the chosen randomization.

FI can never by itself imply "codebook-origin", "process-origin", or historical mechanism identity.

## 10. Target-blind support outputs

For identity and each candidate intervention family, Stage A may compute only:

- deterministic surface SHA-256;
- line/token counts;
- exact invariant-check results;
- changed-event counts;
- direct unchanged `SlotParser(min)` accepted-token count and coverage;
- token-length and basic inventory counts required to understand interface support;
- fixed-path ambiguity-legality diagnostics;
- retry/process diagnostics for total-pipeline PT.

Stage A may not compute pairwise slot co-occurrence/association, even descriptively.

## 11. Explicitly forbidden before later target plan

For any counterfactual surface, do not compute or expose:

- any 2x2 slot-pair table;
- any of the 66 Yule-Q values;
- K_other-conditional association;
- residual Z;
- residual energy E;
- graph reliability W;
- correlation/cosine/sign agreement with ZL3b, IT2a, or published Naibbe residual graphs;
- R1 p-values;
- per-edge differences;
- any intervention/permutation selection based on a Voynich target score.

The Stage-A executable should not import the R1 scorer.

## 12. No inherited 60% hard gate in Stage A

Issue #68 used direct parser coverage `>=0.60` as an interface gate.

Under `research/RESEARCH_PROTOCOL.md`, that numerical boundary is a pragmatic/interface T5 threshold rather than a logically or empirically privileged cutoff.

Therefore Stage A records coverage continuously and does not declare a counterfactual scientifically eligible/ineligible merely because it lies on one side of 0.60.

A later target plan must justify any coverage restriction by its role, positive-control support and selection-bias implications before it becomes a hard decision rule.

## 13. Stage-A completion classes

### `TRACE-IDENTIFIED INTERVENTION SET READY FOR TARGET DESIGN`

Use only if:

- exact baseline replay is established;
- trace-only rendering is exact;
- at least one fixed-path emission intervention is mechanically valid under its invariant checker;
- PT total-pipeline intervention is mechanically valid or explicitly excluded for a source-supported reason;
- FI is either mechanically valid as a descriptive control or explicitly excluded;
- all support diagnostics are frozen without R1 target access.

### `PARTIAL TRACE IDENTIFICATION`

Use if baseline trace authority is exact but only a subset of intervention roles is mechanically interpretable.

### `TRACE AUTHORITY NOT ESTABLISHED`

Use if exact baseline/trace replay fails.

No harder statistical threshold can rescue a failed trace-identification criterion.

## 14. What Stage A does not decide

Stage A does not decide:

- whether any intervention retains R1;
- whether R1 is codebook- or process-generated;
- whether Naibbe is historical;
- whether Voynichese is encrypted Latin;
- whether a decoder exists;
- whether R2/R3/R4 can be repaired.

It establishes only whether later R1 contrasts would have a scientifically valid causal/sufficiency interpretation.

## 15. Required next document after Stage A

Only after Stage A is frozen may a later target plan be written.

That plan must include a new Criterion Validity Table for the **R1 target decisions themselves**, including:

- why R1 is valid for the exact role being asked;
- how parser coverage is handled and calibrated;
- how intervention-family variation is summarized without arbitrary hardness bands;
- what positive and matched negative controls calibrate retention/change;
- the maximum causal statement licensed by each intervention role;
- how multiplicity and target access are controlled.

No target scorer is authorized by this Stage-A plan.
