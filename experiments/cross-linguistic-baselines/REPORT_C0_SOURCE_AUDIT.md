# Issue #84 Phase C0 — genre-control source audit

Status: **COMPLETE — SOURCE-ONLY AUDIT, TARGET SCORE CALLS = 0**

Date: 2026-09-06

Parent: Issue #84 Phase C

Preregistered authority: `PLAN_C0_SOURCE_AUDIT.md` at commit `ab2ec40ab77c614871c56adf57a81392e618364c`.

Source-audit run: `34012229118`, artifact `9982818403`, artifact digest `sha256:5e9a8ac42da461e5b1add46f62276c521ee54f546627e3377e55499060da0b96`.

Layout-audit run: `34012360882`, artifact `9982854639`, artifact digest `sha256:c19edbaf3da84988c7361c1e8c61b4608d9005fcec18ac3fe112f87555e1e922`.

Both workflows explicitly emitted `TARGET_SCORE_CALLS=0`. Neither imports or calls the Phase-A scorer.

---

## 1. Frozen source bytes

| ID | machine-readable authority | SHA-256 | layout XML SHA-256 | C0 result |
|---|---|---|---|---|
| C-REC-1 | Gutenberg `pg8102.txt` | `87d1a2819214526a7410c8b864f39a217e9bf93816a26736e01e8df25447c7eb` | n/a | **PASS** |
| C-REC-2 | IA `twofifteenthcent00aust_djvu.txt` | `6ffbad0b4b0b09e6c41d35c3edb019df42ecc649e0ef24e31bbd9b01d7d4bb6b` | `15cb66dbd33d123f40a79ec3797702f3b866fcc1b1f92121cb3833896e6acb64` | **PASS** |
| C-HERB-1 | IA `deviribusherbaru00mace_djvu.txt` | `1baed87fec67e0c7d785fc7c92452bba8185f03e18b1b02b6b0378717161d8e3` | `eb97444b606bb45b17d36fa3fa3635735c8eeb25537e78721105df3ddd6d1792` | **FAIL** |
| C-MED-1 | IA `leechdomswortcun01cock_djvu.txt` | `47797f08159dee1e1b94d72b909fd9c9d03a057fd539f3e74ac7c88af8b92a1c` | `df7eb45022acdc1bc822713d46f6b7a04c6350cef9743c7698db2bef3ea17fd5` | **PASS** |
| C-ACC-1 | IA `cu31924027939820_djvu.txt` | `0394af1ff19c72736be92e39bb459287c6290909ce85b8dbe65752d055b238e6` | `21124d8e190191cfa3ae1da52d50742e1af97d14a462545332e4c51739329036` | **PASS** |
| C-ACC-2 | IA `cu31924027939861_djvu.txt` | `01b3c016358f12e1e7137ce978dd40f9f34085bb176c22bad1dde6b72ac3e261` | `9e08a2dd2cab4273d3e5a2f90b69e3f77aa4f57db15556bd15b505435dc47552` | **PASS** |
| C-LIT-1 | IA `manualeetp00cath_djvu.txt` | `5724b4e59b8ece94252c7197ffb19f08651e152273f3086ec80553916b1fd059` | `c99a531fff3cf2de1210f301066ff9853dd8f5eeb6735922eb278587defac1ee` | **PASS** |

No downloaded third-party text/XML is committed to this repository.

---

## 2. Admission decisions and deterministic primary spans

### C-REC-1 — PASS

The Gutenberg file contains both the main **Forme of Cury** roll and a later separately introduced `ANCIENT COOKERY. A.D. 1381.` source. To keep the frozen source identity unambiguous, C-REC-1 admits only the main roll:

- start: exact first occurrence `FOR TO MAKE GRONDEN BENES [1]. I.`;
- end: immediately before exact first subsequent occurrence `[1]XPLICIT.`;
- editor note paragraphs whose first non-space characters match `^\[\d+\]` are removed before tokenization.

The later `ANCIENT COOKERY. A.D. 1381.` section is excluded from the C-REC-1 primary view; it was not the named source and is not promoted as an extra work.

Source-only extracted scale under this frozen rule: **11,850 word-like tokens**.

### C-REC-2 — PASS

The DjVu layout makes the two complete named Harleian texts objectively separable from the edition introduction, later small extracts and glossary:

- `Harl279`: DjVu pages 24–83 inclusive;
- `Harl4016`: DjVu pages 86–126 inclusive;
- on each page keep lines whose vertical midpoint is in normalized page-height interval `[0.10, 0.90]`;
- pages 84–85 are the second-text contents and are excluded;
- Ashmole/Laud/Douce extracts beginning after the two named manuscripts are excluded from the primary panel; they are partial extracts rather than comparable complete manuscript controls.

The normalized crop excludes running heads and the lower marginal/editorial notes without lexical judgement.

Source-only extracted scale:

- Harl. 279: **26,210 tokens**;
- Harl. 4016: **19,334 tokens**.

### C-HERB-1 — FAIL

The Macer poem has an objective work span (DjVu pages 43–138, ending at `Explicit Macer. Floridus`), but its critical apparatus is interleaved on the same pages and, on many pages, overlaps the poem's vertical range and uses substantially overlapping OCR line heights. A rule that separated all apparatus without losing variable amounts of poem text would require page-specific or lexical judgement.

Therefore C-HERB-1 is **C0 FAIL** under the preregistered no-target-aware-cleaning rule. This is a failure of this 1832 electronic edition for the automated comparison, not a scientific rejection of Macer or medieval herbals.

No replacement source is added after this failure. The already frozen C-MED-1 Herbarium remains the herbal/medical control.

### C-MED-1 — PASS

Cockayne's printed Herbarium resolves the apparent bilingual-mixing problem structurally:

- Old English primary-text pages are the odd DjVu pages **123, 125, …, 445**;
- the intervening even pages are the modern English translation and are excluded by page parity alone;
- page 447 begins `THE MEDICINA DE QUADRUPEDIBUS` and terminates the Herbarium primary span;
- on admitted odd pages keep lines whose vertical midpoint lies in normalized page-height interval `[0.12, 0.68]`.

The crop excludes running heads and the smaller lower-page apparatus while retaining the main Old English text. No language classifier or target statistic is used.

Source-only extracted scale: **25,012 tokens**.

### C-ACC-1 — PASS

Three explicitly delimited historical components are admitted as separate documents:

- `Countess1265`: pages **112–194**; page 195 begins `ADDITIONAL NOTES`;
- `Executors1291`: pages **202–248**; page 249 begins the editor's `APPENDIX`;
- `Howard1462_69`: pages **258–730**; page 730 contains the final account entries and `FINIS`, page 731 is printer matter.

For all three:

- keep lines with midpoint in normalized vertical interval `[0.12, 0.76]`;
- require OCR line bounding-box height `>= 40` pixels on the fixed 1929×2802 page geometry.

This typography-only rule removes running heads/page numbers and the smaller footnote type without reading account content.

Source-only extracted scale:

- Countess 1265: **22,109 tokens**;
- Executors 1291: **9,588 tokens**;
- Howard 1462–69: **147,864 tokens**.

### C-ACC-2 — PASS

Two large historical account spans are admitted as separate documents:

- `HouseholdBook1`: pages **40–276**; page 277 contains the editor's explicit notice that the MS breaks off and transitions to an index;
- `HouseholdBook2`: pages **320–559**; page 560 begins `ADDITIONAL NOTES AND CORRECTIONS`.

For both:

- keep lines with midpoint in normalized vertical interval `[0.12, 0.76]`;
- require OCR line bounding-box height `>= 40` pixels on the fixed 2085×2810 page geometry.

Source-only extracted scale:

- HouseholdBook1: **57,203 tokens**;
- HouseholdBook2: **69,847 tokens**.

### C-LIT-1 — PASS with fixed music-line exclusion

The York primary text is objectively bounded:

- start DjVu page **34**, headed `Ordo ad Faciendam Aquam Benedictam`;
- end DjVu page **235**, containing `Finit Processionale`;
- page 240 begins the separate comparative `APPENDIX`; pages 236–239 are not admitted.

Primary-page crop: retain line midpoints in normalized vertical interval `[0.10, 0.85]`.

Because the edition contains staff notation, raw OCR of music produces pseudo-word fragments that are not comparable lexical tokens. Before any target scoring, a fixed line-level typography/OCR filter is therefore frozen. A line is retained only when all are true:

1. it contains at least 3 Unicode word-like tokens;
2. at least 70% of non-space characters are alphabetic;
3. ASCII hyphen count / alphabetic-character count is `<= 0.03`;
4. one-character word-like tokens are `<= 25%` of the line's word-like tokens.

This removes staff/noise and heavily syllabified chant OCR while retaining prose prayers, rubrics and formulaic liturgical text. It is a source-validity filter, not a Voynich-similarity filter.

Source-only extracted scale under the frozen rule: **41,689 tokens**.

---

## 3. C0 result

Frozen admission set for Phase C:

- recipe/enumerative: C-REC-1, C-REC-2/Harl279, C-REC-2/Harl4016;
- herbal/medical: C-MED-1/Herbarium Old English;
- household/account: C-ACC-1 three components + C-ACC-2 two components;
- liturgical/formulaic: C-LIT-1 York Manual/Processional prose/formulaic view.

Total admitted independent source documents: **10**.

Excluded: C-HERB-1 Macer electronic edition only.

All admitted primary documents are above the 2,000-token C0 floor before Phase-C statistics are computed.

---

## 4. Firewall statement

At the time these sources, page spans, crop windows, typography thresholds and York music-line filters were selected:

- no Phase-C corrected MI had been computed;
- no Phase-C exact-repeat z-score had been computed;
- no source had been ranked against a Voynich target interval;
- no Phase-B transform had been applied;
- `TARGET_SCORE_CALLS=0` in both source-only workflows.

The next step is a separate `PLAN_C.md` freeze. Only after that plan fixes tokenization, document grouping, target metrics and classification rules may any Phase-C target statistic be produced.
