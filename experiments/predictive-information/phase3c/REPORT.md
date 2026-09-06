# Issue #109 Phase 3C — matched-Herbal Currier transport report

Date: 2026-09-06
Status: **COMPLETE — AUTHORITATIVE FIRST REVEAL RECORDED**
Parent: Issue #88

## Question

Does the Currier A/B `PREV_PARAS` scalar-strength asymmetry found in the all-domain Phase 3A transport test persist when prediction is prospectively restricted to the common Herbal illustration/domain using whole-leaf selection?

## Frozen population and authority

The merged score-free Gate 0 retained only whole numeric physical leaves that are pure Currier A or B and pure Herbal (`I=H`) for the selected prediction population. No within-leaf token filtering was allowed.

- A_HERBAL: 46 leaves / 177 items / 7,387 visible tokens / 5,462 parser-accepted tokens.
- B_HERBAL: 15 leaves / 63 items / 3,153 visible tokens / 2,382 parser-accepted tokens.
- All ten Currier x fold cells remained nonzero under the original five physical-leaf folds.
- Gate-0 result JSON SHA-256: `ec8c1dcb14f4450fe6e9f42d80ad00a60872719553c5ee46c153287723f705d8`.

The predictive scorer recomputed this Gate and refused to run unless the frozen hash and corrected source-order assertions matched.

## Frozen model family

The Phase-3A mechanism-only transport family was reused without architecture search:

1. target-side V2 emission/support;
2. `LOCAL40` edit-distance-1 recency with fixed `H=40`, `tau=32`, scalar `pi`;
3. order-free `PREV_PARAS` inventory on top of `LOCAL40`, scalar `alpha`;
4. `pi, alpha` grids `0.00..0.30` by `.01`, exact ties to the smaller value;
5. source-only five-fold held-out parameter selection;
6. target-only nested oracle for diagnostics.

No H/tau/window, edit relation, paragraph pool, fold, domain, hand, surface-statistic target, imagery, semantic state, plaintext or latent-state search was used.

## Authoritative first reveal

- workflow run: `34022384737`
- scientific head: `b02b1c9f818f1810275aa18de28fd2c9a8e0e6be`
- artifact ID: `9985940850`
- artifact digest: `sha256:72f411141d91d9528bdb613177f41106fef95bfc6792bdbebca3505f8a2683ad`
- result JSON SHA-256: `13579242a30e9001a8913db6c4328a952118268b4fb5ad7a1f919f88c0ecd234`

A post-provenance rerun at head `6616fd84b2a2babf78225eb904c8d5f874f2c71f` also completed successfully (run `34022493059`, artifact `9985980959`). Its result JSON is byte-for-byte identical to the first reveal and has the same SHA-256.

## Frozen source parameters

Selected only from the corresponding source-Herbal stratum:

| Source | `pi_LOCAL` | `alpha_ALL_PREV` |
|---|---:|---:|
| A_HERBAL | 0.10 | 0.04 |
| B_HERBAL | 0.11 | 0.08 |

For comparison only, the all-domain Phase-3A values were A `.14/.09` and B `.16/.19`. Domain restriction lowers both absolute strengths, while the approximately twofold PREV-alpha ratio remains.

## Primary transport results

Directional pass is the frozen rule: mean gain > 0 and positive in at least 4/5 target folds.

### A_HERBAL -> B_HERBAL

- `G_local_transfer = +0.0342552 bit/token`, positive 4/5 — **PASS**.
- `G_prev_transfer = +0.00489741 bit/token`, positive 4/5 — **PASS**.
- `G_core_transfer = +0.0391526 bit/token`, positive 4/5 — **PASS**.
- local oracle penalty mean `-0.00611808 bit/token`.
- core oracle penalty mean `-0.00626700 bit/token`.

Fold 0 is negative for all three transfer gains; folds 1–4 are positive. The frozen 4/5 rule therefore passes the direction without dropping or regrouping the small B fold 0.

### B_HERBAL -> A_HERBAL

- `G_local_transfer = +0.0332095 bit/token`, positive 5/5 — **PASS**.
- `G_prev_transfer = +0.000678861 bit/token`, positive 2/5 — **FAIL**.
- `G_core_transfer = +0.0338884 bit/token`, positive 5/5 — **PASS**.
- local oracle penalty mean `-0.00008734 bit/token`.
- core oracle penalty mean `+0.00149170 bit/token`, positive 4/5.

The failed component is specifically the transferred PREV scalar strength. The local mechanism and full core remain transportable.

## Formal classification

- `LOCAL40`: **BIDIRECTIONAL TRANSPORT**
- `PREV_PARAS`: **A->B ONLY**
- `CORE`: **BIDIRECTIONAL TRANSPORT**

Under the interpretation rule frozen before reveal:

> **CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL**

Therefore broad illustration/domain composition as represented by `$I` is not a sufficient explanation for the all-domain Currier PREV-strength asymmetry under this matched Herbal test.

## Target-oracle PREV diagnostic

The target-only nested oracle gives:

- A_HERBAL PREV increment: mean `+0.00225790 bit/token`, positive 3/5 — frozen reproducibility rule **FAIL**.
- B_HERBAL PREV increment: mean `+0.00474849 bit/token`, positive 4/5 — **PASS**.

This matters for interpretation. The matched-Herbal slow paragraph-scale effect is weaker overall than in the all-domain population, and within the smaller A-Herbal population it is not itself stable under the frozen 4/5 rule. The result therefore supports persistent strength heterogeneity, but not a claim that a sharply estimated A-specific long-memory effect has been established in the restricted subset.

## Secondary strict source-support diagnostic

The source-trained V2/vocabulary/edit-index arm is finite in every fold in both directions, so support is formally `VALID`, but exact-token support mismatch is large.

Weighted over target tokens:

- A_HERBAL -> B_HERBAL: exact-token OOV `818/2382 = 34.34%`; source-support core penalty relative to mechanism-only target support `+2.86954 bits/token`.
- B_HERBAL -> A_HERBAL: exact-token OOV `1875/5462 = 34.33%`; source-support core penalty `+2.18292 bits/token`.

This confirms the same distinction seen in Phase 3A: literal vocabulary/emission support differs strongly even where the short local mechanism transports cleanly. This diagnostic does not override the mechanism-only classification.

## Scientific interpretation

The strongest supported synthesis after Phase 3C is:

1. the short edit-1 recency mechanism remains highly portable across Currier A/B, including inside the common Herbal domain;
2. a slower previous-paragraph inventory architecture remains compatible with both regimes, but its useful scalar strength is lower in A than B and does not transfer symmetrically;
3. matching the broad Herbal domain reduces the absolute slow-memory strengths but does not remove the approximately twofold A/B difference;
4. broad `$I` illustration/domain composition is therefore insufficient by itself to explain the Currier dependence;
5. writing-hand causality is still unresolved because the Phase-3B support audit showed hand and Currier are inadequately crossed.

The result does **not** identify semantics, plaintext, a cipher family, a historical production algorithm, or a latent state. It also does not establish that visible spaces are natural-language word boundaries.

## Program consequence

Issue #109 prospectively specified that persistence of the Currier PREV asymmetry within pure Herbal should move the program either to a stronger support-preserving observational design or to the Phase-4 boundary/segmentation validity challenge before latent-state work.

Because the available hand metadata remains confounded with Currier and no new clean multilevel observable factor has been established, the next high-value threat to validity is Phase 4:

> **Do visible spaces mark a reproducible statistical reset or discontinuity relative to within-token construction?**

That question should be frozen prospectively before any alternative segmentation is scored.
