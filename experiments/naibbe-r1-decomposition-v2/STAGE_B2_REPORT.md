# Issue #72 V2 — Stage B2 extended unchanged-Naibbe calibration report

Status:

> **`EXTENDED UNCHANGED-NAIBBE R1 DISTRIBUTION CALIBRATED`**

Stage B2 expands the unchanged published-Naibbe positive control from the five historically frozen Phase64B realizations to a complete prospectively frozen `rep0..rep24` population before any Issue #72 intervention R1 result is available.

It is a T2 measurement/positive-control calibration. It does **not** define a hard intervention threshold.

## 1. Exact scientific execution

- run: `33466133615`
- exact scientific head: `1799e4d20266406f4e26d93bde8ab770db17ee02`
- prepare chronology/authority gate: PASS
- all twenty new matrix jobs `rep5..rep24`: PASS
- aggregate validation: PASS
- aggregate artifact ID: `9784965611`
- artifact ZIP SHA-256: `8b13008d5720be82051fd73a22042350aecfaae1aea5156652680bd87c370ab7`
- exact raw `stage_b2_calibration.json` SHA-256: `2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147`
- raw size: `157,852` bytes

The B2a archive-transport repair was verified byte-for-byte before scoring. It changed no scientific input.

## 2. 25-realization unchanged-mechanism distribution

| coordinate | mean | median | MAD | population SD | min | max |
|---|---:|---:|---:|---:|---:|---:|
| parser coverage | 0.886355 | 0.886370 | 0.000937 | 0.001529 | 0.883244 | 0.889807 |
| residual energy E | 3.178233 | 3.178404 | 0.013325 | 0.019282 | 3.135055 | 3.217277 |
| fold reliability W | 0.959413 | 0.960387 | 0.005661 | 0.009103 | 0.938317 | 0.976304 |
| R to ZL3b | 0.872623 | 0.871290 | 0.008978 | 0.010907 | 0.853387 | 0.895833 |
| R to IT2a | 0.887029 | 0.887084 | 0.005799 | 0.008562 | 0.872508 | 0.907536 |
| `M_R=min(R_ZL3b,R_IT2a)` | 0.872623 | 0.871290 | 0.008978 | 0.010907 | 0.853387 | 0.895833 |
| ZL3b sign agreement /66 | 59.6 | 60 | 0 | 0.566 | 59 | 61 |
| IT2a sign agreement /66 | 60.6 | 61 | 0 | 0.566 | 60 | 62 |
| `M_sign` /66 | 59.6 | 60 | 0 | 0.566 | 59 | 61 |

The target-limiting reading for all 25 realizations is ZL3b, hence `M_R = R_ZL3b` in this population.

## 3. Internal topology repeatability remains very high

Across all `C(25,2)=300` pairs of unchanged published-Naibbe residual-Z graphs:

- Pearson correlation minimum: `0.9761239364746696`
- median: `0.9916670321955685`
- maximum: `0.9985428812799949`
- sign agreement minimum: `63/66`
- median: `65/66`
- maximum: `66/66`

Therefore the complete residual topology is a highly repeatable property of the published Naibbe mechanism/configuration on the frozen source panel, not a peculiarity of one random execution.

## 4. The original five-rep envelope was not a valid hard threshold

This is the most important calibration result.

When the twenty prospectively frozen new positive controls were compared against the min/max envelope of historical `rep0..rep4`:

### `M_R`

- below old five-rep range: `2/20`
- inside: `15/20`
- above: `3/20`

### W

- below old five-rep range: `1/20`
- inside: `7/20`
- above: `12/20`

### E

- below: `6/20`
- inside: `12/20`
- above: `2/20`

### coverage

- below: `6/20`
- inside: `12/20`
- above: `2/20`

Thus a rule such as "outside the first five known-positive values = failure" would have rejected multiple **unchanged executions of the same published mechanism**.

This directly validates the project-wide rule that threshold hardness cannot substitute for threshold validity.

## 5. Rep0 is valid but target-high, not a neutral mechanism-average path

Issue #68 used historical `rep0`.

Within the 25-realization unchanged population, rep0's empirical midrank locations are:

- coverage: `0.50`
- E: `0.50`
- W: `0.30`
- `M_R`: `0.86`
- `R_IT2a`: `0.94`
- `M_sign`: `0.70`

So rep0 is ordinary in coverage/energy and within the stable unchanged-mechanism family, but it is relatively high in target topology correlation.

This matters for Issue #72 V2. A fixed-path ablation applied only to rep0 estimates a legitimate **conditional effect on that exact path**, but rep0 alone is not sufficient to claim that the same emission-layer effect is typical across Naibbe process realizations.

Therefore Stage C should replicate fixed-path intervention effects across multiple process paths selected by an outcome-independent rule before intervention results are seen.

## 6. What B2 does and does not calibrate

B2 validates these uses:

- scale of ordinary unchanged-process variation;
- positive-control expectation for R1 geometry;
- whether an intervention displacement is small or large relative to normal execution variation;
- assessment of whether a chosen baseline trace is representative.

B2 does **not** validate:

- a worst-positive hard cutoff;
- a Gaussian fitted truth interval;
- a new universal `R>=x` gate;
- the claim that R1 uniquely identifies Naibbe or any cipher family;
- the claim that a fixed-path structural ablation is itself valid historical ciphertext.

## 7. Implication for the intervention design

The next design should not ask merely whether an intervention crosses a human-set R1 boundary.

The stronger question is:

> **Is the published association systematically more Voynich-R1-like than outcome-independent association-destroying assignments, by an amount that is large relative to unchanged-mechanism execution variation, and does that displacement replicate across independently realized process paths?**

That points toward randomization inference/effect-distribution reporting rather than a manually chosen `.90/.70` retention band.

For ES/EG, where Stage A showed substantial parser-coverage loss, parser acceptance must remain an outcome. We must not condition away the post-intervention coverage change and then pretend the remaining parsed tokens are the same causal population. Instead the design must separately quantify:

1. representability/coverage change;
2. R1 geometry among the representable surface;
3. matched target-blind thinning controls estimating how much R1 movement would arise from comparable loss of accepted tokens alone.

No single combined scalar is authorized unless independently justified.

## 8. Firewall status after B2

At Stage B2 completion:

- EL R1: unrevealed
- ES R1: unrevealed
- ET R1: unrevealed
- EG R1: unrevealed
- PT R1: unrevealed
- FI R1: unrevealed
- no hard intervention threshold has been derived.

This preserves a clean prospective point for final Stage C criterion/randomization design.
