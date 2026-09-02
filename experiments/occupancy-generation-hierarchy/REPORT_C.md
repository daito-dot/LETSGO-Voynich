# OGH-C — token content and the cross-token test: first-reveal report

Status: **COMPLETE — information budget frozen; cross-token decision `MEMORYLESS TOKEN GRAMMAR PARTIAL` (with a recorded scorer caveat)**

Plan: `PLAN_C.md` (frozen first). Stage C0: `stage-c0/information_budget.json`. Stage C1: `stage-c1/` (per-realization metrics, aggregate, PROVENANCE, SHA256SUMS). Frozen scorers: `phase62b_n0.py`, `phase62p_h62p1.py`, `phase64b_naibbe.py`, unchanged.

## 1. Stage C0 — how much information does a Voynich token carry?

Cross-fitted held-out cross-entropy on parsed tokens (`SlotParser(min)`, 25,071 of 32,570 visible ZL3b tokens), five physical-leaf folds, ZL3b:

| model | what it knows | free params | bits / token (mean of folds) |
|---|---|---:|---:|
| G7A (OGH-B) | shape only: which of the 12 slots are filled | 298 | **7.01** |
| V0 | G7A shape × independent slot values | 319 | 11.12 |
| V1 | first-order chain over (slot, value) units | ≤ 561 | 9.89 |
| **V2** | second-order chain over units, back-off to V1 | observed contexts | **9.71** |
| V+ | memorized training token types (ceiling; 7.0% of held-out tokens out of vocabulary) | ≈ 3,000 | 9.01 (covered only) |

V2 was selected as the content grammar `V*` by the frozen rule (bits saved over V1 in 5/5 folds, `0.17–0.21`).

Reading: a parsed Voynich token carries about **9.7 bits** under the best compact memoryless grammar, of which **7.0 bits are the slot shape** and only **≈ 2.7 bits are the values** filling the slots. Values are far more predictable than shape: knowing which slots are filled and the two preceding units, the choice of letter in a slot costs on average well under one bit. Even memorizing the whole training vocabulary saves only 0.7 further bits on covered tokens while leaving 7% of held-out tokens unmodelled. For comparison, a uniform choice among the ≈ 4,077 admissible shapes alone would cost 12 bits. This is the first quantitative bound on the per-token information budget of the manuscript under its established structural representation.

## 2. Stage C1 — does a memoryless token generator reproduce cross-token structure?

V0, V2 and V+ were generated (3 realizations each) into the held-out paragraph/line skeleton and scored with the unchanged Phase64B pipeline against the frozen held-out Voynich targets.

| model | S1 ratio | S2 ratio | S3 ratio | exposed gate | H62 mean D | H62 mean ‖ΔC_short‖ | H62 "viable vs N0/C0" | Phase64B class |
|---|---:|---:|---:|---|---:|---:|---|---|
| V0 | −0.17 | 0.02 | 0.04 | fail | 1.13 | 0.23 | pass | PARTIAL |
| **V2** | **0.03** | **−0.02** | **0.03** | **fail** | 1.14 | 0.56 | pass | **PARTIAL** |
| V+ | 0.00 | −0.01 | 0.03 | fail | 1.58 | 0.18 | fail | PARTIAL |
| anchors | Voynich = 1 | | | | A1-R1 0.77 / N0 1.53 / C0 1.86 | A1-R1 0.12 / N0 0.64 / C0 1.31 | | |

Frozen decision (PLAN_C §5, model V2): **`MEMORYLESS TOKEN GRAMMAR PARTIAL`** — the exposed S1/S2/S3 gate fails, the Phase64B H62 viability gate passes.

### 2.1 The exposed responsibilities vanish

With no memory across tokens, paragraph-entry specialization (S1), previous-10 near-family locality (S2) and line-position grammar (S3) are all at **2–4% of the Voynich values**, i.e. zero within noise, for every model including the memorized vocabulary. V0's S1 is slightly negative (−0.17), V2's slightly positive (+0.03). This is the expected result and it is clean: **R3 and S2/S3 are not by-products of token-internal grammar plus layout.** Whatever produces them acts across tokens.

### 2.2 The H62 "viability" pass is a normalization artifact — recorded, not credited

The H62-P1 statistic normalizes the five-bin excess over an item-internal shuffle null to unit L1 mass before comparing profile *shapes*. For a memoryless generator the raw excess is noise: its L1 mass is `0.0017` (V+), `0.0033` (V0) and `0.0051` (V2), against `0.038–0.069` for held-out Voynich — roughly **ten times smaller**. Normalizing a near-zero vector produces an arbitrary unit profile, whose distance to the Voynich profile happens to fall below N0's and C0's. The fold-wise "wins" against N0/C0 therefore carry no evidence that the generator reproduces recurrence geometry; A1-R1 remains far better on both H62 metrics (`0.77 / 0.12`).

The frozen label stands as computed, but the scientifically correct reading of R2 here is **fail**: a memoryless token grammar produces essentially no near-family recurrence excess at any distance. For future scorecards a preregistered raw-excess magnitude gate (e.g. candidate `abs_excess_sum ≥ 0.5 ×` held-out Voynich) should precede any profile-shape comparison; that is a proposal for the next plan, not a retroactive change.

## 3. What OGH-C establishes

1. **Per-token information budget:** ≈ 9.7 bits per parsed token, 7.0 of them shape. The value layer is thin.
2. **Cross-token structure is not token-internal:** S1, S2, S3 and the raw H62 excess all collapse to noise under the best memoryless token grammar and under memorized vocabulary alike. The content-bearing, mechanism-discriminating signals of this program live in **cross-token memory** — which tokens follow which, where paragraphs begin, and how near-family forms recur within ten tokens.
3. **A methodological caveat for H62-P1:** the normalized-profile distance can be "won" by noise-level generators; magnitude must be gated first.

Together with OGH-A/B this closes the token-internal chapter: shape is a compact second-order successor grammar, values add little, and none of it explains the cross-token constraints.

## 4. Next frontier (for a new preregistration)

The obvious inverse question is now sharp. Given ≈ 10 bits per token of memoryless capacity, how many bits per token does the cross-token structure add, and what is the smallest memory (previous token, previous-10 family activation, paragraph-entry state) that recovers S1, S2 and the raw H62 excess while keeping R1? A1's copy-mutate mechanism is one answer; a reversible mechanism must supply the same memory. The first step is a memory-augmented V2 (unit chain conditioned on the previous token's parsed shape or on near-family presence in the previous ten tokens), scored under the same frozen pipeline with a raw-excess H62 gate.

## 5. Limits

ZL3b only (S1/S2/S3 contexts are ZL3b-defined); three realizations; V+ covers 93% of held-out tokens; the H62 caveat above. No claim about meaning, plaintext, cipher tables, word boundaries, Naibbe, or decipherment.
