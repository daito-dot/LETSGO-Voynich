# Phase 68A — pharmaceutical Lf labels -> formal-residual local body text

Status: **CLOSED — NOT SUPPORTED**

## Question

After Phase67 repeatedly failed to connect coarse leaf/root image morphology to the objectively paired local body paragraph, Phase68A changed the content anchor from image traits to the attached pharmaceutical `Lf` label itself.

The test asked:

> If an `Lf` token is an ingredient/name-like identifier, is it unusually likely to occur in the paired body paragraph either exactly or within one edit, after masking the already-established paragraph-entry and preceding-10 edit1-compatible formal channels?

## Frozen design

- Same objective Quire 19 illustration→paragraph blocks as Phase67.
- 13 inferential blocks across f99r, f99v, f100r, f102v2, f102v1; f100v has only one block and is descriptive only.
- 93 valid conservatively extracted `Lf` token occurrences.
- ZL3b source was pinned and verified at Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`.
- Body side used the Phase67C `INNOVATION_RETAINED` tokens only.
- Primary relation: label token equals a retained body token or is Levenshtein distance exactly 1 from it.
- Primary statistic: mean per-block label hit fraction, so blocks with many labels do not dominate.
- Exact null: all 1,152 within-folio paragraph assignments, identity included.
- Coverage gate was passed.

## Primary result

Observed block-balanced hit fraction:

- observed = **0.16445**
- null mean = **0.15368**
- null 95th percentile = **0.20291**
- exact p = **0.38889** (448 / 1,152 assignments at least as large)

The correct local label→paragraph pairing is therefore not privileged under the frozen closed-edit1 family relation.

## Frozen secondary checks

### Exact label identity only

- observed = 0.01099
- null mean = 0.01991
- exact p = **0.80556**

Exact repeats are if anything less common than the within-folio null expectation, but not significantly so.

### All cleaned body tokens, before formal masking

- observed = 0.23442
- null mean = 0.20992
- exact p = **0.15625**

The formal mask did not erase a clearly positive raw label↔body relation.

### Pooled labels instead of equal block weighting

- observed = 0.18280
- null mean = 0.16846
- exact p = **0.36458**

Rows with many labels do not reveal a hidden effect.

## Decision

Phase68A is classified:

> **NOT SUPPORTED**

For these objectively paired Quire 19 pharmaceutical blocks, attached `Lf` labels are not measurably closer to their own local body paragraph than to another paragraph on the same folio under either exact identity or the established one-edit lexical-family relation.

This closes a fairly direct local lexical model:

- the image traits do not map simply to the short attached label;
- the same image traits do not map simply to the local running paragraph;
- filtering the paragraph through the current A1 formal model does not reveal that relation;
- the attached `Lf` label itself still does not become preferentially linked to its paired local paragraph.

The result does **not** show that labels are meaningless. It instead argues against treating the immediately adjacent paragraph as a straightforward lexical expansion of the attached label. A label may index a recipe component, object class, operation, or reference whose relevant text is nonlocal or transformed more strongly than one edit.

## Provenance

- GitHub Actions run: `33384164203`
- job: `99462906752`
- scientific head: `ec25e5fadb4fa1d40a7aca6c58682dc7f0772122`
- artifact ID: `9754901831`
- artifact SHA-256: `b6066bbab02465edb4d884399e888190985459365a30b5bcdafb785f8c0923aa`
