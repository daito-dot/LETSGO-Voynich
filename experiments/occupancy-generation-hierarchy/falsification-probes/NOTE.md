# Falsification probes against the OGH synthesis (exploratory, 2026-09-02)

The OGH-A/B/C synthesis reads the manuscript as "a small token grammar, thin content, local repetition". Three statistics were fixed in `probes.py` before any value was seen, then run on Voynich ZL3b (paragraph text, pages as documents), the four Phase62 CREMMA Latin manuscripts (files as documents), and the OGH-C memoryless V2 generator in the Voynich skeleton. **Exploratory only**: no gate, no classification; nothing here may be reused as a confirmatory target.

| probe | Voynich | Latin (CREMMA) | V2 generator | falsifies synthesis? |
|---|---|---|---|---|
| P1 2nd-order character-chain cross-entropy, bits/token (bits/char) | 12.4 (2.30) | 15.3 (4.50) | — | no: Voynich lower on both scales (representation caveat: graphematic Latin has a large abbreviation-rich inventory and mean token length 3.4 vs 5.4) |
| P1 held-out out-of-vocabulary type rate | 19.8% | 26.1% | — | no |
| P2 exact-repeat excess over within-document shuffle, z by distance bin 1–2 / 3–5 / 6–10 / 11–20 / 21–40 / 41–80 / 81–160 / 161–320 | +6.5 / +5.1 / +5.6 / +4.3 / +0.8 / −1.0 / **−6.7 / −8.0** | −3.8 / +15.6 / +18.3 / +22.0 / +15.1 / +13.1 / +8.5 / −0.4 | ≈ 0 everywhere | no: Voynich repeats cluster only within ≈ 20 tokens and are *depleted* beyond 80 within a page; Latin shows natural-language burstiness out to 160 |
| P3 adjacent-token mutual information, null-corrected (bits) | 0.066 | 0.40 | 0.01 | no: Voynich inter-token dependence is ≈ 6× weaker than Latin, consistent with the 0.06-bit X2 gain |

Caveats: page-level documents for Voynich vs file-level for Latin; graphematic Latin representation; section-scale vocabulary clustering (Montemurro & Zanette 2013; this project's stratum modulation) lies beyond the 320-token window and is not tested here. Results in `probes_results.json`.
