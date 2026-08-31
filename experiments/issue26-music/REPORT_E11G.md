# Issue26E11G — Latin-order specificity audit

Status: **COMPLETED — `NO LATIN-ORDER SPECIFICITY UNDER FREQUENCY/RUN-LENGTH NULLS`**

## Question

E11F established a strong within-segment order effect for the externally defined 23-family STA stream under the frozen medieval-Latin 4-gram substitution objective. Real Voynich order scored much better than fully refitted within-segment order-shuffled Voynich nulls (`p=1/201`), but the recovered substitution key remained unstable and lexical readability was poor.

E11G asked the next explanatory question without extending the León cipher model:

> Is that residual specifically dependent on genuine medieval-Latin higher-order character order, or can frequency- and run-length-matched pseudo-Latin language models fit the Voynich stream equally well or better after the same complete substitution refit?

## Preregistration and provenance

- E11F report parent: `46a42103fe1fd47a08debe104287e373255ac3f7`
- plan-first commit: `641d2735f1c0e01fd6c6adb40485b4da0674f632`
- executable commit: `46e0913f8f1e4f8d8d35ada9104bf8abe85ba136`
- workflow/reveal head: `bcac1ec64fd08a45cd75c85886a958aa98f27654`
- Actions run: `33390924987`
- job: `99484109533`
- artifact: `9757540106`
- raw JSON SHA-256: `7dd7146d59cb6c23648cc837b300e523abf42782007096e45286a6e60357f784`
- artifact ZIP SHA-256: `ef7543c2f5f38c9c76f31aa84096c0227d30fcbfc3401e6a9709e6332adf0c71`.

The workflow verified the exact official STA1 source and frozen CREMMA commit before execution.

## Replay firewall

PASS.

The existing E11 code path reproduced:

- Voynich pooled held-out CE: `3.6860993911494533` — absolute difference `0.0`;
- medieval-Latin self baseline: `3.690390487446225` — difference from the published rounded value `4.62e-11`;
- solver score discrepancy: `0.0`.

The vectorized LM implementation used for the 200 nulls was also checked against the frozen reference implementation on real Latin:

- full 4-gram cost array maximum absolute difference: `0.0`;
- self-baseline difference: `2.75e-14`.

## Null family

Exactly 200 deterministic pseudo-Latin corpora were generated.

For each null, all 77,105 normalized CREMMA characters were globally shuffled without replacement and repartitioned using the exact original 2,147-run length vector. Thus every null preserved exactly:

- the complete 24-letter character multiset and unigram frequencies;
- total character count;
- run count;
- the ordered run-length vector.

Genuine Latin within-run order and higher-order n-gram structure were destroyed.

Every null independently received:

1. its own 4-gram LM;
2. its own five-fold self baseline;
3. the complete frozen FREQ-HILL substitution fit on each 4/5 Voynich training split;
4. untouched corresponding 1/5 Voynich held-out scoring.

No real-Latin fitted key was reused.

## Primary normalized statistic

The preregistered statistic was

`G(L) = CE(Voynich | fitted substitution, L) - CE_self(L)`.

For genuine medieval Latin:

- Voynich held CE: `3.6860993911`;
- Latin self CE: `3.6903904874`;
- normalized gap: **`-0.0042910963 bits/char`**.

For the 200 frequency/run-length-matched pseudo-Latin nulls:

- median normalized gap: **`-1.2095158601`**;
- q05: `-1.2389857867`;
- q95: `-1.1729541636`;
- minimum: `-1.2604728238`;
- maximum: `-1.1403988882`;
- nulls with gap <= real Latin: **200 / 200**;
- preregistered lower-tail p-value: **`1.0`**.

The real-Latin model therefore fails both preregistered specificity gates:

- `p <= .01`: **FAIL**;
- real at least `.10 bits/char` better than the null median: **FAIL**.

The direction is not merely a near miss. Every tested pseudo-Latin model produced a substantially more negative normalized gap than genuine Latin.

## Raw CE diagnostic

The same conclusion is visible even before self-baseline normalization.

Pseudo-Latin Voynich held-out CE:

- median: **`3.5209046105`**;
- q05: `3.4909211449`;
- q95: `3.5495932849`;
- minimum: `3.4725531015`;
- maximum: `3.5829106793`.

Genuine Latin Voynich held CE was `3.6860993911`.

Therefore **200/200 pseudo-Latin null LMs fit the held-out Voynich stream better in raw CE than the genuine Latin LM**, despite having their genuine Latin order destroyed.

This is especially damaging to the earlier phrase “Latin-like CE”: the low target CE is not being supplied by specifically Latin higher-order sequence structure.

## Why the normalized gaps are so negative

The pseudo-Latin self baselines are much worse because the null corpora deliberately destroy within-run order:

- null self-CE median: **`4.7306762993`**;
- q05: `4.7182168212`;
- q95: `4.7414163352`.

Yet the optimizer can map the structured 23-family Voynich stream onto those pseudo-language 4-gram models at about `3.52 bits/char` median. The result therefore exposes a model/objective compatibility effect: a structured target plus a freely refitted monoalphabetic mapping can score substantially better than the pseudo-language's own held-out shuffled samples.

That fact is not evidence for pseudo-Latin plaintext. It is evidence that absolute or self-baseline-relative 4-gram CE under this fitting family is not identifying Latin semantics.

## Key stability diagnostic

Real E11 key stability remained:

- weighted pairwise agreement: `.6219935481`;
- exact full-key recurrence: `1/5`.

Pseudo-Latin nulls had:

- median weighted stability: `.7514068208`;
- 166/200 nulls with stability >= the real-Latin fit;
- recurrence distribution: 1/5 = 165 nulls, 2/5 = 32, 3/5 = 2, 4/5 = 1.

Thus key instability also does not become more favorable for genuine Latin.

## Frozen classification

> **`NO LATIN-ORDER SPECIFICITY UNDER FREQUENCY/RUN-LENGTH NULLS`**

## What this changes about E11E/E11F

E11F's within-Voynich order effect remains real: destroying STA-family order while preserving family frequencies and segment lengths makes the fitted score much worse.

What E11G removes is the stronger interpretation that this residual is unusually compatible with specifically medieval-Latin higher-order order.

The combined result is now better stated as:

> **The 23-family STA stream contains strong local sequential structure that a refitted monoalphabetic 4-gram objective can exploit, but genuine medieval-Latin order is not what makes the fit exceptional. Frequency/run-length-matched pseudo-language models fit even better.**

Accordingly, E11 should no longer be carried forward as positive evidence for a León/Latin decipherment mechanism. The useful residual belongs to broader Voynich sequence-structure/model-identifiability work.

## León stopping boundary

The existing E11F stopping boundary is strengthened.

Do not rescue León by introducing homophones, polyalphabetic keys, family-member splitting, section-specific keys, nulls, or manual semantic readings. Those are new model families and E11G gives no reason to prefer them.

For Issue #26 music-cipher exploration, León is closed as a tested mechanism. Preserve only the non-musical order-structure residual for later work.

No merge to `main` is authorized.
