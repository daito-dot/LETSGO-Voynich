# Issue26E11D — DEV2 synthetic solver diagnosis

Status: **COMPLETED — FAILURE MODE IDENTIFIED — VALIDATION NOT OPENED — NO VOYNICH INFERENCE**

DEV2 was frozen in `PLAN_E11D_DEV2.md` before executable creation. A pre-execution implementation amendment, `PLAN_E11D_DEV2_AMENDMENT.md`, corrected only the mechanics needed to compare genuinely distinct annealing temperatures. The first workflow attempt stopped before calculation because SciPy, imported by a shared module, was not installed; the dependency was added without changing any population, key, metric, or search rule.

## Information firewall

The successful job asserted that no ZL3b/STA/cipher-benchmark target input was present. The only scientific corpus was frozen CREMMA medieval Latin at `292525969ad98380b398e6606a9c2a36d51913ae`.

No Voynich plaintext, score, mapping or folio data was used.

## Provenance

Successful run:

- workflow/head: `3ac2e1488132bfdfd5ceefe983e1fec713212505`
- Actions run: `33384671330`
- job: `99464494492`
- artifact: `9755106984`
- raw JSON SHA-256: `db40f111d91d407b7d77cb9b6ab3006cefe00f5217740a3061b63c86974e0645`
- artifact ZIP SHA-256: `322b42fec48ab98b4f679671f55cf20aa98d7d96a0085d46927369521dd6b0fe`.

The preceding dependency-only failed attempt was Actions run `33384359922`; it produced no diagnostic JSON.

## Population

- known synthetic plaintext characters: **70,000**
- retained runs: **1,985**
- observed cipher symbols: **23**
- plaintext alphabet: **24** normalized Latin letters
- unused plaintext letter in this development case: `w`.

## Result

### Independent score implementation agrees exactly

Known true key:

- direct explicit-24 score: `2.839667215212694 bits/char`
- shared `full_score`: `2.839667215212694`
- absolute difference: **0**.

The same exact agreement held at every reported diagnostic stage.

### Incremental swap delta is correct

Across 200 deterministic candidate swaps from the frequency seed:

- maximum absolute discrepancy between incremental `swap_delta` and direct full rescoring: `1.971756091734278e-13`
- mean discrepancy: `4.931831202106829e-14`.

This is far below the preregistered `1e-10` implementation-failure threshold. Therefore the incremental objective is not the cause of E11C/DEV1 failure.

### Frequency seed is already the true key

Frequency-ranked initialization recovered the known development key exactly:

- CE `2.839667215212694`
- exact key accuracy `1.0`
- occurrence-weighted accuracy `1.0`.

Direct full-score steepest descent accepted **0 swaps**, correctly leaving the exact key unchanged.

### Temperature comparison identifies the failure mode

All runs start from that same exact frequency seed and use the same 100,000-proposal algorithm.

| T0 | final CE | exact key accuracy | weighted accuracy |
|---:|---:|---:|---:|
| `.50` | `4.5923921673` | `.04348` | `.03436` |
| `.020` | `2.8396672152` | `1.0` | `1.0` |
| `.005` | `2.8396672152` | `1.0` | `1.0` |
| `.001` | `2.8396672152` | `1.0` | `1.0` |

## Interpretation

> **The E11C/DEV1 synthetic failure is not evidence that the language objective is unusable and is not an incremental-scoring bug. The dominant identified failure is an excessively hot annealing start (`T0=.50`) that destroys an already excellent frequency initialization and settles in a very poor basin.**

This explains the suspicious DEV1 plateau near `4.593 bits/char`: DEV2 reproduces essentially the same bad basin at `T0=.50`, while low-temperature trajectories preserve the exact key.

This does **not** yet validate the León solver. DEV2 is one known development construction whose cipher frequencies happen to identify the key perfectly. The solver must demonstrate robustness on multiple non-identical development populations before an exact solver generation is frozen and the already-preregistered 12-cipher validation battery is opened.

## Next step

Run a final Voynich-blind robustness development battery with:

- multiple plaintext windows/rotations not equal to the locked validation construction;
- independent development keys;
- frequency initialization plus conservative low-temperature search;
- direct-score consistency checks.

If this is robust, freeze the exact solver as `E11D_SOLVER_FREEZE` **before** generating or opening any locked validation output. Only a passing locked validation may authorize a later separately preregistered E11E Voynich reveal.
