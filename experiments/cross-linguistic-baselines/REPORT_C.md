# Issue #84 Phase C — historical genre controls

Status: **COMPLETE — AUTHORITATIVE FIRST REVEAL ARCHIVED**

Date: 2026-09-06

Parent: Issue #84

Preregistered / audit authority:

- C0 source-list freeze: `PLAN_C0_SOURCE_AUDIT.md`, commit `ab2ec40ab77c614871c56adf57a81392e618364c`;
- C0 source-only report: `REPORT_C0_SOURCE_AUDIT.md`, commit `0efae2f963fb49183668634498c86da0e81c2fef`;
- Phase-C plan freeze: `PLAN_C.md`, commit `9f9bfc5f55041d3a6845b764758b1e0d164bcedf`;
- score-free extraction preflight: run `34012721055`, head `97b2c98a9039c2467a722ee6ba802ec3b8044999`, artifact `9982965549`; all ten C0 counts matched and `TARGET_SCORE_CALLS=0`;
- authoritative first reveal: run `34012762571`, scientific head `2dbb153c492cee3f1ba0b0cc63087900d31dc4a7`;
- first-reveal artifact `9982984175`, ZIP SHA-256 `fb6ee38114f7c016b4d621237cf4a4b1e0d0d17e4317b51c22591dcaf3cee4af`;
- result JSON SHA-256 `e5d688b15538288b435cfdf17ed582d0de13c6d6209f93e67d3096199e84e58b`;
- compact summary SHA-256 `d3762647c2d945c90dec4e13e5af983aa9010be5ccb634e869ab3aabcb32183a`.

The exact result JSON, compact summary, provenance and checksums are committed byte-for-byte under `first-reveal-c/`. Third-party historical source bytes are not committed.

---

## 1. Frozen question

> Do preregistered medieval / late-medieval recipe, herbal-medical, household-account or liturgical texts themselves occupy the transcription-robust Voynich inter-token regime that ordinary natural-language prose and the tested common cipher representatives do not?

Phase C tested source organization **before encryption**. No Phase-B transformation was applied.

The work-level primary responsibilities remained exactly those frozen in Phases A/B:

| responsibility | exact seven-reading Voynich interval |
|---|---:|
| adjacent corrected `MI1` | `0.052873 … 0.110956` bits |
| exact-repeat `z1_2` | `+2.79637 … +8.45583` |
| exact-repeat `z21_40` | `−0.77007 … +3.43462` |

A work was a full source hit only if **all three** responsibilities passed. No omnibus average could repair a failed component.

---

## 2. Frozen source panel

C0 admitted ten independently named primary source documents:

- recipe/enumerative: *The Forme of Cury*, Harleian MS 279, Harleian MS 4016;
- herbal/medical: the Old English *Herbarium* from Cockayne vol. 1;
- household/account: Countess of Leicester 1265, Executors of Eleanor of Castile 1291, Sir John Howard 1462–69, and two Norfolk/Surrey household-book spans;
- liturgical/formulaic: York *Manuale et Processionale*.

The Macer Floridus electronic edition failed C0 before target scoring because the poem and critical apparatus could not be separated by a uniform edition-layout rule. It was not replaced after exclusion.

Each admitted source retained frozen historical/OCR spelling and was scored as one continuous source document, with the first `32,570` normalized tokens used where the source was longer. The C0 extraction counts were reproduced exactly before the first target statistic was allowed to run.

---

## 3. Authoritative work-level result

| source | tokens scored | `MI1` | `z1_2` | `z21_40` | result |
|---|---:|---:|---:|---:|---|
| Forme of Cury | 11,850 | 1.1373 | −11.77 | +5.91 | **0/3 — NO SOURCE HIT** |
| Harl. MS 279 | 26,210 | 1.1978 | −13.08 | +21.41 | **0/3** |
| Harl. MS 4016 | 19,334 | 1.1360 | −26.76 | +18.79 | **0/3** |
| Old English Herbarium | 25,012 | 0.7247 | −1.49 | +25.67 | **0/3** |
| Countess 1265 | 22,109 | 1.6791 | −24.53 | +11.13 | **0/3** |
| Executors 1291 | 9,588 | 1.2713 | −13.09 | +21.00 | **0/3** |
| Howard 1462–69 | 32,570 | 1.6634 | −24.77 | +71.86 | **0/3** |
| Household Book 1 | 32,570 | 1.6209 | −21.99 | +37.66 | **0/3** |
| Household Book 2 | 32,570 | 1.9241 | −31.99 | +54.73 | **0/3** |
| York Manual/Processional | 32,570 | 0.5426 | +0.47 | +72.35 | **0/3** |

Frozen panel classification:

> **`NO FROZEN HISTORICAL SOURCE IN FULL VOYNICH REGIME`**

There were:

- **0 / 10 full hits**;
- **0 / 10 partial 2-of-3 hits**;
- **0 / 10 partial 1-of-3 hits**.

Thus every preregistered source fails every primary responsibility.

---

## 4. The failure direction is uniform across all ten sources

This is stronger than merely observing ten failed conjunctions.

### 4.1 Every source has too much adjacent-token dependence

All ten `MI1` values lie **above** the Voynich upper bound `0.110956`.

The closest source is the York liturgical text at `0.5426`, still about `0.432` bits above the allowed interval. The recipe texts are around `1.14–1.20`; the account texts are mostly `1.27–1.92`.

Changing from ordinary prose to highly formulaic/list-like historical writing therefore does not reproduce the manuscript's unusually weak adjacent token dependence. In this panel it often increases or preserves strong local predictability.

### 4.2 Every source has too little immediate exact-repeat excess

All ten `z1_2` values lie **below** the Voynich lower bound `+2.796`.

The closest source is again the York text at `+0.47`; the Old English Herbarium is `−1.49`; recipes and accounts are substantially negative, down to `−31.99`.

The Phase-A sign contrast therefore survives these historical genre controls: Voynich has a local excess of exact token reuse that the tested natural texts do not reproduce.

### 4.3 Every source has too much 21–40-token recurrence

All ten `z21_40` values lie **above** the Voynich upper bound `+3.435`.

The closest source is *Forme of Cury* at `+5.91`; all others are `+11.13` to `+72.35`.

The structured account and liturgical sources do not suppress ordinary mid-range recurrence. Several intensify it dramatically.

The complete source panel therefore misses Voynich in the same three-dimensional direction:

> **adjacent dependence too high; immediate exact reuse too weak; mid-range recurrence too strong.**

---

## 5. What Phase C changes

The motivating alternative was that Phase A might simply have compared Voynich to the wrong natural-language genre. Recipe collections, herbals, accounts and liturgy have strong formulaic/list structure and are historically closer to plausible manuscript contents than a parallel Bible corpus.

That alternative does not survive this frozen panel.

The result does **not** say that these genres are statistically interchangeable with ordinary prose. They are not. For example, some account/liturgical sources have extremely strong mid-range recurrence. The key result is narrower: their genre-specific organization moves them in the wrong direction for the complete Voynich conjunction.

This is especially important because Phase B had already shown that individual reversible operations can supply individual responsibilities:

- H4 / N256-4 can reduce adjacent MI into the Voynich interval;
- line-local transposition can produce a Voynich-scale positive immediate-repeat excess;
- published Naibbe can suppress the 21–40 recurrence into the Voynich interval.

Phase C now shows that the tested source genres do not naturally provide the missing conjunction before encryption either. Phase B's partial mechanisms therefore remain partial; they are not rescued by simply changing the plaintext from prose to recipe/list/account/liturgy in an untested post-hoc composition.

---

## 6. A–C synthesis for Issue #84

Issue #84 was explicitly designed to break the OGH synthesis if ordinary language, transcription choice, common cipher families or plausible list-like historical genres could reproduce the same regime.

After A–C:

1. **Transcription robustness:** the low-MI / immediate-positive / mid-range-suppressed regime appears across seven independent Voynich readings.
2. **Cross-language control:** none of 101 frozen natural-language samples enters the adjacent-dependence regime; ordinary languages overwhelmingly show the opposite immediate-repeat sign and universally strong 21–40 recurrence under the Phase-A panel.
3. **Cipher-family control:** none of the frozen common reversible-operation representatives produces the complete three-component conjunction from CREMMA Latin; some reproduce one responsibility only.
4. **Historical genre control:** none of ten preregistered recipe, herbal-medical, household-account or liturgical sources reproduces even one of the three responsibilities simultaneously at work level; every work falls on the same side of all three target intervals.

The control-tested descriptive synthesis therefore survives A–C:

> **Voynich token construction is compact and low-order internally, while the sequence of complete tokens occupies an unusual inter-token regime: much weaker adjacent token dependence than ordinary historical language, a localized excess of immediate token reuse, and suppression of the mid-range recurrence/burstiness that remains strong in ordinary and highly formulaic natural texts.**

This is a structural result, not a semantic conclusion.

---

## 7. Hypothesis consequences

The tested branch `ordinary meaningful text → ordinary/list-like source organization → common reversible transform` has become materially narrower.

Still live:

- a generated or syntactically impoverished artificial system;
- a specialized high-redundancy code or mechanism outside the frozen Phase-B representatives;
- meaningful source text under a more specialized historical transformation whose architecture explicitly changes token-relation geometry;
- the independently motivated small-memory generative model from Issue #81;
- untested historical source classes.

Not licensed:

- “the manuscript contains no meaning”;
- “all ciphers are excluded”;
- “all medieval genres are excluded”;
- “the manuscript is a hoax”;
- any plaintext, language, cipher key or author claim.

---

## 8. Next move

Issue #84 specified Phase D only **after Issue #81 lands a sufficient memory**. Phase C therefore changes the active dependency:

> return the main research lane to Issue #81 and test the preregistered **soft near-family / recency-kernel memory** selected by training/held-out likelihood only.

The goal is to determine whether a small target-blind cross-token mechanism can jointly recover the local S2/H62 responsibility without overproducing raw recurrence, while retaining R1. If such a component becomes sufficient, it can then be prospectively combined with the already-supported paragraph ENTRY/BODY component X3. Only after a sufficient memory exists is Issue #84 Phase D (scribe-conditioned memory parameters / external anchors) licensed.

Do not use the Phase-C result to tune that memory against the genre-control statistics.

---

## 9. Claim boundary

The Voynich Manuscript is not deciphered.

Phase C is a source-genre falsification result. It shows that the complete preregistered historical panel fails the same transcription-robust inter-token regime in a uniform direction. It does not establish the historical generation mechanism or the presence/absence of semantics.
