# Predictive-information program closeout — Issue #88

Date: 2026-09-07
Normative parent: Issue #88
Status: **PROGRAM COMPLETE**

This document closes the predictive-information program started by Issue #88. It consolidates only results already accepted through frozen, held-out, provenance-controlled tests. Exact methods and numerical authorities remain in the Issue/phase-specific plans, first-reveal artifacts and provenance files.

## 1. Program question

Issue #88 was created to stop treating individual high-contrast Voynich summaries as if they were sufficient explanations. Its core question was:

> how much held-out predictive information exists beyond the token-internal baseline, which observable mechanisms carry it, which parts transport across manuscript strata and independent transcription readings, and whether any reproducible residual remains that justifies a richer hidden-state mechanism?

That question is now answered to the resolution of the frozen model families tested by the program.

## 2. Program-level conclusion

The Voynich Manuscript is **not deciphered**.

The strongest accepted surface-production description is compact and observable:

1. literal certain visible spaces behave as reproducible construction/production boundaries in both ZL3b and Takahashi/IT2a;
2. inside each bounded unit, token topology is largely captured by a small second-order occupied-slot construction grammar;
3. cross-unit predictive information is real but small relative to token-internal information;
4. very local cross-unit structure includes both near-family recurrence/cache and a same-source-line previous-terminal → next-initial edge;
5. source-line breaks reset the useful raw edge context;
6. slower predictive structure is dominated by causal-prefix / prior-paragraph inventory rather than detailed long ordered memory;
7. the terminal→initial edge architecture and one reading-balanced common-EVA base table are stable across ZL3b/IT2a;
8. Currier A/B adds real edge information, but Issue #161 shows that the Currier distinction does **not** require a robust previous-terminal-specific interaction: a context-invariant next-initial bias is sufficient;
9. Issue #167 shows that this Currier next-initial bias is not ultra-sparse: the preregistered top-16 training-ranked outcome support is the first tested sparse rung that suffices prospectively in all four reading×Currier cells;
10. Issue #165 does not support promoting true section/domain labels beyond that compact Currier model;
11. after the validated observable mechanisms are added, Issue #134 finds **no robust held-out residual** for the stronger flexible challengers, so rich latent-state escalation is not licensed.

A compact shorthand for the currently accepted local construction layer is:

> **production boundary + compact within-unit grammar + shared common-EVA terminal→initial base edge + Currier-specific context-invariant next-initial bias + observable short/slow history.**

## 3. Boundary construct validity — completed

Phase 4A/4B directly challenged the visible-space assumption without using SlotParser eligibility.

ZL3b:

- reset contrast `D_RESET = +8.811905 bits/event`, positive 5/5;
- observed cut beats the one-atom-left shift in 5/5;
- observed cut beats the one-atom-right shift in 5/5.

Takahashi/IT2a:

- `D_RESET = +8.092615 bits/event`, positive 5/5;
- observed cut again beats both shifts in 5/5.

Frozen cross-reading classification:

> **`VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a`**

This licenses “construction/production unit” under the tested representations. It does **not** license “natural-language word”.

## 4. Token-internal construction — compact

Issue #75 and OGH-A/B/C establish that the replicated residual token topology is nearly reproduced by a target-blind second-order occupied-slot successor model:

- 66-edge residual topology authority;
- 298 counted conditional probabilities;
- median topology agreement approximately `0.948` on ZL3b and `0.962` on IT2a;
- memoryless V2 code length approximately `9.7089061 bits/token`;
- approximate token information split: shape `~7.0 bits/token`, values add `~2.7`.

This is a compact construction grammar, not a semantic lexicon.

## 5. Cross-unit predictive-information budget — real but small

After source-order correction:

- B0 V2: `9.7089061 bits/token`;
- B1 local history: `9.5943670`;
- B2 longer causal history: `9.5461692`;
- B3 + observable line/paragraph state: `9.5172688`.

The tested B0→B3 improvement is about `0.19164 bit/token`, far smaller than the information inside a bounded unit.

Longer-history gain is dominated by causal-prefix / prior-paragraph inventory. Detailed long ordered-memory residual is much smaller.

## 6. Immediate raw context localizes to a same-line edge

The flexible residual was progressively localized:

- Issue #118: a small positive flexible residual remains;
- Issue #121: the residual survives after fixing both challengers to `k=2, alpha=.01`;
- Issue #123: same-line continuation is positive, carrying context beyond a line break is harmful;
- Issue #125: the fixed line-local expert is exactly represented by generic onset/position plus previous-terminal identity.

Issue #125:

- generic position/onset gain `+0.00889185 bit/token`, positive 5/5;
- terminal identity adds `+0.02026956`, positive 5/5;
- `EDGE2` and `LINECONT2` token log probabilities are exactly equal.

Thus the useful raw short context does not require an unspecified line-local hidden state.

## 7. Observable-core residual closes — no latent-state license

Issue #134 prospectively augments corrected B3 with the observable edge and then gives stronger flexible RESET/LINE challengers another chance.

Authoritative first reveal:

- corrected B3 mean `9.517268842963203 bits/token`;
- augmented observable core mean `9.451900585480233`;
- gain over B3 `+0.06536825748296984`, positive 5/5;
- RESET selects final `w=0.0` in all five folds;
- LINE selects final `w=0.0` in all five folds;
- `G_residual=[0,0,0,0,0]`.

Frozen classification:

> **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**

Authority: run `34035108074`, artifact `9990011421`, result SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.

This does not prove hidden state is absent. It means the tested data do not justify paying for it after the observable responsibilities are included.

## 8. Edge replication and common representation

Issue #139 independently replicates the edge in Takahashi/IT2a:

> **`INDEPENDENT EDGE REPLICATION PASSES`**

mean gain `+0.1521118854 bit/token`, positive 5/5.

Issue #145 freezes one common Basic-EVA representation:

> **`COMMON-EVA EDGE ROBUST IN BOTH READINGS`**

- ZL3b `+0.1336232955`, 5/5;
- IT2a `+0.1618499834`, 5/5.

Issue #148 then transports the literal common-EVA edge table:

> **`COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`**

with approximately 96–98% retention of the target-native edge gain.

Issue #151 collapses the two reading-native tables:

> **`ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`**

No robust reading-specific table residual remains.

The edge is therefore not a ZL3b-only transcription artifact under the tested common-EVA representation.

## 9. Currier A/B is a real observable gate

Issue #155 shows the stabilized literal edge table is not interchangeable across Currier A/B:

> **`COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE`**

Wrong-regime literal transport is strongly negative in every reading×direction cell, while same-regime tables remain useful.

Issue #158 then measures the incremental information of the observable Currier label relative to a support-matched pooled table:

> **`CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B`**

Currier A:

- ZL3b `+0.0632767341`, 4/5;
- IT2a `+0.0678261662`, 4/5.

Currier B:

- ZL3b `+0.1012061293`, 5/5;
- IT2a `+0.1045681122`, 5/5.

The incremental Currier magnitudes are nearly identical across the two independent readings within each regime.

## 10. Currier difference factorizes globally — Issue #161

Issue #161 asks whether the Currier distinction requires a genuine Currier×previous-terminal×next-initial interaction or can be represented as a global next-initial bias applied to the shared pooled edge table.

Frozen classification:

> **`NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL`**

Thus the accepted Currier responsibility is reduced to a context-invariant next-initial multiplier rather than a second full previous-terminal-conditioned table.

Authority:

- Gate0 merge `6192e5cbe0a5212d089f890ca26bb7d9a10eedbf`;
- scorer blob `d24149977770118505f2147c5aa2bb727631906f`;
- run `34077382499`;
- artifact `10002558153`;
- result SHA-256 `11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031`;
- science merge `72ff98da2eac4b830dd02eae7623577362c29150`.

## 11. Section/domain does not earn another model gate — Issue #165

Issue #165 tests a preregistered section×next-initial factor on the only support-identifiable Currier-B contrast (`I=B` vs `I=S`) with a frozen one-leaf-left placebo.

Frozen classification:

> **`NO ROBUST SECTION/DOMAIN OUTCOME INFORMATION`**

Raw section gain is small and positive in both readings, but the true section labels do not beat the fixed placebo. Currier A is unscorable under the frozen support rule and scribe is not identifiable because of confounding.

Authority:

- run `34078834259`;
- artifact `10003041494`;
- result SHA-256 `0b124ac9b3bbeb3a1a8165390e63176ff30594d46ae45e49be5536efa7e8805c`;
- merge `5545b2657d058abea7973df2386a095b805669ef`.

## 12. Currier outcome bias is moderately broad, not ultra-sparse — Issue #167

Issue #167 freezes a training-only Jeffreys-divergence ranking of the 32 common-EVA next-initial outcomes and evaluates exactly `K={1,2,4,8,16}`.

A K is sufficient only if all four reading×Currier cells have useful sparse gain and none has a robust full-over-sparse residual.

Frozen classification:

> **`CURRIER OUTCOME BIAS SPARSE SUPPORT: K=16 SUFFICES`**

Key boundary:

- K=1/2/4: robust missing residual remains in all four cells;
- K=8: Currier A is adequately captured, but Currier B still has a robust missing residual in both readings;
- K=16: no cell retains a robust full-over-sparse residual.

At K=16 mean `G_missing` is approximately zero:

- ZL3b/A `-0.0008523004`, 1/5 positive;
- ZL3b/B `+0.0009069362`, 3/5;
- IT2a/A `-0.0001418704`, 2/5;
- IT2a/B `+0.0001441156`, 3/5.

Authority:

- Gate0 merge `bb56158e907d7253758cc5a0d8bc4dfa2606f1c7`;
- scorer commit `7c3d29e48ecb5026b11b065c7816ac4bb0d447a2`;
- scorer blob `5e67cecc312b431791c6623d1077ac46533fce0a`;
- workflow head `148faf934a917239d2059a8215de48a799b89b48`;
- run `34079999067`;
- artifact `10003436653`;
- artifact ZIP digest `sha256:f7b698cc44c914e54baa83228823bbb67d6b1b72b759974177e3795baa91a41b`;
- result SHA-256 `a532136b821d3c42f7b340729961da438f1f7cbd9bf20afb73408261d8d7befd`;
- merge `9e2a47b24aac362c8b1dc646417bf7a3faccbec1`.

The common 15-member core of the Gate0 top-16 training rankings is descriptively stable across all five folds, but no new K=15 target test is promoted from the already-revealed #167 result.

## 13. What the program falsified or failed to license

The completed program rejects or declines to promote the following tested explanations:

- a purely token-internal memoryless generator as a manuscript-level explanation;
- detailed long ordered memory as the dominant longer-history mechanism;
- useful short raw context continuing across source-line breaks;
- a reading-specific ZL3b-only edge architecture;
- one Currier-neutral literal edge table;
- a Currier-specific full previous-terminal interaction after the global next-initial bias is included;
- an ultra-sparse 1–8-outcome explanation as sufficient for both Currier regimes;
- true section/domain labels as an additional predictive gate under the identifiable support;
- rich latent-state escalation after the augmented observable core.

These are model-family results, not ontological proofs.

## 14. Program stopping rule is met

Issue #88's remaining licensing question after Phase 4 was whether a stronger flexible challenger retained reproducible held-out information after validated observable mechanisms were combined.

Issue #134 answered that question prospectively with zero selected residual in all folds. Issues #139–#167 then strengthened, transported, factorized and compressed the observable edge responsibility rather than reopening a hidden-state residual.

Therefore the #88 predictive-information program has reached its stopping condition:

> **The currently tested predictive responsibilities can be assigned to compact observable mechanisms without a reproducible residual that licenses richer latent-state modeling.**

Future work should not continue by shaving parameters from the same revealed target set or by adding local repair terms. It should move to a new scientific program with a new question.

## 15. Next-program handoff

The appropriate next frontier is **mechanism discrimination under a frozen structural contract**.

A future reversible decoder or surface generator should be challenged against the now-established responsibilities simultaneously, rather than being tuned to one legacy summary at a time. At minimum the contract should include:

1. transcription-lineage-robust visible-space production boundaries;
2. compact token-internal topology/construction responsibility;
3. manuscript-wide/local near-family recurrence where historically frozen;
4. signed paragraph-entry responsibility where historically frozen;
5. same-line terminal→initial edge with line-break reset;
6. one common-EVA reading-balanced base edge table;
7. Currier-specific context-invariant next-initial bias with the #167 moderate-support result;
8. slower causal-prefix/prior-paragraph inventory responsibility with Currier-dependent strength;
9. reversibility/recoverability for any decoder claim;
10. explicit complexity and target-information accounting.

The new program must freeze candidate architectures and scoring responsibilities before target reveal. Failure of a candidate remains a failure; it is not repaired inside the same confirmatory phase.

## 16. Interpretation boundary

Nothing in this closeout establishes:

- plaintext;
- semantics;
- natural-language wordhood;
- a language family;
- a cipher family;
- authorship or scribe causation;
- historical direction or production mechanism;
- artificial/hoax origin;
- decipherment.

The program establishes a reproducible **surface-production constraint system** that future mechanism hypotheses must explain.
