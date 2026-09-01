# Issue #72 V2 — Stage B amendment B1: calibration noise and non-threshold role

Status: **FROZEN BEFORE ANY NEW rep1–rep4 R1 SCORE**

This amendment refines `STAGE_B_POSITIVE_CONTROL_PLAN.md` after the target-blind B0 support population was frozen and before any new rep1–rep4 R1 quantity exists.

B0 exact authority:

- raw JSON: `stage_b0_support.json`;
- SHA-256: `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`;
- workflow run: `33462658689`;
- all B0 target-access flags false.

## 1. Five unchanged-mechanism reps are a scale, not a hard threshold

The five historical Phase64B reps are an independently frozen positive-control family. However `n=5` is too small to define a scientifically privileged empirical tolerance boundary such as "an intervention passes if it remains above the worst positive control".

Therefore B1 will **not** turn rep0–rep4 min/max, median±constant, or any similar quantity into a decisive intervention threshold.

B1's role is T2 measurement calibration:

> estimate the observed scale of R1 stochastic realization variation under the unchanged published Naibbe mechanism.

Later intervention decisions must use intervention-specific prospective randomization or matched controls (T3 where applicable), with B1 variation reported as an effect-size context rather than as an obstacle-course cutoff.

This supersedes any reading of the original Stage-B plan that would allow the five-rep spread itself to become a hard PASS/FAIL gate.

## 2. Separate surface stochasticity from residual-calibration Monte Carlo noise

R1 residual Z coordinates are themselves estimated from a finite `N_ref=1000` line-local reference-null population. Therefore differences between rep0–rep4 can contain two sources:

1. true stochastic-surface variation of the unchanged Naibbe mechanism;
2. finite-reference-null Monte Carlo calibration variation.

B1 must estimate the second source rather than silently mix it into the first.

### Primary reference calibration

For each rep, generate exactly 1,000 reference nulls.

Namespaces:

- rep0 primary: exact Issue #68 historical namespace
  `issue68:B2:Naibbe:C1-E0:published-respaced:reference-null`
- rep1 primary:
  `issue72v2:positive-control:rep1:reference:primary`
- rep2 primary:
  `issue72v2:positive-control:rep2:reference:primary`
- rep3 primary:
  `issue72v2:positive-control:rep3:reference:primary`
- rep4 primary:
  `issue72v2:positive-control:rep4:reference:primary`

Rep0 uses the historical namespace so that the scorer is required to reproduce the already-frozen Issue #68 values exactly to numerical tolerance.

### Secondary independent reference calibration

For **every** rep0–rep4, generate a second independent 1,000-reference calibration:

`issue72v2:positive-control:rep<r>:reference:secondary`

The secondary calibration is a measurement-noise diagnostic only. It cannot replace the primary result because it looks more favorable.

## 3. Primary B1 coordinates

For each rep under its primary reference calibration, freeze:

- representation support from B0;
- complete real Q vector over all 66 edges;
- complete residual Z vector;
- residual energy E;
- four fold train/held correlations and median W;
- Pearson vs frozen ZL3b pooled residual vector;
- Pearson vs frozen IT2a pooled residual vector;
- sign agreement out of 66 vs both readings;
- `M_R = min(R_ZL3b, R_IT2a)`;
- `M_sign = min(sign_ZL3b, sign_IT2a)`.

No B1 PASS/FAIL class is defined from these coordinates.

## 4. Calibration-noise coordinates

For each rep, compare primary vs secondary reference-calibrated outputs on the exact same real surface:

- `corr_Z_primary_secondary` over 66 edges;
- `sign_Z_primary_secondary` out of 66;
- absolute difference in E;
- absolute difference in W;
- absolute difference in R vs each target reading;
- absolute difference in sign agreement vs each target reading.

Across five reps, report the full values and maxima. Do not hide the worst calibration-noise case.

This answers whether observed between-rep variation is resolvable relative to finite-null calibration noise.

## 5. No independent test-null p-values in B1

B1 is not trying to re-prove five times that unchanged Naibbe beats the line-local null. Rep0 already has exact historical Issue #68 test-null confirmation.

Therefore:

- no B1 `N_test` family;
- no new existence p-values;
- no maxT p-values;
- no R1 PASS/FAIL classification.

The reference null is retained because it defines the residual coordinate system, not because p-value stringency is the purpose of B1.

## 6. Exact rep0 replay requirement

Before any rep1–rep4 B1 values are accepted, rep0 primary must reproduce:

- E `3.1784043855151296`;
- W `0.954726539114345`;
- ZL3b Pearson `0.8830282501011794`;
- IT2a Pearson `0.9000974100381157`;
- ZL3b sign agreement `60/66`;
- IT2a sign agreement `61/66`.

Tolerance for floating-point scalar reproduction:

`abs(new - frozen) <= 1e-12`

Sign counts must match exactly.

If this fails, the B1 scorer stops and **must not emit rep1–rep4 R1 values**.

This is T1 implementation identity, not a statistical threshold.

## 7. Later intervention criterion design

After B1, the preferred later design is:

- fixed-path EL/ES/ET/EG: identity published association compared prospectively with a family of target-independent mapping permutations under the exact same realized path;
- PT: published plaintext order compared with prospectively generated within-line order randomizations passed through the full pipeline;
- FI: published token-to-layout assignment compared with prospectively generated whole-token instance permutations under its fixed preserved quantities.

These designs can support direct randomization-inference questions such as:

> Is the published arrangement unusually R1-like relative to the exact intervention family that destroys the nominated association while preserving its declared lower-order quantities?

B1 then supplies the scale of ordinary unchanged-mechanism variation, not an arbitrary hard barrier.

No intervention family size, randomization statistic, or multiplicity rule may be selected after any Issue #72 intervention R1 value is revealed.

## 8. B1 allowed conclusion

B1's scientific conclusion is descriptive/calibrative:

> **UNCHANGED-NAIBBE R1 STOCHASTIC VARIATION CHARACTERIZED**

with an explicit statement of whether finite-null calibration noise is small, comparable to, or large relative to the observed rep-to-rep spread in each coordinate.

No stronger causal or mechanism claim is licensed by B1 alone.
