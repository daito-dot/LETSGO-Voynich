# Hypothesis ledger addendum — Issue #104 Phase 3A

Date: 2026-09-06
Authority: `experiments/predictive-information/phase3a/REPORT.md`

## H104-1 — LOCAL40 is Currier-specific

**Status: rejected under the frozen mechanism-only transport test.**

Currier A-selected LOCAL40 strength (`pi=.14`) improves B in 5/5 folds; Currier B-selected strength (`pi=.16`) improves A in 5/5 folds. Mean transferred gains are `+0.06031` and `+0.05718 bit/token`, with near-zero target-oracle penalty.

Current evidence supports a common short edit-1 recency regularity across Currier A/B.

## H104-2 — one universal previous-paragraph mixture strength applies across Currier A/B

**Status: rejected.**

Source-stratum held-out selection gives:

- A `alpha_ALL_PREV=.09`;
- B `alpha_ALL_PREV=.19`.

A->B exact scalar transfer passes (`+0.02313 bit/token`, 5/5), whereas B->A fails (`-0.00028`, 2/5).

A target-oracle models nevertheless select nonzero alpha `.07-.10` and gain `+0.00976 bit/token` in 5/5 folds. Therefore the rejection is of a universal scalar strength, not of the PREV_PARAS architecture in A.

## H104-3 — the previous-paragraph mechanism family exists only in Currier B

**Status: rejected under the target-oracle diagnostic.**

Both A and B target-only nested selections use nonzero PREV_PARAS weights and improve all five target folds. B's optimum is materially stronger (`.17-.20`) than A's (`.07-.10`).

Current working hypothesis: **shared paragraph-inventory architecture with observable-regime-dependent strength**.

## H104-4 — Currier A/B differences are only vocabulary/support differences

**Status: rejected as a complete explanation.**

Strict source-support transport shows large vocabulary/emission mismatch, but mechanism-only transport still reveals a substantial A/B difference in the optimal PREV_PARAS strength. Thus support mismatch is real but does not exhaust the observable regime dependence.

## H104-5 — source vocabulary/emission support transports cleanly across Currier A/B

**Status: rejected.**

Strict source-support diagnostic:

- A->B exact-token OOV ~28.2%, mean CORE penalty ~`+2.3804 bits/token` versus target-support mechanism transport;
- B->A OOV ~14.8%, mean penalty ~`+1.3230 bits/token`.

The diagnostic remains finite/normalized, but support transport is poor.

## Next falsifiable question

Does the Currier-associated PREV_PARAS strength difference survive conditioning/transport across independently authoritative section/domain and hand/scribe strata?

Do not introduce latent states until those observable metadata sources have been audited and tested prospectively.
