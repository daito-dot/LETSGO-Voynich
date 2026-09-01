# Issue #68 Stage 0 replay / authority verification

Status: **VERIFIED — `JOINT TOURNAMENT AUTHORITY READY`**

No Issue #68 target candidate R1 graph, residual energy, topology score, or joint R1/R2/R3 classification was computed before this record.

## What passed

1. **Common held-out authority**
   - R1 (#58C/#58D), R2 (H62-P1), and R3 (signed S1) resolve to the same five physical-leaf folds covering 99 unique leaves.

2. **Exact external source authority**
   - ZL3b Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
   - CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`
   - Naibbe commit: `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`
   - Naibbe encoder blob: `b566ad82e4b6ff0782ecdddebf77718dac44f292`
   - Naibbe table: `references/naibbe_tables.csv`, blob `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`
   - Naibbe decoder: `decrypt_naibbe.py`, blob `b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b`

3. **Corrected reversibility authority**
   - all five frozen C0 transforms pass exact synthetic structured round-trip under the actual Phase62C representation;
   - `C0-4_digraph` preserves source token hierarchy and requires no boundary side information;
   - the pinned Naibbe repository contains an explicit decoder, but the published encoder destroys original plaintext spacing/punctuation and applies many-to-one orthographic normalization, so exact original-text recovery is not a valid closure claim.

4. **Phase62P / H62 replay**
   - current frozen-source semantic replay is exact;
   - replay diff count: `0`.

5. **Phase62C first-reveal authority repaired**
   - original successful scientific run: `33313019008`, job `99261341362`;
   - original artifact ID: `9732584331`;
   - artifact ZIP SHA-256: `fe555431c6472b26663a23c842a0c37f70963ca524d7c1759cec6e2799fc4594`;
   - exact original raw JSON SHA-256: `1bd44579b7a57d43ea52ddf9d5bf59acb936b3f6fe7b7346010685c50f10bfb2`;
   - exact raw file is permanently archived at `experiments/phase62/first-reveal/phase62c_c0_a1_results_run33313019008.json`.

## Phase62C replay caveat — retained, not hidden

The later repository file `experiments/phase62/phase62c_c0_a1_results.json` is not the exact first-reveal artifact. Its audited raw SHA-256 is:

`0518ffcebf4666c5b6a142054696c0bf092ee86428ef8282aba6537691eccbb4`

The exact first reveal and later committed record differ in **three numeric fields only**, all inside:

`folds[2].C0_leave_one_manuscript_out.Mazarine915`

| field | first reveal | later committed record |
|---|---:|---:|
| `C0.S1` | -0.9238719297180421 | -0.8830522744522888 |
| `C0_joint_relative_mse` | 10.371319531604906 | 9.044530390532254 |
| `N0_joint_relative_mse` | 11.695085537263099 | 10.659921954292841 |

Audit run `33454247454`, job `99690680088`, found:

- numeric differences: `3`
- nonnumeric differences: `0`
- protected primary scientific field mismatches: `[]`

The first reveal and later record agree on all frozen primary means, ratios, selected C0 transform, LOMO improvement counts, C0 material-improvement decision, A1 competitiveness decision, and the complete Phase62C decision block.

Therefore Stage 0 treats this as a **provenance/reproducibility repair with no scientific decision change**. It does not describe the later committed JSON as the exact first reveal.

## Evidence runs

- corrected external authority + Stage0 audit: run `33453563078`, job `99688595255`
- historical replay drift localization: run `33453683575`, job `99688966414`
- Phase62C original-artifact audit: run `33454247454`, job `99690680088`
- Phase62C original-artifact audit artifact: `9780853020`, ZIP SHA-256 `4de7e2bbc4efce90a4130f2e7a1150cba948850f913f3c08edb825739aebde3f`

## Authorization boundary

Stage 0 now authorizes a **separate preregistered target plan**.

It does not itself authorize outcome-dependent candidate repair. The next target plan must freeze candidate roles, R1/R2/R3/R4 responsibilities, information-access ceilings, null calibration, exact pass/fail gates, and the first-reveal event before any new candidate 66-edge graph is inspected.
