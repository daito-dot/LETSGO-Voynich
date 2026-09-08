# Issue #194 — Ramanacoil Gate 0 outcome

Date: 2026-09-08  
Parent: #172  
PR: #195

## Frozen classification

**`NON_COMPOSABLE_OTHER`**

`stage1_licensed = false`.

No R5 score, transition likelihood, Voynich statistic, candidate score, or effect direction was computed.

## First-reveal authority

- exact tested head: `843045d51de67a51310371255f3675349102e29d`
- Actions run: `34176454461`
- job: `101906717685`
- conclusion: `success`
- artifact: `issue194-ramanacoil-gate0`
- artifact ID: `10037409330`
- artifact ZIP SHA-256: `ad960323edc631c20a7174b758079f0b16219f25b4ea6e9b13c098f3f951792d`
- raw `issue194_gate0_results.json` SHA-256: `92360b75ffb2997539f9eef5fdda0d4530330215818aa5af4ca15f9ed7e935d1`

The pre-reveal sequence was:

1. plan commit `322ff6a0205abb6a262f48de3a01a46bcced7c9c`;
2. CT2 whitespace-key clarification `9247e36fc2910d32f474d2594ce4727d957c2aaf`;
3. score-free executable `50ace01631c0f031b7904c727dbf0b7c11b9940b`;
4. first-reveal workflow / tested head `843045d51de67a51310371255f3675349102e29d`.

## What happened

All six HTTP retrievals completed without curl failure: the three frozen DECODE URLs were each downloaded twice.

Within each URL, the two copies were byte-for-byte identical. However, all three nominal document types returned the **same** payload:

| frozen URL role | bytes | SHA-256 | repeat identity | strict UTF-8 |
|---|---:|---|---|---|
| transcription | 17,947 | `1e47167c4db694fe06f61f4c5650ac54eff2ce3ee2eff9dea78c7f15aa55b606` | identical | fail at byte 0, `0x89` |
| key_CT2 | 17,947 | `1e47167c4db694fe06f61f4c5650ac54eff2ce3ee2eff9dea78c7f15aa55b606` | identical | fail at byte 0, `0x89` |
| decryption_CT2 | 17,947 | `1e47167c4db694fe06f61f4c5650ac54eff2ce3ee2eff9dea78c7f15aa55b606` | identical | fail at byte 0, `0x89` |

The Gate-0 plan freezes strict UTF-8 decoding for the three `.txt` authorities. Therefore execution stopped before key parsing or any structural layer measurement. The machine result intentionally contains an empty `layers` object.

The exact binary media type is irrelevant to the frozen decision and is not repaired or reinterpreted post reveal. The decisive fact is that the three frozen text-authority URLs did not return three usable text payloads under the preregistered transport.

## Interpretation boundary

This result does **not** establish that the underlying Ramanacoil manuscript lacks physical lines, cipher grouping, plaintext lexical boundaries, or a usable scholarly alignment. The external HistoCrypt paper remains evidence that the source material and a CT2 workflow exist.

It establishes only that the **specific public DECODE transport frozen before reveal is not composable for this Priority-3 experiment**. Per the stop rule, no alternate filename, URL repair, archive replay, cached mirror, manual image segmentation, or post-reveal source substitution is licensed for Issue #194.

Ramanacoil therefore stops here for the main Priority-3 lane. The next step is to screen a different independently preserved historical corpus rather than repair this transport.
