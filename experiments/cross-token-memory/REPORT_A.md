# Issue #81 — minimal cross-token memory first reveal

Date: 2026-09-02
Base main: `3a55c53c9cdd57ccf9a48b29f50eb81ef43dead8` (PR #80 merged)
Science implementation: `c8654fdc72365426062ce8b62e9c7a65cbeb81b1`
Authoritative workflow run: `33612699253`, head `0c7933635e57ff1e2579a4ce69b0468fe45839e7`
First-reveal artifact: `issue81-first-reveal`, artifact id `9839900477`, artifact digest `sha256:05c6ccd834b7660d5247b713d70bfa3b76bd40a47509511ae9c96e14f75a207b`
Stage1 JSON SHA-256: `b7c3de603c2bed9a26ae9cc896bea69c88ff0f58bba1bab6b170cbda8032e584`
Final JSON SHA-256: `98aaabefec0409763f07e41badba3aff10027cc59b68cdcd73c66e2927ebb68e`

## Decision

No preregistered candidate recovers the full frozen conjunction `R1 + S1 + S2 + raw H62 + H62 profile`.

- X0: `INSUFFICIENT`
- X1 previous-token shape: `INSUFFICIENT`
- X2 previous-10 edit-1 activation: `INSUFFICIENT` under the frozen responsibility gate, but it is a close H62-profile miss and recovers S2 plus more than the target raw recurrence magnitude.
- X3 paragraph-entry state: `PARTIAL`; it recovers S1.
- X4: `NOT_LICENSED`. The prospective composition rule did not fire because X2 missed the frozen A1-R1 H62-profile regime by one component.

The Issue #68 R1 condition is not the blocker. X0, X1, X2 and X3 pass R1 in all three fixed realizations after surface regeneration and min-slot reparsing.

## First-reveal results

| model | held-out surface bits/token | S1 ratio | S2 ratio | raw H62 ratio | H62 mean D_profile | mean abs C_short diff | R1, 3/3 | frozen class |
|---|---:|---:|---:|---:|---:|---:|---|---|
| X0 | 9.70891 | 0.0329 | -0.0290 | 0.0912 | 1.33997 | 0.58978 | pass | INSUFFICIENT |
| X1 | 10.29337 | 0.0656 | 0.2914 | 0.6772 | 1.26220 | 0.30966 | pass | INSUFFICIENT |
| X2 | **9.64957** | 0.1051 | **0.7877** | **2.1227** | **0.75143** | **0.12569** | pass | INSUFFICIENT |
| X3 | 9.77167 | **0.7184** | 0.0021 | 0.3931 | 1.08758 | 0.34009 | pass | PARTIAL |

Frozen A1-R1 H62 comparator:

- mean `D_profile = 0.76650`
- mean `abs_C_short_diff = 0.11768`

X2 therefore beats A1-R1 on mean `D_profile` (`0.75143 < 0.76650`) but misses it on `abs_C_short_diff` by `0.00801` (`0.12569 > 0.11768`). Because `PLAN_A.md` required both to be no worse than the frozen A1-R1 means, X2 does not pass the full S2+H62 responsibility gate. No post-hoc X4 generation was permitted.

The raw H62 gate was deliberately only a lower bound. X2 passes it easily but produces `2.1227x` the held-out Voynich raw excess. That overshoot is scientifically relevant even though it is not a preregistered failure condition.

## X2 parameter selection and information cost

The single X2 parameter `pi` was selected independently inside every outer fold using only nested held-out literal surface likelihood on training leaves. S1, S2 and H62 were not available to the selector.

All five outer folds selected exactly:

`pi = 0.10`

The generated edit-1 memory-event rate is consequently about 10% and fallback is negligible.

The held-out surface code length changes from:

- X0 V2: `9.70891 bits/token`
- X2: `9.64957 bits/token`
- improvement: **`0.05934 bits/token`**

The improvement is positive in every fold and the same `pi=0.10` optimum appears in all five nested selections. The dependence is therefore detectable by predictive likelihood, but its average information contribution under this mechanism is small.

This directly rejects the prereveal expectation that the tested previous-10 near-family mechanism would account for a `2–3 bit/token` reduction from the 9.7-bit memoryless code length. It does **not** establish the unrestricted conditional entropy `H(token | previous 10)`; a more general predictive model could still capture other dependencies. The conclusion is narrower: the edit-1 near-family component tested here buys only about `0.06 bit/token` while producing a large S2/H62 effect.

That matters for the interpretation of H62. The recurrence statistic is a high-contrast local-structure measure, not evidence by itself for several bits of average cross-token information.

## X1 and X3

X1 confirms that previous-token occupancy shape alone is not the missing memory. It raises raw H62 from X0's `0.091x` target to `0.677x`, but S2 reaches only `0.291x`, the normalized recurrence profile remains far from A1-R1, and held-out code length worsens to `10.293 bits/token`.

X3 is cleaner. A two-state `ENTRY/BODY` emission table recovers the S1 sign and reaches `0.718x` the held-out Voynich S1 magnitude, comfortably inside the frozen `[0.5, 2.0]` range. It contributes essentially nothing to S2. The paragraph-entry effect and near-family locality therefore behave as separable cross-token responsibilities in this experiment.

## R1 retention

All tested candidates preserve the frozen 66-edge residual topology. Parser coverage is `1.0` for every realization, and every Issue #68 existence/topology gate passes.

ZL3b Pearson ranges across the three fixed realizations:

- X0: `0.948–0.959`
- X1: `0.922–0.940`
- X2: `0.954–0.964`
- X3: `0.954–0.960`

IT2a replication ranges:

- X0: `0.956–0.963`
- X1: `0.926–0.935`
- X2: `0.953–0.962`
- X3: `0.959–0.961`

This supports the existing factorization: the small token-internal occupancy grammar remains sufficient for R1 while cross-token states can be changed without destroying it.

## Prereveal predictions versus result

1. **X1 would fail:** supported. It recovers some raw recurrence but not S2/H62 as a mechanism family.
2. **X2 would recover S2 and raw H62:** supported. S2 is `0.788x`; raw H62 is `2.123x`.
3. **X2 C_short would remain around 0.3 away from target:** not supported. Mean absolute C_short difference is `0.126`, almost exactly the frozen A1-R1 regime (`0.118`). This was the largest directional miss in the prereveal forecast.
4. **X3 would get the S1 sign but probably less than half the magnitude:** sign prediction supported, magnitude prediction too pessimistic. X3 reaches `0.718x`.
5. **X4 would probably be needed:** the division of responsibility points that way, but the preregistered X4 trigger did not fire. Running X4 now would be post-hoc and is excluded from Issue #81.
6. **Near-family memory would remove 2–3 bits/token:** not supported for X2. The measured gain is `0.059 bit/token`.

## Consequences for the information argument

The prior 9.7-bit token budget remains approximately intact after accounting for the tested near-family dependency. For this mechanism, the predictive code length is about `9.65 bits/token`, not 7–8.

Therefore the earlier inference that local recurrence necessarily reduces usable token capacity by another 2–3 bits should be withdrawn. This does not make a one-token/one-word substitution model likely or establish any plaintext mapping; it only removes that specific entropy subtraction as evidence against it. The structural objections established elsewhere remain separate evidence.

The new picture is more asymmetric than expected: a small average predictive dependency can produce a conspicuous recurrence fingerprint. H62 should not be converted directly into an information-rate estimate.

## Next frontier

Do not tune X2's `pi` against H62 after this reveal and do not run the blocked X4 as if it had been preregistered.

The immediate unresolved question is why likelihood-selected X2 simultaneously:

- improves held-out prediction in every fold;
- reproduces S2 well;
- nearly matches A1-R1's normalized short-range profile;
- but produces about twice the raw H62 excess.

A follow-up should change the *form* of near-family activation rather than hand-set its strength from the target. Candidate extensions should be frozen and selected using training-leaf likelihood only. A recency kernel or a softer V2 reweighting of edit-1 neighbours are natural rivals; the target question is whether one can keep the predictive gain while matching both recurrence amount and lag profile. Only after such a near-family component passes its own responsibility should it be prospectively composed with the already-supported X3 ENTRY/BODY state.

S3 remains a diagnostic outside the Issue #81 recovery conjunction and is not recovered here.

## Interpretation boundary

Nothing in this result identifies plaintext, token meaning, cipher family, language, semantic absence, or a historical production mechanism. The result concerns the minimum statistical state needed to reproduce the frozen structural targets.