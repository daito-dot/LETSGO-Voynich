# Issue26E11F — fully refitted STA-family order-null audit

Status: **COMPLETED — `ORDER-SPECIFIC BUT KEY-UNSTABLE`**

## Question

E11E used the independently validated E11D `FREQ-HILL` solver on the externally defined 23-family STA representation and obtained a surprising held-out character 4-gram CE essentially equal to the matched medieval-Latin self baseline, while the fitted substitution key remained unstable and the decoded output was lexically poor.

E11F asked the direct falsification question:

> Is that low held-out Latin 4-gram CE actually carried by the observed within-segment order of STA families, or can frequency- and segment-length-preserving shuffled sequences obtain the same result when every null receives the complete substitution refit?

## Preregistration and provenance

- parent E11E result: `1442cdcaa819ed2b0e24eea9c66bc51e40800eaa`
- plan-first commit: `eb6b3bb7a850c58b7468a23949c1d3fdd1647dec`
- first executable commit: `95c3ead64083f438b62963dbe043badb680efca7`
- reveal workflow/head: `d7de6b8351b18c975c2b86e358140524f3504897`
- Actions run: `33387076464`
- job: `99472002975`
- artifact: `9756168030`
- raw JSON SHA-256: `f625827a40bc143f26c3e0a239e605420083695d1fb6d77d7a184b9333294c01`
- artifact ZIP SHA-256: `5d78e22612ca77d5abd0402137bd9bd2ebbfc106f55f84f3feec183b3662904c`.

The workflow verified the exact official STA1 source and frozen CREMMA commit before execution.

## Replay firewall

PASS exactly.

E11F reran the real E11E population through the same code path before generating any null interpretation and reproduced:

- pooled held-out CE: `3.6860993911494533` — absolute replay difference `0.0`;
- mean pairwise occurrence-weighted key stability: `0.6219935480654878` — absolute replay difference `0.0`;
- exact complete-key recurrence: `1/5` — exact match.

## Null family

Exactly 200 deterministic nulls were generated.

For every scoring segment independently, E11F shuffled the 23 STA-family indices without replacement while preserving exactly:

- the segment's family multiset;
- segment length;
- leaf/fold assignment;
- page, locus, source line, and segment identity;
- token count and original token-length vector.

No symbol moved between segments or folds.

Crucially, every null received the complete E11E fitting freedom from scratch:

1. recompute the training frequency seed;
2. run the frozen E11D-validated `FREQ-HILL` substitution optimizer separately on each 4/5 training split;
3. freeze that null-specific key;
4. score the shuffled untouched 1/5 held-out split;
5. compute cross-fold key stability.

No real E11E fitted key was reused for a null.

## Primary CE result

Real E11E pooled held-out CE:

> **`3.6860993911 bits/char`**

Refitted order-null distribution:

- median: **`4.4730503524`**
- q05: **`4.4611442814`**
- minimum: **`4.4537076614`**
- nulls with CE <= real: **0 / 200**
- lower-tail p-value: **`1/201 = 0.0049751244`**
- real advantage below null median: **`0.7869509613 bits/char`**.

Both preregistered CE gates pass strongly:

- p <= .01: **PASS**;
- real at least .10 bits/char below null median: **PASS**.

This is not a small effect created by one lucky shuffled comparator. The best of all 200 fully refitted order-null sequences remained about `0.768 bits/char` worse than the real ordering.

## Key-stability result

The key evidence points in the opposite direction.

Real E11E mean pairwise occurrence-weighted key stability:

> **`0.6219935481`**

Refitted order-null stability:

- median: **`0.8309910057`**
- q95: **`0.9569094806`**
- maximum: **`0.9961324000`**
- nulls with stability >= real: **200 / 200**
- upper-tail p-value: **`1.0`**.

Exact complete-key recurrence among the 200 nulls:

- recurrence 1/5: **196 nulls**
- recurrence 2/5: **4 nulls**.

Thus the real sequence's unusually low Latin CE does **not** come with an unusually stable manuscript-wide monoalphabetic key. In fact its weighted key stability is lower than every tested order null.

## Frozen classification

> **`ORDER-SPECIFIC BUT KEY-UNSTABLE`**

The frozen `ORDER-SPECIFIC LATIN-LIKENESS RESIDUAL` class cannot be used because the stability gate fails. E11E's independent absolute diversity/readability gate also remains failed: pooled top-five decoded-character mass was `.7746` versus the matched Latin `.4932`, and only one distinct whole-token CREMMA match of length >=6 was observed.

## What this establishes

E11F materially changes the interpretation of E11E.

The E11E character-level Latin-like score is **not explained by family frequencies, segment lengths, and unrestricted refitting alone**. Destroying only within-segment order produces a large and highly consistent degradation despite giving every null the same solver freedom.

Therefore the 23-family STA stream contains real local sequential structure that is unusually compatible with the frozen medieval-Latin 4-gram objective under this model.

That is a genuine order-specific residual worth retaining.

## What this does not establish

It does **not** establish a León cipher or a decipherment.

The strongest problem is now clearer rather than weaker:

- if a single manuscript-wide León-style monoalphabetic substitution were the right mechanism, the recovered key should become stable across physical-leaf folds;
- instead the real data require substantially different fitted keys, with weighted agreement only `.622`;
- lexical readability remains essentially absent and output character concentration remains much higher than real Latin.

The observed pattern is therefore better stated as:

> **real Voynich STA-family order has strong Latin-4-gram-compatible sequential structure, but that structure is not captured by one stable León-style monoalphabetic substitution key.**

Possible nonexclusive explanations include manuscript-internal positional/grammatical structure, heterogeneous regimes across sections, or a representation that groups visually related symbols while losing distinctions relevant to any substitution. These are hypotheses for later branches, not conclusions from E11F.

## León stopping boundary

For the current music-cipher exploration, stop the León line here.

Do **not** use this mixed result to post-hoc introduce homophones, polyalphabetic keys, family-member splitting, section-specific keys, or manual semantic reading. Those would create a new model family and require their own independent justification and preregistration.

The León exploration has now answered the intended practical question at the frozen 23-family manuscript-wide monoalphabetic level:

- validated solver: yes;
- character-order signal: surprisingly strong;
- stable decipherment key: no;
- readable plaintext: no.

Preserve the order-specific residual for later non-music / broader language-structure work, and move the active Issue26 music-cipher exploration to a genuinely different historically sourced mechanism.

No merge to `main` is authorized.
