# Issue #203 — Dee plaintext→cipher R5 source attribution result

Date: 2026-09-08  
Parent: #172  
Preregistration authority: `68f4e3a4229b77d673fac27140443cd3288e3fcd`  
Frozen reveal run: `34220076742`  
Frozen result SHA-256: `89023bdcdc5142f8dedc6012b16b18d2e0f4e2c58a33dbb5d3c4d8fa6d2f2b7f`

## Primary result

**`NO_SHARED_LINE_LOCAL_TOPOLOGY`**

The clean Dee source does not reproduce the preregistered Voynich-like R5 topology on true lexical boundaries.

| Stream | G_line mean bits/event | positive folds | G_line | G_cross mean bits/event | positive folds | G_cross | Topology |
|---|---:|---:|---|---:|---:|---|---|
| solved plaintext | -2.330193 | 0/5 | FAIL | +0.432332 | 4/5 | PASS | `CROSS_ONLY_OR_UNSTABLE` |
| corrected ciphertext | -3.345904 | 0/5 | FAIL | -1.014850 | 2/5 | FAIL | `NO_ROBUST_LINE_EDGE` |

The decisive point for R5 source attribution is the same-line result: both streams are negative in **all five held-out folds**. Dee therefore provides no evidence that this historical plaintext or its cipher transform carries the required line-local terminal→initial edge under the frozen scorer.

## What happened across encryption

The preregistered paired transform diagnostics are non-gating, but their direction is simple:

- `D_line = cipher - plaintext`: mean `-1.015710` bits/event, positive in `0/5` folds;
- `D_cross = cipher - plaintext`: mean `-1.447182` bits/event, positive in `1/5` folds.

Within this document, encryption weakens rather than creates the tested terminal→initial predictability on both physical-relation populations. This is descriptive for this one source; it is not a general claim about historical ciphers.

## Secondary all-aligned replay

The frozen secondary replay puts non-ambiguous `WITHIN_WORD_SPLIT` events back into the same scorer. It does not rescue the line-local topology.

| Stream | G_line mean | positive folds | G_line | G_cross mean | positive folds | G_cross | Topology |
|---|---:|---:|---|---:|---:|---|---|
| solved plaintext | -2.285835 | 0/5 | FAIL | +0.087548 | 2/5 | FAIL | `NO_ROBUST_LINE_EDGE` |
| corrected ciphertext | -3.390855 | 0/5 | FAIL | -0.933112 | 1/5 | FAIL | `NO_ROBUST_LINE_EDGE` |

Thus the unusual positive primary plaintext cross-line result is not stable to the preregistered all-aligned replay. It remains part of the primary outcome because the lexical-boundary population was frozen before reveal, but it does not change the source-attribution conclusion.

## Boundary context

The source contains 13 frozen within-word splits: 2 on the same physical line and 11 across physical lines. Their predictive score was explicitly not licensed as a rescue primary.

The primary populations remained exactly as preregistered:

- 147 same-line lexical-boundary events;
- 25 cross-line lexical-boundary events after the prospectively frozen line 18→19 page-carry exclusion.

No event, boundary, fold, alpha, vocabulary rule or plaintext/cipher correction changed after reveal.

## Provenance

The successful one-shot reveal asserted:

- authority commit `68f4e3a4229b77d673fac27140443cd3288e3fcd`;
- scorer SHA-256 `8e373ffccb7871c94f8178daa56d987ba7b94342bbdd5ceb3aec160d61860ec4`;
- scorer Git blob `fa75a4dd8c1f7b39cc340fea5e1bd65fc4d19ba0`;
- `dee.xlsx` SHA-256 `c339aeac63da1b81560e63b02abb807a187a4003d3df44ebf389d3934055605d`;
- Gate-0 ledger SHA-256 `362bcd4a4edbbc5e93559b11a2e495ee71e897bdb97b28f1802b8a9df647edd5`;
- `voynich_accessed=false`.

The exact result JSON and reveal provenance are archived under `experiments/issue203-dee-stage1/result/`.

## Program consequence

This closes the clean Dee source-attribution test without a mechanism-specific rescue.

Combined with #181/#182:

- Borg established that a real historical ciphertext can display the qualitative line-local edge, but its surviving public plaintext transport could not cleanly identify where that topology arose;
- Dee provides a clean source/plaintext/cipher/layout alignment, but **does not display the required line-local topology in either plaintext or ciphertext** under the same basic edge-likelihood responsibility.

The clean external evidence therefore does not currently support a generic explanation in which ordinary plaintext lexical structure or a documented historical cipher transform naturally generates Voynich R5. R5 remains a compatibility responsibility, but Dee gives no positive mechanism attribution for it.

Per the fixed near-term roadmap, Priority 3 has now received one clean complete-preservation attribution test. The appropriate next program decision is to record this null/wrong-topology result and move to Priority 4 unless a new independent source is admitted prospectively; do not tune Dee or reopen Borg transport.
