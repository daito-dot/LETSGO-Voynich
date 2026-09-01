# Issue #72 V2 — Stage D1 PT target-scoring implementation contract

Status: **FROZEN BEFORE ANY PT R1 TARGET SCORE**

This document operationalizes the already-preregistered `STAGE_D_PT_TOTAL_EFFECT_PLAN.md`. It does not change the scientific question, intervention, population, estimand, or interpretation policy.

## Frozen upstream authorities

- Stage D plan commit: `c45c67a665a7e4ad24c1d2706f83c65931d950a9`.
- Complete target-blind D0 permanent commit: `7056e7ed037af7ff53927d04355821606b59ba6e`.
- D0 aggregate raw SHA-256: `17caf1a6c710b367649499a1fbe71be9e969bc295bc868330372620609e7e50e`.
- Restored original B0 raw SHA-256: `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`.
- B2 calibration archive Git blob: `90914e967c4e870443db372c419d8a645cbad756` (raw artifact SHA-256 already frozen in B2 provenance: `2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147`).
- B1 R1 measurement implementation Git blob: `2115e8dec15fca21514c8f57e9f51523d10a77c3`.
- Issue68 target loader/scoring authority Git blob: `e94a24fbdfbb922099407313f23a1b87859130b6`.
- D0 PT implementation Git blob: `56e404b524064bb62e64fd32a6601dd1b77ca347`.

## Exact D1 population

D1 scores every frozen D0 case:

- `j = 0..30`;
- `rep = 0..4`;
- total `155` PT outputs;
- no exclusions, rerolls, support gates, or post-reveal case replacement.

## Surface reconstruction gate

D1 does not accept an arbitrary newly generated PT surface.

For every `(j, rep)` it must:

1. load the corresponding permanent `stage-d0-pt/individual/PT_j{j}_rep{rep}.json`;
2. rerun the exact D0 PT implementation from the same pinned CREMMA/Naibbe authorities;
3. require exact pooled and per-manuscript primary/raw surface SHA identities to the D0 record;
4. require exact visible/accepted support counts and ambiguity-retry counts to the D0 record;
5. only after those T1 identity gates pass may R1 target scoring begin.

A reconstruction mismatch is an implementation/authority failure, not a scientific PT outcome.

## R1 measurement identity

D1 uses the same measurement construct as B1/B2:

- `SlotParser(min)`;
- 66 unordered slot pairs in the frozen pair order;
- K_other-conditional Jeffreys-smoothed Mantel-Haenszel Yule-Q;
- candidate-owned line-local reference null;
- empirical mid-rank normal residual Z;
- residual energy E;
- 4-fold reliability W;
- topology Pearson and sign agreement against ZL3b and IT2a separately.

The implementation reuses the frozen B1 measurement functions rather than introducing a second R1 formula.

For each `(j,rep)`, reference namespace is exactly:

`issue72v2:stageD:PT:j{j}:rep{rep}:reference`

with `N_ref=1000`.

## Frozen target authority

Targets are loaded through the already-audited Issue68 loader.

It requires:

- #58C raw SHA-256 `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`;
- #58D raw SHA-256 `f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6`;
- pooled target cross-reading Pearson `0.9884483852763541`;
- pooled target sign agreement `65/66`.

No target reading is averaged into the other.

## Exact paired baseline authority

D1 does **not** regenerate or rescore unchanged Naibbe as a new baseline.

For each `rep`, it loads `positive_control_summary.per_rep` from the frozen B2 calibration archive and uses the exact stored values:

- `R_ZL3b`;
- `R_IT2a`;
- plus stored E/W/coverage/sign values for descriptive pairing checks.

Thus the paired total-effect contrast is anchored to the already-frozen positive-control result rather than creating a duplicate baseline definition.

## Per-case output

For each `(j,rep)` and target reading `t`, output:

- exact PT R1 correlation `R_PT[j,rep,t]`;
- exact B2 baseline `R_baseline[rep,t]`;
- `delta_R[j,rep,t] = R_PT - R_baseline`;
- PT E, W, sign agreement, coverage;
- exact D0 surface/support authority identifiers;
- target authority identifiers;
- reference-null namespace;
- no binary scientific classification.

## Aggregate law

Only a complete 155-case population may aggregate.

For each `j` and target `t`:

`D[j,t] = mean_rep(delta_R[j,rep,t])` over exactly rep0..rep4.

The aggregate must retain all five block deltas alongside the mean.

For each target separately:

`p_nonloss[t] = (1 + count_j(D[j,t] >= 0)) / 32`.

Also report:

`p_both = max(p_nonloss[ZL3b], p_nonloss[IT2a])`.

These are finite randomization rank/evidence quantities, not hard universal significance gates.

Report distribution summaries of D and continuous ratios to frozen B2 scales:

- ZL3b SD `0.010907479701133605`, MAD `0.00897810342736527`;
- IT2a SD `0.008561663953448985`, MAD `0.005799322835226439`.

No SD/MAD multiple becomes a PASS/FAIL threshold.

## Coverage policy

Coverage remains descriptive. D0 already established the full PT population has coverage `0.8818521546759367..0.8913690874078876`, median `0.8867743449988091`.

D1 applies no coverage eligibility gate and does not delete any low/high-coverage case.

## Forbidden after reveal

After any PT R1 score exists, do not change:

- the 31 assignments;
- the five blocks;
- the PT shuffle law;
- the D0 surface identities;
- the target loader;
- the R1 formula/null namespace;
- the paired B2 baseline source;
- the block averaging law;
- the nonloss definition;
- target handling;
- coverage treatment.

Any implementation incident before target access must be documented separately and may repair only transport/code defects without changing these scientific commitments.
