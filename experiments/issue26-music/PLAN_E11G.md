# Issue26E11G — Latin-order specificity audit

Status: **PREREGISTERED — NO E11G TARGET REVEAL YET**

## Motivation

E11F established that the externally defined 23-family STA stream has a strong within-segment order effect under the frozen medieval-Latin 4-gram substitution objective: real held-out CE was 3.6860993911 bits/char versus a fully refitted within-segment order-null median of 4.4730503524 (p=1/201). At the same time the recovered manuscript-wide substitution key was unstable and lexical readability was poor.

E11G does not extend or rescue the León cipher model. It asks a narrower competing-explanation question:

> Is E11F's normalized fit specifically dependent on genuine medieval-Latin character order, or can character-frequency- and run-length-matched pseudo-Latin 4-gram models obtain an equally close or closer normalized fit after receiving the same complete substitution fitting freedom?

A negative result would reclassify the E11F residual as generic compatibility between Voynich sequential structure and a flexible 4-gram substitution objective, not Latin-specific cipher evidence.

## Frozen target and solver

E11G must reuse without modification:

- official STA1 ZL3b source SHA-256 `8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a`;
- the E11E 23-family representation and numerical-leaf population;
- the same five physical-leaf folds;
- the E11D-validated `FREQ-HILL` 24-letter monoalphabetic solver;
- the same frozen CREMMA-Medieval-LAT commit `292525969ad98380b398e6606a9c2a36d51913ae` and four E11 corpus directories;
- the E11 24-letter normalization (`j→i`, `v→u`).

No STA family may be split, merged, deleted, reordered, or selected after reveal. No homophones, polyalphabetic keys, section-specific keys, family-member distinctions, manual reading, or alternate plaintext alphabets are allowed.

## Replay firewall

Before any null interpretation, the executable must reproduce both published E11 values through the existing code path:

- real Voynich pooled held-out CE: `3.6860993911494533`;
- real medieval-Latin five-fold self baseline: `3.6903904874` bits/char, with tolerance `1e-10` for the rounded published baseline.

If replay fails, classification is `E11G REPLAY FAILURE` and no null result is interpreted.

## Primary statistic

For a language model `L`, define

`G(L) = CE(Voynich | fitted substitution, L) - CE_self(L)`.

`CE(Voynich | fitted substitution, L)` is pooled held-out CE from the same five physical-leaf folds after fitting the frozen FREQ-HILL substitution on the other four folds.

`CE_self(L)` is the same five-fold run-index self baseline used in E11E, computed from the corpus that generated `L`.

For real CREMMA Latin, the frozen reference is approximately:

`G(real Latin) = 3.6860993911 - 3.6903904874 ≈ -0.0042911 bits/char`.

Lower `G` means the Voynich fit is at least as close to that model's own held-out language baseline.

This normalized gap, not raw CE, is primary because order-destroyed language models can have different intrinsic entropy.

## Null family

Generate exactly **200 deterministic pseudo-Latin corpora**.

For each null `n`:

1. concatenate all normalized CREMMA runs in their frozen order;
2. shuffle the complete character vector without replacement using a deterministic E11G seed;
3. repartition the shuffled vector using the exact original run-length vector.

Each null therefore preserves exactly:

- the complete normalized Latin character multiset and all unigram frequencies;
- total character count;
- number of runs;
- the full ordered run-length vector;
- E11 alphabet and normalization.

It deliberately destroys genuine within-run Latin character order, word/line composition, and higher-order n-gram structure.

For every null independently:

1. build a new 4-gram LM from that pseudo-Latin corpus;
2. compute its own five-fold self baseline;
3. fit the full frozen FREQ-HILL substitution separately on each 4/5 Voynich training split;
4. freeze that null-specific fold key;
5. score the untouched corresponding 1/5 Voynich held-out split;
6. compute `G(null)`.

No real-Latin fitted key is reused. No null is selected or discarded by result.

Seed namespace is frozen as:

`Issue26E11G:LatinGlobalShuffle:v1:<null_index>`

## Primary test and classification

Compute the lower-tail Monte-Carlo p-value with +1 correction:

`p = (1 + number of nulls with G(null) <= G(real Latin)) / 201`.

Also compute:

`advantage = median(G(null)) - G(real Latin)`.

Frozen gates for a Latin-order-specific residual are both:

1. `p <= .01`;
2. `advantage >= .10 bits/char`.

Classification:

- if replay fails: **`E11G REPLAY FAILURE`**;
- if both gates pass: **`LATIN-ORDER-SPECIFIC NORMALIZED RESIDUAL`**;
- otherwise: **`NO LATIN-ORDER SPECIFICITY UNDER FREQUENCY/RUN-LENGTH NULLS`**.

The positive class still would not establish plaintext or a León decipherment. E11F key instability and readability failures remain binding.

## Secondary diagnostics — non-gating

Record but do not use for classification:

- raw Voynich held-out CE for real Latin and every pseudo-Latin LM;
- pseudo-Latin self-baseline distribution;
- key stability and complete-key recurrence;
- q05/q50/q95/min/max for raw CE and normalized gap;
- exact character-frequency and run-length preservation checks.

## Interpretation boundaries

If the real Latin model is not exceptional after self-baseline normalization, the E11F order-specific effect should be retained as a Voynich sequential-structure result but not described as Latin-specific cipher evidence.

If the real Latin model is exceptional, the result only establishes specificity to the frozen medieval-Latin 4-gram ordering relative to this matched pseudo-language null family. It does not repair the unstable key, does not make the decoded strings readable, and does not authorize a richer León model.

No merge to `main` is authorized by this experiment.
