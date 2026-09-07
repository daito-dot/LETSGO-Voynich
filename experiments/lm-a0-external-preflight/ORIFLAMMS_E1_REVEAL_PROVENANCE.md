# ORIFLAMMS E1 frozen reveal provenance

Date: 2026-09-07
Parent: Issue #180 / Issue #172
Outcome: **E1_NO_REPLICATION**

## Frozen chronology

The E1 scientific and selection plan was committed before any ORIFLAMMS abbreviation-position effect was computed. A metadata-only inventory then selected the full roster using only date/identity/markup criteria. The resulting 23-manuscript roster was frozen at commit `f370ed68982df9bfc56e68b30b519f247d8cd66e`.

A post-roster structure audit computed no effect statistic and established that the selected corpus has 90 `lb break="no"` boundaries, all represented inside words as `seg/lb/seg`. This permitted the preregistered split-word/both-adjacent-lines exclusion without text-driven inference.

The scorer was frozen at commit `5298c0ea5983992867d544906a719bef7c7eaf49`, synthetic-tested successfully in workflow run `34121851428`, and the complete pre-reveal state was recorded at commit `38851d89248161353322870c524624cf26b8d3e4`.

The reveal workflow deliberately checked out that exact pre-reveal commit rather than current moving `main`.

## Reveal authority

- workflow run: `34121929341`
- workflow trigger commit: `b991005c9b3a2a1ce5fb0f632e2480dbd0253075`
- exact checked-out scientific state: `38851d89248161353322870c524624cf26b8d3e4`
- result artifact ID: `10018521627`
- artifact ZIP SHA-256: `56e71466ea00f9836435599ba96e3e20e3faf0ca6cbe03b33dff743338037cf7`
- full `oriflamms_e1_result.json` SHA-256: `fe59e5588b08155f1378c0da2e376bcd8971071e5b126c70b673de39752f7880`

External data:

- `oriflamms/Dated-and-Datable-Manuscripts_LIRIS`
- pinned commit `93de4af4a470aea3f3b23c2e8bafcfa2161c5438`
- `abbreviations.dtd` SHA-256 `dac3775b16878f596cd51391ef3fdbac6238205c057ac209585245009461f0b2`
- `texts/mss-dates-w.xml` SHA-256 `d1ff8102e8c81f36d45a31143f9294cf5c061d55d879aed44244c858f65018e4`

The workflow re-ran the target-free synthetic preflight successfully immediately before the external reveal and asserted the pinned word-authority SHA-256 before scoring.

## Frozen population

- roster: 23 manuscripts, fixed before effect reveal
- candidate words before frozen exclusions: 2,882
- eligible words: 2,007
- raw physical line slots: 507
- bad line slots from frozen exclusions: 156
- eligible non-empty physical lines: 334
- split words excluded: 90
- `internal lb break=no`: 90
- empty-render words excluded: 52
- unresolved-choice words excluded: 18
- words containing deletion markup excluded: 3

## Primary FINAL1

Frozen prediction:

> Holding expanded lexical form fixed within manuscript, abbreviation is enriched when an occurrence is the final complete lexical token on a physical manuscript line.

Result:

- informative manuscript × lexeme strata: 10
- observed abbreviated FINAL1 occurrences: 8
- null expectation: 5.0000
- z = 1.9188064472
- preregistered one-sided enrichment p = **0.0525173611**
- descriptive two-sided doubled-tail p = 0.1050347222
- raw FINAL1 abbreviation rate = 0.2964071856
- raw non-FINAL1 abbreviation rate = 0.2833233712
- informative manuscripts = 6
- positive-direction informative manuscripts = 5/6 = 0.8333333333

The direction was consistent with the hypothesis and the manuscript-level sign criterion passed, but the preregistered `p <= 0.05` gate did not pass.

The informative manuscript deviations were:

- manuscript 62: +0.8333
- 64: +0.5000
- 71: +0.5000
- 72: -0.5000
- 73: +0.5000
- 80: +1.1667

The small number of informative manuscripts is a property of the frozen lexical-control design and corpus occurrences. It is not grounds for post-reveal subsetting, pooling across manuscripts, weakening lexical control, or changing the threshold.

## FINAL2 sensitivity

- informative strata: 14
- observed: 9
- expected: 6.6428571429
- z = 1.2942558765
- one-sided enrichment p = 0.1536923363
- descriptive two-sided doubled-tail p = 0.3073846726
- informative manuscripts = 9
- positive direction = 6/9 = 0.6666666667

The sensitivity is positive in direction but does not rescue the failed primary gate, by preregistration.

## Mechanical gate evaluation

The frozen E1 promotion conditions were:

1. at least 3 eligible manuscripts — **PASS** (23)
2. pooled FINAL1 observed > expected — **PASS**
3. pooled FINAL1 one-sided p <= 0.05 — **FAIL** (`0.052517...`)
4. at least two-thirds of informative manuscripts positive — **PASS** (5/6)
5. pooled FINAL2 observed > expected — **PASS**

Therefore the mechanically assigned classification is:

> **E1_NO_REPLICATION**

The result is close to the numerical gate, but the selection firewall specifically exists to prevent changing a threshold after such a reveal. No `p < 0.055` reinterpretation, one-stratum removal, manuscript filtering, FINAL2 substitution, or effect-direction rewrite is permitted.

## Combined reading with E0

E0 on the separate 11th-century Bamberg Can. 6 working TEI produced an effect opposite to the preregistered line-final enrichment direction (`z=-2.526`, one-sided enrichment `p=0.998`). E1 on 23 manuscripts nearer the target historical period moved in the predicted direction but narrowly missed the fixed primary threshold.

These two results do not justify a universal claim about medieval abbreviation practice. They do justify the narrower program decision required by Issue #180:

> **LM-A0, as currently operationalized by line-final abbreviation enrichment under same-expanded-form control, is not promoted to LM-A1.**

Do not invert LM-A0 to predict abbreviation suppression, relax the E1 threshold, add a cache, restrict to favorable scripts, or use the Voynich image-interruption test in Issue #179 as a rescue.

## Program consequence

Issue #179 remains exploratory and unlicensed for target scoring. The active program returns to Issue #172 architecture-class selection. Any next mechanism family must have independent mathematical/historical/scribal motivation before Voynich target access, and it must not be assembled from LM-A0 plus a second component chosen to cover the remaining R8 or other failure coordinates.

Permanent condensed result: `oriflamms_e1_result_summary.json`.
