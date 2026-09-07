# Issue #165 — section/domain source-attribution transport plan

Date: 2026-09-07
Status: **FROZEN BEFORE GATE / TARGET SCORING**
Parent: Issue #88
Related: #84, #107, #109, #161

## Scientific question

After fixing the compact edge model selected by Issue #161, does IVTFF illustration/domain `$I` add held-out predictive information that transports across both ZL3b and Takahashi/IT2a?

The entry model is:

> **one shared terminal→initial base table + Currier-specific global next-initial bias.**

This issue asks only whether a further **section/domain × next-initial outcome** bias is required.

## Why scribe is not the primary arm

Issue #107 established that Davis hand `$H` is strongly confounded with Currier. A current audit of the frozen #107 metadata result additionally shows that within Currier B, the two large hands H2/H3 are strongly domain-confounded: H2 is concentrated in `I=B/H/T`, while H3 is overwhelmingly `I=S`; the only material common domain `I=H` has old accepted-token support in only 4 folds for H2 and 3 for H3.

Therefore this issue treats scribe as **support/identifiability audit only**. No scribe predictive score is licensed unless Gate0 independently finds adequate within-Currier, within-section crossing under the current common-EVA target population.

## Frozen entry authority

Issue #161:

- Gate0 merge `6192e5cbe0a5212d089f890ca26bb7d9a10eedbf`;
- Gate result SHA-256 `32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94`;
- Gate script blob `00e5bddc0484b9472bb4fce9dadb89dd52bf578f`;
- Gate provenance blob `67e91ba26a76898f679a5182828ab3e9f512d49a`;
- scientific scorer blob `d24149977770118505f2147c5aa2bb727631906f`;
- first-reveal provenance blob `73100548fef5dbc0d08a1951e3c0ca5b370cd6f4`;
- first-reveal result SHA-256 `11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031`;
- science merge `72ff98da2eac4b830dd02eae7623577362c29150`.

Issue #107 metadata authority:

- metadata scanner blob `110a6b848df71c4f51ec0d9dd3b262039d1fc66f`;
- authoritative Gate0 run `34049262845`;
- artifact `9985775083`;
- result SHA-256 `8f48a01ef4457f38a4e273fe32ea73b9f90817af156be0111bb56a550f443870`;
- classification `NO ADEQUATELY CROSSED OBSERVABLE FACTOR` for the old cross-Currier hand/section screen.

## Frozen metadata semantics

Reuse #107 exactly:

- `$I` = IVTFF illustration/domain code;
- `$H` = Lisa Fagin Davis hand code;
- `$L` = Currier authority;
- legal `@` page-header values are resolved by text tags;
- ZL3b source/mapping/order authority must reproduce exactly.

Candidate section labels are the complete observed set:

`A, B, C, H, P, S, T, Z`.

No post-Gate label merge/drop/rename is allowed.

## Frozen pure-leaf rule

Build the cross-reading section authority only from ZL3b metadata and physical leaf identity.

For every physical leaf, inspect all token-bearing mapped ZL3b loci, whether or not the token is a SlotParser primary target.

- if every token-bearing locus resolves to the same non-special `$I` label, assign `PURE_I=<label>`;
- if multiple non-special labels occur, or any locus is unresolved/special, assign `MIXED_OR_UNUSABLE`;
- only `PURE_I` leaves may enter section-science populations in either ZL3b or IT2a.

The resulting leaf→section map is target-blind and must be frozen by SHA-256.

## Frozen common-EVA target support

Reuse #161 exactly:

- common Basic-EVA, 31 observed atoms + END, `V=32`;
- maximal contiguous clean runs;
- the same physical-leaf Currier A_ONLY/B_ONLY labels;
- same five physical-leaf folds, SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`;
- primary score targets are SlotParser-accepted tokens;
- section support is counted on accepted **run-body** targets (`ti>0`) because the source-attribution factor applies to the same-line edge term.

For Currier regime `R` and section `S`, `S` is **eligible in R** iff all of the following hold:

1. at least 5 physical leaves satisfy both `PURE_I=S` and Currier `R`;
2. ZL3b has at least 300 primary run-body targets in at least 4/5 folds in that `R,S` population;
3. IT2a has at least 300 primary run-body targets in at least 4/5 folds in that `R,S` population.

A Currier regime is scientifically scorable only if at least two section levels are eligible in that regime. Thresholds are fixed and may not be weakened after Gate0.

## Frozen scribe identifiability audit

Build an analogous pure-leaf Davis-hand map from `$H`. Scribe remains unscored unless Gate0 finds at least two hand levels that each satisfy the same `>=300 in >=4/5 folds in both readings` criterion **inside the same Currier regime and at least one common eligible section stratum**.

If not, record `SCRIBE_NOT_IDENTIFIABLE` and do not fit any scribe model.

## Mandatory score-free Gate0

Before any real-target section-conditioned likelihood:

1. reproduce #161 Gate/scorer/provenance authority;
2. reproduce #107 metadata result SHA exactly;
3. freeze pure-I and pure-H physical-leaf maps and hashes;
4. freeze Currier×section×fold run-body target counts in both readings;
5. freeze eligible section sets per Currier using only the support rule above;
6. freeze which Currier regimes are scorable (`>=2` eligible sections);
7. freeze the scribe identifiability result;
8. for each outer fold and scorable Currier regime, freeze a deterministic section-placebo leaf map:
   - sort eligible training leaves by ascending physical leaf id;
   - read their actual section-label sequence in that order;
   - **left cyclic shift by one position**;
   - assign each current leaf the next leaf's actual section label, with last→first wrap;
   - if every leaf retains its original section label, mark that regime/fold invalid rather than changing permutation;
9. prove training leaves and held-out leaves do not overlap;
10. run target-free synthetic tests for pure-leaf classification, support eligibility, and one-position placebo rotation;
11. compute no real-target section probability, likelihood, `G_section`, `G_placebo`, or scientific classification.

If no Currier regime is scorable, Gate0 stops INVALID.

## Frozen scientific model family

The scientific phase may add only a low-dimensional section-specific global next-initial bias on top of the #161 compact Currier model.

For outer fold `f`, Currier `R`, eligible section `S`, outcome `y`:

- aggregate training-only first-outcome counts over pure leaves in `R,S`;
- aggregate the corresponding Currier training counts over the union of all eligible sections in `R`;
- with fixed `alpha=.01`, form a section multiplier relative to that Currier aggregate;
- apply the multiplier context-invariantly to the #161 Currier-conditioned edge distribution and normalize exactly over the same 32 outcomes per retained previous-terminal context.

No section×previous-terminal interaction is allowed.

A placebo model uses the exact same construction but the frozen one-position shifted training leaf labels.

## Frozen primary quantities

For each reading `T`, scorable Currier regime `R`, and outer fold, score the union of target events from all eligible pure sections in `R`:

`G_section[T,R,f] = bits(EDGE_CURRIER) - bits(EDGE_SECTION)`

`G_placebo[T,R,f] = bits(EDGE_SECTION_SHUFFLED) - bits(EDGE_SECTION)`.

A Currier regime has robust section/domain information iff independently in both ZL3b and IT2a:

- mean `G_section > 0`;
- `G_section` positive in >=4/5 folds;
- mean `G_placebo > 0`;
- `G_placebo` positive in >=4/5 folds.

## Frozen classifications

Exactly one:

1. `SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER A AND B`
2. `SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER A ONLY`
3. `SECTION/DOMAIN ADDS ROBUST OUTCOME INFORMATION IN CURRIER B ONLY`
4. `NO ROBUST SECTION/DOMAIN OUTCOME INFORMATION`
5. `INVALID SECTION/DOMAIN SOURCE ATTRIBUTION`

Ineligible Currier regimes cannot count as robust; they remain `UNSCORABLE_BY_FROZEN_SUPPORT` and the joint class is determined by scorable regimes only. If neither regime is scorable, class is INVALID.

## Firewall

Do not:

- use held-out target outcomes for section eligibility or label construction;
- score mixed/unresolved leaves;
- change Currier labels, folds, common-EVA representation, #161 base/Currier model, target population, k, alpha, smoothing or fallback;
- add section×terminal interactions;
- fit scribe effects if Gate0 says non-identifiable;
- repeat/search shuffled permutations;
- interpret illustration labels semantically;
- fit latent states or tune S1/S2/H62/R1;
- infer plaintext, language/cipher family, authorship, historical direction/mechanism, artificiality/hoax, word boundaries, or decipherment.

Refs #84 #88 #107 #109 #151 #155 #158 #161 #164 #165.
