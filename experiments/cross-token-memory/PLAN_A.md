# Issue #81 — minimal cross-token memory on frozen V2

Date frozen: 2026-09-02
Base main: `3a55c53c9cdd57ccf9a48b29f50eb81ef43dead8` (PR #80 merged)
Primary issue: #81

## Question

What is the smallest explicit cross-token memory that recovers the already-frozen cross-token fingerprint on top of OGH-C V2 without sacrificing the Issue #68 residual-topology result?

The experiment is structural. It does not test plaintext, cipher identity, language identity, or semantic content.

## Authorities reused without modification

- OGH-C V2 token generator and min-slot representation: `experiments/occupancy-generation-hierarchy/ogh_c.py`.
- Phase62/64 physical-leaf folds, paragraph parsing, S1/S2/S3, H62-P1 and `output_metrics`/`evaluate_aggregate`.
- Exact edit-distance-1 relation: Phase61/62 `edit1` / `build_neighbors`.
- Frozen H62 comparators N0, C0 and A1-R1 from Phase63A/64B.
- Frozen R1 target vectors, candidate-owned line-local null, 66 edges and Issue #68 gates as re-hosted in `ogh_a.py` for five folds.
- ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`.

No target metric below may be used to tune a model parameter unless explicitly stated here.

## Population and boundaries

ZL3b is primary. The five frozen physical-leaf folds are the train/test split. Every outer held-out leaf is untouched by fitting and model selection.

A Phase62 `Item` is a paragraph. `line_idx == 0` is the paragraph-entry line. Tokens are processed in manuscript order. A recent-token buffer is keyed by physical leaf and persists across paragraph boundaries on the same leaf; it resets at a physical-leaf boundary. This matches the locality scale of the prior A1 mechanism while not exposing future tokens.

Every candidate has exactly three fixed realizations, reps 0, 1, 2. Seeds are stable labels under the namespace `ISSUE81:<model>:fold<f>:rep<r>`. There are no rerolls.

IT2a is used for the replicated R1 topology target where the existing Issue #68 scorer defines it. The cross-token S1/S2/H62 layout is ZL3b-only because the frozen Phase62 paragraph/line contexts are defined there.

## X0 — frozen memoryless control

X0 is OGH-C V2 with no cross-token state. It is regenerated only as a replay/control; its scientific interpretation is already frozen by OGH-C.

## X1 — previous-token shape

State: the exact 12-bit min-parser occupancy mask of the immediately preceding generated token on the same physical leaf, plus a BOS sentinel.

For each previous-mask state, fit second-order unit-transition counts from outer-training leaves. The conditional transition backs off to the outer-training global V2 transition distribution with the same fixed pseudocount `BACKOFF` already used by V2. There is no fitted scalar memory parameter.

Generation samples a token unit sequence from the state-conditioned chain, reconstructs the surface token, then updates the previous-mask state from that generated token. If the contextual table is unseen, generation is exactly global V2.

Responsibility: adjacent shape coupling. X1 is not licensed by an S1/S2/H62 target.

## X2 — near-family activation

State: the previous at most 10 generated surface tokens on the same physical leaf.

The training vocabulary is built only from outer-training leaves. `build_neighbors` defines exact edit-distance-1 neighbors. On a memory event, choose uniformly among recent token occurrences that have at least one training-vocabulary edit-1 neighbor, then choose one of that source token's edit-1 neighbors with probability proportional to its outer-training token frequency. If no recent source has a legal neighbor, use V2. There is no exact-copy fallback: a memory event must emit an edit-1 neighbor.

With probability `pi`, use the memory event; otherwise sample frozen V2. Thus X2 has one fitted scalar, `pi`.

### X2 parameter selection

`pi` is selected without S1/S2/H62 access. For outer fold `f`, use the other four frozen fold groups as an inner leave-one-group-out cross-validation:

- inner validation group `g != f`;
- fit V2, training vocabulary, neighbor graph and frequency weights on leaves outside both `f` and `g`;
- score actual tokens of `g` sequentially using their observed previous-token context;
- evaluate only target tokens on V2 min-parser support so every grid point is compared on the same population;
- mixture probability is `(1-pi) P_V2(token) + pi Q_edit1(token | recent10)` when a legal memory source exists, otherwise `P_V2(token)`;
- sum log likelihood over all four inner validation groups.

Grid: `pi = 0.00, 0.01, ..., 1.00`; ties choose the smaller `pi`. This criterion is frozen before target reveal. The selected `pi` is then refit only in the sense that V2/vocabulary/frequencies use all outer-training leaves; `pi` itself is not changed.

The same likelihood calculation supplies a diagnostic held-out conditional cross-entropy in bits/token. It is explicitly a V2-support cross-entropy, not a claim about full-corpus Shannon entropy.

Responsibility: S2 and the raw H62 recurrence excess/profile. X2 has no paragraph-state input.

## X3 — paragraph-entry state

State: `ENTRY` for tokens on the first line of a Phase62 paragraph, otherwise `BODY`.

Fit one second-order unit-transition table per state from outer-training leaves. Each state-conditioned transition backs off to the same outer-training global V2 transition distribution with fixed `BACKOFF`. There is no fitted scalar memory parameter and no recent-token state.

Responsibility: S1. X3 is not licensed by S2 or H62.

## X4 — composition rule

X4 is run only if, after X1-X3 are frozen and scored:

1. X2 passes its responsibility gate for S2 plus H62 but does not pass S1; and
2. X3 passes S1 but does not itself pass the X2 responsibility gate.

X4 combines the already-selected X2 `pi` with the X3 ENTRY/BODY V2 baseline. `pi` is not reselected. No new parameter is added.

If the trigger is false, X4 is recorded as `NOT_LICENSED` rather than run post hoc.

## Frozen scoring

For each candidate, first aggregate the three fixed realizations with the existing Phase64 machinery.

### S1

- candidate aggregate S1 must have the same sign as the held-out Voynich target;
- ratio of aggregate means to held-out Voynich must be in `[0.5, 2.0]`.

Fold signs are reported diagnostically but are not an extra gate.

### S2

Ratio of aggregate candidate S2 to held-out Voynich must be in `[0.5, 2.0]`.

### H62 raw-magnitude gate

Before normalized profile comparison, require

`candidate H62 abs_excess_sum >= 0.5 * held-out Voynich H62 abs_excess_sum`,

using the same aggregate-excess construction as Phase62P/64B. The raw ratio is reported.

### H62 profile gate

After the raw gate, report the frozen Phase64B `D_profile` and `abs_C_short_diff` comparisons. The A1-R1 regime is operationalized without inventing a new tolerance: candidate mean `D_profile` and mean `abs_C_short_diff` must each be no worse than the frozen A1-R1 mean comparator. Foldwise win counts versus A1-R1 are reported as diagnostics. This gate is evaluated only after the raw-magnitude gate.

### R1

Every generated surface corpus is reparsed with SlotParser(min) into a 12-slot occupancy skeleton. The frozen OGH-A/Issue #68 five-fold scorer is then applied with a candidate-owned line-local reference/test null.

Necessary gate for each scored realization:

- parser coverage >= 0.60;
- residual existence: valid reliability folds >=4, median train-vs-heldout correlation >=0.50, maxT existence p <=0.01;
- for both frozen ZL3b and IT2a target vectors: Pearson >=0.70, familywise maxT p <=0.01, sign agreement >=50/66 with familywise p <=0.01.

All three realizations must pass R1 for the candidate to retain R1.

## Candidate classifications

`RECOVERS` requires all of:

- S1 sign + `[0.5,2]` ratio;
- S2 `[0.5,2]` ratio;
- H62 raw-magnitude gate;
- H62 normalized profile in the frozen A1-R1 regime defined above;
- R1 retained in all three realizations.

`PARTIAL` means at least one predeclared responsibility is recovered while the full conjunction fails.

`INSUFFICIENT` means none of the predeclared responsibilities is recovered.

X4 can receive these labels only if its composition trigger was licensed.

## Parameter accounting

The report distinguishes fitted memory scalars from conditional tables:

- X0: 0 memory parameters;
- X1: 0 fitted scalars; one previous-mask conditional count table with fixed backoff;
- X2: 1 fitted scalar (`pi`); training-vocabulary edit-1 graph and frequency weights are empirical tables;
- X3: 0 fitted scalars; two state conditional count tables with fixed backoff;
- X4: the same 1 fitted scalar inherited from X2 plus X3's two empirical state tables.

Table sizes, observed contexts and effective coverage are reported. They are not hidden by the scalar count.

## Additional diagnostics fixed before reveal

- X0/X1/X2/X3 and, if licensed, X4 V2-support held-out cross-entropy bits/token by outer fold and mean;
- X2 selected `pi` by outer fold and inner-CV likelihood curve;
- generated edit-1 memory-event rate and fallback rate;
- S3 is reported unchanged as a diagnostic but is not part of Issue #81 recovery classification;
- H62 `C_short` and its absolute target difference;
- parser coverage and all R1 continuous metrics.

No semantic or decipherment inference is permitted in the experiment report.