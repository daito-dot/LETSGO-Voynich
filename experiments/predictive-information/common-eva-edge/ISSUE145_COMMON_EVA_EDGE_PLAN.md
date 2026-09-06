# Issue #145 — common-EVA dual terminal→initial edge test

Date: 2026-09-07
Status: **FROZEN BEFORE ANY ISSUE #145 POS2/EDGE2 SCORE**
Parent: Issue #88
Entry authority: Issue #139 / PR #144
Representation authority: Issues #112/#115 Phase4A/4B
Architecture authority: Issue #125

## Question

Does the same-line previous-terminal → next-initial predictive architecture remain robust in **both** ZL3b and independent Takahashi/IT2a when both readings are expressed through the same pre-existing Basic-EVA atomization and evaluated under one frozen held-out contract?

This is a representation-consolidation test. It does not search for a new normalization and it does not test literal table transport.

## 1. Frozen sources

### ZL3b

- mirror: `matthewdgreen/cipher_benchmark`
- mirror commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- path: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- IVTFF header: `#=IVTFF Eva- 2.0 M 5`
- Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`

### IT2a

- URL: `https://www.voynich.nu/data/IT2a-n.txt`
- lineage/alphabet: Takeshi Takahashi / EvaT
- IVTFF header: `#=IVTFF EvaT 2.0 M 3`
- bytes: `342104`
- lines: `5444`
- Git blob SHA-1: `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

No alternate revision or post-reveal repair is allowed.

## 2. Frozen representation authority

Reuse without modification:

- Phase4A Basic-EVA authority: `experiments/predictive-information/phase4a/phase4a_boundary_gate0.py`
  - Git blob SHA-1 `756380dcd6f1b024a359923852627460c0f64dd0`
- Phase4B IT2a adapter authority: `experiments/predictive-information/phase4b/phase4b_it2a_gate0.py`
  - Git blob SHA-1 `7520e1a5f2c64a4ccbc3cc0e65668a4e0a5391cb`
- unchanged SlotParser: `experiments/issue26-music/issue26e_core.py`
  - Git blob SHA-1 `8bafba7f2bce4cf77c9001c729936c1ce619759b`

Representation:

- P-coded IVTFF loci only;
- each P-coded locus is one source line;
- split certain visible units only on literal IVTFF `.` outside markup;
- strip only documented structural edge markers `<%>` / `<$>`;
- longest-match connected composites: `cfh`, `ckh`, `cph`, `cth`, `ch`, `sh`;
- all remaining Basic-EVA letters are one atom;
- comma/uncertainty/high-ASCII/ligature/inline markup/uppercase connectivity/tick/non-Basic-EVA/other exceptional content makes that segment unclean;
- no reading-specific remapping.

The common atom outcome set is fixed before scoring:

- 25 Basic-EVA single-letter atoms;
- 6 connected-composite atoms;
- one `END_TOKEN`;
- categorical outcome vocabulary size `V=32`;
- `BOS` is context padding only and is not an outcome.

## 3. Clean-run reset amendment

Issue #145 Amendment A was frozen in the Issue thread before this Gate code existed.

Within each source line, split the literal-`.` segments into maximal contiguous **clean runs**.

- reset at source-line start and after every unclean segment;
- first clean token of a run uses generic START onset support;
- subsequent clean tokens in the same run are BODY and have an immediately observable previous clean token;
- no edge or short context crosses an unclean segment;
- training uses every clean token in every run;
- primary held-out scoring additionally requires the current raw token to be accepted by the unchanged SlotParser;
- previous clean token need not be SlotParser-accepted.

This is missing-data handling, not a scientific target choice.

## 4. Frozen folds

Reuse the original five physical-leaf folds from the Phase4A authority.

Required fold identity SHA-256:

`cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`

No fold balancing, shuffling or reading-specific regrouping is allowed.

## 5. Score-free Gate0 support rule

Before any predictive probability is implemented, Gate0 must verify for **each reading**:

- exact source identity and header;
- exact representation/SlotParser code blobs;
- exact fold hash;
- P-coded line support and frozen-leaf coverage;
- clean token count;
- clean-run count;
- run-start/run-body counts;
- primary SlotParser-accepted counts by fold;
- accepted run-body targets by fold;
- at least `300` accepted primary targets in every fold;
- at least `300` accepted run-body targets in every fold;
- nonzero training START/BODY support in every outer training complement;
- at least 2 previous-terminal atom contexts in every outer training complement;
- at least 2 previous-terminal→initial atom pairs in every outer training complement;
- every emitted atom belongs to the frozen 31-atom set.

Gate0 may report support counts and exclusions. It must not calculate a probability, log likelihood, bits/token, edge gain, native/common effect ratio, cross-reading agreement statistic, table similarity or final scientific classification.

A failed Gate maps only to `INVALID COMMON-REPRESENTATION EDGE TEST` and blocks scoring.

## 6. Frozen atom-level POS2/EDGE2 architecture

After a merged successful Gate0, the scientific scorer must use:

- fixed atom order `k=2`;
- additive `alpha=0.01`;
- `V=32` outcomes;
- clean-run hard reset;
- no hyperparameter selection.

### POS2_COMMON

For each clean token:

1. first atom at run start: pooled START first-atom distribution;
2. first atom in run body: pooled BODY first-atom distribution ignoring previous identity;
3. second emitted atom: conditioned on current first atom, separately for START/BODY; the outcome may be another atom or `END_TOKEN`;
4. third and later emitted atoms: shared fixed-k2 clean-run atom transition table.

### EDGE2_COMMON

Identical to POS2_COMMON except exactly one factor:

- BODY first atom is conditioned on the immediately previous clean token's terminal atom in the same clean run.

Unseen exact contexts use empty additive smoothing, yielding a uniform `1/32` distribution. No pooled fallback/backoff may be added.

## 7. Frozen primary evaluation

For reading `R` and untouched outer fold `f`:

`G_common[R,f] = bits(POS2_COMMON)[R,f] - bits(EDGE2_COMMON)[R,f]`.

A reading passes iff:

- mean `G_common[R] > 0`; and
- `G_common[R,f] > 0` in at least `4/5` folds.

Exactly one valid scientific class:

1. `COMMON-EVA EDGE ROBUST IN BOTH READINGS`
2. `COMMON-EVA EDGE ROBUST IN ZL3B ONLY`
3. `COMMON-EVA EDGE ROBUST IN IT2A ONLY`
4. `COMMON-EVA EDGE NOT ROBUST IN EITHER READING`
5. `INVALID COMMON-REPRESENTATION EDGE TEST`

No post-reveal rescue class or magnitude threshold.

## 8. Frozen non-promoting diagnostics

The scorer may report, without affecting classification:

- foldwise `G_common[IT2a]-G_common[ZL3b]`;
- mean-gain ratio if both means are positive;
- descriptive change from frozen native Issue #125 / Issue #139 gains;
- previous-terminal support coverage;
- Currier A/B descriptive strata only if available without target-driven mapping;
- EDGE2_COMMON vs full clean-run-contiguous atom-k2 token-logp equivalence, expected algebraically to be exact.

## 9. Chronology firewall

1. commit this plan and a score-free Gate0 executable;
2. run Gate0 without any Issue #145 target score;
3. archive and merge the successful Gate authority;
4. only then commit the scientific scorer separately;
5. commit the scorer before its first target workflow exists/runs;
6. no representation, exclusion, reset, folds, smoothing, target population or pass-rule change after reveal.

Forbidden:

- target-selected normalization;
- token alignment by ZL3b↔IT2a surface similarity;
- cross-line context;
- skipping across unclean segments;
- Currier/hand/section-conditioned fitting;
- latent states;
- S1/S2/H62/R1 tuning;
- semantic/cipher/historical inference.

## 10. Interpretation boundary

A dual pass would promote the edge to a common-representation cross-transcription predictive responsibility and make a subsequent literal table/strength transport test scientifically well-posed.

A one-reading pass or dual fail would demonstrate representation sensitivity that must be understood before manuscript-wide consolidation.

No outcome establishes natural-language words, plaintext, semantics, language, cipher family, historical direction, authorship, artificiality/hoax or decipherment.

Refs #88 #112 #115 #125 #134 #139 #145.
