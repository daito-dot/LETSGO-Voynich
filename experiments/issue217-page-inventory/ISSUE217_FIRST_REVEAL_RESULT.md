# Issue #217 first reveal result

Date: 2026-09-10  
Parent: #172  
Prerequisite: #215 / PR #216  
Frozen issue: #217

## Classification

**`REPLICATED_PAGE_INVENTORY_ASSOCIATION`**

Within the prospectively frozen `pharmaceutical / Currier A / hand 1` stratum, the externally labelled H and P physical folios differ in running-text visible-token inventory composition under the exact frozen Jensen-Shannon statistic. The primary result passes in ZL3b and independently passes the preregistered IT2a replication.

This is a page/folio inventory-composition result. It is not the old Phase65-68 local plant-fragment morphology-to-label/body-text question.

## Frozen population

H folios:

- `f87`
- `f90`
- `f93`
- `f96`

P folios:

- `f88`
- `f89`
- `f99`
- `f100`
- `f101`
- `f102`

Permutation unit: physical folio.  
Exact null: all `C(10,4)=210` assignments.

## Authoritative first reveal

GitHub Actions run: `34466585648`  
Run head: `1d7c924df3b5f4f64a5445602fa33fe797749ac3`  
Artifact ID: `10147759045`  
Artifact digest SHA-256: `7ec05305b6c7e3dbcde45ec35e8bb039fc921ca123790d7f31981ab0cb9d3ddc`  
Frozen analysis script SHA-256: `4c3e0e869fee2f596321859a6c536e86a56e246188b1fb8df42b5d9266c8d95f`  
Authoritative result JSON SHA-256: `afc2b398b48f072f8e503d51d92a6f3b8856641b21f67d1fb77a6538b168220e`

Frozen source verification passed before scoring:

- ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, 411,671 bytes;
- IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`, 342,104 bytes.

## Primary result

### ZL3b

- union vocabulary: `1,241` visible token types;
- mean H-P JS: `0.7029621572027999` bits;
- pooled within-class JS: `0.6380505286698812` bits;
- `T = 0.06491162853291865` bits;
- one-sided exact permutation `p = 0.009523809523809525 = 2/210`;
- primary gate: **PASS**.

### IT2a replication

- union vocabulary: `1,259` visible token types;
- mean H-P JS: `0.7090101817212675` bits;
- pooled within-class JS: `0.6537334163833537` bits;
- `T = 0.055276765337913814` bits;
- one-sided exact permutation `p = 0.009523809523809525 = 2/210`;
- replication gate: **PASS**.

The between-class excess is therefore positive in both readings and the exact observed assignment lies in the upper 2/210 tail in both cases.

## Predictive corroboration

The frozen leave-one-folio-out nearest-centroid corroboration does **not** pass:

- ZL3b balanced accuracy `0.50`, exact `p = 0.45714285714285713`;
- IT2a balanced accuracy `0.50`, exact `p = 0.46190476190476193`.

This matters for interpretation. The primary finding is a group-level separation of inventory distributions. It is not evidence that an unseen individual folio can be reliably classified as H or P by the frozen nearest-centroid rule.

## Accidental post-result rerun and numerical reproducibility note

Archiving the authoritative raw JSON while the temporary workflow still had a branch-wide `push` trigger caused an unintended second Actions execution:

- run `34466745784`;
- artifact `10147823736`;
- excluded from first-reveal authority because it occurred after the result was already revealed.

The second run produced the same:

- final classification;
- exact p-values;
- pass/fail decisions;
- LOFO balanced accuracies and p-values;
- folio token/locus counts;
- vocabulary sizes.

Only a few raw floating-point values differ at approximately `1e-16`. Inspection identified the source: `js_bits()` iterates `set(p) | set(q)` without sorting, so Python hash iteration order changes floating-point summation order between processes. Example ZL3b `T` changed from `0.06491162853291865` to `0.06491162853291876`.

This does not alter any rank, exact p-value, threshold decision or scientific classification. The authoritative numerical record remains run `34466585648`. The workflow was removed immediately after detecting the duplicate trigger. No post-result feature, population, label, distance metric, threshold or classifier change was made.

## Accepted interpretation

Under the externally supplied H/P illustration classification, running-text visible-token inventory composition covaries with H versus P inside one stratum where section, Currier language and scribal hand are held constant.

The result survives the preregistered independent reading replication. It therefore cannot be dismissed as a single-transcription tokenization accident under the two frozen readings.

The failed LOFO corroboration limits the strength of the claim: the result is consistent with a distributed class-level shift rather than a simple, strongly separable folio-level signature.

## What this does not establish

It does not establish:

- the meanings of H or P text;
- that illustrations cause the lexical difference;
- that visible tokens are plaintext words;
- a specific topic vocabulary;
- plant identification;
- language identity;
- cipher identity;
- decipherment.

The old local pharmaceutical morphology-to-text population remains closed. This result opens a different page-level question only.

## No-rescue boundary

Per #217, do not now search stopword removal, token-frequency thresholds, n-grams, slot/shape representations, alternative distances, folio dropping, H/P relabelling or classifier families to improve the result. Any next content experiment must be a separately motivated and prospectively frozen question.
