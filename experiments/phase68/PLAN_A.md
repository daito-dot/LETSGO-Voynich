# Phase 68A — pharmaceutical Lf labels -> formal-residual local body text

Status: **FROZEN BEFORE LABEL↔BODY ASSOCIATION REVEAL**

Date: 2026-08-31

## Why this is the next content anchor

Phase67 closed repeated tests in which **coarse visual morphology** was the content anchor. Leaf/root morphology did not predict short labels, local paragraph character structure, A1-formal-residual character structure, or retained lexical-family selection.

That does not test the more direct lexical hypothesis:

> If a pharmaceutical `Lf` label functions like an ingredient/name identifier, does that label have a privileged lexical-family relation to the body paragraph objectively paired with the same illustration block?

This hypothesis does not require identifying the plant or deciding which visible morphology is semantically salient.

Earlier project work found no simple raw label↔body-row semantic pairing. Phase68A is a new mechanism-conditioned follow-up: the body side is prospectively restricted to the Phase67C `INNOVATION_RETAINED` tokens after the already-supported paragraph-entry and preceding-10 edit1-compatible channels are masked.

Because this test is adaptive to prior nulls, a positive result is a **candidate** only and requires independent replication on earlier pharmaceutical folios.

## Frozen block population

Reuse the objective Phase67 block mapping without modification:

- f99r: 4 blocks
- f99v: 3 blocks
- f100r: 2 blocks
- f100v: 1 descriptive-only block
- f102v2: 2 blocks
- f102v1: 2 blocks

The inferential statistic uses only folios with at least two blocks, because a one-block folio cannot participate in a within-folio reassignment. Therefore f100v is reported descriptively but contributes a constant/no information and is omitted from the inferential numerator.

Inferential blocks: **13** across f99r, f99v, f100r, f102v2, f102v1.

## Frozen transcription authority

Label strings are extracted mechanically at execution time from:

- repository: `Aspect-Research/voynich-autoexploration`
- commit: `31819c914061cc6b63bbf4983e33d643ede52e46`
- path: `data/transcriptions/eva_zl3b.txt`
- expected ZL3b file version header: `Version 3b of 13/05/2025`
- expected Git blob identity already used by this project: `2a4533ab9bdfa85db9bad602d590978953055df1`

Only the exact `Lf` loci already frozen in `../phase67/BLOCK_MANIFEST_A.json` are read. No label is selected or omitted based on a match result.

## Lf token extraction

For each frozen physical fragment object:

1. read all of that object's frozen `Lf` loci in locus order;
2. remove IVTFF locus metadata and leading Petersen/comment markers of the form `<!...>`;
3. treat `.`, `,`, whitespace and `<->` as token separators;
4. retain only complete lowercase alphabetic tokens matching `^[a-z]+$`;
5. discard a candidate token if it contains transcription/editorial uncertainty markup rather than resolving it;
6. for split/multi-locus labels, keep the valid visible token parts as a token list for the same physical object; do **not** concatenate them into a new invented string.

An object with no valid complete Lf token after this rule is unavailable but remains in the object manifest.

## Frozen body-side representation

Reuse the exact Phase67C formal mask on `../phase67/TEXT_TABLE_A.json`:

- conservative complete-token cleaning;
- paragraph line0 tokens masked as `ENTRY_MASKED`;
- for later lines, a token is `LOCAL_EDIT1_MASKED` if it is a non-identical edit-distance-1 neighbor of any previous ten cleaned tokens on the same physical folio;
- every cleaned token enters the ten-token history;
- all other tokens are `INNOVATION_RETAINED`.

Phase68A primary matching uses only `INNOVATION_RETAINED` body tokens.

## Primary relation

Use the same exact `lev1` relation as Phase61/67:

- equality is not edit1;
- one insertion, deletion, or substitution is edit1.

For every valid `Lf` token occurrence `l` in an inferential block, define a primary hit:

`hit(l, body) = 1` iff at least one retained body token `t` satisfies `(l == t) OR lev1(l, t)`.

This is a closed edit1 lexical-family hit; no edit-distance weight or threshold is fitted.

Primary block score:

`B_i = number of valid Lf token occurrences with a hit / number of valid Lf token occurrences`.

Primary global statistic:

`T = mean(B_i)` over inferential blocks that have at least one valid Lf token.

Blocks are weighted equally in the primary statistic so rows with many labels do not dominate.

## Exact null

Hold label tokens and body residual tokens fixed. Reassign complete body paragraphs among blocks **within the same folio**.

Exact space:

`4! * 3! * 2! * 2! * 2! = 1,152`.

(f100v has one block and does not contribute inferential information.)

Enumerate all 1,152 assignments, identity included.

Exact one-sided p-value:

`p = count(T_perm >= T_obs) / 1152`.

## Frozen detection gate

A result is retained as a candidate only if:

1. exact p <= 0.05;
2. at least 10 of the 13 inferential blocks contain at least one valid Lf token after conservative extraction;
3. at least 50 valid Lf token occurrences are included in total across inferential blocks.

A passing result is classified only:

`CANDIDATE Lf↔FORMAL-RESIDUAL BODY FAMILY RELATION — INDEPENDENT REPLICATION REQUIRED`.

## Frozen secondary diagnostics

These are reported but cannot rescue a failed primary test.

### S1 exact-only

Same block-balanced statistic, but a label token hits only an exactly identical retained body token.

### S2 all-clean-body closed edit1

Same primary closed-edit1 label relation, but compare labels to **all conservatively cleaned body tokens**, including entry and local-edit1-compatible tokens. This shows whether the formal mask removed a raw relation rather than revealing one.

### S3 pooled-label hit rate

Use the primary retained-body closed-edit1 relation but pool all valid label token occurrences rather than equal-weighting blocks.

## Interpretation limits

A positive Phase68A result would establish a local lexical-family relation between attached Lf labels and the objectively paired paragraph. It would **not** prove that the label is a plant name, identify a plaintext language, or show that the matching body token is semantically identical.

A null result would reject this direct local label-family model under the frozen pairing and formal mask. It would not reject nonlocal recipe reference, transformed label registers beyond edit1, or labels functioning as nonlexical identifiers.

No locus set, token cleaning, family radius, block weight, paragraph mapping, or statistic may be changed after reveal.
