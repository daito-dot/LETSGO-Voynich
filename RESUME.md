# RESUME — deterministic restart point

## Resume here — after Issue #72, Issue #75 Phases A–F0 and OGH-A

The latest completed scientific reveals are Issue #72 (Naibbe R1 causal decomposition, merged to `main`), Issue #75 Phases A–F0 (branch `issue75-minimal-occupancy-generator`, minimal occupancy generator ladder M0–M5, F0 architecture selection; M6 target reveal pending) and OGH-A (`experiments/occupancy-generation-hierarchy/`). Read, in order:

1. `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE72_RESULT.md`
2. GitHub Issue #75 and, on its branch, `experiments/minimal-occupancy-generator/REPORT_A.md` … `REPORT_F0.md`
3. `experiments/occupancy-generation-hierarchy/PLAN_A.md`
4. `experiments/occupancy-generation-hierarchy/REPORT_A.md`
5. `research/HYPOTHESIS_LEDGER_ADDENDUM_OGH_A.md`
6. `research/NEXT_RESEARCH_FRONTIER.md`

Frozen OGH-A state:

- classification `COMPACT CONSTRUCTION GRAMMAR SUFFICIENT` (Issue #68 gate), identical on ZL3b and IT2a skeletons;
- G4 last-occupied-slot successor grammar, 78 counted parameters: `r 0.917/0.933` (ZL3b arm), `0.908/0.933` (IT2a arm), signs `62–63/66`, `W≈0.97`, all `p=1/1001`;
- G5 pairwise maxent control `0.948–0.969`; G6 empirical ceiling `0.962–0.973`; G0–G3 fail;
- G4 is **not** within the Issue #75 M+-equivalence tolerance (`0.0098`; median gap `≈−0.06`); G5 is inside it on the ZL3b arm (`−0.001`) and marginally outside on the IT2a arm (`−0.012`). OGH-A's label is defined by the Issue #68 gate.

**Next scientific move:** integrate Issue #75 and OGH-A on `main`; then preregister one extension of the successor grammar (second-order successor context, or K/R/S-gated successor tables) chosen by training-only held-out likelihood, and score it under both the Issue #68 gate and the Issue #75 equivalence criterion. Carry the frozen G4 grammar into the next joint tournament as the emission-stage comparator.

**Do not:** select target edges to extend G4, promote G5/G6 as mechanisms, average ZL3b and IT2a, relabel a locally executed reveal as an Actions run (use `.github/workflows/ogh-a-replay.yml` to replay), or infer slot meanings.

Transcriptions are fetched and hash-verified with `data/fetch_transcriptions.py`.

Last consolidated: 2026-09-01

## Previous resume point — after Issue #68 first joint-constraint tournament


The latest completed scientific reveal is Issue #68. Read, in order:

1. `experiments/joint-constraint-tournament/REPORT_A.md`
2. `experiments/joint-constraint-tournament/first-reveal/PROVENANCE.md`
3. `experiments/joint-constraint-tournament/first-reveal/issue68_joint_tournament_results.json`
4. `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE68_RESULT.md`
5. `research/NEXT_RESEARCH_FRONTIER.md`

Frozen Issue #68 state:

- global: `NO TESTED FAMILY JOINT-CONSTRAINT COMPETITIVE`;
- Naibbe: R1 PASS / R2 FAIL / R3 FAIL / R4 FAIL / R5 PASS → `NOT COMPETITIVE`;
- A1: R1 common-representation gate FAIL, R2 PASS, R3 PASS, R5 PASS → `PARTIAL STRUCTURAL MODEL`; no real A1 R1 graph was computed;
- Naibbe R1 vs ZL3b `r=.8830`, vs IT2a `r=.9001`, sign agreement `60/66` and `61/66`, all topology maxT p-values `1/1001`;
- scientific first execution was run `33456282445` / job `99696811349`; result bytes were deterministically recovered after a stdout-framing transport failure. Do not relabel the recovery run as the first reveal.

**Next scientific move:** first integrate/verify Issue #68 on main. Then open a fresh preregistered codebook/process-decomposition issue from post-merge main. Ask whether Naibbe's R1 success survives codebook-association and inventory controls while the encryption architecture is held fixed.

**Do not:** lower the 60% parser gate, remap A1 after its failure, select favorable Naibbe realizations/views, add locality/paragraph-entry repairs to Naibbe, or use individual R1 edges to design the next control.

Last consolidated: 2026-09-01

Do not reconstruct the project from old chat when GitHub contains a newer state.

## First sentence a future agent should be able to say

> We are studying how one **space-delimited Voynich token** is internally assembled, not whole-sentence grammar. The non-trivial token-construction signature survives lower-order controls and an independent Takahashi/IT2a reading: the full ZL3b↔IT2a residual graph correlates `0.98845` with `65/66` signs agreeing. The next research job is no longer another local occupancy discovery; it is to use this replicated constraint together with H62 recurrence and S1 paragraph-entry specialization to discriminate prospectively defined reversible/generative mechanisms.

Visible spaces are not assumed to be proven linguistic word boundaries.

## Read in this order

1. `README.md`
2. `research/RESEARCH_OBJECTIVE.md`
3. `research/TOKEN_CONSTRUCTION_PROGRAM.md`
4. `research/STATUS.md`
5. `ROADMAP.md`
6. `research/NEXT_RESEARCH_FRONTIER.md`
7. `research/hypothesis-ledger.md`
8. `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE55.md`
9. `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE58.md`
10. `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE62.md`
11. `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE64.md`
12. `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE66.md`
13. `experiments/slot35-dependency/REPORT_B.md`
14. `experiments/occupancy-graph/REPORT_A.md`
15. `experiments/occupancy-graph-stability/REPORT_A.md`
16. `experiments/occupancy-graph-residual/REPORT_A.md`
17. `experiments/occupancy-graph-independent-transcription/SOURCE_AUDIT_PLAN.md`
18. `experiments/occupancy-graph-independent-transcription/source-audit/SOURCE_AUDIT_REPORT.md`
19. `experiments/occupancy-graph-independent-transcription/PLAN_A.md`
20. `experiments/occupancy-graph-independent-transcription/REPORT_A.md`
21. `experiments/occupancy-graph-independent-transcription/first-reveal/PROVENANCE.md`
22. exact source/executable files before changing any numerical interpretation.

## Authority hierarchy

1. phase/issue-specific frozen plan, exact first-reveal artifact and report control historical method/numbers;
2. `research/STATUS.md` controls current accepted interpretation;
3. `research/TOKEN_CONSTRUCTION_PROGRAM.md` controls the purpose/object of the token-construction lane;
4. hypothesis ledgers control hypothesis status/history;
5. reproducibility audits control exact-replay claims;
6. `ROADMAP.md` and `research/NEXT_RESEARCH_FRONTIER.md` control current sequencing;
7. old chat/memory is non-authoritative where repository evidence conflicts.

## Current accepted state

The manuscript is not deciphered.

A1/A1-R1 remains the leading tested mechanism for short-range near-family recurrence geometry. Phase69/70 showed comparable recurrence can coexist with exactly recoverable meaningful plaintext, so recurrence is a surface constraint rather than evidence of semantic absence.

S1 paragraph-entry specialization remains a harder discriminator. Phase71's tested Alberti initial-signal/reset mechanism failed in the opposite S1 direction.

The bounded direct-music program in Issue #26 is closed with no supported tested direct-musical interpretation.

## Token-construction history

### #55

#55A found slot3×slot5 dependence; #55B reduced it almost entirely to binary occupancy exclusion.

> `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`

### #58A

The selection-aware complete 66-edge audit showed a broad signed occupancy network rather than a unique slot3×slot5 key.

> `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`

First-reveal raw SHA-256:

`ae0db7dc72cb890a325ef5313a3375a43efde7c27c9bd5b3fcb0632fb808e152`

### #58B / Issue #62

Raw graph stability across Currier/section/line-position was inconclusive because the line-local marginal-preserving null itself produced whole-graph correlations near `0.95`.

> `CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`

> `LINE-POSITION GRAPH STABILITY INCONCLUSIVE`

First-reveal raw SHA-256:

`45024fd1d15b2d2484ffc26657ccc8007fd6a04dc3ed1b53b243f77ba455f8a0`

### #58C / Issue #64

#58C calibrated all 66 conditional edges against an independently split line-local null baseline.

> **`RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`**

ZL3b pooled:

- E `3.23155`;
- test-null max `1.28318`;
- p `1/1001`;
- W `0.94471`.

All seven strata contained residual structure. The three Currier-B section comparisons and interior/final were stable; Currier A/B and line-initial comparisons were related but modulated; no contrast was materially different.

First-reveal raw SHA-256:

`fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`

### #58D / Issue #66

#58D challenged #58C with the independent Takeshi Takahashi / IT2a `EvaT` reading under a strict source/population firewall.

Stage A:

- live source exactly matches the historical Phase63B IT2a bytes;
- 99/99 #58C physical leaves;
- 34,411 clean tokens;
- 28,280 unchanged-parser accepted tokens;
- coverage `82.18%`;
- no pair/residual target metric computed before authorization.

Frozen first-reveal classification:

> **`INDEPENDENT TRANSCRIPTION REPLICATES RESIDUAL TOKEN-CONSTRUCTION CORE`**

Independent IT residual existence:

- `E_IT_ALL = 3.21363`;
- test-null max `1.25891`;
- `p_exist_IT = 1/1001`;
- `W_IT_ALL = 0.95377`.

Complete ZL3b↔IT2a 66-edge topology:

- pooled Pearson `0.988448`;
- pooled sign agreement `65/66`;
- both maxT p-values `1/1001`.

All eight planned groups meet the strong frozen replication class:

- Pearson `0.97031–0.99548`;
- sign agreement `64/66–66/66`;
- all maxT p-values `1/1001`.

Within IT2a, family results again are:

> `REGISTER/SECTION RESIDUAL MODULATION`

> `LINE-POSITION RESIDUAL MODULATION`

All 7/7 contrasts are stable or related/modulated; none is different.

Secondary stable-vs-modulated ordering did **not** pass its frozen threshold (`p_Delta=.08791`). Retain that non-pass.

Correct current interpretation:

> **Within a common EVA/IVTFF framework, a manuscript-level token-internal construction signature survives independent ZL3b and Takahashi/IT2a readings. The broad residual core is shared with stratum modulation, not exact universal invariance.**

#58D first-reveal raw SHA-256:

`f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6`

First-reveal authority:

- exact scientific head `37d9dd1f378a6230a11fbe7694c53eeb8b30f81f`;
- run `33449726473`;
- job `99676742936`;
- artifact `9779393199`;
- ZIP SHA-256 `d78a4355510844dc1ea32fed9c581676ba0c9fd97092e34766f4a2bfbb334577`.

The target workflow is guarded to that exact first-reveal head. Later documentation commits do not redefine the first reveal.

## Archive integrity note

During #58D preflight, the later text-transport copy of the #58C first reveal was found to contain one corrupt base64 chunk (`part06`). The original #58C Actions artifact remained intact and matched every frozen authority hash. Only the repository transport copy was replaced from the verified original; the #58C scientific result did not change.

See:

`experiments/occupancy-graph-residual/first-reveal/ARCHIVE_REPAIR_20260901.md`.

## Current frontier

When asked simply to continue:

1. verify current main, PRs/issues and active branch before acting;
2. if #58D is not yet integrated, finish report/accepted-state updates, exact-head checks and merge it first;
3. do **not** rerun ZL3b/IT2a token-graph discovery as the main frontier;
4. start a new plan-first joint-constraint mechanism tournament from post-#58D main;
5. freeze the **constraint battery before candidate scoring**;
6. at minimum retain independent responsibilities for:
   - cross-reading replicated residual token construction;
   - H62 near-family recurrence geometry;
   - signed S1 paragraph-entry specialization;
   - reversibility/recoverability when claimed;
   - model complexity / degrees of freedom;
7. freeze a small set of architecturally distinct candidate families before seeing tournament outcomes;
8. retain baseline anchors so apparent gains are interpretable;
9. avoid one weighted omnibus score that lets easy structure hide S1 sign failure;
10. classify candidates as surface generators, reversible decoder candidates, or controls;
11. preserve partial/failing results without adding post-reveal repair terms inside the same confirmatory phase.

## Scientific purpose of the next frontier

The project now has a structural constraint strong enough to reject models prospectively.

The question becomes:

> **Can a bounded reversible/generative mechanism jointly satisfy the strongest established Voynich responsibilities on held-out material?**

If one reversible family does, it becomes a serious inverse/decoding candidate and should face stronger unseen prediction and decode/re-encode closure tests.

If non-reversible generators pass but reversible models fail, that informs surface-production architecture but is not decipherment.

If all bounded candidates fail, use the pattern of failures to motivate a genuinely new architecture under a new preregistration rather than a universal repair model.

## Stop rules

Do not:

- assume visible spaces are proven word boundaries;
- drift from token-internal construction into sentence syntax without a new explicit program;
- reinterpret #58D as semantic/plaintext evidence;
- claim exact universal grammar when modulation remains supported;
- select individual saturated edges as fresh confirmatory targets;
- call a non-reversible generator a decoder;
- hide S1 sign failure in an omnibus average;
- tune candidate mechanisms after held-out failures and call the same test confirmatory;
- give candidates undeclared access to held-out layout or target statistics;
- ignore model complexity;
- describe structural fit as decipherment;
- merge diverged historical research branches wholesale when provenance-preserving selective integration is possible.

## Parallel lanes

A GC2a/v101 alphabet-level robustness challenge remains scientifically useful but is secondary after the strong IT2a reading-lineage replication. It requires a separately frozen coarser invariant rather than an outcome-tuned v101→EVA mapping.

Historical real-cipher controls remain source-only until genuine message-entry boundaries are externally fixed. Do not use physical page starts as a post-hoc substitute for historical message starts.