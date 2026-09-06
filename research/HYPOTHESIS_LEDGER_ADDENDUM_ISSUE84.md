# Hypothesis Ledger Addendum — Issue #84 A–C

Date: 2026-09-06

Authority:

- Phase A: `experiments/cross-linguistic-baselines/REPORT_A.md`
- Phase B: `experiments/cross-linguistic-baselines/REPORT_B.md`
- Phase C: `experiments/cross-linguistic-baselines/REPORT_C.md`

Issue #84 was a prospective control program intended to break the post-OGH synthesis if the unusual cross-token regime could be explained by transcription choice, ordinary natural language, common reversible cipher operations, or plausible historical list/formulaic genres.

The relevant regime is the conjunction of:

1. unusually weak adjacent-token dependence (`MI1`);
2. positive immediate exact-repeat excess at distance 1–2;
3. weak/absent ordinary-language mid-range recurrence at distance 21–40.

Exact thresholds are phase-authoritative; this ledger records hypothesis state, not replacement scoring rules.

---

## H84-1 — the regime is a transcription artifact

**Hypothesis:** the cross-token pattern depends on a particular EVA/slot transcription lineage and disappears under independent readings.

**Frozen test:** seven independent Voynich readings in Phase A.

**Result:** **REJECTED for the tested transcription panel.**

All seven readings remain in the same low-adjacent-dependence / immediate-positive / mid-range-suppressed regime. Differences in exact values do not move any reading into the ordinary-language region.

**What this does not reject:** all conceivable tokenizations or the possibility that visible spaces have a non-linguistic role.

---

## H84-2 — ordinary natural language already occupies the regime

**Hypothesis:** the earlier CREMMA Latin contrast was an accidental language choice; sufficiently diverse ordinary natural languages overlap the Voynich regime.

**Frozen test:** 101 natural-language New Testament samples plus CREMMA anchors in Phase A.

**Result:** **REJECTED for the frozen ordinary-language panel.**

No language enters the Voynich adjacent-dependence regime. The large majority show negative immediate-repeat excess, while all 101 retain strong positive 21–40 recurrence.

**What this does not reject:** all meaningful text, all specialized genres, or language under a structure-changing transformation.

---

## H84-3 — a common reversible cipher/recoding operation automatically creates the regime from ordinary Latin prose

**Hypothesis:** monoalphabetic/homophonic substitution, nomenclators, null insertion, local transposition, verbose recoding, or the exact published Naibbe mechanism can transform frozen medieval Latin prose into the full three-component regime.

**Frozen test:** Phase B candidate map on the fixed four-manuscript CREMMA panel.

**Result:** **REJECTED for the frozen representatives.**

There were zero full hits. Partial responsibilities were separable:

- H4 and N256-4: adjacent MI only;
- line-local transposition: immediate-repeat responsibility only;
- published Naibbe: 21–40 recurrence responsibility only.

**What this does not reject:** all ciphers, all parameterizations, historically specialized compound mechanisms, or a separately motivated source×transform architecture.

**Prohibition:** do not post-hoc combine the successful responsibilities of Phase-B candidates and call the result supported. Any composition requires a new prospective plan.

---

## H84-4 — plausible list/formulaic historical source genres already create the regime before encryption

**Hypothesis:** the Phase-A contrast comes from comparing Voynich to prose rather than recipe/herbal/account/liturgical organization.

**Frozen test:** ten preregistered historical primary documents admitted by source-only C0 audit and scored in Phase C.

**Result:** **REJECTED for the frozen historical source panel.**

All ten sources are `0/3`. More strongly, every source misses in the same direction:

- `MI1` above the Voynich upper bound;
- `z1_2` below the Voynich lower bound;
- `z21_40` above the Voynich upper bound.

The closest work on each individual axis still lies outside the target interval: York liturgy for MI/immediate repeat, and *Forme of Cury* for 21–40 recurrence.

**What this does not reject:** every medieval genre, other editions, other languages, or transformed versions of these sources.

---

## H84-5 — ordinary meaningful text plus an untested compound transformation explains the regime

**State:** **LIVE BUT NARROWED / NOT YET TESTED.**

A compound mechanism can in principle alter all three responsibilities, and Phase B demonstrates that different operations can move different components. However, no compound was preregistered before the Phase-B/Phase-C reveals. Therefore no particular composition is currently evidentially supported.

**Licensing condition for a future test:** the architecture must be motivated independently of the observed near-misses, frozen before scoring, reversible if claimed reversible, and evaluated on the full R1/S1/S2/H62 plus inter-token responsibilities rather than only the statistic it was designed to repair.

---

## H84-6 — a small explicit cross-token memory generates the unusual regime without ordinary-language sequence structure

**State:** **LIVE / PRIORITIZED.**

Issue #81 already decomposed two responsibilities prospectively:

- paragraph ENTRY/BODY state recovers much of S1;
- previous-10 edit-1 activation recovers much of S2 but overproduces raw H62 recurrence;
- the tested local-memory predictive gain is small in average bits/token despite large recurrence contrast.

The next licensed test is the independently motivated soft near-family / recency-kernel memory selected by training/held-out likelihood only. It must not be tuned to the Phase-C genre results.

A sufficient memory is the dependency for Issue #84 Phase D scribe-conditioned memory tests.

---

## A–C control-tested synthesis

**SURVIVES CURRENT FALSIFICATION PROGRAM:**

> Voynich complete-token sequences occupy a transcription-robust inter-token regime that is not reproduced by the frozen ordinary-language panel, by the frozen common reversible-operation representatives applied to medieval Latin prose, or by the frozen recipe/herbal-medical/account/liturgical source panel.

This supports continued mechanism search around constrained generation / specialized transformation rather than unconstrained language identification.

It does **not** establish absence of meaning, absence of plaintext, hoax production, historical authorship, a cipher family, or decipherment.
