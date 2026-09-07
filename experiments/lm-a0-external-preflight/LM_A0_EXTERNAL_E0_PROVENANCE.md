# LM-A0 external E0 reveal provenance

Date: 2026-09-07
Parent: Issue #180 / Issue #172
Plan: `research/LM_A0_EXTERNAL_PREFLIGHT_PLAN_20260907.md`
Outcome: **E0_NO_EXTERNAL_SUPPORT_ON_THIS_SAMPLE**

## Frozen authority

External source:

- repository: `michaelscho/transpy`
- repository commit: `7487dd18adb2bbb7194f3f4d32c03e04ac084626`
- file: `new_file.xml`
- Git blob: `b6addd83de208dc97e2013f45978a8d333b02a4f`
- downloaded source SHA-256: `242557b5333d2aa30b1109a80f690858a486b02813cab4a302768556f64599ad`
- TEI: Bamberg, Staatsbibliothek, Can. 6, *Decretum Burchardi*, Book 07

Frozen plan commit:

- `7f114f4b4677ec8c999b0af2b1b63b2cfb0d391c`

Frozen scorer commit:

- `61e9e44fc18180c2dbb80a085979a25414e87fbb`

## Pre-reveal runtime recovery

Initial workflow run `34120364280` failed before writing a result.

The external file downloaded successfully and its SHA-256 was already fixed, but lxml encountered an XML comment whose `.tag` is a non-string callable object. The frozen helper `lname()` assumed a string and raised `TypeError` before `collect_lines()` returned and before any E0 statistic was emitted.

No count, effect size, p-value or classification was revealed by that run.

Recovery commit:

- `b5aadcd0f7950aa75a162e9fc3c682a1768ee82d`
- file: `lm_a0_external_e0_recovery.py`

The recovery changes only XML-node dispatch: non-string tags are ignored. It does not change population rules, boundary exclusions, normalization, FINAL1/FINAL2 definitions, lexical conditioning, hypergeometric null, threshold, or classification.

Execution workflow recovery commit:

- `a1863e2d558441ea7c8a4f03d9b698fef0f22e2b`

Successful reveal:

- workflow run: `34120460343`
- artifact ID: `10017959610`
- artifact ZIP SHA-256: `ae881f057e79454ccbffbf94f04bad75f3f51fc51f20a57745623769c1d2fbf2`
- result JSON SHA-256: `a4d143bfe1531211d1983defa4e42d9559497f1ae36f002da2e7bc927e4a0bf6`

## Population

- raw physical line spans: 576
- eligible non-empty lines after frozen exclusions: 335
- excluded line indices: 239
- `break=no` boundaries: 130
- choices spanning a physical line break: 43
- `expan=ERROR` choices: 22
- eligible lexical occurrences: 1,685
- abbreviated occurrences: 376
- normalized expanded forms showing both abbreviated and unabbreviated realizations: 28

## Primary FINAL1 result

Frozen directional hypothesis: abbreviation is enriched in the final complete lexical token of a physical line, holding expanded lexical form fixed.

Observed:

- informative lexical strata: 15
- abbreviated line-final occurrences `X`: 7
- frozen null expectation: 11.5588972431
- z: -2.5257479715
- one-sided enrichment p: 0.9977654549
- descriptive doubled-tail p: 0.0236044152
- raw abbreviation rate at FINAL1: 0.1731343284
- raw abbreviation rate outside FINAL1: 0.2355555556

The observed effect is opposite to the preregistered enrichment direction.

## FINAL2 sensitivity

- informative strata: 18
- observed: 31
- expected: 33.9009531404
- z: -1.1941503968
- one-sided enrichment p: 0.9203287909
- descriptive doubled-tail p: 0.3218834585

The sensitivity is also negative in direction and therefore does not rescue the primary.

## Classification

Per the frozen E0 plan:

> **E0_NO_EXTERNAL_SUPPORT_ON_THIS_SAMPLE**

This is not evidence that medieval scribes never condition surface form on layout. The authority is one 11th-century working TEI file, and the tested mechanism was specifically line-final abbreviation enrichment under same-expanded-form control.

The result does establish that this first independently sourced external test does **not** support promoting LM-A0 on the basis of line-final abbreviation behavior. The stronger descriptive point is that the primary sample moves significantly in the opposite direction under the frozen two-sided diagnostic, so treating this sample as generic support for line-end compression would be misleading.

## Consequence for Issue #180

Do not modify LM-A0 to predict line-final abbreviation suppression merely because E0 showed it. That would be a post-reveal rescue.

Before any further external test, choose one of two routes prospectively:

1. reject LM-A0 as currently operationalized and return to architecture selection; or
2. identify a genuinely independent and historically closer external layout/allography mechanism whose prediction is specified before its data are scored.

Issue #179 remains sealed. No Voynich target score was computed in E0.
