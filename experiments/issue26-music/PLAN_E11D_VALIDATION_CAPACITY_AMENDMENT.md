# Issue26E11D locked-validation capacity amendment

Status: **FROZEN AFTER FIRST ATTEMPT FAILED BEFORE ANY VALIDATION FIT / SCORE**

The first locked-validation workflow attempt (`33386029356`) did not produce a validation result or artifact. It stopped during construction of validation index 0, before any key fitting, held-out fold scoring, accuracy calculation, or validation classification.

Observed infrastructure/input-capacity failure:

- the prior operational amendment requested 140,423 retained Latin characters per validation cipher;
- after applying the already-frozen unused-letter rule for validation 0 (`w`), the complete frozen CREMMA source provides only **77,099** eligible retained characters;
- the constructor therefore raised `validation population short omitted=w: 77099 != 140423` and exited.

No validation key-search result, fold metric, or pass/fail statistic exists from that attempt.

## Capacity-only correction

Change the per-validation plaintext event budget from **140,423** to **70,000 characters**.

Reasons fixed before any validation result:

1. 70,000 is below the observed frozen-corpus capacity in the first/most restrictive attempted construction;
2. 70,000 is the exact development population size used in DEV2 before validation and is therefore not selected from validation performance;
3. it remains a large sequence population for a 23-symbol monoalphabetic substitution;
4. all twelve validation cases continue to use distinct frozen run rotations, unused-letter positions, hidden-key seeds, and five-fold splits.

Everything else remains unchanged:

- frozen FREQ-HILL solver;
- 24-letter alphabet and normalization;
- run-rotation rule;
- rarity-ranked unused-letter rule;
- hidden-key seeds;
- five-fold rule;
- 12 validation ciphers;
- all validation thresholds;
- no post-validation tuning.

The failed pre-score attempt is retained in provenance and must not be described as a scientific validation failure.
