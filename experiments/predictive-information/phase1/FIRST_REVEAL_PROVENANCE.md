# Issue #92 / Issue #88 Phase 1 — authoritative predictive-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE FIRST REVEAL ARCHIVED**

Phase 1 was prediction-only. The executable contained no S1/S2/H62/R1 target-scoring path, and the workflow enforced that boundary before the scientific run.

## Authority

- GitHub Actions run: `34018276930`
- scientific head: `1f9557bfe80800b486dfc8a6901b8888a153d6f3`
- workflow conclusion: `success`
- artifact: `issue92-phase1-predictive-budget`
- artifact ID: `9984665954`
- artifact ZIP digest: `sha256:0c428a42917f5e622c0b5cf736c31b3cfcc403a927f318c6e8291e03566e538d`
- `phase1_results.json` SHA-256: `dba64d047b8843974e620c5a4e20f8729b5e37602248718f1e2a77aca91baafe`

The result JSON is the complete scientific authority.

## Firewall recorded by the result

- `S1_scored = false`
- `S2_scored = false`
- `H62_scored = false`
- `R1_scored = false`
- `issue84_target_used = false`
- `semantic_or_image_context_used = false`

The B0/B1 regression gate reproduced the frozen Phase-0 V2 and DECAY40 held-out results exactly before the richer ladder was interpreted.

## Frozen classification

> **`MATERIAL PREDICTIVE INFORMATION REMAINS`**

The classification is licensed independently by both preregistered richer V2-based increments:

- longer-history recency `Delta_long`: `+0.0469270813 bit/token`, positive `5/5` outer folds;
- observable line/paragraph state `Delta_state`: `+0.0289294918 bit/token`, positive `5/5` outer folds.

The matched flexible byte model also independently confirms that context crossing visible-space boundaries is predictive:

- `Delta_flex = RESET - CONTINUOUS = +0.1296450893 bit/token`, positive `5/5` folds.

However the preregistered cross-model comparison against the simple local DECAY40 gain does **not** pass:

- `Delta_flex_over_local = +0.0169201078 bit/token` mean;
- positive only `3/5` folds;
- frozen classification: FAIL.

Thus the Phase-1 material-residual conclusion is driven by B2/B3, not by claiming that the flexible byte model exceeds DECAY40.

## Boundary outcomes retained without repair

All five B2 outer-fold selectors choose:

- history `H = ALL` preceding surface tokens on the current physical leaf;
- `tau = 128`;
- `pi = 0.30`.

`H=ALL` and `pi=.30` are frozen grid boundaries. The plan explicitly forbids extending either grid after reveal. They show that the tested longer-history family still wants broader/stronger history than Phase 0, but they do not identify a historical memory horizon or an optimum mixture strength.

The exact B2 winner is nevertheless not a near-tie artifact. Relative to `ALL/tau128/pi=.30`, the nearest `ALL/tau128/pi=.29` alternative is worse by about `8.96–14.38` nested-validation nats, and `H=320/tau128/pi=.30` is worse by about `13.99–21.48` nats across the five outer selectors.

All B3 selectors choose `lambda=.50`; the state-family choice is not uniform:

- `ENTRY_BODY`: folds 0 and 3;
- `LINE4`: folds 1, 2 and 4.

Therefore the evidence supports predictive value in observable paragraph/line state, but does not yet identify one uniquely preferred positional representation.

## Program consequence

Phase 1 does not license a rich latent-state search. Under Issue #88 it licenses Phase 2 source attribution: determine whether the additional predictability is due to genuine sequence ordering/recency, prefix-local vocabulary or token-family inventory, observable document state, or another externally observable source before introducing hidden state.