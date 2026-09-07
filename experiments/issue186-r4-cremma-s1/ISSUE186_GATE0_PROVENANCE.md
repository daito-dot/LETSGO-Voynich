# Issue #186 — R4 / CREMMA Gate0 provenance

Date: 2026-09-08  
Parent: Issue #186 / Issue #172  
Status: **GATE0 VALID — SCORE-FREE COMPOSABILITY AUDIT COMPLETE**

## Frozen authority

- base main: `224c0130016e533823df14df682a30ca668b88e6`
- Gate0 PR: #187
- Gate0 branch: `issue186-r4-cremma-s1-gate0`
- Gate0 scoring-free head: `c5c04e19c1d0fd9d282c1b1d2c618cac784522b1`
- plan blob: `2060cc6381ac42a3cc48ec3b4443128f4d781b62`
- auditor blob: `9e3e869c476ff1ca4986639f7d8ec0ab2bea0424`
- workflow blob: `9d021c5036e11af9830a759b1670e4ae6a0d766d`
- historical Phase62B implementation blob: `e0ada366845c7a6c5a5dd75de91fe262b72a94b6`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`
- ZL3b mirror commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- ZL3b git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

## GitHub Actions execution

- workflow: `Issue186 R4 CREMMA S1 Gate0`
- run ID: `34165149994`
- job ID: `101874617569`
- workflow/job conclusion: `success`
- artifact name: `issue186-r4-cremma-s1-gate0`
- artifact ID: `10033908343`
- artifact ZIP digest: `sha256:5babd43a557c17b6f6ac5d824b9c1623069dd53b48458a9df112ce10450e91e9`
- raw result JSON SHA-256: `e59b783ea5ea51e95cffc4010d2f9b33c131c9f9d016d671fece791ce7a32cc2`
- raw result repository blob: `5a5d7b6571b2f1182a509a5f85495a718ca8ea9b`
- raw result path: `experiments/issue186-r4-cremma-s1/issue186_cremma_gate0_summary.json`

The repository copy is byte-for-byte identical to the workflow artifact JSON: its Git blob equals the Git blob computed over the downloaded artifact bytes (`5a5d7b6571b2f1182a509a5f85495a718ca8ea9b`).

## Firewall verification

The run emitted the required marker:

`NO ISSUE186 SCIENTIFIC S1 SCORE COMPUTED`

and asserted all of the following before artifact upload:

- `scientific_score_computed == false`;
- ZL3b was hash-verified but not parsed;
- `feature8`, `training_sd`, `item_contrast`, `contrasts`, and `s1_projection` were disabled before the external audit;
- no new S1-derived field was emitted;
- all 21 externally frozen CREMMA manuscripts were included;
- `gate0_valid == true`.

No S1 sign, projection, ratio, Type mean, or R4 scientific classification was computed in Gate0.

## Support result

All 21 frozen source folders parsed without source/path failure. The historical paragraph representation, however, yielded usable S1 support in only five manuscripts.

| Type | listed | parsed | Stage1 structurally composable |
|---|---:|---:|---:|
| Medic. | 5 | 5 | 2 |
| Schol. | 5 | 5 | 2 |
| Lit. | 6 | 6 | 0 |
| Eccl. | 3 | 3 | 1 |
| Gramm. | 2 | 2 | 0 |

Totals:

- listed manuscripts: 21
- parsed manuscripts: 21
- parser/source failures: 0
- parsed paragraph items: 324
- base-eligible items: 120
- S1-eligible items: 96
- structurally composable manuscripts: 5
- represented physical lines: 2,426
- represented non-empty lines: 2,423
- represented tokens: 21,536

The five structurally composable manuscripts are:

- `H318`: 2 S1-eligible items
- `CLM13027`: 20
- `BIS-193`: 40
- `Mazarine915`: 29
- `UBL758`: 5

Every one of these five already has a historical Phase62B/H318 S1 result. The full-registry expansion therefore contributes no genuinely unrevealed manuscript to a later S1 reveal under the unchanged historical representation.

Two literary manuscripts contain parsed paragraph items but still have no base-eligible S1 item: `CCCC-MSS-236` (31 items) and `Latin6395` (47 items). The remaining non-composable manuscripts expose no pilcrow-defined item under the frozen parser. These are composability facts only; no boundary repair is licensed from them.

## Consequence

Gate0 itself is valid. The proposed genre-stratified Stage1 is not prospectively informative on this corpus/representation combination.

- `Lit.` and `Gramm.` are non-composable under the Issue #186 class rule.
- `Eccl.` has only one composable manuscript.
- `Medic.` and `Schol.` each have two, but all four corresponding manuscript S1 outcomes were already revealed before Issue #186.

Therefore this Gate0 does not license a new CREMMA genre-attribution reveal. Treating page starts, headings, files, drop capitals, or other metadata as substitute paragraph boundaries would change the frozen S1 representation after support inspection and is forbidden under the Issue #186 firewall.

The next Priority-1 experiment must use a new externally selected corpus in which true paragraph/message/item boundaries and sufficient within-item line support are preserved before S1 scoring. Issue #186 remains the audit record for why the broader CREMMA registry cannot supply that prospective comparison under the historical parser.
