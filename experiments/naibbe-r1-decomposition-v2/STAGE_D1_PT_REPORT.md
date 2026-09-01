# Issue #72 V2 — Stage D1 plaintext local-order total-effect report

## Status

**PLAINTEXT WITHIN-LINE LOCAL ORDER IS NOT A MATERIAL R1 NECESSITY UNDER PT**

Stage D1 is complete and its exact 155-case first-reveal population is permanently frozen.

This report is interpretive metadata over the frozen first-reveal authority. It does not replace the raw population.

Permanent raw authority:

- scientific first-reveal head: `02d757e36d85cdfc9231be0b8753904b3ceb543c`
- canonical first-reveal workflow run: `33494367825`
- workflow conclusion: `success`
- first-reveal artifact ID: `9795439622`
- first-reveal artifact ZIP SHA-256: `f06f6190f802411494bbae77611c803e363013a366196993913a91394c5d6852`
- aggregate SHA-256: `402941d895c020e7f93c8ccab9585d684117227836fa69d7465376a609d24de2`
- permanent-freeze workflow run: `33495408033`
- permanent-freeze workflow conclusion: `success`
- permanent-freeze commit: `0853092d1a6e5bd1dc7f922295a5cc06055fb516`
- permanent authority directory: `experiments/naibbe-r1-decomposition-v2/stage-d1-pt/`
- exact assignment results: **155/155** = 31 prospectively fixed PT assignments × 5 frozen RNG blocks
- drops: **0**
- rerolls: **0**

The permanent-freeze operation was post-reveal transport only. It did not regenerate plaintext shuffles, rerun Naibbe, rescore R1, filter assignments, add a coverage gate, or alter the frozen aggregation law.

---

## Scientific question

Does the observed local character order inside the Latin plaintext lines causally propagate through the complete Naibbe pipeline into the high Voynich-R1 residual topology match?

PT tests this by preserving the exact character inventory and count of every plaintext line while randomizing the character order within that same line, then rerunning the complete Naibbe mechanism and measuring R1.

The intervention therefore keeps line composition and line length fixed while destroying local plaintext sequence.

A systematic negative displacement of R1 would support a material contribution from local plaintext order. A distribution centered near zero would show that the high R1 resemblance does not require the observed local order under this intervention.

---

## Frozen population and chronology

The PT population was fixed target-blind before Stage D1 target scoring:

- 31 fixed PT assignments;
- 5 fixed Naibbe RNG blocks per assignment;
- 155 total cases;
- no target-dependent replacement, deletion, reroll, or support gate;
- target remained inaccessible during D0 generation and successful D1 preflight.

Successful target-blind preflight:

- workflow run: `33494182268`
- preflight head: `0bc909526d5c41f0e31ab5d9f062f92f18b06ff3`
- boundary cases: `j0/rep0` and `j30/rep4`
- exact D0 PT replay: passed
- exact B2 baseline adapter: passed
- target loaded: false
- Q/Z/R1 computed: false

Frozen authorities used by the first reveal:

- full Stage-B0 support SHA-256: `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`
- compact PT authority SHA-256: `703991a4b176e78ea18c30210ec730187b446c0c8b14052fc2d25e4a8d8f86e4`
- D0 aggregate SHA-256: `e3039ed40f72e44cc4964efab50d70bc1b113859c77e23ccc97934bb29edb9b8`
- D0 authority-rebind SHA-256: `cb80833b426d6d9b4d1f307961d862fe02140fcf8f593f870fb3080a39bfc2a0`
- B2 archive SHA-256: `2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147`

---

## Frozen R1 comparison

Each PT case is scored with the same Issue #72 R1 coordinate:

- `SlotParser(min)`;
- all 66 unordered slot pairs;
- K_other-conditioned Jeffreys-smoothed Mantel-Haenszel Yule-Q;
- candidate-owned line-local `N_ref=1000` reference null;
- empirical mid-rank normal residual Z;
- residual energy E and four-fold reliability W;
- full-topology Pearson and sign agreement against ZL3b and IT2a separately.

The unchanged Naibbe baseline is not rescored. Each `rep` uses the exact stored Stage-B2 positive-control baseline for that same RNG block.

For target `t`:

`delta_R[j,rep,t] = R_PT[j,rep,t] - R_B2[rep,t]`

and the assignment-level total effect is

`D[j,t] = mean_rep0..4(delta_R[j,rep,t])`.

No hard intervention threshold was used. ZL3b and IT2a were not averaged. Coverage was descriptive only.

---

## Complete first-reveal result

| Target | Mean D across 31 | Median D | Q25 | Q75 | Min | Max | D >= 0 | D < 0 | p_nonloss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | **+0.000879** | **+0.000827** | -0.001169 | +0.002843 | -0.011100 | +0.011594 | 19 | 12 | 0.6250 |
| IT2a | **-0.000240** | **+0.000153** | -0.001614 | +0.002388 | -0.010947 | +0.009447 | 17 | 14 | 0.5625 |

Across the same 31 assignments, joint target direction was:

- **15 both-nonnegative**;
- **10 both-negative**;
- **6 mixed**.

The frozen combined non-loss quantity is:

`p_both = max(0.6250, 0.5625) = 0.6250`.

The two target-specific D vectors are strongly concordant descriptively (`r ≈ 0.918`), so the near-zero result is not produced by one transcription showing a large systematic loss that is hidden by averaging with the other. The target readings remain separate in the formal result.

---

## Effect-size context from unchanged Naibbe variation

Stage B2 characterized ordinary unchanged-Naibbe R1 variation before PT interpretation:

| Target | B2 SD | B2 MAD | Stage D1 median D / B2 SD | Stage D1 median D / B2 MAD |
|---|---:|---:|---:|---:|
| ZL3b | 0.010907 | 0.008978 | +0.0758 | +0.0921 |
| IT2a | 0.008562 | 0.005799 | +0.0178 | +0.0263 |

The assignment-level PT displacement is therefore small relative to the pre-calibrated unchanged-Naibbe variation scale. These ratios are descriptive context, not significance thresholds.

For completeness, the mean absolute assignment-level D was approximately:

- ZL3b: `0.003702`;
- IT2a: `0.003261`.

Median absolute D was approximately `0.00216` for both readings.

---

## Representation audit

PT materially reorders the plaintext while preserving the exact linewise character inventory. D0 established that roughly 97–98% of non-empty eligible lines were actually reordered.

The resulting Naibbe surfaces remained highly representable under the frozen parser:

- minimum coverage: `0.881903`;
- Q25: `0.885721`;
- median: `0.886817`;
- mean: `0.886887`;
- Q75: `0.888131`;
- maximum: `0.891405`.

No coverage cutoff was applied and no case was removed because of its coverage or R1 outcome.

---

## Scientific interpretation

### 1. Local plaintext sequence is not a material R1 necessity under PT

The observed Latin character order inside each line was extensively destroyed while every line retained the same character multiset and length. After the full downstream Naibbe pipeline was rerun, the R1 topology did not show a systematic loss against either independent Voynich reading.

The central displacement is essentially zero on the calibrated R1 scale:

- ZL3b median D `+0.000827`;
- IT2a median D `+0.000153`.

The assignment directions are also inconsistent with a necessary local-order contribution: only 10 of 31 assignments lowered both readings, while 15 raised or preserved both and 6 were mixed.

Within the frozen PT estimand, the high Naibbe/Voynich R1 resemblance therefore does not require the observed local plaintext order.

### 2. This narrows the causal location identified by Stage C1

Stage C1 showed large, systematic R1 losses when structured emitted-value associations were destroyed:

- EL median D: about `-0.247 / -0.254`;
- ES: about `-0.214 / -0.234`;
- EG: about `-0.334 / -0.368`;
- ET was much weaker and mixed.

Stage D1 changes a different causal layer and gives D values near zero. These are different intervention families, so their magnitudes should not be treated as additive coefficients. The qualitative localization is nevertheless strong:

> **Naibbe's R1 resemblance is much more tightly tied to the structured emission/codebook architecture than to the exact local order of the plaintext characters that drive it.**

The current compact mechanistic description remains:

> **effective-letter × functional-state -> emitted glyph value**

with the added Stage D1 constraint that this scaffold can generate essentially the same R1 topology across extensive within-line plaintext-order rearrangement.

### 3. Composition remains a live upstream possibility

PT preserves each line's exact character inventory. It therefore does not test whether plaintext character frequencies, linewise composition, manuscript-level composition, or other global input statistics contribute to the downstream topology.

Stage D1 localizes away from **sequence order**, not away from every property of the plaintext input.

---

## What Stage D1 does not establish

Stage D1 does **not** establish:

- that plaintext semantics are generally irrelevant;
- that Latin is or is not the Voynich plaintext;
- that plaintext character composition is irrelevant;
- that the Voynich Manuscript was generated by Naibbe;
- that Naibbe is a historical cipher candidate;
- that R1 alone constitutes decipherment evidence;
- that the C1 factors are independent or additive;
- that final complete-token inventory alone is sufficient.

The last question is the preregistered FI allocation experiment.

---

## Relation to the next preregistered test: FI

`STAGE_C1_FI_PLAN.md` was preregistered before FI R1 randomization scoring. It tests whether the exact final complete-token inventory is sufficient once token identities are reassigned to manuscript/line slots.

Its two fixed randomization families are:

- **FI-G**: global permutation of all 33,574 complete token instances over the frozen token slots;
- **FI-M**: independent within-manuscript permutation of complete token instances.

The frozen primary statistic is `T = min(R_ZL3b, R_IT2a)`, with 199 randomizations per family and Holm correction across exactly the two promoting allocation questions.

Stage D1 does not alter that preregistration or its decision map.

---

## Criterion-validity status

- Stage D1 PT intervention population: **COMPLETE / TARGET-BLINDLY FROZEN BEFORE REVEAL**
- exact 155-case first-reveal population: **PERMANENTLY FROZEN AUTHORITY**
- drops / rerolls / target-dependent case selection: **NONE**
- baseline pairing: **EXACT STORED B2 PER-REP AUTHORITY; NOT RESCORED**
- ZL3b and IT2a: **SEPARATE REPLICATION READINGS**
- parser coverage: **DESCRIPTIVE; NO GATE**
- B2 SD/MAD: **DESCRIPTIVE EFFECT-SIZE CONTEXT; NO THRESHOLD**
- within-line plaintext local order as material R1 necessity under PT: **NOT SUPPORTED**
- broader plaintext composition/semantics inference: **NOT AUTHORIZED**
- final-token allocation sufficiency: **UNRESOLVED; FI IS NEXT**
