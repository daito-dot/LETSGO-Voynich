# Issue #211 — Bacon biliteral replacement preflight

Parent: #172  
Candidate: `B1623-BL0`  
Target score: **none**

## Decision

Historical core: **`H0_ARCHITECTURE_RECOVERED`**  
External round-trip: **PASS**  
Target adapter: **`HISTORICAL_CORE_ONLY_TARGET_ADAPTER_UNDERSPECIFIED`**

The stop rule applies. `B1623-BL0` will not be exposed to the Voynich R1–R10 battery under the current roadmap.

## What is fully specified historically

Bacon's biliteral mechanism is unusually clean compared with the failed TP1518 full-table admission.

The 24 plaintext classes are encoded by unique five-position strings over two states, conventionally `a` and `b`:

`A B C D E F G H I/J K L M N O P Q R S T U/V W X Y Z`.

The exact frozen serialization is `bacon_biliteral_table.txt`:

- 24 codewords;
- 5 binary positions per class;
- 192 UTF-8 bytes;
- SHA-256 `191bdb4787baa75011634085700b2e216d234d6ff732f48683d836ef698fdf7a`.

A synchronized decoder groups the interior stream into blocks of five and performs an exact inverse on the 24 classes. `I/J` and `U/V` are not separated by the code itself. Hidden lexical spaces and punctuation are also not carried by the five-position table.

Historical authorities used here:

1. Francis Bacon, *De dignitate et augmentis scientiarum*, London 1623; BHL DOI `10.5962/bhl.title.39021`, Internet Archive witness `operafrancisciba00baco`;
2. Gilbert Wats's 1640 English translation, Book VI chapter 1, which states the five-place/two-state construction and the bi-formed exterior carrier;
3. John Falconer, *Cryptomenysis Patefacta* (1685), pinned public transcription `uwgraphics/VEP2_TCP_SimpleText@7f17f7ab87560c8ea24a82d35789a11fd7e03e53`, `A4/A40781.txt`, which independently reproduces the 24-entry table and operational carrier rule.

No Voynich material was used to choose or repair the table.

## External-only H1

Frozen input:

`BACON`

Encoding:

`B=aaaab`  
`A=aaaaa`  
`C=aaaba`  
`O=abbab`  
`N=abbaa`

Therefore:

`BACON -> aaaab aaaaa aaaba abbab abbaa -> BACON`

The round-trip is exact because this input avoids the merged `I/J` and `U/V` classes.

## Why this still does not produce a #172 candidate surface

Bacon separates the secret binary stream from the visible carrier.

The historically visible construction is an **exterior carrier** whose positions have two distinguishable forms. The form class carries `a` versus `b`; the underlying carrier letters/objects can otherwise be chosen to express an independent overt message. Bacon's mechanism therefore specifies the hidden bit channel very strongly while leaving the overt surface channel intentionally broad.

That distinction is fatal for the current candidate admission question.

### Bare `a/b` stream

We could print the analytical interior states literally as `a` and `b`, but that is not the historical bi-formed carrier. More importantly, the five-bit letter groups are decoder segmentation, not necessarily visible source-space boundaries.

Turning every five bits into a visible Voynich-like token would therefore add an analyst-imposed boundary system. R1 in the frozen #172 plan is explicitly a **candidate-visible-boundary** responsibility.

### Historical bi-formed carrier

Using the actual carrier architecture avoids that problem only by opening a larger one: the carrier content is not determined by the cipher.

To obtain a Voynich surface we would have to decide, independently of Bacon's bit code:

- which exterior base glyph/token identities to emit;
- which visible spaces and token lengths to use;
- line and paragraph organization;
- which exterior forms are the `a` class and which are the `b` class;
- how those forms map to Basic-EVA or another frozen target representation.

If any of those choices are learned from Voynich, the candidate becomes a new target-derived surface generator wrapped around a historical binary code. If arbitrary carrier prose is allowed, almost all R1–R8 structure can come from the carrier rather than from the biliteral mechanism.

That is precisely the kind of hidden flexibility R10 is intended to expose.

## Score-free contract check

The frozen `FIRST_REVEAL_TARGET_PLAN.md` requires an immutable candidate surface/hierarchy:

- R1 uses candidate-visible spaces;
- R2 tests candidate token-internal construction under the frozen representation;
- R5–R8 operate on a fixed candidate line/item/paragraph hierarchy rather than a carrier selected after target inspection.

`B1623-BL0` alone does not determine those properties.

A valid adapter would therefore require an additional, independently specified historical or mathematical surface mechanism. None is supplied by Bacon's biliteral core or by the prospective evidence that selected this fallback.

## R10 consequence

The small biliteral table costs 1,536 bits under the frozen literal serialization, but that is not the main complexity.

A carrier-based tournament entry would also have to charge and freeze before target reveal:

- the complete exterior carrier or an independently specified carrier generator;
- the two-form exterior alphabet/classifier;
- five-position synchronization;
- carrier boundary/line/paragraph layout;
- any mapping into the target atom representation.

The unconstrained carrier is a high-capacity side channel, not free decoration.

## Program consequence

Bacon is useful for a narrower statement:

> A historically documented early-modern mechanism can carry an exactly recoverable 24-class hidden letter stream through an arbitrary two-form exterior channel at five carrier positions per hidden letter.

It does **not** independently predict the Voynich bounded-token, line, paragraph, recurrence, or inventory surface architecture.

Accordingly:

- retain `B1623-BL0` as a clean historical reversibility/steganography control;
- do not search Voynich for a favorable `a/b` partition;
- do not choose a carrier from target resemblance;
- do not score it in the new #172 joint tournament;
- after this clean fallback fails target-adapter admission, prefer a **no-new-entrant Priority-5 closeout** over continued historical candidate fishing.
