# Phase 64A report — empirical-inventory autonomy ablation

Status: **completed; frozen overall classification = `INCONSISTENT / PRIMARY FAILURE`**.

Exact numerical authority: `phase64a_inventory_autonomy_results.json`.

Normative pre-result authority:

- `DECISION_64.md`
- `PLAN_A.md`
- `IMPLEMENTATION_A.md`

## 1. Scientific question

Phase64A tested whether the strongest A1/A1-R1 structural advantage depended on being handed an explicit empirical training-token inventory and its observed edit1 topology.

A1-R2/MG0 replaced that list with a synthetic vocabulary generated only from a low-order character Markov model learned on distinct training token types. It did not add a new A1 mechanism.

Two arms were frozen:

- **ZL primary** — exact canonical Phase63A setup;
- **IT2a W1 independent** — exact independent-reading Phase63B setup.

Strong inventory-autonomy support required both arms to pass every frozen exposed and H62 criterion.

## 2. Chronology and implementation firewall

Before first scientific calculation:

1. Phase63B strong replication was merged to main;
2. `DECISION_64.md` selected inventory autonomy as the next falsification challenge;
3. `PLAN_A.md` froze MG0, seeds, source arms and pass/fail rules;
4. MG0/A1-R2 implementation was committed;
5. static inspection found one **pre-result authority-key typo** in an unused initial `main()` guard; the official entrypoint corrected only that key name before science;
6. non-scientific preflight run `33335257971` compiled the code, verified prior result hashes/keys and tested MG0 only on synthetic toy strings;
7. the read-only first-reveal workflow and official entrypoint were committed at head:

`5e9121f7e05d8950f223298a44b816d6ee088e07`

No Phase64 scientific result existed before that head was frozen.

## 3. MG0 model-selection result

Training-only inner CV independently selected **order 2 in all ten outer folds**:

- ZL: 5/5 folds;
- IT: 5/5 folds.

No order was selected using S1/S2/S3/H62 or held-out token strings.

The order-2 CV NLL was consistently lower than order 1, which was consistently lower than order 0. The result therefore did not depend on a fold-specific switch among qualitatively different morphology models.

## 4. How strong was the inventory intervention?

The synthetic vocabulary had exactly the same number of types as the empirical outer-training vocabulary, but membership was generated rather than selected from the observed list.

Across all 25 synthetic vocabularies per source:

| diagnostic | ZL empirical | ZL MG0 | IT empirical | IT MG0 |
|---|---:|---:|---:|---:|
| mean token length | 6.734 | **8.542** | 6.289 | **8.004** |
| fraction of types with edit1 neighbor | 0.802 | **0.441** | 0.870 | **0.481** |
| mean edit1 degree | 5.997 | **3.048** | 6.988 | **3.382** |

Synthetic membership overlap:

- ZL with empirical training vocabulary: **0.2017**;
- ZL with held-out observed vocabulary: **0.1166**;
- IT with empirical training vocabulary: **0.2270**;
- IT with held-out observed vocabulary: **0.1344**.

Thus roughly four fifths of synthetic ZL types and more than three quarters of synthetic IT types are **not** members of the empirical training token list, and held-out overlap is only about 12–13%.

The edit1 graph is also substantially sparser than the empirical graph. This is a real structural intervention, not a near-copy of the original vocabulary.

No empirical membership lookup was used to accept or reject generated synthetic types.

## 5. ZL primary result — frozen FAIL

### 5.1 Exposed scorecard

A1-R2 / held-out ZL ratio-of-means:

- **S1 0.84668× — PASS**
- **S2 0.92025× — PASS**
- **S3 0.46772× — FAIL** against frozen lower bound `0.5`.

Absolute across-fold means:

- target S1 `0.87599`; A1-R2 `0.74168`;
- target S2 `0.04388`; A1-R2 `0.04038`;
- target S3 `0.02827`; A1-R2 `0.01322`.

The primary arm therefore fails the exact preregistered exposed gate because of S3 alone.

This boundary is not relaxed after the result.

For context only, A1-R1 had ZL ratios:

- S1 `0.65353×`
- S2 `1.51061×`
- S3 `0.58264×`

Removing the empirical vocabulary moved S1/S2 closer to the target but reduced S3 below the historical gate.

### 5.2 ZL H62-P1

A1-R2:

- mean `D_profile` **0.76160**;
- median `D_profile` **0.80436**;
- mean `|ΔC_short|` **0.12030**.

Comparators:

- N0 mean D `1.52982`, mean C-short error `0.63750`;
- C0 mean D `1.85866`, mean C-short error `1.30765`.

A1-R2 wins:

- versus N0: **5/5 on D and 5/5 on C-short**;
- versus C0: **5/5 on D and 5/5 on C-short**.

Relative to empirical-inventory A1-R1:

- mean D changes **-0.00500** (slightly better);
- mean C-short error changes only **+0.00261**.

So the prospective recurrence-distance signature is essentially unchanged despite the severe vocabulary/topology intervention.

### 5.3 ZL fold heterogeneity retained

Per-fold exposed ratios include substantial variation:

- fold0: S1 `0.724`, S2 `0.698`, S3 `0.450`;
- fold1: `0.408 / 0.710 / 0.289`;
- fold2: `4.717 / 1.070 / 0.909`;
- fold3: `1.445 / 1.303 / 0.780`;
- fold4: `0.472 / 0.803 / 0.249`.

The historical gate is aggregate ratio-of-means, not a universal per-fold gate. These values nevertheless reinforce that A1 remains an incomplete generator.

## 6. IT independent result — frozen PASS

### 6.1 Exposed scorecard

A1-R2 / held-out IT W1 ratio-of-means:

- **S1 1.13567× — PASS**
- **S2 0.97605× — PASS**
- **S3 0.58586× — PASS**

All three remain inside `[0.5,2.0]`.

For context, A1-R1 had IT ratios `0.73723 / 1.58617 / 0.64696`.

Again, inventory removal moves S1/S2 closer to unity while reducing S3.

### 6.2 IT H62-P1

A1-R2:

- mean D **0.83163**;
- median D **0.93055**;
- mean C-short error **0.07486**.

Comparators:

- N0 mean D `1.47727`, mean C-short error `0.62192`;
- C0 mean D `1.79735`, mean C-short error `1.29206`.

Fold wins:

- versus N0: D **4/5**, C-short **5/5**;
- versus C0: **5/5 on both**.

Relative to IT A1-R1:

- mean D changes only **+0.00135**;
- mean C-short error changes only **+0.00302**.

The IT arm therefore passes every frozen Phase64A source-arm criterion.

## 7. Frozen Phase64A classification

The preregistered overall rule required both arms to pass.

- ZL primary: **FAIL** — only S3 misses the scalar gate;
- IT independent: **PASS**.

Frozen classification:

> **INCONSISTENT / PRIMARY FAILURE — independent IT passes but canonical ZL fails the frozen inventory-autonomy gate.**

Therefore Phase64A does **not** support the broad preregistered statement that the complete tested A1 scorecard is inventory-autonomous across both source arms.

## 8. What the failure does and does not mean

The failure is narrow but real.

The explicit empirical token inventory contributes enough to the ZL aggregate line-position statistic that removing it reduces S3 from A1-R1 `0.583×` to A1-R2 `0.468×`, below the frozen threshold.

However, the result strongly argues against a different explanation:

> A1's prospective recurrence-distance success is not primarily a consequence of being handed the observed token membership list or its exact edit1 graph.

Why:

1. synthetic vocabularies overlap empirical training vocabulary only ~20–23%;
2. held-out overlap is only ~12–13%;
3. edit1 connectivity is approximately halved;
4. ZL H62 performance is essentially unchanged and beats N0/C0 5/5 on both diagnostics;
5. IT H62 performance is also essentially unchanged and passes the full source-arm gate.

The formal local-family mechanism is therefore doing real explanatory work on the prospective recurrence geometry. The empirical inventory is more relevant to the imperfect line-position behavior than to the core H62 result.

## 9. Why Phase64A should not be repaired

S3 was already known to be a comparatively weak discriminator:

- Phase62 N0 nearly matches the Voynich aggregate S3 scalar;
- Phase61 showed that aggregate eta2 can hide severe coordinate-profile mismatch.

The ZL S3 miss is still a frozen failure and remains in the ledger. But adding A2 machinery merely to push `0.468` over `0.5` would optimize a weak scalar after seeing the result and violate the stop rule.

Therefore the next high-information move is **not** an S3 repair pass.

## 10. Strategic consequence

Phase64A changes the balance of remaining objections:

- exact empirical vocabulary membership is no longer a persuasive explanation for the prospective H62 success;
- full A1 structural autonomy is **not** established because the ZL omnibus gate fails;
- further G-side tuning now has declining information value and high overfitting risk;
- family-comparison unfairness becomes the more important unresolved objection because C0 remains deliberately weak.

The next frontier should therefore shift to a separately frozen **serious bounded C1 challenge** rather than A2.

C1 must be strong enough that a later G-vs-C comparison is scientifically meaningful, but must remain complexity-charged and held-out/prospective.

## 11. Claims still forbidden

Do not infer:

- Voynichese is meaningless;
- semantic content is absent;
- A1 is the historical generator;
- G has defeated the full C or N family;
- Phase64A fully establishes autonomy;
- the manuscript is deciphered.

## 12. First-reveal provenance

- first-reveal head: `5e9121f7e05d8950f223298a44b816d6ee088e07`
- Actions run: `33335306504`
- job: `99321036069`
- artifact: `9738893689`
- artifact ZIP SHA-256: `058852cfc8bf5d718d200f05758d21452f45715d35a2b682f7422afc6261d8fc`
- raw result JSON SHA-256: `43b59ad8539db4cf089e6265c38f81ec9afd2f864877b77373a12adbdccdce1b`

The exact artifact was downloaded and hash-verified by a separate recording workflow before being committed to `phase64a_inventory_autonomy_results.json`.

A clean replay audit is run separately and may qualify byte-level determinism but cannot rewrite this first-reveal classification.
