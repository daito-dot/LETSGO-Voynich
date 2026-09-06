# Issue #90 Phase 0 — authoritative first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE FIRST REVEAL ARCHIVED**
Parent program: Issue #88

## 1. Score-free selection authority

The selected architecture, hyperparameters and three generated populations were frozen before any new-candidate S2/H62/R1 target score existed.

Authoritative Preflight B:

- run: `34016904359`
- head: `152bec1de1db393e46eb712f54320013ff6c301a`
- artifact: `issue90-phase0-preflight-b`
- artifact ID: `9984254233`
- artifact digest: `sha256:a326b27fd5ed4c6caed371970c14ef347770f6a2732b818ca7ffee831b94c4a5`
- `phase0_preflight_b.json` SHA-256: `e016e0da642277adc86b257851eba459e946e40015622d127cb13b85afed33d4`
- selection SHA-256: `8eb8c32709cdf65949e328ad9094f772dc512da52e1241232c44ed72ec856206`
- fold identity SHA-256: `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`
- explicit authority field: `target_score_calls = 0`

All five outer folds selected `DECAY40`, with `tau=32`; `pi=.21,.21,.20,.21,.21`.

Frozen generated-population SHA-256 values:

- rep0: `ee594b3a8b3c3881f0c2aace1c7e5f694d8c6bada8b17ef22e831c2e9b161ee4`
- rep1: `560ca8529279354850420b92fee177b7980436ced6abfe760b79a4b68342fdea`
- rep2: `a8971db75d1cedc79c2bed379d3e5393e1b976abd3d338be356a17369efbb002`

## 2. Scientific first reveal and runner-only repair

The first target-scoring workflow was launched at scientific head:

- run: `34017355970`
- scientific head: `39c4e2efe42e2429d307a2ca755ceda975d38791`

Its Stage 1 S2/H62 reveal completed successfully, as did all three R1 jobs. The aggregate job then failed solely because the aggregate runner had not installed `numpy`; no scientific computation or model-selection path was changed.

The runner-only workflow repair added the missing runtime install. The complete deterministic replay/assembly then ran at:

- run: `34017687319`
- assembly head: `3f7b8cb4b86e805e5332c15aa279db8b4538b6b0`
- workflow conclusion: `success`

The Stage 1 scientific JSON reproduced byte-for-byte across the original reveal and the assembly replay:

- `phase0_stage1.json` SHA-256: `36d2849308f3e7bf5335c037f7fdb4f9b4ef1ffa9c67cf6e4761b7fd7812ec93`

Thus the runtime repair did not change the target result.

## 3. Final artifact authority

Run `34017687319` final artifact:

- artifact: `issue90-phase0-first-reveal`
- artifact ID: `9984482299`
- artifact digest / ZIP SHA-256: `sha256:add18d90595fd0e69f050976628f2213f38810696534f6b73cfa8da9b97243c5`

Contained-file SHA-256 values:

- `phase0_stage1.json`: `36d2849308f3e7bf5335c037f7fdb4f9b4ef1ffa9c67cf6e4761b7fd7812ec93`
- `phase0_final.json`: `028d0feb20ac92c2936611af1daee4fb9446a7473e7b4dfc8afb2d7153f4c22e`
- `r1/selected_rep0.json`: `e3c691c0195ebdb3b82b894a2222b904ee3d1b6d39dc3873dd9aa5ec97017c0c`
- `r1/selected_rep1.json`: `2d88df06291784e2c6a0983d4105e449b1dfb317fa39846a8dad5fa5f58e9c22`
- `r1/selected_rep2.json`: `7b7e2945c2d400c1926ba3e91be959e801f96ad84e3eeaec5764ba51cd0092bb`

The artifact contains the complete scientific result. It is not regenerated from post-report parameters.

## 4. Frozen final classification

`phase0_final.json` records:

> **`PREDICTIVE BUT SURFACE-INCOMPLETE`**

- stable held-out predictive gain: PASS;
- S2 immutable target interval: FAIL low;
- two-sided raw H62 amount: PASS;
- H62 profile conjunction: FAIL on `abs_C_short_diff` despite a strong `D_profile` value;
- R1: PASS in all three fixed realizations.

The result does not license retuning `pi`, `tau`, the history window, S2, or the H62 profile against the revealed target. Under Issue #88, the next program-level step is Phase 1 predictive-information budgeting.