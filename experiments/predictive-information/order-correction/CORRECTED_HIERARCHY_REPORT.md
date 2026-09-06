# Corrected predictive-information hierarchy after source-order repair

Date: 2026-09-06
Issue: #100 under #98 / #88
Status: **CORRECTED C1→C3 SYNTHESIS**

## Why this rerun existed

Issue #98 Gate 0 found that lexical paragraph/document sorting distorted causal history for 22.1012% of parser-accepted tokens. The repair was fixed before any corrected predictive score: raw ZL3b page-header order defines document order and numeric `:pN` defines paragraph order.

The old parser/results remain archived; corrected results are versioned separately.

## Corrected authorities

- C1 Phase 1: `C1_PHASE1_PROVENANCE.md`
- C2 Phase 2A: `C2_PHASE2A_PROVENANCE.md`
- C3 Phase 2B: `C3_PHASE2B_PROVENANCE.md`
- ordering adapter: `../source_order_authority.py`

No S1/S2/H62/R1, semantic/image context, Currier/section/scribe metadata, future token or latent-state information entered the corrected model selection.

## 1. Phase 1 — robust

Legacy conclusion: material predictive information remains beyond simple local context.

Corrected conclusion: **ROBUST TO ORDER CORRECTION**.

Corrected means:

- V2 B0: `9.7089061 bits/token`;
- local B1: `9.5943670`;
- long B2: `9.5461692`;
- + observable state B3: `9.5172688`.

The selected architectures remain strikingly stable:

- B1 chooses `H=40,tau=32` in 5/5 folds;
- B2 chooses `H=ALL,tau=128,pi=.30` in 5/5 folds;
- observable-state gain remains ~`0.02890 bit/token`, positive 5/5.

The corrected long-history increment is `+0.04820 bit/token`, versus legacy `+0.04693`.

## 2. Phase 2A — robust

Legacy conclusion: the apparent long-history gain contains a large order-free prefix-inventory component plus smaller order-sensitive information.

Corrected conclusion: **ROBUST TO ORDER CORRECTION**.

Corrected primary contrasts:

- order-free prefix inventory beyond LOCAL40: `+0.0419740 bit/token`, positive 5/5;
- ORDERED128 over local+prefix hybrid: `+0.0062238`, positive 4/5;
- ORDERED128 over calibrated matched random lag: `+0.0248492`, positive 5/5.

Correct order modestly reduces the inventory estimate and increases the order-sensitive contrasts, but does not change the `MIXED PREFIX + ORDER CONTRIBUTIONS` classification.

## 3. Phase 2B — robust, with stronger cross-paragraph order evidence

Legacy conclusion: the dominant slow predictive source is associated with previous-paragraph inventory, not a uniform token-distance memory.

Corrected conclusion: **ROBUST TO ORDER CORRECTION**.

Corrected primary contrasts:

- same-line inventory: `0`, 0/5;
- current-paragraph inventory: `+0.0005153`, positive 4/5, effect-small;
- cross-paragraph inventory: **`+0.0414587`**, positive 5/5;
- current-paragraph actual lag vs matched random lag: `-0.0000746`, 0/5;
- previous-paragraph actual lag vs matched random lag: **`+0.0043079`**, positive 5/5.

The dominant cross-paragraph inventory effect remains about two orders of magnitude larger than the current-paragraph inventory increment. The corrected cross-paragraph order residual is larger and cleaner than the legacy value (`+0.0006074`, 4/5), but remains much smaller than the inventory effect.

## 4. Corrected working hierarchy

The best current predictive decomposition is:

1. **token-internal construction** — compact frozen V2 grammar;
2. **short local recency** — edit-1 mechanism around `H=40,tau=32`;
3. **dominant slower previous-paragraph inventory** — edit-1 token-family composition established before the current paragraph;
4. **secondary cross-paragraph order/lag information** — reproducible after matched randomization but much smaller than inventory;
5. **observable line/paragraph-position information** — independent additional gain from Phase 1.

This hierarchy survives the explicit source-order repair.

## 5. What is superseded

For future quantitative work, legacy Phase-1/2A/2B code lengths and fold-specific causal-history selections are **superseded numerically** by C1/C2/C3 corrected authorities.

The legacy qualitative conclusions are not retracted because they survive correction. When exact numbers matter, cite corrected authorities only.

Token-internal V2/R1 authorities are not superseded by this correction because the defect was in cross-item causal ordering, not token-internal parsing/emission.

## 6. What this changes conceptually

The earlier phrase “long memory” is now even less appropriate as a mechanistic label.

Corrected evidence says:

- a stable local recency mechanism exists;
- most additional slow predictive information is associated with which edit-1 token families were established in earlier paragraphs;
- exact previous-paragraph source/lag association contains additional information, but is secondary;
- the current paragraph itself contributes almost no extra inventory once LOCAL40 is present.

This points toward an observable paragraph/page-scale production state or external input before it points toward a rich hidden-state process.

## 7. Next licensed step

Resume Issue #98 Phase 2C using corrected C1–C3 as the only quantitative authority.

Primary structural split:

- `PREV1` vs `OLDER` previous paragraphs;
- `SAME_SIDE_PREV` vs `CROSS_SIDE_PREV` within the numeric physical leaf.

Both inventory and matched lag/order diagnostics remain required because corrected C3 strengthened the cross-paragraph order residual.

Only after this structural decomposition should independent Currier/section/scribe metadata and formal transport tests be introduced.

## Claim boundary

No decipherment, plaintext, language, semantic topic, cipher identity, author, syntax or latent state is established. Visible spaces remain production units for this analysis, not proven linguistic words.