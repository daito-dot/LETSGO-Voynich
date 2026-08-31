# Issue #55B — occupancy-versus-subtype decomposition

Status: **PREREGISTERED — NO #55B TARGET REVEAL YET**

Parent result: #55A report commit `b3f2a341e1407c55d681b06d6bcce6c9caf4e7cd`, classification `CROSS-LEAF SLOT3xSLOT5 DEPENDENCE`.

## Motivation

#55A established a stable slot3↔slot5 relation beyond line-local marginal frequencies, but its pooled contingency table showed an extreme near-mutual-exclusion pattern. The next question is whether the apparent five-state×five-state dependence contains information beyond the binary fact that each slot is EMPTY or nonEMPTY.

This phase remains completely non-musical and non-semantic.

## Frozen representations

Reuse the exact #55A population, physical-leaf folds, parser, state order and primary `min` policy.

Full states:

- slot3: `EMPTY,t,k,p,f`;
- slot5: `EMPTY,cth,ckh,cph,cfh`.

Define binary occupancy variables deterministically:

- `B3 = 0` iff slot3 is EMPTY, else `1`;
- `B5 = 0` iff slot5 is EMPTY, else `1`.

No state regrouping other than this predeclared EMPTY/nonEMPTY collapse is allowed.

`max` remains sensitivity only.

## Question 1 — how much of the cross-leaf information gain is binary occupancy?

Repeat five-fold physical-leaf cross-fitting with Jeffreys smoothing `alpha=0.5` for the binary variables.

For each held fold calculate the symmetric binary predictive gain:

`Gbin = 0.5 * [(CE(B5)-CE(B5|B3)) + (CE(B3)-CE(B3|B5))]`.

Compare its equal-fold mean with the already-defined full-state gain `Gfull` computed from the exact same population and fold procedure.

Primary occupancy fraction:

`Focc = mean(Gbin) / mean(Gfull)`.

This is descriptive but enters the frozen classification below.

## Question 2 — does full subtype identity improve held-out prediction beyond occupancy?

Fit two directional conditional models on each training fold.

### Full model

Same as #55A:

- `P(S5 | S3)` and `P(S3 | S5)` over all five states.

### Occupancy-only interaction model

The model is allowed to use the binary occupancy interaction but not opposite-slot subtype identity.

To predict slot5 from slot3:

1. fit `P(B5 | B3)`;
2. if `B5=0`, the predicted slot5 state is EMPTY;
3. if `B5=1`, distribute that probability among `cth/ckh/cph/cfh` using the training marginal subtype distribution `P(S5 subtype | B5=1)`, independent of the slot3 subtype.

The reverse model is defined symmetrically for slot3.

All components use Jeffreys smoothing `alpha=0.5` within their relevant categorical support.

On the held fold calculate:

- `R5 = CE_occupancy_model(S5|S3) - CE_full(S5|S3)`;
- `R3 = CE_occupancy_model(S3|S5) - CE_full(S3|S5)`;
- `Rsym = (R3 + R5)/2`.

Positive `Rsym` means full five-state identity adds predictive information beyond EMPTY/nonEMPTY occupancy.

Primary residual statistic: equal-fold mean `Rsym`.

## Occupancy-preserving subtype null

Generate exactly 1,000 deterministic nulls.

For every physical line independently and for each slot independently:

- keep the EMPTY/nonEMPTY occupancy at every token position fixed exactly;
- among positions where slot3 is nonEMPTY, shuffle only the nonEMPTY slot3 subtype labels (`t/k/p/f`) without replacement;
- among positions where slot5 is nonEMPTY, shuffle only the nonEMPTY slot5 subtype labels (`cth/ckh/cph/cfh`) without replacement;
- do not move labels between lines, leaves or folds.

This preserves exactly:

- the complete token-level `(B3,B5)` occupancy pattern, including the near-mutual exclusion;
- line-local subtype frequency vectors for both slots;
- line/token counts and all structural boundaries.

It destroys only any exact subtype alignment that could provide information beyond occupancy.

Every null is cross-fitted from scratch and scored with the same full-versus-occupancy models.

Seed namespaces:

`Issue55B:Slot3SubtypeShuffle:v1:<null_index>:<page>:<paragraph>:<line_index>`

`Issue55B:Slot5SubtypeShuffle:v1:<null_index>:<page>:<paragraph>:<line_index>`

Upper-tail p-value:

`p_resid = (1 + # null mean Rsym >= real mean Rsym) / 1001`.

## Parser-admissibility audit

Independently of observed token frequencies, enumerate the 24 nonempty canonical strings obtained by concatenating each slot3 state with each slot5 state, excluding only `(EMPTY,EMPTY)`.

For every canonical pair ask whether the frozen `SlotParser.parses()` set contains at least one parse with:

- the intended slot3 state;
- the intended slot5 state;
- all other slot values EMPTY.

Report the number of exact canonical pairs admitted by the parser and list any failures.

This is diagnostic, not a statistical gate. If all 24 are admitted, the observed near-exclusion is not a hard impossibility imposed by the parser grammar itself.

## Rare co-occupancy audit

List every observed parsed token for which both slot3 and slot5 are nonEMPTY, including page/paragraph/line/token and the extracted pair. This is descriptive only and was specified before inspecting those token identities.

## Frozen classification

Classify primary `min` as **`DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`** if both:

1. `Focc >= .95`;
2. real mean `Rsym <= .005 bits/token`.

Classify as **`SUBTYPE-LEVEL SLOT3xSLOT5 DEPENDENCE REMAINS`** only if all:

1. `Focc < .95` or real mean `Rsym > .005`;
2. `p_resid <= .01`;
3. real mean `Rsym` exceeds the subtype-null median by at least `.01 bits/token`;
4. all five held folds have `Rsym > 0`.

Otherwise classify:

**`OCCUPANCY-DOMINANT WITH SMALL OR UNSTABLE SUBTYPE RESIDUAL`**.

The parser-admissibility audit and `max` sensitivity cannot promote a primary failure or change these numerical thresholds.

## Interpretation boundary

If the result reduces to binary occupancy exclusion, #55A should be retained as a real morphotactic constraint but the original E10 5×5 recurrence should not be interpreted as a 25-cell code or richer paired-state system.

A further follow-up would then ask what the two occupied forms represent structurally, for example alternative realizations of a common graphical/morphological feature, and whether the exclusion varies by token position or manuscript register.

If subtype-level information remains, a separate plan-first phase would test which subtype correspondences transfer across sections/transcriptions.
