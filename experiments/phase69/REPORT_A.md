# Phase 69A — long-range near-family persistence beyond A1 direct memory

Status: **CLOSED — A1 LONG-RANGE UNDERPREDICTION / PERSISTENT STATE REQUIRED**

## Question

The A1 line is one of the strongest surviving formal models in the repository: paragraph-entry behavior plus non-identical edit-distance-1 family reuse from the previous ten tokens explains several local recurrence properties on held-out physical leaves.

Phase69A asked whether that frozen mechanism also accounts for same-leaf recurrence much farther away than its direct memory:

- 41–80 tokens back;
- 81–160 tokens back;
- 161–320 tokens back.

The primary object was a non-identical edit-distance-1 family, not exact token identity.

## Frozen design

- same five physical-leaf folds as Phase61/62;
- frozen A1 parameters, no Phase69 fitting;
- training-vocabulary-only A1 generation;
- eligible held-out physical leaves required at least 321 tokens;
- token sequences continue across paragraph/page-side boundaries on the same physical leaf;
- each dataset compared against 40 within-leaf token-order shuffles, preserving leaf token multiset and length;
- bin excess = observed recurrence rate minus median shuffled recurrence rate;
- `E_long` = sum of the three bin excesses;
- 50 A1 predictive realization indices, each aggregated across all five held-out folds;
- frozen one-sided test asks whether real Voynich has more long-range family recurrence than A1 predicts.

All five target folds contained eligible long-range leaves.

## Primary edit1-family result

The manuscript and A1 both have **negative** long-range excess relative to within-leaf shuffled order. The result is therefore not "Voynich shows positive long-range clustering."

The model failure is comparative:

- Voynich mean `E_long` = **-0.02892**
- A1 predictive mean `E_long` = **-0.11839**
- difference `Voynich - A1` = **+0.08947**
- one-sided predictive p = **0.01961**

All 50 frozen A1 predictive realizations were below the real Voynich mean; the plus-one predictive p-value is therefore `1/51`.

A1 95% predictive range for `E_long` was approximately:

- 2.5%: **-0.12904**
- 97.5%: **-0.10774**

The real manuscript lies far above this distribution.

### Where the mismatch grows

Mean signed excess by distance bin:

| distance | Voynich | A1 |
|---|---:|---:|
| 41–80 | -0.00227 | -0.02027 |
| 81–160 | -0.01465 | -0.03732 |
| 161–320 | -0.01201 | -0.06079 |

The A1 deficit grows with distance, especially at 161–320 tokens.

This is consistent with A1 concentrating related variants too strongly in the immediate local neighborhood. The real manuscript still suppresses far-range family recurrence relative to a shuffled leaf, but **far less strongly** than A1 does. In practical terms, related token families return at long distances more often than the frozen ten-token model predicts.

The five held-out Voynich fold `E_long` values were:

- fold 0: -0.02128
- fold 1: -0.04021
- fold 2: -0.06300
- fold 3: +0.00428
- fold 4: -0.02441

The result is therefore not a claim that every fold has positive long-range clustering. The scientific statement is the predictive mismatch against the frozen A1 distribution.

## Exact-token sensitivity

The same analysis using exact token identity gives almost perfect A1 agreement:

- Voynich mean `E_long` = **-0.08225**
- A1 mean `E_long` = **-0.08220**
- difference = **-0.00005**
- one-sided p = **0.50980**

This is the most informative contrast in Phase69A.

A1 is not simply wrong about all long-distance repetition. It reproduces long-range **exact-token repetition**, while underpredicting long-range return of **one-edit morphological families**.

## Decision

Under the frozen Phase69A rule, classify:

> **A1 LONG-RANGE UNDERPREDICTION — PERSISTENT STATE REQUIRED**

"Persistent state" here means only that the current bounded ten-token family mechanism is missing a process that keeps or reactivates token-family information over longer spans on the same physical leaf.

The result does not identify the state. Plausible classes include:

- semantic/topic or recipe/component persistence;
- cipher-key / encoding-state persistence;
- scribal or orthographic state;
- a longer-lived formal family-return mechanism with no semantic content.

The exact-token control argues that the missing process acts on **families/variants**, rather than merely increasing literal word repetition.

## Next falsification

The next test should locate the missing state in the document hierarchy before adding a new generator.

The immediate prospective question is:

> Is the long-range family mismatch specifically carried **across paragraph boundaries**?

If yes, the missing state survives paragraph transitions and A2 should contain an explicit persistent leaf-level state/cache. If the mismatch is only within paragraphs, the next model should instead refine paragraph-internal organization.

## Provenance

Successful predictive run:

- GitHub Actions run: `33384824865`
- scientific head: `15a578190e31d43412346d21427f0a99620d603d`
- artifact: `phase69a-result`, ID `9755221510`
- artifact SHA-256: `fa505774f2c710e4bcba700a9297dfa65fb72cad3d23c0659344972194002dc2`
- ZL3b blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

The executable was optimized before the Phase69 result was observed by reusing an exactly equivalent training-vocabulary edit1 graph for generated subsets and combining edit1/exact rolling passes. The frozen statistic, source, bins, null, A1 parameters, seeds, predictive count, and decision rule were unchanged.
