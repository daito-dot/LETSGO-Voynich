# Issue #84 Phase A — cross-linguistic and cross-transcription baselines: first-reveal report

Status: **COMPLETE — `NO NATURAL LANGUAGE IN VOYNICH REGIME`; `VOYNICH REGIME TRANSCRIPTION-ROBUST`**

Plan: `PLAN_A.md` (frozen first; one recorded parsing clarification). Results: `first-reveal/phase84a_results.json` (SHA-256 `86d18560b5999836b7c0d22fa9c3d8dbfd9f11ba246613fd0c2527d5ed5ffe1c`), pre-reveal head `de55d204c604d5b0d8ee2ee6bed48dc196ef23de`. Sources: seven voynich.nu IVTFF readings (hashes in the JSON), `christos-c/bible-corpus` at `44e5fca1bfb369a5da2ee23ebc6f421c88489c5c`, CREMMA `2925259…`.

## 1. Population

101 languages scored (first 32,570 New-Testament tokens each, chapters as documents); excluded by frozen rules: Chinese (EXCLUDED_UNTOKENIZED_DUPLICATE), Gaelic-PART (NO_NT_MARKER), Japanese (EXCLUDED_UNTOKENIZED_DUPLICATE), Potawatomi-PART (INSUFFICIENT_SIZE), Thai (EXCLUDED_UNTOKENIZED_DUPLICATE), Tuareg-PART (NO_NT_MARKER), Vietnamese (EXCLUDED_UNTOKENIZED_DUPLICATE). Seven Voynich readings (pages as documents): ZL3b, IT2a, VT0e, RF1b (EVA family, composites collapsed), GC2a (v101), CD2a (Currier, partial transcription), FG2a (FSG). Anchors: CREMMA Latin (graphematic) and the OGH-C memoryless V2 generator.

## 2. Results

Columns: MI₁ = null-corrected adjacent-token mutual information (bits); Q1b = compression-based ordering information (bits/token); z₁₋₂, z₂₁₋₄₀, z_far = exact-repeat excess z-scores for distance bins 1–2, 21–40 and max(81–160, 161–320); Q3 = second-order unit-chain held-out cross-entropy; OOV = held-out unseen-type rate.

| corpus | tokens | types | MI₁ | Q1b | z₁₋₂ | z₂₁₋₄₀ | z_far | bits/token | bits/unit | OOV |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 35,205 | 6,879 | 0.110 | 0.16 | +8.5 | +1.4 | -3.8 | 11.26 | 2.55 | 0.143 |
| IT2a | 34,486 | 7,090 | 0.089 | 0.13 | +7.2 | +1.8 | -4.1 | 11.47 | 2.54 | 0.151 |
| VT0e | 34,486 | 7,090 | 0.088 | 0.12 | +7.0 | +2.3 | -5.0 | 11.47 | 2.54 | 0.151 |
| RF1b | 34,865 | 7,152 | 0.090 | 0.13 | +5.0 | +3.4 | -4.2 | 11.43 | 2.63 | 0.151 |
| GC2a | 36,658 | 8,602 | 0.111 | 0.15 | +2.8 | +2.6 | -3.0 | 12.11 | 3.13 | 0.179 |
| CD2a | 16,223 | 3,997 | 0.053 | 0.10 | +4.2 | -0.8 | -4.1 | 11.37 | 2.77 | 0.181 |
| FG2a | 33,199 | 6,598 | 0.084 | 0.11 | +6.0 | +3.1 | -3.9 | 11.27 | 2.63 | 0.143 |
| natural languages (n=101) | 32,570 | 902–18,572 (median 4,669) | 0.173–1.584 (median 0.820) | 0.60–2.96 (median 2.02) | -35.5–+3.9 (median -17.8; 95/101 negative) | +7.1–+33.7 (median +20.2; 101/101 > +2) | -15.1–+4.7 (median -7.2) | 8.55–34.95 (median 14.29) | 2.41–7.80 (median 3.05) | 0.015–0.497 (median 0.100) |
| CREMMA_Latin_graphematic | 18,178 | 5,767 | 0.399 | 1.06 | -3.5 | +19.6 | +8.5 | 20.04 | 5.61 | 0.464 |
| V2_memoryless_generator | 32,570 | 3,523 | 0.010 | 0.01 | +0.9 | +0.9 | +0.6 | 9.73 | 2.21 | 0.061 |

Lowest-MI languages: Burmese 0.173, Telugu 0.387, Ashaninka-NT 0.476, Ojibwa-NT 0.493, Cherokee-NT 0.514. Languages with positive immediate-repeat excess (z₁₋₂ > 0): Amharic +3.9, Turkish +2.8, Tachelhit-NT +2.5, Shona +2.3, Quichua-NT +0.2.

## 3. Frozen classification

- **`NO NATURAL LANGUAGE IN VOYNICH REGIME`.** No language satisfies the joint criterion. The decisive component is MI₁: every Voynich reading lies at `0.053–0.111` bits, below the lowest language (Burmese `0.173`, itself an outlier with 50% OOV from its script's word segmentation) and roughly one eighth of the language median (`0.820`). The Q1b compression measure agrees (Voynich `0.10–0.16` vs language median `2.02`).
- **`VOYNICH REGIME TRANSCRIPTION-ROBUST`.** All seven readings, including the non-EVA Currier and FSG alphabets and the v101 reading, fall below every language on MI₁ and have non-positive far-bin excess.

## 4. What the frozen far-bin criterion did and did not do

The far-bin criterion (z ≤ +2 at 81–160 and 161–320) was satisfied by 100/101 languages, so it did not discriminate. With chapter-length documents (median 757 tokens) the far bins sit at the document boundary, where local clustering produces depletion for any corpus. The exploratory CREMMA result (positive excess to 160 tokens with whole files as documents) is a document-length effect, not a language universal; the plan's far-bin component is therefore reported as **uninformative under the chosen document unit** and the classification rests on MI₁ alone. This is recorded, not repaired.

## 5. Descriptive findings not part of the frozen classification

1. **Immediate repetition has the opposite sign.** 95 of 101 languages have *negative* excess at distance 1–2 (median z `-17.8`: natural prose avoids repeating a word immediately), while every Voynich reading has *positive* excess (z `+2.8` to `+8.5`). Only Amharic, Turkish, Tachelhit and Shona show weak positive values. Voynich's repeat clustering is concentrated exactly where language suppresses it.
2. **Mid-range burstiness is language-universal and absent in Voynich.** At 21–40 tokens 101/101 languages exceed z = +2 (median `+20.2`); Voynich readings sit at `−0.8` to `+3.4`.
3. **Vocabulary is not small.** At matched size Voynich has 6,598–8,602 types against a language median of 4,669, and a higher held-out unseen-type rate (0.14–0.18 vs median 0.10). The earlier informal remark that Voynich has a "small vocabulary" is withdrawn: it has *many* distinct forms that are *weakly predictable from their neighbours* and *similar to one another* (the edit-1 families of H62).
4. **Character-level information density is low-middle, not extreme.** bits/token `11.3–12.1` vs language median `14.3` (range `8.6`–`35.0`); bits/unit `2.5–3.1` vs median `3.05`. Several natural languages (Japanese-tok, Maori, Aukan, Creole) are lower per token. The synthesis's "low information density" should be stated at the token-sequence level (weak dependence, no burstiness), not as an unusually low per-character entropy.

## 6. Reading

The synthesis survives its first cross-linguistic test and is sharpened: what separates Voynich from all 101 natural-language samples is not how much information a token carries but **how tokens relate to their neighbours** — almost no adjacent dependence, repetition of the same form at distance 1–2 where language avoids it, and no topical burstiness at 20–40 tokens where every language shows it. The V2 generator has none of these features either (MI 0.01, all z ≈ 0), so the Voynich regime is a specific signature between "memoryless" and "language", exactly where Issue #81's small memories sit.

## 7. Limits

One genre (Bible prose) and one document unit; Phase C addresses genre and Phase B cipher families. Q3 is representation-dependent. No result bears on meaning, plaintext, cipher tables or decipherment.
