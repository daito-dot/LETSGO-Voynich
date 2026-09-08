# Priority 5 closeout — no new target entrant

Date: 2026-09-08  
Parent program: Issue #172  
Roadmap authority: `research/NEAR_TERM_RESEARCH_ROADMAP_20260908.md`  
Closeout issue: #213

## Decision

**The current near-term historical-mechanism admission search closes with no new #172 target entrant.**

No new candidate target score was computed during Priority 4/5 selection and admission. The project will not continue scanning historical ciphers merely because the two prospectively motivated admission paths terminated before target reveal.

This is a stopping decision for the current search protocol, not a claim about what the Voynich Manuscript is.

## Why the lane closes here

The roadmap deliberately required a candidate to be specified independently of the Voynich failure vector before a new target reveal. That requirement was applied prospectively to a narrow historical search rather than relaxed after failures.

The resulting chain is:

### T1463 — historical mixed-granularity family

Issue #183 established that the family is historically real, but the encoder choice among letters, digrams, doubles, nomenclator items, homophones, nulls and spacing could not be recovered sufficiently.

Result: **`H0_ARCHITECTURE_PARTIAL`**.

No invented encoder policy is licensed.

### TP1518-WA0 — Trithemius sequential word alphabets

Issue #207 recovered a much cleaner historical architecture:

- one code-bearing word per hidden Roman-letter position;
- ordered alphabet advance without skipping;
- documented inverse;
- explicit distinction between code-bearing and auxiliary/filler words;
- documented restart/continuation options.

A bounded external-only test passed:

`ABC -> Deus / Clementissimus / Conservans -> ABC`.

The frozen three-alphabet serialization contains 72 table cells, costs 1,151 UTF-8 bytes / 9,208 bits and has SHA-256:

`ddfbecb0666b4d840a384e0dbf8ae1937769c609a95d538a8a21a27a28a50ad4`.

Priority-5 admission then asked whether a complete exact historical restart cycle could be obtained mechanically without hand repair. Issue #209 found:

- 895 emitted machine-readable substitution columns;
- 723 complete 24/24 columns;
- 172 incomplete columns;
- 52 columns with exact within-column duplicate outputs;
- 40 duplicate-output collisions even among nominally complete 24/24 columns;
- observable column-label gaps in 41 of 63 emitted chunks;
- none of the three source-cross-checked #207 initial table prefixes appears exactly in the emitted column set.

Result: **`MACHINE_EXTRACTION_PARTIAL`**.

The stop rule prohibited manually repairing hundreds of cells or sequence relations to force admission. TP1518 therefore remains a valuable historical architecture/control but receives no Voynich target score.

### B1623-BL0 — Bacon biliteral / `omnia per omnia`

Issue #211 tested the fallback already named prospectively in #207.

The historical core is exceptionally clean:

- 24 hidden letter classes;
- exactly five ordered binary positions per class;
- exact inverse when five-position synchronization is known;
- `I/J` and `U/V` are merged classes;
- the frozen 24-entry table serialization is 192 UTF-8 bytes / 1,536 bits;
- SHA-256 `191bdb4787baa75011634085700b2e216d234d6ff732f48683d836ef698fdf7a`.

External-only round trip:

`BACON -> aaaab aaaaa aaaba abbab abbaa -> BACON`.

Historical core result: **`H0_ARCHITECTURE_RECOVERED`**.

However, Bacon deliberately separates the hidden binary channel from the visible carrier. The two exterior forms carry `a/b`; the carrier letters/objects, visible spaces, lineation and discourse can otherwise be chosen independently. Therefore the cipher core does not itself determine the candidate surface required by the frozen #172 R1–R8 responsibilities.

A Voynich target entry would require at least one additional rule for:

- exterior carrier identity/content;
- visible bounded units/spaces;
- line and paragraph organization;
- the two-form `a/b` classifier;
- mapping to the frozen target atom representation;
- five-position synchronization in the visible stream.

Selecting any of those from Voynich behavior would create a new target-derived surface generator around the historical binary core. Allowing an arbitrary carrier would instead permit most surface structure to be imported through a high-capacity side channel.

Target-adapter result: **`HISTORICAL_CORE_ONLY_TARGET_ADAPTER_UNDERSPECIFIED`**.

No Voynich target score is licensed.

## What has actually been learned

The failed admissions are informative because they fail for different reasons.

| Family | Historical mechanism | Exact inverse | Surface mechanism sufficiently fixed | Target admission |
|---|---|---|---|---|
| T1463 | real but choice policy incomplete | not fully recoverable as frozen encoder | no | stop at H0 |
| TP1518-WA0 | recovered for bounded strict core | yes, bounded source-verified prefix | architecture yes; complete exact machine codebook unavailable | stop before target |
| B1623-BL0 | recovered | yes for 24 classes with synchronization | no; visible carrier intentionally underdetermined | stop before target |

This sharpens the admission requirement. A useful future candidate needs both:

1. a recoverable/invertible information mechanism; and
2. an independently specified **surface-production mechanism** that fixes the visible bounded units, local construction and hierarchy strongly enough for the #172 responsibilities.

Recoverability alone is insufficient. Historical authenticity alone is insufficient. A flexible carrier is also insufficient because it can hide arbitrary surface complexity.

## Relation to the frozen historical anchors

Issue #176 remains the current joint calibration:

- A1/A1-R1: `PARTIAL STRUCTURAL MODEL`; PASS R1/R3/R4/R10, FAIL R2/R5/R6/R7/R8;
- Naibbe C1-E0: `PARTIAL STRUCTURAL MODEL`; PASS R1/R2/R8/R10, FAIL R3/R4/R5/R6/R7/R9.

Their complementary success sets remain useful evidence about what a future mechanism must jointly explain. They are not combined ad hoc.

No new mechanism has now met the external admission conditions required to justify another target reveal. Therefore there is no scientific value in running a ceremonial joint tournament with no new entrant.

## Frozen near-term stopping rule

Under the current roadmap:

- do not search another historical family merely because T1463, TP1518 and Bacon failed different admission gates;
- do not repair TP1518 source tables manually to force a full codebook;
- do not search Voynich for a favorable Bacon `a/b` partition, five-position offset or paired-allograph system;
- do not graft an arbitrary carrier generator onto Bacon;
- do not patch A1 or Naibbe from their #176 failure vectors;
- do not open a new candidate target workflow without an independently motivated architecture and a new prospective admission freeze.

A future candidate may enter only if new external historical/mathematical evidence independently supplies a mechanism that is both executable and surface-composable before target scoring.

## What this closeout does not establish

This result does **not** establish:

- plaintext absence;
- absence of semantics;
- absence of cryptography;
- natural-language wordhood or non-wordhood of visible spaces;
- authorship or provenance;
- deliberate hoax/artificial origin;
- undecipherability;
- any specific historical mechanism.

The accepted result is narrower:

> The current externally motivated historical-mechanism search produced no new candidate that was simultaneously executable, recoverable where claimed, and compositionally specified enough to enter the frozen #172 structural target battery without target-derived repair.

## Program state after closeout

The R1–R10 contract remains useful as a **falsification/admission battery** rather than a leaderboard waiting for a winner.

The mechanism-candidate lane is paused pending new independent external evidence. Separately justified lanes remain separate, including the content/identifiability program and already-frozen mathematical/control work explicitly allowed by the roadmap.

Issue #172 should remain the parent scientific contract rather than being interpreted as solved or exhausted. A new mechanism phase would require an explicit prospective roadmap/admission decision first.
