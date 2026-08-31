# Phase 69 literature context — long-range structure versus local generation

Date: 2026-08-31

## Why this question matters externally

Long-range organization is one of the recurring arguments in the Voynich literature for treating the manuscript as information-bearing rather than as simple random pseudo-text. But the literature contains two claims that have rarely been tested against one another with the same frozen mechanism:

1. **Long-range organization exists.** Montemurro & Zanette (2013) reported scale-dependent information and non-uniform word distributions/co-occurrence networks in the Voynich manuscript, arguing that the organization resembles information-bearing text. Amancio et al. (2013) likewise found intermittency/network statistics that separate the manuscript from shuffled controls. Earlier work by Schinner and Landini also reported non-random long-range behavior.
2. **Strong local generative structure can reproduce many Voynich statistics.** Timm & Schinner (2020) proposed a self-citation process in which nearby similar tokens are reused/modified. This is conceptually close to the local-family component independently recovered in this repository's A1 line, although the implementations and claims are not identical.

A contemporary cipher proposal illustrates the unresolved issue from the other direction: the Naibbe cipher can reproduce multiple Voynich-like local/surface properties but explicitly fails to reproduce the manuscript's long-range correlations in its current form (Cryptologia, 2025/2026 publication cycle).

The missing comparison is therefore not simply:

> "Does Voynich have long-range correlations?"

It is:

> "Does the observed long-range organization contain information that a prospectively frozen local-family generator cannot reproduce?"

That is the role of Phase69A.

## What Phase69A adds methodologically

The older long-range literature often compares Voynich against shuffled text or against generic natural-language/random controls. That establishes non-random order, but does not identify the mechanism producing it.

Phase69A uses a harder null/model comparison:

- preserve the real physical-leaf layout;
- use an already-frozen A1 generator fitted only to independent structural targets;
- give A1 only direct ten-token local family memory plus paragraph-entry behavior;
- evaluate previously unopened distances 41–320 tokens on the same physical leaf;
- remove token-inventory effects by within-leaf shuffling;
- compare the residual long-range excess against 50 held-out A1 predictive realizations.

This separates two possibilities that ordinary shuffling does not:

### If A1 matches the >40-token excess

Long-range recurrence by itself is no longer strong evidence for a separate semantic/topic channel. A bounded local mechanism can generate apparent longer-range persistence indirectly through chains of local family reuse plus the manuscript's empirical vocabulary/entry structure.

This would not prove meaningless generation. It would show that one class of "long-range = message" argument is mechanistically underidentified.

### If A1 underpredicts the >40-token excess

A1 is missing a persistent state operating beyond its direct memory. Candidate explanations would include:

- semantic/topic persistence;
- recipe/component state;
- cipher-key or encoding-state persistence;
- scribal/orthographic state;
- another nonsemantic formal process.

The next experiment would then need to decompose whether the excess crosses paragraph boundaries and whether an explicit persistent-state A2 model can reproduce it.

## Relation to prior project results

Phase69 is intentionally a move away from repeated local botanical-feature testing.

The project has already established that:

- pharmaceutical short labels have strong role/register structure;
- simple visual leaf/root morphology does not predict attached short-label surface form;
- the same morphology does not predict the objectively adjacent body paragraph under raw n-grams, A1-formal-residual n-grams, or retained lexical-family representations;
- attached `Lf` label tokens are not preferentially exact/edit1 related to their own adjacent paragraph after within-folio controls;
- A1-like entry + short-range family generation remains one of the strongest surviving structural mechanisms.

So the high-value question is now the **scale limit of that mechanism**, not another morphology encoding variant.

## Core references

- Montemurro, M. A. & Zanette, D. H. (2013). *Keywords and Co-Occurrence Patterns in the Voynich Manuscript: An Information-Theoretic Analysis*. PLOS ONE 8(6): e66344. DOI: 10.1371/journal.pone.0066344.
- Amancio, D. R. et al. (2013). *Probing the Statistical Properties of Unknown Texts: Application to the Voynich Manuscript*. PLOS ONE 8(7): e67310. DOI: 10.1371/journal.pone.0067310.
- Schinner, A. (2007). *The Voynich Manuscript: Evidence of the Hoax Hypothesis*. Cryptologia 31(2): 95–107. DOI: 10.1080/01611190601133539.
- Timm, T. & Schinner, A. (2020). *A possible generating algorithm of the Voynich manuscript*. Cryptologia 44(1): 1–19. DOI: 10.1080/01611194.2019.1596999.
- Bowern, C. L. & Lindemann, L. (2021). *The Linguistics of the Voynich Manuscript*. Annual Review of Linguistics 7: 285–308. DOI: 10.1146/annurev-linguistics-011619-030613.
- Greshko, M. (2025/2026). *The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext*. Cryptologia. DOI: 10.1080/01611194.2025.2566408.
