# Issue #72 V2 — prior art and publication positioning

Date checked: 2026-09-01  
Scope: Voynich token-internal structure, generative/cipher models, Naibbe-class mechanism tests, order/allocation randomizations, and the specific R1 responsibility decomposition.

## Bottom line

The broad ideas behind Issue #72 are not novel in isolation. Prior literature already establishes that Voynich tokens have strong internal positional structure, that encoding/generative mechanisms can reproduce unusual Voynich statistics, and that Naibbe is a published, reversible, historically motivated Voynich-like cipher. Recent 2026 preprints also perform model discrimination, generator ablation/inversion, and order-sensitive analyses.

The defensible contribution of Issue #72 is narrower:

1. define a replicated R1 target as the null-residual dependency topology over all 66 unordered pairs of binary occupancies in a frozen 12-slot representation;
2. show that published Naibbe reproduces that target against ZL3b and IT2a;
3. prospectively decompose responsibility for that same fixed target at three distinct causal layers:
   - fixed-path emitted-value association (C1: EL/ES/ET/EG),
   - full-pipeline within-line plaintext-order intervention (PT),
   - final complete-token / occupancy-signature allocation sufficiency (FI);
4. localize the R1-sensitive layer to the production and corpus-level inventory/dependency structure of 12-slot occupancy signatures, with strong upstream sensitivity to effective-letter/state-dependent emitted-value assignment but no detected additional requirement for exact local plaintext order or observed placement of finished signatures.

Exact-term searches on 2026-09-01 for Voynich + `Yule Q`, `Yule's Q`, `Mantel-Haenszel`, `slot pair`, `66 slot pairs`, `residual topology`, `slot occupancy`, and close variants did not surface a prior scholarly publication implementing the same R1 construction. This is search evidence, not proof of non-existence.

## Literature that should be treated as foundation rather than re-proved

### Bowern & Lindemann (2021) — linguistic/statistical overview

Claire L. Bowern & Luke Lindemann, “The Linguistics of the Voynich Manuscript,” *Annual Review of Linguistics* 7 (2021), 285–308. DOI: 10.1146/annurev-linguistics-011619-030613.

Use for: established linguistic/statistical background, the abnormal predictability problem, and the need to separate script/morphology/statistics from claimed decipherment.

Publication status: peer-reviewed review article.

### Lindemann & Bowern (2020/2022) — conditional character entropy

Luke Lindemann & Claire Bowern, “Character Entropy in Modern and Historical Texts: Comparison Metrics for an Undeciphered Manuscript,” arXiv:2010.14697.

Use for: Voynich character placement is unusually constrained within tokens and this is robust to major transcription/glyph-composition manipulations.

Publication status: working paper / arXiv preprint; cited by later peer-reviewed/review literature.

### Zattera (2022) — 12-slot word structure

Massimiliano Zattera, “A New Transliteration Alphabet Brings New Evidence of Word Structure and Multiple ‘Languages’ in the Voynich Manuscript,” Proceedings of VOY2022, CEUR-WS Vol. 3313, paper 10.

Use for: the 12-slot representation and the established claim that a large majority of Voynich tokens conform to strong internal positional structure. Issue #72 should not claim discovery of slot-like token grammar.

Publication status: peer-reviewed conference paper; VOY2022 used a two-phase double-blind process, 16 accepted of 32 submissions.

### Bowern & Gaskell (2022) — cipher transformations can create Voynich-like word statistics

Claire L. Bowern & Daniel E. Gaskell, “Enciphered after all? Word-level Text Metrics are Compatible with some Types of Encipherment,” Proceedings of VOY2022, CEUR-WS Vol. 3313, paper 6.

Use for: several text transformations/encipherment schemes can reduce conditional entropy or increase word-form predictability into the Voynich range; abnormal surface statistics alone do not rule out enciphered language.

Publication status: peer-reviewed conference paper.

### Hermes (2022) — historical cipher can mimic artificial-language-like statistics

Jürgen Hermes, “Polygraphia III: The Cipher that Pretends to be an Artificial Language,” Proceedings of VOY2022, CEUR-WS Vol. 3313, paper 7.

Use for: a historical cipher family can produce artificial-language-like/Voynich-like surface statistics. This is useful historical precedent for mechanism-first comparison.

Publication status: peer-reviewed conference paper.

### Greshko (2025) — direct parent work

Michael A. Greshko, “The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext,” *Cryptologia* (published online 26 Nov 2025). DOI: 10.1080/01611194.2025.2566408.

Use for: exact Naibbe mechanism, historical-hand-executability argument, reversibility, plaintext preservation, and demonstrated reproduction of multiple Voynich statistical properties. This is the direct platform on which Issue #72 operates.

Publication status: peer-reviewed journal research article, CC BY.

Preferred positioning: Greshko establishes that one concrete reversible cipher can produce broad Voynich-like properties; Issue #72 asks which parts/layers of that known mechanism causally carry one replicated token-internal topology target.

## Close prior art that must be discussed explicitly

### Parisel (2026) — structural signatures and generator discrimination

Christophe Parisel, “Evidence of Layered Positional and Directional Constraints in the Voynich Manuscript: Implications for Cipher-Like Structure,” arXiv:2604.19762.

Finds distinct word-internal and word-boundary directional/positional signatures and evaluates structured generators against a joint four-signature criterion, including Naibbe in the full paper.

Overlap: mechanism discrimination using structural rather than purely static statistics.

Difference: the targets are directional/boundary signatures, not the 66-edge residual occupancy topology; the paper does not perform the Issue #72 C1/PT/FI responsibility decomposition.

Publication status: arXiv preprint as of 2026-09-01.

### Averyanov (2026) — closest mechanism-level prior art

Vitaly Averyanov, “A Workshop Cipher: a Generative Model Reproducing the Statics and Dynamics of the Voynich Manuscript Text,” Zenodo preprint DOI: 10.5281/zenodo.21761192. Public priority recorded 02 Aug 2026; journal/arXiv submission reported as in progress.

This work explicitly builds on a Naibbe-class cipher and performs mechanism inversions/ablations. Reported tests include reducing table count, skewing global table weights, introducing per-unit habitual table choice, adding/removing serial reuse, graphotactic boundary choice, spelling noise, and plaintext-genre comparisons. It argues that uniform table randomization is functionally necessary for its own discriminator targets. It also reports that within-word ciphertext-character shuffling destroys its directionality signature.

Overlap: causal/mechanistic testing of a Naibbe-class generator. Therefore Issue #72 must not claim to be the first Naibbe ablation or first causal decomposition of a Voynich-like generator in a broad sense.

Difference: Averyanov's measured targets are entropy, lexicon/twin statistics, serial clustering, boundary/directionality signatures and related discriminator windows. Issue #72 asks responsibility for a different fixed object: the replicated 66-edge residual topology of 12-slot occupancies. Its PT intervention shuffles plaintext characters within each line while preserving exact linewise character composition and reruns the complete Naibbe pipeline; this is not the same as within-word ciphertext shuffling. FI separately tests the allocation sufficiency of already-produced occupancy signatures.

Publication status: Zenodo preprint, not peer-reviewed as of 2026-09-01. Treat its results as close prior art, not settled fact.

### Rozanova & Temerev (2026) — weak token succession, stronger unit/boundary structure

Liudmila Rozanova & Alexander Temerev, “A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space: What the Units of Voynichese Are Not,” arXiv:2608.17096 (17 Aug 2026).

Reports that token identity predicts the next token only weakly, while recurrent multi-symbol units and token-edge coupling are stronger; also compares a published Voynich-like cipher and self-citation generator.

Overlap: supports moving explanatory weight away from naive token-as-word succession toward internal/boundary structure.

Difference: observational/descriptive inference on Voynich/control streams, not a matched upstream intervention through a known reversible cipher and not the R1 occupancy-topology estimand.

Publication status: arXiv preprint.

### De Stefano (2026) — mechanism discrimination with known-mechanism positive controls

Carmine De Stefano, “The Generative Frontier of the Voynich Manuscript,” Zenodo preprint DOI: 10.5281/zenodo.21560144.

Uses matched synthetic corpora of known mechanism and discriminates Cardan-grille/self-citation/local-copy style generators with local reuse, entropy and lexical-productivity axes, plus a Parisel cross-check.

Overlap: mechanism-class discrimination, positive controls and ablation/reconstruction logic.

Difference: different candidate mechanisms and target statistics; no 12-slot residual occupancy topology and no Naibbe C1/PT/FI responsibility decomposition.

Publication status: Zenodo preprint.

## Older generative/statistical literature to cite selectively

- Andreas Schinner (2007), “The Voynich Manuscript: Evidence of the Hoax Hypothesis,” *Cryptologia* 31(2):95–107. DOI: 10.1080/01611190601133539. Stochastic-generation argument.
- Gordon Rugg (2004), “An Elegant Hoax? A Possible Solution to the Voynich Manuscript,” *Cryptologia* 28(1):31–46. DOI: 10.1080/0161-110491892755. Table-and-grille generation.
- Gordon Rugg & Gavin Taylor (2017; online 2016), “Hoaxing statistical features of the Voynich Manuscript,” *Cryptologia* 41(3):247–268. DOI: 10.1080/01611194.2016.1206753. Quantitative reproduction of major surface statistics by table/grille generation.
- Torsten Timm & Andreas Schinner (2020; online 2019), “A possible generating algorithm of the Voynich manuscript,” *Cryptologia* 44(1):1–19. DOI: 10.1080/01611194.2019.1596999. Self-citation/local-copy generator.
- Marcelo A. Montemurro & Damián H. Zanette (2013), “Keywords and Co-Occurrence Patterns in the Voynich Manuscript: An Information-Theoretic Analysis,” *PLOS ONE* 8(6):e66344. DOI: 10.1371/journal.pone.0066344. Long-range token-distribution organization and shuffle baselines.
- Sravana Reddy & Kevin Knight (2011), “What We Know About The Voynich Manuscript,” ACL-HLT LaTeCH workshop. Useful early computational survey and constraints.

These should establish the historical debate rather than be treated as direct competitors to Issue #72.

## Claims that are not safe

Do not claim:

- first discovery of strong Voynich token-internal structure;
- first demonstration that a generator/cipher can mimic Voynich statistics;
- first reversible/historically plausible Voynich-like cipher;
- first ablation or mechanism decomposition of a Naibbe-class generator;
- broadly, first evidence that “order does not matter” in Voynich-like text.

All of these have substantial prior art or are too broad to defend.

## Defensible novelty statement

A conservative wording for a paper is:

> We build on the published Naibbe cipher and prior slot-grammar/generative-model work to ask a narrower mechanism-localization question. We define a replicated target as the null-residual dependency topology over all 66 unordered pairs of a frozen 12-slot token-occupancy representation, then prospectively intervene at fixed-path emission assignment, upstream plaintext order, and downstream token allocation. To our knowledge, prior Voynich studies have not separated responsibility for this same fixed topology across those three layers.

A stronger “first” formulation should be used only after a final bibliographic search immediately before submission.

## What Issue #72 can inherit from prior work

The paper does not need to re-establish from scratch that:

- Voynich tokens are positionally constrained / slot-like — cite Zattera; Bowern & Lindemann;
- unusual predictability alone is compatible with encoding transformations — cite Bowern & Gaskell; Hermes;
- a concrete reversible hand-executable Naibbe cipher can reproduce broad Voynich statistics — cite Greshko;
- static fit is not enough and structural/dynamic signatures can discriminate models — cite Parisel and recent mechanism work;
- Naibbe-class generators have already been subjected to some mechanism inversions — cite Averyanov explicitly.

The paper should spend its empirical budget on R1 definition/replication and the C1 -> PT -> FI localization, where the literature search found the clearest gap.

## Search limitation

This note records a targeted prior-art search across journal/publisher pages, CEUR/VOY2022, arXiv, Zenodo-linked preprints, broad web indexing and exact method-keyword searches available on 2026-09-01. It is not a formal systematic review of every non-English book, thesis, private forum archive or unindexed manuscript. “To our knowledge” remains the correct novelty qualifier.
