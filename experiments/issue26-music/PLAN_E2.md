# Issue #26E2 — high-resolution and independent-transcription replication

Status: **FROZEN BEFORE E2 EXECUTABLE / E2 SCIENTIFIC REVEAL**

Issue: #26

Base main: `8ae9b237641725a6eda852027eb6afb366c147a5`

Issue26E produced a narrow positive result under a frozen Zattera-slot / Guidonian-lattice test. E2 does not add musical degrees of freedom. It attacks that result in three prespecified ways.

## Frozen source identities

### ZL3b replay source

- repository: `matthewdgreen/cipher_benchmark`
- commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- path: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`

### IT2a independent-reading source

- canonical distribution: `https://www.voynich.nu/data/IT2a-n.txt`
- transcription lineage: Takeshi Takahashi / EvaT, independently used previously in Phase63B
- frozen SHA-256 from the accepted Phase63B source audit: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

If the live canonical IT2a bytes no longer match that SHA-256, E2 must fail before science rather than silently update the source.

## Frozen physical-leaf folds

Do not reconstruct/rebalance folds from IT. Reuse the exact Issue26E/ZL five fold memberships:

- fold 0: `1,6,11,17,22,27,32,37,42,47,52,57,68,77,82,87,94,101,106,113`
- fold 1: `2,7,13,18,23,28,33,38,43,48,53,58,69,78,83,88,95,102,107,114`
- fold 2: `3,8,14,19,24,29,34,39,44,49,54,65,70,79,84,89,96,103,108,115`
- fold 3: `4,9,15,20,25,30,35,40,45,50,55,66,75,80,85,90,99,104,111,116`
- fold 4: `5,10,16,21,26,31,36,41,46,51,56,67,76,81,86,93,100,105,112`

If an IT leaf contains no usable P-coded token population it remains assigned but contributes no tokens; no reassignment is allowed.

## Frozen representation

Reuse the merged Issue26E code and definitions unchanged unless this plan explicitly says otherwise:

- fresh 12-position Zattera parser and its validation assertions;
- primary `min` earliest-valid and sensitivity `max` latest-valid parses;
- slot 10 as the unique six-state candidate channel `EMPTY,d,l,r,m,n`;
- slots `0..9,11` one-hot representation with slot 10 removed;
- deterministic sequence-blind `k=20` clustering on unique training token types;
- fixed Guidonian 20×6 allowed-pair lattice;
- degree-preserving non-Guidonian nulls;
- all mapping fit only on training physical leaves;
- held-out score `A = allowed parsed occurrences / parsed occurrences`.

No source-specific token repair, glyph remapping, feature tuning, alternative slot choice or alternative gamut is permitted.

## E2-A — higher-resolution ZL null replay

Purpose: determine whether the first-reveal `p=1/101` was merely a low-resolution 100-null artifact.

Repeat the complete Issue26E analysis on the exact ZL3b source with **1,000** degree-matched null lattices per fold for both `min` and `max` parser policies.

Null labels remain exactly the Issue26E labels for `j=0..999`:

`Issue26E:<policy>:fold:<f>:null:<j>`

Therefore the first 100 null matrices are the original frozen nulls and the next 900 are a pure Monte-Carlo extension.

E2-A passes if:

- primary `min` coverage >= 0.60;
- primary global p <= 0.05;
- primary global advantage > 0;
- Guidonian accuracy exceeds fold-specific null median in at least 4/5 folds;
- `max` sensitivity global advantage > 0 and p <= 0.10.

The original 100-null summaries must also reproduce their Issue26E values within floating-point tolerance; otherwise E2 stops as a replay failure.

## E2-B — independent IT2a architecture replication

Run the complete Issue26E architecture on IT2a using the frozen ZL fold memberships but fitting the 20 clusters and all lattice mappings from IT training leaves only.

Use **100** degree-matched null lattices per fold and new deterministic labels:

`Issue26E2:IT:refit:<policy>:fold:<f>:null:<j>`

This is a replication of the architecture, not a fixed symbol dictionary.

E2-B passes if the original Issue26E gate is satisfied on IT:

- `min` coverage >= 0.60;
- `min` global p <= 0.05;
- `min` Guidonian accuracy > null median in >=4/5 folds;
- `max` sensitivity has positive global advantage and p <= 0.10.

## E2-C — prospective fixed-map IT transfer

Issue26E revealed, post hoc, that under the `max` parser one slot10→vox mapping recurred unchanged in 4/5 ZL folds. That observation is **not evidence for E**, but it is now frozen before any IT slot-lattice result is inspected and becomes a prospective E2 prediction.

Frozen mapping, using slot-state order `EMPTY,d,l,r,m,n` and vox order `ut,re,mi,fa,sol,la`:

- `EMPTY -> ut`
- `d -> fa`
- `l -> sol`
- `r -> re`
- `m -> mi`
- `n -> la`

Equivalent index tuple: `(0,3,4,1,2,5)`.

For E2-C:

- use IT2a `max` parses only;
- fit the sequence-blind 20 morphology clusters from IT training leaves;
- **do not optimize or permute the six slot-state→vox mapping**;
- fit only the 20 cluster→locus row assignment on IT training leaves using the frozen Guidonian columns;
- for every null lattice, keep the same six fixed state→column index mapping and fit only its 20 row assignment;
- use 100 degree-matched nulls per fold with labels `Issue26E2:IT:fixed:fold:<f>:null:<j>`.

E2-C passes if:

- max-policy IT parse coverage >= 0.60;
- fixed-map global p <= 0.05;
- fixed-map global advantage > 0;
- fixed-map Guidonian accuracy exceeds the fold-specific null median in >=4/5 folds.

This is the strongest E2 test because the six-state semantic column mapping is no longer free on IT.

## E2 classification

- **`STRONG GUIDONIAN SLOT REPLICATION`**: E2-A, E2-B and E2-C all pass.
- **`PARTIAL GUIDONIAN SLOT REPLICATION`**: E2-A passes and exactly one of E2-B/E2-C passes.
- **`ZL-ONLY / NOT INDEPENDENTLY REPLICATED`**: E2-A passes but both IT tests fail.
- **`ORIGINAL E NOT STABLE`**: E2-A fails.

Even the strongest classification remains a structural coding result. It is not a musical decipherment.

## Next-step firewall

No melody extraction, pitch-order fitting, hexachord-mutation sequence test, duration model or glyph-note naming may be introduced until E2 is revealed and recorded. If E2 is positive, sequence-level tests require a new frozen plan.
