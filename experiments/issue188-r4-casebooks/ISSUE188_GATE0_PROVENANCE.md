# Issue #188 — R4 / Casebooks Gate0 provenance

Date: 2026-09-08  
Parent: Issue #188 / Issue #172  
Status: **GATE0 VALID — STAGE1 LICENSED**

## Frozen authorities

- Gate0 base main: `544a3ae97001ff4ea8c353bde805aee7a1157005`
- issue: #188
- pull request: #189
- final Gate0 branch head: `e1346cde916480ae04db23dce80a008bb3df2c39`
- Gate0 plan blob: `41a4e1857d12876bedea69b0397f51e976b6ca2c`
- Gate0 auditor blob: `9792e32a0cb86bd293491701625e8fe2d530aacd`
- Gate0 workflow blob: `70f1e88db5871249f9b86d6f1db0572e09d20589`
- external repository: `CasebooksProject/casebooks-data`
- external commit: `9d42295d72b5ba8889575a32d79311cc72bce73a`

No Casebooks S1 value had been computed before this Gate0 completed.

## Transport chronology

The first full-corpus attempt used repeated external-DTD resolution and was terminated by the hosted runner before any support result was emitted:

- run: `34165611368`
- job: `101875928671`
- score-free audit step conclusion: `cancelled`
- termination: hosted runner shutdown signal after approximately 87 seconds
- scientific result: none
- artifact: none

Because that attempt produced neither support output nor scientific S1 output, a transport-only recovery was frozen before retry. The scientific extraction and admission rules were not changed.

The recovery removes the repeated external `DOCTYPE`, preserves XML predefined entities, maps any other named entity to one Unicode Private Use placeholder (`Co`, therefore never a Letter/Mark token), and parses standalone XML in parallel. In the successful full-corpus result, `opaque_entity_refs = 0`, so no source entity was actually replaced.

## Successful Gate0 execution

- workflow: `Issue188 R4 Casebooks Gate0`
- run ID: `34165815876`
- job ID: `101876515916`
- run/job conclusion: `success`
- final head: `e1346cde916480ae04db23dce80a008bb3df2c39`
- artifact name: `issue188-r4-casebooks-gate0`
- artifact ID: `10034102947`
- artifact ZIP SHA-256: `a431b35c80ce3a1511a83720c8ad8827a10e5cb0c3c15b408778982f10c0058f`
- raw JSON SHA-256: `6273e7a2abf53a1a95d1bca51e4d19718d49b89d171e75e55ecb6a60c87359ef`
- raw JSON Git blob: `008634b2db4359bf1bb78b1bc31b30913836ff17`
- raw result schema: `issue188-r4-casebooks-gate0-v2-transport`

The successful workflow asserted the literal marker:

`NO ISSUE188 SCIENTIFIC S1 SCORE COMPUTED`

and `scientific_score_computed: false` before artifact upload.

## Score firewall

Gate0 did not:

- parse ZL3b or IT2a;
- import Phase62 S1 feature/projection code;
- compute the eight-feature vector, target fold directions, paragraph contrasts, S1, sign counts, target ratios, or an R4 scientific classification;
- select cases, paragraphs, source volumes, hands, practices, or tokenization based on S1 behavior.

The only computed quantities were source-authenticated structural support and external metadata strata.

## Full-corpus support

The pinned corpus contains 79,881 case XML files. All 79,881 parsed under the frozen standalone transport with zero failures.

| quantity | result |
|---|---:|
| case files | 79,881 |
| parsed cases | 79,881 |
| parse failures | 0 |
| TEI body paragraphs | 89,933 |
| retained physical lines | 311,631 |
| retained Letter/Mark tokens | 1,110,748 |
| structurally S1-eligible paragraphs | 1,082 |
| cases with >=1 eligible paragraph | 1,050 |
| source volumes | 67 |
| source volumes with >=10 eligible paragraphs | 51 |
| hand-set strata | 44 |
| hand-set strata with >=20 eligible paragraphs | 4 |
| paragraphs with leading text before first `<lb/>` | 1,962 |
| opaque named-entity replacements | 0 |

All five predeclared admission conditions passed:

- all files parse: **PASS**
- >=100 eligible paragraphs: **PASS** (`1,082`)
- >=100 independent eligible cases: **PASS** (`1,050`)
- >=5 source volumes with >=10 eligible paragraphs: **PASS** (`51`)
- >=2 hand-set strata with >=20 eligible paragraphs: **PASS** (`4`)

Therefore `stage1_licensed = true`.

## Independent replication support

Practice-level eligible support:

- `forman`: 114 paragraphs
- `napier`: 968 paragraphs

Largest hand-set supports include:

- `#rnapier`: 866
- `#sforman`: 108
- `#srnapier`: 26
- `#gjames`: 24
- `#rwallis`: 17
- `#rruddle`: 13

Source-volume support is broad rather than concentrated in one notebook. Examples include:

- `Forman001`: 16
- `Forman002`: 18
- `Forman003`: 12
- `Forman004`: 22
- `Forman005`: 26
- `Forman006`: 12
- `Napier001`: 17
- `Napier002`: 32
- `Napier003`: 129
- `Napier004`: 20
- `Napier005`: 10

In total, 51 source volumes meet the predeclared >=10-eligible support threshold.

Consultation-class support is also not singular: `#horary` dominates (871), with `#diary` 46, `#nativity` 45, `#decumbiture` 35, `#prescription` 15, `#interrogation` 12, and `#interrogationTreatment` 10 among the larger strata.

## Decision

Casebooks passes the prospective support gate and is admitted to one-shot Stage1 R4 scoring under the already-frozen extraction.

Stage1 must not alter:

- the pinned Casebooks commit;
- `<text>/<body>//p` item boundaries;
- `<lb/>` physical lineation;
- diplomatic choice/translation/note handling;
- Letter/Mark tokenization;
- structural eligibility;
- source-volume, hand, practice, or consultation metadata definitions.

Stage1 may now introduce only the historical Phase62B/62C S1 scoring layer. Its primary interpretation must include replication across source volumes and the two major practices/hands rather than relying on a single pooled corpus mean.
