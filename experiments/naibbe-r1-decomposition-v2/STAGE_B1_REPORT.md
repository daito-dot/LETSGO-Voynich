# Issue #72 V2 — Stage B1 unchanged-Naibbe R1 calibration report

Status:

> **`UNCHANGED-NAIBBE R1 STOCHASTIC VARIATION CHARACTERIZED`**

This is a T2 positive-control calibration result. It is **not** an intervention PASS/FAIL threshold and it does not score any Issue #72 intervention.

## 1. What Stage B1 asked

Issue #68 established one published Naibbe realization (`rep0`) as R1-compatible. Before using that result to localize which Naibbe layer carries R1, Stage B1 asked:

> **How much does the complete R1 surface geometry vary across the five Naibbe realizations that were already frozen by Phase64B before R1 existed?**

The five historical surfaces were frozen target-blind in Stage B0 before B1 scoring.

B1 also separated genuine surface-to-surface stochastic variation from the Monte Carlo variation introduced by the finite 1,000-reference-null residual calibration itself.

No test-null p-value, maxT class, intervention surface, or intervention R1 quantity was computed.

## 2. Exact historical replay gate passed

Before rep1–rep4 could be scored, rep0 was required to reproduce the frozen Issue #68 coordinates under the exact historical reference-null namespace.

The gate passed to the preregistered `1e-12` scalar tolerance and exact sign counts:

- E `3.1784043855151296`;
- W `0.954726539114345`;
- ZL3b Pearson `0.8830282501011794`;
- IT2a Pearson `0.9000974100381157`;
- ZL3b signs `60/66`;
- IT2a signs `61/66`.

Therefore the B1 coordinate system is numerically continuous with the accepted Issue #68 R1 result.

## 3. Primary unchanged-mechanism results

All five rows use the exact same published Naibbe algorithm, codebook, source panel, parser and R1 scorer. Only the historically frozen stochastic realization seed differs.

| rep | coverage | E | W | r vs ZL3b | r vs IT2a | ZL signs | IT signs |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.886370 | 3.178404 | 0.954727 | 0.883028 | 0.900097 | 60/66 | 61/66 |
| 1 | 0.885210 | 3.175456 | 0.960387 | 0.882411 | 0.892744 | 60/66 | 61/66 |
| 2 | 0.885487 | 3.191729 | 0.959300 | 0.862283 | 0.883407 | 60/66 | 61/66 |
| 3 | 0.888162 | 3.165550 | 0.942791 | 0.857780 | 0.872508 | 59/66 | 60/66 |
| 4 | 0.887215 | 3.198378 | 0.951347 | 0.880108 | 0.897112 | 60/66 | 61/66 |

Observed primary ranges:

- coverage: `0.885210–0.888162`, range `0.002951`;
- E: `3.165550–3.198378`, range `0.032828`;
- W: `0.942791–0.960387`, range `0.017596`;
- ZL3b Pearson: `0.857780–0.883028`, range `0.025249`;
- IT2a Pearson: `0.872508–0.900097`, range `0.027589`;
- worst-reading Pearson `M_R`: `0.857780–0.883028`;
- ZL3b signs: `59–60/66`;
- IT2a signs: `60–61/66`;
- worst-reading signs: `59–60/66`.

The primary values stay in the same high-topology-agreement regime across all five independently frozen historical realizations. This is a robustness observation, not a newly defined hard gate.

## 4. Pairwise topology among unchanged Naibbe realizations

There are ten rep-pairs.

Complete 66-edge residual-Z correlation across rep pairs:

- minimum `0.9761239365`;
- median `0.9870032916`;
- maximum `0.9965315285`.

Complete-graph sign agreement:

- minimum `64/66`;
- median `65/66`;
- maximum `66/66`.

Thus the Naibbe R1 residual topology is highly stable to the historical stochastic realization seed even though the exact ciphertext surface and retry trajectory change.

This materially strengthens the interpretation of Issue #68:

> **Naibbe's R1 proximity is a repeatable property of the tested published mechanism/configuration, not evidence that rep0 happened to be a uniquely favorable stochastic draw.**

This still does not establish historical Naibbe use or explain which internal layer causes the property.

## 5. Finite-null calibration noise

For every identical real surface, B1 independently recalibrated residual Z with a second 1,000-reference-null population.

Primary-versus-secondary residual-Z correlation on the **same surface**:

- minimum `0.9996532159`;
- median `0.9998982625`;
- maximum `0.9999641372`.

Sign agreement was exactly:

- `66/66` for all five surfaces.

Maximum absolute primary-versus-secondary change:

- E: `0.0050842730`;
- W: `0.0024329804`;
- ZL3b Pearson: `0.0017859803`;
- IT2a Pearson: `0.0019714007`;
- sign agreement vs either target: `0` edges.

The observed between-rep primary ranges are larger than the maximum within-surface calibration perturbation by approximately:

- E: `6.46×`;
- W: `7.23×`;
- ZL3b Pearson: `14.14×`;
- IT2a Pearson: `13.99×`.

Therefore the measured rep-to-rep variation is resolvable above the finite-null calibration noise. Conversely, the calibration itself is stable enough that later large intervention effects should not be mistaken for ordinary reference-null Monte Carlo fluctuation.

## 6. Criterion-validity interpretation

### R1 topology as an unchanged-Naibbe positive control

Status:

> **CALIBRATED FOR ROLE**

The five historical unchanged-mechanism realizations show that the tested Naibbe configuration repeatedly occupies a very similar R1 topology regime.

### Five-rep spread as a hard intervention threshold

Status:

> **NOT AUTHORIZED**

`n=5` does not justify treating the worst positive-control value as a universal equivalence cutoff. B1 deliberately derives no intervention PASS/FAIL line.

### Finite-reference-null residual coordinates

Status:

> **CALIBRATED FOR ROLE**

Independent 1,000-reference recalibrations produce essentially identical complete-graph directions and very small target-correlation drift.

## 7. What B1 changes

Before B1, a later intervention could have differed from rep0 simply because published Naibbe itself is stochastic.

After B1, that background variation is empirically measured.

The next experiment should therefore not ask whether an intervention clears an arbitrary `0.90×` or `0.70×` barrier. It should ask a causally matched randomization question:

> **Is the published arrangement unusually R1-like relative to the exact intervention family that destroys one nominated association while preserving the quantities that intervention claims to hold fixed?**

B1 provides effect-size context for that comparison.

## 8. Claim boundary

B1 supports only the following strengthened statement:

> **Within the tested published Naibbe configuration, the R1 residual topology is highly stable across the five independently frozen historical stochastic realizations, and this variation is clearly larger than but still small relative to finite reference-null calibration noise.**

B1 does not establish:

- which codebook/process layer causes R1;
- that every Naibbe realization would satisfy the full Issue #68 confirmatory p-value gates;
- historical Naibbe use;
- encrypted Latin;
- decoder closure;
- decipherment.

Those require separate criteria and tests.
