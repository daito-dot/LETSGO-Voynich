# Phase 71A — Alberti message-initial boundary mechanism

Status: **CLOSED — P71-AB1 BOUNDARY-SIGNAL NOT SUPPORTED**

## Question

Phase70 left one conspicuous formal component unresolved: exactly recoverable meaningful plaintext could reproduce much of the Voynich short-range recurrence and aggregate line-position regime under a frozen A1 local selector, but paragraph-entry S1 remained only about 15% of the Voynich target.

Phase71 therefore did not tune Phase70. It tested a separately motivated, historically grounded mechanism:

> Can Alberti's attested message-initial alignment signal + cipher-disk reset, if applied at paragraph boundaries, generate the Voynich paragraph-entry direction in meaningful ciphertext?

This is a mechanism-control experiment, not a claim that the Voynich manuscript used Alberti's disk.

## Frozen construction

The source mechanism is Alberti's first disk method: a capital ciphertext signal identifies the current disk alignment, with alphabet changes signaled again after three or four words.

Frozen example rings:

- stationary: `ABCDEFGILMNOPQRSTVXZ1234`
- movable: `gklnprtuz&xysomqihfdbace`
- movable index: `k`

The primary comparison used the historically attested **4-word** change interval.

- `CONT`: each Latin manuscript is one continuous cipher message; paragraph boundaries have no cryptographic effect.
- `PARA`: every pilcrow paragraph begins a fresh message alignment/reset; otherwise the cipher is the same.

To avoid inventing a one-character word, the capital alignment signal is prefixed to the following encrypted word inside the same token. Paired arms therefore have exactly the same retained plaintext words, line/paragraph layout and output token counts.

The exact four-manuscript CREMMA Latin panel and the frozen Phase62/63 S1 target machinery were reused. S1 was primary; S2/S3/H62 were descriptive and could not rescue a failed S1 result.

## Preflight

The no-score preflight passed before the scientific reveal:

- exact ZL3b and CREMMA authorities verified;
- exact 24/24 rings and all one-to-one alignments verified;
- deterministic indicator/ciphertext generation verified;
- paired plaintext hashes and token counts identical;
- `PARA` had one initial signal/reset per nonempty source paragraph;
- `CONT` had one initial signal per manuscript and zero paragraph resets;
- explicit marker: `NO PHASE71 SCIENTIFIC SCORE COMPUTED`.

Preflight run `33388801448`, job `99477392244`.

## Primary result — 4-word Alberti interval

Frozen classification:

> **P71-AB1 BOUNDARY-SIGNAL NOT SUPPORTED**

The result is not merely weak. It points in the **opposite S1 direction** from Voynich.

| arm | S1 / Voynich | S2 / Voynich | S3 / Voynich |
|---|---:|---:|---:|
| `CONT` | **-0.871×** | 0.277× | 0.911× |
| `PARA` | **-0.952×** | 0.291× | 0.878× |

`PARA` S1 projections in the five frozen target folds were:

- -0.82748
- -0.86606
- -0.82557
- -0.80840
- -0.84288

Therefore:

- positive S1 folds: **0/5**;
- frozen `[0.5, 2.0]` S1 regime: **fail**;
- `PARA` closer to the Voynich target than `CONT`: **no**;
- `PARA > CONT`: **no**.

The paragraph reset/signal bundle actually makes the primary S1 ratio modestly **more negative**, from `-0.871×` to `-0.952×`.

## Descriptive formal channels

The negative S1 result is more informative because some easier formal summaries are not catastrophically far away.

H62-P1:

| arm | mean D_profile | median D_profile | mean |ΔC_short| |
|---|---:|---:|---:|
| `CONT` | 1.00564 | 0.86834 | **0.12273** |
| `PARA` | 1.01014 | **0.82699** | 0.18144 |

S3 is also relatively close to the Voynich scalar (`0.91×` / `0.88×`).

This reproduces an important pattern from earlier phases: aggregate line-position and some recurrence summaries are relatively easy for disparate structured systems to approach, whereas the **signed paragraph-entry transition** is harder to reproduce.

## Predeclared 3-word sensitivity

Alberti explicitly allows changing the alphabet after three or four words, so 3 words was frozen as a non-rescuing sensitivity.

| arm | S1 / Voynich | S2 / Voynich | S3 / Voynich |
|---|---:|---:|---:|
| `CONT` | -1.199× | 0.197× | 0.937× |
| `PARA` | -1.144× | 0.128× | 0.841× |

Here `PARA` is slightly less negative than `CONT`, so the internal directional comparison is better. But:

- `PARA` remains negative in **5/5** folds;
- its S1 ratio is `-1.144×`;
- it fails the frozen primary regime decisively;
- the sensitivity was explicitly forbidden from rescuing the 4-word primary.

It therefore does not change the scientific classification.

## Interpretation

The exact Alberti-style message-boundary hypothesis is rejected under the frozen test:

> **A historically attested initial alignment signal and disk reset is not sufficient, in this direct construction, to explain the Voynich paragraph-entry direction.**

This result sharpens the mechanistic picture after Phase70.

1. **Short-range near-family recurrence is comparatively easy to manufacture over meaningful plaintext.** Phase69/70 demonstrated this directly.
2. **Aggregate line-position structure is also relatively non-specific.** Even this Alberti control reaches roughly 0.88–0.94× on S3.
3. **Voynich paragraph-entry S1 remains unusually selective.** The Alberti boundary mechanism does not merely undershoot it; it consistently projects in the opposite direction.

So the current evidence no longer supports treating all of A1 as one indivisible signature. The local recurrence component can coexist with meaningful plaintext, while the entry component still requires a different explanation.

## Blinded routing

`DECISION_A_BLIND.md` was frozen after the successful no-score preflight and before any Phase71 score.

Route N therefore controls:

- no search over nearby reset intervals;
- no alternate signal tokenization;
- no plaintext-projection repair;
- no Alberti null/numeral/nomenclator additions;
- no post-hoc alphabet or paragraph/message remapping.

The next experiment must change mechanism family or use a genuinely independent external/content discriminator.

## Claim boundary

Phase71 does **not** show that:

- all historical ciphers fail;
- meaningful plaintext is impossible;
- Alberti's cipher is generally unlike Voynich in every respect;
- Voynich paragraphs cannot have functional boundaries;
- the manuscript is meaningless.

It rejects one explicit historically grounded boundary mechanism under one prospectively frozen S1 test.

## Provenance

- scientific head: `edfccb25a3a4241ae72595ed411c0bc179deed5a`
- Actions run: `33388952000`
- job: `99477868519`
- artifact: `phase71a-first-reveal`, ID `9756744780`
- artifact ZIP SHA-256: `41baa98522ca5707294ad81b2e18d63d2bb6629857ece4bb396cc44ddfc49e7d`
- raw result SHA-256: `ac80ad575f20c769bb989a27693402855129cbc3263fb57dfd8b826b4e47f1fc`
- `PLAN_A.md` SHA-256: `e3fe1580737fb67072a9e2c321421c7b735b070749ff2ab376083b65055e3083`
- `DECISION_A_BLIND.md` SHA-256: `d4921996a131d5cd502a6e44246b9168f2740cc990548909aa48fc6cbe4abd28`
- executable SHA-256: `9eca0459e868524499341159da963806f962c1c78eaf2f472dc6772fb9e23b42`
