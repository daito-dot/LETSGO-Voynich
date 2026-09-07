# Issue #172 candidate selection — T1463 historical mixed-granularity codebook preflight

Date: 2026-09-07
Parent: Issue #172
Current main at selection start: `d6880feb849303b02f93302db83f1ac06537fc86`
Status: **EXTERNAL HISTORICAL-AUTHORITY / CANDIDATE-SPECIFICATION PREFLIGHT ONLY — NO VOYNICH TARGET SCORING LICENSED**

## Why this lane is being opened

Issue #180 did not promote the LM-A0 line-managed allographic family. Issue #181 then established that a real historical monoalphabetic ciphertext (Borg) can exhibit the frozen R5-like topology: useful terminal→initial information within physical lines and no useful continuation across line breaks. Issue #182 could not fully attribute the Borg topology to plaintext vs physical line wrapping, but it did show, before any new edge score, that solved-word line wrapping materially contaminates naive boundary labels.

The immediate consequence for architecture selection is:

- do not spend the next candidate on another bespoke R5 reset mechanism;
- retain R5 as a responsibility, but treat it as compatible with historical ciphertext production;
- prioritize an independently attested architecture that has genuine **within-unit construction structure**, because R2 remains a hard responsibility.

The next family is therefore taken from a concrete fifteenth-century historical codebook architecture rather than assembled from the #176 failure vector.

## Historical anchor

Working identifier: **T1463-A0**.

Anchor manuscript/family:

- Francesco Tranchedino, *Diplomatische Geheimschriften*, Österreichische Nationalbibliothek, Cod. 2398;
- manuscript catalogue: Pavia, 1475–1496, 169 folios;
- the specific example used as the architecture anchor is on **fol. 37v**, dated **23 August 1463**, for Antonio de Besana;
- Tranchedino's 1475 compilation contained 159 Milanese codebooks accumulated to that point and was later continued to 297 ciphers; descriptions of the collection state that the codebooks repeatedly use a common structural template with changing cipher signs.

Independent metadata / secondary authorities:

- Austrian manuscript catalogue: https://manuscripta.at/_scripts/php/cat2pdf.php?cat=CMDA3&ms_code=AT8500-2368
- manuscript bibliography: https://manuscripta.at/lit_manu.php?ms=AT8500-2398
- historical codebook description / fol. 37v identification: https://cosec.bit.uni-bonn.de/fileadmin/user_upload/teaching/08ss/08ss-classical-crypto/notes.pdf
- later expanded treatment identifying fol. 37v and the repeated category template: https://dokumen.pub/cryptoschool-1nbsped-3662484234-978-3662484234.html
- facsimile-description source: https://www.facsimilefinder.com/facsimiles/francesco-tranchedino-secret-diplomatic-documents-facsimile
- large comparative key survey: https://www.tandfonline.com/doi/full/10.1080/01611194.2022.2113185
- cipher-key instruction survey with Cod. 2398 / DECODE key 2373 (1450–1496): https://www.tandfonline.com/doi/full/10.1080/01611194.2024.2396800

## Externally reported T1463 structure

The fol. 37v example is reported as a mixed-granularity system containing:

1. alphabetic elements: 21 plaintext letters with multiple cipher equivalents; frequent letters receive up to three homophones;
2. standard non-single-letter elements, including `&`, `con`, and `ex`;
3. null/dummy signs (`Nulle`);
4. dedicated signs for doubled letters (`Duplicate`);
5. a large systematic section of vowel+consonant digrams;
6. a mission-specific nomenclator of whole words, names, places and function-like terms.

The descriptive source gives the specific 1463 example as:

- 12 nulls;
- 12 doubled-letter signs;
- 63 vowel+consonant digram signs;
- 31 nomenclator codewords;
- 165 cipher signs in total.

A later discussion of several Tranchedino keys summarizes the recurring plaintext-category template approximately as:

- C1 letters and standard abbreviations: 24–25 elements;
- C2 short words: 10–12 where present;
- C3 dummies: 10–12;
- C4 vowel+consonant digrams: 60–70;
- C5 doubled consonants: 12;
- C6 words / persons / places: 30–60.

It also reports that T0 (the 1463 fol. 37v key) omits C2, while C1–C5 remain comparatively stable across related keys and C6 changes with the mission.

### Important unresolved authority point

The prose counts above are not sufficient to reconstruct the exact fol. 37v table. In particular, a naive arithmetic reconstruction from the prose summaries does not cleanly recover the reported total of 165 cipher signs. That inconsistency is treated as a **reason to audit the actual key/facsimile before freezing an executable candidate**, not as permission to choose convenient counts.

T1463-A0 is therefore a historical architecture family under preflight, not yet a frozen executable encoder.

## Broader historical support independent of Voynich

The large DECRYPT/DECODE survey of more than 1,600 early-modern keys independently establishes that mixed-granularity nomenclatures are historically ordinary rather than a construction invented for this project:

- nomenclatures may encode names, content words, function words, syllables, phrases and other linguistic elements;
- syllables already occur in fifteenth-century keys (roughly one quarter in the survey, increasing greatly later);
- fifteenth-century nomenclatures commonly use graphic signs and Latin letters, often in combination;
- diacritics are reported in roughly 40% of fifteenth-century nomenclatures;
- simple one-to-one nomenclature codes dominate the fifteenth century, although alphabet sections and other parts of a key may use homophony;
- Italian fifteenth-century material in the survey tends toward fixed-length code elements, while fifteenth-century Vatican material is notable for variable-length code systems.

This evidence licenses **mixed linguistic granularity and structured code inventories** as an independently historical search class. It does not say that the Voynich Manuscript uses this architecture.

## Difference from Issue #84 Phase B N256

T1463-A0 is not a rerun of the old synthetic `N256-1/N256-4` candidates.

Issue #84 Phase B defined `N256` as:

- the top 256 complete source word types selected by source frequency;
- each chosen whole word mapped to one or four opaque whole-word code atoms;
- all other words encoded by ordinary monoalphabetic substitution;
- source word and line boundaries preserved.

That screen deliberately tested **inter-token MI and recurrence**, not the later R2 token-internal construction responsibility. `N256-4` reached only the adjacent-MI target and failed the recurrence conjunction.

T1463-A0 instead imports a historically attested **multi-level plaintext inventory**: letters + special abbreviations + digrams + doubled letters + mission codewords + nulls, with letter homophony. It is neither source-frequency top-256 selection nor a whole-word-only nomenclator.

No old `N256` score is reused as evidence that T1463-A0 will pass or fail the #172 battery.

## Candidate role under preflight

Provisional primary role if the authority audit succeeds:

> **REVERSIBLE TRANSFORM / DECODER CANDIDATE**

This role is conditional. Promotion requires the external key audit to establish enough information to define a deterministic inverse under an explicit interface.

At minimum distinguish:

- exact recovery of plaintext character stream;
- recovery of source lexical spacing;
- recovery of cipher-secretary segmentation choices;
- recovery/removal of nulls.

If only normalized character-stream recovery can be guaranteed, R9 must say so. Exact word-boundary recovery may not be claimed unless historical separators or the key make it identifiable.

## Stage H0 — historical-key authority audit

**H0 is the only currently licensed executable/research work in this lane. It must not score Voynich.**

Before any synthetic plaintext encoding or Voynich output exists, freeze:

1. the exact fol. 37v plaintext-element inventory by category;
2. the exact number of cipher equivalents for every alphabetic / special element;
3. the exact null inventory;
4. the exact doubled-letter inventory;
5. the exact digram inventory;
6. the exact nomenclator inventory size and whether its values are unique;
7. whether cipher signs are disjoint across categories or whether any sign is polyphonic;
8. any explicit instructions governing null use, repeated-letter signs, nomenclator use or segmentation;
9. whether the historical ciphertext practice preserves spaces or another recoverable unit boundary;
10. whether related Tranchedino keys reproduce the same category architecture independently of their mission-specific C6 vocabulary.

Preferred authority order:

1. fol. 37v facsimile / reliable diplomatic transcription;
2. Cod. 2398 scholarly facsimile commentary / DECODE transcription if available;
3. scholarly descriptions that explicitly identify the folio and table;
4. general historical survey only for family-level corroboration.

Do not fill an unreadable or unavailable cell from a Voynich-motivated design choice.

## Stage H0 hard outcomes

### `H0_ARCHITECTURE_RECOVERED`

Requires all of:

- exact category/cardinality authority sufficient to implement the table structure;
- no unresolved symbol collision that makes the inverse undefined without extra rules;
- at least one independently documented usage/segmentation policy or a mathematically valid representation of all historically legal encodings that does not choose among them using Voynich;
- R9 recoverability class can be stated precisely;
- R10 key/vocabulary/side-information cost can be counted.

### `H0_ARCHITECTURE_PARTIAL`

Use if the historical mixed-granularity architecture is clear but the exact choice/segmentation policy remains underdetermined. In that case T1463 may remain historical evidence for a mechanism class but **cannot enter the #172 target tournament yet**.

### `H0_AUTHORITY_INSUFFICIENT`

Use if the key table cannot be reconstructed with adequate provenance or if critical category/count claims conflict irreconcilably.

No threshold relaxation after inspecting Voynich is permitted because H0 never inspects Voynich candidate output at all.

## Stage H1 — external encoder preflight, conditional on H0 only

H1 is blocked until H0 is frozen as `H0_ARCHITECTURE_RECOVERED`.

If H0 passes, select an external fifteenth-century diplomatic plaintext corpus **by date/genre/provenance before any transformed statistic is measured**. A Sforza diplomatic corpus is preferred if licensing and reproducible parsing are adequate because it matches the key's own administrative environment.

H1 must then freeze, from historical authority only:

- plaintext normalization;
- unit-selection policy when several plaintext elements overlap (e.g. letter vs digram vs nomenclator word);
- homophone-selection policy;
- null-use policy;
- source-space / cipher-space treatment;
- line treatment;
- exact encode/decode closure definition.

If historical usage does not determine one of these, H1 may represent the mechanism as a finite set of legal encodings and test all/legal-sampled encodings under a target-blind rule, but it may not choose a rule because it produces a more Voynich-like surface.

### H1 target-free checks

H1 may measure only properties of the external encoded corpus needed for construct validity, for example:

- exact/normalized decode closure;
- code-element usage and category coverage;
- whether the historical architecture actually exercises multiple plaintext granularities on held-out diplomatic text;
- whether the resulting cipher stream has a bounded local construction language under its own native representation.

Do not compare any H1 statistic with Voynich thresholds or use a Voynich distance to select policies.

## Candidate complexity / target-access declaration for later R10

If T1463 is eventually promoted, the later tournament must charge at least:

- full alphabetic homophone table;
- standard abbreviation table;
- digram table;
- doubled-letter table;
- null inventory and null-use policy;
- nomenclator vocabulary and its cipher equivalents;
- any mission-specific codeword table;
- any separator/segmentation convention;
- any stochastic seed or rule required for homophone/null choices;
- external source-language corpus or model used to generate plaintext;
- inverse side information.

A mission-specific nomenclator is a real historical component, but it is still a vocabulary lookup table and must be charged under R10. It does not become free merely because it is historically attested.

Forbidden target access before tournament freeze:

- Voynich token vocabulary to choose nomenclator entries;
- Voynich token/slot frequencies to choose digram inventory;
- Currier labels to choose separate keys;
- Voynich line layout to tune null or homophone use;
- target-derived symbol shapes to design the cipher alphabet;
- #176 failure vector to add cache, paragraph state or R5 reset submodules.

## Expected relationship to R1–R10 — hypotheses, not credits

Before target scoring, no responsibility is marked PASS.

- **R2:** primary reason to test the family. Mixed letter/digram/double/codeword units provide a genuine historical route to nontrivial within-output construction. Whether it resembles the frozen complete-66 topology is unknown.
- **R5:** no special T1463 reset module is added. #181 shows a historical ciphertext can inherit line-local topology; T1463 must take whatever line behavior follows from its independently frozen source/production interface.
- **R3/R4/R8:** may only be inherited from the external source or an independently attested production rule. No cache or paragraph repair is added.
- **R6/R7:** no reading-specific or Currier-specific table is granted. Any later target-side metadata access must be separately charged and preregistered.
- **R9:** potentially strong because the historical key is a substitution/codebook system, but exact closure class is not declared until H0/H1 resolve nulls, segmentation and spacing.
- **R10:** expected to be nontrivial because the architecture contains a substantial key and a mission-specific nomenclator. This complexity must remain visible.

## Selection firewall

Do not:

- infer the exact fol. 37v table from the reported total by adjusting category counts;
- choose a greedy/digram-first/word-first encoder because it scores better on Voynich;
- select a source language or diplomatic corpus after observing Voynich distance;
- replace historical signs with slot-shaped Voynich glyphs before the abstract mechanism passes a separately frozen surface-realization gate;
- add local repetition, Currier state, paragraph memory, line resets or drawing-aware rules to cover known responsibilities;
- reuse Issue #84 N256 partial scores as a tuning signal;
- call a structurally adequate encoder a decipherment unless R9 inverse recovery also passes its separately frozen target.

## Current selection decision

> **Carry T1463-A0 forward to H0 historical-key authority audit only.**

> **No new Voynich candidate is licensed for target scoring yet.**

The reason for carrying it forward is independent historical specificity: a fifteenth-century Milanese key family already combines homophonic alphabetic signs, multi-letter units, doubled-letter units, nulls and whole-word nomenclature under a stable recurring template. The reason it is not yet a candidate is equally specific: the exact table arithmetic, collision structure and encoding-choice policy still require authority before a bounded executable mechanism can be frozen.
