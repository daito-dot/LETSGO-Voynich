# Issue #123 L2 first-reveal provenance

Date: 2026-09-06
Parent: Issue #88 / Issue #118 / Issue #121
Status: **AUTHORITATIVE FIRST REVEAL**

## Frozen scientific head

`87aee03e60e2eab72987eb0cc2bf8c4b992632a0`

No L2 `G_line`, `G_beyond_line`, mixture result or L2 state diagnostic was inspected before PR #124 was opened at this head.

## Workflow authority

- workflow: `Issue123 source-line reset L2 first reveal`
- run: `34027611090`
- conclusion: **SUCCESS**
- artifact: `9987613395`
- artifact ZIP digest: `sha256:0e84611da8fb29810a61b25d48f6cc791e5ee39377e3b08de86fa7dc1128b80b`
- result JSON SHA-256: `dfdfca650a15f1d47bd7124898bc8483a139ce47bb17a2c2802a0d2e946dea55`

## Embedded authorities

The L2 run reproduced:

- corrected B3 normalized authority SHA-256 `0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`;
- exact Issue #121 RESET2↔LEAFCONT2 outer-fold `G_edge` values;
- exact Issue #121 RESET2 and LEAFCONT2 inner-selected mixture weights.

Thus L2 changes only the prospectively inserted source-line reset topology.

## Frozen comparison

All three byte experts use exactly `k=2`, `alpha=.01`:

- `RESET2`: reset history before every visible token;
- `LINECONT2`: carry history across visible spaces within the same source line, reset at each source-line start;
- `LEAFCONT2`: carry history across source-line breaks within a physical leaf.

Each is mixed separately with the same corrected B3 probabilities using `w=0.00..1.00`, selected by pooled inner accepted-token likelihood only, ties to smaller `w`.

## Authoritative result

Frozen classification:

> **LINE-LOCAL CONTEXT CAPTURES RESIDUAL; NO ROBUST BEYOND-LINE GAIN**

### Within-line gain

`G_line = bits(MIX_RESET2) - bits(MIX_LINECONT2)`:

- fold0 `+0.03339038902518254`
- fold1 `+0.02093212050888482`
- fold2 `+0.03017008407788957`
- fold3 `+0.02839973265948892`
- fold4 `+0.03291474485290813`
- mean `+0.029161414224870796 bit/token`
- positive folds `5/5`
- frozen gate: **PASS**

### Beyond-line incremental gain

`G_beyond_line = bits(MIX_LINECONT2) - bits(MIX_LEAFCONT2)`:

- fold0 `-0.01945112606506072`
- fold1 `-0.012817079713640211`
- fold2 `-0.02086966174292293`
- fold3 `-0.017533945725512368`
- fold4 `-0.021974106211112954`
- mean `-0.018529183891649835 bit/token`
- positive folds `0/5`
- frozen gate: **FAIL**

The sign is stronger than simple non-significance: carrying this fixed byte context across source-line breaks is worse than resetting at the line boundary in every outer fold.

### Mean code lengths

- B3 `9.517268842963203`
- MIX_RESET2 `9.497295653343732`
- MIX_LINECONT2 `9.468134239118863`
- MIX_LEAFCONT2 `9.486663423010512`

### Inner-selected mixture weights

- RESET2: `.04` in all five folds;
- LINECONT2: `.15,.16,.15,.15,.15`;
- LEAFCONT2: `.08,.08,.09,.08,.09`.

The larger LINECONT2 weights are descriptive consequences of inner-fold likelihood selection, not outer-result tuning.

## Predeclared diagnostics

RESET2→LINECONT2 contribution is positive across all reported observable line-position strata:

- paragraph BODY: mean `+0.02755258717573894`, n=20,677;
- paragraph ENTRY: mean `+0.036467588418388736`, n=4,394;
- line FIRST: `+0.036467588418388736`;
- line MIDDLE: `+0.02516817814082239`;
- line FINAL: `+0.04069650116915924`.

LINECONT2→LEAFCONT2 contribution is negative across every reported stratum:

- paragraph BODY: mean `-0.018866709979791802`;
- paragraph ENTRY: mean `-0.017138389898774337`;
- line FIRST: `-0.017138389898774337`;
- line MIDDLE: `-0.016890417470250163`;
- line FINAL: `-0.029760905728452525`.

These diagnostics are consistent with the primary topology result and show that the line-reset advantage is not driven by one reported line-position stratum.

## Interpretation boundary

Supported statement:

> Under the fixed k=2 byte representation, the remaining immediate raw-surface predictive information beyond corrected B3 is prospectively localized to adjacent visible construction units within the same source line. Extending that same byte history across a source-line break does not add information and is predictively harmful on average in all five outer folds.

This does **not** establish that a manuscript line is a sentence, semantic unit or historical algorithmic state. It does not identify language, plaintext, cipher family, author, hoax status or latent semantics.

The result instead narrows the residual to a line-local adjacency mechanism. Before any latent-state model is interpreted, the next high-value test is to ask whether a compact explicit boundary-edge observable — principally previous-token terminal byte to next-token initial byte — absorbs this line-local gain, and/or whether its strength transports across already-authorized Currier regimes.
