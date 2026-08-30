# Phase 62D — exposed-score ranking freeze

Date: 2026-08-30

Status: **frozen before H62-P1 is computed or revealed**.

This decision uses only already-exposed Phase62B/C results plus the already-public Phase51–61C reproducibility audit. It computes no new Voynich statistic.

The purpose of this file is to prevent the prospective H62-P1 result from changing how the prior evidence is ranked.

## Inputs already known at freeze time

### N0 — source-native meaningful structured medieval text

Phase62B across-fold ratios to Voynich:

- S1 entry projection: **-0.980**
- S2 locality excess: **0.133**
- S3 aggregate line-position eta2: **0.989**

N0 fails the frozen joint broad-regime criterion on S1/S2. S1 is negative for every primary manuscript. N0's successful S3 match demonstrates that generic line-position structure is not highly discriminative by itself.

### C0 — bounded reversible boundary-blind recoding

All five training folds independently select C0-4 non-overlapping digraph coding.

Phase62C C0/Voynich ratios:

- S1: **-0.932**
- S2: **0.249**
- S3: **0.856**

C0 materially improves N0 under the frozen rule:

- held-out joint MSE improves in 5/5 folds;
- mean joint relative MSE falls from **3.0388** to **2.8884**;
- 3/4 leave-one-manuscript-out conditions show majority fold improvement.

But C0 remains outside the broad Voynich regime on S1/S2 and retains the wrong S1 sign.

### G/A1 — frozen boundary-aware + local-family generator

A1 is re-scored under the Phase62 common representation without retuning.

Phase62C A1/Voynich ratio-of-means:

- S1: **0.623**
- S2: **1.512**
- S3: **0.587**

All pass the frozen `[0.5,2.0]` exposed common-score gate. Mean five-fold joint relative MSE is approximately **0.470**.

The following qualifications are already known and remain binding:

- the pass is an across-fold ratio-of-means pass, not a universal per-fold pass;
- fold-specific ratios show substantial heterogeneity;
- the independent Phase61C audit shows that aggregate line-position eta2 hides coordinate-level over/under-fit cancellation;
- A1 does **not** reproduce the full multivariate line-position profile;
- A1 pays for an explicit Voynich paragraph-entry mechanism, an explicit local-family process with maximum memory 10, Voynich-selected parameters and an empirical Voynich vocabulary of 8,295 types;
- A1 has no meaningful plaintext candidate or historical construction model.

A stricter training-vocabulary-only audit left the first-gate ratios and selected parameters essentially unchanged, so held-out-only vocabulary leakage is not the explanation for A1's scalar survival. The broader target-dependence cost nevertheless remains real.

## Frozen exposed-score structural ranking

Among the **specific implementations actually tested** on the frozen Phase62 exposed scalar scorecard:

> **A1 > C0 > N0**

Meaning:

1. **A1** is the strongest exposed scalar structural fit.
2. **C0** has genuine explanatory value relative to N0 but remains insufficient on the two most discriminative common targets, S1 and S2.
3. **N0** is not jointly competitive, although it explains why aggregate generic line-position S3 is weak standalone evidence.

This ranking is about **exposed structural fit of the tested candidates**, not historical probability, semantics, or decipherment.

## Frozen overall mechanism-family conclusion

> **UNRESOLVED.**

A1 is the **provisional leading exposed-score structural candidate**, but G is not promoted as the overall mechanism-family winner before prospective validation.

Reasons:

1. A1 has materially greater target dependence and explicit mechanism cost than N0/C0.
2. A1's aggregate S3 pass conceals coordinate-level profile mismatch.
3. A1 has nontrivial fold heterogeneity.
4. A1 provides no independently meaningful plaintext or historical construction evidence.
5. C0 tests only a deliberately bounded first family of reversible global encodings; failure of C0 is not falsification of all cipher/shorthand mechanisms.
6. N0 is a limited structured-medieval plaintext panel, not proof that every meaningful source family must behave identically.
7. No candidate has yet passed the sealed prospective H62-P1 discriminator.

Therefore the correct pre-prospective state is:

- **N**: simple source-native N0 is disfavored on the joint exposed scorecard; broader meaningful-text families remain open.
- **C**: C0 gains limited support as a useful transformation but is insufficient; broader C requires a separately frozen C1 if later justified.
- **G**: A1 currently leads exposed structural fit but remains provisional and costly/ungrounded.
- **M**: deferred; no mixed model is introduced before simpler families receive the prospective challenge.

## Frozen prediction for H62-P1

H62-P1 was specified in Phase62A before the tournament result and remains sealed at the time of this commit.

The prospective test examines near-family recurrence excess over distance bins:

- 1–2;
- 3–5;
- 6–10;
- 11–20;
- 21–40 tokens.

A1 contains an explicit local-family mechanism that can directly select only from the preceding **10 tokens**. It therefore predicts a recurrence-excess profile with comparatively strong short-range concentration in 1–10 relative to 11–40. Chained generation can create indirect longer-range structure, so this is not a prediction of a literal zero after token 10; the preregistered profile distance and short/long concentration, not a hard cutoff, own the decision.

N0 and C0 contain no explicit 10-token local generator window. They may show natural lexical/morphological recurrence, and C0 may alter edit-distance geometry, but neither was designed around a 10-token recurrence mechanism.

### Predeclared interpretation after reveal

- If frozen A1 is substantially closer to the Voynich H62-P1 profile than N0/C0 under the already-frozen metric, A1's leading status is strengthened by genuinely prospective evidence.
- If A1 is not closer, especially if its short-range concentration/decay shape is contradicted, A1's current leading status is materially weakened even though its earlier exposed scalar gates remain historical passes.
- If C0 or N0 is closer, record that directly; do not repair A1 before interpretation.
- If no candidate reproduces the profile, the correct result is an unresolved tournament with all tested simple families incomplete.

## Firewall after this decision

Until H62-P1 is recorded and interpreted:

- no A2;
- no C1;
- no M0;
- no replacement prospective statistic;
- no retrospective change to the ranking above.

The next allowed action is to implement the exact already-frozen H62-P1 computation and then reveal/evaluate it without model retuning.